from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw")
RESULTS = BASE / "results"
TRAINS = ["A", "B", "C", "D"]


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    evidence: str
    status: str = "confirmed"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[str]
    edges: list[Edge]
    uncertain_edges: list[Edge]
    include_uncertain_in_matrix: bool
    notes: list[str]


def edge(source: str, target: str, evidence: str, status: str = "confirmed") -> Edge:
    return Edge(source, target, evidence, status)


def chain(items: list[str], evidence: str) -> list[Edge]:
    return [edge(a, b, evidence) for a, b in zip(items, items[1:])]


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    result: list[Edge] = []
    for item in edges:
        key = edge_key(item.source, item.target)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


TOP_NODES = [
    "GEN-01",
    "TR-UAT-1",
    "CB-UAT-1",
    "TR-SUT-1",
    "CB-SUT-1",
    "BUS-13-8A",
    "CB-13-TIE",
    "BUS-13-8B",
    "GEN-02",
    "TR-UAT-2",
    "CB-UAT-2",
    "TR-SUT-2",
    "CB-SUT-2",
]


def train_nodes(x: str) -> list[str]:
    return [
        f"CB-IN-{x}",
        f"RELAY-27{x}",
        f"DG-1{x}",
        f"CB-DG-{x}",
        f"BUS-4160-{x}",
        f"CB-4160-{x}1",
        f"TR-480-{x}1",
        f"CB-480-{x}1",
        f"BUS-480-{x}1",
        f"CB-4160-{x}2",
        f"TR-480-{x}2",
        f"CB-480-{x}2",
        f"BUS-480-{x}2",
        f"CB-MCC-{x}1",
        f"MCC-{x}1",
        f"CB-MCC-{x}2",
        f"MCC-{x}2",
        f"PUMP-SI-{x}",
        f"PUMP-CCW-{x}",
        f"FAN-HVAC-{x}",
        f"MOV-RHR-{x}",
        f"RECT-125-{x}",
        f"PANEL-IC-{x}",
        f"GND-{x}",
    ]


SHARED_DC_CONTROL_NODES = [
    "BAT-125A",
    "BUS-DC-125A",
    "INV-UPS-A",
    "PANEL-RPS-A",
    "BAT-125B",
    "BUS-DC-125B",
    "INV-UPS-B",
    "PANEL-RPS-B",
    "PANEL-SSPS",
    "ATS-480-A",
    "ATS-480-B",
]

FINAL_NODES = TOP_NODES + [node for x in TRAINS for node in train_nodes(x)] + SHARED_DC_CONTROL_NODES

TOP_HELPER_NODES = [
    "13.8KV-1A",
    "UAT1-SEC",
    "SUT1-SEC",
    "13T-A",
    "13T-B",
    "13.8KV-2A",
    "UAT2-SEC",
    "SUT2-SEC",
]

TRAIN_HELPER_NODES = [item for x in TRAINS for item in (f"FDR-{x}1", f"FDR-{x}2", f"TIE-{x}12")]

CONTROL_HELPER_NODES = [
    "ATS-A1",
    "ATS-B1",
    "ATS-C1",
    "ATS-D1",
    "ATS-AOUT",
    "ATS-BOUT",
    "SSPS-A",
    "SSPS-B",
    "SSPS-C",
    "SSPS-D",
    "DC-A125",
    "DC-B125",
    "DC-C125",
    "DC-D125",
]

DIEGO_R1_NODES = FINAL_NODES + TOP_HELPER_NODES + TRAIN_HELPER_NODES + CONTROL_HELPER_NODES


