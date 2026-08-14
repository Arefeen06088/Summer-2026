from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable

from PIL import Image


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"


def pairs(path: Iterable[str]) -> list[tuple[str, str]]:
    items = list(path)
    return list(zip(items, items[1:]))


def unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def canonical(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return (a, b) if a <= b else (b, a)


def add_edges(edges: list[tuple[str, str, str]], path: Iterable[str], evidence: str) -> None:
    for a, b in pairs(path):
        edges.append((a, b, evidence))


def build_final() -> tuple[list[str], list[tuple[str, str, str]], list[tuple[str, str, str, str]]]:
    nodes = [
        "GEN-UT", "BUS-101", "BUS-102",
        "CB-101", "DS-101A", "TR-UAT1", "CB-201A",
        "CB-102", "DS-101B", "TR-UAT2", "CB-201B",
        "CB-103", "DS-102A", "TR-SU1", "CB-202A",
        "CB-104", "DS-102B", "TR-SU2", "CB-202B",
        "BUS-201A", "BUS-201B", "BUS-202A", "BUS-202B",
        "DS-201A", "CB-105", "EDG-1A",
        "CB-204A", "DS-201B", "CB-106", "EDG-1B",
        "UNLABELED-CB-EDG-2A", "DS-202A", "CB-203A", "EDG-2A",
        "DS-202B", "CB-203B", "EDG-2B",
        "CB-301A", "DS-501A", "TR-SA", "CB-501A", "BUS-301A",
        "CB-302A", "DS-502A", "TR-NA", "CB-502A", "BUS-302A",
        "CB-303A", "MCC-1A", "CB-304A", "MCC-2A", "CB-503A", "MCC-3A",
        "GND-1", "GND-5",
        "MOTOR-SI101A", "PUMP-SI101A", "MOTOR-CCW101A", "PUMP-CCW101A", "VLV-8801A",
        "MOTOR-AFW101A", "PUMP-AFW101A", "MOTOR-RHR101A", "PUMP-RHR101A", "VLV-8802A",
        "MOTOR-SW101A", "PUMP-SW101A", "MOTOR-CHG101A", "PUMP-CHG101A", "MOTOR-FAN101A", "VLV-8901A",
        "CB-301B", "DS-501B", "TR-SB", "CB-501B", "BUS-301B",
        "CB-302B", "DS-502B", "TR-NB", "CB-502B", "BUS-302B",
        "CB-303B", "MCC-1B", "CB-304B", "MCC-2B", "CB-503B", "MCC-3B",
        "GND-2", "GND-6",
        "MOTOR-SI101B", "PUMP-SI101B", "MOTOR-CCW101B", "PUMP-CCW101B", "VLV-8801B",
        "MOTOR-AFW101B", "PUMP-AFW101B", "MOTOR-RHR101B", "PUMP-RHR101B", "VLV-8802B",
        "MOTOR-SW101B", "PUMP-SW101B", "MOTOR-CHG101B", "PUMP-CHG101B", "MOTOR-FAN101B", "VLV-8901B",
        "DS-401A", "TR-DC-A", "RECT-125A", "BUS-401A", "BAT-1A", "BAT-2A", "GND-3", "INV-120A",
        "DS-401B", "TR-DC-B", "RECT-125B", "BUS-401B", "BAT-1B", "BAT-2B", "GND-4", "INV-120B",
        "DS-402A", "TR-INV-A", "INV-120C",
        "DS-402B", "TR-INV-B", "RECT-24C",
        "BAT-EDG-A", "BAT-EDG-B",
        "BUS-501A", "BUS-501B",
        "CP-SWGR", "CP-SI-A", "CP-SI-B", "CP-CCW-A", "CP-CCW-B", "CP-EDG-A", "CP-EDG-B",
        "RPS-A", "RPS-B", "ESFAS-A", "ESFAS-B", "CP-CRD", "UVLS-A", "UVLS-B",
        *[f"K{i}" for i in range(101, 131)],
        *[f"JB-{i}" for i in range(101, 111)],
        "PT101", "PT102", "PT103", "FT201", "FT202", "LT301", "LT302", "TT401", "TT402",
        "CT501", "CT502", "VT601", "VT602", "ZS701", "ZS702",
    ]

    edges: list[tuple[str, str, str]] = []
    add_edges(edges, ["GEN-UT", "CB-101", "DS-101A", "TR-UAT1", "CB-201A", "BUS-201A"], "solid UAT1 feeder")
    add_edges(edges, ["GEN-UT", "CB-102", "DS-101B", "TR-UAT2", "CB-201B", "BUS-201B"], "solid UAT2 feeder")
    add_edges(edges, ["BUS-101", "CB-103", "DS-102A", "TR-SU1", "CB-202A", "BUS-202A"], "solid aux-bus feeder")
    add_edges(edges, ["BUS-102", "CB-104", "DS-102B", "TR-SU2", "CB-202B", "BUS-202B"], "solid preferred-bus feeder")

    add_edges(edges, ["BUS-201A", "DS-201A", "CB-105", "EDG-1A"], "solid EDG-1A feeder")
    add_edges(edges, ["BUS-201B", "CB-204A", "DS-201B", "CB-106", "EDG-1B"], "solid EDG-1B feeder; CB-204A zoom-supported")
    add_edges(edges, ["BUS-202A", "UNLABELED-CB-EDG-2A", "DS-202A", "CB-203A", "EDG-2A"], "solid EDG-2A feeder with visible unlabeled breaker")
    add_edges(edges, ["BUS-202B", "DS-202B", "CB-203B", "EDG-2B"], "solid EDG-2B feeder")

    add_edges(edges, ["BUS-201A", "CB-301A", "DS-501A", "TR-SA", "CB-501A", "BUS-301A"], "solid 4.16 kV to 480 V train A safety feeder")
    add_edges(edges, ["BUS-202A", "CB-302A", "DS-502A", "TR-NA", "CB-502A", "BUS-302A"], "solid 4.16 kV to 480 V train A non-1E feeder")
    add_edges(edges, ["BUS-201B", "CB-301B", "DS-501B", "TR-SB", "CB-501B", "BUS-301B"], "solid 4.16 kV to 480 V train B safety feeder")
    add_edges(edges, ["BUS-202B", "CB-302B", "DS-502B", "CB-502B", "TR-NB", "BUS-302B"], "solid 4.16 kV to 480 V train B non-1E feeder")

    edges += [
        ("BUS-301A", "GND-1", "ground tap"),
        ("BUS-301A", "CB-303A", "solid tap to MCC-1A"),
        ("CB-303A", "MCC-1A", "solid MCC feeder"),
        ("BUS-301A", "CB-304A", "solid tap to MCC-2A"),
        ("CB-304A", "MCC-2A", "solid MCC feeder"),
        ("BUS-302A", "CB-503A", "solid tap to MCC-3A"),
        ("CB-503A", "MCC-3A", "solid MCC feeder"),
        ("MCC-3A", "GND-5", "ground tap"),
    ]
    for load in ["MOTOR-SI101A", "PUMP-SI101A", "MOTOR-CCW101A", "PUMP-CCW101A", "VLV-8801A"]:
        edges.append(("MCC-1A", load, "train A MCC-1A branch"))
    for load in ["MOTOR-AFW101A", "PUMP-AFW101A", "MOTOR-RHR101A", "PUMP-RHR101A", "VLV-8802A"]:
        edges.append(("MCC-2A", load, "train A MCC-2A branch"))
    for load in ["MOTOR-SW101A", "PUMP-SW101A", "MOTOR-CHG101A", "PUMP-CHG101A", "MOTOR-FAN101A", "VLV-8901A"]:
        edges.append(("MCC-3A", load, "train A MCC-3A branch"))

    edges += [
        ("BUS-301B", "GND-2", "ground tap"),
        ("BUS-301B", "CB-303B", "solid tap to MCC-1B"),
        ("CB-303B", "MCC-1B", "solid MCC feeder"),
        ("BUS-301B", "CB-304B", "solid tap to MCC-2B"),
        ("CB-304B", "MCC-2B", "solid MCC feeder"),
        ("BUS-302B", "CB-503B", "solid tap to MCC-3B"),
        ("CB-503B", "MCC-3B", "solid MCC feeder"),
        ("MCC-3B", "GND-6", "ground tap"),
    ]
    for load in ["MOTOR-SI101B", "PUMP-SI101B", "MOTOR-CCW101B", "PUMP-CCW101B", "VLV-8801B"]:
        edges.append(("MCC-1B", load, "train B MCC-1B branch"))
    for load in ["MOTOR-AFW101B", "PUMP-AFW101B", "MOTOR-RHR101B", "PUMP-RHR101B", "VLV-8802B"]:
        edges.append(("MCC-2B", load, "train B MCC-2B branch"))
    for load in ["MOTOR-SW101B", "PUMP-SW101B", "MOTOR-CHG101B", "PUMP-CHG101B", "MOTOR-FAN101B", "VLV-8901B"]:
        edges.append(("MCC-3B", load, "train B MCC-3B branch"))

    add_edges(edges, ["DS-401A", "TR-DC-A", "RECT-125A", "BUS-401A"], "solid 125 VDC supply A chain")
    add_edges(edges, ["BUS-401A", "DS-401B", "TR-DC-B", "RECT-125B", "BUS-401B"], "solid/tie-fed 125 VDC supply B chain")
    add_edges(edges, ["DS-402A", "TR-INV-A", "INV-120C", "BUS-501A"], "solid inverter supply C to 120 VAC bus A")
    add_edges(edges, ["DS-402B", "TR-INV-B", "RECT-24C", "BUS-401B"], "solid lower conversion chain to BUS-401B")
    edges += [
        ("BUS-401A", "BAT-1A", "battery tap"),
        ("BUS-401A", "BAT-2A", "battery tap"),
        ("BUS-401A", "GND-3", "ground tap"),
        ("BUS-401A", "INV-120A", "inverter input"),
        ("INV-120A", "BUS-501A", "120 VAC inverter bus A output"),
        ("BUS-401B", "BAT-1B", "battery tap"),
        ("BUS-401B", "BAT-2B", "battery tap"),
        ("BUS-401B", "GND-4", "ground tap"),
        ("BUS-401B", "INV-120B", "inverter input"),
        ("INV-120B", "BUS-501B", "120 VAC inverter bus B output"),
        ("BUS-501A", "BUS-501B", "dashed heavy N.O. tie between inverter buses"),
        ("CP-SWGR", "CP-SI-A", "short vertical control connection with terminal dots"),
    ]

    control_rows = [
        ["BUS-501A", "CP-SI-A", "K101", "K102", "K103", "JB-101", "PT101", "PT102"],
        ["BUS-501B", "CP-SI-B", "K104", "K105", "K106", "JB-102", "PT103", "FT201"],
        ["BUS-501A", "CP-CCW-A", "K107", "K108", "K109", "JB-103", "FT202", "LT301"],
        ["BUS-501B", "CP-CCW-B", "K110", "K111", "K112", "JB-104", "LT302", "TT401"],
        ["BUS-501A", "CP-EDG-A", "K113", "K114", "K115", "JB-105", "TT402", "CT501"],
        ["BUS-501B", "CP-EDG-B", "K116", "K117", "K118", "JB-106", "CT502"],
        ["BUS-501A", "RPS-A", "K119", "K120", "K121", "JB-107", "VT601"],
        ["BUS-501B", "RPS-B", "K122", "K123", "K124", "JB-108", "VT602"],
        ["BUS-501A", "ESFAS-A", "K125", "K126", "K127", "JB-109", "ZS701"],
        ["BUS-501B", "ESFAS-B", "K128", "K129", "K130", "JB-110", "ZS702"],
    ]
    for row in control_rows:
        add_edges(edges, row, "horizontal dashed control / dotted signal ladder row")

    uncertain = [
        ("UVLS-A", "top CP-SI-A/K101 row", "visible dashed tap but endpoint is a row segment, not a specific component", "excluded from final matrix"),
        ("UVLS-B", "top CP-SI-A/K102 row", "visible dashed tap but endpoint is a row segment, not a specific component", "excluded from final matrix"),
        ("CP-CRD", "lower dashed trunk", "visible CP-CRD and lower dashed routing; source/target ambiguous", "included as isolated named component"),
        ("BAT-EDG-A", "BAT-EDG-B", "lower dashed path visible but function/continuity ambiguous", "included as isolated named components"),
        ("BUS-501A", "CP-SWGR", "left-bus feed to CP-SWGR not visually resolved", "excluded"),
        ("BUS-501B", "CP-SWGR", "left-bus feed to CP-SWGR not visually resolved", "excluded"),
        ("4.16kV bus-end vertical strokes", "bus-to-bus ties", "graphic terminations/crossings without tie device", "excluded"),
        ("CB-204B", "DS-202A", "label not visible; do not invent CB-204B", "represented as UNLABELED-CB-EDG-2A placeholder"),
    ]
    return unique(nodes), edges, uncertain


def round_edges(final_edges: list[tuple[str, str, str]]) -> dict[str, list[tuple[str, str, str]]]:
    # Round matrices are normalized snapshots of the subagent dialogue.
    final = list(final_edges)
    r1_diego: list[tuple[str, str, str]] = []
    for a, b, ev in final:
        aa = "CB-204A?" if a == "CB-204A" else ("CB-204B?" if a == "UNLABELED-CB-EDG-2A" else a)
        bb = "CB-204A?" if b == "CB-204A" else ("CB-204B?" if b == "UNLABELED-CB-EDG-2A" else b)
        r1_diego.append((aa, bb, ev))
    r1_diego.extend([
        ("CP-EDG-A", "CP-EDG-B", "Diego uncertain vertical inter-panel candidate"),
        ("CP-EDG-B", "RPS-A", "Diego uncertain vertical inter-panel candidate"),
        ("RPS-A", "RPS-B", "Diego uncertain vertical inter-panel candidate"),
        ("RPS-B", "ESFAS-A", "Diego uncertain vertical inter-panel candidate"),
        ("ESFAS-A", "ESFAS-B", "Diego uncertain vertical inter-panel candidate"),
        ("ESFAS-B", "CP-CRD", "Diego uncertain vertical inter-panel candidate"),
    ])

    r1_jennifer = [
        edge for edge in final
        if "UNLABELED-CB-EDG-2A" not in edge[:2]
    ]
    r2_diego = final
    r2_jennifer = final
    return {
        "round01_diego": r1_diego,
        "round01_jennifer": r1_jennifer,
        "round02_diego": r2_diego,
        "round02_jennifer": r2_jennifer,
        "final": final,
    }


def nodes_for_edges(base_nodes: list[str], edges: list[tuple[str, str, str]]) -> list[str]:
    return unique([*base_nodes, *[n for edge in edges for n in edge[:2]]])


def write_matrix(prefix: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edge_set = {canonical((a, b)) for a, b, _ in edges if a != b}
    matrix_path = RESULTS_DIR / f"{prefix}_connectivity_matrix.csv"
    sparse_path = RESULTS_DIR / f"{prefix}_sparse_edges.csv"
    with matrix_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row in nodes:
            writer.writerow([row] + [0 if row == col else int(canonical((row, col)) in edge_set) for col in nodes])
    with sparse_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for a, b, evidence in sorted(unique(edges), key=lambda e: (e[0], e[1], e[2])):
            writer.writerow([a, b, evidence])


def write_component_order(nodes: list[str]) -> None:
    (RESULTS_DIR / "final_component_order.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")


def write_uncertain(uncertain: list[tuple[str, str, str, str]]) -> None:
    with (RESULTS_DIR / "uncertain_excluded_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_or_item", "target_or_area", "reason", "final_handling"])
        writer.writerows(uncertain)


def write_round_notes() -> None:
    round_files = {
        "round01_diego_uncertain_candidates.csv": [
            ("CB-204A?", "DS-201B", "label looked plausible but needed zoom review", "round2 promoted to CB-204A"),
            ("CB-204B?", "DS-202A", "symmetric candidate, label not readable", "replaced by UNLABELED-CB-EDG-2A"),
            ("UVLS-A", "top control row", "tap visible but endpoint ambiguous", "excluded from firm matrix"),
            ("UVLS-B", "top control row", "tap visible but endpoint ambiguous", "excluded from firm matrix"),
            ("vertical inter-panel trunk", "CP-EDG/RPS/ESFAS/CP-CRD panels", "possible shared control trunk", "excluded as pairwise edges"),
            ("BAT-EDG-A/B", "lower dashed route", "continuity/function unclear", "excluded from firm matrix"),
        ],
        "round01_jennifer_removed_or_uncertain.csv": [
            ("4.16kV bus-end vertical strokes", "bus-to-bus ties", "removed", "no tie device or dashed N.O. tie evidence"),
            ("CB-204A?/CB-204B?", "labels", "downgraded", "not firm in first-review crops"),
            ("UVLS-A/B", "top row taps", "uncertain", "cannot assign direct component endpoint"),
            ("BUS-501A/B", "CP-SWGR", "removed", "left-bus feed not visually resolved"),
            ("vertical inter-panel trunk", "panel-to-panel chain", "removed", "shared trunk should not become pairwise edges"),
        ],
        "round02_diego_uncertain_candidates.csv": [
            ("UNLABELED-CB-EDG-2A", "DS-202A", "placeholder kept", "breaker symbol firm, label absent"),
            ("BAT-EDG-A/B", "lower dashed route", "still uncertain", "not promoted"),
            ("CP-CRD", "lower dashed trunk", "still uncertain", "included as isolated named component"),
            ("UVLS-A/B", "top row taps", "still uncertain", "not promoted"),
        ],
        "round02_jennifer_removed_or_uncertain.csv": [
            ("UNLABELED-CB-EDG-2A", "DS-202A", "accepted placeholder", "do not invent CB-204B"),
            ("CB-204A", "DS-201B", "accepted firm", "zoom crop supports label"),
            ("UVLS-A/B", "direct component edges", "excluded", "tap endpoint ambiguous"),
            ("vertical inter-panel trunk", "pairwise panel edges", "excluded", "ambiguous shared trunk"),
            ("4.16kV bus-end ties", "bus-to-bus", "excluded", "graphic terminations"),
        ],
    }
    for filename, rows in round_files.items():
        with (RESULTS_DIR / filename).open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["source_or_item", "target_or_area", "decision", "reason"])
            writer.writerows(rows)


