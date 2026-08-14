import csv
import json
import shutil
from pathlib import Path

from matrix_writer import RESULTS, write_all


FINAL_NODES = [
    "GRID-345A", "SWGR-52A", "RAT-1A", "MAIN-GEN-1", "GCB-1", "UAT-1A",
    "EDG-1A", "CB-EDG-A", "BUS-4KV-A", "CB-TIE-AB", "DS-TIE-AB",
    "BUS-4KV-B", "GRID-345B", "SWGR-52B", "RAT-1B", "EDG-1B", "CB-EDG-B",
    "CB-TIE-BC", "DS-TIE-BC", "BUS-4KV-C", "EDG-1C", "CB-EDG-C",
    "AAC-GEN-1", "CB-AAC-C", "CB-4A-01", "TR-480A", "CB-48A-01",
    "BUS-480-A", "CB-P201A", "MCC-01A", "RELAY-K201A", "PUMP-P201A",
    "CB-P202A", "MCC-02A", "RELAY-K202A", "PUMP-P202A", "CB-M301A",
    "MCC-03A", "RELAY-K301A", "MOTOR-FAN301A", "CB-V410A", "MCC-04A",
    "SOL-V410A", "VALVE-V410A", "CHG-125A", "BAT-125A", "BUS-125DC-A",
    "INV-120A", "BUS-120AC-A", "PNL-RPS-A", "RELAY-UV-A", "INSTR-PT-A",
    "CB-4B-01", "TR-480B", "CB-48B-01", "BUS-480-B", "CB-P201B",
    "MCC-01B", "RELAY-K201B", "PUMP-P201B", "CB-P202B", "MCC-02B",
    "RELAY-K202B", "PUMP-P202B", "CB-M301B", "MCC-03B", "RELAY-K301B",
    "MOTOR-FAN301B", "CB-V410B", "MCC-04B", "SOL-V410B", "VALVE-V410B",
    "CHG-125B", "BAT-125B", "BUS-125DC-B", "INV-120B", "BUS-120AC-B",
    "PNL-RPS-B", "RELAY-UV-B", "INSTR-PT-B", "N.O. DC TIE", "CB-4C-01",
    "TR-480C", "CB-48C-01", "BUS-480-C", "CB-P501", "MCC-05C",
    "RELAY-K501", "PUMP-CCW501", "CB-M601", "MCC-06C", "RELAY-K601",
    "MOTOR-HVAC601", "CB-V502", "MCC-07C", "SOL-V502", "VALVE-V502",
    "CB-P503", "MCC-08C", "RELAY-K503", "PUMP-SW503",
]


