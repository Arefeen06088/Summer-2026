from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


DOCUMENT = "15"
ITERATION = "1"
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"

SOURCE_FILES = [
    "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
    "wire_nodes.csv",
    "wire_nodes_overlay.png",
]

DIVS = ["A", "B", "C", "D"]

COMMON_NODES = [
    "GEN-101",
    "CB-GEN-101",
    "TR-GSU-1",
    "BUS-SWY-1",
    "TR-UAT-1",
    "TR-SAT-1",
    "BUS-NSS-1",
    "CB-SWY-TIE",
    "GEN-102",
    "CB-GEN-102",
    "TR-GSU-2",
    "BUS-SWY-2",
    "TR-UAT-2",
    "TR-SAT-2",
    "BUS-NSS-2",
    "DG-1A",
    "DG-1B",
    "DG-1C",
    "DG-1D",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "SEQ-1AB",
    "RPS-AC-1",
    "CB-TIE-CD",
    "DS-TIE-CD",
    "SEQ-2CD",
    "RPS-AC-2",
]


def div_nodes(x: str) -> list[str]:
    return [
        f"CB-NF-{x}",
        f"CB-DG-{x}",
        f"BUS-416{x}",
        f"CB-TX-{x}",
        f"TR-480{x}",
        f"BUS-480{x}",
        f"MCC-1{x}",
        f"CB-{x}01",
        f"CB-{x}02",
        f"CB-{x}03",
        f"CB-{x}04",
        f"CB-{x}05",
        f"CB-{x}06",
        f"DS-{x}01",
        f"FU-{x}02",
        f"DS-{x}03",
        f"FU-{x}04",
        f"DS-{x}05",
        f"FU-{x}06",
        f"RLY-{x}01",
        f"RLY-{x}02",
        f"RLY-{x}03",
        f"RLY-{x}04",
        f"RLY-{x}05",
        f"RLY-{x}06",
        f"PMP-SI-{x}1",
        f"PMP-CS-{x}2",
        f"MOV-{x}03",
        f"MTR-{x}04",
        f"INST-{x}05",
        f"PMP-SW-{x}6",
        f"BAT-125{x}",
        f"CHG-1{x}",
        f"BUS-DC-{x}",
        f"INV-1{x}",
        f"CP-1{x}",
        f"TB-1{x}",
        f"JB-1{x}",
        f"GND-{x}",
    ]


NODES = COMMON_NODES[:]
for div in DIVS:
    NODES.extend(div_nodes(div))


def e(source: str, target: str, edge_type: str, confidence: str, evidence: str) -> tuple[str, str, str, str, str]:
    return source, target, edge_type, confidence, evidence


