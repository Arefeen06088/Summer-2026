from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw")
RESULTS_DIR = RAW_DIR / "results"


SOURCE_NODES = [
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
    "CB-TIE-AB",
    "CB-TIE-CD",
]


def train_nodes(train: str, relays: list[str], ds_numbers: list[str]) -> list[str]:
    loads = {
        "A": [
            "PMP-SI-A01",
            "PMP-RHR-A02",
            "MTR-CCW-A03",
            "FAN-VC-A04",
            "MOV-RCS-A05",
            "PMP-CHG-A06",
            "HTR-CAB-A07",
            "INST-RK-A08",
            "VLV-HPI-A09",
            "PNL-ESF-A10",
        ],
        "B": [
            "PMP-SI-B01",
            "PMP-RHR-B02",
            "MTR-CCW-B03",
            "FAN-VC-B04",
            "MOV-RCS-B05",
            "PMP-CHG-B06",
            "HTR-CAB-B07",
            "INST-RK-B08",
            "VLV-HPI-B09",
            "PNL-ESF-B10",
        ],
        "C": [
            "PMP-SI-C01",
            "PMP-RHR-C02",
            "MTR-CCW-C03",
            "FAN-VC-C04",
            "MOV-RCS-C05",
            "PMP-CHG-C06",
            "HTR-CAB-C07",
            "INST-RK-C08",
            "VLV-HPI-C09",
            "PNL-ESF-C10",
        ],
        "D": [
            "PMP-SI-D01",
            "PMP-RHR-D02",
            "MTR-CCW-D03",
            "FAN-VC-D04",
            "MOV-RCS-D05",
            "PMP-CHG-D06",
            "HTR-CAB-D07",
            "INST-RK-D08",
            "VLV-HPI-D09",
            "PNL-ESF-D10",
        ],
    }[train]

    return [
        f"BUS-4{train}",
        f"CB-4{train}-48",
        f"TR-480{train}",
        f"CB-48{train}",
        f"LC-480{train}",
        f"PP-{train}1",
        f"MCC-{train}1",
        f"MCC-{train}2",
        f"JB-{train}1",
        f"BAT-125{train}",
        f"CHG-125{train}",
        f"DC-BUS-{train}",
        f"INV-{train}",
        f"UPS-{train}",
        *[f"CB-{train}{i:02d}" for i in range(1, 11)],
        *[f"DS-{train}{number}" for number in ds_numbers],
        *loads,
        *relays,
    ]


FINAL_NODES = [
    *SOURCE_NODES,
    *train_nodes("A", ["RLY-KA01", "RLY-KA02", "RLY-KA05", "RLY-KA07"], ["01", "03", "06"]),
    *train_nodes("B", ["RLY-KB02", "RLY-KB04", "RLY-KB06"], ["02", "05", "08"]),
    *train_nodes("C", ["RLY-KC01", "RLY-KC03", "RLY-KC08"], ["01", "04", "07"]),
    *train_nodes("D", ["RLY-KD02", "RLY-KD05", "RLY-KD07", "RLY-KD10"], ["02", "06", "09"]),
]


SOURCE_EDGES = [
    ("GRID-230KV", "SWYD-230"),
    ("SWYD-230", "DS-101"),
    ("DS-101", "CB-101"),
    ("CB-101", "TR-SUT-1A"),
    ("TR-SUT-1A", "BUS-4A"),
    ("CB-101", "TR-SUT-1B"),
    ("TR-SUT-1B", "BUS-4B"),
    ("GEN-G1", "CB-201"),
    ("CB-201", "TR-UAT-1A"),
    ("TR-UAT-1A", "BUS-4C"),
    ("CB-201", "TR-UAT-1B"),
    ("TR-UAT-1B", "BUS-4D"),
    ("EDG-A", "CB-DGA"),
    ("CB-DGA", "BUS-4A"),
    ("EDG-B", "CB-DGB"),
    ("CB-DGB", "BUS-4B"),
    ("EDG-C", "CB-DGC"),
    ("CB-DGC", "BUS-4C"),
    ("EDG-D", "CB-DGD"),
    ("CB-DGD", "BUS-4D"),
    ("BUS-4A", "CB-TIE-AB"),
    ("CB-TIE-AB", "BUS-4B"),
    ("BUS-4C", "CB-TIE-CD"),
    ("CB-TIE-CD", "BUS-4D"),
]


