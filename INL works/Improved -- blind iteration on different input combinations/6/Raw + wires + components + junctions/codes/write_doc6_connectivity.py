from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

NODES = [
    "GEN-G201",
    "TPB-201",
    "CB-GEN-201",
    "GSU-201",
    "SWYD-BUS-A",
    "CB-GRID-A",
    "GRID-230A",
    "CB-TIE-230",
    "SWYD-BUS-B",
    "CB-GRID-B",
    "GRID-230B",
    "TR-UAT-201",
    "TR-UAT-202",
    "TR-SST-201",
    "TR-SST-202",
    "DG-EDG-201A",
    "CB-DG-A",
    "ATS-A",
    "CT-EDG-A",
    "CB-UAT-1",
    "CB-SST-1",
    "CB-UAT-2",
    "CB-SST-2",
    "BUS-6KV-A",
    "CB-TIE-6KV",
    "BUS-6KV-B",
    "PT-6KV-A",
    "PT-6KV-B",
    "DS-6KV-A",
    "DS-6KV-B",
    "BUS-4KV-N",
    "TR-480A",
    "CB-LC-A1",
    "LC-480A",
    "UV-SENS-A",
    "TR-480N",
    "CB-LC-N1",
    "LC-480N",
    "LP-N-A",
    "HTR-BLDG-A",
    "LP-N-B",
    "HTR-BLDG-B",
    "TR-480B",
    "CB-LC-B1",
    "LC-480B",
    "UV-SENS-B",
    "DG-EDG-201B",
    "CB-DG-B",
    "ATS-B",
    "CT-EDG-B",
    "MCC-CCW-A",
    "JBX-CCW-A",
    "PUMP-CCW-A",
    "MOV-CCW-201A",
    "MCC-SW-A",
    "JBX-SW-A",
    "PUMP-SW-A",
    "MCC-HPI-A",
    "PUMP-HPI-A",
    "MOV-SI-201A",
    "MCC-VENT-A",
    "FAN-CR-A",
    "MCC-CCW-B",
    "JBX-CCW-B",
    "PUMP-CCW-B",
    "MOV-CCW-201B",
    "MCC-SW-B",
    "JBX-SW-B",
    "PUMP-SW-B",
    "MCC-HPI-B",
    "PUMP-HPI-B",
    "MOV-SI-201B",
    "MCC-VENT-B",
    "FAN-CR-B",
    "AC/DC CHGR-A",
    "BAT-125A",
    "PNL-DC-A",
    "AC/DC REC-A",
    "DC/AC INV-A",
    "UPS-A",
    "AC/DC CHGR-B",
    "BAT-125B",
    "PNL-DC-B",
    "AC/DC REC-B",
    "DC/AC INV-B",
    "UPS-B",
    "PNL-INST-A",
    "PNL-INST-B",
    "CP-ESFAS-A",
    "CP-ESFAS-B",
    "PLC-RPS-A",
    "PLC-RPS-B",
    "JBX-ESF-A",
    "JBX-ESF-B",
    "RELAY-UV-A",
    "RELAY-UV-B",
    "RELAY-SI-A",
    "RELAY-SI-B",
    "RELAY-LOAD-A",
    "RELAY-LOAD-B",
    "RELAY-DG-A",
    "RELAY-DG-B",
    "GND-A",
    "GND-B",
    "GND-MAIN",
]

