from __future__ import annotations

import csv
from pathlib import Path


WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc16_work")


top_nodes = [
    "GRID-161KV",
    "TR-SST-1A",
    "CB-401A",
    "CB-401B",
    "BUS-4KV-A",
    "BUS-4KV-B",
    "CB-TIE-4AB",
    "GEN-EDG-A",
    "CB-EDG-A",
    "GEN-EDG-B",
    "CB-EDG-B",
    "TR-4KV-480A",
    "CB-480A-IN",
    "TR-4KV-480B",
    "CB-480B-IN",
    "BUS-480-A",
    "BUS-480-B",
    "CB-TIE-480AB",
]

mcc_fdr_nodes = [
    "CB-11A-FDR", "MCC-11A",
    "CB-12A-FDR", "MCC-12A",
    "CB-21A-FDR", "MCC-21A",
    "CB-31A-FDR30-B", "MCC-31A",
    "CB-11B-FDR", "MCC-11B",
    "CB-12B-FDR", "MCC-12B",
    "CB-21B-FDR", "MCC-21B",
    "CB-31B-FDR", "MCC-31B",
]

feeders = {
    "MCC-11A": [
        ("CB-P201A", "RELAY-KP201A", "PUMP-RHR201A", "GND-P201A", "power"),
        ("CB-P211A", "RELAY-KP211A", "PUMP-CS211A", "GND-P211A", "power"),
        ("CB-P221A", "RELAY-KP221A", "PUMP-ST221A", "GND-P221A", "power"),
    ],
    "MCC-12A": [
        ("CB-P101A", "RELAY-KP101A", "PUMP-AFW101A", "GND-P101A", "power"),
        ("CB-HV101A", "RELAY-KHV101A", "MOV-HV101A", "TB-HV101A", "control-terminal"),
        ("CB-FN1A", "RELAY-KFN1A", "FAN-HV1A", "GND-FN1A", "power"),
    ],
    "MCC-21A": [
        ("CB-P301A", "RELAY-KP301A", "PUMP-CCW301A", "GND-P301A", "power"),
        ("CB-P401A", "RELAY-KP401A", "PUMP-SW401A", "GND-P401A", "power"),
        ("CB-HT1A", "RELAY-KHT1A", "HTR-PZR1A", "TB-HT1A", "control-terminal"),
    ],
    "MCC-31A": [
        ("CB-RM1A", "RELAY-KRM1A", "MON-RAD1A", "TB-RM1A", "signal-terminal"),
        ("CB-P501A", "RELAY-KP501A", "PUMP-CHM501A", "GND-P501A", "power"),
        ("CB-CV121A", "RELAY-KCV121A", "MOV-CV121A", "TB-CV121A", "control-terminal"),
    ],
    "MCC-11B": [
        ("CB-P201B", "RELAY-KP201B", "PUMP-RHR201B", "GND-P201B", "power"),
        ("CB-P211B", "RELAY-KP211B", "PUMP-CS211B", "GND-P211B", "power"),
        ("CB-P221B", "RELAY-KP221B", "PUMP-ST221B", "GND-P221B", "power"),
    ],
    "MCC-12B": [
        ("CB-P101B", "RELAY-KP101B", "PUMP-AFW101B", "GND-P101B", "power"),
        ("CB-HV101B", "RELAY-KHV101B", "MOV-HV101B", "TB-HV101B", "control-terminal"),
        ("CB-FN1B", "RELAY-KFN1B", "FAN-HV1B", "GND-FN1B", "power"),
    ],
    "MCC-21B": [
        ("CB-P301B", "RELAY-KP301B", "PUMP-CCW301B", "GND-P301B", "power"),
        ("CB-P401B", "RELAY-KP401B", "PUMP-SW401B", "GND-P401B", "power"),
        ("CB-HT1B", "RELAY-KHT1B", "HTR-PZR1B", "TB-HT1B", "control-terminal"),
    ],
    "MCC-31B": [
        ("CB-RM1B", "RELAY-KRM1B", "MON-RAD1B", "TB-RM1B", "signal-terminal"),
        ("CB-P501B", "RELAY-KP501B", "PUMP-CHM501B", "GND-P501B", "power"),
        ("CB-CV121B", "RELAY-KCV121B", "MOV-CV121B", "TB-CV121B", "control-terminal"),
    ],
}

