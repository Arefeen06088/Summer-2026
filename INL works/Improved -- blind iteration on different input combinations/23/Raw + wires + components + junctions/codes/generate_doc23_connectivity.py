from __future__ import annotations

import csv
import json
import math
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = BASE / "codes" / "crops"
DOC_ID = "23"
ITERATION = "1"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    edge_type: str
    evidence: str


LOAD_CENTERS = [
    {
        "code": "1A",
        "source": "BUS-4160-A",
        "loads": ("PUMP-P101", "MOTOR-M102", "VALVE-MOV103", "FAN-F104", "HTR-H105", "VALVE-XV106"),
        "notes": ("INST-1A", "JB-1A-1", "RELAY-K11", "RELAY-K12"),
    },
    {
        "code": "1C",
        "source": "BUS-4160-ESF-A",
        "loads": ("PUMP-P131", "MOTOR-M132", "VALVE-MOV133", "FAN-F134", "HTR-H135", "VALVE-XV136"),
        "notes": ("INST-1C", "JB-1C-1", "RELAY-K21", "RELAY-K22"),
    },
    {
        "code": "1B",
        "source": "BUS-4160-B",
        "loads": ("PUMP-P161", "MOTOR-M162", "VALVE-MOV163", "FAN-F164", "HTR-H165", "VALVE-XV166"),
        "notes": ("INST-1B", "JB-1B-1", "RELAY-K31", "RELAY-K32"),
    },
    {
        "code": "2A",
        "source": "BUS-4160-ESF-A",
        "loads": ("PUMP-P201", "MOTOR-M202", "VALVE-MOV203", "FAN-F204", "HTR-H205", "VALVE-XV206"),
        "notes": ("INST-2A", "JB-2A-1", "RELAY-K41", "RELAY-K42"),
    },
    {
        "code": "2C",
        "source": "BUS-4160-ESF-A",
        "loads": ("PUMP-P231", "MOTOR-M232", "VALVE-MOV233", "FAN-F234", "HTR-H235", "VALVE-XV236"),
        "notes": ("INST-2C", "JB-2C-1", "RELAY-K51", "RELAY-K52"),
    },
    {
        "code": "2B",
        "source": "BUS-4160-ESF-B",
        "loads": ("PUMP-P261", "MOTOR-M262", "VALVE-MOV263", "FAN-F264", "HTR-H265", "VALVE-XV266"),
        "notes": ("INST-2B", "JB-2B-1", "RELAY-K61", "RELAY-K62"),
    },
]


def add_edge(edges: list[Edge], seen: set[tuple[str, str]], a: str, b: str, edge_type: str, evidence: str) -> None:
    if a == b:
        return
    key = tuple(sorted((a, b)))
    if key in seen:
        return
    seen.add(key)
    edges.append(Edge(a, b, edge_type, evidence))


def add_chain(edges: list[Edge], seen: set[tuple[str, str]], nodes: list[str], edge_type: str, evidence: str) -> None:
    for a, b in zip(nodes, nodes[1:]):
        add_edge(edges, seen, a, b, edge_type, evidence)


