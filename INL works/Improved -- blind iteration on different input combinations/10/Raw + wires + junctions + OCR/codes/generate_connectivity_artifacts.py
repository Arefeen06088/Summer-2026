import csv
import math
from collections import Counter
from pathlib import Path

from PIL import Image


DOCUMENT = "10"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw + wires + junctions + OCR")
RESULTS = BASE / "results"
CODES = BASE / "codes"

COMPONENTS_CSV = BASE / "component_visual_ocr_labels.csv"
NODE_ADDITIONS_CSV = BASE / "diego_doc10_node_additions.csv"
DIEGO_R1_EDGES_CSV = BASE / "diego_doc10_edges.csv"
DIEGO_R3_EDGES_CSV = BASE / "diego_doc10_edges_saturated_r3.csv"

REMOVED_EDGES = {
    ("PNL-UPS-A", "HTR-TRACE-A"),
    ("PNL-UPS-B", "HTR-TRACE-B"),
    ("MCC-102A", "FAN-AB-A"),
    ("MCC-102B", "FAN-AB-B"),
    ("480V-LC-FEEDERS-A", "FUSE-A01"),
    ("480V-LC-FEEDERS-A", "FUSE-A02"),
    ("480V-LC-FEEDERS-B", "FUSE-B01"),
    ("480V-LC-FEEDERS-B", "FUSE-B02"),
    ("480V-LC-FEEDERS-A", "RECT-1A"),
    ("480V-LC-FEEDERS-B", "RECT-1B"),
    ("GND-A", "BUS-DC-A"),
    ("GND-A", "PNL-UPS-A"),
    ("GND-B", "BUS-DC-B"),
    ("GND-B", "PNL-UPS-B"),
    ("CT-4160-A", "FUSE-A01"),
    ("CT-4160-B", "FUSE-B01"),
    ("CT-CAB-A-CONTROL-CABLE-TRAY", "JB-CONTROL"),
    ("CT-CAB-B-CONTROL-CABLE-TRAY", "JB-CONTROL"),
    ("CT-CAB-A-CONTROL-CABLE-TRAY", "PNL-MCR-01"),
    ("CT-CAB-B-CONTROL-CABLE-TRAY", "PNL-MCR-01"),
    ("CT-CAB-A-CONTROL-CABLE-TRAY", "PNL-ANN-01"),
    ("CT-CAB-B-CONTROL-CABLE-TRAY", "PNL-ANN-01"),
    ("CT-CAB-A-CONTROL-CABLE-TRAY", "SER-01"),
    ("CT-CAB-B-CONTROL-CABLE-TRAY", "SER-01"),
}


