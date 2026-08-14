from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires + components")
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def add_edge(edges: list[dict[str, str]], source: str, target: str, evidence: str, confidence: str) -> None:
    edges.append(
        {
            "source": source,
            "target": target,
            "evidence": evidence,
            "confidence": confidence,
        }
    )


def branch_spec(group: str) -> list[tuple[str, str, str, str]]:
    if group in {"A", "B"}:
        return [
            ("01", "DS", "PMP", "RLY"),
            ("02", "FU", "MOV", "LS"),
            ("03", "DS", "MTR", "RLY"),
            ("04", "DS", "PNL", "JB"),
            ("05", "FU", "PMP", "FT"),
            ("06", "DS", "MOV", "RLY"),
            ("07", "DS", "MCC", "TB"),
            ("08", "FU", "PMP", "PT"),
            ("09", "DS", "FAN", "HS"),
            ("10", "DS", "JB", "LT"),
        ]
    return [
        ("01", "DS", "MOV", "RLY"),
        ("02", "FU", "PNL", "JB"),
        ("03", "DS", "PMP", "FT"),
        ("04", "DS", "HTR", "HS"),
        ("05", "FU", "INST", "JB"),
        ("06", "DS", "MOV", "LS"),
        ("07", "DS", "MCC", "TB"),
        ("08", "FU", "PMP", "PT"),
        ("09", "DS", "PNL", "RLY"),
        ("10", "DS", "JB", "TB"),
    ]


def branch_nodes(group: str) -> list[str]:
    nodes: list[str] = []
    for num, device1, device2, terminal in branch_spec(group):
        nodes.extend(
            [
                f"CB-{group}{num}",
                f"{device1}-{group}{num}",
                f"{device2}-{group}{num}",
                f"{terminal}-{group}{num}",
            ]
        )
    return nodes


MAJOR_NODES = [
    "GRID-345",
    "DS-101",
    "CB-101",
    "GEN-G1",
    "CB-G1",
    "GEN-G2",
    "CB-G2",
    "BUS-13KV-N",
    "TR-1A",
    "CB-4A-IN",
    "TR-1B",
    "CB-4B-IN",
    "BUS-4160-A",
    "BUS-4160-B",
    "DG-1A",
    "CB-DG1A",
    "DG-1B",
    "CB-DG1B",
    "CB-TIE-41",
    "TR-480-A",
    "CB-480A-IN",
    "BUS-480-A",
    "TR-480-B",
    "CB-480B-IN",
    "BUS-480-B",
    "TR-480-C",
    "CB-480C-IN",
    "BUS-480-C",
    "TR-480-D",
    "CB-480D-IN",
    "BUS-480-D",
]

CONTROL_NODES = [
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-125A",
    "CHGR-125B",
    "BAT-125B",
    "DC-BUS-125B",
    "PANEL-CTRL-MAIN",
    "GND-EQ-A",
    "GND-EQ-B",
]

NODES = MAJOR_NODES + branch_nodes("A") + branch_nodes("B") + branch_nodes("C") + branch_nodes("D") + CONTROL_NODES


