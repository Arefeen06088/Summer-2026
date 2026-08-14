from __future__ import annotations

import csv
import math
import os
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + components")
RESULTS = BASE / "results"


NODES = [
    "GRID-345-01", "SUT-2A", "CB-402A", "BUS-4160-N2A", "GEN-U2",
    "UAT-2A", "CB-401A", "UAT-2B", "CB-401B", "BUS-4160-N2B",
    "GRID-345-02", "SUT-2B", "CB-402B", "CB-TIE-4160", "EDG-2A",
    "CB-EDG-A", "BUS-4160-S2A", "EDG-2C", "CB-EDG-C", "TR-480-2A",
    "BUS-480-E2A", "CT-4160A", "PT-4160A", "RELAY-50/51A", "RELAY-27A",
    "RELAY-86A", "TR-480-N2A", "BUS-480-N2A", "DS-480-A", "DS-480-B",
    "BUS-480-N2B", "TR-480-N2B", "EDG-2B", "CB-EDG-B", "BUS-4160-S2B",
    "TR-480-2B", "BUS-480-E2B", "CT-4160B", "PT-4160B", "RELAY-50/51B",
    "RELAY-27B", "RELAY-86B", "GND-A", "GND-B", "MCC-2A1",
    "CB-51A", "PUMP-SI-2A", "CB-52A", "PUMP-RHR-2A", "CB-53A",
    "PUMP-CS-2A", "CB-54A", "PUMP-CCW-2A", "MCC-2A2", "CB-55A",
    "FAN-CRE-2A", "CB-56A", "MOV-8801A", "CB-57A", "MOV-8802A",
    "CB-58A", "PUMP-AF-2A", "PN-480-A", "PUMP-CHG-2A", "MOV-8810A",
    "VLV-HV-302A", "FAN-VENT-2A", "MCC-2C", "CB-N1", "CHGR-125A",
    "BAT-2A", "BUS-125DC-A", "INV-120A", "BUS-120AC-A", "FUSE-125A",
    "PN-125A", "FUSE-120A", "PN-120A", "CP-ESFAS-A", "CP-RPS-A",
    "JB-2A1", "RELAY-K1A", "MCC-2D", "CB-N2", "PUMP-CHG-2B",
    "FAN-VENT-2B", "MCC-2B1", "CB-51B", "PUMP-SI-2B", "CB-52B",
    "PUMP-RHR-2B", "CB-53B", "PUMP-CS-2B", "CB-54B", "PUMP-CCW-2B",
    "MCC-2B2", "CB-55B", "FAN-CRE-2B", "CB-56B", "MOV-8801B",
    "CB-57B", "MOV-8802B", "CB-58B", "PUMP-AF-2B", "PN-480-B",
    "MOV-8810B", "VLV-HV-302B", "CHGR-125B", "BAT-2B", "BUS-125DC-B",
    "INV-120B", "BUS-120AC-B", "FUSE-125B", "PN-125B", "FUSE-120B",
    "PN-120B", "CP-ESFAS-B", "CP-RPS-B", "JB-2B1", "RELAY-K1B",
]


