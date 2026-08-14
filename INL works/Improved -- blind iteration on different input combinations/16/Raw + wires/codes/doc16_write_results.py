import csv
import json
import math
from pathlib import Path

from PIL import Image


DOC = "16"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires")
CROPS = Path(r"C:\Asif_all_python_projects\INL\INL\doc16_work\crops")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc16_work\results")

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_revised(1).png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def add_unique(items, value):
    if value not in items:
        items.append(value)


def norm_edge(a, b):
    return tuple(sorted((a, b)))


def add_edge(edges, a, b, evidence):
    edges[norm_edge(a, b)] = evidence


def build_nodes():
    nodes = []

    for n in [
        "GRID-161KV",
        "TR-SST-1A",
        "CB-401A",
        "CB-401B",
        "BUS-4KV-A",
        "BUS-4KV-B",
        "CB-TIE-4AB",
        "GEN-EDG-A",
        "CB-EDG-A",
        "GEN-EDG-B",
        "CB-EDG-B",
        "TR-4KV-480A",
        "TR-4KV-480B",
        "CB-480A-IN",
        "CB-480B-IN",
        "BUS-480-A",
        "BUS-480-B",
        "CB-TIE-480AB",
    ]:
        add_unique(nodes, n)

    for n in [
        "CB-11A-FDR",
        "CB-12A-FDR",
        "CB-21A-FDR",
        "CB-31A-FDR30-B",
        "CB-11B-FDR",
        "CB-12B-FDR",
        "CB-21B-FDR",
        "CB-31B-FDR",
        "MCC-11A",
        "MCC-12A",
        "MCC-21A",
        "MCC-31A",
        "MCC-11B",
        "MCC-12B",
        "MCC-21B",
        "MCC-31B",
    ]:
        add_unique(nodes, n)

    for train in ("A", "B"):
        for _, code, relay, load, endpoint, _kind in branch_defs(train):
            for n in [code, relay, load, endpoint]:
                add_unique(nodes, n)

    for n in [
        "TR-RPS-A",
        "MG-RPS-A",
        "BUS-120-RPS-A",
        "BUS-125DC-A",
        "BATT-125A",
        "CHGR-125A",
        "INV-120A",
        "TR-RPS-B",
        "MG-RPS-B",
        "BUS-120-RPS-B",
        "BUS-125DC-B",
        "BATT-125B",
        "CHGR-125B",
        "INV-120B",
        "CP-RPS-A",
        "JB-RPS-A3-1A",
        "PROT-UV-A",
        "RELAY-27A",
        "CP-ESF-A",
        "TB-2A",
        "PROT-GF-A",
        "RELAY-86A",
        "CP-DCS-01",
        "TB-3A",
        "CP-RPS-B",
        "JB-RPS-B3-1B",
        "PROT-UV-B",
        "RELAY-27B",
        "CP-ESF-B",
        "TB-2B",
        "PROT-GF-B",
        "RELAY-86B",
        "CP-ANN-01",
        "TB-3B",
        "TB-ESF-1",
        "PT-RCS101",
        "LT-RWST101",
        "FT-AFW101",
        "REC-SOE-1",
        "ANN-501",
        "METER-VM-1",
        "TB-ESF-2",
        "RTD-RCS101",
        "LS-SUMP101",
        "XS-DOOR101",
        "JB-CONTAIN",
        "UCB-01",
        "GND-NO",
    ]:
        add_unique(nodes, n)

    return nodes


