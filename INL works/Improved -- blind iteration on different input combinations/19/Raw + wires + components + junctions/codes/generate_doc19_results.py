from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components + junctions")
RESULTS = BASE / "results"


def pair(a: str, b: str, evidence: str = "") -> tuple[str, str, str]:
    return (a, b, evidence)


CORE_DIEGO = [
    pair("OFFSITE GRID-1", "DS-101", "solid vertical"),
    pair("DS-101", "CB-101", "solid vertical; 4x crop confirms CB-101"),
    pair("CB-101", "TR-101", "solid vertical; 4x crop confirms CB-101"),
    pair("TR-101", "BUS-4160-A", "solid tap to 4160 bus"),
    pair("DG-1", "CB-DG1", "solid vertical"),
    pair("CB-DG1", "BUS-4160-A", "solid tap to 4160 bus"),
    pair("BUS-4160-A", "PT-4160A", "instrument tap"),
    pair("BUS-4160-A", "CB-201", "solid branch"),
    pair("CB-201", "TR-480-A", "solid vertical"),
    pair("TR-480-A", "CB-480-A", "solid vertical"),
    pair("CB-480-A", "BUS-480-A", "solid tap"),
    pair("BUS-4160-A", "CB-TIE-4160", "tie breaker left side"),
    pair("CB-TIE-4160", "BUS-4160-B", "tie breaker right side"),
    pair("BUS-480-A", "CB-TIE-480", "tie breaker left side"),
    pair("CB-TIE-480", "BUS-480-B", "tie breaker right side"),
    pair("OFFSITE GRID-2", "DS-102", "solid vertical"),
    pair("DS-102", "CB-102", "solid vertical; 4x crop confirms CB-102"),
    pair("CB-102", "TR-102", "solid vertical; 4x crop confirms CB-102"),
    pair("TR-102", "BUS-4160-B", "solid tap to 4160 bus"),
    pair("DG-2", "CB-DG2", "solid vertical"),
    pair("CB-DG2", "BUS-4160-B", "solid tap to 4160 bus"),
    pair("BUS-4160-B", "PT-4160B", "instrument tap"),
    pair("BUS-4160-B", "CB-202", "solid branch"),
    pair("CB-202", "TR-480-B", "solid vertical"),
    pair("TR-480-B", "CB-480-B", "solid vertical"),
    pair("CB-480-B", "BUS-480-B", "solid tap"),
]

CORE_JENNIFER_R1 = [
    pair("OFFSITE GRID-1", "DS-101", "solid vertical"),
    pair("DS-101", "CR-101", "Jennifer round 1 read this as CR-101; corrected in round 2"),
    pair("CR-101", "TR-101", "solid vertical"),
    pair("TR-101", "BUS-4160-A", "solid tap to 4160 bus"),
    pair("DG-1", "CB-DG1", "solid vertical"),
    pair("CB-DG1", "BUS-4160-A", "solid tap to 4160 bus"),
    pair("BUS-4160-A", "PT-4160A", "instrument tap"),
    pair("BUS-4160-A", "CB-201", "solid branch"),
    pair("CB-201", "TR-480-A", "solid vertical"),
    pair("TR-480-A", "CB-480-A", "solid vertical"),
    pair("CB-480-A", "BUS-480-A", "solid tap"),
    pair("BUS-4160-A", "CB-TIE-4160", "tie breaker left side"),
    pair("CB-TIE-4160", "BUS-4160-B", "tie breaker right side"),
    pair("BUS-480-A", "CB-TIE-480", "tie breaker left side"),
    pair("CB-TIE-480", "BUS-480-B", "tie breaker right side"),
    pair("OFFSITE GRID-2", "DS-102", "solid vertical"),
    pair("DS-102", "CR-102", "Jennifer round 1 read this as CR-102; corrected in round 2"),
    pair("CR-102", "TR-102", "solid vertical"),
    pair("TR-102", "BUS-4160-B", "solid tap to 4160 bus"),
    pair("DG-2", "CB-DG2", "solid vertical"),
    pair("CB-DG2", "BUS-4160-B", "solid tap to 4160 bus"),
    pair("BUS-4160-B", "PT-4160B", "instrument tap"),
    pair("BUS-4160-B", "CB-202", "solid branch"),
    pair("CB-202", "TR-480-B", "solid vertical"),
    pair("TR-480-B", "CB-480-B", "solid vertical"),
    pair("CB-480-B", "BUS-480-B", "solid tap"),
]

CORE_FINAL = CORE_DIEGO

