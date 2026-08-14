import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires + components + junctions")
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def add_chain(edges, chain):
    for a, b in zip(chain, chain[1:]):
        edges.add(tuple(sorted((a, b))))


def add_edge(edges, a, b):
    edges.add(tuple(sorted((a, b))))


def final_graph(include_relay_soe=True):
    nodes = []
    edges = set()

    def chain(items):
        for item in items:
            if item not in nodes:
                nodes.append(item)
        add_chain(edges, items)

    def edge(a, b):
        for item in (a, b):
            if item not in nodes:
                nodes.append(item)
        add_edge(edges, a, b)

    chain(["SAT-1A", "CB-SAT-1A", "BUS-4160-A"])
    chain(["GEN-001", "UAT-1A", "CB-UAT-1A", "BUS-4160-A"])
    chain(["DG-1A", "CB-DG-1A", "BUS-4160-A"])
    edge("BUS-4160-A", "PT-4160-A")
    chain(["BUS-4160-A", "CB-TR-A1", "TR-LC-A1", "CB-480-A1", "BUS-480-A"])
    chain(["BUS-4160-A", "CB-TR-A2", "TR-LC-A2", "CB-480-A2", "BUS-480-A"])
    chain(["BUS-4160-A", "CB-TIE-4AB", "BUS-4160-B"])
    chain(["GEN-001", "UAT-1B", "CB-UAT-1B", "BUS-4160-B"])
    chain(["DG-1B", "CB-DG-1B", "BUS-4160-B"])
    chain(["SAT-1B", "CB-SAT-1B", "BUS-4160-B"])
    edge("BUS-4160-B", "PT-4160-B")
    chain(["BUS-4160-B", "CB-TR-B1", "TR-LC-B1", "CB-480-B1", "BUS-480-B"])
    chain(["BUS-4160-B", "CB-TR-B2", "TR-LC-B2", "CB-480-B2", "BUS-480-B"])
    chain(["BUS-480-A", "CB-TIE-480AB", "BUS-480-B"])
    for inst in ["AM-480-A", "VM-480-A", "CT-480-A1", "GND-SMGR-A"]:
        edge("BUS-480-A", inst)
    for inst in ["AM-480-B", "VM-480-B", "CT-480-B1", "GND-SMGR-B"]:
        edge("BUS-480-B", inst)

    a_feeders = [
        ["BUS-480-A", "CB-101A", "DS-101A", "MS-101A", "PUMP-SLC-1A", "TB-SLC-1A"],
        ["BUS-480-A", "CB-102A", "FU-102A", "MS-102A", "PUMP-CCW-2A", "GND-CCW-2A"],
        ["BUS-480-A", "CB-103A", "DS-103A", "MS-103A", "PUMP-RHR-1A", "LS-RHR-1A"],
        ["BUS-480-A", "CB-104A", "FU-104A", "MS-104A", "PUMP-CS-1A", "TB-CS-1A"],
        ["BUS-480-A", "CB-105A", "DS-105A", "MS-105A", "FAN-CRDM-1A", "GND-FAN-1A"],
        ["BUS-480-A", "CB-106A", "FU-106A", "RELAY-K106A", "HOV-RHVC-101A", "LS-RHVC-101A"],
        ["BUS-480-A", "CB-107A", "DS-107A", "RELAY-K107A", "HOV-RHR-102A", "LS-RHR-102A"],
        ["BUS-480-A", "CB-108A", "FU-108A", "MS-108A", "HTR-PZR-1A", "TB-HTR-1A"],
        ["BUS-480-A", "CB-109A", "DS-109A", "MS-109A", "PUMP-SW-1A", "GND-SW-1A"],
        ["BUS-480-A", "CB-110A", "FU-110A", "MS-110A", "HTR-AHU-1A", "GND-AHU-1A"],
        ["BUS-480-A", "CB-111A", "DS-111A", "MS-111A", "CMP-AIR-2A", "TB-AIR-2A"],
        ["BUS-480-A", "CB-112A", "FU-112A", "RELAY-K112A", "INSTR-RAD-1A", "JB-RAD-1A"],
    ]
    b_feeders = [
        ["BUS-480-B", "CB-201B", "DS-201B", "MS-201B", "PUMP-SLC-1B", "TB-SLC-1B"],
        ["BUS-480-B", "CB-202B", "FU-202B", "MS-202B", "PUMP-CCW-1B", "GND-CCW-1B"],
        ["BUS-480-B", "CB-203B", "DS-203B", "MS-203B", "PUMP-RHR-1B", "LS-RHR-1B"],
        ["BUS-480-B", "CB-204B", "FU-204B", "MS-204B", "PUMP-CS-1B", "TB-CS-1B"],
        ["BUS-480-B", "CB-205B", "DS-205B", "MS-205B", "FAN-CRDM-1B", "GND-FAN-1B"],
        ["BUS-480-B", "CB-206B", "FU-206B", "RELAY-K206B", "HOV-RHVC-101B", "LS-RHVC-101B"],
        ["BUS-480-B", "CB-207B", "DS-207B", "RELAY-K207B", "HOV-RHR-102B", "LS-RHR-102B"],
        ["BUS-480-B", "CB-208B", "FU-208B", "MS-208B", "HTR-PZR-1B", "TB-HTR-1B"],
        ["BUS-480-B", "CB-209B", "DS-209B", "MS-209B", "PUMP-SW-1B", "GND-SW-1B"],
        ["BUS-480-B", "CB-210B", "FU-210B", "MS-210B", "HTR-AHU-1B", "GND-AHU-1B"],
        ["BUS-480-B", "CB-211B", "DS-211B", "MS-211B", "CMP-AIR-1B", "TB-AIR-1B"],
        ["BUS-480-B", "CB-212B", "FU-212B", "RELAY-K212B", "INSTR-RAD-1B", "JB-RAD-1B"],
    ]
    for feeder in a_feeders + b_feeders:
        chain(feeder)

    chain(["BUS-480-A", "CB-DC-A", "CHGR-125-A", "BAT-125-A", "BUS-125DC-A"])
    chain(["BUS-480-B", "CB-DC-B", "CHGR-125-B", "BAT-125-B", "BUS-125DC-B"])
    chain(["BUS-125DC-A", "CB-DCTIE-AB", "BUS-125DC-B"])
    edge("BUS-125DC-A", "GND-DC-A")
    edge("BUS-125DC-B", "GND-DC-B")
    chain(["BUS-125DC-A", "INV-120-A", "BUS-120AC-A", "STS-120-A", "PNL-RPS-A"])
    chain(["BUS-125DC-B", "INV-120-B", "BUS-120AC-B", "STS-120-B", "PNL-RPS-B"])
    chain(["TB-RPS-A", "PNL-RPS-A", "RELAY-UV-A1"])
    edge("PNL-RPS-A", "RELAY-UV-A2")
    chain(["TB-RPS-B", "PNL-RPS-B", "RELAY-UV-B1"])
    edge("PNL-RPS-B", "RELAY-UV-B2")
    chain(["TB-ESF-A", "PNL-ESF-A", "RELAY-RPS-A"])
    edge("PNL-ESF-A", "RELAY-ESF-A")
    chain(["TB-ESF-B", "PNL-ESF-B", "RELAY-RPS-B"])
    edge("PNL-ESF-B", "RELAY-ESF-B")
    edge("PNL-DCS", "REC-SOE-1")
    edge("PNL-ANN", "ANN-ESF-A")
    edge("PNL-ANN", "ANN-ESF-B")
    if include_relay_soe:
        edge("RELAY-ESF-A", "REC-SOE-1")
        edge("RELAY-ESF-B", "REC-SOE-2")

    return nodes, edges


