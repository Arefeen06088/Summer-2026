from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

NODE_TEXT = """
UTIL-230A, DS-230A, SAT-1A, CB-SAT-A, EDG-1A, CB-EDG-A, GEN-1A, CB-GEN-1, BUS-13K-01, UAT-1A, CB-UAT-1A, UAT-1B, CB-UAT-1B, CB-TIE-41N, BUS-4160-N1, BUS-4160-N2, UTIL-230B, DS-230B, SAT-1B, CB-SAT-B, EDG-1B, CB-EDG-B, BUS-4160S1A, BUS-4160S1B, CB-481A, TR-480-A1, CB-LV-A1, BUS-480-A1, MCC-SAF-A1, CB-RHR-A, PUMP-RHR-A, CB-SI-A, PUMP-SI-A, CB-CCW-A, PUMP-CCW-A, CB-482A, TR-480-A2, CB-LV-A2, BUS-480-A2, MCC-SAF-A2, CB-CVC-A, PUMP-CVC-A, CB-CRF-A, FAN-CR-A, CB-COMP-A, COMP-AIR-A, CT-41A, PT-41A, RELAY-50/51A, RELAY-86A, PN-MOV-A, FU-8810A, MOV-8810A, FU-HV302A, VLV-HV-302A, FU-RCICA, MOV-RCIC-A, FU-SWA, MOV-SW-A, CB-4160-N1A, TR-480-N1A, CB-480-N1A, BUS-480-N1A, MCC-NORM-1A, PN-480-N1A, CB-CWP-1A, PUMP-CWP-1A, CB-HEAT-1A, HTR-1A, CB-AHU-1A, FAN-AHU-1A, CB-4160-N1B, TR-480-N1B, CB-480-N1B, BUS-480-N1B, MCC-NORM-1B, PN-480-N1B, CB-CWP-1B, PUMP-CWP-1B, CB-SUMP-1B, PUMP-SUMP-1B, CB-LTG-1B, PN-LTG-1B, MTR-480-N1, JB-NORM-A, RTD-PNL-A, TB-SEQ-A, TDR-SEQ-A, CB-4160-N2A, TR-480-N2A, CB-480-N2A, BUS-480-N2A, MCC-NORM-2A, PN-480-N2A, CB-CWP-2A, PUMP-CWP-2A, CB-VAC-2A, PUMP-VAC-2A, CB-AHU-2A, FAN-AHU-2A, CB-4160-N2B, TR-480-N2B, CB-480-N2B, BUS-480-N2B, MCC-NORM-2B, PN-480-N2B, CB-CWP-2B, PUMP-CWP-2B, CB-OIL-2B, PUMP-OIL-2B, CB-LTG-2B, PN-LTG-2B, MTR-480-N2, JB-NORM-B, RTD-PNL-B, TB-SEQ-B, TDR-SEQ-B, CT-41B, PT-41B, RELAY-27B, RELAY-86B, CB-481B, TR-480-B1, CB-LV-B1, BUS-480-B1, MCC-SAF-B1, CB-RHR-B, PUMP-RHR-B, CB-SI-B, PUMP-SI-B, CB-CCW-B, PUMP-CCW-B, CB-482B, TR-480-B2, CB-LV-B2, BUS-480-B2, MCC-SAF-B2, CB-CVC-B, PUMP-CVC-B, CB-CRF-B, FAN-CR-B, CB-COMP-B, COMP-AIR-B, PN-MOV-B, FU-8810B, MOV-8810B, FU-HV302B, VLV-HV-302B, FU-RCICB, MOV-RCIC-B, FU-SWB, MOV-SW-B, BAT-125A, CHG-125A, BUS-125DC-A, INV-120A, BUS-120AC-A, GND-A, PN-125A, JB-1A, JB-2A, PN-120A, PLC-ESF-A, RELAY-K1A, RELAY-K2A, ANN-ESF-A, BAT-125B, CHG-125B, BUS-125DC-B, INV-120B, BUS-120AC-B, GND-B, PN-125B, JB-1B, JB-2B, PN-120B, PLC-ESF-B, RELAY-K1B, RELAY-K2B, ANN-ESF-B
"""

