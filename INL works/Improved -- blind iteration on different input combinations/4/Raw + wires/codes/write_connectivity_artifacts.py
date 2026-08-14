from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


BASE_NODES = [
    "BUS-480-RB1",
    "BUS-480-RB2",
    "BUS-480-LCA",
    "BUS-480-LCB",
    "BUS-125DCA",
    "BUS-UPS-A",
    "BUS-125DCB",
    "BUS-UPS-B",
    "US-345A",
    "CB-UAT-A",
    "TR-UAT-1",
    "CB-IN-A",
    "EDG-1A",
    "CB-DG-A",
    "US-230B",
    "CB-SAT-B",
    "TR-SAT-2",
    "CB-IN-B",
    "EDG-1B",
    "CB-DG-B",
    "CB-TIE-480",
    "CB-LC-A",
    "TR-LC-A",
    "CB-LC-A2",
    "GND-NG-A",
    "CB-LC-B",
    "TR-LC-B",
    "CB-LC-B2",
    "GND-NG-B",
    "CB-LC-TIE",
    "CB-F101",
    "OL-F101",
    "PMP-SI-1A",
    "CB-F102",
    "OL-F102",
    "PMP-RHR-1A",
    "CB-F103",
    "OL-F103",
    "FAN-CTMT-1A",
    "CB-F104",
    "OL-F104",
    "MOV-RC-104",
    "CB-F105",
    "OL-F105",
    "PMP-CCW-1A",
    "CB-F106",
    "OL-F106",
    "MOV-IA-106",
    "CB-F107",
    "OL-F107",
    "FAN-AHU-1A",
    "CB-F108",
    "OL-F108",
    "PMP-CS-1A",
    "CB-F109",
    "OL-F109",
    "MOV-EF-109",
    "CB-F110",
    "OL-F110",
    "HTR-PZR-1",
    "CB-F111",
    "OL-F111",
    "PMP-SI-1B",
    "CB-F112",
    "OL-F112",
    "PMP-RHR-1B",
    "CB-F113",
    "OL-F113",
    "FAN-CTMT-1B",
    "CB-F114",
    "OL-F114",
    "MOV-RC-114",
    "CB-F115",
    "OL-F115",
    "PNL-SPARE-F15",
    "CB-A201",
    "OL-201",
    "PMP-SW-2A",
    "CB-A202",
    "OL-202",
    "PMP-CVC-2A",
    "CB-A203",
    "OL-203",
    "MOV-SI-203",
    "CB-A204",
    "OL-204",
    "FAN-CR-2A",
    "CB-A205",
    "OL-205",
    "HTR-BATT-A",
    "CB-B206",
    "OL-206",
    "PMP-SW-2B",
    "CB-B207",
    "OL-207",
    "PMP-CVC-2B",
    "CB-B208",
    "OL-208",
    "MOV-SI-208",
    "CB-B209",
    "OL-209",
    "PNL-LTG-209",
    "DCA-01",
    "CB-CHG-A",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "RPS-TRAIN-A",
    "ESFAS-TRAIN-A",
    "DCB-01",
    "CB-CHG-B",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "RPS-TRAIN-B",
    "ESFAS-TRAIN-B",
]

CONTROL_NODES = [
    "RELAY-K701",
    "TB-ESF-A",
    "ANN-CP-A",
    "RELAY-K702",
    "TB-ESF-B",
    "REC-SER-01",
]

