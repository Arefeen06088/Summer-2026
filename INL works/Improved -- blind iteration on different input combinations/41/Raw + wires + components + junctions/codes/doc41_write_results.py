from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path


DOCUMENT = "41"
ITERATION = "1"
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"

SOURCE_FILES = [
    "raw -- synthetic_npp_electrical_schematic(2).png",
    "detected_components_and_logical_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
    "wire_nodes.csv",
    "wire_nodes_overlay.png",
]


DIEGO_R1_NODES = [
    "161 kV OFFSITE A",
    "TR-1A SU 13.8/4.16",
    "GND-1E",
    "CB-101",
    "BUS-1A 4.16 kV",
    "EDG-1A 4160 V",
    "CB-105",
    "CB-TIE 1AB",
    "BUS-1B 4.16 kV",
    "CB-102",
    "TR-1B SU 13.8/4.16",
    "161 kV OFFSITE B",
    "EDG-1B 4160 V",
    "CB-106",
    "EDG A INCOMING",
    "EDG B INCOMING",
    "CTRL-86A",
    "CTRL-86B",
    "RELAY-K86A",
    "RELAY-K86B",
    "PANEL-RPS-A",
    "PANEL-RPS-B",
    "JB-ESF-01",
    "TB1",
    "TR-LC-1A 4.16/0.48",
    "TR-LC-1B 4.16/0.48",
    "TR-SAF-1A CLASS 1E",
    "TR-SAF-1B CLASS 1E",
    "CB-201",
    "CB-202",
    "CB-203",
    "CB-204",
    "BUS-480A",
    "BUS-480B",
    "BUS-480E1A",
    "BUS-480E1B",
    "MCC-1A",
    "MCC-1B",
    "MCC-1C",
    "MCC-1D",
    "MCC-ESS-A",
    "MCC-ESS-B",
    "PUMP-CCW-103A",
    "PUMP-CCW-103B",
    "FAN-CRHV-104A",
    "FAN-CRHV-104B",
    "PUMP-SI-101A",
    "PUMP-SI-101B",
    "PUMP-RHR-102A",
    "PUMP-RHR-102B",
    "MOV-1201A",
    "MOV-1201B",
    "CHGR-125A",
    "CHGR-125B",
    "BAT-125A",
    "BAT-125B",
    "DC-BUS-125A",
    "DC-BUS-125B",
    "INV-120A",
    "INV-120B",
    "UPS-BUS-A",
    "UPS-BUS-B",
    "INST-RACK-1",
    "PT",
    "UV",
    "SEQ",
    "CABLE 1A-480-7",
    "CABLE 1B-480-9",
    "FDR A-DC",
    "FDR B-DC",
]

