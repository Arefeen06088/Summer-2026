from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\40\Raw + wires + components + junctions")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def edge(source: str, target: str, kind: str, confidence: str, evidence: str) -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "type": kind,
        "confidence": confidence,
        "evidence": evidence,
    }


FINAL_NODES = [
    "DG-21A",
    "UAT-2A",
    "DS-21A",
    "ATS-21A",
    "SWGR-21A",
    "TIE-BKR-21AB",
    "SWGR-21B",
    "SAT-2B",
    "DS-21B",
    "ATS-21B",
    "DG-21B",
    "CB-21A1",
    "TR-21A",
    "MCC-21A",
    "CB-21B1",
    "TR-21B",
    "MCC-21B",
    "CB-MPA1",
    "PUMP-SI21A",
    "PUMP-CCW21A",
    "FAN-RB21A",
    "MOV-HV211A",
    "MOV-RWST21A",
    "XFMR-CPT21A",
    "AC-PNL-120A",
    "CT-21A",
    "VT-21A",
    "XFMR-CPT21B",
    "AC-PNL-120B",
    "CB-MPB1",
    "PUMP-SI21B",
    "PUMP-CCW21B",
    "FAN-RB21B",
    "MOV-HV211B",
    "MOV-RWST21B",
    "CT-21B",
    "VT-21B",
    "RECT-21A",
    "DC-BUS-21A",
    "BAT-21A",
    "INV-21A",
    "LOCA-SIG-A",
    "JB-21A",
    "RPS-PNL-A",
    "RELAY-K21A",
    "RELAY-86A",
    "RECT-21B",
    "DC-BUS-21B",
    "BAT-21B",
    "INV-21B",
    "LOCA-SIG-B",
    "JB-21B",
    "RPS-PNL-B",
    "RELAY-K21B",
    "RELAY-86B",
]


DIEGO_R1_NODES = [
    "DG-21A",
    "UAT-2A",
    "DS-21A",
    "ATS-21A",
    "SWGR-21A",
    "TIE-BKR-21AB",
    "SWGR-21B",
    "SAT-2B",
    "DS-21B",
    "ATS-21B",
    "DG-21B",
    "CB-21A1",
    "TR-21A",
    "MCC-21A",
    "CB-21B1",
    "TR-21B",
    "MCC-21B",
    "CB-MPA1",
    "TRIP-MPA1",
    "PUMP-SI21A",
    "PUMP-CCW21A",
    "FAN-RB21A",
    "MOV-HV211A",
    "MOV-RWST21A",
    "XFMR-CPT21A",
    "AC-PNL-120A",
    "CT-21A",
    "VT-21A",
    "VOLTAGE-SIG-A",
    "XFMR-CPT21B",
    "AC-PNL-120B",
    "CB-MPB1",
    "TRIP-MPB1",
    "PUMP-SI21B",
    "PUMP-CCW21B",
    "FAN-RB21B",
    "MOV-HV211B",
    "MOV-RWST21B",
    "CT-21B",
    "VT-21B",
    "VOLTAGE-SIG-B",
    "RECT-21A",
    "DC-BUS-21A",
    "BAT-21A",
    "INV-21A",
    "LOCA-SIG-A",
    "JB-21A",
    "RPS-PNL-A",
    "RELAY-K21A",
    "RELAY-86A",
    "RECT-21B",
    "DC-BUS-21B",
    "BAT-21B",
    "INV-21B",
    "LOCA-SIG-B",
    "JB-21B",
    "RPS-PNL-B",
    "RELAY-K21B",
    "RELAY-86B",
]


