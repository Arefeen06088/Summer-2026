from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    evidence: str
    status: str = "confirmed"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[str]
    edges: list[Edge]
    uncertain_edges: list[Edge]
    include_uncertain_in_matrix: bool
    notes: list[str]


SOURCE_NODES = [
    "UTIL-230A", "DS-230A", "SAT-1A", "CB-SAT-A", "GEN-1A",
    "CB-GEN-1", "BUS-13K-01", "UAT-1A", "CB-UAT-1A", "UAT-1B",
    "CB-UAT-1B", "BUS-4160-N1", "CB-TIE-41N", "BUS-4160-N2",
    "CB-SAT-B", "SAT-1B", "DS-230B", "UTIL-230B",
]

TRAIN_A_SAFETY_NODES = [
    "EDG-1A", "CB-EDG-A", "BUS-4160S1A", "CB-481A", "TR-480-A1",
    "CB-LV-A1", "BUS-480-A1", "MCC-SAF-A1", "CB-RHR-A",
    "PUMP-RHR-A", "CB-SI-A", "PUMP-SI-A", "CB-CCW-A",
    "PUMP-CCW-A", "CB-482A", "TR-480-A2", "CB-LV-A2",
    "BUS-480-A2", "MCC-SAF-A2", "CB-CVC-A", "PUMP-CVC-A",
    "CB-CRF-A", "FAN-CR-A", "CB-COMP-A", "COMP-AIR-A",
    "PN-MOV-A", "FU-8810A", "MOV-8810A", "FU-HV302A",
    "VLV-HV-302A", "FU-RCICA", "MOV-RCIC-A", "FU-SWA",
    "MOV-SW-A", "CT-41A", "PT-41A", "RELAY-50/51A", "RELAY-86A",
]

NORMAL_480_NODES = [
    "CB-4160-N1A", "TR-480-N1A", "CB-480-N1A", "BUS-480-N1A",
    "MCC-NORM-1A", "PN-480-N1A", "CB-CWP-1A", "PUMP-CWP-1A",
    "CB-HEAT-1A", "HTR-1A", "CB-AHU-1A", "FAN-AHU-1A",
    "CB-4160-N1B", "TR-480-N1B", "CB-480-N1B", "BUS-480-N1B",
    "MCC-NORM-1B", "PN-480-N1B", "CB-CWP-1B", "PUMP-CWP-1B",
    "CB-SUMP-1B", "PUMP-SUMP-1B", "CB-LTG-1B", "PN-LTG-1B",
    "CB-4160-N2A", "TR-480-N2A", "CB-480-N2A", "BUS-480-N2A",
    "MCC-NORM-2A", "PN-480-N2A", "CB-CWP-2A", "PUMP-CWP-2A",
    "CB-VAC-2A", "PUMP-VAC-2A", "CB-AHU-2A", "FAN-AHU-2A",
    "CB-4160-N2B", "TR-480-N2B", "CB-480-N2B", "BUS-480-N2B",
    "MCC-NORM-2B", "PN-480-N2B", "CB-CWP-2B", "PUMP-CWP-2B",
    "CB-OIL-2B", "PUMP-OIL-2B", "CB-LTG-2B", "PN-LTG-2B",
]

RTD_NODES = [
    "MTR-480-N1", "JB-NORM-A", "RTD-PNL-A", "TB-SEQ-A", "TDR-SEQ-A",
    "MTR-480-N2", "JB-NORM-B", "RTD-PNL-B", "TB-SEQ-B", "TDR-SEQ-B",
]

TRAIN_B_SAFETY_NODES = [
    "EDG-1B", "CB-EDG-B", "BUS-4160S1B", "CB-481B", "TR-480-B1",
    "CB-LV-B1", "BUS-480-B1", "MCC-SAF-B1", "CB-RHR-B",
    "PUMP-RHR-B", "CB-SI-B", "PUMP-SI-B", "CB-CCW-B",
    "PUMP-CCW-B", "CB-482B", "TR-480-B2", "CB-LV-B2",
    "BUS-480-B2", "MCC-SAF-B2", "CB-CVC-B", "PUMP-CVC-B",
    "CB-CRF-B", "FAN-CR-B", "CB-COMP-B", "COMP-AIR-B",
    "PN-MOV-B", "FU-8810B", "MOV-8810B", "FU-HV302B",
    "VLV-HV-302B", "FU-RCICB", "MOV-RCIC-B", "FU-SWB",
    "MOV-SW-B", "CT-41B", "PT-41B", "RELAY-27B", "RELAY-86B",
]

