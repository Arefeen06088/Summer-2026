from __future__ import annotations

from collections import Counter


NODES = [
    "GRID-N230", "ISO-230A", "BRK-2301", "BUS-SY230", "GEN-G101", "GSU-1",
    "GRID-S230", "ISO-230B", "BRK-2302",
    "TR-RAT-1A", "TR-UAT-1A", "CB-AUX-A", "BUS-AUX13A",
    "TR-RAT-1B", "TR-UAT-1B", "CB-AUX-B", "BUS-AUX13B", "CB-TIE13", "BUS-NON1",
    "EDG-A", "CB-EDG-A", "TR-SAF-A", "CB-SAF-A", "BUS-416A", "CB-TIE-AB",
    "TR-480-A", "CB-LC-A", "LC-480A", "CB-MCCA1", "MCC-1A1", "CB-MCCA2", "MCC-1A2",
    "PUMP-AFW-A", "PUMP-CCW-A", "VLV-MSIV-A", "XFER-ATS-A", "CHG-125A", "BAT-125A",
    "PNL-DC-A", "UPS-PNL-A", "INV-UPS-A", "RECT-48V-A", "BAT-48V-A", "JB-RLY-A",
    "EDG-B", "CB-EDG-B", "TR-SAF-B", "CB-SAF-B", "BUS-416B",
    "TR-480-B", "CB-LC-B", "LC-480B", "CB-MCCB1", "MCC-1B1", "CB-MCCB2", "MCC-1B2",
    "PUMP-AFW-B", "PUMP-CCW-B", "VLV-MSIV-B", "JB-RLY-B",
    "EDG-C", "CB-EDG-C", "TR-SAF-C", "CB-SAF-C", "BUS-416C", "CB-TIE-CD",
    "TR-480-C", "CB-LC-C", "LC-480C", "CB-MCCC1", "MCC-1C1", "CB-MCCC2", "MCC-1C2",
    "PUMP-RHR-A", "FAN-CRHV-A", "HTR-BATRM-A", "XFER-ATS-B", "CHG-125B", "BAT-125B",
    "PNL-DC-B", "RECT-48V-B", "BAT-48V-B", "INV-UPS-B", "UPS-PNL-B",
    "EDG-D", "CB-EDG-D", "TR-SAF-D", "CB-SAF-D", "BUS-416D",
    "TR-480-D", "CB-LC-D", "LC-480D", "CB-MCCD1", "MCC-1D1", "CB-MCCD2", "MCC-1D2",
    "PUMP-RHR-B", "FAN-CRHV-B", "HTR-BATRM-B",
    "CP-ESFAS-1", "CP-ESFAS-2", "RELAY-K1A", "RELAY-K2A", "RELAY-K1B", "RELAY-K2B",
    "RELAY-UV-A", "RELAY-UV-B", "RELAY-LOOP-C", "RELAY-LOOP-D",
    "INST-NSSS-A", "INST-NSSS-B", "GND-GRID",
]


def chain(*items: str) -> list[tuple[str, str]]:
    return list(zip(items, items[1:]))


