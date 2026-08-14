from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"


DIEGO_R1_NODES = """
BUS-4A, BUS-4B, BUS-480A, BUS-480B, BUS-125DCA, BUS-125DCB, BUS-UPS-A, BUS-UPS-B, CB-TIE-4KV, CB-480-TIE, CB-DC-TIE
GRID-1, TR-SST-A, CB-SST-A, GEN-TG1, TR-UAT-1, CB-UAT-1, DG-1A, TR-DG-A, CB-DG-A, TR-480A
GRID-2, TR-SST-B, CB-SST-B, DG-1B, TR-DG-B, CB-DG-B, TR-480B
PANEL-ESF-A, PANEL-RPS-A, PANEL-LS-A, PANEL-MCR, PANEL-ANN, PANEL-LS-B, PANEL-RPS-B, PANEL-ESF-B
CHG-125A, BAT-125A, INV-120A, CHG-125B, BAT-125B, INV-120B
CB-4A-01, DS-4A-01, FU-A01, TB-A01, FI-A01, PUMP-CS-1A, RELAY-KA01, GND-A01
CB-4A-02, DS-4A-02, OL-A02, TB-A02, PI-A02, PUMP-RHR-1A, RELAY-KA02, GND-A02
CB-4A-07, DS-4A-07, FU-A07, TB-A07, PT-A07, PUMP-CCW-1A, RELAY-KA07, GND-A07
CB-4B-01, DS-4B-01, FU-B01, TB-B01, FI-B01, PUMP-CS-1B, RELAY-KB01, GND-B01
CB-4B-02, DS-4B-02, OL-B02, TB-B02, PI-B02, PUMP-RHR-1B, RELAY-KB02, GND-B02
CB-4B-07, DS-4B-07, FU-B07, TB-B07, PT-B07, PUMP-CCW-1B, RELAY-KB07, GND-B07
CB-480A-03, DS-480A-03, KON-A03, TB-A03, FS-A03, PUMP-SW-1A, RELAY-KA03, GND-A03
CB-480A-04, DS-480A-04, FU-A04, TB-A04, TS-A04, FAN-CR-1A, RELAY-KA04, GND-A04
CB-480A-05, DS-480A-05, OL-A05, TB-A05, ZS-A05, MOV-SI-101A, RELAY-KA05, GND-A05
CB-480A-06, DS-480A-06, KON-A06, TB-A06, VM-A06, RECT-AUX-1A, RELAY-KA06, GND-A06
CB-480A-08, DS-480A-08, OL-A08, TB-A08, TT-A08, HTR-PZR-A, RELAY-KA08, GND-A08
CB-480A-09, DS-480A-09, KON-A09, TB-A09, PS-A09, COMP-IA-1A, RELAY-KA09, GND-A09
CB-480B-03, DS-480B-03, KON-B03, TB-B03, FS-B03, PUMP-SW-1B, RELAY-KB03, GND-B03
CB-480B-04, DS-480B-04, FU-B04, TB-B04, TS-B04, FAN-CR-1B, RELAY-KB04, GND-B04
CB-480B-05, DS-480B-05, OL-B05, TB-B05, ZS-B05, MOV-SI-101B, RELAY-KB05, GND-B05
CB-480B-06, DS-480B-06, KON-B06, TB-B06, VM-B06, INV-AUX-1B, RELAY-KB06, GND-B06
CB-480B-08, DS-480B-08, OL-B08, TB-B08, LT-B08, HVAC-CHLR-1B, RELAY-KB08, GND-B08
"""


