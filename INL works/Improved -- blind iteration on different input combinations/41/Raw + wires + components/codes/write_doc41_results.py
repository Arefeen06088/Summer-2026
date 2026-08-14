from __future__ import annotations

import csv
import io
import json
import math
import shutil
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires + components"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


FINAL_NODES_TEXT = """
OFFSITE A
TR-1A
CB-101
BUS-1A
EDG-1A
CB-105
CB-TIE-1AB
BUS-1B
CB-102
TR-1B
OFFSITE B
EDG-1B
CB-106
TR-LC-1A
CB-201
BUS-480A
TR-SAF-1A
CB-203
BUS-480E1A
TR-LC-1B
CB-202
BUS-480B
TR-SAF-1B
CB-204
BUS-480E1B
MCC-1A
MCC-1C
MCC-ESS-A
MCC-1B
MCC-1D
MCC-ESS-B
PUMP-CCW-103A
FAN-CRHV-104A
PUMP-SI-101A
PUMP-RHR-102A
MOV-1201A
PUMP-CCW-103B
FAN-CRHV-104B
PUMP-SI-101B
PUMP-RHR-102B
MOV-1201B
CHGR-125A
DC-BUS-125A
BAT-125A
INV-120A
UPS-BUS-A
PANEL-RPS-A
INST-RACK-1
RELAY-K86A
JB-ESF-01
PANEL-RPS-B
RELAY-K86B
CHGR-125B
DC-BUS-125B
BAT-125B
INV-120B
UPS-BUS-B
""".strip()


DIEGO_R1_NODES_TEXT = """
OFFSITE A
TR-1A
GND-1E
CB-101
BUS-1A
EDG-1A
CB-105
CB-TIE-1AB
BUS-1B
CB-102
TR-1B
OFFSITE B
EDG-1B
CB-106
TR-LC-1A
CB-201
BUS-480A
TR-SAF-1A
CB-203
BUS-480E1A
TR-LC-1B
CB-202
BUS-480B
TR-SAF-1B
CB-204
BUS-480E1B
MCC-1A
MCC-1C
MCC-ESS-A
MCC-1B
MCC-1D
MCC-ESS-B
PUMP-CCW-103A
FAN-CRHV-104A
PUMP-SI-101A
PUMP-RHR-102A
MOV-1201A
PUMP-CCW-103B
FAN-CRHV-104B
PUMP-SI-101B
PUMP-RHR-102B
MOV-1201B
CHGR-125A
DC-BUS-125A
BAT-125A
INV-120A
UPS-BUS-A
PANEL-RPS-A
INST-RACK-1
RELAY-K86A
JB-ESF-01
PANEL-RPS-B
RELAY-K86B
CHGR-125B
DC-BUS-125B
BAT-125B
INV-120B
UPS-BUS-B
""".strip()


