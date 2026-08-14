from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from draft_doc5_model import CONTROL_CANDIDATES, NODES, SOLID_EDGES, chain


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


DIEGO_R1_GROUND_CANDIDATES = [
    ("GND-GRID", "GSU-1"),
    ("GND-GRID", "BUS-SY230"),
    ("GND-GRID", "TR-RAT-1A"),
    ("GND-GRID", "TR-RAT-1B"),
    ("GND-GRID", "LC-480A"),
    ("GND-GRID", "LC-480B"),
    ("GND-GRID", "LC-480C"),
    ("GND-GRID", "LC-480D"),
    ("GND-GRID", "MCC-1A2"),
    ("GND-GRID", "MCC-1B2"),
    ("GND-GRID", "MCC-1C1"),
    ("GND-GRID", "MCC-1D2"),
    ("GND-GRID", "PUMP-CCW-A"),
    ("GND-GRID", "PUMP-CCW-B"),
    ("GND-GRID", "PUMP-RHR-A"),
    ("GND-GRID", "FAN-CRHV-A"),
    ("GND-GRID", "FAN-CRHV-B"),
    ("GND-GRID", "HTR-BATRM-A"),
    ("GND-GRID", "HTR-BATRM-B"),
    ("GND-GRID", "UPS-PNL-A"),
    ("GND-GRID", "INV-UPS-A"),
    ("GND-GRID", "BAT-48V-A"),
    ("GND-GRID", "JB-RLY-B"),
    ("GND-GRID", "BAT-48V-B"),
    ("GND-GRID", "UPS-PNL-B"),
    ("GND-GRID", "INV-UPS-B"),
    ("GND-GRID", "INST-NSSS-A"),
    ("GND-GRID", "INST-NSSS-B"),
]


JENNIFER_R1_EDGES = [
    *chain("GRID-N230", "ISO-230A", "BRK-2301", "BUS-SY230"),
    *chain("GRID-S230", "ISO-230B", "BRK-2302", "BUS-SY230"),
    *chain("GEN-G101", "GSU-1", "BUS-SY230"),
    *chain("BUS-SY230", "TR-RAT-1A", "CB-AUX-A", "BUS-AUX13A"),
    *chain("BUS-SY230", "TR-UAT-1A", "CB-AUX-A"),
    *chain("BUS-SY230", "TR-RAT-1B", "CB-AUX-B", "BUS-AUX13B"),
    *chain("BUS-SY230", "TR-UAT-1B", "CB-AUX-B"),
    *chain("BUS-AUX13A", "CB-TIE13", "BUS-AUX13B"),
    *chain("BUS-AUX13A", "BUS-NON1", "TR-SAF-C"),
    ("BUS-AUX13A", "TR-SAF-A"),
    ("BUS-AUX13A", "TR-SAF-B"),
    ("BUS-AUX13B", "TR-SAF-C"),
    ("BUS-AUX13B", "TR-SAF-D"),
    *chain("EDG-A", "CB-EDG-A", "BUS-416A"),
    *chain("TR-SAF-A", "CB-SAF-A", "BUS-416A"),
    *chain("BUS-416A", "CB-TIE-AB", "BUS-416B"),
    *chain("BUS-416A", "TR-480-A", "CB-LC-A", "LC-480A"),
    *chain("LC-480A", "CB-MCCA1", "MCC-1A1"),
    *chain("LC-480A", "CB-MCCA2", "MCC-1A2"),
    ("MCC-1A1", "PUMP-AFW-A"),
    ("MCC-1A1", "VLV-MSIV-A"),
    ("MCC-1A2", "PUMP-CCW-A"),
    ("LC-480A", "XFER-ATS-A"),
    *chain("EDG-B", "CB-EDG-B", "BUS-416B"),
    *chain("TR-SAF-B", "CB-SAF-B", "BUS-416B"),
    *chain("BUS-416B", "TR-480-B", "CB-LC-B", "LC-480B"),
    *chain("LC-480B", "CB-MCCB1", "MCC-1B1"),
    *chain("LC-480B", "CB-MCCB2", "MCC-1B2"),
    ("MCC-1B1", "PUMP-AFW-B"),
    ("MCC-1B1", "VLV-MSIV-B"),
    ("MCC-1B2", "PUMP-CCW-B"),
    ("LC-480B", "XFER-ATS-A"),
    *chain("EDG-C", "CB-EDG-C", "BUS-416C"),
    *chain("TR-SAF-C", "CB-SAF-C", "BUS-416C"),
    *chain("BUS-416C", "CB-TIE-CD", "BUS-416D"),
    *chain("BUS-416C", "TR-480-C", "CB-LC-C", "LC-480C"),
    *chain("LC-480C", "CB-MCCC1", "MCC-1C1"),
    *chain("LC-480C", "CB-MCCC2", "MCC-1C2"),
    ("MCC-1C1", "PUMP-RHR-A"),
    ("MCC-1C2", "FAN-CRHV-A"),
    ("MCC-1C2", "HTR-BATRM-A"),
    ("LC-480C", "XFER-ATS-B"),
    *chain("EDG-D", "CB-EDG-D", "BUS-416D"),
    *chain("TR-SAF-D", "CB-SAF-D", "BUS-416D"),
    *chain("BUS-416D", "TR-480-D", "CB-LC-D", "LC-480D"),
    *chain("LC-480D", "CB-MCCD1", "MCC-1D1"),
    *chain("LC-480D", "CB-MCCD2", "MCC-1D2"),
    ("MCC-1D1", "PUMP-RHR-B"),
    ("MCC-1D2", "FAN-CRHV-B"),
    ("MCC-1D2", "HTR-BATRM-B"),
    ("LC-480D", "XFER-ATS-B"),
    *chain("XFER-ATS-A", "CHG-125A", "BAT-125A", "PNL-DC-A", "INV-UPS-A", "UPS-PNL-A"),
    *chain("XFER-ATS-A", "RECT-48V-A", "BAT-48V-A", "JB-RLY-A"),
    *chain("XFER-ATS-B", "CHG-125B", "BAT-125B", "PNL-DC-B", "INV-UPS-B", "UPS-PNL-B"),
    *chain("XFER-ATS-B", "RECT-48V-B", "BAT-48V-B", "JB-RLY-B"),
    ("GND-GRID", "GSU-1"),
    ("GND-GRID", "TR-RAT-1A"),
    ("GND-GRID", "TR-RAT-1B"),
    ("GND-GRID", "BAT-48V-A"),
    ("GND-GRID", "BAT-48V-B"),
    ("GND-GRID", "UPS-PNL-A"),
    ("GND-GRID", "UPS-PNL-B"),
]


