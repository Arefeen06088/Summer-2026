from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

NODES = [
    "GRID-345-01",
    "SUT-2A",
    "CB-402A",
    "BUS-4160-N2A",
    "GEN-U2",
    "UAT-2A",
    "CB-401A",
    "CB-TIE-4160",
    "UAT-2B",
    "CB-401B",
    "BUS-4160-N2B",
    "GRID-345-02",
    "SUT-2B",
    "CB-402B",
    "EDG-2A",
    "CB-EDG-A",
    "BUS-4160-S2A",
    "CT-4160A",
    "PT-4160A",
    "RELAY-50/51A",
    "RELAY-27A",
    "RELAY-86A",
    "TR-480-2A",
    "EDG-2C",
    "CB-EDG-C",
    "TR-480-N2A",
    "BUS-480-N2A",
    "DS-480-A",
    "DS-480-B",
    "TR-480-N2B",
    "BUS-480-N2B",
    "EDG-2B",
    "CB-EDG-B",
    "BUS-4160-S2B",
    "CT-4160B",
    "PT-4160B",
    "RELAY-50/51B",
    "RELAY-27B",
    "RELAY-86B",
    "TR-480-2B",
    "BUS-480-E2A",
    "MCC-2A1",
    "MCC-2A2",
    "PN-480-A",
    "GND-A",
    "CB-51A",
    "PUMP-SI-2A",
    "CB-52A",
    "PUMP-RHR-2A",
    "CB-53A",
    "PUMP-CS-2A",
    "CB-54A",
    "PUMP-CCW-2A",
    "CB-55A",
    "FAN-CRE-2A",
    "CB-56A",
    "MOV-8801A",
    "CB-57A",
    "MOV-8802A",
    "CB-58A",
    "PUMP-AF-2A",
    "MOV-8810A",
    "PUMP-CHG-2A",
    "VLV-HV-302A",
    "FAN-VENT-2A",
    "JB-2A1",
    "RELAY-K1A",
    "CB-N1",
    "CHGR-125A",
    "BAT-2A",
    "BUS-125DC-A",
    "MCC-2C",
    "FUSE-125A",
    "PN-125A",
    "INV-120A",
    "BUS-120AC-A",
    "FUSE-120A",
    "PN-120A",
    "CP-ESFAS-A",
    "CP-RPS-A",
    "BUS-480-E2B",
    "MCC-2D",
    "MCC-2B1",
    "MCC-2B2",
    "PN-480-B",
    "GND-B",
    "CB-51B",
    "PUMP-SI-2B",
    "CB-52B",
    "PUMP-RHR-2B",
    "CB-53B",
    "PUMP-CS-2B",
    "CB-54B",
    "PUMP-CCW-2B",
    "CB-55B",
    "FAN-CRE-2B",
    "CB-56B",
    "MOV-8801B",
    "CB-57B",
    "MOV-8802B",
    "CB-58B",
    "PUMP-AF-2B",
    "MOV-8810B",
    "PUMP-CHG-2B",
    "FAN-VENT-2B",
    "VLV-HV-302B",
    "JB-2B1",
    "RELAY-K1B",
    "CB-N2",
    "CHGR-125B",
    "BAT-2B",
    "BUS-125DC-B",
    "FUSE-125B",
    "PN-125B",
    "INV-120B",
    "BUS-120AC-B",
    "FUSE-120B",
    "PN-120B",
    "CP-ESFAS-B",
    "CP-RPS-B",
]