def base_edges() -> list[tuple[str, str, str, str, str]]:
    edges = [
        e("GEN-101", "CB-GEN-101", "solid_power", "high", "top source solid line"),
        e("CB-GEN-101", "TR-GSU-1", "solid_power", "high", "top source solid line"),
        e("TR-GSU-1", "BUS-SWY-1", "solid_power", "high", "vertical drop to switchyard bus"),
        e("BUS-SWY-1", "CB-SWY-TIE", "solid_power", "high", "switchyard tie solid line"),
        e("CB-SWY-TIE", "BUS-SWY-2", "solid_power", "high", "switchyard tie solid line"),
        e("GEN-102", "CB-GEN-102", "solid_power", "high", "top source solid line"),
        e("CB-GEN-102", "TR-GSU-2", "solid_power", "high", "top source solid line"),
        e("TR-GSU-2", "BUS-SWY-2", "solid_power", "high", "vertical drop to switchyard bus"),
        e("BUS-SWY-1", "TR-UAT-1", "solid_power", "high", "solid transformer drop"),
        e("TR-UAT-1", "BUS-NSS-1", "solid_power", "high", "solid transformer drop"),
        e("BUS-SWY-1", "TR-SAT-1", "solid_power", "high", "solid transformer drop"),
        e("TR-SAT-1", "BUS-NSS-1", "solid_power", "high", "solid transformer drop"),
        e("BUS-SWY-2", "TR-UAT-2", "solid_power", "high", "solid transformer drop"),
        e("TR-UAT-2", "BUS-NSS-2", "solid_power", "high", "solid transformer drop"),
        e("BUS-SWY-2", "TR-SAT-2", "solid_power", "high", "solid transformer drop"),
        e("TR-SAT-2", "BUS-NSS-2", "solid_power", "high", "solid transformer drop"),
        e("BUS-NSS-1", "CB-NF-A", "solid_power", "high", "solid normal feeder"),
        e("DG-1A", "CB-DG-A", "solid_power", "high", "solid diesel feeder drop"),
        e("CB-NF-A", "BUS-416A", "solid_power", "high", "solid feeder to 4.16 kV bus"),
        e("CB-DG-A", "BUS-416A", "solid_power", "high", "solid diesel feeder to 4.16 kV bus"),
        e("BUS-NSS-1", "CB-NF-B", "solid_power", "high", "solid normal feeder"),
        e("DG-1B", "CB-DG-B", "solid_power", "high", "solid diesel feeder drop"),
        e("CB-NF-B", "BUS-416B", "solid_power", "high", "solid feeder to 4.16 kV bus"),
        e("CB-DG-B", "BUS-416B", "solid_power", "high", "solid diesel feeder to 4.16 kV bus"),
        e("BUS-NSS-2", "CB-NF-C", "solid_power", "high", "solid normal feeder"),
        e("DG-1C", "CB-DG-C", "solid_power", "high", "solid diesel feeder drop"),
        e("CB-NF-C", "BUS-416C", "solid_power", "high", "solid feeder to 4.16 kV bus"),
        e("CB-DG-C", "BUS-416C", "solid_power", "high", "solid diesel feeder to 4.16 kV bus"),
        e("BUS-NSS-2", "CB-NF-D", "solid_power", "high", "solid normal feeder"),
        e("DG-1D", "CB-DG-D", "solid_power", "high", "solid diesel feeder drop"),
        e("CB-NF-D", "BUS-416D", "solid_power", "high", "solid feeder to 4.16 kV bus"),
        e("CB-DG-D", "BUS-416D", "solid_power", "high", "solid diesel feeder to 4.16 kV bus"),
        e("BUS-416A", "CB-TX-A", "solid_power", "high", "solid transformer feeder"),
        e("CB-TX-A", "TR-480A", "solid_power", "high", "solid transformer feeder"),
        e("TR-480A", "BUS-480A", "solid_power", "high", "solid transformer feeder"),
        e("BUS-480A", "MCC-1A", "solid_power", "high", "solid load-center to MCC feeder"),
        e("BUS-416B", "CB-TX-B", "solid_power", "high", "solid transformer feeder"),
        e("CB-TX-B", "TR-480B", "solid_power", "high", "solid transformer feeder"),
        e("TR-480B", "BUS-480B", "solid_power", "high", "solid transformer feeder"),
        e("BUS-480B", "MCC-1B", "solid_power", "high", "solid load-center to MCC feeder"),
        e("BUS-416C", "CB-TX-C", "solid_power", "high", "solid transformer feeder"),
        e("CB-TX-C", "TR-480C", "solid_power", "high", "solid transformer feeder"),
        e("TR-480C", "BUS-480C", "solid_power", "high", "solid transformer feeder"),
        e("BUS-480C", "MCC-1C", "solid_power", "high", "solid load-center to MCC feeder"),
        e("BUS-416D", "CB-TX-D", "solid_power", "high", "solid transformer feeder"),
        e("CB-TX-D", "TR-480D", "solid_power", "high", "solid transformer feeder"),
        e("TR-480D", "BUS-480D", "solid_power", "high", "solid transformer feeder"),
        e("BUS-480D", "MCC-1D", "solid_power", "high", "solid load-center to MCC feeder"),
        e("BUS-416A", "CB-TIE-AB", "solid_power", "high", "normally-open tie solid line"),
        e("CB-TIE-AB", "DS-TIE-AB", "solid_power", "high", "normally-open tie solid line"),
        e("DS-TIE-AB", "BUS-416B", "solid_power", "high", "normally-open tie solid line"),
        e("BUS-416C", "CB-TIE-CD", "solid_power", "high", "normally-open tie solid line"),
        e("CB-TIE-CD", "DS-TIE-CD", "solid_power", "high", "normally-open tie solid line"),
        e("DS-TIE-CD", "BUS-416D", "solid_power", "high", "normally-open tie solid line"),
        e("CB-DG-A", "SEQ-1AB", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-NF-B", "SEQ-1AB", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-DG-A", "RPS-AC-1", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-NF-B", "RPS-AC-1", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-DG-C", "SEQ-2CD", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-NF-D", "SEQ-2CD", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-DG-C", "RPS-AC-2", "dashed_control", "high", "dashed cross-division control endpoint"),
        e("CB-NF-D", "RPS-AC-2", "dashed_control", "high", "dashed cross-division control endpoint"),
    ]

    for x in DIVS:
        branch_specs = [
            ("01", f"DS-{x}01", f"PMP-SI-{x}1", f"RLY-{x}01"),
            ("02", f"FU-{x}02", f"PMP-CS-{x}2", f"RLY-{x}02"),
            ("03", f"DS-{x}03", f"MOV-{x}03", f"RLY-{x}03"),
            ("04", f"FU-{x}04", f"MTR-{x}04", f"RLY-{x}04"),
            ("05", f"DS-{x}05", f"INST-{x}05", f"RLY-{x}05"),
            ("06", f"FU-{x}06", f"PMP-SW-{x}6", f"RLY-{x}06"),
        ]
        for num, mid, load, relay in branch_specs:
            cb = f"CB-{x}{num}"
            edges.append(e(f"MCC-1{x}", cb, "solid_power", "high", f"MCC-1{x} branch vertical feeder"))
            edges.append(e(cb, mid, "solid_power", "high", "branch device in series"))
            edges.append(e(mid, load, "solid_power", "high", "branch load feeder"))
            edges.append(e(cb, relay, "dashed_control", "medium_high", "dashed relay lead from breaker"))
        edges.extend(
            [
                e(f"RLY-{x}06", f"TB-1{x}", "dashed_control", "medium_high", "dashed relay lead continues to terminal block"),
                e(f"BAT-125{x}", f"CHG-1{x}", "dashed_control", "medium_high", "dashed 125 VDC control line"),
                e(f"CHG-1{x}", f"BUS-DC-{x}", "dashed_control", "medium_high", "dashed 125 VDC control line to bus"),
                e(f"BUS-DC-{x}", f"INV-1{x}", "dashed_control", "medium_high", "dashed 125 VDC control line"),
                e(f"INV-1{x}", f"CP-1{x}", "dashed_control", "medium_high", "dashed control line"),
                e(f"CP-1{x}", f"TB-1{x}", "dashed_control", "medium_high", "dashed terminal control line"),
                e(f"CP-1{x}", f"JB-1{x}", "dashed_control", "medium_high", "dashed junction-box branch"),
                e(f"BUS-DC-{x}", f"GND-{x}", "dashed_control", "medium", "explicit dashed ground-reference connection"),
            ]
        )
    return edges


