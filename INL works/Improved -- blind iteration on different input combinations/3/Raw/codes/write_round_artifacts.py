from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\3\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[tuple[str, str]]
    chains: list[list[str]]
    extra_edges: list[tuple[str, str]]
    uncertain_edges: list[tuple[str, str]]
    notes: list[str]


NODE_NAMES = [
    "GRID-1",
    "AUX-TR-1A",
    "CB-101",
    "BUS-416A",
    "BUS-TIE-41",
    "BUS-416B",
    "CB-102",
    "AUX-TR-1B",
    "GRID-2",
    "EDG-1A",
    "CB-DG1A",
    "TR-480A1",
    "CB-480A1",
    "MCC-480A1",
    "TR-480A2",
    "CB-480A2",
    "MCC-480A2",
    "TR-480B1",
    "CB-480B1",
    "MCC-480B1",
    "TR-480B2",
    "CB-480B2",
    "MCC-480B2",
    "EDG-1B",
    "CB-DG1B",
    "GND-1E",
    "CB-CHG-A",
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-A",
    "INV-120A",
    "BUS-120A",
    "CB-CHG-B",
    "CHGR-125B",
    "BAT-125B",
    "DC-BUS-B",
    "INV-120B",
    "BUS-120B",
    "FDB-A1",
    "CB-SI-A1",
    "PUMP-SI-A1",
    "CB-RHR-A1",
    "PUMP-RHR-A1",
    "CB-CCW-A1",
    "PUMP-CCW-A1",
    "CB-FAN-A1",
    "FAN-CR-A1",
    "CB-MOV-A101",
    "VALVE-SI-A101",
    "CB-MOV-A102",
    "VALVE-RHR-A102",
    "FDB-A2",
    "CB-CS-A2",
    "PUMP-CS-A2",
    "CB-SW-A2",
    "PUMP-SW-A2",
    "CB-AFW-A2",
    "PUMP-AFW-A2",
    "CB-FAN-A2",
    "FAN-EB-A2",
    "CB-MOV-A201",
    "VALVE-CCW-A201",
    "CB-HTR-A2",
    "HTR-BAY-A2",
    "FDB-B1",
    "CB-SI-B1",
    "PUMP-SI-B1",
    "CB-RHR-B1",
    "PUMP-RHR-B1",
    "CB-CCW-B1",
    "PUMP-CCW-B1",
    "CB-FAN-B1",
    "FAN-CR-B1",
    "CB-MOV-B101",
    "VALVE-SI-B101",
    "CB-MOV-B102",
    "VALVE-RHR-B102",
    "FDB-B2",
    "CB-CS-B2",
    "PUMP-CS-B2",
    "CB-SW-B2",
    "PUMP-SW-B2",
    "CB-FAN-B2",
    "FAN-EB-B2",
    "CB-MOV-B201",
    "VALVE-CCW-B201",
    "CB-HTR-B2",
    "HTR-BAY-B2",
    "INST-PT-A",
    "INST-LT-A",
    "RELAY-K27A",
    "PANEL-RPS-A",
    "PANEL-ESF-A",
    "JB-A401",
    "INST-PT-B",
    "INST-LT-B",
    "RELAY-K27B",
    "PANEL-RPS-B",
    "PANEL-ESF-B",
    "JB-B501",
]

IDS = {name: f"n{idx:03d}" for idx, name in enumerate(NODE_NAMES, start=1)}
NODES = [(IDS[name], name) for name in NODE_NAMES]

