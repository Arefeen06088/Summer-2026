import csv
import json
import math
from pathlib import Path

from PIL import Image


DOC = "17"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires")
CROPS = Path(r"C:\Asif_all_python_projects\INL\INL\doc17_work\crops")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc17_work\results")

RAW = BASE / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def add_unique(items, value):
    if value not in items:
        items.append(value)


def norm_edge(a, b):
    return tuple(sorted((a, b)))


def add_edge(edges, a, b, evidence):
    edges[norm_edge(a, b)] = evidence


def source_nodes():
    nodes = [
        "GEN-001",
        "SAT-1A", "CB-SAT-1A", "UAT-1A", "CB-UAT-1A", "DG-1A", "CB-DG-1A",
        "SAT-1B", "CB-SAT-1B", "UAT-1B", "CB-UAT-1B", "DG-1B", "CB-DG-1B",
        "BUS-4160-A", "BUS-4160-B", "CB-TIE-4AB", "PT-4160-A", "PT-4160-B",
        "CB-TR-A1", "TR-LC-A1", "CB-480-A1",
        "CB-TR-A2", "TR-LC-A2", "CB-480-A2",
        "CB-TR-B1", "TR-LC-B1", "CB-480-B1",
        "CB-TR-B2", "TR-LC-B2", "CB-480-B2",
        "BUS-480-A", "BUS-480-B", "CB-TIE-480AB",
        "AM-480-A", "VM-480-A", "CT-480-A1",
        "AM-480-B", "VM-480-B", "CT-480-B1",
        "GND-SMGR-A", "GND-SMGR-B",
    ]
    return nodes


def feeder_defs(train):
    if train == "A":
        return [
            ("BUS-480-A", "CB-101A", "DS-101A", "MS-101A", "PUMP-SLC-1A", "TB-SLC-1A", "solid_tail"),
            ("BUS-480-A", "CB-102A", "FU-102A", "MS-102A", "PUMP-CV-1A", "GND-CCW-1A", "solid_tail"),
            ("BUS-480-A", "CB-103A", "DS-103A", "MS-103A", "PUMP-RHR-1A", "LS-RHR-1A", "uncertain_tail"),
            ("BUS-480-A", "CB-104A", "FU-104A", "MS-104A", "PUMP-CS-1A", "TB-CS-1A", "solid_tail"),
            ("BUS-480-A", "CB-105A", "DS-105A", "MS-105A", "FAN-CRDR-1A", "GND-FAN-1A", "solid_tail"),
            ("BUS-480-A", "CB-106A", "FU-106A", "RELAY-K106A", "HOV-RHVC-101A", "LS-RHVC-101A", "uncertain_tail"),
            ("BUS-480-A", "CB-107A", "DS-107A", "RELAY-K107A", "HOV-RHR-102A", "LS-RHR-102A", "uncertain_tail"),
            ("BUS-480-A", "CB-108A", "FU-108A", "MS-108A", "HTR-RPR-1A", "TB-HTR-1A", "solid_tail"),
            ("BUS-480-A", "CB-109A", "DS-109A", "MS-109A", "PUMP-SW-1A", "GND-SW-1A", "solid_tail"),
            ("BUS-480-A", "CB-110A", "FU-110A", "MS-110A", "HTR-AHU-1A", "GND-AHU-1A", "solid_tail"),
            ("BUS-480-A", "CB-111A", "DS-111A", "MS-111A", "CMP-AIR-1A", "TB-AIR-1A", "solid_tail"),
            ("BUS-480-A", "CB-112A", "FU-112A", "RELAY-K112A", "INST-RAD-1A", "JB-RAD-1A", "instrument_tail"),
        ]
    return [
        ("BUS-480-B", "CB-201B", "DS-201B", "MS-201B", "PUMP-SLC-1B", "TB-SLC-1B", "solid_tail"),
        ("BUS-480-B", "CB-202B", "FU-202B", "MS-202B", "PUMP-CV-1B", "GND-CCW-1B", "solid_tail"),
        ("BUS-480-B", "CB-203B", "DS-203B", "MS-203B", "PUMP-RHR-1B", "LS-RHR-1B", "uncertain_tail"),
        ("BUS-480-B", "CB-204B", "FU-204B", "MS-204B", "PUMP-CS-1B", "TB-CS-1B", "solid_tail"),
        ("BUS-480-B", "CB-205B", "DS-205B", "MS-205B", "FAN-CRDR-1B", "GND-FAN-1B", "solid_tail"),
        ("BUS-480-B", "CB-206B", "FU-206B", "RELAY-K206B", "HOV-RHVC-101B", "LS-RHVC-101B", "uncertain_tail"),
        ("BUS-480-B", "CB-207B", "DS-207B", "RELAY-K207B", "HOV-RHR-102B", "LS-RHR-102B", "uncertain_tail"),
        ("BUS-480-B", "CB-208B", "FU-208B", "MS-208B", "HTR-RPR-1B", "TB-HTR-1B", "solid_tail"),
        ("BUS-480-B", "CB-209B", "DS-209B", "MS-209B", "PUMP-SW-1B", "GND-SW-1B", "solid_tail"),
        ("BUS-480-B", "CB-210B", "FU-210B", "MS-210B", "HTR-AHU-1B", "GND-AHU-1B", "solid_tail"),
        ("BUS-480-B", "CB-211B", "DS-211B", "MS-211B", "CMP-AIR-1B", "TB-AIR-1B", "solid_tail"),
        ("BUS-480-B", "CB-212B", "FU-212B", "RELAY-K212B", "INST-RAD-1B", "JB-RAD-1B", "instrument_tail"),
    ]


