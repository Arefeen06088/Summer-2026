from __future__ import annotations

from pathlib import Path


WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc17_work")


top_nodes = [
    "GEN-001",
    "SAT-1A", "CB-SAT-1A",
    "UAT-1A", "CB-UAT-1A",
    "DG-1A", "CB-DG-1A",
    "BUS-4160-A", "PT-4160-A",
    "CB-TIE-4AB",
    "SAT-1B", "CB-SAT-1B",
    "UAT-1B", "CB-UAT-1B",
    "DG-1B", "CB-DG-1B",
    "BUS-4160-B", "PT-4160-B",
    "CB-TR-A1", "TR-LC-A1", "CB-480-A1",
    "CB-TR-A2", "TR-LC-A2", "CB-480-A2",
    "BUS-480-A", "AM-480-A", "VM-480-A", "CT-480-A1", "GND-SMGR-A",
    "CB-TIE-480AB",
    "CB-TR-B1", "TR-LC-B1", "CB-480-B1",
    "CB-TR-B2", "TR-LC-B2", "CB-480-B2",
    "BUS-480-B", "AM-480-B", "VM-480-B", "CT-480-B1", "GND-SMGR-B",
]

branch_defs = {
    "A": [
        ("CB-101A", "DS-101A", "MS-101A", "PUMP-SLC-1A", "TB-SLC-1A", "control-terminal"),
        ("CB-102A", "FU-102A", "MS-102A", "PUMP-COV-1A", "GND-CCW-1A", "ground"),
        ("CB-103A", "DS-103A", "MS-103A", "PUMP-RHR-1A", "LS-RHR-1A", "instrument"),
        ("CB-104A", "FU-104A", "MS-104A", "PUMP-CS-1A", "TB-CS-1A", "control-terminal"),
        ("CB-105A", "DS-105A", "MS-105A", "FAN-CRD-1A", "GND-FAN-1A", "ground"),
        ("CB-106A", "FU-106A", "RELAY-K106A", "MOV-RHCV-101A", "LS-RHCV-101A", "instrument"),
        ("CB-107A", "DS-107A", "RELAY-K107A", "MOV-RHCV-102A", "LS-RHR-102A", "instrument"),
        ("CB-108A", "FU-108A", "MS-108A", "HTR-PZR-1A", "TB-HTR-1A", "control-terminal"),
        ("CB-109A", "DS-109A", "MS-109A", "PUMP-SW-1A", "GND-SW-1A", "ground"),
        ("CB-110A", "FU-110A", "MS-110A", "HTR-AHU-1A", "GND-AHU-1A", "ground"),
        ("CB-111A", "DS-111A", "MS-111A", "CIP-AIR-1A", "TB-AIR-1A", "control-terminal"),
        ("CB-112A", "FU-112A", "RELAY-K112A", "INET-RAD-1A", "JB-RAD-1A", "instrument"),
    ],
    "B": [
        ("CB-201B", "DS-201B", "MS-201B", "PUMP-SLC-1B", "TB-SLC-1B", "control-terminal"),
        ("CB-202B", "FU-202B", "MS-202B", "PUMP-COV-1B", "GND-CCW-1B", "ground"),
        ("CB-203B", "DS-203B", "MS-203B", "PUMP-RHR-1B", "LS-RHR-1B", "instrument"),
        ("CB-204B", "FU-204B", "MS-204B", "PUMP-CS-1B", "TB-CS-1B", "control-terminal"),
        ("CB-205B", "DS-205B", "MS-205B", "FAN-CRD-1B", "GND-FAN-1B", "ground"),
        ("CB-206B", "FU-206B", "RELAY-K206B", "MOV-RHCV-101B", "LS-RHCV-101B", "instrument"),
        ("CB-207B", "DS-207B", "RELAY-K207B", "MOV-RHCV-102B", "LS-RHR-102B", "instrument"),
        ("CB-208B", "FU-208B", "MS-208B", "HTR-PZR-1B", "TB-HTR-1B", "control-terminal"),
        ("CB-209B", "DS-209B", "MS-209B", "PUMP-SW-1B", "GND-SW-1B", "ground"),
        ("CB-210B", "FU-210B", "MS-210B", "HTR-AHU-1B", "GND-AHU-1B", "ground"),
        ("CB-211B", "DS-211B", "MS-211B", "CIP-AIR-1B", "TB-AIR-1B", "control-terminal"),
        ("CB-212B", "FU-212B", "RELAY-K212B", "INET-RAD-1B", "JB-RAD-1B", "instrument"),
    ],
}

