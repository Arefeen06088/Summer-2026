from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"


BASE_NODES = [
    "GRID-230KV",
    "SWYD-230",
    "DS-101",
    "CB-101",
    "TR-SUT-1A",
    "TR-SUT-1B",
    "GEN-G1",
    "CB-201",
    "TR-UAT-1A",
    "TR-UAT-1B",
    "EDG-A",
    "CB-DGA",
    "EDG-B",
    "CB-DGB",
    "EDG-C",
    "CB-DGC",
    "EDG-D",
    "CB-DGD",
    "BUS-4A",
    "BUS-4B",
    "BUS-4C",
    "BUS-4D",
    "CB-TIE-AB",
    "CB-TIE-CD",
]


BASE_EDGES = [
    ("GRID-230KV", "SWYD-230", "P"),
    ("SWYD-230", "DS-101", "P"),
    ("DS-101", "CB-101", "P"),
    ("CB-101", "TR-SUT-1A", "P"),
    ("CB-101", "TR-SUT-1B", "P"),
    ("TR-SUT-1A", "BUS-4A", "P"),
    ("TR-SUT-1B", "BUS-4B", "P"),
    ("GEN-G1", "CB-201", "P"),
    ("CB-201", "TR-UAT-1A", "P"),
    ("CB-201", "TR-UAT-1B", "P"),
    ("TR-UAT-1A", "BUS-4C", "P"),
    ("TR-UAT-1B", "BUS-4D", "P"),
    ("EDG-A", "CB-DGA", "P"),
    ("CB-DGA", "BUS-4A", "P"),
    ("EDG-B", "CB-DGB", "P"),
    ("CB-DGB", "BUS-4B", "P"),
    ("EDG-C", "CB-DGC", "P"),
    ("CB-DGC", "BUS-4C", "P"),
    ("EDG-D", "CB-DGD", "P"),
    ("CB-DGD", "BUS-4D", "P"),
    ("BUS-4A", "CB-TIE-AB", "P"),
    ("CB-TIE-AB", "BUS-4B", "P"),
    ("BUS-4C", "CB-TIE-CD", "P"),
    ("CB-TIE-CD", "BUS-4D", "P"),
]


@dataclass(frozen=True)
class Branch:
    cb: str
    load: str
    ds: str | None = None


@dataclass(frozen=True)
class TrainSpec:
    letter: str
    relays: dict[str, str]
    branches: list[Branch]


