from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[str]
    chains: list[list[str]]
    extra_edges: list[tuple[str, str]]
    uncertain_edges: list[tuple[str, str]]
    notes: list[str]


FINAL_NODES = [
    "GRID-N230", "ISO-230A", "BRK-2301", "BUS-SY230", "GEN-G101", "GSU-1",
    "BRK-2302", "ISO-230B", "GRID-S230", "TR-RAT-1A", "CB-AUX-A",
    "TR-UAT-1A", "TR-UAT-1B", "CB-AUX-B", "TR-RAT-1B", "BUS-AUX13A",
    "CB-TIE13", "BUS-AUX13B", "BUS-NON1", "EDG-A", "CB-EDG-A",
    "TR-SAF-A", "CB-SAF-A", "BUS-416A", "TR-480-A", "CB-LC-A",
    "LC-480A", "CB-MCCA1", "MCC-1A1", "PUMP-AFW-A", "CB-MCCA2",
    "MCC-1A2", "PUMP-CCW-A", "VLV-MSIV-A", "XFER-ATS-A", "CHG-125A",
    "BAT-125A", "PNL-DC-A", "UPS-PNL-A", "INV-UPS-A", "RECT-48V-A",
    "BAT-48V-A", "JB-RLY-A", "EDG-B", "CB-EDG-B", "TR-SAF-B",
    "CB-SAF-B", "BUS-416B", "TR-480-B", "CB-LC-B", "LC-480B",
    "CB-MCCB1", "MCC-1B1", "PUMP-AFW-B", "CB-MCCB2", "MCC-1B2",
    "PUMP-CCW-B", "VLV-MSIV-B", "CB-TIE-AB", "EDG-C", "CB-EDG-C",
    "TR-SAF-C", "CB-SAF-C", "BUS-416C", "TR-480-C", "CB-LC-C",
    "LC-480C", "CB-MCCC1", "MCC-1C1", "PUMP-RHR-A", "CB-MCCC2",
    "MCC-1C2", "FAN-CRHV-A", "HTR-BATRM-A", "CB-TIE-CD", "EDG-D",
    "CB-EDG-D", "TR-SAF-D", "CB-SAF-D", "BUS-416D", "TR-480-D",
    "CB-LC-D", "LC-480D", "CB-MCCD1", "MCC-1D1", "PUMP-RHR-B",
    "CB-MCCD2", "MCC-1D2", "FAN-CRHV-B", "HTR-BATRM-B", "XFER-ATS-B",
    "CHG-125B", "BAT-125B", "PNL-DC-B", "RECT-48V-B", "BAT-48V-B",
    "JB-RLY-B", "INV-UPS-B", "UPS-PNL-B", "CP-ESFAS-1", "CP-ESFAS-2",
    "RELAY-K1A", "RELAY-K2A", "RELAY-K1B", "RELAY-K2B", "RELAY-UV-A",
    "RELAY-LOOP-C", "RELAY-UV-B", "RELAY-LOOP-D", "INST-NSSS-A",
    "INST-NSSS-B", "GND-GRID",
]

DIEGO_R1_NODES = [
    "XFEER-ATS-A" if name == "XFER-ATS-A" else
    "XFEER-ATS-B" if name == "XFER-ATS-B" else name
    for name in FINAL_NODES
]


def r1(name: str) -> str:
    if name == "XFER-ATS-A":
        return "XFEER-ATS-A"
    if name == "XFER-ATS-B":
        return "XFEER-ATS-B"
    return name


