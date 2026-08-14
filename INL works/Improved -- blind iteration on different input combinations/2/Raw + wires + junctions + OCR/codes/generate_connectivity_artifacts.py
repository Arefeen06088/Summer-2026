import csv
import math
import os
import struct
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

DOC_ID = "2"
ITERATION = "1"


def read_component_nodes():
    path = BASE / "component_visual_ocr_labels.csv"
    nodes = []
    seen = set()
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("normalized_text") or row.get("recognized_text") or "").strip()
            if name and name not in seen:
                seen.add(name)
                nodes.append(name)
    return nodes


BUS_NODES = [
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-480-A1",
    "BUS-480-A2",
    "BUS-480-A3",
    "BUS-208-A",
    "BUS-125DC-A",
    "BUS-120AC-A",
    "BUS-480-B1",
    "BUS-480-B2",
    "BUS-480-B3",
    "BUS-208-B",
    "BUS-125DC-B",
    "BUS-120AC-B",
]


COMPONENT_NODES = read_component_nodes()
NODES = COMPONENT_NODES + BUS_NODES


def path_edges(path):
    return list(zip(path, path[1:]))


SOLID_PATHS = [
    ["GRID-N501", "DS-N501", "TR-SU-1A", "CB-SU-1A", "BUS-4160-A"],
    ["GEN-EDG-A", "DS-DG-A", "CB-DG-A", "BUS-4160-A"],
    ["GRID-R502", "DS-R502", "TR-SU-1B", "CB-SU-1B", "BUS-4160-B"],
    ["GEN-EDG-B", "DS-DG-B", "CB-DG-B", "BUS-4160-B"],
    ["GEN-AAC-1", "DS-AAC-1", "CB-AAC-1", "BUS-4160-B"],
    ["BUS-4160-A", "CB-F11A", "TR-LC11A", "BUS-480-A1", "CB-M11A", "MCC-11A", "CB-P101A", "MTR-P101A", "PUMP-RHR-A"],
    ["BUS-4160-A", "CB-F12A", "TR-LC12A", "BUS-480-A2", "CB-M12A", "MCC-12A", "CB-P201A", "MTR-P201A", "PUMP-SI-A"],
    ["BUS-4160-A", "CB-F13A", "TR-LC13A", "BUS-480-A3", "CB-M13A", "MCC-13A", "CB-FAN-A", "MTR-FAN-A", "FAN-CAV-A"],
    ["BUS-4160-A", "CB-F14A", "TR-RPS-A", "BUS-208-A", "REC-125-A", "BUS-125DC-A"],
    ["BUS-125DC-A", "BAT-125-A"],
    ["BUS-125DC-A", "INV-120-A", "BUS-120AC-A", "CP-RPS-A"],
    ["BUS-4160-A", "CB-CVCS-A", "MCC-CVCS-A", "MTR-CVCS-A", "PUMP-CVCS-A"],
    ["BUS-4160-B", "CB-F11B", "TR-LC11B", "BUS-480-B1", "CB-M11B", "MCC-11B", "CB-P101B", "MTR-P101B", "PUMP-RHR-B"],
    ["BUS-4160-B", "CB-F12B", "TR-LC12B", "BUS-480-B2", "CB-M12B", "MCC-12B", "CB-P201B", "MTR-P201B", "PUMP-SI-B"],
    ["BUS-4160-B", "CB-F13B", "TR-LC13B", "BUS-480-B3", "CB-M13B", "MCC-13B", "CB-FAN-B", "MTR-FAN-B", "FAN-CAV-B"],
    ["BUS-4160-B", "CB-F14B", "TR-RPS-B", "BUS-208-B", "REC-125-B", "BUS-125DC-B"],
    ["BUS-125DC-B", "BAT-125-B"],
    ["BUS-125DC-B", "INV-120-B", "BUS-120AC-B", "CP-RPS-B"],
    ["BUS-4160-B", "CB-CVCS-B", "MCC-CVCS-B", "MTR-CVCS-B", "PUMP-CVCS-B"],
]


