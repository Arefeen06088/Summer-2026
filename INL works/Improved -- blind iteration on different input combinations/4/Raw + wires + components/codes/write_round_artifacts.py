import csv
import shutil
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
ROUNDS_OUT = RESULTS / "rounds"


FINAL_NODES = [
    "US-345A",
    "CB-UAT-A",
    "TR-UAT-1",
    "CB-IN-A",
    "EDG-1A",
    "CB-DG-A",
    "US-230B",
    "CB-SAT-B",
    "TR-SAT-2",
    "CB-IN-B",
    "EDG-1B",
    "CB-DG-B",
    "BUS-480-RB1",
    "BUS-480-RB2",
    "CB-TIE-480",
    "CB-LC-A",
    "TR-LC-A",
    "CB-LC-A2",
    "BUS-480-LCA",
    "CB-LC-TIE",
    "BUS-480-LCB",
    "CB-LC-B",
    "TR-LC-B",
    "CB-LC-B2",
    "CB-F101",
    "OL-F101",
    "PMP-SI-1A",
    "CB-F102",
    "OL-F102",
    "PMP-RHR-1A",
    "CB-F103",
    "OL-F103",
    "FAN-CTMT-1A",
    "CB-F104",
    "OL-F104",
    "MOV-RC-104",
    "CB-F105",
    "OL-F105",
    "PMP-CCW-1A",
    "CB-F106",
    "OL-F106",
    "MOV-IA-106",
    "CB-F107",
    "OL-F107",
    "FAN-AHU-1A",
    "CB-F108",
    "OL-F108",
    "PMP-CS-1A",
    "CB-F109",
    "OL-F109",
    "MOV-EF-109",
    "CB-F110",
    "OL-F110",
    "HTR-PZR-1",
    "CB-F111",
    "OL-F111",
    "PMP-SI-1B",
    "CB-F112",
    "OL-F112",
    "PMP-RHR-1B",
    "CB-F113",
    "OL-F113",
    "FAN-CTMT-1B",
    "CB-F114",
    "OL-F114",
    "MOV-RC-114",
    "CB-F115",
    "OL-F115",
    "PNL-SPARE-F15",
    "CB-A201",
    "OL-201",
    "PMP-SW-2A",
    "CB-A202",
    "OL-202",
    "PMP-CVC-2A",
    "CB-A203",
    "OL-203",
    "MOV-SI-203",
    "CB-A204",
    "OL-204",
    "FAN-CR-2A",
    "CB-A205",
    "OL-205",
    "HTR-BATT-A",
    "CB-B206",
    "OL-206",
    "PMP-SW-2B",
    "CB-B207",
    "OL-207",
    "PMP-CVC-2B",
    "CB-B208",
    "OL-208",
    "MOV-SI-208",
    "CB-B209",
    "OL-209",
    "PNL-LTG-209",
    "CB-CHG-A",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DCA",
    "INV-120A",
    "BUS-UPS-A",
    "RPS-TRAIN-A",
    "ESFAS-TRAIN-A",
    "RELAY-K701",
    "TB-ESF-A",
    "ANN-CP-A",
    "CB-CHG-B",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DCB",
    "INV-120B",
    "BUS-UPS-B",
    "RPS-TRAIN-B",
    "ESFAS-TRAIN-B",
    "RELAY-K702",
    "TB-ESF-B",
    "REC-SER-01",
]