FINAL_EDGES = base_edges()
LOCAL_CONTEXT_EDGES = [
    e(f"CB-NF-{x}", f"CB-DG-{x}", "dashed_control_context", "medium", "local dashed breaker-to-breaker context/control-trip line, later excluded")
    for x in DIVS
]
PROXIMITY_EDGES = [
    e("BUS-NSS-1", "DG-1A", "inline_symbol_contact", "medium", "high-recall proximity of DG symbol on NSS bus, later excluded"),
    e("BUS-NSS-2", "DG-1C", "inline_symbol_contact", "medium", "high-recall proximity of DG symbol on NSS bus, later excluded"),
]

DIEGO_R1_EDGES = FINAL_EDGES + LOCAL_CONTEXT_EDGES + PROXIMITY_EDGES
JENNIFER_R2_EDGES = FINAL_EDGES + LOCAL_CONTEXT_EDGES

EXCLUSIONS = [
    ("BUS-NSS-1--DG-1A", "removed as proximity/overlap; diesel source clearly connects to CB-DG-A"),
    ("BUS-NSS-2--DG-1C", "removed as proximity/overlap; diesel source clearly connects to CB-DG-C"),
    ("CB-NF-A--CB-DG-A", "removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing"),
    ("CB-NF-B--CB-DG-B", "removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing"),
    ("CB-NF-C--CB-DG-C", "removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing"),
    ("CB-NF-D--CB-DG-D", "removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing"),
    ("BUS-416A--BUS-416B", "not added directly; normally-open tie passes through CB-TIE-AB and DS-TIE-AB"),
    ("BUS-416C--BUS-416D", "not added directly; normally-open tie passes through CB-TIE-CD and DS-TIE-CD"),
]

