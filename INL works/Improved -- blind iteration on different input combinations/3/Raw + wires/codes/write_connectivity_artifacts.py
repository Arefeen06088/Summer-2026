from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


DIEGO_R1_NODES = [
    "GRID-1", "AUX-TR-1A", "CB-101", "BUS-416A", "EDG-1A", "CB-DG1A",
    "TR-480A1", "CB-480A1", "MCC-480A1", "TR-480A2", "CB-480A2",
    "MCC-480A2", "BUS-TIE-41", "BUS-416B", "CB-102", "AUX-TR-1B",
    "GRID-2", "EDG-1B", "CB-DG1B", "TR-480B1", "CB-480B1", "MCC-480B1",
    "TR-480B2", "CB-480B2", "MCC-480B2", "CB-CHG-A", "CHGR-125A",
    "BAT-125A", "DC-BUS-A", "INV-120A", "BUS-120A", "120A-CNTRL",
    "CB-CHG-B", "CHGR-125B", "BAT-125B", "DC-BUS-B", "INV-120B",
    "BUS-120B", "120B-CNTRL", "FDB-A1", "CB-SI-A1", "PUMP-SI-A1",
    "CB-RHR-A1", "PUMP-RHR-A1", "CB-CCW-A1", "PUMP-CCW-A1",
    "CB-FAN-A1", "FAN-CR-A1", "CB-MOV-A101", "VALVE-SI-A101",
    "CB-MOV-A102", "VALVE-RHR-A102", "FDB-A2", "CB-CS-A2", "PUMP-CS-A2",
    "CB-SW-A2", "PUMP-SW-A2", "CB-AFW-A2", "PUMP-AFW-A2", "CB-FAN-A2",
    "FAN-EB-A2", "CB-MOV-A201", "VALVE-CCW-A201", "CB-HTR-A2",
    "HTR-BAY-A2", "FDB-B1", "CB-SI-B1", "PUMP-SI-B1", "CB-RHR-B1",
    "PUMP-RHR-B1", "CB-CCW-B1", "PUMP-CCW-B1", "CB-FAN-B1", "FAN-CR-B1",
    "CB-MOV-B101", "VALVE-SI-B101", "CB-MOV-B102", "VALVE-RHR-B102",
    "FDB-B2", "CB-CS-B2", "PUMP-CS-B2", "CB-SW-B2", "PUMP-SW-B2",
    "CB-FAN-B2", "FAN-EB-B2", "CB-MOV-B201", "VALVE-CCW-B201",
    "CB-HTR-B2", "HTR-BAY-B2", "INST-PT-A", "INST-LT-A", "RELAY-K27A",
    "PANEL-RPS-A", "PANEL-ESF-A", "JB-A401", "INST-PT-B", "INST-LT-B",
    "RELAY-K27B", "PANEL-RPS-B", "PANEL-ESF-B", "JB-B501",
]


