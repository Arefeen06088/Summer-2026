from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

NODES = [
    "GEN-G01",
    "ISO-GEN-1",
    "CB-GEN-A",
    "BUS-13A",
    "OFFSITE-345",
    "DS-SAT-1",
    "TR-SAT-A",
    "CB-SAT-A",
    "BUS-4A",
    "CB-UAT-A",
    "TR-UAT-A",
    "DG-1A",
    "CB-DG-A",
    "CB-TIE-13",
    "BUS-13B",
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

FINAL_EDGES = [
    ("GEN-G01", "ISO-GEN-1"),
    ("ISO-GEN-1", "CB-GEN-A"),
    ("CB-GEN-A", "BUS-13A"),
    ("OFFSITE-345", "DS-SAT-1"),
    ("DS-SAT-1", "TR-SAT-A"),
    ("DS-SAT-1", "TR-SAT-B"),
    ("TR-SAT-A", "CB-SAT-A"),
    ("CB-SAT-A", "BUS-4A"),
    ("BUS-13A", "CB-UAT-A"),
    ("CB-UAT-A", "TR-UAT-A"),
    ("TR-UAT-A", "BUS-4A"),
    ("DG-1A", "CB-DG-A"),
    ("CB-DG-A", "BUS-4A"),
    ("BUS-13A", "CB-TIE-13"),
    ("CB-TIE-13", "BUS-13B"),
    ("BUS-4A", "CB-TIE-4"),
    ("CB-TIE-4", "BUS-4B"),
    ("BUS-13B", "CB-UAT-B"),
    ("CB-UAT-B", "TR-UAT-B"),
    ("TR-UAT-B", "BUS-4B"),
    ("TR-SAT-B", "CB-SAT-B"),
    ("CB-SAT-B", "BUS-4B"),
    ("DG-1B", "CB-DG-B"),
    ("CB-DG-B", "BUS-4B"),
    ("BUS-4A", "CB-480A"),
    ("CB-480A", "TR-480A"),
    ("TR-480A", "LC-480A"),
    ("BUS-4A", "CB-480B"),
    ("CB-480B", "TR-480B"),
    ("TR-480B", "LC-480B"),
    ("BUS-4B", "CB-480C"),
    ("CB-480C", "TR-480C"),
    ("TR-480C", "LC-480C"),
    ("BUS-4B", "CB-480D"),
    ("CB-480D", "TR-480D"),
    ("TR-480D", "LC-480D"),
    ("LC-480A", "CB-MCC-A1"),
    ("CB-MCC-A1", "MCC-A1"),
    ("MCC-A1", "CB-P201A"),
    ("CB-P201A", "PUMP-P201A"),
    ("MCC-A1", "CB-MOV101A"),
    ("CB-MOV101A", "MOV-101A"),
    ("MCC-A1", "CB-FAN101A"),
    ("CB-FAN101A", "FAN-F101A"),
    ("LC-480A", "CB-MCC-A2"),
    ("CB-MCC-A2", "MCC-A2"),
    ("MCC-A2", "CB-P202A"),
    ("CB-P202A", "PUMP-P202A"),
    ("MCC-A2", "CB-MOV102A"),
    ("CB-MOV102A", "MOV-102A"),
    ("MCC-A2", "CB-HTR101A"),
    ("CB-HTR101A", "HTR-H101A"),
    ("LC-480B", "CB-MCC-B1"),
    ("CB-MCC-B1", "MCC-B1"),
    ("MCC-B1", "CB-P201B"),
    ("CB-P201B", "PUMP-P201B"),
    ("MCC-B1", "CB-MOV101B"),
    ("CB-MOV101B", "MOV-101B"),
    ("MCC-B1", "CB-FAN101B"),
    ("CB-FAN101B", "FAN-F101B"),
    ("LC-480B", "CB-MCC-B2"),
    ("CB-MCC-B2", "MCC-B2"),
    ("MCC-B2", "CB-P202B"),
    ("CB-P202B", "PUMP-P202B"),
    ("MCC-B2", "CB-MOV102B"),
    ("CB-MOV102B", "MOV-102B"),
    ("MCC-B2", "CB-HTR101B"),
    ("CB-HTR101B", "HTR-H101B"),
    ("LC-480C", "CB-MCC-C1"),
    ("CB-MCC-C1", "MCC-C1"),
    ("MCC-C1", "CB-P301A"),
    ("CB-P301A", "PUMP-P301A"),
    ("MCC-C1", "CB-MOV201A"),
    ("CB-MOV201A", "MOV-201A"),
    ("MCC-C1", "CB-FAN201A"),
    ("CB-FAN201A", "FAN-F201A"),
    ("LC-480C", "CB-MCC-C2"),
    ("CB-MCC-C2", "MCC-C2"),
    ("MCC-C2", "CB-P302A"),
    ("CB-P302A", "PUMP-P302A"),
    ("MCC-C2", "CB-MOV202A"),
    ("CB-MOV202A", "MOV-202A"),
    ("MCC-C2", "CB-HTR201A"),
    ("CB-HTR201A", "HTR-H201A"),
    ("LC-480D", "CB-MCC-D1"),
    ("CB-MCC-D1", "MCC-D1"),
    ("MCC-D1", "CB-P301B"),
    ("CB-P301B", "PUMP-P301B"),
    ("MCC-D1", "CB-MOV201B"),
    ("CB-MOV201B", "MOV-201B"),
    ("MCC-D1", "CB-FAN201B"),
    ("CB-FAN201B", "FAN-F201B"),
    ("LC-480D", "CB-MCC-D2"),
    ("CB-MCC-D2", "MCC-D2"),
    ("MCC-D2", "CB-P302B"),
    ("CB-P302B", "PUMP-P302B"),
    ("MCC-D2", "CB-MOV202B"),
    ("CB-MOV202B", "MOV-202B"),
    ("MCC-D2", "CB-HTR201B"),
    ("CB-HTR201B", "HTR-H201B"),
    ("BAT-125A", "BUS-125DCA"),
    ("BCHG-125A", "BUS-125DCA"),
    ("BUS-125DCA", "INV-120A"),
    ("BUS-125DCA", "PPS-A"),
    ("INV-120A", "UPS-120A"),
    ("UPS-120A", "PNL-AC-CR1"),
    ("PNL-AC-CR1", "PPS-A"),
    ("UPS-120A", "ANN-101"),
    ("ANN-101", "PPS-A"),
    ("ANN-101", "RELAY-K101"),
    ("PPS-A", "RELAY-K101"),
    ("PPS-A", "RELAY-K102"),
    ("RELAY-K101", "RELAY-K102"),
    ("RELAY-K102", "SR-101"),
    ("RELAY-K101", "SR-101"),
    ("BAT-125B", "BUS-125DCB"),
    ("BCHG-125B", "BUS-125DCB"),
    ("BUS-125DCB", "INV-120B"),
    ("BUS-125DCB", "PPS-B"),
    ("INV-120B", "UPS-120B"),
    ("UPS-120B", "PNL-AC-CR2"),
    ("PNL-AC-CR2", "PPS-B"),
    ("UPS-120B", "ANN-201"),
    ("ANN-201", "PPS-B"),
    ("ANN-201", "RELAY-K201"),
    ("PPS-B", "RELAY-K201"),
    ("PPS-B", "RELAY-K202"),
    ("RELAY-K201", "RELAY-K202"),
    ("SR-101", "ANN-201"),
]

REMOVED_BY_JENNIFER = [
    ("BAT-125A", "BCHG-125A"),
    ("BAT-125B", "BCHG-125B"),
    ("PNL-AC-CR1", "RELAY-K101"),
    ("PNL-AC-CR2", "RELAY-K201"),
]

ADDED_BY_JENNIFER = [("RELAY-K101", "SR-101")]

UNCERTAIN_EXCLUDED = [
    (
        "BAT-125A",
        "BCHG-125A",
        "Battery and charger both land on BUS-125DCA; the apparent side proximity does not show a direct terminal-to-terminal connection.",
    ),
    (
        "BAT-125B",
        "BCHG-125B",
        "Battery and charger both land on BUS-125DCB; no supported direct battery-to-charger terminal connection.",
    ),
    (
        "PNL-AC-CR1",
        "RELAY-K101",
        "Dashed/vertical conductors near the relay area do not show a clear terminal tap from PNL-AC-CR1 to RELAY-K101.",
    ),
    (
        "PNL-AC-CR2",
        "RELAY-K201",
        "Dashed/vertical conductors near the relay area do not show a clear terminal tap from PNL-AC-CR2 to RELAY-K201.",
    ),
    (
        "CB-DG-A/B",
        "CB-TIE-13",
        "Nearby solid conductors are not terminal-supported direct ties; main supported generator/bus paths are represented separately.",
    ),
    (
        "MCCs/load centers",
        "CTRL RACEWAY A/B",
        "Raceway text labels are not components/nodes, and crossings lack junction dots.",
    ),
    (
        "SR-101",
        "RELAY-K201 or RELAY-K202",
        "The lower control run reaches ANN-201; relay K201/K202 endpoints are not visually supported.",
    ),
    (
        "Dashed raceway crossings",
        "Any unlabeled crossed conductor",
        "Diagram note says crossings without dots are not electrically connected.",
    ),
]

ROUNDS = [
    (
        "round_01_diego_high_recall",
        "Diego high-recall proposal before precision pruning.",
        "diego",
    ),
    (
        "round_02_jennifer_precision",
        "Jennifer precision review removed four unsupported candidates and added RELAY-K101--SR-101.",
        "final",
    ),
    (
        "round_03_diego_saturation",
        "Diego final reconciliation after Jennifer's correction; graph saturated unchanged.",
        "final",
    ),
]


def canonical(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


def round_edges(kind: str) -> list[tuple[str, str]]:
    if kind == "final":
        return FINAL_EDGES
    if kind != "diego":
        raise ValueError(f"Unknown round graph kind: {kind}")
    added = {canonical(edge) for edge in ADDED_BY_JENNIFER}
    edges = [edge for edge in FINAL_EDGES if canonical(edge) not in added]
    edges.extend(REMOVED_BY_JENNIFER)
    return edges


def build_matrix(edges: list[tuple[str, str]]) -> list[list[int]]:
    index = {name: i for i, name in enumerate(NODES)}
    if len(index) != len(NODES):
        raise ValueError("Duplicate node names")
    matrix = [[0 for _ in NODES] for _ in NODES]
    for a, b in edges:
        if a not in index or b not in index:
            raise KeyError(f"Unknown edge endpoint: {a!r}, {b!r}")
        i = index[a]
        j = index[b]
        if i == j:
            raise ValueError(f"Self-loop not expected: {a}")
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def validate(matrix: list[list[int]], edges: list[tuple[str, str]]) -> None:
    n = len(NODES)
    if any(len(row) != n for row in matrix):
        raise ValueError("Non-square matrix")
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError(f"Diagonal is nonzero at {NODES[i]}")
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"Asymmetric matrix at {NODES[i]} / {NODES[j]}")
    expected = len({canonical(edge) for edge in edges})
    actual = sum(sum(row) for row in matrix) // 2
    if actual != expected:
        raise ValueError(f"Edge count mismatch: expected {expected}, got {actual}")


def write_matrix(path: Path, matrix: list[list[int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component"] + NODES)
        for node, row in zip(NODES, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        writer.writerows(edges)


def write_nodes(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "component"])
        for idx, node in enumerate(NODES, start=1):
            writer.writerow([idx, node])


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["endpoint_a", "endpoint_b", "reason_not_included"])
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_notes(path: Path) -> None:
    lines = [
        "# Document 7 Connectivity Extraction",
        "",
        "Scope: blind extraction using only `Raw + wires + components + junctions` resources.",
        "",
        "Rounds:",
    ]
    for round_name, description, kind in ROUNDS:
        edges = round_edges(kind)
        lines.append(f"- `{round_name}`: {description} Edge count: {len({canonical(edge) for edge in edges})}.")
    lines.extend(
        [
            "",
            "Saturation: Diego and Jennifer converged on the Jennifer-refined graph in round 3.",
            "",
            f"Node count: {len(NODES)}",
            f"Final undirected edge count: {len({canonical(edge) for edge in FINAL_EDGES})}",
            "",
            "Important rule applied: no-dot crossings are visual crossings only; raceway/region labels were not treated as components.",
            "",
            "Jennifer changes from Diego round 1:",
            "- Removed `BAT-125A -- BCHG-125A` and `BAT-125B -- BCHG-125B` because both sides land on their DC buses without a direct battery-to-charger terminal connection.",
            "- Removed `PNL-AC-CR1 -- RELAY-K101` and `PNL-AC-CR2 -- RELAY-K201` because terminal taps are not visually supported.",
            "- Added `RELAY-K101 -- SR-101` because the lower dashed control path ties RELAY-K101 to the SR-101 circuit.",
            "",
            "Uncertain/excluded candidates are recorded in `uncertain_excluded_edges.csv`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for round_name, _, kind in ROUNDS:
        edges = round_edges(kind)
        matrix = build_matrix(edges)
        validate(matrix, edges)
        write_matrix(RESULTS / f"{round_name}_connectivity_matrix.csv", matrix)
        write_edges(RESULTS / f"{round_name}_edges.csv", edges)

    final_matrix = build_matrix(FINAL_EDGES)
    validate(final_matrix, FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_matrix)
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_nodes(RESULTS / "final_node_order.csv")
    write_uncertain(RESULTS / "uncertain_excluded_edges.csv")
    write_notes(RESULTS / "round_notes.md")
    print(
        "nodes={nodes} diego_round1_edges={r1} final_edges={final}".format(
            nodes=len(NODES),
            r1=len({canonical(edge) for edge in round_edges("diego")}),
            final=len({canonical(edge) for edge in FINAL_EDGES}),
        )
    )


if __name__ == "__main__":
    main()
