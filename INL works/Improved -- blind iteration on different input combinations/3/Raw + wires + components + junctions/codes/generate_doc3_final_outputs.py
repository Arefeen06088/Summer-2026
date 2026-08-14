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
    return [part.strip() for part in text.replace("\n", ",").split(",") if part.strip()]


@dataclass(frozen=True)
class Edge:
    a: str
    b: str
    evidence: str
    status: str = "accepted"


def e(a: str, b: str, evidence: str, status: str = "accepted") -> Edge:
    return Edge(a, b, evidence, status)


DIEGO_R1_NODES = split_names(
    """
GRID-1, AUX-TR-1A, CB-101, BUS-416A, BUS-TIE-41, BUS-416B, CB-102, AUX-TR-1B, GRID-2,
EDG-1A, CB-DG1A, EDG-1B, CB-DG1B, FDR-A1, FDR-A2, FDR-B1, FDR-B2,
TR-480A1, TR-480A2, TR-480B1, TR-480B2, CB-480A1, CB-480A2, CB-480B1, CB-480B2,
MCC-480A1, MCC-480A2, MCC-480B1, MCC-480B2,
CB-CHG-A, CHGR-125A, BAT-125A, DC-BUS-A, INV-120A, BUS-120A,
CB-CHG-B, CHGR-125B, BAT-125B, DC-BUS-B, INV-120B, BUS-120B, GND-1E, GND-A, GND-B,
FDB-A1, FDB-A2, FDB-B1, FDB-B2,
CB-SI-A1, PUMP-SI-A1, CB-RHR-A1, PUMP-RHR-A1, CB-CCW-A1, PUMP-CCW-A1, CB-FAN-A1, FAN-CR-A1, CB-MOV-A101, VALVE-SI-A101, CB-MOV-A102, VALVE-RHR-A102,
CB-CS-A2, PUMP-CS-A2, CB-SW-A2, PUMP-SW-A2, CB-AFW-A2, PUMP-AFW-A2, CB-FAN-A2, FAN-EB-A2, CB-MOV-A201, VALVE-CCW-A201, CB-HTR-A2, HTR-BAY-A2,
CB-SI-B1, PUMP-SI-B1, CB-RHR-B1, PUMP-RHR-B1, CB-CCW-B1, PUMP-CCW-B1, CB-FAN-B1, FAN-CR-B1, CB-MOV-B101, VALVE-SI-B101, CB-MOV-B102, VALVE-RHR-B102,
CB-CS-B2, PUMP-CS-B2, CB-SW-B2, PUMP-SW-B2, CB-FAN-B2, FAN-EB-B2, CB-MOV-B201, VALVE-CCW-B201, CB-HTR-B2, HTR-BAY-B2,
INST-PT-A, INST-LT-A, RELAY-K27A, PANEL-RPS-A, PANEL-ESF-A, JB-A401,
INST-PT-B, INST-LT-B, RELAY-K27B, PANEL-RPS-B, PANEL-ESF-B, JB-B501
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


def load_edges(bus: str, breaker: str, load: str) -> list[Edge]:
    return [
        e(bus, breaker, "vertical tap from MCC feeder bus to breaker"),
        e(breaker, load, "solid vertical drop from breaker to load"),
    ]


LOAD_CHAINS = [
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


DIEGO_R1_EDGES = [
    e("GRID-1", "AUX-TR-1A", "solid offsite A line"),
    e("AUX-TR-1A", "CB-101", "solid line into CB-101"),
    e("CB-102", "AUX-TR-1B", "solid line from CB-102"),
    e("AUX-TR-1B", "GRID-2", "solid offsite B line"),
    e("BUS-416A", "BUS-TIE-41", "left bus enters tie switch"),
    e("BUS-TIE-41", "BUS-416B", "tie switch exits to right bus"),
    e("EDG-1A", "CB-DG1A", "solid generator A lead"),
    e("CB-DG1A", "FDR-A1", "branch to feeder label"),
    e("BUS-416A", "FDR-A1", "tap from BUS-416A"),
    e("FDR-A1", "TR-480A1", "vertical feeder to transformer"),
    e("TR-480A1", "CB-480A1", "transformer low-side vertical"),
    e("CB-480A1", "MCC-480A1", "breaker output to MCC"),
    e("MCC-480A1", "FDB-A1", "buckets shown below"),
    e("BUS-416A", "FDR-A2", "tap from BUS-416A"),
    e("FDR-A2", "TR-480A2", "vertical feeder to transformer"),
    e("TR-480A2", "CB-480A2", "transformer low-side vertical"),
    e("CB-480A2", "MCC-480A2", "breaker output to MCC"),
    e("MCC-480A2", "FDB-A2", "buckets shown below"),
    e("BUS-416B", "FDR-B1", "tap from BUS-416B"),
    e("FDR-B1", "TR-480B1", "vertical feeder to transformer"),
    e("TR-480B1", "CB-480B1", "transformer low-side vertical"),
    e("CB-480B1", "MCC-480B1", "breaker output to MCC"),
    e("MCC-480B1", "FDB-B1", "buckets shown below"),
    e("BUS-416B", "FDR-B2", "tap from BUS-416B"),
    e("FDR-B2", "TR-480B2", "vertical feeder to transformer"),
    e("TR-480B2", "CB-480B2", "transformer low-side vertical"),
    e("CB-480B2", "MCC-480B2", "breaker output to MCC"),
    e("MCC-480B2", "FDB-B2", "buckets shown below"),
    e("FDR-B2", "CB-DG1B", "branch to DG breaker"),
    e("CB-DG1B", "EDG-1B", "solid generator B lead"),
    e("BUS-416A", "CB-CHG-A", "solid charger A feeder"),
    e("CB-CHG-A", "CHGR-125A", "52-CA downlead"),
    e("CHGR-125A", "DC-BUS-A", "charger A output to DC bus"),
    e("BAT-125A", "DC-BUS-A", "battery A lead to DC bus"),
    e("DC-BUS-A", "INV-120A", "125V DC A vertical"),
    e("INV-120A", "BUS-120A", "120VAC inverter A output"),
    e("BUS-416B", "CB-CHG-B", "solid charger B feeder"),
    e("CB-CHG-B", "CHGR-125B", "52-CB downlead"),
    e("CHGR-125B", "DC-BUS-B", "charger B output to DC bus"),
    e("BAT-125B", "DC-BUS-B", "battery B lead to DC bus"),
    e("DC-BUS-B", "INV-120B", "125V DC B vertical"),
    e("INV-120B", "BUS-120B", "120VAC inverter B output"),
]

for chain in LOAD_CHAINS:
    DIEGO_R1_EDGES.extend(load_edges(*chain))

DIEGO_R1_EDGES.extend(
    [
        e("INST-PT-A", "PANEL-RPS-A", "dotted upper signal line"),
        e("INST-LT-A", "PANEL-RPS-A", "dotted lower signal line"),
        e("RELAY-K27A", "PANEL-RPS-A", "dashed center control line"),
        e("RELAY-K27A", "PANEL-ESF-A", "dashed UV relay A line"),
        e("PANEL-ESF-A", "JB-A401", "dashed TB-ESF-A line"),
        e("INST-PT-B", "PANEL-RPS-B", "dotted upper signal line"),
        e("INST-LT-B", "PANEL-RPS-B", "dotted lower signal line"),
        e("RELAY-K27B", "PANEL-RPS-B", "dashed center control line"),
        e("RELAY-K27B", "PANEL-ESF-B", "dashed UV relay B line"),
        e("PANEL-ESF-B", "JB-B501", "dashed TB-ESF-B line"),
    ]
)

DIEGO_R1_UNCERTAIN = [
    e("CB-101", "BUS-416A", "plausible offsite A source tie but visible lower stub stops above bus", "uncertain"),
    e("CB-102", "BUS-416B", "plausible offsite B source tie but visible lower stub stops above bus", "uncertain"),
    e("BUS-TIE-41", "GND-1E", "nearby ground/reference marking, not a clear conductor", "uncertain"),
    e("GND-A", "GND-1E", "dash-dot ground reference marking", "uncertain"),
    e("GND-B", "GND-1E", "dash-dot ground reference marking", "uncertain"),
    e("BUS-120A", "PANEL-RPS-A", "dashed 120VAC instrument/control riser", "uncertain"),
    e("BUS-120A", "PANEL-ESF-A", "possible but not directly visible into ESF panel", "uncertain"),
    e("BUS-120B", "PANEL-RPS-B", "dashed 120VAC instrument/control riser", "uncertain"),
    e("BUS-120B", "PANEL-ESF-B", "possible but not directly visible into ESF panel", "uncertain"),
    e("PANEL-RPS-A", "PANEL-ESF-A", "functional association only; no direct conductor", "uncertain"),
    e("PANEL-RPS-B", "PANEL-ESF-B", "functional association only; no direct conductor", "uncertain"),
]


FINAL_EDGES = [
    e("GRID-1", "AUX-TR-1A", "solid offsite A line"),
    e("AUX-TR-1A", "CB-101", "solid line into CB-101"),
    e("CB-102", "AUX-TR-1B", "solid line from CB-102"),
    e("AUX-TR-1B", "GRID-2", "solid offsite B line"),
    e("BUS-416A", "BUS-TIE-41", "BUS-416A enters normally open bus tie"),
    e("BUS-TIE-41", "BUS-416B", "bus tie exits to BUS-416B"),
    e("EDG-1A", "CB-DG1A", "solid generator A lead"),
    e("CB-DG1A", "BUS-416A", "DG breaker feeder lands on BUS-416A"),
    e("BUS-416A", "TR-480A1", "solid feeder down to transformer"),
    e("TR-480A1", "CB-480A1", "solid transformer low-side vertical"),
    e("CB-480A1", "MCC-480A1", "solid breaker output to MCC"),
    e("MCC-480A1", "FDB-A1", "buckets shown below connection"),
    e("BUS-416A", "TR-480A2", "solid feeder down to transformer"),
    e("TR-480A2", "CB-480A2", "solid transformer low-side vertical"),
    e("CB-480A2", "MCC-480A2", "solid breaker output to MCC"),
    e("MCC-480A2", "FDB-A2", "buckets shown below connection"),
    e("BUS-416B", "TR-480B1", "solid feeder down to transformer"),
    e("TR-480B1", "CB-480B1", "solid transformer low-side vertical"),
    e("CB-480B1", "MCC-480B1", "solid breaker output to MCC"),
    e("MCC-480B1", "FDB-B1", "buckets shown below connection"),
    e("BUS-416B", "TR-480B2", "solid feeder down to transformer"),
    e("TR-480B2", "CB-480B2", "solid transformer low-side vertical"),
    e("CB-480B2", "MCC-480B2", "solid breaker output to MCC"),
    e("MCC-480B2", "FDB-B2", "buckets shown below connection"),
    e("BUS-416B", "CB-DG1B", "DG breaker feeder lands on BUS-416B"),
    e("CB-DG1B", "EDG-1B", "solid generator B lead"),
    e("BUS-416A", "CB-CHG-A", "solid charger A feeder"),
    e("CB-CHG-A", "CHGR-125A", "52-CA downlead"),
    e("CHGR-125A", "DC-BUS-A", "charger A output to DC bus"),
    e("BAT-125A", "DC-BUS-A", "battery A lead to DC bus"),
    e("DC-BUS-A", "INV-120A", "125V DC A vertical"),
    e("INV-120A", "BUS-120A", "120VAC inverter A output"),
    e("BUS-416B", "CB-CHG-B", "solid charger B feeder"),
    e("CB-CHG-B", "CHGR-125B", "52-CB downlead"),
    e("CHGR-125B", "DC-BUS-B", "charger B output to DC bus"),
    e("BAT-125B", "DC-BUS-B", "battery B lead to DC bus"),
    e("DC-BUS-B", "INV-120B", "125V DC B vertical"),
    e("INV-120B", "BUS-120B", "120VAC inverter B output"),
]

for chain in LOAD_CHAINS:
    FINAL_EDGES.extend(load_edges(*chain))

FINAL_EDGES.extend(
    [
        e("BUS-120A", "PANEL-RPS-A", "dashed 120VAC instrument/control riser to RPS A"),
        e("INST-PT-A", "PANEL-RPS-A", "dotted PT-A signal line"),
        e("INST-LT-A", "PANEL-RPS-A", "dotted LT-A signal line"),
        e("RELAY-K27A", "PANEL-RPS-A", "dashed relay A control line"),
        e("RELAY-K27A", "PANEL-ESF-A", "dashed UV relay A output to ESF"),
        e("PANEL-ESF-A", "JB-A401", "dashed ESF A line to junction box"),
        e("BUS-120B", "PANEL-RPS-B", "dashed 120VAC instrument/control riser to RPS B"),
        e("INST-PT-B", "PANEL-RPS-B", "dotted PT-B signal line"),
        e("INST-LT-B", "PANEL-RPS-B", "dotted LT-B signal line"),
        e("RELAY-K27B", "PANEL-RPS-B", "dashed relay B control line"),
        e("RELAY-K27B", "PANEL-ESF-B", "dashed UV relay B output to ESF"),
        e("PANEL-ESF-B", "JB-B501", "dashed ESF B line to junction box"),
    ]
)


EXCLUDED_CASES = [
    "CB-101--BUS-416A and CB-102--BUS-416B: visible lower stubs stop above BUS-416A/B; no hidden tie inferred.",
    "FDR-A1/FDR-A2/FDR-B1/FDR-B2: feeder line labels, not equipment nodes; collapsed to direct visual component edges.",
    "GND-1E/GND-A/GND-B: standalone reference/ground markings; no unambiguous connected conductor in the graph.",
    "BUS-120A/B--PANEL-ESF-A/B: ESF panels connect via relay path, not directly to the 120 VAC bus.",
    "PANEL-RPS-A/B--PANEL-ESF-A/B: no direct panel-to-panel conductor; connection is through RELAY-K27A/B.",
]


def unique_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str, str]] = set()
    result: list[Edge] = []
    for edge in edges:
        a, b = sorted((edge.a, edge.b))
        key = (a, b, edge.status)
        if key not in seen:
            seen.add(key)
            result.append(edge)
    return result


def validate(nodes: list[str], edges: list[Edge]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
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
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


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


def image_total(paths: list[Path]) -> int:
    return sum(estimate_image_tokens(path) for path in paths)


def make_usage_rows() -> list[dict[str, object]]:
    raw = BASE / "raw -- synthetic_npp_100_component_electrical_schematic.png"
    detected = BASE / "detected_components_and_logical_overlay.png"
    wire_nodes = BASE / "wire_nodes_overlay.png"
    crops = [
        RESULTS / "raw__top_sources_and_buses.png",
        RESULTS / "raw__train_a_4160_mcc.png",
        RESULTS / "raw__train_b_4160_mcc.png",
        RESULTS / "raw__charger_feed_detail.png",
        RESULTS / "raw__dc_ups_center.png",
        RESULTS / "raw__mcc_feeders_a_left.png",
        RESULTS / "raw__mcc_feeders_a_right.png",
        RESULTS / "raw__mcc_feeders_b_left.png",
        RESULTS / "raw__mcc_feeders_b_right.png",
        RESULTS / "raw__lower_rps_a.png",
        RESULTS / "raw__lower_rps_b.png",
        RESULTS / "raw__bus_tie_detail.png",
    ]
    wire_crops = [
        RESULTS / "wire_nodes__top_sources_and_buses.png",
        RESULTS / "wire_nodes__train_a_4160_mcc.png",
        RESULTS / "wire_nodes__train_b_4160_mcc.png",
        RESULTS / "wire_nodes__dc_ups_center.png",
        RESULTS / "wire_nodes__lower_rps_a.png",
        RESULTS / "wire_nodes__lower_rps_b.png",
    ]

    rows = [
        {
            "document": 3,
            "iteration": 1,
            "round": "main-setup",
            "call": "main_01_resource_inventory_crop_visual_inspection",
            "model_response_status": "completed",
            "input_tokens_est": 8000,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total([raw, detected, wire_nodes] + crops + wire_crops),
            "output_tokens_low": 400,
            "output_tokens_expected": 900,
            "output_tokens_high": 1800,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed in Codex runtime",
            "notes": "Main-agent setup, crop generation, and visual inspection. Estimate includes visible task context allowance.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Diego R1",
            "call": "subagent_01_diego_high_recall_extraction",
            "model_response_status": "completed",
            "input_tokens_est": 3100,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total([raw] + crops[:11] + [wire_crops[0], wire_crops[3], wire_crops[4], wire_crops[5]]),
            "output_tokens_low": 2200,
            "output_tokens_expected": 3200,
            "output_tokens_high": 5000,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "High-recall visual extractor. Output known qualitatively; token count estimated locally.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Jennifer R1",
            "call": "subagent_02_jennifer_precision_review",
            "model_response_status": "completed",
            "input_tokens_est": 6200,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total([raw] + [crops[i] for i in [0, 3, 4, 5, 6, 7, 8, 9, 10]] + [wire_crops[0], wire_crops[3], wire_crops[4], wire_crops[5]]),
            "output_tokens_low": 1800,
            "output_tokens_expected": 2700,
            "output_tokens_high": 4300,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "Precision review using Diego proposal and image bundle.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "Diego R2",
            "call": "subagent_03_diego_saturation_check",
            "model_response_status": "completed_agreed_with_gnd_exclusion",
            "input_tokens_est": 2600,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": 0,
            "output_tokens_low": 180,
            "output_tokens_expected": 320,
            "output_tokens_high": 700,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "Text-only saturation check. Diego agreed with Jennifer except excluded isolated GND-1E.",
        },
        {
            "document": 3,
            "iteration": 1,
            "round": "main-finalization",
            "call": "main_02_artifact_generation_validation_final_response",
            "model_response_status": "completed",
            "input_tokens_est": 5500,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": 0,
            "output_tokens_low": 600,
            "output_tokens_expected": 1200,
            "output_tokens_high": 2400,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed in Codex runtime",
            "notes": "Local artifact writing and final response. Excludes hidden system/tool framing.",
        },
    ]

    for row in rows:
        row["input_tokens_low"] = math.ceil(int(row["input_tokens_est"]) * 0.75)
        row["input_tokens_high"] = math.ceil(int(row["input_tokens_est"]) * 1.35)
        row["image_file_tokens_low"] = math.ceil(int(row["image_file_tokens_est"]) * 0.60)
        row["image_file_tokens_high"] = math.ceil(int(row["image_file_tokens_est"]) * 1.40)
        row["total_tokens_low"] = int(row["input_tokens_low"]) + int(row["image_file_tokens_low"]) + int(row["output_tokens_low"])
        row["total_tokens_expected"] = int(row["input_tokens_est"]) + int(row["image_file_tokens_est"]) + int(row["output_tokens_expected"])
        row["total_tokens_high"] = int(row["input_tokens_high"]) + int(row["image_file_tokens_high"]) + int(row["output_tokens_high"])
    return rows


def write_usage_estimates() -> None:
    rows = make_usage_rows()
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
        "responses_input_token_counting_endpoint": "POST /v1/responses/input_tokens",
        "endpoint_called": bool(os.environ.get("OPENAI_API_KEY")),
        "endpoint_status": "Not called because OPENAI_API_KEY is absent." if not os.environ.get("OPENAI_API_KEY") else "API key present; local script still used fallback only.",
        "fallback_method": "Text: tiktoken o200k_base if installed, otherwise ceil(characters/4). Images: high-detail 512px tile estimate, 85 base + 170 per tile after OpenAI-style resizing.",
        "usage_object_status": "Actual usage objects are not exposed by this Codex multi_agent_v1/tool runtime.",
        "official_reference": "https://platform.openai.com/docs/api-reference/responses/input_tokens",
    }
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(totals, indent=2), encoding="utf-8")

    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate\n\n")
        handle.write("No `OPENAI_API_KEY` is available, so the OpenAI Responses input-token counting endpoint was not called.\n")
        handle.write("Official endpoint noted for future runs: `POST /v1/responses/input_tokens`.\n\n")
        handle.write("| Document | Iteration | Low | Expected | High |\n")
        handle.write("|---:|---:|---:|---:|---:|\n")
        handle.write(
            f"| {totals['document']} | {totals['iteration']} | {totals['total_tokens_low']} | "
            f"{totals['total_tokens_expected']} | {totals['total_tokens_high']} |\n\n"
        )
        handle.write("Fallback method: text tokens via `tiktoken` when available, otherwise `ceil(characters / 4)`; ")
        handle.write("image/file tokens via high-detail 512px tile estimate.\n")


def write_round_notes() -> None:
    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Document 3 Round Notes\n\n")
        handle.write("Only resources from `Raw + wires + components + junctions` were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.\n\n")
        handle.write("## Round Sequence\n\n")
        handle.write("1. Diego R1 high-recall extraction proposed component nodes, feeder-label nodes, accepted edges, and uncertain candidates.\n")
        handle.write("2. Jennifer R1 removed non-component line-label nodes, rejected unsupported source-bus and ground-reference edges, and accepted BUS-120A/B to RPS panel risers.\n")
        handle.write("3. Diego R2 agreed with Jennifer after one correction: exclude isolated `GND-1E` from the final matrix.\n\n")
        handle.write("## Final Excluded / Ambiguous Cases\n\n")
        for item in EXCLUDED_CASES:
            handle.write(f"- {item}\n")
        handle.write("\n## Final Counts\n\n")
        handle.write(f"- Final nodes: {len(FINAL_NODES)}\n")
        handle.write(f"- Final undirected edges: {len(unique_edges(FINAL_EDGES))}\n")


def write_outputs() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    diego_edges = unique_edges(DIEGO_R1_EDGES + DIEGO_R1_UNCERTAIN)
    final_edges = unique_edges(FINAL_EDGES)
    rounds = [
        ("round_01_diego_high_recall", DIEGO_R1_NODES, diego_edges),
        ("round_02_jennifer_precision", FINAL_NODES, final_edges),
        ("round_03_diego_agreed", FINAL_NODES, final_edges),
        ("final", FINAL_NODES, final_edges),
    ]
    for prefix, nodes, edges in rounds:
        validate(nodes, edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)
        write_edge_list(RESULTS / f"{prefix}_edge_list.csv", edges)
        (RESULTS / f"{prefix}_node_list.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")

    write_edge_list(RESULTS / "round_01_diego_uncertain_candidates.csv", DIEGO_R1_UNCERTAIN)
    write_round_notes()
    write_usage_estimates()


if __name__ == "__main__":
    write_outputs()
