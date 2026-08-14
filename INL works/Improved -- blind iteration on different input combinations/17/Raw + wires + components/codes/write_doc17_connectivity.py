from __future__ import annotations

import csv
import math
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires + components"
)
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def add(edges: list[tuple[str, str, str, str]], a: str, b: str, typ: str, evidence: str) -> None:
    edges.append((a, b, typ, evidence))


def add_topology(edges: list[tuple[str, str, str, str]]) -> None:
    e = edges
    add(e, "GEN-001", "UAT-1A", "P", "solid generator feeder visibly lands at UAT-1A")
    add(e, "GEN-001", "UAT-1B", "P", "solid generator feeder visibly lands at UAT-1B")
    add(e, "SAT-1A", "CB-SAT-1A", "P", "solid vertical feeder from SAT-1A to breaker")
    add(e, "CB-SAT-1A", "BUS-4160-A", "P", "breaker feeder lands on BUS-4160-A with black dot")
    add(e, "UAT-1A", "CB-UAT-1A", "P", "solid vertical feeder from UAT-1A to breaker")
    add(e, "CB-UAT-1A", "BUS-4160-A", "P", "breaker feeder lands on BUS-4160-A with black dot")
    add(e, "DG-1A", "CB-DG-1A", "P", "solid vertical feeder from DG-1A to breaker")
    add(e, "CB-DG-1A", "BUS-4160-A", "P", "breaker feeder lands on BUS-4160-A with black dot")
    add(e, "BUS-4160-A", "PT-4160-A", "INST", "dotted instrument tap drops from BUS-4160-A to PT")
    add(e, "BUS-4160-A", "CB-TIE-4AB", "P", "solid 4.16 kV bus tie segment enters tie breaker")
    add(e, "CB-TIE-4AB", "BUS-4160-B", "P", "solid 4.16 kV bus tie segment exits tie breaker")
    add(e, "UAT-1B", "CB-UAT-1B", "P", "solid vertical feeder from UAT-1B to breaker")
    add(e, "CB-UAT-1B", "BUS-4160-B", "P", "breaker feeder lands on BUS-4160-B with black dot")
    add(e, "DG-1B", "CB-DG-1B", "P", "solid vertical feeder from DG-1B to breaker")
    add(e, "CB-DG-1B", "BUS-4160-B", "P", "breaker feeder lands on BUS-4160-B with black dot")
    add(e, "SAT-1B", "CB-SAT-1B", "P", "solid vertical feeder from SAT-1B to breaker")
    add(e, "CB-SAT-1B", "BUS-4160-B", "P", "breaker feeder lands on BUS-4160-B with black dot")
    add(e, "BUS-4160-B", "PT-4160-B", "INST", "dotted instrument tap drops from BUS-4160-B to PT")

    add(e, "BUS-4160-A", "CB-TR-A1", "P", "solid feeder from BUS-4160-A to load-center transformer breaker")
    add(e, "CB-TR-A1", "TR-LC-A1", "P", "solid feeder from breaker into transformer")
    add(e, "TR-LC-A1", "CB-480-A1", "P", "solid feeder from transformer to 480 V breaker")
    add(e, "CB-480-A1", "BUS-480-A", "P", "solid feeder lands on BUS-480-A")
    add(e, "BUS-4160-A", "CB-TR-A2", "P", "solid feeder from BUS-4160-A to second transformer breaker")
    add(e, "CB-TR-A2", "TR-LC-A2", "P", "solid feeder from breaker into transformer")
    add(e, "TR-LC-A2", "CB-480-A2", "P", "solid feeder from transformer to 480 V breaker")
    add(e, "CB-480-A2", "BUS-480-A", "P", "solid feeder lands on BUS-480-A")
    add(e, "BUS-480-A", "CB-TIE-480AB", "P", "solid 480 V tie segment enters tie breaker")
    add(e, "CB-TIE-480AB", "BUS-480-B", "P", "solid 480 V tie segment exits tie breaker")

    add(e, "BUS-4160-B", "CB-TR-B1", "P", "solid feeder from BUS-4160-B to load-center transformer breaker")
    add(e, "CB-TR-B1", "TR-LC-B1", "P", "solid feeder from breaker into transformer")
    add(e, "TR-LC-B1", "CB-480-B1", "P", "solid feeder from transformer to 480 V breaker")
    add(e, "CB-480-B1", "BUS-480-B", "P", "solid feeder lands on BUS-480-B")
    add(e, "BUS-4160-B", "CB-TR-B2", "P", "solid feeder from BUS-4160-B to second transformer breaker")
    add(e, "CB-TR-B2", "TR-LC-B2", "P", "solid feeder from breaker into transformer")
    add(e, "TR-LC-B2", "CB-480-B2", "P", "solid feeder from transformer to 480 V breaker")
    add(e, "CB-480-B2", "BUS-480-B", "P", "solid feeder lands on BUS-480-B")

    add(e, "BUS-480-A", "AM-480-A", "INST", "dotted instrument tap from BUS-480-A to ammeter")
    add(e, "BUS-480-A", "VM-480-A", "INST", "dotted instrument tap from BUS-480-A to voltmeter")
    add(e, "BUS-480-A", "CT-480-A1", "INST", "dotted instrument tap from BUS-480-A to CT")
    add(e, "BUS-480-A", "GND-SWGR-A", "GND", "solid branch from switchgear bus to ground")
    add(e, "BUS-480-B", "AM-480-B", "INST", "dotted instrument tap from BUS-480-B to ammeter")
    add(e, "BUS-480-B", "VM-480-B", "INST", "dotted instrument tap from BUS-480-B to voltmeter")
    add(e, "BUS-480-B", "CT-480-B1", "INST", "dotted instrument tap from BUS-480-B to CT")
    add(e, "BUS-480-B", "GND-SWGR-B", "GND", "solid branch from switchgear bus to ground")


