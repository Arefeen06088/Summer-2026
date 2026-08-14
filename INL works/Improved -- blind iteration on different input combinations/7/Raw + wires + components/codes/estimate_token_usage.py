from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = RESULTS / "visual_crops"
RAW_CROPS = CROPS / "raw____synthetic_npp_electrical_schematic_clean__1_"
FOCUSED = CROPS / "focused"


def text_tokens_from_chars(chars: int) -> int:
    # Reproducible offline approximation used because no API key/token endpoint is available.
    return math.ceil(chars / 4)


def image_tokens_high_detail(path: Path) -> int:
    """Approximate high-detail vision token cost using the common 512-tile method."""
    with Image.open(path) as img:
        width, height = img.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    short = min(width, height)
    if short > 0:
        rescale = 768 / short
        width *= rescale
        height *= rescale
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def summarize_images(paths: list[Path]) -> tuple[int, list[dict]]:
    items = []
    total = 0
    for path in paths:
        tokens = image_tokens_high_detail(path)
        total += tokens
        with Image.open(path) as img:
            width, height = img.size
        items.append(
            {
                "path": str(path),
                "width": width,
                "height": height,
                "estimated_image_tokens": tokens,
            }
        )
    return total, items


FULL_RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_clean (1).png"
FULL_OVERLAY = ROOT / "detected_components_and_logical_overlay.png"
FULL_WIRES_OVERLAY = ROOT / "wires_mask_overlay.png"


CALLS = [
    {
        "call_id": "main-setup-and-resource-check",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 18000,
        "images": [],
        "output_low": 600,
        "output_expected": 1200,
        "output_high": 2200,
        "notes": "Directory/file inspection, crop planning, no GT/OCR check. Exact Codex main-call usage is not exposed.",
    },
    {
        "call_id": "main-visual-review",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 9000,
        "images": [
            RAW_CROPS / "top_aux_power_and_sources.png",
            RAW_CROPS / "left_train_ab_loads.png",
            RAW_CROPS / "right_train_cd_loads.png",
            RAW_CROPS / "left_train_a_dc_control.png",
            RAW_CROPS / "right_train_b_dc_control.png",
            RAW_CROPS / "bottom_interlock_raceways.png",
            CROPS / "detected_components_and_logical_overlay" / "top_aux_power_and_sources.png",
            CROPS / "detected_components_and_logical_overlay" / "left_train_ab_loads.png",
            CROPS / "detected_components_and_logical_overlay" / "right_train_cd_loads.png",
            RAW_CROPS / "title_legend_notes.png",
            FOCUSED / "top_left_offsite_satA.png",
            FOCUSED / "top_right_satB_dgB.png",
            FOCUSED / "bus4_tie_middle.png",
            FOCUSED / "a_battery_charger_zoom.png",
            FOCUSED / "b_battery_charger_zoom.png",
            FOCUSED / "a_control_center_zoom.png",
            FOCUSED / "b_control_center_zoom.png",
            FOCUSED / "a_control_full_zoom.png",
            FOCUSED / "b_control_full_zoom.png",
            FOCUSED / "raceways_lower_full.png",
            FOCUSED / "mcc_a_b_control_taps.png",
        ],
        "output_low": 1400,
        "output_expected": 2600,
        "output_high": 4500,
        "notes": "Main-agent visual inspection batches aggregated; individual internal model-call boundaries are not exposed.",
    },
    {
        "call_id": "diego-r1-high-recall",
        "actor": "Diego",
        "round": 1,
        "text_chars": 2100,
        "images": [
            FULL_RAW,
            FULL_OVERLAY,
            FULL_WIRES_OVERLAY,
            RAW_CROPS / "top_aux_power_and_sources.png",
            RAW_CROPS / "left_train_ab_loads.png",
            RAW_CROPS / "right_train_cd_loads.png",
            RAW_CROPS / "left_train_a_dc_control.png",
            RAW_CROPS / "right_train_b_dc_control.png",
            RAW_CROPS / "bottom_interlock_raceways.png",
            CROPS / "detected_components_and_logical_overlay" / "whole_functional_area.png",
            CROPS / "wires_mask_overlay" / "whole_functional_area.png",
        ],
        "output_low": 6500,
        "output_expected": 8500,
        "output_high": 11500,
        "notes": "Subagent output was captured by the tool, but the model usage object was not exposed.",
    },
    {
        "call_id": "jennifer-r1-precision",
        "actor": "Jennifer",
        "round": 2,
        "text_chars": 14500,
        "images": [
            FULL_RAW,
            FULL_OVERLAY,
            FULL_WIRES_OVERLAY,
            RAW_CROPS / "top_aux_power_and_sources.png",
            RAW_CROPS / "left_train_ab_loads.png",
            RAW_CROPS / "right_train_cd_loads.png",
            RAW_CROPS / "left_train_a_dc_control.png",
            RAW_CROPS / "right_train_b_dc_control.png",
            RAW_CROPS / "bottom_interlock_raceways.png",
            CROPS / "detected_components_and_logical_overlay" / "whole_functional_area.png",
            CROPS / "wires_mask_overlay" / "whole_functional_area.png",
        ],
        "output_low": 6200,
        "output_expected": 8200,
        "output_high": 11000,
        "notes": "Input includes Diego R1 proposal summary plus image set.",
    },
    {
        "call_id": "diego-r2-saturation",
        "actor": "Diego",
        "round": 3,
        "text_chars": 4200,
        "images": [
            FULL_RAW,
            FOCUSED / "top_left_offsite_satA.png",
            FOCUSED / "top_right_satB_dgB.png",
            FOCUSED / "bus4_tie_middle.png",
            FOCUSED / "a_control_full_zoom.png",
            FOCUSED / "b_control_full_zoom.png",
            FOCUSED / "raceways_lower_full.png",
        ],
        "output_low": 3800,
        "output_expected": 5200,
        "output_high": 7200,
        "notes": "Saturation review; output is the 120-node/140-edge final candidate.",
    },
    {
        "call_id": "jennifer-r2-final-signoff",
        "actor": "Jennifer",
        "round": 4,
        "text_chars": 16500,
        "images": [
            FULL_RAW,
            FOCUSED / "a_control_full_zoom.png",
            FOCUSED / "b_control_full_zoom.png",
            FOCUSED / "raceways_lower_full.png",
        ],
        "output_low": 200,
        "output_expected": 700,
        "output_high": 2200,
        "notes": "Final agree/disagree check. Expected output is short if saturated.",
    },
    {
        "call_id": "main-artifact-generation-and-final",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 24000,
        "images": [],
        "output_low": 1200,
        "output_expected": 2200,
        "output_high": 4200,
        "notes": "Script generation, validation, final response. Exact Codex usage is not exposed.",
    },
]


