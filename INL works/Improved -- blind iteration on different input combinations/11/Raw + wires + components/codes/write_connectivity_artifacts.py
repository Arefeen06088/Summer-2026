from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"


DIEGO_R1_NODES_TEXT = """
GEN-01
TR-UAT-1
UAT1-SEC
CB-UAT-1
BUS-13-8A
TR-SUT-1
SUT1-SEC
CB-SUT-1
CB-13-TIE
GEN-02
TR-UAT-2
UAT2-SEC
CB-UAT-2
BUS-13-8B
TR-SUT-2
SUT2-SEC
CB-SUT-2
CB-IN-A
RELAY-27A
DG-1A
CB-DG-A
BUS-4160-A
CB-4160-A1
TR-480-A1
CB-480-A1
BUS-480-A1
CB-MCC-A1
MCC-A1
PUMP-SI-A
PUMP-CCW-A
FAN-HVAC-A
CB-4160-A2
TR-480-A2
CB-480-A2
BUS-480-A2
CB-MCC-A2
MCC-A2
MOV-RHR-A
RECT-125-A
PANEL-IC-A
GND-A
CB-IN-B
RELAY-27B
DG-1B
CB-DG-B
BUS-4160-B
CB-4160-B1
TR-480-B1
CB-480-B1
BUS-480-B1
CB-MCC-B1
MCC-B1
PUMP-SI-B
PUMP-CCW-B
FAN-HVAC-B
CB-4160-B2
TR-480-B2
CB-480-B2
BUS-480-B2
CB-MCC-B2
MCC-B2
MOV-RHR-B
RECT-125-B
PANEL-IC-B
GND-B
CB-IN-C
RELAY-27C
DG-1C
CB-DG-C
BUS-4160-C
CB-4160-C1
TR-480-C1
CB-480-C1
BUS-480-C1
CB-MCC-C1
MCC-C1
PUMP-SI-C
PUMP-CCW-C
FAN-HVAC-C
CB-4160-C2
TR-480-C2
CB-480-C2
BUS-480-C2
CB-MCC-C2
MCC-C2
MOV-RHR-C
RECT-125-C
PANEL-IC-C
GND-C
CB-IN-D
RELAY-27D
DG-1D
CB-DG-D
BUS-4160-D
CB-4160-D1
TR-480-D1
CB-480-D1
BUS-480-D1
CB-MCC-D1
MCC-D1
PUMP-SI-D
PUMP-CCW-D
FAN-HVAC-D
CB-4160-D2
TR-480-D2
CB-480-D2
BUS-480-D2
CB-MCC-D2
MCC-D2
MOV-RHR-D
RECT-125-D
PANEL-IC-D
GND-D
BAT-125A
BUS-DC-125A
INV-UPS-A
PANEL-RPS-A
PANEL-SSPS
BAT-125B
BUS-DC-125B
INV-UPS-B
PANEL-RPS-B
ATS-480-A
ATS-480-B
"""