def top_final_edges() -> list[Edge]:
    return dedupe_edges(
        chain(["GEN-01", "TR-UAT-1", "CB-UAT-1", "BUS-13-8A"], "solid GEN-01/UAT feed to 13.8 kV bus A")
        + chain(["TR-SUT-1", "CB-SUT-1", "BUS-13-8A"], "solid SUT-1 feed to 13.8 kV bus A")
        + chain(["BUS-13-8A", "CB-13-TIE", "BUS-13-8B"], "solid 13.8 kV bus tie through CB-13-TIE")
        + chain(["GEN-02", "TR-UAT-2", "CB-UAT-2", "BUS-13-8B"], "solid GEN-02/UAT feed to 13.8 kV bus B")
        + chain(["TR-SUT-2", "CB-SUT-2", "BUS-13-8B"], "solid SUT-2 feed to 13.8 kV bus B")
        + [
            edge("BUS-13-8A", "CB-IN-A", "solid normal incoming feeder drop to Train A"),
            edge("BUS-13-8A", "CB-IN-B", "solid normal incoming feeder drop to Train B"),
            edge("BUS-13-8B", "CB-IN-C", "solid normal incoming feeder drop to Train C"),
            edge("BUS-13-8B", "CB-IN-D", "solid normal incoming feeder drop to Train D"),
        ]
    )


def top_diego_edges() -> list[Edge]:
    return dedupe_edges(
        chain(["GEN-01", "13.8KV-1A", "TR-UAT-1", "UAT1-SEC", "CB-UAT-1", "BUS-13-8A"], "Diego round 1 included conductor/section labels as plausible nodes")
        + chain(["TR-SUT-1", "SUT1-SEC", "CB-SUT-1", "BUS-13-8A"], "Diego round 1 included SUT section label as plausible node")
        + chain(["BUS-13-8A", "13T-A", "CB-13-TIE", "13T-B", "BUS-13-8B"], "Diego round 1 included tie side labels as plausible nodes")
        + chain(["GEN-02", "13.8KV-2A", "TR-UAT-2", "UAT2-SEC", "CB-UAT-2", "BUS-13-8B"], "Diego round 1 included conductor/section labels as plausible nodes")
        + chain(["TR-SUT-2", "SUT2-SEC", "CB-SUT-2", "BUS-13-8B"], "Diego round 1 included SUT section label as plausible node")
        + [
            edge("BUS-13-8A", "CB-IN-A", "solid normal incoming feeder drop to Train A"),
            edge("BUS-13-8A", "CB-IN-B", "solid normal incoming feeder drop to Train B"),
            edge("BUS-13-8B", "CB-IN-C", "solid normal incoming feeder drop to Train C"),
            edge("BUS-13-8B", "CB-IN-D", "solid normal incoming feeder drop to Train D"),
        ]
    )


def train_final_edges(x: str) -> list[Edge]:
    return [
        edge(f"CB-IN-{x}", f"BUS-4160-{x}", "solid incoming feeder to 4.16 kV safety bus"),
        edge(f"DG-1{x}", f"CB-DG-{x}", "solid diesel generator feeder to DG breaker"),
        edge(f"CB-DG-{x}", f"BUS-4160-{x}", "solid DG breaker feeder to 4.16 kV bus"),
        edge(f"CB-IN-{x}", f"RELAY-27{x}", "dashed undervoltage/control interlock path"),
        edge(f"RELAY-27{x}", f"CB-DG-{x}", "dashed undervoltage/control interlock path"),
        edge(f"BUS-4160-{x}", f"CB-4160-{x}1", "solid 4.16 kV branch to transformer 1"),
        edge(f"CB-4160-{x}1", f"TR-480-{x}1", "solid breaker-to-transformer branch"),
        edge(f"TR-480-{x}1", f"CB-480-{x}1", "solid transformer low-side branch"),
        edge(f"CB-480-{x}1", f"BUS-480-{x}1", "solid 480 V breaker-to-bus branch"),
        edge(f"BUS-4160-{x}", f"CB-4160-{x}2", "solid 4.16 kV branch to transformer 2"),
        edge(f"CB-4160-{x}2", f"TR-480-{x}2", "solid breaker-to-transformer branch"),
        edge(f"TR-480-{x}2", f"CB-480-{x}2", "solid transformer low-side branch"),
        edge(f"CB-480-{x}2", f"BUS-480-{x}2", "solid 480 V breaker-to-bus branch"),
        edge(f"BUS-480-{x}1", f"BUS-480-{x}2", "continuous solid 480 V tie conductor; TIE label not used as node"),
        edge(f"BUS-480-{x}1", f"CB-MCC-{x}1", "solid feeder from 480 V bus 1 to MCC breaker"),
        edge(f"CB-MCC-{x}1", f"MCC-{x}1", "solid MCC breaker-to-MCC connection"),
        edge(f"BUS-480-{x}2", f"CB-MCC-{x}2", "solid feeder from 480 V bus 2 to MCC breaker"),
        edge(f"CB-MCC-{x}2", f"MCC-{x}2", "solid MCC breaker-to-MCC connection"),
        edge(f"MCC-{x}1", f"PUMP-SI-{x}", "solid MCC load feeder"),
        edge(f"MCC-{x}1", f"PUMP-CCW-{x}", "solid MCC load feeder"),
        edge(f"MCC-{x}1", f"FAN-HVAC-{x}", "solid MCC load feeder"),
        edge(f"MCC-{x}2", f"MOV-RHR-{x}", "solid MCC load feeder to MOV"),
        edge(f"BUS-480-{x}2", f"RECT-125-{x}", "solid 125 VDC rectifier supply from 480 V bus 2"),
        edge(f"RECT-125-{x}", f"PANEL-IC-{x}", "solid rectifier/DC conductor through I/C panel terminal"),
        edge(f"PANEL-IC-{x}", f"GND-{x}", "visible grounded terminal from I/C panel"),
    ]