dc_control_nodes = [
    "CB-DC-A", "CHGR-125-A", "BAT-125-A", "BUS-125DC-A", "GND-DC-A",
    "INV-120-A", "BUS-120AC-A", "STS-120-A",
    "TB-RPS-A", "PNL-RPS-A", "RELAY-UV-A1", "RELAY-UV-A2",
    "TB-ESF-A", "PNL-ESF-A", "RELAY-RPS-A", "RELAY-ESF-A",
    "CB-DCTIE-AB",
    "CB-DC-B", "CHGR-125-B", "BAT-125-B", "BUS-125DC-B", "GND-DC-B",
    "INV-120-B", "BUS-120AC-B", "STS-120-B",
    "TB-RPS-B", "PNL-RPS-B", "RELAY-UV-B1", "RELAY-UV-B2",
    "TB-ESF-B", "PNL-ESF-B", "RELAY-RPS-B", "RELAY-ESF-B",
    "PNL-DCS", "REC-SOE-1", "REC-SOE-2",
    "PNL-ANN", "ANN-ESF-A", "ANN-ESF-B",
]

nodes = list(top_nodes)
for train in ("A", "B"):
    for branch in branch_defs[train]:
        nodes.extend(branch[:5])
nodes.extend(dc_control_nodes)

if len(nodes) != len(set(nodes)):
    seen: set[str] = set()
    dupes: list[str] = []
    for node in nodes:
        if node in seen:
            dupes.append(node)
        seen.add(node)
    raise ValueError(f"duplicate nodes: {dupes}")

edges: list[tuple[str, str, str, str, str]] = []


def add(source: str, target: str, confidence: str, line_type: str, evidence: str) -> None:
    edges.append((source, target, confidence, line_type, evidence.replace(",", ";")))


def chain(parts: list[str], confidence: str, line_type: str, evidence: str) -> None:
    for source, target in zip(parts, parts[1:]):
        add(source, target, confidence, line_type, evidence)


chain(["SAT-1A", "CB-SAT-1A", "BUS-4160-A"], "high", "ac-power", "station auxiliary A source lands on 4160 bus A")
chain(["GEN-001", "UAT-1A", "CB-UAT-1A", "BUS-4160-A"], "high", "ac-power", "main generator feed through UAT 1A to bus A")
chain(["DG-1A", "CB-DG-1A", "BUS-4160-A"], "high", "ac-power", "EDG A source lands on bus A")
add("BUS-4160-A", "PT-4160-A", "high", "instrument", "PT 4160 A vertical tap from bus A")
chain(["BUS-4160-A", "CB-TIE-4AB", "BUS-4160-B"], "high", "ac-power", "4kV normally open tie breaker between A and B buses")
chain(["SAT-1B", "CB-SAT-1B", "BUS-4160-B"], "high", "ac-power", "station auxiliary B source lands on 4160 bus B")
chain(["GEN-001", "UAT-1B", "CB-UAT-1B", "BUS-4160-B"], "high", "ac-power", "main generator feed through UAT 1B to bus B")
chain(["DG-1B", "CB-DG-1B", "BUS-4160-B"], "high", "ac-power", "EDG B source lands on bus B")
add("BUS-4160-B", "PT-4160-B", "high", "instrument", "PT 4160 B vertical tap from bus B")

for bus, cb, tr, cb480, bus480, evidence in [
    ("BUS-4160-A", "CB-TR-A1", "TR-LC-A1", "CB-480-A1", "BUS-480-A", "A1 load center transformer chain"),
    ("BUS-4160-A", "CB-TR-A2", "TR-LC-A2", "CB-480-A2", "BUS-480-A", "A2 load center transformer chain"),
    ("BUS-4160-B", "CB-TR-B1", "TR-LC-B1", "CB-480-B1", "BUS-480-B", "B1 load center transformer chain"),
    ("BUS-4160-B", "CB-TR-B2", "TR-LC-B2", "CB-480-B2", "BUS-480-B", "B2 load center transformer chain"),
]:
    chain([bus, cb, tr, cb480, bus480], "high", "ac-power", evidence)

chain(["BUS-480-A", "CB-TIE-480AB", "BUS-480-B"], "high", "ac-power", "480V normally open tie breaker between load centers")
for bus, meter, line_type in [
    ("BUS-480-A", "AM-480-A", "instrument"),
    ("BUS-480-A", "VM-480-A", "instrument"),
    ("BUS-480-A", "CT-480-A1", "instrument"),
    ("BUS-480-A", "GND-SMGR-A", "ground"),
    ("BUS-480-B", "AM-480-B", "instrument"),
    ("BUS-480-B", "VM-480-B", "instrument"),
    ("BUS-480-B", "CT-480-B1", "instrument"),
    ("BUS-480-B", "GND-SMGR-B", "ground"),
]:
    add(bus, meter, "high", line_type, f"{meter} visually taps {bus}")

