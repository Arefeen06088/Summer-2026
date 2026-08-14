import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\19")
ART = BASE / "Codes and artifacts"
RESULTS = BASE / "Results" / "Iteration_1"
LABELS = ART / "component_labels_list.csv"
MATRIX_OUT = RESULTS / "round_01_diego_matrix.csv"
NOTES_OUT = RESULTS / "round_01_diego_notes.md"


CPT_NUMBERS = {"201", "202", "203", "204", "301", "302", "401", "402", "501", "502", "601", "701"}
BUS_NODES = [
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-480-A",
    "BUS-480-B",
    "BUS-120AC-A",
    "BUS-120AC-B",
    "BUS-125DC-A",
    "BUS-125DC-B",
]
VISUAL_NODES_MISSED_BY_CSV = ["DS-F301", "CB-F402", "LS-MOV601"]


def corrected(label: str) -> str:
    if label.startswith("PT-") and label[3:] in CPT_NUMBERS:
        return "CPT-" + label[3:]
    return label


def load_nodes():
    nodes = []
    with LABELS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            label = corrected(row["normalized_label"])
            if label not in nodes:
                nodes.append(label)
    # Visible in raw crops but not captured in the component CSV.
    for visual_node in VISUAL_NODES_MISSED_BY_CSV:
        if visual_node not in nodes:
            if visual_node == "LS-MOV601" and "INST-601" in nodes:
                insert_at = nodes.index("INST-601") + 1
            elif visual_node == "DS-F301" and "DS-F203" in nodes:
                insert_at = nodes.index("DS-F203") + 1
            elif visual_node == "CB-F402" and "CB-F302" in nodes:
                insert_at = nodes.index("CB-F302") + 1
            else:
                insert_at = len(nodes)
            nodes.insert(insert_at, visual_node)
    for bus in BUS_NODES:
        if bus not in nodes:
            nodes.append(bus)
    return nodes


solid_edges = []
dashed_edges = []
uncertain_included_edges = []


def add(edge_list, a, b):
    edge_list.append((a, b))


# Top 4160 switchgear, source, tie, and 480 transformer feeds.
for edge in [
    ("GRID-1", "DS-101"),
    ("DS-101", "CB-101"),
    ("CB-101", "TR-101"),
    ("TR-101", "BUS-4160-A"),
    ("DG-1", "CB-DG1"),
    ("CB-DG1", "BUS-4160-A"),
    ("PT-4160A", "BUS-4160-A"),
    ("BUS-4160-A", "CB-TIE-4160"),
    ("CB-TIE-4160", "BUS-4160-B"),
    ("BUS-4160-A", "CB-201"),
    ("CB-201", "TR-480-A"),
    ("TR-480-A", "CB-480-A"),
    ("CB-480-A", "BUS-480-A"),
    ("GRID-2", "DS-102"),
    ("DS-102", "CB-102"),
    ("CB-102", "TR-102"),
    ("TR-102", "BUS-4160-B"),
    ("DG-2", "CB-DG2"),
    ("CB-DG2", "BUS-4160-B"),
    ("PT-4160B", "BUS-4160-B"),
    ("BUS-4160-B", "CB-202"),
    ("CB-202", "TR-480-B"),
    ("TR-480-B", "CB-480-B"),
    ("CB-480-B", "BUS-480-B"),
    ("BUS-480-A", "CB-TIE-480"),
    ("CB-TIE-480", "BUS-480-B"),
]:
    add(solid_edges, *edge)


feeders = {
    "201": ("BUS-480-A", "PUMP-P201", "INST-201"),
    "203": ("BUS-480-A", "PUMP-P203", "INST-203"),
    "301": ("BUS-480-A", "PUMP-P301", "INST-301"),
    "401": ("BUS-480-A", "PUMP-P401", "INST-401"),
    "501": ("BUS-480-A", "MTR-F501", "INST-501"),
    "601": ("BUS-480-A", "VALVE-MOV601", "INST-601"),
    "202": ("BUS-480-B", "PUMP-P202", "INST-202"),
    "204": ("BUS-480-B", "PUMP-P204", "INST-204"),
    "302": ("BUS-480-B", "PUMP-P302", "INST-302"),
    "402": ("BUS-480-B", "PUMP-P402", "INST-402"),
    "502": ("BUS-480-B", "MTR-F502", "INST-502"),
    "701": ("BUS-480-B", "INST-RPS701", "INST-701"),
}

