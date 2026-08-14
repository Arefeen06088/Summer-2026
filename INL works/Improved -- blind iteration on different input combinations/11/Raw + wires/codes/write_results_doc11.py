from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    import tiktoken
except Exception:
    tiktoken = None

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires")
CROPS = BASE / "codes" / "crops_doc11"
RESULTS = BASE / "results"

TRAINS = ["A", "B", "C", "D"]


TOP_NODES = [
    "GEN-01",
    "TR-UAT-1",
    "CB-UAT-1",
    "TR-SUT-1",
    "CB-SUT-1",
    "BUS-13-8A",
    "CB-13-TIE",
    "BUS-13-8B",
    "GEN-02",
    "TR-UAT-2",
    "CB-UAT-2",
    "TR-SUT-2",
    "CB-SUT-2",
]


def train_nodes(train: str) -> list[str]:
    return [
        f"CB-IN-{train}",
        f"RELAY-27{train}",
        f"DG-1{train}",
        f"CB-DG-{train}",
        f"BUS-4160-{train}",
        f"CB-4160-{train}1",
        f"TR-480-{train}1",
        f"CB-480-{train}1",
        f"BUS-480-{train}1",
        f"CB-MCC-{train}1",
        f"MCC-{train}1",
        f"PUMP-SI-{train}",
        f"PUMP-CCW-{train}",
        f"FAN-HVAC-{train}",
        f"CB-4160-{train}2",
        f"TR-480-{train}2",
        f"CB-480-{train}2",
        f"BUS-480-{train}2",
        f"CB-MCC-{train}2",
        f"MCC-{train}2",
        f"MOV-RHR-{train}",
        f"RECT-125-{train}",
        f"PANEL-IC-{train}",
        f"GND-{train}",
    ]


BOTTOM_NODES = [
    "ATS-480-A",
    "ATS-480-B",
    "BAT-125A",
    "BUS-DC-125A",
    "INV-UPS-A",
    "PANEL-RPS-A",
    "PANEL-SSPS",
    "BAT-125B",
    "BUS-DC-125B",
    "INV-UPS-B",
    "PANEL-RPS-B",
]


NODES = TOP_NODES + [node for train in TRAINS for node in train_nodes(train)] + BOTTOM_NODES


def edge(u: str, v: str, kind: str, evidence: str) -> tuple[str, str, str, str]:
    return (u, v, kind, evidence)


TOP_EDGES = [
    edge("GEN-01", "TR-UAT-1", "solid", "Generator GEN-01 solid 13.8 kV feeder lands on TR-UAT-1."),
    edge("TR-UAT-1", "CB-UAT-1", "solid", "TR-UAT-1 secondary feeder lands on CB-UAT-1."),
    edge("CB-UAT-1", "BUS-13-8A", "solid", "CB-UAT-1 is connected to BUS-13-8A."),
    edge("TR-SUT-1", "CB-SUT-1", "solid", "TR-SUT-1 secondary feeder lands on CB-SUT-1."),
    edge("CB-SUT-1", "BUS-13-8A", "solid", "CB-SUT-1 is connected to BUS-13-8A."),
    edge("BUS-13-8A", "CB-13-TIE", "solid", "BUS-13-8A connects to the 13.8 kV tie breaker."),
    edge("CB-13-TIE", "BUS-13-8B", "solid", "Tie breaker output connects to BUS-13-8B."),
    edge("GEN-02", "TR-UAT-2", "solid", "Generator GEN-02 solid 13.8 kV feeder lands on TR-UAT-2."),
    edge("TR-UAT-2", "CB-UAT-2", "solid", "TR-UAT-2 secondary feeder lands on CB-UAT-2."),
    edge("CB-UAT-2", "BUS-13-8B", "solid", "CB-UAT-2 is connected to BUS-13-8B."),
    edge("TR-SUT-2", "CB-SUT-2", "solid", "TR-SUT-2 secondary feeder lands on CB-SUT-2."),
    edge("CB-SUT-2", "BUS-13-8B", "solid", "CB-SUT-2 is connected to BUS-13-8B."),
    edge("BUS-13-8A", "CB-IN-A", "solid", "Normal feeder from BUS-13-8A drops to CB-IN-A."),
    edge("BUS-13-8A", "CB-IN-B", "solid", "Normal feeder from BUS-13-8A drops to CB-IN-B."),
    edge("BUS-13-8B", "CB-IN-C", "solid", "Normal feeder from BUS-13-8B drops to CB-IN-C."),
    edge("BUS-13-8B", "CB-IN-D", "solid", "Normal feeder from BUS-13-8B drops to CB-IN-D."),
]


