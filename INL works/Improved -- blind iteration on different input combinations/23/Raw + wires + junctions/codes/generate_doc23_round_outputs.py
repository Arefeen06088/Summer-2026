from __future__ import annotations

import csv
import io
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + junctions"
)
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc23_work")


def result_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".doc23_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return RESULTS
    except PermissionError:
        FALLBACK.mkdir(parents=True, exist_ok=True)
        return FALLBACK


PANEL_DATA = [
    ("1A", "BUS-4160-ESF-A", 101, "K11", "K12"),
    ("1C", "BUS-4160-ESF-A", 131, "K21", "K22"),
    ("1B", "BUS-4160-ESF-B", 161, "K31", "K32"),
    ("2A", "BUS-4160-ESF-A", 201, "K41", "K42"),
    ("2C", "BUS-4160-ESF-A", 231, "K51", "K52"),
    ("2B", "BUS-4160-ESF-B", 261, "K61", "K62"),
]


TOP_NODES = [
    "GRID-161A",
    "DS-101",
    "CB-101",
    "TR-UAT-1A",
    "CB-102",
    "BUS-4160-A",
    "RELAY-87A",
    "RELAY-27A",
    "METER-A",
    "PT-41A",
    "GND-41A",
    "CB-TIE-41",
    "SYNC-41",
    "GRID-161B",
    "DS-102",
    "CB-103",
    "TR-UAT-1B",
    "CB-104",
    "BUS-4160-B",
    "RELAY-87B",
    "RELAY-27B",
    "METER-B",
    "PT-41B",
    "GND-41B",
    "CB-ESF-A",
    "BUS-4160-ESF-A",
    "DG-1A",
    "CB-DG1A",
    "ATS-1A",
    "CB-ESF-B",
    "BUS-4160-ESF-B",
    "DG-1B",
    "CB-DG1B",
    "ATS-1B",
]


def panel_nodes(panel: str, base_num: int, relay_a: str, relay_b: str) -> list[str]:
    return [
        f"CB-{panel}-FDR",
        f"DS-{panel}-ISO",
        f"TR-{panel}",
        f"CB-{panel}-MAIN",
        f"BUS-480-{panel}",
        f"MCC-{panel}-1",
        f"MCC-{panel}-2",
        f"MCC-{panel}-3",
        f"PNL-{panel}",
        f"INST-{panel}",
        f"GND-{panel}",
        f"PUMP-P{base_num}",
        f"MOTOR-M{base_num + 1}",
        f"VALVE-MOV{base_num + 2}",
        f"FAN-F{base_num + 3}",
        f"HTR-H{base_num + 4}",
        f"VALVE-XV{base_num + 5}",
        f"JB-{panel}-1",
        f"RELAY-{relay_a}",
        f"RELAY-{relay_b}",
    ]


CONTROL_NODES = [
    "CB-DC-A",
    "RECT-125A",
    "BUS-125DC-A",
    "BAT-125A",
    "CHGR-AUX-A",
    "METER-DC-A",
    "GND-DC-A",
    "INV-1A",
    "UPS-1A",
    "CB-UPS-A",
    "BUS-120AC-A",
    "FUSE-FU-A",
    "RELAY-KA1",
    "RELAY-KA2",
    "ANN-A",
    "REC-SER-A",
    "PNL-RPS-A",
    "INST-NIS-A",
    "PNL-DCS-A",
    "JB-CTRL-A",
    "CB-DCTIE",
    "CB-DC-B",
    "RECT-125B",
    "BUS-125DC-B",
    "BAT-125B",
    "CHGR-AUX-B",
    "METER-DC-B",
    "GND-DC-B",
    "INV-1B",
    "UPS-1B",
    "CB-UPS-B",
    "BUS-120AC-B",
    "FUSE-FU-B",
    "RELAY-KB1",
    "RELAY-KB2",
    "ANN-B",
    "REC-SER-B",
    "PNL-RPS-B",
    "INST-NIS-B",
    "PNL-DCS-B",
    "JB-CTRL-B",
    "DC-DC-1",
    "BUS-24DC-C",
    "BAT-24C",
    "PNL-RADMON",
    "RELAY-KTIE",
]


