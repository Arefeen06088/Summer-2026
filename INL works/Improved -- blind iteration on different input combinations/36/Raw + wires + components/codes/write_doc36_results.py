from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + components")
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


DIEGO_NODES = [
    "GRID-230-A",
    "CB-SW-A",
    "TR-SU-A",
    "SU-A",
    "GEN-DG-A",
    "CB-DG-A",
    "TR-EDG-A",
    "EDG-A",
    "BUS-13K-A",
    "CB-13-TIE",
    "BUS-13K-B",
    "SU-B",
    "TR-SU-B",
    "CB-SW-B",
    "GRID-230-B",
    "EDG-B",
    "TR-EDG-B",
    "CB-DG-B",
    "GEN-DG-B",
    "TR-4K-A",
    "CB-4K-A",
    "BUS-4K-A",
    "CB-4K-TIE",
    "RPS-LOCKOUT",
    "RPS-TRIP",
    "PNL-RPS-1",
    "BUS-4K-B",
    "CB-4K-B",
    "TR-4K-B",
    "TR-480-A",
    "CB-LC-A",
    "BUS-480-A",
    "LC-A1",
    "MCC-01A",
    "PUMP-RHR-A",
    "MOTOR-CCW-A",
    "LC-A2",
    "MCC-02A",
    "PUMP-AFW-A",
    "MOV-A",
    "VALVE-MOV-A",
    "FAN-CONTAIN-A",
    "JB-ESF-A",
    "PNL-ESF-A",
    "ESF-A-CONTROL-TRUNK",
    "RECT-125A",
    "BUS-DC125-A",
    "BAT-125A",
    "INV-120A",
    "TR-480-B",
    "CB-LC-B",
    "BUS-480-B",
    "LC-B1",
    "MCC-01B",
    "PUMP-RHR-B",
    "MOTOR-CCW-B",
    "LC-B2",
    "MCC-02B",
    "PUMP-AFW-B",
    "MOV-B",
    "VALVE-MOV-B",
    "FAN-CONTAIN-B",
    "JB-ESF-B",
    "PNL-ESF-B",
    "ESF-B-CONTROL-TRUNK",
    "RECT-125B",
    "BUS-DC125-B",
    "BAT-125B",
    "INV-120B",
]


FINAL_NODES = [
    "GRID-230-A",
    "CB-SW-A",
    "TR-SU-A",
    "GEN-DG-A",
    "CB-DG-A",
    "TR-EDG-A",
    "BUS-13K-A",
    "CB-13-TIE",
    "BUS-13K-B",
    "TR-SU-B",
    "CB-SW-B",
    "GRID-230-B",
    "TR-EDG-B",
    "CB-DG-B",
    "GEN-DG-B",
    "TR-4K-A",
    "CB-4K-A",
    "BUS-4K-A",
    "CB-4K-TIE",
    "PNL-RPS-1",
    "BUS-4K-B",
    "CB-4K-B",
    "TR-4K-B",
    "TR-480-A",
    "CB-LC-A",
    "BUS-480-A",
    "MCC-01A",
    "PUMP-RHR-A",
    "MOTOR-CCW-A",
    "MCC-02A",
    "PUMP-AFW-A",
    "VALVE-MOV-A",
    "FAN-CONTAIN-A",
    "JB-ESF-A",
    "PNL-ESF-A",
    "RECT-125A",
    "BUS-DC125-A",
    "BAT-125A",
    "INV-120A",
    "TR-480-B",
    "CB-LC-B",
    "BUS-480-B",
    "MCC-01B",
    "PUMP-RHR-B",
    "MOTOR-CCW-B",
    "MCC-02B",
    "PUMP-AFW-B",
    "VALVE-MOV-B",
    "FAN-CONTAIN-B",
    "JB-ESF-B",
    "PNL-ESF-B",
    "RECT-125B",
    "BUS-DC125-B",
    "BAT-125B",
    "INV-120B",
]


def edge(source: str, target: str, evidence: str, confidence: str) -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "evidence": evidence,
        "confidence": confidence,
    }


