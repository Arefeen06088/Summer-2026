from __future__ import annotations

import csv
import json
import math
from collections import OrderedDict
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + components")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def ordered_nodes() -> list[str]:
    nodes: list[str] = []

    def add(*names: str) -> None:
        for name in names:
            if name not in nodes:
                nodes.append(name)

    add(
        "GRID-161A", "DS-101", "CB-101", "TR-UAT-1A", "CB-102", "BUS-4160-A",
        "RELAY-87A", "RELAY-27A", "METER-A", "PT-41A", "GND-41A", "CB-ESF-A",
        "BUS-4160-ESF-A", "DG-1A", "CB-DG1A", "ATS-1A", "CB-TIE-41", "SYNC-41",
        "GRID-161B", "DS-102", "CB-103", "TR-UAT-1B", "CB-104", "BUS-4160-B",
        "RELAY-87B", "RELAY-27B", "METER-B", "PT-41B", "GND-41B", "CB-ESF-B",
        "BUS-4160-ESF-B", "DG-1B", "CB-DG1B", "ATS-1B",
    )
    for spec in LC_SPECS:
        add(
            spec["fdr"], spec["iso"], spec["tr"], spec["main"], spec["bus"],
            spec["mcc1"], spec["mcc2"], spec["mcc3"], spec["pnl"], spec["pump"],
            spec["motor"], spec["mov"], spec["fan"], spec["htr"], spec["xv"],
            spec["jb"], spec["relay1"], spec["relay2"], spec["inst"], spec["gnd"],
        )
    add(
        "CB-DC-A", "RECT-125A", "BUS-125DC-A", "BAT-125A", "CHGR-AUX-A",
        "METER-DC-A", "GND-DC-A", "INV-1A", "UPS-1A", "CB-UPS-A", "BUS-120AC-A",
        "FUSE-FU-A", "RELAY-KA1", "RELAY-KA2", "ANN-A", "REC-SER-A", "PNL-RPS-A",
        "INST-NIS-A", "PNL-DCS-A", "JB-CTRL-A", "CB-DCTIE", "DC-DC-1",
        "BUS-24DC-C", "BAT-24C", "PNL-RADMON", "RELAY-KTIE",
        "CB-DC-B", "RECT-125B", "BUS-125DC-B", "BAT-125B", "CHGR-AUX-B",
        "METER-DC-B", "GND-DC-B", "INV-1B", "UPS-1B", "CB-UPS-B", "BUS-120AC-B",
        "FUSE-FU-B", "RELAY-KB1", "RELAY-KB2", "ANN-B", "REC-SER-B", "PNL-RPS-B",
        "INST-NIS-B", "PNL-DCS-B", "JB-CTRL-B",
    )
    return nodes


