import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


RESULT_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\6\Results\Iteration_1")
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
DIEGO_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\07\27"
    r"\rollout-2026-07-27T10-59-12-019fa484-259b-7cd2-8c68-342432c6e4a8.jsonl"
)
JENNIFER_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\07\27"
    r"\rollout-2026-07-27T11-08-15-019fa48c-6e48-7d40-94f6-b13fbd9c9ed7.jsonl"
)

MAIN_START_TS = "2026-07-27T16:56:12.813Z"
DIEGO_ROUND1_CUTOFF_TS = "2026-07-27T17:08:15.000Z"

FIELDS = [
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
]


def usage_from_log(path, start_ts=None, end_ts=None):
    events = []
    with path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if "token_count" not in line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = obj.get("payload", {})
            if payload.get("type") != "token_count":
                continue
            ts = obj.get("timestamp", "")
            if start_ts is not None and ts < start_ts:
                continue
            if end_ts is not None and ts > end_ts:
                continue
            info = payload.get("info", {})
            events.append(
                {
                    "timestamp": ts,
                    "last_token_usage": info.get("last_token_usage", {}),
                    "total_token_usage": info.get("total_token_usage", {}),
                }
            )
    sums = {
        field: sum(
            int(event["last_token_usage"].get(field, 0) or 0) for event in events
        )
        for field in FIELDS
    }
    return {
        "model_calls": len(events),
        "usage": sums,
        "first_timestamp": events[0]["timestamp"] if events else "",
        "last_timestamp": events[-1]["timestamp"] if events else "",
        "final_cumulative_usage": events[-1]["total_token_usage"] if events else {},
        "log_path": str(path),
    }


def read_final_validation():
    path = RESULT_DIR / "final_connectivity_validation.json"
    return json.loads(path.read_text(encoding="utf-8"))


def blank_row(fieldnames):
    return {name: "" for name in fieldnames}


