from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


TOP_NODES = [
    "GRID-SWYD-1",
    "CB-GRID-A",
    "GRID-SWYD-2",
    "CB-GRID-B",
    "BB-SWYD-230",
    "TR-SAT-1A",
    "CB-SAT-A",
    "BUS-4160A",
    "DG-1A",
    "CB-DG-A",
    "PT-4160A",
    "FU-PT-A",
    "XFMR-CTRL-A",
    "TB-RPS-A",
    "SW-43A",
    "CB-4160-TIE",
    "GND-4160A",
    "TR-480-A1",
    "CB-480A-IN",
    "BUS-480A",
    "TR-480-B1",
    "CB-480B-IN",
    "BUS-480B",
    "TR-SAT-1B",
    "CB-SAT-B",
    "BUS-4160B",
    "GND-4160B",
    "PT-4160B",
    "FU-PT-B",
    "XFMR-CTRL-B",
    "TB-RPS-B",
    "SW-43B",
    "TR-480-C1",
    "CB-480C-IN",
    "BUS-480C",
    "CB-GEN-ISO",
    "GEN-MAIN-1",
    "TR-UAT-1A",
    "CB-UAT-A",
    "TR-UAT-1B",
    "CB-UAT-B",
    "DG-1B",
    "CB-DG-B",
    "TR-480-D1",
    "CB-480D-IN",
    "BUS-480D",
]


BRANCHES_A = [
    ("CB-A01", "DS-A01", "MS-A01", "PUMP-CCW-A1"),
    ("CB-A02", "DS-A02", "MS-A02", "PUMP-RHR-A1"),
    ("CB-A03", "FS-A03", "MS-A03", "FAN-RB-A1"),
    ("CB-A04", "DS-A04", "RY-A04", "MOV-SI-A11"),
    ("CB-A05", "DS-A05", "CP-A05", "PNL-LTG-A1"),
    ("CB-A06", "DS-A06", "MS-A06", "PUMP-AFW-A1"),
    ("CB-A07", "FS-A07", "FU-A07", "HTR-PZR-A1"),
    ("CB-A08", "DS-A08", "TB-A08", "SPARE-A8"),
]

BRANCHES_B = [
    ("CB-B01", "DS-B01", "MS-B01", "PUMP-CCW-B1"),
    ("CB-B02", "DS-B02", "MS-B02", "PUMP-RHR-B1"),
    ("CB-B03", "FS-B03", "MS-B03", "FAN-FUEL-B1"),
    ("CB-B04", "DS-B04", "RY-B04", "MOV-CCW-B21"),
    ("CB-B05", "DS-B05", "CP-B05", "MCC-AUX-B6"),
    ("CB-B06", "DS-B06", "MS-B06", "AIR-CMP-B1"),
    ("CB-B07", "FS-B07", "RY-B07", "VLV-CHG-B1"),
]

BRANCHES_C = [
    ("CB-C01", "DS-C01", "MS-C01", "PUMP-HPCI-C1"),
    ("CB-C02", "DS-C02", "MS-C02", "PUMP-RCW-C1"),
    ("CB-C03", "FS-C03", "MS-C03", "FAN-RB-C1"),
    ("CB-C04", "DS-C04", "RY-C04", "MOV-RHR-C11"),
    ("CB-C05", "DS-C05", "MS-C05", "PUMP-SEAL-C1"),
    ("CB-C06", "DS-C06", "CP-C06", "PNL-1C-C7"),
    ("CB-C07", "FS-C07", "MS-C07", "SUMP-PMP-C1"),
    ("CB-C08", "DS-C08", "FU-C08", "HTR-VENT-C2"),
]

BRANCHES_D = [
    ("CB-D01", "DS-D01", "MS-D01", "PUMP-AFW-D1"),
    ("CB-D02", "DS-D02", "MS-D02", "FAN-CR-D1"),
    ("CB-D03", "FS-D03", "RY-D03", "MOV-SI-D21"),
    ("CB-D04", "DS-D04", "MS-D04", "PUMP-LUBE-D1"),
    ("CB-D05", "DS-D05", "CP-D05", "PNL-ESS-D5"),
    ("CB-D06", "DS-D06", "MS-D06", "COMP-AIR-D1"),
    ("CB-D07", "FS-D07", "TB-D07", "SPARE-D7"),
]