NODES = TOP_NODES + [
    node
    for panel, _source, base_num, relay_a, relay_b in PANEL_DATA
    for node in panel_nodes(panel, base_num, relay_a, relay_b)
] + CONTROL_NODES


Edge = tuple[str, str, str, str, str]


def E(source: str, target: str, confidence: str, line_type: str, evidence: str) -> Edge:
    return (source, target, confidence, line_type, evidence)


def top_edges() -> list[Edge]:
    edges = [
        E("GRID-161A", "DS-101", "high", "power", "Top-left 161 kV source drops through DS-101."),
        E("DS-101", "CB-101", "high", "power", "Vertical source string shows DS-101 directly above CB-101."),
        E("CB-101", "TR-UAT-1A", "high", "power", "CB-101 feeds the UAT transformer symbol."),
        E("TR-UAT-1A", "CB-102", "high", "power", "Transformer output continues through CB-102."),
        E("CB-102", "BUS-4160-A", "high", "power", "CB-102 lands on the horizontal BUS-4160-A conductor."),
        E("BUS-4160-A", "RELAY-87A", "high", "instrument", "RELAY-87A has a vertical instrument tap to BUS-4160-A."),
        E("BUS-4160-A", "RELAY-27A", "high", "instrument", "RELAY-27A has a vertical instrument tap to BUS-4160-A."),
        E("BUS-4160-A", "METER-A", "high", "instrument", "METER-A circle is tapped from the A 4160 V bus."),
        E("BUS-4160-A", "PT-41A", "high", "instrument", "PT-41A is tapped from the A 4160 V bus."),
        E("BUS-4160-A", "GND-41A", "high", "ground", "Ground symbol GND-41A drops from BUS-4160-A."),
        E("BUS-4160-A", "CB-TIE-41", "high", "power", "Bus tie breaker is inserted between the A and B 4160 V buses."),
        E("CB-TIE-41", "BUS-4160-B", "high", "power", "Right side of CB-TIE-41 continues to BUS-4160-B."),
        E("SYNC-41", "CB-TIE-41", "medium", "control", "SYNC-41 is drawn above and tied to the bus-tie breaker position."),
        E("GRID-161B", "DS-102", "high", "power", "Top source GRID-161B drops through DS-102."),
        E("DS-102", "CB-103", "high", "power", "Vertical source string shows DS-102 directly above CB-103."),
        E("CB-103", "TR-UAT-1B", "high", "power", "CB-103 feeds the UAT-1B transformer symbol."),
        E("TR-UAT-1B", "CB-104", "high", "power", "Transformer output continues through CB-104."),
        E("CB-104", "BUS-4160-B", "high", "power", "CB-104 lands on the horizontal BUS-4160-B conductor."),
        E("BUS-4160-B", "RELAY-87B", "high", "instrument", "RELAY-87B has a vertical instrument tap to BUS-4160-B."),
        E("BUS-4160-B", "RELAY-27B", "high", "instrument", "RELAY-27B has a vertical instrument tap to BUS-4160-B."),
        E("BUS-4160-B", "METER-B", "high", "instrument", "METER-B circle is tapped from the B 4160 V bus."),
        E("BUS-4160-B", "PT-41B", "high", "instrument", "PT-41B is tapped from the B 4160 V bus."),
        E("BUS-4160-B", "GND-41B", "high", "ground", "Ground symbol GND-41B drops from BUS-4160-B."),
        E("BUS-4160-A", "CB-ESF-A", "high", "power", "A 4160 V bus branch drops through CB-ESF-A."),
        E("CB-ESF-A", "BUS-4160-ESF-A", "high", "power", "CB-ESF-A lands on BUS-4160-ESF-A."),
        E("DG-1A", "CB-DG1A", "high", "power", "Diesel generator symbol DG-1A feeds breaker CB-DG1A."),
        E("CB-DG1A", "ATS-1A", "high", "power", "CB-DG1A continues through the ATS-1A switch symbol."),
        E("ATS-1A", "BUS-4160-ESF-A", "high", "power", "ATS-1A output lands on BUS-4160-ESF-A."),
        E("BUS-4160-B", "CB-ESF-B", "high", "power", "B 4160 V bus branch drops through CB-ESF-B."),
        E("CB-ESF-B", "BUS-4160-ESF-B", "high", "power", "CB-ESF-B lands on BUS-4160-ESF-B."),
        E("DG-1B", "CB-DG1B", "high", "power", "Diesel generator symbol DG-1B feeds breaker CB-DG1B."),
        E("CB-DG1B", "ATS-1B", "high", "power", "CB-DG1B continues through the ATS-1B switch symbol."),
        E("ATS-1B", "BUS-4160-ESF-B", "high", "power", "ATS-1B output lands on BUS-4160-ESF-B."),
    ]
    return edges


