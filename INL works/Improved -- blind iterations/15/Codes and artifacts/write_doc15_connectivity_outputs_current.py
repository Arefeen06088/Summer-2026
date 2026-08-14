from __future__ import annotations

import csv
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\15")
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"
SESSION_ROOT = Path(r"C:\Users\AREFA\.codex\sessions")

DOC_NUMBER = "15"
WORKFLOW_LABEL = "Improved doc 15 / Iteration 1"
INVENTORY_CSV = ARTIFACT_DIR / "component_inventory_doc15_current.csv"
FINAL_PREFIX = "current_round_02_jennifer"
DIEGO_AGENT_IDS = ["019f9101-2250-7aa0-8fe2-f97c1fe2aa67"]
JENNIFER_AGENT_IDS = ["019f9107-28aa-7153-ad84-cbe9ad9076e2"]

DEFAULT_FIELDS = [
    "family",
    "document",
    "iteration",
    "workflow_label",
    "record_type",
    "metric_label",
    "metric_agent",
    "metric_round",
    "is_selected_final_metric",
    "final_metric_selection_basis",
    "validation_note",
    "fp",
    "fn",
    "precision",
    "recall",
    "f1",
    "actual_multi_agent_model_calls",
    "actual_multi_agent_input_tokens",
    "actual_multi_agent_cached_input_tokens",
    "actual_multi_agent_output_tokens",
    "actual_multi_agent_reasoning_output_tokens",
    "actual_multi_agent_total_tokens",
    "image_file_input_note",
    "token_usage_basis",
    "diego_model_calls",
    "diego_input_tokens",
    "diego_cached_input_tokens",
    "diego_output_tokens",
    "diego_reasoning_output_tokens",
    "diego_total_tokens",
    "jennifer_model_calls",
    "jennifer_input_tokens",
    "jennifer_cached_input_tokens",
    "jennifer_output_tokens",
    "jennifer_reasoning_output_tokens",
    "jennifer_total_tokens",
    "data_limitations",
    "performance_status",
    "completed_subagent_model_calls",
    "completed_subagent_input_tokens",
    "completed_subagent_cached_input_tokens",
    "completed_subagent_output_tokens",
    "completed_subagent_reasoning_output_tokens",
    "completed_subagent_total_tokens",
    "main_low_estimate_tokens",
    "main_expected_estimate_tokens",
    "main_high_estimate_tokens",
    "workflow_low_estimate_total_tokens",
    "workflow_expected_estimate_total_tokens",
    "workflow_high_estimate_total_tokens",
    "token_update_timestamp",
]


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_matrix(path: Path) -> tuple[list[str], list[tuple[str, list[str]]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise ValueError(f"Empty matrix file: {path}")
    labels = [value.strip() for value in rows[0][1:]]
    body = [(row[0].strip(), [str(value).strip() for value in row[1:]]) for row in rows[1:]]
    return labels, body


def inventory_rows() -> list[dict[str, str]]:
    return read_dicts(INVENTORY_CSV)


def inventory_labels() -> list[str]:
    return [row["node_name"].strip() for row in inventory_rows() if row.get("node_name", "").strip()]


def matrix_edges(labels: list[str], body: list[tuple[str, list[str]]]) -> list[dict[str, str]]:
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


def validate_matrix(labels: list[str], body: list[tuple[str, list[str]]]) -> dict[str, object]:
    errors: list[str] = []
    row_labels = [row_label for row_label, _ in body]
    if row_labels != labels:
        errors.append("row labels do not match column labels")
    if len(set(labels)) != len(labels):
        errors.append("duplicate node labels present")

    edge_count = 0
    isolated = []
    for i, (row_label, values) in enumerate(body):
        if len(values) != len(labels):
            errors.append(f"row width mismatch for {row_label}")
            continue
        degree = sum(1 for value in values if value == "1")
        if degree == 0:
            isolated.append(row_label)
        if i >= len(values) or values[i] != "0":
            errors.append(f"non-zero diagonal for {row_label}")
        for j, value in enumerate(values):
            if value not in {"0", "1"}:
                errors.append(f"bad matrix value at {row_label},{labels[j]}: {value}")
            if j > i and value == "1":
                edge_count += 1
            if j < len(body) and i < len(body[j][1]) and value != body[j][1][i]:
                errors.append(f"asymmetry at {row_label},{labels[j]}")

    inv = inventory_labels()
    inv_set = set(inv)
    label_set = set(labels)
    if labels != inv:
        errors.append("matrix label order does not exactly match current inventory order")
    return {
        "node_count": len(labels),
        "unique_node_count": len(set(labels)),
        "edge_count": edge_count,
        "symmetric": not any(error.startswith("asymmetry") for error in errors),
        "diagonal_zero": not any(error.startswith("non-zero diagonal") for error in errors),
        "row_column_labels_identical": row_labels == labels,
        "inventory_order_exact": labels == inv,
        "validation_errors": errors,
        "isolated_nodes": isolated,
        "isolated_node_count": len(isolated),
        "inventory_node_count": len(inv),
        "inventory_node_retained_count": len(label_set & inv_set),
        "missing_inventory_nodes": sorted(inv_set - label_set),
        "extra_nodes_not_in_inventory": sorted(label_set - inv_set),
    }


def write_nodes(path: Path, labels: list[str]) -> None:
    inv = {row["node_name"]: row for row in inventory_rows()}
    fields = ["node_name", "node_kind", "component_type", "source", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for label in labels:
            row = inv.get(label, {})
            writer.writerow(
                {
                    "node_name": label,
                    "node_kind": row.get("node_kind", ""),
                    "component_type": row.get("component_type", ""),
                    "source": row.get("source", ""),
                    "evidence": "retained in saturated final matrix from Diego/Jennifer visual review",
                }
            )


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
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


def final_source() -> tuple[str, Path]:
    if not FINAL_PREFIX:
        raise ValueError("Set FINAL_PREFIX to the current-run saturated round before finalizing")
    path = RESULT_DIR / f"{FINAL_PREFIX}_matrix.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return FINAL_PREFIX, path


def extract_markdown_table(notes_path: Path, section_heading: str, output_path: Path) -> int:
    if not notes_path.exists():
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["item"])
            writer.writeheader()
        return 0
    lines = notes_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    table_lines: list[str] = []
    section_lines: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            in_section = section_heading in line
            continue
        if in_section:
            section_lines.append(line.rstrip())
            if line.strip().startswith("|"):
                table_lines.append(line.strip())
    if len(table_lines) >= 3:
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
    rows = []
    for line in section_lines:
        item = line.strip()
        if item.startswith("- "):
            rows.append({"item": item[2:].strip()})
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def write_uncertain_from_edges(edge_path: Path, output_path: Path) -> int:
    rows = []
    for edge in read_dicts(edge_path):
        if "uncertain" in edge.get("edge_type", "").lower():
            rows.append(edge)
    fields = ["source", "target", "confidence", "evidence", "edge_type"]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])
    return len(rows)