LOWER_NODES = [
    "CHG-125A",
    "REC-125A",
    "CB-DC-A",
    "BUS-125A",
    "BAT-125A",
    "GND-DC-A",
    "INV-120A",
    "UPS-120A",
    "BUS-120A",
    "RPS-PNL-A",
    "PLC-RPS-A",
    "RELAY-K101",
    "RELAY-K102",
    "RELAY-K103",
    "RELAY-K104",
    "JB-RPS-A",
    "PNL-ANN-A",
    "CHG-125B",
    "REC-125B",
    "CB-DC-B",
    "BUS-125B",
    "BAT-125B",
    "GND-DC-B",
    "INV-120B",
    "UPS-120B",
    "BUS-120B",
    "RPS-PNL-B",
    "PLC-RPS-B",
    "RELAY-K201",
    "RELAY-K202",
    "RELAY-K203",
    "RELAY-K204",
    "JB-RPS-B",
    "PNL-ANN-B",
]


def branch_nodes(branches: list[tuple[str, str, str, str]]) -> list[str]:
    nodes: list[str] = []
    for cb, device_1, device_2, load in branches:
        nodes.extend([cb, device_1, device_2, load])
    return nodes


FINAL_NODES = (
    TOP_NODES
    + branch_nodes(BRANCHES_A)
    + branch_nodes(BRANCHES_B)
    + branch_nodes(BRANCHES_C)
    + branch_nodes(BRANCHES_D)
    + LOWER_NODES
)


DIEGO_R1_RENAMES = {
    "CB-GEN-ISO": "CB-GEN-150",
    "CB-480A-IN": "CB-480A-1N",
    "CB-480B-IN": "CB-480B-1N",
    "CB-480C-IN": "CB-480C-1N",
    "CB-480D-IN": "CB-480D-1N",
    "PNL-1C-C7": "PNL-IC-C7",
}
DIEGO_R1_NODES = [DIEGO_R1_RENAMES.get(node, node) for node in FINAL_NODES]


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


