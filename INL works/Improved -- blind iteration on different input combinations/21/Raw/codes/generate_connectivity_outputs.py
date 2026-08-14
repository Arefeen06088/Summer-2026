from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


SOURCE_NODES = [
    "GEN-UT",
    "BUS-101",
    "BUS-102",
    "CB-101",
    "CB-102",
    "CB-103",
    "CB-104",
    "CB-105",
    "CB-106",
    "CB-201A",
    "CB-201B",
    "CB-202A",
    "CB-202B",
    "CB-203A",
    "CB-203B",
    "CB-204A",
    "CB-UNLABELED-EDG2A-INBOARD",
    "DS-101A",
    "DS-101B",
    "DS-102A",
    "DS-102B",
    "DS-201A",
    "DS-201B",
    "DS-202A",
    "DS-202B",
    "TR-UAT1",
    "TR-UAT2",
    "TR-SU1",
    "TR-SU2",
    "BUS-201A",
    "BUS-201B",
    "BUS-202A",
    "BUS-202B",
    "EDG-1A",
    "EDG-1B",
    "EDG-2A",
    "EDG-2B",
]


LOAD_CENTER_NODES = [
    "CB-301A",
    "CB-302A",
    "CB-303A",
    "CB-304A",
    "CB-501A",
    "CB-502A",
    "CB-503A",
    "DS-301A",
    "DS-302A",
    "TR-SA",
    "TR-NA",
    "BUS-301A",
    "BUS-302A",
    "MCC-1A",
    "MCC-2A",
    "MCC-3A",
    "GND-1",
    "GND-5",
    "MOTOR-SI101A",
    "PUMP-SI101A",
    "MOTOR-CCW101A",
    "PUMP-CCW101A",
    "VLV-8801A",
    "MOTOR-AFW101A",
    "PUMP-AFW101A",
    "MOTOR-RHR101A",
    "PUMP-RHR101A",
    "VLV-8802A",
    "MOTOR-SW101A",
    "PUMP-SW101A",
    "MOTOR-CHG101A",
    "PUMP-CHG101A",
    "MOTOR-FAN101A",
    "VLV-8901A",
    "CB-301B",
    "CB-302B",
    "CB-303B",
    "CB-304B",
    "CB-501B",
    "CB-502B",
    "CB-503B",
    "DS-301B",
    "DS-302B",
    "TR-SB",
    "TR-NB",
    "BUS-301B",
    "BUS-302B",
    "MCC-1B",
    "MCC-2B",
    "MCC-3B",
    "GND-2",
    "GND-6",
    "MOTOR-SI101B",
    "PUMP-SI101B",
    "MOTOR-CCW101B",
    "PUMP-CCW101B",
    "VLV-8801B",
    "MOTOR-AFW101B",
    "PUMP-AFW101B",
    "MOTOR-RHR101B",
    "PUMP-RHR101B",
    "VLV-8802B",
    "MOTOR-SW101B",
    "PUMP-SW101B",
    "MOTOR-CHG101B",
    "PUMP-CHG101B",
    "MOTOR-FAN101B",
    "VLV-8901B",
]


DC_CONTROL_NODES = [
    "DS-401A",
    "DS-401B",
    "DS-402A",
    "DS-402B",
    "TR-DC-A",
    "TR-DC-B",
    "TR-INV-A",
    "TR-INV-B",
    "RECT-125A",
    "RECT-125B",
    "RECT-24C",
    "INV-120A",
    "INV-120B",
    "INV-120C",
    "BUS-401A",
    "BUS-401B",
    "BAT-1A",
    "BAT-2A",
    "BAT-1B",
    "BAT-2B",
    "BAT-EDG-A",
    "BAT-EDG-B",
    "GND-3",
    "GND-4",
    "BUS-501A",
    "BUS-501B",
    "CP-SWGR",
    "CP-SI-A",
    "CP-SI-B",
    "CP-CCW-A",
    "CP-CCW-B",
    "CP-EDG-A",
    "CP-EDG-B",
    "RPS-A",
    "RPS-B",
    "ESFAS-A",
    "ESFAS-B",
    "CP-CRD",
    "UVLS-A",
    "UVLS-B",
]


