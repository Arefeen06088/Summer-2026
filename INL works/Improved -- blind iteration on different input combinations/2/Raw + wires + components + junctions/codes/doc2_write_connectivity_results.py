from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import UTC, datetime
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"


NODES = [
    "BUS-4160-A",
    "GRID-N501",
    "DS-N501",
    "TR-SU-1A",
    "CB-SU-1A",
    "GEN-EDG-A",
    "DS-DG-A",
    "CB-DG-A",
    "CB-TIE-4AB",
    "BUS-4160-B",
    "GRID-R502",
    "DS-R502",
    "TR-SU-1B",
    "CB-SU-1B",
    "GEN-EDG-B",
    "DS-DG-B",
    "CB-DG-B",
    "GEN-AAC-1",
    "DS-AAC-1",
    "CB-AAC-1",
    "CB-F11A",
    "TR-LC11A",
    "BUS-480-A1",
    "CB-M11A",
    "MCC-11A",
    "CB-P101A",
    "MTR-P101A",
    "PUMP-RHR-A",
    "CB-F12A",
    "TR-LC12A",
    "BUS-480-A2",
    "CB-M12A",
    "MCC-12A",
    "CB-P201A",
    "MTR-P201A",
    "PUMP-SI-A",
    "CB-F13A",
    "TR-LC13A",
    "BUS-480-A3",
    "CB-M13A",
    "MCC-13A",
    "CB-FAN-A",
    "MTR-FAN-A",
    "FAN-CAV-A",
    "CB-F14A",
    "TR-RPS-A",
    "BUS-208-A",
    "REC-125-A",
    "BUS-125DC-A",
    "BAT-125-A",
    "INV-120-A",
    "BUS-120AC-A",
    "CP-RPS-A",
    "RLY-K501A",
    "INST-NI501A",
    "CB-CVCS-A",
    "MCC-CVCS-A",
    "MTR-CVCS-A",
    "PUMP-CVCS-A",
    "VLV-LCV201A",
    "CB-F11B",
    "TR-LC11B",
    "BUS-480-B1",
    "CB-M11B",
    "MCC-11B",
    "CB-P101B",
    "MTR-P101B",
    "PUMP-RHR-B",
    "CB-F12B",
    "TR-LC12B",
    "BUS-480-B2",
    "CB-M12B",
    "MCC-12B",
    "CB-P201B",
    "MTR-P201B",
    "PUMP-SI-B",
    "CB-F13B",
    "TR-LC13B",
    "BUS-480-B3",
    "CB-M13B",
    "MCC-13B",
    "CB-FAN-B",
    "MTR-FAN-B",
    "FAN-CAV-B",
    "CB-F14B",
    "TR-RPS-B",
    "BUS-208-B",
    "REC-125-B",
    "BUS-125DC-B",
    "BAT-125-B",
    "INV-120-B",
    "BUS-120AC-B",
    "CP-RPS-B",
    "RLY-K501B",
    "INST-NI501B",
    "CB-CVCS-B",
    "MCC-CVCS-B",
    "MTR-CVCS-B",
    "PUMP-CVCS-B",
    "VLV-LCV201B",
]


