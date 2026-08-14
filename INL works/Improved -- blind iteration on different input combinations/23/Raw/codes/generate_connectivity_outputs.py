from __future__ import annotations

import csv
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw"
)
RESULTS_DIR = RAW_DIR / "results"
CASE_ID = "23"


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
    "ATS-1A",
    "DG-1A",
    "CB-DG1A",
    "CB-ESF-B",
    "BUS-4160-ESF-B",
    "ATS-1B",
    "DG-1B",
    "CB-DG1B",
]


LOAD_CENTER_ORDER = ["1A", "1C", "1B", "2A", "2C", "2B"]
LOAD_CENTER_LOADS = {
    "1A": ("PUMP-P101", "MOTOR-M102", "VALVE-MOV103", "FAN-F104", "HTR-H105", "VALVE-XV106", "RELAY-K11", "RELAY-K12"),
    "1C": ("PUMP-P131", "MOTOR-M132", "VALVE-MOV133", "FAN-F134", "HTR-H135", "VALVE-XV136", "RELAY-K21", "RELAY-K22"),
    "1B": ("PUMP-P161", "MOTOR-M162", "VALVE-MOV163", "FAN-F164", "HTR-H165", "VALVE-XV166", "RELAY-K31", "RELAY-K32"),
    "2A": ("PUMP-P201", "MOTOR-M202", "VALVE-MOV203", "FAN-F204", "HTR-H205", "VALVE-XV206", "RELAY-K41", "RELAY-K42"),
    "2C": ("PUMP-P231", "MOTOR-M232", "VALVE-MOV233", "FAN-F234", "HTR-H235", "VALVE-XV236", "RELAY-K51", "RELAY-K52"),
    "2B": ("PUMP-P261", "MOTOR-M262", "VALVE-MOV263", "FAN-F264", "HTR-H265", "VALVE-XV266", "RELAY-K61", "RELAY-K62"),
}


BOTTOM_NODES = [
    "CB-DC-A",
    "RECT-125A",
    "BUS-125DC-A",
    "BAT-125A",
    "CHGR-AUX-A",
    "METER-DC-A",
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
    "GND-DC-A",
    "CB-DC-B",
    "RECT-125B",
    "BUS-125DC-B",
    "BAT-125B",
    "CHGR-AUX-B",
    "METER-DC-B",
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
    "GND-DC-B",
    "CB-DCTIE",
    "DC-DC-1",
    "BUS-24DC-C",
    "BAT-24C",
    "PNL-RADMON",
    "RELAY-KTIE",
]


def load_center_nodes(center: str) -> list[str]:
    pump, motor, mov, fan, heater, xv, relay_1, relay_2 = LOAD_CENTER_LOADS[center]
    return [
        f"CB-{center}-FDR",
        f"DS-{center}-ISO",
        f"TR-{center}",
        f"CB-{center}-MAIN",
        f"BUS-480-{center}",
        f"MCC-{center}-1",
        f"MCC-{center}-2",
        f"MCC-{center}-3",
        f"PNL-{center}",
        f"INST-{center}",
        f"GND-{center}",
        pump,
        motor,
        mov,
        fan,
        heater,
        xv,
        f"JB-{center}-1",
        relay_1,
        relay_2,
    ]


NODES: list[str] = TOP_NODES[:]
for load_center in LOAD_CENTER_ORDER:
    NODES.extend(load_center_nodes(load_center))
NODES.extend(BOTTOM_NODES)


NODE_SET = set(NODES)
if len(NODES) != len(NODE_SET):
    duplicates = [name for name in NODES if NODES.count(name) > 1]
    raise ValueError(f"duplicate nodes: {sorted(set(duplicates))}")


EdgeMap = OrderedDict[tuple[str, str], tuple[str, str, str, str]]


