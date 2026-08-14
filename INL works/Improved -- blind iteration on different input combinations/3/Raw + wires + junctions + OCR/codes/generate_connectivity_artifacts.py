import csv
import math
import os
import struct
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

DOC_ID = "3"
ITERATION = "1"


LOGICAL_NODES = [
    "BUS-416A",
    "BUS-416B",
    "FDB-A1",
    "FDB-A2",
    "FDB-B1",
    "FDB-B2",
    "DC-BUS-A",
    "DC-BUS-B",
    "BUS-120A",
    "BUS-120B",
    "GND-1E",
]


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


COMPONENT_NODES = read_component_nodes()
NODES = COMPONENT_NODES + LOGICAL_NODES


def path_edges(path):
    return list(zip(path, path[1:]))


POWER_PATHS = [
    ["GRID-1", "AUX-TR-1A", "CB-101", "BUS-416A"],
    ["EDG-1A", "CB-DG1A", "BUS-416A"],
    ["BUS-416A", "TR-480A1", "CB-480A1", "MCC-480A1", "FDB-A1"],
    ["BUS-416A", "TR-480A2", "CB-480A2", "MCC-480A2", "FDB-A2"],
    ["BUS-416A", "BUS-TIE-41", "BUS-416B"],
    ["GRID-2", "AUX-TR-1B", "CB-102", "BUS-416B"],
    ["EDG-1B", "CB-DG1B", "BUS-416B"],
    ["BUS-416B", "TR-480B1", "CB-480B1", "MCC-480B1", "FDB-B1"],
    ["BUS-416B", "TR-480B2", "CB-480B2", "MCC-480B2", "FDB-B2"],
    ["BUS-416A", "CB-CHG-A", "CHGR-125A", "DC-BUS-A"],
    ["BAT-125A", "DC-BUS-A", "INV-120A", "BUS-120A"],
    ["BUS-416B", "CB-CHG-B", "CHGR-125B", "DC-BUS-B"],
    ["BAT-125B", "DC-BUS-B", "INV-120B", "BUS-120B"],
    ["FDB-A1", "CB-SI-A1", "PUMP-SI-A1"],
    ["FDB-A1", "CB-RHR-A1", "PUMP-RHR-A1"],
    ["FDB-A1", "CB-CCW-A1", "PUMP-CCW-A1"],
    ["FDB-A1", "CB-FAN-A1", "FAN-CR-A1"],
    ["FDB-A1", "CB-MOV-A101", "VALVE-SI-A101"],
    ["FDB-A1", "CB-MOV-A102", "VALVE-RHR-A102"],
    ["FDB-A2", "CB-CS-A2", "PUMP-CS-A2"],
    ["FDB-A2", "CB-SW-A2", "PUMP-SW-A2"],
    ["FDB-A2", "CB-AFW-A2", "PUMP-AFW-A2"],
    ["FDB-A2", "CB-FAN-A2", "FAN-EB-A2"],
    ["FDB-A2", "CB-MOV-A201", "VALVE-CCW-A201"],
    ["FDB-A2", "CB-HTR-A2", "HTR-BAY-A2"],
    ["FDB-B1", "CB-SI-B1", "PUMP-SI-B1"],
    ["FDB-B1", "CB-RHR-B1", "PUMP-RHR-B1"],
    ["FDB-B1", "CB-CCW-B1", "PUMP-CCW-B1"],
    ["FDB-B1", "CB-FAN-B1", "FAN-CR-B1"],
    ["FDB-B1", "CB-MOV-B101", "VALVE-SI-B101"],
    ["FDB-B1", "CB-MOV-B102", "VALVE-RHR-B102"],
    ["FDB-B2", "CB-CS-B2", "PUMP-CS-B2"],
    ["FDB-B2", "CB-SW-B2", "PUMP-SW-B2"],
    ["FDB-B2", "CB-FAN-B2", "FAN-EB-B2"],
    ["FDB-B2", "CB-MOV-B201", "VALVE-CCW-B201"],
    ["FDB-B2", "CB-HTR-B2", "HTR-BAY-B2"],
]