DIEGO_R1_EDGES_CSV = """
A,B,type
GEN-01,TR-UAT-1,S
TR-UAT-1,UAT1-SEC,S
UAT1-SEC,CB-UAT-1,S
CB-UAT-1,BUS-13-8A,S
TR-SUT-1,SUT1-SEC,S
SUT1-SEC,CB-SUT-1,S
CB-SUT-1,BUS-13-8A,S
BUS-13-8A,CB-13-TIE,S
CB-13-TIE,BUS-13-8B,S
GEN-02,TR-UAT-2,S
TR-UAT-2,UAT2-SEC,S
UAT2-SEC,CB-UAT-2,S
CB-UAT-2,BUS-13-8B,S
TR-SUT-2,SUT2-SEC,S
SUT2-SEC,CB-SUT-2,S
CB-SUT-2,BUS-13-8B,S
BUS-13-8A,CB-IN-A,S
BUS-13-8A,CB-IN-B,S
BUS-13-8B,CB-IN-C,S
BUS-13-8B,CB-IN-D,S
CB-IN-A,BUS-4160-A,S
CB-IN-A,RELAY-27A,D
RELAY-27A,CB-DG-A,D
DG-1A,CB-DG-A,S
CB-DG-A,BUS-4160-A,S
BUS-4160-A,CB-4160-A1,S
CB-4160-A1,TR-480-A1,S
TR-480-A1,CB-480-A1,S
CB-480-A1,BUS-480-A1,S
BUS-480-A1,CB-MCC-A1,S
CB-MCC-A1,MCC-A1,S
MCC-A1,PUMP-SI-A,S
MCC-A1,PUMP-CCW-A,S
MCC-A1,FAN-HVAC-A,S
BUS-4160-A,CB-4160-A2,S
CB-4160-A2,TR-480-A2,S
TR-480-A2,CB-480-A2,S
CB-480-A2,BUS-480-A2,S
BUS-480-A1,BUS-480-A2,S
BUS-480-A2,CB-MCC-A2,S
CB-MCC-A2,MCC-A2,S
MCC-A2,MOV-RHR-A,S
BUS-480-A2,RECT-125-A,S
RECT-125-A,PANEL-IC-A,S
MCC-A2,PANEL-IC-A,D
PANEL-IC-A,GND-A,G
CB-IN-B,BUS-4160-B,S
CB-IN-B,RELAY-27B,D
RELAY-27B,CB-DG-B,D
DG-1B,CB-DG-B,S
CB-DG-B,BUS-4160-B,S
BUS-4160-B,CB-4160-B1,S
CB-4160-B1,TR-480-B1,S
TR-480-B1,CB-480-B1,S
CB-480-B1,BUS-480-B1,S
BUS-480-B1,CB-MCC-B1,S
CB-MCC-B1,MCC-B1,S
MCC-B1,PUMP-SI-B,S
MCC-B1,PUMP-CCW-B,S
MCC-B1,FAN-HVAC-B,S
BUS-4160-B,CB-4160-B2,S
CB-4160-B2,TR-480-B2,S
TR-480-B2,CB-480-B2,S
CB-480-B2,BUS-480-B2,S
BUS-480-B1,BUS-480-B2,S
BUS-480-B2,CB-MCC-B2,S
CB-MCC-B2,MCC-B2,S
MCC-B2,MOV-RHR-B,S
BUS-480-B2,RECT-125-B,S
RECT-125-B,PANEL-IC-B,S
MCC-B2,PANEL-IC-B,D
PANEL-IC-B,GND-B,G
CB-IN-C,BUS-4160-C,S
CB-IN-C,RELAY-27C,D
RELAY-27C,CB-DG-C,D
DG-1C,CB-DG-C,S
CB-DG-C,BUS-4160-C,S
BUS-4160-C,CB-4160-C1,S
CB-4160-C1,TR-480-C1,S
TR-480-C1,CB-480-C1,S
CB-480-C1,BUS-480-C1,S
BUS-480-C1,CB-MCC-C1,S
CB-MCC-C1,MCC-C1,S
MCC-C1,PUMP-SI-C,S
MCC-C1,PUMP-CCW-C,S
MCC-C1,FAN-HVAC-C,S
BUS-4160-C,CB-4160-C2,S
CB-4160-C2,TR-480-C2,S
TR-480-C2,CB-480-C2,S
CB-480-C2,BUS-480-C2,S
BUS-480-C1,BUS-480-C2,S
BUS-480-C2,CB-MCC-C2,S
CB-MCC-C2,MCC-C2,S
MCC-C2,MOV-RHR-C,S
BUS-480-C2,RECT-125-C,S
RECT-125-C,PANEL-IC-C,S
MCC-C2,PANEL-IC-C,D
PANEL-IC-C,GND-C,G
CB-IN-D,BUS-4160-D,S
CB-IN-D,RELAY-27D,D
RELAY-27D,CB-DG-D,D
DG-1D,CB-DG-D,S
CB-DG-D,BUS-4160-D,S
BUS-4160-D,CB-4160-D1,S
CB-4160-D1,TR-480-D1,S
TR-480-D1,CB-480-D1,S
CB-480-D1,BUS-480-D1,S
BUS-480-D1,CB-MCC-D1,S
CB-MCC-D1,MCC-D1,S
MCC-D1,PUMP-SI-D,S
MCC-D1,PUMP-CCW-D,S
MCC-D1,FAN-HVAC-D,S
BUS-4160-D,CB-4160-D2,S
CB-4160-D2,TR-480-D2,S
TR-480-D2,CB-480-D2,S
CB-480-D2,BUS-480-D2,S
BUS-480-D1,BUS-480-D2,S
BUS-480-D2,CB-MCC-D2,S
CB-MCC-D2,MCC-D2,S
MCC-D2,MOV-RHR-D,S
BUS-480-D2,RECT-125-D,S
RECT-125-D,PANEL-IC-D,S
MCC-D2,PANEL-IC-D,D
PANEL-IC-D,GND-D,G
BAT-125A,BUS-DC-125A,S
BUS-DC-125A,INV-UPS-A,S
INV-UPS-A,PANEL-RPS-A,S
ATS-480-A,PANEL-RPS-A,S
BAT-125B,BUS-DC-125B,S
BUS-DC-125B,INV-UPS-B,S
INV-UPS-B,PANEL-RPS-B,S
ATS-480-B,PANEL-RPS-B,S
"""


