from __future__ import annotations

import csv
import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
CROP_DIR = RAW_DIR / "codes" / "crops"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v2.png"
RESULTS_DIR.mkdir(exist_ok=True)


def edge(edges: list[dict[str, str]], source: str, target: str, evidence: str) -> None:
    if source == target:
        raise ValueError(f"self-edge requested for {source}")
    key = tuple(sorted((source, target)))
    if any(tuple(sorted((item["source"], item["target"]))) == key for item in edges):
        return
    edges.append({"source": source, "target": target, "evidence": evidence})


FINAL_NODES = [
    "GRID-230-A",
    "CB-SW-A",
    "TR-SU-A",
    "GEN-DG-A",
    "CB-DG-A",
    "TR-EDG-A",
    "BUS-13K-A",
    "CB-13-TIE",
    "BUS-13K-B",
    "TR-SU-B",
    "CB-SW-B",
    "GRID-230-B",
    "TR-EDG-B",
    "CB-DG-B",
    "GEN-DG-B",
    "TR-4K-A",
    "CB-4K-A",
    "BUS-4K-A",
    "CB-4K-TIE",
    "BUS-4K-B",
    "CB-4K-B",
    "TR-4K-B",
    "TR-480-A",
    "CB-LC-A",
    "BUS-480-A",
    "MCC-01A",
    "PUMP-RHR-A",
    "MOTOR-CCW-A",
    "MCC-02A",
    "PUMP-AFW-A",
    "VALVE-MOV-A",
    "FAN-CONTAIN-A",
    "RECT-125A",
    "BUS-DC125-A",
    "BAT-125A",
    "INV-120A",
    "JB-ESF-A",
    "PNL-ESF-A",
    "TR-480-B",
    "CB-LC-B",
    "BUS-480-B",
    "MCC-01B",
    "PUMP-RHR-B",
    "MOTOR-CCW-B",
    "MCC-02B",
    "PUMP-AFW-B",
    "VALVE-MOV-B",
    "FAN-CONTAIN-B",
    "RECT-125B",
    "BUS-DC125-B",
    "BAT-125B",
    "INV-120B",
    "JB-ESF-B",
    "PNL-ESF-B",
    "PNL-RPS-1",
]

CONTROL_ROUTE_NODES = [
    "CONTROL-RPS-TRIP",
    "CONTROL-RPS-LOCKOUT",
    "CONTROL-RPS-ESF-TRUNK",
    "CONTROL-ESF-A",
    "CONTROL-ESF-B",
]


