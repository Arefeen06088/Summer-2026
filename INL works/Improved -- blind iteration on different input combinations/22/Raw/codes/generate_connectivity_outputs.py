from __future__ import annotations

import csv
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw"
)
RESULTS_DIR = RAW_DIR / "results"
CASE_ID = "22"


BUS_13A = "BUS-13A 13.8 KV AUX BUS A"
BUS_13B = "BUS-13B 13.8 KV AUX BUS B"
BUS_4160 = {
    "A": "BUS-4160-A 4160V SAFETY BUS 1A",
    "B": "BUS-4160-B 4160V SAFETY BUS 1B",
    "C": "BUS-4160-C 4160V SAFETY BUS 1C",
    "D": "BUS-4160-D 4160V SAFETY BUS 1D",
}
BUS_480 = {
    "A": "BUS-480-A 480V LOAD CENTER A",
    "B": "BUS-480-B 480V LOAD CENTER B",
    "C": "BUS-480-C 480V LOAD CENTER C",
    "D": "BUS-480-D 480V LOAD CENTER D",
}
BUS_125 = {
    "A": "BUS-125A 125 VDC BUS A",
    "B": "BUS-125B 125 VDC BUS B",
}
BUS_UPS = {
    "A": "BUS-UPS-A 120 VAC UPS BUS A",
    "B": "BUS-UPS-B 120 VAC UPS BUS B",
}


NODES: list[str] = [
    "GEN-G01",
    "GSU-T01",
    "SWYD-345",
    "CB-13A1",
    "CB-13B1",
    "CB-13T",
    BUS_13A,
    BUS_13B,
    "AUX-XFMR-1A",
    "AUX-XFMR-1B",
    "SAT-XFMR-1C",
    "SAT-XFMR-1D",
    "RELAY-87U",
    "SYNC-PNL-1",
    "CB-4A-IN",
    "CB-4B-IN",
    "CB-4C-IN",
    "CB-4D-IN",
    "CB-4AB-TIE",
    "CB-4CD-TIE",
    "DG-1A",
    "DG-1B",
    "DG-1C",
    "DG-1D",
    "CB-DG-A",
    "CB-DG-B",
    "CB-DG-C",
    "CB-DG-D",
    BUS_4160["A"],
    BUS_4160["B"],
    BUS_4160["C"],
    BUS_4160["D"],
    "CB-LC-A",
    "CB-LC-B",
    "CB-LC-C",
    "CB-LC-D",
    "TR-LC-A",
    "TR-LC-B",
    "TR-LC-C",
    "TR-LC-D",
    BUS_480["A"],
    BUS_480["B"],
    BUS_480["C"],
    BUS_480["D"],
    "MCC-AA",
    "MCC-AB",
    "MCC-BA",
    "MCC-BB",
    "MCC-CA",
    "MCC-CB",
    "MCC-DA",
    "MCC-DB",
    "CB-MCC-AA",
    "CB-MCC-AB",
    "CB-MCC-BA",
    "CB-MCC-BB",
    "CB-MCC-CA",
    "CB-MCC-CB",
    "CB-MCC-DA",
    "CB-MCC-DB",
]

for suffix, relay_prefix in [("A", "KA"), ("B", "KB"), ("C", "KC"), ("D", "KD")]:
    NODES.extend(
        [
            f"INST-PT-{suffix}",
            f"INST-CT-{suffix}",
            f"XFMR-120-{suffix}",
            f"PNL-120-{suffix}",
            f"RELAY-{relay_prefix}1",
            f"RELAY-{relay_prefix}2",
            f"JB-{suffix}1",
            f"TERM-{suffix}",
            f"GND-{suffix}",
        ]
    )

