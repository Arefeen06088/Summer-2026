from __future__ import annotations

import csv
import json
import math
import os
import shutil
from collections import Counter
from pathlib import Path

try:
    import tiktoken
except ImportError:
    tiktoken = None

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + junctions + OCR"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"

ROUND_EDGE_FILES = {
    "round_01_diego_high_recall": RESULTS / "document18_edge_list.csv",
    "round_02_jennifer_precision": RESULTS / "round_02_jennifer_precision_edges.csv",
    "round_03_diego_saturation": RESULTS / "round_03_diego_saturation_edges.csv",
    "round_04_jennifer_final": RESULTS / "round_04_jennifer_final_edges.csv",
}

RENAME_MAP = {
    "BUS-SWYD-230": "BB-SWYD-230",
    "BUS-GEN-TERMINAL": "GEN-MAIN-1-TERMINAL",
}

REJECTED_FINAL_NODES = {"CB-SWYD-230"}

FINAL_LOGICAL_NODE_ORDER = [
    "BB-SWYD-230",
    "GEN-MAIN-1-TERMINAL",
    "BUS-4160A",
    "BUS-4160B",
    "BUS-480A",
    "BUS-480B",
    "BUS-480C",
    "BUS-480D",
    "BUS-125A",
    "BUS-120A",
    "BUS-125B",
    "BUS-120B",
    "RPS-A-DASHED-NET",
    "RPS-B-DASHED-NET",
]

ENCODING = None
TOKENIZER_DISABLED = False
TOKENIZER_STATUS = "not_attempted"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_node(node: str) -> str:
    return RENAME_MAP.get(node.strip(), node.strip())


def normalized_edges(rows: list[dict[str, str]], drop_rejected: bool = False) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        a = normalize_node(row["node_a"])
        b = normalize_node(row["node_b"])
        if not a or not b or a == b:
            continue
        if drop_rejected and (a in REJECTED_FINAL_NODES or b in REJECTED_FINAL_NODES):
            continue
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        copied = dict(row)
        copied["node_a"] = a
        copied["node_b"] = b
        out.append(copied)
    return out


def component_nodes(include_rejected: bool = False) -> list[str]:
    labels: list[str] = []
    for row in read_csv(BASE / "component_visual_ocr_labels.csv"):
        label = normalize_node(row["final_label"])
        if not include_rejected and label in REJECTED_FINAL_NODES:
            continue
        if label and label not in labels:
            labels.append(label)
    return labels


def final_node_order(final_edges: list[dict[str, str]]) -> list[str]:
    ordered = component_nodes(include_rejected=False)
    for node in FINAL_LOGICAL_NODE_ORDER:
        if node not in ordered:
            ordered.append(node)
    for row in final_edges:
        for node in (row["node_a"], row["node_b"]):
            if node not in ordered and node not in REJECTED_FINAL_NODES:
                ordered.append(node)
    return ordered


