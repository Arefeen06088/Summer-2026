from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


FINAL_NODES_TEXT = """
OFFSITE-345, DS-SAT-1, TR-SAT-A, CB-SAT-A, TR-SAT-B, CB-SAT-B, GEN-G01, ISO-GEN-1, CB-GEN-A, BUS-13A, CB-TIE-13, BUS-13B, CB-UAT-A, TR-UAT-A, CB-UAT-B, TR-UAT-B, DG-1A, CB-DG-A, DG-1B, CB-DG-B, BUS-4A, CB-TIE-4, BUS-4B,
CB-480A, TR-480A, LC-480A, CB-MCC-A1, MCC-A1, CB-P201A, PUMP-P201A, CB-MOV101A, MOV-101A, CB-FAN101A, FAN-F101A, CB-MCC-A2, MCC-A2, CB-P202A, PUMP-P202A, CB-MOV102A, MOV-102A, CB-HTR101A, HTR-H101A,
CB-480B, TR-480B, LC-480B, CB-MCC-B1, MCC-B1, CB-P201B, PUMP-P201B, CB-MOV101B, MOV-101B, CB-FAN101B, FAN-F101B, CB-MCC-B2, MCC-B2, CB-P202B, PUMP-P202B, CB-MOV102B, MOV-102B, CB-HTR101B, HTR-H101B,
CB-480C, TR-480C, LC-480C, CB-MCC-C1, MCC-C1, CB-P301A, PUMP-P301A, CB-MOV201A, MOV-201A, CB-FAN201A, FAN-F201A, CB-MCC-C2, MCC-C2, CB-P302A, PUMP-P302A, CB-MOV202A, MOV-202A, CB-HTR201A, HTR-H201A,
CB-480D, TR-480D, LC-480D, CB-MCC-D1, MCC-D1, CB-P301B, PUMP-P301B, CB-MOV201B, MOV-201B, CB-FAN201B, FAN-F201B, CB-MCC-D2, MCC-D2, CB-P302B, PUMP-P302B, CB-MOV202B, MOV-202B, CB-HTR201B, HTR-H201B,
BAT-125A, BCHG-125A, BUS-125DCA, INV-120A, UPS-120A, PNL-AC-CR1, PPS-A, ANN-101, RELAY-K101, RELAY-K102, SR-101,
BAT-125B, BCHG-125B, BUS-125DCB, INV-120B, UPS-120B, PNL-AC-CR2, PPS-B, ANN-201, RELAY-K201, RELAY-K202
"""