FINAL_EDGES = [
    ["AAC-GEN-1", "CB-AAC-C", "solid vertical generator feeder"],
    ["BAT-125A", "BUS-125DC-A", "solid vertical DC feeder to bus tap"],
    ["BAT-125A", "CHG-125A", "solid charger/battery feeder"],
    ["BAT-125B", "BUS-125DC-B", "solid vertical DC feeder to bus tap"],
    ["BAT-125B", "CHG-125B", "solid charger/battery feeder"],
    ["BUS-120AC-A", "INV-120A", "solid inverter output to 120 VAC bus"],
    ["BUS-120AC-A", "PNL-RPS-A", "solid panel tap from 120 VAC bus"],
    ["BUS-120AC-B", "INV-120B", "solid inverter output to 120 VAC bus"],
    ["BUS-120AC-B", "PNL-RPS-B", "solid panel tap from 120 VAC bus"],
    ["BUS-125DC-A", "INV-120A", "solid DC bus feeder to inverter"],
    ["BUS-125DC-A", "N.O. DC TIE", "visible normally-open DC tie, visual only"],
    ["BUS-125DC-B", "INV-120B", "solid DC bus feeder to inverter"],
    ["BUS-125DC-B", "N.O. DC TIE", "visible normally-open DC tie, visual only"],
    ["BUS-480-A", "CB-48A-01", "solid transformer low-side feeder to 480 V bus"],
    ["BUS-480-A", "CB-M301A", "solid 3/C feeder tap"],
    ["BUS-480-A", "CB-P201A", "solid 3/C feeder tap"],
    ["BUS-480-A", "CB-P202A", "solid 3/C feeder tap"],
    ["BUS-480-A", "CB-V410A", "solid 3/C feeder tap"],
    ["BUS-480-A", "CHG-125A", "solid charger feed drop"],
    ["BUS-480-B", "CB-48B-01", "solid transformer low-side feeder to 480 V bus"],
    ["BUS-480-B", "CB-M301B", "solid 3/C feeder tap"],
    ["BUS-480-B", "CB-P201B", "solid 3/C feeder tap"],
    ["BUS-480-B", "CB-P202B", "solid 3/C feeder tap"],
    ["BUS-480-B", "CB-V410B", "solid 3/C feeder tap"],
    ["BUS-480-B", "CHG-125B", "solid charger feed drop"],
    ["BUS-480-C", "CB-48C-01", "solid transformer low-side feeder to 480 V bus"],
    ["BUS-480-C", "CB-M601", "solid 3/C feeder tap"],
    ["BUS-480-C", "CB-P501", "solid 3/C feeder tap"],
    ["BUS-480-C", "CB-P503", "solid 3/C feeder tap"],
    ["BUS-480-C", "CB-V502", "solid 3/C feeder tap"],
    ["BUS-4KV-A", "CB-4A-01", "solid 4 kV transformer feeder"],
    ["BUS-4KV-A", "CB-EDG-A", "solid bus tap"],
    ["BUS-4KV-A", "CB-TIE-AB", "N.O. bus tie path, visual only"],
    ["BUS-4KV-A", "RAT-1A", "solid bus tap"],
    ["BUS-4KV-A", "UAT-1A", "solid bus tap"],
    ["BUS-4KV-B", "CB-4B-01", "solid 4 kV transformer feeder"],
    ["BUS-4KV-B", "CB-EDG-B", "solid bus tap"],
    ["BUS-4KV-B", "CB-TIE-BC", "N.O. bus tie path, visual only"],
    ["BUS-4KV-B", "DS-TIE-AB", "N.O. bus tie path, visual only"],
    ["BUS-4KV-B", "RAT-1B", "solid bus tap"],
    ["BUS-4KV-C", "CB-4C-01", "solid 4 kV transformer feeder"],
    ["BUS-4KV-C", "CB-AAC-C", "solid bus tap"],
    ["BUS-4KV-C", "CB-EDG-C", "solid bus tap"],
    ["BUS-4KV-C", "DS-TIE-BC", "N.O. bus tie path, visual only"],
    ["CB-48A-01", "TR-480A", "solid low-side transformer feeder"],
    ["CB-48B-01", "TR-480B", "solid low-side transformer feeder"],
    ["CB-48C-01", "TR-480C", "solid low-side transformer feeder"],
    ["CB-4A-01", "TR-480A", "solid high-side transformer feeder"],
    ["CB-4B-01", "TR-480B", "solid high-side transformer feeder"],
    ["CB-4C-01", "TR-480C", "solid high-side transformer feeder"],
    ["CB-EDG-A", "EDG-1A", "solid EDG feeder"],
    ["CB-EDG-B", "EDG-1B", "solid EDG feeder"],
    ["CB-EDG-C", "EDG-1C", "solid EDG feeder"],
    ["CB-M301A", "MCC-03A", "solid vertical feeder"],
    ["CB-M301B", "MCC-03B", "solid vertical feeder"],
    ["CB-M601", "MCC-06C", "solid vertical feeder"],
    ["CB-P201A", "MCC-01A", "solid vertical feeder"],
    ["CB-P201B", "MCC-01B", "solid vertical feeder"],
    ["CB-P202A", "MCC-02A", "solid vertical feeder"],
    ["CB-P202B", "MCC-02B", "solid vertical feeder"],
    ["CB-P501", "MCC-05C", "solid vertical feeder"],
    ["CB-P503", "MCC-08C", "solid vertical feeder"],
    ["CB-TIE-AB", "DS-TIE-AB", "N.O. bus tie devices in series, visual only"],
    ["CB-TIE-BC", "DS-TIE-BC", "N.O. bus tie devices in series, visual only"],
    ["CB-V410A", "MCC-04A", "solid vertical feeder"],
    ["CB-V410B", "MCC-04B", "solid vertical feeder"],
    ["CB-V502", "MCC-07C", "solid vertical feeder"],
    ["GCB-1", "MAIN-GEN-1", "solid generator feeder"],
    ["GCB-1", "UAT-1A", "solid vertical feeder"],
    ["GRID-345A", "SWGR-52A", "solid vertical feeder"],
    ["GRID-345B", "SWGR-52B", "solid vertical feeder"],
    ["INSTR-PT-A", "RELAY-UV-A", "dotted/dashed instrumentation link via untagged PT circle"],
    ["INSTR-PT-B", "RELAY-UV-B", "dotted/dashed instrumentation link via untagged PT circle"],
    ["MCC-01A", "RELAY-K201A", "solid vertical load/control path"],
    ["MCC-01B", "RELAY-K201B", "solid vertical load/control path"],
    ["MCC-02A", "RELAY-K202A", "solid vertical load/control path"],
    ["MCC-02B", "RELAY-K202B", "solid vertical load/control path"],
    ["MCC-03A", "RELAY-K301A", "solid vertical load/control path"],
    ["MCC-03B", "RELAY-K301B", "solid vertical load/control path"],
    ["MCC-04A", "SOL-V410A", "solid vertical valve-control path"],
    ["MCC-04B", "SOL-V410B", "solid vertical valve-control path"],
    ["MCC-05C", "RELAY-K501", "solid vertical load/control path"],
    ["MCC-06C", "RELAY-K601", "solid vertical load/control path"],
    ["MCC-07C", "SOL-V502", "solid vertical valve-control path"],
    ["MCC-08C", "RELAY-K503", "solid vertical load/control path"],
    ["MOTOR-FAN301A", "RELAY-K301A", "solid fan-start line"],
    ["MOTOR-FAN301B", "RELAY-K301B", "solid fan-start line"],
    ["MOTOR-HVAC601", "RELAY-K601", "solid fan-start line"],
    ["PNL-RPS-A", "RELAY-UV-A", "dashed control link"],
    ["PNL-RPS-B", "RELAY-UV-B", "dashed control link"],
    ["PUMP-CCW501", "RELAY-K501", "solid pump-start line"],
    ["PUMP-P201A", "RELAY-K201A", "solid pump-start line"],
    ["PUMP-P201B", "RELAY-K201B", "solid pump-start line"],
    ["PUMP-P202A", "RELAY-K202A", "solid pump-start line"],
    ["PUMP-P202B", "RELAY-K202B", "solid pump-start line"],
    ["PUMP-SW503", "RELAY-K503", "solid pump-start line"],
    ["RAT-1A", "SWGR-52A", "solid vertical feeder"],
    ["RAT-1B", "SWGR-52B", "solid vertical feeder"],
    ["SOL-V410A", "VALVE-V410A", "solid valve-control line"],
    ["SOL-V410B", "VALVE-V410B", "solid valve-control line"],
    ["SOL-V502", "VALVE-V502", "solid valve-control line"],
]


