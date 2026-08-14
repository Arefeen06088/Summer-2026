from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


@dataclass(frozen=True)
class Edge:
    a: str
    b: str
    evidence: str
    status: str = "accepted"


def e(a: str, b: str, evidence: str, status: str = "accepted") -> Edge:
    return Edge(a, b, evidence, status)


def unique_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str, str]] = set()
    result: list[Edge] = []
    for edge in edges:
        a, b = sorted((edge.a, edge.b))
        key = (a, b, edge.status)
        if key not in seen:
            seen.add(key)
            result.append(edge)
    return result


TRAINS = ["A", "B", "C", "D"]

TOP_NODES = [
    "GEN-01",
    "TR-UAT-1",
    "CB-UAT-1",
    "TR-SUT-1",
    "CB-SUT-1",
    "BUS-13-8A",
    "CB-13-TIE",
    "BUS-13-8B",
    "GEN-02",
    "TR-UAT-2",
    "CB-UAT-2",
    "TR-SUT-2",
    "CB-SUT-2",
]

TRAIN_NODE_TEMPLATE = [
    "CB-IN-{x}",
    "RELAY-27{x}",
    "DG-1{x}",
    "CB-DG-{x}",
    "BUS-4160-{x}",
    "CB-4160-{x}1",
    "CB-4160-{x}2",
    "TR-480-{x}1",
    "TR-480-{x}2",
    "CB-480-{x}1",
    "CB-480-{x}2",
    "BUS-480-{x}1",
    "BUS-480-{x}2",
    "CB-MCC-{x}1",
    "CB-MCC-{x}2",
    "MCC-{x}1",
    "MCC-{x}2",
    "PUMP-SI-{x}",
    "PUMP-CCW-{x}",
    "FAN-HVAC-{x}",
    "MOV-RHR-{x}",
    "RECT-125-{x}",
    "PANEL-IC-{x}",
]

BOTTOM_NODES = [
    "BAT-125A",
    "BUS-DC-125A",
    "INV-UPS-A",
    "PANEL-RPS-A",
    "BAT-125B",
    "BUS-DC-125B",
    "INV-UPS-B",
    "PANEL-RPS-B",
    "PANEL-SSPS",
    "ATS-480-A",
    "ATS-480-B",
]

FINAL_NODES = TOP_NODES + [name.format(x=x) for x in TRAINS for name in TRAIN_NODE_TEMPLATE] + BOTTOM_NODES

DIEGO_EXTRA_NODES = [
    "TIE-A12",
    "TIE-B12",
    "TIE-C12",
    "TIE-D12",
    "GND-A",
    "GND-B",
    "GND-C",
    "GND-D",
]

DIEGO_R1_NODES = FINAL_NODES + DIEGO_EXTRA_NODES


def top_edges() -> list[Edge]:
    return [
        e("GEN-01", "TR-UAT-1", "solid 13.8 kV source line"),
        e("TR-UAT-1", "CB-UAT-1", "solid line from transformer to breaker"),
        e("CB-UAT-1", "BUS-13-8A", "breaker lands on normal service bus A"),
        e("TR-SUT-1", "CB-SUT-1", "solid standby transformer feeder"),
        e("CB-SUT-1", "BUS-13-8A", "breaker lands on normal service bus A"),
        e("BUS-13-8A", "CB-13-TIE", "bus A enters tie breaker"),
        e("CB-13-TIE", "BUS-13-8B", "tie breaker exits to bus B"),
        e("GEN-02", "TR-UAT-2", "solid 13.8 kV source line"),
        e("TR-UAT-2", "CB-UAT-2", "solid line from transformer to breaker"),
        e("CB-UAT-2", "BUS-13-8B", "breaker lands on normal service bus B"),
        e("TR-SUT-2", "CB-SUT-2", "solid standby transformer feeder"),
        e("CB-SUT-2", "BUS-13-8B", "breaker lands on normal service bus B"),
        e("BUS-13-8A", "CB-IN-A", "normal incoming feeder to train A"),
        e("BUS-13-8A", "CB-IN-B", "normal incoming feeder to train B"),
        e("BUS-13-8B", "CB-IN-C", "normal incoming feeder to train C"),
        e("BUS-13-8B", "CB-IN-D", "normal incoming feeder to train D"),
    ]