for n, (bus, load, inst) in feeders.items():
    for edge in [
        (bus, f"CB-F{n}"),
        (f"CB-F{n}", f"DS-F{n}"),
        (f"DS-F{n}", f"CPT-{n}"),
        (f"CPT-{n}", f"MCC-{n}"),
        (f"MCC-{n}", f"CB-L{n}"),
        (f"CB-L{n}", f"RELAY-K{n}"),
        (f"RELAY-K{n}", load),
    ]:
        add(solid_edges, *edge)
    for edge in [
        (f"CB-F{n}", f"RELAY-PR{n}"),
        (f"MCC-{n}", f"RELAY-A{n}"),
        (load, inst),
    ]:
        add(dashed_edges, *edge)
    if n == "601":
        add(dashed_edges, "INST-601", "LS-MOV601")
        add(dashed_edges, "LS-MOV601", "JB-601")
    else:
        add(dashed_edges, inst, f"JB-{n}")
    add(dashed_edges, f"JB-{n}", f"TB-{n}")
    add(dashed_edges, f"TB-{n}", f"LCS-{n}")


# Lower 120 VAC / 125 VDC distribution.
for edge in [
    ("CB-301", "TR-120-A"),
    ("TR-120-A", "BUS-120AC-A"),
    ("CB-302", "TR-120-B"),
    ("TR-120-B", "BUS-120AC-B"),
    ("CHGR-125A", "BAT-125A"),
    ("BAT-125A", "BUS-125DC-A"),
    ("INV-120A", "BUS-125DC-A"),
    ("CHGR-125B", "BAT-125B"),
    ("BAT-125B", "BUS-125DC-B"),
    ("INV-120B", "BUS-125DC-B"),
]:
    add(solid_edges, *edge)

for edge in [
    ("BUS-120AC-A", "JB-MAIN"),
    ("INV-120A", "PN-RPS-A"),
    ("INV-120B", "PN-RPS-B"),
]:
    add(dashed_edges, *edge)

# These top-side feeds are routed through the unlabeled control/DC distribution frame.
# Included for Diego high-recall because the conductors visibly continue from the
# 480 V deck area into these devices, but the frame title itself is not used as a node.
for edge in [
    ("BUS-480-A", "CB-301"),
    ("BUS-480-A", "CHGR-125A"),
    ("BUS-480-B", "CB-302"),
    ("BUS-480-B", "CHGR-125B"),
]:
    add(uncertain_included_edges, *edge)