POWER_EDGES = [
    edge("DG-21A", "ATS-21A", "solid_power", "HIGH", "solid feeder from generator to ATS-21A"),
    edge("UAT-2A", "DS-21A", "solid_power", "HIGH", "UAT-2A stacked over DS-21A with direct conductor"),
    edge("DS-21A", "ATS-21A", "solid_power", "HIGH", "solid feeder from disconnect into ATS-21A"),
    edge("ATS-21A", "SWGR-21A", "solid_power", "HIGH", "ATS-21A vertical feeder lands on SWGR-21A bus dot"),
    edge("SWGR-21A", "TIE-BKR-21AB", "solid_power", "HIGH", "SWGR-21A bus enters the tie breaker node"),
    edge("TIE-BKR-21AB", "SWGR-21B", "solid_power", "HIGH", "tie breaker output continues into SWGR-21B bus"),
    edge("SAT-2B", "DS-21B", "solid_power", "HIGH", "SAT-2B stacked over DS-21B with direct conductor"),
    edge("DS-21B", "ATS-21B", "solid_power", "HIGH", "solid feeder from disconnect into ATS-21B"),
    edge("DG-21B", "ATS-21B", "solid_power", "HIGH", "solid feeder from generator to ATS-21B"),
    edge("ATS-21B", "SWGR-21B", "solid_power", "HIGH", "ATS-21B vertical feeder lands on SWGR-21B bus dot"),
    edge("SWGR-21A", "CB-21A1", "solid_power", "HIGH", "vertical tap from SWGR-21A bus to breaker"),
    edge("CB-21A1", "TR-21A", "solid_power", "HIGH", "breaker directly feeds transformer TR-21A"),
    edge("TR-21A", "MCC-21A", "solid_power", "HIGH", "transformer output lands on MCC-21A bus"),
    edge("SWGR-21B", "CB-21B1", "solid_power", "HIGH", "vertical tap from SWGR-21B bus to breaker"),
    edge("CB-21B1", "TR-21B", "solid_power", "HIGH", "breaker directly feeds transformer TR-21B"),
    edge("TR-21B", "MCC-21B", "solid_power", "HIGH", "transformer output lands on MCC-21B bus"),
    edge("MCC-21A", "CB-MPA1", "solid_power", "HIGH", "MCC-21A load bus feeder through breaker CB-MPA1"),
    edge("CB-MPA1", "PUMP-SI21A", "solid_power", "HIGH", "CB-MPA1 solid feeder continues to PUMP-SI21A"),
    edge("MCC-21A", "PUMP-CCW21A", "solid_power", "HIGH", "solid vertical branch from MCC-21A to PUMP-CCW21A"),
    edge("MCC-21A", "FAN-RB21A", "solid_power", "HIGH", "solid vertical branch from MCC-21A to FAN-RB21A"),
    edge("MCC-21A", "MOV-HV211A", "solid_power", "HIGH", "solid vertical branch from MCC-21A to MOV-HV211A"),
    edge("MCC-21A", "MOV-RWST21A", "solid_power", "HIGH", "solid vertical branch from MCC-21A to MOV-RWST21A"),
    edge("MCC-21A", "XFMR-CPT21A", "solid_power", "HIGH", "solid branch from MCC-21A to control power transformer"),
    edge("XFMR-CPT21A", "AC-PNL-120A", "solid_power", "HIGH", "transformer output connects to AC-PNL-120A"),
    edge("AC-PNL-120A", "RECT-21A", "solid_power", "HIGH", "solid AC panel feeder drops to rectifier/charger"),
    edge("RECT-21A", "DC-BUS-21A", "solid_power", "HIGH", "rectifier output lands on 125 VDC bus dot"),
    edge("BAT-21A", "DC-BUS-21A", "solid_power", "HIGH", "battery tap lands on DC-BUS-21A dot"),
    edge("DC-BUS-21A", "INV-21A", "solid_power", "HIGH", "solid DC bus feeder drops to inverter"),
    edge("MCC-21B", "XFMR-CPT21B", "solid_power", "HIGH", "solid branch from MCC-21B to control power transformer"),
    edge("XFMR-CPT21B", "AC-PNL-120B", "solid_power", "HIGH", "transformer output connects to AC-PNL-120B"),
    edge("AC-PNL-120B", "RECT-21B", "solid_power", "HIGH", "solid AC panel feeder drops to rectifier/charger"),
    edge("MCC-21B", "CB-MPB1", "solid_power", "HIGH", "MCC-21B load bus feeder through breaker CB-MPB1"),
    edge("CB-MPB1", "PUMP-SI21B", "solid_power", "HIGH", "CB-MPB1 solid feeder continues to PUMP-SI21B"),
    edge("MCC-21B", "PUMP-CCW21B", "solid_power", "HIGH", "solid vertical branch from MCC-21B to PUMP-CCW21B"),
    edge("MCC-21B", "FAN-RB21B", "solid_power", "HIGH", "solid vertical branch from MCC-21B to FAN-RB21B"),
    edge("MCC-21B", "MOV-HV211B", "solid_power", "HIGH", "solid vertical branch from MCC-21B to MOV-HV211B"),
    edge("MCC-21B", "MOV-RWST21B", "solid_power", "HIGH", "solid vertical branch from MCC-21B to MOV-RWST21B"),
    edge("RECT-21B", "DC-BUS-21B", "solid_power", "HIGH", "rectifier output lands on 125 VDC bus dot"),
    edge("BAT-21B", "DC-BUS-21B", "solid_power", "HIGH", "battery tap lands on DC-BUS-21B dot"),
    edge("DC-BUS-21B", "INV-21B", "solid_power", "HIGH", "solid DC bus feeder drops to inverter"),
]


