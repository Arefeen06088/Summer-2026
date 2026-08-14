from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\1\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[tuple[str, str]]
    chains: list[list[str]]
    notes: list[str]


DIEGO_01_NODES = [
    ("c001", "BUS-4KV-A"),
    ("c002", "GRID-345A"),
    ("c003", "SWGR-52A"),
    ("c004", "RAT-1A"),
    ("c005", "MAIN-GEN-1"),
    ("c006", "GCB-1"),
    ("c007", "UAT-1A"),
    ("c008", "EDG-1A"),
    ("c009", "CB-EDG-A"),
    ("c010", "CB-4A-01"),
    ("c011", "TR-480A"),
    ("c012", "BUS-480-A"),
    ("c013", "CB-P201A"),
    ("c014", "MCC-01A"),
    ("c015", "RELAY-K201A"),
    ("c016", "PUMP-P201A"),
    ("c017", "CB-P202A"),
    ("c018", "MCC-02A"),
    ("c019", "RELAY-K202A"),
    ("c020", "PUMP-P202A"),
    ("c021", "CB-M301A"),
    ("c022", "MCC-03A"),
    ("c023", "RELAY-K301A"),
    ("c024", "MOTOR-FAN301A"),
    ("c025", "CB-V410A"),
    ("c026", "MCC-04A"),
    ("c027", "SOL-V410A"),
    ("c028", "VALVE-V410A"),
    ("c029", "CHG-125A"),
    ("c030", "BAT-125A"),
    ("c031", "BUS-125DC-A"),
    ("c032", "INV-120A"),
    ("c033", "BUS-120AC-A"),
    ("c034", "PNL-RPS-A"),
    ("c035", "RELAY-UV-A"),
    ("c036", "PT-A (circle)"),
    ("c037", "INSTR-PT-A"),
    ("c038", "CB-TIE-AB"),
    ("c039", "DS-TIE-AB"),
    ("c040", "BUS-4KV-B"),
    ("c041", "GRID-345B"),
    ("c042", "SWGR-52B"),
    ("c043", "RAT-1B"),
    ("c044", "EDG-1B"),
    ("c045", "CB-EDG-B"),
    ("c046", "CB-4B-01"),
    ("c047", "TR-480B"),
    ("c048", "BUS-480-B"),
    ("c049", "CB-P201B"),
    ("c050", "MCC-01B"),
    ("c051", "RELAY-K201B"),
    ("c052", "PUMP-P201B"),
    ("c053", "CB-P202B"),
    ("c054", "MCC-02B"),
    ("c055", "RELAY-K202B"),
    ("c056", "PUMP-P202B"),
    ("c057", "CB-M301B"),
    ("c058", "MCC-03B"),
    ("c059", "RELAY-K301B"),
    ("c060", "MOTOR-FAN301B"),
    ("c061", "CB-V410B"),
    ("c062", "MCC-04B"),
    ("c063", "SOL-V410B"),
    ("c064", "VALVE-V410B"),
    ("c065", "CHG-125B"),
    ("c066", "BAT-125B"),
    ("c067", "BUS-125DC-B"),
    ("c068", "INV-120B"),
    ("c069", "BUS-120AC-B"),
    ("c070", "PNL-RPS-B"),
    ("c071", "RELAY-UV-B"),
    ("c072", "PT-B (circle)"),
    ("c073", "INSTR-PT-B"),
    ("c074", "N.O. DC TIE"),
    ("c075", "CB-TIE-BC"),
    ("c076", "DS-TIE-BC"),
    ("c077", "BUS-4KV-C"),
    ("c078", "EDG-1C"),
    ("c079", "CB-EDG-C"),
    ("c080", "AAC-GEN-1"),
    ("c081", "CB-AAC-C"),
    ("c082", "CB-4C-01"),
    ("c083", "TR-480C"),
    ("c084", "BUS-480-C"),
    ("c085", "CB-P501"),
    ("c086", "MCC-05C"),
    ("c087", "RELAY-K501"),
    ("c088", "PUMP-CCW501"),
    ("c089", "CB-M601"),
    ("c090", "MCC-06C"),
    ("c091", "RELAY-K601"),
    ("c092", "MOTOR-HVAC601"),
    ("c093", "CB-V502"),
    ("c094", "MCC-07C"),
    ("c095", "SOL-V502"),
    ("c096", "VALVE-V502"),
    ("c097", "CB-P503"),
    ("c098", "MCC-08C"),
    ("c099", "RELAY-K503"),
    ("c100", "PUMP-SW503"),
]