JENNIFER_R1_NODES = [
    "BUS-480-RB1",
    "BUS-480-RB2",
    "BUS-480-LCA",
    "BUS-480-LCB",
    "BUS-125DCA",
    "BUS-UPS-A",
    "BUS-125DCB",
    "BUS-UPS-B",
    "DCA-01",
    "DCB-01",
    "GND-NG-A",
    "GND-NG-B",
    "US-345A",
    "CB-UAT-A",
    "TR-UAT-1",
    "CB-IN-A",
    "EDG-1A",
    "CB-DG-A",
    "US-230B",
    "CB-SAT-B",
    "TR-SAT-2",
    "CB-IN-B",
    "EDG-1B",
    "CB-DG-B",
    "CB-TIE-480",
    "CB-F101",
    "OL-F101",
    "PMP-SI-1A",
    "CB-F102",
    "OL-F102",
    "PMP-RHR-1A",
    "CB-F103",
    "OL-F103",
    "FAN-CTMT-1A",
    "CB-F104",
    "OL-F104",
    "MOV-RC-104",
    "CB-F105",
    "OL-F105",
    "PMP-CCW-1A",
    "CB-F106",
    "OL-F106",
    "MOV-IA-106",
    "CB-F107",
    "OL-F107",
    "FAN-AHU-1A",
    "CB-F108",
    "OL-F108",
    "PMP-CS-1A",
    "CB-F109",
    "OL-F109",
    "MOV-EF-109",
    "CB-F110",
    "OL-F110",
    "HTR-PZR-1",
    "CB-F111",
    "OL-F111",
    "PMP-SI-1B",
    "CB-F112",
    "OL-F112",
    "PMP-RHR-1B",
    "CB-F113",
    "OL-F113",
    "FAN-CTMT-1B",
    "CB-F114",
    "OL-F114",
    "MOV-RC-114",
    "CB-F115",
    "OL-F115",
    "PNL-SPARE-F15",
    "CB-LC-A",
    "TR-LC-A",
    "CB-LC-A2",
    "CB-LC-B",
    "TR-LC-B",
    "CB-LC-B2",
    "CB-LC-TIE",
    "CB-A201",
    "OL-201",
    "PMP-SW-2A",
    "CB-A202",
    "OL-202",
    "PMP-CVC-2A",
    "CB-A203",
    "OL-203",
    "MOV-SI-203",
    "CB-A204",
    "OL-204",
    "FAN-CR-2A",
    "CB-A205",
    "OL-205",
    "HTR-BATT-A",
    "CB-B206",
    "OL-206",
    "PMP-SW-2B",
    "CB-B207",
    "OL-207",
    "PMP-CVC-2B",
    "CB-B208",
    "OL-208",
    "MOV-SI-208",
    "CB-B209",
    "OL-209",
    "PNL-LTG-209",
    "CB-CHG-A",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "RPS-TRAIN-A",
    "ESFAS-TRAIN-A",
    "RELAY-K701",
    "TB-ESF-A",
    "ANN-CP-A",
    "CB-CHG-B",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "RPS-TRAIN-B",
    "ESFAS-TRAIN-B",
    "RELAY-K702",
    "TB-ESF-B",
    "REC-SER-01",
]


def with_diego_r1_labels(nodes: list[str]) -> list[str]:
    return [
        node.replace("FAN-CTMT-1A", "FAN-CNTMT-1A").replace(
            "FAN-CTMT-1B", "FAN-CNTMT-1B"
        )
        for node in nodes
    ]


def edge(a: str, b: str, edge_type: str, confidence: str, evidence: str) -> dict[str, str]:
    return {
        "source": a,
        "target": b,
        "edge_type": edge_type,
        "confidence": confidence,
        "evidence": evidence,
    }


def chain_edges(
    nodes: list[str], edge_type: str, confidence: str, evidence: str
) -> list[dict[str, str]]:
    return [
        edge(a, b, edge_type, confidence, evidence)
        for a, b in zip(nodes, nodes[1:])
    ]


