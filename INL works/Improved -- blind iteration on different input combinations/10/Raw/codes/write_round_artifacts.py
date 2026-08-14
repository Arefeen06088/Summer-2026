from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw")
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


COMMON_NODES = [
    "SRC-345KV",
    "BUS-SWY-345KV",
    "GEN-01",
    "UAT-1",
    "CB-UAT",
    "SAT-1",
    "CB-SAT",
    "CB-TIE-AB",
]

DIVISION_A_POWER_NODES = [
    "BUS-4160-A",
    "DG-1A",
    "CB-DGA",
    "CB-A01",
    "CB-A02",
    "CB-A03",
    "CB-A04",
    "CB-A05",
    "CB-A06",
    "CB-A07",
    "CB-A08",
    "CB-A09",
    "TR-480-A1",
    "TR-480-A2",
    "PUMP-RHR-A",
    "PUMP-CS-A",
    "PUMP-AFW-A",
    "TR-UPS-A",
    "CHLR-A",
    "FAN-CR-A",
    "LC-101A",
    "DS-A01",
    "MCC-101A",
    "MOV-101A",
    "MOV-102A",
    "JB-101A",
    "LC-102A",
    "DS-A02",
    "MCC-102A",
    "MCC-103A",
    "AOV-101A",
    "PUMP-CCW-A",
    "FAN-AB-A",
    "HTR-TRACE-A",
]

DIVISION_A_CONTROL_NODES = [
    "TB-SWGR-A",
    "RLY-27A",
    "RLY-50A",
    "RLY-86A",
    "PT-4160-A",
    "CT-4160-A",
    "PNL-RPS-A",
    "PNL-ESFAS-A",
    "TB-LV-A",
    "FUSE-A01",
    "FUSE-A02",
    "RECT-1A",
    "BCHG-1A",
    "BAT-1A",
    "BUS-DC-A",
    "INV-1A",
    "BUS-UPS-A",
    "PNL-UPS-A",
    "GND-A",
]

DIVISION_B_POWER_NODES = [
    "BUS-4160-B",
    "DG-1B",
    "CB-DGB",
    "CB-B01",
    "CB-B02",
    "CB-B03",
    "CB-B04",
    "CB-B05",
    "CB-B06",
    "CB-B07",
    "CB-B08",
    "CB-B09",
    "TR-480-B1",
    "TR-480-B2",
    "PUMP-RHR-B",
    "PUMP-CS-B",
    "PUMP-AFW-B",
    "TR-UPS-B",
    "CHLR-B",
    "FAN-CR-B",
    "LC-101B",
    "DS-B01",
    "MCC-101B",
    "MOV-101B",
    "MOV-102B",
    "JB-101B",
    "LC-102B",
    "DS-B02",
    "MCC-102B",
    "MCC-103B",
    "AOV-101B",
    "PUMP-CCW-B",
    "FAN-AB-B",
    "HTR-TRACE-B",
]

DIVISION_B_CONTROL_NODES = [
    "TB-SWGR-B",
    "RLY-27B",
    "RLY-50B",
    "RLY-86B",
    "PT-4160-B",
    "CT-4160-B",
    "PNL-RPS-B",
    "PNL-ESFAS-B",
    "TB-LV-B",
    "FUSE-B01",
    "FUSE-B02",
    "RECT-1B",
    "BCHG-1B",
    "BAT-1B",
    "BUS-DC-B",
    "INV-1B",
    "BUS-UPS-B",
    "PNL-UPS-B",
    "GND-B",
]

MCR_NODES = [
    "PNL-MCR-01",
    "PNL-ANN-01",
    "SER-01",
    "JB-CONTROL",
]

HELPER_LABEL_NODES = [
    "CT-CAB-A",
    "CT-CAB-B",
    "480V LC FEEDERS-A",
    "480V LC FEEDERS-B",
    "MCR / ANNUNCIATOR CONTROL BAY",
]

FINAL_NODES = (
    COMMON_NODES
    + DIVISION_A_POWER_NODES
    + DIVISION_A_CONTROL_NODES
    + DIVISION_B_POWER_NODES
    + DIVISION_B_CONTROL_NODES
    + MCR_NODES
)