FINAL_EDGES = [
    ("US-345A", "CB-UAT-A"),
    ("CB-UAT-A", "TR-UAT-1"),
    ("TR-UAT-1", "CB-IN-A"),
    ("CB-IN-A", "BUS-480-RB1"),
    ("EDG-1A", "CB-DG-A"),
    ("CB-DG-A", "BUS-480-RB1"),
    ("US-230B", "CB-SAT-B"),
    ("CB-SAT-B", "TR-SAT-2"),
    ("TR-SAT-2", "CB-IN-B"),
    ("CB-IN-B", "BUS-480-RB2"),
    ("EDG-1B", "CB-DG-B"),
    ("CB-DG-B", "BUS-480-RB2"),
    ("BUS-480-RB1", "CB-TIE-480"),
    ("CB-TIE-480", "BUS-480-RB2"),
    ("BUS-480-RB1", "CB-LC-A"),
    ("CB-LC-A", "TR-LC-A"),
    ("TR-LC-A", "CB-LC-A2"),
    ("CB-LC-A2", "BUS-480-LCA"),
    ("BUS-480-RB2", "CB-LC-B"),
    ("CB-LC-B", "TR-LC-B"),
    ("TR-LC-B", "CB-LC-B2"),
    ("CB-LC-B2", "BUS-480-LCB"),
    ("BUS-480-LCA", "CB-LC-TIE"),
    ("CB-LC-TIE", "BUS-480-LCB"),
    ("BUS-480-RB1", "CB-F101"),
    ("CB-F101", "OL-F101"),
    ("OL-F101", "PMP-SI-1A"),
    ("BUS-480-RB2", "CB-F102"),
    ("CB-F102", "OL-F102"),
    ("OL-F102", "PMP-RHR-1A"),
    ("BUS-480-RB1", "CB-F103"),
    ("CB-F103", "OL-F103"),
    ("OL-F103", "FAN-CTMT-1A"),
    ("BUS-480-RB2", "CB-F104"),
    ("CB-F104", "OL-F104"),
    ("OL-F104", "MOV-RC-104"),
    ("BUS-480-RB1", "CB-F105"),
    ("CB-F105", "OL-F105"),
    ("OL-F105", "PMP-CCW-1A"),
    ("BUS-480-RB2", "CB-F106"),
    ("CB-F106", "OL-F106"),
    ("OL-F106", "MOV-IA-106"),
    ("BUS-480-RB1", "CB-F107"),
    ("CB-F107", "OL-F107"),
    ("OL-F107", "FAN-AHU-1A"),
    ("BUS-480-RB2", "CB-F108"),
    ("CB-F108", "OL-F108"),
    ("OL-F108", "PMP-CS-1A"),
    ("BUS-480-RB1", "CB-F109"),
    ("CB-F109", "OL-F109"),
    ("OL-F109", "MOV-EF-109"),
    ("BUS-480-RB2", "CB-F110"),
    ("CB-F110", "OL-F110"),
    ("OL-F110", "HTR-PZR-1"),
    ("BUS-480-RB1", "CB-F111"),
    ("CB-F111", "OL-F111"),
    ("OL-F111", "PMP-SI-1B"),
    ("BUS-480-RB2", "CB-F112"),
    ("CB-F112", "OL-F112"),
    ("OL-F112", "PMP-RHR-1B"),
    ("BUS-480-RB1", "CB-F113"),
    ("CB-F113", "OL-F113"),
    ("OL-F113", "FAN-CTMT-1B"),
    ("BUS-480-RB2", "CB-F114"),
    ("CB-F114", "OL-F114"),
    ("OL-F114", "MOV-RC-114"),
    ("BUS-480-RB1", "CB-F115"),
    ("CB-F115", "OL-F115"),
    ("OL-F115", "PNL-SPARE-F15"),
    ("BUS-480-LCA", "CB-A201"),
    ("CB-A201", "OL-201"),
    ("OL-201", "PMP-SW-2A"),
    ("BUS-480-LCA", "CB-A202"),
    ("CB-A202", "OL-202"),
    ("OL-202", "PMP-CVC-2A"),
    ("BUS-480-LCA", "CB-A203"),
    ("CB-A203", "OL-203"),
    ("OL-203", "MOV-SI-203"),
    ("BUS-480-LCA", "CB-A204"),
    ("CB-A204", "OL-204"),
    ("OL-204", "FAN-CR-2A"),
    ("BUS-480-LCA", "CB-A205"),
    ("CB-A205", "OL-205"),
    ("OL-205", "HTR-BATT-A"),
    ("BUS-480-LCB", "CB-B206"),
    ("CB-B206", "OL-206"),
    ("OL-206", "PMP-SW-2B"),
    ("BUS-480-LCB", "CB-B207"),
    ("CB-B207", "OL-207"),
    ("OL-207", "PMP-CVC-2B"),
    ("BUS-480-LCB", "CB-B208"),
    ("CB-B208", "OL-208"),
    ("OL-208", "MOV-SI-208"),
    ("BUS-480-LCB", "CB-B209"),
    ("CB-B209", "OL-209"),
    ("OL-209", "PNL-LTG-209"),
    ("BUS-480-LCB", "CB-CHG-A"),
    ("CB-CHG-A", "CHG-125A"),
    ("CHG-125A", "BUS-125DCA"),
    ("BUS-125DCA", "BAT-125A"),
    ("BUS-125DCA", "INV-120A"),
    ("INV-120A", "BUS-UPS-A"),
    ("BUS-UPS-A", "RPS-TRAIN-A"),
    ("BUS-UPS-A", "ESFAS-TRAIN-A"),
    ("BUS-480-LCB", "CB-CHG-B"),
    ("CB-CHG-B", "CHG-125B"),
    ("CHG-125B", "BUS-125DCB"),
    ("BUS-125DCB", "BAT-125B"),
    ("BUS-125DCB", "INV-120B"),
    ("INV-120B", "BUS-UPS-B"),
    ("BUS-UPS-B", "RPS-TRAIN-B"),
    ("BUS-UPS-B", "ESFAS-TRAIN-B"),
    ("RPS-TRAIN-A", "RELAY-K701"),
    ("ESFAS-TRAIN-A", "RELAY-K701"),
    ("RELAY-K701", "TB-ESF-A"),
    ("ANN-CP-A", "TB-ESF-A"),
    ("ANN-CP-A", "REC-SER-01"),
    ("RPS-TRAIN-B", "RELAY-K702"),
    ("ESFAS-TRAIN-B", "RELAY-K702"),
    ("RELAY-K702", "TB-ESF-B"),
    ("REC-SER-01", "TB-ESF-B"),
]


