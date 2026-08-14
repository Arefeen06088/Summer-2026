from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\40\Raw + wires"
)
CROPS = BASE / "codes" / "crops"
RESULTS = BASE / "results"


FINAL_NODES = [
    "DG-21A",
    "UAT-2A",
    "DS-21A",
    "ATS-21A",
    "SWGR-21A",
    "TIE-BKR-21AB",
    "SWGR-21B",
    "SAT-2B",
    "DS-21B",
    "ATS-21B",
    "DG-21B",
    "CB-21A1",
    "TR-21A",
    "MCC-21A",
    "VT-21A",
    "CT-21A",
    "CB-MPA1",
    "PUMP-SI21A",
    "PUMP-CCW21A",
    "FAN-RB21A",
    "MOV-HV211A",
    "MOV-RWST21A",
    "XFMR-CPT21A",
    "AC-PNL-120A",
    "RECT-21A",
    "DC-BUS-21A",
    "BAT-21A",
    "INV-21A",
    "LOCA-SIG-A",
    "JB-21A",
    "RPS-PNL-A",
    "RELAY-K21A",
    "RELAY-86A",
    "CB-21B1",
    "TR-21B",
    "MCC-21B",
    "VT-21B",
    "CT-21B",
    "CB-MPB1",
    "PUMP-SI21B",
    "PUMP-CCW21B",
    "FAN-RB21B",
    "MOV-HV211B",
    "MOV-RWST21B",
    "XFMR-CPT21B",
    "AC-PNL-120B",
    "RECT-21B",
    "DC-BUS-21B",
    "BAT-21B",
    "INV-21B",
    "LOCA-SIG-B",
    "JB-21B",
    "RPS-PNL-B",
    "RELAY-K21B",
    "RELAY-86B",
]


FINAL_EDGES = [
    ("DG-21A", "ATS-21A"),
    ("UAT-2A", "DS-21A"),
    ("DS-21A", "ATS-21A"),
    ("ATS-21A", "SWGR-21A"),
    ("SWGR-21A", "TIE-BKR-21AB"),
    ("TIE-BKR-21AB", "SWGR-21B"),
    ("SWGR-21A", "CB-21A1"),
    ("CB-21A1", "TR-21A"),
    ("TR-21A", "MCC-21A"),
    ("SAT-2B", "DS-21B"),
    ("DS-21B", "ATS-21B"),
    ("DG-21B", "ATS-21B"),
    ("ATS-21B", "SWGR-21B"),
    ("SWGR-21B", "CB-21B1"),
    ("CB-21B1", "TR-21B"),
    ("TR-21B", "MCC-21B"),
    ("MCC-21A", "CB-MPA1"),
    ("CB-MPA1", "PUMP-SI21A"),
    ("MCC-21A", "PUMP-CCW21A"),
    ("MCC-21A", "FAN-RB21A"),
    ("MCC-21A", "MOV-HV211A"),
    ("MCC-21A", "MOV-RWST21A"),
    ("MCC-21A", "XFMR-CPT21A"),
    ("XFMR-CPT21A", "AC-PNL-120A"),
    ("AC-PNL-120A", "RECT-21A"),
    ("RECT-21A", "DC-BUS-21A"),
    ("DC-BUS-21A", "BAT-21A"),
    ("DC-BUS-21A", "INV-21A"),
    ("VT-21A", "RPS-PNL-A"),
    ("CT-21A", "RPS-PNL-A"),
    ("LOCA-SIG-A", "JB-21A"),
    ("JB-21A", "RPS-PNL-A"),
    ("RPS-PNL-A", "RELAY-K21A"),
    ("RELAY-K21A", "RELAY-86A"),
    ("RELAY-86A", "CB-MPA1"),
    ("RPS-PNL-A", "INV-21A"),
    ("MCC-21B", "XFMR-CPT21B"),
    ("XFMR-CPT21B", "AC-PNL-120B"),
    ("AC-PNL-120B", "RECT-21B"),
    ("RECT-21B", "DC-BUS-21B"),
    ("DC-BUS-21B", "BAT-21B"),
    ("DC-BUS-21B", "INV-21B"),
    ("MCC-21B", "CB-MPB1"),
    ("CB-MPB1", "PUMP-SI21B"),
    ("MCC-21B", "PUMP-CCW21B"),
    ("MCC-21B", "FAN-RB21B"),
    ("MCC-21B", "MOV-HV211B"),
    ("MCC-21B", "MOV-RWST21B"),
    ("VT-21B", "RPS-PNL-B"),
    ("CT-21B", "RPS-PNL-B"),
    ("LOCA-SIG-B", "JB-21B"),
    ("JB-21B", "RPS-PNL-B"),
    ("RPS-PNL-B", "RELAY-K21B"),
    ("RELAY-K21B", "RELAY-86B"),
    ("RELAY-86B", "CB-MPB1"),
    ("RPS-PNL-B", "INV-21B"),
]