TRAIN_SPECS = [
    TrainSpec(
        "A",
        {"01": "RLY-KA01", "02": "RLY-KA02", "05": "RLY-KA05", "07": "RLY-KA07"},
        [
            Branch("CB-A01", "PMP-SI-A01", "DS-A01"),
            Branch("CB-A02", "PMP-RHR-A02"),
            Branch("CB-A03", "MTR-CCW-A03", "DS-A03"),
            Branch("CB-A04", "FAN-VC-A04"),
            Branch("CB-A05", "MOV-RCS-A05"),
            Branch("CB-A06", "PMP-CHG-A06", "DS-A06"),
            Branch("CB-A07", "HTR-CAB-A07"),
            Branch("CB-A08", "INST-RK-A08"),
            Branch("CB-A09", "VLV-HPI-A09"),
            Branch("CB-A10", "PNL-ESF-A10"),
        ],
    ),
    TrainSpec(
        "B",
        {"02": "RLY-KB02", "04": "RLY-KB04", "06": "RLY-KB06"},
        [
            Branch("CB-B01", "PMP-SI-B01"),
            Branch("CB-B02", "PMP-RHR-B02", "DS-B02"),
            Branch("CB-B03", "MTR-CCW-B03"),
            Branch("CB-B04", "FAN-VC-B04"),
            Branch("CB-B05", "MOV-RCS-B05", "DS-B05"),
            Branch("CB-B06", "PMP-CHG-B06"),
            Branch("CB-B07", "HTR-CAB-B07"),
            Branch("CB-B08", "INST-RK-B08", "DS-B08"),
            Branch("CB-B09", "VLV-HPI-B09"),
            Branch("CB-B10", "PNL-ESF-B10"),
        ],
    ),
    TrainSpec(
        "C",
        {"01": "RLY-KC01", "03": "RLY-KC03", "08": "RLY-KC08"},
        [
            Branch("CB-C01", "PMP-SI-C01", "DS-C01"),
            Branch("CB-C02", "PMP-RHR-C02"),
            Branch("CB-C03", "MTR-CCW-C03"),
            Branch("CB-C04", "FAN-VC-C04", "DS-C04"),
            Branch("CB-C05", "MOV-RCS-C05"),
            Branch("CB-C06", "PMP-CHG-C06"),
            Branch("CB-C07", "HTR-CAB-C07", "DS-C07"),
            Branch("CB-C08", "INST-RK-C08"),
            Branch("CB-C09", "VLV-HPI-C09"),
            Branch("CB-C10", "PNL-ESF-C10"),
        ],
    ),
    TrainSpec(
        "D",
        {"02": "RLY-KD02", "05": "RLY-KD05", "07": "RLY-KD07", "10": "RLY-KD10"},
        [
            Branch("CB-D01", "PMP-SI-D01"),
            Branch("CB-D02", "PMP-RHR-D02", "DS-D02"),
            Branch("CB-D03", "MTR-CCW-D03"),
            Branch("CB-D04", "FAN-VC-D04"),
            Branch("CB-D05", "MOV-RCS-D05"),
            Branch("CB-D06", "PMP-CHG-D06", "DS-D06"),
            Branch("CB-D07", "HTR-CAB-D07"),
            Branch("CB-D08", "INST-RK-D08"),
            Branch("CB-D09", "VLV-HPI-D09", "DS-D09"),
            Branch("CB-D10", "PNL-ESF-D10"),
        ],
    ),
]


GROUND_FINAL_NODES = ["GND-A", "GND-C", "GND-D", "GND-PLANT"]
GROUND_ROUND1_JENNIFER_NODES = ["GND-A", "GND-B", "GND-C", "GND-D", "GND-PLANT"]
GROUND_EDGES = [
    ("GEN-G1", "GND-A", "G"),
    ("TR-480C", "GND-C", "G"),
    ("TR-480D", "GND-D", "G"),
    ("GND-C", "GND-PLANT", "G"),
    ("GND-D", "GND-PLANT", "G"),
]


DIEGO_EXTRA_NODES = [
    "LOCAL-IO-A",
    "LOCAL-IO-B",
    "LOCAL-IO-C",
    "LOCAL-IO-D",
    "125VDC-A",
    "125VDC-B",
    "125VDC-C",
    "125VDC-D",
    "CONTINUATION-125VDC-SHT-DC-2",
    "ANNUNCIATOR-PPC",
]


EXCLUDED_OR_UNCERTAIN = [
    "125VDC-A/B/C/D voltage labels",
    "LOCAL-IO-A/B/C/D line-end labels",
    "CONTINUATION-125VDC-SHT-DC-2",
    "ANNUNCIATOR-PPC",
    "JB-X1,DC-BUS-X",
    "LC-480X,CHG-125X",
    "UPS-X,unlabeled output",
    "auto-start labels to EDGs",
    "ESFAS permissive note text to relays",
    "GND-A,GND-PLANT",
    "GND-B,GND-PLANT",
    "isolated GND-B node",
]


ROUND_NOTES = {
    "round01_diego": {
        "agent": "Diego",
        "role": "high-recall extractor",
        "summary": "Initial high-recall extraction included label/continuation nodes and tentative JB-to-DC/voltage-label/local-I/O edges.",
    },
    "round01_jennifer": {
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "summary": "Removed label-only and continuation-only nodes/edges, kept only landed relay-control edges, but still listed isolated GND-B.",
    },
    "round02_diego": {
        "agent": "Diego",
        "role": "high-recall saturation review",
        "summary": "Agreed with Jennifer's corrected candidate and noted the isolated GND-B count issue.",
    },
    "round02_jennifer": {
        "agent": "Jennifer",
        "role": "precision final signoff",
        "summary": "Removed isolated GND-B for the final accepted/connected matrix.",
    },
}


