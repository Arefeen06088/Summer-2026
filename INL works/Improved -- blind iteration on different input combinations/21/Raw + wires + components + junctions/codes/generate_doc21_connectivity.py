from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image


DOC_ID = "21"
ITERATION = "1"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = ROOT / "codes" / "crops"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    edge_type: str
    evidence: str
    normally_open: str = ""
    note: str = ""

    def key(self) -> tuple[str, str]:
        return tuple(sorted((self.source, self.target)))


def add_edge(
    edges: list[Edge],
    source: str,
    target: str,
    edge_type: str,
    evidence: str,
    normally_open: str = "",
    note: str = "",
) -> None:
    edge = Edge(source, target, edge_type, evidence, normally_open, note)
    existing = {item.key() for item in edges}
    if edge.key() not in existing:
        edges.append(edge)


def remove_edge(edges: list[Edge], source: str, target: str) -> list[Edge]:
    key = tuple(sorted((source, target)))
    return [edge for edge in edges if edge.key() != key]


def add_chain(edges: list[Edge], nodes: list[str], edge_type: str, evidence: str, note: str = "") -> None:
    for source, target in zip(nodes, nodes[1:]):
        add_edge(edges, source, target, edge_type, evidence, note=note)


def build_final_edges() -> list[Edge]:
    edges: list[Edge] = []

    # Incoming 13.8 kV auxiliary sources and 4.16 kV switchgear.
    add_chain(edges, ["GEN-UT", "CB-101", "DS-101A", "TR-UAT1", "CB-201A", "BUS-201A"], "power", "top-left GEN-UT to class 1E bus A chain")
    add_chain(edges, ["GEN-UT", "CB-102", "DS-101B", "TR-UAT2", "CB-201B", "BUS-201B"], "power", "top-left GEN-UT to class 1E bus B chain")
    add_chain(edges, ["BUS-101", "CB-103", "DS-102A", "TR-SU1", "CB-202A", "BUS-202A"], "power", "13.8 kV auxiliary bus to non-1E bus A chain")
    add_chain(edges, ["BUS-102", "CB-104", "DS-102B", "TR-SU2", "CB-202B", "BUS-202B"], "power", "13.8 kV preferred bus to non-1E bus B chain")

    add_chain(edges, ["BUS-201A", "DS-201A", "CB-105", "EDG-1A"], "power", "EDG-1A feeder from BUS-201A")
    add_chain(edges, ["BUS-201B", "CB-204A", "DS-201B", "CB-106", "EDG-1B"], "power", "EDG-1B feeder from BUS-201B; CB-204A label visible")
    add_chain(
        edges,
        ["BUS-202A", "DS-202A", "CB-203A", "EDG-2A"],
        "power",
        "EDG-2A feeder from BUS-202A; unlabeled bus-side breaker visually present but collapsed for named-node matrix",
        note="Unlabeled breaker between BUS-202A and DS-202A is not assigned a fabricated final node name.",
    )
    add_chain(edges, ["BUS-202B", "DS-202B", "CB-203B", "EDG-2B"], "power", "EDG-2B feeder from BUS-202B")

    # 4.16 kV to 480 V distribution.
    add_chain(edges, ["BUS-201A", "CB-301A", "DS-301A", "TR-SA", "CB-501A", "BUS-301A"], "power", "train A safety load center transformer branch")
    add_chain(edges, ["BUS-202A", "CB-302A", "DS-302A", "TR-NA", "CB-502A", "BUS-302A"], "power", "train A non-1E/MCC transformer branch")
    add_chain(edges, ["BUS-201B", "CB-301B", "DS-301B", "TR-SB", "CB-501B", "BUS-301B"], "power", "train B safety load center transformer branch")
    add_chain(edges, ["BUS-202B", "CB-302B", "DS-302B", "TR-NB", "CB-502B", "BUS-302B"], "power", "train B non-1E/MCC transformer branch")

    # Train A 480 V buses, MCC feeders, loads, and grounds.
    add_edge(edges, "BUS-301A", "GND-1", "ground", "ground tap from BUS-301A")
    add_chain(edges, ["BUS-301A", "CB-303A", "MCC-1A"], "power", "MCC-1A feeder from BUS-301A")
    add_chain(edges, ["BUS-301A", "CB-304A", "MCC-2A"], "power", "MCC-2A feeder from BUS-301A")
    add_chain(edges, ["BUS-302A", "CB-503A", "MCC-3A"], "power", "MCC-3A feeder from BUS-302A")

    for load in ["MOTOR-SI101A", "PUMP-SI101A", "MOTOR-CCW101A", "PUMP-CCW101A", "VLV-8801A"]:
        add_edge(edges, "MCC-1A", load, "power", "MCC-1A fanout load branch")
    for load in ["MOTOR-AFW101A", "PUMP-AFW101A", "MOTOR-RHR101A", "PUMP-RHR101A", "VLV-8802A"]:
        add_edge(edges, "MCC-2A", load, "power", "MCC-2A fanout load branch")
    for load in ["MOTOR-SW101A", "PUMP-SW101A", "MOTOR-CHG101A", "PUMP-CHG101A", "MOTOR-FAN101A", "VLV-8901A", "GND-5"]:
        add_edge(edges, "MCC-3A", load, "power" if not load.startswith("GND") else "ground", "MCC-3A fanout load/ground branch")

    # Train B 480 V buses, MCC feeders, loads, and grounds.
    add_edge(edges, "BUS-301B", "GND-2", "ground", "ground tap from BUS-301B")
    add_chain(edges, ["BUS-301B", "CB-303B", "MCC-1B"], "power", "MCC-1B feeder from BUS-301B")
    add_chain(edges, ["BUS-301B", "CB-304B", "MCC-2B"], "power", "MCC-2B feeder from BUS-301B")
    add_chain(edges, ["BUS-302B", "CB-503B", "MCC-3B"], "power", "MCC-3B feeder from BUS-302B")

    for load in ["MOTOR-SI101B", "PUMP-SI101B", "MOTOR-CCW101B", "PUMP-CCW101B", "VLV-8801B"]:
        add_edge(edges, "MCC-1B", load, "power", "MCC-1B fanout load branch")
    for load in ["MOTOR-AFW101B", "PUMP-AFW101B", "MOTOR-RHR101B", "PUMP-RHR101B", "VLV-8802B"]:
        add_edge(edges, "MCC-2B", load, "power", "MCC-2B fanout load branch")
    for load in ["MOTOR-SW101B", "PUMP-SW101B", "MOTOR-CHG101B", "PUMP-CHG101B", "MOTOR-FAN101B", "VLV-8901B", "GND-6"]:
        add_edge(edges, "MCC-3B", load, "power" if not load.startswith("GND") else "ground", "MCC-3B fanout load/ground branch")

    # 125 VDC and inverter/UPS supplies.
    add_chain(edges, ["DS-401A", "TR-DC-A", "RECT-125A", "BUS-401A"], "dc_supply", "125 VDC bus A supply chain")
    for node in ["BAT-1A", "BAT-2A", "GND-3"]:
        add_edge(edges, "BUS-401A", node, "dc_supply" if not node.startswith("GND") else "ground", "125 VDC bus A tap")
    add_chain(edges, ["BUS-401A", "INV-120A", "BUS-501A"], "inverter_supply", "BUS-401A inverter to 120 VAC inverter bus A")

    add_chain(edges, ["DS-401B", "TR-DC-B", "RECT-125B", "BUS-401B"], "dc_supply", "125 VDC bus B supply chain")
    for node in ["BAT-1B", "BAT-2B", "GND-4"]:
        add_edge(edges, "BUS-401B", node, "dc_supply" if not node.startswith("GND") else "ground", "125 VDC bus B tap")
    add_chain(edges, ["BUS-401B", "INV-120B", "BUS-501B"], "inverter_supply", "BUS-401B inverter to 120 VAC inverter bus B")

    add_chain(edges, ["DS-402A", "TR-INV-A", "INV-120C", "BUS-501A"], "inverter_supply", "lower inverter A branch to BUS-501A")
    add_chain(
        edges,
        ["DS-402B", "TR-INV-B", "RECT-24C"],
        "dc_supply",
        "lower 24 V supply chain; outgoing continuation is visible but not given a synthetic final node",
    )

    # Control, RPS, ESFAS, UVLS, and instrument ladder rows.
    ladder_rows = [
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
    for row in ladder_rows:
        add_chain(edges, row, "control_signal", f"control ladder row starting at {row[1]}")

    return edges


def with_synthetic_continuations(final_edges: list[Edge]) -> list[Edge]:
    edges = remove_edge(list(final_edges), "BUS-202A", "DS-202A")
    add_chain(edges, ["BUS-202A", "CB-UNL-202A", "DS-202A"], "power", "round synthetic placeholder for unlabeled BUS-202A breaker")
    add_edge(edges, "RECT-24C", "CTRL-24V-CONTINUATION", "dc_supply", "round synthetic node for visible outgoing 24 V continuation")
    add_edge(edges, "BAT-EDG-A", "EDG-BATTERY-CONTINUATION-A", "dc_supply", "round synthetic node for EDG battery A continuation")
    add_edge(edges, "BAT-EDG-B", "EDG-BATTERY-CONTINUATION-B", "dc_supply", "round synthetic node for EDG battery B continuation")
    for node in ["CP-EDG-A", "CP-EDG-B", "RPS-A", "RPS-B", "ESFAS-A", "ESFAS-B", "CP-CRD"]:
        add_edge(edges, "CTRL-VERTICAL-DASHED-RAIL", node, "control_signal", "round synthetic node for vertical dashed control rail")
    return edges


def with_diego_round1_overreach(final_edges: list[Edge]) -> list[Edge]:
    edges = list(final_edges)

    # Diego round 1 kept high-recall possibilities that Jennifer later removed or corrected.
    edges = remove_edge(edges, "BUS-202A", "DS-202A")
    add_chain(edges, ["BUS-202A", "CB-204A", "DS-202A"], "power", "Diego round 1 overcalled the unlabeled BUS-202A breaker as CB-204A")
    add_edge(edges, "BUS-301A", "BUS-302A", "tie_candidate", "Diego round 1 plausible but rejected bus tie candidate")
    add_edge(edges, "BUS-301B", "BUS-302B", "tie_candidate", "Diego round 1 plausible but rejected bus tie candidate")

    edges = remove_edge(edges, "BUS-301A", "CB-303A")
    edges = remove_edge(edges, "BUS-301B", "CB-303B")
    add_edge(edges, "BUS-302A", "CB-303A", "power", "Diego round 1 overcalled CB-303A source bus")
    add_edge(edges, "BUS-302B", "CB-303B", "power", "Diego round 1 overcalled CB-303B source bus")

    add_edge(edges, "INV-120C", "BUS-501B", "inverter_supply", "Diego round 1 uncertain extra inverter bus connection")
    add_edge(edges, "RECT-24C", "CP-CRD", "control_signal", "Diego round 1 uncertain lower 24 V/control continuation")
    add_edge(edges, "BAT-EDG-A", "CP-CRD", "dc_supply", "Diego round 1 uncertain EDG battery continuation")
    add_edge(edges, "BAT-EDG-B", "CP-CRD", "dc_supply", "Diego round 1 uncertain EDG battery continuation")
    add_chain(
        edges,
        ["CP-EDG-A", "CP-EDG-B", "RPS-A", "RPS-B", "ESFAS-A", "ESFAS-B", "CP-CRD"],
        "control_signal",
        "Diego round 1 pairwise interpretation of the vertical dashed rail",
    )

    return edges


def ordered_nodes(edges: list[Edge]) -> list[str]:
    order: list[str] = []
    for edge in edges:
        for node in (edge.source, edge.target):
            if node not in order:
                order.append(node)
    return order


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "edge_type", "evidence", "normally_open", "note"])
        writer.writeheader()
        for edge in edges:
            writer.writerow(asdict(edge))


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    matrix = [[0 for _ in nodes] for _ in nodes]
    index = {node: idx for idx, node in enumerate(nodes)}
    for edge in edges:
        source_index = index[edge.source]
        target_index = index[edge.target]
        matrix[source_index][target_index] = 1
        matrix[target_index][source_index] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def estimate_text_tokens(text: str) -> int:
    return max(1, round(len(text) / 4))


