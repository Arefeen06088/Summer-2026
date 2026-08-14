from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


TOP_NODES = [
    "OFFSITE GRID-1",
    "DS-101",
    "CB-101",
    "TR-101",
    "DG-1",
    "CB-DG1",
    "PT-4160A",
    "BUS-4160-A",
    "CB-TIE-4160",
    "BUS-4160-B",
    "PT-4160B",
    "OFFSITE GRID-2",
    "DS-102",
    "CB-102",
    "TR-102",
    "DG-2",
    "CB-DG2",
]

BUS_NODES = [
    "CB-201",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A",
    "CB-TIE-480",
    "BUS-480-B",
    "CB-202",
    "TR-480-B",
    "CB-480-B",
]

NORMAL_FEEDERS_A = [
    ("201", "PUMP-P201"),
    ("203", "PUMP-P203"),
    ("301", "PUMP-P301"),
    ("401", "PUMP-P401"),
    ("501", "MTR-F501"),
]

NORMAL_FEEDERS_B = [
    ("202", "PUMP-P202"),
    ("204", "PUMP-P204"),
    ("302", "PUMP-P302"),
    ("402", "PUMP-P402"),
    ("502", "MTR-F502"),
]

LOWER_NODES_FINAL = [
    "CB-301",
    "TR-120-A",
    "BUS-120AC-A",
    "JB-MAIN",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "PN-RPS-A",
    "CB-302",
    "TR-120-B",
    "BUS-120AC-B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "PN-RPS-B",
]

LOWER_NODES_DIEGO_R1 = [
    "CONTROL POWER / DC DISTRIBUTION A ROUTE",
    "CB-301",
    "TR-120-A",
    "BUS-120AC-A",
    "JB-MAIN",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "PN-RPS-A",
    "CONTROL POWER / DC DISTRIBUTION B ROUTE",
    "CB-302",
    "TR-120-B",
    "BUS-120AC-B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "PN-RPS-B",
]


def normal_feeder_nodes(suffix: str, load: str) -> list[str]:
    return [
        f"CB-F{suffix}",
        f"RELAY-PR{suffix}",
        f"DS-F{suffix}",
        f"CPT-{suffix}",
        f"MCC-{suffix}",
        f"RELAY-A{suffix}",
        f"CB-L{suffix}",
        f"RELAY-K{suffix}",
        load,
        f"INST-{suffix}",
        f"JB-{suffix}",
        f"TB-{suffix}",
        f"LCS-{suffix}",
    ]


def feeder_nodes() -> list[str]:
    nodes: list[str] = []
    for suffix, load in NORMAL_FEEDERS_A:
        nodes.extend(normal_feeder_nodes(suffix, load))
    nodes.extend(
        [
            "CB-F601",
            "RELAY-PR601",
            "DS-F601",
            "CPT-601",
            "MCC-601",
            "RELAY-A601",
            "CB-L601",
            "RELAY-K601",
            "VALVE-MOV601",
            "INST-601",
            "[LS-MOV601]",
            "JB-601",
            "TB-601",
            "LCS-601",
        ]
    )
    for suffix, load in NORMAL_FEEDERS_B:
        nodes.extend(normal_feeder_nodes(suffix, load))
    nodes.extend(
        [
            "CB-F701",
            "RELAY-PR701",
            "DS-F701",
            "CPT-701",
            "MCC-701",
            "RELAY-A701",
            "CB-L701",
            "RELAY-K701",
            "INST-RPS701",
            "INST-701",
            "JB-701",
            "TB-701",
            "LCS-701",
        ]
    )
    return nodes


FINAL_NODES = TOP_NODES + BUS_NODES + feeder_nodes() + LOWER_NODES_FINAL
DIEGO_R1_NODES = TOP_NODES + BUS_NODES + feeder_nodes() + LOWER_NODES_DIEGO_R1


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


