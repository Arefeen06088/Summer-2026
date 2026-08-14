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


RAW = BASE / "raw -- synthetic_npp_100_component_electrical_schematic.png"
DETECTED = BASE / "detected_components_and_logical_overlay.png"
WIRE_MASK = BASE / "wires_mask.png"
WIRE_OVERLAY = BASE / "wires_mask_overlay.png"
RAW_CROPS = RESULTS / "visual_crops" / "raw_--_synthetic_npp_100_component_electrical_schematic"
OVERLAY_CROPS = RESULTS / "visual_crops" / "detected_components_and_logical_overlay"


CALLS = [
    {
        "call_id": "main_orchestrator_aggregate",
        "agent": "main",
        "round": "all",
        "purpose": (
            "Resource inspection, crop generation, independent visual checks, "
            "subagent orchestration, artifact generation, and final reporting"
        ),
        "images": [
            RAW,
            DETECTED,
            WIRE_MASK,
            WIRE_OVERLAY,
            RAW_CROPS / "top_left_sources_bus_a.png",
            RAW_CROPS / "top_right_sources_bus_b.png",
            RAW_CROPS / "central_dc_ups.png",
            RAW_CROPS / "mccs_and_feed_buses.png",
            RAW_CROPS / "left_feeders_a1_a2.png",
            RAW_CROPS / "right_feeders_b1_b2.png",
            RAW_CROPS / "bottom_interlocks_a.png",
            RAW_CROPS / "bottom_interlocks_b.png",
            RAW_CROPS / "bus_tie_and_ground.png",
            OVERLAY_CROPS / "bottom_interlocks_a.png",
            OVERLAY_CROPS / "bus_tie_and_ground.png",
        ],
        "text_tokens_low": 16000,
        "text_tokens_expected": 26000,
        "text_tokens_high": 42000,
        "output_tokens_low": 7000,
        "output_tokens_expected": 11500,
        "output_tokens_high": 18500,
        "reasoning_tokens_low": 9000,
        "reasoning_tokens_expected": 24000,
        "reasoning_tokens_high": 56000,
        "image_detail_expected": "high",
        "usage_object": "not exposed by Codex main-agent runtime",
    },
    {
        "call_id": "diego_round1",
        "agent": "Diego",
        "round": "1",
        "purpose": "High-recall visual extraction from raw and derived images",
        "images": [RAW, DETECTED, WIRE_MASK, WIRE_OVERLAY],
        "text_tokens_low": 350,
        "text_tokens_expected": 650,
        "text_tokens_high": 1100,
        "output_tokens_low": 5200,
        "output_tokens_expected": 7600,
        "output_tokens_high": 10500,
        "reasoning_tokens_low": 5000,
        "reasoning_tokens_expected": 13000,
        "reasoning_tokens_high": 32000,
        "image_detail_expected": "original",
        "usage_object": "not exposed by subagent runtime",
    },
    {
        "call_id": "jennifer_round1_aborted_path_retry",
        "agent": "Jennifer",
        "round": "1-aborted",
        "purpose": (
            "Aborted precision-review spawn with incorrect crop path references; "
            "closed before useful extraction output"
        ),
        "images": [RAW, DETECTED, WIRE_OVERLAY],
        "text_tokens_low": 6000,
        "text_tokens_expected": 9500,
        "text_tokens_high": 15000,
        "output_tokens_low": 0,
        "output_tokens_expected": 20,
        "output_tokens_high": 100,
        "reasoning_tokens_low": 500,
        "reasoning_tokens_expected": 1200,
        "reasoning_tokens_high": 4500,
        "image_detail_expected": "high",
        "usage_object": "not exposed; agent was shutdown before final response",
    },
    {
        "call_id": "jennifer_round1",
        "agent": "Jennifer",
        "round": "1",
        "purpose": "Precision review/refinement of Diego round 1 with verified crops",
        "images": [
            RAW,
            DETECTED,
            WIRE_OVERLAY,
            RAW_CROPS / "central_dc_ups.png",
            RAW_CROPS / "bottom_interlocks_a.png",
            RAW_CROPS / "bottom_interlocks_b.png",
            RAW_CROPS / "bus_tie_and_ground.png",
            RAW_CROPS / "mccs_and_feed_buses.png",
            RAW_CROPS / "left_feeders_a1_a2.png",
            RAW_CROPS / "right_feeders_b1_b2.png",
            RAW_CROPS / "top_left_sources_bus_a.png",
            RAW_CROPS / "top_right_sources_bus_b.png",
        ],
        "text_tokens_low": 6500,
        "text_tokens_expected": 9700,
        "text_tokens_high": 14500,
        "output_tokens_low": 3300,
        "output_tokens_expected": 4800,
        "output_tokens_high": 6800,
        "reasoning_tokens_low": 4500,
        "reasoning_tokens_expected": 12000,
        "reasoning_tokens_high": 30000,
        "image_detail_expected": "original",
        "usage_object": "not exposed by subagent runtime",
    },
    {
        "call_id": "diego_round2",
        "agent": "Diego",
        "round": "2",
        "purpose": "Saturation check and acceptance of Jennifer round 1 graph",
        "images": [
            RAW,
            RAW_CROPS / "central_dc_ups.png",
            RAW_CROPS / "bottom_interlocks_a.png",
            RAW_CROPS / "bottom_interlocks_b.png",
            RAW_CROPS / "bus_tie_and_ground.png",
            RAW_CROPS / "mccs_and_feed_buses.png",
        ],
        "text_tokens_low": 5200,
        "text_tokens_expected": 7800,
        "text_tokens_high": 11800,
        "output_tokens_low": 60,
        "output_tokens_expected": 120,
        "output_tokens_high": 250,
        "reasoning_tokens_low": 700,
        "reasoning_tokens_expected": 2300,
        "reasoning_tokens_high": 7000,
        "image_detail_expected": "original",
        "usage_object": "not exposed by subagent runtime",
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
                "document": "3 / Raw + wires + components",
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
                "usage_object": call["usage_object"],
            }
        )

    with (OUT / "model_call_token_estimates.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.DictWriter(fh, fieldnames=call_rows[0].keys())
        writer.writeheader()
        writer.writerows(call_rows)

    summary = {
        "document": "3 / Raw + wires + components",
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
    with (OUT / "iteration_token_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.DictWriter(fh, fieldnames=summary.keys())
        writer.writeheader()
        writer.writerow(summary)

    methodology = f"""# Token Usage Estimate Methodology

The exact OpenAI Responses `usage` objects were not exposed by the Codex
main-agent or subagent tools in this run, so this folder contains estimates.

The official OpenAI input token counting endpoint is `POST /v1/responses/input_tokens`.
It was not called because no API key was available in this environment. If an
API key is added later, the payloads represented by `model_call_token_estimates.csv`
should be sent to that endpoint for exact input counts.

Offline method used here:

- Text input tokens: low/expected/high ranges estimated from visible prompt and
  conversation payload sizes.
- Image/file input tokens: patch-count estimates from the actual local image
  dimensions in `image_token_estimates.csv`.
- Main-agent image views use high-detail estimates.
- Subagent `local_image` detail is not exposed; expected uses original-resolution
  patch estimates for completed visual subagent calls and high-detail estimates
  for the aborted retry.
- Cached input tokens and exact reasoning tokens are not exposed. Cached tokens
  are treated as 0 for totals; reasoning tokens are low/expected/high estimates.
- The aborted Jennifer retry is included because a subagent model call was
  spawned and then shut down before a useful final answer.

Official docs used:

- https://developers.openai.com/api/docs/guides/token-counting
- https://developers.openai.com/api/docs/guides/images-vision
- https://developers.openai.com/api/docs/guides/prompt-caching

Expected total tokens for document 3, iteration 1: {summary['total_tokens_expected']}.
Low/high range: {summary['total_tokens_low']} - {summary['total_tokens_high']}.
"""
    (OUT / "token_usage_methodology.md").write_text(methodology, encoding="utf-8")


if __name__ == "__main__":
    write_reports()
    print(f"Wrote usage estimates to {OUT}")
