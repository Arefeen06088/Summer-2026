from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image


DOC = "36"
ITERATION = "1"

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires")
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_v2.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


DIEGO_R1_NODES = [
    "GRID-230-A", "CB-SW-A", "TR-SU-A", "SU-A", "BUS-13K-A",
    "GEN-DG-A", "CB-DG-A", "TR-EDG-A", "EDG-A",
    "CB-13-TIE", "RPS TRIP", "PNL-RPS-1", "RPS LOCKOUT",
    "BUS-13K-B", "SU-B", "TR-SU-B", "CB-SW-B", "GRID-230-B",
    "EDG-B", "TR-EDG-B", "CB-DG-B", "GEN-DG-B",
    "TR-4K-A", "CB-4K-A", "BUS-4K-A", "CB-4K-TIE",
    "BUS-4K-B", "CB-4K-B", "TR-4K-B",
    "TR-480-A", "CB-LC-A", "BUS-480-A",
    "LC-A1", "MCC-01A", "PUMP-RHR-A", "MOTOR-CCW-A",
    "LC-A2", "MCC-02A", "PUMP-AFW-A", "VALVE-MOV-A", "FAN-CONTAIN-A",
    "JB-ESF-A", "PNL-ESF-A", "RECT-125A", "BUS-DC125-A", "BAT-125A", "INV-120A",
    "TR-480-B", "CB-LC-B", "BUS-480-B",
    "LC-B1", "MCC-01B", "PUMP-RHR-B", "MOTOR-CCW-B",
    "LC-B2", "MCC-02B", "PUMP-AFW-B", "VALVE-MOV-B", "FAN-CONTAIN-B",
    "JB-ESF-B", "PNL-ESF-B", "RECT-125B", "BUS-DC125-B", "BAT-125B", "INV-120B",
]

FINAL_NODES = [
    "GRID-230-A", "CB-SW-A", "TR-SU-A", "SU-A", "BUS-13K-A",
    "GEN-DG-A", "CB-DG-A", "TR-EDG-A", "EDG-A",
    "CB-13-TIE", "BUS-13K-B", "SU-B", "TR-SU-B", "CB-SW-B", "GRID-230-B",
    "EDG-B", "TR-EDG-B", "CB-DG-B", "GEN-DG-B",
    "TR-4K-A", "CB-4K-A", "BUS-4K-A", "CB-4K-TIE",
    "BUS-4K-B", "CB-4K-B", "TR-4K-B",
    "TR-480-A", "CB-LC-A", "BUS-480-A",
    "LC-A1", "MCC-01A", "PUMP-RHR-A", "MOTOR-CCW-A",
    "LC-A2", "MCC-02A", "PUMP-AFW-A", "VALVE-MOV-A", "FAN-CONTAIN-A",
    "RECT-125A", "BUS-DC125-A", "BAT-125A", "INV-120A",
    "JB-ESF-A", "PNL-ESF-A", "PNL-RPS-1",
    "TR-480-B", "CB-LC-B", "BUS-480-B",
    "LC-B1", "MCC-01B", "PUMP-RHR-B", "MOTOR-CCW-B",
    "LC-B2", "MCC-02B", "PUMP-AFW-B", "VALVE-MOV-B", "FAN-CONTAIN-B",
    "RECT-125B", "BUS-DC125-B", "BAT-125B", "INV-120B",
    "JB-ESF-B", "PNL-ESF-B",
]

