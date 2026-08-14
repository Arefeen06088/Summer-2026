from __future__ import annotations

import csv
import json
import math
import shutil
import struct
from collections import Counter
from pathlib import Path


DOC_ID = 16
ITERATION = 1

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

COMPONENTS_CSV = ROOT / "component_visual_ocr_labels.csv"
DIEGO_EDGES_CSV = RESULTS / "document16_edge_list.csv"
DIEGO_NODES_CSV = RESULTS / "document16_node_additions_corrections.csv"
DIEGO_NOTES_MD = RESULTS / "document16_uncertain_rejected_notes.md"
DIEGO_COUNTS_JSON = RESULTS / "document16_final_counts.json"
RAW_IMAGE = ROOT / "raw -- synthetic_npp_electrical_schematic_revised(1).png"

REJECTED_NODES = {"PP-E1-480-125R"}
EXPECTED_ISOLATED_FINAL_NODES = {"JB-R"}

REMOVED_EDGE_KEYS = {
    ("BATT-125A", "BUS-125DC-A"),
    ("BATT-125B", "BUS-125DC-B"),
    ("BUS-125DC-A", "ANN-501"),
    ("RELAY-27A", "CP-RPS-A"),
    ("RELAY-27B", "CP-RPS-B"),
    ("MG-RPS-A", "FT-AFW101"),
    ("CP-ANN-01", "TB-ESF-2"),
    ("MG-RPS-B", "RTD-RCS101"),
    ("JB-CONTAIN", "XS-DOOR101"),
    ("CB-401A", "CP-RPS-A"),
    ("CB-401B", "CP-RPS-A"),
    ("CB-480A-IN", "CP-DCS-01"),
    ("CB-TIE-480AB", "CP-DCS-01"),
    ("CB-480B-IN", "CP-ANN-01"),
    ("CB-12B-FDR", "CP-RPS-B"),
}

MEDIUM_UNCERTAIN_KEYS = {
    ("RTD-RCS101", "BUS-120-RPS-B"),
    ("UCP-01", "BUS-120-RPS-B"),
}

FINAL_KIND_COUNTS = {
    "power": 63,
    "relay_association": 24,
    "controlled_power": 22,
    "control": 23,
    "signal": 16,
    "ground": 17,
    "dc_power": 6,
    "dc_control_power": 7,
    "ac_power": 5,
}

