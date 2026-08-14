from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


TOP_NODES = [
    "SAT-1A",
    "CB-SAT-1A",
    "UAT-1A",
    "CB-UAT-1A",
    "DGS-1A",
    "CB-DG-1A",
    "BUS-4160-A",
    "PT-4160-A",
    "CB-TR-A1",
    "CB-TR-A2",
    "GEN-001 MAIN GEN",
    "CB-TIE-4AB",
    "BUS-4160-B",
    "PT-4160-B",
    "UAT-1B",
    "CB-UAT-1B",
    "DGS-1B",
    "CB-DG-1B",
    "SAT-1B",
    "CB-SAT-1B",
    "CB-TR-B1",
    "CB-TR-B2",
]


A_UPSTREAM = [
    "TR-LC-A1",
    "CB-480-A1",
    "TR-LC-A2",
    "CB-480-A2",
    "BUS-480-A",
    "AM-480-A",
    "VM-480-A",
    "CT-480-A1",
    "GND-SWGR-A",
]

B_UPSTREAM = [
    "TR-LC-B1",
    "CB-480-B1",
    "TR-LC-B2",
    "CB-480-B2",
    "BUS-480-B",
    "AM-480-B",
    "VM-480-B",
    "CT-480-B1",
    "GND-SWGR-B",
    "CB-TIE-480AB",
]


BRANCHES_A = [
    ("101A", "DS-101A", "MS-101A", "PUMP-SLC-1A", "TB-SLC-1A"),
    ("102A", "FU-102A", "MS-102A", "PUMP-CCW-1A", "GND-CCW-1A"),
    ("103A", "DS-103A", "MS-103A", "PUMP-RHR-1A", "LS-RHR-1A"),
    ("104A", "FU-104A", "MS-104A", "PUMP-CS-1A", "TB-CS-1A"),
    ("105A", "DS-105A", "MS-105A", "FAN-CRDM-1A", "GND-FAN-1A"),
    ("106A", "FU-106A", "RELAY-K106A", "HOV-RWCU-101A", "LS-RWCU-101A"),
    ("107A", "DS-107A", "RELAY-K107A", "HOV-RHR-102A", "LS-RHR-102A"),
    ("108A", "FU-108A", "MS-108A", "HTR-PZR-1A", "TB-HTR-1A"),
    ("109A", "DS-109A", "MS-109A", "PUMP-SW-1A", "GND-SW-1A"),
    ("110A", "FU-110A", "MS-110A", "HTR-AHU-1A", "GND-AHU-1A"),
    ("111A", "DS-111A", "MS-111A", "CMP-AIR-1A", "TB-AIR-1A"),
    ("112A", "FU-112A", "RELAY-K112A", "INST-RAD-1A", "JB-RAD-1A"),
]

BRANCHES_B = [
    ("201B", "DS-201B", "MS-201B", "PUMP-SLC-1B", "TB-SLC-1B"),
    ("202B", "FU-202B", "MS-202B", "PUMP-CCW-1B", "GND-CCW-1B"),
    ("203B", "DS-203B", "MS-203B", "PUMP-RHR-1B", "LS-RHR-1B"),
    ("204B", "FU-204B", "MS-204B", "PUMP-CS-1B", "TB-CS-1B"),
    ("205B", "DS-205B", "MS-205B", "FAN-CRDM-1B", "GND-FAN-1B"),
    ("206B", "FU-206B", "RELAY-K206B", "HOV-RWCU-101B", "LS-RWCU-101B"),
    ("207B", "DS-207B", "RELAY-K207B", "HOV-RHR-102B", "LS-RHR-102B"),
    ("208B", "FU-208B", "MS-208B", "HTR-PZR-1B", "TB-HTR-1B"),
    ("209B", "DS-209B", "MS-209B", "PUMP-SW-1B", "GND-SW-1B"),
    ("210B", "FU-210B", "MS-210B", "HTR-AHU-1B", "GND-AHU-1B"),
    ("211B", "DS-211B", "MS-211B", "CMP-AIR-1B", "TB-AIR-1B"),
    ("212B", "FU-212B", "RELAY-K212B", "INST-RAD-1B", "JB-RAD-1B"),
]


