from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


DOCUMENT = "26"
ITERATION = "1"
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"

SOURCE_FILES = [
    "raw -- synthetic_npp_electrical_schematic_v3(1).png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
    "wire_nodes.csv",
    "wire_nodes_overlay.png",
]

TRAINS = ["A", "B"]


def train_nodes(train: str) -> list[str]:
    nodes: list[str] = []
    if train == "A":
        nodes.extend(["GEN-301", "TR-UAT-31", "CB-4A-IN1"])
    nodes.extend(
        [
            f"SAT-31{train}",
            f"CB-4{train}-ST",
            f"DG-31{train}",
            f"CB-4{train}-DG",
            f"BUS-416{train}",
        ]
    )
    nodes.extend(f"CB-4{train}{i:02d}" for i in range(1, 7))
    nodes.extend(
        [
            f"TR-480{train}1",
            f"CB-480{train}-IN",
            f"TR-480{train}2",
            f"CB-480{train}-ALT",
            f"DS-RCP-{train}",
            f"MTR-RCP-{train}",
            f"GND-RCP-{train}",
            f"DS-SW-{train}",
            f"PUMP-SW31{train}",
            f"GND-SW-{train}",
            f"DS-AFW-{train}",
            f"PUMP-AFW31{train}",
            f"DS-CHW-{train}",
            f"MTR-CHWP-{train}",
            f"BUS-480{train}",
        ]
    )
    nodes.extend(f"CB-480{train}{i}" for i in range(11, 15))
    nodes.extend(
        [
            f"MCC-31{train}1",
            f"GND-MCC-{train}1",
            f"MCC-31{train}2",
            f"GND-MCC-{train}2",
            f"LC-31{train}3",
            f"PNL-31{train}4",
        ]
    )
    for group in range(1, 5):
        for branch in range(1, 4):
            nodes.extend([f"STR-{train}{group}-{branch}", f"JB-{train}{group}-{branch:02d}"])
    nodes.extend(
        [
            f"PUMP-CVC-{train}",
            f"MOV-RHR-731{train}",
            f"FAN-CRD-{train}",
            f"PUMP-CCW-{train}",
            f"HTR-BORIC-{train}",
            f"MOV-CHG-121{train}",
            f"MTR-SUMP-{train}",
            f"PUMP-LUBE-{train}",
            f"MOV-SI-902{train}",
            f"FAN-CONT-{train}",
            f"PUMP-SAMPLE-{train}",
            f"MOV-VENT-406{train}",
            f"BAT-31{train}",
            f"DS-BAT-{train}",
            f"CHG-31{train}",
            f"CB-CHG-{train}",
            f"BUS-125DC{train}",
            f"PNL-DC-{train}",
            f"CB-INV-{train}",
            f"INV-31{train}",
            f"BUS-INV-{train}",
            f"PNL-AC-{train}",
            f"RPS-PNL-{train}",
            f"TB-UPS-{train}",
            f"BUS-120N-{train}",
        ]
    )
    for index in range(1, 5):
        nodes.extend([f"RELAY-K7{train}{index}", f"TB-RPS-{train}{index}", f"PT-31{train}{index}"])
    return nodes


NODES = train_nodes("A") + ["CB-4AB-TIE", "CB-480AB-TIE", "CB-DCAB-TIE"] + train_nodes("B")


def e(source: str, target: str, edge_type: str, confidence: str, evidence: str) -> tuple[str, str, str, str, str]:
    return source, target, edge_type, confidence, evidence


def add(edges: list[tuple[str, str, str, str, str]], a: str, b: str, edge_type: str, evidence: str, confidence: str = "high") -> None:
    edges.append(e(a, b, edge_type, confidence, evidence))


