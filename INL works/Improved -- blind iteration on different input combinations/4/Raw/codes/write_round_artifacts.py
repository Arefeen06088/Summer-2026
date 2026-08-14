from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\4\Raw")
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
    "US-345A",
    "CB-UAT-A",
    "TR-UAT-1",
    "CB-IN-A",
    "EDG-1A",
    "CB-DG-A",
    "BUS-480-RB1",
    "US-230B",
    "CB-SAT-B",
    "TR-SAT-2",
    "CB-IN-B",
    "EDG-1B",
    "CB-DG-B",
    "BUS-480-RB2",
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
    "GND-NG-A",
    "CB-LC-A2",
    "BUS-480-LCA",
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
    "CB-CHG-A",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DCA",
    "INV-120A",
    "BUS-UPS-A",
    "RPS-TRAIN-A",
    "ESFAS-TRAIN-A",
    "ANN-CP-A",
    "RELAY-K701",
    "TB-ESF-A",
    "CB-CHG-B",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DCB",
    "INV-120B",
    "BUS-UPS-B",
    "RPS-TRAIN-B",
    "ESFAS-TRAIN-B",
    "REC-SER-01",
    "RELAY-K702",
    "TB-ESF-B",
    "CB-LC-B",
    "TR-LC-B",
    "GND-NG-B",
    "CB-LC-B2",
    "BUS-480-LCB",
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
]

IDS = {name: f"n{idx:03d}" for idx, name in enumerate(NODE_NAMES, start=1)}
NODES = [(IDS[name], name) for name in NODE_NAMES]

BASE_CHAINS = [
    ["US-345A", "CB-UAT-A", "TR-UAT-1", "CB-IN-A", "BUS-480-RB1"],
    ["EDG-1A", "CB-DG-A", "BUS-480-RB1"],
    ["US-230B", "CB-SAT-B", "TR-SAT-2", "CB-IN-B", "BUS-480-RB2"],
    ["EDG-1B", "CB-DG-B", "BUS-480-RB2"],
    ["BUS-480-RB1", "CB-TIE-480", "BUS-480-RB2"],
    ["BUS-480-RB1", "CB-F101", "OL-F101", "PMP-SI-1A"],
    ["BUS-480-RB2", "CB-F102", "OL-F102", "PMP-RHR-1A"],
    ["BUS-480-RB1", "CB-F103", "OL-F103", "FAN-CTMT-1A"],
    ["BUS-480-RB2", "CB-F104", "OL-F104", "MOV-RC-104"],
    ["BUS-480-RB1", "CB-F105", "OL-F105", "PMP-CCW-1A"],
    ["BUS-480-RB2", "CB-F106", "OL-F106", "MOV-IA-106"],
    ["BUS-480-RB1", "CB-F107", "OL-F107", "FAN-AHU-1A"],
    ["BUS-480-RB2", "CB-F108", "OL-F108", "PMP-CS-1A"],
    ["BUS-480-RB1", "CB-F109", "OL-F109", "MOV-EF-109"],
    ["BUS-480-RB2", "CB-F110", "OL-F110", "HTR-PZR-1"],
    ["BUS-480-RB1", "CB-F111", "OL-F111", "PMP-SI-1B"],
    ["BUS-480-RB2", "CB-F112", "OL-F112", "PMP-RHR-1B"],
    ["BUS-480-RB1", "CB-F113", "OL-F113", "FAN-CTMT-1B"],
    ["BUS-480-RB2", "CB-F114", "OL-F114", "MOV-RC-114"],
    ["BUS-480-RB1", "CB-F115", "OL-F115", "PNL-SPARE-F15"],
    ["BUS-480-RB1", "CB-LC-A", "TR-LC-A", "CB-LC-A2", "BUS-480-LCA"],
    ["TR-LC-A", "GND-NG-A"],
    ["BUS-480-RB2", "CB-LC-B", "TR-LC-B", "CB-LC-B2", "BUS-480-LCB"],
    ["TR-LC-B", "GND-NG-B"],
    ["BUS-480-LCA", "CB-LC-TIE", "BUS-480-LCB"],
    ["BUS-480-LCA", "CB-A201", "OL-201", "PMP-SW-2A"],
    ["BUS-480-LCA", "CB-A202", "OL-202", "PMP-CVC-2A"],
    ["BUS-480-LCA", "CB-A203", "OL-203", "MOV-SI-203"],
    ["BUS-480-LCA", "CB-A204", "OL-204", "FAN-CR-2A"],
    ["BUS-480-LCA", "CB-A205", "OL-205", "HTR-BATT-A"],
    ["BUS-480-LCA", "CB-CHG-A", "CHG-125A", "BUS-125DCA"],
    ["BUS-125DCA", "BAT-125A"],
    ["BUS-125DCA", "INV-120A", "BUS-UPS-A"],
    ["BUS-UPS-A", "RPS-TRAIN-A"],
    ["BUS-UPS-A", "ESFAS-TRAIN-A"],
    ["BUS-480-LCB", "CB-CHG-B", "CHG-125B", "BUS-125DCB"],
    ["BUS-125DCB", "BAT-125B"],
    ["BUS-125DCB", "INV-120B", "BUS-UPS-B"],
    ["BUS-UPS-B", "RPS-TRAIN-B"],
    ["BUS-UPS-B", "ESFAS-TRAIN-B"],
    ["BUS-480-LCB", "CB-B206", "OL-206", "PMP-SW-2B"],
    ["BUS-480-LCB", "CB-B207", "OL-207", "PMP-CVC-2B"],
    ["BUS-480-LCB", "CB-B208", "OL-208", "MOV-SI-208"],
    ["BUS-480-LCB", "CB-B209", "OL-209", "PNL-LTG-209"],
]