def train_nodes(spec: TrainSpec) -> list[str]:
    letter = spec.letter
    nodes = [
        f"CB-4{letter}-48",
        f"TR-480{letter}",
        f"CB-48{letter}",
        f"LC-480{letter}",
        f"PP-{letter}1",
        f"MCC-{letter}1",
        f"MCC-{letter}2",
        f"JB-{letter}1",
    ]
    nodes.extend(branch.cb for branch in spec.branches)
    nodes.extend(branch.ds for branch in spec.branches if branch.ds)
    nodes.extend(spec.relays.values())
    nodes.extend(branch.load for branch in spec.branches)
    nodes.extend([f"BAT-125{letter}", f"CHG-125{letter}", f"DC-BUS-{letter}", f"INV-{letter}", f"UPS-{letter}"])
    return nodes


def train_edges(spec: TrainSpec) -> list[tuple[str, str, str]]:
    letter = spec.letter
    edges = [
        (f"BUS-4{letter}", f"CB-4{letter}-48", "P"),
        (f"CB-4{letter}-48", f"TR-480{letter}", "P"),
        (f"TR-480{letter}", f"CB-48{letter}", "P"),
        (f"CB-48{letter}", f"LC-480{letter}", "P"),
        (f"LC-480{letter}", f"PP-{letter}1", "P"),
        (f"LC-480{letter}", f"MCC-{letter}1", "P"),
        (f"LC-480{letter}", f"MCC-{letter}2", "P"),
        (f"LC-480{letter}", f"JB-{letter}1", "P"),
        (f"BAT-125{letter}", f"CHG-125{letter}", "DC"),
        (f"CHG-125{letter}", f"DC-BUS-{letter}", "DC"),
        (f"DC-BUS-{letter}", f"INV-{letter}", "DC"),
        (f"INV-{letter}", f"UPS-{letter}", "P"),
    ]
    for branch in spec.branches:
        mcc = f"MCC-{letter}1" if int(branch.cb[-2:]) <= 5 else f"MCC-{letter}2"
        edges.append((mcc, branch.cb, "P"))
        if branch.ds:
            edges.append((branch.cb, branch.ds, "P"))
            edges.append((branch.ds, branch.load, "P"))
        else:
            edges.append((branch.cb, branch.load, "P"))
    for cb_suffix, relay in spec.relays.items():
        edges.append((relay, f"CB-{letter}{cb_suffix}", "D"))
    return edges


def final_nodes() -> list[str]:
    nodes = list(BASE_NODES)
    for spec in TRAIN_SPECS:
        nodes.extend(train_nodes(spec))
    nodes.extend(GROUND_FINAL_NODES)
    return nodes


def final_edges() -> list[tuple[str, str, str]]:
    edges = list(BASE_EDGES)
    for spec in TRAIN_SPECS:
        edges.extend(train_edges(spec))
    edges.extend(GROUND_EDGES)
    return edges


def diego_r1_nodes() -> list[str]:
    nodes = list(BASE_NODES)
    for spec in TRAIN_SPECS:
        nodes.extend(train_nodes(spec))
    nodes.extend(GROUND_ROUND1_JENNIFER_NODES)
    nodes.extend(DIEGO_EXTRA_NODES)
    return nodes


def diego_r1_edges() -> list[tuple[str, str, str]]:
    edges = final_edges()
    for spec in TRAIN_SPECS:
        letter = spec.letter
        edges.extend(
            [
                (f"LC-480{letter}", f"LOCAL-IO-{letter}", "P"),
                (f"JB-{letter}1", f"DC-BUS-{letter}", "D"),
                (f"DC-BUS-{letter}", f"125VDC-{letter}", "DC"),
            ]
        )
    return edges


def round01_jennifer_nodes() -> list[str]:
    nodes = list(BASE_NODES)
    for spec in TRAIN_SPECS:
        nodes.extend(train_nodes(spec))
    nodes.extend(GROUND_ROUND1_JENNIFER_NODES)
    return nodes


