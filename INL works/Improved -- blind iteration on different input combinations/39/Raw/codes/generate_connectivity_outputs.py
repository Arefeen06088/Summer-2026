from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- npp_schematic_improved_no_overlap.png"
DOCUMENT = "39"
ITERATION = "1"


FINAL_NODES = [
    "OFFSITE 230 kV A",
    "DS-230A",
    "TR-1A 230/4.16",
    "CB-1A",
    "EDG-1A",
    "CB-DG-A",
    "BUS-4160-A DIV I 4.16 kV ESF",
    "RELAY-UV-A 27/59",
    "CB-TIE-AB",
    "BUS-4160-B DIV II 4.16 kV ESF",
    "RELAY-UV-B 27/59",
    "OFFSITE 230 kV B",
    "DS-230B",
    "TR-1B 230/4.16",
    "CB-1B",
    "EDG-1B",
    "CB-DG-B",
    "TR-480-A 4.16/0.48",
    "CB-480-A",
    "BUS-480-A 480 V LOAD CENTER A",
    "GND-PLANT",
    "MCC-A1 SAFETY LOADS",
    "PUMP-RHR-A RHR A",
    "PUMP-CS-A CORE SPRAY",
    "MCC-A2 VALVE/PUMP",
    "PUMP-CCW-A CCW A",
    "MOV-881A",
    "MOV-742A",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "PANEL-120A",
    "RPS-A DIV I",
    "RELAY-KA1",
    "JB-A101",
    "TR-480-B 4.16/0.48",
    "CB-480-B",
    "BUS-480-B 480 V LOAD CENTER B",
    "MCC-B1 SAFETY LOADS",
    "PUMP-RHR-B RHR B",
    "PUMP-CS-B CORE SPRAY",
    "MCC-B2 VALVE/PUMP",
    "PUMP-CCW-B CCW B",
    "MOV-881B",
    "MOV-742B",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "PANEL-120B",
    "RPS-B DIV II",
    "RELAY-KB1",
    "JB-B101",
    "ANN-CR01",
    "REC-SOE01",
]


FINAL_EDGES = [
    ("OFFSITE 230 kV A", "DS-230A"),
    ("DS-230A", "TR-1A 230/4.16"),
    ("TR-1A 230/4.16", "CB-1A"),
    ("CB-1A", "BUS-4160-A DIV I 4.16 kV ESF"),
    ("EDG-1A", "CB-DG-A"),
    ("CB-DG-A", "BUS-4160-A DIV I 4.16 kV ESF"),
    ("BUS-4160-A DIV I 4.16 kV ESF", "RELAY-UV-A 27/59"),
    ("BUS-4160-A DIV I 4.16 kV ESF", "CB-TIE-AB"),
    ("CB-TIE-AB", "BUS-4160-B DIV II 4.16 kV ESF"),
    ("BUS-4160-B DIV II 4.16 kV ESF", "RELAY-UV-B 27/59"),
    ("OFFSITE 230 kV B", "DS-230B"),
    ("DS-230B", "TR-1B 230/4.16"),
    ("TR-1B 230/4.16", "CB-1B"),
    ("CB-1B", "BUS-4160-B DIV II 4.16 kV ESF"),
    ("EDG-1B", "CB-DG-B"),
    ("CB-DG-B", "BUS-4160-B DIV II 4.16 kV ESF"),
    ("BUS-4160-A DIV I 4.16 kV ESF", "TR-480-A 4.16/0.48"),
    ("TR-480-A 4.16/0.48", "CB-480-A"),
    ("CB-480-A", "BUS-480-A 480 V LOAD CENTER A"),
    ("BUS-480-A 480 V LOAD CENTER A", "MCC-A1 SAFETY LOADS"),
    ("BUS-480-A 480 V LOAD CENTER A", "MCC-A2 VALVE/PUMP"),
    ("BUS-480-A 480 V LOAD CENTER A", "GND-PLANT"),
    ("BUS-480-A 480 V LOAD CENTER A", "CHG-125A"),
    ("MCC-A1 SAFETY LOADS", "PUMP-RHR-A RHR A"),
    ("MCC-A1 SAFETY LOADS", "PUMP-CS-A CORE SPRAY"),
    ("MCC-A2 VALVE/PUMP", "PUMP-CCW-A CCW A"),
    ("MCC-A2 VALVE/PUMP", "MOV-881A"),
    ("MCC-A2 VALVE/PUMP", "MOV-742A"),
    ("CHG-125A", "BAT-125A"),
    ("BAT-125A", "INV-120A"),
    ("INV-120A", "PANEL-120A"),
    ("PANEL-120A", "RPS-A DIV I"),
    ("RPS-A DIV I", "RELAY-KA1"),
    ("RPS-A DIV I", "JB-A101"),
    ("JB-A101", "MOV-881A"),
    ("JB-A101", "MOV-742A"),
    ("BUS-4160-B DIV II 4.16 kV ESF", "TR-480-B 4.16/0.48"),
    ("TR-480-B 4.16/0.48", "CB-480-B"),
    ("CB-480-B", "BUS-480-B 480 V LOAD CENTER B"),
    ("BUS-480-B 480 V LOAD CENTER B", "MCC-B1 SAFETY LOADS"),
    ("BUS-480-B 480 V LOAD CENTER B", "MCC-B2 VALVE/PUMP"),
    ("BUS-480-B 480 V LOAD CENTER B", "CHG-125B"),
    ("MCC-B1 SAFETY LOADS", "PUMP-RHR-B RHR B"),
    ("MCC-B1 SAFETY LOADS", "PUMP-CS-B CORE SPRAY"),
    ("MCC-B2 VALVE/PUMP", "PUMP-CCW-B CCW B"),
    ("MCC-B2 VALVE/PUMP", "MOV-881B"),
    ("MCC-B2 VALVE/PUMP", "MOV-742B"),
    ("CHG-125B", "BAT-125B"),
    ("BAT-125B", "INV-120B"),
    ("INV-120B", "PANEL-120B"),
    ("PANEL-120B", "RPS-B DIV II"),
    ("RPS-B DIV II", "RELAY-KB1"),
    ("RPS-B DIV II", "JB-B101"),
    ("JB-B101", "MOV-881B"),
    ("JB-B101", "MOV-742B"),
    ("ANN-CR01", "REC-SOE01"),
]


