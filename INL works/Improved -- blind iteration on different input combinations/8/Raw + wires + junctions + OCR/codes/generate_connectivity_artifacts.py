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
    "NCC-2A1": "MCC-2A1",
    "NCC-2A2": "MCC-2A2",
    "NCC-2B1": "MCC-2B1",
    "NCC-2B2": "MCC-2B2",
    "NCC-2D": "MCC-2D",
    "MOV-8816A": "MOV-8810A",
    "MOV-8816B": "MOV-8810B",
    "GND-AJ": "GND-A",
}

EXCLUDED_FALSE_COMPONENTS = {"CB-303"}

ADDED_PHYSICAL_NODES = {
    "CB-52B": "Visible Train B breaker between CB-51B and CB-53B, feeding PUMP-RHR-2B.",
    "MCC-2C": "Visible Train A DC/UPS/control MCC, absent from component CSV.",
    "PN-125B": "Visible Train B 125 VDC panel, absent from component CSV.",
    "PUMP-AF-2B": "Visible Train B AF pump, absent from component CSV.",
}

LOGICAL_BUS_NODES = [
    "BUS-4160-N2A",
    "BUS-4160-N2B",
    "BUS-4160-S2A",
    "BUS-4160-S2B",
    "BUS-480-E2A",
    "BUS-480-E2B",
    "BUS-480-N2A",
    "BUS-480-N2B",
    "BUS-125DC-A",
    "BUS-125DC-B",
    "BUS-120AC-A",
    "BUS-120AC-B",
]


def read_component_nodes() -> list[str]:
    with COMPONENT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    nodes: list[str] = []
    for row in rows:
        label = LABEL_CORRECTIONS.get(row["final_label"], row["final_label"])
        if label in EXCLUDED_FALSE_COMPONENTS:
            continue
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

    insert_after("CB-51B", "CB-52B")
    insert_after("MCC-2D", "MCC-2C")
    insert_after("PN-125A", "PN-125B")
    insert_after("PUMP-AF-2A", "PUMP-AF-2B")

    return nodes + LOGICAL_BUS_NODES


NODES = read_component_nodes()


def edge(a: str, b: str, kind: str, note: str = "") -> tuple[str, str, str, str]:
    return (a, b, kind, note)