def edge_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def validate(nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"Duplicate nodes: {duplicates}")
    node_set = set(nodes)
    missing = sorted({endpoint for edge in edges for endpoint in edge[:2] if endpoint not in node_set})
    if missing:
        raise ValueError(f"Edges reference nodes not in node list: {missing}")
    keys = [edge_key(a, b) for a, b, _ in edges]
    if len(keys) != len(set(keys)):
        duplicates = sorted({key for key in keys if keys.count(key) > 1})
        raise ValueError(f"Duplicate undirected edges: {duplicates}")


def write_nodes(path: Path, nodes: list[str]) -> None:
    path.write_text("\n".join(nodes) + "\n", encoding="utf-8")


def write_edges(path: Path, edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["A", "B", "type"])
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    adjacency = {node: {other: 0 for other in nodes} for node in nodes}
    for a, b, _ in edges:
        adjacency[a][b] = 1
        adjacency[b][a] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [adjacency[node][other] for other in nodes])


def write_sparse_pairs(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edge_types = {edge_key(a, b): edge_type for a, b, edge_type in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "connected", "type"])
        for i, a in enumerate(nodes):
            for b in nodes[i + 1 :]:
                key = edge_key(a, b)
                writer.writerow([a, b, 1 if key in edge_types else 0, edge_types.get(key, "")])


def write_round_artifacts(round_name: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> dict[str, object]:
    validate(nodes, edges)
    write_nodes(RESULTS_DIR / f"{round_name}_nodes.txt", nodes)
    write_edges(RESULTS_DIR / f"{round_name}_edges.csv", edges)
    write_matrix(RESULTS_DIR / f"{round_name}_connectivity_matrix.csv", nodes, edges)
    return {
        "round": round_name,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "matrix": f"{round_name}_connectivity_matrix.csv",
        "edges": f"{round_name}_edges.csv",
        **ROUND_NOTES[round_name],
    }


def write_report(rounds: list[dict[str, object]], nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    lines = [
        "# Document 13 Connectivity Extraction Report",
        "",
        "Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used.",
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
    for entry in rounds:
        lines.append(
            f"| {entry['round']} | {entry['agent']} | {entry['node_count']} | {entry['edge_count']} | {entry['summary']} |"
        )
    lines.extend(
        [
            "",
            "## Final Precision Changes",
            "",
            "- Removed `125VDC-A/B/C/D` voltage-label nodes.",
            "- Removed `LOCAL-IO-A/B/C/D` line-end label nodes.",
            "- Removed continuation/destination annotations `CONTINUATION-125VDC-SHT-DC-2` and `ANNUNCIATOR-PPC`.",
            "- Removed `JB-X1` to `DC-BUS-X` edges because the dashed/control route does not cleanly land on the DC bus.",
            "- Removed isolated `GND-B` from the final accepted/connected matrix.",
            "- Kept only relay-to-breaker dashed control edges that visibly land at a specific breaker/contact.",
            "",
            "## Excluded Or Still Uncertain",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in EXCLUDED_OR_UNCERTAIN)
    lines.append("")
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_node_list = final_nodes()
    final_edge_list = final_edges()
    rounds = [
        write_round_artifacts("round01_diego", diego_r1_nodes(), diego_r1_edges()),
        write_round_artifacts("round01_jennifer", round01_jennifer_nodes(), final_edge_list),
        write_round_artifacts("round02_diego", final_node_list, final_edge_list),
        write_round_artifacts("round02_jennifer", final_node_list, final_edge_list),
    ]

    write_nodes(RESULTS_DIR / "final_nodes.txt", final_node_list)
    write_edges(RESULTS_DIR / "final_sparse_edges.csv", final_edge_list)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_node_list, final_edge_list)
    write_sparse_pairs(RESULTS_DIR / "final_sparse_matrix_pairs.csv", final_node_list, final_edge_list)
    (RESULTS_DIR / "rounds_connectivity.json").write_text(json.dumps(rounds, indent=2), encoding="utf-8")
    write_report(rounds, final_node_list, final_edge_list)

    print(json.dumps({"final_nodes": len(final_node_list), "final_edges": len(final_edge_list), "rounds": rounds}, indent=2))


if __name__ == "__main__":
    main()
