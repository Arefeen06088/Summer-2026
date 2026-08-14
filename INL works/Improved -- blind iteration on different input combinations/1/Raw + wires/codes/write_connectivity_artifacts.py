from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


DIEGO_R1_NODES = [
    "BUS-4KV-A",
    "GRID-345A",
    "SWGR-52A",
    "RAT-1A",
    "MAIN-GEN-1",
    "GCB-1",
    "UAT-1A",
    "EDG-1A",
    "CB-EDG-A",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "BUS-4KV-B",
    "GRID-345B",
    "SWGR-52B",
    "RAT-1B",
    "EDG-1B",
    "CB-EDG-B",
    "CB-TIE-BC",
    "DS-TIE-BC",
    "BUS-4KV-C",
    "EDG-1C",
    "CB-EDG-C",
    "AAC-GEN-1",
    "CB-AAC-C",
    "CB-4A-01",
    "TR-480A",
    "CB-48A-01",
    "BUS-480-A",
    "CB-P201A",
    "MCC-01A",
    "RELAY-K201A",
    "PUMP-P201A",
    "CB-P202A",
    "MCC-02A",
    "RELAY-K202A",
    "PUMP-P202A",
    "CB-M301A",
    "MCC-03A",
    "RELAY-K301A",
    "MOTOR-FAN301A",
    "CB-V410A",
    "MCC-04A",
    "SOL-V410A",
    "VALVE-V410A",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "BUS-120AC-A",
    "PNL-RPS-A",
    "RELAY-UV-A",
    "PT-A",
    "INSTR-PT-A",
    "CB-4B-01",
    "TR-480B",
    "CB-48B-01",
    "BUS-480-B",
    "CB-P201B",
    "MCC-01B",
    "RELAY-K201B",
    "PUMP-P201B",
    "CB-P202B",
    "MCC-02B",
    "RELAY-K202B",
    "PUMP-P202B",
    "CB-M301B",
    "MCC-03B",
    "RELAY-K301B",
    "MOTOR-FAN301B",
    "CB-V410B",
    "MCC-04B",
    "SOL-V410B",
    "VALVE-V410B",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "BUS-120AC-B",
    "PNL-RPS-B",
    "RELAY-UV-B",
    "PT-B",
    "INSTR-PT-B",
    "CB-4C-01",
    "TR-480C",
    "CB-48C-01",
    "BUS-480-C",
    "CB-P501",
    "MCC-05C",
    "RELAY-K501",
    "PUMP-CCW501",
    "CB-M601",
    "MCC-06C",
    "RELAY-K601",
    "MOTOR-HVAC601",
    "CB-V502",
    "MCC-07C",
    "SOL-V502",
    "VALVE-V502",
    "CB-P503",
    "MCC-08C",
    "RELAY-K503",
    "PUMP-SW503",
    "TO 4KV BUS A ELEMENTARY DIAGRAM SH-2",
    "TO 4KV BUS B ELEMENTARY DIAGRAM SH-3",
    "TO AAC BUS C ELEMENTARY DIAGRAM SH-4",
]


