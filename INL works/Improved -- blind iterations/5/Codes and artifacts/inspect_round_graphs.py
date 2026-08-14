from __future__ import annotations

import csv
from pathlib import Path


RESULTS = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\5\Results\Iteration_1")


def read_matrix(path: Path):
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        nodes = header[1:]
        matrix = {}
        for row in reader:
            if row:
                matrix[row[0]] = {col: int(val) for col, val in zip(nodes, row[1:])}
    return nodes, matrix


def edges_from_matrix(nodes, matrix):
    edges = set()
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            if matrix[a][b] == 1:
                edges.add(tuple(sorted((a, b))))
    return edges


def summarize(name: str):
    nodes, matrix = read_matrix(RESULTS / f"{name}_matrix.csv")
    edges = edges_from_matrix(nodes, matrix)
    symmetric = all(matrix[a][b] == matrix[b][a] for a in nodes for b in nodes)
    diagonal_zero = all(matrix[n][n] == 0 for n in nodes)
    print(f"{name}: nodes={len(nodes)} edges={len(edges)} symmetric={symmetric} diagonal_zero={diagonal_zero}")
    return nodes, edges


def main():
    names = [
        "round_01_diego",
        "round_01_jennifer",
        "round_02_diego",
        "round_02_jennifer",
    ]
    existing = [name for name in names if (RESULTS / f"{name}_matrix.csv").exists()]
    data = {name: summarize(name) for name in existing}
    for before, after in zip(existing, existing[1:]):
        before_nodes, before_edges = data[before]
        after_nodes, after_edges = data[after]
        print(f"\n{before} -> {after}")
        print(f"  nodes removed: {sorted(set(before_nodes) - set(after_nodes))}")
        print(f"  nodes added:   {sorted(set(after_nodes) - set(before_nodes))}")
        print(f"  edges removed: {len(before_edges - after_edges)}")
        for edge in sorted(before_edges - after_edges):
            print(f"    - {edge[0]} -- {edge[1]}")
        print(f"  edges added: {len(after_edges - before_edges)}")
        for edge in sorted(after_edges - before_edges):
            print(f"    + {edge[0]} -- {edge[1]}")


if __name__ == "__main__":
    main()