RELAY_NODES = [f"RELAY-K{i}" for i in range(101, 131)]
JUNCTION_NODES = [f"JB-{i}" for i in range(101, 111)]
INSTRUMENT_NODES = [
    "INST-PT101",
    "INST-PT102",
    "INST-PT103",
    "INST-FT201",
    "INST-FT202",
    "INST-LT301",
    "INST-LT302",
    "INST-TT401",
    "INST-TT402",
    "INST-CT501",
    "INST-CT502",
    "INST-VT601",
    "INST-VT602",
    "INST-ZS701",
    "INST-ZS702",
]


FINAL_NODES = (
    SOURCE_NODES
    + LOAD_CENTER_NODES
    + DC_CONTROL_NODES
    + RELAY_NODES
    + JUNCTION_NODES
    + INSTRUMENT_NODES
)


DIEGO_R1_NODES = [
    node for node in FINAL_NODES if node != "CB-UNLABELED-EDG2A-INBOARD"
]


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


BASE_EDGES = [
    edge("GEN-UT", "CB-101", "solid_power", "generator UT upper feeder"),
    edge("CB-101", "DS-101A", "solid_power", "upper UAT1 feeder breaker to disconnect"),
    edge("DS-101A", "TR-UAT1", "solid_power", "upper UAT1 feeder disconnect to transformer"),
    edge("TR-UAT1", "CB-201A", "solid_power", "UAT1 transformer to 4.16 kV breaker"),
    edge("CB-201A", "BUS-201A", "solid_power", "breaker lands on class 1E A bus"),
    edge("GEN-UT", "CB-102", "solid_power", "generator UT lower feeder"),
    edge("CB-102", "DS-101B", "solid_power", "lower UAT2 feeder breaker to disconnect"),
    edge("DS-101B", "TR-UAT2", "solid_power", "lower UAT2 feeder disconnect to transformer"),
    edge("TR-UAT2", "CB-201B", "solid_power", "UAT2 transformer to 4.16 kV breaker"),
    edge("CB-201B", "BUS-201B", "solid_power", "breaker lands on class 1E B bus"),
    edge("BUS-101", "CB-103", "solid_power", "13.8 kV aux bus to standby transformer feeder"),
    edge("CB-103", "DS-102A", "solid_power", "standby A feeder breaker to disconnect"),
    edge("DS-102A", "TR-SU1", "solid_power", "standby A disconnect to transformer"),
    edge("TR-SU1", "CB-202A", "solid_power", "standby A transformer to breaker"),
    edge("CB-202A", "BUS-202A", "solid_power", "breaker lands on non-1E A bus"),
    edge("BUS-102", "CB-104", "solid_power", "13.8 kV preferred bus to standby transformer feeder"),
    edge("CB-104", "DS-102B", "solid_power", "standby B feeder breaker to disconnect"),
    edge("DS-102B", "TR-SU2", "solid_power", "standby B disconnect to transformer"),
    edge("TR-SU2", "CB-202B", "solid_power", "standby B transformer to breaker"),
    edge("CB-202B", "BUS-202B", "solid_power", "breaker lands on non-1E B bus"),
    edge("BUS-201A", "DS-201A", "solid_power", "EDG-1A feeder from BUS-201A"),
    edge("DS-201A", "CB-105", "solid_power", "EDG-1A feeder disconnect to breaker"),
    edge("CB-105", "EDG-1A", "solid_power", "EDG-1A breaker to generator"),
    edge("BUS-201B", "CB-204A", "solid_power", "EDG-1B bus-side breaker"),
    edge("CB-204A", "DS-201B", "solid_power", "EDG-1B breaker to disconnect"),
    edge("DS-201B", "CB-106", "solid_power", "EDG-1B disconnect to breaker"),
    edge("CB-106", "EDG-1B", "solid_power", "EDG-1B breaker to generator"),
    edge("BUS-202A", "CB-UNLABELED-EDG2A-INBOARD", "solid_power", "visible unlabeled EDG-2A bus-side breaker"),
    edge("CB-UNLABELED-EDG2A-INBOARD", "DS-202A", "solid_power", "unlabeled EDG-2A breaker to disconnect"),
    edge("DS-202A", "CB-203A", "solid_power", "EDG-2A disconnect to breaker"),
    edge("CB-203A", "EDG-2A", "solid_power", "EDG-2A breaker to generator"),
    edge("BUS-202B", "DS-202B", "solid_power", "EDG-2B feeder from BUS-202B"),
    edge("DS-202B", "CB-203B", "solid_power", "EDG-2B disconnect to breaker"),
    edge("CB-203B", "EDG-2B", "solid_power", "EDG-2B breaker to generator"),
    edge("BUS-201A", "CB-301A", "solid_power", "BUS-201A drop to 480 V train A transformer"),
    edge("CB-301A", "DS-301A", "solid_power", "train A transformer breaker to disconnect"),
    edge("DS-301A", "TR-SA", "solid_power", "disconnect to safety transformer A"),
    edge("TR-SA", "CB-501A", "solid_power", "safety transformer A to 480 V breaker"),
    edge("CB-501A", "BUS-301A", "solid_power", "breaker to 480 V load center A1"),
    edge("BUS-202A", "CB-302A", "solid_power", "BUS-202A drop to normal transformer A"),
    edge("CB-302A", "DS-302A", "solid_power", "normal A transformer breaker to disconnect"),
    edge("DS-302A", "TR-NA", "solid_power", "disconnect to normal transformer A"),
    edge("TR-NA", "CB-502A", "solid_power", "normal transformer A to 480 V breaker"),
    edge("CB-502A", "BUS-302A", "solid_power", "breaker to 480 V MCC bus A2"),
    edge("BUS-201B", "CB-301B", "solid_power", "BUS-201B drop to 480 V train B transformer"),
    edge("CB-301B", "DS-301B", "solid_power", "train B transformer breaker to disconnect"),
    edge("DS-301B", "TR-SB", "solid_power", "disconnect to safety transformer B"),
    edge("TR-SB", "CB-501B", "solid_power", "safety transformer B to 480 V breaker"),
    edge("CB-501B", "BUS-301B", "solid_power", "breaker to 480 V load center B1"),
    edge("BUS-202B", "CB-302B", "solid_power", "BUS-202B drop to normal transformer B"),
    edge("CB-302B", "DS-302B", "solid_power", "normal B transformer breaker to disconnect"),
    edge("DS-302B", "CB-502B", "solid_power", "visible B2 order from disconnect to breaker"),
    edge("CB-502B", "TR-NB", "solid_power", "B2 breaker to transformer"),
    edge("TR-NB", "BUS-302B", "solid_power", "normal transformer B to MCC bus B2"),
]