FINAL_NODES_TEXT = """
GEN-01
TR-UAT-1
CB-UAT-1
BUS-13-8A
TR-SUT-1
CB-SUT-1
CB-13-TIE
GEN-02
TR-UAT-2
CB-UAT-2
BUS-13-8B
TR-SUT-2
CB-SUT-2
CB-IN-A
RELAY-27A
DG-1A
CB-DG-A
BUS-4160-A
CB-4160-A1
TR-480-A1
CB-480-A1
BUS-480-A1
CB-MCC-A1
MCC-A1
PUMP-SI-A
PUMP-CCW-A
FAN-HVAC-A
CB-4160-A2
TR-480-A2
CB-480-A2
BUS-480-A2
CB-MCC-A2
MCC-A2
MOV-RHR-A
RECT-125-A
PANEL-IC-A
GND-A
CB-IN-B
RELAY-27B
DG-1B
CB-DG-B
BUS-4160-B
CB-4160-B1
TR-480-B1
CB-480-B1
BUS-480-B1
CB-MCC-B1
MCC-B1
PUMP-SI-B
PUMP-CCW-B
FAN-HVAC-B
CB-4160-B2
TR-480-B2
CB-480-B2
BUS-480-B2
CB-MCC-B2
MCC-B2
MOV-RHR-B
RECT-125-B
PANEL-IC-B
GND-B
CB-IN-C
RELAY-27C
DG-1C
CB-DG-C
BUS-4160-C
CB-4160-C1
TR-480-C1
CB-480-C1
BUS-480-C1
CB-MCC-C1
MCC-C1
PUMP-SI-C
PUMP-CCW-C
FAN-HVAC-C
CB-4160-C2
TR-480-C2
CB-480-C2
BUS-480-C2
CB-MCC-C2
MCC-C2
MOV-RHR-C
RECT-125-C
PANEL-IC-C
GND-C
CB-IN-D
RELAY-27D
DG-1D
CB-DG-D
BUS-4160-D
CB-4160-D1
TR-480-D1
CB-480-D1
BUS-480-D1
CB-MCC-D1
MCC-D1
PUMP-SI-D
PUMP-CCW-D
FAN-HVAC-D
CB-4160-D2
TR-480-D2
CB-480-D2
BUS-480-D2
CB-MCC-D2
MCC-D2
MOV-RHR-D
RECT-125-D
PANEL-IC-D
GND-D
BAT-125A
BUS-DC-125A
INV-UPS-A
PANEL-RPS-A
PANEL-SSPS
BAT-125B
BUS-DC-125B
INV-UPS-B
PANEL-RPS-B
ATS-480-A
ATS-480-B
"""


