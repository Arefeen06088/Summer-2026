from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path
from typing import Any

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

DOC = "36"
ITERATION = "1"
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + components"
)
CODES = ROOT / "codes"
RESULTS = ROOT / "results"
WORK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\results")

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_v2.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"

FINAL_NODES_FILE = WORK_RESULTS / "doc36_round2_jennifer_final_nodes.json"
FINAL_EDGES_FILE = WORK_RESULTS / "doc36_round2_jennifer_final_edges.json"
FINAL_MATRIX_FILE = WORK_RESULTS / "doc36_round2_jennifer_final_matrix.csv"

ROUND_FILES = [
    "doc36_round1_diego_connectivity_proposal.json",
    "doc36_round1_diego_connectivity_matrix.csv",
    "doc36_round1_jennifer_review.json",
    "doc36_round1_jennifer_connectivity_matrix.csv",
    "doc36_round2_diego_connectivity_proposal.json",
    "doc36_round2_diego_connectivity_matrix.csv",
    "doc36_round2_jennifer_final_nodes.json",
    "doc36_round2_jennifer_final_edges.json",
    "doc36_round2_jennifer_final_matrix.csv",
]

ROUND_MATRIX_ALIASES = {
    "doc36_round1_diego_connectivity_matrix.csv": "diego_round1_connectivity_matrix.csv",
    "doc36_round1_jennifer_connectivity_matrix.csv": "jennifer_round1_connectivity_matrix.csv",
    "doc36_round2_diego_connectivity_matrix.csv": "diego_round2_connectivity_matrix.csv",
    "doc36_round2_jennifer_final_matrix.csv": "jennifer_round2_final_connectivity_matrix.csv",
}

FINAL_JENNIFER_IMAGE_BUNDLE = [
    RAW,
    OVERLAY,
    RESULTS / "raw_full_preview.png",
    RESULTS / "overlay_full_preview.png",
    RESULTS / "raw_top.png",
    RESULTS / "raw_upper_middle.png",
    RESULTS / "raw_lower_middle.png",
    RESULTS / "raw_bottom.png",
    RESULTS / "raw_left_core.png",
    RESULTS / "raw_center_core.png",
    RESULTS / "raw_right_core.png",
    RESULTS / "raw_title_notes_area.png",
]

MAIN_VIEWED_IMAGES = [
    RESULTS / "raw_full_preview.png",
    RESULTS / "overlay_full_preview.png",
]


def subagent_image_bundle() -> list[Path]:
    return [RAW, OVERLAY] + sorted(RESULTS.glob("*.png"))


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def node_id(node: Any) -> str:
    if isinstance(node, dict):
        return str(node.get("id", "")).strip()
    return str(node).strip()


def edge_pair(edge: dict[str, Any]) -> tuple[str, str]:
    source = str(edge.get("source", "")).strip()
    target = str(edge.get("target", "")).strip()
    if not source or not target:
        raise ValueError(f"edge missing endpoint: {edge}")
    return tuple(sorted((source, target)))


def validate_matrix(path: Path, node_order: list[str], asserted_edges: list[dict[str, Any]]) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError("empty matrix")
    header = rows[0][1:]
    row_ids = [row[0] for row in rows[1:]]
    if header != node_order or row_ids != node_order:
        raise ValueError("matrix node order does not match final node order")
    values = [[int(cell) for cell in row[1:]] for row in rows[1:]]
    n = len(node_order)
    if len(values) != n or any(len(row) != n for row in values):
        raise ValueError("matrix dimensions do not match node count")
    binary = all(cell in (0, 1) for row in values for cell in row)
    symmetric = all(values[i][j] == values[j][i] for i in range(n) for j in range(n))
    diagonal_zero = all(values[i][i] == 0 for i in range(n))
    matrix_edges = sum(sum(row) for row in values) // 2
    if matrix_edges != len(asserted_edges):
        raise ValueError(f"matrix edge count {matrix_edges} != asserted {len(asserted_edges)}")
    asserted_pairs = {edge_pair(edge) for edge in asserted_edges}
    matrix_pairs = {
        tuple(sorted((node_order[i], node_order[j])))
        for i in range(n)
        for j in range(i + 1, n)
        if values[i][j] == 1
    }
    if matrix_pairs != asserted_pairs:
        missing = sorted(asserted_pairs - matrix_pairs)[:10]
        extra = sorted(matrix_pairs - asserted_pairs)[:10]
        raise ValueError(f"matrix/JSON edge mismatch missing={missing} extra={extra}")
    return {
        "node_count": n,
        "asserted_edge_count": len(asserted_edges),
        "matrix_rows": len(values),
        "matrix_columns": len(values[0]) if values else 0,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "binary": binary,
    }


