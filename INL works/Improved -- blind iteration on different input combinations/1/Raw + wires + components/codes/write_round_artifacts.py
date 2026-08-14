import csv
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "rounds"


DIEGO_ROUND1_NODES = [
    "BUS-4KV-A",
    "GRID-345A",
    "SWGR-52A",
    "RAT-1A",
    "MAIN-GEN-1",
    "GCB-1",
    "UAT-1A",
    "EDG-1A",
    "CB-EDG-A",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "CB-4A-01",
    "TR-480A",
    "CB-48A-01",
    "BUS-480-A",
    "CB-P201A",
    "MCC-01A",
    "RELAY-K201A",
    "PUMP-P201A",
    "CB-P202A",
    "MCC-02A",
    "RELAY-K202A",
    "PUMP-P202A",
    "CB-M301A",
    "MCC-03A",
    "RELAY-K301A",
    "MOTOR-FAN301A",
    "CB-V410A",
    "MCC-04A",
    "SOL-V410A",
    "VALVE-V410A",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "BUS-120AC-A",
    "PNL-RPS-A",
    "RELAY-UV-A",
    "INSTR-PT-A",
    "BUS-4KV-B",
    "GRID-345B",
    "SWGR-52B",
    "RAT-1B",
    "EDG-1B",
    "CB-EDG-B",
    "CB-TIE-BC",
    "DS-TIE-BC",
    "CB-4B-01",
    "TR-480B",
    "CB-48B-01",
    "BUS-480-B",
    "CB-P201B",
    "MCC-01B",
    "RELAY-K201B",
    "PUMP-P201B",
    "CB-P202B",
    "MCC-02B",
    "RELAY-K202B",
    "PUMP-P202B",
    "CB-M301B",
    "MCC-03B",
    "RELAY-K301B",
    "MOTOR-FAN301B",
    "CB-V410B",
    "MCC-04B",
    "SOL-V410B",
    "VALVE-V410B",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "BUS-120AC-B",
    "PNL-RPS-B",
    "RELAY-UV-B",
    "INSTR-PT-B",
    "BUS-4KV-C",
    "EDG-1C",
    "CB-EDG-C",
    "AAC-GEN-1",
    "CB-AAC-C",
    "CB-4C-01",
    "TR-480C",
    "CB-48C-01",
    "BUS-480-C",
    "CB-P501",
    "MCC-05C",
    "RELAY-K501",
    "PUMP-CCW501",
    "CB-M601",
    "MCC-06C",
    "RELAY-K601",
    "MOTOR-HVAC601",
    "CB-V502",
    "MCC-07C",
    "SOL-V502",
    "VALVE-V502",
    "CB-P503",
    "MCC-08C",
    "RELAY-K503",
    "PUMP-SW503",
]