def diego_round1_edges() -> list[dict[str, str]]:
    return [
        edge("GRID-230-A", "CB-SW-A", "solid feeder from grid symbol to breaker", "0.98"),
        edge("CB-SW-A", "TR-SU-A", "solid feeder from breaker to source transformer", "0.98"),
        edge("TR-SU-A", "SU-A", "solid feeder exits transformer and drops to SU-A tap", "0.96"),
        edge("SU-A", "BUS-13K-A", "SU-A feeder lands on left 13.8 kV bus section", "0.96"),
        edge("GEN-DG-A", "CB-DG-A", "solid feeder from DG symbol to breaker", "0.98"),
        edge("CB-DG-A", "TR-EDG-A", "solid feeder from breaker to EDG transformer", "0.98"),
        edge("TR-EDG-A", "EDG-A", "solid feeder exits transformer toward EDG-A tap", "0.96"),
        edge("EDG-A", "BUS-13K-A", "EDG-A tap enters BUS-13K-A", "0.96"),
        edge("BUS-13K-A", "CB-13-TIE", "left 13.8 kV bus terminates at tie breaker", "0.98"),
        edge("CB-13-TIE", "BUS-13K-B", "tie breaker continues to right 13.8 kV bus; labeled TIE OPEN", "0.98"),
        edge("BUS-13K-B", "SU-B", "right 13.8 kV bus has SU-B source tap", "0.96"),
        edge("SU-B", "TR-SU-B", "solid feeder rises to source transformer B", "0.96"),
        edge("TR-SU-B", "CB-SW-B", "solid feeder from transformer to breaker", "0.98"),
        edge("CB-SW-B", "GRID-230-B", "solid feeder from breaker to grid symbol", "0.98"),
        edge("BUS-13K-B", "EDG-B", "EDG-B tap on right 13.8 kV bus", "0.96"),
        edge("EDG-B", "TR-EDG-B", "solid feeder from bus tap to EDG transformer", "0.96"),
        edge("TR-EDG-B", "CB-DG-B", "solid feeder from transformer to breaker", "0.98"),
        edge("CB-DG-B", "GEN-DG-B", "solid feeder from breaker to DG symbol", "0.98"),
        edge("BUS-13K-A", "TR-4K-A", "vertical solid feeder from BUS-13K-A to TR-4K-A", "0.98"),
        edge("TR-4K-A", "CB-4K-A", "solid vertical feeder through transformer to breaker", "0.98"),
        edge("CB-4K-A", "BUS-4K-A", "breaker bottom lands on 4.16 kV bus with tap dot", "0.98"),
        edge("BUS-13K-B", "TR-4K-B", "vertical solid feeder from BUS-13K-B to TR-4K-B", "0.98"),
        edge("TR-4K-B", "CB-4K-B", "solid vertical feeder through transformer to breaker", "0.98"),
        edge("CB-4K-B", "BUS-4K-B", "breaker bottom lands on 4.16 kV bus with tap dot", "0.98"),
        edge("BUS-4K-A", "CB-4K-TIE", "left 4.16 kV bus connects to tie breaker side terminal", "0.97"),
        edge("CB-4K-TIE", "BUS-4K-B", "tie breaker side terminal connects to right 4.16 kV bus", "0.97"),
        edge("CB-4K-TIE", "RPS-LOCKOUT", "lockout label directly under tie breaker with short vertical control/terminal line", "0.82"),
        edge("RPS-LOCKOUT", "PNL-RPS-1", "solid vertical line from lockout area to RPS panel top", "0.90"),
        edge("CB-13-TIE", "RPS-TRIP", "dashed control route drops from CB-13-TIE area to RPS TRIP label", "0.72"),
        edge("RPS-TRIP", "PNL-RPS-1", "dashed route visually continues toward left side of PNL-RPS-1", "0.62"),
        edge("BUS-4K-A", "TR-480-A", "vertical solid tap from 4.16 kV A bus to TR-480-A", "0.98"),
        edge("TR-480-A", "CB-LC-A", "solid feeder from transformer to load-center breaker", "0.98"),
        edge("CB-LC-A", "BUS-480-A", "breaker output lands on 480 V load-center bus", "0.98"),
        edge("BUS-480-A", "LC-A1", "filled bus tap labeled LC-A1", "0.96"),
        edge("LC-A1", "MCC-01A", "vertical solid feeder from LC-A1 tap to MCC-01A", "0.98"),
        edge("MCC-01A", "PUMP-RHR-A", "solid branch from MCC-01A to pump", "0.97"),
        edge("MCC-01A", "MOTOR-CCW-A", "solid branch from MCC-01A to motor", "0.97"),
        edge("BUS-480-A", "LC-A2", "filled bus tap labeled LC-A2", "0.96"),
        edge("LC-A2", "MCC-02A", "vertical solid feeder from LC-A2 tap to MCC-02A", "0.98"),
        edge("MCC-02A", "PUMP-AFW-A", "solid branch from MCC-02A to AFW pump", "0.97"),
        edge("MCC-02A", "MOV-A", "solid branch from MCC-02A to small MOV box over valve", "0.94"),
        edge("MOV-A", "VALVE-MOV-A", "short solid vertical from MOV box to valve", "0.96"),
        edge("MCC-02A", "FAN-CONTAIN-A", "solid branch from MCC-02A to containment fan", "0.96"),
        edge("BUS-480-A", "RECT-125A", "left end of 480 V bus routes down to rectifier AC side", "0.93"),
        edge("RECT-125A", "BUS-DC125-A", "rectifier DC side connects to 125 VDC A bus", "0.98"),
        edge("BUS-DC125-A", "BAT-125A", "filled vertical tap from DC bus to battery", "0.98"),
        edge("BUS-DC125-A", "INV-120A", "DC bus continues to inverter DC side", "0.98"),
        edge("JB-ESF-A", "PNL-ESF-A", "short vertical dashed/control drop from JB to matching ESF panel", "0.86"),
        edge("PNL-ESF-A", "INV-120A", "solid routed line from PNL-ESF-A bottom to INV-120A top", "0.90"),
        edge("PNL-ESF-A", "ESF-A-CONTROL-TRUNK", "dashed side stubs at panel enter lower dashed route", "0.55"),
        edge("ESF-A-CONTROL-TRUNK", "PUMP-AFW-A", "short dashed drop visually reaches lower dashed route near AFW-A", "0.50"),
        edge("ESF-A-CONTROL-TRUNK", "VALVE-MOV-A", "short dashed drop visually reaches lower dashed route near MOV-A valve", "0.50"),
        edge("ESF-A-CONTROL-TRUNK", "FAN-CONTAIN-A", "lower dashed route passes under/near fan A label", "0.38"),
        edge("BUS-4K-B", "TR-480-B", "vertical solid tap from 4.16 kV B bus to TR-480-B", "0.98"),
        edge("TR-480-B", "CB-LC-B", "solid feeder from transformer to load-center breaker", "0.98"),
        edge("CB-LC-B", "BUS-480-B", "breaker output lands on 480 V load-center bus", "0.98"),
        edge("BUS-480-B", "LC-B1", "filled bus tap labeled LC-B1", "0.96"),
        edge("LC-B1", "MCC-01B", "vertical solid feeder from LC-B1 tap to MCC-01B", "0.98"),
        edge("MCC-01B", "PUMP-RHR-B", "solid branch from MCC-01B to pump", "0.97"),
        edge("MCC-01B", "MOTOR-CCW-B", "solid branch from MCC-01B to motor", "0.97"),
        edge("BUS-480-B", "LC-B2", "filled bus tap labeled LC-B2", "0.96"),
        edge("LC-B2", "MCC-02B", "vertical solid feeder from LC-B2 tap to MCC-02B", "0.98"),
        edge("MCC-02B", "PUMP-AFW-B", "solid branch from MCC-02B to AFW pump", "0.97"),
        edge("MCC-02B", "MOV-B", "solid branch from MCC-02B to small MOV box over valve", "0.94"),
        edge("MOV-B", "VALVE-MOV-B", "short solid vertical from MOV box to valve", "0.96"),
        edge("MCC-02B", "FAN-CONTAIN-B", "solid branch from MCC-02B to containment fan", "0.96"),
        edge("BUS-480-B", "RECT-125B", "right end of 480 V bus routes down to rectifier AC side", "0.93"),
        edge("RECT-125B", "BUS-DC125-B", "rectifier DC side connects to 125 VDC B bus", "0.98"),
        edge("BUS-DC125-B", "BAT-125B", "filled vertical tap from DC bus to battery", "0.98"),
        edge("BUS-DC125-B", "INV-120B", "DC bus continues to inverter DC side", "0.98"),
        edge("JB-ESF-B", "PNL-ESF-B", "short vertical dashed/control drop from JB to matching ESF panel", "0.86"),
        edge("PNL-ESF-B", "INV-120B", "solid routed line from PNL-ESF-B bottom to INV-120B top", "0.90"),
        edge("PNL-ESF-B", "ESF-B-CONTROL-TRUNK", "dashed side stubs at panel enter lower dashed route", "0.55"),
        edge("ESF-B-CONTROL-TRUNK", "PUMP-AFW-B", "short dashed drop visually reaches lower dashed route near AFW-B", "0.50"),
        edge("ESF-B-CONTROL-TRUNK", "VALVE-MOV-B", "short dashed drop visually reaches lower dashed route near MOV-B valve", "0.50"),
        edge("ESF-B-CONTROL-TRUNK", "FAN-CONTAIN-B", "lower dashed route passes under/near fan B label", "0.38"),
        edge("ESF-A-CONTROL-TRUNK", "ESF-B-CONTROL-TRUNK", "lower dashed route appears visually continuous across center but may be boundary/routing aid", "0.35"),
    ]


