from __future__ import annotations

import csv
import json
import math
import shutil
import struct
from collections import Counter
from pathlib import Path


DOC_ID = 13
ITERATION = 1

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

COMPONENTS_CSV = ROOT / "component_visual_ocr_labels.csv"
DIEGO_EDGES_CSV = RESULTS / "document13_edge_list.csv"
DIEGO_NODES_CSV = RESULTS / "document13_node_additions_corrections.csv"
DIEGO_NOTES_MD = RESULTS / "document13_uncertain_rejected_notes.md"
DIEGO_COUNTS_JSON = RESULTS / "document13_final_counts.json"

ACCEPTED_ADDITIONS = [
    "SWYD-230",
    "BUS-4A",
    "BUS-4B",
    "BUS-4C",
    "BUS-4D",
    "DC-BUS-A",
    "DC-BUS-B",
    "DC-BUS-C",
    "DC-BUS-D",
    "LOCAL-IO-A",
    "LOCAL-IO-B",
    "LOCAL-IO-C",
    "LOCAL-IO-D",
    "UNIT-GENERATOR-AUX-FEED",
]

DROPPED_ADDITIONS = {
    "BUS-230KV-SWITCHYARD",
    "ESFAS-LO-PERMISSIVE-A",
    "ESFAS-LO-PERMISSIVE-B",
    "ESFAS-LO-PERMISSIVE-C",
    "ESFAS-LO-PERMISSIVE-D",
    "DIESEL-GEN-A-AUTO-START",
    "DIESEL-GEN-B-AUTO-START",
    "DIESEL-GEN-C-AUTO-START",
    "DIESEL-GEN-D-AUTO-START",
    "ANNUNCIATOR-PLANT-PROCESS-COMPUTER",
    "125VDC-SYSTEM-SHT-DC-2",
}

