from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"


SHARED_NODES = [
    "GEN-101",
    "CB-GEN-101",
    "TR-GSU-1",
    "BUS-SWY-1",
    "CB-SWY-TIE",
    "BUS-SWY-2",
    "GEN-102",
    "CB-GEN-102",
    "TR-GSU-2",
    "TR-UAT-1",
    "TR-SAT-1",
    "TR-UAT-2",
    "TR-SAT-2",
    "BUS-NSS-1",
    "BUS-NSS-2",
    "DG-1A",
    "DG-1B",
    "DG-1C",
    "DG-1D",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "SEQ-1AB",
    "RPS-AC-1",
    "CB-TIE-CD",
    "DS-TIE-CD",
    "SEQ-2CD",
    "RPS-AC-2",
]


DIVISIONS = {
    "A": {
        "nss": "BUS-NSS-1",
        "tie_group": "AB",
        "normal_side": "left",
        "loads": ["PMP-SI-A1", "PMP-CS-A2", "MOV-A03", "MTR-A04", "INST-A05", "PMP-SW-A6"],
    },
    "B": {
        "nss": "BUS-NSS-1",
        "tie_group": "AB",
        "normal_side": "right",
        "loads": ["PMP-SI-B1", "PMP-CS-B2", "MOV-B03", "MTR-B04", "INST-B05", "PMP-SW-B6"],
    },
    "C": {
        "nss": "BUS-NSS-2",
        "tie_group": "CD",
        "normal_side": "left",
        "loads": ["PMP-SI-C1", "PMP-CS-C2", "MOV-C03", "MTR-C04", "INST-C05", "PMP-SW-C6"],
    },
    "D": {
        "nss": "BUS-NSS-2",
        "tie_group": "CD",
        "normal_side": "right",
        "loads": ["PMP-SI-D1", "PMP-CS-D2", "MOV-D03", "MTR-D04", "INST-D05", "PMP-SW-D6"],
    },
}


ROUND_META = {
    "round01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "summary": "Accepted all visually landed power, DC, ground, MCC relay, and local tie-control edges; kept DG-to-NSS and cross-side tie-control edges uncertain.",
    },
    "round01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "summary": "Accepted Diego's edge set unchanged; confirmed uncertain DG-to-NSS and cross-side SEQ/RPS cases should not be promoted.",
    },
    "round02_diego": {
        "agent": "Diego",
        "role": "high-recall saturation review",
        "summary": "Rechecked Jennifer's unchanged set and agreed the extraction was saturated.",
    },
    "round02_jennifer": {
        "agent": "Jennifer",
        "role": "precision final signoff",
        "summary": "Final signoff: accepted edge set unchanged and remaining ambiguous cases excluded.",
    },
}


UNCERTAIN = [
    "DG-1A,BUS-NSS-1,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-A feeder is the clean landed source edge",
    "DG-1B,BUS-NSS-1,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-B feeder is the clean landed source edge",
    "DG-1C,BUS-NSS-2,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-C feeder is the clean landed source edge",
    "DG-1D,BUS-NSS-2,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-D feeder is the clean landed source edge",
    "Cross-side SEQ/RPS candidates - possible only through shared dashed nets, not direct clean landings",
]


def division_nodes(letter: str) -> list[str]:
    return [
        f"CB-NF-{letter}",
        f"CB-DG-{letter}",
        f"BUS-416{letter}",
        f"CB-TX-{letter}",
        f"TR-480{letter}",
        f"BUS-480{letter}",
        f"MCC-1{letter}",
        *[f"CB-{letter}{i:02d}" for i in range(1, 7)],
        f"DS-{letter}01",
        f"FU-{letter}02",
        f"DS-{letter}03",
        f"FU-{letter}04",
        f"DS-{letter}05",
        f"FU-{letter}06",
        *[f"RLY-{letter}{i:02d}" for i in range(1, 7)],
        *DIVISIONS[letter]["loads"],
        f"BAT-125{letter}",
        f"CHG-1{letter}",
        f"BUS-DC-{letter}",
        f"INV-1{letter}",
        f"CP-1{letter}",
        f"TB-1{letter}",
        f"JB-1{letter}",
        f"GND-{letter}",
    ]


