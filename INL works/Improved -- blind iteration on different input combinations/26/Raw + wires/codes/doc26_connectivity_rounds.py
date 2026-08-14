from __future__ import annotations

import csv
import json
import shutil
from collections import OrderedDict
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires"
)
RESULTS = BASE / "results"


def edge(a: str, b: str, kind: str = "solid", evidence: str = "") -> dict[str, str]:
    return {"a": a, "b": b, "kind": kind, "evidence": evidence}


def normalize_pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def ordered_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: OrderedDict[tuple[str, str], dict[str, str]] = OrderedDict()
    for item in edges:
        key = normalize_pair(item["a"], item["b"])
        if key in seen:
            raise ValueError(f"duplicate edge: {item['a']} -- {item['b']}")
        seen[key] = item
    return list(seen.values())


BASE_EDGES: list[dict[str, str]] = [
    edge("GEN-301", "TR-UAT-31", "solid", "top source feeder"),
    edge("TR-UAT-31", "CB-4A-IN1", "solid", "UAT feeder breaker"),
    edge("CB-4A-IN1", "BUS-416A", "solid", "breaker lands on BUS-416A"),
    edge("SAT-31A", "CB-4A-ST", "solid", "standby transformer feeder"),
    edge("CB-4A-ST", "BUS-416A", "solid", "breaker lands on BUS-416A"),
    edge("DG-31A", "CB-4A-DG", "solid", "diesel generator feeder"),
    edge("CB-4A-DG", "BUS-416A", "solid", "breaker lands on BUS-416A"),
    edge("BUS-416A", "CB-4AB-TIE", "solid", "4.16 kV tie breaker"),
    edge("CB-4AB-TIE", "BUS-416B", "solid", "4.16 kV tie breaker"),
    edge("SAT-31B", "CB-4B-ST", "solid", "standby transformer feeder"),
    edge("CB-4B-ST", "BUS-416B", "solid", "breaker lands on BUS-416B"),
    edge("DG-31B", "CB-4B-DG", "solid", "diesel generator feeder"),
    edge("CB-4B-DG", "BUS-416B", "solid", "breaker lands on BUS-416B"),
    edge("BUS-416A", "CB-4A01", "solid", "BUS-416A feeder 01"),
    edge("CB-4A01", "TR-480A1", "solid", "feeder to transformer"),
    edge("TR-480A1", "CB-480A-IN", "solid", "transformer secondary breaker"),
    edge("CB-480A-IN", "BUS-480A", "solid", "breaker lands on BUS-480A"),
    edge("BUS-416A", "CB-4A02", "solid", "BUS-416A feeder 02"),
    edge("CB-4A02", "TR-480A2", "solid", "feeder to transformer"),
    edge("TR-480A2", "CB-480A-ALT", "solid", "alternate transformer secondary breaker"),
    edge("CB-480A-ALT", "BUS-480A", "solid", "breaker lands on BUS-480A"),
    edge("BUS-416A", "CB-4A03", "solid", "BUS-416A feeder 03"),
    edge("CB-4A03", "DS-RCP-A", "solid", "RCP feeder disconnect"),
    edge("DS-RCP-A", "MTR-RCP-A", "solid", "RCP motor feeder"),
    edge("MTR-RCP-A", "GND-RCP-A", "solid", "motor ground shown with ground symbol"),
    edge("BUS-416A", "CB-4A04", "solid", "BUS-416A feeder 04"),
    edge("CB-4A04", "DS-SW-A", "solid", "service water feeder disconnect"),
    edge("DS-SW-A", "PUMP-SW31A", "solid", "service water pump feeder"),
    edge("PUMP-SW31A", "GND-SW-A", "solid", "pump ground shown with ground symbol"),
    edge("BUS-416A", "CB-4A05", "solid", "BUS-416A feeder 05"),
    edge("CB-4A05", "DS-AFW-A", "solid", "AFW feeder disconnect"),
    edge("DS-AFW-A", "PUMP-AFW31A", "solid", "AFW pump feeder"),
    edge("BUS-416A", "CB-4A06", "solid", "BUS-416A feeder 06"),
    edge("CB-4A06", "DS-CHW-A", "solid", "CHW feeder disconnect"),
    edge("DS-CHW-A", "MTR-CHWP-A", "solid", "CHW pump motor feeder"),
    edge("BUS-416B", "CB-4B01", "solid", "BUS-416B feeder 01"),
    edge("CB-4B01", "TR-480B1", "solid", "feeder to transformer"),
    edge("TR-480B1", "CB-480B-IN", "solid", "transformer secondary breaker"),
    edge("CB-480B-IN", "BUS-480B", "solid", "breaker lands on BUS-480B"),
    edge("BUS-416B", "CB-4B02", "solid", "BUS-416B feeder 02"),
    edge("CB-4B02", "TR-480B2", "solid", "feeder to transformer"),
    edge("TR-480B2", "CB-480B-ALT", "solid", "alternate transformer secondary breaker"),
    edge("CB-480B-ALT", "BUS-480B", "solid", "breaker lands on BUS-480B"),
    edge("BUS-416B", "CB-4B03", "solid", "BUS-416B feeder 03"),
    edge("CB-4B03", "DS-RCP-B", "solid", "RCP feeder disconnect"),
    edge("DS-RCP-B", "MTR-RCP-B", "solid", "RCP motor feeder"),
    edge("MTR-RCP-B", "GND-RCP-B", "solid", "motor ground shown with ground symbol"),
    edge("BUS-416B", "CB-4B04", "solid", "BUS-416B feeder 04"),
    edge("CB-4B04", "DS-SW-B", "solid", "service water feeder disconnect"),
    edge("DS-SW-B", "PUMP-SW31B", "solid", "service water pump feeder"),
    edge("PUMP-SW31B", "GND-SW-B", "solid", "pump ground shown with ground symbol"),
    edge("BUS-416B", "CB-4B05", "solid", "BUS-416B feeder 05"),
    edge("CB-4B05", "DS-AFW-B", "solid", "AFW feeder disconnect"),
    edge("DS-AFW-B", "PUMP-AFW31B", "solid", "AFW pump feeder"),
    edge("BUS-416B", "CB-4B06", "solid", "BUS-416B feeder 06"),
    edge("CB-4B06", "DS-CHW-B", "solid", "CHW feeder disconnect"),
    edge("DS-CHW-B", "MTR-CHWP-B", "solid", "CHW pump motor feeder"),
    edge("BUS-480A", "CB-480AB-TIE", "solid", "480 V tie breaker"),
    edge("CB-480AB-TIE", "BUS-480B", "solid", "480 V tie breaker"),
    edge("BUS-480A", "CB-480A11", "solid", "480 V feeder"),
    edge("CB-480A11", "MCC-31A1", "solid", "feeder to MCC"),
    edge("BUS-480A", "CB-480A12", "solid", "480 V feeder"),
    edge("CB-480A12", "MCC-31A2", "solid", "feeder to MCC"),
    edge("BUS-480A", "CB-480A13", "solid", "480 V feeder"),
    edge("CB-480A13", "LC-31A3", "solid", "feeder to load center"),
    edge("BUS-480A", "CB-480A14", "solid", "480 V feeder"),
    edge("CB-480A14", "PNL-31A4", "solid", "feeder to panel"),
    edge("BUS-480B", "CB-480B11", "solid", "480 V feeder"),
    edge("CB-480B11", "MCC-31B1", "solid", "feeder to MCC"),
    edge("BUS-480B", "CB-480B12", "solid", "480 V feeder"),
    edge("CB-480B12", "MCC-31B2", "solid", "feeder to MCC"),
    edge("BUS-480B", "CB-480B13", "solid", "480 V feeder"),
    edge("CB-480B13", "LC-31B3", "solid", "feeder to load center"),
    edge("BUS-480B", "CB-480B14", "solid", "480 V feeder"),
    edge("CB-480B14", "PNL-31B4", "solid", "feeder to panel"),
    edge("MCC-31A1", "STR-A1-1", "solid", "starter branch"),
    edge("STR-A1-1", "JB-A1-01", "solid", "branch junction box"),
    edge("JB-A1-01", "PUMP-CVC-A", "solid", "load feeder"),
    edge("MCC-31A1", "STR-A1-2", "solid", "starter branch"),
    edge("STR-A1-2", "JB-A1-02", "solid", "branch junction box"),
    edge("JB-A1-02", "MOV-RHR-731A", "solid", "load feeder"),
    edge("MCC-31A1", "STR-A1-3", "solid", "starter branch"),
    edge("STR-A1-3", "JB-A1-03", "solid", "branch junction box"),
    edge("JB-A1-03", "FAN-CRD-A", "solid", "load feeder"),
    edge("MCC-31A2", "STR-A2-1", "solid", "starter branch"),
    edge("STR-A2-1", "JB-A2-01", "solid", "branch junction box"),
    edge("JB-A2-01", "PUMP-CCW-A", "solid", "load feeder"),
    edge("MCC-31A2", "STR-A2-2", "solid", "starter branch"),
    edge("STR-A2-2", "JB-A2-02", "solid", "branch junction box"),
    edge("JB-A2-02", "HTR-BORIC-A", "solid", "load feeder"),
    edge("MCC-31A2", "STR-A2-3", "solid", "starter branch"),
    edge("STR-A2-3", "JB-A2-03", "solid", "branch junction box"),
    edge("JB-A2-03", "MOV-CHG-121A", "solid", "load feeder"),
    edge("LC-31A3", "STR-A3-1", "solid", "starter branch"),
    edge("STR-A3-1", "JB-A3-01", "solid", "branch junction box"),
    edge("JB-A3-01", "MTR-SUMP-A", "solid", "load feeder"),
    edge("LC-31A3", "STR-A3-2", "solid", "starter branch"),
    edge("STR-A3-2", "JB-A3-02", "solid", "branch junction box"),
    edge("JB-A3-02", "PUMP-LUBE-A", "solid", "load feeder"),
    edge("LC-31A3", "STR-A3-3", "solid", "starter branch"),
    edge("STR-A3-3", "JB-A3-03", "solid", "branch junction box"),
    edge("JB-A3-03", "MOV-SI-902A", "solid", "load feeder"),
    edge("PNL-31A4", "STR-A4-1", "solid", "starter branch"),
    edge("STR-A4-1", "JB-A4-01", "solid", "branch junction box"),
    edge("JB-A4-01", "FAN-CONT-A", "solid", "load feeder"),
    edge("PNL-31A4", "STR-A4-2", "solid", "starter branch"),
    edge("STR-A4-2", "JB-A4-02", "solid", "branch junction box"),
    edge("JB-A4-02", "PUMP-SAMPLE-A", "solid", "load feeder"),
    edge("PNL-31A4", "STR-A4-3", "solid", "starter branch"),
    edge("STR-A4-3", "JB-A4-03", "solid", "branch junction box"),
    edge("JB-A4-03", "MOV-VENT-406A", "solid", "load feeder"),
    edge("MCC-31B1", "STR-B1-1", "solid", "starter branch"),
    edge("STR-B1-1", "JB-B1-01", "solid", "branch junction box"),
    edge("JB-B1-01", "PUMP-CVC-B", "solid", "load feeder"),
    edge("MCC-31B1", "STR-B1-2", "solid", "starter branch"),
    edge("STR-B1-2", "JB-B1-02", "solid", "branch junction box"),
    edge("JB-B1-02", "MOV-RHR-731B", "solid", "load feeder"),
    edge("MCC-31B1", "STR-B1-3", "solid", "starter branch"),
    edge("STR-B1-3", "JB-B1-03", "solid", "branch junction box"),
    edge("JB-B1-03", "FAN-CRD-B", "solid", "load feeder"),
    edge("MCC-31B2", "STR-B2-1", "solid", "starter branch"),
    edge("STR-B2-1", "JB-B2-01", "solid", "branch junction box"),
    edge("JB-B2-01", "PUMP-CCW-B", "solid", "load feeder"),
    edge("MCC-31B2", "STR-B2-2", "solid", "starter branch"),
    edge("STR-B2-2", "JB-B2-02", "solid", "branch junction box"),
    edge("JB-B2-02", "HTR-BORIC-B", "solid", "load feeder"),
    edge("MCC-31B2", "STR-B2-3", "solid", "starter branch"),
    edge("STR-B2-3", "JB-B2-03", "solid", "branch junction box"),
    edge("JB-B2-03", "MOV-CHG-121B", "solid", "load feeder"),
    edge("LC-31B3", "STR-B3-1", "solid", "starter branch"),
    edge("STR-B3-1", "JB-B3-01", "solid", "branch junction box"),
    edge("JB-B3-01", "MTR-SUMP-B", "solid", "load feeder"),
    edge("LC-31B3", "STR-B3-2", "solid", "starter branch"),
    edge("STR-B3-2", "JB-B3-02", "solid", "branch junction box"),
    edge("JB-B3-02", "PUMP-LUBE-B", "solid", "load feeder"),
    edge("LC-31B3", "STR-B3-3", "solid", "starter branch"),
    edge("STR-B3-3", "JB-B3-03", "solid", "branch junction box"),
    edge("JB-B3-03", "MOV-SI-902B", "solid", "load feeder"),
    edge("PNL-31B4", "STR-B4-1", "solid", "starter branch"),
    edge("STR-B4-1", "JB-B4-01", "solid", "branch junction box"),
    edge("JB-B4-01", "FAN-CONT-B", "solid", "load feeder"),
    edge("PNL-31B4", "STR-B4-2", "solid", "starter branch"),
    edge("STR-B4-2", "JB-B4-02", "solid", "branch junction box"),
    edge("JB-B4-02", "PUMP-SAMPLE-B", "solid", "load feeder"),
    edge("PNL-31B4", "STR-B4-3", "solid", "starter branch"),
    edge("STR-B4-3", "JB-B4-03", "solid", "branch junction box"),
    edge("JB-B4-03", "MOV-VENT-406B", "solid", "load feeder"),
    edge("MCC-31A1", "GND-MCC-A1", "solid", "MCC ground symbol"),
    edge("MCC-31A2", "GND-MCC-A2", "solid", "MCC ground symbol"),
    edge("MCC-31B1", "GND-MCC-B1", "solid", "MCC ground symbol"),
    edge("MCC-31B2", "GND-MCC-B2", "solid", "MCC ground symbol"),
    edge("BAT-31A", "DS-BAT-A", "solid", "battery disconnect"),
    edge("DS-BAT-A", "BUS-125DCA", "solid", "disconnect lands on DC bus"),
    edge("CHG-31A", "CB-CHG-A", "solid", "charger breaker"),
    edge("CB-CHG-A", "BUS-125DCA", "solid", "breaker lands on DC bus"),
    edge("BUS-125DCA", "PNL-DC-A", "solid", "DC panel tap"),
    edge("CB-INV-A", "BUS-125DCA", "solid", "inverter input tap/breaker at DC bus"),
    edge("BUS-125DCA", "INV-31A", "solid", "Jennifer R1 corrected inverter feed path"),
    edge("INV-31A", "BUS-INV-A", "solid", "inverter output bus"),
    edge("BUS-INV-A", "PNL-AC-A", "solid", "AC panel feed"),
    edge("PNL-AC-A", "BUS-120N-A", "solid", "120 V vital bus"),
    edge("BUS-INV-A", "RPS-PNL-A", "solid", "RPS panel feed"),
    edge("RPS-PNL-A", "BUS-120N-A", "solid", "120 V vital bus"),
    edge("BUS-125DCA", "CB-DCAB-TIE", "solid", "125 V DC tie breaker"),
    edge("CB-DCAB-TIE", "BUS-125DCB", "solid", "125 V DC tie breaker"),
    edge("BAT-31B", "DS-BAT-B", "solid", "battery disconnect"),
    edge("DS-BAT-B", "BUS-125DCB", "solid", "disconnect lands on DC bus"),
    edge("CHG-31B", "CB-CHG-B", "solid", "charger breaker"),
    edge("CB-CHG-B", "BUS-125DCB", "solid", "breaker lands on DC bus"),
    edge("BUS-125DCB", "PNL-DC-B", "solid", "DC panel tap"),
    edge("CB-INV-B", "BUS-125DCB", "solid", "inverter input tap/breaker at DC bus"),
    edge("BUS-125DCB", "INV-31B", "solid", "Jennifer R1 corrected inverter feed path"),
    edge("INV-31B", "BUS-INV-B", "solid", "inverter output bus"),
    edge("BUS-INV-B", "PNL-AC-B", "solid", "AC panel feed"),
    edge("PNL-AC-B", "BUS-120N-B", "solid", "120 V vital bus"),
    edge("BUS-INV-B", "RPS-PNL-B", "solid", "RPS panel feed"),
    edge("RPS-PNL-B", "BUS-120N-B", "solid", "120 V vital bus"),
    edge("BUS-120N-A", "RELAY-K7A1", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7A1", "TB-RPS-A1", "control_power", "relay terminal block path"),
    edge("TB-RPS-A1", "PT-31A1", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-A", "RELAY-K7A2", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7A2", "TB-RPS-A2", "control_power", "relay terminal block path"),
    edge("TB-RPS-A2", "PT-31A2", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-A", "RELAY-K7A3", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7A3", "TB-RPS-A3", "control_power", "relay terminal block path"),
    edge("TB-RPS-A3", "PT-31A3", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-A", "RELAY-K7A4", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7A4", "TB-RPS-A4", "control_power", "relay terminal block path"),
    edge("TB-RPS-A4", "PT-31A4", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-B", "RELAY-K7B1", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7B1", "TB-RPS-B1", "control_power", "relay terminal block path"),
    edge("TB-RPS-B1", "PT-31B1", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-B", "RELAY-K7B2", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7B2", "TB-RPS-B2", "control_power", "relay terminal block path"),
    edge("TB-RPS-B2", "PT-31B2", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-B", "RELAY-K7B3", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7B3", "TB-RPS-B3", "control_power", "relay terminal block path"),
    edge("TB-RPS-B3", "PT-31B3", "dotted_instrument", "instrument signal circuit"),
    edge("BUS-120N-B", "RELAY-K7B4", "control_power", "relay feeder from vital bus"),
    edge("RELAY-K7B4", "TB-RPS-B4", "control_power", "relay terminal block path"),
    edge("TB-RPS-B4", "PT-31B4", "dotted_instrument", "instrument signal circuit"),
    edge("RPS-PNL-A", "TB-UPS-A", "dashed_control", "Jennifer R1: dashed UPS/RPS control path"),
    edge("RPS-PNL-B", "TB-UPS-B", "dashed_control", "Jennifer R1: dashed UPS/RPS control path"),
]


ROUND_DELTAS = {
    "diego_round_1": {
        "remove": [
            ("BUS-125DCA", "INV-31A"),
            ("BUS-125DCB", "INV-31B"),
        ],
        "add": [
            edge("CB-INV-A", "INV-31A", "solid", "Diego R1 serial inverter interpretation"),
            edge("CB-INV-B", "INV-31B", "solid", "Diego R1 serial inverter interpretation"),
        ],
        "notes": [
            "High-recall matrix excluded unresolved dashed RCP/MOV candidates pending review.",
            "Inverter path was later corrected by Jennifer.",
        ],
    },
    "jennifer_round_1": {
        "remove": [],
        "add": [],
        "notes": [
            "Precision review accepted the main graph.",
            "Corrected inverter path to put BUS-125DC(A/B) between CB-INV and INV-31(A/B).",
            "Kept RCP interlocks and MOV dashed control trunks unresolved.",
            "Reclassified RPS-PNL(A/B)--TB-UPS(A/B) as dashed control rather than instrument.",
        ],
    },
    "diego_round_2": {
        "remove": [],
        "add": [
            edge(
                "STR-A3-3",
                "BUS-120N-A",
                "dashed_control",
                "Diego R2: dashed lead exits STR-A3-3 near MOV-SI-902A and routes to BUS-120N-A tap area",
            ),
            edge(
                "STR-B3-3",
                "BUS-120N-B",
                "dashed_control",
                "Diego R2: dashed lead exits STR-B3-3 near MOV-SI-902B and routes to BUS-120N-B tap area",
            ),
        ],
        "notes": [
            "RCP dashed breaker-side contacts kept uncertain/rejected because no labeled lower endpoint is visible.",
            "High-recall R2 accepted only the two STR-A3/B3 to BUS-120N dashed/protection routes.",
        ],
    },
    "jennifer_round_2_final": {
        "remove": [],
        "add": [
            edge(
                "STR-A3-3",
                "BUS-120N-A",
                "dashed_control",
                "Jennifer R2: accepted; no extra bus-crossing edges added without dots",
            ),
            edge(
                "STR-B3-3",
                "BUS-120N-B",
                "dashed_control",
                "Jennifer R2: accepted; no extra bus-crossing edges added without dots",
            ),
        ],
        "notes": [
            "Final evidence-saturated matrix.",
            "Accepted edge count is 205; title block states 209, but four additional connections were not visually supported enough to include.",
            "RCP dashed endpoints remain uncertain/rejected.",
        ],
    },
}


UNCERTAIN_CANDIDATES = [
    {
        "candidate": "CB-4A03 -- GND-RCP-A or CB-4A03 -- MTR-RCP-A",
        "reason": "dashed interlock line appears near RCP A branch, but endpoint dot/landing was unresolved in R1",
    },
    {
        "candidate": "CB-4B03 -- GND-RCP-B or CB-4B03 -- MTR-RCP-B",
        "reason": "dashed interlock line appears near RCP B branch, but endpoint dot/landing was unresolved in R1",
    },
    {
        "candidate": "MOV A train dashed control trunks",
        "reason": "dashed paths cross/approach MOV branches and lower DC/UPS area; endpoints require focused review",
    },
    {
        "candidate": "MOV B train dashed control trunks",
        "reason": "dashed paths cross/approach MOV branches and lower DC/UPS area; endpoints require focused review",
    },
    {
        "candidate": "Title-block 209 minus final visual 205 connection gap",
        "reason": "no further visually supported labeled endpoint pairs were found in final review",
    },
]


ALIASES_NOT_NODES = [
    "480-A-11",
    "480-B-13",
    "DC-A-INV",
    "DC-B-INV",
    "120-A-N",
    "120-B-N",
]


def apply_delta(base: list[dict[str, str]], delta: dict) -> list[dict[str, str]]:
    remove = {normalize_pair(a, b) for a, b in delta.get("remove", [])}
    result = [item for item in base if normalize_pair(item["a"], item["b"]) not in remove]
    result.extend(delta.get("add", []))
    return ordered_edges(result)


def nodes_for(edges: list[dict[str, str]]) -> list[str]:
    seen: OrderedDict[str, None] = OrderedDict()
    for item in edges:
        seen.setdefault(item["a"], None)
        seen.setdefault(item["b"], None)
    return list(seen)


def write_edgelist(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["a", "b", "kind", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        a = idx[item["a"]]
        b = idx[item["b"]]
        if a == b:
            matrix[a][b] = 1
        else:
            matrix[a][b] = 1
            matrix[b][a] = 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    base = ordered_edges(BASE_EDGES)

    metadata = {
        "document": 26,
        "source_folder": str(BASE),
        "raw_file": "raw -- synthetic_npp_electrical_schematic_v3(1).png",
        "wire_aids": ["wires_mask.png", "wires_mask_overlay.png"],
        "warning": "GT/GT-derived resources were not used.",
        "off_the_shelf_ocr": "not used",
        "aliases_not_nodes": ALIASES_NOT_NODES,
        "uncertain_candidates_after_round_1": UNCERTAIN_CANDIDATES,
        "rounds": {},
    }

    for round_name, delta in ROUND_DELTAS.items():
        edges = apply_delta(base, delta)
        nodes = nodes_for(edges)
        write_edgelist(RESULTS / f"{round_name}_edgelist.csv", edges)
        write_matrix(RESULTS / f"{round_name}_connectivity_matrix.csv", nodes, edges)
        write_nodes(RESULTS / f"{round_name}_nodes.csv", nodes)
        if round_name == "jennifer_round_2_final":
            shutil.copyfile(
                RESULTS / f"{round_name}_edgelist.csv",
                RESULTS / "final_edgelist.csv",
            )
            shutil.copyfile(
                RESULTS / f"{round_name}_connectivity_matrix.csv",
                RESULTS / "final_connectivity_matrix.csv",
            )
            shutil.copyfile(
                RESULTS / f"{round_name}_nodes.csv",
                RESULTS / "final_nodes.csv",
            )
        metadata["rounds"][round_name] = {
            "nodes": len(nodes),
            "edges": len(edges),
            "matrix_csv": f"{round_name}_connectivity_matrix.csv",
            "edgelist_csv": f"{round_name}_edgelist.csv",
            "nodes_csv": f"{round_name}_nodes.csv",
            "notes": delta.get("notes", []),
        }

    with (RESULTS / "doc26_round_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(json.dumps(metadata["rounds"], indent=2))


if __name__ == "__main__":
    main()