DIEGO_ROUND1_PAIRS = [
    ("GRID-345-01", "SUT-2A"),
    ("SUT-2A", "CB-402A"),
    ("CB-402A", "BUS-4160-N2A"),
    ("GEN-U2", "UAT-2A"),
    ("UAT-2A", "CB-401A"),
    ("CB-401A", "BUS-4160-N2A"),
    ("GEN-U2", "UAT-2B"),
    ("UAT-2B", "CB-401B"),
    ("CB-401B", "BUS-4160-N2B"),
    ("GRID-345-02", "SUT-2B"),
    ("SUT-2B", "CB-402B"),
    ("CB-402B", "BUS-4160-N2B"),
    ("BUS-4160-N2A", "CB-TIE-4160"),
    ("CB-TIE-4160", "BUS-4160-N2B"),
    ("EDG-2A", "CB-EDG-A"),
    ("CB-EDG-A", "BUS-4160-S2A"),
    ("BUS-4160-N2A", "BUS-4160-S2A"),
    ("EDG-2C", "CB-EDG-C"),
    ("CB-EDG-C", "BUS-4160-S2A"),
    ("EDG-2B", "CB-EDG-B"),
    ("CB-EDG-B", "BUS-4160-S2B"),
    ("BUS-4160-N2B", "BUS-4160-S2B"),
    ("BUS-4160-S2A", "TR-480-2A"),
    ("TR-480-2A", "BUS-480-E2A"),
    ("BUS-4160-N2A", "TR-480-N2A"),
    ("TR-480-N2A", "BUS-480-N2A"),
    ("BUS-4160-N2B", "TR-480-N2B"),
    ("TR-480-N2B", "BUS-480-N2B"),
    ("BUS-4160-S2B", "TR-480-2B"),
    ("TR-480-2B", "BUS-480-E2B"),
    ("BUS-480-N2A", "DS-480-A"),
    ("DS-480-A", "DS-480-B"),
    ("DS-480-B", "BUS-480-N2B"),
    ("BUS-480-E2A", "GND-A"),
    ("BUS-480-E2B", "GND-B"),
    ("BUS-4160-S2A", "CT-4160A"),
    ("CT-4160A", "RELAY-50/51A"),
    ("RELAY-50/51A", "RELAY-86A"),
    ("BUS-4160-S2A", "PT-4160A"),
    ("PT-4160A", "RELAY-27A"),
    ("RELAY-27A", "RELAY-86A"),
    ("BUS-4160-S2B", "CT-4160B"),
    ("CT-4160B", "RELAY-50/51B"),
    ("RELAY-50/51B", "RELAY-86B"),
    ("BUS-4160-S2B", "PT-4160B"),
    ("PT-4160B", "RELAY-27B"),
    ("RELAY-27B", "RELAY-86B"),
    ("BUS-480-E2A", "MCC-2A1"),
    ("MCC-2A1", "CB-51A"),
    ("CB-51A", "PUMP-SI-2A"),
    ("MCC-2A1", "CB-52A"),
    ("CB-52A", "PUMP-RHR-2A"),
    ("MCC-2A1", "CB-53A"),
    ("CB-53A", "PUMP-CS-2A"),
    ("MCC-2A1", "CB-54A"),
    ("CB-54A", "PUMP-CCW-2A"),
    ("BUS-480-E2A", "MCC-2A2"),
    ("MCC-2A2", "CB-55A"),
    ("CB-55A", "FAN-CRE-2A"),
    ("MCC-2A2", "CB-56A"),
    ("CB-56A", "MOV-8801A"),
    ("MCC-2A2", "CB-57A"),
    ("CB-57A", "MOV-8802A"),
    ("MCC-2A2", "CB-58A"),
    ("CB-58A", "PUMP-AF-2A"),
    ("BUS-480-E2A", "PN-480-A"),
    ("PN-480-A", "PUMP-CHG-2A"),
    ("PN-480-A", "MOV-8810A"),
    ("PN-480-A", "VLV-HV-302A"),
    ("PN-480-A", "FAN-VENT-2A"),
    ("BUS-480-N2A", "CB-N1"),
    ("CB-N1", "CHGR-125A"),
    ("CHGR-125A", "BAT-2A"),
    ("CHGR-125A", "BUS-125DC-A"),
    ("BAT-2A", "BUS-125DC-A"),
    ("BUS-125DC-A", "INV-120A"),
    ("INV-120A", "BUS-120AC-A"),
    ("BUS-125DC-A", "FUSE-125A"),
    ("FUSE-125A", "PN-125A"),
    ("PN-125A", "CP-ESFAS-A"),
    ("BUS-120AC-A", "FUSE-120A"),
    ("FUSE-120A", "PN-120A"),
    ("PN-120A", "CP-RPS-A"),
    ("MOV-8801A", "JB-2A1"),
    ("JB-2A1", "RELAY-K1A"),
    ("RELAY-K1A", "CP-ESFAS-A"),
    ("BUS-480-N2B", "CB-N2"),
    ("CB-N2", "MCC-2D"),
    ("MCC-2D", "PUMP-CHG-2B"),
    ("MCC-2D", "FAN-VENT-2B"),
    ("BUS-480-E2B", "MCC-2B1"),
    ("MCC-2B1", "CB-51B"),
    ("CB-51B", "PUMP-SI-2B"),
    ("MCC-2B1", "CB-52B"),
    ("CB-52B", "PUMP-RHR-2B"),
    ("MCC-2B1", "CB-53B"),
    ("CB-53B", "PUMP-CS-2B"),
    ("MCC-2B1", "CB-54B"),
    ("CB-54B", "PUMP-CCW-2B"),
    ("BUS-480-E2B", "MCC-2B2"),
    ("MCC-2B2", "CB-55B"),
    ("CB-55B", "FAN-CRE-2B"),
    ("MCC-2B2", "CB-56B"),
    ("CB-56B", "MOV-8801B"),
    ("MCC-2B2", "CB-57B"),
    ("CB-57B", "MOV-8802B"),
    ("MCC-2B2", "CB-58B"),
    ("CB-58B", "PUMP-AF-2B"),
    ("BUS-480-E2B", "PN-480-B"),
    ("PN-480-B", "MOV-8810B"),
    ("PN-480-B", "CHGR-125B"),
    ("CHGR-125B", "BUS-125DC-B"),
    ("BAT-2B", "BUS-125DC-B"),
    ("BUS-125DC-B", "INV-120B"),
    ("INV-120B", "BUS-120AC-B"),
    ("BUS-125DC-B", "FUSE-125B"),
    ("FUSE-125B", "PN-125B"),
    ("PN-125B", "CP-ESFAS-B"),
    ("PN-125B", "VLV-HV-302B"),
    ("BUS-120AC-B", "FUSE-120B"),
    ("FUSE-120B", "PN-120B"),
    ("PN-120B", "CP-RPS-B"),
    ("MOV-8801B", "JB-2B1"),
    ("JB-2B1", "RELAY-K1B"),
    ("RELAY-K1B", "CP-ESFAS-B"),
]