FINAL_EDGES_CSV = """source,target,type,confidence,evidence
OFFSITE A,TR-1A,power,0.95,solid source line to transformer primary
TR-1A,CB-101,power,0.95,solid transformer secondary to breaker
CB-101,BUS-1A,power,0.95,breaker output lands on BUS-1A
EDG-1A,CB-105,power,0.95,solid EDG feeder into breaker
CB-105,BUS-1A,power,0.95,breaker output to EDG A incoming bus tap
BUS-1A,CB-TIE-1AB,power,0.95,solid bus end to tie breaker
CB-TIE-1AB,BUS-1B,power,0.95,tie breaker output to BUS-1B
BUS-1B,CB-102,power,0.95,solid bus end to breaker
CB-102,TR-1B,power,0.95,breaker output to transformer
TR-1B,OFFSITE B,power,0.95,solid transformer primary to source
EDG-1B,CB-106,power,0.95,solid EDG feeder into breaker
CB-106,BUS-1B,power,0.95,breaker output to EDG B incoming bus tap
BUS-1A,TR-LC-1A,power,0.90,solid feeder drops from BUS-1A to transformer
TR-LC-1A,CB-201,power,0.95,transformer secondary to breaker
CB-201,BUS-480A,power,0.95,breaker output to BUS-480A
BUS-1A,TR-SAF-1A,power,0.90,solid feeder drops from BUS-1A to transformer
TR-SAF-1A,CB-203,power,0.95,transformer secondary to breaker
CB-203,BUS-480E1A,power,0.95,breaker output to BUS-480E1A
BUS-1B,TR-LC-1B,power,0.90,solid feeder drops from BUS-1B to transformer
TR-LC-1B,CB-202,power,0.95,transformer secondary to breaker
CB-202,BUS-480B,power,0.95,breaker output to BUS-480B
BUS-1B,TR-SAF-1B,power,0.90,solid feeder drops from BUS-1B to transformer
TR-SAF-1B,CB-204,power,0.95,transformer secondary to breaker
CB-204,BUS-480E1B,power,0.95,breaker output to BUS-480E1B
BUS-480A,MCC-1A,power,0.95,solid branch from bus to MCC
MCC-1A,PUMP-CCW-103A,power,0.95,solid feeder from MCC to pump
BUS-480A,MCC-1C,power,0.95,solid branch from bus to MCC
MCC-1C,FAN-CRHV-104A,power,0.95,solid feeder from MCC to fan
BUS-480E1A,MCC-ESS-A,power,0.95,solid branch from bus to MCC
MCC-ESS-A,PUMP-SI-101A,power,0.95,solid feeder from MCC to pump
MCC-ESS-A,PUMP-RHR-102A,power,0.95,solid feeder from MCC to pump
MCC-ESS-A,MOV-1201A,power,0.95,solid feeder from MCC to MOV
BUS-480B,MCC-1B,power,0.95,solid branch from bus to MCC
MCC-1B,PUMP-CCW-103B,power,0.95,solid feeder from MCC to pump
BUS-480B,MCC-1D,power,0.95,solid branch from bus to MCC
MCC-1D,FAN-CRHV-104B,power,0.95,solid feeder from MCC to fan
BUS-480E1B,MCC-ESS-B,power,0.95,solid branch from bus to MCC
MCC-ESS-B,PUMP-SI-101B,power,0.95,solid feeder from MCC to pump
MCC-ESS-B,PUMP-RHR-102B,power,0.95,solid feeder from MCC to pump
MCC-ESS-B,MOV-1201B,power,0.95,solid feeder from MCC to MOV
BUS-480A,CHGR-125A,power,0.85,solid feeder via left BUS-480A cable path
CHGR-125A,DC-BUS-125A,power,0.95,charger DC side to DC bus
BAT-125A,DC-BUS-125A,power,0.95,battery lead to DC bus
DC-BUS-125A,INV-120A,power,0.95,DC bus to inverter
INV-120A,UPS-BUS-A,power,0.95,inverter output to UPS bus
UPS-BUS-A,PANEL-RPS-A,power,0.90,solid feeder from UPS bus to panel
UPS-BUS-A,INST-RACK-1,power,0.90,solid feeder from UPS bus to rack top port
BUS-480E1B,CHGR-125B,power,0.85,solid feeder via right BUS-480E1B cable path
CHGR-125B,DC-BUS-125B,power,0.95,charger DC side to DC bus
BAT-125B,DC-BUS-125B,power,0.95,battery lead to DC bus
DC-BUS-125B,INV-120B,power,0.95,DC bus to inverter
INV-120B,UPS-BUS-B,power,0.95,inverter output to UPS bus
UPS-BUS-B,PANEL-RPS-B,power,0.90,solid feeder from UPS bus to panel
CB-105,RELAY-K86A,control/interlock,0.85,dashed control line to relay port
RELAY-K86A,PANEL-RPS-A,control/interlock,0.90,dashed vertical line from relay to panel port
PANEL-RPS-A,JB-ESF-01,control/interlock,0.90,dashed line from panel to JB left port
JB-ESF-01,PANEL-RPS-B,control/interlock,0.90,dashed line from JB right port to panel
PANEL-RPS-B,RELAY-K86B,control/interlock,0.90,dashed vertical line from panel port to relay
RELAY-K86B,CB-106,control/interlock,0.85,dashed control line from relay port to breaker
"""


