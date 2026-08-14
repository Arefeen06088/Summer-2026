import csv
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "rounds"


DIEGO_ROUND1_NODES = [
    "BUS-4160-A",
    "BUS-4160-B",
    "GRID-N501",
    "DS-N501",
    "TR-SU-1A",
    "CB-SU-1A",
    "GEN-EDG-A",
    "DS-DG-A",
    "CB-DG-A",
    "CB-TIE-4AB",
    "GRID-R502",
    "DS-R502",
    "TR-SU-1B",
    "CB-SU-1B",
    "GEN-EDG-B",
    "DS-DG-B",
    "CB-DG-B",
    "GEN-AAC-1",
    "DS-AAC-1",
    "CB-AAC-1",
    "CB-F11A",
    "TR-LC11A",
    "BUS-480-A1",
    "CB-M11A",
    "MCC-11A",
    "CB-P101A",
    "MTR-P101A",
    "PUMP-RHR-A",
    "CB-F12A",
    "TR-LC12A",
    "BUS-480-A2",
    "CB-M12A",
    "MCC-12A",
    "CB-P201A",
    "MTR-P201A",
    "PUMP-SI-A",
    "CB-F13A",
    "TR-LC13A",
    "BUS-480-A3",
    "CB-M13A",
    "MCC-13A",
    "CB-FAN-A",
    "MTR-FAN-A",
    "FAN-CAV-A",
    "CB-F14A",
    "TR-RPS-A",
    "BUS-208-A",
    "REC-125-A",
    "BUS-125DC-A",
    "BAT-125-A",
    "INV-120-A",
    "BUS-120AC-A",
    "CP-RPS-A",
    "RLY-K501A",
    "INST-N501A",
    "CB-CVCS-A",
    "MCC-CVCS-A",
    "MTR-CVCS-A",
    "PUMP-CVCS-A",
    "VLV-LCV201A",
    "CB-F11B",
    "TR-LC11B",
    "BUS-480-B1",
    "CB-M11B",
    "MCC-11B",
    "CB-P101B",
    "MTR-P101B",
    "PUMP-RHR-B",
    "CB-F12B",
    "TR-LC12B",
    "BUS-480-B2",
    "CB-M12B",
    "MCC-12B",
    "CB-P201B",
    "MTR-P201B",
    "PUMP-SI-B",
    "CB-F13B",
    "TR-LC13B",
    "BUS-480-B3",
    "CB-M13B",
    "MCC-13B",
    "CB-FAN-B",
    "MTR-FAN-B",
    "FAN-CAV-B",
    "CB-F14B",
    "TR-RPS-B",
    "BUS-208-B",
    "REC-125-B",
    "BUS-125DC-B",
    "BAT-125-B",
    "INV-120-B",
    "BUS-120AC-B",
    "CP-RPS-B",
    "RLY-K501B",
    "INST-N501B",
    "CB-CVCS-B",
    "MCC-CVCS-B",
    "MTR-CVCS-B",
    "PUMP-CVCS-B",
    "VLV-LCV201B",
]