PROMOTED_AFTER_REVIEW = [
    ("CB-N1", "MCC-2C"),
    ("MCC-2C", "PUMP-CHG-2A"),
    ("MCC-2C", "VLV-HV-302A"),
    ("MCC-2C", "FAN-VENT-2A"),
    ("CB-N2", "CHGR-125B"),
    ("CHGR-125B", "BAT-2B"),
    ("PN-480-B", "VLV-HV-302B"),
]


REMOVED_AFTER_REVIEW = {
    tuple(sorted(edge))
    for edge in [
        ("PN-480-A", "PUMP-CHG-2A"),
        ("PN-480-A", "VLV-HV-302A"),
        ("PN-480-A", "FAN-VENT-2A"),
        ("PN-480-B", "CHGR-125B"),
        ("PN-125B", "VLV-HV-302B"),
    ]
}


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def edge_type(source: str, target: str) -> str:
    joined = f"{source} {target}"
    if "GND" in joined:
        return "ground_reference"
    if "CT-" in joined or "PT-" in joined or "50/51" in joined or "27" in joined or "86" in joined:
        return "sensing_control"
    if "JB-" in joined or "RELAY-K" in joined or "CP-" in joined:
        return "control"
    return "solid_power"


def edge_record(source: str, target: str, note: str = "") -> tuple[str, str, str, str]:
    etype = edge_type(source, target)
    evidence = note or "Visually supported by a continuous line, filled bus tap, or clear terminal-to-terminal path in the raw/overlay crops."
    return source, target, etype, evidence


DIEGO_ROUND1_EDGES = [edge_record(source, target) for source, target in DIEGO_ROUND1_PAIRS]

FINAL_PAIRS = [pair for pair in DIEGO_ROUND1_PAIRS if edge_key(*pair) not in REMOVED_AFTER_REVIEW] + PROMOTED_AFTER_REVIEW
FINAL_EDGES = [
    edge_record(source, target, "Saturated Diego/Jennifer review accepted this edge after precision ownership review." if edge_key(source, target) in {edge_key(*p) for p in PROMOTED_AFTER_REVIEW} else "")
    for source, target in FINAL_PAIRS
]


UNCERTAIN_EDGES = [
    ("CB-EDG-C", "BUS-4160-S2B", "Center EDG feeder may bridge toward B, but filled endpoint is not clean."),
    ("MOV-8802A", "JB-2A1", "Dashed route is plausible, but endpoint ownership is congested."),
    ("MOV-8802B", "JB-2B1", "Dashed route is plausible, but endpoint ownership is congested."),
    ("PUMP-SI/RHR/CS/CCW branches A/B", "RELAY-K1A/K1B", "Dashed interlock bundles pass nearby but exact branch terminals are not safe."),
    ("CP-RPS-A", "CP-ESFAS-A", "Adjacent cabinets/routing without clear direct terminal."),
    ("CP-RPS-B", "CP-ESFAS-B", "Adjacent cabinets/routing without clear direct terminal."),
    ("CP-ESFAS-A", "RELAY-86A", "Plausible trip/control route but no clean endpoint-to-endpoint evidence."),
    ("CP-ESFAS-B", "RELAY-86B", "Plausible trip/control route but no clean endpoint-to-endpoint evidence."),
    ("BUS-480-E2A", "BUS-480-N2A", "Nearby buses but no direct tie beyond shown devices."),
    ("BUS-480-E2B", "BUS-480-N2B", "Nearby buses but no direct tie beyond shown devices."),
    ("dashed status/interlock bundles", "raceway paths", "Excluded where dashed paths pass through corridors without unambiguous terminal endpoints."),
]


