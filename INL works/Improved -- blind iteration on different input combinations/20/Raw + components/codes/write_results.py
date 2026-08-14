from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path
from typing import Any

from PIL import Image


DOC = "20"
ITERATION = "1"
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + components"
)
CODES = ROOT / "codes"
RESULTS = ROOT / "results"
WORK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\results")

FINAL_NODES_FILE = WORK_RESULTS / "doc20_round2_jennifer_final_nodes.json"
FINAL_EDGES_FILE = WORK_RESULTS / "doc20_round2_jennifer_final_edges.json"
FINAL_MATRIX_FILE = WORK_RESULTS / "doc20_round2_jennifer_final_matrix.csv"

ROUND_FILES = [
    "doc20_round1_diego_connectivity_proposal.json",
    "doc20_round1_diego_connectivity_matrix.csv",
    "doc20_round1_jennifer_review.json",
    "doc20_round1_jennifer_connectivity_matrix.csv",
    "doc20_round2_diego_connectivity_proposal.json",
    "doc20_round2_diego_connectivity_matrix.csv",
    "doc20_round2_jennifer_final_nodes.json",
    "doc20_round2_jennifer_final_edges.json",
    "doc20_round2_jennifer_final_matrix.csv",
]

ROUND_MATRIX_ALIASES = {
    "doc20_round1_diego_connectivity_matrix.csv": "diego_round1_connectivity_matrix.csv",
    "doc20_round1_jennifer_connectivity_matrix.csv": "jennifer_round1_connectivity_matrix.csv",
    "doc20_round2_diego_connectivity_matrix.csv": "diego_round2_connectivity_matrix.csv",
    "doc20_round2_jennifer_final_matrix.csv": "jennifer_round2_final_connectivity_matrix.csv",
}

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"

SUBAGENT_IMAGE_BUNDLE = [
    RAW,
    OVERLAY,
    RESULTS / "raw_01_top_13kv_4160_full.png",
    RESULTS / "raw_05_480_load_centers_full.png",
    RESULTS / "raw_10_bottom_dc_control_full.png",
    RESULTS / "raw_13_notes_legend.png",
    RESULTS / "raw_16_close_a_source_chain_2x.png",
    RESULTS / "raw_17_close_a_4160_to_480_2x.png",
    RESULTS / "raw_18_close_mid_13kv_4160_ties_2x.png",
    RESULTS / "raw_19_close_b_source_chain_2x.png",
    RESULTS / "raw_20_close_480_tie_2x.png",
    RESULTS / "raw_21_close_loads_a1_2x.png",
    RESULTS / "raw_22_close_loads_a2_2x.png",
    RESULTS / "raw_23_close_loads_c_2x.png",
    RESULTS / "raw_24_close_loads_d_2x.png",
    RESULTS / "raw_25_close_dc_a_left_2x.png",
    RESULTS / "raw_26_close_dc_a_right_2x.png",
    RESULTS / "raw_27_close_dc_b_left_2x.png",
    RESULTS / "raw_28_close_dc_b_right_2x.png",
]