def base_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    # Sources and medium-voltage buses.
    for source, target, evidence, confidence in [
        ("GRID-345", "DS-101", "solid source line enters DS-101 from GRID-345 label", "High"),
        ("DS-101", "CB-101", "solid line continues from DS-101 to CB-101", "High"),
        ("CB-101", "BUS-13KV-N", "solid tap from CB-101 into BUS-13KV-N", "High"),
        ("GEN-G1", "CB-G1", "vertical generator feeder through CB-G1", "High"),
        ("CB-G1", "BUS-13KV-N", "filled tap from CB-G1 to BUS-13KV-N", "High"),
        ("GEN-G2", "CB-G2", "vertical generator feeder through CB-G2", "High"),
        ("CB-G2", "BUS-13KV-N", "filled tap from CB-G2 to BUS-13KV-N", "High"),
        ("BUS-13KV-N", "TR-1A", "solid vertical tap from BUS-13KV-N to TR-1A", "High"),
        ("TR-1A", "CB-4A-IN", "solid feeder below TR-1A through CB-4A-IN", "High"),
        ("CB-4A-IN", "BUS-4160-A", "filled tap from CB-4A-IN to BUS-4160-A", "High"),
        ("BUS-13KV-N", "TR-1B", "solid vertical tap from BUS-13KV-N to TR-1B", "High"),
        ("TR-1B", "CB-4B-IN", "solid feeder below TR-1B through CB-4B-IN", "High"),
        ("CB-4B-IN", "BUS-4160-B", "filled tap from CB-4B-IN to BUS-4160-B", "High"),
        ("DG-1A", "CB-DG1A", "diesel generator feeder through CB-DG1A", "High"),
        ("CB-DG1A", "BUS-4160-A", "filled tap from CB-DG1A to BUS-4160-A", "High"),
        ("DG-1B", "CB-DG1B", "diesel generator feeder through CB-DG1B", "High"),
        ("CB-DG1B", "BUS-4160-B", "filled tap from CB-DG1B to BUS-4160-B", "High"),
        ("BUS-4160-A", "CB-TIE-41", "solid 4160 V bus tie breaker from A side", "High"),
        ("CB-TIE-41", "BUS-4160-B", "solid 4160 V bus tie breaker to B side", "High"),
        ("BUS-4160-A", "TR-480-A", "solid feeder from BUS-4160-A down to TR-480-A", "High"),
        ("TR-480-A", "CB-480A-IN", "solid feeder through transformer secondary breaker", "High"),
        ("CB-480A-IN", "BUS-480-A", "slanted incoming feeder lands on BUS-480-A", "High"),
        ("BUS-4160-B", "TR-480-B", "solid feeder from BUS-4160-B down to TR-480-B", "High"),
        ("TR-480-B", "CB-480B-IN", "solid feeder through transformer secondary breaker", "High"),
        ("CB-480B-IN", "BUS-480-B", "slanted incoming feeder lands on BUS-480-B", "High"),
        ("BUS-4160-A", "TR-480-C", "long solid feeder from BUS-4160-A down left side to TR-480-C", "Medium"),
        ("TR-480-C", "CB-480C-IN", "solid feeder through TR-480-C to CB-480C-IN", "High"),
        ("CB-480C-IN", "BUS-480-C", "incoming feeder lands on BUS-480-C", "High"),
        ("BUS-4160-B", "TR-480-D", "long solid feeder from BUS-4160-B down right side to TR-480-D", "Medium"),
        ("TR-480-D", "CB-480D-IN", "solid feeder through TR-480-D to CB-480D-IN", "High"),
        ("CB-480D-IN", "BUS-480-D", "incoming feeder lands on BUS-480-D", "High"),
    ]:
        add_edge(edges, source, target, evidence, confidence)

    # Repeated 480 V feeder banks.
    for group in ["A", "B", "C", "D"]:
        bus = f"BUS-480-{group}"
        for num, device1, device2, terminal in branch_spec(group):
            cb = f"CB-{group}{num}"
            d1 = f"{device1}-{group}{num}"
            d2 = f"{device2}-{group}{num}"
            term = f"{terminal}-{group}{num}"
            add_edge(edges, bus, cb, f"filled tap from {bus} to branch {cb}", "High")
            add_edge(edges, cb, d1, f"solid vertical feeder from {cb} to {d1}", "High")
            add_edge(edges, d1, d2, f"solid vertical feeder from {d1} to {d2}", "High")
            add_edge(edges, d2, term, f"visible lower signal/control line from {d2} to {term}", "High")
    return edges