DIEGO_R1_EDGES_CSV = """source,target,type,confidence,evidence
OFFSITE A,TR-1A,power,0.95,solid feeder from offsite source symbol to transformer primary terminals
TR-1A,CB-101,power,0.95,solid feeder from transformer secondary to CB-101
CB-101,BUS-1A,power,0.97,CB-101 output lands on BUS-1A left side
TR-1A,GND-1E,grounding,0.90,ground conductor from TR-1A bottom terminal to GND-1E symbol
EDG-1A,CB-105,power,0.95,solid feeder from EDG-1A output terminal to CB-105
CB-105,BUS-1A,power,0.94,CB-105 output joins BUS-1A via EDG A incoming feeder
BUS-1A,CB-TIE-1AB,power,0.95,BUS-1A right end connects to bus tie breaker port
CB-TIE-1AB,BUS-1B,power,0.95,bus tie breaker right port connects to BUS-1B
BUS-1B,CB-102,power,0.97,BUS-1B right side connects to CB-102
CB-102,TR-1B,power,0.95,CB-102 output connects to TR-1B secondary
TR-1B,OFFSITE B,power,0.95,TR-1B primary connects to offsite B source terminals
EDG-1B,CB-106,power,0.95,solid feeder from EDG-1B terminal to CB-106
CB-106,BUS-1B,power,0.94,CB-106 output lands on BUS-1B via EDG B incoming feeder
BUS-1A,TR-LC-1A,power,0.93,vertical tap from BUS-1A to TR-LC-1A primary
TR-LC-1A,CB-201,power,0.95,transformer secondary feeds CB-201
CB-201,BUS-480A,power,0.97,CB-201 lower feeder lands on BUS-480A
BUS-1A,TR-SAF-1A,power,0.93,vertical tap from BUS-1A to TR-SAF-1A primary
TR-SAF-1A,CB-203,power,0.95,TR-SAF-1A secondary feeds CB-203
CB-203,BUS-480E1A,power,0.97,CB-203 lower feeder lands on BUS-480E1A
BUS-1B,TR-LC-1B,power,0.93,vertical tap from BUS-1B to TR-LC-1B primary
TR-LC-1B,CB-202,power,0.95,TR-LC-1B secondary feeds CB-202
CB-202,BUS-480B,power,0.97,CB-202 lower feeder lands on BUS-480B
BUS-1B,TR-SAF-1B,power,0.90,right train vertical tap visually feeds TR-SAF-1B primary
TR-SAF-1B,CB-204,power,0.95,TR-SAF-1B secondary feeds CB-204
CB-204,BUS-480E1B,power,0.97,CB-204 lower feeder lands on BUS-480E1B
BUS-480A,MCC-1A,power,0.96,vertical feeder from BUS-480A to MCC-1A top port
MCC-1A,PUMP-CCW-103A,power,0.96,solid feeder from MCC-1A bottom to pump terminal
BUS-480A,MCC-1C,power,0.96,vertical feeder from BUS-480A to MCC-1C top port
MCC-1C,FAN-CRHV-104A,power,0.96,solid feeder from MCC-1C bottom to fan terminal
BUS-480E1A,MCC-ESS-A,power,0.96,vertical feeder from BUS-480E1A to MCC-ESS-A
MCC-ESS-A,PUMP-SI-101A,power,0.95,left bottom feeder from MCC-ESS-A to pump
MCC-ESS-A,PUMP-RHR-102A,power,0.95,middle bottom feeder from MCC-ESS-A to pump
MCC-ESS-A,MOV-1201A,power,0.92,right bottom feeder from MCC-ESS-A to MOV symbol
BUS-480B,MCC-1B,power,0.96,vertical feeder from BUS-480B to MCC-1B
MCC-1B,PUMP-CCW-103B,power,0.96,solid feeder from MCC-1B bottom to pump
BUS-480B,MCC-1D,power,0.96,vertical feeder from BUS-480B to MCC-1D
MCC-1D,FAN-CRHV-104B,power,0.96,solid feeder from MCC-1D bottom to fan
BUS-480E1B,MCC-ESS-B,power,0.96,vertical feeder from BUS-480E1B to MCC-ESS-B
MCC-ESS-B,PUMP-SI-101B,power,0.95,left bottom feeder from MCC-ESS-B to pump
MCC-ESS-B,PUMP-RHR-102B,power,0.95,middle bottom feeder from MCC-ESS-B to pump
MCC-ESS-B,MOV-1201B,power,0.92,right bottom feeder from MCC-ESS-B to MOV
BUS-480A,CHGR-125A,power,0.78,long solid cable route from BUS-480A side to CHGR-125A
CHGR-125A,DC-BUS-125A,power,0.95,charger DC output lands on DC-BUS-125A
BAT-125A,DC-BUS-125A,power,0.95,battery feeder lands on lower side of DC-BUS-125A
DC-BUS-125A,INV-120A,power,0.96,right side of DC-BUS-125A connects to INV-120A
INV-120A,UPS-BUS-A,power,0.96,INV-120A output connects to UPS-BUS-A
UPS-BUS-A,PANEL-RPS-A,power,0.90,short solid branch from UPS-BUS-A area to PANEL-RPS-A bottom
UPS-BUS-A,INST-RACK-1,power,0.90,solid branch from UPS-BUS-A output drops to INST-RACK-1
BUS-480E1B,CHGR-125B,power,0.78,right-side solid cable route from BUS-480E1B area to CHGR-125B
CHGR-125B,DC-BUS-125B,power,0.95,charger DC output lands on DC-BUS-125B
BAT-125B,DC-BUS-125B,power,0.95,battery feeder lands on lower side of DC-BUS-125B
DC-BUS-125B,INV-120B,power,0.96,left side of DC-BUS-125B connects to INV-120B
INV-120B,UPS-BUS-B,power,0.96,INV-120B output connects to UPS-BUS-B
UPS-BUS-B,PANEL-RPS-B,power,0.90,short solid branch from UPS-BUS-B to PANEL-RPS-B bottom
CB-105,RELAY-K86A,control/interlock,0.86,dashed CTRL-86A route from CB-105 bottom continues to K86A relay port
RELAY-K86A,PANEL-RPS-A,control/interlock,0.92,dashed vertical/bracket connection from relay to RPS-A panel side
JB-ESF-01,PANEL-RPS-A,control/interlock,0.88,dashed line from JB-ESF-01 left side to PANEL-RPS-A top/side
JB-ESF-01,PANEL-RPS-B,control/interlock,0.88,dashed line from JB-ESF-01 right side to PANEL-RPS-B top/side
RELAY-K86B,PANEL-RPS-B,control/interlock,0.92,dashed vertical/bracket connection from relay to RPS-B panel side
CB-106,RELAY-K86B,control/interlock,0.86,dashed CTRL-86B route from CB-106 bottom continues to K86B relay port
"""


