from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions + OCR")
RESULTS = BASE / "results"


def text_tokens(text: str) -> int:
    # Conservative local estimate when the OpenAI token-counting endpoint is unavailable.
    return max(1, math.ceil(len(text) / 4))


def file_text_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return text_tokens(path.read_text(encoding="utf-8", errors="ignore"))
    except UnicodeDecodeError:
        return 0


def image_tokens(path: Path) -> int:
    # Approximate high-detail image cost: base 85 + 170 per 512px tile after scaling
    # the longest side to at most 2048, which mirrors common OpenAI vision accounting.
    if not path.exists():
        return 0
    with Image.open(path) as img:
        width, height = img.size
    scale = min(1.0, 2048 / max(width, height))
    scaled_w = math.ceil(width * scale)
    scaled_h = math.ceil(height * scale)
    tiles = math.ceil(scaled_w / 512) * math.ceil(scaled_h / 512)
    return 85 + 170 * tiles


def call_row(
    call_id: str,
    actor: str,
    round_name: str,
    prompt: str,
    text_files: list[Path],
    image_files: list[Path],
    expected_output: int,
    notes: str,
) -> dict[str, object]:
    prompt_est = text_tokens(prompt)
    file_est = sum(file_text_tokens(path) for path in text_files)
    image_est = sum(image_tokens(path) for path in image_files)
    input_expected = prompt_est + file_est + image_est
    return {
        "document": 22,
        "iteration": 1,
        "call_id": call_id,
        "actor": actor,
        "round": round_name,
        "input_tokens_low": math.ceil(input_expected * 0.75),
        "input_tokens_expected": input_expected,
        "input_tokens_high": math.ceil(input_expected * 1.35),
        "cached_input_tokens": 0,
        "output_tokens_low": math.ceil(expected_output * 0.55),
        "output_tokens_expected": expected_output,
        "output_tokens_high": math.ceil(expected_output * 1.8),
        "reasoning_tokens": "not_available",
        "image_file_input_tokens_expected": image_est,
        "total_tokens_low": math.ceil(input_expected * 0.75) + math.ceil(expected_output * 0.55),
        "total_tokens_expected": input_expected + expected_output,
        "total_tokens_high": math.ceil(input_expected * 1.35) + math.ceil(expected_output * 1.8),
        "usage_source": "local_estimate_no_api_key",
        "notes": notes,
    }


def main() -> None:
    crops = BASE / "precision_review_crops"
    full_images = [
        BASE / "raw -- synthetic_npp_electrical_schematic_clean.png",
        BASE / "component_labels_banners_overlay.png",
        BASE / "wire_nodes_overlay.png",
        BASE / "wires_mask_overlay.png",
    ]
    review_images = [
        crops / "raw__full_top.png",
        crops / "raw__full_upper_mid.png",
        crops / "raw__full_lower_mid.png",
        crops / "raw__full_bottom.png",
        crops / "raw__upper_left.png",
        crops / "raw__upper_right.png",
        crops / "raw__bottom_left.png",
        crops / "raw__bottom_center.png",
        crops / "raw__bottom_right.png",
        crops / "nodes__full_upper_mid.png",
        crops / "nodes__full_bottom.png",
    ]
    component_index = [crops / "component_index_by_position.md", BASE / "component_visual_ocr_labels.csv", BASE / "wire_nodes.csv"]
    diego_files = [
        RESULTS / "document22_round01_diego_edges.csv",
        RESULTS / "document22_round01_diego_nodes.csv",
        RESULTS / "document22_round01_diego_notes.md",
    ]
    jennifer_files = [
        RESULTS / "document22_round02_jennifer_edges.csv",
        RESULTS / "document22_round02_jennifer_nodes.csv",
        RESULTS / "document22_round02_jennifer_notes.md",
    ]

    rows = [
        call_row(
            "main-01",
            "main",
            "setup_visual_inventory",
            "Inventory document 22 resources, prepare crops, inspect raw schematic regions, and coordinate subagents.",
            component_index,
            review_images,
            1800,
            "Main orchestration and local visual inspection. Usage object not exposed in this environment.",
        ),
        call_row(
            "diego-01",
            "Diego",
            "round01_high_recall_extraction",
            "High-recall extraction prompt for document 22 with raw folder restriction and required CSV/matrix outputs.",
            component_index,
            full_images + review_images,
            5000,
            "Subagent call. Actual usage object not returned by multi-agent tool; estimated from planned payload and likely inspected images.",
        ),
        call_row(
            "jennifer-01",
            "Jennifer",
            "round02_precision_review",
            "Precision review prompt for document 22, focusing on Diego low/medium-confidence edges and raw-supported omissions.",
            component_index + diego_files,
            full_images + review_images,
            4500,
            "Subagent call. Actual usage object not returned by multi-agent tool; estimated from planned payload and likely inspected images.",
        ),
        call_row(
            "diego-02",
            "Diego",
            "round03_saturation_review",
            "Saturation pass prompt: compare Diego round 01 against Jennifer round 02 and accept or contest only with visual evidence.",
            component_index + diego_files + jennifer_files,
            review_images,
            3000,
            "Planned/actual if run after Jennifer. Output unknown before completion; low/expected/high included.",
        ),
        call_row(
            "jennifer-02",
            "Jennifer",
            "round04_final_agreement",
            "Final agreement prompt: review Diego saturation response and write agreed final round matrix.",
            component_index + jennifer_files,
            review_images,
            2500,
            "Planned/actual if run after Diego saturation. Output unknown before completion; low/expected/high included.",
        ),
        call_row(
            "main-final",
            "main",
            "final_packaging",
            "Generate final matrix aliases, validation summaries, round comparison, token report, and final response.",
            diego_files + jennifer_files,
            [],
            1800,
            "Main final packaging. Actual usage object unavailable; estimated from artifact sizes.",
        ),
    ]

    RESULTS.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS / "document22_token_usage_estimates.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    totals = {
        "document": 22,
        "iteration": 1,
        "method": "No OpenAI API key or response usage objects were available. Estimates use char/4 text tokens plus approximate high-detail image tile tokens.",
        "totals": {
            "input_tokens_low": sum(int(r["input_tokens_low"]) for r in rows),
            "input_tokens_expected": sum(int(r["input_tokens_expected"]) for r in rows),
            "input_tokens_high": sum(int(r["input_tokens_high"]) for r in rows),
            "output_tokens_low": sum(int(r["output_tokens_low"]) for r in rows),
            "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in rows),
            "output_tokens_high": sum(int(r["output_tokens_high"]) for r in rows),
            "image_file_input_tokens_expected": sum(int(r["image_file_input_tokens_expected"]) for r in rows),
            "total_tokens_low": sum(int(r["total_tokens_low"]) for r in rows),
            "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in rows),
            "total_tokens_high": sum(int(r["total_tokens_high"]) for r in rows),
        },
        "calls": rows,
    }
    (RESULTS / "document22_token_usage_estimates.json").write_text(json.dumps(totals, indent=2), encoding="utf-8")
    print(json.dumps(totals["totals"], indent=2))


if __name__ == "__main__":
    main()
