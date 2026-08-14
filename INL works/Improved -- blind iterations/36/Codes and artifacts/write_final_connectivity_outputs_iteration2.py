from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\1")
INPUT_DIR = BASE / "Input resources"
RESULTS_DIR = BASE / "Results" / "Iteration_2"

SOURCE_MATRIX = RESULTS_DIR / "round_02_jennifer_matrix.csv"
SOURCE_EDGES = RESULTS_DIR / "round_02_jennifer_edges.csv"
COMPONENTS_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"

FINAL_MATRIX = RESULTS_DIR / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULTS_DIR / "final_connectivity_edges.csv"
FINAL_NODES = RESULTS_DIR / "final_connectivity_nodes.csv"
FINAL_UNCERTAIN = RESULTS_DIR / "final_uncertain_candidates.csv"
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


def build_matrix(nodes: list[str], edges: list[dict[str, str]]) -> list[list[int]]:
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
    return matrix


def write_matrix(nodes: list[str], matrix: list[list[int]], path: Path) -> None:
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
        for row in sorted_edges:
            writer.writerow({field: row.get(field, "") for field in fields})


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


def write_uncertain(path: Path) -> None:
    rows = [
        {
            "source": "CB-13-TIE",
            "target": "PNL-RPS-1",
            "decision": "excluded_from_matrix",
            "reason": (
                "Dashed RPS TRIP route reaches the PNL-RPS-1 side port, but the upper end "
                "approaches the underside/label area of CB-13-TIE without clear terminal-dot contact."
            ),
        }
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "decision", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def validate(nodes: list[str], matrix: list[list[int]], edge_count: int) -> dict[str, object]:
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix)))
    zero_diagonal = all(matrix[i][i] == 0 for i in range(len(matrix)))
    matrix_edge_count = sum(sum(row) for row in matrix) // 2
    return {
        "node_count": len(nodes),
        "edge_count_from_edges_csv": edge_count,
        "edge_count_from_matrix": matrix_edge_count,
        "headers_match_rows": True,
        "symmetric": symmetric,
        "zero_diagonal": zero_diagonal,
        "edge_counts_match": matrix_edge_count == edge_count,
    }


def write_summary(validation: dict[str, object], path: Path) -> None:
    text = f"""# Final Connectivity Extraction - Iteration 2

Source round: `round_02_jennifer_*`, after Diego and Jennifer converged.

- Nodes: {validation["node_count"]}
- Undirected edges: {validation["edge_count_from_edges_csv"]}
- Matrix headers match row order: {validation["headers_match_rows"]}
- Symmetric matrix: {validation["symmetric"]}
- Zero diagonal: {validation["zero_diagonal"]}
- Edge list and matrix counts match: {validation["edge_counts_match"]}

Iteration 2 collapses `RPS-TRIP` and `RPS-LOCKOUT` out of the matrix node set as route annotations. The visible solid lockout route is represented directly as `CB-4K-TIE` to `PNL-RPS-1`. The uncertain dashed trip route near `CB-13-TIE` is documented in `final_uncertain_candidates.csv` and excluded from the final matrix.

No Ground Truth or GT-derived feedback was used.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    nodes = read_nodes_from_matrix(SOURCE_MATRIX)
    edges = read_edges(SOURCE_EDGES)
    physical = read_physical_components(COMPONENTS_CSV)

    matrix = build_matrix(nodes, edges)
    write_matrix(nodes, matrix, FINAL_MATRIX)
    write_edges(edges, FINAL_EDGES)
    write_nodes(nodes, physical, edges, FINAL_NODES)
    write_uncertain(FINAL_UNCERTAIN)

    validation = validate(nodes, matrix, len(edges))
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
