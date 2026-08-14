from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_schematic_improved.png"
DOCUMENT = "38"
ITERATION = "1"


FINAL_NODES = [
    "GEN-U2A",
    "CB-101",
    "TR-UAT-2A",
    "DG-2A",
    "CB-103",
    "BUS-4160A",
    "CB-105",
    "BUS-4160B",
    "CB-102",
    "TR-SUT-2B",
    "CB-104",
    "DG-2B",
    "CB-201A",
    "TR-201A",
    "CB-301A",
    "BUS-480A",
    "CB-401A",
    "MCC-2A1",
    "PUMP-RHR2A",
    "PUMP-CCW2A",
    "PUMP-SW2A",
    "FAN-CR2A",
    "MOV-RHR141A",
    "MOV-SI221A",
    "TR-CPT-A",
    "CHGR-2A",
    "BAT-125A",
    "125 VDC TRAIN A",
    "INV-2A",
    "BUS-120AC-A",
    "RELAY-86A",
    "RPS-PNL-A",
    "RELAY-27A",
    "CB-201B",
    "TR-201B",
    "CB-301B",
    "BUS-480B",
    "CB-401B",
    "MCC-2B1",
    "PUMP-RHR2B",
    "PUMP-CCW2B",
    "PUMP-SW2B",
    "FAN-CR2B",
    "MOV-RHR142B",
    "MOV-SI222B",
    "TR-CPT-B",
    "CHGR-2B",
    "BAT-125B",
    "125 VDC TRAIN B",
    "INV-2B",
    "BUS-120AC-B",
    "RELAY-86B",
    "RPS-PNL-B",
    "RELAY-27B",
]


FINAL_EDGES = [
    ("GEN-U2A", "CB-101"),
    ("CB-101", "TR-UAT-2A"),
    ("TR-UAT-2A", "BUS-4160A"),
    ("DG-2A", "CB-103"),
    ("CB-103", "BUS-4160A"),
    ("BUS-4160A", "CB-105"),
    ("CB-105", "BUS-4160B"),
    ("TR-SUT-2B", "CB-102"),
    ("CB-102", "BUS-4160B"),
    ("DG-2B", "CB-104"),
    ("CB-104", "BUS-4160B"),
    ("BUS-4160A", "CB-201A"),
    ("CB-201A", "TR-201A"),
    ("TR-201A", "CB-301A"),
    ("CB-301A", "BUS-480A"),
    ("BUS-4160B", "CB-201B"),
    ("CB-201B", "TR-201B"),
    ("TR-201B", "CB-301B"),
    ("CB-301B", "BUS-480B"),
    ("BUS-480A", "CB-401A"),
    ("CB-401A", "MCC-2A1"),
    ("MCC-2A1", "PUMP-RHR2A"),
    ("MCC-2A1", "PUMP-CCW2A"),
    ("MCC-2A1", "PUMP-SW2A"),
    ("MCC-2A1", "FAN-CR2A"),
    ("MCC-2A1", "MOV-RHR141A"),
    ("MCC-2A1", "MOV-SI221A"),
    ("BUS-480A", "TR-CPT-A"),
    ("BUS-480A", "CHGR-2A"),
    ("CHGR-2A", "125 VDC TRAIN A"),
    ("BAT-125A", "125 VDC TRAIN A"),
    ("125 VDC TRAIN A", "INV-2A"),
    ("INV-2A", "BUS-120AC-A"),
    ("125 VDC TRAIN A", "RELAY-86A"),
    ("BUS-120AC-A", "RPS-PNL-A"),
    ("RPS-PNL-A", "RELAY-27A"),
    ("BUS-480B", "CB-401B"),
    ("CB-401B", "MCC-2B1"),
    ("MCC-2B1", "PUMP-RHR2B"),
    ("MCC-2B1", "PUMP-CCW2B"),
    ("MCC-2B1", "PUMP-SW2B"),
    ("MCC-2B1", "FAN-CR2B"),
    ("MCC-2B1", "MOV-RHR142B"),
    ("MCC-2B1", "MOV-SI222B"),
    ("BUS-480B", "TR-CPT-B"),
    ("BUS-480B", "CHGR-2B"),
    ("TR-CPT-B", "BUS-120AC-B"),
    ("CHGR-2B", "125 VDC TRAIN B"),
    ("BAT-125B", "125 VDC TRAIN B"),
    ("125 VDC TRAIN B", "INV-2B"),
    ("INV-2B", "BUS-120AC-B"),
    ("125 VDC TRAIN B", "RELAY-86B"),
    ("BUS-120AC-B", "RPS-PNL-B"),
    ("BUS-120AC-B", "RELAY-27B"),
    ("RPS-PNL-B", "RELAY-27B"),
]


