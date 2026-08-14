import csv
import shutil
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
ROUNDS_OUT = RESULTS / "rounds"


DIEGO_ROUND1_NODES = [
    "GRID-1",
    "AUX-TR-1A",
    "CB-101",
    "BUS-416A",
    "BUS-TIE-41",
    "GND-1E",
    "BUS-416B",
    "CB-102",
    "AUX-TR-1B",
    "GRID-2",
    "EDG-1A",
    "CB-DG1A",
    "TR-480A1",
    "CB-480A1",
    "MCC-480A1",
    "TR-480A2",
    "CB-480A2",
    "MCC-480A2",
    "EDG-1B",
    "CB-DG1B",
    "TR-480B1",
    "CB-480B1",
    "MCC-480B1",
    "TR-480B2",
    "CB-480B2",
    "MCC-480B2",
    "CB-CHG-A",
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-A",
    "INV-120A",
    "BUS-120A",
    "CB-CHG-B",
    "CHGR-125B",
    "BAT-125B",
    "DC-BUS-B",
    "INV-120B",
    "BUS-120B",
    "FDB-A1",
    "CB-SI-A1",
    "PUMP-SI-A1",
    "CB-RHR-A1",
    "PUMP-RHR-A1",
    "CB-CCW-A1",
    "PUMP-CCW-A1",
    "CB-FAN-A1",
    "FAN-CR-A1",
    "CB-MOV-A101",
    "VALVE-SI-A101",
    "CB-MOV-A102",
    "VALVE-RHR-A102",
    "FDB-A2",
    "CB-CS-A2",
    "PUMP-CS-A2",
    "CB-SW-A2",
    "PUMP-SW-A2",
    "CB-AFW-A2",
    "PUMP-AFW-A2",
    "CB-FAN-A2",
    "FAN-EB-A2",
    "CB-MOV-A201",
    "VALVE-CCW-A201",
    "CB-HTR-A2",
    "HTR-BAY-A2",
    "FDB-B1",
    "CB-SI-B1",
    "PUMP-SI-B1",
    "CB-RHR-B1",
    "PUMP-RHR-B1",
    "CB-CCW-B1",
    "PUMP-CCW-B1",
    "CB-FAN-B1",
    "FAN-CR-B1",
    "CB-MOV-B101",
    "VALVE-SI-B101",
    "CB-MOV-B102",
    "VALVE-RHR-B102",
    "FDB-B2",
    "CB-CS-B2",
    "PUMP-CS-B2",
    "CB-SW-B2",
    "PUMP-SW-B2",
    "CB-FAN-B2",
    "FAN-EB-B2",
    "CB-MOV-B201",
    "VALVE-CCW-B201",
    "CB-HTR-B2",
    "HTR-BAY-B2",
    "PANEL-RPS-A",
    "RELAY-K27A",
    "INST-PT-A",
    "INST-LT-A",
    "PANEL-ESF-A",
    "JB-A401",
    "PANEL-RPS-B",
    "RELAY-K27B",
    "INST-PT-B",
    "INST-LT-B",
    "PANEL-ESF-B",
    "JB-B501",
]


