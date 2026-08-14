from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + components + junctions"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
CODES.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)


DIEGO_R1_NODES = [
    "GRID-230-A",
    "CB-SW-A",
    "TR-SU-A",
    "SU-A",
    "BUS-13K-A",
    "GEN-DG-A",
    "CB-DG-A",
    "TR-EDG-A",
    "EDG-A",
    "CB-13-TIE",
    "BUS-13K-B",
    "SU-B",
    "TR-SU-B",
    "CB-SW-B",
    "GRID-230-B",
    "EDG-B",
    "TR-EDG-B",
    "CB-DG-B",
    "GEN-DG-B",
    "TR-4K-A",
    "CB-4K-A",
    "BUS-4K-A",
    "CB-4K-TIE",
    "BUS-4K-B",
    "CB-4K-B",
    "TR-4K-B",
    "TR-480-A",
    "CB-LC-A",
    "BUS-480-A",
    "LC-A1",
    "MCC-01A",
    "PUMP-RHR-A",
    "MOTOR-CCW-A",
    "LC-A2",
    "MCC-02A",
    "PUMP-AFW-A",
    "VALVE-MOV-A",
    "FAN-CONTAIN-A",
    "RECT-125A",
    "BUS-DC125-A",
    "BAT-125A",
    "INV-120A",
    "JB-ESF-A",
    "PNL-ESF-A",
    "PNL-RPS-1",
    "RPS-TRIP",
    "RPS-LOCKOUT",
    "TR-480-B",
    "CB-LC-B",
    "BUS-480-B",
    "LC-B1",
    "MCC-01B",
    "PUMP-RHR-B",
    "MOTOR-CCW-B",
    "LC-B2",
    "MCC-02B",
    "PUMP-AFW-B",
    "VALVE-MOV-B",
    "FAN-CONTAIN-B",
    "RECT-125B",
    "BUS-DC125-B",
    "BAT-125B",
    "INV-120B",
    "JB-ESF-B",
    "PNL-ESF-B",
]

FINAL_NODES = [
    "GRID-230-A",
    "CB-SW-A",
    "TR-SU-A",
    "SU-A",
    "BUS-13K-A",
    "GEN-DG-A",
    "CB-DG-A",
    "TR-EDG-A",
    "EDG-A",
    "CB-13-TIE",
    "BUS-13K-B",
    "SU-B",
    "TR-SU-B",
    "CB-SW-B",
    "GRID-230-B",
    "EDG-B",
    "TR-EDG-B",
    "CB-DG-B",
    "GEN-DG-B",
    "TR-4K-A",
    "CB-4K-A",
    "BUS-4K-A",
    "CB-4K-TIE",
    "BUS-4K-B",
    "CB-4K-B",
    "TR-4K-B",
    "TR-480-A",
    "CB-LC-A",
    "BUS-480-A",
    "LC-A1",
    "MCC-01A",
    "PUMP-RHR-A",
    "MOTOR-CCW-A",
    "LC-A2",
    "MCC-02A",
    "PUMP-AFW-A",
    "VALVE-MOV-A",
    "FAN-CONTAIN-A",
    "RECT-125A",
    "BUS-DC125-A",
    "BAT-125A",
    "INV-120A",
    "JB-ESF-A",
    "PNL-ESF-A",
    "PNL-RPS-1",
    "TR-480-B",
    "CB-LC-B",
    "BUS-480-B",
    "LC-B1",
    "MCC-01B",
    "PUMP-RHR-B",
    "MOTOR-CCW-B",
    "LC-B2",
    "MCC-02B",
    "PUMP-AFW-B",
    "VALVE-MOV-B",
    "FAN-CONTAIN-B",
    "RECT-125B",
    "BUS-DC125-B",
    "BAT-125B",
    "INV-120B",
    "JB-ESF-B",
    "PNL-ESF-B",
]

