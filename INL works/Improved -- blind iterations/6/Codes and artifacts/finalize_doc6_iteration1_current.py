import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\6")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"

COMPONENT_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"
FINAL_SOURCE_EDGES = RESULT_DIR / "round_02_jennifer_edges.csv"
FINAL_SOURCE_MATRIX = RESULT_DIR / "round_02_jennifer_matrix.csv"


def read_edges(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    edges = []
    seen = set()
    duplicates = []
    self_edges = []
    for row in rows:
        source = row["source"].strip()
        target = row["target"].strip()
        if source == target:
            self_edges.append((source, target))
        key = tuple(sorted((source, target)))
        if key in seen:
            duplicates.append(key)
        seen.add(key)
        edges.append(
            {
                "source": source,
                "target": target,
                "confidence": row.get("confidence", ""),
                "evidence": row.get("evidence", ""),
            }
        )
    return edges, duplicates, self_edges


def read_matrix(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        nodes = header[1:]
        matrix = []
        row_labels = []
        for row in reader:
            row_labels.append(row[0])
            matrix.append([int(value) for value in row[1:]])
    return nodes, row_labels, matrix


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["source", "target", "confidence", "evidence"]
        )
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path, nodes, matrix):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_nodes(path, nodes, edges):
    degrees = Counter()
    for edge in edges:
        degrees[edge["source"]] += 1
        degrees[edge["target"]] += 1

    component_rows = {}
    with COMPONENT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            label = row.get("normalized_label") or row.get("final_label")
            component_rows[label] = row

    explicit_buses = {
        "SWYD-BUS-A",
        "SWYD-BUS-B",
        "BUS-6KV-A",
        "BUS-6KV-B",
        "BUS-4KV-N",
    }
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "node",
            "node_class",
            "component_type",
            "stable_node_id",
            "degree",
            "bbox",
            "centroid",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            comp = component_rows.get(node, {})
            if node in explicit_buses:
                node_class = "explicit_bus"
                component_type = "bus"
            else:
                node_class = "component_or_ground"
                component_type = comp.get("component_type", "")
            writer.writerow(
                {
                    "node": node,
                    "node_class": node_class,
                    "component_type": component_type,
                    "stable_node_id": comp.get("stable_node_id", ""),
                    "degree": degrees[node],
                    "bbox": comp.get("bbox", ""),
                    "centroid": comp.get("centroid", ""),
                }
            )


def validate(nodes, row_labels, matrix, edges, duplicates, self_edges):
    edge_set = {tuple(sorted((edge["source"], edge["target"]))) for edge in edges}
    node_set = set(nodes)
    invalid_edge_nodes = sorted(
        {
            endpoint
            for edge in edges
            for endpoint in (edge["source"], edge["target"])
            if endpoint not in node_set
        }
    )
    symmetric = all(
        matrix[i][j] == matrix[j][i]
        for i in range(len(nodes))
        for j in range(len(nodes))
    )
    zero_diagonal = all(matrix[i][i] == 0 for i in range(len(nodes)))
    matrix_edge_count = sum(sum(row) for row in matrix) // 2
    edge_matrix_mismatches = []
    node_index = {node: idx for idx, node in enumerate(nodes)}
    for source, target in edge_set:
        if source in node_index and target in node_index:
            if matrix[node_index[source]][node_index[target]] != 1:
                edge_matrix_mismatches.append((source, target))
    matrix_edges = set()
    for i, source in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            if matrix[i][j]:
                matrix_edges.add(tuple(sorted((source, nodes[j]))))
    edges_missing_from_csv = sorted(matrix_edges - edge_set)
    return {
        "artifact": "final_connectivity_validation",
        "document": "Improved doc 6",
        "iteration": 1,
        "blind_scope_statement": (
            "Final files are copied from saturated Diego/Jennifer round outputs; "
            "extraction used Input resources and fresh input-derived artifacts only."
        ),
        "source_edges": str(FINAL_SOURCE_EDGES),
        "source_matrix": str(FINAL_SOURCE_MATRIX),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "matrix_edge_count": matrix_edge_count,
        "row_header_match": nodes == row_labels,
        "symmetric": symmetric,
        "zero_diagonal": zero_diagonal,
        "duplicate_edges": [list(item) for item in duplicates],
        "self_edges": [list(item) for item in self_edges],
        "invalid_edge_nodes": invalid_edge_nodes,
        "edge_matrix_mismatches": [list(item) for item in edge_matrix_mismatches],
        "edges_missing_from_csv": [list(item) for item in edges_missing_from_csv],
        "bus_6kv_n_present": "BUS-6KV-N" in node_set,
        "bus_4kv_n_present": "BUS-4KV-N" in node_set,
        "isolated_nodes": sorted(
            node
            for node in nodes
            if not any(node in (edge["source"], edge["target"]) for edge in edges)
        ),
    }


def write_summary(path, validation, edges):
    by_class = defaultdict(int)
    for edge in edges:
        evidence = edge["evidence"].lower()
        if "dotted" in evidence or "ground" in evidence:
            by_class["ground_bond_or_grounding"] += 1
        elif "dashed" in evidence or "sensing" in evidence or "control" in evidence:
            by_class["control_or_sensing"] += 1
        else:
            by_class["solid_power"] += 1
    lines = [
        "# Final Connectivity Summary - Improved doc 6 / Iteration_1",
        "",
        "Diego and Jennifer saturated after round 02. The final files are copied from Jennifer round 02.",
        "",
        f"- Nodes: {validation['node_count']}",
        f"- Edges: {validation['edge_count']}",
        f"- Matrix edge count: {validation['matrix_edge_count']}",
        f"- Symmetric: {validation['symmetric']}",
        f"- Zero diagonal: {validation['zero_diagonal']}",
        f"- `BUS-4KV-N` present: {validation['bus_4kv_n_present']}",
        f"- `BUS-6KV-N` present: {validation['bus_6kv_n_present']}",
        "",
        "Approximate retained edge classes from evidence text:",
    ]
    for key in ["solid_power", "control_or_sensing", "ground_bond_or_grounding"]:
        lines.append(f"- {key}: {by_class[key]}")
    lines.extend(
        [
            "",
            "No GT, scoring/evaluation files, or previous result archives were used for extraction.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    edges, duplicates, self_edges = read_edges(FINAL_SOURCE_EDGES)
    nodes, row_labels, matrix = read_matrix(FINAL_SOURCE_MATRIX)
    validation = validate(nodes, row_labels, matrix, edges, duplicates, self_edges)

    write_edges(RESULT_DIR / "final_connectivity_edges.csv", edges)
    write_edges(RESULT_DIR / "final_edges.csv", edges)
    write_matrix(RESULT_DIR / "final_connectivity_matrix.csv", nodes, matrix)
    write_matrix(RESULT_DIR / "connectivity_matrix.csv", nodes, matrix)
    write_nodes(RESULT_DIR / "final_connectivity_nodes.csv", nodes, edges)
    (RESULT_DIR / "final_connectivity_validation.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )
    write_summary(RESULT_DIR / "final_connectivity_summary.md", validation, edges)
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