def train_diego_edges(x: str) -> list[Edge]:
    edges = [
        edge(f"CB-IN-{x}", f"BUS-4160-{x}", "solid incoming feeder to 4.16 kV safety bus"),
        edge(f"DG-1{x}", f"CB-DG-{x}", "solid diesel generator feeder to DG breaker"),
        edge(f"CB-DG-{x}", f"BUS-4160-{x}", "solid DG breaker feeder to 4.16 kV bus"),
        edge(f"CB-IN-{x}", f"RELAY-27{x}", "dashed undervoltage/control interlock path"),
        edge(f"RELAY-27{x}", f"CB-DG-{x}", "dashed undervoltage/control interlock path"),
        edge(f"RELAY-27{x}", f"SSPS-{x}", "Diego round 1 high-recall dashed vertical relay-to-SSPS label path"),
        edge(f"BUS-4160-{x}", f"FDR-{x}1", "Diego round 1 treated feeder label as plausible node"),
        edge(f"FDR-{x}1", f"CB-4160-{x}1", "Diego round 1 treated feeder label as plausible node"),
        edge(f"CB-4160-{x}1", f"TR-480-{x}1", "solid breaker-to-transformer branch"),
        edge(f"TR-480-{x}1", f"CB-480-{x}1", "solid transformer low-side branch"),
        edge(f"CB-480-{x}1", f"BUS-480-{x}1", "solid 480 V breaker-to-bus branch"),
        edge(f"BUS-4160-{x}", f"FDR-{x}2", "Diego round 1 treated feeder label as plausible node"),
        edge(f"FDR-{x}2", f"CB-4160-{x}2", "Diego round 1 treated feeder label as plausible node"),
        edge(f"CB-4160-{x}2", f"TR-480-{x}2", "solid breaker-to-transformer branch"),
        edge(f"TR-480-{x}2", f"CB-480-{x}2", "solid transformer low-side branch"),
        edge(f"CB-480-{x}2", f"BUS-480-{x}2", "solid 480 V breaker-to-bus branch"),
        edge(f"BUS-480-{x}1", f"TIE-{x}12", "Diego round 1 treated tie label as plausible node"),
        edge(f"TIE-{x}12", f"BUS-480-{x}2", "Diego round 1 treated tie label as plausible node"),
        edge(f"BUS-480-{x}1", f"CB-MCC-{x}1", "solid feeder from 480 V bus 1 to MCC breaker"),
        edge(f"CB-MCC-{x}1", f"MCC-{x}1", "solid MCC breaker-to-MCC connection"),
        edge(f"BUS-480-{x}2", f"CB-MCC-{x}2", "solid feeder from 480 V bus 2 to MCC breaker"),
        edge(f"CB-MCC-{x}2", f"MCC-{x}2", "solid MCC breaker-to-MCC connection"),
        edge(f"MCC-{x}1", f"PUMP-SI-{x}", "solid MCC load feeder"),
        edge(f"MCC-{x}1", f"PUMP-CCW-{x}", "solid MCC load feeder"),
        edge(f"MCC-{x}1", f"FAN-HVAC-{x}", "solid MCC load feeder"),
        edge(f"MCC-{x}2", f"MOV-RHR-{x}", "solid MCC load feeder to MOV"),
        edge(f"BUS-480-{x}2", f"RECT-125-{x}", "solid 125 VDC rectifier supply from 480 V bus 2"),
        edge(f"RECT-125-{x}", f"PANEL-IC-{x}", "solid rectifier/DC conductor through I/C panel terminal"),
        edge(f"PANEL-IC-{x}", f"GND-{x}", "visible grounded terminal from I/C panel"),
    ]
    return edges


