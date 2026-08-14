from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\5")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_1"

SOURCE_MATRIX = RESULTS / "round_02_jennifer_matrix.csv"
SOURCE_EDGES = RESULTS / "round_02_jennifer_edges.csv"
DIEGO_MATRIX = RESULTS / "round_02_diego_matrix.csv"

FINAL_MATRIX = RESULTS / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULTS / "final_connectivity_edges.csv"
FINAL_NODES = RESULTS / "final_connectivity_nodes.csv"
FINAL_UNCERTAIN = RESULTS / "final_uncertain_candidates.csv"
FINAL_VALIDATION = RESULTS / "final_connectivity_validation.json"
FINAL_SUMMARY = RESULTS / "final_connectivity_summary.md"

LOGICAL_BUS_NODES = {
    "BUS-SY230",
    "BUS-AUX13A",
    "BUS-AUX13B",
    "BUS-NON1",
    "BUS-416A",
    "BUS-416B",
    "BUS-416C",
    "BUS-416D",
}


def read_matrix(path: Path) -> tuple[list[str], dict[str, dict[str, int]]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        nodes = header[1:]
        matrix: dict[str, dict[str, int]] = {}
        for row in reader:
            if row:
                matrix[row[0]] = {col: int(value) for col, value in zip(nodes, row[1:])}
    return nodes, matrix


def read_edges(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_label_rows() -> list[dict[str, str]]:
    with (INPUT / "component_visual_ocr_labels.csv").open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def canonical(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a < b else (b, a)


def edge_set_from_matrix(nodes: list[str], matrix: dict[str, dict[str, int]]) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            if matrix[a][b] == 1:
                edges.add(canonical(a, b))
    return edges


def write_matrix(nodes: list[str], matrix: dict[str, dict[str, int]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [matrix[node][other] for other in nodes])


def write_edges(edges: list[dict[str, str]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "confidence", "evidence", "final_action"])
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "source": edge["source"],
                    "target": edge["target"],
                    "confidence": edge.get("confidence", ""),
                    "evidence": edge.get("evidence", ""),
                    "final_action": edge.get("jennifer_action", "retained_after_saturation_check"),
                }
            )


def write_nodes(nodes: list[str], matrix: dict[str, dict[str, int]], path: Path) -> None:
    labels = {row["final_label"]: row for row in read_label_rows()}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["node", "node_kind", "component_type", "degree", "source"])
        writer.writeheader()
        for node in nodes:
            label = labels.get(node, {})
            writer.writerow(
                {
                    "node": node,
                    "node_kind": "logical_bus_or_rail" if node in LOGICAL_BUS_NODES else "physical_component",
                    "component_type": label.get("component_type", ""),
                    "degree": sum(matrix[node][other] for other in nodes if other != node),
                    "source": "raw schematic plus component_visual_ocr_labels.csv",
                }
            )


def write_uncertain(edges: list[dict[str, str]], path: Path) -> None:
    rows = [
        {
            "candidate": "GND-GRID",
            "decision": "excluded",
            "reason": "Named station ground reference rail with dotted grounding conductors; excluded as protective/reference system rather than final component connectivity.",
        },
        {
            "candidate": "train boundaries, RAT/SAF/ATS route labels, ESF-K labels, cable labels, WN-* points",
            "decision": "excluded",
            "reason": "Context, route, cable, or anonymous topology labels rather than named connectivity endpoints.",
        },
        {
            "candidate": "JB-RLY-A/B fan-out to individual relays",
            "decision": "excluded",
            "reason": "Round 01 high-recall trunk guesses; not direct visible named-device endpoints in the raw schematic.",
        },
        {
            "candidate": "CP-ESFAS-1/2 to UV/LOOP relay weak guesses",
            "decision": "excluded",
            "reason": "Removed in Round 02 because the direct dashed paths were not sufficiently supported as endpoint pairs.",
        },
    ]
    rows.extend(
        {
            "candidate": f"{edge['source']} -- {edge['target']}",
            "decision": "retained_medium_confidence",
            "reason": edge.get("evidence", ""),
        }
        for edge in edges
        if edge.get("confidence", "").lower() == "medium"
    )
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate", "decision", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    nodes, matrix = read_matrix(SOURCE_MATRIX)
    diego_nodes, diego_matrix = read_matrix(DIEGO_MATRIX)
    edges = read_edges(SOURCE_EDGES)
    matrix_edges = edge_set_from_matrix(nodes, matrix)
    csv_edges = {canonical(edge["source"], edge["target"]) for edge in edges}

    physical_nodes = {row["final_label"] for row in read_label_rows() if row["node_kind"] == "physical_component"}
    expected_nodes = physical_nodes | LOGICAL_BUS_NODES

    validation = {
        "node_count": len(nodes),
        "edge_count": len(matrix_edges),
        "edge_csv_count": len(edges),
        "square": len(nodes) == len(matrix),
        "symmetric": all(matrix[a][b] == matrix[b][a] for a in nodes for b in nodes),
        "diagonal_zero": all(matrix[node][node] == 0 for node in nodes),
        "binary_entries": all(matrix[a][b] in {0, 1} for a in nodes for b in nodes),
        "edge_csv_matches_matrix": matrix_edges == csv_edges,
        "diego_jennifer_round2_agree": nodes == diego_nodes and matrix == diego_matrix,
        "selected_physical_component_count": len(physical_nodes),
        "selected_logical_bus_count": len(LOGICAL_BUS_NODES),
        "expected_node_count_from_blind_policy": len(expected_nodes),
        "missing_expected_nodes": sorted(expected_nodes - set(nodes)),
        "unexpected_nodes": sorted(set(nodes) - expected_nodes),
        "isolated_nodes": [node for node in nodes if sum(matrix[node][other] for other in nodes) == 0],
        "edges_in_matrix_not_csv": sorted(matrix_edges - csv_edges),
        "edges_in_csv_not_matrix": sorted(csv_edges - matrix_edges),
        "ground_truth_used": False,
    }
    validation["passes_internal_validation"] = all(
        [
            validation["square"],
            validation["symmetric"],
            validation["diagonal_zero"],
            validation["binary_entries"],
            validation["edge_csv_matches_matrix"],
            validation["diego_jennifer_round2_agree"],
            not validation["missing_expected_nodes"],
            not validation["unexpected_nodes"],
            not validation["isolated_nodes"],
        ]
    )

    write_matrix(nodes, matrix, FINAL_MATRIX)
    write_edges(edges, FINAL_EDGES)
    write_nodes(nodes, matrix, FINAL_NODES)
    write_uncertain(edges, FINAL_UNCERTAIN)
    FINAL_VALIDATION.write_text(json.dumps(validation, indent=2), encoding="utf-8")
    FINAL_SUMMARY.write_text(
        "\n".join(
            [
                "# Final Connectivity Summary - Improved Doc 5 Iteration 1",
                "",
                "Diego and Jennifer saturated on the Round 02 graph.",
                "",
                f"- Final nodes: {validation['node_count']}",
                f"- Final edges: {validation['edge_count']}",
                f"- Matrix symmetric: {validation['symmetric']}",
                f"- Diagonal zero: {validation['diagonal_zero']}",
                "- Node set: 103 named physical components plus 8 true named bus/rail nodes.",
                "- Retained logical nodes: BUS-SY230, BUS-AUX13A, BUS-AUX13B, BUS-NON1, BUS-416A, BUS-416B, BUS-416C, BUS-416D.",
                "- Excluded GND-GRID as a grounding/reference system rather than final component connectivity.",
                "- Excluded contextual labels, route labels, cable labels, anonymous WN-* wire points, and unsupported relay-trunk fan-out guesses.",
                "- Remaining medium-confidence retained edges are documented in final_uncertain_candidates.csv.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
