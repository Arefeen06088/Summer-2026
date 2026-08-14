import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


DIEGO_ROUND_1_NODES = [
    "GRID-1",
    "AUX-TR-1A",
    "CB-101",
    "EDG-1A",
    "CB-DG1A",
    "BUS-416A",
    "BUS-TIE-41",
    "BUS-416B",
    "CB-102",
    "AUX-TR-1B",
    "GRID-2",
    "CB-DG1B",
    "EDG-1B",
    "TR-480A1",
    "CB-480A1",
    "MCC-480A1",
    "TR-480A2",
    "CB-480A2",
    "MCC-480A2",
    "GND-A",
    "GND-1E",
    "GND-B",
    "CB-CHG-A",
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-A",
    "INV-120A",
    "BUS-120A",
    "CB-CHG-B",
    "CHGR-125B",
    "BAT-125B",
    "DC-BUS-B",
    "INV-120B",
    "BUS-120B",
    "TR-480B1",
    "CB-480B1",
    "MCC-480B1",
    "TR-480B2",
    "CB-480B2",
    "MCC-480B2",
    "FDB-A1",
    "CB-SI-A1",
    "PUMP-SI-A1",
    "CB-RHR-A1",
    "PUMP-RHR-A1",
    "CB-CCW-A1",
    "PUMP-CCW-A1",
    "CB-FAN-A1",
    "FAN-CR-A1",
    "CB-MOV-A101",
    "VALVE-SI-A101",
    "CB-MOV-A102",
    "VALVE-RHR-A102",
    "FDB-A2",
    "CB-CS-A2",
    "PUMP-CS-A2",
    "CB-SW-A2",
    "PUMP-SW-A2",
    "CB-AFW-A2",
    "PUMP-AFW-A2",
    "CB-FAN-A2",
    "FAN-EB-A2",
    "CB-MOV-A201",
    "VALVE-CCW-A201",
    "CB-HTR-A2",
    "HTR-BAY-A2",
    "FDB-B1",
    "CB-SI-B1",
    "PUMP-SI-B1",
    "CB-RHR-B1",
    "PUMP-RHR-B1",
    "CB-CCW-B1",
    "PUMP-CCW-B1",
    "CB-FAN-B1",
    "FAN-CR-B1",
    "CB-MOV-B101",
    "VALVE-SI-B101",
    "CB-MOV-B102",
    "VALVE-RHR-B102",
    "FDB-B2",
    "CB-CS-B2",
    "PUMP-CS-B2",
    "CB-SW-B2",
    "PUMP-SW-B2",
    "CB-FAN-B2",
    "FAN-EB-B2",
    "CB-MOV-B201",
    "VALVE-CCW-B201",
    "CB-HTR-B2",
    "HTR-BAY-B2",
    "INST-PT-A",
    "INST-LT-A",
    "RELAY-K27A",
    "PANEL-RPS-A",
    "PANEL-ESF-A",
    "JB-A401",
    "PANEL-RPS-B",
    "RELAY-K27B",
    "INST-PT-B",
    "INST-LT-B",
    "PANEL-ESF-B",
    "JB-B501",
]


FINAL_NODES = [node for node in DIEGO_ROUND_1_NODES if node not in {"GND-A", "GND-B"}]