EDGES = [
    ("GEN-G201", "TPB-201"),
    ("TPB-201", "CB-GEN-201"),
    ("CB-GEN-201", "GSU-201"),
    ("GSU-201", "SWYD-BUS-A"),
    ("TPB-201", "TR-UAT-201"),
    ("TPB-201", "TR-UAT-202"),
    ("SWYD-BUS-A", "CB-GRID-A"),
    ("CB-GRID-A", "GRID-230A"),
    ("SWYD-BUS-A", "CB-TIE-230"),
    ("CB-TIE-230", "SWYD-BUS-B"),
    ("SWYD-BUS-B", "CB-GRID-B"),
    ("CB-GRID-B", "GRID-230B"),
    ("SWYD-BUS-A", "TR-SST-201"),
    ("SWYD-BUS-B", "TR-SST-202"),
    ("DG-EDG-201A", "CB-DG-A"),
    ("CB-DG-A", "ATS-A"),
    ("ATS-A", "BUS-6KV-A"),
    ("TR-UAT-201", "CB-UAT-1"),
    ("CB-UAT-1", "BUS-6KV-A"),
    ("TR-SST-201", "CB-SST-1"),
    ("CB-SST-1", "BUS-6KV-A"),
    ("BUS-6KV-A", "CB-TIE-6KV"),
    ("CB-TIE-6KV", "BUS-6KV-B"),
    ("TR-UAT-202", "CB-UAT-2"),
    ("CB-UAT-2", "BUS-6KV-B"),
    ("TR-SST-202", "CB-SST-2"),
    ("CB-SST-2", "BUS-6KV-B"),
    ("DG-EDG-201B", "CB-DG-B"),
    ("CB-DG-B", "ATS-B"),
    ("ATS-B", "BUS-6KV-B"),
    ("BUS-6KV-A", "PT-6KV-A"),
    ("BUS-6KV-B", "PT-6KV-B"),
    ("BUS-6KV-A", "DS-6KV-A"),
    ("DS-6KV-A", "BUS-4KV-N"),
    ("BUS-6KV-B", "DS-6KV-B"),
    ("DS-6KV-B", "BUS-4KV-N"),
    ("BUS-6KV-A", "TR-480A"),
    ("TR-480A", "CB-LC-A1"),
    ("CB-LC-A1", "LC-480A"),
    ("BUS-4KV-N", "TR-480N"),
    ("TR-480N", "CB-LC-N1"),
    ("CB-LC-N1", "LC-480N"),
    ("BUS-6KV-B", "TR-480B"),
    ("TR-480B", "CB-LC-B1"),
    ("CB-LC-B1", "LC-480B"),
    ("LC-480A", "UV-SENS-A"),
    ("LC-480B", "UV-SENS-B"),
    ("LC-480N", "LP-N-A"),
    ("LP-N-A", "HTR-BLDG-A"),
    ("LC-480N", "LP-N-B"),
    ("LP-N-B", "HTR-BLDG-B"),
    ("LC-480A", "MCC-CCW-A"),
    ("MCC-CCW-A", "JBX-CCW-A"),
    ("JBX-CCW-A", "PUMP-CCW-A"),
    ("MCC-CCW-A", "MOV-CCW-201A"),
    ("LC-480A", "MCC-SW-A"),
    ("MCC-SW-A", "JBX-SW-A"),
    ("JBX-SW-A", "PUMP-SW-A"),
    ("LC-480A", "MCC-HPI-A"),
    ("MCC-HPI-A", "PUMP-HPI-A"),
    ("MCC-HPI-A", "MOV-SI-201A"),
    ("LC-480A", "MCC-VENT-A"),
    ("MCC-VENT-A", "FAN-CR-A"),
    ("LC-480B", "MCC-CCW-B"),
    ("MCC-CCW-B", "JBX-CCW-B"),
    ("JBX-CCW-B", "PUMP-CCW-B"),
    ("MCC-CCW-B", "MOV-CCW-201B"),
    ("LC-480B", "MCC-SW-B"),
    ("MCC-SW-B", "JBX-SW-B"),
    ("JBX-SW-B", "PUMP-SW-B"),
    ("LC-480B", "MCC-HPI-B"),
    ("MCC-HPI-B", "PUMP-HPI-B"),
    ("MCC-HPI-B", "MOV-SI-201B"),
    ("LC-480B", "MCC-VENT-B"),
    ("MCC-VENT-B", "FAN-CR-B"),
    ("LC-480A", "AC/DC CHGR-A"),
    ("AC/DC CHGR-A", "BAT-125A"),
    ("AC/DC CHGR-A", "PNL-DC-A"),
    ("BAT-125A", "PNL-DC-A"),
    ("PNL-DC-A", "AC/DC REC-A"),
    ("AC/DC REC-A", "DC/AC INV-A"),
    ("DC/AC INV-A", "UPS-A"),
    ("LC-480B", "AC/DC CHGR-B"),
    ("AC/DC CHGR-B", "BAT-125B"),
    ("AC/DC CHGR-B", "PNL-DC-B"),
    ("BAT-125B", "PNL-DC-B"),
    ("PNL-DC-B", "AC/DC REC-B"),
    ("AC/DC REC-B", "DC/AC INV-B"),
    ("DC/AC INV-B", "UPS-B"),
    ("BAT-125A", "GND-A"),
    ("AC/DC REC-A", "GND-A"),
    ("BAT-125B", "GND-B"),
    ("AC/DC REC-B", "GND-B"),
    ("GND-A", "GND-MAIN"),
    ("GND-MAIN", "GND-B"),
    ("DG-EDG-201A", "CT-EDG-A"),
    ("DG-EDG-201B", "CT-EDG-B"),
    ("CT-EDG-A", "PNL-INST-A"),
    ("PT-6KV-A", "PNL-INST-A"),
    ("UV-SENS-A", "PNL-INST-A"),
    ("PNL-INST-A", "RELAY-UV-A"),
    ("CT-EDG-B", "PNL-INST-B"),
    ("PT-6KV-B", "PNL-INST-B"),
    ("UV-SENS-B", "PNL-INST-B"),
    ("PNL-INST-B", "RELAY-UV-B"),
    ("CP-ESFAS-A", "RELAY-SI-A"),
    ("CP-ESFAS-B", "RELAY-SI-B"),
    ("PLC-RPS-A", "RELAY-LOAD-A"),
    ("PLC-RPS-B", "RELAY-LOAD-B"),
    ("JBX-ESF-A", "RELAY-DG-A"),
    ("JBX-ESF-B", "RELAY-DG-B"),
    ("MOV-SI-201A", "RELAY-SI-A"),
    ("MOV-SI-201B", "RELAY-SI-B"),
    ("FAN-CR-A", "RELAY-LOAD-A"),
    ("FAN-CR-B", "RELAY-LOAD-B"),
]

