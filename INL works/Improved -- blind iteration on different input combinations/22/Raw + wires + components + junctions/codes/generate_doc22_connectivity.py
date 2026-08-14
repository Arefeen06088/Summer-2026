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

DOC_ID = "22"
ITERATION = "1"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    edge_type: str
    evidence: str


def add_edge(edges: list[Edge], seen: set[tuple[str, str]], a: str, b: str, edge_type: str, evidence: str) -> None:
    key = tuple(sorted((a, b)))
    if a == b or key in seen:
        return
    seen.add(key)
    edges.append(Edge(a, b, edge_type, evidence))


def add_chain(edges: list[Edge], seen: set[tuple[str, str]], nodes: list[str], edge_type: str, evidence: str) -> None:
    for a, b in zip(nodes, nodes[1:]):
        add_edge(edges, seen, a, b, edge_type, evidence)


def build_solid_edges(final_source: bool, include_ups_supply_panels: bool) -> list[Edge]:
    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()

    if final_source:
        add_chain(edges, seen, ["GEN-G01", "GSU-T01", "SWYD-345"], "power", "Solid upper source conductor.")
        add_chain(edges, seen, ["SWYD-345", "CB-13A1", "BUS-13A"], "power", "Solid feeder from switchyard/source line to 13.8 kV bus A.")
        add_chain(edges, seen, ["SWYD-345", "CB-13B1", "BUS-13B"], "power", "Solid feeder from switchyard/source line to 13.8 kV bus B.")
    else:
        add_chain(edges, seen, ["GEN-G01", "GSU-T01", "N_SRC_345", "SWYD-345"], "power", "Diego round-1 synthetic source junction.")
        add_chain(edges, seen, ["N_SRC_345", "CB-13A1", "BUS-13A"], "power", "Diego round-1 source-to-bus-A branch.")
        add_chain(edges, seen, ["N_SRC_345", "CB-13B1", "BUS-13B"], "power", "Diego round-1 source-to-bus-B branch.")

    add_chain(edges, seen, ["BUS-13A", "CB-13T", "BUS-13B"], "power", "Solid 13.8 kV bus tie.")
    add_chain(edges, seen, ["BUS-13A", "AUX-XFMR-1A", "CB-4A-IN", "BUS-4160-A"], "power", "Solid auxiliary transformer feed to 4160 V bus A.")
    add_chain(edges, seen, ["BUS-13A", "AUX-XFMR-1B", "CB-4B-IN", "BUS-4160-B"], "power", "Solid auxiliary transformer feed to 4160 V bus B.")
    add_chain(edges, seen, ["BUS-13B", "SAT-XFMR-1C", "CB-4C-IN", "BUS-4160-C"], "power", "Solid startup transformer feed to 4160 V bus C.")
    add_chain(edges, seen, ["BUS-13B", "SAT-XFMR-1D", "CB-4D-IN", "BUS-4160-D"], "power", "Solid startup transformer feed to 4160 V bus D.")

    for train in "ABCD":
        add_chain(edges, seen, [f"DG-1{train}", f"CB-DG-{train}", f"BUS-4160-{train}"], "power", "Solid diesel generator feeder.")

    add_chain(edges, seen, ["BUS-4160-A", "CB-4AB-TIE", "BUS-4160-B"], "power", "Solid 4160 V A/B tie.")
    add_chain(edges, seen, ["BUS-4160-C", "CB-4CD-TIE", "BUS-4160-D"], "power", "Solid 4160 V C/D tie.")

    for train in "ABCD":
        add_chain(edges, seen, [f"BUS-4160-{train}", f"CB-LC-{train}", f"TR-LC-{train}", f"BUS-480-{train}"], "power", "Solid load-center transformer chain.")

    for train in "ABCD":
        left_mcc = f"MCC-{train}A"
        right_mcc = f"MCC-{train}B"
        add_chain(edges, seen, [f"BUS-480-{train}", f"CB-MCC-{train}A", left_mcc], "power", "Solid 480 V load-center feeder to left MCC.")
        add_chain(edges, seen, [f"BUS-480-{train}", f"CB-MCC-{train}B", right_mcc], "power", "Solid 480 V load-center feeder to right MCC.")
        add_chain(edges, seen, [f"BUS-480-{train}", f"XFMR-120-{train}", f"PNL-120-{train}"], "power", "Solid 120 V panel transformer tap.")
        add_edge(edges, seen, f"BUS-480-{train}", f"GND-{train}", "ground", "Solid ground branch from 480 V bus.")

        left_loads = [
            ("CB-RHR", "PUMP-RHR"),
            ("CB-SI", "PUMP-SI"),
            ("CB-CCW", "PUMP-CCW"),
            ("CB-FAN", "FAN-CR"),
        ]
        right_loads = [
            ("CB-CH", "CHILLER"),
            ("CB-VLV1", "MOV-HV1"),
            ("CB-VLV2", "MOV-HV2"),
            ("CB-SPARE", "SPARE-LOAD"),
        ]
        for breaker_prefix, load_prefix in left_loads:
            add_chain(edges, seen, [left_mcc, f"{breaker_prefix}-{train}", f"{load_prefix}-{train}"], "power", "Solid MCC branch feeder.")
        for breaker_prefix, load_prefix in right_loads:
            add_chain(edges, seen, [right_mcc, f"{breaker_prefix}-{train}", f"{load_prefix}-{train}"], "power", "Solid MCC branch feeder.")

    add_chain(edges, seen, ["BUS-480-A", "CB-DC-A1", "CHGR-125A", "BUS-125A"], "dc", "Solid feeder to 125 VDC charger A and bus.")
    add_chain(edges, seen, ["BUS-480-B", "CB-DC-B1", "CHGR-125B", "BUS-125B"], "dc", "Solid feeder to 125 VDC charger B and bus.")
    add_edge(edges, seen, "BUS-125A", "BAT-125A", "dc", "Solid battery connection to DC bus A.")
    add_edge(edges, seen, "BUS-125B", "BAT-125B", "dc", "Solid battery connection to DC bus B.")
    add_edge(edges, seen, "BUS-125A", "DC-MCC-A", "dc", "Solid DC MCC A feeder.")
    add_edge(edges, seen, "BUS-125B", "DC-MCC-B", "dc", "Solid DC MCC B feeder.")
    add_chain(edges, seen, ["BUS-125A", "FUSE-FD-A", "INV-UPS-A", "BUS-UPS-A"], "dc/ups", "Solid DC-to-UPS A chain.")
    add_chain(edges, seen, ["BUS-125B", "FUSE-FD-B", "INV-UPS-B", "BUS-UPS-B"], "dc/ups", "Solid DC-to-UPS B chain.")
    add_edge(edges, seen, "BUS-125A", "INST-RACK-A", "dc", "Solid DC bus A instrument rack feed.")
    add_edge(edges, seen, "BUS-125B", "INST-RACK-B", "dc", "Solid DC bus B instrument rack feed.")
    add_edge(edges, seen, "BUS-125A", "GRD-DC-A", "ground", "Solid DC bus A ground branch.")
    add_edge(edges, seen, "BUS-125B", "GRD-DC-B", "ground", "Solid DC bus B ground branch.")

    if include_ups_supply_panels:
        add_edge(edges, seen, "BUS-UPS-A", "PNL-RPS-A", "ups", "Solid vertical UPS bus A supply drop accepted in final round.")
        add_edge(edges, seen, "BUS-UPS-A", "PLC-SAF-A", "ups", "Solid vertical UPS bus A supply drop accepted in final round.")
        add_edge(edges, seen, "BUS-UPS-B", "PNL-RPS-B", "ups", "Solid vertical UPS bus B supply drop accepted in final round.")
        add_edge(edges, seen, "BUS-UPS-B", "PLC-SAF-B", "ups", "Solid vertical UPS bus B supply drop accepted in final round.")

    return edges


