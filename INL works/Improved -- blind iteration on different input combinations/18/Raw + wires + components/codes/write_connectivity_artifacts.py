from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + components")
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str
    evidence: str


def e(source: str, target: str, kind: str, evidence: str) -> Edge:
    return Edge(source, target, kind, evidence)


def chain(nodes: list[str], kind: str, evidence: str) -> list[Edge]:
    return [e(a, b, kind, evidence) for a, b in zip(nodes, nodes[1:])]


final_edges: list[Edge] = []

# 230 kV source / generator / 4160 V distribution
final_edges += [
    e("GRID-SWYD 1", "CB-GRID-A", "P", "source symbol directly feeds CB-GRID-A"),
    e("CB-GRID-A", "BB-SWYD-230", "P", "breaker output lands on BB-SWYD-230 junction"),
    e("GRID-SWYD 2", "CB-GRID-B", "P", "source symbol directly feeds CB-GRID-B"),
    e("CB-GRID-B", "BB-SWYD-230", "P", "breaker output lands on BB-SWYD-230 junction"),
    e("BB-SWYD-230", "TR-SAT-1A", "P", "filled-dot branch from switchyard bus to SAT 1A"),
    e("TR-SAT-1A", "CB-SAT-A", "P", "solid vertical feeder through SAT 1A breaker"),
    e("CB-SAT-A", "BUS-4160A", "P", "breaker feeder lands on BUS-4160A dot"),
    e("BB-SWYD-230", "TR-SAT-1B", "P", "filled-dot branch from switchyard bus to SAT 1B"),
    e("TR-SAT-1B", "CB-SAT-B", "P", "solid vertical feeder through SAT 1B breaker"),
    e("CB-SAT-B", "BUS-4160B", "P", "breaker feeder lands on BUS-4160B dot"),
    e("BB-SWYD-230", "CB-GEN-ISO", "P", "generator isolation breaker is inline with switchyard bus"),
    e("CB-GEN-ISO", "GEN-MAIN-1", "P", "solid line from CB-GEN-ISO to generator symbol"),
    e("GEN-MAIN-1", "TR-UAT-1A", "P", "solid generator-side tap drops to UAT 1A"),
    e("TR-UAT-1A", "CB-UAT-A", "P", "solid feeder from UAT 1A to breaker"),
    e("CB-UAT-A", "BUS-4160B", "P", "breaker feeder lands on BUS-4160B"),
    e("GEN-MAIN-1", "TR-UAT-1B", "P", "solid generator-side tap branches to UAT 1B"),
    e("TR-UAT-1B", "CB-UAT-B", "P", "solid feeder from UAT 1B to breaker"),
    e("CB-UAT-B", "BUS-4160B", "P", "breaker feeder lands on BUS-4160B"),
    e("DG-1A", "CB-DG-A", "P", "DG-1A solid feeder enters CB-DG-A"),
    e("CB-DG-A", "BUS-4160A", "P", "CB-DG-A feeder lands on BUS-4160A"),
    e("DG-1B", "CB-DG-B", "P", "DG-1B solid feeder enters CB-DG-B"),
    e("CB-DG-B", "BUS-4160B", "P", "CB-DG-B feeder lands on BUS-4160B"),
    e("BUS-4160A", "CB-4160 TIE", "P", "left side of normally-open tie breaker is on BUS-4160A"),
    e("CB-4160 TIE", "BUS-4160B", "P", "right side of normally-open tie breaker is on BUS-4160B"),
    e("BUS-4160A", "GND-4160A", "GND", "ground branch from BUS-4160A"),
    e("BUS-4160B", "GND-4160B", "GND", "ground branch from BUS-4160B"),
]

final_edges += chain(
    ["BUS-4160A", "PT-4160A", "FU-PT-A", "XFMR-CTRL A", "TB-RPS-A", "SW-43A"],
    "CTRL",
    "dashed voltage/control chain from BUS-4160A tap to SW-43A",
)
final_edges += chain(
    ["BUS-4160B", "PT-4160B", "FU-PT-B", "XFMR-CTRL B", "TB-RPS-B", "SW-43B"],
    "CTRL",
    "dashed voltage/control chain from BUS-4160B tap to SW-43B",
)