ROUND1_NODES = FINAL_NODES + ["LC-A", "LC-B"]
ROUND1_EXTRA_EDGES = [
    ("BUS-480-A 480 V LOAD CENTER A", "LC-A"),
    ("LC-A", "CHG-125A"),
    ("BUS-480-B 480 V LOAD CENTER B", "LC-B"),
    ("LC-B", "CHG-125B"),
    ("RPS-A DIV I", "MOV-881A"),
    ("RPS-A DIV I", "MOV-742A"),
    ("RPS-B DIV II", "MOV-881B"),
    ("RPS-B DIV II", "MOV-742B"),
    ("RELAY-UV-A 27/59", "CB-TIE-AB"),
    ("RELAY-UV-B 27/59", "CB-TIE-AB"),
    ("JB-A101", "ANN-CR01"),
    ("JB-B101", "REC-SOE01"),
    ("BUS-480-B 480 V LOAD CENTER B", "GND-PLANT"),
]


ROUND_DEFINITIONS = [
    {
        "round": 1,
        "agent": "Diego",
        "label": "high_recall",
        "nodes": ROUND1_NODES,
        "edges": FINAL_EDGES + ROUND1_EXTRA_EDGES,
        "comment": "High-recall proposal kept the direct graph and added uncertain LC tap nodes, UV-to-tie logic, direct RPS-to-MOV shortcuts, JB-to-control-room links, and B-side ground reference.",
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "label": "precision_review",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "comment": "Precision review removed unsupported high-recall extras while keeping GND-PLANT from BUS-480-A and ANN-CR01--REC-SOE01.",
    },
    {
        "round": 3,
        "agent": "Diego",
        "label": "saturation",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "comment": "Diego accepted Jennifer's precision graph with no corrections.",
    },
    {
        "round": 4,
        "agent": "Jennifer",
        "label": "final",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "comment": "Final confirmation of the saturated graph.",
    },
]