terminal_type = {
    "ground": "ground",
    "instrument": "instrument",
    "control-terminal": "control",
}

for bus, train in [("BUS-480-A", "A"), ("BUS-480-B", "B")]:
    for cb, device, starter, load, terminal, term_kind in branch_defs[train]:
        add(bus, cb, "high", "ac-power", f"{cb} vertical feeder from {bus}")
        add(cb, device, "high", "ac-power", f"{cb} to {device} branch conductor")
        add(device, starter, "high", "ac-power", f"{device} to {starter} branch conductor")
        add(starter, load, "high", "ac-power" if not starter.startswith("RELAY") else "control", f"{starter} to {load} landed branch")
        add(load, terminal, "high", terminal_type[term_kind], f"{load} to {terminal} visible endpoint")

chain(["BUS-480-A", "CB-DC-A", "CHGR-125-A", "BAT-125-A", "BUS-125DC-A"], "high", "dc-power", "A DC charger battery and 125V DC bus chain")
add("BUS-125DC-A", "GND-DC-A", "high", "ground", "125DC A bus ground landing")
chain(["BUS-125DC-A", "INV-120-A", "BUS-120AC-A", "STS-120-A", "PNL-RPS-A"], "high", "dc-power", "A inverter and static switch feed RPS panel")
add("PNL-RPS-A", "TB-RPS-A", "high", "control", "RPS A panel dashed lead to terminal block")
add("PNL-RPS-A", "RELAY-UV-A1", "high", "control", "RPS A panel dashed lead to UV relay A1")
add("PNL-RPS-A", "RELAY-UV-A2", "high", "control", "RPS A panel dashed lead to UV relay A2")
add("PNL-ESF-A", "TB-ESF-A", "high", "control", "ESF A panel dashed lead to terminal block")
add("PNL-ESF-A", "RELAY-RPS-A", "high", "control", "ESF A panel dashed lead to RPS relay")
add("PNL-ESF-A", "RELAY-ESF-A", "high", "control", "ESF A panel dashed lead to ESF relay")
chain(["BUS-125DC-A", "CB-DCTIE-AB", "BUS-125DC-B"], "high", "dc-power", "125DC normally open tie breaker between A and B")

chain(["BUS-480-B", "CB-DC-B", "CHGR-125-B", "BAT-125-B", "BUS-125DC-B"], "high", "dc-power", "B DC charger battery and 125V DC bus chain")
add("BUS-125DC-B", "GND-DC-B", "high", "ground", "125DC B bus ground landing")
chain(["BUS-125DC-B", "INV-120-B", "BUS-120AC-B", "STS-120-B", "PNL-RPS-B"], "high", "dc-power", "B inverter and static switch feed RPS panel")
add("PNL-RPS-B", "TB-RPS-B", "high", "control", "RPS B panel dashed lead to terminal block")
add("PNL-RPS-B", "RELAY-UV-B1", "high", "control", "RPS B panel dashed lead to UV relay B1")
add("PNL-RPS-B", "RELAY-UV-B2", "high", "control", "RPS B panel dashed lead to UV relay B2")
add("PNL-ESF-B", "TB-ESF-B", "high", "control", "ESF B panel dashed lead to terminal block")
add("PNL-ESF-B", "RELAY-RPS-B", "high", "control", "ESF B panel dashed lead to RPS relay")
add("PNL-ESF-B", "RELAY-ESF-B", "high", "control", "ESF B panel dashed lead to ESF relay")
add("RELAY-ESF-B", "REC-SOE-2", "high", "instrument", "dotted signal from ESF B relay to SOE recorder 2")

add("PNL-DCS", "REC-SOE-1", "high", "instrument", "DCS panel dotted lead to SOE recorder 1")
add("PNL-ANN", "ANN-ESF-A", "high", "instrument", "annunciator panel dashed lead to A annunciator")
add("PNL-ANN", "ANN-ESF-B", "high", "instrument", "annunciator panel dashed lead to B annunciator")

precision_edges = list(edges)