def branch_nodes(branches: list[tuple[str, str, str, str, str]]) -> list[str]:
    nodes: list[str] = []
    for suffix, protective, relay_or_starter, load, terminal in branches:
        nodes.extend([f"CB-{suffix}", protective, relay_or_starter, load, terminal])
    return nodes


LOWER_NODES = [
    "CB-DC-A",
    "CHGR-125-A",
    "BAT-125-A",
    "BUS-125DC-A",
    "GND-DC-A",
    "INV-120-A",
    "BUS-120AC-A",
    "STS-120-A",
    "TB-RPS-A",
    "PNL-RPS-A",
    "RELAY-UV-A1",
    "RELAY-UV-A2",
    "TB-ESF-A",
    "PNL-ESF-A",
    "RELAY-RPS-A",
    "RELAY-ESF-A",
    "CB-DCTIE-AB",
    "CB-DC-B",
    "CHGR-125-B",
    "BAT-125-B",
    "BUS-125DC-B",
    "GND-DC-B",
    "INV-120-B",
    "BUS-120AC-B",
    "STS-120-B",
    "TB-RPS-B",
    "PNL-RPS-B",
    "RELAY-UV-B1",
    "RELAY-UV-B2",
    "TB-ESF-B",
    "PNL-ESF-B",
    "RELAY-RPS-B",
    "RELAY-ESF-B",
    "PNL-DCS",
    "REC-SOE-1",
    "PNL-ANN",
    "ANN-ESF-A",
    "ANN-ESF-B",
]


FINAL_NODES = TOP_NODES + A_UPSTREAM + branch_nodes(BRANCHES_A) + B_UPSTREAM + branch_nodes(BRANCHES_B) + LOWER_NODES
DIEGO_R1_NODES = (
    TOP_NODES[:10]
    + ["MASTER TERMINAL BLOCKS 21-29"]
    + TOP_NODES[10:]
    + A_UPSTREAM
    + branch_nodes(BRANCHES_A)
    + B_UPSTREAM
    + branch_nodes(BRANCHES_B)
    + ["WIREWAY A CONTROL LANES 2380/2420"]
    + LOWER_NODES[:16]
    + ["WIREWAY B CONTROL LANES 2380/2420"]
    + LOWER_NODES[16:]
    + ["REC-SOE-2"]
)


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


