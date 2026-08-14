from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = BASE / "codes" / "crops"
RESULTS.mkdir(parents=True, exist_ok=True)


def add_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def edge(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"Self edge is not expected: {a}")
    return (a, b)


def normalize_edge(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def train_4kv_nodes(x: str) -> list[str]:
    return [
        *(f"CB-4{x}{i:02d}" for i in range(1, 9)),
        *(f"DS-4{x}{i:02d}" for i in range(1, 9)),
        f"TR-480-1{x}",
        f"CB-52-48{x}",
        f"BUS-480-1{x}",
        f"MS-{x}01",
        f"MS-{x}02",
        f"TR-LC-{x}03",
        f"MS-{x}04",
        f"PNL-ESF-{x}05",
        f"RECT-RPS-{x}06",
        f"MS-{x}07",
        f"TR-CTRL-{x}08",
        f"PUMP-RHR P201{x}",
        f"PUMP-CS-P202{x}",
        f"LC-480-{x}03",
        f"FAN-CR-401{x}",
        f"GND-ESF-{x}05",
        f"INV-RPS-{x}06",
        f"PUMP-AFW P203{x}",
        f"CP-CTRL-{x}08",
    ]


def train_mcc_nodes(x: str) -> list[str]:
    return [
        f"MCC-{x}1",
        f"MCC-{x}2",
        *(f"CB-48{x}{i:02d}" for i in range(1, 7)),
        f"MS-48{x}01",
        f"K-48{x}02",
        f"MS-48{x}03",
        f"MS-48{x}04",
        f"K-48{x}05",
        f"XFU-48{x}06",
        f"PUMP-CVC P301{x}",
        f"MOV-CS-451{x}",
        f"FAN-HVAC-501{x}",
        f"PUMP-SUMP P302{x}",
        f"MOV-RHR-452{x}",
        f"PNL-PI-601{x}",
    ]


def train_4kv_edges(x: str, round1: bool = False) -> list[tuple[str, str]]:
    bus = f"BUS-4160-{x}"
    edges: list[tuple[str, str]] = []
    downstream = {
        "02": (f"MS-{x}02", f"PUMP-CS-P202{x}"),
        "03": (f"TR-LC-{x}03", f"LC-480-{x}03"),
        "04": (f"MS-{x}04", f"FAN-CR-401{x}"),
        "05": (f"PNL-ESF-{x}05", f"GND-ESF-{x}05"),
        "06": (f"RECT-RPS-{x}06", f"INV-RPS-{x}06"),
        "07": (f"MS-{x}07", f"PUMP-AFW P203{x}"),
        "08": (f"TR-CTRL-{x}08", f"CP-CTRL-{x}08"),
    }

    edges.extend(
        [
            edge(bus, f"CB-4{x}01"),
            edge(f"CB-4{x}01", f"DS-4{x}01"),
            edge(f"DS-4{x}01", f"TR-480-1{x}"),
            edge(f"TR-480-1{x}", f"CB-52-48{x}"),
            edge(f"CB-52-48{x}", f"BUS-480-1{x}"),
            edge(f"MS-{x}01", f"PUMP-RHR P201{x}"),
        ]
    )
    if round1:
        edges.append(edge(f"CB-4{x}01", f"MS-{x}01"))
    else:
        edges.append(edge(f"DS-4{x}01", f"MS-{x}01"))

    for suffix, (device, load) in downstream.items():
        edges.extend(
            [
                edge(bus, f"CB-4{x}{suffix}"),
                edge(f"CB-4{x}{suffix}", f"DS-4{x}{suffix}"),
                edge(f"DS-4{x}{suffix}", device),
                edge(device, load),
            ]
        )
    return edges


def train_mcc_edges(x: str, include_charger_feeder: bool = True) -> list[tuple[str, str]]:
    edges = [
        edge(f"BUS-480-1{x}", f"MCC-{x}1"),
        edge(f"BUS-480-1{x}", f"MCC-{x}2"),
        edge(f"MCC-{x}1", f"CB-48{x}01"),
        edge(f"CB-48{x}01", f"MS-48{x}01"),
        edge(f"MS-48{x}01", f"PUMP-CVC P301{x}"),
        edge(f"MCC-{x}1", f"CB-48{x}02"),
        edge(f"CB-48{x}02", f"K-48{x}02"),
        edge(f"K-48{x}02", f"MOV-CS-451{x}"),
        edge(f"MCC-{x}1", f"CB-48{x}03"),
        edge(f"CB-48{x}03", f"MS-48{x}03"),
        edge(f"MS-48{x}03", f"FAN-HVAC-501{x}"),
        edge(f"MCC-{x}2", f"CB-48{x}04"),
        edge(f"CB-48{x}04", f"MS-48{x}04"),
        edge(f"MS-48{x}04", f"PUMP-SUMP P302{x}"),
        edge(f"MCC-{x}2", f"CB-48{x}05"),
        edge(f"CB-48{x}05", f"K-48{x}05"),
        edge(f"K-48{x}05", f"MOV-RHR-452{x}"),
        edge(f"MCC-{x}2", f"CB-48{x}06"),
        edge(f"CB-48{x}06", f"XFU-48{x}06"),
        edge(f"XFU-48{x}06", f"PNL-PI-601{x}"),
    ]
    if include_charger_feeder and x in {"A", "B"}:
        edges.append(edge(f"MCC-{x}2", f"480V CHGR-{x} FEEDER"))
    return edges


CORE_NODES = [
    "SWYD-115KV",
    "FDR-13A",
    "TR-UAT-1A",
    "CB-52-4A",
    "EDG-1A",
    "CB-DG-1A",
    "BUS-4160-A",
    "FDR-13B",
    "TR-UAT-1B",
    "CB-52-4B",
    "EDG-1B",
    "CB-DG-1B",
    "BUS-4160-B",
    "TR-SAT-1",
    "CB-52-4C",
    "EDG-1C",
    "CB-DG-1C",
    "BUS-4160-C",
    "CB-TIE-AB",
    "CB-TIE-BC",
]

LOWER_NODES = [
    "480V CHGR-A FEEDER",
    "CHGR-125-1A",
    "BAT-125-1A",
    "BUS-125DC-A",
    "INV-120-1A",
    "PNL-RPS-A",
    "XMTR-PT-501A",
    "RELAY-K501A",
    "PNL A/B TIE",
    "480V CHGR-B FEEDER",
    "CHGR-125-1B",
    "BAT-125-1B",
    "BUS-125DC-B",
    "INV-120-1B",
    "PNL-RPS-B",
    "XMTR-PT-501B",
    "RELAY-K501B",
    "RPS TRIP BUS",
    "TC-52-4A",
]


def build_nodes() -> list[str]:
    nodes: list[str] = []
    for node in CORE_NODES:
        add_unique(nodes, node)
    for train in "ABC":
        for node in train_4kv_nodes(train):
            add_unique(nodes, node)
        for node in train_mcc_nodes(train):
            add_unique(nodes, node)
    for node in LOWER_NODES:
        add_unique(nodes, node)
    return nodes


def core_edges() -> list[tuple[str, str]]:
    return [
        edge("SWYD-115KV", "FDR-13A"),
        edge("FDR-13A", "TR-UAT-1A"),
        edge("TR-UAT-1A", "CB-52-4A"),
        edge("CB-52-4A", "BUS-4160-A"),
        edge("SWYD-115KV", "FDR-13B"),
        edge("FDR-13B", "TR-UAT-1B"),
        edge("TR-UAT-1B", "CB-52-4B"),
        edge("CB-52-4B", "BUS-4160-B"),
        edge("SWYD-115KV", "TR-SAT-1"),
        edge("TR-SAT-1", "CB-52-4C"),
        edge("CB-52-4C", "BUS-4160-C"),
        edge("EDG-1A", "CB-DG-1A"),
        edge("CB-DG-1A", "BUS-4160-A"),
        edge("EDG-1B", "CB-DG-1B"),
        edge("CB-DG-1B", "BUS-4160-B"),
        edge("EDG-1C", "CB-DG-1C"),
        edge("CB-DG-1C", "BUS-4160-C"),
        edge("BUS-4160-A", "CB-TIE-AB"),
        edge("CB-TIE-AB", "BUS-4160-B"),
        edge("BUS-4160-B", "CB-TIE-BC"),
        edge("CB-TIE-BC", "BUS-4160-C"),
    ]


def lower_edges(round1: bool = False) -> list[tuple[str, str]]:
    edges = [
        edge("480V CHGR-A FEEDER", "CHGR-125-1A"),
        edge("CHGR-125-1A", "BUS-125DC-A"),
        edge("BAT-125-1A", "BUS-125DC-A"),
        edge("BUS-125DC-A", "INV-120-1A"),
        edge("INV-120-1A", "PNL-RPS-A"),
        edge("PNL-RPS-A", "RELAY-K501A"),
        edge("PNL-RPS-A", "XMTR-PT-501A"),
        edge("PNL-RPS-A", "PNL A/B TIE"),
        edge("PNL A/B TIE", "PNL-RPS-B"),
        edge("480V CHGR-B FEEDER", "CHGR-125-1B"),
        edge("CHGR-125-1B", "BUS-125DC-B"),
        edge("BAT-125-1B", "BUS-125DC-B"),
        edge("BUS-125DC-B", "INV-120-1B"),
        edge("INV-120-1B", "PNL-RPS-B"),
        edge("PNL-RPS-B", "RELAY-K501B"),
        edge("PNL-RPS-B", "XMTR-PT-501B"),
        edge("RELAY-K501B", "TC-52-4A"),
        edge("RPS TRIP BUS", "TC-52-4A"),
    ]
    if round1:
        edges.append(edge("RELAY-K501A", "TC-52-4A"))
    else:
        edges.append(edge("RELAY-K501A", "RPS TRIP BUS"))
    return edges


def build_edges(round_name: str) -> list[tuple[str, str]]:
    is_round1 = round_name == "round_01_diego_high_recall"
    include_charger_feeder = not is_round1
    edges: list[tuple[str, str]] = []
    edges.extend(core_edges())
    for train in "ABC":
        edges.extend(train_4kv_edges(train, round1=is_round1))
        edges.extend(train_mcc_edges(train, include_charger_feeder=include_charger_feeder))
    edges.extend(lower_edges(round1=is_round1))
    return edges


def dedupe_edges(edges: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str]] = []
    for a, b in edges:
        key = normalize_edge(a, b)
        if key not in seen:
            seen.add(key)
            result.append((a, b))
    return result


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[tuple[str, str]], round_name: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["round", "source", "target"])
        for source, target in edges:
            writer.writerow([round_name, source, target])


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in edges:
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def matrix_stats(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, int | bool]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in edges:
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    ones = sum(sum(row) for row in matrix)
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "matrix_ones": ones,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
    }