def build_nodes() -> list[str]:
    nodes = [*SHARED_NODES]
    for letter in "ABCD":
        nodes.extend(division_nodes(letter))
    return nodes


def source_edges() -> list[tuple[str, str, str]]:
    return [
        ("GEN-101", "CB-GEN-101", "P"),
        ("CB-GEN-101", "TR-GSU-1", "P"),
        ("TR-GSU-1", "BUS-SWY-1", "P"),
        ("BUS-SWY-1", "CB-SWY-TIE", "P"),
        ("CB-SWY-TIE", "BUS-SWY-2", "P"),
        ("GEN-102", "CB-GEN-102", "P"),
        ("CB-GEN-102", "TR-GSU-2", "P"),
        ("TR-GSU-2", "BUS-SWY-2", "P"),
        ("BUS-SWY-1", "TR-UAT-1", "P"),
        ("TR-UAT-1", "BUS-NSS-1", "P"),
        ("BUS-SWY-1", "TR-SAT-1", "P"),
        ("TR-SAT-1", "BUS-NSS-1", "P"),
        ("BUS-SWY-2", "TR-UAT-2", "P"),
        ("TR-UAT-2", "BUS-NSS-2", "P"),
        ("BUS-SWY-2", "TR-SAT-2", "P"),
        ("TR-SAT-2", "BUS-NSS-2", "P"),
        ("BUS-416A", "CB-TIE-AB", "P"),
        ("CB-TIE-AB", "DS-TIE-AB", "P"),
        ("DS-TIE-AB", "BUS-416B", "P"),
        ("BUS-416C", "CB-TIE-CD", "P"),
        ("CB-TIE-CD", "DS-TIE-CD", "P"),
        ("DS-TIE-CD", "BUS-416D", "P"),
    ]


def division_edges(letter: str) -> list[tuple[str, str, str]]:
    info = DIVISIONS[letter]
    loads = info["loads"]
    branch_devices = [f"DS-{letter}01", f"FU-{letter}02", f"DS-{letter}03", f"FU-{letter}04", f"DS-{letter}05", f"FU-{letter}06"]
    edges = [
        (info["nss"], f"CB-NF-{letter}", "P"),
        (f"CB-NF-{letter}", f"BUS-416{letter}", "P"),
        (f"DG-1{letter}", f"CB-DG-{letter}", "P"),
        (f"CB-DG-{letter}", f"BUS-416{letter}", "P"),
        (f"BUS-416{letter}", f"CB-TX-{letter}", "P"),
        (f"CB-TX-{letter}", f"TR-480{letter}", "P"),
        (f"TR-480{letter}", f"BUS-480{letter}", "P"),
        (f"BUS-480{letter}", f"MCC-1{letter}", "P"),
        (f"CB-NF-{letter}", f"CB-DG-{letter}", "D"),
    ]

    if info["tie_group"] == "AB":
        seq = "SEQ-1AB"
        rps = "RPS-AC-1"
    else:
        seq = "SEQ-2CD"
        rps = "RPS-AC-2"

    direct = f"CB-DG-{letter}" if info["normal_side"] == "left" else f"CB-NF-{letter}"
    edges.extend([(direct, seq, "D"), (direct, rps, "D")])

    for idx, (device, load) in enumerate(zip(branch_devices, loads), start=1):
        cb = f"CB-{letter}{idx:02d}"
        relay = f"RLY-{letter}{idx:02d}"
        edges.extend(
            [
                (f"MCC-1{letter}", cb, "P"),
                (cb, device, "P"),
                (device, load, "P"),
                (cb, relay, "SIG"),
            ]
        )
    edges.extend(
        [
            (f"RLY-{letter}06", f"TB-1{letter}", "SIG"),
            (f"BAT-125{letter}", f"CHG-1{letter}", "DC"),
            (f"CHG-1{letter}", f"BUS-DC-{letter}", "DC"),
            (f"BUS-DC-{letter}", f"INV-1{letter}", "DC"),
            (f"BUS-DC-{letter}", f"GND-{letter}", "G"),
            (f"INV-1{letter}", f"CP-1{letter}", "SIG"),
            (f"CP-1{letter}", f"TB-1{letter}", "SIG"),
            (f"CP-1{letter}", f"JB-1{letter}", "SIG"),
        ]
    )
    return edges