def train_edges(x: str) -> list[Edge]:
    return [
        e(f"CB-IN-{x}", f"BUS-4160-{x}", "normal incoming breaker to 4.16 kV bus"),
        e(f"DG-1{x}", f"CB-DG-{x}", "diesel generator lead to breaker"),
        e(f"CB-DG-{x}", f"BUS-4160-{x}", "DG breaker feeder lands on 4.16 kV bus"),
        e(f"BUS-4160-{x}", f"CB-4160-{x}1", "feeder from 4.16 kV bus to branch 1 breaker"),
        e(f"CB-4160-{x}1", f"TR-480-{x}1", "branch 1 breaker to transformer"),
        e(f"TR-480-{x}1", f"CB-480-{x}1", "branch 1 transformer to low-side breaker"),
        e(f"CB-480-{x}1", f"BUS-480-{x}1", "branch 1 low-side breaker to 480 V bus"),
        e(f"BUS-4160-{x}", f"CB-4160-{x}2", "feeder from 4.16 kV bus to branch 2 breaker"),
        e(f"CB-4160-{x}2", f"TR-480-{x}2", "branch 2 breaker to transformer"),
        e(f"TR-480-{x}2", f"CB-480-{x}2", "branch 2 transformer to low-side breaker"),
        e(f"CB-480-{x}2", f"BUS-480-{x}2", "branch 2 low-side breaker to 480 V bus"),
        e(f"BUS-480-{x}1", f"BUS-480-{x}2", "continuous 480 V bus section with visible tie/junction dots"),
        e(f"BUS-480-{x}1", f"CB-MCC-{x}1", "480 V bus to MCC 1 breaker"),
        e(f"CB-MCC-{x}1", f"MCC-{x}1", "MCC 1 breaker to MCC"),
        e(f"MCC-{x}1", f"PUMP-SI-{x}", "MCC 1 feeder to safety injection pump"),
        e(f"MCC-{x}1", f"PUMP-CCW-{x}", "MCC 1 feeder to CCW pump"),
        e(f"MCC-{x}1", f"FAN-HVAC-{x}", "MCC 1 feeder to HVAC fan"),
        e(f"BUS-480-{x}2", f"CB-MCC-{x}2", "480 V bus to MCC 2 breaker"),
        e(f"CB-MCC-{x}2", f"MCC-{x}2", "MCC 2 breaker to MCC"),
        e(f"MCC-{x}2", f"MOV-RHR-{x}", "MCC 2 feeder to RHR MOV"),
        e(f"BUS-480-{x}2", f"RECT-125-{x}", "480 V bus branch to 125 VDC rectifier"),
        e(f"RECT-125-{x}", f"PANEL-IC-{x}", "rectifier DC output to instrument/control panel"),
    ]


def control_edges() -> list[Edge]:
    result: list[Edge] = []
    for x in TRAINS:
        result.extend(
            [
                e(f"CB-IN-{x}", f"RELAY-27{x}", "dashed undervoltage relay input from incoming breaker"),
                e(f"RELAY-27{x}", f"CB-DG-{x}", "dashed relay interlock to DG breaker"),
                e(f"RELAY-27{x}", "PANEL-SSPS", "dashed relay signal routed to SSPS panel"),
                e(f"MCC-{x}2", f"PANEL-IC-{x}", "dashed instrument/control line from MCC 2 to IC panel"),
            ]
        )
    result.extend(
        [
            e("PANEL-SSPS", "PANEL-RPS-A", "dashed SSPS/RPS interlock route"),
            e("PANEL-SSPS", "PANEL-RPS-B", "dashed SSPS/RPS interlock route"),
        ]
    )
    return result


FINAL_EDGES = (
    top_edges()
    + [edge for x in TRAINS for edge in train_edges(x)]
    + [
        e("BAT-125A", "BUS-DC-125A", "battery A lands on DC bus A"),
        e("BUS-DC-125A", "INV-UPS-A", "DC bus A to inverter/UPS A"),
        e("INV-UPS-A", "PANEL-RPS-A", "UPS A output to RPS A panel"),
        e("BAT-125B", "BUS-DC-125B", "battery B lands on DC bus B"),
        e("BUS-DC-125B", "INV-UPS-B", "DC bus B to inverter/UPS B"),
        e("INV-UPS-B", "PANEL-RPS-B", "UPS B output to RPS B panel"),
        e("ATS-480-A", "PANEL-RPS-A", "visible ATS-AOUT route to RPS A panel"),
        e("ATS-480-B", "PANEL-RPS-B", "visible ATS-BOUT route to RPS B panel"),
    ]
    + control_edges()
)