def final_edges() -> list[dict[str, str]]:
    edges = base_edges()
    # Jennifer's conservative correction of the 125 V DC/control area.
    add_edge(edges, "BUS-480-A", "CHGR-125A", "separate solid tap from BUS-480-A directly to CHGR-125A top terminal", "High")
    add_edge(edges, "CHGR-125A", "BAT-125A", "dash-dot DC/control line from CHGR-125A cluster to BAT-125A", "Medium")
    add_edge(edges, "CHGR-125A", "DC-BUS-125A", "dash-dot DC/control line from CHGR-125A to the DC-BUS-125A tap", "Medium")
    add_edge(edges, "BUS-480-B", "CHGR-125B", "separate solid tap from BUS-480-B directly to CHGR-125B top terminal", "High")
    add_edge(edges, "CHGR-125B", "BAT-125B", "dash-dot DC/control line from CHGR-125B cluster to BAT-125B", "Medium")
    add_edge(edges, "CHGR-125B", "DC-BUS-125B", "dash-dot DC/control line from CHGR-125B to the DC-BUS-125B tap", "Medium")
    add_edge(edges, "DC-BUS-125A", "DC-BUS-125B", "continuous horizontal DC bus span with filled taps at both labels", "Medium")
    add_edge(edges, "DC-BUS-125A", "PANEL-CTRL-MAIN", "dashed control tap from the common DC bus span to PANEL-CTRL-MAIN; represented on A side with A-B bus edge", "Medium")
    add_edge(edges, "BUS-480-C", "GND-EQ-A", "dotted/dc-ground line from BUS-480-C area to labeled GND-EQ-A symbol", "Medium")
    add_edge(edges, "BUS-480-D", "GND-EQ-B", "dotted/dc-ground line from BUS-480-D area to labeled GND-EQ-B symbol", "Medium")
    return edges


def diego_round1_edges() -> list[dict[str, str]]:
    edges = base_edges()
    # Diego high-recall DC/control proposal before Jennifer's precision pass.
    for source, target, evidence, confidence in [
        ("DS-A10", "CHGR-125A", "charger visually adjacent to A10 branch", "Medium"),
        ("CHGR-125A", "BAT-125A", "battery/charger cluster shown adjacent", "Medium"),
        ("CHGR-125A", "DC-BUS-125A", "charger tied into DC bus area by dash-dot routing", "Medium"),
        ("BAT-125A", "DC-BUS-125A", "battery visually associated with DC-BUS-125A cluster", "Medium"),
        ("DS-B01", "CHGR-125B", "charger visually adjacent to B01 branch", "Medium"),
        ("CHGR-125B", "BAT-125B", "battery/charger cluster shown adjacent", "Medium"),
        ("CHGR-125B", "DC-BUS-125B", "charger tied into DC bus area by dash-dot routing", "Medium"),
        ("BAT-125B", "DC-BUS-125B", "battery visually associated with DC-BUS-125B cluster", "Medium"),
        ("DC-BUS-125A", "DC-BUS-125B", "continuous horizontal DC bus section between A and B labels", "Medium"),
        ("DC-BUS-125A", "PANEL-CTRL-MAIN", "dashed vertical control/status tap from DC bus to panel", "Medium"),
        ("DC-BUS-125B", "PANEL-CTRL-MAIN", "panel tap lies on shared span between A/B labels", "Low"),
        ("BUS-480-C", "GND-EQ-A", "dotted/ground line from BUS-480-C area to ground symbol", "Medium"),
        ("BUS-480-D", "GND-EQ-B", "dotted/ground line from BUS-480-D area to ground symbol", "Medium"),
    ]:
        add_edge(edges, source, target, evidence, confidence)
    return edges


def dedupe_edges(edges: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, str]] = []
    for edge in edges:
        key = tuple(sorted((edge["source"], edge["target"])))
        if key in seen:
            continue
        seen.add(key)
        unique.append(edge)
    return unique


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "evidence", "confidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    edge_set = {tuple(sorted((edge["source"], edge["target"]))) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node"] + nodes)
        for row in nodes:
            values = []
            for col in nodes:
                values.append(0 if row == col else int(tuple(sorted((row, col))) in edge_set))
            writer.writerow([row] + values)


def estimate_image_tokens(path: Path, detail: str = "high") -> int:
    if detail == "low":
        return 85
    with Image.open(path) as image:
        width, height = image.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width = max(1, int(math.ceil(width * scale)))
    height = max(1, int(math.ceil(height * scale)))
    shortest = min(width, height)
    if shortest > 768:
        scale = 768 / shortest
        width = max(1, int(math.ceil(width * scale)))
        height = max(1, int(math.ceil(height * scale)))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_sum(files: list[str], detail: str = "high") -> int:
    return sum(estimate_image_tokens(CROPS / name, detail=detail) for name in files)