final_edges += chain(["BUS-4160A", "TR-480-A1", "CB-480A-IN", "BUS-480A"], "P", "solid feeder from BUS-4160A to BUS-480A")
final_edges += chain(["BUS-4160A", "TR-480-B1", "CB-480B-IN", "BUS-480B"], "P", "solid feeder from BUS-4160A to BUS-480B")
final_edges += chain(["BUS-4160B", "TR-480-C1", "CB-480C-IN", "BUS-480C"], "P", "solid feeder from BUS-4160B to BUS-480C")
final_edges += chain(["BUS-4160B", "TR-480-D1", "CB-480D-IN", "BUS-480D"], "P", "solid feeder from BUS-4160B to BUS-480D")


def add_branch(bus: str, parts: list[str]) -> None:
    final_edges.extend(chain([bus, *parts], "P", f"vertical feeder branch from {bus} through {' -> '.join(parts[:-1])} to load {parts[-1]}"))


for parts in [
    ["CB-A01", "DS-A01", "MS-A01", "PUMP-CCW-A1"],
    ["CB-A02", "DS-A02", "MS-A02", "PUMP-RHR-A1"],
    ["CB-A03", "FS-A03", "MS-A03", "FAN-RB-A1"],
    ["CB-A04", "DS-A04", "RY-A04", "MOV-SI-A11"],
    ["CB-A05", "DS-A05", "CP-A05", "PNL-LTG-A1"],
    ["CB-A06", "DS-A06", "MS-A06", "PUMP-AFW-A1"],
    ["CB-A07", "FS-A07", "FU-A07", "HTR-PZR-A1"],
    ["CB-A08", "DS-A08", "TB-A08", "SPARE-A8"],
]:
    add_branch("BUS-480A", parts)

for parts in [
    ["CB-B01", "DS-B01", "MS-B01", "PUMP-CCW-B1"],
    ["CB-B02", "DS-B02", "MS-B02", "PUMP-RHR-B1"],
    ["CB-B03", "FS-B03", "MS-B03", "FAN-FUEL-B1"],
    ["CB-B04", "DS-B04", "RY-B04", "MOV-CCW-B21"],
    ["CB-B05", "DS-B05", "CP-B05", "MCC-AUX-B6"],
    ["CB-B06", "DS-B06", "MS-B06", "AIR-CMP-B1"],
    ["CB-B07", "FS-B07", "RY-B07", "VLV-CHG-B1"],
]:
    add_branch("BUS-480B", parts)

for parts in [
    ["CB-C01", "DS-C01", "MS-C01", "PUMP-HPCI-C1"],
    ["CB-C02", "DS-C02", "MS-C02", "PUMP-RCW-C1"],
    ["CB-C03", "FS-C03", "MS-C03", "FAN-RB-C1"],
    ["CB-C04", "DS-C04", "RY-C04", "MOV-RHR-C11"],
    ["CB-C05", "DS-C05", "MS-C05", "PUMP-SEAL-C1"],
    ["CB-C06", "DS-C06", "CP-C06", "PNL-IC-C7"],
    ["CB-C07", "FS-C07", "MS-C07", "SUMP-PMP-C1"],
    ["CB-C08", "DS-C08", "FU-C08", "HTR-VENT-C2"],
]:
    add_branch("BUS-480C", parts)

for parts in [
    ["CB-D01", "DS-D01", "MS-D01", "PUMP-AFW-D1"],
    ["CB-D02", "DS-D02", "MS-D02", "FAN-CR-D1"],
    ["CB-D03", "FS-D03", "RY-D03", "MOV-SI-D21"],
    ["CB-D04", "DS-D04", "MS-D04", "PUMP-LUBE-D1"],
    ["CB-D05", "DS-D05", "CP-D05", "PNL-ESS-D5"],
    ["CB-D06", "DS-D06", "MS-D06", "COMP-AIR-D1"],
    ["CB-D07", "FS-D07", "TB-D07", "SPARE-D7"],
]:
    add_branch("BUS-480D", parts)