def build_solid_edges(include_jennifer_additions: bool) -> list[Edge]:
    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()

    add_chain(edges, seen, ["GRID-161A", "DS-101", "CB-101", "TR-UAT-1A", "CB-102", "BUS-4160-A"], "power", "Solid A unit auxiliary source chain.")
    add_chain(edges, seen, ["GRID-161B", "DS-102", "CB-103", "TR-UAT-1B", "CB-104", "BUS-4160-B"], "power", "Solid B unit auxiliary source chain.")
    add_chain(edges, seen, ["BUS-4160-A", "CB-TIE-41", "BUS-4160-B"], "power", "Solid 4160 V bus tie.")
    add_chain(edges, seen, ["BUS-4160-A", "CB-ESF-A", "BUS-4160-ESF-A"], "power", "Solid A normal-to-ESF feeder.")
    add_chain(edges, seen, ["BUS-4160-B", "CB-ESF-B", "BUS-4160-ESF-B"], "power", "Solid B normal-to-ESF feeder.")
    add_chain(edges, seen, ["DG-1A", "CB-DG1A", "ATS-1A", "BUS-4160-ESF-A"], "power", "Solid A diesel/ATS feeder to ESF bus.")
    add_chain(edges, seen, ["DG-1B", "CB-DG1B", "ATS-1B", "BUS-4160-ESF-B"], "power", "Solid B diesel/ATS feeder to ESF bus.")

    if include_jennifer_additions:
        add_edge(edges, seen, "BUS-4160-A", "GND-41A", "ground", "Direct solid top-bus ground drop accepted by Jennifer.")
        add_edge(edges, seen, "BUS-4160-B", "GND-41B", "ground", "Direct solid top-bus ground drop accepted by Jennifer.")

    for center in LOAD_CENTERS:
        code = center["code"]
        source = center["source"]
        pump, motor, mov, fan, heater, xv = center["loads"]
        add_chain(
            edges,
            seen,
            [source, f"CB-{code}-FDR", f"DS-{code}-ISO", f"TR-{code}", f"CB-{code}-MAIN", f"BUS-480-{code}"],
            "power",
            f"Solid feeder chain to 480 V load center {code}.",
        )
        add_edge(edges, seen, f"BUS-480-{code}", f"MCC-{code}-1", "power", f"Solid bus tap to MCC {code}-1.")
        add_edge(edges, seen, f"MCC-{code}-1", pump, "power", f"Solid MCC {code}-1 load branch.")
        add_edge(edges, seen, f"MCC-{code}-1", motor, "power", f"Solid MCC {code}-1 load branch.")
        add_edge(edges, seen, f"BUS-480-{code}", f"MCC-{code}-2", "power", f"Solid bus tap to MCC {code}-2.")
        add_edge(edges, seen, f"MCC-{code}-2", mov, "power", f"Solid MCC {code}-2 load branch.")
        add_edge(edges, seen, f"MCC-{code}-2", fan, "power", f"Solid MCC {code}-2 load branch.")
        add_edge(edges, seen, f"BUS-480-{code}", f"MCC-{code}-3", "power", f"Solid bus tap to MCC {code}-3.")
        add_edge(edges, seen, f"MCC-{code}-3", heater, "power", f"Solid MCC {code}-3 load branch.")
        add_edge(edges, seen, f"MCC-{code}-3", xv, "power", f"Solid MCC {code}-3 load branch.")
        add_edge(edges, seen, f"BUS-480-{code}", f"PNL-{code}", "power", f"Direct solid panel supply drop for {code}.")
        add_edge(edges, seen, f"BUS-480-{code}", f"GND-{code}", "ground", f"Direct solid 480 V ground drop for {code}.")

    add_chain(edges, seen, ["BUS-480-2A", "CB-DC-A", "RECT-125A", "BUS-125DC-A"], "dc", "Solid A DC rectifier feed.")
    add_edge(edges, seen, "BUS-125DC-A", "BAT-125A", "dc", "Direct solid battery A connection.")
    add_edge(edges, seen, "BUS-125DC-A", "CHGR-AUX-A", "dc", "Direct solid auxiliary charger A drop.")
    add_chain(edges, seen, ["BUS-125DC-A", "INV-1A", "UPS-1A", "CB-UPS-A", "BUS-120AC-A"], "ups", "Solid A DC-to-UPS chain.")
    add_edge(edges, seen, "BUS-120AC-A", "PNL-RPS-A", "ups", "Direct solid A RPS panel supply.")
    add_edge(edges, seen, "BUS-120AC-A", "FUSE-FU-A", "ups", "Direct solid A fuse drop.")
    add_edge(edges, seen, "BUS-125DC-A", "GND-DC-A", "ground", "Direct solid A DC ground drop.")

    add_chain(edges, seen, ["BUS-125DC-A", "CB-DCTIE", "BUS-125DC-B"], "dc", "Solid 125 VDC A/B tie breaker path.")

    add_chain(edges, seen, ["BUS-480-2B", "CB-DC-B", "RECT-125B", "BUS-125DC-B"], "dc", "Solid B DC rectifier feed.")
    add_edge(edges, seen, "BUS-125DC-B", "BAT-125B", "dc", "Direct solid battery B connection.")
    add_edge(edges, seen, "BUS-125DC-B", "CHGR-AUX-B", "dc", "Direct solid auxiliary charger B drop.")
    add_chain(edges, seen, ["BUS-125DC-B", "INV-1B", "UPS-1B", "CB-UPS-B", "BUS-120AC-B"], "ups", "Solid B DC-to-UPS chain.")
    add_edge(edges, seen, "BUS-120AC-B", "PNL-RPS-B", "ups", "Direct solid B RPS panel supply.")
    add_edge(edges, seen, "BUS-120AC-B", "FUSE-FU-B", "ups", "Direct solid B fuse drop.")
    add_edge(edges, seen, "BUS-125DC-B", "GND-DC-B", "ground", "Direct solid B DC ground drop.")

    add_chain(edges, seen, ["BUS-125DC-A", "DC-DC-1", "BUS-24DC-C"], "dc", "Solid DC/DC converter to 24 VDC bus.")
    add_edge(edges, seen, "BUS-24DC-C", "BAT-24C", "dc", "Direct solid 24 VDC battery connection.")
    add_edge(edges, seen, "BUS-24DC-C", "PNL-RADMON", "dc", "Direct solid radiation monitor panel supply.")
    if include_jennifer_additions:
        add_edge(edges, seen, "BUS-24DC-C", "PNL-DCS-A", "dc", "Direct solid 24 VDC panel supply accepted by Jennifer.")
        add_edge(edges, seen, "BUS-24DC-C", "PNL-DCS-B", "dc", "Direct solid 24 VDC panel supply accepted by Jennifer.")

    return edges