REJECTED_EDGES = [
    ("PN-480-A", "PUMP-CHG-2A", "Jennifer/Diego R2 found MCC-2C owns this A-side load drop."),
    ("PN-480-A", "VLV-HV-302A", "Jennifer/Diego R2 found MCC-2C owns this A-side load drop."),
    ("PN-480-A", "FAN-VENT-2A", "Jennifer/Diego R2 found MCC-2C owns this A-side load drop."),
    ("PN-480-B", "CHGR-125B", "Unsupported; CHGR-125B is fed from the CB-N2 side."),
    ("PN-125B", "VLV-HV-302B", "Unsupported; VLV-HV-302B is owned by PN-480-B."),
    ("TB01-TB15", "matrix nodes", "Terminal references only; excluded from the component connectivity matrix."),
    ("notes/legend/title/cable labels/phase marks", "matrix nodes", "Annotations and references, not graph nodes."),
]


ROUND_EDGE_SETS = {
    "diego_round1": DIEGO_ROUND1_EDGES,
    "jennifer_round1": FINAL_EDGES,
    "diego_round2": FINAL_EDGES,
    "jennifer_round2_final": FINAL_EDGES,
    "final": FINAL_EDGES,
}


def validate_edges(edges: list[tuple[str, str, str, str]]) -> None:
    nodes = set(NODES)
    seen: set[tuple[str, str]] = set()
    for source, target, *_ in edges:
        if source not in nodes:
            raise ValueError(f"Unknown source node: {source}")
        if target not in nodes:
            raise ValueError(f"Unknown target node: {target}")
        if source == target:
            raise ValueError(f"Self-loop not justified: {source}")
        key = edge_key(source, target)
        if key in seen:
            raise ValueError(f"Duplicate edge: {source}--{target}")
        seen.add(key)


def adjacency(edges: list[tuple[str, str, str, str]]) -> dict[str, set[str]]:
    graph = {node: set() for node in NODES}
    for source, target, *_ in edges:
        graph[source].add(target)
        graph[target].add(source)
    return graph


def write_edge_csv(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "evidence_type", "evidence"])
        writer.writerows(edges)


def write_matrix_csv(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    graph = adjacency(edges)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component"] + NODES)
        for row_node in NODES:
            writer.writerow([row_node] + [1 if col_node in graph[row_node] else 0 for col_node in NODES])


def validate_matrix(edges: list[tuple[str, str, str, str]]) -> None:
    graph = adjacency(edges)
    for i, node in enumerate(NODES):
        if node in graph[node]:
            raise ValueError(f"Diagonal/self-loop is nonzero for {node}")
        for j, other in enumerate(NODES):
            value = 1 if other in graph[node] else 0
            reverse = 1 if node in graph[other] else 0
            if value not in (0, 1):
                raise ValueError(f"Non-binary value for {node}, {other}")
            if value != reverse:
                raise ValueError(f"Asymmetric matrix at {i},{j}: {node}, {other}")


def write_uncertain_and_rejected() -> None:
    with (RESULTS / "final_uncertain_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target_or_category", "reason"])
        writer.writerows(UNCERTAIN_EDGES)
    with (RESULTS / "final_rejected_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target_or_category", "reason"])
        writer.writerows(REJECTED_EDGES)


def image_tokens_high_detail(path: Path) -> int:
    with Image.open(path) as image:
        width, height = image.size
    scale = min(1.0, 2048.0 / max(width, height))
    width *= scale
    height *= scale
    if min(width, height) > 768:
        scale = 768.0 / min(width, height)
        width *= scale
        height *= scale
    tiles = math.ceil(width / 512.0) * math.ceil(height / 512.0)
    return 85 + 170 * tiles


def sum_image_tokens(paths: list[Path]) -> int:
    return sum(image_tokens_high_detail(path) for path in paths)