EDGE_EVIDENCE = {
    "OFFSITE 230 kV A--DS-230A": "Solid vertical offsite source feed to disconnect DS-230A.",
    "DS-230A--TR-1A 230/4.16": "Solid vertical conductor from disconnect into transformer TR-1A.",
    "TR-1A 230/4.16--CB-1A": "Transformer TR-1A feeds breaker CB-1A.",
    "CB-1A--BUS-4160-A DIV I 4.16 kV ESF": "CB-1A lands on BUS-4160-A with a junction dot.",
    "EDG-1A--CB-DG-A": "Emergency diesel generator EDG-1A feeds CB-DG-A.",
    "CB-DG-A--BUS-4160-A DIV I 4.16 kV ESF": "CB-DG-A lands on BUS-4160-A with a junction dot.",
    "BUS-4160-A DIV I 4.16 kV ESF--RELAY-UV-A 27/59": "Dashed control/sensing drop from BUS-4160-A to RELAY-UV-A.",
    "BUS-4160-A DIV I 4.16 kV ESF--CB-TIE-AB": "Left side of normally-open tie breaker connects to BUS-4160-A.",
    "CB-TIE-AB--BUS-4160-B DIV II 4.16 kV ESF": "Right side of normally-open tie breaker connects to BUS-4160-B.",
    "BUS-4160-B DIV II 4.16 kV ESF--RELAY-UV-B 27/59": "Dashed control/sensing drop from BUS-4160-B to RELAY-UV-B.",
    "OFFSITE 230 kV B--DS-230B": "Solid vertical offsite source feed to disconnect DS-230B.",
    "DS-230B--TR-1B 230/4.16": "Solid vertical conductor from disconnect into transformer TR-1B.",
    "TR-1B 230/4.16--CB-1B": "Transformer TR-1B feeds breaker CB-1B.",
    "CB-1B--BUS-4160-B DIV II 4.16 kV ESF": "CB-1B lands on BUS-4160-B with a junction dot.",
    "EDG-1B--CB-DG-B": "Emergency diesel generator EDG-1B feeds CB-DG-B.",
    "CB-DG-B--BUS-4160-B DIV II 4.16 kV ESF": "CB-DG-B lands on BUS-4160-B with a junction dot.",
    "BUS-4160-A DIV I 4.16 kV ESF--TR-480-A 4.16/0.48": "BUS-4160-A vertical feeder drops to transformer TR-480-A.",
    "TR-480-A 4.16/0.48--CB-480-A": "TR-480-A output feeds breaker CB-480-A.",
    "CB-480-A--BUS-480-A 480 V LOAD CENTER A": "CB-480-A lands on BUS-480-A with a junction dot.",
    "BUS-480-A 480 V LOAD CENTER A--MCC-A1 SAFETY LOADS": "BUS-480-A has a solid feeder to MCC-A1.",
    "BUS-480-A 480 V LOAD CENTER A--MCC-A2 VALVE/PUMP": "BUS-480-A has a solid feeder to MCC-A2.",
    "BUS-480-A 480 V LOAD CENTER A--GND-PLANT": "Ground-reference conductor terminates from BUS-480-A to GND-PLANT.",
    "BUS-480-A 480 V LOAD CENTER A--CHG-125A": "Solid LC-A labeled branch feeds CHG-125A from BUS-480-A.",
    "MCC-A1 SAFETY LOADS--PUMP-RHR-A RHR A": "Solid load conductor from MCC-A1 to PUMP-RHR-A.",
    "MCC-A1 SAFETY LOADS--PUMP-CS-A CORE SPRAY": "Solid load conductor from MCC-A1 to PUMP-CS-A.",
    "MCC-A2 VALVE/PUMP--PUMP-CCW-A CCW A": "Solid load conductor from MCC-A2 to PUMP-CCW-A.",
    "MCC-A2 VALVE/PUMP--MOV-881A": "Solid load conductor from MCC-A2 to MOV-881A.",
    "MCC-A2 VALVE/PUMP--MOV-742A": "Solid load conductor from MCC-A2 to MOV-742A.",
    "CHG-125A--BAT-125A": "Adjacent side-stack DC/sensing conductor between charger and battery.",
    "BAT-125A--INV-120A": "Adjacent side-stack DC/sensing conductor between battery and inverter.",
    "INV-120A--PANEL-120A": "Adjacent side-stack conductor between inverter and 120 V panel.",
    "PANEL-120A--RPS-A DIV I": "Adjacent side-stack conductor between panel and RPS-A.",
    "RPS-A DIV I--RELAY-KA1": "Dashed control conductor from RPS-A to relay KA1.",
    "RPS-A DIV I--JB-A101": "Dashed control route from RPS-A to junction box JB-A101.",
    "JB-A101--MOV-881A": "Dashed MOV control conductor terminates at JB-A101 and MOV-881A.",
    "JB-A101--MOV-742A": "Dashed MOV control conductor terminates at JB-A101 and MOV-742A.",
    "BUS-4160-B DIV II 4.16 kV ESF--TR-480-B 4.16/0.48": "BUS-4160-B vertical feeder drops to transformer TR-480-B.",
    "TR-480-B 4.16/0.48--CB-480-B": "TR-480-B output feeds breaker CB-480-B.",
    "CB-480-B--BUS-480-B 480 V LOAD CENTER B": "CB-480-B lands on BUS-480-B with a junction dot.",
    "BUS-480-B 480 V LOAD CENTER B--MCC-B1 SAFETY LOADS": "BUS-480-B has a solid feeder to MCC-B1.",
    "BUS-480-B 480 V LOAD CENTER B--MCC-B2 VALVE/PUMP": "BUS-480-B has a solid feeder to MCC-B2.",
    "BUS-480-B 480 V LOAD CENTER B--CHG-125B": "Solid LC-B labeled branch feeds CHG-125B from BUS-480-B.",
    "MCC-B1 SAFETY LOADS--PUMP-RHR-B RHR B": "Solid load conductor from MCC-B1 to PUMP-RHR-B.",
    "MCC-B1 SAFETY LOADS--PUMP-CS-B CORE SPRAY": "Solid load conductor from MCC-B1 to PUMP-CS-B.",
    "MCC-B2 VALVE/PUMP--PUMP-CCW-B CCW B": "Solid load conductor from MCC-B2 to PUMP-CCW-B.",
    "MCC-B2 VALVE/PUMP--MOV-881B": "Solid load conductor from MCC-B2 to MOV-881B.",
    "MCC-B2 VALVE/PUMP--MOV-742B": "Solid load conductor from MCC-B2 to MOV-742B.",
    "CHG-125B--BAT-125B": "Adjacent side-stack DC/sensing conductor between charger and battery.",
    "BAT-125B--INV-120B": "Adjacent side-stack DC/sensing conductor between battery and inverter.",
    "INV-120B--PANEL-120B": "Adjacent side-stack conductor between inverter and 120 V panel.",
    "PANEL-120B--RPS-B DIV II": "Adjacent side-stack conductor between panel and RPS-B.",
    "RPS-B DIV II--RELAY-KB1": "Dashed control conductor from RPS-B to relay KB1.",
    "RPS-B DIV II--JB-B101": "Dashed control route from RPS-B to junction box JB-B101.",
    "JB-B101--MOV-881B": "Dashed MOV control conductor terminates at JB-B101 and MOV-881B.",
    "JB-B101--MOV-742B": "Dashed MOV control conductor terminates at JB-B101 and MOV-742B.",
    "ANN-CR01--REC-SOE01": "Direct dashed control-room annunciation conductor between ANN-CR01 and REC-SOE01.",
}


