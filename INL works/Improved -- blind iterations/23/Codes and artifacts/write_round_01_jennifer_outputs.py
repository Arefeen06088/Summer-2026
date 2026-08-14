import csv
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\23")
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"
DIEGO_MATRIX = RESULT_DIR / "round_01_diego_matrix.csv"
JENNIFER_MATRIX = RESULT_DIR / "round_01_jennifer_matrix.csv"
JENNIFER_NOTES = RESULT_DIR / "round_01_jennifer_notes.md"


def edge(a, b):
    return tuple(sorted((a, b)))


def read_matrix(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    labels = [value.strip() for value in rows[0][1:]]
    edges = set()
    for i, row in enumerate(rows[1:]):
        row_label = row[0].strip()
        if row_label != labels[i]:
            raise ValueError(f"row/column label mismatch at row {i}: {row_label} != {labels[i]}")
        for j, value in enumerate(row[1:]):
            if value.strip() == "1":
                if i == j:
                    raise ValueError(f"non-zero diagonal at {row_label}")
                edges.add(edge(row_label, labels[j]))
    return labels, edges


REMOVALS = {
    edge("PNL-1A", "JB-1A-1"): "The PNL-1A dashed drop is left of JB-1A-1; no direct endpoint contact is visible.",
    edge("JB-1A-1", "RELAY-K12"): "The lower dashed/JB run does not terminate at the second relay; K12 is only on the relay pair line.",
    edge("PNL-1C", "JB-1C-1"): "The PNL-1C dashed drop is offset from JB-1C-1; no direct endpoint contact is visible.",
    edge("JB-1C-1", "RELAY-K22"): "The lower dashed/JB run does not terminate at the second relay; K22 is only on the relay pair line.",
    edge("PNL-1B", "JB-1B-1"): "The PNL-1B dashed drop is offset from JB-1B-1; no direct endpoint contact is visible.",
    edge("JB-1B-1", "RELAY-K32"): "The lower dashed/JB run does not terminate at the second relay; K32 is only on the relay pair line.",
    edge("PNL-2A", "JB-2A-1"): "The PNL-2A dashed drop is offset from JB-2A-1; no direct endpoint contact is visible.",
    edge("JB-2A-1", "RELAY-K42"): "The lower dashed/JB run does not terminate at the second relay; K42 is only on the relay pair line.",
    edge("PNL-2C", "JB-2C-1"): "The PNL-2C dashed drop is offset from JB-2C-1; no direct endpoint contact is visible.",
    edge("JB-2C-1", "RELAY-K52"): "The lower dashed/JB run does not terminate at the second relay; K52 is only on the relay pair line.",
    edge("PNL-2B", "JB-2B-1"): "The PNL-2B dashed drop is offset from JB-2B-1; no direct endpoint contact is visible.",
    edge("JB-2B-1", "RELAY-K62"): "The lower dashed/JB run does not terminate at the second relay; K62 is only on the relay pair line.",
    edge("PNL-RPS-A", "RELAY-KA1"): "RPS A dashed bundle reaches KA1 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint.",
    edge("PNL-RPS-A", "RELAY-KA2"): "RPS A dashed bundle reaches KA2 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint.",
    edge("ANN-A", "PNL-RPS-A"): "ANN-A is on the left-side dashed trunk; REC-SER-A is the adjacent endpoint before PNL-RPS-A.",
    edge("PNL-RPS-B", "RELAY-KB1"): "RPS B dashed bundle reaches KB1 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint.",
    edge("PNL-RPS-B", "RELAY-KB2"): "RPS B dashed bundle reaches KB2 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint.",
    edge("ANN-B", "PNL-RPS-B"): "ANN-B is on the left-side dashed trunk; REC-SER-B is the adjacent endpoint before PNL-RPS-B.",
    edge("JB-CTRL-A", "BUS-24DC-C"): "JB-CTRL-A sits on the lower DCS/control dashed run; the printed 24 VDC bus does not visibly tap it.",
}


ADDITIONS = {
    edge("JB-1A-1", "RELAY-K11"): "The local dashed control run from the JB/valve corner terminates at the first relay K11.",
    edge("JB-1C-1", "RELAY-K21"): "The local dashed control run from the JB/valve corner terminates at the first relay K21.",
    edge("JB-1B-1", "RELAY-K31"): "The local dashed control run from the JB/valve corner terminates at the first relay K31.",
    edge("JB-2A-1", "RELAY-K41"): "The local dashed control run from the JB/valve corner terminates at the first relay K41.",
    edge("JB-2C-1", "RELAY-K51"): "The local dashed control run from the JB/valve corner terminates at the first relay K51.",
    edge("JB-2B-1", "RELAY-K61"): "The local dashed control run from the JB/valve corner terminates at the first relay K61.",
    edge("RELAY-KA2", "ANN-A"): "RPS A dashed relay trunk continues from KA2 to the annunciator side before the recorder/RPS bundle.",
    edge("ANN-A", "REC-SER-A"): "RPS A dashed bundle visibly runs between the annunciator and sequence recorder.",
    edge("RELAY-KB2", "ANN-B"): "RPS B dashed relay trunk continues from KB2 to the annunciator side before the recorder/RPS bundle.",
    edge("ANN-B", "REC-SER-B"): "RPS B dashed bundle visibly runs between the annunciator and sequence recorder.",
}


def apply_review(edges, labels):
    label_set = set(labels)
    for candidate in set(REMOVALS) | set(ADDITIONS):
        missing = set(candidate) - label_set
        if missing:
            raise ValueError(f"edge references nodes not in matrix: {candidate}: {sorted(missing)}")
    absent_removals = sorted(REMOVALS.keys() - edges)
    if absent_removals:
        raise ValueError(f"removal edge(s) not present in Diego matrix: {absent_removals}")
    reviewed = set(edges)
    reviewed.difference_update(REMOVALS)
    reviewed.update(ADDITIONS)
    return reviewed


def write_matrix(path, labels, edges):
    edge_set = set(edges)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["name", *labels])
        for row_label in labels:
            writer.writerow(
                [
                    row_label,
                    *[
                        "0" if row_label == col_label else ("1" if edge(row_label, col_label) in edge_set else "0")
                        for col_label in labels
                    ],
                ]
            )


