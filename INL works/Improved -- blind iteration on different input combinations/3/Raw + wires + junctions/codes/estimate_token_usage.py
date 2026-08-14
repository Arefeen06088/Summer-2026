import csv
import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = ROOT / "codes" / "inspection_crops"

FULL_RAW = ROOT / "raw -- synthetic_npp_100_component_electrical_schematic.png"
ROUND_1_IMAGES = [
    FULL_RAW,
    CROPS / "raw_top_left_train_a.png",
    CROPS / "raw_top_center_dc_ups.png",
    CROPS / "raw_top_right_train_b.png",
    CROPS / "raw_mid_mcc_train_a.png",
    CROPS / "raw_mid_mcc_train_b.png",
    CROPS / "raw_feeders_left_train_a.png",
    CROPS / "raw_feeders_right_train_b.png",
    CROPS / "raw_lower_controls.png",
    CROPS / "raw_notes_legend.png",
    CROPS / "wire_nodes_overlay_top_left_train_a.png",
    CROPS / "wire_nodes_overlay_top_center_dc_ups.png",
    CROPS / "wire_nodes_overlay_top_right_train_b.png",
    CROPS / "wire_nodes_overlay_mid_mcc_train_a.png",
    CROPS / "wire_nodes_overlay_mid_mcc_train_b.png",
    CROPS / "wire_nodes_overlay_feeders_left_train_a.png",
    CROPS / "wire_nodes_overlay_feeders_right_train_b.png",
    CROPS / "wire_nodes_overlay_lower_controls.png",
]


def text_tokens(chars: int) -> int:
    return math.ceil(chars / 4)


def image_tokens(path: Path) -> int:
    # OpenAI high-detail vision estimate: 85 base + 170 per 512px tile after
    # downscaling to max 2048px and, if larger, shortest side 768px.
    with Image.open(path) as image:
        width, height = image.size
    scale = min(1.0, 2048 / max(width, height))
    width = int(round(width * scale))
    height = int(round(height * scale))
    if min(width, height) > 768:
        scale = 768 / min(width, height)
        width = int(round(width * scale))
        height = int(round(height * scale))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_token_total(paths):
    return sum(image_tokens(path) for path in paths)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    wire_csv_chars = (ROOT / "wire_nodes.csv").read_text(encoding="utf-8").__len__()
    image_round_1 = image_token_total(ROUND_1_IMAGES)

    # Text estimates use the actual rough size of prompts/reports sent in this
    # workflow: instruction text plus CSV for Diego, Diego's report for Jennifer,
    # Jennifer's accepted report for Diego round 2, and Diego's agreement for
    # Jennifer round 2. Actual usage objects are unavailable in this local Codex
    # session, and the Responses token-count endpoint was not called because no
    # API key is configured.
    rows = [
        {
            "document": "3",
            "iteration": "1",
            "call_id": "main_coordination",
            "agent": "main",
            "round": "setup+orchestration+final",
            "model": "Codex GPT-5",
            "estimated_text_input_tokens": text_tokens(6500),
            "estimated_cached_input_tokens": "",
            "estimated_image_file_tokens": image_token_total([FULL_RAW]),
            "estimated_total_input_tokens": text_tokens(6500) + image_token_total([FULL_RAW]),
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 900,
            "expected_output_tokens": 1600,
            "high_output_tokens": 2600,
            "low_reasoning_tokens": 1500,
            "expected_reasoning_tokens": 3500,
            "high_reasoning_tokens": 7000,
            "notes": "Main agent inspected files/images, coordinated subagents, wrote scripts, and produced final report.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "diego_round_01",
            "agent": "Diego",
            "round": "1 extractor",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(4200 + wire_csv_chars),
            "estimated_cached_input_tokens": 0,
            "estimated_image_file_tokens": image_round_1,
            "estimated_total_input_tokens": text_tokens(4200 + wire_csv_chars) + image_round_1,
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 4500,
            "expected_output_tokens": 6500,
            "high_output_tokens": 9000,
            "low_reasoning_tokens": 5000,
            "expected_reasoning_tokens": 12000,
            "high_reasoning_tokens": 24000,
            "notes": "Initial high-recall extraction using raw image, crops, overlays, and wire_nodes.csv.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "jennifer_round_01",
            "agent": "Jennifer",
            "round": "1 precision review",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(18500),
            "estimated_cached_input_tokens": 0,
            "estimated_image_file_tokens": image_round_1,
            "estimated_total_input_tokens": text_tokens(18500) + image_round_1,
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 4200,
            "expected_output_tokens": 6200,
            "high_output_tokens": 8500,
            "low_reasoning_tokens": 5000,
            "expected_reasoning_tokens": 12000,
            "high_reasoning_tokens": 24000,
            "notes": "Reviewed Diego report with the same image evidence package.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "diego_round_02",
            "agent": "Diego",
            "round": "2 extractor convergence",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(15000),
            "estimated_cached_input_tokens": image_round_1 + text_tokens(4200 + wire_csv_chars),
            "estimated_image_file_tokens": 0,
            "estimated_total_input_tokens": text_tokens(15000),
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 120,
            "expected_output_tokens": 220,
            "high_output_tokens": 500,
            "low_reasoning_tokens": 600,
            "expected_reasoning_tokens": 1500,
            "high_reasoning_tokens": 4000,
            "notes": "Reviewed Jennifer corrections in same agent thread; prior image/context may have been cached by the platform.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "jennifer_round_02",
            "agent": "Jennifer",
            "round": "2 final saturation",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(1800),
            "estimated_cached_input_tokens": image_round_1 + text_tokens(18500),
            "estimated_image_file_tokens": 0,
            "estimated_total_input_tokens": text_tokens(1800),
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 80,
            "expected_output_tokens": 160,
            "high_output_tokens": 350,
            "low_reasoning_tokens": 400,
            "expected_reasoning_tokens": 1200,
            "high_reasoning_tokens": 3000,
            "notes": "Final agreement check in same Jennifer thread; prior image/context may have been cached by the platform.",
        },
    ]

    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    expected_total = sum(
        row["estimated_total_input_tokens"]
        + row["expected_output_tokens"]
        + row["expected_reasoning_tokens"]
        for row in rows
    )
    low_total = sum(
        row["estimated_total_input_tokens"] + row["low_output_tokens"] + row["low_reasoning_tokens"]
        for row in rows
    )
    high_total = sum(
        row["estimated_total_input_tokens"] + row["high_output_tokens"] + row["high_reasoning_tokens"]
        for row in rows
    )

    report = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key was available in this environment, so actual usage objects and the Responses input-token counting endpoint could not be used. Estimates use `ceil(chars / 4)` for text and a high-detail image tile approximation for image/file inputs.",
        "",
        f"Round 1 image evidence package estimate: {image_round_1} image/file input tokens.",
        "",
        "| Document | Iteration | Calls | Low Total | Expected Total | High Total |",
        "|---|---:|---:|---:|---:|---:|",
        f"| 3 | 1 | {len(rows)} | {low_total} | {expected_total} | {high_total} |",
        "",
        "See `token_usage_estimate.csv` for per-call detail, including estimated cached-input fields where previous thread context was likely reusable.",
    ]
    (RESULTS / "token_usage_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