NORMAL_GROUPS = [
    ("BUS-480-A", "201", "PUMP-P201"),
    ("BUS-480-A", "203", "PUMP-P203"),
    ("BUS-480-A", "301", "PUMP-P301"),
    ("BUS-480-A", "401", "PUMP-P401"),
    ("BUS-480-A", "501", "MTR-F501"),
    ("BUS-480-B", "202", "PUMP-P202"),
    ("BUS-480-B", "204", "PUMP-P204"),
    ("BUS-480-B", "302", "PUMP-P302"),
    ("BUS-480-B", "402", "PUMP-P402"),
    ("BUS-480-B", "502", "MTR-F502"),
]


def normal_edges() -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for bus, n, load in NORMAL_GROUPS:
        edges.extend(
            [
                pair(bus, f"CB-F{n}", "480V bus feeder drop"),
                pair(f"CB-F{n}", f"DS-F{n}", "solid vertical"),
                pair(f"DS-F{n}", f"CPT-{n}", "solid vertical"),
                pair(f"CPT-{n}", f"MCC-{n}", "solid vertical"),
                pair(f"MCC-{n}", f"CB-L{n}", "solid vertical"),
                pair(f"CB-L{n}", f"RELAY-K{n}", "solid vertical"),
                pair(f"RELAY-K{n}", load, "solid vertical to load"),
                pair(f"CB-F{n}", f"RELAY-PR{n}", "dashed protection/control"),
                pair(f"MCC-{n}", f"RELAY-A{n}", "dashed control"),
                pair(load, f"INST-{n}", "dashed indication"),
                pair(f"INST-{n}", f"JB-{n}", "dashed vertical"),
                pair(f"JB-{n}", f"TB-{n}", "dashed vertical"),
                pair(f"TB-{n}", f"LCS-{n}", "dashed control"),
            ]
        )
    return edges


SPECIAL_DIEGO = [
    pair("BUS-480-A", "CB-F601", "480V bus feeder drop"),
    pair("CB-F601", "DS-F601", "solid vertical"),
    pair("DS-F601", "CPT-601", "solid vertical"),
    pair("CPT-601", "MCC-601", "solid vertical"),
    pair("MCC-601", "CB-L601", "solid vertical"),
    pair("CB-L601", "RELAY-K601", "solid vertical"),
    pair("RELAY-K601", "VALVE-MOV601", "solid vertical to valve"),
    pair("CB-F601", "RELAY-PR601", "dashed protection/control"),
    pair("MCC-601", "RELAY-A601", "dashed control"),
    pair("VALVE-MOV601", "INST-601", "dashed indication"),
    pair("VALVE-MOV601", "LS-MOV601", "Diego high-recall uncertain edge; corrected later"),
    pair("LS-MOV601", "JB-601", "Diego high-recall uncertain edge; corrected later"),
    pair("JB-601", "TB-601", "dashed vertical"),
    pair("TB-601", "LCS-601", "dashed control"),
    pair("BUS-480-B", "CB-F701", "480V bus feeder drop"),
    pair("CB-F701", "DS-F701", "solid vertical"),
    pair("DS-F701", "CPT-701", "solid vertical"),
    pair("CPT-701", "MCC-701", "solid vertical"),
    pair("MCC-701", "CB-L701", "solid vertical"),
    pair("CB-L701", "RELAY-K701", "solid vertical"),
    pair("RELAY-K701", "INST-RPS701", "solid vertical to instrument"),
    pair("CB-F701", "RELAY-PR701", "dashed protection/control"),
    pair("MCC-701", "RELAY-A701", "dashed control"),
    pair("INST-RPS701", "INST-701", "dashed indication"),
    pair("INST-RPS701", "JB-701", "Diego high-recall edge; corrected later"),
    pair("JB-701", "TB-701", "dashed vertical"),
    pair("TB-701", "LCS-701", "dashed control"),
]

SPECIAL_FINAL = [
    pair("BUS-480-A", "CB-F601", "480V bus feeder drop"),
    pair("CB-F601", "DS-F601", "solid vertical"),
    pair("DS-F601", "CPT-601", "solid vertical"),
    pair("CPT-601", "MCC-601", "solid vertical"),
    pair("MCC-601", "CB-L601", "solid vertical"),
    pair("CB-L601", "RELAY-K601", "solid vertical"),
    pair("RELAY-K601", "VALVE-MOV601", "solid vertical to valve"),
    pair("CB-F601", "RELAY-PR601", "dashed protection/control"),
    pair("MCC-601", "RELAY-A601", "dashed control"),
    pair("VALVE-MOV601", "INST-601", "dashed indication"),
    pair("INST-601", "[LS-MOV601]", "dashed branch continues from instrument lead"),
    pair("[LS-MOV601]", "JB-601", "dashed vertical"),
    pair("JB-601", "TB-601", "dashed vertical"),
    pair("TB-601", "LCS-601", "dashed control"),
    pair("BUS-480-B", "CB-F701", "480V bus feeder drop"),
    pair("CB-F701", "DS-F701", "solid vertical"),
    pair("DS-F701", "CPT-701", "solid vertical"),
    pair("CPT-701", "MCC-701", "solid vertical"),
    pair("MCC-701", "CB-L701", "solid vertical"),
    pair("CB-L701", "RELAY-K701", "solid vertical"),
    pair("RELAY-K701", "INST-RPS701", "solid vertical to instrument"),
    pair("CB-F701", "RELAY-PR701", "dashed protection/control"),
    pair("MCC-701", "RELAY-A701", "dashed control"),
    pair("INST-RPS701", "INST-701", "dashed horizontal indication"),
    pair("INST-701", "JB-701", "dashed vertical"),
    pair("JB-701", "TB-701", "dashed vertical"),
    pair("TB-701", "LCS-701", "dashed control"),
]