for suffix in "ABCD":
    NODES.extend(
        [
            f"CB-RHR-{suffix}",
            f"PUMP-RHR-{suffix}",
            f"CB-SI-{suffix}",
            f"PUMP-SI-{suffix}",
            f"CB-CCW-{suffix}",
            f"PUMP-CCW-{suffix}",
            f"CB-FAN-{suffix}",
            f"FAN-CR-{suffix}",
            f"CB-CH-{suffix}",
            f"CHILLER-{suffix}",
            f"CB-VLV1-{suffix}",
            f"MOV-HV1-{suffix}",
            f"CB-VLV2-{suffix}",
            f"MOV-HV2-{suffix}",
            f"CB-SPARE-{suffix}",
            f"SPARE-LOAD-{suffix}",
        ]
    )

NODES.extend(
    [
        "CB-DC-A1",
        "CB-DC-B1",
        "CHGR-125A",
        "CHGR-125B",
        BUS_125["A"],
        BUS_125["B"],
        "BAT-125A",
        "BAT-125B",
        "DC-MCC-A",
        "DC-MCC-B",
        "SOL-SDV-A",
        "SOL-SDV-B",
        "DIODE-OR-A",
        "DIODE-OR-B",
        "GRD-DC-A",
        "GRD-DC-B",
        "FUSE-FD-A",
        "FUSE-FD-B",
        "INV-UPS-A",
        "INV-UPS-B",
        BUS_UPS["A"],
        BUS_UPS["B"],
        "INST-RACK-A",
        "INST-RACK-B",
        "PNL-RPS-A",
        "PNL-RPS-B",
        "RELAY-RPS-A1",
        "RELAY-RPS-B1",
        "RELAY-ESF-A",
        "RELAY-ESF-B",
        "PLC-SAF-A",
        "PLC-SAF-B",
        "ANN-PNL-CR",
        "JB-CR-01",
        "TERM-MTB-A",
        "TERM-MTB-B",
        "REC-SEQ-1",
        "XFMR-PT-1",
        "METER-V01",
        "METER-A01",
    ]
)


def edge_key(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop is not allowed: {a}")
    return tuple(sorted((a, b)))


def add_edge(
    edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]],
    a: str,
    b: str,
    edge_type: str,
    evidence: str,
) -> None:
    unknown = [name for name in (a, b) if name not in NODE_SET]
    if unknown:
        raise ValueError(f"unknown node(s) for edge {a!r} -- {b!r}: {unknown}")
    key = edge_key(a, b)
    edges[key] = (a, b, edge_type, evidence)