FINAL_EDGES: list[dict[str, str]] = [
    edge("GRID-SWYD-1", "CB-GRID-A", "solid_power", "grid source 1 feeder"),
    edge("CB-GRID-A", "BB-SWYD-230", "solid_power", "grid source 1 breaker to 230 kV bus"),
    edge("GRID-SWYD-2", "CB-GRID-B", "solid_power", "grid source 2 feeder"),
    edge("CB-GRID-B", "BB-SWYD-230", "solid_power", "grid source 2 breaker to 230 kV bus"),
    edge("BB-SWYD-230", "TR-SAT-1A", "solid_power", "station auxiliary transformer A tap"),
    edge("TR-SAT-1A", "CB-SAT-A", "solid_power", "SAT A low-side breaker"),
    edge("CB-SAT-A", "BUS-4160A", "solid_power", "SAT A breaker to 4160 A bus"),
    edge("BB-SWYD-230", "TR-SAT-1B", "solid_power", "station auxiliary transformer B tap"),
    edge("TR-SAT-1B", "CB-SAT-B", "solid_power", "SAT B low-side breaker"),
    edge("CB-SAT-B", "BUS-4160B", "solid_power", "SAT B breaker to 4160 B bus"),
    edge("BB-SWYD-230", "CB-GEN-ISO", "solid_power", "generator isolation breaker on 230 kV bus"),
    edge("CB-GEN-ISO", "GEN-MAIN-1", "solid_power", "isolation breaker to main generator"),
    edge("GEN-MAIN-1", "TR-UAT-1A", "solid_power", "main generator tap to UAT A"),
    edge("TR-UAT-1A", "CB-UAT-A", "solid_power", "UAT A to visible breaker"),
    edge("GEN-MAIN-1", "TR-UAT-1B", "solid_power", "main generator tap to UAT B"),
    edge("TR-UAT-1B", "CB-UAT-B", "solid_power", "UAT B to visible breaker"),
    edge("DG-1A", "CB-DG-A", "solid_power", "diesel generator A feeder"),
    edge("CB-DG-A", "BUS-4160A", "solid_power", "DG A breaker to 4160 A bus"),
    edge("DG-1B", "CB-DG-B", "solid_power", "diesel generator B feeder"),
    edge("CB-DG-B", "BUS-4160B", "solid_power", "DG B breaker to 4160 B bus"),
    edge("BUS-4160A", "CB-4160-TIE", "solid_power", "normally open 4160 tie from A side"),
    edge("CB-4160-TIE", "BUS-4160B", "solid_power", "normally open 4160 tie to B side"),
    edge("BUS-4160A", "GND-4160A", "ground", "4160 A bus ground tap"),
    edge("BUS-4160B", "GND-4160B", "ground", "4160 B bus ground tap"),
    edge("BUS-4160A", "TR-480-A1", "solid_power", "4160 A feeder to transformer A1"),
    edge("TR-480-A1", "CB-480A-IN", "solid_power", "transformer A1 to 480 A incomer"),
    edge("CB-480A-IN", "BUS-480A", "solid_power", "480 A incomer to bus"),
    edge("BUS-4160A", "TR-480-B1", "solid_power", "4160 A feeder to transformer B1"),
    edge("TR-480-B1", "CB-480B-IN", "solid_power", "transformer B1 to 480 B incomer"),
    edge("CB-480B-IN", "BUS-480B", "solid_power", "480 B incomer to bus"),
    edge("BUS-4160B", "TR-480-C1", "solid_power", "4160 B feeder to transformer C1"),
    edge("TR-480-C1", "CB-480C-IN", "solid_power", "transformer C1 to 480 C incomer"),
    edge("CB-480C-IN", "BUS-480C", "solid_power", "480 C incomer to bus"),
    edge("BUS-4160B", "TR-480-D1", "solid_power", "4160 B feeder to transformer D1"),
    edge("TR-480-D1", "CB-480D-IN", "solid_power", "transformer D1 to 480 D incomer"),
    edge("CB-480D-IN", "BUS-480D", "solid_power", "480 D incomer to bus"),
    edge("BUS-4160A", "PT-4160A", "dashed_instrument", "A bus PT tap"),
    edge("PT-4160A", "FU-PT-A", "dashed_instrument", "A PT fuse chain"),
    edge("FU-PT-A", "XFMR-CTRL-A", "dashed_control", "A control transformer chain"),
    edge("XFMR-CTRL-A", "TB-RPS-A", "dashed_control", "A RPS terminal chain"),
    edge("TB-RPS-A", "SW-43A", "dashed_control", "A selector switch chain"),
    edge("BUS-4160B", "PT-4160B", "dashed_instrument", "B bus PT tap"),
    edge("PT-4160B", "FU-PT-B", "dashed_instrument", "B PT fuse chain"),
    edge("FU-PT-B", "XFMR-CTRL-B", "dashed_control", "B control transformer chain"),
    edge("XFMR-CTRL-B", "TB-RPS-B", "dashed_control", "B RPS terminal chain"),
    edge("TB-RPS-B", "SW-43B", "dashed_control", "B selector switch chain"),
]


def add_branch_edges(
    bus: str, branches: list[tuple[str, str, str, str]], train: str
) -> None:
    for cb, device_1, device_2, load in branches:
        FINAL_EDGES.extend(
            [
                edge(bus, cb, "solid_power", f"{train} feeder {cb} from 480 V bus"),
                edge(cb, device_1, "solid_power", f"{train} feeder {cb} first device"),
                edge(device_1, device_2, "solid_power", f"{train} feeder {cb} second device"),
                edge(device_2, load, "solid_power/control", f"{train} feeder {cb} endpoint load"),
            ]
        )


add_branch_edges("BUS-480A", BRANCHES_A, "Load center A")
add_branch_edges("BUS-480B", BRANCHES_B, "Load center B")
add_branch_edges("BUS-480C", BRANCHES_C, "Load center C")
add_branch_edges("BUS-480D", BRANCHES_D, "Load center D")


