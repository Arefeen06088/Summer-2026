from __future__ import annotations

import csv
import math
import os
from collections import Counter
from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

COMPONENT_CSV = BASE / "component_visual_ocr_labels.csv"

LABEL_CORRECTIONS = {
    "JB-1A0": "JB-1A",
    "JB-2A0": "JB-2A",
    "JB-1BO": "JB-1B",
    "JB-2BO": "JB-2B",
    "CB-COMP-AI": "CB-COMP-A",
}

LOGICAL_BUS_NODES = [
    "BUS-13K-01",
    "BUS-4160-N1",
    "BUS-4160-N2",
    "BUS-4160S1A",
    "BUS-4160S1B",
    "BUS-480-N1A",
    "BUS-480-N1B",
    "BUS-480-N2A",
    "BUS-480-N2B",
    "BUS-480-A1",
    "BUS-480-A2",
    "BUS-480-B1",
    "BUS-480-B2",
    "BUS-125DC-A",
    "BUS-125DC-B",
    "BUS-120AC-A",
    "BUS-120AC-B",
]

ADDED_PHYSICAL_NODES = {
    "RTD-PNL-A": "Visible sequence/RTD panel absent from component CSV.",
    "RTD-PNL-B": "Visible sequence/RTD panel absent from component CSV.",
    "TDR-SEQ-A": "Visible rounded sequence timer/device absent from component CSV.",
    "TDR-SEQ-B": "Visible rounded sequence timer/device absent from component CSV.",
}


def read_component_nodes() -> list[str]:
    with COMPONENT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    nodes: list[str] = []
    for row in rows:
        label = LABEL_CORRECTIONS.get(row["final_label"], row["final_label"])
        if label not in nodes:
            nodes.append(label)

    def insert_after(anchor: str, new_label: str) -> None:
        if new_label in nodes:
            return
        try:
            idx = nodes.index(anchor) + 1
        except ValueError:
            idx = len(nodes)
        nodes.insert(idx, new_label)

    insert_after("JB-NORM-A", "RTD-PNL-A")
    insert_after("RTD-PNL-A", "TDR-SEQ-A")
    insert_after("JB-NORM-B", "RTD-PNL-B")
    insert_after("RTD-PNL-B", "TDR-SEQ-B")
    return nodes + LOGICAL_BUS_NODES


NODES = read_component_nodes()


def edge(a: str, b: str, kind: str, note: str = "") -> tuple[str, str, str, str]:
    return (a, b, kind, note)


def chain(nodes: list[str], kind: str, note: str = "") -> list[tuple[str, str, str, str]]:
    return [edge(a, b, kind, note) for a, b in zip(nodes, nodes[1:])]


POWER_EDGES: list[tuple[str, str, str, str]] = []
POWER_EDGES += chain(["UTIL-230A", "DS-230A", "SAT-1A", "CB-SAT-A", "BUS-4160S1A"], "solid_power")
POWER_EDGES += chain(["UTIL-230B", "DS-230B", "SAT-1B", "CB-SAT-B", "BUS-4160S1B"], "solid_power")
POWER_EDGES += chain(["GEN-1A", "CB-GEN-1", "BUS-13K-01"], "solid_power")
POWER_EDGES += chain(["BUS-13K-01", "UAT-1A", "CB-UAT-1A", "BUS-4160-N1"], "solid_power")
POWER_EDGES += chain(["BUS-13K-01", "UAT-1B", "CB-UAT-1B", "BUS-4160-N2"], "solid_power")
POWER_EDGES += chain(["BUS-4160-N1", "CB-TIE-41N", "BUS-4160-N2"], "solid_power")

for prefix in ["N1A", "N1B"]:
    POWER_EDGES += chain(
        [f"BUS-4160-N1", f"CB-4160-{prefix}", f"TR-480-{prefix}", f"CB-480-{prefix}", f"BUS-480-{prefix}"],
        "solid_power",
    )
for prefix in ["N2A", "N2B"]:
    POWER_EDGES += chain(
        [f"BUS-4160-N2", f"CB-4160-{prefix}", f"TR-480-{prefix}", f"CB-480-{prefix}", f"BUS-480-{prefix}"],
        "solid_power",
    )