POWER_EDGES = [
    ("GRID-230-A", "CB-SW-A", "solid offsite source A to switch breaker"),
    ("CB-SW-A", "TR-SU-A", "solid source A breaker to startup transformer"),
    ("TR-SU-A", "SU-A", "solid startup transformer A to SU-A bus tap"),
    ("SU-A", "BUS-13K-A", "filled-dot tap onto 13.8 kV auxiliary switchgear A"),
    ("GEN-DG-A", "CB-DG-A", "solid emergency generator A to breaker"),
    ("CB-DG-A", "TR-EDG-A", "solid diesel breaker A to EDG transformer"),
    ("TR-EDG-A", "EDG-A", "solid EDG transformer A to EDG-A bus tap"),
    ("EDG-A", "BUS-13K-A", "filled-dot tap onto 13.8 kV bus A"),
    ("BUS-13K-A", "CB-13-TIE", "13.8 kV bus A to tie breaker"),
    ("CB-13-TIE", "BUS-13K-B", "tie breaker to 13.8 kV bus B"),
    ("BUS-13K-B", "SU-B", "filled-dot tap from 13.8 kV bus B to SU-B"),
    ("SU-B", "TR-SU-B", "solid SU-B tap to startup transformer B"),
    ("TR-SU-B", "CB-SW-B", "solid startup transformer B to source breaker"),
    ("CB-SW-B", "GRID-230-B", "solid source breaker to offsite source B"),
    ("BUS-13K-B", "EDG-B", "filled-dot tap from 13.8 kV bus B to EDG-B"),
    ("EDG-B", "TR-EDG-B", "solid EDG-B tap to transformer"),
    ("TR-EDG-B", "CB-DG-B", "solid EDG transformer B to diesel breaker"),
    ("CB-DG-B", "GEN-DG-B", "solid diesel breaker B to generator"),
    ("BUS-13K-A", "TR-4K-A", "solid transformer feed from 13.8 kV bus A"),
    ("TR-4K-A", "CB-4K-A", "solid transformer A to 4.16 kV breaker"),
    ("CB-4K-A", "BUS-4K-A", "solid breaker A to 4.16 kV bus A"),
    ("BUS-13K-B", "TR-4K-B", "solid transformer feed from 13.8 kV bus B"),
    ("TR-4K-B", "CB-4K-B", "solid transformer B to 4.16 kV breaker"),
    ("CB-4K-B", "BUS-4K-B", "solid breaker B to 4.16 kV bus B"),
    ("BUS-4K-A", "CB-4K-TIE", "4.16 kV bus A to tie breaker"),
    ("CB-4K-TIE", "BUS-4K-B", "tie breaker to 4.16 kV bus B"),
    ("BUS-4K-A", "TR-480-A", "solid feed from 4.16 kV bus A to 480 V transformer"),
    ("TR-480-A", "CB-LC-A", "solid transformer A to load-center breaker"),
    ("CB-LC-A", "BUS-480-A", "solid breaker A to 480 VAC bus A"),
    ("BUS-480-A", "LC-A1", "filled-dot 480 VAC load-center A1 tap"),
    ("LC-A1", "MCC-01A", "vertical feeder from LC-A1 tap to MCC-01A"),
    ("MCC-01A", "PUMP-RHR-A", "solid MCC feeder to RHR pump A"),
    ("MCC-01A", "MOTOR-CCW-A", "solid MCC feeder to CCW motor A"),
    ("BUS-480-A", "LC-A2", "filled-dot 480 VAC load-center A2 tap"),
    ("LC-A2", "MCC-02A", "vertical feeder from LC-A2 tap to MCC-02A"),
    ("MCC-02A", "PUMP-AFW-A", "solid MCC feeder to AFW pump A"),
    ("MCC-02A", "VALVE-MOV-A", "solid MCC feeder to MOV A"),
    ("MCC-02A", "FAN-CONTAIN-A", "solid MCC feeder to containment fan A"),
    ("BUS-480-A", "RECT-125A", "solid 480 VAC branch to rectifier/charger A"),
    ("RECT-125A", "BUS-DC125-A", "solid rectifier A output to 125 VDC bus"),
    ("BUS-DC125-A", "BAT-125A", "filled-dot battery A tap on 125 VDC bus"),
    ("BUS-DC125-A", "INV-120A", "filled-dot inverter A DC input on 125 VDC bus"),
    ("INV-120A", "PNL-ESF-A", "solid inverter A AC/control power feed to ESF panel A"),
    ("BUS-4K-B", "TR-480-B", "solid feed from 4.16 kV bus B to 480 V transformer"),
    ("TR-480-B", "CB-LC-B", "solid transformer B to load-center breaker"),
    ("CB-LC-B", "BUS-480-B", "solid breaker B to 480 VAC bus B"),
    ("BUS-480-B", "LC-B1", "filled-dot 480 VAC load-center B1 tap"),
    ("LC-B1", "MCC-01B", "vertical feeder from LC-B1 tap to MCC-01B"),
    ("MCC-01B", "PUMP-RHR-B", "solid MCC feeder to RHR pump B"),
    ("MCC-01B", "MOTOR-CCW-B", "solid MCC feeder to CCW motor B"),
    ("BUS-480-B", "LC-B2", "filled-dot 480 VAC load-center B2 tap"),
    ("LC-B2", "MCC-02B", "vertical feeder from LC-B2 tap to MCC-02B"),
    ("MCC-02B", "PUMP-AFW-B", "solid MCC feeder to AFW pump B"),
    ("MCC-02B", "VALVE-MOV-B", "solid MCC feeder to MOV B"),
    ("MCC-02B", "FAN-CONTAIN-B", "solid MCC feeder to containment fan B"),
    ("BUS-480-B", "RECT-125B", "solid 480 VAC branch to rectifier/charger B"),
    ("RECT-125B", "BUS-DC125-B", "solid rectifier B output to 125 VDC bus"),
    ("BUS-DC125-B", "BAT-125B", "filled-dot battery B tap on 125 VDC bus"),
    ("BUS-DC125-B", "INV-120B", "filled-dot inverter B DC input on 125 VDC bus"),
    ("INV-120B", "PNL-ESF-B", "solid inverter B AC/control power feed to ESF panel B"),
]

