import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\21")
RESULTS = BASE / "Results" / "Iteration_1"
DIEGO_R02_MATRIX = RESULTS / "round_02_diego_matrix.csv"
JENNIFER_R01_MATRIX = RESULTS / "round_01_jennifer_matrix.csv"
JENNIFER_R02_MATRIX = RESULTS / "round_02_jennifer_matrix.csv"
JENNIFER_R02_NOTES = RESULTS / "round_02_jennifer_notes.md"


def read_edges_and_matrix(path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    nodes = rows[0][1:]
    row_labels = [row[0] for row in rows[1:]]
    matrix = [[int(v) for v in row[1:]] for row in rows[1:]]
    edges = set()
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if j > i and value:
                edges.add(tuple(sorted((nodes[i], nodes[j]))))
    return nodes, row_labels, matrix, edges


def validate(path):
    nodes, row_labels, matrix, edges = read_edges_and_matrix(path)
    square = len(matrix) == len(nodes) and all(len(row) == len(nodes) for row in matrix)
    symmetric = square and all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = square and all(matrix[i][i] == 0 for i in range(len(nodes)))
    isolated = [node for i, node in enumerate(nodes) if sum(matrix[i]) == 0]
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "labels_identical": nodes == row_labels,
        "square": square,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "isolated": isolated,
    }


def main():
    if DIEGO_R02_MATRIX.read_bytes() != JENNIFER_R01_MATRIX.read_bytes():
        raise ValueError("Diego round 02 matrix is not byte-identical to Jennifer round 01 matrix")

    JENNIFER_R02_MATRIX.write_bytes(DIEGO_R02_MATRIX.read_bytes())
    result = validate(JENNIFER_R02_MATRIX)

    notes = f"""# Jennifer Round 02 Final Precision Confirmation Notes

## Scope
- Final confirmation used only doc 21 `Input resources`, doc 21 `Codes and artifacts`, and doc 21 iteration results generated from those resources.
- No ground truth, evaluator output, metric feedback, or derived GT material was used.
- Raw schematic remains primary evidence; component/OCR lists, wire masks, wire nodes, and inspection crops were treated only as aids.

## Saturation / Agreement
- Saturation/agreement reached.
- Diego round 02 accepted all 16 Jennifer round 01 precision removals and added no edges back.
- `round_02_diego_matrix.csv` is byte-identical to `round_01_jennifer_matrix.csv`; Jennifer round 02 therefore writes the same final matrix.
- I found no additional visually supported precision issue requiring a final adjustment.

## Final Node / Edge Stance
- Node list unchanged from the agreed round 01 review: 199 nodes.
- `CB-204A` remains included because it is visibly printed on the EDG-1B feeder.
- `DS-401B` remains included because it is visibly printed in the DC/UPS B-side chain.
- Control ladder rows remain row-wise only; opposite-rail overconnections remain removed.
- EDG battery direct links remain excluded because the dashed terminations are ambiguous.

## Remaining Uncertainty
- `BAT-EDG-A` and `BAT-EDG-B` are visible labels, but their dashed routing does not support a named component-to-component edge with enough precision. They remain isolated rather than guessed.
- No explicit `BUS-501A` -- `BUS-501B` tie is included; the rails are printed as separate buses.
- `CP-SWGR` rail-feed ambiguity remains excluded; visible interlock/control lines are retained only where supported by the agreed matrix.

## Validation Summary
- Node count: {result["node_count"]}
- Edge count: {result["edge_count"]}
- Row/column labels identical: {result["labels_identical"]}
- Matrix square: {result["square"]}
- Symmetric: {result["symmetric"]}
- Diagonal zero: {result["diagonal_zero"]}
- Isolated nodes: {", ".join(f"`{node}`" for node in result["isolated"]) if result["isolated"] else "None"}.
"""
    JENNIFER_R02_NOTES.write_text(notes, encoding="utf-8")

    print(f"wrote {JENNIFER_R02_MATRIX}")
    print(f"wrote {JENNIFER_R02_NOTES}")
    print(
        "nodes={node_count} edges={edge_count} labels_identical={labels_identical} "
        "square={square} symmetric={symmetric} diagonal_zero={diagonal_zero} isolated={isolated}".format(**result)
    )


if __name__ == "__main__":
    main()
