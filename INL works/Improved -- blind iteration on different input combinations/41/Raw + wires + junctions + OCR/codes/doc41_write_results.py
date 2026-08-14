from __future__ import annotations

import csv
import json
import math
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # noqa: BLE001
    tiktoken = None


DOCUMENT = "41"
ITERATION = "1"
MODEL = "gpt-5.5"
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires + junctions + OCR"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = BASE / "precision_review_crops"
ROUND_RE = re.compile(rf"document{DOCUMENT}_round(?P<round>\d+)_(?P<agent>diego|jennifer)_edges\.csv$", re.I)

DIEGO_ROUND01_NODES_CSV = """node,component_type,node_kind
OFFSITE-A,source,physical_component
TR-1A,transformer,physical_component
GND-1E,ground_reference,logical_node
CB-101,breaker,physical_component
BUS-1A-4.16KV,bus,logical_node
EDG-1A,generator,physical_component
CB-105,breaker,physical_component
CB-TIE-1AB,tie_breaker,physical_component
BUS-1B-4.16KV,bus,logical_node
CB-102,breaker,physical_component
TR-1B,transformer,physical_component
OFFSITE-B,source,physical_component
EDG-1B,generator,physical_component
CB-106,breaker,physical_component
TR-LC-1A,transformer,physical_component
CB-201,breaker,physical_component
BUS-480A,bus,logical_node
TR-SAF-1A,transformer,physical_component
CB-203,breaker,physical_component
BUS-480E1A,bus,logical_node
TR-LC-1B,transformer,physical_component
CB-202,breaker,physical_component
BUS-480B,bus,logical_node
TR-SAF-1B,transformer,physical_component
CB-204,breaker,physical_component
BUS-480E1B,bus,logical_node
MCC-1A,motor_control_center,physical_component
MCC-1C,motor_control_center,physical_component
MCC-ESS-A,motor_control_center,physical_component
PUMP-CCW-103A,pump_motor,physical_component
FAN-CRHV-104A,fan_motor,physical_component
PUMP-SI-101A,pump_motor,physical_component
PUMP-RHR-102A,pump_motor,physical_component
MOV-1201A,motor_operated_valve,physical_component
MCC-1B,motor_control_center,physical_component
MCC-1D,motor_control_center,physical_component
MCC-ESS-B,motor_control_center,physical_component
PUMP-CCW-103B,pump_motor,physical_component
FAN-CRHV-104B,fan_motor,physical_component
PUMP-SI-101B,pump_motor,physical_component
PUMP-RHR-102B,pump_motor,physical_component
MOV-1201B,motor_operated_valve,physical_component
RELAY-K86A,relay,physical_component
RELAY-K86B,relay,physical_component
JB-ESF-01,junction_box,physical_component
PANEL-RPS-A,panel,physical_component
PANEL-RPS-B,panel,physical_component
CHGR-125A,charger,physical_component
DC-BUS-125A,dc_bus,logical_node
BAT-125A,battery,physical_component
INV-120A,inverter,physical_component
UPS-BUS-A,ups_bus,logical_node
INST-RACK-1,instrument_rack,physical_component
CHGR-125B,charger,physical_component
DC-BUS-125B,dc_bus,logical_node
BAT-125B,battery,physical_component
INV-120B,inverter,physical_component
UPS-BUS-B,ups_bus,logical_node
"""