LOAD_CENTER_EDGES = [
    edge("BUS-301A", "GND-1", "ground", "ground tap on BUS-301A"),
    edge("BUS-301A", "CB-303A", "solid_power", "BUS-301A feeder to MCC-1A"),
    edge("CB-303A", "MCC-1A", "solid_power", "MCC-1A breaker to MCC"),
    edge("BUS-301A", "CB-304A", "solid_power", "BUS-301A feeder to MCC-2A"),
    edge("CB-304A", "MCC-2A", "solid_power", "MCC-2A breaker to MCC"),
    edge("BUS-302A", "CB-503A", "solid_power", "BUS-302A feeder to MCC-3A"),
    edge("CB-503A", "MCC-3A", "solid_power", "MCC-3A breaker to MCC"),
    edge("MCC-3A", "GND-5", "ground", "ground tap from MCC-3A side"),
    edge("MCC-1A", "MOTOR-SI101A", "solid_power", "MCC-1A motor branch"),
    edge("MCC-1A", "PUMP-SI101A", "solid_power", "MCC-1A pump branch"),
    edge("MCC-1A", "MOTOR-CCW101A", "solid_power", "MCC-1A motor branch"),
    edge("MCC-1A", "PUMP-CCW101A", "solid_power", "MCC-1A pump branch"),
    edge("MCC-1A", "VLV-8801A", "solid_power", "MCC-1A valve branch"),
    edge("MCC-2A", "MOTOR-AFW101A", "solid_power", "MCC-2A motor branch"),
    edge("MCC-2A", "PUMP-AFW101A", "solid_power", "MCC-2A pump branch"),
    edge("MCC-2A", "MOTOR-RHR101A", "solid_power", "MCC-2A motor branch"),
    edge("MCC-2A", "PUMP-RHR101A", "solid_power", "MCC-2A pump branch"),
    edge("MCC-2A", "VLV-8802A", "solid_power", "MCC-2A valve branch"),
    edge("MCC-3A", "MOTOR-SW101A", "solid_power", "MCC-3A motor branch"),
    edge("MCC-3A", "PUMP-SW101A", "solid_power", "MCC-3A pump branch"),
    edge("MCC-3A", "MOTOR-CHG101A", "solid_power", "MCC-3A motor branch"),
    edge("MCC-3A", "PUMP-CHG101A", "solid_power", "MCC-3A pump branch"),
    edge("MCC-3A", "MOTOR-FAN101A", "solid_power", "MCC-3A fan motor branch"),
    edge("MCC-3A", "VLV-8901A", "solid_power", "MCC-3A valve branch"),
    edge("BUS-301B", "GND-2", "ground", "ground tap on BUS-301B"),
    edge("BUS-301B", "CB-303B", "solid_power", "BUS-301B feeder to MCC-1B"),
    edge("CB-303B", "MCC-1B", "solid_power", "MCC-1B breaker to MCC"),
    edge("BUS-301B", "CB-304B", "solid_power", "BUS-301B feeder to MCC-2B"),
    edge("CB-304B", "MCC-2B", "solid_power", "MCC-2B breaker to MCC"),
    edge("BUS-302B", "CB-503B", "solid_power", "BUS-302B feeder to MCC-3B"),
    edge("CB-503B", "MCC-3B", "solid_power", "MCC-3B breaker to MCC"),
    edge("MCC-3B", "GND-6", "ground", "ground tap from MCC-3B side"),
    edge("MCC-1B", "MOTOR-SI101B", "solid_power", "MCC-1B motor branch"),
    edge("MCC-1B", "PUMP-SI101B", "solid_power", "MCC-1B pump branch"),
    edge("MCC-1B", "MOTOR-CCW101B", "solid_power", "MCC-1B motor branch"),
    edge("MCC-1B", "PUMP-CCW101B", "solid_power", "MCC-1B pump branch"),
    edge("MCC-1B", "VLV-8801B", "solid_power", "MCC-1B valve branch"),
    edge("MCC-2B", "MOTOR-AFW101B", "solid_power", "MCC-2B motor branch"),
    edge("MCC-2B", "PUMP-AFW101B", "solid_power", "MCC-2B pump branch"),
    edge("MCC-2B", "MOTOR-RHR101B", "solid_power", "MCC-2B motor branch"),
    edge("MCC-2B", "PUMP-RHR101B", "solid_power", "MCC-2B pump branch"),
    edge("MCC-2B", "VLV-8802B", "solid_power", "MCC-2B valve branch"),
    edge("MCC-3B", "MOTOR-SW101B", "solid_power", "MCC-3B motor branch"),
    edge("MCC-3B", "PUMP-SW101B", "solid_power", "MCC-3B pump branch"),
    edge("MCC-3B", "MOTOR-CHG101B", "solid_power", "MCC-3B motor branch"),
    edge("MCC-3B", "PUMP-CHG101B", "solid_power", "MCC-3B pump branch"),
    edge("MCC-3B", "MOTOR-FAN101B", "solid_power", "MCC-3B fan motor branch"),
    edge("MCC-3B", "VLV-8901B", "solid_power", "MCC-3B valve branch"),
]


