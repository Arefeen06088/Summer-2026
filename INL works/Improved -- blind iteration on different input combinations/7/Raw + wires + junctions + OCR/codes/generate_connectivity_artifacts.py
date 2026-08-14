import csv
import math
import os
import struct
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

DOC_ID = "7"
ITERATION = "1"


LOGICAL_NODES = [
    "BUS-13A",
    "BUS-13B",
    "BUS-4A",
    "BUS-4B",
    "LC-480A",
    "LC-480B",
    "LC-480C",
    "LC-480D",
    "BUS-125DCA",
    "BUS-125DCB",
]


def read_component_nodes():
    path = BASE / "component_visual_ocr_labels.csv"
    nodes = []
    seen = set()
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (
                row.get("normalized_label")
                or row.get("final_label")
                or row.get("normalized_text")
                or row.get("recognized_text")
                or ""
            ).strip()
            if name and name not in seen:
                seen.add(name)
                nodes.append(name)
    return nodes


COMPONENT_NODES = read_component_nodes()
NODES = COMPONENT_NODES + LOGICAL_NODES


SOLID_EDGES = [
    ("GEN-G01", "ISO-GEN-1"),
    ("ISO-GEN-1", "CB-GEN-A"),
    ("CB-GEN-A", "BUS-13A"),
    ("OFFSITE-345", "DS-SAT-1"),
    ("DS-SAT-1", "TR-SAT-A"),
    ("TR-SAT-A", "CB-SAT-A"),
    ("CB-SAT-A", "BUS-4A"),
    ("DS-SAT-1", "TR-SAT-B"),
    ("TR-SAT-B", "CB-SAT-B"),
    ("CB-SAT-B", "BUS-4B"),
    ("BUS-13A", "CB-UAT-A"),
    ("CB-UAT-A", "TR-UAT-A"),
    ("TR-UAT-A", "BUS-4A"),
    ("DG-1A", "CB-DG-A"),
    ("CB-DG-A", "BUS-4A"),
    ("BUS-13A", "CB-TIE-13"),
    ("CB-TIE-13", "BUS-13B"),
    ("BUS-4A", "CB-TIE-4"),
    ("CB-TIE-4", "BUS-4B"),
    ("BUS-13B", "CB-UAT-B"),
    ("CB-UAT-B", "TR-UAT-B"),
    ("TR-UAT-B", "BUS-4B"),
    ("DG-1B", "CB-DG-B"),
    ("CB-DG-B", "BUS-4B"),
    ("BUS-4A", "CB-480A"),
    ("CB-480A", "TR-480A"),
    ("TR-480A", "LC-480A"),
    ("BUS-4A", "CB-480B"),
    ("CB-480B", "TR-480B"),
    ("TR-480B", "LC-480B"),
    ("BUS-4B", "CB-480C"),
    ("CB-480C", "TR-480C"),
    ("TR-480C", "LC-480C"),
    ("BUS-4B", "CB-480D"),
    ("CB-480D", "TR-480D"),
    ("TR-480D", "LC-480D"),
    ("LC-480A", "CB-MCC-A1"),
    ("CB-MCC-A1", "MCC-A1"),
    ("LC-480A", "CB-MCC-A2"),
    ("CB-MCC-A2", "MCC-A2"),
    ("LC-480B", "CB-MCC-B1"),
    ("CB-MCC-B1", "MCC-B1"),
    ("LC-480B", "CB-MCC-B2"),
    ("CB-MCC-B2", "MCC-B2"),
    ("LC-480C", "CB-MCC-C1"),
    ("CB-MCC-C1", "MCC-C1"),
    ("LC-480C", "CB-MCC-C2"),
    ("CB-MCC-C2", "MCC-C2"),
    ("LC-480D", "CB-MCC-D1"),
    ("CB-MCC-D1", "MCC-D1"),
    ("LC-480D", "CB-MCC-D2"),
    ("CB-MCC-D2", "MCC-D2"),
    ("MCC-A1", "CB-P201A"),
    ("CB-P201A", "PUMP-P201A"),
    ("MCC-A1", "CB-MOV101A"),
    ("CB-MOV101A", "MOV-101A"),
    ("MCC-A1", "CB-FAN101A"),
    ("CB-FAN101A", "FAN-F101A"),
    ("MCC-A2", "CB-P202A"),
    ("CB-P202A", "PUMP-P202A"),
    ("MCC-A2", "CB-MOV102A"),
    ("CB-MOV102A", "MOV-102A"),
    ("MCC-A2", "CB-HTR101A"),
    ("CB-HTR101A", "HTR-H101A"),
    ("MCC-B1", "CB-P201B"),
    ("CB-P201B", "PUMP-P201B"),
    ("MCC-B1", "CB-MOV101B"),
    ("CB-MOV101B", "MOV-101B"),
    ("MCC-B1", "CB-FAN101B"),
    ("CB-FAN101B", "FAN-F101B"),
    ("MCC-B2", "CB-P202B"),
    ("CB-P202B", "PUMP-P202B"),
    ("MCC-B2", "CB-MOV102B"),
    ("CB-MOV102B", "MOV-102B"),
    ("MCC-B2", "CB-HTR101B"),
    ("CB-HTR101B", "HTR-H101B"),
    ("MCC-C1", "CB-P301A"),
    ("CB-P301A", "PUMP-P301A"),
    ("MCC-C1", "CB-MOV201A"),
    ("CB-MOV201A", "MOV-201A"),
    ("MCC-C1", "CB-FAN201A"),
    ("CB-FAN201A", "FAN-F201A"),
    ("MCC-C2", "CB-P302A"),
    ("CB-P302A", "PUMP-P302A"),
    ("MCC-C2", "CB-MOV202A"),
    ("CB-MOV202A", "MOV-202A"),
    ("MCC-C2", "CB-HTR201A"),
    ("CB-HTR201A", "HTR-H201A"),
    ("MCC-D1", "CB-P301B"),
    ("CB-P301B", "PUMP-P301B"),
    ("MCC-D1", "CB-MOV201B"),
    ("CB-MOV201B", "MOV-201B"),
    ("MCC-D1", "CB-FAN201B"),
    ("CB-FAN201B", "FAN-F201B"),
    ("MCC-D2", "CB-P302B"),
    ("CB-P302B", "PUMP-P302B"),
    ("MCC-D2", "CB-MOV202B"),
    ("CB-MOV202B", "MOV-202B"),
    ("MCC-D2", "CB-HTR201B"),
    ("CB-HTR201B", "HTR-H201B"),
    ("LC-480A", "BAT-125A"),
    ("BAT-125A", "BCHG-125A"),
    ("BAT-125A", "BUS-125DCA"),
    ("BCHG-125A", "BUS-125DCA"),
    ("BUS-125DCA", "INV-120A"),
    ("BUS-125DCA", "PPS-A"),
    ("LC-480D", "BCHG-125B"),
    ("BAT-125B", "BUS-125DCB"),
    ("BCHG-125B", "BUS-125DCB"),
    ("BUS-125DCB", "INV-120B"),
    ("BUS-125DCB", "PPS-B"),
]


