import csv
import math
from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
OUT = RESULTS / "usage_estimates"


def patch_tokens(width, height, patch_budget, max_dimension=None):
    scale = 1.0
    if max_dimension and max(width, height) > max_dimension:
        scale = min(scale, max_dimension / max(width, height))

    if math.ceil(width * scale / 32) * math.ceil(height * scale / 32) > patch_budget:
        shrink_factor = math.sqrt((32**2 * patch_budget) / (width * height))
        scale = min(scale, shrink_factor)
        adjusted = scale * min(
            math.floor(width * scale / 32) / (width * scale / 32),
            math.floor(height * scale / 32) / (height * scale / 32),
        )
        scale = adjusted

    resized_width = max(1, math.floor(width * scale))
    resized_height = max(1, math.floor(height * scale))
    return math.ceil(resized_width / 32) * math.ceil(resized_height / 32)


def image_estimates(path):
    width, height = Image.open(path).size
    return {
        "path": path,
        "width": width,
        "height": height,
        "high_detail_tokens": patch_tokens(width, height, patch_budget=2500, max_dimension=2048),
        "original_detail_tokens": patch_tokens(width, height, patch_budget=10000, max_dimension=6000),
    }


RAW = BASE / "raw -- schematic_image_variant_b_100.png"
DETECTED = BASE / "detected_components_and_logical_overlay.png"
WIRE_MASK = BASE / "wires_mask.png"
WIRE_OVERLAY = BASE / "wires_mask_overlay.png"
CROPS = RESULTS / "visual_crops" / "raw_--_schematic_image_variant_b_100"


CALLS = [
    {
        "call_id": "main_orchestrator_aggregate",
        "agent": "main",
        "round": "all",
        "purpose": "Resource inspection, crop planning, artifact generation, saturation orchestration, final reporting",
        "images": [
            RAW,
            DETECTED,
            WIRE_OVERLAY,
            WIRE_MASK,
            CROPS / "top_left_sources_and_bus.png",
            CROPS / "top_right_sources_and_bus.png",
            CROPS / "bus_tie_center.png",
            CROPS / "left_train_loads.png",
            CROPS / "right_train_loads.png",
            CROPS / "middle_cvcs_a_and_dc_a.png",
            CROPS / "far_right_cvcs_b.png",
            CROPS / "rps_dc_ac_bottom.png",
        ],
        "text_tokens_low": 12000,
        "text_tokens_expected": 18000,
        "text_tokens_high": 30000,
        "output_tokens_low": 1800,
        "output_tokens_expected": 3000,
        "output_tokens_high": 5200,
        "reasoning_tokens_low": 5000,
        "reasoning_tokens_expected": 15000,
        "reasoning_tokens_high": 35000,
        "image_detail_expected": "high",
    },
    {
        "call_id": "diego_round1",
        "agent": "Diego",
        "round": "1",
        "purpose": "High-recall extraction from raw and derived images",
        "images": [RAW, DETECTED, WIRE_MASK, WIRE_OVERLAY],
        "text_tokens_low": 350,
        "text_tokens_expected": 550,
        "text_tokens_high": 900,
        "output_tokens_low": 4300,
        "output_tokens_expected": 5300,
        "output_tokens_high": 6800,
        "reasoning_tokens_low": 4000,
        "reasoning_tokens_expected": 10000,
        "reasoning_tokens_high": 25000,
        "image_detail_expected": "original",
    },
    {
        "call_id": "jennifer_round1",
        "agent": "Jennifer",
        "round": "1",
        "purpose": "Precision review of Diego round 1 with full proposal and crops",
        "images": [
            RAW,
            DETECTED,
            WIRE_OVERLAY,
            CROPS / "top_left_sources_and_bus.png",
            CROPS / "top_right_sources_and_bus.png",
            CROPS / "bus_tie_center.png",
            CROPS / "left_train_loads.png",
            CROPS / "right_train_loads.png",
            CROPS / "middle_cvcs_a_and_dc_a.png",
            CROPS / "far_right_cvcs_b.png",
            CROPS / "rps_dc_ac_bottom.png",
        ],
        "text_tokens_low": 2700,
        "text_tokens_expected": 3800,
        "text_tokens_high": 5400,
        "output_tokens_low": 4700,
        "output_tokens_expected": 6200,
        "output_tokens_high": 8000,
        "reasoning_tokens_low": 3500,
        "reasoning_tokens_expected": 9000,
        "reasoning_tokens_high": 22000,
        "image_detail_expected": "original",
    },
    {
        "call_id": "diego_round2",
        "agent": "Diego",
        "round": "2",
        "purpose": "Saturation check of Jennifer acceptance",
        "images": [
            RAW,
            CROPS / "bus_tie_center.png",
            CROPS / "rps_dc_ac_bottom.png",
            CROPS / "middle_cvcs_a_and_dc_a.png",
            CROPS / "far_right_cvcs_b.png",
        ],
        "text_tokens_low": 250,
        "text_tokens_expected": 450,
        "text_tokens_high": 800,
        "output_tokens_low": 70,
        "output_tokens_expected": 140,
        "output_tokens_high": 300,
        "reasoning_tokens_low": 700,
        "reasoning_tokens_expected": 2200,
        "reasoning_tokens_high": 6500,
        "image_detail_expected": "original",
    },
]