FINAL_EDGES: list[dict[str, str]] = [
    edge("SAT-1A", "CB-SAT-1A", "solid_power", "top train A station auxiliary feeder"),
    edge("CB-SAT-1A", "BUS-4160-A", "solid_power", "top train A 4160 V bus"),
    edge("UAT-1A", "CB-UAT-1A", "solid_power", "top train A unit auxiliary feeder"),
    edge("CB-UAT-1A", "BUS-4160-A", "solid_power", "top train A 4160 V bus"),
    edge("DGS-1A", "CB-DG-1A", "solid_power", "top train A diesel feeder"),
    edge("CB-DG-1A", "BUS-4160-A", "solid_power", "top train A 4160 V bus"),
    edge("GEN-001 MAIN GEN", "UAT-1A", "solid_power", "main generator tap to UAT A"),
    edge("GEN-001 MAIN GEN", "UAT-1B", "solid_power", "main generator tap to UAT B"),
    edge("BUS-4160-A", "PT-4160-A", "dotted_instrument", "A 4160 V PT"),
    edge("BUS-4160-A", "CB-TR-A1", "solid_power", "A load center transformer feeder 1"),
    edge("CB-TR-A1", "TR-LC-A1", "solid_power", "A load center transformer 1"),
    edge("BUS-4160-A", "CB-TR-A2", "solid_power", "A load center transformer feeder 2"),
    edge("CB-TR-A2", "TR-LC-A2", "solid_power", "A load center transformer 2"),
    edge("BUS-4160-A", "CB-TIE-4AB", "solid_power", "normally open 4160 V tie"),
    edge("CB-TIE-4AB", "BUS-4160-B", "solid_power", "normally open 4160 V tie"),
    edge("SAT-1B", "CB-SAT-1B", "solid_power", "top train B station auxiliary feeder"),
    edge("CB-SAT-1B", "BUS-4160-B", "solid_power", "top train B 4160 V bus"),
    edge("UAT-1B", "CB-UAT-1B", "solid_power", "top train B unit auxiliary feeder"),
    edge("CB-UAT-1B", "BUS-4160-B", "solid_power", "top train B 4160 V bus"),
    edge("DGS-1B", "CB-DG-1B", "solid_power", "top train B diesel feeder"),
    edge("CB-DG-1B", "BUS-4160-B", "solid_power", "top train B 4160 V bus"),
    edge("BUS-4160-B", "PT-4160-B", "dotted_instrument", "B 4160 V PT"),
    edge("BUS-4160-B", "CB-TR-B1", "solid_power", "B load center transformer feeder 1"),
    edge("CB-TR-B1", "TR-LC-B1", "solid_power", "B load center transformer 1"),
    edge("BUS-4160-B", "CB-TR-B2", "solid_power", "B load center transformer feeder 2"),
    edge("CB-TR-B2", "TR-LC-B2", "solid_power", "B load center transformer 2"),
    edge("TR-LC-A1", "CB-480-A1", "solid_power", "480 V A incomer 1"),
    edge("CB-480-A1", "BUS-480-A", "solid_power", "480 V A bus"),
    edge("TR-LC-A2", "CB-480-A2", "solid_power", "480 V A incomer 2"),
    edge("CB-480-A2", "BUS-480-A", "solid_power", "480 V A bus"),
    edge("BUS-480-A", "AM-480-A", "dotted_instrument", "A bus ammeter"),
    edge("BUS-480-A", "VM-480-A", "dotted_instrument", "A bus voltmeter"),
    edge("BUS-480-A", "CT-480-A1", "dotted_instrument", "A bus CT"),
    edge("BUS-480-A", "GND-SWGR-A", "ground", "A switchgear ground"),
    edge("BUS-480-A", "CB-TIE-480AB", "solid_power", "normally open 480 V tie"),
    edge("CB-TIE-480AB", "BUS-480-B", "solid_power", "normally open 480 V tie"),
    edge("TR-LC-B1", "CB-480-B1", "solid_power", "480 V B incomer 1"),
    edge("CB-480-B1", "BUS-480-B", "solid_power", "480 V B bus"),
    edge("TR-LC-B2", "CB-480-B2", "solid_power", "480 V B incomer 2"),
    edge("CB-480-B2", "BUS-480-B", "solid_power", "480 V B bus"),
    edge("BUS-480-B", "AM-480-B", "dotted_instrument", "B bus ammeter"),
    edge("BUS-480-B", "VM-480-B", "dotted_instrument", "B bus voltmeter"),
    edge("BUS-480-B", "CT-480-B1", "dotted_instrument", "B bus CT"),
    edge("BUS-480-B", "GND-SWGR-B", "ground", "B switchgear ground"),
]


def add_branch_edges(bus: str, branches: list[tuple[str, str, str, str, str]], train: str) -> None:
    for suffix, protective, relay_or_starter, load, terminal in branches:
        cb = f"CB-{suffix}"
        FINAL_EDGES.extend(
            [
                edge(bus, cb, "solid_power", f"{train} 480 V feeder {suffix}"),
                edge(cb, protective, "solid_power", f"{train} feeder {suffix} protective device"),
                edge(protective, relay_or_starter, "solid_power/control", f"{train} feeder {suffix} starter/relay"),
                edge(relay_or_starter, load, "solid_power/control", f"{train} feeder {suffix} load"),
                edge(load, terminal, "ground_terminal_or_instrument", f"{train} feeder {suffix} endpoint"),
            ]
        )


