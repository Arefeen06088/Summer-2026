from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"


NODES_TEXT = """
GEN-G1
CB-GEN-1
TR-UAT-1
CB-101
TR-SUT-1
DS-SUT-1
CB-102
EDG-1A
DS-EDG-1A
CB-103
BUS-4KV-A
CB-111
TR-480-A
BUS-480-A
CB-112
TR-480-C
BUS-480-C
PT-4160A
CB-TIE-1
BUS-4KV-B
EDG-1B
DS-EDG-1B
CB-203
TR-SUT-2
DS-SUT-2
CB-202
EDG-1C
CB-303
CB-211
TR-480-B
BUS-480-B
PT-4160B
CB-212
TR-480-D
BUS-480-D
CB-M1A
MCC-1A
CB-F001
FU-F001
PUMP-RHR-A1
CB-F002
MS-F002
PUMP-SI-A
CB-F003
FU-F003
FAN-CR-A
CB-F004
DS-F004
MOV-RCIC-A
CB-F005
MS-F005
PUMP-CCW-A
CB-F006
FU-F006
HTR-SUMP-A
CB-F007
MS-F007
PMP-BOR-A
CB-F008
DS-F008
VALVE-IA-A
CB-M2A
MCC-2A
CB-F009
MS-F009
PUMP-AFW-A
CB-F010
MS-F010
PMP-LUBE-A
CB-F011
DS-F011
MOV-RHR-A
CB-F012
FU-F012
FAN-BLDG-A
CB-F013
FU-F013
PNL-RAD-A
CB-F014
MS-F014
PUMP-SW-A
CB-F015
DS-F015
SPARE-A2
CB-M1B
MCC-1B
CB-F016
MS-F016
PUMP-RHR-B1
CB-F017
MS-F017
PUMP-SI-B
CB-F018
FU-F018
FAN-CR-B
CB-F019
DS-F019
MOV-RCIC-B
CB-F020
MS-F020
PUMP-CCW-B
CB-F021
FU-F021
HTR-SUMP-B
CB-F022
MS-F022
PMP-BOR-B
CB-F023
DS-F023
VALVE-IA-B
CB-M2B
MCC-2B
CB-F024
MS-F024
PUMP-AFW-B
CB-F025
MS-F025
PMP-LUBE-B
CB-F026
DS-F026
MOV-RHR-B
CB-F027
FU-F027
FAN-BLDG-B
CB-F028
FU-F028
PNL-RAD-B
CB-F029
MS-F029
PUMP-SW-B
CB-DC-1A
CHGR-125A
BAT-125A
INV-1A
DC-BUS-A
CB-DC-1B
CHGR-125B
BAT-125B
INV-1B
DC-BUS-B
ATS-INV
BUS-120VAC-ESF
SEQ-REC-1
ANN-480A
RELAY-27A
RELAY-50A
RELAY-86A
TB-RPS-A
TB-ANN-1
PNL-RPS-A
PNL-ESFAS-A
GND-1
ANN-480B
RELAY-27B
RELAY-50B
RELAY-86B
TB-RPS-B
PNL-RPS-B
PNL-ESFAS-B
GND-2
"""


