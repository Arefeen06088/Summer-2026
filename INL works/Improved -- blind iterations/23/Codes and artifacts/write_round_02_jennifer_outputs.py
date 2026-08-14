import csv
import hashlib
import shutil
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\23")
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"
ROUND_01_JENNIFER_MATRIX = RESULT_DIR / "round_01_jennifer_matrix.csv"
ROUND_02_DIEGO_MATRIX = RESULT_DIR / "round_02_diego_matrix.csv"
ROUND_02_JENNIFER_MATRIX = RESULT_DIR / "round_02_jennifer_matrix.csv"
ROUND_02_JENNIFER_NOTES = RESULT_DIR / "round_02_jennifer_notes.md"


def read_bytes(path):
    return path.read_bytes()


def sha256(path):
    return hashlib.sha256(read_bytes(path)).hexdigest()


def validate_matrix(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))

    labels = rows[0][1:]
    body = rows[1:]
    errors = []
    if [row[0] for row in body] != labels:
        errors.append("row labels do not match column labels")

    edges = 0
    degrees = {label: 0 for label in labels}
    for i, row in enumerate(body):
        row_label = row[0]
        values = row[1:]
        if len(values) != len(labels):
            errors.append(f"row width mismatch for {row_label}")
            continue
        if values[i] != "0":
            errors.append(f"non-zero diagonal for {row_label}")
        for j, value in enumerate(values):
            if value not in {"0", "1"}:
                errors.append(f"bad matrix value at {row_label},{labels[j]}: {value}")
            if rows[j + 1][i + 1] != value:
                errors.append(f"asymmetry at {row_label},{labels[j]}")
            if j > i and value == "1":
                edges += 1
                degrees[row_label] += 1
                degrees[labels[j]] += 1

    return {
        "node_count": len(labels),
        "edge_count": edges,
        "row_column_labels_identical": [row[0] for row in body] == labels,
        "symmetric": not any(error.startswith("asymmetry") for error in errors),
        "diagonal_zero": not any(error.startswith("non-zero diagonal") for error in errors),
        "validation_errors": errors,
        "isolated_nodes": [label for label, degree in degrees.items() if degree == 0],
    }