FINAL_CONFIDENCE_COUNTS = {
    "high": 150,
    "medium": 33,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def edge_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def unique_preserving_order(values) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def normalize_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for edge in edges:
        key = edge_key(edge["node_a"], edge["node_b"])
        if key in seen:
            continue
        seen.add(key)
        out.append(edge)
    return out


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: idx for idx, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in index or b not in index:
            raise ValueError(f"Missing endpoint in node list: {a} -- {b}")
        if a == b:
            continue
        ia = index[a]
        ib = index[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edge_file(path: Path, edges: list[dict[str, str]]) -> None:
    write_csv(path, edges, ["node_a", "node_b", "kind", "evidence", "confidence"])


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", header[16:24])
    except OSError:
        return None


def high_detail_image_tokens(width: int, height: int) -> int:
    scale = min(2048 / width, 2048 / height, 1.0)
    w = width * scale
    h = height * scale
    shortest = min(w, h)
    if shortest > 768:
        scale = 768 / shortest
        w *= scale
        h *= scale
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def text_token_estimate(path: Path) -> int:
    try:
        return math.ceil(len(path.read_text(encoding="utf-8", errors="ignore")) / 4)
    except OSError:
        return 0


def write_token_estimates() -> None:
    text_paths = [
        COMPONENTS_CSV,
        ROOT / "wire_nodes.csv",
        DIEGO_EDGES_CSV,
        DIEGO_NODES_CSV,
        DIEGO_NOTES_MD,
        DIEGO_COUNTS_JSON,
    ]
    image_paths = [
        RAW_IMAGE,
        ROOT / "wire_nodes_overlay.png",
        ROOT / "component_labels_banners_overlay.png",
        ROOT / "wires_mask_overlay.png",
        ROOT / "wires_mask.png",
    ]

    artifact_rows: list[dict[str, object]] = []
    for path in text_paths:
        artifact_rows.append(
            {
                "artifact": str(path.relative_to(ROOT)),
                "kind": "text/csv/json/md",
                "bytes": path.stat().st_size if path.exists() else 0,
                "width": "",
                "height": "",
                "est_text_tokens_chars_div_4": text_token_estimate(path),
                "est_image_tokens_high_detail": "",
            }
        )
    for path in image_paths:
        size = png_size(path)
        width = size[0] if size else ""
        height = size[1] if size else ""
        artifact_rows.append(
            {
                "artifact": str(path.relative_to(ROOT)),
                "kind": "image/png",
                "bytes": path.stat().st_size if path.exists() else 0,
                "width": width,
                "height": height,
                "est_text_tokens_chars_div_4": "",
                "est_image_tokens_high_detail": high_detail_image_tokens(width, height)
                if size
                else "",
            }
        )
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        artifact_rows,
        [
            "artifact",
            "kind",
            "bytes",
            "width",
            "height",
            "est_text_tokens_chars_div_4",
            "est_image_tokens_high_detail",
        ],
    )

    setup_file_tokens = text_token_estimate(COMPONENTS_CSV) + text_token_estimate(
        ROOT / "wire_nodes.csv"
    )
    diego_package_tokens = (
        text_token_estimate(DIEGO_EDGES_CSV)
        + text_token_estimate(DIEGO_NODES_CSV)
        + text_token_estimate(DIEGO_NOTES_MD)
        + text_token_estimate(DIEGO_COUNTS_JSON)
    )
    full_image_tokens = sum(
        high_detail_image_tokens(*png_size(path))
        for path in image_paths[:3]
        if png_size(path)
    )

    calls = [
        ("main-01", "main", "setup/inventory", 2500, setup_file_tokens, full_image_tokens, 0, 900, 1800, 3200, 1200, 3000, 6000),
        ("subagent-01", "Diego", "round_01_high_recall", 2300, setup_file_tokens, full_image_tokens, 0, 4200, 7800, 12500, 4000, 9000, 16000),
        ("subagent-02", "Jennifer", "round_01_orientation", 2200, setup_file_tokens, full_image_tokens, 0, 650, 1300, 2400, 2000, 4500, 9000),
        ("subagent-03", "Jennifer", "round_02_precision", 1100, diego_package_tokens, 0, setup_file_tokens + full_image_tokens, 500, 900, 1500, 1600, 3500, 7000),
        ("subagent-04", "Diego", "round_03_saturation", 1100, 0, 0, setup_file_tokens + full_image_tokens, 150, 300, 600, 500, 1200, 2500),
        ("subagent-05", "Jennifer", "round_04_final", 500, 0, 0, setup_file_tokens + full_image_tokens + diego_package_tokens, 120, 220, 400, 400, 900, 2000),
        ("main-02", "main", "artifact_generation_and_final", 1700, diego_package_tokens, 0, setup_file_tokens, 600, 1100, 2000, 1200, 2800, 5500),
    ]

    rows: list[dict[str, object]] = []
    for (
        call_id,
        actor,
        round_name,
        prompt_tokens,
        file_tokens,
        image_tokens,
        cached_tokens,
        out_low,
        out_expected,
        out_high,
        reason_low,
        reason_expected,
        reason_high,
    ) in calls:
        total_input = prompt_tokens + file_tokens + image_tokens + cached_tokens
        rows.append(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "call_id": call_id,
                "actor": actor,
                "round": round_name,
                "model_or_role": "gpt-5.5 subagent" if actor in {"Diego", "Jennifer"} else "Codex main agent",
                "payload_summary": "local estimate; actual usage object unavailable",
                "prompt_text_tokens_est": prompt_tokens,
                "file_text_tokens_est": file_tokens,
                "image_input_tokens_est": image_tokens,
                "total_input_tokens_est": total_input,
                "cached_input_tokens_est": cached_tokens,
                "output_tokens_low_est": out_low,
                "output_tokens_expected_est": out_expected,
                "output_tokens_high_est": out_high,
                "reasoning_tokens_low_est": reason_low,
                "reasoning_tokens_expected_est": reason_expected,
                "reasoning_tokens_high_est": reason_high,
                "total_tokens_low_est": total_input + out_low + reason_low,
                "total_tokens_expected_est": total_input + out_expected + reason_expected,
                "total_tokens_high_est": total_input + out_high + reason_high,
                "usage_object_available": "no",
                "usage_object": "not exposed by local Codex/subagent tools",
                "notes": "Responses token-counting endpoint was not called because no API key is available; values are local estimates.",
            }
        )

    fields = [
        "document",
        "iteration",
        "call_id",
        "actor",
        "round",
        "model_or_role",
        "payload_summary",
        "prompt_text_tokens_est",
        "file_text_tokens_est",
        "image_input_tokens_est",
        "total_input_tokens_est",
        "cached_input_tokens_est",
        "output_tokens_low_est",
        "output_tokens_expected_est",
        "output_tokens_high_est",
        "reasoning_tokens_low_est",
        "reasoning_tokens_expected_est",
        "reasoning_tokens_high_est",
        "total_tokens_low_est",
        "total_tokens_expected_est",
        "total_tokens_high_est",
        "usage_object_available",
        "usage_object",
        "notes",
    ]
    write_csv(RESULTS / "model_call_usage_estimates.csv", rows, fields)

    totals = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "model_call_count": len(rows),
        "prompt_text_tokens_est": sum(r["prompt_text_tokens_est"] for r in rows),
        "file_text_tokens_est": sum(r["file_text_tokens_est"] for r in rows),
        "image_input_tokens_est": sum(r["image_input_tokens_est"] for r in rows),
        "total_input_tokens_est": sum(r["total_input_tokens_est"] for r in rows),
        "cached_input_tokens_est": sum(r["cached_input_tokens_est"] for r in rows),
        "output_tokens_low_est": sum(r["output_tokens_low_est"] for r in rows),
        "output_tokens_expected_est": sum(r["output_tokens_expected_est"] for r in rows),
        "output_tokens_high_est": sum(r["output_tokens_high_est"] for r in rows),
        "reasoning_tokens_low_est": sum(r["reasoning_tokens_low_est"] for r in rows),
        "reasoning_tokens_expected_est": sum(r["reasoning_tokens_expected_est"] for r in rows),
        "reasoning_tokens_high_est": sum(r["reasoning_tokens_high_est"] for r in rows),
        "total_tokens_low_est": sum(r["total_tokens_low_est"] for r in rows),
        "total_tokens_expected_est": sum(r["total_tokens_expected_est"] for r in rows),
        "total_tokens_high_est": sum(r["total_tokens_high_est"] for r in rows),
        "usage_objects_available": "no",
    }
    write_csv(RESULTS / "token_usage_totals_by_document.csv", [totals], list(totals.keys()))

    method = f"""# Token Estimation Method

Document: {DOC_ID}
Iteration: {ITERATION}

No OpenAI API key was available in this environment, so the Responses input-token
counting endpoint and response usage objects could not be collected. The token
tables therefore use local estimates:

- Text/file tokens: `ceil(character_count / 4)`.
- Image tokens: high-detail tile estimate after PNG dimension parsing:
  fit within 2048 px, scale shortest side to 768 px when larger, then
  `85 + 170 * ceil(width / 512) * ceil(height / 512)`.
- Cached input tokens are estimates for repeated subagent context only; the
  local tools do not expose actual cache-hit accounting.
- Output and reasoning tokens are low/expected/high estimates because actual
  model usage objects were unavailable.

The per-call estimates are in `model_call_usage_estimates.csv`; grouped totals
are in `token_usage_totals_by_document.csv`.
"""
    (RESULTS / "token_estimation_method.md").write_text(method, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    component_rows = read_csv(COMPONENTS_CSV)
    if len(component_rows) != 169:
        raise ValueError(f"Expected 169 component rows, found {len(component_rows)}")
    base_nodes = unique_preserving_order(
        row["final_label"] for row in component_rows if row["final_label"] not in REJECTED_NODES
    )
    if len(base_nodes) != 168:
        raise ValueError(f"Expected 168 non-rejected component nodes, found {len(base_nodes)}")

    node_rows_raw = read_csv(DIEGO_NODES_CSV)
    added_nodes = [row["label"] for row in node_rows_raw if row["action"] == "add"]
    if len(added_nodes) != 11:
        raise ValueError(f"Expected 11 accepted added nodes, found {len(added_nodes)}")
    final_nodes = base_nodes + added_nodes
    if len(final_nodes) != 179:
        raise ValueError(f"Expected 179 final nodes, found {len(final_nodes)}")

    diego_edges = normalize_edges(read_csv(DIEGO_EDGES_CSV))
    if len(diego_edges) != 198:
        raise ValueError(f"Expected 198 Diego edges, found {len(diego_edges)}")

    removed_edges: list[dict[str, object]] = []
    final_edges: list[dict[str, str]] = []
    removed_keys = {edge_key(*pair) for pair in REMOVED_EDGE_KEYS}
    medium_keys = {edge_key(*pair) for pair in MEDIUM_UNCERTAIN_KEYS}

    for edge in diego_edges:
        key = edge_key(edge["node_a"], edge["node_b"])
        if key in removed_keys:
            row = dict(edge)
            row["removal_reason"] = "Jennifer R2 precision removal: unsupported or overconnected low/medium-confidence lower control/DC edge."
            removed_edges.append(row)
            continue
        kept = dict(edge)
        if key in medium_keys:
            kept["confidence"] = "medium"
            kept["evidence"] = kept["evidence"] + " Jennifer R2: retained as medium-uncertain."
        final_edges.append(kept)

    final_edges = normalize_edges(final_edges)
    if len(removed_edges) != 15:
        raise ValueError(f"Expected 15 removed edges, found {len(removed_edges)}")
    if len(final_edges) != 183:
        raise ValueError(f"Expected 183 final edges, found {len(final_edges)}")

    kind_counts = dict(Counter(edge["kind"] for edge in final_edges))
    confidence_counts = dict(Counter(edge["confidence"] for edge in final_edges))
    if kind_counts != FINAL_KIND_COUNTS:
        raise ValueError(f"Kind counts differ: {kind_counts}")
    if confidence_counts != FINAL_CONFIDENCE_COUNTS:
        raise ValueError(f"Confidence counts differ: {confidence_counts}")

    final_node_set = set(final_nodes)
    missing = [
        (edge["node_a"], edge["node_b"])
        for edge in final_edges
        if edge["node_a"] not in final_node_set or edge["node_b"] not in final_node_set
    ]
    if missing:
        raise ValueError(f"Final edges have missing endpoints: {missing[:10]}")

    degree = Counter()
    for edge in final_edges:
        degree[edge["node_a"]] += 1
        degree[edge["node_b"]] += 1
    isolated = {node for node in final_nodes if degree[node] == 0}
    if isolated != EXPECTED_ISOLATED_FINAL_NODES:
        raise ValueError(f"Unexpected isolated nodes: {sorted(isolated)}")

    write_csv(
        RESULTS / "nodes.csv",
        [
            {
                "order": idx + 1,
                "node": node,
                "source": "component_visual_ocr_labels.csv"
                if node in base_nodes
                else "accepted_added_logical_or_missing_node",
            }
            for idx, node in enumerate(final_nodes)
        ],
        ["order", "node", "source"],
    )

    decisions: list[dict[str, object]] = []
    for row in component_rows:
        label = row["final_label"]
        decisions.append(
            {
                "node": label,
                "decision": "rejected_title_block_artifact" if label in REJECTED_NODES else "accepted_existing",
                "source": "component_visual_ocr_labels.csv",
                "node_kind": row["node_kind"],
                "notes": "Rejected by Diego/Jennifer as non-electrical title-block artifact." if label in REJECTED_NODES else "Existing detected component retained.",
            }
        )
    for row in node_rows_raw:
        decisions.append(
            {
                "node": row["label"],
                "decision": row["action"],
                "source": "Diego R1 / Jennifer R2-R4",
                "node_kind": row["node_kind"],
                "notes": row["role_or_type"],
            }
        )
    write_csv(
        RESULTS / "node_decisions_round_02_jennifer.csv",
        decisions,
        ["node", "decision", "source", "node_kind", "notes"],
    )

    write_edge_file(RESULTS / "round_01_diego_high_recall_edges.csv", diego_edges)
    write_matrix(RESULTS / "round_01_diego_high_recall_matrix.csv", final_nodes, diego_edges)
    write_edge_file(RESULTS / "round_02_jennifer_precision_edges.csv", final_edges)
    write_matrix(RESULTS / "round_02_jennifer_precision_matrix.csv", final_nodes, final_edges)
    write_edge_file(RESULTS / "round_03_diego_saturation_edges.csv", final_edges)
    write_matrix(RESULTS / "round_03_diego_saturation_matrix.csv", final_nodes, final_edges)
    write_edge_file(RESULTS / "round_04_jennifer_final_edges.csv", final_edges)
    write_matrix(RESULTS / "round_04_jennifer_final_matrix.csv", final_nodes, final_edges)
    write_edge_file(RESULTS / "final_connectivity_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    shutil.copyfile(RESULTS / "final_connectivity_matrix.csv", RESULTS / "connectivity_matrix.csv")

    write_csv(
        RESULTS / "removed_edges_round_02_jennifer.csv",
        removed_edges,
        ["node_a", "node_b", "kind", "evidence", "confidence", "removal_reason"],
    )

    kind_fields = [
        "power",
        "relay_association",
        "controlled_power",
        "control",
        "signal",
        "ground",
        "dc_power",
        "dc_control_power",
        "ac_power",
        "control_trip",
    ]
    rounds = [
        ("round_01", "Diego", "high_recall", diego_edges),
        ("round_02", "Jennifer", "precision", final_edges),
        ("round_03", "Diego", "saturation_agreement", final_edges),
        ("round_04", "Jennifer", "final_confirmation", final_edges),
    ]
    summary_rows: list[dict[str, object]] = []
    for round_id, agent, stage, edges in rounds:
        counts = Counter(edge["kind"] for edge in edges)
        row = {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": round_id,
            "agent": agent,
            "stage": stage,
            "node_count": len(final_nodes),
            "edge_count": len(edges),
        }
        row.update({kind: counts.get(kind, 0) for kind in kind_fields})
        summary_rows.append(row)
    write_csv(
        RESULTS / "round_summaries.csv",
        summary_rows,
        [
            "document",
            "iteration",
            "round",
            "agent",
            "stage",
            "node_count",
            "edge_count",
            *kind_fields,
        ],
    )

    readme = f"""# Document 16 Connectivity Extraction

Final saturated graph:

- Nodes: 179
- Undirected edges: 183
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Precision decisions:

- Accepted all non-rejected component CSV labels plus 11 added logical/physical nodes.
- Excluded only `PP-E1-480-125R` as a title-block/drawing-number artifact.
- Retained `JB-R` as an isolated real component.
- Removed 15 unsupported lower control/DC/control-trip edges.
- Retained `RTD-RCS101 -- BUS-120-RPS-B` and `UCP-01 -- BUS-120-RPS-B` as medium-confidence edges.
- Ties are breaker-mediated only; A/B buses are not merged.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
"""
    (RESULTS / "README_document16_results.md").write_text(readme, encoding="utf-8")

    write_token_estimates()

    final_summary = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "final_node_count": len(final_nodes),
        "final_edge_count": len(final_edges),
        "final_edge_kind_counts": kind_counts,
        "final_confidence_counts": confidence_counts,
        "removed_edges_round_02": len(removed_edges),
        "rejected_nodes": sorted(REJECTED_NODES),
        "isolated_final_nodes": sorted(isolated),
        "rounds_written": [round_id for round_id, *_ in rounds],
    }
    (RESULTS / "final_validation_summary.json").write_text(
        json.dumps(final_summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(final_summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
