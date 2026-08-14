from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import UTC, datetime
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"


TOP_NODES = [
    "GRID-345",
    "DS-101",
    "CB-101",
    "BUS-13KV-N",
    "GEN-G1",
    "CB-G1",
    "GEN-G2",
    "CB-G2",
    "TR-1A",
    "CB-4A-IN",
    "TR-1B",
    "CB-4B-IN",
    "BUS-4160-A",
    "BUS-4160-B",
    "DG-1A",
    "CB-DG1A",
    "DG-1B",
    "CB-DG1B",
    "CB-TIE-41",
    "TR-480-A",
    "CB-480A-IN",
    "BUS-480-A",
    "TR-480-B",
    "CB-480B-IN",
    "BUS-480-B",
    "TR-480-C",
    "CB-480C-IN",
    "BUS-480-C",
    "TR-480-D",
    "CB-480D-IN",
    "BUS-480-D",
    "DC-BUS-125A",
    "DC-BUS-125B",
    "PANEL-CTRL-MAIN",
    "GND-EQ-A",
    "GND-EQ-B",
    "CHGR-125A",
    "BAT-125A",
    "CHGR-125B",
    "BAT-125B",
]


BRANCH_PATTERNS = {
    "A": [
        ("01", "DS", "PMP", "RLY", "dashed"),
        ("02", "FU", "MOV", "LS", "dotted"),
        ("03", "DS", "MTR", "RLY", "dashed"),
        ("04", "DS", "PNL", "JB", "dotted"),
        ("05", "FU", "PMP", "FT", "dotted"),
        ("06", "DS", "MOV", "RLY", "dashed"),
        ("07", "DS", "MCC", "TB", "dotted"),
        ("08", "FU", "PMP", "PT", "dotted"),
        ("09", "DS", "FAN", "HS", "dashed"),
        ("10", "DS", "JB", "LT", "dotted"),
    ],
    "B": [
        ("01", "DS", "PMP", "RLY", "dashed"),
        ("02", "FU", "MOV", "LS", "dotted"),
        ("03", "DS", "MTR", "RLY", "dashed"),
        ("04", "DS", "PNL", "JB", "dotted"),
        ("05", "FU", "PMP", "FT", "dotted"),
        ("06", "DS", "MOV", "RLY", "dashed"),
        ("07", "DS", "MCC", "TB", "dotted"),
        ("08", "FU", "PMP", "PT", "dotted"),
        ("09", "DS", "FAN", "HS", "dashed"),
        ("10", "DS", "JB", "LT", "dotted"),
    ],
    "C": [
        ("01", "DS", "MOV", "RLY", "dashed"),
        ("02", "FU", "PNL", "JB", "dotted"),
        ("03", "DS", "PMP", "FT", "dotted"),
        ("04", "DS", "HTR", "HS", "dashed"),
        ("05", "FU", "INST", "JB", "dotted"),
        ("06", "DS", "MOV", "LS", "dotted"),
        ("07", "DS", "MCC", "TB", "dotted"),
        ("08", "FU", "PMP", "PT", "dotted"),
        ("09", "DS", "PNL", "RLY", "dashed"),
        ("10", "DS", "JB", "TB", "dotted"),
    ],
    "D": [
        ("01", "DS", "MOV", "RLY", "dashed"),
        ("02", "FU", "PNL", "JB", "dotted"),
        ("03", "DS", "PMP", "FT", "dotted"),
        ("04", "DS", "HTR", "HS", "dashed"),
        ("05", "FU", "INST", "JB", "dotted"),
        ("06", "DS", "MOV", "LS", "dotted"),
        ("07", "DS", "MCC", "TB", "dotted"),
        ("08", "FU", "PMP", "PT", "dotted"),
        ("09", "DS", "PNL", "RLY", "dashed"),
        ("10", "DS", "JB", "TB", "dotted"),
    ],
}


