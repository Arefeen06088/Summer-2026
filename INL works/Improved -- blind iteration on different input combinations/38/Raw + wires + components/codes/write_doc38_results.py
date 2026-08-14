from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + components")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def edge(source: str, target: str, evidence: str, confidence: str) -> dict[str, str]:
    return {"source": source, "target": target, "evidence": evidence, "confidence": confidence}


DIEGO_NODES = [
    "TO UNIT AUX BUS CONT.",
    "GEN-U2A",
    "CB-101",
    "TR-UAT-2A",
    "FROM UNIT MAIN GENERATOR",
    "DG-2A / ESF DIESEL A",
    "CB-103",
    "BUS-4160A / 4.16 KV ESF DIV I",
    "CB-201A",
    "TR-201A",
    "CB-301A",
    "BUS-480A / 480 VAC DIV I",
    "CB-105 / N.O. BUS TIE",
    "SOURCE: STARTUP AUX XFMR",
    "TR-SUT-2B",
    "CB-102",
    "TO STATION YARD CONT.",
    "DG-2B / ESF DIESEL B",
    "CB-104",
    "BUS-4160B / 4.16 KV ESF DIV II",
    "CB-201B",
    "TR-201B",
    "CB-301B",
    "BUS-480B / 480 VAC DIV II",
    "480V TIE RESERVED SPACE - NO CONNECTION SHOWN",
    "CB-401A",
    "MCC-2A1",
    "2A-F1 RHR2A feeder",
    "PUMP-RHR2A",
    "2A-F2 CCW2A feeder",
    "PUMP-CCW2A",
    "2A-F3 SW2A feeder",
    "PUMP-SW2A",
    "2A-F4 CR2A feeder",
    "FAN-CR2A",
    "2A-F5 RHR141A feeder",
    "MOV-RHR141A",
    "2A-F6 S1221A feeder",
    "MOV-S1221A",
    "TR-CPT-A",
    "CHGR-2A",
    "S-125DC-A",
    "BAT-125A",
    "125 VDC TRAIN A",
    "RELAY-86A LOCKOUT A",
    "INV-2A",
    "BUS-120AC-A / 120 VAC INST A",
    "RELAY-27A UV BUS A",
    "RPS-PNL-A",
    "CB-401B",
    "MCC-2B1",
    "2B-F1 RHR2B feeder",
    "PUMP-RHR2B",
    "2B-F2 CCW2B feeder",
    "PUMP-CCW2B",
    "2B-F3 SW2B feeder",
    "PUMP-SW2B",
    "2B-F4 CR2B feeder",
    "FAN-CR2B",
    "2B-F5 RHR142B feeder",
    "MOV-RHR142B",
    "2B-F6 S1222B feeder",
    "MOV-S1222B",
    "TR-CPT-B",
    "CHGR-2B",
    "S-125DC-B",
    "BAT-125B",
    "125 VDC TRAIN B",
    "RELAY-86B LOCKOUT B",
    "INV-2B",
    "BUS-120AC-B / 120 VAC INST B",
    "RELAY-27B1 / 27B UV BUS B",
    "RPS-PNL-B",
    "GND-STA / STATION GND",
    "2A-CZ?/2A-C86? dashed risers",
    "2B-CZ?/2B-C86? dashed risers",
    "ESF DIESEL A dashed enclosure",
    "ESF DIESEL B dashed enclosure",
]


FINAL_NODES = [
    "GEN-U2A",
    "CB-101",
    "TR-UAT-2A",
    "BUS-4160A",
    "DG-2A",
    "CB-103",
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
    "CB-201B",
    "TR-201B",
    "CB-301B",
    "BUS-480B",
    "CB-401A",
    "MCC-2A1",
    "CB-401B",
    "MCC-2B1",
    "PUMP-RHR2A",
    "PUMP-CCW2A",
    "PUMP-SW2A",
    "FAN-CR2A",
    "MOV-RHR141A",
    "MOV-SI221A",
    "PUMP-RHR2B",
    "PUMP-CCW2B",
    "PUMP-SW2B",
    "FAN-CR2B",
    "MOV-RHR142B",
    "MOV-SI222B",
    "TR-CPT-A",
    "CHGR-2A",
    "BAT-125A",
    "BUS-125VDC-A",
    "INV-2A",
    "BUS-120AC-A",
    "RELAY-86A",
    "RPS-PNL-A",
    "TR-CPT-B",
    "CHGR-2B",
    "BAT-125B",
    "BUS-125VDC-B",
    "INV-2B",
    "BUS-120AC-B",
    "RELAY-86B",
    "RPS-PNL-B",
]