def normalize_row(row: Any, default_status: str = "") -> dict[str, Any]:
    if isinstance(row, dict):
        out = {k: row.get(k, "") for k in sorted(row.keys())}
    else:
        out = {"value": str(row)}
    if default_status and "status" not in out:
        out["status"] = default_status
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], preferred: list[str]) -> None:
    keys: list[str] = []
    for key in preferred:
        if any(key in row for row in rows):
            keys.append(key)
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in keys})


def text_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    return math.ceil(len(path.read_text(encoding="utf-8", errors="ignore")) / 4)


def image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    with Image.open(path) as im:
        w, h = im.size
    scale = min(2048 / max(w, h), 1.0)
    w = math.ceil(w * scale)
    h = math.ceil(h * scale)
    scale = 768 / min(w, h)
    w = math.ceil(w * scale)
    h = math.ceil(h * scale)
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def image_bundle_tokens(paths: list[Path]) -> int:
    return sum(image_tokens(path) for path in paths)


def token_row(
    call: str,
    input_tokens: int,
    image_tokens_est: int,
    output_tokens: int,
    reasoning_tokens: int,
    notes: str,
) -> dict[str, Any]:
    expected = input_tokens + image_tokens_est + output_tokens + reasoning_tokens
    low = input_tokens + image_tokens_est + math.ceil(output_tokens * 0.6) + math.ceil(reasoning_tokens * 0.6)
    high = input_tokens + image_tokens_est + math.ceil(output_tokens * 1.6) + math.ceil(reasoning_tokens * 2.0)
    return {
        "document": DOC,
        "iteration": ITERATION,
        "call": call,
        "input_tokens_est": input_tokens,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": image_tokens_est,
        "output_tokens_expected": output_tokens,
        "reasoning_tokens_expected": reasoning_tokens,
        "total_low": low,
        "total_expected": expected,
        "total_high": high,
        "usage_object_available": "no",
        "notes": notes,
    }