def write_round_summaries() -> None:
    text = f"""# Document 8 Round Summaries

Resource folder: `{BASE}`

Allowed visual resources used:
- `raw -- synthetic_npp_schematic_improved_local_refined_v3.png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | 120 | 125 | no | Proposed top 4.16 kV, safety buses, 480 V buses, load feeders, selected sensing/control paths, and held congested dashed bundles uncertain. |
| 1 | Jennifer precision | 120 | 127 | no | Corrected `MCC-2C` ownership, removed unsupported `PN-480-A/B` shortcuts, and promoted supported B charger/valve edges. |
| 2 | Diego high-recall | 120 | 127 | yes | Accepted Jennifer's edge ownership revision. |
| 2 | Jennifer precision final | 120 | 127 | yes | Confirmed saturated graph; dashed interlock bundles and `CB-EDG-C--BUS-4160-S2B` remain uncertain. |

## Final Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled terminals, solid feeders, bus taps, explicit tie/disconnect components, clear sensing/control links, and explicit ground references are asserted.
- Terminal block references, annotation boxes, phase labels, cable labels, crossings without filled dots, and ambiguous dashed interlock/raceway bundles are excluded and recorded as uncertain/rejected.
"""
    (RESULTS / "round_summaries.md").write_text(text, encoding="utf-8")


