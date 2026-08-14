from __future__ import annotations

import csv
import json
import math
import shutil
import struct
from collections import Counter
from pathlib import Path


DOC_ID = 15
ITERATION = 1

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

COMPONENTS_CSV = ROOT / "component_visual_ocr_labels.csv"
DIEGO_EDGES_CSV = RESULTS / "document15_edge_list.csv"
DIEGO_NODES_CSV = RESULTS / "document15_node_additions_corrections.csv"
DIEGO_NOTES_MD = RESULTS / "document15_uncertain_rejected_notes.md"
DIEGO_COUNTS_JSON = RESULTS / "document15_final_counts.json"
RAW_IMAGE = ROOT / "raw -- improved_synthetic_nuclear_electrical_schematic.png"

REJECTED_EDGES_BY_LABEL = {
    ("CB-TIE-AB", "SEQ-1AB"),
    ("CB-TIE-AB", "RPS-AC-1"),
    ("CB-TIE-CD", "SEQ-2CD"),
    ("CB-TIE-CD", "RPS-AC-2"),
}

FINAL_KIND_COUNTS = {
    "solid_power": 68,
    "solid_bus_tap": 22,
    "transformer_power": 8,
    "tie_power": 8,
    "mcc_feeder_power": 24,
    "dc_bus_connection": 8,
    "ground_reference": 4,
    "dashed_control_association": 24,
    "dashed_control_path": 24,
    "dashed_dc_control_path": 8,
}

