from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import datetime
from pathlib import Path


DOC_ID = 37
ITERATION = 1
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + components"
)
CODES_DIR = BASE / "codes"
RESULTS_DIR = BASE / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"
MANIFEST_PATH = CROPS_DIR / "crop_manifest.json"


def make_edge(source: str, target: str, kind: str, confidence: str, evidence: str) -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "type": kind,
        "confidence": confidence,
        "evidence": evidence,
    }


FINAL_NODES = [
    "GRID-345",
    "CB-101",
    "CB-102",
    "AUX-TR-1A",
    "AUX-TR-1B",
    "CB-TIE-6K",
    "BUS-6KA",
    "BUS-6KB",
    "CB-103A",
    "CB-103B",
    "SWGR-1EA",
    "SWGR-1EB",
    "DG-1A",
    "CB-DG1A",
    "DG-1B",
    "CB-DG1B",
    "ATS-1A",
    "RELAY-K12A",
    "TR-480A",
    "BUS-480A",
    "MCC-1A",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DCA",
    "INV-120A",
    "BUS-120A",
    "PAN-RPS-A",
    "INST-RACK-A",
    "PUMP-SI-1A",
    "PUMP-RHR-1A",
    "PUMP-CCW-1A",
    "FAN-RB-1A",
    "MOV-HPCI-1A",
    "VALVE-SW-1A",
    "ATS-1B",
    "RELAY-K12B",
    "TR-480B",
    "BUS-480B",
    "MCC-1B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DCB",
    "INV-120B",
    "BUS-120B",
    "PAN-RPS-B",
    "INST-RACK-B",
    "PUMP-SI-1B",
    "PUMP-RHR-1B",
    "PUMP-CCW-1B",
    "FAN-RB-1B",
    "MOV-HPCI-1B",
    "VALVE-SW-1B",
    "PLC-ESF",
]