def control_nodes():
    return [
        "CB-DC-A", "CHGR-125-A", "BAT-125-A", "BUS-125DC-A", "GND-DC-A", "INV-120-A", "BUS-120AC-A", "STS-120-A",
        "CB-DC-B", "CHGR-125-B", "BAT-125-B", "BUS-125DC-B", "GND-DC-B", "INV-120-B", "BUS-120AC-B", "STS-120-B",
        "CB-DCTIE-AB",
        "TB-RPS-A", "PNL-RPS-A", "RELAY-UV-A1", "RELAY-UV-A2",
        "TB-ESF-A", "PNL-ESF-A", "RELAY-RPS-A", "RELAY-ESF-A",
        "TB-RPS-B", "PNL-RPS-B", "RELAY-UV-B1", "RELAY-UV-B2",
        "TB-ESF-B", "PNL-ESF-B", "RELAY-RPS-B", "RELAY-ESF-B",
        "PNL-DCS", "PNL-ANN", "REC-SOE-1", "REC-SOE-2", "ANN-ESF-A", "ANN-ESF-B",
        "MTB-21", "MTB-22", "MTB-23", "MTB-24", "MTB-25", "MTB-26", "MTB-27", "MTB-28", "MTB-29",
    ]


def build_nodes():
    nodes = []
    for n in source_nodes():
        add_unique(nodes, n)
    for train in ("A", "B"):
        for row in feeder_defs(train):
            for n in row[:-1]:
                add_unique(nodes, n)
    for n in control_nodes():
        add_unique(nodes, n)
    return nodes


