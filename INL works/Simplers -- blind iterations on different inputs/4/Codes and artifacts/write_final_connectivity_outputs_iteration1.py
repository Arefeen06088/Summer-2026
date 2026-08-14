from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\4")
INPUT_DIR = BASE / "Input resources"
RESULT_DIR = BASE / "Results" / "Iteration_1"

COMPONENTS_CSV = INPUT_DIR / "component_and_logical_visual_ocr_labels.csv"
AGREED_MATRIX = RESULT_DIR / "round_02_jennifer_matrix.csv"
AGREED_EDGES = RESULT_DIR / "round_02_jennifer_edges.csv"
DIEGO_MATRIX = RESULT_DIR / "round_02_diego_matrix.csv"

FINAL_MATRIX = RESULT_DIR / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULT_DIR / "final_connectivity_edges.csv"
FINAL_NODES = RESULT_DIR / "final_connectivity_nodes.csv"
FINAL_UNCERTAIN = RESULT_DIR / "final_uncertain_candidates.csv"
FINAL_VALIDATION = RESULT_DIR / "final_connectivity_validation.json"
FINAL_SUMMARY = RESULT_DIR / "final_connectivity_summary.md"

BUS_NODES = [
    "BUS-4160-A-DIV-I",
    "BUS-4160-B-DIV-II",
    "BUS-480-A",
    "BUS-480-B",
]

UNCERTAIN_OR_EXCLUDED = [
    {
        "candidate": "CONTROL-ROOM-ANNUNCIATION",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Printed along a broad dashed corridor; reviewed as a corridor label rather than a standalone connectivity node.",
    },
    {
        "candidate": "LC-A, LC-B",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Labels mark local load-center/endpoint tap positions at BUS-480-A/B and are represented by direct component-to-bus edges.",
    },
    {
        "candidate": "DIVISION-I-TRAIN-A-SAFETY-POWER, DIVISION-II-TRAIN-B-SAFETY-POWER",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Dashed-region banners describe train boundaries, not electrical connectivity nodes.",
    },
    {
        "candidate": "NORMAL-OFFSITE-FEED-A, NORMAL-OFFSITE-FEED-B, N.O.-TIE",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "Feed/tie annotations describe nearby power paths; the matrix represents the actual named devices and buses.",
    },
    {
        "candidate": "BUS-480-A -- INV-120A",
        "candidate_type": "edge",
        "status": "excluded_uncertain",
        "evidence": "LC-A side-tap geometry clearly supports the charger feed, but no unambiguous direct inverter-to-480-bus landing is visible.",
    },
    {
        "candidate": "BUS-480-B -- INV-120B",
        "candidate_type": "edge",
        "status": "excluded_uncertain",
        "evidence": "LC-B side-tap geometry clearly supports the charger feed, but no unambiguous direct inverter-to-480-bus landing is visible.",
    },
    {
        "candidate": "RPS-A -- MOV-881A, RPS-A -- MOV-742A",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Direct RPS-to-MOV control interpretation would duplicate the visually supported JB-A101-mediated control paths.",
    },
    {
        "candidate": "RPS-B -- MOV-881B, RPS-B -- MOV-742B",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Direct RPS-to-MOV control interpretation would duplicate the visually supported JB-B101-mediated control paths.",
    },
    {
        "candidate": "REC-SOE01 -- JB-B101",
        "candidate_type": "edge",
        "status": "excluded",
        "evidence": "Connection appears to be a broad lower corridor continuation rather than a supported direct edge between named devices.",
    },
    {
        "candidate": "Terminal schedule rows, reference drawing rows, anonymous wire topology points",
        "candidate_type": "node",
        "status": "excluded",
        "evidence": "These are tabular annotations or detected topology endpoints, not named schematic components/buses.",
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


def read_input_labels(node_kind: str) -> list[str]:
    with COMPONENTS_CSV.open(newline="", encoding="utf-8") as handle:
        return [
            row["final_label"]
            for row in csv.DictReader(handle)
            if row.get("node_kind") == node_kind
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
    physical = read_input_labels("physical_component")
    expected_nodes = set(physical) | set(BUS_NODES)
    matrix_pairs = matrix_edge_pairs(nodes, matrix)
    edge_csv_pairs = {edge_pair(row["source"], row["target"]) for row in edge_rows}
    degrees = {node: sum(matrix[index]) for index, node in enumerate(nodes)}
    validation = {
        "node_count": len(nodes),
        "edge_count": len(matrix_pairs),
        "edge_csv_count": len(edge_rows),
        "square": len(matrix) == len(nodes) and all(len(row) == len(nodes) for row in matrix),
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "binary_entries": all(value in (0, 1) for row in matrix for value in row),
        "edge_csv_matches_matrix": matrix_pairs == edge_csv_pairs,
        "physical_component_count_from_input": len(physical),
        "bus_node_count_expected": len(BUS_NODES),
        "expected_node_count": len(expected_nodes),
        "missing_expected_nodes": sorted(expected_nodes - set(nodes)),
        "unexpected_nodes": sorted(set(nodes) - expected_nodes),
        "isolated_nodes": [node for node, degree in degrees.items() if degree == 0],
        "edges_in_matrix_not_csv": sorted(" -- ".join(edge) for edge in matrix_pairs - edge_csv_pairs),
        "edges_in_csv_not_matrix": sorted(" -- ".join(edge) for edge in edge_csv_pairs - matrix_pairs),
        "ground_truth_used": False,
    }
    validation["passes_internal_validation"] = all(
        [
            validation["node_count"] == 54,
            validation["edge_count"] == 56,
            validation["edge_csv_count"] == 56,
            validation["square"],
            validation["symmetric"],
            validation["diagonal_zero"],
            validation["binary_entries"],
            validation["edge_csv_matches_matrix"],
            validation["physical_component_count_from_input"] == 50,
            validation["bus_node_count_expected"] == 4,
            not validation["missing_expected_nodes"],
            not validation["unexpected_nodes"],
        ]
    )
    return validation


def write_nodes(nodes: list[str], matrix: list[list[int]]) -> None:
    physical = set(read_input_labels("physical_component"))
    buses = set(BUS_NODES)
    with FINAL_NODES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "node_kind", "degree", "source"])
        writer.writeheader()
        for index, node in enumerate(nodes):
            if node in physical:
                node_kind = "physical_component"
                source = "component_and_logical_visual_ocr_labels.csv"
            elif node in buses:
                node_kind = "bus"
                source = "raw_schematic_and_label_overlay"
            else:
                node_kind = "unexpected"
                source = "final_matrix"
            writer.writerow(
                {
                    "node": node,
                    "node_kind": node_kind,
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
    summary = f"""# Final Connectivity Summary - Doc 4 Iteration 1

Diego and Jennifer saturated on the Round 02 graph.

- Final nodes: {validation["node_count"]}
- Final edges: {validation["edge_count"]}
- Matrix symmetric: {validation["symmetric"]}
- Diagonal zero: {validation["diagonal_zero"]}
- Node set: 50 OCR physical components plus 4 true power bus rails
- Unexpected nodes: {len(validation["unexpected_nodes"])}
- Missing expected nodes: {len(validation["missing_expected_nodes"])}

The final graph excludes corridor labels, local endpoint labels, banners, feed-note labels, tie-note text, terminal/reference table rows, and anonymous wire topology points. It retains visible named control conductors where supported, JB-mediated MOV control paths, the two charger feeds from the 480 buses, and the lower-confidence BUS-480-A to GND-PLANT ground-reference edge.
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