CONTROL_FINAL = [
    pair("BUS-480-A", "CB-301", "routed control-power source from 480V bus"),
    pair("CB-301", "TR-120-A", "solid vertical"),
    pair("TR-120-A", "BUS-120AC-A", "solid tap"),
    pair("BUS-120AC-A", "JB-MAIN", "dashed vertical branch"),
    pair("BUS-480-A", "CHGR-125A", "routed charger feed from 480V bus"),
    pair("CHGR-125A", "BAT-125A", "solid vertical"),
    pair("BAT-125A", "BUS-125DC-A", "solid tap"),
    pair("BUS-125DC-A", "INV-120A", "solid tap"),
    pair("INV-120A", "PN-RPS-A", "dashed output"),
    pair("BUS-480-B", "CB-302", "routed control-power source from 480V bus"),
    pair("CB-302", "TR-120-B", "solid vertical"),
    pair("TR-120-B", "BUS-120AC-B", "solid tap"),
    pair("BUS-480-B", "CHGR-125B", "routed charger feed from 480V bus"),
    pair("CHGR-125B", "BAT-125B", "solid vertical"),
    pair("BAT-125B", "BUS-125DC-B", "solid tap"),
    pair("BUS-125DC-B", "INV-120B", "solid tap"),
    pair("INV-120B", "PN-RPS-B", "dashed output"),
]

CONTROL_DIEGO = CONTROL_FINAL.copy()


def node_order(edges: list[tuple[str, str, str]]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for a, b, _ in edges:
        for name in (a, b):
            if name not in seen:
                seen.add(name)
                ordered.append(name)
    return ordered


def write_edges(path: Path, edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "value", "evidence"])
        for a, b, evidence in edges:
            writer.writerow([a, b, 1, evidence])


def write_sparse(path: Path, edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row_node", "column_node", "value"])
        for a, b, _ in edges:
            writer.writerow([a, b, 1])


def write_matrix(path: Path, edges: list[tuple[str, str, str]]) -> None:
    nodes = node_order(edges)
    adjacency = {tuple(sorted((a, b))) for a, b, _ in edges if a != b}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for r in nodes:
            row = [r]
            for c in nodes:
                row.append(0 if r == c else int(tuple(sorted((r, c))) in adjacency))
            writer.writerow(row)


def write_nodes(path: Path, edges: list[tuple[str, str, str]]) -> None:
    path.write_text("\n".join(node_order(edges)) + "\n", encoding="utf-8")


def write_manifest(path: Path, rounds: dict[str, list[tuple[str, str, str]]]) -> None:
    manifest = {
        name: {
            "node_count": len(node_order(edges)),
            "edge_count": len(edges),
            "matrix_file": f"{name}_matrix.csv",
            "sparse_file": f"{name}_sparse.csv",
            "edges_file": f"{name}_edges.csv",
        }
        for name, edges in rounds.items()
    }
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    diego_round1 = CORE_DIEGO + normal_edges() + SPECIAL_DIEGO + CONTROL_DIEGO
    jennifer_round1 = CORE_JENNIFER_R1 + normal_edges() + SPECIAL_FINAL + CONTROL_FINAL
    final_edges = CORE_FINAL + normal_edges() + SPECIAL_FINAL + CONTROL_FINAL
    rounds = {
        "round_01_diego": diego_round1,
        "round_01_jennifer": jennifer_round1,
        "round_02_diego": final_edges,
        "round_02_jennifer": final_edges,
        "final": final_edges,
    }
    for name, edges in rounds.items():
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_sparse(RESULTS / f"{name}_sparse.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", edges)
        write_nodes(RESULTS / f"{name}_nodes.txt", edges)
    write_manifest(RESULTS / "round_manifest.json", rounds)


if __name__ == "__main__":
    main()
