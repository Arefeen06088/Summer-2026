import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\21")
RESULTS = BASE / "Results" / "Iteration_1"
DIEGO_MATRIX = RESULTS / "round_01_diego_matrix.csv"
JENNIFER_MATRIX = RESULTS / "round_01_jennifer_matrix.csv"
JENNIFER_NOTES = RESULTS / "round_01_jennifer_notes.md"


REMOVALS = {
    tuple(sorted(edge)): reason
    for edge, reason in {
        ("BAT-EDG-A", "CP-EDG-A"): (
            "Removed: dashed BAT-EDG-A conductor drops to the lower control-ladder area; "
            "it does not visibly terminate at CP-EDG-A."
        ),
        ("BAT-EDG-B", "CP-EDG-B"): (
            "Removed: dashed BAT-EDG-B conductor drops to a lower ambiguous control path; "
            "it does not visibly terminate at CP-EDG-B."
        ),
        ("BAT-EDG-A", "BAT-EDG-B"): (
            "Removed: the two EDG battery dashed conductors are drawn as separate paths; "
            "no direct battery-to-battery junction is visible."
        ),
        ("BUS-501B", "CP-SI-A"): (
            "Removed: CP-SI-A row originates from the BUS-501A side; no B-rail junction dot is visible."
        ),
        ("BUS-501A", "CP-SI-B"): (
            "Removed: CP-SI-B row originates from the BUS-501B side; no A-rail junction dot is visible."
        ),
        ("BUS-501B", "CP-CCW-A"): (
            "Removed: CP-CCW-A dashed row starts at BUS-501A, not BUS-501B."
        ),
        ("BUS-501A", "CP-CCW-B"): (
            "Removed: CP-CCW-B dashed row starts at BUS-501B, not BUS-501A."
        ),
        ("BUS-501B", "CP-EDG-A"): (
            "Removed: CP-EDG-A dashed row starts at BUS-501A, not BUS-501B."
        ),
        ("BUS-501A", "CP-EDG-B"): (
            "Removed: CP-EDG-B dashed row starts at BUS-501B, not BUS-501A."
        ),
        ("BUS-501B", "RPS-A"): (
            "Removed: RPS-A dashed row starts at BUS-501A, not BUS-501B."
        ),
        ("BUS-501A", "RPS-B"): (
            "Removed: RPS-B dashed row starts at BUS-501B, not BUS-501A."
        ),
        ("BUS-501B", "ESFAS-A"): (
            "Removed: ESFAS-A dashed row starts at BUS-501A, not BUS-501B."
        ),
        ("BUS-501A", "ESFAS-B"): (
            "Removed: ESFAS-B dashed row starts at BUS-501B, not BUS-501A."
        ),
        ("BUS-501A", "CP-SWGR"): (
            "Removed: CP-SWGR is connected by visible control/interlock lines, but no direct BUS-501A rail tap is visible."
        ),
        ("BUS-501B", "CP-SWGR"): (
            "Removed: CP-SWGR is connected by visible control/interlock lines, but no direct BUS-501B rail tap is visible."
        ),
        ("BUS-501B", "CP-CRD"): (
            "Removed: CP-CRD lower dashed row is visible from the BUS-501A side; no B-rail tap is visible."
        ),
    }.items()
}