DIEGO_ROUND01_EDGES_CSV = """source,target,edge_kind,confidence,evidence
OFFSITE-A,TR-1A,power_feeder,high,Solid feeder from OFFSITE-A to TR-1A primary.
TR-1A,CB-101,power_feeder,high,Solid feeder from TR-1A secondary to CB-101.
TR-1A,GND-1E,grounding_reference,medium,Ground/reference symbol visibly connected below TR-1A; included for high recall.
CB-101,BUS-1A-4.16KV,power_feeder,high,CB-101 output connects to BUS-1A.
EDG-1A,CB-105,power_feeder,high,EDG A incoming feeder to CB-105.
CB-105,BUS-1A-4.16KV,power_feeder,high,CB-105 output rises to BUS-1A.
BUS-1A-4.16KV,CB-TIE-1AB,power_feeder_normally_open_tie,high,BUS-1A connects to N.O. tie breaker.
CB-TIE-1AB,BUS-1B-4.16KV,power_feeder_normally_open_tie,high,Tie breaker connects to BUS-1B terminal.
BUS-1B-4.16KV,CB-102,power_feeder,high,BUS-1B connects to CB-102.
CB-102,TR-1B,power_feeder,high,CB-102 connects to TR-1B secondary.
TR-1B,OFFSITE-B,power_feeder,high,TR-1B primary connects to OFFSITE-B.
EDG-1B,CB-106,power_feeder,high,EDG B incoming feeder to CB-106.
CB-106,BUS-1B-4.16KV,power_feeder,high,CB-106 output rises to BUS-1B.
CB-105,RELAY-K86A,control_interlock,high,Dashed lockout/control path from CB-105 to Train A 86 relay path.
CB-106,RELAY-K86B,control_interlock,high,Dashed lockout/control path from CB-106 to Train B 86 relay path.
BUS-1A-4.16KV,TR-LC-1A,power_feeder,high,Vertical tap from BUS-1A to TR-LC-1A.
BUS-1A-4.16KV,TR-SAF-1A,power_feeder,high,Vertical tap from BUS-1A to TR-SAF-1A.
BUS-1B-4.16KV,TR-LC-1B,power_feeder,high,Vertical tap from BUS-1B to TR-LC-1B.
BUS-1B-4.16KV,TR-SAF-1B,power_feeder,high,Vertical tap from BUS-1B to TR-SAF-1B.
TR-LC-1A,CB-201,power_feeder,high,TR-LC-1A low side feeds CB-201.
CB-201,BUS-480A,power_feeder,high,CB-201 output feeds BUS-480A.
TR-SAF-1A,CB-203,power_feeder,high,TR-SAF-1A low side feeds CB-203.
CB-203,BUS-480E1A,power_feeder,high,CB-203 output feeds BUS-480E1A.
TR-LC-1B,CB-202,power_feeder,high,TR-LC-1B low side feeds CB-202.
CB-202,BUS-480B,power_feeder,high,CB-202 output feeds BUS-480B.
TR-SAF-1B,CB-204,power_feeder,high,TR-SAF-1B low side feeds CB-204.
CB-204,BUS-480E1B,power_feeder,high,CB-204 output feeds BUS-480E1B.
BUS-480A,MCC-1A,power_feeder,high,Vertical feeder from BUS-480A to MCC-1A.
BUS-480A,MCC-1C,power_feeder,high,Vertical feeder from BUS-480A to MCC-1C.
BUS-480A,CHGR-125A,power_feeder,medium,CABLE 1A-480-7 route from BUS-480A to charger input.
BUS-480E1A,MCC-ESS-A,power_feeder,high,Vertical feeder from BUS-480E1A to MCC-ESS-A.
MCC-1A,PUMP-CCW-103A,power_feeder,high,Solid feeder from MCC-1A to pump motor.
MCC-1C,FAN-CRHV-104A,power_feeder,high,Solid feeder from MCC-1C to fan motor.
MCC-ESS-A,PUMP-SI-101A,power_feeder,high,MCC-ESS-A output feeds SI pump.
MCC-ESS-A,PUMP-RHR-102A,power_feeder,high,MCC-ESS-A output feeds RHR pump.
MCC-ESS-A,MOV-1201A,power_feeder,high,MCC-ESS-A output feeds MOV-1201A.
BUS-480B,MCC-1B,power_feeder,high,Vertical feeder from BUS-480B to MCC-1B.
BUS-480B,MCC-1D,power_feeder,high,Vertical feeder from BUS-480B to MCC-1D.
BUS-480E1B,MCC-ESS-B,power_feeder,high,Vertical feeder from BUS-480E1B to MCC-ESS-B.
BUS-480E1B,CHGR-125B,power_feeder,medium,CABLE 1B-480-9 route from BUS-480E1B area to charger input.
MCC-1B,PUMP-CCW-103B,power_feeder,high,Solid feeder from MCC-1B to pump motor.
MCC-1D,FAN-CRHV-104B,power_feeder,high,Solid feeder from MCC-1D to fan motor.
MCC-ESS-B,PUMP-SI-101B,power_feeder,high,MCC-ESS-B output feeds SI pump.
MCC-ESS-B,PUMP-RHR-102B,power_feeder,high,MCC-ESS-B output feeds RHR pump.
MCC-ESS-B,MOV-1201B,power_feeder,high,MCC-ESS-B output feeds MOV-1201B.
CHGR-125A,DC-BUS-125A,dc_power,high,Charger DC output connects to DC-BUS-125A.
BAT-125A,DC-BUS-125A,dc_power,high,Battery connects to DC-BUS-125A.
DC-BUS-125A,INV-120A,dc_power,high,DC-BUS-125A connects to inverter input.
INV-120A,UPS-BUS-A,ac_power,high,INV-120A output connects to UPS-BUS-A.
UPS-BUS-A,PANEL-RPS-A,ac_power,high,Solid feeder from UPS-BUS-A to PANEL-RPS-A.
UPS-BUS-A,INST-RACK-1,ac_power,high,UPS-BUS-A right terminal feeds INST-RACK-1.
RELAY-K86A,PANEL-RPS-A,control_interlock,high,Dashed control path from relay to panel.
PANEL-RPS-A,JB-ESF-01,control_interlock,high,Dashed control path from panel to JB-ESF-01.
CHGR-125B,DC-BUS-125B,dc_power,high,Charger DC output connects to DC-BUS-125B.
BAT-125B,DC-BUS-125B,dc_power,high,Battery connects to DC-BUS-125B.
DC-BUS-125B,INV-120B,dc_power,high,DC-BUS-125B connects to inverter input.
INV-120B,UPS-BUS-B,ac_power,high,INV-120B output connects to UPS-BUS-B.
UPS-BUS-B,PANEL-RPS-B,ac_power,high,Solid feeder from UPS-BUS-B to PANEL-RPS-B.
RELAY-K86B,PANEL-RPS-B,control_interlock,high,Dashed control path from relay to panel.
PANEL-RPS-B,JB-ESF-01,control_interlock,high,Dashed control path from panel to JB-ESF-01.
"""


