import csv
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


GLOBAL_NODES = [
    "GRID-230KV",
    "SWYD-230",
    "DS-101",
    "CB-101",
    "TR-SUT-1A",
    "TR-SUT-1B",
    "GEN-G1",
    "CB-201",
    "TR-UAT-1A",
    "TR-UAT-1B",
    "EDG-A",
    "CB-DGA",
    "EDG-B",
    "CB-DGB",
    "EDG-C",
    "CB-DGC",
    "EDG-D",
    "CB-DGD",
    "CB-TIE-AB",
    "CB-TIE-CD",
    "GND-PLANT",
]

BRANCH_NODES = {
    "A": [
        "CB-A01",
        "RLY-KA01",
        "DS-A01",
        "PMP-SI-A01",
        "CB-A02",
        "RLY-KA02",
        "PMP-RHR-A02",
        "CB-A03",
        "DS-A03",
        "MTR-CCW-A03",
        "CB-A04",
        "FAN-VC-A04",
        "CB-A05",
        "RLY-KA05",
        "MOV-RCS-A05",
        "CB-A06",
        "DS-A06",
        "PMP-CHG-A06",
        "CB-A07",
        "RLY-KA07",
        "HTR-CAB-A07",
        "CB-A08",
        "INST-RK-A08",
        "CB-A09",
        "VLV-HPI-A09",
        "CB-A10",
        "PNL-ESF-A10",
    ],
    "B": [
        "CB-B01",
        "PMP-SI-B01",
        "CB-B02",
        "RLY-KB02",
        "DS-B02",
        "PMP-RHR-B02",
        "CB-B03",
        "MTR-CCW-B03",
        "CB-B04",
        "RLY-KB04",
        "FAN-VC-B04",
        "CB-B05",
        "DS-B05",
        "MOV-RCS-B05",
        "CB-B06",
        "RLY-KB06",
        "PMP-CHG-B06",
        "CB-B07",
        "HTR-CAB-B07",
        "CB-B08",
        "DS-B08",
        "INST-RK-B08",
        "CB-B09",
        "VLV-HPI-B09",
        "CB-B10",
        "PNL-ESF-B10",
    ],
    "C": [
        "CB-C01",
        "RLY-KC01",
        "DS-C01",
        "PMP-SI-C01",
        "CB-C02",
        "PMP-RHR-C02",
        "CB-C03",
        "RLY-KC03",
        "MTR-CCW-C03",
        "CB-C04",
        "DS-C04",
        "FAN-VC-C04",
        "CB-C05",
        "MOV-RCS-C05",
        "CB-C06",
        "PMP-CHG-C06",
        "CB-C07",
        "DS-C07",
        "HTR-CAB-C07",
        "CB-C08",
        "RLY-KC08",
        "INST-RK-C08",
        "CB-C09",
        "VLV-HPI-C09",
        "CB-C10",
        "PNL-ESF-C10",
    ],
    "D": [
        "CB-D01",
        "PMP-SI-D01",
        "CB-D02",
        "RLY-KD02",
        "DS-D02",
        "PMP-RHR-D02",
        "CB-D03",
        "MTR-CCW-D03",
        "CB-D04",
        "FAN-VC-D04",
        "CB-D05",
        "RLY-KD05",
        "MOV-RCS-D05",
        "CB-D06",
        "DS-D06",
        "PMP-CHG-D06",
        "CB-D07",
        "RLY-KD07",
        "HTR-CAB-D07",
        "CB-D08",
        "INST-RK-D08",
        "CB-D09",
        "DS-D09",
        "VLV-HPI-D09",
        "CB-D10",
        "RLY-KD10",
        "PNL-ESF-D10",
    ],
}