DIEGO_R1_EDGES = [
    ("GRID-345A", "SWGR-52A", "high", "solid"),
    ("SWGR-52A", "RAT-1A", "high", "solid"),
    ("RAT-1A", "BUS-4KV-A", "high", "bus tap"),
    ("MAIN-GEN-1", "GCB-1", "high", "solid"),
    ("GCB-1", "UAT-1A", "high", "solid"),
    ("UAT-1A", "BUS-4KV-A", "high", "bus tap"),
    ("EDG-1A", "CB-EDG-A", "high", "solid"),
    ("CB-EDG-A", "BUS-4KV-A", "high", "bus tap"),
    ("BUS-4KV-A", "CB-TIE-AB", "medium", "normally-open bus tie"),
    ("CB-TIE-AB", "DS-TIE-AB", "medium", "normally-open bus tie"),
    ("DS-TIE-AB", "BUS-4KV-B", "medium", "normally-open bus tie"),
    ("GRID-345B", "SWGR-52B", "high", "solid"),
    ("SWGR-52B", "RAT-1B", "high", "solid"),
    ("RAT-1B", "BUS-4KV-B", "high", "bus tap"),
    ("EDG-1B", "CB-EDG-B", "high", "solid"),
    ("CB-EDG-B", "BUS-4KV-B", "high", "bus tap"),
    ("BUS-4KV-B", "CB-TIE-BC", "medium", "normally-open bus tie"),
    ("CB-TIE-BC", "DS-TIE-BC", "medium", "normally-open bus tie"),
    ("DS-TIE-BC", "BUS-4KV-C", "medium", "normally-open bus tie"),
    ("EDG-1C", "CB-EDG-C", "high", "solid"),
    ("CB-EDG-C", "BUS-4KV-C", "high", "bus tap"),
    ("AAC-GEN-1", "CB-AAC-C", "high", "solid"),
    ("CB-AAC-C", "BUS-4KV-C", "high", "bus tap"),
    ("BUS-4KV-A", "CB-4A-01", "high", "bus tap"),
    ("CB-4A-01", "TR-480A", "high", "solid"),
    ("TR-480A", "CB-48A-01", "high", "solid"),
    ("CB-48A-01", "BUS-480-A", "high", "bus tap"),
    ("BUS-4KV-B", "CB-4B-01", "high", "bus tap"),
    ("CB-4B-01", "TR-480B", "high", "solid"),
    ("TR-480B", "CB-48B-01", "high", "solid"),
    ("CB-48B-01", "BUS-480-B", "high", "bus tap"),
    ("BUS-4KV-C", "CB-4C-01", "high", "bus tap"),
    ("CB-4C-01", "TR-480C", "high", "solid"),
    ("TR-480C", "CB-48C-01", "high", "solid"),
    ("CB-48C-01", "BUS-480-C", "high", "bus tap"),
    ("BUS-480-A", "CB-P201A", "high", "bus tap"),
    ("CB-P201A", "MCC-01A", "high", "solid"),
    ("MCC-01A", "RELAY-K201A", "high", "solid"),
    ("RELAY-K201A", "PUMP-P201A", "high", "solid"),
    ("BUS-480-A", "CB-P202A", "high", "bus tap"),
    ("CB-P202A", "MCC-02A", "high", "solid"),
    ("MCC-02A", "RELAY-K202A", "high", "solid"),
    ("RELAY-K202A", "PUMP-P202A", "high", "solid"),
    ("BUS-480-A", "CB-M301A", "high", "bus tap"),
    ("CB-M301A", "MCC-03A", "high", "solid"),
    ("MCC-03A", "RELAY-K301A", "high", "solid"),
    ("RELAY-K301A", "MOTOR-FAN301A", "high", "solid"),
    ("BUS-480-A", "CB-V410A", "high", "bus tap"),
    ("CB-V410A", "MCC-04A", "high", "solid"),
    ("MCC-04A", "SOL-V410A", "high", "solid"),
    ("SOL-V410A", "VALVE-V410A", "high", "solid"),
    ("BUS-480-A", "CHG-125A", "high", "bus tap"),
    ("CHG-125A", "BAT-125A", "high", "solid"),
    ("BAT-125A", "BUS-125DC-A", "high", "bus tap"),
    ("BUS-125DC-A", "INV-120A", "high", "bus tap"),
    ("INV-120A", "BUS-120AC-A", "high", "bus tap"),
    ("BUS-120AC-A", "PNL-RPS-A", "high", "bus tap"),
    ("PNL-RPS-A", "RELAY-UV-A", "high", "control dashed"),
    ("RELAY-UV-A", "PT-A", "high", "instrument dotted"),
    ("PT-A", "INSTR-PT-A", "high", "instrument dotted"),
    ("BUS-125DC-A", "BUS-125DC-B", "low", "normally-open DC tie"),
    ("BUS-480-B", "CB-P201B", "high", "bus tap"),
    ("CB-P201B", "MCC-01B", "high", "solid"),
    ("MCC-01B", "RELAY-K201B", "high", "solid"),
    ("RELAY-K201B", "PUMP-P201B", "high", "solid"),
    ("BUS-480-B", "CB-P202B", "high", "bus tap"),
    ("CB-P202B", "MCC-02B", "high", "solid"),
    ("MCC-02B", "RELAY-K202B", "high", "solid"),
    ("RELAY-K202B", "PUMP-P202B", "high", "solid"),
    ("BUS-480-B", "CB-M301B", "high", "bus tap"),
    ("CB-M301B", "MCC-03B", "high", "solid"),
    ("MCC-03B", "RELAY-K301B", "high", "solid"),
    ("RELAY-K301B", "MOTOR-FAN301B", "high", "solid"),
    ("BUS-480-B", "CB-V410B", "high", "bus tap"),
    ("CB-V410B", "MCC-04B", "high", "solid"),
    ("MCC-04B", "SOL-V410B", "high", "solid"),
    ("SOL-V410B", "VALVE-V410B", "high", "solid"),
    ("BUS-480-B", "CHG-125B", "high", "bus tap"),
    ("CHG-125B", "BAT-125B", "high", "solid"),
    ("BAT-125B", "BUS-125DC-B", "high", "bus tap"),
    ("BUS-125DC-B", "INV-120B", "high", "bus tap"),
    ("INV-120B", "BUS-120AC-B", "high", "bus tap"),
    ("BUS-120AC-B", "PNL-RPS-B", "high", "bus tap"),
    ("PNL-RPS-B", "RELAY-UV-B", "high", "control dashed"),
    ("RELAY-UV-B", "PT-B", "high", "instrument dotted"),
    ("PT-B", "INSTR-PT-B", "high", "instrument dotted"),
    ("BUS-480-C", "CB-P501", "high", "bus tap"),
    ("CB-P501", "MCC-05C", "high", "solid"),
    ("MCC-05C", "RELAY-K501", "high", "solid"),
    ("RELAY-K501", "PUMP-CCW501", "high", "solid"),
    ("BUS-480-C", "CB-M601", "high", "bus tap"),
    ("CB-M601", "MCC-06C", "high", "solid"),
    ("MCC-06C", "RELAY-K601", "high", "solid"),
    ("RELAY-K601", "MOTOR-HVAC601", "high", "solid"),
    ("BUS-480-C", "CB-V502", "high", "bus tap"),
    ("CB-V502", "MCC-07C", "high", "solid"),
    ("MCC-07C", "SOL-V502", "high", "solid"),
    ("SOL-V502", "VALVE-V502", "high", "solid"),
    ("BUS-480-C", "CB-P503", "high", "bus tap"),
    ("CB-P503", "MCC-08C", "high", "solid"),
    ("MCC-08C", "RELAY-K503", "high", "solid"),
    ("RELAY-K503", "PUMP-SW503", "high", "solid"),
    ("BUS-4KV-A", "TO 4KV BUS A ELEMENTARY DIAGRAM SH-2", "low", "external continuation text"),
    ("BUS-4KV-B", "TO 4KV BUS B ELEMENTARY DIAGRAM SH-3", "low", "external continuation text"),
    ("BUS-4KV-C", "TO AAC BUS C ELEMENTARY DIAGRAM SH-4", "low", "external continuation text"),
]


