from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path


ROUND_RE = re.compile(r"document23_round(?P<round>\d+)_(?P<agent>diego|jennifer)_edges\.csv$", re.I)


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_dicts(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean_node(row: dict[str, str]) -> str:
    return (row.get("node") or row.get("name") or "").strip()


def include_edge(row: dict[str, str]) -> bool:
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    action = (row.get("round_action") or "include").strip().lower()
    return bool(source and target and source != target and action not in {"exclude", "reject", "rejected", "remove", "removed"})


def edge_pair(row: dict[str, str]) -> tuple[str, str]:
    source = (row.get("source") or "").strip()
    target = (row.get("target") or "").strip()
    return tuple(sorted((source, target)))


def edge_label(pair: tuple[str, str]) -> str:
    return f"{pair[0]} -- {pair[1]}"


def load_graph(results_dir: Path, prefix: str) -> dict[str, object]:
    edges_path = results_dir / f"{prefix}_edges.csv"
    nodes_path = results_dir / f"{prefix}_nodes.csv"
    matrix_path = results_dir / f"{prefix}_adjacency_matrix.csv"
    if not edges_path.exists():
        raise FileNotFoundError(edges_path)
    if not nodes_path.exists():
        raise FileNotFoundError(nodes_path)

    edge_rows = read_dicts(edges_path)
    node_rows = read_dicts(nodes_path)
    nodes: list[str] = []
    seen_nodes: set[str] = set()
    for row in node_rows:
        node = clean_node(row)
        decision = (row.get("decision") or "include").strip().lower()
        if node and decision not in {"exclude", "reject", "rejected"} and node not in seen_nodes:
            nodes.append(node)
            seen_nodes.add(node)

    included_edges = [row for row in edge_rows if include_edge(row)]
    pairs = [edge_pair(row) for row in included_edges]
    unique_pairs = sorted(set(pairs))

    return {
        "prefix": prefix,
        "edges_path": edges_path,
        "nodes_path": nodes_path,
        "matrix_path": matrix_path,
        "edge_rows": edge_rows,
        "node_rows": node_rows,
        "nodes": nodes,
        "node_set": set(nodes),
        "included_edges": included_edges,
        "pairs": pairs,
        "unique_pairs": unique_pairs,
    }


def build_matrix(nodes: list[str], pairs: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in pairs:
        i = index[source]
        j = index[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def read_matrix(path: Path) -> tuple[list[str], list[list[int]]] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return None
    header = rows[0][1:]
    matrix: list[list[int]] = []
    row_names: list[str] = []
    for row in rows[1:]:
        if not row:
            continue
        row_names.append(row[0])
        matrix.append([int(value) for value in row[1:]])
    if row_names != header:
        raise ValueError(f"matrix row/header node mismatch in {path}")
    return header, matrix


def write_matrix(path: Path, nodes: list[str], matrix: list[list[int]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def validate_graph(graph: dict[str, object]) -> dict[str, object]:
    nodes = graph["nodes"]
    node_set = graph["node_set"]
    included_edges = graph["included_edges"]
    pairs = graph["pairs"]
    unique_pairs = graph["unique_pairs"]
    matrix_path = graph["matrix_path"]

    unknown_edges = []
    self_loops = []
    for row in included_edges:
        source = (row.get("source") or "").strip()
        target = (row.get("target") or "").strip()
        if source == target:
            self_loops.append(edge_label(tuple(sorted((source, target)))))
        missing = [node for node in (source, target) if node not in node_set]
        if missing:
            unknown_edges.append({"source": source, "target": target, "missing": missing})

    duplicate_pairs = sorted(pair for pair, count in Counter(pairs).items() if count > 1)
    matrix = build_matrix(nodes, unique_pairs)
    matrix_diag_nonzero = []
    matrix_asymmetric = []
    for i, row in enumerate(matrix):
        if row[i] != 0:
            matrix_diag_nonzero.append(nodes[i])
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                matrix_asymmetric.append([nodes[i], nodes[j]])

    existing_matrix_ok = False
    existing_matrix_error = None
    try:
        existing = read_matrix(matrix_path)
        if existing is not None:
            existing_nodes, existing_values = existing
            existing_matrix_ok = existing_nodes == nodes and existing_values == matrix
    except Exception as exc:  # noqa: BLE001
        existing_matrix_error = str(exc)

    edge_kind_counts = Counter((row.get("edge_kind") or "unspecified").strip() or "unspecified" for row in included_edges)
    confidence_counts = Counter((row.get("confidence") or "unspecified").strip() or "unspecified" for row in included_edges)

    errors = []
    if unknown_edges:
        errors.append("unknown_nodes")
    if duplicate_pairs:
        errors.append("duplicate_undirected_edges")
    if self_loops:
        errors.append("self_loops")
    if matrix_diag_nonzero:
        errors.append("matrix_diagonal_nonzero")
    if matrix_asymmetric:
        errors.append("matrix_asymmetric")

    return {
        "prefix": graph["prefix"],
        "node_count": len(nodes),
        "edge_row_count": len(included_edges),
        "unique_edge_count": len(unique_pairs),
        "edge_kind_counts": dict(sorted(edge_kind_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "unknown_edges": unknown_edges,
        "duplicate_pairs": [edge_label(pair) for pair in duplicate_pairs],
        "self_loops": self_loops,
        "matrix_diagonal_nonzero": matrix_diag_nonzero,
        "matrix_asymmetric": matrix_asymmetric[:20],
        "existing_matrix_matches_edges": existing_matrix_ok,
        "existing_matrix_error": existing_matrix_error,
        "validation_passed": not errors,
        "errors": errors,
    }


def discover_rounds(results_dir: Path) -> list[str]:
    found: list[tuple[int, int, str]] = []
    for path in results_dir.glob("document23_round*_*.csv"):
        match = ROUND_RE.match(path.name)
        if not match:
            continue
        round_num = int(match.group("round"))
        agent_order = 0 if match.group("agent").lower() == "diego" else 1
        prefix = path.name[:-len("_edges.csv")]
        found.append((round_num, agent_order, prefix))
    return [prefix for _, _, prefix in sorted(found)]


def write_round_comparison(results_dir: Path, prefixes: list[str], output_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    previous_pairs: set[tuple[str, str]] | None = None
    for prefix in prefixes:
        graph = load_graph(results_dir, prefix)
        pairs = set(graph["unique_pairs"])
        added = sorted(pairs - previous_pairs) if previous_pairs is not None else sorted(pairs)
        removed = sorted(previous_pairs - pairs) if previous_pairs is not None else []
        validation = validate_graph(graph)
        rows.append(
            {
                "round_prefix": prefix,
                "node_count": validation["node_count"],
                "unique_edge_count": validation["unique_edge_count"],
                "added_edge_count_vs_previous": len(added) if previous_pairs is not None else "",
                "removed_edge_count_vs_previous": len(removed) if previous_pairs is not None else "",
                "validation_passed": validation["validation_passed"],
                "added_edges_vs_previous": "; ".join(edge_label(pair) for pair in added[:100]) if previous_pairs is not None else "",
                "removed_edges_vs_previous": "; ".join(edge_label(pair) for pair in removed[:100]) if previous_pairs is not None else "",
            }
        )
        previous_pairs = pairs

    fieldnames = [
        "round_prefix",
        "node_count",
        "unique_edge_count",
        "added_edge_count_vs_previous",
        "removed_edge_count_vs_previous",
        "validation_passed",
        "added_edges_vs_previous",
        "removed_edges_vs_previous",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main(argv: list[str]) -> int:
    base_dir = Path(__file__).resolve().parents[1]
    results_dir = base_dir / "results"
    if len(argv) > 1:
        final_prefix = argv[1]
    else:
        prefixes = discover_rounds(results_dir)
        if not prefixes:
            raise SystemExit("no round edge files found")
        final_prefix = prefixes[-1]

    graph = load_graph(results_dir, final_prefix)
    validation = validate_graph(graph)
    if not validation["validation_passed"]:
        print(json.dumps(validation, indent=2))
        raise SystemExit("final graph validation failed")

    nodes = graph["nodes"]
    pairs = graph["unique_pairs"]
    matrix = build_matrix(nodes, pairs)

    final_edges = results_dir / "document23_final_edges.csv"
    final_nodes = results_dir / "document23_final_nodes.csv"
    final_matrix = results_dir / "document23_final_adjacency_matrix.csv"
    connectivity_matrix = results_dir / "connectivity_matrix.csv"

    edge_rows = graph["edge_rows"]
    node_rows = graph["node_rows"]
    edge_fields = list(edge_rows[0].keys()) if edge_rows else ["source", "target", "edge_kind", "confidence", "evidence"]
    node_fields = list(node_rows[0].keys()) if node_rows else ["node"]
    write_dicts(final_edges, edge_rows, edge_fields)
    write_dicts(final_nodes, node_rows, node_fields)
    write_matrix(final_matrix, nodes, matrix)
    shutil.copyfile(final_matrix, connectivity_matrix)

    prefixes = discover_rounds(results_dir)
    if final_prefix not in prefixes:
        prefixes.append(final_prefix)
    comparison_rows = write_round_comparison(results_dir, prefixes, results_dir / "document23_round_comparison.csv")

    validation["final_source_prefix"] = final_prefix
    validation["final_edges_file"] = str(final_edges)
    validation["final_nodes_file"] = str(final_nodes)
    validation["final_matrix_file"] = str(final_matrix)
    validation["connectivity_matrix_file"] = str(connectivity_matrix)
    validation["rounds_compared"] = [row["round_prefix"] for row in comparison_rows]

    with (results_dir / "document23_validation_summary.json").open("w", encoding="utf-8") as f:
        json.dump(validation, f, indent=2)

    print(json.dumps(validation, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
