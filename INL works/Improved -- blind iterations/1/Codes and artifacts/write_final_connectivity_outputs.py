from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\1")
INPUT_DIR = BASE / "Input resources"
RESULTS_DIR = BASE / "Results" / "Iteration_1"

SOURCE_MATRIX = RESULTS_DIR / "round_02_jennifer_matrix.csv"
SOURCE_EDGES = RESULTS_DIR / "round_02_jennifer_edges.csv"
COMPONENTS_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"

FINAL_MATRIX = RESULTS_DIR / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULTS_DIR / "final_connectivity_edges.csv"
FINAL_NODES = RESULTS_DIR / "final_connectivity_nodes.csv"
FINAL_VALIDATION = RESULTS_DIR / "final_connectivity_validation.json"
FINAL_SUMMARY = RESULTS_DIR / "final_connectivity_summary.md"


def read_nodes_from_matrix(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        header = next(csv.reader(f))
    return [name for name in header[1:] if name]


def read_edges(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_physical_components(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return {row["label"] for row in csv.DictReader(f)}


def write_matrix(nodes: list[str], edges: list[dict[str, str]], path: Path) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]

    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        if source not in index or target not in index:
            raise ValueError(f"Edge references node not in matrix: {source!r}, {target!r}")
        if source == target:
            raise ValueError(f"Unexpected self-loop: {source!r}")
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def write_edges(edges: list[dict[str, str]], path: Path) -> None:
    fields = ["source", "target", "confidence", "evidence"]
    sorted_edges = sorted(edges, key=lambda row: (row["source"], row["target"]))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in sorted_edges)


def write_nodes(nodes: list[str], physical: set[str], edges: list[dict[str, str]], path: Path) -> None:
    degree = {node: 0 for node in nodes}
    for edge in edges:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["node", "node_kind", "degree"])
        writer.writeheader()
        for node in nodes:
            writer.writerow(
                {
                    "node": node,
                    "node_kind": "physical_component" if node in physical else "logical_or_named_node",
                    "degree": degree[node],
                }
            )


def validate_matrix(path: Path, edge_count: int) -> dict[str, object]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    header = rows[0][1:]
    body = rows[1:]
    node_names = [row[0] for row in body]
    values = [[int(value) for value in row[1:]] for row in body]

    symmetric = all(values[i][j] == values[j][i] for i in range(len(values)) for j in range(len(values)))
    zero_diagonal = all(values[i][i] == 0 for i in range(len(values)))
    matrix_edge_count = sum(sum(row) for row in values) // 2

    return {
        "node_count": len(node_names),
        "edge_count_from_edges_csv": edge_count,
        "edge_count_from_matrix": matrix_edge_count,
        "headers_match_rows": header == node_names,
        "symmetric": symmetric,
        "zero_diagonal": zero_diagonal,
        "edge_counts_match": matrix_edge_count == edge_count,
    }


def write_summary(validation: dict[str, object], path: Path) -> None:
    text = f"""# Final Connectivity Extraction

Source round: `round_02_jennifer_*`, after Diego and Jennifer converged.

- Nodes: {validation["node_count"]}
- Undirected edges: {validation["edge_count_from_edges_csv"]}
- Matrix headers match row order: {validation["headers_match_rows"]}
- Symmetric matrix: {validation["symmetric"]}
- Zero diagonal: {validation["zero_diagonal"]}
- Edge list and matrix counts match: {validation["edge_counts_match"]}

No Ground Truth or GT-derived feedback was used. The final edge evidence is in `final_connectivity_edges.csv`.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    nodes = read_nodes_from_matrix(SOURCE_MATRIX)
    edges = read_edges(SOURCE_EDGES)
    physical = read_physical_components(COMPONENTS_CSV)

    write_matrix(nodes, edges, FINAL_MATRIX)
    write_edges(edges, FINAL_EDGES)
    write_nodes(nodes, physical, edges, FINAL_NODES)

    validation = validate_matrix(FINAL_MATRIX, len(edges))
    FINAL_VALIDATION.write_text(json.dumps(validation, indent=2), encoding="utf-8")
    write_summary(validation, FINAL_SUMMARY)

    if not all(
        [
            validation["headers_match_rows"],
            validation["symmetric"],
            validation["zero_diagonal"],
            validation["edge_counts_match"],
        ]
    ):
        raise SystemExit(f"Validation failed: {validation}")

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