def source_edges(policy):
    edges = {}
    for a, b in [
        ("GEN-001", "UAT-1A"),
        ("GEN-001", "UAT-1B"),
        ("SAT-1A", "CB-SAT-1A"),
        ("CB-SAT-1A", "BUS-4160-A"),
        ("UAT-1A", "CB-UAT-1A"),
        ("CB-UAT-1A", "BUS-4160-A"),
        ("DG-1A", "CB-DG-1A"),
        ("CB-DG-1A", "BUS-4160-A"),
        ("SAT-1B", "CB-SAT-1B"),
        ("CB-SAT-1B", "BUS-4160-B"),
        ("UAT-1B", "CB-UAT-1B"),
        ("CB-UAT-1B", "BUS-4160-B"),
        ("DG-1B", "CB-DG-1B"),
        ("CB-DG-1B", "BUS-4160-B"),
        ("BUS-4160-A", "CB-TIE-4AB"),
        ("CB-TIE-4AB", "BUS-4160-B"),
        ("BUS-4160-A", "CB-TR-A1"),
        ("CB-TR-A1", "TR-LC-A1"),
        ("TR-LC-A1", "CB-480-A1"),
        ("CB-480-A1", "BUS-480-A"),
        ("BUS-4160-A", "CB-TR-A2"),
        ("CB-TR-A2", "TR-LC-A2"),
        ("TR-LC-A2", "CB-480-A2"),
        ("CB-480-A2", "BUS-480-A"),
        ("BUS-4160-B", "CB-TR-B1"),
        ("CB-TR-B1", "TR-LC-B1"),
        ("TR-LC-B1", "CB-480-B1"),
        ("CB-480-B1", "BUS-480-B"),
        ("BUS-4160-B", "CB-TR-B2"),
        ("CB-TR-B2", "TR-LC-B2"),
        ("TR-LC-B2", "CB-480-B2"),
        ("CB-480-B2", "BUS-480-B"),
        ("BUS-480-A", "CB-TIE-480AB"),
        ("CB-TIE-480AB", "BUS-480-B"),
        ("BUS-480-A", "GND-SMGR-A"),
        ("BUS-480-B", "GND-SMGR-B"),
    ]:
        add_edge(edges, a, b, "solid source/bus/feed path")
    if policy != "diego_r1":
        for a, b in [
            ("BUS-4160-A", "PT-4160-A"),
            ("BUS-4160-B", "PT-4160-B"),
            ("BUS-480-A", "AM-480-A"),
            ("BUS-480-A", "VM-480-A"),
            ("BUS-480-A", "CT-480-A1"),
            ("BUS-480-B", "AM-480-B"),
            ("BUS-480-B", "VM-480-B"),
            ("BUS-480-B", "CT-480-B1"),
        ]:
            add_edge(edges, a, b, "clean one-hop instrument tap")
    return edges


def feeder_edges(policy):
    edges = {}
    include_uncertain_tails = policy == "diego_r1"
    for train in ("A", "B"):
        for bus, cb, device, starter, load, tail, kind in feeder_defs(train):
            add_edge(edges, bus, cb, "480 V load-center bus feeder drop")
            add_edge(edges, cb, device, "branch breaker to fuse/disconnect")
            add_edge(edges, device, starter, "fuse/disconnect to starter/relay")
            add_edge(edges, starter, load, "starter/relay to load symbol")
            if kind in ("solid_tail", "instrument_tail") or include_uncertain_tails:
                add_edge(edges, load, tail, "visible one-hop load tail")
    return edges


def dc_edges():
    edges = {}
    for train in ("A", "B"):
        add_edge(edges, f"BUS-480-{train}", f"CB-DC-{train}", "480 V feed to DC charger breaker")
        add_edge(edges, f"CB-DC-{train}", f"CHGR-125-{train}", "breaker to battery charger")
        add_edge(edges, f"CHGR-125-{train}", f"BAT-125-{train}", "charger/battery link")
        add_edge(edges, f"BAT-125-{train}", f"BUS-125DC-{train}", "battery to 125 VDC bus")
        add_edge(edges, f"BUS-125DC-{train}", f"GND-DC-{train}", "125 VDC bus ground")
        add_edge(edges, f"BUS-125DC-{train}", f"INV-120-{train}", "125 VDC bus to inverter")
        add_edge(edges, f"INV-120-{train}", f"BUS-120AC-{train}", "inverter output to 120 VAC bus")
        add_edge(edges, f"BUS-120AC-{train}", f"STS-120-{train}", "120 VAC bus to static transfer switch")
    add_edge(edges, "BUS-125DC-A", "CB-DCTIE-AB", "125 VDC bus tie breaker")
    add_edge(edges, "CB-DCTIE-AB", "BUS-125DC-B", "125 VDC bus tie breaker")
    return edges