FINAL_EDGES.extend(
    [
        edge("BUS-480B", "CHG-125A", "solid_power", "Train A control-power source from BUS-480B"),
        edge("CHG-125A", "REC-125A", "solid_power", "A charger/rectifier chain"),
        edge("REC-125A", "CB-DC-A", "solid_power", "A rectifier to DC breaker"),
        edge("CB-DC-A", "BUS-125A", "solid_power", "A DC breaker to 125 VDC bus"),
        edge("BUS-125A", "BAT-125A", "solid_power", "A battery tap with dot"),
        edge("BUS-125A", "GND-DC-A", "ground", "A DC ground tap with dot"),
        edge("BUS-125A", "INV-120A", "solid_power", "A DC bus to inverter"),
        edge("INV-120A", "UPS-120A", "dashed_control_power", "A inverter to UPS"),
        edge("UPS-120A", "BUS-120A", "solid_power", "A UPS to 120 VAC bus"),
        edge("BUS-120A", "RPS-PNL-A", "solid_power", "A 120 VAC bus to RPS panel"),
        edge("RPS-PNL-A", "PLC-RPS-A", "dashed_control", "A RPS panel to PLC"),
        edge("PLC-RPS-A", "RELAY-K101", "dashed_control", "A PLC relay bundle fanout"),
        edge("PLC-RPS-A", "RELAY-K102", "dashed_control", "A PLC relay bundle fanout"),
        edge("PLC-RPS-A", "RELAY-K103", "dashed_control", "A PLC relay bundle fanout"),
        edge("PLC-RPS-A", "RELAY-K104", "dashed_control", "A PLC relay bundle fanout"),
        edge("PLC-RPS-A", "JB-RPS-A", "dashed_control", "A PLC bundle to junction box"),
        edge("RELAY-K102", "PNL-ANN-A", "dashed_control", "A K102 annunciator drop"),
        edge("BUS-480C", "CHG-125B", "solid_power", "Train B control-power source from BUS-480C"),
        edge("CHG-125B", "REC-125B", "solid_power", "B charger/rectifier chain"),
        edge("REC-125B", "CB-DC-B", "solid_power", "B rectifier to DC breaker"),
        edge("CB-DC-B", "BUS-125B", "solid_power", "B DC breaker to 125 VDC bus"),
        edge("BUS-125B", "BAT-125B", "solid_power", "B battery tap with dot"),
        edge("BUS-125B", "GND-DC-B", "ground", "B DC ground tap with dot"),
        edge("BUS-125B", "INV-120B", "solid_power", "B DC bus to inverter"),
        edge("INV-120B", "UPS-120B", "dashed_control_power", "B inverter to UPS"),
        edge("UPS-120B", "BUS-120B", "solid_power", "B UPS to 120 VAC bus"),
        edge("BUS-120B", "RPS-PNL-B", "solid_power", "B 120 VAC bus to RPS panel"),
        edge("RPS-PNL-B", "PLC-RPS-B", "dashed_control", "B RPS panel to PLC"),
        edge("PLC-RPS-B", "RELAY-K201", "dashed_control", "B PLC relay bundle fanout"),
        edge("PLC-RPS-B", "RELAY-K202", "dashed_control", "B PLC relay bundle fanout"),
        edge("PLC-RPS-B", "RELAY-K203", "dashed_control", "B PLC relay bundle fanout"),
        edge("PLC-RPS-B", "RELAY-K204", "dashed_control", "B PLC relay bundle fanout"),
        edge("PLC-RPS-B", "JB-RPS-B", "dashed_control", "B PLC bundle to junction box"),
        edge("RELAY-K202", "PNL-ANN-B", "dashed_control", "B K202 annunciator drop"),
    ]
)


def renamed_edges(edges: list[dict[str, str]], renames: dict[str, str]) -> list[dict[str, str]]:
    output = []
    for item in edges:
        copied = item.copy()
        copied["source"] = renames.get(copied["source"], copied["source"])
        copied["target"] = renames.get(copied["target"], copied["target"])
        output.append(copied)
    return output


DIEGO_R1_EDGES = renamed_edges(FINAL_EDGES, DIEGO_R1_RENAMES)