FINAL_NODES = """
BAT-125A,BAT-125B,BUS-125DCA,BUS-125DCB,BUS-480A,BUS-480B,BUS-4A,BUS-4B,BUS-UPS-A,BUS-UPS-B,CB-480A-03,CB-480A-04,CB-480A-05,CB-480A-06,CB-480A-08,CB-480A-09,CB-480B-03,CB-480B-04,CB-480B-05,CB-480B-06,CB-480B-08,CB-480-TIE,CB-4A-01,CB-4A-02,CB-4A-07,CB-4B-01,CB-4B-02,CB-4B-07,CB-DC-TIE,CB-DG-A,CB-DG-B,CB-SST-A,CB-SST-B,CB-TIE-4KV,CB-UAT-1,CHG-125A,CHG-125B,COMP-IA-1A,DG-1A,DG-1B,DS-480A-03,DS-480A-04,DS-480A-05,DS-480A-06,DS-480A-08,DS-480A-09,DS-480B-03,DS-480B-04,DS-480B-05,DS-480B-06,DS-480B-08,DS-4A-01,DS-4A-02,DS-4A-07,DS-4B-01,DS-4B-02,DS-4B-07,FAN-CR-1A,FAN-CR-1B,FI-A01,FI-B01,FS-A03,FS-B03,FU-A01,FU-A04,FU-A07,FU-B01,FU-B04,FU-B07,GEN-TG1,GND-A01,GND-A02,GND-A03,GND-A04,GND-A05,GND-A06,GND-A07,GND-A08,GND-A09,GND-B01,GND-B02,GND-B03,GND-B04,GND-B05,GND-B06,GND-B07,GND-B08,GRID-1,GRID-2,HTR-PZR-A,HVAC-CHLR-1B,INV-120A,INV-120B,INV-AUX-1B,KON-A03,KON-A06,KON-A09,KON-B03,KON-B06,LT-B08,MOV-SI-101A,MOV-SI-101B,OL-A02,OL-A05,OL-A08,OL-B02,OL-B05,OL-B08,PANEL-ANN,PANEL-MCR,PANEL-RPS-A,PI-A02,PI-B02,PS-A09,PT-A07,PT-B07,PUMP-CCW-1A,PUMP-CCW-1B,PUMP-CS-1A,PUMP-CS-1B,PUMP-RHR-1A,PUMP-RHR-1B,PUMP-SW-1A,PUMP-SW-1B,RECT-AUX-1A,TB-A01,TB-A02,TB-A03,TB-A04,TB-A05,TB-A06,TB-A07,TB-A08,TB-A09,TB-B01,TB-B02,TB-B03,TB-B04,TB-B05,TB-B06,TB-B07,TB-B08,TR-480A,TR-480B,TR-DG-A,TR-DG-B,TR-SST-A,TR-SST-B,TR-UAT-1,TS-A04,TS-B04,TT-A08,VM-A06,VM-B06,ZS-A05,ZS-B05
"""


