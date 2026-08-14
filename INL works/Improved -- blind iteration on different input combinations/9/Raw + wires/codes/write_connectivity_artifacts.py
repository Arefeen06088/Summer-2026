from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw + wires"
)
RESULTS = ROOT / "results"


NODES = [
    "UTIL-230A", "DS-230A", "SAT-1A", "CB-SAT-A", "UTIL-230B", "DS-230B",
    "SAT-1B", "CB-SAT-B", "GEN-1A", "CB-GEN-1", "BUS-13K-01", "UAT-1A",
    "CB-UAT-1A", "UAT-1B", "CB-UAT-1B", "BUS-4160-N1", "CB-TIE-41N",
    "BUS-4160-N2", "EDG-1A", "CB-EDG-A", "BUS-4160S1A", "CT-41A",
    "PT-41A", "RELAY-50/51A", "RELAY-86A", "CB-481A", "TR-480-A1",
    "CB-LV-A1", "BUS-480-A1", "MCC-SAF-A1", "CB-RHR-A", "PUMP-RHR-A",
    "CB-SI-A", "PUMP-SI-A", "CB-CCW-A", "PUMP-CCW-A", "CB-482A",
    "TR-480-A2", "CB-LV-A2", "BUS-480-A2", "MCC-SAF-A2", "CB-CVC-A",
    "PUMP-CVC-A", "CB-CRF-A", "FAN-CR-A", "CB-COMP-A", "COMP-AIR-A",
    "PN-MOV-A", "FU-8810A", "MOV-8810A", "FU-HV302A", "VLV-HV-302A",
    "FU-RCICA", "MOV-RCIC-A", "FU-SWA", "MOV-SW-A", "EDG-1B",
    "CB-EDG-B", "BUS-4160S1B", "CT-41B", "PT-41B", "RELAY-27B",
    "RELAY-86B", "CB-481B", "TR-480-B1", "CB-LV-B1", "BUS-480-B1",
    "MCC-SAF-B1", "CB-RHR-B", "PUMP-RHR-B", "CB-SI-B", "PUMP-SI-B",
    "CB-CCW-B", "PUMP-CCW-B", "CB-482B", "TR-480-B2", "CB-LV-B2",
    "BUS-480-B2", "MCC-SAF-B2", "CB-CVC-B", "PUMP-CVC-B", "CB-CRF-B",
    "FAN-CR-B", "CB-COMP-B", "COMP-AIR-B", "PN-MOV-B", "FU-8810B",
    "MOV-8810B", "FU-HV302B", "VLV-HV-302B", "FU-RCICB", "MOV-RCIC-B",
    "FU-SWB", "MOV-SW-B", "CB-4160-N1A", "TR-480-N1A", "CB-480-N1A",
    "BUS-480-N1A", "MCC-NORM-1A", "PN-480-N1A", "CB-CWP-1A",
    "PUMP-CWP-1A", "CB-HEAT-1A", "HTR-1A", "CB-AHU-1A", "FAN-AHU-1A",
    "CB-4160-N1B", "TR-480-N1B", "CB-480-N1B", "BUS-480-N1B",
    "MCC-NORM-1B", "PN-480-N1B", "CB-CWP-1B", "PUMP-CWP-1B",
    "CB-SUMP-1B", "PUMP-SUMP-1B", "CB-LTG-1B", "PN-LTG-1B",
    "MTR-480-N1", "JB-NORM-A", "RTD-PNL-A", "TB-SEQ-A", "TDR-SEQ-A",
    "CB-4160-N2A", "TR-480-N2A", "CB-480-N2A", "BUS-480-N2A",
    "MCC-NORM-2A", "PN-480-N2A", "CB-CWP-2A", "PUMP-CWP-2A",
    "CB-VAC-2A", "PUMP-VAC-2A", "CB-AHU-2A", "FAN-AHU-2A",
    "MTR-480-N2", "JB-NORM-B", "RTD-PNL-B", "TB-SEQ-B", "TDR-SEQ-B",
    "CB-4160-N2B", "TR-480-N2B", "CB-480-N2B", "BUS-480-N2B",
    "MCC-NORM-2B", "PN-480-N2B", "CB-CWP-2B", "PUMP-CWP-2B",
    "CB-OIL-2B", "PUMP-OIL-2B", "CB-LTG-2B", "PN-LTG-2B", "BAT-125A",
    "CHG-125A", "BUS-125DC-A", "GND-A", "INV-120A", "BUS-120AC-A",
    "PN-125A", "JB-1A", "JB-2A", "PN-120A", "PLC-ESF-A",
    "RELAY-K1A", "RELAY-K2A", "ANN-ESF-A", "BAT-125B", "CHG-125B",
    "BUS-125DC-B", "GND-B", "INV-120B", "BUS-120AC-B", "PN-125B",
    "JB-1B", "JB-2B", "PN-120B", "PLC-ESF-B", "RELAY-K1B",
    "RELAY-K2B", "ANN-ESF-B",
]