JENNIFER_R1_NODES = DIEGO_R1_NODES[:-3]
JENNIFER_R1_EDGES = [
    edge
    for edge in DIEGO_R1_EDGES
    if not edge[3].startswith("external continuation")
]
JENNIFER_R1_EDGES = [
    (
        source,
        target,
        "uncertain" if {source, target} == {"BUS-125DC-A", "BUS-125DC-B"} else confidence,
        (
            "visible labeled N.O. DC TIE; no discrete tagged tie component"
            if {source, target} == {"BUS-125DC-A", "BUS-125DC-B"}
            else evidence
        ),
    )
    for source, target, confidence, evidence in JENNIFER_R1_EDGES
]


ROUNDS = {
    "round1_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "nodes": DIEGO_R1_NODES,
        "edges": DIEGO_R1_EDGES,
    },
    "round1_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer",
        "nodes": JENNIFER_R1_NODES,
        "edges": JENNIFER_R1_EDGES,
    },
    "round2_diego": {
        "agent": "Diego",
        "role": "reconciliation extractor",
        "nodes": JENNIFER_R1_NODES,
        "edges": JENNIFER_R1_EDGES,
    },
    "round2_jennifer": {
        "agent": "Jennifer",
        "role": "final precision confirmation",
        "nodes": JENNIFER_R1_NODES,
        "edges": JENNIFER_R1_EDGES,
    },
    "final": {
        "agent": "Diego + Jennifer",
        "role": "saturated agreed graph",
        "nodes": JENNIFER_R1_NODES,
        "edges": JENNIFER_R1_EDGES,
    },
}


def write_matrix(slug: str, nodes: list[str], edges: list[tuple[str, str, str, str]]) -> None:
    index = {name: i for i, name in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target, _confidence, _evidence in edges:
        if source not in index or target not in index:
            raise ValueError(f"Unknown edge endpoint in {slug}: {source!r}, {target!r}")
        i = index[source]
        j = index[target]
        if i == j:
            raise ValueError(f"Self-loop in {slug}: {source!r}")
        matrix[i][j] = 1
        matrix[j][i] = 1

    with (RESULTS / f"{slug}_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node", *nodes])
        for name, row in zip(nodes, matrix):
            writer.writerow([name, *row])


def write_edges(slug: str, edges: list[tuple[str, str, str, str]]) -> None:
    with (RESULTS / f"{slug}_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "confidence", "evidence"])
        writer.writerows(edges)


def write_nodes(slug: str, nodes: list[str]) -> None:
    with (RESULTS / f"{slug}_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "name"])
        for idx, name in enumerate(nodes, start=1):
            writer.writerow([idx, name])


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary = {}
    for slug, data in ROUNDS.items():
        nodes = data["nodes"]
        edges = data["edges"]
        write_nodes(slug, nodes)
        write_edges(slug, edges)
        write_matrix(slug, nodes, edges)
        summary[slug] = {
            "agent": data["agent"],
            "role": data["role"],
            "node_count": len(nodes),
            "edge_count": len(edges),
        }
    with (RESULTS / "rounds_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