DIEGO_R1_EDGES = """
A,B,type
GRID-1,TR-SST-A,P
TR-SST-A,CB-SST-A,P
CB-SST-A,BUS-4A,P
GEN-TG1,TR-UAT-1,P
TR-UAT-1,CB-UAT-1,P
CB-UAT-1,BUS-4A,P
DG-1A,TR-DG-A,P
TR-DG-A,CB-DG-A,P
CB-DG-A,BUS-4A,P
BUS-4A,TR-480A,P
TR-480A,BUS-480A,P
BUS-4A,CB-TIE-4KV,P
CB-TIE-4KV,BUS-4B,P
GRID-2,TR-SST-B,P
TR-SST-B,CB-SST-B,P
CB-SST-B,BUS-4B,P
DG-1B,TR-DG-B,P
TR-DG-B,CB-DG-B,P
CB-DG-B,BUS-4B,P
BUS-4B,TR-480B,P
TR-480B,BUS-480B,P
BUS-480A,CB-480-TIE,P
CB-480-TIE,BUS-480B,P
BUS-125DCA,CB-DC-TIE,DC
CB-DC-TIE,BUS-125DCB,DC
BUS-480A,PANEL-RPS-A,P
PANEL-RPS-A,CHG-125A,P
CHG-125A,BUS-125DCA,DC
BUS-125DCA,BAT-125A,DC
BUS-125DCA,INV-120A,DC
INV-120A,BUS-UPS-A,DC
BUS-480B,CHG-125B,P
CHG-125B,BUS-125DCB,DC
BUS-125DCB,BAT-125B,DC
BUS-125DCB,INV-120B,DC
INV-120B,BUS-UPS-B,DC
PANEL-MCR,PANEL-ANN,D
PANEL-ANN,CB-DC-TIE,D
BUS-4A,CB-4A-01,P
CB-4A-01,DS-4A-01,P
DS-4A-01,FU-A01,P
FU-A01,TB-A01,P
TB-A01,PUMP-CS-1A,P
PUMP-CS-1A,GND-A01,G
TB-A01,FI-A01,SIG
CB-4A-01,RELAY-KA01,D
BUS-4A,CB-4A-02,P
CB-4A-02,DS-4A-02,P
DS-4A-02,OL-A02,P
OL-A02,TB-A02,P
TB-A02,PUMP-RHR-1A,P
PUMP-RHR-1A,GND-A02,G
TB-A02,PI-A02,SIG
CB-4A-02,RELAY-KA02,D
BUS-4A,CB-4A-07,P
CB-4A-07,DS-4A-07,P
DS-4A-07,FU-A07,P
FU-A07,TB-A07,P
TB-A07,PUMP-CCW-1A,P
PUMP-CCW-1A,GND-A07,G
TB-A07,PT-A07,SIG
CB-4A-07,RELAY-KA07,D
BUS-4B,CB-4B-01,P
CB-4B-01,DS-4B-01,P
DS-4B-01,FU-B01,P
FU-B01,TB-B01,P
TB-B01,PUMP-CS-1B,P
PUMP-CS-1B,GND-B01,G
TB-B01,FI-B01,SIG
CB-4B-01,RELAY-KB01,D
BUS-4B,CB-4B-02,P
CB-4B-02,DS-4B-02,P
DS-4B-02,OL-B02,P
OL-B02,TB-B02,P
TB-B02,PUMP-RHR-1B,P
PUMP-RHR-1B,GND-B02,G
TB-B02,PI-B02,SIG
CB-4B-02,RELAY-KB02,D
BUS-4B,CB-4B-07,P
CB-4B-07,DS-4B-07,P
DS-4B-07,FU-B07,P
FU-B07,TB-B07,P
TB-B07,PUMP-CCW-1B,P
PUMP-CCW-1B,GND-B07,G
TB-B07,PT-B07,SIG
CB-4B-07,RELAY-KB07,D
BUS-480A,CB-480A-03,P
CB-480A-03,DS-480A-03,P
DS-480A-03,KON-A03,P
KON-A03,TB-A03,P
TB-A03,PUMP-SW-1A,P
PUMP-SW-1A,GND-A03,G
TB-A03,FS-A03,SIG
CB-480A-03,RELAY-KA03,D
BUS-480A,CB-480A-04,P
CB-480A-04,DS-480A-04,P
DS-480A-04,FU-A04,P
FU-A04,TB-A04,P
TB-A04,FAN-CR-1A,P
FAN-CR-1A,GND-A04,G
TB-A04,TS-A04,SIG
CB-480A-04,RELAY-KA04,D
BUS-480A,CB-480A-05,P
CB-480A-05,DS-480A-05,P
DS-480A-05,OL-A05,P
OL-A05,TB-A05,P
TB-A05,MOV-SI-101A,P
MOV-SI-101A,GND-A05,G
TB-A05,ZS-A05,SIG
CB-480A-05,RELAY-KA05,D
BUS-480A,CB-480A-06,P
CB-480A-06,DS-480A-06,P
DS-480A-06,KON-A06,P
KON-A06,TB-A06,P
TB-A06,RECT-AUX-1A,P
RECT-AUX-1A,GND-A06,G
TB-A06,VM-A06,SIG
CB-480A-06,RELAY-KA06,D
BUS-480A,CB-480A-08,P
CB-480A-08,DS-480A-08,P
DS-480A-08,OL-A08,P
OL-A08,TB-A08,P
TB-A08,HTR-PZR-A,P
HTR-PZR-A,GND-A08,G
TB-A08,TT-A08,SIG
CB-480A-08,RELAY-KA08,D
BUS-480A,CB-480A-09,P
CB-480A-09,DS-480A-09,P
DS-480A-09,KON-A09,P
KON-A09,TB-A09,P
TB-A09,COMP-IA-1A,P
COMP-IA-1A,GND-A09,G
TB-A09,PS-A09,SIG
CB-480A-09,RELAY-KA09,D
BUS-480B,CB-480B-03,P
CB-480B-03,DS-480B-03,P
DS-480B-03,KON-B03,P
KON-B03,TB-B03,P
TB-B03,PUMP-SW-1B,P
PUMP-SW-1B,GND-B03,G
TB-B03,FS-B03,SIG
CB-480B-03,RELAY-KB03,D
BUS-480B,CB-480B-04,P
CB-480B-04,DS-480B-04,P
DS-480B-04,FU-B04,P
FU-B04,TB-B04,P
TB-B04,FAN-CR-1B,P
FAN-CR-1B,GND-B04,G
TB-B04,TS-B04,SIG
CB-480B-04,RELAY-KB04,D
BUS-480B,CB-480B-05,P
CB-480B-05,DS-480B-05,P
DS-480B-05,OL-B05,P
OL-B05,TB-B05,P
TB-B05,MOV-SI-101B,P
MOV-SI-101B,GND-B05,G
TB-B05,ZS-B05,SIG
CB-480B-05,RELAY-KB05,D
BUS-480B,CB-480B-06,P
CB-480B-06,DS-480B-06,P
DS-480B-06,KON-B06,P
KON-B06,TB-B06,P
TB-B06,INV-AUX-1B,P
INV-AUX-1B,GND-B06,G
TB-B06,VM-B06,SIG
CB-480B-06,RELAY-KB06,D
BUS-480B,CB-480B-08,P
CB-480B-08,DS-480B-08,P
DS-480B-08,OL-B08,P
OL-B08,TB-B08,P
TB-B08,HVAC-CHLR-1B,P
HVAC-CHLR-1B,GND-B08,G
TB-B08,LT-B08,SIG
CB-480B-08,RELAY-KB08,D
"""


