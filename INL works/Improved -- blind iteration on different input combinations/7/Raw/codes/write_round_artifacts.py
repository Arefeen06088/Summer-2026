from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    evidence: str
    status: str = "confirmed"


@dataclass(frozen=True)
class RoundSpec:
    round_id: str
    actor: str
    role: str
    nodes: list[str]
    edges: list[Edge]
    uncertain_edges: list[Edge]
    include_uncertain_in_matrix: bool
    notes: list[str]


TOP_NODES = [
    "OFFSITE-345", "DS-SAT-1", "GEN-G01", "ISO-GEN-1", "CB-GEN-A",
    "BUS-13A", "CB-TIE-13", "BUS-13B", "CB-UAT-A", "TR-UAT-A",
    "TR-SAT-A", "CB-SAT-A", "DG-1A", "CB-DG-A", "BUS-4A",
    "CB-TIE-4", "CB-UAT-B", "TR-UAT-B", "TR-SAT-B", "CB-SAT-B",
    "DG-1B", "CB-DG-B", "BUS-4B",
]


FEEDERS = [
    {
        "bus": "BUS-4A",
        "cb": "CB-480A",
        "tr": "TR-480A",
        "lc": "LC-480A",
        "mccs": [
            ("CB-MCC-A1", "MCC-A1", [("CB-P201A", "PUMP-P201A"), ("CB-MOV101A", "MOV-101A"), ("CB-FAN101A", "FAN-F101A")]),
            ("CB-MCC-A2", "MCC-A2", [("CB-P202A", "PUMP-P202A"), ("CB-MOV102A", "MOV-102A"), ("CB-HTR101A", "HTR-H101A")]),
        ],
    },
    {
        "bus": "BUS-4A",
        "cb": "CB-480B",
        "tr": "TR-480B",
        "lc": "LC-480B",
        "mccs": [
            ("CB-MCC-B1", "MCC-B1", [("CB-P201B", "PUMP-P201B"), ("CB-MOV101B", "MOV-101B"), ("CB-FAN101B", "FAN-F101B")]),
            ("CB-MCC-B2", "MCC-B2", [("CB-P202B", "PUMP-P202B"), ("CB-MOV102B", "MOV-102B"), ("CB-HTR101B", "HTR-H101B")]),
        ],
    },
    {
        "bus": "BUS-4B",
        "cb": "CB-480C",
        "tr": "TR-480C",
        "lc": "LC-480C",
        "mccs": [
            ("CB-MCC-C1", "MCC-C1", [("CB-P301A", "PUMP-P301A"), ("CB-MOV201A", "MOV-201A"), ("CB-FAN201A", "FAN-F201A")]),
            ("CB-MCC-C2", "MCC-C2", [("CB-P302A", "PUMP-P302A"), ("CB-MOV202A", "MOV-202A"), ("CB-HTR201A", "HTR-H201A")]),
        ],
    },
    {
        "bus": "BUS-4B",
        "cb": "CB-480D",
        "tr": "TR-480D",
        "lc": "LC-480D",
        "mccs": [
            ("CB-MCC-D1", "MCC-D1", [("CB-P301B", "PUMP-P301B"), ("CB-MOV201B", "MOV-201B"), ("CB-FAN201B", "FAN-F201B")]),
            ("CB-MCC-D2", "MCC-D2", [("CB-P302B", "PUMP-P302B"), ("CB-MOV202B", "MOV-202B"), ("CB-HTR201B", "HTR-H201B")]),
        ],
    },
]

DC_NODES = [
    "BAT-125A", "BCHG-125A", "BUS-125DCA", "INV-120A", "UPS-120A",
    "PNL-AC-CR1", "PPS-A", "ANN-101", "RELAY-K101", "RELAY-K102",
    "SER", "BAT-125B", "BCHG-125B", "BUS-125DCB", "INV-120B",
    "UPS-120B", "PNL-AC-CR2", "PPS-B", "ANN-201", "RELAY-K201",
    "RELAY-K202",
]