def add_chain(
    edges: list[tuple[str, str, str, str]],
    bus: str,
    breaker: str,
    chain: list[tuple[str, str]],
) -> None:
    add(edges, bus, breaker, "P", f"solid branch from {bus} to {breaker}")
    prev = breaker
    for node, typ in chain:
        style = {
            "P": "solid feeder chain",
            "GND": "solid branch to ground",
            "CTRL": "dashed control path",
            "INST": "dotted instrument path",
        }[typ]
        add(edges, prev, node, typ, style)
        prev = node


def add_feeders(edges: list[tuple[str, str, str, str]], air_prefix: str) -> None:
    a_bus = "BUS-480-A"
    b_bus = "BUS-480-B"
    a_specs = [
        ("CB-101A", [("DS-101A", "P"), ("MS-101A", "P"), ("PUMP-SLC-1A", "P"), ("TB-SLC-1A", "P")]),
        ("CB-102A", [("FU-102A", "P"), ("MS-102A", "P"), ("PUMP-COV-1A", "P"), ("GND-CCW-1A", "GND")]),
        ("CB-103A", [("DS-103A", "P"), ("MS-103A", "P"), ("PUMP-RHR-1A", "P"), ("LS-RHR-1A", "INST")]),
        ("CB-104A", [("FU-104A", "P"), ("MS-104A", "P"), ("PUMP-CS-1A", "P"), ("TB-CS-1A", "P")]),
        ("CB-105A", [("DS-105A", "P"), ("MS-105A", "P"), ("FAN-CRDH-1A", "P"), ("GND-FAN-1A", "GND")]),
        ("CB-106A", [("FU-106A", "P"), ("RELAY-K106A", "CTRL"), ("MOV-RHCU-101A", "CTRL"), ("LS-RHCU-101A", "INST")]),
        ("CB-107A", [("DS-107A", "P"), ("RELAY-K107A", "CTRL"), ("MOV-RHR-102A", "CTRL"), ("LS-RHR-102A", "INST")]),
        ("CB-108A", [("FU-108A", "P"), ("MS-108A", "P"), ("HTR-PZR-1A", "P"), ("TB-HTR-1A", "P")]),
        ("CB-109A", [("DS-109A", "P"), ("MS-109A", "P"), ("PUMP-SW-1A", "P"), ("GND-SW-1A", "GND")]),
        ("CB-110A", [("FU-110A", "P"), ("MS-110A", "P"), ("HTR-AHU-1A", "P"), ("GND-AHU-1A", "GND")]),
        ("CB-111A", [("DS-111A", "P"), ("MS-111A", "P"), (f"{air_prefix}-AIR-1A", "P"), ("TB-AIR-1A", "P")]),
        ("CB-112A", [("FU-112A", "P"), ("RELAY-K112A", "CTRL"), ("INET-RAD-1A", "CTRL"), ("JB-RAD-1A", "INST")]),
    ]
    b_specs = [
        ("CB-201B", [("DS-201B", "P"), ("MS-201B", "P"), ("PUMP-SLC-1B", "P"), ("TB-SLC-1B", "P")]),
        ("CB-202B", [("FU-202B", "P"), ("MS-202B", "P"), ("PUMP-COV-1B", "P"), ("GND-CCW-1B", "GND")]),
        ("CB-203B", [("DS-203B", "P"), ("MS-203B", "P"), ("PUMP-RHR-1B", "P"), ("LS-RHR-1B", "INST")]),
        ("CB-204B", [("FU-204B", "P"), ("MS-204B", "P"), ("PUMP-CS-1B", "P"), ("TB-CS-1B", "P")]),
        ("CB-205B", [("DS-205B", "P"), ("MS-205B", "P"), ("FAN-CRDH-1B", "P"), ("GND-FAN-1B", "GND")]),
        ("CB-206B", [("FU-206B", "P"), ("RELAY-K206B", "CTRL"), ("MOV-RHCU-101B", "CTRL"), ("LS-RHCU-101B", "INST")]),
        ("CB-207B", [("DS-207B", "P"), ("RELAY-K207B", "CTRL"), ("MOV-RHR-102B", "CTRL"), ("LS-RHR-102B", "INST")]),
        ("CB-208B", [("FU-208B", "P"), ("MS-208B", "P"), ("HTR-PZR-1B", "P"), ("TB-HTR-1B", "P")]),
        ("CB-209B", [("DS-209B", "P"), ("MS-209B", "P"), ("PUMP-SW-1B", "P"), ("GND-SW-1B", "GND")]),
        ("CB-210B", [("FU-210B", "P"), ("MS-210B", "P"), ("HTR-AHU-1B", "P"), ("GND-AHU-1B", "GND")]),
        ("CB-211B", [("DS-211B", "P"), ("MS-211B", "P"), (f"{air_prefix}-AIR-1B", "P"), ("TB-AIR-1B", "P")]),
        ("CB-212B", [("FU-212B", "P"), ("RELAY-K212B", "CTRL"), ("INET-RAD-1B", "CTRL"), ("JB-RAD-1B", "INST")]),
    ]
    for breaker, chain in a_specs:
        add_chain(edges, a_bus, breaker, chain)
    for breaker, chain in b_specs:
        add_chain(edges, b_bus, breaker, chain)