SPECIAL_EDGES = [
    ("BUS-416A", "BUS-TIE-41", "solid_power_normally_open_tie", "Drawn N.O. 52-TIE bus tie; included as visible connection, not assumed closed."),
    ("BUS-TIE-41", "BUS-416B", "solid_power_normally_open_tie", "Drawn N.O. 52-TIE bus tie; included as visible connection, not assumed closed."),
    ("BUS-416A", "GND-1E", "ground_reference_dot_dash", "Dot-dash GND-A reference normalized to the visible GND-1E node."),
    ("BUS-416B", "GND-1E", "ground_reference_dot_dash", "Dot-dash GND-B reference normalized to the visible GND-1E node."),
    ("BUS-120A", "PANEL-RPS-A", "control_power_long_dash", "120A-CNTRL long-dash control-power riser to RPS Train A."),
    ("BUS-120B", "PANEL-RPS-B", "control_power_long_dash", "120B-CNTRL long-dash control-power riser to RPS Train B."),
    ("INST-PT-A", "PANEL-RPS-A", "signal_dotted", "Dotted PT-A signal into RPS Train A panel."),
    ("INST-LT-A", "PANEL-RPS-A", "signal_dotted", "Dotted LT-A signal into RPS Train A panel."),
    ("RELAY-K27A", "PANEL-RPS-A", "control_interlock_long_dash", "K27A relay contact/interlock to RPS Train A panel."),
    ("RELAY-K27A", "PANEL-ESF-A", "control_interlock_long_dash", "K27A UV relay/interlock route to ESF Train A panel."),
    ("PANEL-ESF-A", "JB-A401", "terminal_control_link_long_dash", "ESF Train A terminal/control link to JB-A401."),
    ("INST-PT-B", "PANEL-RPS-B", "signal_dotted", "Dotted PT-B signal into RPS Train B panel."),
    ("INST-LT-B", "PANEL-RPS-B", "signal_dotted", "Dotted LT-B signal into RPS Train B panel."),
    ("RELAY-K27B", "PANEL-RPS-B", "control_interlock_long_dash", "K27B relay contact/interlock to RPS Train B panel."),
    ("RELAY-K27B", "PANEL-ESF-B", "control_interlock_long_dash", "K27B UV relay/interlock route to ESF Train B panel."),
    ("PANEL-ESF-B", "JB-B501", "terminal_control_link_long_dash", "ESF Train B terminal/control link to JB-B501."),
]


def edge_key(edge):
    a, b = edge
    return tuple(sorted((a, b)))


def unique_ordered_edges(edges):
    seen = set()
    out = []
    for a, b in edges:
        key = tuple(sorted((a, b)))
        if key not in seen:
            seen.add(key)
            out.append((a, b))
    return out


POWER_EDGES = unique_ordered_edges([edge for path in POWER_PATHS for edge in path_edges(path)])
FINAL_EDGES = unique_ordered_edges(POWER_EDGES + [(a, b) for a, b, _, _ in SPECIAL_EDGES])
SPECIAL_EDGE_KEYS = {tuple(sorted((a, b))) for a, b, _, _ in SPECIAL_EDGES}


ROUND_DEFINITIONS = [
    {
        "round": "01",
        "agent": "Diego",
        "file_stem": "round_01_diego_high_recall",
        "interpretation": "all_drawn_connections_high_recall",
        "edges": FINAL_EDGES,
        "notes": "Initial Diego pass proposed the 100-node/100-edge drawn-link graph, with ground-reference normalization noted.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "file_stem": "round_02_jennifer_precision",
        "interpretation": "all_drawn_connections_precision_review",
        "edges": FINAL_EDGES,
        "notes": "Jennifer retained the graph; confirmed charger feeds from BUS-416A/B and two GND-1E bus-reference edges.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "file_stem": "round_03_diego_saturation",
        "interpretation": "all_drawn_connections_saturated",
        "edges": FINAL_EDGES,
        "notes": "Diego saturation check agreed with Jennifer; no topology changes.",
    },
    {
        "round": "04",
        "agent": "Jennifer",
        "file_stem": "round_04_jennifer_final",
        "interpretation": "all_drawn_connections_final",
        "edges": FINAL_EDGES,
        "notes": "Final precision close-out after Diego agreement; graph saturated.",
    },
]


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
        for sa, sb, kind, note in SPECIAL_EDGES:
            if tuple(sorted((sa, sb))) == key:
                return kind, note
    if a.startswith("DC-BUS") or b.startswith("DC-BUS") or a.startswith("BUS-120") or b.startswith("BUS-120"):
        return "dc_ups_power", "Drawn DC/UPS feeder connection."
    if "CHG" in a or "CHG" in b:
        return "charger_power", "Drawn charger feeder connection."
    return "solid_power", "Drawn solid power/source/load connection."


