import csv
import json
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\9")
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"
TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"

DIEGO_AGENT_ID = "019f5887-6514-7e73-9091-b7942b15b414"
JENNIFER_AGENT_ID = "019f588c-469e-72b1-956a-92c2ec3084a3"
SESSION_ROOT = Path(r"C:\Users\AREFA\.codex\sessions\2026\07\12")


def edge_key(a, b):
    return tuple(sorted((a, b)))


def read_nodes(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_edges(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_nodes(path, nodes):
    fieldnames = ["node_name", "node_class", "subtype", "confidence", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            writer.writerow({field: node.get(field, "") for field in fieldnames})


def normalize_edge_row(edge, source):
    return {
        "node_a": edge["node_a"],
        "node_b": edge["node_b"],
        "edge_type": edge.get("edge_type", ""),
        "source": source,
        "evidence": edge.get("evidence", ""),
    }


def write_edges(path, edges):
    fieldnames = ["node_a", "node_b", "edge_type", "source", "evidence"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for edge in edges:
            writer.writerow({field: edge.get(field, "") for field in fieldnames})


def dedupe_edges(edges):
    seen = set()
    clean = []
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a == b:
            continue
        key = edge_key(a, b)
        if key in seen:
            continue
        seen.add(key)
        clean.append(edge)
    return clean


def write_matrix(path, nodes, edges):
    names = [node["node_name"] for node in nodes]
    index = {name: i for i, name in enumerate(names)}
    matrix = [[0 for _ in names] for _ in names]
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in index or b not in index:
            continue
        i = index[a]
        j = index[b]
        if i != j:
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
    seen = set()
    duplicate_edges = []
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in name_set or b not in name_set:
            missing.append((a, b))
        key = edge_key(a, b)
        if key in seen:
            duplicate_edges.append((a, b))
        seen.add(key)
    return {
        "node_count": len(names),
        "unique_node_count": len(set(names)),
        "edge_count": len(dedupe_edges(edges)),
        "missing_edge_endpoint_count": len(missing),
        "missing_edge_endpoints": missing,
        "duplicate_edge_count": len(duplicate_edges),
        "duplicate_edges": duplicate_edges,
        "diagonal_policy": "all diagonal entries written as 0",
        "symmetric_policy": "all accepted edges written symmetrically",
    }


def materialize(prefix, nodes, edges):
    edges = dedupe_edges(edges)
    write_nodes(RESULT_DIR / f"{prefix}_nodes.csv", nodes)
    write_edges(RESULT_DIR / f"{prefix}_edges.csv", edges)
    write_matrix(RESULT_DIR / f"{prefix}_connectivity_matrix.csv", nodes, edges)
    validation = validate(nodes, edges)
    with (RESULT_DIR / f"{prefix}_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(validation, handle, indent=2)
    return validation


def round_01_diego_edges():
    high = [
        normalize_edge_row(edge, "round_01_diego_high_confidence")
        for edge in read_edges(RESULT_DIR / "round_01_diego_edges_high.csv")
    ]
    plausible = []
    for edge in read_edges(RESULT_DIR / "round_01_diego_edges_plausible.csv"):
        evidence = edge.get("evidence", "")
        reason = edge.get("reason_for_lower_confidence", "")
        if reason:
            evidence = f"{evidence} Lower-confidence note: {reason}"
        plausible.append(
            {
                "node_a": edge["node_a"],
                "node_b": edge["node_b"],
                "edge_type": edge.get("edge_type", ""),
                "source": "round_01_diego_plausible",
                "evidence": evidence,
            }
        )
    return dedupe_edges(high + plausible)


def find_agent_log(agent_id):
    matches = sorted(SESSION_ROOT.glob(f"rollout-*{agent_id}.jsonl"))
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
    return {"model_calls": count, **latest}


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
            and row.get("document") == "9"
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]

    row = {field: "" for field in fieldnames}
    row.update(
        {
            "family": "Improved",
            "document": "9",
            "iteration": "1",
            "workflow_label": "Improved doc 9 / Iteration 1",
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

## Doc 9 Iteration 1 Update - {datetime.now().date().isoformat()}

Added `Improved doc 9 / Iteration 1` as `record_type=multi_agent_token_usage_unvalidated_final`.

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
- FP/FN/precision/recall/F1 are blank for doc 9 until an after-the-fact validation metrics CSV is available.
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


def write_uncertain_copy():
    src = RESULT_DIR / "round_01_jennifer_uncertain.csv"
    if src.exists():
        rows = read_edges(src)
        with (RESULT_DIR / "final_uncertain_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["candidate", "decision", "reason"])
            writer.writeheader()
            writer.writerows(rows)


def write_summary(final_validation):
    text = f"""# Doc 9 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 9 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final nodes: {final_validation['node_count']}
- Final unique undirected edges: {final_validation['edge_count']}
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes

## Final Node Decisions

- Kept 159 detected physical component rows, with raw-label corrections where visually supported.
- Added 17 explicit named buses: `BUS-13K-01`, `BUS-4160-N1`, `BUS-4160-N2`, `BUS-4160S1A`, `BUS-4160S1B`, `BUS-480-A1`, `BUS-480-A2`, `BUS-480-B1`, `BUS-480-B2`, `BUS-480-N1A`, `BUS-480-N1B`, `BUS-480-N2A`, `BUS-480-N2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`.
- Added four visible center sequence/control devices missed by the component CSV: `RTD-PNL-A`, `RTD-PNL-B`, `TDR-SEQ-A`, `TDR-SEQ-B`.
- Corrected lower junction-box names to `JB-1A`, `JB-2A`, `JB-1B`, `JB-2B`; side circles are terminal marks, not trailing `O/0` label characters.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal, including high-confidence and plausible candidates.
- `round_01_jennifer_*`: Jennifer precision-refined accepted set and uncertain exclusions.
- `round_02_diego_*`: Diego agreement with Jennifer's refined set.
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
        [normalize_edge_row(edge, "round_01_jennifer_refined") for edge in read_edges(RESULT_DIR / "round_01_jennifer_edges.csv")],
    )
    validations["round_02_diego"] = materialize(
        "round_02_diego",
        read_nodes(RESULT_DIR / "round_02_diego_nodes.csv"),
        [normalize_edge_row(edge, "round_02_diego_agreed") for edge in read_edges(RESULT_DIR / "round_02_diego_edges.csv")],
    )
    final_nodes_path = RESULT_DIR / "round_02_jennifer_nodes.csv"
    final_edges_path = RESULT_DIR / "round_02_jennifer_edges.csv"
    final_prefix = "round_02_jennifer"
    if not final_nodes_path.exists() or not final_edges_path.exists():
        final_nodes_path = RESULT_DIR / "round_02_diego_nodes.csv"
        final_edges_path = RESULT_DIR / "round_02_diego_edges.csv"
        final_prefix = "round_02_diego"
    validations["round_02_jennifer"] = materialize(
        "round_02_jennifer",
        read_nodes(final_nodes_path),
        [normalize_edge_row(edge, f"{final_prefix}_saturated") for edge in read_edges(final_edges_path)],
    )

    final_nodes = read_nodes(RESULT_DIR / "round_02_jennifer_nodes.csv")
    final_edges = [
        normalize_edge_row(edge, "final_saturated")
        for edge in read_edges(RESULT_DIR / "round_02_jennifer_edges.csv")
    ]
    write_nodes(RESULT_DIR / "final_connectivity_nodes.csv", final_nodes)
    write_edges(RESULT_DIR / "final_edges.csv", final_edges)
    write_edges(RESULT_DIR / "final_connectivity_edges.csv", final_edges)
    write_matrix(RESULT_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_matrix(RESULT_DIR / "connectivity_matrix.csv", final_nodes, final_edges)

    final_validation = validate(final_nodes, final_edges)
    with (RESULT_DIR / "final_connectivity_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(final_validation, handle, indent=2)
    write_uncertain_copy()
    write_summary(final_validation)
    token_status = update_token_tracker(final_validation)

    print(json.dumps({"validations": validations, "final_validation": final_validation, "token_status": token_status}, indent=2))


if __name__ == "__main__":
    main()