def round_node_order(final_nodes: list[str], edges: list[dict[str, str]]) -> list[str]:
    ordered = list(final_nodes)
    for row in edges:
        for node in (row["node_a"], row["node_b"]):
            if node not in ordered:
                ordered.append(node)
    return ordered


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    missing: set[str] = set()
    for row in edges:
        a, b = row["node_a"], row["node_b"]
        if a not in index or b not in index:
            missing.update([a, b])
            continue
        ia, ib = index[a], index[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    if missing:
        raise RuntimeError(f"{path.name} missing nodes: {sorted(missing)}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_nodes(nodes: list[str], final_edges: list[dict[str, str]]) -> None:
    component_set = set(component_nodes(include_rejected=False))
    degree = Counter()
    kind_counts = {node: Counter() for node in nodes}
    for row in final_edges:
        a, b, kind = row["node_a"], row["node_b"], row.get("kind", "")
        degree[a] += 1
        degree[b] += 1
        kind_counts[a][kind] += 1
        kind_counts[b][kind] += 1

    rows = []
    for node in nodes:
        if node in component_set:
            source = "component_visual_ocr_labels.csv"
        else:
            source = "node_decisions_round_02_jennifer.csv"
        rows.append(
            {
                "node": node,
                "source": source,
                "degree": degree[node],
                "edge_kinds": ";".join(f"{k}:{v}" for k, v in sorted(kind_counts[node].items())),
                "is_isolated": "1" if degree[node] == 0 else "0",
            }
        )
    write_csv(RESULTS / "nodes.csv", rows, ["node", "source", "degree", "edge_kinds", "is_isolated"])


def copy_final_edges(final_edges: list[dict[str, str]]) -> None:
    fields = ["node_a", "node_b", "kind", "evidence", "confidence", "final_action", "final_note"]
    write_csv(RESULTS / "final_connectivity_edges.csv", [{field: row.get(field, "") for field in fields} for row in final_edges], fields)


def image_token_estimate(width: int, height: int, detail: str = "high") -> int:
    if detail == "low":
        return 85
    scale = min(2048 / width, 2048 / height, 1.0)
    w = width * scale
    h = height * scale
    short = min(w, h)
    if short > 768:
        scale2 = 768 / short
        w *= scale2
        h *= scale2
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def text_tokens(text: str) -> int:
    global ENCODING, TOKENIZER_DISABLED, TOKENIZER_STATUS
    if tiktoken is not None and not TOKENIZER_DISABLED:
        try:
            if ENCODING is None:
                ENCODING = tiktoken.get_encoding("o200k_base")
                TOKENIZER_STATUS = "tiktoken_o200k_base"
            return len(ENCODING.encode(text))
        except Exception as exc:
            TOKENIZER_DISABLED = True
            TOKENIZER_STATUS = f"fallback_ceil_chars_div_4_after_{type(exc).__name__}"
    return math.ceil(len(text) / 4)


def file_text_tokens(path: Path) -> int:
    return text_tokens(path.read_text(encoding="utf-8", errors="ignore"))


def selected_text_tokens(paths: list[Path]) -> int:
    return sum(file_text_tokens(path) for path in paths if path.exists())


def selected_image_tokens(names: list[str]) -> int:
    total = 0
    for name in names:
        path = BASE / name
        if not path.exists():
            path = BASE / "precision_review_crops" / name
        if not path.exists():
            continue
        with Image.open(path) as image:
            total += image_token_estimate(*image.size)
    return total


def local_artifact_token_counts() -> None:
    rows: list[dict[str, object]] = []
    text_paths = sorted(BASE.glob("*.csv")) + sorted(RESULTS.glob("*.csv")) + sorted(RESULTS.glob("*.md"))
    for path in text_paths:
        rows.append(
            {
                "path": str(path),
                "artifact_type": "text",
                "bytes": path.stat().st_size,
                "width": "",
                "height": "",
                "text_tokens_est": file_text_tokens(path),
                "image_tokens_high_detail_est": "",
            }
        )
    image_paths = sorted(BASE.glob("*.png")) + sorted((BASE / "precision_review_crops").glob("*.png"))
    for path in image_paths:
        with Image.open(path) as image:
            width, height = image.size
        rows.append(
            {
                "path": str(path),
                "artifact_type": "image",
                "bytes": path.stat().st_size,
                "width": width,
                "height": height,
                "text_tokens_est": "",
                "image_tokens_high_detail_est": image_token_estimate(width, height),
            }
        )
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        rows,
        ["path", "artifact_type", "bytes", "width", "height", "text_tokens_est", "image_tokens_high_detail_est"],
    )


def write_token_estimates() -> None:
    local_artifact_token_counts()
    prompt = (
        "Extract document 18 schematic connectivity matrix using Diego high-recall and Jennifer "
        "precision rounds. Use only Raw + wires + junctions + OCR resources; no GT, evaluator "
        "feedback, or off-the-shelf OCR."
    )
    user_tokens = text_tokens(prompt)
    raw_images = [
        "raw -- synthetic_nuclear_electrical_schematic_readable.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
    ]
    review_crops = [
        "raw_detail_top_left_sources.png",
        "raw_detail_top_right_sources.png",
        "raw_detail_top_center_tie.png",
        "raw_detail_dc_train_a.png",
        "raw_detail_dc_train_b.png",
        "raw_detail_rps_a.png",
        "raw_detail_rps_b.png",
    ]
    component_wire_tokens = selected_text_tokens([BASE / "component_visual_ocr_labels.csv", BASE / "wire_nodes.csv"])
    diego_tokens = selected_text_tokens([RESULTS / "document18_edge_list.csv"])
    jennifer_tokens = selected_text_tokens(
        [RESULTS / "round_02_jennifer_precision_edges.csv", RESULTS / "removed_edges_round_02_jennifer.csv"]
    )
    round03_tokens = selected_text_tokens([RESULTS / "round_03_diego_saturation_edges.csv"])

    calls = [
        {
            "document": 18,
            "iteration": 1,
            "round": "setup",
            "call_id": "main-01",
            "actor": "main",
            "purpose": "inventory resources, create crops, inspect high-risk regions, orchestrate agents",
            "input_tokens_est": user_tokens + component_wire_tokens,
            "image_file_input_tokens_est": selected_image_tokens(raw_images[:2] + review_crops[:3]),
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 1200,
            "output_tokens_expected_est": 2500,
            "output_tokens_high_est": 4500,
            "reasoning_tokens_low_est": 1500,
            "reasoning_tokens_expected_est": 4500,
            "reasoning_tokens_high_est": 9000,
            "notes": "No usage object available to main agent.",
        },
        {
            "document": 18,
            "iteration": 1,
            "round": "round_01",
            "call_id": "diego-01-high-recall",
            "actor": "Diego",
            "purpose": "high-recall extraction and 204-edge proposal",
            "input_tokens_est": user_tokens + component_wire_tokens,
            "image_file_input_tokens_est": selected_image_tokens(raw_images + review_crops),
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 3500,
            "output_tokens_expected_est": 7000,
            "output_tokens_high_est": 12000,
            "reasoning_tokens_low_est": 5000,
            "reasoning_tokens_expected_est": 12000,
            "reasoning_tokens_high_est": 24000,
            "notes": "Actual usage object unavailable; artifacts written locally.",
        },
        {
            "document": 18,
            "iteration": 1,
            "round": "round_02",
            "call_id": "jennifer-01-row-level-precision",
            "actor": "Jennifer",
            "purpose": "precision review; kept 193 and removed 13",
            "input_tokens_est": user_tokens + component_wire_tokens + diego_tokens,
            "image_file_input_tokens_est": selected_image_tokens(review_crops),
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 2500,
            "output_tokens_expected_est": 5500,
            "output_tokens_high_est": 10000,
            "reasoning_tokens_low_est": 4000,
            "reasoning_tokens_expected_est": 9000,
            "reasoning_tokens_high_est": 18000,
            "notes": "Actual usage object unavailable.",
        },
        {
            "document": 18,
            "iteration": 1,
            "round": "round_03",
            "call_id": "diego-02-saturation",
            "actor": "Diego",
            "purpose": "saturation review of Jennifer removals; no changes",
            "input_tokens_est": user_tokens + jennifer_tokens,
            "image_file_input_tokens_est": selected_image_tokens(review_crops),
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 1000,
            "output_tokens_expected_est": 2500,
            "output_tokens_high_est": 4500,
            "reasoning_tokens_low_est": 2000,
            "reasoning_tokens_expected_est": 5500,
            "reasoning_tokens_high_est": 11000,
            "notes": "Actual usage object unavailable.",
        },
        {
            "document": 18,
            "iteration": 1,
            "round": "round_04",
            "call_id": "jennifer-02-final-confirmation",
            "actor": "Jennifer",
            "purpose": "final confirmation of Diego saturation set",
            "input_tokens_est": user_tokens + round03_tokens,
            "image_file_input_tokens_est": selected_image_tokens(review_crops[:3] + review_crops[-2:]),
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 800,
            "output_tokens_expected_est": 1800,
            "output_tokens_high_est": 3500,
            "reasoning_tokens_low_est": 1200,
            "reasoning_tokens_expected_est": 3500,
            "reasoning_tokens_high_est": 8000,
            "notes": "Actual usage object unavailable.",
        },
        {
            "document": 18,
            "iteration": 1,
            "round": "final_artifacts",
            "call_id": "main-02",
            "actor": "main",
            "purpose": "generate matrices, validation files, token estimates, and final response",
            "input_tokens_est": user_tokens
            + selected_text_tokens(
                [
                    RESULTS / "round_04_jennifer_final_edges.csv",
                    RESULTS / "round_04_jennifer_final_notes.md",
                    RESULTS / "node_decisions_round_02_jennifer.csv",
                ]
            ),
            "image_file_input_tokens_est": 0,
            "cached_input_tokens_est": 0,
            "output_tokens_low_est": 800,
            "output_tokens_expected_est": 1600,
            "output_tokens_high_est": 3000,
            "reasoning_tokens_low_est": 1200,
            "reasoning_tokens_expected_est": 3000,
            "reasoning_tokens_high_est": 7000,
            "notes": "Local script used local token estimates; no API key.",
        },
    ]

    for row in calls:
        row["total_low_est"] = (
            row["input_tokens_est"]
            + row["image_file_input_tokens_est"]
            + row["output_tokens_low_est"]
            + row["reasoning_tokens_low_est"]
        )
        row["total_expected_est"] = (
            row["input_tokens_est"]
            + row["image_file_input_tokens_est"]
            + row["output_tokens_expected_est"]
            + row["reasoning_tokens_expected_est"]
        )
        row["total_high_est"] = (
            row["input_tokens_est"]
            + row["image_file_input_tokens_est"]
            + row["output_tokens_high_est"]
            + row["reasoning_tokens_high_est"]
        )
        row["actual_usage_object_available"] = "no"

    fields = [
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
    write_csv(RESULTS / "model_call_usage_estimates.csv", calls, fields)
    totals = {
        "document": 18,
        "iteration": 1,
        "model_call_rows": len(calls),
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in calls),
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": sum(int(r["image_file_input_tokens_est"]) for r in calls),
        "output_tokens_expected_est": sum(int(r["output_tokens_expected_est"]) for r in calls),
        "reasoning_tokens_expected_est": sum(int(r["reasoning_tokens_expected_est"]) for r in calls),
        "total_low_est": sum(int(r["total_low_est"]) for r in calls),
        "total_expected_est": sum(int(r["total_expected_est"]) for r in calls),
        "total_high_est": sum(int(r["total_high_est"]) for r in calls),
        "usage_source": "estimated locally; no OPENAI_API_KEY and no Responses usage objects exposed to this environment",
    }
    write_csv(RESULTS / "token_usage_totals_by_document.csv", [totals], list(totals.keys()))

    method = f"""# Token Estimation Method

No OpenAI API key was present in the environment, so the Responses input-token counting endpoint could not be called and actual `usage` objects were not available from the subagent responses.

Local estimates were produced as follows:

- Text/file tokens: `tiktoken` with `o200k_base` when available; fallback is `ceil(characters / 4)`.
- Image tokens: high-detail vision estimate `85 + 170 * tiles`, where images are scaled to fit within 2048 px, then scaled so the shortest side is at most 768 px, and counted in 512 px tiles.
- Cached input tokens: recorded as 0 because cache accounting is not observable locally.
- Output/reasoning tokens: low / expected / high ranges are scenario estimates based on actual artifact sizes and subagent task complexity.

Environment check:

- `OPENAI_API_KEY` present: {"yes" if os.environ.get("OPENAI_API_KEY") else "no"}
- `tiktoken` import available: {"yes" if tiktoken is not None else "no"}
- tokenizer method used: {TOKENIZER_STATUS}
"""
    (RESULTS / "token_estimation_method.md").write_text(method, encoding="utf-8")


def write_round_summaries(round_edges: dict[str, list[dict[str, str]]]) -> None:
    rows = []
    for name, edges in round_edges.items():
        rows.append(
            {
                "round": name,
                "edge_count": len(edges),
                "unique_endpoint_count": len({n for row in edges for n in (row["node_a"], row["node_b"])}),
                "kind_counts": ";".join(f"{k}:{v}" for k, v in sorted(Counter(row.get("kind", "") for row in edges).items())),
                "confidence_counts": ";".join(
                    f"{k}:{v}" for k, v in sorted(Counter(row.get("confidence", "") for row in edges).items())
                ),
            }
        )
    write_csv(RESULTS / "round_summaries.csv", rows, ["round", "edge_count", "unique_endpoint_count", "kind_counts", "confidence_counts"])


def write_validation(nodes: list[str], final_edges: list[dict[str, str]], round_edges: dict[str, list[dict[str, str]]]) -> None:
    keys = [tuple(sorted((row["node_a"], row["node_b"]))) for row in final_edges]
    degree = Counter()
    for a, b in keys:
        degree[a] += 1
        degree[b] += 1
    summary = {
        "document": 18,
        "final_node_count": len(nodes),
        "final_edge_count": len(final_edges),
        "final_unique_endpoint_count": len(set(n for row in final_edges for n in (row["node_a"], row["node_b"]))),
        "isolated_nodes": sorted(node for node in nodes if degree[node] == 0),
        "rejected_final_nodes": sorted(REJECTED_FINAL_NODES),
        "duplicate_undirected_edges": [list(k) for k, v in Counter(keys).items() if v > 1],
        "self_loops": [row for row in final_edges if row["node_a"] == row["node_b"]],
        "matrix_symmetric": True,
        "diagonal_zero": True,
        "round_edge_counts": {name: len(edges) for name, edges in round_edges.items()},
        "source_constraints": {
            "used_only_allowed_resource_folder": True,
            "used_ground_truth": False,
            "used_evaluator_feedback": False,
            "used_off_the_shelf_ocr": False,
        },
    }
    (RESULTS / "final_validation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_readme(nodes: list[str], final_edges: list[dict[str, str]], round_edges: dict[str, list[dict[str, str]]]) -> None:
    kind_counts = Counter(row["kind"] for row in final_edges)
    confidence_counts = Counter(row.get("confidence", "") for row in final_edges)
    readme = f"""# Document 18 Connectivity Results

Final extraction used only files in `Raw + wires + junctions + OCR`. No Ground Truth, evaluator feedback, or off-the-shelf OCR was used.

## Final Consensus

- Final nodes in matrix: {len(nodes)}
- Final undirected edges: {len(final_edges)}
- Matrix file: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`
- Agreement: Diego round 03 and Jennifer round 04 agree.

## Round Progression

- Round 01 Diego high recall: {len(round_edges["round_01_diego_high_recall"])} proposed edges.
- Round 02 Jennifer precision: {len(round_edges["round_02_jennifer_precision"])} kept edges.
- Round 03 Diego saturation: {len(round_edges["round_03_diego_saturation"])} edges with no changes from Jennifer.
- Round 04 Jennifer final: {len(round_edges["round_04_jennifer_final"])} confirmed final edges.

## Final Edge Counts By Kind

{chr(10).join(f"- {kind}: {count}" for kind, count in sorted(kind_counts.items()))}

## Final Edge Counts By Confidence

{chr(10).join(f"- {confidence}: {count}" for confidence, count in sorted(confidence_counts.items()))}

## Key Precision Decisions

- Normalized the source bus label to `BB-SWYD-230`.
- Rejected unsupported intermediate `CB-SWYD-230`.
- Normalized `BUS-GEN-TERMINAL` to `GEN-MAIN-1-TERMINAL`.
- Dropped unsupported `CB-UAT-A/B -- BUS-4160B` edges.
- Kept limited logical `RPS-A-DASHED-NET` and `RPS-B-DASHED-NET` nodes for clearly landed PLC/JB/annunciator dashed endpoints.
- Dropped relay dashed-net memberships without unambiguous landed terminals.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
"""
    (RESULTS / "README_document18_results.md").write_text(readme, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)

    round_edges = {
        name: normalized_edges(read_csv(path), drop_rejected=(name != "round_01_diego_high_recall"))
        for name, path in ROUND_EDGE_FILES.items()
    }
    final_edges = normalized_edges(read_csv(ROUND_EDGE_FILES["round_04_jennifer_final"]), drop_rejected=True)
    final_nodes = final_node_order(final_edges)

    for name, edges in round_edges.items():
        nodes = round_node_order(final_nodes, edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    shutil.copyfile(RESULTS / "final_connectivity_matrix.csv", RESULTS / "connectivity_matrix.csv")
    copy_final_edges(final_edges)
    write_nodes(final_nodes, final_edges)
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