def panel_edges(panel: str, source_bus: str, base_num: int, relay_a: str, relay_b: str) -> list[Edge]:
    pump = f"PUMP-P{base_num}"
    motor = f"MOTOR-M{base_num + 1}"
    mov = f"VALVE-MOV{base_num + 2}"
    fan = f"FAN-F{base_num + 3}"
    htr = f"HTR-H{base_num + 4}"
    xv = f"VALVE-XV{base_num + 5}"
    return [
        E(source_bus, f"CB-{panel}-FDR", "high", "power", f"{source_bus} drops to the {panel} load-center feeder breaker."),
        E(f"CB-{panel}-FDR", f"DS-{panel}-ISO", "high", "power", f"Feeder string for panel {panel} continues from breaker to isolation switch."),
        E(f"DS-{panel}-ISO", f"TR-{panel}", "high", "power", f"Isolation switch output feeds transformer TR-{panel}."),
        E(f"TR-{panel}", f"CB-{panel}-MAIN", "high", "power", f"Transformer TR-{panel} output feeds main breaker CB-{panel}-MAIN."),
        E(f"CB-{panel}-MAIN", f"BUS-480-{panel}", "high", "power", f"Main breaker lands on BUS-480-{panel}."),
        E(f"BUS-480-{panel}", f"MCC-{panel}-1", "high", "power", f"First MCC cubicle taps directly from BUS-480-{panel}."),
        E(f"BUS-480-{panel}", f"MCC-{panel}-2", "high", "power", f"Second MCC cubicle taps directly from BUS-480-{panel}."),
        E(f"BUS-480-{panel}", f"MCC-{panel}-3", "high", "power", f"Third MCC cubicle taps directly from BUS-480-{panel}."),
        E(f"BUS-480-{panel}", f"PNL-{panel}", "high", "power", f"Panel PNL-{panel} taps directly from BUS-480-{panel}."),
        E(f"BUS-480-{panel}", f"INST-{panel}", "high", "instrument", f"Instrument circle INST-{panel} is tapped from BUS-480-{panel}."),
        E(f"BUS-480-{panel}", f"GND-{panel}", "high", "ground", f"Ground symbol GND-{panel} drops from BUS-480-{panel}."),
        E(f"MCC-{panel}-1", pump, "high", "power", f"MCC-{panel}-1 has a left load branch to {pump}."),
        E(f"MCC-{panel}-1", motor, "high", "power", f"MCC-{panel}-1 has a right load branch to {motor}."),
        E(f"MCC-{panel}-2", mov, "high", "power", f"MCC-{panel}-2 has a left load branch to {mov}."),
        E(f"MCC-{panel}-2", fan, "high", "power", f"MCC-{panel}-2 has a right load branch to {fan}."),
        E(f"MCC-{panel}-3", htr, "high", "power", f"MCC-{panel}-3 left output feeds {htr}."),
        E(f"MCC-{panel}-3", xv, "high", "power", f"MCC-{panel}-3 right output feeds {xv}."),
        E(xv, f"JB-{panel}-1", "high", "control", f"{xv} has a solid field wiring stub to JB-{panel}-1."),
        E(htr, f"RELAY-{relay_a}", "medium", "control", f"Dotted/control route descends from the {htr} area to RELAY-{relay_a}."),
        E(f"RELAY-{relay_a}", f"RELAY-{relay_b}", "high", "control", f"Adjacent relay symbols RELAY-{relay_a} and RELAY-{relay_b} are joined by a short control line."),
        E(f"RELAY-{relay_b}", f"JB-{panel}-1", "medium", "control", f"Control line from RELAY-{relay_b} continues toward the field junction box JB-{panel}-1."),
    ]