UNCERTAIN_EXCLUDED = [
    ("PNL-DC-A/UPS-A", "CP-ESFAS-A/PLC-RPS-A", "Dense DC/UPS lanes enter the control bay; exact terminal endpoints are obscured."),
    ("PNL-DC-B/UPS-B", "CP-ESFAS-B/PLC-RPS-B", "Dense DC/UPS lanes enter the control bay; exact terminal endpoints are obscured."),
    ("RELAY-UV-A", "RELAY-UV-B and other relay jumpers", "Right-side loops pass near terminals but include crossings without clear dots."),
    ("CP-ESFAS-A/B or PLC-RPS-A/B", "JBX-ESF-A/B", "Vertical dashed lanes cross panel lanes without explicit junction dots at every crossing."),
    ("ATS-A/B", "ESFAS/RPS bay", "Control conductors are visible, but endpoint assignment inside bay is not visually clean."),
    ("CT-EDG-A/B", "RELAY-DG-A/B", "Signals enter the bay, but direct relay endpoints are not visually supported."),
]

ROUNDS = [
    ("round_01_diego_high_recall", "Diego high-recall extraction; Jennifer later kept all supported edges."),
    ("round_02_jennifer_precision", "Jennifer precision review; no supported edges removed or added."),
    ("round_03_diego_saturation", "Diego final reconciliation; saturation confirmed with no graph changes."),
]


def build_matrix() -> list[list[int]]:
    index = {name: i for i, name in enumerate(NODES)}
    if len(index) != len(NODES):
        raise ValueError("Duplicate node names")
    matrix = [[0 for _ in NODES] for _ in NODES]
    for a, b in EDGES:
        if a not in index or b not in index:
            raise KeyError(f"Unknown edge endpoint: {a!r}, {b!r}")
        i = index[a]
        j = index[b]
        if i == j:
            raise ValueError(f"Self-loop not expected: {a}")
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, matrix: list[list[int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component"] + NODES)
        for node, row in zip(NODES, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        writer.writerows(EDGES)


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
        "# Document 6 Connectivity Extraction",
        "",
        "Scope: blind extraction using only `Raw + wires + components + junctions` resources.",
        "",
        "Rounds:",
    ]
    for name, description in ROUNDS:
        lines.append(f"- `{name}`: {description}")
    lines.extend(
        [
            "",
            "Saturation: Jennifer kept Diego's supported graph unchanged, and Diego confirmed `SATURATED: yes` in the final reconciliation pass.",
            "",
            f"Node count: {len(NODES)}",
            f"Undirected edge count: {len(EDGES)}",
            "",
            "Important rule applied: no-dot crossings are visual crossings only; all included dashed/dot-dash/dotted links have visible terminal support.",
            "",
            "Uncertain/excluded edges are recorded in `uncertain_excluded_edges.csv`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(matrix: list[list[int]]) -> None:
    n = len(NODES)
    if any(len(row) != n for row in matrix):
        raise ValueError("Non-square matrix")
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError(f"Diagonal is nonzero at {NODES[i]}")
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"Asymmetric matrix at {NODES[i]} / {NODES[j]}")
    edge_count = sum(sum(row) for row in matrix) // 2
    if edge_count != len(set(tuple(sorted(edge)) for edge in EDGES)):
        raise ValueError("Edge count mismatch")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    matrix = build_matrix()
    validate(matrix)
    for round_name, _ in ROUNDS:
        write_matrix(RESULTS / f"{round_name}_connectivity_matrix.csv", matrix)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", matrix)
    write_edges(RESULTS / "final_edges.csv")
    write_nodes(RESULTS / "final_node_order.csv")
    write_uncertain(RESULTS / "uncertain_excluded_edges.csv")
    write_notes(RESULTS / "round_notes.md")
    print(f"nodes={len(NODES)} edges={len(EDGES)}")


if __name__ == "__main__":
    main()
