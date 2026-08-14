from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


TOP_AND_BUS_NODES = [
    "GRID-161KV",
    "TR-SST-1A",
    "CB-401A",
    "CB-401B",
    "BUS-4KV-A",
    "BUS-4KV-B",
    "CB-TIE-4AB",
    "GEN-EDG-A",
    "CB-EDG-A",
    "GEN-EDG-B",
    "CB-EDG-B",
    "TR-4KV-480A",
    "TR-4KV-480B",
    "CB-480A-IN",
    "CB-480B-IN",
    "BUS-480-A",
    "BUS-480-B",
    "CB-TIE-480AB",
    "CB-11A-FDR",
    "MCC-11A",
    "CB-12A-FDR",
    "MCC-12A",
    "CB-21A-FDR",
    "MCC-21A",
    "CB-31A-FDR30-B",
    "MCC-31A",
    "CB-11B-FDR",
    "MCC-11B",
    "CB-12B-FDR",
    "MCC-12B",
    "CB-21B-FDR",
    "MCC-21B",
    "CB-31B-FDR",
    "MCC-31B",
]


BRANCH_GROUPS = [
    ("MCC-11A", [("P201A", "PUMP-RHR201A", "GND-P201A"), ("P211A", "PUMP-CS211A", "GND-P211A"), ("P221A", "PUMP-SI221A", "GND-P221A")]),
    ("MCC-12A", [("P101A", "PUMP-AFW101A", "GND-P101A"), ("HV101A", "MOV-HV101A", "TB-HV101A"), ("FN1A", "FAN-FN1A", "GND-FN1A")]),
    ("MCC-21A", [("P301A", "PUMP-CCW301A", "GND-P301A"), ("P401A", "PUMP-SW401A", "GND-P401A"), ("HT1A", "HTR-PZR1A", "TB-HT1A")]),
    ("MCC-31A", [("RM1A", "MON-RAD1A", "TB-RM1A"), ("P501A", "PUMP-CHM501A", "GND-P501A"), ("CV121A", "MOV-CV121A", "TB-CV121A")]),
    ("MCC-11B", [("P201B", "PUMP-RHR201B", "GND-P201B"), ("P211B", "PUMP-CS211B", "GND-P211B"), ("P221B", "PUMP-SI221B", "GND-P221B")]),
    ("MCC-12B", [("P101B", "PUMP-AFW101B", "GND-P101B"), ("HV101B", "MOV-HV101B", "TB-HV101B"), ("FN1B", "FAN-FN1B", "GND-FN1B")]),
    ("MCC-21B", [("P301B", "PUMP-CCW301B", "GND-P301B"), ("P401B", "PUMP-SW401B", "GND-P401B"), ("HT1B", "HTR-PZR1B", "TB-HT1B")]),
    ("MCC-31B", [("RM1B", "MON-RAD1B", "TB-RM1B"), ("P501B", "PUMP-CHM501B", "GND-P501B"), ("CV121B", "MOV-CV121B", "TB-CV121B")]),
]


def branch_nodes() -> list[str]:
    nodes: list[str] = []
    for _mcc, branches in BRANCH_GROUPS:
        for device, load, terminal in branches:
            nodes.extend([f"CB-{device}", f"RELAY-K{device}", load, terminal])
    return nodes


LOWER_A_NODES = [
    "CP-RPS-A",
    "JB-RPS-AB-1A",
    "PROT-UV-A",
    "RELAY-27A",
    "CP-ESF-A",
    "TB-2A",
    "PROT-GF-A",
    "RELAY-86A",
    "CP-DCS-01",
    "TB-3A",
    "TB-ESF-1",
    "PT-RCS101",
    "LT-RWST101",
    "FT-AFW101",
    "REC-SOE-1",
    "ANN-501",
    "METER-VM-1",
    "TR-RPS-A",
    "MG-RPS-A",
    "BUS-125DC-A",
    "BATT-125A",
    "CHGR-125A",
    "INV-120A",
    "BUS-120-RPS-A",
]


