from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + wires"
)
RESULTS = ROOT / "results"

NODES = [
    "GEN-G01",
    "ISO-GEN-1",
    "CB-GEN-A",
    "OFFSITE-345",
    "DS-SAT-1",
    "BUS-13A",
    "CB-TIE-13",
    "BUS-13B",
    "CB-UAT-A",
    "TR-UAT-A",
    "TR-SAT-A",
    "CB-SAT-A",
    "DG-1A",
    "CB-DG-A",
    "BUS-4A",
    "CB-TIE-4",
    "BUS-4B",
    "CB-UAT-B",
    "TR-UAT-B",
    "TR-SAT-B",
    "CB-SAT-B",
    "DG-1B",
    "CB-DG-B",
    "CB-480A",
    "TR-480A",
    "LC-480A",
    "CB-MCC-A1",
    "MCC-A1",
    "CB-P201A",
    "PUMP-P201A",
    "CB-MOV101A",
    "MOV-101A",
    "CB-FAN101A",
    "FAN-F101A",
    "CB-MCC-A2",
    "MCC-A2",
    "CB-P202A",
    "PUMP-P202A",
    "CB-MOV102A",
    "MOV-102A",
    "CB-HTR101A",
    "HTR-H101A",
    "CB-480B",
    "TR-480B",
    "LC-480B",
    "CB-MCC-B1",
    "MCC-B1",
    "CB-P201B",
    "PUMP-P201B",
    "CB-MOV101B",
    "MOV-101B",
    "CB-FAN101B",
    "FAN-F101B",
    "CB-MCC-B2",
    "MCC-B2",
    "CB-P202B",
    "PUMP-P202B",
    "CB-MOV102B",
    "MOV-102B",
    "CB-HTR101B",
    "HTR-H101B",
    "CB-480C",
    "TR-480C",
    "LC-480C",
    "CB-MCC-C1",
    "MCC-C1",
    "CB-P301A",
    "PUMP-P301A",
    "CB-MOV201A",
    "MOV-201A",
    "CB-FAN201A",
    "FAN-F201A",
    "CB-MCC-C2",
    "MCC-C2",
    "CB-P302A",
    "PUMP-P302A",
    "CB-MOV202A",
    "MOV-202A",
    "CB-HTR201A",
    "HTR-H201A",
    "CB-480D",
    "TR-480D",
    "LC-480D",
    "CB-MCC-D1",
    "MCC-D1",
    "CB-P301B",
    "PUMP-P301B",
    "CB-MOV201B",
    "MOV-201B",
    "CB-FAN201B",
    "FAN-F201B",
    "CB-MCC-D2",
    "MCC-D2",
    "CB-P302B",
    "PUMP-P302B",
    "CB-MOV202B",
    "MOV-202B",
    "CB-HTR201B",
    "HTR-H201B",
    "BAT-125A",
    "BCHG-125A",
    "BUS-125DCA",
    "INV-120A",
    "UPS-120A",
    "PNL-AC-CR1",
    "PPS-A",
    "ANN-101",
    "RELAY-K101",
    "RELAY-K102",
    "SR-101",
    "BAT-125B",
    "BCHG-125B",
    "BUS-125DCB",
    "INV-120B",
    "UPS-120B",
    "PNL-AC-CR2",
    "PPS-B",
    "ANN-201",
    "RELAY-K201",
    "RELAY-K202",
]