NODES_DIEGO_R1 = [
    "CB-TIE-416-N" if node == "CB-TIE-41N" else node for node in NODES
]


EDGE_TEXT_DIEGO_R1 = """
UTIL-230A--DS-230A; DS-230A--SAT-1A; SAT-1A--CB-SAT-A; CB-SAT-A--BUS-4160S1A; UTIL-230B--DS-230B; DS-230B--SAT-1B; SAT-1B--CB-SAT-B; CB-SAT-B--BUS-4160S1B; GEN-1A--CB-GEN-1; CB-GEN-1--BUS-13K-01; BUS-13K-01--UAT-1A; UAT-1A--CB-UAT-1A; CB-UAT-1A--BUS-4160-N1; BUS-13K-01--UAT-1B; UAT-1B--CB-UAT-1B; CB-UAT-1B--BUS-4160-N2; BUS-4160-N1--CB-TIE-416-N; CB-TIE-416-N--BUS-4160-N2.
EDG-1A--CB-EDG-A; CB-EDG-A--BUS-4160S1A; BUS-4160S1A--CT-41A; BUS-4160S1A--PT-41A; CT-41A--RELAY-50/51A; PT-41A--RELAY-50/51A; RELAY-50/51A--RELAY-86A; BUS-4160S1A--CB-481A; CB-481A--TR-480-A1; TR-480-A1--CB-LV-A1; CB-LV-A1--BUS-480-A1; BUS-480-A1--MCC-SAF-A1; MCC-SAF-A1--CB-RHR-A; CB-RHR-A--PUMP-RHR-A; MCC-SAF-A1--CB-SI-A; CB-SI-A--PUMP-SI-A; MCC-SAF-A1--CB-CCW-A; CB-CCW-A--PUMP-CCW-A; BUS-4160S1A--CB-482A; CB-482A--TR-480-A2; TR-480-A2--CB-LV-A2; CB-LV-A2--BUS-480-A2; BUS-480-A2--MCC-SAF-A2; MCC-SAF-A2--CB-CVC-A; CB-CVC-A--PUMP-CVC-A; MCC-SAF-A2--CB-CRF-A; CB-CRF-A--FAN-CR-A; MCC-SAF-A2--CB-COMP-A; CB-COMP-A--COMP-AIR-A; FAN-CR-A--PN-MOV-A; PN-MOV-A--FU-8810A; FU-8810A--MOV-8810A; PN-MOV-A--FU-HV302A; FU-HV302A--VLV-HV-302A; PN-MOV-A--FU-RCICA; FU-RCICA--MOV-RCIC-A; PN-MOV-A--FU-SWA; FU-SWA--MOV-SW-A.
EDG-1B--CB-EDG-B; CB-EDG-B--BUS-4160S1B; BUS-4160S1B--CT-41B; BUS-4160S1B--PT-41B; CT-41B--RELAY-27B; PT-41B--RELAY-27B; RELAY-27B--RELAY-86B; BUS-4160S1B--CB-481B; CB-481B--TR-480-B1; TR-480-B1--CB-LV-B1; CB-LV-B1--BUS-480-B1; BUS-480-B1--MCC-SAF-B1; MCC-SAF-B1--CB-RHR-B; CB-RHR-B--PUMP-RHR-B; MCC-SAF-B1--CB-SI-B; CB-SI-B--PUMP-SI-B; MCC-SAF-B1--CB-CCW-B; CB-CCW-B--PUMP-CCW-B; BUS-4160S1B--CB-482B; CB-482B--TR-480-B2; TR-480-B2--CB-LV-B2; CB-LV-B2--BUS-480-B2; BUS-480-B2--MCC-SAF-B2; MCC-SAF-B2--CB-CVC-B; CB-CVC-B--PUMP-CVC-B; MCC-SAF-B2--CB-CRF-B; CB-CRF-B--FAN-CR-B; MCC-SAF-B2--CB-COMP-B; CB-COMP-B--COMP-AIR-B; FAN-CR-B--PN-MOV-B; PN-MOV-B--FU-8810B; FU-8810B--MOV-8810B; PN-MOV-B--FU-HV302B; FU-HV302B--VLV-HV-302B; PN-MOV-B--FU-RCICB; FU-RCICB--MOV-RCIC-B; PN-MOV-B--FU-SWB; FU-SWB--MOV-SW-B.
BUS-4160-N1--CB-4160-N1A; CB-4160-N1A--TR-480-N1A; TR-480-N1A--CB-480-N1A; CB-480-N1A--BUS-480-N1A; BUS-480-N1A--MCC-NORM-1A; MCC-NORM-1A--PN-480-N1A; PN-480-N1A--CB-CWP-1A; CB-CWP-1A--PUMP-CWP-1A; PN-480-N1A--CB-HEAT-1A; CB-HEAT-1A--HTR-1A; PN-480-N1A--CB-AHU-1A; CB-AHU-1A--FAN-AHU-1A; PN-480-N1A--PN-480-N1B; BUS-4160-N1--CB-4160-N1B; CB-4160-N1B--TR-480-N1B; TR-480-N1B--CB-480-N1B; CB-480-N1B--BUS-480-N1B; BUS-480-N1B--MCC-NORM-1B; MCC-NORM-1B--PN-480-N1B; PN-480-N1B--CB-CWP-1B; CB-CWP-1B--PUMP-CWP-1B; PN-480-N1B--CB-SUMP-1B; CB-SUMP-1B--PUMP-SUMP-1B; PN-480-N1B--CB-LTG-1B; CB-LTG-1B--PN-LTG-1B; PUMP-SUMP-1B--MTR-480-N1; MTR-480-N1--JB-NORM-A; JB-NORM-A--RTD-PNL-A; RTD-PNL-A--TB-SEQ-A; TB-SEQ-A--TDR-SEQ-A.
BUS-4160-N2--CB-4160-N2A; CB-4160-N2A--TR-480-N2A; TR-480-N2A--CB-480-N2A; CB-480-N2A--BUS-480-N2A; BUS-480-N2A--MCC-NORM-2A; MCC-NORM-2A--PN-480-N2A; PN-480-N2A--CB-CWP-2A; CB-CWP-2A--PUMP-CWP-2A; PN-480-N2A--CB-VAC-2A; CB-VAC-2A--PUMP-VAC-2A; PN-480-N2A--CB-AHU-2A; CB-AHU-2A--FAN-AHU-2A; PN-480-N2A--PN-480-N2B; FAN-AHU-2A--MTR-480-N2; MTR-480-N2--JB-NORM-B; JB-NORM-B--RTD-PNL-B; RTD-PNL-B--TB-SEQ-B; TB-SEQ-B--TDR-SEQ-B; BUS-4160-N2--CB-4160-N2B; CB-4160-N2B--TR-480-N2B; TR-480-N2B--CB-480-N2B; CB-480-N2B--BUS-480-N2B; BUS-480-N2B--MCC-NORM-2B; MCC-NORM-2B--PN-480-N2B; PN-480-N2B--CB-CWP-2B; CB-CWP-2B--PUMP-CWP-2B; PN-480-N2B--CB-OIL-2B; CB-OIL-2B--PUMP-OIL-2B; PN-480-N2B--CB-LTG-2B; CB-LTG-2B--PN-LTG-2B.
BAT-125A--BUS-125DC-A; CHG-125A--BUS-125DC-A; BUS-125DC-A--GND-A; BUS-125DC-A--PN-125A; BUS-125DC-A--INV-120A; INV-120A--BUS-120AC-A; BUS-120AC-A--PN-120A; PN-125A--JB-1A; PN-125A--JB-2A; PN-120A--PLC-ESF-A; PN-120A--ANN-ESF-A; PLC-ESF-A--ANN-ESF-A; PLC-ESF-A--RELAY-K1A; PLC-ESF-A--RELAY-K2A.
BAT-125B--BUS-125DC-B; CHG-125B--BUS-125DC-B; BUS-125DC-B--GND-B; BUS-125DC-B--PN-125B; BUS-125DC-B--INV-120B; INV-120B--BUS-120AC-B; BUS-120AC-B--PN-120B; PN-125B--JB-1B; PN-125B--JB-2B; PN-120B--PLC-ESF-B; PN-120B--ANN-ESF-B; PLC-ESF-B--ANN-ESF-B; PLC-ESF-B--RELAY-K1B; PLC-ESF-B--RELAY-K2B.
"""