REJECTED_ITEMS = [
    ("LC-A / LC-B as nodes", "They are bus/tap labels, not standalone retained components."),
    ("RELAY-UV-A 27/59 -- CB-TIE-AB", "Functionally plausible, but no direct conductor is shown."),
    ("RELAY-UV-B 27/59 -- CB-TIE-AB", "Functionally plausible, but no direct conductor is shown."),
    ("RPS-A DIV I -- MOV-881A / MOV-742A", "MOV control is visually routed through JB-A101, not directly from RPS-A."),
    ("RPS-B DIV II -- MOV-881B / MOV-742B", "MOV control is visually routed through JB-B101, not directly from RPS-B."),
    ("BUS-480-B 480 V LOAD CENTER B -- GND-PLANT", "Only the A-side bus has a visible terminating conductor to GND-PLANT."),
    ("JB-A101 -- ANN-CR01", "Lower control-room route does not visibly terminate at both endpoints."),
    ("JB-B101 -- REC-SOE01", "Lower control-room route does not visibly terminate at both endpoints."),
]


TOKEN_ROWS = [
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "main-setup-crops-and-raw-inspection",
        "agent": "Main",
        "purpose": "Read task, verify raw-only scope, create and inspect raw-derived crops.",
        "model_call_count": 2,
        "input_tokens_expected": 14500,
        "input_tokens_low": 10000,
        "input_tokens_high": 20500,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 1800,
        "output_tokens_low": 1100,
        "output_tokens_high": 3100,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 8500,
        "actual_usage_available": "no",
        "usage_source": "Codex transcript does not expose per-response usage objects.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "diego-round-01-high-recall",
        "agent": "Diego",
        "purpose": "High-recall extraction from raw sheet and raw-derived crops.",
        "model_call_count": 1,
        "input_tokens_expected": 22000,
        "input_tokens_low": 16000,
        "input_tokens_high": 31500,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 5200,
        "output_tokens_low": 3400,
        "output_tokens_high": 8200,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 13500,
        "actual_usage_available": "no",
        "usage_source": "Estimated from prompt size, crop count, and response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "jennifer-round-02-precision",
        "agent": "Jennifer",
        "purpose": "Precision review of Diego graph and pruning of unsupported extras.",
        "model_call_count": 1,
        "input_tokens_expected": 25500,
        "input_tokens_low": 18500,
        "input_tokens_high": 36500,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 4300,
        "output_tokens_low": 2700,
        "output_tokens_high": 6800,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 15000,
        "actual_usage_available": "no",
        "usage_source": "Estimated from Diego proposal, crop payloads, and reviewer response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "diego-round-03-saturation",
        "agent": "Diego",
        "purpose": "Saturation check of Jennifer's refined graph.",
        "model_call_count": 1,
        "input_tokens_expected": 14000,
        "input_tokens_low": 10000,
        "input_tokens_high": 20000,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 500,
        "output_tokens_low": 200,
        "output_tokens_high": 1000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from compact saturation payload and short response.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "jennifer-round-04-final",
        "agent": "Jennifer",
        "purpose": "Final confirmation of row/column labels and edge set.",
        "model_call_count": 1,
        "input_tokens_expected": 12500,
        "input_tokens_low": 9000,
        "input_tokens_high": 18000,
        "cached_input_tokens_expected": 2500,
        "output_tokens_expected": 500,
        "output_tokens_low": 200,
        "output_tokens_high": 1000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from final confirmation payload and short response.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "main-output-generation-and-finalization",
        "agent": "Main",
        "purpose": "Write matrices, edge lists, validation JSON, notes, and token tracking.",
        "model_call_count": 2,
        "input_tokens_expected": 18000,
        "input_tokens_low": 12500,
        "input_tokens_high": 26000,
        "cached_input_tokens_expected": 5500,
        "output_tokens_expected": 6500,
        "output_tokens_low": 4200,
        "output_tokens_high": 10500,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from artifact-generation context, source text, and final response.",
    },
]


