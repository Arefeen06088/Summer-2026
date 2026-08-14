import csv
import json
import math
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\10")
RESULTS = DOC_ROOT / "Results" / "Iteration_1"
ARTIFACTS = DOC_ROOT / "Codes and artifacts"
TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"
MAIN_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\06\23"
    r"\rollout-2026-06-23T09-16-37-019ef50d-f35f-7dc2-a1f6-b49c274038fe.jsonl"
)
SUBAGENT_LOGS = {
    "diego_r01": Path(
        r"C:\Users\AREFA\.codex\sessions\2026\07\27"
        r"\rollout-2026-07-27T12-41-57-019fa4e2-34e4-79e1-b5ef-33b4ab804dc3.jsonl"
    ),
    "jennifer_r01": Path(
        r"C:\Users\AREFA\.codex\sessions\2026\07\27"
        r"\rollout-2026-07-27T12-54-20-019fa4ed-8f0a-7670-9157-1c64b1e1a5f6.jsonl"
    ),
    "diego_r02": Path(
        r"C:\Users\AREFA\.codex\sessions\2026\07\27"
        r"\rollout-2026-07-27T13-00-02-019fa4f2-c5ce-7430-bcd6-3cbb4f6a1837.jsonl"
    ),
    "jennifer_r02": Path(
        r"C:\Users\AREFA\.codex\sessions\2026\07\27"
        r"\rollout-2026-07-27T13-07-33-019fa4f9-aa02-7742-ae6b-02122b9f48b1.jsonl"
    ),
}
MAIN_BOUNDARY_TS = "2026-07-27T18:39:29.751Z"
FINAL_PREFIX = "current_round_02_jennifer"


