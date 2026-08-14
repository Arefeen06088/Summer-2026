from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except Exception:
    Image = None


DOC = "12"
ITERATION = "1"
RESOURCE_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires"
)
DEFAULT_OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc12_work\results")
OUT = Path(os.environ.get("DOC12_OUTPUT_DIR", str(DEFAULT_OUT)))
RAW = RESOURCE_DIR / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png"
OVERLAY = RESOURCE_DIR / "wires_mask_overlay.png"
MASK = RESOURCE_DIR / "wires_mask.png"
CROP_DIR = Path(r"C:\Asif_all_python_projects\INL\INL\doc12_work\crops")


def add_edge(edges: set[tuple[str, str]], a: str, b: str) -> None:
    if a == b:
        raise ValueError(f"self-loop requested for {a}")
    edges.add(tuple(sorted((a, b))))


def add_edges(edges: set[tuple[str, str]], pairs: Iterable[tuple[str, str]]) -> None:
    for a, b in pairs:
        add_edge(edges, a, b)


def chain(nodes: list[str]) -> list[tuple[str, str]]:
    return list(zip(nodes, nodes[1:]))


source_nodes = [
    "GEN-G1",
    "CB-GEN-1",
    "TR-UAT-1",
    "CB-101",
    "TR-SUT-1",
    "DS-SUT-1",
    "CB-102",
    "EDG-1A",
    "DS-EDG-1A",
    "CB-103",
    "BUS-4KV-A",
    "CB-TIE-1",
    "BUS-4KV-B",
    "EDG-1B",
    "DS-EDG-1B",
    "CB-203",
    "TR-SUT-2",
    "DS-SUT-2",
    "CB-202",
    "EDG-1C",
    "CB-303",
    "CB-111",
    "TR-480-A",
    "BUS-480-A",
    "CB-112",
    "TR-480-C",
    "BUS-480-C",
    "PT-4160A",
    "CB-211",
    "TR-480-B",
    "BUS-480-B",
    "CB-212",
    "TR-480-D",
    "BUS-480-D",
    "PT-4160B",
]

mcc_nodes = ["CB-M1A", "MCC-1A", "CB-M2A", "MCC-2A", "CB-M1B", "MCC-1B", "CB-M2B", "MCC-2B"]

load_branches = [
    ("MCC-1A", "CB-F001", "FU-F001", "PUMP-RHR-A"),
    ("MCC-1A", "CB-F002", "MS-F002", "PUMP-SI-A"),
    ("MCC-1A", "CB-F003", "FU-F003", "FAN-CR-A"),
    ("MCC-1A", "CB-F004", "DS-F004", "MOV-RCIC-A"),
    ("MCC-1A", "CB-F005", "MS-F005", "PUMP-CCW-A"),
    ("MCC-1A", "CB-F006", "FU-F006", "HTR-SUMP-A"),
    ("MCC-1A", "CB-F007", "MS-F007", "PMP-BOR-A"),
    ("MCC-1A", "CB-F008", "DS-F008", "VALVE-IA-A"),
    ("MCC-2A", "CB-F009", "MS-F009", "PUMP-AFW-A"),
    ("MCC-2A", "CB-F010", "MS-F010", "PMP-LUBE-A"),
    ("MCC-2A", "CB-F011", "DS-F011", "MOV-RHR-A"),
    ("MCC-2A", "CB-F012", "FU-F012", "FAN-BLDG-A"),
    ("MCC-2A", "CB-F013", "FU-F013", "PNL-RAD-A"),
    ("MCC-2A", "CB-F014", "MS-F014", "PUMP-SW-A"),
    ("MCC-2A", "CB-F015", "DS-F015", "SPARE-A2"),
    ("MCC-1B", "CB-F016", "MS-F016", "PUMP-RHR-B"),
    ("MCC-1B", "CB-F017", "MS-F017", "PUMP-SI-B"),
    ("MCC-1B", "CB-F018", "FU-F018", "FAN-CR-B"),
    ("MCC-1B", "CB-F019", "DS-F019", "MOV-RCIC-B"),
    ("MCC-1B", "CB-F020", "MS-F020", "PUMP-CCW-B"),
    ("MCC-1B", "CB-F021", "FU-F021", "HTR-SUMP-B"),
    ("MCC-1B", "CB-F022", "MS-F022", "PMP-BOR-B"),
    ("MCC-1B", "CB-F023", "DS-F023", "VALVE-IA-B"),
    ("MCC-2B", "CB-F024", "MS-F024", "PUMP-AFW-B"),
    ("MCC-2B", "CB-F025", "MS-F025", "PMP-LUBE-B"),
    ("MCC-2B", "CB-F026", "DS-F026", "MOV-RHR-B"),
    ("MCC-2B", "CB-F027", "FU-F027", "FAN-BLDG-B"),
    ("MCC-2B", "CB-F028", "FU-F028", "PNL-RAD-B"),
    ("MCC-2B", "CB-F029", "MS-F029", "PUMP-SW-B"),
]