def build_edges() -> list[tuple[str, str, str]]:
    edges = source_edges()
    for letter in "ABCD":
        edges.extend(division_edges(letter))
    return edges


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
            writer.writerow(
                [row_node]
                + [
                    0 if row_node == col_node else int(frozenset((row_node, col_node)) in edge_set)
                    for col_node in nodes
                ]
            )


def write_pair_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edge_set = {frozenset((a, b)) for a, b, _ in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "column", "connected"])
        for a in nodes:
            for b in nodes:
                writer.writerow([a, b, 0 if a == b else int(frozenset((a, b)) in edge_set)])


def validate(nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    node_set = set(nodes)
    missing = sorted({node for a, b, _ in edges for node in (a, b)} - node_set)
    if missing:
        raise ValueError(f"Missing nodes referenced by edges: {missing}")
    if len(nodes) != len(node_set):
        raise ValueError("Duplicate node found")
    if len({frozenset((a, b)) for a, b, _ in edges}) != len(edges):
        raise ValueError("Duplicate undirected edge found")


def write_round(round_name: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> dict[str, object]:
    validate(nodes, edges)
    write_nodes(RESULTS_DIR / f"{round_name}_nodes.txt", nodes)
    write_edges(RESULTS_DIR / f"{round_name}_edges.csv", edges)
    write_matrix(RESULTS_DIR / f"{round_name}_connectivity_matrix.csv", nodes, edges)
    return {
        "round": round_name,
        "nodes": len(nodes),
        "edges": len(edges),
        **ROUND_META[round_name],
    }


def write_report(rounds: list[dict[str, object]], nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    lines = [
        "# Document 15 Connectivity Extraction Report",
        "",
        "Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.",
        "",
        "## Final Matrix",
        "",
        f"- Final node count: {len(nodes)}",
        f"- Final accepted edge count: {len(edges)}",
        "- Matrix file: `final_connectivity_matrix.csv`",
        "- Sparse edge file: `final_sparse_edges.csv`",
        "",
        "## Round Summary",
        "",
        "| Round | Agent | Nodes | Edges | Summary |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rounds:
        lines.append(f"| {row['round']} | {row['agent']} | {row['nodes']} | {row['edges']} | {row['summary']} |")
    lines.extend(
        [
            "",
            "## Final Precision Decisions",
            "",
            "- Kept all Diego R1 accepted edges after Jennifer's visual review.",
            "- Accepted only landed DG-to-`CB-DG-*` feeders, not DG-to-`BUS-NSS-*` overlaps.",
            "- Accepted only direct SEQ/RPS dashed landings: DG-side for A/C and NF-side for B/D.",
            "- Kept MCC `CB-*` to `RLY-*` dashed control edges because each is visibly landed.",
            "- Kept only `RLY-*06` onward terminal-block control edges because only those continue to `TB-1*`.",
            "",
            "## Excluded Or Still Uncertain",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in UNCERTAIN)
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    nodes = build_nodes()
    edges = build_edges()

    rounds = [write_round(round_name, nodes, edges) for round_name in ROUND_META]

    validate(nodes, edges)
    write_nodes(RESULTS_DIR / "final_nodes.txt", nodes)
    write_edges(RESULTS_DIR / "final_sparse_edges.csv", edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", nodes, edges)
    write_pair_matrix(RESULTS_DIR / "final_sparse_matrix_pairs.csv", nodes, edges)
    (RESULTS_DIR / "rounds_connectivity.json").write_text(json.dumps(rounds, indent=2) + "\n", encoding="utf-8")
    write_report(rounds, nodes, edges)

    print(f"Wrote {len(rounds)} round matrices.")
    print(f"Final nodes: {len(nodes)}")
    print(f"Final edges: {len(edges)}")


if __name__ == "__main__":
    main()