LOWER_B_NODES = [
    "CP-RPS-B",
    "JB-RPS-B3-1B",
    "PROT-UV-B",
    "RELAY-27B",
    "CP-ESF-B",
    "TB-2B",
    "PROT-GF-B",
    "RELAY-86B",
    "CP-ANN-01",
    "TB-3B",
    "TR-RPS-B",
    "MG-RPS-B",
    "TB-ESF-2",
    "LS-SUMP101",
    "XS-DOOR101",
    "JB-CONTAIN",
    "BUS-125DC-B",
    "BATT-125B",
    "CHGR-125B",
    "INV-120B",
    "BUS-120-RPS-B",
    "UCP-01",
    "GND-NO",
]


FINAL_NODES = TOP_AND_BUS_NODES + branch_nodes() + LOWER_A_NODES + LOWER_B_NODES
DIEGO_R1_NODES = FINAL_NODES[: FINAL_NODES.index("LS-SUMP101")] + ["RTD-RCS101"] + FINAL_NODES[FINAL_NODES.index("LS-SUMP101") :]


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


FINAL_EDGES: list[dict[str, str]] = [
    edge("GRID-161KV", "TR-SST-1A", "solid_power", "top-left 4160 V station feed"),
    edge("TR-SST-1A", "CB-401A", "solid_power", "top-left station transformer A feeder"),
    edge("CB-401A", "BUS-4KV-A", "solid_power", "top 4 kV A bus"),
    edge("TR-SST-1A", "CB-401B", "solid_power", "top-left station transformer B feeder"),
    edge("CB-401B", "BUS-4KV-B", "solid_power", "top 4 kV B bus"),
    edge("BUS-4KV-A", "CB-TIE-4AB", "solid_power", "4 kV A/B tie"),
    edge("CB-TIE-4AB", "BUS-4KV-B", "solid_power", "4 kV A/B tie"),
    edge("GEN-EDG-A", "CB-EDG-A", "solid_power", "EDG A feeder"),
    edge("CB-EDG-A", "BUS-4KV-A", "solid_power", "EDG A feeder to A bus"),
    edge("GEN-EDG-B", "CB-EDG-B", "solid_power", "EDG B feeder"),
    edge("CB-EDG-B", "BUS-4KV-B", "solid_power", "EDG B feeder to B bus"),
    edge("BUS-4KV-A", "TR-4KV-480A", "solid_power", "A stepdown transformer"),
    edge("TR-4KV-480A", "CB-480A-IN", "solid_power", "A 480 V incomer"),
    edge("CB-480A-IN", "BUS-480-A", "solid_power", "A 480 V bus"),
    edge("BUS-4KV-B", "TR-4KV-480B", "solid_power", "B stepdown transformer"),
    edge("TR-4KV-480B", "CB-480B-IN", "solid_power", "B 480 V incomer"),
    edge("CB-480B-IN", "BUS-480-B", "solid_power", "B 480 V bus; crosses A header without dot"),
    edge("BUS-480-A", "CB-TIE-480AB", "solid_power", "480 V A/B tie"),
    edge("CB-TIE-480AB", "BUS-480-B", "solid_power", "480 V A/B tie"),
    edge("BUS-480-A", "CB-11A-FDR", "solid_power", "480 V A feeder"),
    edge("CB-11A-FDR", "MCC-11A", "solid_power", "MCC 11A feeder"),
    edge("BUS-480-A", "CB-12A-FDR", "solid_power", "480 V A feeder"),
    edge("CB-12A-FDR", "MCC-12A", "solid_power", "MCC 12A feeder"),
    edge("BUS-480-A", "CB-21A-FDR", "solid_power", "480 V A feeder"),
    edge("CB-21A-FDR", "MCC-21A", "solid_power", "MCC 21A feeder"),
    edge("BUS-480-B", "CB-31A-FDR30-B", "solid_power", "lower 480 V B header feeder to MCC 31A"),
    edge("CB-31A-FDR30-B", "MCC-31A", "solid_power", "MCC 31A feeder"),
    edge("BUS-480-B", "CB-11B-FDR", "solid_power", "480 V B feeder"),
    edge("CB-11B-FDR", "MCC-11B", "solid_power", "MCC 11B feeder"),
    edge("BUS-480-B", "CB-12B-FDR", "solid_power", "480 V B feeder"),
    edge("CB-12B-FDR", "MCC-12B", "solid_power", "MCC 12B feeder"),
    edge("BUS-480-B", "CB-21B-FDR", "solid_power", "480 V B feeder"),
    edge("CB-21B-FDR", "MCC-21B", "solid_power", "MCC 21B feeder"),
    edge("BUS-480-B", "CB-31B-FDR", "solid_power", "480 V B feeder"),
    edge("CB-31B-FDR", "MCC-31B", "solid_power", "MCC 31B feeder"),
]


