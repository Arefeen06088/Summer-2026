from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\25\Raw + wires + junctions")
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc25_work")


@dataclass
class ParsedRound:
    nodes: list[str]
    edges: list[dict[str, str]]
    matrix: list[list[str]]


def out_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".doc25_validate_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return RESULTS
    except OSError:
        FALLBACK.mkdir(parents=True, exist_ok=True)
        return FALLBACK


def csv_line(line: str) -> list[str]:
    return [cell.strip() for cell in next(csv.reader([line]))]


def block(lines: list[str], marker: str) -> list[str]:
    markers = {"NODE_ORDER_CSV", "EDGE_LIST_CSV", "MATRIX_CSV", "AMBIGUITIES"}
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == marker) + 1
    except StopIteration:
        return []
    out: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            if out:
                break
            continue
        if stripped in markers and out:
            break
        out.append(line.rstrip("\n"))
    return out


def parse_nodes(lines: list[str]) -> list[str]:
    nodes: list[str] = []
    seen: set[str] = set()
    for line in lines:
        for value in csv_line(line):
            if value and value not in seen:
                seen.add(value)
                nodes.append(value)
    return nodes


def parse_edges(lines: list[str]) -> list[dict[str, str]]:
    rows = list(csv.reader(lines)) if lines else []
    if not rows:
        return []
    header = [cell.strip().lower() for cell in rows[0]]
    if header[:2] != ["source", "target"]:
        return []
    edges: list[dict[str, str]] = []
    for row in rows[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        row = row + [""] * max(0, 5 - len(row))
        edges.append(
            {
                "source": row[0].strip(),
                "target": row[1].strip(),
                "confidence": row[2].strip(),
                "line_type": row[3].strip(),
                "evidence": ",".join(row[4:]).strip(),
            }
        )
    return edges


def first_existing(name: str) -> Path | None:
    for root in (RESULTS, FALLBACK):
        path = root / name
        if path.exists():
            return path
    return None


def parse_round(path: Path) -> ParsedRound:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return ParsedRound(
        nodes=parse_nodes(block(lines, "NODE_ORDER_CSV")),
        edges=parse_edges(block(lines, "EDGE_LIST_CSV")),
        matrix=[csv_line(line) for line in block(lines, "MATRIX_CSV")],
    )


def write_round(output: Path, round_name: str, parsed: ParsedRound) -> tuple[Path | None, Path | None]:
    edge_path = None
    matrix_path = None
    if parsed.edges:
        edge_path = output / f"{round_name}_edges.csv"
        with edge_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["source", "target", "confidence", "line_type", "evidence"])
            writer.writeheader()
            writer.writerows(parsed.edges)
    if parsed.matrix:
        matrix_path = output / f"{round_name}_matrix.csv"
        with matrix_path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerows(parsed.matrix)
    return edge_path, matrix_path


def validate(round_name: str, parsed: ParsedRound) -> dict[str, str | int | bool]:
    nodes, matrix = parsed.nodes, parsed.matrix
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
    if matrix[0][1:] != nodes:
        result["status"] = "header_node_mismatch"
        return result
    if len(matrix) != len(nodes) + 1:
        result["status"] = "row_count_mismatch"
        return result
    values: list[list[int]] = []
    for i, row in enumerate(matrix[1:]):
        if len(row) != len(nodes) + 1 or row[0] != nodes[i]:
            result["status"] = f"row_or_column_mismatch_{i + 1}"
            return result
        try:
            values.append([int(value) for value in row[1:]])
        except ValueError:
            result["status"] = f"non_integer_value_row_{i + 1}"
            return result
    symmetric = all(values[i][j] == values[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    zero_diagonal = all(values[i][i] == 0 for i in range(len(nodes)))
    matrix_edge_count = sum(values[i][j] for i in range(len(nodes)) for j in range(i + 1, len(nodes)))
    edge_nodes_ok = all(edge["source"] in nodes and edge["target"] in nodes for edge in parsed.edges)
    result.update(
        {
            "symmetric": symmetric,
            "zero_diagonal": zero_diagonal,
            "matrix_edge_count": matrix_edge_count,
            "status": "ok" if symmetric and zero_diagonal and edge_nodes_ok else "failed",
        }
    )
    if not edge_nodes_ok:
        result["status"] = "edge_node_missing_from_node_order"
    return result


def main() -> None:
    output = out_dir()
    rounds = {
        "diego_round1": first_existing("diego_round1_output.txt"),
        "jennifer_round1": first_existing("jennifer_round1_review.txt"),
        "diego_round2": first_existing("diego_round2_response.txt"),
        "jennifer_round2": first_existing("jennifer_round2_final.txt"),
    }
    summary: list[dict[str, str | int | bool]] = []
    for round_name, path in rounds.items():
        if not path:
            continue
        parsed = parse_round(path)
        edge_path, matrix_path = write_round(output, round_name, parsed)
        if round_name == "jennifer_round2":
            if matrix_path:
                shutil.copyfile(matrix_path, output / "connectivity_matrix_final.csv")
            if edge_path:
                shutil.copyfile(edge_path, output / "connectivity_edges_final.csv")
        summary.append(validate(round_name, parsed))
    summary_path = output / "round_validation_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        fields = ["round", "node_count", "edge_count_from_list", "matrix_present", "matrix_row_count", "symmetric", "zero_diagonal", "matrix_edge_count", "status"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary)
    for item in summary:
        print(item)
    print(f"Wrote validation summary to {summary_path}")


if __name__ == "__main__":
    main()
