import csv
import math
import os
import struct
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

DOC_ID = "5"
ITERATION = "1"


LOGICAL_NODES = [
    "BUS-SY230",
    "BUS-AUX13A",
    "BUS-AUX13B",
    "BUS-NON1",
    "BUS-416A",
    "BUS-416B",
    "BUS-416C",
    "BUS-416D",
    "GND-GRID",
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


SOLID_SWITCHYARD_AUX = [
    ("GRID-N230", "ISO-230A"),
    ("ISO-230A", "BRK-2301"),
    ("BRK-2301", "BUS-SY230"),
    ("GEN-G101", "GSU-1"),
    ("GSU-1", "BUS-SY230"),
    ("BUS-SY230", "BRK-2302"),
    ("BRK-2302", "ISO-230B"),
    ("ISO-230B", "GRID-S230"),
    ("BUS-SY230", "TR-RAT-1A"),
    ("BUS-SY230", "TR-UAT-1A"),
    ("BUS-SY230", "TR-UAT-1B"),
    ("BUS-SY230", "TR-RAT-1B"),
    ("TR-RAT-1A", "CB-AUX-A"),
    ("TR-UAT-1A", "CB-AUX-A"),
    ("CB-AUX-A", "BUS-AUX13A"),
    ("TR-UAT-1B", "CB-AUX-B"),
    ("TR-RAT-1B", "CB-AUX-B"),
    ("CB-AUX-B", "BUS-AUX13B"),
    ("BUS-AUX13A", "CB-TIE13"),
    ("CB-TIE13", "BUS-AUX13B"),
    ("BUS-AUX13A", "BUS-NON1"),
    ("BUS-NON1", "TR-SAF-C"),
    ("BUS-AUX13A", "TR-SAF-A"),
    ("BUS-AUX13A", "TR-SAF-B"),
    ("BUS-AUX13B", "TR-SAF-C"),
    ("BUS-AUX13B", "TR-SAF-D"),
]


SOLID_SAFETY_416 = [
    ("TR-SAF-A", "CB-SAF-A"),
    ("CB-SAF-A", "BUS-416A"),
    ("EDG-A", "CB-EDG-A"),
    ("CB-EDG-A", "BUS-416A"),
    ("BUS-416A", "CB-TIE-AB"),
    ("CB-TIE-AB", "BUS-416B"),
    ("BUS-416A", "TR-480-A"),
    ("TR-480-A", "CB-LC-A"),
    ("CB-LC-A", "LC-480A"),
    ("TR-SAF-B", "CB-SAF-B"),
    ("CB-SAF-B", "BUS-416B"),
    ("EDG-B", "CB-EDG-B"),
    ("CB-EDG-B", "BUS-416B"),
    ("BUS-416B", "TR-480-B"),
    ("TR-480-B", "CB-LC-B"),
    ("CB-LC-B", "LC-480B"),
    ("TR-SAF-C", "CB-SAF-C"),
    ("CB-SAF-C", "BUS-416C"),
    ("EDG-C", "CB-EDG-C"),
    ("CB-EDG-C", "BUS-416C"),
    ("BUS-416C", "CB-TIE-CD"),
    ("CB-TIE-CD", "BUS-416D"),
    ("BUS-416C", "TR-480-C"),
    ("TR-480-C", "CB-LC-C"),
    ("CB-LC-C", "LC-480C"),
    ("TR-SAF-D", "CB-SAF-D"),
    ("CB-SAF-D", "BUS-416D"),
    ("EDG-D", "CB-EDG-D"),
    ("CB-EDG-D", "BUS-416D"),
    ("BUS-416D", "TR-480-D"),
    ("TR-480-D", "CB-LC-D"),
    ("CB-LC-D", "LC-480D"),
]


SOLID_LOADS_ATS = [
    ("LC-480A", "CB-MCCA1"),
    ("CB-MCCA1", "MCC-1A1"),
    ("MCC-1A1", "PUMP-AFW-A"),
    ("MCC-1A1", "V-MISV-A"),
    ("LC-480A", "CB-MCCA2"),
    ("CB-MCCA2", "MCC-1A2"),
    ("MCC-1A2", "PUMP-CCW-A"),
    ("LC-480A", "XFER-ATS-A"),
    ("LC-480B", "CB-MCCB1"),
    ("CB-MCCB1", "MCC-1B1"),
    ("MCC-1B1", "PUMP-AFW-B"),
    ("MCC-1B1", "V-MISV-B"),
    ("LC-480B", "CB-MCCB2"),
    ("CB-MCCB2", "MCC-1B2"),
    ("MCC-1B2", "PUMP-CCW-B"),
    ("LC-480B", "XFER-ATS-A"),
    ("LC-480C", "CB-MCCC1"),
    ("CB-MCCC1", "MCC-1C1"),
    ("MCC-1C1", "PUMP-RHR-A"),
    ("LC-480C", "CB-MCCC2"),
    ("CB-MCCC2", "MCC-1C2"),
    ("MCC-1C2", "HTR-BATRM-A"),
    ("MCC-1C2", "FAN-CRHV-A"),
    ("LC-480C", "XFER-ATS-B"),
    ("LC-480D", "CB-MCCD1"),
    ("CB-MCCD1", "MCC-1D1"),
    ("MCC-1D1", "PUMP-RHR-B"),
    ("LC-480D", "CB-MCCD2"),
    ("CB-MCCD2", "MCC-1D2"),
    ("MCC-1D2", "HTR-BATRM-B"),
    ("MCC-1D2", "FAN-CRHV-B"),
    ("LC-480D", "XFER-ATS-B"),
]


DIEGO_SOLID_DC = [
    ("XFER-ATS-A", "CHG-125A"),
    ("CHG-125A", "BAT-125A"),
    ("BAT-125A", "PNL-DC-A"),
    ("PNL-DC-A", "INV-UPS-A"),
    ("INV-UPS-A", "UPS-PNL-A"),
    ("RECT-48V-A", "BAT-48V-A"),
    ("BAT-48V-A", "JB-RLY-A"),
    ("JB-RLY-A", "JB-RLY-B"),
    ("JB-RLY-B", "BAT-48V-B"),
    ("BAT-48V-B", "RECT-48V-B"),
    ("XFER-ATS-B", "CHG-125B"),
    ("CHG-125B", "BAT-125B"),
    ("BAT-125B", "PNL-DC-B"),
    ("PNL-DC-B", "INV-UPS-B"),
    ("INV-UPS-B", "UPS-PNL-B"),
]


FINAL_SOLID_DC = [
    ("XFER-ATS-A", "CHG-125A"),
    ("XFER-ATS-A", "RECT-48V-A"),
    ("CHG-125A", "BAT-125A"),
    ("BAT-125A", "PNL-DC-A"),
    ("PNL-DC-A", "INV-UPS-A"),
    ("INV-UPS-A", "UPS-PNL-A"),
    ("RECT-48V-A", "BAT-48V-A"),
    ("BAT-48V-A", "JB-RLY-A"),
    ("JB-RLY-B", "BAT-48V-B"),
    ("BAT-48V-B", "RECT-48V-B"),
    ("XFER-ATS-B", "CHG-125B"),
    ("XFER-ATS-B", "RECT-48V-B"),
    ("CHG-125B", "BAT-125B"),
    ("BAT-125B", "PNL-DC-B"),
    ("PNL-DC-B", "INV-UPS-B"),
    ("INV-UPS-B", "UPS-PNL-B"),
]


DASHED_CONTROL_DIEGO = [
    ("CB-EDG-A", "RELAY-K1A"),
    ("CB-SAF-A", "RELAY-K1A"),
    ("CB-EDG-B", "RELAY-K1B"),
    ("CB-SAF-B", "RELAY-K1B"),
    ("CB-EDG-C", "RELAY-K2A"),
    ("CB-SAF-C", "RELAY-K2A"),
    ("CB-EDG-D", "RELAY-K2B"),
    ("CB-SAF-D", "RELAY-K2B"),
    ("CP-ESFAS-1", "RELAY-K1A"),
    ("CP-ESFAS-1", "RELAY-K1B"),
    ("CP-ESFAS-1", "RELAY-UV-A"),
    ("CP-ESFAS-2", "RELAY-K2A"),
    ("CP-ESFAS-2", "RELAY-K2B"),
    ("CP-ESFAS-2", "RELAY-UV-B"),
    ("CP-ESFAS-2", "RELAY-LOOP-C"),
    ("CP-ESFAS-2", "RELAY-LOOP-D"),
    ("PNL-DC-A", "CP-ESFAS-1"),
    ("PNL-DC-B", "CP-ESFAS-2"),
    ("PNL-DC-A", "PNL-DC-B"),
    ("CP-ESFAS-1", "CP-ESFAS-2"),
]


FINAL_DASHED_CONTROL = [edge for edge in DASHED_CONTROL_DIEGO if set(edge) != {"CP-ESFAS-1", "CP-ESFAS-2"}]


DASH_DOT_SENSING = [
    ("BUS-416A", "RELAY-UV-A"),
    ("BUS-416B", "RELAY-UV-B"),
    ("BUS-416C", "RELAY-LOOP-C"),
    ("BUS-416D", "RELAY-LOOP-D"),
    ("INST-NSSS-A", "CP-ESFAS-1"),
    ("INST-NSSS-B", "CP-ESFAS-2"),
]


DOTTED_GROUND = [
    ("GSU-1", "GND-GRID"),
    ("TR-RAT-1A", "GND-GRID"),
    ("TR-RAT-1B", "GND-GRID"),
    ("PUMP-CCW-A", "GND-GRID"),
    ("PUMP-CCW-B", "GND-GRID"),
    ("FAN-CRHV-A", "GND-GRID"),
    ("FAN-CRHV-B", "GND-GRID"),
    ("BAT-48V-A", "GND-GRID"),
    ("BAT-48V-B", "GND-GRID"),
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


DIEGO_SOLID = unique_ordered_edges(SOLID_SWITCHYARD_AUX + SOLID_SAFETY_416 + SOLID_LOADS_ATS + DIEGO_SOLID_DC)
FINAL_SOLID = unique_ordered_edges(SOLID_SWITCHYARD_AUX + SOLID_SAFETY_416 + SOLID_LOADS_ATS + FINAL_SOLID_DC)
DIEGO_EDGES = unique_ordered_edges(DIEGO_SOLID + DASHED_CONTROL_DIEGO + DASH_DOT_SENSING + DOTTED_GROUND)
FINAL_EDGES = unique_ordered_edges(FINAL_SOLID + FINAL_DASHED_CONTROL + DASH_DOT_SENSING + DOTTED_GROUND)


SPECIAL_STATUS_NOTES = {
    edge_key(("BUS-AUX13A", "CB-TIE13")): ("solid_power_normally_open_tie", "N.O. auxiliary bus tie; drawn connection, not assumed closed."),
    edge_key(("CB-TIE13", "BUS-AUX13B")): ("solid_power_normally_open_tie", "N.O. auxiliary bus tie; drawn connection, not assumed closed."),
    edge_key(("BUS-416A", "CB-TIE-AB")): ("solid_power_normally_open_tie", "N.O. 4.16 kV A/B tie; drawn connection, not assumed closed."),
    edge_key(("CB-TIE-AB", "BUS-416B")): ("solid_power_normally_open_tie", "N.O. 4.16 kV A/B tie; drawn connection, not assumed closed."),
    edge_key(("BUS-416C", "CB-TIE-CD")): ("solid_power_normally_open_tie_lsc", "N.O. 4.16 kV C/D tie with LSC mark; drawn connection, not assumed closed."),
    edge_key(("CB-TIE-CD", "BUS-416D")): ("solid_power_normally_open_tie_lsc", "N.O. 4.16 kV C/D tie with LSC mark; drawn connection, not assumed closed."),
}


ROUND_DEFINITIONS = [
    {
        "round": "01",
        "agent": "Diego",
        "file_stem": "round_01_diego_high_recall",
        "interpretation": "all_visible_connections_high_recall",
        "edges": DIEGO_EDGES,
        "notes": "Initial high-recall graph matched 140 but kept an unsupported JB-RLY-A/JB-RLY-B bridge and CP-ESFAS-1/2 tie while missing ATS-to-rectifier feeds.",
    },
    {
        "round": "02",
        "agent": "Jennifer",
        "file_stem": "round_02_jennifer_precision",
        "interpretation": "all_visible_connections_precision_review",
        "edges": FINAL_EDGES,
        "notes": "Precision diff: add XFER-ATS-A/B to RECT-48V-A/B; remove JB-RLY-A--JB-RLY-B and CP-ESFAS-1--CP-ESFAS-2.",
    },
    {
        "round": "03",
        "agent": "Diego",
        "file_stem": "round_03_diego_saturation",
        "interpretation": "all_visible_connections_saturated",
        "edges": FINAL_EDGES,
        "notes": "Diego saturation pass accepted Jennifer's correction.",
    },
    {
        "round": "04",
        "agent": "Jennifer",
        "file_stem": "round_04_jennifer_final",
        "interpretation": "all_visible_connections_final",
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


def edge_kind_and_note(a, b):
    key = edge_key((a, b))
    if key in SPECIAL_STATUS_NOTES:
        return SPECIAL_STATUS_NOTES[key]
    if key in {edge_key(e) for e in FINAL_DASHED_CONTROL + DASHED_CONTROL_DIEGO}:
        return "control_trip_close_dashed", "Dashed control/trip/close connection with terminal dots."
    if key in {edge_key(e) for e in DASH_DOT_SENSING}:
        return "sensing_instrument_dash_dot", "Dash-dot sensing/instrument connection with terminal dots."
    if key in {edge_key(e) for e in DOTTED_GROUND}:
        return "grounding_conductor_dotted", "Dotted grounding-conductor connection to GND-GRID."
    if "ATS" in a or "ATS" in b or "CHG" in a or "CHG" in b or "RECT" in a or "RECT" in b:
        return "solid_vital_ac_dc_power", "Solid ATS/DC/rectifier feeder connection."
    return "solid_power_feeder", "Solid power feeder/source/load connection."


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
        "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
        "wires_mask.png",
        "component_visual_ocr_labels.csv",
        "wire_nodes.csv",
        "codes/crop_top_switchyard_aux.png",
        "codes/crop_safety_bus_ties.png",
        "codes/crop_train_ab_feeders.png",
        "codes/crop_train_cd_feeders.png",
        "codes/crop_dc_ups_bottom.png",
        "codes/crop_esf_control_bay.png",
        "codes/crop_center_bus_and_dc_ties.png",
        "codes/crop_legend_line_convention.png",
        "codes/crop_title_counts.png",
        "codes/crop_aux_tie_non1_detail.png",
        "codes/crop_ats_a_detail.png",
        "codes/crop_ats_b_detail.png",
        "codes/crop_48v_relay_chain_detail.png",
        "codes/crop_esf_top_detail.png",
        "codes/crop_esf_bottom_instr_detail.png",
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
        "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
        "component_labels_banners_overlay.png",
        "wire_nodes_overlay.png",
        "codes/crop_top_switchyard_aux.png",
        "codes/crop_safety_bus_ties.png",
        "codes/crop_train_ab_feeders.png",
        "codes/crop_train_cd_feeders.png",
        "codes/crop_dc_ups_bottom.png",
        "codes/crop_esf_control_bay.png",
        "codes/crop_center_bus_and_dc_ties.png",
        "codes/crop_legend_line_convention.png",
        "codes/crop_title_counts.png",
    ]
    jennifer_images = [
        "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
        "wire_nodes_overlay.png",
        "codes/crop_top_switchyard_aux.png",
        "codes/crop_aux_tie_non1_detail.png",
        "codes/crop_safety_bus_ties.png",
        "codes/crop_train_ab_feeders.png",
        "codes/crop_train_cd_feeders.png",
        "codes/crop_ats_a_detail.png",
        "codes/crop_ats_b_detail.png",
        "codes/crop_dc_ups_bottom.png",
        "codes/crop_48v_relay_chain_detail.png",
        "codes/crop_esf_control_bay.png",
        "codes/crop_esf_top_detail.png",
        "codes/crop_esf_bottom_instr_detail.png",
        "codes/crop_legend_line_convention.png",
        "codes/crop_title_counts.png",
    ]

    call_specs = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "purpose": "Inventory resources, create crops, inspect title/legend and ambiguity points.",
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
            "purpose": "High-recall extraction of nodes and all plausible visible connections.",
            "input_text_tokens": 4700,
            "images": diego_images,
            "output_low": 2400,
            "output_expected": 4600,
            "output_high": 7200,
            "reasoning_low": 3500,
            "reasoning_expected": 9000,
            "reasoning_high": 18000,
        },
        {
            "call_id": "subagent-02",
            "round": "02",
            "agent": "Jennifer",
            "purpose": "Precision review of Diego Round 1 with detail crops.",
            "input_text_tokens": 7200,
            "images": jennifer_images,
            "output_low": 1200,
            "output_expected": 2600,
            "output_high": 4800,
            "reasoning_low": 3500,
            "reasoning_expected": 9000,
            "reasoning_high": 18000,
        },
        {
            "call_id": "subagent-03",
            "round": "03",
            "agent": "Diego",
            "purpose": "Saturation check after Jennifer correction.",
            "input_text_tokens": 900,
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
            "input_text_tokens": 3400,
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
    missing = sorted({n for edge in DIEGO_EDGES + FINAL_EDGES for n in edge if n not in node_set})
    if missing:
        raise SystemExit(f"Unknown edge node(s): {missing}")
    if len(COMPONENT_NODES) != 103:
        raise SystemExit(f"Expected 103 component labels, got {len(COMPONENT_NODES)}")
    if len(LOGICAL_NODES) != 9:
        raise SystemExit(f"Expected 9 logical nodes, got {len(LOGICAL_NODES)}")
    if len(NODES) != 112:
        raise SystemExit(f"Expected 112 total nodes, got {len(NODES)}")
    if len(DIEGO_SOLID) != 105:
        raise SystemExit(f"Expected Diego solid edge count 105, got {len(DIEGO_SOLID)}")
    if len(FINAL_SOLID) != 106:
        raise SystemExit(f"Expected final solid edge count 106, got {len(FINAL_SOLID)}")
    if len(DASHED_CONTROL_DIEGO) != 20:
        raise SystemExit(f"Expected Diego dashed edge count 20, got {len(DASHED_CONTROL_DIEGO)}")
    if len(FINAL_DASHED_CONTROL) != 19:
        raise SystemExit(f"Expected final dashed edge count 19, got {len(FINAL_DASHED_CONTROL)}")
    if len(DASH_DOT_SENSING) != 6:
        raise SystemExit(f"Expected dash-dot edge count 6, got {len(DASH_DOT_SENSING)}")
    if len(DOTTED_GROUND) != 9:
        raise SystemExit(f"Expected dotted ground edge count 9, got {len(DOTTED_GROUND)}")
    if len(DIEGO_EDGES) != 140:
        raise SystemExit(f"Expected Diego total edge count 140, got {len(DIEGO_EDGES)}")
    if len(FINAL_EDGES) != 140:
        raise SystemExit(f"Expected final total edge count 140, got {len(FINAL_EDGES)}")


def main():
    validate()

    logical = set(LOGICAL_NODES)
    node_rows = []
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
        write_edge_file(RESULTS / f"{definition['file_stem']}_edges.csv", definition["edges"], FINAL_EDGES)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_edge_file(RESULTS / "final_connectivity_edges.csv", FINAL_EDGES, FINAL_EDGES)

    diff_rows = [
        {"change": "add", "node_a": "XFER-ATS-A", "node_b": "RECT-48V-A", "edge_kind": "solid_vital_ac_dc_power", "reason": "Jennifer confirmed terminal-dotted ATS/vital AC feed to rectifier."},
        {"change": "add", "node_a": "XFER-ATS-B", "node_b": "RECT-48V-B", "edge_kind": "solid_vital_ac_dc_power", "reason": "Jennifer confirmed terminal-dotted ATS/vital AC feed to rectifier."},
        {"change": "remove", "node_a": "JB-RLY-A", "node_b": "JB-RLY-B", "edge_kind": "solid_power_feeder", "reason": "No terminal-to-terminal bridge between relay junction boxes."},
        {"change": "remove", "node_a": "CP-ESFAS-1", "node_b": "CP-ESFAS-2", "edge_kind": "control_trip_close_dashed", "reason": "Dense CP routing lacks direct terminal-dot support for a CP1/CP2 tie."},
    ]
    write_csv(RESULTS / "round_02_jennifer_changed_edge_diff.csv", ["change", "node_a", "node_b", "edge_kind", "reason"], diff_rows)

    status_rows = []
    for idx, (key, (kind, note)) in enumerate(SPECIAL_STATUS_NOTES.items(), start=1):
        a, b = key
        status_rows.append({"edge_id": f"S-{idx:03d}", "node_a": a, "node_b": b, "edge_kind": kind, "status_note": note, "included_in_final_matrix": "yes"})
    for edge in FINAL_DASHED_CONTROL:
        a, b = edge
        status_rows.append({"edge_id": f"S-{len(status_rows)+1:03d}", "node_a": a, "node_b": b, "edge_kind": "control_trip_close_dashed", "status_note": "Dashed control/trip/close connection.", "included_in_final_matrix": "yes"})
    for edge in DASH_DOT_SENSING:
        a, b = edge
        status_rows.append({"edge_id": f"S-{len(status_rows)+1:03d}", "node_a": a, "node_b": b, "edge_kind": "sensing_instrument_dash_dot", "status_note": "Dash-dot sensing/instrument connection.", "included_in_final_matrix": "yes"})
    for edge in DOTTED_GROUND:
        a, b = edge
        status_rows.append({"edge_id": f"S-{len(status_rows)+1:03d}", "node_a": a, "node_b": b, "edge_kind": "grounding_conductor_dotted", "status_note": "Dotted grounding-conductor connection.", "included_in_final_matrix": "yes"})
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

Final interpretation: all visible drawn connections from the raw schematic, using the raw title-block count of 112 components and 140 connections as a sanity check.

Artifacts:
- `final_connectivity_matrix.csv`: 112 x 112 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 140 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `round_02_jennifer_changed_edge_diff.csv`: the precision diff from Diego Round 1.
- `special_status_edges.csv`: N.O. ties and non-solid line-type/status edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.
- `local_artifact_token_counts.csv`: local file/image token estimate inputs.

Counts:
- Component-label nodes from CSV: {len(COMPONENT_NODES)}
- Explicit visible logical/reference nodes: {len(LOGICAL_NODES)}
- Total matrix nodes: {len(NODES)}
- Final solid edges: {len(FINAL_SOLID)}
- Final dashed control/trip/close edges: {len(FINAL_DASHED_CONTROL)}
- Dash-dot sensing/instrument edges: {len(DASH_DOT_SENSING)}
- Dotted grounding-conductor edges: {len(DOTTED_GROUND)}
- Final drawn connections: {len(FINAL_EDGES)}

Notes:
- Normally-open tie breakers are included as visible drawn connections and annotated in metadata.
- `JB-RLY-A--JB-RLY-B` and `CP-ESFAS-1--CP-ESFAS-2` are not in the final matrix.
- `XFER-ATS-A--RECT-48V-A` and `XFER-ATS-B--RECT-48V-B` are in the final matrix.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")

    print(
        f"nodes={len(NODES)} final_edges={len(FINAL_EDGES)} "
        f"solid={len(FINAL_SOLID)} dashed={len(FINAL_DASHED_CONTROL)} "
        f"dashdot={len(DASH_DOT_SENSING)} dotted={len(DOTTED_GROUND)}"
    )


if __name__ == "__main__":
    main()
