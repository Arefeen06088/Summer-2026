from __future__ import annotations

import csv
import math
import os
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # noqa: BLE001
    tiktoken = None


DOCUMENT = "23"
ITERATION = "1"
MODEL = "gpt-5.5"


def encoding_token_count(text: str) -> int:
    if not text:
        return 0
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:  # noqa: BLE001
            pass
    return math.ceil(len(text) / 4)


def high_detail_image_tokens(width: int, height: int) -> int:
    # Fallback estimate based on the public high-detail image tiling method:
    # fit within 2048x2048, then scale so the shortest side is 768, count
    # 512px tiles, and charge 85 base + 170 per tile.
    scale = min(2048 / width, 2048 / height, 1.0)
    width2 = width * scale
    height2 = height * scale
    short = min(width2, height2)
    if short > 768:
        scale2 = 768 / short
        width2 *= scale2
        height2 *= scale2
    tiles = math.ceil(width2 / 512) * math.ceil(height2 / 512)
    return 85 + 170 * tiles


def image_tokens(path: Path) -> int:
    with Image.open(path) as image:
        return high_detail_image_tokens(*image.size)


def sum_image_tokens(paths: list[Path]) -> int:
    total = 0
    for path in paths:
        if path.exists():
            total += image_tokens(path)
    return total


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def file_text_tokens(paths: list[Path]) -> int:
    total = 0
    for path in paths:
        total += encoding_token_count(read_text_if_exists(path))
    return total


