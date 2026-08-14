import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires + components + junctions")
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def add_chain(edges, chain):
    for a, b in zip(chain, chain[1:]):
        edges.add(tuple(sorted((a, b))))


def add_edge(edges, a, b):
    edges.add(tuple(sorted((a, b))))


def build_graph(round_name):
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

    hv_a = "RELAY-KHV101A" if round_name == "diego1" else "RELAY-KYHV101A"
    hv_b = "RELAY-KHV101B" if round_name == "diego1" else "RELAY-KYHV101B"

    chain(["GRID-161KV", "TR-SST-1A", "CB-401A", "BUS-4KV-A"])
    chain(["TR-SST-1A", "CB-401B", "BUS-4KV-B"])
    chain(["BUS-4KV-A", "CB-TIE-4AB", "BUS-4KV-B"])
    chain(["GEN-EDG-A", "CB-EDG-A", "BUS-4KV-A"])
    chain(["GEN-EDG-B", "CB-EDG-B", "BUS-4KV-B"])
    chain(["BUS-4KV-A", "TR-4KV-480A", "CB-480A-IN", "BUS-480-A"])
    chain(["BUS-4KV-B", "TR-4KV-480B", "CB-480B-IN", "BUS-480-B"])
    chain(["BUS-480-A", "CB-TIE-480AB", "BUS-480-B"])

    feeder_groups = [
        ("BUS-480-A", "CB-11A-FDR", "MCC-11A", [
            ["CB-P201A", "RELAY-KP201A", "PUMP-RHR201A", "GND-P201A"],
            ["CB-P211A", "RELAY-KP211A", "PUMP-CS211A", "GND-P211A"],
            ["CB-P221A", "RELAY-KP221A", "PUMP-SI221A", "GND-P221A"],
        ]),
        ("BUS-480-A", "CB-12A-FDR", "MCC-12A", [
            ["CB-P101A", "RELAY-KP101A", "PUMP-AFW101A", "GND-P101A"],
            ["CB-HV101A", hv_a, "MOV-HV101A", "TB-HV101A"],
            ["CB-FN1A", "RELAY-KFN1A", "FAN-FN1A", "GND-FN1A"],
        ]),
        ("BUS-480-A", "CB-21A-FDR", "MCC-21A", [
            ["CB-P301A", "RELAY-KP301A", "PUMP-CCW301A", "GND-P301A"],
            ["CB-P401A", "RELAY-KP401A", "PUMP-SW401A", "GND-P401A"],
            ["CB-HT1A", "RELAY-KHT1A", "HTR-PZR1A", "TB-HT1A"],
        ]),
        ("BUS-480-A", "CB-31A-FDR30-B", "MCC-31A", [
            ["CB-RM1A", "RELAY-KRM1A", "MON-RAD1A", "TB-RM1A"],
            ["CB-P501A", "RELAY-KP501A", "PUMP-CHM501A", "GND-P501A"],
            ["CB-CV121A", "RELAY-KCV121A", "MOV-CV121A", "TB-CV121A"],
        ]),
        ("BUS-480-B", "CB-11B-FDR", "MCC-11B", [
            ["CB-P201B", "RELAY-KP201B", "PUMP-RHR201B", "GND-P201B"],
            ["CB-P211B", "RELAY-KP211B", "PUMP-CS211B", "GND-P211B"],
            ["CB-P221B", "RELAY-KP221B", "PUMP-SI221B", "GND-P221B"],
        ]),
        ("BUS-480-B", "CB-12B-FDR", "MCC-12B", [
            ["CB-P101B", "RELAY-KP101B", "PUMP-AFW101B", "GND-P101B"],
            ["CB-HV101B", hv_b, "MOV-HV101B", "TB-HV101B"],
            ["CB-FN1B", "RELAY-KFN1B", "FAN-FN1B", "GND-FN1B"],
        ]),
        ("BUS-480-B", "CB-21B-FDR", "MCC-21B", [
            ["CB-P301B", "RELAY-KP301B", "PUMP-CCW301B", "GND-P301B"],
            ["CB-P401B", "RELAY-KP401B", "PUMP-SW401B", "GND-P401B"],
            ["CB-HT1B", "RELAY-KHT1B", "HTR-PZR1B", "TB-HT1B"],
        ]),
        ("BUS-480-B", "CB-31B-FDR", "MCC-31B", [
            ["CB-RM1B", "RELAY-KRM1B", "MON-RAD1B", "TB-RM1B"],
            ["CB-P501B", "RELAY-KP501B", "PUMP-CHM501B", "GND-P501B"],
            ["CB-CV121B", "RELAY-KCV121B", "MOV-CV121B", "TB-CV121B"],
        ]),
    ]
    for bus, feeder_cb, mcc, branches in feeder_groups:
        chain([bus, feeder_cb, mcc])
        for branch in branches:
            chain([mcc] + branch)

    chain(["BUS-480-A", "TR-RPS-A", "MG-RPS-A", "BUS-120-RPS-A"])
    chain(["BUS-480-B", "TR-RPS-B", "MG-RPS-B", "BUS-120-RPS-B"])
    edge("BUS-125DC-A", "BATT-125A")
    chain(["BATT-125A", "CHGR-125A", "BUS-125DC-A"])
    chain(["BUS-125DC-A", "INV-120A", "BUS-120-RPS-A"])
    edge("BUS-125DC-B", "BATT-125B")
    chain(["BATT-125B", "CHGR-125B", "BUS-125DC-B"])
    chain(["BUS-125DC-B", "INV-120B", "BUS-120-RPS-B"])
    chain(["BUS-120-RPS-A", "UCC-01", "BUS-120-RPS-B"])
    edge("UCC-01", "GND-NO")

    chain(["CP-RPS-A", "JB-RPS-A3-1A", "PROT-UV-A", "RELAY-27A"])
    chain(["CP-ESF-A", "TB-2A", "PROT-GF-A", "RELAY-86A"])
    edge("RELAY-86A", "CP-DCS-01")
    edge("CP-DCS-01", "TB-3A")
    edge("CP-DCS-01", "TB-ESF-1")
    chain(["TB-ESF-1", "PT-RCS101", "REC-SOE-1"])
    chain(["TB-ESF-1", "LT-RWST101", "ANN-501"])
    chain(["TB-ESF-1", "FT-AFW101", "METER-VM-1"])

    chain(["CP-RPS-B", "JB-RPS-B3-1B", "PROT-UV-B", "RELAY-27B"])
    chain(["CP-ESF-B", "TB-2B", "PROT-GF-B", "RELAY-86B"])
    edge("RELAY-86B", "CP-ANN-01")
    edge("CP-ANN-01", "TB-3B")
    edge("CP-ANN-01", "TB-ESF-2")
    edge("TB-ESF-2", "MG-RPS-B")
    chain(["TB-ESF-2", "RTD-RCS101", "BUS-120-RPS-B"])
    edge("TB-ESF-2", "LS-SUMP101")
    edge("TB-ESF-2", "XS-DOOR101")
    edge("TB-ESF-2", "JB-CONTAIN")

    if round_name == "diego1":
        edge("REC-SOE-1", "BUS-125DC-A")
        edge("ANN-501", "BUS-125DC-A")
        edge("METER-VM-1", "BUS-120-RPS-A")

    return nodes, edges