POWER_EDGES = [
    ("GRID-230-A", "CB-SW-A"),
    ("CB-SW-A", "TR-SU-A"),
    ("TR-SU-A", "SU-A"),
    ("SU-A", "BUS-13K-A"),
    ("GEN-DG-A", "CB-DG-A"),
    ("CB-DG-A", "TR-EDG-A"),
    ("TR-EDG-A", "EDG-A"),
    ("EDG-A", "BUS-13K-A"),
    ("BUS-13K-A", "CB-13-TIE"),
    ("CB-13-TIE", "BUS-13K-B"),
    ("BUS-13K-B", "SU-B"),
    ("SU-B", "TR-SU-B"),
    ("TR-SU-B", "CB-SW-B"),
    ("CB-SW-B", "GRID-230-B"),
    ("BUS-13K-B", "EDG-B"),
    ("EDG-B", "TR-EDG-B"),
    ("TR-EDG-B", "CB-DG-B"),
    ("CB-DG-B", "GEN-DG-B"),
    ("BUS-13K-A", "TR-4K-A"),
    ("TR-4K-A", "CB-4K-A"),
    ("CB-4K-A", "BUS-4K-A"),
    ("BUS-13K-B", "TR-4K-B"),
    ("TR-4K-B", "CB-4K-B"),
    ("CB-4K-B", "BUS-4K-B"),
    ("BUS-4K-A", "CB-4K-TIE"),
    ("CB-4K-TIE", "BUS-4K-B"),
    ("BUS-4K-A", "TR-480-A"),
    ("TR-480-A", "CB-LC-A"),
    ("CB-LC-A", "BUS-480-A"),
    ("BUS-480-A", "LC-A1"),
    ("LC-A1", "MCC-01A"),
    ("MCC-01A", "PUMP-RHR-A"),
    ("MCC-01A", "MOTOR-CCW-A"),
    ("BUS-480-A", "LC-A2"),
    ("LC-A2", "MCC-02A"),
    ("MCC-02A", "PUMP-AFW-A"),
    ("MCC-02A", "VALVE-MOV-A"),
    ("MCC-02A", "FAN-CONTAIN-A"),
    ("BUS-480-A", "RECT-125A"),
    ("RECT-125A", "BUS-DC125-A"),
    ("BUS-DC125-A", "BAT-125A"),
    ("BUS-DC125-A", "INV-120A"),
    ("INV-120A", "PNL-ESF-A"),
    ("BUS-4K-B", "TR-480-B"),
    ("TR-480-B", "CB-LC-B"),
    ("CB-LC-B", "BUS-480-B"),
    ("BUS-480-B", "LC-B1"),
    ("LC-B1", "MCC-01B"),
    ("MCC-01B", "PUMP-RHR-B"),
    ("MCC-01B", "MOTOR-CCW-B"),
    ("BUS-480-B", "LC-B2"),
    ("LC-B2", "MCC-02B"),
    ("MCC-02B", "PUMP-AFW-B"),
    ("MCC-02B", "VALVE-MOV-B"),
    ("MCC-02B", "FAN-CONTAIN-B"),
    ("BUS-480-B", "RECT-125B"),
    ("RECT-125B", "BUS-DC125-B"),
    ("BUS-DC125-B", "BAT-125B"),
    ("BUS-DC125-B", "INV-120B"),
    ("INV-120B", "PNL-ESF-B"),
]

DIEGO_R1_CONTROL_EDGES = [
    ("CB-13-TIE", "RPS-TRIP"),
    ("RPS-TRIP", "PNL-RPS-1"),
    ("CB-4K-TIE", "RPS-LOCKOUT"),
    ("RPS-LOCKOUT", "PNL-RPS-1"),
    ("JB-ESF-A", "PNL-ESF-A"),
    ("JB-ESF-B", "PNL-ESF-B"),
    ("PNL-ESF-A", "PUMP-AFW-A"),
    ("PNL-ESF-A", "VALVE-MOV-A"),
    ("PNL-ESF-B", "PUMP-AFW-B"),
    ("PNL-ESF-B", "VALVE-MOV-B"),
]

