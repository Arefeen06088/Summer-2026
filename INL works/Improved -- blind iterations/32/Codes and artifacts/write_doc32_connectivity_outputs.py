import csv
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\32")
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"
INPUT_DIR = DOC_ROOT / "Input resources"
TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"
SESSION_ROOT = Path(r"C:\Users\AREFA\.codex\sessions")

DIEGO_AGENT_IDS = [
    "019f5c05-395c-7ec3-8f4d-7e0717abc107",
]
JENNIFER_AGENT_IDS = [
    "019f5c14-7782-7df1-a8cf-b81c4dc7814d",
]
DOC_NUMBER = "32"
WORKFLOW_LABEL = "Improved doc 32 / Iteration 1"


def read_dicts(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def inventory_labels():
    rows = read_dicts(INPUT_DIR / "component_visual_ocr_labels.csv")
    return {row["normalized_label"].strip() for row in rows if row.get("normalized_label", "").strip()}


def read_matrix(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    labels = [value.strip() for value in rows[0][1:]]
    body = []
    for row in rows[1:]:
        body.append((row[0].strip(), [str(value).strip() for value in row[1:]]))
    return labels, body


def matrix_edges(labels, body):
    edges = []
    for i, (row_label, values) in enumerate(body):
        for j, value in enumerate(values):
            if j > i and value == "1":
                edges.append(
                    {
                        "node_a": row_label,
                        "node_b": labels[j],
                        "edge_type": "accepted",
                        "source": "final_matrix",
                    }
                )
    return edges


def validate_matrix(labels, body):
    errors = []
    row_labels = [row_label for row_label, _ in body]
    if row_labels != labels:
        errors.append("row labels do not match column labels")
    if len(set(labels)) != len(labels):
        errors.append("duplicate node labels present")
    edge_count = 0
    isolated = []
    for i, (row_label, values) in enumerate(body):
        degree = sum(1 for value in values if value == "1")
        if degree == 0:
            isolated.append(row_label)
        if len(values) != len(labels):
            errors.append(f"row width mismatch for {row_label}")
            continue
        if values[i] != "0":
            errors.append(f"non-zero diagonal for {row_label}")
        for j, value in enumerate(values):
            if value not in {"0", "1"}:
                errors.append(f"bad matrix value at {row_label},{labels[j]}: {value}")
            if j > i and value == "1":
                edge_count += 1
            if j < len(body) and value != body[j][1][i]:
                errors.append(f"asymmetry at {row_label},{labels[j]}")
    inv = inventory_labels()
    retained = set(labels) & inv
    return {
        "node_count": len(labels),
        "unique_node_count": len(set(labels)),
        "edge_count": edge_count,
        "symmetric": not any(error.startswith("asymmetry") for error in errors),
        "diagonal_zero": not any(error.startswith("non-zero diagonal") for error in errors),
        "row_column_labels_identical": row_labels == labels,
        "validation_errors": errors,
        "isolated_nodes": isolated,
        "isolated_node_count": len(isolated),
        "inventory_component_count": len(inv),
        "inventory_component_retained_count": len(retained),
        "missing_inventory_components": sorted(inv - set(labels)),
    }


def write_nodes(path, labels):
    inv = inventory_labels()
    fields = ["node_name", "node_class", "subtype", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for label in labels:
            if label in inv:
                node_class = "inventory_component"
            elif label.startswith("BUS-") or label.startswith("BB-"):
                node_class = "visual_logical_bus"
            elif label.startswith("GND-"):
                node_class = "visual_ground"
            else:
                node_class = "visual_logical_node"
            writer.writerow(
                {
                    "node_name": label,
                    "node_class": node_class,
                    "subtype": "",
                    "evidence": "retained in saturated final matrix from Diego/Jennifer visual review",
                }
            )


def write_edges(path, edges):
    fields = ["node_a", "node_b", "edge_type", "source", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "node_a": edge["node_a"],
                    "node_b": edge["node_b"],
                    "edge_type": edge["edge_type"],
                    "source": edge["source"],
                    "evidence": "accepted in saturated final connectivity matrix",
                }
            )


def final_source():
    for prefix in ("round_03_jennifer", "round_03_diego", "round_02_jennifer", "round_02_diego", "round_01_jennifer"):
        path = RESULT_DIR / f"{prefix}_matrix.csv"
        if path.exists():
            return prefix, path
    raise FileNotFoundError("No final round matrix found")


def extract_markdown_table(notes_path, section_heading, output_path):
    if not notes_path.exists():
        return 0
    lines = notes_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    table_lines = []
    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            in_section = section_heading in line
            continue
        if in_section and line.strip().startswith("|"):
            table_lines.append(line.strip())
    if len(table_lines) < 3:
        return 0
    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def find_agent_log(agent_id):
    matches = sorted(
        SESSION_ROOT.rglob(f"rollout-*{agent_id}.jsonl"),
        key=lambda path: path.stat().st_mtime,
    )
    if not matches:
        raise FileNotFoundError(f"No session log found for {agent_id}")
    return matches[-1]


def parse_usage(log_path):
    count = 0
    latest = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }
    with log_path.open(encoding="utf-8") as handle:
        for line in handle:
            if '"type":"token_count"' not in line:
                continue
            payload = json.loads(line)
            usage = payload["payload"]["info"]["total_token_usage"]
            latest = {key: int(usage.get(key, 0)) for key in latest}
            count += 1
    return {"model_calls": count, **latest, "log_path": str(log_path)}


def aggregate_agent_usage(agent_ids):
    usages = [parse_usage(find_agent_log(agent_id)) for agent_id in agent_ids]
    totals = {
        "agent_count": len(agent_ids),
        "model_calls": sum(item["model_calls"] for item in usages),
        "input_tokens": sum(item["input_tokens"] for item in usages),
        "cached_input_tokens": sum(item["cached_input_tokens"] for item in usages),
        "output_tokens": sum(item["output_tokens"] for item in usages),
        "reasoning_output_tokens": sum(item["reasoning_output_tokens"] for item in usages),
        "total_tokens": sum(item["total_tokens"] for item in usages),
        "agent_ids": "; ".join(agent_ids),
        "log_path": "; ".join(item["log_path"] for item in usages),
    }
    return totals


def update_token_tracker(validation):
    if not TRACKER_CSV.exists():
        return None
    diego = aggregate_agent_usage(DIEGO_AGENT_IDS)
    jennifer = aggregate_agent_usage(JENNIFER_AGENT_IDS)
    completed = {
        "model_calls": diego["model_calls"] + jennifer["model_calls"],
        "input_tokens": diego["input_tokens"] + jennifer["input_tokens"],
        "cached_input_tokens": diego["cached_input_tokens"] + jennifer["cached_input_tokens"],
        "output_tokens": diego["output_tokens"] + jennifer["output_tokens"],
        "reasoning_output_tokens": diego["reasoning_output_tokens"] + jennifer["reasoning_output_tokens"],
        "total_tokens": diego["total_tokens"] + jennifer["total_tokens"],
    }
    main_low = 1_250_000
    main_expected = 2_500_000
    main_high = 5_000_000
    workflow_low = completed["total_tokens"] + main_low
    workflow_expected = completed["total_tokens"] + main_expected
    workflow_high = completed["total_tokens"] + main_high

    with TRACKER_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    rows = [
        row
        for row in rows
        if not (
            row.get("family") == "Improved"
            and row.get("document") == DOC_NUMBER
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]
    row = {field: "" for field in fields}
    row.update(
        {
            "family": "Improved",
            "document": DOC_NUMBER,
            "iteration": "1",
            "workflow_label": WORKFLOW_LABEL,
            "record_type": "multi_agent_token_usage_unvalidated_final",
            "metric_label": "Final connectivity -- unvalidated",
            "metric_agent": "Final",
            "metric_round": "final",
            "is_selected_final_metric": "1",
            "final_metric_selection_basis": "final saturated multi-agent extraction; validation metrics pending",
            "validation_note": "No GT or GT-derived validation metric file used during extraction; metrics intentionally blank pending after-the-fact validation.",
            "actual_multi_agent_model_calls": str(completed["model_calls"]),
            "actual_multi_agent_input_tokens": str(completed["input_tokens"]),
            "actual_multi_agent_cached_input_tokens": str(completed["cached_input_tokens"]),
            "actual_multi_agent_output_tokens": str(completed["output_tokens"]),
            "actual_multi_agent_reasoning_output_tokens": str(completed["reasoning_output_tokens"]),
            "actual_multi_agent_total_tokens": str(completed["total_tokens"]),
            "image_file_input_note": "not separately exposed; included in input_tokens",
            "token_usage_basis": "actual completed subagent Codex token_count logs for all Diego/Jennifer round threads; live main-agent orchestration/finalization estimated",
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
            "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available. actual_multi_agent_* columns in this row represent completed subagents only and aggregate all Diego/Jennifer round threads; use workflow_*_estimate_total_tokens for total-turn planning.",
            "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
            "completed_subagent_model_calls": str(completed["model_calls"]),
            "completed_subagent_input_tokens": str(completed["input_tokens"]),
            "completed_subagent_cached_input_tokens": str(completed["cached_input_tokens"]),
            "completed_subagent_output_tokens": str(completed["output_tokens"]),
            "completed_subagent_reasoning_output_tokens": str(completed["reasoning_output_tokens"]),
            "completed_subagent_total_tokens": str(completed["total_tokens"]),
            "main_low_estimate_tokens": str(main_low),
            "main_expected_estimate_tokens": str(main_expected),
            "main_high_estimate_tokens": str(main_high),
            "workflow_low_estimate_total_tokens": str(workflow_low),
            "workflow_expected_estimate_total_tokens": str(workflow_expected),
            "workflow_high_estimate_total_tokens": str(workflow_high),
            "token_update_timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        }
    )
    rows.append(row)
    with TRACKER_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    notes = f"""

## Doc {DOC_NUMBER} Iteration 1 Update - {datetime.now().date().isoformat()}

Added `{WORKFLOW_LABEL}` as `record_type=multi_agent_token_usage_unvalidated_final`.

Token status:
- Diego actual completed usage across {diego['agent_count']} thread(s): {diego['model_calls']} calls, {diego['total_tokens']:,} total tokens.
- Jennifer actual completed usage across {jennifer['agent_count']} thread(s): {jennifer['model_calls']} calls, {jennifer['total_tokens']:,} total tokens.
- Completed subagent total: {completed['model_calls']} calls, {completed['total_tokens']:,} total tokens.
- Main-agent live orchestration/finalization is estimated as low/expected/high = {main_low:,} / {main_expected:,} / {main_high:,} tokens.
- Workflow low/expected/high total estimate = {workflow_low:,} / {workflow_expected:,} / {workflow_high:,} tokens.

Extraction status:
- Final output stored at `{RESULT_DIR}`.
- Saturated final matrix has {validation['node_count']} nodes and {validation['edge_count']} visually supported unique edges.
- No validation metrics were used during extraction.
- FP/FN/precision/recall/F1 are blank for doc {DOC_NUMBER} until an after-the-fact validation metrics CSV is available.
"""
    if TRACKER_NOTES.exists():
        existing_notes = TRACKER_NOTES.read_text(encoding="utf-8")
        existing_notes = re.sub(
            rf"\n## Doc {DOC_NUMBER} Iteration 1 Update - .*?(?=\n## Doc |\Z)",
            "\n",
            existing_notes,
            flags=re.S,
        ).rstrip()
    else:
        existing_notes = ""
    TRACKER_NOTES.write_text(existing_notes + notes, encoding="utf-8")

    return {
        "diego": diego,
        "jennifer": jennifer,
        "completed": completed,
        "workflow_estimates": {
            "low": workflow_low,
            "expected": workflow_expected,
            "high": workflow_high,
        },
    }


def write_summary(source, validation, uncertain_count, rejected_count):
    text = f"""# Doc {DOC_NUMBER} Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc {DOC_NUMBER} input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `{source}`
- Final nodes: {validation['node_count']}
- Final unique undirected edges: {validation['edge_count']}
- Final uncertain/not accepted candidates: {uncertain_count}
- Rejected/removed candidates documented: {rejected_count}
- Matrix symmetry: {validation['symmetric']}
- Diagonal zero: {validation['diagonal_zero']}
- Inventory component labels retained: {validation['inventory_component_retained_count']} of {validation['inventory_component_count']}
- Isolated nodes: {', '.join(validation['isolated_nodes']) if validation['isolated_nodes'] else 'none'}

## Final Node Policy

- Kept detected component labels from the doc {DOC_NUMBER} inventory when visually supported by the raw schematic.
- Added visually labeled process headers, off-page connectors, and extra visible components retained by the final reviewers.
- Excluded anonymous `WN-*` wire-node points, unlabeled elbows/intersections, continuation bubbles, and line-number-only annotations.

## Final Edge Policy

- Accepted visually supported solid process-piping adjacencies, named header/off-page connector adjacencies, and local direct dashed/signal endpoint pairs retained by both reviewers.
- Long process/sample/utility headers are represented through adjacent components and explicit named header nodes, without clique-expanding every object on the same drawn line.
- Ambiguous routed control channels, panel/JB/DCS/PLC bundles, and dashed lines without clear endpoint termination remain outside the final matrix.

## Round Trail

- `round_01_diego_matrix.csv`: Diego high-recall proposal.
- `round_01_jennifer_matrix.csv`: Jennifer precision-refined proposal.
- `round_02_diego_matrix.csv`: Diego saturation agreement/review.
- `round_02_jennifer_matrix.csv`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
"""
    (RESULT_DIR / "final_connectivity_summary.md").write_text(text, encoding="utf-8")


def main():
    source, source_path = final_source()
    labels, body = read_matrix(source_path)
    validation = validate_matrix(labels, body)
    if validation["validation_errors"]:
        raise ValueError(json.dumps(validation, indent=2))

    shutil.copyfile(source_path, RESULT_DIR / "final_connectivity_matrix.csv")
    shutil.copyfile(source_path, RESULT_DIR / "connectivity_matrix.csv")

    edges = matrix_edges(labels, body)
    write_nodes(RESULT_DIR / "final_connectivity_nodes.csv", labels)
    write_edges(RESULT_DIR / "final_connectivity_edges.csv", edges)
    write_edges(RESULT_DIR / "final_edges.csv", edges)

    with (RESULT_DIR / "final_connectivity_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(validation, handle, indent=2)

    notes_path = RESULT_DIR / f"{source}_notes.md"
    uncertain_count = extract_markdown_table(
        notes_path, "Uncertain / Plausible", RESULT_DIR / "final_uncertain_candidates.csv"
    )
    if uncertain_count == 0 and (RESULT_DIR / "round_01_jennifer_notes.md").exists():
        uncertain_count = extract_markdown_table(
            RESULT_DIR / "round_01_jennifer_notes.md",
            "Uncertain / Plausible",
            RESULT_DIR / "final_uncertain_candidates.csv",
        )
    rejected_count = extract_markdown_table(
        notes_path, "Removed / Rejected", RESULT_DIR / "final_rejected_candidates.csv"
    )
    if rejected_count == 0 and (RESULT_DIR / "round_01_jennifer_notes.md").exists():
        rejected_count = extract_markdown_table(
            RESULT_DIR / "round_01_jennifer_notes.md",
            "Removed / Rejected",
            RESULT_DIR / "final_rejected_candidates.csv",
        )
    write_summary(source, validation, uncertain_count, rejected_count)
    token_status = update_token_tracker(validation)

    print(
        json.dumps(
            {
                "final_source": source,
                "final_validation": validation,
                "final_uncertain_count": uncertain_count,
                "final_rejected_count": rejected_count,
                "token_status": token_status,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