MCC_EDGES = {
    "A": [
        ("MCC-A1", "CB-A01", "AC_POWER"),
        ("RLY-KA01", "CB-A01", "CONTROL_TRIP"),
        ("CB-A01", "DS-A01", "AC_POWER"),
        ("DS-A01", "PMP-SI-A01", "AC_POWER"),
        ("MCC-A1", "CB-A02", "AC_POWER"),
        ("RLY-KA02", "CB-A02", "CONTROL_TRIP"),
        ("CB-A02", "PMP-RHR-A02", "AC_POWER"),
        ("MCC-A1", "CB-A03", "AC_POWER"),
        ("CB-A03", "DS-A03", "AC_POWER"),
        ("DS-A03", "MTR-CCW-A03", "AC_POWER"),
        ("MCC-A1", "CB-A04", "AC_POWER"),
        ("CB-A04", "FAN-VC-A04", "AC_POWER"),
        ("MCC-A1", "CB-A05", "AC_POWER"),
        ("RLY-KA05", "CB-A05", "CONTROL_TRIP"),
        ("CB-A05", "MOV-RCS-A05", "AC_POWER"),
        ("MCC-A2", "CB-A06", "AC_POWER"),
        ("CB-A06", "DS-A06", "AC_POWER"),
        ("DS-A06", "PMP-CHG-A06", "AC_POWER"),
        ("MCC-A2", "CB-A07", "AC_POWER"),
        ("RLY-KA07", "CB-A07", "CONTROL_TRIP"),
        ("CB-A07", "HTR-CAB-A07", "AC_POWER"),
        ("MCC-A2", "CB-A08", "AC_POWER"),
        ("CB-A08", "INST-RK-A08", "AC_POWER"),
        ("MCC-A2", "CB-A09", "AC_POWER"),
        ("CB-A09", "VLV-HPI-A09", "AC_POWER"),
        ("MCC-A2", "CB-A10", "AC_POWER"),
        ("CB-A10", "PNL-ESF-A10", "AC_POWER"),
    ],
    "B": [
        ("MCC-B1", "CB-B01", "AC_POWER"),
        ("CB-B01", "PMP-SI-B01", "AC_POWER"),
        ("MCC-B1", "CB-B02", "AC_POWER"),
        ("RLY-KB02", "CB-B02", "CONTROL_TRIP"),
        ("CB-B02", "DS-B02", "AC_POWER"),
        ("DS-B02", "PMP-RHR-B02", "AC_POWER"),
        ("MCC-B1", "CB-B03", "AC_POWER"),
        ("CB-B03", "MTR-CCW-B03", "AC_POWER"),
        ("MCC-B1", "CB-B04", "AC_POWER"),
        ("RLY-KB04", "CB-B04", "CONTROL_TRIP"),
        ("CB-B04", "FAN-VC-B04", "AC_POWER"),
        ("MCC-B1", "CB-B05", "AC_POWER"),
        ("CB-B05", "DS-B05", "AC_POWER"),
        ("DS-B05", "MOV-RCS-B05", "AC_POWER"),
        ("MCC-B2", "CB-B06", "AC_POWER"),
        ("RLY-KB06", "CB-B06", "CONTROL_TRIP"),
        ("CB-B06", "PMP-CHG-B06", "AC_POWER"),
        ("MCC-B2", "CB-B07", "AC_POWER"),
        ("CB-B07", "HTR-CAB-B07", "AC_POWER"),
        ("MCC-B2", "CB-B08", "AC_POWER"),
        ("CB-B08", "DS-B08", "AC_POWER"),
        ("DS-B08", "INST-RK-B08", "AC_POWER"),
        ("MCC-B2", "CB-B09", "AC_POWER"),
        ("CB-B09", "VLV-HPI-B09", "AC_POWER"),
        ("MCC-B2", "CB-B10", "AC_POWER"),
        ("CB-B10", "PNL-ESF-B10", "AC_POWER"),
    ],
    "C": [
        ("MCC-C1", "CB-C01", "AC_POWER"),
        ("RLY-KC01", "CB-C01", "CONTROL_TRIP"),
        ("CB-C01", "DS-C01", "AC_POWER"),
        ("DS-C01", "PMP-SI-C01", "AC_POWER"),
        ("MCC-C1", "CB-C02", "AC_POWER"),
        ("CB-C02", "PMP-RHR-C02", "AC_POWER"),
        ("MCC-C1", "CB-C03", "AC_POWER"),
        ("RLY-KC03", "CB-C03", "CONTROL_TRIP"),
        ("CB-C03", "MTR-CCW-C03", "AC_POWER"),
        ("MCC-C1", "CB-C04", "AC_POWER"),
        ("CB-C04", "DS-C04", "AC_POWER"),
        ("DS-C04", "FAN-VC-C04", "AC_POWER"),
        ("MCC-C1", "CB-C05", "AC_POWER"),
        ("CB-C05", "MOV-RCS-C05", "AC_POWER"),
        ("MCC-C2", "CB-C06", "AC_POWER"),
        ("CB-C06", "PMP-CHG-C06", "AC_POWER"),
        ("MCC-C2", "CB-C07", "AC_POWER"),
        ("CB-C07", "DS-C07", "AC_POWER"),
        ("DS-C07", "HTR-CAB-C07", "AC_POWER"),
        ("MCC-C2", "CB-C08", "AC_POWER"),
        ("RLY-KC08", "CB-C08", "CONTROL_TRIP"),
        ("CB-C08", "INST-RK-C08", "AC_POWER"),
        ("MCC-C2", "CB-C09", "AC_POWER"),
        ("CB-C09", "VLV-HPI-C09", "AC_POWER"),
        ("MCC-C2", "CB-C10", "AC_POWER"),
        ("CB-C10", "PNL-ESF-C10", "AC_POWER"),
    ],
    "D": [
        ("MCC-D1", "CB-D01", "AC_POWER"),
        ("CB-D01", "PMP-SI-D01", "AC_POWER"),
        ("MCC-D1", "CB-D02", "AC_POWER"),
        ("RLY-KD02", "CB-D02", "CONTROL_TRIP"),
        ("CB-D02", "DS-D02", "AC_POWER"),
        ("DS-D02", "PMP-RHR-D02", "AC_POWER"),
        ("MCC-D1", "CB-D03", "AC_POWER"),
        ("CB-D03", "MTR-CCW-D03", "AC_POWER"),
        ("MCC-D1", "CB-D04", "AC_POWER"),
        ("CB-D04", "FAN-VC-D04", "AC_POWER"),
        ("MCC-D1", "CB-D05", "AC_POWER"),
        ("RLY-KD05", "CB-D05", "CONTROL_TRIP"),
        ("CB-D05", "MOV-RCS-D05", "AC_POWER"),
        ("MCC-D2", "CB-D06", "AC_POWER"),
        ("CB-D06", "DS-D06", "AC_POWER"),
        ("DS-D06", "PMP-CHG-D06", "AC_POWER"),
        ("MCC-D2", "CB-D07", "AC_POWER"),
        ("RLY-KD07", "CB-D07", "CONTROL_TRIP"),
        ("CB-D07", "HTR-CAB-D07", "AC_POWER"),
        ("MCC-D2", "CB-D08", "AC_POWER"),
        ("CB-D08", "INST-RK-D08", "AC_POWER"),
        ("MCC-D2", "CB-D09", "AC_POWER"),
        ("CB-D09", "DS-D09", "AC_POWER"),
        ("DS-D09", "VLV-HPI-D09", "AC_POWER"),
        ("MCC-D2", "CB-D10", "AC_POWER"),
        ("RLY-KD10", "CB-D10", "CONTROL_TRIP"),
        ("CB-D10", "PNL-ESF-D10", "AC_POWER"),
    ],
}