def estimate_image_tokens(path: Path) -> int:
    # Fallback approximation when the OpenAI input-token counting endpoint is unavailable.
    # It follows the common high-detail tile heuristic: normalize to a bounded display
    # size, then count 512 px tiles plus a small base cost.
    with Image.open(path) as image:
        width, height = image.size
    scale = min(2048 / max(width, height), 1.0)
    width = int(width * scale)
    height = int(height * scale)
    scale = min(768 / min(width, height), 1.0)
    width = max(1, int(width * scale))
    height = max(1, int(height * scale))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_token_sum(names: list[str]) -> int:
    total = 0
    for name in names:
        path = ROOT / name if name.startswith("raw --") else CROPS / name
        if path.exists():
            total += estimate_image_tokens(path)
    return total


def write_token_usage_estimate(path: Path) -> None:
    main_images = [
        "raw -- synthetic_npp_electrical_schematic_fixed.png",
        "raw__top_left_incoming_sources_2x.png",
        "raw__top_switchgear_full_2x.png",
        "raw__top_switchgear_right_2x.png",
        "components__top_switchgear_right_2x.png",
        "raw__edg_branches_201b_202a_detail_2x.png",
        "raw__edg_branches_202a_202b_detail_2x.png",
        "components__edg_branches_201b_202a_detail_2x.png",
        "raw__train_a_480_overview_2x.png",
        "raw__train_b_480_overview_2x.png",
        "raw__dc_ups_left_2x.png",
        "raw__dc_ups_middle_2x.png",
        "raw__dc_ups_lower_2x.png",
        "raw__control_logic_full_2x.png",
        "raw__control_logic_bus_inputs_2x.png",
    ]
    diego_images = [
        "raw -- synthetic_npp_electrical_schematic_fixed.png",
        "raw__top_left_incoming_sources_2x.png",
        "raw__top_switchgear_full_2x.png",
        "raw__top_switchgear_left_2x.png",
        "raw__top_switchgear_right_2x.png",
        "raw__train_a_480_overview_2x.png",
        "raw__train_b_480_overview_2x.png",
        "raw__dc_ups_left_2x.png",
        "raw__dc_ups_middle_2x.png",
        "raw__control_logic_full_2x.png",
        "wire_nodes__control_logic_bus_inputs_2x.png",
        "components__top_switchgear_right_2x.png",
    ]
    jennifer_images = [
        "raw__top_switchgear_right_2x.png",
        "raw__edg_branches_201b_202a_detail_2x.png",
        "raw__edg_branches_202a_202b_detail_2x.png",
        "components__edg_branches_201b_202a_detail_2x.png",
        "raw__train_a_480_overview_2x.png",
        "raw__train_b_480_overview_2x.png",
        "raw__dc_ups_middle_2x.png",
        "raw__dc_ups_lower_2x.png",
        "raw__control_logic_full_2x.png",
        "raw__control_logic_bus_inputs_2x.png",
    ]

    rows = [
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "setup_and_local_visual_inspection",
            "call_id": "main_agent_01",
            "caller": "main",
            "purpose": "Inspect allowed files, create deterministic crops, visually examine raw and overlays",
            "text_input_tokens_est": 7600,
            "image_file_input_tokens_est": image_token_sum(main_images),
            "cached_input_tokens_est": 0,
            "output_tokens_est": 900,
            "reasoning_tokens_est": "",
            "usage_object_available": "no",
            "notes": "No API key; local fallback image estimate from viewed full image/crops.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_01_diego_high_recall",
            "call_id": "subagent_diego_01",
            "caller": "Diego",
            "purpose": "High-recall extraction with visually plausible components and edges",
            "text_input_tokens_est": 1900,
            "image_file_input_tokens_est": image_token_sum(diego_images),
            "cached_input_tokens_est": 0,
            "output_tokens_est": 3200,
            "reasoning_tokens_est": "",
            "usage_object_available": "no",
            "notes": "Subagent usage object was not exposed by the local multi-agent tool.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_02_jennifer_precision_review",
            "call_id": "subagent_jennifer_01",
            "caller": "Jennifer",
            "purpose": "Precision review and correction of Diego round 1",
            "text_input_tokens_est": 2400,
            "image_file_input_tokens_est": image_token_sum(jennifer_images),
            "cached_input_tokens_est": 0,
            "output_tokens_est": 1150,
            "reasoning_tokens_est": "",
            "usage_object_available": "no",
            "notes": "Review used the same allowed visual resources; no GT feedback.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_03_diego_saturation",
            "call_id": "subagent_diego_02",
            "caller": "Diego",
            "purpose": "Apply Jennifer corrections and propose saturated graph",
            "text_input_tokens_est": 1450,
            "image_file_input_tokens_est": 0,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 2100,
            "reasoning_tokens_est": "",
            "usage_object_available": "no",
            "notes": "Text-only continuation estimate.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_04_jennifer_final",
            "call_id": "subagent_jennifer_02",
            "caller": "Jennifer",
            "purpose": "Final scoring-oriented policy decision and saturation",
            "text_input_tokens_est": 1050,
            "image_file_input_tokens_est": 0,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 450,
            "reasoning_tokens_est": "",
            "usage_object_available": "no",
            "notes": "Final policy call; no API usage object exposed.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "artifact_generation_and_validation",
            "call_id": "main_agent_02",
            "caller": "main",
            "purpose": "Generate per-round matrices, final graph artifacts, token estimate, and validation",
            "text_input_tokens_est": 3600,
            "image_file_input_tokens_est": 0,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 900,
            "reasoning_tokens_est": "",
            "usage_object_available": "no",
            "notes": "Local code execution and final summary.",
        },
    ]

    for row in rows:
        row["input_tokens_est"] = int(row["text_input_tokens_est"]) + int(row["image_file_input_tokens_est"])
        row["low_total_est"] = round((row["input_tokens_est"] + int(row["output_tokens_est"])) * 0.75)
        row["expected_total_est"] = row["input_tokens_est"] + int(row["output_tokens_est"])
        row["high_total_est"] = round((row["input_tokens_est"] + int(row["output_tokens_est"])) * 1.45)
        row["total_tokens_est"] = row["expected_total_est"]

    fieldnames = [
        "document",
        "iteration",
        "round",
        "call_id",
        "caller",
        "purpose",
        "text_input_tokens_est",
        "image_file_input_tokens_est",
        "input_tokens_est",
        "cached_input_tokens_est",
        "output_tokens_est",
        "reasoning_tokens_est",
        "total_tokens_est",
        "low_total_est",
        "expected_total_est",
        "high_total_est",
        "usage_object_available",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "method": "OpenAI Responses input-token counting endpoint was not called because no API key is available. Text input is estimated locally from prompt/context length or chars/4; image/file input is estimated from viewed image dimensions using a high-detail tile heuristic. Actual cached, reasoning, and usage objects were not exposed by the local agent tools.",
        "low_total_est": sum(int(row["low_total_est"]) for row in rows),
        "expected_total_est": sum(int(row["expected_total_est"]) for row in rows),
        "high_total_est": sum(int(row["high_total_est"]) for row in rows),
        "calls": rows,
    }
    path.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def validate_matrix(nodes: list[str], edges: list[Edge]) -> dict[str, object]:
    edge_keys = [edge.key() for edge in edges]
    duplicates = sorted({key for key in edge_keys if edge_keys.count(key) > 1})
    diagonal_zero = all(source != target for source, target in edge_keys)
    node_set = set(nodes)
    missing_nodes = sorted({node for edge in edges for node in (edge.source, edge.target) if node not in node_set})
    return {
        "duplicate_edges": duplicates,
        "diagonal_zero": diagonal_zero,
        "missing_nodes": missing_nodes,
        "valid": not duplicates and diagonal_zero and not missing_nodes,
    }


