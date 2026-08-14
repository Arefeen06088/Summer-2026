from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw")
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


def edge(source: str, target: str, evidence: str, status: str = "confirmed") -> Edge:
    return Edge(source, target, evidence, status)


def chain(items: list[str], evidence: str) -> list[Edge]:
    return [edge(a, b, evidence) for a, b in zip(items, items[1:])]


def edge_key(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted((source, target)))


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    seen: set[tuple[str, str]] = set()
    result: list[Edge] = []
    for item in edges:
        key = edge_key(item.source, item.target)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


TOP_NODES = [
    "GEN-G1",
    "CB-GEN-1",
    "TR-UAT-1",
    "CB-101",
    "TR-SUT-1",
    "DS-SUT-1",
    "CB-102",
    "EDG-1A",
    "DS-EDG-1A",
    "CB-103",
    "BUS-4KV-A",
    "CB-TIE-1",
    "BUS-4KV-B",
    "EDG-1B",
    "DS-EDG-1B",
    "CB-203",
    "TR-SUT-2",
    "DS-SUT-2",
    "CB-202",
    "EDG-1C",
    "CB-303",
]

TRAIN_A_POWER_NODES = [
    "CB-111",
    "TR-480-A",
    "BUS-480-A",
    "CB-M1A",
    "MCC-1A",
    "CB-112",
    "TR-480-C",
    "BUS-480-C",
    "CB-M2A",
    "MCC-2A",
]

TRAIN_B_POWER_NODES = [
    "CB-211",
    "TR-480-B",
    "BUS-480-B",
    "CB-M1B",
    "MCC-1B",
    "CB-212",
    "TR-480-D",
    "BUS-480-D",
    "CB-M2B",
    "MCC-2B",
]

A_MCC_1_BRANCHES = [
    ("CB-F001", "FU-F001", "PUMP-RHR-A"),
    ("CB-F002", "MS-F002", "PUMP-SI-A"),
    ("CB-F003", "FU-F003", "FAN-CR-A"),
    ("CB-F004", "DS-F004", "MOV-RCIC-A"),
    ("CB-F005", "MS-F005", "PUMP-CCW-A"),
    ("CB-F006", "FU-F006", "HTR-SUMP-A"),
    ("CB-F007", "MS-F007", "PMP-BOR-A"),
    ("CB-F008", "DS-F008", "VALVE-IA-A"),
]

A_MCC_2_BRANCHES = [
    ("CB-F009", "MS-F009", "PUMP-AFW-A"),
    ("CB-F010", "MS-F010", "PMP-LUBE-A"),
    ("CB-F011", "DS-F011", "MOV-RHR-A"),
    ("CB-F012", "FU-F012", "FAN-BLDG-A"),
    ("CB-F013", "FU-F013", "PNL-RAD-A"),
    ("CB-F014", "MS-F014", "PUMP-SW-A"),
    ("CB-F015", "DS-F015", None),
]

B_MCC_1_BRANCHES = [
    ("CB-F016", "MS-F016", "PUMP-RHR-B"),
    ("CB-F017", "MS-F017", "PUMP-SI-B"),
    ("CB-F018", "FU-F018", "FAN-CR-B"),
    ("CB-F019", "DS-F019", "MOV-RCIC-B"),
    ("CB-F020", "MS-F020", "PUMP-CCW-B"),
    ("CB-F021", "FU-F021", "HTR-SUMP-B"),
    ("CB-F022", "MS-F022", "PMP-BOR-B"),
    ("CB-F023", "DS-F023", "VALVE-IA-B"),
]

B_MCC_2_BRANCHES = [
    ("CB-F024", "MS-F024", "PUMP-AFW-B"),
    ("CB-F025", "MS-F025", "PMP-LUBE-B"),
    ("CB-F026", "DS-F026", "MOV-RHR-B"),
    ("CB-F027", "FU-F027", "FAN-BLDG-B"),
    ("CB-F028", "FU-F028", "PNL-RAD-B"),
    ("CB-F029", "MS-F029", "PUMP-SW-B"),
]


