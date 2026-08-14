from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires + components")
RESULTS = BASE / "results"


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    columns = rows[0][1:]
    row_names = [row[0] for row in rows[1:]]
    if columns != row_names:
        raise ValueError("matrix rows and columns are not in the same order")
    matrix = [[int(value) for value in row[1:]] for row in rows[1:]]
    return columns, matrix


def main() -> None:
    nodes, matrix = read_matrix(RESULTS / "final_connectivity_matrix.csv")
    size = len(nodes)
    diagonal_zero = all(matrix[i][i] == 0 for i in range(size))
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size))
    matrix_ones = sum(sum(row) for row in matrix)
    with (RESULTS / "final_sparse_edges.csv").open(newline="", encoding="utf-8") as f:
        edge_rows = list(csv.DictReader(f))
    edge_pairs = {tuple(sorted((row["source"], row["target"]))) for row in edge_rows}
    validation = {
        "nodes": size,
        "sparse_edges": len(edge_rows),
        "unique_undirected_sparse_edges": len(edge_pairs),
        "matrix_ones": matrix_ones,
        "undirected_edges_from_matrix": matrix_ones // 2,
        "same_row_column_order": True,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "edge_count_matches_matrix": len(edge_rows) == matrix_ones // 2,
    }
    (RESULTS / "validation_summary.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