ROUND_DEFINITIONS = [
    {
        "round": "round_01_diego",
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "candidate graph; included two NSS-DG proximity edges and four local dashed context edges",
        "nodes": NODES,
        "edges": DIEGO_R1_EDGES,
    },
    {
        "round": "round_02_jennifer",
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "status": "removed NSS-DG proximity edges; retained local dashed context edges pending convergence",
        "nodes": NODES,
        "edges": JENNIFER_R2_EDGES,
    },
    {
        "round": "round_03_diego",
        "agent": "Diego",
        "role": "convergence reviewer",
        "status": "Option B: removed four local dashed context edges and retained ground edges; 183 nodes / 190 edges",
        "nodes": NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_04_jennifer_final",
        "agent": "Jennifer",
        "role": "final saturation reviewer",
        "status": "SATURATED: final graph is Diego round 3 Option B",
        "nodes": NODES,
        "edges": FINAL_EDGES,
    },
]

TOKEN_CALLS = [
    {
        "model_call": "main-01-orchestration-and-visual-prep",
        "caller": "main agent",
        "round": "prep",
        "input_tokens_est": 7800,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 600,
        "output_tokens_expected": 1100,
        "output_tokens_high": 1800,
        "reasoning_tokens_low": 1000,
        "reasoning_tokens_expected": 1800,
        "reasoning_tokens_high": 3200,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "source inventory, crop generation, local visual triage",
    },
    {
        "model_call": "subagent-diego-01-high-recall",
        "caller": "Diego",
        "round": "round_01_diego",
        "input_tokens_est": 3600,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 15000,
        "output_tokens_low": 6500,
        "output_tokens_expected": 9500,
        "output_tokens_high": 13000,
        "reasoning_tokens_low": 1600,
        "reasoning_tokens_expected": 3200,
        "reasoning_tokens_high": 6000,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "large high-recall graph from raw/overlay/crops",
    },
    {
        "model_call": "subagent-jennifer-02-precision-review",
        "caller": "Jennifer",
        "round": "round_02_jennifer",
        "input_tokens_est": 9000,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 12000,
        "output_tokens_low": 5000,
        "output_tokens_expected": 8000,
        "output_tokens_high": 11000,
        "reasoning_tokens_low": 1500,
        "reasoning_tokens_expected": 3000,
        "reasoning_tokens_high": 5500,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "precision review of 183-node graph",
    },
    {
        "model_call": "subagent-diego-03-convergence",
        "caller": "Diego",
        "round": "round_03_diego",
        "input_tokens_est": 4200,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 2500,
        "output_tokens_low": 500,
        "output_tokens_expected": 900,
        "output_tokens_high": 1500,
        "reasoning_tokens_low": 600,
        "reasoning_tokens_expected": 1200,
        "reasoning_tokens_high": 2200,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "resolved count-sensitive edge ambiguity",
    },
    {
        "model_call": "subagent-jennifer-04-saturation",
        "caller": "Jennifer",
        "round": "round_04_jennifer_final",
        "input_tokens_est": 1100,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 20,
        "output_tokens_expected": 80,
        "output_tokens_high": 200,
        "reasoning_tokens_low": 50,
        "reasoning_tokens_expected": 180,
        "reasoning_tokens_high": 450,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "confirmed final saturation",
    },
    {
        "model_call": "main-02-result-writing-and-final-report",
        "caller": "main agent",
        "round": "writeup",
        "input_tokens_est": 9000,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 900,
        "output_tokens_expected": 1600,
        "output_tokens_high": 2600,
        "reasoning_tokens_low": 1000,
        "reasoning_tokens_expected": 1900,
        "reasoning_tokens_high": 3400,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "writes round matrices and final summary",
    },
]


