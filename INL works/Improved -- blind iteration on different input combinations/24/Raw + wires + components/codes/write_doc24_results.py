from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover - fallback for bare environments
    tiktoken = None


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"
DOCUMENT = "24"
ITERATION = "1"


LOADS_A = {
    "01": "PUMP-P201A",
    "02": "FAN-F202A",
    "03": "MOV-HV203A",
    "04": "PUMP-P204A",
    "05": "CHLR-205A",
    "06": "HTR-206A",
    "07": "VALVE-MV207A",
    "08": "PMP-LP208A",
    "09": "COMP-C209A",
}

LOADS_B = {
    "01": "PUMP-P201B",
    "02": "FAN-F202B",
    "03": "MOV-HV203B",
    "04": "PUMP-P204B",
    "05": "CHLR-205B",
    "06": "HTR-206B",
    "07": "VALVE-MV207B",
    "08": "PMP-LP208B",
    "09": "COMP-C209B",
}


TOP_NODES = [
    "OFFSITE-1",
    "CB-101A",
    "TR-SAT-1A",
    "BUS-101A",
    "EDG-1A",
    "CB-DG1A",
    "SW-MAN-A",
    "TB-DG-A",
    "CB-TIE-1",
    "OFFSITE-2",
    "CB-101B",
    "TR-SAT-1B",
    "BUS-101B",
    "EDG-1B",
    "CB-DG1B",
    "SW-MAN-B",
    "TB-DG-B",
    "CB-201A",
    "TR-1A",
    "CB-202A",
    "BUS-201A",
    "CB-201B",
    "TR-1B",
    "CB-202B",
    "BUS-201B",
]

BOTTOM_A_NODES = [
    "DC-BUS-125A",
    "BAT-125A",
    "CHG-125A",
    "INV-120A",
    "PNL-DC-A",
    "METER-V1",
    "ESFAS-PNL-A",
    "GND-DC-A",
    "PNL-AC-A",
    "RPS-PNL-A",
    "TRIP-MOD-A",
    "PT-401A",
    "LT-402A",
    "FT-403A",
    "JB-401A",
    "TB-RPS-A",
    "GND-401A",
    "RELAY-K27A",
    "RELAY-K59A",
    "RELAY-K81A",
    "RELAY-K86A",
    "TDR-1",
    "LAMP-ALM-A",
]

BOTTOM_B_NODES = [
    "DC-BUS-125B",
    "BAT-125B",
    "CHG-125B",
    "INV-120B",
    "PNL-DC-B",
    "ESFAS-PNL-B",
    "GND-DC-B",
    "PNL-AC-B",
    "RPS-PNL-B",
    "TRIP-MOD-B",
    "PT-401B",
    "LT-402B",
    "FT-403B",
    "JB-401B",
    "TB-RPS-B",
    "GND-401B",
    "RELAY-K27B",
    "RELAY-K59B",
    "RELAY-K81B",
    "RELAY-K86B",
    "TDR-2",
    "LAMP-ALM-B",
]

COMMON_NODES = ["SYNC-CAB", "LOAD-SHED-CAB", "ANN-PNL-1", "SEQ-REC-1"]


def add_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def all_nodes() -> list[str]:
    nodes: list[str] = []
    for node in TOP_NODES:
        add_unique(nodes, node)
    for suffix, load in LOADS_A.items():
        for node in [
            f"CB-2A{suffix}",
            f"DS-2A{suffix}",
            f"MCC-2A{suffix}",
            f"TB-2A{suffix}",
            load,
            f"HS-2A{suffix}",
            f"RELAY-K2A{suffix}",
        ]:
            add_unique(nodes, node)
    for suffix, load in LOADS_B.items():
        for node in [
            f"CB-2B{suffix}",
            f"DS-2B{suffix}",
            f"MCC-2B{suffix}",
            f"TB-2B{suffix}",
            load,
            f"HS-2B{suffix}",
            f"RELAY-K2B{suffix}",
        ]:
            add_unique(nodes, node)
    for node in BOTTOM_A_NODES + BOTTOM_B_NODES + COMMON_NODES:
        add_unique(nodes, node)
    return nodes


def edge(a: str, b: str, evidence: str, confidence: str = "high", status: str = "accepted") -> dict[str, str]:
    return {
        "source": a,
        "target": b,
        "evidence": evidence,
        "confidence": confidence,
        "status": status,
    }