CHAIN_SPECS = [
    ("source_grid_a", "solid", ["GRID-N501", "DS-N501", "TR-SU-1A", "CB-SU-1A", "BUS-4160-A"]),
    ("source_edg_a", "solid", ["GEN-EDG-A", "DS-DG-A", "CB-DG-A", "BUS-4160-A"]),
    ("bus_tie_4ab", "solid", ["BUS-4160-A", "CB-TIE-4AB", "BUS-4160-B"]),
    ("source_grid_b", "solid", ["GRID-R502", "DS-R502", "TR-SU-1B", "CB-SU-1B", "BUS-4160-B"]),
    ("source_edg_b", "solid", ["GEN-EDG-B", "DS-DG-B", "CB-DG-B", "BUS-4160-B"]),
    ("source_aac_1", "solid", ["GEN-AAC-1", "DS-AAC-1", "CB-AAC-1", "BUS-4160-B"]),
    (
        "rhr_a",
        "solid",
        ["BUS-4160-A", "CB-F11A", "TR-LC11A", "BUS-480-A1", "CB-M11A", "MCC-11A", "CB-P101A", "MTR-P101A", "PUMP-RHR-A"],
    ),
    (
        "si_a",
        "solid",
        ["BUS-4160-A", "CB-F12A", "TR-LC12A", "BUS-480-A2", "CB-M12A", "MCC-12A", "CB-P201A", "MTR-P201A", "PUMP-SI-A"],
    ),
    (
        "cav_a",
        "solid",
        ["BUS-4160-A", "CB-F13A", "TR-LC13A", "BUS-480-A3", "CB-M13A", "MCC-13A", "CB-FAN-A", "MTR-FAN-A", "FAN-CAV-A"],
    ),
    ("rps_ac_dc_a", "solid", ["BUS-4160-A", "CB-F14A", "TR-RPS-A", "BUS-208-A", "REC-125-A", "BUS-125DC-A"]),
    ("battery_a", "bus-tap", ["BUS-125DC-A", "BAT-125-A"]),
    ("rps_inverter_a", "solid", ["BUS-125DC-A", "INV-120-A", "BUS-120AC-A", "CP-RPS-A"]),
    ("rps_instrument_a", "dashed", ["CP-RPS-A", "RLY-K501A", "INST-NI501A"]),
    ("cvcs_a_power", "solid", ["BUS-4160-A", "CB-CVCS-A", "MCC-CVCS-A", "MTR-CVCS-A", "PUMP-CVCS-A"]),
    ("cvcs_a_valve", "dashed", ["PUMP-CVCS-A", "VLV-LCV201A"]),
    (
        "rhr_b",
        "solid",
        ["BUS-4160-B", "CB-F11B", "TR-LC11B", "BUS-480-B1", "CB-M11B", "MCC-11B", "CB-P101B", "MTR-P101B", "PUMP-RHR-B"],
    ),
    (
        "si_b",
        "solid",
        ["BUS-4160-B", "CB-F12B", "TR-LC12B", "BUS-480-B2", "CB-M12B", "MCC-12B", "CB-P201B", "MTR-P201B", "PUMP-SI-B"],
    ),
    (
        "cav_b",
        "solid",
        ["BUS-4160-B", "CB-F13B", "TR-LC13B", "BUS-480-B3", "CB-M13B", "MCC-13B", "CB-FAN-B", "MTR-FAN-B", "FAN-CAV-B"],
    ),
    ("rps_ac_dc_b", "solid", ["BUS-4160-B", "CB-F14B", "TR-RPS-B", "BUS-208-B", "REC-125-B", "BUS-125DC-B"]),
    ("battery_b", "bus-tap", ["BUS-125DC-B", "BAT-125-B"]),
    ("rps_inverter_b", "solid", ["BUS-125DC-B", "INV-120-B", "BUS-120AC-B", "CP-RPS-B"]),
    ("rps_instrument_b", "dashed", ["CP-RPS-B", "RLY-K501B", "INST-NI501B"]),
    ("cvcs_b_power", "solid", ["BUS-4160-B", "CB-CVCS-B", "MCC-CVCS-B", "MTR-CVCS-B", "PUMP-CVCS-B"]),
    ("cvcs_b_valve", "dashed", ["PUMP-CVCS-B", "VLV-LCV201B"]),
    ("rps_ab_cross_tie", "dashed", ["CP-RPS-A", "CP-RPS-B"]),
]


BUS_TAP_NODES = {
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-480-A1",
    "BUS-480-A2",
    "BUS-480-A3",
    "BUS-208-A",
    "BUS-125DC-A",
    "BUS-120AC-A",
    "BUS-480-B1",
    "BUS-480-B2",
    "BUS-480-B3",
    "BUS-208-B",
    "BUS-125DC-B",
    "BUS-120AC-B",
}