def diego_round1_edges() -> list[dict[str, str]]:
    return [
        edge("TO UNIT AUX BUS CONT.", "GEN-U2A", "off-page box has short conductor toward generator", "medium"),
        edge("GEN-U2A", "CB-101", "solid horizontal conductor", "high"),
        edge("CB-101", "TR-UAT-2A", "solid horizontal conductor", "high"),
        edge("TR-UAT-2A", "BUS-4160A / 4.16 KV ESF DIV I", "vertical tap with dot to 4.16 kV bus", "high"),
        edge("DG-2A / ESF DIESEL A", "CB-103", "solid horizontal conductor", "high"),
        edge("CB-103", "BUS-4160A / 4.16 KV ESF DIV I", "solid branch joins same 4.16 kV bus riser", "high"),
        edge("BUS-4160A / 4.16 KV ESF DIV I", "CB-201A", "vertical feeder from bus", "high"),
        edge("CB-201A", "TR-201A", "vertical conductor", "high"),
        edge("TR-201A", "CB-301A", "vertical conductor", "high"),
        edge("CB-301A", "BUS-480A / 480 VAC DIV I", "vertical conductor to 480 V bus", "high"),
        edge("BUS-4160A / 4.16 KV ESF DIV I", "CB-105 / N.O. BUS TIE", "solid bus-tie connection", "high"),
        edge("CB-105 / N.O. BUS TIE", "BUS-4160B / 4.16 KV ESF DIV II", "solid bus-tie connection", "high"),
        edge("SOURCE: STARTUP AUX XFMR", "TR-SUT-2B", "source annotation directly above transformer", "low"),
        edge("TR-SUT-2B", "CB-102", "solid horizontal conductor", "high"),
        edge("CB-102", "BUS-4160B / 4.16 KV ESF DIV II", "vertical conductor to bus", "high"),
        edge("TO STATION YARD CONT.", "CB-102", "nearby continuation/source area", "low"),
        edge("DG-2B / ESF DIESEL B", "CB-104", "solid horizontal conductor", "high"),
        edge("CB-104", "BUS-4160B / 4.16 KV ESF DIV II", "solid branch joins 4.16 kV bus riser", "high"),
        edge("BUS-4160B / 4.16 KV ESF DIV II", "CB-201B", "vertical feeder from bus", "high"),
        edge("CB-201B", "TR-201B", "vertical conductor", "high"),
        edge("TR-201B", "CB-301B", "vertical conductor", "high"),
        edge("CB-301B", "BUS-480B / 480 VAC DIV II", "vertical conductor to 480 V bus", "high"),
        edge("BUS-480A / 480 VAC DIV I", "CB-401A", "vertical feeder from 480 V bus", "high"),
        edge("CB-401A", "MCC-2A1", "vertical feeder enters MCC", "high"),
        edge("BUS-480B / 480 VAC DIV II", "CB-401B", "vertical feeder from 480 V bus", "high"),
        edge("CB-401B", "MCC-2B1", "vertical feeder enters MCC", "high"),
        edge("MCC-2A1", "2A-F1 RHR2A feeder", "bucket 01 / 2A-F1 vertical", "high"),
        edge("2A-F1 RHR2A feeder", "PUMP-RHR2A", "vertical conductor lands on pump", "high"),
        edge("MCC-2A1", "2A-F2 CCW2A feeder", "bucket 02 / 2A-F2 vertical", "high"),
        edge("2A-F2 CCW2A feeder", "PUMP-CCW2A", "vertical conductor lands on pump", "high"),
        edge("MCC-2A1", "2A-F3 SW2A feeder", "bucket 03 / 2A-F3 vertical", "high"),
        edge("2A-F3 SW2A feeder", "PUMP-SW2A", "vertical conductor lands on pump", "high"),
        edge("MCC-2A1", "2A-F4 CR2A feeder", "bucket 04 / 2A-F4 vertical", "high"),
        edge("2A-F4 CR2A feeder", "FAN-CR2A", "vertical conductor lands on fan", "high"),
        edge("MCC-2A1", "2A-F5 RHR141A feeder", "bucket 05 / 2A-F5 vertical", "high"),
        edge("2A-F5 RHR141A feeder", "MOV-RHR141A", "vertical conductor lands on MOV", "high"),
        edge("MCC-2A1", "2A-F6 S1221A feeder", "bucket 06 / 2A-F6 vertical", "high"),
        edge("2A-F6 S1221A feeder", "MOV-S1221A", "vertical conductor lands on MOV", "high"),
        edge("MCC-2B1", "2B-F1 RHR2B feeder", "bucket 01 / 2B-F1 vertical", "high"),
        edge("2B-F1 RHR2B feeder", "PUMP-RHR2B", "vertical conductor lands on pump", "high"),
        edge("MCC-2B1", "2B-F2 CCW2B feeder", "bucket 02 / 2B-F2 vertical", "high"),
        edge("2B-F2 CCW2B feeder", "PUMP-CCW2B", "vertical conductor lands on pump", "high"),
        edge("MCC-2B1", "2B-F3 SW2B feeder", "bucket 03 / 2B-F3 vertical", "high"),
        edge("2B-F3 SW2B feeder", "PUMP-SW2B", "vertical conductor lands on pump", "high"),
        edge("MCC-2B1", "2B-F4 CR2B feeder", "bucket 04 / 2B-F4 vertical", "high"),
        edge("2B-F4 CR2B feeder", "FAN-CR2B", "vertical conductor lands on fan", "high"),
        edge("MCC-2B1", "2B-F5 RHR142B feeder", "bucket 05 / 2B-F5 vertical", "high"),
        edge("2B-F5 RHR142B feeder", "MOV-RHR142B", "vertical conductor lands on MOV", "high"),
        edge("MCC-2B1", "2B-F6 S1222B feeder", "bucket 06 / 2B-F6 vertical", "high"),
        edge("2B-F6 S1222B feeder", "MOV-S1222B", "vertical conductor lands on MOV", "high"),
        edge("BUS-480A / 480 VAC DIV I", "TR-CPT-A", "left-side 480 V feeder descends to CPT area", "medium"),
        edge("BUS-480A / 480 VAC DIV I", "CHGR-2A", "left-side 480 V feeder/jog reaches charger input", "medium"),
        edge("TR-CPT-A", "BUS-120AC-A / 120 VAC INST A", "480/120 transformer visually associated with 120 VAC bus", "low"),
        edge("CHGR-2A", "125 VDC TRAIN A", "charger bottom terminal lands on DC train", "high"),
        edge("BAT-125A", "125 VDC TRAIN A", "battery tap/dot on DC train", "high"),
        edge("S-125DC-A", "BAT-125A", "DC section label drawn with battery symbol", "medium"),
        edge("S-125DC-A", "125 VDC TRAIN A", "label aligned with DC train", "medium"),
        edge("125 VDC TRAIN A", "INV-2A", "vertical drop from DC train to inverter", "high"),
        edge("INV-2A", "BUS-120AC-A / 120 VAC INST A", "inverter output connects to 120 VAC bus", "high"),
        edge("125 VDC TRAIN A", "RELAY-86A LOCKOUT A", "lockout relay shown adjacent to train A control tap", "medium"),
        edge("BUS-120AC-A / 120 VAC INST A", "RPS-PNL-A", "vertical tap from 120 VAC inst bus to panel", "high"),
        edge("BUS-120AC-A / 120 VAC INST A", "RELAY-27A UV BUS A", "UV relay adjacent to 120 VAC A dashed area", "medium"),
        edge("RELAY-27A UV BUS A", "RPS-PNL-A", "dashed control line encloses relay and panel", "high"),
        edge("RELAY-86A LOCKOUT A", "RPS-PNL-A", "dashed/control routing plausibly links lockout to RPS area", "low"),
        edge("BUS-480B / 480 VAC DIV II", "TR-CPT-B", "right-side 480 V feeder descends to CPT area", "medium"),
        edge("BUS-480B / 480 VAC DIV II", "CHGR-2B", "right-side 480 V feeder/jog reaches charger input", "medium"),
        edge("TR-CPT-B", "BUS-120AC-B / 120 VAC INST B", "480/120 transformer visually associated with 120 VAC bus", "low"),
        edge("CHGR-2B", "125 VDC TRAIN B", "charger bottom terminal lands on DC train", "high"),
        edge("BAT-125B", "125 VDC TRAIN B", "battery tap/dot on DC train", "high"),
        edge("S-125DC-B", "BAT-125B", "DC section label drawn with battery symbol", "medium"),
        edge("S-125DC-B", "125 VDC TRAIN B", "label aligned with DC train", "medium"),
        edge("125 VDC TRAIN B", "INV-2B", "vertical drop from DC train to inverter", "high"),
        edge("INV-2B", "BUS-120AC-B / 120 VAC INST B", "inverter output connects to 120 VAC bus", "high"),
        edge("125 VDC TRAIN B", "RELAY-86B LOCKOUT B", "lockout relay shown adjacent to train B control tap", "medium"),
        edge("BUS-120AC-B / 120 VAC INST B", "RPS-PNL-B", "vertical tap from 120 VAC inst bus to panel", "high"),
        edge("BUS-120AC-B / 120 VAC INST B", "RELAY-27B1 / 27B UV BUS B", "UV relay adjacent to 120 VAC B dashed area", "medium"),
        edge("RELAY-27B1 / 27B UV BUS B", "RPS-PNL-B", "dashed control line encloses relay and panel", "high"),
        edge("RELAY-86B LOCKOUT B", "RPS-PNL-B", "dashed/control routing plausibly links lockout to RPS area", "low"),
        edge("ESF DIESEL A dashed enclosure", "DG-2A / ESF DIESEL A", "dashed box encloses diesel generator area", "medium"),
        edge("ESF DIESEL B dashed enclosure", "DG-2B / ESF DIESEL B", "dashed box encloses diesel generator area", "medium"),
        edge("2A-CZ?/2A-C86? dashed risers", "RPS-PNL-A", "long dashed/control riser turns into lower A area", "low"),
        edge("2B-CZ?/2B-C86? dashed risers", "RPS-PNL-B", "long dashed/control riser turns into lower B area", "low"),
        edge("2A-CZ?/2A-C86? dashed risers", "GND-STA / STATION GND", "dotted lower run visually terminates at station ground", "low"),
    ]