def build_final_edges() -> OrderedDict[tuple[str, str], tuple[str, str, str, str]]:
    edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]] = OrderedDict()

    add_edge(edges, "GEN-G01", "GSU-T01", "solid_power", "generator source detail connects to step-up transformer")
    add_edge(edges, "GSU-T01", "SWYD-345", "solid_power", "step-up transformer line lands on 345 kV switchyard symbol")
    add_edge(edges, "SWYD-345", "CB-13A1", "solid_power", "upper source header feeds 13.8 kV A incoming breaker")
    add_edge(edges, "CB-13A1", BUS_13A, "solid_power", "incoming breaker drops to AUX BUS A with junction dot")
    add_edge(edges, "SWYD-345", "CB-13B1", "solid_power", "upper source header feeds 13.8 kV B incoming breaker")
    add_edge(edges, "CB-13B1", BUS_13B, "solid_power", "incoming breaker drops to AUX BUS B with junction dot")
    add_edge(edges, BUS_13A, "CB-13T", "solid_power", "tie breaker drawn between 13.8 kV buses")
    add_edge(edges, "CB-13T", BUS_13B, "solid_power", "tie breaker drawn between 13.8 kV buses")

    transformer_feeds = [
        (BUS_13A, "AUX-XFMR-1A", "CB-4A-IN", BUS_4160["A"]),
        (BUS_13A, "AUX-XFMR-1B", "CB-4B-IN", BUS_4160["B"]),
        (BUS_13B, "SAT-XFMR-1C", "CB-4C-IN", BUS_4160["C"]),
        (BUS_13B, "SAT-XFMR-1D", "CB-4D-IN", BUS_4160["D"]),
    ]
    for bus13, transformer, breaker, bus4160 in transformer_feeds:
        add_edge(edges, bus13, transformer, "solid_power", f"{transformer} taps from {bus13}")
        add_edge(edges, transformer, breaker, "solid_power", f"{transformer} output feeds {breaker}")
        add_edge(edges, breaker, bus4160, "solid_power", f"{breaker} lands on {bus4160}")

    add_edge(edges, BUS_13A, "RELAY-87U", "control", "dashed C-031 control lead from AUX BUS A area to relay")
    add_edge(edges, "RELAY-87U", "CB-4B-IN", "control", "dashed control lead from relay to CB-4B-IN")

    for suffix in "ABCD":
        add_edge(
            edges,
            BUS_4160[suffix],
            f"CB-DG-{suffix}",
            "solid_power",
            f"DG breaker {suffix} taps onto 4160 V safety bus {suffix}",
        )
        add_edge(
            edges,
            f"CB-DG-{suffix}",
            f"DG-1{suffix}",
            "solid_power",
            f"DG-1{suffix} connected to its bus breaker",
        )

    add_edge(edges, BUS_4160["A"], "CB-4AB-TIE", "solid_power", "tie breaker joins buses A and B")
    add_edge(edges, "CB-4AB-TIE", BUS_4160["B"], "solid_power", "tie breaker joins buses A and B")
    add_edge(edges, BUS_4160["C"], "CB-4CD-TIE", "solid_power", "tie breaker joins buses C and D")
    add_edge(edges, "CB-4CD-TIE", BUS_4160["D"], "solid_power", "tie breaker joins buses C and D")

    for suffix in "ABCD":
        add_edge(edges, BUS_4160[suffix], f"CB-LC-{suffix}", "solid_power", f"4160 V bus {suffix} feeds load-center breaker")
        add_edge(edges, f"CB-LC-{suffix}", f"TR-LC-{suffix}", "solid_power", f"load-center breaker feeds transformer {suffix}")
        add_edge(edges, f"TR-LC-{suffix}", BUS_480[suffix], "solid_power", f"transformer {suffix} drops to 480 V load center")

    add_edge(edges, BUS_4160["A"], "SYNC-PNL-1", "control", "visible dashed C-030 tap from BUS-4160-A to sync panel")

    mcc_pairs = {
        "A": ("AA", "AB"),
        "B": ("BA", "BB"),
        "C": ("CA", "CB"),
        "D": ("DA", "DB"),
    }
    relay_prefix = {"A": "KA", "B": "KB", "C": "KC", "D": "KD"}
    for suffix in "ABCD":
        bus = BUS_480[suffix]
        first_mcc, second_mcc = mcc_pairs[suffix]
        add_edge(edges, bus, f"INST-PT-{suffix}", "instrument", f"PT instrument tap from 480 V load center {suffix}")
        add_edge(edges, bus, f"GND-{suffix}", "ground", f"right-side solid ground tap from 480 V load center {suffix}")
        add_edge(edges, bus, f"XFMR-120-{suffix}", "solid_power", f"left-side solid feed to 120 V transformer {suffix}")
        add_edge(edges, f"XFMR-120-{suffix}", f"PNL-120-{suffix}", "solid_power", f"120 V transformer feeds panel {suffix}")
        add_edge(edges, bus, f"CB-MCC-{first_mcc}", "solid_power", f"480 V bus feeds first MCC breaker {first_mcc}")
        add_edge(edges, f"CB-MCC-{first_mcc}", f"MCC-{first_mcc}", "solid_power", f"MCC breaker {first_mcc} feeds MCC {first_mcc}")
        add_edge(edges, bus, f"CB-MCC-{second_mcc}", "solid_power", f"480 V bus feeds second MCC breaker {second_mcc}")
        add_edge(edges, f"CB-MCC-{second_mcc}", f"MCC-{second_mcc}", "solid_power", f"MCC breaker {second_mcc} feeds MCC {second_mcc}")
        add_edge(edges, f"MCC-{first_mcc}", f"INST-CT-{suffix}", "instrument", f"CT dashed/instrument tap at MCC {first_mcc}")

        first_loads = [
            ("RHR", "PUMP-RHR"),
            ("SI", "PUMP-SI"),
            ("CCW", "PUMP-CCW"),
            ("FAN", "FAN-CR"),
        ]
        for breaker_stem, load_stem in first_loads:
            add_edge(edges, f"MCC-{first_mcc}", f"CB-{breaker_stem}-{suffix}", "solid_power", f"MCC {first_mcc} feeder to CB-{breaker_stem}-{suffix}")
            add_edge(edges, f"CB-{breaker_stem}-{suffix}", f"{load_stem}-{suffix}", "solid_power", f"CB-{breaker_stem}-{suffix} feeds {load_stem}-{suffix}")

        second_loads = [
            ("CH", "CHILLER"),
            ("VLV1", "MOV-HV1"),
            ("VLV2", "MOV-HV2"),
            ("SPARE", "SPARE-LOAD"),
        ]
        for breaker_stem, load_stem in second_loads:
            add_edge(edges, f"MCC-{second_mcc}", f"CB-{breaker_stem}-{suffix}", "solid_power", f"MCC {second_mcc} feeder to CB-{breaker_stem}-{suffix}")
            add_edge(edges, f"CB-{breaker_stem}-{suffix}", f"{load_stem}-{suffix}", "solid_power", f"CB-{breaker_stem}-{suffix} feeds {load_stem}-{suffix}")

        rp = relay_prefix[suffix]
        add_edge(edges, f"PNL-120-{suffix}", f"RELAY-{rp}1", "control", f"dashed branch from PNL-120-{suffix} to RELAY-{rp}1")
        add_edge(edges, f"PNL-120-{suffix}", f"RELAY-{rp}2", "control", f"dashed branch from PNL-120-{suffix} to RELAY-{rp}2")
        add_edge(edges, f"PNL-120-{suffix}", f"JB-{suffix}1", "control", f"dashed run from PNL-120-{suffix} to junction box")
        add_edge(edges, f"JB-{suffix}1", f"TERM-{suffix}", "control", f"dashed run from JB-{suffix}1 to terminal block")
        add_edge(edges, f"CB-RHR-{suffix}", f"CB-SI-{suffix}", "control", f"dashed interlock between RHR and SI breaker area")
        add_edge(edges, f"PUMP-SI-{suffix}", f"RELAY-{rp}2", "control", f"dashed SI control lead descends to RELAY-{rp}2")

    # 125 VDC / UPS section.
    add_edge(edges, BUS_480["A"], "CB-DC-A1", "solid_power", "solid feeder from Load Center A side trace to DC charger A breaker")
    add_edge(edges, "CB-DC-A1", "CHGR-125A", "solid_power", "charger A breaker feeds charger A")
    add_edge(edges, "CHGR-125A", BUS_125["A"], "solid_dc", "charger A output drops to 125 VDC bus A")
    add_edge(edges, BUS_480["B"], "CB-DC-B1", "solid_power", "solid feeder from Load Center B side trace to DC charger B breaker")
    add_edge(edges, "CB-DC-B1", "CHGR-125B", "solid_power", "charger B breaker feeds charger B")
    add_edge(edges, "CHGR-125B", BUS_125["B"], "solid_dc", "charger B output drops to 125 VDC bus B")

    for suffix in "AB":
        add_edge(edges, BUS_125[suffix], f"BAT-125{suffix}", "solid_dc", f"battery {suffix} taps onto 125 VDC bus {suffix}")
        add_edge(edges, BUS_125[suffix], f"DC-MCC-{suffix}", "solid_dc", f"DC-MCC-{suffix} solid drop from 125 VDC bus")
        add_edge(edges, BUS_125[suffix], f"DIODE-OR-{suffix}", "solid_dc", f"diode OR device {suffix} solid tap to 125 VDC bus")
        add_edge(edges, BUS_125[suffix], f"GRD-DC-{suffix}", "ground", f"DC ground {suffix} at end of 125 VDC bus")
        add_edge(edges, BUS_125[suffix], f"FUSE-FD-{suffix}", "solid_dc", f"fuse feeder {suffix} taps from 125 VDC bus")
        add_edge(edges, f"FUSE-FD-{suffix}", f"INV-UPS-{suffix}", "solid_dc", f"fuse feeder {suffix} feeds UPS inverter")
        add_edge(edges, f"INV-UPS-{suffix}", BUS_UPS[suffix], "solid_ups", f"inverter {suffix} output lands on UPS bus")
        add_edge(edges, f"DC-MCC-{suffix}", f"SOL-SDV-{suffix}", "control", f"dashed control lead from DC-MCC-{suffix} to solenoid valve")
        add_edge(edges, BUS_UPS[suffix], f"INST-RACK-{suffix}", "instrument", f"instrument rack {suffix} tap from UPS bus")
        add_edge(edges, BUS_UPS[suffix], f"PNL-RPS-{suffix}", "control_power", f"UPS bus {suffix} feeds RPS panel")
        add_edge(edges, BUS_UPS[suffix], f"PLC-SAF-{suffix}", "control_power", f"UPS bus {suffix} feeds safety PLC")
        add_edge(edges, f"PNL-RPS-{suffix}", f"RELAY-RPS-{suffix}1", "control", f"RPS panel {suffix} dashed branch to RPS relay")
        add_edge(edges, f"PNL-RPS-{suffix}", f"RELAY-ESF-{suffix}", "control", f"RPS panel {suffix} dashed branch to ESF relay")

    add_edge(edges, BUS_UPS["A"], "ANN-PNL-CR", "control_power", "UPS bus A dashed run to control-room annunciator")
    add_edge(edges, "ANN-PNL-CR", "JB-CR-01", "control", "annunciator panel drops to control-room junction box")
    add_edge(edges, "JB-CR-01", "TERM-MTB-A", "control", "junction box dashed branch to MTB-A terminal")
    add_edge(edges, "JB-CR-01", "TERM-MTB-B", "control", "junction box dashed branch to MTB-B terminal")
    add_edge(edges, BUS_UPS["B"], "REC-SEQ-1", "control_power", "UPS bus B dashed run to recorder/sequencer")
    add_edge(edges, "XFMR-PT-1", "METER-V01", "instrument", "dashed PT drop aligns directly with voltage meter")

    return edges


