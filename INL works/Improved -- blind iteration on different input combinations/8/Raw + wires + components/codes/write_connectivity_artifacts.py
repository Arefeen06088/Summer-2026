from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


FINAL_NODES_TEXT = """
GRID-345-01, GRID-345-02, GEN-U2, EDG-2A, EDG-2B, EDG-2C, SUT-2A, SUT-2B, UAT-2A, UAT-2B, CB-401A, CB-401B, CB-402A, CB-402B, CB-TIE-4160, CB-EDG-A, CB-EDG-B, CB-EDG-C, BUS-4160-N2A, BUS-4160-N2B, BUS-4160-S2A, BUS-4160-S2B, TR-480-2A, TR-480-2B, TR-480-N2A, TR-480-N2B, BUS-480-E2A, BUS-480-E2B, BUS-480-N2A, BUS-480-N2B, DS-480-A, DS-480-B, MCC-2A1, MCC-2A2, MCC-2B1, MCC-2B2, MCC-2C, MCC-2D, PN-480-A, PN-480-B, CB-N1, CB-N2, GND-A, GND-B, CB-51A, CB-52A, CB-53A, CB-54A, CB-55A, CB-56A, CB-57A, CB-58A, CB-51B, CB-52B, CB-53B, CB-54B, CB-55B, CB-56B, CB-57B, CB-58B, PUMP-SI-2A, PUMP-RHR-2A, PUMP-CS-2A, PUMP-CCW-2A, FAN-CRE-2A, MOV-8801A, MOV-8802A, PUMP-AF-2A, MOV-8810A, PUMP-CHG-2A, VLV-HV-302A, FAN-VENT-2A, PUMP-SI-2B, PUMP-RHR-2B, PUMP-CS-2B, PUMP-CCW-2B, FAN-CRE-2B, MOV-8801B, MOV-8802B, PUMP-AF-2B, MOV-8810B, PUMP-CHG-2B, VLV-HV-302B, FAN-VENT-2B, CHGR-125A, BAT-2A, INV-120A, BUS-125DC-A, BUS-120AC-A, FUSE-125A, PN-125A, FUSE-120A, PN-120A, CP-ESFAS-A, CP-RPS-A, JB-2A1, RELAY-K1A, CHGR-125B, BAT-2B, INV-120B, BUS-125DC-B, BUS-120AC-B, FUSE-125B, PN-125B, FUSE-120B, PN-120B, CP-ESFAS-B, CP-RPS-B, JB-2B1, RELAY-K1B, CT-4160A, PT-4160A, RELAY-50/51A, RELAY-27A, RELAY-86A, CT-4160B, PT-4160B, RELAY-50/51B, RELAY-27B, RELAY-86B
"""


