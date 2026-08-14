import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


DIEGO_ROUND_1_NODES = [
    "US-345A", "CB-UAT-A", "TR-UAT-1", "CB-IN-A", "EDG-1A", "CB-DG-A", "BUS-480-RB1",
    "US-230B", "CB-SAT-B", "TR-SAT-2", "CB-IN-B", "EDG-1B", "CB-DG-B", "BUS-480-RB2",
    "CB-TIE-480", "CB-LC-A", "TR-LC-A", "GND-NG-A", "CB-LC-A2", "BUS-480-LCA",
    "CB-LC-TIE", "CB-LC-B", "TB-ESF-A", "TR-LC-B", "GND-NG-B", "RELAY-K701",
    "CB-LC-B2", "TB-ESF-B", "RELAY-K702", "BUS-480-LCB", "CB-F101", "OL-F101",
    "PMP-SI-1A", "CB-F102", "OL-F102", "PMP-RHR-1A", "CB-F103", "OL-F103",
    "FAN-CTMT-1A", "CB-F104", "OL-F104", "MOV-RC-104", "CB-F105", "OL-F105",
    "PMP-CCW-1A", "CB-F106", "OL-F106", "MOV-IA-106", "CB-F107", "OL-F107",
    "FAN-AHU-1A", "CB-F108", "OL-F108", "PMP-CS-1A", "CB-F109", "OL-F109",
    "MOV-EF-109", "CB-F110", "OL-F110", "HTR-PZR-1", "CB-F111", "OL-F111",
    "PMP-SI-1B", "CB-F112", "OL-F112", "PMP-RHR-1B", "CB-F113", "OL-F113",
    "FAN-CTMT-1B", "CB-F114", "OL-F114", "MOV-RC-114", "CB-F115", "OL-F115",
    "PNL-SPARE-F15", "CB-CHG-A", "CHG-125A", "BAT-125A", "BUS-125DCA", "INV-120A",
    "BUS-UPS-A", "RPS-TRAIN-A", "ESFAS-TRAIN-A", "CB-CHG-B", "CHG-125B", "BAT-125B",
    "BUS-125DCB", "INV-120B", "BUS-UPS-B", "RPS-TRAIN-B", "ESFAS-TRAIN-B", "ANN-CP-A",
    "REC-SER-01", "CB-A201", "OL-201", "PMP-SW-2A", "CB-A202", "OL-202", "PMP-CVC-2A",
    "CB-A203", "OL-203", "MOV-SI-203", "CB-A204", "OL-204", "FAN-CR-2A", "CB-A205",
    "OL-205", "HTR-BATT-A", "CB-B206", "OL-206", "PMP-SW-2B", "CB-B207", "OL-207",
    "PMP-CVC-2B", "CB-B208", "OL-208", "MOV-SI-208", "CB-B209", "OL-209", "PNL-LTG-209",
]


FINAL_NODES = [
    "US-345A", "CB-UAT-A", "TR-UAT-1", "CB-IN-A", "EDG-1A", "CB-DG-A", "BUS-480-RB1",
    "US-230B", "CB-SAT-B", "TR-SAT-2", "CB-IN-B", "EDG-1B", "CB-DG-B", "BUS-480-RB2",
    "CB-TIE-480", "CB-LC-A", "TR-LC-A", "GND-NG-A", "CB-LC-A2", "BUS-480-LCA",
    "CB-LC-TIE", "CB-LC-B", "TR-LC-B", "GND-NG-B", "CB-LC-B2", "BUS-480-LCB",
    "TB-ESF-A", "RELAY-K701", "TB-ESF-B", "RELAY-K702", "CB-F101", "OL-F101",
    "PMP-SI-1A", "CB-F102", "OL-F102", "PMP-RHR-1A", "CB-F103", "OL-F103",
    "FAN-CTMT-1A", "CB-F104", "OL-F104", "MOV-RC-104", "CB-F105", "OL-F105",
    "PMP-CCW-1A", "CB-F106", "OL-F106", "MOV-IA-106", "CB-F107", "OL-F107",
    "FAN-AHU-1A", "CB-F108", "OL-F108", "PMP-CS-1A", "CB-F109", "OL-F109",
    "MOV-EF-109", "CB-F110", "OL-F110", "HTR-PZR-1", "CB-F111", "OL-F111",
    "PMP-SI-1B", "CB-F112", "OL-F112", "PMP-RHR-1B", "CB-F113", "OL-F113",
    "FAN-CTMT-1B", "CB-F114", "OL-F114", "MOV-RC-114", "CB-F115", "OL-F115",
    "PNL-SPARE-F15", "CB-CHG-A", "CHG-125A", "BAT-125A", "BUS-125DCA", "INV-120A",
    "BUS-UPS-A", "RPS-TRAIN-A", "ESFAS-TRAIN-A", "CB-CHG-B", "CHG-125B", "BAT-125B",
    "BUS-125DCB", "INV-120B", "BUS-UPS-B", "RPS-TRAIN-B", "ESFAS-TRAIN-B", "ANN-CP-A",
    "REC-SER-01", "CB-A201", "OL-201", "PMP-SW-2A", "CB-A202", "OL-202", "PMP-CVC-2A",
    "CB-A203", "OL-203", "MOV-SI-203", "CB-A204", "OL-204", "FAN-CR-2A", "CB-A205",
    "OL-205", "HTR-BATT-A", "CB-B206", "OL-206", "PMP-SW-2B", "CB-B207", "OL-207",
    "PMP-CVC-2B", "CB-B208", "OL-208", "MOV-SI-208", "CB-B209", "OL-209", "PNL-LTG-209",
]


