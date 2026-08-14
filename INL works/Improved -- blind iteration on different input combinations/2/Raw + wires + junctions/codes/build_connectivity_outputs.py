from __future__ import annotations

import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw + wires + junctions")
RESULTS = BASE / "results"

NODES = [
    ("N01", "BUS-4160-A"),
    ("N02", "GRID-N501"),
    ("N03", "DS-N501"),
    ("N04", "TR-SU-1A"),
    ("N05", "CB-SU-1A"),
    ("N06", "GEN-EDG-A"),
    ("N07", "DS-DG-A"),
    ("N08", "CB-DG-A"),
    ("N09", "CB-TIE-4AB"),
    ("N10", "CB-F11A"),
    ("N11", "TR-LC11A"),
    ("N12", "BUS-480-A1"),
    ("N13", "CB-M11A"),
    ("N14", "MCC-11A"),
    ("N15", "CB-P101A"),
    ("N16", "MTR-P101A"),
    ("N17", "PUMP-RHR-A"),
    ("N18", "CB-F12A"),
    ("N19", "TR-LC12A"),
    ("N20", "BUS-480-A2"),
    ("N21", "CB-M12A"),
    ("N22", "MCC-12A"),
    ("N23", "CB-P201A"),
    ("N24", "MTR-P201A"),
    ("N25", "PUMP-SI-A"),
    ("N26", "CB-F13A"),
    ("N27", "TR-LC13A"),
    ("N28", "BUS-480-A3"),
    ("N29", "CB-M13A"),
    ("N30", "MCC-13A"),
    ("N31", "CB-FAN-A"),
    ("N32", "MTR-FAN-A"),
    ("N33", "FAN-CAV-A"),
    ("N34", "CB-F14A"),
    ("N35", "TR-RPS-A"),
    ("N36", "BUS-208-A"),
    ("N37", "REC-125-A"),
    ("N38", "BUS-125DC-A"),
    ("N39", "BAT-125-A"),
    ("N40", "INV-120-A"),
    ("N41", "BUS-120AC-A"),
    ("N42", "CP-RPS-A"),
    ("N43", "RLY-K501A"),
    ("N44", "INST-NI501A"),
    ("N45", "CB-CVCS-A"),
    ("N46", "MCC-CVCS-A"),
    ("N47", "MTR-CVCS-A"),
    ("N48", "PUMP-CVCS-A"),
    ("N49", "VLV-LCV201A"),
    ("N50", "BUS-4160-B"),
    ("N51", "GRID-R502"),
    ("N52", "DS-R502"),
    ("N53", "TR-SU-1B"),
    ("N54", "CB-SU-1B"),
    ("N55", "GEN-EDG-B"),
    ("N56", "DS-DG-B"),
    ("N57", "CB-DG-B"),
    ("N58", "GEN-AAC-1"),
    ("N59", "DS-AAC-1"),
    ("N60", "CB-AAC-1"),
    ("N61", "CB-F11B"),
    ("N62", "TR-LC11B"),
    ("N63", "BUS-480-B1"),
    ("N64", "CB-M11B"),
    ("N65", "MCC-11B"),
    ("N66", "CB-P101B"),
    ("N67", "MTR-P101B"),
    ("N68", "PUMP-RHR-B"),
    ("N69", "CB-F12B"),
    ("N70", "TR-LC12B"),
    ("N71", "BUS-480-B2"),
    ("N72", "CB-M12B"),
    ("N73", "MCC-12B"),
    ("N74", "CB-P201B"),
    ("N75", "MTR-P201B"),
    ("N76", "PUMP-SI-B"),
    ("N77", "CB-F13B"),
    ("N78", "TR-LC13B"),
    ("N79", "BUS-480-B3"),
    ("N80", "CB-M13B"),
    ("N81", "MCC-13B"),
    ("N82", "CB-FAN-B"),
    ("N83", "MTR-FAN-B"),
    ("N84", "FAN-CAV-B"),
    ("N85", "CB-F14B"),
    ("N86", "TR-RPS-B"),
    ("N87", "BUS-208-B"),
    ("N88", "REC-125-B"),
    ("N89", "BUS-125DC-B"),
    ("N90", "BAT-125-B"),
    ("N91", "INV-120-B"),
    ("N92", "BUS-120AC-B"),
    ("N93", "CP-RPS-B"),
    ("N94", "RLY-K501B"),
    ("N95", "INST-NI501B"),
    ("N96", "CB-CVCS-B"),
    ("N97", "MCC-CVCS-B"),
    ("N98", "MTR-CVCS-B"),
    ("N99", "PUMP-CVCS-B"),
    ("N100", "VLV-LCV201B"),
]