SPECIAL_EDGES = [
    ("BUS-4160-A", "CB-TIE-4AB", "solid_feeder_normally_open", "N.O. bus tie, available; not operating alignment"),
    ("CB-TIE-4AB", "BUS-4160-B", "solid_feeder_normally_open", "N.O. bus tie, available; not operating alignment"),
    ("CP-RPS-A", "RLY-K501A", "dashed_control_instrument", "dashed RPS control/instrument wiring"),
    ("RLY-K501A", "INST-NI501A", "dashed_control_instrument", "dashed RPS control/instrument wiring"),
    ("CP-RPS-B", "RLY-K501B", "dashed_control_instrument", "dashed RPS control/instrument wiring"),
    ("RLY-K501B", "INST-NI501B", "dashed_control_instrument", "dashed RPS control/instrument wiring"),
    ("CP-RPS-A", "CP-RPS-B", "dashed_cross_train_permissive", "long dashed cross-train control/permissive wiring"),
    ("PUMP-CVCS-A", "VLV-LCV201A", "dashed_control_signal", "dashed CVCS pump-to-valve control/signal link"),
    ("PUMP-CVCS-B", "VLV-LCV201B", "dashed_control_signal", "dashed CVCS pump-to-valve control/signal link"),
]


def unique_ordered_edges(edges):
    seen = set()
    out = []
    for a, b in edges:
        key = tuple(sorted((a, b)))
        if key not in seen:
            seen.add(key)
            out.append((a, b))
    return out


SOLID_EDGES = unique_ordered_edges([edge for p in SOLID_PATHS for edge in path_edges(p)])
FINAL_EDGES = unique_ordered_edges(SOLID_EDGES + [(a, b) for a, b, _, _ in SPECIAL_EDGES])
SPECIAL_EDGE_KEYS = {tuple(sorted((a, b))) for a, b, _, _ in SPECIAL_EDGES}


ROUND_DEFINITIONS = [
    {
        "round": "01",
        "agent": "Diego",
        "file_stem": "round_01_diego_high_recall",
        "interpretation": "all_drawn_electrical_links_high_recall",
        "edges": FINAL_EDGES,
        "notes": "Initial high-recall pass retained N.O. tie and dashed control/signal candidates as visually drawn links.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "file_stem": "round_02_jennifer_precision_closed_subset",
        "interpretation": "closed_or_solid_operational_subset",
        "edges": SOLID_EDGES,
        "notes": "Precision pass removed N.O./dashed/control candidates for an energized/solid subset.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "file_stem": "round_03_diego_closed_saturation",
        "interpretation": "closed_or_solid_operational_subset",
        "edges": SOLID_EDGES,
        "notes": "Diego initially agreed with Jennifer under the closed/energized interpretation.",
    },
    {
        "round": "04",
        "agent": "Diego",
        "file_stem": "round_04_diego_reconciled_drawn_links",
        "interpretation": "all_drawn_electrical_links",
        "edges": FINAL_EDGES,
        "notes": "After reconciling raw title/notes, Diego recommended the 100-edge drawn-link matrix.",
    },
    {
        "round": "05",
        "agent": "Jennifer",
        "file_stem": "round_05_jennifer_final_drawn_links",
        "interpretation": "all_drawn_electrical_links",
        "edges": FINAL_EDGES,
        "notes": "Jennifer final review agreed that the requested matrix should capture all 100 drawn electrical links.",
    },
]