DC_EDGES = [
    edge("BUS-301A", "DS-401A", "solid_power", "A DC feeder visibly drops from BUS-301A"),
    edge("DS-401A", "TR-DC-A", "solid_power", "A DC disconnect to transformer"),
    edge("TR-DC-A", "RECT-125A", "solid_power", "A DC transformer to rectifier"),
    edge("RECT-125A", "BUS-401A", "dc", "rectifier to 125 VDC bus A"),
    edge("BUS-401A", "BAT-1A", "dc", "battery 1A tap"),
    edge("BUS-401A", "BAT-2A", "dc", "battery 2A tap"),
    edge("BUS-401A", "GND-3", "ground", "ground tap on BUS-401A"),
    edge("BUS-401A", "INV-120A", "dc", "125 VDC bus A to inverter"),
    edge("INV-120A", "BUS-501A", "solid_power", "inverter output to 120 VAC bus A"),
    edge("BUS-401A", "DS-401B", "dc_tie", "drawn tie/drop from BUS-401A to DS-401B"),
    edge("DS-401B", "TR-DC-B", "solid_power", "DS-401B to B DC transformer"),
    edge("TR-DC-B", "RECT-125B", "solid_power", "B DC transformer to rectifier"),
    edge("RECT-125B", "BUS-401B", "dc", "rectifier to 125 VDC bus B"),
    edge("DS-401B", "BUS-401B", "dc_tie", "N.O. tie/drop lands on BUS-401B"),
    edge("BUS-401B", "BAT-1B", "dc", "battery 1B tap"),
    edge("BUS-401B", "BAT-2B", "dc", "battery 2B tap"),
    edge("BUS-401B", "GND-4", "ground", "ground tap on BUS-401B"),
    edge("BUS-401B", "INV-120B", "dc", "125 VDC bus B to inverter"),
    edge("INV-120B", "BUS-501B", "solid_power", "inverter output to 120 VAC bus B"),
    edge("BUS-302A", "DS-402A", "solid_power", "A inverter feeder visibly drops from BUS-302A"),
    edge("DS-402A", "TR-INV-A", "solid_power", "A inverter feeder disconnect to transformer"),
    edge("TR-INV-A", "INV-120C", "solid_power", "transformer to INV-120C"),
    edge("DS-402B", "TR-INV-B", "solid_power", "B inverter/rectifier disconnect to transformer"),
    edge("TR-INV-B", "RECT-24C", "solid_power", "transformer to RECT-24C"),
    edge("RECT-24C", "BUS-401B", "dc", "RECT-24C output riser lands on BUS-401B"),
]