FINAL_CONTROL_EDGES = [
    edge("LOCA-SIG-A", "JB-21A", "instrument_signal", "HIGH", "short-dash signal line from LOCA circle to JB-21A"),
    edge("JB-21A", "RPS-PNL-A", "instrument_signal", "HIGH", "short-dash signal line from JB-21A to RPS-PNL-A terminal strip"),
    edge("INV-21A", "RPS-PNL-A", "control_power_logic", "HIGH", "dashed logic/control-power run between inverter and RPS-PNL-A"),
    edge("CT-21A", "RPS-PNL-A", "instrument_signal", "HIGH", "dashed CT signal path visually routes into RPS logic area"),
    edge("VT-21A", "RPS-PNL-A", "instrument_signal", "MEDIUM", "dashed voltage signal path from VT-21A to RPS-PNL-A"),
    edge("RPS-PNL-A", "RELAY-K21A", "control_logic", "HIGH", "dashed RPS control lane between panel and K relay"),
    edge("RELAY-K21A", "RELAY-86A", "control_logic", "HIGH", "dashed RPS control lane between K relay and 86 relay"),
    edge("RELAY-86A", "CB-MPA1", "trip_control", "HIGH", "dash-dot trip control path labeled TRIP MPA1 to breaker input"),
    edge("LOCA-SIG-B", "JB-21B", "instrument_signal", "HIGH", "short-dash signal line from LOCA circle to JB-21B"),
    edge("JB-21B", "RPS-PNL-B", "instrument_signal", "HIGH", "short-dash signal line from JB-21B to RPS-PNL-B terminal strip"),
    edge("INV-21B", "RPS-PNL-B", "control_power_logic", "HIGH", "dashed logic/control-power run between inverter and RPS-PNL-B"),
    edge("CT-21B", "RPS-PNL-B", "instrument_signal", "HIGH", "dashed CT signal path visually routes into RPS logic area"),
    edge("VT-21B", "RPS-PNL-B", "instrument_signal", "MEDIUM", "dashed voltage signal path from VT-21B to RPS-PNL-B"),
    edge("RPS-PNL-B", "RELAY-K21B", "control_logic", "HIGH", "dashed RPS control lane between panel and K relay"),
    edge("RELAY-K21B", "RELAY-86B", "control_logic", "HIGH", "dashed RPS control lane between K relay and 86 relay"),
    edge("RELAY-86B", "CB-MPB1", "trip_control", "HIGH", "dash-dot trip control path labeled TRIP MPB1 to breaker input"),
]