def final_edges() -> list[dict[str, str]]:
    return [
        edge("GEN-U2A", "CB-101", "solid conductor between generator and breaker", "High"),
        edge("CB-101", "TR-UAT-2A", "solid conductor between breaker and transformer", "High"),
        edge("TR-UAT-2A", "BUS-4160A", "vertical conductor lands on BUS-4160A", "High"),
        edge("DG-2A", "CB-103", "solid conductor between diesel generator and breaker", "High"),
        edge("CB-103", "BUS-4160A", "solid conductor from breaker to BUS-4160A", "High"),
        edge("BUS-4160A", "CB-105", "bus-tie conductor reaches CB-105 from BUS-4160A", "High"),
        edge("CB-105", "BUS-4160B", "bus-tie conductor reaches BUS-4160B from CB-105", "High"),
        edge("TR-SUT-2B", "CB-102", "solid conductor between startup transformer and breaker", "High"),
        edge("CB-102", "BUS-4160B", "vertical conductor from breaker lands on BUS-4160B", "High"),
        edge("DG-2B", "CB-104", "solid conductor between diesel generator and breaker", "High"),
        edge("CB-104", "BUS-4160B", "solid conductor from breaker to BUS-4160B", "High"),
        edge("BUS-4160A", "CB-201A", "vertical feeder from BUS-4160A to breaker", "High"),
        edge("CB-201A", "TR-201A", "stacked vertical connection breaker to transformer", "High"),
        edge("TR-201A", "CB-301A", "stacked vertical connection transformer to breaker", "High"),
        edge("CB-301A", "BUS-480A", "vertical conductor lands on BUS-480A", "High"),
        edge("BUS-4160B", "CB-201B", "vertical feeder from BUS-4160B to breaker", "High"),
        edge("CB-201B", "TR-201B", "stacked vertical connection breaker to transformer", "High"),
        edge("TR-201B", "CB-301B", "stacked vertical connection transformer to breaker", "High"),
        edge("CB-301B", "BUS-480B", "vertical conductor lands on BUS-480B", "High"),
        edge("BUS-480A", "CB-401A", "vertical feeder from BUS-480A to breaker", "High"),
        edge("CB-401A", "MCC-2A1", "solid feeder from breaker into MCC-2A1", "High"),
        edge("BUS-480B", "CB-401B", "vertical feeder from BUS-480B to breaker", "High"),
        edge("CB-401B", "MCC-2B1", "solid feeder from breaker into MCC-2B1", "High"),
        edge("MCC-2A1", "PUMP-RHR2A", "visible feeder from MCC bucket to RHR pump A", "High"),
        edge("MCC-2A1", "PUMP-CCW2A", "visible feeder from MCC bucket to comp svc pump A", "High"),
        edge("MCC-2A1", "PUMP-SW2A", "visible feeder from MCC bucket to service water A", "High"),
        edge("MCC-2A1", "FAN-CR2A", "visible feeder from MCC bucket to control room fan A", "High"),
        edge("MCC-2A1", "MOV-RHR141A", "visible feeder from MCC bucket to RHR HX inlet A MOV", "High"),
        edge("MCC-2A1", "MOV-SI221A", "visible feeder from MCC bucket to SI test valve A MOV", "High"),
        edge("MCC-2B1", "PUMP-RHR2B", "visible feeder from MCC bucket to RHR pump B", "High"),
        edge("MCC-2B1", "PUMP-CCW2B", "visible feeder from MCC bucket to comp svc pump B", "High"),
        edge("MCC-2B1", "PUMP-SW2B", "visible feeder from MCC bucket to service water B", "High"),
        edge("MCC-2B1", "FAN-CR2B", "visible feeder from MCC bucket to control room fan B", "High"),
        edge("MCC-2B1", "MOV-RHR142B", "visible feeder from MCC bucket to RHR HX inlet B MOV", "High"),
        edge("MCC-2B1", "MOV-SI222B", "visible feeder from MCC bucket to SI test valve B MOV", "High"),
        edge("BUS-480A", "TR-CPT-A", "auxiliary 480V drop feeds CPT-A", "Medium"),
        edge("TR-CPT-A", "BUS-120AC-A", "CPT-A secondary appears to land on 120AC-A bus", "Medium"),
        edge("BUS-480A", "CHGR-2A", "auxiliary 480V drop feeds charger 2A", "Medium"),
        edge("CHGR-2A", "BUS-125VDC-A", "charger output lands on 125VDC train A bus", "High"),
        edge("BAT-125A", "BUS-125VDC-A", "battery symbol connected to 125VDC train A bus", "High"),
        edge("BUS-125VDC-A", "INV-2A", "DC bus tap feeds inverter 2A", "High"),
        edge("INV-2A", "BUS-120AC-A", "inverter output lands on 120AC-A bus", "High"),
        edge("BUS-120AC-A", "RPS-PNL-A", "solid 120AC-A feeder drops into RPS panel A", "High"),
        edge("BUS-125VDC-A", "RELAY-86A", "solid tap from 125VDC train A to relay 86A", "Medium"),
        edge("BUS-480B", "TR-CPT-B", "auxiliary 480V drop feeds CPT-B", "Medium"),
        edge("TR-CPT-B", "BUS-120AC-B", "CPT-B secondary lands on 120AC-B bus", "High"),
        edge("BUS-480B", "CHGR-2B", "auxiliary 480V drop feeds charger 2B", "Medium"),
        edge("CHGR-2B", "BUS-125VDC-B", "charger output lands on 125VDC train B bus", "High"),
        edge("BAT-125B", "BUS-125VDC-B", "battery symbol connected to 125VDC train B bus", "High"),
        edge("BUS-125VDC-B", "INV-2B", "DC bus tap feeds inverter 2B", "High"),
        edge("INV-2B", "BUS-120AC-B", "inverter output lands on 120AC-B bus", "High"),
        edge("BUS-120AC-B", "RPS-PNL-B", "solid 120AC-B feeder drops into RPS panel B", "High"),
        edge("BUS-125VDC-B", "RELAY-86B", "solid tap from 125VDC train B to relay 86B", "Medium"),
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
        a, b = item["source"], item["target"]
        if a not in index or b not in index:
            continue
        i, j = index[a], index[b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix, strict=True):
            writer.writerow([node] + row)


def estimate_image_tokens(path: Path, detail: str = "high") -> int:
    with Image.open(path) as img:
        w, h = img.size
    if detail == "low":
        return 85
    scale = min(2048 / max(w, h), 1.0)
    w = math.ceil(w * scale)
    h = math.ceil(h * scale)
    return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)


