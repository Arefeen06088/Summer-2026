from __future__ import annotations

import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\1\Raw + wires + junctions")
RESULTS = BASE / "results"

NODES = [
    ("N001", "BUS-4KV-A"),
    ("N002", "GRID-345A"),
    ("N003", "SWGR-52A"),
    ("N004", "RAT-1A"),
    ("N005", "MAIN-GEN-1"),
    ("N006", "GCB-1"),
    ("N007", "UAT-1A"),
    ("N008", "EDG-1A"),
    ("N009", "CB-EDG-A"),
    ("N010", "CB-TIE-AB"),
    ("N011", "DS-TIE-AB"),
    ("N012", "BUS-4KV-B"),
    ("N013", "GRID-345B"),
    ("N014", "SWGR-52B"),
    ("N015", "RAT-1B"),
    ("N016", "EDG-1B"),
    ("N017", "CB-EDG-B"),
    ("N018", "CB-TIE-BC"),
    ("N019", "DS-TIE-BC"),
    ("N020", "BUS-4KV-C"),
    ("N021", "EDG-1C"),
    ("N022", "CB-EDG-C"),
    ("N023", "AAC-GEN-1"),
    ("N024", "CB-AAC-C"),
    ("N025", "CB-4A-01"),
    ("N026", "TR-480A"),
    ("N027", "CB-48A-01"),
    ("N028", "BUS-480-A"),
    ("N029", "CB-P201A"),
    ("N030", "MCC-01A"),
    ("N031", "RELAY-K201A"),
    ("N032", "PUMP-P201A"),
    ("N033", "CB-P202A"),
    ("N034", "MCC-02A"),
    ("N035", "RELAY-K202A"),
    ("N036", "PUMP-P202A"),
    ("N037", "CB-M301A"),
    ("N038", "MCC-03A"),
    ("N039", "RELAY-K301A"),
    ("N040", "MOTOR-FAN301A"),
    ("N041", "CB-V410A"),
    ("N042", "MCC-04A"),
    ("N043", "SOL-V410A"),
    ("N044", "VALVE-V410A"),
    ("N045", "CHG-125A"),
    ("N046", "BAT-125A"),
    ("N047", "BUS-125DC-A"),
    ("N048", "INV-120A"),
    ("N049", "BUS-120AC-A"),
    ("N050", "PNL-RPS-A"),
    ("N051", "RELAY-UV-A"),
    ("N052", "PT-A"),
    ("N053", "INSTR-PT-A"),
    ("N054", "CB-4B-01"),
    ("N055", "TR-480B"),
    ("N056", "CB-48B-01"),
    ("N057", "BUS-480-B"),
    ("N058", "CB-P201B"),
    ("N059", "MCC-01B"),
    ("N060", "RELAY-K201B"),
    ("N061", "PUMP-P201B"),
    ("N062", "CB-P202B"),
    ("N063", "MCC-02B"),
    ("N064", "RELAY-K202B"),
    ("N065", "PUMP-P202B"),
    ("N066", "CB-M301B"),
    ("N067", "MCC-03B"),
    ("N068", "RELAY-K301B"),
    ("N069", "MOTOR-FAN301B"),
    ("N070", "CB-V410B"),
    ("N071", "MCC-04B"),
    ("N072", "SOL-V410B"),
    ("N073", "VALVE-V410B"),
    ("N074", "CHG-125B"),
    ("N075", "BAT-125B"),
    ("N076", "BUS-125DC-B"),
    ("N077", "INV-120B"),
    ("N078", "BUS-120AC-B"),
    ("N079", "PNL-RPS-B"),
    ("N080", "RELAY-UV-B"),
    ("N081", "PT-B"),
    ("N082", "INSTR-PT-B"),
    ("N083", "CB-4C-01"),
    ("N084", "TR-480C"),
    ("N085", "CB-48C-01"),
    ("N086", "BUS-480-C"),
    ("N087", "CB-P501"),
    ("N088", "MCC-05C"),
    ("N089", "RELAY-K501"),
    ("N090", "PUMP-CCW501"),
    ("N091", "CB-M601"),
    ("N092", "MCC-06C"),
    ("N093", "RELAY-K601"),
    ("N094", "MOTOR-HVAC601"),
    ("N095", "CB-V502"),
    ("N096", "MCC-07C"),
    ("N097", "SOL-V502"),
    ("N098", "VALVE-V502"),
    ("N099", "CB-P503"),
    ("N100", "MCC-08C"),
    ("N101", "RELAY-K503"),
    ("N102", "PUMP-SW503"),
    ("N103", "DC-TIE-125AB"),
]

