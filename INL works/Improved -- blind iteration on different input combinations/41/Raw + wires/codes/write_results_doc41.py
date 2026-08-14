from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    import tiktoken
except Exception:  # pragma: no cover - estimate fallback
    tiktoken = None

try:
    from PIL import Image
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PIL/Pillow is required for image-size estimates: {exc}")


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires")
CROPS = BASE / "codes" / "crops"
RESULTS = BASE / "results"


NODES = [
    "OFFSITE_A_161KV",
    "TR_1A",
    "GND_1E",
    "CB_101",
    "BUS_1A_4160",
    "EDG_1A",
    "CB_105",
    "CB_TIE_1AB",
    "BUS_1B_4160",
    "CB_102",
    "TR_1B",
    "OFFSITE_B_161KV",
    "EDG_1B",
    "CB_106",
    "TR_LC_1A",
    "CB_201",
    "BUS_480A",
    "MCC_1A",
    "PUMP_CCW_103A",
    "MCC_1C",
    "FAN_CRHV_104A",
    "TR_SAF_1A",
    "CB_203",
    "BUS_480E1A",
    "MCC_ESS_A",
    "PUMP_SI_101A",
    "PUMP_RHR_102A",
    "MOV_1201A",
    "TR_LC_1B",
    "CB_202",
    "BUS_480B",
    "MCC_1B",
    "PUMP_CCW_103B",
    "MCC_1D",
    "FAN_CRHV_104B",
    "TR_SAF_1B",
    "CB_204",
    "BUS_480E1B",
    "MCC_ESS_B",
    "PUMP_SI_101B",
    "PUMP_RHR_102B",
    "MOV_1201B",
    "RELAY_K86A",
    "PANEL_RPS_A",
    "JB_ESF_01",
    "RELAY_K86B",
    "PANEL_RPS_B",
    "CHGR_125A",
    "DC_BUS_125A",
    "BAT_125A",
    "INV_120A",
    "UPS_BUS_A",
    "INST_RACK_1",
    "CHGR_125B",
    "DC_BUS_125B",
    "BAT_125B",
    "INV_120B",
    "UPS_BUS_B",
]