ROUND1_NODES = [
    "TO UNIT AUX BUS CONT.",
    "GEN-U2A",
    "CB-101",
    "TR-UAT-2A",
    "DG-2A",
    "CB-103",
    "BUS-4160A",
    "CB-105",
    "BUS-4160B",
    "TR-SUT-2B",
    "CB-102",
    "DG-2B",
    "CB-104",
    "CB-201A",
    "TR-201A",
    "CB-301A",
    "BUS-480A",
    "CB-401A",
    "MCC-2A1",
    "MCC-2A1-01",
    "MCC-2A1-02",
    "MCC-2A1-03",
    "MCC-2A1-04",
    "MCC-2A1-05",
    "MCC-2A1-06",
    "PUMP-RHR2A",
    "PUMP-CCW2A",
    "PUMP-SW2A",
    "FAN-CR2A",
    "MOV-RHR141A",
    "MOV-SI221A",
    "TR-CPT-A",
    "CHGR-2A",
    "BAT-125A",
    "125 VDC TRAIN A",
    "INV-2A",
    "BUS-120AC-A",
    "RELAY-86A",
    "RPS-PNL-A",
    "RELAY-27A",
    "CB-201B",
    "TR-201B",
    "CB-301B",
    "BUS-480B",
    "CB-401B",
    "MCC-2B1",
    "MCC-2B1-01",
    "MCC-2B1-02",
    "MCC-2B1-03",
    "MCC-2B1-04",
    "MCC-2B1-05",
    "MCC-2B1-06",
    "PUMP-RHR2B",
    "PUMP-CCW2B",
    "PUMP-SW2B",
    "FAN-CR2B",
    "MOV-RHR142B",
    "MOV-SI222B",
    "TR-CPT-B",
    "CHGR-2B",
    "BAT-125B",
    "125 VDC TRAIN B",
    "INV-2B",
    "BUS-120AC-B",
    "RELAY-86B",
    "RPS-PNL-B",
    "RELAY-27B",
    "GND-STA",
    "2A-C72",
    "2A-C86",
    "2B-C72",
    "2B-C86",
    "ESF DIESEL A",
    "ESF DIESEL B",
]