def branch_nodes(branches: list[tuple[str, str, str | None]]) -> list[str]:
    nodes: list[str] = []
    for cb, device, load in branches:
        nodes.extend([cb, device])
        if load is not None:
            nodes.append(load)
    return nodes


TRAIN_A_LOAD_NODES = branch_nodes(A_MCC_1_BRANCHES) + branch_nodes(A_MCC_2_BRANCHES)
TRAIN_B_LOAD_NODES = branch_nodes(B_MCC_1_BRANCHES) + branch_nodes(B_MCC_2_BRANCHES)

DC_POWER_NODES = [
    "CB-DC-1A",
    "CHGR-125A",
    "BAT-125A",
    "DC-BUS-A",
    "INV-1A",
    "CB-DC-1B",
    "CHGR-125B",
    "BAT-125B",
    "DC-BUS-B",
    "INV-1B",
    "ATS-INV",
    "BUS-120VAC-ESF",
]

BOTTOM_CONTROL_NODES = [
    "TB-RPS-A",
    "PNL-RPS-A",
    "PNL-ESFAS-A",
    "RELAY-50A",
    "RELAY-86A",
    "TB-ANN-1",
    "ANN A",
    "TB-RPS-B",
    "PNL-RPS-B",
    "PNL-ESFAS-B",
    "RELAY-50B",
    "RELAY-86B",
    "SEQ-REC-1",
]

FINAL_NODES = (
    TOP_NODES
    + TRAIN_A_POWER_NODES
    + TRAIN_A_LOAD_NODES
    + TRAIN_B_POWER_NODES
    + TRAIN_B_LOAD_NODES
    + DC_POWER_NODES
    + BOTTOM_CONTROL_NODES
)

VISIBLE_NON_MATRIX_NODES = [
    "PT-4160A",
    "PT-4160B",
    "ANN B",
    "GND-1",
    "GND-2",
    "SPARE-A2",
    "RELAY-27A",
    "RELAY-27B",
]

HELPER_NODES = [
    "A_SOURCE_INTERLOCK_TRUNK",
    "B_SOURCE_INTERLOCK_TRUNK",
    "A_RPS_CONTROL_TRUNK",
    "B_RPS_CONTROL_TRUNK",
    "ANN_SIGNAL_TRUNK_A",
    "ANN_SIGNAL_TRUNK_B",
    "ESFAS_SIGNAL_TRUNK_A",
    "ESFAS_SIGNAL_TRUNK_B",
]

DIEGO_R1_NODES = FINAL_NODES + VISIBLE_NON_MATRIX_NODES + HELPER_NODES


def mcc_edges(mcc: str, branches: list[tuple[str, str, str | None]], evidence: str) -> list[Edge]:
    result: list[Edge] = []
    for cb, device, load in branches:
        result.append(edge(mcc, cb, evidence))
        result.append(edge(cb, device, evidence))
        if load is not None:
            result.append(edge(device, load, evidence))
    return result


TOP_EDGES = dedupe_edges(
    chain(["GEN-G1", "CB-GEN-1", "TR-UAT-1", "CB-101", "BUS-4KV-A"], "solid source feeder to BUS-4KV-A")
    + chain(["TR-SUT-1", "DS-SUT-1", "CB-102", "BUS-4KV-A"], "solid standby transformer feeder to BUS-4KV-A")
    + chain(["EDG-1A", "DS-EDG-1A", "CB-103", "BUS-4KV-A"], "solid EDG-1A feeder to BUS-4KV-A")
    + chain(["BUS-4KV-A", "CB-TIE-1", "BUS-4KV-B"], "solid 4 kV bus tie through CB-TIE-1")
    + chain(["EDG-1B", "DS-EDG-1B", "CB-203", "BUS-4KV-B"], "solid EDG-1B feeder to BUS-4KV-B")
    + chain(["TR-SUT-2", "DS-SUT-2", "CB-202", "BUS-4KV-B"], "solid standby transformer feeder to BUS-4KV-B")
    + chain(["EDG-1C", "CB-303", "BUS-4KV-B"], "solid EDG-1C feeder to BUS-4KV-B")
)