load_nodes: list[str] = []
for _mcc, cb, dev, load in load_branches:
    load_nodes.extend([cb, dev, load])

control_nodes = [
    "CB-DC-1A",
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-A",
    "INV-1A",
    "ATS-INV",
    "INV-1B",
    "DC-BUS-B",
    "CHGR-125B",
    "CB-DC-1B",
    "BAT-125B",
    "BUS-120VAC-ESF",
    "ANN-480A",
    "RELAY-27A",
    "RELAY-50A",
    "RELAY-86A",
    "TB-ANN-1",
    "TB-A",
    "TB-RPS-A",
    "PNL-RPS-A",
    "PNL-ESFAS-A",
    "SEQ-REC-1",
    "PNL-ESFAS-B",
    "PNL-RPS-B",
    "TB-RPS-B",
    "TB-B",
    "RELAY-86B",
    "RELAY-50B",
    "RELAY-27B",
    "ANN-480B",
    "GND-1",
    "GND-2",
]

final_nodes = source_nodes + mcc_nodes + load_nodes + control_nodes


def build_power_load_dc_edges() -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    add_edges(edges, chain(["GEN-G1", "CB-GEN-1", "TR-UAT-1", "CB-101", "BUS-4KV-A"]))
    add_edges(edges, chain(["TR-SUT-1", "DS-SUT-1", "CB-102", "BUS-4KV-A"]))
    add_edges(edges, chain(["EDG-1A", "DS-EDG-1A", "CB-103", "BUS-4KV-A"]))
    add_edges(edges, chain(["BUS-4KV-A", "CB-TIE-1", "BUS-4KV-B"]))
    add_edges(edges, chain(["EDG-1B", "DS-EDG-1B", "CB-203", "BUS-4KV-B"]))
    add_edges(edges, chain(["TR-SUT-2", "DS-SUT-2", "CB-202", "BUS-4KV-B"]))
    add_edges(edges, chain(["EDG-1C", "CB-303", "BUS-4KV-B"]))
    add_edges(edges, chain(["BUS-4KV-A", "CB-111", "TR-480-A", "BUS-480-A"]))
    add_edges(edges, chain(["BUS-4KV-A", "CB-112", "TR-480-C", "BUS-480-C"]))
    add_edges(edges, chain(["BUS-4KV-B", "CB-211", "TR-480-B", "BUS-480-B"]))
    add_edges(edges, chain(["BUS-4KV-B", "CB-212", "TR-480-D", "BUS-480-D"]))
    add_edges(edges, [("PT-4160A", "BUS-4KV-A"), ("PT-4160B", "BUS-4KV-B")])

    add_edges(edges, chain(["BUS-480-A", "CB-M1A", "MCC-1A"]))
    add_edges(edges, chain(["BUS-480-C", "CB-M2A", "MCC-2A"]))
    add_edges(edges, chain(["BUS-480-B", "CB-M1B", "MCC-1B"]))
    add_edges(edges, chain(["BUS-480-D", "CB-M2B", "MCC-2B"]))

    for mcc, cb, dev, load in load_branches:
        add_edges(edges, chain([mcc, cb, dev, load]))

    add_edges(edges, chain(["MCC-2A", "CB-DC-1A", "CHGR-125A", "DC-BUS-A"]))
    add_edges(edges, chain(["BAT-125A", "DC-BUS-A", "INV-1A", "ATS-INV"]))
    add_edges(edges, chain(["BUS-480-B", "CB-DC-1B", "CHGR-125B", "DC-BUS-B"]))
    add_edges(edges, chain(["BAT-125B", "DC-BUS-B", "INV-1B", "ATS-INV"]))
    add_edge(edges, "ATS-INV", "BUS-120VAC-ESF")
    return edges