FINAL_EDGES = """
A,B,type
GRID-1,TR-SST-A,P
TR-SST-A,CB-SST-A,P
CB-SST-A,BUS-4A,P
GEN-TG1,TR-UAT-1,P
TR-UAT-1,CB-UAT-1,P
CB-UAT-1,BUS-4A,P
DG-1A,TR-DG-A,P
TR-DG-A,CB-DG-A,P
CB-DG-A,BUS-4A,P
BUS-4A,TR-480A,P
TR-480A,BUS-480A,P
BUS-4A,CB-TIE-4KV,P
CB-TIE-4KV,BUS-4B,P
GRID-2,TR-SST-B,P
TR-SST-B,CB-SST-B,P
CB-SST-B,BUS-4B,P
DG-1B,TR-DG-B,P
TR-DG-B,CB-DG-B,P
CB-DG-B,BUS-4B,P
BUS-4B,TR-480B,P
TR-480B,BUS-480B,P
BUS-480A,CB-480-TIE,P
CB-480-TIE,BUS-480B,P
BUS-125DCA,CB-DC-TIE,DC
CB-DC-TIE,BUS-125DCB,DC
BUS-480A,PANEL-RPS-A,P
PANEL-RPS-A,CHG-125A,P
CHG-125A,BUS-125DCA,DC
BUS-125DCA,BAT-125A,DC
BUS-125DCA,INV-120A,DC
INV-120A,BUS-UPS-A,DC
BUS-480B,CHG-125B,P
CHG-125B,BUS-125DCB,DC
BUS-125DCB,BAT-125B,DC
BUS-125DCB,INV-120B,DC
INV-120B,BUS-UPS-B,DC
PANEL-MCR,PANEL-ANN,D
PANEL-ANN,CB-DC-TIE,D
BUS-4A,CB-4A-01,P
CB-4A-01,DS-4A-01,P
DS-4A-01,FU-A01,P
FU-A01,TB-A01,P
TB-A01,PUMP-CS-1A,P
PUMP-CS-1A,GND-A01,G
TB-A01,FI-A01,SIG
BUS-4A,CB-4A-02,P
CB-4A-02,DS-4A-02,P
DS-4A-02,OL-A02,P
OL-A02,TB-A02,P
TB-A02,PUMP-RHR-1A,P
PUMP-RHR-1A,GND-A02,G
TB-A02,PI-A02,SIG
BUS-4A,CB-4A-07,P
CB-4A-07,DS-4A-07,P
DS-4A-07,FU-A07,P
FU-A07,TB-A07,P
TB-A07,PUMP-CCW-1A,P
PUMP-CCW-1A,GND-A07,G
TB-A07,PT-A07,SIG
BUS-4B,CB-4B-01,P
CB-4B-01,DS-4B-01,P
DS-4B-01,FU-B01,P
FU-B01,TB-B01,P
TB-B01,PUMP-CS-1B,P
PUMP-CS-1B,GND-B01,G
TB-B01,FI-B01,SIG
BUS-4B,CB-4B-02,P
CB-4B-02,DS-4B-02,P
DS-4B-02,OL-B02,P
OL-B02,TB-B02,P
TB-B02,PUMP-RHR-1B,P
PUMP-RHR-1B,GND-B02,G
TB-B02,PI-B02,SIG
BUS-4B,CB-4B-07,P
CB-4B-07,DS-4B-07,P
DS-4B-07,FU-B07,P
FU-B07,TB-B07,P
TB-B07,PUMP-CCW-1B,P
PUMP-CCW-1B,GND-B07,G
TB-B07,PT-B07,SIG
BUS-480A,CB-480A-03,P
CB-480A-03,DS-480A-03,P
DS-480A-03,KON-A03,P
KON-A03,TB-A03,P
TB-A03,PUMP-SW-1A,P
PUMP-SW-1A,GND-A03,G
TB-A03,FS-A03,SIG
BUS-480A,CB-480A-04,P
CB-480A-04,DS-480A-04,P
DS-480A-04,FU-A04,P
FU-A04,TB-A04,P
TB-A04,FAN-CR-1A,P
FAN-CR-1A,GND-A04,G
TB-A04,TS-A04,SIG
BUS-480A,CB-480A-05,P
CB-480A-05,DS-480A-05,P
DS-480A-05,OL-A05,P
OL-A05,TB-A05,P
TB-A05,MOV-SI-101A,P
MOV-SI-101A,GND-A05,G
TB-A05,ZS-A05,SIG
BUS-480A,CB-480A-06,P
CB-480A-06,DS-480A-06,P
DS-480A-06,KON-A06,P
KON-A06,TB-A06,P
TB-A06,RECT-AUX-1A,P
RECT-AUX-1A,GND-A06,G
TB-A06,VM-A06,SIG
BUS-480A,CB-480A-08,P
CB-480A-08,DS-480A-08,P
DS-480A-08,OL-A08,P
OL-A08,TB-A08,P
TB-A08,HTR-PZR-A,P
HTR-PZR-A,GND-A08,G
TB-A08,TT-A08,SIG
BUS-480A,CB-480A-09,P
CB-480A-09,DS-480A-09,P
DS-480A-09,KON-A09,P
KON-A09,TB-A09,P
TB-A09,COMP-IA-1A,P
COMP-IA-1A,GND-A09,G
TB-A09,PS-A09,SIG
BUS-480B,CB-480B-03,P
CB-480B-03,DS-480B-03,P
DS-480B-03,KON-B03,P
KON-B03,TB-B03,P
TB-B03,PUMP-SW-1B,P
PUMP-SW-1B,GND-B03,G
TB-B03,FS-B03,SIG
BUS-480B,CB-480B-04,P
CB-480B-04,DS-480B-04,P
DS-480B-04,FU-B04,P
FU-B04,TB-B04,P
TB-B04,FAN-CR-1B,P
FAN-CR-1B,GND-B04,G
TB-B04,TS-B04,SIG
BUS-480B,CB-480B-05,P
CB-480B-05,DS-480B-05,P
DS-480B-05,OL-B05,P
OL-B05,TB-B05,P
TB-B05,MOV-SI-101B,P
MOV-SI-101B,GND-B05,G
TB-B05,ZS-B05,SIG
BUS-480B,CB-480B-06,P
CB-480B-06,DS-480B-06,P
DS-480B-06,KON-B06,P
KON-B06,TB-B06,P
TB-B06,INV-AUX-1B,P
INV-AUX-1B,GND-B06,G
TB-B06,VM-B06,SIG
BUS-480B,CB-480B-08,P
CB-480B-08,DS-480B-08,P
DS-480B-08,OL-B08,P
OL-B08,TB-B08,P
TB-B08,HVAC-CHLR-1B,P
HVAC-CHLR-1B,GND-B08,G
TB-B08,LT-B08,SIG
"""