ROUND1_BASE_EDGES = [
    ("TO UNIT AUX BUS CONT.", "GEN-U2A"),
    ("GEN-U2A", "CB-101"),
    ("CB-101", "TR-UAT-2A"),
    ("TR-UAT-2A", "BUS-4160A"),
    ("DG-2A", "CB-103"),
    ("CB-103", "BUS-4160A"),
    ("BUS-4160A", "CB-105"),
    ("CB-105", "BUS-4160B"),
    ("TR-SUT-2B", "CB-102"),
    ("CB-102", "BUS-4160B"),
    ("DG-2B", "CB-104"),
    ("CB-104", "BUS-4160B"),
    ("BUS-4160A", "CB-201A"),
    ("CB-201A", "TR-201A"),
    ("TR-201A", "CB-301A"),
    ("CB-301A", "BUS-480A"),
    ("BUS-4160B", "CB-201B"),
    ("CB-201B", "TR-201B"),
    ("TR-201B", "CB-301B"),
    ("CB-301B", "BUS-480B"),
    ("BUS-480A", "CB-401A"),
    ("CB-401A", "MCC-2A1"),
    ("MCC-2A1", "MCC-2A1-01"),
    ("MCC-2A1-01", "PUMP-RHR2A"),
    ("MCC-2A1", "MCC-2A1-02"),
    ("MCC-2A1-02", "PUMP-CCW2A"),
    ("MCC-2A1", "MCC-2A1-03"),
    ("MCC-2A1-03", "PUMP-SW2A"),
    ("MCC-2A1", "MCC-2A1-04"),
    ("MCC-2A1-04", "FAN-CR2A"),
    ("MCC-2A1", "MCC-2A1-05"),
    ("MCC-2A1-05", "MOV-RHR141A"),
    ("MCC-2A1", "MCC-2A1-06"),
    ("MCC-2A1-06", "MOV-SI221A"),
    ("BUS-480A", "TR-CPT-A"),
    ("BUS-480A", "CHGR-2A"),
    ("CHGR-2A", "125 VDC TRAIN A"),
    ("BAT-125A", "125 VDC TRAIN A"),
    ("125 VDC TRAIN A", "INV-2A"),
    ("INV-2A", "BUS-120AC-A"),
    ("125 VDC TRAIN A", "RELAY-86A"),
    ("BUS-120AC-A", "RPS-PNL-A"),
    ("RPS-PNL-A", "RELAY-27A"),
    ("BUS-480B", "CB-401B"),
    ("CB-401B", "MCC-2B1"),
    ("MCC-2B1", "MCC-2B1-01"),
    ("MCC-2B1-01", "PUMP-RHR2B"),
    ("MCC-2B1", "MCC-2B1-02"),
    ("MCC-2B1-02", "PUMP-CCW2B"),
    ("MCC-2B1", "MCC-2B1-03"),
    ("MCC-2B1-03", "PUMP-SW2B"),
    ("MCC-2B1", "MCC-2B1-04"),
    ("MCC-2B1-04", "FAN-CR2B"),
    ("MCC-2B1", "MCC-2B1-05"),
    ("MCC-2B1-05", "MOV-RHR142B"),
    ("MCC-2B1", "MCC-2B1-06"),
    ("MCC-2B1-06", "MOV-SI222B"),
    ("BUS-480B", "TR-CPT-B"),
    ("BUS-480B", "CHGR-2B"),
    ("TR-CPT-B", "BUS-120AC-B"),
    ("CHGR-2B", "125 VDC TRAIN B"),
    ("BAT-125B", "125 VDC TRAIN B"),
    ("125 VDC TRAIN B", "INV-2B"),
    ("INV-2B", "BUS-120AC-B"),
    ("125 VDC TRAIN B", "RELAY-86B"),
    ("BUS-120AC-B", "RPS-PNL-B"),
    ("BUS-120AC-B", "RELAY-27B"),
    ("RPS-PNL-B", "RELAY-27B"),
]


ROUND1_EXTRA_EDGES = [
    ("TR-CPT-A", "BUS-120AC-A"),
    ("BUS-120AC-A", "RELAY-27A"),
    ("RELAY-86A", "2A-C86"),
    ("RELAY-27A", "2A-C72"),
    ("RELAY-86B", "2B-C86"),
    ("RELAY-27B", "2B-C72"),
    ("DG-2A", "ESF DIESEL A"),
    ("DG-2B", "ESF DIESEL B"),
    ("GND-STA", "2A-C72"),
    ("GND-STA", "2A-C86"),
]


ROUND_DEFINITIONS = [
    {
        "round": 1,
        "agent": "Diego",
        "label": "high_recall",
        "nodes": ROUND1_NODES,
        "edges": ROUND1_BASE_EDGES + ROUND1_EXTRA_EDGES,
        "comment": "High-recall proposal included off-sheet continuation, MCC bucket numbers, cable-route labels, ESF area labels, and ambiguous A-side/bus/ground extras.",
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "label": "precision_review",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "comment": "Precision review folded MCC bucket numbers into MCC-to-load edges and removed route labels, continuation boxes, ground/reference labels, and unsupported A-side inferred edges.",
    },
    {
        "round": 3,
        "agent": "Diego",
        "label": "saturation",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "comment": "Diego accepted Jennifer's precision graph after checking the raw-only crops.",
    },
    {
        "round": 4,
        "agent": "Jennifer",
        "label": "final",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "comment": "Final confirmation using normalized primary device IDs and exact bus labels.",
    },
]