DIEGO_R1_EDGES = [
    ("161 kV OFFSITE A", "TR-1A SU 13.8/4.16"),
    ("TR-1A SU 13.8/4.16", "GND-1E"),
    ("TR-1A SU 13.8/4.16", "CB-101"),
    ("CB-101", "BUS-1A 4.16 kV"),
    ("EDG-1A 4160 V", "CB-105"),
    ("CB-105", "BUS-1A 4.16 kV"),
    ("BUS-1A 4.16 kV", "CB-TIE 1AB"),
    ("CB-TIE 1AB", "BUS-1B 4.16 kV"),
    ("BUS-1B 4.16 kV", "CB-102"),
    ("CB-102", "TR-1B SU 13.8/4.16"),
    ("TR-1B SU 13.8/4.16", "161 kV OFFSITE B"),
    ("EDG-1B 4160 V", "CB-106"),
    ("CB-106", "BUS-1B 4.16 kV"),
    ("BUS-1A 4.16 kV", "TR-LC-1A 4.16/0.48"),
    ("BUS-1A 4.16 kV", "TR-SAF-1A CLASS 1E"),
    ("BUS-1B 4.16 kV", "TR-LC-1B 4.16/0.48"),
    ("BUS-1B 4.16 kV", "TR-SAF-1B CLASS 1E"),
    ("TR-LC-1A 4.16/0.48", "CB-201"),
    ("CB-201", "BUS-480A"),
    ("TR-SAF-1A CLASS 1E", "CB-203"),
    ("CB-203", "BUS-480E1A"),
    ("TR-LC-1B 4.16/0.48", "CB-202"),
    ("CB-202", "BUS-480B"),
    ("TR-SAF-1B CLASS 1E", "CB-204"),
    ("CB-204", "BUS-480E1B"),
    ("BUS-480A", "MCC-1A"),
    ("BUS-480A", "MCC-1C"),
    ("MCC-1A", "PUMP-CCW-103A"),
    ("MCC-1C", "FAN-CRHV-104A"),
    ("BUS-480A", "CHGR-125A"),
    ("BUS-480E1A", "MCC-ESS-A"),
    ("MCC-ESS-A", "PUMP-SI-101A"),
    ("MCC-ESS-A", "PUMP-RHR-102A"),
    ("MCC-ESS-A", "MOV-1201A"),
    ("BUS-480B", "MCC-1B"),
    ("BUS-480B", "MCC-1D"),
    ("MCC-1B", "PUMP-CCW-103B"),
    ("MCC-1D", "FAN-CRHV-104B"),
    ("BUS-480B", "CHGR-125B"),
    ("BUS-480E1B", "MCC-ESS-B"),
    ("MCC-ESS-B", "PUMP-SI-101B"),
    ("MCC-ESS-B", "PUMP-RHR-102B"),
    ("MCC-ESS-B", "MOV-1201B"),
    ("CHGR-125A", "DC-BUS-125A"),
    ("BAT-125A", "DC-BUS-125A"),
    ("DC-BUS-125A", "INV-120A"),
    ("INV-120A", "UPS-BUS-A"),
    ("UPS-BUS-A", "PANEL-RPS-A"),
    ("UPS-BUS-A", "INST-RACK-1"),
    ("CHGR-125B", "DC-BUS-125B"),
    ("BAT-125B", "DC-BUS-125B"),
    ("DC-BUS-125B", "INV-120B"),
    ("INV-120B", "UPS-BUS-B"),
    ("UPS-BUS-B", "PANEL-RPS-B"),
    ("CB-105", "CTRL-86A"),
    ("CTRL-86A", "RELAY-K86A"),
    ("RELAY-K86A", "PANEL-RPS-A"),
    ("CB-106", "CTRL-86B"),
    ("CTRL-86B", "RELAY-K86B"),
    ("RELAY-K86B", "PANEL-RPS-B"),
    ("JB-ESF-01", "PANEL-RPS-A"),
    ("JB-ESF-01", "PANEL-RPS-B"),
    ("JB-ESF-01", "TB1"),
    ("INST-RACK-1", "PT"),
    ("INST-RACK-1", "UV"),
    ("INST-RACK-1", "SEQ"),
]


FINAL_NODES = [
    "OFFSITE-A",
    "OFFSITE-B",
    "TR-1A",
    "TR-1B",
    "GND-1E",
    "CB-101",
    "CB-102",
    "CB-TIE-1AB",
    "BUS-1A-4.16KV",
    "BUS-1B-4.16KV",
    "EDG-1A",
    "EDG-1B",
    "CB-105",
    "CB-106",
    "RELAY-K86A",
    "RELAY-K86B",
    "PANEL-RPS-A",
    "PANEL-RPS-B",
    "JB-ESF-01",
    "TR-LC-1A",
    "TR-LC-1B",
    "TR-SAF-1A",
    "TR-SAF-1B",
    "CB-201",
    "CB-202",
    "CB-203",
    "CB-204",
    "BUS-480A",
    "BUS-480B",
    "BUS-480E1A",
    "BUS-480E1B",
    "MCC-1A",
    "MCC-1B",
    "MCC-1C",
    "MCC-1D",
    "MCC-ESS-A",
    "MCC-ESS-B",
    "PUMP-CCW-103A",
    "PUMP-CCW-103B",
    "FAN-CRHV-104A",
    "FAN-CRHV-104B",
    "PUMP-SI-101A",
    "PUMP-SI-101B",
    "PUMP-RHR-102A",
    "PUMP-RHR-102B",
    "MOV-1201A",
    "MOV-1201B",
    "CHGR-125A",
    "CHGR-125B",
    "BAT-125A",
    "BAT-125B",
    "DC-BUS-125A",
    "DC-BUS-125B",
    "INV-120A",
    "INV-120B",
    "UPS-BUS-A",
    "UPS-BUS-B",
    "INST-RACK-1",
]


