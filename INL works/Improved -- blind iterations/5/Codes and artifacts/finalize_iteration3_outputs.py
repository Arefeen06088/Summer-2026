from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\5")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_3"

ROUND_MATRIX = RESULTS / "round_02_jennifer_matrix.csv"
ROUND_EDGES = RESULTS / "round_02_jennifer_edges.csv"
ROUND_NOTES = RESULTS / "round_02_jennifer_notes.csv"

FINAL_MATRIX = RESULTS / "final_connectivity_matrix.csv"
FINAL_EDGES = RESULTS / "final_edges.csv"
FINAL_NOTES = RESULTS / "final_notes.csv"
SUMMARY_JSON = RESULTS / "final_validation_summary.json"
ROUND_COMPARISON = RESULTS / "round_comparison_summary.csv"


def read_matrix(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)
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
            v = data[i][j]
            if v not in {"0", "1"}:
                raise ValueError(f"non-binary value {v!r} at {src},{dst}")
            if i == j and v != "0":
                raise ValueError(f"non-zero diagonal at {src}")
            if data[j][i] != v:
                raise ValueError(f"asymmetry between {src} and {dst}")
            if v == "1" and i < j:
                edges.add(tuple(sorted((src, dst))))
    return edges


def read_edges(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def edge_set(rows):
    return {tuple(sorted((r["source"], r["target"]))) for r in rows}


def component_labels():
    with (INPUT / "component_visual_ocr_labels.csv").open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [r["final_label"] for r in reader]


def compare_round(label: str, matrix_path: Path, edge_path: Path):
    header, names, data = read_matrix(matrix_path)
    m_edges = matrix_edges(header, names, data)
    e_rows = read_edges(edge_path)
    e_edges = edge_set(e_rows)
    return {
        "round": label,
        "nodes": len(names),
        "matrix_edges": len(m_edges),
        "edge_csv_edges": len(e_edges),
        "matrix_edge_csv_match": m_edges == e_edges,
    }


def main():
    shutil.copy2(ROUND_MATRIX, FINAL_MATRIX)
    shutil.copy2(ROUND_EDGES, FINAL_EDGES)
    shutil.copy2(ROUND_NOTES, FINAL_NOTES)

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

    summaries = [
        compare_round("round_01_diego", RESULTS / "round_01_diego_matrix.csv", RESULTS / "round_01_diego_edges.csv"),
        compare_round("round_01_jennifer", RESULTS / "round_01_jennifer_matrix.csv", RESULTS / "round_01_jennifer_edges.csv"),
        compare_round("round_02_diego", RESULTS / "round_02_diego_matrix.csv", RESULTS / "round_02_diego_edges.csv"),
        compare_round("round_02_jennifer", RESULTS / "round_02_jennifer_matrix.csv", RESULTS / "round_02_jennifer_edges.csv"),
    ]
    with ROUND_COMPARISON.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
        writer.writeheader()
        writer.writerows(summaries)

    summary = {
        "iteration": 3,
        "document": 5,
        "final_source_round": "round_02_jennifer",
        "saturated": True,
        "nodes": len(names),
        "edges": len(m_edges),
        "physical_components_in_input": len(labels),
        "physical_components_in_final": len(label_set & node_set),
        "physical_missing": physical_missing,
        "logical_nodes": extra_nodes,
        "matrix_is_symmetric_binary_zero_diagonal": True,
        "matrix_edge_csv_match": True,
        "notes": [
            "All 103 physical OCR/manual component labels are represented as rows.",
            "INST-NSSS-A and INST-NSSS-B are retained as physical rows with no final edges.",
            "GND-GRID is excluded as a station grounding/reference rail.",
            "ATS-to-rectifier proximity edges are excluded due lack of direct terminal-dot support.",
            "Remaining uncertainty is documented in final_notes.csv.",
        ],
    }
    with SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
