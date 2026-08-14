from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:
    tiktoken = None


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires")
CROPS = BASE / "codes" / "crops_doc18"
RESULTS = BASE / "results"


TOP_NODES = [
    "GRID-SWYD-1",
    "CB-GRID-A",
    "GRID-SWYD-2",
    "CB-GRID-B",
    "BB-SWYD-230",
    "CB-GEN-ISO",
    "GEN-MAIN-1",
    "TR-UAT-1A",
    "CB-UAT-A",
    "TR-UAT-1B",
    "CB-UAT-B",
    "TR-SAT-1A",
    "CB-SAT-A",
    "TR-SAT-1B",
    "CB-SAT-B",
    "BUS-4160A",
    "DG-1A",
    "CB-DG-A",
    "PT-4160A",
    "FU-PT-A",
    "XFMR-CTRL-A",
    "TB-RPS-A",
    "SW-43A",
    "GND-4160A",
    "CB-4160-TIE",
    "BUS-4160B",
    "GND-4160B",
    "PT-4160B",
    "FU-PT-B",
    "XFMR-CTRL-B",
    "TB-RPS-B",
    "SW-43B",
    "DG-1B",
    "CB-DG-B",
    "TR-480-A1",
    "CB-480A-IN",
    "TR-480-B1",
    "CB-480B-IN",
    "TR-480-C1",
    "CB-480C-IN",
    "TR-480-D1",
    "CB-480D-IN",
    "BUS-480A",
    "BUS-480B",
    "BUS-480C",
    "BUS-480D",
]

CONTROL_NODES = [
    "CHG-125A",
    "REC-125A",
    "CB-DC-A",
    "BUS-125A",
    "BAT-125A",
    "GND-DC-A",
    "INV-120A",
    "UPS-120A",
    "BUS-120A",
    "RPS-PNL-A",
    "PLC-RPS-A",
    "RELAY-K101",
    "RELAY-K102",
    "RELAY-K103",
    "RELAY-K104",
    "JB-RPS-A",
    "PNL-ANN-A",
    "CHG-125B",
    "REC-125B",
    "CB-DC-B",
    "BUS-125B",
    "BAT-125B",
    "GND-DC-B",
    "INV-120B",
    "UPS-120B",
    "BUS-120B",
    "RPS-PNL-B",
    "PLC-RPS-B",
    "RELAY-K201",
    "RELAY-K202",
    "RELAY-K203",
    "RELAY-K204",
    "JB-RPS-B",
    "PNL-ANN-B",
]


def load_branches(c06_panel_label: str) -> dict[str, list[list[str]]]:
    return {
        "BUS-480A": [
            ["CB-A01", "DS-A01", "MS-A01", "PUMP-CCW-A1"],
            ["CB-A02", "DS-A02", "MS-A02", "PUMP-RHR-A1"],
            ["CB-A03", "FS-A03", "MS-A03", "FAN-RB-A1"],
            ["CB-A04", "DS-A04", "RY-A04", "MOV-SI-A11"],
            ["CB-A05", "DS-A05", "CP-A05", "PNL-LTG-A1"],
            ["CB-A06", "DS-A06", "MS-A06", "PUMP-AFW-A1"],
            ["CB-A07", "FS-A07", "FU-A07", "HTR-PZR-A1"],
            ["CB-A08", "DS-A08", "TB-A08", "SPARE-A8"],
        ],
        "BUS-480B": [
            ["CB-B01", "DS-B01", "MS-B01", "PUMP-CCW-B1"],
            ["CB-B02", "DS-B02", "MS-B02", "PUMP-RHR-B1"],
            ["CB-B03", "FS-B03", "MS-B03", "FAN-FUEL-B1"],
            ["CB-B04", "DS-B04", "RY-B04", "MOV-CCW-B21"],
            ["CB-B05", "DS-B05", "CP-B05", "MCC-AUX-B6"],
            ["CB-B06", "DS-B06", "MS-B06", "AIR-CMP-B1"],
            ["CB-B07", "FS-B07", "RY-B07", "VLV-CHG-B1"],
        ],
        "BUS-480C": [
            ["CB-C01", "DS-C01", "MS-C01", "PUMP-HPCI-C1"],
            ["CB-C02", "DS-C02", "MS-C02", "PUMP-RCW-C1"],
            ["CB-C03", "FS-C03", "MS-C03", "FAN-RB-C1"],
            ["CB-C04", "DS-C04", "RY-C04", "MOV-RHR-C11"],
            ["CB-C05", "DS-C05", "MS-C05", "PUMP-SEAL-C1"],
            ["CB-C06", "DS-C06", "CP-C06", c06_panel_label],
            ["CB-C07", "FS-C07", "MS-C07", "SUMP-PMP-C1"],
            ["CB-C08", "DS-C08", "FU-C08", "HTR-VENT-C2"],
        ],
        "BUS-480D": [
            ["CB-D01", "DS-D01", "MS-D01", "PUMP-AFW-D1"],
            ["CB-D02", "DS-D02", "MS-D02", "FAN-CR-D1"],
            ["CB-D03", "FS-D03", "RY-D03", "MOV-SI-D21"],
            ["CB-D04", "DS-D04", "MS-D04", "PUMP-LUBE-D1"],
            ["CB-D05", "DS-D05", "CP-D05", "PNL-ESS-D5"],
            ["CB-D06", "DS-D06", "MS-D06", "COMP-AIR-D1"],
            ["CB-D07", "FS-D07", "TB-D07", "SPARE-D7"],
        ],
    }


