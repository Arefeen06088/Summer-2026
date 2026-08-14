from __future__ import annotations

import csv
import math
import os
from dataclasses import dataclass
from pathlib import Path

import tiktoken
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CODES = ROOT / "codes"

try:
    ENCODING = tiktoken.get_encoding("o200k_base")
    TOKENIZER_NOTE = "`tiktoken` `o200k_base`"
except Exception as exc:  # Local cache/network/cert dependent.
    ENCODING = None
    TOKENIZER_NOTE = f"character-count fallback because tiktoken encoding load failed: {type(exc).__name__}"


@dataclass(frozen=True)
class CallSpec:
    call_name: str
    agent: str
    model: str
    round_name: str
    text_input_tokens_expected: int
    output_tokens_low: int
    output_tokens_expected: int
    output_tokens_high: int
    images: tuple[str, ...]
    notes: str


def text_tokens(text: str) -> int:
    if ENCODING is None:
        return max(1, math.ceil(len(text) / 4))
    return len(ENCODING.encode(text))


def image_tokens_for_size(width: int, height: int) -> tuple[int, int, int]:
    def tiles_after_resize(short_side_cap: int | None) -> int:
        w, h = float(width), float(height)
        scale = min(1.0, 2048.0 / max(w, h))
        w *= scale
        h *= scale
        if short_side_cap is not None and min(w, h) > short_side_cap:
            scale = short_side_cap / min(w, h)
            w *= scale
            h *= scale
        return math.ceil(w / 512.0) * math.ceil(h / 512.0)

    return (
        85,
        85 + 170 * tiles_after_resize(768),
        85 + 170 * tiles_after_resize(None),
    )


def image_token_sum(paths: tuple[str, ...]) -> tuple[int, int, int]:
    low = expected = high = 0
    for rel_path in paths:
        with Image.open(ROOT / rel_path) as image:
            l, e, h = image_tokens_for_size(*image.size)
        low += l
        expected += e
        high += h
    return low, expected, high


def generated_code_output_tokens() -> int:
    return sum(text_tokens(path.read_text(encoding="utf-8")) for path in sorted(CODES.glob("*.py")))


def build_calls() -> list[CallSpec]:
    main_images = (
        "raw -- schematic_image_variant_b_100.png",
        "wires_mask_overlay.png",
        "results/crops/raw_01_top_train_a_sources.png",
        "results/crops/raw_02_top_bus_tie.png",
        "results/crops/raw_03_top_train_b_sources.png",
        "results/crops/raw_04_train_a_480_feeders.png",
        "results/crops/raw_05_train_a_dc_rps.png",
        "results/crops/raw_06_cvcs_a.png",
        "results/crops/raw_07_train_b_480_feeders.png",
        "results/crops/raw_08_train_b_dc_rps.png",
        "results/crops/raw_09_cvcs_b.png",
        "results/crops/raw_10_title_notes.png",
        "results/crops/raw_11_bottom_rps_control.png",
        "results/crops/raw_12_middle_cvcs_control.png",
        "results/crops/overlay_11_bottom_rps_control.png",
        "results/crops/overlay_12_middle_cvcs_control.png",
    )
    code_tokens = generated_code_output_tokens()
    return [
        CallSpec(
            call_name="main_agent_orchestration_and_artifact_generation",
            agent="main",
            model="Codex GPT-5",
            round_name="iteration_1",
            text_input_tokens_expected=13000,
            output_tokens_low=max(4500, code_tokens - 1800),
            output_tokens_expected=code_tokens + 1300,
            output_tokens_high=code_tokens + 3800,
            images=main_images,
            notes="Aggregate estimate for main visual inspection, crop creation, scripts, QA, and final response.",
        ),
        CallSpec(
            call_name="diego_round1_high_recall_extraction",
            agent="Diego",
            model="gpt-5.5",
            round_name="round1",
            text_input_tokens_expected=900,
            output_tokens_low=2600,
            output_tokens_expected=3700,
            output_tokens_high=5200,
            images=(
                "raw -- schematic_image_variant_b_100.png",
                "wires_mask.png",
                "wires_mask_overlay.png",
            ),
            notes="Spawned with full raw, mask, overlay and high-recall instructions.",
        ),
        CallSpec(
            call_name="jennifer_round1_precision_review",
            agent="Jennifer",
            model="gpt-5.5",
            round_name="round1",
            text_input_tokens_expected=5200,
            output_tokens_low=2200,
            output_tokens_expected=3100,
            output_tokens_high=4500,
            images=(
                "raw -- schematic_image_variant_b_100.png",
                "wires_mask.png",
                "wires_mask_overlay.png",
                "results/crops/raw_01_top_train_a_sources.png",
                "results/crops/raw_02_top_bus_tie.png",
                "results/crops/raw_03_top_train_b_sources.png",
                "results/crops/raw_04_train_a_480_feeders.png",
                "results/crops/raw_05_train_a_dc_rps.png",
                "results/crops/raw_06_cvcs_a.png",
                "results/crops/raw_07_train_b_480_feeders.png",
                "results/crops/raw_08_train_b_dc_rps.png",
                "results/crops/raw_09_cvcs_b.png",
                "results/crops/raw_10_title_notes.png",
                "results/crops/raw_11_bottom_rps_control.png",
                "results/crops/raw_12_middle_cvcs_control.png",
                "results/crops/overlay_11_bottom_rps_control.png",
                "results/crops/overlay_12_middle_cvcs_control.png",
            ),
            notes="Included Diego round1 text, full images, notes crop, and control/CVCS crops.",
        ),
        CallSpec(
            call_name="diego_round2_reconciliation",
            agent="Diego",
            model="gpt-5.5",
            round_name="round2",
            text_input_tokens_expected=1700,
            output_tokens_low=1800,
            output_tokens_expected=2600,
            output_tokens_high=3800,
            images=(
                "raw -- schematic_image_variant_b_100.png",
                "wires_mask_overlay.png",
                "results/crops/raw_10_title_notes.png",
                "results/crops/raw_11_bottom_rps_control.png",
                "results/crops/raw_12_middle_cvcs_control.png",
            ),
            notes="Reconciled Jennifer corrections and final 100-node/100-edge scope.",
        ),
        CallSpec(
            call_name="jennifer_round2_final_confirmation",
            agent="Jennifer",
            model="gpt-5.5",
            round_name="round2",
            text_input_tokens_expected=650,
            output_tokens_low=350,
            output_tokens_expected=550,
            output_tokens_high=900,
            images=(
                "raw -- schematic_image_variant_b_100.png",
                "results/crops/raw_10_title_notes.png",
                "results/crops/raw_11_bottom_rps_control.png",
                "results/crops/raw_12_middle_cvcs_control.png",
            ),
            notes="Final saturation check after generated artifact QA.",
        ),
    ]


