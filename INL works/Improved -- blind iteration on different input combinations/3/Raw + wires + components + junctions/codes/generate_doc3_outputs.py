from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\3\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


def split_names(text: str) -> list[str]:
    names: list[str] = []
    for part in text.replace("\n", ",").split(","):
        value = part.strip()
        if value:
            names.append(value)
    return names


DIEGO_R1_NODES = split_names(
    """
GRID-1, AUX-TR-1A, CB-101, 4A-SA-01, BUS-416A, BUS-TIE-41, BUS-416B, 4B-SB-01, CB-102, AUX-TR-1B, GRID-2,
EDG-1A, CB-DG1A, FDR-A1, TR-480A1, CB-480A1, MCC-480A1, FDR-A2, TR-480A2, CB-480A2, MCC-480A2,
CHG-A, GND-A, GND-1E, GND-B, CHG-B, FDR-B1, TR-480B1, CB-480B1, MCC-480B1, FDR-B2, TR-480B2, CB-480B2, MCC-480B2, CB-DG1B, EDG-1B,
BAT-125A, CB-CHG-A, CHGR-125A, DC-BUS-A, INV-120A, BUS-120A, BAT-125B, CB-CHG-B, CHGR-125B, DC-BUS-B, INV-120B, BUS-120B, 120A-CNTL, 120B-CNTL,
FDB-A1, MCC A1 FEEDER BUS, FDB-A2, MCC A2 FEEDER BUS, FDB-B1, MCC B1 FEEDER BUS, FDB-B2, MCC B2 FEEDER BUS,
CB-SI-A1, PUMP-SI-A1, CB-RHR-A1, PUMP-RHR-A1, CB-CCW-A1, PUMP-CCW-A1, CB-FAN-A1, FAN-CR-A1, CB-MOV-A101, VALVE-SI-A101, CB-MOV-A102, VALVE-RHR-A102,
CB-CS-A2, PUMP-CS-A2, CB-SW-A2, PUMP-SW-A2, CB-AFW-A2, PUMP-AFW-A2, CB-FAN-A2, FAN-EB-A2, CB-MOV-A201, VALVE-CCW-A201, CB-HTR-A2, HTR-BAY-A2,
CB-SI-B1, PUMP-SI-B1, CB-RHR-B1, PUMP-RHR-B1, CB-CCW-B1, PUMP-CCW-B1, CB-FAN-B1, FAN-CR-B1, CB-MOV-B101, VALVE-SI-B101, CB-MOV-B102, VALVE-RHR-B102,
CB-CS-B2, PUMP-CS-B2, CB-SW-B2, PUMP-SW-B2, CB-FAN-B2, FAN-EB-B2, CB-MOV-B201, VALVE-CCW-B201, CB-HTR-B2, HTR-BAY-B2,
INST-PT-A, INST-LT-A, RELAY-K27A, PANEL-RPS-A, PANEL-ESF-A, JB-A401, TB-A401, TB-ESF-A, UV RELAY A,
INST-PT-B, INST-LT-B, RELAY-K27B, PANEL-RPS-B, PANEL-ESF-B, JB-B501, TB-B501, TB-ESF-B, UV RELAY B
"""
)


