from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


NODES = [
    "GRID-N501",
    "DS-N501",
    "TR-SU-1A",
    "CB-SU-1A",
    "GEN-EDG-A",
    "DS-DG-A",
    "CB-DG-A",
    "BUS-4160-A",
    "CB-F11A",
    "TR-LC11A",
    "BUS-480-A1",
    "CB-M11A",
    "MCC-11A",
    "CB-P101A",
    "MTR-P101A",
    "PUMP-RHR-A",
    "CB-F12A",
    "TR-LC12A",
    "BUS-480-A2",
    "CB-M12A",
    "MCC-12A",
    "CB-P201A",
    "MTR-P201A",
    "PUMP-SI-A",
    "CB-F13A",
    "TR-LC13A",
    "BUS-480-A3",
    "CB-M13A",
    "MCC-13A",
    "CB-FAN-A",
    "MTR-FAN-A",
    "FAN-CAV-A",
    "CB-F14A",
    "TR-RPS-A",
    "BUS-208-A",
    "REC-125-A",
    "BUS-125DC-A",
    "BAT-125-A",
    "INV-120-A",
    "BUS-120AC-A",
    "CP-RPS-A",
    "RLY-K501A",
    "INST-NI501A",
    "CB-CVCS-A",
    "MCC-CVCS-A",
    "MTR-CVCS-A",
    "PUMP-CVCS-A",
    "VLV-LCV201A",
    "CB-TIE-4AB",
    "BUS-4160-B",
    "GRID-R502",
    "DS-R502",
    "TR-SU-1B",
    "CB-SU-1B",
    "GEN-EDG-B",
    "DS-DG-B",
    "CB-DG-B",
    "GEN-AAC-1",
    "DS-AAC-1",
    "CB-AAC-1",
    "CB-F11B",
    "TR-LC11B",
    "BUS-480-B1",
    "CB-M11B",
    "MCC-11B",
    "CB-P101B",
    "MTR-P101B",
    "PUMP-RHR-B",
    "CB-F12B",
    "TR-LC12B",
    "BUS-480-B2",
    "CB-M12B",
    "MCC-12B",
    "CB-P201B",
    "MTR-P201B",
    "PUMP-SI-B",
    "CB-F13B",
    "TR-LC13B",
    "BUS-480-B3",
    "CB-M13B",
    "MCC-13B",
    "CB-FAN-B",
    "MTR-FAN-B",
    "FAN-CAV-B",
    "CB-F14B",
    "TR-RPS-B",
    "BUS-208-B",
    "REC-125-B",
    "BUS-125DC-B",
    "BAT-125-B",
    "INV-120-B",
    "BUS-120AC-B",
    "CP-RPS-B",
    "RLY-K501B",
    "INST-NI501B",
    "CB-CVCS-B",
    "MCC-CVCS-B",
    "MTR-CVCS-B",
    "PUMP-CVCS-B",
    "VLV-LCV201B",
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
    names: list[str], edge_type: str, confidence: str, evidence: str
) -> list[dict[str, str]]:
    return [
        edge(a, b, edge_type, confidence, evidence)
        for a, b in zip(names, names[1:])
    ]


