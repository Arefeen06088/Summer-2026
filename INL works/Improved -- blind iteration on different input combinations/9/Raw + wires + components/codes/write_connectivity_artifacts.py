from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


FINAL_NODES_TEXT = """
UTIL-230A, DS-230A, SAT-1A, CB-SAT-A, GEN-1A, CB-GEN-1, BUS-13K-01, UAT-1A, CB-UAT-1A, UAT-1B, CB-UAT-1B, UTIL-230B, DS-230B, SAT-1B, CB-SAT-B,
BUS-4160-N1, CB-TIE-41N, BUS-4160-N2,
EDG-1A, CB-EDG-A, BUS-4160S1A, CT-41A, PT-41A, RELAY-50/51A, RELAY-86A, CB-481A, TR-480-A1, CB-LV-A1, BUS-480-A1, MCC-SAF-A1, CB-RHR-A, PUMP-RHR-A, CB-SI-A, PUMP-SI-A, CB-CCW-A, PUMP-CCW-A, CB-482A, TR-480-A2, CB-LV-A2, BUS-480-A2, MCC-SAF-A2, CB-CVC-A, PUMP-CVC-A, CB-CRF-A, FAN-CR-A, CB-COMP-A, COMP-AIR-A, PN-MOV-A, FU-8810A, MOV-8810A, FU-HV302A, VLV-HV-302A, FU-RCICA, MOV-RCIC-A, FU-SWA, MOV-SW-A,
CB-4160-N1A, TR-480-N1A, CB-480-N1A, BUS-480-N1A, MCC-NORM-1A, PN-480-N1A, CB-CWP-1A, PUMP-CWP-1A, CB-HEAT-1A, HTR-1A, CB-AHU-1A, FAN-AHU-1A, CB-4160-N1B, TR-480-N1B, CB-480-N1B, BUS-480-N1B, MCC-NORM-1B, PN-480-N1B, CB-CWP-1B, PUMP-CWP-1B, CB-SUMP-1B, PUMP-SUMP-1B, CB-LTG-1B, PN-LTG-1B,
CB-4160-N2A, TR-480-N2A, CB-480-N2A, BUS-480-N2A, MCC-NORM-2A, PN-480-N2A, CB-CWP-2A, PUMP-CWP-2A, CB-VAC-2A, PUMP-VAC-2A, CB-AHU-2A, FAN-AHU-2A, CB-4160-N2B, TR-480-N2B, CB-480-N2B, BUS-480-N2B, MCC-NORM-2B, PN-480-N2B, CB-CWP-2B, PUMP-CWP-2B, CB-OIL-2B, PUMP-OIL-2B, CB-LTG-2B, PN-LTG-2B, MTR-480-N1, MTR-480-N2, JB-NORM-A, JB-NORM-B, RTD-PNL-A, RTD-PNL-B, TB-SEQ-A, TB-SEQ-B, TDR-SEQ-A, TDR-SEQ-B,
EDG-1B, CB-EDG-B, BUS-4160S1B, CT-41B, PT-41B, RELAY-27B, RELAY-86B, CB-481B, TR-480-B1, CB-LV-B1, BUS-480-B1, MCC-SAF-B1, CB-RHR-B, PUMP-RHR-B, CB-SI-B, PUMP-SI-B, CB-CCW-B, PUMP-CCW-B, CB-482B, TR-480-B2, CB-LV-B2, BUS-480-B2, MCC-SAF-B2, CB-CVC-B, PUMP-CVC-B, CB-CRF-B, FAN-CR-B, CB-COMP-B, COMP-AIR-B, PN-MOV-B, FU-8810B, MOV-8810B, FU-HV302B, VLV-HV-302B, FU-RCICB, MOV-RCIC-B, FU-SWB, MOV-SW-B,
BAT-125A, CHG-125A, BUS-125DC-A, INV-120A, BUS-120AC-A, GND-A, PN-125A, JB-1A, JB-2A, PN-120A, PLC-ESF-A, ANN-ESF-A, RELAY-K1A, RELAY-K2A,
BAT-125B, CHG-125B, BUS-125DC-B, INV-120B, BUS-120AC-B, GND-B, PN-125B, JB-1B, JB-2B, PN-120B, PLC-ESF-B, ANN-ESF-B, RELAY-K1B, RELAY-K2B
"""