SOLID_EDGES = [
    *chain("GRID-N230", "ISO-230A", "BRK-2301", "BUS-SY230"),
    *chain("GRID-S230", "ISO-230B", "BRK-2302", "BUS-SY230"),
    *chain("GEN-G101", "GSU-1", "BUS-SY230"),
    *chain("BUS-SY230", "TR-RAT-1A", "CB-AUX-A", "BUS-AUX13A"),
    *chain("BUS-SY230", "TR-UAT-1A", "CB-AUX-A"),
    *chain("BUS-SY230", "TR-RAT-1B", "CB-AUX-B", "BUS-AUX13B"),
    *chain("BUS-SY230", "TR-UAT-1B", "CB-AUX-B"),
    *chain("BUS-AUX13A", "CB-TIE13", "BUS-AUX13B"),
    ("BUS-AUX13A", "BUS-NON1"),
    ("BUS-NON1", "TR-SAF-C"),
    *chain("BUS-AUX13A", "TR-SAF-A", "CB-SAF-A", "BUS-416A"),
    *chain("EDG-A", "CB-EDG-A", "BUS-416A"),
    *chain("BUS-416A", "CB-TIE-AB", "BUS-416B"),
    *chain("BUS-416A", "TR-480-A", "CB-LC-A", "LC-480A"),
    *chain("LC-480A", "CB-MCCA1", "MCC-1A1"),
    *chain("LC-480A", "CB-MCCA2", "MCC-1A2"),
    ("MCC-1A1", "PUMP-AFW-A"),
    *chain("MCC-1A1", "VLV-MSIV-A", "XFER-ATS-A"),
    ("MCC-1A2", "PUMP-CCW-A"),
    ("MCC-1A2", "XFER-ATS-A"),
    *chain("BUS-AUX13A", "TR-SAF-B", "CB-SAF-B", "BUS-416B"),
    *chain("EDG-B", "CB-EDG-B", "BUS-416B"),
    *chain("BUS-416B", "TR-480-B", "CB-LC-B", "LC-480B"),
    *chain("LC-480B", "CB-MCCB1", "MCC-1B1"),
    *chain("LC-480B", "CB-MCCB2", "MCC-1B2"),
    ("MCC-1B1", "PUMP-AFW-B"),
    ("MCC-1B1", "VLV-MSIV-B"),
    ("MCC-1B2", "PUMP-CCW-B"),
    ("PUMP-AFW-B", "XFER-ATS-A"),
    ("MCC-1B2", "XFER-ATS-A"),
    *chain("BUS-AUX13B", "TR-SAF-C", "CB-SAF-C", "BUS-416C"),
    *chain("EDG-C", "CB-EDG-C", "BUS-416C"),
    *chain("BUS-416C", "CB-TIE-CD", "BUS-416D"),
    *chain("BUS-416C", "TR-480-C", "CB-LC-C", "LC-480C"),
    *chain("LC-480C", "CB-MCCC1", "MCC-1C1"),
    *chain("LC-480C", "CB-MCCC2", "MCC-1C2"),
    ("MCC-1C1", "PUMP-RHR-A"),
    ("MCC-1C2", "FAN-CRHV-A"),
    *chain("MCC-1C2", "HTR-BATRM-A", "XFER-ATS-B"),
    *chain("BUS-AUX13B", "TR-SAF-D", "CB-SAF-D", "BUS-416D"),
    *chain("EDG-D", "CB-EDG-D", "BUS-416D"),
    *chain("BUS-416D", "TR-480-D", "CB-LC-D", "LC-480D"),
    *chain("LC-480D", "CB-MCCD1", "MCC-1D1"),
    *chain("LC-480D", "CB-MCCD2", "MCC-1D2"),
    *chain("MCC-1D1", "PUMP-RHR-B", "XFER-ATS-B"),
    ("MCC-1D2", "FAN-CRHV-B"),
    ("MCC-1D2", "HTR-BATRM-B"),
    *chain("XFER-ATS-A", "CHG-125A", "BAT-125A", "PNL-DC-A"),
    *chain("PNL-DC-A", "INV-UPS-A", "UPS-PNL-A"),
    *chain("XFER-ATS-A", "RECT-48V-A", "BAT-48V-A", "JB-RLY-A"),
    ("JB-RLY-A", "JB-RLY-B"),
    *chain("XFER-ATS-B", "CHG-125B", "BAT-125B", "PNL-DC-B"),
    *chain("PNL-DC-B", "INV-UPS-B", "UPS-PNL-B"),
    *chain("XFER-ATS-B", "RECT-48V-B", "BAT-48V-B", "JB-RLY-B"),
    ("PNL-DC-A", "PNL-DC-B"),
]


CONTROL_CANDIDATES = [
    ("CP-ESFAS-1", "CP-ESFAS-2"),
    *[(src, dst) for src in ["CP-ESFAS-1"] for dst in ["RELAY-K1A", "RELAY-K1B", "RELAY-UV-A", "RELAY-UV-B", "INST-NSSS-A", "INST-NSSS-B"]],
    *[(src, dst) for src in ["CP-ESFAS-2"] for dst in ["RELAY-K2A", "RELAY-K2B", "RELAY-LOOP-C", "RELAY-LOOP-D", "INST-NSSS-A", "INST-NSSS-B"]],
    ("CB-EDG-A", "RELAY-K1A"), ("CB-SAF-A", "RELAY-K1A"),
    ("CB-EDG-B", "RELAY-K1B"), ("CB-SAF-B", "RELAY-K1B"),
    ("CB-EDG-C", "RELAY-K2A"), ("CB-SAF-C", "RELAY-K2A"),
    ("CB-EDG-D", "RELAY-K2B"), ("CB-SAF-D", "RELAY-K2B"),
    ("CB-TIE-AB", "RELAY-LOOP-C"), ("CB-TIE-CD", "RELAY-LOOP-D"),
    ("BUS-416A", "RELAY-UV-A"), ("BUS-416B", "RELAY-UV-A"),
    ("BUS-416C", "RELAY-UV-B"), ("BUS-416D", "RELAY-UV-B"),
    *[("JB-RLY-A", dst) for dst in ["RELAY-K1A", "RELAY-K2A", "RELAY-UV-A", "RELAY-LOOP-C"]],
    *[("JB-RLY-B", dst) for dst in ["RELAY-K1B", "RELAY-K2B", "RELAY-UV-B", "RELAY-LOOP-D"]],
]


def summarize(edges: list[tuple[str, str]]) -> None:
    unique = {tuple(sorted(edge)) for edge in edges}
    deg = Counter()
    for a, b in unique:
        deg[a] += 1
        deg[b] += 1
    print("nodes", len(NODES), "edges", len(unique), "isolated", [n for n in NODES if deg[n] == 0])


if __name__ == "__main__":
    print("solid")
    summarize(SOLID_EDGES)
    print("solid+control")
    summarize(SOLID_EDGES + CONTROL_CANDIDATES)