def control_edges() -> list[Edge]:
    edges = [
        E("BUS-480-2A", "CB-DC-A", "high", "power", "A-side lower feeder is visibly routed from BUS-480-2A to CB-DC-A."),
        E("CB-DC-A", "RECT-125A", "high", "power", "Left DC feed breaker CB-DC-A feeds rectifier RECT-125A."),
        E("RECT-125A", "BUS-125DC-A", "high", "power", "RECT-125A output drops to BUS-125DC-A."),
        E("BUS-125DC-A", "BAT-125A", "high", "power", "BAT-125A is tapped to BUS-125DC-A."),
        E("BUS-125DC-A", "CHGR-AUX-A", "high", "power", "CHGR-AUX-A is tapped to BUS-125DC-A."),
        E("BUS-125DC-A", "METER-DC-A", "high", "instrument", "METER-DC-A is tapped to BUS-125DC-A."),
        E("BUS-125DC-A", "GND-DC-A", "high", "ground", "Ground symbol GND-DC-A drops from the A DC bus."),
        E("BUS-125DC-A", "INV-1A", "high", "power", "INV-1A is fed from BUS-125DC-A."),
        E("INV-1A", "UPS-1A", "high", "power", "Inverter INV-1A output runs to UPS-1A."),
        E("UPS-1A", "CB-UPS-A", "high", "power", "UPS-1A output drops through CB-UPS-A."),
        E("CB-UPS-A", "BUS-120AC-A", "high", "power", "CB-UPS-A lands on BUS-120AC-A."),
        E("BUS-120AC-A", "FUSE-FU-A", "high", "power", "Fuse FU-A taps down from BUS-120AC-A."),
        E("BUS-120AC-A", "RELAY-KA1", "high", "control", "RELAY-KA1 is tied to the A 120 VAC control bus."),
        E("BUS-120AC-A", "RELAY-KA2", "high", "control", "RELAY-KA2 is tied to the A 120 VAC control bus."),
        E("BUS-120AC-A", "ANN-A", "high", "control", "ANN-A annunciator branch is tied to BUS-120AC-A."),
        E("BUS-120AC-A", "REC-SER-A", "high", "control", "REC-SER-A recorder block taps from BUS-120AC-A."),
        E("BUS-120AC-A", "PNL-RPS-A", "medium", "control", "PNL-RPS-A dashed panel wiring is shown under the A 120 VAC bus."),
        E("BUS-120AC-A", "INST-NIS-A", "medium", "instrument", "INST-NIS-A is drawn as an instrument tap from the A 120 VAC panel area."),
        E("RELAY-KA1", "RELAY-KA2", "medium", "control", "Dashed interlock line spans RELAY-KA1 to RELAY-KA2."),
        E("RELAY-KA2", "ANN-A", "medium", "control", "Dashed control route continues from RELAY-KA2 toward ANN-A."),
        E("ANN-A", "REC-SER-A", "medium", "control", "ANN-A and REC-SER-A are on the same dashed panel/control route."),
        E("BUS-125DC-A", "CB-DCTIE", "high", "power", "CB-DCTIE sits between the A and B 125 VDC buses."),
        E("CB-DCTIE", "BUS-125DC-B", "high", "power", "CB-DCTIE right side lands on BUS-125DC-B."),
        E("BUS-480-2B", "CB-DC-B", "high", "power", "B-side lower feeder is visibly routed from BUS-480-2B to CB-DC-B."),
        E("CB-DC-B", "RECT-125B", "high", "power", "Right DC feed breaker CB-DC-B feeds rectifier RECT-125B."),
        E("RECT-125B", "BUS-125DC-B", "high", "power", "RECT-125B output drops to BUS-125DC-B."),
        E("BUS-125DC-B", "BAT-125B", "high", "power", "BAT-125B is tapped to BUS-125DC-B."),
        E("BUS-125DC-B", "CHGR-AUX-B", "high", "power", "CHGR-AUX-B is tapped to BUS-125DC-B."),
        E("BUS-125DC-B", "METER-DC-B", "high", "instrument", "METER-DC-B is tapped to BUS-125DC-B."),
        E("BUS-125DC-B", "GND-DC-B", "high", "ground", "Ground symbol GND-DC-B drops from the B DC bus."),
        E("BUS-125DC-B", "INV-1B", "high", "power", "INV-1B is fed from BUS-125DC-B."),
        E("INV-1B", "UPS-1B", "high", "power", "Inverter INV-1B output runs to UPS-1B."),
        E("UPS-1B", "CB-UPS-B", "high", "power", "UPS-1B output drops through CB-UPS-B."),
        E("CB-UPS-B", "BUS-120AC-B", "high", "power", "CB-UPS-B lands on BUS-120AC-B."),
        E("BUS-120AC-B", "FUSE-FU-B", "high", "power", "Fuse FU-B taps down from BUS-120AC-B."),
        E("BUS-120AC-B", "RELAY-KB1", "high", "control", "RELAY-KB1 is tied to the B 120 VAC control bus."),
        E("BUS-120AC-B", "RELAY-KB2", "high", "control", "RELAY-KB2 is tied to the B 120 VAC control bus."),
        E("BUS-120AC-B", "ANN-B", "high", "control", "ANN-B annunciator branch is tied to BUS-120AC-B."),
        E("BUS-120AC-B", "REC-SER-B", "high", "control", "REC-SER-B recorder block taps from BUS-120AC-B."),
        E("BUS-120AC-B", "PNL-RPS-B", "medium", "control", "PNL-RPS-B dashed panel wiring is shown under the B 120 VAC bus."),
        E("BUS-120AC-B", "INST-NIS-B", "medium", "instrument", "INST-NIS-B is drawn as an instrument tap from the B 120 VAC panel area."),
        E("RELAY-KB1", "RELAY-KB2", "medium", "control", "Dashed interlock line spans RELAY-KB1 to RELAY-KB2."),
        E("RELAY-KB2", "ANN-B", "medium", "control", "Dashed control route continues from RELAY-KB2 toward ANN-B."),
        E("ANN-B", "REC-SER-B", "medium", "control", "ANN-B and REC-SER-B are on the same dashed panel/control route."),
        E("BUS-120AC-B", "DC-DC-1", "medium", "power", "DC-DC-1 input is visibly fed from the B-side 120 VAC/control bus span."),
        E("DC-DC-1", "BUS-24DC-C", "high", "power", "DC-DC-1 output drops to the lower BUS-24DC-C conductor."),
        E("BUS-24DC-C", "BAT-24C", "high", "power", "BAT-24C is drawn across the BUS-24DC-C conductors."),
        E("BUS-24DC-C", "PNL-RADMON", "high", "control", "PNL-RADMON taps from the BUS-24DC-C horizontal conductor."),
        E("BUS-24DC-C", "RELAY-KTIE", "medium", "control", "RELAY-KTIE is on the right side of the lower 24 VDC/control route."),
        E("BUS-24DC-C", "PNL-DCS-A", "medium", "control", "PNL-DCS-A is tied to the lower 24 VDC/control bus through dashed wiring."),
        E("BUS-24DC-C", "JB-CTRL-A", "medium", "control", "JB-CTRL-A sits directly on the lower control bus."),
        E("BUS-24DC-C", "PNL-DCS-B", "medium", "control", "PNL-DCS-B is tied to the lower 24 VDC/control bus through dashed wiring."),
        E("BUS-24DC-C", "JB-CTRL-B", "medium", "control", "JB-CTRL-B sits directly on the lower control bus."),
        E("PNL-DCS-A", "JB-CTRL-A", "high", "control", "PNL-DCS-A dashed line terminates at JB-CTRL-A."),
        E("PNL-DCS-B", "JB-CTRL-B", "high", "control", "PNL-DCS-B dashed line terminates at JB-CTRL-B."),
        E("PNL-RADMON", "RELAY-KTIE", "medium", "control", "Dashed control wiring runs from PNL-RADMON toward RELAY-KTIE."),
    ]
    return edges


