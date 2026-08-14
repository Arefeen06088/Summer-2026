from __future__ import annotations

import csv
import math
from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\4\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


NODES = [
    "US-345A",
    "US-230B",
    "BUS-480-RB1",
    "BUS-480-RB2",
    "BUS-480-LCA",
    "BUS-480-LCB",
    "BUS-125DCA",
    "BUS-125DCB",
    "BUS-UPS-A",
    "BUS-UPS-B",
    "GND-NG-A",
    "GND-NG-B",
    "CB-UAT-A",
    "TR-UAT-1",
    "CB-IN-A",
    "EDG-1A",
    "CB-DG-A",
    "CB-SAT-B",
    "TR-SAT-2",
    "CB-IN-B",
    "EDG-1B",
    "CB-DG-B",
    "CB-TIE-480",
    "CB-F101",
    "OL-F101",
    "PMP-SI-1A",
    "CB-F102",
    "OL-F102",
    "PMP-RHR-1A",
    "CB-F103",
    "OL-F103",
    "FAN-CTMT-1A",
    "CB-F104",
    "OL-F104",
    "MOV-RC-104",
    "CB-F105",
    "OL-F105",
    "PMP-CCW-1A",
    "CB-F106",
    "OL-F106",
    "MOV-IA-106",
    "CB-F107",
    "OL-F107",
    "FAN-AHU-1A",
    "CB-F108",
    "OL-F108",
    "PMP-CS-1A",
    "CB-F109",
    "OL-F109",
    "MOV-EF-109",
    "CB-F110",
    "OL-F110",
    "HTR-PZR-1",
    "CB-F111",
    "OL-F111",
    "PMP-SI-1B",
    "CB-F112",
    "OL-F112",
    "PMP-RHR-1B",
    "CB-F113",
    "OL-F113",
    "FAN-CTMT-1B",
    "CB-F114",
    "OL-F114",
    "MOV-RC-114",
    "CB-F115",
    "OL-F115",
    "PNL-SPARE-F15",
    "CB-LC-A",
    "TR-LC-A",
    "CB-LC-A2",
    "CB-LC-B",
    "TR-LC-B",
    "CB-LC-B2",
    "CB-LC-TIE",
    "CB-A201",
    "OL-201",
    "PMP-SW-2A",
    "CB-A202",
    "OL-202",
    "PMP-CVC-2A",
    "CB-A203",
    "OL-203",
    "MOV-SI-203",
    "CB-A204",
    "OL-204",
    "FAN-CR-2A",
    "CB-A205",
    "OL-205",
    "HTR-BATT-A",
    "CB-B206",
    "OL-206",
    "PMP-SW-2B",
    "CB-B207",
    "OL-207",
    "PMP-CVC-2B",
    "CB-B208",
    "OL-208",
    "MOV-SI-208",
    "CB-B209",
    "OL-209",
    "PNL-LTG-209",
    "CB-CHG-A",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "RPS-TRAIN-A",
    "ESFAS-TRAIN-A",
    "RELAY-K701",
    "TB-ESF-A",
    "ANN-CP-A",
    "CB-CHG-B",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "RPS-TRAIN-B",
    "ESFAS-TRAIN-B",
    "RELAY-K702",
    "TB-ESF-B",
    "REC-SER-01",
]


def chain(*items: str) -> list[tuple[str, str]]:
    return list(zip(items, items[1:]))


def sorted_edge(a: str, b: str) -> tuple[str, str]:
    if a not in NODES or b not in NODES:
        raise ValueError(f"Unknown node in edge: {a!r}, {b!r}")
    return tuple(sorted((a, b)))