UNCERTAIN = [
    "BUS-480A,CHG-125A,P - direct feed possible only if PANEL-RPS-A is crossed rather than landed",
    "All CB-* to RELAY-* dashed candidates - relay symbol adjacent to dashed lead, no clean landing",
    "All RELAY-* to panel candidates - dashed run heads toward panel bundle, no panel landing visible",
    "PANEL-ESF-A,PANEL-RPS-A,D - dashed conductors pass near panels without explicit landing",
    "PANEL-RPS-A,PANEL-LS-A,D - dashed conductors pass near panels without explicit landing",
    "PANEL-LS-B,PANEL-RPS-B,D - dashed conductors pass near panels without explicit landing",
    "PANEL-RPS-B,PANEL-ESF-B,D - dashed conductors pass near panels without explicit landing",
]


ROUND_META = {
    "round01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "summary": "Initial proposal kept all plausible power/DC/signal/ground edges and accepted CB-to-relay dashed control edges; included several visible but isolated panel nodes.",
    },
    "round01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "summary": "Removed relay/control edges and isolated ambiguous panel nodes because the dashed conductors were adjacent or passing nearby without clean landed terminals.",
    },
    "round02_diego": {
        "agent": "Diego",
        "role": "high-recall saturation review",
        "summary": "Rechecked relay, panel, DC/UPS, and tie crops; agreed with Jennifer's corrected edge list unchanged.",
    },
    "round02_jennifer": {
        "agent": "Jennifer",
        "role": "precision final signoff",
        "summary": "Confirmed saturated/final unchanged; relay/panel/tie ambiguities remain excluded or uncertain.",
    },
}