def edge_key(edge):
    a, b = edge
    return tuple(sorted((a, b)))


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path, edges):
    adjacency = {edge_key(e) for e in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"] + NODES)
        for a in NODES:
            row = [a]
            for b in NODES:
                row.append("0" if a == b else ("1" if tuple(sorted((a, b))) in adjacency else "0"))
            writer.writerow(row)


def metadata_for_edge(a, b):
    key = tuple(sorted((a, b)))
    if key in SPECIAL_EDGE_KEYS:
        for sa, sb, kind, status in SPECIAL_EDGES:
            if tuple(sorted((sa, sb))) == key:
                return kind, status
    return "solid_power_feeder", "drawn solid feeder/load/source connection"


def write_edge_file(path, edges):
    rows = []
    for idx, (a, b) in enumerate(edges, start=1):
        kind, status = metadata_for_edge(a, b)
        rows.append(
            {
                "edge_id": f"E-{idx:03d}",
                "node_a": a,
                "node_b": b,
                "edge_kind": kind,
                "status_note": status,
                "included_in_final_matrix": "yes",
            }
        )
    write_csv(path, ["edge_id", "node_a", "node_b", "edge_kind", "status_note", "included_in_final_matrix"], rows)


def png_size(path):
    with path.open("rb") as f:
        sig = f.read(24)
    if len(sig) >= 24 and sig[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", sig[16:24])
    return None, None


def estimate_image_tokens(path, detail="high"):
    width, height = png_size(path)
    if not width or not height:
        return 0, "", ""
    if detail == "low":
        return 85, f"{width}x{height}", "low_detail_flat_85"
    scale = min(2048 / width, 2048 / height, 1.0)
    sw = int(math.ceil(width * scale))
    sh = int(math.ceil(height * scale))
    if min(sw, sh) > 768:
        scale2 = 768 / min(sw, sh)
        sw = int(math.ceil(sw * scale2))
        sh = int(math.ceil(sh * scale2))
    tiles = int(math.ceil(sw / 512) * math.ceil(sh / 512))
    return 85 + 170 * tiles, f"{width}x{height}", f"high_detail_scaled_{sw}x{sh}_{tiles}_tiles"


def approx_text_tokens(text_or_chars):
    if isinstance(text_or_chars, int):
        return int(math.ceil(text_or_chars / 4))
    return int(math.ceil(len(text_or_chars) / 4))


def build_usage_estimates():
    images = {
        "raw": BASE / "raw -- schematic_image_variant_b_100.png",
        "component_overlay": BASE / "component_labels_banners_overlay.png",
        "wire_nodes_overlay": BASE / "wire_nodes_overlay.png",
        "top_sources_zoom": BASE / "codes" / "crop_top_sources_zoom.png",
        "top_tie_zoom": BASE / "codes" / "crop_top_tie_zoom.png",
        "train_a": BASE / "codes" / "crop_train_a_feeders.png",
        "train_b": BASE / "codes" / "crop_train_b_feeders.png",
        "a_rps": BASE / "codes" / "crop_a_rps_zoom.png",
        "b_rps": BASE / "codes" / "crop_b_rps_zoom.png",
        "a_rps_bottom": BASE / "codes" / "crop_a_rps_bottom_zoom.png",
        "b_rps_bottom": BASE / "codes" / "crop_b_rps_bottom_zoom.png",
        "notes": BASE / "codes" / "crop_notes_and_legend.png",
        "a_cvcs": BASE / "codes" / "crop_a_cvcs_zoom.png",
        "b_cvcs": BASE / "codes" / "crop_b_cvcs_zoom.png",
    }
    image_rows = []
    image_token_map = {}
    for name, path in images.items():
        if path.exists():
            tokens, dims, method = estimate_image_tokens(path)
            image_token_map[name] = tokens
            image_rows.append(
                {
                    "artifact": name,
                    "path": str(path),
                    "dimensions": dims,
                    "estimated_image_tokens_high_detail": tokens,
                    "method": method,
                }
            )
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        ["artifact", "path", "dimensions", "estimated_image_tokens_high_detail", "method"],
        image_rows,
    )

    diego_r1_images = [
        "raw",
        "component_overlay",
        "wire_nodes_overlay",
        "top_sources_zoom",
        "top_tie_zoom",
        "train_a",
        "train_b",
        "a_rps",
        "b_rps",
        "a_rps_bottom",
        "b_rps_bottom",
        "notes",
    ]
    jennifer_r2_images = diego_r1_images
    main_images = [
        "raw",
        "top_sources_zoom",
        "top_tie_zoom",
        "train_a",
        "train_b",
        "a_rps",
        "b_rps",
        "a_rps_bottom",
        "b_rps_bottom",
        "a_cvcs",
        "b_cvcs",
        "notes",
    ]

    def img_sum(names):
        return sum(image_token_map.get(n, 0) for n in names)

    # Text and output/reasoning estimates are local approximations because no
    # Responses token-count endpoint or usage objects are available here.
    call_specs = [
        {
            "call_id": "main_agent_01_orchestration_visual_inspection",
            "agent": "main",
            "round": "main",
            "text_tokens": 3800,
            "image_tokens": img_sum(main_images),
            "cached_tokens": 0,
            "output_expected": 1200,
            "reasoning_expected": 5000,
            "notes": "Main agent inventory, crop planning, visual inspection, and reconciliation reasoning.",
        },
        {
            "call_id": "diego_01_high_recall_extract",
            "agent": "Diego",
            "round": "01",
            "text_tokens": 720,
            "image_tokens": img_sum(diego_r1_images),
            "cached_tokens": 0,
            "output_expected": 1900,
            "reasoning_expected": 4500,
            "notes": "Spawned GPT-5.5 xhigh subagent with raw/overlay/crops.",
        },
        {
            "call_id": "jennifer_02_precision_review",
            "agent": "Jennifer",
            "round": "02",
            "text_tokens": 1450,
            "image_tokens": img_sum(jennifer_r2_images),
            "cached_tokens": 0,
            "output_expected": 1200,
            "reasoning_expected": 4200,
            "notes": "Spawned GPT-5.5 xhigh subagent with Diego proposal and raw/overlay/crops.",
        },
        {
            "call_id": "diego_03_closed_saturation",
            "agent": "Diego",
            "round": "03",
            "text_tokens": 520,
            "image_tokens": 0,
            "cached_tokens": img_sum(diego_r1_images) + 720 + 1900,
            "output_expected": 900,
            "reasoning_expected": 2500,
            "notes": "Text follow-up in same Diego agent; previous image context likely cached by provider.",
        },
        {
            "call_id": "diego_04_drawn_link_reconciliation",
            "agent": "Diego",
            "round": "04",
            "text_tokens": 500,
            "image_tokens": 0,
            "cached_tokens": img_sum(diego_r1_images) + 720 + 1900 + 520 + 900,
            "output_expected": 330,
            "reasoning_expected": 1600,
            "notes": "Text reconciliation using raw drawing metadata already in context.",
        },
        {
            "call_id": "jennifer_05_final_reconciliation",
            "agent": "Jennifer",
            "round": "05",
            "text_tokens": 520,
            "image_tokens": 0,
            "cached_tokens": img_sum(jennifer_r2_images) + 1450 + 1200,
            "output_expected": 360,
            "reasoning_expected": 1700,
            "notes": "Text final review using raw drawing metadata already in context.",
        },
        {
            "call_id": "main_agent_02_artifact_generation_final",
            "agent": "main",
            "round": "main",
            "text_tokens": 1800,
            "image_tokens": 0,
            "cached_tokens": 9000,
            "output_expected": 700,
            "reasoning_expected": 2200,
            "notes": "Script creation, validation, and final response.",
        },
    ]

    usage_rows = []
    total_low = total_expected = total_high = 0
    for spec in call_specs:
        input_tokens = spec["text_tokens"] + spec["image_tokens"]
        low = int(round(input_tokens + spec["output_expected"] * 0.7 + spec["reasoning_expected"] * 0.5))
        expected = int(round(input_tokens + spec["output_expected"] + spec["reasoning_expected"]))
        high = int(round(input_tokens + spec["output_expected"] * 1.4 + spec["reasoning_expected"] * 1.8))
        total_low += low
        total_expected += expected
        total_high += high
        usage_rows.append(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "call_id": spec["call_id"],
                "agent": spec["agent"],
                "round": spec["round"],
                "model": "gpt-5.5 for subagents; main model unavailable",
                "input_tokens_est": input_tokens,
                "cached_input_tokens_est": spec["cached_tokens"],
                "image_file_input_tokens_est": spec["image_tokens"],
                "output_tokens_low": int(round(spec["output_expected"] * 0.7)),
                "output_tokens_expected": spec["output_expected"],
                "output_tokens_high": int(round(spec["output_expected"] * 1.4)),
                "reasoning_tokens_low": int(round(spec["reasoning_expected"] * 0.5)),
                "reasoning_tokens_expected": spec["reasoning_expected"],
                "reasoning_tokens_high": int(round(spec["reasoning_expected"] * 1.8)),
                "total_tokens_low": low,
                "total_tokens_expected": expected,
                "total_tokens_high": high,
                "usage_object_available": "no",
                "notes": spec["notes"],
            }
        )
    write_csv(
        RESULTS / "model_call_usage_estimates.csv",
        [
            "document",
            "iteration",
            "call_id",
            "agent",
            "round",
            "model",
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
            "notes",
        ],
        usage_rows,
    )
    write_csv(
        RESULTS / "token_usage_totals_by_document.csv",
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
        [
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "api_key_available": "yes" if os.environ.get("OPENAI_API_KEY") else "no",
                "responses_token_count_endpoint_used": "no_api_key",
                "usage_objects_collected": "not_exposed_by_multi_agent_tool",
                "model_calls_counted": len(call_specs),
                "total_tokens_low": total_low,
                "total_tokens_expected": total_expected,
                "total_tokens_high": total_high,
                "method": "chars/4 text estimate plus high-detail 512px image tile estimate; low/high bands applied to unknown output and reasoning tokens",
            }
        ],
    )


