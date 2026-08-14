import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\20")
DIEGO_MATRIX = BASE / "Results" / "Iteration_1" / "round_01_diego_matrix.csv"
JENNIFER_MATRIX = BASE / "Results" / "Iteration_1" / "round_01_jennifer_matrix.csv"
JENNIFER_NOTES = BASE / "Results" / "Iteration_1" / "round_01_jennifer_notes.md"

ADDED_EDGES = [
    ("BUS-480-A", "RECT-125A"),
    ("BUS-480-C", "RECT-125B"),
]

REMOVED_EDGES = []


def load_matrix(path):
    with path.open(newline="") as f:
        rows = list(csv.reader(f))
    labels = rows[0][1:]
    matrix = {}
    for row in rows[1:]:
        matrix[row[0]] = {label: int(value) for label, value in zip(labels, row[1:])}
    return labels, matrix


def set_edge(matrix, a, b, value):
    matrix[a][b] = value
    matrix[b][a] = value


def edge_count(labels, matrix):
    return sum(
        matrix[labels[i]][labels[j]]
        for i in range(len(labels))
        for j in range(i + 1, len(labels))
    )


def validate(labels, matrix):
    rows_match = list(matrix.keys()) == labels
    symmetric = all(matrix[a][b] == matrix[b][a] for a in labels for b in labels)
    diagonal_zero = all(matrix[a][a] == 0 for a in labels)
    return rows_match, symmetric, diagonal_zero


def write_matrix(labels, matrix, path):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([""] + labels)
        for label in labels:
            writer.writerow([label] + [matrix[label][other] for other in labels])


def write_notes(labels, matrix, path):
    rows_match, symmetric, diagonal_zero = validate(labels, matrix)
    edge_total = edge_count(labels, matrix)
    added = ", ".join(f"`{a} - {b}`" for a, b in ADDED_EDGES)
    removed = "none"
    if REMOVED_EDGES:
        removed = ", ".join(f"`{a} - {b}`" for a, b in REMOVED_EDGES)

    text = f"""# Round 01 Jennifer Connectivity Notes

## Accepted Node Policy

- Kept Diego's 190 visually detected physical component labels and the 10 visually printed logical bus nodes: `BUS-13K-A`, `BUS-13K-B`, `BUS-416-A`, `BUS-416-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `BUS-125DCA`, and `BUS-125DCB`.
- Kept logical BUS-* nodes as bus representatives instead of expanding components sharing a bus into direct cliques.
- Did not add WN-* wire nodes, arbitrary intermediate junction dots, cable/boundary segments, or section titles such as AC/DC distribution headings.
- Node removals: none.
- Node additions: none.

## Accepted Edge Categories

- Accepted the solid single-line source, transformer, breaker, disconnect, tie, diesel-generator, and 480 V load-center paths where the conductor visibly terminates at each named component or bus.
- Accepted the repeated 480 V feeder branches as bus-to-breaker, breaker-to-disconnect, disconnect-to-MCC/JB, and MCC/JB-to-relay/control-switch/load chains.
- Accepted the dashed 125 VDC source chains from `BAT-125A - CHGR-125A - RECT-125A - BUS-125DCA` and `BAT-125B - CHGR-125B - RECT-125B - BUS-125DCB`; the dashed conductors visibly terminate at each source component and at the 125 VDC bus.
- Accepted the inverter taps `INV-UPS-A - BUS-125DCA` and `INV-UPS-B - BUS-125DCB`; each dashed vertical tap lands on the printed bus.
- Accepted the lower RPS and ESFAS control-panel drops and device chains where the dashed or solid line terminates at both named endpoints.
- Accepted the long A/B ESF interlock `RELAY-K106 - RELAY-K108`; the dashed run is labeled as the A/B ESF interlock and visually ties the K106 branch to the left side of K108, while not landing on K107.

## Refinements From Diego

- Added visually supported omitted AC-feed edges: {added}. `RECT-125A` has a solid upper feed from the 480 V load center A bus, and `RECT-125B` has the analogous solid upper feed from the 480 V load center C bus.
- Removed/rejected Diego candidates: {removed}. The reviewed high-recall dashed candidates were supported closely enough to keep.

## Uncertain Candidates Kept Out

- Did not add any unlabeled intermediate wire nodes, junction dots, dashed boundary-box contacts, or section-title nodes.
- Did not add direct component cliques across any printed bus; bus-tapped equipment remains connected through the corresponding BUS-* node.
- Did not add an ESF interlock edge to `RELAY-K107`; the visible interlock route terminates at the K108 side, not the K107 instrument branch.
- Did not add AC-side inverter source edges because no clear named upstream endpoint was visible for those inverter boxes beyond the 125 VDC bus tap.

## Validation Summary

- Node count: {len(labels)}
- Edge count: {edge_total}
- Matrix is symmetric: {'yes' if symmetric else 'no'}
- Matrix diagonal is zero: {'yes' if diagonal_zero else 'no'}
- Row and column labels are identical and in the same order: {'yes' if rows_match else 'no'}
"""
    path.write_text(text, encoding="utf-8")


def main():
    labels, matrix = load_matrix(DIEGO_MATRIX)

    for a, b in REMOVED_EDGES:
        set_edge(matrix, a, b, 0)
    for a, b in ADDED_EDGES:
        if a not in matrix or b not in matrix:
            raise KeyError(f"Missing node for edge {a} - {b}")
        set_edge(matrix, a, b, 1)

    for label in labels:
        matrix[label][label] = 0

    rows_match, symmetric, diagonal_zero = validate(labels, matrix)
    if not (rows_match and symmetric and diagonal_zero):
        raise RuntimeError(
            f"Validation failed rows_match={rows_match} symmetric={symmetric} diagonal_zero={diagonal_zero}"
        )

    write_matrix(labels, matrix, JENNIFER_MATRIX)
    write_notes(labels, matrix, JENNIFER_NOTES)
    print(f"wrote {JENNIFER_MATRIX}")
    print(f"wrote {JENNIFER_NOTES}")
    print(f"nodes={len(labels)} edges={edge_count(labels, matrix)}")


if __name__ == "__main__":
    main()