@dataclass
class Graph:
    nodes: list[str]
    edges: list[tuple[str, str]]
    metadata: dict[tuple[str, str], dict[str, str]]


def edge_key(u: str, v: str) -> tuple[str, str]:
    return tuple(sorted((u, v)))


def ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def build_graph(c06_panel_label: str) -> Graph:
    nodes = list(TOP_NODES)
    for branches in load_branches(c06_panel_label).values():
        for branch in branches:
            nodes.extend(branch)
    nodes.extend(CONTROL_NODES)
    nodes = ordered_unique(nodes)

    edges: list[tuple[str, str]] = []
    metadata: dict[tuple[str, str], dict[str, str]] = {}

    def add(u: str, v: str, confidence: str = "0.97", evidence: str = "visually supported") -> None:
        key = edge_key(u, v)
        if key not in metadata:
            edges.append((u, v))
            metadata[key] = {"confidence": confidence, "evidence": evidence}

    def chain(seq: list[str], confidence: str = "0.97", evidence: str = "adjacent visible chain") -> None:
        for u, v in zip(seq, seq[1:]):
            add(u, v, confidence, evidence)

    chain(["GRID-SWYD-1", "CB-GRID-A", "BB-SWYD-230"], "0.98", "solid switchyard feeder")
    chain(["GRID-SWYD-2", "CB-GRID-B", "BB-SWYD-230"], "0.98", "solid switchyard feeder")
    chain(["BB-SWYD-230", "TR-SAT-1A", "CB-SAT-A", "BUS-4160A"], "0.98", "solid standby transformer feeder")
    chain(["BB-SWYD-230", "TR-SAT-1B", "CB-SAT-B", "BUS-4160B"], "0.98", "solid standby transformer feeder")
    chain(["BB-SWYD-230", "CB-GEN-ISO", "GEN-MAIN-1"], "0.98", "solid generator isolation path")
    chain(["GEN-MAIN-1", "TR-UAT-1A", "CB-UAT-A"], "0.95", "solid UAT branch; lower breaker terminal is dangling")
    chain(["GEN-MAIN-1", "TR-UAT-1B", "CB-UAT-B"], "0.95", "solid UAT branch; lower breaker terminal is dangling")

    chain(["BUS-4160A", "CB-DG-A", "DG-1A"], "0.98", "solid diesel generator feeder")
    chain(["BUS-4160B", "CB-DG-B", "DG-1B"], "0.98", "solid diesel generator feeder")
    add("BUS-4160A", "GND-4160A", "0.96", "solid named ground tap")
    add("BUS-4160B", "GND-4160B", "0.96", "solid named ground tap")
    chain(["BUS-4160A", "CB-4160-TIE", "BUS-4160B"], "0.97", "solid 4160 bus tie marked N.O.")

    chain(["BUS-4160A", "TB-RPS-A", "TR-480-A1", "CB-480A-IN", "BUS-480A"], "0.93", "solid A feeder; terminal block visibly inline")
    chain(["BUS-4160A", "TR-480-B1", "CB-480B-IN", "BUS-480B"], "0.98", "solid 4160-to-480 feeder")
    chain(["BUS-4160B", "TR-480-C1", "CB-480C-IN", "BUS-480C"], "0.98", "solid 4160-to-480 feeder")
    chain(["BUS-4160B", "TR-480-D1", "CB-480D-IN", "BUS-480D"], "0.98", "solid 4160-to-480 feeder")

    chain(["BUS-4160A", "PT-4160A", "FU-PT-A", "XFMR-CTRL-A", "TB-RPS-A", "SW-43A"], "0.95", "dashed PT/RPS control chain")
    chain(["BUS-4160B", "PT-4160B", "FU-PT-B", "XFMR-CTRL-B", "TB-RPS-B", "SW-43B"], "0.95", "dashed PT/RPS control chain")

    for bus, branches in load_branches(c06_panel_label).items():
        for branch in branches:
            chain([bus, *branch], "0.98", "solid 480V bus-tap load chain")

    chain(["BUS-480B", "CHG-125A", "REC-125A", "CB-DC-A", "BUS-125A"], "0.95", "solid Train A control-power source path")
    chain(["BUS-480C", "CHG-125B", "REC-125B", "CB-DC-B", "BUS-125B"], "0.95", "solid Train B control-power source path")

    add("BUS-125A", "BAT-125A", "0.98", "solid battery tap")
    add("BUS-125A", "GND-DC-A", "0.96", "solid DC ground tap")
    add("BUS-125A", "INV-120A", "0.96", "solid DC bus to inverter path")
    add("INV-120A", "UPS-120A", "0.94", "dashed inverter-to-UPS signal/power path")
    add("UPS-120A", "BUS-120A", "0.98", "solid UPS output to 120V bus")
    add("BUS-120A", "RPS-PNL-A", "0.98", "solid 120V bus tap to RPS panel")
    add("RPS-PNL-A", "PLC-RPS-A", "0.95", "dashed RPS panel to PLC path")
    for relay in ["RELAY-K101", "RELAY-K102", "RELAY-K103", "RELAY-K104"]:
        add("PLC-RPS-A", relay, "0.86", "dashed RPS relay harness endpoint")
    add("RELAY-K102", "JB-RPS-A", "0.86", "dashed branch from K102 harness to JB")
    add("RELAY-K102", "PNL-ANN-A", "0.86", "dashed branch from K102 harness to annunciator")

    add("BUS-125B", "BAT-125B", "0.98", "solid battery tap")
    add("BUS-125B", "GND-DC-B", "0.96", "solid DC ground tap")
    add("BUS-125B", "INV-120B", "0.96", "solid DC bus to inverter path")
    add("INV-120B", "UPS-120B", "0.94", "dashed inverter-to-UPS signal/power path")
    add("UPS-120B", "BUS-120B", "0.98", "solid UPS output to 120V bus")
    add("BUS-120B", "RPS-PNL-B", "0.98", "solid 120V bus tap to RPS panel")
    add("RPS-PNL-B", "PLC-RPS-B", "0.95", "dashed RPS panel to PLC path")
    for relay in ["RELAY-K201", "RELAY-K202", "RELAY-K203", "RELAY-K204"]:
        add("PLC-RPS-B", relay, "0.86", "dashed RPS relay harness endpoint")
    add("RELAY-K202", "JB-RPS-B", "0.86", "dashed branch from K202 harness to JB")
    add("RELAY-K202", "PNL-ANN-B", "0.86", "dashed branch from K202 harness to annunciator")

    unknown = sorted({node for edge in edges for node in edge} - set(nodes))
    if unknown:
        raise ValueError(f"Edges reference nodes missing from node list: {unknown}")

    return Graph(nodes=nodes, edges=edges, metadata=metadata)