def diego_round_1_label(name):
    return (
        name.replace("CB-48A-01", "CB-480A-01")
        .replace("CB-48B-01", "CB-480B-01")
        .replace("CB-48C-01", "CB-480C-01")
    )


def diego_round_1_edges():
    edges = [
        [diego_round_1_label(a), diego_round_1_label(b), evidence]
        for a, b, evidence in FINAL_EDGES
    ]
    edges.extend(
        [
            [
                "BUS-4KV-A",
                "TO 4KV BUS A ELEMENTARY DIAGRAM SH-2",
                "solid bus continuation/external reference label",
            ],
            [
                "BUS-4KV-B",
                "TO 4KV BUS B ELEMENTARY DIAGRAM SH-3",
                "solid bus continuation/external reference label",
            ],
            [
                "BUS-4KV-C",
                "TO AAC BUS C ELEMENTARY DIAGRAM SH-4",
                "solid bus continuation/external reference label",
            ],
        ]
    )
    return edges


def write_closed_state_exclusions():
    rows = []
    for a, b, evidence in FINAL_EDGES:
        e = evidence.lower()
        if "n.o." in e or "dashed" in e or "dotted" in e:
            rows.append([a, b, evidence])
    path = RESULTS / "closed_state_excluded_visual_edges.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "visual_edge_evidence"])
        writer.writerows(rows)
    return path


def main():
    diego_1_nodes = [diego_round_1_label(node) for node in FINAL_NODES] + [
        "TO 4KV BUS A ELEMENTARY DIAGRAM SH-2",
        "TO 4KV BUS B ELEMENTARY DIAGRAM SH-3",
        "TO AAC BUS C ELEMENTARY DIAGRAM SH-4",
    ]

    rounds = [
        {
            "name": "round_01_diego_high_recall",
            "nodes": diego_1_nodes,
            "edges": diego_round_1_edges(),
            "notes": [
                "High-recall proposal before Jennifer correction.",
                "Contains off-sheet annotation nodes and CB-480x-01 labels as Diego originally proposed.",
            ],
        },
        {
            "name": "round_02_jennifer_precision",
            "nodes": FINAL_NODES,
            "edges": FINAL_EDGES,
            "notes": [
                "Jennifer corrected CB-480x-01 to CB-48x-01.",
                "Off-sheet TO ... DIAGRAM annotations removed as non-component annotations.",
            ],
        },
        {
            "name": "round_03_diego_saturation",
            "nodes": FINAL_NODES,
            "edges": FINAL_EDGES,
            "notes": [
                "Diego accepted Jennifer's refined graph with no changes.",
            ],
        },
        {
            "name": "round_04_jennifer_final_agreed",
            "nodes": FINAL_NODES,
            "edges": FINAL_EDGES,
            "notes": [
                "Jennifer final status: AGREED.",
                "Final matrix is visual schematic connectivity; normally-open ties are visual-only.",
            ],
        },
    ]

    summaries = write_all(rounds)
    shutil.copyfile(
        RESULTS / "round_04_jennifer_final_agreed_connectivity_matrix.csv",
        RESULTS / "final_connectivity_matrix.csv",
    )
    shutil.copyfile(
        RESULTS / "round_04_jennifer_final_agreed_edges.csv",
        RESULTS / "final_edges.csv",
    )
    write_closed_state_exclusions()

    final_graph = {
        "document": "1",
        "iteration": 1,
        "interpretation": "visual schematic connectivity",
        "node_count": len(FINAL_NODES),
        "edge_count": len(FINAL_EDGES),
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "precision_notes": [
            "Normally-open 4 kV bus ties and N.O. DC tie are retained as visual-only connectivity.",
            "Dashed RPS/PT control and instrumentation links are retained.",
            "Off-sheet continuation text, drawing notes, legend, title block, and zone boundaries are not matrix nodes.",
            "Untagged PT circles are folded into INSTR-PT-A and INSTR-PT-B.",
        ],
        "round_summaries": summaries,
    }
    (RESULTS / "final_graph.json").write_text(json.dumps(final_graph, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