DIEGO_ROUND1_EDGES = [
    ("GRID-N501", "DS-N501"),
    ("DS-N501", "TR-SU-1A"),
    ("TR-SU-1A", "CB-SU-1A"),
    ("CB-SU-1A", "BUS-4160-A"),
    ("GEN-EDG-A", "DS-DG-A"),
    ("DS-DG-A", "CB-DG-A"),
    ("CB-DG-A", "BUS-4160-A"),
    ("BUS-4160-A", "CB-TIE-4AB"),
    ("CB-TIE-4AB", "BUS-4160-B"),
    ("GRID-R502", "DS-R502"),
    ("DS-R502", "TR-SU-1B"),
    ("TR-SU-1B", "CB-SU-1B"),
    ("CB-SU-1B", "BUS-4160-B"),
    ("GEN-EDG-B", "DS-DG-B"),
    ("DS-DG-B", "CB-DG-B"),
    ("CB-DG-B", "BUS-4160-B"),
    ("GEN-AAC-1", "DS-AAC-1"),
    ("DS-AAC-1", "CB-AAC-1"),
    ("CB-AAC-1", "BUS-4160-B"),
    ("BUS-4160-A", "CB-F11A"),
    ("CB-F11A", "TR-LC11A"),
    ("TR-LC11A", "BUS-480-A1"),
    ("BUS-480-A1", "CB-M11A"),
    ("CB-M11A", "MCC-11A"),
    ("MCC-11A", "CB-P101A"),
    ("CB-P101A", "MTR-P101A"),
    ("MTR-P101A", "PUMP-RHR-A"),
    ("BUS-4160-A", "CB-F12A"),
    ("CB-F12A", "TR-LC12A"),
    ("TR-LC12A", "BUS-480-A2"),
    ("BUS-480-A2", "CB-M12A"),
    ("CB-M12A", "MCC-12A"),
    ("MCC-12A", "CB-P201A"),
    ("CB-P201A", "MTR-P201A"),
    ("MTR-P201A", "PUMP-SI-A"),
    ("BUS-4160-A", "CB-F13A"),
    ("CB-F13A", "TR-LC13A"),
    ("TR-LC13A", "BUS-480-A3"),
    ("BUS-480-A3", "CB-M13A"),
    ("CB-M13A", "MCC-13A"),
    ("MCC-13A", "CB-FAN-A"),
    ("CB-FAN-A", "MTR-FAN-A"),
    ("MTR-FAN-A", "FAN-CAV-A"),
    ("BUS-4160-A", "CB-F14A"),
    ("CB-F14A", "TR-RPS-A"),
    ("TR-RPS-A", "BUS-208-A"),
    ("BUS-208-A", "REC-125-A"),
    ("REC-125-A", "BUS-125DC-A"),
    ("BUS-125DC-A", "BAT-125-A"),
    ("BUS-125DC-A", "INV-120-A"),
    ("INV-120-A", "BUS-120AC-A"),
    ("BUS-120AC-A", "CP-RPS-A"),
    ("CP-RPS-A", "RLY-K501A"),
    ("RLY-K501A", "INST-N501A"),
    ("BUS-4160-A", "CB-CVCS-A"),
    ("CB-CVCS-A", "MCC-CVCS-A"),
    ("MCC-CVCS-A", "MTR-CVCS-A"),
    ("MTR-CVCS-A", "PUMP-CVCS-A"),
    ("PUMP-CVCS-A", "VLV-LCV201A"),
    ("BUS-4160-B", "CB-F11B"),
    ("CB-F11B", "TR-LC11B"),
    ("TR-LC11B", "BUS-480-B1"),
    ("BUS-480-B1", "CB-M11B"),
    ("CB-M11B", "MCC-11B"),
    ("MCC-11B", "CB-P101B"),
    ("CB-P101B", "MTR-P101B"),
    ("MTR-P101B", "PUMP-RHR-B"),
    ("BUS-4160-B", "CB-F12B"),
    ("CB-F12B", "TR-LC12B"),
    ("TR-LC12B", "BUS-480-B2"),
    ("BUS-480-B2", "CB-M12B"),
    ("CB-M12B", "MCC-12B"),
    ("MCC-12B", "CB-P201B"),
    ("CB-P201B", "MTR-P201B"),
    ("MTR-P201B", "PUMP-SI-B"),
    ("BUS-4160-B", "CB-F13B"),
    ("CB-F13B", "TR-LC13B"),
    ("TR-LC13B", "BUS-480-B3"),
    ("BUS-480-B3", "CB-M13B"),
    ("CB-M13B", "MCC-13B"),
    ("MCC-13B", "CB-FAN-B"),
    ("CB-FAN-B", "MTR-FAN-B"),
    ("MTR-FAN-B", "FAN-CAV-B"),
    ("BUS-4160-B", "CB-F14B"),
    ("CB-F14B", "TR-RPS-B"),
    ("TR-RPS-B", "BUS-208-B"),
    ("BUS-208-B", "REC-125-B"),
    ("REC-125-B", "BUS-125DC-B"),
    ("BUS-125DC-B", "BAT-125-B"),
    ("BUS-125DC-B", "INV-120-B"),
    ("INV-120-B", "BUS-120AC-B"),
    ("BUS-120AC-B", "CP-RPS-B"),
    ("CP-RPS-B", "RLY-K501B"),
    ("RLY-K501B", "INST-N501B"),
    ("BUS-4160-B", "CB-CVCS-B"),
    ("CB-CVCS-B", "MCC-CVCS-B"),
    ("MCC-CVCS-B", "MTR-CVCS-B"),
    ("MTR-CVCS-B", "PUMP-CVCS-B"),
    ("PUMP-CVCS-B", "VLV-LCV201B"),
    ("CP-RPS-A", "CP-RPS-B"),
]


ROUNDS = {
    "diego_round1": {
        "nodes": DIEGO_ROUND1_NODES,
        "edges": DIEGO_ROUND1_EDGES,
    },
    "jennifer_round1": {
        "nodes": DIEGO_ROUND1_NODES,
        "edges": DIEGO_ROUND1_EDGES,
    },
    "diego_round2_accepted": {
        "nodes": DIEGO_ROUND1_NODES,
        "edges": DIEGO_ROUND1_EDGES,
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


def write_round(name, nodes, edges):
    validate(nodes, edges)
    OUT.mkdir(parents=True, exist_ok=True)

    (OUT / f"{name}_nodes.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")

    with (OUT / f"{name}_edges.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["source", "target", "connected"])
        for source, target in edges:
            writer.writerow([source, target, 1])

    with (OUT / f"{name}_sparse_symmetric_matrix.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["source", "target", "connected"])
        for source, target in edges:
            writer.writerow([source, target, 1])
            writer.writerow([target, source, 1])

    edge_set = set(edges)
    with (OUT / f"{name}_connectivity_matrix.csv").open("w", newline="", encoding="utf-8") as fh:
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


if __name__ == "__main__":
    for round_name, round_data in ROUNDS.items():
        write_round(round_name, round_data["nodes"], round_data["edges"])
    print(f"Wrote {len(ROUNDS)} round(s) to {OUT}")