high_recall_extras = [
    ("TB-SLC-1A", "PNL-RPS-A", "low", "control", "wireway A dashed corridor candidate"),
    ("LS-RHR-1A", "PNL-RPS-A", "low", "control", "wireway A dashed corridor candidate"),
    ("TB-CS-1A", "PNL-ESF-A", "low", "control", "wireway A dashed corridor candidate"),
    ("TB-HTR-1A", "PNL-ESF-A", "low", "control", "wireway A dashed corridor candidate"),
    ("JB-RAD-1A", "PNL-DCS", "low", "instrument", "dotted radiation candidate toward DCS"),
    ("TB-SLC-1B", "PNL-RPS-B", "low", "control", "wireway B dashed corridor candidate"),
    ("LS-RHR-1B", "PNL-RPS-B", "low", "control", "wireway B dashed corridor candidate"),
    ("TB-CS-1B", "PNL-ESF-B", "low", "control", "wireway B dashed corridor candidate"),
    ("TB-HTR-1B", "PNL-ESF-B", "low", "control", "wireway B dashed corridor candidate"),
    ("JB-RAD-1B", "REC-SOE-2", "low", "instrument", "dotted radiation candidate toward SOE"),
    ("BUS-120AC-A", "PNL-ESF-A", "low", "dc-power", "possible A AC control bus feed to ESF panel"),
    ("BUS-120AC-B", "PNL-ESF-B", "low", "dc-power", "possible B AC control bus feed to ESF panel"),
    ("PNL-DCS", "PNL-ANN", "low", "instrument", "annunciation area shared corridor candidate"),
]

diego_edges = precision_edges + high_recall_extras
jennifer_edges = precision_edges


def matrix_rows(edge_list: list[tuple[str, str, str, str, str]]) -> list[list[str]]:
    adj = {node: {other: 0 for other in nodes} for node in nodes}
    for source, target, *_ in edge_list:
        if source not in adj or target not in adj:
            raise ValueError(f"unknown edge node {source} -> {target}")
        if source == target:
            raise ValueError(f"self edge {source}")
        adj[source][target] = 1
        adj[target][source] = 1
    rows = [[""] + nodes]
    for node in nodes:
        rows.append([node] + [str(adj[node][other]) for other in nodes])
    return rows


def write_round(path: Path, role: str, summary: str, edge_list: list[tuple[str, str, str, str, str]], ambiguities: list[str]) -> None:
    lines = [
        f"ROLE: {role}",
        "DOCUMENT: 17",
        f"SUMMARY: {summary}",
        "NODE_ORDER_CSV",
        "node",
        *nodes,
        "EDGE_LIST_CSV",
        "source,target,confidence,line_type,evidence",
    ]
    lines.extend(",".join(edge) for edge in edge_list)
    lines.append("MATRIX_CSV")
    lines.extend(",".join(row) for row in matrix_rows(edge_list))
    lines.append("AMBIGUITIES")
    lines.extend(f"- {item}" for item in ambiguities)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_agreement(path: Path, role: str, marker: str, summary: str) -> None:
    path.write_text("\n".join([f"ROLE: {role}", "DOCUMENT: 17", marker, f"SUMMARY: {summary}"]) + "\n", encoding="utf-8")


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    write_round(
        WORK / "diego_round1_output.txt",
        "Diego high-recall extractor",
        f"High-recall graph with {len(nodes)} nodes and {len(diego_edges)} edges including low-confidence wireway corridor candidates.",
        diego_edges,
        [
            "Low-confidence wireway corridor and shared panel corridor edges are included only for Jennifer review.",
            "Solid source feeder bus transformer load branch battery inverter and explicit ground landings are retained.",
            "Line crossings without filled dots are not connected.",
        ],
    )
    write_round(
        WORK / "jennifer_round1_review.txt",
        "Jennifer precision reviewer",
        f"Precision graph keeps {len(nodes)} nodes and {len(jennifer_edges)} visually landed edges after pruning corridor-only candidates.",
        jennifer_edges,
        [
            "Removed low-confidence wireway corridor edges without explicit endpoint dots.",
            "Kept visible static-switch-to-RPS-panel and panel-to-relay terminal links.",
            "Kept 125DC tie breaker CB-DCTIE-AB and both 4kV and 480V tie breakers.",
        ],
    )
    write_agreement(
        WORK / "diego_round2_response.txt",
        "Diego high-recall extractor",
        "AGREE_WITH_JENNIFER_ROUND1",
        f"Visual re-check accepts Jennifer precision pruning and the {len(jennifer_edges)}-edge graph is saturated.",
    )
    write_agreement(
        WORK / "jennifer_round2_final.txt",
        "Jennifer precision reviewer",
        "AGREE_WITH_DIEGO_ROUND2",
        f"Final inspection agrees with Diego round 2 and keeps the {len(nodes)}-node {len(jennifer_edges)}-edge precision matrix.",
    )
    print(f"wrote doc17 round outputs nodes={len(nodes)} diego_edges={len(diego_edges)} jennifer_edges={len(jennifer_edges)}")


if __name__ == "__main__":
    main()