EDGES = [
    ("N002", "N003"),
    ("N003", "N004"),
    ("N004", "N001"),
    ("N005", "N006"),
    ("N006", "N007"),
    ("N007", "N001"),
    ("N008", "N009"),
    ("N009", "N001"),
    ("N001", "N010"),
    ("N010", "N011"),
    ("N011", "N012"),
    ("N013", "N014"),
    ("N014", "N015"),
    ("N015", "N012"),
    ("N016", "N017"),
    ("N017", "N012"),
    ("N012", "N018"),
    ("N018", "N019"),
    ("N019", "N020"),
    ("N021", "N022"),
    ("N022", "N020"),
    ("N023", "N024"),
    ("N024", "N020"),
    ("N001", "N025"),
    ("N025", "N026"),
    ("N026", "N027"),
    ("N027", "N028"),
    ("N012", "N054"),
    ("N054", "N055"),
    ("N055", "N056"),
    ("N056", "N057"),
    ("N020", "N083"),
    ("N083", "N084"),
    ("N084", "N085"),
    ("N085", "N086"),
    ("N028", "N029"),
    ("N029", "N030"),
    ("N030", "N031"),
    ("N031", "N032"),
    ("N028", "N033"),
    ("N033", "N034"),
    ("N034", "N035"),
    ("N035", "N036"),
    ("N028", "N037"),
    ("N037", "N038"),
    ("N038", "N039"),
    ("N039", "N040"),
    ("N028", "N041"),
    ("N041", "N042"),
    ("N042", "N043"),
    ("N043", "N044"),
    ("N028", "N045"),
    ("N045", "N046"),
    ("N046", "N047"),
    ("N047", "N048"),
    ("N048", "N049"),
    ("N049", "N050"),
    ("N050", "N051"),
    ("N051", "N052"),
    ("N052", "N053"),
    ("N057", "N058"),
    ("N058", "N059"),
    ("N059", "N060"),
    ("N060", "N061"),
    ("N057", "N062"),
    ("N062", "N063"),
    ("N063", "N064"),
    ("N064", "N065"),
    ("N057", "N066"),
    ("N066", "N067"),
    ("N067", "N068"),
    ("N068", "N069"),
    ("N057", "N070"),
    ("N070", "N071"),
    ("N071", "N072"),
    ("N072", "N073"),
    ("N057", "N074"),
    ("N074", "N075"),
    ("N075", "N076"),
    ("N076", "N077"),
    ("N077", "N078"),
    ("N078", "N079"),
    ("N079", "N080"),
    ("N080", "N081"),
    ("N081", "N082"),
    ("N086", "N087"),
    ("N087", "N088"),
    ("N088", "N089"),
    ("N089", "N090"),
    ("N086", "N091"),
    ("N091", "N092"),
    ("N092", "N093"),
    ("N093", "N094"),
    ("N086", "N095"),
    ("N095", "N096"),
    ("N096", "N097"),
    ("N097", "N098"),
    ("N086", "N099"),
    ("N099", "N100"),
    ("N100", "N101"),
    ("N101", "N102"),
    ("N047", "N103"),
    ("N103", "N076"),
]

ROUND_NOTES = {
    "round_01_diego": [
        "High-recall extraction from raw schematic and allowed wire/node aids.",
        "Included visible solid power/DC chains, dashed control/instrument links, explicit 4 kV bus-tie devices, and text-tagged normally-open DC tie.",
        "No direct bus-to-bus shorts were added across normally-open ties.",
    ],
    "round_01_jennifer": [
        "Precision review accepted Diego round 1 unchanged.",
        "Retained DC-TIE-125AB as a text-tagged normally-open tie between 125 VDC bus terminal dots.",
        "Retained dashed PNL-RPS/RELAY-UV/PT/INSTR-PT links as signal connectivity.",
    ],
    "final": [
        "Consensus graph after Diego round 1 and Jennifer round 1.",
        "Matrix rows and columns are component/node labels in N001-N103 order.",
    ],
}


def validate() -> None:
    ids = [node_id for node_id, _ in NODES]
    labels = [label for _, label in NODES]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate node ids")
    if len(labels) != len(set(labels)):
        raise ValueError("Duplicate node labels")
    valid = set(ids)
    for edge in EDGES:
        if edge[0] not in valid or edge[1] not in valid:
            raise ValueError(f"Unknown node in edge {edge}")
        if edge[0] == edge[1]:
            raise ValueError(f"Self-loop edge {edge}")


def write_nodes(prefix: str) -> None:
    with (RESULTS / f"{prefix}_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label"])
        writer.writerows(NODES)


def write_edges(prefix: str) -> None:
    id_to_label = dict(NODES)
    with (RESULTS / f"{prefix}_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target"])
        for source_id, target_id in EDGES:
            writer.writerow([source_id, id_to_label[source_id], target_id, id_to_label[target_id]])


def write_matrix(prefix: str) -> None:
    ids = [node_id for node_id, _ in NODES]
    labels = [label for _, label in NODES]
    index = {node_id: i for i, node_id in enumerate(ids)}
    matrix = [[0 for _ in ids] for _ in ids]
    for source_id, target_id in EDGES:
        i = index[source_id]
        j = index[target_id]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with (RESULTS / f"{prefix}_connectivity_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + labels)
        for label, row in zip(labels, matrix):
            writer.writerow([label] + row)


def write_notes(prefix: str) -> None:
    notes = ROUND_NOTES[prefix]
    path = RESULTS / f"{prefix}_notes.md"
    path.write_text(
        "# " + prefix.replace("_", " ").title() + "\n\n"
        + "\n".join(f"- {note}" for note in notes)
        + f"\n\nNodes: {len(NODES)}\n\nEdges: {len(EDGES)}\n",
        encoding="utf-8",
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    validate()
    for prefix in ["round_01_diego", "round_01_jennifer", "final"]:
        write_nodes(prefix)
        write_edges(prefix)
        write_matrix(prefix)
        write_notes(prefix)
    print(f"Wrote 3 matrix sets with {len(NODES)} nodes and {len(EDGES)} edges to {RESULTS}")


if __name__ == "__main__":
    main()