def add_power_dc_edges(edges: list[dict[str, str]]) -> None:
    edge(edges, "GRID-230-A", "CB-SW-A", "offsite A source to source breaker")
    edge(edges, "CB-SW-A", "TR-SU-A", "offsite A source breaker to startup transformer")
    edge(edges, "TR-SU-A", "BUS-13K-A", "startup transformer A tap to 13.8 kV bus A")
    edge(edges, "GEN-DG-A", "CB-DG-A", "diesel generator A to breaker")
    edge(edges, "CB-DG-A", "TR-EDG-A", "DG A breaker to emergency transformer")
    edge(edges, "TR-EDG-A", "BUS-13K-A", "emergency transformer A tap to 13.8 kV bus A")
    edge(edges, "BUS-13K-A", "CB-13-TIE", "13.8 kV bus tie left side")
    edge(edges, "CB-13-TIE", "BUS-13K-B", "13.8 kV bus tie right side")
    edge(edges, "BUS-13K-B", "TR-SU-B", "13.8 kV bus B to startup transformer B")
    edge(edges, "TR-SU-B", "CB-SW-B", "startup transformer B to source breaker")
    edge(edges, "CB-SW-B", "GRID-230-B", "source breaker to offsite B source")
    edge(edges, "BUS-13K-B", "TR-EDG-B", "13.8 kV bus B to emergency transformer B")
    edge(edges, "TR-EDG-B", "CB-DG-B", "emergency transformer B to DG breaker")
    edge(edges, "CB-DG-B", "GEN-DG-B", "DG B breaker to diesel generator B")

    edge(edges, "BUS-13K-A", "TR-4K-A", "13.8 kV bus A to 4.16 kV transformer A")
    edge(edges, "TR-4K-A", "CB-4K-A", "4.16 kV transformer A to incomer breaker")
    edge(edges, "CB-4K-A", "BUS-4K-A", "incomer breaker to bus 4K-A")
    edge(edges, "BUS-4K-A", "CB-4K-TIE", "4.16 kV tie left side")
    edge(edges, "CB-4K-TIE", "BUS-4K-B", "4.16 kV tie right side")
    edge(edges, "BUS-13K-B", "TR-4K-B", "13.8 kV bus B to 4.16 kV transformer B")
    edge(edges, "TR-4K-B", "CB-4K-B", "4.16 kV transformer B to incomer breaker")
    edge(edges, "CB-4K-B", "BUS-4K-B", "incomer breaker to bus 4K-B")

    edge(edges, "BUS-4K-A", "TR-480-A", "4.16 kV bus A to 480 V transformer A")
    edge(edges, "TR-480-A", "CB-LC-A", "480 V transformer A to load-center breaker")
    edge(edges, "CB-LC-A", "BUS-480-A", "load-center breaker A to 480 V bus A")
    edge(edges, "BUS-480-A", "MCC-01A", "480 V bus A tap to MCC-01A")
    edge(edges, "MCC-01A", "PUMP-RHR-A", "MCC-01A feeder to RHR pump A")
    edge(edges, "MCC-01A", "MOTOR-CCW-A", "MCC-01A feeder to CCW motor A")
    edge(edges, "BUS-480-A", "MCC-02A", "480 V bus A tap to MCC-02A")
    edge(edges, "MCC-02A", "PUMP-AFW-A", "MCC-02A feeder to AFW pump A")
    edge(edges, "MCC-02A", "VALVE-MOV-A", "MCC-02A feeder to MOV valve A")
    edge(edges, "MCC-02A", "FAN-CONTAIN-A", "MCC-02A feeder to containment fan A")
    edge(edges, "BUS-480-A", "RECT-125A", "480 V bus A feed to 125 VDC rectifier A")
    edge(edges, "RECT-125A", "BUS-DC125-A", "rectifier A output to 125 VDC bus A")
    edge(edges, "BUS-DC125-A", "BAT-125A", "battery A tap on 125 VDC bus A")
    edge(edges, "BUS-DC125-A", "INV-120A", "inverter A tap on 125 VDC bus A")
    edge(edges, "INV-120A", "PNL-ESF-A", "inverter A solid output to ESF panel A")

    edge(edges, "BUS-4K-B", "TR-480-B", "4.16 kV bus B to 480 V transformer B")
    edge(edges, "TR-480-B", "CB-LC-B", "480 V transformer B to load-center breaker")
    edge(edges, "CB-LC-B", "BUS-480-B", "load-center breaker B to 480 V bus B")
    edge(edges, "BUS-480-B", "MCC-01B", "480 V bus B tap to MCC-01B")
    edge(edges, "MCC-01B", "PUMP-RHR-B", "MCC-01B feeder to RHR pump B")
    edge(edges, "MCC-01B", "MOTOR-CCW-B", "MCC-01B feeder to CCW motor B")
    edge(edges, "BUS-480-B", "MCC-02B", "480 V bus B tap to MCC-02B")
    edge(edges, "MCC-02B", "PUMP-AFW-B", "MCC-02B feeder to AFW pump B")
    edge(edges, "MCC-02B", "VALVE-MOV-B", "MCC-02B feeder to MOV valve B")
    edge(edges, "MCC-02B", "FAN-CONTAIN-B", "MCC-02B feeder to containment fan B")
    edge(edges, "BUS-480-B", "RECT-125B", "480 V bus B feed to 125 VDC rectifier B")
    edge(edges, "RECT-125B", "BUS-DC125-B", "rectifier B output to 125 VDC bus B")
    edge(edges, "BUS-DC125-B", "BAT-125B", "battery B tap on 125 VDC bus B")
    edge(edges, "BUS-DC125-B", "INV-120B", "inverter B tap on 125 VDC bus B")
    edge(edges, "INV-120B", "PNL-ESF-B", "inverter B solid output to ESF panel B")