DIEGO_R1_CONTROL_EDGES = [
    edge("LOCA-SIG-A", "JB-21A", "instrument_signal", "HIGH", "short-dash signal line from LOCA circle to JB-21A"),
    edge("JB-21A", "RPS-PNL-A", "instrument_signal", "HIGH", "short-dash signal line from JB-21A to RPS-PNL-A terminal strip"),
    edge("INV-21A", "RPS-PNL-A", "control_power_logic", "MEDIUM", "dashed logic/control-power run between inverter and RPS-PNL-A"),
    edge("DC-BUS-21A", "RPS-PNL-A", "control_power", "MEDIUM", "Diego high-recall candidate from dashed RPS terminal drops near DC bus"),
    edge("CT-21A", "RPS-PNL-A", "instrument_signal", "HIGH", "dashed CT signal to RPS logic"),
    edge("VT-21A", "VOLTAGE-SIG-A", "instrument_signal", "MEDIUM", "Diego high-recall split of voltage signal label node"),
    edge("VOLTAGE-SIG-A", "RPS-PNL-A", "instrument_signal", "MEDIUM", "Diego high-recall split of voltage signal label node"),
    edge("RPS-PNL-A", "RELAY-K21A", "control_logic", "HIGH", "dashed RPS control lane between panel and K relay"),
    edge("RELAY-K21A", "RELAY-86A", "control_logic", "HIGH", "dashed RPS control lane between K relay and 86 relay"),
    edge("RELAY-86A", "TRIP-MPA1", "trip_control", "HIGH", "Diego high-recall split of TRIP MPA1 line label"),
    edge("TRIP-MPA1", "CB-MPA1", "trip_control", "HIGH", "Diego high-recall split of TRIP MPA1 line label"),
    edge("LOCA-SIG-B", "JB-21B", "instrument_signal", "HIGH", "short-dash signal line from LOCA circle to JB-21B"),
    edge("JB-21B", "RPS-PNL-B", "instrument_signal", "HIGH", "short-dash signal line from JB-21B to RPS-PNL-B terminal strip"),
    edge("INV-21B", "RPS-PNL-B", "control_power_logic", "MEDIUM", "dashed logic/control-power run between inverter and RPS-PNL-B"),
    edge("DC-BUS-21B", "RPS-PNL-B", "control_power", "MEDIUM", "Diego high-recall candidate from dashed RPS terminal drops near DC bus"),
    edge("CT-21B", "RPS-PNL-B", "instrument_signal", "HIGH", "dashed CT signal to RPS logic"),
    edge("VT-21B", "VOLTAGE-SIG-B", "instrument_signal", "MEDIUM", "Diego high-recall split of voltage signal label node"),
    edge("VOLTAGE-SIG-B", "RPS-PNL-B", "instrument_signal", "MEDIUM", "Diego high-recall split of voltage signal label node"),
    edge("RPS-PNL-B", "RELAY-K21B", "control_logic", "HIGH", "dashed RPS control lane between panel and K relay"),
    edge("RELAY-K21B", "RELAY-86B", "control_logic", "HIGH", "dashed RPS control lane between K relay and 86 relay"),
    edge("RELAY-86B", "TRIP-MPB1", "trip_control", "HIGH", "Diego high-recall split of TRIP MPB1 line label"),
    edge("TRIP-MPB1", "CB-MPB1", "trip_control", "HIGH", "Diego high-recall split of TRIP MPB1 line label"),
    edge("MCC-21A", "VT-21A", "sensing_source", "LOW", "Diego plausible but unsupported source association"),
    edge("MCC-21B", "VT-21B", "sensing_source", "LOW", "Diego plausible but unsupported source association"),
    edge("MCC-21A", "CT-21A", "sensing_source", "LOW", "Diego plausible but unsupported source association"),
    edge("MCC-21B", "CT-21B", "sensing_source", "LOW", "Diego plausible but unsupported source association"),
]


FINAL_EDGES = POWER_EDGES + FINAL_CONTROL_EDGES
DIEGO_R1_EDGES = POWER_EDGES + DIEGO_R1_CONTROL_EDGES


UNCERTAIN_OR_EXCLUDED = [
    {"item": "MCC-21A--VT-21A", "status": "removed_after_round_1", "reason": "VT signal line is visible, but no MCC bus endpoint or junction dot supports a direct source edge."},
    {"item": "MCC-21B--VT-21B", "status": "removed_after_round_1", "reason": "VT signal line is visible, but no MCC bus endpoint or junction dot supports a direct source edge."},
    {"item": "MCC-21A--CT-21A", "status": "removed_after_round_1", "reason": "CT signal line is visible, but no conductor is drawn through the CT to the MCC bus."},
    {"item": "MCC-21B--CT-21B", "status": "removed_after_round_1", "reason": "CT signal line is visible, but no conductor is drawn through the CT to the MCC bus."},
    {"item": "DC-BUS-21A--RPS-PNL-A", "status": "removed_after_round_1", "reason": "Dashed RPS terminal drops cross near the DC bus without a clear solid DC junction dot."},
    {"item": "DC-BUS-21B--RPS-PNL-B", "status": "removed_after_round_1", "reason": "Dashed RPS terminal drops cross near the DC bus without a clear solid DC junction dot."},
    {"item": "VOLTAGE-SIG-A / VOLTAGE-SIG-B", "status": "excluded_from_final_nodes", "reason": "Line labels on dashed instrument-signal paths, not component symbols."},
    {"item": "TRIP-MPA1 / TRIP-MPB1", "status": "excluded_from_final_nodes", "reason": "Trip labels beside breaker control inputs, not standalone component symbols."},
    {"item": "C21A-01, C21B-01, D21A-07, D21B-07, S21A-11, S21B-11", "status": "excluded", "reason": "Cable index and cable/rating labels are metadata or conductor labels, not matrix nodes."},
    {"item": "SWGR-21A--SWGR-21B direct edge", "status": "excluded", "reason": "A and B buses connect through TIE-BKR-21AB, not by direct splice."},
    {"item": "DC-BUS-21A--DC-BUS-21B", "status": "excluded", "reason": "Separate 125 VDC buses; no cross-train DC tie is drawn."},
    {"item": "MOV-RWST crossed dashed lines", "status": "excluded", "reason": "The drawing explicitly marks line crossing without dot as no junction."},
    {"item": "Source Normal/Alternate, Bus Loads, channel/control-lane titles", "status": "excluded", "reason": "Area labels and headings, not components."},
]


