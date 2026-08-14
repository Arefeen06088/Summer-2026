from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic(2).png"
DOCUMENT = "41"
ITERATION = "1"


DIEGO_NODES = [
    "OFFSITE-A-161KV",
    "TR-1A",
    "GND-1E",
    "CB-101",
    "BUS-1A-4.16KV",
    "EDG-1A",
    "CB-105",
    "CB-TIE-1AB",
    "BUS-1B-4.16KV",
    "CB-102",
    "TR-1B",
    "OFFSITE-B-161KV",
    "EDG-1B",
    "CB-106",
    "TR-LC-1A",
    "CB-201",
    "BUS-480A",
    "MCC-1A",
    "PUMP-CCW-103A",
    "MCC-1C",
    "FAN-CRHV-104A",
    "TR-SAF-1A",
    "CB-203",
    "BUS-480E1A",
    "MCC-ESS-A",
    "PUMP-SI-101A",
    "PUMP-RHR-102A",
    "MOV-1201A",
    "TR-LC-1B",
    "CB-202",
    "BUS-480B",
    "MCC-1B",
    "PUMP-CCW-103B",
    "MCC-1D",
    "FAN-CRHV-104B",
    "TR-SAF-1B",
    "CB-204",
    "BUS-480E1B",
    "MCC-ESS-B",
    "PUMP-SI-101B",
    "PUMP-RHR-102B",
    "MOV-1201B",
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-125A",
    "INV-120A",
    "UPS-BUS-A",
    "PANEL-RPS-A",
    "RELAY-K86A",
    "JB-ESF-01-TB1",
    "PANEL-RPS-B",
    "RELAY-K86B",
    "UPS-BUS-B",
    "INV-120B",
    "DC-BUS-125B",
    "BAT-125B",
    "CHGR-125B",
    "INST-RACK-1",
    "CTRL-86A",
    "CTRL-86B",
]


FINAL_NODES = [node for node in DIEGO_NODES if node not in {"CTRL-86A", "CTRL-86B"}]


DIEGO_CONFIRMED_EDGES = [
    ("OFFSITE-A-161KV", "TR-1A"),
    ("TR-1A", "CB-101"),
    ("CB-101", "BUS-1A-4.16KV"),
    ("TR-1A", "GND-1E"),
    ("EDG-1A", "CB-105"),
    ("CB-105", "BUS-1A-4.16KV"),
    ("BUS-1A-4.16KV", "CB-TIE-1AB"),
    ("CB-TIE-1AB", "BUS-1B-4.16KV"),
    ("BUS-1B-4.16KV", "CB-102"),
    ("CB-102", "TR-1B"),
    ("TR-1B", "OFFSITE-B-161KV"),
    ("EDG-1B", "CB-106"),
    ("CB-106", "BUS-1B-4.16KV"),
    ("BUS-1A-4.16KV", "TR-LC-1A"),
    ("TR-LC-1A", "CB-201"),
    ("CB-201", "BUS-480A"),
    ("BUS-1A-4.16KV", "TR-SAF-1A"),
    ("TR-SAF-1A", "CB-203"),
    ("CB-203", "BUS-480E1A"),
    ("BUS-1B-4.16KV", "TR-LC-1B"),
    ("TR-LC-1B", "CB-202"),
    ("CB-202", "BUS-480B"),
    ("BUS-1B-4.16KV", "TR-SAF-1B"),
    ("TR-SAF-1B", "CB-204"),
    ("CB-204", "BUS-480E1B"),
    ("BUS-480A", "MCC-1A"),
    ("MCC-1A", "PUMP-CCW-103A"),
    ("BUS-480A", "MCC-1C"),
    ("MCC-1C", "FAN-CRHV-104A"),
    ("BUS-480E1A", "MCC-ESS-A"),
    ("MCC-ESS-A", "PUMP-SI-101A"),
    ("MCC-ESS-A", "PUMP-RHR-102A"),
    ("MCC-ESS-A", "MOV-1201A"),
    ("BUS-480B", "MCC-1B"),
    ("MCC-1B", "PUMP-CCW-103B"),
    ("BUS-480B", "MCC-1D"),
    ("MCC-1D", "FAN-CRHV-104B"),
    ("BUS-480E1B", "MCC-ESS-B"),
    ("MCC-ESS-B", "PUMP-SI-101B"),
    ("MCC-ESS-B", "PUMP-RHR-102B"),
    ("MCC-ESS-B", "MOV-1201B"),
    ("BUS-480A", "CHGR-125A"),
    ("CHGR-125A", "DC-BUS-125A"),
    ("BAT-125A", "DC-BUS-125A"),
    ("DC-BUS-125A", "INV-120A"),
    ("INV-120A", "UPS-BUS-A"),
    ("UPS-BUS-A", "PANEL-RPS-A"),
    ("UPS-BUS-A", "INST-RACK-1"),
    ("BUS-480E1B", "CHGR-125B"),
    ("CHGR-125B", "DC-BUS-125B"),
    ("BAT-125B", "DC-BUS-125B"),
    ("DC-BUS-125B", "INV-120B"),
    ("INV-120B", "UPS-BUS-B"),
    ("UPS-BUS-B", "PANEL-RPS-B"),
    ("CB-105", "CTRL-86A"),
    ("CTRL-86A", "RELAY-K86A"),
    ("RELAY-K86A", "PANEL-RPS-A"),
    ("PANEL-RPS-A", "JB-ESF-01-TB1"),
    ("JB-ESF-01-TB1", "PANEL-RPS-B"),
    ("PANEL-RPS-B", "RELAY-K86B"),
    ("RELAY-K86B", "CTRL-86B"),
    ("CTRL-86B", "CB-106"),
]