def build_high_recall_edges() -> list[Edge]:
    edges = build_solid_edges(final_source=False, include_ups_supply_panels=True)
    seen = {tuple(sorted((edge.source, edge.target))) for edge in edges}

    add_chain(edges, seen, ["BUS-13A", "RELAY-87U", "BUS-13B"], "control_candidate", "Diego round-1 high-recall control/instrument candidate near upper bus.")
    add_chain(edges, seen, ["RELAY-87U", "C-031", "W-011"], "control_candidate", "Diego round-1 dashed/callout candidate.")
    add_edge(edges, seen, "SYNC-PNL-1", "CB-DG-A", "control_candidate", "Diego round-1 synchronizing-panel control candidate.")
    add_edge(edges, seen, "SYNC-PNL-1", "BUS-4160-A", "control_candidate", "Diego round-1 synchronizing-panel candidate.")

    for train in "ABCD":
        add_edge(edges, seen, f"BUS-480-{train}", f"INST-PT-{train}", "instrument_candidate", "Diego round-1 PT candidate.")
        add_edge(edges, seen, f"MCC-{train}A", f"INST-CT-{train}", "instrument_candidate", "Diego round-1 CT candidate on MCC/RHR branch.")
        add_edge(edges, seen, f"INST-CT-{train}", f"CB-RHR-{train}", "instrument_candidate", "Diego round-1 CT candidate on MCC/RHR branch.")
        add_chain(edges, seen, [f"PNL-120-{train}", f"RELAY-K{train}1", f"JB-{train}1", f"TERM-{train}"], "control_candidate", "Diego round-1 dashed lower-control candidate.")
        add_edge(edges, seen, f"PNL-120-{train}", f"RELAY-K{train}2", "control_candidate", "Diego round-1 dashed lower-control candidate.")

    add_edge(edges, seen, "BUS-125A", "SOL-SDV-A", "control_candidate", "Diego round-1 solenoid candidate.")
    add_edge(edges, seen, "DC-MCC-A", "SOL-SDV-A", "control_candidate", "Diego round-1 solenoid candidate.")
    add_edge(edges, seen, "BUS-125B", "SOL-SDV-B", "control_candidate", "Diego round-1 solenoid candidate.")
    add_edge(edges, seen, "DC-MCC-B", "SOL-SDV-B", "control_candidate", "Diego round-1 solenoid candidate.")
    add_edge(edges, seen, "BUS-125A", "DIODE-OR-A", "instrument_candidate", "Diego round-1 diode candidate.")
    add_edge(edges, seen, "BUS-125B", "DIODE-OR-B", "instrument_candidate", "Diego round-1 diode candidate.")
    add_edge(edges, seen, "BUS-125A", "XFMR-PT-1", "instrument_candidate", "Diego round-1 metering/PT candidate.")
    add_edge(edges, seen, "BUS-125B", "XFMR-PT-1", "instrument_candidate", "Diego round-1 metering/PT candidate.")
    add_edge(edges, seen, "XFMR-PT-1", "METER-V01", "instrument_candidate", "Diego round-1 meter candidate.")
    add_edge(edges, seen, "XFMR-PT-1", "METER-A01", "instrument_candidate", "Diego round-1 meter candidate.")

    add_edge(edges, seen, "BUS-UPS-A", "ANN-PNL-CR", "control_candidate", "Diego round-1 UPS/control candidate.")
    add_edge(edges, seen, "BUS-UPS-B", "REC-SEQ-1", "control_candidate", "Diego round-1 UPS/control candidate.")
    add_edge(edges, seen, "PNL-RPS-A", "RELAY-RPS-A1", "control_candidate", "Diego round-1 downstream relay candidate.")
    add_edge(edges, seen, "PNL-RPS-A", "RELAY-ESF-A", "control_candidate", "Diego round-1 downstream relay candidate.")
    add_edge(edges, seen, "PNL-RPS-B", "RELAY-RPS-B1", "control_candidate", "Diego round-1 downstream relay candidate.")
    add_edge(edges, seen, "PNL-RPS-B", "RELAY-ESF-B", "control_candidate", "Diego round-1 downstream relay candidate.")
    add_edge(edges, seen, "PLC-SAF-A", "ANN-PNL-CR", "control_candidate", "Diego round-1 annunciator/PLC candidate.")
    add_edge(edges, seen, "PNL-RPS-A", "JB-CR-01", "control_candidate", "Diego round-1 control junction candidate.")
    add_edge(edges, seen, "ANN-PNL-CR", "JB-CR-01", "control_candidate", "Diego round-1 control junction candidate.")
    add_edge(edges, seen, "REC-SEQ-1", "JB-CR-01", "control_candidate", "Diego round-1 control junction candidate.")
    add_edge(edges, seen, "JB-CR-01", "TERM-MTB-A", "control_candidate", "Diego round-1 terminal candidate.")
    add_edge(edges, seen, "JB-CR-01", "TERM-MTB-B", "control_candidate", "Diego round-1 terminal candidate.")
    add_edge(edges, seen, "PNL-RPS-B", "PLC-SAF-B", "control_candidate", "Diego round-1 right UPS/control candidate.")
    add_edge(edges, seen, "PNL-RPS-B", "REC-SEQ-1", "control_candidate", "Diego round-1 right UPS/control candidate.")

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
            writer.writerow([node] + [adjacency[node][other] if other != node else 0 for other in nodes])