ROUND_TEXT = {
    "round_02_jennifer_review.md": """# Jennifer Round 2 Precision Review

Jennifer removed the low-confidence sensing-source edges `MCC-21A--VT-21A`, `MCC-21B--VT-21B`, `MCC-21A--CT-21A`, and `MCC-21B--CT-21B` because the dashed CT/VT signal paths are visible but no terminal dot or conductor endpoint supports those direct MCC associations.

She also removed `DC-BUS-21A--RPS-PNL-A` and `DC-BUS-21B--RPS-PNL-B`; the dashed RPS terminal drops pass near or across the DC buses without a solid DC junction. `VOLTAGE-SIG-A`, `VOLTAGE-SIG-B`, `TRIP-MPA1`, and `TRIP-MPB1` were removed as matrix nodes and retained only as edge evidence/labels. Cable IDs, voltage ratings, source labels, bus-load labels, and control-lane labels were excluded as non-component text.
""",
    "round_03_diego_reconciliation.md": """# Diego Round 3 Reconciliation

Diego accepted Jennifer's refined graph unchanged and marked the extraction saturated: 55 nodes and 56 undirected edges. He did not restore the removed MCC sensing-source edges, DC-bus-to-RPS candidates, label nodes, cable IDs, or pseudo area labels.
""",
    "round_04_jennifer_final_saturation_check.md": """# Jennifer Round 4 Final Saturation Check

Jennifer confirmed Diego's agreement with the refined graph. The final matrix is generated from the approved edge CSV itself: 55 nodes and 56 undirected edges.
""",
    "round_01_diego_notes.md": """# Diego Round 1 High-Recall Notes

Diego proposed a high-recall graph with visually plausible label/logical nodes for `VOLTAGE-SIG-A/B` and `TRIP-MPA1/MPB1`, low-confidence MCC-to-CT/VT sensing-source edges, and candidate DC-bus-to-RPS control-power edges. These were intentionally carried into the round 1 matrix so the later precision pruning is auditable.
""",
}


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    fields = ["source", "target", "type", "confidence", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    index = {node: idx for idx, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    unknown: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    duplicate_count = 0

    for row in edges:
        source = row["source"]
        target = row["target"]
        if source not in index or target not in index:
            unknown.append((source, target))
            continue
        if source == target:
            matrix[index[source]][index[target]] = 1
            continue
        key = tuple(sorted((source, target)))
        if key in seen:
            duplicate_count += 1
        seen.add(key)
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)

    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unknown_nodes": unknown,
        "duplicate_undirected_edges": duplicate_count,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "matrix_header_nodes": len(nodes),
    }


def openai_high_detail_image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    with Image.open(path) as img:
        width, height = img.size
    scale = min(1.0, 2048.0 / max(width, height))
    width = max(1, int(round(width * scale)))
    height = max(1, int(round(height * scale)))
    short = min(width, height)
    if short > 768:
        scale = 768.0 / short
        width = max(1, int(round(width * scale)))
        height = max(1, int(round(height * scale)))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def estimate_image_tokens(paths: list[Path]) -> int:
    return sum(openai_high_detail_image_tokens(path) for path in paths)


