from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions + OCR")
RESULTS = BASE / "results"


def count_matrix(path: Path) -> dict[str, int | bool]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    body = rows[1:]
    symmetric = True
    diagonal_zero = True
    ones = 0
    for i, row in enumerate(body):
        values = [int(v) for v in row[1:]]
        if i < len(values) and values[i] != 0:
            diagonal_zero = False
        for j, value in enumerate(values):
            ones += value
            if j < len(body) and value != int(body[j][i + 1]):
                symmetric = False
    return {
        "nodes": len(header),
        "rows": len(body),
        "same_header_row_order": header == [row[0] for row in body],
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "undirected_edges": ones // 2,
    }


def main() -> None:
    final_edges = RESULTS / "document22_round04_jennifer_final_edges.csv"
    final_nodes = RESULTS / "document22_round04_jennifer_final_nodes.csv"
    final_matrix = RESULTS / "document22_round04_jennifer_final_adjacency_matrix.csv"

    if not final_edges.exists() or not final_nodes.exists() or not final_matrix.exists():
        raise FileNotFoundError("Round 04 final files are required before finalization.")

    aliases = {
        final_edges: RESULTS / "document22_final_edges.csv",
        final_nodes: RESULTS / "document22_final_nodes.csv",
        final_matrix: RESULTS / "document22_final_connectivity_matrix.csv",
    }
    for src, dst in aliases.items():
        shutil.copyfile(src, dst)
    shutil.copyfile(final_matrix, RESULTS / "connectivity_matrix.csv")

    validation = {
        "document": 22,
        "iteration": 1,
        "final_matrix": str(RESULTS / "connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "document22_final_edges.csv"),
        "final_nodes": str(RESULTS / "document22_final_nodes.csv"),
        "matrix_validation": count_matrix(final_matrix),
        "ground_truth_used": False,
        "off_the_shelf_ocr_used": False,
        "allowed_resource_folder": str(BASE),
    }
    (RESULTS / "document22_final_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    with (RESULTS / "document22_final_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Document 22 Final Connectivity Extraction\n\n")
        f.write("- Final agreement: Diego Round 03 accepted Jennifer Round 02; Jennifer Round 04 signed off.\n")
        f.write(f"- Nodes: {validation['matrix_validation']['nodes']}\n")
        f.write(f"- Undirected edges: {validation['matrix_validation']['undirected_edges']}\n")
        f.write(f"- Matrix symmetric: {validation['matrix_validation']['symmetric']}\n")
        f.write(f"- Diagonal zero: {validation['matrix_validation']['diagonal_zero']}\n")
        f.write("- Ground truth/evaluator data used: no.\n")
        f.write("- Off-the-shelf OCR used: no.\n")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