FINAL_EDGES = [
    ("US-345A", "CB-UAT-A"), ("CB-UAT-A", "TR-UAT-1"), ("TR-UAT-1", "CB-IN-A"),
    ("CB-IN-A", "BUS-480-RB1"), ("EDG-1A", "CB-DG-A"), ("CB-DG-A", "BUS-480-RB1"),
    ("US-230B", "CB-SAT-B"), ("CB-SAT-B", "TR-SAT-2"), ("TR-SAT-2", "CB-IN-B"),
    ("CB-IN-B", "BUS-480-RB2"), ("EDG-1B", "CB-DG-B"), ("CB-DG-B", "BUS-480-RB2"),
    ("BUS-480-RB1", "CB-TIE-480"), ("CB-TIE-480", "BUS-480-RB2"),
    ("BUS-480-RB1", "CB-LC-A"), ("CB-LC-A", "TR-LC-A"), ("TR-LC-A", "GND-NG-A"),
    ("TR-LC-A", "CB-LC-A2"), ("CB-LC-A2", "BUS-480-LCA"), ("BUS-480-RB2", "CB-LC-B"),
    ("CB-LC-B", "TR-LC-B"), ("TR-LC-B", "GND-NG-B"), ("TR-LC-B", "CB-LC-B2"),
    ("CB-LC-B2", "BUS-480-LCB"), ("BUS-480-LCA", "CB-LC-TIE"), ("CB-LC-TIE", "BUS-480-LCB"),
    ("BUS-480-RB1", "CB-F101"), ("CB-F101", "OL-F101"), ("OL-F101", "PMP-SI-1A"),
    ("BUS-480-RB2", "CB-F102"), ("CB-F102", "OL-F102"), ("OL-F102", "PMP-RHR-1A"),
    ("BUS-480-RB1", "CB-F103"), ("CB-F103", "OL-F103"), ("OL-F103", "FAN-CTMT-1A"),
    ("BUS-480-RB2", "CB-F104"), ("CB-F104", "OL-F104"), ("OL-F104", "MOV-RC-104"),
    ("BUS-480-RB1", "CB-F105"), ("CB-F105", "OL-F105"), ("OL-F105", "PMP-CCW-1A"),
    ("BUS-480-RB2", "CB-F106"), ("CB-F106", "OL-F106"), ("OL-F106", "MOV-IA-106"),
    ("BUS-480-RB1", "CB-F107"), ("CB-F107", "OL-F107"), ("OL-F107", "FAN-AHU-1A"),
    ("BUS-480-RB2", "CB-F108"), ("CB-F108", "OL-F108"), ("OL-F108", "PMP-CS-1A"),
    ("BUS-480-RB1", "CB-F109"), ("CB-F109", "OL-F109"), ("OL-F109", "MOV-EF-109"),
    ("BUS-480-RB2", "CB-F110"), ("CB-F110", "OL-F110"), ("OL-F110", "HTR-PZR-1"),
    ("BUS-480-RB1", "CB-F111"), ("CB-F111", "OL-F111"), ("OL-F111", "PMP-SI-1B"),
    ("BUS-480-RB2", "CB-F112"), ("CB-F112", "OL-F112"), ("OL-F112", "PMP-RHR-1B"),
    ("BUS-480-RB1", "CB-F113"), ("CB-F113", "OL-F113"), ("OL-F113", "FAN-CTMT-1B"),
    ("BUS-480-RB2", "CB-F114"), ("CB-F114", "OL-F114"), ("OL-F114", "MOV-RC-114"),
    ("BUS-480-RB1", "CB-F115"), ("CB-F115", "OL-F115"), ("OL-F115", "PNL-SPARE-F15"),
    ("BUS-480-LCA", "CB-CHG-A"), ("CB-CHG-A", "CHG-125A"), ("CHG-125A", "BUS-125DCA"),
    ("BAT-125A", "BUS-125DCA"), ("BUS-125DCA", "INV-120A"), ("INV-120A", "BUS-UPS-A"),
    ("BUS-UPS-A", "RPS-TRAIN-A"), ("BUS-UPS-A", "ESFAS-TRAIN-A"),
    ("BUS-480-LCB", "CB-CHG-B"), ("CB-CHG-B", "CHG-125B"), ("CHG-125B", "BUS-125DCB"),
    ("BAT-125B", "BUS-125DCB"), ("BUS-125DCB", "INV-120B"), ("INV-120B", "BUS-UPS-B"),
    ("BUS-UPS-B", "RPS-TRAIN-B"), ("BUS-UPS-B", "ESFAS-TRAIN-B"),
    ("RPS-TRAIN-A", "RELAY-K701"), ("ESFAS-TRAIN-A", "RELAY-K701"),
    ("RELAY-K701", "TB-ESF-A"), ("ANN-CP-A", "TB-ESF-A"),
    ("RPS-TRAIN-B", "RELAY-K702"), ("ESFAS-TRAIN-B", "RELAY-K702"),
    ("RELAY-K702", "TB-ESF-B"), ("REC-SER-01", "TB-ESF-B"), ("ANN-CP-A", "REC-SER-01"),
    ("BUS-480-LCA", "CB-A201"), ("CB-A201", "OL-201"), ("OL-201", "PMP-SW-2A"),
    ("BUS-480-LCA", "CB-A202"), ("CB-A202", "OL-202"), ("OL-202", "PMP-CVC-2A"),
    ("BUS-480-LCA", "CB-A203"), ("CB-A203", "OL-203"), ("OL-203", "MOV-SI-203"),
    ("BUS-480-LCA", "CB-A204"), ("CB-A204", "OL-204"), ("OL-204", "FAN-CR-2A"),
    ("BUS-480-LCA", "CB-A205"), ("CB-A205", "OL-205"), ("OL-205", "HTR-BATT-A"),
    ("BUS-480-LCB", "CB-B206"), ("CB-B206", "OL-206"), ("OL-206", "PMP-SW-2B"),
    ("BUS-480-LCB", "CB-B207"), ("CB-B207", "OL-207"), ("OL-207", "PMP-CVC-2B"),
    ("BUS-480-LCB", "CB-B208"), ("CB-B208", "OL-208"), ("OL-208", "MOV-SI-208"),
    ("BUS-480-LCB", "CB-B209"), ("CB-B209", "OL-209"), ("OL-209", "PNL-LTG-209"),
]