TRAIN_A_CONTROL_NODES = [
    "BAT-125A", "CHG-125A", "BUS-125DC-A", "GND-A", "PN-125A",
    "INV-120A", "BUS-120AC-A", "PN-120A", "JB-1A", "JB-2A",
    "PLC-ESF-A", "RELAY-K1A", "RELAY-K2A", "ANN-ESF-A",
]

TRAIN_B_CONTROL_NODES = [
    "BAT-125B", "CHG-125B", "BUS-125DC-B", "GND-B", "PN-125B",
    "INV-120B", "BUS-120AC-B", "PN-120B", "JB-1B", "JB-2B",
    "PLC-ESF-B", "RELAY-K1B", "RELAY-K2B", "ANN-ESF-B",
]

FINAL_NODES = (
    SOURCE_NODES
    + TRAIN_A_SAFETY_NODES
    + NORMAL_480_NODES
    + RTD_NODES
    + TRAIN_B_SAFETY_NODES
    + TRAIN_A_CONTROL_NODES
    + TRAIN_B_CONTROL_NODES
)


def edge(source: str, target: str, evidence: str, status: str = "confirmed") -> Edge:
    return Edge(source, target, evidence, status)


def chain(items: list[str], evidence: str) -> list[Edge]:
    return [edge(a, b, evidence) for a, b in zip(items, items[1:])]


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    result: list[Edge] = []
    for item in edges:
        key = edge_key(item.source, item.target)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


SOURCE_EDGES = (
    chain(["UTIL-230A", "DS-230A", "SAT-1A", "CB-SAT-A", "BUS-4160S1A"], "solid utility/SAT A feed")
    + chain(["UTIL-230B", "DS-230B", "SAT-1B", "CB-SAT-B", "BUS-4160S1B"], "solid utility/SAT B feed")
    + chain(["GEN-1A", "CB-GEN-1", "BUS-13K-01"], "solid generator to 13 kV bus")
    + chain(["BUS-13K-01", "UAT-1A", "CB-UAT-1A", "BUS-4160-N1"], "solid UAT 1A feed")
    + chain(["BUS-13K-01", "UAT-1B", "CB-UAT-1B", "BUS-4160-N2"], "solid UAT 1B feed")
    + chain(["BUS-4160-N1", "CB-TIE-41N", "BUS-4160-N2"], "solid normal 4.16 kV bus tie")
)

TRAIN_A_SAFETY_EDGES = (
    chain(["EDG-1A", "CB-EDG-A", "BUS-4160S1A"], "solid EDG A feed")
    + chain(["BUS-4160S1A", "CB-481A", "TR-480-A1", "CB-LV-A1", "BUS-480-A1", "MCC-SAF-A1"], "solid Train A safety 480 branch A1")
    + chain(["MCC-SAF-A1", "CB-RHR-A", "PUMP-RHR-A"], "solid Train A safety load branch")
    + chain(["MCC-SAF-A1", "CB-SI-A", "PUMP-SI-A"], "solid Train A safety load branch")
    + chain(["MCC-SAF-A1", "CB-CCW-A", "PUMP-CCW-A"], "solid Train A safety load branch")
    + chain(["BUS-4160S1A", "CB-482A", "TR-480-A2", "CB-LV-A2", "BUS-480-A2", "MCC-SAF-A2"], "solid Train A safety 480 branch A2")
    + chain(["MCC-SAF-A2", "CB-CVC-A", "PUMP-CVC-A"], "solid Train A safety load branch")
    + chain(["MCC-SAF-A2", "CB-CRF-A", "FAN-CR-A"], "solid Train A safety load branch")
    + chain(["MCC-SAF-A2", "CB-COMP-A", "COMP-AIR-A"], "solid Train A safety load branch")
    + [edge("MCC-SAF-A2", "PN-MOV-A", "solid Train A MOV panel feed")]
    + chain(["PN-MOV-A", "FU-8810A", "MOV-8810A"], "solid Train A MOV fused branch")
    + chain(["PN-MOV-A", "FU-HV302A", "VLV-HV-302A"], "solid Train A MOV fused branch")
    + chain(["PN-MOV-A", "FU-RCICA", "MOV-RCIC-A"], "solid Train A MOV fused branch")
    + chain(["PN-MOV-A", "FU-SWA", "MOV-SW-A"], "solid Train A MOV fused branch")
)

