import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"


def normalize_edge(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop not expected: {a}")
    return tuple(sorted((a, b)))


def write_matrix(path: Path, nodes: list[str], edges: set[tuple[str, str]]) -> None:
    neighbors = {node: set() for node in nodes}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [1 if other in neighbors[node] else 0 for other in nodes])


def write_sparse(path: Path, nodes: list[str], edges: set[tuple[str, str]]) -> None:
    neighbors = {node: [] for node in nodes}
    for a, b in sorted(edges):
        neighbors[a].append(b)
        neighbors[b].append(a)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "neighbors"])
        for node in nodes:
            writer.writerow([node, "; ".join(sorted(neighbors[node]))])


def write_edges(path: Path, edges: set[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b"])
        for a, b in sorted(edges):
            writer.writerow([a, b])


def edge_set_from_pairs(nodes: list[str], pairs: str) -> set[tuple[str, str]]:
    edges = set()
    for raw_line in pairs.strip().splitlines():
        if not raw_line.strip():
            continue
        left, right = [int(part) for part in raw_line.replace("-", " ").split()[:2]]
        edges.add(normalize_edge(nodes[left - 1], nodes[right - 1]))
    return edges


def qa(nodes: list[str], edges: set[tuple[str, str]]) -> dict:
    errors = []
    seen = set()
    for node in nodes:
        if node in seen:
            errors.append(f"duplicate node: {node}")
        seen.add(node)
    node_set = set(nodes)
    for a, b in edges:
        if a == b:
            errors.append(f"self-loop: {a}")
        if a not in node_set:
            errors.append(f"edge endpoint missing: {a}")
        if b not in node_set:
            errors.append(f"edge endpoint missing: {b}")
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "qa_errors": errors,
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    # Populated after Diego/Jennifer saturation.
    nodes = []
    final_pairs = ""
    round_specs = []

    edges = edge_set_from_pairs(nodes, final_pairs) if nodes and final_pairs.strip() else set()
    if nodes:
        write_matrix(RESULTS / "connectivity_matrix_final.csv", nodes, edges)
        write_sparse(RESULTS / "connectivity_sparse_final.csv", nodes, edges)
        write_edges(RESULTS / "edges_final.csv", edges)
        with (RESULTS / "nodes_final.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "node"])
            for index, node in enumerate(nodes, start=1):
                writer.writerow([index, node])
        report = qa(nodes, edges)
        (RESULTS / "qa_final.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
    else:
        print("placeholder writer; patch nodes/final_pairs after saturation")


if __name__ == "__main__":
    main()