DIEGO_CONFIDENT_EDGES = [
    edge for edge in FINAL_EDGES
    if edge not in {
        ("CB-LC-B", "TR-LC-B"),
        ("CB-LC-B2", "BUS-480-LCB"),
        ("RPS-TRAIN-A", "RELAY-K701"),
        ("ESFAS-TRAIN-A", "RELAY-K701"),
        ("RELAY-K701", "TB-ESF-A"),
        ("ANN-CP-A", "TB-ESF-A"),
        ("RPS-TRAIN-B", "RELAY-K702"),
        ("ESFAS-TRAIN-B", "RELAY-K702"),
        ("RELAY-K702", "TB-ESF-B"),
        ("REC-SER-01", "TB-ESF-B"),
        ("ANN-CP-A", "REC-SER-01"),
    }
] + [
    ("CB-LC-B", "TB-ESF-A"),
    ("TB-ESF-A", "TR-LC-B"),
    ("CB-LC-B2", "TB-ESF-B"),
    ("TB-ESF-B", "BUS-480-LCB"),
]


DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES = [
    ("RPS-TRAIN-A", "RELAY-K701"),
    ("ESFAS-TRAIN-A", "RELAY-K701"),
    ("RELAY-K701", "TB-ESF-A"),
    ("ANN-CP-A", "TB-ESF-A"),
    ("RPS-TRAIN-B", "RELAY-K702"),
    ("ESFAS-TRAIN-B", "RELAY-K702"),
    ("RELAY-K702", "TB-ESF-B"),
    ("REC-SER-01", "TB-ESF-B"),
    ("ANN-CP-A", "REC-SER-01"),
    ("RELAY-K701", "CB-LC-B"),
    ("RELAY-K702", "CB-LC-B2"),
]