TRAIN_B_SAFETY_EDGES = (
    chain(["EDG-1B", "CB-EDG-B", "BUS-4160S1B"], "solid EDG B feed")
    + chain(["BUS-4160S1B", "CB-481B", "TR-480-B1", "CB-LV-B1", "BUS-480-B1", "MCC-SAF-B1"], "solid Train B safety 480 branch B1")
    + chain(["MCC-SAF-B1", "CB-RHR-B", "PUMP-RHR-B"], "solid Train B safety load branch")
    + chain(["MCC-SAF-B1", "CB-SI-B", "PUMP-SI-B"], "solid Train B safety load branch")
    + chain(["MCC-SAF-B1", "CB-CCW-B", "PUMP-CCW-B"], "solid Train B safety load branch")
    + chain(["BUS-4160S1B", "CB-482B", "TR-480-B2", "CB-LV-B2", "BUS-480-B2", "MCC-SAF-B2"], "solid Train B safety 480 branch B2")
    + chain(["MCC-SAF-B2", "CB-CVC-B", "PUMP-CVC-B"], "solid Train B safety load branch")
    + chain(["MCC-SAF-B2", "CB-CRF-B", "FAN-CR-B"], "solid Train B safety load branch")
    + chain(["MCC-SAF-B2", "CB-COMP-B", "COMP-AIR-B"], "solid Train B safety load branch")
    + [edge("MCC-SAF-B2", "PN-MOV-B", "solid Train B MOV panel feed")]
    + chain(["PN-MOV-B", "FU-8810B", "MOV-8810B"], "solid Train B MOV fused branch")
    + chain(["PN-MOV-B", "FU-HV302B", "VLV-HV-302B"], "solid Train B MOV fused branch")
    + chain(["PN-MOV-B", "FU-RCICB", "MOV-RCIC-B"], "solid Train B MOV fused branch")
    + chain(["PN-MOV-B", "FU-SWB", "MOV-SW-B"], "solid Train B MOV fused branch")
)

NORMAL_480_EDGES = (
    chain(["BUS-4160-N1", "CB-4160-N1A", "TR-480-N1A", "CB-480-N1A", "BUS-480-N1A", "MCC-NORM-1A", "PN-480-N1A"], "solid normal 480 N1A branch")
    + chain(["PN-480-N1A", "CB-CWP-1A", "PUMP-CWP-1A"], "solid normal 480 load branch")
    + chain(["PN-480-N1A", "CB-HEAT-1A", "HTR-1A"], "solid normal 480 load branch")
    + chain(["PN-480-N1A", "CB-AHU-1A", "FAN-AHU-1A"], "solid normal 480 load branch")
    + chain(["BUS-4160-N1", "CB-4160-N1B", "TR-480-N1B", "CB-480-N1B", "BUS-480-N1B", "MCC-NORM-1B", "PN-480-N1B"], "solid normal 480 N1B branch")
    + chain(["PN-480-N1B", "CB-CWP-1B", "PUMP-CWP-1B"], "solid normal 480 load branch")
    + chain(["PN-480-N1B", "CB-SUMP-1B", "PUMP-SUMP-1B"], "solid normal 480 load branch")
    + chain(["PN-480-N1B", "CB-LTG-1B", "PN-LTG-1B"], "solid normal 480 load branch")
    + chain(["BUS-4160-N2", "CB-4160-N2A", "TR-480-N2A", "CB-480-N2A", "BUS-480-N2A", "MCC-NORM-2A", "PN-480-N2A"], "solid normal 480 N2A branch")
    + chain(["PN-480-N2A", "CB-CWP-2A", "PUMP-CWP-2A"], "solid normal 480 load branch")
    + chain(["PN-480-N2A", "CB-VAC-2A", "PUMP-VAC-2A"], "solid normal 480 load branch")
    + chain(["PN-480-N2A", "CB-AHU-2A", "FAN-AHU-2A"], "solid normal 480 load branch")
    + chain(["BUS-4160-N2", "CB-4160-N2B", "TR-480-N2B", "CB-480-N2B", "BUS-480-N2B", "MCC-NORM-2B", "PN-480-N2B"], "solid normal 480 N2B branch")
    + chain(["PN-480-N2B", "CB-CWP-2B", "PUMP-CWP-2B"], "solid normal 480 load branch")
    + chain(["PN-480-N2B", "CB-OIL-2B", "PUMP-OIL-2B"], "solid normal 480 load branch")
    + chain(["PN-480-N2B", "CB-LTG-2B", "PN-LTG-2B"], "solid normal 480 load branch")
)