FIRM_CHAINS = [
    ["GRID-1", "AUX-TR-1A", "CB-101", "BUS-416A", "BUS-TIE-41", "BUS-416B", "CB-102", "AUX-TR-1B", "GRID-2"],
    ["EDG-1A", "CB-DG1A", "BUS-416A"],
    ["BUS-416B", "CB-DG1B", "EDG-1B"],
    ["BUS-416A", "TR-480A1", "CB-480A1", "MCC-480A1", "FDB-A1"],
    ["BUS-416A", "TR-480A2", "CB-480A2", "MCC-480A2", "FDB-A2"],
    ["BUS-416B", "TR-480B1", "CB-480B1", "MCC-480B1", "FDB-B1"],
    ["BUS-416B", "TR-480B2", "CB-480B2", "MCC-480B2", "FDB-B2"],
    ["BUS-416A", "CB-CHG-A", "CHGR-125A", "DC-BUS-A", "INV-120A", "BUS-120A"],
    ["BAT-125A", "DC-BUS-A"],
    ["BUS-416B", "CB-CHG-B", "CHGR-125B", "DC-BUS-B", "INV-120B", "BUS-120B"],
    ["BAT-125B", "DC-BUS-B"],
    ["FDB-A1", "CB-SI-A1", "PUMP-SI-A1"],
    ["FDB-A1", "CB-RHR-A1", "PUMP-RHR-A1"],
    ["FDB-A1", "CB-CCW-A1", "PUMP-CCW-A1"],
    ["FDB-A1", "CB-FAN-A1", "FAN-CR-A1"],
    ["FDB-A1", "CB-MOV-A101", "VALVE-SI-A101"],
    ["FDB-A1", "CB-MOV-A102", "VALVE-RHR-A102"],
    ["FDB-A2", "CB-CS-A2", "PUMP-CS-A2"],
    ["FDB-A2", "CB-SW-A2", "PUMP-SW-A2"],
    ["FDB-A2", "CB-AFW-A2", "PUMP-AFW-A2"],
    ["FDB-A2", "CB-FAN-A2", "FAN-EB-A2"],
    ["FDB-A2", "CB-MOV-A201", "VALVE-CCW-A201"],
    ["FDB-A2", "CB-HTR-A2", "HTR-BAY-A2"],
    ["FDB-B1", "CB-SI-B1", "PUMP-SI-B1"],
    ["FDB-B1", "CB-RHR-B1", "PUMP-RHR-B1"],
    ["FDB-B1", "CB-CCW-B1", "PUMP-CCW-B1"],
    ["FDB-B1", "CB-FAN-B1", "FAN-CR-B1"],
    ["FDB-B1", "CB-MOV-B101", "VALVE-SI-B101"],
    ["FDB-B1", "CB-MOV-B102", "VALVE-RHR-B102"],
    ["FDB-B2", "CB-CS-B2", "PUMP-CS-B2"],
    ["FDB-B2", "CB-SW-B2", "PUMP-SW-B2"],
    ["FDB-B2", "CB-FAN-B2", "FAN-EB-B2"],
    ["FDB-B2", "CB-MOV-B201", "VALVE-CCW-B201"],
    ["FDB-B2", "CB-HTR-B2", "HTR-BAY-B2"],
    ["BUS-120A", "PANEL-RPS-A"],
    ["INST-PT-A", "PANEL-RPS-A"],
    ["INST-LT-A", "PANEL-RPS-A"],
    ["RELAY-K27A", "PANEL-RPS-A"],
    ["RELAY-K27A", "PANEL-ESF-A", "JB-A401"],
    ["BUS-120B", "PANEL-RPS-B"],
    ["INST-PT-B", "PANEL-RPS-B"],
    ["INST-LT-B", "PANEL-RPS-B"],
    ["RELAY-K27B", "PANEL-RPS-B"],
    ["RELAY-K27B", "PANEL-ESF-B", "JB-B501"],
]

GROUND_EDGES = [
    ("GND-1E", "BUS-416A"),
    ("GND-1E", "BUS-416B"),
]


def ids(chains: list[list[str]]) -> list[list[str]]:
    return [[IDS[name] for name in chain] for chain in chains]


def edge_ids(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(IDS[left], IDS[right]) for left, right in edges]


ROUNDS = [
    RoundSpec(
        round_id="round_01",
        actor="diego",
        role="high_recall_extractor",
        nodes=NODES,
        chains=ids(FIRM_CHAINS),
        extra_edges=edge_ids(GROUND_EDGES),
        uncertain_edges=edge_ids(GROUND_EDGES),
        notes=[
            "High-recall extraction from raw PNG only.",
            "Included two visually plausible GND-1E ground-reference edges in the proposed matrix.",
            "Marked GND-1E to BUS-416A and GND-1E to BUS-416B as uncertain pending precision review.",
        ],
    ),
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=NODES,
        chains=ids(FIRM_CHAINS),
        extra_edges=edge_ids(GROUND_EDGES),
        uncertain_edges=[],
        notes=[
            "Precision review from raw PNG and raw-derived crops only.",
            "Confirmed GND-1E as a node and confirmed its two ground-reference edges to BUS-416A and BUS-416B.",
            "Rejected additional BUS-120A to BUS-120B, PANEL-RPS-A to PANEL-RPS-B, and riser cross-edges.",
            "No uncertainty retained.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor",
        nodes=NODES,
        chains=ids(FIRM_CHAINS),
        extra_edges=edge_ids(GROUND_EDGES),
        uncertain_edges=[],
        notes=[
            "Second high-recall pass after Jennifer's correction.",
            "Agreed with confirming the two GND-1E ground-reference edges.",
            "Retained no BUS-120A to BUS-120B, PANEL-RPS-A to PANEL-RPS-B, or additional riser cross-edge.",
            "Saturation reached from Diego's side.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=NODES,
        chains=ids(FIRM_CHAINS),
        extra_edges=edge_ids(GROUND_EDGES),
        uncertain_edges=[],
        notes=[
            "Final precision review after Diego round 02.",
            "Confirmed the same 100-node order and same 100 direct undirected edges.",
            "Confirmed GND-1E to BUS-416A and GND-1E to BUS-416B.",
            "Excluded BUS-120A to BUS-120B, PANEL-RPS-A to PANEL-RPS-B, extra riser cross-edges, and crossings without terminal dots.",
            "No uncertainty retained.",
        ],
    ),
]


def adjacent_edges(chains: list[list[str]], extra_edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    edges: list[tuple[str, str]] = []
    for chain in chains:
        for left, right in zip(chain, chain[1:]):
            key = tuple(sorted((left, right)))
            if key not in seen:
                seen.add(key)
                edges.append((left, right))
    for left, right in extra_edges:
        key = tuple(sorted((left, right)))
        if key not in seen:
            seen.add(key)
            edges.append((left, right))
    return edges


def write_node_map(spec: RoundSpec) -> None:
    path = RESULTS / f"{spec.round_id}_{spec.actor}_node_map.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "node"])
        writer.writerows(spec.nodes)


def write_edges(spec: RoundSpec, edges: list[tuple[str, str]]) -> None:
    id_to_name = dict(spec.nodes)
    uncertain = {tuple(sorted(edge)) for edge in spec.uncertain_edges}
    path = RESULTS / f"{spec.round_id}_{spec.actor}_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target", "status"])
        for left, right in edges:
            status = "uncertain" if tuple(sorted((left, right))) in uncertain else "confirmed"
            writer.writerow([left, id_to_name[left], right, id_to_name[right], status])