# Diego round 1 high-recall edges, normalized to final raw-label spellings.
DIEGO_R1_EDGES = [
    edge("GRID-345-01", "SUT-2A", "solid_ac_power"),
    edge("SUT-2A", "CB-402A", "solid_ac_power"),
    edge("CB-402A", "BUS-4160-N2A", "solid_ac_power"),
    edge("GEN-U2", "UAT-2A", "solid_ac_power"),
    edge("UAT-2A", "CB-401A", "solid_ac_power"),
    edge("CB-401A", "BUS-4160-N2A", "solid_ac_power"),
    edge("GEN-U2", "UAT-2B", "solid_ac_power"),
    edge("UAT-2B", "CB-401B", "solid_ac_power"),
    edge("CB-401B", "BUS-4160-N2B", "solid_ac_power"),
    edge("GRID-345-02", "SUT-2B", "solid_ac_power"),
    edge("SUT-2B", "CB-402B", "solid_ac_power"),
    edge("CB-402B", "BUS-4160-N2B", "solid_ac_power"),
    edge("BUS-4160-N2A", "CB-TIE-4160", "solid_ac_power"),
    edge("CB-TIE-4160", "BUS-4160-N2B", "solid_ac_power"),
    edge("BUS-4160-N2A", "BUS-4160-S2A", "solid_ac_power"),
    edge("BUS-4160-N2B", "BUS-4160-S2B", "solid_ac_power"),
    edge("BUS-4160-N2A", "TR-480-N2A", "solid_ac_power"),
    edge("BUS-4160-N2B", "TR-480-N2B", "solid_ac_power"),
    edge("EDG-2A", "CB-EDG-A", "solid_ac_power"),
    edge("CB-EDG-A", "BUS-4160-S2A", "solid_ac_power"),
    edge("EDG-2B", "CB-EDG-B", "solid_ac_power"),
    edge("CB-EDG-B", "BUS-4160-S2B", "solid_ac_power"),
    edge("EDG-2C", "CB-EDG-C", "solid_ac_power"),
    edge("CB-EDG-C", "BUS-4160-S2A", "solid_ac_power"),
    edge("CB-EDG-C", "BUS-4160-S2B", "solid_ac_power"),
    edge("BUS-4160-S2A", "TR-480-2A", "solid_ac_power"),
    edge("TR-480-2A", "BUS-480-E2A", "solid_ac_power"),
    edge("BUS-4160-S2B", "TR-480-2B", "solid_ac_power"),
    edge("TR-480-2B", "BUS-480-E2B", "solid_ac_power"),
    edge("TR-480-N2A", "BUS-480-N2A", "solid_ac_power"),
    edge("TR-480-N2B", "BUS-480-N2B", "solid_ac_power"),
    edge("BUS-4160-S2A", "CT-4160A", "ct_pt_signal"),
    edge("CT-4160A", "RELAY-50/51A", "ct_pt_signal"),
    edge("BUS-4160-S2A", "PT-4160A", "ct_pt_signal"),
    edge("PT-4160A", "RELAY-27A", "ct_pt_signal"),
    edge("RELAY-50/51A", "RELAY-86A", "interlock_trip_permit"),
    edge("RELAY-27A", "RELAY-86A", "interlock_trip_permit"),
    edge("RELAY-86A", "CB-EDG-A", "interlock_trip_permit"),
    edge("RELAY-86A", "CB-401A", "interlock_trip_permit"),
    edge("BUS-4160-S2B", "CT-4160B", "ct_pt_signal"),
    edge("CT-4160B", "RELAY-50/51B", "ct_pt_signal"),
    edge("BUS-4160-S2B", "PT-4160B", "ct_pt_signal"),
    edge("PT-4160B", "RELAY-27B", "ct_pt_signal"),
    edge("RELAY-50/51B", "RELAY-86B", "interlock_trip_permit"),
    edge("RELAY-27B", "RELAY-86B", "interlock_trip_permit"),
    edge("RELAY-86B", "CB-EDG-B", "interlock_trip_permit"),
    edge("RELAY-86B", "CB-401B", "interlock_trip_permit"),
    edge("BUS-480-E2A", "MCC-2A1", "solid_ac_power"),
    edge("BUS-480-E2A", "MCC-2A2", "solid_ac_power"),
    edge("BUS-480-E2A", "PN-480-A", "solid_ac_power"),
    edge("BUS-480-E2A", "GND-A", "equipment_ground"),
    edge("BUS-480-E2A", "DS-480-A", "solid_ac_power"),
    edge("DS-480-A", "DS-480-B", "solid_ac_power"),
    edge("DS-480-B", "BUS-480-E2B", "solid_ac_power"),
    edge("BUS-480-E2B", "MCC-2B1", "solid_ac_power"),
    edge("BUS-480-E2B", "MCC-2B2", "solid_ac_power"),
    edge("BUS-480-E2B", "PN-480-B", "solid_ac_power"),
    edge("BUS-480-E2B", "GND-B", "equipment_ground"),
    edge("BUS-480-N2A", "CB-N1", "solid_ac_power"),
    edge("CB-N1", "CHGR-125A", "solid_ac_power", "Removed by Jennifer: no supported downstream conductor."),
    edge("BUS-480-N2B", "CB-N2", "solid_ac_power"),
    edge("CB-N2", "MCC-2D", "solid_ac_power"),
    edge("PN-480-B", "CHGR-125B", "solid_ac_power"),
    edge("MCC-2C", "PUMP-CHG-2A", "solid_ac_power"),
    edge("MCC-2C", "FAN-VENT-2A", "solid_ac_power"),
    edge("MCC-2D", "PUMP-CHG-2B", "solid_ac_power"),
    edge("MCC-2D", "FAN-VENT-2B", "solid_ac_power"),
    edge("MCC-2A1", "CB-51A", "solid_ac_power"),
    edge("CB-51A", "PUMP-SI-2A", "solid_ac_power"),
    edge("MCC-2A1", "CB-52A", "solid_ac_power"),
    edge("CB-52A", "PUMP-RHR-2A", "solid_ac_power"),
    edge("MCC-2A1", "CB-53A", "solid_ac_power"),
    edge("CB-53A", "PUMP-CS-2A", "solid_ac_power"),
    edge("MCC-2A1", "CB-54A", "solid_ac_power"),
    edge("CB-54A", "PUMP-CCW-2A", "solid_ac_power"),
    edge("MCC-2A2", "CB-55A", "solid_ac_power"),
    edge("CB-55A", "FAN-CRE-2A", "solid_ac_power"),
    edge("MCC-2A2", "CB-56A", "solid_ac_power"),
    edge("CB-56A", "MOV-8801A", "solid_ac_power"),
    edge("MCC-2A2", "CB-57A", "solid_ac_power"),
    edge("CB-57A", "MOV-8802A", "solid_ac_power"),
    edge("MCC-2A2", "CB-58A", "solid_ac_power"),
    edge("CB-58A", "PUMP-AF-2A", "solid_ac_power"),
    edge("CB-58A", "MOV-8810A", "solid_ac_power"),
    edge("PUMP-CHG-2A", "VLV-HV-302A", "solid_ac_power"),
    edge("MCC-2B1", "CB-51B", "solid_ac_power"),
    edge("CB-51B", "PUMP-SI-2B", "solid_ac_power"),
    edge("MCC-2B1", "CB-52B", "solid_ac_power"),
    edge("CB-52B", "PUMP-RHR-2B", "solid_ac_power"),
    edge("MCC-2B1", "CB-53B", "solid_ac_power"),
    edge("CB-53B", "PUMP-CS-2B", "solid_ac_power"),
    edge("MCC-2B1", "CB-54B", "solid_ac_power"),
    edge("CB-54B", "PUMP-CCW-2B", "solid_ac_power"),
    edge("MCC-2B2", "CB-55B", "solid_ac_power"),
    edge("CB-55B", "FAN-CRE-2B", "solid_ac_power"),
    edge("MCC-2B2", "CB-56B", "solid_ac_power"),
    edge("CB-56B", "MOV-8801B", "solid_ac_power"),
    edge("MCC-2B2", "CB-57B", "solid_ac_power"),
    edge("CB-57B", "MOV-8802B", "solid_ac_power"),
    edge("MCC-2B2", "CB-58B", "solid_ac_power"),
    edge("CB-58B", "PUMP-AF-2B", "solid_ac_power"),
    edge("CB-58B", "MOV-8810B", "solid_ac_power"),
    edge("CHGR-125A", "BUS-125DC-A", "solid_dc_125"),
    edge("BAT-2A", "BUS-125DC-A", "solid_dc_125"),
    edge("CHGR-125A", "BAT-2A", "solid_dc_125"),
    edge("BUS-125DC-A", "INV-120A", "solid_dc_125"),
    edge("INV-120A", "BUS-120AC-A", "solid_120vac_control"),
    edge("BUS-125DC-A", "FUSE-125A", "solid_dc_125"),
    edge("FUSE-125A", "PN-125A", "solid_dc_125"),
    edge("PN-125A", "CP-ESFAS-A", "solid_dc_125"),
    edge("BUS-120AC-A", "FUSE-120A", "solid_120vac_control"),
    edge("FUSE-120A", "PN-120A", "solid_120vac_control"),
    edge("PN-120A", "CP-RPS-A", "solid_120vac_control"),
    edge("CHGR-125B", "BUS-125DC-B", "solid_dc_125"),
    edge("BAT-2B", "BUS-125DC-B", "solid_dc_125"),
    edge("CHGR-125B", "BAT-2B", "solid_dc_125"),
    edge("BUS-125DC-B", "INV-120B", "solid_dc_125"),
    edge("INV-120B", "BUS-120AC-B", "solid_120vac_control"),
    edge("BUS-125DC-B", "FUSE-125B", "solid_dc_125"),
    edge("FUSE-125B", "PN-125B", "solid_dc_125"),
    edge("PN-125B", "CP-ESFAS-B", "solid_dc_125"),
    edge("BUS-120AC-B", "FUSE-120B", "solid_120vac_control"),
    edge("FUSE-120B", "PN-120B", "solid_120vac_control"),
    edge("PN-120B", "CP-RPS-B", "solid_120vac_control"),
    edge("CP-ESFAS-A", "RELAY-K1A", "interlock_trip_permit"),
    edge("RELAY-K1A", "CB-51A", "interlock_trip_permit"),
    edge("RELAY-K1A", "CB-52A", "interlock_trip_permit"),
    edge("RELAY-K1A", "CB-53A", "interlock_trip_permit"),
    edge("MOV-8801A", "JB-2A1", "interlock_trip_permit"),
    edge("MOV-8802A", "JB-2A1", "interlock_trip_permit", "Removed by Jennifer: route passes nearby without supported termination."),
    edge("JB-2A1", "CP-ESFAS-A", "interlock_trip_permit"),
    edge("MOV-8810A", "CP-ESFAS-A", "interlock_trip_permit", "Removed by Jennifer: no supported direct termination."),
    edge("CP-ESFAS-B", "RELAY-K1B", "interlock_trip_permit"),
    edge("RELAY-K1B", "CB-51B", "interlock_trip_permit"),
    edge("RELAY-K1B", "CB-52B", "interlock_trip_permit"),
    edge("RELAY-K1B", "CB-53B", "interlock_trip_permit"),
    edge("MOV-8801B", "JB-2B1", "interlock_trip_permit"),
    edge("MOV-8802B", "JB-2B1", "interlock_trip_permit", "Removed by Jennifer: route passes nearby without supported termination."),
    edge("JB-2B1", "CP-ESFAS-B", "interlock_trip_permit", "Removed by Jennifer: no supported direct junction."),
    edge("MOV-8810B", "CP-ESFAS-B", "interlock_trip_permit", "Removed by Jennifer: no supported direct termination."),
]