RTD_CHAIN_EDGES = (
    chain(["MTR-480-N1", "JB-NORM-A", "RTD-PNL-A", "TB-SEQ-A", "TDR-SEQ-A"], "dashed normal RTD/control chain")
    + chain(["MTR-480-N2", "JB-NORM-B", "RTD-PNL-B", "TB-SEQ-B", "TDR-SEQ-B"], "dashed normal RTD/control chain")
)

DC_POWER_EDGES = (
    chain(["BAT-125A", "BUS-125DC-A"], "solid battery feed to DC bus")
    + chain(["CHG-125A", "BUS-125DC-A"], "solid charger feed to DC bus")
    + [
        edge("BUS-125DC-A", "GND-A", "ground symbol tied to DC bus"),
        edge("BUS-125DC-A", "PN-125A", "solid DC panel feed"),
    ]
    + chain(["BUS-125DC-A", "INV-120A", "BUS-120AC-A", "PN-120A"], "solid inverter and 120 VAC panel feed")
    + chain(["BAT-125B", "BUS-125DC-B"], "solid battery feed to DC bus")
    + chain(["CHG-125B", "BUS-125DC-B"], "solid charger feed to DC bus")
    + [
        edge("BUS-125DC-B", "GND-B", "ground symbol tied to DC bus"),
        edge("BUS-125DC-B", "PN-125B", "solid DC panel feed"),
    ]
    + chain(["BUS-125DC-B", "INV-120B", "BUS-120AC-B", "PN-120B"], "solid inverter and 120 VAC panel feed")
)

PROTECTION_EDGES = (
    chain(["BUS-4160S1A", "CT-41A", "RELAY-50/51A"], "dashed A-side CT relay path")
    + chain(["BUS-4160S1A", "PT-41A", "RELAY-50/51A"], "dashed A-side PT relay path")
    + [edge("RELAY-50/51A", "RELAY-86A", "dashed A-side protection relay path")]
    + chain(["BUS-4160S1B", "CT-41B", "RELAY-27B"], "dashed B-side CT relay path")
    + chain(["BUS-4160S1B", "PT-41B", "RELAY-27B"], "dashed B-side PT relay path")
    + [edge("RELAY-27B", "RELAY-86B", "dashed B-side protection relay path")]
)

JENNIFER_ADDITIONS = [
    edge("PUMP-SUMP-1B", "MTR-480-N1", "dashed source path to normal RTD/control meter"),
    edge("FAN-AHU-2A", "MTR-480-N2", "dashed source path to normal RTD/control meter"),
    edge("PN-125A", "JB-1A", "dashed Train A DC panel to junction box"),
    edge("PN-125A", "JB-2A", "dashed Train A DC panel to junction box"),
    edge("PN-125B", "JB-1B", "dashed Train B DC panel to junction box"),
    edge("PN-125B", "JB-2B", "dashed Train B DC panel to junction box"),
    edge("PN-120A", "PLC-ESF-A", "dashed Train A AC/control panel to PLC"),
    edge("PN-120B", "PLC-ESF-B", "dashed Train B AC/control panel to PLC"),
    edge("PLC-ESF-A", "RELAY-K1A", "dashed Train A PLC relay path"),
    edge("PLC-ESF-A", "RELAY-K2A", "dashed Train A PLC relay path"),
    edge("PLC-ESF-A", "ANN-ESF-A", "dashed Train A PLC annunciator path"),
    edge("PLC-ESF-B", "RELAY-K1B", "dashed Train B PLC relay path"),
    edge("PLC-ESF-B", "RELAY-K2B", "dashed Train B PLC relay path"),
    edge("PLC-ESF-B", "ANN-ESF-B", "dashed Train B PLC annunciator path"),
]