EDGE_SPECS = [
    ("N01", "N05", "solid"),
    ("N05", "N04", "solid"),
    ("N04", "N03", "solid"),
    ("N03", "N02", "solid"),
    ("N01", "N08", "solid"),
    ("N08", "N07", "solid"),
    ("N07", "N06", "solid"),
    ("N01", "N09", "solid_tie_terminal"),
    ("N09", "N50", "solid_tie_terminal"),
    ("N01", "N10", "solid"),
    ("N10", "N11", "solid"),
    ("N11", "N12", "solid"),
    ("N12", "N13", "solid"),
    ("N13", "N14", "solid"),
    ("N14", "N15", "solid"),
    ("N15", "N16", "solid"),
    ("N16", "N17", "solid"),
    ("N01", "N18", "solid"),
    ("N18", "N19", "solid"),
    ("N19", "N20", "solid"),
    ("N20", "N21", "solid"),
    ("N21", "N22", "solid"),
    ("N22", "N23", "solid"),
    ("N23", "N24", "solid"),
    ("N24", "N25", "solid"),
    ("N01", "N26", "solid"),
    ("N26", "N27", "solid"),
    ("N27", "N28", "solid"),
    ("N28", "N29", "solid"),
    ("N29", "N30", "solid"),
    ("N30", "N31", "solid"),
    ("N31", "N32", "solid"),
    ("N32", "N33", "solid"),
    ("N01", "N34", "solid"),
    ("N34", "N35", "solid"),
    ("N35", "N36", "solid"),
    ("N36", "N37", "solid"),
    ("N37", "N38", "solid"),
    ("N38", "N39", "solid_branch"),
    ("N38", "N40", "solid_branch"),
    ("N40", "N41", "solid"),
    ("N41", "N42", "solid"),
    ("N01", "N45", "solid"),
    ("N45", "N46", "solid"),
    ("N46", "N47", "solid"),
    ("N47", "N48", "solid"),
    ("N50", "N54", "solid"),
    ("N54", "N53", "solid"),
    ("N53", "N52", "solid"),
    ("N52", "N51", "solid"),
    ("N50", "N57", "solid"),
    ("N57", "N56", "solid"),
    ("N56", "N55", "solid"),
    ("N50", "N60", "solid"),
    ("N60", "N59", "solid"),
    ("N59", "N58", "solid"),
    ("N50", "N61", "solid"),
    ("N61", "N62", "solid"),
    ("N62", "N63", "solid"),
    ("N63", "N64", "solid"),
    ("N64", "N65", "solid"),
    ("N65", "N66", "solid"),
    ("N66", "N67", "solid"),
    ("N67", "N68", "solid"),
    ("N50", "N69", "solid"),
    ("N69", "N70", "solid"),
    ("N70", "N71", "solid"),
    ("N71", "N72", "solid"),
    ("N72", "N73", "solid"),
    ("N73", "N74", "solid"),
    ("N74", "N75", "solid"),
    ("N75", "N76", "solid"),
    ("N50", "N77", "solid"),
    ("N77", "N78", "solid"),
    ("N78", "N79", "solid"),
    ("N79", "N80", "solid"),
    ("N80", "N81", "solid"),
    ("N81", "N82", "solid"),
    ("N82", "N83", "solid"),
    ("N83", "N84", "solid"),
    ("N50", "N85", "solid"),
    ("N85", "N86", "solid"),
    ("N86", "N87", "solid"),
    ("N87", "N88", "solid"),
    ("N88", "N89", "solid"),
    ("N89", "N90", "solid_branch"),
    ("N89", "N91", "solid_branch"),
    ("N91", "N92", "solid"),
    ("N92", "N93", "solid"),
    ("N50", "N96", "solid"),
    ("N96", "N97", "solid"),
    ("N97", "N98", "solid"),
    ("N98", "N99", "solid"),
    ("N42", "N43", "signal"),
    ("N43", "N44", "signal"),
    ("N48", "N49", "signal"),
    ("N93", "N94", "signal"),
    ("N94", "N95", "signal"),
    ("N99", "N100", "signal"),
    ("N42", "N93", "signal_cross_train"),
]

ROUND_NOTES = {
    "round_01_diego": [
        "High-recall extraction from raw schematic and allowed wire/node aids.",
        "Included solid power feeders, explicit N.O. bus-tie component, and visibly terminated dashed signal/control links.",
        "No direct BUS-4160-A to BUS-4160-B edge was added except through CB-TIE-4AB.",
    ],
    "round_01_jennifer": [
        "Precision review accepted Diego round 1 unchanged.",
        "Retained dashed links as signal/control edges and excluded unlabeled border boxes, stubs, and crossing-only junctions.",
    ],
    "final": [
        "Consensus graph after Diego round 1 and Jennifer round 1.",
        "Matrix rows and columns are component/node labels in N01-N100 order.",
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
    edge_pairs = set()
    for source_id, target_id, _kind in EDGE_SPECS:
        if source_id not in valid or target_id not in valid:
            raise ValueError(f"Unknown node in edge {(source_id, target_id)}")
        if source_id == target_id:
            raise ValueError(f"Self-loop edge {(source_id, target_id)}")
        pair = tuple(sorted((source_id, target_id)))
        if pair in edge_pairs:
            raise ValueError(f"Duplicate edge {pair}")
        edge_pairs.add(pair)


def write_nodes(prefix: str) -> None:
    with (RESULTS / f"{prefix}_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label"])
        writer.writerows(NODES)


def write_edges(prefix: str) -> None:
    id_to_label = dict(NODES)
    with (RESULTS / f"{prefix}_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target", "kind"])
        for source_id, target_id, kind in EDGE_SPECS:
            writer.writerow([source_id, id_to_label[source_id], target_id, id_to_label[target_id], kind])


def write_matrix(prefix: str) -> None:
    ids = [node_id for node_id, _ in NODES]
    labels = [label for _, label in NODES]
    index = {node_id: i for i, node_id in enumerate(ids)}
    matrix = [[0 for _ in ids] for _ in ids]
    for source_id, target_id, _kind in EDGE_SPECS:
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
    path = RESULTS / f"{prefix}_notes.md"
    path.write_text(
        "# " + prefix.replace("_", " ").title() + "\n\n"
        + "\n".join(f"- {note}" for note in ROUND_NOTES[prefix])
        + f"\n\nNodes: {len(NODES)}\n\nEdges: {len(EDGE_SPECS)}\n",
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
    print(f"Wrote 3 matrix sets with {len(NODES)} nodes and {len(EDGE_SPECS)} edges to {RESULTS}")


if __name__ == "__main__":
    main()
