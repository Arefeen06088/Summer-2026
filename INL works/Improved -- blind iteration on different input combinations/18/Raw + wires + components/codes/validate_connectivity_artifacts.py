from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + components")
RESULTS = BASE / "results"


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    header = rows[0][1:]
    labels = [row[0] for row in rows[1:]]
    if labels != header:
        raise ValueError("row and column labels differ")
    matrix = [[int(value) for value in row[1:]] for row in rows[1:]]
    return labels, matrix


def read_sparse(path: Path) -> set[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return {tuple(sorted((row["source"], row["target"]))) for row in rows}


def main() -> None:
    labels, matrix = read_matrix(RESULTS / "final_connectivity_matrix.csv")
    sparse = read_sparse(RESULTS / "final_sparse_edges.csv")
    n = len(labels)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(n))
    matrix_edges = sum(sum(row) for row in matrix) // 2
    critical_present = [
        ("CB-GRID-A", "BB-SWYD-230"),
        ("BB-SWYD-230", "CB-GEN-ISO"),
        ("GEN-MAIN-1", "TR-UAT-1A"),
        ("GEN-MAIN-1", "TR-UAT-1B"),
        ("CB-DG-B", "BUS-4160B"),
        ("BUS-4160A", "TR-480-B1"),
        ("BUS-4160B", "TR-480-C1"),
        ("BUS-480B", "CHG-125A"),
        ("BUS-480C", "CHG-125B"),
        ("RELAY-K101", "RELAY-K102"),
        ("RELAY-K201", "RELAY-K202"),
    ]
    critical_absent = [
        ("BUS-MAIN-230", "TR-UAT-1A"),
        ("BUS-MAIN-230", "TR-UAT-1B"),
        ("PLC-RPS-A", "RELAY-K102"),
        ("PLC-RPS-B", "RELAY-K202"),
    ]
    present_ok = all(tuple(sorted(edge)) in sparse for edge in critical_present)
    absent_ok = all(tuple(sorted(edge)) not in sparse for edge in critical_absent)
    result = {
        "nodes": n,
        "sparse_edges": len(sparse),
        "matrix_edges": matrix_edges,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "sparse_matches_matrix": matrix_edges == len(sparse),
        "critical_present_ok": present_ok,
        "critical_absent_ok": absent_ok,
        "passed": symmetric and diagonal_zero and matrix_edges == len(sparse) and present_ok and absent_ok,
    }
    (RESULTS / "validation_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