def write_edge_file(path, edges):
    rows = []
    for idx, (a, b) in enumerate(edges, start=1):
        kind, note = metadata_for_edge(a, b)
        rows.append(
            {
                "edge_id": f"E-{idx:03d}",
                "node_a": a,
                "node_b": b,
                "edge_kind": kind,
                "status_note": note,
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
    tiles = math.ceil(sw / 512) * math.ceil(sh / 512)
    return 85 + 170 * tiles, f"{width}x{height}", f"high_detail_scaled_{sw}x{sh}_{tiles}_tiles"


def estimate_text_tokens(text):
    return max(1, math.ceil(len(text) / 4))


def artifact_token_rows():
    files = [
        "raw -- synthetic_npp_100_component_electrical_schematic.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
        "wires_mask.png",
        "component_visual_ocr_labels.csv",
        "wire_nodes.csv",
        "codes/crop_top_sources_buses_tie.png",
        "codes/crop_top_tie_ground_detail.png",
        "codes/crop_dc_ups_center.png",
        "codes/crop_train_a_mcc_feeders.png",
        "codes/crop_train_b_mcc_feeders.png",
        "codes/crop_rps_esf_interlocks.png",
        "codes/crop_rps_a_detail.png",
        "codes/crop_rps_b_detail.png",
        "codes/crop_control_riser_mid.png",
        "codes/crop_notes_legend.png",
        "codes/crop_title_counts.png",
    ]
    rows = []
    for rel in files:
        path = BASE / rel
        if not path.exists():
            continue
        if path.suffix.lower() == ".png":
            tokens, dimensions, method = estimate_image_tokens(path)
            kind = "image"
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
            tokens, dimensions, method = estimate_text_tokens(text), "", "chars_div_4"
            kind = "text_file"
        rows.append(
            {
                "artifact": rel,
                "kind": kind,
                "bytes": path.stat().st_size,
                "dimensions": dimensions,
                "estimated_input_tokens": tokens,
                "method": method,
            }
        )
    return rows


def build_usage_estimates():
    artifact_rows = artifact_token_rows()
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        ["artifact", "kind", "bytes", "dimensions", "estimated_input_tokens", "method"],
        artifact_rows,
    )
    token_by_artifact = {row["artifact"]: int(row["estimated_input_tokens"]) for row in artifact_rows}

    common_images = [
        "raw -- synthetic_npp_100_component_electrical_schematic.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "codes/crop_top_sources_buses_tie.png",
        "codes/crop_dc_ups_center.png",
        "codes/crop_train_a_mcc_feeders.png",
        "codes/crop_train_b_mcc_feeders.png",
        "codes/crop_rps_esf_interlocks.png",
        "codes/crop_notes_legend.png",
        "codes/crop_title_counts.png",
    ]
    precision_images = common_images + [
        "codes/crop_top_tie_ground_detail.png",
        "codes/crop_rps_a_detail.png",
        "codes/crop_rps_b_detail.png",
        "codes/crop_control_riser_mid.png",
    ]

    call_specs = [
        {
            "call_id": "main-01",
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "setup",
            "agent": "Main",
            "purpose": "Inventory resources, create crops, visually inspect key ambiguity points.",
            "input_text_tokens": 2200,
            "images": precision_images,
            "output_low": 250,
            "output_expected": 700,
            "output_high": 1400,
            "reasoning_low": 600,
            "reasoning_expected": 1800,
            "reasoning_high": 3600,
            "usage_object_available": "not_exposed",
        },
        {
            "call_id": "subagent-01",
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "01",
            "agent": "Diego",
            "purpose": "High-recall extraction of all plausible nodes/edges from raw and aids.",
            "input_text_tokens": 3300,
            "images": common_images,
            "output_low": 1200,
            "output_expected": 2600,
            "output_high": 4200,
            "reasoning_low": 2500,
            "reasoning_expected": 7000,
            "reasoning_high": 14000,
            "usage_object_available": "not_exposed",
        },
        {
            "call_id": "subagent-02",
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "02",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego round 1 with detailed ambiguity crops.",
            "input_text_tokens": 5200,
            "images": precision_images,
            "output_low": 1200,
            "output_expected": 2600,
            "output_high": 4200,
            "reasoning_low": 2500,
            "reasoning_expected": 7000,
            "reasoning_high": 14000,
            "usage_object_available": "not_exposed",
        },
        {
            "call_id": "subagent-03",
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "03",
            "agent": "Diego",
            "purpose": "High-recall saturation check after Jennifer review.",
            "input_text_tokens": 850,
            "images": [],
            "output_low": 120,
            "output_expected": 250,
            "output_high": 600,
            "reasoning_low": 250,
            "reasoning_expected": 800,
            "reasoning_high": 1800,
            "usage_object_available": "not_exposed",
        },
        {
            "call_id": "subagent-04",
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "04",
            "agent": "Jennifer",
            "purpose": "Final precision saturation close-out.",
            "input_text_tokens": 450,
            "images": [],
            "output_low": 100,
            "output_expected": 220,
            "output_high": 500,
            "reasoning_low": 200,
            "reasoning_expected": 650,
            "reasoning_high": 1500,
            "usage_object_available": "not_exposed",
        },
        {
            "call_id": "main-02",
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "artifact",
            "agent": "Main",
            "purpose": "Generate matrices, validate counts, and prepare final report.",
            "input_text_tokens": 2600,
            "images": [],
            "output_low": 300,
            "output_expected": 800,
            "output_high": 1600,
            "reasoning_low": 600,
            "reasoning_expected": 1800,
            "reasoning_high": 3600,
            "usage_object_available": "not_exposed",
        },
    ]

    usage_rows = []
    total_low = total_expected = total_high = 0
    for spec in call_specs:
        image_tokens = sum(token_by_artifact.get(img, 0) for img in spec["images"])
        input_tokens = spec["input_text_tokens"] + image_tokens
        low = input_tokens + spec["output_low"] + spec["reasoning_low"]
        expected = input_tokens + spec["output_expected"] + spec["reasoning_expected"]
        high = input_tokens + spec["output_high"] + spec["reasoning_high"]
        total_low += low
        total_expected += expected
        total_high += high
        usage_rows.append(
            {
                "call_id": spec["call_id"],
                "document": spec["document"],
                "iteration": spec["iteration"],
                "round": spec["round"],
                "agent": spec["agent"],
                "purpose": spec["purpose"],
                "input_tokens_est": input_tokens,
                "cached_input_tokens_est": 0,
                "image_file_input_tokens_est": image_tokens,
                "output_tokens_low": spec["output_low"],
                "output_tokens_expected": spec["output_expected"],
                "output_tokens_high": spec["output_high"],
                "reasoning_tokens_low": spec["reasoning_low"],
                "reasoning_tokens_expected": spec["reasoning_expected"],
                "reasoning_tokens_high": spec["reasoning_high"],
                "total_tokens_low": low,
                "total_tokens_expected": expected,
                "total_tokens_high": high,
                "usage_object_available": spec["usage_object_available"],
                "notes": "No OPENAI_API_KEY was available, so Responses input-token endpoint and response usage objects could not be collected here.",
            }
        )

    write_csv(
        RESULTS / "model_call_usage_estimates.csv",
        [
            "call_id",
            "document",
            "iteration",
            "round",
            "agent",
            "purpose",
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
                "method": "Local estimate: chars/4 for text plus OpenAI-style high-detail image tile estimate (85 + 170 per 512px tile after scaling); low/expected/high bands for unknown output and reasoning.",
            }
        ],
    )


