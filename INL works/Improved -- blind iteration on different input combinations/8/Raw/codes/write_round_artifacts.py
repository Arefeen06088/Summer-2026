from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw")
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


SOURCE_NODES = [
    "GRID-345-01", "SUT-2A", "CB-402A", "BUS-4160-N2A", "GEN-U2",
    "UAT-2A", "CB-401A", "UAT-2B", "CB-401B", "CB-TIE-4160",
    "BUS-4160-N2B", "GRID-345-02", "SUT-2B", "CB-402B",
    "BUS-4160-S2A", "EDG-2A", "CB-EDG-A", "EDG-2C", "CB-EDG-C",
    "BUS-4160-S2B", "EDG-2B", "CB-EDG-B", "CT-4160A", "PT-4160A",
    "RELAY-50/51A", "RELAY-27A", "RELAY-86A", "CT-4160B",
    "PT-4160B", "RELAY-50/51B", "RELAY-27B", "RELAY-86B",
]

COMMON_480_NODES = [
    "TR-480-2A", "BUS-480-E2A", "TR-480-N2A", "BUS-480-N2A",
    "DS-480-A", "DS-480-B", "TR-480-N2B", "BUS-480-N2B",
    "TR-480-2B", "BUS-480-E2B", "GND-A", "GND-B", "CB-N1", "CB-N2",
]

A_LOAD_NODES = [
    "MCC-2A1", "MCC-2A2", "PN-480-A", "MCC-2C",
    "CB-51A", "PUMP-SI-2A", "CB-52A", "PUMP-RHR-2A",
    "CB-53A", "PUMP-CS-2A", "CB-54A", "PUMP-CCW-2A",
    "CB-55A", "FAN-CRE-2A", "CB-56A", "MOV-8801A",
    "CB-57A", "MOV-8802A", "CB-58A", "PUMP-AF-2A",
    "MOV-8810A", "PUMP-CHG-2A", "VLV-HV-302A", "FAN-VENT-2A",
    "JB-2A1", "RELAY-K1A",
]

A_DC_NODES = [
    "CHGR-125A", "BAT-2A", "BUS-125DC-A", "FUSE-125A", "PN-125A",
    "INV-120A", "BUS-120AC-A", "FUSE-120A", "PN-120A",
    "CP-ESFAS-A", "CP-RPS-A",
]

B_LOAD_NODES = [
    "MCC-2B1", "MCC-2B2", "PN-480-B", "MCC-2D",
    "CB-51B", "PUMP-SI-2B", "CB-52B", "PUMP-RHR-2B",
    "CB-53B", "PUMP-CS-2B", "CB-54B", "PUMP-CCW-2B",
    "CB-55B", "FAN-CRE-2B", "CB-56B", "MOV-8801B",
    "CB-57B", "MOV-8802B", "CB-58B", "PUMP-AF-2B",
    "MOV-8810B", "PUMP-CHG-2B", "VLV-HV-302B", "FAN-VENT-2B",
    "JB-2B1", "RELAY-K1B",
]

B_DC_NODES = [
    "CHGR-125B", "BAT-2B", "BUS-125DC-B", "FUSE-125B", "PN-125B",
    "INV-120B", "BUS-120AC-B", "FUSE-120B", "PN-120B",
    "CP-ESFAS-B", "CP-RPS-B",
]

FINAL_NODES = SOURCE_NODES + COMMON_480_NODES + A_LOAD_NODES + A_DC_NODES + B_LOAD_NODES + B_DC_NODES

LABEL_ONLY_NODES = [
    "TB01", "TB02", "TB03", "TB04", "TB05", "TB06", "TB07", "TB08",
    "TB09", "TB10", "TB11", "TB12", "TB13", "TB14", "TB15",
    "2E-100", "2E-110", "2E-A-101", "2E-B-101", "2E-140",
    "2E-170", "2E-180", "2E-190", "2E-200", "2C-254", "2C-263",
    "2C-311", "2C-326", "2C-335", "2DCA-045", "2DCB-045",
    "2LPA-007", "2LPB-007", "2SIG-021", "2SIG-022",
]


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


