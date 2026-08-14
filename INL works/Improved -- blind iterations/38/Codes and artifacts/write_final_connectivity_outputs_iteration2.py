from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\3")
INPUT_DIR = BASE / "Input resources"
RESULT_DIR = BASE / "Results" / "Iteration_2"

AGREED_MATRIX = RESULT_DIR / "round_02_jennifer_matrix.csv"
AGREED_EDGES = RESULT_DIR / "round_02_jennifer_edges.csv"
DIEGO_MATRIX = RESULT_DIR / "round_02_diego_matrix.csv"
COMPONENTS_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"

FINAL_MATRIX = RESULT_DIR / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULT_DIR / "final_connectivity_edges.csv"
FINAL_NODES = RESULT_DIR / "final_connectivity_nodes.csv"
FINAL_UNCERTAIN = RESULT_DIR / "final_uncertain_candidates.csv"
FINAL_VALIDATION = RESULT_DIR / "final_connectivity_validation.json"
FINAL_SUMMARY = RESULT_DIR / "final_connectivity_summary.md"

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
        "status": "excluded",
        "evidence": "TR-CPT-A secondary descends to an isolated terminal dot left of BUS-120AC-A; no solid landing or junction to the rail is visible.",
    },
    {
        "candidate": "RELAY-27A -- BUS-120AC-A",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "RELAY-27A is near BUS-120AC-A but has no visible solid tap or junction to the 120 VAC rail.",
    },
    {
        "candidate": "BUS-4160A -- BUS-4160B",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "The visible path is mediated by normally-open bus tie CB-105; no direct bus-bus matrix edge is used.",
    },
    {
        "candidate": "BUS-480A -- BUS-480B",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "The diagram notes 480V tie reserved space and no connection shown between the two 480 VAC divisions.",
    },
    {
        "candidate": "GND-STA -- dashed/dotted route",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "GND-STA is visible but the dashed/dotted route does not provide a clear named component or BUS endpoint.",
    },
    {
        "candidate": "2A-XC1, 2A-BCL, 2B-XC1, 2B-BCL",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "These are terminal/cable route labels near risers, not physical components or true BUS rails.",
    },
    {
        "candidate": "2A-F1..2A-F6, 2B-F1..2B-F6, bucket numbers",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Feeder IDs and MCC bucket numbers describe load routes and internal buckets rather than independent matrix nodes.",
    },
    {
        "candidate": "division descriptors and continuation/source boxes",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Text such as 4.16 KV ESF DIV I/II, 480 VAC DIV I/II, 125 VDC TRAIN A/B, 120 VAC INST A/B, TO UNIT AUX BUS CONT., and TO STATION YARD CONT. describes rails or external continuations.",
    },
]


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows or rows[0][0] != "node":
        raise ValueError(f"Invalid matrix header in {path}")
    nodes = rows[0][1:]
    matrix: list[list[int]] = []
    for index, row in enumerate(rows[1:]):
        if index >= len(nodes) or row[0] != nodes[index]:
            raise ValueError(f"Row/header mismatch in {path} at row {index + 2}")
        values = [int(value) for value in row[1:]]
        if len(values) != len(nodes):
            raise ValueError(f"Wrong row length in {path} at row {index + 2}")
        matrix.append(values)
    if len(matrix) != len(nodes):
        raise ValueError(f"Matrix is not square in {path}")
    return nodes, matrix