def write_removed_from_round_delta(final_edge_path: Path, output_path: Path) -> int:
    first_round = RESULT_DIR / "current_round_01_diego_edges.csv"
    if not first_round.exists():
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["source", "target", "reason"])
            writer.writeheader()
        return 0

    def edge_key(row: dict[str, str]) -> tuple[str, str]:
        left = row.get("source", "").strip()
        right = row.get("target", "").strip()
        return tuple(sorted((left, right)))

    final_keys = {edge_key(row) for row in read_dicts(final_edge_path)}
    removed = []
    for row in read_dicts(first_round):
        key = edge_key(row)
        if key not in final_keys:
            removed.append(
                {
                    "source": row.get("source", ""),
                    "target": row.get("target", ""),
                    "confidence": row.get("confidence", ""),
                    "edge_type": row.get("edge_type", ""),
                    "reason": "removed by Jennifer precision review before saturation",
                    "original_evidence": row.get("evidence", ""),
                }
            )
    fields = ["source", "target", "confidence", "edge_type", "reason", "original_evidence"]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(removed)
    return len(removed)


def session_log_for_agent(agent_id: str) -> Path:
    matches = list(SESSION_ROOT.rglob(f"*{agent_id}.jsonl"))
    if not matches:
        raise FileNotFoundError(f"No session log for agent {agent_id}")
    return max(matches, key=lambda path: path.stat().st_mtime)


def parse_usage(log_path: Path) -> dict[str, object]:
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


def aggregate_agent_usage(agent_ids: list[str]) -> dict[str, object]:
    usages = [parse_usage(session_log_for_agent(agent_id)) for agent_id in agent_ids]
    return {
        "agent_count": len(agent_ids),
        "model_calls": sum(int(item["model_calls"]) for item in usages),
        "input_tokens": sum(int(item["input_tokens"]) for item in usages),
        "cached_input_tokens": sum(int(item["cached_input_tokens"]) for item in usages),
        "output_tokens": sum(int(item["output_tokens"]) for item in usages),
        "reasoning_output_tokens": sum(int(item["reasoning_output_tokens"]) for item in usages),
        "total_tokens": sum(int(item["total_tokens"]) for item in usages),
        "agent_ids": "; ".join(agent_ids),
        "log_path": "; ".join(str(item["log_path"]) for item in usages),
    }


