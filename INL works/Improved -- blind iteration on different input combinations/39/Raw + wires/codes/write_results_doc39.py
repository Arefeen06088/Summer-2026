from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires")
CROPS = BASE / "codes" / "crops"
RESULTS = BASE / "results"


DIEGO_R1_NODES = [
    "OFFSITE-230KV-A",
    "DS-230A",
    "TR-1A",
    "CB-1A",
    "BUS-4160-A",
    "EDG-1A",
    "CB-DG-A",
    "RELAY-UV-A",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A/LC-A",
    "GND-PLANT",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "PANEL-120A",
    "RPS-A",
    "RELAY-KA1",
    "MCC-A1",
    "PUMP-RHR-A",
    "PUMP-CS-A",
    "MCC-A2",
    "PUMP-CCW-A",
    "MOV-881A",
    "MOV-742A",
    "JB-A101",
    "ANN-CR01",
    "CONTROL-ROOM-ANNUNCIATION",
    "REC-SOE01",
    "CB-TIE-AB",
    "OFFSITE-230KV-B",
    "DS-230B",
    "TR-1B",
    "CB-1B",
    "BUS-4160-B",
    "EDG-1B",
    "CB-DG-B",
    "RELAY-UV-B",
    "TR-480-B",
    "CB-480-B",
    "BUS-480-B/LC-B",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "PANEL-120B",
    "RPS-B",
    "RELAY-KB1",
    "MCC-B1",
    "PUMP-RHR-B",
    "PUMP-CS-B",
    "MCC-B2",
    "PUMP-CCW-B",
    "MOV-881B",
    "MOV-742B",
    "JB-B101",
]

FINAL_NODES = [
    "OFFSITE-230KV-A",
    "DS-230A",
    "TR-1A",
    "CB-1A",
    "BUS-4160-A",
    "EDG-1A",
    "CB-DG-A",
    "RELAY-UV-A",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A/LC-A",
    "GND-PLANT",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "PANEL-120A",
    "RPS-A",
    "RELAY-KA1",
    "MCC-A1",
    "PUMP-RHR-A",
    "PUMP-CS-A",
    "MCC-A2",
    "PUMP-CCW-A",
    "MOV-881A",
    "MOV-742A",
    "JB-A101",
    "ANN-CR01",
    "REC-SOE01",
    "CB-TIE-AB",
    "OFFSITE-230KV-B",
    "DS-230B",
    "TR-1B",
    "CB-1B",
    "BUS-4160-B",
    "EDG-1B",
    "CB-DG-B",
    "RELAY-UV-B",
    "TR-480-B",
    "CB-480-B",
    "BUS-480-B/LC-B",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "PANEL-120B",
    "RPS-B",
    "RELAY-KB1",
    "MCC-B1",
    "PUMP-RHR-B",
    "PUMP-CS-B",
    "MCC-B2",
    "PUMP-CCW-B",
    "MOV-881B",
    "MOV-742B",
    "JB-B101",
]