EDGE_EVIDENCE = {
    "GEN-U2A--CB-101": "Solid conductor from generator GEN-U2A to breaker CB-101.",
    "CB-101--TR-UAT-2A": "CB-101 output is wired into transformer TR-UAT-2A.",
    "TR-UAT-2A--BUS-4160A": "Transformer secondary lands on BUS-4160A with a junction dot.",
    "DG-2A--CB-103": "Diesel generator DG-2A feeds breaker CB-103.",
    "CB-103--BUS-4160A": "CB-103 feeder ties into the BUS-4160A riser.",
    "BUS-4160A--CB-105": "Left side of the normally open bus-tie breaker connects to BUS-4160A.",
    "CB-105--BUS-4160B": "Right side of the normally open bus-tie breaker connects to BUS-4160B.",
    "TR-SUT-2B--CB-102": "Startup auxiliary transformer TR-SUT-2B feeds breaker CB-102.",
    "CB-102--BUS-4160B": "CB-102 drops onto BUS-4160B with a junction dot.",
    "DG-2B--CB-104": "Diesel generator DG-2B feeds breaker CB-104.",
    "CB-104--BUS-4160B": "CB-104 feeder lands on BUS-4160B.",
    "BUS-4160A--CB-201A": "BUS-4160A vertical feeder enters CB-201A.",
    "CB-201A--TR-201A": "CB-201A is in series above transformer TR-201A.",
    "TR-201A--CB-301A": "Transformer TR-201A output passes through CB-301A.",
    "CB-301A--BUS-480A": "CB-301A lands on BUS-480A.",
    "BUS-4160B--CB-201B": "BUS-4160B vertical feeder enters CB-201B.",
    "CB-201B--TR-201B": "CB-201B is in series above transformer TR-201B.",
    "TR-201B--CB-301B": "Transformer TR-201B output passes through CB-301B.",
    "CB-301B--BUS-480B": "CB-301B lands on BUS-480B.",
    "BUS-480A--CB-401A": "BUS-480A feeder enters CB-401A.",
    "CB-401A--MCC-2A1": "CB-401A output enters MCC-2A1.",
    "MCC-2A1--PUMP-RHR2A": "MCC-2A1 bucket 01 feeder 2A-F1 drops to PUMP-RHR2A.",
    "MCC-2A1--PUMP-CCW2A": "MCC-2A1 bucket 02 feeder 2A-F2 drops to PUMP-CCW2A.",
    "MCC-2A1--PUMP-SW2A": "MCC-2A1 bucket 03 feeder 2A-F3 drops to PUMP-SW2A.",
    "MCC-2A1--FAN-CR2A": "MCC-2A1 bucket 04 feeder 2A-F4 drops to FAN-CR2A.",
    "MCC-2A1--MOV-RHR141A": "MCC-2A1 bucket 05 feeder 2A-F5 drops to MOV-RHR141A.",
    "MCC-2A1--MOV-SI221A": "MCC-2A1 bucket 06 feeder 2A-F6 drops to MOV-SI221A.",
    "BUS-480A--TR-CPT-A": "A solid feeder from BUS-480A drops to TR-CPT-A.",
    "BUS-480A--CHGR-2A": "A separate solid feeder from BUS-480A supplies CHGR-2A.",
    "CHGR-2A--125 VDC TRAIN A": "Charger output lands on the Train A 125 VDC bus.",
    "BAT-125A--125 VDC TRAIN A": "Battery BAT-125A lands directly on the Train A 125 VDC bus.",
    "125 VDC TRAIN A--INV-2A": "Train A 125 VDC bus feeds inverter INV-2A.",
    "INV-2A--BUS-120AC-A": "INV-2A AC output lands on BUS-120AC-A.",
    "125 VDC TRAIN A--RELAY-86A": "Dashed control lead terminates at the Train A DC bus and RELAY-86A.",
    "BUS-120AC-A--RPS-PNL-A": "BUS-120AC-A has a solid vertical feed to RPS-PNL-A.",
    "RPS-PNL-A--RELAY-27A": "Dashed control connection runs between RPS-PNL-A and RELAY-27A.",
    "BUS-480B--CB-401B": "BUS-480B feeder enters CB-401B.",
    "CB-401B--MCC-2B1": "CB-401B output enters MCC-2B1.",
    "MCC-2B1--PUMP-RHR2B": "MCC-2B1 bucket 01 feeder 2B-F1 drops to PUMP-RHR2B.",
    "MCC-2B1--PUMP-CCW2B": "MCC-2B1 bucket 02 feeder 2B-F2 drops to PUMP-CCW2B.",
    "MCC-2B1--PUMP-SW2B": "MCC-2B1 bucket 03 feeder 2B-F3 drops to PUMP-SW2B.",
    "MCC-2B1--FAN-CR2B": "MCC-2B1 bucket 04 feeder 2B-F4 drops to FAN-CR2B.",
    "MCC-2B1--MOV-RHR142B": "MCC-2B1 bucket 05 feeder 2B-F5 drops to MOV-RHR142B.",
    "MCC-2B1--MOV-SI222B": "MCC-2B1 bucket 06 feeder 2B-F6 drops to MOV-SI222B.",
    "BUS-480B--TR-CPT-B": "A solid feeder from BUS-480B drops to TR-CPT-B.",
    "BUS-480B--CHGR-2B": "A separate solid feeder from BUS-480B supplies CHGR-2B.",
    "TR-CPT-B--BUS-120AC-B": "TR-CPT-B secondary visibly lands on BUS-120AC-B.",
    "CHGR-2B--125 VDC TRAIN B": "Charger output lands on the Train B 125 VDC bus.",
    "BAT-125B--125 VDC TRAIN B": "Battery BAT-125B lands directly on the Train B 125 VDC bus.",
    "125 VDC TRAIN B--INV-2B": "Train B 125 VDC bus feeds inverter INV-2B.",
    "INV-2B--BUS-120AC-B": "INV-2B AC output lands on BUS-120AC-B.",
    "125 VDC TRAIN B--RELAY-86B": "Dashed control lead terminates at the Train B DC bus and RELAY-86B.",
    "BUS-120AC-B--RPS-PNL-B": "BUS-120AC-B has a solid vertical feed to RPS-PNL-B.",
    "BUS-120AC-B--RELAY-27B": "RELAY-27B is visibly tied at the BUS-120AC-B junction.",
    "RPS-PNL-B--RELAY-27B": "Dashed control connection runs between RPS-PNL-B and RELAY-27B.",
}