EDGE_TEXT_JENNIFER_R1 = EDGE_TEXT_DIEGO_R1.replace("CB-TIE-416-N", "CB-TIE-41N")

JENNIFER_R1_REMOVE = [
    ("FAN-CR-B", "PN-MOV-B"),
]

JENNIFER_R1_ADD = [
    ("CB-EDG-A", "CB-482A"),
    ("CB-EDG-B", "CB-482B"),
    ("RELAY-27B", "CB-481B"),
    ("MCC-SAF-B2", "PN-MOV-B"),
]

DIEGO_R2_ADD = [
    ("JB-2B", "PLC-ESF-B"),
]

JENNIFER_R2_ADD = [
    ("RELAY-86A", "CB-482A"),
]

DIEGO_R3_ADD = [
    ("RELAY-27B", "CB-482B"),
    ("PN-LTG-1B", "JB-NORM-A"),
    ("RTD-PNL-A", "RTD-PNL-B"),
    ("PUMP-RHR-A", "JB-1A"),
    ("PUMP-SI-A", "JB-2A"),
    ("PUMP-CCW-A", "JB-2A"),
    ("PUMP-RHR-B", "JB-1B"),
    ("PUMP-SI-B", "JB-2B"),
    ("PUMP-CCW-B", "JB-2B"),
]