FINAL_EDGES = [
    ("OFFSITE-230KV-A", "DS-230A"),
    ("DS-230A", "TR-1A"),
    ("TR-1A", "CB-1A"),
    ("CB-1A", "BUS-4160-A"),
    ("EDG-1A", "CB-DG-A"),
    ("CB-DG-A", "BUS-4160-A"),
    ("BUS-4160-A", "RELAY-UV-A"),
    ("BUS-4160-A", "TR-480-A"),
    ("TR-480-A", "CB-480-A"),
    ("CB-480-A", "BUS-480-A/LC-A"),
    ("BUS-480-A/LC-A", "GND-PLANT"),
    ("BUS-480-A/LC-A", "CHG-125A"),
    ("CHG-125A", "BAT-125A"),
    ("BAT-125A", "INV-120A"),
    ("INV-120A", "PANEL-120A"),
    ("PANEL-120A", "RPS-A"),
    ("RPS-A", "RELAY-KA1"),
    ("RPS-A", "JB-A101"),
    ("BUS-480-A/LC-A", "MCC-A1"),
    ("MCC-A1", "PUMP-RHR-A"),
    ("MCC-A1", "PUMP-CS-A"),
    ("BUS-480-A/LC-A", "MCC-A2"),
    ("MCC-A2", "PUMP-CCW-A"),
    ("MCC-A2", "MOV-881A"),
    ("MCC-A2", "MOV-742A"),
    ("JB-A101", "MOV-881A"),
    ("JB-A101", "MOV-742A"),
    ("ANN-CR01", "REC-SOE01"),
    ("BUS-4160-A", "CB-TIE-AB"),
    ("CB-TIE-AB", "BUS-4160-B"),
    ("OFFSITE-230KV-B", "DS-230B"),
    ("DS-230B", "TR-1B"),
    ("TR-1B", "CB-1B"),
    ("CB-1B", "BUS-4160-B"),
    ("EDG-1B", "CB-DG-B"),
    ("CB-DG-B", "BUS-4160-B"),
    ("BUS-4160-B", "RELAY-UV-B"),
    ("BUS-4160-B", "TR-480-B"),
    ("TR-480-B", "CB-480-B"),
    ("CB-480-B", "BUS-480-B/LC-B"),
    ("BUS-480-B/LC-B", "CHG-125B"),
    ("CHG-125B", "BAT-125B"),
    ("BAT-125B", "INV-120B"),
    ("INV-120B", "PANEL-120B"),
    ("PANEL-120B", "RPS-B"),
    ("RPS-B", "RELAY-KB1"),
    ("RPS-B", "JB-B101"),
    ("BUS-480-B/LC-B", "MCC-B1"),
    ("MCC-B1", "PUMP-RHR-B"),
    ("MCC-B1", "PUMP-CS-B"),
    ("BUS-480-B/LC-B", "MCC-B2"),
    ("MCC-B2", "PUMP-CCW-B"),
    ("MCC-B2", "MOV-881B"),
    ("MCC-B2", "MOV-742B"),
    ("JB-B101", "MOV-881B"),
    ("JB-B101", "MOV-742B"),
]

DIEGO_R1_EDGES = [
    edge for edge in FINAL_EDGES if edge != ("ANN-CR01", "REC-SOE01")
] + [
    ("JB-A101", "CONTROL-ROOM-ANNUNCIATION"),
    ("ANN-CR01", "CONTROL-ROOM-ANNUNCIATION"),
    ("CONTROL-ROOM-ANNUNCIATION", "REC-SOE01"),
    ("JB-B101", "CONTROL-ROOM-ANNUNCIATION"),
]

ROUND_DEFINITIONS = [
    (
        "round1_diego_high_recall",
        "Diego R1",
        DIEGO_R1_NODES,
        DIEGO_R1_EDGES,
        "High-recall graph. Included CONTROL-ROOM-ANNUNCIATION as a tentative route node and four low-confidence route edges.",
    ),
    (
        "round1_jennifer_precision",
        "Jennifer R1",
        FINAL_NODES,
        FINAL_EDGES,
        "Precision review. Removed route-label node and replaced its ANN/REC relationship with direct ANN-CR01--REC-SOE01.",
    ),
    (
        "round2_diego_saturation",
        "Diego R2",
        FINAL_NODES,
        FINAL_EDGES,
        "Diego agreed Jennifer R1 is saturated with no additions or removals.",
    ),
    (
        "round2_jennifer_final",
        "Jennifer R2",
        FINAL_NODES,
        FINAL_EDGES,
        "Final precision confirmation; no additional changes expected after saturation.",
    ),
]

EDGE_EVIDENCE = {
    "power_bus": "Visible solid conductor or bus branch with component terminals/junction dots.",
    "dc_stack": "Visible vertical DC/120 V stack conductor through the 125 VDC and 120 V components.",
    "control": "Visible dashed control/sensing conductor; terminal schedule in drawing supports RPS-to-JB/relay paths.",
    "annunciation": "Visible dashed conductor directly between ANN-CR01 and REC-SOE01.",
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


def validate_edges(nodes: list[str], edges: list[tuple[str, str]]) -> None:
    node_set = set(nodes)
    missing = [(a, b) for a, b in edges if a not in node_set or b not in node_set]
    if missing:
        raise ValueError(f"Edges refer to missing nodes: {missing}")
    dupes = []
    seen = set()
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
        writer.writerow(["source", "target"])
        for a, b in edges:
            writer.writerow([a, b])


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
        "",
        "## Nodes",
        "",
    ]
    lines += [f"{i:02d}. {node}" for i, node in enumerate(nodes, start=1)]
    lines += ["", "## Edges", ""]
    lines += [f"- {a} -- {b}" for a, b in edges]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def openai_high_detail_image_tokens(width: int, height: int) -> int:
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