for mcc, branches in BRANCH_GROUPS:
    for device, load, terminal in branches:
        cb = f"CB-{device}"
        relay = f"RELAY-K{device}"
        FINAL_EDGES.extend(
            [
                edge(mcc, cb, "solid_power", f"{mcc} branch {device}"),
                edge(cb, relay, "solid_power/control", f"{mcc} branch {device} relay path"),
                edge(relay, load, "solid_power", f"{mcc} branch {device} load path"),
                edge(load, terminal, "ground_or_terminal", f"{mcc} branch {device} terminal/ground endpoint"),
            ]
        )


FINAL_EDGES.extend(
    [
        edge("BUS-480-A", "TR-RPS-A", "solid_power", "A RPS transformer feed"),
        edge("TR-RPS-A", "MG-RPS-A", "solid_power", "A RPS motor-generator feed"),
        edge("MG-RPS-A", "BUS-120-RPS-A", "solid_power", "A 120 VAC vital bus"),
        edge("BUS-480-B", "TR-RPS-B", "solid_power", "B RPS transformer feed"),
        edge("TR-RPS-B", "MG-RPS-B", "solid_power", "B RPS motor-generator feed"),
        edge("MG-RPS-B", "BUS-120-RPS-B", "solid_power", "B 120 VAC vital bus"),
        edge("BATT-125A", "CHGR-125A", "dashed_dc_power", "A battery to charger"),
        edge("CHGR-125A", "BUS-125DC-A", "solid/dc_power", "A charger to 125 VDC bus"),
        edge("BUS-125DC-A", "INV-120A", "solid_power", "A DC bus to inverter"),
        edge("INV-120A", "BUS-120-RPS-A", "solid_power", "A inverter to 120 VAC bus"),
        edge("BATT-125B", "CHGR-125B", "dashed_dc_power", "B battery to charger"),
        edge("CHGR-125B", "BUS-125DC-B", "solid/dc_power", "B charger to 125 VDC bus"),
        edge("BUS-125DC-B", "INV-120B", "solid_power", "B DC bus to inverter"),
        edge("INV-120B", "BUS-120-RPS-B", "solid_power", "B inverter to 120 VAC bus"),
        edge("CP-RPS-A", "JB-RPS-AB-1A", "dashed_control", "A RPS control panel to junction box"),
        edge("JB-RPS-AB-1A", "PROT-UV-A", "dashed_control", "A UV protection path"),
        edge("PROT-UV-A", "RELAY-27A", "dashed_control", "A UV protection relay"),
        edge("CP-ESF-A", "TB-2A", "dashed_control", "A ESF control panel to terminal block"),
        edge("TB-2A", "PROT-GF-A", "dashed_control", "A GF protection path"),
        edge("PROT-GF-A", "RELAY-86A", "dashed_control", "A GF lockout relay"),
        edge("CP-DCS-01", "TB-3A", "dashed_control", "DCS panel to A terminal block"),
        edge("CP-DCS-01", "PT-RCS101", "dotted_signal", "DCS to pressure transmitter"),
        edge("PT-RCS101", "REC-SOE-1", "dotted_signal", "pressure transmitter to recorder"),
        edge("CP-DCS-01", "TB-ESF-1", "dotted_signal", "DCS to ESF terminal block 1"),
        edge("TB-ESF-1", "LT-RWST101", "dotted_signal", "level signal path"),
        edge("LT-RWST101", "ANN-501", "dotted_signal", "level transmitter to annunciator"),
        edge("TB-ESF-1", "FT-AFW101", "dotted_signal", "flow signal path"),
        edge("FT-AFW101", "METER-VM-1", "dotted_signal", "flow transmitter to meter"),
        edge("CP-RPS-B", "JB-RPS-B3-1B", "dashed_control", "B RPS control panel to junction box"),
        edge("JB-RPS-B3-1B", "PROT-UV-B", "dashed_control", "B UV protection path"),
        edge("PROT-UV-B", "RELAY-27B", "dashed_control", "B UV protection relay"),
        edge("CP-ESF-B", "TB-2B", "dashed_control", "B ESF control panel to terminal block"),
        edge("TB-2B", "PROT-GF-B", "dashed_control", "B GF protection path"),
        edge("PROT-GF-B", "RELAY-86B", "dashed_control", "B GF lockout relay"),
        edge("CP-ANN-01", "TB-3B", "dashed_control", "annunciator panel to B terminal block"),
        edge("MG-RPS-B", "TB-ESF-2", "dotted_signal", "B-side MG/ESF signal path accepted by reviewer"),
        edge("TB-ESF-2", "LS-SUMP101", "dotted_signal", "sump level switch"),
        edge("TB-ESF-2", "XS-DOOR101", "dotted_signal", "door switch"),
        edge("TB-ESF-2", "JB-CONTAIN", "dotted_signal", "containment junction box"),
        edge("BUS-120-RPS-A", "UCP-01", "dashed_control", "A 120 VAC bus to shared UCP"),
        edge("BUS-120-RPS-B", "UCP-01", "dashed_control", "B 120 VAC bus to shared UCP"),
        edge("UCP-01", "GND-NO", "ground", "UCP ground"),
    ]
)


