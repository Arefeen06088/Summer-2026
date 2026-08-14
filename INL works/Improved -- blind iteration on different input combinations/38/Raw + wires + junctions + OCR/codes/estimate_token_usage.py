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

DOCUMENT = "38"
ITERATION = "1"
MODEL = "gpt-5.5"


def text_tokens(text: str) -> int:
    if not text:
        return 0
    if tiktoken is not None:
        try:
            return len(tiktoken.get_encoding("o200k_base").encode(text))
        except Exception:  # noqa: BLE001
            pass
    return math.ceil(len(text) / 4)


def file_tokens(path: Path) -> int:
    return text_tokens(path.read_text(encoding="utf-8", errors="ignore")) if path.exists() else 0


def image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    with Image.open(path) as image:
        width, height = image.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    short = min(width, height)
    if short > 768:
        scale2 = 768 / short
        width *= scale2
        height *= scale2
    return 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)


def image_sum(paths: list[Path]) -> int:
    return sum(image_tokens(path) for path in paths)


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    results = base / "results"
    crops = base / "precision_review_crops"
    raw = sorted(base.glob("raw -- *.png"))[0]
    full_images = [raw, base / "component_labels_banners_overlay.png", base / "wires_mask_overlay.png", base / "wire_nodes_overlay.png"]
    key_names = [
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
    key_crops = [crops / name for name in key_names if (crops / name).exists()]
    all_crops = sorted(crops.glob("*.png"))
    task = "Extract document 38 connectivity matrix using Diego high-recall and Jennifer precision review. No GT and no off-the-shelf OCR."
    prompt_bits = {
        "main-01": task,
        "diego-01": task + " Inspect raw, overlays, CSV aids, and crops. Write high-recall round 01 graph.",
        "jennifer-01": task + " Review Diego, prune unsupported edges, write precision round 02 graph.",
        "diego-02": task + " Recheck Jennifer changes and saturate in round 03.",
        "jennifer-02": task + " Final precision sign-off and saturation in round 04.",
        "main-02": task + " Validate final graph, compare rounds, and summarize.",
    }
    round_files = {
        "main-01": [],
        "diego-01": [base / "component_visual_ocr_labels.csv", base / "wire_nodes.csv"],
        "jennifer-01": [base / "component_visual_ocr_labels.csv", base / "wire_nodes.csv", results / "document38_round01_diego_edges.csv", results / "document38_round01_diego_nodes.csv", results / "document38_round01_diego_notes.md"],
        "diego-02": [base / "component_visual_ocr_labels.csv", base / "wire_nodes.csv", results / "document38_round01_diego_edges.csv", results / "document38_round02_jennifer_edges.csv", results / "document38_round02_jennifer_notes.md"],
        "jennifer-02": [base / "component_visual_ocr_labels.csv", base / "wire_nodes.csv", results / "document38_round01_diego_edges.csv", results / "document38_round02_jennifer_edges.csv", results / "document38_round03_diego_edges.csv", results / "document38_round03_diego_notes.md"],
        "main-02": [results / "document38_round01_diego_notes.md", results / "document38_round02_jennifer_notes.md", results / "document38_round03_diego_notes.md", results / "document38_round04_jennifer_notes.md"],
    }
    output_ranges = {
        "main-01": (250, 600, 1200),
        "diego-01": (7000, 12000, 20000),
        "jennifer-01": (6000, 10000, 18000),
        "diego-02": (4000, 8000, 15000),
        "jennifer-02": (3500, 6500, 12000),
        "main-02": (700, 1200, 2200),
    }
    agents = {
        "main-01": ("main", "setup", "orchestrator"),
        "diego-01": ("Diego", "01", "high-recall extractor"),
        "jennifer-01": ("Jennifer", "02", "precision reviewer"),
        "diego-02": ("Diego", "03", "saturation extractor"),
        "jennifer-02": ("Jennifer", "04", "final precision signoff"),
        "main-02": ("main", "finalize", "orchestrator"),
    }
    image_low = image_sum([raw, base / "component_labels_banners_overlay.png", base / "wire_nodes_overlay.png"])
    image_expected = image_sum(full_images + key_crops)
    image_high = image_sum(full_images + all_crops)
    image_calls = {"diego-01", "jennifer-01", "diego-02", "jennifer-02"}
    rows = []
    for call_id in ["main-01", "diego-01", "jennifer-01", "diego-02", "jennifer-02", "main-02"]:
        expected_text = text_tokens(prompt_bits[call_id]) + sum(file_tokens(path) for path in round_files[call_id])
        low_text = math.ceil(expected_text * 0.75)
        high_text = math.ceil(expected_text * 1.25)
        low_img = image_low if call_id in image_calls else 0
        exp_img = image_expected if call_id in image_calls else 0
        high_img = image_high if call_id in image_calls else 0
        out_low, out_exp, out_high = output_ranges[call_id]
        agent, round_name, role = agents[call_id]
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "call_id": call_id,
                "agent": agent,
                "round": round_name,
                "role": role,
                "model": MODEL,
                "input_text_tokens_low": low_text,
                "input_text_tokens_expected": expected_text,
                "input_text_tokens_high": high_text,
                "cached_input_tokens": "unknown",
                "image_file_input_tokens_low": low_img,
                "image_file_input_tokens_expected": exp_img,
                "image_file_input_tokens_high": high_img,
                "output_tokens_low": out_low,
                "output_tokens_expected": out_exp,
                "output_tokens_high": out_high,
                "reasoning_tokens": "unavailable",
                "total_tokens_low": low_text + low_img + out_low,
                "total_tokens_expected": expected_text + exp_img + out_exp,
                "total_tokens_high": high_text + high_img + out_high,
                "usage_object_available": "no",
                "counting_method": "tiktoken o200k_base for text; public high-detail image tiling estimate; output ranges estimated",
            }
        )
    detail_path = results / f"document{DOCUMENT}_token_usage_estimates.csv"
    with detail_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    totals = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "calls": len(rows),
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "input_text_tokens_expected": sum(int(row["input_text_tokens_expected"]) for row in rows),
        "image_file_input_tokens_expected": sum(int(row["image_file_input_tokens_expected"]) for row in rows),
        "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in rows),
        "openai_api_key_present": "yes" if os.environ.get("OPENAI_API_KEY") else "no",
    }
    totals_path = results / f"document{DOCUMENT}_token_usage_totals.csv"
    with totals_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(totals.keys()))
        writer.writeheader()
        writer.writerow(totals)
    (results / f"document{DOCUMENT}_token_usage_notes.md").write_text(
        "# Document 38 Token Usage Notes\n\n"
        "- Actual model usage objects were unavailable to this local script.\n"
        "- If `OPENAI_API_KEY` is `no` in totals, the Responses token-counting endpoint could not be called.\n"
        "- Text estimates use `tiktoken` `o200k_base`; image estimates use public high-detail image tiling.\n"
        "- Low/expected/high ranges vary visual context volume and unknown output length.\n",
        encoding="utf-8",
    )
    print(f"wrote {detail_path}")
    print(f"wrote {totals_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