def branch_defs(train):
    return [
        (f"MCC-11{train}", f"CB-P201{train}", f"RELAY-KP201{train}", f"PUMP-RHR201{train}", f"GND-P201{train}", "ground"),
        (f"MCC-11{train}", f"CB-P211{train}", f"RELAY-KP211{train}", f"PUMP-CS211{train}", f"GND-P211{train}", "ground"),
        (f"MCC-11{train}", f"CB-P221{train}", f"RELAY-KP221{train}", f"PUMP-SI221{train}", f"GND-P221{train}", "ground"),
        (f"MCC-12{train}", f"CB-P101{train}", f"RELAY-KP101{train}", f"PUMP-AFW101{train}", f"GND-P101{train}", "ground"),
        (f"MCC-12{train}", f"CB-HV101{train}", f"RELAY-KHV101{train}", f"MOV-HV101{train}", f"TB-HV101{train}", "terminal"),
        (f"MCC-12{train}", f"CB-FN1{train}", f"RELAY-KFN1{train}", f"FAN-HV1{train}", f"GND-FN1{train}", "ground"),
        (f"MCC-21{train}", f"CB-P301{train}", f"RELAY-KP301{train}", f"PUMP-CCM301{train}", f"GND-P301{train}", "ground"),
        (f"MCC-21{train}", f"CB-P401{train}", f"RELAY-KP401{train}", f"PUMP-SM401{train}", f"GND-P401{train}", "ground"),
        (f"MCC-21{train}", f"CB-HT1{train}", f"RELAY-KHT1{train}", f"HTR-PZR1{train}", f"TB-HT1{train}", "terminal"),
        (f"MCC-31{train}", f"CB-RM1{train}", f"RELAY-KRM1{train}", f"MON-RAD1{train}", f"TB-RM1{train}", "signal_terminal"),
        (f"MCC-31{train}", f"CB-P501{train}", f"RELAY-KP501{train}", f"PUMP-CHM501{train}", f"GND-P501{train}", "ground"),
        (f"MCC-31{train}", f"CB-CV121{train}", f"RELAY-KCV121{train}", f"MOV-CV121{train}", f"TB-CV121{train}", "terminal"),
    ]


def backbone_edges():
    edges = {}
    ev = "solid source/bus/feed path visible in raw and overlay"
    for a, b in [
        ("GRID-161KV", "TR-SST-1A"),
        ("TR-SST-1A", "CB-401A"),
        ("CB-401A", "BUS-4KV-A"),
        ("TR-SST-1A", "CB-401B"),
        ("CB-401B", "BUS-4KV-B"),
        ("BUS-4KV-A", "CB-TIE-4AB"),
        ("CB-TIE-4AB", "BUS-4KV-B"),
        ("GEN-EDG-A", "CB-EDG-A"),
        ("CB-EDG-A", "BUS-4KV-A"),
        ("GEN-EDG-B", "CB-EDG-B"),
        ("CB-EDG-B", "BUS-4KV-B"),
        ("BUS-4KV-A", "TR-4KV-480A"),
        ("TR-4KV-480A", "CB-480A-IN"),
        ("CB-480A-IN", "BUS-480-A"),
        ("BUS-4KV-B", "TR-4KV-480B"),
        ("TR-4KV-480B", "CB-480B-IN"),
        ("CB-480B-IN", "BUS-480-B"),
        ("BUS-480-A", "CB-TIE-480AB"),
        ("CB-TIE-480AB", "BUS-480-B"),
    ]:
        add_edge(edges, a, b, ev)
    return edges


def feeder_edges():
    edges = {}
    for bus, cb, mcc in [
        ("BUS-480-A", "CB-11A-FDR", "MCC-11A"),
        ("BUS-480-A", "CB-12A-FDR", "MCC-12A"),
        ("BUS-480-A", "CB-21A-FDR", "MCC-21A"),
        ("BUS-480-B", "CB-31A-FDR30-B", "MCC-31A"),
        ("BUS-480-B", "CB-11B-FDR", "MCC-11B"),
        ("BUS-480-B", "CB-12B-FDR", "MCC-12B"),
        ("BUS-480-B", "CB-21B-FDR", "MCC-21B"),
        ("BUS-480-B", "CB-31B-FDR", "MCC-31B"),
    ]:
        add_edge(edges, bus, cb, "480 V rail drop to feeder breaker with filled junction")
        add_edge(edges, cb, mcc, "feeder breaker vertical conductor into MCC")
    return edges


