from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path


DOCUMENT = 37
ITERATION = 1
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + components + junctions"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
CODES.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)


FINAL_NODES = [
    "GRID-345",
    "CB-101",
    "AUX-TR-1A",
    "CB-102",
    "AUX-TR-1B",
    "BUS-6KA",
    "CB-TIE-6K",
    "BUS-6KB",
    "CB-103A",
    "SWGR-1EA",
    "DG-1A",
    "CB-DG1A",
    "ATS-1A",
    "RELAY-K12A",
    "TR-480A",
    "BUS-480A",
    "MCC-1A",
    "PUMP-SI-1A",
    "PUMP-RHR-1A",
    "PUMP-CCW-1A",
    "FAN-RB-1A",
    "MOV-HPCI-1A",
    "VALVE-SW-1A",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DCA",
    "GND-01A",
    "INV-120A",
    "BUS-120A",
    "PAN-RPS-A",
    "INST-RACK-A",
    "PLC-ESF",
    "CB-103B",
    "SWGR-1EB",
    "DG-1B",
    "CB-DG1B",
    "ATS-1B",
    "RELAY-K12B",
    "TR-480B",
    "BUS-480B",
    "MCC-1B",
    "PUMP-SI-1B",
    "PUMP-RHR-1B",
    "PUMP-CCW-1B",
    "FAN-RB-1B",
    "MOV-HPCI-1B",
    "VALVE-SW-1B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DCB",
    "GND-01B",
    "INV-120B",
    "BUS-120B",
    "PAN-RPS-B",
    "INST-RACK-B",
]


FINAL_EDGES = [
    ("AUX-TR-1A", "CB-101", "power"),
    ("CB-101", "GRID-345", "power"),
    ("GRID-345", "CB-102", "power"),
    ("CB-102", "AUX-TR-1B", "power"),
    ("AUX-TR-1A", "BUS-6KA", "power"),
    ("AUX-TR-1B", "BUS-6KB", "power"),
    ("BUS-6KA", "CB-TIE-6K", "power"),
    ("CB-TIE-6K", "BUS-6KB", "power"),
    ("BUS-6KA", "CB-103A", "power"),
    ("CB-103A", "SWGR-1EA", "power"),
    ("DG-1A", "CB-DG1A", "power"),
    ("CB-DG1A", "SWGR-1EA", "power"),
    ("SWGR-1EA", "ATS-1A", "power"),
    ("ATS-1A", "TR-480A", "power"),
    ("TR-480A", "BUS-480A", "power"),
    ("ATS-1A", "RELAY-K12A", "control"),
    ("BUS-480A", "MCC-1A", "power"),
    ("MCC-1A", "PUMP-SI-1A", "power"),
    ("MCC-1A", "PUMP-RHR-1A", "power"),
    ("MCC-1A", "PUMP-CCW-1A", "power"),
    ("MCC-1A", "FAN-RB-1A", "power"),
    ("MCC-1A", "MOV-HPCI-1A", "power"),
    ("MCC-1A", "VALVE-SW-1A", "power"),
    ("BUS-480A", "CHGR-125A", "power"),
    ("CHGR-125A", "BUS-125DCA", "power"),
    ("BAT-125A", "BUS-125DCA", "power"),
    ("BUS-125DCA", "GND-01A", "dc_ref"),
    ("BUS-125DCA", "INV-120A", "power"),
    ("INV-120A", "BUS-120A", "power"),
    ("BUS-120A", "PAN-RPS-A", "power"),
    ("BUS-120A", "INST-RACK-A", "power"),
    ("BUS-6KB", "CB-103B", "power"),
    ("CB-103B", "SWGR-1EB", "power"),
    ("DG-1B", "CB-DG1B", "power"),
    ("CB-DG1B", "SWGR-1EB", "power"),
    ("SWGR-1EB", "ATS-1B", "power"),
    ("ATS-1B", "TR-480B", "power"),
    ("TR-480B", "BUS-480B", "power"),
    ("ATS-1B", "RELAY-K12B", "control"),
    ("BUS-480B", "MCC-1B", "power"),
    ("MCC-1B", "PUMP-SI-1B", "power"),
    ("MCC-1B", "PUMP-RHR-1B", "power"),
    ("MCC-1B", "PUMP-CCW-1B", "power"),
    ("MCC-1B", "FAN-RB-1B", "power"),
    ("MCC-1B", "MOV-HPCI-1B", "power"),
    ("MCC-1B", "VALVE-SW-1B", "power"),
    ("BUS-480B", "CHGR-125B", "power"),
    ("CHGR-125B", "BUS-125DCB", "power"),
    ("BAT-125B", "BUS-125DCB", "power"),
    ("BUS-125DCB", "GND-01B", "dc_ref"),
    ("BUS-125DCB", "INV-120B", "power"),
    ("INV-120B", "BUS-120B", "power"),
    ("BUS-120B", "PAN-RPS-B", "power"),
    ("BUS-120B", "INST-RACK-B", "power"),
]