EDGES = [
    ("OFFSITE_A_161KV", "TR_1A", "solid", "Offsite A source lead terminates at TR-1A primary."),
    ("TR_1A", "GND_1E", "ground", "Grounding conductor from TR-1A to named ground node GND-1E."),
    ("TR_1A", "CB_101", "solid", "TR-1A secondary feeder terminates at CB-101."),
    ("CB_101", "BUS_1A_4160", "solid", "CB-101 output lands on BUS-1A 4160 V."),
    ("EDG_1A", "CB_105", "solid", "EDG-1A generator feeder enters CB-105."),
    ("CB_105", "BUS_1A_4160", "solid", "CB-105 incoming feeder lands on BUS-1A."),
    ("BUS_1A_4160", "CB_TIE_1AB", "solid", "BUS-1A is drawn to tie breaker CB-TIE-1AB."),
    ("CB_TIE_1AB", "BUS_1B_4160", "solid", "Tie breaker connects to BUS-1B; breaker is marked N.O. but drawn connected."),
    ("BUS_1B_4160", "CB_102", "solid", "BUS-1B terminates at CB-102."),
    ("CB_102", "TR_1B", "solid", "CB-102 feeder connects to TR-1B."),
    ("TR_1B", "OFFSITE_B_161KV", "solid", "TR-1B primary connects to Offsite B source."),
    ("EDG_1B", "CB_106", "solid", "EDG-1B generator feeder enters CB-106."),
    ("CB_106", "BUS_1B_4160", "solid", "CB-106 incoming feeder lands on BUS-1B."),
    ("BUS_1A_4160", "TR_LC_1A", "solid", "Vertical feeder from BUS-1A to TR-LC-1A."),
    ("TR_LC_1A", "CB_201", "solid", "TR-LC-1A secondary connects to CB-201."),
    ("CB_201", "BUS_480A", "solid", "CB-201 output connects to BUS-480A."),
    ("BUS_480A", "MCC_1A", "solid", "BUS-480A drop feeds MCC-1A."),
    ("MCC_1A", "PUMP_CCW_103A", "solid", "MCC-1A feeder terminates at PUMP-CCW-103A."),
    ("BUS_480A", "MCC_1C", "solid", "BUS-480A drop feeds MCC-1C."),
    ("MCC_1C", "FAN_CRHV_104A", "solid", "MCC-1C feeder terminates at FAN-CRHV-104A."),
    ("BUS_1A_4160", "TR_SAF_1A", "solid", "Vertical feeder from BUS-1A to TR-SAF-1A."),
    ("TR_SAF_1A", "CB_203", "solid", "TR-SAF-1A secondary connects to CB-203."),
    ("CB_203", "BUS_480E1A", "solid", "CB-203 output connects to BUS-480E1A."),
    ("BUS_480E1A", "MCC_ESS_A", "solid", "BUS-480E1A drop feeds MCC-ESS-A."),
    ("MCC_ESS_A", "PUMP_SI_101A", "solid", "MCC-ESS-A feeder terminates at PUMP-SI-101A."),
    ("MCC_ESS_A", "PUMP_RHR_102A", "solid", "MCC-ESS-A feeder terminates at PUMP-RHR-102A."),
    ("MCC_ESS_A", "MOV_1201A", "solid", "MCC-ESS-A feeder terminates at MOV-1201A."),
    ("BUS_1B_4160", "TR_LC_1B", "solid", "Vertical feeder from BUS-1B to TR-LC-1B."),
    ("TR_LC_1B", "CB_202", "solid", "TR-LC-1B secondary connects to CB-202."),
    ("CB_202", "BUS_480B", "solid", "CB-202 output connects to BUS-480B."),
    ("BUS_480B", "MCC_1B", "solid", "BUS-480B drop feeds MCC-1B."),
    ("MCC_1B", "PUMP_CCW_103B", "solid", "MCC-1B feeder terminates at PUMP-CCW-103B."),
    ("BUS_480B", "MCC_1D", "solid", "BUS-480B drop feeds MCC-1D."),
    ("MCC_1D", "FAN_CRHV_104B", "solid", "MCC-1D feeder terminates at FAN-CRHV-104B."),
    ("BUS_1B_4160", "TR_SAF_1B", "solid", "Vertical feeder from BUS-1B to TR-SAF-1B."),
    ("TR_SAF_1B", "CB_204", "solid", "TR-SAF-1B secondary connects to CB-204."),
    ("CB_204", "BUS_480E1B", "solid", "CB-204 output connects to BUS-480E1B."),
    ("BUS_480E1B", "MCC_ESS_B", "solid", "BUS-480E1B drop feeds MCC-ESS-B."),
    ("MCC_ESS_B", "PUMP_SI_101B", "solid", "MCC-ESS-B feeder terminates at PUMP-SI-101B."),
    ("MCC_ESS_B", "PUMP_RHR_102B", "solid", "MCC-ESS-B feeder terminates at PUMP-RHR-102B."),
    ("MCC_ESS_B", "MOV_1201B", "solid", "MCC-ESS-B feeder terminates at MOV-1201B."),
    ("BUS_480A", "CHGR_125A", "solid route", "FDR A-DC route leaves BUS-480A and terminates at CHGR-125A AC input."),
    ("CHGR_125A", "DC_BUS_125A", "solid", "CHGR-125A DC output connects to DC-BUS-125A."),
    ("DC_BUS_125A", "BAT_125A", "solid", "BAT-125A lead connects to DC-BUS-125A."),
    ("DC_BUS_125A", "INV_120A", "solid", "DC-BUS-125A connects to INV-120A input."),
    ("INV_120A", "UPS_BUS_A", "solid", "INV-120A output connects to UPS-BUS-A."),
    ("UPS_BUS_A", "INST_RACK_1", "solid", "UPS-BUS-A feeder drops to INST-RACK-1."),
    ("UPS_BUS_A", "PANEL_RPS_A", "solid", "UPS-BUS-A branch feeds PANEL-RPS-A bottom port."),
    ("BUS_480B", "CHGR_125B", "solid route", "FDR B-DC route is traced from BUS-480B side to CHGR-125B AC input; no ESS-B terminal dot."),
    ("CHGR_125B", "DC_BUS_125B", "solid", "CHGR-125B DC output connects to DC-BUS-125B."),
    ("DC_BUS_125B", "BAT_125B", "solid", "BAT-125B lead connects to DC-BUS-125B."),
    ("DC_BUS_125B", "INV_120B", "solid", "DC-BUS-125B connects to INV-120B input."),
    ("INV_120B", "UPS_BUS_B", "solid", "INV-120B output connects to UPS-BUS-B."),
    ("UPS_BUS_B", "PANEL_RPS_B", "solid", "UPS-BUS-B branch feeds PANEL-RPS-B bottom port."),
    ("CB_105", "RELAY_K86A", "dashed control", "CTRL-86A dashed route terminates at CB-105 and K86A relay port."),
    ("RELAY_K86A", "PANEL_RPS_A", "dashed control", "Dashed interlock from K86A relay to PANEL-RPS-A side port."),
    ("PANEL_RPS_A", "JB_ESF_01", "dashed control", "PANEL-RPS-A top dashed interlock terminates at JB-ESF-01."),
    ("JB_ESF_01", "PANEL_RPS_B", "dashed control", "JB-ESF-01 dashed interlock terminates at PANEL-RPS-B top port."),
    ("PANEL_RPS_B", "RELAY_K86B", "dashed control", "PANEL-RPS-B side dashed interlock terminates at K86B relay."),
    ("RELAY_K86B", "CB_106", "dashed control", "K86B relay dashed route terminates at CB-106 lower port."),
]


