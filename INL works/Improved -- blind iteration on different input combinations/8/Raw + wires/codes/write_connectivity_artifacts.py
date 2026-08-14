from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires"
)
RESULTS = ROOT / "results"

NODES = [
    "GRID-345-01", "SUT-2A", "CB-402A", "BUS-4160-N2A", "CB-401A",
    "UAT-2A", "GEN-U2", "UAT-2B", "CB-401B", "BUS-4160-N2B",
    "CB-402B", "SUT-2B", "GRID-345-02", "CB-TIE-4160", "EDG-2A",
    "CB-EDG-A", "BUS-4160-S2A", "TR-480-2A", "CT-4160A",
    "RELAY-50/51A", "PT-4160A", "RELAY-27A", "RELAY-86A", "EDG-2C",
    "CB-EDG-C", "TR-480-N2A", "BUS-480-N2A", "DS-480-A", "DS-480-B",
    "TR-480-N2B", "BUS-480-N2B", "EDG-2B", "CB-EDG-B",
    "BUS-4160-S2B", "TR-480-2B", "CT-4160B", "RELAY-50/51B",
    "PT-4160B", "RELAY-27B", "RELAY-86B", "BUS-480-E2A", "GND-A",
    "MCC-2A1", "CB-51A", "PUMP-SI-2A", "CB-52A", "PUMP-RHR-2A",
    "CB-53A", "PUMP-CS-2A", "CB-54A", "PUMP-CCW-2A", "MCC-2A2",
    "CB-55A", "FAN-CRE-2A", "CB-56A", "MOV-8801A", "CB-57A",
    "MOV-8802A", "CB-58A", "PUMP-AF-2A", "PN-480-A", "MOV-8810A",
    "PUMP-CHG-2A", "VLV-HV-302A", "MCC-2C", "FAN-VENT-2A", "JB-2A1",
    "RELAY-K1A", "CHGR-125A", "BAT-2A", "BUS-125DC-A", "FUSE-125A",
    "PN-125A", "INV-120A", "BUS-120AC-A", "FUSE-120A", "PN-120A",
    "CP-ESFAS-A", "CP-RPS-A", "CB-N1", "BUS-480-E2B", "GND-B",
    "MCC-2B1", "CB-51B", "PUMP-SI-2B", "CB-52B", "PUMP-RHR-2B",
    "CB-53B", "PUMP-CS-2B", "CB-54B", "PUMP-CCW-2B", "MCC-2B2",
    "CB-55B", "FAN-CRE-2B", "CB-56B", "MOV-8801B", "CB-57B",
    "MOV-8802B", "CB-58B", "PUMP-AF-2B", "PN-480-B", "MOV-8810B",
    "PUMP-CHG-2B", "VLV-HV-302B", "MCC-2D", "FAN-VENT-2B", "JB-2B1",
    "RELAY-K1B", "CHGR-125B", "BAT-2B", "BUS-125DC-B", "FUSE-125B",
    "PN-125B", "INV-120B", "BUS-120AC-B", "FUSE-120B", "PN-120B",
    "CP-ESFAS-B", "CP-RPS-B", "CB-N2",
]

