from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires"
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


COMMON_TASK = """Extract the connectivity matrix from document 27 using only Raw + wires resources.
No GT or GT-derived feedback. No off-the-shelf OCR. Rows/columns are the same component/node names,
1 means connected, symmetric, diagonal 0 unless justified. Diego is the high-recall extractor.
Jennifer is the precision reviewer/refiner. Store matrices for every round."""


def image(path: str) -> str:
    return path


CALLS = [
    {
        "document": 27,
        "iteration": 1,
        "call_id": "main_orchestration",
        "agent": "main",
        "round": "setup, local visual inspection, integration, artifact writing",
        "model": "Codex/GPT-5 family session model",
        "text": COMMON_TASK
        + "\nMain agent inspected folders and images, created crops, coordinated Diego/Jennifer rounds, wrote matrices, and estimated usage.",
        "images": [],
        "cached_input_tokens": None,
        "output_tokens_low": 1000,
        "output_tokens_expected": 2500,
        "output_tokens_high": 5000,
        "reasoning_tokens_low": 2000,
        "reasoning_tokens_expected": 8000,
        "reasoning_tokens_high": 18000,
        "status": "estimated; platform usage object not exposed to local script",
    },
    {
        "document": 27,
        "iteration": 1,
        "call_id": "diego_round_1",
        "agent": "Diego",
        "round": "R1 high-recall extraction",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nHigh-recall pass over full raw, overlay, overview, top/source, train, load, bottom-control, title/notes crops. Return all visually plausible nodes and edges with evidence.",
        "images": [
            image("raw -- synthetic_npp_electrical_schematic_readable.png"),
            image("wires_mask_overlay.png"),
            image("codes/crops/raw__overview_large.png"),
            image("codes/crops/raw__top_band.png"),
            image("codes/crops/raw__top_source_bus.png"),
            image("codes/crops/raw__upper_left_trains.png"),
            image("codes/crops/raw__upper_right_trains.png"),
            image("codes/crops/raw__mid_left_loads.png"),
            image("codes/crops/raw__mid_right_loads.png"),
            image("codes/crops/raw__bottom_left_controls.png"),
            image("codes/crops/raw__bottom_right_controls.png"),
            image("codes/crops/raw__bottom_controls_wide.png"),
            image("codes/crops/wires_overlay__bottom_controls_wide.png"),
            image("codes/crops/raw__title_notes.png"),
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 2500,
        "output_tokens_expected": 4800,
        "output_tokens_high": 8500,
        "reasoning_tokens_low": 7000,
        "reasoning_tokens_expected": 16000,
        "reasoning_tokens_high": 34000,
        "status": "completed; subagent usage object not exposed by multi-agent tool",
    },
    {
        "document": 27,
        "iteration": 1,
        "call_id": "jennifer_round_1",
        "agent": "Jennifer",
        "round": "R1 precision review",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nPrecision-review Diego R1. Remove unsupported edges, fix labels, and focus on CHGR/BAT/JB/DC/PANEL/ground regions.",
        "images": [
            image("raw -- synthetic_npp_electrical_schematic_readable.png"),
            image("wires_mask_overlay.png"),
            image("codes/crops/raw__top_source_bus.png"),
            image("codes/crops/raw__focus_a_dc_ups_controls.png"),
            image("codes/crops/raw__focus_b_dc_ups_controls.png"),
            image("codes/crops/raw__zoom_a10_b01_dc.png"),
            image("codes/crops/wires_overlay__zoom_a10_b01_dc.png"),
            image("codes/crops/raw__zoom_c_ground.png"),
            image("codes/crops/raw__zoom_d_ground.png"),
            image("codes/crops/raw__title_notes.png"),
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 1800,
        "output_tokens_expected": 3600,
        "output_tokens_high": 6500,
        "reasoning_tokens_low": 5000,
        "reasoning_tokens_expected": 12000,
        "reasoning_tokens_high": 26000,
        "status": "completed; subagent usage object not exposed by multi-agent tool",
    },
    {
        "document": 27,
        "iteration": 1,
        "call_id": "diego_round_2",
        "agent": "Diego",
        "round": "R2 saturation check",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nRe-check Jennifer R1 corrected matrix against focused charger/battery/DC/panel/ground crops. List only exact supported changes or agree saturated.",
        "images": [
            image("codes/crops/raw__zoom_a10_b01_dc.png"),
            image("codes/crops/wires_overlay__zoom_a10_b01_dc.png"),
            image("codes/crops/raw__zoom_a10_dc.png"),
            image("codes/crops/raw__zoom_b01_dc.png"),
            image("codes/crops/raw__focus_a_dc_ups_controls.png"),
            image("codes/crops/raw__focus_b_dc_ups_controls.png"),
            image("codes/crops/raw__overview_large.png"),
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 350,
        "output_tokens_expected": 800,
        "output_tokens_high": 1600,
        "reasoning_tokens_low": 2000,
        "reasoning_tokens_expected": 7000,
        "reasoning_tokens_high": 18000,
        "status": "completed; subagent usage object not exposed by multi-agent tool",
    },
    {
        "document": 27,
        "iteration": 1,
        "call_id": "jennifer_round_2_final",
        "agent": "Jennifer",
        "round": "R2 final closure",
        "model": "gpt-5.5 xhigh",
        "text": COMMON_TASK
        + "\nFinal precision closure after Diego R2 agreement. Confirm saturated final matrix and high-risk exclusions.",
        "images": [
            image("codes/crops/raw__zoom_a10_b01_dc.png"),
            image("codes/crops/wires_overlay__zoom_a10_b01_dc.png"),
            image("codes/crops/raw__focus_a_dc_ups_controls.png"),
            image("codes/crops/raw__focus_b_dc_ups_controls.png"),
            image("codes/crops/raw__overview_large.png"),
        ],
        "cached_input_tokens": None,
        "output_tokens_low": 250,
        "output_tokens_expected": 600,
        "output_tokens_high": 1200,
        "reasoning_tokens_low": 1500,
        "reasoning_tokens_expected": 5500,
        "reasoning_tokens_high": 14000,
        "status": "submitted/completed depending on final run; usage object not exposed by multi-agent tool",
    },
]


def estimate_text_tokens(text: str) -> int:
    if ENCODING is not None:
        return len(ENCODING.encode(text))
    return math.ceil(len(text) / 4)


def image_token_estimate(path: Path) -> dict[str, int]:
    with Image.open(path) as img:
        width, height = img.size
    # Offline proxy for high-detail vision inputs: charge one 512px tile at 170 tokens plus 85 base tokens.
    # The official endpoint should replace this whenever OPENAI_API_KEY is available.
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    expected = 85 + 170 * tiles
    return {
        "width": width,
        "height": height,
        "tiles_512": tiles,
        "low": max(85, round(expected * 0.75)),
        "expected": expected,
        "high": round(expected * 1.35),
    }


def resolve_image(name: str) -> Path:
    return BASE / name


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for call in CALLS:
        text_tokens = estimate_text_tokens(call["text"])
        image_details = []
        image_low = image_expected = image_high = 0
        for img_name in call["images"]:
            stats = image_token_estimate(resolve_image(img_name))
            image_details.append({"path": img_name, **stats})
            image_low += stats["low"]
            image_expected += stats["expected"]
            image_high += stats["high"]

        input_low = text_tokens + image_low
        input_expected = text_tokens + image_expected
        input_high = text_tokens + image_high
        output_low = call["output_tokens_low"]
        output_expected = call["output_tokens_expected"]
        output_high = call["output_tokens_high"]
        reasoning_low = call["reasoning_tokens_low"]
        reasoning_expected = call["reasoning_tokens_expected"]
        reasoning_high = call["reasoning_tokens_high"]
        rows.append(
            {
                "document": call["document"],
                "iteration": call["iteration"],
                "call_id": call["call_id"],
                "agent": call["agent"],
                "round": call["round"],
                "model": call["model"],
                "text_input_tokens_est": text_tokens,
                "image_input_tokens_low_est": image_low,
                "image_input_tokens_expected_est": image_expected,
                "image_input_tokens_high_est": image_high,
                "input_tokens_low_est": input_low,
                "input_tokens_expected_est": input_expected,
                "input_tokens_high_est": input_high,
                "cached_input_tokens": call["cached_input_tokens"],
                "output_tokens_low_est": output_low,
                "output_tokens_expected_est": output_expected,
                "output_tokens_high_est": output_high,
                "reasoning_tokens_low_est": reasoning_low,
                "reasoning_tokens_expected_est": reasoning_expected,
                "reasoning_tokens_high_est": reasoning_high,
                "total_tokens_low_est": input_low + output_low + reasoning_low,
                "total_tokens_expected_est": input_expected + output_expected + reasoning_expected,
                "total_tokens_high_est": input_high + output_high + reasoning_high,
                "status": call["status"],
                "image_details": image_details,
            }
        )

    totals = {
        "document": 27,
        "iteration": 1,
        "calls": len(rows),
        "input_tokens_low_est": sum(row["input_tokens_low_est"] for row in rows),
        "input_tokens_expected_est": sum(row["input_tokens_expected_est"] for row in rows),
        "input_tokens_high_est": sum(row["input_tokens_high_est"] for row in rows),
        "output_tokens_low_est": sum(row["output_tokens_low_est"] for row in rows),
        "output_tokens_expected_est": sum(row["output_tokens_expected_est"] for row in rows),
        "output_tokens_high_est": sum(row["output_tokens_high_est"] for row in rows),
        "reasoning_tokens_low_est": sum(row["reasoning_tokens_low_est"] for row in rows),
        "reasoning_tokens_expected_est": sum(row["reasoning_tokens_expected_est"] for row in rows),
        "reasoning_tokens_high_est": sum(row["reasoning_tokens_high_est"] for row in rows),
        "total_tokens_low_est": sum(row["total_tokens_low_est"] for row in rows),
        "total_tokens_expected_est": sum(row["total_tokens_expected_est"] for row in rows),
        "total_tokens_high_est": sum(row["total_tokens_high_est"] for row in rows),
        "official_method": {
            "endpoint": "POST /v1/responses/input_tokens",
            "docs": "https://developers.openai.com/api/docs/guides/token-counting",
            "note": "Use the same Responses payload, including input_image items, to get exact input_tokens. This environment has no API key, so local text tokenization plus image tile proxy was used.",
        },
    }

    csv_path = RESULTS / "doc27_token_usage_estimate.csv"
    fieldnames = [
        "document",
        "iteration",
        "call_id",
        "agent",
        "round",
        "model",
        "text_input_tokens_est",
        "image_input_tokens_low_est",
        "image_input_tokens_expected_est",
        "image_input_tokens_high_est",
        "input_tokens_low_est",
        "input_tokens_expected_est",
        "input_tokens_high_est",
        "cached_input_tokens",
        "output_tokens_low_est",
        "output_tokens_expected_est",
        "output_tokens_high_est",
        "reasoning_tokens_low_est",
        "reasoning_tokens_expected_est",
        "reasoning_tokens_high_est",
        "total_tokens_low_est",
        "total_tokens_expected_est",
        "total_tokens_high_est",
        "status",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})
        writer.writerow(
            {
                "document": totals["document"],
                "iteration": totals["iteration"],
                "call_id": "TOTAL",
                "agent": "all",
                "round": "iteration total",
                "model": "mixed",
                "text_input_tokens_est": "",
                "image_input_tokens_low_est": "",
                "image_input_tokens_expected_est": "",
                "image_input_tokens_high_est": "",
                "input_tokens_low_est": totals["input_tokens_low_est"],
                "input_tokens_expected_est": totals["input_tokens_expected_est"],
                "input_tokens_high_est": totals["input_tokens_high_est"],
                "cached_input_tokens": "",
                "output_tokens_low_est": totals["output_tokens_low_est"],
                "output_tokens_expected_est": totals["output_tokens_expected_est"],
                "output_tokens_high_est": totals["output_tokens_high_est"],
                "reasoning_tokens_low_est": totals["reasoning_tokens_low_est"],
                "reasoning_tokens_expected_est": totals["reasoning_tokens_expected_est"],
                "reasoning_tokens_high_est": totals["reasoning_tokens_high_est"],
                "total_tokens_low_est": totals["total_tokens_low_est"],
                "total_tokens_expected_est": totals["total_tokens_expected_est"],
                "total_tokens_high_est": totals["total_tokens_high_est"],
                "status": "summed estimate",
            }
        )

    (RESULTS / "doc27_token_usage_estimate.json").write_text(
        json.dumps({"calls": rows, "totals": totals}, indent=2), encoding="utf-8"
    )
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