FINAL_SOLID_CHAINS = [
    ["GRID-N230", "ISO-230A", "BRK-2301", "BUS-SY230"],
    ["GRID-S230", "ISO-230B", "BRK-2302", "BUS-SY230"],
    ["GEN-G101", "GSU-1", "BUS-SY230"],
    ["BUS-SY230", "TR-RAT-1A"],
    ["BUS-SY230", "TR-UAT-1A"],
    ["BUS-SY230", "TR-UAT-1B"],
    ["BUS-SY230", "TR-RAT-1B"],
    ["TR-RAT-1A", "CB-AUX-A", "TR-UAT-1A"],
    ["CB-AUX-A", "BUS-AUX13A"],
    ["TR-UAT-1B", "CB-AUX-B", "TR-RAT-1B"],
    ["CB-AUX-B", "BUS-AUX13B"],
    ["BUS-AUX13A", "CB-TIE13", "BUS-AUX13B"],
    ["BUS-AUX13A", "BUS-NON1"],
    ["BUS-AUX13A", "TR-SAF-A", "CB-SAF-A", "BUS-416A"],
    ["BUS-AUX13A", "TR-SAF-B", "CB-SAF-B", "BUS-416B"],
    ["BUS-AUX13B", "TR-SAF-C"],
    ["BUS-NON1", "TR-SAF-C", "CB-SAF-C", "BUS-416C"],
    ["BUS-AUX13B", "TR-SAF-D", "CB-SAF-D", "BUS-416D"],
    ["EDG-A", "CB-EDG-A", "BUS-416A"],
    ["EDG-B", "CB-EDG-B", "BUS-416B"],
    ["EDG-C", "CB-EDG-C", "BUS-416C"],
    ["EDG-D", "CB-EDG-D", "BUS-416D"],
    ["BUS-416A", "CB-TIE-AB", "BUS-416B"],
    ["BUS-416C", "CB-TIE-CD", "BUS-416D"],
    ["BUS-416A", "TR-480-A", "CB-LC-A", "LC-480A"],
    ["BUS-416B", "TR-480-B", "CB-LC-B", "LC-480B"],
    ["BUS-416C", "TR-480-C", "CB-LC-C", "LC-480C"],
    ["BUS-416D", "TR-480-D", "CB-LC-D", "LC-480D"],
    ["LC-480A", "CB-MCCA1", "MCC-1A1", "PUMP-AFW-A"],
    ["MCC-1A1", "VLV-MSIV-A"],
    ["LC-480A", "CB-MCCA2", "MCC-1A2", "PUMP-CCW-A"],
    ["LC-480A", "XFER-ATS-A"],
    ["LC-480B", "XFER-ATS-A"],
    ["LC-480B", "CB-MCCB1", "MCC-1B1", "PUMP-AFW-B"],
    ["MCC-1B1", "VLV-MSIV-B"],
    ["LC-480B", "CB-MCCB2", "MCC-1B2", "PUMP-CCW-B"],
    ["LC-480C", "CB-MCCC1", "MCC-1C1", "PUMP-RHR-A"],
    ["LC-480C", "CB-MCCC2", "MCC-1C2", "FAN-CRHV-A"],
    ["MCC-1C2", "HTR-BATRM-A"],
    ["LC-480C", "XFER-ATS-B"],
    ["LC-480D", "XFER-ATS-B"],
    ["LC-480C", "FAN-CRHV-A"],
    ["LC-480D", "CB-MCCD1", "MCC-1D1", "PUMP-RHR-B"],
    ["LC-480D", "CB-MCCD2", "MCC-1D2", "FAN-CRHV-B"],
    ["MCC-1D2", "HTR-BATRM-B"],
    ["LC-480D", "FAN-CRHV-B"],
    ["XFER-ATS-A", "CHG-125A", "BAT-125A", "PNL-DC-A", "INV-UPS-A", "UPS-PNL-A"],
    ["RECT-48V-A", "BAT-48V-A", "JB-RLY-A"],
    ["XFER-ATS-B", "CHG-125B", "BAT-125B", "PNL-DC-B", "INV-UPS-B", "UPS-PNL-B"],
    ["JB-RLY-B", "BAT-48V-B", "RECT-48V-B"],
]

DIEGO_R1_SOLID_CHAINS = [
    [r1(name) for name in chain]
    for chain in FINAL_SOLID_CHAINS
    if chain not in (["BUS-AUX13A", "BUS-NON1"], ["LC-480C", "FAN-CRHV-A"], ["LC-480D", "FAN-CRHV-B"])
]
DIEGO_R1_SOLID_CHAINS.append(["JB-RLY-A", "JB-RLY-B", "BAT-48V-B", "RECT-48V-B"])

CONTROL_EDGES = [
    ("CB-EDG-A", "RELAY-K1A"), ("CB-EDG-B", "RELAY-K1B"),
    ("CB-EDG-C", "RELAY-K2A"), ("CB-EDG-D", "RELAY-K2B"),
    ("RELAY-K1A", "CP-ESFAS-1"), ("RELAY-K1B", "CP-ESFAS-1"),
    ("RELAY-K2A", "CP-ESFAS-2"), ("RELAY-K2B", "CP-ESFAS-2"),
    ("CB-SAF-A", "CP-ESFAS-1"), ("CB-SAF-B", "CP-ESFAS-1"),
    ("CB-SAF-C", "CP-ESFAS-2"), ("CB-SAF-D", "CP-ESFAS-2"),
    ("RELAY-UV-A", "CB-LC-A"), ("RELAY-UV-A", "CB-LC-B"),
    ("RELAY-UV-A", "CB-TIE-AB"), ("RELAY-UV-B", "CB-LC-C"),
    ("RELAY-UV-B", "CB-LC-D"), ("RELAY-UV-B", "CB-TIE-CD"),
    ("RELAY-LOOP-C", "CB-MCCC1"), ("RELAY-LOOP-C", "CB-MCCC2"),
    ("RELAY-LOOP-C", "CB-TIE-CD"), ("RELAY-LOOP-D", "CB-MCCD1"),
    ("RELAY-LOOP-D", "CB-MCCD2"), ("INST-NSSS-A", "CP-ESFAS-1"),
    ("INST-NSSS-B", "CP-ESFAS-2"), ("PNL-DC-A", "PNL-DC-B"),
    ("INV-UPS-A", "RECT-48V-A"), ("INV-UPS-B", "RECT-48V-B"),
]