def update_tracker(summary):
    with TRACKER_CSV.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)

    rows = [
        row
        for row in rows
        if not (
            row.get("family") == "Improved"
            and row.get("document") == "6"
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]

    ts = summary["token_update_timestamp"]
    row = blank_row(fieldnames)
    row.update(
        {
            "family": "Improved",
            "document": "6",
            "iteration": "1",
            "workflow_label": "Improved doc 6 / Iteration 1",
            "record_type": "multi_agent_token_usage_unvalidated_final",
            "metric_label": "Final connectivity -- unvalidated",
            "metric_agent": "Saturated Diego/Jennifer",
            "metric_round": "round_02_jennifer",
            "is_selected_final_metric": "TRUE",
            "final_metric_selection_basis": (
                "Saturated blind multi-agent result; no GT metrics used during extraction"
            ),
            "validation_note": (
                "Unvalidated blind extraction; FP/FN/precision/recall/F1 pending "
                "after-the-fact validation."
            ),
            "actual_multi_agent_model_calls": str(summary["actual"]["model_calls"]),
            "actual_multi_agent_input_tokens": str(summary["actual"]["input_tokens"]),
            "actual_multi_agent_cached_input_tokens": str(
                summary["actual"]["cached_input_tokens"]
            ),
            "actual_multi_agent_output_tokens": str(summary["actual"]["output_tokens"]),
            "actual_multi_agent_reasoning_output_tokens": str(
                summary["actual"]["reasoning_output_tokens"]
            ),
            "actual_multi_agent_total_tokens": str(summary["actual"]["total_tokens"]),
            "image_file_input_tokens": "",
            "image_file_input_note": "not separately exposed; included in input_tokens",
            "token_usage_basis": (
                "actual completed subagent cumulative token_count logs plus main-thread "
                "per-call token_count logs after doc6 task start; final assistant response "
                "is estimated only in workflow_* high/expected margins"
            ),
            "main_model_calls": str(summary["main"]["model_calls"]),
            "main_input_tokens": str(summary["main"]["usage"]["input_tokens"]),
            "main_cached_input_tokens": str(
                summary["main"]["usage"]["cached_input_tokens"]
            ),
            "main_output_tokens": str(summary["main"]["usage"]["output_tokens"]),
            "main_reasoning_output_tokens": str(
                summary["main"]["usage"]["reasoning_output_tokens"]
            ),
            "main_total_tokens": str(summary["main"]["usage"]["total_tokens"]),
            "diego_model_calls": str(summary["diego"]["model_calls"]),
            "diego_input_tokens": str(summary["diego"]["usage"]["input_tokens"]),
            "diego_cached_input_tokens": str(
                summary["diego"]["usage"]["cached_input_tokens"]
            ),
            "diego_output_tokens": str(summary["diego"]["usage"]["output_tokens"]),
            "diego_reasoning_output_tokens": str(
                summary["diego"]["usage"]["reasoning_output_tokens"]
            ),
            "diego_total_tokens": str(summary["diego"]["usage"]["total_tokens"]),
            "jennifer_model_calls": str(summary["jennifer"]["model_calls"]),
            "jennifer_input_tokens": str(summary["jennifer"]["usage"]["input_tokens"]),
            "jennifer_cached_input_tokens": str(
                summary["jennifer"]["usage"]["cached_input_tokens"]
            ),
            "jennifer_output_tokens": str(summary["jennifer"]["usage"]["output_tokens"]),
            "jennifer_reasoning_output_tokens": str(
                summary["jennifer"]["usage"]["reasoning_output_tokens"]
            ),
            "jennifer_total_tokens": str(summary["jennifer"]["usage"]["total_tokens"]),
            "single_agent_proxy_basis": (
                "Diego round 1 from the same multi-agent workflow used as one-agent/one-round "
                "proxy; not an independent single-agent execution"
            ),
            "single_agent_low_total_tokens": str(
                summary["single_agent_proxy"]["low_total_tokens"]
            ),
            "single_agent_expected_total_tokens": str(
                summary["single_agent_proxy"]["expected_total_tokens"]
            ),
            "single_agent_high_total_tokens": str(
                summary["single_agent_proxy"]["high_total_tokens"]
            ),
            "single_agent_estimate_basis": (
                "Diego round-1 cumulative usage plus 25%/50%/100% of observed main "
                "orchestration tokens after task start"
            ),
            "single_agent_expected_token_savings_vs_multi_agent": str(
                summary["single_agent_proxy"]["expected_token_savings_vs_multi_agent"]
            ),
            "single_agent_expected_token_savings_pct_vs_multi_agent": str(
                summary["single_agent_proxy"][
                    "expected_token_savings_pct_vs_multi_agent"
                ]
            ),
            "multi_agent_vs_single_agent_expected_token_ratio": str(
                summary["single_agent_proxy"][
                    "multi_agent_vs_single_agent_expected_token_ratio"
                ]
            ),
            "extra_multi_agent_tokens_vs_single_agent_expected": str(
                summary["single_agent_proxy"][
                    "extra_multi_agent_tokens_vs_single_agent_expected"
                ]
            ),
            "data_limitations": (
                "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 "
                "are intentionally blank until an after-the-fact validation CSV is available. "
                "Single-agent fields are counterfactual/proxy estimates, not a separately "
                "executed run."
            ),
            "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
            "completed_subagent_model_calls": str(
                summary["completed_subagent"]["model_calls"]
            ),
            "completed_subagent_input_tokens": str(
                summary["completed_subagent"]["input_tokens"]
            ),
            "completed_subagent_cached_input_tokens": str(
                summary["completed_subagent"]["cached_input_tokens"]
            ),
            "completed_subagent_output_tokens": str(
                summary["completed_subagent"]["output_tokens"]
            ),
            "completed_subagent_reasoning_output_tokens": str(
                summary["completed_subagent"]["reasoning_output_tokens"]
            ),
            "completed_subagent_total_tokens": str(
                summary["completed_subagent"]["total_tokens"]
            ),
            "main_low_estimate_tokens": str(summary["main"]["usage"]["total_tokens"]),
            "main_expected_estimate_tokens": str(summary["main"]["usage"]["total_tokens"]),
            "main_high_estimate_tokens": str(summary["main"]["usage"]["total_tokens"]),
            "workflow_low_estimate_total_tokens": str(
                summary["workflow_estimate"]["low_total_tokens"]
            ),
            "workflow_expected_estimate_total_tokens": str(
                summary["workflow_estimate"]["expected_total_tokens"]
            ),
            "workflow_high_estimate_total_tokens": str(
                summary["workflow_estimate"]["high_total_tokens"]
            ),
            "token_update_timestamp": ts,
        }
    )

    rows.append(row)
    with TRACKER_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_notes(summary):
    note = f"""

## Doc 6 Iteration 1 Update - {summary['token_update_timestamp']}

Added/replaced `Improved doc 6 / Iteration 1` as `record_type=multi_agent_token_usage_unvalidated_final`.

Token status:
- Main actual usage after doc6 task start: {summary['main']['model_calls']} calls, {summary['main']['usage']['total_tokens']} total tokens.
- Diego actual cumulative usage: {summary['diego']['model_calls']} calls, {summary['diego']['usage']['total_tokens']} total tokens.
- Jennifer actual cumulative usage: {summary['jennifer']['model_calls']} calls, {summary['jennifer']['usage']['total_tokens']} total tokens.
- Completed subagent total: {summary['completed_subagent']['model_calls']} calls, {summary['completed_subagent']['total_tokens']} total tokens.
- Actual total recorded so far: {summary['actual']['model_calls']} calls, {summary['actual']['total_tokens']} total tokens.
- Workflow low/expected/high estimate = {summary['workflow_estimate']['low_total_tokens']} / {summary['workflow_estimate']['expected_total_tokens']} / {summary['workflow_estimate']['high_total_tokens']} tokens.
- One-agent/one-round proxy low/expected/high = {summary['single_agent_proxy']['low_total_tokens']} / {summary['single_agent_proxy']['expected_total_tokens']} / {summary['single_agent_proxy']['high_total_tokens']} tokens.

Extraction status:
- Final output stored at `C:\\Asif_all_python_projects\\INL\\Improved -- blind iterations\\6\\Results\\Iteration_1`.
- Saturated final matrix has {summary['final_validation']['node_count']} nodes and {summary['final_validation']['edge_count']} visually supported unique edges.
- Central lower bus label corrected/retained as `BUS-4KV-N`; `BUS-6KV-N` is absent.
- No validation metrics were used during extraction.
- FP/FN/precision/recall/F1 are blank for doc 6 until an after-the-fact validation metrics CSV is available.
"""
    with TRACKER_NOTES.open("a", encoding="utf-8") as handle:
        handle.write(note)


def build_summary():
    main = usage_from_log(MAIN_LOG, start_ts=MAIN_START_TS)
    diego = usage_from_log(DIEGO_LOG)
    jennifer = usage_from_log(JENNIFER_LOG)
    diego_round1 = usage_from_log(DIEGO_LOG, end_ts=DIEGO_ROUND1_CUTOFF_TS)

    completed_subagent = {
        field: diego["usage"][field] + jennifer["usage"][field] for field in FIELDS
    }
    completed_subagent["model_calls"] = diego["model_calls"] + jennifer["model_calls"]

    actual = {
        field: main["usage"][field] + completed_subagent[field] for field in FIELDS
    }
    actual["model_calls"] = main["model_calls"] + completed_subagent["model_calls"]

    main_total = main["usage"]["total_tokens"]
    single_low = int(round(diego_round1["usage"]["total_tokens"] + 0.25 * main_total))
    single_expected = int(
        round(diego_round1["usage"]["total_tokens"] + 0.50 * main_total)
    )
    single_high = int(round(diego_round1["usage"]["total_tokens"] + main_total))

    savings = single_expected - actual["total_tokens"]
    savings_pct = round(savings / actual["total_tokens"] * 100, 6)
    ratio = round(actual["total_tokens"] / single_expected, 6)
    extra = actual["total_tokens"] - single_expected

    timestamp = datetime.now(ZoneInfo("America/Denver")).isoformat(timespec="seconds")
    final_validation = read_final_validation()
    summary = {
        "document": "Improved doc 6",
        "iteration": 1,
        "token_update_timestamp": timestamp,
        "main_task_start_timestamp": MAIN_START_TS,
        "main": main,
        "diego": diego,
        "jennifer": jennifer,
        "diego_round1_proxy": diego_round1,
        "completed_subagent": completed_subagent,
        "actual": actual,
        "workflow_estimate": {
            "low_total_tokens": actual["total_tokens"],
            "expected_total_tokens": actual["total_tokens"] + 50_000,
            "high_total_tokens": actual["total_tokens"] + 150_000,
            "basis": "actual observed usage plus final response/closeout margin",
        },
        "single_agent_proxy": {
            "low_total_tokens": single_low,
            "expected_total_tokens": single_expected,
            "high_total_tokens": single_high,
            "expected_token_savings_vs_multi_agent": savings,
            "expected_token_savings_pct_vs_multi_agent": savings_pct,
            "multi_agent_vs_single_agent_expected_token_ratio": ratio,
            "extra_multi_agent_tokens_vs_single_agent_expected": extra,
            "basis": (
                "Diego round 1 cumulative usage plus 25%/50%/100% of observed main "
                "orchestration usage"
            ),
        },
        "final_validation": final_validation,
        "logs": {
            "main": str(MAIN_LOG),
            "diego": str(DIEGO_LOG),
            "jennifer": str(JENNIFER_LOG),
        },
    }
    return summary


def main():
    summary = build_summary()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    (RESULT_DIR / "token_usage_actual_estimate.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    update_tracker(summary)
    append_notes(summary)
    print(json.dumps(summary["actual"], indent=2))
    print(json.dumps(summary["single_agent_proxy"], indent=2))


if __name__ == "__main__":
    main()