DIEGO_CONFIRMED_EDGES = dedupe_edges(
    SOURCE_EDGES
    + TRAIN_A_SAFETY_EDGES
    + TRAIN_B_SAFETY_EDGES
    + NORMAL_480_EDGES
    + RTD_CHAIN_EDGES
    + DC_POWER_EDGES
    + PROTECTION_EDGES
)

FINAL_EDGES = dedupe_edges(DIEGO_CONFIRMED_EDGES + JENNIFER_ADDITIONS)

DIEGO_R1_UNCERTAIN = [
    edge("RELAY-86A", "CB-EDG-A", "A-side lockout trip path visible but endpoint is not isolated", "uncertain_included"),
    edge("RELAY-86A", "CB-482A", "A-side lockout trip path visible but endpoint is not isolated", "uncertain_included"),
    edge("RELAY-86A", "CB-TIE-41N", "possible tie trip path, not endpoint-clean", "uncertain_included"),
    edge("RELAY-86B", "CB-EDG-B", "B-side lockout trip path visible but endpoint is not isolated", "uncertain_included"),
    edge("RELAY-86B", "CB-481B", "B-side lockout trip path visible but endpoint is not isolated", "uncertain_included"),
    edge("RELAY-86B", "CB-482B", "B-side lockout trip path visible but endpoint is not isolated", "uncertain_included"),
    edge("FAN-CR-A", "PN-MOV-A", "possible solid continuation near fan/MOV-panel geometry", "uncertain_included"),
    edge("FAN-CR-B", "PN-MOV-B", "possible solid continuation near fan/MOV-panel geometry", "uncertain_included"),
] + [Edge(item.source, item.target, item.evidence, "uncertain_included") for item in JENNIFER_ADDITIONS]

FINAL_UNCERTAIN = [
    edge("RELAY-86A", "CB-EDG-A", "dashed lockout trip route crosses the area but endpoint is ambiguous", "uncertain_excluded"),
    edge("RELAY-86A", "CB-482A", "dashed lockout trip route crosses the area but endpoint is ambiguous", "uncertain_excluded"),
    edge("RELAY-86A", "CB-TIE-41N", "possible tie trip route lacks clear named endpoint", "uncertain_excluded"),
    edge("RELAY-86B", "CB-EDG-B", "dashed lockout trip route crosses the area but endpoint is ambiguous", "uncertain_excluded"),
    edge("RELAY-86B", "CB-481B", "dashed lockout trip route crosses the area but endpoint is ambiguous", "uncertain_excluded"),
    edge("RELAY-86B", "CB-482B", "dashed lockout trip route crosses the area but endpoint is ambiguous", "uncertain_excluded"),
    edge("FAN-CR-A", "PN-MOV-A", "fan-area linework too close to promote as a separate edge", "uncertain_excluded"),
    edge("FAN-CR-B", "PN-MOV-B", "fan-area linework too close to promote as a separate edge", "uncertain_excluded"),
    edge("CHG-125A", "BAT-125A", "charger and battery separately drop to BUS-125DC-A; no direct conductor", "uncertain_excluded"),
    edge("CHG-125B", "BAT-125B", "charger and battery separately drop to BUS-125DC-B; no direct conductor", "uncertain_excluded"),
    edge("PN-120A", "ANN-ESF-A", "clearest path is through PLC-ESF-A, not direct", "uncertain_excluded"),
    edge("PN-120B", "ANN-ESF-B", "clearest path is through PLC-ESF-B, not direct", "uncertain_excluded"),
    edge("RELAY-K1A/K2A", "ANN-ESF-A", "relay-to-annunciator variants are not endpoint-clean", "uncertain_excluded"),
    edge("RELAY-K1B/K2B", "ANN-ESF-B", "relay-to-annunciator variants are not endpoint-clean", "uncertain_excluded"),
]