FINAL_EDGES_CSV = """
A,B,type
GEN-01,TR-UAT-1,S
TR-UAT-1,CB-UAT-1,S
CB-UAT-1,BUS-13-8A,S
TR-SUT-1,CB-SUT-1,S
CB-SUT-1,BUS-13-8A,S
BUS-13-8A,CB-13-TIE,S
CB-13-TIE,BUS-13-8B,S
GEN-02,TR-UAT-2,S
TR-UAT-2,CB-UAT-2,S
CB-UAT-2,BUS-13-8B,S
TR-SUT-2,CB-SUT-2,S
CB-SUT-2,BUS-13-8B,S
BUS-13-8A,CB-IN-A,S
BUS-13-8A,CB-IN-B,S
BUS-13-8B,CB-IN-C,S
BUS-13-8B,CB-IN-D,S
CB-IN-A,BUS-4160-A,S
CB-IN-A,RELAY-27A,D
RELAY-27A,CB-DG-A,D
DG-1A,CB-DG-A,S
CB-DG-A,BUS-4160-A,S
BUS-4160-A,CB-4160-A1,S
CB-4160-A1,TR-480-A1,S
TR-480-A1,CB-480-A1,S
CB-480-A1,BUS-480-A1,S
BUS-480-A1,CB-MCC-A1,S
CB-MCC-A1,MCC-A1,S
MCC-A1,PUMP-SI-A,S
MCC-A1,PUMP-CCW-A,S
MCC-A1,FAN-HVAC-A,S
MCC-A1,ATS-480-A,S
BUS-4160-A,CB-4160-A2,S
CB-4160-A2,TR-480-A2,S
TR-480-A2,CB-480-A2,S
CB-480-A2,BUS-480-A2,S
BUS-480-A1,BUS-480-A2,S
BUS-480-A2,CB-MCC-A2,S
CB-MCC-A2,MCC-A2,S
MCC-A2,MOV-RHR-A,S
BUS-480-A2,RECT-125-A,S
RECT-125-A,PANEL-IC-A,S
RECT-125-A,BUS-DC-125A,S
MCC-A2,PANEL-IC-A,D
PANEL-IC-A,GND-A,G
CB-IN-B,BUS-4160-B,S
CB-IN-B,RELAY-27B,D
RELAY-27B,CB-DG-B,D
DG-1B,CB-DG-B,S
CB-DG-B,BUS-4160-B,S
BUS-4160-B,CB-4160-B1,S
CB-4160-B1,TR-480-B1,S
TR-480-B1,CB-480-B1,S
CB-480-B1,BUS-480-B1,S
BUS-480-B1,CB-MCC-B1,S
CB-MCC-B1,MCC-B1,S
MCC-B1,PUMP-SI-B,S
MCC-B1,PUMP-CCW-B,S
MCC-B1,FAN-HVAC-B,S
MCC-B1,ATS-480-A,S
BUS-4160-B,CB-4160-B2,S
CB-4160-B2,TR-480-B2,S
TR-480-B2,CB-480-B2,S
CB-480-B2,BUS-480-B2,S
BUS-480-B1,BUS-480-B2,S
BUS-480-B2,CB-MCC-B2,S
CB-MCC-B2,MCC-B2,S
MCC-B2,MOV-RHR-B,S
BUS-480-B2,RECT-125-B,S
RECT-125-B,PANEL-IC-B,S
RECT-125-B,BUS-DC-125A,S
MCC-B2,PANEL-IC-B,D
PANEL-IC-B,GND-B,G
CB-IN-C,BUS-4160-C,S
CB-IN-C,RELAY-27C,D
RELAY-27C,CB-DG-C,D
DG-1C,CB-DG-C,S
CB-DG-C,BUS-4160-C,S
BUS-4160-C,CB-4160-C1,S
CB-4160-C1,TR-480-C1,S
TR-480-C1,CB-480-C1,S
CB-480-C1,BUS-480-C1,S
BUS-480-C1,CB-MCC-C1,S
CB-MCC-C1,MCC-C1,S
MCC-C1,PUMP-SI-C,S
MCC-C1,PUMP-CCW-C,S
MCC-C1,FAN-HVAC-C,S
MCC-C1,ATS-480-B,S
BUS-4160-C,CB-4160-C2,S
CB-4160-C2,TR-480-C2,S
TR-480-C2,CB-480-C2,S
CB-480-C2,BUS-480-C2,S
BUS-480-C1,BUS-480-C2,S
BUS-480-C2,CB-MCC-C2,S
CB-MCC-C2,MCC-C2,S
MCC-C2,MOV-RHR-C,S
BUS-480-C2,RECT-125-C,S
RECT-125-C,PANEL-IC-C,S
RECT-125-C,BUS-DC-125B,S
MCC-C2,PANEL-IC-C,D
PANEL-IC-C,GND-C,G
CB-IN-D,BUS-4160-D,S
CB-IN-D,RELAY-27D,D
RELAY-27D,CB-DG-D,D
DG-1D,CB-DG-D,S
CB-DG-D,BUS-4160-D,S
BUS-4160-D,CB-4160-D1,S
CB-4160-D1,TR-480-D1,S
TR-480-D1,CB-480-D1,S
CB-480-D1,BUS-480-D1,S
BUS-480-D1,CB-MCC-D1,S
CB-MCC-D1,MCC-D1,S
MCC-D1,PUMP-SI-D,S
MCC-D1,PUMP-CCW-D,S
MCC-D1,FAN-HVAC-D,S
MCC-D1,ATS-480-B,S
BUS-4160-D,CB-4160-D2,S
CB-4160-D2,TR-480-D2,S
TR-480-D2,CB-480-D2,S
CB-480-D2,BUS-480-D2,S
BUS-480-D1,BUS-480-D2,S
BUS-480-D2,CB-MCC-D2,S
CB-MCC-D2,MCC-D2,S
MCC-D2,MOV-RHR-D,S
BUS-480-D2,RECT-125-D,S
RECT-125-D,PANEL-IC-D,S
RECT-125-D,BUS-DC-125B,S
MCC-D2,PANEL-IC-D,D
PANEL-IC-D,GND-D,G
BAT-125A,BUS-DC-125A,S
BUS-DC-125A,INV-UPS-A,S
INV-UPS-A,PANEL-RPS-A,S
ATS-480-A,PANEL-RPS-A,S
BAT-125B,BUS-DC-125B,S
BUS-DC-125B,INV-UPS-B,S
INV-UPS-B,PANEL-RPS-B,S
ATS-480-B,PANEL-RPS-B,S
"""