def solid_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += chain_edges(
        ["GRID-N501", "DS-N501", "TR-SU-1A", "CB-SU-1A", "BUS-4160-A"],
        "power_feeder",
        "high",
        "solid normal source feeder to Train A 4160 V bus",
    )
    edges += chain_edges(
        ["GEN-EDG-A", "DS-DG-A", "CB-DG-A", "BUS-4160-A"],
        "power_feeder",
        "high",
        "solid EDG-A feeder to Train A 4160 V bus",
    )
    edges += chain_edges(
        ["BUS-4160-A", "CB-F11A", "TR-LC11A", "BUS-480-A1", "CB-M11A", "MCC-11A", "CB-P101A", "MTR-P101A", "PUMP-RHR-A"],
        "power_feeder",
        "high",
        "solid RHR A feeder chain",
    )
    edges += chain_edges(
        ["BUS-4160-A", "CB-F12A", "TR-LC12A", "BUS-480-A2", "CB-M12A", "MCC-12A", "CB-P201A", "MTR-P201A", "PUMP-SI-A"],
        "power_feeder",
        "high",
        "solid SI A feeder chain",
    )
    edges += chain_edges(
        ["BUS-4160-A", "CB-F13A", "TR-LC13A", "BUS-480-A3", "CB-M13A", "MCC-13A", "CB-FAN-A", "MTR-FAN-A", "FAN-CAV-A"],
        "power_feeder",
        "high",
        "solid CAV A feeder chain",
    )
    edges += chain_edges(
        ["BUS-4160-A", "CB-F14A", "TR-RPS-A", "BUS-208-A", "REC-125-A", "BUS-125DC-A"],
        "power_dc",
        "high",
        "solid RPS/DC A feeder to 125 VDC bus",
    )
    edges.append(edge("BUS-125DC-A", "BAT-125-A", "power_dc", "high", "solid battery tie to BUS-125DC-A"))
    edges += chain_edges(
        ["BUS-125DC-A", "INV-120-A", "BUS-120AC-A", "CP-RPS-A"],
        "power_dc",
        "high",
        "solid inverter/120 VAC supply to CP-RPS-A",
    )
    edges += chain_edges(
        ["BUS-4160-A", "CB-CVCS-A", "MCC-CVCS-A", "MTR-CVCS-A", "PUMP-CVCS-A"],
        "power_feeder",
        "high",
        "solid CVCS A feeder chain",
    )

    edges += chain_edges(
        ["GRID-R502", "DS-R502", "TR-SU-1B", "CB-SU-1B", "BUS-4160-B"],
        "power_feeder",
        "high",
        "solid normal source feeder to Train B 4160 V bus",
    )
    edges += chain_edges(
        ["GEN-EDG-B", "DS-DG-B", "CB-DG-B", "BUS-4160-B"],
        "power_feeder",
        "high",
        "solid EDG-B feeder to Train B 4160 V bus",
    )
    edges += chain_edges(
        ["GEN-AAC-1", "DS-AAC-1", "CB-AAC-1", "BUS-4160-B"],
        "power_feeder",
        "high",
        "solid AAC feeder to Train B 4160 V bus",
    )
    edges += chain_edges(
        ["BUS-4160-B", "CB-F11B", "TR-LC11B", "BUS-480-B1", "CB-M11B", "MCC-11B", "CB-P101B", "MTR-P101B", "PUMP-RHR-B"],
        "power_feeder",
        "high",
        "solid RHR B feeder chain",
    )
    edges += chain_edges(
        ["BUS-4160-B", "CB-F12B", "TR-LC12B", "BUS-480-B2", "CB-M12B", "MCC-12B", "CB-P201B", "MTR-P201B", "PUMP-SI-B"],
        "power_feeder",
        "high",
        "solid SI B feeder chain",
    )
    edges += chain_edges(
        ["BUS-4160-B", "CB-F13B", "TR-LC13B", "BUS-480-B3", "CB-M13B", "MCC-13B", "CB-FAN-B", "MTR-FAN-B", "FAN-CAV-B"],
        "power_feeder",
        "high",
        "solid CAV B feeder chain",
    )
    edges += chain_edges(
        ["BUS-4160-B", "CB-F14B", "TR-RPS-B", "BUS-208-B", "REC-125-B", "BUS-125DC-B"],
        "power_dc",
        "high",
        "solid RPS/DC B feeder to 125 VDC bus",
    )
    edges.append(edge("BUS-125DC-B", "BAT-125-B", "power_dc", "high", "solid battery tie to BUS-125DC-B"))
    edges += chain_edges(
        ["BUS-125DC-B", "INV-120-B", "BUS-120AC-B", "CP-RPS-B"],
        "power_dc",
        "high",
        "solid inverter/120 VAC supply to CP-RPS-B",
    )
    edges += chain_edges(
        ["BUS-4160-B", "CB-CVCS-B", "MCC-CVCS-B", "MTR-CVCS-B", "PUMP-CVCS-B"],
        "power_feeder",
        "high",
        "solid CVCS B feeder chain",
    )
    return edges


TIE_EDGES = [
    edge("BUS-4160-A", "CB-TIE-4AB", "bus_tie", "high", "solid N.O. bus tie drawn as physical electrical link"),
    edge("CB-TIE-4AB", "BUS-4160-B", "bus_tie", "high", "solid N.O. bus tie drawn as physical electrical link"),
]