DIEGO_R1_EDGES_CSV = """
A,B,type
GEN-G1,CB-GEN-1,P
CB-GEN-1,TR-UAT-1,P
TR-UAT-1,CB-101,P
CB-101,BUS-4KV-A,P
TR-SUT-1,DS-SUT-1,P
DS-SUT-1,CB-102,P
CB-102,BUS-4KV-A,P
EDG-1A,DS-EDG-1A,P
DS-EDG-1A,CB-103,P
CB-103,BUS-4KV-A,P
BUS-4KV-A,CB-111,P
CB-111,TR-480-A,P
TR-480-A,BUS-480-A,P
BUS-4KV-A,CB-112,P
CB-112,TR-480-C,P
TR-480-C,BUS-480-C,P
BUS-4KV-A,CB-TIE-1,P
CB-TIE-1,BUS-4KV-B,P
EDG-1B,DS-EDG-1B,P
DS-EDG-1B,CB-203,P
CB-203,BUS-4KV-B,P
TR-SUT-2,DS-SUT-2,P
DS-SUT-2,CB-202,P
CB-202,BUS-4KV-B,P
EDG-1C,CB-303,P
CB-303,BUS-4KV-B,P
BUS-4KV-B,CB-211,P
CB-211,TR-480-B,P
TR-480-B,BUS-480-B,P
BUS-4KV-B,CB-212,P
CB-212,TR-480-D,P
TR-480-D,BUS-480-D,P
BUS-4KV-A,PT-4160A,SIG
BUS-4KV-B,PT-4160B,SIG
CB-101,CB-102,I
CB-102,CB-103,I
CB-103,CB-TIE-1,I
CB-TIE-1,CB-203,I
CB-203,CB-202,I
CB-202,CB-303,I
CB-111,CB-112,I
CB-211,CB-212,I
BUS-480-A,CB-M1A,P
CB-M1A,MCC-1A,P
MCC-1A,CB-F001,P
CB-F001,FU-F001,P
FU-F001,PUMP-RHR-A1,P
MCC-1A,CB-F002,P
CB-F002,MS-F002,P
MS-F002,PUMP-SI-A,P
MCC-1A,CB-F003,P
CB-F003,FU-F003,P
FU-F003,FAN-CR-A,P
MCC-1A,CB-F004,P
CB-F004,DS-F004,P
DS-F004,MOV-RCIC-A,P
MCC-1A,CB-F005,P
CB-F005,MS-F005,P
MS-F005,PUMP-CCW-A,P
MCC-1A,CB-F006,P
CB-F006,FU-F006,P
FU-F006,HTR-SUMP-A,P
MCC-1A,CB-F007,P
CB-F007,MS-F007,P
MS-F007,PMP-BOR-A,P
MCC-1A,CB-F008,P
CB-F008,DS-F008,P
DS-F008,VALVE-IA-A,P
BUS-480-C,CB-M2A,P
CB-M2A,MCC-2A,P
MCC-2A,CB-F009,P
CB-F009,MS-F009,P
MS-F009,PUMP-AFW-A,P
MCC-2A,CB-F010,P
CB-F010,MS-F010,P
MS-F010,PMP-LUBE-A,P
MCC-2A,CB-F011,P
CB-F011,DS-F011,P
DS-F011,MOV-RHR-A,P
MCC-2A,CB-F012,P
CB-F012,FU-F012,P
FU-F012,FAN-BLDG-A,P
MCC-2A,CB-F013,P
CB-F013,FU-F013,P
FU-F013,PNL-RAD-A,P
MCC-2A,CB-F014,P
CB-F014,MS-F014,P
MS-F014,PUMP-SW-A,P
MCC-2A,CB-F015,P
CB-F015,DS-F015,P
DS-F015,SPARE-A2,P
BUS-480-C,CB-DC-1A,P
CB-DC-1A,CHGR-125A,P
CHGR-125A,DC-BUS-A,P
BAT-125A,DC-BUS-A,P
DC-BUS-A,INV-1A,P
BUS-480-B,CB-M1B,P
CB-M1B,MCC-1B,P
MCC-1B,CB-F016,P
CB-F016,MS-F016,P
MS-F016,PUMP-RHR-B1,P
MCC-1B,CB-F017,P
CB-F017,MS-F017,P
MS-F017,PUMP-SI-B,P
MCC-1B,CB-F018,P
CB-F018,FU-F018,P
FU-F018,FAN-CR-B,P
MCC-1B,CB-F019,P
CB-F019,DS-F019,P
DS-F019,MOV-RCIC-B,P
MCC-1B,CB-F020,P
CB-F020,MS-F020,P
MS-F020,PUMP-CCW-B,P
MCC-1B,CB-F021,P
CB-F021,FU-F021,P
FU-F021,HTR-SUMP-B,P
MCC-1B,CB-F022,P
CB-F022,MS-F022,P
MS-F022,PMP-BOR-B,P
MCC-1B,CB-F023,P
CB-F023,DS-F023,P
DS-F023,VALVE-IA-B,P
BUS-480-D,CB-M2B,P
CB-M2B,MCC-2B,P
MCC-2B,CB-F024,P
CB-F024,MS-F024,P
MS-F024,PUMP-AFW-B,P
MCC-2B,CB-F025,P
CB-F025,MS-F025,P
MS-F025,PMP-LUBE-B,P
MCC-2B,CB-F026,P
CB-F026,DS-F026,P
DS-F026,MOV-RHR-B,P
MCC-2B,CB-F027,P
CB-F027,FU-F027,P
FU-F027,FAN-BLDG-B,P
MCC-2B,CB-F028,P
CB-F028,FU-F028,P
FU-F028,PNL-RAD-B,P
MCC-2B,CB-F029,P
CB-F029,MS-F029,P
MS-F029,PUMP-SW-B,P
BUS-480-D,CB-DC-1B,P
CB-DC-1B,CHGR-125B,P
CHGR-125B,DC-BUS-B,P
BAT-125B,DC-BUS-B,P
DC-BUS-B,INV-1B,P
INV-1A,ATS-INV,P
INV-1B,ATS-INV,P
ATS-INV,BUS-120VAC-ESF,P
BUS-120VAC-ESF,PNL-ESFAS-A,P
BUS-120VAC-ESF,PNL-ESFAS-B,P
ANN-480A,RELAY-27A,I
ANN-480A,TB-ANN-1,SIG
RELAY-27A,TB-RPS-A,D
RELAY-50A,TB-RPS-A,D
RELAY-50A,RELAY-86A,D
RELAY-86A,TB-RPS-A,D
TB-RPS-A,PNL-RPS-A,D
PNL-RPS-A,PNL-ESFAS-A,D
PNL-ESFAS-A,SEQ-REC-1,SIG
PNL-RPS-A,GND-1,G
ANN-480B,RELAY-27B,I
RELAY-27B,TB-RPS-B,D
RELAY-50B,TB-RPS-B,D
RELAY-50B,RELAY-86B,D
RELAY-86B,TB-RPS-B,D
TB-RPS-B,PNL-RPS-B,D
PNL-RPS-B,PNL-ESFAS-B,D
PNL-ESFAS-B,SEQ-REC-1,SIG
PNL-RPS-B,GND-2,G
"""