def parse_nodes(text: str) -> list[str]:
    nodes: list[str] = []
    seen: set[str] = set()
    for raw in text.replace("\n", ",").split(","):
        node = raw.strip()
        if node and node not in seen:
            nodes.append(node)
            seen.add(node)
    return nodes


def parse_edges(text: str) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line == "A,B,type":
            continue
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
            raise ValueError(f"Bad edge line: {line}")
        edges.append((parts[0], parts[1], parts[2]))
    return edges


def edge_nodes(edges: list[tuple[str, str, str]]) -> set[str]:
    return {node for a, b, _ in edges for node in (a, b)}


def write_nodes(path: Path, nodes: list[str]) -> None:
    path.write_text("\n".join(nodes) + "\n", encoding="utf-8")


def write_edges(path: Path, edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["A", "B", "type"])
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edge_set = {frozenset((a, b)) for a, b, _ in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                if row_node == col_node:
                    row.append(0)
                else:
                    row.append(1 if frozenset((row_node, col_node)) in edge_set else 0)
            writer.writerow(row)


def write_pair_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edge_set = {frozenset((a, b)) for a, b, _ in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "column", "connected"])
        for a in nodes:
            for b in nodes:
                writer.writerow([a, b, 0 if a == b else int(frozenset((a, b)) in edge_set)])