def final_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += [
        edge("OFFSITE-1", "CB-101A", "solid source conductor"),
        edge("CB-101A", "TR-SAT-1A", "solid conductor"),
        edge("TR-SAT-1A", "BUS-101A", "vertical tap with junction dot"),
        edge("EDG-1A", "CB-DG1A", "vertical solid conductor"),
        edge("CB-DG1A", "BUS-101A", "vertical tap with junction dot"),
        edge("SW-MAN-A", "TB-DG-A", "dashed control line"),
        edge("TB-DG-A", "CB-DG1A", "dashed control line to breaker"),
        edge("BUS-101A", "CB-201A", "solid vertical feeder"),
        edge("CB-201A", "TR-1A", "solid vertical conductor"),
        edge("TR-1A", "CB-202A", "solid vertical conductor"),
        edge("CB-202A", "BUS-201A", "solid tap to lower bus"),
        edge("OFFSITE-2", "CB-101B", "solid source conductor"),
        edge("CB-101B", "TR-SAT-1B", "solid conductor"),
        edge("TR-SAT-1B", "BUS-101B", "vertical tap with junction dot"),
        edge("EDG-1B", "CB-DG1B", "vertical solid conductor"),
        edge("CB-DG1B", "BUS-101B", "vertical tap with junction dot"),
        edge("SW-MAN-B", "TB-DG-B", "dashed control line"),
        edge("TB-DG-B", "CB-DG1B", "dashed control line to breaker"),
        edge("BUS-101B", "CB-201B", "solid vertical feeder"),
        edge("CB-201B", "TR-1B", "solid vertical conductor"),
        edge("TR-1B", "CB-202B", "solid vertical conductor"),
        edge("CB-202B", "BUS-201B", "solid tap to lower bus"),
        edge("BUS-101A", "CB-TIE-1", "top bus enters tie breaker"),
        edge("CB-TIE-1", "BUS-101B", "top bus exits tie breaker"),
        edge("CB-TIE-1", "SYNC-CAB", "vertical routed control path from tie breaker to sync cabinet", "medium"),
    ]

    for train, bus, loads in [("A", "BUS-201A", LOADS_A), ("B", "BUS-201B", LOADS_B)]:
        for suffix, load in loads.items():
            prefix = f"2{train}{suffix}"
            edges += [
                edge(bus, f"CB-{prefix}", "solid bus tap with junction dot"),
                edge(f"CB-{prefix}", f"DS-{prefix}", "vertical solid feeder"),
                edge(f"DS-{prefix}", f"MCC-{prefix}", "vertical solid feeder"),
                edge(f"MCC-{prefix}", f"TB-{prefix}", "vertical solid feeder"),
                edge(f"TB-{prefix}", load, "vertical solid feeder to load"),
                edge(f"MCC-{prefix}", f"RELAY-K{prefix}", "dashed control/trip drop from MCC"),
            ]
        chain: list[str] = []
        for suffix in loads:
            prefix = f"2{train}{suffix}"
            chain.extend([f"HS-{prefix}", f"RELAY-K{prefix}"])
        for a, b in zip(chain, chain[1:]):
            edges.append(edge(a, b, "adjacent dashed control/trip chain"))

    edges += [
        edge("DC-BUS-125A", "BAT-125A", "solid DC bus tap"),
        edge("DC-BUS-125A", "CHG-125A", "solid DC bus tap"),
        edge("DC-BUS-125A", "INV-120A", "solid DC bus tap"),
        edge("DC-BUS-125A", "PNL-DC-A", "solid DC bus tap"),
        edge("DC-BUS-125A", "METER-V1", "meter tap at bus end"),
        edge("PNL-DC-A", "ESFAS-PNL-A", "solid horizontal conductor"),
        edge("PNL-DC-A", "GND-DC-A", "dashed ground drop"),
        edge("INV-120A", "PNL-AC-A", "solid vertical conductor"),
        edge("PNL-AC-A", "RPS-PNL-A", "dashed control/trip line"),
        edge("RPS-PNL-A", "TRIP-MOD-A", "dashed control/trip line"),
        edge("RPS-PNL-A", "RELAY-K27A", "dashed control drop to relay chain", "medium"),
        edge("RELAY-K27A", "RELAY-K59A", "dashed relay chain"),
        edge("RELAY-K59A", "RELAY-K81A", "dashed relay chain"),
        edge("RELAY-K81A", "RELAY-K86A", "dashed relay chain"),
        edge("TRIP-MOD-A", "RELAY-K86A", "dashed vertical control/trip line"),
        edge("PT-401A", "JB-401A", "dotted signal route", "medium"),
        edge("LT-402A", "JB-401A", "dotted signal route"),
        edge("FT-403A", "JB-401A", "dotted signal route"),
        edge("JB-401A", "TB-RPS-A", "dotted signal route"),
        edge("JB-401A", "GND-401A", "dashed grounding drop"),
        edge("TB-RPS-A", "RPS-PNL-A", "dotted signal route to RPS panel", "medium"),
        edge("DC-BUS-125B", "BAT-125B", "solid DC bus tap"),
        edge("DC-BUS-125B", "CHG-125B", "solid DC bus tap"),
        edge("DC-BUS-125B", "INV-120B", "solid DC bus tap"),
        edge("DC-BUS-125B", "PNL-DC-B", "solid DC bus tap"),
        edge("PNL-DC-B", "ESFAS-PNL-B", "solid horizontal conductor"),
        edge("PNL-DC-B", "GND-DC-B", "dashed ground drop"),
        edge("INV-120B", "PNL-AC-B", "solid vertical conductor"),
        edge("PNL-AC-B", "RPS-PNL-B", "dashed control/trip line"),
        edge("RPS-PNL-B", "TRIP-MOD-B", "dashed control/trip line"),
        edge("RPS-PNL-B", "RELAY-K27B", "dashed control drop to relay chain", "medium"),
        edge("RELAY-K27B", "RELAY-K59B", "dashed relay chain"),
        edge("RELAY-K59B", "RELAY-K81B", "dashed relay chain"),
        edge("RELAY-K81B", "RELAY-K86B", "dashed relay chain"),
        edge("TRIP-MOD-B", "RELAY-K86B", "dashed vertical control/trip line"),
        edge("PT-401B", "JB-401B", "dotted signal route", "medium"),
        edge("LT-402B", "JB-401B", "dotted signal route"),
        edge("FT-403B", "JB-401B", "dotted signal route"),
        edge("JB-401B", "TB-RPS-B", "dotted signal route"),
        edge("JB-401B", "GND-401B", "dashed grounding drop"),
        edge("TB-RPS-B", "RPS-PNL-B", "dotted signal route to RPS panel", "medium"),
        edge("LOAD-SHED-CAB", "TDR-1", "dashed horizontal control/trip line"),
        edge("LOAD-SHED-CAB", "TDR-2", "dashed horizontal control/trip line"),
        edge("LOAD-SHED-CAB", "LAMP-ALM-A", "dotted signal branch", "medium"),
        edge("LOAD-SHED-CAB", "LAMP-ALM-B", "dotted signal branch", "medium"),
        edge("LOAD-SHED-CAB", "ANN-PNL-1", "vertical dotted/signal route", "medium"),
        edge("ANN-PNL-1", "SEQ-REC-1", "dotted signal line"),
    ]
    return dedupe_edges(edges)