HIGH_RECALL_REVIEW_EXTRAS = [
    ("BUS-1A-4.16KV", "BUS-1B-4.16KV"),
    ("CHGR-125B", "CB-204"),
    ("PUMP-RHR-102A", "CTRL-86A"),
    ("FAN-CRHV-104B", "CTRL-86B"),
    ("UPS-BUS-A", "UPS-BUS-B"),
    ("UPS-BUS-B", "INST-RACK-1"),
]


FINAL_EDGES = [
    ("OFFSITE-A-161KV", "TR-1A"),
    ("TR-1A", "CB-101"),
    ("CB-101", "BUS-1A-4.16KV"),
    ("TR-1A", "GND-1E"),
    ("EDG-1A", "CB-105"),
    ("CB-105", "BUS-1A-4.16KV"),
    ("BUS-1A-4.16KV", "CB-TIE-1AB"),
    ("CB-TIE-1AB", "BUS-1B-4.16KV"),
    ("BUS-1B-4.16KV", "CB-102"),
    ("CB-102", "TR-1B"),
    ("TR-1B", "OFFSITE-B-161KV"),
    ("EDG-1B", "CB-106"),
    ("CB-106", "BUS-1B-4.16KV"),
    ("BUS-1A-4.16KV", "TR-LC-1A"),
    ("TR-LC-1A", "CB-201"),
    ("CB-201", "BUS-480A"),
    ("BUS-1A-4.16KV", "TR-SAF-1A"),
    ("TR-SAF-1A", "CB-203"),
    ("CB-203", "BUS-480E1A"),
    ("BUS-1B-4.16KV", "TR-LC-1B"),
    ("TR-LC-1B", "CB-202"),
    ("CB-202", "BUS-480B"),
    ("BUS-1B-4.16KV", "TR-SAF-1B"),
    ("TR-SAF-1B", "CB-204"),
    ("CB-204", "BUS-480E1B"),
    ("BUS-480A", "MCC-1A"),
    ("MCC-1A", "PUMP-CCW-103A"),
    ("BUS-480A", "MCC-1C"),
    ("MCC-1C", "FAN-CRHV-104A"),
    ("BUS-480E1A", "MCC-ESS-A"),
    ("MCC-ESS-A", "PUMP-SI-101A"),
    ("MCC-ESS-A", "PUMP-RHR-102A"),
    ("MCC-ESS-A", "MOV-1201A"),
    ("BUS-480B", "MCC-1B"),
    ("MCC-1B", "PUMP-CCW-103B"),
    ("BUS-480B", "MCC-1D"),
    ("MCC-1D", "FAN-CRHV-104B"),
    ("BUS-480E1B", "MCC-ESS-B"),
    ("MCC-ESS-B", "PUMP-SI-101B"),
    ("MCC-ESS-B", "PUMP-RHR-102B"),
    ("MCC-ESS-B", "MOV-1201B"),
    ("BUS-480A", "CHGR-125A"),
    ("CHGR-125A", "DC-BUS-125A"),
    ("BAT-125A", "DC-BUS-125A"),
    ("DC-BUS-125A", "INV-120A"),
    ("INV-120A", "UPS-BUS-A"),
    ("UPS-BUS-A", "PANEL-RPS-A"),
    ("UPS-BUS-A", "INST-RACK-1"),
    ("CB-204", "CHGR-125B"),
    ("CHGR-125B", "DC-BUS-125B"),
    ("BAT-125B", "DC-BUS-125B"),
    ("DC-BUS-125B", "INV-120B"),
    ("INV-120B", "UPS-BUS-B"),
    ("UPS-BUS-B", "PANEL-RPS-B"),
    ("CB-105", "RELAY-K86A"),
    ("RELAY-K86A", "PANEL-RPS-A"),
    ("PANEL-RPS-A", "JB-ESF-01-TB1"),
    ("JB-ESF-01-TB1", "PANEL-RPS-B"),
    ("PANEL-RPS-B", "RELAY-K86B"),
    ("RELAY-K86B", "CB-106"),
]