def add_train_power(edges: list[tuple[str, str, str, str, str]], train: str) -> None:
    if train == "A":
        add(edges, "GEN-301", "TR-UAT-31", "solid_power", "generator to unit auxiliary transformer")
        add(edges, "TR-UAT-31", "CB-4A-IN1", "solid_power", "unit auxiliary transformer incoming feeder")
        add(edges, "CB-4A-IN1", "BUS-416A", "solid_power", "incoming breaker lands on BUS-416A")

    add(edges, f"SAT-31{train}", f"CB-4{train}-ST", "solid_power", "standby transformer vertical feeder")
    add(edges, f"CB-4{train}-ST", f"BUS-416{train}", "solid_power", "standby breaker lands on 4.16 kV bus")
    add(edges, f"DG-31{train}", f"CB-4{train}-DG", "solid_power", "diesel generator feeder")
    add(edges, f"CB-4{train}-DG", f"BUS-416{train}", "solid_power", "diesel breaker lands on 4.16 kV bus")

    feeder_specs = [
        ("01", f"TR-480{train}1", f"CB-480{train}-IN", f"BUS-480{train}"),
        ("02", f"TR-480{train}2", f"CB-480{train}-ALT", f"BUS-480{train}"),
        ("03", f"DS-RCP-{train}", f"MTR-RCP-{train}", f"GND-RCP-{train}"),
        ("04", f"DS-SW-{train}", f"PUMP-SW31{train}", f"GND-SW-{train}"),
        ("05", f"DS-AFW-{train}", f"PUMP-AFW31{train}", None),
        ("06", f"DS-CHW-{train}", f"MTR-CHWP-{train}", None),
    ]
    for number, mid, load, tail in feeder_specs:
        breaker = f"CB-4{train}{number}"
        add(edges, f"BUS-416{train}", breaker, "solid_power", f"feeder tap from BUS-416{train}")
        add(edges, breaker, mid, "solid_power", "solid feeder through branch device")
        add(edges, mid, load, "solid_power", "branch device lands on load")
        if tail:
            add(edges, load, tail, "solid_ground", "explicit tagged ground lead", "medium_high")


def add_480_distribution(edges: list[tuple[str, str, str, str, str]], train: str) -> None:
    panel_specs = [
        (11, f"MCC-31{train}1", f"GND-MCC-{train}1"),
        (12, f"MCC-31{train}2", f"GND-MCC-{train}2"),
        (13, f"LC-31{train}3", None),
        (14, f"PNL-31{train}4", None),
    ]
    for breaker_number, panel, ground in panel_specs:
        breaker = f"CB-480{train}{breaker_number}"
        add(edges, f"BUS-480{train}", breaker, "solid_power", f"feeder tap from BUS-480{train}")
        add(edges, breaker, panel, "solid_power", "breaker lands on 480 V distribution panel")
        if ground:
            add(edges, panel, ground, "solid_ground", "explicit tagged ground lead", "medium_high")

    group_panels = {
        1: f"MCC-31{train}1",
        2: f"MCC-31{train}2",
        3: f"LC-31{train}3",
        4: f"PNL-31{train}4",
    }
    loads = [
        f"PUMP-CVC-{train}",
        f"MOV-RHR-731{train}",
        f"FAN-CRD-{train}",
        f"PUMP-CCW-{train}",
        f"HTR-BORIC-{train}",
        f"MOV-CHG-121{train}",
        f"MTR-SUMP-{train}",
        f"PUMP-LUBE-{train}",
        f"MOV-SI-902{train}",
        f"FAN-CONT-{train}",
        f"PUMP-SAMPLE-{train}",
        f"MOV-VENT-406{train}",
    ]
    load_index = 0
    for group in range(1, 5):
        for branch in range(1, 4):
            starter = f"STR-{train}{group}-{branch}"
            junction = f"JB-{train}{group}-{branch:02d}"
            load = loads[load_index]
            load_index += 1
            add(edges, group_panels[group], starter, "solid_power", "branch tap from distribution panel")
            add(edges, starter, junction, "solid_power", "starter-to-junction vertical feeder")
            add(edges, junction, load, "solid_power", "junction lands on load")