def final_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    add_power_dc_edges(edges)
    edge(edges, "CB-13-TIE", "PNL-RPS-1", "dashed RPS trip/control line lands on CB-13-TIE and PNL-RPS-1")
    edge(edges, "CB-4K-TIE", "PNL-RPS-1", "dashed RPS lockout/control line lands on CB-4K-TIE and PNL-RPS-1")
    edge(edges, "JB-ESF-A", "PNL-ESF-A", "dashed vertical control drop between JB-ESF-A and PNL-ESF-A")
    edge(edges, "JB-ESF-B", "PNL-ESF-B", "dashed vertical control drop between JB-ESF-B and PNL-ESF-B")
    edge(edges, "PNL-ESF-A", "PUMP-AFW-A", "dashed ESF control line lands on PNL-ESF-A and AFW pump A")
    edge(edges, "PNL-ESF-A", "VALVE-MOV-A", "dashed ESF control line lands on PNL-ESF-A and MOV valve A")
    edge(edges, "PNL-ESF-B", "PUMP-AFW-B", "dashed ESF control line lands on PNL-ESF-B and AFW pump B")
    edge(edges, "PNL-ESF-B", "VALVE-MOV-B", "dashed ESF control line lands on PNL-ESF-B and MOV valve B")
    return edges


def diego_round1_nodes() -> list[str]:
    return FINAL_NODES + CONTROL_ROUTE_NODES


def diego_round1_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    add_power_dc_edges(edges)
    edge(edges, "JB-ESF-A", "PNL-ESF-A", "Diego accepted dashed JB/panel control drop A")
    edge(edges, "JB-ESF-B", "PNL-ESF-B", "Diego accepted dashed JB/panel control drop B")
    edge(edges, "CB-13-TIE", "CONTROL-RPS-TRIP", "Diego high-recall RPS trip route abstraction")
    edge(edges, "CONTROL-RPS-TRIP", "PNL-RPS-1", "Diego high-recall RPS trip route abstraction")
    edge(edges, "CB-4K-TIE", "CONTROL-RPS-LOCKOUT", "Diego high-recall RPS lockout route abstraction")
    edge(edges, "CONTROL-RPS-LOCKOUT", "PNL-RPS-1", "Diego high-recall RPS lockout route abstraction")
    edge(edges, "PNL-RPS-1", "CONTROL-RPS-ESF-TRUNK", "Diego high-recall central RPS trunk")
    edge(edges, "PNL-ESF-A", "CONTROL-ESF-A", "Diego high-recall ESF A control route abstraction")
    edge(edges, "CONTROL-ESF-A", "PUMP-AFW-A", "Diego high-recall ESF A control route to AFW pump")
    edge(edges, "CONTROL-ESF-A", "VALVE-MOV-A", "Diego high-recall ESF A control route to MOV")
    edge(edges, "PNL-ESF-B", "CONTROL-ESF-B", "Diego high-recall ESF B control route abstraction")
    edge(edges, "CONTROL-ESF-B", "PUMP-AFW-B", "Diego high-recall ESF B control route to AFW pump")
    edge(edges, "CONTROL-ESF-B", "VALVE-MOV-B", "Diego high-recall ESF B control route to MOV")
    edge(edges, "CONTROL-RPS-ESF-TRUNK", "CONTROL-ESF-A", "Diego ambiguous central trunk to ESF A route")
    edge(edges, "CONTROL-RPS-ESF-TRUNK", "CONTROL-ESF-B", "Diego ambiguous central trunk to ESF B route")
    edge(edges, "CONTROL-ESF-A", "FAN-CONTAIN-A", "Diego ambiguous ESF A fan-control candidate")
    edge(edges, "CONTROL-ESF-B", "FAN-CONTAIN-B", "Diego ambiguous ESF B fan-control candidate")
    edge(edges, "CONTROL-ESF-A", "INV-120A", "Diego ambiguous ESF A inverter-control candidate")
    edge(edges, "CONTROL-ESF-B", "INV-120B", "Diego ambiguous ESF B inverter-control candidate")
    edge(edges, "CONTROL-ESF-A", "BUS-DC125-A", "Diego ambiguous ESF A DC-bus-control candidate")
    edge(edges, "CONTROL-ESF-B", "BUS-DC125-B", "Diego ambiguous ESF B DC-bus-control candidate")
    edge(edges, "CONTROL-RPS-TRIP", "CB-4K-TIE", "Diego ambiguous RPS trip to 4K tie candidate")
    return edges