FINAL_EDGES_TEXT = """
OFFSITE-345,DS-SAT-1,S
DS-SAT-1,TR-SAT-A,S
DS-SAT-1,TR-SAT-B,S
TR-SAT-A,CB-SAT-A,S
CB-SAT-A,BUS-4A,S
GEN-G01,ISO-GEN-1,S
ISO-GEN-1,CB-GEN-A,S
CB-GEN-A,BUS-13A,S
BUS-13A,CB-TIE-13,S
CB-TIE-13,BUS-13B,S
BUS-13A,CB-UAT-A,S
CB-UAT-A,TR-UAT-A,S
TR-UAT-A,BUS-4A,S
BUS-13B,CB-UAT-B,S
CB-UAT-B,TR-UAT-B,S
TR-UAT-B,BUS-4B,S
DG-1A,CB-DG-A,S
CB-DG-A,BUS-4A,S
BUS-4A,CB-TIE-4,S
CB-TIE-4,BUS-4B,S
TR-SAT-B,CB-SAT-B,S
CB-SAT-B,BUS-4B,S
DG-1B,CB-DG-B,S
CB-DG-B,BUS-4B,S
BUS-4A,CB-480A,S
CB-480A,TR-480A,S
TR-480A,LC-480A,S
BUS-4A,CB-480B,S
CB-480B,TR-480B,S
TR-480B,LC-480B,S
BUS-4B,CB-480C,S
CB-480C,TR-480C,S
TR-480C,LC-480C,S
BUS-4B,CB-480D,S
CB-480D,TR-480D,S
TR-480D,LC-480D,S
LC-480A,CB-MCC-A1,S
CB-MCC-A1,MCC-A1,S
MCC-A1,CB-P201A,S
CB-P201A,PUMP-P201A,S
MCC-A1,CB-MOV101A,S
CB-MOV101A,MOV-101A,S
MCC-A1,CB-FAN101A,S
CB-FAN101A,FAN-F101A,S
LC-480A,CB-MCC-A2,S
CB-MCC-A2,MCC-A2,S
MCC-A2,CB-P202A,S
CB-P202A,PUMP-P202A,S
MCC-A2,CB-MOV102A,S
CB-MOV102A,MOV-102A,S
MCC-A2,CB-HTR101A,S
CB-HTR101A,HTR-H101A,S
LC-480B,CB-MCC-B1,S
CB-MCC-B1,MCC-B1,S
MCC-B1,CB-P201B,S
CB-P201B,PUMP-P201B,S
MCC-B1,CB-MOV101B,S
CB-MOV101B,MOV-101B,S
MCC-B1,CB-FAN101B,S
CB-FAN101B,FAN-F101B,S
LC-480B,CB-MCC-B2,S
CB-MCC-B2,MCC-B2,S
MCC-B2,CB-P202B,S
CB-P202B,PUMP-P202B,S
MCC-B2,CB-MOV102B,S
CB-MOV102B,MOV-102B,S
MCC-B2,CB-HTR101B,S
CB-HTR101B,HTR-H101B,S
LC-480C,CB-MCC-C1,S
CB-MCC-C1,MCC-C1,S
MCC-C1,CB-P301A,S
CB-P301A,PUMP-P301A,S
MCC-C1,CB-MOV201A,S
CB-MOV201A,MOV-201A,S
MCC-C1,CB-FAN201A,S
CB-FAN201A,FAN-F201A,S
LC-480C,CB-MCC-C2,S
CB-MCC-C2,MCC-C2,S
MCC-C2,CB-P302A,S
CB-P302A,PUMP-P302A,S
MCC-C2,CB-MOV202A,S
CB-MOV202A,MOV-202A,S
MCC-C2,CB-HTR201A,S
CB-HTR201A,HTR-H201A,S
LC-480D,CB-MCC-D1,S
CB-MCC-D1,MCC-D1,S
MCC-D1,CB-P301B,S
CB-P301B,PUMP-P301B,S
MCC-D1,CB-MOV201B,S
CB-MOV201B,MOV-201B,S
MCC-D1,CB-FAN201B,S
CB-FAN201B,FAN-F201B,S
LC-480D,CB-MCC-D2,S
CB-MCC-D2,MCC-D2,S
MCC-D2,CB-P302B,S
CB-P302B,PUMP-P302B,S
MCC-D2,CB-MOV202B,S
CB-MOV202B,MOV-202B,S
MCC-D2,CB-HTR201B,S
CB-HTR201B,HTR-H201B,S
LC-480A,BAT-125A,S
BAT-125A,BCHG-125A,S
BAT-125A,BUS-125DCA,S
BCHG-125A,BUS-125DCA,S
BUS-125DCA,INV-120A,S
BUS-125DCA,PPS-A,S
LC-480D,BCHG-125B,S
BAT-125B,BUS-125DCB,S
BCHG-125B,BUS-125DCB,S
BUS-125DCB,INV-120B,S
BUS-125DCB,PPS-B,S
INV-120A,UPS-120A,D
UPS-120A,PNL-AC-CR1,D
PNL-AC-CR1,PPS-A,D
UPS-120A,ANN-101,D
ANN-101,PPS-A,D
ANN-101,RELAY-K101,D
PPS-A,RELAY-K101,D
PPS-A,RELAY-K102,D
RELAY-K101,RELAY-K102,D
RELAY-K102,SR-101,D
MCC-A1,PNL-AC-CR1,D
MCC-B1,PNL-AC-CR1,D
PNL-AC-CR1,RELAY-K101,D
PNL-AC-CR1,RELAY-K102,D
SR-101,ANN-201,D
INV-120B,UPS-120B,D
UPS-120B,PNL-AC-CR2,D
PNL-AC-CR2,PPS-B,D
UPS-120B,ANN-201,D
ANN-201,PPS-B,D
ANN-201,RELAY-K201,D
PPS-B,RELAY-K201,D
PPS-B,RELAY-K202,D
RELAY-K201,RELAY-K202,D
MCC-C1,PNL-AC-CR2,D
MCC-D1,PNL-AC-CR2,D
PNL-AC-CR2,RELAY-K201,D
PNL-AC-CR2,RELAY-K202,D
SR-101,RELAY-K202,D
"""