def branch_nodes() -> list[str]:
    nodes: list[str] = []
    for center, specs in BRANCH_PATTERNS.items():
        for number, second, device, endpoint, _line_type in specs:
            suffix = f"{center}{number}"
            nodes.extend(
                [
                    f"CB-{suffix}",
                    f"{second}-{suffix}",
                    f"{device}-{suffix}",
                    f"{endpoint}-{suffix}",
                ]
            )
    return nodes


NODES = TOP_NODES + branch_nodes()


def add_edge(
    edges: list[dict[str, str]],
    source: str,
    target: str,
    line_type: str,
    evidence: str,
    status: str = "confirmed",
) -> None:
    edges.append(
        {
            "source": source,
            "target": target,
            "line_type": line_type,
            "status": status,
            "evidence": evidence,
        }
    )


def build_final_edges(include_tie: bool = True) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    add_edge(edges, "GRID-345", "DS-101", "solid", "Normal/emergency source block to source disconnect.")
    add_edge(edges, "DS-101", "CB-101", "solid", "Source disconnect to main incoming breaker.")
    add_edge(edges, "CB-101", "BUS-13KV-N", "bus-tap", "Main breaker taps BUS-13KV-N.")
    add_edge(edges, "GEN-G1", "CB-G1", "solid", "Generator G1 downlead to breaker.")
    add_edge(edges, "CB-G1", "BUS-13KV-N", "bus-tap", "G1 breaker taps BUS-13KV-N.")
    add_edge(edges, "GEN-G2", "CB-G2", "solid", "Generator G2 downlead to breaker.")
    add_edge(edges, "CB-G2", "BUS-13KV-N", "bus-tap", "G2 breaker taps BUS-13KV-N.")
    add_edge(edges, "BUS-13KV-N", "TR-1A", "bus-tap", "13 kV bus vertical feeder to transformer TR-1A.")
    add_edge(edges, "TR-1A", "CB-4A-IN", "solid", "TR-1A secondary to 4160 A incoming breaker.")
    add_edge(edges, "CB-4A-IN", "BUS-4160-A", "bus-tap", "4160 A incoming breaker taps BUS-4160-A.")
    add_edge(edges, "BUS-13KV-N", "TR-1B", "bus-tap", "13 kV bus vertical feeder to transformer TR-1B.")
    add_edge(edges, "TR-1B", "CB-4B-IN", "solid", "TR-1B secondary to 4160 B incoming breaker.")
    add_edge(edges, "CB-4B-IN", "BUS-4160-B", "bus-tap", "4160 B incoming breaker taps BUS-4160-B.")
    add_edge(edges, "DG-1A", "CB-DG1A", "solid", "Diesel generator A downlead to breaker.")
    add_edge(edges, "CB-DG1A", "BUS-4160-A", "bus-tap", "DG A breaker taps BUS-4160-A.")
    add_edge(edges, "DG-1B", "CB-DG1B", "solid", "Diesel generator B downlead to breaker.")
    add_edge(edges, "CB-DG1B", "BUS-4160-B", "bus-tap", "DG B breaker taps BUS-4160-B.")
    if include_tie:
        add_edge(edges, "BUS-4160-A", "CB-TIE-41", "normally_open_tie", "CB-TIE-41 is drawn between 4160 A and B buses; retained as terminal adjacency, normally open.", "normally_open")
        add_edge(edges, "CB-TIE-41", "BUS-4160-B", "normally_open_tie", "CB-TIE-41 is drawn between 4160 A and B buses; retained as terminal adjacency, normally open.", "normally_open")

    transformer_feeds = [
        ("A", "BUS-4160-A", "TR-480-A", "CB-480A-IN", "BUS-480-A"),
        ("B", "BUS-4160-B", "TR-480-B", "CB-480B-IN", "BUS-480-B"),
        ("C", "BUS-4160-A", "TR-480-C", "CB-480C-IN", "BUS-480-C"),
        ("D", "BUS-4160-B", "TR-480-D", "CB-480D-IN", "BUS-480-D"),
    ]
    for center, primary_bus, transformer, breaker, bus in transformer_feeds:
        add_edge(edges, primary_bus, transformer, "bus-tap", f"480 V load center {center} transformer primary is routed from {primary_bus}.")
        add_edge(edges, transformer, breaker, "solid", f"{transformer} secondary connects to {breaker}.")
        add_edge(edges, breaker, bus, "bus-tap", f"{breaker} incoming feeder taps {bus}.")

    add_edge(edges, "DC-BUS-125A", "DC-BUS-125B", "dc_ground", "Continuous labeled 125 V DC bus segment between A and B DC bus labels.")
    add_edge(edges, "DC-BUS-125A", "PANEL-CTRL-MAIN", "dashed", "Common DC bus tap drops to PANEL-CTRL-MAIN; represented at DC-BUS-125A/B common segment.")
    add_edge(edges, "BUS-480-C", "GND-EQ-A", "dc_ground", "Left lower ground path from BUS-480-C area to GND-EQ-A symbol.")
    add_edge(edges, "BUS-480-D", "GND-EQ-B", "dc_ground", "Right lower ground path from BUS-480-D area to GND-EQ-B symbol.")

    add_edge(edges, "BUS-480-A", "CHGR-125A", "bus-tap", "CHGR-125A is a separate direct tap from BUS-480-A.")
    add_edge(edges, "CHGR-125A", "DC-BUS-125A", "dc_ground", "CHGR-125A output connects to DC-BUS-125A enclosure/bus path.")
    add_edge(edges, "BAT-125A", "DC-BUS-125A", "dc_ground", "BAT-125A is associated with the DC-BUS-125A enclosure/bus path.")
    add_edge(edges, "BUS-480-B", "CHGR-125B", "bus-tap", "CHGR-125B is a separate direct tap from BUS-480-B.")
    add_edge(edges, "CHGR-125B", "DC-BUS-125B", "dc_ground", "CHGR-125B output connects to DC-BUS-125B enclosure/bus path.")
    add_edge(edges, "BAT-125B", "DC-BUS-125B", "dc_ground", "BAT-125B is associated with the DC-BUS-125B enclosure/bus path.")

    for center, specs in BRANCH_PATTERNS.items():
        bus = f"BUS-480-{center}"
        for number, second, device, endpoint, lower_line_type in specs:
            suffix = f"{center}{number}"
            cb = f"CB-{suffix}"
            second_node = f"{second}-{suffix}"
            device_node = f"{device}-{suffix}"
            endpoint_node = f"{endpoint}-{suffix}"
            add_edge(edges, bus, cb, "bus-tap", f"{cb} is a filled-dot tap from {bus}.")
            add_edge(edges, cb, second_node, "solid", f"{suffix} feeder breaker to {second_node}.")
            add_edge(edges, second_node, device_node, "solid", f"{suffix} feeder device chain to {device_node}.")
            add_edge(edges, device_node, endpoint_node, lower_line_type, f"{suffix} lower {lower_line_type} lead to {endpoint_node}.")
    return dedupe_edges(edges)