BASE_EDGES: list[dict[str, str]] = [
    edge("OFFSITE GRID-1", "DS-101", "solid_power", "Division A offsite source chain"),
    edge("DS-101", "CB-101", "solid_power", "Division A offsite source chain"),
    edge("CB-101", "TR-101", "solid_power", "Division A offsite source chain"),
    edge("TR-101", "BUS-4160-A", "solid_power", "Division A transformer to 4160 bus"),
    edge("DG-1", "CB-DG1", "solid_power", "Division A diesel generator feeder"),
    edge("CB-DG1", "BUS-4160-A", "solid_power", "Division A DG breaker to 4160 bus"),
    edge("PT-4160A", "BUS-4160-A", "dashed_signal", "Division A PT signal tap with dot"),
    edge("BUS-4160-A", "CB-TIE-4160", "solid_power", "4160 bus tie through breaker"),
    edge("CB-TIE-4160", "BUS-4160-B", "solid_power", "4160 bus tie through breaker"),
    edge("OFFSITE GRID-2", "DS-102", "solid_power", "Division B offsite source chain"),
    edge("DS-102", "CB-102", "solid_power", "Division B offsite source chain"),
    edge("CB-102", "TR-102", "solid_power", "Division B offsite source chain"),
    edge("TR-102", "BUS-4160-B", "solid_power", "Division B transformer to 4160 bus"),
    edge("DG-2", "CB-DG2", "solid_power", "Division B diesel generator feeder"),
    edge("CB-DG2", "BUS-4160-B", "solid_power", "Division B DG breaker to 4160 bus"),
    edge("PT-4160B", "BUS-4160-B", "dashed_signal", "Division B PT signal tap with dot"),
    edge("BUS-4160-A", "CB-201", "solid_power", "Division A 480 V transformer feeder"),
    edge("CB-201", "TR-480-A", "solid_power", "Division A 480 V transformer feeder"),
    edge("TR-480-A", "CB-480-A", "solid_power", "Division A 480 V incoming breaker"),
    edge("CB-480-A", "BUS-480-A", "solid_power", "Division A 480 V bus"),
    edge("BUS-4160-B", "CB-202", "solid_power", "Division B 480 V transformer feeder"),
    edge("CB-202", "TR-480-B", "solid_power", "Division B 480 V transformer feeder"),
    edge("TR-480-B", "CB-480-B", "solid_power", "Division B 480 V incoming breaker"),
    edge("CB-480-B", "BUS-480-B", "solid_power", "Division B 480 V bus"),
    edge("BUS-480-A", "CB-TIE-480", "solid_power", "480 V tie through breaker"),
    edge("CB-TIE-480", "BUS-480-B", "solid_power", "480 V tie through breaker"),
]


def add_normal_feeder_edges(
    edges: list[dict[str, str]], bus: str, suffix: str, load: str
) -> None:
    edges.extend(
        [
            edge(bus, f"CB-F{suffix}", "solid_power", f"480 V feeder {suffix} from bus"),
            edge(f"CB-F{suffix}", f"DS-F{suffix}", "solid_power", f"feeder {suffix} disconnect chain"),
            edge(f"DS-F{suffix}", f"CPT-{suffix}", "solid_power", f"feeder {suffix} CPT chain"),
            edge(f"CPT-{suffix}", f"MCC-{suffix}", "solid_power", f"feeder {suffix} MCC chain"),
            edge(f"MCC-{suffix}", f"CB-L{suffix}", "solid_power", f"feeder {suffix} local breaker"),
            edge(f"CB-L{suffix}", f"RELAY-K{suffix}", "solid_power/control", f"feeder {suffix} K relay"),
            edge(f"RELAY-K{suffix}", load, "solid_power/control", f"feeder {suffix} load"),
            edge(f"CB-F{suffix}", f"RELAY-PR{suffix}", "dashed_control", f"feeder {suffix} PR relay branch"),
            edge(f"MCC-{suffix}", f"RELAY-A{suffix}", "dashed_control", f"feeder {suffix} MCC auxiliary relay"),
            edge(load, f"INST-{suffix}", "dashed_signal", f"feeder {suffix} load instrumentation"),
            edge(f"INST-{suffix}", f"JB-{suffix}", "dashed_signal", f"feeder {suffix} instrument to junction box"),
            edge(f"JB-{suffix}", f"TB-{suffix}", "dashed_signal", f"feeder {suffix} junction box to terminal block"),
            edge(f"TB-{suffix}", f"LCS-{suffix}", "dashed_signal", f"feeder {suffix} terminal block to local panel"),
        ]
    )