DIEGO_R1_CONTROL_EDGES = [
    ("CB-13-TIE", "RPS TRIP", "high-recall dashed path label near tie breaker"),
    ("RPS TRIP", "CB-4K-TIE", "high-recall dashed path between RPS trip label and 4.16 kV tie"),
    ("CB-4K-TIE", "PNL-RPS-1", "high-recall dashed path through RPS lockout label to RPS panel"),
    ("JB-ESF-A", "PNL-ESF-A", "dashed vertical line from ESF junction box A to panel A"),
    ("JB-ESF-B", "PNL-ESF-B", "dashed vertical line from ESF junction box B to panel B"),
    ("PNL-ESF-A", "PUMP-AFW-A", "dashed ESF control branch to AFW pump A"),
    ("PNL-ESF-A", "VALVE-MOV-A", "dashed ESF control branch to MOV A"),
    ("PNL-ESF-B", "PUMP-AFW-B", "dashed ESF control branch to AFW pump B"),
    ("PNL-ESF-B", "VALVE-MOV-B", "dashed ESF control branch to MOV B"),
]

FINAL_CONTROL_EDGES = [
    ("CB-13-TIE", "PNL-RPS-1", "single dashed RPS trip/interlock path; RPS TRIP is annotation text"),
    ("CB-4K-TIE", "PNL-RPS-1", "single dashed RPS lockout/interlock path; RPS LOCKOUT is annotation text"),
    ("JB-ESF-A", "PNL-ESF-A", "dashed vertical line from ESF junction box A to panel A"),
    ("JB-ESF-B", "PNL-ESF-B", "dashed vertical line from ESF junction box B to panel B"),
    ("PNL-ESF-A", "PUMP-AFW-A", "dashed ESF control branch to AFW pump A"),
    ("PNL-ESF-A", "VALVE-MOV-A", "dashed ESF control branch to MOV A"),
    ("PNL-ESF-B", "PUMP-AFW-B", "dashed ESF control branch to AFW pump B"),
    ("PNL-ESF-B", "VALVE-MOV-B", "dashed ESF control branch to MOV B"),
]

UNCERTAIN_FINAL = [
    ("PNL-RPS-1", "PNL-ESF-A", "possible central dashed corridor relation, but no clean terminal/dot into ESF panel A"),
    ("PNL-RPS-1", "PNL-ESF-B", "possible central dashed corridor relation, but no clean terminal/dot into ESF panel B"),
    ("PNL-ESF-A", "FAN-CONTAIN-A", "dashed boundary/route passes near fan A but no clean vertical tap is visible"),
    ("PNL-ESF-B", "FAN-CONTAIN-B", "dashed boundary/route passes near fan B but no clean vertical tap is visible"),
]