FINAL_EDGES = [
    make_edge("GRID-345", "CB-101", "power", "high", "solid P01"),
    make_edge("CB-101", "AUX-TR-1A", "power", "high", "solid P02"),
    make_edge("GRID-345", "CB-102", "power", "high", "solid P04"),
    make_edge("CB-102", "AUX-TR-1B", "power", "high", "solid P05"),
    make_edge("AUX-TR-1A", "BUS-6KA", "power", "high", "vertical P03 filled bus tap"),
    make_edge("AUX-TR-1B", "BUS-6KB", "power", "high", "vertical P06 filled bus tap"),
    make_edge("BUS-6KA", "CB-TIE-6K", "power", "high", "solid P07"),
    make_edge("CB-TIE-6K", "BUS-6KB", "power", "high", "solid P08"),
    make_edge("BUS-6KA", "CB-103A", "power", "high", "filled tap"),
    make_edge("CB-103A", "SWGR-1EA", "power", "high", "vertical conductor"),
    make_edge("DG-1A", "CB-DG1A", "power", "high", "solid P09"),
    make_edge("CB-DG1A", "SWGR-1EA", "power", "high", "solid P10"),
    make_edge("BUS-6KB", "CB-103B", "power", "high", "filled tap"),
    make_edge("CB-103B", "SWGR-1EB", "power", "high", "vertical conductor"),
    make_edge("DG-1B", "CB-DG1B", "power", "high", "solid P16"),
    make_edge("CB-DG1B", "SWGR-1EB", "power", "high", "solid P17"),
    make_edge("SWGR-1EA", "ATS-1A", "power", "high", "vertical P13"),
    make_edge("ATS-1A", "TR-480A", "power", "high", "vertical P14"),
    make_edge("TR-480A", "BUS-480A", "power", "high", "vertical P15 filled tap"),
    make_edge("ATS-1A", "RELAY-K12A", "control", "high", "dashed C01"),
    make_edge("SWGR-1EB", "ATS-1B", "power", "high", "vertical P20"),
    make_edge("ATS-1B", "TR-480B", "power", "high", "vertical P21"),
    make_edge("TR-480B", "BUS-480B", "power", "high", "vertical P22 filled tap"),
    make_edge("ATS-1B", "RELAY-K12B", "control", "high", "dashed C04"),
    make_edge("RELAY-K12B", "PLC-ESF", "control", "medium", "dashed C05 routed to PLC-ESF/ESF logic area"),
    make_edge("BUS-480A", "MCC-1A", "power", "high", "vertical P23 filled tap"),
    make_edge("BUS-480A", "CHGR-125A", "power", "high", "vertical P37 filled tap"),
    make_edge("MCC-1A", "PUMP-SI-1A", "power", "high", "vertical P24"),
    make_edge("MCC-1A", "PUMP-RHR-1A", "power", "high", "vertical P25"),
    make_edge("MCC-1A", "PUMP-CCW-1A", "power", "high", "vertical P26"),
    make_edge("MCC-1A", "FAN-RB-1A", "power", "high", "vertical P27"),
    make_edge("MCC-1A", "MOV-HPCI-1A", "power", "high", "vertical P28"),
    make_edge("MCC-1A", "VALVE-SW-1A", "power", "high", "vertical P29"),
    make_edge("CHGR-125A", "BUS-125DCA", "dc-power", "high", "vertical P38"),
    make_edge("BAT-125A", "BUS-125DCA", "dc-power", "high", "vertical P39"),
    make_edge("BUS-125DCA", "INV-120A", "dc-power", "high", "filled tap to inverter"),
    make_edge("INV-120A", "BUS-120A", "ac-power", "high", "vertical P41"),
    make_edge("BUS-120A", "PAN-RPS-A", "ac-power", "high", "solid P42 tap"),
    make_edge("BUS-120A", "INST-RACK-A", "ac-power", "high", "solid P43 tap"),
    make_edge("PAN-RPS-A", "INST-RACK-A", "control", "medium", "dashed C03 functional route"),
    make_edge("BUS-480B", "MCC-1B", "power", "high", "vertical P30 filled tap"),
    make_edge("BUS-480B", "CHGR-125B", "power", "high", "vertical P44 filled tap"),
    make_edge("MCC-1B", "PUMP-SI-1B", "power", "high", "vertical P31"),
    make_edge("MCC-1B", "PUMP-RHR-1B", "power", "high", "vertical P32"),
    make_edge("MCC-1B", "PUMP-CCW-1B", "power", "high", "vertical P33"),
    make_edge("MCC-1B", "FAN-RB-1B", "power", "high", "vertical P34"),
    make_edge("MCC-1B", "MOV-HPCI-1B", "power", "high", "vertical P35"),
    make_edge("MCC-1B", "VALVE-SW-1B", "power", "high", "vertical P36"),
    make_edge("CHGR-125B", "BUS-125DCB", "dc-power", "high", "vertical P45"),
    make_edge("BAT-125B", "BUS-125DCB", "dc-power", "high", "vertical P46"),
    make_edge("BUS-125DCB", "INV-120B", "dc-power", "high", "filled tap to inverter"),
    make_edge("INV-120B", "BUS-120B", "ac-power", "high", "vertical P48"),
    make_edge("BUS-120B", "PAN-RPS-B", "ac-power", "high", "solid P49 tap"),
    make_edge("BUS-120B", "INST-RACK-B", "ac-power", "high", "solid P50 tap"),
    make_edge("PLC-ESF", "PAN-RPS-B", "control", "medium", "dashed C06 functional route"),
]


ROUND1_RENAME = {
    "GRID-345": "SOURCE-3PH",
    "CB-TIE-6K": "CB-TIE-6KA-6KB",
}


def renamed(name: str) -> str:
    return ROUND1_RENAME.get(name, name)


ROUND1_NODES = [renamed(node) for node in FINAL_NODES]
ROUND1_NODES.insert(25, "GND-01A")
ROUND1_NODES.insert(44, "GND-01B")

ROUND1_EDGES = [
    make_edge(
        renamed(edge["source"]),
        renamed(edge["target"]),
        edge["type"],
        edge["confidence"],
        edge["evidence"],
    )
    for edge in FINAL_EDGES
]
ROUND1_EDGES.extend(
    [
        make_edge("BUS-125DCA", "GND-01A", "reference", "low", "G01 ground/reference symbol near DC bus"),
        make_edge("BUS-125DCB", "GND-01B", "reference", "low", "G02 ground/reference symbol near DC bus"),
        make_edge("PAN-RPS-A", "PLC-ESF", "control", "low", "high-recall C03/central dashed routing candidate"),
        make_edge("INST-RACK-A", "PLC-ESF", "control", "low", "high-recall C03/central dashed routing candidate"),
        make_edge("INST-RACK-B", "PLC-ESF", "control", "low", "high-recall C06/B-side dashed routing candidate"),
    ]
)