EDGE_TEXT_FINAL = """
GRID-345-01--SUT-2A; SUT-2A--CB-402A; CB-402A--BUS-4160-N2A; BUS-4160-N2A--CB-401A; CB-401A--UAT-2A; UAT-2A--GEN-U2; GEN-U2--UAT-2B; UAT-2B--CB-401B; CB-401B--BUS-4160-N2B; BUS-4160-N2B--CB-402B; CB-402B--SUT-2B; SUT-2B--GRID-345-02; BUS-4160-N2A--CB-TIE-4160; CB-TIE-4160--BUS-4160-N2B; BUS-4160-N2A--BUS-4160-S2A; BUS-4160-N2B--BUS-4160-S2B; BUS-4160-N2A--TR-480-N2A; BUS-4160-N2B--TR-480-N2B; EDG-2A--CB-EDG-A; CB-EDG-A--BUS-4160-S2A; BUS-4160-S2A--TR-480-2A; BUS-4160-S2A--CT-4160A; CT-4160A--RELAY-50/51A; BUS-4160-S2A--PT-4160A; PT-4160A--RELAY-27A; RELAY-50/51A--RELAY-86A; RELAY-27A--RELAY-86A; RELAY-86A--CB-EDG-A; RELAY-86A--CB-401A; BUS-4160-S2A--CB-EDG-C; EDG-2C--CB-EDG-C; CB-EDG-C--BUS-4160-S2B; EDG-2B--CB-EDG-B; CB-EDG-B--BUS-4160-S2B; BUS-4160-S2B--TR-480-2B; BUS-4160-S2B--CT-4160B; CT-4160B--RELAY-50/51B; BUS-4160-S2B--PT-4160B; PT-4160B--RELAY-27B; RELAY-50/51B--RELAY-86B; RELAY-27B--RELAY-86B; RELAY-86B--CB-EDG-B; RELAY-86B--CB-401B
TR-480-N2A--BUS-480-N2A; TR-480-N2B--BUS-480-N2B; TR-480-2A--BUS-480-E2A; TR-480-2B--BUS-480-E2B; BUS-480-N2A--DS-480-A; DS-480-A--DS-480-B; DS-480-B--BUS-480-N2B; BUS-480-N2A--CB-N1; CB-N1--CHGR-125A; BUS-480-N2B--CB-N2; CB-N2--MCC-2D; BUS-480-E2A--GND-A; BUS-480-E2B--GND-B; BUS-480-E2A--MCC-2A1; BUS-480-E2A--MCC-2A2; BUS-480-E2A--PN-480-A; BUS-480-E2B--MCC-2B1; BUS-480-E2B--MCC-2B2; BUS-480-E2B--PN-480-B; BUS-480-E2B--CHGR-125B
MCC-2A1--CB-51A; CB-51A--PUMP-SI-2A; MCC-2A1--CB-52A; CB-52A--PUMP-RHR-2A; MCC-2A1--CB-53A; CB-53A--PUMP-CS-2A; MCC-2A1--CB-54A; CB-54A--PUMP-CCW-2A; MCC-2A2--CB-55A; CB-55A--FAN-CRE-2A; MCC-2A2--CB-56A; CB-56A--MOV-8801A; MCC-2A2--CB-57A; CB-57A--MOV-8802A; MCC-2A2--CB-58A; CB-58A--PUMP-AF-2A; PN-480-A--MOV-8810A; PN-480-A--PUMP-CHG-2A; PUMP-CHG-2A--VLV-HV-302A; CHGR-125A--MCC-2C; MCC-2C--PUMP-CHG-2A; MCC-2C--FAN-VENT-2A
CHGR-125A--BAT-2A; CHGR-125A--BUS-125DC-A; BAT-2A--BUS-125DC-A; BUS-125DC-A--FUSE-125A; FUSE-125A--PN-125A; BUS-125DC-A--INV-120A; INV-120A--BUS-120AC-A; PN-125A--BUS-120AC-A; BUS-120AC-A--FUSE-120A; FUSE-120A--PN-120A; PN-125A--CP-ESFAS-A; PN-120A--CP-RPS-A; MOV-8801A--JB-2A1; JB-2A1--CP-ESFAS-A; RELAY-K1A--CP-ESFAS-A; RELAY-K1A--CB-51A; RELAY-K1A--CB-52A; RELAY-K1A--CB-53A
MCC-2B1--CB-51B; CB-51B--PUMP-SI-2B; MCC-2B1--CB-52B; CB-52B--PUMP-RHR-2B; MCC-2B1--CB-53B; CB-53B--PUMP-CS-2B; MCC-2B1--CB-54B; CB-54B--PUMP-CCW-2B; MCC-2B2--CB-55B; CB-55B--FAN-CRE-2B; MCC-2B2--CB-56B; CB-56B--MOV-8801B; MCC-2B2--CB-57B; CB-57B--MOV-8802B; MCC-2B2--CB-58B; CB-58B--PUMP-AF-2B; PN-480-B--MOV-8810B; PN-480-B--VLV-HV-302B; MCC-2D--PUMP-CHG-2B; MCC-2D--FAN-VENT-2B
CHGR-125B--BAT-2B; CHGR-125B--BUS-125DC-B; BAT-2B--BUS-125DC-B; BUS-125DC-B--FUSE-125B; FUSE-125B--PN-125B; BUS-125DC-B--INV-120B; INV-120B--BUS-120AC-B; PN-125B--BUS-120AC-B; BUS-120AC-B--FUSE-120B; FUSE-120B--PN-120B; PN-125B--CP-ESFAS-B; PN-120B--CP-RPS-B; MOV-8801B--JB-2B1; RELAY-K1B--CP-ESFAS-B; RELAY-K1B--CB-51B; RELAY-K1B--CB-52B; RELAY-K1B--CB-53B
"""