def edge_pairs(edges: list[tuple[str, str, str, str, str]]) -> list[tuple[str, str]]:
    return [(a, b) for a, b, *_ in edges]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_matrix(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    node_set = set(nodes)
    missing = sorted({node for edge in edges for node in edge if node not in node_set})
    if missing:
        raise ValueError(f"Edges reference missing nodes: {missing}")
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        if a == b:
            matrix[idx[a]][idx[b]] = 1
        else:
            matrix[idx[a]][idx[b]] = 1
            matrix[idx[b]][idx[a]] = 1
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = build_matrix(nodes, edges)
    for i, row in enumerate(matrix):
        if row[i] != 0:
            raise ValueError(f"Unexpected nonzero diagonal for {nodes[i]}")
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                raise ValueError(f"Matrix not symmetric at {nodes[i]} / {nodes[j]}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str, str, str, str]]) -> None:
    write_csv(
        path,
        [
            {
                "source": a,
                "target": b,
                "edge_type": edge_type,
                "confidence": confidence,
                "evidence": evidence,
            }
            for a, b, edge_type, confidence, evidence in edges
        ],
        ["source", "target", "edge_type", "confidence", "evidence"],
    )


def write_round_outputs() -> None:
    rows = []
    for rd in ROUND_DEFINITIONS:
        prefix = rd["round"]
        nodes = list(rd["nodes"])
        edges = list(rd["edges"])
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edge_pairs(edges))
        write_csv(
            RESULTS / f"{prefix}_node_order.csv",
            [{"index": i, "node": node} for i, node in enumerate(nodes)],
            ["index", "node"],
        )
        rows.append(
            {
                "round": prefix,
                "agent": rd["agent"],
                "role": rd["role"],
                "node_count": len(nodes),
                "edge_count": len(edges),
                "status": rd["status"],
            }
        )
    write_csv(RESULTS / "rounds_summary.csv", rows, ["round", "agent", "role", "node_count", "edge_count", "status"])


def write_final_outputs() -> None:
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", NODES, edge_pairs(FINAL_EDGES))
    write_csv(
        RESULTS / "final_node_order.csv",
        [{"index": i, "node": node} for i, node in enumerate(NODES)],
        ["index", "node"],
    )
    write_csv(
        RESULTS / "uncertain_or_excluded_edges.csv",
        [{"item": item, "reason": reason} for item, reason in EXCLUSIONS],
        ["item", "reason"],
    )


def total_for_call(call: dict[str, object], band: str) -> int:
    return (
        int(call["input_tokens_est"])
        + int(call["image_file_input_tokens_est"])
        + int(call[f"output_tokens_{band}"])
        + int(call[f"reasoning_tokens_{band}"])
    )


def token_rows() -> list[dict[str, object]]:
    rows = []
    for call in TOKEN_CALLS:
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": call["round"],
                "caller": call["caller"],
                "model_call": call["model_call"],
                "input_tokens_est": call["input_tokens_est"],
                "cached_input_tokens_est": call["cached_input_tokens_est"],
                "image_file_input_tokens_est": call["image_file_input_tokens_est"],
                "output_tokens_low": call["output_tokens_low"],
                "output_tokens_expected": call["output_tokens_expected"],
                "output_tokens_high": call["output_tokens_high"],
                "reasoning_tokens_low": call["reasoning_tokens_low"],
                "reasoning_tokens_expected": call["reasoning_tokens_expected"],
                "reasoning_tokens_high": call["reasoning_tokens_high"],
                "total_tokens_low": total_for_call(call, "low"),
                "total_tokens_expected": total_for_call(call, "expected"),
                "total_tokens_high": total_for_call(call, "high"),
                "usage_status": call["usage_status"],
                "counting_endpoint_status": call["counting_endpoint_status"],
                "notes": call["notes"],
            }
        )
    return rows


