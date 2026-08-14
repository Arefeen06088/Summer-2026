import csv
import json
import math
import shutil
import struct
from datetime import datetime, timezone
from pathlib import Path


DOC = "13"
ITERATION = "1"

WORK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\results")
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + components"
)
CODES_DIR = BASE / "codes"
RESULTS_DIR = BASE / "results"
RAW_IMAGE = BASE / "raw -- synthetic diagram _.png"
OVERLAY_IMAGE = BASE / "detected_components_and_logical_overlay.png"

ROUND_FILES = {
    "diego_round1": {
        "json": WORK_RESULTS / "doc13_round1_diego_connectivity_proposal.json",
        "matrix": WORK_RESULTS / "doc13_round1_diego_connectivity_matrix.csv",
    },
    "jennifer_round1": {
        "nodes": WORK_RESULTS / "doc13_round1_jennifer_nodes.json",
        "json": WORK_RESULTS / "doc13_round1_jennifer_edges.json",
        "matrix": WORK_RESULTS / "doc13_round1_jennifer_matrix.csv",
    },
    "diego_round2": {
        "json": WORK_RESULTS / "doc13_round2_diego_connectivity_proposal.json",
        "matrix": WORK_RESULTS / "doc13_round2_diego_connectivity_matrix.csv",
    },
    "jennifer_round2_final": {
        "nodes": WORK_RESULTS / "doc13_round2_jennifer_final_nodes.json",
        "json": WORK_RESULTS / "doc13_round2_jennifer_final_edges.json",
        "matrix": WORK_RESULTS / "doc13_round2_jennifer_final_matrix.csv",
    },
}

DIEGO_IMAGES = [
    RAW_IMAGE,
    OVERLAY_IMAGE,
    RESULTS_DIR / "raw_01_left_schematic_full.png",
    RESULTS_DIR / "raw_02_top_sources_and_4160_buses.png",
    RESULTS_DIR / "raw_03_train_a_full_2x.png",
    RESULTS_DIR / "raw_04_train_b_full_2x.png",
    RESULTS_DIR / "raw_05_train_c_full_2x.png",
    RESULTS_DIR / "raw_06_train_d_full_2x.png",
    RESULTS_DIR / "raw_07_train_a_loads_dc_zoom_2x.png",
    RESULTS_DIR / "raw_08_train_b_loads_dc_zoom_2x.png",
    RESULTS_DIR / "raw_09_train_c_loads_dc_zoom_2x.png",
    RESULTS_DIR / "raw_10_train_d_loads_dc_zoom_2x.png",
    RESULTS_DIR / "raw_11_startup_switchyard_feed_2x.png",
    RESULTS_DIR / "raw_16_common_ground_and_cross_ties.png",
    RESULTS_DIR / "raw_17_notes_legend_schedule.png",
]

JENNIFER_IMAGES = DIEGO_IMAGES + [
    RESULTS_DIR / "raw_12_train_a_source_detail_2x.png",
    RESULTS_DIR / "raw_13_train_b_source_detail_2x.png",
    RESULTS_DIR / "raw_14_train_c_source_detail_2x.png",
    RESULTS_DIR / "raw_15_train_d_source_detail_2x.png",
]

MAIN_VIEWED_IMAGES = JENNIFER_IMAGES


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)


def edge_parts(edge):
    if isinstance(edge, dict):
        return (
            edge.get("node_a") or edge.get("a") or edge.get("source") or edge.get("from"),
            edge.get("node_b") or edge.get("b") or edge.get("target") or edge.get("to"),
            edge.get("evidence") or edge.get("reason") or "",
            edge.get("why_uncertain") or edge.get("notes") or "",
        )
    return (
        edge[0],
        edge[1],
        edge[2] if len(edge) > 2 else "",
        edge[3] if len(edge) > 3 else "",
    )