FINAL_NODES = [
    "GRID-1", "AUX-TR-1A", "CB-101", "BUS-416A", "EDG-1A", "CB-DG1A",
    "TR-480A1", "CB-480A1", "MCC-480A1", "TR-480A2", "CB-480A2",
    "MCC-480A2", "BUS-TIE-41", "GND-1E", "BUS-416B", "CB-102",
    "AUX-TR-1B", "GRID-2", "EDG-1B", "CB-DG1B", "TR-480B1", "CB-480B1",
    "MCC-480B1", "TR-480B2", "CB-480B2", "MCC-480B2", "CB-CHG-A",
    "CHGR-125A", "BAT-125A", "DC-BUS-A", "INV-120A", "BUS-120A",
    "CB-CHG-B", "CHGR-125B", "BAT-125B", "DC-BUS-B", "INV-120B",
    "BUS-120B", "FDB-A1", "CB-SI-A1", "PUMP-SI-A1", "CB-RHR-A1",
    "PUMP-RHR-A1", "CB-CCW-A1", "PUMP-CCW-A1", "CB-FAN-A1", "FAN-CR-A1",
    "CB-MOV-A101", "VALVE-SI-A101", "CB-MOV-A102", "VALVE-RHR-A102",
    "FDB-A2", "CB-CS-A2", "PUMP-CS-A2", "CB-SW-A2", "PUMP-SW-A2",
    "CB-AFW-A2", "PUMP-AFW-A2", "CB-FAN-A2", "FAN-EB-A2",
    "CB-MOV-A201", "VALVE-CCW-A201", "CB-HTR-A2", "HTR-BAY-A2",
    "FDB-B1", "CB-SI-B1", "PUMP-SI-B1", "CB-RHR-B1", "PUMP-RHR-B1",
    "CB-CCW-B1", "PUMP-CCW-B1", "CB-FAN-B1", "FAN-CR-B1", "CB-MOV-B101",
    "VALVE-SI-B101", "CB-MOV-B102", "VALVE-RHR-B102", "FDB-B2",
    "CB-CS-B2", "PUMP-CS-B2", "CB-SW-B2", "PUMP-SW-B2", "CB-FAN-B2",
    "FAN-EB-B2", "CB-MOV-B201", "VALVE-CCW-B201", "CB-HTR-B2",
    "HTR-BAY-B2", "INST-PT-A", "INST-LT-A", "RELAY-K27A", "PANEL-RPS-A",
    "PANEL-ESF-A", "JB-A401", "INST-PT-B", "INST-LT-B", "RELAY-K27B",
    "PANEL-RPS-B", "PANEL-ESF-B", "JB-B501",
]


def expand_chain(*names: str) -> list[tuple[str, str]]:
    return list(zip(names, names[1:]))


COMMON_FEEDER_EDGES = [
    *expand_chain("BUS-416A", "TR-480A1", "CB-480A1", "MCC-480A1"),
    *expand_chain("BUS-416A", "TR-480A2", "CB-480A2", "MCC-480A2"),
    *expand_chain("BUS-416A", "BUS-TIE-41", "BUS-416B"),
    *expand_chain("BUS-416B", "TR-480B1", "CB-480B1", "MCC-480B1"),
    *expand_chain("BUS-416B", "TR-480B2", "CB-480B2", "MCC-480B2"),
    *expand_chain("BUS-416A", "CB-CHG-A", "CHGR-125A", "DC-BUS-A"),
    ("BAT-125A", "DC-BUS-A"),
    *expand_chain("DC-BUS-A", "INV-120A", "BUS-120A"),
    *expand_chain("BUS-416B", "CB-CHG-B", "CHGR-125B", "DC-BUS-B"),
    ("BAT-125B", "DC-BUS-B"),
    *expand_chain("DC-BUS-B", "INV-120B", "BUS-120B"),
]


LOAD_EDGES = [
    ("MCC-480A1", "FDB-A1"),
    *expand_chain("FDB-A1", "CB-SI-A1", "PUMP-SI-A1"),
    *expand_chain("FDB-A1", "CB-RHR-A1", "PUMP-RHR-A1"),
    *expand_chain("FDB-A1", "CB-CCW-A1", "PUMP-CCW-A1"),
    *expand_chain("FDB-A1", "CB-FAN-A1", "FAN-CR-A1"),
    *expand_chain("FDB-A1", "CB-MOV-A101", "VALVE-SI-A101"),
    *expand_chain("FDB-A1", "CB-MOV-A102", "VALVE-RHR-A102"),
    ("MCC-480A2", "FDB-A2"),
    *expand_chain("FDB-A2", "CB-CS-A2", "PUMP-CS-A2"),
    *expand_chain("FDB-A2", "CB-SW-A2", "PUMP-SW-A2"),
    *expand_chain("FDB-A2", "CB-AFW-A2", "PUMP-AFW-A2"),
    *expand_chain("FDB-A2", "CB-FAN-A2", "FAN-EB-A2"),
    *expand_chain("FDB-A2", "CB-MOV-A201", "VALVE-CCW-A201"),
    *expand_chain("FDB-A2", "CB-HTR-A2", "HTR-BAY-A2"),
    ("MCC-480B1", "FDB-B1"),
    *expand_chain("FDB-B1", "CB-SI-B1", "PUMP-SI-B1"),
    *expand_chain("FDB-B1", "CB-RHR-B1", "PUMP-RHR-B1"),
    *expand_chain("FDB-B1", "CB-CCW-B1", "PUMP-CCW-B1"),
    *expand_chain("FDB-B1", "CB-FAN-B1", "FAN-CR-B1"),
    *expand_chain("FDB-B1", "CB-MOV-B101", "VALVE-SI-B101"),
    *expand_chain("FDB-B1", "CB-MOV-B102", "VALVE-RHR-B102"),
    ("MCC-480B2", "FDB-B2"),
    *expand_chain("FDB-B2", "CB-CS-B2", "PUMP-CS-B2"),
    *expand_chain("FDB-B2", "CB-SW-B2", "PUMP-SW-B2"),
    *expand_chain("FDB-B2", "CB-FAN-B2", "FAN-EB-B2"),
    *expand_chain("FDB-B2", "CB-MOV-B201", "VALVE-CCW-B201"),
    *expand_chain("FDB-B2", "CB-HTR-B2", "HTR-BAY-B2"),
]