def load_edges(policy):
    edges = {}
    for train in ("A", "B"):
        for mcc, cb, relay, load, endpoint, kind in branch_defs(train):
            add_edge(edges, mcc, cb, "MCC internal bus branch to load breaker")
            add_edge(edges, cb, relay, "vertical branch from breaker to relay/contact device")
            include_load = True
            include_tail = True
            if policy == "jennifer_r1":
                if kind == "signal_terminal":
                    include_load = False
                    include_tail = False
                elif kind == "terminal":
                    include_tail = False
            if include_load:
                add_edge(edges, relay, load, "direct relay/contact to load symbol")
            if include_tail:
                add_edge(edges, load, endpoint, "direct one-hop load tail to ground or terminal block")
    return edges


def vital_power_edges():
    edges = {}
    for train in ("A", "B"):
        add_edge(edges, f"TR-RPS-{train}", f"MG-RPS-{train}", "RPS transformer output to motor-generator set")
        add_edge(edges, f"MG-RPS-{train}", f"BUS-120-RPS-{train}", "motor-generator output to 120 VAC RPS bus")
        add_edge(edges, f"BATT-125{train}", f"CHGR-125{train}", "125 V battery/charger DC link")
        add_edge(edges, f"CHGR-125{train}", f"BUS-125DC-{train}", "charger output to 125 VDC bus")
        add_edge(edges, f"BUS-125DC-{train}", f"INV-120{train}", "125 VDC bus feeds inverter")
        add_edge(edges, f"INV-120{train}", f"BUS-120-RPS-{train}", "inverter output to 120 VAC RPS bus")
    return edges


def local_control_edges(include_panel_chains=True, include_clean_stubs=True, include_jb_contain=False, include_ucb_ground=False):
    edges = {}
    if include_panel_chains:
        for a, b in [
            ("CP-RPS-A", "JB-RPS-A3-1A"),
            ("JB-RPS-A3-1A", "PROT-UV-A"),
            ("PROT-UV-A", "RELAY-27A"),
            ("CP-ESF-A", "TB-2A"),
            ("TB-2A", "PROT-GF-A"),
            ("PROT-GF-A", "RELAY-86A"),
            ("CP-DCS-01", "TB-3A"),
            ("TB-3A", "RELAY-86A"),
            ("CP-RPS-B", "JB-RPS-B3-1B"),
            ("JB-RPS-B3-1B", "PROT-UV-B"),
            ("PROT-UV-B", "RELAY-27B"),
            ("CP-ESF-B", "TB-2B"),
            ("TB-2B", "PROT-GF-B"),
            ("PROT-GF-B", "RELAY-86B"),
            ("CP-ANN-01", "TB-3B"),
            ("TB-3B", "RELAY-86B"),
        ]:
            add_edge(edges, a, b, "local dashed control/protection chain with visible endpoint dots")

    if include_clean_stubs:
        for a, b in [
            ("TB-ESF-1", "PT-RCS101"),
            ("PT-RCS101", "REC-SOE-1"),
            ("TB-ESF-1", "LT-RWST101"),
            ("LT-RWST101", "ANN-501"),
            ("TB-ESF-1", "FT-AFW101"),
            ("FT-AFW101", "METER-VM-1"),
            ("TB-ESF-2", "LS-SUMP101"),
            ("TB-ESF-2", "XS-DOOR101"),
        ]:
            add_edge(edges, a, b, "local one-hop signal/ground stub with visible endpoint")
        if include_ucb_ground:
            add_edge(edges, "UCB-01", "GND-NO", "local one-hop ground/common stub")
        if include_jb_contain:
            add_edge(edges, "JB-CONTAIN", "XS-DOOR101", "visually plausible containment junction signal stub")
    return edges