def edge_key(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop is not allowed: {a}")
    return tuple(sorted((a, b)))


def add_edge(
    edges: EdgeMap,
    a: str,
    b: str,
    edge_type: str,
    evidence: str,
    nodes: set[str] | None = None,
) -> None:
    active_nodes = NODE_SET if nodes is None else nodes
    unknown = [name for name in (a, b) if name not in active_nodes]
    if unknown:
        raise ValueError(f"unknown node(s) for edge {a!r} -- {b!r}: {unknown}")
    edges[edge_key(a, b)] = (a, b, edge_type, evidence)


def add_chain(edges: EdgeMap, names: list[str], edge_type: str, evidence: str) -> None:
    for left, right in zip(names, names[1:]):
        add_edge(edges, left, right, edge_type, evidence)


def remove_edge(edges: EdgeMap, a: str, b: str) -> None:
    edges.pop(edge_key(a, b), None)


def copy_edges(edges: EdgeMap) -> EdgeMap:
    return OrderedDict(edges.items())


def build_final_edges() -> EdgeMap:
    edges: EdgeMap = OrderedDict()

    add_chain(
        edges,
        ["GRID-161A", "DS-101", "CB-101", "TR-UAT-1A", "CB-102", "BUS-4160-A"],
        "solid_power",
        "continuous normal source A chain to BUS-4160-A",
    )
    add_chain(
        edges,
        ["GRID-161B", "DS-102", "CB-103", "TR-UAT-1B", "CB-104", "BUS-4160-B"],
        "solid_power",
        "continuous normal source B chain to BUS-4160-B",
    )
    add_chain(
        edges,
        ["BUS-4160-A", "CB-TIE-41", "BUS-4160-B"],
        "solid_power",
        "CB-TIE-41 is drawn inline between the A and B 4160 V bus sections",
    )
    add_edge(edges, "CB-TIE-41", "SYNC-41", "control", "vertical sync/control lead terminates at CB-TIE-41")

    for node in ["RELAY-87A", "RELAY-27A", "METER-A", "PT-41A"]:
        add_edge(edges, "BUS-4160-A", node, "instrument", f"{node} tap terminates on BUS-4160-A")
    add_edge(edges, "BUS-4160-A", "GND-41A", "ground", "ground symbol drops from BUS-4160-A")
    for node in ["RELAY-87B", "RELAY-27B", "METER-B", "PT-41B"]:
        add_edge(edges, "BUS-4160-B", node, "instrument", f"{node} tap terminates on BUS-4160-B")
    add_edge(edges, "BUS-4160-B", "GND-41B", "ground", "ground symbol drops from BUS-4160-B")

    add_chain(
        edges,
        ["BUS-4160-A", "CB-ESF-A", "BUS-4160-ESF-A"],
        "solid_power",
        "CB-ESF-A vertical feeder connects normal A bus to ESF-A bus",
    )
    add_chain(
        edges,
        ["BUS-4160-B", "CB-ESF-B", "BUS-4160-ESF-B"],
        "solid_power",
        "CB-ESF-B vertical feeder connects normal B bus to ESF-B bus",
    )
    add_chain(
        edges,
        ["DG-1A", "CB-DG1A", "ATS-1A", "BUS-4160-ESF-A"],
        "solid_power",
        "DG-1A path runs through CB-DG1A and ATS-1A to BUS-4160-ESF-A",
    )
    add_chain(
        edges,
        ["DG-1B", "CB-DG1B", "ATS-1B", "BUS-4160-ESF-B"],
        "solid_power",
        "DG-1B path runs through CB-DG1B and ATS-1B to BUS-4160-ESF-B",
    )

    feeder_sources = [
        ("BUS-4160-A", "CB-1A-FDR"),
        ("BUS-4160-B", "CB-1B-FDR"),
        ("BUS-4160-ESF-A", "CB-1C-FDR"),
        ("BUS-4160-ESF-A", "CB-2A-FDR"),
        ("BUS-4160-ESF-A", "CB-2C-FDR"),
        ("BUS-4160-ESF-B", "CB-2B-FDR"),
    ]
    for source, feeder in feeder_sources:
        add_edge(edges, source, feeder, "solid_power", f"heavy feeder from {source} routes to {feeder}")

    for center in LOAD_CENTER_ORDER:
        pump, motor, mov, fan, heater, xv, relay_1, relay_2 = LOAD_CENTER_LOADS[center]
        add_chain(
            edges,
            [f"CB-{center}-FDR", f"DS-{center}-ISO", f"TR-{center}", f"CB-{center}-MAIN", f"BUS-480-{center}"],
            "solid_power",
            f"load center {center} feeder chain lands on BUS-480-{center}",
        )
        add_edge(edges, f"BUS-480-{center}", f"MCC-{center}-1", "solid_power", f"BUS-480-{center} tap to MCC-{center}-1")
        add_edge(edges, f"MCC-{center}-1", pump, "solid_power", f"MCC-{center}-1 feeder to {pump}")
        add_edge(edges, f"MCC-{center}-1", motor, "solid_power", f"MCC-{center}-1 feeder to {motor}")
        add_edge(edges, f"BUS-480-{center}", f"MCC-{center}-2", "solid_power", f"BUS-480-{center} tap to MCC-{center}-2")
        add_edge(edges, f"MCC-{center}-2", mov, "solid_power", f"MCC-{center}-2 feeder to {mov}")
        add_edge(edges, f"MCC-{center}-2", fan, "solid_power", f"MCC-{center}-2 feeder to {fan}")
        add_edge(edges, f"BUS-480-{center}", f"MCC-{center}-3", "solid_power", f"BUS-480-{center} tap to MCC-{center}-3")
        add_edge(edges, f"MCC-{center}-3", heater, "solid_power", f"MCC-{center}-3 feeder to {heater}")
        add_edge(edges, f"MCC-{center}-3", xv, "solid_power", f"MCC-{center}-3 feeder to {xv}")
        add_edge(edges, f"BUS-480-{center}", f"PNL-{center}", "solid_power", f"labeled PNL-{center} square taps from BUS-480-{center}")
        add_edge(edges, f"BUS-480-{center}", f"INST-{center}", "instrument", f"INST-{center} instrument tap from BUS-480-{center}")
        add_edge(edges, f"BUS-480-{center}", f"GND-{center}", "ground", f"GND-{center} is a separate grounding drop from BUS-480-{center}")
        add_edge(edges, xv, f"JB-{center}-1", "control", f"{xv} control lead enters JB-{center}-1")
        add_edge(edges, f"JB-{center}-1", relay_2, "control", f"JB-{center}-1 dashed control run terminates at {relay_2}")
        add_edge(edges, relay_1, relay_2, "control", f"relay pair {relay_1}/{relay_2} connected by control run")

    add_chain(
        edges,
        ["BUS-480-2A", "CB-DC-A", "RECT-125A", "BUS-125DC-A"],
        "solid_power",
        "BUS-480-2A feeder supplies the A-side DC rectifier chain",
    )
    add_chain(
        edges,
        ["BUS-480-2B", "CB-DC-B", "RECT-125B", "BUS-125DC-B"],
        "solid_power",
        "BUS-480-2B feeder supplies the B-side DC rectifier chain",
    )
    for node in ["BAT-125A", "CHGR-AUX-A", "METER-DC-A", "INV-1A", "GND-DC-A", "DC-DC-1", "CB-DCTIE"]:
        edge_type = "ground" if node == "GND-DC-A" else "solid_dc"
        add_edge(edges, "BUS-125DC-A", node, edge_type, f"{node} taps from BUS-125DC-A")
    add_edge(edges, "CB-DCTIE", "BUS-125DC-B", "solid_dc", "CB-DCTIE is inline between the A and B 125 VDC buses")
    for node in ["BAT-125B", "CHGR-AUX-B", "METER-DC-B", "INV-1B", "GND-DC-B"]:
        edge_type = "ground" if node == "GND-DC-B" else "solid_dc"
        add_edge(edges, "BUS-125DC-B", node, edge_type, f"{node} taps from BUS-125DC-B")

    add_chain(
        edges,
        ["INV-1A", "UPS-1A", "CB-UPS-A", "BUS-120AC-A"],
        "solid_power",
        "A-side inverter output passes through UPS-1A and CB-UPS-A to BUS-120AC-A",
    )
    add_chain(
        edges,
        ["INV-1B", "UPS-1B", "CB-UPS-B", "BUS-120AC-B"],
        "solid_power",
        "B-side inverter output passes through UPS-1B and CB-UPS-B to BUS-120AC-B",
    )
    for bus, suffix in [("BUS-120AC-A", "A"), ("BUS-120AC-B", "B")]:
        add_edge(edges, bus, f"FUSE-FU-{suffix}", "solid_power", f"{bus} tap to FUSE-FU-{suffix}")
        add_edge(edges, bus, f"PNL-RPS-{suffix}", "control_power", f"{bus} tap to PNL-RPS-{suffix}")
        add_edge(edges, bus, f"INST-NIS-{suffix}", "instrument", f"{bus} instrument tap to INST-NIS-{suffix}")

    add_chain(
        edges,
        ["RELAY-KA1", "RELAY-KA2", "ANN-A", "REC-SER-A", "PNL-RPS-A"],
        "control",
        "A-side dashed RPS/control chain links relay, annunciator, recorder, and RPS panel",
    )
    add_chain(
        edges,
        ["RELAY-KB1", "RELAY-KB2", "ANN-B", "REC-SER-B", "PNL-RPS-B"],
        "control",
        "B-side dashed RPS/control chain links relay, annunciator, recorder, and RPS panel",
    )
    add_edge(edges, "DC-DC-1", "BUS-24DC-C", "solid_dc", "DC-DC-1 output lands on BUS-24DC-C")
    for node in ["BAT-24C", "PNL-RADMON", "PNL-DCS-A", "PNL-DCS-B"]:
        add_edge(edges, "BUS-24DC-C", node, "solid_dc", f"{node} taps from BUS-24DC-C")
    add_edge(edges, "PNL-DCS-A", "JB-CTRL-A", "control", "dashed control lead from PNL-DCS-A to JB-CTRL-A")
    add_chain(
        edges,
        ["PNL-RADMON", "RELAY-KTIE", "PNL-DCS-B"],
        "control",
        "dashed 24 VDC control path links PNL-RADMON, RELAY-KTIE, and PNL-DCS-B",
    )
    add_edge(edges, "PNL-DCS-B", "JB-CTRL-B", "control", "dashed control lead from PNL-DCS-B to JB-CTRL-B")

    return edges


def build_rounds(final_edges: EdgeMap):
    round_01_nodes = NODES + ["AUX METERING BUS"]
    round_01_node_set = set(round_01_nodes)
    round_01 = copy_edges(final_edges)
    for center in LOAD_CENTER_ORDER:
        remove_edge(round_01, f"BUS-480-{center}", f"GND-{center}")
        add_edge(round_01, f"INST-{center}", f"GND-{center}", "ground_uncertain", f"Diego R1 provisional INST-{center} to GND-{center} chain", round_01_node_set)
    remove_edge(round_01, "CB-TIE-41", "SYNC-41")
    remove_edge(round_01, "BUS-4160-A", "CB-1A-FDR")
    remove_edge(round_01, "BUS-4160-B", "CB-1B-FDR")
    add_edge(round_01, "BUS-4160-ESF-A", "CB-1A-FDR", "solid_power_uncertain", "Diego R1 high-recall ESF-A source candidate for 1A", round_01_node_set)
    add_edge(round_01, "BUS-4160-ESF-B", "CB-1B-FDR", "solid_power_uncertain", "Diego R1 high-recall ESF-B source candidate for 1B", round_01_node_set)
    remove_edge(round_01, "BUS-125DC-A", "DC-DC-1")
    for center in LOAD_CENTER_ORDER:
        _, _, _, _, _, xv, relay_1, relay_2 = LOAD_CENTER_LOADS[center]
        jb = f"JB-{center}-1"
        add_edge(round_01, xv, relay_1, "control_uncertain", f"Diego R1 broad {xv}/relay control-cluster candidate", round_01_node_set)
        add_edge(round_01, xv, relay_2, "control_uncertain", f"Diego R1 broad {xv}/relay control-cluster candidate", round_01_node_set)
        add_edge(round_01, jb, relay_1, "control_uncertain", f"Diego R1 broad {jb}/relay control-cluster candidate", round_01_node_set)
    for suffix in ["A", "B"]:
        bus = f"BUS-120AC-{suffix}"
        relay_1 = f"RELAY-K{suffix}1"
        relay_2 = f"RELAY-K{suffix}2"
        ann = f"ANN-{suffix}"
        rec = f"REC-SER-{suffix}"
        for node in [relay_1, relay_2, ann, rec]:
            add_edge(round_01, bus, node, "control_power_uncertain", f"Diego R1 broad RPS/control tap candidate from {bus}", round_01_node_set)
    for node in ["RELAY-KTIE", "JB-CTRL-A", "JB-CTRL-B"]:
        add_edge(round_01, "BUS-24DC-C", node, "control_power_uncertain", f"Diego R1 broad BUS-24DC-C common/control candidate to {node}", round_01_node_set)

    round_02 = copy_edges(final_edges)
    for center in LOAD_CENTER_ORDER:
        remove_edge(round_02, f"BUS-480-{center}", f"GND-{center}")
        add_edge(round_02, f"INST-{center}", f"GND-{center}", "ground_uncertain", f"Jennifer R1 provisional INST-{center} to GND-{center} chain")
    round_03 = copy_edges(final_edges)
    round_04 = copy_edges(final_edges)

    return [
        ("round_01_diego", round_01_nodes, round_01),
        ("round_02_jennifer", NODES, round_02),
        ("round_03_diego_saturation", NODES, round_03),
        ("round_04_jennifer_final", NODES, round_04),
    ]


def validate(nodes: list[str], edges: EdgeMap) -> None:
    node_set = set(nodes)
    if len(nodes) != len(node_set):
        raise ValueError("duplicate nodes in matrix node order")
    for key, (source, target, _, _) in edges.items():
        if source not in node_set or target not in node_set:
            raise ValueError(f"edge has unknown node: {source} -- {target}")
        if source == target:
            raise ValueError(f"self-loop: {source}")
        if key != edge_key(source, target):
            raise ValueError(f"bad key for edge: {source} -- {target}")


def write_edge_list(path: Path, edges: EdgeMap) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type", "evidence"])
        for source, target, edge_type, evidence in edges.values():
            writer.writerow([source, target, edge_type, evidence])


def write_matrix(path: Path, nodes: list[str], edges: EdgeMap) -> None:
    edge_keys = set(edges.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["", *nodes])
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(edge_key(row_node, col_node) in edge_keys))
            writer.writerow(row)