FINAL_REMOVED_EDGES = {
    ("BUS-4KV-A", "PT-4160A"),
    ("BUS-4KV-B", "PT-4160B"),
    ("BUS-120VAC-ESF", "PNL-ESFAS-A"),
    ("BUS-120VAC-ESF", "PNL-ESFAS-B"),
    ("PNL-ESFAS-B", "SEQ-REC-1"),
}


FINAL_TYPE_CHANGES = {
    ("ANN-480A", "RELAY-27A"): "D",
    ("ANN-480B", "RELAY-27B"): "D",
}


ROUND_NOTES = {
    "round01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "summary": "Initial extraction included visible PT nodes with tentative PT-to-bus signal edges and several lower ESF/RPS signal/power candidates.",
    },
    "round01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "summary": "Kept node list, removed unlanded PT-to-bus and ESF-bus-to-panel edges, removed unlanded ESFAS-B-to-sequence-recorder edge, and corrected ANN-to-27 edge types.",
    },
    "round02_diego": {
        "agent": "Diego",
        "role": "high-recall saturation review",
        "summary": "Agreed with Jennifer's corrected final candidate.",
    },
    "round02_jennifer": {
        "agent": "Jennifer",
        "role": "precision final signoff",
        "summary": "Final precision signoff after Diego saturation response.",
    },
}


EXCLUDED_OR_UNCERTAIN = [
    "BUS-4KV-A,PT-4160A,SIG",
    "BUS-4KV-B,PT-4160B,SIG",
    "BUS-120VAC-ESF,PNL-ESFAS-A,P",
    "BUS-120VAC-ESF,PNL-ESFAS-B,P",
    "PNL-ESFAS-B,SEQ-REC-1,SIG",
    "CB-M1A,CB-M2A,I",
    "CB-M1B,CB-M2B,I",
    "CB-111,CB-211,I",
    "CB-112,CB-212,I",
    "ATS-INV,DC-BUS-A,D",
    "ATS-INV,DC-BUS-B,D",
    "BUS-120VAC-ESF,SEQ-REC-1,SIG",
    "TB-ANN-1,PNL-ESFAS-A,SIG",
    "ANN-480A,PNL-ESFAS-A,SIG",
    "ANN-480B,PNL-ESFAS-B,SIG",
    "RELAY-27A,RELAY-86A,D",
    "RELAY-27B,RELAY-86B,D",
    "TB-RPS-A,PNL-ESFAS-A,D",
    "TB-RPS-B,PNL-ESFAS-B,D",
    "ANN-480A,RELAY-50A,D",
    "ANN-480B,RELAY-50B,D",
    "BUS-480-C,MCC-2A,P",
    "BUS-480-D,MCC-2B,P",
]


