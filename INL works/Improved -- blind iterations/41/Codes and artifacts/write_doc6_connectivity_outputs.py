import csv
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\6")
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
    "019f8f94-2c1e-78f0-bc0c-68f53a1bf2b0",
    "019f8f9e-112c-7f31-879c-81d6cf1b8e54",
]
JENNIFER_AGENT_IDS = [
    "019f8f9a-2871-7832-a408-a5c65d2b4cd9",
    "019f8fa1-1984-7310-94bb-30b40a49a692",
]
FAMILY = "Simplers"
DOC_NUMBER = "6"
ITERATION = "1"
WORKFLOW_LABEL = "Simplers doc 6 / Iteration 1"


def load_inventory():
    path = INPUT_DIR / "component_visual_ocr_labels.csv"
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    inventory = {}
    for row in rows:
        label = row.get("normalized_label") or row.get("final_label")
        inventory[label] = row
    return inventory


def read_matrix(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    labels = rows[0][1:]
    body = []
    for row in rows[1:]:
        body.append([row[0]] + [int(value) for value in row[1:]])
    return labels, body


def validate_matrix(labels, body):
    errors = []
    if len(labels) != len(set(labels)):
        errors.append("duplicate labels")
    if len(body) != len(labels):
        errors.append("row count does not match header")
    row_labels = [row[0] for row in body]
    if row_labels != labels:
        errors.append("row labels differ from column labels")
    matrix = [row[1:] for row in body]
    diagonal_zero = True
    symmetric = True
    for i, row in enumerate(matrix):
        if len(row) != len(labels):
            errors.append(f"row {i} length mismatch")
            continue
        if row[i] != 0:
            diagonal_zero = False
        for j, value in enumerate(row):
            if value not in (0, 1):
                errors.append(f"non-binary value at {i},{j}")
            if j < len(matrix) and i < len(matrix[j]) and value != matrix[j][i]:
                symmetric = False
    if not diagonal_zero:
        errors.append("diagonal not zero")
    if not symmetric:
        errors.append("matrix not symmetric")
    degrees = {labels[i]: sum(matrix[i]) for i in range(len(labels))}
    inventory = load_inventory()
    missing_inventory = [label for label in inventory if label not in labels]
    return {
        "node_count": len(labels),
        "unique_node_count": len(set(labels)),
        "edge_count": sum(sum(row) for row in matrix) // 2,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "row_column_labels_identical": row_labels == labels,
        "validation_errors": errors,
        "isolated_nodes": [label for label, degree in degrees.items() if degree == 0],
        "isolated_node_count": sum(1 for degree in degrees.values() if degree == 0),
        "inventory_label_count": len(inventory),
        "inventory_label_retained_count": sum(1 for label in inventory if label in labels),
        "missing_inventory_labels": missing_inventory,
    }


def matrix_edges(labels, body):
    matrix = [row[1:] for row in body]
    edges = []
    for i, label_a in enumerate(labels):
        for j in range(i + 1, len(labels)):
            if matrix[i][j] == 1:
                edges.append(
                    {
                        "node_a": label_a,
                        "node_b": labels[j],
                        "edge_type": "accepted",
                        "source": "final_matrix",
                    }
                )
    return edges


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_a", "node_b", "edge_type", "source", "evidence"])
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


def node_class_for(label, inventory):
    if label in inventory:
        node_kind = inventory[label].get("node_kind", "")
        component_type = inventory[label].get("component_type", "")
        if component_type in {"bus", "dc_bus", "ups_bus"} or label.startswith(("BUS-", "DC-BUS", "UPS-BUS")):
            return "visual_logical_bus", component_type
        if node_kind:
            return node_kind, component_type
        return "inventory_label", component_type
    if label.startswith("GND-"):
        return "visual_ground", ""
    if label.startswith(("BUS-", "DC-BUS", "UPS-BUS")):
        return "visual_logical_bus", ""
    return "visual_logical_node", ""


def write_nodes(path, labels):
    inventory = load_inventory()
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_label", "node_class", "subtype", "evidence"])
        writer.writeheader()
        for label in labels:
            node_class, subtype = node_class_for(label, inventory)
            writer.writerow(
                {
                    "node_label": label,
                    "node_class": node_class,
                    "subtype": subtype,
                    "evidence": "retained in saturated Diego/Jennifer visual review",
                }
            )


def final_source():
    for prefix in ("round_03_jennifer", "round_03_diego", "round_02_jennifer", "round_02_diego", "round_01_jennifer"):
        path = RESULT_DIR / f"{prefix}_matrix.csv"
        if path.exists():
            return prefix, path
    raise FileNotFoundError("No final round matrix found")


def extract_section_items(notes_path, section_heading, output_path):
    if not notes_path.exists():
        return 0
    lines = notes_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    table_lines = []
    section_lines = []
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
        if not item.startswith("- "):
            continue
        item = item[2:].strip()
        source = ""
        target = ""
        note = item
        match = re.match(r"`?([^`:]+?)`?\s+--\s+`?([^`:]+?)`?\s*:\s*(.*)", item)
        if match:
            source = match.group(1).strip()
            target = match.group(2).strip()
            note = match.group(3).strip()
        rows.append({"source": source, "target": target, "item": item, "note": note})
    if not rows:
        return 0
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "item", "note"])
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