DIEGO_R1_EDGES = FINAL_EDGES + [
    ("DC-BUS-21A", "RPS-PNL-A"),
    ("DC-BUS-21B", "RPS-PNL-B"),
]


ROUND_DEFINITIONS = [
    (
        "round1_diego_high_recall",
        "Diego R1",
        FINAL_NODES,
        DIEGO_R1_EDGES,
        "High-recall graph. Included two low-confidence DC-BUS-to-RPS-panel candidate edges.",
    ),
    (
        "round1_jennifer_precision",
        "Jennifer R1",
        FINAL_NODES,
        FINAL_EDGES,
        "Precision review. Removed both DC-BUS-to-RPS-panel edges because dashed signal drops cross the DC buses without filled junction dots.",
    ),
    (
        "round2_diego_saturation",
        "Diego R2",
        FINAL_NODES,
        FINAL_EDGES,
        "Saturation check against Jennifer R1 graph; no additional visually supported nodes or edges.",
    ),
    (
        "round2_jennifer_final",
        "Jennifer R2",
        FINAL_NODES,
        FINAL_EDGES,
        "Final precision confirmation; no additional changes after Diego R2.",
    ),
]


EDGE_DETAILS = {
    ("DG-21A", "ATS-21A"): ("high", "solid feeder from DG into ATS source terminal"),
    ("UAT-2A", "DS-21A"): ("high", "solid vertical feeder between UAT and disconnect"),
    ("DS-21A", "ATS-21A"): ("high", "solid feeder from disconnect into ATS terminal"),
    ("ATS-21A", "SWGR-21A"): ("high", "solid ATS drop lands on SWGR bus junction dot"),
    ("SWGR-21A", "TIE-BKR-21AB"): ("high", "SWGR bus enters tie breaker left terminal"),
    ("TIE-BKR-21AB", "SWGR-21B"): ("high", "tie breaker right terminal continues as SWGR bus"),
    ("SWGR-21A", "CB-21A1"): ("high", "solid bus tap with junction dot drops to breaker"),
    ("CB-21A1", "TR-21A"): ("high", "solid feeder from breaker to transformer"),
    ("TR-21A", "MCC-21A"): ("high", "solid feeder from transformer lands on MCC bus dot"),
    ("SAT-2B", "DS-21B"): ("high", "solid vertical feeder between SAT and disconnect"),
    ("DS-21B", "ATS-21B"): ("high", "solid feeder from disconnect into ATS terminal"),
    ("DG-21B", "ATS-21B"): ("high", "solid feeder from DG into ATS source terminal"),
    ("ATS-21B", "SWGR-21B"): ("high", "solid ATS drop lands on SWGR bus junction dot"),
    ("SWGR-21B", "CB-21B1"): ("high", "solid bus tap with junction dot drops to breaker"),
    ("CB-21B1", "TR-21B"): ("high", "solid feeder from breaker to transformer"),
    ("TR-21B", "MCC-21B"): ("high", "solid feeder from transformer lands on MCC bus dot"),
    ("MCC-21A", "CB-MPA1"): ("high", "solid MCC feeder enters breaker"),
    ("CB-MPA1", "PUMP-SI21A"): ("high", "solid feeder exits breaker to pump"),
    ("MCC-21A", "PUMP-CCW21A"): ("high", "solid MCC branch lands on pump"),
    ("MCC-21A", "FAN-RB21A"): ("high", "solid MCC branch lands on fan"),
    ("MCC-21A", "MOV-HV211A"): ("high", "solid MCC branch lands on MOV"),
    ("MCC-21A", "MOV-RWST21A"): ("high", "solid MCC branch lands on MOV"),
    ("MCC-21A", "XFMR-CPT21A"): ("high", "solid MCC branch feeds CPT transformer"),
    ("XFMR-CPT21A", "AC-PNL-120A"): ("high", "solid feeder from CPT transformer to AC panel"),
    ("AC-PNL-120A", "RECT-21A"): ("high", "solid feeder from AC panel to rectifier"),
    ("RECT-21A", "DC-BUS-21A"): ("high", "solid rectifier output joins 125 VDC bus at dot"),
    ("DC-BUS-21A", "BAT-21A"): ("high", "solid battery lead joins DC bus at dot"),
    ("DC-BUS-21A", "INV-21A"): ("high", "solid inverter lead joins DC bus at dot"),
    ("VT-21A", "RPS-PNL-A"): ("high", "short-dash Voltage Sig A path lands on RPS top terminal"),
    ("CT-21A", "RPS-PNL-A"): ("high", "short-dash CT signal lands on RPS top terminal"),
    ("LOCA-SIG-A", "JB-21A"): ("high", "dashed logic line terminates at LOCA and JB"),
    ("JB-21A", "RPS-PNL-A"): ("high", "dashed logic line from JB lands on RPS terminal"),
    ("RPS-PNL-A", "RELAY-K21A"): ("high", "dashed control line connects RPS to K relay"),
    ("RELAY-K21A", "RELAY-86A"): ("high", "dashed control line connects K relay to 86 relay"),
    ("RELAY-86A", "CB-MPA1"): ("high", "dash-dot trip control route lands at breaker trip MPA1"),
    ("RPS-PNL-A", "INV-21A"): ("high", "dashed control line connects RPS to inverter terminal"),
    ("MCC-21B", "XFMR-CPT21B"): ("high", "solid MCC branch feeds CPT transformer"),
    ("XFMR-CPT21B", "AC-PNL-120B"): ("high", "solid feeder from CPT transformer to AC panel"),
    ("AC-PNL-120B", "RECT-21B"): ("high", "solid feeder from AC panel to rectifier"),
    ("RECT-21B", "DC-BUS-21B"): ("high", "solid rectifier output joins 125 VDC bus at dot"),
    ("DC-BUS-21B", "BAT-21B"): ("high", "solid battery lead joins DC bus at dot"),
    ("DC-BUS-21B", "INV-21B"): ("high", "solid inverter lead joins DC bus at dot"),
    ("MCC-21B", "CB-MPB1"): ("high", "solid MCC feeder enters breaker"),
    ("CB-MPB1", "PUMP-SI21B"): ("high", "solid feeder exits breaker to pump"),
    ("MCC-21B", "PUMP-CCW21B"): ("high", "solid MCC branch lands on pump"),
    ("MCC-21B", "FAN-RB21B"): ("high", "solid MCC branch lands on fan"),
    ("MCC-21B", "MOV-HV211B"): ("high", "solid MCC branch lands on MOV"),
    ("MCC-21B", "MOV-RWST21B"): ("high", "solid MCC branch lands on MOV"),
    ("VT-21B", "RPS-PNL-B"): ("high", "short-dash Voltage Sig B path lands on RPS top terminal"),
    ("CT-21B", "RPS-PNL-B"): ("high", "short-dash CT signal lands on RPS top terminal"),
    ("LOCA-SIG-B", "JB-21B"): ("high", "dashed logic line terminates at LOCA and JB"),
    ("JB-21B", "RPS-PNL-B"): ("high", "dashed logic line from JB lands on RPS terminal"),
    ("RPS-PNL-B", "RELAY-K21B"): ("high", "dashed control line connects RPS to K relay"),
    ("RELAY-K21B", "RELAY-86B"): ("high", "dashed control line connects K relay to 86 relay"),
    ("RELAY-86B", "CB-MPB1"): ("high", "dash-dot trip control route lands at breaker trip MPB1"),
    ("RPS-PNL-B", "INV-21B"): ("high", "dashed control line connects RPS to inverter terminal"),
    ("DC-BUS-21A", "RPS-PNL-A"): (
        "low",
        "Diego R1 high-recall candidate; removed because visible dashed drops cross the 125 VDC bus without filled junction dots",
    ),
    ("DC-BUS-21B", "RPS-PNL-B"): (
        "low",
        "Diego R1 high-recall candidate; removed because visible dashed drops cross the 125 VDC bus without filled junction dots",
    ),
}