def main() -> int:
    base_dir = Path(__file__).resolve().parents[1]
    results_dir = base_dir / "results"
    crops_dir = base_dir / "precision_review_crops"
    raw = base_dir / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png"
    labels = base_dir / "component_labels_banners_overlay.png"
    wires = base_dir / "wires_mask_overlay.png"
    nodes_overlay = base_dir / "wire_nodes_overlay.png"

    all_crop_images = sorted(crops_dir.glob("*.png"))
    key_crop_names = [
        "raw__top_band.png",
        "raw__middle_band.png",
        "raw__bottom_band.png",
        "labels__top_band.png",
        "labels__middle_band.png",
        "labels__bottom_band.png",
        "nodes__top_band.png",
        "nodes__middle_band.png",
        "nodes__bottom_band.png",
        "wires__top_band.png",
        "wires__middle_band.png",
        "wires__bottom_band.png",
        "labels__row1_col1.png",
        "labels__row1_col2.png",
        "labels__row1_col3.png",
        "labels__row2_col1.png",
        "labels__row2_col2.png",
        "labels__row2_col3.png",
        "labels__row3_col1.png",
        "labels__row3_col2.png",
        "labels__row3_col3.png",
    ]
    key_crops = [crops_dir / name for name in key_crop_names if (crops_dir / name).exists()]
    full_images = [raw, labels, wires, nodes_overlay]
    low_images = [raw, labels, nodes_overlay]
    expected_images = full_images + key_crops
    high_images = full_images + all_crop_images

    task_brief = """
Extract document 23 connectivity matrix from raw schematic and allowed visual aids.
Use Diego as high-recall extractor and Jennifer as precision reviewer. Do not use
Ground Truth or off-the-shelf OCR. Store every round matrix and token accounting.
"""
    diego_instruction = """
High-recall visual extraction prompt: inspect raw schematic, overlays, crops,
component CSV, and wire node aids. Propose all visually/geometrically plausible
components, logical buses, and undirected edges with evidence. Write round files.
"""
    jennifer_instruction = """
Precision review prompt: inspect the raw image and aids, compare Diego proposal,
remove unsupported or overconnected edges, fix visually supported labels, and
write refined round files with notes and validation.
"""
    saturation_instruction = """
Saturation prompt: compare prior Diego/Jennifer outputs, inspect changed or
ambiguous areas visually, converge only when the connectivity matrix is stable.
"""

    diego_round1_files = [
        results_dir / "document23_round01_diego_edges.csv",
        results_dir / "document23_round01_diego_nodes.csv",
        results_dir / "document23_round01_diego_notes.md",
    ]
    jennifer_round2_files = [
        results_dir / "document23_round02_jennifer_edges.csv",
        results_dir / "document23_round02_jennifer_nodes.csv",
        results_dir / "document23_round02_jennifer_notes.md",
    ]
    diego_round3_files = [
        results_dir / "document23_round03_diego_edges.csv",
        results_dir / "document23_round03_diego_nodes.csv",
        results_dir / "document23_round03_diego_notes.md",
    ]

    image_low = sum_image_tokens(low_images)
    image_expected = sum_image_tokens(expected_images)
    image_high = sum_image_tokens(high_images)

    rows = [
        {
            "call_id": "main-01",
            "agent": "main",
            "round": "setup",
            "role": "orchestrator",
            "prompt_text": task_brief,
            "file_text_tokens_expected": 0,
            "image_low": 0,
            "image_expected": 0,
            "image_high": 0,
            "output_low": 250,
            "output_expected": 600,
            "output_high": 1200,
        },
        {
            "call_id": "diego-01",
            "agent": "Diego",
            "round": "01",
            "role": "high-recall extractor",
            "prompt_text": task_brief + diego_instruction,
            "file_text_tokens_expected": file_text_tokens([base_dir / "component_visual_ocr_labels.csv", base_dir / "wire_nodes.csv"]),
            "image_low": image_low,
            "image_expected": image_expected,
            "image_high": image_high,
            "output_low": 7000,
            "output_expected": 12000,
            "output_high": 20000,
        },
        {
            "call_id": "jennifer-01",
            "agent": "Jennifer",
            "round": "02",
            "role": "precision reviewer",
            "prompt_text": task_brief + jennifer_instruction,
            "file_text_tokens_expected": file_text_tokens(
                [base_dir / "component_visual_ocr_labels.csv", base_dir / "wire_nodes.csv", *diego_round1_files]
            ),
            "image_low": image_low,
            "image_expected": image_expected,
            "image_high": image_high,
            "output_low": 6000,
            "output_expected": 10000,
            "output_high": 18000,
        },
        {
            "call_id": "diego-02",
            "agent": "Diego",
            "round": "03",
            "role": "saturation extractor",
            "prompt_text": task_brief + saturation_instruction,
            "file_text_tokens_expected": file_text_tokens(
                [base_dir / "component_visual_ocr_labels.csv", base_dir / "wire_nodes.csv", *diego_round1_files, *jennifer_round2_files]
            ),
            "image_low": image_low,
            "image_expected": image_expected,
            "image_high": image_high,
            "output_low": 4000,
            "output_expected": 8000,
            "output_high": 15000,
        },
        {
            "call_id": "jennifer-02",
            "agent": "Jennifer",
            "round": "04",
            "role": "final precision signoff",
            "prompt_text": task_brief + jennifer_instruction + saturation_instruction,
            "file_text_tokens_expected": file_text_tokens(
                [
                    base_dir / "component_visual_ocr_labels.csv",
                    base_dir / "wire_nodes.csv",
                    *diego_round1_files,
                    *jennifer_round2_files,
                    *diego_round3_files,
                ]
            ),
            "image_low": image_low,
            "image_expected": image_expected,
            "image_high": image_high,
            "output_low": 3500,
            "output_expected": 6500,
            "output_high": 12000,
        },
        {
            "call_id": "main-02",
            "agent": "main",
            "round": "finalize",
            "role": "orchestrator",
            "prompt_text": "Validate final graph, write aliases, compare rounds, summarize token estimates.",
            "file_text_tokens_expected": file_text_tokens(
                [
                    results_dir / "document23_round01_diego_notes.md",
                    results_dir / "document23_round02_jennifer_notes.md",
                    results_dir / "document23_round03_diego_notes.md",
                    results_dir / "document23_round04_jennifer_notes.md",
                ]
            ),
            "image_low": 0,
            "image_expected": 0,
            "image_high": 0,
            "output_low": 700,
            "output_expected": 1200,
            "output_high": 2200,
        },
    ]

    detail_rows = []
    for row in rows:
        prompt_tokens = encoding_token_count(row["prompt_text"])
        text_expected = prompt_tokens + row["file_text_tokens_expected"]
        text_low = math.ceil(text_expected * 0.75)
        text_high = math.ceil(text_expected * 1.25)
        total_low = text_low + row["image_low"] + row["output_low"]
        total_expected = text_expected + row["image_expected"] + row["output_expected"]
        total_high = text_high + row["image_high"] + row["output_high"]
        detail_rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "call_id": row["call_id"],
                "agent": row["agent"],
                "round": row["round"],
                "role": row["role"],
                "model": MODEL,
                "input_text_tokens_low": text_low,
                "input_text_tokens_expected": text_expected,
                "input_text_tokens_high": text_high,
                "cached_input_tokens": "unknown",
                "image_file_input_tokens_low": row["image_low"],
                "image_file_input_tokens_expected": row["image_expected"],
                "image_file_input_tokens_high": row["image_high"],
                "output_tokens_low": row["output_low"],
                "output_tokens_expected": row["output_expected"],
                "output_tokens_high": row["output_high"],
                "reasoning_tokens": "unavailable",
                "total_tokens_low": total_low,
                "total_tokens_expected": total_expected,
                "total_tokens_high": total_high,
                "usage_object_available": "no",
                "counting_method": "tiktoken o200k_base for text if available; public high-detail image tiling estimate; output ranges estimated",
            }
        )

    detail_path = results_dir / "document23_token_usage_estimates.csv"
    fieldnames = list(detail_rows[0].keys())
    with detail_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(detail_rows)

    totals = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "calls": len(detail_rows),
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in detail_rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in detail_rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in detail_rows),
        "input_text_tokens_expected": sum(int(row["input_text_tokens_expected"]) for row in detail_rows),
        "image_file_input_tokens_expected": sum(int(row["image_file_input_tokens_expected"]) for row in detail_rows),
        "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in detail_rows),
        "openai_api_key_present": "yes" if os.environ.get("OPENAI_API_KEY") else "no",
    }
    totals_path = results_dir / "document23_token_usage_totals.csv"
    with totals_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(totals.keys()))
        writer.writeheader()
        writer.writerow(totals)

    notes_path = results_dir / "document23_token_usage_notes.md"
    notes_path.write_text(
        "\n".join(
            [
                "# Document 23 Token Usage Notes",
                "",
                "- Actual model usage objects were not available to this local script.",
                "- `OPENAI_API_KEY` was not present, so the OpenAI Responses input-token counting endpoint could not be called.",
                "- Text estimates use `tiktoken` `o200k_base` when available, otherwise character/4.",
                "- Image estimates use the public high-detail tiling approximation: 85 base tokens plus 170 per 512px tile after scaling.",
                "- Low/expected/high ranges vary the amount of visual context and unknown output length.",
                f"- Detail CSV: `{detail_path}`",
                f"- Totals CSV: `{totals_path}`",
            ]
        ),
        encoding="utf-8",
    )

    print(f"wrote {detail_path}")
    print(f"wrote {totals_path}")
    print(f"wrote {notes_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