def final_edges() -> list[dict[str, str]]:
    return [
        edge("GRID-230-A", "CB-SW-A", "solid feeder from grid symbol to breaker", "High"),
        edge("CB-SW-A", "TR-SU-A", "solid feeder from breaker to source transformer", "High"),
        edge("TR-SU-A", "BUS-13K-A", "solid feeder lands on 13.8 kV bus at SU-A tap label; SU-A is evidence only", "High"),
        edge("GEN-DG-A", "CB-DG-A", "solid feeder from DG symbol to breaker", "High"),
        edge("CB-DG-A", "TR-EDG-A", "solid feeder from breaker to EDG transformer", "High"),
        edge("TR-EDG-A", "BUS-13K-A", "solid feeder lands on 13.8 kV bus at EDG-A tap label; EDG-A is evidence only", "High"),
        edge("BUS-13K-A", "CB-13-TIE", "13.8 kV bus physically connects to tie breaker despite TIE OPEN state annotation", "High"),
        edge("CB-13-TIE", "BUS-13K-B", "tie breaker physically connects to right 13.8 kV bus despite TIE OPEN state annotation", "High"),
        edge("BUS-13K-B", "TR-SU-B", "solid feeder lands on BUS-13K-B at SU-B tap label; SU-B is evidence only", "High"),
        edge("TR-SU-B", "CB-SW-B", "solid feeder from transformer to breaker", "High"),
        edge("CB-SW-B", "GRID-230-B", "solid feeder from breaker to grid symbol", "High"),
        edge("BUS-13K-B", "TR-EDG-B", "solid feeder lands on BUS-13K-B at EDG-B tap label; EDG-B is evidence only", "High"),
        edge("TR-EDG-B", "CB-DG-B", "solid feeder from transformer to breaker", "High"),
        edge("CB-DG-B", "GEN-DG-B", "solid feeder from breaker to DG symbol", "High"),
        edge("BUS-13K-A", "TR-4K-A", "solid vertical feeder from BUS-13K-A to 4.16 kV transformer", "High"),
        edge("TR-4K-A", "CB-4K-A", "solid feeder from transformer to breaker", "High"),
        edge("CB-4K-A", "BUS-4K-A", "breaker bottom lands on 4.16 kV bus with tap dot", "High"),
        edge("BUS-13K-B", "TR-4K-B", "solid vertical feeder from BUS-13K-B to 4.16 kV transformer", "High"),
        edge("TR-4K-B", "CB-4K-B", "solid feeder from transformer to breaker", "High"),
        edge("CB-4K-B", "BUS-4K-B", "breaker bottom lands on 4.16 kV bus with tap dot", "High"),
        edge("BUS-4K-A", "CB-4K-TIE", "left 4.16 kV bus connects to tie breaker side terminal", "High"),
        edge("CB-4K-TIE", "BUS-4K-B", "tie breaker connects to right 4.16 kV bus; visual label is CB-4K-TIE", "High"),
        edge("CB-4K-TIE", "PNL-RPS-1", "control/lockout line from tie breaker area to RPS panel; RPS LOCKOUT is annotation", "Medium-High"),
        edge("BUS-4K-A", "TR-480-A", "vertical solid tap from 4.16 kV A bus to TR-480-A", "High"),
        edge("TR-480-A", "CB-LC-A", "solid feeder from transformer to load-center breaker", "High"),
        edge("CB-LC-A", "BUS-480-A", "breaker output lands on 480 V load-center bus", "High"),
        edge("BUS-480-A", "MCC-01A", "vertical solid tap from 480 VAC bus at LC-A1 evidence label", "High"),
        edge("MCC-01A", "PUMP-RHR-A", "solid branch from MCC-01A to RHR pump", "High"),
        edge("MCC-01A", "MOTOR-CCW-A", "solid branch from MCC-01A to CCW motor", "High"),
        edge("BUS-480-A", "MCC-02A", "vertical solid tap from 480 VAC bus at LC-A2 evidence label", "High"),
        edge("MCC-02A", "PUMP-AFW-A", "solid branch from MCC-02A to AFW pump", "High"),
        edge("MCC-02A", "VALVE-MOV-A", "solid branch from MCC-02A through folded MOV actuator box to valve", "High"),
        edge("MCC-02A", "FAN-CONTAIN-A", "solid branch from MCC-02A to containment fan", "High"),
        edge("BUS-480-A", "RECT-125A", "solid route from 480 V bus to rectifier AC side", "High"),
        edge("RECT-125A", "BUS-DC125-A", "rectifier DC side connects to A 125 VDC bus", "High"),
        edge("BUS-DC125-A", "BAT-125A", "filled bus tap from A DC bus to battery", "High"),
        edge("BUS-DC125-A", "INV-120A", "A DC bus continues to inverter DC side", "High"),
        edge("JB-ESF-A", "PNL-ESF-A", "short dashed/control drop from JB-ESF-A to PNL-ESF-A", "High"),
        edge("PNL-ESF-A", "INV-120A", "routed line from PNL-ESF-A bottom to INV-120A top", "Medium-High"),
        edge("BUS-4K-B", "TR-480-B", "vertical solid tap from 4.16 kV B bus to TR-480-B", "High"),
        edge("TR-480-B", "CB-LC-B", "solid feeder from transformer to load-center breaker", "High"),
        edge("CB-LC-B", "BUS-480-B", "breaker output lands on 480 V load-center bus", "High"),
        edge("BUS-480-B", "MCC-01B", "vertical solid tap from 480 VAC bus at LC-B1 evidence label", "High"),
        edge("MCC-01B", "PUMP-RHR-B", "solid branch from MCC-01B to RHR pump", "High"),
        edge("MCC-01B", "MOTOR-CCW-B", "solid branch from MCC-01B to CCW motor", "High"),
        edge("BUS-480-B", "MCC-02B", "vertical solid tap from 480 VAC bus at LC-B2 evidence label", "High"),
        edge("MCC-02B", "PUMP-AFW-B", "solid branch from MCC-02B to AFW pump", "High"),
        edge("MCC-02B", "VALVE-MOV-B", "solid branch from MCC-02B through folded MOV actuator box to valve", "High"),
        edge("MCC-02B", "FAN-CONTAIN-B", "solid branch from MCC-02B to containment fan", "High"),
        edge("BUS-480-B", "RECT-125B", "solid route from 480 V bus to rectifier AC side", "High"),
        edge("RECT-125B", "BUS-DC125-B", "rectifier DC side connects to B 125 VDC bus", "High"),
        edge("BUS-DC125-B", "BAT-125B", "filled bus tap from B DC bus to battery", "High"),
        edge("BUS-DC125-B", "INV-120B", "B DC bus continues to inverter DC side", "High"),
        edge("JB-ESF-B", "PNL-ESF-B", "short dashed/control drop from JB-ESF-B to PNL-ESF-B", "High"),
        edge("PNL-ESF-B", "INV-120B", "routed line from PNL-ESF-B bottom to INV-120B top", "Medium-High"),
    ]