FINAL_EDGE_PAIRS = [
    *chain("US-345A", "CB-UAT-A", "TR-UAT-1", "CB-IN-A", "BUS-480-RB1"),
    *chain("EDG-1A", "CB-DG-A", "BUS-480-RB1"),
    *chain("US-230B", "CB-SAT-B", "TR-SAT-2", "CB-IN-B", "BUS-480-RB2"),
    *chain("EDG-1B", "CB-DG-B", "BUS-480-RB2"),
    *chain("BUS-480-RB1", "CB-TIE-480", "BUS-480-RB2"),
    *chain("BUS-480-RB1", "CB-F101", "OL-F101", "PMP-SI-1A"),
    *chain("BUS-480-RB2", "CB-F102", "OL-F102", "PMP-RHR-1A"),
    *chain("BUS-480-RB1", "CB-F103", "OL-F103", "FAN-CTMT-1A"),
    *chain("BUS-480-RB2", "CB-F104", "OL-F104", "MOV-RC-104"),
    *chain("BUS-480-RB1", "CB-F105", "OL-F105", "PMP-CCW-1A"),
    *chain("BUS-480-RB2", "CB-F106", "OL-F106", "MOV-IA-106"),
    *chain("BUS-480-RB1", "CB-F107", "OL-F107", "FAN-AHU-1A"),
    *chain("BUS-480-RB2", "CB-F108", "OL-F108", "PMP-CS-1A"),
    *chain("BUS-480-RB1", "CB-F109", "OL-F109", "MOV-EF-109"),
    *chain("BUS-480-RB2", "CB-F110", "OL-F110", "HTR-PZR-1"),
    *chain("BUS-480-RB1", "CB-F111", "OL-F111", "PMP-SI-1B"),
    *chain("BUS-480-RB2", "CB-F112", "OL-F112", "PMP-RHR-1B"),
    *chain("BUS-480-RB1", "CB-F113", "OL-F113", "FAN-CTMT-1B"),
    *chain("BUS-480-RB2", "CB-F114", "OL-F114", "MOV-RC-114"),
    *chain("BUS-480-RB1", "CB-F115", "OL-F115", "PNL-SPARE-F15"),
    *chain("BUS-480-RB1", "CB-LC-A", "TR-LC-A", "CB-LC-A2", "BUS-480-LCA"),
    ("TR-LC-A", "GND-NG-A"),
    *chain("BUS-480-RB2", "CB-LC-B", "TR-LC-B", "CB-LC-B2", "BUS-480-LCB"),
    ("TR-LC-B", "GND-NG-B"),
    *chain("BUS-480-LCA", "CB-LC-TIE", "BUS-480-LCB"),
    *chain("BUS-480-LCA", "CB-A201", "OL-201", "PMP-SW-2A"),
    *chain("BUS-480-LCA", "CB-A202", "OL-202", "PMP-CVC-2A"),
    *chain("BUS-480-LCA", "CB-A203", "OL-203", "MOV-SI-203"),
    *chain("BUS-480-LCA", "CB-A204", "OL-204", "FAN-CR-2A"),
    *chain("BUS-480-LCA", "CB-A205", "OL-205", "HTR-BATT-A"),
    *chain("BUS-480-LCB", "CB-B206", "OL-206", "PMP-SW-2B"),
    *chain("BUS-480-LCB", "CB-B207", "OL-207", "PMP-CVC-2B"),
    *chain("BUS-480-LCB", "CB-B208", "OL-208", "MOV-SI-208"),
    *chain("BUS-480-LCB", "CB-B209", "OL-209", "PNL-LTG-209"),
    *chain("BUS-480-LCA", "CB-CHG-A", "CHG-125A"),
    ("CHG-125A", "BAT-125A"),
    *chain("CHG-125A", "BUS-125DCA", "INV-120A", "BUS-UPS-A"),
    ("BUS-UPS-A", "RPS-TRAIN-A"),
    ("BUS-UPS-A", "ESFAS-TRAIN-A"),
    *chain("BUS-480-LCB", "CB-CHG-B", "CHG-125B"),
    ("CHG-125B", "BAT-125B"),
    *chain("CHG-125B", "BUS-125DCB", "INV-120B", "BUS-UPS-B"),
    ("BUS-UPS-B", "RPS-TRAIN-B"),
    ("BUS-UPS-B", "ESFAS-TRAIN-B"),
    ("RPS-TRAIN-A", "RELAY-K701"),
    ("ESFAS-TRAIN-A", "RELAY-K701"),
    ("RPS-TRAIN-B", "RELAY-K702"),
    ("ESFAS-TRAIN-B", "RELAY-K702"),
    ("RELAY-K701", "TB-ESF-A"),
    ("RELAY-K702", "TB-ESF-B"),
    ("ANN-CP-A", "TB-ESF-A"),
    ("ANN-CP-A", "REC-SER-01"),
    ("REC-SER-01", "TB-ESF-B"),
]

FINAL_EDGES = {sorted_edge(a, b) for a, b in FINAL_EDGE_PAIRS}

