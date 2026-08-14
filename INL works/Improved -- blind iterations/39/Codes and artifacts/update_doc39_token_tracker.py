import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\39")
RESULTS = BASE / "Results" / "Iteration_1"
TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"
MODEL_CALLS_CSV = RESULTS / "token_usage_model_calls.csv"
USAGE_JSON = RESULTS / "token_usage_actual_estimate.json"
VALIDATION_JSON = RESULTS / "final_connectivity_validation.json"

MAIN_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\06\23\rollout-2026-06-23T09-16-37-019ef50d-f35f-7dc2-a1f6-b49c274038fe.jsonl"
)
SUBAGENTS = [
    {
        "agent_id": "019fa4c5-6689-7e52-a791-9c8404d200f8",
        "nickname": "Dewey",
        "agent_role": "Diego",
        "round": "round_01",
        "log": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27\rollout-2026-07-27T12-10-28-019fa4c5-6689-7e52-a791-9c8404d200f8.jsonl"
        ),
    },
    {
        "agent_id": "019fa4cb-63d2-7282-b57e-cc21ff33962f",
        "nickname": "Sartre",
        "agent_role": "Jennifer",
        "round": "round_01",
        "log": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27\rollout-2026-07-27T12-17-01-019fa4cb-63d2-7282-b57e-cc21ff33962f.jsonl"
        ),
    },
    {
        "agent_id": "019fa4d3-6e33-79d2-98f3-1bd69207b24b",
        "nickname": "Ampere",
        "agent_role": "Diego",
        "round": "round_02",
        "log": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27\rollout-2026-07-27T12-25-48-019fa4d3-6e33-79d2-98f3-1bd69207b24b.jsonl"
        ),
    },
    {
        "agent_id": "019fa4d7-933d-7cc2-8f4b-833a27af6f59",
        "nickname": "Heisenberg",
        "agent_role": "Jennifer",
        "round": "round_02",
        "log": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27\rollout-2026-07-27T12-30-19-019fa4d7-933d-7cc2-8f4b-833a27af6f59.jsonl"
        ),
    },
]


