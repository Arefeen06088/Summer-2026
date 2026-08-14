from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class UncertainEdge:
    source: str
    target: str
    rationale: str


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[str]
    chains: list[list[str]]
    extra_edges: list[tuple[str, str]]
    uncertain_edges: list[UncertainEdge]
    include_uncertain_in_matrix: bool
    notes: list[str]


FINAL_NODES = [
    "GEN-G201", "IPB-201", "CB-GEN-201", "GSU-201", "SWYD-BUS-A",
    "CB-GRID-A", "GRID-230A", "CB-TIE-230", "SWYD-BUS-B", "CB-GRID-B",
    "GRID-230B", "TR-UAT-201", "TR-UAT-202", "TR-SST-201", "TR-SST-202",
    "DG EDG-201A", "CB-DG-A", "ATS-A", "DG EDG-201B", "CB-DG-B", "ATS-B",
    "CB-UAT-1", "CB-UAT-2", "CB-SST-1", "CB-SST-2", "BUS-6KV-A",
    "CB-TIE-6KV", "BUS-6KV-B", "PT-6KV-A", "PT-6KV-B", "DS-6KV-A",
    "DS-6KV-B", "BUS-4KV-N", "TR-480A", "CB-LC-A1", "LC-480A",
    "UV-SENS-A", "TR-480B", "CB-LC-B1", "LC-480B", "UV-SENS-B",
    "TR-480N", "CB-LC-N1", "LC-480N", "MCC-CCW-A", "JBX-CCW-A",
    "PUMP-CCW-A", "MOV-CCW-201A", "MCC-SW-A", "JBX-SW-A", "PUMP-SW-A",
    "MCC-HPI-A", "PUMP-HPI-A", "MOV-SI-201A", "MCC-VENT-A", "FAN-CR-A",
    "MCC-CCW-B", "JBX-CCW-B", "PUMP-CCW-B", "MOV-CCW-201B", "MCC-SW-B",
    "JBX-SW-B", "PUMP-SW-B", "MCC-HPI-B", "PUMP-HPI-B", "MOV-SI-201B",
    "MCC-VENT-B", "FAN-CR-B", "LP-N-A", "HTR-BLDG-A", "LP-N-B",
    "HTR-BLDG-B", "AC/DC CHGR-A", "BAT-125A", "PNL-DC-A", "AC/DC REC-A",
    "DC/AC INV-A", "UPS-A", "AC/DC CHGR-B", "BAT-125B", "PNL-DC-B",
    "AC/DC REC-B", "DC/AC INV-B", "UPS-B", "PNL-INST-A", "PNL-INST-B",
    "CP-ESFAS-A", "CP-ESFAS-B", "PLC-RPS-A", "PLC-RPS-B", "JBX-ESF-A",
    "JBX-ESF-B", "RELAY-UV-A", "RELAY-UV-B", "RELAY-SI-A", "RELAY-SI-B",
    "RELAY-LOAD-A", "RELAY-LOAD-B", "RELAY-DG-A", "RELAY-DG-B",
    "CT-EDG-A", "CT-EDG-B", "GND-A", "GND-B", "GND-MAIN",
]


def d1_name(name: str) -> str:
    if name == "DG EDG-201A":
        return "DG-EDG-201A"
    if name == "DG EDG-201B":
        return "DG-EDG-201B"
    return name


DIEGO_R1_NODES: list[str] = []
for node in FINAL_NODES:
    DIEGO_R1_NODES.append(d1_name(node))
    if node == "IPB-201":
        DIEGO_R1_NODES.append("IPB/UAT tap")