FINAL_CONTROL_EDGES = [
    ("CB-13-TIE", "PNL-RPS-1"),
    ("CB-4K-TIE", "PNL-RPS-1"),
    ("JB-ESF-A", "PNL-ESF-A"),
    ("JB-ESF-B", "PNL-ESF-B"),
    ("PNL-ESF-A", "PUMP-AFW-A"),
    ("PNL-ESF-A", "VALVE-MOV-A"),
    ("PNL-ESF-B", "PUMP-AFW-B"),
    ("PNL-ESF-B", "VALVE-MOV-B"),
]


ROUNDS = [
    {
        "round": 1,
        "agent": "Diego",
        "label": "high_recall",
        "nodes": DIEGO_R1_NODES,
        "power_edges": POWER_EDGES,
        "control_edges": DIEGO_R1_CONTROL_EDGES,
        "notes": "High-recall proposal included annotation labels RPS-TRIP and RPS-LOCKOUT as tentative logical nodes.",
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "label": "precision_review",
        "nodes": FINAL_NODES,
        "power_edges": POWER_EDGES,
        "control_edges": FINAL_CONTROL_EDGES,
        "notes": "Removed RPS-TRIP/RPS-LOCKOUT as nodes; included visibly terminated dashed control/interlock wires; excluded fan control edges.",
    },
    {
        "round": 3,
        "agent": "Diego",
        "label": "saturation_check",
        "nodes": FINAL_NODES,
        "power_edges": POWER_EDGES,
        "control_edges": FINAL_CONTROL_EDGES,
        "notes": "Agreed with Jennifer: RPS labels are annotations and fan control taps are not visually supported.",
    },
    {
        "round": 4,
        "agent": "Jennifer",
        "label": "final_confirmation",
        "nodes": FINAL_NODES,
        "power_edges": POWER_EDGES,
        "control_edges": FINAL_CONTROL_EDGES,
        "notes": "Final consensus achieved with very low visual uncertainty.",
    },
]


TOKEN_ROWS = [
    {
        "document": 36,
        "iteration": 1,
        "call": "Main agent orchestration and visual inspection",
        "model_call_count": 1,
        "input_tokens_est": 9500,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 9000,
        "output_tokens_est": 4500,
        "reasoning_tokens": "unavailable",
        "low_total_est": 18000,
        "expected_total_est": 23000,
        "high_total_est": 30000,
        "method": "Local approximation from prompt/context text plus image-tile heuristic; no API key available.",
    },
    {
        "document": 36,
        "iteration": 1,
        "call": "Diego R1 high-recall extraction",
        "model_call_count": 1,
        "input_tokens_est": 22000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 16000,
        "output_tokens_est": 4200,
        "reasoning_tokens": "unavailable",
        "low_total_est": 22000,
        "expected_total_est": 26200,
        "high_total_est": 34000,
        "method": "Local approximation; actual subagent usage object not exposed.",
    },
    {
        "document": 36,
        "iteration": 1,
        "call": "Jennifer R1 precision review",
        "model_call_count": 1,
        "input_tokens_est": 27000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 18000,
        "output_tokens_est": 2400,
        "reasoning_tokens": "unavailable",
        "low_total_est": 25000,
        "expected_total_est": 29400,
        "high_total_est": 38000,
        "method": "Local approximation; actual subagent usage object not exposed.",
    },
    {
        "document": 36,
        "iteration": 1,
        "call": "Diego R2 saturation check",
        "model_call_count": 1,
        "input_tokens_est": 19000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 10500,
        "output_tokens_est": 1500,
        "reasoning_tokens": "unavailable",
        "low_total_est": 17000,
        "expected_total_est": 20500,
        "high_total_est": 27000,
        "method": "Local approximation; actual subagent usage object not exposed.",
    },
    {
        "document": 36,
        "iteration": 1,
        "call": "Jennifer R2 final confirmation",
        "model_call_count": 1,
        "input_tokens_est": 13000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 7000,
        "output_tokens_est": 120,
        "reasoning_tokens": "unavailable",
        "low_total_est": 11000,
        "expected_total_est": 13120,
        "high_total_est": 17000,
        "method": "Local approximation; actual subagent usage object not exposed.",
    },
]