def parse_nodes(text: str) -> list[str]:
    return [part.strip() for part in text.replace("\n", ",").split(",") if part.strip()]


def parse_edges(text: str) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for raw in text.strip().splitlines():
        if not raw.strip() or raw.lower().startswith("a,b"):
            continue
        a, b, kind = [part.strip() for part in raw.split(",")]
        edges.append((a, b, kind))
    return edges


FINAL_NODES = parse_nodes(FINAL_NODES_TEXT)
FINAL_EDGES = parse_edges(FINAL_EDGES_TEXT)


DIEGO_R1_NODES = (
    ["AUX/STBY-13.8KV-FEED"]
    + FINAL_NODES[:4]
    + FINAL_NODES[6:18]
    + FINAL_NODES[20:21]
    + FINAL_NODES[21:23]
    + FINAL_NODES[4:6]
    + FINAL_NODES[18:20]
    + FINAL_NODES[23:]
    + ["CTRL-RACEWAY-A", "CTRL-RACEWAY-B"]
)

DIEGO_R1_EDGES = parse_edges(
    """
AUX/STBY-13.8KV-FEED,DS-SAT-1,S
AUX/STBY-13.8KV-FEED,TR-SAT-B,S
OFFSITE-345,DS-SAT-1,S
DS-SAT-1,TR-SAT-A,S
TR-SAT-A,CB-SAT-A,S
CB-SAT-A,BUS-4A,S
GEN-G01,ISO-GEN-1,S
ISO-GEN-1,CB-GEN-A,S
CB-GEN-A,BUS-13A,S
BUS-13A,CB-TIE-13,S
CB-TIE-13,BUS-13B,S
BUS-13A,CB-UAT-A,S
CB-UAT-A,TR-UAT-A,S
TR-UAT-A,BUS-4A,S
BUS-13B,CB-UAT-B,S
CB-UAT-B,TR-UAT-B,S
TR-UAT-B,BUS-4B,S
DG-1A,CB-DG-A,S
CB-DG-A,BUS-4A,S
BUS-4A,CB-TIE-4,S
CB-TIE-4,BUS-4B,S
TR-SAT-B,CB-SAT-B,S
CB-SAT-B,BUS-4B,S
DG-1B,CB-DG-B,S
CB-DG-B,BUS-4B,S
BUS-4A,CB-480A,S
BUS-4A,CB-480B,S
BUS-4B,CB-480C,S
BUS-4B,CB-480D,S
"""
) + [
    edge for edge in FINAL_EDGES
    if edge[2] == "S" and edge[0] not in {"OFFSITE-345", "DS-SAT-1", "TR-SAT-A", "CB-SAT-A", "TR-SAT-B", "CB-SAT-B", "GEN-G01", "ISO-GEN-1", "CB-GEN-A", "BUS-13A", "CB-TIE-13", "BUS-13B", "CB-UAT-A", "TR-UAT-A", "CB-UAT-B", "TR-UAT-B", "DG-1A", "CB-DG-A", "DG-1B", "CB-DG-B", "BUS-4A", "CB-TIE-4", "BUS-4B"}
    and edge not in {
        ("LC-480A", "BAT-125A", "S"),
        ("BAT-125A", "BCHG-125A", "S"),
        ("BAT-125A", "BUS-125DCA", "S"),
        ("BCHG-125A", "BUS-125DCA", "S"),
        ("BUS-125DCA", "INV-120A", "S"),
        ("BUS-125DCA", "PPS-A", "S"),
        ("LC-480D", "BCHG-125B", "S"),
        ("BAT-125B", "BUS-125DCB", "S"),
        ("BCHG-125B", "BUS-125DCB", "S"),
        ("BUS-125DCB", "INV-120B", "S"),
        ("BUS-125DCB", "PPS-B", "S"),
    }
] + parse_edges(
    """
BAT-125A,BUS-125DCA,S
BCHG-125A,BUS-125DCA,S
BUS-125DCA,INV-120A,S
BUS-125DCA,PPS-A,S
BAT-125B,BUS-125DCB,S
BCHG-125B,BUS-125DCB,S
BUS-125DCB,INV-120B,S
BUS-125DCB,PPS-B,S
INV-120A,UPS-120A,D
UPS-120A,PNL-AC-CR1,D
PNL-AC-CR1,PPS-A,D
UPS-120A,ANN-101,D
ANN-101,PNL-AC-CR1,D
ANN-101,PPS-A,D
ANN-101,RELAY-K101,D
PPS-A,RELAY-K101,D
PPS-A,RELAY-K102,D
RELAY-K101,RELAY-K102,D
RELAY-K102,SR-101,D
INV-120B,UPS-120B,D
UPS-120B,PNL-AC-CR2,D
PNL-AC-CR2,PPS-B,D
UPS-120B,ANN-201,D
ANN-201,PNL-AC-CR2,D
ANN-201,PPS-B,D
ANN-201,RELAY-K201,D
PPS-B,RELAY-K201,D
PPS-B,RELAY-K202,D
RELAY-K201,RELAY-K202,D
SR-101,ANN-201,D
MCC-A1,CTRL-RACEWAY-A,D
MCC-B1,CTRL-RACEWAY-A,D
MCC-C1,CTRL-RACEWAY-B,D
MCC-D1,CTRL-RACEWAY-B,D
CTRL-RACEWAY-A,CTRL-RACEWAY-B,D
"""
)

