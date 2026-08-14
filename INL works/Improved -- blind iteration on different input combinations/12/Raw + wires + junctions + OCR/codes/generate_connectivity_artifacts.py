import csv
import math
from collections import Counter
from pathlib import Path

from PIL import Image


DOCUMENT = "12"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires + junctions + OCR")
CODES = BASE / "codes"
RESULTS = BASE / "results"

COMPONENTS_CSV = BASE / "component_visual_ocr_labels.csv"
NODE_DECISIONS_CSV = RESULTS / "node_additions_corrections.csv"
DIEGO_EDGES_CSV = RESULTS / "proposed_edges.csv"

ACCEPTED_ADDITIONS = [
    "BUS-4KV-A",
    "BUS-4KV-B",
    "BUS-480-A",
    "BUS-480-B",
    "BUS-480-C",
    "BUS-480-D",
    "DC-BUS-A",
    "DC-BUS-B",
    "BUS-120VAC-ESF",
]

REJECTED_ADDITION_KINDS = {
    "logical_interlock_net",
    "logical_control_net",
    "logical_signal_net",
}


def canon(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def accepted_label_corrections() -> dict[str, str]:
    corrections = {}
    for row in read_csv(NODE_DECISIONS_CSV):
        if row["action"] != "correction":
            continue
        original = row["original_label"]
        proposed = row["proposed_label"]
        if original == "DS-F23" and proposed == "DS-F023":
            continue
        corrections[original] = proposed
    return corrections


def diego_label_corrections() -> dict[str, str]:
    corrections = {}
    for row in read_csv(NODE_DECISIONS_CSV):
        if row["action"] == "correction":
            corrections[row["original_label"]] = row["proposed_label"]
    return corrections


def apply_label(name: str, corrections: dict[str, str]) -> str:
    return corrections.get(name, name)


def component_nodes(corrections: dict[str, str]) -> list[dict[str, str]]:
    rows = []
    for row in read_csv(COMPONENTS_CSV):
        node = apply_label(row["final_label"], corrections)
        rows.append(
            {
                "node": node,
                "node_kind": row["node_kind"],
                "component_type": row["component_type"],
                "source": "component_visual_ocr_labels.csv",
                "evidence": row["evidence_description"],
            }
        )
    return rows


def final_nodes(corrections: dict[str, str]) -> list[dict[str, str]]:
    rows = component_nodes(corrections)
    decisions = {row["proposed_label"]: row for row in read_csv(NODE_DECISIONS_CSV)}
    for node in ACCEPTED_ADDITIONS:
        src = decisions[node]
        rows.append(
            {
                "node": node,
                "node_kind": src["node_kind"],
                "component_type": src["node_kind"],
                "source": "round_02_jennifer_precision_accepted",
                "evidence": src["evidence"],
            }
        )
    seen = {}
    for row in rows:
        if row["node"] in seen:
            raise ValueError(f"duplicate final node: {row['node']}")
        seen[row["node"]] = row
    return sorted(rows, key=lambda row: row["node"])


def diego_round1_nodes(corrections: dict[str, str]) -> list[dict[str, str]]:
    rows = component_nodes(corrections)
    for row in read_csv(NODE_DECISIONS_CSV):
        if row["action"] == "addition":
            rows.append(
                {
                    "node": row["proposed_label"],
                    "node_kind": row["node_kind"],
                    "component_type": row["node_kind"],
                    "source": "diego_round_01_high_recall",
                    "evidence": row["evidence"],
                }
            )
    seen = {}
    for row in rows:
        if row["node"] in seen:
            raise ValueError(f"duplicate Diego node: {row['node']}")
        seen[row["node"]] = row
    return sorted(rows, key=lambda row: row["node"])


def load_diego_edges(corrections: dict[str, str]) -> list[dict[str, str]]:
    rows = []
    seen = set()
    for row in read_csv(DIEGO_EDGES_CSV):
        a = apply_label(row["node_a"], corrections)
        b = apply_label(row["node_b"], corrections)
        key = canon(a, b)
        if key in seen:
            raise ValueError(f"duplicate edge after corrections: {a} -- {b}")
        seen.add(key)
        rows.append(
            {
                "node_a": a,
                "node_b": b,
                "edge_kind": row["kind"],
                "confidence": row["confidence"],
                "evidence": row["evidence"],
            }
        )
    return rows


def final_edges_from_diego(diego_edges: list[dict[str, str]]) -> list[dict[str, str]]:
    # Jennifer precision: keep Diego rows 1-142, 146-147, 192, and 214-217.
    keep_1_based = set(range(1, 143)) | {146, 147, 192, 214, 215, 216, 217}
    final = []
    for idx, row in enumerate(diego_edges, start=1):
        if idx not in keep_1_based:
            continue
        if row["edge_kind"] == "interlock":
            raise ValueError(f"interlock edge unexpectedly retained at row {idx}: {row}")
        final.append(
            {
                **row,
                "node_a": "DS-F23" if row["node_a"] == "DS-F023" else row["node_a"],
                "node_b": "DS-F23" if row["node_b"] == "DS-F023" else row["node_b"],
            }
        )
    if len(final) != 149:
        raise ValueError(f"expected 149 final edges, got {len(final)}")
    return final


def assert_edges_valid(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    names = {row["node"] for row in nodes}
    missing = sorted({n for e in edges for n in (e["node_a"], e["node_b"]) if n not in names})
    if missing:
        raise ValueError(f"edge endpoint(s) missing from node list: {missing}")


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    write_csv(path, edges, ["node_a", "node_b", "edge_kind", "confidence", "evidence"])


def write_matrix(path: Path, node_names: list[str], edges: list[dict[str, str]]) -> None:
    idx = {name: i for i, name in enumerate(node_names)}
    matrix = [[0 for _ in node_names] for _ in node_names]
    for e in edges:
        i = idx[e["node_a"]]
        j = idx[e["node_b"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + node_names)
        for name, row in zip(node_names, matrix):
            writer.writerow([name] + row)


def image_tokens_high_detail(path: Path) -> int:
    with Image.open(path) as im:
        w, h = im.size
    scale = min(2048 / max(w, h), 1.0)
    w2, h2 = w * scale, h * scale
    shortest = min(w2, h2)
    if shortest > 768:
        scale2 = 768 / shortest
        w2, h2 = w2 * scale2, h2 * scale2
    return 85 + 170 * math.ceil(w2 / 512) * math.ceil(h2 / 512)


def text_tokens_est(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def file_text_tokens(path: Path) -> int:
    return text_tokens_est(path.read_text(encoding="utf-8", errors="replace"))


def write_local_artifact_token_counts() -> None:
    rows = []
    for path in sorted(BASE.glob("*.csv")) + sorted(RESULTS.glob("*.csv")) + sorted(RESULTS.glob("*.md")) + sorted(RESULTS.glob("*.txt")) + sorted(CODES.glob("*.py")):
        if path.is_file():
            rows.append(
                {
                    "document": DOCUMENT,
                    "iteration": ITERATION,
                    "artifact": str(path.relative_to(BASE)),
                    "modality": "text",
                    "tokens_est": file_text_tokens(path),
                    "method": "ceil(characters/4)",
                }
            )
    for path in sorted(BASE.glob("*.png")) + sorted(CODES.glob("*.png")):
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "artifact": str(path.relative_to(BASE)),
                "modality": "image",
                "tokens_est": image_tokens_high_detail(path),
                "method": "85 + 170 per 512 tile after OpenAI high-detail scaling",
            }
        )
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        rows,
        ["document", "iteration", "artifact", "modality", "tokens_est", "method"],
    )


def write_model_usage_estimates() -> None:
    full_images = [
        BASE / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png",
        BASE / "wire_nodes_overlay.png",
        BASE / "component_labels_banners_overlay.png",
    ]
    crop_images = list(CODES.glob("crop_raw_*.png")) + list(CODES.glob("contrast_crop_raw_*.png"))
    full_image_tokens = sum(image_tokens_high_detail(p) for p in full_images)
    crop_tokens = sum(image_tokens_high_detail(p) for p in crop_images)
    csv_bundle = file_text_tokens(COMPONENTS_CSV) + file_text_tokens(BASE / "wire_nodes.csv")
    diego_bundle = file_text_tokens(NODE_DECISIONS_CSV) + file_text_tokens(DIEGO_EDGES_CSV)

    calls = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "description": "Inventory document 12 resources, inspect full images, create evidence crops.",
            "input_tokens_est": full_image_tokens + text_tokens_est("document 12 setup prompt"),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens,
            "output_tokens_low": 800,
            "output_tokens_expected": 1500,
            "output_tokens_high": 3000,
            "reasoning_tokens_low": 1400,
            "reasoning_tokens_expected": 4200,
            "reasoning_tokens_high": 8500,
        },
        {
            "call_id": "subagent-01",
            "round": "01",
            "agent": "Diego",
            "description": "High-recall extraction from raw/overlays/crops.",
            "input_tokens_est": full_image_tokens + crop_tokens + csv_bundle,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens + crop_tokens,
            "output_tokens_low": 5200,
            "output_tokens_expected": 8500,
            "output_tokens_high": 13000,
            "reasoning_tokens_low": 7500,
            "reasoning_tokens_expected": 14000,
            "reasoning_tokens_high": 23000,
        },
        {
            "call_id": "subagent-02",
            "round": "01",
            "agent": "Jennifer",
            "description": "Independent precision orientation from raw/overlays/crops.",
            "input_tokens_est": full_image_tokens + crop_tokens + csv_bundle,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens + crop_tokens,
            "output_tokens_low": 900,
            "output_tokens_expected": 1700,
            "output_tokens_high": 3200,
            "reasoning_tokens_low": 3000,
            "reasoning_tokens_expected": 7000,
            "reasoning_tokens_high": 13000,
        },
        {
            "call_id": "subagent-03",
            "round": "02",
            "agent": "Jennifer",
            "description": "Precision review of Diego high-recall proposal.",
            "input_tokens_est": diego_bundle + 1200,
            "cached_input_tokens_est": full_image_tokens + crop_tokens,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 1500,
            "output_tokens_expected": 2800,
            "output_tokens_high": 5200,
            "reasoning_tokens_low": 4500,
            "reasoning_tokens_expected": 9500,
            "reasoning_tokens_high": 17000,
        },
        {
            "call_id": "subagent-04",
            "round": "03",
            "agent": "Diego",
            "description": "Saturation check against Jennifer precision result.",
            "input_tokens_est": 1300,
            "cached_input_tokens_est": full_image_tokens + crop_tokens + diego_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 400,
            "output_tokens_expected": 800,
            "output_tokens_high": 1800,
            "reasoning_tokens_low": 1200,
            "reasoning_tokens_expected": 3200,
            "reasoning_tokens_high": 6500,
        },
        {
            "call_id": "subagent-05",
            "round": "04",
            "agent": "Jennifer",
            "description": "Final confirmation of saturated result.",
            "input_tokens_est": 500,
            "cached_input_tokens_est": full_image_tokens + crop_tokens + diego_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 250,
            "output_tokens_expected": 500,
            "output_tokens_high": 1200,
            "reasoning_tokens_low": 800,
            "reasoning_tokens_expected": 1800,
            "reasoning_tokens_high": 4200,
        },
        {
            "call_id": "main-02",
            "round": "artifact",
            "agent": "Main",
            "description": "Generate round matrices, validate final matrix, summarize usage.",
            "input_tokens_est": diego_bundle + file_text_tokens(CODES / "generate_connectivity_artifacts.py"),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 700,
            "output_tokens_expected": 1300,
            "output_tokens_high": 2600,
            "reasoning_tokens_low": 1400,
            "reasoning_tokens_expected": 3600,
            "reasoning_tokens_high": 7500,
        },
    ]
    for call in calls:
        call["total_tokens_low"] = call["input_tokens_est"] + call["output_tokens_low"] + call["reasoning_tokens_low"]
        call["total_tokens_expected"] = call["input_tokens_est"] + call["output_tokens_expected"] + call["reasoning_tokens_expected"]
        call["total_tokens_high"] = call["input_tokens_est"] + call["output_tokens_high"] + call["reasoning_tokens_high"]
    rows = []
    for call in calls:
        row = {"document": DOCUMENT, "iteration": ITERATION, "usage_object_available": "no"}
        row.update(call)
        rows.append(row)
    fields = [
        "document",
        "iteration",
        "call_id",
        "round",
        "agent",
        "description",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_object_available",
    ]
    write_csv(RESULTS / "model_call_usage_estimates.csv", rows, fields)
    totals = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "api_key_available": "no",
        "responses_token_count_endpoint_used": "no_api_key",
        "usage_objects_collected": "not_exposed_by_multi_agent_tool",
        "model_calls_counted": len(rows),
        "total_tokens_low": sum(row["total_tokens_low"] for row in rows),
        "total_tokens_expected": sum(row["total_tokens_expected"] for row in rows),
        "total_tokens_high": sum(row["total_tokens_high"] for row in rows),
        "method": "Local estimate: chars/4 for text plus OpenAI-style high-detail image tile estimate; low/expected/high bands for unknown output and reasoning.",
    }
    write_csv(
        RESULTS / "token_usage_totals_by_document.csv",
        [totals],
        [
            "document",
            "iteration",
            "api_key_available",
            "responses_token_count_endpoint_used",
            "usage_objects_collected",
            "model_calls_counted",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
            "method",
        ],
    )


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    final_corrections = accepted_label_corrections()
    r1_corrections = diego_label_corrections()
    r1_nodes = diego_round1_nodes(r1_corrections)
    final_node_rows = final_nodes(final_corrections)
    r1_edges = load_diego_edges(r1_corrections)
    final_edge_rows = final_edges_from_diego(r1_edges)
    assert_edges_valid(r1_nodes, r1_edges)
    assert_edges_valid(final_node_rows, final_edge_rows)

    r1_node_names = [row["node"] for row in r1_nodes]
    final_node_names = [row["node"] for row in final_node_rows]

    write_csv(RESULTS / "nodes.csv", final_node_rows, ["node", "node_kind", "component_type", "source", "evidence"])
    write_csv(RESULTS / "round_01_diego_high_recall_nodes.csv", r1_nodes, ["node", "node_kind", "component_type", "source", "evidence"])

    rounds = [
        ("01", "Diego", "round_01_diego_high_recall", r1_node_names, r1_edges, "High-recall proposal; includes abstract logical net nodes."),
        ("02", "Jennifer", "round_02_jennifer_precision", final_node_names, final_edge_rows, "Precision review removed abstract net nodes/edges and kept locally landed dashed/dotted edges only."),
        ("03", "Diego", "round_03_diego_saturation", final_node_names, final_edge_rows, "Diego saturation check accepted Jennifer result."),
        ("04", "Jennifer", "round_04_jennifer_final", final_node_names, final_edge_rows, "Final Jennifer confirmation of saturated result."),
    ]
    summaries = []
    prev = None
    for round_no, agent, basename, names, edges, notes in rounds:
        write_edges(RESULTS / f"{basename}_edges.csv", edges)
        write_matrix(RESULTS / f"{basename}_matrix.csv", names, edges)
        summaries.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": round_no,
                "agent": agent,
                "interpretation": basename,
                "node_count": len(names),
                "edge_count": len(edges),
                "delta_edges_from_previous_round": "" if prev is None else len(edges) - prev,
                "edge_kind_counts": "; ".join(f"{k}:{v}" for k, v in sorted(Counter(e["edge_kind"] for e in edges).items())),
                "notes": notes,
            }
        )
        prev = len(edges)

    write_edges(RESULTS / "final_connectivity_edges.csv", final_edge_rows)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_node_names, final_edge_rows)
    write_csv(
        RESULTS / "round_summaries.csv",
        summaries,
        [
            "document",
            "iteration",
            "round",
            "agent",
            "interpretation",
            "node_count",
            "edge_count",
            "delta_edges_from_previous_round",
            "edge_kind_counts",
            "notes",
        ],
    )

    node_decisions = []
    for row in read_csv(NODE_DECISIONS_CSV):
        original = row["original_label"]
        proposed = row["proposed_label"]
        if row["action"] == "addition":
            status = "accepted_final_node" if proposed in ACCEPTED_ADDITIONS else "rejected_abstract_net"
            reason = "Accepted visible named bus." if proposed in ACCEPTED_ADDITIONS else "Abstract logical net rejected by Jennifer precision review."
        else:
            accepted = original != "DS-F23" or proposed != "DS-F023"
            status = "accepted_label_correction" if accepted else "rejected_label_correction"
            reason = "Accepted visually supported label correction." if accepted else "Keep visible DS-F23; leading zero was pattern inference."
        node_decisions.append(
            {
                "action": row["action"],
                "stable_node_id": row["stable_node_id"],
                "original_label": original,
                "proposed_label": proposed,
                "node_kind": row["node_kind"],
                "final_status": status,
                "reason": reason,
            }
        )
    write_csv(
        RESULTS / "node_addition_correction_decisions.csv",
        node_decisions,
        ["action", "stable_node_id", "original_label", "proposed_label", "node_kind", "final_status", "reason"],
    )

    final_keys = {canon(e["node_a"], e["node_b"]) for e in final_edge_rows}
    rejected = []
    for idx, e in enumerate(r1_edges, start=1):
        if canon(e["node_a"], e["node_b"]) not in final_keys:
            rejected.append(
                {
                    "round1_row": idx,
                    "node_a": e["node_a"],
                    "node_b": e["node_b"],
                    "original_edge_kind": e["edge_kind"],
                    "original_confidence": e["confidence"],
                    "final_status": "excluded",
                    "reason": "Removed by Jennifer precision review; abstract net/unclear dashed-dotted route or not locally landed.",
                }
            )
    write_csv(
        RESULTS / "rejected_or_uncertain_edges.csv",
        rejected,
        ["round1_row", "node_a", "node_b", "original_edge_kind", "original_confidence", "final_status", "reason"],
    )

    write_local_artifact_token_counts()
    write_model_usage_estimates()

    readme = """# Document 12 Connectivity Extraction

Blind extraction using only resources in `Raw + wires + junctions + OCR`.

- Base component labels: 151
- Accepted added nodes: 9
- Accepted label corrections: 23
- Final nodes: 160
- Diego round 1 high-recall nodes/edges: 168 / 217
- Final saturated precision edges: 149
- Final matrix: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
Token counts are local estimates because no API key / Responses token-count endpoint was available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")
    print(
        f"round1_nodes={len(r1_node_names)} round1_edges={len(r1_edges)} "
        f"final_nodes={len(final_node_names)} final_edges={len(final_edge_rows)} "
        f"kind_counts={dict(Counter(e['edge_kind'] for e in final_edge_rows))}"
    )


if __name__ == "__main__":
    main()