def dedupe_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for edge in edges:
        key = tuple(sorted((edge["source"], edge["target"])))
        if key in seen:
            raise ValueError(f"duplicate edge {edge['source']} -- {edge['target']}")
        seen.add(key)
        deduped.append(edge)
    return deduped


def round_01_diego_edges() -> list[dict[str, str]]:
    edges = build_final_edges(include_tie=True)
    remove_keys = {tuple(sorted(pair)) for pair in [("BUS-480-A", "CHGR-125A"), ("BUS-480-B", "CHGR-125B")]}
    edges = [edge for edge in edges if tuple(sorted((edge["source"], edge["target"]))) not in remove_keys]
    add_edge(edges, "CB-A10", "CHGR-125A", "solid", "Diego high-recall candidate: charger near A10 branch; later corrected by Jennifer.", "rejected_later")
    add_edge(edges, "DS-A10", "BAT-125A", "solid", "Diego high-recall candidate: battery near DS-A10; later rejected by Jennifer.", "rejected_later")
    add_edge(edges, "CB-B01", "CHGR-125B", "solid", "Diego high-recall candidate: charger near B01 branch; later corrected by Jennifer.", "rejected_later")
    add_edge(edges, "DS-B01", "BAT-125B", "solid", "Diego high-recall candidate: battery near DS-B01; later rejected by Jennifer.", "rejected_later")
    return dedupe_edges(edges)


