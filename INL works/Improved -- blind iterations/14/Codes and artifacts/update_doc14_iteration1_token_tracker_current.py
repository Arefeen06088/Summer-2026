from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RESULTS_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\14\Results\Iteration_1")
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
DOC_NEEDLE = r"Improved -- blind iterations\14\Input resources"
FIELDS = [
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
]

SUBAGENT_LOGS = [
    {
        "agent": "Diego",
        "round": "1",
        "nickname": "Pauli",
        "session_id": "019fa49c-7527-7740-a563-2059f013f512",
        "path": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27"
            r"\rollout-2026-07-27T11-25-45-019fa49c-7527-7740-a563-2059f013f512.jsonl"
        ),
    },
    {
        "agent": "Jennifer",
        "round": "1",
        "nickname": "Mill",
        "session_id": "019fa4a3-105e-7410-8391-0ee374661c12",
        "path": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27"
            r"\rollout-2026-07-27T11-32-58-019fa4a3-105e-7410-8391-0ee374661c12.jsonl"
        ),
    },
    {
        "agent": "Diego",
        "round": "2",
        "nickname": "Ohm",
        "session_id": "019fa4a7-14f4-7cc2-b0f5-82058a824048",
        "path": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27"
            r"\rollout-2026-07-27T11-37-21-019fa4a7-14f4-7cc2-b0f5-82058a824048.jsonl"
        ),
    },
    {
        "agent": "Jennifer",
        "round": "2",
        "nickname": "Dirac",
        "session_id": "019fa4ac-6897-71a3-9ccb-3fde526ff5f9",
        "path": Path(
            r"C:\Users\AREFA\.codex\sessions\2026\07\27"
            r"\rollout-2026-07-27T11-43-10-019fa4ac-6897-71a3-9ccb-3fde526ff5f9.jsonl"
        ),
    },
]


def blank_usage() -> dict[str, int]:
    return {"model_calls": 0, **{field: 0 for field in FIELDS}}


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def text_from_user_payload(obj: dict) -> str:
    payload = obj.get("payload", {})
    if obj.get("type") == "event_msg" and payload.get("type") == "user_message":
        return payload.get("message", "")
    if obj.get("type") == "response_item" and payload.get("role") == "user":
        parts = []
        for item in payload.get("content", []):
            if isinstance(item, dict) and item.get("type") == "input_text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)
    return ""


def latest_doc14_start(log_path: Path) -> str:
    latest = ""
    for obj in read_jsonl(log_path):
        text = text_from_user_payload(obj)
        if DOC_NEEDLE in text:
            latest = obj.get("timestamp", latest)
    if not latest:
        raise RuntimeError(f"Could not locate latest doc14 user boundary in {log_path}")
    return latest


def token_events(log_path: Path, start_ts: str | None = None) -> list[dict[str, object]]:
    events = []
    for obj in read_jsonl(log_path):
        ts = obj.get("timestamp", "")
        if start_ts and ts < start_ts:
            continue
        payload = obj.get("payload", {})
        if obj.get("type") != "event_msg" or payload.get("type") != "token_count":
            continue
        info = payload.get("info", {})
        usage = info.get("last_token_usage") or {}
        events.append(
            {
                "timestamp": ts,
                **{field: int(usage.get(field, 0) or 0) for field in FIELDS},
            }
        )
    return events


def summarize_events(events: list[dict[str, object]]) -> dict[str, int | str]:
    summary: dict[str, int | str] = blank_usage()
    summary["model_calls"] = len(events)
    for field in FIELDS:
        summary[field] = sum(int(event.get(field, 0) or 0) for event in events)
    if events:
        summary["first_token_count_timestamp"] = str(events[0]["timestamp"])
        summary["last_token_count_timestamp"] = str(events[-1]["timestamp"])
    else:
        summary["first_token_count_timestamp"] = ""
        summary["last_token_count_timestamp"] = ""
    return summary


def add_usage(a: dict[str, int | str], b: dict[str, int | str]) -> dict[str, int]:
    out = blank_usage()
    out["model_calls"] = int(a.get("model_calls", 0) or 0) + int(b.get("model_calls", 0) or 0)
    for field in FIELDS:
        out[field] = int(a.get(field, 0) or 0) + int(b.get(field, 0) or 0)
    return out


def aggregate(parts: list[dict[str, int | str]]) -> dict[str, int]:
    total = blank_usage()
    for part in parts:
        total = add_usage(total, part)
    return total


