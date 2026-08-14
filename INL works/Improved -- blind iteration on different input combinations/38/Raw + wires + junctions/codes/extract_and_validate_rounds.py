from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DOC = "38"
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc38_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions")
ROUND_DIR = WORK / "results"
DESIGNATED_RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"

ROUND_FILES = [
    ("diego_round1", "diego_doc38_round1_extraction.txt"),
    ("jennifer_round1", "jennifer_doc38_round1_precision.txt"),
    ("diego_round2", "diego_doc38_round2_extraction.txt"),
    ("jennifer_round2_final", "jennifer_doc38_round2_final.txt"),
]

FINAL_PRIORITY = ["jennifer_round2_final", "diego_round2", "jennifer_round1", "diego_round1"]
STOP_PREFIXES = (
    "1)",
    "2)",
    "3)",
    "4)",
    "5)",
    "REMOVED",
    "UNCERTAIN",
    "COUNTS",
    "NOTES",
    "SUMMARY",
    "AGREE",
    "FINAL_",
    "CHANGES",
    "REMAINING",
    "REVIEW_",
    "ROUND2_",
)


@dataclass
class RoundGraph:
    slug: str
    source_file: Path
    nodes: list[str]
    edges: list[dict[str, str]]

    @property
    def pairs(self) -> set[tuple[str, str]]:
        return {canonical_pair(row["source"], row["target"]) for row in self.edges}


def result_dir() -> Path:
    try:
        DESIGNATED_RESULTS.mkdir(parents=True, exist_ok=True)
        probe = DESIGNATED_RESULTS / ".write_probe_doc38"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return DESIGNATED_RESULTS
    except OSError:
        FALLBACK_RESULTS.mkdir(parents=True, exist_ok=True)
        return FALLBACK_RESULTS


def canonical_pair(a: str, b: str) -> tuple[str, str]:
    a = a.strip()
    b = b.strip()
    return (a, b) if a <= b else (b, a)


def stable_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        value = value.strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def is_stop_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    upper = stripped.upper()
    return upper.startswith(STOP_PREFIXES)


def csv_block(lines: list[str], marker: str, header: str) -> list[str]:
    marker_indexes = []
    for idx, line in enumerate(lines):
        stripped = line.strip().upper()
        if stripped == marker or stripped.endswith(f") {marker}"):
            marker_indexes.append(idx)
    if not marker_indexes:
        return []
    start = marker_indexes[-1] + 1
    while start < len(lines) and lines[start].strip().lower() != header:
        start += 1
    if start >= len(lines):
        return []
    collected = [lines[start].strip()]
    for line in lines[start + 1 :]:
        if is_stop_line(line):
            break
        collected.append(line.rstrip("\n"))
    return collected


def parse_nodes(lines: list[str]) -> list[str]:
    block = csv_block(lines, "NODE_LIST_CSV", "node")
    if not block:
        return []
    reader = csv.reader(block)
    rows = list(reader)
    return stable_unique(row[0].strip() for row in rows[1:] if row and row[0].strip())


def parse_edges(lines: list[str]) -> list[dict[str, str]]:
    block = csv_block(lines, "EDGE_LIST_CSV", "source,target,confidence,line_type,evidence")
    if not block:
        return []
    reader = csv.DictReader(block)
    edges: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for row in reader:
        source = (row.get("source") or "").strip()
        target = (row.get("target") or "").strip()
        if not source or not target or source == target or source == "source":
            continue
        pair = canonical_pair(source, target)
        if pair in seen:
            continue
        seen.add(pair)
        edges.append(
            {
                "source": source,
                "target": target,
                "confidence": (row.get("confidence") or "").strip(),
                "line_type": (row.get("line_type") or "").strip(),
                "evidence": (row.get("evidence") or "").strip(),
            }
        )
    return edges


def parse_round(slug: str, source_file: Path) -> RoundGraph | None:
    if not source_file.exists():
        return None
    lines = source_file.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    nodes = parse_nodes(lines)
    edges = parse_edges(lines)
    edge_nodes = stable_unique(endpoint for edge in edges for endpoint in (edge["source"], edge["target"]))
    if nodes:
        nodes.extend(node for node in edge_nodes if node not in nodes)
    else:
        nodes = edge_nodes
    return RoundGraph(slug, source_file, nodes, edges)


def write_nodes(path: Path, nodes: list[str]) -> None:
    path.write_text("\n".join(nodes) + "\n", encoding="utf-8")


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "confidence", "line_type", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], pairs: set[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for row_node in nodes:
            writer.writerow(
                [row_node]
                + [0 if row_node == col_node else int(canonical_pair(row_node, col_node) in pairs) for col_node in nodes]
            )


def choose_final(graphs: dict[str, RoundGraph]) -> RoundGraph:
    for slug in FINAL_PRIORITY:
        graph = graphs.get(slug)
        if graph is not None:
            return graph
    raise RuntimeError("No parseable round graph found.")


def main() -> None:
    out_dir = result_dir()
    graphs: dict[str, RoundGraph] = {}
    summary = [f"Document {DOC} round extraction validation", ""]
    for slug, filename in ROUND_FILES:
        graph = parse_round(slug, ROUND_DIR / filename)
        if graph is None:
            summary.append(f"{slug}: missing")
            continue
        graphs[slug] = graph
        write_nodes(out_dir / f"{slug}_nodes.txt", graph.nodes)
        write_edges(out_dir / f"{slug}_edges.csv", graph.edges)
        write_matrix(out_dir / f"{slug}_connectivity_matrix.csv", graph.nodes, graph.pairs)
        diagonal_ok = all(canonical_pair(node, node) not in graph.pairs for node in graph.nodes)
        summary.append(
            f"{slug}: nodes={len(graph.nodes)}, edges={len(graph.pairs)}, "
            f"diagonal_zero={diagonal_ok}, source={graph.source_file.name}"
        )
    final = choose_final(graphs)
    write_nodes(out_dir / "final_nodes.txt", final.nodes)
    write_edges(out_dir / "final_edges.csv", final.edges)
    write_matrix(out_dir / "final_connectivity_matrix.csv", final.nodes, final.pairs)
    summary.extend(
        [
            "",
            f"FINAL_SELECTED={final.slug}",
            f"FINAL_NODE_COUNT={len(final.nodes)}",
            f"FINAL_EDGE_COUNT={len(final.pairs)}",
            "MATRIX_FORMAT=rows and columns share final_nodes.txt order; symmetric; diagonal zero.",
        ]
    )
    (out_dir / "validation_summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