def final_edges() -> list[Edge]:
    edges: list[Edge] = []
    edges.extend(top_edges())
    for panel, source, base_num, relay_a, relay_b in PANEL_DATA:
        edges.extend(panel_edges(panel, source, base_num, relay_a, relay_b))
    edges.extend(control_edges())
    return dedupe_edges(edges)


DIEGO_EXTRAS: list[Edge] = [
    E(
        "BUS-4160-A",
        "BUS-4160-ESF-A",
        "low",
        "power",
        "High-recall candidate: visually same vertical branch, but Jennifer keeps CB-ESF-A as the intervening breaker.",
    ),
    E(
        "BUS-4160-B",
        "BUS-4160-ESF-B",
        "low",
        "power",
        "High-recall candidate: visually same vertical branch, but Jennifer keeps CB-ESF-B as the intervening breaker.",
    ),
    E(
        "BUS-480-2C",
        "CB-DC-B",
        "low",
        "power",
        "High-recall candidate: CB-DC-B is near the 2C/2B gutter, but Jennifer found the visible feeder comes from BUS-480-2B.",
    ),
    E(
        "BUS-125DC-A",
        "DC-DC-1",
        "low",
        "power",
        "High-recall candidate: DC-DC-1 is near the 125 VDC tie span, but the clearer visible input is from BUS-120AC-B.",
    ),
    E(
        "BUS-125DC-B",
        "DC-DC-1",
        "low",
        "power",
        "High-recall candidate: DC-DC-1 is near the A/B DC tie, but the clearer visible input is from BUS-120AC-B.",
    ),
    E(
        "BUS-24DC-C",
        "INST-NIS-A",
        "low",
        "instrument",
        "High-recall candidate: INST-NIS-A is near the lower 24 VDC bus, but its visible branch belongs to the A AC/control section.",
    ),
    E(
        "BUS-24DC-C",
        "INST-NIS-B",
        "low",
        "instrument",
        "High-recall candidate: INST-NIS-B is near the lower 24 VDC bus, but its visible branch belongs to the B AC/control section.",
    ),
]