def add_control(edges: list[tuple[str, str, str, str]], ann_split: bool) -> None:
    e = edges
    add(e, "BUS-480-A", "CB-DC-A", "P", "solid feed down left side to DC/control breaker")
    add(e, "CB-DC-A", "CHGR-125-A", "P", "solid feed from breaker to charger")
    add(e, "CHGR-125-A", "BAT-125-A", "P", "solid connection between charger and battery")
    add(e, "BAT-125-A", "BUS-125DC-A", "P", "solid battery drop lands on BUS-125DC-A")
    add(e, "BUS-125DC-A", "GND-DC-A", "GND", "solid branch from DC bus to ground")
    add(e, "BUS-125DC-A", "INV-120-A", "P", "solid branch from DC bus to inverter")
    add(e, "INV-120-A", "BUS-120AC-A", "P", "solid inverter output lands on BUS-120AC-A")
    add(e, "BUS-120AC-A", "STS-120-A", "P", "solid branch from 120 VAC bus to STS")
    add(e, "STS-120-A", "PNL-RPS-A", "CTRL", "dashed control run from STS to RPS panel")
    add(e, "PNL-RPS-A", "TB-RPS-A", "CTRL", "dashed control run from RPS panel to terminal block")
    add(e, "PNL-RPS-A", "RELAY-UV-A1", "CTRL", "dashed control run from RPS panel to UV relay")
    add(e, "PNL-RPS-A", "RELAY-UV-A2", "CTRL", "dashed control run from RPS panel to UV relay")
    add(e, "PNL-ESF-A", "TB-ESF-A", "CTRL", "dashed control run from ESF panel to terminal block")
    add(e, "PNL-ESF-A", "RELAY-RPS-A", "CTRL", "dashed control run from ESF panel to RPS relay")
    add(e, "PNL-ESF-A", "RELAY-ESF-A", "CTRL", "dashed control run from ESF panel to ESF relay")
    add(e, "RELAY-ESF-A", "REC-SOE-1", "INST", "dotted instrument run from ESF relay to SOE recorder")
    add(e, "PNL-DCS", "REC-SOE-1", "CTRL", "dashed run from DCS panel lands at REC-SOE-1")

    if ann_split:
        add(e, "PNL-ANN-A", "ANN-ESF-A", "CTRL", "Diego R1 read the singular ANN panel as A-suffixed")
    else:
        add(e, "PNL-ANN", "ANN-ESF-A", "CTRL", "singular PNL-ANN dashed line lands at ANN-ESF-A")

    add(e, "BUS-125DC-A", "CB-DCTIE-AB", "P", "solid DC bus tie segment enters normally-open tie breaker")
    add(e, "CB-DCTIE-AB", "BUS-125DC-B", "P", "solid DC bus tie segment exits normally-open tie breaker")

    add(e, "BUS-480-B", "CB-DC-B", "P", "solid feed down right side to DC/control breaker")
    add(e, "CB-DC-B", "CHGR-125-B", "P", "solid feed from breaker to charger")
    add(e, "CHGR-125-B", "BAT-125-B", "P", "solid connection between charger and battery")
    add(e, "BAT-125-B", "BUS-125DC-B", "P", "solid battery drop lands on BUS-125DC-B")
    add(e, "BUS-125DC-B", "GND-DC-B", "GND", "solid branch from DC bus to ground")
    add(e, "BUS-125DC-B", "INV-120-B", "P", "solid branch from DC bus to inverter")
    add(e, "INV-120-B", "BUS-120AC-B", "P", "solid inverter output lands on BUS-120AC-B")
    add(e, "BUS-120AC-B", "STS-120-B", "P", "solid branch from 120 VAC bus to STS")
    add(e, "STS-120-B", "PNL-RPS-B", "CTRL", "dashed control run from STS to RPS panel")
    add(e, "PNL-RPS-B", "TB-RPS-B", "CTRL", "dashed control run from RPS panel to terminal block")
    add(e, "PNL-RPS-B", "RELAY-UV-B1", "CTRL", "dashed control run from RPS panel to UV relay")
    add(e, "PNL-RPS-B", "RELAY-UV-B2", "CTRL", "dashed control run from RPS panel to UV relay")
    add(e, "PNL-ESF-B", "TB-ESF-B", "CTRL", "dashed control run from ESF panel to terminal block")
    add(e, "PNL-ESF-B", "RELAY-RPS-B", "CTRL", "dashed control run from ESF panel to RPS relay")
    add(e, "PNL-ESF-B", "RELAY-ESF-B", "CTRL", "dashed control run from ESF panel to ESF relay")
    add(e, "RELAY-ESF-B", "REC-SOE-2", "INST", "dotted instrument run from ESF relay to SOE recorder")
    if ann_split:
        add(e, "PNL-ANN-B", "ANN-ESF-B", "CTRL", "Diego R1 read the singular ANN panel as B-suffixed")
    else:
        add(e, "PNL-ANN", "ANN-ESF-B", "CTRL", "singular PNL-ANN dashed line lands at ANN-ESF-B")