add_branch_edges("BUS-480-A", BRANCHES_A, "Train A")
add_branch_edges("BUS-480-B", BRANCHES_B, "Train B")


FINAL_EDGES.extend(
    [
        edge("BUS-480-A", "CB-DC-A", "solid_power", "A lower DC feeder from 480 bus"),
        edge("CB-DC-A", "CHGR-125-A", "solid_power", "A charger feeder"),
        edge("CHGR-125-A", "BAT-125-A", "solid_power", "A charger to battery"),
        edge("BAT-125-A", "BUS-125DC-A", "solid_power", "A battery to 125 VDC bus"),
        edge("BUS-125DC-A", "GND-DC-A", "ground", "A DC bus ground"),
        edge("BUS-125DC-A", "INV-120-A", "solid_power", "A DC bus to inverter"),
        edge("INV-120-A", "BUS-120AC-A", "solid_power", "A inverter to AC bus"),
        edge("BUS-120AC-A", "STS-120-A", "solid_power/control", "A AC bus to static transfer switch"),
        edge("STS-120-A", "PNL-RPS-A", "dashed_control", "A STS to RPS panel"),
        edge("PNL-RPS-A", "TB-RPS-A", "dashed_control", "A RPS panel terminal block"),
        edge("PNL-RPS-A", "RELAY-UV-A1", "dashed_control", "A RPS undervoltage relay 1"),
        edge("PNL-RPS-A", "RELAY-UV-A2", "dashed_control", "A RPS undervoltage relay 2"),
        edge("PNL-ESF-A", "TB-ESF-A", "dashed_control", "A ESF panel terminal block"),
        edge("PNL-ESF-A", "RELAY-RPS-A", "dashed_control", "A ESF/RPS relay"),
        edge("PNL-ESF-A", "RELAY-ESF-A", "dashed_control", "A ESF relay"),
        edge("BUS-125DC-A", "CB-DCTIE-AB", "solid_power", "normally open DC tie"),
        edge("CB-DCTIE-AB", "BUS-125DC-B", "solid_power", "normally open DC tie"),
        edge("BUS-480-B", "CB-DC-B", "solid_power", "B lower DC feeder from 480 bus"),
        edge("CB-DC-B", "CHGR-125-B", "solid_power", "B charger feeder"),
        edge("CHGR-125-B", "BAT-125-B", "solid_power", "B charger to battery"),
        edge("BAT-125-B", "BUS-125DC-B", "solid_power", "B battery to 125 VDC bus"),
        edge("BUS-125DC-B", "GND-DC-B", "ground", "B DC bus ground"),
        edge("BUS-125DC-B", "INV-120-B", "solid_power", "B DC bus to inverter"),
        edge("INV-120-B", "BUS-120AC-B", "solid_power", "B inverter to AC bus"),
        edge("BUS-120AC-B", "STS-120-B", "solid_power/control", "B AC bus to static transfer switch"),
        edge("STS-120-B", "PNL-RPS-B", "dashed_control", "B STS to RPS panel"),
        edge("PNL-RPS-B", "TB-RPS-B", "dashed_control", "B RPS panel terminal block"),
        edge("PNL-RPS-B", "RELAY-UV-B1", "dashed_control", "B RPS undervoltage relay 1"),
        edge("PNL-RPS-B", "RELAY-UV-B2", "dashed_control", "B RPS undervoltage relay 2"),
        edge("PNL-ESF-B", "TB-ESF-B", "dashed_control", "B ESF panel terminal block"),
        edge("PNL-ESF-B", "RELAY-RPS-B", "dashed_control", "B ESF/RPS relay"),
        edge("PNL-ESF-B", "RELAY-ESF-B", "dashed_control", "B ESF relay"),
        edge("PNL-DCS", "REC-SOE-1", "dashed_control", "DCS panel to SOE recorder"),
        edge("PNL-ANN", "ANN-ESF-A", "dashed_control", "annunciator panel to A annunciator"),
        edge("PNL-ANN", "ANN-ESF-B", "dashed_control", "annunciator panel to B annunciator"),
    ]
)