def build_matrix(nodes, edges):
    idx = {node: i for i, node in enumerate(nodes)}
    if len(idx) != len(nodes):
        raise ValueError("Duplicate node in node_order")
    matrix = [[0] * len(nodes) for _ in nodes]
    pairs = set()
    for edge in edges:
        a, b, _evidence, _extra = edge_parts(edge)
        if a not in idx or b not in idx:
            raise ValueError(f"Unknown edge endpoint: {a!r}, {b!r}")
        if a == b:
            raise ValueError(f"Unexpected self-loop: {a!r}")
        i, j = idx[a], idx[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
        pairs.add(tuple(sorted((a, b))))
    return matrix, pairs


def validate_matrix(nodes, matrix, expected_edges):
    n = len(nodes)
    if len(matrix) != n:
        raise ValueError("Matrix row count mismatch")
    ones = 0
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise ValueError("Matrix column count mismatch")
        if row[i] != 0:
            raise ValueError("Matrix diagonal is not zero")
        for j, value in enumerate(row):
            if value not in (0, 1):
                raise ValueError("Matrix is not binary")
            if value != matrix[j][i]:
                raise ValueError("Matrix is not symmetric")
            ones += value
    edge_count = ones // 2
    if edge_count != expected_edges:
        raise ValueError(f"Matrix edge count {edge_count} != expected {expected_edges}")
    return {
        "node_count": n,
        "asserted_edge_count": edge_count,
        "symmetric": True,
        "diagonal_zero": True,
        "binary": True,
    }


def matrix_rows(nodes, matrix):
    return [[""] + nodes] + [[node] + row for node, row in zip(nodes, matrix)]


def edge_rows(edges, include_uncertain_reason=False):
    header = ["node_a", "node_b", "evidence"]
    if include_uncertain_reason:
        header.append("why_uncertain")
    rows = [header]
    for edge in edges:
        a, b, evidence, extra = edge_parts(edge)
        row = [a, b, evidence]
        if include_uncertain_reason:
            row.append(extra)
        rows.append(row)
    return rows


def png_dimensions(path):
    with path.open("rb") as f:
        data = f.read(24)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def text_tokens(chars):
    return max(1, math.ceil(chars / 4))


def file_tokens(path):
    if not path.exists():
        return 0
    try:
        return text_tokens(len(path.read_text(encoding="utf-8")))
    except UnicodeDecodeError:
        return 0


def image_tokens(path):
    if not path.exists():
        return 0
    dims = png_dimensions(path)
    if not dims:
        return 0
    width, height = dims
    w, h = float(width), float(height)
    if max(w, h) > 2048:
        scale = 2048 / max(w, h)
        w *= scale
        h *= scale
    if min(w, h) > 768:
        scale = 768 / min(w, h)
        w *= scale
        h *= scale
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def images_tokens(paths):
    return sum(image_tokens(path) for path in paths if path.exists())


def copy_round_files():
    copied = []
    for round_name, files in ROUND_FILES.items():
        for kind, src in files.items():
            if not src.exists():
                raise FileNotFoundError(src)
            suffix = "connectivity_matrix.csv" if kind == "matrix" else f"{kind}.json"
            if kind == "json":
                suffix = "edges.json"
            dst = RESULTS_DIR / f"{round_name}_{suffix}"
            shutil.copy2(src, dst)
            copied.append(str(dst))
    return copied


def token_usage_rows():
    calls = [
        {
            "round": "main",
            "agent": "Main Codex",
            "model_call": "main_orchestration_grouped",
            "model": "Codex session model",
            "text": 1400,
            "images": MAIN_VIEWED_IMAGES,
            "file_inputs": [],
            "output_files": [],
            "output_expected": 900,
            "reasoning": (5000, 18000, 45000),
            "notes": "Grouped main-agent model calls; exact internal call count and usage objects are not exposed.",
        },
        {
            "round": "1",
            "agent": "Diego",
            "model_call": "diego_round1_high_recall_extraction",
            "model": "gpt-5.5 xhigh",
            "text": 720,
            "images": DIEGO_IMAGES,
            "file_inputs": [],
            "output_files": [ROUND_FILES["diego_round1"]["json"], ROUND_FILES["diego_round1"]["matrix"]],
            "reasoning": (10000, 30000, 75000),
            "notes": "Spawned Diego with raw image, overlay, and focused Doc 13 crops.",
        },
        {
            "round": "1",
            "agent": "Jennifer",
            "model_call": "jennifer_round1_precision_review",
            "model": "gpt-5.5 xhigh",
            "text": 720,
            "images": JENNIFER_IMAGES,
            "file_inputs": [ROUND_FILES["diego_round1"]["json"]],
            "output_files": [
                ROUND_FILES["jennifer_round1"]["nodes"],
                ROUND_FILES["jennifer_round1"]["json"],
                ROUND_FILES["jennifer_round1"]["matrix"],
            ],
            "reasoning": (10000, 28000, 70000),
            "notes": "Spawned Jennifer with Diego round-1 proposal plus raw/overlay/crops.",
        },
        {
            "round": "2",
            "agent": "Diego",
            "model_call": "diego_round2_saturation_review",
            "model": "gpt-5.5 xhigh",
            "text": 360,
            "images": [],
            "file_inputs": [
                ROUND_FILES["jennifer_round1"]["nodes"],
                ROUND_FILES["jennifer_round1"]["json"],
                ROUND_FILES["jennifer_round1"]["matrix"],
            ],
            "output_files": [ROUND_FILES["diego_round2"]["json"], ROUND_FILES["diego_round2"]["matrix"]],
            "reasoning": (2000, 8000, 20000),
            "notes": "Sent to existing Diego thread; previous image context/caching is not exposed.",
        },
        {
            "round": "2",
            "agent": "Jennifer",
            "model_call": "jennifer_round2_final_confirmation",
            "model": "gpt-5.5 xhigh",
            "text": 340,
            "images": [],
            "file_inputs": [ROUND_FILES["diego_round2"]["json"], ROUND_FILES["diego_round2"]["matrix"]],
            "output_files": [
                ROUND_FILES["jennifer_round2_final"]["nodes"],
                ROUND_FILES["jennifer_round2_final"]["json"],
                ROUND_FILES["jennifer_round2_final"]["matrix"],
            ],
            "reasoning": (2000, 6000, 16000),
            "notes": "Sent to existing Jennifer thread for final saturation confirmation.",
        },
    ]

    rows = []
    for call in calls:
        input_file = sum(file_tokens(path) for path in call["file_inputs"])
        input_image = images_tokens(call["images"])
        input_total = call["text"] + input_file + input_image
        output_expected = call.get("output_expected") or sum(file_tokens(path) for path in call["output_files"])
        output_low = math.ceil(output_expected * 0.75)
        output_high = math.ceil(output_expected * 1.25)
        reasoning_low, reasoning_expected, reasoning_high = call["reasoning"]
        rows.append(
            {
                "document": DOC,
                "iteration": ITERATION,
                "round": call["round"],
                "agent": call["agent"],
                "model_call": call["model_call"],
                "model": call["model"],
                "input_text_tokens_est": call["text"],
                "cached_input_tokens_recorded": "unavailable",
                "input_file_tokens_est": input_file,
                "input_image_tokens_est": input_image,
                "total_input_tokens_est": input_total,
                "output_tokens_recorded": "unavailable",
                "output_tokens_est_low": output_low,
                "output_tokens_est_expected": output_expected,
                "output_tokens_est_high": output_high,
                "reasoning_tokens_recorded": "unavailable",
                "reasoning_tokens_est_low": reasoning_low,
                "reasoning_tokens_est_expected": reasoning_expected,
                "reasoning_tokens_est_high": reasoning_high,
                "total_tokens_low": input_total + output_low + reasoning_low,
                "total_tokens_expected": input_total + output_expected + reasoning_expected,
                "total_tokens_high": input_total + output_high + reasoning_high,
                "usage_source": "local estimate; Responses count endpoint unavailable; subagent tool usage object unavailable",
                "notes": call["notes"],
            }
        )
    return rows


def write_token_usage(rows):
    headers = list(rows[0].keys())
    write_csv(RESULTS_DIR / "token_usage_estimate.csv", [headers] + [[row[h] for h in headers] for row in rows])
    totals = {
        "total_input_tokens_expected": sum(row["total_input_tokens_est"] for row in rows),
        "total_image_tokens_expected": sum(row["input_image_tokens_est"] for row in rows),
        "total_output_tokens_expected": sum(row["output_tokens_est_expected"] for row in rows),
        "total_reasoning_tokens_expected": sum(row["reasoning_tokens_est_expected"] for row in rows),
        "total_tokens_low": sum(row["total_tokens_low"] for row in rows),
        "total_tokens_expected": sum(row["total_tokens_expected"] for row in rows),
        "total_tokens_high": sum(row["total_tokens_high"] for row in rows),
    }

    lines = [
        "# Document 13 Token Usage Estimate",
        "",
        "No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.",
        "",
        "| Document | Iteration | Call | Input est | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['document']} | {row['iteration']} | {row['agent']}: {row['model_call']} | {row['total_input_tokens_est']} | {row['input_image_tokens_est']} | {row['output_tokens_est_expected']} | {row['reasoning_tokens_est_expected']} | {row['total_tokens_low']} | {row['total_tokens_expected']} | {row['total_tokens_high']} |"
        )
    lines.append(
        f"| **{DOC}** | **{ITERATION}** | **TOTAL** | **{totals['total_input_tokens_expected']}** | **{totals['total_image_tokens_expected']}** | **{totals['total_output_tokens_expected']}** | **{totals['total_reasoning_tokens_expected']}** | **{totals['total_tokens_low']}** | **{totals['total_tokens_expected']}** | **{totals['total_tokens_high']}** |"
    )
    (RESULTS_DIR / "token_usage_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return totals


def main():
    CODES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    copied = copy_round_files()
    diego_round1 = read_json(ROUND_FILES["diego_round1"]["json"])
    jennifer_round1 = read_json(ROUND_FILES["jennifer_round1"]["json"])
    final = read_json(ROUND_FILES["jennifer_round2_final"]["json"])
    nodes = final["node_order"]
    asserted = final["asserted_edges"]
    uncertain = final.get("uncertain_edges", [])
    removed = final.get("removed_edges", [])
    final_added = final.get("added_edges", [])
    label_corrections = final.get("label_corrections", [])

    matrix, pairs = build_matrix(nodes, asserted)
    validation = validate_matrix(nodes, matrix, len(pairs))

    write_csv(RESULTS_DIR / "final_connectivity_matrix.csv", matrix_rows(nodes, matrix))
    write_csv(RESULTS_DIR / "final_matrix.csv", matrix_rows(nodes, matrix))
    write_csv(RESULTS_DIR / "final_edges.csv", edge_rows(asserted))
    write_csv(RESULTS_DIR / "final_uncertain_edges.csv", edge_rows(uncertain, include_uncertain_reason=True))
    write_csv(RESULTS_DIR / "final_removed_edges.csv", edge_rows(removed))
    write_csv(RESULTS_DIR / "final_added_edges.csv", edge_rows(final_added))
    write_csv(RESULTS_DIR / "jennifer_round1_added_edges.csv", edge_rows(jennifer_round1.get("added_edges", [])))
    write_csv(RESULTS_DIR / "final_rejected_non_edges.csv", edge_rows(diego_round1.get("rejected_non_edges", [])))

    write_json(RESULTS_DIR / "final_nodes.json", nodes)
    write_json(
        RESULTS_DIR / "final_edges.json",
        {
            "document": DOC,
            "iteration": ITERATION,
            "node_order": nodes,
            "asserted_edges": asserted,
            "uncertain_edges": uncertain,
            "removed_edges": removed,
            "final_round_added_edges": final_added,
            "jennifer_round1_added_edges": jennifer_round1.get("added_edges", []),
            "rejected_non_edges": diego_round1.get("rejected_non_edges", []),
            "label_corrections": label_corrections,
            "agreement_status": final.get("agreement_status", {}),
            "matrix_policy": "Final matrix contains asserted_edges only; uncertain_edges are excluded.",
        },
    )

    token_rows = token_usage_rows()
    token_totals = write_token_usage(token_rows)
    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "resource_folder": str(BASE),
        "source_restriction": "Only Document 13 Raw + components resources were used; no GT, no OCR, no web, no Raw + wires.",
        "agents": ["Diego", "Jennifer"],
        "round_sequence": [
            "Diego round 1 high-recall extraction",
            "Jennifer round 1 precision review",
            "Diego round 2 saturation review",
            "Jennifer round 2 final confirmation",
        ],
        "agreement_status": final.get("agreement_status", {}),
        "validation": validation,
        "uncertain_edge_count": len(uncertain),
        "removed_edge_count": len(removed),
        "final_round_added_edge_count": len(final_added),
        "jennifer_round1_added_edge_count": len(jennifer_round1.get("added_edges", [])),
        "label_correction_count": len(label_corrections),
        "round_files_copied": copied,
        "token_estimate_totals": token_totals,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(RESULTS_DIR / "final_extraction_summary.json", summary)

    lines = [
        "# Document 13 Round Summary",
        "",
        "- Diego round 1: 193 nodes, 187 asserted edges, 15 uncertain edges.",
        "- Jennifer round 1: kept the node order, added 4 PP-to-UPS feeders, refined to 191 asserted edges and 19 uncertain edges.",
        "- Diego round 2: agreed with Jennifer; no further changes.",
        "- Jennifer final: confirmed saturated consensus.",
        "",
        "Final matrix policy: asserted edges only. Uncertain dashed/control/signal candidates are preserved separately and excluded from the matrix.",
        "",
        f"Validation: {validation['node_count']} nodes, {validation['asserted_edge_count']} asserted undirected edges, symmetric matrix, zero diagonal.",
    ]
    (RESULTS_DIR / "round_summaries.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