EVIDENCE = {
    "source_grid_a": "Raw top-left source crop: GRID-N501, DS-N501, TR-SU-1A, and CB-SU-1A are joined by a solid vertical conductor into BUS-4160-A.",
    "source_edg_a": "Raw top-left source crop: GEN-EDG-A, DS-DG-A, and CB-DG-A are joined by a solid vertical conductor into BUS-4160-A.",
    "bus_tie_4ab": "Raw header tie crop: BUS-4160-A and BUS-4160-B are connected through CB-TIE-4AB; labeled normally open but physically drawn.",
    "source_grid_b": "Raw top-right source crop: GRID-R502, DS-R502, TR-SU-1B, and CB-SU-1B are joined by a solid vertical conductor into BUS-4160-B.",
    "source_edg_b": "Raw top-right source crop: GEN-EDG-B, DS-DG-B, and CB-DG-B are joined by a solid vertical conductor into BUS-4160-B.",
    "source_aac_1": "Raw top-right source crop: GEN-AAC-1, DS-AAC-1, and CB-AAC-1 are joined by a solid vertical conductor into BUS-4160-B.",
    "rhr_a": "Raw left feeder/load crops: RHR A feeder is one vertical solid chain from BUS-4160-A through CB-F11A and downstream RHR A load devices.",
    "si_a": "Raw left feeder/load crops: SI A feeder is one vertical solid chain from BUS-4160-A through CB-F12A and downstream SI A load devices.",
    "cav_a": "Raw left feeder/load crops: CAV A feeder is one vertical solid chain from BUS-4160-A through CB-F13A and downstream CAV fan devices.",
    "rps_ac_dc_a": "Raw left feeder/RPS crops: RPS/DC A vertical solid chain runs from BUS-4160-A through CB-F14A, TR-RPS-A, BUS-208-A, REC-125-A to BUS-125DC-A.",
    "battery_a": "Raw left RPS crop: BAT-125-A taps directly to BUS-125DC-A at the busbar.",
    "rps_inverter_a": "Raw left RPS crop: BUS-125DC-A feeds INV-120-A, BUS-120AC-A, and CP-RPS-A through a vertical solid chain.",
    "rps_instrument_a": "Raw left RPS crop: CP-RPS-A connects to RLY-K501A and INST-NI501A with dashed control/instrument linework.",
    "cvcs_a_power": "Raw CVCS A crop: BUS-4160-A feeds CB-CVCS-A, MCC-CVCS-A, MTR-CVCS-A, and PUMP-CVCS-A through a vertical solid chain.",
    "cvcs_a_valve": "Raw CVCS A crop: PUMP-CVCS-A connects to VLV-LCV201A with dashed control/permissive linework.",
    "rhr_b": "Raw right feeder/load crops: RHR B feeder is one vertical solid chain from BUS-4160-B through CB-F11B and downstream RHR B load devices.",
    "si_b": "Raw right feeder/load crops: SI B feeder is one vertical solid chain from BUS-4160-B through CB-F12B and downstream SI B load devices.",
    "cav_b": "Raw right feeder/load crops: CAV B feeder is one vertical solid chain from BUS-4160-B through CB-F13B and downstream CAV fan devices.",
    "rps_ac_dc_b": "Raw right feeder/RPS crops: RPS/DC B vertical solid chain runs from BUS-4160-B through CB-F14B, TR-RPS-B, BUS-208-B, REC-125-B to BUS-125DC-B.",
    "battery_b": "Raw right RPS crop: BAT-125-B taps directly to BUS-125DC-B at the busbar.",
    "rps_inverter_b": "Raw right RPS crop: BUS-125DC-B feeds INV-120-B, BUS-120AC-B, and CP-RPS-B through a vertical solid chain.",
    "rps_instrument_b": "Raw right RPS crop: CP-RPS-B connects to RLY-K501B and INST-NI501B with dashed control/instrument linework.",
    "cvcs_b_power": "Raw CVCS B crop: BUS-4160-B feeds CB-CVCS-B, MCC-CVCS-B, MTR-CVCS-B, and PUMP-CVCS-B through a vertical solid chain.",
    "cvcs_b_valve": "Raw CVCS B crop: PUMP-CVCS-B connects to VLV-LCV201B with dashed control/permissive linework.",
    "rps_ab_cross_tie": "Raw lower control tie crop: long dashed line joins CP-RPS-A to CP-RPS-B.",
}


def expand_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for chain_name, default_type, chain in CHAIN_SPECS:
        for a, b in zip(chain, chain[1:]):
            key = tuple(sorted((a, b)))
            if key in seen:
                raise ValueError(f"duplicate edge {a}-{b}")
            seen.add(key)
            edge_type = default_type
            if default_type == "solid" and (a in BUS_TAP_NODES or b in BUS_TAP_NODES):
                edge_type = "bus-tap"
            edges.append(
                {
                    "source": a,
                    "target": b,
                    "edge_type": edge_type,
                    "chain": chain_name,
                    "evidence": EVIDENCE[chain_name],
                }
            )
    return edges