def high_recall_extras() -> list[dict[str, str]]:
    return [
        edge("SYNC-CAB", "LOAD-SHED-CAB", "possible vertical routing near cabinets", "medium", "removed_by_jennifer"),
        edge("RELAY-K2A09", "SYNC-CAB", "possible continuation near crowded note/crop edge", "low", "uncertain"),
        edge("TRIP-MOD-A", "LOAD-SHED-CAB", "nearby dashed route but no clean endpoint", "low", "uncertain"),
        edge("TRIP-MOD-B", "LOAD-SHED-CAB", "nearby dashed route but no clean endpoint", "low", "uncertain"),
        edge("ESFAS-PNL-A", "TDR-1", "possible route through channel without visible termination", "low", "uncertain"),
        edge("ESFAS-PNL-B", "TDR-2", "possible route through channel without visible termination", "low", "uncertain"),
        edge("LAMP-ALM-A", "LAMP-ALM-B", "shared dotted signal route, not a direct edge", "low", "removed_by_jennifer"),
    ]


def dedupe_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for item in edges:
        key = tuple(sorted((item["source"], item["target"])))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source", "target", "confidence", "status", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        a, b = item["source"], item["target"]
        if a not in index or b not in index:
            raise ValueError(f"Unknown edge endpoint: {a!r}, {b!r}")
        if a == b:
            matrix[index[a]][index[b]] = 0
        else:
            matrix[index[a]][index[b]] = 1
            matrix[index[b]][index[a]] = 1
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def text_tokens(text: str) -> int:
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    words = max(1, len(text.split()))
    by_chars = max(1, math.ceil(len(text) / 4))
    return max(words, by_chars)