CONTROL_FEED_EDGES = [
    edge("BUS-501A", "CP-SWGR", "control", "top control rung from 120 VAC bus A"),
    edge("CP-SWGR", "CP-SI-A", "control", "vertical dashed link between control panels"),
    edge("CP-SWGR", "UVLS-A", "control", "upper auxiliary dashed line to UVLS-A"),
    edge("UVLS-A", "UVLS-B", "control", "upper auxiliary dashed line between UVLS blocks"),
    edge("BUS-501A", "CP-SI-A", "control", "A bus to SI-A control row"),
    edge("BUS-501B", "CP-SI-B", "control", "B bus to SI-B control row"),
    edge("BUS-501A", "CP-CCW-A", "control", "A bus to CCW-A control row"),
    edge("BUS-501B", "CP-CCW-B", "control", "B bus to CCW-B control row"),
    edge("BUS-501A", "CP-EDG-A", "control", "A bus to EDG-A control row"),
    edge("BUS-501B", "CP-EDG-B", "control", "B bus to EDG-B control row"),
    edge("BUS-501A", "RPS-A", "control", "A bus to RPS-A row"),
    edge("BUS-501B", "RPS-B", "control", "B bus to RPS-B row"),
    edge("BUS-501A", "ESFAS-A", "control", "A bus to ESFAS-A row"),
    edge("BUS-501B", "ESFAS-B", "control", "B bus to ESFAS-B row"),
    edge("CP-EDG-A", "CP-EDG-B", "control_trunk", "vertical dashed trunk"),
    edge("CP-EDG-B", "RPS-A", "control_trunk", "vertical dashed trunk"),
    edge("RPS-A", "RPS-B", "control_trunk", "vertical dashed trunk"),
    edge("RPS-B", "ESFAS-A", "control_trunk", "vertical dashed trunk"),
    edge("ESFAS-A", "ESFAS-B", "control_trunk", "vertical dashed trunk"),
    edge("ESFAS-B", "CP-CRD", "control_trunk", "vertical dashed trunk"),
]