def write_tokens() -> dict[str, object]:
    rows = token_rows()
    fields = [
        "document",
        "iteration",
        "round",
        "caller",
        "model_call",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_status",
        "counting_endpoint_status",
        "notes",
    ]
    write_csv(RESULTS / "token_usage_estimate.csv", rows, fields)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "method": "local estimate because no API key was available for the OpenAI Responses input-token counting endpoint",
        "text_token_estimator": "approximate prompt/message token count from observed prompt sizes; fallback about 4 characters per token",
        "image_file_token_estimator": "standard high-detail vision tile heuristic applied qualitatively to raw/overlay/crop payloads",
        "usage_objects": "not exposed by the local Codex main/subagent tool responses",
        "calls": len(rows),
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in rows),
        "cached_input_tokens_est": sum(int(r["cached_input_tokens_est"]) for r in rows),
        "image_file_input_tokens_est": sum(int(r["image_file_input_tokens_est"]) for r in rows),
        "output_tokens_low": sum(int(r["output_tokens_low"]) for r in rows),
        "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in rows),
        "output_tokens_high": sum(int(r["output_tokens_high"]) for r in rows),
        "reasoning_tokens_low": sum(int(r["reasoning_tokens_low"]) for r in rows),
        "reasoning_tokens_expected": sum(int(r["reasoning_tokens_expected"]) for r in rows),
        "reasoning_tokens_high": sum(int(r["reasoning_tokens_high"]) for r in rows),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in rows),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in rows),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in rows),
    }
    summary_fields = [
        "document",
        "iteration",
        "method",
        "text_token_estimator",
        "image_file_token_estimator",
        "usage_objects",
        "calls",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
    ]
    write_csv(RESULTS / "token_usage_summary.csv", [summary], summary_fields)
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_source_inventory() -> None:
    rows = []
    for name in SOURCE_FILES:
        path = BASE / name
        rows.append({"file": name, "exists": path.exists(), "bytes": path.stat().st_size if path.exists() else ""})
    write_csv(RESULTS / "source_inventory.csv", rows, ["file", "exists", "bytes"])


def write_report(token_summary: dict[str, object]) -> None:
    edge_lines = "\n".join(f"- {a} -- {b} ({edge_type}, {confidence})" for a, b, edge_type, confidence, _ in FINAL_EDGES)
    exclusion_lines = "\n".join(f"- {item}: {reason}" for item, reason in EXCLUSIONS)
    report = f"""# Document 15 Connectivity Extraction

## Scope

Only resources inside:

`{BASE}`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, validation metrics, prior result files, or off-the-shelf OCR outputs were used. Existing validation files in the results folder were not used as extraction evidence.

## Multi-Agent Rounds

1. Diego round 1: high-recall graph with 183 nodes and 196 plausible edges.
2. Jennifer round 2: removed the two NSS-to-DG proximity edges.
3. Diego round 3: selected Option B; removed four local dashed breaker-to-breaker context edges and retained ground edges.
4. Jennifer round 4: confirmed saturation at Diego round 3 Option B.

## Final Result

- Final nodes: {len(NODES)}
- Final undirected edges: {len(FINAL_EDGES)}
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`
- Visible raw-sheet drafting QC: 183 nodes / 190 connections.

## Final Edges

{edge_lines}

## Excluded Or Collapsed Items

{exclusion_lines}

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: {token_summary["total_tokens_low"]}
- Estimated total expected: {token_summary["total_tokens_expected"]}
- Estimated total high: {token_summary["total_tokens_high"]}
- Estimated image/file input tokens: {token_summary["image_file_input_tokens_est"]}

Detailed estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    if len(NODES) != 183:
        raise AssertionError(f"Expected 183 nodes, got {len(NODES)}")
    if len(FINAL_EDGES) != 190:
        raise AssertionError(f"Expected 190 final edges, got {len(FINAL_EDGES)}")
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    write_source_inventory()
    write_round_outputs()
    write_final_outputs()
    token_summary = write_tokens()
    write_report(token_summary)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "base": str(BASE),
        "allowed_sources_only": True,
        "used_ground_truth": False,
        "used_ocr": False,
        "final_node_count": len(NODES),
        "final_edge_count": len(FINAL_EDGES),
        "rounds": [
            {
                "round": rd["round"],
                "agent": rd["agent"],
                "role": rd["role"],
                "node_count": len(rd["nodes"]),
                "edge_count": len(rd["edges"]),
                "status": rd["status"],
            }
            for rd in ROUND_DEFINITIONS
        ],
        "token_summary": token_summary,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    shutil.copy2(Path(__file__), CODES / Path(__file__).name)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