ROUNDS = [
    RoundSpec(
        "round_01",
        "diego",
        "high_recall_extractor",
        FINAL_NODES,
        DIEGO_CONFIRMED_EDGES,
        DIEGO_R1_UNCERTAIN,
        True,
        [
            "High-recall extraction from raw PNG and crops generated only from that PNG.",
            "Included visually plausible trip-output, fan/MOV-panel, RTD source, and bottom-control candidates in the round matrix.",
            "Highlighted label spellings for Jennifer: BUS-4160S1A/B, FU-RCICA/B, FU-SWA/B, FU-HV302A/B, and MTR-480-N1/N2.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_01",
        "jennifer",
        "precision_reviewer_refiner",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Precision review confirmed the 180 visible-node set and exact label spellings.",
            "Added RTD source edges and bottom DC/control dashed edges.",
            "Excluded lockout trip-output guesses, fan-to-MOV-panel candidates, and direct annunciator variants.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_02",
        "diego",
        "high_recall_extractor_consensus",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Round 2 Diego accepted Jennifer's precision decisions.",
            "Confirmed RTD/TB/TDR chains remain in the final graph.",
            "Confirmed CHG-125A/B to BAT-125A/B direct edges should remain excluded.",
        ],
    ),
    RoundSpec(
        "round_02",
        "jennifer",
        "precision_reviewer_final",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Final precision review agreed saturation was reached with Diego.",
            "Final matrix keeps 180 visible component/node labels.",
            "Final graph was not forced to match unreadable/faint title-block counts; visible named endpoints controlled the result.",
            "No GT or GT-derived resources were used.",
        ],
    ),
]


def matrix_edges(spec: RoundSpec) -> list[Edge]:
    edges = list(spec.edges)
    if spec.include_uncertain_in_matrix:
        node_set = set(spec.nodes)
        edges.extend([item for item in spec.uncertain_edges if item.source in node_set and item.target in node_set])
    return dedupe_edges(edges)


def validate_spec(spec: RoundSpec) -> dict[str, int | str]:
    nodes = spec.nodes
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{spec.round_id} {spec.actor} duplicate nodes: {duplicates}")
    node_set = set(nodes)
    edges = matrix_edges(spec)
    missing = sorted({endpoint for item in edges for endpoint in (item.source, item.target) if endpoint not in node_set})
    if missing:
        raise ValueError(f"{spec.round_id} {spec.actor} missing edge endpoints: {missing}")
    if any(item.source == item.target for item in edges):
        raise ValueError(f"{spec.round_id} {spec.actor} contains self-loop")
    if len(edges) != len({edge_key(item.source, item.target) for item in edges}):
        raise ValueError(f"{spec.round_id} {spec.actor} contains duplicate undirected edges")
    return {
        "round": spec.round_id,
        "actor": spec.actor,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "uncertain_item_count": len(spec.uncertain_edges),
        "symmetric": "yes",
        "diagonal_zero": "yes",
    }


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    adjacency = {edge_key(item.source, item.target) for item in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *nodes])
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(edge_key(row_node, col_node) in adjacency))
            writer.writerow(row)


def write_node_map(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "component"])
        for index, node in enumerate(nodes, start=1):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "status", "evidence"])
        for item in edges:
            writer.writerow([item.source, item.target, item.status, item.evidence])


def write_notes(path: Path, spec: RoundSpec, metrics: dict[str, int | str]) -> None:
    lines = [
        f"# {spec.round_id} {spec.actor.title()}",
        "",
        f"Role: {spec.role}",
        "",
        "Evidence source: raw schematic PNG and crops generated only from that PNG.",
        "",
        f"Node count: {metrics['node_count']}",
        f"Matrix edge count: {metrics['edge_count']}",
        f"Uncertain item count: {metrics['uncertain_item_count']}",
        "",
        "Notes:",
    ]
    lines.extend([f"- {note}" for note in spec.notes])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def copy_final_artifacts(final_prefix: str) -> None:
    copies = [
        (f"{final_prefix}_connectivity_matrix.csv", "final_connectivity_matrix.csv"),
        (f"{final_prefix}_edges.csv", "final_edges.csv"),
        (f"{final_prefix}_node_map.csv", "final_node_map.csv"),
        (f"{final_prefix}_uncertain_edges.csv", "final_uncertain_edges.csv"),
        (f"{final_prefix}_notes.md", "final_notes.md"),
        (f"{final_prefix}_connectivity_matrix.csv", "connectivity_matrix_final.csv"),
        (f"{final_prefix}_edges.csv", "edge_candidates_jennifer_round4_final.csv"),
    ]
    for source_name, target_name in copies:
        shutil.copyfile(RESULTS / source_name, RESULTS / target_name)