def build_high_recall_edges() -> list[Edge]:
    edges = build_solid_edges(include_jennifer_additions=False)
    seen = {tuple(sorted((edge.source, edge.target))) for edge in edges}

    top_candidates = [
        ("BUS-4160-A", "RELAY-87A"),
        ("BUS-4160-A", "RELAY-27A"),
        ("BUS-4160-A", "METER-A"),
        ("BUS-4160-A", "PT-41A"),
        ("CB-TIE-41", "SYNC-41"),
        ("BUS-4160-B", "RELAY-87B"),
        ("BUS-4160-B", "RELAY-27B"),
        ("BUS-4160-B", "METER-B"),
        ("BUS-4160-B", "PT-41B"),
    ]
    for a, b in top_candidates:
        add_edge(edges, seen, a, b, "instrument_or_control_candidate", "Diego round-1 notes-only candidate on dashed/instrument drop.")

    for center in LOAD_CENTERS:
        code = center["code"]
        inst, jb, relay_1, relay_2 = center["notes"]
        xv = center["loads"][5]
        add_edge(edges, seen, f"BUS-480-{code}", inst, "instrument_candidate", "Diego round-1 long-dashed instrument candidate.")
        add_edge(edges, seen, f"PNL-{code}", jb, "control_candidate", "Diego round-1 dashed panel/control candidate.")
        add_edge(edges, seen, jb, relay_1, "control_candidate", "Diego round-1 dashed control candidate.")
        add_edge(edges, seen, jb, relay_2, "control_candidate", "Diego round-1 dashed control candidate.")
        add_edge(edges, seen, relay_1, relay_2, "control_candidate", "Diego round-1 dashed relay candidate.")
        add_edge(edges, seen, jb, xv, "control_candidate", "Diego round-1 local XV control candidate.")

    for a, b in [
        ("BUS-125DC-A", "METER-DC-A"),
        ("BUS-125DC-B", "METER-DC-B"),
        ("BUS-120AC-A", "RELAY-KA1"),
        ("BUS-120AC-A", "RELAY-KA2"),
        ("BUS-120AC-A", "ANN-A"),
        ("BUS-120AC-A", "REC-SER-A"),
        ("PNL-RPS-A", "INST-NIS-A"),
        ("PNL-RPS-A", "PNL-DCS-A"),
        ("PNL-DCS-A", "JB-CTRL-A"),
        ("BUS-120AC-B", "RELAY-KB1"),
        ("BUS-120AC-B", "RELAY-KB2"),
        ("BUS-120AC-B", "ANN-B"),
        ("BUS-120AC-B", "REC-SER-B"),
        ("PNL-RPS-B", "INST-NIS-B"),
        ("PNL-RPS-B", "PNL-DCS-B"),
        ("PNL-DCS-B", "JB-CTRL-B"),
        ("BUS-24DC-C", "RELAY-KTIE"),
    ]:
        add_edge(edges, seen, a, b, "control_or_instrument_candidate", "Diego round-1 RPS/DCS notes-only candidate.")

    return edges


