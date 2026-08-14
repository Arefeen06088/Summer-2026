from __future__ import annotations

import csv
import math
import os
from pathlib import Path

from PIL import Image


DOC = 26
ITERATION = 1
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + junctions"
)
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc26_work")
RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"
CROPS = RESULTS / "inspection_crops"
FALLBACK_CROPS = WORK / "inspection_crops"


def result_dir() -> Path:
    if RESULTS.exists() and any(RESULTS.glob("*_matrix.csv")):
        return RESULTS
    return FALLBACK_RESULTS


def crop_dir() -> Path:
    if CROPS.exists() and any(CROPS.glob("*.png")):
        return CROPS
    return FALLBACK_CROPS


def token_counter():
    try:
        import tiktoken

        encoding = tiktoken.get_encoding("o200k_base")
        return lambda text: len(encoding.encode(text))
    except Exception:
        return lambda text: max(1, math.ceil(len(text) / 4))


count_tokens = token_counter()


def file_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return count_tokens(path.read_text(encoding="utf-8", errors="ignore"))
    except UnicodeDecodeError:
        return 0


def image_tokens(paths: list[Path]) -> tuple[int, int, int]:
    low = expected = high = 0
    for path in paths:
        if not path.exists():
            continue
        with Image.open(path) as image:
            width, height = image.size
        tiles = math.ceil(width / 512) * math.ceil(height / 512)
        low += 85
        expected += 85 + 170 * tiles
        high += 85 + 255 * tiles
    return low, expected, high


def row(round_name: str, agent: str, text_paths: list[Path], image_paths: list[Path], output_paths: list[Path], reasoning_expected: int, notes: str) -> dict[str, int | str]:
    text_expected = sum(file_tokens(path) for path in text_paths)
    prompt_floor = {
        "Setup and visual inspection": 3000,
        "Diego round 1": 4500,
        "Jennifer round 1": 5500,
        "Diego round 2": 4500,
        "Jennifer round 2 final": 3500,
        "Generation and validation": 2500,
    }.get(round_name, 2500)
    input_expected = max(prompt_floor, text_expected + prompt_floor)
    input_low = max(1000, math.floor(input_expected * 0.75))
    input_high = math.ceil(input_expected * 1.45)
    image_low, image_expected, image_high = image_tokens(image_paths)
    output_expected = sum(file_tokens(path) for path in output_paths)
    if output_expected == 0:
        output_expected = {
            "Diego round 1": 6500,
            "Jennifer round 1": 4500,
            "Diego round 2": 2500,
            "Jennifer round 2 final": 2000,
            "Setup and visual inspection": 1500,
            "Generation and validation": 1800,
        }.get(round_name, 1800)
    output_low = max(500, math.floor(output_expected * 0.65))
    output_high = math.ceil(output_expected * 1.5)
    reasoning_low = max(0, math.floor(reasoning_expected * 0.45))
    reasoning_high = math.ceil(reasoning_expected * 1.8)
    total_low = input_low + image_low + output_low + reasoning_low
    total_expected = input_expected + image_expected + output_expected + reasoning_expected
    total_high = input_high + image_high + output_high + reasoning_high
    return {
        "document": DOC,
        "iteration": ITERATION,
        "round": round_name,
        "agent": agent,
        "model_call_made": "yes",
        "input_tokens_low": input_low,
        "input_tokens_expected": input_expected,
        "input_tokens_high": input_high,
        "cached_input_tokens_expected": 0,
        "image_file_input_tokens_low": image_low,
        "image_file_input_tokens_expected": image_expected,
        "image_file_input_tokens_high": image_high,
        "output_tokens_low": output_low,
        "output_tokens_expected": output_expected,
        "output_tokens_high": output_high,
        "reasoning_tokens_low": reasoning_low,
        "reasoning_tokens_expected": reasoning_expected,
        "reasoning_tokens_high": reasoning_high,
        "total_tokens_low": total_low,
        "total_tokens_expected": total_expected,
        "total_tokens_high": total_high,
        "usage_object_available": "no",
        "notes": notes,
    }