FINAL_EDGE_KIND_COUNTS = {
    "ac_power_feeder": 145,
    "dc_power_feeder": 12,
    "control_trip": 14,
    "instrument_or_io": 8,
    "grounding": 8,
    "ac_or_dc_power_feeder": 4,
    "control_or_aux_power_loop": 4,
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


def is_local_io_to_jb(a: str, b: str) -> bool:
    return (a.startswith("LOCAL-IO-") and b.startswith("JB-")) or (
        b.startswith("LOCAL-IO-") and a.startswith("JB-")
    )


def is_jb_to_dc_bus(a: str, b: str) -> bool:
    return (a.startswith("JB-") and b.startswith("DC-BUS-")) or (
        b.startswith("JB-") and a.startswith("DC-BUS-")
    )


def is_mcc_to_relay(a: str, b: str) -> bool:
    return (a.startswith("MCC-") and b.startswith("RLY-")) or (
        b.startswith("MCC-") and a.startswith("RLY-")
    )


def removal_reason(edge: dict[str, str]) -> str | None:
    a = edge["node_a"]
    b = edge["node_b"]
    kind = edge["kind"]
    nodes = {a, b}

    if "BUS-230KV-SWITCHYARD" in nodes:
        return "Jennifer R2: collapsed title/feed descriptor; replace source chain with GRID-230KV--SWYD-230."
    if edge_key(a, b) == edge_key("UNIT-GENERATOR-AUX-FEED", "GEN-G1"):
        return "Jennifer R2: UNIT-GENERATOR-AUX-FEED is downstream of CB-201, not a separate edge to GEN-G1."
    if is_local_io_to_jb(a, b):
        return "Jennifer R2: LOCAL I/O co-location does not prove a conductor to the junction box."
    if is_jb_to_dc_bus(a, b):
        return "Jennifer R2: dashed/local I/O mark does not prove a hard DC-bus connection."
    if kind == "control_trip" and is_mcc_to_relay(a, b):
        return "Jennifer R2: relays are not directly wired to MCC busbars."
    if any(node.startswith("ESFAS-LO-PERMISSIVE-") for node in nodes):
        return "Jennifer R2: ESFAS permissive is note-level only."
    if any(node.startswith("DIESEL-GEN-") and node.endswith("-AUTO-START") for node in nodes):
        return "Jennifer R2: diesel auto-start text is not a point-to-point wire."
    if "ANNUNCIATOR-PLANT-PROCESS-COMPUTER" in nodes:
        return "Jennifer R2: offpage continuation excluded from the precise graph."
    if "125VDC-SYSTEM-SHT-DC-2" in nodes:
        return "Jennifer R2: offpage continuation excluded from the precise graph."
    if any(node in DROPPED_ADDITIONS for node in nodes):
        return "Jennifer R2: edge uses a dropped low-support added node."
    if kind in {"control_trip_uncertain", "offpage_continuation_uncertain", "ac_power_source_label"}:
        return "Jennifer R2: uncertain/source-label edge kind excluded from precise graph."
    return None


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
    fields = ["node_a", "node_b", "kind", "evidence", "confidence"]
    write_csv(path, edges, fields)


def png_size(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", header[16:24])
        return width, height
    except OSError:
        return None


def high_detail_image_tokens(width: int, height: int) -> int:
    # Local estimate based on the common high-detail image tiling rule:
    # fit within 2048 px, then scale shortest side to 768 px, then charge
    # 85 base tokens plus 170 per 512 px tile.
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
        chars = len(path.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return 0
    return math.ceil(chars / 4)


def write_token_estimates() -> None:
    artifacts: list[dict[str, object]] = []
    text_paths = [
        COMPONENTS_CSV,
        ROOT / "wire_nodes.csv",
        DIEGO_EDGES_CSV,
        DIEGO_NODES_CSV,
        DIEGO_NOTES_MD,
        DIEGO_COUNTS_JSON,
    ]
    for path in text_paths:
        artifacts.append(
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

    image_paths = [
        ROOT / "raw -- synthetic diagram _.png",
        ROOT / "wire_nodes_overlay.png",
        ROOT / "component_labels_banners_overlay.png",
        ROOT / "wires_mask_overlay.png",
        ROOT / "wires_mask.png",
    ]
    for path in image_paths:
        size = png_size(path)
        width = size[0] if size else ""
        height = size[1] if size else ""
        artifacts.append(
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
        artifacts,
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

    component_tokens = text_token_estimate(COMPONENTS_CSV)
    wire_tokens = text_token_estimate(ROOT / "wire_nodes.csv")
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
    setup_file_tokens = component_tokens + wire_tokens

    calls = [
        {
            "call_id": "main-01",
            "actor": "main",
            "round": "setup/inventory",
            "model_or_role": "Codex main agent",
            "payload_summary": "User instructions, folder inventory, component/wire CSV summaries, visual inspection of raw and overlays.",
            "prompt_text_tokens_est": 2400,
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
            "payload_summary": "Raw schematic, wire overlay, label overlay, component CSV, wire nodes, crop inventory, extraction instructions.",
            "prompt_text_tokens_est": 2200,
            "file_text_tokens_est": setup_file_tokens,
            "image_input_tokens_est": full_image_tokens,
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 4500,
            "output_tokens_expected_est": 8500,
            "output_tokens_high_est": 14000,
            "reasoning_tokens_low_est": 4000,
            "reasoning_tokens_expected_est": 9000,
            "reasoning_tokens_high_est": 16000,
        },
        {
            "call_id": "subagent-02",
            "actor": "Jennifer",
            "round": "round_01_orientation",
            "model_or_role": "gpt-5.5 precision reviewer",
            "payload_summary": "Raw schematic, wire overlay, label overlay, component CSV, wire nodes, independent orientation instructions.",
            "prompt_text_tokens_est": 2100,
            "file_text_tokens_est": setup_file_tokens,
            "image_input_tokens_est": full_image_tokens,
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 700,
            "output_tokens_expected_est": 1400,
            "output_tokens_high_est": 2600,
            "reasoning_tokens_low_est": 2000,
            "reasoning_tokens_expected_est": 4500,
            "reasoning_tokens_high_est": 9000,
        },
        {
            "call_id": "subagent-03",
            "actor": "Jennifer",
            "round": "round_02_precision",
            "model_or_role": "gpt-5.5 precision reviewer",
            "payload_summary": "Jennifer prior context plus Diego proposal CSV/JSON/notes and precision review prompt.",
            "prompt_text_tokens_est": 950,
            "file_text_tokens_est": diego_package_tokens,
            "image_input_tokens_est": 0,
            "cached_input_tokens_est": setup_file_tokens + full_image_tokens,
            "output_tokens_low_est": 550,
            "output_tokens_expected_est": 850,
            "output_tokens_high_est": 1300,
            "reasoning_tokens_low_est": 1600,
            "reasoning_tokens_expected_est": 3500,
            "reasoning_tokens_high_est": 7000,
        },
        {
            "call_id": "subagent-04",
            "actor": "Diego",
            "round": "round_03_saturation",
            "model_or_role": "gpt-5.5 high-recall extractor",
            "payload_summary": "Diego prior context plus Jennifer precision decision and saturation check prompt.",
            "prompt_text_tokens_est": 1050,
            "file_text_tokens_est": 0,
            "image_input_tokens_est": 0,
            "cached_input_tokens_est": setup_file_tokens + full_image_tokens,
            "output_tokens_low_est": 120,
            "output_tokens_expected_est": 220,
            "output_tokens_high_est": 400,
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
            "payload_summary": "Subagent decisions, CSV structure inspection, artifact generator design, validation, final response.",
            "prompt_text_tokens_est": 1600,
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
    base_nodes = unique_preserving_order([row["final_label"] for row in component_rows])
    if len(base_nodes) != len(component_rows):
        duplicates = [
            label for label, count in Counter(row["final_label"] for row in component_rows).items() if count > 1
        ]
        raise ValueError(f"Duplicate component labels in component CSV: {duplicates}")
    if len(base_nodes) != 178:
        raise ValueError(f"Expected 178 detected component nodes, found {len(base_nodes)}")

    diego_node_rows = read_csv(DIEGO_NODES_CSV)
    diego_additions = [
        row["label"] for row in diego_node_rows if row["action"].startswith("add_")
    ]
    diego_nodes = base_nodes + diego_additions
    final_nodes = base_nodes + ACCEPTED_ADDITIONS

    if len(diego_nodes) != 203:
        raise ValueError(f"Expected Diego round-1 node count 203, found {len(diego_nodes)}")
    if len(final_nodes) != 192:
        raise ValueError(f"Expected final node count 192, found {len(final_nodes)}")

    diego_edges = normalize_edges(read_csv(DIEGO_EDGES_CSV))
    if len(diego_edges) != 243:
        raise ValueError(f"Expected Diego round-1 edge count 243, found {len(diego_edges)}")

    removed_edges: list[dict[str, object]] = []
    kept_edges: list[dict[str, str]] = []
    for edge in diego_edges:
        reason = removal_reason(edge)
        if reason:
            row = dict(edge)
            row["removal_reason"] = reason
            removed_edges.append(row)
        else:
            kept_edges.append(edge)

    replacement_edge = {
        "node_a": "GRID-230KV",
        "node_b": "SWYD-230",
        "kind": "ac_power_feeder",
        "evidence": "Jennifer R2 replacement: collapse title/feed descriptor into the drawn direct incoming source-to-switchyard connection.",
        "confidence": "high",
    }
    final_edges = normalize_edges([replacement_edge] + kept_edges)

    if len(removed_edges) != 49:
        raise ValueError(f"Expected 49 removed edges, found {len(removed_edges)}")
    if len(final_edges) != 195:
        raise ValueError(f"Expected final edge count 195, found {len(final_edges)}")
    final_kind_counts = dict(Counter(edge["kind"] for edge in final_edges))
    if final_kind_counts != FINAL_EDGE_KIND_COUNTS:
        raise ValueError(f"Final edge kind counts differ: {final_kind_counts}")

    final_node_set = set(final_nodes)
    missing = [
        (edge["node_a"], edge["node_b"])
        for edge in final_edges
        if edge["node_a"] not in final_node_set or edge["node_b"] not in final_node_set
    ]
    if missing:
        raise ValueError(f"Final edges contain endpoints missing from final nodes: {missing[:10]}")

    node_decision_rows: list[dict[str, object]] = []
    for row in component_rows:
        node_decision_rows.append(
            {
                "node": row["final_label"],
                "decision": "accepted",
                "source": "component_visual_ocr_labels.csv",
                "node_kind": row["node_kind"],
                "notes": "Existing detected component node retained.",
            }
        )
    for row in diego_node_rows:
        if not row["action"].startswith("add_"):
            node_decision_rows.append(
                {
                    "node": row["label"],
                    "decision": "interpret_existing",
                    "source": "Diego R1 / Jennifer R2",
                    "node_kind": row["node_kind"],
                    "notes": row["role_or_type"],
                }
            )
            continue
        label = row["label"]
        node_decision_rows.append(
            {
                "node": label,
                "decision": "accepted_added" if label in ACCEPTED_ADDITIONS else "dropped",
                "source": "Diego R1 / Jennifer R2",
                "node_kind": row["node_kind"],
                "notes": row["role_or_type"],
            }
        )

    final_node_rows = [
        {
            "order": idx + 1,
            "node": node,
            "source": "component_visual_ocr_labels.csv"
            if node in base_nodes
            else "accepted_added_logical_or_missing_node",
        }
        for idx, node in enumerate(final_nodes)
    ]

    write_csv(RESULTS / "nodes.csv", final_node_rows, ["order", "node", "source"])
    write_csv(
        RESULTS / "node_decisions_round_02_jennifer.csv",
        node_decision_rows,
        ["node", "decision", "source", "node_kind", "notes"],
    )

    write_edge_file(RESULTS / "round_01_diego_high_recall_edges.csv", diego_edges)
    write_matrix(RESULTS / "round_01_diego_high_recall_matrix.csv", diego_nodes, diego_edges)

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
    write_csv(
        RESULTS / "added_edges_round_02_jennifer.csv",
        [replacement_edge],
        ["node_a", "node_b", "kind", "evidence", "confidence"],
    )

    round_rows = []
    rounds = [
        ("round_01", "Diego", "high_recall", diego_nodes, diego_edges),
        ("round_02", "Jennifer", "precision", final_nodes, final_edges),
        ("round_03", "Diego", "saturation_agreement", final_nodes, final_edges),
        ("round_04", "Jennifer", "final_confirmation", final_nodes, final_edges),
    ]
    all_kind_fields = [
        "ac_power_feeder",
        "dc_power_feeder",
        "control_trip",
        "instrument_or_io",
        "grounding",
        "ac_or_dc_power_feeder",
        "control_or_aux_power_loop",
        "ac_power_source_label",
        "control_trip_uncertain",
        "offpage_continuation_uncertain",
    ]
    for round_id, agent, stage, nodes, edges in rounds:
        counts = Counter(edge["kind"] for edge in edges)
        row = {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": round_id,
            "agent": agent,
            "stage": stage,
            "node_count": len(nodes),
            "edge_count": len(edges),
        }
        row.update({kind: counts.get(kind, 0) for kind in all_kind_fields})
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
            *all_kind_fields,
        ],
    )

    readme = f"""# Document 13 Connectivity Extraction

Final saturated graph:

- Nodes: 192
- Undirected edges: 195
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Round progression:

- Round 01 Diego high recall: 203 nodes / 243 edges.
- Round 02 Jennifer precision: 192 nodes / 195 edges.
- Round 03 Diego saturation: agreed with Jennifer.
- Round 04 Jennifer final: confirmed no further changes.

Precision decisions:

- Included missing physical node `SWYD-230`.
- Included logical buses `BUS-4A/B/C/D`, `DC-BUS-A/B/C/D`, `LOCAL-IO-A/B/C/D`, and `UNIT-GENERATOR-AUX-FEED`.
- Excluded `BUS-230KV-SWITCHYARD`, ESFAS/diesel note-only control nodes, and offpage endpoints from the precise graph.
- Removed unsupported LOCAL I/O to JB, JB to DC bus, MCC to relay, note-only control, diesel auto-start, and offpage edges.
- Replaced the two-step switchyard descriptor path with `GRID-230KV -- SWYD-230`.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
"""
    (RESULTS / "README_document13_results.md").write_text(readme, encoding="utf-8")

    write_token_estimates()

    summary = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "final_node_count": len(final_nodes),
        "final_edge_count": len(final_edges),
        "final_edge_kind_counts": final_kind_counts,
        "removed_edges_round_02": len(removed_edges),
        "added_edges_round_02": 1,
        "rounds_written": [round_id for round_id, *_ in rounds],
    }
    (RESULTS / "final_validation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
