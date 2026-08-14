import csv
import json
import math
import shutil
from pathlib import Path

from PIL import Image


DOC = "11"
ITERATION = "1"
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + components")
RESULTS = ROOT / "results"
CODES = ROOT / "codes"
LOCAL_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\results")


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def write_edges_csv(path, edges):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "evidence", "kind"])
        writer.writerows(edges)


def matrix_from_edges(nodes, edges):
    index = {name: i for i, name in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in edges:
        a, b = edge[0], edge[1]
        if a not in index or b not in index:
            raise ValueError(f"Edge references unknown node: {a!r}, {b!r}")
        if a == b:
            raise ValueError(f"Unexpected self-loop: {a!r}")
        ia, ib = index[a], index[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    return matrix


def write_matrix_csv(path, nodes, edges):
    matrix = matrix_from_edges(nodes, edges)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)
    return matrix


def validate_matrix(nodes, edges, matrix):
    if len(matrix) != len(nodes):
        raise ValueError("Matrix row count does not match nodes")
    for i, row in enumerate(matrix):
        if len(row) != len(nodes):
            raise ValueError(f"Matrix column count mismatch at row {i}")
        if row[i] != 0:
            raise ValueError(f"Diagonal must be zero at {nodes[i]}")
        for j in range(len(nodes)):
            if row[j] not in (0, 1):
                raise ValueError("Matrix must be binary")
            if row[j] != matrix[j][i]:
                raise ValueError(f"Matrix not symmetric at {i},{j}")
    undirected_count = sum(sum(row) for row in matrix) // 2
    unique_edges = {tuple(sorted((edge[0], edge[1]))) for edge in edges}
    if undirected_count != len(unique_edges):
        raise ValueError(f"Matrix edge count {undirected_count} != unique edge count {len(unique_edges)}")
    return undirected_count


def canonicalize_edges(edges):
    seen = set()
    out = []
    for edge in edges:
        a, b, evidence, kind = edge
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        out.append([a, b, evidence, kind])
    return out


def text_tokens(text):
    return math.ceil(len(text) / 4)


def image_tokens_high_detail(path):
    # Fallback estimate matching the common high-detail 512-tile method:
    # fit within 2048x2048, scale shortest side to 768 when larger, then
    # charge 85 base + 170 per 512px tile. This is only an estimate.
    with Image.open(path) as img:
        width, height = img.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width2, height2 = width * scale, height * scale
    shortest = min(width2, height2)
    if shortest > 768:
        scale2 = 768 / shortest
        width2, height2 = width2 * scale2, height2 * scale2
    tiles = math.ceil(width2 / 512) * math.ceil(height2 / 512)
    return 85 + 170 * tiles


def image_total(paths):
    return sum(image_tokens_high_detail(path) for path in paths)


def write_token_estimates(rounds):
    raw = ROOT / "raw -- synthetic_npp_electrical_schematic_relocated_names.png"
    overlay = ROOT / "detected_components_and_logical_overlay.png"
    R = RESULTS
    diego_r1_images = [
        raw,
        overlay,
        R / "raw_01_top_sources_13kv.png",
        R / "raw_02_train_a_full.png",
        R / "raw_03_train_b_full.png",
        R / "raw_04_train_c_full.png",
        R / "raw_05_train_d_full.png",
        R / "raw_06_bottom_dc_a.png",
        R / "raw_07_bottom_dc_b.png",
        R / "raw_08_cross_train_controls.png",
        R / "raw_09_train_a_label_zoom_2x.png",
        R / "raw_10_train_b_label_zoom_2x.png",
        R / "raw_11_train_c_label_zoom_2x.png",
        R / "raw_12_train_d_label_zoom_2x.png",
        R / "raw_13_dc_a_label_zoom_2x.png",
        R / "raw_14_dc_b_label_zoom_2x.png",
    ]
    jennifer_r1_images = diego_r1_images
    diego_r2_images = [
        raw,
        overlay,
        R / "raw_01_top_sources_13kv.png",
        R / "raw_02_train_a_full.png",
        R / "raw_03_train_b_full.png",
        R / "raw_04_train_c_full.png",
        R / "raw_05_train_d_full.png",
        R / "raw_06_bottom_dc_a.png",
        R / "raw_07_bottom_dc_b.png",
        R / "raw_08_cross_train_controls.png",
        R / "raw_13_dc_a_label_zoom_2x.png",
        R / "raw_14_dc_b_label_zoom_2x.png",
    ]
    jennifer_r2_images = [
        raw,
        R / "raw_01_top_sources_13kv.png",
        R / "raw_02_train_a_full.png",
        R / "raw_03_train_b_full.png",
        R / "raw_04_train_c_full.png",
        R / "raw_05_train_d_full.png",
        R / "raw_06_bottom_dc_a.png",
        R / "raw_07_bottom_dc_b.png",
        R / "raw_08_cross_train_controls.png",
    ]
    main_images = [
        raw,
        overlay,
        R / "raw_01_top_sources_13kv.png",
        R / "overlay_01_top_sources_13kv.png",
        R / "raw_02_train_a_full.png",
        R / "raw_03_train_b_full.png",
        R / "raw_04_train_c_full.png",
        R / "raw_05_train_d_full.png",
        R / "raw_06_bottom_dc_a.png",
        R / "raw_07_bottom_dc_b.png",
        R / "raw_08_cross_train_controls.png",
        R / "raw_13_dc_a_label_zoom_2x.png",
        R / "raw_14_dc_b_label_zoom_2x.png",
    ]

    diego_prompt = "Diego high-recall extractor prompt with raw/overlay/crops and CSV/edge-list output schema."
    jennifer_prompt = "Jennifer precision reviewer prompt, Diego node/edge summary, high-risk edge list, raw/overlay/crops, and CSV output schema."
    diego_r2_prompt = "Diego round-2 reconciliation prompt containing Jennifer decisions and focused raw/overlay/crops."
    jennifer_r2_prompt = "Jennifer final confirmation prompt containing converged node/edge decisions and focused raw/crops."
    main_prompt = "Main Codex orchestration for document 11, file inspection, crop review, subagent coordination, result writing, and validation."

    # Expected visible output estimates use actual generated artifact/prose sizes where available.
    diego_r1_visible = text_tokens((LOCAL_RESULTS / "doc11_round1_diego_connectivity_proposal.json").read_text(encoding="utf-8"))
    jennifer_r1_visible = text_tokens((LOCAL_RESULTS / "doc11_round1_jennifer_edges.json").read_text(encoding="utf-8")) + 2000
    diego_r2_visible = text_tokens((LOCAL_RESULTS / "doc11_round2_diego_connectivity_proposal.json").read_text(encoding="utf-8"))
    jennifer_r2_visible = 260
    main_visible = 3000

    calls = [
        {
            "call_id": "main-aggregate-doc11",
            "agent": "Main Codex",
            "round": "orchestration",
            "model": "gpt-5",
            "purpose": "Inspect resources, create crops, coordinate subagents, write/validate outputs.",
            "text_prompt": main_prompt,
            "images": main_images,
            "visible_output_expected": main_visible,
            "reasoning_expected": 12000,
            "notes": "Aggregated because individual main-agent model-call usage is not exposed by this runtime.",
        },
        {
            "call_id": "diego-r1",
            "agent": "Diego",
            "round": "1",
            "model": "gpt-5.5 xhigh",
            "purpose": "High-recall extraction proposal.",
            "text_prompt": diego_prompt,
            "images": diego_r1_images,
            "visible_output_expected": diego_r1_visible,
            "reasoning_expected": 18000,
            "notes": "Usage object not exposed; output estimated from generated JSON.",
        },
        {
            "call_id": "jennifer-r1",
            "agent": "Jennifer",
            "round": "1",
            "model": "gpt-5.5 xhigh",
            "purpose": "Precision review/refinement of Diego round 1.",
            "text_prompt": jennifer_prompt,
            "images": jennifer_r1_images,
            "visible_output_expected": jennifer_r1_visible,
            "reasoning_expected": 18000,
            "notes": "Usage object not exposed; output estimated from generated edge JSON plus matrix/prose overhead.",
        },
        {
            "call_id": "diego-r2",
            "agent": "Diego",
            "round": "2",
            "model": "gpt-5.5 xhigh",
            "purpose": "Reconcile Jennifer changes and confirm convergence.",
            "text_prompt": diego_r2_prompt,
            "images": diego_r2_images,
            "visible_output_expected": diego_r2_visible,
            "reasoning_expected": 10000,
            "notes": "Usage object not exposed; output estimated from generated JSON.",
        },
        {
            "call_id": "jennifer-r2-final",
            "agent": "Jennifer",
            "round": "2",
            "model": "gpt-5.5 xhigh",
            "purpose": "Final precision confirmation.",
            "text_prompt": jennifer_r2_prompt,
            "images": jennifer_r2_images,
            "visible_output_expected": jennifer_r2_visible,
            "reasoning_expected": 6000,
            "notes": "Usage object not exposed; short final confirmation.",
        },
    ]

    rows = []
    for call in calls:
        text_expected = text_tokens(call["text_prompt"])
        image_expected = image_total(call["images"])
        input_expected = text_expected + image_expected
        visible_expected = call["visible_output_expected"]
        reasoning_expected = call["reasoning_expected"]
        total_expected = input_expected + visible_expected + reasoning_expected
        rows.append(
            {
                "document": DOC,
                "iteration": ITERATION,
                "call_id": call["call_id"],
                "agent": call["agent"],
                "round": call["round"],
                "model": call["model"],
                "purpose": call["purpose"],
                "text_input_tokens_low": math.ceil(text_expected * 0.7),
                "text_input_tokens_expected": text_expected,
                "text_input_tokens_high": math.ceil(text_expected * 1.3),
                "cached_input_tokens": "not_exposed_assumed_0",
                "image_count": len(call["images"]),
                "image_file_input_tokens_low": math.ceil(image_expected * 0.6),
                "image_file_input_tokens_expected": image_expected,
                "image_file_input_tokens_high": math.ceil(image_expected * 1.5),
                "input_tokens_low": math.ceil(input_expected * 0.65),
                "input_tokens_expected": input_expected,
                "input_tokens_high": math.ceil(input_expected * 1.45),
                "visible_output_tokens_low": math.ceil(visible_expected * 0.6),
                "visible_output_tokens_expected": visible_expected,
                "visible_output_tokens_high": math.ceil(visible_expected * 1.8),
                "reasoning_tokens_low": math.ceil(reasoning_expected * 0.5),
                "reasoning_tokens_expected": reasoning_expected,
                "reasoning_tokens_high": math.ceil(reasoning_expected * 2.0),
                "total_tokens_low": math.ceil(total_expected * 0.6),
                "total_tokens_expected": total_expected,
                "total_tokens_high": math.ceil(total_expected * 1.8),
                "usage_object_available": "no",
                "usage_source": "fallback_estimate_no_api_key",
                "notes": call["notes"],
            }
        )

    out_csv = RESULTS / "token_usage_estimate.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)
    input_expected_total = sum(int(row["input_tokens_expected"]) for row in rows)
    image_expected_total = sum(int(row["image_file_input_tokens_expected"]) for row in rows)

    md = [
        "# Document 11 Token Usage Estimate",
        "",
        "No OpenAI API key was present, and the Codex/subagent runtime did not expose response usage objects. The official Responses input-token counting endpoint could therefore not be called.",
        "",
        "Fallback method: text tokens are estimated as ceil(characters / 4). Image/file input tokens are estimated with a high-detail 512-tile method (fit within 2048 px, shortest side 768 px when larger, 85 base + 170 per tile). Low/high ranges apply multipliers around that expected value.",
        "",
        f"- Total expected input tokens: {input_expected_total}",
        f"- Total expected image/file input tokens: {image_expected_total}",
        f"- Total low / expected / high tokens including estimated visible output and reasoning: {total_low} / {total_expected} / {total_high}",
        "",
        "| Document | Iteration | Calls | Total Low | Total Expected | Total High |",
        "|---|---:|---:|---:|---:|---:|",
        f"| {DOC} | {ITERATION} | {len(rows)} | {total_low} | {total_expected} | {total_high} |",
        "",
        "Per-call details are in `token_usage_estimate.csv`.",
    ]
    (RESULTS / "token_usage_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return rows, (total_low, total_expected, total_high)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)

    diego_r1 = read_json(LOCAL_RESULTS / "doc11_round1_diego_connectivity_proposal.json")
    diego_r2 = read_json(LOCAL_RESULTS / "doc11_round2_diego_connectivity_proposal.json")
    jennifer_nodes = read_json(LOCAL_RESULTS / "doc11_round1_jennifer_nodes.json")
    jennifer_edges = read_json(LOCAL_RESULTS / "doc11_round1_jennifer_edges.json")

    rounds = {
        "diego_round1": {
            "nodes": diego_r1["node_order"],
            "edges": canonicalize_edges(diego_r1["asserted_edges"]),
            "uncertain": diego_r1.get("uncertain_edges", []),
            "rejected": diego_r1.get("excluded_non_edges", []),
        },
        "jennifer_round1": {
            "nodes": jennifer_nodes,
            "edges": canonicalize_edges(jennifer_edges),
            "uncertain": [
                ["ATS-480-A", "CONTROL_POWER_RPS_INTERLOCKS", "Nearby/crossing dashed routing, no clear ATS endpoint; not asserted"],
                ["ATS-480-B", "CONTROL_POWER_RPS_INTERLOCKS", "Nearby/crossing dashed routing, no clear ATS endpoint; not asserted"],
            ],
            "rejected": [
                ["ATS-480-A", "CONTROL_POWER_RPS_INTERLOCKS", "removed Diego assertion: nearby/crossing dashed line is not a visible ATS termination"],
                ["ATS-480-B", "CONTROL_POWER_RPS_INTERLOCKS", "removed Diego assertion: nearby/crossing dashed line is not a visible ATS termination"],
                ["BUS-480-A2", "BUS-480-B1", "train boundary/end caps separate these buses"],
                ["BUS-480-B2", "BUS-480-C1", "train boundary/end caps separate these buses"],
                ["BUS-480-C2", "BUS-480-D1", "train boundary/end caps separate these buses"],
                ["BUS-DC-125A", "BUS-DC-125B", "separate lower DC divisions; no direct solid tie"],
                ["PANEL-IC-B", "BUS-DC-125B", "no direct landing; represented via GND-B route"],
                ["PANEL-IC-D", "BUS-DC-125B", "no direct adjacency; represented via GND-D route"],
            ],
        },
        "diego_round2": {
            "nodes": diego_r2["final_node_order_round2_diego"],
            "edges": canonicalize_edges(diego_r2["final_asserted_edges_round2_diego"]),
            "uncertain": diego_r2.get("uncertain_edges_round2_diego", []),
            "rejected": diego_r2.get("rejected_edges_round2_diego", []),
        },
        "jennifer_round2_final": {
            "nodes": diego_r2["final_node_order_round2_diego"],
            "edges": canonicalize_edges(diego_r2["final_asserted_edges_round2_diego"]),
            "uncertain": [],
            "rejected": [
                ["ATS-480-A", "CONTROL_POWER_RPS_INTERLOCKS", "final rejected: no visible ATS dashed endpoint/junction"],
                ["ATS-480-B", "CONTROL_POWER_RPS_INTERLOCKS", "final rejected: no visible ATS dashed endpoint/junction"],
                ["BUS-480-A2", "BUS-480-B1", "final rejected: train boundary/end caps separate these buses"],
                ["BUS-480-B2", "BUS-480-C1", "final rejected: train boundary/end caps separate these buses"],
                ["BUS-480-C2", "BUS-480-D1", "final rejected: train boundary/end caps separate these buses"],
                ["BUS-DC-125A", "BUS-DC-125B", "final rejected: separate lower DC divisions; no direct solid tie"],
            ],
        },
    }

    summaries = []
    for name, data in rounds.items():
        nodes = data["nodes"]
        edges = data["edges"]
        write_json(RESULTS / f"{name}_nodes.json", nodes)
        write_json(RESULTS / f"{name}_edges.json", edges)
        write_edges_csv(RESULTS / f"{name}_edges.csv", edges)
        matrix = write_matrix_csv(RESULTS / f"{name}_connectivity_matrix.csv", nodes, edges)
        count = validate_matrix(nodes, edges, matrix)
        write_json(RESULTS / f"{name}_uncertain_edges.json", data["uncertain"])
        write_json(RESULTS / f"{name}_rejected_edges.json", data["rejected"])
        summaries.append((name, len(nodes), count, len(data["uncertain"]), len(data["rejected"])))

    final = rounds["jennifer_round2_final"]
    write_json(RESULTS / "final_nodes.json", final["nodes"])
    write_json(RESULTS / "final_edges.json", final["edges"])
    write_edges_csv(RESULTS / "final_edges.csv", final["edges"])
    final_matrix = write_matrix_csv(RESULTS / "final_connectivity_matrix.csv", final["nodes"], final["edges"])
    final_count = validate_matrix(final["nodes"], final["edges"], final_matrix)
    shutil.copyfile(RESULTS / "final_connectivity_matrix.csv", RESULTS / "final_matrix.csv")

    with open(RESULTS / "final_uncertain_edges.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "reason"])
        writer.writerows(final["uncertain"])
    with open(RESULTS / "final_rejected_edges.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "reason"])
        writer.writerows(final["rejected"])

    write_json(
        RESULTS / "final_extraction_summary.json",
        {
            "document": DOC,
            "iteration": ITERATION,
            "node_count": len(final["nodes"]),
            "edge_count": final_count,
            "uncertain_edge_count": len(final["uncertain"]),
            "rejected_edge_count": len(final["rejected"]),
            "converged": True,
            "rounds": [
                {
                    "round": name,
                    "node_count": node_count,
                    "edge_count": edge_count,
                    "uncertain_edge_count": uncertain_count,
                    "rejected_edge_count": rejected_count,
                }
                for name, node_count, edge_count, uncertain_count, rejected_count in summaries
            ],
        },
    )

    lines = [
        "# Document 11 Round Summaries",
        "",
        "| Round | Nodes | Asserted Edges | Uncertain | Rejected |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, node_count, edge_count, uncertain_count, rejected_count in summaries:
        lines.append(f"| {name} | {node_count} | {edge_count} | {uncertain_count} | {rejected_count} |")
    lines.extend(
        [
            "",
            "Final matrix: `final_connectivity_matrix.csv`.",
            "Final convergence: Diego round 2 matched Jennifer round 1, and Jennifer round 2 confirmed no final changes.",
            "Ground truth or GT-derived feedback was not used.",
        ]
    )
    (RESULTS / "round_summaries.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    token_rows, token_totals = write_token_estimates(rounds)

    print(json.dumps({
        "document": DOC,
        "iteration": ITERATION,
        "final_nodes": len(final["nodes"]),
        "final_edges": final_count,
        "rounds_written": len(rounds),
        "token_total_low_expected_high": token_totals,
        "results_dir": str(RESULTS),
    }, indent=2))


if __name__ == "__main__":
    main()
