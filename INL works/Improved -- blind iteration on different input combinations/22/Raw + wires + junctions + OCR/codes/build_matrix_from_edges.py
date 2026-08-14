from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


EDGE_COLUMNS = ["source", "target", "edge_kind", "confidence", "evidence", "round_action", "notes"]


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_matrix(edges_path: Path, nodes_path: Path, matrix_path: Path, summary_path: Path) -> None:
    edge_rows = read_csv_dicts(edges_path)
    node_rows = read_csv_dicts(nodes_path) if nodes_path.exists() else []

    ordered_nodes: list[str] = []
    seen: set[str] = set()

    for row in node_rows:
        node = (row.get("node") or "").strip()
        decision = (row.get("decision") or "include").strip().lower()
        if node and decision not in {"exclude", "reject", "rejected"} and node not in seen:
            ordered_nodes.append(node)
            seen.add(node)

    clean_edges: list[tuple[str, str]] = []
    skipped: list[dict[str, str]] = []
    for row in edge_rows:
        source = (row.get("source") or "").strip()
        target = (row.get("target") or "").strip()
        action = (row.get("round_action") or "include").strip().lower()
        if not source or not target or source == target or action in {"exclude", "reject", "rejected", "remove"}:
            skipped.append(row)
            continue
        for node in (source, target):
            if node not in seen:
                ordered_nodes.append(node)
                seen.add(node)
        clean_edges.append((source, target))

    index = {node: i for i, node in enumerate(ordered_nodes)}
    matrix = [[0 for _ in ordered_nodes] for _ in ordered_nodes]
    duplicates = 0
    for source, target in clean_edges:
        i = index[source]
        j = index[target]
        if matrix[i][j]:
            duplicates += 1
        matrix[i][j] = 1
        matrix[j][i] = 1

    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    with matrix_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *ordered_nodes])
        for node, row in zip(ordered_nodes, matrix):
            writer.writerow([node, *row])

    summary = {
        "nodes": len(ordered_nodes),
        "included_edge_rows": len(clean_edges),
        "unique_undirected_edges": sum(sum(row) for row in matrix) // 2,
        "skipped_edge_rows": len(skipped),
        "duplicate_edge_rows": duplicates,
        "matrix_file": str(matrix_path),
        "edges_file": str(edges_path),
        "nodes_file": str(nodes_path),
    }
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(
            "usage: build_matrix_from_edges.py EDGES_CSV NODES_CSV MATRIX_CSV SUMMARY_JSON",
            file=sys.stderr,
        )
        return 2
    edges_path = Path(argv[1])
    nodes_path = Path(argv[2])
    matrix_path = Path(argv[3])
    summary_path = Path(argv[4])
    write_matrix(edges_path, nodes_path, matrix_path, summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
