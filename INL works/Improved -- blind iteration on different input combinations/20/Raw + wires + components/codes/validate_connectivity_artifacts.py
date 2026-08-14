from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def read_edges(path: Path) -> list[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [(row["source"], row["target"]) for row in reader]


def read_matrix(path: Path) -> tuple[list[str], dict[str, dict[str, int]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        cols = header[1:]
        rows: list[str] = []
        matrix: dict[str, dict[str, int]] = {}
        for raw_row in reader:
            node = raw_row[0]
            values = [int(value) for value in raw_row[1:]]
            rows.append(node)
            matrix[node] = dict(zip(cols, values))
    if rows != cols:
        raise AssertionError("matrix row and column names differ or are not in the same order")
    return rows, matrix


def validate() -> dict[str, object]:
    nodes, matrix = read_matrix(RESULTS_DIR / "final_connectivity_matrix.csv")
    final_edges = read_edges(RESULTS_DIR / "final_sparse_edges.csv")
    excluded_edges = read_edges(RESULTS_DIR / "uncertain_excluded_edges.csv")
    final_keys = {edge_key(source, target) for source, target in final_edges}
    failures: list[str] = []

    for node in nodes:
        if matrix[node][node] != 0:
            failures.append(f"nonzero diagonal for {node}")

    for source in nodes:
        for target in nodes:
            if matrix[source][target] != matrix[target][source]:
                failures.append(f"asymmetric matrix values for {source} and {target}")

    seen: set[tuple[str, str]] = set()
    for source, target in final_edges:
        key = edge_key(source, target)
        if key in seen:
            failures.append(f"duplicate final edge {source} -- {target}")
        seen.add(key)
        if source not in matrix or target not in matrix[source]:
            failures.append(f"final edge has unknown node {source} -- {target}")
        elif matrix[source][target] != 1:
            failures.append(f"final sparse edge missing from matrix {source} -- {target}")

    matrix_edge_count = 0
    for i, source in enumerate(nodes):
        for target in nodes[i + 1 :]:
            matrix_edge_count += matrix[source][target]
    if matrix_edge_count != len(final_edges):
        failures.append(f"matrix edge count {matrix_edge_count} does not match sparse edge count {len(final_edges)}")

    must_have = [
        ("BUS-480-A", "RECT-125A"),
        ("BUS-480-C", "RECT-125B"),
        ("RELAY-K106", "RELAY-K108"),
    ]
    for source, target in must_have:
        if edge_key(source, target) not in final_keys:
            failures.append(f"required final edge missing {source} -- {target}")

    must_not_have = [
        ("HTR-PZR-01A", "RECT-125A"),
        ("BUS-13K-A", "BUS-13K-B"),
        ("BUS-416-A", "BUS-416-B"),
        ("BUS-480-B", "BUS-480-C"),
        ("BUS-125DCA", "BUS-125DCB"),
    ]
    for source, target in must_not_have:
        if edge_key(source, target) in final_keys:
            failures.append(f"forbidden final edge present {source} -- {target}")

    for source, target in excluded_edges:
        if edge_key(source, target) in final_keys:
            failures.append(f"excluded edge appears in final sparse list {source} -- {target}")
        if source in matrix and target in matrix[source] and matrix[source][target] != 0:
            failures.append(f"excluded edge appears in final matrix {source} -- {target}")

    result = {
        "document": 20,
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