GRID_TO_TIE_CANDIDATE = ("GRID-345", "CB-TIE-6K", "power_candidate_removed")
PLC_A_CANDIDATE = ("PAN-RPS-A", "PLC-ESF", "control_candidate_removed")
PLC_B_CANDIDATE = ("PLC-ESF", "PAN-RPS-B", "control_candidate_removed")

ROUNDS = [
    {
        "round": 1,
        "agent": "Diego",
        "label": "high_recall",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES + [GRID_TO_TIE_CANDIDATE, PLC_A_CANDIDATE, PLC_B_CANDIDATE],
        "notes": (
            "High-recall proposal included the possible GRID-345 to CB-TIE-6K source/tie "
            "edge and C03/C06 PLC-ESF dashed routing candidates."
        ),
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "label": "precision_review",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES + [GRID_TO_TIE_CANDIDATE],
        "notes": (
            "Removed C03/C06 PLC-ESF dashed routes as unsupported direct terminations; "
            "kept GRID-345 to CB-TIE-6K for a saturation check."
        ),
    },
    {
        "round": 3,
        "agent": "Diego",
        "label": "saturation_check",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": (
            "Removed GRID-345 to CB-TIE-6K after re-inspection; raw crop shows only "
            "P07/P08 bus-tie conductors through CB-TIE-6K."
        ),
    },
    {
        "round": 4,
        "agent": "Jennifer",
        "label": "final_confirmation",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Final consensus set.",
    },
]


TOKEN_ROWS = [
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call": "Main agent orchestration, local visual inspection, and artifact writing",
        "model_call_count": 3,
        "input_tokens_est": 21000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 14000,
        "output_tokens_est": 6500,
        "reasoning_tokens": "unavailable",
        "low_total_est": 30000,
        "expected_total_est": 41500,
        "high_total_est": 56000,
        "method": "Grouped local estimate; exact internal main-agent continuations and usage objects were not exposed.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call": "Diego R1 high-recall extraction",
        "model_call_count": 1,
        "input_tokens_est": 23000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 17000,
        "output_tokens_est": 3600,
        "reasoning_tokens": "unavailable",
        "low_total_est": 36000,
        "expected_total_est": 43600,
        "high_total_est": 56000,
        "method": "Local approximation; actual subagent usage object was not exposed.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call": "Jennifer R1 precision review",
        "model_call_count": 1,
        "input_tokens_est": 27000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 18000,
        "output_tokens_est": 2600,
        "reasoning_tokens": "unavailable",
        "low_total_est": 40000,
        "expected_total_est": 47600,
        "high_total_est": 62000,
        "method": "Local approximation; actual subagent usage object was not exposed.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call": "Diego R2 saturation check",
        "model_call_count": 1,
        "input_tokens_est": 18000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 10000,
        "output_tokens_est": 1500,
        "reasoning_tokens": "unavailable",
        "low_total_est": 25000,
        "expected_total_est": 29500,
        "high_total_est": 38000,
        "method": "Local approximation; actual subagent usage object was not exposed.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call": "Jennifer R2 final confirmation",
        "model_call_count": 1,
        "input_tokens_est": 15000,
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": 9000,
        "output_tokens_est": 1200,
        "reasoning_tokens": "unavailable",
        "low_total_est": 21000,
        "expected_total_est": 25200,
        "high_total_est": 33000,
        "method": "Local approximation; actual subagent usage object was not exposed.",
    },
]