ROUNDS = [
    ("round_01_diego_high_recall", DIEGO_R1_NODES, POWER_EDGES, DIEGO_R1_CONTROL_EDGES, [
        ("CB-4K-TIE", "RPS LOCKOUT", "Diego R1 marked RPS LOCKOUT as a possible separate node rather than annotation text"),
        ("RPS LOCKOUT", "PNL-RPS-1", "Diego R1 marked RPS LOCKOUT as a possible separate node rather than annotation text"),
        *UNCERTAIN_FINAL,
    ],
     "Diego R1 high recall: accepted RPS TRIP as a tentative logical node and kept RPS LOCKOUT split uncertain."),
    ("round_01_jennifer_precision", FINAL_NODES, POWER_EDGES, FINAL_CONTROL_EDGES, UNCERTAIN_FINAL,
     "Jennifer R1 precision: removed annotation-only RPS labels as nodes and excluded unsupported fan-control taps."),
    ("round_02_diego_saturation", FINAL_NODES, POWER_EDGES, FINAL_CONTROL_EDGES, UNCERTAIN_FINAL,
     "Diego R2 saturation: agreed final graph should keep RPS labels as path annotations only."),
    ("round_02_jennifer_final", FINAL_NODES, POWER_EDGES, FINAL_CONTROL_EDGES, UNCERTAIN_FINAL,
     "Jennifer final: confirmed no extra hard edges beyond the refined Raw + wires graph."),
]


def dedupe_edges(edges: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str, str]] = []
    for a, b, evidence in edges:
        key = tuple(sorted((a, b)))
        if a == b or key in seen:
            continue
        seen.add(key)
        out.append((a, b, evidence))
    return out