FINAL_EDGES = [
    ("OFFSITE-A", "TR-1A", "power_feeder", "high", "solid offsite A feeder to TR-1A"),
    ("TR-1A", "GND-1E", "grounding", "high", "grounding conductor and ground symbol below TR-1A"),
    ("TR-1A", "CB-101", "power_feeder", "high", "TR-1A secondary to CB-101"),
    ("CB-101", "BUS-1A-4.16KV", "power_feeder", "high", "CB-101 output to BUS-1A"),
    ("EDG-1A", "CB-105", "power_feeder", "high", "EDG-1A feeder to CB-105"),
    ("CB-105", "BUS-1A-4.16KV", "power_feeder", "high", "CB-105 incoming feeder rises to BUS-1A"),
    ("BUS-1A-4.16KV", "CB-TIE-1AB", "power_feeder", "high", "bus tie from right end of BUS-1A"),
    ("CB-TIE-1AB", "BUS-1B-4.16KV", "power_feeder", "high", "normally-open tie to BUS-1B"),
    ("BUS-1B-4.16KV", "CB-102", "power_feeder", "high", "BUS-1B right terminal to CB-102"),
    ("CB-102", "TR-1B", "power_feeder", "high", "CB-102 to TR-1B"),
    ("TR-1B", "OFFSITE-B", "power_feeder", "high", "TR-1B primary to offsite B source"),
    ("EDG-1B", "CB-106", "power_feeder", "high", "EDG-1B feeder to CB-106"),
    ("CB-106", "BUS-1B-4.16KV", "power_feeder", "high", "CB-106 incoming feeder rises to BUS-1B"),
    ("BUS-1A-4.16KV", "TR-LC-1A", "power_feeder", "high", "vertical drop from BUS-1A"),
    ("BUS-1A-4.16KV", "TR-SAF-1A", "power_feeder", "high", "vertical drop from BUS-1A"),
    ("BUS-1B-4.16KV", "TR-LC-1B", "power_feeder", "high", "vertical drop from BUS-1B"),
    ("BUS-1B-4.16KV", "TR-SAF-1B", "power_feeder", "high", "vertical drop from BUS-1B"),
    ("TR-LC-1A", "CB-201", "power_feeder", "high", "transformer secondary to CB-201"),
    ("CB-201", "BUS-480A", "power_feeder", "high", "CB-201 output to BUS-480A"),
    ("TR-SAF-1A", "CB-203", "power_feeder", "high", "transformer secondary to CB-203"),
    ("CB-203", "BUS-480E1A", "power_feeder", "high", "CB-203 output to BUS-480E1A"),
    ("TR-LC-1B", "CB-202", "power_feeder", "high", "transformer secondary to CB-202"),
    ("CB-202", "BUS-480B", "power_feeder", "high", "CB-202 output to BUS-480B"),
    ("TR-SAF-1B", "CB-204", "power_feeder", "high", "transformer secondary to CB-204"),
    ("CB-204", "BUS-480E1B", "power_feeder", "high", "CB-204 output to BUS-480E1B"),
    ("BUS-480A", "MCC-1A", "power_feeder", "high", "vertical feeder from BUS-480A"),
    ("BUS-480A", "MCC-1C", "power_feeder", "high", "vertical feeder from BUS-480A"),
    ("BUS-480A", "CHGR-125A", "power_feeder", "high", "left feeder/cable callout from BUS-480A to charger"),
    ("BUS-480E1A", "MCC-ESS-A", "power_feeder", "high", "vertical feeder from BUS-480E1A"),
    ("MCC-1A", "PUMP-CCW-103A", "power_feeder", "high", "MCC output to pump"),
    ("MCC-1C", "FAN-CRHV-104A", "power_feeder", "high", "MCC output to fan"),
    ("MCC-ESS-A", "PUMP-SI-101A", "power_feeder", "high", "MCC-ESS-A output to pump"),
    ("MCC-ESS-A", "PUMP-RHR-102A", "power_feeder", "high", "MCC-ESS-A output to pump"),
    ("MCC-ESS-A", "MOV-1201A", "power_feeder", "high", "MCC-ESS-A output to MOV"),
    ("BUS-480B", "MCC-1B", "power_feeder", "high", "vertical feeder from BUS-480B"),
    ("BUS-480B", "MCC-1D", "power_feeder", "high", "vertical feeder from BUS-480B"),
    ("BUS-480E1B", "MCC-ESS-B", "power_feeder", "high", "vertical feeder from BUS-480E1B"),
    ("BUS-480E1B", "CHGR-125B", "power_feeder", "medium", "right-side cable 1B-480-9 appears to land on BUS-480E1B"),
    ("MCC-1B", "PUMP-CCW-103B", "power_feeder", "high", "MCC output to pump"),
    ("MCC-1D", "FAN-CRHV-104B", "power_feeder", "high", "MCC output to fan"),
    ("MCC-ESS-B", "PUMP-SI-101B", "power_feeder", "high", "MCC-ESS-B output to pump"),
    ("MCC-ESS-B", "PUMP-RHR-102B", "power_feeder", "high", "MCC-ESS-B output to pump"),
    ("MCC-ESS-B", "MOV-1201B", "power_feeder", "high", "MCC-ESS-B output to MOV"),
    ("CHGR-125A", "DC-BUS-125A", "dc_power", "high", "charger output to DC bus"),
    ("BAT-125A", "DC-BUS-125A", "dc_power", "high", "battery connected to DC bus"),
    ("DC-BUS-125A", "INV-120A", "dc_power", "high", "DC bus feeds inverter"),
    ("INV-120A", "UPS-BUS-A", "ac_power", "high", "inverter output to UPS bus"),
    ("UPS-BUS-A", "PANEL-RPS-A", "ac_power", "medium", "UPS A feeder to RPS panel"),
    ("UPS-BUS-A", "INST-RACK-1", "instrument_power", "high", "UPS A feeder to instrument rack"),
    ("CHGR-125B", "DC-BUS-125B", "dc_power", "high", "charger output to DC bus"),
    ("BAT-125B", "DC-BUS-125B", "dc_power", "high", "battery connected to DC bus"),
    ("DC-BUS-125B", "INV-120B", "dc_power", "high", "DC bus feeds inverter"),
    ("INV-120B", "UPS-BUS-B", "ac_power", "high", "inverter output to UPS bus"),
    ("UPS-BUS-B", "PANEL-RPS-B", "ac_power", "medium", "UPS B feeder to RPS panel"),
    ("CB-105", "RELAY-K86A", "control_interlock", "high", "dashed control circuit from CB-105 to K86A relay path"),
    ("RELAY-K86A", "PANEL-RPS-A", "control_interlock", "high", "dashed relay-to-panel interlock"),
    ("CB-106", "RELAY-K86B", "control_interlock", "high", "dashed control circuit from CB-106 to K86B relay path"),
    ("RELAY-K86B", "PANEL-RPS-B", "control_interlock", "high", "dashed relay-to-panel interlock"),
    ("JB-ESF-01", "PANEL-RPS-A", "control_interlock", "medium", "dashed wiring between junction box and RPS-A area"),
    ("JB-ESF-01", "PANEL-RPS-B", "control_interlock", "medium", "dashed wiring between junction box and RPS-B area"),
]