def estimate_text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def estimate_file_tokens(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 0
    return estimate_text_tokens(text)


def estimate_image_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        from PIL import Image

        with Image.open(path) as image:
            width, height = image.size
    except Exception:
        return 0

    # Local approximation of high-detail vision accounting: resize into a
    # 2048 square, then scale the shortest side to at most 768, then count
    # 512-pixel tiles. The actual Responses token counter should be used
    # when an API key is available.
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


def sum_image_tokens(paths: list[Path]) -> int:
    return sum(estimate_image_tokens(path) for path in paths)


def token_rows() -> list[dict[str, object]]:
    raw = BASE / "raw -- synthetic_npp_electrical_schematic_clean.png"
    components = BASE / "detected_components_overlay.png"
    wires = BASE / "wires_mask_overlay.png"
    nodes_overlay = BASE / "wire_nodes_overlay.png"
    wire_nodes = BASE / "wire_nodes.csv"

    top_and_train_crops = [
        CROPS / "raw__top_source_and_aux_buses_2x.png",
        CROPS / "raw__train_a_full_2x.png",
        CROPS / "raw__train_b_full_2x.png",
        CROPS / "raw__train_c_full_2x.png",
        CROPS / "raw__train_d_full_2x.png",
        CROPS / "raw__dc_ups_full_2x.png",
        CROPS / "wire_nodes__top_source_and_aux_buses_2x.png",
        CROPS / "wire_nodes__dc_ups_full_2x.png",
    ]
    precision_crops = [
        CROPS / "raw__top_source_and_aux_buses_2x.png",
        CROPS / "raw__train_a_loads_detail_2x.png",
        CROPS / "raw__dc_ups_full_2x.png",
        CROPS / "components__dc_ups_full_2x.png",
        CROPS / "wire_nodes__dc_ups_full_2x.png",
    ]
    ups_crops = [
        CROPS / "raw__dc_ups_full_2x.png",
        CROPS / "raw__dc_ups_left_2x.png",
        CROPS / "raw__dc_ups_right_2x.png",
    ]

    rows = [
        {
            "call_id": "main_01_resource_inventory_crop_generation",
            "actor": "main",
            "round": "setup",
            "input_text": "Document 22 task prompt, workflow instructions, no-GT constraint, local file inventory, crop script planning.",
            "text_tokens_override": 3200,
            "image_paths": [raw, components, wires, nodes_overlay],
            "file_tokens": estimate_file_tokens(wire_nodes),
            "output_expected": 650,
            "reasoning_expected": 1800,
            "notes": "No OpenAI token-count endpoint call; no API key in environment.",
        },
        {
            "call_id": "subagent_diego_01_high_recall",
            "actor": "Diego",
            "round": "round_01",
            "input_text": "High-recall extractor instructions plus allowed resource paths and key crop names.",
            "text_tokens_override": 1900,
            "image_paths": top_and_train_crops,
            "file_tokens": estimate_file_tokens(wire_nodes),
            "output_expected": 1450,
            "reasoning_expected": 2600,
            "notes": "High-recall visual extraction; usage object unavailable from subagent response.",
        },
        {
            "call_id": "subagent_jennifer_01_precision",
            "actor": "Jennifer",
            "round": "round_02",
            "input_text": "Diego proposal, precision-review instructions, and focused topology questions.",
            "text_tokens_override": 2600,
            "image_paths": precision_crops,
            "file_tokens": 0,
            "output_expected": 1050,
            "reasoning_expected": 2200,
            "notes": "Precision review; usage object unavailable from subagent response.",
        },
        {
            "call_id": "subagent_diego_02_saturation",
            "actor": "Diego",
            "round": "round_03",
            "input_text": "Jennifer corrected matrix and request to find any missing solid conductor edges.",
            "text_tokens_override": 1150,
            "image_paths": ups_crops,
            "file_tokens": 0,
            "output_expected": 220,
            "reasoning_expected": 900,
            "notes": "Returned four UPS panel/PLC feeder additions.",
        },
        {
            "call_id": "subagent_jennifer_02_final",
            "actor": "Jennifer",
            "round": "round_04",
            "input_text": "Diego saturation objection and final accept/reject request for four UPS supply feeders.",
            "text_tokens_override": 700,
            "image_paths": ups_crops,
            "file_tokens": 0,
            "output_expected": 170,
            "reasoning_expected": 700,
            "notes": "Accepted four UPS solid supply drops.",
        },
        {
            "call_id": "main_02_artifact_generation_validation",
            "actor": "main",
            "round": "final_artifacts",
            "input_text": "Final saturated edge set, artifact generator implementation, validation, and final summary.",
            "text_tokens_override": 4200,
            "image_paths": [],
            "file_tokens": 0,
            "output_expected": 550,
            "reasoning_expected": 1400,
            "notes": "Local deterministic CSV/JSON generation and matrix validation.",
        },
    ]

    output: list[dict[str, object]] = []
    for row in rows:
        text_tokens = int(row.get("text_tokens_override") or estimate_text_tokens(str(row["input_text"])))
        image_tokens = sum_image_tokens(row["image_paths"])  # type: ignore[arg-type]
        file_tokens = int(row["file_tokens"])
        input_expected = text_tokens + image_tokens + file_tokens
        output_expected = int(row["output_expected"])
        reasoning_expected = int(row["reasoning_expected"])
        total_expected = input_expected + output_expected + reasoning_expected
        output.append(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "call_id": row["call_id"],
                "actor": row["actor"],
                "round": row["round"],
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
                "notes": row["notes"],
            }
        )
    return output