def make_edges(air_prefix: str, ann_split: bool) -> list[tuple[str, str, str, str]]:
    edges: list[tuple[str, str, str, str]] = []
    add_topology(edges)
    add_feeders(edges, air_prefix=air_prefix)
    add_control(edges, ann_split=ann_split)
    return edges


def ordered_nodes(edges: list[tuple[str, str, str, str]]) -> list[str]:
    nodes: list[str] = []
    seen: set[str] = set()
    for a, b, _, _ in edges:
        for n in (a, b):
            if n not in seen:
                seen.add(n)
                nodes.append(n)
    return nodes


def write_sparse(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type", "evidence"])
        writer.writerows(edges)


def write_matrix(path: Path, edges: list[tuple[str, str, str, str]]) -> tuple[int, int]:
    nodes = ordered_nodes(edges)
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b, _, _ in edges:
        if a == b:
            matrix[index[a]][index[b]] = 1
        else:
            matrix[index[a]][index[b]] = 1
            matrix[index[b]][index[a]] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)
    ones = sum(sum(row) for row in matrix)
    return len(nodes), ones


def validate(edges: list[tuple[str, str, str, str]]) -> dict[str, int | bool]:
    nodes = ordered_nodes(edges)
    unique_pairs = {tuple(sorted((a, b))) for a, b, _, _ in edges}
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unique_undirected_edges": len(unique_pairs),
        "has_duplicate_undirected_edges": len(unique_pairs) != len(edges),
        "self_loops": sum(1 for a, b, _, _ in edges if a == b),
        "expected_matrix_ones": 2 * len(unique_pairs),
    }