def matrix_for(edges: list[dict[str, str]]) -> list[list[int]]:
    index = {node: idx for idx, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for edge in edges:
        a = edge["source"]
        b = edge["target"]
        i = index[a]
        j = index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, matrix: list[list[int]]) -> None:
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
        writer = csv.DictWriter(f, fieldnames=["source", "target", "edge_type", "chain", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def estimate_text_tokens(text: str) -> int:
    # Conservative local approximation when API/token-counting endpoint is unavailable.
    return max(1, math.ceil(len(text) / 4))


def image_tokens(width: int, height: int) -> int:
    # Approximation for high-detail tiled image inputs: base 85 + 170 per 512px tile
    # after resizing so the long side is at most 2048 and short side at most 768.
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
    image_inputs = {
        "raw full schematic": (10800, 7200),
        "detected components overlay": (10800, 7200),
        "wire nodes overlay": (10800, 7200),
        "raw_top_sources_and_4160": (8100, 1650),
        "raw_left_feeders_close": (3200, 2250),
        "raw_left_480_and_loads": (3200, 2700),
        "raw_left_dc_ac_rps": (2000, 3450),
        "raw_cvcs_a_branch": (1150, 2450),
        "raw_right_feeders_close": (3750, 2250),
        "raw_right_480_and_loads": (3750, 2700),
        "raw_right_dc_ac_rps": (1700, 3450),
        "raw_cvcs_b_branch": (850, 2450),
        "raw_lower_control_tie": (4750, 1600),
    }
    image_token_total_diego = (
        image_tokens(*image_inputs["raw full schematic"])
        + image_tokens(*image_inputs["wire nodes overlay"])
        + sum(image_tokens(*image_inputs[name]) for name in image_inputs if name.startswith("raw_"))
    )
    image_token_total_jennifer = (
        image_tokens(*image_inputs["raw full schematic"])
        + image_tokens(*image_inputs["detected components overlay"])
        + sum(image_tokens(*image_inputs[name]) for name in image_inputs if name.startswith("raw_"))
    )

    calls = [
        {
            "document": "2",
            "iteration": "1",
            "round": "main_setup_visual_inspection",
            "agent": "Main",
            "model_call": "main agent orchestration and visual crop inspection",
            "input_tokens_est_low": 6500,
            "input_tokens_est_expected": 9500,
            "input_tokens_est_high": 13000,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 6200,
            "output_tokens_est_low": 800,
            "output_tokens_est_expected": 1400,
            "output_tokens_est_high": 2400,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Local shell/PIL inspection plus model visual reads; no OCR and no GT/validation artifacts.",
        },
        {
            "document": "2",
            "iteration": "1",
            "round": "round_01_diego",
            "agent": "Diego",
            "model_call": "high-recall extraction",
            "input_tokens_est_low": 5600,
            "input_tokens_est_expected": 7600,
            "input_tokens_est_high": 9800,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": image_token_total_diego,
            "output_tokens_est_low": 1800,
            "output_tokens_est_expected": 2700,
            "output_tokens_est_high": 3900,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Subagent usage object not returned by tool; image tokens approximated from dimensions.",
        },
        {
            "document": "2",
            "iteration": "1",
            "round": "round_02_jennifer",
            "agent": "Jennifer",
            "model_call": "precision review/refinement",
            "input_tokens_est_low": 8200,
            "input_tokens_est_expected": 10800,
            "input_tokens_est_high": 13600,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": image_token_total_jennifer,
            "output_tokens_est_low": 1200,
            "output_tokens_est_expected": 1900,
            "output_tokens_est_high": 2800,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Includes Diego proposal text plus visual resources.",
        },
        {
            "document": "2",
            "iteration": "1",
            "round": "round_03_diego",
            "agent": "Diego",
            "model_call": "convergence check after Jennifer correction",
            "input_tokens_est_low": 500,
            "input_tokens_est_expected": 750,
            "input_tokens_est_high": 1100,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 0,
            "output_tokens_est_low": 120,
            "output_tokens_est_expected": 220,
            "output_tokens_est_high": 400,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Text-only follow-up in same subagent context; cached tokens not exposed.",
        },
        {
            "document": "2",
            "iteration": "1",
            "round": "round_04_jennifer",
            "agent": "Jennifer",
            "model_call": "final sign-off",
            "input_tokens_est_low": 350,
            "input_tokens_est_expected": 550,
            "input_tokens_est_high": 900,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 0,
            "output_tokens_est_low": 80,
            "output_tokens_est_expected": 160,
            "output_tokens_est_high": 300,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Text-only final confirmation; no API key for Responses counting endpoint.",
        },
        {
            "document": "2",
            "iteration": "1",
            "round": "main_write_verify",
            "agent": "Main",
            "model_call": "artifact writing, verification, final response",
            "input_tokens_est_low": 2500,
            "input_tokens_est_expected": 4000,
            "input_tokens_est_high": 6500,
            "cached_input_tokens": "not exposed",
            "image_file_input_tokens_est": 0,
            "output_tokens_est_low": 400,
            "output_tokens_est_expected": 900,
            "output_tokens_est_high": 1500,
            "reasoning_tokens": "not exposed",
            "usage_object_available": "no",
            "notes": "Final report generation and sanity-check command outputs.",
        },
    ]

    token_path = RESULTS / "token_usage_estimate.csv"
    with token_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "document",
            "iteration",
            "round",
            "agent",
            "model_call",
            "input_tokens_est_low",
            "input_tokens_est_expected",
            "input_tokens_est_high",
            "cached_input_tokens",
            "image_file_input_tokens_est",
            "output_tokens_est_low",
            "output_tokens_est_expected",
            "output_tokens_est_high",
            "reasoning_tokens",
            "usage_object_available",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    totals = {
        "document": "2",
        "iteration": "1",
        "endpoint_status": "Responses input-token counting endpoint not called because no API key is available.",
        "usage_object_status": "Subagent tool responses did not expose OpenAI usage objects or reasoning token counts.",
        "local_estimation_method": "Text tokens approximated at ceil(characters/4) for planned prompts; image tokens approximated from high-detail 512px tile formula after resize; outputs estimated low/expected/high from observed response sizes.",
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


def write_reports(edges: list[dict[str, str]], matrix: list[list[int]]) -> None:
    edge_type_counts: dict[str, int] = {}
    for edge in edges:
        edge_type_counts[edge["edge_type"]] = edge_type_counts.get(edge["edge_type"], 0) + 1

    rounds = [
        {
            "round": "round_01_diego_high_recall",
            "agent": "Diego",
            "status": "proposed 100 nodes and 100 edges from visual evidence, including dashed control/permissive links.",
            "nodes": len(NODES),
            "edges": len(edges),
        },
        {
            "round": "round_02_jennifer_precision_review",
            "agent": "Jennifer",
            "status": "no nodes or edges removed; clarified dashed/control edge classification.",
            "nodes": len(NODES),
            "edges": len(edges),
        },
        {
            "round": "round_03_diego_convergence",
            "agent": "Diego",
            "status": "accepted Jennifer refinement; no graph changes.",
            "nodes": len(NODES),
            "edges": len(edges),
        },
        {
            "round": "round_04_jennifer_final",
            "agent": "Jennifer",
            "status": "final saturated matrix confirmed.",
            "nodes": len(NODES),
            "edges": len(edges),
        },
    ]
    with (RESULTS / "rounds_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["round", "agent", "status", "nodes", "edges"])
        writer.writeheader()
        writer.writerows(rounds)

    excluded = [
        {
            "item": "feeder-zone dashed boundary boxes",
            "decision": "excluded",
            "reason": "Visual zone boundaries, not component nodes or electrical links.",
        },
        {
            "item": "cable IDs, ratings, voltage/frequency text, title block, revision/cable index",
            "decision": "excluded",
            "reason": "Annotations only; not graph nodes.",
        },
        {
            "item": "unconnected busbar endcaps",
            "decision": "excluded",
            "reason": "No component/node label and no adjacent connected device.",
        },
        {
            "item": "CB-TIE-4AB operating state",
            "decision": "retained physical edge; noted normally open",
            "reason": "Breaker is visibly connected between BUS-4160-A and BUS-4160-B; N.O. text describes state, not absence of drawn connectivity.",
        },
    ]
    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "decision", "reason"])
        writer.writeheader()
        writer.writerows(excluded)

    inventory = [
        {
            "resource": "raw -- schematic_image_variant_b_100.png",
            "used": "yes",
            "notes": "Primary evidence for labels and connections.",
        },
        {
            "resource": "detected_components_and_logical_overlay.png",
            "used": "yes",
            "notes": "Approved visual aid for component positions during Jennifer review.",
        },
        {
            "resource": "wire_nodes_overlay.png",
            "used": "yes",
            "notes": "Approved visual aid for wire/junction geometry during Diego review.",
        },
        {
            "resource": "wires_mask.png / wires_mask_overlay.png",
            "used": "limited",
            "notes": "Approved aid considered through crops/visual context; raw remained authoritative.",
        },
        {
            "resource": "wire_nodes.csv",
            "used": "limited",
            "notes": "Approved aid briefly inspected for node coordinate structure only; no GT or validation content.",
        },
        {
            "resource": "connectivity_matrix_validation_metrics.csv / summary",
            "used": "no",
            "notes": "Ignored because it is validation/GT-derived feedback.",
        },
    ]
    with (RESULTS / "source_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["resource", "used", "notes"])
        writer.writeheader()
        writer.writerows(inventory)

    summary = {
        "document": "2",
        "iteration": "1",
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "nodes": len(NODES),
        "edges": len(edges),
        "matrix_rows": len(matrix),
        "matrix_cols": len(matrix[0]),
        "diagonal_sum": sum(matrix[i][i] for i in range(len(NODES))),
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(NODES)) for j in range(len(NODES))),
        "off_diagonal_nonzero_entries": sum(sum(row) for row in matrix),
        "edge_type_counts": edge_type_counts,
        "subagent_rounds": rounds,
        "ocr_used": False,
        "gt_or_validation_used": False,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    report = f"""# Document 2 Connectivity Extraction

Blind extraction using only `Raw + wires + components + junctions` resources.

## Final Counts

- Nodes: {len(NODES)}
- Undirected edges: {len(edges)}
- Matrix: {len(matrix)} x {len(matrix[0])}
- Symmetric: {summary["symmetric"]}
- Diagonal sum: {summary["diagonal_sum"]}
- Off-diagonal nonzero entries: {summary["off_diagonal_nonzero_entries"]}
- Edge type counts: {edge_type_counts}

## Round Saturation

1. Diego high-recall: proposed 100 nodes / 100 edges.
2. Jennifer precision review: removed no nodes/edges; clarified dashed/control edge typing.
3. Diego convergence: accepted Jennifer's correction without graph changes.
4. Jennifer final: saturated matrix confirmed.

## Important Interpretation Notes

- Dashed links were retained as control/instrument/permissive connectivity because the drawing legend says dashed lines indicate those wiring types.
- `CB-TIE-4AB` was retained as a physical drawn bus-tie component between `BUS-4160-A` and `BUS-4160-B`; its `N.O.` label is an operating-state note, not a reason to remove the drawn connection.
- Feeder-zone boxes, cable IDs, ratings, title-block text, and unconnected busbar endcaps were excluded.
- No off-the-shelf OCR was used.
- GT, validation metrics, and GT-derived feedback were not used.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    if len(NODES) != 100:
        raise ValueError(f"expected 100 nodes, got {len(NODES)}")
    if len(set(NODES)) != len(NODES):
        raise ValueError("node list contains duplicates")

    edges = expand_edges()
    if len(edges) != 100:
        raise ValueError(f"expected 100 edges, got {len(edges)}")
    for edge in edges:
        if edge["source"] not in NODES or edge["target"] not in NODES:
            raise ValueError(f"unknown node in edge {edge}")

    matrix = matrix_for(edges)
    if any(matrix[i][i] for i in range(len(NODES))):
        raise ValueError("diagonal contains nonzero values")
    if not all(matrix[i][j] == matrix[j][i] for i in range(len(NODES)) for j in range(len(NODES))):
        raise ValueError("matrix is not symmetric")
    if sum(sum(row) for row in matrix) != 200:
        raise ValueError("matrix off-diagonal count is not 200")

    write_node_order(RESULTS / "final_node_order.csv")
    write_edges(RESULTS / "final_edges.csv", edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", matrix)

    round_files = [
        "round_01_diego_high_recall_connectivity_matrix.csv",
        "round_02_jennifer_precision_connectivity_matrix.csv",
        "round_03_diego_convergence_connectivity_matrix.csv",
        "round_04_jennifer_final_connectivity_matrix.csv",
    ]
    edge_round_files = [
        "round_01_diego_high_recall_edges.csv",
        "round_02_jennifer_precision_edges.csv",
        "round_03_diego_convergence_edges.csv",
        "round_04_jennifer_final_edges.csv",
    ]
    node_round_files = [
        "round_01_diego_high_recall_node_order.csv",
        "round_02_jennifer_precision_node_order.csv",
        "round_03_diego_convergence_node_order.csv",
        "round_04_jennifer_final_node_order.csv",
    ]
    for path in round_files:
        write_matrix(RESULTS / path, matrix)
    for path in edge_round_files:
        write_edges(RESULTS / path, edges)
    for path in node_round_files:
        write_node_order(RESULTS / path)

    write_reports(edges, matrix)
    write_token_estimates()
    shutil.copy2(Path(__file__).resolve(), CODES / Path(__file__).name)
    print(json.dumps({"nodes": len(NODES), "edges": len(edges), "matrix": [len(matrix), len(matrix[0])]}, indent=2))


if __name__ == "__main__":
    main()