def build_edges(policy):
    edges = {}
    for group in [
        backbone_edges(),
        feeder_edges(),
        load_edges("jennifer_r1" if policy == "jennifer_r1" else "full"),
        vital_power_edges(),
    ]:
        edges.update(group)

    if policy == "diego_r1":
        edges.update(local_control_edges(include_panel_chains=False, include_clean_stubs=False))
    elif policy == "jennifer_r1":
        edges.update(local_control_edges(include_panel_chains=False, include_clean_stubs=False))
    elif policy == "diego_r2":
        edges.update(local_control_edges(include_panel_chains=False, include_clean_stubs=True, include_jb_contain=False, include_ucb_ground=False))
    elif policy == "final":
        edges.update(local_control_edges(include_panel_chains=False, include_clean_stubs=True, include_jb_contain=False, include_ucb_ground=False))
    else:
        raise ValueError(policy)
    return edges


def uncertain_edges(policy):
    rows = []
    def u(a, b, reason):
        rows.append((a, b, reason))

    # Edges that are plausible but route-shared or label-inferred.
    for a, b, reason in [
        ("BUS-480-A", "TR-RPS-A", "upstream RPS transformer feeder source is not cleanly terminated at the A rail"),
        ("BUS-480-B", "TR-RPS-B", "upstream RPS transformer feeder source is not cleanly terminated at the B rail"),
        ("BUS-120-RPS-A", "UCB-01", "lower shared dashed/common route is not a clean one-hop endpoint"),
        ("BUS-120-RPS-B", "UCB-01", "lower shared dashed/common route is not a clean one-hop endpoint"),
        ("UCB-01", "GND-NO", "UCB/common ground routing is shared and not accepted as a hard endpoint chain"),
        ("JB-CONTAIN", "XS-DOOR101", "containment junction to door switch is visually plausible but routed through shared signal trunk"),
        ("RTD-RCS101", "MG-RPS-B", "RTD side connection lands near a shared vertical route; exact endpoint ambiguous"),
        ("CP-DCS-01", "TB-ESF-1", "dotted/signal route is shared with multiple endpoints"),
        ("CP-ANN-01", "TB-ESF-2", "dotted/signal route is shared with multiple endpoints"),
        ("CB-401A", "CB-401B", "dashed breaker trip/interlock routing is visually plausible but not a hard terminal-to-terminal edge"),
    ]:
        u(a, b, reason)

    if policy in ("diego_r1", "diego_r2"):
        for a, b, reason in [
            ("CP-RPS-A", "JB-RPS-A3-1A", "control chain initially treated as uncertain"),
            ("CP-ESF-A", "TB-2A", "control chain initially treated as uncertain"),
            ("CP-DCS-01", "TB-3A", "control chain initially treated as uncertain"),
            ("CP-RPS-B", "JB-RPS-B3-1B", "control chain initially treated as uncertain"),
            ("CP-ESF-B", "TB-2B", "control chain initially treated as uncertain"),
            ("CP-ANN-01", "TB-3B", "control chain initially treated as uncertain"),
        ]:
            u(a, b, reason)

    if policy == "jennifer_r1":
        for train in ("A", "B"):
            for a, b in [
                (f"MOV-HV101{train}", f"TB-HV101{train}"),
                (f"HTR-PZR1{train}", f"TB-HT1{train}"),
                (f"RELAY-KRM1{train}", f"MON-RAD1{train}"),
                (f"MON-RAD1{train}", f"TB-RM1{train}"),
                (f"MOV-CV121{train}", f"TB-CV121{train}"),
            ]:
                u(a, b, "demoted by Jennifer R1 because the tail is dashed/dotted")
        for a, b in [
            ("PT-RCS101", "REC-SOE-1"),
            ("LT-RWST101", "ANN-501"),
            ("FT-AFW101", "METER-VM-1"),
            ("TB-ESF-2", "LS-SUMP101"),
            ("TB-ESF-2", "XS-DOOR101"),
        ]:
            u(a, b, "local signal stub demoted pending saturation")

    if policy == "final":
        # Final keeps only the weak/shared cases uncertain; local one-hop stubs are hard.
        pass

    return rows