DIEGO_EDGE_TEXT = """
UTIL-230A -- DS-230A
DS-230A -- SAT-1A
SAT-1A -- CB-SAT-A
CB-SAT-A -- BUS-4160S1A
EDG-1A -- CB-EDG-A
CB-EDG-A -- BUS-4160S1A
GEN-1A -- CB-GEN-1
CB-GEN-1 -- BUS-13K-01
BUS-13K-01 -- UAT-1A
UAT-1A -- CB-UAT-1A
CB-UAT-1A -- BUS-4160-N1
BUS-13K-01 -- UAT-1B
UAT-1B -- CB-UAT-1B
CB-UAT-1B -- BUS-4160-N2
BUS-4160-N1 -- CB-TIE-41N
CB-TIE-41N -- BUS-4160-N2
UTIL-230B -- DS-230B
DS-230B -- SAT-1B
SAT-1B -- CB-SAT-B
CB-SAT-B -- BUS-4160S1B
EDG-1B -- CB-EDG-B
CB-EDG-B -- BUS-4160S1B
BUS-4160S1A -- CB-481A
CB-481A -- TR-480-A1
TR-480-A1 -- CB-LV-A1
CB-LV-A1 -- BUS-480-A1
BUS-480-A1 -- MCC-SAF-A1
MCC-SAF-A1 -- CB-RHR-A
CB-RHR-A -- PUMP-RHR-A
MCC-SAF-A1 -- CB-SI-A
CB-SI-A -- PUMP-SI-A
MCC-SAF-A1 -- CB-CCW-A
CB-CCW-A -- PUMP-CCW-A
BUS-4160S1A -- CB-482A
CB-482A -- TR-480-A2
TR-480-A2 -- CB-LV-A2
CB-LV-A2 -- BUS-480-A2
BUS-480-A2 -- MCC-SAF-A2
MCC-SAF-A2 -- CB-CVC-A
CB-CVC-A -- PUMP-CVC-A
MCC-SAF-A2 -- CB-CRF-A
CB-CRF-A -- FAN-CR-A
MCC-SAF-A2 -- CB-COMP-A
CB-COMP-A -- COMP-AIR-A
FAN-CR-A -- PN-MOV-A
PN-MOV-A -- FU-8810A
FU-8810A -- MOV-8810A
PN-MOV-A -- FU-HV302A
FU-HV302A -- VLV-HV-302A
PN-MOV-A -- FU-RCICA
FU-RCICA -- MOV-RCIC-A
PN-MOV-A -- FU-SWA
FU-SWA -- MOV-SW-A
BUS-4160S1A -- CT-41A
BUS-4160S1A -- PT-41A
CT-41A -- RELAY-50/51A
PT-41A -- RELAY-50/51A
RELAY-50/51A -- RELAY-86A
CB-EDG-A -- CB-482A
CB-482A -- RELAY-50/51A
BUS-4160-N1 -- CB-4160-N1A
CB-4160-N1A -- TR-480-N1A
TR-480-N1A -- CB-480-N1A
CB-480-N1A -- BUS-480-N1A
BUS-480-N1A -- MCC-NORM-1A
MCC-NORM-1A -- PN-480-N1A
PN-480-N1A -- CB-CWP-1A
CB-CWP-1A -- PUMP-CWP-1A
PN-480-N1A -- CB-HEAT-1A
CB-HEAT-1A -- HTR-1A
PN-480-N1A -- CB-AHU-1A
CB-AHU-1A -- FAN-AHU-1A
PN-480-N1A -- PN-480-N1B
BUS-4160-N1 -- CB-4160-N1B
CB-4160-N1B -- TR-480-N1B
TR-480-N1B -- CB-480-N1B
CB-480-N1B -- BUS-480-N1B
BUS-480-N1B -- MCC-NORM-1B
MCC-NORM-1B -- PN-480-N1B
PN-480-N1B -- CB-CWP-1B
CB-CWP-1B -- PUMP-CWP-1B
PN-480-N1B -- CB-SUMP-1B
CB-SUMP-1B -- PUMP-SUMP-1B
PN-480-N1B -- CB-LTG-1B
CB-LTG-1B -- PN-LTG-1B
PUMP-SUMP-1B -- MTR-480-N1
MTR-480-N1 -- JB-NORM-A
PN-LTG-1B -- JB-NORM-A
JB-NORM-A -- RTD-PNL-A
RTD-PNL-A -- TB-SEQ-A
TB-SEQ-A -- TDR-SEQ-A
BUS-4160-N2 -- CB-4160-N2A
CB-4160-N2A -- TR-480-N2A
TR-480-N2A -- CB-480-N2A
CB-480-N2A -- BUS-480-N2A
BUS-480-N2A -- MCC-NORM-2A
MCC-NORM-2A -- PN-480-N2A
PN-480-N2A -- CB-CWP-2A
CB-CWP-2A -- PUMP-CWP-2A
PN-480-N2A -- CB-VAC-2A
CB-VAC-2A -- PUMP-VAC-2A
PN-480-N2A -- CB-AHU-2A
CB-AHU-2A -- FAN-AHU-2A
PN-480-N2A -- PN-480-N2B
BUS-4160-N2 -- CB-4160-N2B
CB-4160-N2B -- TR-480-N2B
TR-480-N2B -- CB-480-N2B
CB-480-N2B -- BUS-480-N2B
BUS-480-N2B -- MCC-NORM-2B
MCC-NORM-2B -- PN-480-N2B
PN-480-N2B -- CB-CWP-2B
CB-CWP-2B -- PUMP-CWP-2B
PN-480-N2B -- CB-OIL-2B
CB-OIL-2B -- PUMP-OIL-2B
PN-480-N2B -- CB-LTG-2B
CB-LTG-2B -- PN-LTG-2B
FAN-AHU-2A -- MTR-480-N2
MTR-480-N2 -- JB-NORM-B
JB-NORM-B -- RTD-PNL-B
RTD-PNL-B -- TB-SEQ-B
TB-SEQ-B -- TDR-SEQ-B
BUS-4160S1B -- CB-481B
CB-481B -- TR-480-B1
TR-480-B1 -- CB-LV-B1
CB-LV-B1 -- BUS-480-B1
BUS-480-B1 -- MCC-SAF-B1
MCC-SAF-B1 -- CB-RHR-B
CB-RHR-B -- PUMP-RHR-B
MCC-SAF-B1 -- CB-SI-B
CB-SI-B -- PUMP-SI-B
MCC-SAF-B1 -- CB-CCW-B
CB-CCW-B -- PUMP-CCW-B
BUS-4160S1B -- CB-482B
CB-482B -- TR-480-B2
TR-480-B2 -- CB-LV-B2
CB-LV-B2 -- BUS-480-B2
BUS-480-B2 -- MCC-SAF-B2
MCC-SAF-B2 -- CB-CVC-B
CB-CVC-B -- PUMP-CVC-B
MCC-SAF-B2 -- CB-CRF-B
CB-CRF-B -- FAN-CR-B
MCC-SAF-B2 -- CB-COMP-B
CB-COMP-B -- COMP-AIR-B
FAN-CR-B -- PN-MOV-B
PN-MOV-B -- FU-8810B
FU-8810B -- MOV-8810B
PN-MOV-B -- FU-HV302B
FU-HV302B -- VLV-HV-302B
PN-MOV-B -- FU-RCICB
FU-RCICB -- MOV-RCIC-B
PN-MOV-B -- FU-SWB
FU-SWB -- MOV-SW-B
BUS-4160S1B -- CT-41B
BUS-4160S1B -- PT-41B
CT-41B -- RELAY-27B
PT-41B -- RELAY-27B
RELAY-27B -- RELAY-86B
CB-481B -- RELAY-27B
CB-482B -- RELAY-27B
CB-482B -- CB-EDG-B
BAT-125A -- BUS-125DC-A
CHG-125A -- BUS-125DC-A
BUS-125DC-A -- INV-120A
INV-120A -- BUS-120AC-A
BUS-125DC-A -- GND-A
BUS-125DC-A -- PN-125A
BUS-120AC-A -- PN-120A
PN-125A -- JB-1A
PN-125A -- JB-2A
INV-120A -- PLC-ESF-A
PN-120A -- PLC-ESF-A
PLC-ESF-A -- RELAY-K1A
PLC-ESF-A -- RELAY-K2A
PLC-ESF-A -- ANN-ESF-A
PN-120A -- ANN-ESF-A
RELAY-K2A -- ANN-ESF-A
BAT-125B -- BUS-125DC-B
CHG-125B -- BUS-125DC-B
BUS-125DC-B -- INV-120B
INV-120B -- BUS-120AC-B
BUS-125DC-B -- GND-B
BUS-125DC-B -- PN-125B
BUS-120AC-B -- PN-120B
PN-125B -- JB-1B
PN-125B -- JB-2B
JB-2B -- PLC-ESF-B
INV-120B -- PLC-ESF-B
PN-120B -- PLC-ESF-B
PLC-ESF-B -- RELAY-K1B
PLC-ESF-B -- RELAY-K2B
PLC-ESF-B -- ANN-ESF-B
PN-120B -- ANN-ESF-B
RELAY-K2B -- ANN-ESF-B
"""