def build_token_estimates() -> list[CallEstimate]:
    raw = BASE / "raw -- npp_schematic_improved_no_overlap.png"
    overlay = BASE / "wires_mask_overlay.png"
    calls = [
        (
            "main_agent_visual_orchestration",
            "Main agent",
            "gpt-5-class Codex runtime",
            24000,
            [
                raw,
                overlay,
                CROPS / "top_bus_tie_raw_2x.png",
                CROPS / "left_480_loads_raw_2x.png",
                CROPS / "left_bottom_devices_raw_2x.png",
                CROPS / "bottom_controls_raw_2x.png",
                CROPS / "bottom_controls_overlay_2x.png",
                CROPS / "right_480_loads_raw_2x.png",
                CROPS / "left_dc_control_raw_2x.png",
                CROPS / "left_train_full_raw_2x.png",
                CROPS / "left_dc_control_overlay_2x.png",
                CROPS / "right_control_lower_wide_raw_2x.png",
                CROPS / "right_dc_control_raw_2x.png",
                CROPS / "right_dc_control_overlay_2x.png",
                CROPS / "title_and_notes_raw_2x.png",
                CROPS / "annunciation_center_raw_2x.png",
                CROPS / "jb_a101_ann_detail_raw_2x.png",
                CROPS / "jb_b101_ann_detail_raw_2x.png",
            ],
            (2800, 4500, 8000),
            "Aggregate estimate for this Codex turn; exact main-agent usage is not exposed.",
        ),
        (
            "round1_diego_high_recall",
            "Diego",
            "gpt-5.5",
            650,
            [
                raw,
                overlay,
                CROPS / "top_bus_tie_raw_2x.png",
                CROPS / "left_480_loads_raw_2x.png",
                CROPS / "right_480_loads_raw_2x.png",
                CROPS / "left_dc_control_raw_2x.png",
                CROPS / "right_dc_control_raw_2x.png",
                CROPS / "bottom_controls_raw_2x.png",
                CROPS / "title_and_notes_raw_2x.png",
            ],
            (8500, 11500, 15000),
            "Subagent final response contained full high-recall matrix.",
        ),
        (
            "round1_jennifer_precision",
            "Jennifer",
            "gpt-5.5",
            1750,
            [
                raw,
                overlay,
                CROPS / "top_bus_tie_raw_2x.png",
                CROPS / "left_train_full_raw_2x.png",
                CROPS / "right_train_full_raw_2x.png",
                CROPS / "left_control_lower_wide_raw_2x.png",
                CROPS / "right_control_lower_wide_raw_2x.png",
                CROPS / "annunciation_center_raw_2x.png",
                CROPS / "title_and_notes_raw_2x.png",
            ],
            (3500, 5800, 8500),
            "Subagent final response included sparse corrected graph and partial matrix; edge list is authoritative.",
        ),
        (
            "round2_diego_saturation",
            "Diego",
            "gpt-5.5",
            1700,
            [
                raw,
                overlay,
                CROPS / "top_bus_tie_raw_2x.png",
                CROPS / "left_control_lower_wide_raw_2x.png",
                CROPS / "right_control_lower_wide_raw_2x.png",
                CROPS / "annunciation_center_raw_2x.png",
                CROPS / "title_and_notes_raw_2x.png",
            ],
            (180, 300, 600),
            "Focused saturation check; Diego agreed with Jennifer R1.",
        ),
        (
            "round2_jennifer_final",
            "Jennifer",
            "gpt-5.5",
            1550,
            [
                raw,
                overlay,
                CROPS / "top_bus_tie_raw_2x.png",
                CROPS / "left_train_full_raw_2x.png",
                CROPS / "right_train_full_raw_2x.png",
                CROPS / "jb_a101_ann_detail_raw_2x.png",
                CROPS / "jb_b101_ann_detail_raw_2x.png",
                CROPS / "title_and_notes_raw_2x.png",
            ],
            (250, 450, 900),
            "Final precision confirmation; exact output usage unavailable until API usage objects are exposed.",
        ),
    ]
    estimates = []
    for name, actor, model, text_tokens, image_paths, out_range, notes in calls:
        image_low, image_expected, image_high = image_token_bundle(image_paths)
        estimates.append(
            CallEstimate(
                document=39,
                iteration=1,
                call=name,
                actor=actor,
                model=model,
                text_input_tokens=text_tokens,
                cached_input_tokens=0,
                image_input_tokens_low=image_low,
                image_input_tokens_expected=image_expected,
                image_input_tokens_high=image_high,
                output_tokens_low=out_range[0],
                output_tokens_expected=out_range[1],
                output_tokens_high=out_range[2],
                reasoning_tokens="not available",
                usage_object_available="no",
                notes=notes,
            )
        )
    return estimates