EXCLUSIONS = [
    ("GND-1E", "node", "excluded", "ground/reference symbol tied to TR-1A, not peer equipment matrix node"),
    ("TR-1A--GND-1E", "edge", "excluded", "visual grounding annotation, excluded with GND-1E node"),
    ("UPS-BUS-B--INST-RACK-1", "edge", "excluded", "no terminal-supported feeder from B UPS bus to rack"),
    ("PANEL-RPS-A--PANEL-RPS-B", "edge", "excluded", "control path visibly passes through JB-ESF-01"),
    ("RELAY-K86A--JB-ESF-01", "edge", "excluded", "PANEL-RPS-A is visible intermediate endpoint"),
    ("RELAY-K86B--JB-ESF-01", "edge", "excluded", "PANEL-RPS-B is visible intermediate endpoint"),
    ("BUS-1A--BUS-1B", "edge", "excluded", "CB-TIE-1AB is between the buses"),
    ("CABLE 1A-480-7 / CABLE 1B-480-9", "node", "excluded", "cable callouts only"),
    ("FDR A-DC / FDR B-DC", "node", "excluded", "feeder labels only"),
    ("PT / UV / SEQ", "node", "excluded", "internal markings inside INST-RACK-1, not external endpoints"),
    ("title block, terminal block schedule, notes, grid labels", "node", "excluded", "metadata/annotation, not connectivity endpoints"),
]