def round_02_jennifer_edges() -> list[dict[str, str]]:
    return build_final_edges(include_tie=False)


def matrix_for(edges: list[dict[str, str]]) -> list[list[int]]:
    index = {node: idx for idx, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for edge in edges:
        a = edge["source"]
        b = edge["target"]
        if a not in index or b not in index:
            raise ValueError(f"unknown node in edge {a} -- {b}")
        i = index[a]
        j = index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, edges: list[dict[str, str]]) -> None:
    matrix = matrix_for(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + NODES)
        for node, row in zip(NODES, matrix):
            writer.writerow([node] + row)


def write_node_order(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for idx, node in enumerate(NODES):
            writer.writerow([idx, node])


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "line_type", "status", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def verify_edges(edges: list[dict[str, str]], expected_edges: int) -> dict[str, object]:
    matrix = matrix_for(edges)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(NODES)) for j in range(len(NODES)))
    diag_sum = sum(matrix[i][i] for i in range(len(NODES)))
    edge_count = sum(sum(row) for row in matrix) // 2
    if len(NODES) != 200:
        raise ValueError(f"expected 200 nodes, got {len(NODES)}")
    if len(set(NODES)) != len(NODES):
        raise ValueError("duplicate nodes")
    if edge_count != expected_edges:
        raise ValueError(f"expected {expected_edges} matrix edges, got {edge_count}")
    if diag_sum != 0:
        raise ValueError(f"nonzero diagonal sum {diag_sum}")
    if not symmetric:
        raise ValueError("matrix is not symmetric")
    line_type_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for edge in edges:
        line_type_counts[edge["line_type"]] = line_type_counts.get(edge["line_type"], 0) + 1
        status_counts[edge["status"]] = status_counts.get(edge["status"], 0) + 1
    return {
        "nodes": len(NODES),
        "edges": edge_count,
        "off_diagonal_nonzero_entries": sum(sum(row) for row in matrix),
        "symmetric": symmetric,
        "diagonal_sum": diag_sum,
        "line_type_counts": line_type_counts,
        "status_counts": status_counts,
    }


def image_tokens(width: int, height: int) -> int:
    long_side = max(width, height)
    scale = 1.0
    if long_side > 2048:
        scale = 2048 / long_side
    width2 = width * scale
    height2 = height * scale
    short_side = min(width2, height2)
    if short_side > 768:
        scale *= 768 / short_side
        width2 = width * scale
        height2 = height * scale
    tiles = math.ceil(width2 / 512) * math.ceil(height2 / 512)
    return 85 + 170 * tiles