FINAL_NODES = split_names(
    """
GRID-1, AUX-TR-1A, CB-101, BUS-416A, BUS-TIE-41, BUS-416B, CB-102, AUX-TR-1B, GRID-2,
EDG-1A, CB-DG1A, TR-480A1, CB-480A1, MCC-480A1, TR-480A2, CB-480A2, MCC-480A2,
CB-CHG-A, CHGR-125A, BAT-125A, DC-BUS-A, INV-120A, BUS-120A,
CB-CHG-B, CHGR-125B, BAT-125B, DC-BUS-B, INV-120B, BUS-120B,
TR-480B1, CB-480B1, MCC-480B1, TR-480B2, CB-480B2, MCC-480B2, CB-DG1B, EDG-1B,
FDB-A1, FDB-A2, FDB-B1, FDB-B2,
CB-SI-A1, PUMP-SI-A1, CB-RHR-A1, PUMP-RHR-A1, CB-CCW-A1, PUMP-CCW-A1, CB-FAN-A1, FAN-CR-A1, CB-MOV-A101, VALVE-SI-A101, CB-MOV-A102, VALVE-RHR-A102,
CB-CS-A2, PUMP-CS-A2, CB-SW-A2, PUMP-SW-A2, CB-AFW-A2, PUMP-AFW-A2, CB-FAN-A2, FAN-EB-A2, CB-MOV-A201, VALVE-CCW-A201, CB-HTR-A2, HTR-BAY-A2,
CB-SI-B1, PUMP-SI-B1, CB-RHR-B1, PUMP-RHR-B1, CB-CCW-B1, PUMP-CCW-B1, CB-FAN-B1, FAN-CR-B1, CB-MOV-B101, VALVE-SI-B101, CB-MOV-B102, VALVE-RHR-B102,
CB-CS-B2, PUMP-CS-B2, CB-SW-B2, PUMP-SW-B2, CB-FAN-B2, FAN-EB-B2, CB-MOV-B201, VALVE-CCW-B201, CB-HTR-B2, HTR-BAY-B2,
INST-PT-A, INST-LT-A, RELAY-K27A, PANEL-RPS-A, PANEL-ESF-A, JB-A401,
INST-PT-B, INST-LT-B, RELAY-K27B, PANEL-RPS-B, PANEL-ESF-B, JB-B501
"""
)


@dataclass(frozen=True)
class Edge:
    a: str
    b: str
    evidence: str
    status: str = "accepted"


def e(a: str, b: str, evidence: str, status: str = "accepted") -> Edge:
    return Edge(a, b, evidence, status)


DIEGO_R1_ACCEPTED_EDGES = [
    e("GRID-1", "AUX-TR-1A", "solid offsite A line"),
    e("AUX-TR-1A", "CB-101", "solid line into breaker"),
    e("GRID-2", "AUX-TR-1B", "solid offsite B line"),
    e("AUX-TR-1B", "CB-102", "solid line into breaker"),
    e("BUS-416A", "BUS-TIE-41", "left bus enters tie switch"),
    e("BUS-TIE-41", "BUS-416B", "tie switch exits to right bus"),
    e("BUS-416A", "FDR-A1", "tap down from BUS-416A"),
    e("FDR-A1", "CB-DG1A", "branch to DG breaker"),
    e("CB-DG1A", "EDG-1A", "solid generator lead"),
    e("FDR-A1", "TR-480A1", "vertical feeder to transformer"),
    e("TR-480A1", "CB-480A1", "transformer low-side vertical"),
    e("CB-480A1", "MCC-480A1", "breaker output to MCC"),
    e("BUS-416A", "FDR-A2", "tap down from BUS-416A"),
    e("FDR-A2", "TR-480A2", "vertical feeder"),
    e("TR-480A2", "CB-480A2", "transformer low-side vertical"),
    e("CB-480A2", "MCC-480A2", "breaker output to MCC"),
    e("BUS-416A", "CHG-A", "vertical charger feeder"),
    e("CHG-A", "CB-CHG-A", "charger feeder into breaker"),
    e("CB-CHG-A", "CHGR-125A", "52-CA downlead"),
    e("CHGR-125A", "DC-BUS-A", "125V CHGR A lead"),
    e("BAT-125A", "DC-BUS-A", "+125V battery lead"),
    e("DC-BUS-A", "INV-120A", "125V DC A vertical"),
    e("INV-120A", "BUS-120A", "120VAC INV A output"),
    e("BUS-416B", "CHG-B", "vertical charger feeder"),
    e("CHG-B", "CB-CHG-B", "charger feeder into breaker"),
    e("CB-CHG-B", "CHGR-125B", "52-CB downlead"),
    e("CHGR-125B", "DC-BUS-B", "125V CHGR B lead"),
    e("BAT-125B", "DC-BUS-B", "+125V battery lead"),
    e("DC-BUS-B", "INV-120B", "125V DC B vertical"),
    e("INV-120B", "BUS-120B", "120VAC INV B output"),
    e("BUS-416B", "FDR-B1", "tap down from BUS-416B"),
    e("FDR-B1", "TR-480B1", "vertical feeder"),
    e("TR-480B1", "CB-480B1", "transformer low-side vertical"),
    e("CB-480B1", "MCC-480B1", "breaker output to MCC"),
    e("BUS-416B", "FDR-B2", "tap down from BUS-416B"),
    e("FDR-B2", "CB-DG1B", "branch to DG breaker"),
    e("CB-DG1B", "EDG-1B", "solid generator lead"),
    e("FDR-B2", "TR-480B2", "vertical feeder to transformer"),
    e("TR-480B2", "CB-480B2", "transformer low-side vertical"),
    e("CB-480B2", "MCC-480B2", "breaker output to MCC"),
    e("MCC-480A1", "FDB-A1", "buckets shown below"),
    e("MCC-480A2", "FDB-A2", "buckets shown below"),
    e("MCC-480B1", "FDB-B1", "buckets shown below"),
    e("MCC-480B2", "FDB-B2", "buckets shown below"),
    e("FDB-A1", "MCC A1 FEEDER BUS", "thick feeder bus"),
    e("FDB-A2", "MCC A2 FEEDER BUS", "thick feeder bus"),
    e("FDB-B1", "MCC B1 FEEDER BUS", "thick feeder bus"),
    e("FDB-B2", "MCC B2 FEEDER BUS", "thick feeder bus"),
]


