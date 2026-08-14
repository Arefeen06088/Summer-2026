from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


FINAL_NODES_TEXT = """
SRC-345KV, BUS-SWY-345KV, GEN-01, UAT-1, CB-UAT, DG-1A, CB-DGA, BUS-4160-A, CB-TIE-AB, SAT-1, CB-SAT, DG-1B, CB-DGB, BUS-4160-B, CB-A01, TR-480-A1, CB-A02, TR-480-A2, CB-A03, PUMP-RHR-A, CB-A04, PUMP-CS-A, CB-A05, PUMP-AFW-A, CB-A06, TR-UPS-A, CB-A07, CHLR-A, CB-A08, 480V-LC-FEEDERS-A, FAN-CR-A, CB-A09, TB-SWGR-A, RLY-27A, RLY-50A, RLY-86A, PT-4160-A, CT-4160-A, PNL-RPS-A, PNL-ESFAS-A, TB-LV-A, FUSE-A01, FUSE-A02, LC-101A, DS-A01, MCC-101A, MOV-101A, MOV-102A, JB-101A, LC-102A, DS-A02, MCC-102A, AOV-101A, PUMP-CCW-A, FAN-AB-A, HTR-TRACE-A, MCC-103A, RECT-1A, BCHG-1A, BAT-1A, BUS-DC-A, INV-1A, BUS-UPS-A, PNL-UPS-A, GND-A, CB-B01, TR-480-B1, CB-B02, TR-480-B2, CB-B03, PUMP-RHR-B, CB-B04, PUMP-CS-B, CB-B05, PUMP-AFW-B, CB-B06, TR-UPS-B, CB-B07, CHLR-B, CB-B08, 480V-LC-FEEDERS-B, FAN-CR-B, CB-B09, TB-SWGR-B, RLY-27B, RLY-50B, RLY-86B, PT-4160-B, CT-4160-B, PNL-RPS-B, PNL-ESFAS-B, TB-LV-B, FUSE-B01, FUSE-B02, LC-101B, DS-B01, MCC-101B, MOV-101B, MOV-102B, JB-101B, LC-102B, DS-B02, MCC-102B, AOV-101B, PUMP-CCW-B, FAN-AB-B, HTR-TRACE-B, MCC-103B, RECT-1B, BCHG-1B, BAT-1B, BUS-DC-B, INV-1B, BUS-UPS-B, PNL-UPS-B, GND-B, PNL-MCR-01, PNL-ANN-01, SER-01, JB-CONTROL
"""