def validate(nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    node_set = set(nodes)
    referenced = {item["source"] for item in edges} | {item["target"] for item in edges}
    missing = sorted(referenced - node_set)
    if missing:
        raise ValueError(f"edges reference missing nodes: {missing}")
    pairs = [tuple(sorted((item["source"], item["target"]))) for item in edges]
    if len(pairs) != len(set(pairs)):
        raise ValueError("duplicate undirected edges")
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        i = index[item["source"]]
        j = index[item["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "zero_diagonal": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "unique_nodes": len(nodes) == len(node_set),
    }


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        i = index[item["source"]]
        j = index[item["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node"])
        for node in nodes:
            writer.writerow([node])


def image_expected_tokens(path: Path) -> int:
    # Heuristic only. Exact counts require POST /v1/responses/input_tokens.
    with Image.open(path) as image:
        width, height = image.size
    scale = min(1.0, 2048 / max(width, height))
    width = max(1, int(width * scale))
    height = max(1, int(height * scale))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def text_expected_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def estimate_row(
    document: str,
    iteration: str,
    call_id: str,
    agent: str,
    role: str,
    payload_text: str,
    images: Iterable[Path],
    expected_output_tokens: int,
    expected_reasoning_tokens: int,
    decision: str,
) -> dict[str, object]:
    text_tokens = text_expected_tokens(payload_text)
    image_tokens = sum(image_expected_tokens(path) for path in images)
    expected_input = text_tokens + image_tokens
    low_input = math.ceil(expected_input * 0.75)
    high_input = math.ceil(expected_input * 1.45)
    low_output = math.ceil(expected_output_tokens * 0.65)
    high_output = math.ceil(expected_output_tokens * 1.6)
    low_reasoning = math.ceil(expected_reasoning_tokens * 0.5)
    high_reasoning = math.ceil(expected_reasoning_tokens * 2.0)
    return {
        "document": document,
        "iteration": iteration,
        "call_id": call_id,
        "agent": agent,
        "role": role,
        "actual_usage_available": "no",
        "actual_input_tokens": "",
        "actual_cached_input_tokens": "",
        "actual_output_tokens": "",
        "actual_reasoning_tokens": "",
        "actual_image_file_input_tokens": "",
        "estimated_text_input_tokens": text_tokens,
        "estimated_image_file_input_tokens_low": math.ceil(image_tokens * 0.65),
        "estimated_image_file_input_tokens_expected": image_tokens,
        "estimated_image_file_input_tokens_high": math.ceil(image_tokens * 1.8),
        "estimated_input_tokens_low": low_input,
        "estimated_input_tokens_expected": expected_input,
        "estimated_input_tokens_high": high_input,
        "estimated_cached_input_tokens_low": 0,
        "estimated_cached_input_tokens_expected": 0,
        "estimated_cached_input_tokens_high": 0,
        "estimated_output_tokens_low": low_output,
        "estimated_output_tokens_expected": expected_output_tokens,
        "estimated_output_tokens_high": high_output,
        "estimated_reasoning_tokens_low": low_reasoning,
        "estimated_reasoning_tokens_expected": expected_reasoning_tokens,
        "estimated_reasoning_tokens_high": high_reasoning,
        "estimated_total_tokens_low": low_input + low_output + low_reasoning,
        "estimated_total_tokens_expected": expected_input + expected_output_tokens + expected_reasoning_tokens,
        "estimated_total_tokens_high": high_input + high_output + high_reasoning,
        "endpoint_count_status": "skipped_no_OPENAI_API_KEY",
        "decision": decision,
    }


def write_token_audit(round_validations: dict[str, dict[str, object]]) -> None:
    common_images = [
        RAW_IMAGE,
        CROP_DIR / "top_sources.png",
        CROP_DIR / "mid_4160.png",
        CROP_DIR / "train_a_loads.png",
        CROP_DIR / "train_b_loads.png",
        CROP_DIR / "dc_control_center.png",
        CROP_DIR / "title_notes_legend.png",
    ]
    rows = [
        estimate_row(
            "case_36",
            "iteration_01",
            "main_aggregate",
            "Codex",
            "orchestrator/extractor/output-writer",
            "Main agent inspected raw/crops, coordinated subagents, generated code, validation, token audit, and final answer.",
            [RAW_IMAGE, CROP_DIR / "full_sheet.png", CROP_DIR / "lower_loads_overview.png"],
            expected_output_tokens=3200,
            expected_reasoning_tokens=4500,
            decision="aggregate estimate; per-turn usage object not exposed by Codex runtime",
        ),
        estimate_row(
            "case_36",
            "iteration_01",
            "round_01_diego_high_recall",
            "Diego",
            "high-recall extractor",
            "High-recall extraction prompt with full raw schematic and focused crops.",
            common_images,
            expected_output_tokens=2600,
            expected_reasoning_tokens=3200,
            decision=f"{round_validations['round_01_diego_high_recall']['node_count']} nodes / {round_validations['round_01_diego_high_recall']['edge_count']} edges",
        ),
        estimate_row(
            "case_36",
            "iteration_01",
            "round_02_jennifer_precision",
            "Jennifer",
            "precision reviewer/refiner",
            "Precision review prompt with Diego proposal and full raw/focused crops.",
            common_images,
            expected_output_tokens=1700,
            expected_reasoning_tokens=2600,
            decision=f"{round_validations['round_02_jennifer_precision']['node_count']} nodes / {round_validations['round_02_jennifer_precision']['edge_count']} edges",
        ),
        estimate_row(
            "case_36",
            "iteration_01",
            "round_03_diego_saturation",
            "Diego",
            "saturation extractor",
            "Saturation prompt with Jennifer precision corrections; no images reattached.",
            [],
            expected_output_tokens=450,
            expected_reasoning_tokens=900,
            decision="AGREED with Jennifer precision graph",
        ),
        estimate_row(
            "case_36",
            "iteration_01",
            "round_04_jennifer_agreement",
            "Jennifer",
            "final precision confirmation",
            "Final agreement prompt with saturated graph summary; no images reattached.",
            [],
            expected_output_tokens=80,
            expected_reasoning_tokens=250,
            decision="AGREED final saturated matrix",
        ),
    ]

    fieldnames = list(rows[0].keys())
    with (RESULTS_DIR / "token_usage_estimates_by_call.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "document": "case_36",
        "iteration": "iteration_01",
        "actual_usage_available": "no",
        "actual_usage_reason": "Codex tool and subagent responses in this environment do not expose OpenAI response usage objects; OPENAI_API_KEY is unset, so /v1/responses/input_tokens could not be called.",
        "total_estimated_tokens_low": sum(int(row["estimated_total_tokens_low"]) for row in rows),
        "total_estimated_tokens_expected": sum(int(row["estimated_total_tokens_expected"]) for row in rows),
        "total_estimated_tokens_high": sum(int(row["estimated_total_tokens_high"]) for row in rows),
        "total_estimated_image_file_input_tokens_expected": sum(int(row["estimated_image_file_input_tokens_expected"]) for row in rows),
    }
    with (RESULTS_DIR / "token_usage_summary_by_document.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    manifest = {
        "endpoint": "POST /v1/responses/input_tokens",
        "status": "not_called",
        "reason": "OPENAI_API_KEY is not set in this environment.",
        "openai_docs": "https://platform.openai.com/docs/guides/token-counting",
        "payload_shape": {
            "model": "gpt-5.4",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "<prompt text>"},
                        {"type": "input_image", "image_url": "data:image/png;base64,<image bytes>"},
                    ],
                }
            ],
        },
        "planned_calls": [
            {
                "call_id": row["call_id"],
                "agent": row["agent"],
                "role": row["role"],
                "image_paths": [str(path) for path in (common_images if row["call_id"] in {"round_01_diego_high_recall", "round_02_jennifer_precision"} else [])],
            }
            for row in rows
        ],
    }
    (RESULTS_DIR / "responses_input_token_count_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Compatibility with the user's existing tracking file name, including typo.
    tracking_rows = [
        [
            "stage",
            "agent",
            "role",
            "artifact",
            "node_count",
            "edge_count",
            "token_accounting",
            "decision",
        ],
        [
            "prep",
            "Codex",
            "orchestrator",
            "codes/make_crops.py and codes/crops",
            "",
            "",
            "usage object not exposed; see token_usage_estimates_by_call.csv",
            "raw-derived crops generated for visual inspection",
        ],
        [
            "round_01",
            "Diego",
            "high-recall extractor",
            "round_01_diego_high_recall_matrix.csv",
            round_validations["round_01_diego_high_recall"]["node_count"],
            round_validations["round_01_diego_high_recall"]["edge_count"],
            "actual usage unavailable; low/expected/high estimates recorded",
            "included route-node and uncertain dashed-control candidates",
        ],
        [
            "round_02",
            "Jennifer",
            "precision reviewer/refiner",
            "round_02_jennifer_precision_matrix.csv",
            round_validations["round_02_jennifer_precision"]["node_count"],
            round_validations["round_02_jennifer_precision"]["edge_count"],
            "actual usage unavailable; low/expected/high estimates recorded",
            "removed invented CONTROL-* nodes and unsupported dashed extras",
        ],
        [
            "round_03",
            "Diego",
            "saturation extractor",
            "round_03_diego_saturation_matrix.csv",
            round_validations["round_03_diego_saturation"]["node_count"],
            round_validations["round_03_diego_saturation"]["edge_count"],
            "actual usage unavailable; low/expected/high estimates recorded",
            "AGREED with Jennifer precision graph",
        ],
        [
            "round_04",
            "Jennifer",
            "final precision confirmation",
            "round_04_jennifer_agreement_matrix.csv",
            round_validations["round_04_jennifer_agreement"]["node_count"],
            round_validations["round_04_jennifer_agreement"]["edge_count"],
            "actual usage unavailable; low/expected/high estimates recorded",
            "AGREED final saturated matrix",
        ],
        [
            "final",
            "Codex",
            "orchestrator",
            "final_connectivity_matrix.csv",
            round_validations["final"]["node_count"],
            round_validations["final"]["edge_count"],
            "see token_usage_summary_by_document.csv",
            "validated symmetric zero-diagonal component matrix",
        ],
    ]
    for name in ["token_performance_tracking.csv", "token_performance_traking.csv"]:
        with (RESULTS_DIR / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerows(tracking_rows)


def write_note(rounds: dict[str, tuple[list[str], list[dict[str, str]]]], validations: dict[str, dict[str, object]]) -> None:
    rows = "\n".join(f"| `{name}` | {len(nodes)} | {len(edges)} |" for name, (nodes, edges) in rounds.items())
    note = f"""# Case 36 Connectivity Extraction Note

Generated: {datetime.now().replace(microsecond=0).isoformat()}

## Scope

- Raw resource: `raw -- synthetic_npp_electrical_schematic_v2.png`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Sibling derived-resource folders and any ground-truth material were not opened or used.

## Subagent Rounds

1. Diego high-recall pass: proposed the labeled equipment set plus route-node abstractions for dashed/control circuits and uncertain extras.
2. Jennifer precision pass: removed invented `CONTROL-*` route nodes, kept only labeled equipment/bus nodes, and converted visually supported control routes to direct edges between labeled endpoints.
3. Diego saturation pass: AGREED with Jennifer's precision graph.
4. Jennifer final confirmation: AGREED.

## Final Decisions

- Final rows are labeled equipment and logical buses only.
- Route labels, aliases, titles, legends, notes, enclosure text, bus tick marks, `TIE OPEN`, `EXC`, `RPS TRIP`, `RPS LOCKOUT`, `SU-A/B`, `EDG-A/B`, and `LC-*` tap aliases are excluded as nodes.
- Direct drawn adjacencies are encoded, not transitive closure across an entire bus.
- Control/dashed connections are retained only where the line visibly lands on labeled component endpoints.
- The RPS-to-ESF trunk candidate, fan dashed-control candidates, inverter/DC-bus dashed candidates, and direct `RECT/BAT/INV` edges not mediated by `BUS-DC125-*` are excluded.

## Counts

- Final nodes: {validations["final"]["node_count"]}
- Final undirected component edges: {validations["final"]["edge_count"]}
- Matrix is symmetric with zero diagonal: {validations["final"]["symmetric"] and validations["final"]["zero_diagonal"]}

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
{rows}

## Token Accounting

- Actual model usage objects were not exposed by the Codex/subagent tool responses.
- `OPENAI_API_KEY` is unset, so the Responses input-token counting endpoint was not called.
- Low/expected/high estimates and endpoint-ready manifest are saved in:
  - `token_usage_estimates_by_call.csv`
  - `token_usage_summary_by_document.csv`
  - `responses_input_token_count_manifest.json`

## Output Files

- `connectivity_matrix.csv`
- `final_connectivity_matrix.csv`
- `final_nodes.csv`
- `final_edges.csv`
- `connectivity_graph.json`
- `validation_summary.json`
- `round_01_diego_high_recall_matrix.csv`
- `round_02_jennifer_precision_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_agreement_matrix.csv`
- `token_performance_tracking.csv`
- `token_performance_traking.csv`
"""
    (RESULTS_DIR / "extraction_note.md").write_text(note, encoding="utf-8")


def main() -> None:
    final_edge_list = final_edges()
    rounds = {
        "round_01_diego_high_recall": (diego_round1_nodes(), diego_round1_edges()),
        "round_02_jennifer_precision": (FINAL_NODES, final_edge_list),
        "round_03_diego_saturation": (FINAL_NODES, final_edge_list),
        "round_04_jennifer_agreement": (FINAL_NODES, final_edge_list),
    }
    validations = {name: validate(nodes, edges) for name, (nodes, edges) in rounds.items()}
    validations["final"] = validate(FINAL_NODES, final_edge_list)

    for name, (nodes, edges) in rounds.items():
        write_matrix(RESULTS_DIR / f"{name}_matrix.csv", nodes, edges)
        write_edges(RESULTS_DIR / f"{name}_edges.csv", edges)

    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", FINAL_NODES, final_edge_list)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, final_edge_list)
    write_edges(RESULTS_DIR / "final_edges.csv", final_edge_list)
    write_nodes(RESULTS_DIR / "final_nodes.csv", FINAL_NODES)

    graph = {
        "case": 36,
        "raw_resource": str(RAW_IMAGE),
        "nodes": FINAL_NODES,
        "edges": final_edge_list,
        "validation": validations["final"],
        "rounds": validations,
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(validations, indent=2), encoding="utf-8")
    write_token_audit(validations)
    write_note(rounds, validations)
    print(json.dumps(validations, indent=2))


if __name__ == "__main__":
    main()