REMOVED_CANDIDATES = [
    ("BUS_480E1A", "CHGR_125A", "No terminal dot or termination at BUS-480E1A; charger route is from BUS-480A."),
    ("BUS_480E1B", "CHGR_125B", "Route passes near ESS-B without terminal dot; upstream kept as BUS-480B."),
    ("UPS_BUS_B", "INST_RACK_1", "Only A-side UPS feed visibly drops into INST-RACK-1."),
    ("LOAD_TO_RPS_CROSSINGS", "RPS_CONTROL", "Crossings near loads have no terminal dots; not modeled as edges."),
    ("PT_UV_SEQ", "INST_RACK_1", "PT/UV/SEQ are internal rack markings, not independently externally wired nodes."),
    ("CTRL_86A_OR_B", "ANY", "CTRL labels are route labels, not component/node names."),
]


ROUND_DEFINITIONS = [
    ("round1_diego", "Diego", "Round 1 high-recall extraction", EDGES),
    ("round1_jennifer", "Jennifer", "Round 1 precision refinement; graph unchanged, rejected overconnections", EDGES),
    ("round2_diego", "Diego", "Round 2 saturation check; populated after saturation agreement", EDGES),
    ("round2_jennifer", "Jennifer", "Round 2 final precision confirmation; populated after final agreement", EDGES),
]


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


def ensure_results() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)


def node_ids() -> dict[str, str]:
    return {node: f"N{i:02d}" for i, node in enumerate(NODES, start=1)}


def write_nodes(path: Path) -> None:
    ids = node_ids()
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "node"])
        for node in NODES:
            writer.writerow([ids[node], node])


def write_edges(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["u", "v", "kind", "evidence"])
        for edge in edges:
            writer.writerow(edge)


def adjacency(edges: list[tuple[str, str, str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for u, v, _, _ in edges:
        if u not in index:
            raise ValueError(f"Unknown edge node: {u}")
        if v not in index:
            raise ValueError(f"Unknown edge node: {v}")
        if u == v:
            raise ValueError(f"Unexpected self-loop: {u}")
        i = index[u]
        j = index[v]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def validate_matrix(matrix: list[list[int]]) -> dict[str, object]:
    n = len(matrix)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(n))
    ones = sum(sum(row) for row in matrix)
    return {
        "node_count": n,
        "edge_count": ones // 2,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
    }


def write_matrix(path: Path, edges: list[tuple[str, str, str, str]]) -> dict[str, object]:
    matrix = adjacency(edges)
    summary = validate_matrix(matrix)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *NODES])
        for node, row in zip(NODES, matrix):
            writer.writerow([node, *row])
    return summary


def image_token_estimate(path: Path) -> int:
    """Approximate high-detail image input tokens.

    The exact Responses tokenizer was unavailable. This uses the documented style
    of tiled image charging used by current OpenAI vision models: scale within a
    2048 square, then scale shortest side to 768, then count 512px tiles at
    170 tokens each plus an 85-token base. GPT-5.5 accounting may differ.
    """

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
    if tiktoken is None:
        return math.ceil(len(text) / 4)
    for name in ("cl100k_base", "p50k_base", "r50k_base"):
        try:
            encoding = tiktoken.get_encoding(name)
            return len(encoding.encode(text))
        except Exception:
            continue
    return math.ceil(len(text) / 4)


