from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


NODE_TEXT = """
GEN-G201; IPB-201; CB-GEN-201; GSU-201; SWYD-BUS-A; SWYD-BUS-B; CB-TIE-230; CB-GRID-A; GRID-230A; CB-GRID-B; GRID-230B; TR-UAT-201; TR-UAT-202; TR-SST-201; TR-SST-202; CB-UAT-1; CB-UAT-2; CB-SST-1; CB-SST-2; DG EDG-201A; CT-EDG-A; CB-DG-A; ATS-A; BUS-6KV-A; PT-6KV-A; DS-6KV-A; CB-TIE-6KV; DG EDG-201B; CT-EDG-B; CB-DG-B; ATS-B; BUS-6KV-B; PT-6KV-B; DS-6KV-B; BUS-4KV-N; TR-480A; CB-LC-A1; LC-480A; UV-SENS-A; TR-480B; CB-LC-B1; LC-480B; UV-SENS-B; TR-480N; CB-LC-N1; LC-480N; MCC-CCW-A; JBX-CCW-A; PUMP-CCW-A; MOV-CCW-201A; MCC-SW-A; JBX-SW-A; PUMP-SW-A; MCC-HPI-A; PUMP-HPI-A; MCC-VENT-A; MOV-SI-201A; FAN-CR-A; MCC-CCW-B; JBX-CCW-B; PUMP-CCW-B; MOV-CCW-201B; MCC-SW-B; JBX-SW-B; PUMP-SW-B; MCC-HPI-B; PUMP-HPI-B; MCC-VENT-B; MOV-SI-201B; FAN-CR-B; LP-N-A; HTR-BLDG-A; LP-N-B; HTR-BLDG-B; AC/DC CHGR-A; PNL-DC-A; DC/AC INV-A; BAT-125A; AC/DC REC-A; UPS-A; AC/DC CHGR-B; PNL-DC-B; DC/AC INV-B; BAT-125B; AC/DC REC-B; UPS-B; GND-A; GND-B; GND-MAIN; PNL-INST-A; PNL-INST-B; CP-ESFAS-A; CP-ESFAS-B; PLC-RPS-A; PLC-RPS-B; JBX-ESF-A; JBX-ESF-B; RELAY-UV-A; RELAY-UV-B; RELAY-SI-A; RELAY-SI-B; RELAY-LOAD-A; RELAY-LOAD-B; RELAY-DG-A; RELAY-DG-B
"""


