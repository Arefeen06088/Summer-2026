from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + junctions"
)
RESULTS = ROOT / "results"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc26_work\results")


def result_dir() -> Path:
    if (RESULTS / "connectivity_edges_final.csv").exists():
        return RESULTS
    return FALLBACK_RESULTS


def read_edges(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    header = rows[0][1:]
    matrix: list[list[int]] = []
    for row in rows[1:]:
        if row[0] not in header:
            raise ValueError(f"matrix row node {row[0]} missing from header in {path.name}")
        matrix.append([int(value) for value in row[1:]])
    return header, matrix


def validate_round(base: Path, prefix: str, edge_name: str | None = None, matrix_name: str | None = None) -> dict[str, str | int]:
    edge_path = base / (edge_name or f"{prefix}_edges.csv")
    matrix_path = base / (matrix_name or f"{prefix}_matrix.csv")
    edges = read_edges(edge_path)
    nodes, matrix = read_matrix(matrix_path)
    node_set = set(nodes)
    endpoints = {edge["source"] for edge in edges} | {edge["target"] for edge in edges}
    missing = sorted(endpoints - node_set)
    undirected_pairs = {tuple(sorted((edge["source"], edge["target"]))) for edge in edges}
    matrix_edges = 0
    symmetric = True
    diagonal_zero = True
    for i, row in enumerate(matrix):
        if row[i] != 0:
            diagonal_zero = False
        for j, value in enumerate(row):
            if matrix[j][i] != value:
                symmetric = False
            if j > i and value == 1:
                matrix_edges += 1
    status = "PASS"
    if missing or not symmetric or not diagonal_zero or matrix_edges != len(undirected_pairs):
        status = "CHECK"
    return {
        "round": prefix,
        "nodes": len(nodes),
        "csv_rows": len(edges),
        "unique_pairs": len(undirected_pairs),
        "matrix_edges": matrix_edges,
        "missing_endpoints": ";".join(missing),
        "symmetric": str(symmetric),
        "diagonal_zero": str(diagonal_zero),
        "status": status,
    }


def main() -> None:
    base = result_dir()
    rounds = ["diego_round1", "jennifer_round1", "diego_round2", "jennifer_round2"]
    rows = [validate_round(base, prefix) for prefix in rounds]
    rows.append(validate_round(base, "final", "connectivity_edges_final.csv", "connectivity_matrix_final.csv"))
    out = base / "round_validation_summary.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "round",
                "nodes",
                "csv_rows",
                "unique_pairs",
                "matrix_edges",
                "missing_endpoints",
                "symmetric",
                "diagonal_zero",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"validation summary written to {out}")


if __name__ == "__main__":
    main()