DIEGO_COMMITTED_EDGES = FINAL_EDGES - {
    sorted_edge("TR-LC-A", "GND-NG-A"),
    sorted_edge("TR-LC-B", "GND-NG-B"),
    sorted_edge("RELAY-K701", "TB-ESF-A"),
    sorted_edge("RELAY-K702", "TB-ESF-B"),
    sorted_edge("ANN-CP-A", "REC-SER-01"),
}

DIEGO_REJECTED_HIGH_RECALL = {
    sorted_edge("RELAY-K701", "CB-LC-B"),
    sorted_edge("RELAY-K702", "CB-LC-B2"),
    sorted_edge("BUS-UPS-B", "ANN-CP-A"),
    sorted_edge("BUS-UPS-B", "REC-SER-01"),
}

DIEGO_PLUS_UNCERTAIN_EDGES = FINAL_EDGES | DIEGO_REJECTED_HIGH_RECALL

EDGE_EVIDENCE = {
    sorted_edge("US-345A", "CB-UAT-A"): "solid Train A utility source lead",
    sorted_edge("CB-UAT-A", "TR-UAT-1"): "solid source feeder",
    sorted_edge("TR-UAT-1", "CB-IN-A"): "solid transformer outgoing feeder",
    sorted_edge("CB-IN-A", "BUS-480-RB1"): "incomer dots onto BUS-480-RB1",
    sorted_edge("EDG-1A", "CB-DG-A"): "solid EDG A lead",
    sorted_edge("CB-DG-A", "BUS-480-RB1"): "breaker output dots onto BUS-480-RB1",
    sorted_edge("US-230B", "CB-SAT-B"): "solid Train B utility source lead",
    sorted_edge("CB-SAT-B", "TR-SAT-2"): "solid source feeder",
    sorted_edge("TR-SAT-2", "CB-IN-B"): "solid transformer outgoing feeder",
    sorted_edge("CB-IN-B", "BUS-480-RB2"): "incomer dots onto BUS-480-RB2",
    sorted_edge("EDG-1B", "CB-DG-B"): "solid EDG B lead",
    sorted_edge("CB-DG-B", "BUS-480-RB2"): "breaker output dots onto BUS-480-RB2",
    sorted_edge("BUS-480-RB1", "CB-TIE-480"): "upper tie terminal",
    sorted_edge("CB-TIE-480", "BUS-480-RB2"): "lower tie terminal",
    sorted_edge("BUS-480-RB1", "CB-LC-A"): "LC-A feeder leaves RB1; crossing at RB2 has no dot",
    sorted_edge("CB-LC-A", "TR-LC-A"): "solid LC-A feeder",
    sorted_edge("TR-LC-A", "CB-LC-A2"): "solid LC-A feeder",
    sorted_edge("CB-LC-A2", "BUS-480-LCA"): "LC-A feeder lands on BUS-480-LCA dot",
    sorted_edge("TR-LC-A", "GND-NG-A"): "named ground symbol tied to transformer",
    sorted_edge("BUS-480-RB2", "CB-LC-B"): "LC-B feeder leaves RB2 side",
    sorted_edge("CB-LC-B", "TR-LC-B"): "solid LC-B feeder",
    sorted_edge("TR-LC-B", "CB-LC-B2"): "solid LC-B feeder",
    sorted_edge("CB-LC-B2", "BUS-480-LCB"): "LC-B feeder lands on BUS-480-LCB dot",
    sorted_edge("TR-LC-B", "GND-NG-B"): "named ground symbol tied to transformer",
    sorted_edge("BUS-480-LCA", "CB-LC-TIE"): "left LC tie terminal",
    sorted_edge("CB-LC-TIE", "BUS-480-LCB"): "right LC tie terminal",
    sorted_edge("BUS-480-LCA", "CB-CHG-A"): "DCA-01 spur from LC-A side",
    sorted_edge("BUS-480-LCB", "CB-CHG-B"): "DCB-01 spur from LC-B bus dot",
    sorted_edge("RPS-TRAIN-A", "RELAY-K701"): "dashed control line terminates at RPS-A and relay",
    sorted_edge("ESFAS-TRAIN-A", "RELAY-K701"): "dashed control line terminates at ESFAS-A and relay",
    sorted_edge("RPS-TRAIN-B", "RELAY-K702"): "dashed control line terminates at RPS-B and relay",
    sorted_edge("ESFAS-TRAIN-B", "RELAY-K702"): "dashed control line terminates at ESFAS-B and relay",
    sorted_edge("RELAY-K701", "TB-ESF-A"): "dashed relay line visibly lands on terminal block",
    sorted_edge("RELAY-K702", "TB-ESF-B"): "dashed relay line visibly lands on terminal block",
    sorted_edge("ANN-CP-A", "TB-ESF-A"): "dashed SIGA-01 line terminates at both named boxes",
    sorted_edge("ANN-CP-A", "REC-SER-01"): "vertical dashed line terminates at both named panels",
    sorted_edge("REC-SER-01", "TB-ESF-B"): "dashed SIGB-01 line terminates at both named boxes",
}