ROUNDS = [
    ("round_01_diego_high_recall", "diego_r1", "Diego R1: high recall; full selected-load chains hard, lower route-shared controls uncertain."),
    ("round_01_jennifer_precision", "jennifer_r1", "Jennifer R1: strict power/backbone hard; dashed/dotted terminal and signal tails demoted."),
    ("round_02_diego_saturation", "diego_r2", "Diego R2: accepts backbone correction; promotes clean one-hop terminal/instrument stubs."),
    ("round_02_jennifer_final", "final", "Jennifer final saturation: hard includes clean one-hop terminal/instrument stubs; shared CP/RPS/ESF/DCS/ANN, JB-CONTAIN/XS, and UCB/common routes remain uncertain."),
]


def matrix_for(nodes, edges):
    idx = {n: i for i, n in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    missing = []
    for a, b in edges:
        if a not in idx or b not in idx:
            missing.append((a, b))
            continue
        i = idx[a]
        j = idx[b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    return matrix, missing


def write_matrix(path, nodes, matrix):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for n, row in zip(nodes, matrix):
            writer.writerow([n] + row)


def write_sparse(path, nodes, matrix):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "connected"])
        for i, a in enumerate(nodes):
            for j, b in enumerate(nodes):
                writer.writerow([a, b, matrix[i][j]])


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for (a, b), ev in sorted(edges.items()):
            writer.writerow([a, b, ev])


def write_nodes(path, nodes):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"])
        for n in nodes:
            writer.writerow([n])


def write_uncertain(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "reason"])
        for row in rows:
            writer.writerow(row)


def qa(nodes, edges, matrix, missing):
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    degree = {n: 0 for n in nodes}
    for a, b in edges:
        if a in degree:
            degree[a] += 1
        if b in degree:
            degree[b] += 1
    return {
        "node_count": len(nodes),
        "hard_edge_count": len(edges),
        "missing_edge_endpoints": missing,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "isolated_hard_only_nodes": [n for n, d in degree.items() if d == 0],
    }


def image_tokens(path):
    with Image.open(path) as im:
        w, h = im.size
    return math.ceil(w / 32) * math.ceil(h / 32)