def enrich_call(call: dict) -> dict:
    text_input = text_tokens_from_chars(call["text_chars"])
    image_input, image_items = summarize_images(call["images"])
    expected_input = text_input + image_input
    low_total = math.ceil(text_input * 0.85 + image_input * 0.75 + call["output_low"])
    expected_total = expected_input + call["output_expected"]
    high_total = math.ceil(text_input * 1.25 + image_input * 1.35 + call["output_high"])
    enriched = {
        "document": 7,
        "iteration": 1,
        "call_id": call["call_id"],
        "actor": call["actor"],
        "round": call["round"],
        "input_tokens_est": expected_input,
        "cached_input_tokens": None,
        "output_tokens_low": call["output_low"],
        "output_tokens_expected": call["output_expected"],
        "output_tokens_high": call["output_high"],
        "reasoning_tokens": None,
        "image_file_input_tokens_est": image_input,
        "text_input_tokens_est": text_input,
        "total_tokens_low": low_total,
        "total_tokens_expected": expected_total,
        "total_tokens_high": high_total,
        "usage_object_available": False,
        "image_inputs": image_items,
        "notes": call["notes"],
    }
    return enriched


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    enriched = [enrich_call(call) for call in CALLS]
    totals = {
        "document": 7,
        "iteration": 1,
        "method": "offline estimate; no API key, no Responses input-token counting endpoint call",
        "input_tokens_est": sum(row["input_tokens_est"] for row in enriched),
        "image_file_input_tokens_est": sum(row["image_file_input_tokens_est"] for row in enriched),
        "text_input_tokens_est": sum(row["text_input_tokens_est"] for row in enriched),
        "output_tokens_low": sum(row["output_tokens_low"] for row in enriched),
        "output_tokens_expected": sum(row["output_tokens_expected"] for row in enriched),
        "output_tokens_high": sum(row["output_tokens_high"] for row in enriched),
        "total_tokens_low": sum(row["total_tokens_low"] for row in enriched),
        "total_tokens_expected": sum(row["total_tokens_expected"] for row in enriched),
        "total_tokens_high": sum(row["total_tokens_high"] for row in enriched),
        "cached_input_tokens": None,
        "reasoning_tokens": None,
    }
    payload = {
        "limitations": [
            "No OpenAI API key was available, so the Responses input-token counting endpoint could not be called.",
            "The Codex/subagent tool responses did not expose usage objects, cached input tokens, or reasoning tokens.",
            "Text tokens use chars/4 approximation because tiktoken is not installed in this environment.",
            "Image tokens use a high-detail 512-tile approximation from actual image dimensions.",
        ],
        "calls": enriched,
        "totals": totals,
    }
    (RESULTS / "token_usage_estimate.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    csv_path = RESULTS / "token_usage_estimate.csv"
    fieldnames = [
        "document",
        "iteration",
        "call_id",
        "actor",
        "round",
        "text_input_tokens_est",
        "image_file_input_tokens_est",
        "input_tokens_est",
        "cached_input_tokens",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_object_available",
        "notes",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in enriched:
            writer.writerow({key: row.get(key) for key in fieldnames})

    md_lines = [
        "# Token Usage Estimate - Document 7",
        "",
        "No API key was available; endpoint and exact usage-object collection were not possible.",
        "",
        "| Document | Iteration | Call | Actor | Text In | Image/File In | Input Est | Output Low | Output Exp | Output High | Total Low | Total Exp | Total High |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in enriched:
        md_lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call_id']} | {row['actor']} | "
            f"{row['text_input_tokens_est']} | {row['image_file_input_tokens_est']} | {row['input_tokens_est']} | "
            f"{row['output_tokens_low']} | {row['output_tokens_expected']} | {row['output_tokens_high']} | "
            f"{row['total_tokens_low']} | {row['total_tokens_expected']} | {row['total_tokens_high']} |"
        )
    md_lines.append(
        f"| {totals['document']} | {totals['iteration']} | TOTAL | all | "
        f"{totals['text_input_tokens_est']} | {totals['image_file_input_tokens_est']} | {totals['input_tokens_est']} | "
        f"{totals['output_tokens_low']} | {totals['output_tokens_expected']} | {totals['output_tokens_high']} | "
        f"{totals['total_tokens_low']} | {totals['total_tokens_expected']} | {totals['total_tokens_high']} |"
    )
    (RESULTS / "token_usage_estimate.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
