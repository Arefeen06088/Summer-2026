from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def include_edge(row: dict[str, str]) -> bool:
    action = (row.get("round_action") or "include").strip().lower()
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    return bool(source and target and source != target and action not in {"exclude", "reject", "rejected", "remove", "removed"})


def write_matrix(edges_path: Path, nodes_path: Path, matrix_path: Path, summary_path: Path) -> None:
    nodes: list[str] = []
    seen: set[str] = set()
    for row in read_rows(nodes_path):
        node = (row.get("node") or row.get("name") or "").strip()
        decision = (row.get("decision") or "include").strip().lower()
        if node and decision not in {"exclude", "reject", "rejected"} and node not in seen:
            nodes.append(node)
            seen.add(node)
    pairs: list[tuple[str, str]] = []
    for row in read_rows(edges_path):
        if not include_edge(row):
            continue
        source = row["source"].strip()
        target = row["target"].strip()
        for node in (source, target):
            if node not in seen:
                nodes.append(node)
                seen.add(node)
        pairs.append((source, target))
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    duplicates = 0
    for source, target in pairs:
        i, j = index[source], index[target]
        duplicates += 1 if matrix[i][j] else 0
        matrix[i][j] = matrix[j][i] = 1
    with matrix_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])
    summary_path.write_text(
        json.dumps(
            {
                "nodes": len(nodes),
                "included_edge_rows": len(pairs),
                "unique_undirected_edges": sum(sum(row) for row in matrix) // 2,
                "duplicate_edge_rows": duplicates,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print("usage: build_matrix_from_edges.py EDGES_CSV NODES_CSV MATRIX_CSV SUMMARY_JSON", file=sys.stderr)
        return 2
    write_matrix(Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