def complete_edge_evidence() -> None:
    for edge in FINAL_EDGES:
        a, b = edge
        if edge in EDGE_EVIDENCE:
            continue
        if a.startswith("BUS-480-RB") and b.startswith("CB-F"):
            EDGE_EVIDENCE[edge] = "visible feeder drop from upper 480 V bus"
        elif a.startswith("BUS-480-LC") and (b.startswith("CB-A") or b.startswith("CB-B")):
            EDGE_EVIDENCE[edge] = "visible feeder drop from lower load-center bus"
        elif a.startswith("CB-F") and b.startswith("OL-F"):
            EDGE_EVIDENCE[edge] = "inline breaker to overload on feeder branch"
        elif a.startswith("OL-F") and not b.startswith("CB"):
            EDGE_EVIDENCE[edge] = "inline overload to named upper load"
        elif a.startswith("CB-A") or a.startswith("CB-B") or b.startswith("CB-A") or b.startswith("CB-B"):
            EDGE_EVIDENCE[edge] = "inline lower load-center branch"
        elif "CHG-125" in edge or "BAT-125" in edge or "INV-120" in edge or "BUS-125" in edge or "BUS-UPS" in edge:
            EDGE_EVIDENCE[edge] = "solid DC/UPS power conductor"
        else:
            EDGE_EVIDENCE[edge] = "visible named-node conductor"


def write_matrix(path: Path, edges: set[tuple[str, str]]) -> None:
    idx = {name: i for i, name in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for a, b in edges:
        i, j = idx[a], idx[b]
        if i == j:
            raise ValueError(f"Self-loop not expected: {a}")
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + NODES)
        for name, row in zip(NODES, matrix):
            writer.writerow([name] + row)