RELAY_SUPPLY_EDGES = [
    ("JB-RLY-A", "RELAY-K1A"), ("JB-RLY-A", "RELAY-K2A"),
    ("JB-RLY-A", "RELAY-UV-A"), ("JB-RLY-A", "RELAY-LOOP-C"),
    ("JB-RLY-B", "RELAY-K1B"), ("JB-RLY-B", "RELAY-K2B"),
    ("JB-RLY-B", "RELAY-UV-B"), ("JB-RLY-B", "RELAY-LOOP-D"),
]

FINAL_GROUND_EDGES = [
    ("GND-GRID", "TR-RAT-1A"), ("GND-GRID", "BUS-SY230"),
    ("GND-GRID", "TR-RAT-1B"), ("GND-GRID", "LC-480A"),
    ("GND-GRID", "LC-480B"), ("GND-GRID", "LC-480C"),
    ("GND-GRID", "LC-480D"), ("GND-GRID", "PUMP-CCW-A"),
    ("GND-GRID", "PUMP-CCW-B"), ("GND-GRID", "PUMP-RHR-A"),
    ("GND-GRID", "PUMP-RHR-B"), ("GND-GRID", "FAN-CRHV-A"),
    ("GND-GRID", "FAN-CRHV-B"), ("GND-GRID", "UPS-PNL-A"),
    ("GND-GRID", "INV-UPS-A"), ("GND-GRID", "BAT-48V-A"),
    ("GND-GRID", "BAT-48V-B"), ("GND-GRID", "INV-UPS-B"),
    ("GND-GRID", "UPS-PNL-B"),
]

DIEGO_R1_GROUND_EDGES = FINAL_GROUND_EDGES + [
    ("GND-GRID", "BUS-NON1"), ("GND-GRID", "JB-RLY-A"), ("GND-GRID", "JB-RLY-B"),
]

DIEGO_R1_UNCERTAIN = [
    ("BUS-NON1", "CB-TIE13"), ("MCC-1A2", "RECT-48V-A"),
    ("MCC-1B2", "RECT-48V-B"), ("LC-480C", "FAN-CRHV-A"),
    ("LC-480D", "FAN-CRHV-B"), ("RELAY-UV-A", "RELAY-LOOP-C"),
    ("RELAY-UV-B", "RELAY-LOOP-D"), ("INST-NSSS-A", "CP-ESFAS-2"),
    ("INST-NSSS-B", "CP-ESFAS-1"), ("JB-RLY-A", "RELAY-K1A"),
    ("JB-RLY-A", "RELAY-K2A"), ("JB-RLY-A", "RELAY-UV-A"),
    ("JB-RLY-A", "RELAY-LOOP-C"), ("JB-RLY-B", "RELAY-K1B"),
    ("JB-RLY-B", "RELAY-K2B"), ("JB-RLY-B", "RELAY-UV-B"),
    ("JB-RLY-B", "RELAY-LOOP-D"), ("CP-ESFAS-1", "CP-ESFAS-2"),
]

FINAL_UNCERTAIN = [
    ("JB-RLY-A", "GND-GRID"), ("JB-RLY-B", "GND-GRID"),
    ("RELAY-UV-A", "RELAY-LOOP-C"), ("RELAY-UV-B", "RELAY-LOOP-D"),
]