DIEGO_ROUND1_EDGES = [
    ("GRID-1", "AUX-TR-1A"),
    ("AUX-TR-1A", "CB-101"),
    ("CB-101", "BUS-416A"),
    ("BUS-416A", "BUS-TIE-41"),
    ("BUS-TIE-41", "GND-1E"),
    ("BUS-TIE-41", "BUS-416B"),
    ("BUS-416B", "CB-102"),
    ("CB-102", "AUX-TR-1B"),
    ("AUX-TR-1B", "GRID-2"),
    ("EDG-1A", "CB-DG1A"),
    ("CB-DG1A", "BUS-416A"),
    ("BUS-416A", "TR-480A1"),
    ("TR-480A1", "CB-480A1"),
    ("CB-480A1", "MCC-480A1"),
    ("MCC-480A1", "FDB-A1"),
    ("BUS-416A", "TR-480A2"),
    ("TR-480A2", "CB-480A2"),
    ("CB-480A2", "MCC-480A2"),
    ("MCC-480A2", "FDB-A2"),
    ("EDG-1B", "CB-DG1B"),
    ("CB-DG1B", "BUS-416B"),
    ("BUS-416B", "TR-480B1"),
    ("TR-480B1", "CB-480B1"),
    ("CB-480B1", "MCC-480B1"),
    ("MCC-480B1", "FDB-B1"),
    ("BUS-416B", "TR-480B2"),
    ("TR-480B2", "CB-480B2"),
    ("CB-480B2", "MCC-480B2"),
    ("MCC-480B2", "FDB-B2"),
    ("BUS-416A", "CB-CHG-A"),
    ("CB-CHG-A", "CHGR-125A"),
    ("CHGR-125A", "DC-BUS-A"),
    ("BAT-125A", "DC-BUS-A"),
    ("DC-BUS-A", "INV-120A"),
    ("INV-120A", "BUS-120A"),
    ("BUS-416B", "CB-CHG-B"),
    ("CB-CHG-B", "CHGR-125B"),
    ("CHGR-125B", "DC-BUS-B"),
    ("BAT-125B", "DC-BUS-B"),
    ("DC-BUS-B", "INV-120B"),
    ("INV-120B", "BUS-120B"),
    ("FDB-A1", "CB-SI-A1"),
    ("CB-SI-A1", "PUMP-SI-A1"),
    ("FDB-A1", "CB-RHR-A1"),
    ("CB-RHR-A1", "PUMP-RHR-A1"),
    ("FDB-A1", "CB-CCW-A1"),
    ("CB-CCW-A1", "PUMP-CCW-A1"),
    ("FDB-A1", "CB-FAN-A1"),
    ("CB-FAN-A1", "FAN-CR-A1"),
    ("FDB-A1", "CB-MOV-A101"),
    ("CB-MOV-A101", "VALVE-SI-A101"),
    ("FDB-A1", "CB-MOV-A102"),
    ("CB-MOV-A102", "VALVE-RHR-A102"),
    ("FDB-A2", "CB-CS-A2"),
    ("CB-CS-A2", "PUMP-CS-A2"),
    ("FDB-A2", "CB-SW-A2"),
    ("CB-SW-A2", "PUMP-SW-A2"),
    ("FDB-A2", "CB-AFW-A2"),
    ("CB-AFW-A2", "PUMP-AFW-A2"),
    ("FDB-A2", "CB-FAN-A2"),
    ("CB-FAN-A2", "FAN-EB-A2"),
    ("FDB-A2", "CB-MOV-A201"),
    ("CB-MOV-A201", "VALVE-CCW-A201"),
    ("FDB-A2", "CB-HTR-A2"),
    ("CB-HTR-A2", "HTR-BAY-A2"),
    ("FDB-B1", "CB-SI-B1"),
    ("CB-SI-B1", "PUMP-SI-B1"),
    ("FDB-B1", "CB-RHR-B1"),
    ("CB-RHR-B1", "PUMP-RHR-B1"),
    ("FDB-B1", "CB-CCW-B1"),
    ("CB-CCW-B1", "PUMP-CCW-B1"),
    ("FDB-B1", "CB-FAN-B1"),
    ("CB-FAN-B1", "FAN-CR-B1"),
    ("FDB-B1", "CB-MOV-B101"),
    ("CB-MOV-B101", "VALVE-SI-B101"),
    ("FDB-B1", "CB-MOV-B102"),
    ("CB-MOV-B102", "VALVE-RHR-B102"),
    ("FDB-B2", "CB-CS-B2"),
    ("CB-CS-B2", "PUMP-CS-B2"),
    ("FDB-B2", "CB-SW-B2"),
    ("CB-SW-B2", "PUMP-SW-B2"),
    ("FDB-B2", "CB-FAN-B2"),
    ("CB-FAN-B2", "FAN-EB-B2"),
    ("FDB-B2", "CB-MOV-B201"),
    ("CB-MOV-B201", "VALVE-CCW-B201"),
    ("FDB-B2", "CB-HTR-B2"),
    ("CB-HTR-B2", "HTR-BAY-B2"),
    ("BUS-120A", "PANEL-RPS-A"),
    ("PANEL-RPS-A", "INST-PT-A"),
    ("PANEL-RPS-A", "RELAY-K27A"),
    ("PANEL-RPS-A", "INST-LT-A"),
    ("RELAY-K27A", "PANEL-ESF-A"),
    ("PANEL-ESF-A", "JB-A401"),
    ("BUS-120B", "PANEL-RPS-B"),
    ("PANEL-RPS-B", "INST-PT-B"),
    ("PANEL-RPS-B", "RELAY-K27B"),
    ("PANEL-RPS-B", "INST-LT-B"),
    ("RELAY-K27B", "PANEL-ESF-B"),
    ("PANEL-ESF-B", "JB-B501"),
    ("BUS-120A", "BUS-120B"),
]