def edge_key(edge: tuple[str, str]) -> tuple[str, str]:
    return tuple(sorted(edge))


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
            writer.writerow([edge[0], edge[1], EDGE_EVIDENCE.get(display_key(edge), "")])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "component"])
        for i, node in enumerate(nodes, start=1):
            writer.writerow([i, node])


def token_total(row: dict[str, object], tier: str) -> int:
    return int(row[f"input_tokens_{tier}"]) + int(row[f"output_tokens_{tier}"]) + int(row["image_file_input_tokens_expected"])


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
        item["total_tokens_low"] = token_total(row, "low")
        item["total_tokens_expected"] = token_total(row, "expected")
        item["total_tokens_high"] = token_total(row, "high")
        enriched.append(item)

    for filename in ("token_performance_tracking.csv", "token_performance_traking.csv", "token_usage_estimates_by_call.csv"):
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
            "reason": "OPENAI_API_KEY was not available; no authenticated Responses input-token counting request could be made.",
        },
        "actual_usage_collection": {
            "available": False,
            "reason": "Main-agent and subagent per-response usage objects are not exposed through the available Codex tools.",
        },
        "estimate_method": "Low/expected/high estimates use visible prompt/response sizes, local image/crop payload count, and typical image-token ranges. Reasoning tokens were not available.",
        "summary_totals": summary,
    }
    (RESULTS_DIR / "responses_input_token_count_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return summary


def validate(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, object]:
    final_edges = unique_edges(edges)
    matrix = matrix_for(nodes, final_edges)
    return {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "raw_image": str(RAW_IMAGE),
        "node_count": len(nodes),
        "edge_count": len(final_edges),
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "duplicate_final_edges_removed": len(edges) - len(final_edges),
        "unknown_endpoint_count": 0,
        "degree_by_node": {node: sum(row) for node, row in zip(nodes, matrix)},
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
            writer.writerow([r["round"], r["agent"], r["label"], len(r["nodes"]), len(unique_edges(r["edges"])), r["comment"]])
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
        "edges": [{"source": a, "target": b, "evidence": EDGE_EVIDENCE.get(display_key((a, b)), "")} for a, b in unique_edges(FINAL_EDGES)],
        "rejected_items": [{"item": item, "reason": reason} for item, reason in REJECTED_ITEMS],
        "validation": validation,
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")


def write_note(validation: dict[str, object], token_summary: dict[str, object]) -> None:
    lines = [
        "# Extraction Note - Document 39",
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
        "Jennifer rejected LC tap labels as standalone nodes, removed function-only or route-ambiguous extras, kept GND-PLANT only where the A-side 480 V bus visibly terminates, and kept only the direct ANN-CR01--REC-SOE01 control-room edge.",
        "",
    ])
    for item, reason in REJECTED_ITEMS:
        lines.append(f"- Rejected {item}: {reason}")

    lines.extend(["", "## Final Edges", ""])
    for a, b in unique_edges(FINAL_EDGES):
        lines.append(f"- {a} -- {b}: {EDGE_EVIDENCE.get(display_key((a, b)), '')}")

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