def canon(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_nodes() -> list[dict[str, str]]:
    nodes: list[dict[str, str]] = []
    for row in read_csv(COMPONENTS_CSV):
        nodes.append(
            {
                "node": row["final_label"],
                "node_kind": row["node_kind"],
                "component_type": row["component_type"],
                "source": "component_visual_ocr_labels.csv",
                "evidence": row["evidence_description"],
            }
        )
    for row in read_csv(NODE_ADDITIONS_CSV):
        nodes.append(
            {
                "node": row["node_label"],
                "node_kind": row["node_kind"],
                "component_type": row["node_kind"],
                "source": "diego_round_1_jennifer_accepted",
                "evidence": row["reason"],
            }
        )
    seen = {}
    for row in nodes:
        if row["node"] in seen:
            raise ValueError(f"duplicate node label: {row['node']}")
        seen[row["node"]] = row
    return sorted(nodes, key=lambda row: row["node"])


def load_edges(path: Path) -> list[dict[str, str]]:
    edges = []
    seen = set()
    for row in read_csv(path):
        a = row["node_a"]
        b = row["node_b"]
        key = canon(a, b)
        if a == b:
            raise ValueError(f"self-loop not expected: {a}")
        if key in seen:
            raise ValueError(f"duplicate edge: {a} -- {b}")
        seen.add(key)
        edges.append(
            {
                "node_a": a,
                "node_b": b,
                "edge_kind": row["kind"],
                "confidence": row["confidence"],
                "evidence": row["evidence"],
            }
        )
    return edges


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
    for edge in edges:
        i = idx[edge["node_a"]]
        j = idx[edge["node_b"]]
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
    for path in sorted(BASE.glob("*.csv")) + sorted(BASE.glob("*.md")):
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
    for path in sorted(CODES.glob("*.py")):
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
        BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png",
        BASE / "wire_nodes_overlay.png",
        BASE / "component_labels_banners_overlay.png",
    ]
    crop_images = list(CODES.glob("crop_raw_*.png")) + list(CODES.glob("contrast_crop_raw_*.png"))
    full_image_tokens = sum(image_tokens_high_detail(p) for p in full_images)
    crop_token_bundle = sum(image_tokens_high_detail(p) for p in crop_images)
    csv_bundle = sum(
        file_text_tokens(p)
        for p in (COMPONENTS_CSV, BASE / "wire_nodes.csv", NODE_ADDITIONS_CSV, DIEGO_R1_EDGES_CSV)
        if p.exists()
    )

    calls = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "description": "Inventory resources, inspect source images, create evidence crops.",
            "input_tokens_est": full_image_tokens + text_tokens_est("document 10 setup prompt"),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens,
            "output_tokens_low": 700,
            "output_tokens_expected": 1400,
            "output_tokens_high": 2600,
            "reasoning_tokens_low": 1200,
            "reasoning_tokens_expected": 3600,
            "reasoning_tokens_high": 7200,
        },
        {
            "call_id": "subagent-01",
            "round": "01",
            "agent": "Diego",
            "description": "High-recall extraction from raw/overlays/crops.",
            "input_tokens_est": full_image_tokens + crop_token_bundle + csv_bundle,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens + crop_token_bundle,
            "output_tokens_low": 3800,
            "output_tokens_expected": 6200,
            "output_tokens_high": 9600,
            "reasoning_tokens_low": 6000,
            "reasoning_tokens_expected": 11000,
            "reasoning_tokens_high": 18000,
        },
        {
            "call_id": "subagent-02",
            "round": "01",
            "agent": "Jennifer",
            "description": "Independent precision orientation from raw/overlays/crops.",
            "input_tokens_est": full_image_tokens + crop_token_bundle + file_text_tokens(COMPONENTS_CSV),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens + crop_token_bundle,
            "output_tokens_low": 800,
            "output_tokens_expected": 1600,
            "output_tokens_high": 2800,
            "reasoning_tokens_low": 2500,
            "reasoning_tokens_expected": 6000,
            "reasoning_tokens_high": 11000,
        },
        {
            "call_id": "subagent-03",
            "round": "02",
            "agent": "Jennifer",
            "description": "Precision review of Diego round 1 proposal.",
            "input_tokens_est": file_text_tokens(DIEGO_R1_EDGES_CSV) + file_text_tokens(NODE_ADDITIONS_CSV) + 900,
            "cached_input_tokens_est": full_image_tokens + crop_token_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 900,
            "output_tokens_expected": 1800,
            "output_tokens_high": 3400,
            "reasoning_tokens_low": 3000,
            "reasoning_tokens_expected": 7000,
            "reasoning_tokens_high": 13000,
        },
        {
            "call_id": "subagent-04",
            "round": "03",
            "agent": "Diego",
            "description": "Saturation check against Jennifer removals.",
            "input_tokens_est": 1200 + file_text_tokens(DIEGO_R1_EDGES_CSV),
            "cached_input_tokens_est": full_image_tokens + crop_token_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1800,
            "reasoning_tokens_low": 1500,
            "reasoning_tokens_expected": 3500,
            "reasoning_tokens_high": 7000,
        },
        {
            "call_id": "subagent-05",
            "round": "04",
            "agent": "Jennifer",
            "description": "Final confirmation of saturated result.",
            "input_tokens_est": 350,
            "cached_input_tokens_est": full_image_tokens + crop_token_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 250,
            "output_tokens_expected": 500,
            "output_tokens_high": 1100,
            "reasoning_tokens_low": 800,
            "reasoning_tokens_expected": 1800,
            "reasoning_tokens_high": 4000,
        },
        {
            "call_id": "main-02",
            "round": "artifact",
            "agent": "Main",
            "description": "Generate round matrices, validate final matrix, summarize usage.",
            "input_tokens_est": 1200 + file_text_tokens(DIEGO_R3_EDGES_CSV),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 600,
            "output_tokens_expected": 1200,
            "output_tokens_high": 2400,
            "reasoning_tokens_low": 1200,
            "reasoning_tokens_expected": 3200,
            "reasoning_tokens_high": 6500,
        },
    ]
    for call in calls:
        call["total_tokens_low"] = (
            call["input_tokens_est"] + call["output_tokens_low"] + call["reasoning_tokens_low"]
        )
        call["total_tokens_expected"] = (
            call["input_tokens_est"] + call["output_tokens_expected"] + call["reasoning_tokens_expected"]
        )
        call["total_tokens_high"] = (
            call["input_tokens_est"] + call["output_tokens_high"] + call["reasoning_tokens_high"]
        )

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
    rows = []
    for call in calls:
        row = {"document": DOCUMENT, "iteration": ITERATION, "usage_object_available": "no"}
        row.update(call)
        rows.append(row)
    write_csv(RESULTS / "model_call_usage_estimates.csv", rows, fields)

    totals = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "api_key_available": "no",
        "responses_token_count_endpoint_used": "no_api_key",
        "usage_objects_collected": "not_exposed_by_multi_agent_tool",
        "model_calls_counted": len(calls),
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
    nodes = load_nodes()
    node_names = [row["node"] for row in nodes]
    write_csv(RESULTS / "nodes.csv", nodes, ["node", "node_kind", "component_type", "source", "evidence"])

    r1_edges = load_edges(DIEGO_R1_EDGES_CSV)
    r3_edges = load_edges(DIEGO_R3_EDGES_CSV)
    r2_edges = r3_edges
    r4_edges = r3_edges
    for edge_list in (r1_edges, r2_edges, r3_edges, r4_edges):
        assert_edges_valid(nodes, edge_list)

    rounds = [
        ("01", "Diego", "round_01_diego_high_recall", r1_edges, "High-recall broad proposal; included medium/low candidates."),
        ("02", "Jennifer", "round_02_jennifer_precision", r2_edges, "Precision review removed 24 unsupported or overconnected edges."),
        ("03", "Diego", "round_03_diego_saturation", r3_edges, "Diego accepted Jennifer removals and restored none."),
        ("04", "Jennifer", "round_04_jennifer_final", r4_edges, "Final confirmation of saturated precision result."),
    ]

    for _, _, basename, edges, _ in rounds:
        write_edges(RESULTS / f"{basename}_edges.csv", edges)
        write_matrix(RESULTS / f"{basename}_matrix.csv", node_names, edges)
    write_edges(RESULTS / "final_connectivity_edges.csv", r4_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", node_names, r4_edges)

    removed_rows = []
    r1_by_key = {canon(e["node_a"], e["node_b"]): e for e in r1_edges}
    for a, b in sorted(REMOVED_EDGES):
        edge = r1_by_key[canon(a, b)]
        reason = "Removed by Jennifer precision review; Diego accepted removal in saturation."
        removed_rows.append(
            {
                "node_a": a,
                "node_b": b,
                "original_edge_kind": edge["edge_kind"],
                "original_confidence": edge["confidence"],
                "final_status": "excluded",
                "reason": reason,
            }
        )
    write_csv(
        RESULTS / "rejected_or_uncertain_edges.csv",
        removed_rows,
        ["node_a", "node_b", "original_edge_kind", "original_confidence", "final_status", "reason"],
    )

    node_additions = read_csv(NODE_ADDITIONS_CSV)
    write_csv(RESULTS / "node_additions.csv", node_additions, list(node_additions[0].keys()))

    summaries = []
    prev_count = None
    for round_no, agent, basename, edges, notes in rounds:
        count = len(edges)
        summaries.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": round_no,
                "agent": agent,
                "interpretation": basename,
                "node_count": len(node_names),
                "edge_count": count,
                "delta_edges_from_previous_round": "" if prev_count is None else count - prev_count,
                "edge_kind_counts": "; ".join(f"{k}:{v}" for k, v in sorted(Counter(e["edge_kind"] for e in edges).items())),
                "notes": notes,
            }
        )
        prev_count = count
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

    write_local_artifact_token_counts()
    write_model_usage_estimates()

    readme = """# Document 10 Connectivity Extraction

Blind extraction using only resources in `Raw + wires + junctions + OCR`.

- Base component labels: 109
- Accepted added nodes: 13
- Final nodes: 122
- Diego round 1 high-recall edges: 157
- Jennifer precision / final saturated edges: 133
- Final matrix: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
Token counts are local estimates because no API key / Responses token-count endpoint was available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")
    print(
        f"nodes={len(node_names)} final_edges={len(r4_edges)} "
        f"kind_counts={dict(Counter(e['edge_kind'] for e in r4_edges))}"
    )


if __name__ == "__main__":
    main()