CONTROL_EDGES = [
    edge("CP-RPS-A", "RLY-K501A", "control_signal", "high", "dashed RPS A control/instrument link"),
    edge("RLY-K501A", "INST-NI501A", "control_signal", "high", "dashed RPS A control/instrument link"),
    edge("CP-RPS-B", "RLY-K501B", "control_signal", "high", "dashed RPS B control/instrument link"),
    edge("RLY-K501B", "INST-NI501B", "control_signal", "high", "dashed RPS B control/instrument link"),
    edge("CP-RPS-A", "CP-RPS-B", "control_signal", "high", "long dashed inter-panel control link"),
    edge("PUMP-CVCS-A", "VLV-LCV201A", "control_signal", "high", "dashed CVCS A pump-to-valve control link"),
    edge("PUMP-CVCS-B", "VLV-LCV201B", "control_signal", "high", "dashed CVCS B pump-to-valve control link"),
]

FINAL_EDGES = solid_edges() + TIE_EDGES + CONTROL_EDGES
SOLID_ONLY_EDGES = solid_edges()

EXCLUDED_CANDIDATES = [
    edge("BUS-4160-A", "BUS-4160-B", "excluded_transitive", "excluded", "bus tie represented through CB-TIE-4AB, not direct bus-bus edge"),
    edge("PUMP-CVCS-A", "CP-RPS-A", "excluded_crossing", "excluded", "no drawn terminating link between CVCS pump and RPS panel"),
    edge("PUMP-CVCS-B", "CP-RPS-B", "excluded_crossing", "excluded", "no drawn terminating link between CVCS pump and RPS panel"),
]


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
    if len(set(nodes)) != len(nodes):
        raise ValueError(f"{stem}: duplicate nodes")
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    missing = []
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
        raise ValueError(f"{stem}: missing edge endpoints {missing}")

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
    rounds = {
        "round1_diego": (NODES, FINAL_EDGES),
        "round1_jennifer": (NODES, FINAL_EDGES),
        "round2_diego": (NODES, FINAL_EDGES),
        "round2_jennifer": (NODES, FINAL_EDGES),
        "final": (NODES, FINAL_EDGES),
        "candidate_solid_power_only": (NODES, SOLID_ONLY_EDGES),
    }

    qa = {}
    for stem, (nodes, edges) in rounds.items():
        write_nodes(stem, nodes)
        write_edges(stem, edges, include_in_matrix=True)
        qa[stem] = write_matrix(stem, nodes, edges)

    write_edges("final_excluded_candidates", EXCLUDED_CANDIDATES, include_in_matrix=False)

    summary = {
        "document": 2,
        "resource_folder": str(ROOT),
        "main_decision": (
            "final_matrix.csv includes all drawn electrical links: solid feeders, "
            "the drawn N.O. bus tie through CB-TIE-4AB, and supported dashed "
            "control/instrument/permissive wiring. This follows notes 3 and 5."
        ),
        "agents": {
            "diego": {
                "id": "019f6dec-deb0-7660-8ef9-00f8fa716958",
                "model": "gpt-5.5",
                "role": "high-recall extractor",
            },
            "jennifer": {
                "id": "019f6df2-7ffd-7243-859a-d9ec07e2c201",
                "model": "gpt-5.5",
                "role": "precision reviewer/refiner",
            },
        },
        "rounds": {
            "round1_diego": "high-recall all-plausible extraction; tie/control edges tagged but included in all-drawn-link matrix",
            "round1_jennifer": "precision review confirmed all drawn electrical links are in scope and corrected labels/scope",
            "round2_diego": "reconciliation pass accepting Jennifer's scope and labels",
            "round2_jennifer": "final saturation confirmation",
        },
        "qa": qa,
        "edge_type_counts": {
            "solid_power_or_dc": len(SOLID_ONLY_EDGES),
            "bus_tie": len(TIE_EDGES),
            "control_signal": len(CONTROL_EDGES),
            "final_total": len(FINAL_EDGES),
        },
    }
    with (RESULTS / "rounds_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with (RESULTS / "qa_summary.json").open("w", encoding="utf-8") as f:
        json.dump(qa, f, indent=2)


if __name__ == "__main__":
    build_artifacts()