def write_token_estimates() -> None:
    crop_dims = {
        "raw full": (10522, 7307),
        "wire nodes overlay": (10522, 7307),
        "components overlay": (10522, 7307),
        "raw_top_13kv_sources": (8240, 1750),
        "raw_4160_a_bus_and_left_transformer": (4280, 1500),
        "raw_4160_b_bus_and_right_transformer": (4600, 1500),
        "raw_train_a_load_center_a_full": (3930, 2050),
        "raw_train_b_load_center_b_full": (3850, 2050),
        "raw_train_c_load_center_c_full": (3930, 2350),
        "raw_train_d_load_center_d_full": (3850, 2350),
        "raw_dc_bus_125a_and_control": (2500, 1350),
        "raw_bottom_ground_paths": (7950, 1200),
    }
    diego_images = ["raw full", "wire nodes overlay"] + [name for name in crop_dims if name.startswith("raw_")]
    jennifer_images = ["raw full", "components overlay", "raw_top_13kv_sources", "raw_train_a_load_center_a_full", "raw_train_b_load_center_b_full", "raw_train_c_load_center_c_full", "raw_train_d_load_center_d_full", "raw_dc_bus_125a_and_control", "raw_bottom_ground_paths"]
    calls = [
        {
            "document": "27",
            "iteration": "1",
            "round": "main_setup_visual_inspection",
            "agent": "Main",
            "model_call": "resource inventory, crop generation, visual inspection",
            "input_tokens_est_low": 9000,
            "input_tokens_est_expected": 13000,
            "input_tokens_est_high": 18000,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 9800,
            "output_tokens_est_low": 1000,
            "output_tokens_est_expected": 1800,
            "output_tokens_est_high": 3200,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Local crop generation and model visual inspection; no OCR or GT/validation files.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_01_diego",
            "agent": "Diego",
            "model_call": "high-recall extraction",
            "input_tokens_est_low": 9500,
            "input_tokens_est_expected": 13000,
            "input_tokens_est_high": 17000,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": sum(image_tokens(*crop_dims[name]) for name in diego_images),
            "output_tokens_est_low": 3800,
            "output_tokens_est_expected": 5600,
            "output_tokens_est_high": 8000,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Subagent usage object not exposed by tool.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_02_jennifer",
            "agent": "Jennifer",
            "model_call": "precision review/refinement",
            "input_tokens_est_low": 13000,
            "input_tokens_est_expected": 18000,
            "input_tokens_est_high": 24000,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": sum(image_tokens(*crop_dims[name]) for name in jennifer_images),
            "output_tokens_est_low": 2400,
            "output_tokens_est_expected": 3600,
            "output_tokens_est_high": 5200,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Includes Diego proposal text plus visual resources.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_03_diego",
            "agent": "Diego",
            "model_call": "convergence check after Jennifer correction",
            "input_tokens_est_low": 800,
            "input_tokens_est_expected": 1200,
            "input_tokens_est_high": 1700,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 0,
            "output_tokens_est_low": 250,
            "output_tokens_est_expected": 450,
            "output_tokens_est_high": 800,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Text-only follow-up in same subagent context.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_04_jennifer",
            "agent": "Jennifer",
            "model_call": "final sign-off",
            "input_tokens_est_low": 500,
            "input_tokens_est_expected": 800,
            "input_tokens_est_high": 1200,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 0,
            "output_tokens_est_low": 100,
            "output_tokens_est_expected": 250,
            "output_tokens_est_high": 500,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Text-only final confirmation.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "main_write_verify",
            "agent": "Main",
            "model_call": "artifact writing, verification, final response",
            "input_tokens_est_low": 4500,
            "input_tokens_est_expected": 7000,
            "input_tokens_est_high": 11000,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 0,
            "output_tokens_est_low": 500,
            "output_tokens_est_expected": 1100,
            "output_tokens_est_high": 1800,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "No API key for Responses input-token counting endpoint.",
        },
    ]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(calls[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)
    totals = {
        "document": "27",
        "iteration": "1",
        "endpoint_status": "Responses input-token counting endpoint not called because no API key is available.",
        "usage_object_status": "Subagent tool responses did not expose OpenAI usage objects or reasoning token counts.",
        "local_estimation_method": "Text tokens estimated from prompt sizes; image tokens approximated with high-detail 512px tile formula after resize; outputs estimated low/expected/high from observed response sizes.",
        "calls": len(calls),
        "input_tokens_low_total": sum(int(row["input_tokens_est_low"]) for row in calls),
        "input_tokens_expected_total": sum(int(row["input_tokens_est_expected"]) for row in calls),
        "input_tokens_high_total": sum(int(row["input_tokens_est_high"]) for row in calls),
        "image_file_input_tokens_est_total": sum(int(row["image_file_input_tokens_est"]) for row in calls),
        "output_tokens_low_total": sum(int(row["output_tokens_est_low"]) for row in calls),
        "output_tokens_expected_total": sum(int(row["output_tokens_est_expected"]) for row in calls),
        "output_tokens_high_total": sum(int(row["output_tokens_est_high"]) for row in calls),
    }
    totals["total_tokens_low"] = totals["input_tokens_low_total"] + totals["output_tokens_low_total"]
    totals["total_tokens_expected"] = totals["input_tokens_expected_total"] + totals["output_tokens_expected_total"]
    totals["total_tokens_high"] = totals["input_tokens_high_total"] + totals["output_tokens_high_total"]
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(totals, indent=2), encoding="utf-8")