def train_edges(train: str) -> list[tuple[str, str, str, str]]:
    return [
        edge(f"CB-IN-{train}", f"BUS-4160-{train}", "solid", f"CB-IN-{train} solid incoming feeder lands on BUS-4160-{train}."),
        edge(f"DG-1{train}", f"CB-DG-{train}", "solid", f"Diesel generator DG-1{train} feeder lands on CB-DG-{train}."),
        edge(f"CB-DG-{train}", f"BUS-4160-{train}", "solid", f"CB-DG-{train} output lands on BUS-4160-{train}."),
        edge(f"CB-IN-{train}", f"RELAY-27{train}", "dashed control", f"Dashed control path terminates at CB-IN-{train} and RELAY-27{train}."),
        edge(f"RELAY-27{train}", f"CB-DG-{train}", "dashed control", f"Dashed 27 relay path terminates at CB-DG-{train}."),
        edge(f"RELAY-27{train}", "PANEL-SSPS", "dashed control", f"Dashed RELAY-27{train} route continues to visible PANEL-SSPS top terminals."),
        edge(f"BUS-4160-{train}", f"CB-4160-{train}1", "solid", f"First 4.16 kV feeder from BUS-4160-{train}."),
        edge(f"CB-4160-{train}1", f"TR-480-{train}1", "solid", f"CB-4160-{train}1 feeds TR-480-{train}1."),
        edge(f"TR-480-{train}1", f"CB-480-{train}1", "solid", f"TR-480-{train}1 secondary feeds CB-480-{train}1."),
        edge(f"CB-480-{train}1", f"BUS-480-{train}1", "solid", f"CB-480-{train}1 output lands on BUS-480-{train}1."),
        edge(f"BUS-4160-{train}", f"CB-4160-{train}2", "solid", f"Second 4.16 kV feeder from BUS-4160-{train}."),
        edge(f"CB-4160-{train}2", f"TR-480-{train}2", "solid", f"CB-4160-{train}2 feeds TR-480-{train}2."),
        edge(f"TR-480-{train}2", f"CB-480-{train}2", "solid", f"TR-480-{train}2 secondary feeds CB-480-{train}2."),
        edge(f"CB-480-{train}2", f"BUS-480-{train}2", "solid", f"CB-480-{train}2 output lands on BUS-480-{train}2."),
        edge(f"BUS-480-{train}1", f"BUS-480-{train}2", "solid tie", f"Solid continuous 480 V bus tie at TIE-{train}12 between bus sections."),
        edge(f"BUS-480-{train}1", f"CB-MCC-{train}1", "solid", f"BUS-480-{train}1 feeder drops to CB-MCC-{train}1."),
        edge(f"CB-MCC-{train}1", f"MCC-{train}1", "solid", f"CB-MCC-{train}1 feeds MCC-{train}1."),
        edge(f"MCC-{train}1", f"PUMP-SI-{train}", "solid", f"MCC-{train}1 feeder terminates at PUMP-SI-{train}."),
        edge(f"MCC-{train}1", f"PUMP-CCW-{train}", "solid", f"MCC-{train}1 feeder terminates at PUMP-CCW-{train}."),
        edge(f"MCC-{train}1", f"FAN-HVAC-{train}", "solid", f"MCC-{train}1 feeder terminates at FAN-HVAC-{train}."),
        edge(f"BUS-480-{train}2", f"CB-MCC-{train}2", "solid", f"BUS-480-{train}2 feeder drops to CB-MCC-{train}2."),
        edge(f"CB-MCC-{train}2", f"MCC-{train}2", "solid", f"CB-MCC-{train}2 feeds MCC-{train}2."),
        edge(f"MCC-{train}2", f"MOV-RHR-{train}", "solid", f"MCC-{train}2 feeder terminates at MOV-RHR-{train}."),
        edge(f"MCC-{train}2", f"PANEL-IC-{train}", "dashed control", f"Dashed conductor from MCC-{train}2 area terminates at PANEL-IC-{train}."),
        edge(f"BUS-480-{train}2", f"RECT-125-{train}", "solid", f"BUS-480-{train}2 branch labeled 125 VDC/BC-{train} feeds RECT-125-{train}."),
        edge(f"RECT-125-{train}", f"PANEL-IC-{train}", "solid", f"RECT-125-{train} output enters the PANEL-IC-{train} conductor path."),
        edge(f"PANEL-IC-{train}", f"GND-{train}", "solid ground", f"PANEL-IC-{train} lower conductor connects to explicit GND-{train} symbol with dot."),
    ]