def parse_ts(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_jsonl(path):
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError:
                continue


def token_rows(path, after_ts=None, agent="main"):
    rows = []
    for line_no, obj in read_jsonl(path):
        ts = parse_ts(obj.get("timestamp"))
        if after_ts and (ts is None or ts < after_ts):
            continue
        payload = obj.get("payload", {})
        if obj.get("type") != "event_msg" or payload.get("type") != "token_count":
            continue
        usage = payload.get("info", {}).get("last_token_usage", {}) or {}
        total_usage = payload.get("info", {}).get("total_token_usage", {}) or {}
        rows.append(
            {
                "agent": agent,
                "log_path": str(path),
                "line_no": line_no,
                "timestamp": obj.get("timestamp", ""),
                "input_tokens": int(usage.get("input_tokens") or 0),
                "cached_input_tokens": int(usage.get("cached_input_tokens") or 0),
                "cache_write_input_tokens": int(usage.get("cache_write_input_tokens") or 0),
                "output_tokens": int(usage.get("output_tokens") or 0),
                "reasoning_output_tokens": int(usage.get("reasoning_output_tokens") or 0),
                "total_tokens": int(usage.get("total_tokens") or 0),
                "cumulative_total_tokens_reported": int(total_usage.get("total_tokens") or 0),
                "image_file_input_tokens": "",
                "image_file_input_note": "not separately exposed; included in input_tokens",
            }
        )
    return rows


def sum_usage(rows):
    fields = [
        "input_tokens",
        "cached_input_tokens",
        "cache_write_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
        "total_tokens",
    ]
    out = {field: sum(int(row.get(field) or 0) for row in rows) for field in fields}
    out["model_calls"] = len(rows)
    return out


def read_csv_dicts(path):
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv_dicts(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def edge_key(a, b):
    return tuple(sorted((a, b)))


def validate_final(nodes_path, edges_path, matrix_path):
    nodes = read_csv_dicts(nodes_path)
    edges = read_csv_dicts(edges_path)
    def get_node_name(row):
        for key in ("node_name", "name", "node"):
            if row.get(key):
                return row[key]
        return ""

    node_names = [get_node_name(row) for row in nodes]
    node_set = set(node_names)
    duplicate_nodes = [name for name, count in Counter(node_names).items() if count > 1]
    edge_status_counts = Counter(row.get("status", "") for row in edges)
    keep_edges = [row for row in edges if row.get("status") == "keep"]
    keep_set = {edge_key(row["source"], row["target"]) for row in keep_edges}
    duplicate_keep_edges = [
        "::".join(key)
        for key, count in Counter(edge_key(row["source"], row["target"]) for row in keep_edges).items()
        if count > 1
    ]
    missing_edge_refs = sorted(
        {
            ref
            for row in edges
            for ref in (row.get("source", ""), row.get("target", ""))
            if ref not in node_set
        }
    )

    with matrix_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    header = rows[0][1:]
    matrix_rows = rows[1:]
    matrix_names = [row[0] for row in matrix_rows]
    matrix_edge_set = set()
    binary_entries = True
    zero_diagonal = True
    symmetric = True
    values = {}
    for i, row in enumerate(matrix_rows):
        for j, value in enumerate(row[1:]):
            if value not in {"0", "1", 0, 1}:
                binary_entries = False
            v = int(value)
            values[(i, j)] = v
            if i == j and v != 0:
                zero_diagonal = False
            if j > i and v == 1:
                matrix_edge_set.add(edge_key(matrix_names[i], header[j]))
    for i in range(len(matrix_rows)):
        for j in range(len(header)):
            if values.get((i, j)) != values.get((j, i)):
                symmetric = False
                break
        if not symmetric:
            break

    isolated = []
    for name in node_names:
        if all(name not in key for key in matrix_edge_set):
            isolated.append(name)

    return {
        "family": "Improved",
        "document": 10,
        "iteration": 1,
        "final_source": FINAL_PREFIX,
        "node_count": len(node_names),
        "unique_node_count": len(node_set),
        "edge_candidate_count": len(edges),
        "status_counts": dict(edge_status_counts),
        "keep_edge_count": len(keep_edges),
        "matrix_node_count": len(header),
        "matrix_edge_count": len(matrix_edge_set),
        "isolated_nodes_after_keep_matrix": isolated,
        "checks": {
            "node_names_unique": not duplicate_nodes,
            "no_WN_final_nodes": not any(name.startswith("WN-") for name in node_names),
            "edges_reference_only_final_nodes": not missing_edge_refs,
            "no_duplicate_keep_edges": not duplicate_keep_edges,
            "matrix_node_order_matches_nodes_csv": header == node_names and matrix_names == node_names,
            "matrix_binary_entries_only": binary_entries,
            "matrix_zero_diagonal": zero_diagonal,
            "matrix_symmetric": symmetric,
            "matrix_edge_set_equals_keep_edge_set": matrix_edge_set == keep_set,
        },
        "duplicate_nodes": duplicate_nodes,
        "missing_edge_references": missing_edge_refs,
        "duplicate_keep_edges": duplicate_keep_edges,
        "scope": {
            "ground_truth_or_eval_outputs_used": False,
            "gt_derived_feedback_used": False,
            "tracker_performance_metrics_used_for_extraction": False,
            "prior_or_archived_result_folders_used_for_extraction": False,
        },
    }


def update_tracker(tracker_summary, validation):
    rows = read_csv_dicts(TRACKER_CSV)
    fieldnames = list(rows[0].keys()) if rows else []
    timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
    workflow_label = "Improved doc 10 / Iteration 1"
    target = None
    for row in rows:
        if (
            row.get("family") == "Improved"
            and row.get("document") == "10"
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        ):
            target = row
            break
    if target is None:
        target = {name: "" for name in fieldnames}
        rows.append(target)

    def set_value(key, value):
        if key in target:
            target[key] = str(value)

    total = tracker_summary["total"]
    main = tracker_summary["main"]
    diego = tracker_summary["diego"]
    jennifer = tracker_summary["jennifer"]
    subagents = tracker_summary["subagents"]
    single = tracker_summary["single_agent_proxy"]

    values = {
        "family": "Improved",
        "document": 10,
        "iteration": 1,
        "workflow_label": workflow_label,
        "record_type": "multi_agent_token_usage_unvalidated_final",
        "metric_source_path": str(RESULTS / "final_connectivity_validation.json"),
        "metric_label": "Final connectivity -- unvalidated",
        "metric_agent": "Jennifer",
        "metric_round": 2,
        "is_selected_final_metric": 1,
        "final_metric_selection_basis": "round_02_jennifer accepted Diego round 2 unchanged; saturation reached",
        "validation_note": "Extraction completed blind; final matrix is unvalidated against GT pending after-the-fact metrics.",
        "actual_multi_agent_model_calls": total["model_calls"],
        "actual_multi_agent_input_tokens": total["input_tokens"],
        "actual_multi_agent_cached_input_tokens": total["cached_input_tokens"],
        "actual_multi_agent_output_tokens": total["output_tokens"],
        "actual_multi_agent_reasoning_output_tokens": total["reasoning_output_tokens"],
        "actual_multi_agent_total_tokens": total["total_tokens"],
        "image_file_input_tokens": "",
        "image_file_input_note": "not separately exposed; included in input_tokens",
        "token_usage_basis": "actual completed-call Codex token_count logs after latest doc10 user boundary; final response not included",
        "main_model_calls": main["model_calls"],
        "main_input_tokens": main["input_tokens"],
        "main_cached_input_tokens": main["cached_input_tokens"],
        "main_output_tokens": main["output_tokens"],
        "main_reasoning_output_tokens": main["reasoning_output_tokens"],
        "main_total_tokens": main["total_tokens"],
        "diego_model_calls": diego["model_calls"],
        "diego_input_tokens": diego["input_tokens"],
        "diego_cached_input_tokens": diego["cached_input_tokens"],
        "diego_output_tokens": diego["output_tokens"],
        "diego_reasoning_output_tokens": diego["reasoning_output_tokens"],
        "diego_total_tokens": diego["total_tokens"],
        "jennifer_model_calls": jennifer["model_calls"],
        "jennifer_input_tokens": jennifer["input_tokens"],
        "jennifer_cached_input_tokens": jennifer["cached_input_tokens"],
        "jennifer_output_tokens": jennifer["output_tokens"],
        "jennifer_reasoning_output_tokens": jennifer["reasoning_output_tokens"],
        "jennifer_total_tokens": jennifer["total_tokens"],
        "single_agent_proxy_basis": "Diego round 1 actual usage plus low/expected/high 25/50/100 percent of observed main orchestration tokens",
        "single_agent_round1_proxy_metric_label": "Diego round 1 proxy -- unvalidated",
        "single_agent_low_total_tokens": single["low"],
        "single_agent_expected_total_tokens": single["expected"],
        "single_agent_high_total_tokens": single["high"],
        "single_agent_estimate_basis": "actual Diego R01 subagent total plus assumed main orchestration fraction; no output forecast needed for completed Diego R01",
        "single_agent_expected_token_savings_vs_multi_agent": single["expected"] - total["total_tokens"],
        "single_agent_expected_token_savings_pct_vs_multi_agent": (
            (single["expected"] - total["total_tokens"]) / total["total_tokens"] if total["total_tokens"] else ""
        ),
        "multi_agent_vs_single_agent_expected_token_ratio": (
            total["total_tokens"] / single["expected"] if single["expected"] else ""
        ),
        "extra_multi_agent_tokens_vs_single_agent_expected": total["total_tokens"] - single["expected"],
        "data_limitations": (
            "FP/FN/precision/recall/F1 blank until after-the-fact validation metrics are available; "
            "image/file tokens are included in input_tokens but not separately exposed; final assistant response not included."
        ),
        "performance_status": "unvalidated_pending_after_the_fact_metrics",
        "completed_subagent_model_calls": subagents["model_calls"],
        "completed_subagent_input_tokens": subagents["input_tokens"],
        "completed_subagent_cached_input_tokens": subagents["cached_input_tokens"],
        "completed_subagent_output_tokens": subagents["output_tokens"],
        "completed_subagent_reasoning_output_tokens": subagents["reasoning_output_tokens"],
        "completed_subagent_total_tokens": subagents["total_tokens"],
        "main_low_estimate_tokens": main["total_tokens"],
        "main_expected_estimate_tokens": main["total_tokens"] + 50000,
        "main_high_estimate_tokens": main["total_tokens"] + 150000,
        "workflow_low_estimate_total_tokens": total["total_tokens"],
        "workflow_expected_estimate_total_tokens": total["total_tokens"] + 50000,
        "workflow_high_estimate_total_tokens": total["total_tokens"] + 150000,
        "token_update_timestamp": timestamp,
        "f1": "",
    }
    for key, value in values.items():
        set_value(key, value)

    for key in ["tp", "fp", "fn", "precision", "recall", "f1_score", "total_errors"]:
        set_value(key, "")

    write_csv_dicts(TRACKER_CSV, rows, fieldnames)
    return timestamp


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    mappings = {
        f"{FINAL_PREFIX}_nodes.csv": ["final_connectivity_nodes.csv", "final_nodes.csv"],
        f"{FINAL_PREFIX}_matrix.csv": ["final_connectivity_matrix.csv", "connectivity_matrix.csv"],
        f"{FINAL_PREFIX}_notes.md": ["final_connectivity_notes.md"],
    }
    for source_name, destinations in mappings.items():
        source = RESULTS / source_name
        for destination_name in destinations:
            shutil.copyfile(source, RESULTS / destination_name)

    review_edges = read_csv_dicts(RESULTS / f"{FINAL_PREFIX}_edges.csv")
    edge_fieldnames = list(review_edges[0].keys()) if review_edges else []
    write_csv_dicts(RESULTS / "final_edge_review.csv", review_edges, edge_fieldnames)
    keep_edges = [row for row in review_edges if row.get("status") == "keep"]
    write_csv_dicts(RESULTS / "final_connectivity_edges.csv", keep_edges, edge_fieldnames)
    write_csv_dicts(RESULTS / "final_edges.csv", keep_edges, edge_fieldnames)

    validation = validate_final(
        RESULTS / "final_connectivity_nodes.csv",
        RESULTS / "final_edge_review.csv",
        RESULTS / "final_connectivity_matrix.csv",
    )
    (RESULTS / "final_connectivity_validation.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )

    boundary = parse_ts(MAIN_BOUNDARY_TS)
    main_rows = token_rows(MAIN_LOG, after_ts=boundary, agent="main")
    sub_rows = []
    for agent, path in SUBAGENT_LOGS.items():
        sub_rows.extend(token_rows(path, agent=agent))
    all_rows = main_rows + sub_rows
    write_csv_dicts(
        RESULTS / "token_usage_model_calls.csv",
        all_rows,
        [
            "agent",
            "log_path",
            "line_no",
            "timestamp",
            "input_tokens",
            "cached_input_tokens",
            "cache_write_input_tokens",
            "output_tokens",
            "reasoning_output_tokens",
            "total_tokens",
            "cumulative_total_tokens_reported",
            "image_file_input_tokens",
            "image_file_input_note",
        ],
    )

    by_agent = {agent: sum_usage([row for row in all_rows if row["agent"] == agent]) for agent in sorted({row["agent"] for row in all_rows})}
    main_usage = sum_usage(main_rows)
    diego_rows = [row for row in sub_rows if row["agent"].startswith("diego")]
    jennifer_rows = [row for row in sub_rows if row["agent"].startswith("jennifer")]
    diego_usage = sum_usage(diego_rows)
    jennifer_usage = sum_usage(jennifer_rows)
    subagent_usage = sum_usage(sub_rows)
    total_usage = sum_usage(all_rows)
    diego_r01_usage = sum_usage([row for row in all_rows if row["agent"] == "diego_r01"])
    single_agent_proxy = {
        "low": int(round(diego_r01_usage["total_tokens"] + 0.25 * main_usage["total_tokens"])),
        "expected": int(round(diego_r01_usage["total_tokens"] + 0.50 * main_usage["total_tokens"])),
        "high": int(round(diego_r01_usage["total_tokens"] + 1.00 * main_usage["total_tokens"])),
    }
    token_summary = {
        "family": "Improved",
        "document": 10,
        "iteration": 1,
        "main_boundary_timestamp": MAIN_BOUNDARY_TS,
        "usage_by_agent": by_agent,
        "main": main_usage,
        "diego": diego_usage,
        "jennifer": jennifer_usage,
        "subagents": subagent_usage,
        "total": total_usage,
        "single_agent_proxy": single_agent_proxy,
        "image_file_input_note": "not separately exposed; included in input_tokens",
        "planned_payload_counting_endpoint_note": (
            "Not separately called for this completed run; actual Codex token_count usage objects "
            "were available for all completed calls."
        ),
    }
    (RESULTS / "token_usage_actual_estimate.json").write_text(
        json.dumps(token_summary, indent=2), encoding="utf-8"
    )

    timestamp = update_tracker(token_summary, validation)

    summary_md = f"""# Final Connectivity Summary

Document: Improved doc 10
Iteration: 1
Final source: `current_round_02_jennifer`

## Extraction Outcome

- Saturation reached: Jennifer R02 accepted Diego R02 unchanged.
- Final nodes: {validation['node_count']}
- Final kept edges: {validation['keep_edge_count']}
- Removed review edges: {validation['status_counts'].get('remove', 0)}
- Uncertain review edges: {validation['status_counts'].get('uncertain', 0)}
- Isolated final nodes: {', '.join(validation['isolated_nodes_after_keep_matrix']) if validation['isolated_nodes_after_keep_matrix'] else 'none'}

## Key Final Decisions

- Kept `CT-4160-A -- BUS-4160-A` and `CT-4160-B -- BUS-4160-B`.
- Removed all eight previously uncertain candidates from the final matrix.
- Kept `SER-01` as an isolated named component because no raw-supported terminal edge enters it.
- No `WN-*` wire nodes or annotation-only labels are final matrix nodes.

## Validation

- Matrix node order matches final nodes CSV: {validation['checks']['matrix_node_order_matches_nodes_csv']}
- Matrix edge set equals keep-edge set: {validation['checks']['matrix_edge_set_equals_keep_edge_set']}
- Symmetric: {validation['checks']['matrix_symmetric']}
- Zero diagonal: {validation['checks']['matrix_zero_diagonal']}
- Binary entries only: {validation['checks']['matrix_binary_entries_only']}

## Token Tracking Snapshot

- Main calls: {main_usage['model_calls']}, total tokens: {main_usage['total_tokens']}
- Diego calls: {diego_usage['model_calls']}, total tokens: {diego_usage['total_tokens']}
- Jennifer calls: {jennifer_usage['model_calls']}, total tokens: {jennifer_usage['total_tokens']}
- Observed multi-agent total: {total_usage['model_calls']} calls, {total_usage['total_tokens']} tokens
- Single-agent one-round proxy low/expected/high: {single_agent_proxy['low']} / {single_agent_proxy['expected']} / {single_agent_proxy['high']} tokens
- Tracker updated: {timestamp}

No Ground Truth, evaluator/scoring output, GT-derived feedback, prior/archived result folders, or tracker performance metrics were used for extraction.
"""
    (RESULTS / "final_connectivity_summary.md").write_text(summary_md, encoding="utf-8")

    notes_append = f"""

## Doc 10 Iteration 1 Current Update - {timestamp}

Updated/replaced `Improved doc 10 / Iteration 1` after the current one-iteration Diego/Jennifer workflow.

Extraction:
- Final source: `current_round_02_jennifer`, accepting Diego round 2 unchanged after focused saturation review.
- Final matrix: {validation['node_count']} nodes and {validation['keep_edge_count']} kept edges.
- Excluded review edges: {validation['status_counts'].get('uncertain', 0)} uncertain, {validation['status_counts'].get('remove', 0)} removed.
- Key refinement: the mirrored CT-to-4160-bus pair was retained, all eight previously uncertain edges were removed, and `SER-01` was left isolated.
- No GT, GT-derived feedback, scoring output, evaluator file, archived prior result, or tracker performance metric was used during extraction.

Token snapshot:
- Main agent observed: {main_usage['model_calls']} calls, {main_usage['total_tokens']} total tokens from the latest doc10 user boundary.
- Diego aggregate: {diego_usage['model_calls']} calls, {diego_usage['total_tokens']} total tokens.
- Jennifer aggregate: {jennifer_usage['model_calls']} calls, {jennifer_usage['total_tokens']} total tokens.
- Completed subagents: {subagent_usage['model_calls']} calls, {subagent_usage['total_tokens']} total tokens.
- Observed multi-agent workflow: {total_usage['model_calls']} calls, {total_usage['total_tokens']} total tokens.
- Single-agent one-round proxy: low/expected/high = {single_agent_proxy['low']} / {single_agent_proxy['expected']} / {single_agent_proxy['high']} tokens.

Limitations:
- Image/file input tokens are not separately exposed in the local Codex `token_count` records; they are included inside `input_tokens`.
- This is an observed pre-final-response snapshot. The final assistant response and any later bookkeeping calls are not included.
- FP/FN/precision/recall/F1 remain blank until after-the-fact validation metrics are available.
"""
    existing_notes = TRACKER_NOTES.read_text(encoding="utf-8") if TRACKER_NOTES.exists() else ""
    existing_notes = re.sub(
        r"\n## Doc 10 Iteration 1 Current Update - .*?(?=\n## |\Z)",
        "",
        existing_notes,
        flags=re.S,
    )
    TRACKER_NOTES.write_text(existing_notes.rstrip() + notes_append, encoding="utf-8")

    print(json.dumps({"validation": validation, "token_summary": token_summary, "tracker_timestamp": timestamp}, indent=2))


if __name__ == "__main__":
    main()