ROUND_NOTES = {
    "round_01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "matrix_policy": "Includes Diego's confident edges plus plausible/uncertain dashed/control extras as 1s; uncertain extras are listed separately.",
        "uncertain_edges_included": DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES,
    },
    "round_01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer",
        "matrix_policy": "Accepted visual edges only; solid LC-B feeder bypasses TB boxes, and accepted clearly connected dashed control/signal links.",
        "removed_or_replaced_edges": [
            ("CB-LC-B", "TB-ESF-A"),
            ("TB-ESF-A", "TR-LC-B"),
            ("CB-LC-B2", "TB-ESF-B"),
            ("TB-ESF-B", "BUS-480-LCB"),
            ("RELAY-K701", "CB-LC-B"),
            ("RELAY-K702", "CB-LC-B2"),
        ],
    },
    "round_02_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "matrix_policy": "Same as Jennifer round 1 after Diego agreement.",
    },
    "round_02_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "matrix_policy": "Same as Jennifer round 1 after final agreement.",
    },
    "final": {
        "agent": "main",
        "role": "saturated consensus",
        "matrix_policy": "Final accepted visible connectivity matrix.",
    },
}


def validate(nodes, edges):
    if len(nodes) != len(set(nodes)):
        raise ValueError("duplicate node label")
    seen = set()
    for edge in edges:
        if edge[0] == edge[1]:
            raise ValueError(f"self-loop: {edge}")
        if edge[0] not in nodes or edge[1] not in nodes:
            raise ValueError(f"edge references missing node: {edge}")
        key = tuple(sorted(edge))
        if key in seen:
            raise ValueError(f"duplicate undirected edge: {edge}")
        seen.add(key)


def write_nodes(prefix, nodes):
    with (RESULTS / f"{prefix}_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(prefix, edges):
    with (RESULTS / f"{prefix}_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        writer.writerows(edges)


def write_matrix(prefix, nodes, edges):
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in edges:
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with (RESULTS / f"{prefix}_connectivity_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_report(prefix, nodes, edges):
    payload = {
        "document": "4",
        "iteration": 1,
        "round": prefix,
        "node_count": len(nodes),
        "edge_count": len(edges),
        **ROUND_NOTES[prefix],
    }
    with (RESULTS / f"{prefix}_report.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_outputs(prefix, nodes, edges):
    validate(nodes, edges)
    write_nodes(prefix, nodes)
    write_edges(prefix, edges)
    write_matrix(prefix, nodes, edges)
    write_report(prefix, nodes, edges)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)

    diego_round_1_edges = DIEGO_CONFIDENT_EDGES + DIEGO_ROUND_1_PLAUSIBLE_EXTRA_EDGES
    write_outputs("round_01_diego", DIEGO_ROUND_1_NODES, diego_round_1_edges)

    for prefix in ["round_01_jennifer", "round_02_diego", "round_02_jennifer", "final"]:
        write_outputs(prefix, FINAL_NODES, FINAL_EDGES)

    rows = [
        ["document", "iteration", "round", "nodes", "edges", "matrix_file"],
        ["4", "1", "round_01_diego", len(DIEGO_ROUND_1_NODES), len(diego_round_1_edges), "round_01_diego_connectivity_matrix.csv"],
        ["4", "1", "round_01_jennifer", len(FINAL_NODES), len(FINAL_EDGES), "round_01_jennifer_connectivity_matrix.csv"],
        ["4", "1", "round_02_diego", len(FINAL_NODES), len(FINAL_EDGES), "round_02_diego_connectivity_matrix.csv"],
        ["4", "1", "round_02_jennifer", len(FINAL_NODES), len(FINAL_EDGES), "round_02_jennifer_connectivity_matrix.csv"],
        ["4", "1", "final", len(FINAL_NODES), len(FINAL_EDGES), "final_connectivity_matrix.csv"],
    ]
    with (RESULTS / "round_matrix_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)


if __name__ == "__main__":
    main()