def image_token_sum(paths, mode):
    total = 0
    for path in paths:
        est = image_estimates(path)
        total += est["high_detail_tokens"] if mode == "high" else est["original_detail_tokens"]
    return total


def write_reports():
    OUT.mkdir(parents=True, exist_ok=True)

    all_images = sorted({path for call in CALLS for path in call["images"]}, key=lambda p: str(p))
    image_rows = []
    for path in all_images:
        est = image_estimates(path)
        image_rows.append(
            {
                "image": str(path.relative_to(BASE)),
                "width": est["width"],
                "height": est["height"],
                "high_detail_tokens": est["high_detail_tokens"],
                "original_detail_tokens": est["original_detail_tokens"],
            }
        )

    with (OUT / "image_token_estimates.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=image_rows[0].keys())
        writer.writeheader()
        writer.writerows(image_rows)

    call_rows = []
    for call in CALLS:
        image_low = image_token_sum(call["images"], "high")
        image_expected = image_token_sum(call["images"], call["image_detail_expected"])
        image_high = image_token_sum(call["images"], "original")
        low = (
            call["text_tokens_low"]
            + image_low
            + call["output_tokens_low"]
            + call["reasoning_tokens_low"]
        )
        expected = (
            call["text_tokens_expected"]
            + image_expected
            + call["output_tokens_expected"]
            + call["reasoning_tokens_expected"]
        )
        high = (
            call["text_tokens_high"]
            + image_high
            + call["output_tokens_high"]
            + call["reasoning_tokens_high"]
        )
        call_rows.append(
            {
                "document": "2 / Raw + wires + components",
                "iteration": "1",
                "call_id": call["call_id"],
                "agent": call["agent"],
                "round": call["round"],
                "purpose": call["purpose"],
                "input_text_tokens_low": call["text_tokens_low"],
                "input_text_tokens_expected": call["text_tokens_expected"],
                "input_text_tokens_high": call["text_tokens_high"],
                "image_file_tokens_low": image_low,
                "image_file_tokens_expected": image_expected,
                "image_file_tokens_high": image_high,
                "cached_input_tokens": "not exposed; assumed 0 in estimates",
                "output_tokens_low": call["output_tokens_low"],
                "output_tokens_expected": call["output_tokens_expected"],
                "output_tokens_high": call["output_tokens_high"],
                "reasoning_tokens_low": call["reasoning_tokens_low"],
                "reasoning_tokens_expected": call["reasoning_tokens_expected"],
                "reasoning_tokens_high": call["reasoning_tokens_high"],
                "total_tokens_low": low,
                "total_tokens_expected": expected,
                "total_tokens_high": high,
                "usage_object": "not exposed by Codex subagent/tool runtime",
            }
        )

    with (OUT / "model_call_token_estimates.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=call_rows[0].keys())
        writer.writeheader()
        writer.writerows(call_rows)

    summary = {
        "document": "2 / Raw + wires + components",
        "iteration": "1",
        "model_calls_identified": len(call_rows),
        "input_text_tokens_expected": sum(int(r["input_text_tokens_expected"]) for r in call_rows),
        "image_file_tokens_expected": sum(int(r["image_file_tokens_expected"]) for r in call_rows),
        "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in call_rows),
        "reasoning_tokens_expected": sum(int(r["reasoning_tokens_expected"]) for r in call_rows),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in call_rows),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in call_rows),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in call_rows),
    }
    with (OUT / "iteration_token_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=summary.keys())
        writer.writeheader()
        writer.writerow(summary)

    methodology = f"""# Token Usage Estimate Methodology

The exact OpenAI Responses `usage` objects were not exposed by the Codex main-agent or subagent tools in this run.

The official OpenAI input token counting endpoint is `POST /responses/input_tokens`.
It was not called because no API key was available in this environment. If an API key is added later, that endpoint should replace these estimates.

Offline method used here:

- Text tokens: approximate ranges from prompt/response character volume and visible payload size.
- Image/file input tokens: patch-count estimates from actual image dimensions.
- Main-agent image views used high-detail estimates because `view_image` was called with `detail=high`.
- Subagent `local_image` detail is not exposed; expected uses GPT-5.5-style omitted/auto-or-original behavior, with high-detail as the low bound.
- Cached input tokens and exact reasoning tokens are not exposed; cached tokens are treated as 0 for totals, and reasoning tokens are low/expected/high estimates.

Expected total tokens for document 2, iteration 1: {summary['total_tokens_expected']}.
Low/high range: {summary['total_tokens_low']} - {summary['total_tokens_high']}.
"""
    (OUT / "token_usage_methodology.md").write_text(methodology, encoding="utf-8")


if __name__ == "__main__":
    write_reports()
    print(f"Wrote usage estimates to {OUT}")
