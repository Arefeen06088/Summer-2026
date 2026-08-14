from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = RESULTS / "visual_crops"
RAW_CROPS = CROPS / "raw_--_synthetic_npp_schematic_improved_local_refined_v3"
DETECTED_CROPS = CROPS / "detected_components_overlay"
WIRE_OVERLAY_CROPS = CROPS / "wires_mask_overlay"
FOCUSED = CROPS / "focused_raw"

FULL_RAW = ROOT / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
FULL_DETECTED = ROOT / "detected_components_overlay.png"
FULL_WIRES_OVERLAY = ROOT / "wires_mask_overlay.png"


def text_tokens_from_chars(chars: int) -> int:
    # Offline approximation because no API key/token-count endpoint is available.
    return math.ceil(chars / 4)


def image_tokens_high_detail(path: Path) -> int:
    """Approximate high-detail vision input with the common 512-tile method."""
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
    total = 0
    items = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
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


CALLS = [
    {
        "call_id": "main-01-resource-check-and-crop-setup",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 16000,
        "images": [],
        "output_low": 500,
        "output_expected": 1100,
        "output_high": 2200,
        "notes": "Directory inspection, no-GT check, crop-script planning, and initial orchestration. Exact Codex main usage was not exposed.",
    },
    {
        "call_id": "main-02-local-visual-review-and-agent-briefing",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 12000,
        "images": [
            RAW_CROPS / "whole_schematic_area.png",
            RAW_CROPS / "top_normal_source_and_terminals.png",
            RAW_CROPS / "middle_4160v_buses_and_generators.png",
            RAW_CROPS / "left_train_a_loads.png",
            RAW_CROPS / "center_train_a_dc_control.png",
            RAW_CROPS / "right_train_b_loads.png",
            RAW_CROPS / "right_train_b_dc_control.png",
            RAW_CROPS / "bottom_interlock_controls.png",
            RAW_CROPS / "title_legend_notes.png",
            FOCUSED / "left_jb_k1_zoom.png",
            FOCUSED / "right_jb_k1_zoom.png",
            FOCUSED / "left_cb_interlocks_zoom.png",
            FOCUSED / "right_cb_interlocks_zoom.png",
        ],
        "output_low": 1000,
        "output_expected": 2200,
        "output_high": 4200,
        "notes": "Main visual observations and prompt preparation for Diego/Jennifer. Grouped because internal model-call boundaries are unavailable.",
    },
    {
        "call_id": "diego-r1-high-recall-extraction",
        "actor": "Diego",
        "round": 1,
        "text_chars": 2600,
        "images": [
            FULL_RAW,
            FULL_DETECTED,
            FULL_WIRES_OVERLAY,
            RAW_CROPS / "top_normal_source_and_terminals.png",
            RAW_CROPS / "middle_4160v_buses_and_generators.png",
            RAW_CROPS / "left_train_a_loads.png",
            RAW_CROPS / "center_train_a_dc_control.png",
            RAW_CROPS / "right_train_b_loads.png",
            RAW_CROPS / "right_train_b_dc_control.png",
            RAW_CROPS / "bottom_interlock_controls.png",
            DETECTED_CROPS / "whole_schematic_area.png",
            WIRE_OVERLAY_CROPS / "whole_schematic_area.png",
        ],
        "output_low": 5500,
        "output_expected": 7600,
        "output_high": 10500,
        "notes": "High-recall node/edge extraction. Tool returned text but no usage object, cached tokens, or reasoning tokens.",
    },
    {
        "call_id": "jennifer-r1-precision-review",
        "actor": "Jennifer",
        "round": 2,
        "text_chars": 16500,
        "images": [
            FULL_RAW,
            FULL_DETECTED,
            FULL_WIRES_OVERLAY,
            RAW_CROPS / "top_normal_source_and_terminals.png",
            RAW_CROPS / "middle_4160v_buses_and_generators.png",
            RAW_CROPS / "left_train_a_loads.png",
            RAW_CROPS / "center_train_a_dc_control.png",
            RAW_CROPS / "right_train_b_loads.png",
            RAW_CROPS / "right_train_b_dc_control.png",
            RAW_CROPS / "bottom_interlock_controls.png",
            FOCUSED / "left_jb_k1_zoom.png",
            FOCUSED / "right_jb_k1_zoom.png",
        ],
        "output_low": 7600,
        "output_expected": 10300,
        "output_high": 13700,
        "notes": "Precision review of Diego R1 and rejected uncertain candidates. Output is known only as returned text, not model usage.",
    },
    {
        "call_id": "main-03-resume-and-artifact-prep",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 21000,
        "images": [],
        "output_low": 800,
        "output_expected": 1800,
        "output_high": 3200,
        "notes": "Continuation, filesystem inspection, script generation, and mechanical validation.",
    },
    {
        "call_id": "diego-r2-saturation-check",
        "actor": "Diego",
        "round": 3,
        "text_chars": 2900,
        "images": [
            FULL_RAW,
            FULL_DETECTED,
            FULL_WIRES_OVERLAY,
            FOCUSED / "left_jb_k1_zoom.png",
            FOCUSED / "right_jb_k1_zoom.png",
            FOCUSED / "left_cb_interlocks_zoom.png",
            FOCUSED / "right_cb_interlocks_zoom.png",
        ],
        "output_low": 180,
        "output_expected": 260,
        "output_high": 450,
        "notes": "Saturation check of Jennifer's three additions and rejected uncertain edges; returned a short agreement response.",
    },
    {
        "call_id": "jennifer-r2-final-signoff",
        "actor": "Jennifer",
        "round": 4,
        "text_chars": 5200,
        "images": [
            FULL_RAW,
            FOCUSED / "left_jb_k1_zoom.png",
            FOCUSED / "right_jb_k1_zoom.png",
            FOCUSED / "left_cb_interlocks_zoom.png",
            FOCUSED / "right_cb_interlocks_zoom.png",
        ],
        "output_low": 90,
        "output_expected": 150,
        "output_high": 300,
        "notes": "Final agree/disagree sign-off after Diego R2; returned a short SATURATED / AGREED response.",
    },
    {
        "call_id": "main-04-final-validation-and-response",
        "actor": "Main",
        "round": "orchestration",
        "text_chars": 18000,
        "images": [],
        "output_low": 900,
        "output_expected": 1700,
        "output_high": 3200,
        "notes": "Final artifact validation, token table summary, and response to user.",
    },
]