def write_edge_list(path: Path, edges: set[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for a, b in sorted(edges, key=lambda e: (NODES.index(e[0]), NODES.index(e[1]))):
            writer.writerow([a, b, EDGE_EVIDENCE.get((a, b), "")])


def text_tokens(text: str) -> int:
    if tiktoken is not None:
        for encoding_name in ("o200k_base", "cl100k_base"):
            try:
                enc = tiktoken.get_encoding(encoding_name)
                return len(enc.encode(text))
            except Exception:
                continue
    return math.ceil(len(text) / 4)


def estimate_image_tokens(path: Path) -> int:
    """Offline proxy for high-detail vision input tokens, not an API count."""
    if Image is None:
        return 0
    with Image.open(path) as img:
        width, height = img.size
    scale = min(1.0, 2048.0 / max(width, height))
    width = math.ceil(width * scale)
    height = math.ceil(height * scale)
    if min(width, height) > 768:
        scale = 768.0 / min(width, height)
        width = math.ceil(width * scale)
        height = math.ceil(height * scale)
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_sum(names: list[str]) -> int:
    total = 0
    for name in names:
        path = BASE / name if not name.startswith("results\\") else BASE / name
        total += estimate_image_tokens(path)
    return total


def write_token_estimates() -> None:
    diego_images = [
        "raw.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
        r"results\raw__top_left_sources.png",
        r"results\raw__upper_buses_left.png",
        r"results\raw__upper_buses_right.png",
        r"results\raw__upper_loads_left.png",
        r"results\raw__upper_loads_mid.png",
        r"results\raw__upper_loads_right.png",
        r"results\raw__left_vertical_source_to_lc.png",
        r"results\raw__lower_loads_left.png",
        r"results\raw__lower_loads_right.png",
        r"results\raw__dc_ups_top.png",
        r"results\raw__dc_ups_bottom.png",
        r"results\raw__right_lc_b_transfer_detail.png",
        r"results\raw__charger_a_feed_to_lca.png",
        r"results\raw__charger_b_feed_to_lcb.png",
        r"results\raw__dc_ups_control_detail.png",
    ]
    jennifer_images = [
        "raw.png",
        "detected_components_and_logical_overlay.png",
        r"results\raw__upper_buses_left.png",
        r"results\raw__upper_buses_right.png",
        r"results\raw__right_bus_tie_480_detail.png",
        r"results\raw__right_lc_b_transfer_detail.png",
        r"results\raw__lower_bus_full.png",
        r"results\raw__charger_a_feed_to_lca.png",
        r"results\raw__charger_b_feed_to_lcb.png",
        r"results\raw__dc_ups_top.png",
        r"results\raw__dc_ups_bottom.png",
        r"results\raw__dc_ups_control_detail.png",
    ]
    diego_prompt = "High-recall schematic connectivity extraction for document 4 using raw, wires, components, and junction crops only."
    jennifer_prompt = "Precision review of Diego proposal for document 4 using raw schematic and selected crops only."
    diego_r2_prompt = "Saturation check after Jennifer corrections; agree or list specific visual changes."

    calls = [
        {
            "call_id": "main-01",
            "actor": "Main",
            "round": "setup/visual workbench",
            "description": "Read doc4 prompt, inventory files, create crops, inspect allowed visual aids.",
            "input_text": "Document 4 user request and local visual inspection orchestration.",
            "input_text_tokens_override": 8500,
            "image_tokens": 0,
            "cached_est": 0,
            "output_low": 500,
            "output_expected": 900,
            "output_high": 1400,
        },
        {
            "call_id": "diego-01",
            "actor": "Diego",
            "round": "round 1 high recall",
            "description": "High-recall extraction from raw image and crop bundle.",
            "input_text": diego_prompt,
            "input_text_tokens_override": 1800,
            "image_tokens": image_sum(diego_images),
            "cached_est": 0,
            "output_low": 2400,
            "output_expected": 3900,
            "output_high": 6200,
        },
        {
            "call_id": "jennifer-01",
            "actor": "Jennifer",
            "round": "round 2 precision review",
            "description": "Precision review of Diego graph and selected raw crops.",
            "input_text": jennifer_prompt + "\n" + "Diego proposal text, node list, edge list, and uncertain candidates.",
            "input_text_tokens_override": 6500,
            "image_tokens": image_sum(jennifer_images),
            "cached_est": 0,
            "output_low": 1900,
            "output_expected": 3100,
            "output_high": 4700,
        },
        {
            "call_id": "diego-02",
            "actor": "Diego",
            "round": "round 3 saturation",
            "description": "Diego reviewed Jennifer corrections and agreed/saturated.",
            "input_text": diego_r2_prompt + "\n" + "Jennifer correction summary.",
            "input_text_tokens_override": 550,
            "image_tokens": 0,
            "cached_est": 22000,
            "output_low": 35,
            "output_expected": 70,
            "output_high": 160,
        },
        {
            "call_id": "main-02",
            "actor": "Main",
            "round": "finalization",
            "description": "Generate matrices, edge lists, notes, and usage estimate artifacts.",
            "input_text": "Subagent outputs and final artifact generation script.",
            "input_text_tokens_override": 14000,
            "image_tokens": 0,
            "cached_est": 0,
            "output_low": 450,
            "output_expected": 800,
            "output_high": 1300,
        },
    ]

    rows = []
    for call in calls:
        text_est = call.get("input_text_tokens_override", text_tokens(call["input_text"]))
        input_expected = text_est + call["image_tokens"] + call["cached_est"]
        total_low = input_expected + call["output_low"]
        total_expected = input_expected + call["output_expected"]
        total_high = input_expected + call["output_high"]
        rows.append(
            {
                "document": 4,
                "iteration": 1,
                "call_id": call["call_id"],
                "actor": call["actor"],
                "round": call["round"],
                "description": call["description"],
                "input_text_tokens_est": text_est,
                "image_file_input_tokens_est": call["image_tokens"],
                "cached_input_tokens_est": call["cached_est"],
                "recorded_input_tokens": "unavailable",
                "recorded_cached_input_tokens": "unavailable",
                "recorded_output_tokens": "unavailable",
                "recorded_reasoning_tokens": "unavailable",
                "output_tokens_low": call["output_low"],
                "output_tokens_expected": call["output_expected"],
                "output_tokens_high": call["output_high"],
                "total_tokens_low": total_low,
                "total_tokens_expected": total_expected,
                "total_tokens_high": total_high,
                "method": "manual text/context estimate where needed, otherwise local tokenizer fallback; high-detail image tile proxy; actual Responses usage object not exposed in this tool run",
            }
        )

    path = RESULTS / "token_usage_estimates.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary_path = RESULTS / "token_usage_summary_by_document_iteration.csv"
    low = sum(row["total_tokens_low"] for row in rows)
    expected = sum(row["total_tokens_expected"] for row in rows)
    high = sum(row["total_tokens_high"] for row in rows)
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "calls", "total_tokens_low", "total_tokens_expected", "total_tokens_high"])
        writer.writerow([4, 1, len(rows), low, expected, high])