def agent_usage(agent_id):
    path = find_agent_log(agent_id)
    latest = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }
    count = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if '"type":"token_count"' not in line:
                continue
            payload = json.loads(line)
            usage = payload["payload"]["info"]["total_token_usage"]
            latest = {key: int(usage.get(key, 0)) for key in latest}
            count += 1
    latest["model_calls"] = count
    latest["log_path"] = str(path)
    return latest


def aggregate_usage(agent_ids):
    usages = [agent_usage(agent_id) for agent_id in agent_ids]
    return {
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


def update_token_tracker(validation):
    if not TRACKER_CSV.exists():
        return None
    diego = aggregate_usage(DIEGO_AGENT_IDS)
    jennifer = aggregate_usage(JENNIFER_AGENT_IDS)
    completed = {
        "model_calls": diego["model_calls"] + jennifer["model_calls"],
        "input_tokens": diego["input_tokens"] + jennifer["input_tokens"],
        "cached_input_tokens": diego["cached_input_tokens"] + jennifer["cached_input_tokens"],
        "output_tokens": diego["output_tokens"] + jennifer["output_tokens"],
        "reasoning_output_tokens": diego["reasoning_output_tokens"] + jennifer["reasoning_output_tokens"],
        "total_tokens": diego["total_tokens"] + jennifer["total_tokens"],
    }
    main_low = 1_000_000
    main_expected = 2_000_000
    main_high = 4_000_000
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
            row.get("family") == FAMILY
            and row.get("document") == DOC_NUMBER
            and row.get("iteration") == ITERATION
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]
    row = {field: "" for field in fields}
    row.update(
        {
            "family": FAMILY,
            "document": DOC_NUMBER,
            "iteration": ITERATION,
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
            "token_usage_basis": "actual completed subagent token_count logs plus main-agent estimate",
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
            "performance_status": "unvalidated_final_pending_metrics",
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
            "token_update_timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        }
    )
    rows.append(row)
    with TRACKER_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    notes = f"""
## Doc {DOC_NUMBER} Iteration {ITERATION} Update - {datetime.now().date().isoformat()}

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
    existing = TRACKER_NOTES.read_text(encoding="utf-8") if TRACKER_NOTES.exists() else ""
    existing = re.sub(
        rf"\n## Doc {DOC_NUMBER} Iteration {ITERATION} Update - .*?(?=\n## Doc |\Z)",
        "",
        existing,
        flags=re.S,
    )
    TRACKER_NOTES.write_text(existing + notes, encoding="utf-8")
    return {"diego": diego, "jennifer": jennifer, "completed": completed, "workflow_estimates": {"low": workflow_low, "expected": workflow_expected, "high": workflow_high}}


def write_summary(source, validation, uncertain_count, rejected_count):
    text = f"""# Doc {DOC_NUMBER} Iteration {ITERATION} Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc {DOC_NUMBER} input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `{source}`
- Final nodes: {validation['node_count']}
- Final unique undirected edges: {validation['edge_count']}
- Final uncertain/not accepted candidates: {uncertain_count}
- Rejected/removed candidates documented: {rejected_count}
- Matrix symmetry: {validation['symmetric']}
- Diagonal zero: {validation['diagonal_zero']}
- Inventory labels retained: {validation['inventory_label_retained_count']} of {validation['inventory_label_count']}
- Isolated nodes: {', '.join(validation['isolated_nodes']) if validation['isolated_nodes'] else 'none'}

## Final Node Policy

- Kept detected physical components and visually meaningful logical bus/ground nodes when supported by the raw schematic.
- Excluded context-only region boxes if they did not function as electrical nodes.
- Excluded anonymous `WN-*` wire-node points, junction dots, line tags, cable callouts, and drawing annotations.

## Final Edge Policy

- Accepted visually supported solid electrical feeder adjacencies, named busbar taps, transformer/source chains, breaker/load chains, DC/UPS power chains, and direct dashed control endpoints retained by both reviewers.
- Long buses are represented through explicit named bus nodes, without clique-expanding all objects on the same drawn busbar.
- Ambiguous dashed interlocks and boundary continuations without clear endpoint termination remain outside the final matrix.

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
    uncertain_count = extract_section_items(notes_path, "Uncertain / Plausible", RESULT_DIR / "final_uncertain_candidates.csv")
    if uncertain_count == 0 and (RESULT_DIR / "round_01_jennifer_notes.md").exists():
        uncertain_count = extract_section_items(
            RESULT_DIR / "round_01_jennifer_notes.md",
            "Uncertain / Plausible",
            RESULT_DIR / "final_uncertain_candidates.csv",
        )
    rejected_count = extract_section_items(notes_path, "Removed / Rejected", RESULT_DIR / "final_rejected_candidates.csv")
    if rejected_count == 0 and (RESULT_DIR / "round_01_jennifer_notes.md").exists():
        rejected_count = extract_section_items(
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