def validate(nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    missing = sorted(edge_nodes(edges) - set(nodes))
    if missing:
        raise ValueError(f"Edges reference nodes absent from node list: {missing}")
    duplicate_edges = len({frozenset((a, b)) for a, b, _ in edges}) != len(edges)
    if duplicate_edges:
        raise ValueError("Duplicate undirected edge found")


def write_round(name: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> dict[str, object]:
    validate(nodes, edges)
    write_nodes(RESULTS_DIR / f"{name}_nodes.txt", nodes)
    write_edges(RESULTS_DIR / f"{name}_edges.csv", edges)
    write_matrix(RESULTS_DIR / f"{name}_connectivity_matrix.csv", nodes, edges)
    return {
        "round": name,
        "nodes": len(nodes),
        "edges": len(edges),
        **ROUND_META[name],
    }


def write_report(rounds: list[dict[str, object]], final_nodes: list[str], final_edges: list[tuple[str, str, str]]) -> None:
    lines = [
        "# Document 14 Connectivity Extraction Report",
        "",
        "Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.",
        "",
        "## Final Matrix",
        "",
        f"- Final node count: {len(final_nodes)}",
        f"- Final accepted edge count: {len(final_edges)}",
        "- Matrix file: `final_connectivity_matrix.csv`",
        "- Sparse edge file: `final_sparse_edges.csv`",
        "",
        "## Round Summary",
        "",
        "| Round | Agent | Nodes | Edges | Summary |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rounds:
        lines.append(
            f"| {row['round']} | {row['agent']} | {row['nodes']} | {row['edges']} | {row['summary']} |"
        )
    lines.extend(
        [
            "",
            "## Final Precision Changes",
            "",
            "- Demoted all `CB-*` to `RELAY-*` control edges from Diego R1 because relay symbols were adjacent to dashed leads without clear landed terminals.",
            "- Excluded isolated/ambiguous panel nodes `PANEL-ESF-A`, `PANEL-LS-A`, `PANEL-LS-B`, `PANEL-RPS-B`, and `PANEL-ESF-B`.",
            "- Kept `PANEL-RPS-A` because the solid feeder visibly lands through it to `CHG-125A`.",
            "- Kept `PANEL-MCR`, `PANEL-ANN`, and `CB-DC-TIE` dashed path because the vertical dashed route visibly lands through the two panel symbols to the DC tie breaker.",
            "",
            "## Excluded Or Still Uncertain",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in UNCERTAIN)
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    diego_r1_nodes = parse_nodes(DIEGO_R1_NODES)
    final_nodes = parse_nodes(FINAL_NODES)
    diego_r1_edges = parse_edges(DIEGO_R1_EDGES)
    final_edges = parse_edges(FINAL_EDGES)

    rounds = [
        write_round("round01_diego", diego_r1_nodes, diego_r1_edges),
        write_round("round01_jennifer", final_nodes, final_edges),
        write_round("round02_diego", final_nodes, final_edges),
        write_round("round02_jennifer", final_nodes, final_edges),
    ]

    validate(final_nodes, final_edges)
    write_nodes(RESULTS_DIR / "final_nodes.txt", final_nodes)
    write_edges(RESULTS_DIR / "final_sparse_edges.csv", final_edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_pair_matrix(RESULTS_DIR / "final_sparse_matrix_pairs.csv", final_nodes, final_edges)
    (RESULTS_DIR / "rounds_connectivity.json").write_text(json.dumps(rounds, indent=2) + "\n", encoding="utf-8")
    write_report(rounds, final_nodes, final_edges)

    print(f"Wrote {len(rounds)} round matrices.")
    print(f"Final nodes: {len(final_nodes)}")
    print(f"Final edges: {len(final_edges)}")


if __name__ == "__main__":
    main()