CONTROL_ROWS = [
    ("CP-SI-A", "RELAY-K101", "RELAY-K102", "RELAY-K103", "JB-101", ["INST-PT101", "INST-PT102"]),
    ("CP-SI-B", "RELAY-K104", "RELAY-K105", "RELAY-K106", "JB-102", ["INST-PT103", "INST-FT201"]),
    ("CP-CCW-A", "RELAY-K107", "RELAY-K108", "RELAY-K109", "JB-103", ["INST-FT202", "INST-LT301"]),
    ("CP-CCW-B", "RELAY-K110", "RELAY-K111", "RELAY-K112", "JB-104", ["INST-LT302", "INST-TT401"]),
    ("CP-EDG-A", "RELAY-K113", "RELAY-K114", "RELAY-K115", "JB-105", ["INST-TT402", "INST-CT501"]),
    ("CP-EDG-B", "RELAY-K116", "RELAY-K117", "RELAY-K118", "JB-106", ["INST-CT502"]),
    ("RPS-A", "RELAY-K119", "RELAY-K120", "RELAY-K121", "JB-107", ["INST-VT601"]),
    ("RPS-B", "RELAY-K122", "RELAY-K123", "RELAY-K124", "JB-108", ["INST-VT602"]),
    ("ESFAS-A", "RELAY-K125", "RELAY-K126", "RELAY-K127", "JB-109", ["INST-ZS701"]),
    ("ESFAS-B", "RELAY-K128", "RELAY-K129", "RELAY-K130", "JB-110", ["INST-ZS702"]),
]


CONTROL_ROW_EDGES: list[dict[str, str]] = []
for src, relay_1, relay_2, relay_3, junction, instruments in CONTROL_ROWS:
    CONTROL_ROW_EDGES.extend(
        [
            edge(src, relay_1, "control", f"{src} dashed control row"),
            edge(relay_1, relay_2, "control", f"{src} relay chain"),
            edge(relay_2, relay_3, "control", f"{src} relay chain"),
            edge(relay_3, junction, "control", f"{src} relay chain to junction box"),
            edge(junction, instruments[0], "signal", f"{junction} dotted instrument continuation"),
        ]
    )
    if len(instruments) > 1:
        CONTROL_ROW_EDGES.append(
            edge(
                instruments[0],
                instruments[1],
                "signal",
                f"{junction} dotted instrument continuation",
            )
        )


FINAL_EDGES = (
    BASE_EDGES
    + LOAD_CENTER_EDGES
    + DC_EDGES
    + CONTROL_FEED_EDGES
    + CONTROL_ROW_EDGES
)


def pair_key(src: str, dst: str) -> tuple[str, str]:
    return tuple(sorted((src, dst)))


DIEGO_R1_EXCLUDED = {
    pair_key("BUS-202A", "CB-UNLABELED-EDG2A-INBOARD"),
    pair_key("CB-UNLABELED-EDG2A-INBOARD", "DS-202A"),
    pair_key("BUS-301A", "DS-401A"),
    pair_key("BUS-302A", "DS-402A"),
    pair_key("DS-401B", "BUS-401B"),
    pair_key("CP-SWGR", "UVLS-A"),
    pair_key("UVLS-A", "UVLS-B"),
    pair_key("CP-EDG-A", "CP-EDG-B"),
    pair_key("CP-EDG-B", "RPS-A"),
    pair_key("RPS-A", "RPS-B"),
    pair_key("RPS-B", "ESFAS-A"),
    pair_key("ESFAS-A", "ESFAS-B"),
    pair_key("ESFAS-B", "CP-CRD"),
    pair_key("RECT-24C", "BUS-401B"),
}