def write_uncertain_edges(spec: RoundSpec) -> None:
    id_to_name = dict(spec.nodes)
    path = RESULTS / f"{spec.round_id}_{spec.actor}_uncertain_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target"])
        for left, right in spec.uncertain_edges:
            writer.writerow([left, id_to_name[left], right, id_to_name[right]])


def write_matrix(spec: RoundSpec, edges: list[tuple[str, str]]) -> None:
    node_ids = [node_id for node_id, _ in spec.nodes]
    names = [name for _, name in spec.nodes]
    index = {node_id: idx for idx, node_id in enumerate(node_ids)}
    matrix = [[0 for _ in node_ids] for _ in node_ids]
    for left, right in edges:
        i = index[left]
        j = index[right]
        matrix[i][j] = 1
        matrix[j][i] = 1

    path = RESULTS / f"{spec.round_id}_{spec.actor}_connectivity_matrix.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *names])
        for name, row in zip(names, matrix):
            writer.writerow([name, *row])


def write_notes(spec: RoundSpec) -> None:
    path = RESULTS / f"{spec.round_id}_{spec.actor}_notes.md"
    lines = [
        f"# {spec.round_id} {spec.actor.title()}",
        "",
        f"Role: {spec.role}",
        "",
        "Evidence source: raw schematic PNG and crops generated only from that PNG.",
        "",
        "Notes:",
    ]
    lines.extend(f"- {note}" for note in spec.notes)
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def update_tracking(specs: list[RoundSpec]) -> None:
    csv_path = RESULTS / "token_performance_tracking.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp_local",
                "round_id",
                "actor",
                "role",
                "node_count",
                "edge_count",
                "uncertain_edge_count",
                "token_telemetry",
                "artifact_prefix",
            ]
        )
        for spec in specs:
            writer.writerow(
                [
                    datetime.now().isoformat(timespec="seconds"),
                    spec.round_id,
                    spec.actor,
                    spec.role,
                    len(spec.nodes),
                    len(adjacent_edges(spec.chains, spec.extra_edges)),
                    len(spec.uncertain_edges),
                    "not available from current goal telemetry",
                    f"{spec.round_id}_{spec.actor}",
                ]
            )

    note_path = RESULTS / "token_performance_notes.md"
    note_path.write_text(
        "\n".join(
            [
                "# Token Performance Notes",
                "",
                "- No Codex goal token budget was active, so exact token telemetry was not available from the environment.",
                "- Tracking CSV records each extraction/review round, node count, edge count, uncertainty count, and artifact prefix.",
                "- Agents used only the raw schematic image and crops generated from it; no GT or GT-derived feedback was used.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_final_aliases(spec: RoundSpec) -> None:
    prefix = f"{spec.round_id}_{spec.actor}"
    copies = {
        f"{prefix}_node_map.csv": "final_node_map.csv",
        f"{prefix}_edges.csv": "final_edges.csv",
        f"{prefix}_uncertain_edges.csv": "final_uncertain_edges.csv",
        f"{prefix}_connectivity_matrix.csv": "final_connectivity_matrix.csv",
        f"{prefix}_notes.md": "final_notes.md",
    }
    for source, target in copies.items():
        shutil.copyfile(RESULTS / source, RESULTS / target)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for spec in ROUNDS:
        edges = adjacent_edges(spec.chains, spec.extra_edges)
        write_node_map(spec)
        write_edges(spec, edges)
        write_uncertain_edges(spec)
        write_matrix(spec, edges)
        write_notes(spec)
    update_tracking(ROUNDS)
    write_final_aliases(ROUNDS[-1])


if __name__ == "__main__":
    main()