REJECTED_ITEMS = [
    ("TO UNIT AUX BUS CONT.", "Off-sheet continuation box, not retained as a matrix component."),
    ("MCC-2A1-01..06", "MCC bucket/local-disconnect numbers were folded into MCC-to-load edges."),
    ("MCC-2B1-01..06", "MCC bucket/local-disconnect numbers were folded into MCC-to-load edges."),
    ("2A-C72/2A-C86/2B-C72/2B-C86", "Dashed cable-route labels, not components."),
    ("ESF DIESEL A/B", "Area/enclosure text labels; actual electrical nodes are DG-2A and DG-2B."),
    ("GND-STA", "Station ground reference symbol only; not a visible direct electrical connection to a retained component."),
    ("TR-CPT-A--BUS-120AC-A", "A-side transformer secondary ends at an isolated dot/gap and does not visibly land on BUS-120AC-A."),
    ("BUS-120AC-A--RELAY-27A", "No visible BUS-120AC-A tap to RELAY-27A; RELAY-27A is only dashed to RPS-PNL-A."),
]


TOKEN_ROWS = [
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "main-setup-crops-and-raw-inspection",
        "agent": "Main",
        "purpose": "Read task, verify raw-only scope, create crop script, inspect raw image/crops.",
        "model_call_count": 2,
        "input_tokens_expected": 13500,
        "input_tokens_low": 9500,
        "input_tokens_high": 19000,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 1500,
        "output_tokens_low": 900,
        "output_tokens_high": 2600,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 6500,
        "actual_usage_available": "no",
        "usage_source": "Codex transcript does not expose per-response usage objects in this environment.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "diego-round-01-high-recall",
        "agent": "Diego",
        "purpose": "High-recall extraction from raw sheet and raw-only crops.",
        "model_call_count": 1,
        "input_tokens_expected": 18500,
        "input_tokens_low": 13500,
        "input_tokens_high": 26000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 5200,
        "output_tokens_low": 3500,
        "output_tokens_high": 8000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 11500,
        "actual_usage_available": "no",
        "usage_source": "Estimated from prompt size, local-image payload count, and response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "jennifer-round-02-precision",
        "agent": "Jennifer",
        "purpose": "Precision review of Diego's proposal and pruning of unsupported nodes/edges.",
        "model_call_count": 1,
        "input_tokens_expected": 23000,
        "input_tokens_low": 16500,
        "input_tokens_high": 32000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 4600,
        "output_tokens_low": 3100,
        "output_tokens_high": 7200,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 13000,
        "actual_usage_available": "no",
        "usage_source": "Estimated from Diego proposal, image/crop payloads, and reviewer response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "diego-round-03-saturation",
        "agent": "Diego",
        "purpose": "Check Jennifer's refined matrix and confirm or contest saturation.",
        "model_call_count": 1,
        "input_tokens_expected": 13000,
        "input_tokens_low": 9000,
        "input_tokens_high": 18500,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 1100,
        "output_tokens_low": 600,
        "output_tokens_high": 2000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from compact saturation prompt and response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "jennifer-round-04-final",
        "agent": "Jennifer",
        "purpose": "Final confirmation of normalized node names and saturated edge set.",
        "model_call_count": 1,
        "input_tokens_expected": 10500,
        "input_tokens_low": 7500,
        "input_tokens_high": 15000,
        "cached_input_tokens_expected": 2500,
        "output_tokens_expected": 700,
        "output_tokens_low": 250,
        "output_tokens_high": 1200,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from final-confirmation payload and response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "main-output-generation-and-finalization",
        "agent": "Main",
        "purpose": "Write matrices, edge lists, validation JSON, notes, and token tracking.",
        "model_call_count": 2,
        "input_tokens_expected": 16000,
        "input_tokens_low": 11000,
        "input_tokens_high": 23500,
        "cached_input_tokens_expected": 5500,
        "output_tokens_expected": 5800,
        "output_tokens_low": 3800,
        "output_tokens_high": 9300,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from artifact-generation context, source text, and final response.",
    },
]


