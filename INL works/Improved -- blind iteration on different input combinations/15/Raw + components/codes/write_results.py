from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path
from typing import Any

from PIL import Image


DOC = "15"
ITERATION = "1"
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + components"
)
CODES = ROOT / "codes"
RESULTS = ROOT / "results"
WORK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\results")

FINAL_NODES_FILE = WORK_RESULTS / "doc15_round2_jennifer_final_nodes.json"
FINAL_EDGES_FILE = WORK_RESULTS / "doc15_round2_jennifer_final_edges.json"
FINAL_MATRIX_FILE = WORK_RESULTS / "doc15_round2_jennifer_final_matrix.csv"

ROUND_FILES = [
    "doc15_round1_diego_connectivity_proposal.json",
    "doc15_round1_diego_connectivity_matrix.csv",
    "doc15_round1_jennifer_nodes.json",
    "doc15_round1_jennifer_edges.json",
    "doc15_round1_jennifer_matrix.csv",
    "doc15_round2_diego_connectivity_proposal.json",
    "doc15_round2_diego_connectivity_matrix.csv",
    "doc15_round2_jennifer_final_nodes.json",
    "doc15_round2_jennifer_final_edges.json",
    "doc15_round2_jennifer_final_matrix.csv",
]

ROUND_MATRIX_ALIASES = {
    "doc15_round1_diego_connectivity_matrix.csv": "diego_round1_connectivity_matrix.csv",
    "doc15_round1_jennifer_matrix.csv": "jennifer_round1_connectivity_matrix.csv",
    "doc15_round2_diego_connectivity_matrix.csv": "diego_round2_connectivity_matrix.csv",
    "doc15_round2_jennifer_final_matrix.csv": "jennifer_round2_final_connectivity_matrix.csv",
}

IMAGE_BUNDLE = [
    ROOT / "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    ROOT / "detected_components_and_logical_overlay.png",
    RESULTS / "raw_02_offsite_sources_top_2x.png",
    RESULTS / "raw_07_div_1a_safety_4160_480_2x.png",
    RESULTS / "raw_08_div_1b_safety_4160_480_2x.png",
    RESULTS / "raw_09_div_2a_safety_4160_480_2x.png",
    RESULTS / "raw_10_div_2b_safety_4160_480_2x.png",
    RESULTS / "raw_11_div_1a_mcc_loads.png",
    RESULTS / "raw_12_div_1b_mcc_loads.png",
    RESULTS / "raw_13_div_2a_mcc_loads.png",
    RESULTS / "raw_14_div_2b_mcc_loads.png",
    RESULTS / "raw_19_tie_1a_1b_2x.png",
    RESULTS / "raw_20_tie_2a_2b_2x.png",
    RESULTS / "raw_26_div_1a_dc_detail_2x.png",
    RESULTS / "raw_27_div_1b_dc_detail_2x.png",
    RESULTS / "raw_28_div_2a_dc_detail_2x.png",
    RESULTS / "raw_29_div_2b_dc_detail_2x.png",
    RESULTS / "raw_21_right_notes_legend.png",
    RESULTS / "raw_22_load_schedule.png",
]