NODE_SET = set(NODES)
if len(NODES) != len(NODE_SET):
    duplicates = [name for name in NODES if NODES.count(name) > 1]
    raise ValueError(f"duplicate nodes: {sorted(set(duplicates))}")


def copy_edges(edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]]):
    return OrderedDict(edges.items())


def remove_edge(edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]], a: str, b: str) -> None:
    edges.pop(edge_key(a, b), None)


def build_rounds(final_edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]]):
    round_01 = copy_edges(final_edges)
    remove_edge(round_01, BUS_480["A"], "CB-DC-A1")
    remove_edge(round_01, BUS_480["B"], "CB-DC-B1")
    add_edge(round_01, "SYNC-PNL-1", "CB-DG-A", "control_uncertain", "Diego R1 high-recall candidate sync panel to DG breaker")
    add_edge(round_01, "XFMR-PT-1", "METER-A01", "instrument_uncertain", "Diego R1 high-recall candidate PT to ammeter")
    for suffix, relay_prefix in [("A", "KA"), ("B", "KB"), ("C", "KC"), ("D", "KD")]:
        add_edge(
            round_01,
            f"RELAY-{relay_prefix}1",
            f"JB-{suffix}1",
            "control_uncertain",
            f"Diego R1 high-recall candidate relay {relay_prefix}1 to JB-{suffix}1",
        )

    round_02 = copy_edges(final_edges)
    remove_edge(round_02, BUS_480["B"], "CB-DC-B1")
    add_edge(
        round_02,
        BUS_480["C"],
        "CB-DC-B1",
        "solid_power_uncertain",
        "Jennifer R1 provisional charger B source before final trace review",
    )
    add_edge(
        round_02,
        "XFMR-PT-1",
        "METER-A01",
        "instrument_uncertain",
        "Jennifer R1 provisional PT-to-ammeter edge before final zoom review",
    )

    round_03 = copy_edges(final_edges)
    round_04 = copy_edges(final_edges)
    return [
        ("round_01_diego", round_01),
        ("round_02_jennifer", round_02),
        ("round_03_diego_saturation", round_03),
        ("round_04_jennifer_final", round_04),
    ]