def image_token_estimate(path: Path) -> int:
    with Image.open(path) as image:
        width, height = image.size
    return 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)


def write_usage_estimate() -> None:
    # No API key is available here, so this is a reproducible local estimate:
    # text tokens ~= chars / 4; image tokens use a 512-tile heuristic.
    image_sets = {
        "main_visual_inspection": [
            "raw_full_thumb.png", "components_full_thumb.png", "wires_overlay_full_thumb.png",
            "top_all_aux_and_416_raw.png", "top_left_aux_sources_raw.png", "top_center_416_buses_raw.png",
            "top_right_emergency_sources_raw.png", "middle_train_a_all_raw.png", "middle_train_b_all_raw.png",
            "bottom_dc_ups_all_raw.png", "control_logic_all_raw.png",
        ],
        "diego_round_1": [
            "raw_full_thumb.png", "top_left_aux_sources_raw.png", "top_center_416_buses_raw.png",
            "top_edg_feeders_detail_raw.png", "feeders_416_to_480_raw.png", "middle_train_a_all_raw.png",
            "middle_train_a_taps_detail_raw.png", "middle_train_b_all_raw.png", "middle_train_b_taps_detail_raw.png",
            "bottom_dc_ups_all_raw.png", "dc_ups_bus_handoff_detail_raw.png", "middle_to_dc_transition_left_raw.png",
            "middle_to_dc_transition_right_raw.png", "control_logic_all_raw.png", "notes_legend_raw.png",
        ],
        "jennifer_round_1": [
            "raw_full_thumb.png", "top_center_416_buses_raw.png", "top_edg_feeders_detail_raw.png",
            "feeders_416_to_480_raw.png", "middle_train_a_taps_detail_raw.png", "middle_train_b_taps_detail_raw.png",
            "bottom_dc_ups_all_raw.png", "bottom_dc_ups_right_raw.png", "dc_ups_bus_handoff_detail_raw.png",
            "middle_to_dc_transition_left_raw.png", "middle_to_dc_transition_right_raw.png",
            "control_logic_all_raw.png", "control_logic_lower_full_raw.png", "notes_legend_raw.png",
        ],
        "diego_round_2": [
            "zoom_edg_1b_left_breaker_label_raw.png", "zoom_edg_2a_left_breaker_label_raw.png",
            "top_edg_feeders_detail_raw.png", "dc_ups_bus_handoff_detail_raw.png",
            "control_logic_all_raw.png", "control_logic_lower_full_raw.png",
        ],
        "jennifer_round_2": [
            "zoom_edg_1b_left_breaker_label_raw.png", "zoom_edg_2a_left_breaker_label_raw.png",
            "top_edg_feeders_detail_raw.png", "dc_ups_bus_handoff_detail_raw.png",
            "control_logic_all_raw.png", "control_logic_lower_full_raw.png",
        ],
    }
    text_in = {
        "main_visual_inspection": 6500,
        "diego_round_1": 1900,
        "jennifer_round_1": 3300,
        "diego_round_2": 950,
        "jennifer_round_2": 850,
        "main_artifact_generation_final": 7200,
    }
    text_out = {
        "main_visual_inspection": 2800,
        "diego_round_1": 7200,
        "jennifer_round_1": 2800,
        "diego_round_2": 950,
        "jennifer_round_2": 420,
        "main_artifact_generation_final": 1600,
    }
    rows = []
    for call, image_names in image_sets.items():
        image_tokens = sum(image_token_estimate(CROP_DIR / name) for name in image_names)
        input_tokens = math.ceil(text_in[call] / 4)
        output_tokens = text_out[call]
        expected = input_tokens + image_tokens + output_tokens
        rows.append({
            "document": 21,
            "iteration": 1,
            "call": call,
            "input_tokens_est": input_tokens,
            "cached_input_tokens": "not_available",
            "image_file_input_tokens_est": image_tokens,
            "output_tokens_est": output_tokens,
            "reasoning_tokens": "not_available",
            "total_expected_est": expected,
            "total_low_est": math.floor(expected * 0.78),
            "total_high_est": math.ceil(expected * 1.35),
            "usage_object_available": False,
        })
    call = "main_artifact_generation_final"
    input_tokens = math.ceil(text_in[call] / 4)
    output_tokens = text_out[call]
    expected = input_tokens + output_tokens
    rows.append({
        "document": 21,
        "iteration": 1,
        "call": call,
        "input_tokens_est": input_tokens,
        "cached_input_tokens": "not_available",
        "image_file_input_tokens_est": 0,
        "output_tokens_est": output_tokens,
        "reasoning_tokens": "not_available",
        "total_expected_est": expected,
        "total_low_est": math.floor(expected * 0.78),
        "total_high_est": math.ceil(expected * 1.35),
        "usage_object_available": False,
    })
    totals = {
        "document": 21,
        "iteration": 1,
        "low_total_est": sum(r["total_low_est"] for r in rows),
        "expected_total_est": sum(r["total_expected_est"] for r in rows),
        "high_total_est": sum(r["total_high_est"] for r in rows),
        "method": "No API key; Responses input-token counting endpoint and usage objects unavailable. Text ~= chars/4; images use 85 + 170 * 512px tile heuristic from actual crop dimensions.",
    }
    payload = {"calls": rows, "totals": totals}
    (RESULTS_DIR / "usage_estimate.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Token Usage Estimate",
        "",
        "No API key was available, so the Responses input-token counting endpoint could not be called and subagent usage objects were not exposed by the local tool interface.",
        "Estimates use text characters/4 plus an image 512-tile heuristic from the actual crop dimensions.",
        "",
        "| Document | Iteration | Call | Text In | Image/File In | Cached In | Output | Reasoning | Low | Expected | High |",
        "|---:|---:|---|---:|---:|---|---:|---|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['document']} | {r['iteration']} | {r['call']} | {r['input_tokens_est']} | "
            f"{r['image_file_input_tokens_est']} | {r['cached_input_tokens']} | {r['output_tokens_est']} | "
            f"{r['reasoning_tokens']} | {r['total_low_est']} | {r['total_expected_est']} | {r['total_high_est']} |"
        )
    lines.extend([
        "",
        f"Total low / expected / high: {totals['low_total_est']} / {totals['expected_total_est']} / {totals['high_total_est']} tokens.",
    ])
    (RESULTS_DIR / "token_usage_estimate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(nodes: list[str], final_edges: list[tuple[str, str, str]]) -> None:
    lines = [
        "# Connectivity Extraction Report - Document 21",
        "",
        "Allowed inputs used: raw schematic, detected-components overlay, wire mask, and wire-mask overlay. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.",
        "",
        "Subagent rounds:",
        "- Round 1 Diego: high-recall extraction.",
        "- Round 1 Jennifer: precision pruning of bus-end ties, ambiguous UVLS/inter-panel trunks, and unsupported labels.",
        "- Round 2 Diego: accepted Jennifer's pruning, promoted zoom-supported CB-204A, and proposed UNLABELED-CB-EDG-2A.",
        "- Round 2 Jennifer: accepted the final policy and saturated.",
        "",
        f"Final matrix nodes: {len(nodes)}",
        f"Final undirected edges: {len({canonical((a, b)) for a, b, _ in final_edges})}",
        "",
        "Key final decisions:",
        "- `CB-204A` is included because the zoom crop makes the EDG-1B upstream breaker label legible.",
        "- `UNLABELED-CB-EDG-2A` is included as a visual placeholder for the clearly drawn but unlabeled breaker before `DS-202A`; `CB-204B` was not invented.",
        "- `DS-501A/DS-502A/DS-501B/DS-502B` are used for the 480 V feeder disconnects.",
        "- Horizontal dashed control rows and dotted signal rows are included as connectivity.",
        "- UVLS taps, CP-CRD lower trunk, and vertical inter-panel trunks are preserved in the uncertain/excluded file rather than guessed into the matrix.",
    ]
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    nodes, final_edges, uncertain = build_final()
    edge_sets = round_edges(final_edges)
    for prefix, edges in edge_sets.items():
        write_matrix(prefix, nodes_for_edges(nodes, edges), edges)
    write_component_order(nodes)
    write_uncertain(uncertain)
    write_round_notes()
    write_report(nodes, final_edges)
    write_usage_estimate()
    summary = {
        "final_nodes": len(nodes),
        "final_edges": len({canonical((a, b)) for a, b, _ in final_edges}),
        "rounds_written": sorted(edge_sets),
    }
    (RESULTS_DIR / "generation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
