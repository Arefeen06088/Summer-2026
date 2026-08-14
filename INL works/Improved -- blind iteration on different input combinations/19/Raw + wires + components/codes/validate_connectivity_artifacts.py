from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"


def read_edges(path: Path) -> list[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [(row["source"], row["target"]) for row in reader]


def read_matrix(path: Path) -> tuple[list[str], dict[str, dict[str, int]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        cols = header[1:]
        matrix: dict[str, dict[str, int]] = {}
        rows: list[str] = []
        for raw_row in reader:
            node = raw_row[0]
            values = [int(value) for value in raw_row[1:]]
            rows.append(node)
            matrix[node] = dict(zip(cols, values))
    if rows != cols:
        raise AssertionError("matrix row and column names differ or are not in the same order")
    return rows, matrix


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def validate() -> dict[str, object]:
    nodes, matrix = read_matrix(RESULTS_DIR / "final_connectivity_matrix.csv")
    final_edges = read_edges(RESULTS_DIR / "final_sparse_edges.csv")
    excluded_edges = read_edges(RESULTS_DIR / "uncertain_excluded_edges.csv")

    failures: list[str] = []

    for node in nodes:
        if matrix[node][node] != 0:
            failures.append(f"diagonal is nonzero for {node}")

    for source in nodes:
        for target in nodes:
            if matrix[source][target] != matrix[target][source]:
                failures.append(f"asymmetric value for {source} <-> {target}")

    seen_edges: set[tuple[str, str]] = set()
    for source, target in final_edges:
        key = edge_key(source, target)
        if key in seen_edges:
            failures.append(f"duplicate final edge {source} -- {target}")
        seen_edges.add(key)
        if source not in matrix or target not in matrix[source]:
            failures.append(f"final edge has unknown node {source} -- {target}")
        elif matrix[source][target] != 1:
            failures.append(f"final edge missing from matrix {source} -- {target}")

    matrix_edge_count = 0
    for i, source in enumerate(nodes):
        for target in nodes[i + 1 :]:
            matrix_edge_count += matrix[source][target]
    if matrix_edge_count != len(final_edges):
        failures.append(f"matrix edge count {matrix_edge_count} does not match sparse edge count {len(final_edges)}")

    final_keys = {edge_key(source, target) for source, target in final_edges}
    for source, target in excluded_edges:
        if edge_key(source, target) in final_keys:
            failures.append(f"excluded edge appears in final sparse list {source} -- {target}")
        if source in matrix and target in matrix[source] and matrix[source][target] != 0:
            failures.append(f"excluded edge appears in final matrix {source} -- {target}")

    result = {
        "document": 19,
        "iteration": 1,
        "passed": not failures,
        "final_node_count": len(nodes),
        "final_edge_count": len(final_edges),
        "matrix_edge_count": matrix_edge_count,
        "excluded_candidate_edge_count": len(excluded_edges),
        "failures": failures,
    }
    (RESULTS_DIR / "validation_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