def final_power_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += chain_edges(
        ["US-345A", "CB-UAT-A", "TR-UAT-1", "CB-IN-A", "BUS-480-RB1"],
        "power",
        "high",
        "solid utility transformer feeder to RB1",
    )
    edges += chain_edges(
        ["EDG-1A", "CB-DG-A", "BUS-480-RB1"],
        "power",
        "high",
        "solid emergency generator feeder to RB1",
    )
    edges += chain_edges(
        ["US-230B", "CB-SAT-B", "TR-SAT-2", "CB-IN-B", "BUS-480-RB2"],
        "power",
        "high",
        "solid utility transformer feeder to RB2",
    )
    edges += chain_edges(
        ["EDG-1B", "CB-DG-B", "BUS-480-RB2"],
        "power",
        "high",
        "solid emergency generator feeder to RB2",
    )
    edges += chain_edges(
        ["BUS-480-RB1", "CB-TIE-480", "BUS-480-RB2"],
        "power",
        "high",
        "solid right-side tie between 480 V buses",
    )
    edges += chain_edges(
        ["BUS-480-RB1", "CB-LC-A", "TR-LC-A", "CB-LC-A2", "BUS-480-LCA"],
        "power",
        "high",
        "solid feeder from RB1 to LC-A",
    )
    edges.append(edge("TR-LC-A", "GND-NG-A", "ground", "high", "ground symbol at TR-LC-A"))
    edges += chain_edges(
        ["BUS-480-RB2", "CB-LC-B", "TR-LC-B", "CB-LC-B2", "BUS-480-LCB"],
        "power",
        "high",
        "solid feeder from RB2 to LC-B",
    )
    edges.append(edge("TR-LC-B", "GND-NG-B", "ground", "high", "ground symbol at TR-LC-B"))
    edges += chain_edges(
        ["BUS-480-LCA", "CB-LC-TIE", "BUS-480-LCB"],
        "power",
        "high",
        "dot-marked lower bus tie via CB-LC-TIE",
    )

    f_branches = [
        ("BUS-480-RB1", "CB-F101", "OL-F101", "PMP-SI-1A"),
        ("BUS-480-RB2", "CB-F102", "OL-F102", "PMP-RHR-1A"),
        ("BUS-480-RB1", "CB-F103", "OL-F103", "FAN-CTMT-1A"),
        ("BUS-480-RB2", "CB-F104", "OL-F104", "MOV-RC-104"),
        ("BUS-480-RB1", "CB-F105", "OL-F105", "PMP-CCW-1A"),
        ("BUS-480-RB2", "CB-F106", "OL-F106", "MOV-IA-106"),
        ("BUS-480-RB1", "CB-F107", "OL-F107", "FAN-AHU-1A"),
        ("BUS-480-RB2", "CB-F108", "OL-F108", "PMP-CS-1A"),
        ("BUS-480-RB1", "CB-F109", "OL-F109", "MOV-EF-109"),
        ("BUS-480-RB2", "CB-F110", "OL-F110", "HTR-PZR-1"),
        ("BUS-480-RB1", "CB-F111", "OL-F111", "PMP-SI-1B"),
        ("BUS-480-RB2", "CB-F112", "OL-F112", "PMP-RHR-1B"),
        ("BUS-480-RB1", "CB-F113", "OL-F113", "FAN-CTMT-1B"),
        ("BUS-480-RB2", "CB-F114", "OL-F114", "MOV-RC-114"),
        ("BUS-480-RB1", "CB-F115", "OL-F115", "PNL-SPARE-F15"),
    ]
    for bus, cb, ol, load in f_branches:
        edges += chain_edges([bus, cb, ol, load], "power", "high", f"solid {cb} load branch")

    lc_branches = [
        ("BUS-480-LCA", "CB-A201", "OL-201", "PMP-SW-2A"),
        ("BUS-480-LCA", "CB-A202", "OL-202", "PMP-CVC-2A"),
        ("BUS-480-LCA", "CB-A203", "OL-203", "MOV-SI-203"),
        ("BUS-480-LCA", "CB-A204", "OL-204", "FAN-CR-2A"),
        ("BUS-480-LCA", "CB-A205", "OL-205", "HTR-BATT-A"),
        ("BUS-480-LCB", "CB-B206", "OL-206", "PMP-SW-2B"),
        ("BUS-480-LCB", "CB-B207", "OL-207", "PMP-CVC-2B"),
        ("BUS-480-LCB", "CB-B208", "OL-208", "MOV-SI-208"),
        ("BUS-480-LCB", "CB-B209", "OL-209", "PNL-LTG-209"),
    ]
    for bus, cb, ol, load in lc_branches:
        edges += chain_edges([bus, cb, ol, load], "power", "high", f"solid {cb} load-center branch")

    edges += chain_edges(
        ["BUS-480-LCA", "DCA-01", "CB-CHG-A", "CHG-125A", "BUS-125DCA"],
        "dc_power",
        "high",
        "solid train A charger feed into 125 VDC bus",
    )
    edges.append(edge("BUS-125DCA", "BAT-125A", "dc_power", "high", "battery tie to BUS-125DCA"))
    edges += chain_edges(
        ["BUS-125DCA", "INV-120A", "BUS-UPS-A"],
        "dc_power",
        "high",
        "solid train A inverter feed to UPS-A",
    )
    edges.append(edge("BUS-UPS-A", "RPS-TRAIN-A", "dc_power", "high", "solid UPS-A supply branch"))
    edges.append(edge("BUS-UPS-A", "ESFAS-TRAIN-A", "dc_power", "high", "solid UPS-A supply branch"))

    edges += chain_edges(
        ["BUS-480-LCB", "DCB-01", "CB-CHG-B", "CHG-125B", "BUS-125DCB"],
        "dc_power",
        "high",
        "solid train B charger feed into 125 VDC bus",
    )
    edges.append(edge("BUS-125DCB", "BAT-125B", "dc_power", "high", "battery tie to BUS-125DCB"))
    edges += chain_edges(
        ["BUS-125DCB", "INV-120B", "BUS-UPS-B"],
        "dc_power",
        "high",
        "solid train B inverter feed to UPS-B",
    )
    edges.append(edge("BUS-UPS-B", "RPS-TRAIN-B", "dc_power", "high", "solid UPS-B supply branch"))
    edges.append(edge("BUS-UPS-B", "ESFAS-TRAIN-B", "dc_power", "high", "solid UPS-B supply branch"))
    return edges


