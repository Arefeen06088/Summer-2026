from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\5")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_1"

FINAL_MATRIX = RESULTS / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULTS / "final_connectivity_edges.csv"
FINAL_NODES = RESULTS / "final_connectivity_nodes.csv"
FINAL_UNCERTAIN = RESULTS / "final_uncertain_candidates.csv"
FINAL_VALIDATION = RESULTS / "final_connectivity_validation.json"
FINAL_SUMMARY = RESULTS / "final_connectivity_summary.md"


def read_matrix(path: Path) -> tuple[list[str], dict[str, dict[str, int]]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        nodes = header[1:]
        matrix: dict[str, dict[str, int]] = {}
        for row in reader:
            if not row:
                continue
            node = row[0]
            matrix[node] = {col: int(value) for col, value in zip(nodes, row[1:])}
    return nodes, matrix


def read_edges(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def edge_set_from_matrix(nodes: list[str], matrix: dict[str, dict[str, int]]) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            if matrix[a][b] == 1:
                edges.add((a, b) if a < b else (b, a))
    return edges


def canonical_edge(edge: dict[str, str]) -> tuple[str, str]:
    a = edge["source"]
    b = edge["target"]
    return (a, b) if a < b else (b, a)


def read_label_rows() -> list[dict[str, str]]:
    labels_path = INPUT / "component_and_logical_visual_ocr_labels.csv"
    with labels_path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_matrix(nodes: list[str], matrix: dict[str, dict[str, int]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [matrix[node][other] for other in nodes])


def write_edges(edges: list[dict[str, str]], path: Path) -> None:
    fieldnames = ["source", "target", "confidence", "evidence", "final_action"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
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
    label_rows = {row["final_label"]: row for row in read_label_rows()}
    explicit_bus_nodes = {
        "SWGR-21A",
        "SWGR-21B",
        "MCC-21A-480V-3PH",
        "MCC-21B-480V-3PH",
        "DC-BUS-21A",
        "DC-BUS-21B",
    }
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["node", "node_kind", "component_type", "degree", "source"])
        writer.writeheader()
        for node in nodes:
            label = label_rows.get(node, {})
            node_kind = "logical_bus_or_rail" if node in explicit_bus_nodes else "physical_component"
            degree = sum(matrix[node][other] for other in nodes if other != node)
            writer.writerow(
                {
                    "node": node,
                    "node_kind": node_kind,
                    "component_type": label.get("component_type", ""),
                    "degree": degree,
                    "source": "component_and_logical_visual_ocr_labels.csv/raw visual refinement",
                }
            )


def write_uncertain(edges: list[dict[str, str]], path: Path) -> None:
    excluded = [
        {
            "candidate": "MCC-21A / MCC-21B physical enclosure labels",
            "decision": "excluded",
            "reason": "Duplicate enclosure labels for the named MCC 480 V bus rails; final graph keeps the actual rail nodes.",
        },
        {
            "candidate": "RPS-CH-A-CONTROL-LANE / RPS-CH-B-CONTROL-LANE",
            "decision": "excluded",
            "reason": "Route text labels for dashed control wiring, not separate terminal endpoints.",
        },
        {
            "candidate": "VOLTAGE-SIG-A / VOLTAGE-SIG-B",
            "decision": "excluded",
            "reason": "Signal-route labels; direct VT-to-RPS named-device edges preserve the visually supported connectivity.",
        },
        {
            "candidate": "DC-BUS-21A/B -- RPS-PNL-A/B",
            "decision": "excluded",
            "reason": "Dashed terminal drops cross or approach the solid 125 VDC rails without junction dots.",
        },
        {
            "candidate": "CT-21A/B -- FAN-RB21A/B",
            "decision": "excluded",
            "reason": "CT symbols are adjacent to fan feeders but not visibly in series with them; dashed leads route to RPS panels.",
        },
    ]
    medium_edges = [
        {
            "candidate": f"{edge['source']} -- {edge['target']}",
            "decision": "retained_medium_confidence",
            "reason": edge.get("evidence", ""),
        }
        for edge in edges
        if edge.get("confidence", "").lower() == "medium"
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate", "decision", "reason"])
        writer.writeheader()
        writer.writerows(excluded + medium_edges)


def main() -> None:
    source_matrix = RESULTS / "round_02_jennifer_matrix.csv"
    source_edges = RESULTS / "round_02_jennifer_edges.csv"
    diego_matrix = RESULTS / "round_02_diego_matrix.csv"

    nodes, matrix = read_matrix(source_matrix)
    diego_nodes, diego = read_matrix(diego_matrix)
    edges = read_edges(source_edges)

    matrix_edges = edge_set_from_matrix(nodes, matrix)
    csv_edges = {canonical_edge(edge) for edge in edges}

    physical_labels = {
        row["final_label"]
        for row in read_label_rows()
        if row["node_kind"] == "physical_component" and row["final_label"] not in {"MCC-21A", "MCC-21B"}
    }
    selected_bus_nodes = {
        "SWGR-21A",
        "SWGR-21B",
        "MCC-21A-480V-3PH",
        "MCC-21B-480V-3PH",
        "DC-BUS-21A",
        "DC-BUS-21B",
    }
    selected_nodes = physical_labels | selected_bus_nodes

    validation = {
        "node_count": len(nodes),
        "edge_count": len(matrix_edges),
        "edge_csv_count": len(edges),
        "square": len(nodes) == len(matrix),
        "symmetric": all(matrix[a][b] == matrix[b][a] for a in nodes for b in nodes),
        "diagonal_zero": all(matrix[node][node] == 0 for node in nodes),
        "binary_entries": all(matrix[a][b] in {0, 1} for a in nodes for b in nodes),
        "edge_csv_matches_matrix": matrix_edges == csv_edges,
        "diego_jennifer_round2_agree": nodes == diego_nodes and matrix == diego,
        "selected_physical_component_count": len(physical_labels),
        "selected_bus_or_rail_count": len(selected_bus_nodes),
        "expected_node_count_from_blind_policy": len(selected_nodes),
        "missing_selected_nodes": sorted(selected_nodes - set(nodes)),
        "unexpected_nodes": sorted(set(nodes) - selected_nodes),
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
            not validation["missing_selected_nodes"],
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
                "# Final Connectivity Summary - Doc 5 Iteration 1",
                "",
                "Diego and Jennifer saturated on the Round 02 graph.",
                "",
                f"- Final nodes: {validation['node_count']}",
                f"- Final edges: {validation['edge_count']}",
                f"- Matrix symmetric: {validation['symmetric']}",
                f"- Diagonal zero: {validation['diagonal_zero']}",
                "- Node set: 49 selected physical components plus 6 true bus/rail nodes.",
                "- Excluded as non-endpoint labels: train banners, source notes, RPS control-lane route labels, voltage-signal route labels, and anonymous wire topology points.",
                "- Excluded as duplicate enclosure labels: MCC-21A and MCC-21B; the final graph keeps their actual 480 V bus rails.",
                "- Retained medium-confidence named-device control edges: CT/VT to RPS, CB trip path to first relay, RPS to inverter, and JB-B to RPS-B.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