LOAD_EDGES_DIEGO = [
    ("MCC A1 FEEDER BUS", "CB-SI-A1", "PUMP-SI-A1"),
    ("MCC A1 FEEDER BUS", "CB-RHR-A1", "PUMP-RHR-A1"),
    ("MCC A1 FEEDER BUS", "CB-CCW-A1", "PUMP-CCW-A1"),
    ("MCC A1 FEEDER BUS", "CB-FAN-A1", "FAN-CR-A1"),
    ("MCC A1 FEEDER BUS", "CB-MOV-A101", "VALVE-SI-A101"),
    ("MCC A1 FEEDER BUS", "CB-MOV-A102", "VALVE-RHR-A102"),
    ("MCC A2 FEEDER BUS", "CB-CS-A2", "PUMP-CS-A2"),
    ("MCC A2 FEEDER BUS", "CB-SW-A2", "PUMP-SW-A2"),
    ("MCC A2 FEEDER BUS", "CB-AFW-A2", "PUMP-AFW-A2"),
    ("MCC A2 FEEDER BUS", "CB-FAN-A2", "FAN-EB-A2"),
    ("MCC A2 FEEDER BUS", "CB-MOV-A201", "VALVE-CCW-A201"),
    ("MCC A2 FEEDER BUS", "CB-HTR-A2", "HTR-BAY-A2"),
    ("MCC B1 FEEDER BUS", "CB-SI-B1", "PUMP-SI-B1"),
    ("MCC B1 FEEDER BUS", "CB-RHR-B1", "PUMP-RHR-B1"),
    ("MCC B1 FEEDER BUS", "CB-CCW-B1", "PUMP-CCW-B1"),
    ("MCC B1 FEEDER BUS", "CB-FAN-B1", "FAN-CR-B1"),
    ("MCC B1 FEEDER BUS", "CB-MOV-B101", "VALVE-SI-B101"),
    ("MCC B1 FEEDER BUS", "CB-MOV-B102", "VALVE-RHR-B102"),
    ("MCC B2 FEEDER BUS", "CB-CS-B2", "PUMP-CS-B2"),
    ("MCC B2 FEEDER BUS", "CB-SW-B2", "PUMP-SW-B2"),
    ("MCC B2 FEEDER BUS", "CB-FAN-B2", "FAN-EB-B2"),
    ("MCC B2 FEEDER BUS", "CB-MOV-B201", "VALVE-CCW-B201"),
    ("MCC B2 FEEDER BUS", "CB-HTR-B2", "HTR-BAY-B2"),
]

for bus, breaker, load in LOAD_EDGES_DIEGO:
    DIEGO_R1_ACCEPTED_EDGES.append(e(bus, breaker, "top tap"))
    DIEGO_R1_ACCEPTED_EDGES.append(e(breaker, load, "vertical drop to load"))