DIEGO_R1_EDGES = FINAL_EDGES.copy()
DIEGO_R1_EDGES.extend(
    [
        edge("WIREWAY A CONTROL LANES 2380/2420", "CB-DC-A", "dashed_control", "Diego R1 routed wireway node, later removed"),
        edge("WIREWAY B CONTROL LANES 2380/2420", "CB-DC-B", "dashed_control", "Diego R1 routed wireway node, later removed"),
        edge("RELAY-ESF-A", "REC-SOE-1", "dotted_instrument", "Diego R1 plausible recorder tail, later removed"),
        edge("RELAY-ESF-B", "REC-SOE-2", "dotted_instrument", "Diego R1 plausible recorder tail, later removed"),
    ]
)


ROUND_DEFINITIONS = [
    ("round_01_diego", "Diego high-recall extraction", DIEGO_R1_NODES, DIEGO_R1_EDGES),
    ("round_02_jennifer", "Jennifer precision review", FINAL_NODES, FINAL_EDGES),
    ("round_03_diego_saturation", "Diego saturation check", FINAL_NODES, FINAL_EDGES),
    ("round_04_jennifer_final", "Jennifer final confirmation", FINAL_NODES, FINAL_EDGES),
]


UNCERTAIN_EXCLUDED = [
    ("MASTER TERMINAL BLOCKS 21-29", "control lanes", "Visible component but no accepted edge clearly terminates on it; removed from final matrix"),
    ("REC-SOE-2", "RELAY-ESF-B", "Visible component but no reliable terminated edge; removed from final matrix"),
    ("WIREWAY A CONTROL LANES 2380/2420", "CB-DC-A", "Wireway is a routing annotation, not equipment endpoint"),
    ("WIREWAY B CONTROL LANES 2380/2420", "CB-DC-B", "Wireway is a routing annotation, not equipment endpoint"),
    ("RELAY-ESF-A", "REC-SOE-1", "Dotted/tail route not clearly terminated at recorder"),
    ("RELAY-ESF-B", "REC-SOE-2", "Dotted/tail route not clearly terminated at recorder"),
    ("MS-103A/MS-104A/MS-203B/MS-204B", "long dashed tails", "Long routed tails lack named terminal endpoints in crops"),
    ("crossings/overlaps without black dots", "any node", "Notes specify crossings without dots are not electrically connected"),
]