DASHED_EDGES = [
    ("MCC-A1", "PNL-AC-CR1"),
    ("MCC-B1", "PNL-AC-CR1"),
    ("MCC-C1", "PNL-AC-CR2"),
    ("MCC-D1", "PNL-AC-CR2"),
    ("INV-120A", "UPS-120A"),
    ("UPS-120A", "PNL-AC-CR1"),
    ("PNL-AC-CR1", "PPS-A"),
    ("UPS-120A", "ANN-101"),
    ("ANN-101", "PPS-A"),
    ("ANN-101", "RELAY-K101"),
    ("PNL-AC-CR1", "RELAY-K101"),
    ("PPS-A", "RELAY-K101"),
    ("PPS-A", "RELAY-K102"),
    ("RELAY-K101", "RELAY-K102"),
    ("RELAY-K102", "SR-101"),
    ("ANN-101", "SR-101"),
    ("INV-120B", "UPS-120B"),
    ("UPS-120B", "PNL-AC-CR2"),
    ("PNL-AC-CR2", "PPS-B"),
    ("UPS-120B", "ANN-201"),
    ("ANN-201", "PPS-B"),
    ("ANN-201", "RELAY-K201"),
    ("PNL-AC-CR2", "RELAY-K201"),
    ("PPS-B", "RELAY-K201"),
    ("PPS-B", "RELAY-K202"),
    ("RELAY-K201", "RELAY-K202"),
    ("SR-101", "ANN-201"),
    ("RELAY-K101", "RELAY-K201"),
    ("RELAY-K102", "RELAY-K202"),
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


SOLID_EDGES = unique_ordered_edges(SOLID_EDGES)
DASHED_EDGES = unique_ordered_edges(DASHED_EDGES)
FINAL_EDGES = unique_ordered_edges(SOLID_EDGES + DASHED_EDGES)


ROUND_DEFINITIONS = [
    {
        "round": "01",
        "agent": "Diego",
        "file_stem": "round_01_diego_high_recall",
        "interpretation": "all_visible_connections_high_recall",
        "edges": FINAL_EDGES,
        "notes": "Diego proposed a 120-node/140-edge graph matching the raw revision-status count.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "file_stem": "round_02_jennifer_precision",
        "interpretation": "all_visible_connections_precision_review",
        "edges": FINAL_EDGES,
        "notes": "Jennifer retained Diego's proposal unchanged after checking DC and dashed control endpoints.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "file_stem": "round_03_diego_saturation",
        "interpretation": "all_visible_connections_saturated",
        "edges": FINAL_EDGES,
        "notes": "Diego saturation check accepted Jennifer's no-change review.",
    },
    {
        "round": "04",
        "agent": "Jennifer",
        "file_stem": "round_04_jennifer_final",
        "interpretation": "all_visible_connections_final",
        "edges": FINAL_EDGES,
        "notes": "Final precision close-out after Diego agreement.",
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


def edge_kind_and_note(a, b):
    if edge_key((a, b)) in {edge_key(e) for e in DASHED_EDGES}:
        return "control_trip_status_alarm_dashed", "Dashed control/trip/status/alarm circuit with visually supported endpoints."
    if a.startswith("BUS-125") or b.startswith("BUS-125") or "BCHG" in a or "BCHG" in b or "BAT-125" in a or "BAT-125" in b or "INV-120" in a or "INV-120" in b:
        return "solid_dc_power_feeder", "Solid DC/control-power feeder connection."
    return "solid_power_feeder", "Solid power/source/load feeder connection."


def write_edge_file(path, edges):
    rows = []
    for idx, (a, b) in enumerate(edges, start=1):
        kind, note = edge_kind_and_note(a, b)
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
        "raw -- synthetic_npp_electrical_schematic_clean (1).png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
        "wires_mask.png",
        "component_visual_ocr_labels.csv",
        "wire_nodes.csv",
        "codes/crop_top_13kv_416_sources.png",
        "codes/crop_top_notes_legend_status.png",
        "codes/crop_title_block.png",
        "codes/crop_train_a_480_loads.png",
        "codes/crop_train_b_480_loads.png",
        "codes/crop_train_a_dc_control.png",
        "codes/crop_train_b_dc_control.png",
        "codes/crop_bus_tie_13_detail.png",
        "codes/crop_bus_tie_4_detail.png",
        "codes/crop_mcc_a_detail.png",
        "codes/crop_mcc_b_detail.png",
        "codes/crop_control_cross_bottom.png",
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

    diego_images = [
        "raw -- synthetic_npp_electrical_schematic_clean (1).png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "codes/crop_top_13kv_416_sources.png",
        "codes/crop_top_notes_legend_status.png",
        "codes/crop_title_block.png",
        "codes/crop_train_a_480_loads.png",
        "codes/crop_train_b_480_loads.png",
        "codes/crop_train_a_dc_control.png",
        "codes/crop_train_b_dc_control.png",
        "codes/crop_bus_tie_13_detail.png",
        "codes/crop_bus_tie_4_detail.png",
        "codes/crop_mcc_a_detail.png",
        "codes/crop_mcc_b_detail.png",
        "codes/crop_control_cross_bottom.png",
    ]
    jennifer_images = [
        "raw -- synthetic_npp_electrical_schematic_clean (1).png",
        "wire_nodes_overlay.png",
        "codes/crop_top_13kv_416_sources.png",
        "codes/crop_train_a_480_loads.png",
        "codes/crop_train_b_480_loads.png",
        "codes/crop_train_a_dc_control.png",
        "codes/crop_train_b_dc_control.png",
        "codes/crop_control_cross_bottom.png",
        "codes/crop_bus_tie_13_detail.png",
        "codes/crop_bus_tie_4_detail.png",
        "codes/crop_top_notes_legend_status.png",
    ]

    call_specs = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "purpose": "Inventory resources, create crops, inspect notes/revision and ambiguity points.",
            "input_text_tokens": 3300,
            "images": diego_images,
            "output_low": 350,
            "output_expected": 900,
            "output_high": 1800,
            "reasoning_low": 900,
            "reasoning_expected": 2400,
            "reasoning_high": 5200,
        },
        {
            "call_id": "subagent-01",
            "round": "01",
            "agent": "Diego",
            "purpose": "High-recall extraction of 120-node/140-edge graph.",
            "input_text_tokens": 5100,
            "images": diego_images,
            "output_low": 2600,
            "output_expected": 5200,
            "output_high": 8200,
            "reasoning_low": 3500,
            "reasoning_expected": 9000,
            "reasoning_high": 18000,
        },
        {
            "call_id": "subagent-02",
            "round": "02",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego edge list and bottom control/DC uncertainties.",
            "input_text_tokens": 8200,
            "images": jennifer_images,
            "output_low": 700,
            "output_expected": 1500,
            "output_high": 3000,
            "reasoning_low": 2500,
            "reasoning_expected": 6500,
            "reasoning_high": 14000,
        },
        {
            "call_id": "subagent-03",
            "round": "03",
            "agent": "Diego",
            "purpose": "Saturation check after Jennifer no-change review.",
            "input_text_tokens": 450,
            "images": [],
            "output_low": 100,
            "output_expected": 220,
            "output_high": 550,
            "reasoning_low": 250,
            "reasoning_expected": 750,
            "reasoning_high": 1800,
        },
        {
            "call_id": "subagent-04",
            "round": "04",
            "agent": "Jennifer",
            "purpose": "Final precision saturation close-out.",
            "input_text_tokens": 420,
            "images": [],
            "output_low": 100,
            "output_expected": 200,
            "output_high": 500,
            "reasoning_low": 250,
            "reasoning_expected": 700,
            "reasoning_high": 1600,
        },
        {
            "call_id": "main-02",
            "round": "artifact",
            "agent": "Main",
            "purpose": "Generate matrices, validate counts, and prepare final report.",
            "input_text_tokens": 3600,
            "images": [],
            "output_low": 350,
            "output_expected": 900,
            "output_high": 1800,
            "reasoning_low": 900,
            "reasoning_expected": 2400,
            "reasoning_high": 5200,
        },
    ]

    rows = []
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
        rows.append(
            {
                "call_id": spec["call_id"],
                "document": DOC_ID,
                "iteration": ITERATION,
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
                "usage_object_available": "not_exposed",
                "notes": "No OPENAI_API_KEY was available, so the Responses input-token endpoint and response usage objects could not be collected here.",
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
        rows,
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


def validate():
    node_set = set(NODES)
    missing = sorted({n for edge in FINAL_EDGES for n in edge if n not in node_set})
    if missing:
        raise SystemExit(f"Unknown edge node(s): {missing}")
    if len(COMPONENT_NODES) != 110:
        raise SystemExit(f"Expected 110 component labels, got {len(COMPONENT_NODES)}")
    if len(LOGICAL_NODES) != 10:
        raise SystemExit(f"Expected 10 logical nodes, got {len(LOGICAL_NODES)}")
    if len(NODES) != 120:
        raise SystemExit(f"Expected 120 total nodes, got {len(NODES)}")
    if len(SOLID_EDGES) != 111:
        raise SystemExit(f"Expected 111 solid edges, got {len(SOLID_EDGES)}")
    if len(DASHED_EDGES) != 29:
        raise SystemExit(f"Expected 29 dashed edges, got {len(DASHED_EDGES)}")
    if len(FINAL_EDGES) != 140:
        raise SystemExit(f"Expected 140 final edges, got {len(FINAL_EDGES)}")


def main():
    validate()

    logical = set(LOGICAL_NODES)
    node_rows = []
    for idx, node in enumerate(NODES, start=1):
        node_rows.append(
            {
                "node_index": idx,
                "node_name": node,
                "node_type": "logical_bus" if node in logical else "component",
                "source": "visible_raw_bus_label" if node in logical else "component_visual_ocr_labels.csv",
                "included_in_final_matrix": "yes",
            }
        )
    write_csv(RESULTS / "nodes.csv", ["node_index", "node_name", "node_type", "source", "included_in_final_matrix"], node_rows)

    for definition in ROUND_DEFINITIONS:
        write_matrix(RESULTS / f"{definition['file_stem']}_matrix.csv", definition["edges"])
        write_edge_file(RESULTS / f"{definition['file_stem']}_edges.csv", definition["edges"])

    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_edge_file(RESULTS / "final_connectivity_edges.csv", FINAL_EDGES)

    status_rows = []
    for idx, (a, b) in enumerate(DASHED_EDGES, start=1):
        status_rows.append(
            {
                "edge_id": f"S-{idx:03d}",
                "node_a": a,
                "node_b": b,
                "edge_kind": "control_trip_status_alarm_dashed",
                "status_note": "Dashed control/trip/status/alarm circuit.",
                "included_in_final_matrix": "yes",
            }
        )
    write_csv(RESULTS / "special_status_edges.csv", ["edge_id", "node_a", "node_b", "edge_kind", "status_note", "included_in_final_matrix"], status_rows)

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

Final interpretation: all visually supported solid power/DC feeder and dashed control/trip/status/alarm connections from the raw schematic.

Artifacts:
- `final_connectivity_matrix.csv`: 120 x 120 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 140 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `special_status_edges.csv`: dashed control/trip/status/alarm edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.

Counts:
- Component-label nodes from CSV: {len(COMPONENT_NODES)}
- Explicit visible logical bus nodes: {len(LOGICAL_NODES)}
- Total matrix nodes: {len(NODES)}
- Solid power/DC feeder edges: {len(SOLID_EDGES)}
- Dashed control/trip/status/alarm edges: {len(DASHED_EDGES)}
- Final drawn connections: {len(FINAL_EDGES)}

Notes:
- Raw revision status says `120 NODES / 140 EDGES`; the final graph matches it.
- Crossings without dots were not encoded as edges.
- `BAT-125B--BCHG-125B` is not included.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")

    print(f"nodes={len(NODES)} final_edges={len(FINAL_EDGES)} solid={len(SOLID_EDGES)} dashed={len(DASHED_EDGES)}")


if __name__ == "__main__":
    main()