def token_estimates():
    image_sets = {
        "main_01_visual_orchestration_and_artifacts": [
            CROPS / "raw_full_preview.png",
            CROPS / "overlay_full_preview.png",
            CROPS / "raw_top_band.png",
            CROPS / "overlay_top_band.png",
            CROPS / "raw_upper_middle_band.png",
            CROPS / "raw_middle_band.png",
            CROPS / "overlay_middle_band.png",
            CROPS / "raw_bottom_band.png",
            CROPS / "overlay_bottom_band.png",
            CROPS / "close_480_tie_cb31a.png",
            CROPS / "close_vital_a.png",
            CROPS / "close_vital_b.png",
            CROPS / "close_rps_control_a.png",
            CROPS / "close_b_instr.png",
        ],
        "diego_01_high_recall": [
            CROPS / "raw_full_preview.png",
            CROPS / "overlay_full_preview.png",
            CROPS / "raw_top_band.png",
            CROPS / "raw_middle_band.png",
            CROPS / "raw_bottom_band.png",
        ],
        "jennifer_01_precision": [
            CROPS / "raw_full_preview.png",
            CROPS / "overlay_full_preview.png",
            CROPS / "raw_top_band.png",
            CROPS / "raw_upper_middle_band.png",
            CROPS / "raw_middle_band.png",
            CROPS / "raw_bottom_band.png",
        ],
        "diego_02_saturation": [],
        "jennifer_02_final": [],
    }
    rows = []
    specs = [
        ("main_01_visual_orchestration_and_artifacts", "main", "orchestration", "gpt-5", 1200, 4200, (2500, 5200, 9000), 0, "local visual inspection, scripts, artifact writing"),
        ("diego_01_high_recall", "Diego", "round_01", "gpt-5.5 xhigh", 2600, 2800, (4500, 9000, 16200), 0, "subagent usage object unavailable; visual draft observed"),
        ("jennifer_01_precision", "Jennifer", "round_01", "gpt-5.5 xhigh", 3300, 2300, (4000, 8000, 14400), 0, "subagent usage object unavailable; visual review observed"),
        ("diego_02_saturation", "Diego", "round_02", "gpt-5.5 xhigh", 2300, 520, (1200, 2400, 4500), 0, "follow-up in same Diego context; prior image packet estimated cached"),
        ("jennifer_02_final", "Jennifer", "round_02", "gpt-5.5 xhigh", 1800, 420, (900, 1800, 3400), 0, "follow-up in same Jennifer context; prior image packet estimated cached"),
    ]
    cached = {
        "diego_02_saturation": sum(image_tokens(p) for p in image_sets["diego_01_high_recall"] if p.exists()),
        "jennifer_02_final": sum(image_tokens(p) for p in image_sets["jennifer_01_precision"] if p.exists()),
    }
    for call_id, actor, round_name, model, text_in, out_tokens, reason, cache_text, note in specs:
        image_in = sum(image_tokens(p) for p in image_sets[call_id] if p.exists())
        cached_in = cached.get(call_id, cache_text)
        low = text_in + image_in + out_tokens + reason[0]
        expected = text_in + image_in + out_tokens + reason[1]
        high = text_in + image_in + out_tokens + reason[2]
        rows.append({
            "document": DOC,
            "iteration": ITERATION,
            "call_id": call_id,
            "actor": actor,
            "round": round_name,
            "model": model,
            "input_tokens_est": text_in,
            "cached_input_tokens_est": cached_in,
            "output_tokens_est": out_tokens,
            "reasoning_tokens_available": "no",
            "reasoning_tokens_low_est": reason[0],
            "reasoning_tokens_expected_est": reason[1],
            "reasoning_tokens_high_est": reason[2],
            "image_file_input_tokens_est": image_in,
            "total_tokens_low_est": low,
            "total_tokens_expected_est": expected,
            "total_tokens_high_est": high,
            "usage_object_available": "no",
            "notes": note,
        })
    return rows