def write_token_usage() -> list[dict[str, Any]]:
    diego_r1_out = text_tokens(WORK_RESULTS / "doc36_round1_diego_connectivity_proposal.json") + text_tokens(
        WORK_RESULTS / "doc36_round1_diego_connectivity_matrix.csv"
    )
    jennifer_r1_out = text_tokens(WORK_RESULTS / "doc36_round1_jennifer_review.json") + text_tokens(
        WORK_RESULTS / "doc36_round1_jennifer_connectivity_matrix.csv"
    )
    diego_r2_out = text_tokens(WORK_RESULTS / "doc36_round2_diego_connectivity_proposal.json") + text_tokens(
        WORK_RESULTS / "doc36_round2_diego_connectivity_matrix.csv"
    )
    jennifer_r2_out = (
        text_tokens(WORK_RESULTS / "doc36_round2_jennifer_final_nodes.json")
        + text_tokens(WORK_RESULTS / "doc36_round2_jennifer_final_edges.json")
        + text_tokens(WORK_RESULTS / "doc36_round2_jennifer_final_matrix.csv")
    )
    full_bundle = image_bundle_tokens(subagent_image_bundle())
    final_bundle = image_bundle_tokens(FINAL_JENNIFER_IMAGE_BUNDLE)
    main_images = image_bundle_tokens(MAIN_VIEWED_IMAGES)

    rows = [
        token_row(
            "Main Codex: grouped orchestration, visual triage, prompts, packaging",
            30000,
            main_images,
            2200,
            22000,
            "Grouped main-agent model turns; exact usage was not exposed.",
        ),
        token_row(
            "Diego: round1_high_recall_extraction",
            9500,
            full_bundle,
            diego_r1_out,
            40000,
            "Initial Diego prompt plus Doc36 full raw/overlay and generated crop bundle.",
        ),
        token_row(
            "Jennifer: round1_precision_review",
            5400 + diego_r1_out,
            full_bundle,
            jennifer_r1_out,
            36000,
            "Jennifer prompt plus Diego round 1 artifacts and the same image bundle.",
        ),
        token_row(
            "Diego: round2_saturation_review",
            4800 + jennifer_r1_out + text_tokens(WORK_RESULTS / "doc36_round1_diego_connectivity_proposal.json"),
            0,
            diego_r2_out,
            10500,
            "Diego round 2 used prior visual context and Jennifer round 1 artifacts.",
        ),
        token_row(
            "Jennifer: round2_final_precision_confirmation",
            5400 + diego_r2_out + text_tokens(WORK_RESULTS / "doc36_round1_jennifer_review.json"),
            final_bundle,
            jennifer_r2_out,
            14500,
            "Final Jennifer prompt plus Diego round 2 artifacts, Jennifer round 1 artifacts, and a smaller final image bundle.",
        ),
    ]
    totals = {
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
        "notes": "Total over estimated visible workflow calls.",
    }
    rows.append(totals)

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Document 36 Token Usage Estimate\n\n")
        f.write(
            "No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. "
            "The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. "
            "Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, "
            "then short side 768px, then `85 + 170 * 512px_tiles`.\n\n"
        )
        f.write("| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |\n")
        f.write("|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            call = f"**{row['call']}**" if row["call"] == "TOTAL" else row["call"]
            f.write(
                f"| {row['document']} | {row['iteration']} | {call} | {row['input_tokens_est']} | "
                f"{row['cached_input_tokens']} | {row['image_file_input_tokens_est']} | {row['output_tokens_expected']} | "
                f"{row['reasoning_tokens_expected']} | {row['total_low']} | {row['total_expected']} | {row['total_high']} |\n"
            )
    return rows


def round_counts(path: Path) -> dict[str, int]:
    doc = load_json(path)
    return {
        "nodes": len(doc.get("nodes", [])),
        "asserted_edges": len(doc.get("asserted_edges", [])),
        "uncertain_edges": len(doc.get("uncertain_edges", [])),
        "removed_edges": len(doc.get("removed_edges", [])),
        "added_edges": len(doc.get("added_edges", [])),
        "label_corrections": len(doc.get("label_corrections", [])),
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)

    nodes_doc = load_json(FINAL_NODES_FILE)
    edges_doc = load_json(FINAL_EDGES_FILE)
    nodes = nodes_doc.get("nodes", edges_doc.get("nodes", []))
    ids = [node_id(node) for node in nodes]
    if len(ids) != len(set(ids)):
        duplicates = sorted({node for node in ids if ids.count(node) > 1})
        raise ValueError(f"duplicate node IDs: {duplicates[:10]}")

    asserted = edges_doc.get("asserted_edges", [])
    uncertain = [normalize_row(row) for row in edges_doc.get("uncertain_edges", [])]
    removed = [normalize_row(row) for row in edges_doc.get("removed_edges", [])]
    added = [normalize_row(row) for row in edges_doc.get("added_edges", [])]
    corrections = [normalize_row(row) for row in edges_doc.get("label_corrections", [])]
    rejected = [normalize_row(row) for row in edges_doc.get("rejected_non_edges", [])]
    validation = validate_matrix(FINAL_MATRIX_FILE, ids, asserted)

    (RESULTS / "final_nodes.json").write_text(
        json.dumps(
            {
                "document": DOC,
                "iteration": ITERATION,
                "final_status": nodes_doc.get("final_status", edges_doc.get("final_status", "saturation_agreement")),
                "nodes": nodes,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    shutil.copyfile(FINAL_EDGES_FILE, RESULTS / "final_edges.json")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "final_connectivity_matrix.csv")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "final_matrix.csv")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "connectivity_matrix.csv")

    write_csv(RESULTS / "final_edges.csv", asserted, ["source", "target", "kind", "confidence", "evidence"])
    write_csv(RESULTS / "final_uncertain_edges.csv", uncertain, ["source", "target", "status", "reason", "evidence"])
    write_csv(RESULTS / "final_removed_edges.csv", removed, ["source", "target", "status", "reason", "evidence"])
    write_csv(RESULTS / "final_added_edges.csv", added, ["source", "target", "kind", "confidence", "evidence", "reason"])
    write_csv(RESULTS / "final_label_corrections.csv", corrections, ["from", "to", "evidence", "reason"])
    write_csv(RESULTS / "final_rejected_non_edges.csv", rejected, ["source", "target", "reason", "evidence"])

    for filename in ROUND_FILES:
        source = WORK_RESULTS / filename
        if source.exists():
            shutil.copyfile(source, RESULTS / filename)
            alias = ROUND_MATRIX_ALIASES.get(filename)
            if alias:
                shutil.copyfile(source, RESULTS / alias)

    diego_r1 = round_counts(WORK_RESULTS / "doc36_round1_diego_connectivity_proposal.json")
    jennifer_r1 = round_counts(WORK_RESULTS / "doc36_round1_jennifer_review.json")
    diego_r2 = round_counts(WORK_RESULTS / "doc36_round2_diego_connectivity_proposal.json")
    j1_doc = load_json(WORK_RESULTS / "doc36_round1_jennifer_review.json")
    round1_removed = [normalize_row(row, "removed_by_jennifer_round1") for row in j1_doc.get("removed_edges", [])]
    write_csv(RESULTS / "jennifer_round1_removed_edges.csv", round1_removed, ["source", "target", "status", "reason", "evidence"])

    with (RESULTS / "round_summaries.md").open("w", encoding="utf-8") as f:
        f.write("# Document 36 Round Summaries\n\n")
        f.write(f"- Diego round 1: {diego_r1['nodes']} nodes, {diego_r1['asserted_edges']} asserted edges, {diego_r1['uncertain_edges']} uncertain edges.\n")
        f.write(
            f"- Jennifer round 1: {jennifer_r1['nodes']} nodes, {jennifer_r1['asserted_edges']} asserted edges, "
            f"{jennifer_r1['added_edges']} additions, {jennifer_r1['removed_edges']} removals, "
            f"{jennifer_r1['label_corrections']} label corrections, {jennifer_r1['uncertain_edges']} uncertain edges.\n"
        )
        f.write(f"- Diego round 2: {diego_r2['nodes']} nodes, {diego_r2['asserted_edges']} asserted edges.\n")
        f.write(f"- Jennifer final round 2: {len(ids)} nodes, {len(asserted)} asserted edges, {len(uncertain)} uncertain candidates kept out of the matrix.\n\n")
        f.write(
            "Final consensus: saturated agreement after Diego -> Jennifer -> Diego -> Jennifer. "
            "The final matrix asserts only visually supported adjacencies from the allowed raw schematic and Raw+components overlay/crops.\n"
        )

    token_rows = write_token_usage()
    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "source_restriction": "Doc36 Raw + components only; no GT, no GT-derived feedback, no Raw+wires, no OCR engines, no web",
        "final_status": nodes_doc.get("final_status", edges_doc.get("final_status", "saturation_agreement")),
        "validation": validation,
        "uncertain_edge_count": len(uncertain),
        "removed_edge_count": len(removed),
        "added_edge_count": len(added),
        "label_correction_count": len(corrections),
        "rejected_non_edge_count": len(rejected),
        "round1_removed_edge_count": len(round1_removed),
        "token_estimate_totals": token_rows[-1],
    }
    (RESULTS / "final_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