def local_control_edges(policy):
    edges = {}
    if policy in ("jennifer_r1", "diego_r2", "final"):
        for a, b in [
            ("STS-120-A", "PNL-RPS-A"),
            ("TB-RPS-A", "PNL-RPS-A"),
            ("PNL-RPS-A", "RELAY-UV-A1"),
            ("PNL-RPS-A", "RELAY-UV-A2"),
            ("PNL-ESF-A", "TB-ESF-A"),
            ("PNL-ESF-A", "RELAY-RPS-A"),
            ("PNL-ESF-A", "RELAY-ESF-A"),
            ("STS-120-B", "PNL-RPS-B"),
            ("TB-RPS-B", "PNL-RPS-B"),
            ("PNL-RPS-B", "RELAY-UV-B1"),
            ("PNL-RPS-B", "RELAY-UV-B2"),
            ("PNL-ESF-B", "TB-ESF-B"),
            ("PNL-ESF-B", "RELAY-RPS-B"),
            ("PNL-ESF-B", "RELAY-ESF-B"),
            ("PNL-DCS", "REC-SOE-1"),
        ]:
            add_edge(edges, a, b, "clean local lower dashed/control endpoint")
    if policy == "diego_r1":
        for a, b in [
            ("STS-120-A", "PNL-RPS-A"),
            ("TB-RPS-A", "PNL-RPS-A"),
            ("PNL-RPS-A", "RELAY-UV-A1"),
            ("PNL-RPS-A", "RELAY-UV-A2"),
            ("PNL-ESF-A", "TB-ESF-A"),
            ("PNL-ESF-A", "RELAY-RPS-A"),
            ("PNL-ESF-A", "RELAY-ESF-A"),
            ("STS-120-B", "PNL-RPS-B"),
            ("TB-RPS-B", "PNL-RPS-B"),
            ("PNL-RPS-B", "RELAY-UV-B1"),
            ("PNL-RPS-B", "RELAY-UV-B2"),
            ("PNL-ESF-B", "TB-ESF-B"),
            ("PNL-ESF-B", "RELAY-RPS-B"),
            ("PNL-ESF-B", "RELAY-ESF-B"),
            ("PNL-DCS", "REC-SOE-1"),
            ("PNL-ANN", "REC-SOE-2"),
            ("PNL-ANN", "ANN-ESF-A"),
            ("PNL-ANN", "ANN-ESF-B"),
        ]:
            add_edge(edges, a, b, "high-recall dashed/control endpoint")
    return edges


def build_edges(policy):
    edges = {}
    for group in [source_edges(policy), feeder_edges(policy), dc_edges(), local_control_edges(policy)]:
        edges.update(group)
    return edges


def uncertain_edges(policy):
    rows = []
    def u(a, b, reason):
        rows.append((a, b, reason))

    if policy == "diego_r1":
        for a, b in [
            ("BUS-4160-A", "PT-4160-A"),
            ("BUS-4160-B", "PT-4160-B"),
            ("BUS-480-A", "AM-480-A"),
            ("BUS-480-A", "VM-480-A"),
            ("BUS-480-A", "CT-480-A1"),
            ("BUS-480-B", "AM-480-B"),
            ("BUS-480-B", "VM-480-B"),
            ("BUS-480-B", "CT-480-B1"),
        ]:
            u(a, b, "Diego R1 marked instrument taps uncertain")

    for train in ("A", "B"):
        for _bus, _cb, _dev, _starter, load, tail, kind in feeder_defs(train):
            if kind == "uncertain_tail":
                u(load, tail, "dashed LS/control tail not accepted as hard in precision pass")

    for a, b, reason in [
        ("CB-TR-A2", "MTB-21", "top master-terminal dashed lane exists but exact terminal endpoint is unclear"),
        ("CB-TR-A2", "MTB-29", "top master-terminal dashed lane exists but exact terminal endpoint is unclear"),
        ("CB-TR-A1", "MTB-21", "possible transformer breaker control lane, route-shared"),
        ("CB-TR-B1", "MTB-29", "possible transformer breaker control lane, route-shared"),
        ("CB-TR-B2", "MTB-29", "possible transformer breaker control lane, route-shared"),
        ("PNL-ANN", "REC-SOE-2", "lower annunciation/SOE shared trunk, not clean pairwise"),
        ("PNL-ANN", "ANN-ESF-A", "lower annunciation shared trunk, not clean pairwise"),
        ("PNL-ANN", "ANN-ESF-B", "lower annunciation shared trunk, not clean pairwise"),
        ("REC-SOE-2", "ANN-ESF-B", "shared SOE/annunciation trunk, not clean pairwise"),
        ("PNL-DCS", "PNL-ANN", "shared lower trunk crossing/route, not clean pairwise"),
    ]:
        u(a, b, reason)

    return rows