def update_token_tracker(validation: dict[str, object]) -> dict[str, object]:
    diego = aggregate_agent_usage(DIEGO_AGENT_IDS)
    jennifer = aggregate_agent_usage(JENNIFER_AGENT_IDS)
    completed = {
        "model_calls": int(diego["model_calls"]) + int(jennifer["model_calls"]),
        "input_tokens": int(diego["input_tokens"]) + int(jennifer["input_tokens"]),
        "cached_input_tokens": int(diego["cached_input_tokens"]) + int(jennifer["cached_input_tokens"]),
        "output_tokens": int(diego["output_tokens"]) + int(jennifer["output_tokens"]),
        "reasoning_output_tokens": int(diego["reasoning_output_tokens"]) + int(jennifer["reasoning_output_tokens"]),
        "total_tokens": int(diego["total_tokens"]) + int(jennifer["total_tokens"]),
    }
    main_low = 1_200_000
    main_expected = 2_400_000
    main_high = 4_800_000
    workflow_low = completed["total_tokens"] + main_low
    workflow_expected = completed["total_tokens"] + main_expected
    workflow_high = completed["total_tokens"] + main_high

    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    if TRACKER_CSV.exists():
        with TRACKER_CSV.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
            fields = list(rows[0].keys()) if rows else DEFAULT_FIELDS[:]
    else:
        rows = []
        fields = DEFAULT_FIELDS[:]
    for field in DEFAULT_FIELDS:
        if field not in fields:
            fields.append(field)
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
            "token_usage_basis": "actual completed subagent Codex token_count logs for Diego/Jennifer current round threads; live main-agent orchestration/finalization estimated",
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
            "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available.",
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
- Diego actual completed usage across {diego['agent_count']} thread(s): {diego['model_calls']} calls, {int(diego['total_tokens']):,} total tokens.
- Jennifer actual completed usage across {jennifer['agent_count']} thread(s): {jennifer['model_calls']} calls, {int(jennifer['total_tokens']):,} total tokens.
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
        existing = TRACKER_NOTES.read_text(encoding="utf-8")
        existing = re.sub(rf"\n## Doc {DOC_NUMBER} Iteration 1 Update - .*?(?=\n## Doc |\Z)", "\n", existing, flags=re.S).rstrip()
    else:
        existing = ""
    TRACKER_NOTES.write_text(existing + notes, encoding="utf-8")
    return {"diego": diego, "jennifer": jennifer, "completed": completed, "workflow_estimates": {"low": workflow_low, "expected": workflow_expected, "high": workflow_high}}


def write_summary(source: str, validation: dict[str, object], uncertain_count: int, rejected_count: int) -> None:
    text = f"""# Doc {DOC_NUMBER} Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only doc {DOC_NUMBER} input resources, generated current inspection artifacts, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `{source}`
- Final nodes: {validation['node_count']}
- Final unique undirected edges: {validation['edge_count']}
- Uncertain candidates left in final notes: {uncertain_count}
- Rejected/removed candidates documented: {rejected_count}
- Matrix symmetry: {validation['symmetric']}
- Diagonal zero: {validation['diagonal_zero']}
- Inventory order exact: {validation['inventory_order_exact']}
- Inventory nodes retained: {validation['inventory_node_retained_count']} of {validation['inventory_node_count']}
- Missing inventory nodes: {', '.join(validation['missing_inventory_nodes']) if validation['missing_inventory_nodes'] else 'none'}
- Extra nodes not in inventory: {', '.join(validation['extra_nodes_not_in_inventory']) if validation['extra_nodes_not_in_inventory'] else 'none'}
- Isolated nodes: {', '.join(validation['isolated_nodes']) if validation['isolated_nodes'] else 'none'}

## Final Node Policy

- Kept physical/OCR components from the input CSV.
- Added four visually named tie-control components and sixteen visually labeled bus nodes from the raw/overlay.
- Excluded `OFFSITE SOURCES`, drawing regions/enclosures, title block, notes, legends, feeder note text, anonymous wire-node points, and pure crossings.

## Final Edge Policy

- Represented visually supported solid power, dashed control/DC, and ground-route connections between named endpoints.
- Connected named components to named buses rather than expanding same-bus cliques.
- Did not add anonymous intermediate wire-node points or collapse through named devices.
"""
    (RESULT_DIR / "final_connectivity_summary.md").write_text(text, encoding="utf-8")


def main() -> None:
    source, matrix_path = final_source()
    labels, body = read_matrix(matrix_path)
    validation = validate_matrix(labels, body)
    if validation["validation_errors"]:
        raise ValueError(json.dumps(validation, indent=2))
    edges = matrix_edges(labels, body)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(matrix_path, RESULT_DIR / "final_connectivity_matrix.csv")
    shutil.copyfile(matrix_path, RESULT_DIR / "connectivity_matrix.csv")
    write_edges(RESULT_DIR / "final_connectivity_edges.csv", edges)
    write_edges(RESULT_DIR / "final_edges.csv", edges)
    write_nodes(RESULT_DIR / "final_connectivity_nodes.csv", labels)
    (RESULT_DIR / "final_connectivity_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    notes_path = RESULT_DIR / f"{source}_notes.md"
    final_edge_source = RESULT_DIR / f"{source}_edges.csv"
    uncertain_count = extract_markdown_table(notes_path, "Uncertain", RESULT_DIR / "final_uncertain_candidates.csv")
    if uncertain_count == 0:
        uncertain_count = write_uncertain_from_edges(final_edge_source, RESULT_DIR / "final_uncertain_candidates.csv")
    rejected_count = extract_markdown_table(notes_path, "Removed", RESULT_DIR / "final_rejected_candidates.csv")
    if rejected_count == 0:
        rejected_count = write_removed_from_round_delta(final_edge_source, RESULT_DIR / "final_rejected_candidates.csv")
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