def node_order(edges: list[Edge]) -> list[str]:
    ordered: OrderedDict[str, None] = OrderedDict()
    for edge in edges:
        ordered.setdefault(edge.source, None)
        ordered.setdefault(edge.target, None)
    return list(ordered.keys())


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "edge_type", "evidence"])
        for edge in edges:
            writer.writerow([edge.source, edge.target, edge.edge_type, edge.evidence])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "name"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    adjacency = {node: {other: 0 for other in nodes} for node in nodes}
    for edge in edges:
        adjacency[edge.source][edge.target] = 1
        adjacency[edge.target][edge.source] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component"] + nodes)
        for node in nodes:
            writer.writerow([node] + [0 if node == other else adjacency[node][other] for other in nodes])


def write_round(round_name: str, actor: str, policy: str, edges: list[Edge]) -> dict[str, object]:
    nodes = node_order(edges)
    prefix = RESULTS / round_name
    write_nodes(prefix.with_name(prefix.name + "_nodes.csv"), nodes)
    write_edges(prefix.with_name(prefix.name + "_edges.csv"), edges)
    write_matrix(prefix.with_name(prefix.name + "_connectivity_matrix.csv"), nodes, edges)
    return {
        "round": round_name,
        "actor": actor,
        "policy": policy,
        "nodes": len(nodes),
        "edges": len(edges),
        "matrix": prefix.with_name(prefix.name + "_connectivity_matrix.csv").name,
    }


def validate_matrix(nodes: list[str], edges: list[Edge]) -> dict[str, object]:
    adjacency = {node: {other: 0 for other in nodes} for node in nodes}
    for edge in edges:
        adjacency[edge.source][edge.target] = 1
        adjacency[edge.target][edge.source] = 1
    return {
        "symmetric": all(adjacency[a][b] == adjacency[b][a] for a in nodes for b in nodes),
        "diagonal_zero": all(adjacency[node][node] == 0 for node in nodes),
    }