JENNIFER_R3_ADD = [
    ("PN-LTG-1B", "JB-NORM-A"),
    ("PUMP-SI-B", "JB-2B"),
]

ROUND_NOTES = {
    "round01_diego": (
        "Diego R1 high-recall accepted graph. Kept the initially read tie label "
        "CB-TIE-416-N and included the visually plausible FAN-CR-B--PN-MOV-B "
        "MOV feed. Uncertain edges from Diego R1 are documented separately, "
        "but not set to 1 in this round matrix."
    ),
    "round02_jennifer": (
        "Jennifer R1 precision graph. Corrected CB-TIE-416-N to CB-TIE-41N; "
        "replaced FAN-CR-B--PN-MOV-B with MCC-SAF-B2--PN-MOV-B; promoted "
        "CB-EDG-A--CB-482A, CB-EDG-B--CB-482B, and RELAY-27B--CB-481B."
    ),
    "round03_diego": (
        "Diego R2 saturation check over Jennifer R1. Added the plausible "
        "B-side lower control edge JB-2B--PLC-ESF-B; the other R2 mentions "
        "were already present in Jennifer R1."
    ),
    "round04_jennifer": (
        "Jennifer R2 precision graph. Accepted JB-2B--PLC-ESF-B and "
        "RELAY-86A--CB-482A. Other R2 additions were duplicates of already "
        "accepted relay edges."
    ),
    "round05_diego": (
        "Diego R3 count-sanity high-recall graph. Added all R3 candidate "
        "edges that had some visual plausibility, including low-confidence "
        "shared-trunk candidates, so Jennifer could filter them."
    ),
    "round06_jennifer_final": (
        "Jennifer R3 final precision graph. Accepted PN-LTG-1B--JB-NORM-A "
        "and PUMP-SI-B--JB-2B only; rejected the remaining R3 shared-trunk "
        "or endpoint-ambiguous candidates. Final saturated matrix."
    ),
}

