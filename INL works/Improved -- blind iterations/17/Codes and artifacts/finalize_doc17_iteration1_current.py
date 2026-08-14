import csv
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


DOC = 17
FAMILY = "Improved"
ITERATION = 1

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\17")
RESULTS = BASE / "Results" / "Iteration_1"
ARTIFACTS = BASE / "Codes and artifacts"
INVENTORY = ARTIFACTS / "component_inventory_doc17_current.csv"

TRACKER = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06\token_performance_tracking.csv"
)
TRACKER_NOTES = TRACKER.with_name("token_performance_tracking_notes.md")

LOG_ROOT = Path(r"C:\Users\AREFA\.codex\sessions")
MAIN_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\06\23"
    r"\rollout-2026-06-23T09-16-37-019ef50d-f35f-7dc2-a1f6-b49c274038fe.jsonl"
)
DIEGO_ID = "019fa469-3bb8-7393-b0de-90d5c0e1a9d3"
JENNIFER_ID = "019fa473-4b07-7b21-8bea-eb05d2db499f"
TASK_START_UTC = "2026-07-27T16:25:00Z"


def parse_ts(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def token_zero():
    return {
        "model_calls": 0,
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }


def usage_from_obj(obj):
    return {
        "input_tokens": int(obj.get("input_tokens", 0) or 0),
        "cached_input_tokens": int(obj.get("cached_input_tokens", 0) or 0),
        "output_tokens": int(obj.get("output_tokens", 0) or 0),
        "reasoning_output_tokens": int(obj.get("reasoning_output_tokens", 0) or 0),
        "total_tokens": int(obj.get("total_tokens", 0) or 0),
    }


def add_usage(a, b):
    out = dict(a)
    for key in [
        "model_calls",
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
        "total_tokens",
    ]:
        out[key] = int(out.get(key, 0) or 0) + int(b.get(key, 0) or 0)
    return out


def find_agent_log(agent_id):
    dated = LOG_ROOT / "2026" / "07" / "27"
    candidates = list(dated.glob(f"*{agent_id}.jsonl"))
    if candidates:
        return candidates[0]
    for path in LOG_ROOT.rglob("*.jsonl"):
        if agent_id in path.name:
            return path
    return None


def read_token_events(path, start_ts=None, end_ts=None):
    events = []
    if not path or not path.exists():
        return events
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = parse_ts(rec.get("timestamp"))
            if start_ts and ts and ts < start_ts:
                continue
            if end_ts and ts and ts > end_ts:
                continue
            payload = rec.get("payload", {})
            if rec.get("type") == "event_msg" and payload.get("type") == "token_count":
                info = payload.get("info", {})
                events.append(
                    {
                        "timestamp": ts.isoformat() if ts else "",
                        "last": usage_from_obj(info.get("last_token_usage", {})),
                        "total": usage_from_obj(info.get("total_token_usage", {})),
                    }
                )
    return events


def cumulative_usage(path):
    events = read_token_events(path)
    usage = token_zero()
    if events:
        usage.update(events[-1]["total"])
        usage["model_calls"] = len(events)
    return usage


def summed_last_usage(path, start_ts=None, end_ts=None):
    usage = token_zero()
    for event in read_token_events(path, start_ts=start_ts, end_ts=end_ts):
        one = token_zero()
        one.update(event["last"])
        one["model_calls"] = 1
        usage = add_usage(usage, one)
    return usage


def cumulative_usage_before(path, end_ts):
    events = read_token_events(path, end_ts=end_ts)
    usage = token_zero()
    if events:
        usage.update(events[-1]["total"])
        usage["model_calls"] = len(events)
    return usage


def load_matrix(path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError(f"empty matrix: {path}")
    header = rows[0]
    nodes = header[1:]
    body = []
    for row in rows[1:]:
        if len(row) != len(nodes) + 1:
            raise ValueError(f"bad row width in {path}: {row[:3]}")
        body.append((row[0], [int(v) for v in row[1:]]))
    return nodes, body


def matrix_edges(nodes, body):
    edges = set()
    for i, (row_name, values) in enumerate(body):
        if row_name != nodes[i]:
            raise ValueError(f"row/column order mismatch at {i}: {row_name} != {nodes[i]}")
        if values[i] != 0:
            raise ValueError(f"nonzero diagonal at {row_name}")
        for j in range(i + 1, len(nodes)):
            if values[j]:
                edges.add(tuple(sorted((nodes[i], nodes[j]))))
            if values[j] != body[j][1][i]:
                raise ValueError(f"asymmetric matrix at {nodes[i]}, {nodes[j]}")
    return edges


def load_edges(path):
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def validate(edges_path, matrix_path):
    nodes, body = load_matrix(matrix_path)
    edge_rows = load_edges(edges_path)
    node_set = set(nodes)
    seen = set()
    duplicate_edges = []
    missing = []
    self_edges = []
    for row in edge_rows:
        a = row["source"]
        b = row["target"]
        if a == b:
            self_edges.append(a)
        if a not in node_set or b not in node_set:
            missing.append((a, b))
        key = tuple(sorted((a, b)))
        if key in seen:
            duplicate_edges.append(key)
        seen.add(key)
    from_matrix = matrix_edges(nodes, body)
    if missing or self_edges or duplicate_edges or seen != from_matrix:
        raise ValueError(
            json.dumps(
                {
                    "missing": missing,
                    "self_edges": self_edges,
                    "duplicate_edges": duplicate_edges,
                    "edge_csv_minus_matrix": sorted(seen - from_matrix),
                    "matrix_minus_edge_csv": sorted(from_matrix - seen),
                },
                indent=2,
            )
        )
    return {
        "node_count": len(nodes),
        "edge_count": len(seen),
        "isolated_nodes": sorted(node_set - {x for e in seen for x in e}),
    }


def write_nodes_file(nodes):
    inventory = []
    with INVENTORY.open(newline="", encoding="utf-8") as f:
        inventory = list(csv.DictReader(f))
    old_names = [r["node_name"] for r in inventory]
    rows = []
    for idx, node in enumerate(nodes, 1):
        inv = inventory[idx - 1] if idx - 1 < len(inventory) else {}
        rows.append(
            {
                "index": idx,
                "node_name": node,
                "original_inventory_name": old_names[idx - 1] if idx - 1 < len(old_names) else "",
                "label_changed": "Y"
                if idx - 1 < len(old_names) and node != old_names[idx - 1]
                else "N",
                "stable_node_id": inv.get("stable_node_id", ""),
                "component_type": inv.get("component_type", ""),
                "node_kind": inv.get("node_kind", ""),
                "centroid_x": inv.get("centroid_x", ""),
                "centroid_y": inv.get("centroid_y", ""),
            }
        )
    out = RESULTS / "final_connectivity_nodes.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out, sum(1 for r in rows if r["label_changed"] == "Y")


def copy_round_aliases():
    aliases = {
        "current_round_01_diego_matrix.csv": "round_01_diego_matrix.csv",
        "current_round_01_jennifer_matrix.csv": "round_01_jennifer_matrix.csv",
        "current_round_02_diego_matrix.csv": "round_02_diego_matrix.csv",
        "current_round_02_jennifer_matrix.csv": "round_02_jennifer_matrix.csv",
        "current_round_01_diego_edges.csv": "round_01_diego_edges.csv",
        "current_round_01_jennifer_edges.csv": "round_01_jennifer_edges.csv",
        "current_round_02_diego_edges.csv": "round_02_diego_edges.csv",
        "current_round_02_jennifer_edges.csv": "round_02_jennifer_edges.csv",
    }
    copied = []
    for src_name, dst_name in aliases.items():
        src = RESULTS / src_name
        if src.exists():
            dst = RESULTS / dst_name
            shutil.copyfile(src, dst)
            copied.append(dst.name)
    return copied


def write_final_outputs():
    final_edges = RESULTS / "current_round_02_jennifer_edges.csv"
    final_matrix = RESULTS / "current_round_02_jennifer_matrix.csv"
    if not final_edges.exists() or not final_matrix.exists():
        final_edges = RESULTS / "current_round_02_diego_edges.csv"
        final_matrix = RESULTS / "current_round_02_diego_matrix.csv"
    summary = validate(final_edges, final_matrix)
    nodes, _ = load_matrix(final_matrix)

    final_edges_out = RESULTS / "final_connectivity_edges.csv"
    final_matrix_out = RESULTS / "final_connectivity_matrix.csv"
    canonical_out = RESULTS / "connectivity_matrix.csv"
    shutil.copyfile(final_edges, final_edges_out)
    shutil.copyfile(final_matrix, final_matrix_out)
    shutil.copyfile(final_matrix, canonical_out)
    nodes_out, label_changes = write_nodes_file(nodes)
    copied = copy_round_aliases()

    validation = {
        "family": FAMILY,
        "document": DOC,
        "iteration": ITERATION,
        "source_edges": str(final_edges),
        "source_matrix": str(final_matrix),
        "node_count": summary["node_count"],
        "edge_count": summary["edge_count"],
        "isolated_nodes": summary["isolated_nodes"],
        "label_changes_vs_prepared_inventory": label_changes,
        "checks": {
            "endpoints_valid": True,
            "no_duplicate_undirected_edges": True,
            "no_self_edges": True,
            "matrix_symmetric": True,
            "diagonal_zero": True,
            "matrix_edge_count_matches_edge_csv": True,
        },
        "source_discipline": "Only blind input resources and input-derived/current-round artifacts were used for extraction; no GT/evaluation/scoring files were used.",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "round_aliases_copied": copied,
    }
    validation_out = RESULTS / "final_connectivity_validation.json"
    validation_out.write_text(json.dumps(validation, indent=2), encoding="utf-8")

    edge_rows = load_edges(final_edges_out)
    by_region = Counter(r.get("region", "") for r in edge_rows)
    notes = [
        "# Final Connectivity Summary - Improved Doc 17 Iteration 1",
        "",
        "Blind extraction only. No ground truth, evaluation, scoring, or GT-derived feedback was used during extraction.",
        "",
        f"- Nodes: {summary['node_count']}",
        f"- Edges: {summary['edge_count']}",
        f"- Isolated nodes: {len(summary['isolated_nodes'])}",
        f"- Label corrections vs prepared inventory: {label_changes}",
        "- Saturation: Diego round 2 accepted Jennifer round 1 exactly; Jennifer round 2 is the final reviewer confirmation when present.",
        "",
        "## Final Files",
        "",
        f"- `connectivity_matrix.csv`",
        f"- `final_connectivity_matrix.csv`",
        f"- `final_connectivity_edges.csv`",
        f"- `final_connectivity_nodes.csv`",
        f"- `final_connectivity_validation.json`",
        "",
        "## Region Edge Counts",
        "",
    ]
    for region, count in sorted(by_region.items()):
        notes.append(f"- {region or '(blank)'}: {count}")
    notes.extend(
        [
            "",
            "## Validation",
            "",
            "- Endpoints valid.",
            "- No duplicate undirected edges.",
            "- No self-edges.",
            "- Matrix symmetric.",
            "- Diagonal zero.",
            "- Matrix edge count matches edge CSV.",
        ]
    )
    summary_out = RESULTS / "final_connectivity_summary.md"
    summary_out.write_text("\n".join(notes) + "\n", encoding="utf-8")

    return validation


def update_tracker(validation):
    start_ts = parse_ts(TASK_START_UTC)
    diego_path = find_agent_log(DIEGO_ID)
    jennifer_path = find_agent_log(JENNIFER_ID)
    diego = cumulative_usage(diego_path)
    jennifer = cumulative_usage(jennifer_path)
    subagents = add_usage(diego, jennifer)

    main = summed_last_usage(MAIN_LOG, start_ts=start_ts)
    actual_total = add_usage(subagents, main)

    # Approximate one-agent/one-round counterfactual from Diego round-1 cumulative
    # before the first subagent completion notification reached the parent.
    diego_round1 = cumulative_usage_before(diego_path, parse_ts("2026-07-27T16:39:30Z"))
    single_low = diego_round1["total_tokens"] + int(main["total_tokens"] * 0.25)
    single_expected = diego_round1["total_tokens"] + int(main["total_tokens"] * 0.50)
    single_high = diego_round1["total_tokens"] + int(main["total_tokens"] * 1.00)

    final_margin_expected = 50000
    final_margin_high = 150000
    workflow_low = actual_total["total_tokens"]
    workflow_expected = actual_total["total_tokens"] + final_margin_expected
    workflow_high = actual_total["total_tokens"] + final_margin_high

    with TRACKER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise ValueError("tracker header missing")

    def is_current_doc17_row(row):
        return (
            row.get("family") == FAMILY
            and row.get("document") == str(DOC)
            and row.get("iteration") == str(ITERATION)
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )

    rows = [r for r in rows if not is_current_doc17_row(r)]
    row = {name: "" for name in fieldnames}
    row.update(
        {
            "family": FAMILY,
            "document": str(DOC),
            "iteration": str(ITERATION),
            "workflow_label": f"{FAMILY} doc {DOC} / Iteration {ITERATION}",
            "record_type": "multi_agent_token_usage_unvalidated_final",
            "metric_label": "Final connectivity -- unvalidated",
            "metric_agent": "Final",
            "metric_round": "final",
            "is_selected_final_metric": "1",
            "final_metric_selection_basis": "final saturated multi-agent extraction; validation metrics pending",
            "validation_note": "No GT or GT-derived validation metric file used during extraction; metrics intentionally blank pending after-the-fact validation.",
            "actual_multi_agent_model_calls": str(actual_total["model_calls"]),
            "actual_multi_agent_input_tokens": str(actual_total["input_tokens"]),
            "actual_multi_agent_cached_input_tokens": str(actual_total["cached_input_tokens"]),
            "actual_multi_agent_output_tokens": str(actual_total["output_tokens"]),
            "actual_multi_agent_reasoning_output_tokens": str(actual_total["reasoning_output_tokens"]),
            "actual_multi_agent_total_tokens": str(actual_total["total_tokens"]),
            "image_file_input_note": "not separately exposed; included in input_tokens",
            "token_usage_basis": "actual completed subagent cumulative token_count logs plus main-thread per-call token_count logs after doc17 task start; final assistant response is estimated only in workflow_* high/expected margins",
            "main_model_calls": str(main["model_calls"]),
            "main_input_tokens": str(main["input_tokens"]),
            "main_cached_input_tokens": str(main["cached_input_tokens"]),
            "main_output_tokens": str(main["output_tokens"]),
            "main_reasoning_output_tokens": str(main["reasoning_output_tokens"]),
            "main_total_tokens": str(main["total_tokens"]),
            "diego_model_calls": str(diego["model_calls"]),
            "diego_input_tokens": str(diego["input_tokens"]),
            "diego_cached_input_tokens": str(diego["cached_input_tokens"]),
            "diego_output_tokens": str(diego["output_tokens"]),
            "diego_reasoning_output_tokens": str(diego["reasoning_output_tokens"]),
            "diego_total_tokens": str(diego["total_tokens"]),
            "jennifer_model_calls": str(jennifer["model_calls"]),
            "jennifer_input_tokens": str(jennifer["input_tokens"]),
            "jennifer_cached_input_tokens": str(jennifer["cached_input_tokens"]),
            "jennifer_output_tokens": str(jennifer["output_tokens"]),
            "jennifer_reasoning_output_tokens": str(jennifer["reasoning_output_tokens"]),
            "jennifer_total_tokens": str(jennifer["total_tokens"]),
            "single_agent_proxy_basis": "Diego round 1 from the same multi-agent workflow used as one-agent/one-round proxy; not an independent single-agent execution",
            "single_agent_round1_proxy_metric_label": "Diego -- Round 1",
            "single_agent_low_total_tokens": str(single_low),
            "single_agent_expected_total_tokens": str(single_expected),
            "single_agent_high_total_tokens": str(single_high),
            "single_agent_estimate_basis": "Diego round-1 cumulative usage plus 25%/50%/100% of observed main orchestration tokens after task start",
            "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available. Single-agent fields are counterfactual/proxy estimates, not a separately executed run.",
            "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
            "completed_subagent_model_calls": str(subagents["model_calls"]),
            "completed_subagent_input_tokens": str(subagents["input_tokens"]),
            "completed_subagent_cached_input_tokens": str(subagents["cached_input_tokens"]),
            "completed_subagent_output_tokens": str(subagents["output_tokens"]),
            "completed_subagent_reasoning_output_tokens": str(subagents["reasoning_output_tokens"]),
            "completed_subagent_total_tokens": str(subagents["total_tokens"]),
            "main_low_estimate_tokens": str(main["total_tokens"]),
            "main_expected_estimate_tokens": str(main["total_tokens"] + final_margin_expected),
            "main_high_estimate_tokens": str(main["total_tokens"] + final_margin_high),
            "workflow_low_estimate_total_tokens": str(workflow_low),
            "workflow_expected_estimate_total_tokens": str(workflow_expected),
            "workflow_high_estimate_total_tokens": str(workflow_high),
            "token_update_timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        }
    )
    rows.append(row)
    with TRACKER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    note = f"""

## Doc 17 Iteration 1 Update - {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}

Added/replaced `Improved doc 17 / Iteration 1` as `record_type=multi_agent_token_usage_unvalidated_final`.

Token status:
- Main actual usage after doc17 task start: {main['model_calls']} calls, {main['total_tokens']} total tokens.
- Diego actual cumulative usage: {diego['model_calls']} calls, {diego['total_tokens']} total tokens.
- Jennifer actual cumulative usage: {jennifer['model_calls']} calls, {jennifer['total_tokens']} total tokens.
- Actual total recorded so far: {actual_total['model_calls']} calls, {actual_total['total_tokens']} total tokens.
- Workflow low/expected/high estimate = {workflow_low} / {workflow_expected} / {workflow_high} tokens.
- One-agent/one-round proxy low/expected/high = {single_low} / {single_expected} / {single_high} tokens.

Extraction status:
- Final output stored at `{RESULTS}`.
- Saturated final matrix has {validation['node_count']} nodes and {validation['edge_count']} visually supported unique edges.
- Label corrections vs prepared inventory: {validation['label_changes_vs_prepared_inventory']}.
- No validation metrics were used during extraction.
- FP/FN/precision/recall/F1 are blank for doc 17 until an after-the-fact validation metrics CSV is available.
"""
    with TRACKER_NOTES.open("a", encoding="utf-8") as f:
        f.write(note)

    usage_out = RESULTS / "token_usage_doc17_iteration1_current.json"
    usage_out.write_text(
        json.dumps(
            {
                "main": main,
                "diego": diego,
                "jennifer": jennifer,
                "completed_subagents": subagents,
                "actual_total_recorded": actual_total,
                "workflow_low_estimate_total_tokens": workflow_low,
                "workflow_expected_estimate_total_tokens": workflow_expected,
                "workflow_high_estimate_total_tokens": workflow_high,
                "single_agent_proxy": {
                    "diego_round1_usage": diego_round1,
                    "low_total_tokens": single_low,
                    "expected_total_tokens": single_expected,
                    "high_total_tokens": single_high,
                    "basis": "Diego round-1 cumulative usage plus 25%/50%/100% of observed main orchestration tokens after task start.",
                },
                "task_start_utc": TASK_START_UTC,
                "diego_log": str(diego_path) if diego_path else "",
                "jennifer_log": str(jennifer_path) if jennifer_path else "",
                "main_log": str(MAIN_LOG),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return usage_out, actual_total, workflow_expected


def main():
    validation = write_final_outputs()
    usage_out, actual_total, workflow_expected = update_tracker(validation)
    print(json.dumps(validation, indent=2))
    print(f"token_usage_json={usage_out}")
    print(f"actual_total_tokens={actual_total['total_tokens']}")
    print(f"workflow_expected_total_tokens={workflow_expected}")


if __name__ == "__main__":
    main()