CONTROL_EDGES = [
    ("RPS-TRAIN-A", "RELAY-K701"),
    ("ESFAS-TRAIN-A", "RELAY-K701"),
    ("RELAY-K701", "TB-ESF-A"),
    ("ANN-CP-A", "TB-ESF-A"),
    ("ANN-CP-A", "REC-SER-01"),
    ("RPS-TRAIN-B", "RELAY-K702"),
    ("ESFAS-TRAIN-B", "RELAY-K702"),
    ("RELAY-K702", "TB-ESF-B"),
    ("REC-SER-01", "TB-ESF-B"),
]

DIEGO_R1_UNCERTAIN = [
    ("BUS-480-LCA", "CB-CHG-A"),
    ("RELAY-K701", "CB-LC-B"),
    ("RELAY-K702", "CB-LC-B2"),
    ("TB-ESF-A", "TB-ESF-B"),
]

FINAL_UNCERTAIN = [
    ("TB-ESF-A", "TB-ESF-B"),
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
        chains=ids(BASE_CHAINS),
        extra_edges=edge_ids(CONTROL_EDGES + DIEGO_R1_UNCERTAIN[1:]),
        uncertain_edges=edge_ids(DIEGO_R1_UNCERTAIN),
        notes=[
            "High-recall extraction from raw PNG only.",
            "Included all visually plausible dashed/control edges in the round matrix.",
            "Marked relay-to-breaker edges, TB-ESF-A to TB-ESF-B, and the A charger tap as uncertain.",
            "The supplied resource path named 3\\R4w did not exist; used 4\\Raw\\raw.png matching the requested output folders.",
        ],
    ),
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=NODES,
        chains=ids(BASE_CHAINS),
        extra_edges=edge_ids(CONTROL_EDGES),
        uncertain_edges=edge_ids(FINAL_UNCERTAIN),
        notes=[
            "Precision review from raw PNG and crops generated from that PNG.",
            "Confirmed BUS-480-LCA to CB-CHG-A as solid L-shaped feed.",
            "Rejected RELAY-K701 to CB-LC-B and RELAY-K702 to CB-LC-B2.",
            "Kept TB-ESF-A to TB-ESF-B uncertain and excluded it from the confirmed matrix.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor",
        nodes=NODES,
        chains=ids(BASE_CHAINS),
        extra_edges=edge_ids(CONTROL_EDGES),
        uncertain_edges=edge_ids(FINAL_UNCERTAIN),
        notes=[
            "Second high-recall pass after Jennifer's correction.",
            "Agreed with confirming BUS-480-LCA to CB-CHG-A.",
            "Agreed to exclude RELAY-K701 to CB-LC-B, RELAY-K702 to CB-LC-B2, and TB-ESF-A to TB-ESF-B from the confirmed matrix.",
            "Retained TB-ESF-A to TB-ESF-B only as an uncertainty outside the matrix.",
            "Saturation reached from Diego's side.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=NODES,
        chains=ids(BASE_CHAINS),
        extra_edges=edge_ids(CONTROL_EDGES),
        uncertain_edges=edge_ids(FINAL_UNCERTAIN),
        notes=[
            "Final precision review after Diego round 02.",
            "Confirmed unchanged 120-node order and 123 confirmed direct undirected edges.",
            "Confirmed BUS-480-LCA to CB-CHG-A and the nine dashed/control edges.",
            "Excluded RELAY-K701 to CB-LC-B, RELAY-K702 to CB-LC-B2, and TB-ESF-A to TB-ESF-B from the confirmed matrix.",
            "Final remaining uncertainty is TB-ESF-A to TB-ESF-B, omitted from the matrix.",
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
        writer.writerow(["source_id", "source", "target_id", "target", "included_in_matrix"])
        matrix_edges = {tuple(sorted(edge)) for edge in adjacent_edges(spec.chains, spec.extra_edges)}
        for left, right in spec.uncertain_edges:
            included = tuple(sorted((left, right))) in matrix_edges
            writer.writerow([left, id_to_name[left], right, id_to_name[right], int(included)])


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
                "- The user-supplied resource path `3\\R4w` was not present; extraction used `4\\Raw\\raw.png`, which matches the requested code/results paths.",
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