FINAL_CHAINS = [
    ["GEN-G201", "IPB-201", "CB-GEN-201", "GSU-201", "SWYD-BUS-A"],
    ["SWYD-BUS-A", "CB-GRID-A", "GRID-230A"],
    ["SWYD-BUS-B", "CB-GRID-B", "GRID-230B"],
    ["SWYD-BUS-A", "CB-TIE-230", "SWYD-BUS-B"],
    ["IPB-201", "TR-UAT-201"],
    ["IPB-201", "TR-UAT-202"],
    ["SWYD-BUS-A", "TR-SST-201"],
    ["SWYD-BUS-B", "TR-SST-202"],
    ["TR-UAT-201", "CB-UAT-1", "BUS-6KV-A"],
    ["TR-SST-201", "CB-SST-1", "BUS-6KV-A"],
    ["DG EDG-201A", "CB-DG-A", "ATS-A", "BUS-6KV-A"],
    ["TR-UAT-202", "CB-UAT-2", "BUS-6KV-B"],
    ["TR-SST-202", "CB-SST-2", "BUS-6KV-B"],
    ["DG EDG-201B", "CB-DG-B", "ATS-B", "BUS-6KV-B"],
    ["BUS-6KV-A", "CB-TIE-6KV", "BUS-6KV-B"],
    ["BUS-6KV-A", "PT-6KV-A"],
    ["BUS-6KV-B", "PT-6KV-B"],
    ["BUS-6KV-A", "DS-6KV-A", "BUS-4KV-N"],
    ["BUS-6KV-B", "DS-6KV-B", "BUS-4KV-N"],
    ["BUS-6KV-A", "TR-480A", "CB-LC-A1", "LC-480A"],
    ["BUS-6KV-B", "TR-480B", "CB-LC-B1", "LC-480B"],
    ["BUS-4KV-N", "TR-480N", "CB-LC-N1", "LC-480N"],
    ["LC-480A", "MCC-CCW-A", "JBX-CCW-A", "PUMP-CCW-A"],
    ["MCC-CCW-A", "MOV-CCW-201A"],
    ["LC-480A", "MCC-SW-A", "JBX-SW-A", "PUMP-SW-A"],
    ["LC-480A", "MCC-HPI-A", "PUMP-HPI-A"],
    ["MCC-HPI-A", "MOV-SI-201A"],
    ["LC-480A", "MCC-VENT-A", "FAN-CR-A"],
    ["LC-480B", "MCC-CCW-B", "JBX-CCW-B", "PUMP-CCW-B"],
    ["MCC-CCW-B", "MOV-CCW-201B"],
    ["LC-480B", "MCC-SW-B", "JBX-SW-B", "PUMP-SW-B"],
    ["LC-480B", "MCC-HPI-B", "PUMP-HPI-B"],
    ["MCC-HPI-B", "MOV-SI-201B"],
    ["LC-480B", "MCC-VENT-B", "FAN-CR-B"],
    ["LC-480N", "LP-N-A", "HTR-BLDG-A"],
    ["LC-480N", "LP-N-B", "HTR-BLDG-B"],
    ["LC-480A", "AC/DC CHGR-A", "PNL-DC-A"],
    ["AC/DC CHGR-A", "BAT-125A", "PNL-DC-A"],
    ["PNL-DC-A", "AC/DC REC-A", "DC/AC INV-A", "UPS-A"],
    ["LC-480B", "AC/DC CHGR-B", "PNL-DC-B"],
    ["AC/DC CHGR-B", "BAT-125B", "PNL-DC-B"],
    ["PNL-DC-B", "AC/DC REC-B", "DC/AC INV-B", "UPS-B"],
]

DIEGO_R1_CHAINS = []
for chain in FINAL_CHAINS:
    if chain == ["IPB-201", "TR-UAT-201"]:
        DIEGO_R1_CHAINS.append(["IPB-201", "IPB/UAT tap", "TR-UAT-201"])
    elif chain == ["IPB-201", "TR-UAT-202"]:
        DIEGO_R1_CHAINS.append(["IPB-201", "IPB/UAT tap", "TR-UAT-202"])
    else:
        DIEGO_R1_CHAINS.append([d1_name(name) for name in chain])

FINAL_EXTRA_EDGES = [
    ("LC-480A", "UV-SENS-A"), ("LC-480B", "UV-SENS-B"),
    ("MOV-SI-201A", "FAN-CR-A"), ("MOV-SI-201B", "FAN-CR-B"),
    ("PNL-INST-A", "RELAY-UV-A"), ("PNL-INST-B", "RELAY-UV-B"),
    ("CP-ESFAS-A", "RELAY-SI-A"), ("CP-ESFAS-B", "RELAY-SI-B"),
    ("PLC-RPS-A", "RELAY-LOAD-A"), ("PLC-RPS-B", "RELAY-LOAD-B"),
    ("JBX-ESF-A", "RELAY-DG-A"), ("JBX-ESF-B", "RELAY-DG-B"),
    ("BAT-125A", "GND-A"), ("AC/DC REC-A", "GND-A"), ("GND-A", "GND-MAIN"),
    ("BAT-125B", "GND-B"), ("AC/DC REC-B", "GND-B"), ("GND-B", "GND-MAIN"),
]