DIEGO_R1_EDGES_TEXT = """
UTIL-230A,DS-230A,S
DS-230A,SAT-1A,S
SAT-1A,CB-SAT-A,S
CB-SAT-A,BUS-4160S1A,S
GEN-1A,CB-GEN-1,S
CB-GEN-1,BUS-13K-01,S
BUS-13K-01,UAT-1A,S
UAT-1A,CB-UAT-1A,S
CB-UAT-1A,BUS-4160-N1,S
BUS-13K-01,UAT-1B,S
UAT-1B,CB-UAT-1B,S
CB-UAT-1B,BUS-4160-N2,S
UTIL-230B,DS-230B,S
DS-230B,SAT-1B,S
SAT-1B,CB-SAT-B,S
CB-SAT-B,BUS-4160S1B,S
BUS-4160-N1,CB-TIE-41N,S
CB-TIE-41N,BUS-4160-N2,S
EDG-1A,CB-EDG-A,S
CB-EDG-A,BUS-4160S1A,S
BUS-4160S1A,CB-481A,S
CB-481A,TR-480-A1,S
TR-480-A1,CB-LV-A1,S
CB-LV-A1,BUS-480-A1,S
BUS-480-A1,MCC-SAF-A1,S
MCC-SAF-A1,CB-RHR-A,S
CB-RHR-A,PUMP-RHR-A,S
MCC-SAF-A1,CB-SI-A,S
CB-SI-A,PUMP-SI-A,S
MCC-SAF-A1,CB-CCW-A,S
CB-CCW-A,PUMP-CCW-A,S
BUS-4160S1A,CB-482A,S
CB-482A,TR-480-A2,S
TR-480-A2,CB-LV-A2,S
CB-LV-A2,BUS-480-A2,S
BUS-480-A2,MCC-SAF-A2,S
MCC-SAF-A2,CB-CVC-A,S
CB-CVC-A,PUMP-CVC-A,S
MCC-SAF-A2,CB-CRF-A,S
CB-CRF-A,FAN-CR-A,S
FAN-CR-A,PN-MOV-A,S
MCC-SAF-A2,CB-COMP-A,S
CB-COMP-A,COMP-AIR-A,S
PN-MOV-A,FU-8810A,S
FU-8810A,MOV-8810A,S
PN-MOV-A,FU-HV302A,S
FU-HV302A,VLV-HV-302A,S
PN-MOV-A,FU-RCICA,S
FU-RCICA,MOV-RCIC-A,S
PN-MOV-A,FU-SWA,S
FU-SWA,MOV-SW-A,S
BUS-4160S1A,CT-41A,CT
CT-41A,RELAY-50/51A,CT
BUS-4160S1A,PT-41A,CT
PT-41A,RELAY-50/51A,CT
RELAY-50/51A,RELAY-86A,I
BUS-4160-N1,CB-4160-N1A,S
CB-4160-N1A,TR-480-N1A,S
TR-480-N1A,CB-480-N1A,S
CB-480-N1A,BUS-480-N1A,S
BUS-480-N1A,MCC-NORM-1A,S
MCC-NORM-1A,PN-480-N1A,S
PN-480-N1A,CB-CWP-1A,S
CB-CWP-1A,PUMP-CWP-1A,S
PN-480-N1A,CB-HEAT-1A,S
CB-HEAT-1A,HTR-1A,S
PN-480-N1A,CB-AHU-1A,S
CB-AHU-1A,FAN-AHU-1A,S
BUS-4160-N1,CB-4160-N1B,S
CB-4160-N1B,TR-480-N1B,S
TR-480-N1B,CB-480-N1B,S
CB-480-N1B,BUS-480-N1B,S
BUS-480-N1B,MCC-NORM-1B,S
MCC-NORM-1B,PN-480-N1B,S
PN-480-N1B,CB-CWP-1B,S
CB-CWP-1B,PUMP-CWP-1B,S
PN-480-N1B,CB-SUMP-1B,S
CB-SUMP-1B,PUMP-SUMP-1B,S
PN-480-N1B,CB-LTG-1B,S
CB-LTG-1B,PN-LTG-1B,S
PN-480-N1A,PN-480-N1B,D
PUMP-SUMP-1B,MTR-480-N1,D
MTR-480-N1,JB-NORM-A,D
BUS-4160-N2,CB-4160-N2A,S
CB-4160-N2A,TR-480-N2A,S
TR-480-N2A,CB-480-N2A,S
CB-480-N2A,BUS-480-N2A,S
BUS-480-N2A,MCC-NORM-2A,S
MCC-NORM-2A,PN-480-N2A,S
PN-480-N2A,CB-CWP-2A,S
CB-CWP-2A,PUMP-CWP-2A,S
PN-480-N2A,CB-VAC-2A,S
CB-VAC-2A,PUMP-VAC-2A,S
PN-480-N2A,CB-AHU-2A,S
CB-AHU-2A,FAN-AHU-2A,S
BUS-4160-N2,CB-4160-N2B,S
CB-4160-N2B,TR-480-N2B,S
TR-480-N2B,CB-480-N2B,S
CB-480-N2B,BUS-480-N2B,S
BUS-480-N2B,MCC-NORM-2B,S
MCC-NORM-2B,PN-480-N2B,S
PN-480-N2B,CB-CWP-2B,S
CB-CWP-2B,PUMP-CWP-2B,S
PN-480-N2B,CB-OIL-2B,S
CB-OIL-2B,PUMP-OIL-2B,S
PN-480-N2B,CB-LTG-2B,S
CB-LTG-2B,PN-LTG-2B,S
PN-480-N2A,PN-480-N2B,D
FAN-AHU-2A,MTR-480-N2,D
MTR-480-N2,JB-NORM-B,D
JB-NORM-A,RTD-PNL-A,D
RTD-PNL-A,TB-SEQ-A,D
TB-SEQ-A,TDR-SEQ-A,D
JB-NORM-B,RTD-PNL-B,D
RTD-PNL-B,TB-SEQ-B,D
TB-SEQ-B,TDR-SEQ-B,D
EDG-1B,CB-EDG-B,S
CB-EDG-B,BUS-4160S1B,S
BUS-4160S1B,CB-481B,S
CB-481B,TR-480-B1,S
TR-480-B1,CB-LV-B1,S
CB-LV-B1,BUS-480-B1,S
BUS-480-B1,MCC-SAF-B1,S
MCC-SAF-B1,CB-RHR-B,S
CB-RHR-B,PUMP-RHR-B,S
MCC-SAF-B1,CB-SI-B,S
CB-SI-B,PUMP-SI-B,S
MCC-SAF-B1,CB-CCW-B,S
CB-CCW-B,PUMP-CCW-B,S
BUS-4160S1B,CB-482B,S
CB-482B,TR-480-B2,S
TR-480-B2,CB-LV-B2,S
CB-LV-B2,BUS-480-B2,S
BUS-480-B2,MCC-SAF-B2,S
MCC-SAF-B2,CB-CVC-B,S
CB-CVC-B,PUMP-CVC-B,S
MCC-SAF-B2,CB-CRF-B,S
CB-CRF-B,FAN-CR-B,S
MCC-SAF-B2,CB-COMP-B,S
CB-COMP-B,COMP-AIR-B,S
MCC-SAF-B2,PN-MOV-B,S
PN-MOV-B,FU-8810B,S
FU-8810B,MOV-8810B,S
PN-MOV-B,FU-HV302B,S
FU-HV302B,VLV-HV-302B,S
PN-MOV-B,FU-RCICB,S
FU-RCICB,MOV-RCIC-B,S
PN-MOV-B,FU-SWB,S
FU-SWB,MOV-SW-B,S
BUS-4160S1B,CT-41B,CT
CT-41B,RELAY-27B,CT
BUS-4160S1B,PT-41B,CT
PT-41B,RELAY-27B,CT
RELAY-27B,RELAY-86B,I
RELAY-27B,CB-481B,I
BAT-125A,BUS-125DC-A,S
CHG-125A,BUS-125DC-A,S
BUS-125DC-A,INV-120A,S
INV-120A,BUS-120AC-A,S
BUS-125DC-A,PN-125A,S
BUS-125DC-A,GND-A,G
BUS-120AC-A,PN-120A,S
PN-125A,JB-1A,D
PN-125A,JB-2A,D
PN-120A,PLC-ESF-A,I
PLC-ESF-A,ANN-ESF-A,I
PLC-ESF-A,RELAY-K1A,I
PLC-ESF-A,RELAY-K2A,I
RELAY-K2A,ANN-ESF-A,D
BAT-125B,BUS-125DC-B,S
CHG-125B,BUS-125DC-B,S
BUS-125DC-B,INV-120B,S
INV-120B,BUS-120AC-B,S
BUS-125DC-B,PN-125B,S
BUS-125DC-B,GND-B,G
BUS-120AC-B,PN-120B,S
PN-125B,JB-1B,D
PN-125B,JB-2B,D
PN-120B,PLC-ESF-B,I
PLC-ESF-B,ANN-ESF-B,I
PLC-ESF-B,RELAY-K1B,I
PLC-ESF-B,RELAY-K2B,I
RELAY-K2B,ANN-ESF-B,D
"""