ROUNDS = [
    {
        "round": "01",
        "agent": "Diego",
        "stage": "high_recall",
        "nodes": DIEGO_NODES,
        "edges": DIEGO_CONFIRMED_EDGES + HIGH_RECALL_REVIEW_EXTRAS,
        "notes": "High-recall graph included CTRL-86 callout nodes and six review-only candidate extras.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "stage": "precision_review",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Precision review removed CTRL-86 callout nodes and unsupported crossings; selected CB-204 as charger-B feed anchor.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "stage": "saturation",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Diego accepted Jennifer's refined graph without corrections.",
    },
    {
        "round": "04",
        "agent": "Jennifer",
        "stage": "final",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": "Jennifer confirmed final graph as 58 nodes and 60 edges.",
    },
]


TOKEN_CALLS = [
    {
        "call_id": "main-setup-crops-and-local-inspection",
        "agent": "Main",
        "purpose": "Read task, verify raw-only scope, create and inspect raw-derived crops.",
        "model_call_count": 3,
        "input_tokens_expected": 18500,
        "input_tokens_low": 13000,
        "input_tokens_high": 26500,
        "cached_input_tokens_expected": 4500,
        "output_tokens_expected": 2600,
        "output_tokens_low": 1600,
        "output_tokens_high": 4300,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 12500,
        "usage_source": "Estimated from visible task context, crop count, and local image-inspection payloads.",
    },
    {
        "call_id": "diego-round-01-high-recall",
        "agent": "Diego",
        "purpose": "High-recall extraction from the raw sheet and raw-derived crops.",
        "model_call_count": 1,
        "input_tokens_expected": 27500,
        "input_tokens_low": 19500,
        "input_tokens_high": 39500,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 5600,
        "output_tokens_low": 3600,
        "output_tokens_high": 9000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 20000,
        "usage_source": "Estimated from Diego prompt, 10 local-image inputs, and response length.",
    },
    {
        "call_id": "jennifer-round-02-precision",
        "agent": "Jennifer",
        "purpose": "Precision review of Diego graph and pruning of unsupported/control-callout nodes.",
        "model_call_count": 1,
        "input_tokens_expected": 32000,
        "input_tokens_low": 22500,
        "input_tokens_high": 46000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 5000,
        "output_tokens_low": 3200,
        "output_tokens_high": 8000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 22000,
        "usage_source": "Estimated from Diego proposal, local-image payloads, and reviewer response length.",
    },
    {
        "call_id": "diego-round-03-saturation",
        "agent": "Diego",
        "purpose": "Saturation check of Jennifer's refined graph.",
        "model_call_count": 1,
        "input_tokens_expected": 16500,
        "input_tokens_low": 11500,
        "input_tokens_high": 24000,
        "cached_input_tokens_expected": 4000,
        "output_tokens_expected": 350,
        "output_tokens_low": 150,
        "output_tokens_high": 800,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "usage_source": "Estimated from compact refined-graph payload and short response.",
    },
    {
        "call_id": "jennifer-round-04-final",
        "agent": "Jennifer",
        "purpose": "Final confirmation of labels, edge list, and counts.",
        "model_call_count": 1,
        "input_tokens_expected": 16500,
        "input_tokens_low": 11500,
        "input_tokens_high": 24000,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 250,
        "output_tokens_low": 100,
        "output_tokens_high": 600,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "usage_source": "Estimated from final confirmation payload and short acknowledgement.",
    },
    {
        "call_id": "main-output-generation-and-finalization",
        "agent": "Main",
        "purpose": "Write matrices, edge lists, validation JSON, notes, token tracking, and final response.",
        "model_call_count": 2,
        "input_tokens_expected": 20500,
        "input_tokens_low": 14500,
        "input_tokens_high": 30000,
        "cached_input_tokens_expected": 6500,
        "output_tokens_expected": 7000,
        "output_tokens_low": 4500,
        "output_tokens_high": 11200,
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
    for a, b in edges:
        if a not in node_set or b not in node_set:
            errors.append(f"Edge endpoint outside node list: {a} -- {b}")
        if a == b:
            errors.append(f"Self-loop present without justification: {a}")
        ce = canonical_edge((a, b))
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
    reasoning = row.get("reasoning_tokens_expected") or 0
    return (
        int(row[f"input_tokens_{band}"])
        + int(row[f"output_tokens_{band}"])
        + int(row["image_file_input_tokens_expected"])
        + int(reasoning)
    )


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
    with (RESULTS_DIR / "token_usage_summary_by_document.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
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
    final_edges = "\n".join(f"- `{a} -- {b}`" for a, b in FINAL_EDGES)
    pruned = "\n".join(
        [
            "- `CTRL-86A`, `CTRL-86B` removed as callout/conductor labels, not device nodes.",
            "- `BUS-1A-4.16KV -- BUS-1B-4.16KV` direct bus collapse removed; `CB-TIE-1AB` remains between buses.",
            "- `BUS-480E1B -- CHGR-125B` changed to `CB-204 -- CHGR-125B` based on visible load-side branch.",
            "- `PUMP-RHR-102A -- CTRL-86A` and `FAN-CRHV-104B -- CTRL-86B` removed as unsupported crossings/nearby dashed runs.",
            "- `UPS-BUS-A -- UPS-BUS-B` and `UPS-BUS-B -- INST-RACK-1` removed because no terminal dot/device port supports those joins.",
        ]
    )
    round_lines = "\n".join(
        f"- Round {row['round']} {row['agent']} `{row['stage']}`: {row['node_count']} nodes, {row['edge_count']} edges, valid={row['valid']}"
        for row in round_summary
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

## Final Result

- Final node count: {validation['node_count']}
- Final edge count: {validation['edge_count']}
- Matrix: {validation['matrix_size'][0]} x {validation['matrix_size'][1]}
- Symmetric: {validation['symmetric']}
- Diagonal zero: {validation['diagonal_zero']}
- Validation errors: {len(validation['errors'])}

## Final Edges

{final_edges}

## Precision Changes

{pruned}

## Label Notes

- Cable labels such as `CABLE 1A-480-7`, `CABLE 1B-480-9`, `4160V FEED A`, `FDR A-DC`, and `FDR B-DC` were treated as annotations, not component nodes.
- `JB-ESF-01-TB1` was aggregated as one junction/terminal-block node.
- Internal labels inside `INST-RACK-1` (`PT`, `UV`, `SEQ`) were treated as internal subdevices without separate external edges.

## Token Tracking

- Expected total tokens: {token_summary['total_tokens_expected']} (low {token_summary['total_tokens_low']}, high {token_summary['total_tokens_high']}).
- Model calls counted: {token_summary['model_call_count']}.
- Actual usage objects unavailable: yes.

Actual per-response usage objects were not exposed by the available Codex subagent tools. The Responses input-token counting endpoint was not called because `OPENAI_API_KEY` was unavailable in this execution environment. The CSV files therefore contain low/expected/high estimates and explicit `actual_usage_available=no` markers.
"""
    (RESULTS_DIR / "extraction_note.md").write_text(content, encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    final_validation = validate_graph(FINAL_NODES, FINAL_EDGES)
    if not final_validation["valid"]:
        raise SystemExit(f"Final graph failed validation: {final_validation['errors']}")
    if final_validation["node_count"] != 58 or final_validation["edge_count"] != 60:
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
        "round_01_high_recall_review_extras": [{"source": a, "target": b} for a, b in HIGH_RECALL_REVIEW_EXTRAS],
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