LC_SPECS = [
    {
        "tag": "1A", "source": "BUS-4160-A", "fdr": "CB-1A-FDR", "iso": "DS-1A-ISO",
        "tr": "TR-1A", "main": "CB-1A-MAIN", "bus": "BUS-480-1A", "mcc1": "MCC-1A-1",
        "mcc2": "MCC-1A-2", "mcc3": "MCC-1A-3", "pnl": "PNL-1A", "pump": "PUMP-P101",
        "motor": "MOTOR-M102", "mov": "VALVE-MOV103", "fan": "FAN-F104", "htr": "HTR-H105",
        "xv": "VALVE-XV106", "jb": "JB-1A-1", "relay1": "RELAY-K11", "relay2": "RELAY-K12",
        "inst": "INST-1A", "gnd": "GND-1A",
    },
    {
        "tag": "1C", "source": "BUS-4160-ESF-A", "fdr": "CB-1C-FDR", "iso": "DS-1C-ISO",
        "tr": "TR-1C", "main": "CB-1C-MAIN", "bus": "BUS-480-1C", "mcc1": "MCC-1C-1",
        "mcc2": "MCC-1C-2", "mcc3": "MCC-1C-3", "pnl": "PNL-1C", "pump": "PUMP-P131",
        "motor": "MOTOR-M132", "mov": "VALVE-MOV133", "fan": "FAN-F134", "htr": "HTR-H135",
        "xv": "VALVE-XV136", "jb": "JB-1C-1", "relay1": "RELAY-K21", "relay2": "RELAY-K22",
        "inst": "INST-1C", "gnd": "GND-1C",
    },
    {
        "tag": "1B", "source": "BUS-4160-B", "fdr": "CB-1B-FDR", "iso": "DS-1B-ISO",
        "tr": "TR-1B", "main": "CB-1B-MAIN", "bus": "BUS-480-1B", "mcc1": "MCC-1B-1",
        "mcc2": "MCC-1B-2", "mcc3": "MCC-1B-3", "pnl": "PNL-1B", "pump": "PUMP-P161",
        "motor": "MOTOR-M162", "mov": "VALVE-MOV163", "fan": "FAN-F164", "htr": "HTR-H165",
        "xv": "VALVE-XV166", "jb": "JB-1B-1", "relay1": "RELAY-K31", "relay2": "RELAY-K32",
        "inst": "INST-1B", "gnd": "GND-1B",
    },
    {
        "tag": "2A", "source": "BUS-4160-ESF-A", "fdr": "CB-2A-FDR", "iso": "DS-2A-ISO",
        "tr": "TR-2A", "main": "CB-2A-MAIN", "bus": "BUS-480-2A", "mcc1": "MCC-2A-1",
        "mcc2": "MCC-2A-2", "mcc3": "MCC-2A-3", "pnl": "PNL-2A", "pump": "PUMP-P201",
        "motor": "MOTOR-M202", "mov": "VALVE-MOV203", "fan": "FAN-F204", "htr": "HTR-H205",
        "xv": "VALVE-XV206", "jb": "JB-2A-1", "relay1": "RELAY-K41", "relay2": "RELAY-K42",
        "inst": "INST-2A", "gnd": "GND-2A",
    },
    {
        "tag": "2C", "source": "BUS-4160-ESF-A", "fdr": "CB-2C-FDR", "iso": "DS-2C-ISO",
        "tr": "TR-2C", "main": "CB-2C-MAIN", "bus": "BUS-480-2C", "mcc1": "MCC-2C-1",
        "mcc2": "MCC-2C-2", "mcc3": "MCC-2C-3", "pnl": "PNL-2C", "pump": "PUMP-P231",
        "motor": "MOTOR-M232", "mov": "VALVE-MOV233", "fan": "FAN-F234", "htr": "HTR-H235",
        "xv": "VALVE-XV236", "jb": "JB-2C-1", "relay1": "RELAY-K51", "relay2": "RELAY-K52",
        "inst": "INST-2C", "gnd": "GND-2C",
    },
    {
        "tag": "2B", "source": "BUS-4160-ESF-B", "fdr": "CB-2B-FDR", "iso": "DS-2B-ISO",
        "tr": "TR-2B", "main": "CB-2B-MAIN", "bus": "BUS-480-2B", "mcc1": "MCC-2B-1",
        "mcc2": "MCC-2B-2", "mcc3": "MCC-2B-3", "pnl": "PNL-2B", "pump": "PUMP-P261",
        "motor": "MOTOR-M262", "mov": "VALVE-MOV263", "fan": "FAN-F264", "htr": "HTR-H265",
        "xv": "VALVE-XV266", "jb": "JB-2B-1", "relay1": "RELAY-K61", "relay2": "RELAY-K62",
        "inst": "INST-2B", "gnd": "GND-2B",
    },
]