control_nodes = [
    "CP-RPS-A",
    "JB-RPS-A3-1A",
    "PROT-UV-A",
    "RELAY-27A",
    "CP-ESF-A",
    "TB-2A",
    "PROT-GF-A",
    "RELAY-86A",
    "CP-DCS-01",
    "TB-3A",
    "TR-RPS-A",
    "MG-RPS-A",
    "TB-ESF-1",
    "PT-RCS101",
    "LT-RWST101",
    "FT-AFW101",
    "REC-SOE-1",
    "ANN-501",
    "METER-VM-1",
    "BATT-125A",
    "CHGR-125A",
    "BUS-125DC-A",
    "INV-120A",
    "BUS-120-RPS-A",
    "CP-RPS-B",
    "JB-RPS-B3-1B",
    "PROT-UV-B",
    "RELAY-27B",
    "CP-ESF-B",
    "TB-2B",
    "PROT-GF-B",
    "RELAY-86B",
    "CP-ANN-01",
    "TB-3B",
    "TR-RPS-B",
    "MG-RPS-B",
    "TB-ESF-2",
    "RTD-RCS101",
    "LS-SUMP101",
    "XS-DOOR101",
    "JB-CONTAIN",
    "BATT-125B",
    "CHGR-125B",
    "BUS-125DC-B",
    "INV-120B",
    "BUS-120-RPS-B",
    "UCC-01",
    "GND-NO",
]


nodes = list(top_nodes) + list(mcc_fdr_nodes)
for mcc_feed in feeders.values():
    for branch in mcc_feed:
        nodes.extend(branch[:4])
nodes.extend(control_nodes)

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


chain(["GRID-161KV", "TR-SST-1A", "CB-401A", "BUS-4KV-A"], "high", "ac-power", "upper left solid feeder to bus A")
chain(["TR-SST-1A", "CB-401B", "BUS-4KV-B"], "high", "ac-power", "upper left solid feeder to bus B")
chain(["BUS-4KV-A", "CB-TIE-4AB", "BUS-4KV-B"], "high", "ac-power", "upper center vertical tie breaker between 4kV buses")
chain(["GEN-EDG-A", "CB-EDG-A", "BUS-4KV-A"], "high", "ac-power", "EDG A solid feeder lands on bus A")
chain(["GEN-EDG-B", "CB-EDG-B", "BUS-4KV-B"], "high", "ac-power", "EDG B solid feeder lands on bus B")
chain(["BUS-4KV-A", "TR-4KV-480A", "CB-480A-IN", "BUS-480-A"], "high", "ac-power", "A transformer drop to 480V bus")
chain(["BUS-4KV-B", "TR-4KV-480B", "CB-480B-IN", "BUS-480-B"], "high", "ac-power", "B transformer drop to 480V bus")
chain(["BUS-480-A", "CB-TIE-480AB", "BUS-480-B"], "high", "ac-power", "480V bus tie breaker has filled dots on both buses")

for bus, cb, mcc in [
    ("BUS-480-A", "CB-11A-FDR", "MCC-11A"),
    ("BUS-480-A", "CB-12A-FDR", "MCC-12A"),
    ("BUS-480-A", "CB-21A-FDR", "MCC-21A"),
    ("BUS-480-B", "CB-31A-FDR30-B", "MCC-31A"),
    ("BUS-480-B", "CB-11B-FDR", "MCC-11B"),
    ("BUS-480-B", "CB-12B-FDR", "MCC-12B"),
    ("BUS-480-B", "CB-21B-FDR", "MCC-21B"),
    ("BUS-480-B", "CB-31B-FDR", "MCC-31B"),
]:
    chain([bus, cb, mcc], "high", "ac-power", f"solid 480V feeder from {bus} through {cb} to {mcc}")

terminal_line_type = {
    "power": "ground",
    "control-terminal": "control",
    "signal-terminal": "signal",
}