def normalized_pairs(rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    return [tuple(sorted((row["source"], row["target"]))) for row in rows]


def validate(nodes: list[str], rows: list[dict[str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        raise ValueError("Duplicate node names detected")
    node_set = set(nodes)
    pairs = normalized_pairs(rows)
    if len(pairs) != len(set(pairs)):
        dupes = sorted({pair for pair in pairs if pairs.count(pair) > 1})
        raise ValueError(f"Duplicate undirected edges detected: {dupes}")
    missing = sorted({node for pair in pairs for node in pair if node not in node_set})
    if missing:
        raise ValueError(f"Edges reference missing nodes: {missing}")
    loops = [pair for pair in pairs if pair[0] == pair[1]]
    if loops:
        raise ValueError(f"Self loops detected: {loops}")


def write_matrix(path: Path, nodes: list[str], rows: list[dict[str, str]]) -> None:
    node_index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for src, dst in normalized_pairs(rows):
        i = node_index[src]
        j = node_index[dst]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, values in zip(nodes, matrix):
            writer.writerow([node] + values)


def write_edges(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        writer.writerows(rows)


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_token_tracking(path: Path) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = [
        [timestamp, "17", "local", "main", "inventory/crops/local inspection", 1500, 260, len(FINAL_NODES), len(FINAL_EDGES), "codes/crops", "Approximate tokens; exact tool token accounting unavailable"],
        [timestamp, "17", "round_01", "Diego", "high-recall extraction", 4700, 3300, len(DIEGO_R1_NODES), len(DIEGO_R1_EDGES), "round_01_diego_matrix.csv", "Broad extraction with wireway and recorder-tail candidates"],
        [timestamp, "17", "round_02", "Jennifer", "precision review", 5400, 1700, len(FINAL_NODES), len(FINAL_EDGES), "round_02_jennifer_matrix.csv", "Removed routing annotations and unsupported recorder tails"],
        [timestamp, "17", "round_03", "Diego", "saturation check", 900, 180, len(FINAL_NODES), len(FINAL_EDGES), "round_03_diego_saturation_matrix.csv", "Agreed with Jennifer corrections"],
        [timestamp, "17", "round_04", "Jennifer", "final confirmation", 380, 150, len(FINAL_NODES), len(FINAL_EDGES), "round_04_jennifer_final_matrix.csv", "Removed edge-free visible components from final node list"],
        [timestamp, "17", "local", "main", "artifact generation/validation", 1200, 200, len(FINAL_NODES), len(FINAL_EDGES), "final_connectivity_matrix.csv", "Symmetric matrix, zero diagonal"],
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "case",
                "round",
                "agent",
                "role",
                "approx_prompt_tokens",
                "approx_completion_tokens",
                "matrix_nodes",
                "matrix_edges",
                "output_artifact",
                "notes",
            ]
        )
        writer.writerows(rows)


def write_note(path: Path) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    note = f"""# Case 17 Connectivity Extraction Note

Generated: {now}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the two-train 4160 V/480 V/DC/UPS/control topology.
2. Jennifer precision review removed routing-only wireway nodes, unsupported recorder-tail edges, and long dashed branch tails.
3. Diego saturation check agreed with Jennifer and added no nodes or edges.
4. Jennifer final confirmation removed edge-free visible components `MASTER TERMINAL BLOCKS 21-29` and `REC-SOE-2` from the final matrix.

## Final Counts

- Nodes: {len(FINAL_NODES)}
- Undirected edges in matrix: {len(FINAL_EDGES)}
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings/overlaps without black-dot terminations were not modeled as edges.
- `WIREWAY A/B CONTROL LANES 2380/2420` were treated as routing annotations, not equipment nodes.
- `REC-SOE-2` and `MASTER TERMINAL BLOCKS 21-29` are visible but omitted from the final matrix because no accepted edge terminates on them.
- The accepted final set keeps the three A/B ties: `CB-TIE-4AB`, `CB-TIE-480AB`, and `CB-DCTIE-AB`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
"""
    path.write_text(note, encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for stem, _description, nodes, rows in ROUND_DEFINITIONS:
        validate(nodes, rows)
        write_matrix(RESULTS_DIR / f"{stem}_matrix.csv", nodes, rows)
        write_edges(RESULTS_DIR / f"{stem}_edges.csv", rows)
    validate(FINAL_NODES, FINAL_EDGES)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_edges(RESULTS_DIR / "final_edge_list.csv", FINAL_EDGES)
    write_uncertain(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_token_tracking(RESULTS_DIR / "token_performance_tracking.csv")
    write_note(RESULTS_DIR / "extraction_note.md")
    print(f"final_nodes={len(FINAL_NODES)}")
    print(f"final_edges={len(FINAL_EDGES)}")
    print(f"rounds={len(ROUND_DEFINITIONS)}")
    print(f"results={RESULTS_DIR}")


if __name__ == "__main__":
    main()