POWER_EDGES += chain(["BUS-480-N1A", "MCC-NORM-1A", "PN-480-N1A"], "solid_power")
POWER_EDGES += chain(["BUS-480-N1B", "MCC-NORM-1B", "PN-480-N1B"], "solid_power")
POWER_EDGES += chain(["BUS-480-N2A", "MCC-NORM-2A", "PN-480-N2A"], "solid_power")
POWER_EDGES += chain(["BUS-480-N2B", "MCC-NORM-2B", "PN-480-N2B"], "solid_power")

for panel, branches in {
    "PN-480-N1A": [
        ("CB-CWP-1A", "PUMP-CWP-1A"),
        ("CB-HEAT-1A", "HTR-1A"),
        ("CB-AHU-1A", "FAN-AHU-1A"),
    ],
    "PN-480-N1B": [
        ("CB-CWP-1B", "PUMP-CWP-1B"),
        ("CB-SUMP-1B", "PUMP-SUMP-1B"),
        ("CB-LTG-1B", "PN-LTG-1B"),
    ],
    "PN-480-N2A": [
        ("CB-CWP-2A", "PUMP-CWP-2A"),
        ("CB-VAC-2A", "PUMP-VAC-2A"),
        ("CB-AHU-2A", "FAN-AHU-2A"),
    ],
    "PN-480-N2B": [
        ("CB-CWP-2B", "PUMP-CWP-2B"),
        ("CB-OIL-2B", "PUMP-OIL-2B"),
        ("CB-LTG-2B", "PN-LTG-2B"),
    ],
}.items():
    for breaker, load in branches:
        POWER_EDGES += chain([panel, breaker, load], "solid_power")

POWER_EDGES += chain(["EDG-1A", "CB-EDG-A", "BUS-4160S1A"], "solid_power")
POWER_EDGES += chain(["BUS-4160S1A", "CB-481A", "TR-480-A1", "CB-LV-A1", "BUS-480-A1"], "solid_power")
POWER_EDGES += chain(["BUS-4160S1A", "CB-482A", "TR-480-A2", "CB-LV-A2", "BUS-480-A2"], "solid_power")
POWER_EDGES += [edge("BUS-480-A1", "MCC-SAF-A1", "solid_power")]
POWER_EDGES += chain(["MCC-SAF-A1", "CB-RHR-A", "PUMP-RHR-A"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-A1", "CB-SI-A", "PUMP-SI-A"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-A1", "CB-CCW-A", "PUMP-CCW-A"], "solid_power")
POWER_EDGES += [edge("BUS-480-A2", "MCC-SAF-A2", "solid_power")]
POWER_EDGES += chain(["MCC-SAF-A2", "CB-CVC-A", "PUMP-CVC-A"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-A2", "CB-CRF-A", "FAN-CR-A"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-A2", "CB-COMP-A", "COMP-AIR-A"], "solid_power")
POWER_EDGES += [edge("FAN-CR-A", "PN-MOV-A", "solid_power")]
POWER_EDGES += chain(["PN-MOV-A", "FU-8810A", "MOV-8810A"], "solid_power")
POWER_EDGES += chain(["PN-MOV-A", "FU-HV302A", "VLV-HV-302A"], "solid_power")
POWER_EDGES += chain(["PN-MOV-A", "FU-RCICA", "MOV-RCIC-A"], "solid_power")
POWER_EDGES += chain(["PN-MOV-A", "FU-SWA", "MOV-SW-A"], "solid_power")