def dc_bus_for_train(x: str) -> str:
    return "BUS-DC-125A" if x == "A" else "BUS-DC-125B"


def final_dc_edges() -> list[Edge]:
    return [
        edge("PANEL-IC-A", "BUS-DC-125A", "solid DC-A125 landing to Division A DC bus"),
        edge("PANEL-IC-B", "BUS-DC-125B", "solid DC-B125 route into Division B DC bus area"),
        edge("PANEL-IC-C", "BUS-DC-125B", "solid DC-C125 route into Division B DC bus area"),
        edge("PANEL-IC-D", "BUS-DC-125B", "solid DC-D125 route into Division B DC bus area"),
        edge("BAT-125A", "BUS-DC-125A", "solid battery A connection to DC bus"),
        edge("BUS-DC-125A", "INV-UPS-A", "solid UPS-AIN connection from DC bus"),
        edge("INV-UPS-A", "PANEL-RPS-A", "solid UPS-AOUT connection to RPS panel"),
        edge("BAT-125B", "BUS-DC-125B", "solid battery B connection to DC bus"),
        edge("BUS-DC-125B", "INV-UPS-B", "solid UPS-BIN connection from DC bus"),
        edge("INV-UPS-B", "PANEL-RPS-B", "solid UPS-BOUT connection to RPS panel"),
        edge("MCC-A1", "ATS-480-A", "solid ATS-A1 route from A-side MCC branch to ATS-480-A"),
        edge("MCC-B1", "ATS-480-A", "solid ATS-B1 route from B-side MCC branch to ATS-480-A"),
        edge("ATS-480-A", "PANEL-RPS-A", "solid ATS-AOUT route to PANEL-RPS-A"),
        edge("MCC-C1", "ATS-480-B", "solid ATS-C1 route from C-side MCC branch to ATS-480-B"),
        edge("MCC-D1", "ATS-480-B", "solid ATS-D1 route from D-side MCC branch to ATS-480-B"),
        edge("ATS-480-B", "PANEL-RPS-B", "solid ATS-BOUT route to PANEL-RPS-B"),
    ]


