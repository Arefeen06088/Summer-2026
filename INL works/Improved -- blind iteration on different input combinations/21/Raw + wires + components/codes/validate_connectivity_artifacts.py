from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"


def canonical(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    headers = rows[0][1:]
    names = [row[0] for row in rows[1:]]
    matrix = [[int(cell) for cell in row[1:]] for row in rows[1:]]
    assert headers == names, f"{path.name}: row/column names differ"
    return names, matrix


def read_sparse(path: Path) -> set[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {canonical(row["source"], row["target"]) for row in reader}


def validate_pair(prefix: str) -> dict[str, object]:
    matrix_path = RESULTS_DIR / f"{prefix}_connectivity_matrix.csv"
    sparse_path = RESULTS_DIR / f"{prefix}_sparse_edges.csv"
    names, matrix = read_matrix(matrix_path)
    n = len(names)
    assert all(len(row) == n for row in matrix), f"{prefix}: matrix is not square"
    assert len(set(names)) == n, f"{prefix}: duplicate node names"
    for i in range(n):
        assert matrix[i][i] == 0, f"{prefix}: non-zero diagonal at {names[i]}"
        for j in range(n):
            assert matrix[i][j] == matrix[j][i], f"{prefix}: asymmetric at {names[i]}, {names[j]}"
    matrix_edges = {
        canonical(names[i], names[j])
        for i in range(n)
        for j in range(i + 1, n)
        if matrix[i][j] == 1
    }
    sparse_edges = read_sparse(sparse_path)
    assert matrix_edges == sparse_edges, f"{prefix}: sparse/matrix edge mismatch"
    return {
        "prefix": prefix,
        "nodes": n,
        "edges": len(matrix_edges),
        "matrix_file": str(matrix_path),
        "sparse_file": str(sparse_path),
        "ok": True,
    }


def main() -> None:
    prefixes = ["round01_diego", "round01_jennifer", "round02_diego", "round02_jennifer", "final"]
    results = [validate_pair(prefix) for prefix in prefixes]
    payload = {"ok": True, "matrices": results}
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (RESULTS_DIR / "validation_check.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