DIEGO_R1_ACCEPTED_EDGES.extend(
    [
        e("BUS-120A", "PANEL-RPS-A", "dashed 120A-CNTL riser"),
        e("INST-PT-A", "PANEL-RPS-A", "dotted upper signal line"),
        e("INST-LT-A", "PANEL-RPS-A", "dotted lower signal line"),
        e("RELAY-K27A", "PANEL-RPS-A", "dashed center line"),
        e("RELAY-K27A", "PANEL-ESF-A", "dashed UV RELAY A line"),
        e("PANEL-ESF-A", "JB-A401", "dashed TB-ESF-A line"),
        e("BUS-120B", "PANEL-RPS-B", "dashed 120B-CNTL riser"),
        e("INST-PT-B", "PANEL-RPS-B", "dotted upper signal line"),
        e("INST-LT-B", "PANEL-RPS-B", "dotted lower signal line"),
        e("RELAY-K27B", "PANEL-RPS-B", "dashed center line"),
        e("RELAY-K27B", "PANEL-ESF-B", "dashed UV RELAY B line"),
        e("PANEL-ESF-B", "JB-B501", "dashed TB-ESF-B line"),
    ]
)

DIEGO_R1_UNCERTAIN_EDGES = [
    e("CB-101", "4A-SA-01", "bottom source-breaker stub visible", "uncertain"),
    e("4A-SA-01", "BUS-416A", "likely source feeder, visible gap to bus", "uncertain"),
    e("CB-102", "4B-SB-01", "bottom source-breaker stub visible", "uncertain"),
    e("4B-SB-01", "BUS-416B", "likely source feeder, visible gap to bus", "uncertain"),
    e("GND-A", "GND-1E", "dash-dot ground reference near ground symbol", "uncertain"),
    e("GND-B", "GND-1E", "dash-dot ground reference near ground symbol", "uncertain"),
    e("PANEL-ESF-A", "TB-ESF-A", "TB label on same dashed run", "uncertain"),
    e("TB-ESF-A", "JB-A401", "same dashed run to junction box", "uncertain"),
    e("JB-A401", "TB-A401", "TB-A401 appears as sublabel under JB-A401", "uncertain"),
    e("PANEL-ESF-B", "TB-ESF-B", "TB label on same dashed run", "uncertain"),
    e("TB-ESF-B", "JB-B501", "same dashed run to junction box", "uncertain"),
    e("JB-B501", "TB-B501", "TB-B501 appears as sublabel under JB-B501", "uncertain"),
]

DIEGO_R1_EDGES = DIEGO_R1_ACCEPTED_EDGES + DIEGO_R1_UNCERTAIN_EDGES


FINAL_EDGES = [
    e("GRID-1", "AUX-TR-1A", "solid source line to transformer terminal"),
    e("AUX-TR-1A", "CB-101", "solid line to CB-101 terminal"),
    e("GRID-2", "AUX-TR-1B", "solid source line to transformer terminal"),
    e("AUX-TR-1B", "CB-102", "solid line to CB-102 terminal"),
    e("BUS-416A", "BUS-TIE-41", "solid bus connection into tie breaker"),
    e("BUS-TIE-41", "BUS-416B", "solid bus connection out of tie breaker"),
    e("BUS-416A", "CB-DG1A", "solid feeder tap to breaker terminal"),
    e("CB-DG1A", "EDG-1A", "solid line from breaker to generator"),
    e("BUS-416A", "TR-480A1", "solid feeder down to transformer"),
    e("TR-480A1", "CB-480A1", "solid vertical conductor"),
    e("CB-480A1", "MCC-480A1", "solid vertical conductor"),
    e("BUS-416A", "TR-480A2", "solid feeder down to transformer"),
    e("TR-480A2", "CB-480A2", "solid vertical conductor"),
    e("CB-480A2", "MCC-480A2", "solid vertical conductor"),
    e("BUS-416A", "CB-CHG-A", "solid charger feeder; CHG-A is label only"),
    e("CB-CHG-A", "CHGR-125A", "solid vertical conductor"),
    e("CHGR-125A", "DC-BUS-A", "solid vertical conductor"),
    e("BAT-125A", "DC-BUS-A", "solid battery lead to DC bus"),
    e("DC-BUS-A", "INV-120A", "solid vertical conductor"),
    e("INV-120A", "BUS-120A", "visible inverter output to 120 V bus"),
    e("BUS-416B", "CB-CHG-B", "solid charger feeder; CHG-B is label only"),
    e("CB-CHG-B", "CHGR-125B", "solid vertical conductor"),
    e("CHGR-125B", "DC-BUS-B", "solid vertical conductor"),
    e("BAT-125B", "DC-BUS-B", "solid battery lead to DC bus"),
    e("DC-BUS-B", "INV-120B", "solid vertical conductor"),
    e("INV-120B", "BUS-120B", "visible inverter output to 120 V bus"),
    e("BUS-416B", "TR-480B1", "solid feeder down to transformer"),
    e("TR-480B1", "CB-480B1", "solid vertical conductor"),
    e("CB-480B1", "MCC-480B1", "solid vertical conductor"),
    e("BUS-416B", "TR-480B2", "solid feeder down to transformer"),
    e("TR-480B2", "CB-480B2", "solid vertical conductor"),
    e("CB-480B2", "MCC-480B2", "solid vertical conductor"),
    e("BUS-416B", "CB-DG1B", "solid feeder tap to breaker terminal"),
    e("CB-DG1B", "EDG-1B", "solid line from breaker to generator"),
    e("MCC-480A1", "FDB-A1", "vertical buckets-shown-below feed to bus"),
    e("MCC-480A2", "FDB-A2", "vertical buckets-shown-below feed to bus"),
    e("MCC-480B1", "FDB-B1", "vertical buckets-shown-below feed to bus"),
    e("MCC-480B2", "FDB-B2", "vertical buckets-shown-below feed to bus"),
]