EDGE_TEXT_DIEGO_R1 = """
GEN-G01--ISO-GEN-1; ISO-GEN-1--CB-GEN-A; CB-GEN-A--BUS-13A; BUS-13A--CB-TIE-13; CB-TIE-13--BUS-13B
OFFSITE-345--DS-SAT-1; DS-SAT-1--TR-SAT-A; DS-SAT-1--TR-SAT-B; TR-SAT-A--CB-SAT-A; CB-SAT-A--BUS-4A
BUS-13A--CB-UAT-A; CB-UAT-A--TR-UAT-A; TR-UAT-A--BUS-4A; BUS-13B--CB-UAT-B; CB-UAT-B--TR-UAT-B; TR-UAT-B--BUS-4B
TR-SAT-B--CB-SAT-B; CB-SAT-B--BUS-4B; DG-1A--CB-DG-A; CB-DG-A--BUS-4A; DG-1B--CB-DG-B; CB-DG-B--BUS-4B; BUS-4A--CB-TIE-4; CB-TIE-4--BUS-4B
BUS-4A--CB-480A; CB-480A--TR-480A; TR-480A--LC-480A; BUS-4A--CB-480B; CB-480B--TR-480B; TR-480B--LC-480B
BUS-4B--CB-480C; CB-480C--TR-480C; TR-480C--LC-480C; BUS-4B--CB-480D; CB-480D--TR-480D; TR-480D--LC-480D
LC-480A--CB-MCC-A1; CB-MCC-A1--MCC-A1; MCC-A1--CB-P201A; CB-P201A--PUMP-P201A; MCC-A1--CB-MOV101A; CB-MOV101A--MOV-101A; MCC-A1--CB-FAN101A; CB-FAN101A--FAN-F101A
LC-480A--CB-MCC-A2; CB-MCC-A2--MCC-A2; MCC-A2--CB-P202A; CB-P202A--PUMP-P202A; MCC-A2--CB-MOV102A; CB-MOV102A--MOV-102A; MCC-A2--CB-HTR101A; CB-HTR101A--HTR-H101A
LC-480B--CB-MCC-B1; CB-MCC-B1--MCC-B1; MCC-B1--CB-P201B; CB-P201B--PUMP-P201B; MCC-B1--CB-MOV101B; CB-MOV101B--MOV-101B; MCC-B1--CB-FAN101B; CB-FAN101B--FAN-F101B
LC-480B--CB-MCC-B2; CB-MCC-B2--MCC-B2; MCC-B2--CB-P202B; CB-P202B--PUMP-P202B; MCC-B2--CB-MOV102B; CB-MOV102B--MOV-102B; MCC-B2--CB-HTR101B; CB-HTR101B--HTR-H101B
LC-480C--CB-MCC-C1; CB-MCC-C1--MCC-C1; MCC-C1--CB-P301A; CB-P301A--PUMP-P301A; MCC-C1--CB-MOV201A; CB-MOV201A--MOV-201A; MCC-C1--CB-FAN201A; CB-FAN201A--FAN-F201A
LC-480C--CB-MCC-C2; CB-MCC-C2--MCC-C2; MCC-C2--CB-P302A; CB-P302A--PUMP-P302A; MCC-C2--CB-MOV202A; CB-MOV202A--MOV-202A; MCC-C2--CB-HTR201A; CB-HTR201A--HTR-H201A
LC-480D--CB-MCC-D1; CB-MCC-D1--MCC-D1; MCC-D1--CB-P301B; CB-P301B--PUMP-P301B; MCC-D1--CB-MOV201B; CB-MOV201B--MOV-201B; MCC-D1--CB-FAN201B; CB-FAN201B--FAN-F201B
LC-480D--CB-MCC-D2; CB-MCC-D2--MCC-D2; MCC-D2--CB-P302B; CB-P302B--PUMP-P302B; MCC-D2--CB-MOV202B; CB-MOV202B--MOV-202B; MCC-D2--CB-HTR201B; CB-HTR201B--HTR-H201B
BAT-125A--BUS-125DCA; BCHG-125A--BUS-125DCA; BAT-125A--BCHG-125A; BUS-125DCA--INV-120A; BUS-125DCA--PNL-AC-CR1; BUS-125DCA--PPS-A
BAT-125B--BUS-125DCB; BCHG-125B--BUS-125DCB; BUS-125DCB--INV-120B; BUS-125DCB--PNL-AC-CR2; BUS-125DCB--PPS-B
INV-120A--UPS-120A; UPS-120A--PNL-AC-CR1; PNL-AC-CR1--PPS-A; ANN-101--RELAY-K101; RELAY-K101--RELAY-K102; RELAY-K102--SR-101
INV-120B--UPS-120B; UPS-120B--PNL-AC-CR2; PNL-AC-CR2--PPS-B; ANN-201--RELAY-K201; RELAY-K201--RELAY-K202; RELAY-K202--SR-101
"""