def main():
    missing = sorted({n for edge in FINAL_EDGES for n in edge if n not in set(NODES)})
    if missing:
        raise SystemExit(f"Unknown edge node(s): {missing}")

    if len(COMPONENT_NODES) != 86:
        raise SystemExit(f"Expected 86 component labels, got {len(COMPONENT_NODES)}")
    if len(NODES) != 100:
        raise SystemExit(f"Expected 100 total nodes, got {len(NODES)}")
    if len(SOLID_EDGES) != 91:
        raise SystemExit(f"Expected 91 solid/closed subset edges, got {len(SOLID_EDGES)}")
    if len(FINAL_EDGES) != 100:
        raise SystemExit(f"Expected 100 final drawn-link edges, got {len(FINAL_EDGES)}")

    node_rows = []
    for idx, node in enumerate(NODES, start=1):
        node_rows.append(
            {
                "node_index": idx,
                "node_name": node,
                "node_type": "bus" if node.startswith("BUS-") else "component",
                "source": "visible_bus_label" if node.startswith("BUS-") else "component_visual_ocr_labels.csv",
                "included_in_final_matrix": "yes",
            }
        )
    write_csv(RESULTS / "nodes.csv", ["node_index", "node_name", "node_type", "source", "included_in_final_matrix"], node_rows)

    for definition in ROUND_DEFINITIONS:
        matrix_path = RESULTS / f"{definition['file_stem']}_matrix.csv"
        edge_path = RESULTS / f"{definition['file_stem']}_edges.csv"
        write_matrix(matrix_path, definition["edges"])
        write_edge_file(edge_path, definition["edges"])

    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_edge_file(RESULTS / "final_connectivity_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS / "operational_solid_subset_matrix.csv", SOLID_EDGES)
    write_edge_file(RESULTS / "operational_solid_subset_edges.csv", SOLID_EDGES)

    special_rows = []
    for idx, (a, b, kind, status) in enumerate(SPECIAL_EDGES, start=1):
        special_rows.append(
            {
                "edge_id": f"S-{idx:03d}",
                "node_a": a,
                "node_b": b,
                "edge_kind": kind,
                "status_note": status,
                "included_in_final_matrix": "yes",
                "included_in_operational_solid_subset": "no",
            }
        )
    write_csv(
        RESULTS / "special_status_edges.csv",
        [
            "edge_id",
            "node_a",
            "node_b",
            "edge_kind",
            "status_note",
            "included_in_final_matrix",
            "included_in_operational_solid_subset",
        ],
        special_rows,
    )

    summary_rows = []
    previous_count = None
    for definition in ROUND_DEFINITIONS:
        edge_count = len(definition["edges"])
        delta = "" if previous_count is None else edge_count - previous_count
        previous_count = edge_count
        summary_rows.append(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "round": definition["round"],
                "agent": definition["agent"],
                "interpretation": definition["interpretation"],
                "node_count": len(NODES),
                "edge_count": edge_count,
                "delta_edges_from_previous_round": delta,
                "matrix_file": f"{definition['file_stem']}_matrix.csv",
                "edge_file": f"{definition['file_stem']}_edges.csv",
                "notes": definition["notes"],
            }
        )
    write_csv(
        RESULTS / "round_summaries.csv",
        [
            "document",
            "iteration",
            "round",
            "agent",
            "interpretation",
            "node_count",
            "edge_count",
            "delta_edges_from_previous_round",
            "matrix_file",
            "edge_file",
            "notes",
        ],
        summary_rows,
    )

    build_usage_estimates()

    readme = f"""# Document {DOC_ID} Connectivity Extraction

Final interpretation: all drawn electrical links from the raw schematic, matching the raw title block count of 100 components and 100 connections.

Artifacts:
- `final_connectivity_matrix.csv`: 100 x 100 symmetric adjacency matrix for final drawn-link connectivity.
- `final_connectivity_edges.csv`: 100 direct undirected edges with status metadata.
- `operational_solid_subset_matrix.csv`: 91-edge derived subset excluding N.O./dashed/control links.
- `special_status_edges.csv`: the 9 final-matrix edges that are N.O. or dashed/control/signal.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `model_call_usage_estimates.csv`: estimated model-call usage; no API key was available, and usage objects were not exposed by the subagent tool.

Counts:
- Component labels from CSV: {len(COMPONENT_NODES)}
- Explicit visible bus nodes: {len(BUS_NODES)}
- Total matrix nodes: {len(NODES)}
- Final drawn-link edges: {len(FINAL_EDGES)}
- Operational solid subset edges: {len(SOLID_EDGES)}
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")

    print(f"nodes={len(NODES)} final_edges={len(FINAL_EDGES)} solid_subset_edges={len(SOLID_EDGES)}")


if __name__ == "__main__":
    main()