DIEGO_R1_UNCERTAIN = [
    e("BUS-480-A1", "TIE-A12", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("TIE-A12", "BUS-480-A2", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("BUS-480-B1", "TIE-B12", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("TIE-B12", "BUS-480-B2", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("BUS-480-C1", "TIE-C12", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("TIE-C12", "BUS-480-C2", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("BUS-480-D1", "TIE-D12", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("TIE-D12", "BUS-480-D2", "possible explicit tie-label node on continuous 480 V bus", "uncertain"),
    e("MCC-A1", "ATS-480-A", "possible ATS input-side feeder, source mapping not clean", "uncertain"),
    e("MCC-B1", "ATS-480-A", "possible ATS input-side feeder, source mapping not clean", "uncertain"),
    e("ATS-480-A", "PANEL-RPS-A", "ATS output route to RPS A", "uncertain"),
    e("MCC-C1", "ATS-480-B", "possible ATS input-side feeder, source mapping not clean", "uncertain"),
    e("MCC-D1", "ATS-480-B", "possible ATS input-side feeder, source mapping not clean", "uncertain"),
    e("ATS-480-B", "PANEL-RPS-B", "ATS output route to RPS B", "uncertain"),
    e("PANEL-IC-A", "BUS-DC-125A", "possible DC-A125 route to division A bus", "uncertain"),
    e("PANEL-IC-B", "BUS-DC-125B", "possible DC-B125 route to division B bus", "uncertain"),
    e("PANEL-IC-C", "BUS-DC-125B", "possible DC-C125 route to division B bus", "uncertain"),
    e("PANEL-IC-D", "BUS-DC-125B", "possible DC-D125 route to division B bus", "uncertain"),
    e("PANEL-IC-A", "GND-A", "visible ground reference on DC-A125 conductor", "uncertain"),
    e("PANEL-IC-B", "GND-B", "visible ground reference on DC-B125 conductor", "uncertain"),
    e("PANEL-IC-C", "GND-C", "visible ground reference on DC-C125 conductor", "uncertain"),
    e("PANEL-IC-D", "GND-D", "visible ground reference on DC-D125 conductor", "uncertain"),
]

DIEGO_R1_EDGES = unique_edges(FINAL_EDGES + DIEGO_R1_UNCERTAIN)
FINAL_EDGES = unique_edges(FINAL_EDGES)

EXCLUDED_CASES = [
    "TIE-A12/B12/C12/D12, FDR, LC, BC, 52, 480, NORM, L, ATS-AOUT/BOUT, DC-A125/B125/C125/D125: line/cable/function labels, not standalone components.",
    "ATS-480-A/B input-side mappings: ATS output to RPS panels is visible, but input source mapping to train feeders is ambiguous.",
    "PANEL-IC-X to BUS-DC-125A/B: conductors route through bottom crossings; Diego and Jennifer agreed the named-bus mapping is not reliable enough.",
    "GND-A/B/C/D: visible ground references, excluded from ordinary component connectivity.",
]


def validate(nodes: list[str], edges: list[Edge]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")
    node_set = set(nodes)
    missing = sorted({name for edge in edges for name in (edge.a, edge.b) if name not in node_set})
    if missing:
        raise ValueError(f"edges reference missing nodes: {missing}")


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    index = {name: i for i, name in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in edges:
        i = index[edge.a]
        j = index[edge.b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edge_list(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "status", "evidence"])
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "source": edge.a,
                    "target": edge.b,
                    "status": edge.status,
                    "evidence": edge.evidence,
                }
            )


def estimate_image_tokens(path: Path, detail: str = "high") -> int:
    if detail == "low":
        return 85
    width, height = Image.open(path).size
    scale = min(2048 / width, 2048 / height, 1.0)
    width = math.ceil(width * scale)
    height = math.ceil(height * scale)
    shortest = min(width, height)
    if shortest > 768:
        scale = 768 / shortest
        width = math.ceil(width * scale)
        height = math.ceil(height * scale)
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_total(paths: list[Path]) -> int:
    return sum(estimate_image_tokens(path) for path in paths)


def usage_rows() -> list[dict[str, object]]:
    raw = BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png"
    core_images = [
        raw,
        RESULTS / "raw__top_sources_and_bus_tie.png",
        RESULTS / "raw__train_a_full.png",
        RESULTS / "raw__train_b_full.png",
        RESULTS / "raw__train_c_full.png",
        RESULTS / "raw__train_d_full.png",
        RESULTS / "raw__bottom_dc_control.png",
        RESULTS / "raw__bottom_ssps_ats.png",
        RESULTS / "detected__top_sources_and_bus_tie.png",
        RESULTS / "detected__train_a_full.png",
        RESULTS / "detected__train_b_full.png",
        RESULTS / "detected__train_c_full.png",
        RESULTS / "detected__train_d_full.png",
        RESULTS / "wire_nodes__train_a_full.png",
        RESULTS / "wire_nodes__bottom_dc_control.png",
    ]
    review_images = [
        raw,
        RESULTS / "raw__top_sources_and_bus_tie.png",
        RESULTS / "raw__train_a_full.png",
        RESULTS / "raw__train_b_full.png",
        RESULTS / "raw__train_c_full.png",
        RESULTS / "raw__train_d_full.png",
        RESULTS / "raw__bottom_dc_control.png",
        RESULTS / "raw__bottom_dc_a_rps.png",
        RESULTS / "raw__bottom_ssps_ats.png",
        RESULTS / "raw__bottom_dc_b_rps.png",
        RESULTS / "detected__bottom_dc_control.png",
        RESULTS / "wire_nodes__train_a_full.png",
        RESULTS / "wire_nodes__bottom_dc_control.png",
        RESULTS / "wire_nodes__bottom_ssps_ats.png",
    ]
    main_images = [
        raw,
        BASE / "detected_components_overlay.png",
        BASE / "wire_nodes_overlay.png",
        RESULTS / "raw__top_sources_and_bus_tie.png",
        RESULTS / "raw__train_a_full.png",
        RESULTS / "raw__train_b_full.png",
        RESULTS / "raw__train_c_full.png",
        RESULTS / "raw__train_d_full.png",
        RESULTS / "raw__bottom_dc_control.png",
        RESULTS / "raw__ats_480_a_detail.png",
        RESULTS / "raw__ats_480_b_detail.png",
        RESULTS / "raw__panel_ic_a_to_dc_bus.png",
        RESULTS / "raw__panel_ic_b_to_dc_bus.png",
        RESULTS / "raw__panel_ic_c_to_dc_bus.png",
        RESULTS / "raw__panel_ic_d_to_dc_bus.png",
    ]
    rows = [
        {
            "document": 11,
            "iteration": 1,
            "round": "main-setup",
            "call": "main_01_inventory_crop_visual_inspection",
            "model_response_status": "completed",
            "input_tokens_est": 9000,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(main_images),
            "output_tokens_low": 500,
            "output_tokens_expected": 1000,
            "output_tokens_high": 2000,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed in Codex runtime",
            "notes": "Main-agent setup and visual inspection; no OCR or GT.",
        },
        {
            "document": 11,
            "iteration": 1,
            "round": "Diego R1",
            "call": "subagent_01_diego_high_recall_extraction",
            "model_response_status": "completed",
            "input_tokens_est": 3500,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(core_images),
            "output_tokens_low": 2200,
            "output_tokens_expected": 3600,
            "output_tokens_high": 6500,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "High-recall extraction proposal.",
        },
        {
            "document": 11,
            "iteration": 1,
            "round": "Jennifer R1",
            "call": "subagent_02_jennifer_precision_review",
            "model_response_status": "completed",
            "input_tokens_est": 7000,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": image_total(review_images),
            "output_tokens_low": 2000,
            "output_tokens_expected": 3300,
            "output_tokens_high": 6000,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "Precision review of Diego proposal.",
        },
        {
            "document": 11,
            "iteration": 1,
            "round": "Diego R2",
            "call": "subagent_03_diego_saturation_check",
            "model_response_status": "completed_agreed_final",
            "input_tokens_est": 3200,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": 0,
            "output_tokens_low": 180,
            "output_tokens_expected": 350,
            "output_tokens_high": 800,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed by multi_agent_v1",
            "notes": "Text-only saturation check. Diego agreed with Jennifer.",
        },
        {
            "document": 11,
            "iteration": 1,
            "round": "main-finalization",
            "call": "main_02_artifact_generation_validation_final_response",
            "model_response_status": "completed",
            "input_tokens_est": 6000,
            "cached_input_tokens_est": 0,
            "image_file_tokens_est": 0,
            "output_tokens_low": 600,
            "output_tokens_expected": 1200,
            "output_tokens_high": 2500,
            "reasoning_tokens_est": "",
            "actual_usage_object": "not exposed in Codex runtime",
            "notes": "Local artifact writing and final response.",
        },
    ]
    for row in rows:
        row["input_tokens_low"] = math.ceil(int(row["input_tokens_est"]) * 0.75)
        row["input_tokens_high"] = math.ceil(int(row["input_tokens_est"]) * 1.35)
        row["image_file_tokens_low"] = math.ceil(int(row["image_file_tokens_est"]) * 0.60)
        row["image_file_tokens_high"] = math.ceil(int(row["image_file_tokens_est"]) * 1.40)
        row["total_tokens_low"] = int(row["input_tokens_low"]) + int(row["image_file_tokens_low"]) + int(row["output_tokens_low"])
        row["total_tokens_expected"] = int(row["input_tokens_est"]) + int(row["image_file_tokens_est"]) + int(row["output_tokens_expected"])
        row["total_tokens_high"] = int(row["input_tokens_high"]) + int(row["image_file_tokens_high"]) + int(row["output_tokens_high"])
    return rows


def write_usage() -> None:
    rows = usage_rows()
    fieldnames = [
        "document",
        "iteration",
        "round",
        "call",
        "model_response_status",
        "input_tokens_low",
        "input_tokens_est",
        "input_tokens_high",
        "cached_input_tokens_est",
        "image_file_tokens_low",
        "image_file_tokens_est",
        "image_file_tokens_high",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_est",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_object",
        "notes",
    ]
    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    totals = {
        "document": 11,
        "iteration": 1,
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "responses_input_token_counting_endpoint": "POST /v1/responses/input_tokens",
        "endpoint_called": bool(os.environ.get("OPENAI_API_KEY")),
        "endpoint_status": "Not called because OPENAI_API_KEY is absent." if not os.environ.get("OPENAI_API_KEY") else "API key present; fallback estimates were still recorded.",
        "fallback_method": "Text: local fixed prompt-size estimates. Images: high-detail 512px tile estimate, 85 base + 170 per tile after OpenAI-style resizing.",
        "usage_object_status": "Actual usage objects are not exposed by this Codex multi_agent_v1/tool runtime.",
        "official_reference": "https://platform.openai.com/docs/api-reference/responses/input_tokens",
    }
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(totals, indent=2), encoding="utf-8")
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate\n\n")
        handle.write("No `OPENAI_API_KEY` is available, so the OpenAI Responses input-token counting endpoint was not called.\n")
        handle.write("Official endpoint noted for future runs: `POST /v1/responses/input_tokens`.\n\n")
        handle.write("| Document | Iteration | Low | Expected | High |\n")
        handle.write("|---:|---:|---:|---:|---:|\n")
        handle.write(
            f"| {totals['document']} | {totals['iteration']} | {totals['total_tokens_low']} | "
            f"{totals['total_tokens_expected']} | {totals['total_tokens_high']} |\n\n"
        )
        handle.write("Fallback method: text prompt-size estimates plus image high-detail 512px tile estimates.\n")


def write_round_notes() -> None:
    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Document 11 Round Notes\n\n")
        handle.write("Only resources from `Raw + wires + components + junctions` were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.\n\n")
        handle.write("## Round Sequence\n\n")
        handle.write("1. Diego R1 high-recall extraction proposed top feeders, four train graphs, DC/control nodes, and uncertain ATS/DC/ground candidates.\n")
        handle.write("2. Jennifer R1 removed label-only pseudo-nodes, rejected unsupported ATS input and panel-IC-to-bus mappings, and kept ATS outputs to RPS panels.\n")
        handle.write("3. Diego R2 returned `AGREED_FINAL`; final matrix equals Jennifer R1.\n\n")
        handle.write("## Final Excluded / Ambiguous Cases\n\n")
        for item in EXCLUDED_CASES:
            handle.write(f"- {item}\n")
        handle.write("\n## Final Counts\n\n")
        handle.write(f"- Final nodes: {len(FINAL_NODES)}\n")
        handle.write(f"- Final undirected edges: {len(FINAL_EDGES)}\n")


def write_outputs() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds = [
        ("round_01_diego_high_recall", DIEGO_R1_NODES, DIEGO_R1_EDGES),
        ("round_02_jennifer_precision", FINAL_NODES, FINAL_EDGES),
        ("round_03_diego_agreed", FINAL_NODES, FINAL_EDGES),
        ("final", FINAL_NODES, FINAL_EDGES),
    ]
    for prefix, nodes, edges in rounds:
        validate(nodes, edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)
        write_edge_list(RESULTS / f"{prefix}_edge_list.csv", edges)
        (RESULTS / f"{prefix}_node_list.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")

    write_edge_list(RESULTS / "round_01_diego_uncertain_candidates.csv", DIEGO_R1_UNCERTAIN)
    write_round_notes()
    write_usage()


if __name__ == "__main__":
    write_outputs()