DIEGO_R1_EDGES = [
    e
    for e in FINAL_EDGES
    if tuple(sorted((e["source"], e["target"])))
    != tuple(sorted(("BUS-480-B", "CB-31A-FDR30-B")))
]
DIEGO_R1_EDGES.extend(
    [
        edge("BUS-480-A", "CB-31A-FDR30-B", "solid_power", "Diego R1 high-recall placement, later corrected to BUS-480-B"),
        edge("BUS-125DC-A", "BATT-125A", "solid/dc_power", "Diego R1 direct battery-bus edge, later removed"),
        edge("BUS-125DC-B", "BATT-125B", "solid/dc_power", "Diego R1 direct battery-bus edge, later removed"),
        edge("RELAY-86A", "TB-3A", "dashed_control", "Diego R1 plausible lower control route, later removed"),
        edge("RELAY-86B", "TB-3B", "dashed_control", "Diego R1 plausible lower control route, later removed"),
        edge("MG-RPS-B", "RTD-RCS101", "dotted_signal", "Diego R1 plausible signal tap, later excluded"),
    ]
)


ROUND_DEFINITIONS = [
    ("round_01_diego", "Diego high-recall extraction", DIEGO_R1_NODES, DIEGO_R1_EDGES),
    ("round_02_jennifer", "Jennifer precision review", FINAL_NODES, FINAL_EDGES),
    ("round_03_diego_saturation", "Diego saturation check", FINAL_NODES, FINAL_EDGES),
    ("round_04_jennifer_final", "Jennifer final confirmation", FINAL_NODES, FINAL_EDGES),
]