def write_reports(round_edges: dict[str, list[dict[str, str]]], final_summary: dict[str, object]) -> None:
    rounds = [
        {
            "round": "round_01_diego_high_recall",
            "agent": "Diego",
            "status": "High-recall candidate matrix; included four charger/battery overconnection candidates later rejected.",
            "nodes": len(NODES),
            "edges": len(round_edges["round_01"]),
        },
        {
            "round": "round_02_jennifer_precision_review",
            "agent": "Jennifer",
            "status": "Removed four unsupported charger/battery candidates; counted only closed/confirmed edges and status-marked open tie separately.",
            "nodes": len(NODES),
            "edges": len(round_edges["round_02"]),
        },
        {
            "round": "round_03_diego_convergence",
            "agent": "Diego",
            "status": "Accepted Jennifer corrections and retained CB-TIE-41 terminal edges as drawn physical adjacency.",
            "nodes": len(NODES),
            "edges": len(round_edges["round_03"]),
        },
        {
            "round": "round_04_jennifer_final",
            "agent": "Jennifer",
            "status": "Final saturated physical-adjacency matrix confirmed.",
            "nodes": len(NODES),
            "edges": len(round_edges["round_04"]),
        },
    ]
    with (RESULTS / "rounds_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["round", "agent", "status", "nodes", "edges"])
        writer.writeheader()
        writer.writerows(rounds)

    decisions = [
        {
            "item": "CB-A10--CHGR-125A",
            "decision": "removed",
            "reason": "CHGR-125A is visually a separate direct tap from BUS-480-A, not downstream of CB-A10.",
        },
        {
            "item": "DS-A10--BAT-125A",
            "decision": "removed",
            "reason": "BAT-125A is associated with DC-BUS-125A path/enclosure, not with DS-A10 feeder chain.",
        },
        {
            "item": "CB-B01--CHGR-125B",
            "decision": "removed",
            "reason": "CHGR-125B is visually a separate direct tap from BUS-480-B, not downstream of CB-B01.",
        },
        {
            "item": "DS-B01--BAT-125B",
            "decision": "removed",
            "reason": "BAT-125B is associated with DC-BUS-125B path/enclosure, not with DS-B01 feeder chain.",
        },
        {
            "item": "BUS-4160-A--CB-TIE-41--BUS-4160-B",
            "decision": "retained with normally_open status",
            "reason": "Tie breaker terminals are drawn; matrix represents physical drawn adjacency, not energized bus collapse.",
        },
        {
            "item": "unmarked crossings, zone boxes, title/notes/legend text, revision table",
            "decision": "excluded",
            "reason": "No filled dot or component/logical-node label indicating an electrical connection.",
        },
    ]
    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "decision", "reason"])
        writer.writeheader()
        writer.writerows(decisions)

    inventory = [
        {
            "resource": "raw -- synthetic_npp_electrical_schematic_readable.png",
            "used": "yes",
            "notes": "Primary source for labels and connectivity.",
        },
        {
            "resource": "detected_components_overlay.png",
            "used": "yes",
            "notes": "Approved visual aid for component locations during Jennifer review.",
        },
        {
            "resource": "wire_nodes_overlay.png",
            "used": "yes",
            "notes": "Approved visual aid for junction/line geometry during Diego review.",
        },
        {
            "resource": "wires_mask.png / wires_mask_overlay.png / wire_nodes.csv",
            "used": "limited",
            "notes": "Approved aids for geometry/crop planning; raw remained authoritative.",
        },
        {
            "resource": "connectivity_matrix_validation_metrics.csv / summary",
            "used": "no",
            "notes": "Ignored as validation/GT-derived feedback.",
        },
    ]
    with (RESULTS / "source_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["resource", "used", "notes"])
        writer.writeheader()
        writer.writerows(inventory)

    summary = {
        "document": "27",
        "iteration": "1",
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        **final_summary,
        "subagent_rounds": rounds,
        "ocr_used": False,
        "gt_or_validation_used": False,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    report = f"""# Document 27 Connectivity Extraction

Blind extraction using only the `Raw + wires + components + junctions` resources.

## Final Counts

- Nodes: {final_summary["nodes"]}
- Undirected edges: {final_summary["edges"]}
- Matrix: {final_summary["nodes"]} x {final_summary["nodes"]}
- Symmetric: {final_summary["symmetric"]}
- Diagonal sum: {final_summary["diagonal_sum"]}
- Off-diagonal nonzero entries: {final_summary["off_diagonal_nonzero_entries"]}
- Line type counts: {final_summary["line_type_counts"]}

## Round Saturation

1. Diego high-recall: 200 nodes, {len(round_edges["round_01"])} candidate edges.
2. Jennifer precision: removed four unsupported charger/battery overconnections; status-marked normally-open tie.
3. Diego convergence: accepted corrections and retained `CB-TIE-41` terminal edges as drawn physical adjacency.
4. Jennifer final: saturated physical-adjacency matrix confirmed.

## Important Interpretation Notes

- The final matrix represents drawn component/node adjacency, not energized operating alignment.
- `CB-TIE-41` terminal edges are retained and marked `normally_open`; `BUS-4160-A` and `BUS-4160-B` are not collapsed.
- Solid, dashed, dotted, and DC/ground lines are included where they terminate at labeled devices, buses, panels, or ground symbols.
- No off-the-shelf OCR was used.
- GT, validation metrics, and GT-derived feedback were not used.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)

    final_edges = build_final_edges(include_tie=True)
    round_edges = {
        "round_01": round_01_diego_edges(),
        "round_02": round_02_jennifer_edges(),
        "round_03": final_edges,
        "round_04": final_edges,
    }

    final_summary = verify_edges(final_edges, expected_edges=201)
    verify_edges(round_edges["round_01"], expected_edges=203)
    verify_edges(round_edges["round_02"], expected_edges=199)
    verify_edges(round_edges["round_03"], expected_edges=201)
    verify_edges(round_edges["round_04"], expected_edges=201)

    write_node_order(RESULTS / "final_node_order.csv")
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_edges)

    round_file_info = [
        ("round_01", "round_01_diego_high_recall"),
        ("round_02", "round_02_jennifer_precision"),
        ("round_03", "round_03_diego_convergence"),
        ("round_04", "round_04_jennifer_final"),
    ]
    for key, prefix in round_file_info:
        write_node_order(RESULTS / f"{prefix}_node_order.csv")
        write_edges(RESULTS / f"{prefix}_edges.csv", round_edges[key])
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", round_edges[key])

    write_reports(round_edges, final_summary)
    write_token_estimates()
    shutil.copy2(Path(__file__).resolve(), CODES / Path(__file__).name)
    print(json.dumps(final_summary, indent=2))


if __name__ == "__main__":
    main()