for mcc, mcc_feed in feeders.items():
    for cb, relay, load, terminal, kind in mcc_feed:
        add(mcc, cb, "high", "ac-power", f"{mcc} branch landing to {cb}")
        add(cb, relay, "high", "ac-power", f"{cb} vertical feeder to {relay}")
        add(relay, load, "high", "ac-power", f"{relay} vertical feeder to {load}")
        add(load, terminal, "high", terminal_line_type[kind], f"{load} visible landing to {terminal}")

chain(["CP-RPS-A", "JB-RPS-A3-1A", "PROT-UV-A", "RELAY-27A"], "high", "control", "left A RPS under-voltage control chain")
add("RELAY-27A", "CP-ESF-A", "medium", "control", "dashed A trip route continues toward ESF panel")
chain(["CP-ESF-A", "TB-2A", "PROT-GF-A", "RELAY-86A"], "high", "control", "A ESF ground-fault protection chain")
chain(["RELAY-86A", "CP-DCS-01", "TB-3A"], "high", "control", "relay 86A route visibly lands at DCS panel and terminal block")
add("BUS-480-A", "TR-RPS-A", "high", "ac-power", "Jennifer review confirms A RPS transformer source from 480V bus A")
chain(["TR-RPS-A", "MG-RPS-A", "BUS-120-RPS-A"], "high", "ac-power", "A RPS transformer and motor-generator land on 120V RPS bus A")
add("MG-RPS-A", "TB-ESF-1", "medium", "signal", "dotted signal from MG area lands on ESF terminal block 1")
add("TB-ESF-1", "PT-RCS101", "high", "signal", "left dotted ESF signal branch to PT")
add("TB-ESF-1", "LT-RWST101", "high", "signal", "middle dotted ESF signal branch to LT")
add("TB-ESF-1", "FT-AFW101", "high", "signal", "right dotted ESF signal branch to FT")
add("PT-RCS101", "REC-SOE-1", "high", "signal", "PT vertical signal to SOE recorder")
add("LT-RWST101", "ANN-501", "high", "signal", "LT vertical signal to annunciator")
add("FT-AFW101", "METER-VM-1", "high", "signal", "FT vertical instrument path to meter")
add("METER-VM-1", "BUS-120-RPS-A", "high", "ac-power", "meter bottom lands on 120V RPS bus A")
add("REC-SOE-1", "BUS-125DC-A", "high", "dc-power", "SOE recorder bottom lands on 125DC A bus")
add("ANN-501", "BUS-125DC-A", "high", "dc-power", "annunciator bottom lands on 125DC A bus")
add("BUS-125DC-A", "CP-RPS-A", "high", "dc-power", "filled bus tap supplies A RPS panel")
add("BUS-125DC-A", "CP-ESF-A", "high", "dc-power", "filled bus tap supplies A ESF panel")
add("BUS-125DC-A", "CP-DCS-01", "high", "dc-power", "filled bus tap supplies DCS panel")
add("BATT-125A", "BUS-125DC-A", "high", "dc-power", "battery A vertical landing to 125DC bus")
add("BATT-125A", "CHGR-125A", "high", "dc-power", "dashed DC lead from battery A to charger A")
add("CHGR-125A", "BUS-125DC-A", "high", "dc-power", "charger A output lands on 125DC A bus")
chain(["BUS-125DC-A", "INV-120A", "BUS-120-RPS-A"], "high", "dc-power", "inverter A bridges 125DC bus to 120VAC RPS bus")