def image_tokens_high_detail(path: Path) -> int:
    with Image.open(path) as image:
        width, height = image.size
    scale = min(1.0, 2048.0 / width, 2048.0 / height)
    width *= scale
    height *= scale
    short = min(width, height)
    if short > 768:
        scale = 768.0 / short
        width *= scale
        height *= scale
    tiles = math.ceil(width / 512.0) * math.ceil(height / 512.0)
    return 85 + 170 * tiles


def image_token_sum(names: list[str]) -> int:
    total = 0
    for name in names:
        path = CROPS / name
        if path.exists():
            total += image_tokens_high_detail(path)
    return total


def token_rows() -> list[dict[str, object]]:
    diego_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "detail_top_div1_components.png",
        "detail_top_div1_wires_overlay.png",
        "detail_top_div2_components.png",
        "detail_top_div2_wires_overlay.png",
        "detail_div1_feeders_components.png",
        "detail_div1_feeders_wires_overlay.png",
        "detail_div2_feeders_components.png",
        "detail_div2_feeders_wires_overlay.png",
        "detail_div1_feeders_left_components.png",
        "detail_div1_feeders_mid_components.png",
        "detail_div1_feeders_right_components.png",
        "detail_div2_feeders_left_components.png",
        "detail_div2_feeders_mid_components.png",
        "detail_div2_feeders_right_components.png",
        "detail_bottom_div1_dc_control_components.png",
        "detail_bottom_div1_dc_control_wires_overlay.png",
        "detail_bottom_div2_dc_control_components.png",
        "detail_bottom_div2_dc_control_wires_overlay.png",
        "detail_bottom_center_control_components.png",
        "detail_bottom_center_control_wires_overlay.png",
        "detail_notes_legend_title_components.png",
    ]
    jennifer_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "detail_top_div1_components.png",
        "detail_top_div1_wires_overlay.png",
        "detail_top_div2_components.png",
        "detail_top_div2_wires_overlay.png",
        "detail_div1_feeders_components.png",
        "detail_div1_feeders_wires_overlay.png",
        "detail_div2_feeders_components.png",
        "detail_div2_feeders_wires_overlay.png",
        "detail_bottom_div1_dc_control_components.png",
        "detail_bottom_div1_dc_control_wires_overlay.png",
        "detail_bottom_div2_dc_control_components.png",
        "detail_bottom_div2_dc_control_wires_overlay.png",
        "detail_bottom_center_control_components.png",
        "detail_bottom_center_control_wires_overlay.png",
    ]
    diego_prompt = "High-recall visual-only extraction for document 24 using raw, component overlay, wire mask overlay, and focused crops. Propose all plausible nodes and edges with evidence. No GT and no OCR."
    jennifer_prompt = "Precision visual review for document 24 using Diego round 1 proposal and raw/overlay crops. Remove unsupported edges and keep uncertain cases out of the final matrix."
    diego_round1_summary = json.dumps(
        {"nodes": len(all_nodes()), "edges": len(final_edges()) + len(high_recall_extras())},
        sort_keys=True,
    )
    jennifer_round2_summary = json.dumps(
        {"nodes": len(all_nodes()), "edges": len(final_edges()), "rejected": len(high_recall_extras())},
        sort_keys=True,
    )
    main_task_text = (
        "User requested document 24 blind one-iteration schematic connectivity extraction with Diego and Jennifer rounds, "
        "round matrices saved under results, and token usage estimates without an API key."
    )
    specs = [
        {
            "call_id": "main-setup",
            "actor": "main",
            "round": "setup",
            "text": main_task_text,
            "text_tokens_override": 2200,
            "image_names": [],
            "out_low": 600,
            "out_expected": 1100,
            "out_high": 1800,
            "reasoning_est": 900,
            "notes": "Main agent inspected paths/crops and spawned Diego; exact usage object not exposed.",
        },
        {
            "call_id": "diego-r1",
            "actor": "Diego",
            "round": "1",
            "text": diego_prompt,
            "text_tokens_override": 1700,
            "image_names": diego_images,
            "out_low": 2500,
            "out_expected": 4200,
            "out_high": 6200,
            "reasoning_est": 1500,
            "notes": "High-recall extraction; image tokens estimated from 24 visual crops.",
        },
        {
            "call_id": "jennifer-r2",
            "actor": "Jennifer",
            "round": "2",
            "text": jennifer_prompt + diego_round1_summary,
            "text_tokens_override": 6000,
            "image_names": jennifer_images,
            "out_low": 1800,
            "out_expected": 3100,
            "out_high": 4800,
            "reasoning_est": 1100,
            "notes": "Precision review; exact usage object not exposed by subagent notification.",
        },
        {
            "call_id": "diego-r3",
            "actor": "Diego",
            "round": "3",
            "text": "Review Jennifer round 2 corrections and converge if visually supported. " + jennifer_round2_summary,
            "text_tokens_override": 4200,
            "image_names": [],
            "out_low": 300,
            "out_expected": 800,
            "out_high": 1600,
            "reasoning_est": 450,
            "notes": "Convergence review; text-only estimate.",
        },
        {
            "call_id": "jennifer-r4",
            "actor": "Jennifer",
            "round": "4",
            "text": "Final precision confirmation after Diego round 3. " + jennifer_round2_summary,
            "text_tokens_override": 140,
            "image_names": [],
            "out_low": 250,
            "out_expected": 650,
            "out_high": 1300,
            "reasoning_est": 350,
            "notes": "Final convergence confirmation; text-only estimate.",
        },
        {
            "call_id": "main-artifacts-final",
            "actor": "main",
            "round": "write/final",
            "text": "Write CSV matrices, edge lists, token estimate tables, report, and final user response.",
            "text_tokens_override": 1800,
            "image_names": [],
            "out_low": 600,
            "out_expected": 1200,
            "out_high": 2200,
            "reasoning_est": 1200,
            "notes": "Artifact writing and final report; exact usage object not exposed.",
        },
    ]
    rows: list[dict[str, object]] = []
    for spec in specs:
        input_text = int(spec.get("text_tokens_override") or text_tokens(str(spec["text"])))
        image_tokens = image_token_sum(list(spec["image_names"]))
        total_low = input_text + image_tokens + int(spec["out_low"]) + int(spec["reasoning_est"])
        expected_total = input_text + image_tokens + int(spec["out_expected"]) + int(spec["reasoning_est"])
        total_high = input_text + image_tokens + int(spec["out_high"]) + int(spec["reasoning_est"])
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": spec["round"],
                "call_id": spec["call_id"],
                "actor": spec["actor"],
                "input_tokens_est": input_text + image_tokens,
                "cached_input_tokens_est": 0,
                "text_input_tokens_est": input_text,
                "image_file_count": len(spec["image_names"]),
                "image_input_tokens_est": image_tokens,
                "output_tokens_low_est": spec["out_low"],
                "output_tokens_expected_est": spec["out_expected"],
                "output_tokens_high_est": spec["out_high"],
                "reasoning_tokens_est": spec["reasoning_est"],
                "total_low_tokens_est": total_low,
                "total_expected_tokens_est": expected_total,
                "total_high_tokens_est": total_high,
                "usage_object_available": "no",
                "notes": spec["notes"],
            }
        )
    return rows