EXCLUSIONS = [
    ("EDG A INCOMING", "feeder/callout label, not a component node"),
    ("EDG B INCOMING", "feeder/callout label, not a component node"),
    ("CTRL-86A", "control circuit label; collapsed to CB-105--RELAY-K86A"),
    ("CTRL-86B", "control circuit label; collapsed to CB-106--RELAY-K86B"),
    ("CABLE 1A-480-7", "cable callout used as evidence, not a node"),
    ("CABLE 1B-480-9", "cable callout used as evidence, not a node"),
    ("FDR A-DC", "feeder label used as evidence, not a node"),
    ("FDR B-DC", "feeder label used as evidence, not a node"),
    ("TB1", "terminal label internal to JB-ESF-01"),
    ("PT", "internal function inside INST-RACK-1"),
    ("UV", "internal function inside INST-RACK-1"),
    ("SEQ", "internal function inside INST-RACK-1"),
    ("BUS-480B--CHGR-125B", "excluded; final review supports BUS-480E1B--CHGR-125B instead"),
    ("INST-RACK-1--PT/UV/SEQ", "excluded as internal annotations without separate external terminals"),
    ("JB-ESF-01--TB1", "excluded as an internal terminal annotation"),
]


ROUND_DEFINITIONS = [
    {
        "round": "round_01_diego",
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "candidate graph; intentionally retained plausible labels/internal symbols",
        "nodes": DIEGO_R1_NODES,
        "edges": [(a, b, "candidate", "high_recall", "Diego round 1 plausible visual/geometric connection") for a, b in DIEGO_R1_EDGES],
    },
    {
        "round": "round_02_jennifer",
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "status": "refined graph; removed callouts/internal annotations and corrected B charger feed",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_03_diego",
        "agent": "Diego",
        "role": "convergence reviewer",
        "status": "agreed with Jennifer round 2 unchanged",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_04_jennifer_final",
        "agent": "Jennifer",
        "role": "final saturation reviewer",
        "status": "SATURATED: final graph is Jennifer round 2 unchanged",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
]


TOKEN_CALLS = [
    {
        "model_call": "main-01-orchestration-and-visual-prep",
        "caller": "main agent",
        "round": "prep",
        "input_tokens_est": 7000,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 500,
        "output_tokens_expected": 900,
        "output_tokens_high": 1500,
        "reasoning_tokens_low": 800,
        "reasoning_tokens_expected": 1500,
        "reasoning_tokens_high": 2600,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "filesystem inspection, crop planning, visual triage",
    },
    {
        "model_call": "subagent-diego-01-high-recall",
        "caller": "Diego",
        "round": "round_01_diego",
        "input_tokens_est": 3200,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 11500,
        "output_tokens_low": 3500,
        "output_tokens_expected": 5000,
        "output_tokens_high": 6500,
        "reasoning_tokens_low": 1200,
        "reasoning_tokens_expected": 2500,
        "reasoning_tokens_high": 4500,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "raw image plus overlays/crops; high-recall graph with callout candidates",
    },
    {
        "model_call": "subagent-jennifer-02-precision-review",
        "caller": "Jennifer",
        "round": "round_02_jennifer",
        "input_tokens_est": 6500,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 9000,
        "output_tokens_low": 3500,
        "output_tokens_expected": 5300,
        "output_tokens_high": 7000,
        "reasoning_tokens_low": 1200,
        "reasoning_tokens_expected": 2200,
        "reasoning_tokens_high": 4000,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "reviewed Diego proposal and visual resources; refined final graph",
    },
    {
        "model_call": "subagent-diego-03-convergence",
        "caller": "Diego",
        "round": "round_03_diego",
        "input_tokens_est": 5600,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 3500,
        "output_tokens_low": 250,
        "output_tokens_expected": 600,
        "output_tokens_high": 1200,
        "reasoning_tokens_low": 500,
        "reasoning_tokens_expected": 1000,
        "reasoning_tokens_high": 1800,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "checked Jennifer corrections; agreed unchanged",
    },
    {
        "model_call": "subagent-jennifer-04-saturation",
        "caller": "Jennifer",
        "round": "round_04_jennifer_final",
        "input_tokens_est": 1200,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 20,
        "output_tokens_expected": 80,
        "output_tokens_high": 200,
        "reasoning_tokens_low": 50,
        "reasoning_tokens_expected": 200,
        "reasoning_tokens_high": 500,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "confirmed saturated graph unchanged",
    },
    {
        "model_call": "main-02-result-writing-and-final-report",
        "caller": "main agent",
        "round": "writeup",
        "input_tokens_est": 8000,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 700,
        "output_tokens_expected": 1300,
        "output_tokens_high": 2200,
        "reasoning_tokens_low": 900,
        "reasoning_tokens_expected": 1600,
        "reasoning_tokens_high": 3000,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "writes round matrices and summarizes final result",
    },
]


def edge_pairs(edges: list[tuple[str, str, str, str, str]]) -> list[tuple[str, str]]:
    return [(row[0], row[1]) for row in edges]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_matrix(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    node_set = set(nodes)
    missing = sorted({n for edge in edges for n in edge if n not in node_set})
    if missing:
        raise ValueError(f"Edges reference missing nodes: {missing}")
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        if a == b:
            matrix[idx[a]][idx[b]] = 1
        else:
            matrix[idx[a]][idx[b]] = 1
            matrix[idx[b]][idx[a]] = 1
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = build_matrix(nodes, edges)
    for i, row in enumerate(matrix):
        if row[i] != 0:
            raise ValueError(f"Unexpected nonzero diagonal for {nodes[i]}")
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                raise ValueError(f"Matrix is not symmetric at {nodes[i]} / {nodes[j]}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str, str, str, str]]) -> None:
    rows = [
        {
            "source": a,
            "target": b,
            "edge_type": edge_type,
            "confidence": confidence,
            "evidence": evidence,
        }
        for a, b, edge_type, confidence, evidence in edges
    ]
    write_csv(path, rows, ["source", "target", "edge_type", "confidence", "evidence"])


def total_for_call(call: dict[str, object], band: str) -> int:
    return int(call["input_tokens_est"]) + int(call["image_file_input_tokens_est"]) + int(call[f"output_tokens_{band}"]) + int(call[f"reasoning_tokens_{band}"])


def token_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for call in TOKEN_CALLS:
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": call["round"],
                "caller": call["caller"],
                "model_call": call["model_call"],
                "input_tokens_est": call["input_tokens_est"],
                "cached_input_tokens_est": call["cached_input_tokens_est"],
                "image_file_input_tokens_est": call["image_file_input_tokens_est"],
                "output_tokens_low": call["output_tokens_low"],
                "output_tokens_expected": call["output_tokens_expected"],
                "output_tokens_high": call["output_tokens_high"],
                "reasoning_tokens_low": call["reasoning_tokens_low"],
                "reasoning_tokens_expected": call["reasoning_tokens_expected"],
                "reasoning_tokens_high": call["reasoning_tokens_high"],
                "total_tokens_low": total_for_call(call, "low"),
                "total_tokens_expected": total_for_call(call, "expected"),
                "total_tokens_high": total_for_call(call, "high"),
                "usage_status": call["usage_status"],
                "counting_endpoint_status": call["counting_endpoint_status"],
                "notes": call["notes"],
            }
        )
    return rows


def write_token_files() -> dict[str, object]:
    rows = token_rows()
    fieldnames = [
        "document",
        "iteration",
        "round",
        "caller",
        "model_call",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_status",
        "counting_endpoint_status",
        "notes",
    ]
    write_csv(RESULTS / "token_usage_estimate.csv", rows, fieldnames)

    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "method": "local estimate because no API key was available for the OpenAI Responses input-token counting endpoint",
        "text_token_estimator": "approximate prompt/message token count derived from observed prompt sizes; fallback assumption is about 4 characters per token",
        "image_file_token_estimator": "standard high-detail vision tile heuristic applied qualitatively to raw/overlay/crop payloads",
        "usage_objects": "not exposed by the local Codex main/subagent tool responses",
        "calls": len(rows),
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in rows),
        "cached_input_tokens_est": sum(int(r["cached_input_tokens_est"]) for r in rows),
        "image_file_input_tokens_est": sum(int(r["image_file_input_tokens_est"]) for r in rows),
        "output_tokens_low": sum(int(r["output_tokens_low"]) for r in rows),
        "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in rows),
        "output_tokens_high": sum(int(r["output_tokens_high"]) for r in rows),
        "reasoning_tokens_low": sum(int(r["reasoning_tokens_low"]) for r in rows),
        "reasoning_tokens_expected": sum(int(r["reasoning_tokens_expected"]) for r in rows),
        "reasoning_tokens_high": sum(int(r["reasoning_tokens_high"]) for r in rows),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in rows),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in rows),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in rows),
    }
    write_csv(
        RESULTS / "token_usage_summary.csv",
        [summary],
        [
            "document",
            "iteration",
            "method",
            "text_token_estimator",
            "image_file_token_estimator",
            "usage_objects",
            "calls",
            "input_tokens_est",
            "cached_input_tokens_est",
            "image_file_input_tokens_est",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens_low",
            "reasoning_tokens_expected",
            "reasoning_tokens_high",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
        ],
    )
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_round_outputs() -> None:
    round_summary_rows = []
    for rd in ROUND_DEFINITIONS:
        prefix = rd["round"]
        nodes = list(rd["nodes"])
        edges = list(rd["edges"])
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edge_pairs(edges))
        write_csv(
            RESULTS / f"{prefix}_node_order.csv",
            [{"index": i, "node": node} for i, node in enumerate(nodes)],
            ["index", "node"],
        )
        round_summary_rows.append(
            {
                "round": prefix,
                "agent": rd["agent"],
                "role": rd["role"],
                "node_count": len(nodes),
                "edge_count": len(edges),
                "status": rd["status"],
            }
        )
    write_csv(
        RESULTS / "rounds_summary.csv",
        round_summary_rows,
        ["round", "agent", "role", "node_count", "edge_count", "status"],
    )


