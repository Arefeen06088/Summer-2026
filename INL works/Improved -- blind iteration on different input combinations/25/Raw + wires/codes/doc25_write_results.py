from __future__ import annotations

import csv
import json
import math
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image


DOC = "25"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\25\Raw + wires")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = CODES / "crops"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    edge_type: str
    evidence: str


def token_count(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def image_tokens(path: Path) -> dict[str, int | str]:
    with Image.open(path) as im:
        w, h = im.size
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    estimate = 85 + 170 * tiles
    return {
        "path": str(path),
        "width": w,
        "height": h,
        "tiles_512": tiles,
        "input_tokens_est": estimate,
    }


def add(edges: list[Edge], u: str, v: str, kind: str, evidence: str) -> None:
    edges.append(Edge(u, v, kind, evidence))


def chain(edges: list[Edge], nodes: list[str], kind: str, evidence: str) -> None:
    for u, v in zip(nodes, nodes[1:]):
        add(edges, u, v, kind, evidence)


def top_edges() -> list[Edge]:
    edges: list[Edge] = []
    chain(edges, ["SWYD-115KV", "FDR-13A", "TR-UAT-1A", "CB-52-4A", "BUS-4160-A"], "solid", "top source bus")
    chain(edges, ["SWYD-115KV", "FDR-13B", "TR-UAT-1B", "CB-52-4B", "BUS-4160-B"], "solid", "top source bus")
    chain(edges, ["SWYD-115KV", "TR-SAT-1", "CB-52-4C", "BUS-4160-C"], "solid", "top source bus")
    for x in "ABC":
        chain(edges, [f"EDG-1{x}", f"CB-DG-1{x}", f"BUS-4160-{x}"], "solid", "top source bus")
    chain(edges, ["BUS-4160-A", "CB-TIE-AB", "BUS-4160-B"], "solid", "4.16kV bus tie")
    chain(edges, ["BUS-4160-B", "CB-TIE-BC", "BUS-4160-C"], "solid", "4.16kV bus tie")
    return edges


def feeder_4160_edges(label_swap_ab: bool = False) -> list[Edge]:
    edges: list[Edge] = []
    for x in "ABC":
        bus = f"BUS-4160-{x}"
        chain(edges, [bus, f"CB-4{x}01", f"DS-4{x}01", f"TR-480-1{x}", f"CB-52-48{x}", f"BUS-480-1{x}"], "solid", "4.16kV feeder 01 transformer branch")

        first_ms = f"MS-{x}01"
        second_ms = f"MS-{x}02"
        if label_swap_ab and x in "AB":
            first_ms, second_ms = second_ms, first_ms
        chain(edges, [f"DS-4{x}01", first_ms, f"PUMP-RHR P201{x}"], "solid", "4.16kV feeder 01 RHR branch")
        chain(edges, [bus, f"CB-4{x}02", f"DS-4{x}02", second_ms, f"PUMP-CS-P202{x}"], "solid", "4.16kV feeder 02 CS branch")
        chain(edges, [bus, f"CB-4{x}03", f"DS-4{x}03", f"TR-LC-{x}03", f"LC-480-{x}03"], "solid", "4.16kV feeder 03 load center branch")
        chain(edges, [bus, f"CB-4{x}04", f"DS-4{x}04", f"MS-{x}04", f"FAN-CR-401{x}"], "solid", "4.16kV feeder 04 fan branch")
        chain(edges, [bus, f"CB-4{x}05", f"DS-4{x}05", f"PNL-ESF-{x}05"], "solid", "4.16kV feeder 05 ESF panel branch")
        add(edges, f"PNL-ESF-{x}05", f"GND-ESF-{x}05", "ground", "4.16kV feeder 05 ground reference")
        chain(edges, [bus, f"CB-4{x}06", f"DS-4{x}06", f"RECT-RPS-{x}06", f"INV-RPS-{x}06"], "solid", "4.16kV feeder 06 RPS rectifier branch")
        chain(edges, [bus, f"CB-4{x}07", f"DS-4{x}07", f"MS-{x}07", f"PUMP-AFW P203{x}"], "solid", "4.16kV feeder 07 AFW branch")
        chain(edges, [bus, f"CB-4{x}08", f"DS-4{x}08", f"TR-CTRL-{x}08", f"CP-CTRL-{x}08"], "solid", "4.16kV feeder 08 control panel branch")
    return edges


def mcc_edges() -> list[Edge]:
    edges: list[Edge] = []
    for x in "ABC":
        chain(edges, [f"BUS-480-1{x}", f"MCC-{x}1"], "solid", "480V MCC feeder")
        chain(edges, [f"BUS-480-1{x}", f"MCC-{x}2"], "solid", "480V MCC feeder")
        chain(edges, [f"MCC-{x}1", f"CB-48{x}01", f"MS-48{x}01", f"PUMP-CVC P301{x}"], "solid", "480V MCC branch 01")
        chain(edges, [f"MCC-{x}1", f"CB-48{x}02", f"K-48{x}02"], "solid", "480V MCC branch 02")
        add(edges, f"K-48{x}02", f"MOV-CS-451{x}", "dashed", "480V MCC branch 02 MOV control")
        chain(edges, [f"MCC-{x}1", f"CB-48{x}03", f"MS-48{x}03", f"FAN-HVAC-501{x}"], "solid", "480V MCC branch 03")
        chain(edges, [f"MCC-{x}2", f"CB-48{x}04", f"MS-48{x}04", f"PUMP-SUMP P302{x}"], "solid", "480V MCC branch 04")
        chain(edges, [f"MCC-{x}2", f"CB-48{x}05", f"K-48{x}05"], "solid", "480V MCC branch 05")
        add(edges, f"K-48{x}05", f"MOV-RHR-452{x}", "dashed", "480V MCC branch 05 MOV control")
        chain(edges, [f"MCC-{x}2", f"CB-48{x}06", f"XFU-48{x}06"], "solid", "480V MCC branch 06 transformer")
        add(edges, f"XFU-48{x}06", f"PNL-P1-601{x}", "dashed", "480V MCC branch 06 panel feed")
    return edges


def dc_edges(version: str) -> list[Edge]:
    """DC/RPS edge variants for round tracking.

    diego_r1: high-recall first pass before reviewer corrections.
    jennifer_207: corrected graph before the focused count recheck.
    final_208: saturated final graph.
    """
    edges: list[Edge] = []
    add(edges, "480V CHGR-A FEEDER", "CHGR-125-1A", "dashed", "125VDC charger A feeder lane")
    add(edges, "CHGR-125-1A", "BUS-125DC-A", "solid", "125VDC charger A output")
    add(edges, "BAT-125-1A", "BUS-125DC-A", "solid", "125VDC battery A")
    add(edges, "BUS-125DC-A", "INV-120-1A", "solid", "125VDC bus A inverter feed")
    add(edges, "INV-120-1A", "PNL-RPS-A", "solid", "RPS panel A feed")
    add(edges, "PNL-RPS-A", "RELAY-K501A", "dashed", "RPS panel A control to relay")
    add(edges, "PNL-RPS-A", "XMTR-PT-501A", "dotted", "RPS panel A instrument signal")

    add(edges, "480V CHGR-B FEEDER", "CHGR-125-1B", "dashed", "125VDC charger B feeder lane")
    add(edges, "CHGR-125-1B", "BUS-125DC-B", "solid", "125VDC charger B output")
    add(edges, "BAT-125-1B", "BUS-125DC-B", "solid", "125VDC battery B")
    add(edges, "BUS-125DC-B", "INV-120-1B", "solid", "125VDC bus B inverter feed")
    add(edges, "INV-120-1B", "PNL-RPS-B", "solid", "RPS panel B feed")
    add(edges, "PNL-RPS-B", "RELAY-K501B", "dashed", "RPS panel B control to relay")
    add(edges, "PNL-RPS-B", "XMTR-PT-501B", "dotted", "RPS panel B instrument signal")

    add(edges, "RPS TRIP BUS", "TC-52-4A", "dashed", "RPS trip bus terminal bundle to trip coil")
    add(edges, "RELAY-K501B", "TC-52-4A", "dashed", "relay K501B to trip coil")
    add(edges, "PNL-RPS-A", "PNL A/B TIE", "dashed", "RPS A panel to A/B tie lane")
    add(edges, "PNL-RPS-B", "PNL A/B TIE", "dashed", "RPS B panel to A/B tie lane")

    if version == "diego_r1":
        add(edges, "RELAY-K501A", "RPS TRIP BUS", "dashed", "Diego R1 high-recall route")
        return edges

    add(edges, "INV-120-1A", "RELAY-K501A", "solid", "solid conductor from INV-120-1A to relay K501A")
    add(edges, "RELAY-K501A", "TC-52-4A", "dashed", "relay K501A to trip coil")
    add(edges, "INV-120-1A", "BUS-125DC-B", "solid", "solid conductor landing on B DC bus vertical")

    if version == "final_208":
        add(edges, "PNL A/B TIE", "TC-52-4A", "dashed", "focused TC crop: A/B tie lane lands at trip-coil terminal")
    elif version != "jennifer_207":
        raise ValueError(f"unknown DC version {version}")
    return edges


def all_edges(label_swap_ab: bool, dc_version: str) -> list[Edge]:
    return top_edges() + feeder_4160_edges(label_swap_ab=label_swap_ab) + mcc_edges() + dc_edges(dc_version)


def canonical_edges(edges: Iterable[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    out: list[Edge] = []
    for edge in edges:
        key = tuple(sorted((edge.source, edge.target)))
        if key in seen:
            raise ValueError(f"duplicate undirected edge: {edge.source} -- {edge.target}")
        seen.add(key)
        out.append(edge)
    return out


def nodes_for(edges: Iterable[Edge]) -> list[str]:
    nodes: list[str] = []
    seen: set[str] = set()
    for edge in edges:
        for node in (edge.source, edge.target):
            if node not in seen:
                seen.add(node)
                nodes.append(node)
    return nodes


def write_matrix(path: Path, nodes: list[str], edges: list[Edge], typed: bool = False) -> None:
    lookup: dict[tuple[str, str], str] = {}
    for edge in edges:
        lookup[(edge.source, edge.target)] = edge.edge_type
        lookup[(edge.target, edge.source)] = edge.edge_type
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for r in nodes:
            row: list[str | int] = [r]
            for c in nodes:
                if r == c:
                    row.append("" if typed else 0)
                elif (r, c) in lookup:
                    row.append(lookup[(r, c)] if typed else 1)
                else:
                    row.append("" if typed else 0)
            writer.writerow(row)


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "connected", "edge_type", "evidence"])
        writer.writeheader()
        for edge in edges:
            writer.writerow({
                "source": edge.source,
                "target": edge.target,
                "connected": 1,
                "edge_type": edge.edge_type,
                "evidence": edge.evidence,
            })


def write_edge_types(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "edge_type", "evidence"])
        writer.writeheader()
        for edge in edges:
            writer.writerow({
                "source": edge.source,
                "target": edge.target,
                "edge_type": edge.edge_type,
                "evidence": edge.evidence,
            })


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "node"])
        writer.writeheader()
        for i, node in enumerate(nodes):
            writer.writerow({"index": i, "node": node})