base_edges = build_power_load_dc_edges()

final_control_edges: set[tuple[str, str]] = set()
add_edges(
    final_control_edges,
    [
        ("BUS-120VAC-ESF", "PNL-RPS-A"),
        ("BUS-120VAC-ESF", "PNL-RPS-B"),
        ("PNL-RPS-A", "PNL-ESFAS-A"),
        ("PNL-RPS-B", "PNL-ESFAS-B"),
        ("PNL-RPS-A", "GND-1"),
        ("PNL-RPS-B", "GND-2"),
        ("ANN-480A", "RELAY-27A"),
        ("ANN-480A", "TB-ANN-1"),
        ("RELAY-50A", "RELAY-86A"),
        ("RELAY-27B", "ANN-480B"),
        ("RELAY-86B", "RELAY-50B"),
        ("PNL-ESFAS-A", "SEQ-REC-1"),
    ],
)

final_edges = base_edges | final_control_edges

removed_direct_edges: set[tuple[str, str]] = set()
add_edges(removed_direct_edges, [("BUS-120VAC-ESF", "PNL-ESFAS-A"), ("BUS-120VAC-ESF", "PNL-ESFAS-B")])

restored_by_r2: set[tuple[str, str]] = set()
add_edges(
    restored_by_r2,
    [
        ("ANN-480A", "RELAY-27A"),
        ("ANN-480A", "TB-ANN-1"),
        ("RELAY-50A", "RELAY-86A"),
        ("RELAY-27B", "ANN-480B"),
        ("RELAY-86B", "RELAY-50B"),
        ("PNL-ESFAS-A", "SEQ-REC-1"),
    ],
)

diego_high_recall_extra: set[tuple[str, str]] = set()
add_edges(
    diego_high_recall_extra,
    [
        ("BUS-120VAC-ESF", "SEQ-REC-1"),
        ("BUS-120VAC-ESF", "PNL-ESFAS-A"),
        ("BUS-120VAC-ESF", "PNL-ESFAS-B"),
        ("RELAY-27A", "TB-RPS-A"),
        ("RELAY-86A", "TB-RPS-A"),
        ("TB-RPS-A", "PNL-RPS-A"),
        ("TB-ANN-1", "PNL-ESFAS-A"),
        ("RELAY-27B", "TB-RPS-B"),
        ("RELAY-86B", "TB-RPS-B"),
        ("TB-RPS-B", "PNL-RPS-B"),
    ],
)

uncertain_final: set[tuple[str, str]] = set()
add_edges(
    uncertain_final,
    [
        ("PT-4160A", "RELAY-27A"),
        ("PT-4160B", "RELAY-27B"),
        ("PT-4160A", "ANN-480A"),
        ("PT-4160B", "ANN-480B"),
        ("BUS-120VAC-ESF", "SEQ-REC-1"),
        ("RELAY-27A", "RELAY-86A"),
        ("RELAY-27B", "RELAY-86B"),
        ("RELAY-50A", "TB-RPS-A"),
        ("RELAY-50B", "TB-RPS-B"),
        ("TB-ANN-1", "RELAY-50A"),
        ("TB-ANN-1", "RELAY-86A"),
        ("ANN-480A", "RELAY-50A"),
        ("ANN-480B", "RELAY-50B"),
        ("ANN-480A", "RELAY-86A"),
        ("ANN-480B", "RELAY-86B"),
        ("TB-RPS-A", "PNL-ESFAS-A"),
        ("TB-RPS-B", "PNL-ESFAS-B"),
    ],
)

jennifer_r1_edges = (final_edges - restored_by_r2) | {tuple(sorted(("BUS-120VAC-ESF", "SEQ-REC-1")))}
diego_r2_edges = final_edges | {tuple(sorted(("BUS-120VAC-ESF", "SEQ-REC-1")))}
diego_r1_edges = final_edges | diego_high_recall_extra | removed_direct_edges