def edge_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def parse_nodes(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_edges(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    reader = csv.DictReader(line for line in text.splitlines() if line.strip())
    for row in reader:
        a = row["A"].strip()
        b = row["B"].strip()
        kind = row["type"].strip()
        key = edge_key(a, b)
        if key in seen:
            raise ValueError(f"Duplicate undirected edge: {a} -- {b}")
        seen.add(key)
        rows.append({"A": a, "B": b, "type": kind})
    return rows


def derive_final_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    removed = {edge_key(a, b) for a, b in FINAL_REMOVED_EDGES}
    type_changes = {edge_key(a, b): kind for (a, b), kind in FINAL_TYPE_CHANGES.items()}
    final: list[dict[str, str]] = []
    for edge in edges:
        key = edge_key(edge["A"], edge["B"])
        if key in removed:
            continue
        final.append({"A": edge["A"], "B": edge["B"], "type": type_changes.get(key, edge["type"])})
    return final


def validate(nodes: list[str], edges: list[dict[str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        raise ValueError("Duplicate node names found")
    node_set = set(nodes)
    missing = sorted({endpoint for edge in edges for endpoint in (edge["A"], edge["B"]) if endpoint not in node_set})
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
        adjacency[edge["A"]][edge["B"]] = 1
        adjacency[edge["B"]][edge["A"]] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [adjacency[node][other] for other in nodes])


def write_sparse_pairs(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    edge_types = {edge_key(edge["A"], edge["B"]): edge["type"] for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "connected", "type"])
        for i, a in enumerate(nodes):
            for b in nodes[i + 1 :]:
                key = edge_key(a, b)
                writer.writerow([a, b, 1 if key in edge_types else 0, edge_types.get(key, "")])


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
        "# Document 12 Connectivity Extraction Report",
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
            "## Final Precision Changes From Diego R1",
            "",
            "- Removed unlanded PT-to-bus signal edges while retaining `PT-4160A` and `PT-4160B` as visible component nodes.",
            "- Removed unlanded `BUS-120VAC-ESF` to `PNL-ESFAS-A/B` edges.",
            "- Removed unlanded `PNL-ESFAS-B` to `SEQ-REC-1` signal edge.",
            "- Changed `ANN-480A/B` to `RELAY-27A/B` from interlock type to dashed control type.",
            "- Kept `SPARE-A2` because the visible spare box is landed by `DS-F015`.",
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
    nodes = parse_nodes(NODES_TEXT)
    diego_r1_edges = parse_edges(DIEGO_R1_EDGES_CSV)
    final_edges = derive_final_edges(diego_r1_edges)

    rounds = [
        write_round_artifacts("round01_diego", nodes, diego_r1_edges),
        write_round_artifacts("round01_jennifer", nodes, final_edges),
        write_round_artifacts("round02_diego", nodes, final_edges),
        write_round_artifacts("round02_jennifer", nodes, final_edges),
    ]

    write_nodes(RESULTS_DIR / "final_nodes.txt", nodes)
    write_edges(RESULTS_DIR / "final_sparse_edges.csv", final_edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", nodes, final_edges)
    write_sparse_pairs(RESULTS_DIR / "final_sparse_matrix_pairs.csv", nodes, final_edges)
    (RESULTS_DIR / "rounds_connectivity.json").write_text(json.dumps(rounds, indent=2), encoding="utf-8")
    write_report(rounds, nodes, final_edges)

    print(json.dumps({"final_nodes": len(nodes), "final_edges": len(final_edges), "rounds": rounds}, indent=2))


if __name__ == "__main__":
    main()