def enrich_call(call: dict) -> dict:
    text_input = text_tokens_from_chars(call["text_chars"])
    image_input, image_items = summarize_images(call["images"])
    expected_input = text_input + image_input
    low_total = math.ceil(text_input * 0.85 + image_input * 0.75 + call["output_low"])
    expected_total = expected_input + call["output_expected"]
    high_total = math.ceil(text_input * 1.25 + image_input * 1.35 + call["output_high"])
    return {
        "document": 8,
        "iteration": 1,
        "call_id": call["call_id"],
        "actor": call["actor"],
        "round": call["round"],
        "text_input_tokens_est": text_input,
        "image_file_input_tokens_est": image_input,
        "input_tokens_est": expected_input,
        "cached_input_tokens": None,
        "output_tokens_low": call["output_low"],
        "output_tokens_expected": call["output_expected"],
        "output_tokens_high": call["output_high"],
        "reasoning_tokens": None,
        "total_tokens_low": low_total,
        "total_tokens_expected": expected_total,
        "total_tokens_high": high_total,
        "usage_object_available": False,
        "image_inputs": image_items,
        "notes": call["notes"],
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    enriched = [enrich_call(call) for call in CALLS]
    totals = {
        "document": 8,
        "iteration": 1,
        "method": "offline estimate; no API key, so no Responses input-token counting endpoint call",
        "text_input_tokens_est": sum(row["text_input_tokens_est"] for row in enriched),
        "image_file_input_tokens_est": sum(row["image_file_input_tokens_est"] for row in enriched),
        "input_tokens_est": sum(row["input_tokens_est"] for row in enriched),
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
            "Text tokens use chars/4 approximation.",
            "Image/file input tokens use a high-detail 512-tile approximation from actual image dimensions.",
            "Visible workflow calls are grouped where exact internal main-agent model-call boundaries are unavailable.",
        ],
        "calls": enriched,
        "totals": totals,
    }

    (RESULTS / "token_usage_estimate.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

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
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in enriched:
            writer.writerow({key: row.get(key) for key in fieldnames})

    md_lines = [
        "# Token Usage Estimate - Document 8",
        "",
        "No API key was available; endpoint counting and exact usage-object collection were not possible.",
        "",
        "| Document | Iteration | Call | Actor | Round | Text In | Image/File In | Input Est | Output Low | Output Exp | Output High | Total Low | Total Exp | Total High |",
        "|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in enriched:
        md_lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call_id']} | {row['actor']} | {row['round']} | "
            f"{row['text_input_tokens_est']} | {row['image_file_input_tokens_est']} | {row['input_tokens_est']} | "
            f"{row['output_tokens_low']} | {row['output_tokens_expected']} | {row['output_tokens_high']} | "
            f"{row['total_tokens_low']} | {row['total_tokens_expected']} | {row['total_tokens_high']} |"
        )
    md_lines.append(
        f"| {totals['document']} | {totals['iteration']} | TOTAL | all | all | "
        f"{totals['text_input_tokens_est']} | {totals['image_file_input_tokens_est']} | {totals['input_tokens_est']} | "
        f"{totals['output_tokens_low']} | {totals['output_tokens_expected']} | {totals['output_tokens_high']} | "
        f"{totals['total_tokens_low']} | {totals['total_tokens_expected']} | {totals['total_tokens_high']} |"
    )
    (RESULTS / "token_usage_estimate.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
