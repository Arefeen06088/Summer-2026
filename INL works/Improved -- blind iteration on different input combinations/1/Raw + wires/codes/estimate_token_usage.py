from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


RAW = ROOT / "raw -- schematic_image_clean_100_connected.png"
MASK = ROOT / "wires_mask.png"
OVERLAY = ROOT / "wires_mask_overlay.png"
CROPS = RESULTS / "crops"


def image_tokens_expected(path: Path) -> int:
    """Rough high-detail tiled vision estimate, not an official API count."""
    with Image.open(path) as image:
        width, height = image.size
    scale = min(1.0, 2048 / max(width, height))
    scaled_width = math.ceil(width * scale)
    scaled_height = math.ceil(height * scale)
    tiles = math.ceil(scaled_width / 512) * math.ceil(scaled_height / 512)
    return 85 + 170 * tiles


def image_token_range(paths: Iterable[Path]) -> tuple[int, int, int]:
    expected = sum(image_tokens_expected(path) for path in paths)
    return math.ceil(expected * 0.65), expected, math.ceil(expected * 1.35)


def text_range(expected: int) -> tuple[int, int, int]:
    return math.ceil(expected * 0.75), expected, math.ceil(expected * 1.35)


SUBAGENT_IMAGES = [RAW, MASK, OVERLAY]
MAIN_VIEWED_IMAGES = [
    RAW,
    OVERLAY,
    CROPS / "raw_01_ac_train_a.png",
    CROPS / "raw_02_ac_train_b.png",
    CROPS / "raw_03_ac_train_c.png",
    CROPS / "raw_04_480_loads_a.png",
    CROPS / "raw_05_480_loads_b.png",
    CROPS / "raw_06_480_loads_c.png",
    CROPS / "raw_07_dc_ac_control_power.png",
    CROPS / "raw_08_bus_tie_a_b.png",
    CROPS / "raw_09_bus_tie_b_c.png",
    MASK,
]


def call_row(
    call_id: str,
    actor: str,
    round_name: str,
    purpose: str,
    input_text_expected: int,
    image_paths: list[Path],
    output_expected: int,
    cached_expected: int = 0,
    notes: str = "",
) -> dict[str, object]:
    text_low, text_exp, text_high = text_range(input_text_expected)
    image_low, image_exp, image_high = image_token_range(image_paths)
    output_low, output_exp, output_high = text_range(output_expected)
    return {
        "document": "1",
        "iteration": "1",
        "call_id": call_id,
        "actor": actor,
        "model": "gpt-5.5 for subagents; main model as configured by session",
        "round": round_name,
        "purpose": purpose,
        "input_text_tokens_low": text_low,
        "input_text_tokens_expected": text_exp,
        "input_text_tokens_high": text_high,
        "cached_input_tokens_estimated": cached_expected,
        "image_file_tokens_low": image_low,
        "image_file_tokens_expected": image_exp,
        "image_file_tokens_high": image_high,
        "output_tokens_low": output_low,
        "output_tokens_expected": output_exp,
        "output_tokens_high": output_high,
        "reasoning_tokens_recorded": "not available",
        "usage_object_available": "no",
        "total_tokens_low": text_low + image_low + output_low,
        "total_tokens_expected": text_exp + image_exp + output_exp,
        "total_tokens_high": text_high + image_high + output_high,
        "notes": notes,
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    rows = [
        call_row(
            call_id="main-agent-aggregate",
            actor="Main agent",
            round_name="orchestration",
            purpose="Inventory resources, inspect images/crops, generate artifacts, validate matrices",
            input_text_expected=18_000,
            image_paths=MAIN_VIEWED_IMAGES,
            output_expected=2_500,
            cached_expected=12_000,
            notes=(
                "Aggregate estimate only; platform did not expose individual main-agent "
                "model-call usage objects."
            ),
        ),
        call_row(
            call_id="diego-r1",
            actor="Diego",
            round_name="Round 1",
            purpose="High-recall extraction from raw/mask/overlay",
            input_text_expected=300,
            image_paths=SUBAGENT_IMAGES,
            output_expected=4_200,
            notes="Initial subagent call with three full-page images.",
        ),
        call_row(
            call_id="jennifer-r1",
            actor="Jennifer",
            round_name="Round 1",
            purpose="Precision review/refinement of Diego Round 1",
            input_text_expected=2_800,
            image_paths=SUBAGENT_IMAGES,
            output_expected=2_600,
            notes="Prompt included Diego's node and edge proposal plus three full-page images.",
        ),
        call_row(
            call_id="diego-r2",
            actor="Diego",
            round_name="Round 2",
            purpose="Reconcile with Jennifer's precision edits",
            input_text_expected=4_800,
            image_paths=SUBAGENT_IMAGES,
            output_expected=1_100,
            cached_expected=10_800,
            notes=(
                "Same Diego agent context; image/context tokens likely mostly cached, "
                "but usage object was not exposed."
            ),
        ),
        call_row(
            call_id="jennifer-r2",
            actor="Jennifer",
            round_name="Round 2",
            purpose="Final precision confirmation",
            input_text_expected=5_600,
            image_paths=SUBAGENT_IMAGES,
            output_expected=160,
            cached_expected=11_800,
            notes=(
                "Same Jennifer agent context; image/context tokens likely mostly cached, "
                "but usage object was not exposed."
            ),
        ),
    ]

    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate\n\n")
        handle.write("Document: 1\n\n")
        handle.write("Iteration: 1\n\n")
        handle.write(f"Low estimate: {total_low:,} tokens\n\n")
        handle.write(f"Expected estimate: {total_expected:,} tokens\n\n")
        handle.write(f"High estimate: {total_high:,} tokens\n\n")
        handle.write(
            "The OpenAI Responses input-token counting endpoint was not called because "
            "`OPENAI_API_KEY` was not present in the environment. The multi-agent tool "
            "did not expose response usage objects, cached-input counts, or reasoning-token "
            "details. Text counts use a 4 characters/token heuristic; image/file counts use "
            "a reproducible tiled vision heuristic implemented in `codes/estimate_token_usage.py`.\n"
        )


if __name__ == "__main__":
    main()