FINAL_CONFIDENCE_COUNTS = {
    "high": 138,
    "medium": 56,
    "low": 4,
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


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique.append(value)
    return unique


def edge_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def normalize_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    normalized: list[dict[str, str]] = []
    for edge in edges:
        key = edge_key(edge["node_a"], edge["node_b"])
        if key in seen:
            continue
        seen.add(key)
        normalized.append(edge)
    return normalized


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: idx for idx, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in index or b not in index:
            raise ValueError(f"Edge endpoint missing from node list: {a} -- {b}")
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
        {
            "call_id": "main-01",
            "actor": "main",
            "round": "setup/inventory",
            "model_or_role": "Codex main agent",
            "payload_summary": "User instructions, folder inventory, CSV summaries, crop creation, and visual inspection.",
            "prompt_text_tokens_est": 2500,
            "file_text_tokens_est": setup_file_tokens,
            "image_input_tokens_est": full_image_tokens,
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 900,
            "output_tokens_expected_est": 1800,
            "output_tokens_high_est": 3200,
            "reasoning_tokens_low_est": 1200,
            "reasoning_tokens_expected_est": 3000,
            "reasoning_tokens_high_est": 6000,
        },
        {
            "call_id": "subagent-01",
            "actor": "Diego",
            "round": "round_01_high_recall",
            "model_or_role": "gpt-5.5 high-recall extractor",
            "payload_summary": "Raw schematic, wire overlay, label overlay, CSV aids, crop inventory, extraction prompt.",
            "prompt_text_tokens_est": 2300,
            "file_text_tokens_est": setup_file_tokens,
            "image_input_tokens_est": full_image_tokens,
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 4000,
            "output_tokens_expected_est": 7200,
            "output_tokens_high_est": 12000,
            "reasoning_tokens_low_est": 4000,
            "reasoning_tokens_expected_est": 9000,
            "reasoning_tokens_high_est": 16000,
        },
        {
            "call_id": "subagent-02",
            "actor": "Jennifer",
            "round": "round_01_orientation",
            "model_or_role": "gpt-5.5 precision reviewer",
            "payload_summary": "Raw schematic, wire overlay, label overlay, CSV aids, independent orientation prompt.",
            "prompt_text_tokens_est": 2200,
            "file_text_tokens_est": setup_file_tokens,
            "image_input_tokens_est": full_image_tokens,
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 650,
            "output_tokens_expected_est": 1300,
            "output_tokens_high_est": 2400,
            "reasoning_tokens_low_est": 2000,
            "reasoning_tokens_expected_est": 4500,
            "reasoning_tokens_high_est": 9000,
        },
        {
            "call_id": "subagent-03",
            "actor": "Jennifer",
            "round": "round_02_precision",
            "model_or_role": "gpt-5.5 precision reviewer",
            "payload_summary": "Jennifer prior context, Diego proposal package, and precision-review prompt.",
            "prompt_text_tokens_est": 1100,
            "file_text_tokens_est": diego_package_tokens,
            "image_input_tokens_est": 0,
            "cached_input_tokens_est": setup_file_tokens + full_image_tokens,
            "output_tokens_low_est": 500,
            "output_tokens_expected_est": 850,
            "output_tokens_high_est": 1400,
            "reasoning_tokens_low_est": 1600,
            "reasoning_tokens_expected_est": 3500,
            "reasoning_tokens_high_est": 7000,
        },
        {
            "call_id": "subagent-04",
            "actor": "Diego",
            "round": "round_03_saturation",
            "model_or_role": "gpt-5.5 high-recall extractor",
            "payload_summary": "Diego prior context plus Jennifer precision decision and saturation prompt.",
            "prompt_text_tokens_est": 950,
            "file_text_tokens_est": 0,
            "image_input_tokens_est": 0,
            "cached_input_tokens_est": setup_file_tokens + full_image_tokens,
            "output_tokens_low_est": 150,
            "output_tokens_expected_est": 280,
            "output_tokens_high_est": 500,
            "reasoning_tokens_low_est": 500,
            "reasoning_tokens_expected_est": 1200,
            "reasoning_tokens_high_est": 2500,
        },
        {
            "call_id": "subagent-05",
            "actor": "Jennifer",
            "round": "round_04_final",
            "model_or_role": "gpt-5.5 precision reviewer",
            "payload_summary": "Jennifer prior context plus Diego saturation statement and final confirmation prompt.",
            "prompt_text_tokens_est": 450,
            "file_text_tokens_est": 0,
            "image_input_tokens_est": 0,
            "cached_input_tokens_est": setup_file_tokens + full_image_tokens + diego_package_tokens,
            "output_tokens_low_est": 120,
            "output_tokens_expected_est": 220,
            "output_tokens_high_est": 400,
            "reasoning_tokens_low_est": 400,
            "reasoning_tokens_expected_est": 900,
            "reasoning_tokens_high_est": 2000,
        },
        {
            "call_id": "main-02",
            "actor": "main",
            "round": "artifact_generation_and_final",
            "model_or_role": "Codex main agent",
            "payload_summary": "Subagent decisions, ID-to-label mapping, validation, token estimates, final response.",
            "prompt_text_tokens_est": 1700,
            "file_text_tokens_est": diego_package_tokens,
            "image_input_tokens_est": 0,
            "cached_input_tokens_est": setup_file_tokens,
            "output_tokens_low_est": 600,
            "output_tokens_expected_est": 1100,
            "output_tokens_high_est": 2000,
            "reasoning_tokens_low_est": 1200,
            "reasoning_tokens_expected_est": 2800,
            "reasoning_tokens_high_est": 5500,
        },
    ]

    for call in calls:
        total_input = (
            call["prompt_text_tokens_est"]
            + call["file_text_tokens_est"]
            + call["image_input_tokens_est"]
            + call["cached_input_tokens_est"]
        )
        call["document"] = DOC_ID
        call["iteration"] = ITERATION
        call["total_input_tokens_est"] = total_input
        call["total_tokens_low_est"] = (
            total_input + call["output_tokens_low_est"] + call["reasoning_tokens_low_est"]
        )
        call["total_tokens_expected_est"] = (
            total_input
            + call["output_tokens_expected_est"]
            + call["reasoning_tokens_expected_est"]
        )
        call["total_tokens_high_est"] = (
            total_input + call["output_tokens_high_est"] + call["reasoning_tokens_high_est"]
        )
        call["usage_object_available"] = "no"
        call["usage_object"] = "not exposed by local Codex/subagent tools"
        call[
            "notes"
        ] = "Responses token-counting endpoint was not called because no API key is available; values are local estimates."

    call_fields = [
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
    write_csv(RESULTS / "model_call_usage_estimates.csv", calls, call_fields)

    totals = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "model_call_count": len(calls),
        "prompt_text_tokens_est": sum(c["prompt_text_tokens_est"] for c in calls),
        "file_text_tokens_est": sum(c["file_text_tokens_est"] for c in calls),
        "image_input_tokens_est": sum(c["image_input_tokens_est"] for c in calls),
        "total_input_tokens_est": sum(c["total_input_tokens_est"] for c in calls),
        "cached_input_tokens_est": sum(c["cached_input_tokens_est"] for c in calls),
        "output_tokens_low_est": sum(c["output_tokens_low_est"] for c in calls),
        "output_tokens_expected_est": sum(c["output_tokens_expected_est"] for c in calls),
        "output_tokens_high_est": sum(c["output_tokens_high_est"] for c in calls),
        "reasoning_tokens_low_est": sum(c["reasoning_tokens_low_est"] for c in calls),
        "reasoning_tokens_expected_est": sum(c["reasoning_tokens_expected_est"] for c in calls),
        "reasoning_tokens_high_est": sum(c["reasoning_tokens_high_est"] for c in calls),
        "total_tokens_low_est": sum(c["total_tokens_low_est"] for c in calls),
        "total_tokens_expected_est": sum(c["total_tokens_expected_est"] for c in calls),
        "total_tokens_high_est": sum(c["total_tokens_high_est"] for c in calls),
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
    if len(component_rows) != 163:
        raise ValueError(f"Expected 163 detected component nodes, found {len(component_rows)}")
    component_id_to_label = {
        row["stable_node_id"]: row["final_label"] for row in component_rows
    }
    base_nodes = unique_preserving_order(row["final_label"] for row in component_rows)
    if len(base_nodes) != 163:
        raise ValueError("Component labels are not unique")

    diego_node_rows = read_csv(DIEGO_NODES_CSV)
    add_id_to_label = {
        row["node_id"]: row["label"] for row in diego_node_rows if row["action"] == "add"
    }
    added_nodes = [row["label"] for row in diego_node_rows if row["action"] == "add"]
    final_nodes = base_nodes + added_nodes
    if len(added_nodes) != 20 or len(final_nodes) != 183:
        raise ValueError(
            f"Expected 20 added nodes / 183 total nodes, found {len(added_nodes)} / {len(final_nodes)}"
        )

    id_to_label = {**component_id_to_label, **add_id_to_label}

    def label_for(node_id: str) -> str:
        try:
            return id_to_label[node_id]
        except KeyError as exc:
            raise ValueError(f"Unknown node id in Diego edge list: {node_id}") from exc

    raw_diego_edges = normalize_edges(read_csv(DIEGO_EDGES_CSV))
    if len(raw_diego_edges) != 202:
        raise ValueError(f"Expected Diego round-1 edge count 202, found {len(raw_diego_edges)}")

    diego_edges: list[dict[str, str]] = []
    removed_edges: list[dict[str, object]] = []
    final_edges: list[dict[str, str]] = []

    for edge in raw_diego_edges:
        mapped = dict(edge)
        mapped["node_a"] = label_for(edge["node_a"])
        mapped["node_b"] = label_for(edge["node_b"])
        diego_edges.append(mapped)

        if edge_key(mapped["node_a"], mapped["node_b"]) in {
            edge_key(*pair) for pair in REJECTED_EDGES_BY_LABEL
        }:
            removed = dict(mapped)
            removed[
                "removal_reason"
            ] = "Jennifer R2: no explicit dashed lead terminates at the tie breaker."
            removed_edges.append(removed)
        else:
            final_edges.append(mapped)

    diego_edges = normalize_edges(diego_edges)
    final_edges = normalize_edges(final_edges)
    if len(removed_edges) != 4:
        raise ValueError(f"Expected 4 removed edges, found {len(removed_edges)}")
    if len(final_edges) != 198:
        raise ValueError(f"Expected final edge count 198, found {len(final_edges)}")

    final_kind_counts = dict(Counter(edge["kind"] for edge in final_edges))
    final_confidence_counts = dict(Counter(edge["confidence"] for edge in final_edges))
    if final_kind_counts != FINAL_KIND_COUNTS:
        raise ValueError(f"Final edge kind counts differ: {final_kind_counts}")
    if final_confidence_counts != FINAL_CONFIDENCE_COUNTS:
        raise ValueError(f"Final confidence counts differ: {final_confidence_counts}")

    node_set = set(final_nodes)
    missing = [
        (edge["node_a"], edge["node_b"])
        for edge in final_edges
        if edge["node_a"] not in node_set or edge["node_b"] not in node_set
    ]
    if missing:
        raise ValueError(f"Final edges contain endpoints missing from node list: {missing[:10]}")

    node_rows = [
        {
            "order": idx + 1,
            "node": node,
            "source": "component_visual_ocr_labels.csv"
            if node in base_nodes
            else "accepted_added_logical_or_control_node",
        }
        for idx, node in enumerate(final_nodes)
    ]
    write_csv(RESULTS / "nodes.csv", node_rows, ["order", "node", "source"])

    node_decisions: list[dict[str, object]] = []
    for row in component_rows:
        node_decisions.append(
            {
                "original_id": row["stable_node_id"],
                "node": row["final_label"],
                "decision": "accepted_existing",
                "source": "component_visual_ocr_labels.csv",
                "node_kind": row["node_kind"],
                "notes": "Existing detected component retained.",
            }
        )
    for row in diego_node_rows:
        if row["action"] == "add":
            decision = "accepted_added"
        elif row["action"] == "confirm_role_correction":
            decision = "accepted_role_confirmation"
        else:
            decision = row["action"]
        node_decisions.append(
            {
                "original_id": row["node_id"],
                "node": row["label"],
                "decision": decision,
                "source": "Diego R1 / Jennifer R2",
                "node_kind": row["node_kind"],
                "notes": row["role_or_type"],
            }
        )
    write_csv(
        RESULTS / "node_decisions_round_02_jennifer.csv",
        node_decisions,
        ["original_id", "node", "decision", "source", "node_kind", "notes"],
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
        "solid_power",
        "solid_bus_tap",
        "transformer_power",
        "tie_power",
        "mcc_feeder_power",
        "dc_bus_connection",
        "ground_reference",
        "dashed_control_association",
        "dashed_control_path",
        "dashed_dc_control_path",
    ]
    rounds = [
        ("round_01", "Diego", "high_recall", diego_edges),
        ("round_02", "Jennifer", "precision", final_edges),
        ("round_03", "Diego", "saturation_agreement", final_edges),
        ("round_04", "Jennifer", "final_confirmation", final_edges),
    ]
    round_rows: list[dict[str, object]] = []
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
        round_rows.append(row)
    write_csv(
        RESULTS / "round_summaries.csv",
        round_rows,
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

    readme = f"""# Document 15 Connectivity Extraction

Final saturated graph:

- Nodes: 183
- Undirected edges: 198
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Round progression:

- Round 01 Diego high recall: 183 nodes / 202 edges.
- Round 02 Jennifer precision: 183 nodes / 198 edges.
- Round 03 Diego saturation: agreed with Jennifer.
- Round 04 Jennifer final: confirmed no further changes.

Precision decisions:

- Accepted buses `BUS-SWY-1/2`, `BUS-NSS-1/2`, `BUS-416A/B/C/D`, `BUS-480A/B/C/D`, and `BUS-DC-A/B/C/D`.
- Accepted control nodes `SEQ-1AB`, `RPS-AC-1`, `SEQ-2CD`, and `RPS-AC-2`.
- Confirmed `MCC-1A/B/C/D` as busbar-style physical components already in the component CSV.
- Removed four low-confidence direct `SEQ/RPS` to tie-breaker control associations.
- Kept medium `BUS-NSS` to `CB-DG` tap edges and all solid source/tie/transformer/MCC feeder paths.
- Kept lower DC/control strings and individual `BUS-DC` to ground references.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
"""
    (RESULTS / "README_document15_results.md").write_text(readme, encoding="utf-8")

    write_token_estimates()

    summary = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "final_node_count": len(final_nodes),
        "final_edge_count": len(final_edges),
        "final_edge_kind_counts": final_kind_counts,
        "final_confidence_counts": final_confidence_counts,
        "removed_edges_round_02": len(removed_edges),
        "rounds_written": [round_id for round_id, *_ in rounds],
    }
    (RESULTS / "final_validation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