def add_dc_control(edges: list[tuple[str, str, str, str, str]], train: str) -> None:
    add(edges, f"BAT-31{train}", f"DS-BAT-{train}", "solid_dc", "battery feeds disconnect")
    add(edges, f"DS-BAT-{train}", f"BUS-125DC{train}", "solid_dc", "battery disconnect lands on DC bus")
    add(edges, f"CHG-31{train}", f"CB-CHG-{train}", "solid_dc", "charger feeds breaker")
    add(edges, f"CB-CHG-{train}", f"BUS-125DC{train}", "solid_dc", "charger breaker lands on DC bus")
    add(edges, f"BUS-125DC{train}", f"PNL-DC-{train}", "solid_dc", "DC panel tap from bus")
    add(edges, f"BUS-125DC{train}", f"CB-INV-{train}", "solid_dc", "inverter breaker tap from DC bus")
    add(edges, f"CB-INV-{train}", f"INV-31{train}", "solid_dc", "inverter breaker lands on inverter")
    add(edges, f"INV-31{train}", f"BUS-INV-{train}", "solid_ac", "inverter output lands on inverter bus")
    add(edges, f"BUS-INV-{train}", f"PNL-AC-{train}", "solid_ac", "AC panel feed from inverter bus")
    add(edges, f"PNL-AC-{train}", f"BUS-120N-{train}", "solid_ac", "AC panel lower feed lands on 120N bus")
    add(edges, f"BUS-INV-{train}", f"RPS-PNL-{train}", "solid_ac", "RPS panel feed from inverter bus")
    add(edges, f"RPS-PNL-{train}", f"TB-UPS-{train}", "dashed_control", "dashed UPS/RPS control run", "medium_high")
    for index in range(1, 5):
        relay = f"RELAY-K7{train}{index}"
        terminal = f"TB-RPS-{train}{index}"
        pt = f"PT-31{train}{index}"
        add(edges, f"BUS-120N-{train}", relay, "solid_ac", "relay tap from 120N bus")
        add(edges, relay, terminal, "dotted_instrument", "short instrument drop to terminal block", "medium_high")
        add(edges, terminal, pt, "dotted_instrument", "dotted instrument lead to PT", "high")


def final_edges() -> list[tuple[str, str, str, str, str]]:
    edges: list[tuple[str, str, str, str, str]] = []
    for train in TRAINS:
        add_train_power(edges, train)
    add(edges, "BUS-416A", "CB-4AB-TIE", "solid_power", "left side of 4.16 kV tie breaker")
    add(edges, "CB-4AB-TIE", "BUS-416B", "solid_power", "right side of 4.16 kV tie breaker")

    for train in TRAINS:
        add_480_distribution(edges, train)
    add(edges, "BUS-480A", "CB-480AB-TIE", "solid_power", "left side of 480 V tie breaker")
    add(edges, "CB-480AB-TIE", "BUS-480B", "solid_power", "right side of 480 V tie breaker")

    add(edges, "BUS-125DCA", "CB-DCAB-TIE", "solid_dc", "left side of 125 VDC tie breaker")
    add(edges, "CB-DCAB-TIE", "BUS-125DCB", "solid_dc", "right side of 125 VDC tie breaker")
    for train in TRAINS:
        add_dc_control(edges, train)

    add(edges, "CB-480A13", "STR-A3-3", "dashed_control", "dashed side trunk from breaker/load-center region to A3-3 branch", "medium")
    add(edges, "CB-480B13", "STR-B3-3", "dashed_control", "dashed side trunk from breaker/load-center region to B3-3 branch", "medium")
    return edges