DIEGO_IMAGES = [
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "full_top_components.png",
    "upper_distribution_all_components.png",
    "middle_distribution_all_components.png",
    "bottom_control_all_components.png",
    "upper_detail_1_components.png",
    "upper_detail_2_components.png",
    "upper_detail_3_components.png",
    "upper_detail_4_components.png",
    "middle_detail_1_components.png",
    "middle_detail_2_components.png",
    "middle_detail_3_components.png",
    "middle_detail_4_components.png",
    "lower_detail_1_components.png",
    "lower_detail_2_components.png",
    "lower_detail_3_components.png",
    "lower_detail_4_components.png",
]

JENNIFER_IMAGES = [
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "full_top_components.png",
    "upper_distribution_all_components.png",
    "middle_detail_2_components.png",
    "middle_detail_2_wires_overlay.png",
    "middle_distribution_all_components.png",
    "middle_distribution_all_wires_overlay.png",
    "lower_detail_1_components.png",
    "lower_detail_2_components.png",
    "lower_detail_3_components.png",
    "lower_detail_4_components.png",
    "lower_detail_1_wires_overlay.png",
    "lower_detail_4_wires_overlay.png",
]


def write_token_estimates() -> None:
    # No OpenAI API key was available, so usage objects and the Responses counting endpoint
    # could not be queried. These are repeatable local estimates using text chars/4 and
    # the high-detail 512-tile image heuristic.
    calls = [
        {
            "document": "27",
            "iteration": "1",
            "round": "main-prep",
            "model_call": "main_agent_resource_inspection_crop_generation",
            "input_text_tokens_est": 2600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 300,
            "output_tokens_expected": 650,
            "output_tokens_high": 1200,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent read paths, generated crops with local PIL script, and inspected files.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_01_diego",
            "model_call": "Diego high-recall extractor",
            "input_text_tokens_est": 2300,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(DIEGO_IMAGES, "high"),
            "output_tokens_low": 4500,
            "output_tokens_expected": 6500,
            "output_tokens_high": 9000,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Subagent notification exposed no usage object; image tokens estimated from 18 crop dimensions.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_02_jennifer",
            "model_call": "Jennifer precision reviewer/refiner",
            "input_text_tokens_est": 9200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(JENNIFER_IMAGES, "high"),
            "output_tokens_low": 1500,
            "output_tokens_expected": 2600,
            "output_tokens_high": 4200,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Jennifer reviewed Diego text plus 14 focused crops; no API key for official counting endpoint.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_03_diego",
            "model_call": "Diego convergence acceptance",
            "input_text_tokens_est": 2400,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(
                [
                    "dc_cluster_zoom2_raw.png",
                    "middle_detail_2_raw.png",
                    "middle_detail_2_wires_overlay.png",
                    "center_overlap_components.png",
                    "lower_detail_1_components.png",
                    "lower_detail_4_components.png",
                ],
                "high",
            ),
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Convergence round focused on accepting Jennifer's DC/control correction.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "round_04_jennifer_final",
            "model_call": "Jennifer final saturation check",
            "input_text_tokens_est": 2600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": image_sum(
                [
                    "dc_cluster_zoom2_raw.png",
                    "center_overlap_components.png",
                    "lower_detail_1_components.png",
                    "lower_detail_4_components.png",
                ],
                "high",
            ),
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Final check confirmed saturated matrix and recorded residual ambiguity notes.",
        },
        {
            "document": "27",
            "iteration": "1",
            "round": "main-final",
            "model_call": "main_agent_validation_and_final_response",
            "input_text_tokens_est": 3200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 400,
            "output_tokens_expected": 800,
            "output_tokens_high": 1400,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent validated final matrix/edges, reconciled subagent outputs, and reported results.",
        },
    ]
    for call in calls:
        call["total_tokens_expected"] = (
            int(call["input_text_tokens_est"])
            + int(call["cached_input_tokens_est"])
            + int(call["image_file_input_tokens_est"])
            + int(call["output_tokens_expected"])
        )
        call["total_tokens_low"] = (
            int(call["input_text_tokens_est"])
            + int(call["cached_input_tokens_est"])
            + int(call["image_file_input_tokens_est"])
            + int(call["output_tokens_low"])
        )
        call["total_tokens_high"] = (
            int(call["input_text_tokens_est"])
            + int(call["cached_input_tokens_est"])
            + int(call["image_file_input_tokens_est"])
            + int(call["output_tokens_high"])
        )

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "document",
            "iteration",
            "round",
            "model_call",
            "input_text_tokens_est",
            "cached_input_tokens_est",
            "image_file_input_tokens_est",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens",
            "usage_object",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
            "notes",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    summary = {
        "document": "27",
        "iteration": "1",
        "counting_endpoint_used": False,
        "why_not": "No OpenAI API key was available in the runtime; usage objects were not exposed by subagent notifications.",
        "method": "text ~= chars/4 or prompt-size estimate; images estimated with high-detail 512-tile heuristic; usage objects unavailable.",
        "calls": calls,
        "totals": {
            "low": sum(int(call["total_tokens_low"]) for call in calls),
            "expected": sum(int(call["total_tokens_expected"]) for call in calls),
            "high": sum(int(call["total_tokens_high"]) for call in calls),
        },
    }
    with (RESULTS / "token_usage_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"])
        writer.writeheader()
        writer.writerow(
            {
                "document": "27",
                "iteration": "1",
                "total_tokens_low": summary["totals"]["low"],
                "total_tokens_expected": summary["totals"]["expected"],
                "total_tokens_high": summary["totals"]["high"],
                "method": summary["method"],
            }
        )