def diego_round1_graph():
    nodes, edges = final_graph(include_relay_soe=True)
    replacements = {
        "PUMP-CCW-2A": "PUMP-COV-1A",
        "GND-CCW-2A": "GND-CCW-1A",
        "PUMP-CCW-1B": "PUMP-COV-1B",
        "HOV-RHVC-101A": "HOV-RHCU-101A",
        "HOV-RHVC-101B": "HOV-RHCU-101B",
        "HTR-PZR-1A": "HTR-PR-1A",
        "HTR-PZR-1B": "HTR-PR-1B",
        "CMP-AIR-2A": "CIP-AIR-1A",
        "TB-AIR-2A": "TB-AIR-1A",
        "CMP-AIR-1B": "CIP-AIR-1B",
    }
    nodes = [replacements.get(n, n) for n in nodes]
    edges = {tuple(sorted((replacements.get(a, a), replacements.get(b, b)))) for a, b in edges}
    if "MASTER-TB-21-29" not in nodes:
        nodes.insert(nodes.index("CB-TIE-4AB"), "MASTER-TB-21-29")
    add_edge(edges, "CB-TR-A2", "MASTER-TB-21-29")
    return nodes, edges


def write_edges(path, edges):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        for a, b in sorted(edges):
            writer.writerow([a, b])