FINAL_EDGES = final_edges()
REMOVED_DIEGO_EDGES = [
    e("CB-4A03", "MTR-RCP-A", "dashed_control_candidate", "low", "removed: route passes beside tagged RCP motor rather than landing on it"),
    e("CB-4B03", "MTR-RCP-B", "dashed_control_candidate", "low", "removed: route passes beside tagged RCP motor rather than landing on it"),
    e("STR-A1-1", "MOV-RHR-731A", "dashed_control_candidate", "low", "removed: route passes beside RHR branch rather than landing on the valve"),
    e("STR-B1-1", "MOV-RHR-731B", "dashed_control_candidate", "low", "removed: route passes beside RHR branch rather than landing on the valve"),
    e("STR-A3-3", "MOV-SI-902A", "dashed_control_candidate", "low", "removed: route passes beside SI branch rather than landing on the valve"),
    e("STR-B3-3", "MOV-SI-902B", "dashed_control_candidate", "low", "removed: route passes beside SI branch rather than landing on the valve"),
]
DIEGO_R1_EDGES = FINAL_EDGES + REMOVED_DIEGO_EDGES

EXCLUSIONS = [
    ("CB-4A03--MTR-RCP-A", "removed in Jennifer/Diego convergence: dashed route is adjacent to RCP branch, not landed on motor"),
    ("CB-4B03--MTR-RCP-B", "removed in Jennifer/Diego convergence: dashed route is adjacent to RCP branch, not landed on motor"),
    ("STR-A1-1--MOV-RHR-731A", "removed in Jennifer/Diego convergence: dashed route is adjacent to RHR branch"),
    ("STR-B1-1--MOV-RHR-731B", "removed in Jennifer/Diego convergence: dashed route is adjacent to RHR branch"),
    ("STR-A3-3--MOV-SI-902A", "removed in Jennifer/Diego convergence: dashed route is adjacent to SI branch"),
    ("STR-B3-3--MOV-SI-902B", "removed in Jennifer/Diego convergence: dashed route is adjacent to SI branch"),
    ("RPS-PNL-A--BUS-120N-A", "not added: RPS panel has no visible solid downlead to 120N bus"),
    ("RPS-PNL-B--BUS-120N-B", "not added: RPS panel has no visible solid downlead to 120N bus"),
    ("wire tag labels", "excluded as cable/wire labels, not component or logical-node names"),
]

ROUND_DEFINITIONS = [
    {
        "round": "round_01_diego",
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "candidate graph; included six route-adjacent dashed control candidates",
        "nodes": NODES,
        "edges": DIEGO_R1_EDGES,
    },
    {
        "round": "round_02_jennifer",
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "status": "removed six unsupported dashed route-adjacent candidates; no additions",
        "nodes": NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_03_diego",
        "agent": "Diego",
        "role": "convergence reviewer",
        "status": "SATURATED_CANDIDATE: agreed with Jennifer corrected set",
        "nodes": NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_04_jennifer_final",
        "agent": "Jennifer",
        "role": "final saturation reviewer",
        "status": "SATURATED final graph confirmed",
        "nodes": NODES,
        "edges": FINAL_EDGES,
    },
]

