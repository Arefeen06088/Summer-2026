from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_nuclear_distribution_schematic.png"
DOCUMENT = "40"
ITERATION = "1"


FINAL_NODES = [
    "DG-21A",
    "UAT-2A",
    "DS-21A",
    "ATS-21A",
    "SWGR-21A",
    "CB-21A1",
    "TR-21A",
    "MCC-21A",
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
    "VT-21A",
    "CT-21A",
    "LOCA-SIG-A",
    "JB-21A",
    "RPS-PNL-A",
    "RELAY-K21A",
    "RELAY-86A",
    "TIE-BKR-21AB",
    "SWGR-21B",
    "DG-21B",
    "SAT-2B",
    "DS-21B",
    "ATS-21B",
    "CB-21B1",
    "TR-21B",
    "MCC-21B",
    "XFMR-CPT21B",
    "AC-PNL-120B",
    "RECT-21B",
    "DC-BUS-21B",
    "BAT-21B",
    "INV-21B",
    "CB-MPB1",
    "PUMP-SI21B",
    "PUMP-CCW21B",
    "FAN-RB21B",
    "MOV-HV211B",
    "MOV-RWST21B",
    "VT-21B",
    "CT-21B",
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
    ("SWGR-21A", "CB-21A1"),
    ("CB-21A1", "TR-21A"),
    ("TR-21A", "MCC-21A"),
    ("SWGR-21A", "TIE-BKR-21AB"),
    ("TIE-BKR-21AB", "SWGR-21B"),
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
    ("BAT-21A", "DC-BUS-21A"),
    ("INV-21A", "DC-BUS-21A"),
    ("LOCA-SIG-A", "JB-21A"),
    ("JB-21A", "RPS-PNL-A"),
    ("CT-21A", "RPS-PNL-A"),
    ("VT-21A", "RPS-PNL-A"),
    ("INV-21A", "RPS-PNL-A"),
    ("RPS-PNL-A", "RELAY-K21A"),
    ("RELAY-K21A", "RELAY-86A"),
    ("RELAY-86A", "CB-MPA1"),
    ("DG-21B", "ATS-21B"),
    ("SAT-2B", "DS-21B"),
    ("DS-21B", "ATS-21B"),
    ("ATS-21B", "SWGR-21B"),
    ("SWGR-21B", "CB-21B1"),
    ("CB-21B1", "TR-21B"),
    ("TR-21B", "MCC-21B"),
    ("MCC-21B", "XFMR-CPT21B"),
    ("XFMR-CPT21B", "AC-PNL-120B"),
    ("AC-PNL-120B", "RECT-21B"),
    ("RECT-21B", "DC-BUS-21B"),
    ("BAT-21B", "DC-BUS-21B"),
    ("INV-21B", "DC-BUS-21B"),
    ("MCC-21B", "CB-MPB1"),
    ("CB-MPB1", "PUMP-SI21B"),
    ("MCC-21B", "PUMP-CCW21B"),
    ("MCC-21B", "FAN-RB21B"),
    ("MCC-21B", "MOV-HV211B"),
    ("MCC-21B", "MOV-RWST21B"),
    ("LOCA-SIG-B", "JB-21B"),
    ("JB-21B", "RPS-PNL-B"),
    ("CT-21B", "RPS-PNL-B"),
    ("VT-21B", "RPS-PNL-B"),
    ("INV-21B", "RPS-PNL-B"),
    ("RPS-PNL-B", "RELAY-K21B"),
    ("RELAY-K21B", "RELAY-86B"),
    ("RELAY-86B", "CB-MPB1"),
]


HIGH_RECALL_REVIEW_EXTRAS = [
    ("MOV-RWST21A", "RPS-PNL-A"),
    ("MOV-RWST21B", "RPS-PNL-B"),
    ("DC-BUS-21A", "RPS-PNL-A"),
    ("DC-BUS-21B", "RPS-PNL-B"),
    ("SWGR-21A", "VT-21A"),
    ("SWGR-21B", "VT-21B"),
    ("MCC-21A", "CT-21A"),
    ("FAN-RB21A", "CT-21A"),
    ("MCC-21B", "CT-21B"),
    ("FAN-RB21B", "CT-21B"),
]


ROUNDS = [
    {
        "round": "01",
        "agent": "Diego",
        "stage": "high_recall",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES + HIGH_RECALL_REVIEW_EXTRAS,
        "notes": "High-recall graph retained visually plausible review extras before precision pruning.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "stage": "precision_review",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Precision review removed unsupported crossing/nearby-line candidates without junction dots.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "stage": "saturation",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Diego accepted Jennifer's refined graph.",
    },
    {
        "round": "04",
        "agent": "Jennifer",
        "stage": "final",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Jennifer confirmed graph content and corrected the bookkeeping count to 56 edges.",
    },
]