RPS_ESF_EDGES = [
    ("INST-PT-A", "PANEL-RPS-A"),
    ("INST-LT-A", "PANEL-RPS-A"),
    ("RELAY-K27A", "PANEL-RPS-A"),
    ("RELAY-K27A", "PANEL-ESF-A"),
    ("PANEL-ESF-A", "JB-A401"),
    ("INST-PT-B", "PANEL-RPS-B"),
    ("INST-LT-B", "PANEL-RPS-B"),
    ("RELAY-K27B", "PANEL-RPS-B"),
    ("RELAY-K27B", "PANEL-ESF-B"),
    ("PANEL-ESF-B", "JB-B501"),
]


DIEGO_R1_EDGES = [
    *expand_chain("GRID-1", "AUX-TR-1A", "CB-101", "BUS-416A"),
    *expand_chain("EDG-1A", "CB-DG1A", "BUS-416A"),
    *COMMON_FEEDER_EDGES,
    *expand_chain("BUS-416B", "CB-DG1B", "EDG-1B"),
    *expand_chain("BUS-416B", "CB-102", "AUX-TR-1B", "GRID-2"),
    *expand_chain("BUS-120A", "120A-CNTRL", "PANEL-RPS-A"),
    *expand_chain("BUS-120B", "120B-CNTRL", "PANEL-RPS-B"),
    *LOAD_EDGES,
    *RPS_ESF_EDGES,
]


FINAL_EDGES = [
    *expand_chain("GRID-1", "AUX-TR-1A", "CB-101"),
    *expand_chain("EDG-1A", "CB-DG1A", "BUS-416A"),
    *COMMON_FEEDER_EDGES,
    *expand_chain("BUS-416B", "CB-DG1B", "EDG-1B"),
    *expand_chain("CB-102", "AUX-TR-1B", "GRID-2"),
    ("BUS-120A", "PANEL-RPS-A"),
    ("BUS-120B", "PANEL-RPS-B"),
    *LOAD_EDGES,
    *RPS_ESF_EDGES,
]


