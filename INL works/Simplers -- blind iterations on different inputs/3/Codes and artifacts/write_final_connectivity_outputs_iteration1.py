from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\3")
INPUT_DIR = BASE / "Input resources"
RESULT_DIR = BASE / "Results" / "Iteration_1"

FINAL_MATRIX = RESULT_DIR / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULT_DIR / "final_connectivity_edges.csv"
FINAL_NODES = RESULT_DIR / "final_connectivity_nodes.csv"
FINAL_UNCERTAIN = RESULT_DIR / "final_uncertain_candidates.csv"
FINAL_VALIDATION = RESULT_DIR / "final_connectivity_validation.json"
FINAL_SUMMARY = RESULT_DIR / "final_connectivity_summary.md"

AGREED_MATRIX = RESULT_DIR / "round_02_jennifer_matrix.csv"
AGREED_EDGES = RESULT_DIR / "round_02_jennifer_edges.csv"
DIEGO_MATRIX = RESULT_DIR / "round_02_diego_matrix.csv"
COMPONENTS_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"

BUS_NODES = [
    "BUS-4160A",
    "BUS-4160B",
    "BUS-480A",
    "BUS-480B",
    "BUS-125DC-A",
    "BUS-125DC-B",
    "BUS-120AC-A",
    "BUS-120AC-B",
]

UNCERTAIN_OR_EXCLUDED = [
    {
        "candidate": "TR-CPT-A -- BUS-120AC-A",
        "candidate_type": "edge",
        "status": "excluded_uncertain",
        "evidence": "A-side CPT secondary conductor terminates at a visible endpoint/gap; no solid landing on BUS-120AC-A is visible.",
    },
    {
        "candidate": "BUS-125DC-A -- RELAY-86A",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Relay 86A route is dashed/control-only from the 125 VDC rail area, not a solid matrix conductor.",
    },
    {
        "candidate": "BUS-120AC-A -- RELAY-27A",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Relay 27A has no visible solid tap to BUS-120AC-A; nearby route is dashed/control-only.",
    },
    {
        "candidate": "RELAY-27A -- RPS-PNL-A",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "The visible route between relay 27A and RPS-PNL-A is dashed/control wiring, not a solid connectivity edge.",
    },
    {
        "candidate": "RELAY-86A -- RPS-PNL-A",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "The visible route between relay 86A and RPS-PNL-A is dashed/control wiring, not a solid connectivity edge.",
    },
    {
        "candidate": "BUS-125DC-B -- RELAY-86B",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Relay 86B route is dashed/control-only from the 125 VDC rail area, not a solid matrix conductor.",
    },
    {
        "candidate": "RELAY-27B -- RPS-PNL-B",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Relay 27B has a solid BUS-120AC-B tap, but its route toward RPS-PNL-B is dashed/control-only.",
    },
    {
        "candidate": "RELAY-86B -- RPS-PNL-B",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "The visible route between relay 86B and RPS-PNL-B is dashed/control wiring, not a solid connectivity edge.",
    },
    {
        "candidate": "GND-STA -- dotted ground/control route",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Station ground is visible but no supported solid edge to a named component or BUS node is visible.",
    },
    {
        "candidate": "2A-XC1, 2A-BCL, 2B-XC1, 2B-BCL",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Cable/terminal route labels sit near dashed/side risers and are not physical components or true BUS rails.",
    },
    {
        "candidate": "division descriptors and feeder IDs",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Labels such as 4.16 KV ESF DIV I/II, 480 VAC DIV I/II, 125 VDC TRAIN A/B, 120 VAC INST A/B, feeder IDs, and bucket numbers describe routes/rails rather than separate connectivity nodes.",
    },
]


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise ValueError(f"{path} is empty")
    header = rows[0]
    if header[0] != "node":
        raise ValueError(f"{path} first header cell must be 'node'")
    nodes = header[1:]
    matrix: list[list[int]] = []
    for index, row in enumerate(rows[1:]):
        if len(row) != len(nodes) + 1:
            raise ValueError(f"{path} row {index + 2} has wrong length")
        if row[0] != nodes[index]:
            raise ValueError(f"{path} row {index + 2} name does not match header order")
        matrix.append([int(value) for value in row[1:]])
    if len(matrix) != len(nodes):
        raise ValueError(f"{path} is not square")
    return nodes, matrix


def matrix_edges(nodes: list[str], matrix: list[list[int]]) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for i, source in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            if matrix[i][j] == 1:
                edges.add((source, nodes[j]))
    return edges