def image_tokens(path: Path) -> int:
    if Image is None or not path.exists():
        return 0
    with Image.open(path) as image:
        width, height = image.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width = max(1, int(width * scale))
    height = max(1, int(height * scale))
    short = min(width, height)
    if short > 768:
        scale = 768 / short
        width = max(1, int(width * scale))
        height = max(1, int(height * scale))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def rough_text_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def write_token_estimates() -> None:
    diego_images = [
        "raw__overview.png",
        "raw__top_left_2x.png",
        "raw__top_center_2x.png",
        "raw__top_right_2x.png",
        "raw__mid_left_2x.png",
        "raw__mid_center_2x.png",
        "raw__bottom_left_2x.png",
        "raw__bottom_center_2x.png",
    ]
    jennifer_images = [
        "raw__overview.png",
        "wire_nodes__working_area_2x.png",
        "raw__top_left_2x.png",
        "raw__top_center_2x.png",
        "raw__mid_left_2x.png",
        "raw__mid_center_2x.png",
        "raw__bottom_left_2x.png",
        "raw__bottom_center_2x.png",
    ]
    main_images = [
        "raw__mid_left_2x.png",
        "raw__top_center_2x.png",
        "raw__top_right_2x.png",
        "raw__bottom_left_2x.png",
        "raw__bottom_center_2x.png",
        "raw__bottom_right_2x.png",
        "wire_nodes__working_area_2x.png",
        "raw__top_left_2x.png",
        "raw__bottom_dc_full_2x.png",
        "raw__dc_a_panel_detail_3x.png",
    ]
    main_image_tokens = sum(image_tokens(CROPS / name) for name in main_images)
    diego_image_tokens = sum(image_tokens(CROPS / name) for name in diego_images)
    jennifer_image_tokens = sum(image_tokens(CROPS / name) for name in jennifer_images)

    calls = [
        {
            "document": 25,
            "iteration": 1,
            "call_id": "main_doc25_orchestration",
            "caller": "main",
            "round": "orchestration",
            "purpose": "inspect resources, create crops, coordinate agents, generate artifacts",
            "input_low": 11000,
            "input_expected": 16000 + main_image_tokens,
            "input_high": 24000 + main_image_tokens,
            "cached_input_tokens": "not_available",
            "image_file_input_expected": main_image_tokens,
            "output_low": 2500,
            "output_expected": 4500,
            "output_high": 8000,
            "reasoning_tokens": "not_available",
            "usage_object": "not_available",
            "method": "local chars/4 text estimate plus high-detail image tile heuristic; API token endpoint unavailable",
        },
        {
            "document": 25,
            "iteration": 1,
            "call_id": "round_01_diego_high_recall",
            "caller": "Diego",
            "round": "1",
            "purpose": "high-recall extraction from raw and aid crops",
            "input_low": 6500 + diego_image_tokens,
            "input_expected": 8500 + diego_image_tokens,
            "input_high": 11500 + diego_image_tokens,
            "cached_input_tokens": "not_available",
            "image_file_input_expected": diego_image_tokens,
            "output_low": 9000,
            "output_expected": 13500,
            "output_high": 18000,
            "reasoning_tokens": "not_available",
            "usage_object": "not_available",
            "method": "prompt/file estimate; output estimated from returned text length scale",
        },
        {
            "document": 25,
            "iteration": 1,
            "call_id": "round_02_jennifer_precision",
            "caller": "Jennifer",
            "round": "2",
            "purpose": "precision review and refined edge list",
            "input_low": 7500 + jennifer_image_tokens,
            "input_expected": 10500 + jennifer_image_tokens,
            "input_high": 15000 + jennifer_image_tokens,
            "cached_input_tokens": "not_available",
            "image_file_input_expected": jennifer_image_tokens,
            "output_low": 8500,
            "output_expected": 12500,
            "output_high": 17000,
            "reasoning_tokens": "not_available",
            "usage_object": "not_available",
            "method": "prompt/file estimate; output estimated from returned text length scale",
        },
        {
            "document": 25,
            "iteration": 1,
            "call_id": "round_03_diego_saturation",
            "caller": "Diego",
            "round": "3",
            "purpose": "saturation agreement check",
            "input_low": 6500,
            "input_expected": 12000,
            "input_high": 22000,
            "cached_input_tokens": "not_available",
            "image_file_input_expected": 0,
            "output_low": 120,
            "output_expected": 260,
            "output_high": 600,
            "reasoning_tokens": "not_available",
            "usage_object": "not_available",
            "method": "existing agent context plus new text; cached tokens unavailable",
        },
        {
            "document": 25,
            "iteration": 1,
            "call_id": "round_04_jennifer_final",
            "caller": "Jennifer",
            "round": "4",
            "purpose": "final unchanged confirmation",
            "input_low": 5000,
            "input_expected": 11000,
            "input_high": 21000,
            "cached_input_tokens": "not_available",
            "image_file_input_expected": 0,
            "output_low": 20,
            "output_expected": 35,
            "output_high": 100,
            "reasoning_tokens": "not_available",
            "usage_object": "not_available",
            "method": "existing agent context plus new text; cached tokens unavailable",
        },
    ]
    for call in calls:
        call["total_expected"] = int(call["input_expected"]) + int(call["output_expected"])

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "document",
            "iteration",
            "call_id",
            "caller",
            "round",
            "purpose",
            "input_low",
            "input_expected",
            "input_high",
            "cached_input_tokens",
            "image_file_input_expected",
            "output_low",
            "output_expected",
            "output_high",
            "reasoning_tokens",
            "usage_object",
            "total_expected",
            "method",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    summary = {
        "document": 25,
        "iteration": 1,
        "calls": calls,
        "total_expected_tokens": sum(int(call["total_expected"]) for call in calls),
        "total_low_tokens": sum(int(call["input_low"]) + int(call["output_low"]) for call in calls),
        "total_high_tokens": sum(int(call["input_high"]) + int(call["output_high"]) for call in calls),
        "responses_input_token_count_endpoint": "not_called_no_api_key",
        "usage_objects": "not_available_from_subagent_tool_or_main_runtime",
        "local_estimation_method": "text chars/4 plus OpenAI-style high-detail image tile heuristic",
    }
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_notes(stats: dict[str, dict[str, int | bool]]) -> None:
    notes = """# Document 25 Extraction Notes

Scope: visual extraction from `Raw + wires + components + junctions` only. No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels and edges were read from the raw schematic and local visual crops/overlays.

Agent rounds:
- Round 01 Diego high-recall: broad graph including plausible branch-01 direct breaker-to-MS edges and lower RPS route interpretations.
- Round 02 Jennifer precision: accepted source/train structure, moved branch-01 MS feeds downstream of DS-4X01, removed MCC-to-MCC and pass-by dashed/dotted overconnections, added visible charger feeder edges from MCC-A2/B2.
- Round 03 Diego saturation: accepted Jennifer final unchanged.
- Round 04 Jennifer final: confirmed final accepted unchanged.

Important conventions applied:
- Crossings without dots are not junctions.
- Bus dots/taps are true terminals.
- Solid lines are power/DC power; dashed lines are control/interlock/trip; dotted lines are instrument signal.
- Ground references such as GND-ESF-X05 are kept as tagged nodes where visibly labelled.
- The title-block CSV filename was ignored as non-visual/GT-adjacent reference text.

Remaining uncertainties not included:
- Pin-level detail inside TC-52-4A.
- Dashed-lane junctions near TC-52-4A without visible terminals/dots.
- Any direct connection from 480V CHGR-B FEEDER to INV-120-1A, PNL-RPS-A, or RELAY-K501A.
- Any direct MCC-X1 to MCC-X2 tie.
- Any off-sheet continuation beyond the visible RPS TRIP BUS arrow.

Final stats:
"""
    for name, values in stats.items():
        notes += f"- {name}: {values['nodes']} nodes, {values['edges']} edges, symmetric={values['symmetric']}, diagonal_zero={values['diagonal_zero']}\n"
    (RESULTS / "extraction_notes.md").write_text(notes, encoding="utf-8")