def estimate_text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def estimate_file_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return estimate_text_tokens(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return 0


def estimate_image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        from PIL import Image

        Image.MAX_IMAGE_PIXELS = None
        with Image.open(path) as image:
            width, height = image.size
    except Exception:
        return 0
    scale = min(1.0, 2048 / max(width, height))
    width *= scale
    height *= scale
    shortest = min(width, height)
    if shortest > 768:
        scale = 768 / shortest
        width *= scale
        height *= scale
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def token_rows() -> list[dict[str, object]]:
    raw = BASE / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png"
    components = BASE / "detected_components_overlay.png"
    wires = BASE / "wires_mask_overlay.png"
    nodes_overlay = BASE / "wire_nodes_overlay.png"
    wire_nodes = BASE / "wire_nodes.csv"
    diego_images = [
        CROPS / "raw__overview.png",
        CROPS / "raw__top_full_power_2x.png",
        CROPS / "raw__train_a_full_2x.png",
        CROPS / "raw__train_b_full_2x.png",
        CROPS / "raw__train_c_full_2x.png",
        CROPS / "raw__dc_ups_left_2x.png",
        CROPS / "raw__dc_ups_right_2x.png",
        CROPS / "raw__vital_ac_a_detail_2x.png",
        CROPS / "raw__vital_ac_b_detail_2x.png",
    ]
    jennifer_images = [
        CROPS / "raw__top_full_power_2x.png",
        CROPS / "raw__ats_1a_detail_2x.png",
        CROPS / "raw__ats_1b_detail_2x.png",
        CROPS / "raw__dc_ups_left_2x.png",
        CROPS / "raw__dc_ups_right_2x.png",
        CROPS / "raw__lower_dc_cross_tie_2x.png",
        CROPS / "raw__vital_ac_a_detail_2x.png",
        CROPS / "raw__vital_ac_b_detail_2x.png",
    ]
    rows = [
        ("main_01_resource_inventory_crop_generation", "main", "setup", 3600, [raw, components, wires, nodes_overlay], estimate_file_tokens(wire_nodes), 650, 1800, "Local file inventory, visual crop creation, and no-GT planning."),
        ("subagent_diego_01_high_recall", "Diego", "round_01", 2600, diego_images, estimate_file_tokens(wire_nodes), 1650, 2900, "High-recall extraction; actual usage object unavailable."),
        ("subagent_jennifer_01_precision", "Jennifer", "round_02", 3300, jennifer_images, 0, 1200, 2400, "Precision review of Diego proposal; actual usage object unavailable."),
        ("subagent_diego_02_saturation", "Diego", "round_03", 850, [CROPS / "raw__top_full_power_2x.png", CROPS / "raw__vital_ac_a_detail_2x.png"], 0, 220, 800, "Saturation check of Jennifer additions; actual usage object unavailable."),
        ("subagent_jennifer_02_final", "Jennifer", "round_04", 450, [], 0, 120, 450, "Final no-change confirmation/record if needed; estimated because no usage object exposed."),
        ("main_02_artifact_generation_validation", "main", "final_artifacts", 4600, [], 0, 600, 1400, "Generator implementation, CSV/JSON validation, and final response."),
    ]
    output: list[dict[str, object]] = []
    for call_id, actor, round_name, text_tokens, image_paths, file_tokens, output_expected, reasoning_expected, notes in rows:
        image_tokens = sum(estimate_image_tokens(path) for path in image_paths)
        input_expected = text_tokens + image_tokens + file_tokens
        total_expected = input_expected + output_expected + reasoning_expected
        output.append(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "call_id": call_id,
                "actor": actor,
                "round": round_name,
                "input_tokens_low_est": math.floor(input_expected * 0.85),
                "input_tokens_expected_est": input_expected,
                "input_tokens_high_est": math.ceil(input_expected * 1.25),
                "cached_input_tokens": "unavailable",
                "text_input_tokens_est": text_tokens,
                "file_input_tokens_est": file_tokens,
                "image_file_input_tokens_est": image_tokens,
                "output_tokens_low_est": math.floor(output_expected * 0.75),
                "output_tokens_expected_est": output_expected,
                "output_tokens_high_est": math.ceil(output_expected * 1.5),
                "reasoning_tokens_low_est": math.floor(reasoning_expected * 0.5),
                "reasoning_tokens_expected_est": reasoning_expected,
                "reasoning_tokens_high_est": math.ceil(reasoning_expected * 1.75),
                "total_tokens_low_est": math.floor(total_expected * 0.75),
                "total_tokens_expected_est": total_expected,
                "total_tokens_high_est": math.ceil(total_expected * 1.45),
                "usage_object_available": "no",
                "counting_endpoint_status": "not_called_no_api_key",
                "notes": notes,
            }
        )
    return output


def write_token_estimates(rows: list[dict[str, object]]) -> None:
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    total = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "input_tokens_expected_est": sum(int(row["input_tokens_expected_est"]) for row in rows),
        "image_file_input_tokens_expected_est": sum(int(row["image_file_input_tokens_est"]) for row in rows),
        "output_tokens_expected_est": sum(int(row["output_tokens_expected_est"]) for row in rows),
        "reasoning_tokens_expected_est": sum(int(row["reasoning_tokens_expected_est"]) for row in rows),
        "total_tokens_low_est": sum(int(row["total_tokens_low_est"]) for row in rows),
        "total_tokens_expected_est": sum(int(row["total_tokens_expected_est"]) for row in rows),
        "total_tokens_high_est": sum(int(row["total_tokens_high_est"]) for row in rows),
        "method": "Local text-token estimates plus local high-detail image tile heuristic. The OpenAI Responses input-token counting endpoint was not called because no API key is available.",
    }
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps({"calls": rows, "total": total}, indent=2), encoding="utf-8")