FEEDER_480_EDGES = dedupe_edges(
    chain(["BUS-4KV-A", "CB-111", "TR-480-A", "BUS-480-A", "CB-M1A", "MCC-1A"], "solid 4 kV to 480 V MCC-1A feeder")
    + chain(["BUS-4KV-A", "CB-112", "TR-480-C", "BUS-480-C", "CB-M2A", "MCC-2A"], "solid 4 kV to 480 V MCC-2A feeder")
    + chain(["BUS-4KV-B", "CB-211", "TR-480-B", "BUS-480-B", "CB-M1B", "MCC-1B"], "solid 4 kV to 480 V MCC-1B feeder")
    + chain(["BUS-4KV-B", "CB-212", "TR-480-D", "BUS-480-D", "CB-M2B", "MCC-2B"], "solid 4 kV to 480 V MCC-2B feeder")
)

MCC_LOAD_EDGES = dedupe_edges(
    mcc_edges("MCC-1A", A_MCC_1_BRANCHES, "solid MCC-1A load branch")
    + mcc_edges("MCC-2A", A_MCC_2_BRANCHES, "solid MCC-2A load branch")
    + mcc_edges("MCC-1B", B_MCC_1_BRANCHES, "solid MCC-1B load branch")
    + mcc_edges("MCC-2B", B_MCC_2_BRANCHES, "solid MCC-2B load branch")
)

DC_INVERTER_EDGES = dedupe_edges(
    chain(["BUS-480-C", "CB-DC-1A", "CHGR-125A", "DC-BUS-A"], "solid Train A 125 VDC charger feeder")
    + [
        edge("BAT-125A", "DC-BUS-A", "solid battery A tap to DC-BUS-A"),
        edge("DC-BUS-A", "INV-1A", "solid DC-BUS-A input to inverter"),
        edge("INV-1A", "ATS-INV", "solid inverter A output to inverter ATS"),
    ]
    + chain(["BUS-480-B", "CB-DC-1B", "CHGR-125B", "DC-BUS-B"], "solid Train B 125 VDC charger feeder")
    + [
        edge("BAT-125B", "DC-BUS-B", "solid battery B tap to DC-BUS-B"),
        edge("DC-BUS-B", "INV-1B", "solid DC-BUS-B input to inverter"),
        edge("INV-1B", "ATS-INV", "solid inverter B output to inverter ATS"),
        edge("ATS-INV", "BUS-120VAC-ESF", "solid ATS output to 120 VAC ESF instrument bus"),
        edge("BUS-120VAC-ESF", "PNL-ESFAS-A", "confirmed 120 VAC ESF bus feed to ESFAS-A panel"),
        edge("BUS-120VAC-ESF", "PNL-ESFAS-B", "confirmed 120 VAC ESF bus feed to ESFAS-B panel"),
    ]
)

BOTTOM_CONTROL_EDGES = [
    edge("RELAY-50A", "RELAY-86A", "dashed A-side relay control line"),
    edge("RELAY-50B", "RELAY-86B", "dashed B-side relay control line"),
    edge("TB-RPS-A", "PNL-RPS-A", "dashed/control route into A RPS terminal-panel cluster"),
    edge("TB-RPS-B", "PNL-RPS-B", "dashed/control route into B RPS terminal-panel cluster"),
    edge("ANN A", "TB-ANN-1", "dotted annunciator A signal to terminal block"),
    edge("SEQ-REC-1", "PNL-ESFAS-A", "dotted signal route from sequence recorder to ESFAS-A"),
    edge("SEQ-REC-1", "PNL-ESFAS-B", "dotted signal route from sequence recorder to ESFAS-B"),
]

FINAL_EDGES = dedupe_edges(TOP_EDGES + FEEDER_480_EDGES + MCC_LOAD_EDGES + DC_INVERTER_EDGES + BOTTOM_CONTROL_EDGES)