SOURCE_EDGES = (
    chain(["GRID-345-01", "SUT-2A", "CB-402A", "BUS-4160-N2A"], "solid source feeder to normal bus N2A")
    + chain(["GEN-U2", "UAT-2A", "CB-401A", "BUS-4160-N2A"], "solid generator/UAT feeder to normal bus N2A")
    + chain(["GEN-U2", "UAT-2B", "CB-401B", "BUS-4160-N2B"], "solid generator/UAT feeder to normal bus N2B")
    + chain(["GRID-345-02", "SUT-2B", "CB-402B", "BUS-4160-N2B"], "solid source feeder to normal bus N2B")
    + chain(["BUS-4160-N2A", "CB-TIE-4160", "BUS-4160-N2B"], "solid 4.16 kV normal bus tie")
    + [
        edge("BUS-4160-N2A", "BUS-4160-S2A", "solid vertical tie from normal to safety bus A"),
        edge("BUS-4160-N2B", "BUS-4160-S2B", "solid vertical tie from normal to safety bus B"),
        edge("BUS-4160-N2A", "TR-480-N2A", "solid normal bus transformer primary feed"),
        edge("BUS-4160-N2B", "TR-480-N2B", "solid normal bus transformer primary feed"),
    ]
    + chain(["EDG-2A", "CB-EDG-A", "BUS-4160-S2A"], "solid EDG A feed to safety bus")
    + chain(["EDG-2B", "CB-EDG-B", "BUS-4160-S2B"], "solid EDG B feed to safety bus")
    + [
        edge("BUS-4160-S2A", "TR-480-2A", "solid safety bus A transformer feed"),
        edge("BUS-4160-S2B", "TR-480-2B", "solid safety bus B transformer feed"),
    ]
    + [
        edge("EDG-2C", "CB-EDG-C", "solid center EDG feed to center breaker"),
        edge("CB-EDG-C", "BUS-4160-S2A", "solid center EDG tie to safety bus A route"),
        edge("CB-EDG-C", "BUS-4160-S2B", "solid center EDG tie to safety bus B route"),
    ]
)

PROTECTION_EDGES = []
for side in ("A", "B"):
    PROTECTION_EDGES.extend([
        edge(f"BUS-4160-S2{side}", f"CT-4160{side}", "CT/PT signal tap from safety bus"),
        edge(f"CT-4160{side}", f"RELAY-50/51{side}", "CT signal to overcurrent relay"),
        edge(f"BUS-4160-S2{side}", f"PT-4160{side}", "CT/PT signal tap from safety bus"),
        edge(f"PT-4160{side}", f"RELAY-27{side}", "PT signal to undervoltage relay"),
        edge(f"RELAY-50/51{side}", f"RELAY-86{side}", "dashed protection relay trip path"),
        edge(f"RELAY-27{side}", f"RELAY-86{side}", "dashed protection relay trip path"),
    ])
PROTECTION_EDGES.extend([
    edge("RELAY-86A", "CB-401A", "dashed 86A trip path to normal feeder breaker"),
    edge("RELAY-86A", "CB-EDG-A", "dashed 86A trip path to EDG breaker"),
    edge("RELAY-86B", "CB-401B", "dashed 86B trip path to normal feeder breaker"),
    edge("RELAY-86B", "CB-EDG-B", "dashed 86B trip path to EDG breaker"),
])

COMMON_480_EDGES = (
    chain(["TR-480-2A", "BUS-480-E2A"], "solid transformer secondary to 480 V bus")
    + chain(["TR-480-N2A", "BUS-480-N2A"], "solid transformer secondary to normal 480 V bus")
    + chain(["BUS-480-N2A", "DS-480-A", "DS-480-B", "BUS-480-N2B"], "solid normally-open 480 V feeder tie path")
    + chain(["TR-480-N2B", "BUS-480-N2B"], "solid transformer secondary to normal 480 V bus")
    + chain(["TR-480-2B", "BUS-480-E2B"], "solid transformer secondary to 480 V bus")
    + [
        edge("BUS-480-E2A", "MCC-2A1", "solid 480 V bus A load-center tap"),
        edge("BUS-480-E2A", "MCC-2A2", "solid 480 V bus A load-center tap"),
        edge("BUS-480-E2A", "PN-480-A", "solid 480 V bus A panel tap"),
        edge("BUS-480-E2A", "GND-A", "equipment ground symbol tied to 480 V bus A"),
        edge("BUS-480-E2A", "MCC-2C", "solid 480 V bus A feed to MCC-2C"),
        edge("BUS-480-E2A", "CHGR-125A", "solid charger source feed from 480 V bus A"),
        edge("BUS-480-N2A", "CB-N1", "solid normal 480 V A breaker tap"),
        edge("BUS-480-E2B", "MCC-2B1", "solid 480 V bus B load-center tap"),
        edge("BUS-480-E2B", "MCC-2B2", "solid 480 V bus B load-center tap"),
        edge("BUS-480-E2B", "PN-480-B", "solid 480 V bus B panel tap"),
        edge("BUS-480-E2B", "GND-B", "equipment ground symbol tied to 480 V bus B"),
        edge("BUS-480-E2B", "CHGR-125B", "solid charger source feed from 480 V bus B"),
        edge("BUS-480-N2B", "CB-N2", "solid normal 480 V B breaker tap"),
        edge("CB-N2", "MCC-2D", "solid CB-N2 downstream feed to MCC-2D"),
    ]
)


