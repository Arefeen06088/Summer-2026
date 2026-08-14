import csv
import math
import os
import struct
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

DOC_ID = "6"
ITERATION = "1"


LOGICAL_NODES = [
    "SWYD-BUS-A",
    "SWYD-BUS-B",
    "BUS-6KV-A",
    "BUS-6KV-B",
    "BUS-4KV-N",
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


POWER_EDGES = [
    ("GEN-G201", "IPB-201"),
    ("IPB-201", "CB-GEN-201"),
    ("CB-GEN-201", "GSU-201"),
    ("GSU-201", "SWYD-BUS-A"),
    ("SWYD-BUS-A", "CB-GRID-A"),
    ("CB-GRID-A", "GRID-230A"),
    ("SWYD-BUS-B", "CB-GRID-B"),
    ("CB-GRID-B", "GRID-230B"),
    ("SWYD-BUS-A", "CB-TIE-230"),
    ("CB-TIE-230", "SWYD-BUS-B"),
    ("IPB-201", "TR-UAT-201"),
    ("IPB-201", "TR-UAT-202"),
    ("SWYD-BUS-A", "TR-SST-201"),
    ("SWYD-BUS-B", "TR-SST-202"),
    ("TR-UAT-201", "CB-UAT-1"),
    ("CB-UAT-1", "BUS-6KV-A"),
    ("TR-SST-201", "CB-SST-1"),
    ("CB-SST-1", "BUS-6KV-A"),
    ("DG-201A", "CB-DG-A"),
    ("CB-DG-A", "ATS-A"),
    ("ATS-A", "BUS-6KV-A"),
    ("BUS-6KV-A", "CB-TIE-6KV"),
    ("CB-TIE-6KV", "BUS-6KV-B"),
    ("BUS-6KV-A", "PT-6KV-A"),
    ("BUS-6KV-A", "TR-480A"),
    ("BUS-6KV-A", "DS-6KV-A"),
    ("DS-6KV-A", "BUS-4KV-N"),
    ("TR-UAT-202", "CB-UAT-2"),
    ("CB-UAT-2", "BUS-6KV-B"),
    ("TR-SST-202", "CB-SST-2"),
    ("CB-SST-2", "BUS-6KV-B"),
    ("DG-201B", "CB-DG-B"),
    ("CB-DG-B", "ATS-B"),
    ("ATS-B", "BUS-6KV-B"),
    ("BUS-6KV-B", "PT-6KV-B"),
    ("BUS-6KV-B", "TR-480B"),
    ("BUS-6KV-B", "DS-6KV-B"),
    ("DS-6KV-B", "BUS-4KV-N"),
    ("BUS-4KV-N", "TR-480N"),
    ("TR-480A", "CB-LC-A1"),
    ("CB-LC-A1", "LC-480A"),
    ("LC-480A", "MCC-CCW-A"),
    ("LC-480A", "MCC-SW-A"),
    ("LC-480A", "MCC-HPI-A"),
    ("LC-480A", "MCC-VENT-A"),
    ("MCC-CCW-A", "JBX-CCW-A"),
    ("JBX-CCW-A", "PUMP-CCW-A"),
    ("MCC-CCW-A", "MOV-CCW-201A"),
    ("MCC-SW-A", "JBX-SW-A"),
    ("JBX-SW-A", "PUMP-SW-A"),
    ("MCC-HPI-A", "PUMP-HPI-A"),
    ("MCC-HPI-A", "MOV-SI-201A"),
    ("MCC-VENT-A", "FAN-CR-A"),
    ("TR-480B", "CB-LC-B1"),
    ("CB-LC-B1", "LC-480B"),
    ("LC-480B", "MCC-CCW-B"),
    ("LC-480B", "MCC-SW-B"),
    ("LC-480B", "MCC-HPI-B"),
    ("LC-480B", "MCC-VENT-B"),
    ("MCC-CCW-B", "JBX-CCW-B"),
    ("JBX-CCW-B", "PUMP-CCW-B"),
    ("MCC-CCW-B", "MOV-CCW-201B"),
    ("MCC-SW-B", "JBX-SW-B"),
    ("JBX-SW-B", "PUMP-SW-B"),
    ("MCC-HPI-B", "PUMP-HPI-B"),
    ("MCC-HPI-B", "MOV-SI-201B"),
    ("MCC-VENT-B", "FAN-CR-B"),
    ("TR-480N", "CB-LC-N1"),
    ("CB-LC-N1", "LC-480N"),
    ("LC-480N", "LP-N-A"),
    ("LP-N-A", "HTR-BLDG-A"),
    ("LC-480N", "LP-N-B"),
    ("LP-N-B", "HTR-BLDG-B"),
    ("LC-480A", "CHGR-A"),
    ("CHGR-A", "BAT-125A"),
    ("CHGR-A", "PNL-DC-A"),
    ("BAT-125A", "PNL-DC-A"),
    ("PNL-DC-A", "REC-A"),
    ("REC-A", "INV-A"),
    ("INV-A", "UPS-A"),
    ("LC-480B", "CHGR-B"),
    ("CHGR-B", "BAT-125B"),
    ("CHGR-B", "PNL-DC-B"),
    ("BAT-125B", "PNL-DC-B"),
    ("PNL-DC-B", "REC-B"),
    ("REC-B", "INV-B"),
    ("INV-B", "UPS-B"),
]


FIRM_SENSING_EDGES = [
    ("CT-EDG-A", "DG-201A"),
    ("CT-EDG-B", "DG-201B"),
    ("UV-SENS-A", "LC-480A"),
    ("UV-SENS-B", "LC-480B"),
]


FIRM_CONTROL_EDGES = [
    ("PNL-INST-A", "RELAY-UV-A"),
    ("PNL-INST-B", "RELAY-UV-B"),
    ("CP-ESFAS-A", "RELAY-SI-A"),
    ("CP-ESFAS-B", "RELAY-SI-B"),
    ("PLC-RPS-A", "RELAY-LOAD-A"),
    ("PLC-RPS-B", "RELAY-LOAD-B"),
    ("JBX-ESF-A", "RELAY-DG-A"),
    ("JBX-ESF-B", "RELAY-DG-B"),
    ("MOV-SI-201A", "FAN-CR-A"),
    ("MOV-SI-201B", "FAN-CR-B"),
    ("CP-ESFAS-A", "JBX-ESF-A"),
    ("CP-ESFAS-B", "JBX-ESF-B"),
    ("PLC-RPS-A", "JBX-ESF-A"),
    ("PLC-RPS-B", "JBX-ESF-B"),
]


PROMOTED_SENSING_EDGES = [
    ("PT-6KV-A", "PNL-INST-A"),
    ("PT-6KV-B", "PNL-INST-B"),
    ("UV-SENS-A", "PNL-INST-A"),
    ("UV-SENS-B", "PNL-INST-B"),
]


PROMOTED_CONTROL_EDGES = [
    ("MCC-HPI-A", "RELAY-LOAD-A"),
    ("MCC-HPI-B", "RELAY-LOAD-B"),
    ("MOV-SI-201A", "RELAY-SI-A"),
    ("MOV-SI-201B", "RELAY-SI-B"),
    ("FAN-CR-A", "RELAY-LOAD-A"),
    ("FAN-CR-B", "RELAY-LOAD-B"),
    ("DG-201A", "RELAY-DG-A"),
    ("DG-201B", "RELAY-DG-B"),
    ("CB-DG-A", "RELAY-DG-A"),
    ("CB-DG-B", "RELAY-DG-B"),
    ("ATS-A", "RELAY-DG-A"),
    ("ATS-B", "RELAY-DG-B"),
    ("UPS-A", "PNL-INST-A"),
    ("UPS-B", "PNL-INST-B"),
    ("UPS-A", "CP-ESFAS-A"),
    ("UPS-B", "CP-ESFAS-B"),
]


GROUND_EDGES = [
    ("BAT-125A", "GND-A"),
    ("REC-A", "GND-A"),
    ("GND-A", "GND-MAIN"),
    ("BAT-125B", "GND-B"),
    ("REC-B", "GND-B"),
    ("GND-B", "GND-MAIN"),
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


FIRM_EDGES = unique_ordered_edges(POWER_EDGES + FIRM_CONTROL_EDGES + FIRM_SENSING_EDGES + GROUND_EDGES)
FINAL_SENSING_EDGES = unique_ordered_edges(FIRM_SENSING_EDGES + PROMOTED_SENSING_EDGES)
FINAL_CONTROL_EDGES = unique_ordered_edges(FIRM_CONTROL_EDGES + PROMOTED_CONTROL_EDGES)
FINAL_EDGES = unique_ordered_edges(POWER_EDGES + FINAL_CONTROL_EDGES + FINAL_SENSING_EDGES + GROUND_EDGES)


ROUND_DEFINITIONS = [
    {
        "round": "01a",
        "agent": "Diego",
        "file_stem": "round_01a_diego_firm",
        "interpretation": "firm_visible_connections",
        "edges": FIRM_EDGES,
        "notes": "Diego firm proposal before candidate promotion.",
    },
    {
        "round": "01b",
        "agent": "Diego",
        "file_stem": "round_01b_diego_high_recall_inclusive",
        "interpretation": "high_recall_inclusive_candidates",
        "edges": FINAL_EDGES,
        "notes": "Diego high-recall inclusive proposal including the 20 candidate edges later promoted by Jennifer.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "file_stem": "round_02_jennifer_precision",
        "interpretation": "precision_review_finalized_candidates",
        "edges": FINAL_EDGES,
        "notes": "Jennifer promoted all 20 Diego candidate edges and removed none.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "file_stem": "round_03_diego_saturation",
        "interpretation": "saturated_after_precision_review",
        "edges": FINAL_EDGES,
        "notes": "Diego accepted Jennifer's promoted candidate set.",
    },
    {
        "round": "04",
        "agent": "Jennifer",
        "file_stem": "round_04_jennifer_final",
        "interpretation": "final_saturated_graph",
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
    key = edge_key((a, b))
    if key in {edge_key(e) for e in FINAL_CONTROL_EDGES}:
        return "control_interlock_dashed", "Dashed control/interlock connection with visually supported endpoints."
    if key in {edge_key(e) for e in FINAL_SENSING_EDGES}:
        return "sensing_instrument_dashed", "Dashed/dot sensing or instrument connection with visually supported endpoints."
    if key in {edge_key(e) for e in GROUND_EDGES}:
        return "ground_bond_dotted", "Dotted ground-bond connection."
    return "solid_power_feeder", "Solid power feeder/load/source connection."


def write_edge_file(path, edges, final_edges):
    final_keys = {edge_key(e) for e in final_edges}
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
                "included_in_final_matrix": "yes" if edge_key((a, b)) in final_keys else "no",
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
        "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
        "wires_mask.png",
        "component_visual_ocr_labels.csv",
        "wire_nodes.csv",
        "codes/crop_top_generator_switchyard.png",
        "codes/crop_top_legend.png",
        "codes/crop_mv_safety_buses_full.png",
        "codes/crop_mv_left_detail.png",
        "codes/crop_mv_right_detail.png",
        "codes/crop_loads_left.png",
        "codes/crop_loads_right.png",
        "codes/crop_dc_ups_bottom.png",
        "codes/crop_esf_rps_bay.png",
        "codes/crop_esf_top_detail.png",
        "codes/crop_esf_mid_detail.png",
        "codes/crop_notes.png",
        "codes/crop_title_block.png",
        "codes/crop_ground_grid_bottom.png",
        "codes/crop_center_ups_loads.png",
        "codes/crop_ct_edg_a_detail.png",
        "codes/crop_ct_edg_b_detail.png",
        "codes/crop_pt_uv_a_detail.png",
        "codes/crop_pt_uv_b_detail.png",
        "codes/crop_dc_a_detail.png",
        "codes/crop_dc_b_detail.png",
        "codes/crop_esf_left_inputs_detail.png",
        "codes/crop_esf_relay_outputs_detail.png",
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
        "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "codes/crop_top_generator_switchyard.png",
        "codes/crop_mv_safety_buses_full.png",
        "codes/crop_mv_left_detail.png",
        "codes/crop_mv_right_detail.png",
        "codes/crop_loads_left.png",
        "codes/crop_loads_right.png",
        "codes/crop_center_ups_loads.png",
        "codes/crop_dc_ups_bottom.png",
        "codes/crop_esf_rps_bay.png",
        "codes/crop_esf_top_detail.png",
        "codes/crop_esf_mid_detail.png",
        "codes/crop_top_legend.png",
        "codes/crop_notes.png",
        "codes/crop_title_block.png",
        "codes/crop_ground_grid_bottom.png",
    ]
    jennifer_images = [
        "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "codes/crop_top_generator_switchyard.png",
        "codes/crop_mv_left_detail.png",
        "codes/crop_mv_right_detail.png",
        "codes/crop_loads_left.png",
        "codes/crop_loads_right.png",
        "codes/crop_center_ups_loads.png",
        "codes/crop_dc_ups_bottom.png",
        "codes/crop_ct_edg_a_detail.png",
        "codes/crop_ct_edg_b_detail.png",
        "codes/crop_pt_uv_a_detail.png",
        "codes/crop_pt_uv_b_detail.png",
        "codes/crop_dc_a_detail.png",
        "codes/crop_dc_b_detail.png",
        "codes/crop_esf_rps_bay.png",
        "codes/crop_esf_left_inputs_detail.png",
        "codes/crop_esf_relay_outputs_detail.png",
        "codes/crop_ground_grid_bottom.png",
        "codes/crop_top_legend.png",
        "codes/crop_notes.png",
        "codes/crop_title_block.png",
    ]

    call_specs = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "purpose": "Inventory resources, create crops, inspect notes/legend and ambiguity points.",
            "input_text_tokens": 3000,
            "images": jennifer_images,
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
            "purpose": "High-recall extraction of nodes, firm edges, and candidate edges.",
            "input_text_tokens": 4600,
            "images": diego_images,
            "output_low": 2200,
            "output_expected": 4300,
            "output_high": 7200,
            "reasoning_low": 3500,
            "reasoning_expected": 9000,
            "reasoning_high": 18000,
        },
        {
            "call_id": "subagent-02",
            "round": "02",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego firm and candidate edges.",
            "input_text_tokens": 7600,
            "images": jennifer_images,
            "output_low": 1200,
            "output_expected": 2500,
            "output_high": 4600,
            "reasoning_low": 3500,
            "reasoning_expected": 9000,
            "reasoning_high": 18000,
        },
        {
            "call_id": "subagent-03",
            "round": "03",
            "agent": "Diego",
            "purpose": "Saturation check after Jennifer promoted all candidates.",
            "input_text_tokens": 950,
            "images": [],
            "output_low": 120,
            "output_expected": 260,
            "output_high": 650,
            "reasoning_low": 300,
            "reasoning_expected": 900,
            "reasoning_high": 2000,
        },
        {
            "call_id": "subagent-04",
            "round": "04",
            "agent": "Jennifer",
            "purpose": "Final precision saturation close-out.",
            "input_text_tokens": 520,
            "images": [],
            "output_low": 100,
            "output_expected": 220,
            "output_high": 550,
            "reasoning_low": 250,
            "reasoning_expected": 750,
            "reasoning_high": 1800,
        },
        {
            "call_id": "main-02",
            "round": "artifact",
            "agent": "Main",
            "purpose": "Generate matrices, validate counts, and prepare final report.",
            "input_text_tokens": 3500,
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
    missing = sorted({n for edge in FIRM_EDGES + FINAL_EDGES for n in edge if n not in node_set})
    if missing:
        raise SystemExit(f"Unknown edge node(s): {missing}")
    if len(COMPONENT_NODES) != 100:
        raise SystemExit(f"Expected 100 component labels, got {len(COMPONENT_NODES)}")
    if len(LOGICAL_NODES) != 5:
        raise SystemExit(f"Expected 5 logical nodes, got {len(LOGICAL_NODES)}")
    if len(NODES) != 105:
        raise SystemExit(f"Expected 105 total nodes, got {len(NODES)}")
    if len(POWER_EDGES) != 87:
        raise SystemExit(f"Expected 87 power edges, got {len(POWER_EDGES)}")
    if len(FIRM_SENSING_EDGES) != 4:
        raise SystemExit(f"Expected 4 firm sensing edges, got {len(FIRM_SENSING_EDGES)}")
    if len(FIRM_CONTROL_EDGES) != 14:
        raise SystemExit(f"Expected 14 firm control edges, got {len(FIRM_CONTROL_EDGES)}")
    if len(GROUND_EDGES) != 6:
        raise SystemExit(f"Expected 6 ground edges, got {len(GROUND_EDGES)}")
    if len(FIRM_EDGES) != 111:
        raise SystemExit(f"Expected 111 firm edges, got {len(FIRM_EDGES)}")
    if len(FINAL_SENSING_EDGES) != 8:
        raise SystemExit(f"Expected 8 final sensing edges, got {len(FINAL_SENSING_EDGES)}")
    if len(FINAL_CONTROL_EDGES) != 30:
        raise SystemExit(f"Expected 30 final control edges, got {len(FINAL_CONTROL_EDGES)}")
    if len(FINAL_EDGES) != 131:
        raise SystemExit(f"Expected 131 final edges, got {len(FINAL_EDGES)}")


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
        write_edge_file(RESULTS / f"{definition['file_stem']}_edges.csv", definition["edges"], FINAL_EDGES)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_edge_file(RESULTS / "final_connectivity_edges.csv", FINAL_EDGES, FINAL_EDGES)

    diff_rows = []
    for a, b in PROMOTED_SENSING_EDGES:
        diff_rows.append({"change": "promote", "node_a": a, "node_b": b, "edge_kind": "sensing_instrument_dashed", "reason": "Jennifer found visual terminal/lane support."})
    for a, b in PROMOTED_CONTROL_EDGES:
        diff_rows.append({"change": "promote", "node_a": a, "node_b": b, "edge_kind": "control_interlock_dashed", "reason": "Jennifer found visual terminal/lane support."})
    write_csv(RESULTS / "round_02_jennifer_promoted_edges.csv", ["change", "node_a", "node_b", "edge_kind", "reason"], diff_rows)

    status_rows = []
    for edge in FINAL_CONTROL_EDGES:
        a, b = edge
        status_rows.append({"edge_id": f"S-{len(status_rows)+1:03d}", "node_a": a, "node_b": b, "edge_kind": "control_interlock_dashed", "status_note": "Dashed control/interlock connection.", "included_in_final_matrix": "yes"})
    for edge in FINAL_SENSING_EDGES:
        a, b = edge
        status_rows.append({"edge_id": f"S-{len(status_rows)+1:03d}", "node_a": a, "node_b": b, "edge_kind": "sensing_instrument_dashed", "status_note": "Dashed/dot sensing or instrument connection.", "included_in_final_matrix": "yes"})
    for edge in GROUND_EDGES:
        a, b = edge
        status_rows.append({"edge_id": f"S-{len(status_rows)+1:03d}", "node_a": a, "node_b": b, "edge_kind": "ground_bond_dotted", "status_note": "Dotted ground bond.", "included_in_final_matrix": "yes"})
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

Final interpretation: all visually supported solid, dashed control/interlock, sensing/instrument, and ground-bond connections from the raw schematic.

Artifacts:
- `final_connectivity_matrix.csv`: 105 x 105 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 131 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `round_02_jennifer_promoted_edges.csv`: the 20 Diego candidate edges promoted by Jennifer.
- `special_status_edges.csv`: non-solid/control/sensing/ground metadata edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.

Counts:
- Component-label nodes from CSV: {len(COMPONENT_NODES)}
- Explicit visible logical bus nodes: {len(LOGICAL_NODES)}
- Total matrix nodes: {len(NODES)}
- Final power edges: {len(POWER_EDGES)}
- Final sensing/instrument edges: {len(FINAL_SENSING_EDGES)}
- Final control/interlock edges: {len(FINAL_CONTROL_EDGES)}
- Final ground-bond edges: {len(GROUND_EDGES)}
- Final drawn connections: {len(FINAL_EDGES)}

Notes:
- Crossings without dots were not encoded as edges.
- No extra DC/UPS bus nodes were added.
- The drawing has no visible title-block component/connection checksum; counts are visual-extraction results.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")

    print(
        f"nodes={len(NODES)} final_edges={len(FINAL_EDGES)} "
        f"power={len(POWER_EDGES)} sensing={len(FINAL_SENSING_EDGES)} "
        f"control={len(FINAL_CONTROL_EDGES)} ground={len(GROUND_EDGES)}"
    )


if __name__ == "__main__":
    main()