REMOVED_BY_JENNIFER = [
    ("PN-LTG-1B", "JB-NORM-A"),
    ("FAN-CR-B", "PN-MOV-B"),
    ("INV-120B", "PLC-ESF-B"),
]

ADDED_BY_JENNIFER = [
    ("MCC-SAF-B2", "PN-MOV-B"),
]

UNCERTAIN_EXCLUDED = [
    ("PN-LTG-1B", "JB-NORM-A", "Dashed vertical run passes beside PN-LTG-1B; no visible terminal contact or junction dot."),
    ("FAN-CR-B", "PN-MOV-B", "FAN-CR-B is fed from CB-CRF-B; PN-MOV-B is fed by a separate solid tap from MCC-SAF-B2."),
    ("INV-120B", "PLC-ESF-B", "B-side dashed control loop reaches PLC area without a direct INV-120B terminal."),
    ("BAT-125A", "JB-1A", "Dashed vertical path passes near/through battery area without clear battery-to-JB terminal support."),
    ("BAT-125B", "JB-1B", "Dashed vertical path passes near/through battery area without clear battery-to-JB terminal support."),
    ("JB-2A", "PLC-ESF-A", "No continuous terminal-supported dashed path from JB-2A to PLC-ESF-A."),
    ("RELAY-86A", "CB-482A", "Nearby dashed relay-control paths route around devices, but no clear direct termination at both endpoints."),
    ("RELAY-86B", "CB-481B", "Nearby dashed relay-control paths route around devices, but no clear direct termination at both endpoints."),
    ("COMP-AIR-A", "PN-MOV-A", "Dashed lines pass near MOV panel/compressor area without clear terminal contact."),
    ("COMP-AIR-B", "PN-MOV-B", "Dashed lines pass near MOV panel/compressor area without clear terminal contact."),
    ("Pump safety-load dashed trunks", "JB nodes", "Several dashed trunks cross or pass near pump symbols without component terminal endpoints or junction dots."),
    ("BUS-4160S1A/B", "BUS-4160-N1/N2", "Safety-to-normal bus crossings lack junction dots or terminal contact."),
    ("Notes/legend/title/region/overlay text", "graph nodes", "Non-component text excluded."),
]

ROUNDS = [
    ("round_01_diego_high_recall", "Diego high-recall proposal before precision pruning.", "diego"),
    ("round_02_jennifer_precision", "Jennifer precision patch applied to Diego graph.", "final"),
    ("round_03_diego_saturation", "Diego final reconciliation; Jennifer-patched graph saturated unchanged.", "final"),
]


def parse_nodes() -> list[str]:
    return [name.strip() for name in NODE_TEXT.replace("\n", " ").split(",") if name.strip()]


def parse_edges(text: str) -> list[tuple[str, str]]:
    edges = []
    for raw_line in text.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        a, b = [part.strip() for part in line.split("--", 1)]
        edges.append((a, b))
    return edges


NODES = parse_nodes()
DIEGO_EDGES = parse_edges(DIEGO_EDGE_TEXT)


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
    if len(nodes) != len(NODES):
        raise ValueError("Duplicate node names")
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
        "# Document 9 Connectivity Extraction",
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
            "Important rule applied: crossings without filled dots are not electrically connected, and note/legend/title/region/overlay text was excluded as graph nodes.",
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