def train_nodes(train, combined_jb=False):
    jb = f"JB-{train}1/LOCAL-IO-{train}" if combined_jb else f"JB-{train}1"
    return [
        f"BUS-4{train}",
        f"CB-4{train}-48",
        f"TR-480{train}",
        f"CB-48{train}",
        f"LC-480{train}",
        f"PP-{train}1",
        f"MCC-{train}1",
        f"MCC-{train}2",
        jb,
        f"BAT-125{train}",
        f"CHG-125{train}",
        f"DC-BUS-{train}",
        f"INV-{train}",
        f"UPS-{train}",
        f"125VDC-{train}",
        f"GND-{train}",
    ] + BRANCH_NODES[train]


def unique(items):
    seen = set()
    output = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def edge(a, b, edge_type, evidence):
    return (a, b, edge_type, evidence)


def source_edges():
    return [
        edge("GRID-230KV", "SWYD-230", "AC_POWER", "solid_source_high"),
        edge("SWYD-230", "DS-101", "AC_POWER", "solid_source_high"),
        edge("DS-101", "CB-101", "AC_POWER", "solid_source_high"),
        edge("CB-101", "TR-SUT-1A", "AC_POWER", "solid_source_high"),
        edge("CB-101", "TR-SUT-1B", "AC_POWER", "solid_source_high"),
        edge("TR-SUT-1A", "BUS-4A", "AC_POWER", "solid_feeder_high"),
        edge("TR-SUT-1B", "BUS-4B", "AC_POWER", "solid_feeder_high"),
        edge("GEN-G1", "CB-201", "AC_POWER", "solid_source_high"),
        edge("CB-201", "TR-UAT-1A", "AC_POWER", "solid_source_high"),
        edge("CB-201", "TR-UAT-1B", "AC_POWER", "solid_source_med_high"),
        edge("TR-UAT-1A", "BUS-4C", "AC_POWER", "solid_feeder_high"),
        edge("TR-UAT-1B", "BUS-4D", "AC_POWER", "solid_feeder_high"),
        edge("EDG-A", "CB-DGA", "AC_POWER", "solid_source_high"),
        edge("CB-DGA", "BUS-4A", "AC_POWER", "solid_feeder_high"),
        edge("EDG-B", "CB-DGB", "AC_POWER", "solid_source_high"),
        edge("CB-DGB", "BUS-4B", "AC_POWER", "solid_feeder_high"),
        edge("EDG-C", "CB-DGC", "AC_POWER", "solid_source_high"),
        edge("CB-DGC", "BUS-4C", "AC_POWER", "solid_feeder_high"),
        edge("EDG-D", "CB-DGD", "AC_POWER", "solid_source_high"),
        edge("CB-DGD", "BUS-4D", "AC_POWER", "solid_feeder_high"),
        edge("BUS-4A", "CB-TIE-AB", "AC_POWER", "solid_tie_high"),
        edge("CB-TIE-AB", "BUS-4B", "AC_POWER", "solid_tie_high"),
        edge("BUS-4C", "CB-TIE-CD", "AC_POWER", "solid_tie_high"),
        edge("CB-TIE-CD", "BUS-4D", "AC_POWER", "solid_tie_high"),
    ]