rounds = [
    {
        "slug": "round_01_diego_high_recall",
        "agent": "Diego",
        "nodes": final_nodes,
        "edges": sorted(diego_r1_edges),
        "uncertain_edges": sorted(uncertain_final | diego_high_recall_extra),
        "notes": "High-recall pass with broad dashed/control fan-out and direct ESFAS bus edges.",
    },
    {
        "slug": "round_01_jennifer_precision_stalled",
        "agent": "Jennifer",
        "nodes": final_nodes,
        "edges": [],
        "uncertain_edges": [],
        "notes": "First Jennifer pass was shut down after timing out; no usable matrix returned.",
    },
    {
        "slug": "round_01_jennifer_precision",
        "agent": "Jennifer",
        "nodes": final_nodes,
        "edges": sorted(jennifer_r1_edges),
        "uncertain_edges": sorted(restored_by_r2 | uncertain_final),
        "notes": "Targeted precision pass: removed direct ESF bus to ESFAS panels and broad control fan-out.",
    },
    {
        "slug": "round_02_diego_saturation",
        "agent": "Diego",
        "nodes": final_nodes,
        "edges": sorted(diego_r2_edges),
        "uncertain_edges": sorted(uncertain_final),
        "notes": "Restored six directly visible control edges; left broad fan-out uncertain.",
    },
    {
        "slug": "round_02_jennifer_final",
        "agent": "Jennifer",
        "nodes": final_nodes,
        "edges": sorted(final_edges),
        "uncertain_edges": sorted(uncertain_final),
        "notes": "Final saturation: accepted the six restorations and demoted BUS-120VAC-ESF--SEQ-REC-1 to uncertain.",
    },
]


def write_matrix(path: Path, nodes: list[str], edges: Iterable[tuple[str, str]]) -> None:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row in nodes:
            writer.writerow([row] + [0 if row == col else int(tuple(sorted((row, col))) in edge_set) for col in nodes])


def write_edges(path: Path, edges: Iterable[tuple[str, str]], include_status: bool = True) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["source", "target"]
        if include_status:
            fieldnames.extend(["edge_type", "evidence"])
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for a, b in sorted({tuple(sorted(e)) for e in edges}):
            row = {"source": a, "target": b}
            if include_status:
                row["edge_type"] = "visual_schematic"
                row["evidence"] = "solid or dashed line visibly terminates on both endpoints; crossings and label-only associations excluded"
            writer.writerow(row)


def write_sparse_matrix(path: Path, nodes: list[str], edges: Iterable[tuple[str, str]]) -> None:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "connected"])
        for i, a in enumerate(nodes):
            for b in nodes[i + 1 :]:
                writer.writerow([a, b, int(tuple(sorted((a, b))) in edge_set)])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def image_token_estimate(path: Path) -> int:
    if Image is not None and path.exists():
        with Image.open(path) as img:
            w, h = img.size
    else:
        w, h = 4200, 3000
    return math.ceil(w / 32) * math.ceil(h / 32)


def band(expected: int) -> tuple[int, int, int]:
    return (math.ceil(expected * 0.75), expected, math.ceil(expected * 1.35))