def text_tokens(text: str) -> int:
    if not text:
        return 0
    if tiktoken is not None:
        try:
            return len(tiktoken.get_encoding("o200k_base").encode(text))
        except Exception:  # noqa: BLE001
            pass
    return math.ceil(len(text) / 4)


def file_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    return text_tokens(path.read_text(encoding="utf-8", errors="ignore"))


def image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    with Image.open(path) as image:
        width, height = image.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    short = min(width, height)
    if short > 768:
        scale2 = 768 / short
        width *= scale2
        height *= scale2
    return 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def node_name(row: dict[str, str]) -> str:
    return (row.get("node") or row.get("name") or row.get("final_label") or "").strip()


def include_node(row: dict[str, str]) -> bool:
    decision = (row.get("decision") or "include").strip().lower()
    return bool(node_name(row)) and decision not in {"exclude", "reject", "rejected", "remove", "removed"}


def include_edge(row: dict[str, str]) -> bool:
    action = (row.get("round_action") or row.get("decision") or "include").strip().lower()
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    return bool(source and target and source != target and action not in {"exclude", "reject", "rejected", "remove", "removed"})


def pair(row: dict[str, str]) -> tuple[str, str]:
    return tuple(sorted(((row.get("source") or "").strip(), (row.get("target") or "").strip())))


def edge_label(edge: tuple[str, str]) -> str:
    return f"{edge[0]} -- {edge[1]}"


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path: Path, nodes: list[str], pairs: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in pairs:
        if source in index and target in index and source != target:
            matrix[index[source]][index[target]] = 1
            matrix[index[target]][index[source]] = 1
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])
    return matrix


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return None
    nodes = rows[0][1:]
    row_names = [row[0] for row in rows[1:] if row]
    matrix = [[int(value) for value in row[1:]] for row in rows[1:] if row]
    if row_names != nodes:
        raise ValueError(f"matrix row/header mismatch in {path}")
    return nodes, matrix


def load_graph(prefix: str) -> dict[str, object]:
    edge_rows = read_rows(RESULTS / f"{prefix}_edges.csv")
    node_rows = read_rows(RESULTS / f"{prefix}_nodes.csv")
    nodes: list[str] = []
    seen: set[str] = set()
    for row in node_rows:
        node = node_name(row)
        if include_node(row) and node not in seen:
            nodes.append(node)
            seen.add(node)
    included = [row for row in edge_rows if include_edge(row)]
    for row in included:
        for node in ((row.get("source") or "").strip(), (row.get("target") or "").strip()):
            if node and node not in seen:
                nodes.append(node)
                seen.add(node)
    pairs = [pair(row) for row in included]
    return {
        "prefix": prefix,
        "edge_rows": edge_rows,
        "node_rows": node_rows,
        "nodes": nodes,
        "node_set": set(nodes),
        "included": included,
        "pairs": pairs,
        "unique_pairs": sorted(set(pairs)),
        "matrix_path": RESULTS / f"{prefix}_adjacency_matrix.csv",
    }