def main() -> None:
    base = result_dir()
    crops = crop_dir()
    key_images = [
        crops / "raw_overview_1800.png",
        crops / "raw_doc26_top_full.png",
        crops / "raw_doc26_mid_full.png",
        crops / "raw_doc26_bottom_full.png",
        crops / "raw_doc26_A_mcc_control_close.png",
        crops / "raw_doc26_B_mcc_control_close.png",
        crops / "raw_doc26_A_ups_close.png",
        crops / "raw_doc26_B_ups_close.png",
    ]
    review_images = [
        crops / "raw_doc26_feeder_mid_close.png",
        crops / "raw_doc26_A_interlock_routes.png",
        crops / "raw_doc26_B_interlock_routes.png",
        crops / "wires_doc26_mid_full.png",
        crops / "nodes_doc26_mid_full.png",
    ]
    rows = [
        row("Setup and visual inspection", "Main Codex agent", [WORK / "create_inspection_crops.py"], key_images[:4], [], 5000, "Main inspected resources/crops and planned the Diego/Jennifer workflow."),
        row("Diego round 1", "Diego", [WORK / "create_inspection_crops.py"], key_images + review_images, [base / "diego_round1_output.txt"], 8000, "High-recall visual extraction; multi-agent usage object not exposed."),
        row("Jennifer round 1", "Jennifer", [base / "diego_round1_output.txt"], key_images + review_images, [base / "jennifer_round1_review.txt"], 7000, "Precision review of Diego proposal; usage object not exposed."),
        row("Diego round 2", "Diego", [base / "jennifer_round1_review.txt", base / "connectivity_edges_final.csv"], review_images, [base / "diego_round2_response.txt"], 2500, "Agreement/saturation check after Jennifer corrections."),
        row("Jennifer round 2 final", "Jennifer", [base / "diego_round2_response.txt", base / "connectivity_edges_final.csv"], review_images, [base / "jennifer_round2_final.txt"], 2500, "Final precision confirmation."),
        row("Generation and validation", "Main Codex agent", [WORK / "generate_doc26_round_outputs.py", WORK / "extract_and_validate_rounds.py"], [], [base / "round_validation_summary.csv"], 4000, "Local CSV/matrix generation, validation, and summary."),
    ]

    api_note = (
        "OPENAI_API_KEY was not present; the OpenAI Responses input-token counting endpoint was not called."
        if not os.environ.get("OPENAI_API_KEY")
        else "OPENAI_API_KEY was present, but this local workflow did not call the Responses counting endpoint."
    )
    csv_path = base / "token_usage_estimate_doc26.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    low_total = sum(int(item["total_tokens_low"]) for item in rows)
    expected_total = sum(int(item["total_tokens_expected"]) for item in rows)
    high_total = sum(int(item["total_tokens_high"]) for item in rows)
    md_lines = [
        "# Token Usage Estimate - Document 26, Iteration 1",
        "",
        api_note,
        "Multi-agent tool responses did not expose usage objects, cached token counts, or reasoning token counts; all values here are estimates.",
        "",
        "| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in rows:
        md_lines.append(
            f"| {item['document']} | {item['iteration']} | {item['round']} | {item['agent']} | "
            f"{item['input_tokens_expected']} | {item['cached_input_tokens_expected']} | "
            f"{item['image_file_input_tokens_expected']} | {item['output_tokens_expected']} | "
            f"{item['reasoning_tokens_expected']} | {item['total_tokens_expected']} |"
        )
    md_lines.extend(
        [
            "",
            f"Low total estimate: {low_total}",
            "",
            f"Expected total estimate: {expected_total}",
            "",
            f"High total estimate: {high_total}",
        ]
    )
    md_path = base / "token_usage_estimate_doc26.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"token estimates written to {csv_path} and {md_path}")


if __name__ == "__main__":
    main()