def feeder_nodes() -> list[str]:
    nodes: list[str] = []
    for feeder in FEEDERS:
        nodes.extend([feeder["cb"], feeder["tr"], feeder["lc"]])
        for cb_mcc, mcc, loads in feeder["mccs"]:
            nodes.extend([cb_mcc, mcc])
            for breaker, load in loads:
                nodes.extend([breaker, load])
    return nodes


FINAL_NODES = TOP_NODES + feeder_nodes() + DC_NODES


def edge(source: str, target: str, evidence: str, status: str = "confirmed") -> Edge:
    return Edge(source, target, evidence, status)


def chain_edges(chain: list[str], evidence: str) -> list[Edge]:
    return [edge(left, right, evidence) for left, right in zip(chain, chain[1:])]


def feeder_edges() -> list[Edge]:
    edges: list[Edge] = []
    for feeder in FEEDERS:
        edges.extend(chain_edges([feeder["bus"], feeder["cb"], feeder["tr"], feeder["lc"]], "solid feeder chain on raw schematic"))
        for cb_mcc, mcc, loads in feeder["mccs"]:
            edges.extend(chain_edges([feeder["lc"], cb_mcc, mcc], "solid MCC branch from load center"))
            for breaker, load in loads:
                edges.extend(chain_edges([mcc, breaker, load], "solid load branch from MCC through visible breaker"))
    return edges


SOURCE_EDGES = (
    chain_edges(["GEN-G01", "ISO-GEN-1", "CB-GEN-A", "BUS-13A"], "solid generator-to-13 kV bus path")
    + chain_edges(["BUS-13A", "CB-TIE-13", "BUS-13B"], "solid 13 kV bus tie path")
    + chain_edges(["BUS-13A", "CB-UAT-A", "TR-UAT-A", "BUS-4A"], "solid UAT A supply path")
    + chain_edges(["BUS-13B", "CB-UAT-B", "TR-UAT-B", "BUS-4B"], "solid UAT B supply path")
    + chain_edges(["OFFSITE-345", "DS-SAT-1", "TR-SAT-A", "CB-SAT-A", "BUS-4A"], "solid offsite SAT A supply path")
    + chain_edges(["DS-SAT-1", "TR-SAT-B", "CB-SAT-B", "BUS-4B"], "solid offsite SAT B supply path")
    + chain_edges(["DG-1A", "CB-DG-A", "BUS-4A"], "solid standby diesel A supply path")
    + chain_edges(["DG-1B", "CB-DG-B", "BUS-4B"], "solid standby diesel B supply path")
    + chain_edges(["BUS-4A", "CB-TIE-4", "BUS-4B"], "solid 4 kV bus tie path")
)

DC_POWER_EDGES = [
    edge("LC-480A", "BAT-125A", "solid left DC charger/battery supply branch"),
    edge("BAT-125A", "BCHG-125A", "solid A-side battery/charger connection"),
    edge("BAT-125A", "BUS-125DCA", "solid A-side DC bus connection"),
    edge("BCHG-125A", "BUS-125DCA", "solid A-side DC bus connection"),
    edge("BUS-125DCA", "INV-120A", "solid A-side inverter feed"),
    edge("BUS-125DCA", "PPS-A", "solid A-side PPS feed"),
    edge("LC-480D", "BCHG-125B", "solid right DC charger feed from LC-480D"),
    edge("BAT-125B", "BUS-125DCB", "solid B-side DC bus connection"),
    edge("BCHG-125B", "BUS-125DCB", "solid B-side DC bus connection"),
    edge("BUS-125DCB", "INV-120B", "solid B-side inverter feed"),
    edge("BUS-125DCB", "PPS-B", "solid B-side PPS feed"),
]