def diego_dc_edges() -> list[Edge]:
    return [
        edge("PANEL-IC-A", "DC-A125", "Diego round 1 retained conductor label for DC-A125 landing"),
        edge("DC-A125", "BUS-DC-125A", "Diego round 1 retained conductor label for DC-A125 landing"),
        edge("PANEL-IC-B", "DC-B125", "Diego round 1 retained conductor label for DC-B125 landing"),
        edge("DC-B125", "BUS-DC-125B", "Diego round 1 plausible DC-B125 landing"),
        edge("PANEL-IC-C", "DC-C125", "Diego round 1 retained conductor label for DC-C125 landing"),
        edge("DC-C125", "BUS-DC-125B", "Diego round 1 plausible DC-C125 landing"),
        edge("PANEL-IC-D", "DC-D125", "Diego round 1 retained conductor label for DC-D125 landing"),
        edge("DC-D125", "BUS-DC-125B", "Diego round 1 plausible DC-D125 landing"),
        edge("BAT-125A", "BUS-DC-125A", "solid battery A connection to DC bus"),
        edge("BUS-DC-125A", "INV-UPS-A", "solid UPS-AIN connection from DC bus"),
        edge("INV-UPS-A", "PANEL-RPS-A", "solid UPS-AOUT connection to RPS panel"),
        edge("BAT-125B", "BUS-DC-125B", "solid battery B connection to DC bus"),
        edge("BUS-DC-125B", "INV-UPS-B", "solid UPS-BIN connection from DC bus"),
        edge("INV-UPS-B", "PANEL-RPS-B", "solid UPS-BOUT connection to RPS panel"),
        edge("MCC-A1", "ATS-A1", "Diego round 1 retained ATS-A1 conductor label"),
        edge("ATS-A1", "ATS-480-A", "Diego round 1 retained ATS-A1 conductor label"),
        edge("MCC-B1", "ATS-B1", "Diego round 1 retained ATS-B1 conductor label"),
        edge("ATS-B1", "ATS-480-A", "Diego round 1 retained ATS-B1 conductor label"),
        edge("ATS-480-A", "ATS-AOUT", "Diego round 1 retained ATS-AOUT conductor label"),
        edge("ATS-AOUT", "PANEL-RPS-A", "Diego round 1 retained ATS-AOUT conductor label"),
        edge("MCC-C1", "ATS-C1", "Diego round 1 retained ATS-C1 conductor label"),
        edge("ATS-C1", "ATS-480-B", "Diego round 1 retained ATS-C1 conductor label"),
        edge("MCC-D1", "ATS-D1", "Diego round 1 retained ATS-D1 conductor label"),
        edge("ATS-D1", "ATS-480-B", "Diego round 1 retained ATS-D1 conductor label"),
        edge("ATS-480-B", "ATS-BOUT", "Diego round 1 retained ATS-BOUT conductor label"),
        edge("ATS-BOUT", "PANEL-RPS-B", "Diego round 1 retained ATS-BOUT conductor label"),
    ]


FINAL_EDGES = dedupe_edges(top_final_edges() + [item for x in TRAINS for item in train_final_edges(x)] + final_dc_edges())

DIEGO_R1_EDGES = dedupe_edges(top_diego_edges() + [item for x in TRAINS for item in train_diego_edges(x)] + diego_dc_edges())

DIEGO_R1_UNCERTAIN = [
    edge(f"SSPS-{x}", "PANEL-SSPS", "dashed SSPS-labeled trunk enters lower SSPS bundle but individual landing is crowded", "uncertain_included")
    for x in TRAINS
] + [
    edge("PANEL-SSPS", "PANEL-RPS-A", "plausible dashed RPS interlock bundle; endpoint not clean", "uncertain_included"),
    edge("PANEL-SSPS", "PANEL-RPS-B", "plausible dashed RPS interlock bundle; endpoint not clean", "uncertain_included"),
    edge("RECT-125-A", "BUS-DC-125A", "Diego direct rectifier-to-bus simplification before precision review", "uncertain_included"),
    edge("RECT-125-B", "BUS-DC-125B", "Diego direct rectifier-to-bus simplification before precision review", "uncertain_included"),
    edge("RECT-125-C", "BUS-DC-125B", "Diego direct rectifier-to-bus simplification before precision review", "uncertain_included"),
    edge("RECT-125-D", "BUS-DC-125B", "Diego direct rectifier-to-bus simplification before precision review", "uncertain_included"),
    edge("GND-A", "BUS-DC-125A", "ground-to-DC-bus crossing plausible before dot review", "uncertain_included"),
    edge("GND-B", "BUS-DC-125B", "ground-to-DC-bus crossing plausible before dot review", "uncertain_included"),
    edge("GND-C", "BUS-DC-125B", "ground-to-DC-bus crossing plausible before dot review", "uncertain_included"),
    edge("GND-D", "BUS-DC-125B", "ground-to-DC-bus crossing plausible before dot review", "uncertain_included"),
]