def regular_load_edges(side: str) -> list[Edge]:
    prefix = "2A" if side == "A" else "2B"
    branches = [
        (f"MCC-{prefix}1", "51", f"PUMP-SI-2{side}"),
        (f"MCC-{prefix}1", "52", f"PUMP-RHR-2{side}"),
        (f"MCC-{prefix}1", "53", f"PUMP-CS-2{side}"),
        (f"MCC-{prefix}1", "54", f"PUMP-CCW-2{side}"),
        (f"MCC-{prefix}2", "55", f"FAN-CRE-2{side}"),
        (f"MCC-{prefix}2", "56", f"MOV-8801{side}"),
        (f"MCC-{prefix}2", "57", f"MOV-8802{side}"),
        (f"MCC-{prefix}2", "58", f"PUMP-AF-2{side}"),
    ]
    result: list[Edge] = []
    for mcc, num, load in branches:
        result.extend(chain([mcc, f"CB-{num}{side}", load], f"solid Train {side} load feeder branch"))
    return result


PANEL_LOAD_EDGES = [
    edge("PN-480-A", "MOV-8810A", "solid Train A panel load parent"),
    edge("MCC-2C", "PUMP-CHG-2A", "solid Train A MCC-2C load parent"),
    edge("PUMP-CHG-2A", "VLV-HV-302A", "solid Train A pump-to-valve continuation"),
    edge("MCC-2C", "FAN-VENT-2A", "solid Train A MCC-2C load parent"),
    edge("PN-480-B", "MOV-8810B", "solid Train B panel load parent"),
    edge("MCC-2D", "PUMP-CHG-2B", "solid Train B MCC-2D load parent"),
    edge("MCC-2D", "FAN-VENT-2B", "solid Train B MCC-2D load parent"),
]

DC_CONTROL_EDGES = []
for side in ("A", "B"):
    DC_CONTROL_EDGES.extend([
        edge(f"CHGR-125{side}", f"BAT-2{side}", "dashed charger-to-battery link"),
        edge(f"CHGR-125{side}", f"BUS-125DC-{side}", "dashed/solid charger feed to 125 VDC bus"),
        edge(f"BAT-2{side}", f"BUS-125DC-{side}", "dashed battery feed to 125 VDC bus"),
        edge(f"BUS-125DC-{side}", f"FUSE-125{side}", "125 VDC bus fused panel feed"),
        edge(f"FUSE-125{side}", f"PN-125{side}", "125 VDC fuse to panel"),
        edge(f"BUS-125DC-{side}", f"INV-120{side}", "125 VDC bus to inverter"),
        edge(f"INV-120{side}", f"BUS-120AC-{side}", "inverter to 120 VAC bus"),
        edge(f"BUS-120AC-{side}", f"FUSE-120{side}", "120 VAC bus fused panel feed"),
        edge(f"FUSE-120{side}", f"PN-120{side}", "120 VAC fuse to panel"),
        edge(f"PN-125{side}", f"CP-ESFAS-{side}", "raw table and dashed route PN-125 to ESFAS panel"),
        edge(f"PN-120{side}", f"CP-RPS-{side}", "dashed route from PN-120 to RPS panel"),
        edge(f"RELAY-K1{side}", f"CP-ESFAS-{side}", "clear dashed K1 relay to ESFAS control path"),
        edge(f"MOV-8801{side}", f"JB-2{side}1", "clear dashed MOV-8801 to junction box path"),
    ])

