from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

DOCUMENT = "24"
ROUND_RE = re.compile(rf"document{DOCUMENT}_round(?P<round>\d+)_(?P<agent>diego|jennifer)_edges\.csv$", re.I)


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def node_name(row: dict[str, str]) -> str:
    return (row.get("node") or row.get("name") or "").strip()


def edge_included(row: dict[str, str]) -> bool:
    action = (row.get("round_action") or "include").strip().lower()
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    return bool(source and target and source != target and action not in {"exclude", "reject", "rejected", "remove", "removed"})


def edge_pair(row: dict[str, str]) -> tuple[str, str]:
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    return tuple(sorted((source, target)))


def edge_label(pair: tuple[str, str]) -> str:
    return f"{pair[0]} -- {pair[1]}"


def write_dicts(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path: Path, nodes: list[str], pairs: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in pairs:
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])
    return matrix


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return None
    nodes = rows[0][1:]
    matrix = [[int(value) for value in row[1:]] for row in rows[1:] if row]
    row_names = [row[0] for row in rows[1:] if row]
    if nodes != row_names:
        raise ValueError(f"matrix row/header mismatch in {path}")
    return nodes, matrix


def load_graph(results_dir: Path, prefix: str) -> dict[str, object]:
    edges_path = results_dir / f"{prefix}_edges.csv"
    nodes_path = results_dir / f"{prefix}_nodes.csv"
    matrix_path = results_dir / f"{prefix}_adjacency_matrix.csv"
    edge_rows = read_dicts(edges_path)
    node_rows = read_dicts(nodes_path)

    nodes: list[str] = []
    seen_nodes: set[str] = set()
    for row in node_rows:
        node = node_name(row)
        decision = (row.get("decision") or "include").strip().lower()
        if node and decision not in {"exclude", "reject", "rejected"} and node not in seen_nodes:
            nodes.append(node)
            seen_nodes.add(node)

    included = [row for row in edge_rows if edge_included(row)]
    pairs = [edge_pair(row) for row in included]
    return {
        "prefix": prefix,
        "edges_path": edges_path,
        "nodes_path": nodes_path,
        "matrix_path": matrix_path,
        "edge_rows": edge_rows,
        "node_rows": node_rows,
        "nodes": nodes,
        "node_set": set(nodes),
        "included": included,
        "pairs": pairs,
        "unique_pairs": sorted(set(pairs)),
    }


def validate(graph: dict[str, object]) -> dict[str, object]:
    nodes = graph["nodes"]
    node_set = graph["node_set"]
    included = graph["included"]
    pairs = graph["pairs"]
    unique_pairs = graph["unique_pairs"]
    matrix_path = graph["matrix_path"]

    unknown = []
    for row in included:
        missing = [n for n in [(row.get("source") or "").strip(), (row.get("target") or "").strip()] if n not in node_set]
        if missing:
            unknown.append({"source": row.get("source"), "target": row.get("target"), "missing": missing})
    duplicates = sorted(pair for pair, count in Counter(pairs).items() if count > 1)
    matrix = [[0 for _ in nodes] for _ in nodes]
    index = {node: i for i, node in enumerate(nodes)}
    for source, target in unique_pairs:
        if source in index and target in index:
            matrix[index[source]][index[target]] = 1
            matrix[index[target]][index[source]] = 1
    asymmetric = []
    diagonal = []
    for i, row in enumerate(matrix):
        if row[i]:
            diagonal.append(nodes[i])
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                asymmetric.append([nodes[i], nodes[j]])

    existing_matrix_matches_edges = False
    existing_matrix_error = None
    try:
        existing = read_matrix(matrix_path)
        existing_matrix_matches_edges = existing == (nodes, matrix)
    except Exception as exc:  # noqa: BLE001
        existing_matrix_error = str(exc)

    edge_kind_counts = Counter((row.get("edge_kind") or "unspecified").strip() or "unspecified" for row in included)
    confidence_counts = Counter((row.get("confidence") or "unspecified").strip() or "unspecified" for row in included)
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
        "edge_kind_counts": dict(sorted(edge_kind_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "unknown_edges": unknown,
        "duplicate_pairs": [edge_label(pair) for pair in duplicates],
        "matrix_diagonal_nonzero": diagonal,
        "matrix_asymmetric": asymmetric[:20],
        "existing_matrix_matches_edges": existing_matrix_matches_edges,
        "existing_matrix_error": existing_matrix_error,
        "validation_passed": not errors,
        "errors": errors,
    }


def discover_rounds(results_dir: Path) -> list[str]:
    found: list[tuple[int, int, str]] = []
    for path in results_dir.glob(f"document{DOCUMENT}_round*_*.csv"):
        match = ROUND_RE.match(path.name)
        if match:
            order = 0 if match.group("agent").lower() == "diego" else 1
            found.append((int(match.group("round")), order, path.name[: -len("_edges.csv")]))
    return [prefix for _, _, prefix in sorted(found)]


def write_round_comparison(results_dir: Path, prefixes: list[str]) -> None:
    previous: set[tuple[str, str]] | None = None
    rows = []
    for prefix in prefixes:
        graph = load_graph(results_dir, prefix)
        validation = validate(graph)
        pairs = set(graph["unique_pairs"])
        added = sorted(pairs - previous) if previous is not None else []
        removed = sorted(previous - pairs) if previous is not None else []
        rows.append(
            {
                "round_prefix": prefix,
                "node_count": validation["node_count"],
                "unique_edge_count": validation["unique_edge_count"],
                "added_edge_count_vs_previous": "" if previous is None else len(added),
                "removed_edge_count_vs_previous": "" if previous is None else len(removed),
                "validation_passed": validation["validation_passed"],
                "added_edges_vs_previous": "; ".join(edge_label(pair) for pair in added[:100]),
                "removed_edges_vs_previous": "; ".join(edge_label(pair) for pair in removed[:100]),
            }
        )
        previous = pairs

    path = results_dir / f"document{DOCUMENT}_round_comparison.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
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

    write_dicts(final_edges, graph["edge_rows"], list(graph["edge_rows"][0].keys()))
    write_dicts(final_nodes, graph["node_rows"], list(graph["node_rows"][0].keys()))
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