DIEGO_R1_EXTRA_CONFIRMED = [
    edge("PNL-RPS-A", "GND-1", "Diego round 1 high-recall equipment ground reference line"),
    edge("PNL-RPS-B", "GND-2", "Diego round 1 high-recall equipment ground reference line"),
    edge("DS-F015", "SPARE-A2", "Diego round 1 retained visible spare placeholder load"),
]

DIEGO_R1_EDGES = dedupe_edges(
    TOP_EDGES
    + FEEDER_480_EDGES
    + MCC_LOAD_EDGES
    + [
        item
        for item in DC_INVERTER_EDGES
        if edge_key(item.source, item.target)
        not in {
            edge_key("BUS-120VAC-ESF", "PNL-ESFAS-A"),
            edge_key("BUS-120VAC-ESF", "PNL-ESFAS-B"),
        }
    ]
    + BOTTOM_CONTROL_EDGES
    + DIEGO_R1_EXTRA_CONFIRMED
)

DIEGO_R1_UNCERTAIN = [
    edge("BUS-4KV-A", "PT-4160A", "likely voltage sensing but no precision-clean bus tap", "uncertain_included"),
    edge("BUS-4KV-B", "PT-4160B", "likely voltage sensing but no precision-clean bus tap", "uncertain_included"),
    edge("CB-101", "A_SOURCE_INTERLOCK_TRUNK", "dash-dot source interlock trunk crosses source area", "uncertain_included"),
    edge("CB-102", "A_SOURCE_INTERLOCK_TRUNK", "dash-dot source interlock trunk crosses source area", "uncertain_included"),
    edge("CB-103", "A_SOURCE_INTERLOCK_TRUNK", "dash-dot source interlock trunk crosses source area", "uncertain_included"),
    edge("CB-203", "B_SOURCE_INTERLOCK_TRUNK", "dash-dot source interlock trunk crosses source area", "uncertain_included"),
    edge("CB-202", "B_SOURCE_INTERLOCK_TRUNK", "dash-dot source interlock trunk crosses source area", "uncertain_included"),
    edge("CB-303", "B_SOURCE_INTERLOCK_TRUNK", "dash-dot source interlock trunk crosses source area", "uncertain_included"),
    edge("BUS-120VAC-ESF", "PNL-ESFAS-A", "Diego uncertain instrument-bus panel feed later accepted by Jennifer", "uncertain_included"),
    edge("BUS-120VAC-ESF", "PNL-ESFAS-B", "Diego uncertain instrument-bus panel feed later accepted by Jennifer", "uncertain_included"),
    edge("BUS-120VAC-ESF", "PNL-RPS-A", "possible instrument bus feed but endpoint not precision-clean", "uncertain_included"),
    edge("BUS-120VAC-ESF", "PNL-RPS-B", "possible instrument bus feed but endpoint not precision-clean", "uncertain_included"),
    edge("BUS-120VAC-ESF", "SEQ-REC-1", "possible recorder feed but endpoint not precision-clean", "uncertain_included"),
    edge("RELAY-27A", "TB-RPS-A", "dashed relay/RPS route is crowded", "uncertain_included"),
    edge("RELAY-27B", "TB-RPS-B", "dashed relay/RPS route is crowded", "uncertain_included"),
    edge("RELAY-86A", "TB-RPS-A", "possible lockout relay control to terminal block", "uncertain_included"),
    edge("RELAY-86B", "TB-RPS-B", "possible lockout relay control to terminal block", "uncertain_included"),
    edge("ANN B", "TB-RPS-B", "visible B annunciator route but no discrete endpoint comparable to ANN A", "uncertain_included"),
    edge("PNL-RPS-A", "PNL-ESFAS-A", "dashed logic route between panel groups is ambiguous", "uncertain_included"),
    edge("PNL-RPS-B", "PNL-ESFAS-B", "dashed logic route between panel groups is ambiguous", "uncertain_included"),
]