def dedupe_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for item in edges:
        key = tuple(sorted((item["source"], item["target"])))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "evidence", "confidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: idx for idx, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        a = item["source"]
        b = item["target"]
        if a not in index or b not in index:
            continue
        i = index[a]
        j = index[b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix, strict=True):
            writer.writerow([node] + row)


def estimate_image_tokens(path: Path, detail: str = "high") -> int:
    # Repeatable local estimate used because the Responses counting endpoint was unavailable.
    with Image.open(path) as img:
        w, h = img.size
    if detail == "low":
        return 85
    scale = min(2048 / max(w, h), 1.0)
    w = math.ceil(w * scale)
    h = math.ceil(h * scale)
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def image_sum(names: list[str]) -> int:
    return sum(estimate_image_tokens(CROPS / name, "high") for name in names)


DIEGO_IMAGES = [
    "raw_full_thumb.png",
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "focus_top_distribution_raw.png",
    "focus_top_distribution_components.png",
    "focus_top_distribution_wires_overlay.png",
    "focus_middle_distribution_raw.png",
    "focus_middle_distribution_components.png",
    "focus_middle_distribution_wires_overlay.png",
    "focus_lower_distribution_raw.png",
    "focus_lower_distribution_components.png",
    "focus_lower_distribution_wires_overlay.png",
    "focus_center_components.png",
    "focus_center_wires_overlay.png",
    "detail_06_components.png",
    "detail_07_components.png",
    "detail_13_components.png",
    "detail_14_components.png",
    "detail_18_components.png",
    "detail_19_components.png",
]