def write_call_csv(call_rows: list[dict[str, object]]) -> None:
    path = RESULTS_DIR / "token_usage_model_calls.csv"
    fieldnames = [
        "workflow_label",
        "family",
        "document",
        "iteration",
        "agent",
        "agent_round",
        "agent_nickname",
        "session_id",
        "session_file",
        "model_call_index_in_session",
        "timestamp",
        *FIELDS,
        "image_file_input_tokens",
        "image_file_input_note",
        "usage_source",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(call_rows)


def tracker_row(fieldnames: list[str], payload: dict[str, object]) -> dict[str, str]:
    row = {field: "" for field in fieldnames}
    for key, value in payload.items():
        if key in row:
            row[key] = str(value)
    return row


def write_tracker(payload: dict[str, object]) -> None:
    with TRACKER_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []

    rows = [
        row
        for row in rows
        if not (
            row.get("family") == "Improved"
            and row.get("document") == "14"
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]
    rows.append(tracker_row(fieldnames, payload))

    with TRACKER_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_notes(summary: dict[str, object]) -> None:
    notes = f"""

## Doc 14 Iteration 1 Current Update - {datetime.now().astimezone().isoformat(timespec="seconds")}

Updated `Improved doc 14 / Iteration 1` after the current one-iteration Diego/Jennifer workflow.

Extraction:
- Final source: `round_02_jennifer`, accepting Diego round 2 without corrections.
- Final matrix: 178 nodes and 190 kept edges.
- Excluded review edges: 8 uncertain, 1 removed.
- No GT, GT-derived feedback, scoring output, evaluator file, or archived prior result was used during extraction.

Token snapshot:
- Main agent observed: {summary["main"]["model_calls"]} calls, {summary["main"]["total_tokens"]:,} total tokens from the latest doc14 user boundary.
- Diego aggregate: {summary["diego"]["model_calls"]} calls, {summary["diego"]["total_tokens"]:,} total tokens.
- Jennifer aggregate: {summary["jennifer"]["model_calls"]} calls, {summary["jennifer"]["total_tokens"]:,} total tokens.
- Completed subagents: {summary["subagents"]["model_calls"]} calls, {summary["subagents"]["total_tokens"]:,} total tokens.
- Observed multi-agent workflow: {summary["workflow"]["model_calls"]} calls, {summary["workflow"]["total_tokens"]:,} total tokens.
- Single-agent one-round proxy: low/expected/high = {summary["single_agent"]["low"]:,} / {summary["single_agent"]["expected"]:,} / {summary["single_agent"]["high"]:,} tokens.

Limitations:
- Image/file input tokens are not separately exposed in the local Codex `token_count` records; they are included inside `input_tokens`.
- This is an observed pre-final-response snapshot. The final assistant response and any later bookkeeping calls are not included.
- FP/FN/precision/recall/F1 remain blank until after-the-fact validation metrics are available.
"""
    with TRACKER_NOTES.open("a", encoding="utf-8") as handle:
        handle.write(notes)


def main() -> None:
    final_validation = json.loads((RESULTS_DIR / "final_connectivity_validation.json").read_text(encoding="utf-8"))
    main_start = latest_doc14_start(MAIN_LOG)
    main_events = token_events(MAIN_LOG, start_ts=main_start)
    main_summary = summarize_events(main_events)

    call_rows = []
    for index, event in enumerate(main_events, 1):
        call_rows.append(
            {
                "workflow_label": "Improved doc 14 / Iteration 1",
                "family": "Improved",
                "document": "14",
                "iteration": "1",
                "agent": "Main",
                "agent_round": "orchestration",
                "agent_nickname": "",
                "session_id": MAIN_LOG.stem,
                "session_file": str(MAIN_LOG),
                "model_call_index_in_session": index,
                "timestamp": event["timestamp"],
                **{field: event[field] for field in FIELDS},
                "image_file_input_tokens": "",
                "image_file_input_note": "not separately exposed; included in input_tokens",
                "usage_source": "local Codex token_count last_token_usage",
            }
        )

    round_summaries = []
    for spec in SUBAGENT_LOGS:
        events = token_events(spec["path"])
        summary = summarize_events(events)
        summary.update(
            {
                "agent": spec["agent"],
                "round": spec["round"],
                "nickname": spec["nickname"],
                "session_id": spec["session_id"],
                "session_file": str(spec["path"]),
            }
        )
        round_summaries.append(summary)
        for index, event in enumerate(events, 1):
            call_rows.append(
                {
                    "workflow_label": "Improved doc 14 / Iteration 1",
                    "family": "Improved",
                    "document": "14",
                    "iteration": "1",
                    "agent": spec["agent"],
                    "agent_round": spec["round"],
                    "agent_nickname": spec["nickname"],
                    "session_id": spec["session_id"],
                    "session_file": str(spec["path"]),
                    "model_call_index_in_session": index,
                    "timestamp": event["timestamp"],
                    **{field: event[field] for field in FIELDS},
                    "image_file_input_tokens": "",
                    "image_file_input_note": "not separately exposed; included in input_tokens",
                    "usage_source": "local Codex token_count last_token_usage",
                }
            )

    diego = aggregate([s for s in round_summaries if s["agent"] == "Diego"])
    jennifer = aggregate([s for s in round_summaries if s["agent"] == "Jennifer"])
    subagents = aggregate(round_summaries)
    workflow = add_usage(main_summary, subagents)
    diego_round_1 = next(s for s in round_summaries if s["agent"] == "Diego" and s["round"] == "1")
    single_agent = {
        "low": int(round(int(diego_round_1["total_tokens"]) + 0.25 * int(main_summary["total_tokens"]))),
        "expected": int(round(int(diego_round_1["total_tokens"]) + 0.50 * int(main_summary["total_tokens"]))),
        "high": int(round(int(diego_round_1["total_tokens"]) + 1.00 * int(main_summary["total_tokens"]))),
    }

    update_timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    token_basis = (
        "actual local Codex token_count last_token_usage logs for the main agent since the latest doc14 "
        "user boundary plus all four completed Diego/Jennifer subagent session logs; final response not included"
    )
    single_basis = (
        "single-agent one-round proxy = Diego round 1 actual usage plus 25%/50%/100% of observed main-agent "
        "orchestration tokens for low/expected/high; no GT metrics used"
    )

    payload = {
        "family": "Improved",
        "document": "14",
        "iteration": "1",
        "workflow_label": "Improved doc 14 / Iteration 1",
        "record_type": "multi_agent_token_usage_unvalidated_final",
        "metric_source_path": str(RESULTS_DIR / "final_connectivity_validation.json"),
        "metric_label": "Final connectivity -- unvalidated",
        "metric_agent": "Final",
        "metric_round": "final",
        "is_selected_final_metric": "1",
        "final_metric_selection_basis": "round_02_jennifer accepted round_02_diego without corrections; saturated",
        "validation_note": (
            "No GT or GT-derived validation metric file used during extraction; metrics intentionally blank "
            "pending after-the-fact validation."
        ),
        "actual_multi_agent_model_calls": workflow["model_calls"],
        "actual_multi_agent_input_tokens": workflow["input_tokens"],
        "actual_multi_agent_cached_input_tokens": workflow["cached_input_tokens"],
        "actual_multi_agent_output_tokens": workflow["output_tokens"],
        "actual_multi_agent_reasoning_output_tokens": workflow["reasoning_output_tokens"],
        "actual_multi_agent_total_tokens": workflow["total_tokens"],
        "image_file_input_tokens": "",
        "image_file_input_note": "not separately exposed; included in input_tokens",
        "token_usage_basis": token_basis,
        "main_model_calls": main_summary["model_calls"],
        "main_input_tokens": main_summary["input_tokens"],
        "main_cached_input_tokens": main_summary["cached_input_tokens"],
        "main_output_tokens": main_summary["output_tokens"],
        "main_reasoning_output_tokens": main_summary["reasoning_output_tokens"],
        "main_total_tokens": main_summary["total_tokens"],
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
        "single_agent_proxy_basis": single_basis,
        "single_agent_round1_proxy_metric_label": "Diego round 1 extraction -- unvalidated proxy",
        "single_agent_low_total_tokens": single_agent["low"],
        "single_agent_expected_total_tokens": single_agent["expected"],
        "single_agent_high_total_tokens": single_agent["high"],
        "single_agent_estimate_basis": single_basis,
        "single_agent_expected_token_savings_vs_multi_agent": workflow["total_tokens"] - single_agent["expected"],
        "single_agent_expected_token_savings_pct_vs_multi_agent": (
            (workflow["total_tokens"] - single_agent["expected"]) / workflow["total_tokens"]
            if workflow["total_tokens"]
            else ""
        ),
        "multi_agent_vs_single_agent_expected_token_ratio": (
            workflow["total_tokens"] / single_agent["expected"] if single_agent["expected"] else ""
        ),
        "extra_multi_agent_tokens_vs_single_agent_expected": workflow["total_tokens"] - single_agent["expected"],
        "data_limitations": (
            "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank "
            "until an after-the-fact validation CSV is available. Image/file input tokens are not separately "
            "exposed in the Codex logs."
        ),
        "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
        "completed_subagent_model_calls": subagents["model_calls"],
        "completed_subagent_input_tokens": subagents["input_tokens"],
        "completed_subagent_cached_input_tokens": subagents["cached_input_tokens"],
        "completed_subagent_output_tokens": subagents["output_tokens"],
        "completed_subagent_reasoning_output_tokens": subagents["reasoning_output_tokens"],
        "completed_subagent_total_tokens": subagents["total_tokens"],
        "main_low_estimate_tokens": main_summary["total_tokens"],
        "main_expected_estimate_tokens": main_summary["total_tokens"],
        "main_high_estimate_tokens": main_summary["total_tokens"],
        "workflow_low_estimate_total_tokens": workflow["total_tokens"],
        "workflow_expected_estimate_total_tokens": workflow["total_tokens"],
        "workflow_high_estimate_total_tokens": workflow["total_tokens"],
        "token_update_timestamp": update_timestamp,
    }
    write_tracker(payload)
    write_call_csv(call_rows)

    summary = {
        "workflow_label": "Improved doc 14 / Iteration 1",
        "update_timestamp": update_timestamp,
        "main_start_timestamp": main_start,
        "main": main_summary,
        "rounds": round_summaries,
        "diego": diego,
        "jennifer": jennifer,
        "subagents": subagents,
        "workflow": workflow,
        "single_agent": single_agent,
        "final_validation": final_validation,
        "token_usage_basis": token_basis,
        "single_agent_estimate_basis": single_basis,
    }
    (RESULTS_DIR / "token_usage_actual_estimate.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    append_notes(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