FINAL_CONTROL_EDGES = [
    ("CP-ESFAS-1", "CP-ESFAS-2"),
    ("CP-ESFAS-1", "RELAY-K1A"),
    ("CP-ESFAS-1", "RELAY-K1B"),
    ("CP-ESFAS-1", "RELAY-UV-A"),
    ("CP-ESFAS-1", "RELAY-UV-B"),
    ("CP-ESFAS-1", "INST-NSSS-A"),
    ("CP-ESFAS-1", "INST-NSSS-B"),
    ("CP-ESFAS-2", "RELAY-K2A"),
    ("CP-ESFAS-2", "RELAY-K2B"),
    ("CP-ESFAS-2", "RELAY-LOOP-C"),
    ("CP-ESFAS-2", "RELAY-LOOP-D"),
    ("CP-ESFAS-2", "INST-NSSS-A"),
    ("CP-ESFAS-2", "INST-NSSS-B"),
    ("CB-EDG-A", "RELAY-K1A"),
    ("CB-SAF-A", "RELAY-K1A"),
    ("CB-EDG-B", "RELAY-K1B"),
    ("CB-SAF-B", "RELAY-K1B"),
    ("CB-EDG-C", "RELAY-K2A"),
    ("CB-SAF-C", "RELAY-K2A"),
    ("CB-EDG-D", "RELAY-K2B"),
    ("CB-SAF-D", "RELAY-K2B"),
    ("BUS-416A", "RELAY-UV-A"),
    ("BUS-416B", "RELAY-UV-A"),
    ("BUS-416C", "RELAY-UV-B"),
    ("BUS-416D", "RELAY-UV-B"),
    ("CB-TIE-AB", "RELAY-LOOP-C"),
    ("CB-TIE-CD", "RELAY-LOOP-D"),
]


DIEGO_R1_EDGES = [
    *SOLID_EDGES,
    *CONTROL_CANDIDATES,
    *DIEGO_R1_GROUND_CANDIDATES,
]

FINAL_EDGES = [
    *JENNIFER_R1_EDGES,
    *FINAL_CONTROL_EDGES,
]