def load_matrix(path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    nodes = rows[0][1:]
    row_labels = [row[0] for row in rows[1:]]
    if row_labels != nodes:
        raise ValueError("Diego matrix row and column labels do not match")

    edges = set()
    matrix = []
    for i, row in enumerate(rows[1:]):
        vals = [int(v) for v in row[1:]]
        matrix.append(vals)
        for j, val in enumerate(vals):
            if j > i and val:
                edges.add(tuple(sorted((nodes[i], nodes[j]))))
    return nodes, edges, matrix


def build_matrix(nodes, edges):
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b in edges:
        ia, ib = index[a], index[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    return matrix


def validate(nodes, matrix):
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    edge_count = sum(sum(row) for row in matrix) // 2
    isolated = [node for i, node in enumerate(nodes) if sum(matrix[i]) == 0]
    return {
        "node_count": len(nodes),
        "edge_count": edge_count,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "isolated": isolated,
    }


def write_matrix(nodes, matrix, path):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_notes(nodes, diego_edges, reviewed_edges, validation):
    removed = sorted(diego_edges - reviewed_edges)
    added = sorted(reviewed_edges - diego_edges)

    lines = [
        "# Jennifer Round 01 Precision Review Notes",
        "",
        "## Scope",
        "- Reviewed only doc 21 input resources and doc 21 artifacts/results generated from those resources.",
        "- Did not use ground truth, evaluator output, metric feedback, or anything derived from ground truth.",
        "- Treated the raw schematic as primary evidence; overlays, component labels, wire masks, and crops were only aids.",
        "",
        "## Node List",
        "- Accepted Diego's node list unchanged.",
        "- Node set remains the 183 labels from `component_labels_list.csv`, the 14 printed bus nodes, plus raw-visible `CB-204A` and `DS-401B`.",
        "- `CB-204A` stays: the raw EDG-1B feeder visibly prints `CB-204A` between the BUS-201B tap and `DS-201B`.",
        "- `DS-401B` stays: the raw DC/UPS B-side chain visibly prints `DS-401B` before `TR-DC-B` and `RECT-125B`.",
        "",
        "## Edge Changes",
        f"- Removed {len(removed)} Diego edges.",
        f"- Added {len(added)} edges.",
        "- Changed rail treatment: ladder row starts were reduced to the single printed BUS-501 rail side that visibly feeds each row.",
        "",
        "### Removed Edges",
    ]

    for edge in removed:
        reason = REMOVALS.get(edge, "Removed during precision review.")
        a, b = edge
        lines.append(f"- `{a}` -- `{b}`: {reason}")

    lines.extend(
        [
            "",
            "### Added Edges",
        ]
    )
    if added:
        for a, b in added:
            lines.append(f"- `{a}` -- `{b}`")
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Retained Visual Support",
            "- Retained upper switchgear/EDG edges, including `CB-204A`, because the raw top-switchgear crops show direct bus taps and serial feeder components.",
            "- Retained 480 V transformer and MCC feeder/load edges; bus taps, breakers, MCC boxes, loads, and grounds are directly drawn.",
            "- Retained `GND-1`/`GND-2` only on BUS-301A/B and `GND-5`/`GND-6` only on MCC-3A/B, matching the visible ground symbols.",
            "- Retained DC/UPS chains for `DS-401A/B`, `DS-402A/B`, `INV-120C`, and `RECT-24C`; the raw schematic shows serial connections and direct bus outputs.",
            "- Retained row-wise ladder chains and the visible vertical/top interlock links; no all-to-all ladder clique was added.",
            "",
            "## Deliberately Excluded or Uncertain",
            "- Excluded all direct `BAT-EDG-A/B` links. The dashed EDG battery paths are visible, but their named termination is ambiguous and they do not visibly land on `CP-EDG-A/B` or on each other.",
            "- Excluded cross-rail ladder edges where a row only visibly starts from the opposite BUS-501 rail.",
            "- Excluded direct BUS-501 rail edges to `CP-SWGR`; it has visible control/interlock wiring but no clear printed rail tap.",
            "- Did not add a `BUS-501A` -- `BUS-501B` edge despite the lower dashed continuation shape, because the rails are printed as separate A/B buses and no explicit tie component is shown.",
            "",
            "## Validation Summary",
            f"- Node count: {validation['node_count']}",
            f"- Edge count: {validation['edge_count']}",
            f"- Symmetric: {validation['symmetric']}",
            f"- Diagonal zero: {validation['diagonal_zero']}",
            "- Row and column labels: identical and in the same order.",
            "- Isolated nodes: "
            + (", ".join(f"`{node}`" for node in validation["isolated"]) if validation["isolated"] else "None")
            + ".",
        ]
    )

    JENNIFER_NOTES.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    nodes, diego_edges, _ = load_matrix(DIEGO_MATRIX)
    missing = sorted(edge for edge in REMOVALS if edge not in diego_edges)
    if missing:
        raise ValueError(f"Removal edges not found in Diego matrix: {missing}")

    reviewed_edges = set(diego_edges)
    reviewed_edges.difference_update(REMOVALS)
    matrix = build_matrix(nodes, reviewed_edges)
    validation = validate(nodes, matrix)

    write_matrix(nodes, matrix, JENNIFER_MATRIX)
    write_notes(nodes, diego_edges, reviewed_edges, validation)

    print(f"wrote {JENNIFER_MATRIX}")
    print(f"wrote {JENNIFER_NOTES}")
    print(
        "nodes={node_count} edges={edge_count} symmetric={symmetric} "
        "diagonal_zero={diagonal_zero} isolated={isolated}".format(**validation)
    )


if __name__ == "__main__":
    main()