JENNIFER_R1_NODES = FINAL_NODES + ["CTRL-RACEWAY-A", "CTRL-RACEWAY-B"]
JENNIFER_R1_EDGES = [
    edge for edge in FINAL_EDGES
    if edge not in {
        ("MCC-A1", "PNL-AC-CR1", "D"),
        ("MCC-B1", "PNL-AC-CR1", "D"),
        ("PNL-AC-CR1", "RELAY-K101", "D"),
        ("PNL-AC-CR1", "RELAY-K102", "D"),
        ("MCC-C1", "PNL-AC-CR2", "D"),
        ("MCC-D1", "PNL-AC-CR2", "D"),
        ("PNL-AC-CR2", "RELAY-K201", "D"),
        ("PNL-AC-CR2", "RELAY-K202", "D"),
        ("SR-101", "RELAY-K202", "D"),
    }
] + parse_edges(
    """
MCC-A1,CTRL-RACEWAY-A,D
MCC-B1,CTRL-RACEWAY-A,D
MCC-C1,CTRL-RACEWAY-B,D
MCC-D1,CTRL-RACEWAY-B,D
"""
)


ROUNDS = [
    {
        "round": 1,
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "proposal_with_uncertain_candidates",
        "nodes": DIEGO_R1_NODES,
        "edges": DIEGO_R1_EDGES,
        "notes": [
            "Included AUX/STBY-13.8KV-FEED and CTRL-RACEWAY-A/B as high-recall logical nodes.",
            "Kept only accepted edges; separately flagged uncertain BAT-125A--BCHG-125A, LC-480D--BCHG-125B, and MCC-2 raceway candidates.",
        ],
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "status": "refined",
        "nodes": JENNIFER_R1_NODES,
        "edges": JENNIFER_R1_EDGES,
        "notes": [
            "Removed AUX/STBY as a node and added DS-SAT-1--TR-SAT-B.",
            "Kept CTRL-RACEWAY-A/B provisionally as routing nodes before Diego saturation review.",
        ],
    },
    {
        "round": 3,
        "agent": "Diego",
        "role": "saturation extractor",
        "status": "final_candidate",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": [
            "Excluded raceways as graph nodes; mapped dashed raceway routes to visible component endpoints.",
            "Final candidate has 120 nodes and 140 undirected edges.",
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
            "Dashed MCC-to-PNL and PNL-to-relay edges are accepted as functional/control endpoint evidence, not solid electrical continuity.",
        ],
    },
]