def write_token_estimates(estimates: list[CallEstimate]) -> None:
    path = RESULTS / "token_usage_estimate.csv"
    fields = list(CallEstimate.__dataclass_fields__.keys())
    extra_fields = [
        "total_low",
        "total_expected",
        "total_high",
        "input_total_expected",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
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
            writer.writerow(row)

    json_rows = []
    for est in estimates:
        row = est.__dict__.copy()
        row["input_total_expected"] = est.text_input_tokens + est.cached_input_tokens + est.image_input_tokens_expected
        row["total_low"] = est.text_input_tokens + est.cached_input_tokens + est.image_input_tokens_low + est.output_tokens_low
        row["total_expected"] = row["input_total_expected"] + est.output_tokens_expected
        row["total_high"] = math.ceil(est.text_input_tokens * 1.2) + est.cached_input_tokens + est.image_input_tokens_high + est.output_tokens_high
        json_rows.append(row)
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(json_rows, indent=2), encoding="utf-8")

    total_expected = sum(row["total_expected"] for row in json_rows)
    total_low = sum(row["total_low"] for row in json_rows)
    total_high = sum(row["total_high"] for row in json_rows)
    md = [
        "# Token Usage Estimate",
        "",
        "Exact Responses token-count endpoint calls and model usage objects were not available because no API key/runtime usage object was exposed. This file uses local text-token heuristics plus an OpenAI-style high-detail image tiling estimate for each planned image payload.",
        "",
        "| Document | Iteration | Call | Actor | Input expected | Cached input | Output expected | Image expected | Total low | Total expected | Total high |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in json_rows:
        md.append(
            f"| {row['document']} | {row['iteration']} | {row['call']} | {row['actor']} | "
            f"{row['input_total_expected']} | {row['cached_input_tokens']} | {row['output_tokens_expected']} | "
            f"{row['image_input_tokens_expected']} | {row['total_low']} | {row['total_expected']} | {row['total_high']} |"
        )
    md += [
        f"| 39 | 1 | **TOTAL** | all |  |  |  |  | **{total_low}** | **{total_expected}** | **{total_high}** |",
        "",
        "Reasoning tokens: not available from the subagent tool responses.",
        "Cached input tokens: recorded as 0 because cache accounting was not exposed.",
    ]
    (RESULTS / "token_usage_estimate.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def write_consensus_notes() -> None:
    edge_lines = [f"- {a} -- {b}" for a, b in FINAL_EDGES]
    notes = [
        "# Document 39 Consensus Notes",
        "",
        "Final graph saturated after Diego R1 -> Jennifer R1 -> Diego R2. Jennifer final confirmation was requested as R2; the saved final matrix follows the saturated Jennifer R1 / Diego R2 graph.",
        "",
        f"- Final node count: {len(FINAL_NODES)}",
        f"- Final edge count: {len(FINAL_EDGES)}",
        "- Matrix type: undirected, symmetric, diagonal zero.",
        "- Source restriction: only files in Raw + wires were used.",
        "- OCR restriction: no off-the-shelf OCR was used.",
        "",
        "## Precision Decisions",
        "",
        "- `CONTROL-ROOM-ANNUNCIATION` was treated as a route/area label, not a component node.",
        "- `ANN-CR01 -- REC-SOE01` was retained as the only direct annunciation edge.",
        "- `JB-A101` and `JB-B101` were retained only for RPS/MOV control circuits; no JB-to-annunciation edge was retained.",
        "- `GND-PLANT` was retained only as connected to `BUS-480-A/LC-A`.",
        "- `LC-A` and `LC-B` were merged into the corresponding 480 V bus/load-center nodes.",
        "- Direct RPS-to-MOV edges were omitted; visible/control-schedule evidence supports RPS-to-JB and JB-to-MOV.",
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
        "document": 39,
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