def split_nodes(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_edges(text: str) -> list[dict[str, str]]:
    return [dict(row) for row in csv.DictReader(io.StringIO(text.strip()))]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for row in edges:
        a, b = row["source"], row["target"]
        if a not in index or b not in index:
            continue
        if a == b:
            continue
        matrix[index[a]][index[b]] = 1
        matrix[index[b]][index[a]] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, values in zip(nodes, matrix):
            writer.writerow([node] + values)
    return matrix


def validate(nodes: list[str], edges: list[dict[str, str]], matrix: list[list[int]]) -> dict[str, object]:
    node_set = set(nodes)
    unknown = sorted(
        {
            endpoint
            for row in edges
            for endpoint in (row["source"], row["target"])
            if endpoint not in node_set
        }
    )
    seen: set[tuple[str, str]] = set()
    duplicates = 0
    for row in edges:
        key = tuple(sorted((row["source"], row["target"])))
        if key in seen:
            duplicates += 1
        seen.add(key)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unknown_nodes": unknown,
        "duplicate_undirected_edges": duplicates,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "matrix_header_nodes": len(nodes),
    }


def image_tokens(paths: list[str]) -> int:
    total = 0
    for name in paths:
        path = CROPS / name
        if not path.exists():
            continue
        with Image.open(path) as im:
            w, h = im.size
        # Local no-API estimate: high-detail image cost approximated as 85 + 170 per 512px tile.
        total += 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)
    return total