DIEGO_01_CHAINS = [
    ["c002", "c003", "c004", "c001"],
    ["c005", "c006", "c007", "c001"],
    ["c008", "c009", "c001"],
    ["c001", "c010", "c011", "c012"],
    ["c012", "c013", "c014", "c015", "c016"],
    ["c012", "c017", "c018", "c019", "c020"],
    ["c012", "c021", "c022", "c023", "c024"],
    ["c012", "c025", "c026", "c027", "c028"],
    ["c012", "c029", "c030", "c031", "c032", "c033", "c034", "c035", "c036", "c037"],
    ["c001", "c038", "c039", "c040"],
    ["c041", "c042", "c043", "c040"],
    ["c044", "c045", "c040"],
    ["c040", "c046", "c047", "c048"],
    ["c048", "c049", "c050", "c051", "c052"],
    ["c048", "c053", "c054", "c055", "c056"],
    ["c048", "c057", "c058", "c059", "c060"],
    ["c048", "c061", "c062", "c063", "c064"],
    ["c048", "c065", "c066", "c067", "c068", "c069", "c070", "c071", "c072", "c073"],
    ["c031", "c074", "c067"],
    ["c040", "c075", "c076", "c077"],
    ["c078", "c079", "c077"],
    ["c080", "c081", "c077"],
    ["c077", "c082", "c083", "c084"],
    ["c084", "c085", "c086", "c087", "c088"],
    ["c084", "c089", "c090", "c091", "c092"],
    ["c084", "c093", "c094", "c095", "c096"],
    ["c084", "c097", "c098", "c099", "c100"],
]


ROUNDS = [
    RoundSpec(
        round_id="round_01",
        actor="diego",
        role="high_recall_extractor",
        nodes=DIEGO_01_NODES,
        chains=DIEGO_01_CHAINS,
        notes=[
            "High-recall proposal from raw image only.",
            "Includes normally-open bus/DC tie hardware or logical tie nodes as conditional edges.",
            "Known reviewer concern: visible CB-48A-01, CB-48B-01, and CB-48C-01 were omitted in this round.",
        ],
    )
]


JENNIFER_01_NODES = [
    *DIEGO_01_NODES[:12],
    ("c101", "CB-48A-01"),
    *DIEGO_01_NODES[12:48],
    ("c102", "CB-48B-01"),
    *DIEGO_01_NODES[48:84],
    ("c103", "CB-48C-01"),
    *DIEGO_01_NODES[84:],
]
JENNIFER_01_NODES = [node for node in JENNIFER_01_NODES if node[0] != "c074"]

JENNIFER_01_CHAINS = [
    ["c002", "c003", "c004", "c001"],
    ["c005", "c006", "c007", "c001"],
    ["c008", "c009", "c001"],
    ["c001", "c010", "c011", "c101", "c012"],
    ["c012", "c013", "c014", "c015", "c016"],
    ["c012", "c017", "c018", "c019", "c020"],
    ["c012", "c021", "c022", "c023", "c024"],
    ["c012", "c025", "c026", "c027", "c028"],
    ["c012", "c029", "c030", "c031", "c032", "c033", "c034", "c035", "c036", "c037"],
    ["c001", "c038", "c039", "c040"],
    ["c041", "c042", "c043", "c040"],
    ["c044", "c045", "c040"],
    ["c040", "c046", "c047", "c102", "c048"],
    ["c048", "c049", "c050", "c051", "c052"],
    ["c048", "c053", "c054", "c055", "c056"],
    ["c048", "c057", "c058", "c059", "c060"],
    ["c048", "c061", "c062", "c063", "c064"],
    ["c048", "c065", "c066", "c067", "c068", "c069", "c070", "c071", "c072", "c073"],
    ["c040", "c075", "c076", "c077"],
    ["c078", "c079", "c077"],
    ["c080", "c081", "c077"],
    ["c077", "c082", "c083", "c103", "c084"],
    ["c084", "c085", "c086", "c087", "c088"],
    ["c084", "c089", "c090", "c091", "c092"],
    ["c084", "c093", "c094", "c095", "c096"],
    ["c084", "c097", "c098", "c099", "c100"],
]