def make_diego_round1_nodes():
    nodes = list(FINAL_NODES)
    nodes.insert(nodes.index("CB-LC-A2"), "GND-NG-A")
    nodes.insert(nodes.index("CB-LC-B2"), "GND-NG-B")
    return nodes


def make_diego_round1_edges():
    edges = [edge for edge in FINAL_EDGES if edge != ("BUS-480-LCB", "CB-CHG-A")]
    edges.remove(("ANN-CP-A", "REC-SER-01"))
    edges.extend(
        [
            ("TR-LC-A", "GND-NG-A"),
            ("TR-LC-B", "GND-NG-B"),
            ("BUS-480-LCA", "CB-CHG-A"),
        ]
    )
    return edges


DIEGO_ROUND1_NODES = make_diego_round1_nodes()
DIEGO_ROUND1_EDGES = make_diego_round1_edges()
JENNIFER_ROUND1_NODES = FINAL_NODES
JENNIFER_ROUND1_EDGES = FINAL_EDGES


ROUNDS = {
    "diego_round1": {
        "nodes": DIEGO_ROUND1_NODES,
        "edges": DIEGO_ROUND1_EDGES,
        "notes": (
            "High-recall visual pass. Included GND-NG-A/GND-NG-B as possible "
            "ground-reference nodes, interpreted CB-CHG-A source as BUS-480-LCA, "
            "and did not include the ANN-CP-A--REC-SER-01 dashed signal link."
        ),
    },
    "jennifer_round1": {
        "nodes": JENNIFER_ROUND1_NODES,
        "edges": JENNIFER_ROUND1_EDGES,
        "notes": (
            "Precision pass removed GND-NG-A/GND-NG-B as reference symbols, "
            "changed CB-CHG-A source to BUS-480-LCB, and added the visually "
            "supported ANN-CP-A--REC-SER-01 dashed signal link."
        ),
    },
    "diego_round2_accepted": {
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "notes": (
            "Saturation check accepted Jennifer round 1. Diego agreed that "
            "ground symbols are not matrix nodes, both chargers are fed from "
            "BUS-480-LCB, and the ANN/REC dashed link crosses BUS-UPS-B without "
            "a junction."
        ),
    },
}