def distribution_edges(train, combined_jb=False):
    jb = f"JB-{train}1/LOCAL-IO-{train}" if combined_jb else f"JB-{train}1"
    return [
        edge(f"BUS-4{train}", f"CB-4{train}-48", "AC_POWER", "solid_bus_tap_high"),
        edge(f"CB-4{train}-48", f"TR-480{train}", "AC_POWER", "solid_feeder_high"),
        edge(f"TR-480{train}", f"CB-48{train}", "AC_POWER", "solid_feeder_high"),
        edge(f"CB-48{train}", f"LC-480{train}", "AC_POWER", "solid_feeder_high"),
        edge(f"LC-480{train}", f"PP-{train}1", "AC_POWER", "solid_lc_tap_high"),
        edge(f"LC-480{train}", f"MCC-{train}1", "AC_POWER", "solid_lc_tap_high"),
        edge(f"LC-480{train}", f"MCC-{train}2", "AC_POWER", "solid_lc_tap_high"),
        edge(f"LC-480{train}", jb, "AC_POWER", "solid_lc_tap_high"),
        edge(f"PP-{train}1", f"UPS-{train}", "AC_POWER", "routed_solid_feed_med_high"),
        edge(f"BAT-125{train}", f"CHG-125{train}", "DC_POWER", "solid_dc_high"),
        edge(f"CHG-125{train}", f"DC-BUS-{train}", "DC_POWER", "solid_dc_high"),
        edge(f"DC-BUS-{train}", f"INV-{train}", "DC_POWER", "solid_dc_high"),
        edge(f"INV-{train}", f"UPS-{train}", "AC_POWER", "solid_converter_high"),
        edge(f"DC-BUS-{train}", f"125VDC-{train}", "DC_POWER", "solid_dc_stub_high"),
    ]


def final_nodes():
    nodes = GLOBAL_NODES[:]
    for train in "ABCD":
        nodes.extend(train_nodes(train, combined_jb=False))
    return unique(nodes)


def diego_round1_nodes():
    nodes = GLOBAL_NODES[:]
    nodes.extend([f"DG_AUTO_START_{train}" for train in "ABCD"])
    for train in "ABCD":
        nodes.extend(train_nodes(train, combined_jb=True))
    return unique(nodes)


def final_edges():
    edges = source_edges()
    for train in "ABCD":
        edges.extend(distribution_edges(train, combined_jb=False))
        for a, b, edge_type in MCC_EDGES[train]:
            evidence = "dashed_trip_high" if edge_type == "CONTROL_TRIP" else "solid_branch_high"
            if a.startswith("MCC-"):
                evidence = "solid_mcc_branch_high"
            edges.append(edge(a, b, edge_type, evidence))
    for train in "ABCD":
        edges.append(edge(f"GND-{train}", "GND-PLANT", "GROUNDING", "grounding_conductor_high"))
    return edges


def diego_round1_edges():
    edges = source_edges()
    for train in "ABCD":
        edges.extend(distribution_edges(train, combined_jb=True))
        for a, b, edge_type in MCC_EDGES[train]:
            evidence = "dashed_trip_high" if edge_type == "CONTROL_TRIP" else "solid_branch_high"
            if a.startswith("MCC-"):
                evidence = "solid_mcc_branch_high"
            edges.append(edge(a, b, edge_type, evidence))
        edges.append(
            edge(
                f"JB-{train}1/LOCAL-IO-{train}",
                f"DC-BUS-{train}",
                "CONTROL_TRIP",
                "diego_high_recall_dashed_path_low_conf",
            )
        )
        edges.append(
            edge(
                f"TR-480{train}",
                f"GND-{train}",
                "GROUNDING",
                "diego_high_recall_transformer_ground_low_conf",
            )
        )
        edges.append(edge(f"DG_AUTO_START_{train}", f"EDG-{train}", "CONTROL_TRIP", "diego_high_recall_annotation"))
        edges.append(edge(f"GND-{train}", "GND-PLANT", "GROUNDING", "grounding_conductor_high"))
    return edges