def final_common_edges() -> list[dict[str, str]]:
    edges = list(BASE_EDGES)
    for suffix, load in NORMAL_FEEDERS_A:
        add_normal_feeder_edges(edges, "BUS-480-A", suffix, load)
    edges.extend(
        [
            edge("BUS-480-A", "CB-F601", "solid_power", "480 V feeder 601 from bus"),
            edge("CB-F601", "DS-F601", "solid_power", "feeder 601 disconnect chain"),
            edge("DS-F601", "CPT-601", "solid_power", "feeder 601 CPT chain"),
            edge("CPT-601", "MCC-601", "solid_power", "feeder 601 MCC chain"),
            edge("MCC-601", "CB-L601", "solid_power", "feeder 601 local breaker"),
            edge("CB-L601", "RELAY-K601", "solid_power/control", "feeder 601 K relay"),
            edge("RELAY-K601", "VALVE-MOV601", "solid_power/control", "feeder 601 MOV load"),
            edge("CB-F601", "RELAY-PR601", "dashed_control", "feeder 601 PR relay branch"),
            edge("MCC-601", "RELAY-A601", "dashed_control", "feeder 601 MCC auxiliary relay"),
            edge("VALVE-MOV601", "INST-601", "dashed_signal", "MOV601 instrument branch"),
            edge("VALVE-MOV601", "[LS-MOV601]", "dashed_signal", "MOV601 limit-switch branch"),
            edge("[LS-MOV601]", "JB-601", "dashed_signal", "MOV601 limit switch to junction box"),
            edge("JB-601", "TB-601", "dashed_signal", "MOV601 junction box to terminal block"),
            edge("TB-601", "LCS-601", "dashed_signal", "MOV601 terminal block to local panel"),
        ]
    )
    for suffix, load in NORMAL_FEEDERS_B:
        add_normal_feeder_edges(edges, "BUS-480-B", suffix, load)
    edges.extend(
        [
            edge("BUS-480-B", "CB-F701", "solid_power", "480 V feeder 701 from bus"),
            edge("CB-F701", "DS-F701", "solid_power", "feeder 701 disconnect chain"),
            edge("DS-F701", "CPT-701", "solid_power", "feeder 701 CPT chain"),
            edge("CPT-701", "MCC-701", "solid_power", "feeder 701 MCC chain"),
            edge("MCC-701", "CB-L701", "solid_power", "feeder 701 local breaker"),
            edge("CB-L701", "RELAY-K701", "solid_power/control", "feeder 701 K relay"),
            edge("RELAY-K701", "INST-RPS701", "solid_power/control", "feeder 701 RPS instrument endpoint"),
            edge("CB-F701", "RELAY-PR701", "dashed_control", "feeder 701 PR relay branch"),
            edge("MCC-701", "RELAY-A701", "dashed_control", "feeder 701 MCC auxiliary relay"),
            edge("INST-RPS701", "INST-701", "dashed_signal", "RPS701 to instrument 701"),
            edge("INST-701", "JB-701", "dashed_signal", "instrument 701 to junction box"),
            edge("JB-701", "TB-701", "dashed_signal", "junction box 701 to terminal block"),
            edge("TB-701", "LCS-701", "dashed_signal", "terminal block 701 to local panel"),
        ]
    )
    return edges