FINAL_EDGES = TOP_EDGES + [item for train in TRAINS for item in train_edges(train)] + [
    edge("PANEL-IC-A", "BUS-DC-125A", "solid route", "DC-A125 route from PANEL-IC-A lands on BUS-DC-125A."),
    edge("PANEL-IC-B", "BUS-DC-125B", "solid route", "DC-B125 route from PANEL-IC-B lands on BUS-DC-125B routing."),
    edge("PANEL-IC-C", "BUS-DC-125B", "solid route", "DC-C125 route from PANEL-IC-C ties into the division B DC bus routing."),
    edge("PANEL-IC-D", "BUS-DC-125B", "solid route", "DC-D125 route from PANEL-IC-D lands on BUS-DC-125B routing."),
    edge("BUS-480-A1", "ATS-480-A", "solid", "ATS-A1 branch from BUS-480-A1 lands on ATS-480-A."),
    edge("BUS-480-B1", "ATS-480-A", "solid", "ATS-B1 branch from BUS-480-B1 lands on ATS-480-A."),
    edge("ATS-480-A", "PANEL-RPS-A", "solid", "ATS-AOUT route from ATS-480-A enters PANEL-RPS-A."),
    edge("BUS-480-C1", "ATS-480-B", "solid", "ATS-C1 branch from BUS-480-C1 lands on ATS-480-B."),
    edge("BUS-480-D1", "ATS-480-B", "solid", "ATS-D1 branch from BUS-480-D1 lands on ATS-480-B."),
    edge("ATS-480-B", "PANEL-RPS-B", "solid", "ATS-BOUT route from ATS-480-B enters PANEL-RPS-B."),
    edge("BAT-125A", "BUS-DC-125A", "solid", "BAT-125A connects to BUS-DC-125A."),
    edge("BUS-DC-125A", "INV-UPS-A", "solid", "BUS-DC-125A UPS-AIN feeder lands on INV-UPS-A."),
    edge("INV-UPS-A", "PANEL-RPS-A", "solid", "INV-UPS-A UPS-AOUT lands on PANEL-RPS-A."),
    edge("BAT-125B", "BUS-DC-125B", "solid", "BAT-125B connects to BUS-DC-125B."),
    edge("BUS-DC-125B", "INV-UPS-B", "solid", "BUS-DC-125B UPS-BIN feeder lands on INV-UPS-B."),
    edge("INV-UPS-B", "PANEL-RPS-B", "solid", "INV-UPS-B UPS-BOUT lands on PANEL-RPS-B."),
    edge("PANEL-RPS-A", "PANEL-SSPS", "dashed control", "Dashed RPS-A interlock enters the PANEL-SSPS control network."),
    edge("PANEL-RPS-B", "PANEL-SSPS", "dashed control", "Dashed RPS-B interlock enters the PANEL-SSPS control network."),
]

REMOVED_ATS_SSPS = [
    edge("ATS-480-A", "PANEL-SSPS", "dashed adjacent", "Removed: dashed ATS/interlock route lacks a clear ATS-to-SSPS terminal."),
    edge("ATS-480-B", "PANEL-SSPS", "dashed adjacent", "Removed: dashed ATS/interlock route lacks a clear ATS-to-SSPS terminal."),
]

ROUND_EDGES = {
    "round1_diego": FINAL_EDGES + REMOVED_ATS_SSPS,
    "round1_jennifer": FINAL_EDGES,
    "round2_diego": FINAL_EDGES,
    "round2_jennifer": FINAL_EDGES,
}