ROUNDS = [
    ("round_01_diego_high_recall", "diego_r1", "Diego R1: broad hard graph, uncertain instrument taps and route-shared lower/control lanes."),
    ("round_01_jennifer_precision", "jennifer_r1", "Jennifer R1: instrument taps and clean local RPS/ESF edges hard; top MTB and shared SOE/annunciation trunks uncertain."),
    ("round_02_diego_saturation", "diego_r2", "Diego R2: narrow review of top MTB lane and lower SOE trunk."),
    ("round_02_jennifer_final", "final", "Jennifer final: no extra hard pairwise edges from shared MTB/SOE trunks; keep local PNL-DCS--REC-SOE-1 only."),
]


def matrix_for(nodes, edges):
    idx = {n: i for i, n in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    missing = []
    for a, b in edges:
        if a not in idx or b not in idx:
            missing.append((a, b))
            continue
        i, j = idx[a], idx[b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    return matrix, missing


def write_matrix(path, nodes, matrix):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_sparse(path, nodes, matrix):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "connected"])
        for i, a in enumerate(nodes):
            for j, b in enumerate(nodes):
                writer.writerow([a, b, matrix[i][j]])


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for (a, b), ev in sorted(edges.items()):
            writer.writerow([a, b, ev])


def write_nodes(path, nodes):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"])
        for node in nodes:
            writer.writerow([node])