UNCERTAIN_EXCLUDED = [
    ("DG_AUTO_START_A,EDG-A", "annotation text only; no terminal node"),
    ("DG_AUTO_START_B,EDG-B", "annotation text only; no terminal node"),
    ("DG_AUTO_START_C,EDG-C", "annotation text only; no terminal node"),
    ("DG_AUTO_START_D,EDG-D", "annotation text only; no terminal node"),
    ("TR-480A,GND-A", "no clear transformer grounding terminal visible"),
    ("TR-480B,GND-B", "no clear transformer grounding terminal visible"),
    ("TR-480C,GND-C", "no clear transformer grounding terminal visible"),
    ("TR-480D,GND-D", "no clear transformer grounding terminal visible"),
    ("JB-A1,DC-BUS-A", "dashed/control contact near DC bus; no clear closed terminal/junction"),
    ("JB-B1,DC-BUS-B", "dashed/control contact near DC bus; no clear closed terminal/junction"),
    ("JB-C1,DC-BUS-C", "dashed/control contact near DC bus; no clear closed terminal/junction"),
    ("JB-D1,DC-BUS-D", "dashed/control contact near DC bus; no clear closed terminal/junction"),
    ("LOCAL-I/O-X", "label/terminal text, not a separate component node"),
    ("TO ANNUNCIATOR / PLANT PROCESS COMPUTER", "continuation arrow only"),
    ("CONTINUATION TO 125 VDC SYSTEM SHT-DC-2", "continuation label only"),
]


ROUNDS = [
    ("round_01_diego_high_recall", diego_round1_nodes, diego_round1_edges),
    ("round_02_jennifer_precision", final_nodes, final_edges),
    ("round_03_diego_saturation", final_nodes, final_edges),
]


def validate(nodes, edges):
    node_set = set(nodes)
    missing = sorted({n for a, b, _, _ in edges for n in (a, b) if n not in node_set})
    if missing:
        raise ValueError(f"Missing nodes referenced by edges: {missing}")
    duplicates = []
    seen = set()
    for a, b, _, _ in edges:
        if a == b:
            raise ValueError(f"Self-loop found: {a}")
        key = tuple(sorted((a, b)))
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    if duplicates:
        raise ValueError(f"Duplicate undirected edges: {duplicates}")


def write_node_order(path, nodes):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type", "evidence_conf"])
        writer.writerows(edges)


def write_matrix(path, nodes, edges):
    positions = {node: index for index, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b, _, _ in edges:
        i = positions[a]
        j = positions[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_uncertain():
    with (RESULTS / "uncertain_excluded_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["edge_or_node", "reason"])
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_round_notes():
    text = """# Document 13 round notes

## Round 1 - Diego high recall
Diego extracted the four-train source, 4.16 kV, 480 V, MCC, DC/UPS, relay/control, and grounding graph.
He included low-confidence DG auto-start annotation nodes, JB-to-DC-bus dashed paths, and transformer-to-ground edges for Jennifer to verify.

## Round 2 - Jennifer precision
Jennifer retained the visually supported solid source, distribution, MCC, DC/UPS, relay/control, and plant-ground connections.
She normalized JB-X1/LOCAL-IO-X to JB-X1, removed text-only DG auto-start nodes, removed transformer-to-ground edges without clear terminals, and excluded JB-to-DC-bus dashed paths as uncertain.

## Round 3 - Diego saturation
Diego agreed Jennifer's corrected graph was saturated. Final matrix equals round 2.
"""
    (RESULTS / "round_notes.md").write_text(text, encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    for prefix, nodes_fn, edges_fn in ROUNDS:
        nodes = nodes_fn()
        edges = edges_fn()
        validate(nodes, edges)
        write_node_order(RESULTS / f"{prefix}_node_order.csv", nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)

    final = final_nodes()
    edges = final_edges()
    write_node_order(RESULTS / "final_node_order.csv", final)
    write_edges(RESULTS / "final_edges.csv", edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final, edges)
    write_uncertain()
    write_round_notes()

    print(f"Final nodes: {len(final)}")
    print(f"Final edges: {len(edges)}")
    print(RESULTS)


if __name__ == "__main__":
    main()