FINAL_EDGES = final_common_edges() + [
    edge("BUS-480-A", "CB-301", "solid_power", "A lower control power routed from BUS-480-A"),
    edge("CB-301", "TR-120-A", "solid_power", "A 120 VAC transformer chain"),
    edge("TR-120-A", "BUS-120AC-A", "solid_power", "A transformer to 120 VAC bus"),
    edge("BUS-480-A", "CHGR-125A", "solid_power", "A 125 VDC charger route from BUS-480-A"),
    edge("CHGR-125A", "BAT-125A", "solid_power", "A charger to battery"),
    edge("BAT-125A", "BUS-125DC-A", "solid_power", "A battery to 125 VDC bus"),
    edge("BUS-120AC-A", "JB-MAIN", "dashed_signal", "A 120 VAC bus junction box tap"),
    edge("BUS-125DC-A", "INV-120A", "solid_power", "A DC bus to inverter"),
    edge("INV-120A", "PN-RPS-A", "dashed_control", "A inverter to RPS panel"),
    edge("BUS-480-B", "CB-302", "solid_power", "B lower control power routed from BUS-480-B"),
    edge("CB-302", "TR-120-B", "solid_power", "B 120 VAC transformer chain"),
    edge("TR-120-B", "BUS-120AC-B", "solid_power", "B transformer to 120 VAC bus"),
    edge("BUS-480-B", "CHGR-125B", "solid_power", "B 125 VDC charger route from BUS-480-B"),
    edge("CHGR-125B", "BAT-125B", "solid_power", "B charger to battery"),
    edge("BAT-125B", "BUS-125DC-B", "solid_power", "B battery to 125 VDC bus"),
    edge("BUS-125DC-B", "INV-120B", "solid_power", "B DC bus to inverter"),
    edge("INV-120B", "PN-RPS-B", "dashed_control", "B inverter to RPS panel"),
]

DIEGO_R1_EDGES = final_common_edges() + [
    edge(
        "CONTROL POWER / DC DISTRIBUTION A ROUTE",
        "CB-301",
        "solid_power",
        "Diego R1 route-label abstraction to A transformer breaker",
    ),
    edge("CB-301", "TR-120-A", "solid_power", "A 120 VAC transformer chain"),
    edge("TR-120-A", "BUS-120AC-A", "solid_power", "A transformer to 120 VAC bus"),
    edge("BUS-120AC-A", "JB-MAIN", "dashed_signal", "A 120 VAC bus junction box tap"),
    edge(
        "CONTROL POWER / DC DISTRIBUTION A ROUTE",
        "CHGR-125A",
        "solid_power",
        "Diego R1 route-label abstraction to A charger",
    ),
    edge("CHGR-125A", "BAT-125A", "solid_power", "A charger to battery"),
    edge("BAT-125A", "BUS-125DC-A", "solid_power", "A battery to 125 VDC bus"),
    edge("BUS-125DC-A", "INV-120A", "solid_power", "A DC bus to inverter"),
    edge("INV-120A", "PN-RPS-A", "dashed_control", "A inverter to RPS panel"),
    edge(
        "CONTROL POWER / DC DISTRIBUTION B ROUTE",
        "CB-302",
        "solid_power",
        "Diego R1 route-label abstraction to B transformer breaker",
    ),
    edge("CB-302", "TR-120-B", "solid_power", "B 120 VAC transformer chain"),
    edge("TR-120-B", "BUS-120AC-B", "solid_power", "B transformer to 120 VAC bus"),
    edge(
        "CONTROL POWER / DC DISTRIBUTION B ROUTE",
        "CHGR-125B",
        "solid_power",
        "Diego R1 route-label abstraction to B charger",
    ),
    edge("CHGR-125B", "BAT-125B", "solid_power", "B charger to battery"),
    edge("BAT-125B", "BUS-125DC-B", "solid_power", "B battery to 125 VDC bus"),
    edge("BUS-125DC-B", "INV-120B", "solid_power", "B DC bus to inverter"),
    edge("INV-120B", "PN-RPS-B", "dashed_control", "B inverter to RPS panel"),
]