DIEGO_EDGES = [
    ("GRID-345-01", "SUT-2A"),
    ("SUT-2A", "CB-402A"),
    ("CB-402A", "BUS-4160-N2A"),
    ("GEN-U2", "UAT-2A"),
    ("GEN-U2", "UAT-2B"),
    ("UAT-2A", "CB-401A"),
    ("CB-401A", "BUS-4160-N2A"),
    ("BUS-4160-N2A", "CB-TIE-4160"),
    ("CB-TIE-4160", "BUS-4160-N2B"),
    ("UAT-2B", "CB-401B"),
    ("CB-401B", "BUS-4160-N2B"),
    ("GRID-345-02", "SUT-2B"),
    ("SUT-2B", "CB-402B"),
    ("CB-402B", "BUS-4160-N2B"),
    ("BUS-4160-N2A", "BUS-4160-S2A"),
    ("EDG-2A", "CB-EDG-A"),
    ("CB-EDG-A", "BUS-4160-S2A"),
    ("BUS-4160-S2A", "TR-480-2A"),
    ("BUS-4160-S2A", "CT-4160A"),
    ("CT-4160A", "RELAY-50/51A"),
    ("BUS-4160-S2A", "PT-4160A"),
    ("PT-4160A", "RELAY-27A"),
    ("RELAY-50/51A", "RELAY-86A"),
    ("RELAY-27A", "RELAY-86A"),
    ("RELAY-86A", "CB-401A"),
    ("RELAY-86A", "CB-EDG-A"),
    ("BUS-4160-S2A", "CB-EDG-C"),
    ("CB-EDG-C", "EDG-2C"),
    ("CB-EDG-C", "BUS-4160-S2B"),
    ("BUS-4160-N2A", "TR-480-N2A"),
    ("BUS-4160-N2B", "TR-480-N2B"),
    ("BUS-4160-N2B", "BUS-4160-S2B"),
    ("EDG-2B", "CB-EDG-B"),
    ("CB-EDG-B", "BUS-4160-S2B"),
    ("BUS-4160-S2B", "TR-480-2B"),
    ("BUS-4160-S2B", "CT-4160B"),
    ("CT-4160B", "RELAY-50/51B"),
    ("BUS-4160-S2B", "PT-4160B"),
    ("PT-4160B", "RELAY-27B"),
    ("RELAY-50/51B", "RELAY-86B"),
    ("RELAY-27B", "RELAY-86B"),
    ("RELAY-86B", "CB-401B"),
    ("RELAY-86B", "CB-EDG-B"),
    ("TR-480-2A", "BUS-480-E2A"),
    ("TR-480-N2A", "BUS-480-N2A"),
    ("BUS-480-N2A", "BUS-480-E2A"),
    ("BUS-480-E2A", "DS-480-A"),
    ("DS-480-A", "DS-480-B"),
    ("DS-480-B", "BUS-480-E2B"),
    ("TR-480-N2B", "BUS-480-N2B"),
    ("BUS-480-N2B", "BUS-480-E2B"),
    ("TR-480-2B", "BUS-480-E2B"),
    ("BUS-480-E2A", "GND-A"),
    ("BUS-480-E2B", "GND-B"),
    ("BUS-480-E2A", "MCC-2A1"),
    ("MCC-2A1", "CB-51A"),
    ("CB-51A", "PUMP-SI-2A"),
    ("MCC-2A1", "CB-52A"),
    ("CB-52A", "PUMP-RHR-2A"),
    ("MCC-2A1", "CB-53A"),
    ("CB-53A", "PUMP-CS-2A"),
    ("MCC-2A1", "CB-54A"),
    ("CB-54A", "PUMP-CCW-2A"),
    ("BUS-480-E2A", "MCC-2A2"),
    ("MCC-2A2", "CB-55A"),
    ("CB-55A", "FAN-CRE-2A"),
    ("MCC-2A2", "CB-56A"),
    ("CB-56A", "MOV-8801A"),
    ("MCC-2A2", "CB-57A"),
    ("CB-57A", "MOV-8802A"),
    ("MCC-2A2", "CB-58A"),
    ("CB-58A", "PUMP-AF-2A"),
    ("BUS-480-E2A", "PN-480-A"),
    ("PN-480-A", "MOV-8810A"),
    ("PN-480-A", "PUMP-CHG-2A"),
    ("PUMP-CHG-2A", "VLV-HV-302A"),
    ("BUS-480-N2A", "CB-N1"),
    ("CB-N1", "CHGR-125A"),
    ("CHGR-125A", "BAT-2A"),
    ("CHGR-125A", "BUS-125DC-A"),
    ("BAT-2A", "BUS-125DC-A"),
    ("BUS-125DC-A", "MCC-2C"),
    ("MCC-2C", "FAN-VENT-2A"),
    ("BUS-125DC-A", "FUSE-125A"),
    ("FUSE-125A", "PN-125A"),
    ("BUS-125DC-A", "INV-120A"),
    ("INV-120A", "BUS-120AC-A"),
    ("BUS-120AC-A", "FUSE-120A"),
    ("FUSE-120A", "PN-120A"),
    ("PN-125A", "CP-ESFAS-A"),
    ("PN-120A", "CP-RPS-A"),
    ("FAN-VENT-2A", "CP-ESFAS-A"),
    ("MOV-8801A", "JB-2A1"),
    ("JB-2A1", "CP-ESFAS-A"),
    ("RELAY-K1A", "CP-ESFAS-A"),
    ("CB-51A", "RELAY-K1A"),
    ("CB-52A", "RELAY-K1A"),
    ("CB-53A", "RELAY-K1A"),
    ("BUS-480-E2B", "MCC-2B1"),
    ("MCC-2B1", "CB-51B"),
    ("CB-51B", "PUMP-SI-2B"),
    ("MCC-2B1", "CB-52B"),
    ("CB-52B", "PUMP-RHR-2B"),
    ("MCC-2B1", "CB-53B"),
    ("CB-53B", "PUMP-CS-2B"),
    ("MCC-2B1", "CB-54B"),
    ("CB-54B", "PUMP-CCW-2B"),
    ("BUS-480-E2B", "MCC-2B2"),
    ("MCC-2B2", "CB-55B"),
    ("CB-55B", "FAN-CRE-2B"),
    ("MCC-2B2", "CB-56B"),
    ("CB-56B", "MOV-8801B"),
    ("MCC-2B2", "CB-57B"),
    ("CB-57B", "MOV-8802B"),
    ("MCC-2B2", "CB-58B"),
    ("CB-58B", "PUMP-AF-2B"),
    ("BUS-480-E2B", "PN-480-B"),
    ("BUS-480-N2B", "CB-N2"),
    ("CB-N2", "MCC-2D"),
    ("MCC-2D", "PUMP-CHG-2B"),
    ("MCC-2D", "FAN-VENT-2B"),
    ("PN-480-B", "CHGR-125B"),
    ("PN-480-B", "MOV-8810B"),
    ("CHGR-125B", "BAT-2B"),
    ("CHGR-125B", "BUS-125DC-B"),
    ("BAT-2B", "BUS-125DC-B"),
    ("BUS-125DC-B", "FUSE-125B"),
    ("FUSE-125B", "PN-125B"),
    ("BUS-125DC-B", "INV-120B"),
    ("INV-120B", "BUS-120AC-B"),
    ("BUS-120AC-B", "FUSE-120B"),
    ("FUSE-120B", "PN-120B"),
    ("PN-125B", "VLV-HV-302B"),
    ("VLV-HV-302B", "PN-120B"),
    ("PN-125B", "CP-ESFAS-B"),
    ("PN-120B", "CP-RPS-B"),
    ("MOV-8810B", "CP-ESFAS-B"),
    ("RELAY-K1B", "CP-ESFAS-B"),
    ("CB-51B", "RELAY-K1B"),
    ("CB-52B", "RELAY-K1B"),
    ("CB-53B", "RELAY-K1B"),
    ("CB-54B", "RELAY-K1B"),
    ("MOV-8801B", "JB-2B1"),
    ("PUMP-AF-2B", "JB-2B1"),
]