UNCERTAIN_CANDIDATES = [
    "CB-EDG-A,CB-482A,I",
    "CB-482A,RELAY-50/51A,I",
    "CB-482A,RELAY-86A,I",
    "CB-TIE-41N,RELAY-86A,I",
    "CB-TIE-41N,RELAY-86B,I",
    "RELAY-86B,CB-481B,I",
    "RELAY-86B,CB-482B,I",
    "MCC-SAF-A1,MCC-SAF-A2,D",
    "MCC-SAF-B1,MCC-SAF-B2,D",
    "PUMP-RHR-A,PUMP-SI-A,D",
    "PUMP-RHR-B,PUMP-SI-B,D",
    "PN-MOV-A,PN-120A,D",
    "PN-MOV-A,PLC-ESF-A,D",
    "PN-MOV-B,PN-120B,D",
    "PN-MOV-B,PLC-ESF-B,D",
    "PN-125A,PN-120A,D",
    "PN-125B,PN-120B,D",
    "RTD-PNL-A,RTD-PNL-B,D",
    "PN-480-N1B,CB-SUMP-1B,D",
    "PN-480-N2A,CB-AHU-2A,D",
]


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
DIEGO_R1_EDGES = parse_edges(DIEGO_R1_EDGES_TEXT)
FINAL_EDGES = [
    edge for edge in DIEGO_R1_EDGES if edge != ("FAN-CR-A", "PN-MOV-A", "S")
] + [("MCC-SAF-A2", "PN-MOV-A", "S")]