DIEGO_R1_NODES = FINAL_NODES + HELPER_LABEL_NODES


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
    chain(["SRC-345KV", "BUS-SWY-345KV", "SAT-1", "CB-SAT", "BUS-4160-B"], "solid offsite 345 kV/sat feed to B bus")
    + chain(["GEN-01", "UAT-1", "CB-UAT", "BUS-4160-A"], "solid generator/UAT feed to A bus")
    + chain(["DG-1A", "CB-DGA", "BUS-4160-A"], "solid diesel generator A feed")
    + chain(["DG-1B", "CB-DGB", "BUS-4160-B"], "solid diesel generator B feed")
    + chain(["BUS-4160-A", "CB-TIE-AB", "BUS-4160-B"], "solid bus tie between 4.16 kV buses")
)

A_BUS_BREAKER_EDGES = [
    edge("BUS-4160-A", f"CB-A{index:02d}", "solid tap from BUS-4160-A to breaker")
    for index in range(1, 10)
]
B_BUS_BREAKER_EDGES = [
    edge("BUS-4160-B", f"CB-B{index:02d}", "solid tap from BUS-4160-B to breaker")
    for index in range(1, 10)
]

A_BREAKER_LOAD_EDGES = [
    edge("CB-A01", "TR-480-A1", "solid breaker load conductor"),
    edge("CB-A02", "TR-480-A2", "solid breaker load conductor"),
    edge("CB-A03", "PUMP-RHR-A", "solid breaker load conductor"),
    edge("CB-A04", "PUMP-CS-A", "solid breaker load conductor"),
    edge("CB-A05", "PUMP-AFW-A", "solid breaker load conductor"),
    edge("CB-A06", "TR-UPS-A", "solid breaker load conductor"),
    edge("CB-A07", "CHLR-A", "solid breaker load conductor"),
    edge("CB-A08", "FAN-CR-A", "solid breaker load conductor"),
]

B_BREAKER_LOAD_EDGES = [
    edge("CB-B01", "TR-480-B1", "solid breaker load conductor"),
    edge("CB-B02", "TR-480-B2", "solid breaker load conductor"),
    edge("CB-B03", "PUMP-RHR-B", "solid breaker load conductor"),
    edge("CB-B04", "PUMP-CS-B", "solid breaker load conductor"),
    edge("CB-B05", "PUMP-AFW-B", "solid breaker load conductor"),
    edge("CB-B06", "TR-UPS-B", "solid breaker load conductor"),
    edge("CB-B07", "CHLR-B", "solid breaker load conductor"),
    edge("CB-B08", "FAN-CR-B", "solid breaker load conductor"),
]

A_DIRECT_TR_LC_EDGES = [
    edge("TR-480-A1", "LC-101A", "direct solid 480 V transformer-to-load-center feed"),
    edge("TR-480-A2", "LC-102A", "direct solid 480 V transformer-to-load-center feed"),
]

B_DIRECT_TR_LC_EDGES = [
    edge("TR-480-B1", "LC-101B", "direct solid 480 V transformer-to-load-center feed"),
    edge("TR-480-B2", "LC-102B", "direct solid 480 V transformer-to-load-center feed"),
]

A_FEEDER_HELPER_EDGES = [
    edge("TR-480-A1", "480V LC FEEDERS-A", "Diego round 1 interpreted feeder label as logical node"),
    edge("TR-480-A2", "480V LC FEEDERS-A", "Diego round 1 interpreted feeder label as logical node"),
    edge("480V LC FEEDERS-A", "LC-101A", "Diego round 1 interpreted feeder label as logical node"),
    edge("480V LC FEEDERS-A", "LC-102A", "Diego round 1 interpreted feeder label as logical node"),
]

B_FEEDER_HELPER_EDGES = [
    edge("TR-480-B1", "480V LC FEEDERS-B", "Diego round 1 interpreted feeder label as logical node"),
    edge("TR-480-B2", "480V LC FEEDERS-B", "Diego round 1 interpreted feeder label as logical node"),
    edge("480V LC FEEDERS-B", "LC-101B", "Diego round 1 interpreted feeder label as logical node"),
    edge("480V LC FEEDERS-B", "LC-102B", "Diego round 1 interpreted feeder label as logical node"),
]