def write_tracking(metrics_rows: list[dict[str, int | str]], prefixes: list[str]) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    with (RESULTS / "token_performance_tracking.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "timestamp_local", "round_id", "actor", "role", "node_count",
            "edge_count", "uncertain_item_count", "token_telemetry", "artifact_prefix",
        ])
        for spec, metrics, prefix in zip(ROUNDS, metrics_rows, prefixes):
            writer.writerow([
                now, spec.round_id, spec.actor, spec.role, metrics["node_count"],
                metrics["edge_count"], metrics["uncertain_item_count"],
                "not available from current goal telemetry", prefix,
            ])

    notes = [
        "# Token Performance Notes",
        "",
        "- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and notes telemetry as unavailable.",
        "- Two deployed subagents were used: Diego for high-recall extraction and Jennifer for precision review/refinement.",
        "- The process saturated after Diego round 2 and Jennifer round 2 agreed on the same final matrix.",
        "- Only the raw schematic PNG and crops generated from that raw PNG were used; no GT or GT-derived resources were used.",
        "",
    ]
    (RESULTS / "token_performance_notes.md").write_text("\n".join(notes), encoding="utf-8")


def write_validation(metrics_rows: list[dict[str, int | str]]) -> None:
    with (RESULTS / "connectivity_matrix_validation_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["round", "actor", "node_count", "edge_count", "uncertain_item_count", "symmetric", "diagonal_zero"],
        )
        writer.writeheader()
        writer.writerows(metrics_rows)
    final = metrics_rows[-1]
    summary = [
        "Connectivity matrix validation summary",
        "",
        f"Final round: {final['round']} {final['actor']}",
        f"Final node count: {final['node_count']}",
        f"Final edge count: {final['edge_count']}",
        f"Symmetric: {final['symmetric']}",
        f"Diagonal zero: {final['diagonal_zero']}",
        "Duplicate nodes: none",
        "Missing edge endpoints: none",
        "Self-loops: none",
        "",
    ]
    (RESULTS / "connectivity_matrix_validation_summary.txt").write_text("\n".join(summary), encoding="utf-8")


def write_extraction_notes() -> None:
    lines = [
        "# Extraction Notes",
        "",
        "Case: 9 Raw",
        "",
        "Evidence used:",
        "- Raw schematic PNG in the Raw folder.",
        "- Crops generated from that same PNG and stored under results/crops.",
        "- No Ground Truth or GT-derived feedback/resources were used.",
        "",
        "Final consensus:",
        "- Diego and Jennifer agreed after two rounds.",
        "- Final node count is 180 visible component/node labels.",
        f"- Final confirmed edge count is {len(FINAL_EDGES)}.",
        "- Lockout trip-output guesses, fan-to-MOV-panel candidates, direct charger-to-battery edges, and direct annunciator variants were excluded.",
        "- Unreadable/faint title-block counts were not forced; visible named endpoints controlled the matrix.",
        "",
    ]
    (RESULTS / "extraction_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    metrics_rows: list[dict[str, int | str]] = []
    prefixes: list[str] = []
    for spec in ROUNDS:
        prefix = f"{spec.round_id}_{spec.actor}"
        prefixes.append(prefix)
        metrics = validate_spec(spec)
        metrics_rows.append(metrics)
        edges = matrix_edges(spec)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", spec.nodes, edges)
        write_node_map(RESULTS / f"{prefix}_node_map.csv", spec.nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_edges(RESULTS / f"{prefix}_uncertain_edges.csv", spec.uncertain_edges)
        write_notes(RESULTS / f"{prefix}_notes.md", spec, metrics)

    copy_final_artifacts("round_02_jennifer")
    write_tracking(metrics_rows, prefixes)
    write_validation(metrics_rows)
    write_extraction_notes()


if __name__ == "__main__":
    main()
