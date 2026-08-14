import csv
import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = ROOT / "codes" / "inspection_crops"

FULL_RAW = ROOT / "raw.png"

DIEGO_ROUND_1_IMAGES = [
    FULL_RAW,
    CROPS / "raw_top_left_sources.png",
    CROPS / "raw_upper_left_bus_source_detail.png",
    CROPS / "raw_upper_source_b_detail.png",
    CROPS / "raw_upper_bus_left.png",
    CROPS / "raw_upper_bus_mid.png",
    CROPS / "raw_upper_bus_right.png",
    CROPS / "raw_upper_loads_left.png",
    CROPS / "raw_upper_loads_mid.png",
    CROPS / "raw_upper_loads_right.png",
    CROPS / "raw_upper_right_tie_detail.png",
    CROPS / "raw_dc_ups.png",
    CROPS / "raw_left_utility_feed.png",
    CROPS / "raw_right_utility_feed.png",
    CROPS / "raw_lower_bus_tie.png",
    CROPS / "raw_lower_loads_left.png",
    CROPS / "raw_lower_loads_right.png",
    CROPS / "raw_notes_legend.png",
    CROPS / "wire_nodes_overlay_upper_left_bus_source_detail.png",
    CROPS / "wire_nodes_overlay_upper_bus_mid.png",
    CROPS / "wire_nodes_overlay_upper_bus_right.png",
    CROPS / "wire_nodes_overlay_dc_ups.png",
    CROPS / "wire_nodes_overlay_lower_bus_tie.png",
    CROPS / "wire_nodes_overlay_lower_loads_left.png",
    CROPS / "wire_nodes_overlay_lower_loads_right.png",
]

JENNIFER_ROUND_1_IMAGES = DIEGO_ROUND_1_IMAGES + [
    CROPS / "raw_dc_ups_right_controls.png",
    CROPS / "wire_nodes_overlay_dc_ups_right_controls.png",
]


def text_tokens(chars: int) -> int:
    return math.ceil(chars / 4)


def image_tokens(path: Path) -> int:
    # High-detail vision approximation: 85 base + 170 per 512 tile after
    # constraining max side to 2048 and shortest side to 768 when applicable.
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
    wire_csv_chars = len((ROOT / "wire_nodes.csv").read_text(encoding="utf-8"))
    diego_images = image_token_total(DIEGO_ROUND_1_IMAGES)
    jennifer_images = image_token_total(JENNIFER_ROUND_1_IMAGES)

    rows = [
        {
            "document": "4",
            "iteration": "1",
            "call_id": "main_coordination",
            "agent": "main",
            "round": "setup+orchestration+final",
            "model": "Codex GPT-5",
            "estimated_text_input_tokens": text_tokens(9500),
            "estimated_cached_input_tokens": "",
            "estimated_image_file_tokens": image_token_total([FULL_RAW]),
            "estimated_total_input_tokens": text_tokens(9500) + image_token_total([FULL_RAW]),
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 1100,
            "expected_output_tokens": 1900,
            "high_output_tokens": 3200,
            "low_reasoning_tokens": 1800,
            "expected_reasoning_tokens": 4200,
            "high_reasoning_tokens": 8500,
            "notes": "Main agent inspected files/images, coordinated subagents, wrote scripts, and produced final report.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "diego_round_01",
            "agent": "Diego",
            "round": "1 extractor",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(5200 + wire_csv_chars),
            "estimated_cached_input_tokens": 0,
            "estimated_image_file_tokens": diego_images,
            "estimated_total_input_tokens": text_tokens(5200 + wire_csv_chars) + diego_images,
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 7000,
            "expected_output_tokens": 10000,
            "high_output_tokens": 14000,
            "low_reasoning_tokens": 7000,
            "expected_reasoning_tokens": 16000,
            "high_reasoning_tokens": 32000,
            "notes": "Initial high-recall extraction using full raw image, crops, overlays, and wire_nodes.csv.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "jennifer_round_01",
            "agent": "Jennifer",
            "round": "1 precision review",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(34000),
            "estimated_cached_input_tokens": 0,
            "estimated_image_file_tokens": jennifer_images,
            "estimated_total_input_tokens": text_tokens(34000) + jennifer_images,
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 6500,
            "expected_output_tokens": 9500,
            "high_output_tokens": 13500,
            "low_reasoning_tokens": 7000,
            "expected_reasoning_tokens": 16000,
            "high_reasoning_tokens": 32000,
            "notes": "Reviewed Diego report with image evidence, including extended DC/UPS right-control crop.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "diego_round_02",
            "agent": "Diego",
            "round": "2 extractor convergence",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(20500),
            "estimated_cached_input_tokens": diego_images + text_tokens(5200 + wire_csv_chars),
            "estimated_image_file_tokens": 0,
            "estimated_total_input_tokens": text_tokens(20500),
            "actual_input_tokens": "unavailable",
            "actual_cached_input_tokens": "unavailable",
            "actual_output_tokens": "unavailable",
            "actual_reasoning_tokens": "unavailable",
            "low_output_tokens": 120,
            "expected_output_tokens": 260,
            "high_output_tokens": 600,
            "low_reasoning_tokens": 700,
            "expected_reasoning_tokens": 1800,
            "high_reasoning_tokens": 4500,
            "notes": "Reviewed Jennifer corrections in the same Diego thread; prior context may have been cached by the platform.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "jennifer_round_02",
            "agent": "Jennifer",
            "round": "2 final saturation",
            "model": "gpt-5.5",
            "estimated_text_input_tokens": text_tokens(1800),
            "estimated_cached_input_tokens": jennifer_images + text_tokens(34000),
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
            "notes": "Final agreement check in the same Jennifer thread; prior context may have been cached by the platform.",
        },
    ]

    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    def total(kind):
        return sum(
            row["estimated_total_input_tokens"]
            + row[f"{kind}_output_tokens"]
            + row[f"{kind}_reasoning_tokens"]
            for row in rows
        )

    low_total = total("low")
    expected_total = total("expected")
    high_total = total("high")

    report = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key was available in this environment, so actual usage objects and the Responses input-token counting endpoint could not be used. Estimates use `ceil(chars / 4)` for text and a high-detail image tile approximation for image/file inputs.",
        "",
        f"Diego round 1 image evidence package estimate: {diego_images} image/file input tokens.",
        f"Jennifer round 1 image evidence package estimate: {jennifer_images} image/file input tokens.",
        "",
        "| Document | Iteration | Calls | Low Total | Expected Total | High Total |",
        "|---|---:|---:|---:|---:|---:|",
        f"| 4 | 1 | {len(rows)} | {low_total} | {expected_total} | {high_total} |",
        "",
        "See `token_usage_estimate.csv` for per-call detail, including estimated cached-input fields where previous thread context was likely reusable.",
    ]
    (RESULTS / "token_usage_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