def read_edges(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def physical_components() -> list[str]:
    with COMPONENTS_CSV.open(newline="", encoding="utf-8") as handle:
        return [
            row["label"]
            for row in csv.DictReader(handle)
            if row.get("node_kind") == "physical_component"
        ]


def edge_pair(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def matrix_edge_pairs(nodes: list[str], matrix: list[list[int]]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for i, source in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            if matrix[i][j] == 1:
                pairs.add(edge_pair(source, nodes[j]))
    return pairs


def validate(nodes: list[str], matrix: list[list[int]], edge_rows: list[dict[str, str]]) -> dict:
    degrees = {node: sum(matrix[index]) for index, node in enumerate(nodes)}
    matrix_pairs = matrix_edge_pairs(nodes, matrix)
    edge_csv_pairs = {edge_pair(row["source"], row["target"]) for row in edge_rows}
    physical = physical_components()
    expected_nodes = set(physical) | set(BUS_NODES)
    validation = {
        "node_count": len(nodes),
        "edge_count": len(matrix_pairs),
        "edge_csv_count": len(edge_rows),
        "square": len(matrix) == len(nodes) and all(len(row) == len(nodes) for row in matrix),
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "binary_entries": all(value in (0, 1) for row in matrix for value in row),
        "edge_csv_matches_matrix": matrix_pairs == edge_csv_pairs,
        "isolated_nodes": [node for node, degree in degrees.items() if degree == 0],
        "physical_component_count_from_input": len(physical),
        "bus_node_count_expected": len(BUS_NODES),
        "expected_node_count": len(expected_nodes),
        "missing_expected_nodes": sorted(expected_nodes - set(nodes)),
        "unexpected_nodes": sorted(set(nodes) - expected_nodes),
        "edges_in_matrix_not_csv": sorted(" -- ".join(edge) for edge in matrix_pairs - edge_csv_pairs),
        "edges_in_csv_not_matrix": sorted(" -- ".join(edge) for edge in edge_csv_pairs - matrix_pairs),
        "ground_truth_used": False,
    }
    validation["passes_internal_validation"] = all(
        [
            validation["node_count"] == 55,
            validation["edge_count"] == 55,
            validation["edge_csv_count"] == 55,
            validation["square"],
            validation["symmetric"],
            validation["diagonal_zero"],
            validation["binary_entries"],
            validation["edge_csv_matches_matrix"],
            validation["physical_component_count_from_input"] == 47,
            validation["bus_node_count_expected"] == 8,
            not validation["missing_expected_nodes"],
            not validation["unexpected_nodes"],
            validation["isolated_nodes"] == ["GND-STA"],
        ]
    )
    return validation


def write_nodes(nodes: list[str], matrix: list[list[int]]) -> None:
    physical = set(physical_components())
    buses = set(BUS_NODES)
    with FINAL_NODES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "node_kind", "degree", "source"])
        writer.writeheader()
        for index, node in enumerate(nodes):
            if node in physical:
                kind = "physical_component"
                source = "component_visual_ocr_labels.csv"
            elif node in buses:
                kind = "bus"
                source = "raw_schematic_and_label_overlay"
            else:
                kind = "unexpected"
                source = "final_matrix"
            writer.writerow(
                {
                    "node": node,
                    "node_kind": kind,
                    "degree": sum(matrix[index]),
                    "source": source,
                }
            )


def write_uncertain() -> None:
    with FINAL_UNCERTAIN.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate", "candidate_type", "status", "evidence"])
        writer.writeheader()
        writer.writerows(UNCERTAIN_OR_EXCLUDED)


def write_summary(validation: dict) -> None:
    summary = f"""# Final Connectivity Summary - Doc 3 Iteration 2

Diego and Jennifer saturated on the Round 02 graph.

- Final nodes: {validation["node_count"]}
- Final edges: {validation["edge_count"]}
- Matrix symmetric: {validation["symmetric"]}
- Diagonal zero: {validation["diagonal_zero"]}
- Node set: 47 OCR physical components plus 8 true BUS-* rails
- Isolated nodes: {", ".join(validation["isolated_nodes"]) if validation["isolated_nodes"] else "none"}

This iteration keeps named dashed control-device edges where both agents found visible terminations at named nodes: RELAY-86A/B to their 125 VDC buses, RELAY-27A to RPS-PNL-A, and RELAY-27B to RPS-PNL-B. It still excludes anonymous/intermediate wire points, terminal/cable labels, descriptors, direct bus-bus ties not shown, TR-CPT-A to BUS-120AC-A, and any GND-STA edge.
"""
    FINAL_SUMMARY.write_text(summary, encoding="utf-8")


def main() -> None:
    nodes, matrix = read_matrix(AGREED_MATRIX)
    diego_nodes, diego_matrix = read_matrix(DIEGO_MATRIX)
    if nodes != diego_nodes or matrix != diego_matrix:
        raise ValueError("Round 02 Diego and Jennifer matrices do not match")

    edge_rows = read_edges(AGREED_EDGES)
    validation = validate(nodes, matrix, edge_rows)
    validation["input_matrix"] = str(AGREED_MATRIX)
    validation["input_edges"] = str(AGREED_EDGES)
    validation["diego_jennifer_round2_agree"] = True

    shutil.copyfile(AGREED_MATRIX, FINAL_MATRIX)
    shutil.copyfile(AGREED_EDGES, FINAL_EDGES)
    write_nodes(nodes, matrix)
    write_uncertain()
    write_summary(validation)
    FINAL_VALIDATION.write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