POWER_EDGES += chain(["EDG-1B", "CB-EDG-B", "BUS-4160S1B"], "solid_power")
POWER_EDGES += chain(["BUS-4160S1B", "CB-481B", "TR-480-B1", "CB-LV-B1", "BUS-480-B1"], "solid_power")
POWER_EDGES += chain(["BUS-4160S1B", "CB-482B", "TR-480-B2", "CB-LV-B2", "BUS-480-B2"], "solid_power")
POWER_EDGES += [edge("BUS-480-B1", "MCC-SAF-B1", "solid_power")]
POWER_EDGES += chain(["MCC-SAF-B1", "CB-RHR-B", "PUMP-RHR-B"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-B1", "CB-SI-B", "PUMP-SI-B"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-B1", "CB-CCW-B", "PUMP-CCW-B"], "solid_power")
POWER_EDGES += [edge("BUS-480-B2", "MCC-SAF-B2", "solid_power")]
POWER_EDGES += chain(["MCC-SAF-B2", "CB-CVC-B", "PUMP-CVC-B"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-B2", "CB-CRF-B", "FAN-CR-B"], "solid_power")
POWER_EDGES += chain(["MCC-SAF-B2", "CB-COMP-B", "COMP-AIR-B"], "solid_power")
POWER_EDGES += [edge("FAN-CR-B", "PN-MOV-B", "solid_power")]
POWER_EDGES += chain(["PN-MOV-B", "FU-8810B", "MOV-8810B"], "solid_power")
POWER_EDGES += chain(["PN-MOV-B", "FU-HV302B", "VLV-HV-302B"], "solid_power")
POWER_EDGES += chain(["PN-MOV-B", "FU-RCICB", "MOV-RCIC-B"], "solid_power")
POWER_EDGES += chain(["PN-MOV-B", "FU-SWB", "MOV-SW-B"], "solid_power")

POWER_EDGES += [
    edge("BAT-125A", "BUS-125DC-A", "solid_dc_control_power"),
    edge("CHG-125A", "BUS-125DC-A", "solid_dc_control_power"),
    edge("BUS-125DC-A", "GND-A", "solid_dc_control_power"),
    edge("BUS-125DC-A", "PN-125A", "solid_dc_control_power"),
]
POWER_EDGES += chain(["BUS-125DC-A", "INV-120A", "BUS-120AC-A", "PN-120A"], "solid_dc_control_power")
POWER_EDGES += [
    edge("BAT-125B", "BUS-125DC-B", "solid_dc_control_power"),
    edge("CHG-125B", "BUS-125DC-B", "solid_dc_control_power"),
    edge("BUS-125DC-B", "GND-B", "solid_dc_control_power"),
    edge("BUS-125DC-B", "PN-125B", "solid_dc_control_power"),
]
POWER_EDGES += chain(["BUS-125DC-B", "INV-120B", "BUS-120AC-B", "PN-120B"], "solid_dc_control_power")


CONTROL_FINAL = [
    edge("CT-41A", "RELAY-50/51A", "control_signal"),
    edge("RELAY-50/51A", "RELAY-86A", "control_signal"),
    edge("PT-41A", "RELAY-50/51A", "control_signal"),
    edge("CB-EDG-A", "CB-482A", "control_signal"),
    edge("CB-482A", "RELAY-50/51A", "control_signal"),
    edge("RELAY-86A", "MCC-SAF-A1", "control_signal"),
    edge("RELAY-86A", "MCC-SAF-A2", "control_signal", "Jennifer precision fanout correction."),
    edge("CT-41B", "RELAY-27B", "control_signal"),
    edge("RELAY-27B", "RELAY-86B", "control_signal"),
    edge("PT-41B", "RELAY-27B", "control_signal"),
    edge("RELAY-27B", "CB-481B", "control_signal"),
    edge("CB-481B", "CB-482B", "control_signal"),
    edge("CB-482B", "CB-EDG-B", "control_signal"),
    edge("RELAY-86B", "MCC-SAF-B1", "control_signal"),
    edge("RELAY-86B", "MCC-SAF-B2", "control_signal", "Jennifer precision fanout correction."),
    edge("PN-480-N1A", "PN-480-N1B", "control_signal"),
    edge("PUMP-SUMP-1B", "MTR-480-N1", "control_signal"),
    edge("MTR-480-N1", "JB-NORM-A", "control_signal"),
    edge("JB-NORM-A", "RTD-PNL-A", "control_signal"),
    edge("RTD-PNL-A", "TB-SEQ-A", "control_signal"),
    edge("TB-SEQ-A", "TDR-SEQ-A", "control_signal"),
    edge("FAN-AHU-2A", "MTR-480-N2", "control_signal"),
    edge("MTR-480-N2", "JB-NORM-B", "control_signal"),
    edge("JB-NORM-B", "RTD-PNL-B", "control_signal"),
    edge("RTD-PNL-B", "TB-SEQ-B", "control_signal"),
    edge("TB-SEQ-B", "TDR-SEQ-B", "control_signal"),
    edge("PUMP-SI-A", "JB-2A", "control_signal"),
    edge("PUMP-RHR-A", "JB-1A", "control_signal"),
    edge("PN-125A", "JB-1A", "control_signal"),
    edge("PN-125A", "JB-2A", "control_signal"),
    edge("PN-120A", "PLC-ESF-A", "control_signal"),
    edge("PLC-ESF-A", "RELAY-K1A", "control_signal"),
    edge("PLC-ESF-A", "RELAY-K2A", "control_signal"),
    edge("RELAY-K2A", "ANN-ESF-A", "control_signal"),
    edge("PN-120A", "ANN-ESF-A", "control_signal"),
    edge("PLC-ESF-A", "ANN-ESF-A", "control_signal"),
    edge("PUMP-SI-B", "JB-2B", "control_signal"),
    edge("PUMP-RHR-B", "JB-1B", "control_signal"),
    edge("PN-125B", "JB-1B", "control_signal"),
    edge("PN-125B", "JB-2B", "control_signal"),
    edge("PN-120B", "PLC-ESF-B", "control_signal"),
    edge("PLC-ESF-B", "RELAY-K1B", "control_signal"),
    edge("PLC-ESF-B", "RELAY-K2B", "control_signal"),
    edge("RELAY-K2B", "ANN-ESF-B", "control_signal"),
    edge("PN-120B", "ANN-ESF-B", "control_signal"),
    edge("PLC-ESF-B", "ANN-ESF-B", "control_signal"),
]

REMOVED_CONTROL = [
    edge("MCC-SAF-A1", "MCC-SAF-A2", "control_signal", "Removed: fanout route, no direct MCC-to-MCC terminal."),
    edge("MCC-SAF-B1", "MCC-SAF-B2", "control_signal", "Removed: fanout route, no direct MCC-to-MCC terminal."),
    edge("PN-480-N2A", "PN-480-N2B", "control_signal", "Removed: no clean termination."),
    edge("PUMP-RHR-A", "PUMP-SI-A", "control_signal", "Removed: separate drops/no terminal junction."),
    edge("PUMP-RHR-B", "PUMP-SI-B", "control_signal", "Removed: separate drops/no terminal junction."),
    edge("PN-MOV-A", "PN-120A", "control_signal", "Removed: long nearby route without supported endpoint."),
    edge("PN-MOV-B", "PN-120B", "control_signal", "Removed: long nearby route without supported endpoint."),
    edge("RELAY-K1A", "RELAY-K2A", "control_signal", "Removed: relay fanout, no direct relay-to-relay edge."),
    edge("RELAY-K1B", "RELAY-K2B", "control_signal", "Removed: relay fanout, no direct relay-to-relay edge."),
]

UNCERTAIN_CONTROL = [
    edge("RTD-PNL-A", "RTD-PNL-B", "control_signal", "Uncertain: horizontal dashed run suggestive but no clear bridge/termination."),
]

DIEGO_R1_CONTROL = [
    e for e in CONTROL_FINAL if frozenset((e[0], e[1])) not in {
        frozenset(("RELAY-86A", "MCC-SAF-A2")),
        frozenset(("RELAY-86B", "MCC-SAF-B2")),
    }
] + REMOVED_CONTROL + UNCERTAIN_CONTROL

FINAL_EDGES = POWER_EDGES + CONTROL_FINAL
DIEGO_R1_EDGES = POWER_EDGES + DIEGO_R1_CONTROL
DIEGO_R3_EDGES = FINAL_EDGES

ROUND_DEFINITIONS = [
    ("round_01_diego_high_recall", "Diego", DIEGO_R1_EDGES, "High-recall graph: included uncertain/overconnected dashed control candidates."),
    ("round_02_jennifer_precision", "Jennifer", FINAL_EDGES, "Precision graph: 192 certain edges; RTD-PNL-A--RTD-PNL-B excluded."),
    ("round_03_diego_saturation", "Diego", DIEGO_R3_EDGES, "Accepted Jennifer precision result."),
    ("round_04_jennifer_final", "Jennifer", FINAL_EDGES, "Final saturation confirmation."),
]


def unique_edges(edges: list[tuple[str, str, str, str]]) -> list[tuple[str, str, str, str]]:
    seen: set[frozenset[str]] = set()
    result: list[tuple[str, str, str, str]] = []
    for item in edges:
        key = frozenset((item[0], item[1]))
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def validate_edges(edges: list[tuple[str, str, str, str]]) -> None:
    node_set = set(NODES)
    missing = sorted({n for e in edges for n in e[:2] if n not in node_set})
    if missing:
        raise ValueError(f"edge references missing nodes: {missing}")


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b, _kind, _note in edges:
        ia = index[a]
        ib = index[b]
        if ia == ib:
            raise ValueError(f"self-loop is not expected: {a}")
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    final_keys = {frozenset((a, b)) for a, b, _kind, _note in FINAL_EDGES}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["edge_id", "node_a", "node_b", "edge_kind", "status_note", "included_in_final_matrix"],
        )
        writer.writeheader()
        for idx, (a, b, kind, note) in enumerate(edges, start=1):
            writer.writerow(
                {
                    "edge_id": f"E-{idx:03d}",
                    "node_a": a,
                    "node_b": b,
                    "edge_kind": kind,
                    "status_note": note,
                    "included_in_final_matrix": "yes" if frozenset((a, b)) in final_keys else "no",
                }
            )


def write_nodes() -> None:
    with (RESULTS / "nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_order", "node_name", "node_kind", "note"])
        writer.writeheader()
        for idx, node in enumerate(NODES, start=1):
            if node in LOGICAL_BUS_NODES:
                kind = "logical_bus_node"
                note = "Named bus/logical conductor node read from raw schematic."
            elif node in ADDED_PHYSICAL_NODES:
                kind = "physical_component_added_from_raw"
                note = ADDED_PHYSICAL_NODES[node]
            else:
                kind = "physical_component_from_csv_corrected"
                note = ""
            writer.writerow({"node_order": idx, "node_name": node, "node_kind": kind, "note": note})