def validate(graph: dict[str, object]) -> dict[str, object]:
    nodes: list[str] = graph["nodes"]  # type: ignore[assignment]
    node_set: set[str] = graph["node_set"]  # type: ignore[assignment]
    included: list[dict[str, str]] = graph["included"]  # type: ignore[assignment]
    pairs: list[tuple[str, str]] = graph["pairs"]  # type: ignore[assignment]
    unique_pairs: list[tuple[str, str]] = graph["unique_pairs"]  # type: ignore[assignment]
    matrix = [[0 for _ in nodes] for _ in nodes]
    index = {node: i for i, node in enumerate(nodes)}
    for source, target in unique_pairs:
        if source in index and target in index:
            matrix[index[source]][index[target]] = 1
            matrix[index[target]][index[source]] = 1
    unknown = []
    for row in included:
        missing = [n for n in ((row.get("source") or "").strip(), (row.get("target") or "").strip()) if n not in node_set]
        if missing:
            unknown.append({"source": row.get("source"), "target": row.get("target"), "missing": missing})
    duplicates = sorted(edge for edge, count in Counter(pairs).items() if count > 1)
    diagonal = [nodes[i] for i, row in enumerate(matrix) if row[i]]
    asymmetric = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                asymmetric.append([nodes[i], nodes[j]])
    existing_matches = False
    existing_error = None
    try:
        existing_matches = read_matrix(graph["matrix_path"]) == (nodes, matrix)
    except Exception as exc:  # noqa: BLE001
        existing_error = str(exc)
    edge_kind_counts = Counter(
        (row.get("edge_kind") or row.get("type") or "unspecified").strip() or "unspecified" for row in included
    )
    confidence_counts = Counter((row.get("confidence") or "unspecified").strip() or "unspecified" for row in included)
    errors = []
    if unknown:
        errors.append("unknown_nodes")
    if duplicates:
        errors.append("duplicate_undirected_edges")
    if diagonal:
        errors.append("diagonal_nonzero")
    if asymmetric:
        errors.append("matrix_asymmetric")
    return {
        "prefix": graph["prefix"],
        "node_count": len(nodes),
        "edge_row_count": len(included),
        "unique_edge_count": len(unique_pairs),
        "edge_kind_counts": dict(sorted(edge_kind_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "unknown_edges": unknown,
        "duplicate_pairs": [edge_label(edge) for edge in duplicates],
        "matrix_diagonal_nonzero": diagonal,
        "matrix_asymmetric": asymmetric[:20],
        "existing_matrix_matches_edges": existing_matches,
        "existing_matrix_error": existing_error,
        "validation_passed": not errors,
        "errors": errors,
    }


def discover_rounds() -> list[str]:
    found: list[tuple[int, int, str]] = []
    for path in RESULTS.glob(f"document{DOCUMENT}_round*_*.csv"):
        match = ROUND_RE.match(path.name)
        if match:
            order = 0 if match.group("agent").lower() == "diego" else 1
            found.append((int(match.group("round")), order, path.name[: -len("_edges.csv")]))
    return [prefix for _, _, prefix in sorted(found)]


def write_round_comparison(prefixes: list[str]) -> None:
    rows = []
    previous: set[tuple[str, str]] | None = None
    for prefix in prefixes:
        graph = load_graph(prefix)
        report = validate(graph)
        current = set(graph["unique_pairs"])  # type: ignore[arg-type]
        added = sorted(current - previous) if previous is not None else []
        removed = sorted(previous - current) if previous is not None else []
        rows.append(
            {
                "round_prefix": prefix,
                "node_count": report["node_count"],
                "unique_edge_count": report["unique_edge_count"],
                "added_edge_count_vs_previous": "" if previous is None else len(added),
                "removed_edge_count_vs_previous": "" if previous is None else len(removed),
                "validation_passed": report["validation_passed"],
                "added_edges_vs_previous": "; ".join(edge_label(edge) for edge in added[:100]),
                "removed_edges_vs_previous": "; ".join(edge_label(edge) for edge in removed[:100]),
            }
        )
        previous = current
    if rows:
        with (RESULTS / f"document{DOCUMENT}_round_comparison.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def token_usage_estimates() -> tuple[Path, Path]:
    raw = sorted(BASE.glob("raw -- *.png"))[0]
    full_images = [raw, BASE / "component_labels_banners_overlay.png", BASE / "wires_mask_overlay.png", BASE / "wire_nodes_overlay.png"]
    key_names = [
        "raw__full_sheet.png",
        "labels__full_sheet.png",
        "wires__full_sheet.png",
        "nodes__full_sheet.png",
        "raw__focus_top_distribution.png",
        "raw__focus_middle_distribution.png",
        "raw__focus_lower_distribution.png",
        "raw__focus_dc_controls.png",
        "wires__focus_dc_controls.png",
        "raw__row3_col2.png",
        "wires__row3_col2.png",
    ]
    key_crops = [CROPS / name for name in key_names if (CROPS / name).exists()]
    all_crops = sorted(CROPS.glob("*.png"))
    task = "Extract document 41 connectivity matrix using Diego high-recall and Jennifer precision review. No GT and no off-the-shelf OCR."
    prompt_bits = {
        "main-01": task,
        "diego-01": task + " Inspect raw, overlays, CSV aids, and crops. Write high-recall round 01 graph.",
        "jennifer-01": task + " Review Diego, prune unsupported edges, write precision round 02 graph.",
        "diego-02": task + " Recheck Jennifer changes and saturate in round 03.",
        "jennifer-02": task + " Final precision sign-off and saturation in round 04.",
        "main-02": task + " Validate final graph, compare rounds, and summarize.",
    }
    round_files = {
        "main-01": [],
        "diego-01": [BASE / "component_visual_ocr_labels.csv", BASE / "wire_nodes.csv"],
        "jennifer-01": [
            BASE / "component_visual_ocr_labels.csv",
            BASE / "wire_nodes.csv",
            RESULTS / "document41_round01_diego_edges.csv",
            RESULTS / "document41_round01_diego_nodes.csv",
            RESULTS / "document41_round01_diego_notes.md",
        ],
        "diego-02": [
            BASE / "component_visual_ocr_labels.csv",
            BASE / "wire_nodes.csv",
            RESULTS / "document41_round01_diego_edges.csv",
            RESULTS / "document41_round02_jennifer_edges.csv",
            RESULTS / "document41_round02_jennifer_notes.md",
        ],
        "jennifer-02": [
            BASE / "component_visual_ocr_labels.csv",
            BASE / "wire_nodes.csv",
            RESULTS / "document41_round01_diego_edges.csv",
            RESULTS / "document41_round02_jennifer_edges.csv",
            RESULTS / "document41_round03_diego_edges.csv",
            RESULTS / "document41_round03_diego_notes.md",
        ],
        "main-02": [
            RESULTS / "document41_round01_diego_notes.md",
            RESULTS / "document41_round02_jennifer_notes.md",
            RESULTS / "document41_round03_diego_notes.md",
            RESULTS / "document41_round04_jennifer_notes.md",
        ],
    }
    output_ranges = {
        "main-01": (250, 600, 1200),
        "diego-01": (6500, 11000, 19000),
        "jennifer-01": (5500, 9000, 16000),
        "diego-02": (3500, 7000, 13000),
        "jennifer-02": (3000, 5500, 11000),
        "main-02": (700, 1200, 2200),
    }
    agents = {
        "main-01": ("main", "setup", "orchestrator"),
        "diego-01": ("Diego", "01", "high-recall extractor"),
        "jennifer-01": ("Jennifer", "02", "precision reviewer"),
        "diego-02": ("Diego", "03", "saturation extractor"),
        "jennifer-02": ("Jennifer", "04", "final precision signoff"),
        "main-02": ("main", "finalize", "orchestrator"),
    }
    image_low = sum(image_tokens(path) for path in full_images[:3])
    image_expected = sum(image_tokens(path) for path in full_images + key_crops)
    image_high = sum(image_tokens(path) for path in full_images + all_crops)
    image_calls = {"diego-01", "jennifer-01", "diego-02", "jennifer-02"}
    rows = []
    for call_id in ["main-01", "diego-01", "jennifer-01", "diego-02", "jennifer-02", "main-02"]:
        expected_text = text_tokens(prompt_bits[call_id]) + sum(file_tokens(path) for path in round_files[call_id])
        low_text = math.ceil(expected_text * 0.75)
        high_text = math.ceil(expected_text * 1.25)
        low_img = image_low if call_id in image_calls else 0
        exp_img = image_expected if call_id in image_calls else 0
        high_img = image_high if call_id in image_calls else 0
        out_low, out_exp, out_high = output_ranges[call_id]
        agent, round_name, role = agents[call_id]
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "call_id": call_id,
                "agent": agent,
                "round": round_name,
                "role": role,
                "model": MODEL,
                "input_text_tokens_low": low_text,
                "input_text_tokens_expected": expected_text,
                "input_text_tokens_high": high_text,
                "cached_input_tokens": "unknown",
                "image_file_input_tokens_low": low_img,
                "image_file_input_tokens_expected": exp_img,
                "image_file_input_tokens_high": high_img,
                "output_tokens_low": out_low,
                "output_tokens_expected": out_exp,
                "output_tokens_high": out_high,
                "reasoning_tokens": "unavailable",
                "total_tokens_low": low_text + low_img + out_low,
                "total_tokens_expected": expected_text + exp_img + out_exp,
                "total_tokens_high": high_text + high_img + out_high,
                "usage_object_available": "no",
                "counting_method": "tiktoken o200k_base for text; public high-detail image tiling estimate; output ranges estimated",
            }
        )
    detail_path = RESULTS / f"document{DOCUMENT}_token_usage_estimates.csv"
    with detail_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    totals = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "calls": len(rows),
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "input_text_tokens_expected": sum(int(row["input_text_tokens_expected"]) for row in rows),
        "image_file_input_tokens_expected": sum(int(row["image_file_input_tokens_expected"]) for row in rows),
        "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in rows),
        "openai_api_key_present": "no",
    }
    totals_path = RESULTS / f"document{DOCUMENT}_token_usage_totals.csv"
    with totals_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(totals.keys()))
        writer.writeheader()
        writer.writerow(totals)
    (RESULTS / f"document{DOCUMENT}_token_usage_notes.md").write_text(
        "# Document 41 Token Usage Notes\n\n"
        "- Actual model usage objects were unavailable from the local subagent tool responses.\n"
        "- No API key was available, so the Responses token-counting endpoint could not be called.\n"
        "- Text estimates use `tiktoken` `o200k_base` where available; image estimates use public high-detail image tiling.\n"
        "- Low/expected/high ranges vary visual context volume and unknown output length.\n",
        encoding="utf-8",
    )
    return detail_path, totals_path