DIEGO_R1_EDGES_TEXT = """
SRC-345KV,BUS-SWY-345KV,S
BUS-SWY-345KV,SAT-1,S
GEN-01,UAT-1,S
UAT-1,CB-UAT,S
CB-UAT,BUS-4160-A,S
DG-1A,CB-DGA,S
CB-DGA,BUS-4160-A,S
BUS-4160-A,CB-TIE-AB,S
CB-TIE-AB,BUS-4160-B,S
SAT-1,CB-SAT,S
CB-SAT,BUS-4160-B,S
DG-1B,CB-DGB,S
CB-DGB,BUS-4160-B,S
BUS-4160-A,CB-A01,S
CB-A01,TR-480-A1,S
BUS-4160-A,CB-A02,S
CB-A02,TR-480-A2,S
BUS-4160-A,CB-A03,S
CB-A03,PUMP-RHR-A,S
BUS-4160-A,CB-A04,S
CB-A04,PUMP-CS-A,S
BUS-4160-A,CB-A05,S
CB-A05,PUMP-AFW-A,S
BUS-4160-A,CB-A06,S
CB-A06,TR-UPS-A,S
BUS-4160-A,CB-A07,S
CB-A07,CHLR-A,S
BUS-4160-A,CB-A08,S
CB-A08,480V-LC-FEEDERS-A,S
480V-LC-FEEDERS-A,FAN-CR-A,S
480V-LC-FEEDERS-A,LC-101A,S
480V-LC-FEEDERS-A,LC-102A,S
BUS-4160-A,CB-A09,S
BUS-4160-A,PT-4160-A,S
BUS-4160-A,CT-4160-A,S
TB-SWGR-A,RLY-27A,D
TB-SWGR-A,RLY-50A,D
TB-SWGR-A,RLY-86A,D
RLY-27A,PT-4160-A,SIG
RLY-50A,CT-4160-A,SIG
RLY-86A,CT-4160-A,SIG
PNL-RPS-A,FUSE-A01,S
PNL-ESFAS-A,FUSE-A02,S
PNL-RPS-A,TB-LV-A,D
PNL-ESFAS-A,TB-LV-A,D
FUSE-A02,DS-A01,S
FUSE-A02,DS-A02,S
480V-LC-FEEDERS-A,DS-A01,S
LC-101A,DS-A01,S
DS-A01,MCC-101A,S
LC-102A,DS-A02,S
DS-A02,MCC-102A,S
LC-102A,MCC-103A,S
MCC-101A,MOV-101A,S
MCC-101A,MOV-102A,S
MCC-101A,JB-101A,D
JB-101A,AOV-101A,D
MCC-102A,AOV-101A,S
MCC-102A,PUMP-CCW-A,S
MCC-103A,FAN-AB-A,S
FAN-AB-A,HTR-TRACE-A,S
RECT-1A,BCHG-1A,S
BCHG-1A,BAT-1A,S
BAT-1A,BUS-DC-A,S
BUS-DC-A,INV-1A,S
INV-1A,BUS-UPS-A,S
BUS-UPS-A,PNL-UPS-A,S
GND-A,BUS-DC-A,G
BUS-4160-B,CB-B01,S
CB-B01,TR-480-B1,S
BUS-4160-B,CB-B02,S
CB-B02,TR-480-B2,S
BUS-4160-B,CB-B03,S
CB-B03,PUMP-RHR-B,S
BUS-4160-B,CB-B04,S
CB-B04,PUMP-CS-B,S
BUS-4160-B,CB-B05,S
CB-B05,PUMP-AFW-B,S
BUS-4160-B,CB-B06,S
CB-B06,TR-UPS-B,S
BUS-4160-B,CB-B07,S
CB-B07,CHLR-B,S
BUS-4160-B,CB-B08,S
CB-B08,480V-LC-FEEDERS-B,S
480V-LC-FEEDERS-B,FAN-CR-B,S
480V-LC-FEEDERS-B,LC-101B,S
480V-LC-FEEDERS-B,LC-102B,S
BUS-4160-B,CB-B09,S
BUS-4160-B,PT-4160-B,S
BUS-4160-B,CT-4160-B,S
TB-SWGR-B,RLY-27B,D
TB-SWGR-B,RLY-50B,D
TB-SWGR-B,RLY-86B,D
RLY-27B,PT-4160-B,SIG
RLY-50B,CT-4160-B,SIG
RLY-86B,CT-4160-B,SIG
PNL-RPS-B,FUSE-B01,S
PNL-ESFAS-B,FUSE-B02,S
PNL-RPS-B,TB-LV-B,D
PNL-ESFAS-B,TB-LV-B,D
FUSE-B02,DS-B01,S
FUSE-B02,DS-B02,S
480V-LC-FEEDERS-B,DS-B01,S
LC-101B,DS-B01,S
DS-B01,MCC-101B,S
LC-102B,DS-B02,S
DS-B02,MCC-102B,S
LC-102B,MCC-103B,S
MCC-101B,MOV-101B,S
MCC-101B,MOV-102B,S
MCC-101B,JB-101B,D
JB-101B,AOV-101B,D
MCC-102B,AOV-101B,S
MCC-102B,PUMP-CCW-B,S
MCC-103B,FAN-AB-B,S
FAN-AB-B,HTR-TRACE-B,S
RECT-1B,BCHG-1B,S
BCHG-1B,BAT-1B,S
BAT-1B,BUS-DC-B,S
BUS-DC-B,INV-1B,S
INV-1B,BUS-UPS-B,S
BUS-UPS-B,PNL-UPS-B,S
GND-B,BUS-DC-B,G
PNL-MCR-01,JB-CONTROL,D
PNL-ANN-01,JB-CONTROL,SIG
SER-01,JB-CONTROL,SIG
"""


REMOVED_BY_JENNIFER = {
    ("BUS-4160-A", "PT-4160-A", "S"),
    ("BUS-4160-A", "CT-4160-A", "S"),
    ("BUS-4160-B", "PT-4160-B", "S"),
    ("BUS-4160-B", "CT-4160-B", "S"),
    ("480V-LC-FEEDERS-A", "DS-A01", "S"),
    ("480V-LC-FEEDERS-B", "DS-B01", "S"),
}