ROUND_NOTES = {
    "round01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "summary": "Initial high-recall extraction retained four *-SEC conductor labels as nodes and left ATS feeder/DC bus landings uncertain.",
    },
    "round01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "summary": "Removed conductor-label-only *-SEC nodes, promoted clear MCC-to-ATS and rectifier-to-DC-bus solid landings, kept SSPS dashed routes uncertain.",
    },
    "round02_diego": {
        "agent": "Diego",
        "role": "high-recall saturation review",
        "summary": "Saturation pass over Jennifer's corrected candidate.",
    },
    "round02_jennifer": {
        "agent": "Jennifer",
        "role": "precision final signoff",
        "summary": "Final precision signoff after Diego saturation response.",
    },
}


EXCLUDED_OR_UNCERTAIN = [
    "PANEL-RPS-A,PANEL-SSPS,D",
    "PANEL-RPS-B,PANEL-SSPS,D",
    "ATS-480-A,PANEL-SSPS,D",
    "ATS-480-B,PANEL-SSPS,D",
    "RELAY-27A,PANEL-SSPS,D",
    "RELAY-27B,PANEL-SSPS,D",
    "RELAY-27C,PANEL-SSPS,D",
    "RELAY-27D,PANEL-SSPS,D",
    "RELAY-27A,BUS-4160-A,D",
    "RELAY-27B,BUS-4160-B,D",
    "RELAY-27C,BUS-4160-C,D",
    "RELAY-27D,BUS-4160-D,D",
    "GND-A,GND-B,G",
    "GND-C,GND-D,G",
]