def edge_key(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


def display_key(edge: tuple[str, str]) -> str:
    return "--".join(edge)


def unique_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = set()
    ordered = []
    for edge in edges:
        key = edge_key(edge)
        if key not in seen:
            seen.add(key)
            ordered.append(edge)
    return ordered


def matrix_for(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in unique_edges(edges):
        if a not in idx or b not in idx:
            raise ValueError(f"Unknown edge endpoint: {a!r}, {b!r}")
        if a == b:
            raise ValueError(f"Unexpected self-loop: {a}")
        i, j = idx[a], idx[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = matrix_for(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for edge in unique_edges(edges):
            evidence = EDGE_EVIDENCE.get(display_key(edge), "")
            writer.writerow([edge[0], edge[1], evidence])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "component"])
        for i, node in enumerate(nodes, start=1):
            writer.writerow([i, node])


def token_totals(row: dict[str, object], tier: str) -> int:
    return (
        int(row[f"input_tokens_{tier}"])
        + int(row[f"output_tokens_{tier}"])
        + int(row["image_file_input_tokens_expected"])
    )


def write_token_files() -> dict[str, object]:
    fields = [
        "document",
        "iteration",
        "call_id",
        "agent",
        "purpose",
        "model_call_count",
        "input_tokens_expected",
        "input_tokens_low",
        "input_tokens_high",
        "cached_input_tokens_expected",
        "output_tokens_expected",
        "output_tokens_low",
        "output_tokens_high",
        "reasoning_tokens_expected",
        "image_file_input_tokens_expected",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_available",
        "usage_source",
    ]
    enriched = []
    for row in TOKEN_ROWS:
        item = dict(row)
        item["total_tokens_low"] = token_totals(row, "low")
        item["total_tokens_expected"] = token_totals(row, "expected")
        item["total_tokens_high"] = token_totals(row, "high")
        enriched.append(item)

    for filename in (
        "token_performance_tracking.csv",
        "token_performance_traking.csv",
        "token_usage_estimates_by_call.csv",
    ):
        with (RESULTS_DIR / filename).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(enriched)

    summary_fields = [
        "document",
        "iteration",
        "model_call_count",
        "input_tokens_low",
        "input_tokens_expected",
        "input_tokens_high",
        "cached_input_tokens_expected",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "image_file_input_tokens_expected",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_available",
    ]
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "model_call_count": sum(int(r["model_call_count"]) for r in enriched),
        "input_tokens_low": sum(int(r["input_tokens_low"]) for r in enriched),
        "input_tokens_expected": sum(int(r["input_tokens_expected"]) for r in enriched),
        "input_tokens_high": sum(int(r["input_tokens_high"]) for r in enriched),
        "cached_input_tokens_expected": sum(int(r["cached_input_tokens_expected"]) for r in enriched),
        "output_tokens_low": sum(int(r["output_tokens_low"]) for r in enriched),
        "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in enriched),
        "output_tokens_high": sum(int(r["output_tokens_high"]) for r in enriched),
        "image_file_input_tokens_expected": sum(int(r["image_file_input_tokens_expected"]) for r in enriched),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in enriched),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in enriched),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in enriched),
        "actual_usage_available": "no",
    }
    with (RESULTS_DIR / "token_usage_summary_by_document.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerow(summary)

    manifest = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "responses_input_token_count_endpoint": {
            "attempted": False,
            "reason": "OPENAI_API_KEY was not available, so no authenticated Responses input-token counting request could be made.",
        },
        "actual_usage_collection": {
            "available": False,
            "reason": "Main-agent and subagent per-response usage objects are not exposed through the available Codex tools in this session.",
        },
        "estimate_method": "Low/expected/high estimates are based on visible prompt and response sizes, local image/crop payload count, and typical image-token accounting ranges. Reasoning token counts were not available.",
        "summary_totals": summary,
    }
    (RESULTS_DIR / "responses_input_token_count_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return summary


def validate(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, object]:
    final_edges = unique_edges(edges)
    matrix = matrix_for(nodes, final_edges)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    degree = {node: sum(row) for node, row in zip(nodes, matrix)}
    return {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "raw_image": str(RAW_IMAGE),
        "node_count": len(nodes),
        "edge_count": len(final_edges),
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "duplicate_final_edges_removed": len(edges) - len(final_edges),
        "unknown_endpoint_count": 0,
        "degree_by_node": degree,
        "round_edge_counts": [
            {
                "round": r["round"],
                "agent": r["agent"],
                "label": r["label"],
                "node_count": len(r["nodes"]),
                "edge_count": len(unique_edges(r["edges"])),
            }
            for r in ROUND_DEFINITIONS
        ],
    }


def write_round_files() -> None:
    with (RESULTS_DIR / "all_rounds_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["round", "agent", "label", "node_count", "edge_count", "comment"])
        for r in ROUND_DEFINITIONS:
            writer.writerow([
                r["round"],
                r["agent"],
                r["label"],
                len(r["nodes"]),
                len(unique_edges(r["edges"])),
                r["comment"],
            ])
    for r in ROUND_DEFINITIONS:
        stem = f"round_{int(r['round']):02d}_{str(r['agent']).lower()}_{r['label']}"
        write_nodes(RESULTS_DIR / f"{stem}_nodes.csv", r["nodes"])
        write_matrix(RESULTS_DIR / f"{stem}_matrix.csv", r["nodes"], r["edges"])
        write_edges(RESULTS_DIR / f"{stem}_edges.csv", r["edges"])


def write_graph_json(validation: dict[str, object]) -> None:
    graph = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "nodes": [{"id": node, "index": i} for i, node in enumerate(FINAL_NODES, start=1)],
        "edges": [
            {
                "source": a,
                "target": b,
                "evidence": EDGE_EVIDENCE.get(display_key((a, b)), ""),
            }
            for a, b in unique_edges(FINAL_EDGES)
        ],
        "rejected_items": [
            {"item": item, "reason": reason}
            for item, reason in REJECTED_ITEMS
        ],
        "validation": validation,
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")


def write_note(validation: dict[str, object], token_summary: dict[str, object]) -> None:
    lines = [
        "# Extraction Note - Document 38",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Scope",
        "",
        "Only the raw schematic image and crops generated from that raw image were used. Sibling derived folders and any ground-truth resources were not inspected.",
        "",
        "## Final Connectivity",
        "",
        f"- Nodes: {validation['node_count']}",
        f"- Edges: {validation['edge_count']}",
        f"- Symmetric matrix: {validation['symmetric']}",
        f"- Diagonal zero: {validation['diagonal_zero']}",
        "",
        "## Multi-Agent Rounds",
        "",
    ]
    for r in ROUND_DEFINITIONS:
        lines.append(f"- Round {r['round']} ({r['agent']}, {r['label']}): {len(r['nodes'])} nodes, {len(unique_edges(r['edges']))} edges. {r['comment']}")

    lines.extend([
        "",
        "## Precision Decisions",
        "",
        "The final graph excludes off-sheet continuation boxes, route-label text, MCC bucket numbers, ESF area labels, and station ground because those did not constitute supported retained component nodes in the raw schematic.",
        "",
    ])
    for item, reason in REJECTED_ITEMS:
        lines.append(f"- Rejected {item}: {reason}")

    lines.extend([
        "",
        "## Final Edges",
        "",
    ])
    for a, b in unique_edges(FINAL_EDGES):
        evidence = EDGE_EVIDENCE.get(display_key((a, b)), "")
        lines.append(f"- {a} -- {b}: {evidence}")

    lines.extend([
        "",
        "## Token Performance Tracking",
        "",
        "Actual per-response usage objects and reasoning-token counts were not exposed through the available Codex/subagent tools. OPENAI_API_KEY was not available, so the OpenAI Responses input-token counting endpoint could not be called for planned payloads. The CSVs therefore contain low/expected/high estimates and mark actual usage unavailable.",
        "",
        f"- Estimated total tokens low: {token_summary['total_tokens_low']}",
        f"- Estimated total tokens expected: {token_summary['total_tokens_expected']}",
        f"- Estimated total tokens high: {token_summary['total_tokens_high']}",
        "",
        "Detailed token rows are in token_performance_tracking.csv and token_usage_estimates_by_call.csv. The misspelled compatibility file token_performance_traking.csv is also written.",
        "",
    ])
    (RESULTS_DIR / "extraction_note.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_nodes(RESULTS_DIR / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS_DIR / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_round_files()
    validation = validate(FINAL_NODES, FINAL_EDGES)
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    write_graph_json(validation)
    token_summary = write_token_files()
    write_note(validation, token_summary)
    print(f"Wrote outputs to {RESULTS_DIR}")
    print(f"Final nodes: {validation['node_count']}")
    print(f"Final edges: {validation['edge_count']}")
    print(f"Symmetric: {validation['symmetric']}")
    print(f"Diagonal zero: {validation['diagonal_zero']}")
    print(f"Estimated total tokens expected: {token_summary['total_tokens_expected']}")


if __name__ == "__main__":
    main()