TOKEN_CALLS = [
    {
        "call_id": "main-setup-crops-and-raw-inspection",
        "agent": "Main",
        "purpose": "Read task, enforce raw-only scope, create and inspect raw-derived crops.",
        "model_call_count": 2,
        "input_tokens_expected": 15000,
        "input_tokens_low": 10500,
        "input_tokens_high": 21500,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 1800,
        "output_tokens_low": 1100,
        "output_tokens_high": 3100,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 8500,
        "usage_source": "Estimated from visible task context, crop count, and image inspection payloads.",
    },
    {
        "call_id": "diego-round-01-high-recall",
        "agent": "Diego",
        "purpose": "High-recall extraction from the raw sheet and raw-derived crops.",
        "model_call_count": 1,
        "input_tokens_expected": 23000,
        "input_tokens_low": 16500,
        "input_tokens_high": 33000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 5400,
        "output_tokens_low": 3500,
        "output_tokens_high": 8500,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 14000,
        "usage_source": "Estimated from Diego prompt size, crop/image payloads, and response length.",
    },
    {
        "call_id": "jennifer-round-02-precision",
        "agent": "Jennifer",
        "purpose": "Precision review of Diego graph and pruning of unsupported extras.",
        "model_call_count": 1,
        "input_tokens_expected": 26500,
        "input_tokens_low": 19000,
        "input_tokens_high": 38000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 4500,
        "output_tokens_low": 2800,
        "output_tokens_high": 7200,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 15500,
        "usage_source": "Estimated from Diego proposal, crop/image payloads, and reviewer response length.",
    },
    {
        "call_id": "diego-round-03-saturation",
        "agent": "Diego",
        "purpose": "Saturation check of Jennifer's refined graph.",
        "model_call_count": 1,
        "input_tokens_expected": 14500,
        "input_tokens_low": 10500,
        "input_tokens_high": 21000,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 550,
        "output_tokens_low": 250,
        "output_tokens_high": 1100,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "usage_source": "Estimated from compact saturation payload and short response.",
    },
    {
        "call_id": "jennifer-round-04-final",
        "agent": "Jennifer",
        "purpose": "Final confirmation of row/column labels and edge set.",
        "model_call_count": 1,
        "input_tokens_expected": 13000,
        "input_tokens_low": 9500,
        "input_tokens_high": 19000,
        "cached_input_tokens_expected": 2500,
        "output_tokens_expected": 650,
        "output_tokens_low": 250,
        "output_tokens_high": 1300,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "usage_source": "Estimated from final confirmation payload and short correction response.",
    },
    {
        "call_id": "diego-round-05-count-reconciliation",
        "agent": "Diego",
        "purpose": "Confirm Jennifer's count correction from 57 to 56 edges without graph changes.",
        "model_call_count": 1,
        "input_tokens_expected": 3500,
        "input_tokens_low": 2500,
        "input_tokens_high": 5500,
        "cached_input_tokens_expected": 1000,
        "output_tokens_expected": 120,
        "output_tokens_low": 50,
        "output_tokens_high": 300,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "usage_source": "Estimated from short reconciliation message and acknowledgement.",
    },
    {
        "call_id": "main-output-generation-and-finalization",
        "agent": "Main",
        "purpose": "Write matrices, edge lists, validation JSON, notes, token tracking, and final response.",
        "model_call_count": 2,
        "input_tokens_expected": 19000,
        "input_tokens_low": 13000,
        "input_tokens_high": 27000,
        "cached_input_tokens_expected": 5500,
        "output_tokens_expected": 6500,
        "output_tokens_low": 4200,
        "output_tokens_high": 10500,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "usage_source": "Estimated from artifact-generation context, source text, and final response.",
    },
]