ROUNDS = [
    RoundSpec(
        round_id="round_01",
        actor="diego",
        role="high_recall_extractor",
        nodes=DIEGO_R1_NODES,
        chains=DIEGO_R1_SOLID_CHAINS,
        extra_edges=[
            *[(r1(a), r1(b)) for a, b in CONTROL_EDGES],
            *[(r1(a), r1(b)) for a, b in DIEGO_R1_GROUND_EDGES],
            *[(r1(a), r1(b)) for a, b in DIEGO_R1_UNCERTAIN],
        ],
        uncertain_edges=[(r1(a), r1(b)) for a, b in DIEGO_R1_UNCERTAIN],
        notes=[
            "High-recall extraction from raw PNG only.",
            "Used XFEER-ATS-A/B labels in this round; Jennifer later corrected them to XFER-ATS-A/B.",
            "Included visually plausible control, sensing, ground, and uncertain edges in the round matrix.",
            "The supplied resource path 5\\R4w did not exist; used 5\\Raw raw PNG matching requested outputs.",
        ],
    ),
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=FINAL_NODES,
        chains=FINAL_SOLID_CHAINS,
        extra_edges=[*CONTROL_EDGES, *RELAY_SUPPLY_EDGES, *FINAL_GROUND_EDGES],
        uncertain_edges=FINAL_UNCERTAIN,
        notes=[
            "Precision review from raw PNG and crops generated from that PNG.",
            "Corrected ATS labels to XFER-ATS-A and XFER-ATS-B.",
            "Confirmed BUS-AUX13A to BUS-NON1, LC-480C to FAN-CRHV-A, and LC-480D to FAN-CRHV-B.",
            "Rejected unsupported crossings/fanouts including JB-RLY-A to JB-RLY-B and cross-division NSSS/ESFAS links.",
            "Kept four uncertain edges outside the matrix.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor_consensus",
        nodes=FINAL_NODES,
        chains=FINAL_SOLID_CHAINS,
        extra_edges=[*CONTROL_EDGES, *RELAY_SUPPLY_EDGES, *FINAL_GROUND_EDGES],
        uncertain_edges=FINAL_UNCERTAIN,
        notes=[
            "Round 2 high-recall review accepted Jennifer's label corrections and edge removals.",
            "No additional raw-image-supported edges were added after precision review.",
            "Saturation reached from Diego side with four excluded uncertain edges.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_final",
        nodes=FINAL_NODES,
        chains=FINAL_SOLID_CHAINS,
        extra_edges=[*CONTROL_EDGES, *RELAY_SUPPLY_EDGES, *FINAL_GROUND_EDGES],
        uncertain_edges=FINAL_UNCERTAIN,
        notes=[
            "Final precision review agreed saturation was reached.",
            "Kept corrected XFER-ATS-A and XFER-ATS-B labels.",
            "Excluded JB-RLY-A to GND-GRID, JB-RLY-B to GND-GRID, RELAY-UV-A to RELAY-LOOP-C, and RELAY-UV-B to RELAY-LOOP-D.",
            "Final matrix excludes unsupported relay-bus shortcut, cross-NSSS/ESFAS links, CP-ESFAS cabinet tie, and MCC-to-rectifier shortcuts.",
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


def node_rows(nodes: list[str]) -> list[tuple[str, str]]:
    return [(f"n{idx:03d}", name) for idx, name in enumerate(nodes, start=1)]


def write_node_map(spec: RoundSpec) -> None:
    path = RESULTS / f"{spec.round_id}_{spec.actor}_node_map.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "node"])
        writer.writerows(node_rows(spec.nodes))


def write_edges(spec: RoundSpec, edges: list[tuple[str, str]]) -> None:
    name_to_id = {name: node_id for node_id, name in node_rows(spec.nodes)}
    uncertain = {tuple(sorted(edge)) for edge in spec.uncertain_edges}
    path = RESULTS / f"{spec.round_id}_{spec.actor}_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target", "status"])
        for left, right in edges:
            status = "uncertain" if tuple(sorted((left, right))) in uncertain else "confirmed"
            writer.writerow([name_to_id[left], left, name_to_id[right], right, status])


def write_uncertain_edges(spec: RoundSpec) -> None:
    name_to_id = {name: node_id for node_id, name in node_rows(spec.nodes)}
    matrix_edges = {tuple(sorted(edge)) for edge in adjacent_edges(spec.chains, spec.extra_edges)}
    path = RESULTS / f"{spec.round_id}_{spec.actor}_uncertain_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target", "included_in_matrix"])
        for left, right in spec.uncertain_edges:
            included = tuple(sorted((left, right))) in matrix_edges
            writer.writerow([name_to_id[left], left, name_to_id[right], right, int(included)])


def write_matrix(spec: RoundSpec, edges: list[tuple[str, str]]) -> None:
    index = {name: idx for idx, name in enumerate(spec.nodes)}
    matrix = [[0 for _ in spec.nodes] for _ in spec.nodes]
    for left, right in edges:
        i = index[left]
        j = index[right]
        matrix[i][j] = 1
        matrix[j][i] = 1

    path = RESULTS / f"{spec.round_id}_{spec.actor}_connectivity_matrix.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *spec.nodes])
        for name, row in zip(spec.nodes, matrix):
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
                "timestamp_local", "round_id", "actor", "role", "node_count",
                "edge_count", "uncertain_edge_count", "token_telemetry", "artifact_prefix",
            ]
        )
        for spec in specs:
            writer.writerow(
                [
                    datetime.now().isoformat(timespec="seconds"), spec.round_id, spec.actor,
                    spec.role, len(spec.nodes), len(adjacent_edges(spec.chains, spec.extra_edges)),
                    len(spec.uncertain_edges), "not available from current goal telemetry",
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
                "- The user-supplied resource path `5\\R4w` was not present; extraction used the raw PNG in `5\\Raw`, matching the requested code/results paths.",
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