def parse_csv_text(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(text.strip().splitlines()))


def seed_round01() -> dict[str, object]:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), CODES / "doc41_write_results.py")
    node_rows = parse_csv_text(DIEGO_ROUND01_NODES_CSV)
    edge_rows = parse_csv_text(DIEGO_ROUND01_EDGES_CSV)
    prefix = "document41_round01_diego"
    nodes_path = RESULTS / f"{prefix}_nodes.csv"
    edges_path = RESULTS / f"{prefix}_edges.csv"
    matrix_path = RESULTS / f"{prefix}_adjacency_matrix.csv"
    summary_path = RESULTS / f"{prefix}_matrix_summary.json"
    notes_path = RESULTS / f"{prefix}_notes.md"
    write_rows(nodes_path, node_rows, ["node", "component_type", "node_kind"])
    write_rows(edges_path, edge_rows, ["source", "target", "edge_kind", "confidence", "evidence"])
    graph = load_graph(prefix)
    write_matrix(matrix_path, graph["nodes"], graph["unique_pairs"])  # type: ignore[arg-type]
    report = validate(load_graph(prefix))
    summary = {
        "nodes": report["node_count"],
        "included_edge_rows": report["edge_row_count"],
        "unique_undirected_edges": report["unique_edge_count"],
        "duplicate_edge_rows": len(report["duplicate_pairs"]),
        "validation_passed": report["validation_passed"],
        "unknown_endpoint_count": len(report["unknown_edges"]),
        "symmetric": not bool(report["matrix_asymmetric"]),
        "diagonal_zero": not bool(report["matrix_diagonal_nonzero"]),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    notes_path.write_text(
        "# Document 41 Round01 Diego Notes\n\n"
        "Diego returned this high-recall graph as text because direct writes to the results folder were blocked. "
        "The main agent wrote the CSV/matrix artifacts from Diego's returned CSV using the approved doc41 writer.\n\n"
        "- GND-1E is included as a high-recall grounding/reference candidate.\n"
        "- CLASS-1E-AC/DC, VITAL-POWER-TRAIN-A/B, cable/feeder callouts, CTRL-86A/B text, notes, legend, "
        "terminal schedule, title, and grid metadata are excluded as annotations.\n"
        "- Uncertain/high-recall edges: TR-1A -- GND-1E, BUS-480A -- CHGR-125A, BUS-480E1B -- CHGR-125B.\n",
        encoding="utf-8",
    )
    print(json.dumps({"seeded": prefix, **summary}, indent=2))
    return summary


def seed_round02_from_jennifer() -> dict[str, object]:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), CODES / "doc41_write_results.py")
    r1_nodes = RESULTS / "document41_round01_diego_nodes.csv"
    r1_edges = RESULTS / "document41_round01_diego_edges.csv"
    if not r1_nodes.exists() or not r1_edges.exists():
        seed_round01()
    node_rows = [row for row in read_rows(r1_nodes) if node_name(row) != "GND-1E"]
    edge_rows = []
    for row in read_rows(r1_edges):
        source = (row.get("source") or "").strip()
        target = (row.get("target") or "").strip()
        if "GND-1E" in {source, target}:
            continue
        if {source, target} == {"BUS-480A", "CHGR-125A"}:
            row["confidence"] = "high"
            row["evidence"] = "Solid CABLE 1A-480-7 feeder route from BUS-480A to CHGR-125A input; cable label is annotation only."
        if {source, target} == {"BUS-480E1B", "CHGR-125B"}:
            row["confidence"] = "high"
            row["evidence"] = "Solid CABLE 1B-480-9 feeder route from BUS-480E1B area to CHGR-125B input; cable label is annotation only."
        edge_rows.append(row)

    prefix = "document41_round02_jennifer"
    nodes_path = RESULTS / f"{prefix}_nodes.csv"
    edges_path = RESULTS / f"{prefix}_edges.csv"
    matrix_path = RESULTS / f"{prefix}_adjacency_matrix.csv"
    summary_path = RESULTS / f"{prefix}_matrix_summary.json"
    notes_path = RESULTS / f"{prefix}_notes.md"
    write_rows(nodes_path, node_rows, list(node_rows[0].keys()))
    write_rows(edges_path, edge_rows, list(edge_rows[0].keys()))
    graph = load_graph(prefix)
    write_matrix(matrix_path, graph["nodes"], graph["unique_pairs"])  # type: ignore[arg-type]
    report = validate(load_graph(prefix))
    summary = {
        "nodes": report["node_count"],
        "included_edge_rows": report["edge_row_count"],
        "unique_undirected_edges": report["unique_edge_count"],
        "duplicate_edge_rows": len(report["duplicate_pairs"]),
        "validation_passed": report["validation_passed"],
        "unknown_endpoint_count": len(report["unknown_edges"]),
        "symmetric": not bool(report["matrix_asymmetric"]),
        "diagonal_zero": not bool(report["matrix_diagonal_nonzero"]),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    notes_path.write_text(
        "# Document 41 Round02 Jennifer Notes\n\n"
        "Jennifer returned this precision graph as text because direct writes to the results folder were blocked. "
        "The main agent wrote the CSV/matrix artifacts from Jennifer's returned decision using the approved doc41 writer.\n\n"
        "## Precision Changes From Diego Round01\n\n"
        "- Removed `GND-1E` and `TR-1A -- GND-1E`; the raw schematic shows a grounding/reference symbol below `TR-1A`, "
        "but it is not a peer equipment matrix node and is absent from the component CSV.\n"
        "- Kept `BUS-480A -- CHGR-125A`; the solid `CABLE 1A-480-7` feeder route visually supports this connection, "
        "while the cable text itself remains an annotation only.\n"
        "- Kept `BUS-480E1B -- CHGR-125B`; the solid `CABLE 1B-480-9` feeder route visually supports this connection, "
        "while the cable text itself remains an annotation only.\n"
        "- Kept the lower dashed control chain as `CB-105 -- RELAY-K86A -- PANEL-RPS-A -- JB-ESF-01 -- PANEL-RPS-B -- RELAY-K86B -- CB-106`.\n"
        "- Did not add direct `PANEL-RPS-A -- PANEL-RPS-B`, direct relay-to-JB shortcuts, or `UPS-BUS-B -- INST-RACK-1`.\n\n"
        "## Final Round02 Graph\n\n"
        f"- Nodes: {summary['nodes']}\n"
        f"- Included undirected edges: {summary['unique_undirected_edges']}\n",
        encoding="utf-8",
    )
    print(json.dumps({"seeded": prefix, **summary}, indent=2))
    return summary


def copy_round(source_prefix: str, target_prefix: str, notes: str) -> dict[str, object]:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), CODES / "doc41_write_results.py")
    source_nodes = RESULTS / f"{source_prefix}_nodes.csv"
    source_edges = RESULTS / f"{source_prefix}_edges.csv"
    if not source_nodes.exists() or not source_edges.exists():
        seed_round02_from_jennifer()
    node_rows = read_rows(source_nodes)
    edge_rows = read_rows(source_edges)
    nodes_path = RESULTS / f"{target_prefix}_nodes.csv"
    edges_path = RESULTS / f"{target_prefix}_edges.csv"
    matrix_path = RESULTS / f"{target_prefix}_adjacency_matrix.csv"
    summary_path = RESULTS / f"{target_prefix}_matrix_summary.json"
    notes_path = RESULTS / f"{target_prefix}_notes.md"
    write_rows(nodes_path, node_rows, list(node_rows[0].keys()))
    write_rows(edges_path, edge_rows, list(edge_rows[0].keys()))
    graph = load_graph(target_prefix)
    write_matrix(matrix_path, graph["nodes"], graph["unique_pairs"])  # type: ignore[arg-type]
    report = validate(load_graph(target_prefix))
    summary = {
        "nodes": report["node_count"],
        "included_edge_rows": report["edge_row_count"],
        "unique_undirected_edges": report["unique_edge_count"],
        "duplicate_edge_rows": len(report["duplicate_pairs"]),
        "validation_passed": report["validation_passed"],
        "unknown_endpoint_count": len(report["unknown_edges"]),
        "symmetric": not bool(report["matrix_asymmetric"]),
        "diagonal_zero": not bool(report["matrix_diagonal_nonzero"]),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    notes_path.write_text(notes + "\n", encoding="utf-8")
    print(json.dumps({"seeded": target_prefix, "source": source_prefix, **summary}, indent=2))
    return summary


def seed_round03_from_diego() -> dict[str, object]:
    return copy_round(
        "document41_round02_jennifer",
        "document41_round03_diego",
        "# Document 41 Round03 Diego Saturation Notes\n\n"
        "Diego agreed with Jennifer round02 unchanged. The round03 graph copies the 57-node, 59-edge graph forward.\n\n"
        "- `GND-1E` and `TR-1A -- GND-1E` remain excluded as grounding/reference annotation.\n"
        "- `BUS-480A -- CHGR-125A` and `BUS-480E1B -- CHGR-125B` remain included as solid feeder routes.\n"
        "- The lower dashed control chain remains `CB-105 -- RELAY-K86A -- PANEL-RPS-A -- JB-ESF-01 -- PANEL-RPS-B -- RELAY-K86B -- CB-106`.\n"
        "- No node or edge changes were made from Jennifer round02.\n",
    )


def seed_round04_from_jennifer() -> dict[str, object]:
    return copy_round(
        "document41_round03_diego",
        "document41_round04_jennifer",
        "# Document 41 Round04 Jennifer Final Precision Sign-Off\n\n"
        "Jennifer agreed with Diego round03 unchanged. Saturation is reached with the 57-node, 59-edge graph.\n\n"
        "- `GND-1E` remains excluded as a grounding/reference annotation, not a peer matrix node.\n"
        "- Charger feeder routes and the lower RPS/control interlock chain remain included.\n"
        "- No no-dot/callout/metadata crossing was modeled as a connection.\n"
        "- No further precision changes were made.\n",
    )


def main(argv: list[str]) -> int:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), CODES / "doc41_write_results.py")
    if len(argv) > 1 and argv[1] == "seed_round01":
        seed_round01()
        return 0
    if len(argv) > 1 and argv[1] == "seed_round02":
        seed_round02_from_jennifer()
        return 0
    if len(argv) > 1 and argv[1] == "seed_round03":
        seed_round03_from_diego()
        return 0
    if len(argv) > 1 and argv[1] == "seed_round04":
        seed_round04_from_jennifer()
        return 0
    prefixes = discover_rounds()
    if not prefixes:
        raise SystemExit("no round edge CSV files found")
    prefix = argv[1] if len(argv) > 1 else prefixes[-1]
    graph = load_graph(prefix)
    report = validate(graph)
    if not report["validation_passed"]:
        print(json.dumps(report, indent=2))
        raise SystemExit("final graph validation failed")

    final_edges = RESULTS / f"document{DOCUMENT}_final_edges.csv"
    final_nodes = RESULTS / f"document{DOCUMENT}_final_nodes.csv"
    final_matrix = RESULTS / f"document{DOCUMENT}_final_adjacency_matrix.csv"
    connectivity = RESULTS / "connectivity_matrix.csv"
    write_rows(final_edges, graph["edge_rows"], list(graph["edge_rows"][0].keys()))  # type: ignore[index]
    write_rows(final_nodes, graph["node_rows"], list(graph["node_rows"][0].keys()))  # type: ignore[index]
    write_matrix(final_matrix, graph["nodes"], graph["unique_pairs"])  # type: ignore[arg-type]
    shutil.copyfile(final_matrix, connectivity)
    write_round_comparison(discover_rounds())
    detail_path, totals_path = token_usage_estimates()
    report.update(
        {
            "final_source_prefix": prefix,
            "final_edges_file": str(final_edges),
            "final_nodes_file": str(final_nodes),
            "final_matrix_file": str(final_matrix),
            "connectivity_matrix_file": str(connectivity),
            "rounds_compared": discover_rounds(),
            "token_usage_estimates_file": str(detail_path),
            "token_usage_totals_file": str(totals_path),
        }
    )
    with (RESULTS / f"document{DOCUMENT}_validation_summary.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