def write_notes() -> None:
    notes = f"""# Document 4 Connectivity Extraction Notes

Allowed resource folder only:
`{BASE}`

No Ground Truth or GT-derived feedback was used.

## Rounds

1. Diego high-recall extraction:
   - Proposed the main source, bus, feeder, load-center, DC/UPS, and control topology.
   - Marked several plausible dashed/control/ground candidates as uncertain.
   - Matrix files:
     - `round_01_diego_high_recall_connectivity_matrix.csv` uses Diego's committed edge list.
     - `round_01_diego_high_recall_plus_uncertain_connectivity_matrix.csv` additionally includes his uncertain edge candidates.

2. Jennifer precision review:
   - Kept the main power topology.
   - Added GND-NG-A and GND-NG-B as named nodes with transformer ground edges.
   - Accepted relay-to-terminal-block and annunciator-to-recorder dashed control edges where endpoints visibly terminate.
   - Rejected dashed crossings near CB-LC-B/CB-LC-B2 and BUS-UPS-B because they do not visibly terminate there.

3. Diego saturation review:
   - Agreed with Jennifer.
   - Final graph saturated at {len(NODES)} nodes and {len(FINAL_EDGES)} edges.

## Final Counts

- Nodes: {len(NODES)}
- Edges: {len(FINAL_EDGES)}
- Connectivity matrix is symmetric with zero diagonal.

## Token Usage

The official Responses input-token counting endpoint could not be called because no `OPENAI_API_KEY` is available in this environment. Token artifacts are therefore local estimates:

- Text: `tiktoken` using `o200k_base` when available.
- Images/files: offline high-detail tile proxy based on image dimensions.
- Actual usage objects, cached input tokens, output tokens, and reasoning tokens were not exposed by the local multi-agent tool responses.
"""
    (RESULTS / "round_notes.md").write_text(notes, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    complete_edge_evidence()

    assert len(NODES) == 120, len(NODES)
    assert len(FINAL_EDGES) == 123, len(FINAL_EDGES)
    assert len(DIEGO_COMMITTED_EDGES) == 118, len(DIEGO_COMMITTED_EDGES)
    assert len(DIEGO_PLUS_UNCERTAIN_EDGES) == 127, len(DIEGO_PLUS_UNCERTAIN_EDGES)

    matrix_sets = {
        "round_01_diego_high_recall_connectivity_matrix.csv": DIEGO_COMMITTED_EDGES,
        "round_01_diego_high_recall_plus_uncertain_connectivity_matrix.csv": DIEGO_PLUS_UNCERTAIN_EDGES,
        "round_02_jennifer_precision_connectivity_matrix.csv": FINAL_EDGES,
        "round_03_diego_saturation_connectivity_matrix.csv": FINAL_EDGES,
        "final_connectivity_matrix.csv": FINAL_EDGES,
    }
    for filename, edges in matrix_sets.items():
        write_matrix(RESULTS / filename, edges)

    write_edge_list(RESULTS / "final_edge_list.csv", FINAL_EDGES)
    write_edge_list(RESULTS / "round_01_diego_high_recall_edge_list.csv", DIEGO_COMMITTED_EDGES)
    write_edge_list(RESULTS / "round_01_diego_high_recall_plus_uncertain_edge_list.csv", DIEGO_PLUS_UNCERTAIN_EDGES)
    write_edge_list(RESULTS / "round_02_jennifer_precision_edge_list.csv", FINAL_EDGES)
    write_edge_list(RESULTS / "round_03_diego_saturation_edge_list.csv", FINAL_EDGES)

    (RESULTS / "final_node_list.txt").write_text("\n".join(NODES) + "\n", encoding="utf-8")
    write_notes()
    write_token_estimates()

    print(f"Wrote document 4 artifacts to {RESULTS}")
    print(f"Final nodes: {len(NODES)}")
    print(f"Final edges: {len(FINAL_EDGES)}")


if __name__ == "__main__":
    main()