FINAL_EDGES_TEXT = """
GRID-345-01,SUT-2A,S
SUT-2A,CB-402A,S
CB-402A,BUS-4160-N2A,S
GEN-U2,UAT-2A,S
UAT-2A,CB-401A,S
CB-401A,BUS-4160-N2A,S
BUS-4160-N2A,CB-TIE-4160,S
CB-TIE-4160,BUS-4160-N2B,S
GEN-U2,UAT-2B,S
UAT-2B,CB-401B,S
CB-401B,BUS-4160-N2B,S
GRID-345-02,SUT-2B,S
SUT-2B,CB-402B,S
CB-402B,BUS-4160-N2B,S
BUS-4160-N2A,BUS-4160-S2A,S
BUS-4160-N2B,BUS-4160-S2B,S
EDG-2A,CB-EDG-A,S
CB-EDG-A,BUS-4160-S2A,S
EDG-2B,CB-EDG-B,S
CB-EDG-B,BUS-4160-S2B,S
EDG-2C,CB-EDG-C,S
CB-EDG-C,BUS-4160-S2A,S
CB-EDG-C,BUS-4160-S2B,S
BUS-4160-S2A,TR-480-2A,S
TR-480-2A,BUS-480-E2A,S
BUS-4160-S2B,TR-480-2B,S
TR-480-2B,BUS-480-E2B,S
BUS-4160-N2A,TR-480-N2A,S
TR-480-N2A,BUS-480-N2A,S
BUS-4160-N2B,TR-480-N2B,S
TR-480-N2B,BUS-480-N2B,S
BUS-480-N2A,DS-480-A,S
DS-480-A,DS-480-B,S
DS-480-B,BUS-480-N2B,S
BUS-480-E2A,MCC-2A1,S
BUS-480-E2A,MCC-2A2,S
BUS-480-E2A,PN-480-A,S
BUS-480-E2A,GND-A,G
BUS-480-N2A,CB-N1,S
CB-N1,CHGR-125A,S
PN-480-A,MCC-2C,S
PN-480-A,MOV-8810A,S
PN-480-A,VLV-HV-302A,S
MCC-2C,PUMP-CHG-2A,S
MCC-2C,FAN-VENT-2A,S
BUS-480-E2B,MCC-2B1,S
BUS-480-E2B,MCC-2B2,S
BUS-480-E2B,PN-480-B,S
BUS-480-E2B,GND-B,G
BUS-480-N2B,CB-N2,S
CB-N2,MCC-2D,S
PN-480-B,MOV-8810B,S
PN-480-B,VLV-HV-302B,S
MCC-2D,PUMP-CHG-2B,S
MCC-2D,FAN-VENT-2B,S
MCC-2A1,CB-51A,S
CB-51A,PUMP-SI-2A,S
MCC-2A1,CB-52A,S
CB-52A,PUMP-RHR-2A,S
MCC-2A1,CB-53A,S
CB-53A,PUMP-CS-2A,S
MCC-2A1,CB-54A,S
CB-54A,PUMP-CCW-2A,S
MCC-2A2,CB-55A,S
CB-55A,FAN-CRE-2A,S
MCC-2A2,CB-56A,S
CB-56A,MOV-8801A,S
MCC-2A2,CB-57A,S
CB-57A,MOV-8802A,S
MCC-2A2,CB-58A,S
CB-58A,PUMP-AF-2A,S
MCC-2B1,CB-51B,S
CB-51B,PUMP-SI-2B,S
MCC-2B1,CB-52B,S
CB-52B,PUMP-RHR-2B,S
MCC-2B1,CB-53B,S
CB-53B,PUMP-CS-2B,S
MCC-2B1,CB-54B,S
CB-54B,PUMP-CCW-2B,S
MCC-2B2,CB-55B,S
CB-55B,FAN-CRE-2B,S
MCC-2B2,CB-56B,S
CB-56B,MOV-8801B,S
MCC-2B2,CB-57B,S
CB-57B,MOV-8802B,S
MCC-2B2,CB-58B,S
CB-58B,PUMP-AF-2B,S
PUMP-AF-2B,JB-2B1,I
BUS-125DC-A,CHGR-125A,D
BUS-125DC-A,BAT-2A,D
CHGR-125A,BAT-2A,D
BUS-125DC-A,INV-120A,D
BUS-125DC-A,FUSE-125A,D
FUSE-125A,PN-125A,D
PN-125A,CP-ESFAS-A,D
BUS-120AC-A,INV-120A,D
BUS-120AC-A,FUSE-120A,D
FUSE-120A,PN-120A,D
PN-120A,CP-RPS-A,D
BUS-125DC-B,CHGR-125B,D
BUS-125DC-B,BAT-2B,D
CHGR-125B,BAT-2B,D
BUS-125DC-B,INV-120B,D
BUS-125DC-B,FUSE-125B,D
FUSE-125B,PN-125B,D
PN-125B,CP-ESFAS-B,D
BUS-120AC-B,INV-120B,D
BUS-120AC-B,FUSE-120B,D
FUSE-120B,PN-120B,D
PN-120B,CP-RPS-B,D
BUS-4160-S2A,CT-4160A,CT
CT-4160A,RELAY-50/51A,CT
BUS-4160-S2A,PT-4160A,CT
PT-4160A,RELAY-27A,CT
RELAY-50/51A,RELAY-86A,I
RELAY-27A,RELAY-86A,I
RELAY-86A,CB-EDG-A,I
RELAY-86A,CB-401A,I
BUS-4160-S2B,CT-4160B,CT
CT-4160B,RELAY-50/51B,CT
BUS-4160-S2B,PT-4160B,CT
PT-4160B,RELAY-27B,CT
RELAY-50/51B,RELAY-86B,I
RELAY-27B,RELAY-86B,I
RELAY-86B,CB-EDG-B,I
RELAY-86B,CB-401B,I
CB-51A,RELAY-K1A,I
CB-52A,RELAY-K1A,I
CB-53A,RELAY-K1A,I
MOV-8801A,JB-2A1,I
VLV-HV-302A,JB-2A1,I
JB-2A1,RELAY-K1A,I
RELAY-K1A,CP-ESFAS-A,I
CB-51B,RELAY-K1B,I
CB-52B,RELAY-K1B,I
CB-53B,RELAY-K1B,I
MOV-8801B,JB-2B1,I
VLV-HV-302B,JB-2B1,I
JB-2B1,RELAY-K1B,I
RELAY-K1B,CP-ESFAS-B,I
"""