def image_sum(names: list[str]) -> int:
    return sum(estimate_image_tokens(CROPS / name, "high") for name in names)


MAIN_IMAGES = [
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "focus_top_distribution_components.png",
    "focus_middle_distribution_components.png",
    "focus_lower_distribution_components.png",
    "focus_left_loads_components.png",
    "focus_right_loads_components.png",
    "focus_dc_controls_components.png",
    "focus_dc_controls_wires_overlay.png",
    "bottom_band_components.png",
]

DIEGO_IMAGES = [
    "raw_full_thumb.png",
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "focus_top_distribution_components.png",
    "focus_top_distribution_wires_overlay.png",
    "focus_middle_distribution_components.png",
    "focus_middle_distribution_wires_overlay.png",
    "focus_lower_distribution_components.png",
    "focus_lower_distribution_wires_overlay.png",
    "focus_left_loads_components.png",
    "focus_right_loads_components.png",
    "focus_dc_controls_components.png",
    "focus_dc_controls_wires_overlay.png",
]

JENNIFER_IMAGES = [
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "focus_top_distribution_components.png",
    "focus_top_distribution_wires_overlay.png",
    "focus_middle_distribution_components.png",
    "focus_middle_distribution_wires_overlay.png",
    "focus_dc_controls_components.png",
    "focus_dc_controls_wires_overlay.png",
    "focus_left_loads_components.png",
    "focus_right_loads_components.png",
]