A_LOWER_EDGES = [
    edge("LC-101A", "DS-A01", "solid load center branch"),
    edge("DS-A01", "MCC-101A", "solid disconnect-to-MCC branch"),
    edge("MCC-101A", "MOV-101A", "solid MCC load branch"),
    edge("MCC-101A", "MOV-102A", "solid MCC load branch"),
    edge("MCC-101A", "JB-101A", "dashed/control connection to junction box"),
    edge("JB-101A", "AOV-101A", "control connection from junction box to AOV"),
    edge("LC-102A", "DS-A02", "solid load center branch"),
    edge("DS-A02", "MCC-102A", "solid disconnect-to-MCC branch"),
    edge("LC-102A", "MCC-103A", "solid load center branch"),
    edge("MCC-102A", "AOV-101A", "solid/control load branch to AOV"),
    edge("MCC-102A", "PUMP-CCW-A", "solid MCC load branch"),
    edge("MCC-103A", "FAN-AB-A", "solid MCC load branch"),
    edge("FAN-AB-A", "HTR-TRACE-A", "solid continuation to heat trace"),
]

B_LOWER_EDGES = [
    edge("LC-101B", "DS-B01", "solid load center branch"),
    edge("DS-B01", "MCC-101B", "solid disconnect-to-MCC branch"),
    edge("MCC-101B", "MOV-101B", "solid MCC load branch"),
    edge("MCC-101B", "MOV-102B", "solid MCC load branch"),
    edge("MCC-101B", "JB-101B", "dashed/control connection to junction box"),
    edge("JB-101B", "AOV-101B", "control connection from junction box to AOV"),
    edge("LC-102B", "DS-B02", "solid load center branch"),
    edge("DS-B02", "MCC-102B", "solid disconnect-to-MCC branch"),
    edge("LC-102B", "MCC-103B", "solid load center branch"),
    edge("MCC-102B", "AOV-101B", "solid/control load branch to AOV"),
    edge("MCC-102B", "PUMP-CCW-B", "solid MCC load branch"),
    edge("MCC-103B", "FAN-AB-B", "solid MCC load branch"),
    edge("FAN-AB-B", "HTR-TRACE-B", "solid continuation to heat trace"),
]

A_LOWER_EDGES_DIEGO_R1 = [item for item in A_LOWER_EDGES if edge_key(item.source, item.target) != edge_key("MCC-101A", "JB-101A")]
B_LOWER_EDGES_DIEGO_R1 = [item for item in B_LOWER_EDGES if edge_key(item.source, item.target) != edge_key("MCC-101B", "JB-101B")]

A_DC_UPS_EDGES = [
    edge("RECT-1A", "BCHG-1A", "solid DC/UPS train A rectifier-to-charger conductor"),
    edge("BCHG-1A", "BAT-1A", "solid DC/UPS train A charger-to-battery conductor"),
    edge("BCHG-1A", "BUS-DC-A", "separate upper conductor from charger to DC bus junction"),
    edge("BAT-1A", "BUS-DC-A", "solid battery-to-DC bus conductor"),
    edge("BUS-DC-A", "INV-1A", "solid DC bus to inverter conductor"),
    edge("INV-1A", "BUS-UPS-A", "solid inverter to UPS bus conductor"),
    edge("BUS-UPS-A", "PNL-UPS-A", "solid UPS bus to UPS panel conductor"),
]

B_DC_UPS_EDGES = [
    edge("RECT-1B", "BCHG-1B", "solid DC/UPS train B rectifier-to-charger conductor"),
    edge("BCHG-1B", "BAT-1B", "solid DC/UPS train B charger-to-battery conductor"),
    edge("BCHG-1B", "BUS-DC-B", "separate upper conductor from charger to DC bus junction"),
    edge("BAT-1B", "BUS-DC-B", "solid battery-to-DC bus conductor"),
    edge("BUS-DC-B", "INV-1B", "solid DC bus to inverter conductor"),
    edge("INV-1B", "BUS-UPS-B", "solid inverter to UPS bus conductor"),
    edge("BUS-UPS-B", "PNL-UPS-B", "solid UPS bus to UPS panel conductor"),
]