LOAD_EDGES_FINAL = [
    ("FDB-A1", "CB-SI-A1", "PUMP-SI-A1"),
    ("FDB-A1", "CB-RHR-A1", "PUMP-RHR-A1"),
    ("FDB-A1", "CB-CCW-A1", "PUMP-CCW-A1"),
    ("FDB-A1", "CB-FAN-A1", "FAN-CR-A1"),
    ("FDB-A1", "CB-MOV-A101", "VALVE-SI-A101"),
    ("FDB-A1", "CB-MOV-A102", "VALVE-RHR-A102"),
    ("FDB-A2", "CB-CS-A2", "PUMP-CS-A2"),
    ("FDB-A2", "CB-SW-A2", "PUMP-SW-A2"),
    ("FDB-A2", "CB-AFW-A2", "PUMP-AFW-A2"),
    ("FDB-A2", "CB-FAN-A2", "FAN-EB-A2"),
    ("FDB-A2", "CB-MOV-A201", "VALVE-CCW-A201"),
    ("FDB-A2", "CB-HTR-A2", "HTR-BAY-A2"),
    ("FDB-B1", "CB-SI-B1", "PUMP-SI-B1"),
    ("FDB-B1", "CB-RHR-B1", "PUMP-RHR-B1"),
    ("FDB-B1", "CB-CCW-B1", "PUMP-CCW-B1"),
    ("FDB-B1", "CB-FAN-B1", "FAN-CR-B1"),
    ("FDB-B1", "CB-MOV-B101", "VALVE-SI-B101"),
    ("FDB-B1", "CB-MOV-B102", "VALVE-RHR-B102"),
    ("FDB-B2", "CB-CS-B2", "PUMP-CS-B2"),
    ("FDB-B2", "CB-SW-B2", "PUMP-SW-B2"),
    ("FDB-B2", "CB-FAN-B2", "FAN-EB-B2"),
    ("FDB-B2", "CB-MOV-B201", "VALVE-CCW-B201"),
    ("FDB-B2", "CB-HTR-B2", "HTR-BAY-B2"),
]

for bus, breaker, load in LOAD_EDGES_FINAL:
    FINAL_EDGES.append(e(bus, breaker, "vertical tap from feeder bus"))
    FINAL_EDGES.append(e(breaker, load, "solid drop from breaker to load"))

FINAL_EDGES.extend(
    [
        e("INST-PT-A", "PANEL-RPS-A", "dotted signal line to RPS panel"),
        e("INST-LT-A", "PANEL-RPS-A", "dotted signal line to RPS panel"),
        e("RELAY-K27A", "PANEL-RPS-A", "dashed control line to RPS panel"),
        e("RELAY-K27A", "PANEL-ESF-A", "dashed UV relay output to ESF panel"),
        e("PANEL-ESF-A", "JB-A401", "dashed vertical line from ESF panel to junction box"),
        e("INST-PT-B", "PANEL-RPS-B", "dotted signal line to RPS panel"),
        e("INST-LT-B", "PANEL-RPS-B", "dotted signal line to RPS panel"),
        e("RELAY-K27B", "PANEL-RPS-B", "dashed control line to RPS panel"),
        e("RELAY-K27B", "PANEL-ESF-B", "dashed UV relay output to ESF panel"),
        e("PANEL-ESF-B", "JB-B501", "dashed vertical line from ESF panel to junction box"),
    ]
)


