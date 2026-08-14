import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\39")
RESULTS = BASE / "Results" / "Iteration_1"
SOURCE_NODES = RESULTS / "round_02_jennifer_nodes.csv"
SOURCE_EDGES = RESULTS / "round_02_jennifer_edges.csv"
SOURCE_MATRIX = RESULTS / "round_02_jennifer_matrix.csv"

FINAL_MATRIX = RESULTS / "final_connectivity_matrix.csv"
ALT_MATRIX = RESULTS / "connectivity_matrix.csv"
FINAL_NODES = RESULTS / "final_connectivity_nodes.csv"
ALT_NODES = RESULTS / "final_nodes.csv"
FINAL_EDGES = RESULTS / "final_connectivity_edges.csv"
ALT_EDGES = RESULTS / "final_edges.csv"
FINAL_REVIEW = RESULTS / "final_edge_review.csv"
FINAL_SUMMARY = RESULTS / "final_connectivity_summary.md"
FINAL_VALIDATION = RESULTS / "final_connectivity_validation.json"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


nodes = read_csv(SOURCE_NODES)
edge_rows = read_csv(SOURCE_EDGES)
node_names = [row["node_name"] for row in nodes]
node_set = set(node_names)
keep_edges = [row for row in edge_rows if row["status"] == "keep"]
remove_edges = [row for row in edge_rows if row["status"] == "remove"]
uncertain_edges = [row for row in edge_rows if row["status"] == "uncertain"]

errors = []
if len(node_names) != len(node_set):
    errors.append("duplicate node names")
if any(name.startswith("WIRE-NODE-") for name in node_names):
    errors.append("WIRE-NODE final node present")
annotation_nodes = {
    "CONTROL-ROOM-ANNUNCIATION",
    "DIVISION-I-TRAIN-A-SAFETY-POWER",
    "DIVISION-II-TRAIN-B-SAFETY-POWER",
    "LC-A",
    "LC-B",
    "N-O-TIE",
    "NORMAL-OFFSITE-FEED-A",
    "NORMAL-OFFSITE-FEED-B",
}
if annotation_nodes & node_set:
    errors.append(f"annotation-only final node present: {sorted(annotation_nodes & node_set)}")

valid_statuses = {"keep", "remove", "uncertain"}
bad_statuses = sorted({row["status"] for row in edge_rows} - valid_statuses)
if bad_statuses:
    errors.append(f"bad status values: {bad_statuses}")

seen_keep = set()
for row in keep_edges:
    a = row["source"]
    b = row["target"]
    if a not in node_set or b not in node_set:
        errors.append(f"keep edge references missing node: {a}--{b}")
    if a == b:
        errors.append(f"self-loop keep edge: {a}")
    key = tuple(sorted((a, b)))
    if key in seen_keep:
        errors.append(f"duplicate keep edge: {a}--{b}")
    seen_keep.add(key)

index = {name: i for i, name in enumerate(node_names)}
matrix = [[0 for _ in node_names] for _ in node_names]
for row in keep_edges:
    a = row["source"]
    b = row["target"]
    if a in index and b in index:
        i = index[a]
        j = index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

with SOURCE_MATRIX.open(newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    source_matrix_rows = list(reader)

generated_matrix_rows = [["node_name"] + node_names]
generated_matrix_rows.extend(
    [[name] + [str(value) for value in matrix[i]] for i, name in enumerate(node_names)]
)

source_normalized = [[cell.strip() for cell in row] for row in source_matrix_rows]
if source_normalized != generated_matrix_rows:
    errors.append("generated matrix differs from round_02_jennifer_matrix.csv")

if any(matrix[i][i] != 0 for i in range(len(matrix))):
    errors.append("matrix diagonal is not zero")
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if matrix[i][j] != matrix[j][i]:
            errors.append(f"matrix asymmetry at {i},{j}")

if errors:
    raise SystemExit("Validation failed: " + "; ".join(errors))

shutil.copyfile(SOURCE_MATRIX, FINAL_MATRIX)
shutil.copyfile(SOURCE_MATRIX, ALT_MATRIX)
write_csv(
    FINAL_NODES,
    nodes,
    ["node_name", "node_type", "evidence", "change_vs_diego_r02"],
)
shutil.copyfile(FINAL_NODES, ALT_NODES)

keep_fieldnames = ["source", "target", "evidence"]
write_csv(
    FINAL_EDGES,
    [{field: row[field] for field in keep_fieldnames} for row in keep_edges],
    keep_fieldnames,
)
shutil.copyfile(FINAL_EDGES, ALT_EDGES)
write_csv(
    FINAL_REVIEW,
    edge_rows,
    ["source", "target", "evidence", "status", "change_vs_diego_r02"],
)

validation = {
    "family": "Improved",
    "document": 39,
    "iteration": 1,
    "selected_final_round": "round_02_jennifer",
    "saturation_reached": True,
    "node_count": len(nodes),
    "edge_row_count": len(edge_rows),
    "keep_edge_count": len(keep_edges),
    "remove_edge_count": len(remove_edges),
    "uncertain_edge_count": len(uncertain_edges),
    "matrix_shape": [len(node_names), len(node_names)],
    "checks": {
        "no_duplicate_node_names": True,
        "no_wire_node_nodes": True,
        "no_annotation_only_final_nodes": True,
        "all_status_values_valid": True,
        "keep_edges_reference_only_final_nodes": True,
        "no_duplicate_keep_edges": True,
        "matrix_matches_selected_round": True,
        "matrix_symmetric": True,
        "matrix_zero_diagonal": True,
    },
    "excluded_annotation_labels": sorted(annotation_nodes),
    "final_keep_edges": len(keep_edges),
    "created_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
}
FINAL_VALIDATION.write_text(json.dumps(validation, indent=2), encoding="utf-8")

summary = f"""# Final Connectivity Summary - Improved Doc 39 Iteration 1

Selected final round: `round_02_jennifer`

Saturation reached: yes. Jennifer R02 agreed with Diego R02 after a focused review of the only remaining disagreement.

Final counts:
- Nodes: {len(nodes)}
- Kept connectivity edges: {len(keep_edges)}
- Removed/non-final review edges: {len(remove_edges)}
- Uncertain edges: {len(uncertain_edges)}

Final node policy:
- Kept named physical components, explicit 4160/480 buses, and the visible plant ground.
- Excluded intermediate `WIRE-NODE-*` points.
- Excluded annotation-only labels: `LC-A`, `LC-B`, `CONTROL-ROOM-ANNUNCIATION`, division headings, normal offsite feed notes, and `N.O. TIE`.

Key final refinements:
- Charger feeds are modeled as `BUS-480-A -> CHG-125A` and `BUS-480-B -> CHG-125B`.
- `RPS-A -> JB-A101` and `RPS-B -> JB-B101` are kept after focused raw-image review of continuous dashed control conductors.
- `ANN-CR01 -> REC-SOE01` is kept as a direct dashed segment.
- `JB-A101 -> ANN-CR01`, `REC-SOE01 -> JB-B101`, and logical taps to `CONTROL-ROOM-ANNUNCIATION` are not kept.

Primary files:
- `final_connectivity_matrix.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_edge_review.csv`
- `final_connectivity_validation.json`
"""
FINAL_SUMMARY.write_text(summary, encoding="utf-8")

print(json.dumps(validation, indent=2))