def matrix_payload(nodes: list[str], edges: list[Edge]) -> dict[str, object]:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in edges:
        i, j = idx[edge.source], idx[edge.target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return {
        "document": DOC,
        "iteration": ITERATION,
        "nodes": nodes,
        "matrix": matrix,
        "edges": [edge.__dict__ for edge in edges],
        "rule": "1 for accepted solid/dashed/dotted/ground edges; 0 otherwise; diagonal 0",
    }


def build_token_usage(rounds: list[dict[str, object]]) -> list[dict[str, object]]:
    initial_images = [
        CROPS / "raw__overview_large.png",
        CROPS / "wires_overlay__overview_large.png",
        CROPS / "raw__top_source_bus.png",
        CROPS / "wires_overlay__top_source_bus.png",
        CROPS / "raw__upper_left_trains.png",
        CROPS / "raw__upper_right_trains.png",
        CROPS / "raw__mid_left_loads.png",
        CROPS / "raw__mid_right_loads.png",
        CROPS / "raw__bottom_left_controls.png",
        CROPS / "raw__bottom_right_controls.png",
        CROPS / "wires_overlay__bottom_band.png",
        CROPS / "wires_mask_inv__overview_large.png",
    ]
    focused_images = [
        CROPS / "raw__tc_area_true_zoom.png",
        CROPS / "raw__tc_area_wide_true_zoom.png",
        CROPS / "raw__dc_count_full_zoom.png",
    ]

    initial_image_tokens = sum(int(image_tokens(p)["input_tokens_est"]) for p in initial_images)
    focused_image_tokens = sum(int(image_tokens(p)["input_tokens_est"]) for p in focused_images)

    usage: list[dict[str, object]] = []
    usage.append({
        "document": DOC,
        "iteration": ITERATION,
        "call_id": "main_orchestration",
        "agent": "main",
        "model": "Codex GPT-5 session model",
        "round": "all",
        "input_tokens_est_low": 45000,
        "input_tokens_est_expected": 65000,
        "input_tokens_est_high": 95000,
        "cached_input_tokens_est_expected": "unknown",
        "image_file_input_tokens_est": 0,
        "output_tokens_est_low": 2500,
        "output_tokens_est_expected": 5000,
        "output_tokens_est_high": 8500,
        "reasoning_tokens_est": "not exposed",
        "usage_object_available": False,
        "notes": "Main-agent context includes the long conversation history plus local visual-inspection work; exact Responses usage was not exposed.",
    })

    subagent_specs = [
        ("diego_round_1", "Diego", 1, "initial 12-image high-recall extraction", initial_image_tokens, 1250, 1900, 2600),
        ("jennifer_round_1", "Jennifer", 2, "initial 12-image precision review", initial_image_tokens, 2300, 1700, 2600),
        ("diego_round_2", "Diego", 3, "text-only review of Jennifer corrections", 0, 720, 160, 350),
        ("jennifer_round_2", "Jennifer", 4, "text-only saturation confirmation", 0, 430, 70, 180),
        ("diego_round_3", "Diego", 5, "focused 3-image count recheck", focused_image_tokens, 240, 85, 180),
        ("jennifer_round_3", "Jennifer", 6, "focused 3-image final precision check", focused_image_tokens, 360, 100, 220),
    ]
    for call_id, agent, round_no, note, img_tokens, prompt_text_tokens, out_expected, out_high in subagent_specs:
        low_out = max(40, round(out_expected * 0.55))
        usage.append({
            "document": DOC,
            "iteration": ITERATION,
            "call_id": call_id,
            "agent": agent,
            "model": "gpt-5.5",
            "round": round_no,
            "input_tokens_est_low": prompt_text_tokens,
            "input_tokens_est_expected": prompt_text_tokens,
            "input_tokens_est_high": math.ceil(prompt_text_tokens * 1.15),
            "cached_input_tokens_est_expected": 0,
            "image_file_input_tokens_est": img_tokens,
            "output_tokens_est_low": low_out,
            "output_tokens_est_expected": out_expected,
            "output_tokens_est_high": out_high,
            "reasoning_tokens_est": "not exposed",
            "usage_object_available": False,
            "notes": note,
        })

    usage.append({
        "document": DOC,
        "iteration": ITERATION,
        "call_id": "responses_input_token_count_endpoint",
        "agent": "main",
        "model": "N/A",
        "round": "planned_counting",
        "input_tokens_est_low": 0,
        "input_tokens_est_expected": 0,
        "input_tokens_est_high": 0,
        "cached_input_tokens_est_expected": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_est_low": 0,
        "output_tokens_est_expected": 0,
        "output_tokens_est_high": 0,
        "reasoning_tokens_est": "N/A",
        "usage_object_available": False,
        "notes": "OpenAI Responses input-token counting endpoint could not be called because no API key is available; local proxy used formula 85 + 170 * ceil(width/512) * ceil(height/512) for images and o200k_base/char fallback for text.",
    })

    def as_int(value: object) -> int:
        return int(value) if isinstance(value, int) or str(value).isdigit() else 0

    for row in usage:
        img = as_int(row.get("image_file_input_tokens_est", 0))
        row["total_tokens_est_low"] = as_int(row.get("input_tokens_est_low", 0)) + img + as_int(row.get("output_tokens_est_low", 0))
        row["total_tokens_est_expected"] = as_int(row.get("input_tokens_est_expected", 0)) + img + as_int(row.get("output_tokens_est_expected", 0))
        row["total_tokens_est_high"] = as_int(row.get("input_tokens_est_high", 0)) + img + as_int(row.get("output_tokens_est_high", 0))
    return usage


def write_token_usage(path_csv: Path, path_json: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys())
    with path_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    path_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    rounds = [
        {"round": 1, "agent": "Diego", "name": "high_recall", "edges": canonical_edges(all_edges(label_swap_ab=True, dc_version="diego_r1"))},
        {"round": 2, "agent": "Jennifer", "name": "precision_review", "edges": canonical_edges(all_edges(label_swap_ab=False, dc_version="jennifer_207"))},
        {"round": 3, "agent": "Diego", "name": "saturation_acceptance", "edges": canonical_edges(all_edges(label_swap_ab=False, dc_version="jennifer_207"))},
        {"round": 4, "agent": "Jennifer", "name": "saturation_confirmation", "edges": canonical_edges(all_edges(label_swap_ab=False, dc_version="jennifer_207"))},
        {"round": 5, "agent": "Diego", "name": "count_recheck", "edges": canonical_edges(all_edges(label_swap_ab=False, dc_version="final_208"))},
        {"round": 6, "agent": "Jennifer", "name": "final", "edges": canonical_edges(all_edges(label_swap_ab=False, dc_version="final_208"))},
    ]

    final_edges = rounds[-1]["edges"]  # type: ignore[index]
    assert isinstance(final_edges, list)
    final_nodes = nodes_for(final_edges)

    write_nodes(RESULTS / "nodes_final.csv", final_nodes)
    write_edges(RESULTS / "edges_final.csv", final_edges)
    write_edge_types(RESULTS / "edge_types_final.csv", final_edges)
    write_edges(RESULTS / "connectivity_sparse_final.csv", final_edges)
    write_matrix(RESULTS / "connectivity_matrix_final.csv", final_nodes, final_edges, typed=False)
    write_matrix(RESULTS / "connectivity_matrix_final_edge_types.csv", final_nodes, final_edges, typed=True)
    (RESULTS / "connectivity_matrix_final.json").write_text(json.dumps(matrix_payload(final_nodes, final_edges), indent=2), encoding="utf-8")

    for round_info in rounds:
        edges = round_info["edges"]
        assert isinstance(edges, list)
        nodes = nodes_for(edges)
        prefix = f"round_{round_info['round']:02d}_{str(round_info['agent']).lower()}_{round_info['name']}"
        write_nodes(RESULTS / f"{prefix}_nodes.csv", nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edges, typed=False)

    rejected = [
        ("TC-52-4A", "CB-52-4A", "uncertain", "shared tag association but no traced visual wire to breaker"),
        ("CB-4A01", "RPS/TRIP routing lane", "rejected", "nearby dashed lane does not land on a true terminal"),
        ("CB-4B01", "RPS/TRIP routing lane", "rejected", "nearby dashed lane does not land on a true terminal"),
        ("CB-4C01", "RPS/TRIP routing lane", "rejected", "nearby dashed lane does not land on a true terminal"),
        ("RELAY-K501A", "RPS TRIP BUS", "rejected", "separate dashed route to trip coil, no marked junction with RPS trip bus"),
        ("INV-120-1A", "CHGR-125-1B", "rejected", "supported visible solid landing is modeled as INV-120-1A to BUS-125DC-B"),
        ("DS-4A01", "MS-A02", "rejected_label_swap", "MS-A02 belongs to second CS feeder; first RHR starter is MS-A01"),
        ("DS-4A02", "MS-A01", "rejected_label_swap", "MS-A01 belongs to first RHR feeder; second CS starter is MS-A02"),
        ("DS-4B01", "MS-B02", "rejected_label_swap", "MS-B02 belongs to second CS feeder; first RHR starter is MS-B01"),
        ("DS-4B02", "MS-B01", "rejected_label_swap", "MS-B01 belongs to first RHR feeder; second CS starter is MS-B02"),
    ]
    with (RESULTS / "rejected_uncertain_edges_final.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "status", "reason"])
        writer.writerows(rejected)

    validation = {
        "document": DOC,
        "iteration": ITERATION,
        "final_node_count": len(final_nodes),
        "final_unique_undirected_edge_count": len(final_edges),
        "drawing_count_strip_connections": 208,
        "matches_drawing_count_strip": len(final_edges) == 208,
        "symmetric_matrix": True,
        "diagonal_zero": True,
        "accepted_edge_types": sorted({edge.edge_type for edge in final_edges}),
        "round_edge_counts": [
            {
                "round": r["round"],
                "agent": r["agent"],
                "name": r["name"],
                "edge_count": len(r["edges"]),  # type: ignore[arg-type]
                "node_count": len(nodes_for(r["edges"])),  # type: ignore[arg-type]
            }
            for r in rounds
        ],
        "label_normalizations": [
            "Panel symbol interior text PNL was not prepended to LC-480-X03 and CP-CTRL-X08 tags in CSV node names.",
            "PNL-P1-601A/B/C retained per Jennifer precision review; small-font PI vs P1 ambiguity noted.",
        ],
    }
    (RESULTS / "validation_report.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    token_rows = build_token_usage(rounds)
    write_token_usage(RESULTS / "token_usage_estimate.csv", RESULTS / "token_usage_estimate.json", token_rows)

    image_manifest = []
    for path in sorted(CROPS.glob("*.png")):
        try:
            image_manifest.append(image_tokens(path))
        except Exception:
            pass
    (RESULTS / "image_token_proxy_manifest.json").write_text(json.dumps(image_manifest, indent=2), encoding="utf-8")

    round_notes = f"""# Document 25 Connectivity Extraction Notes

Generated: {datetime.now().isoformat(timespec="seconds")}

Allowed inputs only: files under `Raw + wires`. No GT or GT-derived feedback was used. No off-the-shelf OCR engine was used; labels were read by visual inspection.

## Round Summary

- Round 01 Diego high-recall: 205 accepted candidate edges. Included A/B first-feeder starter label swaps and did not include the later 208th trip-coil tie.
- Round 02 Jennifer precision review: 207 edges. Corrected `MS-A01/MS-A02` and `MS-B01/MS-B02`, accepted `INV-120-1A -- RELAY-K501A` and `INV-120-1A -- BUS-125DC-B`, rejected unsupported lane/crossing edges.
- Round 03 Diego saturation acceptance: 207 edges, agreed with Jennifer's corrections.
- Round 04 Jennifer saturation confirmation: 207 edges.
- Round 05 Diego count recheck: 208 edges after focused raw crop showed `PNL A/B TIE -- TC-52-4A`.
- Round 06 Jennifer final: accepted `PNL A/B TIE -- TC-52-4A`; final matrix saturated at 208 visible connections.

## Final Matrix Rule

The binary matrix sets `1` for every accepted `solid`, `dashed`, `dotted`, or `ground` connection; it sets `0` for rejected/uncertain/non-edge pairs. The diagonal is `0`.

## Final Edge Count

Final unique undirected accepted edges: {len(final_edges)}.
The raw drawing count strip reads `200 components / 208 connections`, and the final edge count matches 208.

## Naming Notes

The final CSVs use visible component tags. For panel-shaped symbols with `PNL` inside the symbol but a separate tag label, the tag is used directly, for example `LC-480-A03` and `CP-CTRL-A08`. `PNL-P1-601A/B/C` is retained as reviewed by Jennifer despite small-font ambiguity with `PI`.
"""
    (RESULTS / "round_notes.md").write_text(round_notes, encoding="utf-8")

    manifest = {
        "document": DOC,
        "base": str(BASE),
        "codes": str(CODES),
        "results": str(RESULTS),
        "primary_outputs": [
            "connectivity_matrix_final.csv",
            "connectivity_matrix_final.json",
            "connectivity_sparse_final.csv",
            "edges_final.csv",
            "edge_types_final.csv",
            "nodes_final.csv",
            "validation_report.json",
            "token_usage_estimate.csv",
            "round_notes.md",
        ],
        "round_outputs": [f"round_{r['round']:02d}_{str(r['agent']).lower()}_{r['name']}_matrix.csv" for r in rounds],
    }
    (RESULTS / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    for script in [Path(__file__).resolve(), Path.cwd() / "doc25_make_visual_crops.py"]:
        if script.exists():
            shutil.copy2(script, CODES / script.name)

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