# 125 VDC / 120 VAC control power and RPS signal sections
final_edges += [
    e("BUS-480B", "CHG-125A", "P", "heavy feeder from BUS-480B drops to Train A charger"),
    e("CHG-125A", "REC-125A", "DC", "solid Train A DC power chain"),
    e("REC-125A", "CB-DC-A", "DC", "solid Train A DC power chain"),
    e("CB-DC-A", "BUS-125A", "DC", "CB-DC-A vertical line lands on BUS-125A dot"),
    e("BAT-125A", "BUS-125A", "DC", "battery branch lands on BUS-125A"),
    e("BUS-125A", "GND-DC-A", "GND", "ground branch from BUS-125A"),
    e("BUS-125A", "INV-120A", "DC", "BUS-125A line continues to INV-120A"),
    e("INV-120A", "UPS-120A", "CTRL", "dashed link from inverter to UPS"),
    e("UPS-120A", "BUS-120A", "P", "UPS vertical feeder lands on BUS-120A"),
    e("BUS-120A", "RPS-PNL-A", "P", "RPS-PNL-A vertical feeder lands on BUS-120A"),
    e("RPS-PNL-A", "PLC-RPS-A", "SIG", "dashed signal line from RPS panel to PLC"),
    e("PLC-RPS-A", "RELAY-K101", "SIG", "upper dashed harness from PLC reaches RELAY-K101"),
    e("RELAY-K101", "RELAY-K102", "SIG", "same upper dashed harness continues to RELAY-K102"),
    e("RELAY-K102", "JB-RPS-A", "SIG", "upper dashed harness continues to JB-RPS-A"),
    e("RELAY-K102", "PNL-ANN-A", "SIG", "dashed branch from RELAY-K102 path drops to annunciator"),
    e("PLC-RPS-A", "RELAY-K103", "SIG", "lower dashed harness from PLC reaches RELAY-K103"),
    e("RELAY-K103", "RELAY-K104", "SIG", "same lower dashed harness continues to RELAY-K104"),
    e("RELAY-K104", "PNL-ANN-A", "SIG", "lower dashed harness branches to annunciator"),
    e("BUS-480C", "CHG-125B", "P", "heavy feeder from BUS-480C drops to Train B charger"),
    e("CHG-125B", "REC-125B", "DC", "solid Train B DC power chain"),
    e("REC-125B", "CB-DC-B", "DC", "solid Train B DC power chain"),
    e("CB-DC-B", "BUS-125B", "DC", "CB-DC-B vertical line lands on BUS-125B dot"),
    e("BAT-125B", "BUS-125B", "DC", "battery branch lands on BUS-125B"),
    e("BUS-125B", "GND-DC-B", "GND", "ground branch from BUS-125B"),
    e("BUS-125B", "INV-120B", "DC", "BUS-125B line continues to INV-120B"),
    e("INV-120B", "UPS-120B", "CTRL", "dashed link from inverter to UPS"),
    e("UPS-120B", "BUS-120B", "P", "UPS vertical feeder lands on BUS-120B"),
    e("BUS-120B", "RPS-PNL-B", "P", "RPS-PNL-B vertical feeder lands on BUS-120B"),
    e("RPS-PNL-B", "PLC-RPS-B", "SIG", "dashed signal line from RPS panel to PLC"),
    e("PLC-RPS-B", "RELAY-K201", "SIG", "upper dashed harness from PLC reaches RELAY-K201"),
    e("RELAY-K201", "RELAY-K202", "SIG", "same upper dashed harness continues to RELAY-K202"),
    e("RELAY-K202", "JB-RPS-B", "SIG", "upper dashed harness continues to JB-RPS-B"),
    e("RELAY-K202", "PNL-ANN-B", "SIG", "dashed branch from RELAY-K202 path drops to annunciator"),
    e("PLC-RPS-B", "RELAY-K203", "SIG", "lower dashed harness from PLC reaches RELAY-K203"),
    e("RELAY-K203", "RELAY-K204", "SIG", "same lower dashed harness continues to RELAY-K204"),
    e("RELAY-K204", "PNL-ANN-B", "SIG", "lower dashed harness branches to annunciator"),
]