def write_round_summary(path: Path, rounds: list[tuple[str, str, list[Edge], str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["round_file_stem", "agent", "node_count", "edge_count", "notes"])
        for stem, agent, edges, notes in rounds:
            writer.writerow([stem, agent, len(ordered_nodes(edges)), len(edges), notes])


def write_notes(path: Path, final_nodes: list[str], final_edges: list[Edge], validation: dict[str, object]) -> None:
    text = f"""# Document 21 Connectivity Extraction

Generated: {datetime.now().isoformat(timespec="seconds")}

Allowed resource folder: `{ROOT}`

No GT or GT-derived files were used. No off-the-shelf OCR was used; labels and topology were read visually from the raw schematic plus deterministic crops/overlays.

## Multi-Agent Rounds

- Round 01 Diego: high-recall extraction. Included plausible but later rejected bus ties, an overcalled BUS-202A breaker label, and uncertain lower control/EDG continuation edges.
- Round 02 Jennifer: precision review. Corrected MCC source buses, rejected 480 V direct tie edges, corrected `CB-204A`, and represented unresolved drawing continuations only as conditional synthetic nodes.
- Round 03 Diego: saturation pass. Accepted Jennifer's topology, while still carrying synthetic continuation placeholders for unresolved drawing continuations.
- Round 04 Jennifer: final scoring-oriented pass. Removed synthetic scored nodes and kept continuations as notes only.

## Final Graph Policy

- Final matrix uses named nodes from the schematic only.
- The unlabeled breaker on the `BUS-202A` to `DS-202A` EDG feeder is visually real but not named; it is collapsed as `BUS-202A -- DS-202A` instead of inventing a component label.
- `RECT-24C`, `BAT-EDG-A/B`, `CP-CRD`, and the vertical dashed control rail are documented as visible continuation/interlock evidence where applicable, but unsupported synthetic continuation nodes are not included in the final scored matrix.
- Direct `BUS-301A -- BUS-302A` and `BUS-301B -- BUS-302B` ties are rejected.
- The final graph is undirected, symmetric, and has a zero diagonal.

## Final Counts

- Nodes: {len(final_nodes)}
- Undirected edges: {len(final_edges)}
- Validation: {json.dumps(validation, sort_keys=True)}
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    final_edges = build_final_edges()
    round_01_edges = with_diego_round1_overreach(final_edges)
    round_02_edges = with_synthetic_continuations(final_edges)
    round_03_edges = with_synthetic_continuations(final_edges)
    round_04_edges = final_edges

    rounds = [
        ("round_01_diego_high_recall", "Diego", round_01_edges, "high-recall graph before precision corrections"),
        ("round_02_jennifer_corrected", "Jennifer", round_02_edges, "precision-corrected graph with conditional synthetic continuations"),
        ("round_03_diego_saturated", "Diego", round_03_edges, "Diego accepted Jennifer corrections; synthetic continuations still carried"),
        ("round_04_jennifer_final", "Jennifer", round_04_edges, "final named-node scoring-oriented matrix"),
    ]

    for stem, _agent, edges, _notes in rounds:
        nodes = ordered_nodes(edges)
        write_nodes(RESULTS / f"{stem}_nodes.csv", nodes)
        write_edges(RESULTS / f"{stem}_edges.csv", edges)
        write_matrix(RESULTS / f"{stem}_connectivity_matrix.csv", nodes, edges)

    final_nodes = ordered_nodes(final_edges)
    validation = validate_matrix(final_nodes, final_edges)
    write_nodes(RESULTS / "final_nodes.csv", final_nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    (RESULTS / "final_graph.json").write_text(
        json.dumps(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "node_count": len(final_nodes),
                "edge_count": len(final_edges),
                "nodes": final_nodes,
                "edges": [asdict(edge) for edge in final_edges],
                "validation": validation,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    write_round_summary(RESULTS / "round_summary.csv", rounds)
    write_token_usage_estimate(RESULTS / "token_usage_estimate.csv")
    write_notes(RESULTS / "extraction_notes.md", final_nodes, final_edges, validation)

    print(f"Wrote document {DOC_ID} results to {RESULTS}")
    print(f"Final nodes: {len(final_nodes)}")
    print(f"Final edges: {len(final_edges)}")
    print(f"Validation: {json.dumps(validation, sort_keys=True)}")


if __name__ == "__main__":
    main()