def write_notes(round_summaries: list[dict[str, object]], final_nodes: list[str], final_edges: list[Edge]) -> None:
    notes_only = [
        "Top relays/meters/PT/sync: RELAY-87A/B, RELAY-27A/B, METER-A/B, PT-41A/B, SYNC-41",
        "Load-center instruments and control wiring: INST-*, JB-*-1, RELAY-K*, dashed local XV controls",
        "DC/RPS metering and controls: METER-DC-A/B, RELAY-KA/KB/KTIE, ANN-A/B, REC-SER-A/B, INST-NIS-A/B, JB-CTRL-A/B",
        "PNL-DCS-A/B to JB-CTRL-A/B continuations are dashed/control notes only",
    ]
    lines = [
        "# Document 23 Connectivity Extraction",
        "",
        "Scope: one blind iteration using only the document 23 `Raw + wires + components + junctions` folder and generated crops. No GT or GT-derived feedback was used.",
        "",
        "Visual method: native visual inspection of the raw diagram and derived overlays/crops. No off-the-shelf OCR engine was used.",
        "",
        "Final policy: primary matrix contains visually supported solid power/DC/UPS paths, direct solid panel/fuse drops, and direct solid grounding drops. Dashed control/interlock and long-dashed instrument/metering relationships are notes only.",
        "",
        f"Final node count: {len(final_nodes)}",
        f"Final edge count: {len(final_edges)}",
        "",
        "Jennifer precision additions retained in final:",
        "- BUS-4160-A -- GND-41A",
        "- BUS-4160-B -- GND-41B",
        "- BUS-24DC-C -- PNL-DCS-A",
        "- BUS-24DC-C -- PNL-DCS-B",
        "",
        "Notes-only visual candidates removed from primary scoring matrix:",
    ]
    lines.extend(f"- {item}" for item in notes_only)
    lines.extend(["", "Round artifacts:"])
    lines.extend(f"- {row['round']}: {row['actor']}, {row['nodes']} nodes, {row['edges']} edges, {row['matrix']}" for row in round_summaries)
    lines.extend(["", "Token accounting: usage objects were not exposed by the subagent/tool responses, and no API key is available for the Responses input-token counting endpoint. The saved table uses local estimates.", ""])
    (RESULTS / "extraction_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    round_01 = build_high_recall_edges()
    round_02 = build_solid_edges(include_jennifer_additions=True)
    round_03 = build_solid_edges(include_jennifer_additions=True)
    round_04 = build_solid_edges(include_jennifer_additions=True)

    summaries = [
        write_round("round_01_diego_high_recall", "Diego", "High recall: primary solid edges plus notes-only dashed/control/instrument candidates.", round_01),
        write_round("round_02_jennifer_precision", "Jennifer", "Precision solid-only matrix with top grounds and 24 VDC panel drops added.", round_02),
        write_round("round_03_diego_saturation", "Diego", "Saturation check of Jennifer-corrected primary matrix.", round_03),
        write_round("round_04_jennifer_final", "Jennifer", "Final saturated primary matrix.", round_04),
    ]

    final_edges = round_04
    final_nodes = node_order(final_edges)
    write_nodes(RESULTS / "final_nodes.csv", final_nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    validation = validate_matrix(final_nodes, final_edges)
    (RESULTS / "final_graph.json").write_text(
        json.dumps(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "nodes": final_nodes,
                "edges": [edge.__dict__ for edge in final_edges],
                "validation": validation,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["round", "actor", "policy", "nodes", "edges", "matrix"])
        writer.writeheader()
        writer.writerows(summaries)
    token_estimates = token_rows()
    write_token_estimates(token_estimates)
    write_notes(summaries, final_nodes, final_edges)
    print(json.dumps({"final_nodes": len(final_nodes), "final_edges": len(final_edges), "validation": validation}, indent=2))


if __name__ == "__main__":
    main()