def read_edge_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalized_edge(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def read_physical_components() -> list[str]:
    with COMPONENTS_CSV.open(newline="", encoding="utf-8") as handle:
        return [
            row["label"]
            for row in csv.DictReader(handle)
            if row.get("node_kind") == "physical_component"
        ]


def validate_matrix(nodes: list[str], matrix: list[list[int]]) -> dict:
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    binary = all(value in (0, 1) for row in matrix for value in row)
    degrees = {node: sum(matrix[index]) for index, node in enumerate(nodes)}
    return {
        "node_count": len(nodes),
        "edge_count": sum(degrees.values()) // 2,
        "square": len(matrix) == len(nodes) and all(len(row) == len(nodes) for row in matrix),
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "binary_entries": binary,
        "isolated_nodes": [node for node, degree in degrees.items() if degree == 0],
    }


def write_nodes_csv(nodes: list[str], matrix: list[list[int]], physical_components: list[str]) -> None:
    physical_set = set(physical_components)
    bus_set = set(BUS_NODES)
    degrees = {node: sum(matrix[index]) for index, node in enumerate(nodes)}
    with FINAL_NODES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "node_kind", "degree", "source"])
        writer.writeheader()
        for node in nodes:
            if node in physical_set:
                node_kind = "physical_component"
                source = "component_visual_ocr_labels.csv"
            elif node in bus_set:
                node_kind = "bus"
                source = "raw_schematic_and_label_overlay"
            else:
                node_kind = "unexpected"
                source = "final_matrix"
            writer.writerow(
                {
                    "node": node,
                    "node_kind": node_kind,
                    "degree": degrees[node],
                    "source": source,
                }
            )


def write_uncertain_csv() -> None:
    with FINAL_UNCERTAIN.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["candidate", "candidate_type", "status", "evidence"],
        )
        writer.writeheader()
        writer.writerows(UNCERTAIN_OR_EXCLUDED)


def write_summary(validation: dict, unexpected_nodes: list[str], missing_nodes: list[str]) -> None:
    summary = f"""# Final Connectivity Summary - Doc 3 Iteration 1

Diego and Jennifer saturated on the Round 02 graph.

- Final nodes: {validation["node_count"]}
- Final edges: {validation["edge_count"]}
- Matrix symmetric: {validation["symmetric"]}
- Diagonal zero: {validation["diagonal_zero"]}
- Node set: 47 OCR physical components plus 8 true BUS-* rails
- Unexpected nodes: {len(unexpected_nodes)}
- Missing expected nodes: {len(missing_nodes)}

The final graph excludes descriptor labels, feeder IDs, load bucket numbers, cable/terminal labels, and anonymous wire topology points. Dashed/control-only paths are documented in `final_uncertain_candidates.csv` instead of being promoted to matrix edges.
"""
    FINAL_SUMMARY.write_text(summary, encoding="utf-8")


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    nodes, matrix = read_matrix(AGREED_MATRIX)
    diego_nodes, diego_matrix = read_matrix(DIEGO_MATRIX)
    if nodes != diego_nodes or matrix != diego_matrix:
        raise ValueError("Round 02 Diego and Jennifer matrices do not match")

    shutil.copyfile(AGREED_MATRIX, FINAL_MATRIX)
    shutil.copyfile(AGREED_EDGES, FINAL_EDGES)

    physical_components = read_physical_components()
    expected_nodes = set(physical_components) | set(BUS_NODES)
    actual_nodes = set(nodes)
    missing_expected_nodes = sorted(expected_nodes - actual_nodes)
    unexpected_nodes = sorted(actual_nodes - expected_nodes)

    validation = validate_matrix(nodes, matrix)
    validation.update(
        {
            "input_matrix": str(AGREED_MATRIX),
            "input_edges": str(AGREED_EDGES),
            "diego_jennifer_round2_agree": True,
            "physical_component_count_from_input": len(physical_components),
            "bus_node_count_expected": len(BUS_NODES),
            "expected_node_count": len(expected_nodes),
            "missing_expected_nodes": missing_expected_nodes,
            "unexpected_nodes": unexpected_nodes,
            "ground_truth_used": False,
        }
    )

    edge_rows = read_edge_csv(AGREED_EDGES)
    matrix_edge_set = {normalized_edge(source, target) for source, target in matrix_edges(nodes, matrix)}
    csv_edge_set = {normalized_edge(row["source"], row["target"]) for row in edge_rows}
    validation["edge_csv_count"] = len(edge_rows)
    validation["edge_csv_matches_matrix"] = matrix_edge_set == csv_edge_set
    validation["edges_in_matrix_not_csv"] = sorted([" -- ".join(edge) for edge in matrix_edge_set - csv_edge_set])
    validation["edges_in_csv_not_matrix"] = sorted([" -- ".join(edge) for edge in csv_edge_set - matrix_edge_set])

    all_checks = [
        validation["square"],
        validation["symmetric"],
        validation["diagonal_zero"],
        validation["binary_entries"],
        validation["edge_csv_matches_matrix"],
        not missing_expected_nodes,
        not unexpected_nodes,
        validation["node_count"] == 55,
        validation["edge_count"] == 51,
        len(physical_components) == 47,
    ]
    validation["passes_internal_validation"] = all(all_checks)

    write_nodes_csv(nodes, matrix, physical_components)
    write_uncertain_csv()
    write_summary(validation, unexpected_nodes, missing_expected_nodes)
    FINAL_VALIDATION.write_text(json.dumps(validation, indent=2), encoding="utf-8")

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