def write_sparse(path: Path, edges: list[tuple[str, str, str]], value_column: str = "type") -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["A", "B", value_column])
        for a, b, kind in edges:
            writer.writerow([a, b, kind if value_column == "type" else 1])


def matrix_for(nodes: list[str], edges: list[tuple[str, str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    if len(index) != len(nodes):
        raise ValueError("Duplicate node name in node list")
    matrix = [[0 for _ in nodes] for _ in nodes]
    seen_pairs: set[tuple[str, str]] = set()
    for a, b, _ in edges:
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
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    matrix = matrix_for(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def summarize_round(round_data: dict) -> dict:
    nodes = round_data["nodes"]
    edges = round_data["edges"]
    return {
        "round": round_data["round"],
        "agent": round_data["agent"],
        "status": round_data["status"],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "solid_edge_count": sum(1 for _, _, kind in edges if kind == "S"),
        "dashed_edge_count": sum(1 for _, _, kind in edges if kind == "D"),
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds_dir = RESULTS / "round_matrices"
    rounds_dir.mkdir(exist_ok=True)

    summaries = []
    for round_data in ROUNDS:
        prefix = f"round_{round_data['round']:02d}_{round_data['agent'].lower()}"
        sparse_path = rounds_dir / f"{prefix}_sparse_edges.csv"
        matrix_path = rounds_dir / f"{prefix}_connectivity_matrix.csv"
        nodes_path = rounds_dir / f"{prefix}_nodes.txt"
        write_sparse(sparse_path, round_data["edges"])
        write_matrix(matrix_path, round_data["nodes"], round_data["edges"])
        nodes_path.write_text("\n".join(round_data["nodes"]) + "\n", encoding="utf-8")
        summaries.append(summarize_round(round_data))

    write_sparse(RESULTS / "final_sparse_edges.csv", FINAL_EDGES)
    write_sparse(RESULTS / "final_sparse_matrix_pairs.csv", FINAL_EDGES, value_column="value")
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    (RESULTS / "final_nodes.txt").write_text("\n".join(FINAL_NODES) + "\n", encoding="utf-8")

    serializable_rounds = []
    for round_data in ROUNDS:
        serializable = dict(round_data)
        serializable["edges"] = [
            {"A": a, "B": b, "type": kind} for a, b, kind in round_data["edges"]
        ]
        serializable_rounds.append(serializable)

    payload = {
        "document": 7,
        "iteration": 1,
        "resource_location": str(ROOT),
        "node_count_final": len(FINAL_NODES),
        "edge_count_final": len(FINAL_EDGES),
        "round_summaries": summaries,
        "rounds": serializable_rounds,
    }
    (RESULTS / "rounds_connectivity.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    report_lines = [
        "# Connectivity Extraction - Document 7",
        "",
        "Raw schematic and visual aids only; no GT or OCR.",
        "",
        "| Round | Agent | Status | Nodes | Edges | Solid | Dashed |",
        "|---:|---|---|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        report_lines.append(
            f"| {summary['round']} | {summary['agent']} | {summary['status']} | "
            f"{summary['node_count']} | {summary['edge_count']} | "
            f"{summary['solid_edge_count']} | {summary['dashed_edge_count']} |"
        )
    report_lines.extend(
        [
            "",
            f"Final matrix: {len(FINAL_NODES)} nodes, {len(FINAL_EDGES)} undirected edges.",
            "Matrix values are 1 for any accepted solid or dashed/control connection and 0 otherwise.",
        ]
    )
    (RESULTS / "connectivity_extraction_report.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["round_summaries"], indent=2))


if __name__ == "__main__":
    main()
