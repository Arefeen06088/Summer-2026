import csv
from pathlib import Path

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\19")
RESULTS = BASE / "Results" / "Iteration_1"

DIEGO_MATRIX = RESULTS / "round_01_diego_matrix.csv"
JENNIFER_MATRIX = RESULTS / "round_01_jennifer_matrix.csv"
JENNIFER_NOTES = RESULTS / "round_01_jennifer_notes.md"

REMOVED_EDGES = {
    tuple(sorted(edge))
    for edge in [
        ("BUS-480-A", "CB-301"),
        ("BUS-480-A", "CHGR-125A"),
        ("BUS-480-B", "CB-302"),
        ("BUS-480-B", "CHGR-125B"),
    ]
}


def read_matrix(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    labels = rows[0][1:]
    data = {}
    for row in rows[1:]:
        data[row[0]] = {label: int(value) for label, value in zip(labels, row[1:])}
    return labels, data


def edge_count(labels, data):
    total = 0
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            total += data[a][b]
    return total


def validate(labels, data):
    symmetric = all(data[a][b] == data[b][a] for a in labels for b in labels)
    diagonal_zero = all(data[a][a] == 0 for a in labels)
    return symmetric, diagonal_zero


def write_matrix(labels, data, path):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + labels)
        for label in labels:
            writer.writerow([label] + [data[label][other] for other in labels])


def main():
    labels, data = read_matrix(DIEGO_MATRIX)

    for a, b in REMOVED_EDGES:
        if a not in data or b not in data[a]:
            raise ValueError(f"Missing edge endpoint in Diego matrix: {a}, {b}")
        data[a][b] = 0
        data[b][a] = 0

    symmetric, diagonal_zero = validate(labels, data)
    if not symmetric or not diagonal_zero:
        raise ValueError("Jennifer matrix failed validation")

    write_matrix(labels, data, JENNIFER_MATRIX)

    count = edge_count(labels, data)
    notes = f"""# Jennifer Round 01 Precision Review Notes

## Scope
- Reviewed Diego round 01 using only doc 19 input resources and doc 19 derived inspection artifacts.
- Did not use any GT, evaluator output, metric feedback, or folders outside doc 19 Input resources / doc 19 Codes and artifacts.
- Jennifer inspection crops were generated under `Codes and artifacts/jennifer_round01_crops` from the permitted raw schematic and overlays.

## Accepted Node List Policy
- Kept real physical components and the visually printed logical buses.
- Kept printed logical buses: `BUS-4160-A`, `BUS-4160-B`, `BUS-480-A`, `BUS-480-B`, `BUS-120AC-A`, `BUS-120AC-B`, `BUS-125DC-A`, `BUS-125DC-B`.
- Kept Diego's raw-label corrections from feeder `PT-*` OCR to printed `CPT-*`: `CPT-201`, `CPT-202`, `CPT-203`, `CPT-204`, `CPT-301`, `CPT-302`, `CPT-401`, `CPT-402`, `CPT-501`, `CPT-502`, `CPT-601`, `CPT-701`.
- Kept `PT-4160A` and `PT-4160B` as PT labels because the top bus instruments are printed that way.
- Kept Diego-added nodes `DS-F301`, `CB-F402`, and `LS-MOV601`; all are visible in the raw schematic and connected to the associated feeder/control paths.
- Removed no nodes in this precision round.
- Continued to exclude `WN-*`, arbitrary bend/intermediate points, and section/header text such as `CONTROL POWER / DC DISTRIBUTION`.

## Accepted Edge Categories
- Kept solid source/switchgear edges where a continuous conductor or bus connection dot is visible.
- Kept feeder solid chains from the 480 V buses through `CB-Fxxx`, `DS-Fxxx`, `CPT-xxx`, `MCC-xxx`, `CB-Lxxx`, `RELAY-Kxxx`, and the load endpoints.
- Kept dashed control/signal edges where the dashed line visibly terminates at the two named components without a crossing/gap ambiguity.
- Kept lower control/DC internal edges with clear printed conductors: `CB-301 -- TR-120-A`, `TR-120-A -- BUS-120AC-A`, `CB-302 -- TR-120-B`, `TR-120-B -- BUS-120AC-B`, charger-to-battery paths, battery/inverter-to-DC-bus paths, `INV-120A -- PN-RPS-A`, `INV-120B -- PN-RPS-B`, and `BUS-120AC-A -- JB-MAIN`.

## Removed / Rejected Candidates
- Removed `BUS-480-A -- CB-301`: the lower frame shows a local solid feed line to `CB-301`, but it is not printed as `BUS-480-A` and the raw crop does not show an unambiguous continuous connection from the 480-A bus to that lower-frame line.
- Removed `BUS-480-A -- CHGR-125A`: same issue; `CHGR-125A` ties to the lower-frame feed line, not to a clearly printed or traced `BUS-480-A` node.
- Removed `BUS-480-B -- CB-302`: the lower frame feed is visible, but assigning it to `BUS-480-B` is not visually certain.
- Removed `BUS-480-B -- CHGR-125B`: same issue; no clear printed `BUS-480-B` identity for the lower-frame feed conductor.

## Uncertain Candidates Kept Out
- Kept out all four lower BUS-480 candidates listed above rather than guessing.
- Did not add a `CONTROL POWER / DC DISTRIBUTION` node because it is section/header text, not a printed logical bus node.
- Did not add direct component cliques across the unlabeled lower-frame feed line; no arbitrary bus/intermediate node was introduced.
- Did not connect `CHGR-125A` or `CHGR-125B` directly to the 120VAC buses at visual crossings without junction dots.

## Validation Summary
- Node count: {len(labels)}
- Edge count: {count}
- Symmetric: {symmetric}
- Diagonal zero: {diagonal_zero}
- Row/column labels identical: True
"""
    JENNIFER_NOTES.write_text(notes, encoding="utf-8")
    print(f"wrote {JENNIFER_MATRIX}")
    print(f"wrote {JENNIFER_NOTES}")
    print(f"nodes={len(labels)} edges={count} symmetric={symmetric} diagonal_zero={diagonal_zero}")


if __name__ == "__main__":
    main()