UNCERTAIN = [
    ("CB-TR-A1", "MASTER-TERMINAL-BLOCKS", "CTRL", "dashed route leaves breaker area but exact terminal landing is unclear"),
    ("CB-TR-A2", "MASTER-TERMINAL-BLOCKS", "CTRL", "dashed route approaches terminal block area but terminal number is unclear"),
    ("CB-TR-B1", "MASTER-TERMINAL-BLOCKS", "CTRL", "dashed route crosses top-center area but exact terminal landing is unclear"),
    ("CB-TR-B2", "MASTER-TERMINAL-BLOCKS", "CTRL", "dashed route leaves breaker area but exact terminal landing is unclear"),
    ("PNL-DCS", "ANN-ESF-A", "CTRL", "annunciation routing crosses nearby but no clear landed junction"),
    ("PNL-DCS", "ANN-ESF-B", "CTRL", "annunciation routing crosses nearby but no clear landed junction"),
    ("RELAY-UV-A1", "TRAIN-A-CONTROL-WIREWAY", "CTRL", "dashed run continues into wireway with destination not explicit"),
    ("RELAY-UV-A2", "TRAIN-A-CONTROL-WIREWAY", "CTRL", "dashed run continues into wireway with destination not explicit"),
    ("RELAY-UV-B1", "TRAIN-B-CONTROL-WIREWAY", "CTRL", "dashed run continues into wireway with destination not explicit"),
    ("RELAY-UV-B2", "TRAIN-B-CONTROL-WIREWAY", "CTRL", "dashed run continues into wireway with destination not explicit"),
    ("RELAY-RPS-A", "TRAIN-A-RPS-ESF-CONTROL", "CTRL", "side-channel run continues beyond visible labelled landing"),
    ("RELAY-RPS-B", "TRAIN-B-RPS-ESF-CONTROL", "CTRL", "side-channel run continues beyond visible labelled landing"),
]


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type", "reason"])
        writer.writerows(UNCERTAIN)