@dataclass
class TokenCallEstimate:
    document: int
    iteration: int
    round_name: str
    actor: str
    model_call: str
    model: str
    text_input_tokens_est: int
    image_input_tokens_est: int
    cached_input_tokens: str
    output_tokens_low: int
    output_tokens_expected: int
    output_tokens_high: int
    reasoning_tokens: str
    total_low: int
    total_expected: int
    total_high: int
    method: str


def write_nodes(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "node"])
        for i, node in enumerate(NODES, start=1):
            writer.writerow([f"N{i:03d}", node])


def write_edges(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["u", "v", "kind", "evidence"])
        for item in edges:
            writer.writerow(item)


def adjacency(edges: list[tuple[str, str, str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    seen: set[tuple[str, str]] = set()
    for u, v, _, _ in edges:
        if u not in index or v not in index:
            raise ValueError(f"Unknown node in edge: {u} -- {v}")
        if u == v:
            raise ValueError(f"Unexpected self-loop: {u}")
        key = tuple(sorted((u, v)))
        if key in seen:
            raise ValueError(f"Duplicate undirected edge: {u} -- {v}")
        seen.add(key)
        i, j = index[u], index[v]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def validate(matrix: list[list[int]]) -> dict[str, object]:
    n = len(matrix)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(n))
    edge_count = sum(sum(row) for row in matrix) // 2
    return {
        "node_count": n,
        "edge_count": edge_count,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
    }


def write_matrix(path: Path, edges: list[tuple[str, str, str, str]]) -> dict[str, object]:
    matrix = adjacency(edges)
    summary = validate(matrix)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node", *NODES])
        for node, row in zip(NODES, matrix):
            writer.writerow([node, *row])
    return summary


def image_token_estimate(path: Path) -> int:
    with Image.open(path) as im:
        width, height = im.size
    max_side = max(width, height)
    if max_side > 2048:
        scale = 2048 / max_side
        width = math.ceil(width * scale)
        height = math.ceil(height * scale)
    min_side = min(width, height)
    if min_side > 768:
        scale = 768 / min_side
        width = math.ceil(width * scale)
        height = math.ceil(height * scale)
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def count_text_tokens(text: str) -> int:
    if tiktoken is not None:
        for name in ("cl100k_base", "p50k_base", "r50k_base"):
            try:
                enc = tiktoken.get_encoding(name)
                return len(enc.encode(text))
            except Exception:
                continue
    return math.ceil(len(text) / 4)


def graph_text(edges: list[tuple[str, str, str, str]]) -> str:
    return "Nodes: " + ", ".join(NODES) + "\nEdges: " + "; ".join(f"{u}--{v}" for u, v, _, _ in edges)


def token_estimates() -> list[TokenCallEstimate]:
    common_instruction = (
        "Extract connectivity matrix from document 11 Raw + wires only. "
        "No GT, no GT-derived feedback, no OCR. Diego high recall, Jennifer precision. "
        "Return nodes, edges, evidence, round matrices, and token estimates."
    )
    image_sets = {
        "Main orchestration and visual spot checks": [
            "overview_raw.png",
            "top_sources_buses_raw_2x.png",
            "train_a_full_raw_2x.png",
            "bottom_dc_full_raw_2x.png",
            "train_a_loads_raw_2x.png",
            "train_b_loads_raw_2x.png",
            "ats_sps_center_raw_2x.png",
            "bottom_dc_left_raw_2x.png",
            "bottom_dc_center_raw_2x.png",
            "bottom_dc_right_raw_2x.png",
        ],
        "Diego R1": [
            "overview_raw.png",
            "top_sources_buses_raw_2x.png",
            "top_sources_buses_overlay_2x.png",
            "train_a_full_overlay_2x.png",
            "train_b_full_overlay_2x.png",
            "train_c_full_overlay_2x.png",
            "train_d_full_overlay_2x.png",
            "bottom_dc_full_overlay_2x.png",
            "ats_sps_center_overlay_2x.png",
            "rps_sps_interlocks_raw_2x.png",
            "notes_legend_raw_2x.png",
        ],
        "Jennifer R1": [
            "overview_raw.png",
            "top_sources_buses_raw_2x.png",
            "train_a_full_raw_2x.png",
            "train_b_full_raw_2x.png",
            "train_c_full_raw_2x.png",
            "train_d_full_raw_2x.png",
            "bottom_dc_full_raw_2x.png",
            "bottom_dc_left_raw_2x.png",
            "bottom_dc_center_raw_2x.png",
            "bottom_dc_right_raw_2x.png",
            "ats_sps_center_raw_2x.png",
            "rps_sps_interlocks_raw_2x.png",
            "notes_legend_raw_2x.png",
        ],
        "Diego R2": [
            "top_sources_buses_raw_2x.png",
            "train_a_full_raw_2x.png",
            "train_b_full_raw_2x.png",
            "train_c_full_raw_2x.png",
            "train_d_full_raw_2x.png",
            "bottom_dc_full_raw_2x.png",
            "ats_sps_center_raw_2x.png",
            "rps_sps_interlocks_raw_2x.png",
        ],
        "Jennifer R2": [
            "top_sources_buses_raw_2x.png",
            "train_a_full_raw_2x.png",
            "train_b_full_raw_2x.png",
            "train_c_full_raw_2x.png",
            "train_d_full_raw_2x.png",
            "bottom_dc_full_raw_2x.png",
            "ats_sps_center_raw_2x.png",
            "rps_sps_interlocks_raw_2x.png",
        ],
    }
    text_inputs = {
        "Main orchestration and visual spot checks": common_instruction + "\n" + graph_text(FINAL_EDGES),
        "Diego R1": common_instruction,
        "Jennifer R1": common_instruction + "\nDiego R1 proposal:\n" + graph_text(ROUND_EDGES["round1_diego"]),
        "Diego R2": common_instruction + "\nJennifer R1 refined graph:\n" + graph_text(FINAL_EDGES),
        "Jennifer R2": common_instruction + "\nDiego R2 saturation result and final candidate:\n" + graph_text(FINAL_EDGES),
    }
    outputs = {
        "Main orchestration and visual spot checks": (1800, 3500, 6500),
        "Diego R1": (6000, 11000, 18000),
        "Jennifer R1": (5000, 9000, 15000),
        "Diego R2": (900, 1800, 3500),
        "Jennifer R2": (900, 1800, 3500),
    }
    actors = {
        "Main orchestration and visual spot checks": "Main agent",
        "Diego R1": "Diego",
        "Jennifer R1": "Jennifer",
        "Diego R2": "Diego",
        "Jennifer R2": "Jennifer",
    }
    round_names = {
        "Main orchestration and visual spot checks": "orchestration",
        "Diego R1": "round1_diego",
        "Jennifer R1": "round1_jennifer",
        "Diego R2": "round2_diego",
        "Jennifer R2": "round2_jennifer",
    }
    rows: list[TokenCallEstimate] = []
    for call_name, images in image_sets.items():
        text_tokens = count_text_tokens(text_inputs[call_name])
        image_tokens = sum(image_token_estimate(CROPS / name) for name in images)
        low, expected, high = outputs[call_name]
        input_total = text_tokens + image_tokens
        rows.append(
            TokenCallEstimate(
                document=11,
                iteration=1,
                round_name=round_names[call_name],
                actor=actors[call_name],
                model_call=call_name,
                model="gpt-5.5 for subagents; main agent model not exposed",
                text_input_tokens_est=text_tokens,
                image_input_tokens_est=image_tokens,
                cached_input_tokens="not available",
                output_tokens_low=low,
                output_tokens_expected=expected,
                output_tokens_high=high,
                reasoning_tokens="not available",
                total_low=input_total + low,
                total_expected=input_total + expected,
                total_high=input_total + high,
                method="local text estimate + high-detail 512px image tile heuristic; no API key/usage object available",
            )
        )
    return rows


def write_token_estimates() -> dict[str, int]:
    rows = token_estimates()
    fields = list(TokenCallEstimate.__dataclass_fields__.keys())
    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)
    totals = {
        "input_text_tokens_est": sum(row.text_input_tokens_est for row in rows),
        "input_image_tokens_est": sum(row.image_input_tokens_est for row in rows),
        "total_low": sum(row.total_low for row in rows),
        "total_expected": sum(row.total_expected for row in rows),
        "total_high": sum(row.total_high for row in rows),
    }
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate\n\n")
        handle.write("Exact Responses token-counting and model usage objects were unavailable because no API key/usage metadata was exposed.\n\n")
        handle.write("Text input was locally estimated; image/file input used a high-detail tile heuristic. Cached and reasoning tokens are unavailable.\n\n")
        handle.write("| Document | Iteration | Input text est | Image/file input est | Low total | Expected total | High total |\n")
        handle.write("|---:|---:|---:|---:|---:|---:|---:|\n")
        handle.write(
            f"| 11 | 1 | {totals['input_text_tokens_est']} | {totals['input_image_tokens_est']} | "
            f"{totals['total_low']} | {totals['total_expected']} | {totals['total_high']} |\n"
        )
    return totals


def write_notes(validation: dict[str, object], round_validations: dict[str, dict[str, object]], totals: dict[str, int]) -> None:
    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Document 11 Connectivity Extraction Notes\n\n")
        handle.write("Only the raw schematic, wires mask, and wires mask overlay under `Raw + wires` were used for extraction. Existing result/validation files were not opened or used. No GT-derived feedback or off-the-shelf OCR was used.\n\n")
        handle.write("## Final Result\n\n")
        handle.write(f"- Nodes: {validation['node_count']}\n")
        handle.write(f"- Edges: {validation['edge_count']}\n")
        handle.write(f"- Symmetric matrix: {validation['symmetric']}\n")
        handle.write(f"- Diagonal zero: {validation['diagonal_zero']}\n\n")
        handle.write("## Round Progress\n\n")
        for name, summary in round_validations.items():
            handle.write(f"- `{name}`: {summary['node_count']} nodes, {summary['edge_count']} edges.\n")
        handle.write("\n## Precision Decisions\n\n")
        handle.write("- Removed `ATS-480-A--PANEL-SSPS` and `ATS-480-B--PANEL-SSPS`; dashed routing is adjacent/crossing without a clear ATS-to-SSPS terminal.\n")
        handle.write("- Kept `BUS-480-X1--BUS-480-X2` solid bus ties at `TIE-X12`; no separate `TIE-X12` nodes were added.\n")
        handle.write("- Kept relay-27, I/C, ground, and DC bus assignments that terminate at visible dots or panel terminals.\n")
        handle.write("- Treated labels such as `FDR-*`, `52-*`, `LC-*`, `BC-*`, `DC-*125`, `ATS-*OUT`, `UPS-*IN/OUT`, and `SSPS-A/B/C/D` as route labels, not component nodes.\n\n")
        handle.write("## Token Estimate\n\n")
        handle.write(f"- Expected total tokens estimated: {totals['total_expected']} (low {totals['total_low']}, high {totals['total_high']}).\n")


def write_manifest(validation: dict[str, object], round_validations: dict[str, dict[str, object]], totals: dict[str, int]) -> None:
    manifest = {
        "document": 11,
        "iteration": 1,
        "resource_root": str(BASE),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "final_validation": validation,
        "round_validations": round_validations,
        "final_files": ["final_nodes.csv", "final_edges.csv", "connectivity_matrix.csv"],
        "round_prefixes": list(ROUND_EDGES.keys()),
        "token_estimate_totals": totals,
    }
    (RESULTS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    round_validations: dict[str, dict[str, object]] = {}
    for prefix, edges in ROUND_EDGES.items():
        write_nodes(RESULTS / f"{prefix}_nodes.csv")
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        round_validations[prefix] = write_matrix(RESULTS / f"{prefix}_matrix.csv", edges)
    write_nodes(RESULTS / "final_nodes.csv")
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    validation = write_matrix(RESULTS / "connectivity_matrix.csv", FINAL_EDGES)
    totals = write_token_estimates()
    write_notes(validation, round_validations, totals)
    write_manifest(validation, round_validations, totals)
    print(json.dumps({"validation": validation, "round_validations": round_validations, "token_estimate_totals": totals}, indent=2))


if __name__ == "__main__":
    main()
