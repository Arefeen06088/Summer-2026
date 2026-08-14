from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + wires + junctions")
RESULTS = BASE / "results"


@dataclass
class ParsedRound:
    nodes: list[str]
    edges: list[tuple[str, str, str, str]]
    matrix_rows: list[list[str]]


def read_csv_line(line: str) -> list[str]:
    return next(csv.reader([line]))


def extract_block(lines: list[str], marker: str) -> list[str]:
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == marker) + 1
    except StopIteration:
        return []

    block: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            if block:
                break
            continue
        if stripped.endswith("_CSV") and block:
            break
        if stripped.startswith(tuple(f"{n}. " for n in range(1, 10))) and block:
            break
        block.append(line.rstrip("\n"))
    return block


def parse_round(path: Path) -> ParsedRound:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    node_block = extract_block(lines, "NODE_ORDER_CSV")
    nodes = read_csv_line(node_block[0]) if node_block else []

    edge_block = extract_block(lines, "EDGE_LIST_CSV")
    edges: list[tuple[str, str, str, str]] = []
    if edge_block and edge_block[0].strip().lower().startswith("source,target"):
        for row in csv.DictReader(edge_block):
            edges.append((
                row.get("source", "").strip(),
                row.get("target", "").strip(),
                row.get("confidence", "").strip(),
                row.get("evidence", "").strip(),
            ))

    matrix_block = extract_block(lines, "MATRIX_CSV")
    matrix_rows = [read_csv_line(line) for line in matrix_block] if matrix_block else []

    return ParsedRound(nodes=nodes, edges=edges, matrix_rows=matrix_rows)


def write_edge_csv(round_name: str, parsed: ParsedRound) -> Path:
    path = RESULTS / f"{round_name}_edges.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "confidence", "evidence"])
        writer.writerows(parsed.edges)
    return path


def write_matrix_csv(round_name: str, parsed: ParsedRound) -> Path:
    path = RESULTS / f"{round_name}_matrix.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(parsed.matrix_rows)
    return path


def validate(round_name: str, parsed: ParsedRound) -> dict[str, str | int | bool]:
    nodes = parsed.nodes
    matrix = parsed.matrix_rows
    result: dict[str, str | int | bool] = {
        "round": round_name,
        "node_count": len(nodes),
        "edge_count_from_list": len(parsed.edges),
        "matrix_present": bool(matrix),
        "matrix_row_count": max(len(matrix) - 1, 0),
        "symmetric": False,
        "zero_diagonal": False,
        "matrix_edge_count": 0,
        "status": "not_validated",
    }
    if not nodes or not matrix:
        result["status"] = "missing_nodes_or_matrix"
        return result

    header = matrix[0][1:]
    if header != nodes:
        result["status"] = "header_node_mismatch"
        return result
    if len(matrix) != len(nodes) + 1:
        result["status"] = "row_count_mismatch"
        return result
    values: list[list[int]] = []
    for i, row in enumerate(matrix[1:]):
        if len(row) != len(nodes) + 1:
            result["status"] = f"col_count_mismatch_row_{i + 1}"
            return result
        if row[0] != nodes[i]:
            result["status"] = f"row_label_mismatch_{i + 1}"
            return result
        try:
            values.append([int(value) for value in row[1:]])
        except ValueError:
            result["status"] = f"non_integer_value_row_{i + 1}"
            return result

    zero_diagonal = all(values[i][i] == 0 for i in range(len(nodes)))
    symmetric = all(values[i][j] == values[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    matrix_edge_count = sum(values[i][j] for i in range(len(nodes)) for j in range(i + 1, len(nodes)))
    result.update(
        {
            "symmetric": symmetric,
            "zero_diagonal": zero_diagonal,
            "matrix_edge_count": matrix_edge_count,
            "status": "ok" if symmetric and zero_diagonal else "failed",
        }
    )
    return result


def main() -> None:
    candidates = {
        "diego_round1": RESULTS / "inspection_crops" / "proposed_graph_output.txt",
        "jennifer_round1": RESULTS / "jennifer_round1_review.txt",
        "diego_round2": RESULTS / "diego_round2_response.txt",
        "jennifer_round2": RESULTS / "jennifer_round2_final.txt",
    }

    summary_rows: list[dict[str, str | int | bool]] = []
    for round_name, path in candidates.items():
        if not path.exists():
            continue
        parsed = parse_round(path)
        if round_name == "diego_round2" and not parsed.matrix_rows:
            agreed_matrix = RESULTS / "jennifer_round1_matrix.csv"
            agreed_edges = RESULTS / "jennifer_round1_edges.csv"
            if agreed_matrix.exists():
                shutil.copyfile(agreed_matrix, RESULTS / "diego_round2_matrix.csv")
            if agreed_edges.exists():
                shutil.copyfile(agreed_edges, RESULTS / "diego_round2_edges.csv")
            if "AGREE_WITH_JENNIFER" in path.read_text(encoding="utf-8", errors="replace"):
                jennifer_round1 = parse_round(candidates["jennifer_round1"])
                row = validate(round_name, jennifer_round1)
                row["status"] = "ok_copied_from_jennifer_round1_agreement"
                summary_rows.append(row)
                continue
        if parsed.edges:
            write_edge_csv(round_name, parsed)
        if parsed.matrix_rows:
            matrix_path = write_matrix_csv(round_name, parsed)
            if round_name == "jennifer_round2":
                shutil.copyfile(matrix_path, RESULTS / "connectivity_matrix_final.csv")
        if parsed.edges and round_name == "jennifer_round2":
            shutil.copyfile(RESULTS / f"{round_name}_edges.csv", RESULTS / "connectivity_edges_final.csv")
        summary_rows.append(validate(round_name, parsed))

    summary_path = RESULTS / "round_validation_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "round",
            "node_count",
            "edge_count_from_list",
            "matrix_present",
            "matrix_row_count",
            "symmetric",
            "zero_diagonal",
            "matrix_edge_count",
            "status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    for row in summary_rows:
        print(row)
    print(f"Wrote validation summary to {summary_path}")


if __name__ == "__main__":
    main()