UNCERTAIN_EXCLUDED = [
    ("MG-RPS-B", "RTD-RCS101", "Visible signal tap is not a clean accepted component-to-component edge; RTD node removed from final matrix"),
    ("BUS-125DC-A", "BATT-125A", "Battery visibly connects to charger, not directly to 125 VDC bus"),
    ("BUS-125DC-B", "BATT-125B", "Battery visibly connects to charger, not directly to 125 VDC bus"),
    ("RELAY-86A", "TB-3A", "Dashed route crosses/approaches TB-3A area without clear filled-dot termination"),
    ("RELAY-86B", "TB-3B", "Dashed route crosses/approaches TB-3B area without clear filled-dot termination"),
    ("CB-480B-IN", "BUS-480-A", "B incomer crosses upper A header without filled dot and lands on BUS-480-B"),
    ("BUS-480-A", "CB-31A-FDR30-B", "Feeder is connected to lower BUS-480-B header, not upper BUS-480-A"),
    ("long dashed MCC/control routes", "lower control panels", "Excluded unless both endpoints are named devices with filled dots"),
    ("BUS-125DC-A/B", "CP-RPS/CP-ESF/CP-DCS/CP-ANN", "Panel power/control feeds are not reliable component edges from crops alone"),
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
        raise ValueError(f"Unknown nodes referenced by edges: {missing}")
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
        [timestamp, "16", "local", "main", "inventory/crops/local inspection", 1400, 240, len(FINAL_NODES), len(FINAL_EDGES), "codes/crops", "Approximate tokens; exact tool token accounting unavailable"],
        [timestamp, "16", "round_01", "Diego", "high-recall extraction", 4300, 3200, len(DIEGO_R1_NODES), len(DIEGO_R1_EDGES), "round_01_diego_matrix.csv", "Broad proposal with later-pruned edges"],
        [timestamp, "16", "round_02", "Jennifer", "precision review", 5200, 1900, len(FINAL_NODES), len(FINAL_EDGES), "round_02_jennifer_matrix.csv", "Corrected BUS-480-B, removed unsupported lower edges"],
        [timestamp, "16", "round_03", "Diego", "saturation check", 900, 220, len(FINAL_NODES), len(FINAL_EDGES), "round_03_diego_saturation_matrix.csv", "Agreed with Jennifer corrections"],
        [timestamp, "16", "round_04", "Jennifer", "final confirmation", 420, 160, len(FINAL_NODES), len(FINAL_EDGES), "round_04_jennifer_final_matrix.csv", "Removed RTD-RCS101 from final node list"],
        [timestamp, "16", "local", "main", "artifact generation/validation", 1200, 200, len(FINAL_NODES), len(FINAL_EDGES), "final_connectivity_matrix.csv", "Symmetric matrix, zero diagonal"],
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
    note = f"""# Case 16 Connectivity Extraction Note

Generated: {now}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_revised(1).png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the full two-train topology and flagged bus/label/control uncertainties.
2. Jennifer precision review corrected `BUS-480-B`, `CB-31A-FDR30-B`, `JB-RPS-AB-1A`, `GND-NO`, removed unsupported battery-bus and RELAY-86/TB-3 edges, and excluded weak long dashed routes.
3. Diego saturation check agreed with Jennifer's corrections and added no edges.
4. Jennifer final confirmation removed `RTD-RCS101` from the accepted final node list because its only visible connection remained uncertain.

## Final Counts

- Nodes: {len(FINAL_NODES)}
- Undirected edges in matrix: {len(FINAL_EDGES)}
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- `BUS-480-B` is kept as the lower 480 V header. `CB-480B-IN` crosses the upper A header without a filled dot and lands on the lower B header.
- `CB-31A-FDR30-B` is connected to `BUS-480-B`, not `BUS-480-A`.
- Direct `BUS-125DC-* -- BATT-125*` edges were removed; the visible connection is `BATT-125* -- CHGR-125* -- BUS-125DC-*`.
- `RELAY-86A/B -- TB-3A/B` and `MG-RPS-B -- RTD-RCS101` remain excluded/uncertain.

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
