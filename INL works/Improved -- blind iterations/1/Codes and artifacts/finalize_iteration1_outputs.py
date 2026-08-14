from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\1")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_1"

FINAL_MATRIX = RESULTS / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULTS / "final_edges.csv"
FINAL_NOTES = RESULTS / "final_notes.csv"
SUMMARY_JSON = RESULTS / "final_validation_summary.json"
ROUND_COMPARISON = RESULTS / "round_comparison_summary.csv"

EXPECTED_BUSES = {
    "BUS-4KV-A",
    "BUS-4KV-B",
    "BUS-4KV-C",
    "BUS-480-A",
    "BUS-480-B",
    "BUS-480-C",
    "BUS-125DC-A",
    "BUS-125DC-B",
    "BUS-120AC-A",
    "BUS-120AC-B",
}


def read_matrix(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError(f"empty matrix: {path}")
    header = rows[0][1:]
    names = []
    data = []
    for row in rows[1:]:
        if len(row) != len(header) + 1:
            raise ValueError(f"row width mismatch in {path}: {row[:3]}")
        names.append(row[0])
        data.append(row[1:])
    return header, names, data


def matrix_edges(header, names, data):
    if header != names:
        raise ValueError("matrix row and column names differ")
    edges = set()
    for i, src in enumerate(names):
        for j, dst in enumerate(header):
            value = data[i][j]
            if value not in {"0", "1"}:
                raise ValueError(f"non-binary value {value!r} at {src},{dst}")
            if i == j and value != "0":
                raise ValueError(f"non-zero diagonal at {src}")
            if data[j][i] != value:
                raise ValueError(f"asymmetry between {src} and {dst}")
            if value == "1" and i < j:
                edges.add(tuple(sorted((src, dst))))
    return edges


def read_edges(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def edge_set(rows):
    return {tuple(sorted((row["source"], row["target"]))) for row in rows}


def component_labels():
    with (INPUT / "component_visual_ocr_labels.csv").open(newline="", encoding="utf-8-sig") as f:
        return [row["normalized_text"] for row in csv.DictReader(f)]


def compare_round(prefix: str):
    matrix_path = RESULTS / f"{prefix}_matrix.csv"
    edge_path = RESULTS / f"{prefix}_edges.csv"
    if not matrix_path.exists() or not edge_path.exists():
        return None
    header, names, data = read_matrix(matrix_path)
    m_edges = matrix_edges(header, names, data)
    e_rows = read_edges(edge_path)
    e_edges = edge_set(e_rows)
    return {
        "round": prefix,
        "nodes": len(names),
        "matrix_edges": len(m_edges),
        "edge_csv_edges": len(e_edges),
        "matrix_edge_csv_match": m_edges == e_edges,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-prefix", default="round_02_jennifer")
    args = parser.parse_args()

    round_matrix = RESULTS / f"{args.source_prefix}_matrix.csv"
    round_edges = RESULTS / f"{args.source_prefix}_edges.csv"
    round_notes = RESULTS / f"{args.source_prefix}_notes.csv"
    for path in (round_matrix, round_edges, round_notes):
        if not path.exists():
            raise FileNotFoundError(path)

    shutil.copy2(round_matrix, FINAL_MATRIX)
    shutil.copy2(round_edges, FINAL_EDGES)
    shutil.copy2(round_notes, FINAL_NOTES)

    header, names, data = read_matrix(FINAL_MATRIX)
    m_edges = matrix_edges(header, names, data)
    e_rows = read_edges(FINAL_EDGES)
    e_edges = edge_set(e_rows)
    if m_edges != e_edges:
        raise ValueError("final matrix and edge CSV disagree")

    labels = component_labels()
    label_set = set(labels)
    node_set = set(names)
    physical_missing = sorted(label_set - node_set)
    extra_nodes = sorted(node_set - label_set)

    prefixes = [
        "round_01_diego",
        "round_01_jennifer",
        "round_02_diego",
        "round_02_jennifer",
        "round_03_diego",
        "round_03_jennifer",
    ]
    summaries = [summary for prefix in prefixes if (summary := compare_round(prefix))]
    if summaries:
        with ROUND_COMPARISON.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
            writer.writeheader()
            writer.writerows(summaries)

    summary = {
        "iteration": 1,
        "document_folder": str(BASE),
        "final_source_round": args.source_prefix,
        "nodes": len(names),
        "edges": len(m_edges),
        "physical_components_in_input": len(labels),
        "physical_components_in_final": len(label_set & node_set),
        "physical_missing": physical_missing,
        "expected_buses_present": sorted(EXPECTED_BUSES & node_set),
        "expected_buses_missing": sorted(EXPECTED_BUSES - node_set),
        "logical_or_nonphysical_nodes": extra_nodes,
        "ground_like_nodes": sorted(n for n in node_set if "GND" in n or "GROUND" in n or "GRD" in n),
        "matrix_is_symmetric_binary_zero_diagonal": True,
        "matrix_edge_csv_match": True,
        "notes": [
            "All physical normalized_text labels should remain represented as rows.",
            "Intermediate anonymous wire-node points are intentionally excluded.",
            "Only visually named bus bars are retained as logical nodes.",
            "No ground node is included unless visible in the final source round.",
            "Remaining uncertainty is documented in final_notes.csv.",
        ],
    }
    with SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
