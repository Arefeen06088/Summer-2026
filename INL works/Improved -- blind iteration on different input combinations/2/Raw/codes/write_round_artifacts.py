from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[tuple[str, str]]
    chains: list[list[str]]
    notes: list[str]


NODE_NAMES = [
    "GRID-N501",
    "DS-N501",
    "TR-SU-1A",
    "CB-SU-1A",
    "GEN-EDG-A",
    "DS-DG-A",
    "CB-DG-A",
    "BUS-4160-A",
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

IDS = {name: f"n{idx:03d}" for idx, name in enumerate(NODE_NAMES, start=1)}
NODES = [(IDS[name], name) for name in NODE_NAMES]

BASE_CHAINS = [
    ["GRID-N501", "DS-N501", "TR-SU-1A", "CB-SU-1A", "BUS-4160-A"],
    ["GEN-EDG-A", "DS-DG-A", "CB-DG-A", "BUS-4160-A"],
    ["BUS-4160-A", "CB-TIE-4AB", "BUS-4160-B"],
    ["GRID-R502", "DS-R502", "TR-SU-1B", "CB-SU-1B", "BUS-4160-B"],
    ["GEN-EDG-B", "DS-DG-B", "CB-DG-B", "BUS-4160-B"],
    ["GEN-AAC-1", "DS-AAC-1", "CB-AAC-1", "BUS-4160-B"],
    ["BUS-4160-A", "CB-F11A", "TR-LC11A", "BUS-480-A1", "CB-M11A", "MCC-11A", "CB-P101A", "MTR-P101A", "PUMP-RHR-A"],
    ["BUS-4160-A", "CB-F12A", "TR-LC12A", "BUS-480-A2", "CB-M12A", "MCC-12A", "CB-P201A", "MTR-P201A", "PUMP-SI-A"],
    ["BUS-4160-A", "CB-F13A", "TR-LC13A", "BUS-480-A3", "CB-M13A", "MCC-13A", "CB-FAN-A", "MTR-FAN-A", "FAN-CAV-A"],
    ["BUS-4160-A", "CB-F14A", "TR-RPS-A", "BUS-208-A", "REC-125-A", "BUS-125DC-A"],
    ["BUS-125DC-A", "BAT-125-A"],
    ["BUS-125DC-A", "INV-120-A", "BUS-120AC-A", "CP-RPS-A"],
    ["CP-RPS-A", "RLY-K501A", "INST-NI501A"],
    ["BUS-4160-A", "CB-CVCS-A", "MCC-CVCS-A", "MTR-CVCS-A", "PUMP-CVCS-A", "VLV-LCV201A"],
    ["BUS-4160-B", "CB-F11B", "TR-LC11B", "BUS-480-B1", "CB-M11B", "MCC-11B", "CB-P101B", "MTR-P101B", "PUMP-RHR-B"],
    ["BUS-4160-B", "CB-F12B", "TR-LC12B", "BUS-480-B2", "CB-M12B", "MCC-12B", "CB-P201B", "MTR-P201B", "PUMP-SI-B"],
    ["BUS-4160-B", "CB-F13B", "TR-LC13B", "BUS-480-B3", "CB-M13B", "MCC-13B", "CB-FAN-B", "MTR-FAN-B", "FAN-CAV-B"],
    ["BUS-4160-B", "CB-F14B", "TR-RPS-B", "BUS-208-B", "REC-125-B", "BUS-125DC-B"],
    ["BUS-125DC-B", "BAT-125-B"],
    ["BUS-125DC-B", "INV-120-B", "BUS-120AC-B", "CP-RPS-B"],
    ["CP-RPS-B", "RLY-K501B", "INST-NI501B"],
    ["BUS-4160-B", "CB-CVCS-B", "MCC-CVCS-B", "MTR-CVCS-B", "PUMP-CVCS-B", "VLV-LCV201B"],
]

FINAL_CHAINS = [*BASE_CHAINS, ["CP-RPS-A", "CP-RPS-B"]]


def ids(chains: list[list[str]]) -> list[list[str]]:
    return [[IDS[name] for name in chain] for chain in chains]


ROUNDS = [
    RoundSpec(
        round_id="round_01",
        actor="diego",
        role="high_recall_extractor",
        nodes=NODES,
        chains=ids(BASE_CHAINS),
        notes=[
            "High-recall proposal from raw image only.",
            "Marked CP-RPS-A to CP-RPS-B as uncertain/plausible, not confirmed in this round matrix.",
        ],
    ),
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=NODES,
        chains=ids(FINAL_CHAINS),
        notes=[
            "Precision review from raw image only.",
            "Promoted CP-RPS-A to CP-RPS-B dashed route to confirmed control/signal edge.",
            "Confirmed CB-TIE-4AB as visible tie hardware; N.O. is an operating-state annotation.",
            "No uncertain edges retained.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor",
        nodes=NODES,
        chains=ids(FINAL_CHAINS),
        notes=[
            "Second high-recall pass after Jennifer's correction.",
            "Accepted CP-RPS-A to CP-RPS-B as confirmed dashed control/signal edge.",
            "No added or removed nodes; no uncertainty retained.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=NODES,
        chains=ids(FINAL_CHAINS),
        notes=[
            "Final precision review from raw image only.",
            "Confirmed saturation with Diego's round 02 extraction.",
            "Retained 100-node order and direct-adjacency edges only; no transitive closure.",
            "No uncertainty retained.",
        ],
    ),
]


def adjacent_edges(chains: list[list[str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    edges: list[tuple[str, str]] = []
    for chain in chains:
        for left, right in zip(chain, chain[1:]):
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
    path = RESULTS / f"{spec.round_id}_{spec.actor}_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target"])
        for left, right in edges:
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
        "Evidence source: raw schematic PNG only.",
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
                    len(adjacent_edges(spec.chains)),
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
                "- Tracking CSV records each extraction/review round, node count, edge count, and artifact prefix.",
                "- Agents used only the raw schematic image as extraction evidence; no GT or GT-derived feedback was used.",
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
        f"{prefix}_connectivity_matrix.csv": "final_connectivity_matrix.csv",
        f"{prefix}_notes.md": "final_notes.md",
    }
    for source, target in copies.items():
        shutil.copyfile(RESULTS / source, RESULTS / target)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for spec in ROUNDS:
        edges = adjacent_edges(spec.chains)
        write_node_map(spec)
        write_edges(spec, edges)
        write_matrix(spec, edges)
        write_notes(spec)
    update_tracking(ROUNDS)
    write_final_aliases(ROUNDS[-1])


if __name__ == "__main__":
    main()