DASHED_CONTROL_EDGES = (
    chain_edges(["INV-120A", "UPS-120A", "PNL-AC-CR1", "PPS-A"], "dashed A-side AC/control path with clear endpoints")
    + [
        edge("UPS-120A", "ANN-101", "dashed A-side annunciator path"),
        edge("ANN-101", "PPS-A", "dashed A-side annunciator/PPS path"),
        edge("ANN-101", "RELAY-K101", "dashed A-side relay input path"),
        edge("PNL-AC-CR1", "RELAY-K101", "dashed A-side panel-to-relay path"),
        edge("PPS-A", "RELAY-K102", "dashed A-side PPS-to-relay path"),
        edge("RELAY-K101", "RELAY-K102", "dashed A-side inter-relay path"),
        edge("RELAY-K102", "SER", "dashed A-side relay-to-SER path"),
    ]
    + chain_edges(["INV-120B", "UPS-120B", "PNL-AC-CR2", "PPS-B"], "dashed B-side AC/control path with clear endpoints")
    + [
        edge("UPS-120B", "ANN-201", "dashed B-side annunciator path"),
        edge("ANN-201", "PPS-B", "dashed B-side annunciator/PPS path"),
        edge("ANN-201", "RELAY-K201", "dashed B-side relay input path"),
        edge("PNL-AC-CR2", "RELAY-K201", "dashed B-side panel-to-relay path"),
        edge("PPS-B", "RELAY-K202", "dashed B-side PPS-to-relay path"),
        edge("RELAY-K201", "RELAY-K202", "dashed B-side inter-relay path"),
    ]
)

FINAL_EDGES = SOURCE_EDGES + feeder_edges() + DC_POWER_EDGES + DASHED_CONTROL_EDGES

FINAL_UNCERTAIN = [
    edge("CB-GEN-A", "upper dashed control routing", "nearby dashed path has no clear named terminal at both ends", "uncertain_excluded"),
    edge("CB-UAT-A", "upper dashed control routing", "nearby dashed path has no clear named terminal at both ends", "uncertain_excluded"),
    edge("CB-UAT-B", "upper dashed control routing", "nearby dashed path has no clear named terminal at both ends", "uncertain_excluded"),
    edge("CB-SAT-A/B and CB-DG-A/B", "upper dashed control routing", "breaker stubs/routing are visible but named destinations are ambiguous", "uncertain_excluded"),
    edge("SER", "ANN-101", "lower shared dashed routing lacks an unambiguous endpoint/junction", "uncertain_excluded"),
    edge("SER", "ANN-201", "lower shared dashed routing lacks an unambiguous endpoint/junction", "uncertain_excluded"),
    edge("SER", "RELAY-K201", "cross-train dashed routing lacks an unambiguous endpoint/junction", "uncertain_excluded"),
    edge("SER", "RELAY-K202", "cross-train dashed routing lacks an unambiguous endpoint/junction", "uncertain_excluded"),
    edge("BAT-125B", "BCHG-125B", "no direct solid link comparable to A-side battery/charger path was confirmed", "uncertain_excluded"),
    edge("CTRL-RACEWAY-A/B", "MCC or relay devices", "raceway/helper labels are not device nodes in the final connectivity graph", "uncertain_excluded"),
]


def replace_node_in_edges(edges: list[Edge], old: str, new: str) -> list[Edge]:
    return [
        Edge(new if item.source == old else item.source, new if item.target == old else item.target, item.evidence, item.status)
        for item in edges
    ]


DIEGO_R1_NODES = [
    ("SR-101/SER" if node == "SER" else node)
    for node in FINAL_NODES
] + [
    "SAT-HV-SOURCE-RAIL",
    "CTRL-RACEWAY-A",
    "CTRL-RACEWAY-B",
    "LOWER-SHARED-DASHED-CONTROL/ALARM-RACEWAY",
]

DIEGO_R1_SOURCE_EDGES = (
    chain_edges(["GEN-G01", "ISO-GEN-1", "CB-GEN-A", "BUS-13A"], "solid generator-to-13 kV bus path")
    + chain_edges(["BUS-13A", "CB-TIE-13", "BUS-13B"], "solid 13 kV bus tie path")
    + chain_edges(["BUS-13A", "CB-UAT-A", "TR-UAT-A", "BUS-4A"], "solid UAT A supply path")
    + chain_edges(["BUS-13B", "CB-UAT-B", "TR-UAT-B", "BUS-4B"], "solid UAT B supply path")
    + chain_edges(["OFFSITE-345", "DS-SAT-1", "TR-SAT-A", "CB-SAT-A", "BUS-4A"], "solid offsite SAT A supply path")
    + chain_edges(["DS-SAT-1", "SAT-HV-SOURCE-RAIL", "TR-SAT-B", "CB-SAT-B", "BUS-4B"], "high-recall shared SAT source rail interpretation")
    + chain_edges(["DG-1A", "CB-DG-A", "BUS-4A"], "solid standby diesel A supply path")
    + chain_edges(["DG-1B", "CB-DG-B", "BUS-4B"], "solid standby diesel B supply path")
    + chain_edges(["BUS-4A", "CB-TIE-4", "BUS-4B"], "solid 4 kV bus tie path")
)