def validate_matrix(edges):
    node_set = set(NODES)
    missing = sorted({n for edge in edges for n in edge if n not in node_set})
    if missing:
        raise SystemExit(f"Unknown edge node(s): {missing}")
    if len(COMPONENT_NODES) != 89:
        raise SystemExit(f"Expected 89 component labels, got {len(COMPONENT_NODES)}")
    if len(LOGICAL_NODES) != 11:
        raise SystemExit(f"Expected 11 logical nodes, got {len(LOGICAL_NODES)}")
    if len(NODES) != 100:
        raise SystemExit(f"Expected 100 total nodes, got {len(NODES)}")
    if len(POWER_EDGES) != 86:
        raise SystemExit(f"Expected 86 solid/DC power edges, got {len(POWER_EDGES)}")
    if len(FINAL_EDGES) != 100:
        raise SystemExit(f"Expected 100 final drawn connections, got {len(FINAL_EDGES)}")
    if len({edge_key(edge) for edge in edges}) != len(edges):
        raise SystemExit("Duplicate undirected edge detected")


def main():
    validate_matrix(FINAL_EDGES)

    node_rows = []
    logical = set(LOGICAL_NODES)
    for idx, node in enumerate(NODES, start=1):
        node_rows.append(
            {
                "node_index": idx,
                "node_name": node,
                "node_type": "logical_bus_or_reference" if node in logical else "component",
                "source": "visible_raw_label_normalized" if node in logical else "component_visual_ocr_labels.csv",
                "included_in_final_matrix": "yes",
            }
        )
    write_csv(RESULTS / "nodes.csv", ["node_index", "node_name", "node_type", "source", "included_in_final_matrix"], node_rows)

    for definition in ROUND_DEFINITIONS:
        write_matrix(RESULTS / f"{definition['file_stem']}_matrix.csv", definition["edges"])
        write_edge_file(RESULTS / f"{definition['file_stem']}_edges.csv", definition["edges"])

    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_edge_file(RESULTS / "final_connectivity_edges.csv", FINAL_EDGES)

    special_rows = []
    for idx, (a, b, kind, note) in enumerate(SPECIAL_EDGES, start=1):
        special_rows.append(
            {
                "edge_id": f"S-{idx:03d}",
                "node_a": a,
                "node_b": b,
                "edge_kind": kind,
                "status_note": note,
                "included_in_final_matrix": "yes",
            }
        )
    write_csv(
        RESULTS / "special_status_edges.csv",
        ["edge_id", "node_a", "node_b", "edge_kind", "status_note", "included_in_final_matrix"],
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

Final interpretation: all visible drawn electrical connections from the raw schematic, using the raw title-block count of 100 visible components and 100 visible connections as a sanity check.

Artifacts:
- `final_connectivity_matrix.csv`: 100 x 100 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 100 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `special_status_edges.csv`: N.O. tie, ground-reference, control-power, signal, interlock, and terminal-control edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.
- `local_artifact_token_counts.csv`: local file/image token estimate inputs.

Counts:
- Component-label nodes from CSV: {len(COMPONENT_NODES)}
- Explicit visible logical/reference nodes: {len(LOGICAL_NODES)}
- Total matrix nodes: {len(NODES)}
- Final drawn connections: {len(FINAL_EDGES)}

Notes:
- `BUS-TIE-41` is included as a drawn normally-open tie connection, with status metadata.
- `GND-1E` is represented by two dot-dash ground-reference edges to `BUS-416A` and `BUS-416B`.
- `GND-A`, `GND-B`, and `AFW-B2` were not promoted to matrix nodes.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")

    print(f"nodes={len(NODES)} final_edges={len(FINAL_EDGES)} power_edges={len(POWER_EDGES)}")


if __name__ == "__main__":
    main()