FINAL_UNCERTAIN = [
    edge("BUS-4KV-A", "PT-4160A", "PT is visible but PT-to-bus sensing edge is not precision-clean", "uncertain_excluded"),
    edge("BUS-4KV-B", "PT-4160B", "PT is visible but PT-to-bus sensing edge is not precision-clean", "uncertain_excluded"),
    edge("PNL-RPS-A", "GND-1", "ground shown as equipment reference only, not matrix connectivity", "uncertain_excluded"),
    edge("PNL-RPS-B", "GND-2", "ground shown as equipment reference only, not matrix connectivity", "uncertain_excluded"),
    edge("DS-F015", "SPARE-A2", "SPARE-A2 is a placeholder, not active load connectivity", "uncertain_excluded"),
    edge("ANN B", "TB-RPS-B", "ANN B visible but no confirmed discrete endpoint", "uncertain_excluded"),
    edge("RELAY-27A", "TB-RPS-A", "dashed relay/RPS route is crowded and not endpoint-clean", "uncertain_excluded"),
    edge("RELAY-27B", "TB-RPS-B", "dashed relay/RPS route is crowded and not endpoint-clean", "uncertain_excluded"),
    edge("RELAY-86A", "TB-RPS-A", "lockout-to-terminal route is not endpoint-clean; only RELAY-50A--RELAY-86A retained", "uncertain_excluded"),
    edge("RELAY-86B", "TB-RPS-B", "lockout-to-terminal route is not endpoint-clean; only RELAY-50B--RELAY-86B retained", "uncertain_excluded"),
    edge("BUS-120VAC-ESF", "PNL-RPS-A", "instrument bus to RPS-A endpoint is not precision-clean", "uncertain_excluded"),
    edge("BUS-120VAC-ESF", "PNL-RPS-B", "instrument bus to RPS-B endpoint is not precision-clean", "uncertain_excluded"),
    edge("BUS-120VAC-ESF", "SEQ-REC-1", "recorder feed is not precision-clean", "uncertain_excluded"),
    edge("PNL-RPS-A", "PNL-ESFAS-A", "dashed RPS/ESFAS route is ambiguous", "uncertain_excluded"),
    edge("PNL-RPS-B", "PNL-ESFAS-B", "dashed RPS/ESFAS route is ambiguous", "uncertain_excluded"),
    edge("BUS-480-C", "MCC-2A", "direct bypass would skip CB-M2A and appears to be routing/crossing clutter", "uncertain_excluded"),
    edge("BUS-480-B", "MCC-2B", "direct bypass would skip CB-M2B and appears to be routing/crossing clutter", "uncertain_excluded"),
    edge("CB-F019", "CB-DC-1B", "vertical alignment near MOV-RCIC-B is treated as crossing/routing artifact", "uncertain_excluded"),
    edge("CB-F027", "CB-DC-1B", "vertical alignment near FAN-BLDG-B is treated as crossing/routing artifact", "uncertain_excluded"),
    edge("A_SOURCE_INTERLOCK_TRUNK", "CB-101", "helper trunk node removed from final graph", "uncertain_excluded"),
    edge("B_SOURCE_INTERLOCK_TRUNK", "CB-203", "helper trunk node removed from final graph", "uncertain_excluded"),
]

ROUNDS = [
    RoundSpec(
        "round_01",
        "diego",
        "high_recall_extractor",
        DIEGO_R1_NODES,
        DIEGO_R1_EDGES,
        DIEGO_R1_UNCERTAIN,
        True,
        [
            "High-recall extraction from raw PNG and crops generated only from that PNG.",
            "Included PTs, relay-27 nodes, ANN B, grounds, spare placeholder, and logical trunk candidates for review.",
            "Included uncertain instrument-bus, relay/RPS, source-interlock, and bypass candidates in the round matrix.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_01",
        "jennifer",
        "precision_reviewer_refiner",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Trimmed graph to edge-supported component nodes only.",
            "Excluded PTs, relay-27 nodes, ANN B, equipment grounds, spare placeholder, and helper trunks from the final matrix.",
            "Accepted only precision-clean 120 VAC ESF edges to ESFAS-A/B and kept RPS/relay clutter uncertain.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_02",
        "diego",
        "high_recall_extractor_consensus",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Diego accepted Jennifer's refined final matrix with no edge changes.",
            "Confirmed exclusions for PT-4160A/B, ANN B, GND-1/2, SPARE-A2, and RELAY-27A/B.",
            "Confirmed no crossing-only, helper-trunk, or inferred RPS/ESFAS relay edges should be added.",
        ],
    ),
    RoundSpec(
        "round_02",
        "jennifer",
        "precision_reviewer_final",
        FINAL_NODES,
        FINAL_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Final saturation confirmed after Diego agreed.",
            "Final matrix includes only nodes incident to visually confirmed edges.",
            "Visible non-matrix annotations are PT-4160A/B, ANN B, GND-1/2, SPARE-A2, and RELAY-27A/B.",
            "No GT or GT-derived resources were used.",
        ],
    ),
]