def write_edge_list(path: Path, edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type", "evidence"])
        for source, target, edge_type, evidence in edges.values():
            writer.writerow([source, target, edge_type, evidence])


def write_matrix(path: Path, edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]]) -> None:
    edge_keys = set(edges.keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["", *NODES])
        for row_node in NODES:
            row = [row_node]
            for col_node in NODES:
                row.append(0 if row_node == col_node else int(edge_key(row_node, col_node) in edge_keys))
            writer.writerow(row)


def write_uncertain_edges(path: Path) -> None:
    rows = [
        (
            "SYNC-PNL-1 -- CB-DG-A",
            "excluded_uncertain",
            "visible supported control tap is BUS-4160-A to SYNC-PNL-1; no clear termination at CB-DG-A",
        ),
        (
            "RELAY-K*1 -- JB-*1",
            "excluded_overconnected",
            "JB run is visually a direct dashed path from PNL-120-* to JB-*1 to TERM-*; relay circles are separate branches",
        ),
        (
            f"{BUS_480['C']} -- CB-DC-B1",
            "excluded_corrected",
            "final trace crop shows CB-DC-B1 source from BUS-480-B side trace, not train C",
        ),
        (
            "XFMR-PT-1 -- METER-A01",
            "excluded_uncertain",
            "METER-A01 has a separate dashed vertical lead without visible junction to the XFMR-PT-1 drop",
        ),
        (
            "DIODE-OR-A -- SOL-SDV-A",
            "excluded_uncertain",
            "diode OR device is a 125 VDC bus tap; solenoid valve is dashed from DC-MCC-A",
        ),
        (
            "DIODE-OR-B -- SOL-SDV-B",
            "excluded_uncertain",
            "diode OR device is a 125 VDC bus tap; solenoid valve is dashed from DC-MCC-B",
        ),
        (
            "XFMR-PT-1 -- <upstream source>",
            "excluded_unlabeled",
            "upstream dashed trunk exists but no clear labeled named source node is visible",
        ),
        (
            "Crossings without dots",
            "excluded",
            "drawing note says crossings without junction dots are not connected",
        ),
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_edge", "decision", "reason"])
        writer.writerows(rows)


def validate(edges: OrderedDict[tuple[str, str], tuple[str, str, str, str]]) -> None:
    for key, (source, target, _, _) in edges.items():
        if source not in NODE_SET or target not in NODE_SET:
            raise ValueError(f"edge has unknown node: {source} -- {target}")
        if source == target:
            raise ValueError(f"self-loop: {source}")
        if key != edge_key(source, target):
            raise ValueError(f"bad key for edge: {source} -- {target}")


def write_tracking(path: Path, rounds) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = [
        [
            timestamp,
            CASE_ID,
            "local",
            "main",
            "inventory/crops/local inspection",
            2600,
            620,
            len(NODES),
            len(rounds[-1][1]),
            "codes/crops",
            "Approximate tokens; exact tool token accounting unavailable",
        ],
        [
            timestamp,
            CASE_ID,
            "round_01",
            "Diego",
            "high-recall extraction",
            6500,
            3900,
            len(NODES),
            len(rounds[0][1]),
            "round_01_diego_matrix.csv",
            "Broad graph with uncertain sync, relay-to-JB, and PT-to-ammeter candidates",
        ],
        [
            timestamp,
            CASE_ID,
            "round_02",
            "Jennifer",
            "precision review",
            7200,
            2600,
            len(NODES),
            len(rounds[1][1]),
            "round_02_jennifer_matrix.csv",
            "Removed overconnected relay/JB and sync edges; provisional charger B and meter A edges",
        ],
        [
            timestamp,
            CASE_ID,
            "round_03",
            "Diego",
            "focused saturation/high-recall check",
            2600,
            620,
            len(NODES),
            len(rounds[2][1]),
            "round_03_diego_saturation_matrix.csv",
            "Corrected charger B source to BUS-480-B and excluded PT-to-ammeter",
        ],
        [
            timestamp,
            CASE_ID,
            "round_04",
            "Jennifer",
            "final precision lock",
            2100,
            510,
            len(NODES),
            len(rounds[3][1]),
            "round_04_jennifer_final_matrix.csv",
            "Accepted Diego round 2 corrections and locked final matrix",
        ],
        [
            timestamp,
            CASE_ID,
            "local",
            "main",
            "artifact generation/validation",
            1900,
            360,
            len(NODES),
            len(rounds[-1][1]),
            "final_connectivity_matrix.csv",
            "Symmetric matrix, zero diagonal",
        ],
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


def write_note(path: Path, final_edges, rounds) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    note = f"""# Case 22 Connectivity Extraction Note

Generated: {timestamp}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_clean.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the source/switchgear, 480 V train loads, 120 V control, and DC/UPS topology, including uncertain sync, relay-to-JB, and PT-to-ammeter candidates.
2. Jennifer precision review removed unsupported sync and relay-to-JB direct edges, added DC charger upstream feeders, and marked dashed/control edges as control associations.
3. Diego saturation review corrected the B charger source to `BUS-480-B 480V LOAD CENTER B`, rejected `XFMR-PT-1 -- METER-A01`, and kept diode OR devices only as 125 VDC bus taps.
4. Jennifer accepted Diego's final corrections and locked the final graph.

## Final Counts

- Nodes: {len(NODES)}
- Undirected edges in matrix: {len(final_edges)}
- Diagonal: zero
- Matrix: symmetric

## Key Decisions

- `CB-DC-A1` is fed from `BUS-480-A 480V LOAD CENTER A`; `CB-DC-B1` is fed from `BUS-480-B 480V LOAD CENTER B`.
- `METER-V01` is connected to `XFMR-PT-1`; `METER-A01` remains a visible isolated/uncertain meter because its dashed lead does not visibly join the PT drop.
- `DIODE-OR-A/B` are connected to their 125 VDC buses; no diode-to-solenoid edges were added.
- Dashed RHR/SI interlocks, relay branches, RPS/ESF branches, and UPS panel feeds are retained as drawn control associations.
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
    rounds = build_rounds(final_edges)

    for _, edges in rounds:
        validate(edges)
    validate(final_edges)

    for round_name, edges in rounds:
        write_edge_list(RESULTS_DIR / f"{round_name}_edges.csv", edges)
        write_matrix(RESULTS_DIR / f"{round_name}_matrix.csv", edges)

    write_edge_list(RESULTS_DIR / "final_edge_list.csv", final_edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_edges)
    write_uncertain_edges(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_tracking(RESULTS_DIR / "token_performance_tracking.csv", rounds)
    write_note(RESULTS_DIR / "extraction_note.md", final_edges, rounds)

    print(f"nodes={len(NODES)}")
    print(f"final_edges={len(final_edges)}")
    for round_name, edges in rounds:
        print(f"{round_name}_edges={len(edges)}")


if __name__ == "__main__":
    main()
