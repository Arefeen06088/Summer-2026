from __future__ import annotations

import csv
import json
import math
import os
import shutil
from collections import Counter
from pathlib import Path
from typing import Iterable

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + junctions + OCR")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = BASE / "precision_review_crops"

ROUND_EDGE_FILES = {
    "round_01_diego_high_recall": RESULTS / "document20_edge_list.csv",
    "round_02_jennifer_precision": RESULTS / "round_02_jennifer_precision_edges.csv",
    "round_03_diego_saturation": RESULTS / "round_03_diego_saturation_edges.csv",
    "round_04_jennifer_final": RESULTS / "round_04_jennifer_final_edges.csv",
}

FINAL_LOGICAL_NODES = [
    "BUS-13K-A",
    "BUS-13K-B",
    "BUS-416-A",
    "BUS-416-B",
    "BUS-480-A",
    "BUS-480-B",
    "BUS-480-C",
    "BUS-480-D",
    "BUS-125DCA",
    "BUS-125DCB",
]

REJECTED_ROUND_ONLY_NODES = [
    "UPS-A AC OUTPUT",
    "UPS-B AC OUTPUT",
    "A/B ESF INTERLOCK",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def component_order() -> list[str]:
    rows = read_csv(BASE / "component_visual_ocr_labels.csv")

    def sort_key(row: dict[str, str]) -> tuple[int, int, str]:
        x1, y1, _x2, _y2 = json.loads(row["bbox"])
        return int(y1), int(x1), row["final_label"]

    labels: list[str] = []
    for row in sorted(rows, key=sort_key):
        label = row["final_label"].strip()
        if label and label not in labels:
            labels.append(label)
    return labels


def normalize_edges(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        source = row["source"].strip()
        target = row["target"].strip()
        if not source or not target:
            raise ValueError(f"blank endpoint in {row}")
        if source == target:
            raise ValueError(f"self-loop edge: {source}")
        key = tuple(sorted((source, target)))
        if key in seen:
            raise ValueError(f"duplicate undirected edge: {source} -- {target}")
        seen.add(key)
        out.append(
            {
                "source": source,
                "target": target,
                "edge_kind": row.get("edge_kind", "").strip(),
                "confidence": row.get("confidence", "").strip(),
                "evidence": row.get("evidence", "").strip(),
            }
        )
    return out


def endpoints(edges: Iterable[dict[str, str]]) -> set[str]:
    names: set[str] = set()
    for edge in edges:
        names.add(edge["source"])
        names.add(edge["target"])
    return names


def node_order_for_edges(edges: list[dict[str, str]]) -> list[str]:
    component_nodes = component_order()
    edge_nodes = endpoints(edges)
    nodes: list[str] = []
    for node in FINAL_LOGICAL_NODES:
        if node in edge_nodes:
            nodes.append(node)
    for node in component_nodes:
        if node not in nodes:
            nodes.append(node)
    extras = sorted(edge_nodes - set(nodes))
    nodes.extend(extras)
    return nodes


def final_node_order(final_edges: list[dict[str, str]]) -> list[str]:
    nodes = node_order_for_edges(final_edges)
    return [node for node in nodes if node not in REJECTED_ROUND_ONLY_NODES]


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    node_set = set(nodes)
    missing = endpoints(edges) - node_set
    if missing:
        raise ValueError(f"{path.name} missing nodes: {sorted(missing)}")
    edge_pairs = {tuple(sorted((edge["source"], edge["target"]))) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                if row_node == col_node:
                    row.append("0")
                else:
                    row.append("1" if tuple(sorted((row_node, col_node))) in edge_pairs else "0")
            writer.writerow(row)


def matrix_health(nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    edge_pairs = {tuple(sorted((edge["source"], edge["target"]))) for edge in edges}
    isolated = sorted(set(nodes) - endpoints(edges))
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "unique_undirected_edge_count": len(edge_pairs),
        "unique_endpoint_count": len(endpoints(edges)),
        "isolated_nodes": isolated,
        "duplicate_undirected_edges": len(edge_pairs) != len(edges),
        "self_loops": [edge for edge in edges if edge["source"] == edge["target"]],
    }


def write_final_edges(final_edges: list[dict[str, str]]) -> None:
    fieldnames = ["source", "target", "edge_kind", "confidence", "evidence"]
    write_csv(RESULTS / "final_connectivity_edges.csv", final_edges, fieldnames)


def write_nodes(path: Path, nodes: list[str], final_edges: list[dict[str, str]]) -> None:
    component_nodes = set(component_order())
    endpoint_set = endpoints(final_edges)
    rows: list[dict[str, object]] = []
    for idx, node in enumerate(nodes, start=1):
        if node in FINAL_LOGICAL_NODES:
            node_kind = "logical_bus"
        elif node in component_nodes:
            node_kind = "physical_component"
        else:
            node_kind = "logical_or_added_node"
        rows.append(
            {
                "node_order": idx,
                "node": node,
                "node_kind": node_kind,
                "in_final_edges": node in endpoint_set,
            }
        )
    write_csv(path, rows, ["node_order", "node", "node_kind", "in_final_edges"])


def write_round_summaries(round_edges: dict[str, list[dict[str, str]]]) -> None:
    rows: list[dict[str, object]] = []
    for name, edges in round_edges.items():
        rows.append(
            {
                "round": name,
                "edge_count": len(edges),
                "unique_endpoint_count": len(endpoints(edges)),
                "kind_counts": ";".join(f"{k}:{v}" for k, v in sorted(Counter(e["edge_kind"] for e in edges).items())),
                "confidence_counts": ";".join(
                    f"{k}:{v}" for k, v in sorted(Counter(e["confidence"] for e in edges).items())
                ),
            }
        )
    write_csv(RESULTS / "round_summaries.csv", rows, ["round", "edge_count", "unique_endpoint_count", "kind_counts", "confidence_counts"])


def validate_matrix_file(path: Path) -> dict[str, object]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    body = rows[1:]
    row_names = [row[0] for row in body]
    issues: list[str] = []
    edge_count = 0
    if header != row_names:
        issues.append("row_column_order_mismatch")
    if len(set(header)) != len(header):
        issues.append("duplicate_nodes")
    for i, row in enumerate(body):
        values = row[1:]
        if len(values) != len(header):
            issues.append(f"bad_width_row_{i}")
            continue
        if values[i] != "0":
            issues.append(f"nonzero_diagonal_{row[0]}")
        for j, value in enumerate(values):
            if value not in {"0", "1"}:
                issues.append(f"bad_value_{row[0]}_{header[j]}_{value}")
            if rows[j + 1][i + 1] != value:
                issues.append(f"asymmetry_{row[0]}_{header[j]}")
            if j > i and value == "1":
                edge_count += 1
    return {
        "matrix_path": str(path),
        "node_count": len(header),
        "undirected_edges_from_matrix": edge_count,
        "issue_count": len(issues),
        "issues": issues,
    }


def token_counter():
    try:
        import tiktoken

        enc = tiktoken.get_encoding("o200k_base")

        def count_text(text: str) -> int:
            return len(enc.encode(text))

        return count_text, "tiktoken_o200k_base"
    except Exception as exc:
        error_name = exc.__class__.__name__

        def count_text(text: str) -> int:
            return math.ceil(len(text) / 4)

        return count_text, f"fallback_ceil_chars_div_4_after_{error_name}"


def image_token_estimate(path: Path) -> int:
    width, height = Image.open(path).size
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    short = min(width, height)
    if short > 768:
        scale2 = 768 / short
        width *= scale2
        height *= scale2
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def file_text_tokens(path: Path, count_text) -> int:
    try:
        return count_text(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return count_text(path.read_text(encoding="utf-8-sig"))


def prompt_tokens(text: str, count_text) -> int:
    return count_text(text)


def existing(paths: Iterable[Path]) -> list[Path]:
    return [path for path in paths if path.exists()]


def write_token_estimates() -> None:
    count_text, token_method = token_counter()
    api_key_present = bool(os.getenv("OPENAI_API_KEY"))

    prompts = {
        "main-01": "Document 20 setup, inventory, crop generation, and visual inspection orchestration.",
        "diego-01-high-recall": "Diego high-recall extraction prompt for document 20 with raw/crop/overlay review.",
        "jennifer-01-row-level-precision": "Jennifer precision review prompt for document 20 disputed edge decisions.",
        "diego-02-saturation": "Diego saturation review prompt after Jennifer round 02.",
        "jennifer-02-final-confirmation": "Jennifer final confirmation prompt after Diego round 03 saturation.",
        "main-02": "Main agent artifact generation, validation, token accounting, and final response.",
    }

    call_specs = [
        {
            "round": "setup",
            "call_id": "main-01",
            "actor": "main",
            "purpose": "inventory resources, create review crops, inspect high-risk regions, orchestrate agents",
            "text_files": [BASE / "component_visual_ocr_labels.csv", BASE / "wire_nodes.csv"],
            "image_files": [
                CROPS / "raw__full_top.png",
                CROPS / "raw__left_mid.png",
                CROPS / "raw__center_mid.png",
                CROPS / "raw__left_lower.png",
                CROPS / "raw__center_lower.png",
                CROPS / "raw__battery_dc_left.png",
                CROPS / "raw__battery_dc_right.png",
            ],
            "output": (1200, 2400, 4500),
            "reasoning": (1500, 4500, 9000),
        },
        {
            "round": "round_01",
            "call_id": "diego-01-high-recall",
            "actor": "Diego",
            "purpose": "high-recall extraction and 205-edge proposal",
            "text_files": [
                BASE / "component_visual_ocr_labels.csv",
                BASE / "wire_nodes.csv",
                CROPS / "component_index_by_position.md",
            ],
            "image_files": [
                CROPS / "raw__full_top.png",
                CROPS / "raw__left_top_sources.png",
                CROPS / "raw__center_top_buses.png",
                CROPS / "raw__right_top_sources.png",
                CROPS / "raw__left_mid.png",
                CROPS / "raw__center_mid.png",
                CROPS / "raw__right_mid.png",
                CROPS / "raw__left_lower.png",
                CROPS / "raw__center_lower.png",
                CROPS / "raw__battery_dc_left.png",
                CROPS / "raw__battery_dc_right.png",
                CROPS / "nodes__full_middle.png",
            ],
            "output": (3500, 7000, 12000),
            "reasoning": (5000, 12000, 24000),
        },
        {
            "round": "round_02",
            "call_id": "jennifer-01-row-level-precision",
            "actor": "Jennifer",
            "purpose": "precision review; kept 202, removed 4, added 1 replacement",
            "text_files": [
                RESULTS / "document20_edge_list.csv",
                RESULTS / "document20_node_additions_corrections.csv",
                RESULTS / "document20_uncertain_rejected_notes.md",
            ],
            "image_files": [
                CROPS / "raw__battery_dc_left.png",
                CROPS / "raw__battery_dc_right.png",
                CROPS / "nodes__battery_dc_left.png",
                CROPS / "nodes__battery_dc_right.png",
                CROPS / "raw__center_lower.png",
                CROPS / "raw__left_lower.png",
                CROPS / "raw__center_mid.png",
            ],
            "output": (2500, 5500, 10000),
            "reasoning": (4000, 9000, 18000),
        },
        {
            "round": "round_03",
            "call_id": "diego-02-saturation",
            "actor": "Diego",
            "purpose": "saturation review of Jennifer round 02; no changes",
            "text_files": [
                RESULTS / "round_02_jennifer_precision_edges.csv",
                RESULTS / "removed_edges_round_02_jennifer.csv",
                RESULTS / "added_edges_round_02_jennifer.csv",
                RESULTS / "jennifer_round_02_notes.md",
            ],
            "image_files": [
                CROPS / "raw__battery_dc_left.png",
                CROPS / "raw__battery_dc_right.png",
                CROPS / "raw__center_lower.png",
            ],
            "output": (1000, 2500, 4500),
            "reasoning": (2000, 5500, 11000),
        },
        {
            "round": "round_04",
            "call_id": "jennifer-02-final-confirmation",
            "actor": "Jennifer",
            "purpose": "final confirmation of Diego saturation set",
            "text_files": [
                RESULTS / "round_02_jennifer_precision_edges.csv",
                RESULTS / "round_03_diego_saturation_edges.csv",
                RESULTS / "round_03_diego_changes.csv",
                RESULTS / "diego_round_03_notes.md",
            ],
            "image_files": [CROPS / "raw__center_lower.png", CROPS / "raw__battery_dc_left.png", CROPS / "raw__battery_dc_right.png"],
            "output": (800, 1800, 3500),
            "reasoning": (1200, 3500, 8000),
        },
        {
            "round": "final_artifacts",
            "call_id": "main-02",
            "actor": "main",
            "purpose": "generate matrices, validation files, token estimates, and final response",
            "text_files": [
                RESULTS / "round_04_jennifer_final_edges.csv",
                RESULTS / "round_04_jennifer_final_notes.md",
                CODES / "generate_document20_artifacts.py",
            ],
            "image_files": [],
            "output": (800, 1600, 3000),
            "reasoning": (1200, 3000, 7000),
        },
    ]

    rows: list[dict[str, object]] = []
    for spec in call_specs:
        text_files = existing(spec["text_files"])
        image_files = existing(spec["image_files"])
        text_tokens = prompt_tokens(prompts[spec["call_id"]], count_text) + sum(file_text_tokens(path, count_text) for path in text_files)
        image_tokens = sum(image_token_estimate(path) for path in image_files)
        out_low, out_exp, out_high = spec["output"]
        rea_low, rea_exp, rea_high = spec["reasoning"]
        rows.append(
            {
                "document": 20,
                "iteration": 1,
                "round": spec["round"],
                "call_id": spec["call_id"],
                "actor": spec["actor"],
                "purpose": spec["purpose"],
                "input_tokens_est": text_tokens,
                "cached_input_tokens_est": 0,
                "image_file_input_tokens_est": image_tokens,
                "output_tokens_low_est": out_low,
                "output_tokens_expected_est": out_exp,
                "output_tokens_high_est": out_high,
                "reasoning_tokens_low_est": rea_low,
                "reasoning_tokens_expected_est": rea_exp,
                "reasoning_tokens_high_est": rea_high,
                "total_low_est": text_tokens + image_tokens + out_low + rea_low,
                "total_expected_est": text_tokens + image_tokens + out_exp + rea_exp,
                "total_high_est": text_tokens + image_tokens + out_high + rea_high,
                "actual_usage_object_available": "no",
                "notes": "Actual usage object unavailable; no OPENAI_API_KEY for Responses input-token counting endpoint.",
            }
        )

    fieldnames = [
        "document",
        "iteration",
        "round",
        "call_id",
        "actor",
        "purpose",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low_est",
        "output_tokens_expected_est",
        "output_tokens_high_est",
        "reasoning_tokens_low_est",
        "reasoning_tokens_expected_est",
        "reasoning_tokens_high_est",
        "total_low_est",
        "total_expected_est",
        "total_high_est",
        "actual_usage_object_available",
        "notes",
    ]
    write_csv(RESULTS / "model_call_usage_estimates.csv", rows, fieldnames)

    total_row = {
        "document": 20,
        "iteration": 1,
        "model_call_rows": len(rows),
        "input_tokens_est": sum(int(row["input_tokens_est"]) for row in rows),
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": sum(int(row["image_file_input_tokens_est"]) for row in rows),
        "output_tokens_expected_est": sum(int(row["output_tokens_expected_est"]) for row in rows),
        "reasoning_tokens_expected_est": sum(int(row["reasoning_tokens_expected_est"]) for row in rows),
        "total_low_est": sum(int(row["total_low_est"]) for row in rows),
        "total_expected_est": sum(int(row["total_expected_est"]) for row in rows),
        "total_high_est": sum(int(row["total_high_est"]) for row in rows),
        "usage_source": "estimated locally; no OPENAI_API_KEY and no Responses usage objects exposed to this environment",
    }
    write_csv(RESULTS / "token_usage_totals_by_document.csv", [total_row], list(total_row.keys()))

    artifact_rows: list[dict[str, object]] = []
    for path in sorted(set(p for spec in call_specs for p in existing(spec["text_files"]))):
        artifact_rows.append(
            {
                "artifact": str(path),
                "artifact_type": "text",
                "text_tokens_est": file_text_tokens(path, count_text),
                "image_tokens_est": 0,
                "method": token_method,
            }
        )
    for path in sorted(set(p for spec in call_specs for p in existing(spec["image_files"]))):
        artifact_rows.append(
            {
                "artifact": str(path),
                "artifact_type": "image",
                "text_tokens_est": 0,
                "image_tokens_est": image_token_estimate(path),
                "method": "high_detail_85_plus_170_per_512_tile_after_scaling",
            }
        )
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        artifact_rows,
        ["artifact", "artifact_type", "text_tokens_est", "image_tokens_est", "method"],
    )

    method_md = f"""# Token Estimation Method

No OpenAI API key was present in the environment, so the Responses input-token counting endpoint could not be called and actual `usage` objects were not available from the subagent responses.

Local estimates were produced as follows:

- Text/file tokens: `tiktoken` with `o200k_base` when available; fallback is `ceil(characters / 4)`.
- Image tokens: high-detail vision estimate `85 + 170 * tiles`, where images are scaled to fit within 2048 px, then scaled so the shortest side is at most 768 px, and counted in 512 px tiles.
- Cached input tokens: recorded as 0 because cache accounting is not observable locally.
- Output/reasoning tokens: low / expected / high ranges are scenario estimates based on actual artifact sizes and subagent task complexity.

Environment check:

- `OPENAI_API_KEY` present: {'yes' if api_key_present else 'no'}
- tokenizer method used: {token_method}
"""
    (RESULTS / "token_estimation_method.md").write_text(method_md, encoding="utf-8")


def write_validation(
    final_nodes: list[str],
    final_edges: list[dict[str, str]],
    round_edges: dict[str, list[dict[str, str]]],
) -> None:
    final_health = matrix_health(final_nodes, final_edges)
    matrix_validation = validate_matrix_file(RESULTS / "final_connectivity_matrix.csv")
    rejected_present = sorted(endpoints(final_edges).intersection(REJECTED_ROUND_ONLY_NODES))
    summary = {
        "document": 20,
        "final_node_count": len(final_nodes),
        "final_edge_count": len(final_edges),
        "final_unique_endpoint_count": len(endpoints(final_edges)),
        "isolated_nodes": final_health["isolated_nodes"],
        "duplicate_undirected_edges": final_health["duplicate_undirected_edges"],
        "self_loops": final_health["self_loops"],
        "matrix_symmetric": matrix_validation["issue_count"] == 0,
        "diagonal_zero": not any(issue.startswith("nonzero_diagonal") for issue in matrix_validation["issues"]),
        "undirected_edges_from_matrix": matrix_validation["undirected_edges_from_matrix"],
        "rejected_round_only_nodes_in_final_edges": rejected_present,
        "round_edge_counts": {name: len(edges) for name, edges in round_edges.items()},
        "source_constraints": {
            "used_only_allowed_resource_folder": True,
            "used_ground_truth": False,
            "used_evaluator_feedback": False,
            "used_off_the_shelf_ocr": False,
        },
    }
    (RESULTS / "final_validation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_readme(
    final_nodes: list[str],
    final_edges: list[dict[str, str]],
    round_edges: dict[str, list[dict[str, str]]],
) -> None:
    kind_counts = Counter(edge["edge_kind"] for edge in final_edges)
    confidence_counts = Counter(edge["confidence"] for edge in final_edges)
    readme = f"""# Document 20 Connectivity Extraction

This folder contains the saturated Diego/Jennifer extraction for document 20.

## Final Files

- `final_connectivity_matrix.csv`: final saturated matrix, 200 nodes by 200 nodes.
- `connectivity_matrix.csv`: copy of the final matrix for downstream consumers.
- `final_connectivity_edges.csv`: final saturated edge list.
- `nodes.csv`: final matrix node order and node kind.
- `round_*_matrix.csv`: per-round matrices. Round 01 includes the high-recall-only rejected logical nodes; later rounds do not.

## Round Progression

- Round 01 Diego high recall: {len(round_edges["round_01_diego_high_recall"])} proposed edges.
- Round 02 Jennifer precision: {len(round_edges["round_02_jennifer_precision"])} edges after 4 removals and 1 replacement edge.
- Round 03 Diego saturation: {len(round_edges["round_03_diego_saturation"])} edges with no changes from Jennifer.
- Round 04 Jennifer final: {len(round_edges["round_04_jennifer_final"])} confirmed final edges.

## Final Edge Counts By Kind

{chr(10).join(f"- {kind}: {count}" for kind, count in sorted(kind_counts.items()))}

## Final Edge Counts By Confidence

{chr(10).join(f"- {confidence}: {count}" for confidence, count in sorted(confidence_counts.items()))}

## Key Precision Decisions

- Removed unsupported `UPS-A AC OUTPUT` and `UPS-B AC OUTPUT` logical stubs.
- Treated `A/B ESF INTERLOCK` as a conductor label, not a matrix node; retained direct `RELAY-K106 -- RELAY-K108`.
- Kept 480 VAC-to-rectifier AC feeds as medium confidence where no separate breaker label is visible.
- Kept seven residual medium-confidence edges documented in `round_04_jennifer_final_notes.md`.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
"""
    (RESULTS / "README_document20_results.md").write_text(readme, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    round_edges = {name: normalize_edges(read_csv(path)) for name, path in ROUND_EDGE_FILES.items()}

    final_edges = round_edges["round_04_jennifer_final"]
    final_nodes = final_node_order(final_edges)

    for name, edges in round_edges.items():
        write_matrix(RESULTS / f"{name}_matrix.csv", node_order_for_edges(edges), edges)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    shutil.copyfile(RESULTS / "final_connectivity_matrix.csv", RESULTS / "connectivity_matrix.csv")
    write_final_edges(final_edges)
    write_nodes(RESULTS / "nodes.csv", final_nodes, final_edges)
    write_round_summaries(round_edges)
    write_validation(final_nodes, final_edges, round_edges)
    write_token_estimates()
    write_readme(final_nodes, final_edges, round_edges)

    print(
        json.dumps(
            {
                "nodes": len(final_nodes),
                "final_edges": len(final_edges),
                "round_edge_counts": {name: len(edges) for name, edges in round_edges.items()},
                "results": str(RESULTS),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