def joined_graph_text() -> str:
    edge_text = "; ".join(f"{u}--{v}" for u, v, _, _ in EDGES)
    return "Nodes: " + ", ".join(NODES) + "\nEdges: " + edge_text


def token_estimates() -> list[TokenCallEstimate]:
    common_instruction = (
        "Extract an undirected connectivity matrix from the raw schematic and "
        "wire aids. Use only Raw + wires, no GT, no off-the-shelf OCR. "
        "Diego is high recall; Jennifer is precision review. Return nodes, "
        "edges, evidence, ambiguities, and matrices where requested."
    )
    image_sets = {
        "Main orchestration and visual spot checks": [
            "overview_raw.png",
            "right_480_loads_overlay_2x.png",
            "right_vital_dc_overlay_2x.png",
            "bottom_dc_ups_full_overlay_2x.png",
            "left_480_loads_overlay_2x.png",
            "right_480_loads_raw_2x.png",
        ],
        "Diego R1": [
            "overview_raw.png",
            "top_switchgear_full_raw_2x.png",
            "top_switchgear_full_overlay_2x.png",
            "left_480_loads_overlay_2x.png",
            "right_480_loads_overlay_2x.png",
            "rps_interlocks_center_raw_2x.png",
            "bottom_dc_ups_full_overlay_2x.png",
            "notes_raw_2x.png",
            "legend_reference_raw_2x.png",
        ],
        "Jennifer R1": [
            "overview_raw.png",
            "top_switchgear_full_raw_2x.png",
            "top_switchgear_full_overlay_2x.png",
            "left_480_loads_overlay_2x.png",
            "right_480_loads_overlay_2x.png",
            "bottom_dc_ups_full_overlay_2x.png",
            "rps_interlocks_center_raw_2x.png",
            "rps_interlocks_center_overlay_2x.png",
            "instrument_rack_ups_raw_2x.png",
            "notes_raw_2x.png",
            "legend_reference_raw_2x.png",
        ],
        "Diego R2": [
            "top_switchgear_full_overlay_2x.png",
            "left_480_loads_overlay_2x.png",
            "right_480_loads_overlay_2x.png",
            "bottom_dc_ups_full_overlay_2x.png",
            "rps_interlocks_center_overlay_2x.png",
            "instrument_rack_ups_raw_2x.png",
        ],
        "Jennifer R2": [
            "top_switchgear_full_overlay_2x.png",
            "left_480_loads_overlay_2x.png",
            "right_480_loads_overlay_2x.png",
            "bottom_dc_ups_full_overlay_2x.png",
            "rps_interlocks_center_overlay_2x.png",
            "instrument_rack_ups_raw_2x.png",
        ],
    }
    text_inputs = {
        "Main orchestration and visual spot checks": common_instruction + "\n" + joined_graph_text(),
        "Diego R1": common_instruction,
        "Jennifer R1": common_instruction + "\nDiego R1 proposal:\n" + joined_graph_text(),
        "Diego R2": common_instruction + "\nJennifer R1 decisions:\n" + joined_graph_text(),
        "Jennifer R2": common_instruction + "\nDiego R2 saturation response plus agreed graph:\n" + joined_graph_text(),
    }
    outputs = {
        "Main orchestration and visual spot checks": (1200, 2200, 4200),
        "Diego R1": (4500, 8500, 14000),
        "Jennifer R1": (3500, 7000, 12000),
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
    estimates: list[TokenCallEstimate] = []
    for call_name, images in image_sets.items():
        text_tokens = count_text_tokens(text_inputs[call_name])
        image_tokens = sum(image_token_estimate(CROPS / image) for image in images)
        low, expected, high = outputs[call_name]
        input_total = text_tokens + image_tokens
        estimates.append(
            TokenCallEstimate(
                document=41,
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
                method="tiktoken text estimate + tiled high-detail image-token heuristic; no API key/usage object available",
            )
        )
    return estimates


def write_token_estimates() -> dict[str, int]:
    estimates = token_estimates()
    path = RESULTS / "token_usage_estimates.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(TokenCallEstimate.__dataclass_fields__.keys()))
        writer.writeheader()
        for item in estimates:
            writer.writerow(item.__dict__)
    totals = {
        "input_text_tokens_est": sum(i.text_input_tokens_est for i in estimates),
        "input_image_tokens_est": sum(i.image_input_tokens_est for i in estimates),
        "total_low": sum(i.total_low for i in estimates),
        "total_expected": sum(i.total_expected for i in estimates),
        "total_high": sum(i.total_high for i in estimates),
    }
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Token Usage Estimate\n\n")
        f.write("Exact OpenAI Responses token counting and response usage objects were unavailable in this environment because no API key/usage metadata was exposed.\n\n")
        f.write("Method: local text tokens were estimated with `tiktoken`; image tokens were estimated from image dimensions with a high-detail 512px tile heuristic. Cached input and reasoning tokens are marked unavailable.\n\n")
        f.write("| Document | Iteration | Input text est | Image/file input est | Low total | Expected total | High total |\n")
        f.write("|---:|---:|---:|---:|---:|---:|---:|\n")
        f.write(
            f"| 41 | 1 | {totals['input_text_tokens_est']} | {totals['input_image_tokens_est']} | "
            f"{totals['total_low']} | {totals['total_expected']} | {totals['total_high']} |\n"
        )
    return totals


def write_notes(validation: dict[str, object], totals: dict[str, int]) -> None:
    with (RESULTS / "round_notes.md").open("w", encoding="utf-8") as f:
        f.write("# Document 41 Connectivity Extraction Notes\n\n")
        f.write("Only files under `Raw + wires` were used. No Ground Truth or GT-derived feedback was used. No off-the-shelf OCR was used.\n\n")
        f.write("## Saturated Result\n\n")
        f.write(f"- Nodes: {validation['node_count']}\n")
        f.write(f"- Edges: {validation['edge_count']}\n")
        f.write(f"- Symmetric matrix: {validation['symmetric']}\n")
        f.write(f"- Diagonal zero: {validation['diagonal_zero']}\n\n")
        f.write("## Precision Decisions\n\n")
        for u, v, reason in REMOVED_CANDIDATES:
            f.write(f"- Removed/not modeled `{u}--{v}`: {reason}\n")
        f.write("\n## Round Progress\n\n")
        f.write("- Diego R1 proposed the full 58-node graph; the saved unique undirected edge list validates to 60 edges.\n")
        f.write("- Jennifer R1 kept the graph and rejected unsupported overconnections.\n")
        f.write("- Diego R2 and Jennifer R2 are saturation confirmations; their matrix files preserve the agreed graph unless manually revised after review.\n\n")
        f.write("## Token Estimate Summary\n\n")
        f.write(
            f"- Total expected tokens estimated: {totals['total_expected']} "
            f"(low {totals['total_low']}, high {totals['total_high']}).\n"
        )


def write_manifest(validation: dict[str, object], totals: dict[str, int]) -> None:
    manifest = {
        "document": 41,
        "iteration": 1,
        "resource_root": str(BASE),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "node_count": validation["node_count"],
        "edge_count": validation["edge_count"],
        "symmetric": validation["symmetric"],
        "diagonal_zero": validation["diagonal_zero"],
        "round_files": [
            f"{prefix}_{suffix}.csv"
            for prefix, _, _, _ in ROUND_DEFINITIONS
            for suffix in ("nodes", "edges", "matrix")
        ],
        "final_files": ["final_nodes.csv", "final_edges.csv", "connectivity_matrix.csv"],
        "token_estimate_totals": totals,
    }
    (RESULTS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    ensure_results()
    last_validation: dict[str, object] | None = None
    for prefix, _, _, edges in ROUND_DEFINITIONS:
        write_nodes(RESULTS / f"{prefix}_nodes.csv")
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        last_validation = write_matrix(RESULTS / f"{prefix}_matrix.csv", edges)

    write_nodes(RESULTS / "final_nodes.csv")
    write_edges(RESULTS / "final_edges.csv", EDGES)
    validation = write_matrix(RESULTS / "connectivity_matrix.csv", EDGES)
    if last_validation != validation:
        raise ValueError("Round and final validation summaries diverged unexpectedly.")
    totals = write_token_estimates()
    write_notes(validation, totals)
    write_manifest(validation, totals)
    print(json.dumps({"validation": validation, "token_estimate_totals": totals}, indent=2))


if __name__ == "__main__":
    main()