def token_rows() -> list[dict[str, object]]:
    diego_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "focus_top_distribution_raw.png",
        "focus_middle_distribution_raw.png",
        "focus_lower_distribution_raw.png",
        "focus_dc_controls_raw.png",
        "detail_00_wires_overlay.png",
        "detail_01_wires_overlay.png",
        "detail_02_wires_overlay.png",
        "detail_05_wires_overlay.png",
    ]
    jennifer_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "focus_top_distribution_raw.png",
        "focus_middle_distribution_raw.png",
        "focus_lower_distribution_wires_overlay.png",
        "focus_dc_controls_wires_overlay.png",
        "detail_15_wires_overlay.png",
        "detail_16_wires_overlay.png",
        "detail_17_wires_overlay.png",
        "detail_20_wires_overlay.png",
        "detail_21_wires_overlay.png",
    ]
    main_images = sorted(
        {
            "raw_full_thumb.png",
            "components_full_thumb.png",
            "wires_overlay_full_thumb.png",
            "focus_top_distribution_raw.png",
            "focus_middle_distribution_raw.png",
            "focus_lower_distribution_raw.png",
            "focus_dc_controls_raw.png",
            "focus_dc_controls_wires_overlay.png",
            "focus_left_loads_wires_overlay.png",
            "focus_right_loads_wires_overlay.png",
            "focus_lower_distribution_wires_overlay.png",
            "detail_00_wires_overlay.png",
            "detail_01_wires_overlay.png",
            "detail_02_wires_overlay.png",
            "detail_03_wires_overlay.png",
            "detail_05_wires_overlay.png",
            "detail_15_wires_overlay.png",
            "detail_16_wires_overlay.png",
            "detail_17_wires_overlay.png",
            "detail_20_wires_overlay.png",
            "detail_21_wires_overlay.png",
            "detail_00_components.png",
            "detail_16_components.png",
        }
    )
    raw_rows = [
        {
            "document": "41",
            "iteration": "1",
            "call_id": "main_doc41_01",
            "round": "main-prep-and-local-visual-review",
            "model_call": "main_agent_resource_inspection_crop_generation_visual_review",
            "input_text_tokens_est": 5200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_tokens(main_images),
            "output_tokens_low": 700,
            "output_tokens_expected": 1300,
            "output_tokens_high": 2200,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent inspected resources, generated crops, and reviewed full/focus/detail visual crops.",
        },
        {
            "document": "41",
            "iteration": "1",
            "call_id": "diego_doc41_r1",
            "round": "round_01_diego",
            "model_call": "Diego high-recall extractor",
            "input_text_tokens_est": 3900,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_tokens(diego_images),
            "output_tokens_low": 4200,
            "output_tokens_expected": 6000,
            "output_tokens_high": 8200,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Diego proposed all visually/geometrically plausible nodes and edges.",
        },
        {
            "document": "41",
            "iteration": "1",
            "call_id": "jennifer_doc41_r2",
            "round": "round_02_jennifer",
            "model_call": "Jennifer precision reviewer/refiner",
            "input_text_tokens_est": 8600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_tokens(jennifer_images),
            "output_tokens_low": 2600,
            "output_tokens_expected": 3800,
            "output_tokens_high": 5500,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Jennifer reviewed Diego R1, removed ground/reference node, and refined dashed control chain.",
        },
        {
            "document": "41",
            "iteration": "1",
            "call_id": "diego_doc41_r3",
            "round": "round_03_diego",
            "model_call": "Diego convergence reconciliation",
            "input_text_tokens_est": 3600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 1700,
            "output_tokens_expected": 2500,
            "output_tokens_high": 3600,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Diego accepted Jennifer's refined graph and restated the agreed edge CSV.",
        },
        {
            "document": "41",
            "iteration": "1",
            "call_id": "jennifer_doc41_r4",
            "round": "round_04_jennifer_final",
            "model_call": "Jennifer final saturation check",
            "input_text_tokens_est": 1000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 150,
            "output_tokens_expected": 280,
            "output_tokens_high": 500,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Jennifer confirmed saturation after Diego R2 agreement.",
        },
        {
            "document": "41",
            "iteration": "1",
            "call_id": "main_doc41_02",
            "round": "main-final-artifact-write",
            "model_call": "main_agent_write_validate_report",
            "input_text_tokens_est": 4800,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1500,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent wrote matrices/reports, validated symmetry/diagonal, and prepared final response.",
        },
    ]
    for row in raw_rows:
        row["total_tokens_low"] = (
            int(row["input_text_tokens_est"])
            + int(row["cached_input_tokens_est"])
            + int(row["image_file_input_tokens_est"])
            + int(row["output_tokens_low"])
        )
        row["total_tokens_expected"] = (
            int(row["input_text_tokens_est"])
            + int(row["cached_input_tokens_est"])
            + int(row["image_file_input_tokens_est"])
            + int(row["output_tokens_expected"])
        )
        row["total_tokens_high"] = (
            int(row["input_text_tokens_est"])
            + int(row["cached_input_tokens_est"])
            + int(row["image_file_input_tokens_est"])
            + int(row["output_tokens_high"])
        )
    return raw_rows


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), CODES / "write_doc41_results.py")

    final_nodes = split_nodes(FINAL_NODES_TEXT)
    diego_r1_nodes = split_nodes(DIEGO_R1_NODES_TEXT)
    final_edges = parse_edges(FINAL_EDGES_CSV)
    diego_r1_edges = parse_edges(DIEGO_R1_EDGES_CSV)

    rounds = [
        ("round_01_diego", diego_r1_nodes, diego_r1_edges),
        ("round_02_jennifer", final_nodes, final_edges),
        ("round_03_diego", final_nodes, final_edges),
        ("round_04_jennifer_final", final_nodes, final_edges),
    ]

    round_validations: dict[str, dict[str, object]] = {}
    for name, nodes, edges in rounds:
        write_csv(RESULTS / f"{name}_edges.csv", edges, ["source", "target", "type", "confidence", "evidence"])
        matrix = write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)
        round_validations[name] = validate(nodes, edges, matrix)

    write_csv(
        RESULTS / "final_node_order.csv",
        [{"index": i + 1, "node": node} for i, node in enumerate(final_nodes)],
        ["index", "node"],
    )
    write_csv(RESULTS / "final_edges.csv", final_edges, ["source", "target", "type", "confidence", "evidence"])
    final_matrix = write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    final_validation = validate(final_nodes, final_edges, final_matrix)

    write_csv(
        RESULTS / "uncertain_or_excluded_edges.csv",
        [
            {"candidate": item, "kind": kind, "decision": decision, "reason": reason}
            for item, kind, decision, reason in EXCLUSIONS
        ],
        ["candidate", "kind", "decision", "reason"],
    )

    (RESULTS / "round_01_diego_notes.md").write_text(
        "Diego high-recall round included GND-1E as a grounding node and used direct JB-to-panel interlock edges while excluding cable labels and annotations.\n",
        encoding="utf-8",
    )
    (RESULTS / "round_02_jennifer_review.md").write_text(
        "Jennifer removed GND-1E as a reference/ground symbol, kept charger AC source edges, kept only UPS-BUS-A to INST-RACK-1, and refined the dashed interlock chain through panels and JB.\n",
        encoding="utf-8",
    )
    (RESULTS / "round_03_diego_reconciliation.md").write_text(
        "Diego agreed exactly with Jennifer's refined graph and restated the same 57-node, 59-edge matrix-ready graph.\n",
        encoding="utf-8",
    )
    (RESULTS / "round_04_jennifer_final_saturation_check.md").write_text(
        "Jennifer final saturation check confirmed Diego and Jennifer agree on the final graph; no additional precision changes were needed.\n",
        encoding="utf-8",
    )

    tokens = token_rows()
    token_fields = [
        "document",
        "iteration",
        "call_id",
        "round",
        "model_call",
        "input_text_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens",
        "usage_object",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "notes",
    ]
    write_csv(RESULTS / "token_usage_estimate.csv", tokens, token_fields)
    token_summary = {
        "document": "41",
        "iteration": "1",
        "calls": tokens,
        "method": (
            "No API key was available, so the OpenAI Responses input-token counting endpoint "
            "could not be called. Text tokens are estimated locally; image/file input tokens "
            "use an approximate high-detail vision formula of 85 + 170 per 512px tile for each "
            "image file passed or visually inspected."
        ),
        "low": sum(int(row["total_tokens_low"]) for row in tokens),
        "expected": sum(int(row["total_tokens_expected"]) for row in tokens),
        "high": sum(int(row["total_tokens_high"]) for row in tokens),
    }
    write_csv(
        RESULTS / "token_usage_summary.csv",
        [
            {
                "document": "41",
                "iteration": "1",
                "total_tokens_low": token_summary["low"],
                "total_tokens_expected": token_summary["expected"],
                "total_tokens_high": token_summary["high"],
                "method": "local estimate; Responses counting endpoint unavailable without API key",
            }
        ],
        ["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"],
    )
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(token_summary, indent=2), encoding="utf-8")

    summary = {
        "document": "41",
        "iteration": "1",
        "rounds": {
            name: {"nodes": data["nodes"], "edges": data["edges"]} for name, data in round_validations.items()
        },
        "final": final_validation,
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
        "token_usage": {
            "low": token_summary["low"],
            "expected": token_summary["expected"],
            "high": token_summary["high"],
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    report = f"""# Document 41 Connectivity Extraction

Blind extraction used only the document 41 input resources and derived visual aids. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Saturated Result

- Final node count: {final_validation["nodes"]}
- Final undirected edge count: {final_validation["edges"]}
- Matrix: final_connectivity_matrix.csv
- Edge list: final_edges.csv
- Symmetric: {final_validation["symmetric"]}
- Diagonal zero: {final_validation["diagonal_zero"]}
- Duplicate undirected edges: {final_validation["duplicate_undirected_edges"]}
- Unknown edge endpoints: {len(final_validation["unknown_nodes"])}

## Round Progress

- Round 01 Diego: high-recall graph, {round_validations["round_01_diego"]["nodes"]} nodes, {round_validations["round_01_diego"]["edges"]} edges.
- Round 02 Jennifer: precision-refined graph, {round_validations["round_02_jennifer"]["nodes"]} nodes, {round_validations["round_02_jennifer"]["edges"]} edges.
- Round 03 Diego: agreed with Jennifer's refined graph.
- Round 04 Jennifer final: saturation confirmed.

## Key Precision Decisions

- Excluded GND-1E as a ground/reference symbol rather than a peer matrix node.
- Excluded cable labels, feeder callouts, title block, terminal schedule, notes, and grid labels.
- Kept charger AC source edges from BUS-480A to CHGR-125A and BUS-480E1B to CHGR-125B.
- Kept only UPS-BUS-A to INST-RACK-1; no supported UPS-BUS-B to INST-RACK-1 edge.
- Routed the lower dashed interlock as CB-105 - RELAY-K86A - PANEL-RPS-A - JB-ESF-01 - PANEL-RPS-B - RELAY-K86B - CB-106.

## Token Accounting

Usage objects were not exposed by the subagent tool or main-agent interface. The token files provide low/expected/high local estimates, with image/file tokens estimated from crop dimensions because no API key was available for the Responses counting endpoint.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