def write_token_usage(rows):
    fields = [
        "document",
        "iteration",
        "call_id",
        "actor",
        "round",
        "model",
        "input_tokens_est",
        "cached_input_tokens_est",
        "output_tokens_est",
        "reasoning_tokens_available",
        "reasoning_tokens_low_est",
        "reasoning_tokens_expected_est",
        "reasoning_tokens_high_est",
        "image_file_input_tokens_est",
        "total_tokens_low_est",
        "total_tokens_expected_est",
        "total_tokens_high_est",
        "usage_object_available",
        "notes",
    ]
    with (OUT / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(r["total_tokens_low_est"] for r in rows)
    total_expected = sum(r["total_tokens_expected_est"] for r in rows)
    total_high = sum(r["total_tokens_high_est"] for r in rows)
    total_image = sum(r["image_file_input_tokens_est"] for r in rows)
    total_cached = sum(r["cached_input_tokens_est"] for r in rows)
    with (OUT / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write(f"# Token Usage Estimate - Document {DOC}, Iteration {ITERATION}\n\n")
        f.write("OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.\n\n")
        f.write("Local estimate method:\n")
        f.write("- Text tokens: coarse manual estimate based on prompt/response size.\n")
        f.write("- Image/file tokens: ceil(width / 32) * ceil(height / 32) for each included local image.\n")
        f.write("- Reasoning tokens: unavailable, so low/expected/high ranges are estimated.\n")
        f.write("- Cached input tokens: estimated prior subagent visual packet for round-2 follow-ups.\n\n")
        f.write("| document | iteration | low | expected | high | image/file input | cached input |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        f.write(f"| {DOC} | {ITERATION} | {total_low} | {total_expected} | {total_high} | {total_image} | {total_cached} |\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = build_nodes()
    final_summary = {}
    qas = {}

    for round_name, policy, note in ROUNDS:
        edges = build_edges(policy)
        matrix, missing = matrix_for(nodes, edges)
        write_matrix(OUT / f"connectivity_matrix_{round_name}.csv", nodes, matrix)
        write_sparse(OUT / f"connectivity_sparse_{round_name}.csv", nodes, matrix)
        write_edges(OUT / f"edges_{round_name}.csv", edges)
        write_nodes(OUT / f"nodes_{round_name}.csv", nodes)
        write_uncertain(OUT / f"uncertain_edges_{round_name}.csv", uncertain_edges(policy))
        qas[round_name] = qa(nodes, edges, matrix, missing)
        qas[round_name]["uncertain_edge_count"] = len(uncertain_edges(policy))
        qas[round_name]["note"] = note

        if policy == "final":
            write_matrix(OUT / "connectivity_matrix_final.csv", nodes, matrix)
            write_sparse(OUT / "connectivity_sparse_final.csv", nodes, matrix)
            write_edges(OUT / "edges_final.csv", edges)
            write_nodes(OUT / "nodes_final.csv", nodes)
            write_uncertain(OUT / "uncertain_edges_final.csv", uncertain_edges(policy))
            final_summary = {
                "node_count": len(nodes),
                "hard_edge_count": len(edges),
                "uncertain_edge_count": len(uncertain_edges(policy)),
            }

    final_edges = build_edges("final")
    final_matrix, final_missing = matrix_for(nodes, final_edges)
    qa_final = qa(nodes, final_edges, final_matrix, final_missing)
    qa_final["uncertain_edge_count"] = len(uncertain_edges("final"))
    qa_final["rounds"] = qas
    qa_final["raw_resource"] = str(RAW)
    qa_final["overlay_resource"] = str(OVERLAY)
    qa_final["mask_resource"] = str(MASK)
    qa_final["notes"] = [
        "Final matrix includes hard visual connections only.",
        "Direct one-hop terminal and instrument stubs are hard when both endpoint dots/contacts are visually clean.",
        "Long route-shared dashed/dotted control and signal trunks remain in uncertain_edges_final.csv instead of being overconnected.",
        "Jennifer final kept JB-CONTAIN--XS-DOOR101 and UCB-01/GND-NO common routing uncertain.",
        "BUS-480-B is an inferred lower 480 V bus label based on the redundant A/B train geometry; the sheet does not print it beside the lower rail.",
    ]
    (OUT / "qa_final.json").write_text(json.dumps(qa_final, indent=2), encoding="utf-8")

    with (OUT / "round_notes.md").open("w", encoding="utf-8") as f:
        f.write(f"# Document {DOC} Round Notes\n\n")
        for round_name, _policy, note in ROUNDS:
            f.write(f"## {round_name}\n\n{note}\n\n")
        f.write("## Saturation Decision\n\n")
        f.write("Final hard set follows Jennifer's corrected backbone and Diego's R2 promotion of clean one-hop terminal/instrument stubs. ")
        f.write("Shared CP/RPS/ESF/DCS/ANN trunks, JB-CONTAIN/XS routing, and UCB/common routing remain uncertain.\n")

    token_rows = token_estimates()
    write_token_usage(token_rows)

    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "final_node_count": final_summary["node_count"],
        "final_hard_edge_count": final_summary["hard_edge_count"],
        "final_uncertain_edge_count": final_summary["uncertain_edge_count"],
        "round_hard_edge_counts": {r: q["hard_edge_count"] for r, q in qas.items()},
        "round_uncertain_edge_counts": {r: q["uncertain_edge_count"] for r, q in qas.items()},
        "files_written": sorted(p.name for p in OUT.iterdir() if p.is_file()),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