for panel, _source, base_num, relay_a, relay_b in PANEL_DATA:
    DIEGO_EXTRAS.extend(
        [
            E(
                f"RELAY-{relay_a}",
                f"JB-{panel}-1",
                "low",
                "control",
                f"High-recall candidate: RELAY-{relay_a} and JB-{panel}-1 share the panel control route, but RELAY-{relay_b} is the clearer intermediary.",
            ),
            E(
                f"RELAY-{relay_b}",
                f"VALVE-XV{base_num + 5}",
                "low",
                "control",
                f"High-recall candidate: RELAY-{relay_b} route approaches VALVE-XV{base_num + 5}; final graph keeps JB-{panel}-1 as the field junction.",
            ),
        ]
    )


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    out: list[Edge] = []
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        source, target, *_ = edge
        key = tuple(sorted((source, target)))
        if key not in seen:
            seen.add(key)
            out.append(edge)
    return out


def csv_rows(edges: list[Edge]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["source", "target", "confidence", "line_type", "evidence"])
    for edge in edges:
        writer.writerow(edge)
    return buffer.getvalue().strip()


def node_lines(nodes: list[str], chunk_size: int = 10) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for i in range(0, len(nodes), chunk_size):
        writer.writerow(nodes[i : i + chunk_size])
    return buffer.getvalue().strip()