DIEGO_R1_EDGE_TEXT = """
GEN-G201|IPB-201|H|solid feeder
IPB-201|CB-GEN-201|H|solid feeder
CB-GEN-201|GSU-201|H|solid feeder
GSU-201|SWYD-BUS-A|H|solid feeder
GSU-201|SWYD-BUS-B|M|high-recall lower-bus candidate
SWYD-BUS-A|CB-TIE-230|H|solid feeder
CB-TIE-230|SWYD-BUS-B|H|solid feeder
SWYD-BUS-A|CB-GRID-A|H|solid bus tap
CB-GRID-A|GRID-230A|H|solid feeder
SWYD-BUS-B|CB-GRID-B|H|solid bus tap
CB-GRID-B|GRID-230B|H|solid feeder
SWYD-BUS-B|TR-UAT-201|M|high-recall transformer source candidate
SWYD-BUS-B|TR-UAT-202|M|high-recall transformer source candidate
SWYD-BUS-B|TR-SST-201|M|solid/drop candidate
SWYD-BUS-B|TR-SST-202|M|solid/drop candidate
TR-UAT-201|CB-UAT-1|H|solid feeder
CB-UAT-1|BUS-6KV-A|H|solid bus drop
TR-SST-201|CB-SST-1|H|solid feeder
CB-SST-1|BUS-6KV-A|H|solid bus drop
TR-UAT-202|CB-UAT-2|H|solid feeder
CB-UAT-2|BUS-6KV-B|H|solid bus drop
TR-SST-202|CB-SST-2|H|solid feeder
CB-SST-2|BUS-6KV-B|H|solid bus drop
DG EDG-201A|CB-DG-A|H|solid feeder
CB-DG-A|ATS-A|H|solid feeder
ATS-A|BUS-6KV-A|H|solid bus drop
CT-EDG-A|DG EDG-201A|M|associated instrument line
BUS-6KV-A|PT-6KV-A|H|solid bus tap
BUS-6KV-A|DS-6KV-A|H|solid bus drop
BUS-6KV-A|CB-TIE-6KV|H|tie breaker terminal
CB-TIE-6KV|BUS-6KV-B|M|tie breaker terminal
DG EDG-201B|CB-DG-B|H|solid feeder
CB-DG-B|ATS-B|H|solid feeder
ATS-B|BUS-6KV-B|H|solid bus drop
CT-EDG-B|DG EDG-201B|M|associated instrument line
BUS-6KV-B|PT-6KV-B|H|solid bus tap
BUS-6KV-B|DS-6KV-B|H|solid bus drop
BUS-4KV-N|TR-480N|H|solid transformer drop
BUS-6KV-A|BUS-4KV-N|L|unsupported high-recall shortcut candidate
BUS-6KV-A|TR-480A|H|solid transformer drop
TR-480A|CB-LC-A1|H|solid feeder
CB-LC-A1|LC-480A|H|solid feeder
LC-480A|UV-SENS-A|M|dashed sensor lead
LC-480A|MCC-CCW-A|H|solid feeder
MCC-CCW-A|JBX-CCW-A|H|solid feeder
JBX-CCW-A|PUMP-CCW-A|H|solid feeder
MCC-CCW-A|MOV-CCW-201A|M|solid/control branch
LC-480A|MCC-SW-A|H|solid feeder
MCC-SW-A|JBX-SW-A|H|solid feeder
JBX-SW-A|PUMP-SW-A|H|solid feeder
LC-480A|MCC-HPI-A|H|solid feeder
MCC-HPI-A|PUMP-HPI-A|H|solid feeder
LC-480A|MCC-VENT-A|H|solid feeder
MCC-VENT-A|MOV-SI-201A|M|solid/control branch
MCC-VENT-A|FAN-CR-A|L|weak high-recall load branch
MOV-SI-201A|FAN-CR-A|L|dashed neighbor link
BUS-6KV-B|TR-480B|H|solid transformer drop
TR-480B|CB-LC-B1|H|solid feeder
CB-LC-B1|LC-480B|H|solid feeder
LC-480B|UV-SENS-B|M|dashed sensor lead
LC-480B|MCC-CCW-B|H|solid feeder
MCC-CCW-B|JBX-CCW-B|H|solid feeder
JBX-CCW-B|PUMP-CCW-B|H|solid feeder
MCC-CCW-B|MOV-CCW-201B|M|solid/control branch
LC-480B|MCC-SW-B|H|solid feeder
MCC-SW-B|JBX-SW-B|H|solid feeder
JBX-SW-B|PUMP-SW-B|H|solid feeder
LC-480B|MCC-HPI-B|H|solid feeder
MCC-HPI-B|PUMP-HPI-B|H|solid feeder
LC-480B|MCC-VENT-B|H|solid feeder
MCC-VENT-B|MOV-SI-201B|M|solid/control branch
MCC-VENT-B|FAN-CR-B|L|weak high-recall load branch
MOV-SI-201B|FAN-CR-B|L|dashed neighbor link
TR-480N|CB-LC-N1|H|solid feeder
CB-LC-N1|LC-480N|H|solid feeder
LC-480N|LP-N-A|H|solid feeder
LP-N-A|HTR-BLDG-A|H|solid feeder
LC-480N|LP-N-B|H|solid feeder
LP-N-B|HTR-BLDG-B|H|solid feeder
AC/DC CHGR-A|PNL-DC-A|H|DC/UPS link
PNL-DC-A|DC/AC INV-A|H|high-recall direct candidate
AC/DC CHGR-A|BAT-125A|H|battery link
BAT-125A|AC/DC REC-A|M|visible branch
AC/DC REC-A|PNL-DC-A|M|visible branch
AC/DC REC-A|UPS-A|M|visible branch
DC/AC INV-A|UPS-A|M|visible branch
BAT-125A|GND-A|M|dotted ground bond
GND-A|GND-MAIN|M|dotted ground bond
AC/DC CHGR-B|PNL-DC-B|H|DC/UPS link
PNL-DC-B|DC/AC INV-B|H|high-recall direct candidate
AC/DC CHGR-B|BAT-125B|H|battery link
BAT-125B|AC/DC REC-B|M|visible branch
AC/DC REC-B|PNL-DC-B|M|visible branch
AC/DC REC-B|UPS-B|M|visible branch
DC/AC INV-B|UPS-B|M|visible branch
BAT-125B|GND-B|M|dotted ground bond
GND-B|GND-MAIN|M|dotted ground bond
PNL-DC-A|PNL-DC-B|L|long common run candidate
CT-EDG-A|PNL-INST-A|L|long dashed instrument path
CT-EDG-B|PNL-INST-B|L|long dashed instrument path
UV-SENS-A|RELAY-UV-A|M|long dashed sensing path
UV-SENS-B|RELAY-UV-B|M|long dashed sensing path
PNL-INST-A|RELAY-UV-A|M|dashed terminal path
PNL-INST-B|RELAY-UV-B|M|dashed terminal path
PNL-INST-A|CP-ESFAS-A|L|dense dashed candidate
PNL-INST-B|CP-ESFAS-B|L|dense dashed candidate
CP-ESFAS-A|RELAY-SI-A|M|dashed terminal path
CP-ESFAS-B|RELAY-SI-B|M|dashed terminal path
CP-ESFAS-A|PLC-RPS-A|M|dashed terminal path
CP-ESFAS-B|PLC-RPS-B|M|dashed terminal path
CP-ESFAS-A|JBX-ESF-A|M|dashed terminal path
CP-ESFAS-B|JBX-ESF-B|M|dashed terminal path
PLC-RPS-A|RELAY-LOAD-A|M|dashed terminal path
PLC-RPS-B|RELAY-LOAD-B|M|dashed terminal path
PLC-RPS-A|RELAY-DG-A|L|dense dashed candidate
PLC-RPS-B|RELAY-DG-B|L|dense dashed candidate
JBX-ESF-A|RELAY-DG-A|M|dashed terminal path
JBX-ESF-B|RELAY-DG-B|M|dashed terminal path
DG EDG-201A|RELAY-DG-A|L|long dashed control route
DG EDG-201B|RELAY-DG-B|L|long dashed control route
ATS-A|RELAY-DG-A|L|long dashed control route
ATS-B|RELAY-DG-B|L|long dashed control route
MOV-SI-201A|RELAY-SI-A|L|long dashed route
MOV-SI-201B|RELAY-SI-B|L|long dashed route
FAN-CR-A|RELAY-LOAD-A|L|long dashed route
FAN-CR-B|RELAY-LOAD-B|L|long dashed route
PUMP-HPI-A|RELAY-LOAD-A|L|long dashed route
PUMP-HPI-B|RELAY-LOAD-B|L|long dashed route
"""