def dedupe_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str]] = []
    for a, b in edges:
        key = tuple(sorted((a, b)))
        if a == b or key in seen:
            continue
        seen.add(key)
        result.append((a, b))
    return result


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for idx, node in enumerate(nodes, start=1):
            writer.writerow([idx, node])


def write_edges(path: Path, power_edges: list[tuple[str, str]], control_edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "edge_type"])
        for source, target in dedupe_edges(power_edges):
            writer.writerow([source, target, "power"])
        for source, target in dedupe_edges(control_edges):
            writer.writerow([source, target, "control"])


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    node_set = set(nodes)
    missing = sorted({n for edge in edges for n in edge if n not in node_set})
    if missing:
        raise ValueError(f"Edges reference nodes not in node list: {missing}")
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in dedupe_edges(edges):
        i, j = index[a], index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_graph_json(
    path: Path,
    nodes: list[str],
    power_edges: list[tuple[str, str]],
    control_edges: list[tuple[str, str]],
    note: str,
) -> None:
    graph = {
        "document": 36,
        "iteration": 1,
        "node_count": len(nodes),
        "edge_count": len(dedupe_edges(power_edges + control_edges)),
        "nodes": nodes,
        "edges": [
            {"source": a, "target": b, "edge_type": "power"} for a, b in dedupe_edges(power_edges)
        ]
        + [
            {"source": a, "target": b, "edge_type": "control"} for a, b in dedupe_edges(control_edges)
        ],
        "note": note,
    }
    path.write_text(json.dumps(graph, indent=2), encoding="utf-8")


