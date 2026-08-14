import csv
import json
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\13")
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"
INPUT_DIR = DOC_ROOT / "Input resources"
TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"

DIEGO_AGENT_ID = "019f5944-8b57-7192-b0e6-fe6ef2eba53b"
JENNIFER_AGENT_ID = "019f594e-d8b5-7410-8cd7-6b3c80e80431"
SESSION_ROOT = Path(r"C:\Users\AREFA\.codex\sessions")


def edge_key(a, b):
    return tuple(sorted((a, b)))


def read_dicts(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_inventory_labels():
    rows = read_dicts(INPUT_DIR / "component_visual_ocr_labels.csv")
    return {row["normalized_label"].strip() for row in rows if row.get("normalized_label", "").strip()}


def normalize_node(row):
    name = (row.get("node") or row.get("node_name") or "").strip()
    return {
        "node_name": name,
        "node_class": (row.get("kind") or row.get("node_class") or "").strip(),
        "subtype": (row.get("type") or row.get("subtype") or "").strip(),
        "evidence": (row.get("evidence") or "").strip(),
    }


def read_nodes(path):
    nodes = [normalize_node(row) for row in read_dicts(path)]
    return [node for node in nodes if node["node_name"]]


def normalize_edge(row, source_label):
    a = (row.get("source") or row.get("node_a") or row.get("node1") or "").strip()
    b = (row.get("target") or row.get("node_b") or row.get("node2") or "").strip()
    evidence = (row.get("evidence") or "").strip()
    reason = (row.get("uncertainty_reason") or row.get("reason_for_lower_confidence") or "").strip()
    if reason:
        evidence = f"{evidence} Uncertainty: {reason}".strip()
    return {
        "node_a": a,
        "node_b": b,
        "edge_type": (row.get("edge_type") or "").strip(),
        "source": source_label,
        "evidence": evidence,
    }


def read_edges(path, source_label):
    return [normalize_edge(row, source_label) for row in read_dicts(path)]


def dedupe_edges(edges):
    seen = set()
    clean = []
    for edge in edges:
        a = edge["node_a"].strip()
        b = edge["node_b"].strip()
        if not a or not b or a == b:
            continue
        key = edge_key(a, b)
        if key in seen:
            continue
        seen.add(key)
        copy = dict(edge)
        copy["node_a"] = a
        copy["node_b"] = b
        clean.append(copy)
    return clean


def write_nodes(path, nodes):
    fieldnames = ["node_name", "node_class", "subtype", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            writer.writerow({field: node.get(field, "") for field in fieldnames})


def write_edges(path, edges):
    fieldnames = ["node_a", "node_b", "edge_type", "source", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for edge in edges:
            writer.writerow({field: edge.get(field, "") for field in fieldnames})


def write_matrix(path, nodes, edges):
    names = [node["node_name"] for node in nodes]
    index = {name: idx for idx, name in enumerate(names)}
    matrix = [[0 for _ in names] for _ in names]
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in index or b not in index or a == b:
            continue
        i = index[a]
        j = index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + names)
        for name, row in zip(names, matrix):
            writer.writerow([name] + row)


def validate(nodes, edges):
    names = [node["node_name"] for node in nodes]
    name_set = set(names)
    missing = []
    duplicate_edges = []
    self_loops = []
    seen = set()
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a == b:
            self_loops.append((a, b))
        if a not in name_set or b not in name_set:
            missing.append((a, b))
        key = edge_key(a, b)
        if key in seen:
            duplicate_edges.append((a, b))
        seen.add(key)

    inventory = read_inventory_labels()
    retained = name_set & inventory
    missing_inventory = sorted(inventory - name_set)
    return {
        "node_count": len(names),
        "unique_node_count": len(set(names)),
        "edge_count": len(dedupe_edges(edges)),
        "missing_edge_endpoint_count": len(missing),
        "missing_edge_endpoints": missing,
        "duplicate_edge_count": len(duplicate_edges),
        "duplicate_edges": duplicate_edges,
        "self_loop_count": len(self_loops),
        "self_loops": self_loops,
        "inventory_component_count": len(inventory),
        "inventory_component_retained_count": len(retained),
        "missing_inventory_components": missing_inventory,
        "diagonal_policy": "all diagonal entries written as 0",
        "symmetric_policy": "all accepted edges written symmetrically",
    }


def materialize(prefix, nodes, edges):
    clean_edges = dedupe_edges(edges)
    write_matrix(RESULT_DIR / f"{prefix}_connectivity_matrix.csv", nodes, clean_edges)
    validation = validate(nodes, clean_edges)
    with (RESULT_DIR / f"{prefix}_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(validation, handle, indent=2)
    return validation


def round_01_diego_edges():
    high = read_edges(RESULT_DIR / "round_01_diego_edges_high.csv", "round_01_diego_high_confidence")
    plausible = read_edges(RESULT_DIR / "round_01_diego_edges_plausible.csv", "round_01_diego_plausible")
    return dedupe_edges(high + plausible)


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


def update_token_tracker(final_validation):
    if not TRACKER_CSV.exists():
        return None

    diego = parse_usage(find_agent_log(DIEGO_AGENT_ID))
    jennifer = parse_usage(find_agent_log(JENNIFER_AGENT_ID))
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
        fieldnames = list(rows[0].keys()) if rows else []

    rows = [
        row
        for row in rows
        if not (
            row.get("family") == "Improved"
            and row.get("document") == "13"
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]

    row = {field: "" for field in fieldnames}
    row.update(
        {
            "family": "Improved",
            "document": "13",
            "iteration": "1",
            "workflow_label": "Improved doc 13 / Iteration 1",
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
            "token_usage_basis": "actual completed subagent Codex token_count logs; live main-agent orchestration/finalization estimated",
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
            "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available. actual_multi_agent_* columns in this row represent completed subagents only; use workflow_*_estimate_total_tokens for total-turn planning.",
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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    notes = f"""

## Doc 13 Iteration 1 Update - {datetime.now().date().isoformat()}

Added `Improved doc 13 / Iteration 1` as `record_type=multi_agent_token_usage_unvalidated_final`.

Token status:
- Diego actual completed usage: {diego['model_calls']} calls, {diego['total_tokens']:,} total tokens.
- Jennifer actual completed usage: {jennifer['model_calls']} calls, {jennifer['total_tokens']:,} total tokens.
- Completed subagent total: {completed['model_calls']} calls, {completed['total_tokens']:,} total tokens.
- Main-agent live orchestration/finalization is estimated as low/expected/high = {main_low:,} / {main_expected:,} / {main_high:,} tokens.
- Workflow low/expected/high total estimate = {workflow_low:,} / {workflow_expected:,} / {workflow_high:,} tokens.

Extraction status:
- Final output stored at `{RESULT_DIR}`.
- Saturated final matrix has {final_validation['node_count']} nodes and {final_validation['edge_count']} visually supported unique edges.
- No validation metrics were used during extraction.
- FP/FN/precision/recall/F1 are blank for doc 13 until an after-the-fact validation metrics CSV is available.
"""
    with TRACKER_NOTES.open("a", encoding="utf-8") as handle:
        handle.write(notes)

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


def copy_uncertain(final_source):
    uncertain_name = f"{final_source}_uncertain.csv"
    source = RESULT_DIR / uncertain_name
    if not source.exists():
        return 0
    rows = read_dicts(source)
    fieldnames = ["source", "target", "evidence", "uncertainty_reason"]
    with (RESULT_DIR / "final_uncertain_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return len(rows)


def write_summary(final_validation, final_source, uncertain_count):
    text = f"""# Doc 13 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 13 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `{final_source}`
- Final nodes: {final_validation['node_count']}
- Final unique undirected edges: {final_validation['edge_count']}
- Final uncertain/not accepted candidates: {uncertain_count}
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes
- Inventory component labels retained: {final_validation['inventory_component_retained_count']} of {final_validation['inventory_component_count']}

## Final Node Decisions

- Kept all 178 detected component-inventory labels.
- Added visually labeled `SWYD-230` from the raw top-left 230 kV source chain.
- Added named logical buses `BUS-4A`, `BUS-4B`, `BUS-4C`, `BUS-4D`, `DC-BUS-A`, `DC-BUS-B`, `DC-BUS-C`, and `DC-BUS-D`.
- Kept `LC-480A` through `LC-480D`, `MCC-A1` through `MCC-D2`, and `GND-A` through `GND-PLANT` as named bus/ground-like component nodes.
- Kept `LOCAL-IO-A` through `LOCAL-IO-D` as drawn named terminal endpoints on the 480 V load-center buses.
- Removed floating annotation nodes for EDG auto-start, ESFAS permissive notes, unit-generator-aux-feed text, and off-sheet continuation labels.

## Final Edge Policy

- Accepted direct solid-line power/DC/ground connections, bus ties, load-center taps, MCC branch feeders, disconnect-to-load branches, and charger-to-DC/inverter/UPS chains.
- Represented batteries through their visible charger connection: `BAT-125* -> CHG-125* -> DC-BUS-*`.
- Left relay-to-breaker dashed control/trip associations uncertain rather than accepted.
- Left cross-routing, charger AC input, JB-to-DC, UPS-to-local-I/O, and off-sheet continuation candidates uncertain unless a clean visible endpoint and junction were present.
- Excluded anonymous wire-node points.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal with high and plausible candidates.
- `round_01_jennifer_*`: Jennifer precision-refined accepted set and uncertainty list.
- `round_02_diego_*`: Diego saturation pass, agreeing with Jennifer and pruning isolated off-sheet annotations.
- `round_02_jennifer_*`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
"""
    (RESULT_DIR / "final_connectivity_summary.md").write_text(text, encoding="utf-8")


def final_source():
    for prefix in ("round_02_jennifer", "round_02_diego", "round_01_jennifer"):
        if (RESULT_DIR / f"{prefix}_nodes.csv").exists() and (RESULT_DIR / f"{prefix}_edges.csv").exists():
            return prefix
    raise FileNotFoundError("No refined final source found")


def main():
    validations = {}
    validations["round_01_diego"] = materialize(
        "round_01_diego",
        read_nodes(RESULT_DIR / "round_01_diego_nodes.csv"),
        round_01_diego_edges(),
    )
    validations["round_01_jennifer"] = materialize(
        "round_01_jennifer",
        read_nodes(RESULT_DIR / "round_01_jennifer_nodes.csv"),
        read_edges(RESULT_DIR / "round_01_jennifer_edges.csv", "round_01_jennifer_refined"),
    )
    for prefix, label in (
        ("round_02_diego", "round_02_diego_reviewed"),
        ("round_02_jennifer", "round_02_jennifer_saturated"),
    ):
        nodes_path = RESULT_DIR / f"{prefix}_nodes.csv"
        edges_path = RESULT_DIR / f"{prefix}_edges.csv"
        if nodes_path.exists() and edges_path.exists():
            validations[prefix] = materialize(
                prefix,
                read_nodes(nodes_path),
                read_edges(edges_path, label),
            )

    source = final_source()
    final_nodes = read_nodes(RESULT_DIR / f"{source}_nodes.csv")
    final_edges = dedupe_edges(read_edges(RESULT_DIR / f"{source}_edges.csv", f"{source}_final"))

    write_nodes(RESULT_DIR / "final_connectivity_nodes.csv", final_nodes)
    write_edges(RESULT_DIR / "final_edges.csv", final_edges)
    write_edges(RESULT_DIR / "final_connectivity_edges.csv", final_edges)
    write_matrix(RESULT_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_matrix(RESULT_DIR / "connectivity_matrix.csv", final_nodes, final_edges)

    final_validation = validate(final_nodes, final_edges)
    with (RESULT_DIR / "final_connectivity_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(final_validation, handle, indent=2)
    uncertain_count = copy_uncertain(source)
    write_summary(final_validation, source, uncertain_count)
    token_status = update_token_tracker(final_validation)

    print(
        json.dumps(
            {
                "validations": validations,
                "final_source": source,
                "final_validation": final_validation,
                "final_uncertain_count": uncertain_count,
                "token_status": token_status,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