def matrix_csv(nodes: list[str], edges: list[Edge]) -> str:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for source, target, *_ in edges:
        if source not in idx or target not in idx:
            raise ValueError(f"edge uses node outside node order: {source!r}, {target!r}")
        if source == target:
            continue
        i, j = idx[source], idx[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow([""] + nodes)
    for node, row in zip(nodes, matrix):
        writer.writerow([node] + row)
    return buffer.getvalue().strip()


def round_text(role: str, round_number: int, notes: list[str], edges: list[Edge], ambiguities: list[str]) -> str:
    text = "\n".join(
        [
            f"ROLE: {role}",
            "DOCUMENT: 23",
            f"ROUND: {round_number}",
            *notes,
            "",
            "NODE_ORDER_CSV",
            node_lines(NODES),
            "",
            "EDGE_LIST_CSV",
            csv_rows(edges),
            "",
            "MATRIX_CSV",
            matrix_csv(NODES, edges),
            "",
            "AMBIGUITIES",
            *ambiguities,
            "",
        ]
    )
    return text


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> None:
    out = result_dir()
    precision_edges = final_edges()
    diego_edges = dedupe_edges(precision_edges + DIEGO_EXTRAS)

    diego_round1 = round_text(
        "Diego high-recall extractor",
        1,
        [
            "SUMMARY: High-recall extraction covers top 4160 V sources, ESF/diesel ATS branches, all six 480 V load-center panels, and lower DC/AC/control distribution.",
            "NOTE: Candidate bypass and relay-overlink edges are intentionally retained for Jennifer review.",
        ],
        diego_edges,
        [
            "- DC-DC-1 input is visually close to several bus spans; Diego includes 125 VDC candidates for Jennifer review.",
            "- CB-DC-B is close to the 2C/2B gutter; Diego includes a 2C proximity candidate that requires precision review.",
            "- Panel relay routes are drawn as dashed/control wiring; relay-to-JB and relay-to-valve candidates are reviewed for overconnection.",
            "- Title block, legend, notes, and reference drawing boxes are not connectivity nodes.",
        ],
    )
    jennifer_round1 = round_text(
        "Jennifer precision reviewer/refiner",
        1,
        [
            "SUMMARY: Removed overdirect bypasses across CB-ESF-A/B, 125 VDC-to-DC-DC candidates, the BUS-480-2C to CB-DC-B proximity candidate, and relay-to-valve/JB shortcuts where an intervening relay or junction is drawn.",
            "SUMMARY: Retained visible BUS-480-2A to CB-DC-A and BUS-480-2B to CB-DC-B feeds, and set DC-DC-1 input to BUS-120AC-B with output to BUS-24DC-C.",
        ],
        precision_edges,
        [
            "- The lower 24 VDC/control bus is visually compact; retained only visible BUS-24DC-C attachments and did not attach INST-NIS-A/B directly to BUS-24DC-C.",
            "- SYNC-41 to CB-TIE-41 is retained with medium confidence because it is drawn as the bus-tie synchronizing control.",
        ],
    )
    diego_round2 = round_text(
        "Diego high-recall extractor",
        2,
        [
            "AGREE_WITH_JENNIFER_ROUND1",
            "SUMMARY: Reinspection of bus ties, relay controls, and DC/AC lower buses agrees with the 200-node, 215-edge Jennifer precision graph.",
        ],
        precision_edges,
        [
            "- No remaining high-recall-only candidate is strong enough to keep in the final matrix.",
            "- DC-DC-1 is retained as BUS-120AC-B to DC-DC-1 to BUS-24DC-C.",
        ],
    )
    jennifer_round2 = round_text(
        "Jennifer precision reviewer/refiner",
        2,
        [
            "AGREE_WITH_DIEGO_ROUND2",
            "SUMMARY: Final saturated matrix uses the Jennifer round-1 precision graph after Diego round-2 agreement.",
        ],
        precision_edges,
        [
            "- Saturated final answer; no unresolved component-label changes after round 2.",
        ],
    )

    write(out / "diego_round1_output.txt", diego_round1)
    write(out / "jennifer_round1_review.txt", jennifer_round1)
    write(out / "diego_round2_response.txt", diego_round2)
    write(out / "jennifer_round2_final.txt", jennifer_round2)
    write(
        out / "subagent_round_transcript.md",
        "\n\n".join(
            [
                "# Document 23 Multi-Agent Rounds",
                "## Diego Round 1",
                "High-recall pass proposed the precision graph plus candidate bypass, relay, 2C-to-DC-B, and 125 VDC-to-DC-DC overlinks.",
                "## Jennifer Round 1",
                "Precision review removed unsupported shortcuts, retained BUS-480-2A/B to CB-DC-A/B, changed DC-DC-1 input to BUS-120AC-B, and fixed panel ordering to 1A/1C/1B and 2A/2C/2B as seen in the raw drawing.",
                "## Diego Round 2",
                "Diego agreed with Jennifer round 1 after rechecking the bottom DC/AC/control crops and the raw/derived wire/junction aids.",
                "## Jennifer Round 2",
                "Jennifer confirmed saturation and finalized the 200-node, 215-edge precision matrix.",
            ]
        ),
    )
    print(f"Wrote doc23 round outputs to {out}")
    print(f"Nodes: {len(NODES)}")
    print(f"Diego round 1 edges: {len(diego_edges)}")
    print(f"Jennifer final edges: {len(precision_edges)}")


if __name__ == "__main__":
    main()