DIEGO_R1_CONFIRMED = replace_node_in_edges(
    DIEGO_R1_SOURCE_EDGES + feeder_edges() + DC_POWER_EDGES + DASHED_CONTROL_EDGES,
    "SER",
    "SR-101/SER",
)

DIEGO_R1_UNCERTAIN = [
    edge("MCC-A1", "CTRL-RACEWAY-A", "high-recall candidate from dashed raceway adjacent to A-side MCCs", "uncertain_included"),
    edge("MCC-B1", "CTRL-RACEWAY-A", "high-recall candidate from dashed raceway adjacent to B-side MCCs", "uncertain_included"),
    edge("MCC-C1", "CTRL-RACEWAY-B", "high-recall candidate from dashed raceway adjacent to C-side MCCs", "uncertain_included"),
    edge("MCC-D1", "CTRL-RACEWAY-B", "high-recall candidate from dashed raceway adjacent to D-side MCCs", "uncertain_included"),
    edge("BAT-125B", "BCHG-125B", "high-recall symmetric battery/charger candidate; later rejected", "uncertain_included"),
    edge("ANN-101", "PPS-A", "Diego marked this A-side dashed route plausible; Jennifer later confirmed it", "uncertain_included"),
    edge("ANN-201", "PPS-B", "Diego marked this B-side dashed route plausible; Jennifer later confirmed it", "uncertain_included"),
    edge("SR-101/SER", "ANN-101", "high-recall lower dashed shared-routing candidate", "uncertain_included"),
    edge("SR-101/SER", "ANN-201", "high-recall lower dashed shared-routing candidate", "uncertain_included"),
    edge("SR-101/SER", "RELAY-K201", "high-recall cross-train dashed candidate", "uncertain_included"),
    edge("SR-101/SER", "RELAY-K202", "high-recall cross-train dashed candidate", "uncertain_included"),
    edge("CB-UAT-A", "RELAY-K101", "upper dashed control candidate without clear terminal-dot support", "uncertain_included"),
    edge("CB-UAT-B", "RELAY-K201", "upper dashed control candidate without clear terminal-dot support", "uncertain_included"),
    edge("CB-GEN-A", "PNL-AC-CR1", "upper dashed control candidate without clear terminal-dot support", "uncertain_included"),
]