ROUNDS = {
    "round1_diego": {
        "agent": "Diego",
        "summary": "High-recall first pass with broad control and ground candidates retained as matrix edges for audit.",
        "nodes": NODES,
        "edges": DIEGO_R1_EDGES,
    },
    "round1_jennifer": {
        "agent": "Jennifer",
        "summary": "Precision review preserving the main AC/DC skeleton and limited ground links; ESF/control nodes left for R2.",
        "nodes": NODES,
        "edges": JENNIFER_R1_EDGES,
    },
    "round2_diego": {
        "agent": "Diego",
        "summary": "Narrow recheck adding 27 terminal-dot-supported ESF/control links and retaining Jennifer's rejections.",
        "nodes": NODES,
        "edges": FINAL_EDGES,
    },
    "round2_jennifer_final": {
        "agent": "Jennifer",
        "summary": "Final precision acceptance of Diego R2; saturated at 112 nodes and 140 edges.",
        "nodes": NODES,
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
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in normalize_edges(edges):
        if a not in idx or b not in idx:
            raise ValueError(f"Unknown endpoint in edge: {a!r} -- {b!r}")
        if a == b:
            raise ValueError(f"Unexpected self-loop: {a!r}")
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
    duplicate_counts = Counter(tuple(sorted(edge)) for edge in edges)
    return {
        "node_count": len(nodes),
        "edge_count": len(normalize_edges(edges)),
        "matrix_rows": len(matrix),
        "matrix_columns": len(matrix[0]) if matrix else 0,
        "duplicate_edges": [list(edge) for edge, count in duplicate_counts.items() if count > 1],
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
        writer.writerows(normalize_edges(edges))


def write_adjacency(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    adjacency = {node: [] for node in nodes}
    for a, b in normalize_edges(edges):
        adjacency[a].append(b)
        adjacency[b].append(a)
    for values in adjacency.values():
        values.sort()
    path.write_text(json.dumps(adjacency, indent=2), encoding="utf-8")


def write_rounds_summary(path: Path) -> None:
    lines = [
        "# Document 5 Connectivity Extraction Rounds",
        "",
        "Scope: include visually supported power, DC/vital AC, control/trip/close, sensing/instrument, and grounding-conductor links between accepted real nodes. Annotation-only tags are not nodes.",
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
        "## Final Decisions",
        "- Final saturated graph: 112 nodes, 140 edges, no isolated nodes.",
        "- Normally-open tie breakers `CB-TIE13`, `CB-TIE-AB`, and `CB-TIE-CD` are included as visible physical connectivity through breaker nodes.",
        "- `JB-RLY-A--JB-RLY-B` and `PNL-DC-A--PNL-DC-B` are excluded because the dashed routing lacks accepted terminal-dot support for direct matrix edges.",
        "- Load-to-ATS crossing interpretations are excluded; accepted ATS links are `LC-480A/B--XFER-ATS-A` and `LC-480C/D--XFER-ATS-B`.",
        "- Ground is limited to seven visibly supported `GND-GRID` links accepted by both subagents.",
        "- ESF/control final adds the 27 terminal-dot-supported pairs accepted in Diego R2 and Jennifer final.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    qa_all = {}
    for name, data in ROUNDS.items():
        nodes = data["nodes"]
        edges = data["edges"]
        qa_all[name] = qa_for(nodes, edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)
        write_nodes(RESULTS / f"{name}_nodes.csv", nodes)
        write_edges(RESULTS / f"{name}_edges.csv", edges)

    write_matrix(RESULTS / "final_matrix.csv", NODES, FINAL_EDGES)
    write_nodes(RESULTS / "final_nodes.csv", NODES)
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_adjacency(RESULTS / "final_adjacency.json", NODES, FINAL_EDGES)
    write_rounds_summary(RESULTS / "rounds_summary.md")
    (RESULTS / "qa_summary.json").write_text(json.dumps(qa_all, indent=2), encoding="utf-8")

    final_qa = qa_for(NODES, FINAL_EDGES)
    if final_qa["edge_count"] != 140 or final_qa["node_count"] != 112:
        raise SystemExit(f"Unexpected final count: {final_qa}")
    if final_qa["isolated_nodes"] or not final_qa["symmetric"] or not final_qa["diagonal_zero"]:
        raise SystemExit(f"Final matrix QA failed: {final_qa}")
    print(json.dumps({"final": final_qa}, indent=2))


if __name__ == "__main__":
    main()