def make_edges() -> dict[str, OrderedDict[tuple[str, str], dict[str, str]]]:
    rounds = {
        "round_01_diego": OrderedDict(),
        "round_02_jennifer": OrderedDict(),
        "round_03_diego": OrderedDict(),
        "round_04_jennifer_final": OrderedDict(),
    }

    def key(a: str, b: str) -> tuple[str, str]:
        return tuple(sorted((a, b)))

    def add_to(round_name: str, a: str, b: str, confidence: str, evidence: str) -> None:
        rounds[round_name][key(a, b)] = {"a": a, "b": b, "confidence": confidence, "evidence": evidence}

    def add_all(a: str, b: str, confidence: str, evidence: str) -> None:
        for name in rounds:
            add_to(name, a, b, confidence, evidence)

    # 4160 V train A.
    for a, b, ev in [
        ("GRID-161A", "DS-101", "source lead"),
        ("DS-101", "CB-101", "vertical feeder stack"),
        ("CB-101", "TR-UAT-1A", "vertical feeder stack"),
        ("TR-UAT-1A", "CB-102", "vertical feeder stack"),
        ("CB-102", "BUS-4160-A", "breaker lands on bus"),
        ("BUS-4160-A", "RELAY-87A", "bus tap"),
        ("BUS-4160-A", "RELAY-27A", "bus tap"),
        ("BUS-4160-A", "METER-A", "meter tap"),
        ("BUS-4160-A", "PT-41A", "PT tap"),
        ("BUS-4160-A", "GND-41A", "ground branch"),
        ("BUS-4160-A", "CB-ESF-A", "vertical ESF breaker branch"),
        ("CB-ESF-A", "BUS-4160-ESF-A", "ESF breaker to ESF bus"),
        ("DG-1A", "CB-DG1A", "generator output lead"),
        ("CB-DG1A", "ATS-1A", "DG breaker to transfer switch"),
        ("ATS-1A", "BUS-4160-ESF-A", "ATS output to ESF bus"),
        ("BUS-4160-A", "CB-TIE-41", "A side tie"),
        ("CB-TIE-41", "BUS-4160-B", "tie breaker to B bus"),
        ("SYNC-41", "CB-TIE-41", "sync/control tap"),
    ]:
        add_all(a, b, "H", ev)

    # 4160 V train B.
    for a, b, ev in [
        ("GRID-161B", "DS-102", "source lead"),
        ("DS-102", "CB-103", "vertical feeder stack"),
        ("CB-103", "TR-UAT-1B", "vertical feeder stack"),
        ("TR-UAT-1B", "CB-104", "vertical feeder stack"),
        ("CB-104", "BUS-4160-B", "breaker lands on bus"),
        ("BUS-4160-B", "RELAY-87B", "bus tap"),
        ("BUS-4160-B", "RELAY-27B", "bus tap"),
        ("BUS-4160-B", "METER-B", "meter tap"),
        ("BUS-4160-B", "PT-41B", "PT tap"),
        ("BUS-4160-B", "GND-41B", "ground branch"),
        ("BUS-4160-B", "CB-ESF-B", "vertical ESF breaker branch"),
        ("CB-ESF-B", "BUS-4160-ESF-B", "ESF breaker to ESF bus"),
        ("DG-1B", "CB-DG1B", "generator output lead"),
        ("CB-DG1B", "ATS-1B", "DG breaker to transfer switch"),
        ("ATS-1B", "BUS-4160-ESF-B", "ATS output to ESF bus"),
    ]:
        add_all(a, b, "H", ev)

    # Load centers.
    for spec in LC_SPECS:
        add_all(spec["source"], spec["fdr"], "H", f"{spec['tag']} incoming feeder source")
        add_all(spec["fdr"], spec["iso"], "H", "vertical feeder stack")
        add_all(spec["iso"], spec["tr"], "H", "vertical feeder stack")
        add_all(spec["tr"], spec["main"], "H", "vertical feeder stack")

        # Diego kept these as functional/uncertain; Jennifer excluded them from hard final.
        for name in ("round_01_diego", "round_03_diego"):
            add_to(name, spec["main"], spec["bus"], "U", "functional-inferred main-to-480V bus continuity; visible gap in crop")

        add_all(spec["bus"], spec["mcc1"], "H", "480 V bus tap")
        add_all(spec["mcc1"], spec["pump"], "H", "MCC branch")
        add_all(spec["mcc1"], spec["motor"], "H", "MCC branch")
        add_all(spec["bus"], spec["mcc2"], "H", "480 V bus tap")
        add_all(spec["mcc2"], spec["mov"], "H", "MCC branch")
        add_all(spec["mcc2"], spec["fan"], "H", "MCC branch")
        add_all(spec["bus"], spec["mcc3"], "H", "480 V bus tap")
        add_all(spec["bus"], spec["pnl"], "H", "panel bus tap")
        add_all(spec["mcc3"], spec["htr"], "M", "heater branch from MCC-3 area")
        add_all(spec["mcc3"], spec["xv"], "H", "valve branch from MCC-3 area")
        add_all(spec["xv"], spec["jb"], "H", "local valve/JB link")
        add_all(spec["jb"], spec["relay1"], "M", "control line from JB to relay pair")
        add_all(spec["relay1"], spec["relay2"], "M", "relay pair on control line")
        add_all(spec["bus"], spec["inst"], "H", "instrument tap")
        add_all(spec["bus"], spec["gnd"], "H", "ground branch")

        # Diego round 1 high-recall overconnection removed by Jennifer.
        add_to("round_01_diego", spec["inst"], spec["gnd"], "U", "Diego high-recall; Jennifer removed as separate bus taps")

    # Diego's first round explicitly left 2C source ambiguous; keep the extra plausible edge only there.
    add_to("round_01_diego", "BUS-4160-A", "CB-2C-FDR", "U", "Diego high-recall alternate 2C feeder source")

    # Bottom DC/AC A.
    for a, b, conf, ev in [
        ("BUS-480-2A", "CB-DC-A", "H", "480 V 2A feeder to DC rectifier supply"),
        ("CB-DC-A", "RECT-125A", "H", "rectifier input lead"),
        ("RECT-125A", "BUS-125DC-A", "H", "rectifier output to 125 VDC bus"),
        ("BUS-125DC-A", "BAT-125A", "H", "battery tap"),
        ("BUS-125DC-A", "CHGR-AUX-A", "H", "charger tap"),
        ("BUS-125DC-A", "METER-DC-A", "M", "meter tap"),
        ("BUS-125DC-A", "GND-DC-A", "H", "ground branch"),
        ("BUS-125DC-A", "INV-1A", "H", "inverter DC input"),
        ("BUS-125DC-A", "CB-DCTIE", "H", "DC tie left side"),
        ("BUS-125DC-A", "DC-DC-1", "H", "DC-DC input from A 125 VDC bus"),
        ("INV-1A", "UPS-1A", "H", "inverter to UPS lead"),
        ("UPS-1A", "CB-UPS-A", "H", "UPS output lead"),
        ("CB-UPS-A", "BUS-120AC-A", "H", "UPS breaker to vital AC bus"),
        ("BUS-120AC-A", "FUSE-FU-A", "H", "AC bus tap"),
        ("BUS-120AC-A", "PNL-RPS-A", "H", "RPS panel bus tap"),
        ("BUS-120AC-A", "INST-NIS-A", "M", "instrument branch"),
        ("FUSE-FU-A", "RELAY-KA1", "M", "vital AC dashed/control chain"),
        ("RELAY-KA1", "RELAY-KA2", "M", "vital AC dashed/control chain"),
        ("RELAY-KA2", "ANN-A", "M", "vital AC dashed/control chain"),
        ("ANN-A", "REC-SER-A", "M", "vital AC dashed/control chain"),
        ("REC-SER-A", "PNL-RPS-A", "M", "vital AC dashed/control chain"),
        ("PNL-RPS-A", "PNL-DCS-A", "H", "control link down to DCS panel"),
        ("PNL-DCS-A", "JB-CTRL-A", "H", "DCS panel to control JB"),
        ("BUS-24DC-C", "PNL-DCS-A", "H", "24 VDC bus tap"),
    ]:
        add_all(a, b, conf, ev)

    # Bottom DC/AC B.
    for a, b, conf, ev in [
        ("BUS-480-2B", "CB-DC-B", "H", "480 V 2B feeder to DC rectifier supply"),
        ("CB-DC-B", "RECT-125B", "H", "rectifier input lead"),
        ("RECT-125B", "BUS-125DC-B", "H", "rectifier output to 125 VDC bus"),
        ("BUS-125DC-B", "BAT-125B", "H", "battery tap"),
        ("BUS-125DC-B", "CHGR-AUX-B", "H", "charger tap"),
        ("BUS-125DC-B", "METER-DC-B", "M", "meter tap"),
        ("BUS-125DC-B", "GND-DC-B", "H", "ground branch"),
        ("BUS-125DC-B", "INV-1B", "H", "inverter DC input"),
        ("CB-DCTIE", "BUS-125DC-B", "H", "DC tie right side"),
        ("INV-1B", "UPS-1B", "H", "inverter to UPS lead"),
        ("UPS-1B", "CB-UPS-B", "H", "UPS output lead"),
        ("CB-UPS-B", "BUS-120AC-B", "H", "UPS breaker to vital AC bus"),
        ("BUS-120AC-B", "FUSE-FU-B", "H", "AC bus tap"),
        ("BUS-120AC-B", "PNL-RPS-B", "H", "RPS panel bus tap"),
        ("BUS-120AC-B", "INST-NIS-B", "M", "instrument branch"),
        ("FUSE-FU-B", "RELAY-KB1", "M", "vital AC dashed/control chain"),
        ("RELAY-KB1", "RELAY-KB2", "M", "vital AC dashed/control chain"),
        ("RELAY-KB2", "ANN-B", "M", "vital AC dashed/control chain"),
        ("ANN-B", "REC-SER-B", "M", "vital AC dashed/control chain"),
        ("REC-SER-B", "PNL-RPS-B", "M", "vital AC dashed/control chain"),
        ("PNL-RPS-B", "PNL-DCS-B", "H", "control link down to DCS panel"),
        ("PNL-DCS-B", "JB-CTRL-B", "H", "DCS panel to control JB"),
        ("BUS-24DC-C", "PNL-DCS-B", "H", "24 VDC bus tap"),
    ]:
        add_all(a, b, conf, ev)

    # Shared 24 VDC and control.
    for a, b, conf, ev in [
        ("DC-DC-1", "BUS-24DC-C", "H", "DC-DC output to 24 VDC bus"),
        ("BAT-24C", "BUS-24DC-C", "H", "24 VDC battery tap"),
        ("BUS-24DC-C", "PNL-RADMON", "H", "24 VDC bus tap"),
        ("PNL-RADMON", "RELAY-KTIE", "M", "lower control/tie dashed line"),
        ("RELAY-KTIE", "PNL-DCS-B", "M", "lower control/tie dashed line continuation"),
    ]:
        add_all(a, b, conf, ev)

    # Diego round 1 overconnected bottom vital AC devices directly to buses.
    for side, bus, relay1, relay2, ann, rec in [
        ("A", "BUS-120AC-A", "RELAY-KA1", "RELAY-KA2", "ANN-A", "REC-SER-A"),
        ("B", "BUS-120AC-B", "RELAY-KB1", "RELAY-KB2", "ANN-B", "REC-SER-B"),
    ]:
        for node in (relay1, relay2, ann, rec):
            add_to("round_01_diego", bus, node, "U", f"Diego high-recall direct bus tap for {side} vital AC/control device")
    add_to("round_01_diego", "DC-DC-1", "BUS-125DC-B", "U", "Diego uncertain alternate DC-DC input")

    return rounds


