from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires"
)
CROPS = BASE / "codes" / "crops"
RESULTS = BASE / "results"


try:
    import tiktoken

    try:
        ENCODING = tiktoken.encoding_for_model("gpt-5.5")
    except Exception:
        ENCODING = tiktoken.get_encoding("o200k_base")
except Exception:
    ENCODING = None


COMMON_TASK = """Extract the connectivity matrix from document 26 using only Raw + wires resources.
No GT or GT-derived feedback. No off-the-shelf OCR. Rows/columns are the same component/node names,
1 means connected, symmetric, diagonal 0 unless justified. Diego is the high-recall extractor.
Jennifer is the precision reviewer/refiner. Store matrices for every round."""


CALLS = [
    {
        "document": 26,
        "iteration": 1,
        "call_id": "main_orchestration",
        "agent": "main",
        "round": "setup_and_integration",
        "model": "Codex/GPT-5 family session model",
        "text": COMMON_TASK
        + "\nMain agent inspects folders, creates crops, writes matrices, coordinates Diego/Jennifer, and estimates usage.",
        "images": [],
        "cached_input_tokens": None,
        "output_tokens_low": 1000,
        "output_tokens_expected": 2500,
        "output_tokens_high": 5000,
        "reasoning_tokens_low": 2000,
        "reasoning_tokens_expected": 8000,
        "reasoning_tokens_high": 18000,
        "status": "estimated; platform usage object not exposed",
    },
    {
        "document": 26,
        "iteration": 1,
        "call_id": "diego_round_1",
        "agent": "Diego",
        "round": "R1 extraction",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nHigh-recall pass over raw, wire mask, overlay, overview, top/mid/bottom crops. Return all plausible nodes and edges with evidence.",
        "images": [
            "raw -- synthetic_npp_electrical_schematic_v3(1).png",
            "wires_mask.png",
            "wires_mask_overlay.png",
            "raw__overview_large.png",
            "wires_overlay__overview_large.png",
            "raw__upper_left_trains.png",
            "raw__upper_right_trains.png",
            "raw__mid_left_loads.png",
            "raw__mid_right_loads.png",
            "raw__bottom_controls_wide.png",
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 2200,
        "output_tokens_expected": 4500,
        "output_tokens_high": 8000,
        "reasoning_tokens_low": 6000,
        "reasoning_tokens_expected": 14000,
        "reasoning_tokens_high": 30000,
        "status": "estimated; completed subagent usage object not exposed",
    },
    {
        "document": 26,
        "iteration": 1,
        "call_id": "jennifer_round_1",
        "agent": "Jennifer",
        "round": "R1 precision review",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nPrecision-review Diego R1, remove unsupported edges, fix labels, mark ambiguous dashed endpoints uncertain.",
        "images": [
            "raw -- synthetic_npp_electrical_schematic_v3(1).png",
            "wires_mask_overlay.png",
            "raw__upper_left_trains.png",
            "raw__upper_right_trains.png",
            "raw__mid_left_loads.png",
            "raw__mid_right_loads.png",
            "raw__bottom_controls_wide.png",
            "raw__focus_a_dc_ups_controls.png",
            "raw__focus_b_dc_ups_controls.png",
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 1800,
        "output_tokens_expected": 3500,
        "output_tokens_high": 6500,
        "reasoning_tokens_low": 5000,
        "reasoning_tokens_expected": 12000,
        "reasoning_tokens_high": 26000,
        "status": "estimated; completed subagent usage object not exposed",
    },
    {
        "document": 26,
        "iteration": 1,
        "call_id": "diego_round_2_initial",
        "agent": "Diego",
        "round": "R2 dashed-control revisit",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nJennifer accepted the main graph. Revisit only dashed RCP/MOV/control candidates from focused crops and return exact additions/removals.",
        "images": [
            "raw__focus_a_rcp_interlock.png",
            "wires_overlay__focus_a_rcp_interlock.png",
            "raw__focus_b_rcp_interlock.png",
            "wires_overlay__focus_b_rcp_interlock.png",
            "raw__focus_a_mov_controls.png",
            "wires_overlay__focus_a_mov_controls.png",
            "raw__focus_b_mov_controls.png",
            "wires_overlay__focus_b_mov_controls.png",
            "raw__focus_a_dc_ups_controls.png",
            "wires_overlay__focus_a_dc_ups_controls.png",
            "raw__focus_b_dc_ups_controls.png",
            "wires_overlay__focus_b_dc_ups_controls.png",
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 900,
        "output_tokens_expected": 1800,
        "output_tokens_high": 3500,
        "reasoning_tokens_low": 0,
        "reasoning_tokens_expected": 5000,
        "reasoning_tokens_high": 15000,
        "status": "submitted then interrupted by RCP zoom addendum; no final usage object exposed",
    },
    {
        "document": 26,
        "iteration": 1,
        "call_id": "diego_round_2_addendum",
        "agent": "Diego",
        "round": "R2 RCP zoom decision",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nAddendum: use tighter RCP zooms and decide whether the lower endpoint is labeled/supported.",
        "images": [
            "raw__zoom_rcp_a.png",
            "wires_overlay__zoom_rcp_a.png",
            "raw__zoom_rcp_b.png",
            "wires_overlay__zoom_rcp_b.png",
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 180,
        "output_tokens_expected": 300,
        "output_tokens_high": 500,
        "reasoning_tokens_low": 1000,
        "reasoning_tokens_expected": 4500,
        "reasoning_tokens_high": 12000,
        "status": "completed; usage object not exposed",
    },
    {
        "document": 26,
        "iteration": 1,
        "call_id": "diego_round_2_mov_followup",
        "agent": "Diego",
        "round": "R2 MOV/SI candidate restatement",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nRestate exact MOV/SI dashed additions from R2 after the RCP addendum; keep RCP unresolved.",
        "images": [
            "raw__focus_a_mov_controls.png",
            "wires_overlay__focus_a_mov_controls.png",
            "raw__focus_b_mov_controls.png",
            "wires_overlay__focus_b_mov_controls.png",
            "raw__focus_a_dc_ups_controls.png",
            "wires_overlay__focus_a_dc_ups_controls.png",
            "raw__focus_b_dc_ups_controls.png",
            "wires_overlay__focus_b_dc_ups_controls.png",
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 120,
        "output_tokens_expected": 200,
        "output_tokens_high": 350,
        "reasoning_tokens_low": 1500,
        "reasoning_tokens_expected": 5000,
        "reasoning_tokens_high": 12000,
        "status": "completed; usage object not exposed",
    },
    {
        "document": 26,
        "iteration": 1,
        "call_id": "jennifer_round_2",
        "agent": "Jennifer",
        "round": "R2 final precision review",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nReview Diego R2 dashed-control decisions against focused and zoom crops, then produce final accepted matrix or unresolved uncertainties.",
        "images": [
            "raw__focus_a_mov_controls.png",
            "wires_overlay__focus_a_mov_controls.png",
            "raw__focus_b_mov_controls.png",
            "wires_overlay__focus_b_mov_controls.png",
            "raw__focus_a_dc_ups_controls.png",
            "wires_overlay__focus_a_dc_ups_controls.png",
            "raw__focus_b_dc_ups_controls.png",
            "wires_overlay__focus_b_dc_ups_controls.png",
            "raw__zoom_rcp_a.png",
            "wires_overlay__zoom_rcp_a.png",
            "raw__zoom_rcp_b.png",
            "wires_overlay__zoom_rcp_b.png",
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 280,
        "output_tokens_expected": 450,
        "output_tokens_high": 700,
        "reasoning_tokens_low": 2500,
        "reasoning_tokens_expected": 8000,
        "reasoning_tokens_high": 18000,
        "status": "completed; usage object not exposed",
    },
]


def text_tokens(text: str) -> int:
    if ENCODING is not None:
        return len(ENCODING.encode(text))
    return max(1, math.ceil(len(text) / 4))


def resolve_image(name: str) -> Path:
    path = BASE / name
    if path.exists():
        return path
    path = CROPS / name
    if path.exists():
        return path
    raise FileNotFoundError(name)


def high_detail_expected_tiles(width: int, height: int) -> int:
    scale = min(1.0, 2048 / max(width, height))
    width2 = width * scale
    height2 = height * scale
    if min(width2, height2) > 768:
        scale2 = 768 / min(width2, height2)
        width2 *= scale2
        height2 *= scale2
    return math.ceil(width2 / 512) * math.ceil(height2 / 512)


def image_tokens_for(path: Path) -> dict[str, int]:
    with Image.open(path) as img:
        width, height = img.size
    low = 85
    expected = 85 + 170 * high_detail_expected_tiles(width, height)
    high = 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)
    return {
        "width": width,
        "height": height,
        "image_tokens_low": low,
        "image_tokens_expected": expected,
        "image_tokens_high": high,
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    image_cache: dict[str, dict[str, int]] = {}
    rows = []

    for call in CALLS:
        image_low = image_expected = image_high = 0
        image_details = []
        for image_name in call["images"]:
            path = resolve_image(image_name)
            stats = image_cache.setdefault(image_name, image_tokens_for(path))
            image_low += stats["image_tokens_low"]
            image_expected += stats["image_tokens_expected"]
            image_high += stats["image_tokens_high"]
            image_details.append({"name": image_name, **stats})

        text_input = text_tokens(call["text"])
        input_expected = text_input + image_expected
        row = {
            "document": call["document"],
            "iteration": call["iteration"],
            "call_id": call["call_id"],
            "agent": call["agent"],
            "round": call["round"],
            "model": call["model"],
            "text_input_tokens_est": text_input,
            "cached_input_tokens": call["cached_input_tokens"],
            "image_file_count": len(call["images"]),
            "image_input_tokens_low": image_low,
            "image_input_tokens_expected": image_expected,
            "image_input_tokens_high": image_high,
            "input_tokens_low": text_input + image_low,
            "input_tokens_expected": input_expected,
            "input_tokens_high": text_input + image_high,
            "output_tokens_low": call["output_tokens_low"],
            "output_tokens_expected": call["output_tokens_expected"],
            "output_tokens_high": call["output_tokens_high"],
            "reasoning_tokens_low": call["reasoning_tokens_low"],
            "reasoning_tokens_expected": call["reasoning_tokens_expected"],
            "reasoning_tokens_high": call["reasoning_tokens_high"],
            "total_tokens_low": text_input
            + image_low
            + call["output_tokens_low"]
            + call["reasoning_tokens_low"],
            "total_tokens_expected": input_expected
            + call["output_tokens_expected"]
            + call["reasoning_tokens_expected"],
            "total_tokens_high": text_input
            + image_high
            + call["output_tokens_high"]
            + call["reasoning_tokens_high"],
            "status": call["status"],
        }
        rows.append(row)

    fieldnames = list(rows[0].keys())
    with (RESULTS / "doc26_token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "document": 26,
        "iteration": 1,
        "method": {
            "official_endpoint": "client.responses.input_tokens.count / POST /v1/responses/input_tokens",
            "official_endpoint_used": False,
            "reason_official_not_used": "No OPENAI_API_KEY/API usage object is available in this execution environment.",
            "text_estimator": "tiktoken gpt-5.5 if available, else o200k_base, else characters/4",
            "image_estimator": "local low/expected/high proxy from image dimensions; exact image/file/tool tokens require the API endpoint",
        },
        "totals": {
            "input_tokens_low": sum(r["input_tokens_low"] for r in rows),
            "input_tokens_expected": sum(r["input_tokens_expected"] for r in rows),
            "input_tokens_high": sum(r["input_tokens_high"] for r in rows),
            "output_tokens_low": sum(r["output_tokens_low"] for r in rows),
            "output_tokens_expected": sum(r["output_tokens_expected"] for r in rows),
            "output_tokens_high": sum(r["output_tokens_high"] for r in rows),
            "reasoning_tokens_low": sum(r["reasoning_tokens_low"] for r in rows),
            "reasoning_tokens_expected": sum(r["reasoning_tokens_expected"] for r in rows),
            "reasoning_tokens_high": sum(r["reasoning_tokens_high"] for r in rows),
            "total_tokens_low": sum(r["total_tokens_low"] for r in rows),
            "total_tokens_expected": sum(r["total_tokens_expected"] for r in rows),
            "total_tokens_high": sum(r["total_tokens_high"] for r in rows),
        },
        "calls": rows,
    }
    with (RESULTS / "doc26_token_usage_estimate.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary["totals"], indent=2))


if __name__ == "__main__":
    main()