def parse_nodes(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_edges(text: str) -> list[dict[str, str]]:
    rows = []
    reader = csv.DictReader(line for line in text.splitlines() if line.strip())
    seen: set[tuple[str, str]] = set()
    for row in reader:
        a = row["A"].strip()
        b = row["B"].strip()
        edge_type = row["type"].strip()
        key = tuple(sorted((a, b)))
        if key in seen:
            raise ValueError(f"Duplicate undirected edge: {a} -- {b}")
        seen.add(key)
        rows.append({"A": a, "B": b, "type": edge_type})
    return rows


def validate(nodes: list[str], edges: list[dict[str, str]]) -> None:
    node_set = set(nodes)
    if len(node_set) != len(nodes):
        raise ValueError("Duplicate node names found")
    missing = sorted({endpoint for e in edges for endpoint in (e["A"], e["B"]) if endpoint not in node_set})
    if missing:
        raise ValueError(f"Edges reference nodes not in node list: {missing}")


def write_nodes(path: Path, nodes: list[str]) -> None:
    path.write_text("\n".join(nodes) + "\n", encoding="utf-8")


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["A", "B", "type"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    adjacency = {node: {other: 0 for other in nodes} for node in nodes}
    for edge in edges:
        a = edge["A"]
        b = edge["B"]
        adjacency[a][b] = 1
        adjacency[b][a] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [adjacency[node][other] for other in nodes])


def write_sparse_pairs(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    edge_types = {tuple(sorted((e["A"], e["B"]))): e["type"] for e in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "connected", "type"])
        for i, a in enumerate(nodes):
            for b in nodes[i + 1 :]:
                key = tuple(sorted((a, b)))
                connected = 1 if key in edge_types else 0
                writer.writerow([a, b, connected, edge_types.get(key, "")])


def write_round_artifacts(round_name: str, nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    validate(nodes, edges)
    write_nodes(RESULTS_DIR / f"{round_name}_nodes.txt", nodes)
    write_edges(RESULTS_DIR / f"{round_name}_edges.csv", edges)
    write_matrix(RESULTS_DIR / f"{round_name}_connectivity_matrix.csv", nodes, edges)
    return {
        "round": round_name,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "matrix": f"{round_name}_connectivity_matrix.csv",
        "edges": f"{round_name}_edges.csv",
        **ROUND_NOTES[round_name],
    }


def write_report(rounds: list[dict[str, object]], final_nodes: list[str], final_edges: list[dict[str, str]]) -> None:
    lines = [
        "# Document 11 Connectivity Extraction Report",
        "",
        "Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used.",
        "",
        "## Final Matrix",
        "",
        f"- Final node count: {len(final_nodes)}",
        f"- Final accepted edge count: {len(final_edges)}",
        "- Matrix file: `final_connectivity_matrix.csv`",
        "- Sparse edge file: `final_sparse_edges.csv`",
        "",
        "## Round Summary",
        "",
        "| Round | Agent | Nodes | Edges | Summary |",
        "|---|---:|---:|---:|---|",
    ]
    for entry in rounds:
        lines.append(
            f"| {entry['round']} | {entry['agent']} | {entry['node_count']} | {entry['edge_count']} | {entry['summary']} |"
        )
    lines.extend(
        [
            "",
            "## Final Corrections From Diego R1",
            "",
            "- Removed `UAT1-SEC`, `SUT1-SEC`, `UAT2-SEC`, and `SUT2-SEC` as conductor labels rather than standalone nodes.",
            "- Replaced the top-source paths with direct transformer-to-breaker edges.",
            "- Accepted four solid MCC-to-ATS feeder landings.",
            "- Accepted four rectifier-to-125 VDC bus landings.",
            "- Kept dashed SSPS/RPS/ATS interlock routes, relay-to-SSPS routes, relay-to-4160-bus candidates, and ground-to-ground ties excluded/uncertain.",
            "",
            "## Excluded Or Still Uncertain",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in EXCLUDED_OR_UNCERTAIN)
    lines.append("")
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    diego_r1_nodes = parse_nodes(DIEGO_R1_NODES_TEXT)
    diego_r1_edges = parse_edges(DIEGO_R1_EDGES_CSV)
    final_nodes = parse_nodes(FINAL_NODES_TEXT)
    final_edges = parse_edges(FINAL_EDGES_CSV)

    rounds = [
        write_round_artifacts("round01_diego", diego_r1_nodes, diego_r1_edges),
        write_round_artifacts("round01_jennifer", final_nodes, final_edges),
        write_round_artifacts("round02_diego", final_nodes, final_edges),
        write_round_artifacts("round02_jennifer", final_nodes, final_edges),
    ]

    write_nodes(RESULTS_DIR / "final_nodes.txt", final_nodes)
    write_edges(RESULTS_DIR / "final_sparse_edges.csv", final_edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_sparse_pairs(RESULTS_DIR / "final_sparse_matrix_pairs.csv", final_nodes, final_edges)
    (RESULTS_DIR / "rounds_connectivity.json").write_text(json.dumps(rounds, indent=2), encoding="utf-8")
    write_report(rounds, final_nodes, final_edges)

    print(json.dumps({"final_nodes": len(final_nodes), "final_edges": len(final_edges), "rounds": rounds}, indent=2))


if __name__ == "__main__":
    main()