def write_token_usage() -> None:
    raw = BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
    overlay = BASE / "detected_components_and_logical_overlay.png"
    r = RESULTS
    main_images = [
        raw, overlay,
        r / "raw_01_top_416kv_sources.png",
        r / "raw_02_safety_416kv_buses.png",
        r / "raw_03_480_distribution.png",
        r / "raw_04_train_a_loads.png",
        r / "raw_05_train_a_dc_control.png",
        r / "raw_06_train_b_loads.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_interlocks.png",
        r / "raw_09_left_source_label_zoom_2x.png",
        r / "raw_10_center_source_label_zoom_2x.png",
        r / "raw_11_right_source_label_zoom_2x.png",
        r / "raw_12_left_load_label_zoom_2x.png",
        r / "raw_13_center_dc_label_zoom_2x.png",
        r / "raw_14_right_load_label_zoom_2x.png",
        r / "raw_16_a_pn480_mcc2c_zoom_2x.png",
        r / "raw_17_b_pn480_mcc2d_zoom_2x.png",
    ]
    diego_r1_images = [
        raw, overlay,
        r / "raw_01_top_416kv_sources.png",
        r / "raw_02_safety_416kv_buses.png",
        r / "raw_03_480_distribution.png",
        r / "raw_04_train_a_loads.png",
        r / "raw_05_train_a_dc_control.png",
        r / "raw_06_train_b_loads.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_interlocks.png",
        r / "raw_09_left_source_label_zoom_2x.png",
        r / "raw_10_center_source_label_zoom_2x.png",
        r / "raw_11_right_source_label_zoom_2x.png",
        r / "overlay_02_safety_416kv_buses.png",
        r / "overlay_04_train_a_loads.png",
        r / "overlay_06_train_b_loads.png",
    ]
    jennifer_r1_images = [
        raw, overlay,
        r / "raw_01_top_416kv_sources.png",
        r / "raw_02_safety_416kv_buses.png",
        r / "raw_03_480_distribution.png",
        r / "raw_16_a_pn480_mcc2c_zoom_2x.png",
        r / "raw_17_b_pn480_mcc2d_zoom_2x.png",
        r / "raw_12_left_load_label_zoom_2x.png",
        r / "raw_14_right_load_label_zoom_2x.png",
        r / "overlay_05_train_a_dc_control.png",
        r / "overlay_07_train_b_dc_control.png",
    ]
    diego_r2_images = [
        raw,
        r / "raw_16_a_pn480_mcc2c_zoom_2x.png",
        r / "raw_17_b_pn480_mcc2d_zoom_2x.png",
        r / "raw_02_safety_416kv_buses.png",
        r / "raw_12_left_load_label_zoom_2x.png",
        r / "raw_14_right_load_label_zoom_2x.png",
    ]
    jennifer_r2_images = [
        r / "raw_16_a_pn480_mcc2c_zoom_2x.png",
        r / "raw_17_b_pn480_mcc2d_zoom_2x.png",
        r / "raw_08_bottom_interlocks.png",
    ]

    rows = [
        ("main-orchestration-aggregate", "Main agent", "Codex session model", 24000, sum_image_tokens(main_images), 8000, "Aggregate estimate for visual inspection, crop generation, subagent orchestration, artifact writing, validation, and final reporting."),
        ("diego-round-1", "Diego", "gpt-5.5 requested; reused existing agent due thread limit", 650, sum_image_tokens(diego_r1_images), 7600, "High-recall extraction prompt plus full raw/overlay and crop package."),
        ("jennifer-round-1", "Jennifer", "gpt-5.5 requested; reused existing agent due thread limit", 7200, sum_image_tokens(jennifer_r1_images), 1200, "Precision review prompt with Diego proposal text and ownership-focused crops."),
        ("diego-round-2", "Diego", "gpt-5.5 requested; reused existing agent due thread limit", 520, sum_image_tokens(diego_r2_images), 260, "Saturation check against Jennifer revision."),
        ("jennifer-round-2-final", "Jennifer", "gpt-5.5 requested; reused existing agent due thread limit", 280, sum_image_tokens(jennifer_r2_images), 80, "Final confirmation prompt."),
    ]

    fieldnames = [
        "document", "iteration", "call_id", "agent", "model",
        "text_input_tokens_low", "text_input_tokens_expected", "text_input_tokens_high",
        "cached_input_tokens_est",
        "image_file_input_tokens_low", "image_file_input_tokens_expected", "image_file_input_tokens_high",
        "output_tokens_low", "output_tokens_expected", "output_tokens_high",
        "reasoning_tokens_est", "total_low", "total_expected", "total_high",
        "usage_object_available", "notes",
    ]
    totals = [0, 0, 0]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for call_id, agent, model, text_expected, image_expected, output_expected, notes in rows:
            text_low, text_high = round(text_expected * 0.75), round(text_expected * 1.35)
            image_low, image_high = round(image_expected * 0.80), round(image_expected * 1.30)
            output_low, output_high = round(output_expected * 0.60), round(output_expected * 1.60)
            total_low = text_low + image_low + output_low
            total_expected = text_expected + image_expected + output_expected
            total_high = text_high + image_high + output_high
            totals[0] += total_low
            totals[1] += total_expected
            totals[2] += total_high
            writer.writerow({
                "document": 8,
                "iteration": 1,
                "call_id": call_id,
                "agent": agent,
                "model": model,
                "text_input_tokens_low": text_low,
                "text_input_tokens_expected": text_expected,
                "text_input_tokens_high": text_high,
                "cached_input_tokens_est": 0,
                "image_file_input_tokens_low": image_low,
                "image_file_input_tokens_expected": image_expected,
                "image_file_input_tokens_high": image_high,
                "output_tokens_low": output_low,
                "output_tokens_expected": output_expected,
                "output_tokens_high": output_high,
                "reasoning_tokens_est": "not exposed",
                "total_low": total_low,
                "total_expected": total_expected,
                "total_high": total_high,
                "usage_object_available": "no",
                "notes": notes + " Official token counter and response usage objects unavailable because OPENAI_API_KEY was not set/exposed.",
            })

    api_key_present = bool(os.environ.get("OPENAI_API_KEY"))
    summary = f"""# Token Usage Estimate

Document: 8
Iteration: 1

Official Responses token counting endpoint used: no
Reason: no API key was available in the environment (`OPENAI_API_KEY_PRESENT={str(api_key_present).lower()}`), and the subagent tool responses did not expose usage objects.

Fallback method:
- Text tokens estimated from prompt/response size by rough token budgeting.
- Image/file input tokens estimated with a high-detail 512-pixel tile method using actual image dimensions.
- Low/high totals apply conservative multipliers to text, image, and output estimates.

| document | iteration | calls | total low | total expected | total high |
|---:|---:|---:|---:|---:|---:|
| 8 | 1 | {len(rows)} | {totals[0]} | {totals[1]} | {totals[2]} |
"""
    (RESULTS / "token_usage_summary.md").write_text(summary, encoding="utf-8")


def write_all() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    validate_edges(DIEGO_ROUND1_EDGES)
    validate_edges(FINAL_EDGES)
    for round_name, edges in ROUND_EDGE_SETS.items():
        validate_matrix(edges)
        write_edge_csv(RESULTS / f"{round_name}_edges.csv", edges)
        write_matrix_csv(RESULTS / f"{round_name}_matrix.csv", edges)
        write_matrix_csv(RESULTS / f"{round_name}_connectivity_matrix.csv", edges)
    write_edge_csv(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix_csv(RESULTS / "final_matrix.csv", FINAL_EDGES)
    write_matrix_csv(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_uncertain_and_rejected()
    write_round_summaries()
    write_token_usage()
    print(f"nodes={len(NODES)}")
    print(f"diego_round1_edges={len(DIEGO_ROUND1_EDGES)}")
    print(f"final_edges={len(FINAL_EDGES)}")
    print(f"results={RESULTS}")


if __name__ == "__main__":
    write_all()