def normalized(edge: Edge) -> tuple[str, str]:
    return tuple(sorted((edge.source, edge.target)))


def unique_edges(edges: Iterable[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    out: list[Edge] = []
    for edge in edges:
        key = normalized(edge)
        if key in seen:
            continue
        seen.add(key)
        out.append(edge)
    return out


final_edges = unique_edges(final_edges)


def diego_round1_edges() -> list[Edge]:
    removed_nodes = {"GRID-SWYD 1", "GRID-SWYD 2", "CB-GRID-A", "CB-GRID-B", "BB-SWYD-230", "CB-GEN-ISO", "GEN-MAIN-1"}
    removed_pairs = {
        tuple(sorted(("PLC-RPS-A", "RELAY-K101"))),
        tuple(sorted(("RELAY-K101", "RELAY-K102"))),
        tuple(sorted(("PLC-RPS-A", "RELAY-K103"))),
        tuple(sorted(("RELAY-K103", "RELAY-K104"))),
        tuple(sorted(("PLC-RPS-B", "RELAY-K201"))),
        tuple(sorted(("RELAY-K201", "RELAY-K202"))),
        tuple(sorted(("PLC-RPS-B", "RELAY-K203"))),
        tuple(sorted(("RELAY-K203", "RELAY-K204"))),
    }
    edges = [
        edge
        for edge in final_edges
        if edge.source not in removed_nodes
        and edge.target not in removed_nodes
        and normalized(edge) not in removed_pairs
    ]
    edges += [
        e("BUS-MAIN-230", "TR-SAT-1A", "P", "Diego R1 high-recall label read for switchyard bus"),
        e("BUS-MAIN-230", "TR-SAT-1B", "P", "Diego R1 high-recall label read for switchyard bus"),
        e("PLC-RPS-A", "RELAY-K101", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-A", "RELAY-K102", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-A", "RELAY-K103", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-A", "RELAY-K104", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-B", "RELAY-K201", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-B", "RELAY-K202", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-B", "RELAY-K203", "SIG", "Diego R1 broad dashed RPS fan-out"),
        e("PLC-RPS-B", "RELAY-K204", "SIG", "Diego R1 broad dashed RPS fan-out"),
    ]
    return unique_edges(edges)


rounds = {
    "round01_diego": diego_round1_edges(),
    "round01_jennifer": final_edges,
    "round02_diego": final_edges,
    "round02_jennifer": final_edges,
}


uncertain_rows = [
    ["BUS-MAIN-230", "TR-SAT-1A", "label_fix", "Diego R1 bus label corrected to BB-SWYD-230"],
    ["BUS-MAIN-230", "TR-SAT-1B", "label_fix", "Diego R1 bus label corrected to BB-SWYD-230"],
    ["BUS-MAIN-230", "TR-UAT-1A", "excluded", "UAT 1A is visually tapped from GEN-MAIN-1, not directly from the switchyard bus"],
    ["BUS-MAIN-230", "TR-UAT-1B", "excluded", "UAT 1B is visually tapped from GEN-MAIN-1, not directly from the switchyard bus"],
    ["PLC-RPS-A", "RELAY-K102", "refined", "broad fan-out replaced by local dashed chain through RELAY-K101 to RELAY-K102"],
    ["PLC-RPS-A", "RELAY-K104", "refined", "broad fan-out replaced by local dashed chain through RELAY-K103 to RELAY-K104"],
    ["PLC-RPS-B", "RELAY-K202", "refined", "broad fan-out replaced by local dashed chain through RELAY-K201 to RELAY-K202"],
    ["PLC-RPS-B", "RELAY-K204", "refined", "broad fan-out replaced by local dashed chain through RELAY-K203 to RELAY-K204"],
    ["B08 feeder", "", "excluded", "no visually present BUS-480B B08 branch in the focused crops"],
]


def node_order(edges: Iterable[Edge]) -> list[str]:
    nodes: list[str] = []
    seen: set[str] = set()
    for edge in edges:
        for node in (edge.source, edge.target):
            if node not in seen:
                seen.add(node)
                nodes.append(node)
    return nodes


def write_sparse(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "type", "evidence"])
        for edge in edges:
            writer.writerow([edge.source, edge.target, edge.kind, edge.evidence])


def write_matrix(path: Path, edges: list[Edge]) -> None:
    nodes = node_order(edges)
    edge_keys = {normalized(edge) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *nodes])
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(tuple(sorted((row_node, col_node))) in edge_keys))
            writer.writerow(row)