def matrix_edges(spec: RoundSpec) -> list[Edge]:
    edges = list(spec.edges)
    if spec.include_uncertain_in_matrix:
        node_set = set(spec.nodes)
        edges.extend([item for item in spec.uncertain_edges if item.source in node_set and item.target in node_set])
    return dedupe_edges(edges)


def validate_spec(spec: RoundSpec) -> dict[str, int | str]:
    nodes = spec.nodes
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{spec.round_id} {spec.actor} duplicate nodes: {duplicates}")
    node_set = set(nodes)
    edges = matrix_edges(spec)
    missing = sorted({endpoint for item in edges for endpoint in (item.source, item.target) if endpoint not in node_set})
    if missing:
        raise ValueError(f"{spec.round_id} {spec.actor} missing edge endpoints: {missing}")
    if any(item.source == item.target for item in edges):
        raise ValueError(f"{spec.round_id} {spec.actor} contains self-loop")
    if len(edges) != len({edge_key(item.source, item.target) for item in edges}):
        raise ValueError(f"{spec.round_id} {spec.actor} contains duplicate undirected edges")
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
    agent_ids = {
        "diego": "019f5f97-0fcc-7ea0-b8b6-22511ddaca9f",
        "jennifer": "019f5f9b-0cf4-7c10-a067-27ade4a0b7f0",
    }
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
            "subagent_runtime_id",
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
                agent_ids["diego" if spec.actor == "diego" else "jennifer"],
                "not available from current runtime telemetry",
                prefix,
            ])

    notes = [
        "# Token Performance Notes",
        "",
        "- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and marks token telemetry unavailable.",
        "- Two deployed subagents were used: Diego for high-recall extraction and Jennifer for precision review/refinement.",
        "- The process saturated after Diego accepted Jennifer's edge-supported final matrix and Jennifer final-confirmed it.",
        "- There was no Input resources folder; only the raw schematic PNG and crops generated from it were used. No GT or GT-derived resources were used.",
        "",
    ]
    (RESULTS / "token_performance_notes.md").write_text("\n".join(notes), encoding="utf-8")


def write_validation(metrics_rows: list[dict[str, int | str]]) -> None:
    with (RESULTS / "connectivity_matrix_validation_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["round", "actor", "node_count", "edge_count", "uncertain_item_count", "symmetric", "diagonal_zero"],
        )
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
        "Case: 12 Raw",
        "",
        "Evidence used:",
        "- Raw schematic PNG in the Raw folder.",
        "- Crops generated from that same PNG and stored under results/crops.",
        "- No Input resources folder was present; no Ground Truth or GT-derived feedback/resources were used.",
        "",
        "Final consensus:",
        "- Diego and Jennifer agreed after two rounds.",
        f"- Final node count is {len(FINAL_NODES)} edge-supported component/node labels.",
        f"- Final confirmed edge count is {len(FINAL_EDGES)}.",
        "- Final visible non-matrix annotations: PT-4160A, PT-4160B, ANN B, GND-1, GND-2, SPARE-A2, RELAY-27A, RELAY-27B.",
        "- Crossings without dots, helper trunks, PT sensing, ground references, spare placeholder, and crowded RPS/ESFAS relay routes were excluded.",
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