ROUNDS = [
    {
        "round": 1,
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "proposal_with_uncertain_candidates",
        "nodes": FINAL_NODES,
        "edges": DIEGO_R1_EDGES,
        "notes": [
            "High-recall accepted edge list plus separate uncertain candidates.",
            "Jennifer later found the A-side MOV panel feeder should land on MCC-SAF-A2 rather than FAN-CR-A.",
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
            "Removed FAN-CR-A--PN-MOV-A because the line appears to pass near the fan branch.",
            "Added MCC-SAF-A2--PN-MOV-A, matching the visible feeder and B-side pattern.",
            "Kept all uncertain dashed/control candidates out of the accepted matrix.",
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
            "AGREED with Jennifer refined matrix.",
            "Confirmed the PN-MOV-A feeder lands on MCC-SAF-A2, while FAN-CR-A is a pass-by/overlap.",
            "Confirmed uncertain dashed/control candidates remain out.",
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
            "Final graph is 180 nodes and 183 accepted undirected edges.",
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
        "document": 9,
        "iteration": 1,
        "resource_location": str(ROOT),
        "method": "raw schematic plus visual aids only; no GT and no OCR",
        "node_count_final": len(FINAL_NODES),
        "edge_count_final": len(FINAL_EDGES),
        "uncertain_candidates": UNCERTAIN_CANDIDATES,
        "round_summaries": summaries,
        "rounds": [serializable_round(round_data) for round_data in ROUNDS],
    }
    (RESULTS / "rounds_connectivity.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    headers = sorted({kind for _a, _b, kind in FINAL_EDGES})
    report_lines = [
        "# Connectivity Extraction - Document 9",
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
            "",
            "Jennifer correction applied: removed FAN-CR-A--PN-MOV-A and added MCC-SAF-A2--PN-MOV-A.",
        ]
    )
    (RESULTS / "connectivity_extraction_report.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(payload["round_summaries"], indent=2))


if __name__ == "__main__":
    main()