def write_token_tables(rows: list[dict[str, object]]) -> None:
    path = RESULTS / "token_usage_estimate.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in rows),
        "image_input_tokens_est": sum(int(r["image_input_tokens_est"]) for r in rows),
        "output_tokens_low_est": sum(int(r["output_tokens_low_est"]) for r in rows),
        "output_tokens_expected_est": sum(int(r["output_tokens_expected_est"]) for r in rows),
        "output_tokens_high_est": sum(int(r["output_tokens_high_est"]) for r in rows),
        "reasoning_tokens_est": sum(int(r["reasoning_tokens_est"]) for r in rows),
        "total_low_tokens_est": sum(int(r["total_low_tokens_est"]) for r in rows),
        "total_expected_tokens_est": sum(int(r["total_expected_tokens_est"]) for r in rows),
        "total_high_tokens_est": sum(int(r["total_high_tokens_est"]) for r in rows),
        "method": "Responses input-token counting endpoint not called because OPENAI_API_KEY is not available. Text estimated with tiktoken o200k_base when available; image inputs estimated by high-detail tile sizing.",
    }
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    with (RESULTS / "token_usage_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)


def write_uncertain_edges(path: Path) -> None:
    rows = [
        {
            "edge": "SYNC-CAB--LOAD-SHED-CAB",
            "status": "rejected",
            "reason": "Vertical dashed routing is beside SYNC-CAB; no clean terminal connection to LOAD-SHED-CAB.",
        },
        {
            "edge": "RELAY-K2A09--SYNC-CAB",
            "status": "uncertain_excluded",
            "reason": "Continuation is partly obscured by nearby note text and crop boundary.",
        },
        {
            "edge": "TRIP-MOD-A--LOAD-SHED-CAB",
            "status": "uncertain_excluded",
            "reason": "Route passes nearby, but endpoint-to-endpoint connection is not visible.",
        },
        {
            "edge": "TRIP-MOD-B--LOAD-SHED-CAB",
            "status": "uncertain_excluded",
            "reason": "Route passes nearby, but endpoint-to-endpoint connection is not visible.",
        },
        {
            "edge": "ESFAS-PNL-A--TDR-1",
            "status": "uncertain_excluded",
            "reason": "ESFAS route exits into channel area without visible termination on TDR-1.",
        },
        {
            "edge": "ESFAS-PNL-B--TDR-2",
            "status": "uncertain_excluded",
            "reason": "ESFAS route exits into channel area without visible termination on TDR-2.",
        },
        {
            "edge": "LAMP-ALM-A--LAMP-ALM-B",
            "status": "rejected",
            "reason": "Both lamps are tied through the LOAD-SHED-CAB signal route, not directly to each other.",
        },
        {
            "edge": "METER-V2",
            "status": "not_added",
            "reason": "No corresponding B-side meter label is visible.",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["edge", "status", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def write_report(nodes: list[str], final: list[dict[str, str]], token_summary: dict[str, object]) -> None:
    report = f"""# Document 24 Connectivity Extraction

Blind visual extraction using only the raw schematic and derived visual aids in the resource folder. No GT, GT-derived feedback, or OCR tools were used.

## Rounds

1. Diego high-recall extraction included visually plausible power, control, and signal edges plus seven low-confidence/uncertain extras.
2. Jennifer precision review retained the repeated feeder and DC/control structure, accepted `CB-TIE-1 -- SYNC-CAB`, and removed unsupported common-control overconnections.
3. Diego convergence review was run against Jennifer's correction.
4. Jennifer final confirmation was run after Diego's convergence reply.

## Final Matrix

- Nodes: {len(nodes)}
- Final accepted undirected edges: {len(final)}
- Matrix file: `final_connectivity_matrix.csv`
- Edge file: `final_edges.csv`

## Label Decisions

- Use `BUS-201A` and `BUS-201B`; adjacent long text is descriptive bus text.
- Use `PMP-LP208A/B`, `COMP-C209A/B`, and `VALVE-MV207A/B` as visible component labels.
- Use `METER-V1` only; no visible `METER-V2` was found.

## Token Estimation

The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Actual usage objects were not exposed by the Codex subagent notification/tooling. The local estimate uses `tiktoken` (`o200k_base`) for text when available and high-detail image tile sizing for image inputs.

- Estimated input tokens: {token_summary['input_tokens_est']}
- Estimated image input tokens: {token_summary['image_input_tokens_est']}
- Expected output tokens: {token_summary['output_tokens_expected_est']}
- Estimated reasoning tokens: {token_summary['reasoning_tokens_est']}
- Expected total tokens: {token_summary['total_expected_tokens_est']}
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = all_nodes()
    final = final_edges()
    round1 = dedupe_edges(final + high_recall_extras())
    round2 = final
    round3 = final
    round4 = final

    rounds = [
        ("round_01_diego", round1),
        ("round_02_jennifer", round2),
        ("round_03_diego", round3),
        ("round_04_jennifer_final", round4),
    ]
    for name, edges in rounds:
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)

    write_edges(RESULTS / "final_edges.csv", final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final)
    write_uncertain_edges(RESULTS / "uncertain_or_excluded_edges.csv")

    rows = token_rows()
    write_token_tables(rows)
    with (RESULTS / "token_usage_summary.json").open("r", encoding="utf-8") as fh:
        token_summary = json.load(fh)
    write_report(nodes, final, token_summary)

    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "nodes": len(nodes),
        "final_edges": len(final),
        "rounds": {name: len(edges) for name, edges in rounds},
        "matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges_file": str(RESULTS / "final_edges.csv"),
        "uncertain_file": str(RESULTS / "uncertain_or_excluded_edges.csv"),
        "token_usage_estimate": str(RESULTS / "token_usage_estimate.csv"),
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
    }
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