def write_token_estimates(rows: list[dict[str, object]]) -> None:
    csv_path = RESULTS / "token_usage_estimate.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
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
        "method": "Local text tokenizer when available, otherwise chars/4; local high-detail image tile heuristic; exact Responses count endpoint unavailable without API key.",
    }
    with (RESULTS / "token_usage_estimate.json").open("w", encoding="utf-8") as handle:
        json.dump({"calls": rows, "total": total}, handle, indent=2)


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
    symmetric = all(adjacency[a][b] == adjacency[b][a] for a in nodes for b in nodes)
    diagonal_zero = all(adjacency[node][node] == 0 for node in nodes)
    return {"symmetric": symmetric, "diagonal_zero": diagonal_zero}


def write_notes(round_summaries: list[dict[str, object]], final_nodes: list[str], final_edges: list[Edge]) -> None:
    notes_only = [
        "RELAY-87U, C-031, W-011, SYNC-PNL-1",
        "INST-PT-A/B/C/D and INST-CT-A/B/C/D",
        "RELAY-K* lower-control relays, JB-* junction boxes, TERM-* terminals",
        "SOL-SDV-A/B, DIODE-OR-A/B, XFMR-PT-1, METER-V01, METER-A01",
        "ANN-PNL-CR, REC-SEQ-1, JB-CR-01, TERM-MTB-A/B, downstream UPS relays",
    ]
    lines = [
        "# Document 22 Connectivity Extraction",
        "",
        "Scope: one blind iteration using only the `Raw + wires + components + junctions` folder. No GT or GT-derived feedback was used.",
        "",
        "Visual method: native visual inspection of the raw diagram and derived overlays/crops. No off-the-shelf OCR engine was used.",
        "",
        "Final policy: primary matrix contains visually supported solid power/DC/UPS supply conductors. Dashed control and dotted/instrument relationships are retained as notes only.",
        "",
        f"Final node count: {len(final_nodes)}",
        f"Final edge count: {len(final_edges)}",
        "",
        "Final saturation detail: Diego identified four solid UPS feeder drops that Jennifer accepted in the last round:",
        "- BUS-UPS-A -- PNL-RPS-A",
        "- BUS-UPS-A -- PLC-SAF-A",
        "- BUS-UPS-B -- PNL-RPS-B",
        "- BUS-UPS-B -- PLC-SAF-B",
        "",
        "Notes-only visual candidates removed from the primary matrix:",
    ]
    lines.extend(f"- {item}" for item in notes_only)
    lines.extend(["", "Round artifacts:"])
    lines.extend(f"- {row['round']}: {row['actor']}, {row['nodes']} nodes, {row['edges']} edges, {row['matrix']}" for row in round_summaries)
    lines.extend(
        [
            "",
            "Token accounting note: the OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Estimates use a local tokenizer when installed, a chars/4 fallback for text, and a high-detail image tile heuristic for image inputs.",
            "",
        ]
    )
    (RESULTS / "extraction_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    round_01 = build_high_recall_edges()
    round_02 = build_solid_edges(final_source=True, include_ups_supply_panels=False)
    round_03 = build_solid_edges(final_source=True, include_ups_supply_panels=True)
    round_04 = build_solid_edges(final_source=True, include_ups_supply_panels=True)

    round_summaries = [
        write_round("round_01_diego_high_recall", "Diego", "High recall, includes plausible control/instrument candidates and synthetic source junction.", round_01),
        write_round("round_02_jennifer_precision", "Jennifer", "Solid power/DC only, before final UPS-panel feeder correction.", round_02),
        write_round("round_03_diego_saturation", "Diego", "Jennifer solid matrix plus four visually solid UPS feeder additions.", round_03),
        write_round("round_04_jennifer_final", "Jennifer", "Final saturated solid power/DC/UPS supply matrix.", round_04),
    ]

    final_edges = round_04
    final_nodes = node_order(final_edges)
    write_nodes(RESULTS / "final_nodes.csv", final_nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    validation = validate_matrix(final_nodes, final_edges)

    with (RESULTS / "final_graph.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "nodes": final_nodes,
                "edges": [edge.__dict__ for edge in final_edges],
                "validation": validation,
            },
            handle,
            indent=2,
        )

    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["round", "actor", "policy", "nodes", "edges", "matrix"])
        writer.writeheader()
        writer.writerows(round_summaries)

    token_estimates = token_rows()
    write_token_estimates(token_estimates)
    write_notes(round_summaries, final_nodes, final_edges)

    print(json.dumps({"final_nodes": len(final_nodes), "final_edges": len(final_edges), "validation": validation}, indent=2))


if __name__ == "__main__":
    main()