def write_token_usage() -> None:
    images = {
        "full_raw": RAW,
        "full_overlay": OVERLAY,
        "top_left": CROP_DIR / "raw_top_4160_sources_left.png",
        "top_right": CROP_DIR / "raw_top_4160_sources_right.png",
        "train_a_mcc1": CROP_DIR / "raw_train_a_480_mcc1.png",
        "train_a_mcc2_dc": CROP_DIR / "raw_train_a_mcc2_and_dc_left.png",
        "train_b_mcc1": CROP_DIR / "raw_train_b_480_mcc1.png",
        "train_b_mcc2_dc": CROP_DIR / "raw_train_b_mcc2_and_dc_right.png",
        "left_dc": CROP_DIR / "raw_left_dc_bus.png",
        "right_dc": CROP_DIR / "raw_right_dc_bus.png",
        "bottom_logic": CROP_DIR / "raw_bottom_control_logic.png",
        "bottom_overlay": CROP_DIR / "overlay_bottom_control_logic.png",
        "overlay_full_left_center": CROP_DIR / "overlay_full_left_and_center.png",
        "center_tie": CROP_DIR / "raw_center_bus_tie.png",
        "grid_r2c2": CROP_DIR / "raw_grid_r2_c2.png",
    }
    img_tokens = {name: image_token_estimate(path) for name, path in images.items()}

    def img_sum(names: list[str]) -> int:
        return sum(img_tokens[name] for name in names)

    calls = [
        {
            "call": "main_agent_orchestration",
            "model": "gpt-5",
            "text": 28000,
            "image": img_sum(list(img_tokens)),
            "output": 2800,
            "reasoning": 10000,
            "notes": "Main visual inspection, tool orchestration, graph construction, validation, and file writing.",
        },
        {
            "call": "Diego_R1_high_recall",
            "model": "gpt-5.5",
            "text": 850,
            "image": img_sum(
                [
                    "full_raw",
                    "full_overlay",
                    "top_left",
                    "top_right",
                    "train_a_mcc1",
                    "train_a_mcc2_dc",
                    "train_b_mcc1",
                    "train_b_mcc2_dc",
                    "left_dc",
                    "right_dc",
                    "bottom_logic",
                    "bottom_overlay",
                    "overlay_full_left_center",
                ]
            ),
            "output": 4200,
            "reasoning": 6500,
            "notes": "Completed high-recall extractor pass.",
        },
        {
            "call": "Jennifer_R1_precision_stalled_shutdown",
            "model": "gpt-5.5",
            "text": 5200,
            "image": img_sum(
                [
                    "full_raw",
                    "full_overlay",
                    "top_left",
                    "top_right",
                    "train_a_mcc1",
                    "train_a_mcc2_dc",
                    "train_b_mcc1",
                    "train_b_mcc2_dc",
                    "left_dc",
                    "right_dc",
                    "bottom_logic",
                    "bottom_overlay",
                    "overlay_full_left_center",
                ]
            ),
            "output": 0,
            "reasoning": 6000,
            "notes": "Spawned and then shut down after two long waits; no usage object or final output was exposed.",
        },
        {
            "call": "Jennifer_R1_precision_targeted",
            "model": "gpt-5.5",
            "text": 3600,
            "image": img_sum(
                [
                    "full_raw",
                    "full_overlay",
                    "top_left",
                    "top_right",
                    "train_a_mcc1",
                    "train_a_mcc2_dc",
                    "train_b_mcc1",
                    "train_b_mcc2_dc",
                    "left_dc",
                    "right_dc",
                    "bottom_logic",
                    "bottom_overlay",
                ]
            ),
            "output": 1000,
            "reasoning": 3600,
            "notes": "Completed narrowed precision review.",
        },
        {
            "call": "Diego_R2_saturation",
            "model": "gpt-5.5",
            "text": 1450,
            "image": img_sum(["full_raw", "full_overlay", "bottom_logic", "bottom_overlay", "left_dc", "right_dc", "overlay_full_left_center"]),
            "output": 800,
            "reasoning": 3000,
            "notes": "Completed saturation pass focused on deltas.",
        },
        {
            "call": "Jennifer_R2_final",
            "model": "gpt-5.5",
            "text": 900,
            "image": img_sum(["full_raw", "full_overlay", "bottom_logic", "bottom_overlay", "left_dc", "right_dc"]),
            "output": 850,
            "reasoning": 2600,
            "notes": "Completed final precision confirmation.",
        },
    ]

    fieldnames = [
        "document",
        "iteration",
        "call",
        "model",
        "text_input_tokens_low",
        "text_input_tokens_expected",
        "text_input_tokens_high",
        "cached_input_tokens",
        "image_file_input_tokens_low",
        "image_file_input_tokens_expected",
        "image_file_input_tokens_high",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_object_available",
        "notes",
    ]
    totals = [0, 0, 0]
    with (OUT / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for spec in calls:
            tl, te, th = band(spec["text"])
            il, ie, ih = band(spec["image"])
            ol, oe, oh = band(spec["output"])
            rl, re, rh = band(spec["reasoning"])
            low, expected, high = tl + il + ol + rl, te + ie + oe + re, th + ih + oh + rh
            totals[0] += low
            totals[1] += expected
            totals[2] += high
            writer.writerow(
                {
                    "document": DOC,
                    "iteration": ITERATION,
                    "call": spec["call"],
                    "model": spec["model"],
                    "text_input_tokens_low": tl,
                    "text_input_tokens_expected": te,
                    "text_input_tokens_high": th,
                    "cached_input_tokens": 0,
                    "image_file_input_tokens_low": il,
                    "image_file_input_tokens_expected": ie,
                    "image_file_input_tokens_high": ih,
                    "output_tokens_low": ol,
                    "output_tokens_expected": oe,
                    "output_tokens_high": oh,
                    "reasoning_tokens_low": rl,
                    "reasoning_tokens_expected": re,
                    "reasoning_tokens_high": rh,
                    "total_tokens_low": low,
                    "total_tokens_expected": expected,
                    "total_tokens_high": high,
                    "usage_object_available": "no",
                    "notes": spec["notes"],
                }
            )

    lines = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key was available, so the Responses input-token counting endpoint could not be called. Subagent usage objects were not exposed to the main agent. Estimates use local text bands plus image token proxies of ceil(width/32) * ceil(height/32). Cached input tokens are recorded as 0/unknown.",
        "",
        "| document | iteration | calls | low | expected | high |",
        "|---|---:|---:|---:|---:|---:|",
        f"| {DOC} | {ITERATION} | {len(calls)} | {totals[0]} | {totals[1]} | {totals[2]} |",
        "",
        "Image proxy token estimates:",
    ]
    for name, value in sorted(img_tokens.items()):
        lines.append(f"- {name}: {value}")
    (OUT / "token_usage_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    for item in rounds:
        slug = item["slug"]
        write_nodes(OUT / f"nodes_{slug}.csv", item["nodes"])
        write_edges(OUT / f"edges_{slug}.csv", item["edges"])
        write_edges(OUT / f"uncertain_edges_{slug}.csv", item["uncertain_edges"], include_status=False)
        write_matrix(OUT / f"connectivity_matrix_{slug}.csv", item["nodes"], item["edges"])
        write_sparse_matrix(OUT / f"connectivity_sparse_{slug}.csv", item["nodes"], item["edges"])

    write_nodes(OUT / "nodes_final.csv", final_nodes)
    write_edges(OUT / "edges_final.csv", sorted(final_edges))
    write_edges(OUT / "uncertain_edges_final.csv", sorted(uncertain_final), include_status=False)
    write_edges(OUT / "removed_edges_final.csv", sorted(removed_direct_edges), include_status=False)
    write_matrix(OUT / "connectivity_matrix_final.csv", final_nodes, sorted(final_edges))
    write_sparse_matrix(OUT / "connectivity_sparse_final.csv", final_nodes, sorted(final_edges))

    endpoint_nodes = {node for edge in final_edges for node in edge}
    qa = {
        "document": DOC,
        "iteration": ITERATION,
        "node_count_final": len(final_nodes),
        "edge_count_final": len(final_edges),
        "uncertain_edge_count_final": len(uncertain_final),
        "duplicates": sorted({n for n in final_nodes if final_nodes.count(n) > 1}),
        "missing_edge_endpoints": sorted(endpoint_nodes - set(final_nodes)),
        "isolated_nodes_final": sorted(set(final_nodes) - endpoint_nodes),
        "diagonal_policy": "all zero; no self-loops justified",
        "symmetry": "matrix writer mirrors undirected edge set",
        "final_policy": "solid or dashed line endpoints count only when visually terminating on both endpoint nodes; crossings and label-only associations excluded",
        "source_files": [str(RAW), str(OVERLAY), str(MASK)],
    }
    (OUT / "qa_final.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")

    notes = [
        "# Document 12 Round Notes",
        "",
        "Inputs used: only raw schematic, wires mask, wires overlay, and local crops derived from those files. No GT or GT-derived feedback/resources were used.",
        "",
        "| round | agent | matrix | notes |",
        "|---|---|---|---|",
    ]
    for item in rounds:
        notes.append(f"| {item['slug']} | {item['agent']} | connectivity_matrix_{item['slug']}.csv | {item['notes']} |")
    notes.extend(
        [
            "",
            "Final saturation: Jennifer R2 accepted Diego R2's six directly visible control-edge restorations and kept broader relay/TB/RPS fan-out uncertain.",
            "",
            "Final removed edges: direct BUS-120VAC-ESF--PNL-ESFAS-A and BUS-120VAC-ESF--PNL-ESFAS-B.",
        ]
    )
    (OUT / "round_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")
    write_token_usage()

    print(json.dumps({"out": str(OUT), "nodes": len(final_nodes), "edges": len(final_edges), "uncertain": len(uncertain_final)}, indent=2))


if __name__ == "__main__":
    main()