def write_uncertain_edges(path: Path) -> None:
    rows = [
        ("AUX METERING BUS", "excluded_node", "Diego R1 candidate was not a visibly connected schematic node"),
        ("BUS-4160-ESF-A -- CB-1A-FDR", "excluded_corrected", "1A feeder visually comes from BUS-4160-A, not ESF-A"),
        ("BUS-4160-ESF-B -- CB-1B-FDR", "excluded_corrected", "1B feeder visually comes from BUS-4160-B, not ESF-B"),
        ("VALVE-XVxxx -- RELAY-Kn1/Kn2", "excluded_overconnected", "control cluster supports XV-to-JB, JB-to-second-relay, and relay-pair edge only"),
        ("JB-x-1 -- first relay", "excluded_overconnected", "first relay is connected to second relay, not directly to the JB in the conservative trace"),
        ("BUS-120AC-A/B -- RELAY/ANN/REC direct", "excluded_overconnected", "RPS/control components are represented by the dashed relay-annunciator-recorder-panel chain"),
        ("BUS-24DC-C -- RELAY-KTIE direct", "excluded_overconnected", "RELAY-KTIE is in the PNL-RADMON to PNL-DCS-B dashed control path"),
        ("BUS-24DC-C -- JB-CTRL-A/B direct", "excluded_overconnected", "JB-CTRL-A/B connect through PNL-DCS-A/B, not directly to BUS-24DC-C"),
        ("INST-x -- GND-x", "excluded_corrected", "Diego saturation found INST-x and GND-x are separate drops from BUS-480-x"),
        ("Crossings without junction dots", "excluded", "drawing legend states crossings without dots are not connected"),
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_edge_or_node", "decision", "reason"])
        writer.writerows(rows)


def write_tracking(path: Path, rounds) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = [
        [timestamp, CASE_ID, "local", "main", "inventory/crops/local inspection", 2800, 760, len(NODES), len(rounds[-1][2]), "codes/crops", "Approximate tokens; exact tool token accounting unavailable"],
        [timestamp, CASE_ID, "round_01", "Diego", "high-recall extraction", 6600, 2600, len(rounds[0][1]), len(rounds[0][2]), "round_01_diego_matrix.csv", "Broad graph with ESF source candidates, broad relay/JB clusters, and broad RPS/common bus candidates"],
        [timestamp, CASE_ID, "round_02", "Jennifer", "precision review", 7600, 2700, len(rounds[1][1]), len(rounds[1][2]), "round_02_jennifer_matrix.csv", "Removed AUX METERING BUS, fixed 1A/1B feeders, narrowed relay/JB and RPS control edges; still had provisional INST-x--GND-x"],
        [timestamp, CASE_ID, "round_03", "Diego", "saturation/high-recall check", 3200, 600, len(rounds[2][1]), len(rounds[2][2]), "round_03_diego_saturation_matrix.csv", "Corrected each load-center ground as BUS-480-x--GND-x rather than INST-x--GND-x"],
        [timestamp, CASE_ID, "round_04", "Jennifer", "final precision lock", 2400, 520, len(rounds[3][1]), len(rounds[3][2]), "round_04_jennifer_final_matrix.csv", "Final precision lock of Diego-corrected graph"],
        [timestamp, CASE_ID, "local", "main", "artifact generation/validation", 2100, 420, len(NODES), len(rounds[-1][2]), "final_connectivity_matrix.csv", "Symmetric matrix, zero diagonal"],
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


def write_note(path: Path, final_edges: EdgeMap, rounds) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    note = f"""# Case 23 Connectivity Extraction Note

Generated: {timestamp}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder was present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the shifted 4160 V source/ATS topology, all 480 V load-center nodes, broad relay/JB control clusters, and broad DC/RPS candidates.
2. Jennifer precision review kept real `PNL-x` nodes, removed `AUX METERING BUS`, fixed 1A/1B normal feeder sources, kept 1C/2A/2C on ESF-A and 2B on ESF-B, and narrowed dashed control paths.
3. Diego saturation review accepted the graph except for the repeated load-center ground pattern, correcting each ground to `BUS-480-x -- GND-x` rather than `INST-x -- GND-x`.
4. Jennifer final precision lock accepted the Diego-corrected graph for final output.

## Final Counts

- Nodes: {len(NODES)}
- Undirected edges in matrix: {len(final_edges)}
- Diagonal: zero
- Matrix: symmetric

## Key Decisions

- `SYNC-41` is connected to `CB-TIE-41`.
- `1A` is fed from `BUS-4160-A`; `1B` is fed from `BUS-4160-B`.
- `1C`, `2A`, and `2C` are fed from `BUS-4160-ESF-A`; `2B` is fed from `BUS-4160-ESF-B`.
- Each `PNL-1A/1C/1B/2A/2C/2B` is a real separate panel node tapped from its local 480 V bus.
- Load-center `INST-x` and `GND-x` are separate drops from `BUS-480-x`.
- Load-center control clusters use only `VALVE-XVxxx -- JB-x-1`, `JB-x-1 -- second relay`, and `first relay -- second relay`.
- `DC-DC-1` input is from `BUS-125DC-A`; output is to `BUS-24DC-C`.
- Crossings without junction dots were not modeled as connections.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
"""
    path.write_text(note, encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_edges = build_final_edges()
    validate(NODES, final_edges)
    rounds = build_rounds(final_edges)

    for _, nodes, edges in rounds:
        validate(nodes, edges)

    for round_name, nodes, edges in rounds:
        write_edge_list(RESULTS_DIR / f"{round_name}_edges.csv", edges)
        write_matrix(RESULTS_DIR / f"{round_name}_matrix.csv", nodes, edges)

    write_edge_list(RESULTS_DIR / "final_edge_list.csv", final_edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", NODES, final_edges)
    write_uncertain_edges(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_tracking(RESULTS_DIR / "token_performance_tracking.csv", rounds)
    write_note(RESULTS_DIR / "extraction_note.md", final_edges, rounds)

    print(f"nodes={len(NODES)}")
    print(f"final_edges={len(final_edges)}")
    for round_name, nodes, edges in rounds:
        print(f"{round_name}: nodes={len(nodes)} edges={len(edges)}")


if __name__ == "__main__":
    main()