def adjacency_matrix(graph: Graph) -> list[list[int]]:
    idx = {node: i for i, node in enumerate(graph.nodes)}
    matrix = [[0 for _ in graph.nodes] for _ in graph.nodes]
    for u, v in graph.edges:
        i, j = idx[u], idx[v]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def validate(graph: Graph) -> dict[str, int | bool]:
    matrix = adjacency_matrix(graph)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(matrix)))
    return {
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
    }


def write_nodes(path: Path, graph: Graph) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(graph.nodes):
            writer.writerow([i, node])


def write_edges(path: Path, graph: Graph) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["edge_id", "u", "v", "confidence", "evidence"])
        for i, (u, v) in enumerate(graph.edges):
            meta = graph.metadata[edge_key(u, v)]
            writer.writerow([i, u, v, meta["confidence"], meta["evidence"]])


def write_matrix(path: Path, graph: Graph) -> None:
    matrix = adjacency_matrix(graph)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component"] + graph.nodes)
        for node, row in zip(graph.nodes, matrix):
            writer.writerow([node] + row)


def write_round(prefix: str, graph: Graph) -> dict[str, int | bool]:
    write_nodes(RESULTS / f"{prefix}_nodes.csv", graph)
    write_edges(RESULTS / f"{prefix}_edges.csv", graph)
    write_matrix(RESULTS / f"{prefix}_matrix.csv", graph)
    return validate(graph)