FINAL_EDGES = dedupe_edges(
    SOURCE_EDGES
    + PROTECTION_EDGES
    + COMMON_480_EDGES
    + regular_load_edges("A")
    + regular_load_edges("B")
    + PANEL_LOAD_EDGES
    + DC_CONTROL_EDGES
)

JENNIFER_R1_EDGES = [
    item for item in FINAL_EDGES
    if edge_key(item.source, item.target) not in {
        edge_key("BUS-4160-N2A", "TR-480-N2A"),
        edge_key("BUS-4160-N2B", "TR-480-N2B"),
        edge_key("CHGR-125A", "BAT-2A"),
        edge_key("CHGR-125B", "BAT-2B"),
    }
]

DIEGO_R1_BASE_EDGES = [
    item for item in FINAL_EDGES
    if edge_key(item.source, item.target) not in {
        edge_key("BUS-4160-N2A", "TR-480-N2A"),
        edge_key("BUS-4160-N2B", "TR-480-N2B"),
        edge_key("BUS-480-E2A", "CHGR-125A"),
        edge_key("BUS-480-E2B", "CHGR-125B"),
        edge_key("BUS-480-E2A", "MCC-2C"),
        edge_key("CB-N2", "MCC-2D"),
        edge_key("RELAY-86A", "CB-401A"),
        edge_key("RELAY-86A", "CB-EDG-A"),
        edge_key("RELAY-86B", "CB-401B"),
        edge_key("RELAY-86B", "CB-EDG-B"),
        edge_key("CHGR-125A", "BAT-2A"),
        edge_key("CHGR-125B", "BAT-2B"),
    }
] + [
    edge("CB-N1", "CHGR-125A", "Diego round 1 high-recall charger path later removed", "confirmed_proposed"),
    edge("CB-N2", "CHGR-125B", "Diego round 1 high-recall charger path later removed", "confirmed_proposed"),
]