A_PROTECTION_EDGES = [
    edge("TB-SWGR-A", "RLY-27A", "dashed TB-SWGR-A to relay path"),
    edge("TB-SWGR-A", "RLY-50A", "dashed TB-SWGR-A to relay path"),
    edge("TB-SWGR-A", "RLY-86A", "dashed TB-SWGR-A to relay path"),
    edge("PT-4160-A", "RLY-27A", "dotted PT-to-undervoltage relay path"),
    edge("CT-4160-A", "RLY-50A", "dotted CT-to-overcurrent relay path"),
]

B_PROTECTION_EDGES = [
    edge("TB-SWGR-B", "RLY-27B", "dashed TB-SWGR-B to relay path"),
    edge("TB-SWGR-B", "RLY-50B", "dashed TB-SWGR-B to relay path"),
    edge("TB-SWGR-B", "RLY-86B", "dashed TB-SWGR-B to relay path"),
    edge("PT-4160-B", "RLY-27B", "dotted PT-to-undervoltage relay path"),
    edge("CT-4160-B", "RLY-50B", "dotted CT-to-overcurrent relay path"),
]

A_PROTECTION_DIEGO_R1_EXTRA = [
    edge("CT-CAB-A", "TB-SWGR-A", "Diego round 1 treated cable-tray label as a logical node"),
    edge("CT-4160-A", "RLY-86A", "Diego round 1 high-recall possible CT lockout relay path"),
]

B_PROTECTION_DIEGO_R1_EXTRA = [
    edge("CT-CAB-B", "TB-SWGR-B", "Diego round 1 treated cable-tray label as a logical node"),
    edge("CT-4160-B", "RLY-86B", "Diego round 1 high-recall possible CT lockout relay path"),
]

MCR_FINAL_EDGES = [
    edge("PNL-MCR-01", "JB-CONTROL", "dashed MCR panel to control junction box"),
    edge("PNL-ANN-01", "JB-CONTROL", "dotted annunciator panel to control junction box"),
    edge("SER-01", "JB-CONTROL", "dotted/solid server/control route to junction box"),
]

MCR_DIEGO_R1_EDGES = [
    edge("CT-CAB-B", "PNL-MCR-01", "Diego round 1 high-recall cable-tray-to-MCR candidate"),
    edge("CT-CAB-B", "JB-CONTROL", "Diego round 1 high-recall cable-tray-to-control-JB candidate"),
    edge("PNL-ANN-01", "JB-CONTROL", "visible annunciator panel to control junction box"),
    edge("SER-01", "JB-CONTROL", "visible server/control route to junction box"),
]

FINAL_EDGES = dedupe_edges(
    SOURCE_EDGES
    + A_BUS_BREAKER_EDGES
    + B_BUS_BREAKER_EDGES
    + A_BREAKER_LOAD_EDGES
    + B_BREAKER_LOAD_EDGES
    + A_DIRECT_TR_LC_EDGES
    + B_DIRECT_TR_LC_EDGES
    + A_LOWER_EDGES
    + B_LOWER_EDGES
    + A_DC_UPS_EDGES
    + B_DC_UPS_EDGES
    + A_PROTECTION_EDGES
    + B_PROTECTION_EDGES
    + MCR_FINAL_EDGES
)

DIEGO_R1_EDGES = dedupe_edges(
    SOURCE_EDGES
    + A_BUS_BREAKER_EDGES
    + B_BUS_BREAKER_EDGES
    + A_BREAKER_LOAD_EDGES
    + B_BREAKER_LOAD_EDGES
    + A_FEEDER_HELPER_EDGES
    + B_FEEDER_HELPER_EDGES
    + A_LOWER_EDGES_DIEGO_R1
    + B_LOWER_EDGES_DIEGO_R1
    + A_DC_UPS_EDGES
    + B_DC_UPS_EDGES
    + A_PROTECTION_EDGES
    + B_PROTECTION_EDGES
    + A_PROTECTION_DIEGO_R1_EXTRA
    + B_PROTECTION_DIEGO_R1_EXTRA
    + MCR_DIEGO_R1_EDGES
)