def write_matrix(nodes, edges):
    RESULTS.mkdir(parents=True, exist_ok=True)
    idx = {name: i for i, name in enumerate(nodes)}
    missing = sorted({x for edge in edges for x in edge if x not in idx})
    if missing:
        raise RuntimeError(f"Edges reference missing nodes: {missing}")
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b in edges:
        if a == b:
            raise RuntimeError(f"Self edge: {a}")
        ia = idx[a]
        ib = idx[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    with MATRIX_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for name, row in zip(nodes, matrix):
            writer.writerow([name] + row)
    return matrix


def describe_edges(title, edges):
    lines = [f"### {title}"]
    for a, b in edges:
        lines.append(f"- {a} -- {b}")
    return "\n".join(lines)


def write_notes(nodes, all_edges, matrix):
    edge_count = len({tuple(sorted(e)) for e in all_edges})
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    labels_identical = True
    notes = f"""# Diego Round 01 Connectivity Notes

## Scope and Inputs
- Used only doc 19 raw schematic and derived doc 19 artifacts under `Input resources` and `Codes and artifacts`.
- Matrix rows and columns are the same ordered node list; WN-* intermediate wire-node IDs are not included.
- Section/header text such as `DIVISION A SAFETY BUS AND LOAD GROUPS`, `480 V LOAD FEEDERS - SOLID POWER DROPS`, and `CONTROL POWER / DC DISTRIBUTION` is not included as a node.

## Node List Rationale
- Physical component nodes start from `component_labels_list.csv`, checked against the raw schematic crops.
- Feeder transformer labels shown in the CSV as `PT-201`, `PT-202`, etc. are corrected to the raw printed `CPT-*` labels: `CPT-201`, `CPT-202`, `CPT-203`, `CPT-204`, `CPT-301`, `CPT-302`, `CPT-401`, `CPT-402`, `CPT-501`, `CPT-502`, `CPT-601`, `CPT-701`.
- `PT-4160A` and `PT-4160B` are retained as PT labels because the top bus instruments are printed that way.
- Added visually printed logical buses: {", ".join(BUS_NODES)}.
- Added visually printed nodes missed by the CSV: `DS-F301`, `CB-F402`, and `LS-MOV601`.

## Evidence Summary
- Solid evidence means continuous solid conductor/power drop in the raw crop.
- Dashed evidence means visible dashed control/signal conductor in the raw crop.
- Uncertain included edges are in the matrix because Diego is high recall, but they depend on interpreting the unlabeled lower distribution frame as a continuation from the 480 V deck rather than as a separately named node.

{describe_edges("Top Switchgear and Bus Solid Edges", solid_edges[:26])}

### Repeated Feeder Evidence
- A-side feeders from `BUS-480-A`: 201, 203, 301, 401, 501, 601.
- B-side feeders from `BUS-480-B`: 202, 204, 302, 402, 502, 701.
- For each feeder, the solid chain is `BUS-480-* -- CB-Fxxx -- DS-Fxxx -- CPT-xxx -- MCC-xxx -- CB-Lxxx -- RELAY-Kxxx -- load`.
- For each feeder, dashed/control evidence includes `CB-Fxxx -- RELAY-PRxxx`, `MCC-xxx -- RELAY-Axxx`, load/instrument/JB/TB/LCS links.
- Load endpoints: pumps for 201/202/203/204/301/302/401/402, motors for 501/502, valve path for 601, and RPS instrument path for 701.

{describe_edges("Lower Control/DC Solid Edges", solid_edges[26 + 12 * 7:])}

{describe_edges("Dashed Control/Signal Edges", dashed_edges)}

{describe_edges("Uncertain Included Candidates", uncertain_included_edges)}

## Uncertain Candidates Kept Out
- Did not add `CONTROL POWER / DC DISTRIBUTION` as a row/column node because it reads as section/header text rather than a clear bus label.
- Did not connect `CHGR-125A` or `CHGR-125B` directly to the 120VAC buses: the vertical charger/battery conductors do not show clear connection dots at the 120VAC bus crossings.
- Did not add direct component-to-component clique edges along buses; logical `BUS-*` nodes represent those shared conductors.
- Did not add WN-* wire-node IDs or arbitrary intermediate bends/endpoints.

## Validation Summary
- Node count: {len(nodes)}
- Edge count: {edge_count}
- Symmetric: {symmetric}
- Diagonal zero: {diagonal_zero}
- Row/column labels identical: {labels_identical}
"""
    NOTES_OUT.write_text(notes, encoding="utf-8")


def main():
    nodes = load_nodes()
    all_edges = solid_edges + dashed_edges + uncertain_included_edges
    matrix = write_matrix(nodes, all_edges)
    write_notes(nodes, all_edges, matrix)
    print(f"wrote {MATRIX_OUT}")
    print(f"wrote {NOTES_OUT}")
    print(f"nodes={len(nodes)} edges={len({tuple(sorted(e)) for e in all_edges})}")


if __name__ == "__main__":
    main()