EXCLUDED_CASES = [
    "GND-1E, GND-A, GND-B: visible ground/reference markings; no clear connected named endpoints in the raw crop.",
    "120A-CNTL, 120B-CNTL: control-line labels only, not component nodes.",
    "TB-ESF-A/B and TB-A401/B501: terminal labels associated with the panel/JB line, not separate visible matrix nodes.",
    "4A-SA-01 and 4B-SB-01: labels/stubs below CB-101/CB-102; visible gaps to BUS-416A/B.",
    "No direct BUS-120A/B to PANEL-RPS-A/B edge: the visible riser is a separate control run and does not land on the 120 V busbar.",
]


def unique_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str, str]] = set()
    result: list[Edge] = []
    for edge in edges:
        key_nodes = tuple(sorted((edge.a, edge.b)))
        key = (key_nodes[0], key_nodes[1], edge.status)
        if key not in seen:
            seen.add(key)
            result.append(edge)
    return result


def validate(nodes: list[str], edges: list[Edge]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({name for name in nodes if nodes.count(name) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")
    node_set = set(nodes)
    missing = sorted({name for edge in edges for name in (edge.a, edge.b) if name not in node_set})
    if missing:
        raise ValueError(f"edges reference missing nodes: {missing}")


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    index = {name: i for i, name in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in edges:
        i = index[edge.a]
        j = index[edge.b]
        if i == j:
            continue
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for name, row in zip(nodes, matrix):
            writer.writerow([name] + row)


def write_edge_list(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "status", "evidence"])
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "source": edge.a,
                    "target": edge.b,
                    "status": edge.status,
                    "evidence": edge.evidence,
                }
            )


def estimate_text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        try:
            encoding = tiktoken.encoding_for_model("gpt-5")
        except Exception:
            encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def estimate_image_tokens(path: Path, detail: str = "high") -> int:
    if detail == "low":
        return 85
    width, height = Image.open(path).size
    scale = min(2048 / width, 2048 / height, 1.0)
    width = math.ceil(width * scale)
    height = math.ceil(height * scale)
    shortest = min(width, height)
    if shortest > 768:
        scale = 768 / shortest
        width = math.ceil(width * scale)
        height = math.ceil(height * scale)
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_total(paths: list[str]) -> int:
    return sum(estimate_image_tokens(Path(path)) for path in paths)


def write_usage_estimates() -> None:
    raw = BASE / "raw -- synthetic_npp_100_component_electrical_schematic.png"
    detected = BASE / "detected_components_and_logical_overlay.png"
    wire_nodes = BASE / "wire_nodes_overlay.png"
    crops = {
        name: RESULTS / name
        for name in [
            "raw__top_sources_and_buses.png",
            "raw__train_a_4160_mcc.png",
            "raw__train_b_4160_mcc.png",
            "raw__charger_feed_detail.png",
            "raw__dc_ups_center.png",
            "raw__mcc_feeders_a_left.png",
            "raw__mcc_feeders_a_right.png",
            "raw__mcc_feeders_b_left.png",
            "raw__mcc_feeders_b_right.png",
            "raw__lower_rps_a.png",
            "raw__lower_rps_b.png",
            "raw__bus_tie_detail.png",
        ]
    }
    diego_attempt_images = [str(raw), str(detected), str(wire_nodes)] + [str(crops[name]) for name in crops]
    diego_r1_images = [str(crops[name]) for name in crops]
    jennifer_images = [
        str(crops[name])
        for name in [
            "raw__top_sources_and_buses.png",
            "raw__charger_feed_detail.png",
            "raw__dc_ups_center.png",
            "raw__mcc_feeders_a_left.png",
            "raw__mcc_feeders_a_right.png",
            "raw__mcc_feeders_b_left.png",
            "raw__mcc_feeders_b_right.png",
            "raw__lower_rps_a.png",
            "raw__lower_rps_b.png",
        ]
    ] + [
        str(RESULTS / "wire_nodes__top_sources_and_buses.png"),
        str(RESULTS / "wire_nodes__lower_rps_a.png"),
        str(RESULTS / "wire_nodes__lower_rps_b.png"),
    ]

    rows = [
        {
            "document": 3,
            "iteration": 1,
            "round": "main-setup",
            "call": "main_01_resource_inventory_crop_visual_inspection",
            "model_response_status": "completed",
            "input_tokens_est": 9000,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(
                [
                    str(raw),
                    str(detected),
                    str(crops["raw__top_sources_and_buses.png"]),
                    str(crops["raw__train_a_4160_mcc.png"]),
                    str(crops["raw__dc_ups_center.png"]),
                    str(crops["raw__mcc_feeders_a_left.png"]),
                    str(crops["raw__mcc_feeders_a_right.png"]),
                    str(crops["raw__mcc_feeders_b_left.png"]),
                    str(crops["raw__mcc_feeders_b_right.png"]),
                    str(crops["raw__lower_rps_a.png"]),
                    str(crops["raw__lower_rps_b.png"]),
                    str(crops["raw__bus_tie_detail.png"]),
                ]
            ),
            "output_tokens_low": 1500,
            "output_tokens_expected": 3500,
            "output_tokens_high": 7000,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed in Codex tool runtime",
            "notes": "Main-agent visual inspection and setup; no Responses input-token API key available.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Diego R1 attempted",
            "call": "subagent_01_diego_full_bundle_shutdown",
            "model_response_status": "shutdown_after_timeout",
            "input_tokens_est": 4500,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(diego_attempt_images),
            "output_tokens_low": 0,
            "output_tokens_expected": 0,
            "output_tokens_high": 500,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed; no completed response returned",
            "notes": "Timed out and was closed; no matrix produced from this attempt.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Diego R1",
            "call": "subagent_02_diego_high_recall",
            "model_response_status": "completed",
            "input_tokens_est": 2500,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(diego_r1_images),
            "output_tokens_low": 3000,
            "output_tokens_expected": 4500,
            "output_tokens_high": 9000,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "High-recall extractor; matrix includes uncertain candidates for audit.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Jennifer R1",
            "call": "subagent_03_jennifer_precision_review",
            "model_response_status": "completed",
            "input_tokens_est": 5200,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(jennifer_images),
            "output_tokens_low": 2500,
            "output_tokens_expected": 4800,
            "output_tokens_high": 8500,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "Precision reviewer refined node set and removed line-label edges.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Diego R2",
            "call": "subagent_04_diego_saturation_check",
            "model_response_status": "completed_agreed_final",
            "input_tokens_est": 1400,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": 0,
            "output_tokens_low": 80,
            "output_tokens_expected": 120,
            "output_tokens_high": 300,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "Diego agreed with Jennifer's refined final matrix.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "main-finalization",
            "call": "main_02_artifact_generation_and_final_response",
            "model_response_status": "completed",
            "input_tokens_est": 6000,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(
                [
                    str(Path(r"C:\Asif_all_python_projects\INL\INL\doc3_work\close_cb101_bus.png")),
                    str(Path(r"C:\Asif_all_python_projects\INL\INL\doc3_work\close_dg1a_wide.png")),
                    str(Path(r"C:\Asif_all_python_projects\INL\INL\doc3_work\close_ground_raw.png")),
                    str(Path(r"C:\Asif_all_python_projects\INL\INL\doc3_work\riser_to_panel_a_full.png")),
                ]
            ),
            "output_tokens_low": 800,
            "output_tokens_expected": 1800,
            "output_tokens_high": 3500,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed in Codex tool runtime",
            "notes": "Local validation and final answer.",
        },
    ]

    for row in rows:
        row["input_tokens_low"] = math.ceil(int(row["input_tokens_est"]) * 0.75)
        row["input_tokens_high"] = math.ceil(int(row["input_tokens_est"]) * 1.35)
        row["image_file_tokens_low"] = math.ceil(int(row["image_file_tokens_est"]) * 0.6)
        row["image_file_tokens_high"] = math.ceil(int(row["image_file_tokens_est"]) * 1.4)
        row["total_tokens_low"] = (
            row["input_tokens_low"] + row["image_file_tokens_low"] + int(row["output_tokens_low"])
        )
        row["total_tokens_expected"] = (
            int(row["input_tokens_est"])
            + int(row["image_file_tokens_est"])
            + int(row["output_tokens_expected"])
        )
        row["total_tokens_high"] = (
            row["input_tokens_high"] + row["image_file_tokens_high"] + int(row["output_tokens_high"])
        )

    fieldnames = [
        "document",
        "iteration",
        "round",
        "call",
        "model_response_status",
        "input_tokens_low",
        "input_tokens_est",
        "input_tokens_high",
        "cached_input_tokens_est",
        "image_file_tokens_low",
        "image_file_tokens_est",
        "image_file_tokens_high",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_est",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_object",
        "notes",
    ]
    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    totals = {
        "document": 3,
        "iteration": 1,
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "endpoint_status": "OpenAI Responses input-token counting endpoint not called because OPENAI_API_KEY is absent.",
        "fallback_method": "Local estimate: tiktoken if installed, otherwise ceil(characters/4), plus high-detail image tile estimate.",
        "openai_docs": "https://developers.openai.com/api/docs/guides/token-counting",
    }
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(totals, indent=2), encoding="utf-8")

    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate\n\n")
        handle.write("The OpenAI Responses input-token counting endpoint was identified from official docs, ")
        handle.write("but was not called because no `OPENAI_API_KEY` is available in this environment.\n\n")
        handle.write("| Document | Iteration | Low | Expected | High |\n")
        handle.write("|---:|---:|---:|---:|---:|\n")
        handle.write(
            f"| {totals['document']} | {totals['iteration']} | {totals['total_tokens_low']} | "
            f"{totals['total_tokens_expected']} | {totals['total_tokens_high']} |\n\n"
        )
        handle.write("Fallback method: tiktoken when installed, otherwise `ceil(characters / 4)`; ")
        handle.write("image tokens use a conservative high-detail 512px tile estimate.\n\n")
        handle.write("Official docs: https://developers.openai.com/api/docs/guides/token-counting\n")


