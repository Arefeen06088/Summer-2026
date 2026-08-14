from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

DOCUMENT = "27"
ROUND_RE = re.compile(rf"document{DOCUMENT}_round(?P<round>\d+)_(?P<agent>diego|jennifer)_edges\.csv$", re.I)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def include_edge(row: dict[str, str]) -> bool:
    action = (row.get("round_action") or "include").strip().lower()
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    return bool(source and target and source != target and action not in {"exclude", "reject", "rejected", "remove", "removed"})


def pair(row: dict[str, str]) -> tuple[str, str]:
    return tuple(sorted(((row.get("source") or "").strip(), (row.get("target") or "").strip())))


def edge_label(edge: tuple[str, str]) -> str:
    return f"{edge[0]} -- {edge[1]}"


def node_name(row: dict[str, str]) -> str:
    return (row.get("node") or row.get("name") or "").strip()


def load_graph(results: Path, prefix: str) -> dict[str, object]:
    edge_rows = read_rows(results / f"{prefix}_edges.csv")
    node_rows = read_rows(results / f"{prefix}_nodes.csv")
    nodes: list[str] = []
    seen: set[str] = set()
    for row in node_rows:
        node = node_name(row)
        decision = (row.get("decision") or "include").strip().lower()
        if node and decision not in {"exclude", "reject", "rejected"} and node not in seen:
            nodes.append(node)
            seen.add(node)
    included = [row for row in edge_rows if include_edge(row)]
    pairs = [pair(row) for row in included]
    return {
        "prefix": prefix,
        "edge_rows": edge_rows,
        "node_rows": node_rows,
        "nodes": nodes,
        "node_set": set(nodes),
        "included": included,
        "pairs": pairs,
        "unique_pairs": sorted(set(pairs)),
        "matrix_path": results / f"{prefix}_adjacency_matrix.csv",
    }


def build_matrix(nodes: list[str], pairs: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in pairs:
        if source in index and target in index:
            matrix[index[source]][index[target]] = 1
            matrix[index[target]][index[source]] = 1
    return matrix


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return None
    nodes = rows[0][1:]
    row_names = [row[0] for row in rows[1:] if row]
    matrix = [[int(value) for value in row[1:]] for row in rows[1:] if row]
    if row_names != nodes:
        raise ValueError(f"matrix row/header mismatch in {path}")
    return nodes, matrix


def validate(graph: dict[str, object]) -> dict[str, object]:
    nodes = graph["nodes"]
    node_set = graph["node_set"]
    included = graph["included"]
    pairs = graph["pairs"]
    unique_pairs = graph["unique_pairs"]
    matrix = build_matrix(nodes, unique_pairs)
    unknown = []
    for row in included:
        missing = [n for n in [(row.get("source") or "").strip(), (row.get("target") or "").strip()] if n not in node_set]
        if missing:
            unknown.append({"source": row.get("source"), "target": row.get("target"), "missing": missing})
    duplicates = sorted(edge for edge, count in Counter(pairs).items() if count > 1)
    diagonal = [nodes[i] for i, row in enumerate(matrix) if row[i]]
    asymmetric = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                asymmetric.append([nodes[i], nodes[j]])
    existing_matches = False
    existing_error = None
    try:
        existing_matches = read_matrix(graph["matrix_path"]) == (nodes, matrix)
    except Exception as exc:  # noqa: BLE001
        existing_error = str(exc)
    errors = []
    if unknown:
        errors.append("unknown_nodes")
    if duplicates:
        errors.append("duplicate_undirected_edges")
    if diagonal:
        errors.append("diagonal_nonzero")
    if asymmetric:
        errors.append("matrix_asymmetric")
    return {
        "prefix": graph["prefix"],
        "node_count": len(nodes),
        "edge_row_count": len(included),
        "unique_edge_count": len(unique_pairs),
        "edge_kind_counts": dict(sorted(Counter((row.get("edge_kind") or "unspecified").strip() or "unspecified" for row in included).items())),
        "confidence_counts": dict(sorted(Counter((row.get("confidence") or "unspecified").strip() or "unspecified" for row in included).items())),
        "unknown_edges": unknown,
        "duplicate_pairs": [edge_label(edge) for edge in duplicates],
        "matrix_diagonal_nonzero": diagonal,
        "matrix_asymmetric": asymmetric[:20],
        "existing_matrix_matches_edges": existing_matches,
        "existing_matrix_error": existing_error,
        "validation_passed": not errors,
        "errors": errors,
    }


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path: Path, nodes: list[str], pairs: list[tuple[str, str]]) -> None:
    matrix = build_matrix(nodes, pairs)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def discover_rounds(results: Path) -> list[str]:
    found: list[tuple[int, int, str]] = []
    for path in results.glob(f"document{DOCUMENT}_round*_*.csv"):
        match = ROUND_RE.match(path.name)
        if match:
            order = 0 if match.group("agent").lower() == "diego" else 1
            found.append((int(match.group("round")), order, path.name[: -len("_edges.csv")]))
    return [prefix for _, _, prefix in sorted(found)]


def write_round_comparison(results: Path, prefixes: list[str]) -> None:
    rows = []
    previous: set[tuple[str, str]] | None = None
    for prefix in prefixes:
        graph = load_graph(results, prefix)
        report = validate(graph)
        current = set(graph["unique_pairs"])
        added = sorted(current - previous) if previous is not None else []
        removed = sorted(previous - current) if previous is not None else []
        rows.append(
            {
                "round_prefix": prefix,
                "node_count": report["node_count"],
                "unique_edge_count": report["unique_edge_count"],
                "added_edge_count_vs_previous": "" if previous is None else len(added),
                "removed_edge_count_vs_previous": "" if previous is None else len(removed),
                "validation_passed": report["validation_passed"],
                "added_edges_vs_previous": "; ".join(edge_label(edge) for edge in added[:100]),
                "removed_edges_vs_previous": "; ".join(edge_label(edge) for edge in removed[:100]),
            }
        )
        previous = current
    if rows:
        with (results / f"document{DOCUMENT}_round_comparison.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def main(argv: list[str]) -> int:
    base = Path(__file__).resolve().parents[1]
    results = base / "results"
    prefix = argv[1] if len(argv) > 1 else discover_rounds(results)[-1]
    graph = load_graph(results, prefix)
    report = validate(graph)
    if not report["validation_passed"]:
        print(json.dumps(report, indent=2))
        raise SystemExit("final graph validation failed")
    final_edges = results / f"document{DOCUMENT}_final_edges.csv"
    final_nodes = results / f"document{DOCUMENT}_final_nodes.csv"
    final_matrix = results / f"document{DOCUMENT}_final_adjacency_matrix.csv"
    connectivity = results / "connectivity_matrix.csv"
    write_rows(final_edges, graph["edge_rows"], list(graph["edge_rows"][0].keys()))
    write_rows(final_nodes, graph["node_rows"], list(graph["node_rows"][0].keys()))
    write_matrix(final_matrix, graph["nodes"], graph["unique_pairs"])
    shutil.copyfile(final_matrix, connectivity)
    prefixes = discover_rounds(results)
    write_round_comparison(results, prefixes)
    report.update(
        {
            "final_source_prefix": prefix,
            "final_edges_file": str(final_edges),
            "final_nodes_file": str(final_nodes),
            "final_matrix_file": str(final_matrix),
            "connectivity_matrix_file": str(connectivity),
            "rounds_compared": prefixes,
        }
    )
    with (results / f"document{DOCUMENT}_validation_summary.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