FINAL_UNCERTAIN = [
    edge("BUS-480-A1", "TIE-A12", "TIE-A12 is a conductor/tie label, replaced by direct BUS-480-A1--BUS-480-A2", "uncertain_excluded"),
    edge("BUS-480-B1", "TIE-B12", "TIE-B12 is a conductor/tie label, replaced by direct BUS-480-B1--BUS-480-B2", "uncertain_excluded"),
    edge("BUS-480-C1", "TIE-C12", "TIE-C12 is a conductor/tie label, replaced by direct BUS-480-C1--BUS-480-C2", "uncertain_excluded"),
    edge("BUS-480-D1", "TIE-D12", "TIE-D12 is a conductor/tie label, replaced by direct BUS-480-D1--BUS-480-D2", "uncertain_excluded"),
    edge("RECT-125-A", "BUS-DC-125A", "precision path is RECT-125-A--PANEL-IC-A--BUS-DC-125A", "uncertain_excluded"),
    edge("RECT-125-B", "BUS-DC-125B", "precision path is RECT-125-B--PANEL-IC-B--BUS-DC-125B", "uncertain_excluded"),
    edge("RECT-125-C", "BUS-DC-125B", "precision path is RECT-125-C--PANEL-IC-C--BUS-DC-125B", "uncertain_excluded"),
    edge("RECT-125-D", "BUS-DC-125B", "precision path is RECT-125-D--PANEL-IC-D--BUS-DC-125B", "uncertain_excluded"),
    edge("PANEL-SSPS", "RELAY-27A", "dashed SSPS/interlock bundle is visible but endpoint-specific landing is ambiguous", "uncertain_excluded"),
    edge("PANEL-SSPS", "RELAY-27B", "dashed SSPS/interlock bundle is visible but endpoint-specific landing is ambiguous", "uncertain_excluded"),
    edge("PANEL-SSPS", "RELAY-27C", "dashed SSPS/interlock bundle is visible but endpoint-specific landing is ambiguous", "uncertain_excluded"),
    edge("PANEL-SSPS", "RELAY-27D", "dashed SSPS/interlock bundle is visible but endpoint-specific landing is ambiguous", "uncertain_excluded"),
    edge("PANEL-SSPS", "PANEL-RPS-A", "dashed RPS/SSPS interlock path is not endpoint-clean", "uncertain_excluded"),
    edge("PANEL-SSPS", "PANEL-RPS-B", "dashed RPS/SSPS interlock path is not endpoint-clean", "uncertain_excluded"),
    edge("PANEL-SSPS", "ATS-480-A", "no clean direct endpoint from SSPS to ATS-480-A", "uncertain_excluded"),
    edge("PANEL-SSPS", "ATS-480-B", "no clean direct endpoint from SSPS to ATS-480-B", "uncertain_excluded"),
    edge("GND-A", "BUS-DC-125A", "ground terminal is tied to PANEL-IC-A, not directly to the DC bus", "uncertain_excluded"),
    edge("GND-B", "BUS-DC-125B", "ground terminal is tied to PANEL-IC-B, not directly to the DC bus", "uncertain_excluded"),
    edge("GND-C", "BUS-DC-125B", "ground terminal is tied to PANEL-IC-C, not directly to the DC bus", "uncertain_excluded"),
    edge("GND-D", "BUS-DC-125B", "ground terminal is tied to PANEL-IC-D, not directly to the DC bus", "uncertain_excluded"),
]

ROUNDS = [
    RoundSpec(
        "round_01",
        "diego",
        "high_recall_extractor",
        DIEGO_R1_NODES,
        DIEGO_R1_EDGES,
        DIEGO_R1_UNCERTAIN,
        True,
        [
            "High-recall extraction from raw PNG and crops generated only from that PNG.",
            "Included conductor/helper labels such as FDR, TIE, DC, SSPS, and ATS line labels as plausible nodes.",
            "Included plausible SSPS, direct rectifier-to-bus, and ground-to-bus candidates for precision review.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_01",
        "jennifer",
        "precision_reviewer_refiner",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Removed helper/conductor/location labels and retained only component/symbol/bus nodes.",
            "Replaced TIE labels with direct 480 V bus-to-bus edges and FDR labels with bus-to-breaker edges.",
            "Kept GND nodes connected only to PANEL-IC nodes; left SSPS dashed bundles uncertain and excluded.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_02",
        "diego",
        "high_recall_extractor_consensus",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Diego accepted Jennifer's precision removals and final edge set.",
            "Confirmed ATS endpoints to MCC-A1/B1/C1/D1 and A/B/C/D DC bus assignments.",
            "Confirmed direct RECT-to-BUS-DC, SSPS inferred edges, and crossing-only edges remain excluded.",
        ],
    ),
    RoundSpec(
        "round_02",
        "jennifer",
        "precision_reviewer_final",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Final precision lock after Diego agreed with the refined matrix.",
            "Final graph keeps PANEL-SSPS as a visible but isolated node because dashed endpoint-specific landings are ambiguous.",
            "Only raw PNG evidence and crops generated from that raw PNG were used.",
        ],
    ),
]