def validate(nodes, edges):
    duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
    if duplicates:
        raise ValueError(f"duplicate nodes: {duplicates}")

    node_set = set(nodes)
    missing = sorted({node for edge in edges for node in edge if node not in node_set})
    if missing:
        raise ValueError(f"edge references missing nodes: {missing}")

    normalized = [tuple(sorted(edge)) for edge in edges]
    duplicate_edges = sorted({edge for edge in normalized if normalized.count(edge) > 1})
    if duplicate_edges:
        raise ValueError(f"duplicate undirected edges: {duplicate_edges}")

    self_loops = [edge for edge in edges if edge[0] == edge[1]]
    if self_loops:
        raise ValueError(f"unexpected self loops: {self_loops}")


def write_round(name, nodes, edges, notes):
    validate(nodes, edges)
    ROUNDS_OUT.mkdir(parents=True, exist_ok=True)

    (ROUNDS_OUT / f"{name}_nodes.txt").write_text(
        "\n".join(nodes) + "\n", encoding="utf-8"
    )
    (ROUNDS_OUT / f"{name}_notes.md").write_text(notes + "\n", encoding="utf-8")

    with (ROUNDS_OUT / f"{name}_edges.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["source", "target", "connected"])
        for source, target in edges:
            writer.writerow([source, target, 1])

    with (ROUNDS_OUT / f"{name}_sparse_symmetric_matrix.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow(["source", "target", "connected"])
        for source, target in edges:
            writer.writerow([source, target, 1])
            writer.writerow([target, source, 1])

    edge_set = set(edges)
    reverse_edge_set = {(target, source) for source, target in edges}
    with (ROUNDS_OUT / f"{name}_connectivity_matrix.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow([""] + nodes)
        for row in nodes:
            writer.writerow(
                [row]
                + [
                    int(row != col and ((row, col) in edge_set or (row, col) in reverse_edge_set))
                    for col in nodes
                ]
            )


def copy_final_files(final_name):
    mappings = {
        f"{final_name}_connectivity_matrix.csv": "final_connectivity_matrix.csv",
        f"{final_name}_sparse_symmetric_matrix.csv": "final_sparse_symmetric_matrix.csv",
        f"{final_name}_edges.csv": "final_edges.csv",
        f"{final_name}_nodes.txt": "final_nodes.txt",
    }
    for source_name, target_name in mappings.items():
        shutil.copyfile(ROUNDS_OUT / source_name, RESULTS / target_name)


def write_final_summary(final_name):
    final = ROUNDS[final_name]
    nodes = final["nodes"]
    edges = final["edges"]
    summary = f"""# Final Connectivity Extraction

Document: 4 / Raw + wires + components

Iteration: 1

Final accepted round: {final_name}

Nodes: {len(nodes)}

Undirected edges: {len(edges)}

Diagonal: 0

Matrix symmetry: undirected/symmetric

Visual workflow:
- Diego round 1: high-recall extraction.
- Jennifer round 1: precision refinement.
- Diego round 2: accepted Jennifer's refinement; saturation reached.

Key refinements:
- Removed GND-NG-A and GND-NG-B from the matrix as neutral/ground reference symbols.
- Changed CB-CHG-A source from BUS-480-LCA to BUS-480-LCB after reviewing the LC-B vertical supply.
- Added ANN-CP-A--REC-SER-01 as a visible dashed signal link.
- Preserved the odd/even RB feeder alternation: odd F101/F103/.../F115 on BUS-480-RB1, even F102/F104/.../F114 on BUS-480-RB2.

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
"""
    (RESULTS / "final_summary.md").write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    for round_name, round_data in ROUNDS.items():
        write_round(
            round_name,
            round_data["nodes"],
            round_data["edges"],
            round_data["notes"],
        )
    copy_final_files("diego_round2_accepted")
    write_final_summary("diego_round2_accepted")
    print(f"Wrote {len(ROUNDS)} rounds to {ROUNDS_OUT}")
    print(f"Final graph: {len(FINAL_NODES)} nodes, {len(FINAL_EDGES)} undirected edges")