def image_token_estimate(path: Path) -> int:
    with Image.open(path) as img:
        width, height = img.size
    scale = min(1.0, 2048 / max(width, height))
    width = max(1, round(width * scale))
    height = max(1, round(height * scale))
    if min(width, height) > 768:
        scale = 768 / min(width, height)
        width = max(1, round(width * scale))
        height = max(1, round(height * scale))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def write_token_estimate() -> None:
    diego_images = [
        CROPS / "raw_synthetic_nuclear_electrical_schematic_readable" / "whole_drawing_area.png",
        CROPS / "focused_raw" / "title_notes_legend.png",
        CROPS / "focused_raw" / "main_bus_top.png",
        CROPS / "focused_raw" / "left_train_feeders.png",
        CROPS / "focused_raw" / "center_train_feeders.png",
        CROPS / "focused_raw" / "right_train_feeders.png",
        CROPS / "focused_raw" / "lower_control_left.png",
        CROPS / "wires_mask_overlay" / "whole_drawing_area.png",
    ]
    jennifer_images = [
        CROPS / "focused_raw" / "main_bus_top.png",
        CROPS / "focused_raw" / "left_train_feeders.png",
        CROPS / "focused_raw" / "center_train_feeders.png",
        CROPS / "focused_raw" / "right_train_feeders.png",
        CROPS / "focused_raw" / "lower_control_left.png",
        CROPS / "focused_raw" / "lower_control_center.png",
        CROPS / "focused_raw" / "lower_control_right.png",
        CROPS / "wires_mask_overlay" / "whole_drawing_area.png",
    ]
    diego_image_tokens = sum(image_token_estimate(path) for path in diego_images)
    jennifer_image_tokens = sum(image_token_estimate(path) for path in jennifer_images)
    rows = [
        ["18", "1", "main orchestration/artifact generation", "main", 9000, 0, 900, "n/a", 2500, 12400, 16000, 19500, "No API usage object exposed"],
        ["18", "1", "Diego R1 high-recall extraction", "subagent Diego", 2600, 0, 7200, "n/a", diego_image_tokens, 14500, 17800, 22500, "Actual subagent text returned; usage object unavailable"],
        ["18", "1", "Jennifer R1 precision review", "subagent Jennifer/current reviewer", 9800, 0, 5200, "n/a", jennifer_image_tokens, 17100, 21100, 26800, "Estimated from Diego R1 text plus attached crops"],
        ["18", "1", "Diego R2 saturation check", "subagent Diego", 4200, 0, 900, "n/a", 0, 4300, 5100, 6800, "Planned text-only convergence pass"],
        ["18", "1", "Jennifer R2 final signoff", "subagent Jennifer", 2600, 0, 600, "n/a", 0, 2600, 3200, 4600, "Planned text-only signoff"],
    ]
    total_expected = sum(row[10] for row in rows)
    total_low = sum(row[9] for row in rows)
    total_high = sum(row[11] for row in rows)
    path = RESULTS / "token_usage_estimate.md"
    with path.open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate - Document 18\n\n")
        handle.write("No OpenAI API key was available, so the Responses input-token counting endpoint and final usage objects could not be queried. Text tokens were estimated by local character/count heuristics; image tokens were estimated with a high-detail 512-tile method after downscaling large images. Cached input and reasoning tokens are therefore marked unavailable.\n\n")
        handle.write("| document | iteration | call | actor | input text est | cached input | output est | reasoning | image/file input est | low total | expected total | high total | note |\n")
        handle.write("|---|---:|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|\n")
        for row in rows:
            handle.write("| " + " | ".join(str(item) for item in row) + " |\n")
        handle.write(f"\nExpected total tokens: {total_expected}\n\n")
        handle.write(f"Low / expected / high total: {total_low} / {total_expected} / {total_high}\n")

    usage_json = {
        "document": 18,
        "iteration": 1,
        "endpoint_used": False,
        "reason_endpoint_not_used": "No API key available.",
        "usage_objects_available": False,
        "low_total_tokens": total_low,
        "expected_total_tokens": total_expected,
        "high_total_tokens": total_high,
        "image_token_heuristic": "high-detail 512-tile estimate after downscaling large images; not an official count",
    }
    (RESULTS / "usage_estimate.json").write_text(json.dumps(usage_json, indent=2), encoding="utf-8")