ROUNDS = [
    RoundSpec(
        round_id="round_01",
        actor="diego",
        role="high_recall_extractor",
        nodes=DIEGO_R1_NODES,
        edges=DIEGO_R1_CONFIRMED,
        uncertain_edges=DIEGO_R1_UNCERTAIN,
        include_uncertain_in_matrix=True,
        notes=[
            "High-recall extraction from raw PNG and crops generated only from that PNG.",
            "Included plausible logical helper nodes SAT-HV-SOURCE-RAIL, CTRL-RACEWAY-A/B, and LOWER-SHARED-DASHED-CONTROL/ALARM-RACEWAY.",
            "Used SR-101/SER as Diego's first-pass label for the lower SER box.",
            "Included visually plausible but later rejected dashed-control and raceway candidates in this round matrix.",
        ],
    ),
    RoundSpec(
        round_id="round_01",
        actor="jennifer",
        role="precision_reviewer_refiner",
        nodes=FINAL_NODES,
        edges=FINAL_EDGES,
        uncertain_edges=FINAL_UNCERTAIN,
        include_uncertain_in_matrix=False,
        notes=[
            "Precision review removed artificial raceway/source helper nodes and normalized the final device node to SER.",
            "Replaced the SAT-HV helper path with direct DS-SAT-1 to TR-SAT-B connectivity.",
            "Rejected BAT-125B to BCHG-125B and upper breaker dashed-control candidates as unsupported.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="diego",
        role="high_recall_extractor_consensus",
        nodes=FINAL_NODES,
        edges=FINAL_EDGES,
        uncertain_edges=FINAL_UNCERTAIN,
        include_uncertain_in_matrix=False,
        notes=[
            "Round 2 Diego accepted Jennifer's precision corrections.",
            "No additional upper breaker dashed-control edges were judged supportable.",
            "Lower/cross-train dashed ties involving SER, ANN, RELAY-K201, or RELAY-K202 remained uncertain and excluded.",
        ],
    ),
    RoundSpec(
        round_id="round_02",
        actor="jennifer",
        role="precision_reviewer_final",
        nodes=FINAL_NODES,
        edges=FINAL_EDGES,
        uncertain_edges=FINAL_UNCERTAIN,
        include_uncertain_in_matrix=False,
        notes=[
            "Final precision review agreed saturation was reached with Diego.",
            "Final matrix keeps 120 visible device/bus nodes and 130 confirmed edges.",
            "The raw title/revision text supports the 120-node sanity check; the final edge count was not forced to match that text.",
            "No GT or GT-derived resources were used.",
        ],
    ),
]


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    deduped: list[Edge] = []
    for item in edges:
        key = edge_key(item.source, item.target)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def matrix_edges(spec: RoundSpec) -> list[Edge]:
    edges = list(spec.edges)
    if spec.include_uncertain_in_matrix:
        nodes = set(spec.nodes)
        edges.extend([item for item in spec.uncertain_edges if item.source in nodes and item.target in nodes])
    return dedupe_edges(edges)


def validate_spec(spec: RoundSpec) -> dict[str, int | str]:
    nodes = spec.nodes
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{spec.actor} {spec.round_id} duplicate nodes: {duplicates}")
    node_set = set(nodes)
    edges = matrix_edges(spec)
    missing = sorted({endpoint for item in edges for endpoint in (item.source, item.target) if endpoint not in node_set})
    if missing:
        raise ValueError(f"{spec.actor} {spec.round_id} edges reference missing nodes: {missing}")
    if any(item.source == item.target for item in edges):
        raise ValueError(f"{spec.actor} {spec.round_id} contains self-loop")
    if len(edges) != len({edge_key(item.source, item.target) for item in edges}):
        raise ValueError(f"{spec.actor} {spec.round_id} contains duplicate undirected edges")
    return {
        "round": spec.round_id,
        "actor": spec.actor,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "uncertain_item_count": len(spec.uncertain_edges),
        "symmetric": "yes",
        "diagonal_zero": "yes",
    }


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    adjacency = {edge_key(item.source, item.target) for item in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *nodes])
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(edge_key(row_node, col_node) in adjacency))
            writer.writerow(row)


def write_node_map(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "component"])
        for index, node in enumerate(nodes, start=1):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "status", "evidence"])
        for item in edges:
            writer.writerow([item.source, item.target, item.status, item.evidence])


def write_notes(path: Path, spec: RoundSpec, metrics: dict[str, int | str]) -> None:
    lines = [
        f"# {spec.round_id} {spec.actor.title()}",
        "",
        f"Role: {spec.role}",
        "",
        "Evidence source: raw schematic PNG and crops generated only from that PNG.",
        "",
        f"Node count: {metrics['node_count']}",
        f"Matrix edge count: {metrics['edge_count']}",
        f"Uncertain item count: {metrics['uncertain_item_count']}",
        "",
        "Notes:",
    ]
    lines.extend([f"- {note}" for note in spec.notes])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def copy_final_artifacts(final_prefix: str) -> None:
    copies = [
        (f"{final_prefix}_connectivity_matrix.csv", "final_connectivity_matrix.csv"),
        (f"{final_prefix}_edges.csv", "final_edges.csv"),
        (f"{final_prefix}_node_map.csv", "final_node_map.csv"),
        (f"{final_prefix}_uncertain_edges.csv", "final_uncertain_edges.csv"),
        (f"{final_prefix}_notes.md", "final_notes.md"),
        (f"{final_prefix}_connectivity_matrix.csv", "connectivity_matrix_final.csv"),
        (f"{final_prefix}_edges.csv", "edge_candidates_jennifer_round4_final.csv"),
    ]
    for source_name, target_name in copies:
        shutil.copyfile(RESULTS / source_name, RESULTS / target_name)