TOKEN_CALLS = [
    {
        "model_call": "main-01-inventory-visual-crop-and-local-graphing",
        "caller": "main agent",
        "round": "prep",
        "input_tokens_est": 10800,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 8500,
        "output_tokens_low": 800,
        "output_tokens_expected": 1500,
        "output_tokens_high": 2400,
        "reasoning_tokens_low": 1400,
        "reasoning_tokens_expected": 2600,
        "reasoning_tokens_high": 4600,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "folder inventory, visual crop generation, local candidate graph",
    },
    {
        "model_call": "subagent-diego-01-high-recall",
        "caller": "Diego",
        "round": "round_01_diego",
        "input_tokens_est": 4300,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 22000,
        "output_tokens_low": 12000,
        "output_tokens_expected": 18000,
        "output_tokens_high": 25000,
        "reasoning_tokens_low": 2500,
        "reasoning_tokens_expected": 5200,
        "reasoning_tokens_high": 9000,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "high-recall extraction from raw, crops, and wire-node overlay",
    },
    {
        "model_call": "subagent-jennifer-02-precision-review",
        "caller": "Jennifer",
        "round": "round_02_jennifer",
        "input_tokens_est": 8200,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 17000,
        "output_tokens_low": 500,
        "output_tokens_expected": 900,
        "output_tokens_high": 1500,
        "reasoning_tokens_low": 1200,
        "reasoning_tokens_expected": 2500,
        "reasoning_tokens_high": 4500,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "precision review of dashed/RPS ambiguity",
    },
    {
        "model_call": "subagent-diego-03-convergence",
        "caller": "Diego",
        "round": "round_03_diego",
        "input_tokens_est": 1100,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 80,
        "output_tokens_expected": 160,
        "output_tokens_high": 300,
        "reasoning_tokens_low": 120,
        "reasoning_tokens_expected": 300,
        "reasoning_tokens_high": 700,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "agreed with Jennifer corrected set",
    },
    {
        "model_call": "subagent-jennifer-04-final-saturation",
        "caller": "Jennifer",
        "round": "round_04_jennifer_final",
        "input_tokens_est": 360,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 40,
        "output_tokens_expected": 90,
        "output_tokens_high": 180,
        "reasoning_tokens_low": 50,
        "reasoning_tokens_expected": 150,
        "reasoning_tokens_high": 350,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "final saturation confirmation",
    },
    {
        "model_call": "main-02-result-writing-and-final-response",
        "caller": "main agent",
        "round": "writeup",
        "input_tokens_est": 9500,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 900,
        "output_tokens_expected": 1600,
        "output_tokens_high": 2600,
        "reasoning_tokens_low": 1100,
        "reasoning_tokens_expected": 2100,
        "reasoning_tokens_high": 3800,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "round/final matrix generation and final summary",
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
    missing = sorted({node for pair in edges for node in pair if node not in node_set})
    if missing:
        raise ValueError(f"Edges reference missing nodes: {missing}")
    idx = {node: index for index, node in enumerate(nodes)}
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
    report = f"""# Document 26 Connectivity Extraction

## Scope

Only resources inside:

`{BASE}`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, validation metrics, prior result files, or off-the-shelf OCR outputs were used. Existing validation files in the results folder were not used as extraction evidence.

## Multi-Agent Rounds

1. Diego round 1: high-recall graph with 200 nodes and 209 plausible edges.
2. Jennifer round 2: removed six route-adjacent dashed control candidates, leaving 200 nodes and 203 edges.
3. Diego round 3: agreed with Jennifer's corrected set.
4. Jennifer round 4: confirmed saturation.

The raw title block visibly states 200 components and 209 connections. The agents treated that as a consistency clue only. The final precision graph keeps the 200 visible component/node tags and excludes six dashed route-adjacent candidates that do not visually land on the tagged endpoints.

## Final Result

- Final nodes: {len(NODES)}
- Final undirected edges: {len(FINAL_EDGES)}
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`

## Final Edges

{edge_lines}

## Excluded Or Ambiguous Items

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


def validate_no_duplicates(edges: list[tuple[str, str, str, str, str]]) -> None:
    pairs = [tuple(sorted((a, b))) for a, b, *_ in edges]
    duplicates = sorted({pair for pair in pairs if pairs.count(pair) > 1})
    if duplicates:
        raise AssertionError(f"Duplicate undirected edges: {duplicates}")


def main() -> None:
    if len(NODES) != 200:
        raise AssertionError(f"Expected 200 nodes, got {len(NODES)}")
    if len(set(NODES)) != len(NODES):
        raise AssertionError("Node list contains duplicates")
    if len(FINAL_EDGES) != 203:
        raise AssertionError(f"Expected 203 final edges, got {len(FINAL_EDGES)}")
    if len(DIEGO_R1_EDGES) != 209:
        raise AssertionError(f"Expected 209 Diego round 1 edges, got {len(DIEGO_R1_EDGES)}")
    validate_no_duplicates(FINAL_EDGES)
    validate_no_duplicates(DIEGO_R1_EDGES)

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
