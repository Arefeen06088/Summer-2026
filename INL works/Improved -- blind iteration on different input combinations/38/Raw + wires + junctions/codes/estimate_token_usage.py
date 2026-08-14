from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image


DOC = "38"
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc38_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions")
ROUND_DIR = WORK / "results"
DESIGNATED_RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"


def result_dir() -> Path:
    try:
        DESIGNATED_RESULTS.mkdir(parents=True, exist_ok=True)
        probe = DESIGNATED_RESULTS / ".write_probe_doc38"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return DESIGNATED_RESULTS
    except OSError:
        FALLBACK_RESULTS.mkdir(parents=True, exist_ok=True)
        return FALLBACK_RESULTS


def text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def image_tokens(path: Path, detail: str = "high") -> int:
    with Image.open(path) as img:
        w, h = img.size
    if detail != "high":
        return 85
    scale = min(2048 / max(w, h), 1.0)
    w2 = int(w * scale)
    h2 = int(h * scale)
    if min(w2, h2) > 768:
        scale2 = 768 / min(w2, h2)
        w2 = int(w2 * scale2)
        h2 = int(h2 * scale2)
    tiles = math.ceil(w2 / 512) * math.ceil(h2 / 512)
    return 85 + 170 * tiles


def round_text_file(name: str) -> tuple[int, int]:
    path = ROUND_DIR / name
    if not path.exists():
        return 0, 0
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text_tokens(text), len(text)


def main() -> None:
    out_dir = result_dir()
    crops = out_dir / "inspection_crops"
    if not crops.exists():
        crops = ROUND_DIR / "inspection_crops"

    selected_images = [
        crops / "raw_overview_2400.png",
        crops / "raw_top_full.png",
        crops / "raw_mid_full.png",
        crops / "raw_bottom_full.png",
        crops / "raw_lower_control_center.png",
        crops / "nodes_overview_2400.png",
        crops / "wires_overview_2400.png",
    ]
    image_expected = sum(image_tokens(path) for path in selected_images if path.exists())

    prompt_base = text_tokens(
        "Document 38 schematic connectivity extraction. Use only Raw + wires + junctions. "
        "Return NODE_LIST_CSV and EDGE_LIST_CSV with evidence. Diego high recall and Jennifer precision rounds."
    )
    main_text = prompt_base + text_tokens(str(ROOT)) + text_tokens(str(selected_images))

    files = {
        "diego_round1": "diego_doc38_round1_extraction.txt",
        "jennifer_round1": "jennifer_doc38_round1_precision.txt",
        "diego_round2": "diego_doc38_round2_extraction.txt",
        "jennifer_round2_final": "jennifer_doc38_round2_final.txt",
    }
    output_actual = {}
    for slug, filename in files.items():
        toks, _chars = round_text_file(filename)
        output_actual[slug] = toks or {
            "diego_round1": 2200,
            "jennifer_round1": 2200,
            "diego_round2": 2000,
            "jennifer_round2_final": 2000,
        }[slug]

    rows = []
    calls = [
        ("main_doc38_orchestration", "main", "Codex GPT-5 session", main_text + image_expected, 1800, "Local orchestration and visual inspection estimate."),
        ("diego_round1", "Diego", "gpt-5.5-based visual subagent (usage object unavailable)", prompt_base + image_expected, output_actual["diego_round1"], "high-recall extractor"),
        ("jennifer_round1", "Jennifer", "gpt-5.5-based visual subagent (usage object unavailable)", prompt_base + image_expected + output_actual["diego_round1"], output_actual["jennifer_round1"], "precision reviewer"),
        ("diego_round2", "Diego", "gpt-5.5-based visual subagent (usage object unavailable)", prompt_base + image_expected + output_actual["jennifer_round1"], output_actual["diego_round2"], "agreement/high-recall reconciliation"),
        ("jennifer_round2_final", "Jennifer", "gpt-5.5-based visual subagent (usage object unavailable)", prompt_base + image_expected + output_actual["diego_round2"], output_actual["jennifer_round2_final"], "final precision saturation"),
    ]
    for call_id, agent, model, expected_in, expected_out, notes in calls:
        rows.append(
            {
                "document": DOC,
                "iteration": 1,
                "call_id": call_id,
                "agent": agent,
                "model": model,
                "input_tokens_low": max(1, int(expected_in * 0.85)),
                "input_tokens_expected": expected_in,
                "input_tokens_high": int(expected_in * 1.15),
                "cached_input_tokens": 0,
                "output_tokens_low": max(1, int(expected_out * 0.75)),
                "output_tokens_expected": expected_out,
                "output_tokens_high": int(expected_out * 1.35),
                "reasoning_tokens": "unavailable",
                "image_file_input_tokens_expected": image_expected,
                "text_file_input_tokens_expected": max(0, expected_in - image_expected),
                "usage_object": "not exposed in Codex tool transcript",
                "notes": notes,
            }
        )

    csv_path = out_dir / "token_usage_estimate_doc38.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    expected_total = sum(row["input_tokens_expected"] + row["output_tokens_expected"] for row in rows)
    md_lines = [
        "# Document 38 Token Usage Estimate",
        "",
        "No API key or subagent usage objects were available, so these are local estimates.",
        "Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.",
        "",
        "| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |",
        "|---|---:|---|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call_id']} | {row['agent']} | "
            f"{row['input_tokens_expected']} | {row['image_file_input_tokens_expected']} | "
            f"{row['output_tokens_expected']} | {row['input_tokens_expected'] + row['output_tokens_expected']} |"
        )
    md_lines.extend(["", f"Expected total tokens across listed calls: {expected_total}", ""])
    (out_dir / "token_usage_estimate_doc38.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"expected_total_tokens={expected_total}")


if __name__ == "__main__":
    main()