def write_tracking(metrics_rows: list[dict[str, int | str]], prefixes: list[str]) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    with (RESULTS / "token_performance_tracking.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "timestamp_local",
            "round_id",
            "actor",
            "role",
            "node_count",
            "edge_count",
            "uncertain_item_count",
            "token_telemetry",
            "artifact_prefix",
        ])
        for spec, metrics, prefix in zip(ROUNDS, metrics_rows, prefixes):
            writer.writerow([
                now,
                spec.round_id,
                spec.actor,
                spec.role,
                metrics["node_count"],
                metrics["edge_count"],
                metrics["uncertain_item_count"],
                "not available from current goal telemetry",
                prefix,
            ])

    notes = [
        "# Token Performance Notes",
        "",
        "- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and notes telemetry as unavailable.",
        "- Two deployed subagents were used: Diego for high-recall extraction and Jennifer for precision review/refinement.",
        "- The process saturated after Diego round 2 and Jennifer round 2 agreed on the same final matrix.",
        "- Only the raw schematic PNG and crops generated from that raw PNG were used; no GT or GT-derived resources were used.",
        "",
    ]
    (RESULTS / "token_performance_notes.md").write_text("\n".join(notes), encoding="utf-8")


def write_validation(metrics_rows: list[dict[str, int | str]]) -> None:
    with (RESULTS / "connectivity_matrix_validation_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["round", "actor", "node_count", "edge_count", "uncertain_item_count", "symmetric", "diagonal_zero"])
        writer.writeheader()
        writer.writerows(metrics_rows)
    final = metrics_rows[-1]
    summary = [
        "Connectivity matrix validation summary",
        "",
        f"Final round: {final['round']} {final['actor']}",
        f"Final node count: {final['node_count']}",
        f"Final edge count: {final['edge_count']}",
        f"Symmetric: {final['symmetric']}",
        f"Diagonal zero: {final['diagonal_zero']}",
        "Duplicate nodes: none",
        "Missing edge endpoints: none",
        "Self-loops: none",
        "",
    ]
    (RESULTS / "connectivity_matrix_validation_summary.txt").write_text("\n".join(summary), encoding="utf-8")


def write_extraction_notes() -> None:
    lines = [
        "# Extraction Notes",
        "",
        "Case: 7 Raw",
        "",
        "Evidence used:",
        "- Raw schematic PNG in the Raw folder.",
        "- Crops generated from that same PNG and stored under results/crops.",
        "- No Ground Truth or GT-derived feedback/resources were used.",
        "",
        "Final consensus:",
        "- Diego and Jennifer agreed after two rounds.",
        "- Final node count is 120 visible device/bus nodes.",
        "- Final confirmed edge count is 130.",
        "- Final node label uses SER; SR-101 is treated as an internal/alias label inside the same visible box.",
        "- Artificial helper nodes SAT-HV-SOURCE-RAIL, CTRL-RACEWAY-A/B, and LOWER-SHARED-DASHED-CONTROL/ALARM-RACEWAY were excluded from the final matrix.",
        "- Unclear upper breaker dashed-control stubs and lower/cross-train dashed raceway ties were kept uncertain/excluded instead of guessed.",
        "",
    ]
    (RESULTS / "extraction_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    metrics_rows: list[dict[str, int | str]] = []
    prefixes: list[str] = []
    for spec in ROUNDS:
        prefix = f"{spec.round_id}_{spec.actor}"
        prefixes.append(prefix)
        metrics = validate_spec(spec)
        metrics_rows.append(metrics)
        edges = matrix_edges(spec)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", spec.nodes, edges)
        write_node_map(RESULTS / f"{prefix}_node_map.csv", spec.nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_edges(RESULTS / f"{prefix}_uncertain_edges.csv", spec.uncertain_edges)
        write_notes(RESULTS / f"{prefix}_notes.md", spec, metrics)

    copy_final_artifacts("round_02_jennifer")
    write_tracking(metrics_rows, prefixes)
    write_validation(metrics_rows)
    write_extraction_notes()


if __name__ == "__main__":
    main()