FINAL_UNCERTAIN = [
    UncertainEdge("UV-SENS-A", "PNL-INST-A or RELAY-UV-A", "Onward dashed sensing/control lane is crowded beyond the LC-to-sensor endpoint."),
    UncertainEdge("UV-SENS-B", "PNL-INST-B or RELAY-UV-B", "Onward dashed sensing/control lane is crowded beyond the LC-to-sensor endpoint."),
    UncertainEdge("CT-EDG-A", "DG EDG-201A / panels / relays", "Sensing lanes exist, but exact terminal pairing cannot be traced through no-dot crossings."),
    UncertainEdge("CT-EDG-B", "DG EDG-201B / panels / relays", "Sensing lanes exist, but exact terminal pairing cannot be traced through no-dot crossings."),
    UncertainEdge("6 kV breaker and ATS controls", "ESFAS/RPS relay bay", "Interlock trunks enter the bay, but one-to-one relay destinations are ambiguous."),
    UncertainEdge("Relay outputs", "SI/load/DG/UPS/DC field wiring", "Relay output paths run through crowded dashed lanes without clear terminal-dot endpoints."),
]

DIEGO_R1_UNCERTAIN = [
    UncertainEdge("UV-SENS-A", "PNL-INST-A", "High-recall candidate from sensor dashed lane."),
    UncertainEdge("UV-SENS-A", "RELAY-UV-A", "High-recall candidate from sensor/control lane."),
    UncertainEdge("UV-SENS-B", "PNL-INST-B", "High-recall candidate from sensor dashed lane."),
    UncertainEdge("UV-SENS-B", "RELAY-UV-B", "High-recall candidate from sensor/control lane."),
    UncertainEdge("CT-EDG-A", "DG-EDG-201A", "High-recall candidate from CT sensing box near A EDG."),
    UncertainEdge("CT-EDG-A", "PNL-INST-A", "High-recall candidate through left control-bay sensing lanes."),
    UncertainEdge("CT-EDG-A", "RELAY-DG-A", "High-recall candidate through left control-bay sensing lanes."),
    UncertainEdge("CT-EDG-B", "DG-EDG-201B", "High-recall candidate from CT sensing box near B EDG."),
    UncertainEdge("CT-EDG-B", "PNL-INST-B", "High-recall candidate through left control-bay sensing lanes."),
    UncertainEdge("CT-EDG-B", "RELAY-DG-B", "High-recall candidate through left control-bay sensing lanes."),
    UncertainEdge("CB-DG-A", "RELAY-DG-A", "High-recall candidate from breaker interlock trunk."),
    UncertainEdge("CB-DG-B", "RELAY-DG-B", "High-recall candidate from breaker interlock trunk."),
    UncertainEdge("MOV-SI-201A", "RELAY-SI-A", "High-recall candidate from SI control lane."),
    UncertainEdge("MOV-SI-201B", "RELAY-SI-B", "High-recall candidate from SI control lane."),
]


def map_edges_for_diego(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(d1_name(left), d1_name(right)) for left, right in edges]