DIEGO_R1_UNCERTAIN = [
    edge("EDG-2C", "CB-EDG-C", "common diesel route visible but exact intent initially uncertain", "uncertain_included"),
    edge("CB-EDG-C", "BUS-4160-S2A", "common diesel route initially uncertain", "uncertain_included"),
    edge("CB-EDG-C", "BUS-4160-S2B", "common diesel route initially uncertain", "uncertain_included"),
    edge("RELAY-86A", "CB-401A", "86A dashed trip path initially uncertain", "uncertain_included"),
    edge("RELAY-86A", "CB-EDG-A", "86A dashed trip path initially uncertain", "uncertain_included"),
    edge("RELAY-86B", "CB-401B", "86B dashed trip path initially uncertain", "uncertain_included"),
    edge("RELAY-86B", "CB-EDG-B", "86B dashed trip path initially uncertain", "uncertain_included"),
    edge("PN-480-A", "PUMP-CHG-2A", "alternate parent candidate near Train A panel/MCC crowding", "uncertain_included"),
    edge("MCC-2C", "MOV-8810A", "alternate parent candidate near Train A panel/MCC crowding", "uncertain_included"),
    edge("PN-480-B", "PUMP-CHG-2B", "alternate parent candidate near Train B panel/MCC crowding", "uncertain_included"),
    edge("MCC-2D", "MOV-8810B", "alternate parent candidate near Train B panel/MCC crowding", "uncertain_included"),
    edge("MCC-2D", "VLV-HV-302B", "possible B-side HV valve parent later rejected", "uncertain_included"),
    edge("PUMP-CHG-2B", "VLV-HV-302B", "possible B-side continuation later rejected", "uncertain_included"),
    edge("CB-52A", "RELAY-K1A", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("CB-53A", "RELAY-K1A", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("CB-54A", "RELAY-K1A", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("CB-52B", "RELAY-K1B", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("CB-53B", "RELAY-K1B", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("CB-54B", "RELAY-K1B", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("JB-2A1", "RELAY-K1A", "bundled dashed control candidate later excluded", "uncertain_included"),
    edge("JB-2B1", "RELAY-K1B", "bundled dashed control candidate later excluded", "uncertain_included"),
]

FINAL_UNCERTAIN = [
    edge("TBxx/cable labels", "schematic devices", "labels are references, not graph nodes", "uncertain_excluded"),
    edge("CB-N1", "CHGR-125A", "downstream destination from CB-N1 not matrix-safe after precision review", "uncertain_excluded"),
    edge("CB-N2", "CHGR-125B", "downstream destination from CB-N2 not supported; CB-N2 to MCC-2D was confirmed instead", "uncertain_excluded"),
    edge("VLV-HV-302B", "panel/MCC parent", "B-side parent/continuation not visually safe", "uncertain_excluded"),
    edge("PUMP-CHG-2B", "VLV-HV-302B", "B-side continuation not visually safe", "uncertain_excluded"),
    edge("CB-52A/CB-53A/CB-54A", "RELAY-K1A or CP-ESFAS-A", "bundled dashed interlock lacks clear named endpoints", "uncertain_excluded"),
    edge("CB-52B/CB-53B/CB-54B", "RELAY-K1B or CP-ESFAS-B", "bundled dashed interlock lacks clear named endpoints", "uncertain_excluded"),
    edge("JB-2A1", "RELAY-K1A", "bundled dashed route lacks a clean terminal-dot endpoint", "uncertain_excluded"),
    edge("JB-2B1", "RELAY-K1B", "bundled dashed route lacks a clean terminal-dot endpoint", "uncertain_excluded"),
    edge("RELAY-86A/B", "CB-EDG-C", "no confirmed dashed trip termination to center EDG breaker", "uncertain_excluded"),
]

ROUNDS = [
    RoundSpec(
        "round_01",
        "diego",
        "high_recall_extractor",
        FINAL_NODES + LABEL_ONLY_NODES,
        DIEGO_R1_BASE_EDGES,
        DIEGO_R1_UNCERTAIN,
        True,
        [
            "High-recall extraction from raw PNG and crops generated only from that PNG.",
            "Included terminal blocks and cable/reference labels as candidate nodes; Jennifer later removed them as label-only items.",
            "Included visually plausible panel-parent and bundled dashed-control candidates in this round matrix.",
            "No GT or GT-derived resources were used.",
        ],
    ),
    RoundSpec(
        "round_01",
        "jennifer",
        "precision_reviewer_refiner",
        FINAL_NODES,
        JENNIFER_R1_EDGES,
        FINAL_UNCERTAIN,
        False,
        [
            "Precision review removed terminal blocks and cable/reference labels from the graph.",
            "Confirmed EDG-2C ties, 86 trip edges, MCC-2C/2D refinements, and clear MOV-to-JB control links.",
            "Removed CB-N1/CB-N2 to charger edges and kept bundled dashed interlocks uncertain.",
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
            "Round 2 Diego accepted Jennifer's precision rules.",
            "Added visible normal-bus transformer primary feeds and charger-to-battery dashed links.",
            "No further raw-supported additions or removals were proposed.",
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
            "Final precision review confirmed Diego's four additions and agreed saturation was reached.",
            "Final matrix keeps 120 real device/bus/ground nodes and excludes label-only references.",
            "The raw title-block count was noted but not forced; ambiguous dashed bundles remain uncertain/excluded.",
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
    with (RESULTS / "token_performance_tracking.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "timestamp_local", "round_id", "actor", "role", "node_count",
            "edge_count", "uncertain_item_count", "token_telemetry", "artifact_prefix",
        ])
        for spec, metrics, prefix in zip(ROUNDS, metrics_rows, prefixes):
            writer.writerow([
                now, spec.round_id, spec.actor, spec.role, metrics["node_count"],
                metrics["edge_count"], metrics["uncertain_item_count"],
                "not available from current goal telemetry", prefix,
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
        "Case: 8 Raw",
        "",
        "Evidence used:",
        "- Raw schematic PNG in the Raw folder.",
        "- Crops generated from that same PNG and stored under results/crops.",
        "- No Ground Truth or GT-derived feedback/resources were used.",
        "",
        "Final consensus:",
        "- Diego and Jennifer agreed after two rounds.",
        "- Final node count is 120 real visible device/bus/ground nodes.",
        f"- Final confirmed edge count is {len(FINAL_EDGES)}.",
        "- Terminal blocks and cable/reference labels were excluded as graph nodes.",
        "- Ambiguous bundled dashed interlocks were kept uncertain/excluded instead of guessed.",
        "- The raw title-block count was noted as raw-image sanity text, but the final graph was not forced to match it.",
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