def parse_ts(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def usage_zero():
    return {
        "model_calls": 0,
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }


def add_usage(acc, usage):
    acc["model_calls"] += 1
    for key in [
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
        "total_tokens",
    ]:
        acc[key] += int(usage.get(key, 0) or 0)


def extract_text_from_user_payload(payload):
    if payload.get("type") != "message" or payload.get("role") != "user":
        return ""
    parts = payload.get("content", [])
    texts = []
    for part in parts:
        if isinstance(part, dict):
            texts.append(str(part.get("text") or ""))
    return "\n".join(texts)


def find_latest_main_start(log_path):
    latest = None
    with log_path.open(encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            payload = obj.get("payload", {})
            text = ""
            if obj.get("type") == "response_item":
                text = extract_text_from_user_payload(payload)
            if (
                "Improved -- blind iterations\\39\\Input resources" in text
                or "Improved -- blind iterations\\\\39\\\\Input resources" in text
            ):
                latest = parse_ts(obj["timestamp"])
    if latest is None:
        raise RuntimeError("Could not locate current doc39 user boundary in parent log.")
    return latest


def collect_token_calls(log_path, source, start_ts=None, metadata=None):
    metadata = metadata or {}
    rows = []
    total = usage_zero()
    with log_path.open(encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") != "event_msg":
                continue
            payload = obj.get("payload", {})
            if payload.get("type") != "token_count":
                continue
            ts = parse_ts(obj["timestamp"])
            if start_ts is not None and ts < start_ts:
                continue
            usage = payload.get("info", {}).get("last_token_usage", {})
            add_usage(total, usage)
            rows.append(
                {
                    "source": source,
                    "agent_role": metadata.get("agent_role", "Main"),
                    "agent_id": metadata.get("agent_id", "main"),
                    "nickname": metadata.get("nickname", "main"),
                    "round": metadata.get("round", "main"),
                    "session_log": str(log_path),
                    "call_index": total["model_calls"],
                    "timestamp": obj["timestamp"],
                    "input_tokens": usage.get("input_tokens", 0),
                    "cached_input_tokens": usage.get("cached_input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                    "reasoning_output_tokens": usage.get("reasoning_output_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                    "image_file_input_tokens": "",
                    "image_file_input_note": "not separately exposed; included in input_tokens",
                }
            )
    return total, rows


def combine(*parts):
    out = usage_zero()
    out["model_calls"] = 0
    for part in parts:
        for key, value in part.items():
            out[key] += value
    return out


def fmt(value):
    return str(value)


def blank_row(fieldnames):
    return {field: "" for field in fieldnames}


start_ts = find_latest_main_start(MAIN_LOG)
main_total, call_rows = collect_token_calls(
    MAIN_LOG,
    "main_agent_current_doc39_window",
    start_ts=start_ts,
    metadata={"agent_role": "Main", "agent_id": "main", "nickname": "main", "round": "main"},
)

by_role = {"Diego": usage_zero(), "Jennifer": usage_zero()}
round_totals = []
for sub in SUBAGENTS:
    total, rows = collect_token_calls(
        sub["log"],
        "subagent_full_session",
        metadata=sub,
    )
    call_rows.extend(rows)
    for key, value in total.items():
        by_role[sub["agent_role"]][key] += value
    round_totals.append({**sub, "usage": total})

completed_subagents = combine(by_role["Diego"], by_role["Jennifer"])
observed_workflow = combine(main_total, completed_subagents)
diego_r1 = next(item["usage"] for item in round_totals if item["agent_role"] == "Diego" and item["round"] == "round_01")

single_low = diego_r1["total_tokens"] + round(main_total["total_tokens"] * 0.25)
single_expected = diego_r1["total_tokens"] + round(main_total["total_tokens"] * 0.50)
single_high = diego_r1["total_tokens"] + main_total["total_tokens"]

with VALIDATION_JSON.open(encoding="utf-8") as f:
    final_validation = json.load(f)

call_fieldnames = [
    "source",
    "agent_role",
    "agent_id",
    "nickname",
    "round",
    "session_log",
    "call_index",
    "timestamp",
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
    "image_file_input_tokens",
    "image_file_input_note",
]
with MODEL_CALLS_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=call_fieldnames)
    writer.writeheader()
    writer.writerows(call_rows)

timestamp = datetime.now(ZoneInfo("America/Denver")).isoformat(timespec="seconds")
usage_summary = {
    "family": "Improved",
    "document": 39,
    "iteration": 1,
    "main_start_boundary_utc": start_ts.isoformat(),
    "token_update_timestamp": timestamp,
    "basis": "Actual local Codex token_count last_token_usage logs for the main agent since the latest doc39 user boundary plus all four completed Diego/Jennifer subagent session logs; final response not included.",
    "main": main_total,
    "diego": by_role["Diego"],
    "jennifer": by_role["Jennifer"],
    "completed_subagents": completed_subagents,
    "observed_workflow": observed_workflow,
    "round_totals": [
        {
            "agent_role": item["agent_role"],
            "round": item["round"],
            "agent_id": item["agent_id"],
            "nickname": item["nickname"],
            "usage": item["usage"],
        }
        for item in round_totals
    ],
    "single_agent_one_round_proxy": {
        "low_total_tokens": single_low,
        "expected_total_tokens": single_expected,
        "high_total_tokens": single_high,
        "basis": "Diego round 1 actual total plus 25%/50%/100% of observed main-agent orchestration tokens, as a one-agent one-round proxy.",
    },
    "image_file_input_tokens": None,
    "image_file_input_note": "not separately exposed; included in input_tokens",
}
USAGE_JSON.write_text(json.dumps(usage_summary, indent=2), encoding="utf-8")

with TRACKER_CSV.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames or []
    existing_rows = list(reader)

filtered_rows = [
    row
    for row in existing_rows
    if not (
        row.get("family") == "Improved"
        and row.get("document") == "39"
        and row.get("iteration") == "1"
        and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
    )
]

row = blank_row(fieldnames)
row.update(
    {
        "family": "Improved",
        "document": "39",
        "iteration": "1",
        "workflow_label": "Improved doc 39 / Iteration 1",
        "record_type": "multi_agent_token_usage_unvalidated_final",
        "metric_label": "Final connectivity -- unvalidated",
        "metric_agent": "Final",
        "metric_round": "final",
        "is_selected_final_metric": "1",
        "final_metric_selection_basis": "final saturated multi-agent extraction; validation metrics pending",
        "validation_note": "No GT or GT-derived validation metric file used during extraction; metrics intentionally blank pending after-the-fact validation.",
        "actual_multi_agent_model_calls": fmt(observed_workflow["model_calls"]),
        "actual_multi_agent_input_tokens": fmt(observed_workflow["input_tokens"]),
        "actual_multi_agent_cached_input_tokens": fmt(observed_workflow["cached_input_tokens"]),
        "actual_multi_agent_output_tokens": fmt(observed_workflow["output_tokens"]),
        "actual_multi_agent_reasoning_output_tokens": fmt(observed_workflow["reasoning_output_tokens"]),
        "actual_multi_agent_total_tokens": fmt(observed_workflow["total_tokens"]),
        "image_file_input_tokens": "",
        "image_file_input_note": "not separately exposed; included in input_tokens",
        "token_usage_basis": "actual local Codex token_count last_token_usage logs for the main agent since the latest doc39 user boundary plus all four completed Diego/Jennifer subagent session logs; final response not included",
        "main_model_calls": fmt(main_total["model_calls"]),
        "main_input_tokens": fmt(main_total["input_tokens"]),
        "main_cached_input_tokens": fmt(main_total["cached_input_tokens"]),
        "main_output_tokens": fmt(main_total["output_tokens"]),
        "main_reasoning_output_tokens": fmt(main_total["reasoning_output_tokens"]),
        "main_total_tokens": fmt(main_total["total_tokens"]),
        "diego_model_calls": fmt(by_role["Diego"]["model_calls"]),
        "diego_input_tokens": fmt(by_role["Diego"]["input_tokens"]),
        "diego_cached_input_tokens": fmt(by_role["Diego"]["cached_input_tokens"]),
        "diego_output_tokens": fmt(by_role["Diego"]["output_tokens"]),
        "diego_reasoning_output_tokens": fmt(by_role["Diego"]["reasoning_output_tokens"]),
        "diego_total_tokens": fmt(by_role["Diego"]["total_tokens"]),
        "jennifer_model_calls": fmt(by_role["Jennifer"]["model_calls"]),
        "jennifer_input_tokens": fmt(by_role["Jennifer"]["input_tokens"]),
        "jennifer_cached_input_tokens": fmt(by_role["Jennifer"]["cached_input_tokens"]),
        "jennifer_output_tokens": fmt(by_role["Jennifer"]["output_tokens"]),
        "jennifer_reasoning_output_tokens": fmt(by_role["Jennifer"]["reasoning_output_tokens"]),
        "jennifer_total_tokens": fmt(by_role["Jennifer"]["total_tokens"]),
        "single_agent_proxy_basis": "single agent one-round proxy based on Diego round 1 actual plus 25%/50%/100% of observed main-agent orchestration tokens",
        "single_agent_low_total_tokens": fmt(single_low),
        "single_agent_expected_total_tokens": fmt(single_expected),
        "single_agent_high_total_tokens": fmt(single_high),
        "single_agent_estimate_basis": "Diego round 1 actual total plus low/expected/high main-agent fractions of 25%/50%/100%; output quality/performance unknown until validation",
        "single_agent_expected_token_savings_vs_multi_agent": fmt(single_expected - observed_workflow["total_tokens"]),
        "single_agent_expected_token_savings_pct_vs_multi_agent": f"{(single_expected - observed_workflow['total_tokens']) / observed_workflow['total_tokens']:.6f}",
        "multi_agent_vs_single_agent_expected_token_ratio": f"{observed_workflow['total_tokens'] / single_expected:.6f}" if single_expected else "",
        "extra_multi_agent_tokens_vs_single_agent_expected": fmt(observed_workflow["total_tokens"] - single_expected),
        "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available. Image/file input tokens are not separately exposed; final response not included in this snapshot.",
        "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
        "completed_subagent_model_calls": fmt(completed_subagents["model_calls"]),
        "completed_subagent_input_tokens": fmt(completed_subagents["input_tokens"]),
        "completed_subagent_cached_input_tokens": fmt(completed_subagents["cached_input_tokens"]),
        "completed_subagent_output_tokens": fmt(completed_subagents["output_tokens"]),
        "completed_subagent_reasoning_output_tokens": fmt(completed_subagents["reasoning_output_tokens"]),
        "completed_subagent_total_tokens": fmt(completed_subagents["total_tokens"]),
        "main_low_estimate_tokens": fmt(main_total["total_tokens"]),
        "main_expected_estimate_tokens": fmt(main_total["total_tokens"]),
        "main_high_estimate_tokens": fmt(main_total["total_tokens"]),
        "workflow_low_estimate_total_tokens": fmt(observed_workflow["total_tokens"]),
        "workflow_expected_estimate_total_tokens": fmt(observed_workflow["total_tokens"]),
        "workflow_high_estimate_total_tokens": fmt(observed_workflow["total_tokens"]),
        "token_update_timestamp": timestamp,
    }
)
filtered_rows.append(row)

with TRACKER_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered_rows)

note = f"""

## Doc 39 Iteration 1 Current Update - {timestamp}

Updated/replaced `Improved doc 39 / Iteration 1` after the current one-iteration Diego/Jennifer workflow.

Extraction:
- Final source: `round_02_jennifer`, accepting Diego round 2 after focused review.
- Final matrix: {final_validation['node_count']} nodes and {final_validation['keep_edge_count']} kept edges.
- Excluded review edges: {final_validation['uncertain_edge_count']} uncertain, {final_validation['remove_edge_count']} removed.
- Key refinement: `LC-A`, `LC-B`, and `CONTROL-ROOM-ANNUNCIATION` were treated as labels/annotation text, not final nodes; both long RPS-to-JB dashed control paths were kept after zoomed raw-image review.
- No GT, GT-derived feedback, scoring output, evaluator file, or archived prior result was used during extraction.

Token snapshot:
- Main agent observed: {main_total['model_calls']} calls, {main_total['total_tokens']} total tokens from the latest doc39 user boundary.
- Diego aggregate: {by_role['Diego']['model_calls']} calls, {by_role['Diego']['total_tokens']} total tokens.
- Jennifer aggregate: {by_role['Jennifer']['model_calls']} calls, {by_role['Jennifer']['total_tokens']} total tokens.
- Completed subagents: {completed_subagents['model_calls']} calls, {completed_subagents['total_tokens']} total tokens.
- Observed multi-agent workflow: {observed_workflow['model_calls']} calls, {observed_workflow['total_tokens']} total tokens.
- Single-agent one-round proxy: low/expected/high = {single_low} / {single_expected} / {single_high} tokens.

Limitations:
- Image/file input tokens are not separately exposed in the local Codex `token_count` records; they are included inside `input_tokens`.
- This is an observed pre-final-response snapshot. The final assistant response and any later bookkeeping calls are not included.
- FP/FN/precision/recall/F1 remain blank until after-the-fact validation metrics are available.
"""
with TRACKER_NOTES.open("a", encoding="utf-8", newline="\n") as f:
    f.write(note)

print(json.dumps(usage_summary, indent=2))