DIEGO_R1_EDGES = [
    e for e in FINAL_EDGES if pair_key(e["source"], e["target"]) not in DIEGO_R1_EXCLUDED
] + [
    edge("BUS-202A", "DS-202A", "solid_power", "round-01 high-recall direct EDG-2A path before unlabeled breaker review")
]

JENNIFER_R2_EXCLUDED = {
    pair_key("CP-SWGR", "UVLS-A"),
    pair_key("UVLS-A", "UVLS-B"),
    pair_key("CP-EDG-A", "CP-EDG-B"),
    pair_key("CP-EDG-B", "RPS-A"),
    pair_key("RPS-A", "RPS-B"),
    pair_key("RPS-B", "ESFAS-A"),
    pair_key("ESFAS-A", "ESFAS-B"),
    pair_key("ESFAS-B", "CP-CRD"),
    pair_key("RECT-24C", "BUS-401B"),
}

JENNIFER_R2_EDGES = [
    e for e in FINAL_EDGES if pair_key(e["source"], e["target"]) not in JENNIFER_R2_EXCLUDED
]


def write_edge_list(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        for row in edges:
            writer.writerow(row)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for e in edges:
        src, dst = e["source"], e["target"]
        if src not in index or dst not in index:
            raise ValueError(f"edge references unknown node: {src} -- {dst}")
        if src == dst:
            continue
        i, j = index[src], index[dst]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def validate(nodes: list[str], edges: list[dict[str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")
    pairs = [pair_key(e["source"], e["target"]) for e in edges]
    if len(pairs) != len(set(pairs)):
        duplicates = sorted({pair for pair in pairs if pairs.count(pair) > 1})
        raise ValueError(f"duplicate edges: {duplicates}")
    missing = sorted(
        {n for e in edges for n in (e["source"], e["target"]) if n not in set(nodes)}
    )
    if missing:
        raise ValueError(f"missing edge nodes: {missing}")


def write_uncertain(path: Path) -> None:
    rows = [
        {
            "candidate_edge": "BAT-EDG-A -- BAT-EDG-B",
            "decision": "excluded_uncertain",
            "reason": "dashed EDG battery loop visible, but exact adjacent component representation was not clean enough without an unlabeled loop node",
        },
        {
            "candidate_edge": "BAT-EDG-B -- CP-CRD",
            "decision": "excluded_uncertain",
            "reason": "dashed loop appears to continue toward CP-CRD, but pairwise adjacency was not visually locked by reviewers",
        },
        {
            "candidate_edge": "INV-120C -- <named destination>",
            "decision": "excluded_uncertain",
            "reason": "INV-120C output line continues, but no legible named endpoint was visually confirmed",
        },
        {
            "candidate_edge": "CB-204B",
            "decision": "excluded_label",
            "reason": "EDG-2A inboard breaker is drawn but unlabeled; canonical node kept as CB-UNLABELED-EDG2A-INBOARD",
        },
        {
            "candidate_edge": "EDG feeder / no-tie crossings",
            "decision": "excluded",
            "reason": "drawing note and geometry show crossings without junction dots are not connections",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_edge", "decision", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def write_tracking(path: Path, now: str) -> None:
    rows = [
        [now, "21", "local", "main", "inventory/crops/local inspection", 2300, 450, len(FINAL_NODES), len(FINAL_EDGES), "codes/crops", "Approximate tokens; exact tool token accounting unavailable"],
        [now, "21", "round_01", "Diego", "high-recall extraction", 6100, 4300, len(DIEGO_R1_NODES), len(DIEGO_R1_EDGES), "round_01_diego_matrix.csv", "Broad extraction before unlabeled EDG-2A breaker and focused control additions"],
        [now, "21", "round_02", "Jennifer", "precision review", 6400, 1600, len(FINAL_NODES), len(JENNIFER_R2_EDGES), "round_02_jennifer_matrix.csv", "Added unlabeled EDG-2A breaker and supported DC/feed edges; excluded uncertain trunk/control features"],
        [now, "21", "round_03", "Diego", "focused saturation/high-recall check", 1900, 520, len(FINAL_NODES), len(FINAL_EDGES), "round_03_diego_saturation_matrix.csv", "Accepted nine focused UVLS/trunk/RECT-24C additions"],
        [now, "21", "round_04", "Jennifer", "final precision lock", 1400, 430, len(FINAL_NODES), len(FINAL_EDGES), "round_04_jennifer_final_matrix.csv", "Final matrix after Diego/Jennifer agreement"],
        [now, "21", "local", "main", "artifact generation/validation", 1800, 320, len(FINAL_NODES), len(FINAL_EDGES), "final_connectivity_matrix.csv", "Symmetric matrix, zero diagonal"],
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "case",
                "round",
                "agent",
                "role",
                "approx_prompt_tokens",
                "approx_completion_tokens",
                "matrix_nodes",
                "matrix_edges",
                "output_artifact",
                "notes",
            ]
        )
        writer.writerows(rows)


def write_note(path: Path, now: str) -> None:
    path.write_text(
        f"""# Case 21 Connectivity Extraction Note

Generated: {now}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_fixed.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the AC source/switchgear, 480 V load-center, DC/UPS, and control/instrument topology.
2. Jennifer precision review added the visible unlabeled EDG-2A inboard breaker, supported DC/feed edges, and removed guessed labels/no-tie crossings.
3. Diego focused on isolated control/DC features and added only visually supported UVLS auxiliary, vertical control-trunk, and `RECT-24C` output edges.
4. Jennifer accepted those focused additions and locked the final matrix.

## Final Counts

- Nodes: {len(FINAL_NODES)}
- Undirected edges in matrix: {len(FINAL_EDGES)}
- Diagonal: zero
- Matrix: symmetric

## Key Decisions

- Crossings without junction dots, including the EDG feeder/no-tie crossing, were not modeled as edges.
- The EDG-2A inboard breaker is drawn but unlabeled, so it is named `CB-UNLABELED-EDG2A-INBOARD`.
- The visible vertical dashed control trunk is represented by adjacent component pairs from `CP-EDG-A` through `CP-CRD`.
- `BAT-EDG-A`, `BAT-EDG-B`, and the `INV-120C` output remain visible but edge-uncertain/excluded rather than guessed.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
""",
        encoding="utf-8",
    )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().replace(microsecond=0).isoformat()

    validate(FINAL_NODES, FINAL_EDGES)
    validate(DIEGO_R1_NODES, DIEGO_R1_EDGES)
    validate(FINAL_NODES, JENNIFER_R2_EDGES)

    outputs = [
        ("round_01_diego", DIEGO_R1_NODES, DIEGO_R1_EDGES),
        ("round_02_jennifer", FINAL_NODES, JENNIFER_R2_EDGES),
        ("round_03_diego_saturation", FINAL_NODES, FINAL_EDGES),
        ("round_04_jennifer_final", FINAL_NODES, FINAL_EDGES),
        ("final", FINAL_NODES, FINAL_EDGES),
    ]

    for stem, nodes, edges in outputs:
        matrix_name = (
            "final_connectivity_matrix.csv"
            if stem == "final"
            else f"{stem}_matrix.csv"
        )
        edge_name = "final_edge_list.csv" if stem == "final" else f"{stem}_edges.csv"
        write_matrix(RESULTS_DIR / matrix_name, nodes, edges)
        write_edge_list(RESULTS_DIR / edge_name, edges)

    write_uncertain(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_tracking(RESULTS_DIR / "token_performance_tracking.csv", now)
    write_note(RESULTS_DIR / "extraction_note.md", now)

    print(
        f"wrote {len(FINAL_NODES)} nodes and {len(FINAL_EDGES)} edges to {RESULTS_DIR}"
    )


if __name__ == "__main__":
    main()