UNCERTAIN_CANDIDATES = [
    "BUS-SWY-345KV,UAT-1,S",
    "BUS-SWY-345KV,GEN-01,S",
    "TR-480-A1,480V-LC-FEEDERS-A,S",
    "TR-480-A2,480V-LC-FEEDERS-A,S",
    "TR-480-B1,480V-LC-FEEDERS-B,S",
    "TR-480-B2,480V-LC-FEEDERS-B,S",
    "FUSE-A01,CT-4160-A,SIG",
    "FUSE-A01,CB-A09,SIG",
    "FUSE-B01,CT-4160-B,SIG",
    "FUSE-B01,CB-B09,SIG",
    "PT-4160-A,PNL-RPS-A,SIG",
    "CT-4160-A,PNL-RPS-A,SIG",
    "PT-4160-B,PNL-RPS-B,SIG",
    "CT-4160-B,PNL-RPS-B,SIG",
    "MCC-102A,FAN-AB-A,S",
    "MCC-103A,PUMP-CCW-A,S",
    "MCC-102B,FAN-AB-B,S",
    "MCC-103B,PUMP-CCW-B,S",
    "TB-LV-A,MCC-101A,D",
    "TB-LV-B,MCC-101B,D",
    "TB-LV-A,PNL-UPS-A,D",
    "TB-LV-B,PNL-UPS-B,D",
    "JB-CONTROL,TB-SWGR-A,D",
    "JB-CONTROL,TB-LV-A,D",
    "JB-CONTROL,TB-SWGR-B,D",
    "JB-CONTROL,TB-LV-B,D",
    "GND-A,PNL-UPS-A,G",
    "GND-B,PNL-UPS-B,G",
    "GND-A,TB-LV-A,G",
    "GND-B,TB-LV-B,G",
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
FINAL_EDGES = [edge for edge in DIEGO_R1_EDGES if edge not in REMOVED_BY_JENNIFER]


ROUNDS = [
    {
        "round": 1,
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "proposal_with_uncertain_candidates",
        "nodes": FINAL_NODES,
        "edges": DIEGO_R1_EDGES,
        "notes": [
            "Initial high-recall proposal with separate uncertain candidate list.",
            "Jennifer later removed six overconnected accepted edges.",
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
            "Removed solid bus-to-PT/CT edges because PT/CT devices are visually tied by dotted signal routing, not clean solid bus landings.",
            "Removed direct 480V-LC-FEEDERS-A/B to DS-A01/B01 edges as overconnected.",
            "No added edges; uncertain cable-tray, signal, transformer-secondary, and ground candidates remain out.",
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
            "Confirmed the six removed edges should stay out.",
            "Confirmed no uncertain candidates should be promoted.",
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
            "Final graph is 120 nodes and 120 accepted undirected edges.",
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
        "document": 10,
        "iteration": 1,
        "resource_location": str(ROOT),
        "method": "raw schematic plus visual aids only; no GT and no OCR",
        "node_count_final": len(FINAL_NODES),
        "edge_count_final": len(FINAL_EDGES),
        "removed_by_jennifer": [
            {"A": a, "B": b, "type": kind} for a, b, kind in sorted(REMOVED_BY_JENNIFER)
        ],
        "uncertain_candidates": UNCERTAIN_CANDIDATES,
        "round_summaries": summaries,
        "rounds": [serializable_round(round_data) for round_data in ROUNDS],
    }
    (RESULTS / "rounds_connectivity.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    headers = sorted({kind for _a, _b, kind in DIEGO_R1_EDGES})
    report_lines = [
        "# Connectivity Extraction - Document 10",
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
            "Matrix values are 1 for accepted solid/power, dashed/control, dotted/signal, and ground connections; 0 otherwise.",
            "",
            "Jennifer precision removals: BUS-4160-A--PT-4160-A, BUS-4160-A--CT-4160-A, BUS-4160-B--PT-4160-B, BUS-4160-B--CT-4160-B, 480V-LC-FEEDERS-A--DS-A01, 480V-LC-FEEDERS-B--DS-B01.",
        ]
    )
    (RESULTS / "connectivity_extraction_report.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(payload["round_summaries"], indent=2))


if __name__ == "__main__":
    main()