MAIN_VIEWED_IMAGES = [
    RAW,
    OVERLAY,
    RESULTS / "raw_01_top_13kv_4160_full.png",
    RESULTS / "raw_05_480_load_centers_full.png",
    RESULTS / "raw_10_bottom_dc_control_full.png",
    RESULTS / "raw_13_notes_legend.png",
    RESULTS / "raw_25_close_dc_a_left_2x.png",
    RESULTS / "raw_26_close_dc_a_right_2x.png",
    RESULTS / "raw_27_close_dc_b_left_2x.png",
    RESULTS / "raw_28_close_dc_b_right_2x.png",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def node_ids(nodes_doc: dict[str, Any]) -> list[str]:
    if "matrix_order" in nodes_doc:
        return list(nodes_doc["matrix_order"])
    nodes = nodes_doc.get("nodes", [])
    if nodes and isinstance(nodes[0], dict):
        return [str(row["id"]) for row in nodes]
    return [str(row) for row in nodes]


def edge_ends(edge: dict[str, Any]) -> tuple[str, str]:
    a = edge.get("source", edge.get("a"))
    b = edge.get("target", edge.get("b"))
    if not a or not b:
        raise ValueError(f"edge missing endpoints: {edge}")
    return str(a), str(b)


def edge_key(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop not expected: {a}")
    return tuple(sorted((a, b)))


def normalize_row(row: dict[str, Any], status: str | None = None) -> dict[str, Any]:
    source, target = edge_ends(row)
    out = dict(row)
    out["source"] = source
    out["target"] = target
    if status is not None:
        out["status"] = status
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
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

    matrix_edges = set()
    for i, a in enumerate(nodes):
        for j in range(i + 1, n):
            if values[i][j] == 1:
                matrix_edges.add(edge_key(a, nodes[j]))
    json_edges = {edge_key(*edge_ends(edge)) for edge in edges}
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
    if not path.exists():
        return 0
    return math.ceil(len(path.read_text(encoding="utf-8", errors="ignore")) / 4)


def image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
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
    return sum(image_tokens(path) for path in paths)


def call_row(
    call: str,
    input_tokens: int,
    image_tokens_est: int,
    output_tokens: int,
    reasoning_tokens: int,
    notes: str,
) -> dict[str, Any]:
    expected = input_tokens + image_tokens_est + output_tokens + reasoning_tokens
    low = input_tokens + image_tokens_est + math.ceil(output_tokens * 0.6) + math.ceil(reasoning_tokens * 0.4)
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
    diego_r1_out = text_tokens(WORK_RESULTS / "doc20_round1_diego_connectivity_proposal.json") + text_tokens(
        WORK_RESULTS / "doc20_round1_diego_connectivity_matrix.csv"
    )
    jennifer_r1_out = text_tokens(WORK_RESULTS / "doc20_round1_jennifer_review.json") + text_tokens(
        WORK_RESULTS / "doc20_round1_jennifer_connectivity_matrix.csv"
    )
    diego_r2_out = text_tokens(WORK_RESULTS / "doc20_round2_diego_connectivity_proposal.json") + text_tokens(
        WORK_RESULTS / "doc20_round2_diego_connectivity_matrix.csv"
    )
    jennifer_r2_out = (
        text_tokens(WORK_RESULTS / "doc20_round2_jennifer_final_nodes.json")
        + text_tokens(WORK_RESULTS / "doc20_round2_jennifer_final_edges.json")
        + text_tokens(WORK_RESULTS / "doc20_round2_jennifer_final_matrix.csv")
    )

    image_bundle = image_bundle_tokens(SUBAGENT_IMAGE_BUNDLE)
    main_images = image_bundle_tokens(MAIN_VIEWED_IMAGES)
    rows = [
        call_row(
            "Main Codex: orchestration_visual_review_packaging",
            26000,
            main_images,
            1600,
            22000,
            "Grouped main-agent calls; exact per-response usage unavailable in this environment.",
        ),
        call_row(
            "Diego: round1_high_recall_extraction",
            6200,
            image_bundle,
            diego_r1_out,
            34000,
            "Initial prompt plus 19 Doc20 Raw+components images.",
        ),
        call_row(
            "Jennifer: round1_precision_review",
            7200 + diego_r1_out,
            image_bundle,
            jennifer_r1_out,
            32000,
            "Review prompt plus Diego round 1 artifacts and the same 19-image bundle.",
        ),
        call_row(
            "Diego: round2_saturation_review",
            3600 + jennifer_r1_out + text_tokens(WORK_RESULTS / "doc20_round1_diego_connectivity_proposal.json"),
            0,
            diego_r2_out,
            9000,
            "No new images were explicitly attached; prior visual context/caching was not exposed.",
        ),
        call_row(
            "Jennifer: round2_final_confirmation",
            3200 + diego_r2_out + text_tokens(WORK_RESULTS / "doc20_round1_jennifer_review.json"),
            0,
            jennifer_r2_out,
            8000,
            "No new images were explicitly attached; final confirmation used previous visual context and files.",
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
        "notes": "Total over estimated workflow calls.",
    }
    all_rows = rows + [total]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Document 20 Token Usage Estimate\n\n")
        f.write(
            "No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. "
            "The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. "
            "Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: "
            "downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.\n\n"
        )
        f.write(
            "| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |\n"
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


def round_counts(path: Path) -> dict[str, int]:
    if not path.exists():
        return {"nodes": 0, "asserted_edges": 0, "uncertain_edges": 0}
    data = load_json(path)
    return {
        "nodes": len(data.get("matrix_order", data.get("nodes", []))),
        "asserted_edges": len(data.get("asserted_edges", [])),
        "uncertain_edges": len(data.get("uncertain_edges", [])),
        "removed_edges": len(data.get("removed_edges", [])),
        "added_edges": len(data.get("added_edges", [])),
        "label_corrections": len(data.get("label_corrections", [])),
    }


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    nodes_doc = load_json(FINAL_NODES_FILE)
    edges_doc = load_json(FINAL_EDGES_FILE)
    ids = node_ids(nodes_doc)
    node_objects = list(nodes_doc.get("nodes", ids))
    asserted = [normalize_row(row) for row in edges_doc["asserted_edges"]]
    uncertain = [normalize_row(row, "uncertain_not_asserted") for row in edges_doc.get("uncertain_edges", [])]
    removed = [normalize_row(row, "removed") for row in edges_doc.get("removed_edges", [])]
    added = [normalize_row(row, "added") for row in edges_doc.get("added_edges", [])]
    corrections = list(edges_doc.get("label_corrections", []))
    rejected_non_edges = [
        normalize_row(row, "rejected_non_edge") for row in edges_doc.get("rejected_non_edges", [])
    ]

    validation = validate_matrix(FINAL_MATRIX_FILE, ids, asserted)

    (RESULTS / "final_nodes.json").write_text(
        json.dumps(
            {
                "document": DOC,
                "iteration": ITERATION,
                "node_count": len(ids),
                "matrix_order": ids,
                "nodes": node_objects,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    shutil.copyfile(FINAL_EDGES_FILE, RESULTS / "final_edges.json")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "final_connectivity_matrix.csv")
    shutil.copyfile(FINAL_MATRIX_FILE, RESULTS / "final_matrix.csv")

    write_csv(RESULTS / "final_edges.csv", asserted, ["source", "target", "kind", "confidence", "evidence"])
    write_csv(RESULTS / "final_uncertain_edges.csv", uncertain, ["source", "target", "status", "reason", "evidence"])
    write_csv(RESULTS / "final_removed_edges.csv", removed, ["source", "target", "status", "reason", "evidence"])
    write_csv(RESULTS / "final_added_edges.csv", added, ["source", "target", "status", "kind", "confidence", "evidence", "reason"])
    write_csv(RESULTS / "final_label_corrections.csv", corrections, ["from", "to", "evidence", "reason"])
    write_csv(
        RESULTS / "final_rejected_non_edges.csv",
        uncertain + removed + rejected_non_edges,
        ["source", "target", "status", "reason", "evidence"],
    )

    for filename in ROUND_FILES:
        src = WORK_RESULTS / filename
        if src.exists():
            shutil.copyfile(src, RESULTS / filename)
        alias = ROUND_MATRIX_ALIASES.get(filename)
        if alias and src.exists():
            shutil.copyfile(src, RESULTS / alias)

    diego_r1 = round_counts(WORK_RESULTS / "doc20_round1_diego_connectivity_proposal.json")
    jennifer_r1 = round_counts(WORK_RESULTS / "doc20_round1_jennifer_review.json")
    diego_r2 = round_counts(WORK_RESULTS / "doc20_round2_diego_connectivity_proposal.json")
    with (RESULTS / "round_summaries.md").open("w", encoding="utf-8") as f:
        f.write("# Document 20 Round Summaries\n\n")
        f.write(
            f"- Diego round 1: {diego_r1['nodes']} nodes, {diego_r1['asserted_edges']} asserted edges, "
            f"{diego_r1['uncertain_edges']} uncertain edges.\n"
        )
        f.write(
            f"- Jennifer round 1: {jennifer_r1['nodes']} nodes, {jennifer_r1['asserted_edges']} asserted edges, "
            f"{jennifer_r1['added_edges']} additions, {jennifer_r1['removed_edges']} removals, "
            f"{jennifer_r1['label_corrections']} label corrections, {jennifer_r1['uncertain_edges']} uncertain edges.\n"
        )
        f.write(
            f"- Diego round 2: {diego_r2['nodes']} nodes, {diego_r2['asserted_edges']} asserted edges; "
            "agreed with Jennifer's precision review and kept the matrix unchanged.\n"
        )
        f.write(
            f"- Jennifer final round 2: {len(ids)} nodes, {len(asserted)} asserted edges, "
            f"{len(uncertain)} uncertain candidates kept out of the matrix.\n\n"
        )
        f.write(
            "Final consensus: saturated agreement after Diego -> Jennifer -> Diego -> Jennifer. "
            "No asserted edge was added or removed in the final review, and no label correction was needed.\n\n"
        )
        f.write(
            "Key precision decisions: the 480 VAC B/C tie is represented through CB-TIE-480, DC chargers are not "
            "shortcut-connected directly to the 125 VDC buses, and the long A/B ESF interlock remains asserted only "
            "between the visually supported relay endpoints.\n"
        )

    token_rows = write_token_usage()
    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "source_restriction": "Doc20 Raw + components only; no GT, no GT-derived feedback, no Raw+wires, no OCR engines, no web",
        "final_status": nodes_doc.get("final_status", "agreed_saturated"),
        "validation": validation,
        "uncertain_edge_count": len(uncertain),
        "removed_edge_count": len(removed),
        "added_edge_count": len(added),
        "label_correction_count": len(corrections),
        "rejected_non_edge_count": len(rejected_non_edges),
        "token_estimate_totals": token_rows[-1],
    }
    (RESULTS / "final_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
