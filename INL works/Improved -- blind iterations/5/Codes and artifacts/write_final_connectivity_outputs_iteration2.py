from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\5")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_2"

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
        matrix = {}
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


def matrix_edges(nodes: list[str], matrix: dict[str, dict[str, int]]) -> set[tuple[str, str]]:
    out = set()
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            if matrix[a][b] == 1:
                out.add(canonical(a, b))
    return out


def write_matrix(nodes: list[str], matrix: dict[str, dict[str, int]]) -> None:
    with FINAL_MATRIX.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [matrix[node][other] for other in nodes])


def write_edges(edges: list[dict[str, str]]) -> None:
    with FINAL_EDGES.open("w", newline="", encoding="utf-8") as f:
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


def write_nodes(nodes: list[str], matrix: dict[str, dict[str, int]]) -> None:
    labels = {row["final_label"]: row for row in read_label_rows()}
    with FINAL_NODES.open("w", newline="", encoding="utf-8") as f:
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


def write_uncertain(edges: list[dict[str, str]]) -> None:
    rows = [
        {
            "candidate": "GND-GRID",
            "decision": "excluded",
            "reason": "Station grounding/reference rail; excluded from the final component connectivity matrix.",
        },
        {
            "candidate": "JB-RLY-A/B fan-out to K relays",
            "decision": "excluded",
            "reason": "Broad dashed relay-power/control trunk, not direct named endpoint pairs to individual K relays.",
        },
        {
            "candidate": "BUS-AUX13B -- BUS-NON1",
            "decision": "excluded",
            "reason": "Raw BUS-NON1 geometry supports the left BUS-AUX13A tap and TR-SAF-C termination, not a mirrored BUS-AUX13B tap.",
        },
        {
            "candidate": "context/route labels and WN-* points",
            "decision": "excluded",
            "reason": "Train/division banners, RAT/SAF/ATS route labels, ESF-K text, cable labels, drawing notes, and anonymous wire points are not matrix endpoints.",
        },
    ]
    for edge in edges:
        if edge.get("confidence", "").lower() == "medium":
            rows.append(
                {
                    "candidate": f"{edge['source']} -- {edge['target']}",
                    "decision": "retained_medium_confidence",
                    "reason": edge.get("evidence", ""),
                }
            )
    with FINAL_UNCERTAIN.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate", "decision", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    nodes, matrix = read_matrix(SOURCE_MATRIX)
    diego_nodes, diego_matrix = read_matrix(DIEGO_MATRIX)
    edges = read_edges(SOURCE_EDGES)
    edge_set = matrix_edges(nodes, matrix)
    csv_edge_set = {canonical(edge["source"], edge["target"]) for edge in edges}

    physical_nodes = {row["final_label"] for row in read_label_rows() if row["node_kind"] == "physical_component"}
    expected_nodes = physical_nodes | LOGICAL_BUS_NODES

    validation = {
        "node_count": len(nodes),
        "edge_count": len(edge_set),
        "edge_csv_count": len(edges),
        "square": len(nodes) == len(matrix),
        "symmetric": all(matrix[a][b] == matrix[b][a] for a in nodes for b in nodes),
        "diagonal_zero": all(matrix[node][node] == 0 for node in nodes),
        "binary_entries": all(matrix[a][b] in {0, 1} for a in nodes for b in nodes),
        "edge_csv_matches_matrix": edge_set == csv_edge_set,
        "diego_jennifer_round2_agree": nodes == diego_nodes and matrix == diego_matrix,
        "selected_physical_component_count": len(physical_nodes),
        "selected_logical_bus_count": len(LOGICAL_BUS_NODES),
        "expected_node_count_from_blind_policy": len(expected_nodes),
        "missing_expected_nodes": sorted(expected_nodes - set(nodes)),
        "unexpected_nodes": sorted(set(nodes) - expected_nodes),
        "isolated_nodes": [node for node in nodes if sum(matrix[node][other] for other in nodes) == 0],
        "edges_in_matrix_not_csv": sorted(edge_set - csv_edge_set),
        "edges_in_csv_not_matrix": sorted(csv_edge_set - edge_set),
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

    write_matrix(nodes, matrix)
    write_edges(edges)
    write_nodes(nodes, matrix)
    write_uncertain(edges)
    FINAL_VALIDATION.write_text(json.dumps(validation, indent=2), encoding="utf-8")
    FINAL_SUMMARY.write_text(
        "\n".join(
            [
                "# Final Connectivity Summary - Improved Doc 5 Iteration 2",
                "",
                "Diego and Jennifer saturated on the Round 02 graph.",
                "",
                f"- Final nodes: {validation['node_count']}",
                f"- Final edges: {validation['edge_count']}",
                f"- Matrix symmetric: {validation['symmetric']}",
                f"- Diagonal zero: {validation['diagonal_zero']}",
                "- Node set: 103 named physical components plus 8 true named bus/rail nodes.",
                "- Retained logical nodes: BUS-SY230, BUS-AUX13A, BUS-AUX13B, BUS-NON1, BUS-416A, BUS-416B, BUS-416C, BUS-416D.",
                "- Excluded GND-GRID, contextual labels, route labels, cable labels, WN-* points, and JB relay fan-out trunk guesses.",
                "- Final refinements include BUS-NON1--TR-SAF-C, MCC-fed CCW pumps, BUS-416C/D UV sensing, and exclusion of JB-RLY-to-K fan-outs.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