FINAL_EDGES = final_power_edges()

SUPPORTED_CONTROL_EDGES = [
    edge("RPS-TRAIN-A", "RELAY-K701", "control_signal", "medium", "dashed control/signal route"),
    edge("ESFAS-TRAIN-A", "RELAY-K701", "control_signal", "medium", "dashed control/signal route"),
    edge("ANN-CP-A", "TB-ESF-A", "control_signal", "high", "dashed SIGA-01 route"),
    edge("REC-SER-01", "TB-ESF-B", "control_signal", "high", "dashed SIGB-01 route"),
    edge("ANN-CP-A", "REC-SER-01", "control_signal", "medium", "dashed SIG-X2 route"),
    edge("RPS-TRAIN-B", "RELAY-K702", "control_signal", "medium", "dashed control/signal route"),
    edge("ESFAS-TRAIN-B", "RELAY-K702", "control_signal", "medium", "dashed control/signal route"),
]

UNCERTAIN_CONTROL_EDGES = [
    edge("RELAY-K701", "TB-ESF-A", "control_signal", "uncertain", "crowded dashed routing near terminal board"),
    edge("RELAY-K702", "TB-ESF-B", "control_signal", "uncertain", "crowded dashed routing near terminal board"),
    edge("RELAY-K701", "CB-LC-B", "control_signal", "uncertain", "dashed interlock passes near breaker without solid terminal clarity"),
    edge("RELAY-K702", "CB-LC-B2", "control_signal", "uncertain", "dashed interlock passes near breaker without solid terminal clarity"),
]


def replace_labels_in_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    replaced = []
    for row in edges:
        new_row = row.copy()
        for key in ("source", "target"):
            new_row[key] = new_row[key].replace("FAN-CTMT-1A", "FAN-CNTMT-1A").replace(
                "FAN-CTMT-1B", "FAN-CNTMT-1B"
            )
        replaced.append(new_row)
    return replaced


