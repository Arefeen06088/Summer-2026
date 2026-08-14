from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\40")
ARTIFACTS = BASE / "Codes and artifacts"
RESULTS = BASE / "Results" / "Iteration_1"
TRACKER_DIR = Path(r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples\token_usage_estimate_2026-07-06")
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"

FINAL_PREFIX = "current_round_02_jennifer"
DIEGO_AGENT_IDS = ["019fa423-c011-7dd3-b14e-7716a63e7475"]
JENNIFER_AGENT_IDS = ["019fa44f-e1a2-7712-b143-c9362af5fd4a"]

# Live parent-agent orchestration estimates. Subagent completed usage is pulled from
# local Codex logs when available; these estimates cover unexposed main-agent work.
MAIN_LOW_ESTIMATE = 1_150_000
MAIN_EXPECTED_ESTIMATE = 2_300_000
MAIN_HIGH_ESTIMATE = 4_600_000


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def edge_key(row: dict[str, str]) -> tuple[str, str]:
    a = row["source"].strip()
    b = row["target"].strip()
    return tuple(sorted((a, b)))


def validate_matrix(matrix_path: Path, edges_path: Path) -> dict[str, object]:
    rows = read_csv(matrix_path)
    edges = read_csv(edges_path)
    errors: list[str] = []
    if not rows:
        errors.append("Matrix has no rows.")
        return {"validation_errors": errors}

    headers = list(rows[0].keys())
    if headers[0] != "node_name":
        errors.append("First matrix column is not node_name.")
    nodes = [row["node_name"] for row in rows]
    cols = headers[1:]
    if nodes != cols:
        errors.append("Matrix row names and column names differ or are differently ordered.")
    if len(nodes) != len(set(nodes)):
        errors.append("Matrix node names are not unique.")

    nonzero_pairs: set[tuple[str, str]] = set()
    diag_zero = True
    symmetric = True
    for r, src in enumerate(nodes):
        for c, dst in enumerate(cols):
            value = rows[r].get(dst, "")
            if value not in {"0", "1"}:
                errors.append(f"Non-binary matrix value at {src},{dst}: {value!r}")
            if src == dst and value != "0":
                diag_zero = False
            if rows[r].get(dst) != rows[c].get(src):
                symmetric = False
            if value == "1" and src != dst:
                nonzero_pairs.add(tuple(sorted((src, dst))))
    if not diag_zero:
        errors.append("Matrix diagonal is not zero.")
    if not symmetric:
        errors.append("Matrix is not symmetric.")

    edge_pairs = {edge_key(edge) for edge in edges}
    edge_endpoints_missing = [
        f"{edge['source']}--{edge['target']}"
        for edge in edges
        if edge["source"] not in nodes or edge["target"] not in nodes
    ]
    if edge_endpoints_missing:
        errors.append("Edge endpoints missing from matrix: " + "; ".join(edge_endpoints_missing))
    if edge_pairs != nonzero_pairs:
        missing_in_matrix = sorted(edge_pairs - nonzero_pairs)
        missing_in_edges = sorted(nonzero_pairs - edge_pairs)
        if missing_in_matrix:
            errors.append("Edges absent from matrix: " + "; ".join(f"{a}--{b}" for a, b in missing_in_matrix))
        if missing_in_edges:
            errors.append("Matrix pairs absent from edge CSV: " + "; ".join(f"{a}--{b}" for a, b in missing_in_edges))

    degree = {node: 0 for node in nodes}
    for a, b in edge_pairs:
        if a in degree:
            degree[a] += 1
        if b in degree:
            degree[b] += 1
    isolated = [node for node, count in degree.items() if count == 0]

    return {
        "node_count": len(nodes),
        "unique_node_count": len(set(nodes)),
        "edge_count": len(edges),
        "symmetric": symmetric,
        "diagonal_zero": diag_zero,
        "row_column_labels_identical": nodes == cols,
        "validation_errors": errors,
        "isolated_nodes": isolated,
        "isolated_node_count": len(isolated),
        "matrix_sha256": sha256(matrix_path),
        "edges_sha256": sha256(edges_path),
    }


def copy_text(src: Path, dst: Path) -> None:
    dst.write_bytes(src.read_bytes())


def final_nodes_from_matrix(matrix_path: Path) -> list[dict[str, object]]:
    rows = read_csv(matrix_path)
    inventory = {row["node_name"]: row for row in read_csv(ARTIFACTS / "component_inventory_doc40_current.csv")}
    final = []
    for idx, row in enumerate(rows, 1):
        name = row["node_name"]
        inv = inventory.get(name, {})
        final.append(
            {
                "node_name": name,
                "order": idx,
                "component_type": inv.get("component_type", ""),
                "node_kind": inv.get("node_kind", ""),
                "bbox": inv.get("bbox", ""),
                "centroid_x": inv.get("centroid_x", ""),
                "centroid_y": inv.get("centroid_y", ""),
                "source": "input_inventory_retained",
            }
        )
    return final


def rejected_candidates() -> list[dict[str, object]]:
    diego_edges = {edge_key(r): r for r in read_csv(RESULTS / "current_round_01_diego_edges.csv")}
    final_edges = {edge_key(r): r for r in read_csv(RESULTS / f"{FINAL_PREFIX}_edges.csv")}
    rejected: list[dict[str, object]] = []
    for key, row in sorted(diego_edges.items()):
        if key not in final_edges:
            rejected.append(
                {
                    "source": key[0],
                    "target": key[1],
                    "round_first_seen": "current_round_01_diego",
                    "rejected_by": "current_round_01_jennifer",
                    "original_edge_type": row.get("edge_type", ""),
                    "original_confidence": row.get("confidence", ""),
                    "reason": "Removed during precision review as unsupported edge or endpoint excluded from final node set.",
                    "original_evidence": row.get("evidence", ""),
                }
            )
    diego_matrix_nodes = [r["node_name"] for r in read_csv(RESULTS / "current_round_01_diego_matrix.csv")]
    final_nodes = {r["node_name"] for r in read_csv(RESULTS / f"{FINAL_PREFIX}_matrix.csv")}
    for name in diego_matrix_nodes:
        if name not in final_nodes:
            rejected.append(
                {
                    "source": name,
                    "target": "",
                    "round_first_seen": "current_round_01_diego",
                    "rejected_by": "current_round_01_jennifer",
                    "original_edge_type": "node",
                    "original_confidence": "",
                    "reason": "Excluded from final matrix because it is a label-only banner/source/control-lane/enclosure title rather than a connected electrical/logical node.",
                    "original_evidence": "",
                }
            )
    return rejected


def uncertain_candidates() -> list[dict[str, object]]:
    rows = []
    for edge in read_csv(RESULTS / f"{FINAL_PREFIX}_edges.csv"):
        try:
            conf = float(edge.get("confidence", ""))
        except ValueError:
            conf = 1.0
        if conf < 0.90 or "uncertain" in edge.get("edge_type", "").lower():
            rows.append(
                {
                    "source": edge["source"],
                    "target": edge["target"],
                    "edge_type": edge.get("edge_type", ""),
                    "confidence": edge.get("confidence", ""),
                    "evidence": edge.get("evidence", ""),
                }
            )
    return rows


def find_agent_usage(agent_ids: list[str]) -> dict[str, int]:
    roots = [
        Path(r"C:\Users\AREFA\.codex"),
        Path(r"C:\Users\AREFA\AppData\Roaming\Codex"),
        Path(r"C:\Users\AREFA\AppData\Local\Codex"),
    ]
    usage = {
        "model_calls": 0,
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }
    matched_files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            if any(agent_id in path.name for agent_id in agent_ids):
                matched_files.append(path)
                continue
            # Some sessions do not include the agent id in the file name; only
            # inspect the first metadata line rather than scanning every token line.
            try:
                with path.open("r", encoding="utf-8", errors="ignore") as fh:
                    head = fh.readline()
            except OSError:
                continue
            if any(agent_id in head for agent_id in agent_ids):
                matched_files.append(path)

    for path in sorted(set(matched_files)):
        model_calls = 0
        last_total: dict[str, int] | None = None
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line in lines:
            if '"type":"token_count"' not in line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            info = obj.get("payload", {}).get("info", {})
            total_usage = info.get("total_token_usage")
            if not isinstance(total_usage, dict):
                continue
            model_calls += 1
            last_total = {
                "input_tokens": int(total_usage.get("input_tokens", 0) or 0),
                "cached_input_tokens": int(total_usage.get("cached_input_tokens", 0) or 0),
                "output_tokens": int(total_usage.get("output_tokens", 0) or 0),
                "reasoning_output_tokens": int(total_usage.get("reasoning_output_tokens", 0) or 0),
                "total_tokens": int(total_usage.get("total_tokens", 0) or 0),
            }
        if last_total:
            usage["model_calls"] += model_calls
            usage["input_tokens"] += last_total["input_tokens"]
            usage["cached_input_tokens"] += last_total["cached_input_tokens"]
            usage["output_tokens"] += last_total["output_tokens"]
            usage["reasoning_output_tokens"] += last_total["reasoning_output_tokens"]
            usage["total_tokens"] += last_total["total_tokens"]

    # Fallback for any non-Codex-style usage objects colocated with metadata.
    if usage["model_calls"] == 0:
        for path in sorted(set(matched_files)):
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for line_no, line in enumerate(lines, 1):
                if "token_count" not in line and '"usage"' not in line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                key = f"{path}:{line_no}"
                candidates = []
                if isinstance(obj, dict):
                    candidates.extend([obj.get("token_count"), obj.get("usage")])
                    payload = obj.get("payload")
                    if isinstance(payload, dict):
                        candidates.extend([payload.get("token_count"), payload.get("usage")])
                    msg = obj.get("message")
                    if isinstance(msg, dict):
                        candidates.extend([msg.get("token_count"), msg.get("usage")])
                for cand in candidates:
                    if not isinstance(cand, dict):
                        continue
                    total = cand.get("total_tokens") or cand.get("total")
                    inp = cand.get("input_tokens") or cand.get("prompt_tokens") or 0
                    out = cand.get("output_tokens") or cand.get("completion_tokens") or 0
                    cached = cand.get("cached_input_tokens") or cand.get("cached_tokens") or 0
                    reasoning = cand.get("reasoning_output_tokens") or cand.get("reasoning_tokens") or 0
                    if total or inp or out:
                        usage["model_calls"] += 1
                        usage["input_tokens"] += int(inp or 0)
                        usage["cached_input_tokens"] += int(cached or 0)
                        usage["output_tokens"] += int(out or 0)
                        usage["reasoning_output_tokens"] += int(reasoning or 0)
                        usage["total_tokens"] += int(total or (int(inp or 0) + int(out or 0)))
                        break
    return usage


def update_tracker(validation: dict[str, object]) -> dict[str, object]:
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    diego = find_agent_usage(DIEGO_AGENT_IDS)
    jennifer = find_agent_usage(JENNIFER_AGENT_IDS)
    completed = {
        key: diego.get(key, 0) + jennifer.get(key, 0)
        for key in [
            "model_calls",
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "reasoning_output_tokens",
            "total_tokens",
        ]
    }
    workflow_low = completed["total_tokens"] + MAIN_LOW_ESTIMATE
    workflow_expected = completed["total_tokens"] + MAIN_EXPECTED_ESTIMATE
    workflow_high = completed["total_tokens"] + MAIN_HIGH_ESTIMATE
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    row_updates = {
        "family": "Improved",
        "document": "40",
        "iteration": "1",
        "workflow_label": "Improved doc 40 / Iteration 1",
        "record_type": "multi_agent_token_usage_unvalidated_final",
        "metric_label": "Final connectivity -- unvalidated",
        "metric_agent": "Final",
        "metric_round": "final",
        "is_selected_final_metric": "1",
        "final_metric_selection_basis": "final saturated multi-agent extraction; validation metrics pending",
        "validation_note": "No GT or GT-derived validation metric file used during extraction; metrics intentionally blank pending after-the-fact validation.",
        "actual_multi_agent_model_calls": completed["model_calls"],
        "actual_multi_agent_input_tokens": completed["input_tokens"],
        "actual_multi_agent_cached_input_tokens": completed["cached_input_tokens"],
        "actual_multi_agent_output_tokens": completed["output_tokens"],
        "actual_multi_agent_reasoning_output_tokens": completed["reasoning_output_tokens"],
        "actual_multi_agent_total_tokens": completed["total_tokens"],
        "image_file_input_tokens": "",
        "image_file_input_note": "not separately exposed; included in input_tokens",
        "token_usage_basis": "actual completed subagent Codex token_count logs for all Diego/Jennifer round threads; live main-agent orchestration/finalization estimated",
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
        "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available. actual_multi_agent_* columns in this row represent completed subagents only and aggregate all Diego/Jennifer round threads; use workflow_*_estimate_total_tokens for total-turn planning.",
        "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
        "completed_subagent_model_calls": completed["model_calls"],
        "completed_subagent_input_tokens": completed["input_tokens"],
        "completed_subagent_cached_input_tokens": completed["cached_input_tokens"],
        "completed_subagent_output_tokens": completed["output_tokens"],
        "completed_subagent_reasoning_output_tokens": completed["reasoning_output_tokens"],
        "completed_subagent_total_tokens": completed["total_tokens"],
        "main_low_estimate_tokens": MAIN_LOW_ESTIMATE,
        "main_expected_estimate_tokens": MAIN_EXPECTED_ESTIMATE,
        "main_high_estimate_tokens": MAIN_HIGH_ESTIMATE,
        "workflow_low_estimate_total_tokens": workflow_low,
        "workflow_expected_estimate_total_tokens": workflow_expected,
        "workflow_high_estimate_total_tokens": workflow_high,
        "token_update_timestamp": timestamp,
    }

    rows: list[dict[str, str]] = []
    fields: list[str] = []
    if TRACKER_CSV.exists():
        rows = read_csv(TRACKER_CSV)
        fields = list(rows[0].keys()) if rows else []
    for field in row_updates:
        if field not in fields:
            fields.append(field)
    if not fields:
        fields = list(row_updates.keys())

    new_rows = []
    replaced = False
    for row in rows:
        if row.get("family") == "Improved" and row.get("document") == "40" and row.get("iteration") == "1":
            merged = {field: row.get(field, "") for field in fields}
            merged.update({key: str(value) for key, value in row_updates.items()})
            new_rows.append(merged)
            replaced = True
        else:
            new_rows.append({field: row.get(field, "") for field in fields})
    if not replaced:
        new_rows.append({field: str(row_updates.get(field, "")) for field in fields})

    write_csv(TRACKER_CSV, new_rows, fields)

    note = f"""
## Doc 40 Iteration 1 Update - {timestamp}

Updated `Improved doc 40 / Iteration 1` as `record_type=multi_agent_token_usage_unvalidated_final`.

Extraction status:
- Final output stored at `{RESULTS}`.
- Saturated final matrix source: `{FINAL_PREFIX}`.
- Final matrix has {validation['node_count']} nodes and {validation['edge_count']} visually supported unique edges.
- Excluded label/enclosure rows and unsupported no-dot voltage-to-RWST MOV candidates during precision review.
- No validation metrics or GT-derived feedback were used during extraction.
- FP/FN/precision/recall/F1 are blank for doc 40 until an after-the-fact validation metrics CSV is available.

Token status:
- Diego actual completed usage across {len(DIEGO_AGENT_IDS)} thread(s): {diego['model_calls']} calls, {diego['total_tokens']} total tokens.
- Jennifer actual completed usage across {len(JENNIFER_AGENT_IDS)} thread(s): {jennifer['model_calls']} calls, {jennifer['total_tokens']} total tokens.
- Completed subagent total: {completed['model_calls']} calls, {completed['total_tokens']} total tokens.
- Workflow total estimate including main-agent orchestration/finalization: low {workflow_low}, expected {workflow_expected}, high {workflow_high}.
"""
    previous = TRACKER_NOTES.read_text(encoding="utf-8") if TRACKER_NOTES.exists() else "# Token Performance Tracking Notes\n"
    marker = "## Doc 40 Iteration 1 Update - "
    if marker in previous:
        before = previous[: previous.rfind(marker)]
        TRACKER_NOTES.write_text(before.rstrip() + "\n\n" + note.strip() + "\n", encoding="utf-8")
    else:
        TRACKER_NOTES.write_text(previous.rstrip() + "\n\n" + note.strip() + "\n", encoding="utf-8")

    return {
        "diego": diego,
        "jennifer": jennifer,
        "completed": completed,
        "workflow_estimates": {"low": workflow_low, "expected": workflow_expected, "high": workflow_high},
    }


def main() -> None:
    final_edges_src = RESULTS / f"{FINAL_PREFIX}_edges.csv"
    final_matrix_src = RESULTS / f"{FINAL_PREFIX}_matrix.csv"
    if not final_edges_src.exists() or not final_matrix_src.exists():
        raise FileNotFoundError(f"Missing final source files for prefix {FINAL_PREFIX}")

    copy_text(final_edges_src, RESULTS / "final_connectivity_edges.csv")
    copy_text(final_edges_src, RESULTS / "final_edges.csv")
    copy_text(final_matrix_src, RESULTS / "final_connectivity_matrix.csv")
    copy_text(final_matrix_src, RESULTS / "connectivity_matrix.csv")

    nodes = final_nodes_from_matrix(final_matrix_src)
    write_csv(
        RESULTS / "final_connectivity_nodes.csv",
        nodes,
        ["node_name", "order", "component_type", "node_kind", "bbox", "centroid_x", "centroid_y", "source"],
    )

    validation = validate_matrix(RESULTS / "final_connectivity_matrix.csv", RESULTS / "final_connectivity_edges.csv")
    (RESULTS / "final_connectivity_validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    if validation.get("validation_errors"):
        raise RuntimeError(validation["validation_errors"])

    rejected = rejected_candidates()
    write_csv(
        RESULTS / "final_rejected_candidates.csv",
        rejected,
        ["source", "target", "round_first_seen", "rejected_by", "original_edge_type", "original_confidence", "reason", "original_evidence"],
    )
    uncertain = uncertain_candidates()
    write_csv(
        RESULTS / "final_uncertain_candidates.csv",
        uncertain,
        ["source", "target", "edge_type", "confidence", "evidence"],
    )

    token_status = update_tracker(validation)

    summary = [
        "# Final Connectivity Summary - Doc 40 / Iteration_1",
        "",
        "Final saturated source: `current_round_02_jennifer`.",
        "",
        "No GT, GT-derived feedback, evaluation metrics, or validation directories were used during extraction.",
        "",
        f"- Final node count: {validation['node_count']}",
        f"- Final undirected edge count: {validation['edge_count']}",
        f"- Matrix symmetric: {validation['symmetric']}",
        f"- Diagonal zero: {validation['diagonal_zero']}",
        f"- Validation errors: {len(validation['validation_errors'])}",
        f"- Isolated nodes: {', '.join(validation['isolated_nodes']) if validation['isolated_nodes'] else 'none'}",
        f"- Rejected candidates recorded: {len(rejected)}",
        f"- Lower-confidence/uncertain final candidates recorded: {len(uncertain)}",
        "",
        "Final files:",
        "- `final_connectivity_matrix.csv` and duplicate `connectivity_matrix.csv`",
        "- `final_connectivity_edges.csv` and duplicate `final_edges.csv`",
        "- `final_connectivity_nodes.csv`",
        "- `final_connectivity_validation.json`",
        "- `final_rejected_candidates.csv`",
        "- `final_uncertain_candidates.csv`",
        "",
        "Token tracking:",
        f"- Completed subagent calls: {token_status['completed']['model_calls']}",
        f"- Completed subagent total tokens: {token_status['completed']['total_tokens']}",
        f"- Workflow low/expected/high estimate: {token_status['workflow_estimates']['low']} / {token_status['workflow_estimates']['expected']} / {token_status['workflow_estimates']['high']}",
    ]
    (RESULTS / "final_connectivity_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "final_source": FINAL_PREFIX,
                "final_validation": validation,
                "final_uncertain_count": len(uncertain),
                "final_rejected_count": len(rejected),
                "token_status": token_status,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