JENNIFER_R1_EDGE_TEXT = """
GEN-G201|IPB-201|H|solid feeder
IPB-201|CB-GEN-201|H|solid feeder
CB-GEN-201|GSU-201|H|solid feeder
GSU-201|SWYD-BUS-A|H|solid drop to upper switchyard bus
SWYD-BUS-A|CB-TIE-230|H|tie breaker terminal
CB-TIE-230|SWYD-BUS-B|H|tie breaker terminal
SWYD-BUS-A|CB-GRID-A|H|solid bus tap
CB-GRID-A|GRID-230A|H|solid feeder
SWYD-BUS-B|CB-GRID-B|H|solid bus tap
CB-GRID-B|GRID-230B|H|solid feeder
IPB-201|TR-UAT-201|M|generator/IPB branch
IPB-201|TR-UAT-202|M|generator/IPB branch
SWYD-BUS-B|TR-SST-201|H|solid lower-bus drop
SWYD-BUS-B|TR-SST-202|H|solid lower-bus drop
TR-UAT-201|CB-UAT-1|H|solid feeder
CB-UAT-1|BUS-6KV-A|H|solid bus drop
TR-SST-201|CB-SST-1|H|solid feeder
CB-SST-1|BUS-6KV-A|H|solid bus drop
TR-UAT-202|CB-UAT-2|H|solid feeder
CB-UAT-2|BUS-6KV-B|H|solid bus drop
TR-SST-202|CB-SST-2|H|solid feeder
CB-SST-2|BUS-6KV-B|H|solid bus drop
DG EDG-201A|CB-DG-A|H|solid feeder
CB-DG-A|ATS-A|H|solid feeder
ATS-A|BUS-6KV-A|H|solid bus drop
CT-EDG-A|DG EDG-201A|M|visible associated instrument line
BUS-6KV-A|PT-6KV-A|H|solid bus tap
BUS-6KV-A|DS-6KV-A|H|solid bus drop
DS-6KV-A|BUS-4KV-N|H|disconnect to 4 kV N bus
BUS-6KV-A|CB-TIE-6KV|H|tie breaker terminal
CB-TIE-6KV|BUS-6KV-B|H|tie breaker terminal
DG EDG-201B|CB-DG-B|H|solid feeder
CB-DG-B|ATS-B|H|solid feeder
ATS-B|BUS-6KV-B|H|solid bus drop
CT-EDG-B|DG EDG-201B|M|visible associated instrument line
BUS-6KV-B|PT-6KV-B|H|solid bus tap
BUS-6KV-B|DS-6KV-B|H|solid bus drop
DS-6KV-B|BUS-4KV-N|H|disconnect to 4 kV N bus
BUS-4KV-N|TR-480N|H|solid transformer drop
BUS-6KV-A|TR-480A|H|solid transformer drop
BUS-6KV-B|TR-480B|H|solid transformer drop
TR-480A|CB-LC-A1|H|solid feeder
CB-LC-A1|LC-480A|H|solid feeder
LC-480A|UV-SENS-A|M|dashed sensor lead
LC-480A|MCC-CCW-A|H|solid feeder
MCC-CCW-A|JBX-CCW-A|H|solid feeder
JBX-CCW-A|PUMP-CCW-A|H|solid feeder
MCC-CCW-A|MOV-CCW-201A|H|solid feeder
LC-480A|MCC-SW-A|H|solid feeder
MCC-SW-A|JBX-SW-A|H|solid feeder
JBX-SW-A|PUMP-SW-A|H|solid feeder
LC-480A|MCC-HPI-A|H|solid feeder
MCC-HPI-A|PUMP-HPI-A|H|solid feeder
LC-480A|MCC-VENT-A|H|solid feeder
MCC-VENT-A|MOV-SI-201A|H|solid feeder
MCC-VENT-A|FAN-CR-A|H|solid feeder
MOV-SI-201A|FAN-CR-A|U|short dashed neighbor link ambiguous
TR-480B|CB-LC-B1|H|solid feeder
CB-LC-B1|LC-480B|H|solid feeder
LC-480B|UV-SENS-B|M|dashed sensor lead
LC-480B|MCC-CCW-B|H|solid feeder
MCC-CCW-B|JBX-CCW-B|H|solid feeder
JBX-CCW-B|PUMP-CCW-B|H|solid feeder
MCC-CCW-B|MOV-CCW-201B|H|solid feeder
LC-480B|MCC-SW-B|H|solid feeder
MCC-SW-B|JBX-SW-B|H|solid feeder
JBX-SW-B|PUMP-SW-B|H|solid feeder
LC-480B|MCC-HPI-B|H|solid feeder
MCC-HPI-B|PUMP-HPI-B|H|solid feeder
LC-480B|MCC-VENT-B|H|solid feeder
MCC-VENT-B|MOV-SI-201B|H|solid feeder
MCC-VENT-B|FAN-CR-B|H|solid feeder
MOV-SI-201B|FAN-CR-B|U|short dashed neighbor link ambiguous
TR-480N|CB-LC-N1|H|solid feeder
CB-LC-N1|LC-480N|H|solid feeder
LC-480N|LP-N-A|H|solid feeder
LP-N-A|HTR-BLDG-A|H|solid feeder
LC-480N|LP-N-B|H|solid feeder
LP-N-B|HTR-BLDG-B|H|solid feeder
AC/DC CHGR-A|PNL-DC-A|H|solid DC/UPS link
AC/DC CHGR-A|BAT-125A|H|solid battery link
BAT-125A|AC/DC REC-A|M|visible branch but partly indirect
AC/DC REC-A|PNL-DC-A|H|solid vertical link
AC/DC REC-A|UPS-A|H|solid link
DC/AC INV-A|UPS-A|H|solid link
BAT-125A|GND-A|M|dotted ground bond
GND-A|GND-MAIN|M|dotted ground bond
AC/DC CHGR-B|PNL-DC-B|H|solid DC/UPS link
AC/DC CHGR-B|BAT-125B|H|solid battery link
BAT-125B|AC/DC REC-B|M|visible branch but partly indirect
AC/DC REC-B|PNL-DC-B|H|solid vertical link
AC/DC REC-B|UPS-B|H|solid link
DC/AC INV-B|UPS-B|H|solid link
BAT-125B|GND-B|M|dotted ground bond
GND-B|GND-MAIN|M|dotted ground bond
CT-EDG-A|PNL-INST-A|U|long dashed instrument path not fully traceable
CT-EDG-B|PNL-INST-B|U|long dashed instrument path not fully traceable
UV-SENS-A|RELAY-UV-A|M|long dashed sensing path
UV-SENS-B|RELAY-UV-B|M|long dashed sensing path
PNL-INST-A|RELAY-UV-A|M|dashed terminal-to-terminal path
PNL-INST-B|RELAY-UV-B|M|dashed terminal-to-terminal path
CP-ESFAS-A|RELAY-SI-A|M|dashed terminal path
CP-ESFAS-B|RELAY-SI-B|M|dashed terminal path
CP-ESFAS-A|PLC-RPS-A|U|shared dashed trunk/crossings ambiguous
CP-ESFAS-B|PLC-RPS-B|U|shared dashed trunk/crossings ambiguous
CP-ESFAS-A|JBX-ESF-A|M|dashed ESF path
CP-ESFAS-B|JBX-ESF-B|M|dashed ESF path
PLC-RPS-A|RELAY-LOAD-A|M|dashed terminal path
PLC-RPS-B|RELAY-LOAD-B|M|dashed terminal path
PLC-RPS-A|RELAY-DG-A|U|dense dashed trunk ambiguous
PLC-RPS-B|RELAY-DG-B|U|dense dashed trunk ambiguous
JBX-ESF-A|RELAY-DG-A|M|dashed terminal path
JBX-ESF-B|RELAY-DG-B|M|dashed terminal path
DG EDG-201A|RELAY-DG-A|U|long dashed control route ambiguous
DG EDG-201B|RELAY-DG-B|U|long dashed control route ambiguous
ATS-A|RELAY-DG-A|U|long dashed control route ambiguous
ATS-B|RELAY-DG-B|U|long dashed control route ambiguous
MOV-SI-201A|RELAY-SI-A|L|long dashed control/sensing route
MOV-SI-201B|RELAY-SI-B|L|long dashed control/sensing route
FAN-CR-A|RELAY-LOAD-A|L|long dashed load-control route
FAN-CR-B|RELAY-LOAD-B|L|long dashed load-control route
PUMP-HPI-A|RELAY-LOAD-A|L|long dashed load-control route
PUMP-HPI-B|RELAY-LOAD-B|L|long dashed load-control route
"""