ROUNDS.append(
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=JENNIFER_01_NODES,
        chains=JENNIFER_01_CHAINS,
        notes=[
            "Precision review from raw image only.",
            "Added visible breakers CB-48A-01, CB-48B-01, and CB-48C-01.",
            "Removed confirmed node/edges for unboxed N.O. DC TIE; retained it only as uncertain note.",
            "Retained boxed normally-open 4 kV tie devices as visible nodes/edges.",
            "Uncertain, not encoded in confirmed matrix: BUS-125DC-A to BUS-125DC-B unboxed N.O. DC tie.",
        ],
    )
)


FINAL_NODE_NAMES = [
    "BUS-4KV-A",
    "GRID-345A",
    "SWGR-52A",
    "RAT-1A",
    "MAIN-GEN-1",
    "GCB-1",
    "UAT-1A",
    "EDG-1A",
    "CB-EDG-A",
    "CB-4A-01",
    "TR-480A",
    "CB-48A-01",
    "BUS-480-A",
    "CB-P201A",
    "MCC-01A",
    "RELAY-K201A",
    "PUMP-P201A",
    "CB-P202A",
    "MCC-02A",
    "RELAY-K202A",
    "PUMP-P202A",
    "CB-M301A",
    "MCC-03A",
    "RELAY-K301A",
    "MOTOR-FAN301A",
    "CB-V410A",
    "MCC-04A",
    "SOL-V410A",
    "VALVE-V410A",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "BUS-120AC-A",
    "PNL-RPS-A",
    "RELAY-UV-A",
    "PT-A",
    "INSTR-PT-A",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "BUS-4KV-B",
    "GRID-345B",
    "SWGR-52B",
    "RAT-1B",
    "EDG-1B",
    "CB-EDG-B",
    "CB-4B-01",
    "TR-480B",
    "CB-48B-01",
    "BUS-480-B",
    "CB-P201B",
    "MCC-01B",
    "RELAY-K201B",
    "PUMP-P201B",
    "CB-P202B",
    "MCC-02B",
    "RELAY-K202B",
    "PUMP-P202B",
    "CB-M301B",
    "MCC-03B",
    "RELAY-K301B",
    "MOTOR-FAN301B",
    "CB-V410B",
    "MCC-04B",
    "SOL-V410B",
    "VALVE-V410B",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "BUS-120AC-B",
    "PNL-RPS-B",
    "RELAY-UV-B",
    "PT-B",
    "INSTR-PT-B",
    "CB-TIE-BC",
    "DS-TIE-BC",
    "BUS-4KV-C",
    "EDG-1C",
    "CB-EDG-C",
    "AAC-GEN-1",
    "CB-AAC-C",
    "CB-4C-01",
    "TR-480C",
    "CB-48C-01",
    "BUS-480-C",
    "CB-P501",
    "MCC-05C",
    "RELAY-K501",
    "PUMP-CCW501",
    "CB-M601",
    "MCC-06C",
    "RELAY-K601",
    "MOTOR-HVAC601",
    "CB-V502",
    "MCC-07C",
    "SOL-V502",
    "VALVE-V502",
    "CB-P503",
    "MCC-08C",
    "RELAY-K503",
    "PUMP-SW503",
]

FINAL_NODE_IDS = {name: f"f{idx:03d}" for idx, name in enumerate(FINAL_NODE_NAMES, start=1)}
FINAL_NODES = [(FINAL_NODE_IDS[name], name) for name in FINAL_NODE_NAMES]