def estimate_text_tokens(text: str) -> int:
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    return math.ceil(len(text) / 4)


def estimate_image_tokens(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)


def estimate_images(paths: list[str]) -> int:
    return sum(estimate_image_tokens(CROPS / name) for name in paths)


def write_token_estimates() -> dict[str, int]:
    method = "local text estimate + high-detail 512px image tile heuristic; no API key/usage object available"
    model = "gpt-5.5 for subagents; main agent model not exposed"

    main_images = [
        "overview_raw.png",
        "top_sources_buses_raw_2x.png",
        "top_left_sources_raw_2x.png",
        "top_center_tie_raw_2x.png",
        "top_right_sources_notes_raw_2x.png",
        "top_right_uat_bus_raw_2x.png",
        "train_a_loads_raw_2x.png",
        "train_b_loads_raw_2x.png",
        "train_c_loads_raw_2x.png",
        "train_d_loads_raw_2x.png",
        "bottom_control_a_raw_2x.png",
        "bottom_control_b_raw_2x.png",
        "bottom_a_right_rps_raw_2x.png",
        "bottom_b_right_rps_raw_2x.png",
    ]
    r1_images = [
        "overview_raw.png",
        "top_sources_buses_raw_2x.png",
        "top_sources_buses_overlay_2x.png",
        "top_left_sources_raw_2x.png",
        "top_center_tie_raw_2x.png",
        "top_right_uat_bus_raw_2x.png",
        "train_a_loads_raw_2x.png",
        "train_b_loads_raw_2x.png",
        "train_c_loads_raw_2x.png",
        "train_d_loads_raw_2x.png",
        "bottom_control_a_raw_2x.png",
        "bottom_control_b_raw_2x.png",
        "bottom_control_all_overlay_2x.png",
        "bottom_a_right_rps_raw_2x.png",
        "bottom_b_right_rps_raw_2x.png",
    ]
    r2_images = [
        "overview_raw.png",
        "top_sources_buses_raw_2x.png",
        "top_a_pt_rps_detail_raw_2x.png",
        "top_right_uat_bus_raw_2x.png",
        "top_b_pt_rps_detail_raw_2x.png",
        "train_c_loads_raw_2x.png",
        "bottom_control_a_raw_2x.png",
        "bottom_control_b_raw_2x.png",
        "bottom_a_right_rps_raw_2x.png",
        "bottom_b_right_rps_raw_2x.png",
    ]

    prompts = {
        "Main orchestration and visual spot checks": "Document 18 blind extraction; inspect raw, overlay, generated crops; create scripts, matrix artifacts, token estimates.",
        "Diego R1": "High-recall extractor prompt with resource rules, component/node/edge request, evidence and ambiguity instructions.",
        "Jennifer R1": "Precision reviewer prompt with Diego proposal summary, candidate removals, label check, and relay-network focus.",
        "Diego R2": "Second high-recall saturation prompt with Jennifer corrections and final candidate focus areas.",
        "Jennifer R2": "Final precision saturation prompt confirming no further graph changes after Diego R2.",
    }
    rows = [
        ("orchestration", "Main agent", "Main orchestration and visual spot checks", main_images, 2200, 1800, 3500, 6500),
        ("round1_diego", "Diego", "Diego R1", r1_images, 650, 6500, 11000, 18000),
        ("round1_jennifer", "Jennifer", "Jennifer R1", r1_images, 1450, 4500, 8000, 14000),
        ("round2_diego", "Diego", "Diego R2", r2_images, 650, 800, 1600, 3200),
        ("round2_jennifer", "Jennifer", "Jennifer R2", r2_images, 550, 800, 1600, 3200),
    ]

    totals = {
        "input_text_tokens_est": 0,
        "input_image_tokens_est": 0,
        "total_low": 0,
        "total_expected": 0,
        "total_high": 0,
    }
    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "document",
            "iteration",
            "round_name",
            "actor",
            "model_call",
            "model",
            "text_input_tokens_est",
            "image_input_tokens_est",
            "cached_input_tokens",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens",
            "total_low",
            "total_expected",
            "total_high",
            "method",
        ])
        for round_name, actor, call, images, manual_text_tokens, out_low, out_exp, out_high in rows:
            text_tokens = max(estimate_text_tokens(prompts[call]), manual_text_tokens)
            image_tokens = estimate_images(images)
            total_low = text_tokens + image_tokens + out_low
            total_expected = text_tokens + image_tokens + out_exp
            total_high = text_tokens + image_tokens + out_high
            totals["input_text_tokens_est"] += text_tokens
            totals["input_image_tokens_est"] += image_tokens
            totals["total_low"] += total_low
            totals["total_expected"] += total_expected
            totals["total_high"] += total_high
            writer.writerow([
                18,
                1,
                round_name,
                actor,
                call,
                model,
                text_tokens,
                image_tokens,
                "not available",
                out_low,
                out_exp,
                out_high,
                "not available",
                total_low,
                total_expected,
                total_high,
                method,
            ])

    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Token Usage Estimate - Document 18\n\n")
        f.write("The OpenAI Responses input-token counting endpoint and actual subagent usage objects were unavailable because no API key/usage object was exposed in this environment.\n\n")
        f.write(f"- Input text tokens estimated: {totals['input_text_tokens_est']}\n")
        f.write(f"- Image/file input tokens estimated: {totals['input_image_tokens_est']}\n")
        f.write(f"- Total low estimate: {totals['total_low']}\n")
        f.write(f"- Total expected estimate: {totals['total_expected']}\n")
        f.write(f"- Total high estimate: {totals['total_high']}\n")

    return totals