def write_nodes(stem: str, nodes: list[str]) -> None:
    with (RESULTS / f"{stem}_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "name"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(stem: str, edges: list[dict[str, str]], include_in_matrix: bool) -> None:
    with (RESULTS / f"{stem}_edges.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "source",
            "target",
            "include_in_matrix",
            "edge_type",
            "confidence",
            "evidence",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in edges:
            out = row.copy()
            out["include_in_matrix"] = "1" if include_in_matrix else "0"
            writer.writerow(out)


def write_matrix(stem: str, nodes: list[str], edges: list[dict[str, str]]) -> dict[str, int | bool]:
    index = {node: i for i, node in enumerate(nodes)}
    if len(index) != len(nodes):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{stem}: duplicate nodes {duplicates}")
    matrix = [[0 for _ in nodes] for _ in nodes]
    missing: list[tuple[str, str]] = []
    for row in edges:
        a, b = row["source"], row["target"]
        if a not in index or b not in index:
            missing.append((a, b))
            continue
        i, j = index[a], index[b]
        if i == j:
            raise ValueError(f"{stem}: self-loop {a}")
        matrix[i][j] = 1
        matrix[j][i] = 1
    if missing:
        raise ValueError(f"{stem}: edge endpoints missing from nodes {missing}")

    with (RESULTS / f"{stem}_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)

    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    zero_diagonal = all(matrix[i][i] == 0 for i in range(len(nodes)))
    edge_count = sum(sum(row) for row in matrix) // 2
    return {
        "node_count": len(nodes),
        "edge_count": edge_count,
        "symmetric": symmetric,
        "zero_diagonal": zero_diagonal,
    }


def build_artifacts() -> None:
    round1_diego_nodes = with_diego_r1_labels(JENNIFER_R1_NODES)
    round1_diego_edges = replace_labels_in_edges(FINAL_EDGES) + replace_labels_in_edges(
        SUPPORTED_CONTROL_EDGES + UNCERTAIN_CONTROL_EDGES
    )
    round1_jennifer_nodes = JENNIFER_R1_NODES
    round1_jennifer_edges = FINAL_EDGES
    round2_diego_nodes = BASE_NODES
    round2_diego_edges = FINAL_EDGES
    round2_jennifer_nodes = BASE_NODES
    round2_jennifer_edges = FINAL_EDGES
    all_visual_nodes = JENNIFER_R1_NODES
    all_visual_edges = FINAL_EDGES + SUPPORTED_CONTROL_EDGES

    rounds = {
        "round1_diego": (round1_diego_nodes, round1_diego_edges),
        "round1_jennifer": (round1_jennifer_nodes, round1_jennifer_edges),
        "round2_diego": (round2_diego_nodes, round2_diego_edges),
        "round2_jennifer": (round2_jennifer_nodes, round2_jennifer_edges),
        "final": (BASE_NODES, FINAL_EDGES),
        "candidate_all_visual_supported": (all_visual_nodes, all_visual_edges),
    }

    qa = {}
    for stem, (nodes, edges) in rounds.items():
        write_nodes(stem, nodes)
        write_edges(stem, edges, include_in_matrix=True)
        qa[stem] = write_matrix(stem, nodes, edges)

    write_edges("final_control_signal_supported_excluded", SUPPORTED_CONTROL_EDGES, include_in_matrix=False)
    write_edges("final_control_signal_uncertain_excluded", UNCERTAIN_CONTROL_EDGES, include_in_matrix=False)

    summary = {
        "document": 4,
        "resource_folder": str(ROOT),
        "main_decision": (
            "final_matrix.csv is the saturated Diego/Jennifer solid power/DC-power "
            "connectivity matrix; dashed control/signal routes are preserved separately."
        ),
        "agents": {
            "diego": {
                "id": "019f6dda-b9a7-74a0-9bd4-0c80fff2dc6b",
                "model": "gpt-5.5",
                "role": "high-recall extractor",
            },
            "jennifer": {
                "id": "019f6de1-05e7-7fb0-aa30-32843bcb5b47",
                "model": "gpt-5.5",
                "role": "precision reviewer/refiner",
            },
        },
        "rounds": {
            "round1_diego": "high-recall matrix with originally read FAN-CNTMT labels and dashed/uncertain candidates included",
            "round1_jennifer": "corrected solid power/DC-power matrix with dashed-only nodes retained as isolated rows",
            "round2_diego": "accepted corrections; omitted dashed-only control nodes",
            "round2_jennifer": "accepted round2 Diego as saturated/final",
        },
        "qa": qa,
        "control_signal_note": {
            "supported_excluded_edges": len(SUPPORTED_CONTROL_EDGES),
            "uncertain_excluded_edges": len(UNCERTAIN_CONTROL_EDGES),
            "all_visual_candidate": "candidate_all_visual_supported_matrix.csv includes supported dashed/control routes only",
        },
    }
    with (RESULTS / "rounds_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with (RESULTS / "qa_summary.json").open("w", encoding="utf-8") as f:
        json.dump(qa, f, indent=2)


if __name__ == "__main__":
    build_artifacts()