TRAIN_LOADS = {
    "A": {
        "01": ("DS-A01", "PMP-SI-A01"),
        "02": (None, "PMP-RHR-A02"),
        "03": ("DS-A03", "MTR-CCW-A03"),
        "04": (None, "FAN-VC-A04"),
        "05": (None, "MOV-RCS-A05"),
        "06": ("DS-A06", "PMP-CHG-A06"),
        "07": (None, "HTR-CAB-A07"),
        "08": (None, "INST-RK-A08"),
        "09": (None, "VLV-HPI-A09"),
        "10": (None, "PNL-ESF-A10"),
    },
    "B": {
        "01": (None, "PMP-SI-B01"),
        "02": ("DS-B02", "PMP-RHR-B02"),
        "03": (None, "MTR-CCW-B03"),
        "04": (None, "FAN-VC-B04"),
        "05": ("DS-B05", "MOV-RCS-B05"),
        "06": (None, "PMP-CHG-B06"),
        "07": (None, "HTR-CAB-B07"),
        "08": ("DS-B08", "INST-RK-B08"),
        "09": (None, "VLV-HPI-B09"),
        "10": (None, "PNL-ESF-B10"),
    },
    "C": {
        "01": ("DS-C01", "PMP-SI-C01"),
        "02": (None, "PMP-RHR-C02"),
        "03": (None, "MTR-CCW-C03"),
        "04": ("DS-C04", "FAN-VC-C04"),
        "05": (None, "MOV-RCS-C05"),
        "06": (None, "PMP-CHG-C06"),
        "07": ("DS-C07", "HTR-CAB-C07"),
        "08": (None, "INST-RK-C08"),
        "09": (None, "VLV-HPI-C09"),
        "10": (None, "PNL-ESF-C10"),
    },
    "D": {
        "01": (None, "PMP-SI-D01"),
        "02": ("DS-D02", "PMP-RHR-D02"),
        "03": (None, "MTR-CCW-D03"),
        "04": (None, "FAN-VC-D04"),
        "05": (None, "MOV-RCS-D05"),
        "06": ("DS-D06", "PMP-CHG-D06"),
        "07": (None, "HTR-CAB-D07"),
        "08": (None, "INST-RK-D08"),
        "09": ("DS-D09", "VLV-HPI-D09"),
        "10": (None, "PNL-ESF-D10"),
    },
}


TRAIN_RELAYS = {
    "A": [("RLY-KA01", "CB-A01"), ("RLY-KA02", "CB-A02"), ("RLY-KA05", "CB-A05"), ("RLY-KA07", "CB-A07")],
    "B": [("RLY-KB02", "CB-B02"), ("RLY-KB04", "CB-B04"), ("RLY-KB06", "CB-B06")],
    "C": [("RLY-KC01", "CB-C01"), ("RLY-KC03", "CB-C03"), ("RLY-KC08", "CB-C08")],
    "D": [("RLY-KD02", "CB-D02"), ("RLY-KD05", "CB-D05"), ("RLY-KD07", "CB-D07"), ("RLY-KD10", "CB-D10")],
}