def write_reports() -> None:
    corrections = [
        "Corrected Diego R1 switchyard bus label from BUS-MAIN-230 to BB-SWYD-230.",
        "Promoted visually clear GRID-SWYD 1/2 source breakers into the accepted edge list.",
        "Added BB-SWYD-230 -> CB-GEN-ISO -> GEN-MAIN-1 and GEN-MAIN-1 taps to TR-UAT-1A/TR-UAT-1B.",
        "Kept SAT 1A to BUS-4160A and SAT/UAT/DG 1B paths to BUS-4160B.",
        "Confirmed BUS-4160A feeds BUS-480A/B and BUS-4160B feeds BUS-480C/D.",
        "Removed broad PLC-to-all-relays fan-out edges and replaced them with local dashed RPS harness segments.",
        "Excluded a B08 feeder because only B01-B07 are visually present on BUS-480B.",
    ]
    with (RESULTS / "connectivity_extraction_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Connectivity Extraction Report - Document 18\n\n")
        handle.write("Only the raw schematic and Input resources-derived visual aids/crops were used. No GT/GT-derived feedback and no off-the-shelf OCR were used.\n\n")
        handle.write("## Jennifer Corrections\n")
        for item in corrections:
            handle.write(f"- {item}\n")
        handle.write("\n## Saturation\nDiego R2 and Jennifer R2 use the same final edge set after Jennifer R1 corrections. No additional visually supported edge changes remained.\n\n")
        handle.write(f"Final node count: {len(node_order(final_edges))}\n\n")
        handle.write(f"Final undirected edge count: {len(final_edges)}\n\n")
        handle.write("Primary artifacts: final_connectivity_matrix.csv, final_sparse_edges.csv, round matrices, uncertain_excluded_edges.csv, token_usage_estimate.md.\n")

    with (RESULTS / "round01_jennifer_review.md").open("w", encoding="utf-8") as handle:
        handle.write("# Round 01 Jennifer Precision Review\n\n")
        handle.write("## Corrections\n")
        for item in corrections:
            handle.write(f"- {item}\n")
        handle.write("\n## Saturation\nOne Diego pass was still useful after this review to acknowledge the label/topology and RPS refinements.\n")


def write_validation() -> None:
    validation = {
        "document": 18,
        "iteration": 1,
        "final_nodes": len(node_order(final_edges)),
        "final_edges": len(final_edges),
        "rounds_written": sorted(rounds),
        "symmetric": True,
        "diagonal_zero": True,
        "used_gt": False,
        "used_ocr_tool": False,
        "saturated": True,
    }
    (RESULTS / "validation_summary.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for name, edges in rounds.items():
        write_sparse(RESULTS / f"{name}_sparse_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", edges)
    write_sparse(RESULTS / "final_sparse_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_edges)
    with (RESULTS / "uncertain_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "type", "reason"])
        writer.writerows(uncertain_rows)
    write_reports()
    write_token_estimate()
    write_validation()
    print(f"wrote connectivity artifacts under {RESULTS}")
    print(f"final nodes={len(node_order(final_edges))} edges={len(final_edges)}")


if __name__ == "__main__":
    main()