DIEGO_R1_UNCERTAIN = [
    edge("MCC-101A", "JB-101A", "junction-box endpoint visible but not promoted until precision review", "uncertain_included"),
    edge("MCC-101B", "JB-101B", "junction-box endpoint visible but not promoted until precision review", "uncertain_included"),
    edge("PNL-RPS-A", "FUSE-A01", "nearby panel-to-fuse solid strokes were visually plausible but endpoint-cleanliness was uncertain", "uncertain_included"),
    edge("PNL-ESFAS-A", "FUSE-A02", "nearby panel-to-fuse solid strokes were visually plausible but endpoint-cleanliness was uncertain", "uncertain_included"),
    edge("PNL-RPS-B", "FUSE-B01", "nearby panel-to-fuse solid strokes were visually plausible but endpoint-cleanliness was uncertain", "uncertain_included"),
    edge("PNL-ESFAS-B", "FUSE-B02", "nearby panel-to-fuse solid strokes were visually plausible but endpoint-cleanliness was uncertain", "uncertain_included"),
    edge("BUS-DC-A", "GND-A", "ground route visible in the area but endpoint was not clean enough", "uncertain_included"),
    edge("BUS-DC-B", "GND-B", "ground route visible in the area but endpoint was not clean enough", "uncertain_included"),
    edge("CB-A09", "unresolved downstream A load", "CB-A09 has a bus tap but no clean named downstream endpoint", "uncertain_excluded"),
    edge("CB-B09", "unresolved downstream B load", "CB-B09 has a bus tap but no clean named downstream endpoint", "uncertain_excluded"),
]