def token_rows() -> list[dict[str, object]]:
    main_imgs = [
        CROPS / "raw_full_thumb.png",
        CROPS / "components_full_thumb.png",
        CROPS / "wires_overlay_full_thumb.png",
        CROPS / "focus_top_distribution_raw.png",
        CROPS / "focus_middle_distribution_raw.png",
        CROPS / "focus_lower_distribution_raw.png",
        CROPS / "focus_left_loads_raw.png",
        CROPS / "focus_right_loads_raw.png",
        CROPS / "focus_dc_controls_raw.png",
        CROPS / "detail_00_wires_overlay.png",
        CROPS / "detail_01_wires_overlay.png",
        CROPS / "detail_02_wires_overlay.png",
        CROPS / "detail_03_wires_overlay.png",
        CROPS / "detail_05_wires_overlay.png",
        CROPS / "detail_06_wires_overlay.png",
        CROPS / "detail_07_wires_overlay.png",
        CROPS / "detail_08_wires_overlay.png",
        CROPS / "detail_10_wires_overlay.png",
        CROPS / "detail_11_wires_overlay.png",
        CROPS / "detail_12_wires_overlay.png",
        CROPS / "detail_13_wires_overlay.png",
        CROPS / "detail_15_wires_overlay.png",
        CROPS / "detail_16_wires_overlay.png",
        CROPS / "detail_17_wires_overlay.png",
        CROPS / "detail_18_wires_overlay.png",
    ]
    diego_imgs = [
        CROPS / "raw_full_thumb.png",
        CROPS / "components_full_thumb.png",
        CROPS / "wires_overlay_full_thumb.png",
        CROPS / "focus_top_distribution_raw.png",
        CROPS / "focus_middle_distribution_raw.png",
        CROPS / "focus_lower_distribution_raw.png",
        CROPS / "left_half_raw.png",
        CROPS / "right_half_raw.png",
        CROPS / "focus_dc_controls_raw.png",
    ]
    jennifer_imgs = [
        CROPS / "raw_full_thumb.png",
        CROPS / "components_full_thumb.png",
        CROPS / "wires_overlay_full_thumb.png",
        CROPS / "focus_top_distribution_raw.png",
        CROPS / "focus_middle_distribution_raw.png",
        CROPS / "focus_left_loads_raw.png",
        CROPS / "focus_right_loads_raw.png",
        CROPS / "focus_dc_controls_raw.png",
        CROPS / "focus_lower_distribution_raw.png",
        CROPS / "focus_dc_controls_wires_overlay.png",
        CROPS / "detail_15_wires_overlay.png",
        CROPS / "detail_16_wires_overlay.png",
        CROPS / "detail_17_wires_overlay.png",
        CROPS / "detail_18_wires_overlay.png",
    ]
    rows = [
        {
            "call_id": "main_doc40_01",
            "round": "main-prep-and-local-visual-review",
            "model_call": "main_agent_resource_inspection_crop_generation_visual_review",
            "input_text_tokens_est": 4200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": estimate_image_tokens(main_imgs),
            "output_tokens_low": 600,
            "output_tokens_expected": 1100,
            "output_tokens_high": 1900,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent inspected resources, generated crops, and reviewed thumbnails/focus/detail crops.",
        },
        {
            "call_id": "diego_doc40_r1",
            "round": "round_01_diego",
            "model_call": "Diego high-recall extractor",
            "input_text_tokens_est": 3000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": estimate_image_tokens(diego_imgs),
            "output_tokens_low": 4200,
            "output_tokens_expected": 5900,
            "output_tokens_high": 8100,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Diego proposed all visually/geometrically plausible nodes and edges.",
        },
        {
            "call_id": "jennifer_doc40_r2",
            "round": "round_02_jennifer",
            "model_call": "Jennifer precision reviewer/refiner",
            "input_text_tokens_est": 7900,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": estimate_image_tokens(jennifer_imgs),
            "output_tokens_low": 2200,
            "output_tokens_expected": 3300,
            "output_tokens_high": 4800,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Jennifer reviewed Diego R1 and pruned unsupported or label-only nodes/edges.",
        },
        {
            "call_id": "diego_doc40_r3",
            "round": "round_03_diego",
            "model_call": "Diego convergence reconciliation",
            "input_text_tokens_est": 3600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 250,
            "output_tokens_expected": 500,
            "output_tokens_high": 900,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Diego accepted Jennifer's refined graph unchanged.",
        },
        {
            "call_id": "jennifer_doc40_r4",
            "round": "round_04_jennifer_final",
            "model_call": "Jennifer final saturation check",
            "input_text_tokens_est": 700,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 120,
            "output_tokens_expected": 220,
            "output_tokens_high": 400,
            "reasoning_tokens": "unavailable",
            "usage_object": "not exposed by subagent notification",
            "notes": "Jennifer confirmed saturation; final counts are validated from the approved CSV rows.",
        },
        {
            "call_id": "main_doc40_02",
            "round": "main-final-artifact-write",
            "model_call": "main_agent_write_validate_report",
            "input_text_tokens_est": 4200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent wrote matrices/reports, validated symmetry/diagonal, and prepared final response.",
        },
    ]
    for row in rows:
        row["document"] = "40"
        row["iteration"] = "1"
        for label in ("low", "expected", "high"):
            row[f"total_tokens_{label}"] = (
                int(row["input_text_tokens_est"])
                + int(row["cached_input_tokens_est"])
                + int(row["image_file_input_tokens_est"])
                + int(row[f"output_tokens_{label}"])
            )
    return rows