UNCERTAIN_BY_ROUND = {
    "round01_diego": [
        "CB-482A--RELAY-50/51A",
        "RELAY-86A--CB-482A",
        "RELAY-86A--CB-CWP-1A",
        "CB-482B--RELAY-86B",
        "RELAY-86B--CB-481B",
        "CB-482B--RELAY-27B",
        "BUS-480-A2--CB-CWP-1A",
        "PUMP-RHR-A--PLC-ESF-A",
        "PUMP-SI-A--PLC-ESF-A",
        "PUMP-CCW-A--PLC-ESF-A",
        "PUMP-RHR-B--PLC-ESF-B",
        "PUMP-SI-B--PLC-ESF-B",
        "PUMP-CCW-B--PLC-ESF-B",
        "JB-2A--PLC-ESF-A",
        "JB-2B--PLC-ESF-B",
        "PN-MOV-A--MCC-SAF-A2",
        "PN-MOV-B--MCC-SAF-B2",
    ],
    "round02_jennifer": [
        "CB-482A--RELAY-50/51A",
        "RELAY-86A--CB-482A",
        "RELAY-86A--CB-CWP-1A",
        "CB-482B--RELAY-86B",
        "RELAY-86B--CB-481B",
        "CB-482B--RELAY-27B",
        "BUS-480-A2--CB-CWP-1A",
        "PUMP-RHR-A--PLC-ESF-A",
        "PUMP-SI-A--PLC-ESF-A",
        "PUMP-CCW-A--PLC-ESF-A",
        "PUMP-RHR-B--PLC-ESF-B",
        "PUMP-SI-B--PLC-ESF-B",
        "PUMP-CCW-B--PLC-ESF-B",
        "JB-2A--PLC-ESF-A",
        "JB-2B--PLC-ESF-B",
        "PN-MOV-A--MCC-SAF-A2",
        "FAN-CR-B--PN-MOV-B",
    ],
    "round03_diego": [
        "RELAY-86B--RELAY-27B duplicate of accepted RELAY-27B--RELAY-86B",
        "PUMP-SUMP-1B--MTR-480-N1 duplicate of accepted edge",
        "FAN-AHU-2A--MTR-480-N2 duplicate of accepted edge",
    ],
    "round04_jennifer": [
        "JB-2A--PLC-ESF-A rejected",
    ],
    "round05_diego": [
        "RELAY-27B--CB-482B",
        "RTD-PNL-A--RTD-PNL-B",
        "PUMP-RHR-A--JB-1A",
        "PUMP-SI-A--JB-2A",
        "PUMP-CCW-A--JB-2A",
        "PUMP-RHR-B--JB-1B",
        "PUMP-SI-B--JB-2B",
        "PUMP-CCW-B--JB-2B",
    ],
    "round06_jennifer_final": [
        "RELAY-27B--CB-482B rejected",
        "RTD-PNL-A--RTD-PNL-B rejected",
        "PUMP-RHR-A--JB-1A rejected",
        "PUMP-SI-A--JB-2A rejected",
        "PUMP-CCW-A--JB-2A rejected",
        "PUMP-RHR-B--JB-1B rejected",
        "PUMP-CCW-B--JB-2B rejected",
        "RELAY-86A--CB-CWP-1A rejected",
        "PN-LTG-2B--JB-NORM-B rejected",
        "PN-MOV-A--MCC-SAF-A2 rejected",
        "FAN-CR-B--PN-MOV-B rejected",
        "JB-2A--PLC-ESF-A rejected",
    ],
}


@dataclass(frozen=True)
class RoundGraph:
    name: str
    agent: str
    nodes: list[str]
    edges: list[tuple[str, str]]
    note: str