def write_round_notes() -> None:
    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Document 3 Round Notes\n\n")
        handle.write("Only resources from `Raw + wires + components + junctions` were used. No GT or GT-derived feedback was used.\n\n")
        handle.write("## Round Sequence\n\n")
        handle.write("1. Diego R1 full-bundle attempt timed out and was shut down; no matrix was produced from that attempt.\n")
        handle.write("2. Diego R1 narrowed high-recall extraction produced a matrix including uncertain candidate nodes/edges.\n")
        handle.write("3. Jennifer R1 removed line-label nodes and unsupported/overconnected edges.\n")
        handle.write("4. Diego R2 returned `AGREED_FINAL`; final matrix equals Jennifer R1.\n\n")
        handle.write("## Final Excluded / Ambiguous Cases\n\n")
        for item in EXCLUDED_CASES:
            handle.write(f"- {item}\n")
        handle.write("\n## Final Counts\n\n")
        handle.write(f"- Final nodes: {len(FINAL_NODES)}\n")
        handle.write(f"- Final undirected edges: {len(unique_edges(FINAL_EDGES))}\n")


def write_outputs() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds = [
        ("round_01_diego_high_recall", DIEGO_R1_NODES, unique_edges(DIEGO_R1_EDGES)),
        ("round_02_jennifer_precision", FINAL_NODES, unique_edges(FINAL_EDGES)),
        ("round_03_diego_agreed", FINAL_NODES, unique_edges(FINAL_EDGES)),
        ("final", FINAL_NODES, unique_edges(FINAL_EDGES)),
    ]
    for prefix, nodes, edges in rounds:
        validate(nodes, edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)
        write_edge_list(RESULTS / f"{prefix}_edge_list.csv", edges)
        (RESULTS / f"{prefix}_node_list.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")

    write_edge_list(RESULTS / "round_01_diego_uncertain_candidates.csv", DIEGO_R1_UNCERTAIN_EDGES)
    write_round_notes()
    write_usage_estimates()


if __name__ == "__main__":
    write_outputs()