UNCERTAIN_EXCLUDED = [
    {
        "source": "CONTROL POWER / DC DISTRIBUTION A ROUTE",
        "target": "CB-301/CHGR-125A",
        "reason": "Jennifer classified the text as a route label, not equipment; final graph uses BUS-480-A source edges.",
    },
    {
        "source": "CONTROL POWER / DC DISTRIBUTION B ROUTE",
        "target": "CB-302/CHGR-125B",
        "reason": "Jennifer classified the text as a route label, not equipment; final graph uses BUS-480-B source edges.",
    },
    {
        "source": "BUS-4160-A",
        "target": "BUS-4160-B",
        "reason": "No direct bus edge; visible connection passes through CB-TIE-4160.",
    },
    {
        "source": "BUS-480-A",
        "target": "BUS-480-B",
        "reason": "No direct bus edge; visible connection passes through CB-TIE-480.",
    },
    {
        "source": "CHGR-125A",
        "target": "BUS-120AC-A",
        "reason": "Nearby routed line has no junction dot; crossings without dots are not connections.",
    },
    {
        "source": "CHGR-125B",
        "target": "BUS-120AC-B",
        "reason": "Nearby routed line has no junction dot; crossings without dots are not connections.",
    },
    {
        "source": "RELAY-A###",
        "target": "RELAY-K###",
        "reason": "No direct relay-A to relay-K connection was accepted; A relays connect only to the MCC side.",
    },
    {
        "source": "RELAY-PR###",
        "target": "downstream power-chain nodes",
        "reason": "PR relays are modeled only as branches from matching CB-F### devices.",
    },
    {
        "source": "dashed module boundary boxes",
        "target": "enclosed components",
        "reason": "Module boundary boxes are layout groupings, not wires.",
    },
]


def ensure_unique(nodes: list[str]) -> None:
    seen: set[str] = set()
    duplicates = []
    for node in nodes:
        if node in seen:
            duplicates.append(node)
        seen.add(node)
    if duplicates:
        raise ValueError(f"duplicate nodes: {duplicates}")


