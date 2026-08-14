from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = RESULTS / "crops"

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png"
MASK = ROOT / "wires_mask.png"
OVERLAY = ROOT / "wires_mask_overlay.png"


def image_tokens_expected(path: Path) -> int:
    """Approximate high-detail tiled vision tokens; not an official API count."""
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
    CROPS / "raw_01_generator_switchyard.png",
    CROPS / "raw_02_medium_voltage_buses.png",
    CROPS / "raw_03_480_load_center_a.png",
    CROPS / "raw_04_480_load_center_b.png",
    CROPS / "raw_05_non_safety_480.png",
    CROPS / "raw_05b_non_safety_loads.png",
    CROPS / "raw_06_dc_ups_distribution.png",
    CROPS / "raw_07_esfas_rps_control_bay.png",
    CROPS / "raw_08_line_types_notes_title.png",
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
        "document": "6",
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
            "main-agent-aggregate",
            "Main agent",
            "orchestration",
            "Inventory resources, inspect images/crops, generate artifacts, validate matrices",
            input_text_expected=22_000,
            image_paths=MAIN_VIEWED_IMAGES,
            output_expected=3_000,
            cached_expected=18_000,
            notes="Aggregate estimate; platform did not expose individual main-agent usage objects.",
        ),
        call_row(
            "diego-r1",
            "Diego",
            "Round 1",
            "High-recall extraction from raw/mask/overlay",
            input_text_expected=320,
            image_paths=SUBAGENT_IMAGES,
            output_expected=5_800,
            notes="Initial subagent call with three full-page images.",
        ),
        call_row(
            "jennifer-r1",
            "Jennifer",
            "Round 1",
            "Precision review/refinement of Diego Round 1",
            input_text_expected=7_600,
            image_paths=SUBAGENT_IMAGES,
            output_expected=4_400,
            notes="Prompt included Diego's 105-node proposal and full edge list plus images.",
        ),
        call_row(
            "diego-r2",
            "Diego",
            "Round 2",
            "Reconcile with Jennifer precision edits",
            input_text_expected=1_100,
            image_paths=SUBAGENT_IMAGES,
            output_expected=450,
            cached_expected=12_000,
            notes="Same Diego context; cached image/context tokens likely but not exposed.",
        ),
        call_row(
            "jennifer-r2",
            "Jennifer",
            "Round 2",
            "Final precision confirmation",
            input_text_expected=420,
            image_paths=SUBAGENT_IMAGES,
            output_expected=160,
            cached_expected=14_000,
            notes="Same Jennifer context; cached image/context tokens likely but not exposed.",
        ),
    ]

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate\n\n")
        handle.write("Document: 6\n\n")
        handle.write("Iteration: 1\n\n")
        handle.write(f"Low estimate: {total_low:,} tokens\n\n")
        handle.write(f"Expected estimate: {total_expected:,} tokens\n\n")
        handle.write(f"High estimate: {total_high:,} tokens\n\n")
        handle.write(
            "The OpenAI Responses input-token counting endpoint was not called because "
            "`OPENAI_API_KEY` was not present in the environment. The multi-agent tool did "
            "not expose response usage objects, cached-input counts, or reasoning-token "
            "details. Text counts use a simple 4 characters/token heuristic; image/file "
            "counts use the tiled vision heuristic implemented in this script.\n"
        )


if __name__ == "__main__":
    main()