EDGE_TEXT_JENNIFER_R1 = """
GEN-G01--ISO-GEN-1; ISO-GEN-1--CB-GEN-A; CB-GEN-A--BUS-13A; BUS-13A--CB-TIE-13; CB-TIE-13--BUS-13B
OFFSITE-345--DS-SAT-1; DS-SAT-1--TR-SAT-A; TR-SAT-A--CB-SAT-A; CB-SAT-A--BUS-4A
BUS-13A--CB-UAT-A; CB-UAT-A--TR-UAT-A; TR-UAT-A--BUS-4A; BUS-13B--CB-UAT-B; CB-UAT-B--TR-UAT-B; TR-UAT-B--BUS-4B
TR-SAT-B--CB-SAT-B; CB-SAT-B--BUS-4B; DG-1A--CB-DG-A; CB-DG-A--BUS-4A; DG-1B--CB-DG-B; CB-DG-B--BUS-4B; BUS-4A--CB-TIE-4; CB-TIE-4--BUS-4B
BUS-4A--CB-480A; CB-480A--TR-480A; TR-480A--LC-480A; BUS-4A--CB-480B; CB-480B--TR-480B; TR-480B--LC-480B
BUS-4B--CB-480C; CB-480C--TR-480C; TR-480C--LC-480C; BUS-4B--CB-480D; CB-480D--TR-480D; TR-480D--LC-480D
LC-480A--CB-MCC-A1; CB-MCC-A1--MCC-A1; MCC-A1--CB-P201A; CB-P201A--PUMP-P201A; MCC-A1--CB-MOV101A; CB-MOV101A--MOV-101A; MCC-A1--CB-FAN101A; CB-FAN101A--FAN-F101A
LC-480A--CB-MCC-A2; CB-MCC-A2--MCC-A2; MCC-A2--CB-P202A; CB-P202A--PUMP-P202A; MCC-A2--CB-MOV102A; CB-MOV102A--MOV-102A; MCC-A2--CB-HTR101A; CB-HTR101A--HTR-H101A
LC-480B--CB-MCC-B1; CB-MCC-B1--MCC-B1; MCC-B1--CB-P201B; CB-P201B--PUMP-P201B; MCC-B1--CB-MOV101B; CB-MOV101B--MOV-101B; MCC-B1--CB-FAN101B; CB-FAN101B--FAN-F101B
LC-480B--CB-MCC-B2; CB-MCC-B2--MCC-B2; MCC-B2--CB-P202B; CB-P202B--PUMP-P202B; MCC-B2--CB-MOV102B; CB-MOV102B--MOV-102B; MCC-B2--CB-HTR101B; CB-HTR101B--HTR-H101B
LC-480C--CB-MCC-C1; CB-MCC-C1--MCC-C1; MCC-C1--CB-P301A; CB-P301A--PUMP-P301A; MCC-C1--CB-MOV201A; CB-MOV201A--MOV-201A; MCC-C1--CB-FAN201A; CB-FAN201A--FAN-F201A
LC-480C--CB-MCC-C2; CB-MCC-C2--MCC-C2; MCC-C2--CB-P302A; CB-P302A--PUMP-P302A; MCC-C2--CB-MOV202A; CB-MOV202A--MOV-202A; MCC-C2--CB-HTR201A; CB-HTR201A--HTR-H201A
LC-480D--CB-MCC-D1; CB-MCC-D1--MCC-D1; MCC-D1--CB-P301B; CB-P301B--PUMP-P301B; MCC-D1--CB-MOV201B; CB-MOV201B--MOV-201B; MCC-D1--CB-FAN201B; CB-FAN201B--FAN-F201B
LC-480D--CB-MCC-D2; CB-MCC-D2--MCC-D2; MCC-D2--CB-P302B; CB-P302B--PUMP-P302B; MCC-D2--CB-MOV202B; CB-MOV202B--MOV-202B; MCC-D2--CB-HTR201B; CB-HTR201B--HTR-H201B
BAT-125A--BUS-125DCA; BCHG-125A--BUS-125DCA; BAT-125A--BCHG-125A; BUS-125DCA--INV-120A; BUS-125DCA--PPS-A
BAT-125B--BUS-125DCB; BCHG-125B--BUS-125DCB; BUS-125DCB--INV-120B; BUS-125DCB--PPS-B
INV-120A--UPS-120A; UPS-120A--PNL-AC-CR1; PNL-AC-CR1--PPS-A; UPS-120A--ANN-101; ANN-101--PPS-A; ANN-101--RELAY-K101; PNL-AC-CR1--RELAY-K101; PPS-A--RELAY-K102; RELAY-K101--RELAY-K102; RELAY-K102--SR-101
INV-120B--UPS-120B; UPS-120B--PNL-AC-CR2; PNL-AC-CR2--PPS-B; UPS-120B--ANN-201; ANN-201--PPS-B; ANN-201--RELAY-K201; PNL-AC-CR2--RELAY-K201; PPS-B--RELAY-K202
"""

ROUND_NOTES = {
    "round1_diego": "High-recall proposal. Candidate matrix includes visually plausible items later rejected or left uncertain, including DS-SAT-1--TR-SAT-B, BUS-125DC*--PNL-* and RELAY-K202--SR-101.",
    "round1_jennifer": "Precision refinement. Removed unsupported/ambiguous high-recall edges and added resolved bottom control-panel dashed edges.",
    "round2_diego": "Targeted adjudication. Diego accepted Jennifer R1 unchanged.",
    "round2_jennifer_final": "Final precision pass. Jennifer R2 accepted RELAY-K202--SR-101 based on the added SR-to-B-relay crop and otherwise kept Diego R2/Jennifer R1 unchanged.",
    "round3_diego_saturation": "Saturation pass. Diego R3 agreed with Jennifer R2: RELAY-K202--SR-101 accepted, DS-SAT-1--TR-SAT-B rejected/uncertain, no further deltas.",
}