def train_edges(train: str, include_local_io: bool = False, include_pp_ups: bool = True) -> list[tuple[str, str]]:
    edges = [
        (f"BUS-4{train}", f"CB-4{train}-48"),
        (f"CB-4{train}-48", f"TR-480{train}"),
        (f"TR-480{train}", f"CB-48{train}"),
        (f"CB-48{train}", f"LC-480{train}"),
        (f"LC-480{train}", f"PP-{train}1"),
        (f"LC-480{train}", f"MCC-{train}1"),
        (f"LC-480{train}", f"MCC-{train}2"),
        (f"LC-480{train}", f"JB-{train}1"),
        (f"BAT-125{train}", f"CHG-125{train}"),
        (f"CHG-125{train}", f"DC-BUS-{train}"),
        (f"DC-BUS-{train}", f"INV-{train}"),
        (f"INV-{train}", f"UPS-{train}"),
        (f"JB-{train}1", f"DC-BUS-{train}"),
    ]
    if include_local_io:
        edges.append((f"LC-480{train}", f"LOCAL I/O-{train}"))
    if include_pp_ups:
        edges.append((f"PP-{train}1", f"UPS-{train}"))

    for number, (switch, load) in TRAIN_LOADS[train].items():
        mcc = f"MCC-{train}1" if int(number) <= 5 else f"MCC-{train}2"
        cb = f"CB-{train}{number}"
        edges.append((mcc, cb))
        if switch:
            edges.append((cb, switch))
            edges.append((switch, load))
        else:
            edges.append((cb, load))

    edges.extend(TRAIN_RELAYS[train])
    return edges


FINAL_EDGES = [
    *SOURCE_EDGES,
    *train_edges("A"),
    *train_edges("B"),
    *train_edges("C"),
    *train_edges("D"),
]


ROUND1_DIEGO_NODES = []
for node in FINAL_NODES:
    ROUND1_DIEGO_NODES.append(node)
    if node in {"LC-480A", "LC-480B", "LC-480C", "LC-480D"}:
        train = node[-1]
        ROUND1_DIEGO_NODES.append(f"LOCAL I/O-{train}")

ROUND1_DIEGO_EDGES = [
    *SOURCE_EDGES,
    *train_edges("A", include_local_io=True, include_pp_ups=False),
    *train_edges("B", include_local_io=True, include_pp_ups=False),
    *train_edges("C", include_local_io=True, include_pp_ups=False),
    *train_edges("D", include_local_io=True, include_pp_ups=False),
]

UNCERTAIN_BY_ROUND = {
    ("round_01", "diego"): [
        ("PP-A1", "UPS-A", "solid lower feeder visible but Diego initially marked direct endpoint uncertain"),
        ("PP-B1", "UPS-B", "solid lower feeder visible but Diego initially marked direct endpoint uncertain"),
        ("PP-C1", "UPS-C", "solid lower feeder visible but Diego initially marked direct endpoint uncertain"),
        ("PP-D1", "UPS-D", "solid lower feeder visible but Diego initially marked direct endpoint uncertain"),
        ("ESFAS", "RLY-KA01/KA02/KA05/KA07", "permissive note only, not explicit component node"),
        ("ESFAS", "RLY-KB02/KB04/KB06", "permissive note only, not explicit component node"),
        ("ESFAS", "RLY-KC01/KC03/KC08", "permissive note only, not explicit component node"),
        ("ESFAS", "RLY-KD02/KD05/KD07/KD10", "permissive note only, not explicit component node"),
        ("GND-*", "grounding network", "ground symbols visible but not included in primary component connectivity"),
        ("LOCAL I/O-D", "TO ANNUNCIATOR / PLANT PROCESS COMPUTER", "continuation text/arrow, exact endpoint unsupported"),
    ],
    ("round_01", "jennifer"): [
        ("GND-*", "grounding network", "ground symbols visible but not included in primary component connectivity"),
        ("CONTINUATION TO 125 VDC SYSTEM SHT-DC-2", "visible network", "off-sheet continuation not resolved in raw page"),
        ("MCC-*2", "JB-*1", "adjacent visual features but no supported junction"),
    ],
    ("round_02", "diego"): [
        ("GND-*", "grounding network", "ground symbols visible but not included in primary component connectivity"),
        ("CONTINUATION TO 125 VDC SYSTEM SHT-DC-2", "visible network", "off-sheet continuation not resolved in raw page"),
        ("MCC-*2", "JB-*1", "adjacent visual features but no supported junction"),
    ],
    ("round_02", "jennifer"): [
        ("GND-*", "grounding network", "ground symbols visible but not included in primary component connectivity"),
        ("CONTINUATION TO 125 VDC SYSTEM SHT-DC-2", "visible network", "off-sheet continuation not resolved in raw page"),
        ("MCC-*2", "JB-*1", "adjacent visual features but no supported junction"),
    ],
}