def write_notes(validation, byte_identical, diego_hash):
    isolated = ", ".join(validation["isolated_nodes"]) if validation["isolated_nodes"] else "none"
    errors = ", ".join(validation["validation_errors"]) if validation["validation_errors"] else "none"
    text = f"""# Round 02 Jennifer Final Precision Confirmation Notes

Scope and evidence rules: I used only doc 23 input resources, doc 23 input-derived artifacts, and the round artifacts in the doc 23 Iteration_1 folder. I did not use ground truth, evaluator output, metric feedback, or anything derived from ground truth. Raw schematic evidence remains primary; overlays, crops, component labels, and round notes are aids.

## Saturation / Agreement Decision

Saturation/agreement was reached.

- Diego round 02 accepted Jennifer round 01 precision changes without further edits.
- `round_02_diego_matrix.csv` is byte-identical to `round_01_jennifer_matrix.csv`: {byte_identical}.
- Shared SHA-256 for the accepted matrix: `{diego_hash}`.
- I found no final visual or structural reason to restore any removed edge, remove any corrected edge, or change the node list.
- Jennifer round 02 matrix is intentionally written as the same accepted matrix.

## Node List Confirmation

Accepted unchanged: 200 nodes.

- 184 detected physical component nodes.
- One added raw-visible physical component: `DC-DC-1`.
- Fifteen printed bus nodes: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-ESF-A`, `BUS-4160-ESF-B`, `BUS-480-1A`, `BUS-480-1C`, `BUS-480-1B`, `BUS-480-2A`, `BUS-480-2C`, `BUS-480-2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`, `BUS-24DC-C`.
- No WN IDs, title/section text, voltage descriptions, unlabeled junctions, or extra text nodes were added.

## Remaining Uncertainty / Included Conservative Cases

- `BUS-480-2A -- CB-DC-A` and `BUS-480-2B -- CB-DC-B` remain included because the raw/full crops show continuous routed feeds from the respective 480 V buses down to the DC breakers.
- `BUS-125DC-A -- DC-DC-1` remains included as the visible upstream DC/DC input route; it is less visually strong than the converter output but still supported by the raw linework.
- `DC-DC-1 -- BUS-24DC-C`, `BUS-24DC-C -- BAT-24C`, and `BUS-24DC-C -- PNL-RADMON` remain included where the 24 VDC bus/output/taps are visible.
- Repeated 480 V local dashed/control edges retained only as direct visible endpoints: `PNL-* -- RELAY-K*1`, `JB-* -- RELAY-K*1`, and `RELAY-K*1 -- RELAY-K*2`.
- RPS/control dashed edges retained only where the adjacent visual endpoints are supported: relay-to-relay, second relay to annunciator, annunciator to recorder, recorder to RPS panel, RPS panel to NIS, RPS panel to DCS panel, and DCS panel to JB/control.

## Deliberately Excluded Cases

- 480 V `PNL-* -- JB-*` shortcuts remain excluded because the dashed panel drops are offset from the JB boxes and do not visibly terminate there.
- 480 V `JB-* -- RELAY-K*2` remains excluded because the local JB/control run terminates at the first relay, while the second relay sits on the relay-pair line.
- Direct RPS `PNL-RPS-* -- RELAY-KA/KB*` edges remain excluded because the relays are reached through the left dashed trunk rather than direct panel endpoints.
- Direct RPS `ANN-* -- PNL-RPS-*` edges remain excluded because the sequence recorder lies on the adjacent visual path before the RPS panel.
- `BUS-24DC-C -- JB-CTRL-A` remains excluded because `JB-CTRL-A` is on the lower dashed DCS/control run below the printed 24 VDC bus, with no visible 24 V bus tap.

## Validation Summary

- Node count: {validation["node_count"]}
- Undirected edge count: {validation["edge_count"]}
- Matrix shape/order: {validation["node_count"]} rows x {validation["node_count"]} columns; row and column labels identical: {validation["row_column_labels_identical"]}
- Symmetric: {validation["symmetric"]}
- Diagonal zero: {validation["diagonal_zero"]}
- Isolated nodes: {isolated}
- Validation errors: {errors}

Output files:

- `{ROUND_02_JENNIFER_MATRIX}`
- `{ROUND_02_JENNIFER_NOTES}`
"""
    ROUND_02_JENNIFER_NOTES.write_text(text, encoding="utf-8")


def main():
    if not ROUND_02_DIEGO_MATRIX.exists():
        raise FileNotFoundError(ROUND_02_DIEGO_MATRIX)
    if not ROUND_01_JENNIFER_MATRIX.exists():
        raise FileNotFoundError(ROUND_01_JENNIFER_MATRIX)

    byte_identical = read_bytes(ROUND_02_DIEGO_MATRIX) == read_bytes(ROUND_01_JENNIFER_MATRIX)
    validation = validate_matrix(ROUND_02_DIEGO_MATRIX)
    if validation["validation_errors"]:
        raise ValueError(validation["validation_errors"])

    shutil.copyfile(ROUND_02_DIEGO_MATRIX, ROUND_02_JENNIFER_MATRIX)
    write_notes(validation, byte_identical, sha256(ROUND_02_DIEGO_MATRIX))

    print(f"wrote {ROUND_02_JENNIFER_MATRIX}")
    print(f"wrote {ROUND_02_JENNIFER_NOTES}")
    print(
        f"nodes={validation['node_count']} edges={validation['edge_count']} "
        f"symmetric={validation['symmetric']} diagonal_zero={validation['diagonal_zero']} "
        f"isolated={len(validation['isolated_nodes'])} byte_identical={byte_identical}"
    )


if __name__ == "__main__":
    main()