EDGE_TEXT_FINAL = EDGE_TEXT_JENNIFER_R1 + "\nRELAY-K202--SR-101\n"


def parse_edges(text: str) -> list[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    valid = set(NODES)
    for chunk in text.replace("\n", ";").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        left, right = [part.strip() for part in chunk.split("--", 1)]
        if left not in valid or right not in valid:
            raise ValueError(f"Unknown node in edge: {left}--{right}")
        if left == right:
            raise ValueError(f"Unexpected self-loop: {left}")
        edges.add(tuple(sorted((left, right))))
    return sorted(edges, key=lambda edge: (NODES.index(edge[0]), NODES.index(edge[1])))


def adjacency(edges: list[tuple[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for left, right in edges:
        i = index[left]
        j = index[right]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, edges: list[tuple[str, str]]) -> None:
    matrix = adjacency(edges)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *NODES])
        for node, row in zip(NODES, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        writer.writerows(edges)


def qa(round_name: str, edges: list[tuple[str, str]]) -> dict[str, object]:
    matrix = adjacency(edges)
    isolated = [
        node
        for node, row in zip(NODES, matrix)
        if not any(row)
    ]
    symmetric = all(
        matrix[i][j] == matrix[j][i]
        for i in range(len(NODES))
        for j in range(len(NODES))
    )
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(NODES)))
    return {
        "round": round_name,
        "node_count": len(NODES),
        "edge_count": len(edges),
        "matrix_size": [len(NODES), len(NODES)],
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "isolated_nodes": isolated,
        "notes": ROUND_NOTES[round_name],
    }


def write_markdown_summary(round_edges: dict[str, list[tuple[str, str]]]) -> None:
    lines = [
        "# Document 7 Connectivity Extraction",
        "",
        "Resources used: only files under `Raw + wires` plus generated crops stored in `results/crops`.",
        "Ground truth and GT-derived feedback were not used.",
        "",
        "## Rounds",
        "",
    ]
    previous: set[tuple[str, str]] | None = None
    for name, edges in round_edges.items():
        current = set(edges)
        lines.append(f"### {name}")
        lines.append(f"- Nodes: {len(NODES)}")
        lines.append(f"- Edges: {len(edges)}")
        lines.append(f"- Note: {ROUND_NOTES[name]}")
        if previous is not None:
            added = sorted(current - previous)
            removed = sorted(previous - current)
            lines.append(f"- Added vs previous: {len(added)}")
            if added:
                lines.append("  - " + "; ".join(f"{a}--{b}" for a, b in added))
            lines.append(f"- Removed vs previous: {len(removed)}")
            if removed:
                lines.append("  - " + "; ".join(f"{a}--{b}" for a, b in removed))
        lines.append("")
        previous = current
    lines.extend(
        [
            "## Final",
            "",
            "Final matrix: `final_matrix.csv`.",
            "Final edge list: `final_edges.csv`.",
            "Final node order: `final_nodes.csv`.",
            "",
            "Saturation: Jennifer R2 added RELAY-K202--SR-101, and Diego R3 agreed with no further deltas.",
        ]
    )
    (RESULTS / "rounds_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    round_edges = {
        "round1_diego": parse_edges(EDGE_TEXT_DIEGO_R1),
        "round1_jennifer": parse_edges(EDGE_TEXT_JENNIFER_R1),
        "round2_diego": parse_edges(EDGE_TEXT_JENNIFER_R1),
        "round2_jennifer_final": parse_edges(EDGE_TEXT_FINAL),
        "round3_diego_saturation": parse_edges(EDGE_TEXT_FINAL),
    }

    qa_rows = []
    for name, edges in round_edges.items():
        write_matrix(RESULTS / f"{name}_matrix.csv", edges)
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        qa_rows.append(qa(name, edges))

    final_edges = round_edges["round3_diego_saturation"]
    write_matrix(RESULTS / "final_matrix.csv", final_edges)
    write_edges(RESULTS / "final_edges.csv", final_edges)

    with (RESULTS / "final_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "component"])
        for index, node in enumerate(NODES, start=1):
            writer.writerow([index, node])

    final_adj = {
        node: sorted(
            other
            for edge in final_edges
            for other in (
                [edge[1]] if edge[0] == node else [edge[0]] if edge[1] == node else []
            )
        )
        for node in NODES
    }
    (RESULTS / "final_adjacency.json").write_text(
        json.dumps(final_adj, indent=2),
        encoding="utf-8",
    )
    (RESULTS / "qa_summary.json").write_text(
        json.dumps(qa_rows, indent=2),
        encoding="utf-8",
    )
    write_markdown_summary(round_edges)

    print(json.dumps(qa_rows, indent=2))


if __name__ == "__main__":
    main()