def parse_edges(text: str, nodes: list[str]) -> list[tuple[str, str]]:
    valid = set(nodes)
    edges: set[tuple[str, str]] = set()
    for chunk in text.replace("\n", ";").replace(".", ";").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "--" not in chunk:
            continue
        left, right = [item.strip() for item in chunk.split("--", 1)]
        if left not in valid or right not in valid:
            raise ValueError(f"Unknown node in edge: {left}--{right}")
        if left == right:
            raise ValueError(f"Unexpected self-loop: {left}")
        edges.add(tuple(sorted((left, right))))
    return sort_edges(edges, nodes)


def sort_edges(edges: set[tuple[str, str]], nodes: list[str]) -> list[tuple[str, str]]:
    order = {node: index for index, node in enumerate(nodes)}
    return sorted(edges, key=lambda edge: (min(order[edge[0]], order[edge[1]]), max(order[edge[0]], order[edge[1]])))


def with_deltas(
    base_edges: list[tuple[str, str]],
    nodes: list[str],
    add: list[tuple[str, str]] | None = None,
    remove: list[tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    valid = set(nodes)
    edges = set(base_edges)
    for left, right in remove or []:
        if left not in valid or right not in valid:
            raise ValueError(f"Unknown remove edge: {left}--{right}")
        edges.discard(tuple(sorted((left, right))))
    for left, right in add or []:
        if left not in valid or right not in valid:
            raise ValueError(f"Unknown add edge: {left}--{right}")
        if left == right:
            raise ValueError(f"Unexpected self-loop add: {left}")
        edges.add(tuple(sorted((left, right))))
    return sort_edges(edges, nodes)


def adjacency(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: pos for pos, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for left, right in edges:
        i = index[left]
        j = index[right]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = adjacency(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        writer.writerows(edges)


def qa(round_graph: RoundGraph) -> dict[str, object]:
    matrix = adjacency(round_graph.nodes, round_graph.edges)
    return {
        "round": round_graph.name,
        "agent": round_graph.agent,
        "node_count": len(round_graph.nodes),
        "edge_count": len(round_graph.edges),
        "matrix_size": [len(round_graph.nodes), len(round_graph.nodes)],
        "symmetric": all(
            matrix[i][j] == matrix[j][i]
            for i in range(len(round_graph.nodes))
            for j in range(len(round_graph.nodes))
        ),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(round_graph.nodes))),
        "isolated_nodes": [
            node for node, row in zip(round_graph.nodes, matrix) if not any(row)
        ],
        "note": round_graph.note,
        "uncertain_or_rejected_edges": UNCERTAIN_BY_ROUND.get(round_graph.name, []),
    }


def build_rounds() -> list[RoundGraph]:
    diego_r1 = parse_edges(EDGE_TEXT_DIEGO_R1, NODES_DIEGO_R1)
    jennifer_base = parse_edges(EDGE_TEXT_JENNIFER_R1, NODES)
    jennifer_r1 = with_deltas(
        jennifer_base,
        NODES,
        add=JENNIFER_R1_ADD,
        remove=JENNIFER_R1_REMOVE,
    )
    diego_r2 = with_deltas(jennifer_r1, NODES, add=DIEGO_R2_ADD)
    jennifer_r2 = with_deltas(diego_r2, NODES, add=JENNIFER_R2_ADD)
    diego_r3 = with_deltas(jennifer_r2, NODES, add=DIEGO_R3_ADD)
    jennifer_r3 = with_deltas(jennifer_r2, NODES, add=JENNIFER_R3_ADD)

    return [
        RoundGraph(
            "round01_diego",
            "Diego",
            NODES_DIEGO_R1,
            diego_r1,
            ROUND_NOTES["round01_diego"],
        ),
        RoundGraph(
            "round02_jennifer",
            "Jennifer",
            NODES,
            jennifer_r1,
            ROUND_NOTES["round02_jennifer"],
        ),
        RoundGraph(
            "round03_diego",
            "Diego",
            NODES,
            diego_r2,
            ROUND_NOTES["round03_diego"],
        ),
        RoundGraph(
            "round04_jennifer",
            "Jennifer",
            NODES,
            jennifer_r2,
            ROUND_NOTES["round04_jennifer"],
        ),
        RoundGraph(
            "round05_diego",
            "Diego",
            NODES,
            diego_r3,
            ROUND_NOTES["round05_diego"],
        ),
        RoundGraph(
            "round06_jennifer_final",
            "Jennifer",
            NODES,
            jennifer_r3,
            ROUND_NOTES["round06_jennifer_final"],
        ),
    ]


def write_rounds_summary(rounds: list[RoundGraph]) -> None:
    lines = [
        "# Document 9 Connectivity Extraction",
        "",
        "Resources used: only document 9 `Raw + wires` images and generated crops.",
        "No GT, GT-derived feedback, or OCR engine was used.",
        "",
        "## Rounds",
        "",
    ]
    previous_edges: set[tuple[str, str]] | None = None
    previous_nodes: list[str] | None = None
    for round_graph in rounds:
        current_edges = set(round_graph.edges)
        lines.append(f"### {round_graph.name} ({round_graph.agent})")
        lines.append(f"- Nodes: {len(round_graph.nodes)}")
        lines.append(f"- Edges: {len(round_graph.edges)}")
        lines.append(f"- Note: {round_graph.note}")
        if previous_edges is not None and previous_nodes == round_graph.nodes:
            added = sorted(current_edges - previous_edges)
            removed = sorted(previous_edges - current_edges)
            lines.append(f"- Added vs previous: {len(added)}")
            if added:
                lines.append("  - " + "; ".join(f"{a}--{b}" for a, b in added))
            lines.append(f"- Removed vs previous: {len(removed)}")
            if removed:
                lines.append("  - " + "; ".join(f"{a}--{b}" for a, b in removed))
        elif previous_edges is not None:
            lines.append("- Added/removed vs previous: not compared because node label changed.")
        uncertain = UNCERTAIN_BY_ROUND.get(round_graph.name, [])
        if uncertain:
            lines.append(f"- Uncertain/rejected notes: {len(uncertain)}")
        lines.append("")
        previous_edges = current_edges
        previous_nodes = round_graph.nodes

    final_round = rounds[-1]
    lines.extend(
        [
            "## Final",
            "",
            f"- Final nodes: {len(final_round.nodes)}",
            f"- Final unique undirected edges: {len(final_round.edges)}",
            "- Diagonal: 0 for all nodes; no self-loops observed.",
            "- Matrix: `final_matrix.csv`",
            "- Edge list: `final_edges.csv`",
            "- Node order: `final_nodes.csv`",
            "",
            "Saturation: Jennifer R3 accepted only PN-LTG-1B--JB-NORM-A and "
            "PUMP-SI-B--JB-2B from Diego R3. Remaining count shortfall was not "
            "filled because the candidate routes were shared trunks, crossings, "
            "near-routes, or lacked clear endpoints.",
        ]
    )
    (RESULTS / "rounds_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds = build_rounds()
    qa_rows = []

    for round_graph in rounds:
        write_matrix(RESULTS / f"{round_graph.name}_matrix.csv", round_graph.nodes, round_graph.edges)
        write_edges(RESULTS / f"{round_graph.name}_edges.csv", round_graph.edges)
        qa_rows.append(qa(round_graph))

    final_round = rounds[-1]
    write_matrix(RESULTS / "final_matrix.csv", final_round.nodes, final_round.edges)
    write_edges(RESULTS / "final_edges.csv", final_round.edges)

    with (RESULTS / "final_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "component"])
        for index, node in enumerate(final_round.nodes, start=1):
            writer.writerow([index, node])

    final_adjacency = {
        node: sorted(
            other
            for left, right in final_round.edges
            for other in (
                [right] if left == node else [left] if right == node else []
            )
        )
        for node in final_round.nodes
    }
    (RESULTS / "final_adjacency.json").write_text(
        json.dumps(final_adjacency, indent=2),
        encoding="utf-8",
    )
    (RESULTS / "qa_summary.json").write_text(
        json.dumps(qa_rows, indent=2),
        encoding="utf-8",
    )
    (RESULTS / "uncertain_rejected_edges_by_round.json").write_text(
        json.dumps(UNCERTAIN_BY_ROUND, indent=2),
        encoding="utf-8",
    )
    write_rounds_summary(rounds)

    print(json.dumps(qa_rows, indent=2))


if __name__ == "__main__":
    main()