ROUND_DATA = [
    {
        "prefix": "round_01_diego",
        "agent": "Diego",
        "role": "high-recall extractor",
        "nodes": ROUND1_NODES,
        "edges": ROUND1_EDGES,
        "note": (
            "Initial high-recall graph reconstructed from the Diego round summary. "
            "It intentionally preserves plausible but later rejected ground/reference nodes "
            "and A/B control overconnections."
        ),
    },
    {
        "prefix": "round_02_jennifer",
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "note": (
            "Jennifer renamed SOURCE-3PH to GRID-345, renamed the tie breaker to CB-TIE-6K, "
            "excluded GND-01A/GND-01B as matrix nodes, removed unsupported PLC overconnections, "
            "and retained three medium-confidence control edges."
        ),
    },
    {
        "prefix": "round_03_diego",
        "agent": "Diego",
        "role": "high-recall reconciliation",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "note": "Diego agreed exactly with Jennifer's refinement: 53 nodes and 55 edges.",
    },
    {
        "prefix": "round_04_jennifer_final",
        "agent": "Jennifer",
        "role": "precision final saturation check",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "note": (
            "Jennifer confirmed saturation. RELAY-K12B--PLC-ESF remains medium confidence via C05; "
            "GND-01A/GND-01B remain excluded as reference/ground annotations."
        ),
    },
]


