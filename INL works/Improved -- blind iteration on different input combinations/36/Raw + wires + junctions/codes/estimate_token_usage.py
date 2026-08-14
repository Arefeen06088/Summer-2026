from __future__ import annotations

import csv
import math
from pathlib import Path


DOC = "36"
ITERATION = "1"
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc36_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + junctions")
DESIGNATED_RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"
CROPS = WORK / "inspection_crops"

MAIN_IMAGES = [
    "raw_overview_2400.png",
    "raw_doc36_top_full.png",
    "raw_doc36_mid_full.png",
    "raw_doc36_bottom_full.png",
    "raw_doc36_left_full.png",
    "raw_doc36_center_full.png",
    "raw_doc36_right_full.png",
]

SUBAGENT_IMAGES = [
    "raw_overview_2400.png",
    "raw_doc36_top_full.png",
    "raw_doc36_mid_full.png",
    "raw_doc36_bottom_full.png",
    "raw_doc36_left_full.png",
    "raw_doc36_center_full.png",
    "raw_doc36_right_full.png",
    "raw_doc36_lower_bus_center.png",
    "nodes_overview_2400.png",
]

ROUND_TEXTS = {
    "diego_round1": WORK / "results" / "diego_doc36_round1_extraction.txt",
    "jennifer_round1": WORK / "results" / "jennifer_doc36_round1_precision.txt",
    "diego_round2": WORK / "results" / "diego_doc36_round2_extraction.txt",
    "jennifer_round2_final": WORK / "results" / "jennifer_doc36_round2_final.txt",
}


def result_dir() -> Path:
    try:
        DESIGNATED_RESULTS.mkdir(parents=True, exist_ok=True)
        probe = DESIGNATED_RESULTS / ".write_probe_doc36_tokens"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return DESIGNATED_RESULTS
    except OSError:
        FALLBACK_RESULTS.mkdir(parents=True, exist_ok=True)
        return FALLBACK_RESULTS


def token_count(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        try:
            enc = tiktoken.encoding_for_model("gpt-5")
        except Exception:
            enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def file_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    return token_count(path.read_text(encoding="utf-8-sig", errors="replace"))


def image_size(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image

        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def image_tokens(path: Path) -> int:
    size = image_size(path)
    if not size:
        return 0
    width, height = size
    scale = min(1.0, 2048 / max(width, height))
    width *= scale
    height *= scale
    scale = min(1.0, 768 / min(width, height))
    width *= scale
    height *= scale
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * max(1, tiles)


def image_set_tokens(names: list[str]) -> int:
    return sum(image_tokens(CROPS / name) for name in names)


def output_estimate(path: Path, fallback_expected: int) -> tuple[int, int, int, str]:
    if path.exists():
        actual = file_tokens(path)
        return actual, actual, actual, "actual_text_file_estimate"
    return max(1500, fallback_expected // 2), fallback_expected, fallback_expected * 2, "planned_output_estimate"


def rows() -> list[dict[str, str | int]]:
    prompt_core = token_count(
        "Extract/review schematic connectivity matrix from raw nuclear plant AC/DC distribution schematic. "
        "Use only allowed Raw + wires + junctions resources. No GT and no OCR. "
        "Rows and columns share the same node order; undirected symmetric matrix; diagonal zero."
    )
    wire_csv_tokens = file_tokens(ROOT / "wire_nodes.csv")
    main_image_tokens = image_set_tokens(MAIN_IMAGES)
    subagent_image_tokens = image_set_tokens(SUBAGENT_IMAGES)
    data: list[dict[str, str | int]] = []
    data.append(
        {
            "document": DOC,
            "iteration": ITERATION,
            "call_id": "main_doc36_orchestration",
            "agent": "main",
            "model": "Codex GPT-5 session",
            "input_tokens_low": prompt_core + main_image_tokens // 2,
            "input_tokens_expected": prompt_core + wire_csv_tokens + main_image_tokens,
            "input_tokens_high": prompt_core + wire_csv_tokens + int(main_image_tokens * 1.25),
            "cached_input_tokens": 0,
            "output_tokens_low": 800,
            "output_tokens_expected": 1600,
            "output_tokens_high": 3000,
            "reasoning_tokens": "unavailable",
            "image_file_input_tokens_expected": main_image_tokens,
            "text_file_input_tokens_expected": prompt_core + wire_csv_tokens,
            "usage_object": "not exposed in Codex tool transcript",
            "notes": "Local orchestration and visual inspection estimate.",
        }
    )
    specs = [
        ("diego_round1", "Diego", "high-recall extractor", None, 5200),
        ("jennifer_round1", "Jennifer", "precision reviewer", "diego_round1", 4800),
        ("diego_round2", "Diego", "agreement/high-recall reconciliation", "jennifer_round1", 3500),
        ("jennifer_round2_final", "Jennifer", "final precision saturation", "diego_round2", 3000),
    ]
    for slug, agent, role, prior_slug, fallback_out in specs:
        prior_tokens = file_tokens(ROUND_TEXTS[prior_slug]) if prior_slug else 0
        text_expected = prompt_core + prior_tokens
        out_low, out_exp, out_high, usage_source = output_estimate(ROUND_TEXTS[slug], fallback_out)
        data.append(
            {
                "document": DOC,
                "iteration": ITERATION,
                "call_id": slug,
                "agent": agent,
                "model": "gpt-5.5-based visual subagent (usage object unavailable)",
                "input_tokens_low": int((text_expected + subagent_image_tokens) * 0.85),
                "input_tokens_expected": text_expected + subagent_image_tokens,
                "input_tokens_high": int((text_expected + subagent_image_tokens) * 1.15),
                "cached_input_tokens": 0,
                "output_tokens_low": out_low,
                "output_tokens_expected": out_exp,
                "output_tokens_high": out_high,
                "reasoning_tokens": "unavailable",
                "image_file_input_tokens_expected": subagent_image_tokens,
                "text_file_input_tokens_expected": text_expected,
                "usage_object": usage_source,
                "notes": role,
            }
        )
    return data


def main() -> None:
    out_dir = result_dir()
    data = rows()
    csv_path = out_dir / "token_usage_estimate_doc36.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    expected_total = sum(int(row["input_tokens_expected"]) + int(row["output_tokens_expected"]) for row in data)
    md_lines = [
        "# Document 36 Token Usage Estimate",
        "",
        "No API key or subagent usage objects were available, so these are local estimates.",
        "Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.",
        "",
        "| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |",
        "|---|---:|---|---|---:|---:|---:|---:|",
    ]
    for row in data:
        total = int(row["input_tokens_expected"]) + int(row["output_tokens_expected"])
        md_lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call_id']} | {row['agent']} | "
            f"{row['input_tokens_expected']} | {row['image_file_input_tokens_expected']} | "
            f"{row['output_tokens_expected']} | {total} |"
        )
    md_lines.extend(["", f"Expected total tokens across listed calls: {expected_total}"])
    (out_dir / "token_usage_estimate_doc36.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"expected_total_tokens={expected_total}")


if __name__ == "__main__":
    main()