def write_token_estimates() -> None:
    calls = [
        {
            "document": "38",
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
            "document": "38",
            "iteration": "1",
            "round": "round_01_diego",
            "model_call": "Diego high-recall extractor",
            "input_text_tokens_est": 2600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(DIEGO_IMAGES),
            "output_tokens_low": 3200,
            "output_tokens_expected": 5200,
            "output_tokens_high": 7600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Diego reviewed full and focused crops; subagent notification exposed no usage object.",
        },
        {
            "document": "38",
            "iteration": "1",
            "round": "round_02_jennifer",
            "model_call": "Jennifer precision reviewer/refiner",
            "input_text_tokens_est": 7200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(JENNIFER_IMAGES),
            "output_tokens_low": 2000,
            "output_tokens_expected": 3400,
            "output_tokens_high": 5200,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Jennifer reviewed Diego text plus focused crops and pruned pseudo/control edges.",
        },
        {
            "document": "38",
            "iteration": "1",
            "round": "round_03_diego",
            "model_call": "Diego convergence reconciliation",
            "input_text_tokens_est": 3000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(
                [
                    "focus_top_distribution_components.png",
                    "focus_middle_distribution_components.png",
                    "focus_dc_controls_components.png",
                    "focus_dc_controls_wires_overlay.png",
                ]
            ),
            "output_tokens_low": 300,
            "output_tokens_expected": 650,
            "output_tokens_high": 1200,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Diego agreed with Jennifer's corrected graph and restored no edges.",
        },
        {
            "document": "38",
            "iteration": "1",
            "round": "round_04_jennifer_final",
            "model_call": "Jennifer final saturation check",
            "input_text_tokens_est": 1800,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(
                [
                    "components_full_thumb.png",
                    "focus_dc_controls_components.png",
                    "focus_dc_controls_wires_overlay.png",
                ]
            ),
            "output_tokens_low": 300,
            "output_tokens_expected": 600,
            "output_tokens_high": 1000,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Jennifer confirmed saturation and residual uncertain/excluded items.",
        },
        {
            "document": "38",
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
        call["total_tokens_low"] = int(call["input_text_tokens_est"]) + int(call["cached_input_tokens_est"]) + int(call["image_file_input_tokens_est"]) + int(call["output_tokens_low"])
        call["total_tokens_expected"] = int(call["input_text_tokens_est"]) + int(call["cached_input_tokens_est"]) + int(call["image_file_input_tokens_est"]) + int(call["output_tokens_expected"])
        call["total_tokens_high"] = int(call["input_text_tokens_est"]) + int(call["cached_input_tokens_est"]) + int(call["image_file_input_tokens_est"]) + int(call["output_tokens_high"])

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
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    summary = {
        "document": "38",
        "iteration": "1",
        "counting_endpoint_used": False,
        "why_not": "No OpenAI API key was available; usage objects were not exposed by subagent notifications.",
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
                "document": "38",
                "iteration": "1",
                "total_tokens_low": summary["totals"]["low"],
                "total_tokens_expected": summary["totals"]["expected"],
                "total_tokens_high": summary["totals"]["high"],
                "method": summary["method"],
            }
        )


def write_review_files(final: list[dict[str, str]]) -> None:
    rejected = [
        ("TO UNIT AUX BUS CONT.", "", "excluded_node", "off-page continuation label, not a component node"),
        ("FROM UNIT MAIN GENERATOR", "", "excluded_node", "source/annotation label, not a component node"),
        ("SOURCE STARTUP AUX XFMR", "", "excluded_node", "source/annotation label, not a component node"),
        ("TO STATION YARD CONT.", "", "excluded_node", "off-page continuation label, not a component node"),
        ("2A-F1..2A-F6", "", "folded_node", "feeder labels folded into direct MCC-2A1 to load edges"),
        ("2B-F1..2B-F6", "", "folded_node", "feeder labels folded into direct MCC-2B1 to load edges"),
        ("S-125DC-A", "125 VDC TRAIN A", "merged_node", "same visible bus label family represented as BUS-125VDC-A"),
        ("S-125DC-B", "125 VDC TRAIN B", "merged_node", "same visible bus label family represented as BUS-125VDC-B"),
        ("RELAY-27A", "", "uncertain_excluded_node", "visible UV relay, but dashed/control endpoints are not clean enough for final binary topology"),
        ("RELAY-27B", "", "uncertain_excluded_node", "visible UV relay, but dashed/control endpoints are not clean enough for final binary topology"),
        ("BUS-480A", "BUS-480B", "excluded_edge", "nearby note says 480V tie reserved space; no connection shown"),
        ("BUS-4160A", "BUS-4160B", "excluded_edge", "A/B 4.16 kV tie is represented only through CB-105"),
        ("RELAY-86A", "RPS-PNL-A", "uncertain_excluded_edge", "dashed/control logic relationship is visually mixed with routing outline"),
        ("RELAY-86B", "RPS-PNL-B", "uncertain_excluded_edge", "dashed/control logic relationship is visually mixed with routing outline"),
        ("RELAY-27A", "RPS-PNL-A", "uncertain_excluded_edge", "dashed control boundary is visible but endpoint routing is not precise enough"),
        ("RELAY-27B", "RPS-PNL-B", "uncertain_excluded_edge", "dashed control boundary is visible but endpoint routing is not precise enough"),
        ("dashed risers/enclosures/tables", "", "excluded_annotation", "routing boundaries, schedules, notes, title block, status/reference tables are not graph nodes"),
    ]
    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "status", "reason"])
        writer.writerows(rejected)

    (RESULTS / "round_02_jennifer_review.md").write_text(
        "\n".join(
            [
                "# Round 2 Jennifer Precision Review",
                "",
                "Jennifer removed off-page/source/table annotations, folded feeder pseudo-nodes, merged duplicate 125 VDC bus labels, fixed MOV-SI221A/B labels, and excluded imprecise dashed relay/control relationships.",
                "",
                f"Corrected nodes: {len(FINAL_NODES)}",
                f"Corrected edges: {len(final)}",
                "",
                "See round_02_jennifer_edges.csv and uncertain_or_excluded_edges.csv.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (RESULTS / "round_03_diego_reconciliation.md").write_text(
        "\n".join(
            [
                "# Round 3 Diego Reconciliation",
                "",
                "Diego agreed Jennifer's corrected graph should replace the high-recall graph.",
                "",
                "No nodes or edges were restored. Diego affirmed removal of annotation/source nodes, feeder pseudo-nodes, direct 480V and direct 4.16 kV bypass ties, and dashed relay/control edges.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (RESULTS / "round_04_jennifer_final_saturation_check.md").write_text(
        "\n".join(
            [
                "# Round 4 Jennifer Final Saturation Check",
                "",
                "Status: saturated. Jennifer confirmed no further corrections are needed and no nodes or edges should be restored.",
                "",
                "Residual uncertain/excluded items include RELAY-27A/B, dashed RELAY-86-to-RPS logic edges, off-page/source labels, folded feeder labels, dashed risers/enclosures, tables, notes, and title block items.",
                "",
                "TR-CPT-A -> BUS-120AC-A remains the only lower-confidence retained edge; it is visually plausible but less crisp than the B-side.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (RESULTS / "extraction_report.md").write_text(
        "\n".join(
            [
                "# Document 38 Connectivity Extraction Report",
                "",
                "Resources used: raw schematic plus wire/component overlays and visual crops. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.",
                "",
                "## Saturated Decision",
                "",
                "The final matrix follows Jennifer's conservative correction confirmed by Diego: off-page labels, source labels, feeder IDs, dashed risers, enclosures, tables, and imprecise dashed relay/control relationships are excluded from the binary topology. Feeder labels are folded into direct MCC-to-load edges. `S-125DC-A/B` and `125 VDC TRAIN A/B` are represented as `BUS-125VDC-A/B`.",
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
                "- round_04_jennifer_final_edges.csv / round_04_jennifer_final_matrix.csv",
                "- final_edges.csv / final_connectivity_matrix.csv",
                "- uncertain_or_excluded_edges.csv",
                "- token_usage_estimate.csv / token_usage_summary.csv / token_usage_summary.json",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def validate(nodes: list[str], edges: list[dict[str, str]], matrix_path: Path) -> dict[str, object]:
    index = set(nodes)
    unknown = sorted({node for item in edges for node in (item["source"], item["target"]) if node not in index})
    duplicate_pairs = len(edges) - len({tuple(sorted((item["source"], item["target"]))) for item in edges})
    with matrix_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
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
        "matrix_header_nodes": len(rows[0][1:]),
    }


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (CODES / "write_doc38_results.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")

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
    write_review_files(final)
    write_token_estimates()
    summary = {
        "document": "38",
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