@dataclass(frozen=True)
class CallEstimate:
    document: int
    iteration: int
    call: str
    actor: str
    model: str
    text_input_tokens: int
    cached_input_tokens: int
    image_file_count: int
    image_input_tokens_low: int
    image_input_tokens_expected: int
    image_input_tokens_high: int
    output_tokens_low: int
    output_tokens_expected: int
    output_tokens_high: int
    reasoning_tokens: str
    usage_object_available: str
    notes: str


def normalized_edge(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def edge_detail(a: str, b: str) -> tuple[str, str]:
    return EDGE_DETAILS.get((a, b)) or EDGE_DETAILS.get((b, a)) or (
        "high",
        "visible conductor/terminal relationship in Raw + wires schematic",
    )


def validate_edges(nodes: list[str], edges: list[tuple[str, str]]) -> None:
    node_set = set(nodes)
    missing = [(a, b) for a, b in edges if a not in node_set or b not in node_set]
    if missing:
        raise ValueError(f"Edges refer to missing nodes: {missing}")

    seen = set()
    dupes = []
    for a, b in edges:
        key = normalized_edge(a, b)
        if key in seen:
            dupes.append((a, b))
        seen.add(key)
    if dupes:
        raise ValueError(f"Duplicate undirected edges: {dupes}")


def matrix_for(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    idx = {node: i for i, node in enumerate(nodes)}
    mat = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        i, j = idx[a], idx[b]
        if i == j:
            raise ValueError(f"Self-loop not expected for {a}")
        mat[i][j] = 1
        mat[j][i] = 1

    for i, row in enumerate(mat):
        if row[i] != 0:
            raise ValueError("Diagonal must be zero")
        for j, val in enumerate(row):
            if val != mat[j][i]:
                raise ValueError("Matrix must be symmetric")
    return mat


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label"])
        for i, node in enumerate(nodes, start=1):
            writer.writerow([f"N{i:02d}", node])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "confidence", "evidence"])
        for a, b in edges:
            confidence, evidence = edge_detail(a, b)
            writer.writerow([a, b, confidence, evidence])


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    mat = matrix_for(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, mat):
            writer.writerow([node] + row)