JENNIFER_REMOVED = {
    frozenset(("CB-N1", "CHGR-125A")),
    frozenset(("MOV-8802A", "JB-2A1")),
    frozenset(("MOV-8810A", "CP-ESFAS-A")),
    frozenset(("MOV-8802B", "JB-2B1")),
    frozenset(("JB-2B1", "CP-ESFAS-B")),
    frozenset(("MOV-8810B", "CP-ESFAS-B")),
}

JENNIFER_ADDED = [
    edge("BUS-480-E2A", "CHGR-125A", "solid_ac_power", "Jennifer accepted: charger feed comes from E2A side."),
    edge("BUS-480-E2A", "MCC-2C", "solid_ac_power", "Jennifer accepted visible source feed."),
    edge("PUMP-AF-2B", "JB-2B1", "interlock_trip_permit", "Jennifer accepted visible B-side dashed termination."),
    edge("PN-120B", "VLV-HV-302B", "solid_120vac_control", "Jennifer accepted visible B-side control/panel termination."),
]

FINAL_EDGES = [
    e for e in DIEGO_R1_EDGES if frozenset((e[0], e[1])) not in JENNIFER_REMOVED
] + JENNIFER_ADDED

DIEGO_R3_REJECTED_ADDITIONS = [
    edge("PUMP-AF-2A", "JB-2A1", "interlock_trip_permit", "Rejected by Jennifer: no visible termination at pump."),
    edge("PN-120A", "VLV-HV-302A", "solid_120vac_control", "Rejected by Jennifer: no clean A-side PN-to-valve termination."),
]