def canonical_edge(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return (a, b) if a <= b else (b, a)


def matrix_for(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        matrix[index[a]][index[b]] = 1
        matrix[index[b]][index[a]] = 1
    return matrix


def validate_graph(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, object]:
    errors: list[str] = []
    if len(nodes) != len(set(nodes)):
        errors.append("Duplicate node labels found.")
    node_set = set(nodes)
    canonical_seen: set[tuple[str, str]] = set()
    for edge in edges:
        a, b = edge
        if a not in node_set or b not in node_set:
            errors.append(f"Edge endpoint outside node list: {a} -- {b}")
        if a == b:
            errors.append(f"Self-loop present without justification: {a}")
        ce = canonical_edge(edge)
        if ce in canonical_seen:
            errors.append(f"Duplicate undirected edge: {a} -- {b}")
        canonical_seen.add(ce)
    matrix = matrix_for(nodes, edges)
    for i, row in enumerate(matrix):
        if row[i] != 0:
            errors.append(f"Diagonal entry not zero for {nodes[i]}")
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                errors.append(f"Matrix asymmetry at {nodes[i]} / {nodes[j]}")
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "matrix_size": [len(nodes), len(nodes)],
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(nodes))),
        "symmetric": all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes))),
        "errors": errors,
        "valid": not errors,
    }


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "component"])
        for i, node in enumerate(nodes, 1):
            writer.writerow([i, node])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        for a, b in edges:
            writer.writerow([a, b])


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = matrix_for(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def token_total(row: dict[str, object], band: str) -> int:
    input_key = f"input_tokens_{band}"
    output_key = f"output_tokens_{band}"
    image_key = "image_file_input_tokens_expected"
    reasoning = row.get("reasoning_tokens_expected") or 0
    return int(row[input_key]) + int(row[output_key]) + int(row[image_key]) + int(reasoning)


def write_token_files() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for call in TOKEN_CALLS:
        row = {
            "document": DOCUMENT,
            "iteration": ITERATION,
            **call,
            "total_tokens_low": token_total(call, "low"),
            "total_tokens_expected": token_total(call, "expected"),
            "total_tokens_high": token_total(call, "high"),
            "actual_usage_available": "no",
        }
        rows.append(row)

    fieldnames = [
        "document",
        "iteration",
        "call_id",
        "agent",
        "purpose",
        "model_call_count",
        "input_tokens_expected",
        "input_tokens_low",
        "input_tokens_high",
        "cached_input_tokens_expected",
        "output_tokens_expected",
        "output_tokens_low",
        "output_tokens_high",
        "reasoning_tokens_expected",
        "image_file_input_tokens_expected",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_available",
        "usage_source",
    ]
    for filename in [
        "token_usage_estimates_by_call.csv",
        "token_performance_tracking.csv",
        "token_performance_traking.csv",
    ]:
        with (RESULTS_DIR / filename).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "model_call_count": sum(int(row["model_call_count"]) for row in rows),
        "input_tokens_low": sum(int(row["input_tokens_low"]) for row in rows),
        "input_tokens_expected": sum(int(row["input_tokens_expected"]) for row in rows),
        "input_tokens_high": sum(int(row["input_tokens_high"]) for row in rows),
        "cached_input_tokens_expected": sum(int(row["cached_input_tokens_expected"]) for row in rows),
        "output_tokens_low": sum(int(row["output_tokens_low"]) for row in rows),
        "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in rows),
        "output_tokens_high": sum(int(row["output_tokens_high"]) for row in rows),
        "image_file_input_tokens_expected": sum(int(row["image_file_input_tokens_expected"]) for row in rows),
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "actual_usage_available": "no",
    }
    summary_fields = list(summary.keys())
    with (RESULTS_DIR / "token_usage_summary_by_document.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerow(summary)

    manifest = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "responses_input_token_count_endpoint": {
            "attempted": False,
            "reason": "OPENAI_API_KEY was not available in the execution environment; no authenticated Responses input-token counting request could be made.",
        },
        "actual_usage_collection": {
            "available": False,
            "reason": "Main-agent and subagent per-response usage objects are not exposed through the available Codex tools.",
        },
        "estimate_method": "Low/expected/high estimates use visible prompt/response sizes, local image/crop payload count, and typical image-token ranges. Reasoning-token counts were not available.",
        "summary_totals": summary,
    }
    with (RESULTS_DIR / "responses_input_token_count_manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    return summary


def write_rounds() -> list[dict[str, object]]:
    summary_rows = []
    for item in ROUNDS:
        prefix = f"round_{item['round']}_{item['agent'].lower()}_{item['stage']}"
        nodes = item["nodes"]
        edges = item["edges"]
        write_nodes(RESULTS_DIR / f"{prefix}_nodes.csv", nodes)
        write_edges(RESULTS_DIR / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS_DIR / f"{prefix}_matrix.csv", nodes, edges)
        validation = validate_graph(nodes, edges)
        summary_rows.append(
            {
                "round": item["round"],
                "agent": item["agent"],
                "stage": item["stage"],
                "node_count": validation["node_count"],
                "edge_count": validation["edge_count"],
                "valid": validation["valid"],
                "notes": item["notes"],
            }
        )

    with (RESULTS_DIR / "all_rounds_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["round", "agent", "stage", "node_count", "edge_count", "valid", "notes"],
        )
        writer.writeheader()
        writer.writerows(summary_rows)
    return summary_rows


def write_note(validation: dict[str, object], round_summary: list[dict[str, object]], token_summary: dict[str, object]) -> None:
    pruned = "\n".join(f"- `{a} -- {b}`" for a, b in HIGH_RECALL_REVIEW_EXTRAS)
    final_edges = "\n".join(f"- `{a} -- {b}`" for a, b in FINAL_EDGES)
    round_lines = "\n".join(
        f"- Round {row['round']} {row['agent']} `{row['stage']}`: {row['node_count']} nodes, {row['edge_count']} edges, valid={row['valid']}"
        for row in round_summary
    )
    token_lines = "\n".join(
        f"- Expected total tokens: {token_summary['total_tokens_expected']} "
        f"(low {token_summary['total_tokens_low']}, high {token_summary['total_tokens_high']}); "
        f"model calls counted: {token_summary['model_call_count']}."
    )
    content = f"""# Connectivity Extraction Note - Document {DOCUMENT}

Generated: {datetime.now().isoformat(timespec="seconds")}

## Scope

- Raw resource folder: `{RAW_DIR}`
- Raw image: `{RAW_IMAGE.name}`
- Constraint followed: Diego and Jennifer used only the Raw/Input resources. Ground Truth and GT-derived feedback were not used.
- Derived sibling folders outside `Raw` were not used for extraction.

## Agent Rounds

{round_lines}

Diego's high-recall round carried review-only extras where nearby lines or crossings could be visually tempting. Jennifer pruned them because the schematic legend states that a dot denotes a junction and a line crossing without a dot is not a connection.

## Final Result

- Final node count: {validation['node_count']}
- Final edge count: {validation['edge_count']}
- Matrix: {validation['matrix_size'][0]} x {validation['matrix_size'][1]}
- Symmetric: {validation['symmetric']}
- Diagonal zero: {validation['diagonal_zero']}
- Validation errors: {len(validation['errors'])}

## Final Edges

{final_edges}

## Pruned High-Recall Candidates

{pruned}

## Label Notes

- `PUMP-SI21A` and `PUMP-SI21B` are safety-injection pump labels; the middle characters are `SI`, not `S1`.
- The right-side offsite/source label is `SAT-2B`.
- Cable or route labels such as `C21A-01`, `C21B-01`, `D21A-07`, `D21B-07`, `S21A-11`, and `S21B-11` were treated as annotations, not connectivity nodes.

## Token Tracking

{token_lines}

Actual per-response usage objects were not exposed by the available Codex subagent tools. The Responses input-token counting endpoint was not called because `OPENAI_API_KEY` was unavailable in this execution environment. The CSV files therefore contain low/expected/high estimates and explicit `actual_usage_available=no` markers.
"""
    (RESULTS_DIR / "extraction_note.md").write_text(content, encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    final_validation = validate_graph(FINAL_NODES, FINAL_EDGES)
    if not final_validation["valid"]:
        raise SystemExit(f"Final graph failed validation: {final_validation['errors']}")
    if final_validation["node_count"] != 55 or final_validation["edge_count"] != 56:
        raise SystemExit(f"Unexpected final graph size: {final_validation}")

    write_nodes(RESULTS_DIR / "final_nodes.csv", FINAL_NODES)
    write_edges(RESULTS_DIR / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)

    round_summary = write_rounds()

    graph = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "source_image": str(RAW_IMAGE),
        "nodes": FINAL_NODES,
        "edges": [{"source": a, "target": b} for a, b in FINAL_EDGES],
        "pruned_high_recall_candidates": [{"source": a, "target": b} for a, b in HIGH_RECALL_REVIEW_EXTRAS],
        "validation": final_validation,
    }
    with (RESULTS_DIR / "connectivity_graph.json").open("w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
        f.write("\n")

    validation_summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "raw_image": RAW_IMAGE.name,
        "final": final_validation,
        "rounds": round_summary,
        "no_gt_used": True,
        "raw_only_scope": True,
    }
    with (RESULTS_DIR / "validation_summary.json").open("w", encoding="utf-8") as f:
        json.dump(validation_summary, f, indent=2)
        f.write("\n")

    token_summary = write_token_files()
    write_note(final_validation, round_summary, token_summary)

    print(json.dumps({"final": final_validation, "token_summary": token_summary}, indent=2))


if __name__ == "__main__":
    main()
