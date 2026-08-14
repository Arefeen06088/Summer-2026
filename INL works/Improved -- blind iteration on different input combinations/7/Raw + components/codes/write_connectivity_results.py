from __future__ import annotations

import csv
import math
import os
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + components")
RESULTS = BASE / "results"


NODES = [
    "GEN-G01",
    "ISO-GEN-1",
    "CB-GEN-A",
    "BUS-13A",
    "CB-TIE-13",
    "BUS-13B",
    "OFFSITE-345",
    "DS-SAT-1",
    "TR-SAT-A",
    "CB-SAT-A",
    "TR-SAT-B",
    "CB-SAT-B",
    "TR-UAT-A",
    "CB-UAT-A",
    "TR-UAT-B",
    "CB-UAT-B",
    "DG-1A",
    "CB-DG-A",
    "DG-1B",
    "CB-DG-B",
    "BUS-4A",
    "CB-TIE-4",
    "BUS-4B",
    "CB-480A",
    "TR-480A",
    "LC-480A",
    "CB-480B",
    "TR-480B",
    "LC-480B",
    "CB-480C",
    "TR-480C",
    "LC-480C",
    "CB-480D",
    "TR-480D",
    "LC-480D",
    "CB-MCC-A1",
    "MCC-A1",
    "CB-MCC-A2",
    "MCC-A2",
    "CB-MCC-B1",
    "MCC-B1",
    "CB-MCC-B2",
    "MCC-B2",
    "CB-MCC-C1",
    "MCC-C1",
    "CB-MCC-C2",
    "MCC-C2",
    "CB-MCC-D1",
    "MCC-D1",
    "CB-MCC-D2",
    "MCC-D2",
    "CB-P201A",
    "PUMP-P201A",
    "CB-MOV101A",
    "MOV-101A",
    "CB-FAN101A",
    "FAN-F101A",
    "CB-P202A",
    "PUMP-P202A",
    "CB-MOV102A",
    "MOV-102A",
    "CB-HTR101A",
    "HTR-H101A",
    "CB-P201B",
    "PUMP-P201B",
    "CB-MOV101B",
    "MOV-101B",
    "CB-FAN101B",
    "FAN-F101B",
    "CB-P202B",
    "PUMP-P202B",
    "CB-MOV102B",
    "MOV-102B",
    "CB-HTR101B",
    "HTR-H101B",
    "CB-P301A",
    "PUMP-P301A",
    "CB-MOV201A",
    "MOV-201A",
    "CB-FAN201A",
    "FAN-F201A",
    "CB-P302A",
    "PUMP-P302A",
    "CB-MOV202A",
    "MOV-202A",
    "CB-HTR201A",
    "HTR-H201A",
    "CB-P301B",
    "PUMP-P301B",
    "CB-MOV201B",
    "MOV-201B",
    "CB-FAN201B",
    "FAN-F201B",
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


DIEGO_ROUND1_EDGES = [
    ("GEN-G01", "ISO-GEN-1", "solid_power", "Generator symbol connects directly to generator isolator."),
    ("ISO-GEN-1", "CB-GEN-A", "solid_power", "Isolator output connects to generator breaker."),
    ("CB-GEN-A", "BUS-13A", "solid_power", "Generator breaker vertical feeder lands on BUS-13A."),
    ("BUS-13A", "CB-TIE-13", "solid_bus_tie", "BUS-13A right end enters 13 kV tie breaker."),
    ("CB-TIE-13", "BUS-13B", "solid_bus_tie", "13 kV tie breaker output enters BUS-13B."),
    ("OFFSITE-345", "DS-SAT-1", "solid_power", "Offsite source connects to station auxiliary disconnect."),
    ("DS-SAT-1", "TR-SAT-A", "solid_power", "Disconnect lower/right terminal feeds TR-SAT-A."),
    ("TR-SAT-A", "CB-SAT-A", "solid_power", "TR-SAT-A secondary connects to SAT breaker A."),
    ("CB-SAT-A", "BUS-4A", "solid_power", "SAT breaker A lands on BUS-4A."),
    ("DS-SAT-1", "TR-SAT-B", "solid_power", "Disconnect top/right feeder continues across to TR-SAT-B."),
    ("TR-SAT-B", "CB-SAT-B", "solid_power", "TR-SAT-B secondary connects to SAT breaker B."),
    ("CB-SAT-B", "BUS-4B", "solid_power", "SAT breaker B lands on BUS-4B."),
    ("BUS-13A", "CB-UAT-A", "solid_power", "BUS-13A tap feeds UAT breaker A."),
    ("CB-UAT-A", "TR-UAT-A", "solid_power", "UAT breaker A connects to TR-UAT-A."),
    ("TR-UAT-A", "BUS-4A", "solid_power", "TR-UAT-A secondary lands on BUS-4A."),
    ("BUS-13B", "CB-UAT-B", "solid_power", "BUS-13B tap feeds UAT breaker B."),
    ("CB-UAT-B", "TR-UAT-B", "solid_power", "UAT breaker B connects to TR-UAT-B."),
    ("TR-UAT-B", "BUS-4B", "solid_power", "TR-UAT-B secondary lands on BUS-4B."),
    ("DG-1A", "CB-DG-A", "solid_power", "Diesel generator A connects to DG breaker A."),
    ("CB-DG-A", "BUS-4A", "solid_power", "DG breaker A lands on BUS-4A."),
    ("DG-1B", "CB-DG-B", "solid_power", "Diesel generator B connects to DG breaker B."),
    ("CB-DG-B", "BUS-4B", "solid_power", "DG breaker B lands on BUS-4B."),
    ("BUS-4A", "CB-TIE-4", "solid_bus_tie", "BUS-4A right end enters 4.16 kV tie breaker."),
    ("CB-TIE-4", "BUS-4B", "solid_bus_tie", "4.16 kV tie breaker output enters BUS-4B."),
    ("BUS-4A", "CB-480A", "solid_power", "BUS-4A feeder 4A-FDR-A drops to CB-480A."),
    ("CB-480A", "TR-480A", "solid_power", "CB-480A feeds transformer 480A."),
    ("TR-480A", "LC-480A", "solid_power", "Transformer 480A lands on LC-480A."),
    ("BUS-4A", "CB-480B", "solid_power", "BUS-4A feeder 4A-FDR-B drops to CB-480B."),
    ("CB-480B", "TR-480B", "solid_power", "CB-480B feeds transformer 480B."),
    ("TR-480B", "LC-480B", "solid_power", "Transformer 480B lands on LC-480B."),
    ("BUS-4B", "CB-480C", "solid_power", "BUS-4B feeder 4B-FDR-C drops to CB-480C."),
    ("CB-480C", "TR-480C", "solid_power", "CB-480C feeds transformer 480C."),
    ("TR-480C", "LC-480C", "solid_power", "Transformer 480C lands on LC-480C."),
    ("BUS-4B", "CB-480D", "solid_power", "BUS-4B feeder 4B-FDR-D drops to CB-480D."),
    ("CB-480D", "TR-480D", "solid_power", "CB-480D feeds transformer 480D."),
    ("TR-480D", "LC-480D", "solid_power", "Transformer 480D lands on LC-480D."),
    ("LC-480A", "CB-MCC-A1", "solid_power", "LC-480A left drop feeds MCC breaker A1."),
    ("CB-MCC-A1", "MCC-A1", "solid_power", "MCC breaker A1 lands on MCC-A1."),
    ("LC-480A", "CB-MCC-A2", "solid_power", "LC-480A right drop feeds MCC breaker A2."),
    ("CB-MCC-A2", "MCC-A2", "solid_power", "MCC breaker A2 lands on MCC-A2."),
    ("LC-480B", "CB-MCC-B1", "solid_power", "LC-480B left drop feeds MCC breaker B1."),
    ("CB-MCC-B1", "MCC-B1", "solid_power", "MCC breaker B1 lands on MCC-B1."),
    ("LC-480B", "CB-MCC-B2", "solid_power", "LC-480B right drop feeds MCC breaker B2."),
    ("CB-MCC-B2", "MCC-B2", "solid_power", "MCC breaker B2 lands on MCC-B2."),
    ("LC-480C", "CB-MCC-C1", "solid_power", "LC-480C left drop feeds MCC breaker C1."),
    ("CB-MCC-C1", "MCC-C1", "solid_power", "MCC breaker C1 lands on MCC-C1."),
    ("LC-480C", "CB-MCC-C2", "solid_power", "LC-480C right drop feeds MCC breaker C2."),
    ("CB-MCC-C2", "MCC-C2", "solid_power", "MCC breaker C2 lands on MCC-C2."),
    ("LC-480D", "CB-MCC-D1", "solid_power", "LC-480D left drop feeds MCC breaker D1."),
    ("CB-MCC-D1", "MCC-D1", "solid_power", "MCC breaker D1 lands on MCC-D1."),
    ("LC-480D", "CB-MCC-D2", "solid_power", "LC-480D center drop feeds MCC breaker D2."),
    ("CB-MCC-D2", "MCC-D2", "solid_power", "MCC breaker D2 lands on MCC-D2."),
    ("MCC-A1", "CB-P201A", "solid_power", "MCC-A1 left branch feeds pump breaker P201A."),
    ("CB-P201A", "PUMP-P201A", "solid_power", "Breaker P201A feeds pump P201A."),
    ("MCC-A1", "CB-MOV101A", "solid_power", "MCC-A1 center branch feeds MOV breaker 101A."),
    ("CB-MOV101A", "MOV-101A", "solid_power", "MOV breaker 101A feeds MOV-101A."),
    ("MCC-A1", "CB-FAN101A", "solid_power", "MCC-A1 right branch feeds fan breaker 101A."),
    ("CB-FAN101A", "FAN-F101A", "solid_power", "Fan breaker 101A feeds FAN-F101A."),
    ("MCC-A2", "CB-P202A", "solid_power", "MCC-A2 left branch feeds pump breaker P202A."),
    ("CB-P202A", "PUMP-P202A", "solid_power", "Breaker P202A feeds pump P202A."),
    ("MCC-A2", "CB-MOV102A", "solid_power", "MCC-A2 center branch feeds MOV breaker 102A."),
    ("CB-MOV102A", "MOV-102A", "solid_power", "MOV breaker 102A feeds MOV-102A."),
    ("MCC-A2", "CB-HTR101A", "solid_power", "MCC-A2 right branch feeds heater breaker 101A."),
    ("CB-HTR101A", "HTR-H101A", "solid_power", "Heater breaker 101A feeds HTR-H101A."),
    ("MCC-B1", "CB-P201B", "solid_power", "MCC-B1 left branch feeds pump breaker P201B."),
    ("CB-P201B", "PUMP-P201B", "solid_power", "Breaker P201B feeds pump P201B."),
    ("MCC-B1", "CB-MOV101B", "solid_power", "MCC-B1 center branch feeds MOV breaker 101B."),
    ("CB-MOV101B", "MOV-101B", "solid_power", "MOV breaker 101B feeds MOV-101B."),
    ("MCC-B1", "CB-FAN101B", "solid_power", "MCC-B1 right branch feeds fan breaker 101B."),
    ("CB-FAN101B", "FAN-F101B", "solid_power", "Fan breaker 101B feeds FAN-F101B."),
    ("MCC-B2", "CB-P202B", "solid_power", "MCC-B2 left branch feeds pump breaker P202B."),
    ("CB-P202B", "PUMP-P202B", "solid_power", "Breaker P202B feeds pump P202B."),
    ("MCC-B2", "CB-MOV102B", "solid_power", "MCC-B2 center branch feeds MOV breaker 102B."),
    ("CB-MOV102B", "MOV-102B", "solid_power", "MOV breaker 102B feeds MOV-102B."),
    ("MCC-B2", "CB-HTR101B", "solid_power", "MCC-B2 right branch feeds heater breaker 101B."),
    ("CB-HTR101B", "HTR-H101B", "solid_power", "Heater breaker 101B feeds HTR-H101B."),
    ("MCC-C1", "CB-P301A", "solid_power", "MCC-C1 left branch feeds pump breaker P301A."),
    ("CB-P301A", "PUMP-P301A", "solid_power", "Breaker P301A feeds pump P301A."),
    ("MCC-C1", "CB-MOV201A", "solid_power", "MCC-C1 center branch feeds MOV breaker 201A."),
    ("CB-MOV201A", "MOV-201A", "solid_power", "MOV breaker 201A feeds MOV-201A."),
    ("MCC-C1", "CB-FAN201A", "solid_power", "MCC-C1 right branch feeds fan breaker 201A."),
    ("CB-FAN201A", "FAN-F201A", "solid_power", "Fan breaker 201A feeds FAN-F201A."),
    ("MCC-C2", "CB-P302A", "solid_power", "MCC-C2 left branch feeds pump breaker P302A."),
    ("CB-P302A", "PUMP-P302A", "solid_power", "Breaker P302A feeds pump P302A."),
    ("MCC-C2", "CB-MOV202A", "solid_power", "MCC-C2 center branch feeds MOV breaker 202A."),
    ("CB-MOV202A", "MOV-202A", "solid_power", "MOV breaker 202A feeds MOV-202A."),
    ("MCC-C2", "CB-HTR201A", "solid_power", "MCC-C2 right branch feeds heater breaker 201A."),
    ("CB-HTR201A", "HTR-H201A", "solid_power", "Heater breaker 201A feeds HTR-H201A."),
    ("MCC-D1", "CB-P301B", "solid_power", "MCC-D1 left branch feeds pump breaker P301B."),
    ("CB-P301B", "PUMP-P301B", "solid_power", "Breaker P301B feeds pump P301B."),
    ("MCC-D1", "CB-MOV201B", "solid_power", "MCC-D1 center branch feeds MOV breaker 201B."),
    ("CB-MOV201B", "MOV-201B", "solid_power", "MOV breaker 201B feeds MOV-201B."),
    ("MCC-D1", "CB-FAN201B", "solid_power", "MCC-D1 right branch feeds fan breaker 201B."),
    ("CB-FAN201B", "FAN-F201B", "solid_power", "Fan breaker 201B feeds FAN-F201B."),
    ("MCC-D2", "CB-P302B", "solid_power", "MCC-D2 left branch feeds pump breaker P302B."),
    ("CB-P302B", "PUMP-P302B", "solid_power", "Breaker P302B feeds pump P302B."),
    ("MCC-D2", "CB-MOV202B", "solid_power", "MCC-D2 center branch feeds MOV breaker 202B."),
    ("CB-MOV202B", "MOV-202B", "solid_power", "MOV breaker 202B feeds MOV-202B."),
    ("MCC-D2", "CB-HTR201B", "solid_power", "MCC-D2 right branch feeds heater breaker 201B."),
    ("CB-HTR201B", "HTR-H201B", "solid_power", "Heater breaker 201B feeds HTR-H201B."),
    ("BAT-125A", "BUS-125DCA", "solid_dc", "Battery A bottom terminal lands on BUS-125DCA."),
    ("BAT-125A", "BCHG-125A", "solid_dc", "Train A battery and charger share a visible solid terminal conductor."),
    ("BCHG-125A", "BUS-125DCA", "solid_dc", "Charger A bottom terminal lands on BUS-125DCA."),
    ("BUS-125DCA", "INV-120A", "solid_dc", "BUS-125DCA tap feeds inverter A."),
    ("BUS-125DCA", "PPS-A", "solid_dc", "BUS-125DCA tap feeds PPS-A."),
    ("INV-120A", "UPS-120A", "dashed_control", "Dashed terminal line connects inverter A to UPS A."),
    ("UPS-120A", "PNL-AC-CR1", "dashed_control", "Dashed terminal line connects UPS A to AC panel CR1."),
    ("PNL-AC-CR1", "PPS-A", "dashed_control", "Dashed terminal line connects panel CR1 to PPS-A."),
    ("UPS-120A", "ANN-101", "dashed_control", "Vertical dashed line from UPS A terminal drops to ANN-101."),
    ("ANN-101", "RELAY-K101", "dashed_control", "ANN-101 right terminal has dashed line to relay K101."),
    ("PPS-A", "RELAY-K101", "dashed_control", "PPS-A lower dashed path lands on relay K101."),
    ("PPS-A", "RELAY-K102", "dashed_control", "PPS-A lower dashed path lands on relay K102."),
    ("BAT-125B", "BUS-125DCB", "solid_dc", "Battery B bottom terminal lands on BUS-125DCB."),
    ("BCHG-125B", "BUS-125DCB", "solid_dc", "Charger B bottom terminal lands on BUS-125DCB."),
    ("BUS-125DCB", "INV-120B", "solid_dc", "BUS-125DCB tap feeds inverter B."),
    ("BUS-125DCB", "PPS-B", "solid_dc", "BUS-125DCB tap feeds PPS-B."),
    ("INV-120B", "UPS-120B", "dashed_control", "Dashed terminal line connects inverter B to UPS B."),
    ("UPS-120B", "PNL-AC-CR2", "dashed_control", "Dashed terminal line connects UPS B to AC panel CR2."),
    ("PNL-AC-CR2", "PPS-B", "dashed_control", "Dashed terminal line connects panel CR2 to PPS-B."),
    ("UPS-120B", "ANN-201", "dashed_control", "Vertical dashed line from UPS B terminal drops to ANN-201."),
    ("ANN-201", "RELAY-K201", "dashed_control", "ANN-201 right terminal has dashed line to relay K201."),
    ("PPS-B", "RELAY-K201", "dashed_control", "PPS-B lower dashed path lands on relay K201."),
    ("PPS-B", "RELAY-K202", "dashed_control", "PPS-B lower dashed path lands on relay K202."),
]


PROMOTED_AFTER_REVIEW = [
    ("LC-480A", "BAT-125A", "solid_power", "Jennifer and Diego R2 promoted: solid feeder from LC-480A region lands on BAT-125A terminal."),
    ("LC-480D", "BCHG-125B", "solid_power", "Jennifer and Diego R2 promoted: solid feeder from LC-480D right side lands on BCHG-125B right terminal."),
]


FINAL_EDGES = DIEGO_ROUND1_EDGES + PROMOTED_AFTER_REVIEW


UNCERTAIN_EDGES = [
    ("PNL-AC-CR1", "RELAY-K101", "Nearby vertical dashed conductors, but terminal ownership is unclear."),
    ("PNL-AC-CR2", "RELAY-K201", "Nearby vertical dashed conductors, but terminal ownership is unclear."),
    ("ANN-101", "PPS-A", "Diagonal dotted/sensing path visible, but endpoint semantics are ambiguous."),
    ("ANN-201", "PPS-B", "Diagonal dotted/sensing path visible, but endpoint semantics are ambiguous."),
    ("ANN-101", "SR-101", "Bottom cross-train dashed route approaches SR-101, but exact terminal ownership is unclear."),
    ("SR-101", "ANN-201", "Bottom cross-train dashed route approaches SR-101, but exact terminal ownership is unclear."),
    ("RELAY-K101", "RELAY-K102", "Plausible dashed interlock in congested area; not asserted without clear terminal-to-terminal ownership."),
    ("RELAY-K201", "RELAY-K202", "Plausible dashed interlock in congested area; not asserted without clear terminal-to-terminal ownership."),
    ("RELAY-K102", "SR-101", "Plausible dashed interlock/cross-train path; held uncertain."),
    ("RELAY-K202", "SR-101", "Plausible dashed interlock/cross-train path; held uncertain."),
    ("MCC/load devices", "CTRL-RACEWAY-A/B", "Dashed raceway paths are visually present but are routing regions, not safe component-to-component edges."),
]


REJECTED_EDGES = [
    ("LC-480A", "BCHG-125A", "No direct terminal; reviewed solid line lands on BAT-125A, while BCHG-125A separately ties to BAT-125A and BUS-125DCA."),
    ("BAT-125B", "BCHG-125B", "No direct battery-to-charger conductor is visible on Train B."),
    ("CTRL-RACEWAY-A", "matrix node", "Raceway label is a routing region, not a component/logical bus node in the asserted matrix."),
    ("CTRL-RACEWAY-B", "matrix node", "Raceway label is a routing region, not a component/logical bus node in the asserted matrix."),
    ("TRAIN-A/B area titles", "matrix nodes", "Area titles and green region boxes are not asserted as connectivity nodes."),
]


ROUND_EDGE_SETS = {
    "diego_round1": DIEGO_ROUND1_EDGES,
    "jennifer_round1": FINAL_EDGES,
    "diego_round2": FINAL_EDGES,
    "jennifer_round2_final": FINAL_EDGES,
    "final": FINAL_EDGES,
}


def normalize_edge(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def validate_edges(edges: list[tuple[str, str, str, str]]) -> None:
    nodes = set(NODES)
    seen: set[tuple[str, str]] = set()
    for source, target, *_ in edges:
        if source not in nodes:
            raise ValueError(f"Unknown source node: {source}")
        if target not in nodes:
            raise ValueError(f"Unknown target node: {target}")
        if source == target:
            raise ValueError(f"Self-loop not justified: {source}")
        key = normalize_edge(source, target)
        if key in seen:
            raise ValueError(f"Duplicate undirected edge: {source}--{target}")
        seen.add(key)


def adjacency(edges: list[tuple[str, str, str, str]]) -> dict[str, set[str]]:
    graph = {node: set() for node in NODES}
    for source, target, *_ in edges:
        graph[source].add(target)
        graph[target].add(source)
    return graph


def write_edge_csv(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "evidence_type", "evidence"])
        for source, target, evidence_type, evidence in edges:
            writer.writerow([source, target, evidence_type, evidence])


def write_matrix_csv(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    graph = adjacency(edges)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component"] + NODES)
        for row_node in NODES:
            writer.writerow([row_node] + [1 if col_node in graph[row_node] else 0 for col_node in NODES])


def validate_matrix(edges: list[tuple[str, str, str, str]]) -> None:
    graph = adjacency(edges)
    for node in NODES:
        if node in graph[node]:
            raise ValueError(f"Diagonal/self-loop is nonzero for {node}")
        for other in NODES:
            if (other in graph[node]) != (node in graph[other]):
                raise ValueError(f"Asymmetric adjacency: {node}, {other}")
            value = 1 if other in graph[node] else 0
            if value not in (0, 1):
                raise ValueError(f"Non-binary value for {node}, {other}")


def write_uncertain_and_rejected() -> None:
    with (RESULTS / "final_uncertain_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(UNCERTAIN_EDGES)

    with (RESULTS / "final_rejected_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target_or_category", "reason"])
        writer.writerows(REJECTED_EDGES)


def write_round_summaries() -> None:
    text = f"""# Document 7 Round Summaries

Resource folder: `{BASE}`

Allowed visual resources used:
- `raw -- synthetic_npp_electrical_schematic_clean (1).png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | 120 | 123 | no | Proposed all main solid feeders, MCC branches, selected clear dashed terminal paths, and held congested control paths uncertain. |
| 1 | Jennifer precision | 120 | 125 | no | Promoted two solid feeder edges (`LC-480A--BAT-125A`, `LC-480D--BCHG-125B`); rejected unsupported charger/battery shortcuts. |
| 2 | Diego high-recall | 120 | 125 | yes | Agreed with Jennifer's precision revision and kept `SR-101` isolated. |
| 2 | Jennifer precision final | 120 | 125 | yes | Confirmed saturated 120-node, 125-edge graph; uncertain dashed interlocks remain out of matrix. |

## Final Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled terminals, solid feeders, bus taps, explicit tie/disconnect components, and clear dashed terminal-to-terminal control lines are asserted.
- Raceway labels, area titles, crossings without filled dots, and congested dashed interlocks without clear terminal ownership are excluded and recorded as uncertain/rejected.
"""
    (RESULTS / "round_summaries.md").write_text(text, encoding="utf-8")


def image_tokens_high_detail(path: Path) -> int:
    with Image.open(path) as image:
        width, height = image.size

    # Approximation for high-detail vision inputs: constrain to 2048 px max,
    # then to 768 px on the short side, and count 512 px tiles.
    scale = min(1.0, 2048.0 / max(width, height))
    width *= scale
    height *= scale
    if min(width, height) > 768:
        scale = 768.0 / min(width, height)
        width *= scale
        height *= scale
    tiles = math.ceil(width / 512.0) * math.ceil(height / 512.0)
    return 85 + 170 * tiles


def sum_image_tokens(paths: list[Path]) -> int:
    return sum(image_tokens_high_detail(path) for path in paths)


def write_token_usage() -> None:
    raw = BASE / "raw -- synthetic_npp_electrical_schematic_clean (1).png"
    overlay = BASE / "detected_components_and_logical_overlay.png"
    r = RESULTS
    main_images = [
        raw,
        overlay,
        r / "raw_01_top_sources_and_13kv_buses.png",
        r / "raw_02_mv_bus_a_sources.png",
        r / "raw_03_mv_bus_b_sources.png",
        r / "raw_04_train_a_480_loads.png",
        r / "raw_05_train_b_480_loads.png",
        r / "raw_06_train_a_dc_control.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_cross_train_controls.png",
        r / "overlay_01_top_sources_and_13kv_buses.png",
        r / "overlay_04_train_a_480_loads.png",
        r / "overlay_05_train_b_480_loads.png",
        r / "overlay_06_train_a_dc_control.png",
        r / "overlay_07_train_b_dc_control.png",
        r / "overlay_08_bottom_cross_train_controls.png",
    ]
    diego_r1_images = [
        raw,
        overlay,
        r / "raw_01_top_sources_and_13kv_buses.png",
        r / "raw_04_train_a_480_loads.png",
        r / "raw_05_train_b_480_loads.png",
        r / "raw_06_train_a_dc_control.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_cross_train_controls.png",
        r / "overlay_01_top_sources_and_13kv_buses.png",
        r / "overlay_04_train_a_480_loads.png",
        r / "overlay_05_train_b_480_loads.png",
        r / "overlay_06_train_a_dc_control.png",
        r / "overlay_07_train_b_dc_control.png",
    ]
    jennifer_r1_images = [
        raw,
        overlay,
        r / "raw_01_top_sources_and_13kv_buses.png",
        r / "raw_04_train_a_480_loads.png",
        r / "raw_05_train_b_480_loads.png",
        r / "raw_06_train_a_dc_control.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_cross_train_controls.png",
        r / "overlay_01_top_sources_and_13kv_buses.png",
        r / "overlay_06_train_a_dc_control.png",
        r / "overlay_07_train_b_dc_control.png",
        r / "overlay_08_bottom_cross_train_controls.png",
    ]
    diego_r2_images = [
        raw,
        r / "raw_01_top_sources_and_13kv_buses.png",
        r / "raw_04_train_a_480_loads.png",
        r / "raw_05_train_b_480_loads.png",
        r / "raw_06_train_a_dc_control.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_cross_train_controls.png",
        r / "overlay_06_train_a_dc_control.png",
        r / "overlay_07_train_b_dc_control.png",
    ]
    jennifer_r2_images = [
        r / "raw_06_train_a_dc_control.png",
        r / "raw_07_train_b_dc_control.png",
        r / "raw_08_bottom_cross_train_controls.png",
        r / "overlay_06_train_a_dc_control.png",
        r / "overlay_07_train_b_dc_control.png",
    ]

    rows = [
        {
            "call_id": "main-orchestration-aggregate",
            "agent": "Main agent",
            "model": "Codex session model",
            "text_input_expected": 22000,
            "image_expected": sum_image_tokens(main_images),
            "output_expected": 7500,
            "notes": "Aggregate estimate for main-agent visual inspection, tool-result digestion, subagent orchestration, artifact generation, and final reporting. Per-turn main usage was not exposed.",
        },
        {
            "call_id": "diego-round-1",
            "agent": "Diego",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "text_input_expected": 650,
            "image_expected": sum_image_tokens(diego_r1_images),
            "output_expected": 7600,
            "notes": "High-recall extraction prompt plus full raw/overlay and focused crop package.",
        },
        {
            "call_id": "jennifer-round-1",
            "agent": "Jennifer",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "text_input_expected": 6000,
            "image_expected": sum_image_tokens(jennifer_r1_images),
            "output_expected": 3600,
            "notes": "Precision review prompt including Diego proposal text and focused visual package.",
        },
        {
            "call_id": "diego-round-2",
            "agent": "Diego",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "text_input_expected": 650,
            "image_expected": sum_image_tokens(diego_r2_images),
            "output_expected": 750,
            "notes": "Saturation check against Jennifer revision with focused visuals.",
        },
        {
            "call_id": "jennifer-round-2-final",
            "agent": "Jennifer",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "text_input_expected": 300,
            "image_expected": sum_image_tokens(jennifer_r2_images),
            "output_expected": 90,
            "notes": "Final confirmation prompt with control-power and cross-train crops.",
        },
    ]

    fieldnames = [
        "document",
        "iteration",
        "call_id",
        "agent",
        "model",
        "text_input_tokens_low",
        "text_input_tokens_expected",
        "text_input_tokens_high",
        "cached_input_tokens_est",
        "image_file_input_tokens_low",
        "image_file_input_tokens_expected",
        "image_file_input_tokens_high",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_est",
        "total_low",
        "total_expected",
        "total_high",
        "usage_object_available",
        "notes",
    ]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            text_expected = row["text_input_expected"]
            image_expected = row["image_expected"]
            output_expected = row["output_expected"]
            text_low = round(text_expected * 0.75)
            text_high = round(text_expected * 1.35)
            image_low = round(image_expected * 0.80)
            image_high = round(image_expected * 1.30)
            output_low = round(output_expected * 0.60)
            output_high = round(output_expected * 1.60)
            writer.writerow(
                {
                    "document": 7,
                    "iteration": 1,
                    "call_id": row["call_id"],
                    "agent": row["agent"],
                    "model": row["model"],
                    "text_input_tokens_low": text_low,
                    "text_input_tokens_expected": text_expected,
                    "text_input_tokens_high": text_high,
                    "cached_input_tokens_est": 0,
                    "image_file_input_tokens_low": image_low,
                    "image_file_input_tokens_expected": image_expected,
                    "image_file_input_tokens_high": image_high,
                    "output_tokens_low": output_low,
                    "output_tokens_expected": output_expected,
                    "output_tokens_high": output_high,
                    "reasoning_tokens_est": "not exposed",
                    "total_low": text_low + image_low + output_low,
                    "total_expected": text_expected + image_expected + output_expected,
                    "total_high": text_high + image_high + output_high,
                    "usage_object_available": "no",
                    "notes": row["notes"] + " Official token counter and response usage objects unavailable because OPENAI_API_KEY was not set/exposed.",
                }
            )

    total_expected = 0
    total_low = 0
    total_high = 0
    with (RESULTS / "token_usage_estimate.csv").open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            total_low += int(row["total_low"])
            total_expected += int(row["total_expected"])
            total_high += int(row["total_high"])

    api_key_present = bool(os.environ.get("OPENAI_API_KEY"))
    summary = f"""# Token Usage Estimate

Document: 7
Iteration: 1

Official Responses token counting endpoint used: no
Reason: no API key was available in the environment (`OPENAI_API_KEY_PRESENT={str(api_key_present).lower()}`), and the subagent tool responses did not expose usage objects.

Fallback method:
- Text tokens estimated from prompt/response size by rough token budgeting.
- Image/file input tokens estimated with a high-detail 512-pixel tile method using actual image dimensions.
- Low/high totals apply conservative multipliers to text, image, and output estimates.

| document | iteration | calls | total low | total expected | total high |
|---:|---:|---:|---:|---:|---:|
| 7 | 1 | {len(rows)} | {total_low} | {total_expected} | {total_high} |
"""
    (RESULTS / "token_usage_summary.md").write_text(summary, encoding="utf-8")


def write_all() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    validate_edges(DIEGO_ROUND1_EDGES)
    validate_edges(FINAL_EDGES)

    for round_name, edges in ROUND_EDGE_SETS.items():
        validate_matrix(edges)
        write_edge_csv(RESULTS / f"{round_name}_edges.csv", edges)
        write_matrix_csv(RESULTS / f"{round_name}_matrix.csv", edges)
        write_matrix_csv(RESULTS / f"{round_name}_connectivity_matrix.csv", edges)

    write_edge_csv(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix_csv(RESULTS / "final_matrix.csv", FINAL_EDGES)
    write_matrix_csv(RESULTS / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_uncertain_and_rejected()
    write_round_summaries()
    write_token_usage()

    print(f"nodes={len(NODES)}")
    print(f"diego_round1_edges={len(DIEGO_ROUND1_EDGES)}")
    print(f"final_edges={len(FINAL_EDGES)}")
    print(f"results={RESULTS}")


if __name__ == "__main__":
    write_all()