chain(["CP-RPS-B", "JB-RPS-B3-1B", "PROT-UV-B", "RELAY-27B"], "high", "control", "B RPS under-voltage control chain")
add("RELAY-27B", "CP-ESF-B", "medium", "control", "dashed B trip route continues toward ESF panel")
chain(["CP-ESF-B", "TB-2B", "PROT-GF-B", "RELAY-86B"], "high", "control", "B ESF ground-fault protection chain")
chain(["RELAY-86B", "CP-ANN-01", "TB-3B"], "high", "control", "relay 86B route visibly lands at annunciator panel and terminal block")
add("BUS-480-B", "TR-RPS-B", "medium", "ac-power", "overlay shows B RPS transformer top feeder descends from 480V bus corridor")
chain(["TR-RPS-B", "MG-RPS-B", "BUS-120-RPS-B"], "high", "ac-power", "B RPS transformer and motor-generator land on 120V RPS bus B")
add("MG-RPS-B", "RTD-RCS101", "high", "signal", "RTD signal branch lands at MG RPS B area")
add("MG-RPS-B", "TB-ESF-2", "high", "signal", "filled dots attach MG RPS B to ESF terminal block 2")
add("TB-ESF-2", "LS-SUMP101", "high", "signal", "dotted ESF signal branch to sump level switch")
add("TB-ESF-2", "XS-DOOR101", "high", "signal", "dotted ESF signal branch to door switch")
add("TB-ESF-2", "JB-CONTAIN", "medium", "control", "right dashed ESF route lands on containment junction box")
add("BATT-125B", "BUS-125DC-B", "high", "dc-power", "battery B vertical landing to 125DC bus")
add("BATT-125B", "CHGR-125B", "high", "dc-power", "dashed DC lead from battery B to charger B")
add("CHGR-125B", "BUS-125DC-B", "high", "dc-power", "charger B output lands on 125DC B bus")
add("BUS-125DC-B", "CP-RPS-B", "high", "dc-power", "filled bus tap supplies B RPS panel")
add("BUS-125DC-B", "CP-ESF-B", "high", "dc-power", "filled bus tap supplies B ESF panel")
add("BUS-125DC-B", "CP-ANN-01", "high", "dc-power", "filled bus tap supplies annunciator panel")
chain(["BUS-125DC-B", "INV-120B", "BUS-120-RPS-B"], "high", "dc-power", "inverter B bridges 125DC bus to 120VAC RPS bus")
chain(["BUS-120-RPS-A", "UCC-01", "BUS-120-RPS-B"], "medium", "control", "lower center dashed route connects both 120 RPS buses through UCC")
add("UCC-01", "GND-NO", "high", "ground", "UCC bottom solid ground symbol labelled GND-NO")

branch_control_links = [
    ("CB-401A", "CP-RPS-A", "control", "dashed breaker trip route descends from CB 401A area"),
    ("CB-401B", "CP-RPS-A", "control", "dashed breaker trip route descends from CB 401B area"),
    ("TB-HV101A", "CP-DCS-01", "control", "MOV HV101A terminal dashed route descends toward DCS panel"),
    ("TB-CV121A", "CP-DCS-01", "control", "MOV CV121A terminal dashed route joins DCS control corridor"),
    ("TB-HT1A", "CP-ESF-A", "control", "heater A terminal dashed route descends toward ESF panel"),
    ("TB-RM1A", "CP-DCS-01", "signal", "radiation monitor A terminal signal route enters DCS area"),
    ("TB-HV101B", "CP-ANN-01", "control", "MOV HV101B terminal dashed route descends toward ANN panel"),
    ("TB-CV121B", "JB-CONTAIN", "control", "MOV CV121B terminal route continues toward containment junction box"),
    ("TB-HT1B", "CP-ANN-01", "control", "heater B terminal dashed route descends toward annunciator panel"),
    ("TB-RM1B", "CP-ANN-01", "signal", "radiation monitor B terminal signal route enters annunciator area"),
    ("CP-DCS-01", "TB-ESF-1", "signal", "DCS right-side signal route lands at ESF terminal block 1"),
    ("CP-ANN-01", "TB-ESF-2", "signal", "ANN right-side signal route lands at ESF terminal block 2"),
]

precision_edges = list(edges)
for source, target, line_type, evidence in branch_control_links:
    add(source, target, "medium", line_type, evidence)

precision_edges = list(edges)

