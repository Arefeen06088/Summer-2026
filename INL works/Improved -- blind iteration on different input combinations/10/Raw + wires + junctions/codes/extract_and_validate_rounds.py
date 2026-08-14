from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw + wires + junctions")
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc10_work")


@dataclass
class ParsedRound:
    nodes: list[str]
    edges: list[dict[str, str]]
    matrix_rows: list[list[str]]


def csv_line(line: str) -> list[str]:
    return [value.strip() for value in next(csv.reader([line]))]


def block(lines: list[str], marker: str) -> list[str]:
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == marker) + 1
    except StopIteration:
        return []
    out: list[str] = []
    markers = {"NODE_ORDER_CSV", "EDGE_LIST_CSV", "MATRIX_CSV", "AMBIGUITIES"}
    for line in lines[start:]:
        stripped = line.strip()
        if stripped in {"```", "```csv"}:
            continue
        if not stripped:
            if out:
                break
            continue
        if stripped in markers and out:
            break
        if stripped.startswith(tuple(f"{n}. " for n in range(1, 10))) and out:
            break
        out.append(line.rstrip("\n"))
    return out


def parse_edges(lines: list[str]) -> list[dict[str, str]]:
    if not lines:
        return []
    rows = list(csv.reader(lines))
    if not rows:
        return []
    if [cell.strip().lower() for cell in rows[0]][:5] != ["source", "target", "confidence", "line_type", "evidence"]:
        return []
    edges: list[dict[str, str]] = []
    for row in rows[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        padded = row + [""] * max(0, 5 - len(row))
        edges.append(
            {
                "source": padded[0].strip(),
                "target": padded[1].strip(),
                "confidence": padded[2].strip(),
                "line_type": padded[3].strip(),
                "evidence": ",".join(padded[4:]).strip(),
            }
        )
    return edges


def parse_round(path: Path) -> ParsedRound:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    node_block = block(lines, "NODE_ORDER_CSV")
    nodes = csv_line(node_block[0]) if node_block else []
    edges = parse_edges(block(lines, "EDGE_LIST_CSV"))
    matrix_rows = [csv_line(line) for line in block(lines, "MATRIX_CSV")]
    return ParsedRound(nodes=nodes, edges=edges, matrix_rows=matrix_rows)


def write_outputs(round_name: str, parsed: ParsedRound) -> tuple[Path | None, Path | None]:
    edge_path = None
    matrix_path = None
    if parsed.edges:
        edge_path = RESULTS / f"{round_name}_edges.csv"
        with edge_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["source", "target", "confidence", "line_type", "evidence"])
            writer.writeheader()
            writer.writerows(parsed.edges)
    if parsed.matrix_rows:
        matrix_path = RESULTS / f"{round_name}_matrix.csv"
        with matrix_path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerows(parsed.matrix_rows)
    return edge_path, matrix_path


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
    if matrix[0][1:] != nodes:
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
    edge_count = sum(values[i][j] for i in range(len(nodes)) for j in range(i + 1, len(nodes)))
    result.update(
        {
            "symmetric": symmetric,
            "zero_diagonal": zero_diagonal,
            "matrix_edge_count": edge_count,
            "status": "ok" if symmetric and zero_diagonal else "failed",
        }
    )
    return result


def materialize_fallbacks() -> None:
    for name in [
        "diego_round1_output.txt",
        "jennifer_round1_review.txt",
        "diego_round2_response.txt",
        "jennifer_round2_final.txt",
    ]:
        target = RESULTS / name
        source = FALLBACK / name
        if not target.exists() and source.exists():
            shutil.copyfile(source, target)


def copy_agreement(round_name: str, source_round: str, source_path: Path) -> dict[str, str | int | bool] | None:
    matrix_path = RESULTS / f"{source_round}_matrix.csv"
    edge_path = RESULTS / f"{source_round}_edges.csv"
    if not matrix_path.exists():
        return None
    shutil.copyfile(matrix_path, RESULTS / f"{round_name}_matrix.csv")
    if edge_path.exists():
        shutil.copyfile(edge_path, RESULTS / f"{round_name}_edges.csv")
    parsed = parse_round(source_path)
    result = validate(round_name, parsed)
    result["status"] = f"ok_copied_from_{source_round}_agreement"
    return result


def main() -> None:
    materialize_fallbacks()
    candidates = {
        "diego_round1": RESULTS / "diego_round1_output.txt",
        "jennifer_round1": RESULTS / "jennifer_round1_review.txt",
        "diego_round2": RESULTS / "diego_round2_response.txt",
        "jennifer_round2": RESULTS / "jennifer_round2_final.txt",
    }
    summary: list[dict[str, str | int | bool]] = []
    for round_name, path in candidates.items():
        if not path.exists():
            continue
        parsed = parse_round(path)
        if round_name in {"diego_round2", "jennifer_round2"} and not parsed.matrix_rows:
            text = path.read_text(encoding="utf-8", errors="replace")
            if "AGREE_WITH_JENNIFER_ROUND1" in text or "AGREE_WITH_DIEGO_ROUND2" in text:
                copied = copy_agreement(round_name, "jennifer_round1", candidates["jennifer_round1"])
                if copied:
                    if round_name == "jennifer_round2":
                        shutil.copyfile(RESULTS / "jennifer_round2_matrix.csv", RESULTS / "connectivity_matrix_final.csv")
                        if (RESULTS / "jennifer_round2_edges.csv").exists():
                            shutil.copyfile(RESULTS / "jennifer_round2_edges.csv", RESULTS / "connectivity_edges_final.csv")
                    summary.append(copied)
                    continue
        edge_path, matrix_path = write_outputs(round_name, parsed)
        if round_name == "jennifer_round2":
            if matrix_path:
                shutil.copyfile(matrix_path, RESULTS / "connectivity_matrix_final.csv")
            if edge_path:
                shutil.copyfile(edge_path, RESULTS / "connectivity_edges_final.csv")
        summary.append(validate(round_name, parsed))

    if not (RESULTS / "connectivity_matrix_final.csv").exists() and (RESULTS / "jennifer_round1_matrix.csv").exists():
        shutil.copyfile(RESULTS / "jennifer_round1_matrix.csv", RESULTS / "connectivity_matrix_final.csv")
    if not (RESULTS / "connectivity_edges_final.csv").exists() and (RESULTS / "jennifer_round1_edges.csv").exists():
        shutil.copyfile(RESULTS / "jennifer_round1_edges.csv", RESULTS / "connectivity_edges_final.csv")

    summary_path = RESULTS / "round_validation_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        fields = [
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
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary)
    for item in summary:
        print(item)
    print(f"Wrote validation summary to {summary_path}")


if __name__ == "__main__":
    main()