ROUNDS = {
    "round1_diego": {
        "agent": "Diego",
        "summary": "High-recall first pass. Included two source-to-bus edges and promoted 120A/120B control-run labels to nodes.",
        "nodes": DIEGO_R1_NODES,
        "edges": DIEGO_R1_EDGES,
    },
    "round1_jennifer": {
        "agent": "Jennifer",
        "summary": "Precision review. Removed 120A/120B run labels as nodes, added GND-1E, excluded source-gap and ground-label edges.",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
    "round2_diego": {
        "agent": "Diego",
        "summary": "Narrow recheck. Accepted Jennifer's 96-edge set and rejected the two source-gap and two ground-label uncertainties.",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
    "round2_jennifer_final": {
        "agent": "Jennifer",
        "summary": "Final precision saturation. Kept GND-1E as a visible zero-degree node; no visually supported edge was added.",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
}


def normalize_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    normalized: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for a, b in edges:
        key = tuple(sorted((a, b)))
        if key not in seen:
            seen.add(key)
            normalized.append((a, b))
    return normalized


def matrix_for(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    idx = {name: i for i, name in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in normalize_edges(edges):
        if a not in idx or b not in idx:
            raise ValueError(f"Edge has unknown endpoint: {a!r} -- {b!r}")
        if a == b:
            raise ValueError(f"Self-loop not expected: {a!r}")
        ia, ib = idx[a], idx[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    return matrix


def qa_for(nodes: list[str], edges: list[tuple[str, str]]) -> dict:
    matrix = matrix_for(nodes, edges)
    degree = Counter()
    for a, b in normalize_edges(edges):
        degree[a] += 1
        degree[b] += 1
    duplicates = [item for item, count in Counter(map(lambda e: tuple(sorted(e)), edges)).items() if count > 1]
    return {
        "node_count": len(nodes),
        "edge_count": len(normalize_edges(edges)),
        "matrix_rows": len(matrix),
        "matrix_columns": len(matrix[0]) if matrix else 0,
        "duplicate_edges": duplicates,
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "isolated_nodes": [node for node in nodes if degree[node] == 0],
    }


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = matrix_for(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        for a, b in normalize_edges(edges):
            writer.writerow([a, b])


def write_adjacency(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    adjacency: dict[str, list[str]] = {node: [] for node in nodes}
    for a, b in normalize_edges(edges):
        adjacency[a].append(b)
        adjacency[b].append(a)
    for values in adjacency.values():
        values.sort()
    path.write_text(json.dumps(adjacency, indent=2), encoding="utf-8")


def write_rounds_summary(path: Path) -> None:
    lines = [
        "# Document 3 Connectivity Extraction Rounds",
        "",
        "Scope: include visually supported power, DC power, control/interlock, instrument-signal, and ground-reference links between accepted real nodes. Do not promote gray run labels unless they are accepted as logical nodes.",
        "",
    ]
    for name, data in ROUNDS.items():
        qa = qa_for(data["nodes"], data["edges"])
        lines.extend([
            f"## {name} ({data['agent']})",
            data["summary"],
            f"- Nodes: {qa['node_count']}",
            f"- Edges: {qa['edge_count']}",
            f"- Isolated nodes: {', '.join(qa['isolated_nodes']) if qa['isolated_nodes'] else 'none'}",
            "",
        ])
    lines.extend([
        "## Final Ambiguity Decisions",
        "- `CB-101--BUS-416A`: excluded; source stub stops above the bus with no visually supported terminal connection.",
        "- `BUS-416B--CB-102`: excluded; source stub stops above the bus with no visually supported terminal connection.",
        "- `120A-CNTRL` and `120B-CNTRL`: excluded as nodes; treated as gray control-run labels, with direct accepted edges from `BUS-120A/B` to `PANEL-RPS-A/B`.",
        "- `GND-A` and `GND-B`: excluded as matrix nodes; treated as gray ground-reference labels.",
        "- `GND-1E`: retained as a visible ground symbol/node, but zero-degree because no accepted real-node edge is visually supported without promoting `GND-A/B` or inventing a link.",
        "- `AFW-B2`: excluded; no visible pair is present.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    qa_all = {}
    for name, data in ROUNDS.items():
        nodes = data["nodes"]
        edges = data["edges"]
        qa = qa_for(nodes, edges)
        qa_all[name] = qa
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)
        write_nodes(RESULTS / f"{name}_nodes.csv", nodes)
        write_edges(RESULTS / f"{name}_edges.csv", edges)

    write_matrix(RESULTS / "final_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_nodes(RESULTS / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_adjacency(RESULTS / "final_adjacency.json", FINAL_NODES, FINAL_EDGES)
    write_rounds_summary(RESULTS / "rounds_summary.md")
    (RESULTS / "qa_summary.json").write_text(json.dumps(qa_all, indent=2), encoding="utf-8")

    final_qa = qa_for(FINAL_NODES, FINAL_EDGES)
    if not final_qa["symmetric"] or not final_qa["diagonal_zero"]:
        raise SystemExit(f"Final matrix QA failed: {final_qa}")
    print(json.dumps({"final": final_qa}, indent=2))


if __name__ == "__main__":
    main()