JENNIFER_ROUND1_NODES = [
    node for node in DIEGO_ROUND1_NODES if node != "GND-1E"
]
JENNIFER_ROUND1_NODES.insert(JENNIFER_ROUND1_NODES.index("PANEL-RPS-B"), "TB-A401")
JENNIFER_ROUND1_NODES.append("TB-B501")


def make_jennifer_round1_edges():
    removed = {
        ("BUS-TIE-41", "GND-1E"),
        ("BUS-120A", "BUS-120B"),
    }
    edges = [edge for edge in DIEGO_ROUND1_EDGES if edge not in removed]
    edges.extend(
        [
            ("JB-A401", "TB-A401"),
            ("JB-B501", "TB-B501"),
        ]
    )
    return edges


JENNIFER_ROUND1_EDGES = make_jennifer_round1_edges()


ROUNDS = {
    "diego_round1": {
        "nodes": DIEGO_ROUND1_NODES,
        "edges": DIEGO_ROUND1_EDGES,
        "notes": (
            "High-recall visual pass. Included weak/uncertain edges "
            "BUS-120A--BUS-120B and BUS-TIE-41--GND-1E."
        ),
    },
    "jennifer_round1": {
        "nodes": JENNIFER_ROUND1_NODES,
        "edges": JENNIFER_ROUND1_EDGES,
        "notes": (
            "Precision pass removed unsupported BUS-120A--BUS-120B and "
            "BUS-TIE-41--GND-1E, added TB-A401/TB-B501 with JB edges."
        ),
    },
    "diego_round2_accepted": {
        "nodes": JENNIFER_ROUND1_NODES,
        "edges": JENNIFER_ROUND1_EDGES,
        "notes": (
            "Saturation check accepted Jennifer round 1. Kept INST-PT/LT labels "
            "as visible component identifiers."
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
    with (ROUNDS_OUT / f"{name}_connectivity_matrix.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow([""] + nodes)
        for row in nodes:
            writer.writerow(
                [row]
                + [
                    int(row != col and ((row, col) in edge_set or (col, row) in edge_set))
                    for col in nodes
                ]
            )


def write_final_summary(final_name):
    final = ROUNDS[final_name]
    nodes = final["nodes"]
    edges = final["edges"]
    summary = f"""# Final Connectivity Extraction

Document: 3 / Raw + wires + components

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
- Removed unsupported BUS-120A--BUS-120B edge; the two 120 VAC instrument buses have a visible gap.
- Removed unsupported BUS-TIE-41--GND-1E edge; GND-1E is visible but not geometrically tied to BUS-TIE-41.
- Added terminal blocks TB-A401 and TB-B501, connected from JB-A401 and JB-B501.
- Kept INST-PT-A, INST-LT-A, INST-PT-B, and INST-LT-B as component identifiers; PT-A/LT-A/PT-B/LT-B are secondary visible labels.

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
"""
    (RESULTS / "final_summary.md").write_text(summary, encoding="utf-8")


def copy_final_files(final_name):
    mappings = {
        f"{final_name}_connectivity_matrix.csv": "final_connectivity_matrix.csv",
        f"{final_name}_sparse_symmetric_matrix.csv": "final_sparse_symmetric_matrix.csv",
        f"{final_name}_edges.csv": "final_edges.csv",
        f"{final_name}_nodes.txt": "final_nodes.txt",
    }
    for source_name, target_name in mappings.items():
        shutil.copyfile(ROUNDS_OUT / source_name, RESULTS / target_name)


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
    print("Final graph: 101 nodes, 100 undirected edges")