def image_tokens(path: Path) -> int:
    try:
        from PIL import Image

        with Image.open(path) as img:
            w, h = img.size
    except Exception:
        return 0
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def write_token_estimate(path: Path) -> None:
    image_payloads = {
        "Diego R1 extraction": [
            CROPS / "raw_synthetic_npp_aux_power_schematic_overlap_fixed" / "whole_drawing_area.png",
            CROPS / "focused_raw" / "top_4160_left_half_fine.png",
            CROPS / "focused_raw" / "top_4160_right_half_fine.png",
            CROPS / "focused_raw" / "bus480_a_feeders_1.png",
            CROPS / "focused_raw" / "bus480_a_feeders_2.png",
            CROPS / "focused_raw" / "bus480_b_feeders_1.png",
            CROPS / "focused_raw" / "bus480_b_feeders_2.png",
            CROPS / "focused_raw" / "dc_control_a_fine.png",
            CROPS / "focused_raw" / "ann_control_center_fine.png",
            CROPS / "focused_raw" / "dc_control_b_fine.png",
        ],
        "Jennifer R1 review": [
            CROPS / "focused_raw" / "top_4160_left_half_fine.png",
            CROPS / "focused_raw" / "top_4160_right_half_fine.png",
            CROPS / "focused_raw" / "bus480_a_feeders_1.png",
            CROPS / "focused_raw" / "bus480_a_feeders_2.png",
            CROPS / "focused_raw" / "bus480_b_feeders_1.png",
            CROPS / "focused_raw" / "bus480_b_feeders_2.png",
            CROPS / "focused_raw" / "dc_control_a_fine.png",
            CROPS / "focused_raw" / "ann_control_center_fine.png",
            CROPS / "focused_raw" / "dc_control_b_fine.png",
            CROPS / "focused_raw" / "ann_pnl_ann_zoom.png",
            CROPS / "focused_raw" / "air_label_a_candidate_1_6x.png",
            CROPS / "focused_raw" / "air_label_b_6x.png",
        ],
        "Diego R2 revision": [
            CROPS / "focused_raw" / "ann_pnl_ann_zoom.png",
            CROPS / "focused_raw" / "air_label_a_candidate_1_6x.png",
            CROPS / "focused_raw" / "air_label_b_6x.png",
        ],
        "Jennifer R2 saturation": [
            CROPS / "focused_raw" / "ann_pnl_ann_zoom.png",
            CROPS / "focused_raw" / "air_label_a_candidate_1_6x.png",
            CROPS / "focused_raw" / "air_label_b_6x.png",
        ],
    }
    calls = [
        ("17", "1", "main setup/resource inspection", 1800, 0, 500, 600, 1200),
        ("17", "1", "Diego R1 extraction", 3200, sum(image_tokens(p) for p in image_payloads["Diego R1 extraction"]), 8500, 5000, 10500),
        ("17", "1", "Jennifer R1 precision review", 11800, sum(image_tokens(p) for p in image_payloads["Jennifer R1 review"]), 5200, 3500, 7000),
        ("17", "1", "main integration/artifact planning", 5200, 0, 1000, 900, 2000),
        ("17", "1", "Diego R2 revision after corrections", 4600, sum(image_tokens(p) for p in image_payloads["Diego R2 revision"]), 900, 500, 1500),
        ("17", "1", "Jennifer R2 final saturation", 2500, sum(image_tokens(p) for p in image_payloads["Jennifer R2 saturation"]), 300, 150, 700),
        ("17", "1", "main final report", 2200, 0, 700, 500, 1200),
    ]
    rows = []
    for document, iteration, call, text_in, img_in, expected_out, low_out, high_out in calls:
        expected_total = text_in + img_in + expected_out
        low_total = text_in + img_in + low_out
        high_total = text_in + img_in + high_out
        rows.append((document, iteration, call, text_in, img_in, 0, expected_out, "n/a", low_total, expected_total, high_total))
    total_low = sum(r[8] for r in rows)
    total_expected = sum(r[9] for r in rows)
    total_high = sum(r[10] for r in rows)
    lines = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key was available, so the Responses input-token counting endpoint and model usage objects could not be collected. Image input tokens are estimated with a local high-detail tile heuristic: 85 base tokens plus 170 tokens per 512 px tile. Text tokens are estimated from prompt sizes and transcript volume.",
        "",
        "| Document | Iteration | Model call | Text input | Image/file input | Cached input | Expected output | Reasoning | Low total | Expected total | High total |",
        "|---|---:|---|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]} | {row[10]} |"
        )
    lines.extend(
        [
            f"| **17** | **1** | **Total** |  |  |  |  |  | **{total_low}** | **{total_expected}** | **{total_high}** |",
            "",
            "Actual usage object fields are unavailable in this environment. Cached input and reasoning-token values are therefore reported as 0/n/a rather than guessed.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(path: Path, final_edges: list[tuple[str, str, str, str]], validation: dict[str, int | bool]) -> None:
    lines = [
        "# Document 17 Connectivity Extraction Report",
        "",
        "Scope: raw schematic and visual aids only. No GT, target, answer, or GT-derived feedback was used. No off-the-shelf OCR was used; labels were read visually from the provided crops.",
        "",
        "## Jennifer R1 Corrections",
        "",
        "KEEP:",
        "- `GEN-001` visibly lands on both `UAT-1A` and `UAT-1B` through solid feeders with black terminations.",
        "- `SAT-1A/B`, `UAT-1A/B`, `DG-1A/B`, bus ties, and transformer feeder chains are visually supported.",
        "- Dotted PT/AM/VM/CT instrument taps are retained as direct bus-to-instrument edges.",
        "- 480 V feeder chains are retained where the solid/dashed/dotted line style visibly enters and leaves each symbol.",
        "",
        "REMOVE:",
        "- `PNL-DCS -> ANN-ESF-A/B` remain excluded; the nearby dashed routing does not show a clean landed junction.",
        "- Long control-wireway continuations from UV/RPS relays remain excluded where their final labelled endpoint is not visible.",
        "",
        "ADD:",
        "- `PNL-ANN -> ANN-ESF-A` and `PNL-ANN -> ANN-ESF-B`; the singular `PNL-ANN` panel has a dashed horizontal run visibly landing at both annunciator boxes.",
        "",
        "RENAME / TYPE CHANGE:",
        "- `PNL-ANN-A` and `PNL-ANN-B` are collapsed to one node, `PNL-ANN`.",
        "- `CIP-AIR-1A/B` are renamed to `CMP-AIR-1A/B`; magnified label crops show `CMP-AIR`.",
        "- Line types are normalized to `P` for solid power, `GND` for solid ground branches, `CTRL` for dashed control/trip, and `INST` for dotted instrument.",
        "",
        "## Final Counts",
        "",
        f"- Nodes: {validation['nodes']}",
        f"- Undirected edges: {validation['edges']}",
        f"- Matrix ones: {validation['expected_matrix_ones']}",
        f"- Duplicate undirected edges: {validation['has_duplicate_undirected_edges']}",
        f"- Self-loops: {validation['self_loops']}",
        "",
        "## Remaining Uncertain Edges",
        "",
        "These are excluded from the accepted matrix.",
        "",
        "```csv",
        "source,target,type,reason",
    ]
    lines.extend(",".join(row) for row in UNCERTAIN)
    lines.extend(["```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds = {
        "round01_diego": make_edges(air_prefix="CIP", ann_split=True),
        "round01_jennifer": make_edges(air_prefix="CMP", ann_split=False),
        "round02_diego": make_edges(air_prefix="CMP", ann_split=False),
        "round02_jennifer": make_edges(air_prefix="CMP", ann_split=False),
    }
    final_edges = rounds["round02_jennifer"]
    for name, edges in rounds.items():
        write_sparse(RESULTS / f"{name}_sparse_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", edges)
    write_sparse(RESULTS / "final_sparse_edges.csv", final_edges)
    nodes, ones = write_matrix(RESULTS / "final_connectivity_matrix.csv", final_edges)
    final_validation = validate(final_edges)
    if nodes != final_validation["nodes"] or ones != final_validation["expected_matrix_ones"]:
        raise RuntimeError("matrix validation mismatch")
    if final_validation["has_duplicate_undirected_edges"] or final_validation["self_loops"]:
        raise RuntimeError(f"unexpected validation issue: {final_validation}")
    write_uncertain(RESULTS / "uncertain_excluded_edges.csv")
    write_report(RESULTS / "connectivity_extraction_report.md", final_edges, final_validation)
    write_token_estimate(RESULTS / "token_usage_estimate.md")
    print(f"final nodes: {final_validation['nodes']}")
    print(f"final undirected edges: {final_validation['edges']}")
    print(f"matrix ones: {final_validation['expected_matrix_ones']}")
    print(f"results: {RESULTS}")


if __name__ == "__main__":
    main()