def write_notes(round_validations: dict[str, dict[str, int | bool]], final_validation: dict[str, int | bool], token_totals: dict[str, int]) -> None:
    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as f:
        f.write("# Document 18 Connectivity Extraction Notes\n\n")
        f.write("Only the raw schematic, wires mask, wires mask overlay, and generated crops under `Raw + wires` were used. Existing result/validation files were not opened or used. No GT-derived feedback or off-the-shelf OCR was used.\n\n")
        f.write("## Final Result\n\n")
        f.write(f"- Nodes: {final_validation['node_count']}\n")
        f.write(f"- Edges: {final_validation['edge_count']}\n")
        f.write(f"- Symmetric matrix: {final_validation['symmetric']}\n")
        f.write(f"- Diagonal zero: {final_validation['diagonal_zero']}\n\n")
        f.write("## Round Progress\n\n")
        for name, stats in round_validations.items():
            f.write(f"- `{name}`: {stats['node_count']} nodes, {stats['edge_count']} edges.\n")
        f.write("\n## Precision Decisions\n\n")
        f.write("- Corrected Diego R1 label `PNL-TC-C7` to visually supported `PNL-IC-C7`.\n")
        f.write("- Kept `TB-RPS-A` inline on the A-side solid feeder and also on the dashed PT/RPS control chain.\n")
        f.write("- Kept UAT lower breaker stubs as dangling from `TR-UAT-1A/B`; no `CB-UAT-A/B` to 4160 bus edges were added.\n")
        f.write("- Kept `TB-RPS-B` only on the dashed PT/control chain; no `TB-RPS-B--TR-480-D1` edge was added.\n")
        f.write("- Kept compact RPS relay harness edges through `PLC-RPS-A/B` and `RELAY-K102/K202`; no extra relay-to-relay or direct JB-to-annunciator edges were added.\n\n")
        f.write("## Token Estimate\n\n")
        f.write(f"- Expected total tokens estimated: {token_totals['total_expected']} (low {token_totals['total_low']}, high {token_totals['total_high']}).\n")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    round_graphs = {
        "round1_diego": build_graph("PNL-TC-C7"),
        "round1_jennifer": build_graph("PNL-IC-C7"),
        "round2_diego": build_graph("PNL-IC-C7"),
        "round2_jennifer": build_graph("PNL-IC-C7"),
    }
    round_validations = {name: write_round(name, graph) for name, graph in round_graphs.items()}

    final_graph = round_graphs["round2_jennifer"]
    write_nodes(RESULTS / "final_nodes.csv", final_graph)
    write_edges(RESULTS / "final_edges.csv", final_graph)
    write_matrix(RESULTS / "connectivity_matrix.csv", final_graph)
    final_validation = validate(final_graph)

    token_totals = write_token_estimates()
    write_notes(round_validations, final_validation, token_totals)

    manifest = {
        "document": 18,
        "iteration": 1,
        "resource_root": str(BASE),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "final_validation": final_validation,
        "round_validations": round_validations,
        "final_files": ["final_nodes.csv", "final_edges.csv", "connectivity_matrix.csv"],
        "round_prefixes": list(round_graphs.keys()),
        "token_estimate_totals": token_totals,
    }
    with (RESULTS / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps({
        "validation": final_validation,
        "round_validations": round_validations,
        "token_estimate_totals": token_totals,
    }, indent=2))


if __name__ == "__main__":
    main()