def main() -> None:
    has_api_key = bool(os.environ.get("OPENAI_API_KEY"))
    rows = []
    totals = {"low": 0, "expected": 0, "high": 0}
    for call in build_calls():
        image_low, image_expected, image_high = image_token_sum(call.images)
        input_low = int(call.text_input_tokens_expected * 0.8) + image_low
        input_expected = call.text_input_tokens_expected + image_expected
        input_high = int(call.text_input_tokens_expected * 1.25) + image_high
        total_low = input_low + call.output_tokens_low
        total_expected = input_expected + call.output_tokens_expected
        total_high = input_high + call.output_tokens_high
        totals["low"] += total_low
        totals["expected"] += total_expected
        totals["high"] += total_high
        rows.append(
            {
                "document": 2,
                "iteration": 1,
                "call_name": call.call_name,
                "agent": call.agent,
                "model": call.model,
                "round": call.round_name,
                "usage_source": "estimate_no_api_key" if not has_api_key else "estimate_api_key_present_not_called",
                "input_tokens_low": input_low,
                "input_tokens_expected": input_expected,
                "input_tokens_high": input_high,
                "cached_input_tokens": "unavailable",
                "output_tokens_low": call.output_tokens_low,
                "output_tokens_expected": call.output_tokens_expected,
                "output_tokens_high": call.output_tokens_high,
                "reasoning_tokens": "unavailable",
                "image_file_count": len(call.images),
                "image_input_tokens_low": image_low,
                "image_input_tokens_expected": image_expected,
                "image_input_tokens_high": image_high,
                "file_input_tokens": image_expected,
                "total_tokens_low": total_low,
                "total_tokens_expected": total_expected,
                "total_tokens_high": total_high,
                "notes": call.notes,
            }
        )

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Token Usage Estimate\n\n")
        f.write("No `OPENAI_API_KEY` was available, so the OpenAI Responses input-token counting endpoint was not called. ")
        f.write("The multi-agent tool did not expose usage objects, cached-token counts, or reasoning-token counts. ")
        f.write(f"Text estimate method: {TOKENIZER_NOTE}. Image estimate method: 512-tile heuristic.\n\n")
        f.write("| Document | Iteration | Calls | Low total | Expected total | High total |\n")
        f.write("|---:|---:|---:|---:|---:|---:|\n")
        f.write(f"| 2 | 1 | {len(rows)} | {totals['low']} | {totals['expected']} | {totals['high']} |\n\n")
        f.write("| Call | Input expected | Image expected | Output expected | Total expected |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for row in rows:
            f.write(
                f"| {row['call_name']} | {row['input_tokens_expected']} | "
                f"{row['image_input_tokens_expected']} | {row['output_tokens_expected']} | "
                f"{row['total_tokens_expected']} |\n"
            )


if __name__ == "__main__":
    main()