def write_token_tables() -> dict[str, object]:
    rows = token_rows()
    fields = [
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
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "document": "40",
        "iteration": "1",
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "method": "No API key was available for the Responses input-token counting endpoint. Text was estimated from prompt/message size; images were estimated with the public high-detail 512-tile heuristic after 2048/768 resizing.",
        "counting_endpoint_used": False,
        "counting_endpoint_reason": "No API key available.",
        "usage_objects_collected": False,
        "usage_object_reason": "Codex subagent notifications in this environment did not expose model usage objects.",
        "calls": rows,
    }
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"])
        writer.writeheader()
        writer.writerow({key: summary[key] for key in ["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"]})
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (CODES / "write_doc40_results.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")

    round_specs = [
        ("round_01_diego", DIEGO_R1_NODES, DIEGO_R1_EDGES),
        ("round_02_jennifer", FINAL_NODES, FINAL_EDGES),
        ("round_03_diego", FINAL_NODES, FINAL_EDGES),
        ("round_04_jennifer_final", FINAL_NODES, FINAL_EDGES),
    ]
    validations: dict[str, dict[str, object]] = {}
    for prefix, nodes, edges in round_specs:
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        validations[prefix] = write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edges)

    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    final_validation = write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    with (RESULTS / "final_node_order.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for idx, node in enumerate(FINAL_NODES):
            writer.writerow([idx, node])

    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item", "status", "reason"])
        writer.writeheader()
        writer.writerows(UNCERTAIN_OR_EXCLUDED)

    for name, text in ROUND_TEXT.items():
        (RESULTS / name).write_text(text, encoding="utf-8")

    token_summary = write_token_tables()

    report = f"""# Document 40 Extraction Report

Blind visual extraction used only the raw schematic and the provided derived component/wire visual aids. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Final Result

- Nodes: {len(FINAL_NODES)}
- Edges: {len(FINAL_EDGES)}
- Symmetric matrix: {final_validation['symmetric']}
- Diagonal zero: {final_validation['diagonal_zero']}
- Unknown edge endpoints: {len(final_validation['unknown_nodes'])}
- Duplicate undirected edges: {final_validation['duplicate_undirected_edges']}

## Saturation

Diego R1 produced a high-recall graph. Jennifer R2 removed label-only nodes, unsupported MCC-to-CT/VT source associations, and unsupported DC-bus-to-RPS direct edges. Diego R3 agreed with Jennifer's graph unchanged. Jennifer R4 confirmed saturation; final counts here are validated from the approved edge CSV.

## Key Precision Decisions

- `TIE-BKR-21AB` is retained as the only A/B 4160 V bus tie node; no direct `SWGR-21A--SWGR-21B` edge is added.
- `VOLTAGE-SIG-A/B` and `TRIP-MPA1/MPB1` are labels on signal/trip lines, not final matrix nodes.
- `CT-21A/B` and `VT-21A/B` remain as instrument-signal nodes connected to their RPS panels; inferred MCC source edges are excluded.
- `DC-BUS-21A/B` connect to batteries, rectifiers, and inverters only; direct RPS-panel DC bus edges are excluded.
- Cable IDs, voltage ratings, channel headings, and control-lane labels are excluded as non-component text.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")

    summary = {
        "document": "40",
        "iteration": "1",
        "rounds": {name: {"nodes": validations[name]["nodes"], "edges": validations[name]["edges"]} for name, _, _ in round_specs},
        "final": final_validation,
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
        "token_usage": {
            "low": token_summary["total_tokens_low"],
            "expected": token_summary["total_tokens_expected"],
            "high": token_summary["total_tokens_high"],
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