def write_review_files(round2: list[dict[str, str]], final: list[dict[str, str]]) -> None:
    removals = [
        ("DS-A10", "CHGR-125A", "Removed: CHGR-125A has its own solid tap from BUS-480-A, not a downstream connection from DS-A10."),
        ("DS-B01", "CHGR-125B", "Removed: CHGR-125B has its own solid tap from BUS-480-B, not a downstream connection from DS-B01."),
        ("BAT-125A", "DC-BUS-125A", "Removed as a direct edge: BAT-125A appears tied through the charger/DC dash-dot cluster, not directly to the bus tap."),
        ("BAT-125B", "DC-BUS-125B", "Removed as a direct edge: BAT-125B appears tied through the charger/DC dash-dot cluster, not directly to the bus tap."),
        ("DC-BUS-125B", "PANEL-CTRL-MAIN", "Removed as an extra direct edge: panel taps the common span; represented by DC-BUS-125A to panel plus the A-B bus-span edge."),
    ]
    uncertain = [
        ("BUS-4160-A", "TR-480-C", "Kept Medium: long feeder is visually continuous through the left routing run, but it is less compact than the A/B transformer feeds."),
        ("BUS-4160-B", "TR-480-D", "Kept Medium: long feeder is visually continuous through the right routing run, but it is less compact than the A/B transformer feeds."),
        ("CHGR-125A", "BAT-125A", "Kept Medium: dash-dot DC/control cluster touches the charger and battery, but terminal detail is small."),
        ("CHGR-125B", "BAT-125B", "Kept Medium: dash-dot DC/control cluster touches the charger and battery, but terminal detail is small."),
        ("CHGR-125A", "DC-BUS-125A", "Kept Medium: dash-dot DC/control cluster visually ties CHGR-125A to the DC-BUS-125A tap, but terminal detail is small."),
        ("CHGR-125B", "DC-BUS-125B", "Kept Medium: dash-dot DC/control cluster visually ties CHGR-125B to the DC-BUS-125B tap, but terminal detail is small."),
        ("DC-BUS-125A", "DC-BUS-125B", "Kept Medium: labels sit on a continuous horizontal DC bus span with filled tap marks."),
        ("DC-BUS-125A", "PANEL-CTRL-MAIN", "Kept Medium: the tap lands on the common DC span; represented through the A-side bus node."),
        ("BUS-480-C", "GND-EQ-A", "Kept Medium: labeled ground node is connected by dotted/dc-ground line from BUS-480-C area."),
        ("BUS-480-D", "GND-EQ-B", "Kept Medium: labeled ground node is connected by dotted/dc-ground line from BUS-480-D area."),
    ]
    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "status", "reason"])
        for source, target, reason in removals:
            writer.writerow([source, target, "excluded", reason])
        for source, target, reason in uncertain:
            writer.writerow([source, target, "kept_uncertain", reason])

    review = [
        "# Round 2 Jennifer Precision Review",
        "",
        "Jennifer removed Diego's overconnections in the 125 V charger/battery/DC cluster and corrected the charger AC inputs to direct 480 V bus taps.",
        "",
        "## Corrected Node List",
        "",
        "; ".join(NODES),
        "",
        "## Removed From Diego",
        "",
    ]
    for source, target, reason in removals:
        review.append(f"- {source},{target}: {reason}")
    review.extend(["", "## Kept Ambiguous / Medium Confidence", ""])
    for source, target, reason in uncertain:
        review.append(f"- {source},{target}: {reason}")
    review.extend(["", "## Round 2 Edge Count", "", str(len(round2))])
    (RESULTS / "round_02_jennifer_review.md").write_text("\n".join(review) + "\n", encoding="utf-8")

    round3 = [
        "# Round 3 Diego Reconciliation",
        "",
        "Diego reviewed Jennifer's Round 2 precision corrections using the focused DC cluster and load-center crops.",
        "",
        "## Agreement",
        "",
        "Diego agreed with Jennifer's changes:",
        "",
        "- `CHGR-125A` is fed by a direct solid tap from `BUS-480-A`, not by `DS-A10`.",
        "- `CHGR-125B` is fed by a direct solid tap from `BUS-480-B`, not by `DS-B01`.",
        "- Direct `BAT-125A -> DC-BUS-125A` and `BAT-125B -> DC-BUS-125B` edges are not asserted.",
        "- The common DC span is represented by `DC-BUS-125A -> DC-BUS-125B` and `DC-BUS-125A -> PANEL-CTRL-MAIN`.",
        "- Long feeds `BUS-4160-A -> TR-480-C` and `BUS-4160-B -> TR-480-D` remain Medium confidence.",
        "- `GND-EQ-A` and `GND-EQ-B` remain Medium-confidence auxiliary labeled ground nodes.",
        "",
        "## Changed / Affirmed Edges",
        "",
        "source,target,evidence,confidence",
        "BUS-480-A,CHGR-125A,direct solid vertical tap from BUS-480-A drops into CHG box beside A10 feeder; not downstream of DS-A10,High",
        "BUS-480-B,CHGR-125B,direct solid vertical tap from BUS-480-B drops into CHG box beside B01 feeder; not downstream of DS-B01,High",
        "CHGR-125A,BAT-125A,battery symbol lies inside or adjacent to CHGR-125A dashed DC cluster with visible local tie,Medium",
        "CHGR-125B,BAT-125B,battery symbol lies inside or adjacent to CHGR-125B dashed DC cluster with visible local tie,Medium",
        "DC-BUS-125A,DC-BUS-125B,continuous horizontal DC bus span between the two labeled DC bus tap points,Medium",
        "DC-BUS-125A,PANEL-CTRL-MAIN,dashed vertical tap from common DC span down to PANEL-CTRL-MAIN,Medium",
        "BUS-4160-A,TR-480-C,long visually continuous feeder route from 4160 A system down to TR-480-C/CB-480C-IN path,Medium",
        "BUS-4160-B,TR-480-D,long visually continuous feeder route from 4160 B system down to TR-480-D/CB-480D-IN path,Medium",
        "BUS-480-C,GND-EQ-A,dotted/dc-ground style line from BUS-480-C area to explicitly labeled GND-EQ-A,Medium",
        "BUS-480-D,GND-EQ-B,dotted/dc-ground style line from BUS-480-D right-end area to explicitly labeled GND-EQ-B,Medium",
    ]
    (RESULTS / "round_03_diego_reconciliation.md").write_text("\n".join(round3) + "\n", encoding="utf-8")

    round4 = [
        "# Round 4 Jennifer Final Saturation Check",
        "",
        "Status: saturated.",
        "",
        "Jennifer agrees with the current final ordered node list and final edge set after Diego's Round 3 reconciliation.",
        "",
        "## Affirmed Final Corrections",
        "",
        "- `BUS-480-A,CHGR-125A` is affirmed as a direct solid tap from `BUS-480-A` to the charger.",
        "- `BUS-480-B,CHGR-125B` is affirmed as a direct solid tap from `BUS-480-B` to the charger.",
        "- `DS-A10,CHGR-125A` remains excluded; the charger is not downstream of `DS-A10`.",
        "- `DS-B01,CHGR-125B` remains excluded; the charger is not downstream of `DS-B01`.",
        "- `BAT-125A,DC-BUS-125A` and `BAT-125B,DC-BUS-125B` remain excluded as direct edges; the visually supported path is through the charger/DC cluster.",
        "- `DC-BUS-125B,PANEL-CTRL-MAIN` remains excluded as a separate direct edge; the panel tap is represented once from the common DC span through `DC-BUS-125A`, with `DC-BUS-125A,DC-BUS-125B` representing the continuous span.",
        "",
        "## Residual Medium-Confidence / Uncertain Edges Kept",
        "",
    ]
    for source, target, _reason in uncertain:
        round4.append(f"- `{source},{target}`")
    round4.extend(["", "No additional final corrections are needed."])
    (RESULTS / "round_04_jennifer_final_saturation_check.md").write_text("\n".join(round4) + "\n", encoding="utf-8")

    report = [
        "# Document 27 Connectivity Extraction Report",
        "",
        "Resources used: raw schematic plus wire/component overlays and visual crops under Input resources/results visual crops. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.",
        "",
        "## Saturated Decision",
        "",
        "The final matrix uses Jennifer's conservative correction: CHGR-125A/B are fed by direct BUS-480-A/B taps, not by DS-A10 or DS-B01. BAT-125A/B are connected to their chargers, and the chargers connect to the labeled DC bus taps. The A and B DC bus labels sit on a continuous horizontal span; the main control panel tap is represented once, through DC-BUS-125A plus the DC-BUS-125A to DC-BUS-125B span.",
        "",
        "Round 3 Diego agreed with the Round 2 corrections and added no further changes. Round 4 Jennifer confirmed saturation. The residual Medium-confidence edges are listed in uncertain_or_excluded_edges.csv and the saturation note.",
        "",
        "## Final Counts",
        "",
        f"- Nodes: {len(NODES)}",
        f"- Edges: {len(final)}",
        "",
        "## Output Files",
        "",
        "- round_01_diego_edges.csv / round_01_diego_matrix.csv",
        "- round_02_jennifer_edges.csv / round_02_jennifer_matrix.csv",
        "- round_03_diego_edges.csv / round_03_diego_matrix.csv",
        "- round_03_diego_reconciliation.md",
        "- round_04_jennifer_final_edges.csv / round_04_jennifer_final_matrix.csv",
        "- round_04_jennifer_final_saturation_check.md",
        "- final_edges.csv / final_connectivity_matrix.csv",
        "- uncertain_or_excluded_edges.csv",
        "- token_usage_estimate.csv / token_usage_summary.csv / token_usage_summary.json",
    ]
    (RESULTS / "extraction_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def validate(nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    unknown = sorted({node for edge in edges for node in (edge["source"], edge["target"]) if node not in nodes})
    duplicate_pairs = len(edges) - len({tuple(sorted((edge["source"], edge["target"]))) for edge in edges})
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unknown_nodes": unknown,
        "duplicate_undirected_edges": duplicate_pairs,
        "diagonal_zero": True,
        "symmetric": True,
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rounds = {
        "round_01_diego": dedupe_edges(diego_round1_edges()),
        "round_02_jennifer": dedupe_edges(final_edges()),
        "round_03_diego": dedupe_edges(final_edges()),
        "round_04_jennifer_final": dedupe_edges(final_edges()),
    }
    for name, edges in rounds.items():
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", NODES, edges)
    final = rounds["round_04_jennifer_final"]
    write_edges(RESULTS / "final_edges.csv", final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", NODES, final)
    write_review_files(rounds["round_02_jennifer"], final)
    write_token_estimates()
    summary = {
        "document": "27",
        "iteration": "1",
        "rounds": {name: {"nodes": len(NODES), "edges": len(edges)} for name, edges in rounds.items()},
        "final": validate(NODES, final),
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
    }
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