ROUNDS = [
    RoundSpec(
        round_id="round_01",
        actor="diego",
        role="high_recall_extractor",
        nodes=DIEGO_R1_NODES,
        chains=DIEGO_R1_CHAINS,
        extra_edges=map_edges_for_diego(FINAL_EXTRA_EDGES),
        uncertain_edges=DIEGO_R1_UNCERTAIN,
        include_uncertain_in_matrix=True,
        notes=[
            "High-recall extraction from raw PNG and raw-derived crops only.",
            "Used normalized DG-EDG-201A/B labels and an inferred IPB/UAT tap node in this first proposal.",
            "Included exact high-recall uncertain candidates in this round matrix; Jennifer later removed them.",
            "The supplied resource path 6\\R4w did not exist; extraction used 6\\Raw as the raw source.",
        ],
    ),
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=FINAL_NODES,
        chains=FINAL_CHAINS,
        extra_edges=FINAL_EXTRA_EDGES,
        uncertain_edges=FINAL_UNCERTAIN,
        include_uncertain_in_matrix=False,
        notes=[
            "Precision review corrected labels to visible DG EDG-201A/B and removed the artificial IPB/UAT tap node.",
            "Confirmed direct IPB-201 to TR-UAT-201 and TR-UAT-202 edges.",
            "Kept device-mediated tie, disconnect, and UPS paths; crossings without filled dots were excluded.",
            "Kept crowded dashed control-harness endpoints outside the matrix.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor_consensus",
        nodes=FINAL_NODES,
        chains=FINAL_CHAINS,
        extra_edges=FINAL_EXTRA_EDGES,
        uncertain_edges=FINAL_UNCERTAIN,
        include_uncertain_in_matrix=False,
        notes=[
            "Round 2 high-recall review accepted Jennifer's precision corrections.",
            "No additional raw-image-supported edges were added.",
            "Saturation reached from Diego side with the dashed control-harness uncertainties excluded.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_final",
        nodes=FINAL_NODES,
        chains=FINAL_CHAINS,
        extra_edges=FINAL_EXTRA_EDGES,
        uncertain_edges=FINAL_UNCERTAIN,
        include_uncertain_in_matrix=False,
        notes=[
            "Final precision review agreed saturation was reached.",
            "Preserved exact visible labels DG EDG-201A/B, CB-LC-A1, CB-LC-B1, CB-LC-N1, HTR-BLDG-A/B, and MOV-CCW-201B.",
            "Final matrix excludes UV-sensor onward wiring, CT-EDG endpoints, 6 kV breaker/ATS interlock destinations, and relay outputs requiring crowded dashed-lane tracing.",
            "No GT or GT-derived resources were used.",
        ],
    ),
]


def edge_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def adjacent_edges(chains: list[list[str]], extra_edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    edges: list[tuple[str, str]] = []
    for chain in chains:
        for left, right in zip(chain, chain[1:]):
            key = edge_key(left, right)
            if key not in seen:
                seen.add(key)
                edges.append((left, right))
    for left, right in extra_edges:
        key = edge_key(left, right)
        if key not in seen:
            seen.add(key)
            edges.append((left, right))
    return edges


def matrix_edges(spec: RoundSpec) -> list[tuple[str, str]]:
    nodes = set(spec.nodes)
    edges = adjacent_edges(spec.chains, spec.extra_edges)
    seen = {edge_key(left, right) for left, right in edges}
    if spec.include_uncertain_in_matrix:
        for item in spec.uncertain_edges:
            if item.source in nodes and item.target in nodes:
                key = edge_key(item.source, item.target)
                if key not in seen:
                    seen.add(key)
                    edges.append((item.source, item.target))
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
    uncertain = {
        edge_key(item.source, item.target)
        for item in spec.uncertain_edges
        if item.source in name_to_id and item.target in name_to_id
    }
    path = RESULTS / f"{spec.round_id}_{spec.actor}_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "source", "target_id", "target", "status"])
        for left, right in edges:
            status = "uncertain" if edge_key(left, right) in uncertain else "confirmed"
            writer.writerow([name_to_id[left], left, name_to_id[right], right, status])


def write_uncertain_edges(spec: RoundSpec, edges: list[tuple[str, str]]) -> None:
    edge_keys = {edge_key(left, right) for left, right in edges}
    node_set = set(spec.nodes)
    path = RESULTS / f"{spec.round_id}_{spec.actor}_uncertain_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "included_in_matrix", "rationale"])
        for item in spec.uncertain_edges:
            included = (
                item.source in node_set
                and item.target in node_set
                and edge_key(item.source, item.target) in edge_keys
            )
            writer.writerow([item.source, item.target, int(included), item.rationale])


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
                "edge_count", "uncertain_item_count", "token_telemetry", "artifact_prefix",
            ]
        )
        for spec in specs:
            writer.writerow(
                [
                    datetime.now().isoformat(timespec="seconds"), spec.round_id, spec.actor,
                    spec.role, len(spec.nodes), len(matrix_edges(spec)), len(spec.uncertain_edges),
                    "not available from current goal telemetry", f"{spec.round_id}_{spec.actor}",
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
                "- Diego and Jennifer used only the raw schematic image and crops generated from it; no GT or GT-derived feedback was used.",
                "- The user-supplied resource path `6\\R4w` was not present; extraction used the raw PNG in `6\\Raw`, matching the requested code/results paths.",
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
        edges = matrix_edges(spec)
        write_node_map(spec)
        write_edges(spec, edges)
        write_uncertain_edges(spec, edges)
        write_matrix(spec, edges)
        write_notes(spec)
    update_tracking(ROUNDS)
    write_final_aliases(ROUNDS[-1])


if __name__ == "__main__":
    main()