def write_round_outputs() -> None:
    for spec in ROUNDS:
        prefix = f"round_{spec['round']:02d}_{spec['agent'].lower()}_{spec['label']}"
        nodes = spec["nodes"]
        power_edges = spec["power_edges"]
        control_edges = spec["control_edges"]
        all_edges = dedupe_edges(power_edges + control_edges)
        write_nodes(RESULTS / f"{prefix}_nodes.csv", nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", power_edges, control_edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, all_edges)
        write_graph_json(RESULTS / f"{prefix}_graph.json", nodes, power_edges, control_edges, spec["notes"])


def write_final_outputs() -> None:
    all_edges = dedupe_edges(POWER_EDGES + FINAL_CONTROL_EDGES)
    if len(FINAL_NODES) != 63:
        raise ValueError(f"Expected 63 final nodes, got {len(FINAL_NODES)}")
    if len(all_edges) != 68:
        raise ValueError(f"Expected 68 final edges, got {len(all_edges)}")
    write_nodes(RESULTS / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS / "final_edges.csv", POWER_EDGES, FINAL_CONTROL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, all_edges)
    write_graph_json(
        RESULTS / "final_graph.json",
        FINAL_NODES,
        POWER_EDGES,
        FINAL_CONTROL_EDGES,
        "Final consensus after Diego high-recall and Jennifer precision review. Matrix includes solid power wires plus visibly terminated dashed control/interlock wires.",
    )


def write_summary_outputs() -> None:
    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "round", "agent", "label", "node_count", "edge_count", "notes"])
        for spec in ROUNDS:
            writer.writerow(
                [
                    36,
                    1,
                    spec["round"],
                    spec["agent"],
                    spec["label"],
                    len(spec["nodes"]),
                    len(dedupe_edges(spec["power_edges"] + spec["control_edges"])),
                    spec["notes"],
                ]
            )

    token_fields = list(TOKEN_ROWS[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=token_fields)
        writer.writeheader()
        writer.writerows(TOKEN_ROWS)
        total = {
            "document": 36,
            "iteration": 1,
            "call": "TOTAL",
            "model_call_count": sum(row["model_call_count"] for row in TOKEN_ROWS),
            "input_tokens_est": sum(row["input_tokens_est"] for row in TOKEN_ROWS),
            "cached_input_tokens": "unavailable",
            "image_file_input_tokens_est": sum(row["image_file_input_tokens_est"] for row in TOKEN_ROWS),
            "output_tokens_est": sum(row["output_tokens_est"] for row in TOKEN_ROWS),
            "reasoning_tokens": "unavailable",
            "low_total_est": sum(row["low_total_est"] for row in TOKEN_ROWS),
            "expected_total_est": sum(row["expected_total_est"] for row in TOKEN_ROWS),
            "high_total_est": sum(row["high_total_est"] for row in TOKEN_ROWS),
            "method": "Sum of local estimates.",
        }
        writer.writerow(total)

    payload = {
        "document": 36,
        "iteration": 1,
        "calls": TOKEN_ROWS,
        "totals": {
            "model_call_count": sum(row["model_call_count"] for row in TOKEN_ROWS),
            "input_tokens_est": sum(row["input_tokens_est"] for row in TOKEN_ROWS),
            "image_file_input_tokens_est": sum(row["image_file_input_tokens_est"] for row in TOKEN_ROWS),
            "output_tokens_est": sum(row["output_tokens_est"] for row in TOKEN_ROWS),
            "low_total_est": sum(row["low_total_est"] for row in TOKEN_ROWS),
            "expected_total_est": sum(row["expected_total_est"] for row in TOKEN_ROWS),
            "high_total_est": sum(row["high_total_est"] for row in TOKEN_ROWS),
        },
        "limitations": [
            "No OpenAI API key was available, so the Responses input-token counting endpoint was not called.",
            "Subagent usage objects were not exposed to the main agent; values are local estimates.",
            "Cached input and reasoning-token counts are unavailable.",
        ],
    }
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_notes() -> None:
    notes = f"""# Document 36 Connectivity Extraction

Generated: {datetime.now().isoformat(timespec="seconds")}

Allowed resources used: files under `{BASE}` only. No GT or GT-derived feedback was used.

## Consensus

Diego R1 produced a high-recall graph. Jennifer R1 removed annotation-only RPS labels as nodes and refined control/interlock connectivity. Diego R2 agreed the correction was saturated. Jennifer R2 gave final confirmation.

Final matrix:
- Nodes: 63
- Edges: 68
- Symmetric undirected matrix with zero diagonal
- Includes solid power conductors and visibly terminated dashed control/interlock wires
- Excludes dashed enclosure boundaries, un-dotted crossings, EXC annotations, RPS-TRIP/RPS-LOCKOUT as nodes, and FAN-CONTAIN-A/B ESF control edges

## Final Control/Interlock Edges Included

- CB-13-TIE -- PNL-RPS-1
- CB-4K-TIE -- PNL-RPS-1
- JB-ESF-A -- PNL-ESF-A
- JB-ESF-B -- PNL-ESF-B
- PNL-ESF-A -- PUMP-AFW-A
- PNL-ESF-A -- VALVE-MOV-A
- PNL-ESF-B -- PUMP-AFW-B
- PNL-ESF-B -- VALVE-MOV-B

## Token Accounting Note

No API key was available, so the Responses token-counting endpoint could not be used. Actual model response usage objects were not exposed for subagent calls. Token files therefore report a local estimate using approximate text-token counts plus an image-tile heuristic for the crops supplied to each model call.
"""
    (RESULTS / "extraction_notes.md").write_text(notes, encoding="utf-8")


def copy_code_artifacts() -> None:
    this_file = Path(__file__).resolve()
    target = CODES / this_file.name
    if this_file != target:
        shutil.copy2(this_file, target)
    crop_script = this_file.with_name("doc36_make_visual_crops.py")
    if crop_script.exists():
        shutil.copy2(crop_script, CODES / crop_script.name)


def main() -> None:
    write_round_outputs()
    write_final_outputs()
    write_summary_outputs()
    write_notes()
    copy_code_artifacts()
    print(f"Wrote document 36 results to {RESULTS}")
    print(f"Final nodes: {len(FINAL_NODES)}")
    print(f"Final edges: {len(dedupe_edges(POWER_EDGES + FINAL_CONTROL_EDGES))}")


if __name__ == "__main__":
    main()