def write_round_notes(path: Path, title: str, nodes: list[str], edges: list[tuple[str, str]], note: str) -> None:
    lines = [
        f"# {title}",
        "",
        f"- Node count: {len(nodes)}",
        f"- Edge count: {len(edges)}",
        f"- Note: {note}",
        "- Source restriction: Raw + wires only; no GT/GT-derived files used.",
        "- OCR restriction: no off-the-shelf OCR used.",
        "- Matrix type: undirected, symmetric, diagonal zero.",
        "",
        "## Nodes",
        "",
    ]
    lines += [f"{i:02d}. {node}" for i, node in enumerate(nodes, start=1)]
    lines += ["", "## Edges", ""]
    for a, b in edges:
        confidence, evidence = edge_detail(a, b)
        lines.append(f"- {a} -- {b} ({confidence}): {evidence}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def openai_high_detail_image_tokens(width: int, height: int) -> int:
    """Approximate OpenAI high-detail image token cost from public tiling rules."""
    scale = min(2048 / width, 2048 / height, 1.0)
    w = width * scale
    h = height * scale
    if min(w, h) > 768:
        scale2 = 768 / min(w, h)
        w *= scale2
        h *= scale2
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def image_dims(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.width, img.height


def image_token_bundle(paths: list[Path]) -> tuple[int, int, int]:
    low = 85 * len(paths)
    expected = 0
    for path in paths:
        w, h = image_dims(path)
        expected += openai_high_detail_image_tokens(w, h)
    high = math.ceil(expected * 1.25)
    return low, expected, high


def estimate_text_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def build_token_estimates() -> list[CallEstimate]:
    raw = BASE / "raw -- synthetic_nuclear_distribution_schematic.png"
    overlay = BASE / "wires_mask_overlay.png"
    r1_images = [
        raw,
        overlay,
        CROPS / "top_sources_tie_raw_2x.png",
        CROPS / "left_train_full_overlay_2x.png",
        CROPS / "right_train_full_overlay_2x.png",
        CROPS / "left_rps_terminals_detail_raw_2x.png",
        CROPS / "left_trip_loca_detail_raw_2x.png",
        CROPS / "right_rps_terminals_detail_raw_2x.png",
        CROPS / "right_trip_loca_detail_raw_2x.png",
        CROPS / "notes_legend_raw_2x.png",
    ]
    focused_images = [
        CROPS / "top_sources_tie_raw_2x.png",
        CROPS / "left_train_full_overlay_2x.png",
        CROPS / "right_train_full_overlay_2x.png",
        CROPS / "left_rps_terminals_detail_raw_2x.png",
        CROPS / "left_trip_loca_detail_raw_2x.png",
        CROPS / "right_rps_terminals_detail_raw_2x.png",
        CROPS / "right_trip_loca_detail_raw_2x.png",
    ]
    final_images = [
        CROPS / "top_sources_tie_raw_2x.png",
        CROPS / "left_train_full_overlay_2x.png",
        CROPS / "right_train_full_overlay_2x.png",
        CROPS / "left_rps_terminals_detail_raw_2x.png",
        CROPS / "left_trip_loca_detail_raw_2x.png",
        CROPS / "right_rps_terminals_detail_raw_2x.png",
        CROPS / "right_trip_loca_detail_raw_2x.png",
        CROPS / "notes_legend_raw_2x.png",
    ]
    graph_text = "\n".join(FINAL_NODES) + "\n" + "\n".join(f"{a}--{b}" for a, b in FINAL_EDGES)
    calls = [
        (
            "main_agent_visual_orchestration",
            "Main agent",
            "gpt-5-class Codex runtime",
            30000,
            r1_images,
            (2200, 3600, 7000),
            "Aggregate estimate for the main Codex calls in document 40, including crop inspection, orchestration, script writing, validation, and final response. Exact usage is not exposed.",
        ),
        (
            "round1_diego_high_recall",
            "Diego",
            "gpt-5.5",
            estimate_text_tokens(
                "High-recall extraction instructions, source restrictions, crop/resource paths, and requested matrix format."
            ),
            r1_images,
            (7000, 10000, 15000),
            "Subagent usage object was not exposed; output estimate is based on the returned full node/edge list and matrix.",
        ),
        (
            "round1_jennifer_precision",
            "Jennifer",
            "gpt-5.5",
            estimate_text_tokens(
                "Precision review prompt with Diego R1 node list, edge list, restrictions, and requested corrected matrix."
                + graph_text
            ),
            final_images,
            (7000, 10500, 16000),
            "Subagent usage object was not exposed; image set matches the submitted Jennifer R1 local-image payload.",
        ),
        (
            "round2_diego_saturation",
            "Diego",
            "gpt-5.5",
            estimate_text_tokens(
                "Saturation prompt with Jennifer R1 corrected node and edge list plus focus questions."
                + graph_text
            ),
            focused_images,
            (800, 1500, 3500),
            "Focused saturation check; image set matches the submitted Diego R2 local-image payload.",
        ),
        (
            "round2_jennifer_final",
            "Jennifer",
            "gpt-5.5",
            estimate_text_tokens(
                "Final precision confirmation prompt with Diego R2 saturation report and corrected graph."
                + graph_text
            ),
            final_images,
            (600, 1200, 3000),
            "Final confirmation estimate; exact usage object unavailable.",
        ),
    ]

    estimates: list[CallEstimate] = []
    for name, actor, model, text_tokens, image_paths, output_range, notes in calls:
        image_low, image_expected, image_high = image_token_bundle(image_paths)
        estimates.append(
            CallEstimate(
                document=40,
                iteration=1,
                call=name,
                actor=actor,
                model=model,
                text_input_tokens=text_tokens,
                cached_input_tokens=0,
                image_file_count=len(image_paths),
                image_input_tokens_low=image_low,
                image_input_tokens_expected=image_expected,
                image_input_tokens_high=image_high,
                output_tokens_low=output_range[0],
                output_tokens_expected=output_range[1],
                output_tokens_high=output_range[2],
                reasoning_tokens="not available",
                usage_object_available="no",
                notes=notes,
            )
        )
    return estimates


def write_token_estimates(estimates: list[CallEstimate]) -> None:
    fields = list(CallEstimate.__dataclass_fields__.keys())
    extra_fields = ["input_total_expected", "total_low", "total_expected", "total_high"]
    rows = []

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields + extra_fields)
        writer.writeheader()
        for est in estimates:
            row = est.__dict__.copy()
            row["input_total_expected"] = (
                est.text_input_tokens + est.cached_input_tokens + est.image_input_tokens_expected
            )
            row["total_low"] = (
                est.text_input_tokens
                + est.cached_input_tokens
                + est.image_input_tokens_low
                + est.output_tokens_low
            )
            row["total_expected"] = row["input_total_expected"] + est.output_tokens_expected
            row["total_high"] = (
                math.ceil(est.text_input_tokens * 1.2)
                + est.cached_input_tokens
                + est.image_input_tokens_high
                + est.output_tokens_high
            )
            rows.append(row)
            writer.writerow(row)

    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    total_low = sum(row["total_low"] for row in rows)
    total_expected = sum(row["total_expected"] for row in rows)
    total_high = sum(row["total_high"] for row in rows)
    md = [
        "# Token Usage Estimate",
        "",
        "Exact Responses token-count endpoint calls and model usage objects were not available because no API key or usage object was exposed through the local subagent tools. This file uses local text-token heuristics plus an OpenAI-style high-detail image tiling estimate for each planned image payload.",
        "",
        "| Document | Iteration | Call | Actor | Input expected | Cached input | Output expected | Image/file tokens expected | Total low | Total expected | Total high |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        md.append(
            f"| {row['document']} | {row['iteration']} | {row['call']} | {row['actor']} | "
            f"{row['input_total_expected']} | {row['cached_input_tokens']} | {row['output_tokens_expected']} | "
            f"{row['image_input_tokens_expected']} | {row['total_low']} | {row['total_expected']} | {row['total_high']} |"
        )
    md += [
        f"| 40 | 1 | **TOTAL** | all |  |  |  |  | **{total_low}** | **{total_expected}** | **{total_high}** |",
        "",
        "Reasoning tokens: not available from the subagent tool responses.",
        "Cached input tokens: recorded as 0 because cache accounting was not exposed.",
    ]
    (RESULTS / "token_usage_estimate.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def write_consensus_notes() -> None:
    edge_lines = [f"- {a} -- {b}" for a, b in FINAL_EDGES]
    notes = [
        "# Document 40 Consensus Notes",
        "",
        "Final graph saturated after Diego R1 -> Jennifer R1 -> Diego R2 -> Jennifer R2.",
        "",
        f"- Final node count: {len(FINAL_NODES)}",
        f"- Final edge count: {len(FINAL_EDGES)}",
        "- Matrix type: undirected, symmetric, diagonal zero.",
        "- Source restriction: only files in Raw + wires were used.",
        "- OCR restriction: no off-the-shelf OCR was used.",
        "",
        "## Precision Decisions",
        "",
        "- `DC-BUS-21A -- RPS-PNL-A` and `DC-BUS-21B -- RPS-PNL-B` were removed; the dashed signal drops cross the 125 VDC buses without filled junction dots before landing at RPS terminals.",
        "- `VOLTAGE SIG A` and `VOLTAGE SIG B` were treated as route labels, not nodes. The modeled edges are `VT-21A -- RPS-PNL-A` and `VT-21B -- RPS-PNL-B`.",
        "- Cable IDs such as `D21A-07` and `D21B-07` were treated as conductor labels, not nodes.",
        "- MOV-RWST21A/B have only their MCC power feeders modeled; nearby dashed/short-dash routes cross without junction dots or belong to voltage/trip routing.",
        "- Relay-86 trip/control routes to `CB-MPA1` and `CB-MPB1` were retained because the dash-dot trip route visibly lands at the breaker trip terminals.",
        "",
        "## Removed High-Recall Candidates",
        "",
        "- DC-BUS-21A -- RPS-PNL-A",
        "- DC-BUS-21B -- RPS-PNL-B",
        "",
        "## Final Edges",
        "",
        *edge_lines,
    ]
    (RESULTS / "consensus_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary_rows = []
    for slug, title, nodes, edges, note in ROUND_DEFINITIONS:
        validate_edges(nodes, edges)
        write_nodes(RESULTS / f"{slug}_nodes.csv", nodes)
        write_edges(RESULTS / f"{slug}_edges.csv", edges)
        write_matrix(RESULTS / f"{slug}_connectivity_matrix.csv", nodes, edges)
        write_round_notes(RESULTS / f"{slug}_notes.md", title, nodes, edges, note)
        summary_rows.append([slug, title, len(nodes), len(edges), note])

    write_nodes(RESULTS / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_consensus_notes()
    write_token_estimates(build_token_estimates())

    with (RESULTS / "rounds_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["slug", "round", "node_count", "edge_count", "note"])
        writer.writerows(summary_rows)

    manifest = {
        "document": 40,
        "iteration": 1,
        "source_folder": str(BASE),
        "final_node_count": len(FINAL_NODES),
        "final_edge_count": len(FINAL_EDGES),
        "rounds": [row[0] for row in summary_rows],
        "final_files": [
            "final_nodes.csv",
            "final_edges.csv",
            "final_connectivity_matrix.csv",
            "consensus_notes.md",
            "token_usage_estimate.csv",
            "token_usage_estimate.md",
        ],
    }
    (RESULTS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