def dedupe_edges(edges: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str, str]] = []
    for source, target, edge_type in edges:
        key = tuple(sorted((source, target)))
        if source == target or key in seen:
            continue
        seen.add(key)
        result.append((source, target, edge_type))
    return result


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for idx, node in enumerate(nodes, start=1):
            writer.writerow([idx, node])


def write_edges(path: Path, edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "edge_type"])
        writer.writerows(dedupe_edges(edges))


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    node_set = set(nodes)
    missing = sorted({n for source, target, _ in edges for n in (source, target) if n not in node_set})
    if missing:
        raise ValueError(f"Edges reference nodes not in node list: {missing}")
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target, _ in dedupe_edges(edges):
        i, j = index[source], index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_graph_json(path: Path, nodes: list[str], edges: list[tuple[str, str, str]], note: str) -> None:
    clean_edges = dedupe_edges(edges)
    graph = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "node_count": len(nodes),
        "edge_count": len(clean_edges),
        "nodes": nodes,
        "edges": [
            {"source": source, "target": target, "edge_type": edge_type}
            for source, target, edge_type in clean_edges
        ],
        "note": note,
    }
    path.write_text(json.dumps(graph, indent=2), encoding="utf-8")


def write_round_outputs() -> None:
    for spec in ROUNDS:
        prefix = f"round_{spec['round']:02d}_{spec['agent'].lower()}_{spec['label']}"
        nodes = spec["nodes"]
        edges = spec["edges"]
        write_nodes(RESULTS / f"{prefix}_nodes.csv", nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)
        write_graph_json(RESULTS / f"{prefix}_graph.json", nodes, edges, spec["notes"])