JENNIFER_ADDED_TEXT = """
PUMP-AF-2B,JB-2B1,I
CHGR-125A,BAT-2A,D
CHGR-125B,BAT-2B,D
"""


def parse_nodes(text: str) -> list[str]:
    return [part.strip() for part in text.replace("\n", ",").split(",") if part.strip()]


def parse_edges(text: str) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for raw in text.strip().splitlines():
        if not raw.strip() or raw.lower().startswith("a,b"):
            continue
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) != 3:
            raise ValueError(f"Expected edge row A,B,type; got {raw!r}")
        edges.append((parts[0], parts[1], parts[2]))
    return edges


FINAL_NODES = parse_nodes(FINAL_NODES_TEXT)
FINAL_EDGES = parse_edges(FINAL_EDGES_TEXT)
JENNIFER_ADDED = set(parse_edges(JENNIFER_ADDED_TEXT))
DIEGO_R1_EDGES = [edge for edge in FINAL_EDGES if edge not in JENNIFER_ADDED]


ROUNDS = [
    {
        "round": 1,
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "proposal_with_uncertain_candidates",
        "nodes": FINAL_NODES,
        "edges": DIEGO_R1_EDGES,
        "notes": [
            "Initial high-recall proposal from raw image and visual aids.",
            "Uncertain candidates included CB-54A/B interlock routes, PUMP-AF-2A/B to JB, charger source alternatives, and TB references.",
            "Accepted proposal had 120 nodes and 137 edges before Jennifer's additions.",
        ],
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "status": "refined",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": [
            "Added PUMP-AF-2B--JB-2B1, CHGR-125A--BAT-2A, and CHGR-125B--BAT-2B.",
            "Rejected unsupported CB-54A/B interlock routes, PUMP-AF-2A--JB-2A1, PN-480 charger routes, CB-N1--MCC-2C, CB-N2--CHGR-125B, and TB01-TB15 graph edges.",
        ],
    },
    {
        "round": 3,
        "agent": "Diego",
        "role": "saturation extractor",
        "status": "saturated_agreed",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": [
            "AGREED with Jennifer final matrix.",
            "Confirmed the final edge set is R1 accepted edges plus PUMP-AF-2B--JB-2B1, CHGR-125A--BAT-2A, and CHGR-125B--BAT-2B.",
            "Confirmed rejected uncertain edges stay out.",
        ],
    },
    {
        "round": 4,
        "agent": "Jennifer",
        "role": "final precision sign-off",
        "status": "saturated_agreed",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": [
            "SATURATED / AGREED.",
            "Final graph is 120 nodes and 140 accepted undirected edges.",
            "No final correction.",
        ],
    },
]