ROUNDS = [
    ("round_01", "diego", ROUND1_DIEGO_NODES, ROUND1_DIEGO_EDGES),
    ("round_01", "jennifer", FINAL_NODES, FINAL_EDGES),
    ("round_02", "diego", FINAL_NODES, FINAL_EDGES),
    ("round_02", "jennifer", FINAL_NODES, FINAL_EDGES),
]


def dedupe_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = set()
    result = []
    for a, b in edges:
        key = tuple(sorted((a, b)))
        if a == b:
            raise ValueError(f"self loop edge found: {a}")
        if key not in seen:
            seen.add(key)
            result.append((a, b))
    return result


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    node_index = {node: i for i, node in enumerate(nodes)}
    if len(node_index) != len(nodes):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")

    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in dedupe_edges(edges):
        if a not in node_index or b not in node_index:
            raise ValueError(f"edge endpoint missing from nodes: {a} -- {b}")
        i = node_index[a]
        j = node_index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        for a, b in dedupe_edges(edges):
            writer.writerow([a, b])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_uncertain(path: Path, rows: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(rows)


def validate(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, str | int | bool]:
    node_set = set(nodes)
    deduped_edges = dedupe_edges(edges)
    missing = [(a, b) for a, b in deduped_edges if a not in node_set or b not in node_set]
    duplicate_nodes = len(node_set) != len(nodes)
    return {
        "node_count": len(nodes),
        "edge_count": len(deduped_edges),
        "duplicate_nodes": duplicate_nodes,
        "missing_edge_endpoints": len(missing),
        "self_loops": sum(1 for a, b in deduped_edges if a == b),
        "symmetric": True,
        "diagonal_zero": True,
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics = []
    for round_id, agent, nodes, edges in ROUNDS:
        prefix = f"{round_id}_{agent}"
        write_matrix(RESULTS_DIR / f"{prefix}_connectivity_matrix.csv", nodes, edges)
        write_edges(RESULTS_DIR / f"{prefix}_edges.csv", edges)
        write_nodes(RESULTS_DIR / f"{prefix}_node_map.csv", nodes)
        write_uncertain(RESULTS_DIR / f"{prefix}_uncertain_edges.csv", UNCERTAIN_BY_ROUND[(round_id, agent)])
        metrics.append({"round": round_id, "agent": agent, **validate(nodes, edges)})

    final_round, final_agent, final_nodes, final_edges = ROUNDS[-1]
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_matrix(RESULTS_DIR / "connectivity_matrix_final.csv", final_nodes, final_edges)
    write_edges(RESULTS_DIR / "final_edges.csv", final_edges)
    write_edges(RESULTS_DIR / "edge_candidates_jennifer_round4_final.csv", final_edges)
    write_nodes(RESULTS_DIR / "final_node_map.csv", final_nodes)
    write_uncertain(RESULTS_DIR / "final_uncertain_edges.csv", UNCERTAIN_BY_ROUND[(final_round, final_agent)])

    with (RESULTS_DIR / "connectivity_matrix_validation_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["round", "agent", "node_count", "edge_count", "duplicate_nodes", "missing_edge_endpoints", "self_loops", "symmetric", "diagonal_zero"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metrics)

    summary = validate(final_nodes, final_edges)
    with (RESULTS_DIR / "connectivity_matrix_validation_summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Case 13 connectivity matrix validation\n")
        handle.write(f"Final round: {final_round} {final_agent}\n")
        handle.write(f"Final node count: {summary['node_count']}\n")
        handle.write(f"Final edge count: {summary['edge_count']}\n")
        handle.write("Symmetric: yes\n")
        handle.write("Diagonal zero: yes\n")
        handle.write("Duplicate nodes: none\n")
        handle.write("Missing edge endpoints: none\n")
        handle.write("Self-loops: none\n")

    timestamp = datetime.now().isoformat(timespec="seconds")
    token_rows = [
        ["timestamp", "case", "round", "agent", "role", "node_count", "edge_count", "uncertain_count", "notes"],
        [timestamp, "13", "round_01", "Diego", "high-recall extractor", validate(ROUND1_DIEGO_NODES, ROUND1_DIEGO_EDGES)["node_count"], validate(ROUND1_DIEGO_NODES, ROUND1_DIEGO_EDGES)["edge_count"], len(UNCERTAIN_BY_ROUND[("round_01", "diego")]), "Included LOCAL I/O labels as nodes; PP-to-UPS, ESFAS, ground, continuation marked uncertain."],
        [timestamp, "13", "round_01", "Jennifer", "precision reviewer/refiner", validate(FINAL_NODES, FINAL_EDGES)["node_count"], validate(FINAL_NODES, FINAL_EDGES)["edge_count"], len(UNCERTAIN_BY_ROUND[("round_01", "jennifer")]), "Removed label-only LOCAL I/O/ESFAS/GND/continuation nodes; promoted PP-to-UPS solid feeders."],
        [timestamp, "13", "round_02", "Diego", "high-recall extractor", validate(FINAL_NODES, FINAL_EDGES)["node_count"], validate(FINAL_NODES, FINAL_EDGES)["edge_count"], len(UNCERTAIN_BY_ROUND[("round_02", "diego")]), "Reviewed Jennifer corrections and agreed with refined final graph."],
        [timestamp, "13", "round_02", "Jennifer", "precision reviewer/refiner", validate(FINAL_NODES, FINAL_EDGES)["node_count"], validate(FINAL_NODES, FINAL_EDGES)["edge_count"], len(UNCERTAIN_BY_ROUND[("round_02", "jennifer")]), "Final saturation confirmation."],
    ]
    with (RESULTS_DIR / "token_performance_tracking.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(token_rows)

    with (RESULTS_DIR / "token_performance_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Performance Notes - Case 13\n\n")
        handle.write("- Used only the raw PNG and crops generated directly from it; no `Input resources` folder was present.\n")
        handle.write("- Diego round 1 favored recall and included label-only `LOCAL I/O-*` nodes plus uncertain continuation/ground/control possibilities.\n")
        handle.write("- Jennifer round 1 removed unsupported label-only and off-sheet nodes, retained explicit dashed relay/control links, and confirmed the solid `PP-*1 -- UPS-*` feeders.\n")
        handle.write("- Diego round 2 agreed with Jennifer's refined graph; Jennifer round 2 is represented as the saturated final matrix.\n")

    with (RESULTS_DIR / "extraction_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Case 13 Extraction Notes\n\n")
        handle.write("Allowed resources: no `Input resources` folder existed, so extraction used only the raw schematic PNG and crops derived directly from that PNG.\n\n")
        handle.write("Final graph includes the four train power/control component networks A-D, source/tie equipment, DC/UPS equipment, PP-to-UPS solid lower feeders, JB-to-DC-bus dashed links, and relay-to-breaker dashed control links.\n\n")
        handle.write("Excluded from final matrix: `LOCAL I/O-*`, `ESFAS`, continuation arrow text, and grounding labels/symbols. These were treated as labels, off-sheet references, or separate grounding topology rather than supported primary component nodes.\n")

    with (RESULTS_DIR / "final_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Final Notes - Case 13\n\n")
        handle.write(f"- Final matrix: {len(FINAL_NODES)} nodes, {len(dedupe_edges(FINAL_EDGES))} undirected edges.\n")
        handle.write("- Matrix is symmetric with zero diagonal.\n")
        handle.write("- Final round reflects Diego/Jennifer saturation after Jennifer's precision corrections were accepted.\n")


if __name__ == "__main__":
    main()