FINAL_CHAIN_NAMES = [
    ["GRID-345A", "SWGR-52A", "RAT-1A", "BUS-4KV-A"],
    ["MAIN-GEN-1", "GCB-1", "UAT-1A", "BUS-4KV-A"],
    ["EDG-1A", "CB-EDG-A", "BUS-4KV-A"],
    ["BUS-4KV-A", "CB-4A-01", "TR-480A", "CB-48A-01", "BUS-480-A"],
    ["BUS-480-A", "CB-P201A", "MCC-01A", "RELAY-K201A", "PUMP-P201A"],
    ["BUS-480-A", "CB-P202A", "MCC-02A", "RELAY-K202A", "PUMP-P202A"],
    ["BUS-480-A", "CB-M301A", "MCC-03A", "RELAY-K301A", "MOTOR-FAN301A"],
    ["BUS-480-A", "CB-V410A", "MCC-04A", "SOL-V410A", "VALVE-V410A"],
    ["BUS-480-A", "CHG-125A", "BAT-125A", "BUS-125DC-A", "INV-120A", "BUS-120AC-A"],
    ["BUS-120AC-A", "PNL-RPS-A", "RELAY-UV-A", "PT-A", "INSTR-PT-A"],
    ["BUS-4KV-A", "CB-TIE-AB", "DS-TIE-AB", "BUS-4KV-B"],
    ["GRID-345B", "SWGR-52B", "RAT-1B", "BUS-4KV-B"],
    ["EDG-1B", "CB-EDG-B", "BUS-4KV-B"],
    ["BUS-4KV-B", "CB-4B-01", "TR-480B", "CB-48B-01", "BUS-480-B"],
    ["BUS-480-B", "CB-P201B", "MCC-01B", "RELAY-K201B", "PUMP-P201B"],
    ["BUS-480-B", "CB-P202B", "MCC-02B", "RELAY-K202B", "PUMP-P202B"],
    ["BUS-480-B", "CB-M301B", "MCC-03B", "RELAY-K301B", "MOTOR-FAN301B"],
    ["BUS-480-B", "CB-V410B", "MCC-04B", "SOL-V410B", "VALVE-V410B"],
    ["BUS-480-B", "CHG-125B", "BAT-125B", "BUS-125DC-B", "INV-120B", "BUS-120AC-B"],
    ["BUS-120AC-B", "PNL-RPS-B", "RELAY-UV-B", "PT-B", "INSTR-PT-B"],
    ["BUS-4KV-B", "CB-TIE-BC", "DS-TIE-BC", "BUS-4KV-C"],
    ["EDG-1C", "CB-EDG-C", "BUS-4KV-C"],
    ["AAC-GEN-1", "CB-AAC-C", "BUS-4KV-C"],
    ["BUS-4KV-C", "CB-4C-01", "TR-480C", "CB-48C-01", "BUS-480-C"],
    ["BUS-480-C", "CB-P501", "MCC-05C", "RELAY-K501", "PUMP-CCW501"],
    ["BUS-480-C", "CB-M601", "MCC-06C", "RELAY-K601", "MOTOR-HVAC601"],
    ["BUS-480-C", "CB-V502", "MCC-07C", "SOL-V502", "VALVE-V502"],
    ["BUS-480-C", "CB-P503", "MCC-08C", "RELAY-K503", "PUMP-SW503"],
]
FINAL_CHAINS = [[FINAL_NODE_IDS[name] for name in chain] for chain in FINAL_CHAIN_NAMES]

ROUNDS.append(
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor",
        nodes=FINAL_NODES,
        chains=FINAL_CHAINS,
        notes=[
            "Diego agreed with Jennifer's visual corrections.",
            "Visible CB-48A-01, CB-48B-01, and CB-48C-01 are included between transformer and 480 V bus.",
            "Uncertain, not encoded in confirmed matrix: BUS-125DC-A to BUS-125DC-B unboxed N.O. DC tie.",
            "PT-A and PT-B are disambiguated extraction names; visible circle labels read PT.",
        ],
    )
)

ROUNDS.append(
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=FINAL_NODES,
        chains=FINAL_CHAINS,
        notes=[
            "Jennifer confirmed saturation/agreement with Diego round 2.",
            "Visible CB-48A-01, CB-48B-01, and CB-48C-01 are included between transformer and 480 V bus.",
            "Boxed normally-open 4 kV tie devices are retained as visible nodes/edges.",
            "Uncertain, excluded from confirmed matrix: BUS-125DC-A to BUS-125DC-B unboxed N.O. DC tie.",
            "PT-A and PT-B are disambiguated extraction names; visible circle labels read PT.",
        ],
    )
)


def adjacent_edges(chains: list[list[str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    edges: list[tuple[str, str]] = []
    for chain in chains:
        for left, right in zip(chain, chain[1:]):
            edge = tuple(sorted((left, right)))
            if edge not in seen:
                seen.add(edge)
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
    ids = [node_id for node_id, _ in spec.nodes]
    names = [name for _, name in spec.nodes]
    index = {node_id: idx for idx, node_id in enumerate(ids)}
    matrix = [[0 for _ in ids] for _ in ids]
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
    lines = [
        "# Token Performance Notes",
        "",
        "- No Codex goal token budget was active, so exact token telemetry was not available from the environment.",
        "- Tracking CSV records each extraction/review round, node count, edge count, and artifact prefix.",
        "- Agents used only the raw schematic image as extraction evidence; no GT or GT-derived feedback was used.",
        "",
    ]
    note_path.write_text("\n".join(lines), encoding="utf-8")


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