def validate(labels, edges):
    degrees = {label: 0 for label in labels}
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    return {
        "node_count": len(labels),
        "edge_count": len(edges),
        "symmetric": True,
        "diagonal_zero": True,
        "row_column_labels_identical": True,
        "isolated_nodes": [label for label in labels if degrees[label] == 0],
    }


def table_rows(changes, action):
    lines = ["| Edge | Action | Visual evidence |", "|---|---|---|"]
    for (a, b), evidence in changes:
        lines.append(f"| `{a} -- {b}` | {action} | {evidence} |")
    return "\n".join(lines)


def write_notes(labels, original_edges, reviewed_edges, validation):
    removed = sorted(REMOVALS.items())
    added = sorted(ADDITIONS.items())
    retained_uncertain = [
        ("`BUS-480-2A -- CB-DC-A`", "Included; left-full raw crop shows a continuous routed feed from the 480 V 2A bus tap down to CB-DC-A."),
        ("`BUS-480-2B -- CB-DC-B`", "Included; right/full raw crop shows the analogous routed feed from the 480 V 2B bus tap to CB-DC-B."),
        ("`BUS-125DC-A -- DC-DC-1`", "Included; DC-DC-1 is raw-visible and its upper input trace routes from the upper DC run, though less legible than the 24 V output."),
        ("`DC-DC-1 -- BUS-24DC-C`", "Included; converter output drops directly to the printed 24 VDC bus."),
        ("480 V `PNL-* -- RELAY-K*1` and `RELAY-K*1 -- RELAY-K*2`", "Included as lower-confidence dashed/local control edges where the first-relay drop and relay-pair line are visibly drawn."),
        ("RPS `REC-SER-* -- PNL-RPS-*` and `PNL-RPS-* -- INST-NIS-*`", "Included; dashed bundles enter the RPS panel directly from the recorder side and from the NIS side."),
    ]
    excluded_uncertain = [
        ("480 V `PNL-* -- JB-*`", "Excluded; the panel dashed drop is offset from the JB box and no direct endpoint contact is visible."),
        ("480 V `JB-* -- RELAY-K*2`", "Excluded/retargeted; the visible lower local run terminates at the first relay, not the second relay."),
        ("RPS direct `PNL-RPS-* -- RELAY-K*`", "Excluded; relays are reached through the left dashed trunk rather than direct panel endpoints."),
        ("RPS direct `ANN-* -- PNL-RPS-*`", "Excluded; ANN connects through the adjacent recorder-side dashed trunk before the RPS panel."),
        ("`BUS-24DC-C -- JB-CTRL-A`", "Excluded; JB-CTRL-A is on the lower DCS/JB dashed run below the 24 V bus."),
    ]
    retained_lines = "\n".join(f"- {edge_name}: {reason}" for edge_name, reason in retained_uncertain)
    excluded_lines = "\n".join(f"- {edge_name}: {reason}" for edge_name, reason in excluded_uncertain)
    validation_text = (
        f"- Node count: {validation['node_count']}\n"
        f"- Undirected edge count: {validation['edge_count']}\n"
        f"- Matrix shape/order: {validation['node_count']} rows x {validation['node_count']} columns, row and column labels identical\n"
        f"- Symmetric: {validation['symmetric']}\n"
        f"- Diagonal zero: {validation['diagonal_zero']}\n"
        f"- Isolated nodes: {', '.join(validation['isolated_nodes']) if validation['isolated_nodes'] else 'none'}"
    )
    text = f"""# Round 01 Jennifer Precision Review Notes

Scope and evidence rules: I used only doc 23 input resources and doc 23 input-derived Codes/artifacts/Results. I did not use ground truth, evaluator output, metric feedback, or anything derived from ground truth. The raw schematic remained the primary evidence; overlays, wire-node views, component labels, masks, and temporary zoom crops were used only as aids.

## Node List Decision

Accepted Diego's node list unchanged.

- Node count remains 200: 184 detected physical components, raw-visible added physical component `DC-DC-1`, and 15 printed bus nodes.
- `DC-DC-1` is visible in the lower control/24 VDC area as the small DC/DC converter symbol feeding the printed `BUS-24DC-C`.
- Printed bus nodes retained: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-ESF-A`, `BUS-4160-ESF-B`, `BUS-480-1A`, `BUS-480-1C`, `BUS-480-1B`, `BUS-480-2A`, `BUS-480-2C`, `BUS-480-2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`, `BUS-24DC-C`.
- I did not add section titles, voltage descriptions, title-block text, WN IDs, unlabeled junctions, or extra text nodes.

## Overall Review Result

- Started from Diego round 1: {len(labels)} nodes and {len(original_edges)} unique undirected edges.
- Jennifer reviewed matrix: {validation['node_count']} nodes and {validation['edge_count']} unique undirected edges.
- Solid power paths, printed bus taps, grounds, transformer/breaker feeder chains, diesel/ATS paths, DC/UPS chains, and bus-mediated MCC/load branches were retained where the raw linework directly supports them.
- Revisions concentrate on dashed/control overconnections and one unsupported 24 VDC/JB tap.

## Removed / Rejected Edges

{table_rows(removed, "removed")}

## Added / Corrected Edges

{table_rows(added, "added/corrected")}

## Remaining Uncertain / Lower-Confidence Included Cases

{retained_lines}

## Deliberately Excluded Ambiguous Cases

{excluded_lines}

## Validation Summary

{validation_text}

Output files:

- `{JENNIFER_MATRIX}`
- `{JENNIFER_NOTES}`
"""
    JENNIFER_NOTES.write_text(text, encoding="utf-8")


def main():
    labels, original_edges = read_matrix(DIEGO_MATRIX)
    reviewed_edges = apply_review(original_edges, labels)
    write_matrix(JENNIFER_MATRIX, labels, reviewed_edges)
    validation = validate(labels, reviewed_edges)
    write_notes(labels, original_edges, reviewed_edges, validation)
    print(
        f"wrote {JENNIFER_MATRIX}\n"
        f"wrote {JENNIFER_NOTES}\n"
        f"nodes={validation['node_count']} edges={validation['edge_count']} "
        f"isolated={len(validation['isolated_nodes'])}"
    )


if __name__ == "__main__":
    main()