DIEGO_ROUND1_EDGES = [
    ("GRID-345A", "SWGR-52A"),
    ("SWGR-52A", "RAT-1A"),
    ("RAT-1A", "BUS-4KV-A"),
    ("MAIN-GEN-1", "GCB-1"),
    ("GCB-1", "UAT-1A"),
    ("UAT-1A", "BUS-4KV-A"),
    ("EDG-1A", "CB-EDG-A"),
    ("CB-EDG-A", "BUS-4KV-A"),
    ("BUS-4KV-A", "CB-TIE-AB"),
    ("CB-TIE-AB", "DS-TIE-AB"),
    ("DS-TIE-AB", "BUS-4KV-B"),
    ("BUS-4KV-A", "CB-4A-01"),
    ("CB-4A-01", "TR-480A"),
    ("TR-480A", "CB-48A-01"),
    ("CB-48A-01", "BUS-480-A"),
    ("BUS-480-A", "CB-P201A"),
    ("CB-P201A", "MCC-01A"),
    ("MCC-01A", "RELAY-K201A"),
    ("RELAY-K201A", "PUMP-P201A"),
    ("BUS-480-A", "CB-P202A"),
    ("CB-P202A", "MCC-02A"),
    ("MCC-02A", "RELAY-K202A"),
    ("RELAY-K202A", "PUMP-P202A"),
    ("BUS-480-A", "CB-M301A"),
    ("CB-M301A", "MCC-03A"),
    ("MCC-03A", "RELAY-K301A"),
    ("RELAY-K301A", "MOTOR-FAN301A"),
    ("BUS-480-A", "CB-V410A"),
    ("CB-V410A", "MCC-04A"),
    ("MCC-04A", "SOL-V410A"),
    ("SOL-V410A", "VALVE-V410A"),
    ("BUS-480-A", "CHG-125A"),
    ("CHG-125A", "BAT-125A"),
    ("BAT-125A", "BUS-125DC-A"),
    ("BUS-125DC-A", "INV-120A"),
    ("INV-120A", "BUS-120AC-A"),
    ("BUS-120AC-A", "PNL-RPS-A"),
    ("PNL-RPS-A", "RELAY-UV-A"),
    ("RELAY-UV-A", "INSTR-PT-A"),
    ("GRID-345B", "SWGR-52B"),
    ("SWGR-52B", "RAT-1B"),
    ("RAT-1B", "BUS-4KV-B"),
    ("EDG-1B", "CB-EDG-B"),
    ("CB-EDG-B", "BUS-4KV-B"),
    ("BUS-4KV-B", "CB-TIE-BC"),
    ("CB-TIE-BC", "DS-TIE-BC"),
    ("DS-TIE-BC", "BUS-4KV-C"),
    ("BUS-4KV-B", "CB-4B-01"),
    ("CB-4B-01", "TR-480B"),
    ("TR-480B", "CB-48B-01"),
    ("CB-48B-01", "BUS-480-B"),
    ("BUS-480-B", "CB-P201B"),
    ("CB-P201B", "MCC-01B"),
    ("MCC-01B", "RELAY-K201B"),
    ("RELAY-K201B", "PUMP-P201B"),
    ("BUS-480-B", "CB-P202B"),
    ("CB-P202B", "MCC-02B"),
    ("MCC-02B", "RELAY-K202B"),
    ("RELAY-K202B", "PUMP-P202B"),
    ("BUS-480-B", "CB-M301B"),
    ("CB-M301B", "MCC-03B"),
    ("MCC-03B", "RELAY-K301B"),
    ("RELAY-K301B", "MOTOR-FAN301B"),
    ("BUS-480-B", "CB-V410B"),
    ("CB-V410B", "MCC-04B"),
    ("MCC-04B", "SOL-V410B"),
    ("SOL-V410B", "VALVE-V410B"),
    ("BUS-480-B", "CHG-125B"),
    ("CHG-125B", "BAT-125B"),
    ("BAT-125B", "BUS-125DC-B"),
    ("BUS-125DC-B", "INV-120B"),
    ("INV-120B", "BUS-120AC-B"),
    ("BUS-120AC-B", "PNL-RPS-B"),
    ("PNL-RPS-B", "RELAY-UV-B"),
    ("RELAY-UV-B", "INSTR-PT-B"),
    ("EDG-1C", "CB-EDG-C"),
    ("CB-EDG-C", "BUS-4KV-C"),
    ("AAC-GEN-1", "CB-AAC-C"),
    ("CB-AAC-C", "BUS-4KV-C"),
    ("BUS-4KV-C", "CB-4C-01"),
    ("CB-4C-01", "TR-480C"),
    ("TR-480C", "CB-48C-01"),
    ("CB-48C-01", "BUS-480-C"),
    ("BUS-480-C", "CB-P501"),
    ("CB-P501", "MCC-05C"),
    ("MCC-05C", "RELAY-K501"),
    ("RELAY-K501", "PUMP-CCW501"),
    ("BUS-480-C", "CB-M601"),
    ("CB-M601", "MCC-06C"),
    ("MCC-06C", "RELAY-K601"),
    ("RELAY-K601", "MOTOR-HVAC601"),
    ("BUS-480-C", "CB-V502"),
    ("CB-V502", "MCC-07C"),
    ("MCC-07C", "SOL-V502"),
    ("SOL-V502", "VALVE-V502"),
    ("BUS-480-C", "CB-P503"),
    ("CB-P503", "MCC-08C"),
    ("MCC-08C", "RELAY-K503"),
    ("RELAY-K503", "PUMP-SW503"),
    ("BUS-125DC-A", "BUS-125DC-B"),
]


def insert_after(items, marker, additions):
    result = []
    for item in items:
        result.append(item)
        if item == marker:
            result.extend(additions)
    return result


JENNIFER_ROUND1_NODES = insert_after(
    insert_after(DIEGO_ROUND1_NODES, "RELAY-UV-A", ["PT-A"]), "RELAY-UV-B", ["PT-B"]
)


def make_jennifer_round1_edges():
    removed = {
        ("RELAY-UV-A", "INSTR-PT-A"),
        ("RELAY-UV-B", "INSTR-PT-B"),
        ("BUS-125DC-A", "BUS-125DC-B"),
    }
    edges = [edge for edge in DIEGO_ROUND1_EDGES if edge not in removed]
    edges.extend(
        [
            ("RELAY-UV-A", "PT-A"),
            ("PT-A", "INSTR-PT-A"),
            ("RELAY-UV-B", "PT-B"),
            ("PT-B", "INSTR-PT-B"),
        ]
    )
    return edges


JENNIFER_ROUND1_EDGES = make_jennifer_round1_edges()


ROUNDS = {
    "diego_round1": {
        "nodes": DIEGO_ROUND1_NODES,
        "edges": DIEGO_ROUND1_EDGES,
    },
    "jennifer_round1": {
        "nodes": JENNIFER_ROUND1_NODES,
        "edges": JENNIFER_ROUND1_EDGES,
    },
    "diego_round2_accepted": {
        "nodes": JENNIFER_ROUND1_NODES,
        "edges": JENNIFER_ROUND1_EDGES,
    },
}


def validate(nodes, edges):
    node_set = set(nodes)
    duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
    if duplicates:
        raise ValueError(f"duplicate nodes: {duplicates}")
    missing = sorted({node for edge in edges for node in edge if node not in node_set})
    if missing:
        raise ValueError(f"edge references missing nodes: {missing}")


def write_round(name, nodes, edges):
    validate(nodes, edges)
    OUT.mkdir(parents=True, exist_ok=True)

    (OUT / f"{name}_nodes.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")

    edge_set = {tuple(edge) for edge in edges}
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

    with (OUT / f"{name}_connectivity_matrix.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([""] + nodes)
        for row in nodes:
            values = []
            for col in nodes:
                connected = int(row != col and ((row, col) in edge_set or (col, row) in edge_set))
                values.append(connected)
            writer.writerow([row] + values)


if __name__ == "__main__":
    for round_name, round_data in ROUNDS.items():
        write_round(round_name, round_data["nodes"], round_data["edges"])
    print(f"Wrote {len(ROUNDS)} round(s) to {OUT}")