def matrix_for(nodes: list[str], edges: list[tuple[str, str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    if len(index) != len(nodes):
        duplicates = [node for node, count in Counter(nodes).items() if count > 1]
        raise ValueError(f"Duplicate node name(s): {duplicates}")

    matrix = [[0 for _ in nodes] for _ in nodes]
    seen_pairs: set[tuple[str, str]] = set()
    for a, b, _kind in edges:
        if a not in index or b not in index:
            raise ValueError(f"Edge references unknown node: {a!r}, {b!r}")
        if a == b:
            raise ValueError(f"Self-loop is not expected: {a}")
        pair = tuple(sorted((a, b)))
        if pair in seen_pairs:
            raise ValueError(f"Duplicate undirected edge: {pair}")
        seen_pairs.add(pair)
        i, j = index[a], index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

    for i in range(len(nodes)):
        if matrix[i][i] != 0:
            raise ValueError("Diagonal must remain zero")
        for j in range(len(nodes)):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Matrix is not symmetric")
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    matrix = matrix_for(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_sparse(path: Path, edges: list[tuple[str, str, str]], value_column: str = "type") -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["A", "B", value_column])
        for a, b, kind in edges:
            writer.writerow([a, b, kind if value_column == "type" else 1])


def summarize_round(round_data: dict) -> dict:
    type_counts = Counter(kind for _a, _b, kind in round_data["edges"])
    return {
        "round": round_data["round"],
        "agent": round_data["agent"],
        "status": round_data["status"],
        "node_count": len(round_data["nodes"]),
        "edge_count": len(round_data["edges"]),
        "type_counts": dict(sorted(type_counts.items())),
    }


def serializable_round(round_data: dict) -> dict:
    return {
        "round": round_data["round"],
        "agent": round_data["agent"],
        "role": round_data["role"],
        "status": round_data["status"],
        "nodes": round_data["nodes"],
        "edges": [
            {"A": a, "B": b, "type": kind}
            for a, b, kind in round_data["edges"]
        ],
        "notes": round_data["notes"],
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds_dir = RESULTS / "round_matrices"
    rounds_dir.mkdir(exist_ok=True)

    summaries = []
    for round_data in ROUNDS:
        prefix = f"round_{round_data['round']:02d}_{round_data['agent'].lower()}"
        write_sparse(rounds_dir / f"{prefix}_sparse_edges.csv", round_data["edges"])
        write_matrix(rounds_dir / f"{prefix}_connectivity_matrix.csv", round_data["nodes"], round_data["edges"])
        (rounds_dir / f"{prefix}_nodes.txt").write_text(
            "\n".join(round_data["nodes"]) + "\n", encoding="utf-8"
        )
        summaries.append(summarize_round(round_data))

    write_sparse(RESULTS / "final_sparse_edges.csv", FINAL_EDGES)
    write_sparse(RESULTS / "final_sparse_matrix_pairs.csv", FINAL_EDGES, value_column="value")
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    (RESULTS / "final_nodes.txt").write_text("\n".join(FINAL_NODES) + "\n", encoding="utf-8")

    payload = {
        "document": 8,
        "iteration": 1,
        "resource_location": str(ROOT),
        "method": "raw schematic plus visual aids only; no GT and no OCR",
        "node_count_final": len(FINAL_NODES),
        "edge_count_final": len(FINAL_EDGES),
        "round_summaries": summaries,
        "rounds": [serializable_round(round_data) for round_data in ROUNDS],
    }
    (RESULTS / "rounds_connectivity.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    headers = sorted({kind for _a, _b, kind in FINAL_EDGES})
    report_lines = [
        "# Connectivity Extraction - Document 8",
        "",
        "Raw schematic and visual aids only; no GT or OCR.",
        "",
        "| Round | Agent | Status | Nodes | Edges | " + " | ".join(headers) + " |",
        "|---:|---|---|---:|---:|" + "|".join("---:" for _ in headers) + "|",
    ]
    for summary in summaries:
        counts = summary["type_counts"]
        report_lines.append(
            f"| {summary['round']} | {summary['agent']} | {summary['status']} | "
            f"{summary['node_count']} | {summary['edge_count']} | "
            + " | ".join(str(counts.get(kind, 0)) for kind in headers)
            + " |"
        )
    report_lines.extend(
        [
            "",
            f"Final matrix: {len(FINAL_NODES)} nodes, {len(FINAL_EDGES)} undirected edges.",
            "Matrix values are 1 for accepted solid, dashed/control, CT/PT, interlock, and ground connections; 0 otherwise.",
        ]
    )
    (RESULTS / "connectivity_extraction_report.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(payload["round_summaries"], indent=2))


if __name__ == "__main__":
    main()
