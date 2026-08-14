import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA_PATH = RESULTS / "rounds_connectivity.json"


def parse_chain(chain):
    parts = [part.strip() for part in chain.split("--") if part.strip()]
    if len(parts) < 2:
        raise ValueError(f"edge chain must contain at least two names: {chain!r}")
    return list(zip(parts, parts[1:]))


def expand_edges(edge_chains):
    edges = []
    for chain in edge_chains:
        edges.extend(parse_chain(chain))
    return edges


def validate_round(round_name, nodes, edges):
    seen_nodes = set()
    duplicate_nodes = []
    for node in nodes:
        if node in seen_nodes:
            duplicate_nodes.append(node)
        seen_nodes.add(node)

    unknown = sorted({name for edge in edges for name in edge if name not in seen_nodes})
    normalized_edges = {tuple(sorted(edge)) for edge in edges if edge[0] != edge[1]}
    self_loops = sorted({edge[0] for edge in edges if edge[0] == edge[1]})

    problems = []
    if duplicate_nodes:
        problems.append(f"duplicate nodes: {duplicate_nodes}")
    if unknown:
        problems.append(f"unknown edge endpoints: {unknown}")
    if self_loops:
        problems.append(f"self-loops found: {self_loops}")

    if problems:
        raise ValueError(f"{round_name}: " + "; ".join(problems))

    return sorted(normalized_edges)


def write_csv_matrix(path, nodes, edges):
    index = {node: pos for pos, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        i = index[a]
        j = index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edge_list(path, edges):
    with path.open("w", encoding="utf-8") as handle:
        for a, b in edges:
            handle.write(f"{a}--{b}\n")


def write_notes(path, item):
    with path.open("w", encoding="utf-8") as handle:
        handle.write(f"# {item['name']}\n\n")
        for key in ("agent", "role", "status"):
            if key in item:
                handle.write(f"- {key}: {item[key]}\n")
        handle.write("\n")
        for note in item.get("notes", []):
            handle.write(f"- {note}\n")


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"missing {DATA_PATH}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    summary_rows = []

    for item in payload["rounds"]:
        name = item["name"]
        nodes = item["nodes"]
        edges = validate_round(name, nodes, expand_edges(item["edge_chains"]))
        stem = name.lower().replace(" ", "_")
        write_csv_matrix(RESULTS / f"{stem}_matrix.csv", nodes, edges)
        write_edge_list(RESULTS / f"{stem}_edges.txt", edges)
        write_notes(RESULTS / f"{stem}_notes.md", item)

        summary_rows.append(
            {
                "round": name,
                "agent": item.get("agent", ""),
                "node_count": len(nodes),
                "edge_count": len(edges),
                "matrix_file": f"{stem}_matrix.csv",
                "edge_file": f"{stem}_edges.txt",
                "notes_file": f"{stem}_notes.md",
            }
        )

    with (RESULTS / "round_artifacts_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    final_name = payload.get("final_round")
    if final_name:
        final = next(item for item in payload["rounds"] if item["name"] == final_name)
        final_edges = validate_round(final_name, final["nodes"], expand_edges(final["edge_chains"]))
        write_csv_matrix(RESULTS / "connectivity_matrix_final.csv", final["nodes"], final_edges)
        write_edge_list(RESULTS / "connectivity_edges_final.txt", final_edges)

    print(f"wrote {len(summary_rows)} round artifact sets to {RESULTS}")


if __name__ == "__main__":
    main()