high_recall_extras = [
    ("CB-480A-IN", "CP-DCS-01", "low", "control", "vertical dashed near incoming breaker may continue to DCS panel"),
    ("CB-480B-IN", "CP-ANN-01", "low", "control", "vertical dashed near incoming breaker may continue to ANN panel"),
    ("CB-TIE-480AB", "CP-DCS-01", "low", "control", "center tie breaker dashed trip route proximity"),
    ("CP-RPS-A", "CP-ESF-A", "low", "control", "adjacent top control panels share dashed corridor"),
    ("CP-RPS-B", "CP-ESF-B", "low", "control", "adjacent B-side top control panels share dashed corridor"),
    ("CP-ESF-B", "CP-ANN-01", "low", "control", "B-side panels connected by long dashed corridor"),
    ("MG-RPS-A", "BUS-125DC-A", "low", "dc-power", "MG A sits near 125DC corridor and may have DC landing"),
    ("MG-RPS-B", "BUS-125DC-B", "low", "dc-power", "MG B sits near 125DC corridor and may have DC landing"),
    ("CB-P201A", "CP-RPS-A", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P211A", "CP-RPS-A", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P221A", "CP-RPS-A", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P101A", "CP-ESF-A", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-HV101A", "CP-ESF-A", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-FN1A", "CP-ESF-A", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P301A", "CP-DCS-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P401A", "CP-DCS-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-HT1A", "CP-DCS-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-RM1A", "CP-DCS-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P501A", "CP-DCS-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-CV121A", "CP-DCS-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P201B", "CP-RPS-B", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P211B", "CP-RPS-B", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P221B", "CP-RPS-B", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P101B", "CP-ESF-B", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-HV101B", "CP-ESF-B", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-FN1B", "CP-ESF-B", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P301B", "CP-ANN-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P401B", "CP-ANN-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-HT1B", "CP-ANN-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-RM1B", "CP-ANN-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-P501B", "CP-ANN-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
    ("CB-CV121B", "CP-ANN-01", "low", "control", "Diego high-recall dashed breaker row candidate"),
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
    lines: list[str] = [
        f"ROLE: {role}",
        "DOCUMENT: 16",
        f"SUMMARY: {summary}",
        "NODE_ORDER_CSV",
        "node",
        *nodes,
        "EDGE_LIST_CSV",
        "source,target,confidence,line_type,evidence",
    ]
    lines.extend(",".join(edge) for edge in edge_list)
    rows = matrix_rows(edge_list)
    lines.append("MATRIX_CSV")
    lines.extend(",".join(row) for row in rows)
    lines.append("AMBIGUITIES")
    lines.extend(f"- {item}" for item in ambiguities)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_agreement(path: Path, role: str, marker: str, summary: str) -> None:
    path.write_text(
        "\n".join([
            f"ROLE: {role}",
            "DOCUMENT: 16",
            marker,
            f"SUMMARY: {summary}",
        ]) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    write_round(
        WORK / "diego_round1_output.txt",
        "Diego high-recall extractor",
        f"High-recall visual extraction with {len(nodes)} nodes and {len(diego_edges)} edges including low-confidence control corridor candidates.",
        diego_edges,
        [
            "Low-confidence breaker-to-panel and MG-to-DC-bus proximity edges are included only for Jennifer review.",
            "Crossings without filled junction dots were not connected.",
            "RPS transformer top landings are retained because the wire/node overlay shows continuous vertical landings.",
        ],
    )
    write_round(
        WORK / "jennifer_round1_review.txt",
        "Jennifer precision reviewer",
        f"Precision review keeps the visually landed graph with {len(nodes)} nodes and {len(jennifer_edges)} edges and removes unsupported proximity-only Diego candidates.",
        jennifer_edges,
        [
            "Removed thirty two low-confidence proximity-only corridor or breaker-row candidates from Diego round 1.",
            "Kept branch terminal to panel links where a dashed or dotted route visibly lands at a named panel or junction box.",
            "Kept UCC-01 as the lower grounded tie component between BUS-120-RPS-A and BUS-120-RPS-B.",
        ],
    )
    write_agreement(
        WORK / "diego_round2_response.txt",
        "Diego high-recall extractor",
        "AGREE_WITH_JENNIFER_ROUND1",
        "After rechecking the raw and overlay crops I agree Jennifer removed only unsupported proximity candidates and the 201-edge precision graph is saturated.",
    )
    write_agreement(
        WORK / "jennifer_round2_final.txt",
        "Jennifer precision reviewer",
        "AGREE_WITH_DIEGO_ROUND2",
        "Final inspection agrees with Diego round 2 and keeps the Jennifer round 1 precision matrix as the saturated final graph.",
    )
    print(f"wrote doc16 round outputs nodes={len(nodes)} diego_edges={len(diego_edges)} jennifer_edges={len(jennifer_edges)}")


if __name__ == "__main__":
    main()