ROUND_DEFINITIONS = [
    ("round_01_diego_high_recall", "Diego", DIEGO_R1_EDGES, "High-recall graph before precision removals; labels normalized for row comparison."),
    ("round_02_jennifer_precision", "Jennifer", FINAL_EDGES, "Precision-reviewed graph: 138 visually supported edges."),
    ("round_03_diego_saturation", "Diego", FINAL_EDGES + DIEGO_R3_REJECTED_ADDITIONS, "Diego proposed two symmetry additions; later rejected."),
    ("round_04_jennifer_final_precision", "Jennifer", FINAL_EDGES, "Rejected symmetry additions and false CB-303 node."),
    ("round_05_diego_node_saturation", "Diego", FINAL_EDGES, "Accepted 138 edges; replaced false CB-303 with visible CB-52B."),
    ("round_06_jennifer_final", "Jennifer", FINAL_EDGES, "Final saturation: 120 nodes, 138 edges, no remaining uncertainties."),
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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["edge_id", "node_a", "node_b", "edge_kind", "status_note", "included_in_final_matrix"],
        )
        writer.writeheader()
        final_keys = {frozenset((a, b)) for a, b, _kind, _note in FINAL_EDGES}
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
    node_kinds = {}
    for node in NODES:
        if node in LOGICAL_BUS_NODES:
            node_kinds[node] = "logical_bus_node"
        elif node in ADDED_PHYSICAL_NODES:
            node_kinds[node] = "physical_component_added_from_raw"
        else:
            node_kinds[node] = "physical_component_from_csv_corrected"

    with (RESULTS / "nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_order", "node_name", "node_kind", "note"])
        writer.writeheader()
        for idx, node in enumerate(NODES, start=1):
            note = ADDED_PHYSICAL_NODES.get(node, "")
            if node in LOGICAL_BUS_NODES:
                note = "Named bus/logical connection node read from raw schematic."
            writer.writerow({"node_order": idx, "node_name": node, "node_kind": node_kinds[node], "note": note})


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
    raw = BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
    label_overlay = BASE / "component_labels_banners_overlay.png"
    wire_overlay = BASE / "wires_mask_overlay.png"
    core_crops = [
        BASE / "codes" / name
        for name in [
            "crop_raw_top_4160_normal_sources.png",
            "crop_raw_middle_4160_safety_buses.png",
            "crop_raw_middle_480_distribution.png",
            "crop_raw_train_a_loads_left.png",
            "crop_raw_train_b_loads_right.png",
            "crop_raw_train_a_dc_control.png",
            "crop_raw_train_b_dc_control.png",
            "zoom2_raw_center_480_tie_dc.png",
            "crop_raw_notes_legend_title.png",
        ]
    ]
    precision_crops = [
        BASE / "codes" / name
        for name in [
            "zoom2_raw_pn480a_mcc2c.png",
            "zoom2_raw_pn480b_chgr125b.png",
            "zoom2_raw_left_lower_interlocks.png",
            "zoom2_raw_right_lower_interlocks.png",
            "zoom4_raw_cb303_bbox.png",
            "zoom4_raw_pump_af_2a_jb.png",
            "zoom4_raw_vlv302a_pn120a.png",
            "zoom5_raw_cb_n1_chgr.png",
            "zoom5_wires_cb_n1_chgr.png",
        ]
    ]

    inventory_images = [raw, label_overlay, wire_overlay]
    diego_images = [raw, label_overlay, wire_overlay] + core_crops
    jennifer_images = [raw, label_overlay, wire_overlay] + core_crops

    calls = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "purpose": "Inventory resources, create crops, inspect notes/title and visual ambiguities.",
            "text": "Document 8 setup and visual inspection.",
            "images": inventory_images + core_crops + precision_crops[:4],
            "output_low": 500,
            "output_expected": 1100,
            "output_high": 2200,
            "reasoning_low": 1200,
            "reasoning_expected": 3500,
            "reasoning_high": 7000,
        },
        {
            "call_id": "subagent-01",
            "round": "01",
            "agent": "Diego",
            "purpose": "High-recall visual extraction.",
            "text": "Full high-recall prompt plus component list and image references.",
            "images": diego_images,
            "output_low": 3500,
            "output_expected": 6200,
            "output_high": 9500,
            "reasoning_low": 5500,
            "reasoning_expected": 10000,
            "reasoning_high": 16000,
        },
        {
            "call_id": "subagent-02",
            "round": "02",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego round 1.",
            "text": "Precision review prompt containing Diego edge proposal.",
            "images": jennifer_images,
            "output_low": 1200,
            "output_expected": 2300,
            "output_high": 4300,
            "reasoning_low": 4500,
            "reasoning_expected": 8000,
            "reasoning_high": 13000,
        },
        {
            "call_id": "subagent-03",
            "round": "03",
            "agent": "Diego",
            "purpose": "Saturation check after Jennifer precision edits.",
            "text": "Jennifer edits and two-edge discrepancy prompt.",
            "images": [],
            "output_low": 250,
            "output_expected": 520,
            "output_high": 1000,
            "reasoning_low": 800,
            "reasoning_expected": 1800,
            "reasoning_high": 3500,
        },
        {
            "call_id": "subagent-04",
            "round": "04",
            "agent": "Jennifer",
            "purpose": "Final precision check of Diego symmetry additions and false CB-303.",
            "text": "Diego additions plus crop-based caveats.",
            "images": precision_crops[4:],
            "output_low": 450,
            "output_expected": 900,
            "output_high": 1800,
            "reasoning_low": 1200,
            "reasoning_expected": 2600,
            "reasoning_high": 5200,
        },
        {
            "call_id": "subagent-05",
            "round": "05",
            "agent": "Diego",
            "purpose": "Node bookkeeping saturation after CB-303 exclusion.",
            "text": "Question about node replacement and final edge acceptance.",
            "images": [],
            "output_low": 200,
            "output_expected": 420,
            "output_high": 900,
            "reasoning_low": 500,
            "reasoning_expected": 1200,
            "reasoning_high": 2600,
        },
        {
            "call_id": "subagent-06",
            "round": "06",
            "agent": "Jennifer",
            "purpose": "Final close-out confirmation.",
            "text": "Confirm CB-52B replacement and final 120-node/138-edge graph.",
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
            "purpose": "Generate matrices, edge files, validation, and final report.",
            "text": "Artifact generation script, validation, and response.",
            "images": [],
            "output_low": 450,
            "output_expected": 900,
            "output_high": 1700,
            "reasoning_low": 1100,
            "reasoning_expected": 2600,
            "reasoning_high": 5200,
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
                "document": "8",
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
        "document": "8",
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
                    "document": "8",
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
        writer.writerow({"action": "exclude", "from_label": "CB-303", "to_label": "", "reason": "False component read on feeder-tie gap/label area."})
        writer.writerow({"action": "add", "from_label": "", "to_label": "CB-52B", "reason": ADDED_PHYSICAL_NODES["CB-52B"]})
        writer.writerow({"action": "add", "from_label": "", "to_label": "MCC-2C", "reason": ADDED_PHYSICAL_NODES["MCC-2C"]})
        writer.writerow({"action": "add", "from_label": "", "to_label": "PN-125B", "reason": ADDED_PHYSICAL_NODES["PN-125B"]})
        writer.writerow({"action": "add", "from_label": "", "to_label": "PUMP-AF-2B", "reason": ADDED_PHYSICAL_NODES["PUMP-AF-2B"]})

    rejected = [
        edge("PUMP-AF-2A", "JB-2A1", "interlock_trip_permit", "Rejected: dashed route passes below/near pump with no termination."),
        edge("PN-120A", "VLV-HV-302A", "solid_120vac_control", "Rejected: PN-120A routes to FUSE-120A/CP-RPS-A; valve is fed from PUMP-CHG-2A."),
        *[e for e in DIEGO_R1_EDGES if frozenset((e[0], e[1])) in JENNIFER_REMOVED],
    ]
    write_edges(RESULTS / "rejected_or_round_only_edges.csv", rejected)


def write_readme() -> None:
    counts = Counter(kind for _a, _b, kind, _note in FINAL_EDGES)
    text = f"""# Document 8 Connectivity Extraction

Final saturated graph:

- Nodes: {len(NODES)}
- Edges: {len(FINAL_EDGES)}
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Important label decisions:

- Corrected `NCC-*` load centers to `MCC-*`.
- Corrected `MOV-8816A/B` to `MOV-8810A/B`.
- Corrected `GND-AJ` to `GND-A`.
- Removed false CSV component `CB-303`; added visually supported missing `CB-52B`.
- Added visible missing nodes `MCC-2C`, `PN-125B`, and `PUMP-AF-2B`.
- Did not include `TB01`-`TB15`; their short stubs did not show supported schematic connectivity.

Final edge-kind counts:

{dict(counts)}

No GT, GT-derived feedback, or off-the-shelf OCR was used. The title-block connection count was treated as sanity metadata; unsupported symmetry edges were rejected in favor of visual precision.
"""
    (RESULTS / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    if len(NODES) != 120:
        raise ValueError(f"expected 120 nodes, got {len(NODES)}")
    if len(set(NODES)) != len(NODES):
        duplicates = [node for node, count in Counter(NODES).items() if count > 1]
        raise ValueError(f"duplicate nodes: {duplicates}")

    for name, _agent, edges, _notes in ROUND_DEFINITIONS:
        edges = unique_edges(edges)
        validate_edges(edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", NODES, edges)
        write_edges(RESULTS / f"{name}_edges.csv", edges)

    final_edges = unique_edges(FINAL_EDGES)
    if len(final_edges) != 138:
        raise ValueError(f"expected 138 final edges, got {len(final_edges)}")
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
