from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


RESULTS_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\14\Results\Iteration_1")
SOURCE_NODES = RESULTS_DIR / "round_02_jennifer_nodes.csv"
SOURCE_EDGES = RESULTS_DIR / "round_02_jennifer_edges.csv"
SOURCE_MATRIX = RESULTS_DIR / "round_02_jennifer_matrix.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_matrix(nodes: list[str], kept_edges: list[tuple[str, str]]) -> list[dict[str, int | str]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in kept_edges:
        i = index[source]
        j = index[target]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    return [
        {"node_name": node, **{nodes[j]: matrix[i][j] for j in range(len(nodes))}}
        for i, node in enumerate(nodes)
    ]


def validate(nodes: list[str], edge_rows: list[dict[str, str]], matrix_rows: list[dict[str, str]]) -> dict[str, object]:
    node_set = set(nodes)
    kept = [
        (row["source"].strip(), row["target"].strip())
        for row in edge_rows
        if row.get("status", "keep").strip().lower() == "keep"
    ]
    status_counts = Counter(row.get("status", "keep").strip().lower() for row in edge_rows)
    duplicate_kept = []
    seen = set()
    for source, target in kept:
        key = tuple(sorted((source, target)))
        if key in seen:
            duplicate_kept.append([source, target])
        seen.add(key)
    invalid_edges = [
        [source, target]
        for source, target in kept
        if source not in node_set or target not in node_set
    ]

    header = list(matrix_rows[0].keys()) if matrix_rows else []
    matrix_nodes = header[1:]
    symmetric = True
    zero_diagonal = True
    if matrix_nodes != nodes or len(matrix_rows) != len(nodes):
        symmetric = False
    else:
        for i, row in enumerate(matrix_rows):
            if row.get("node_name") != nodes[i]:
                symmetric = False
            for j, col in enumerate(nodes):
                value = int(row[col])
                if i == j and value != 0:
                    zero_diagonal = False
                if value != int(matrix_rows[j][nodes[i]]):
                    symmetric = False

    return {
        "document": "Improved doc 14",
        "iteration": "Iteration_1",
        "source_round": "round_02_jennifer",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "node_count": len(nodes),
        "edge_rows": len(edge_rows),
        "kept_edges_in_matrix": len(kept),
        "uncertain_edges_excluded_from_matrix": status_counts.get("uncertain", 0),
        "removed_edges_excluded_from_matrix": status_counts.get("remove", 0),
        "status_counts": dict(status_counts),
        "matrix_size": [len(matrix_rows), len(matrix_nodes)],
        "matrix_symmetric": symmetric,
        "matrix_zero_diagonal": zero_diagonal,
        "duplicate_kept_edges": duplicate_kept,
        "invalid_kept_edge_endpoints": invalid_edges,
        "no_intermediate_wire_nodes": not any(node.upper().startswith("WN-") for node in nodes),
        "blind_extraction_note": (
            "Final files are promoted from Jennifer round 2 agreement. Extraction used only input "
            "resources, current input-derived crops/aids, and current-round Diego/Jennifer files; "
            "GT, evaluator outputs, and archived prior results were not used."
        ),
    }


def main() -> None:
    nodes_rows = read_csv(SOURCE_NODES)
    edge_rows = read_csv(SOURCE_EDGES)
    nodes = [row["node_name"].strip() for row in nodes_rows]
    kept_edges = [
        (row["source"].strip(), row["target"].strip())
        for row in edge_rows
        if row.get("status", "keep").strip().lower() == "keep"
    ]

    final_matrix_rows = build_matrix(nodes, kept_edges)
    write_csv(RESULTS_DIR / "final_connectivity_nodes.csv", nodes_rows, list(nodes_rows[0].keys()))
    write_csv(RESULTS_DIR / "final_edge_review.csv", edge_rows, list(edge_rows[0].keys()))
    write_csv(
        RESULTS_DIR / "final_connectivity_edges.csv",
        [row for row in edge_rows if row.get("status", "keep").strip().lower() == "keep"],
        list(edge_rows[0].keys()),
    )
    write_csv(
        RESULTS_DIR / "final_edges.csv",
        [row for row in edge_rows if row.get("status", "keep").strip().lower() == "keep"],
        list(edge_rows[0].keys()),
    )
    write_csv(RESULTS_DIR / "final_connectivity_matrix.csv", final_matrix_rows, ["node_name", *nodes])
    write_csv(RESULTS_DIR / "connectivity_matrix.csv", final_matrix_rows, ["node_name", *nodes])

    matrix_rows_for_validation = read_csv(RESULTS_DIR / "final_connectivity_matrix.csv")
    validation = validate(nodes, edge_rows, matrix_rows_for_validation)
    (RESULTS_DIR / "final_connectivity_validation.json").write_text(
        json.dumps(validation, indent=2),
        encoding="utf-8",
    )
    summary = f"""# Final Connectivity Summary - Improved doc 14 / Iteration_1

Final source: `round_02_jennifer`, accepting Diego round 2 without corrections.

- Nodes: {validation["node_count"]}
- Kept matrix edges: {validation["kept_edges_in_matrix"]}
- Edge review rows: {validation["edge_rows"]}
- Uncertain excluded edges: {validation["uncertain_edges_excluded_from_matrix"]}
- Removed excluded edges: {validation["removed_edges_excluded_from_matrix"]}
- Symmetric matrix: {validation["matrix_symmetric"]}
- Zero diagonal: {validation["matrix_zero_diagonal"]}
- Invalid kept endpoints: {len(validation["invalid_kept_edge_endpoints"])}
- Intermediate WN nodes included: {not validation["no_intermediate_wire_nodes"]}

Blind extraction note: {validation["blind_extraction_note"]}
"""
    (RESULTS_DIR / "final_connectivity_summary.md").write_text(summary, encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
