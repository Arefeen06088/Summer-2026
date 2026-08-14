from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions + OCR")
RESULTS = BASE / "results"


ROUNDS = [
    ("round01_diego", RESULTS / "document22_round01_diego_edges.csv", RESULTS / "document22_round01_diego_nodes.csv", RESULTS / "document22_round01_diego_adjacency_matrix.csv"),
    ("round02_jennifer", RESULTS / "document22_round02_jennifer_edges.csv", RESULTS / "document22_round02_jennifer_nodes.csv", RESULTS / "document22_round02_jennifer_adjacency_matrix.csv"),
    ("round03_diego", RESULTS / "document22_round03_diego_edges.csv", RESULTS / "document22_round03_diego_nodes.csv", RESULTS / "document22_round03_diego_adjacency_matrix.csv"),
    ("round04_jennifer_final", RESULTS / "document22_round04_jennifer_final_edges.csv", RESULTS / "document22_round04_jennifer_final_nodes.csv", RESULTS / "document22_round04_jennifer_final_adjacency_matrix.csv"),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def edge_key(row: dict[str, str]) -> tuple[str, str]:
    a = row["source"].strip()
    b = row["target"].strip()
    return tuple(sorted((a, b)))


def validate_matrix(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"exists": False}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    body = rows[1:]
    row_nodes = [row[0] for row in body]
    square = len(header) == len(body) == len(row_nodes)
    same_order = header == row_nodes
    symmetric = True
    diagonal_zero = True
    ones = 0
    for i, row in enumerate(body):
        values = [int(v) for v in row[1:]]
        if i < len(values) and values[i] != 0:
            diagonal_zero = False
        for j, value in enumerate(values):
            ones += value
            if j < len(body):
                other = int(body[j][i + 1])
                if value != other:
                    symmetric = False
    return {
        "exists": True,
        "nodes": len(header),
        "square": square,
        "same_header_row_order": same_order,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "undirected_edges_from_matrix": ones // 2,
    }


def main() -> None:
    summaries: list[dict[str, object]] = []
    previous_edges: set[tuple[str, str]] | None = None
    previous_nodes: set[str] | None = None
    for name, edges_path, nodes_path, matrix_path in ROUNDS:
        edges = read_rows(edges_path)
        nodes = read_rows(nodes_path)
        included_edges = {
            edge_key(row)
            for row in edges
            if row.get("source", "").strip()
            and row.get("target", "").strip()
            and row.get("source", "").strip() != row.get("target", "").strip()
            and row.get("round_action", "").strip().lower() not in {"exclude", "reject", "rejected", "remove", "removed"}
        }
        included_nodes = {
            row.get("node", "").strip()
            for row in nodes
            if row.get("node", "").strip()
            and row.get("decision", "").strip().lower() not in {"exclude", "reject", "rejected"}
        }
        summary = {
            "round": name,
            "edges_file": str(edges_path),
            "nodes_file": str(nodes_path),
            "matrix_file": str(matrix_path),
            "node_count": len(included_nodes),
            "edge_count": len(included_edges),
            "edge_kind_counts": dict(Counter(row.get("edge_kind", "") for row in edges)),
            "confidence_counts": dict(Counter(row.get("confidence", "") for row in edges)),
            "matrix_validation": validate_matrix(matrix_path),
        }
        if previous_edges is not None:
            summary["edges_added_vs_previous"] = len(included_edges - previous_edges)
            summary["edges_removed_vs_previous"] = len(previous_edges - included_edges)
        if previous_nodes is not None:
            summary["nodes_added_vs_previous"] = len(included_nodes - previous_nodes)
            summary["nodes_removed_vs_previous"] = len(previous_nodes - included_nodes)
        summaries.append(summary)
        previous_edges = included_edges
        previous_nodes = included_nodes

    final_summary = {
        "document": 22,
        "iteration": 1,
        "rounds": summaries,
    }
    (RESULTS / "document22_round_comparison_and_validation.json").write_text(json.dumps(final_summary, indent=2), encoding="utf-8")
    with (RESULTS / "document22_round_comparison_and_validation.md").open("w", encoding="utf-8") as f:
        f.write("# Document 22 Round Comparison and Validation\n\n")
        f.write("| Round | Nodes | Edges | Added Edges | Removed Edges | Matrix OK |\n")
        f.write("|---|---:|---:|---:|---:|---|\n")
        for summary in summaries:
            matrix = summary["matrix_validation"]
            matrix_ok = (
                isinstance(matrix, dict)
                and matrix.get("exists")
                and matrix.get("square")
                and matrix.get("same_header_row_order")
                and matrix.get("symmetric")
                and matrix.get("diagonal_zero")
            )
            f.write(
                f"| {summary['round']} | {summary['node_count']} | {summary['edge_count']} | "
                f"{summary.get('edges_added_vs_previous', 0)} | {summary.get('edges_removed_vs_previous', 0)} | {matrix_ok} |\n"
            )
    print(json.dumps(final_summary, indent=2))


if __name__ == "__main__":
    main()