def write_final_outputs() -> None:
    final_edges = dedupe_edges(FINAL_EDGES)
    if len(FINAL_NODES) != 55:
        raise ValueError(f"Expected 55 final nodes, got {len(FINAL_NODES)}")
    if len(final_edges) != 54:
        raise ValueError(f"Expected 54 final edges, got {len(final_edges)}")
    write_nodes(RESULTS / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_graph_json(
        RESULTS / "final_graph.json",
        FINAL_NODES,
        FINAL_EDGES,
        (
            "Final consensus after Diego high-recall extraction and Jennifer precision review. "
            "The matrix includes supported solid power conductors, ATS relay dashed controls, "
            "and DC reference taps. It excludes the unsupported GRID-345 to CB-TIE-6K candidate "
            "and C03/C06 PLC-ESF cable-tray routing candidates. PLC-ESF remains as a visible isolated node."
        ),
    )


def write_summary_outputs() -> None:
    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "round", "agent", "label", "node_count", "edge_count", "notes"])
        for spec in ROUNDS:
            writer.writerow(
                [
                    DOCUMENT,
                    ITERATION,
                    spec["round"],
                    spec["agent"],
                    spec["label"],
                    len(spec["nodes"]),
                    len(dedupe_edges(spec["edges"])),
                    spec["notes"],
                ]
            )

    token_fields = list(TOKEN_ROWS[0].keys())
    total = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call": "TOTAL",
        "model_call_count": sum(int(row["model_call_count"]) for row in TOKEN_ROWS),
        "input_tokens_est": sum(int(row["input_tokens_est"]) for row in TOKEN_ROWS),
        "cached_input_tokens": "unavailable",
        "image_file_input_tokens_est": sum(int(row["image_file_input_tokens_est"]) for row in TOKEN_ROWS),
        "output_tokens_est": sum(int(row["output_tokens_est"]) for row in TOKEN_ROWS),
        "reasoning_tokens": "unavailable",
        "low_total_est": sum(int(row["low_total_est"]) for row in TOKEN_ROWS),
        "expected_total_est": sum(int(row["expected_total_est"]) for row in TOKEN_ROWS),
        "high_total_est": sum(int(row["high_total_est"]) for row in TOKEN_ROWS),
        "method": "Sum of local estimates.",
    }
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=token_fields)
        writer.writeheader()
        writer.writerows(TOKEN_ROWS)
        writer.writerow(total)

    payload = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "calls": TOKEN_ROWS,
        "totals": total,
        "limitations": [
            "No OpenAI API key was available, so the Responses input-token counting endpoint was not called.",
            "Subagent usage objects were not exposed to the main agent; values are local estimates.",
            "Cached input and reasoning-token counts are unavailable.",
            "Main-agent system-internal continuations are grouped into one row because exact per-continuation usage was not exposed.",
        ],
    }
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_notes() -> None:
    notes = f"""# Document 37 Connectivity Extraction

Generated: {datetime.now().isoformat(timespec="seconds")}

Allowed resources used: files under `{BASE}` only. No GT or GT-derived feedback was used.

## Consensus

Diego R1 produced a high-recall graph. Jennifer R1 removed unsupported PLC-ESF cable-tray route candidates. Diego R2 re-inspected the top-center source/tie crop and removed GRID-345 -- CB-TIE-6K. Jennifer R2 confirmed the saturated final graph.

Final matrix:
- Nodes: 55
- Edges: 54
- Symmetric undirected matrix with zero diagonal
- Includes solid power conductors, ATS relay dashed control wires, and DC reference taps
- Excludes Pxx/Cxx path labels as nodes
- Excludes GRID-345 -- CB-TIE-6K because the raw crop shows no visible source-to-tie conductor
- Excludes PAN-RPS-A -- PLC-ESF and PLC-ESF -- PAN-RPS-B because C03/C06 look like functional cable-tray/routing paths without clear component-port terminations
- Keeps PLC-ESF as a visible isolated component/logical block

## Final Edge Decisions

- CB-TIE-6K connects BUS-6KA and BUS-6KB only.
- GRID-345 connects through CB-101 and CB-102 to AUX-TR-1A and AUX-TR-1B, but not directly to CB-TIE-6K.
- ATS-1A -- RELAY-K12A and ATS-1B -- RELAY-K12B are retained as visibly terminated dashed control edges.
- GND-01A and GND-01B are retained as DC reference nodes tied to BUS-125DCA and BUS-125DCB.

## Token Accounting Note

No API key was available, so the Responses token-counting endpoint could not be used. Actual model response usage objects were not exposed for the subagent calls. Token files therefore report a local estimate using prompt/context length plus an image/file input heuristic for the crops and source aids reviewed in each round.
"""
    (RESULTS / "extraction_notes.md").write_text(notes, encoding="utf-8")


def copy_code_artifacts() -> None:
    this_file = Path(__file__).resolve()
    target = CODES / this_file.name
    if this_file != target:
        shutil.copy2(this_file, target)
    crop_script = this_file.with_name("doc37_make_visual_crops.py")
    if crop_script.exists():
        shutil.copy2(crop_script, CODES / crop_script.name)


def main() -> None:
    write_round_outputs()
    write_final_outputs()
    write_summary_outputs()
    write_notes()
    copy_code_artifacts()
    print(f"Wrote document {DOCUMENT} results to {RESULTS}")
    print(f"Final nodes: {len(FINAL_NODES)}")
    print(f"Final edges: {len(dedupe_edges(FINAL_EDGES))}")


if __name__ == "__main__":
    main()