def matrix_edges(spec: RoundSpec) -> list[Edge]:
    edges = list(spec.edges)
    if spec.include_uncertain_in_matrix:
        node_set = set(spec.nodes)
        edges.extend([item for item in spec.uncertain_edges if item.source in node_set and item.target in node_set])
    return dedupe_edges(edges)


def validate_spec(spec: RoundSpec) -> dict[str, int | str]:
    nodes = spec.nodes
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{spec.round_id} {spec.actor} duplicate nodes: {duplicates}")
    node_set = set(nodes)
    edges = matrix_edges(spec)
    missing = sorted({endpoint for item in edges for endpoint in (item.source, item.target) if endpoint not in node_set})
    if missing:
        raise ValueError(f"{spec.round_id} {spec.actor} missing edge endpoints: {missing}")
    if any(item.source == item.target for item in edges):
        raise ValueError(f"{spec.round_id} {spec.actor} contains self-loop")
    if len(edges) != len({edge_key(item.source, item.target) for item in edges}):
        raise ValueError(f"{spec.round_id} {spec.actor} contains duplicate undirected edges")
    return {
        "round": spec.round_id,
        "actor": spec.actor,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "uncertain_item_count": len(spec.uncertain_edges),
        "symmetric": "yes",
        "diagonal_zero": "yes",
    }


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    adjacency = {edge_key(item.source, item.target) for item in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *nodes])
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(edge_key(row_node, col_node) in adjacency))
            writer.writerow(row)


def write_node_map(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "component"])
        for index, node in enumerate(nodes, start=1):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "status", "evidence"])
        for item in edges:
            writer.writerow([item.source, item.target, item.status, item.evidence])


def write_notes(path: Path, spec: RoundSpec, metrics: dict[str, int | str]) -> None:
    lines = [
        f"# {spec.round_id} {spec.actor.title()}",
        "",
        f"Role: {spec.role}",
        "",
        "Evidence source: raw schematic PNG and crops generated only from that PNG.",
        "",
        f"Node count: {metrics['node_count']}",
        f"Matrix edge count: {metrics['edge_count']}",
        f"Uncertain item count: {metrics['uncertain_item_count']}",
        "",
        "Notes:",
    ]
    lines.extend([f"- {note}" for note in spec.notes])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def copy_final_artifacts(final_prefix: str) -> None:
    copies = [
        (f"{final_prefix}_connectivity_matrix.csv", "final_connectivity_matrix.csv"),
        (f"{final_prefix}_edges.csv", "final_edges.csv"),
        (f"{final_prefix}_node_map.csv", "final_node_map.csv"),
        (f"{final_prefix}_uncertain_edges.csv", "final_uncertain_edges.csv"),
        (f"{final_prefix}_notes.md", "final_notes.md"),
        (f"{final_prefix}_connectivity_matrix.csv", "connectivity_matrix_final.csv"),
        (f"{final_prefix}_edges.csv", "edge_candidates_jennifer_round4_final.csv"),
    ]
    for source_name, target_name in copies:
        shutil.copyfile(RESULTS / source_name, RESULTS / target_name)