def matrix_for(nodes: list[str], edges: list[tuple[str, str, str]]) -> tuple[list[list[int]], list[tuple[str, str]]]:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    missing: list[tuple[str, str]] = []
    for a, b, _evidence in dedupe_edges(edges):
        if a not in idx or b not in idx:
            missing.append((a, b))
            continue
        i, j = idx[a], idx[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix, missing


def write_matrix(path: Path, nodes: list[str], matrix: list[list[int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_sparse(path: Path, nodes: list[str], matrix: list[list[int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "connected"])
        for i, source in enumerate(nodes):
            for j, target in enumerate(nodes):
                writer.writerow([source, target, matrix[i][j]])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"])
        for node in nodes:
            writer.writerow([node])


def write_edges(path: Path, power_edges: list[tuple[str, str, str]], control_edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "edge_type", "evidence"])
        for a, b, evidence in dedupe_edges(power_edges):
            writer.writerow([a, b, "power", evidence])
        for a, b, evidence in dedupe_edges(control_edges):
            writer.writerow([a, b, "control", evidence])


def write_uncertain(path: Path, rows: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(rows)


def qa(nodes: list[str], edges: list[tuple[str, str, str]], matrix: list[list[int]], missing: list[tuple[str, str]]) -> dict:
    degree = {node: 0 for node in nodes}
    for a, b, _ in dedupe_edges(edges):
        if a in degree:
            degree[a] += 1
        if b in degree:
            degree[b] += 1
    return {
        "node_count": len(nodes),
        "hard_edge_count": len(dedupe_edges(edges)),
        "missing_edge_endpoints": missing,
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "isolated_hard_only_nodes": [node for node, deg in degree.items() if deg == 0],
    }


def image_tokens(path: Path) -> int:
    with Image.open(path) as im:
        w, h = im.size
    return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)


def token_estimates() -> list[dict]:
    image_sets = {
        "main_01_visual_orchestration_and_artifacts": [
            CROPS / "raw__overview.png",
            CROPS / "raw__top_power_bus_ties_2x.png",
            CROPS / "wires_overlay__top_power_bus_ties_2x.png",
            CROPS / "raw__central_ties_2x.png",
            CROPS / "wires_overlay__central_ties_2x.png",
            CROPS / "raw__left_480_loads_2x.png",
            CROPS / "raw__right_480_loads_2x.png",
            CROPS / "raw__left_dc_control_2x.png",
            CROPS / "raw__right_dc_control_2x.png",
            CROPS / "wires_overlay__working_area_2x.png",
        ],
        "diego_01_high_recall": [
            RAW,
            OVERLAY,
            CROPS / "raw__overview.png",
            CROPS / "raw__top_power_bus_ties_2x.png",
            CROPS / "raw__left_480_loads_2x.png",
            CROPS / "raw__right_480_loads_2x.png",
            CROPS / "raw__left_dc_control_2x.png",
            CROPS / "raw__right_dc_control_2x.png",
            CROPS / "wires_overlay__working_area_2x.png",
            CROPS / "wires_overlay__left_dc_control_2x.png",
            CROPS / "wires_overlay__right_dc_control_2x.png",
        ],
        "jennifer_01_precision": [
            RAW,
            OVERLAY,
            CROPS / "raw__overview.png",
            CROPS / "raw__top_power_bus_ties_2x.png",
            CROPS / "raw__central_ties_2x.png",
            CROPS / "wires_overlay__central_ties_2x.png",
            CROPS / "raw__left_dc_control_2x.png",
            CROPS / "raw__right_dc_control_2x.png",
            CROPS / "wires_overlay__left_dc_control_2x.png",
            CROPS / "wires_overlay__right_dc_control_2x.png",
            CROPS / "wires_overlay__working_area_2x.png",
        ],
        "diego_02_saturation": [
            CROPS / "raw__central_ties_2x.png",
            CROPS / "wires_overlay__central_ties_2x.png",
            CROPS / "raw__left_dc_control_2x.png",
            CROPS / "raw__right_dc_control_2x.png",
            CROPS / "wires_overlay__left_dc_control_2x.png",
            CROPS / "wires_overlay__right_dc_control_2x.png",
        ],
        "jennifer_02_final": [
            CROPS / "raw__central_ties_2x.png",
            CROPS / "wires_overlay__central_ties_2x.png",
            CROPS / "raw__left_dc_control_2x.png",
            CROPS / "raw__right_dc_control_2x.png",
            CROPS / "wires_overlay__working_area_2x.png",
        ],
    }
    specs = [
        ("main_01_visual_orchestration_and_artifacts", "main", "", "orchestration", "gpt-5", 1700, 4200, (2500, 5200, 9000), 0, "main local visual inspection and script writing"),
        ("diego_01_high_recall", "Diego", "019f76d7-661b-75a1-a971-5b83dc21f325", "round_01", "gpt-5.5 xhigh", 2300, 3200, (4200, 8500, 15000), 0, "high-recall subagent; usage object unavailable"),
        ("jennifer_01_precision", "Jennifer", "019f76db-828f-7530-b14b-82eb55ad04ed", "round_01", "gpt-5.5 xhigh", 3400, 2600, (4200, 8000, 14000), 0, "precision-review subagent; usage object unavailable"),
        ("diego_02_saturation", "Diego", "019f76de-51cc-7113-9663-50e27ebeb997", "round_02", "gpt-5.5 xhigh", 1700, 900, (1200, 2500, 4800), 0, "saturation check; usage object unavailable"),
        ("jennifer_02_final", "Jennifer", "019f76df-9679-72d0-807f-b3e6a6d228e0", "round_02", "gpt-5.5 xhigh", 1300, 500, (800, 1700, 3400), 0, "final confirmation; usage object unavailable"),
    ]
    cached = {
        "diego_02_saturation": sum(image_tokens(p) for p in image_sets["diego_01_high_recall"] if p.exists()),
        "jennifer_02_final": sum(image_tokens(p) for p in image_sets["jennifer_01_precision"] if p.exists()),
    }
    rows: list[dict] = []
    for call_id, actor, agent_id, round_name, model, text_in, output, reasoning, cached_text, note in specs:
        image_in = sum(image_tokens(p) for p in image_sets[call_id] if p.exists())
        low = text_in + image_in + output + reasoning[0]
        expected = text_in + image_in + output + reasoning[1]
        high = text_in + image_in + output + reasoning[2]
        rows.append({
            "document": DOC,
            "iteration": ITERATION,
            "call_id": call_id,
            "actor": actor,
            "agent_id": agent_id,
            "round": round_name,
            "model": model,
            "input_tokens_est": text_in,
            "cached_input_tokens_est": cached.get(call_id, cached_text),
            "output_tokens_est": output,
            "reasoning_tokens_available": "no",
            "reasoning_tokens_low_est": reasoning[0],
            "reasoning_tokens_expected_est": reasoning[1],
            "reasoning_tokens_high_est": reasoning[2],
            "image_file_input_tokens_est": image_in,
            "total_tokens_low_est": low,
            "total_tokens_expected_est": expected,
            "total_tokens_high_est": high,
            "usage_object_available": "no",
            "notes": note,
        })
    return rows


def write_token_usage(rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys())
    total = {
        "document": DOC,
        "iteration": ITERATION,
        "call_id": "TOTAL",
        "actor": "all",
        "agent_id": "",
        "round": "all",
        "model": "mixed",
        "input_tokens_est": sum(r["input_tokens_est"] for r in rows),
        "cached_input_tokens_est": sum(r["cached_input_tokens_est"] for r in rows),
        "output_tokens_est": sum(r["output_tokens_est"] for r in rows),
        "reasoning_tokens_available": "no",
        "reasoning_tokens_low_est": sum(r["reasoning_tokens_low_est"] for r in rows),
        "reasoning_tokens_expected_est": sum(r["reasoning_tokens_expected_est"] for r in rows),
        "reasoning_tokens_high_est": sum(r["reasoning_tokens_high_est"] for r in rows),
        "image_file_input_tokens_est": sum(r["image_file_input_tokens_est"] for r in rows),
        "total_tokens_low_est": sum(r["total_tokens_low_est"] for r in rows),
        "total_tokens_expected_est": sum(r["total_tokens_expected_est"] for r in rows),
        "total_tokens_high_est": sum(r["total_tokens_high_est"] for r in rows),
        "usage_object_available": "no",
        "notes": "total local estimate; Responses token-count endpoint unavailable because no API key was provided",
    }
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        writer.writerow(total)
    (RESULTS / "token_usage_estimate.json").write_text(
        json.dumps({"calls": rows, "total": total}, indent=2),
        encoding="utf-8",
    )
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write(f"# Token Usage Estimate - Document {DOC}, Iteration {ITERATION}\n\n")
        f.write("OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.\n\n")
        f.write("Local estimate method: coarse text estimates plus image tokens as 85 + 170 * ceil(width / 512) * ceil(height / 512); reasoning tokens are low/expected/high estimates.\n\n")
        f.write("| document | iteration | low | expected | high | image/file input | cached input |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        f.write(
            f"| {DOC} | {ITERATION} | {total['total_tokens_low_est']} | {total['total_tokens_expected_est']} | {total['total_tokens_high_est']} | {total['image_file_input_tokens_est']} | {total['cached_input_tokens_est']} |\n"
        )


def write_round_outputs() -> dict:
    qas: dict = {}
    for round_name, nodes, power_edges, control_edges, uncertain, note in ROUNDS:
        all_edges = power_edges + control_edges
        matrix, missing = matrix_for(nodes, all_edges)
        round_qa = qa(nodes, all_edges, matrix, missing)
        round_qa["uncertain_edge_count"] = len(uncertain)
        round_qa["note"] = note
        qas[round_name] = round_qa
        write_nodes(RESULTS / f"nodes_{round_name}.csv", nodes)
        write_edges(RESULTS / f"edges_{round_name}.csv", power_edges, control_edges)
        write_uncertain(RESULTS / f"uncertain_edges_{round_name}.csv", uncertain)
        write_matrix(RESULTS / f"connectivity_matrix_{round_name}.csv", nodes, matrix)
        write_sparse(RESULTS / f"connectivity_sparse_{round_name}.csv", nodes, matrix)
    return qas


def write_final_aliases(final_matrix: list[list[int]], final_edges: list[tuple[str, str, str]]) -> None:
    write_nodes(RESULTS / "nodes_final.csv", FINAL_NODES)
    write_edges(RESULTS / "edges_final.csv", POWER_EDGES, FINAL_CONTROL_EDGES)
    write_uncertain(RESULTS / "uncertain_edges_final.csv", UNCERTAIN_FINAL)
    write_matrix(RESULTS / "connectivity_matrix_final.csv", FINAL_NODES, final_matrix)
    write_sparse(RESULTS / "connectivity_sparse_final.csv", FINAL_NODES, final_matrix)
    write_nodes(RESULTS / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS / "final_edgelist.csv", POWER_EDGES, FINAL_CONTROL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, final_matrix)
    write_matrix(RESULTS / "connectivity_matrix.csv", FINAL_NODES, final_matrix)
    (RESULTS / "final_graph.json").write_text(
        json.dumps({
            "document": DOC,
            "iteration": ITERATION,
            "node_count": len(FINAL_NODES),
            "hard_edge_count": len(dedupe_edges(final_edges)),
            "nodes": FINAL_NODES,
            "edges": [
                {"source": a, "target": b, "evidence": evidence}
                for a, b, evidence in dedupe_edges(final_edges)
            ],
            "uncertain_edges": [
                {"source": a, "target": b, "reason": reason}
                for a, b, reason in UNCERTAIN_FINAL
            ],
        }, indent=2),
        encoding="utf-8",
    )


def copy_code_artifacts() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    for name in ("doc36_make_visual_crops.py", "doc36_write_results.py"):
        src = Path(__file__).resolve().with_name(name)
        if src.exists():
            dst = CODES / name
            if src.resolve() != dst.resolve():
                shutil.copy2(src, dst)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    qas = write_round_outputs()
    final_edges = POWER_EDGES + FINAL_CONTROL_EDGES
    final_matrix, final_missing = matrix_for(FINAL_NODES, final_edges)
    final_qa = qa(FINAL_NODES, final_edges, final_matrix, final_missing)
    final_qa["uncertain_edge_count"] = len(UNCERTAIN_FINAL)
    final_qa["rounds"] = qas
    final_qa["raw_resource"] = str(RAW)
    final_qa["overlay_resource"] = str(OVERLAY)
    final_qa["mask_resource"] = str(MASK)
    final_qa["notes"] = [
        "Final matrix includes visible solid power connections and clearly terminated dashed control/interlock paths only.",
        "RPS TRIP and RPS LOCKOUT are treated as text annotations on dashed paths, not final component nodes.",
        "Fan ESF-control taps are not hardened because no clean dashed tap reaches FAN-CONTAIN-A/B.",
        "Only Raw + wires resources were used.",
    ]
    (RESULTS / "qa_final.json").write_text(json.dumps(final_qa, indent=2), encoding="utf-8")
    write_final_aliases(final_matrix, final_edges)

    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as f:
        f.write(f"# Document {DOC} Round Notes\n\n")
        for round_name, _nodes, _power, _control, _uncertain, note in ROUNDS:
            f.write(f"## {round_name}\n\n{note}\n\n")
        f.write("## Saturation Decision\n\n")
        f.write("The final graph keeps all solid power feeders and clean dashed control/interlock paths. RPS TRIP/RPS LOCKOUT remain annotations, and FAN-CONTAIN-A/B dashed-control contacts remain uncertain/excluded.\n")

    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "round", "node_count", "hard_edge_count", "uncertain_edge_count", "note"])
        for round_name, q in qas.items():
            writer.writerow([DOC, ITERATION, round_name, q["node_count"], q["hard_edge_count"], q["uncertain_edge_count"], q["note"]])

    token_rows = token_estimates()
    write_token_usage(token_rows)
    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "final_node_count": final_qa["node_count"],
        "final_hard_edge_count": final_qa["hard_edge_count"],
        "final_uncertain_edge_count": final_qa["uncertain_edge_count"],
        "round_hard_edge_counts": {name: q["hard_edge_count"] for name, q in qas.items()},
        "round_uncertain_edge_counts": {name: q["uncertain_edge_count"] for name, q in qas.items()},
        "files_written": sorted(p.name for p in RESULTS.iterdir() if p.is_file()),
        "generated": datetime.now().isoformat(timespec="seconds"),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    copy_code_artifacts()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