UNCERTAIN_EXCLUDED = [
    {
        "source": "BUS-4160A",
        "target": "BUS-4160B",
        "reason": "No direct edge modeled; visible connection passes through CB-4160-TIE marked normally open.",
    },
    {
        "source": "CB-UAT-A",
        "target": "BUS-4160A",
        "reason": "UAT A breaker lower terminal stops without a visible connection to the 4160 A bus.",
    },
    {
        "source": "CB-UAT-B",
        "target": "BUS-4160B",
        "reason": "UAT B breaker lower terminal stops without a visible connection to the 4160 B bus.",
    },
    {
        "source": "RELAY-K101",
        "target": "RELAY-K102",
        "reason": "Relay bundle internals are not modeled as relay-to-relay edges without direct component-to-component evidence.",
    },
    {
        "source": "RELAY-K103",
        "target": "RELAY-K104",
        "reason": "Relay bundle internals are not modeled as relay-to-relay edges without direct component-to-component evidence.",
    },
    {
        "source": "RELAY-K201",
        "target": "RELAY-K202",
        "reason": "Relay bundle internals are not modeled as relay-to-relay edges without direct component-to-component evidence.",
    },
    {
        "source": "RELAY-K203",
        "target": "RELAY-K204",
        "reason": "Relay bundle internals are not modeled as relay-to-relay edges without direct component-to-component evidence.",
    },
    {
        "source": "crossing-without-dot",
        "target": "any crossing line",
        "reason": "Legend says crossing without dot is not a connection.",
    },
]


def ensure_unique(nodes: list[str]) -> None:
    seen = set()
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
            "case": "18",
            "round": "local",
            "agent": "main",
            "role": "inventory/crops/local inspection",
            "approx_prompt_tokens": "1600",
            "approx_completion_tokens": "260",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "codes/crops",
            "notes": "Approximate tokens; exact tool token accounting unavailable",
        },
        {
            "timestamp": timestamp,
            "case": "18",
            "round": "round_01",
            "agent": "Diego",
            "role": "high-recall extraction",
            "approx_prompt_tokens": "4300",
            "approx_completion_tokens": "3300",
            "matrix_nodes": len(DIEGO_R1_NODES),
            "matrix_edges": len(DIEGO_R1_EDGES),
            "output_artifact": "round_01_diego_matrix.csv",
            "notes": "Broad extraction before precision label fixes",
        },
        {
            "timestamp": timestamp,
            "case": "18",
            "round": "round_02",
            "agent": "Jennifer",
            "role": "precision review",
            "approx_prompt_tokens": "5200",
            "approx_completion_tokens": "1700",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_02_jennifer_matrix.csv",
            "notes": "Corrected CB-GEN-ISO, CB-480*-IN, and PNL-1C-C7; rejected unsupported relay-to-relay edges",
        },
        {
            "timestamp": timestamp,
            "case": "18",
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
            "case": "18",
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
            "case": "18",
            "round": "local",
            "agent": "main",
            "role": "artifact generation/validation",
            "approx_prompt_tokens": "1300",
            "approx_completion_tokens": "220",
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
        f"""# Case 18 Connectivity Extraction Note

Generated: {timestamp}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_nuclear_electrical_schematic_readable.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the source, 4160 V, 480 V load-center, and lower control-power topology.
2. Jennifer precision review corrected `CB-GEN-ISO`, `CB-480*-IN`, and `PNL-1C-C7`; she kept B/D at seven load branches and removed unsupported relay-to-relay/direct bus/UAT-bus edges.
3. Diego saturation check accepted the precision corrections and added no supported nodes or edges.
4. Jennifer final confirmation used the same saturated matrix.

## Final Counts

- Nodes: {len(FINAL_NODES)}
- Undirected edges in matrix: {len(FINAL_EDGES)}
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings without junction dots were not modeled as edges.
- The 4160 A/B connection is represented through `CB-4160-TIE`, not as a direct bus-to-bus edge.
- `CB-UAT-A` and `CB-UAT-B` remain as visible endpoints in the UAT chains, but no 4160 bus connection was accepted.
- The PLC/relay dashed groups are represented as component-level PLC fanout associations plus the visible K102/K202 annunciator drops.
- Train A control power is sourced from `BUS-480B`; Train B control power is sourced from `BUS-480C`.

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