def write_edges(path: Path, edges: OrderedDict[tuple[str, str], dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "confidence", "evidence"])
        writer.writeheader()
        for record in edges.values():
            writer.writerow(
                {
                    "source": record["a"],
                    "target": record["b"],
                    "confidence": record["confidence"],
                    "evidence": record["evidence"],
                }
            )


def write_matrix(path: Path, nodes: list[str], edges: OrderedDict[tuple[str, str], dict[str, str]]) -> None:
    edge_keys = set(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                if row_node == col_node:
                    row.append(0)
                else:
                    row.append(1 if tuple(sorted((row_node, col_node))) in edge_keys else 0)
            writer.writerow(row)


def write_uncertain(path: Path) -> None:
    rows = []
    for spec in LC_SPECS:
        rows.append(
            {
                "source": spec["main"],
                "target": spec["bus"],
                "status": "excluded_from_final_matrix",
                "reason": "Visible gap/offset between main breaker output dot and horizontal 480 V bus; Diego would include functionally, Jennifer final excluded as not visually hard-supported.",
            }
        )
    rows += [
        {
            "source": "INST-xx",
            "target": "GND-xx",
            "status": "removed_pattern",
            "reason": "In each 480 V cell, instrument and ground are separate bus taps, not an instrument-to-ground edge.",
        },
        {
            "source": "DC-DC-1",
            "target": "BUS-125DC-B",
            "status": "removed",
            "reason": "No direct visually supported B-side input; DC-DC-1 is connected to BUS-125DC-A and BUS-24DC-C.",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "status", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def image_token_estimate(path: Path) -> dict[str, int]:
    with Image.open(path) as im:
        w, h = im.size
    low = 85
    scale = min(2048 / w, 2048 / h, 1.0)
    w1 = max(1, int(round(w * scale)))
    h1 = max(1, int(round(h * scale)))
    if min(w1, h1) > 768:
        scale2 = 768 / min(w1, h1)
        w1 = max(1, int(round(w1 * scale2)))
        h1 = max(1, int(round(h1 * scale2)))
    tiles = math.ceil(w1 / 512) * math.ceil(h1 / 512)
    expected = 85 + 170 * tiles
    high = math.ceil(expected * 1.35)
    return {"low": low, "expected": expected, "high": high, "width": w, "height": h}


def estimate_text_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def image_sum(paths: list[str]) -> dict[str, int]:
    totals = {"low": 0, "expected": 0, "high": 0}
    for rel in paths:
        est = image_token_estimate(CROPS / rel)
        for key in totals:
            totals[key] += est[key]
    return totals


def write_token_usage(path: Path) -> None:
    diego_images = [
        "raw_full_thumb.png", "components_full_thumb.png",
        "upper_4160_all_raw.png", "upper_4160_all_components.png", "upper_4160_all_wires_overlay.png",
        "middle_distribution_all_raw.png", "middle_distribution_all_components.png", "middle_distribution_all_wires_overlay.png",
        "detail_top_train_a_raw.png", "detail_top_train_a_components.png",
        "detail_top_train_b_raw.png", "detail_top_train_b_components.png",
        "detail_lc_1a_components.png", "detail_lc_1b_components.png", "detail_lc_1c_components.png",
        "detail_lc_2a_components.png", "detail_lc_2b_components.png", "detail_lc_2c_components.png",
        "bottom_control_power_all_raw.png", "bottom_control_power_all_components.png", "bottom_control_power_all_wires_overlay.png",
        "detail_bottom_dc_left_components.png", "detail_bottom_dc_right_components.png", "detail_bottom_center_tie_components.png",
    ]
    jennifer_images = [
        "left_half_components.png", "right_half_components.png", "upper_4160_all_components.png",
        "middle_distribution_all_components.png", "bottom_control_power_all_components.png",
        "detail_lc_1a_components.png", "detail_lc_1b_components.png", "detail_lc_1c_components.png",
        "detail_lc_2a_components.png", "detail_lc_2b_components.png", "detail_lc_2c_components.png",
        "detail_bottom_dc_left_components.png", "detail_bottom_dc_right_components.png", "detail_bottom_center_tie_components.png",
    ]
    calls = [
        {
            "document": "23", "iteration": "1", "call": "main_agent_orchestration",
            "model_role": "main", "text_prompt": "User prompt plus visible conversation summary and orchestration.",
            "input_text_tokens_override": 12000,
            "images": [], "output_expected": 900,
            "notes": "Actual usage object unavailable; broad estimate includes visible doc prompt, compacted history, and platform instructions.",
        },
        {
            "document": "23", "iteration": "1", "call": "round_01_diego",
            "model_role": "subagent Diego high-recall extractor",
            "text_prompt": "High-recall extraction prompt with visual-only/no-GT instructions.",
            "input_text_tokens_override": 400,
            "images": diego_images, "output_expected": 2500,
            "notes": "Actual usage object unavailable from multi_agent_v1 wait result.",
        },
        {
            "document": "23", "iteration": "1", "call": "round_02_jennifer",
            "model_role": "subagent Jennifer precision reviewer",
            "text_prompt": "Precision review prompt plus condensed Diego proposal.",
            "input_text_tokens_override": 2000,
            "images": jennifer_images, "output_expected": 1650,
            "notes": "Actual usage object unavailable from multi_agent_v1 wait result.",
        },
        {
            "document": "23", "iteration": "1", "call": "round_03_diego_consensus",
            "model_role": "subagent Diego consensus check",
            "text_prompt": "Jennifer refinements and remaining main-to-bus question.",
            "input_text_tokens_override": 420,
            "images": [], "output_expected": 550,
            "notes": "Text-only follow-up; actual usage object unavailable.",
        },
        {
            "document": "23", "iteration": "1", "call": "round_04_jennifer_final",
            "model_role": "subagent Jennifer final reviewer",
            "text_prompt": "Diego's remaining disagreement and final decision request.",
            "input_text_tokens_override": 160,
            "images": [], "output_expected": 230,
            "notes": "Text-only follow-up; actual usage object unavailable.",
        },
    ]
    summary_rows = []
    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "document", "iteration", "call", "model_role", "input_text_tokens_est",
            "cached_input_tokens", "image_file_tokens_low", "image_file_tokens_expected",
            "image_file_tokens_high", "output_tokens_low", "output_tokens_expected",
            "output_tokens_high", "reasoning_tokens", "total_low", "total_expected",
            "total_high", "usage_object_status", "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for call in calls:
            text_tokens = call.get("input_text_tokens_override") or estimate_text_tokens(call["text_prompt"])
            image_tokens = image_sum(call["images"])
            output_expected = call["output_expected"]
            output_low = math.ceil(output_expected * 0.65)
            output_high = math.ceil(output_expected * 1.45)
            total_low = math.ceil(text_tokens * 0.75) + image_tokens["low"] + output_low
            total_expected = text_tokens + image_tokens["expected"] + output_expected
            total_high = math.ceil(text_tokens * 1.25) + image_tokens["high"] + output_high
            writer.writerow(
                {
                    "document": call["document"],
                    "iteration": call["iteration"],
                    "call": call["call"],
                    "model_role": call["model_role"],
                    "input_text_tokens_est": text_tokens,
                    "cached_input_tokens": "unavailable",
                    "image_file_tokens_low": image_tokens["low"],
                    "image_file_tokens_expected": image_tokens["expected"],
                    "image_file_tokens_high": image_tokens["high"],
                    "output_tokens_low": output_low,
                    "output_tokens_expected": output_expected,
                    "output_tokens_high": output_high,
                    "reasoning_tokens": "unavailable",
                    "total_low": total_low,
                    "total_expected": total_expected,
                    "total_high": total_high,
                    "usage_object_status": "not exposed by local tools; estimated",
                    "notes": call["notes"],
                }
            )
            summary_rows.append(
                {
                    "document": call["document"],
                    "iteration": call["iteration"],
                    "total_low": total_low,
                    "total_expected": total_expected,
                    "total_high": total_high,
                }
            )
    summary_path = path.with_name("token_usage_summary.csv")
    by_group: dict[tuple[str, str], dict[str, int | str]] = {}
    for row in summary_rows:
        group_key = (str(row["document"]), str(row["iteration"]))
        if group_key not in by_group:
            by_group[group_key] = {
                "document": group_key[0],
                "iteration": group_key[1],
                "total_low": 0,
                "total_expected": 0,
                "total_high": 0,
            }
        by_group[group_key]["total_low"] = int(by_group[group_key]["total_low"]) + int(row["total_low"])
        by_group[group_key]["total_expected"] = int(by_group[group_key]["total_expected"]) + int(row["total_expected"])
        by_group[group_key]["total_high"] = int(by_group[group_key]["total_high"]) + int(row["total_high"])
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["document", "iteration", "total_low", "total_expected", "total_high"])
        writer.writeheader()
        writer.writerows(by_group.values())


def write_report(path: Path, nodes: list[str], final_edges: OrderedDict[tuple[str, str], dict[str, str]]) -> None:
    report = f"""# Document 23 Connectivity Extraction

Source folder: `{BASE}`

Allowed resources used: raw schematic image, detected component overlay, wire mask/overlay, and generated visual crops under `results/visual_crops`.

GT/feedback use: none. OCR use: none.

## Multi-agent rounds

1. Diego high-recall extraction: proposed all visually/geometrically plausible nodes and edges.
2. Jennifer precision review: removed INST-to-GND overedges, corrected feeder sources, added BUS-24DC-C to DCS panel taps, and marked six main-to-480V-bus edges uncertain.
3. Diego consensus: agreed with Jennifer except he preferred including the six main-to-480V-bus links as functional inferred candidates.
4. Jennifer final: excluded the six main-to-480V-bus links from the hard matrix because the raw/wire crops show a visible gap.

## Final hard matrix policy

- Include directly visible high/medium confidence power, control/interlock, metering, and grounding connections.
- Treat named buses as nodes; components that tap a named bus connect to the bus node.
- Exclude section frames, title blocks, notes, reference drawings, and crop borders.
- Exclude functional-but-not-visually-hard-supported candidates from `final_connectivity_matrix.csv`; list them in `uncertain_or_excluded_edges.csv`.

Final node count: {len(nodes)}

Final hard edge count: {len(final_edges)}

Primary result files:

- `final_connectivity_matrix.csv`
- `final_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `uncertain_or_excluded_edges.csv`
- `token_usage_estimate.csv`

## Token estimate method

No OpenAI API key was available, so the Responses input-token counting endpoint could not be called. The local estimate uses:

- Text tokens: `ceil(characters / 4)`.
- Image/file tokens: low = 85 tokens per image, expected = approximate high-detail 512-tile heuristic after resizing to the common 2048/768 bounds, high = 1.35x expected.
- Output tokens: low/expected/high scenario estimates based on actual response lengths and round scope.
- Cached input and hidden reasoning tokens were not exposed by the local subagent tooling.
"""
    path.write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = ordered_nodes()
    rounds = make_edges()
    for round_name, edges in rounds.items():
        write_edges(RESULTS / f"{round_name}_edges.csv", edges)
        write_matrix(RESULTS / f"{round_name}_matrix.csv", nodes, edges)

    final_edges = rounds["round_04_jennifer_final"]
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final_edges)
    write_uncertain(RESULTS / "uncertain_or_excluded_edges.csv")
    write_token_usage(RESULTS / "token_usage_estimate.csv")
    write_report(RESULTS / "extraction_report.md", nodes, final_edges)

    summary = {
        "document": 23,
        "iteration": 1,
        "node_count": len(nodes),
        "final_edge_count": len(final_edges),
        "round_edge_counts": {name: len(edges) for name, edges in rounds.items()},
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