JENNIFER_IMAGES = [
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "focus_top_distribution_components.png",
    "top_band_components.png",
    "focus_middle_distribution_components.png",
    "focus_center_components.png",
    "focus_center_wires_overlay.png",
    "focus_lower_distribution_components.png",
    "focus_lower_distribution_wires_overlay.png",
    "bottom_band_components.png",
    "detail_13_components.png",
    "detail_13_wires_overlay.png",
    "detail_18_components.png",
    "detail_18_wires_overlay.png",
    "detail_19_components.png",
    "detail_19_wires_overlay.png",
]

MAIN_IMAGES = [
    "components_full_thumb.png",
    "focus_top_distribution_components.png",
    "top_band_components.png",
    "focus_middle_distribution_components.png",
    "focus_lower_distribution_components.png",
    "focus_center_components.png",
    "focus_center_wires_overlay.png",
    "bottom_band_components.png",
    "lower_mid_band_components.png",
    "detail_13_components.png",
    "detail_18_components.png",
    "detail_18_wires_overlay.png",
    "detail_17_wires_overlay.png",
]


def write_token_estimates() -> None:
    calls = [
        {
            "document": "36",
            "iteration": "1",
            "round": "main-prep-and-visual-inspection",
            "model_call": "main_agent_resource_inspection_crop_generation_visual_review",
            "input_text_tokens_est": 3600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(MAIN_IMAGES),
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent inspected resources, generated crops, and visually reviewed focused regions.",
        },
        {
            "document": "36",
            "iteration": "1",
            "round": "round_01_diego",
            "model_call": "Diego high-recall extractor",
            "input_text_tokens_est": 2300,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(DIEGO_IMAGES),
            "output_tokens_low": 3000,
            "output_tokens_expected": 5000,
            "output_tokens_high": 7200,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Subagent notification exposed no usage object; image tokens estimated from 20 crop dimensions.",
        },
        {
            "document": "36",
            "iteration": "1",
            "round": "round_02_jennifer",
            "model_call": "Jennifer precision reviewer/refiner",
            "input_text_tokens_est": 6500,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(JENNIFER_IMAGES),
            "output_tokens_low": 1800,
            "output_tokens_expected": 3000,
            "output_tokens_high": 4800,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Jennifer reviewed Diego text plus focused crops; no API key for official counting endpoint.",
        },
        {
            "document": "36",
            "iteration": "1",
            "round": "round_03_diego",
            "model_call": "Diego convergence reconciliation",
            "input_text_tokens_est": 2400,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(
                [
                    "focus_top_distribution_components.png",
                    "focus_center_wires_overlay.png",
                    "detail_17_wires_overlay.png",
                    "detail_18_wires_overlay.png",
                    "bottom_band_components.png",
                ]
            ),
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1500,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Diego accepted Jennifer's corrections and listed changed/affirmed edges.",
        },
        {
            "document": "36",
            "iteration": "1",
            "round": "round_04_jennifer_final",
            "model_call": "Jennifer final saturation check",
            "input_text_tokens_est": 2600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(
                [
                    "components_full_thumb.png",
                    "focus_center_wires_overlay.png",
                    "detail_17_wires_overlay.png",
                    "detail_18_wires_overlay.png",
                    "bottom_band_components.png",
                ]
            ),
            "output_tokens_low": 400,
            "output_tokens_expected": 800,
            "output_tokens_high": 1400,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Final check confirmed saturated matrix and residual uncertainty notes.",
        },
        {
            "document": "36",
            "iteration": "1",
            "round": "main-final",
            "model_call": "main_agent_write_validate_report",
            "input_text_tokens_est": 3200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 400,
            "output_tokens_expected": 800,
            "output_tokens_high": 1400,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent wrote artifacts, validated matrices, closed agents, and reported results.",
        },
    ]
    for call in calls:
        call["total_tokens_expected"] = (
            int(call["input_text_tokens_est"])
            + int(call["cached_input_tokens_est"])
            + int(call["image_file_input_tokens_est"])
            + int(call["output_tokens_expected"])
        )
        call["total_tokens_low"] = (
            int(call["input_text_tokens_est"])
            + int(call["cached_input_tokens_est"])
            + int(call["image_file_input_tokens_est"])
            + int(call["output_tokens_low"])
        )
        call["total_tokens_high"] = (
            int(call["input_text_tokens_est"])
            + int(call["cached_input_tokens_est"])
            + int(call["image_file_input_tokens_est"])
            + int(call["output_tokens_high"])
        )

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "document",
            "iteration",
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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    summary = {
        "document": "36",
        "iteration": "1",
        "counting_endpoint_used": False,
        "why_not": "No OpenAI API key was available in the runtime; usage objects were not exposed by subagent notifications.",
        "method": "text ~= chars/4 or prompt-size estimate; images estimated with high-detail 512-tile heuristic; usage objects unavailable.",
        "calls": calls,
        "totals": {
            "low": sum(int(call["total_tokens_low"]) for call in calls),
            "expected": sum(int(call["total_tokens_expected"]) for call in calls),
            "high": sum(int(call["total_tokens_high"]) for call in calls),
        },
    }
    with (RESULTS / "token_usage_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"])
        writer.writeheader()
        writer.writerow(
            {
                "document": "36",
                "iteration": "1",
                "total_tokens_low": summary["totals"]["low"],
                "total_tokens_expected": summary["totals"]["expected"],
                "total_tokens_high": summary["totals"]["high"],
                "method": summary["method"],
            }
        )