ROUND_NOTES = {
    "round1_diego": (
        "Diego R1 high-recall proposal. This is reconstructed from the final "
        "list plus Jennifer's explicit deltas: it includes PN-480-B--CHGR-125B "
        "and JB-2B1--CP-ESFAS-B, but excludes Jennifer's promoted edges."
    ),
    "round1_jennifer": (
        "Jennifer R1 precision correction. Promoted BUS-480-E2B--CHGR-125B, "
        "MCC-2C--PUMP-CHG-2A, PN-480-B--VLV-HV-302B; removed "
        "PN-480-B--CHGR-125B and JB-2B1--CP-ESFAS-B."
    ),
    "round2_diego_saturation": (
        "Diego R2 accepted Jennifer R1 unchanged. Matrix saturated at 120 "
        "nodes and 140 accepted edges."
    ),
}


def parse_edges(text: str) -> list[tuple[str, str]]:
    valid = set(NODES)
    edges: set[tuple[str, str]] = set()
    for chunk in text.replace("\n", ";").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        left, right = [item.strip() for item in chunk.split("--", 1)]
        if left not in valid or right not in valid:
            raise ValueError(f"Unknown node in edge: {left}--{right}")
        if left == right:
            raise ValueError(f"Unexpected self-loop: {left}")
        edges.add(tuple(sorted((left, right))))
    return sorted(edges, key=lambda edge: (NODES.index(edge[0]), NODES.index(edge[1])))


def with_deltas(
    base: list[tuple[str, str]],
    add: list[tuple[str, str]],
    remove: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    edges = set(base)
    for edge in remove:
        edges.discard(tuple(sorted(edge)))
    for edge in add:
        edges.add(tuple(sorted(edge)))
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
    isolated = [node for node, row in zip(NODES, matrix) if not any(row)]
    return {
        "round": round_name,
        "node_count": len(NODES),
        "edge_count": len(edges),
        "matrix_size": [len(NODES), len(NODES)],
        "symmetric": all(
            matrix[i][j] == matrix[j][i]
            for i in range(len(NODES))
            for j in range(len(NODES))
        ),
        "diagonal_zero": all(matrix[i][i] == 0 for i in range(len(NODES))),
        "isolated_nodes": isolated,
        "notes": ROUND_NOTES[round_name],
    }


def write_summary(round_edges: dict[str, list[tuple[str, str]]]) -> None:
    lines = [
        "# Document 8 Connectivity Extraction",
        "",
        "Resources used: only document 8 `Raw + wires` images and generated crops.",
        "GT and GT-derived feedback were not used.",
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
            "Saturation: Diego R2 agreed with Jennifer R1 without further deltas.",
        ]
    )
    (RESULTS / "rounds_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    final_edges = parse_edges(EDGE_TEXT_FINAL)
    diego_r1 = with_deltas(
        final_edges,
        add=[
            ("PN-480-B", "CHGR-125B"),
            ("JB-2B1", "CP-ESFAS-B"),
        ],
        remove=[
            ("BUS-480-E2B", "CHGR-125B"),
            ("MCC-2C", "PUMP-CHG-2A"),
            ("PN-480-B", "VLV-HV-302B"),
        ],
    )
    round_edges = {
        "round1_diego": diego_r1,
        "round1_jennifer": final_edges,
        "round2_diego_saturation": final_edges,
    }

    qa_rows = []
    for name, edges in round_edges.items():
        write_matrix(RESULTS / f"{name}_matrix.csv", edges)
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        qa_rows.append(qa(name, edges))

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
    write_summary(round_edges)
    print(json.dumps(qa_rows, indent=2))


if __name__ == "__main__":
    main()