FINAL_UNCERTAIN = [
    edge("CT-CAB-A", "TB-SWGR-A", "CT-CAB-A is a cable-tray/location label, not a component node", "uncertain_excluded"),
    edge("CT-CAB-B", "TB-SWGR-B", "CT-CAB-B is a cable-tray/location label, not a component node", "uncertain_excluded"),
    edge("TR-480-A1", "480V LC FEEDERS-A", "480V LC FEEDERS-A is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("TR-480-A2", "480V LC FEEDERS-A", "480V LC FEEDERS-A is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("480V LC FEEDERS-A", "LC-101A", "480V LC FEEDERS-A is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("480V LC FEEDERS-A", "LC-102A", "480V LC FEEDERS-A is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("TR-480-B1", "480V LC FEEDERS-B", "480V LC FEEDERS-B is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("TR-480-B2", "480V LC FEEDERS-B", "480V LC FEEDERS-B is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("480V LC FEEDERS-B", "LC-101B", "480V LC FEEDERS-B is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("480V LC FEEDERS-B", "LC-102B", "480V LC FEEDERS-B is a feeder label replaced by direct TR-to-LC edges", "uncertain_excluded"),
    edge("CT-4160-A", "RLY-86A", "nearby dotted/control linework does not cleanly terminate at RLY-86A", "uncertain_excluded"),
    edge("CT-4160-B", "RLY-86B", "nearby dotted/control linework does not cleanly terminate at RLY-86B", "uncertain_excluded"),
    edge("CT-CAB-B", "PNL-MCR-01", "MCR route enters the bay, but CT-CAB-B was removed as a non-component label", "uncertain_excluded"),
    edge("CT-CAB-B", "JB-CONTROL", "MCR route enters the bay, but CT-CAB-B was removed as a non-component label", "uncertain_excluded"),
    edge("PNL-RPS-A", "FUSE-A01", "fuse area has overlapping solid/dotted routes; endpoint pair is not precision-clean", "uncertain_excluded"),
    edge("PNL-ESFAS-A", "FUSE-A02", "fuse area has overlapping solid/dotted routes; endpoint pair is not precision-clean", "uncertain_excluded"),
    edge("PNL-RPS-B", "FUSE-B01", "fuse area has overlapping solid/dotted routes; endpoint pair is not precision-clean", "uncertain_excluded"),
    edge("PNL-ESFAS-B", "FUSE-B02", "fuse area has overlapping solid/dotted routes; endpoint pair is not precision-clean", "uncertain_excluded"),
    edge("BUS-DC-A", "GND-A", "ground symbol is visible but endpoint is not clean enough to assert", "uncertain_excluded"),
    edge("BUS-DC-B", "GND-B", "ground symbol is visible but endpoint is not clean enough to assert", "uncertain_excluded"),
    edge("CB-A09", "unresolved downstream A load", "CB-A09 has a bus tap but no clean named downstream endpoint", "uncertain_excluded"),
    edge("CB-B09", "unresolved downstream B load", "CB-B09 has a bus tap but no clean named downstream endpoint", "uncertain_excluded"),
]

ROUNDS = [
    RoundSpec(
        "round_01",
        "diego",
        "high_recall_extractor",
        DIEGO_R1_NODES,
        DIEGO_R1_EDGES,
        DIEGO_R1_UNCERTAIN,
        True,
        [
            "High-recall extraction from the raw PNG and crops generated from that PNG.",
            "Included helper/location labels and plausible fuse/ground candidates to avoid false negatives.",
            "Flagged CB-A09/CB-B09 downstream endpoints as unresolved rather than inventing names.",
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
            "Removed cable-tray, feeder-label, and bay-label helper nodes.",
            "Replaced feeder-label paths with direct transformer-to-load-center edges.",
            "Added MCC-101A/B to JB-101A/B and retained JB-to-AOV links.",
            "Kept fuse and ground nodes visible but isolated/uncertain to avoid overconnecting.",
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
            "Diego accepted Jennifer's precision removals and direct transformer-to-LC replacements.",
            "Confirmed fuses should remain visible nodes with no confirmed endpoint edges.",
            "Confirmed BCHG-to-BAT, BCHG-to-BUS-DC, and BAT-to-BUS-DC all remain in the DC/UPS graph.",
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
            "Final precision pass confirmed the direct charger-to-DC-bus branch in both trains.",
            "Saturation/agreement reached with Diego after two rounds.",
            "Final graph uses only visually supported named endpoints from the raw schematic and derived crops.",
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
            "timestamp_local",
            "round_id",
            "actor",
            "role",
            "node_count",
            "edge_count",
            "uncertain_item_count",
            "subagent_runtime_id",
            "token_telemetry",
            "artifact_prefix",
        ])
        runtime_ids = {
            "diego": "019f5f70-30c6-7362-b527-0693415eff21",
            "jennifer": "019f5f74-7d4b-7c02-9daf-c7fefc428062",
        }
        for spec, metrics, prefix in zip(ROUNDS, metrics_rows, prefixes):
            writer.writerow([
                now,
                spec.round_id,
                spec.actor,
                spec.role,
                metrics["node_count"],
                metrics["edge_count"],
                metrics["uncertain_item_count"],
                runtime_ids["diego" if spec.actor == "diego" else "jennifer"],
                "not available from current runtime telemetry",
                prefix,
            ])

    notes = [
        "# Token Performance Notes",
        "",
        "- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and marks token telemetry unavailable.",
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
        "Case: 10 Raw",
        "",
        "Evidence used:",
        "- Raw schematic PNG in the Raw folder.",
        "- Crops generated from that same PNG and stored under results/crops.",
        "- No Ground Truth or GT-derived feedback/resources were used.",
        "",
        "Final consensus:",
        "- Diego and Jennifer agreed after two rounds.",
        f"- Final node count is {len(FINAL_NODES)} visible component/node labels.",
        f"- Final confirmed edge count is {len(FINAL_EDGES)}.",
        "- Helper labels CT-CAB-A/B, 480V LC FEEDERS-A/B, and MCR / ANNUNCIATOR CONTROL BAY were excluded as graph nodes.",
        "- FUSE-A01/A02/B01/B02 and GND-A/B remain visible nodes but have no confirmed edges.",
        "- BCHG-1A/B have confirmed direct edges to both BAT-1A/B and BUS-DC-A/B.",
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