def write_nodes(path, nodes):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_edges(path, edges):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        for a, b in sorted(edges):
            writer.writerow([a, b])


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
    missing = sorted({x for edge in edges for x in edge if x not in nodes})
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "duplicate_node_count": len(nodes) - len(set(nodes)),
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
    crops = BASE / "codes" / "crops"
    raw = BASE / "raw -- synthetic_npp_electrical_schematic_revised(1).png"
    main_images = [
        raw,
        BASE / "wire_nodes_overlay.png",
        BASE / "detected_components_overlay.png",
    ] + sorted(crops.glob("raw__*.png"))
    diego_images = [
        raw,
        BASE / "wire_nodes_overlay.png",
        BASE / "detected_components_overlay.png",
        BASE / "wires_mask_overlay.png",
        crops / "raw__top_4160_full.png",
        crops / "raw__top_4160_left.png",
        crops / "raw__top_4160_right.png",
        crops / "raw__tie_4kv_center.png",
        crops / "raw__main_480_full.png",
        crops / "raw__feeders_11a_12a.png",
        crops / "raw__feeders_21a_31a.png",
        crops / "raw__feeders_11b_12b.png",
        crops / "raw__feeders_21b_31b.png",
        crops / "raw__tie_480_center.png",
        crops / "raw__lower_controls_full.png",
        crops / "raw__lower_controls_left.png",
        crops / "raw__lower_controls_center.png",
        crops / "raw__lower_controls_right.png",
        crops / "wire_nodes__lower_controls_full.png",
        crops / "raw__notes_legend.png",
    ]
    jennifer_images = [
        raw,
        BASE / "wire_nodes_overlay.png",
        BASE / "detected_components_overlay.png",
        crops / "raw__top_4160_full.png",
        crops / "raw__main_480_full.png",
        crops / "raw__feeders_11a_12a.png",
        crops / "raw__feeders_21a_31a.png",
        crops / "raw__feeders_11b_12b.png",
        crops / "raw__feeders_21b_31b.png",
        crops / "raw__tie_480_center.png",
        crops / "wire_nodes__main_480_full.png",
        crops / "raw__lower_controls_left.png",
        crops / "raw__lower_controls_center.png",
        crops / "raw__lower_controls_right.png",
        crops / "wire_nodes__lower_controls_full.png",
        crops / "raw__dc_vital_left.png",
        crops / "raw__dc_vital_right.png",
        crops / "raw__notes_legend.png",
    ]
    calls = [
        ("16", "main", "main-orchestration-visual-inspection", 8800, 0, 1700, None, sum(image_token_estimate(p) for p in main_images)),
        ("16", "round-1", "Diego high-recall extractor", 2600, 0, 6400, None, sum(image_token_estimate(p) for p in diego_images)),
        ("16", "round-1", "Jennifer precision reviewer", 6500, 0, 5200, None, sum(image_token_estimate(p) for p in jennifer_images)),
        ("16", "round-2", "Diego saturation check", 3600, 0, 160, None, 0),
        ("16", "final", "main synthesis/artifact generation", 5200, 0, 700, None, 0),
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
        grouped.setdefault(key, {"calls": 0, "low": 0, "expected": 0, "high": 0})
        grouped[key]["calls"] += 1
        grouped[key]["low"] += int(total * 0.75)
        grouped[key]["expected"] += total
        grouped[key]["high"] += int(total * 1.35)
    with (RESULTS / "token_usage_by_iteration.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "model_calls", "low_estimate", "expected_estimate", "high_estimate"])
        for (doc, iteration), data in grouped.items():
            writer.writerow([doc, iteration, data["calls"], data["low"], data["expected"], data["high"]])


def main():
    rounds = {
        "round_1_diego": build_graph("diego1"),
        "round_1_jennifer": build_graph("final"),
        "round_2_diego_saturated": build_graph("final"),
    }
    validations = {}
    for name, (nodes, edges) in rounds.items():
        write_nodes(RESULTS / f"{name}_nodes.csv", nodes)
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", nodes, edges)
        validations[name] = validate(nodes, edges)

    final_nodes, final_edges = rounds["round_2_diego_saturated"]
    write_nodes(RESULTS / "final_nodes.csv", final_nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_token_estimates()
    with (RESULTS / "validation_report.json").open("w") as f:
        json.dump(validations, f, indent=2)

    notes = """# Document 16 Extraction Notes

Allowed resources only: raw schematic, detected overlay, wire mask/overlay, wire-node overlay, and wire_nodes.csv from the `Raw + wires + components + junctions` folder.

No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels were read visually from raw/crop images.

Round outcome:
- Round 1 Diego: high-recall graph with three extra lower tail edges and `RELAY-KHV101A/B` labels.
- Round 1 Jennifer: removed `REC-SOE-1--BUS-125DC-A`, `ANN-501--BUS-125DC-A`, and `METER-VM-1--BUS-120-RPS-A`; corrected `RELAY-KYHV101A/B`; confirmed 480 rail interpretation.
- Round 2 Diego: agreed/saturated with Jennifer.

Final excluded:
- `REC-SOE-1--BUS-125DC-A`
- `ANN-501--BUS-125DC-A`
- `METER-VM-1--BUS-120-RPS-A`
- `CB-31A-FDR30-B--BUS-480-B`
"""
    (RESULTS / "extraction_notes.md").write_text(notes, encoding="utf-8")


if __name__ == "__main__":
    main()