FINAL_EDGES = [
    ("GRID-1", "AUX-TR-1A"),
    ("AUX-TR-1A", "CB-101"),
    ("EDG-1A", "CB-DG1A"),
    ("CB-DG1A", "BUS-416A"),
    ("BUS-416A", "TR-480A1"),
    ("BUS-416A", "TR-480A2"),
    ("BUS-416A", "CB-CHG-A"),
    ("BUS-416A", "BUS-TIE-41"),
    ("BUS-TIE-41", "BUS-416B"),
    ("BUS-416B", "CB-CHG-B"),
    ("BUS-416B", "TR-480B1"),
    ("BUS-416B", "TR-480B2"),
    ("BUS-416B", "CB-DG1B"),
    ("CB-DG1B", "EDG-1B"),
    ("GRID-2", "AUX-TR-1B"),
    ("AUX-TR-1B", "CB-102"),
    ("TR-480A1", "CB-480A1"),
    ("CB-480A1", "MCC-480A1"),
    ("MCC-480A1", "FDB-A1"),
    ("TR-480A2", "CB-480A2"),
    ("CB-480A2", "MCC-480A2"),
    ("MCC-480A2", "FDB-A2"),
    ("TR-480B1", "CB-480B1"),
    ("CB-480B1", "MCC-480B1"),
    ("MCC-480B1", "FDB-B1"),
    ("TR-480B2", "CB-480B2"),
    ("CB-480B2", "MCC-480B2"),
    ("MCC-480B2", "FDB-B2"),
    ("CB-CHG-A", "CHGR-125A"),
    ("CHGR-125A", "DC-BUS-A"),
    ("BAT-125A", "DC-BUS-A"),
    ("DC-BUS-A", "INV-120A"),
    ("INV-120A", "BUS-120A"),
    ("CB-CHG-B", "CHGR-125B"),
    ("CHGR-125B", "DC-BUS-B"),
    ("BAT-125B", "DC-BUS-B"),
    ("DC-BUS-B", "INV-120B"),
    ("INV-120B", "BUS-120B"),
    ("FDB-A1", "CB-SI-A1"),
    ("CB-SI-A1", "PUMP-SI-A1"),
    ("FDB-A1", "CB-RHR-A1"),
    ("CB-RHR-A1", "PUMP-RHR-A1"),
    ("FDB-A1", "CB-CCW-A1"),
    ("CB-CCW-A1", "PUMP-CCW-A1"),
    ("FDB-A1", "CB-FAN-A1"),
    ("CB-FAN-A1", "FAN-CR-A1"),
    ("FDB-A1", "CB-MOV-A101"),
    ("CB-MOV-A101", "VALVE-SI-A101"),
    ("FDB-A1", "CB-MOV-A102"),
    ("CB-MOV-A102", "VALVE-RHR-A102"),
    ("FDB-A2", "CB-CS-A2"),
    ("CB-CS-A2", "PUMP-CS-A2"),
    ("FDB-A2", "CB-SW-A2"),
    ("CB-SW-A2", "PUMP-SW-A2"),
    ("FDB-A2", "CB-AFW-A2"),
    ("CB-AFW-A2", "PUMP-AFW-A2"),
    ("FDB-A2", "CB-FAN-A2"),
    ("CB-FAN-A2", "FAN-EB-A2"),
    ("FDB-A2", "CB-MOV-A201"),
    ("CB-MOV-A201", "VALVE-CCW-A201"),
    ("FDB-A2", "CB-HTR-A2"),
    ("CB-HTR-A2", "HTR-BAY-A2"),
    ("FDB-B1", "CB-SI-B1"),
    ("CB-SI-B1", "PUMP-SI-B1"),
    ("FDB-B1", "CB-RHR-B1"),
    ("CB-RHR-B1", "PUMP-RHR-B1"),
    ("FDB-B1", "CB-CCW-B1"),
    ("CB-CCW-B1", "PUMP-CCW-B1"),
    ("FDB-B1", "CB-FAN-B1"),
    ("CB-FAN-B1", "FAN-CR-B1"),
    ("FDB-B1", "CB-MOV-B101"),
    ("CB-MOV-B101", "VALVE-SI-B101"),
    ("FDB-B1", "CB-MOV-B102"),
    ("CB-MOV-B102", "VALVE-RHR-B102"),
    ("FDB-B2", "CB-CS-B2"),
    ("CB-CS-B2", "PUMP-CS-B2"),
    ("FDB-B2", "CB-SW-B2"),
    ("CB-SW-B2", "PUMP-SW-B2"),
    ("FDB-B2", "CB-FAN-B2"),
    ("CB-FAN-B2", "FAN-EB-B2"),
    ("FDB-B2", "CB-MOV-B201"),
    ("CB-MOV-B201", "VALVE-CCW-B201"),
    ("FDB-B2", "CB-HTR-B2"),
    ("CB-HTR-B2", "HTR-BAY-B2"),
    ("BUS-120A", "PANEL-RPS-A"),
    ("INST-PT-A", "PANEL-RPS-A"),
    ("INST-LT-A", "PANEL-RPS-A"),
    ("RELAY-K27A", "PANEL-RPS-A"),
    ("RELAY-K27A", "PANEL-ESF-A"),
    ("PANEL-ESF-A", "JB-A401"),
    ("BUS-120B", "PANEL-RPS-B"),
    ("PANEL-RPS-B", "RELAY-K27B"),
    ("INST-PT-B", "PANEL-RPS-B"),
    ("INST-LT-B", "PANEL-RPS-B"),
    ("RELAY-K27B", "PANEL-ESF-B"),
    ("PANEL-ESF-B", "JB-B501"),
]


DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES = [
    ("CB-101", "BUS-416A"),
    ("CB-102", "BUS-416B"),
    ("GND-A", "GND-1E"),
    ("GND-B", "GND-1E"),
]


ROUND_NOTES = {
    "round_01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "matrix_policy": "Includes Diego's confident edges plus plausible/uncertain extras as 1s; uncertain extras are also listed separately.",
        "uncertain_edges_included": DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES,
    },
    "round_01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer",
        "matrix_policy": "Accepted visual edges only; removed reference labels GND-A/GND-B and visibly gapped source-breaker-to-bus stubs.",
        "removed_edges": DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES,
    },
    "round_02_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "matrix_policy": "Same as Jennifer round 1 after Diego agreement.",
    },
    "round_02_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "matrix_policy": "Same as Jennifer round 1 after final agreement.",
    },
    "final": {
        "agent": "main",
        "role": "saturated consensus",
        "matrix_policy": "Final accepted visual connectivity matrix.",
    },
}


def validate(nodes, edges):
    seen = set()
    for edge in edges:
        if edge[0] == edge[1]:
            raise ValueError(f"self-loop: {edge}")
        if edge[0] not in nodes or edge[1] not in nodes:
            raise ValueError(f"edge references missing node: {edge}")
        key = tuple(sorted(edge))
        if key in seen:
            raise ValueError(f"duplicate undirected edge: {edge}")
        seen.add(key)
    if len(nodes) != len(set(nodes)):
        raise ValueError("duplicate node label")


def write_nodes(prefix, nodes):
    with (RESULTS / f"{prefix}_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(prefix, edges):
    with (RESULTS / f"{prefix}_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        for source, target in edges:
            writer.writerow([source, target])


def write_matrix(prefix, nodes, edges):
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in edges:
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with (RESULTS / f"{prefix}_connectivity_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)
    return matrix


def write_report(prefix, nodes, edges):
    note = ROUND_NOTES[prefix]
    payload = {
        "document": "3",
        "iteration": 1,
        "round": prefix,
        "node_count": len(nodes),
        "edge_count": len(edges),
        **note,
    }
    with (RESULTS / f"{prefix}_report.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_outputs(prefix, nodes, edges):
    validate(nodes, edges)
    write_nodes(prefix, nodes)
    write_edges(prefix, edges)
    matrix = write_matrix(prefix, nodes, edges)
    write_report(prefix, nodes, edges)
    return matrix


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)

    diego_edges = FINAL_EDGES + DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES
    write_outputs("round_01_diego", DIEGO_ROUND_1_NODES, diego_edges)

    for prefix in ["round_01_jennifer", "round_02_diego", "round_02_jennifer", "final"]:
        write_outputs(prefix, FINAL_NODES, FINAL_EDGES)

    summary_rows = [
        ["document", "iteration", "round", "nodes", "edges", "matrix_file"],
        ["3", "1", "round_01_diego", len(DIEGO_ROUND_1_NODES), len(diego_edges), "round_01_diego_connectivity_matrix.csv"],
        ["3", "1", "round_01_jennifer", len(FINAL_NODES), len(FINAL_EDGES), "round_01_jennifer_connectivity_matrix.csv"],
        ["3", "1", "round_02_diego", len(FINAL_NODES), len(FINAL_EDGES), "round_02_diego_connectivity_matrix.csv"],
        ["3", "1", "round_02_jennifer", len(FINAL_NODES), len(FINAL_EDGES), "round_02_jennifer_connectivity_matrix.csv"],
        ["3", "1", "final", len(FINAL_NODES), len(FINAL_EDGES), "final_connectivity_matrix.csv"],
    ]
    with (RESULTS / "round_matrix_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(summary_rows)


if __name__ == "__main__":
    main()