def image_token_estimate(path: Path) -> int:
    with Image.open(path) as im:
        w, h = im.size
    scale = min(2048 / max(w, h), 1.0)
    sw = math.ceil(w * scale)
    sh = math.ceil(h * scale)
    tiles = math.ceil(sw / 512) * math.ceil(sh / 512)
    return 85 + 170 * tiles


def text_tokens_estimate(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def write_token_estimates() -> None:
    raw = BASE / "raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png"
    label_overlay = BASE / "component_labels_banners_overlay.png"
    wire_overlay = BASE / "wires_mask_overlay.png"
    core_crops = [
        BASE / "codes" / name
        for name in [
            "crop_raw_top_sources_13kv_4160.png",
            "crop_raw_middle_4160_normal_and_safety.png",
            "crop_raw_middle_480_normal_mcc.png",
            "crop_raw_left_safety_480_loads.png",
            "crop_raw_right_safety_480_loads.png",
            "crop_raw_left_mov_controls.png",
            "crop_raw_right_mov_controls.png",
            "crop_raw_center_jb_tb_sequence.png",
            "crop_raw_left_dc_control.png",
            "crop_raw_right_dc_control.png",
        ]
    ]
    precision_crops = [
        BASE / "codes" / name
        for name in [
            "zoom4_raw_jb_labels_a.png",
            "zoom4_raw_jb_labels_b.png",
            "zoom4_raw_cb_comp_a.png",
            "zoom4_raw_center_seq_labels.png",
        ]
    ]

    calls = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "purpose": "Inventory resources, create crops, inspect notes/title and ambiguous labels.",
            "text": "Document 9 setup, local visual inspection, component list, and crop generation.",
            "images": [raw, label_overlay, wire_overlay] + core_crops + precision_crops,
            "output_low": 650,
            "output_expected": 1300,
            "output_high": 2600,
            "reasoning_low": 1600,
            "reasoning_expected": 4200,
            "reasoning_high": 8500,
        },
        {
            "call_id": "subagent-01",
            "round": "01",
            "agent": "Diego",
            "purpose": "High-recall visual extraction.",
            "text": "High-recall prompt with 159 labels, bus candidates, raw/overlay/crop references.",
            "images": [raw, label_overlay, wire_overlay] + core_crops,
            "output_low": 4200,
            "output_expected": 7600,
            "output_high": 11500,
            "reasoning_low": 6500,
            "reasoning_expected": 12000,
            "reasoning_high": 19000,
        },
        {
            "call_id": "subagent-02",
            "round": "02",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego round 1.",
            "text": "Precision prompt containing Diego's complete high-recall graph.",
            "images": [raw, label_overlay, wire_overlay] + core_crops,
            "output_low": 1200,
            "output_expected": 2400,
            "output_high": 4500,
            "reasoning_low": 5000,
            "reasoning_expected": 9000,
            "reasoning_high": 15000,
        },
        {
            "call_id": "subagent-03",
            "round": "03",
            "agent": "Diego",
            "purpose": "Saturation check after Jennifer precision edits.",
            "text": "Jennifer edits, removals, uncertainty, and saturation question.",
            "images": [],
            "output_low": 260,
            "output_expected": 520,
            "output_high": 1100,
            "reasoning_low": 800,
            "reasoning_expected": 1800,
            "reasoning_high": 3800,
        },
        {
            "call_id": "subagent-04",
            "round": "04",
            "agent": "Jennifer",
            "purpose": "Final saturation close-out.",
            "text": "Confirm final 180-node/192-edge graph and excluded uncertainty.",
            "images": [],
            "output_low": 180,
            "output_expected": 360,
            "output_high": 800,
            "reasoning_low": 400,
            "reasoning_expected": 1000,
            "reasoning_high": 2200,
        },
        {
            "call_id": "main-02",
            "round": "artifact",
            "agent": "Main",
            "purpose": "Generate matrices, validate, and report.",
            "text": "Artifact generation script, validation, and final response.",
            "images": [],
            "output_low": 500,
            "output_expected": 950,
            "output_high": 1800,
            "reasoning_low": 1200,
            "reasoning_expected": 2800,
            "reasoning_high": 5500,
        },
    ]

    rows = []
    for call in calls:
        image_tokens = sum(image_token_estimate(path) for path in call["images"] if path.exists())
        text_tokens = text_tokens_estimate(call["text"])
        input_est = image_tokens + text_tokens
        total_low = input_est + call["output_low"] + call["reasoning_low"]
        total_expected = input_est + call["output_expected"] + call["reasoning_expected"]
        total_high = input_est + call["output_high"] + call["reasoning_high"]
        rows.append(
            {
                "call_id": call["call_id"],
                "document": "9",
                "iteration": "1",
                "round": call["round"],
                "agent": call["agent"],
                "purpose": call["purpose"],
                "input_tokens_est": input_est,
                "cached_input_tokens_est": 0,
                "image_file_input_tokens_est": image_tokens,
                "output_tokens_low": call["output_low"],
                "output_tokens_expected": call["output_expected"],
                "output_tokens_high": call["output_high"],
                "reasoning_tokens_low": call["reasoning_low"],
                "reasoning_tokens_expected": call["reasoning_expected"],
                "reasoning_tokens_high": call["reasoning_high"],
                "total_tokens_low": total_low,
                "total_tokens_expected": total_expected,
                "total_tokens_high": total_high,
                "usage_object_available": "not_exposed",
                "notes": "No OPENAI_API_KEY was available; local chars/4 plus high-detail image tile estimate used.",
            }
        )

    with (RESULTS / "model_call_usage_estimates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    totals = {
        "document": "9",
        "iteration": "1",
        "api_key_available": "yes" if os.environ.get("OPENAI_API_KEY") else "no",
        "responses_token_count_endpoint_used": "no_api_key" if not os.environ.get("OPENAI_API_KEY") else "not_used_local_run",
        "usage_objects_collected": "not_exposed_by_multi_agent_tool",
        "model_calls_counted": len(rows),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in rows),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in rows),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in rows),
        "method": "Local estimate: chars/4 for text plus OpenAI-style high-detail image tile estimate (85 + 170 per 512px tile after scaling); low/expected/high bands for unknown output and reasoning.",
    }
    with (RESULTS / "token_usage_totals_by_document.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(totals.keys()))
        writer.writeheader()
        writer.writerow(totals)

    artifact_rows = []
    for path in sorted(BASE.glob("*.png")) + sorted((BASE / "codes").glob("*.png")):
        artifact_rows.append(
            {
                "file": str(path.relative_to(BASE)),
                "image_tokens_est": image_token_estimate(path),
                "bytes": path.stat().st_size,
            }
        )
    with (RESULTS / "local_artifact_token_counts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "image_tokens_est", "bytes"])
        writer.writeheader()
        writer.writerows(artifact_rows)


def write_summaries() -> None:
    with (RESULTS / "round_summaries.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "document",
                "iteration",
                "round",
                "agent",
                "interpretation",
                "node_count",
                "edge_count",
                "delta_edges_from_previous_round",
                "notes",
            ],
        )
        writer.writeheader()
        previous_count = None
        for idx, (round_name, agent, edges, notes) in enumerate(ROUND_DEFINITIONS, start=1):
            edge_count = len(unique_edges(edges))
            writer.writerow(
                {
                    "document": "9",
                    "iteration": "1",
                    "round": f"{idx:02d}",
                    "agent": agent,
                    "interpretation": round_name,
                    "node_count": len(NODES),
                    "edge_count": edge_count,
                    "delta_edges_from_previous_round": "" if previous_count is None else edge_count - previous_count,
                    "notes": notes,
                }
            )
            previous_count = edge_count

    with (RESULTS / "node_label_corrections.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["action", "from_label", "to_label", "reason"])
        writer.writeheader()
        for old, new in LABEL_CORRECTIONS.items():
            writer.writerow({"action": "rename", "from_label": old, "to_label": new, "reason": "Raw schematic label inspection."})
        for node, reason in ADDED_PHYSICAL_NODES.items():
            writer.writerow({"action": "add", "from_label": "", "to_label": node, "reason": reason})

    write_edges(RESULTS / "rejected_or_uncertain_edges.csv", REMOVED_CONTROL + UNCERTAIN_CONTROL)


def write_readme() -> None:
    counts = Counter(kind for _a, _b, kind, _note in FINAL_EDGES)
    text = f"""# Document 9 Connectivity Extraction

Final saturated graph:

- Nodes: {len(NODES)}
- Edges: {len(FINAL_EDGES)}
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Final edge-kind counts:

{dict(counts)}

Important decisions:

- Added 17 named bus/logical conductor nodes.
- Added visible missing nodes `RTD-PNL-A`, `RTD-PNL-B`, `TDR-SEQ-A`, `TDR-SEQ-B`.
- Corrected `JB-1A0/JB-2A0/JB-1BO/JB-2BO` to `JB-1A/JB-2A/JB-1B/JB-2B`.
- Corrected `CB-COMP-AI` to `CB-COMP-A`.
- Excluded uncertain `RTD-PNL-A -- RTD-PNL-B`.

No GT, GT-derived feedback, or off-the-shelf OCR was used.
"""
    (RESULTS / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    final_edges = unique_edges(FINAL_EDGES)
    diego_edges = unique_edges(DIEGO_R1_EDGES)

    if len(NODES) != 180:
        raise ValueError(f"expected 180 nodes, got {len(NODES)}")
    if len(set(NODES)) != len(NODES):
        duplicates = [node for node, count in Counter(NODES).items() if count > 1]
        raise ValueError(f"duplicate nodes: {duplicates}")
    if len(POWER_EDGES) != 146:
        raise ValueError(f"expected 146 power edges, got {len(POWER_EDGES)}")
    if len(CONTROL_FINAL) != 46:
        raise ValueError(f"expected 46 final control edges, got {len(CONTROL_FINAL)}")
    if len(final_edges) != 192:
        raise ValueError(f"expected 192 final edges, got {len(final_edges)}")
    if len(diego_edges) != 200:
        raise ValueError(f"expected 200 Diego R1 edges, got {len(diego_edges)}")

    for name, _agent, edges, _notes in ROUND_DEFINITIONS:
        edges = unique_edges(edges)
        validate_edges(edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", NODES, edges)
        write_edges(RESULTS / f"{name}_edges.csv", edges)

    validate_edges(final_edges)
    write_nodes()
    write_matrix(RESULTS / "final_connectivity_matrix.csv", NODES, final_edges)
    write_edges(RESULTS / "final_connectivity_edges.csv", final_edges)
    write_summaries()
    write_token_estimates()
    write_readme()

    kind_counts = Counter(kind for _a, _b, kind, _note in final_edges)
    print(f"nodes={len(NODES)} final_edges={len(final_edges)} kind_counts={dict(kind_counts)}")


if __name__ == "__main__":
    main()