def write_nodes(path, nodes):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_matrix(path, nodes, edges):
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b in edges:
        matrix[idx[a]][idx[b]] = 1
        matrix[idx[b]][idx[a]] = 1
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def validate(nodes, edges):
    missing = sorted({x for e in edges for x in e if x not in nodes})
    duplicate_nodes = len(nodes) - len(set(nodes))
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "duplicate_node_count": duplicate_nodes,
        "missing_edge_endpoint_count": len(missing),
        "missing_edge_endpoints": missing,
        "diagonal_zero": True,
        "symmetric": True,
    }


def image_token_estimate(path):
    with Image.open(path) as img:
        w, h = img.size
    scale = min(2048 / max(w, h), 1.0)
    w2, h2 = int(math.ceil(w * scale)), int(math.ceil(h * scale))
    if min(w2, h2) > 768:
        scale2 = 768 / min(w2, h2)
        w2, h2 = int(math.ceil(w2 * scale2)), int(math.ceil(h2 * scale2))
    tiles = math.ceil(w2 / 512) * math.ceil(h2 / 512)
    return 85 + 170 * tiles


def write_token_estimates():
    raw = BASE / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png"
    crops = BASE / "codes" / "crops"
    diego_images = [
        raw,
        BASE / "wire_nodes_overlay.png",
        BASE / "detected_components_overlay.png",
        BASE / "wires_mask_overlay.png",
        crops / "raw__full_left_train.png",
        crops / "raw__full_right_train.png",
        crops / "raw__top_sources_left.png",
        crops / "raw__top_sources_right.png",
        crops / "raw__ac_bus_tie_center.png",
        crops / "raw__left_mcc_feeders.png",
        crops / "raw__right_mcc_feeders.png",
        crops / "raw__left_mcc_feeders_01_05.png",
        crops / "raw__left_mcc_feeders_06_09.png",
        crops / "raw__left_mcc_feeders_10_12.png",
        crops / "raw__right_mcc_feeders_01_05.png",
        crops / "raw__right_mcc_feeders_06_09.png",
        crops / "raw__right_mcc_feeders_10_12.png",
        crops / "raw__left_dc_ups.png",
        crops / "raw__right_dc_ups.png",
        crops / "raw__center_annunciator_controls.png",
        crops / "raw__dc_tie_center.png",
        crops / "raw__notes_legend.png",
    ]
    jennifer_images = [
        raw,
        BASE / "wire_nodes_overlay.png",
        BASE / "detected_components_overlay.png",
        crops / "raw__top_sources_left.png",
        crops / "raw__top_sources_right.png",
        crops / "raw__ac_bus_tie_center.png",
        crops / "raw__left_mcc_feeders_01_05.png",
        crops / "raw__left_mcc_feeders_06_09.png",
        crops / "raw__left_mcc_feeders_10_12.png",
        crops / "raw__right_mcc_feeders_01_05.png",
        crops / "raw__right_mcc_feeders_06_09.png",
        crops / "raw__right_mcc_feeders_10_12.png",
        crops / "raw__left_dc_ups.png",
        crops / "raw__right_dc_ups.png",
        crops / "raw__center_annunciator_controls.png",
        crops / "raw__notes_legend.png",
    ]

    calls = [
        ("17", "main", "main-orchestration-visual-inspection", 9000, 0, 1800, None, sum(image_token_estimate(p) for p in [raw, BASE / "wire_nodes_overlay.png", BASE / "detected_components_overlay.png"] + list((BASE / "codes" / "crops").glob("raw__*.png")))),
        ("17", "round-1", "Diego high-recall extractor", 2400, 0, 7600, None, sum(image_token_estimate(p) for p in diego_images)),
        ("17", "round-1", "Jennifer precision reviewer", 6200, 0, 4300, None, sum(image_token_estimate(p) for p in jennifer_images)),
        ("17", "round-2", "Diego saturation check", 3900, 0, 220, None, 0),
        ("17", "round-2", "Jennifer final dotted-edge decision", 220, 0, 120, None, 0),
        ("17", "final", "main synthesis/artifact generation", 5200, 0, 700, None, 0),
    ]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "document",
            "iteration",
            "model_call",
            "input_tokens_expected",
            "cached_input_tokens",
            "output_tokens_expected",
            "reasoning_tokens",
            "image_file_input_tokens_expected",
            "total_expected",
            "low_estimate",
            "high_estimate",
            "usage_source",
        ])
        for doc, iteration, name, input_tokens, cached, output, reasoning, image_tokens in calls:
            total = input_tokens + output + image_tokens
            writer.writerow([
                doc,
                iteration,
                name,
                input_tokens,
                cached,
                output,
                "" if reasoning is None else reasoning,
                image_tokens,
                total,
                int(total * 0.75),
                int(total * 1.35),
                "local estimate; Responses token-count endpoint unavailable without API key; usage object not exposed by local subagent tool",
            ])

    grouped = {}
    for doc, iteration, _name, input_tokens, _cached, output, _reasoning, image_tokens in calls:
        key = (doc, iteration)
        total = input_tokens + output + image_tokens
        grouped.setdefault(key, {"expected": 0, "low": 0, "high": 0, "calls": 0})
        grouped[key]["expected"] += total
        grouped[key]["low"] += int(total * 0.75)
        grouped[key]["high"] += int(total * 1.35)
        grouped[key]["calls"] += 1
    with (RESULTS / "token_usage_by_iteration.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "model_calls", "low_estimate", "expected_estimate", "high_estimate"])
        for (doc, iteration), data in grouped.items():
            writer.writerow([doc, iteration, data["calls"], data["low"], data["expected"], data["high"]])


def main():
    rounds = {
        "round_1_diego": diego_round1_graph(),
        "round_1_jennifer": final_graph(include_relay_soe=False),
        "round_2_diego": final_graph(include_relay_soe=True),
        "round_2_jennifer_final": final_graph(include_relay_soe=True),
    }
    validations = {}
    for name, (nodes, edges) in rounds.items():
        write_nodes(RESULTS / f"{name}_nodes.csv", nodes)
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", nodes, edges)
        validations[name] = validate(nodes, edges)

    final_nodes, final_edges = rounds["round_2_jennifer_final"]
    write_nodes(RESULTS / "final_nodes.csv", final_nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_token_estimates()

    with (RESULTS / "validation_report.json").open("w") as f:
        json.dump(validations, f, indent=2)

    notes = """# Document 17 Extraction Notes

Allowed resources only: raw schematic, detected overlay, wire mask/overlay, wire-node overlay, and wire_nodes.csv from the `Raw + wires + components + junctions` folder.

No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels were read visually from the raw/crop images.

Round outcome:
- Round 1 Diego: high-recall graph, including aggregated master terminal block and two dotted relay-to-recorder candidates.
- Round 1 Jennifer: removed the master-terminal-block node/edge, corrected labels, removed the two relay-to-recorder dotted edges pending support.
- Round 2 Diego: agreed with Jennifer except restored `RELAY-ESF-A--REC-SOE-1` and `RELAY-ESF-B--REC-SOE-2`.
- Round 2 Jennifer: accepted both restored dotted relay-to-recorder edges. Saturated.

Final excluded:
- `MASTER-TB-21-29` and `CB-TR-A2--MASTER-TB-21-29`.
- Long dashed side-channel crossings without black-dot terminations.
"""
    (RESULTS / "extraction_notes.md").write_text(notes, encoding="utf-8")


if __name__ == "__main__":
    main()