REMOVED_BY_JENNIFER = [
    ("BUS-4160-N2A", "TR-480-N2A"),
    ("BUS-4160-N2B", "TR-480-N2B"),
    ("BUS-480-N2A", "BUS-480-E2A"),
    ("BUS-480-N2B", "BUS-480-E2B"),
    ("BUS-125DC-A", "MCC-2C"),
    ("FAN-VENT-2A", "CP-ESFAS-A"),
    ("JB-2A1", "CP-ESFAS-A"),
    ("PN-125B", "VLV-HV-302B"),
    ("CB-54B", "RELAY-K1B"),
]

ADDED_BY_JENNIFER = [
    ("BUS-4160-S2A", "TR-480-N2A"),
    ("BUS-4160-S2B", "TR-480-N2B"),
    ("CB-N1", "MCC-2C"),
    ("PN-125A", "BUS-120AC-A"),
    ("PN-125B", "BUS-120AC-B"),
]

UNCERTAIN_EXCLUDED = [
    ("BUS-480-N2A", "BUS-480-E2A", "Vertical N2 drop crosses the E2/DS tie level without a filled junction dot."),
    ("BUS-480-N2B", "BUS-480-E2B", "Vertical N2 drop crosses the E2/DS tie level without a filled junction dot."),
    ("BUS-480-N2A", "DS-480-A", "DS-480-A is on the E2A/E2B feeder-tie conductor, not terminal-supported to the N2 bus."),
    ("BUS-480-N2B", "DS-480-B", "DS-480-B is on the E2A/E2B feeder-tie conductor, not terminal-supported to the N2 bus."),
    ("CB-54A", "RELAY-K1A", "K1A dashed relay inputs visibly support CB-51A/52A/53A, not CB-54A."),
    ("CB-54B", "RELAY-K1B", "K1B dashed relay inputs visibly support CB-51B/52B/53B, not CB-54B."),
    ("JB-2A1", "CP-ESFAS-A", "JB path has local dashed endpoints but no clear terminal-supported CP-ESFAS-A endpoint."),
    ("JB-2B1", "RELAY-K1B", "B-side JB continuation to K1B is not terminal-supported."),
    ("JB-2B1", "CP-ESFAS-B", "B-side JB continuation to CP-ESFAS-B is not terminal-supported."),
    ("FAN-VENT-2A", "CP-ESFAS-A", "Nearby dashed route passes by; no clear filled junction or terminal endpoint."),
    ("PN-125B", "VLV-HV-302B", "VLV-HV-302B is on the PN-120B/FUSE-120B path while PN-125B path runs separately."),
    ("Cable IDs / terminal blocks / title text", "graph nodes", "Annotations such as TB01-TB15 and cable labels were not components."),
]