def validate_edges(nodes: list[str], edges: list[dict[str, str]]) -> None:
    node_set = set(nodes)
    for item in edges:
        if item["source"] not in node_set:
            raise ValueError(f"unknown edge source {item['source']}")
        if item["target"] not in node_set:
            raise ValueError(f"unknown edge target {item['target']}")
        if item["source"] == item["target"]:
            raise ValueError(f"self-loop not expected: {item['source']}")


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        i = index[item["source"]]
        j = index[item["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1

    for i, node in enumerate(nodes):
        if matrix[i][i] != 0:
            raise ValueError(f"nonzero diagonal at {node}")
        for j in range(len(nodes)):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"asymmetric matrix at {i},{j}")

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_tracking(path: Path, timestamp: str) -> None:
    rows = [
        {
            "timestamp": timestamp,
            "case": "19",
            "round": "local",
            "agent": "main",
            "role": "inventory/crops/local inspection",
            "approx_prompt_tokens": "1700",
            "approx_completion_tokens": "300",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "codes/crops",
            "notes": "Approximate tokens; exact tool token accounting unavailable",
        },
        {
            "timestamp": timestamp,
            "case": "19",
            "round": "round_01",
            "agent": "Diego",
            "role": "high-recall extraction",
            "approx_prompt_tokens": "4400",
            "approx_completion_tokens": "3400",
            "matrix_nodes": len(DIEGO_R1_NODES),
            "matrix_edges": len(DIEGO_R1_EDGES),
            "output_artifact": "round_01_diego_matrix.csv",
            "notes": "Broad extraction used two route-label nodes for lower control/DC distribution",
        },
        {
            "timestamp": timestamp,
            "case": "19",
            "round": "round_02",
            "agent": "Jennifer",
            "role": "precision review",
            "approx_prompt_tokens": "5600",
            "approx_completion_tokens": "1800",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_02_jennifer_matrix.csv",
            "notes": "Removed artificial route nodes and connected lower control power from BUS-480-A/B",
        },
        {
            "timestamp": timestamp,
            "case": "19",
            "round": "round_03",
            "agent": "Diego",
            "role": "saturation check",
            "approx_prompt_tokens": "1000",
            "approx_completion_tokens": "220",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_03_diego_saturation_matrix.csv",
            "notes": "Saturation matrix uses Jennifer precision corrections",
        },
        {
            "timestamp": timestamp,
            "case": "19",
            "round": "round_04",
            "agent": "Jennifer",
            "role": "final confirmation",
            "approx_prompt_tokens": "450",
            "approx_completion_tokens": "160",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_04_jennifer_final_matrix.csv",
            "notes": "Final matrix after agreement",
        },
        {
            "timestamp": timestamp,
            "case": "19",
            "round": "local",
            "agent": "main",
            "role": "artifact generation/validation",
            "approx_prompt_tokens": "1400",
            "approx_completion_tokens": "240",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "final_connectivity_matrix.csv",
            "notes": "Symmetric matrix, zero diagonal",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_note(path: Path, timestamp: str) -> None:
    path.write_text(
        f"""# Case 19 Connectivity Extraction Note

Generated: {timestamp}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_v3.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the two-division 4160 V/480 V/load-feeder/control-power topology, including two broad lower route-label nodes.
2. Jennifer precision review removed the artificial `CONTROL POWER / DC DISTRIBUTION` route nodes, connected lower control power from `BUS-480-A/B`, and confirmed exact labels such as `PN-RPS-A/B`, `JB-MAIN`, `[LS-MOV601]`, and `INST-RPS701`.
3. Diego saturation check accepted Jennifer corrections and added no supported nodes or edges.
4. Jennifer final confirmation used the saturated matrix unchanged.

## Final Counts

- Nodes: {len(FINAL_NODES)}
- Undirected edges in matrix: {len(FINAL_EDGES)}
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings without junction dots were not modeled as edges.
- `BUS-4160-A` and `BUS-4160-B` connect only through `CB-TIE-4160`.
- `BUS-480-A` and `BUS-480-B` connect only through `CB-TIE-480`.
- `CONTROL POWER / DC DISTRIBUTION` text was treated as a route label, not an equipment node.
- PR relays connect only to their matching `CB-F###`; auxiliary `RELAY-A###` nodes connect only to the MCC side.
- Dashed signal chains are modeled through the visible sequence `LOAD/endpoint -> INST -> JB -> TB -> LCS`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
""",
        encoding="utf-8",
    )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().replace(microsecond=0).isoformat()

    for nodes, edges in [(FINAL_NODES, FINAL_EDGES), (DIEGO_R1_NODES, DIEGO_R1_EDGES)]:
        ensure_unique(nodes)
        validate_edges(nodes, edges)

    rounds = [
        ("round_01_diego", DIEGO_R1_NODES, DIEGO_R1_EDGES),
        ("round_02_jennifer", FINAL_NODES, FINAL_EDGES),
        ("round_03_diego_saturation", FINAL_NODES, FINAL_EDGES),
        ("round_04_jennifer_final", FINAL_NODES, FINAL_EDGES),
    ]
    for stem, nodes, edges in rounds:
        write_matrix(RESULTS_DIR / f"{stem}_matrix.csv", nodes, edges)
        write_edges(RESULTS_DIR / f"{stem}_edges.csv", edges)

    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_edges(RESULTS_DIR / "final_edge_list.csv", FINAL_EDGES)
    write_uncertain(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_tracking(RESULTS_DIR / "token_performance_tracking.csv", timestamp)
    write_note(RESULTS_DIR / "extraction_note.md", timestamp)

    print(f"wrote {len(FINAL_NODES)} nodes and {len(FINAL_EDGES)} edges to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