MAIN_VIEWED_IMAGES = IMAGE_BUNDLE + [RESULTS / "raw_24_title_block.png"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_nodes(data: Any) -> list[str]:
    if isinstance(data, dict) and "nodes" in data:
        return list(data["nodes"])
    if isinstance(data, list):
        return list(data)
    raise ValueError("Could not extract nodes")


def edge_key(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop not expected: {a}")
    return tuple(sorted((a, b)))


def write_edge_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def validate_matrix(path: Path, nodes: list[str], edges: list[dict[str, Any]]) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    body = rows[1:]
    if header != nodes:
        raise ValueError("matrix header does not match final node order")
    if [row[0] for row in body] != nodes:
        raise ValueError("matrix row names do not match final node order")
    n = len(nodes)
    values = [[int(cell) for cell in row[1:]] for row in body]
    if any(len(row) != n for row in values):
        raise ValueError("matrix is not square")
    if any(values[i][i] != 0 for i in range(n)):
        raise ValueError("matrix diagonal is not zero")
    if any(values[i][j] not in (0, 1) for i in range(n) for j in range(n)):
        raise ValueError("matrix is not binary")
    if any(values[i][j] != values[j][i] for i in range(n) for j in range(n)):
        raise ValueError("matrix is not symmetric")
    index = {node: i for i, node in enumerate(nodes)}
    matrix_edges = set()
    for i, a in enumerate(nodes):
        for j in range(i + 1, n):
            if values[i][j] == 1:
                matrix_edges.add(edge_key(a, nodes[j]))
    json_edges = {edge_key(edge["source"], edge["target"]) for edge in edges}
    if matrix_edges != json_edges:
        missing = sorted(json_edges - matrix_edges)[:5]
        extra = sorted(matrix_edges - json_edges)[:5]
        raise ValueError(f"matrix/json edge mismatch; missing={missing}, extra={extra}")
    return {
        "node_count": n,
        "asserted_edge_count": len(json_edges),
        "matrix_rows": len(body),
        "matrix_columns": len(header),
        "symmetric": True,
        "diagonal_zero": True,
        "binary": True,
    }


def text_tokens(path: Path) -> int:
    return math.ceil(len(path.read_text(encoding="utf-8", errors="ignore")) / 4)


def image_tokens(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    scale = min(1.0, 2048 / max(w, h))
    w = int(math.ceil(w * scale))
    h = int(math.ceil(h * scale))
    if min(w, h) > 768:
        scale = 768 / min(w, h)
        w = int(math.ceil(w * scale))
        h = int(math.ceil(h * scale))
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def image_bundle_tokens(paths: list[Path]) -> int:
    return sum(image_tokens(path) for path in paths if path.exists())


def call_row(
    call: str,
    input_tokens: int,
    image_input_tokens: int,
    output_tokens: int,
    reasoning_tokens: int,
) -> dict[str, Any]:
    total_expected = input_tokens + image_input_tokens + output_tokens + reasoning_tokens
    total_low = input_tokens + image_input_tokens + math.ceil(output_tokens * 0.6) + math.ceil(reasoning_tokens * 0.4)
    total_high = input_tokens + image_input_tokens + math.ceil(output_tokens * 1.6) + math.ceil(reasoning_tokens * 2.0)
    return {
        "document": DOC,
        "iteration": ITERATION,
        "call": call,
        "input_tokens_est": input_tokens,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": image_input_tokens,
        "output_tokens_expected": output_tokens,
        "reasoning_tokens_expected": reasoning_tokens,
        "total_low": total_low,
        "total_expected": total_expected,
        "total_high": total_high,
        "usage_object_available": "no",
    }


def write_token_usage() -> list[dict[str, Any]]:
    diego_r1_out = text_tokens(WORK_RESULTS / "doc15_round1_diego_connectivity_proposal.json") + text_tokens(
        WORK_RESULTS / "doc15_round1_diego_connectivity_matrix.csv"
    )
    jennifer_r1_out = (
        text_tokens(WORK_RESULTS / "doc15_round1_jennifer_nodes.json")
        + text_tokens(WORK_RESULTS / "doc15_round1_jennifer_edges.json")
        + text_tokens(WORK_RESULTS / "doc15_round1_jennifer_matrix.csv")
    )
    diego_r2_out = text_tokens(WORK_RESULTS / "doc15_round2_diego_connectivity_proposal.json") + text_tokens(
        WORK_RESULTS / "doc15_round2_diego_connectivity_matrix.csv"
    )
    jennifer_r2_out = (
        text_tokens(WORK_RESULTS / "doc15_round2_jennifer_final_nodes.json")
        + text_tokens(WORK_RESULTS / "doc15_round2_jennifer_final_edges.json")
        + text_tokens(WORK_RESULTS / "doc15_round2_jennifer_final_matrix.csv")
    )

    rows = [
        call_row("Main Codex: main_orchestration_grouped", 22000, image_bundle_tokens(MAIN_VIEWED_IMAGES), 1200, 18000),
        call_row("Diego: diego_round1_high_recall_extraction", 5200, image_bundle_tokens(IMAGE_BUNDLE), diego_r1_out, 30000),
        call_row(
            "Jennifer: jennifer_round1_precision_review",
            6500 + diego_r1_out,
            image_bundle_tokens(IMAGE_BUNDLE),
            jennifer_r1_out,
            28000,
        ),
        call_row(
            "Diego: diego_round2_saturation_review",
            2800 + jennifer_r1_out,
            0,
            diego_r2_out,
            8000,
        ),
        call_row(
            "Jennifer: jennifer_round2_final_confirmation",
            2200 + diego_r2_out,
            0,
            jennifer_r2_out,
            6000,
        ),
    ]
    total = {
        "document": DOC,
        "iteration": ITERATION,
        "call": "TOTAL",
        "input_tokens_est": sum(int(row["input_tokens_est"]) for row in rows),
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": sum(int(row["image_file_input_tokens_est"]) for row in rows),
        "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in rows),
        "reasoning_tokens_expected": sum(int(row["reasoning_tokens_expected"]) for row in rows),
        "total_low": sum(int(row["total_low"]) for row in rows),
        "total_expected": sum(int(row["total_expected"]) for row in rows),
        "total_high": sum(int(row["total_high"]) for row in rows),
        "usage_object_available": "no",
    }
    all_rows = rows + [total]
    fields = list(all_rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Document 15 Token Usage Estimate\n\n")
        f.write(
            "No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. "
            "The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. "
            "Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: "
            "downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.\n\n"
        )
        f.write(
            "| Document | Iteration | Call | Input est | Cached | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |\n"
        )
        f.write("|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|\n")
        for row in all_rows:
            call = f"**{row['call']}**" if row["call"] == "TOTAL" else row["call"]
            f.write(
                f"| {row['document']} | {row['iteration']} | {call} | {row['input_tokens_est']} | "
                f"{row['cached_input_tokens']} | {row['image_file_input_tokens_est']} | "
                f"{row['output_tokens_expected']} | {row['reasoning_tokens_expected']} | "
                f"{row['total_low']} | {row['total_expected']} | {row['total_high']} |\n"
            )
    return all_rows


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    nodes_doc = load_json(FINAL_NODES_FILE)
    edges_doc = load_json(FINAL_EDGES_FILE)
    nodes = extract_nodes(nodes_doc)
    asserted = list(edges_doc["asserted_edges"])
    uncertain = list(edges_doc.get("uncertain_edges", []))
    removed = list(edges_doc.get("removed_edges", []))
    added = list(edges_doc.get("added_edges", []))
    corrections = list(edges_doc.get("label_corrections", []))

    validation = validate_matrix(FINAL_MATRIX_FILE, nodes, asserted)

    (RESULTS / "final_nodes.json").write_text(
        json.dumps({"document": DOC, "node_count": len(nodes), "nodes": nodes}, indent=2),
        encoding="utf-8",
    )
    shutil.copyfile(FINAL_EDGES_FILE, RESULTS / "final_edges.json")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "final_connectivity_matrix.csv")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "final_matrix.csv")

    write_edge_csv(RESULTS / "final_edges.csv", asserted, ["source", "target", "type", "evidence"])
    write_edge_csv(RESULTS / "final_uncertain_edges.csv", uncertain, ["source", "target", "reason"])
    write_edge_csv(RESULTS / "final_removed_edges.csv", removed, ["source", "target", "reason"])
    write_edge_csv(RESULTS / "final_added_edges.csv", added, ["source", "target", "type", "evidence"])
    write_edge_csv(RESULTS / "final_label_corrections.csv", corrections, ["from", "to", "reason"])

    j1_edges = load_json(WORK_RESULTS / "doc15_round1_jennifer_edges.json")
    write_edge_csv(
        RESULTS / "jennifer_round1_added_edges.csv",
        list(j1_edges.get("added_edges", [])),
        ["source", "target", "type", "evidence"],
    )

    rejected = []
    for row in uncertain:
        rejected.append({"source": row["source"], "target": row["target"], "status": "uncertain", "reason": row["reason"]})
    for row in removed:
        rejected.append({"source": row["source"], "target": row["target"], "status": "removed", "reason": row["reason"]})
    write_edge_csv(RESULTS / "final_rejected_non_edges.csv", rejected, ["source", "target", "status", "reason"])

    for filename in ROUND_FILES:
        src = WORK_RESULTS / filename
        if src.exists():
            shutil.copyfile(src, RESULTS / filename)
        alias = ROUND_MATRIX_ALIASES.get(filename)
        if alias and src.exists():
            shutil.copyfile(src, RESULTS / alias)

    with (RESULTS / "round_summaries.md").open("w", encoding="utf-8") as f:
        f.write("# Document 15 Round Summaries\n\n")
        f.write("- Diego round 1: 183 nodes, 130 asserted edges, 70 uncertain edges.\n")
        f.write("- Jennifer round 1: 183 nodes, 182 asserted edges, 52 additions, 0 removals, 18 uncertain edges.\n")
        f.write("- Diego round 2: agreed with Jennifer; matrix matched Jennifer round 1 byte-for-byte.\n")
        f.write("- Jennifer final round 2: no topology changes; final saturation confirmed.\n\n")
        f.write("Final consensus: 183 nodes, 182 asserted undirected edges, 18 uncertain edges kept out of the matrix.\n\n")
        f.write(
            "Key precision decisions: direct dashed endpoint-to-endpoint control traces were asserted; DG-to-NSS overlaps, "
            "direct bus-to-bus tie shortcuts, SEQ/RPS long paths, and relay-to-terminal-box tails stayed uncertain.\n"
        )

    token_rows = write_token_usage()

    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "source_restriction": "Doc15 Raw + components only; no GT, no Raw+wires, no OCR, no web",
        "validation": validation,
        "uncertain_edge_count": len(uncertain),
        "removed_edge_count": len(removed),
        "final_round_added_edge_count": len(added),
        "jennifer_round1_added_edge_count": len(j1_edges.get("added_edges", [])),
        "label_correction_count": len(corrections),
        "token_estimate_totals": token_rows[-1],
    }
    (RESULTS / "final_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