def main() -> None:
    nodes = build_nodes()
    rounds = [
        ("round_01_diego_high_recall", "Diego high-recall"),
        ("round_02_jennifer_precision", "Jennifer precision"),
        ("round_03_diego_saturation", "Diego saturation acceptance"),
        ("round_04_jennifer_final", "Jennifer final accepted"),
    ]
    stats: dict[str, dict[str, int | bool]] = {}
    final_edges: list[tuple[str, str]] | None = None

    for round_name, _label in rounds:
        round_edges = dedupe_edges(build_edges(round_name))
        unknown = sorted({node for pair in round_edges for node in pair if node not in nodes})
        if unknown:
            raise ValueError(f"{round_name} has edges referencing unknown nodes: {unknown}")
        write_nodes(RESULTS / f"{round_name}_nodes.csv", nodes)
        write_edges(RESULTS / f"{round_name}_edges.csv", round_edges, round_name)
        write_matrix(RESULTS / f"{round_name}_connectivity_matrix.csv", nodes, round_edges)
        stats[round_name] = matrix_stats(nodes, round_edges)
        if round_name == "round_04_jennifer_final":
            final_edges = round_edges

    assert final_edges is not None
    write_nodes(RESULTS / "final_nodes.csv", nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges, "final")
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final_edges)

    graph = {
        "document": 25,
        "iteration": 1,
        "nodes": nodes,
        "edges": [{"source": a, "target": b} for a, b in final_edges],
        "stats": stats["round_04_jennifer_final"],
    }
    (RESULTS / "final_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")

    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["document", "iteration", "round", "description", "nodes", "edges", "matrix_ones", "symmetric", "diagonal_zero"])
        for round_name, label in rounds:
            values = stats[round_name]
            writer.writerow(
                [
                    25,
                    1,
                    round_name,
                    label,
                    values["nodes"],
                    values["edges"],
                    values["matrix_ones"],
                    values["symmetric"],
                    values["diagonal_zero"],
                ]
            )

    write_token_estimates()
    write_notes(stats)


if __name__ == "__main__":
    main()