def write_final_outputs() -> None:
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, edge_pairs(FINAL_EDGES))
    write_csv(
        RESULTS / "final_node_order.csv",
        [{"index": i, "node": node} for i, node in enumerate(FINAL_NODES)],
        ["index", "node"],
    )
    write_csv(
        RESULTS / "uncertain_or_excluded_edges.csv",
        [{"item": item, "reason": reason} for item, reason in EXCLUSIONS],
        ["item", "reason"],
    )


def source_inventory() -> list[dict[str, object]]:
    rows = []
    for name in SOURCE_FILES:
        path = BASE / name
        rows.append(
            {
                "file": name,
                "exists": path.exists(),
                "bytes": path.stat().st_size if path.exists() else "",
            }
        )
    return rows


def write_report(token_summary: dict[str, object]) -> None:
    final_edges_text = "\n".join(f"- {a} -- {b} ({edge_type}, {confidence})" for a, b, edge_type, confidence, _ in FINAL_EDGES)
    exclusions_text = "\n".join(f"- {item}: {reason}" for item, reason in EXCLUSIONS)
    report = f"""# Document 41 Connectivity Extraction

## Scope

Only resources inside:

`{BASE}`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, or off-the-shelf OCR outputs were used. The extraction relied on visual inspection of the raw schematic plus the allowed wire/component/junction aids.

## Multi-Agent Rounds

1. Diego round 1: high-recall extraction with plausible labels/internal symbols retained.
2. Jennifer round 2: precision review; removed callouts/internal annotations and corrected the B charger feed.
3. Diego round 3: agreed with Jennifer unchanged.
4. Jennifer round 4: confirmed saturation unchanged.

## Final Result

- Final nodes: {len(FINAL_NODES)}
- Final undirected edges: {len(FINAL_EDGES)}
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`

## Final Edges

{final_edges_text}

## Excluded Or Collapsed Items

{exclusions_text}

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available in this environment. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: {token_summary["total_tokens_low"]}
- Estimated total expected: {token_summary["total_tokens_expected"]}
- Estimated total high: {token_summary["total_tokens_high"]}
- Estimated image/file input tokens: {token_summary["image_file_input_tokens_est"]}

Detailed call-level estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)

    write_csv(RESULTS / "source_inventory.csv", source_inventory(), ["file", "exists", "bytes"])
    write_round_outputs()
    write_final_outputs()
    token_summary = write_token_files()
    write_report(token_summary)

    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "base": str(BASE),
        "allowed_sources_only": True,
        "used_ground_truth": False,
        "used_ocr": False,
        "final_node_count": len(FINAL_NODES),
        "final_edge_count": len(FINAL_EDGES),
        "rounds": [
            {
                "round": rd["round"],
                "agent": rd["agent"],
                "role": rd["role"],
                "node_count": len(rd["nodes"]),
                "edge_count": len(rd["edges"]),
                "status": rd["status"],
            }
            for rd in ROUND_DEFINITIONS
        ],
        "token_summary": token_summary,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    shutil.copy2(Path(__file__), CODES / Path(__file__).name)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