def write_review_files(round2: list[dict[str, str]], final: list[dict[str, str]]) -> None:
    excluded_nodes = [
        "SU-A",
        "EDG-A",
        "SU-B",
        "EDG-B",
        "LC-A1",
        "LC-A2",
        "LC-B1",
        "LC-B2",
        "RPS-LOCKOUT",
        "RPS-TRIP",
        "MOV-A",
        "MOV-B",
        "ESF-A-CONTROL-TRUNK",
        "ESF-B-CONTROL-TRUNK",
    ]
    excluded_edges = [
        ("CB-4K-TIE", "RPS-LOCKOUT", "RPS LOCKOUT is a status/annotation label, not a graph node."),
        ("RPS-LOCKOUT", "PNL-RPS-1", "Represented as CB-4K-TIE to PNL-RPS-1 control edge without a separate status node."),
        ("CB-13-TIE", "RPS-TRIP", "RPS TRIP is a control annotation on dashed routing, not a graph node."),
        ("RPS-TRIP", "PNL-RPS-1", "Endpoint is ambiguous; kept as uncertain CB-13-TIE to PNL-RPS-1 instead of final edge."),
        ("ESF-A-CONTROL-TRUNK", "ESF-B-CONTROL-TRUNK", "Lower dashed route is not labeled as a component node and partly follows routing/boundary graphics."),
        ("ESF-A-CONTROL-TRUNK", "PUMP-AFW-A", "Dashed route may imply control but is too ambiguous for the binary matrix."),
        ("ESF-A-CONTROL-TRUNK", "VALVE-MOV-A", "Dashed route may imply control but is too ambiguous for the binary matrix."),
        ("ESF-A-CONTROL-TRUNK", "FAN-CONTAIN-A", "Dashed route is too weak/ambiguous near fan A."),
        ("ESF-B-CONTROL-TRUNK", "PUMP-AFW-B", "Dashed route may imply control but is too ambiguous for the binary matrix."),
        ("ESF-B-CONTROL-TRUNK", "VALVE-MOV-B", "Dashed route may imply control but is too ambiguous for the binary matrix."),
        ("ESF-B-CONTROL-TRUNK", "FAN-CONTAIN-B", "Dashed route is too weak/ambiguous near fan B."),
    ]
    final_rejected_edges = [
        ("CB-13-TIE", "PNL-RPS-1", "uncertain_excluded", "dashed RPS trip route approaches RPS area but endpoint is not clean enough for binary connectivity"),
        ("PNL-ESF-A", "PUMP-AFW-A", "uncertain_excluded", "lower dashed ESF route may imply control but also behaves like routing/boundary graphic"),
        ("PNL-ESF-A", "VALVE-MOV-A", "uncertain_excluded", "lower dashed ESF route may imply control but endpoint is not explicit"),
        ("PNL-ESF-A", "FAN-CONTAIN-A", "excluded", "route proximity only; no clear supported endpoint"),
        ("PNL-ESF-B", "PUMP-AFW-B", "uncertain_excluded", "lower dashed ESF route may imply control but also behaves like routing/boundary graphic"),
        ("PNL-ESF-B", "VALVE-MOV-B", "uncertain_excluded", "lower dashed ESF route may imply control but endpoint is not explicit"),
        ("PNL-ESF-B", "FAN-CONTAIN-B", "excluded", "route proximity only; no clear supported endpoint"),
        ("PNL-ESF-A", "PNL-ESF-B", "excluded", "no explicit A/B panel interconnection"),
        ("BUS-DC125-A", "BUS-DC125-B", "excluded", "no visible DC A/B cross-tie"),
        ("RECT-125A", "RECT-125B", "excluded", "no visible rectifier cross-tie"),
        ("INV-120A", "INV-120B", "excluded", "no visible inverter cross-tie"),
        ("BAT-125A", "BAT-125B", "excluded", "no visible battery cross-tie"),
    ]
    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "status", "reason"])
        for node in excluded_nodes:
            writer.writerow([node, "", "excluded_node", "tap/status/routing label or folded actuator, not a standalone final node"])
        for source, target, reason in excluded_edges:
            writer.writerow([source, target, "excluded_edge", reason])
        for source, target, status, reason in final_rejected_edges:
            writer.writerow([source, target, status, reason])

    round2_doc = [
        "# Round 2 Jennifer Precision Review",
        "",
        "Jennifer tightened Diego's high-recall graph by removing tap/status pseudo-nodes and low-confidence dashed ESF trunk edges.",
        "",
        "## Removed Standalone Nodes",
        "",
        ", ".join(excluded_nodes),
        "",
        "## Normalizations",
        "",
        "- Kept `CB-4K-TIE`; visually it reads as `CB-4K-TIE`, not `CB-4K-1E`.",
        "- Treated `TIE OPEN` and `RPS LOCKOUT` as state annotations, not nodes.",
        "- Folded generic `MOV` actuator boxes into `VALVE-MOV-A` and `VALVE-MOV-B`.",
        "- Treated `SU-*`, `EDG-*`, and `LC-*` labels as tap evidence, not nodes.",
        "",
        "## Corrected Edge Count",
        "",
        str(len(round2)),
        "",
        "## Corrected Edge List",
        "",
        "See round_02_jennifer_edges.csv.",
        "",
        "## Uncertain / Excluded",
        "",
        "See uncertain_or_excluded_edges.csv.",
    ]
    (RESULTS / "round_02_jennifer_review.md").write_text("\n".join(round2_doc) + "\n", encoding="utf-8")

    round3_doc = [
        "# Round 3 Diego Reconciliation",
        "",
        "Diego agreed with Jennifer's Round 2 corrections and raised no final objections.",
        "",
        "## Affirmed Changes",
        "",
        "- Removed tap/status pseudo-nodes.",
        "- Folded `MOV-A/B` into `VALVE-MOV-A/B`.",
        "- Excluded lower dashed ESF trunk routes from the final binary matrix.",
        "- Kept DC topology as `RECT -> BUS-DC125 -> BAT/INV` with no A/B DC cross-tie.",
        "- Confirmed `CB-4K-TIE` as the visual label.",
    ]
    (RESULTS / "round_03_diego_reconciliation.md").write_text("\n".join(round3_doc) + "\n", encoding="utf-8")

    round4_doc = [
        "# Round 4 Jennifer Final Saturation Check",
        "",
        "Status: saturated. Jennifer agreed with the corrected node/edge set and made no further changes to the final matrix.",
        "",
        "The final matrix uses only the corrected solid/explicit component connections. Tap labels and status/control annotations are excluded as nodes.",
        "",
        "`CB-4K-TIE -> PNL-RPS-1` remains in the matrix as the only RPS/control edge supported enough for binary connectivity: the vertical line from the tie breaker / RPS LOCKOUT area terminates directly at `PNL-RPS-1`.",
        "",
        "Residual uncertain/excluded items are recorded in uncertain_or_excluded_edges.csv.",
    ]
    (RESULTS / "round_04_jennifer_final_saturation_check.md").write_text("\n".join(round4_doc) + "\n", encoding="utf-8")

    report = [
        "# Document 36 Connectivity Extraction Report",
        "",
        "Resources used: raw schematic plus wire/component overlays and visual crops. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.",
        "",
        "## Saturated Decision",
        "",
        "The final matrix uses Jennifer's conservative correction confirmed by Diego: tap labels (`SU-*`, `EDG-*`, `LC-*`) and state/routing labels (`TIE OPEN`, `RPS LOCKOUT`, `RPS TRIP`) are not standalone nodes. The visual `CB-4K-TIE` label is retained. Generic MOV actuator boxes are folded into the labeled valve nodes. Lower dashed ESF trunk routes are kept uncertain/excluded rather than promoted to binary edges.",
        "",
        "## Final Counts",
        "",
        f"- Nodes: {len(FINAL_NODES)}",
        f"- Edges: {len(final)}",
        "",
        "## Output Files",
        "",
        "- round_01_diego_edges.csv / round_01_diego_matrix.csv",
        "- round_02_jennifer_edges.csv / round_02_jennifer_matrix.csv",
        "- round_03_diego_edges.csv / round_03_diego_matrix.csv",
        "- round_03_diego_reconciliation.md",
        "- round_04_jennifer_final_edges.csv / round_04_jennifer_final_matrix.csv",
        "- round_04_jennifer_final_saturation_check.md",
        "- final_edges.csv / final_connectivity_matrix.csv",
        "- uncertain_or_excluded_edges.csv",
        "- token_usage_estimate.csv / token_usage_summary.csv / token_usage_summary.json",
    ]
    (RESULTS / "extraction_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def validate(nodes: list[str], edges: list[dict[str, str]], matrix_path: Path) -> dict[str, object]:
    index = set(nodes)
    unknown = sorted({node for item in edges for node in (item["source"], item["target"]) if node not in index})
    duplicate_pairs = len(edges) - len({tuple(sorted((item["source"], item["target"]))) for item in edges})
    with matrix_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    header = rows[0][1:]
    diagonal_zero = True
    symmetric = True
    for i, row in enumerate(rows[1:]):
        if row[1 + i] != "0":
            diagonal_zero = False
        for j, value in enumerate(row[1:]):
            if rows[1 + j][1 + i] != value:
                symmetric = False
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unknown_nodes": unknown,
        "duplicate_undirected_edges": duplicate_pairs,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "matrix_header_nodes": len(header),
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    round1 = dedupe_edges(diego_round1_edges())
    final = dedupe_edges(final_edges())
    rounds = {
        "round_01_diego": (DIEGO_NODES, round1),
        "round_02_jennifer": (FINAL_NODES, final),
        "round_03_diego": (FINAL_NODES, final),
        "round_04_jennifer_final": (FINAL_NODES, final),
    }
    for name, (nodes, edges) in rounds.items():
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)
    write_edges(RESULTS / "final_edges.csv", final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, final)
    write_review_files(final, final)
    write_token_estimates()
    summary = {
        "document": "36",
        "iteration": "1",
        "rounds": {name: {"nodes": len(nodes), "edges": len(edges)} for name, (nodes, edges) in rounds.items()},
        "final": validate(FINAL_NODES, final, RESULTS / "final_connectivity_matrix.csv"),
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
    }
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