def write_uncertain(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(rows)


def qa(nodes, edges, matrix, missing):
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    degree = {n: 0 for n in nodes}
    for a, b in edges:
        if a in degree:
            degree[a] += 1
        if b in degree:
            degree[b] += 1
    return {
        "node_count": len(nodes),
        "hard_edge_count": len(edges),
        "missing_edge_endpoints": missing,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "isolated_hard_only_nodes": [n for n, d in degree.items() if d == 0],
    }


def image_tokens(path):
    with Image.open(path) as im:
        w, h = im.size
    return math.ceil(w / 32) * math.ceil(h / 32)


def token_estimates():
    image_sets = {
        "main_01_visual_orchestration_and_artifacts": [
            CROPS / "raw_full_preview.png",
            CROPS / "overlay_full_preview.png",
            CROPS / "raw_top_band.png",
            CROPS / "raw_upper_middle_band.png",
            CROPS / "raw_bottom_band.png",
            CROPS / "close_a_feeders_left.png",
            CROPS / "close_b_feeders_left.png",
            CROPS / "raw_close_master_lane.png",
            CROPS / "raw_close_lower_soe_a.png",
            CROPS / "raw_close_lower_soe_b.png",
        ],
        "diego_01_high_recall": [
            CROPS / "raw_full_preview.png",
            CROPS / "overlay_full_preview.png",
            CROPS / "raw_top_band.png",
            CROPS / "raw_middle_band.png",
            CROPS / "raw_bottom_band.png",
        ],
        "jennifer_01_precision": [
            CROPS / "raw_full_preview.png",
            CROPS / "overlay_full_preview.png",
            CROPS / "raw_top_band.png",
            CROPS / "raw_upper_middle_band.png",
            CROPS / "raw_bottom_band.png",
        ],
        "diego_02_saturation": [
            CROPS / "raw_close_master_lane.png",
            CROPS / "overlay_close_master_lane.png",
            CROPS / "raw_close_lower_soe_a.png",
            CROPS / "overlay_close_lower_soe_a.png",
            CROPS / "raw_close_lower_soe_b.png",
            CROPS / "overlay_close_lower_soe_b.png",
            CROPS / "raw_close_ann_dcs_center.png",
            CROPS / "overlay_close_ann_dcs_center.png",
        ],
        "jennifer_02_final": [
            CROPS / "raw_close_master_lane.png",
            CROPS / "overlay_close_master_lane.png",
            CROPS / "raw_close_lower_soe_a.png",
            CROPS / "overlay_close_lower_soe_a.png",
            CROPS / "raw_close_lower_soe_b.png",
            CROPS / "overlay_close_lower_soe_b.png",
            CROPS / "raw_close_ann_dcs_center.png",
            CROPS / "overlay_close_ann_dcs_center.png",
        ],
    }
    rows = []
    specs = [
        ("main_01_visual_orchestration_and_artifacts", "main", "orchestration", "gpt-5", 1400, 4200, (2500, 5200, 9000), 0, "local visual inspection, crop/result scripts"),
        ("diego_01_high_recall", "Diego", "round_01", "gpt-5.5 xhigh", 2600, 3100, (4500, 9000, 16200), 0, "subagent usage object unavailable; high-recall response observed"),
        ("jennifer_01_precision", "Jennifer", "round_01", "gpt-5.5 xhigh", 3600, 3200, (4500, 9000, 16200), 0, "subagent usage object unavailable; precision response observed"),
        ("diego_02_saturation", "Diego", "round_02", "gpt-5.5 xhigh", 2100, 900, (1500, 3000, 5600), 0, "narrow follow-up with extra crops"),
        ("jennifer_02_final", "Jennifer", "round_02", "gpt-5.5 xhigh", 1200, 500, (800, 1600, 3000), 0, "final accept/refine response observed; usage object unavailable"),
    ]
    cached = {
        "diego_02_saturation": sum(image_tokens(p) for p in image_sets["diego_01_high_recall"] if p.exists()),
        "jennifer_02_final": sum(image_tokens(p) for p in image_sets["jennifer_01_precision"] if p.exists()),
    }
    for call_id, actor, round_name, model, text_in, out_tokens, reason, cache_text, note in specs:
        image_in = sum(image_tokens(p) for p in image_sets[call_id] if p.exists())
        cached_in = cached.get(call_id, cache_text)
        low = text_in + image_in + out_tokens + reason[0]
        expected = text_in + image_in + out_tokens + reason[1]
        high = text_in + image_in + out_tokens + reason[2]
        rows.append({
            "document": DOC,
            "iteration": ITERATION,
            "call_id": call_id,
            "actor": actor,
            "round": round_name,
            "model": model,
            "input_tokens_est": text_in,
            "cached_input_tokens_est": cached_in,
            "output_tokens_est": out_tokens,
            "reasoning_tokens_available": "no",
            "reasoning_tokens_low_est": reason[0],
            "reasoning_tokens_expected_est": reason[1],
            "reasoning_tokens_high_est": reason[2],
            "image_file_input_tokens_est": image_in,
            "total_tokens_low_est": low,
            "total_tokens_expected_est": expected,
            "total_tokens_high_est": high,
            "usage_object_available": "no",
            "notes": note,
        })
    return rows


def write_token_usage(rows):
    fields = [
        "document", "iteration", "call_id", "actor", "round", "model",
        "input_tokens_est", "cached_input_tokens_est", "output_tokens_est",
        "reasoning_tokens_available", "reasoning_tokens_low_est",
        "reasoning_tokens_expected_est", "reasoning_tokens_high_est",
        "image_file_input_tokens_est", "total_tokens_low_est",
        "total_tokens_expected_est", "total_tokens_high_est",
        "usage_object_available", "notes",
    ]
    with (OUT / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    low = sum(r["total_tokens_low_est"] for r in rows)
    expected = sum(r["total_tokens_expected_est"] for r in rows)
    high = sum(r["total_tokens_high_est"] for r in rows)
    image_total = sum(r["image_file_input_tokens_est"] for r in rows)
    cached = sum(r["cached_input_tokens_est"] for r in rows)
    with (OUT / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write(f"# Token Usage Estimate - Document {DOC}, Iteration {ITERATION}\n\n")
        f.write("OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.\n\n")
        f.write("Local estimate method: coarse text estimates plus image tokens as ceil(width / 32) * ceil(height / 32); reasoning tokens are low/expected/high estimates.\n\n")
        f.write("| document | iteration | low | expected | high | image/file input | cached input |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        f.write(f"| {DOC} | {ITERATION} | {low} | {expected} | {high} | {image_total} | {cached} |\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = build_nodes()
    qas = {}
    final_summary = {}
    for round_name, policy, note in ROUNDS:
        edges = build_edges(policy)
        matrix, missing = matrix_for(nodes, edges)
        write_matrix(OUT / f"connectivity_matrix_{round_name}.csv", nodes, matrix)
        write_sparse(OUT / f"connectivity_sparse_{round_name}.csv", nodes, matrix)
        write_edges(OUT / f"edges_{round_name}.csv", edges)
        write_nodes(OUT / f"nodes_{round_name}.csv", nodes)
        write_uncertain(OUT / f"uncertain_edges_{round_name}.csv", uncertain_edges(policy))
        qas[round_name] = qa(nodes, edges, matrix, missing)
        qas[round_name]["uncertain_edge_count"] = len(uncertain_edges(policy))
        qas[round_name]["note"] = note
        if policy == "final":
            write_matrix(OUT / "connectivity_matrix_final.csv", nodes, matrix)
            write_sparse(OUT / "connectivity_sparse_final.csv", nodes, matrix)
            write_edges(OUT / "edges_final.csv", edges)
            write_nodes(OUT / "nodes_final.csv", nodes)
            write_uncertain(OUT / "uncertain_edges_final.csv", uncertain_edges(policy))
            final_summary = {
                "node_count": len(nodes),
                "hard_edge_count": len(edges),
                "uncertain_edge_count": len(uncertain_edges(policy)),
            }
    final_edges = build_edges("final")
    final_matrix, final_missing = matrix_for(nodes, final_edges)
    qa_final = qa(nodes, final_edges, final_matrix, final_missing)
    qa_final["uncertain_edge_count"] = len(uncertain_edges("final"))
    qa_final["rounds"] = qas
    qa_final["raw_resource"] = str(RAW)
    qa_final["overlay_resource"] = str(OVERLAY)
    qa_final["mask_resource"] = str(MASK)
    qa_final["notes"] = [
        "Final matrix includes hard visual connections only.",
        "Instrument taps and clean local lower RPS/ESF endpoints are hard.",
        "Top master-terminal lane and lower shared SOE/annunciation trunks remain uncertain after Diego R2/Jennifer final saturation.",
        "GND-CCW labels are used for CV pump grounds per precision review.",
    ]
    (OUT / "qa_final.json").write_text(json.dumps(qa_final, indent=2), encoding="utf-8")

    with (OUT / "round_notes.md").open("w", encoding="utf-8") as f:
        f.write(f"# Document {DOC} Round Notes\n\n")
        for round_name, _policy, note in ROUNDS:
            f.write(f"## {round_name}\n\n{note}\n\n")
        f.write("## Saturation Decision\n\n")
        f.write("Final hard graph uses Jennifer's precision policy. Diego R2 and Jennifer final agreed that no additional shared SOE/MTB trunk edge should be hardened; those dashed shared trunks remain uncertain.\n")

    token_rows = token_estimates()
    write_token_usage(token_rows)
    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "final_node_count": final_summary["node_count"],
        "final_hard_edge_count": final_summary["hard_edge_count"],
        "final_uncertain_edge_count": final_summary["uncertain_edge_count"],
        "round_hard_edge_counts": {r: q["hard_edge_count"] for r, q in qas.items()},
        "round_uncertain_edge_counts": {r: q["uncertain_edge_count"] for r, q in qas.items()},
        "files_written": sorted(p.name for p in OUT.iterdir() if p.is_file()),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
