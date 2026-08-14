import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"


def normalize_edge(edge):
    a, b = edge[:2]
    if a == b:
        raise ValueError(f"self-loop edge is not expected: {edge!r}")
    return tuple(sorted((a, b)))


def validate_round(name, nodes, edges):
    seen_nodes = set(nodes)
    if len(seen_nodes) != len(nodes):
        dupes = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{name}: duplicate nodes: {dupes}")

    normalized = set()
    for edge in edges:
        a, b = edge[:2]
        missing = [node for node in (a, b) if node not in seen_nodes]
        if missing:
            raise ValueError(f"{name}: edge {edge!r} references missing nodes {missing}")
        key = normalize_edge(edge)
        if key in normalized:
            raise ValueError(f"{name}: duplicate undirected edge {edge!r}")
        normalized.add(key)


def write_round(name, nodes, edges, notes=None):
    RESULTS.mkdir(parents=True, exist_ok=True)
    validate_round(name, nodes, edges)

    edge_keys = {normalize_edge(edge) for edge in edges}
    matrix_path = RESULTS / f"{name}_connectivity_matrix.csv"
    with matrix_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(normalize_edge((row_node, col_node)) in edge_keys))
            writer.writerow(row)

    edge_path = RESULTS / f"{name}_edges.csv"
    with edge_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "evidence"])
        for a, b, evidence in edges:
            writer.writerow([a, b, evidence])

    summary_path = RESULTS / f"{name}_summary.json"
    summary = {
        "round": name,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "matrix_file": matrix_path.name,
        "edge_file": edge_path.name,
        "notes": notes or [],
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_all(rounds):
    summaries = []
    for round_def in rounds:
        summaries.append(write_round(**round_def))

    (RESULTS / "round_summaries.json").write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    return summaries