ROUNDS = [
    ("round_01_diego_high_recall", "Diego high-recall proposal before precision pruning.", "diego"),
    ("round_02_jennifer_precision", "Jennifer precision patch applied to Diego graph.", "final"),
    ("round_03_diego_saturation", "Diego final reconciliation; Jennifer-patched graph saturated unchanged.", "final"),
]


def canonical(edge: tuple[str, str]) -> tuple[str, str]:
    return tuple(sorted(edge))


def final_edges() -> list[tuple[str, str]]:
    removed = {canonical(edge) for edge in REMOVED_BY_JENNIFER}
    edges = [edge for edge in DIEGO_EDGES if canonical(edge) not in removed]
    edges.extend(ADDED_BY_JENNIFER)
    return edges


def edges_for(kind: str) -> list[tuple[str, str]]:
    if kind == "diego":
        return DIEGO_EDGES
    if kind == "final":
        return final_edges()
    raise ValueError(f"Unknown graph kind: {kind}")


def validate_edges(edges: list[tuple[str, str]]) -> None:
    nodes = set(NODES)
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        a, b = edge
        if a not in nodes or b not in nodes:
            raise KeyError(f"Unknown endpoint: {edge}")
        if a == b:
            raise ValueError(f"Self-loop not expected: {edge}")
        key = canonical(edge)
        if key in seen:
            raise ValueError(f"Duplicate edge: {edge}")
        seen.add(key)


def build_matrix(edges: list[tuple[str, str]]) -> list[list[int]]:
    validate_edges(edges)
    index = {name: i for i, name in enumerate(NODES)}
    if len(index) != len(NODES):
        raise ValueError("Duplicate node names")
    matrix = [[0 for _ in NODES] for _ in NODES]
    for a, b in edges:
        i = index[a]
        j = index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def validate_matrix(matrix: list[list[int]], edges: list[tuple[str, str]]) -> None:
    n = len(NODES)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Non-square matrix")
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError(f"Diagonal is nonzero at {NODES[i]}")
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"Asymmetric matrix at {NODES[i]} / {NODES[j]}")
    actual = sum(sum(row) for row in matrix) // 2
    expected = len({canonical(edge) for edge in edges})
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
        "# Document 8 Connectivity Extraction",
        "",
        "Scope: blind extraction using only `Raw + wires + components + junctions` resources.",
        "",
        "Rounds:",
    ]
    for round_name, description, kind in ROUNDS:
        count = len({canonical(edge) for edge in edges_for(kind)})
        lines.append(f"- `{round_name}`: {description} Edge count: {count}.")
    lines.extend(
        [
            "",
            "Saturation: Jennifer corrected Diego's high-recall graph; Diego agreed with the patch in round 3.",
            "",
            f"Node count: {len(NODES)}",
            f"Final undirected edge count: {len({canonical(edge) for edge in final_edges()})}",
            "",
            "Important rule applied: crossings without filled dots are not electrically connected, and cable/table/title text was excluded as graph nodes.",
            "",
            "Precision changes:",
        ]
    )
    for edge in REMOVED_BY_JENNIFER:
        lines.append(f"- Removed `{edge[0]} -- {edge[1]}`.")
    for edge in ADDED_BY_JENNIFER:
        lines.append(f"- Added `{edge[0]} -- {edge[1]}`.")
    lines.extend(["", "Uncertain/excluded candidates are recorded in `uncertain_excluded_edges.csv`."])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for round_name, _, kind in ROUNDS:
        edges = edges_for(kind)
        matrix = build_matrix(edges)
        validate_matrix(matrix, edges)
        write_matrix(RESULTS / f"{round_name}_connectivity_matrix.csv", matrix)
        write_edges(RESULTS / f"{round_name}_edges.csv", edges)

    final = final_edges()
    final_matrix = build_matrix(final)
    validate_matrix(final_matrix, final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_matrix)
    write_edges(RESULTS / "final_edges.csv", final)
    write_nodes(RESULTS / "final_node_order.csv")
    write_uncertain(RESULTS / "uncertain_excluded_edges.csv")
    write_notes(RESULTS / "round_notes.md")
    print(
        "nodes={nodes} diego_round1_edges={r1} final_edges={final}".format(
            nodes=len(NODES),
            r1=len({canonical(edge) for edge in DIEGO_EDGES}),
            final=len({canonical(edge) for edge in final}),
        )
    )


if __name__ == "__main__":
    main()