UNCERTAIN_OR_EXCLUDED = [
    {
        "source": "BUS-125DCA",
        "target": "GND-01A",
        "status": "excluded",
        "reason": "DC reference/ground annotation, not equipment/node for this matrix.",
    },
    {
        "source": "BUS-125DCB",
        "target": "GND-01B",
        "status": "excluded",
        "reason": "DC reference/ground annotation, not equipment/node for this matrix.",
    },
    {
        "source": "PAN-RPS-A",
        "target": "PLC-ESF",
        "status": "excluded",
        "reason": "A-side dashed C03 route supports PAN-RPS-A--INST-RACK-A rather than a clear PLC landing.",
    },
    {
        "source": "INST-RACK-A",
        "target": "PLC-ESF",
        "status": "excluded",
        "reason": "No crisp visual terminal landing to PLC-ESF; C03 is treated as the A-side panel/rack functional route.",
    },
    {
        "source": "INST-RACK-B",
        "target": "PLC-ESF",
        "status": "excluded",
        "reason": "No supported B-side instrument-rack-to-PLC dashed route; C06 supports PLC-ESF--PAN-RPS-B.",
    },
    {
        "source": "PAN-RPS-B",
        "target": "INST-RACK-B",
        "status": "excluded",
        "reason": "No dashed route visually supports this pair; both receive 120 VAC from BUS-120B separately.",
    },
    {
        "source": "RELAY-K12B",
        "target": "PLC-ESF",
        "status": "included_medium_confidence",
        "reason": "C05 visibly routes from RELAY-K12B down toward the PLC-ESF/ESF logic area; endpoint is functional/diagrammatic.",
    },
    {
        "source": "PLC-ESF",
        "target": "PAN-RPS-B",
        "status": "included_medium_confidence",
        "reason": "C06 functional dashed route to RPS Panel B.",
    },
    {
        "source": "PAN-RPS-A",
        "target": "INST-RACK-A",
        "status": "included_medium_confidence",
        "reason": "C03 functional dashed route under the A-side RPS panel and instrument rack.",
    },
]


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def validate_graph(nodes: list[str], edges: list[dict[str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")
    node_set = set(nodes)
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        if edge["source"] not in node_set or edge["target"] not in node_set:
            raise ValueError(f"edge references missing node: {edge}")
        key = edge_key(edge["source"], edge["target"])
        if key in seen:
            raise ValueError(f"duplicate undirected edge: {edge}")
        seen.add(key)


def write_edges_csv(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "type", "confidence", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix_csv(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    adjacency = {edge_key(edge["source"], edge["target"]) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(edge_key(row_node, col_node) in adjacency))
            writer.writerow(row)


def write_nodes_csv(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes, start=1):
            writer.writerow([index, node])


def crop_sizes() -> dict[str, tuple[int, int]]:
    if not MANIFEST_PATH.exists():
        return {}
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {crop["file"]: tuple(crop["size"]) for crop in manifest.get("crops", [])}


def estimate_image_tokens(file_names: list[str], sizes: dict[str, tuple[int, int]]) -> int:
    total = 0
    for name in file_names:
        size = sizes.get(name)
        if not size:
            continue
        width, height = size
        total += 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)
    return total


def estimate_text_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def build_token_usage_rows() -> list[dict[str, object]]:
    sizes = crop_sizes()
    diego_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "focus_top_distribution_raw.png",
        "focus_top_distribution_wires_overlay.png",
        "focus_middle_distribution_raw.png",
        "focus_middle_distribution_wires_overlay.png",
        "focus_lower_distribution_raw.png",
        "focus_lower_distribution_wires_overlay.png",
        "focus_bottom_controls_raw.png",
        "focus_bottom_controls_wires_overlay.png",
    ]
    jennifer_images = [
        "raw_full_thumb.png",
        "focus_top_distribution_raw.png",
        "focus_middle_distribution_raw.png",
        "focus_lower_distribution_raw.png",
        "focus_bottom_controls_raw.png",
        "focus_bottom_controls_wires_overlay.png",
        "detail_01_raw.png",
        "detail_02_raw.png",
        "detail_05_raw.png",
        "detail_06_raw.png",
        "detail_08_raw.png",
        "detail_11_raw.png",
        "detail_12_raw.png",
        "detail_13_raw.png",
        "detail_15_raw.png",
        "detail_16_raw.png",
        "detail_17_raw.png",
        "detail_18_raw.png",
        "detail_19_raw.png",
        "detail_20_raw.png",
        "detail_21_raw.png",
        "detail_22_raw.png",
        "detail_22_wires_overlay.png",
        "detail_22_components.png",
    ]
    calls = [
        {
            "round": "main_preparation",
            "call_id": "main-01",
            "agent": "Main",
            "purpose": "Inspect folder, create visual crops, view selected raw/wire/component crops, orchestrate agents.",
            "text": "Main agent preparation and local visual review.",
            "text_tokens_est": 3500,
            "images": ["raw_full_thumb.png", "focus_bottom_controls_raw.png", "detail_22_raw.png"],
            "cached": 0,
            "output_low": 300,
            "output_expected": 650,
            "output_high": 1200,
        },
        {
            "round": "round_01",
            "call_id": "diego-r1",
            "agent": "Diego",
            "purpose": "High-recall extraction from raw schematic and derived visual aids.",
            "text": "Diego high-recall prompt with workflow rules, folder constraints, crop references, and requested evidence.",
            "text_tokens_est": 2200,
            "images": diego_images,
            "cached": 0,
            "output_low": 1500,
            "output_expected": 2600,
            "output_high": 4200,
        },
        {
            "round": "round_02",
            "call_id": "jennifer-r2",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego round 1 proposal and visual evidence.",
            "text": "Jennifer precision prompt plus Diego node/edge proposal and targeted ambiguity questions.",
            "text_tokens_est": 4800,
            "images": jennifer_images,
            "cached": 0,
            "output_low": 1200,
            "output_expected": 2200,
            "output_high": 3600,
        },
        {
            "round": "round_03",
            "call_id": "diego-r3",
            "agent": "Diego",
            "purpose": "Reconcile Jennifer refinement and check for missed high-recall edges.",
            "text": "Jennifer refined graph sent back to Diego for saturation check.",
            "text_tokens_est": 3800,
            "images": [],
            "cached": 22000,
            "output_low": 40,
            "output_expected": 80,
            "output_high": 250,
        },
        {
            "round": "round_04",
            "call_id": "jennifer-r4",
            "agent": "Jennifer",
            "purpose": "Final precision saturation check after Diego agreement.",
            "text": "Diego agreement plus request to confirm final nodes/edges and revisit C05 and grounds.",
            "text_tokens_est": 1200,
            "images": [],
            "cached": 32000,
            "output_low": 900,
            "output_expected": 1700,
            "output_high": 2800,
        },
        {
            "round": "main_writeup",
            "call_id": "main-02",
            "agent": "Main",
            "purpose": "Write round artifacts, final matrix, and concise final response.",
            "text": "Main agent result-writing code, final edge list, token ledger, and final response.",
            "text_tokens_est": 2500,
            "images": [],
            "cached": 0,
            "output_low": 250,
            "output_expected": 550,
            "output_high": 1000,
        },
    ]
    rows = []
    for call in calls:
        text_tokens = int(call.get("text_tokens_est", estimate_text_tokens(call["text"])))
        image_tokens = estimate_image_tokens(call["images"], sizes)
        cached = int(call["cached"])
        input_expected = text_tokens + image_tokens + cached
        rows.append(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "round": call["round"],
                "call_id": call["call_id"],
                "agent": call["agent"],
                "purpose": call["purpose"],
                "input_text_tokens_est": text_tokens,
                "cached_input_tokens_est": cached,
                "input_image_file_tokens_est": image_tokens,
                "input_total_tokens_est": input_expected,
                "output_tokens_low": call["output_low"],
                "output_tokens_expected": call["output_expected"],
                "output_tokens_high": call["output_high"],
                "reasoning_tokens_recorded": "",
                "total_tokens_low": input_expected + call["output_low"],
                "total_tokens_expected": input_expected + call["output_expected"],
                "total_tokens_high": input_expected + call["output_high"],
                "usage_object_available": False,
                "counting_method": "local estimate: text chars/4 plus image tiles 85 + 170*ceil(w/512)*ceil(h/512)",
                "notes": "Responses token-count endpoint and actual usage objects unavailable without API key/tool exposure.",
            }
        )
    return rows


def write_token_usage(rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys())
    with (RESULTS_DIR / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    totals = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "calls": len(rows),
        "input_text_tokens_est": sum(int(row["input_text_tokens_est"]) for row in rows),
        "cached_input_tokens_est": sum(int(row["cached_input_tokens_est"]) for row in rows),
        "input_image_file_tokens_est": sum(int(row["input_image_file_tokens_est"]) for row in rows),
        "input_total_tokens_est": sum(int(row["input_total_tokens_est"]) for row in rows),
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "actual_usage_available": False,
        "responses_counting_endpoint_used": False,
        "why_endpoint_not_used": "No API key was available in this environment.",
    }
    with (RESULTS_DIR / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(totals.keys()))
        writer.writeheader()
        writer.writerow(totals)
    (RESULTS_DIR / "token_usage_summary.json").write_text(json.dumps(totals, indent=2), encoding="utf-8")


def write_uncertain_or_excluded() -> None:
    with (RESULTS_DIR / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "status", "reason"])
        writer.writeheader()
        writer.writerows(UNCERTAIN_OR_EXCLUDED)


def write_round_notes(round_info: dict[str, object]) -> None:
    prefix = str(round_info["prefix"])
    nodes = round_info["nodes"]
    edges = round_info["edges"]
    text = "\n".join(
        [
            f"# {prefix}",
            "",
            f"Document: {DOC_ID}",
            f"Iteration: {ITERATION}",
            f"Agent: {round_info['agent']}",
            f"Role: {round_info['role']}",
            f"Node count: {len(nodes)}",
            f"Edge count: {len(edges)}",
            "",
            str(round_info["note"]),
            "",
            "Ground truth and validation/feedback files were not used for this extraction.",
            "",
        ]
    )
    (RESULTS_DIR / f"{prefix}_notes.md").write_text(text, encoding="utf-8")


def write_report(token_rows: list[dict[str, object]]) -> None:
    high_edges = sum(1 for edge in FINAL_EDGES if edge["confidence"] == "high")
    medium_edges = sum(1 for edge in FINAL_EDGES if edge["confidence"] == "medium")
    token_expected = sum(int(row["total_tokens_expected"]) for row in token_rows)
    token_low = sum(int(row["total_tokens_low"]) for row in token_rows)
    token_high = sum(int(row["total_tokens_high"]) for row in token_rows)
    lines = [
        "# Document 37 Connectivity Extraction",
        "",
        "Final saturated result from Diego and Jennifer, using only Input resources/raw and derived visual aids.",
        "",
        f"- Final nodes: {len(FINAL_NODES)}",
        f"- Final edges: {len(FINAL_EDGES)}",
        f"- High-confidence edges: {high_edges}",
        f"- Medium-confidence edges: {medium_edges}",
        "- Excluded ground/reference labels: GND-01A, GND-01B",
        "- GT/validation/feedback files: not used",
        "- Off-the-shelf OCR: not used",
        "",
        "## Final Medium-Confidence Edges",
        "",
    ]
    for edge in FINAL_EDGES:
        if edge["confidence"] == "medium":
            lines.append(f"- {edge['source']} -- {edge['target']}: {edge['evidence']}")
    lines.extend(
        [
            "",
            "## Token Usage Estimate",
            "",
            "Actual OpenAI usage objects and Responses input-token counting were unavailable because no API key "
            "or usage-returning model-call interface was available in this environment.",
            "",
            f"- Low estimate: {token_low}",
            f"- Expected estimate: {token_expected}",
            f"- High estimate: {token_high}",
            "",
            "Local estimate method: text tokens are approximated as characters/4; image/file input tokens use "
            "85 + 170 * ceil(width/512) * ceil(height/512) per image crop.",
            "",
            "## Main Output Files",
            "",
            "- final_connectivity_matrix.csv",
            "- final_edges.csv",
            "- final_node_order.csv",
            "- round_01_diego_matrix.csv through round_04_jennifer_final_matrix.csv",
            "- token_usage_estimate.csv",
            "- token_usage_summary.csv/json",
            "- uncertain_or_excluded_edges.csv",
            "",
        ]
    )
    (RESULTS_DIR / "extraction_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_summary(token_rows: list[dict[str, object]]) -> None:
    high_edges = sum(1 for edge in FINAL_EDGES if edge["confidence"] == "high")
    medium_edges = sum(1 for edge in FINAL_EDGES if edge["confidence"] == "medium")
    summary = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "resource_location": str(BASE),
        "codes_dir": str(CODES_DIR),
        "results_dir": str(RESULTS_DIR),
        "final_node_count": len(FINAL_NODES),
        "final_edge_count": len(FINAL_EDGES),
        "high_confidence_edge_count": high_edges,
        "medium_confidence_edge_count": medium_edges,
        "agents": [
            {"name": "Diego", "role": "high-recall extractor"},
            {"name": "Jennifer", "role": "precision reviewer/refiner"},
        ],
        "rounds": [
            {
                "round": round_info["prefix"],
                "agent": round_info["agent"],
                "node_count": len(round_info["nodes"]),
                "edge_count": len(round_info["edges"]),
            }
            for round_info in ROUND_DATA
        ],
        "final_files": {
            "matrix": str(RESULTS_DIR / "final_connectivity_matrix.csv"),
            "edges": str(RESULTS_DIR / "final_edges.csv"),
            "node_order": str(RESULTS_DIR / "final_node_order.csv"),
            "report": str(RESULTS_DIR / "extraction_report.md"),
            "token_usage": str(RESULTS_DIR / "token_usage_estimate.csv"),
        },
        "actual_usage_available": False,
        "responses_counting_endpoint_used": False,
        "token_usage_expected_total": sum(int(row["total_tokens_expected"]) for row in token_rows),
        "extraction_constraints": {
            "gt_or_feedback_used": False,
            "off_the_shelf_ocr_used": False,
            "allowed_inputs": [
                "raw schematic image",
                "detected components/logical overlay",
                "wires mask",
                "wires mask overlay",
                "visual crops made from those images",
            ],
        },
    }
    (RESULTS_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CODES_DIR.mkdir(parents=True, exist_ok=True)

    validate_graph(FINAL_NODES, FINAL_EDGES)
    assert len(FINAL_NODES) == 53
    assert len(FINAL_EDGES) == 55

    for round_info in ROUND_DATA:
        nodes = round_info["nodes"]
        edges = round_info["edges"]
        validate_graph(nodes, edges)
        prefix = round_info["prefix"]
        write_nodes_csv(RESULTS_DIR / f"{prefix}_node_order.csv", nodes)
        write_edges_csv(RESULTS_DIR / f"{prefix}_edges.csv", edges)
        write_matrix_csv(RESULTS_DIR / f"{prefix}_matrix.csv", nodes, edges)
        write_round_notes(round_info)

    write_nodes_csv(RESULTS_DIR / "final_node_order.csv", FINAL_NODES)
    write_edges_csv(RESULTS_DIR / "final_edges.csv", FINAL_EDGES)
    write_matrix_csv(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_uncertain_or_excluded()

    token_rows = build_token_usage_rows()
    write_token_usage(token_rows)
    write_report(token_rows)
    write_summary(token_rows)

    shutil.copy2(Path(__file__), CODES_DIR / "write_doc37_results.py")
    print(f"wrote final matrix with {len(FINAL_NODES)} nodes and {len(FINAL_EDGES)} edges")
    print(f"results: {RESULTS_DIR}")
    print(f"codes copy: {CODES_DIR / 'write_doc37_results.py'}")


if __name__ == "__main__":
    main()