def parse_nodes() -> list[str]:
    return [part.strip() for part in NODE_TEXT.replace("\n", " ").split(";") if part.strip()]


def parse_edges(text: str, include_uncertain: bool = False) -> list[dict[str, object]]:
    rows = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        source, target, confidence, evidence = [part.strip() for part in line.split("|", 3)]
        rows.append(
            {
                "source": source,
                "target": target,
                "confidence": confidence,
                "evidence": evidence,
                "include_in_matrix": confidence != "U" or include_uncertain,
            }
        )
    return rows


def write_nodes(slug: str, nodes: list[str]) -> None:
    with (RESULTS / f"{slug}_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "name"])
        for idx, node in enumerate(nodes, start=1):
            writer.writerow([idx, node])


def write_edges(slug: str, edges: list[dict[str, object]]) -> None:
    with (RESULTS / f"{slug}_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source", "target", "confidence", "evidence", "include_in_matrix"],
        )
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(slug: str, nodes: list[str], edges: list[dict[str, object]]) -> None:
    index = {node: idx for idx, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in edges:
        source = str(edge["source"])
        target = str(edge["target"])
        if source not in index or target not in index:
            raise ValueError(f"{slug}: unknown endpoint {source!r}, {target!r}")
        if not edge["include_in_matrix"]:
            continue
        i = index[source]
        j = index[target]
        if i == j:
            raise ValueError(f"{slug}: self loop {source!r}")
        matrix[i][j] = 1
        matrix[j][i] = 1

    with (RESULTS / f"{slug}_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = parse_nodes()
    rounds = {
        "round1_diego": {
            "agent": "Diego",
            "role": "high-recall extractor",
            "edges": parse_edges(DIEGO_R1_EDGE_TEXT, include_uncertain=True),
        },
        "round1_jennifer": {
            "agent": "Jennifer",
            "role": "precision reviewer",
            "edges": parse_edges(JENNIFER_R1_EDGE_TEXT, include_uncertain=False),
        },
        "round2_diego": {
            "agent": "Diego",
            "role": "reconciliation extractor",
            "edges": parse_edges(JENNIFER_R1_EDGE_TEXT, include_uncertain=False),
        },
        "round2_jennifer": {
            "agent": "Jennifer",
            "role": "final precision confirmation",
            "edges": parse_edges(JENNIFER_R1_EDGE_TEXT, include_uncertain=False),
        },
        "final": {
            "agent": "Diego + Jennifer",
            "role": "saturated agreed graph",
            "edges": parse_edges(JENNIFER_R1_EDGE_TEXT, include_uncertain=False),
        },
    }

    summary = {}
    for slug, data in rounds.items():
        edges = data["edges"]
        write_nodes(slug, nodes)
        write_edges(slug, edges)
        write_matrix(slug, nodes, edges)
        uncertain_edges = [edge for edge in edges if edge["confidence"] == "U"]
        if uncertain_edges:
            write_edges(f"{slug}_uncertain", uncertain_edges)
        summary[slug] = {
            "agent": data["agent"],
            "role": data["role"],
            "node_count": len(nodes),
            "edge_count_in_edge_file": len(edges),
            "edge_count_in_binary_matrix": sum(1 for edge in edges if edge["include_in_matrix"]),
            "uncertain_edge_count": sum(1 for edge in edges if edge["confidence"] == "U"),
        }

    with (RESULTS / "rounds_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