def write_tracking(metrics_rows: list[dict[str, int | str]], prefixes: list[str]) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    agent_ids = {
        "diego": "019f5f85-5419-7683-b5ff-6c06fdeb8e90",
        "jennifer": "019f5f8a-693b-7770-96eb-700f992f3990",
    }
    with (RESULTS / "token_performance_tracking.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "timestamp_local",
            "round_id",
            "actor",
            "role",
            "node_count",
            "edge_count",
            "uncertain_item_count",
            "subagent_runtime_id",
            "token_telemetry",
            "artifact_prefix",
        ])
        for spec, metrics, prefix in zip(ROUNDS, metrics_rows, prefixes):
            writer.writerow([
                now,
                spec.round_id,
                spec.actor,
                spec.role,
                metrics["node_count"],
                metrics["edge_count"],
                metrics["uncertain_item_count"],
                agent_ids["diego" if spec.actor == "diego" else "jennifer"],
                "not available from current runtime telemetry",
                prefix,
            ])

    notes = [
        "# Token Performance Notes",
        "",
        "- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and marks token telemetry unavailable.",
        "- Two deployed subagents were used: Diego for high-recall extraction and Jennifer for precision review/refinement.",
        "- The process saturated after Diego round 2 accepted Jennifer's refined matrix and Jennifer final-confirmed it.",
        "- There was no Input resources folder; only the raw schematic PNG and crops generated from it were used. No GT or GT-derived resources were used.",
        "",
    ]
    (RESULTS / "token_performance_notes.md").write_text("\n".join(notes), encoding="utf-8")


def write_validation(metrics_rows: list[dict[str, int | str]]) -> None:
    with (RESULTS / "connectivity_matrix_validation_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["round", "actor", "node_count", "edge_count", "uncertain_item_count", "symmetric", "diagonal_zero"],
        )
        writer.writeheader()
        writer.writerows(metrics_rows)
    final = metrics_rows[-1]
    summary = [
        "Connectivity matrix validation summary",
        "",
        f"Final round: {final['round']} {final['actor']}",
        f"Final node count: {final['node_count']}",
        f"Final edge count: {final['edge_count']}",
        f"Symmetric: {final['symmetric']}",
        f"Diagonal zero: {final['diagonal_zero']}",
        "Duplicate nodes: none",
        "Missing edge endpoints: none",
        "Self-loops: none",
        "",
    ]
    (RESULTS / "connectivity_matrix_validation_summary.txt").write_text("\n".join(summary), encoding="utf-8")


def write_extraction_notes() -> None:
    lines = [
        "# Extraction Notes",
        "",
        "Case: 11 Raw",
        "",
        "Evidence used:",
        "- Raw schematic PNG in the Raw folder.",
        "- Crops generated from that same PNG and stored under results/crops.",
        "- No Input resources folder was present; no Ground Truth or GT-derived feedback/resources were used.",
        "",
        "Final consensus:",
        "- Diego and Jennifer agreed after two rounds.",
        f"- Final node count is {len(FINAL_NODES)} visible component/node labels.",
        f"- Final confirmed edge count is {len(FINAL_EDGES)}.",
        "- Conductor/helper labels such as FDR, TIE, DC-X125, SSPS-X, ATS-X1, and section labels were excluded as graph nodes.",
        "- PANEL-SSPS remains a visible node with no confirmed matrix edges because endpoint-specific dashed interlocks are ambiguous.",
        "- GND-A/B/C/D are connected only to their PANEL-IC-A/B/C/D terminals.",
        "",
    ]
    (RESULTS / "extraction_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    metrics_rows: list[dict[str, int | str]] = []
    prefixes: list[str] = []
    for spec in ROUNDS:
        prefix = f"{spec.round_id}_{spec.actor}"
        prefixes.append(prefix)
        metrics = validate_spec(spec)
        metrics_rows.append(metrics)
        edges = matrix_edges(spec)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", spec.nodes, edges)
        write_node_map(RESULTS / f"{prefix}_node_map.csv", spec.nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_edges(RESULTS / f"{prefix}_uncertain_edges.csv", spec.uncertain_edges)
        write_notes(RESULTS / f"{prefix}_notes.md", spec, metrics)

    copy_final_artifacts("round_02_jennifer")
    write_tracking(metrics_rows, prefixes)
    write_validation(metrics_rows)
    write_extraction_notes()


if __name__ == "__main__":
    main()
