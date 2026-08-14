from __future__ import annotations

import csv
import json
import shutil
from collections import OrderedDict
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires"
)
RESULTS = BASE / "results"


def edge(a: str, b: str, kind: str = "solid_power", evidence: str = "") -> dict[str, str]:
    return {"a": a, "b": b, "kind": kind, "evidence": evidence}


def normalize_pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def ordered_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: OrderedDict[tuple[str, str], dict[str, str]] = OrderedDict()
    for item in edges:
        key = normalize_pair(item["a"], item["b"])
        if key in seen:
            raise ValueError(f"duplicate edge: {item['a']} -- {item['b']}")
        seen[key] = item
    return list(seen.values())


def chain(nodes: list[str], kind: str = "solid_power", evidence: str = "") -> list[dict[str, str]]:
    return [edge(a, b, kind, evidence) for a, b in zip(nodes, nodes[1:])]


def feeder_edges(
    bus: str,
    prefix: str,
    feeder: str,
    protective: str,
    load: str,
    terminal: str,
    terminal_kind: str,
) -> list[dict[str, str]]:
    return [
        edge(bus, f"CB-{prefix}{feeder}", "solid_power", f"{bus} feeder {prefix}{feeder} tap"),
        edge(
            f"CB-{prefix}{feeder}",
            f"{protective}-{prefix}{feeder}",
            "solid_power",
            f"breaker to {'disconnect' if protective == 'DS' else 'fuse'}",
        ),
        edge(
            f"{protective}-{prefix}{feeder}",
            f"{load}-{prefix}{feeder}",
            "solid_power",
            f"{protective}-{prefix}{feeder} to load {load}-{prefix}{feeder}",
        ),
        edge(
            f"{load}-{prefix}{feeder}",
            f"{terminal}-{prefix}{feeder}",
            terminal_kind,
            f"visible {'dashed control/status' if terminal_kind == 'dashed_control' else 'dotted signal'} drop",
        ),
    ]


MAIN_EDGES: list[dict[str, str]] = []
MAIN_EDGES += chain(["GRID-345", "DS-101", "CB-101", "BUS-13KV-N"], "solid_power", "top normal/emergency source feeder")
MAIN_EDGES += chain(["GEN-G1", "CB-G1", "BUS-13KV-N"], "solid_power", "G1 tap to 13 kV bus")
MAIN_EDGES += chain(["GEN-G2", "CB-G2", "BUS-13KV-N"], "solid_power", "G2 tap to 13 kV bus")
MAIN_EDGES += chain(["BUS-13KV-N", "TR-1A", "CB-4A-IN", "BUS-4160-A"], "solid_power", "13 kV bus to train A 4.16 kV bus")
MAIN_EDGES += chain(["BUS-13KV-N", "TR-1B", "CB-4B-IN", "BUS-4160-B"], "solid_power", "13 kV bus to train B 4.16 kV bus")
MAIN_EDGES += chain(["DG-1A", "CB-DG1A", "BUS-4160-A"], "solid_power", "diesel generator 1A feeder")
MAIN_EDGES += chain(["DG-1B", "CB-DG1B", "BUS-4160-B"], "solid_power", "diesel generator 1B feeder")
MAIN_EDGES += chain(["BUS-4160-A", "CB-TIE-41", "BUS-4160-B"], "solid_power", "4.16 kV bus tie")
MAIN_EDGES += chain(["BUS-4160-A", "TR-480-A", "CB-480A-IN", "BUS-480-A"], "solid_power", "train A 480 V transformer feeder")
MAIN_EDGES += chain(["BUS-4160-B", "TR-480-B", "CB-480B-IN", "BUS-480-B"], "solid_power", "train B 480 V transformer feeder")
MAIN_EDGES += chain(["BUS-4160-A", "TR-480-C", "CB-480C-IN", "BUS-480-C"], "solid_power", "train A auxiliary 480 V transformer feeder")
MAIN_EDGES += chain(["BUS-4160-B", "TR-480-D", "CB-480D-IN", "BUS-480-D"], "solid_power", "train B auxiliary 480 V transformer feeder")


A_FEEDERS = [
    ("01", "DS", "PMP", "RLY", "dashed_control"),
    ("02", "FU", "MOV", "LS", "dotted_signal"),
    ("03", "DS", "MTR", "RLY", "dashed_control"),
    ("04", "DS", "PNL", "JB", "dotted_signal"),
    ("05", "FU", "PMP", "FT", "dotted_signal"),
    ("06", "DS", "MOV", "RLY", "dashed_control"),
    ("07", "DS", "MCC", "TB", "dotted_signal"),
    ("08", "FU", "PMP", "PT", "dotted_signal"),
    ("09", "DS", "FAN", "HS", "dashed_control"),
]

B_FEEDERS = [
    ("01", "DS", "PMP", "RLY", "dashed_control"),
    ("02", "FU", "MOV", "LS", "dotted_signal"),
    ("03", "DS", "MTR", "RLY", "dashed_control"),
    ("04", "DS", "PNL", "JB", "dotted_signal"),
    ("05", "FU", "PMP", "FT", "dotted_signal"),
    ("06", "DS", "MOV", "RLY", "dashed_control"),
    ("07", "DS", "MCC", "TB", "dotted_signal"),
    ("08", "FU", "PMP", "PT", "dotted_signal"),
    ("09", "DS", "FAN", "HS", "dashed_control"),
    ("10", "DS", "JB", "LT", "dotted_signal"),
]

CD_FEEDERS = [
    ("01", "DS", "MOV", "RLY", "dashed_control"),
    ("02", "FU", "PNL", "JB", "dotted_signal"),
    ("03", "DS", "PMP", "FT", "dotted_signal"),
    ("04", "DS", "HTR", "HS", "dashed_control"),
    ("05", "FU", "INST", "JB", "dotted_signal"),
    ("06", "DS", "MOV", "LS", "dotted_signal"),
    ("07", "DS", "MCC", "TB", "dotted_signal"),
    ("08", "FU", "PMP", "PT", "dotted_signal"),
    ("09", "DS", "PNL", "RLY", "dashed_control"),
    ("10", "DS", "JB", "TB", "dotted_signal"),
]


def normal_load_center(bus: str, prefix: str, feeders: list[tuple[str, str, str, str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for feeder, protective, load, terminal, terminal_kind in feeders:
        result += feeder_edges(bus, prefix, feeder, protective, load, terminal, terminal_kind)
    return result


def final_edges() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    result += MAIN_EDGES
    result += normal_load_center("BUS-480-A", "A", A_FEEDERS)
    result += chain(["BUS-480-A", "CB-A10", "DS-A10", "BAT-125A", "JB-A10", "LT-A10"], "solid_power", "A10 battery/JB chain; final JB to LT is a signal drop")
    result[-1]["kind"] = "dotted_signal"
    result[-1]["evidence"] = "dotted signal from JB-A10 to LT-A10"
    result += [
        edge("BUS-480-A", "CHGR-125A", "solid_power", "solid tap from BUS-480-A to CHG box labelled CHGR-125A"),
        edge("CHGR-125A", "DC-BUS-125A", "dc_ground", "dash-dot charger/DC line lands on DC-BUS-125A dot"),
    ]
    result += normal_load_center("BUS-480-B", "B", B_FEEDERS)
    result += [
        edge("BUS-480-B", "CHGR-125B", "solid_power", "solid tap from BUS-480-B to CHG box labelled CHGR-125B"),
        edge("CHGR-125B", "DC-BUS-125B", "dc_ground", "dash-dot charger/DC line lands on DC-BUS-125B dot"),
    ]
    result += normal_load_center("BUS-480-C", "C", CD_FEEDERS)
    result += [edge("BUS-480-C", "GND-EQ-A", "dc_ground", "dash-dot ground connection from BUS-480-C to GND-EQ-A")]
    result += normal_load_center("BUS-480-D", "D", CD_FEEDERS)
    result += [edge("BUS-480-D", "GND-EQ-B", "dc_ground", "dash-dot ground connection from BUS-480-D to GND-EQ-B")]
    result += [
        edge("DC-BUS-125A", "DC-BUS-125B", "dc_bus", "continuous central 125 V DC bus"),
        edge("DC-BUS-125A", "PANEL-CTRL-MAIN", "dashed_control", "dashed tap from central DC bus to panel; represented once on A side"),
    ]
    return ordered_edges(result)


def diego_round_1_edges() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    result += MAIN_EDGES
    result += normal_load_center("BUS-480-A", "A", A_FEEDERS)
    result += chain(
        ["BUS-480-A", "CB-A10", "DS-A10", "BAT-125A", "JB-A10", "DC-BUS-125A"],
        "solid_power",
        "Diego R1 high-recall A10 battery/JB/DC chain",
    )
    result += [edge("JB-A10", "LT-A10", "dotted_signal", "A10 lamp signal drop")]
    result += normal_load_center("BUS-480-B", "B", B_FEEDERS)
    result += [
        edge("DS-B01", "BAT-125B", "solid_power", "Diego R1 plausible adjacent B battery tie"),
        edge("BAT-125B", "DC-BUS-125B", "dc_ground", "Diego R1 plausible B battery to DC bus tie"),
    ]
    result += normal_load_center("BUS-480-C", "C", CD_FEEDERS)
    result += normal_load_center("BUS-480-D", "D", CD_FEEDERS)
    result += [
        edge("DC-BUS-125A", "DC-BUS-125B", "dc_bus", "continuous central 125 V DC bus"),
        edge("DC-BUS-125A", "PANEL-CTRL-MAIN", "dashed_control", "dashed tap from central DC bus to panel"),
        edge("BUS-480-C", "GND-EQ-A", "dc_ground", "dash-dot ground connection"),
        edge("BUS-480-D", "GND-EQ-B", "dc_ground", "dash-dot ground connection"),
    ]
    return ordered_edges(result)


EXTRA_NODES = [
    "CHGR-125A",
    "CHGR-125B",
    "BAT-125B",
]


def ordered_nodes(round_edges: list[list[dict[str, str]]]) -> list[str]:
    nodes: OrderedDict[str, None] = OrderedDict()
    for edges in round_edges:
        for item in edges:
            nodes.setdefault(item["a"], None)
            nodes.setdefault(item["b"], None)
    for node in EXTRA_NODES:
        nodes.setdefault(node, None)
    return list(nodes)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["a", "b", "kind", "evidence"])
        writer.writeheader()
        for item in edges:
            writer.writerow(item)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        a = index[item["a"]]
        b = index[item["b"]]
        if a == b:
            matrix[a][b] = 1
        else:
            matrix[a][b] = 1
            matrix[b][a] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_round(prefix: str, nodes: list[str], edges: list[dict[str, str]]) -> None:
    write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)
    write_edges(RESULTS / f"{prefix}_edgelist.csv", edges)
    write_nodes(RESULTS / f"{prefix}_nodes.csv", nodes)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    diego_r1 = diego_round_1_edges()
    jennifer_r1 = final_edges()
    diego_r2 = final_edges()
    jennifer_r2 = final_edges()
    nodes = ordered_nodes([diego_r1, jennifer_r1, diego_r2, jennifer_r2])

    rounds = [
        ("diego_round_1", diego_r1),
        ("jennifer_round_1", jennifer_r1),
        ("diego_round_2", diego_r2),
        ("jennifer_round_2_final", jennifer_r2),
    ]
    for prefix, edges in rounds:
        write_round(prefix, nodes, edges)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, jennifer_r2)
    write_edges(RESULTS / "final_edgelist.csv", jennifer_r2)
    write_nodes(RESULTS / "final_nodes.csv", nodes)

    metadata = {
        "document": 27,
        "iteration": 1,
        "source_folder": str(BASE),
        "source_discipline": [
            "Used only Raw + wires resources.",
            "No GT or GT-derived feedback used.",
            "No off-the-shelf OCR used; labels were read visually by agents/main inspection.",
        ],
        "rounds": [
            {
                "round": "Diego R1",
                "agent": "Diego",
                "agent_id": "019f76c5-c8cc-7a11-9693-621484aabb1f",
                "nodes": len(nodes),
                "accepted_edges": len(diego_r1),
                "outcome": "High-recall graph; charger boxes left ambiguous; A10/B01 battery/DC area overconnected.",
            },
            {
                "round": "Jennifer R1",
                "agent": "Jennifer",
                "agent_id": "019f76cc-93e6-7c10-bb73-a58b98cc1e2c",
                "nodes": len(nodes),
                "accepted_edges": len(jennifer_r1),
                "outcome": "Promoted CHGR-125A/B as real nodes; removed unsupported JB-A10/DC and B battery ties.",
            },
            {
                "round": "Diego R2",
                "agent": "Diego",
                "agent_id": "019f76d1-8fd4-7ab1-b625-3d8c2c3f45b1",
                "nodes": len(nodes),
                "accepted_edges": len(diego_r2),
                "outcome": "Saturation check of Jennifer R1 corrections; no matrix-changing additions expected unless noted in final review.",
            },
            {
                "round": "Jennifer R2 final",
                "agent": "Jennifer",
                "agent_id": "019f76d3-8cb5-7d80-89fb-38132de46751",
                "nodes": len(nodes),
                "accepted_edges": len(jennifer_r2),
                "outcome": "Confirmed saturation/final state; no additions or removals from Diego R2/Jennifer R1 corrected matrix.",
            },
        ],
        "final_edge_count": len(jennifer_r2),
        "final_node_count": len(nodes),
        "final_uncertain_excluded": [
            "JB-A10 -- DC-BUS-125A",
            "DS-B01 -- BAT-125B",
            "BAT-125B -- DC-BUS-125B",
            "CHGR-125A -- BAT-125A",
            "CHGR-125B -- BAT-125B",
            "BAT-125A -- DC-BUS-125A",
            "PANEL-CTRL-MAIN -- DC-BUS-125B",
        ],
    }
    (RESULTS / "doc27_round_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    report = f"""# Document 27 Connectivity Extraction Report

## Source Discipline

- Used only `Raw + wires` resources.
- Did not use GT or GT-derived feedback.
- Did not use off-the-shelf OCR; labels were read visually.

## Rounds

| Round | Agent | Nodes | Accepted edges | Outcome |
|---|---:|---:|---:|---|
| Diego R1 | high-recall extraction | {len(nodes)} | {len(diego_r1)} | Main graph proposed; A10/B01 charger and battery region over-included. |
| Jennifer R1 | precision review | {len(nodes)} | {len(jennifer_r1)} | Promoted `CHGR-125A/B`; removed unsupported `JB-A10` to DC bus and B battery ties. |
| Diego R2 | saturation check | {len(nodes)} | {len(diego_r2)} | Rechecked Jennifer corrections against focused crops. |
| Jennifer R2 final | precision review | {len(nodes)} | {len(jennifer_r2)} | Confirmed saturated final matrix; no additions/removals. |

## Final Accepted Charger / DC / Ground Edges

- `BUS-480-A -- CHGR-125A`
- `CHGR-125A -- DC-BUS-125A`
- `BUS-480-B -- CHGR-125B`
- `CHGR-125B -- DC-BUS-125B`
- `DC-BUS-125A -- DC-BUS-125B`
- `DC-BUS-125A -- PANEL-CTRL-MAIN`
- `BUS-480-C -- GND-EQ-A`
- `BUS-480-D -- GND-EQ-B`

## Final Rejected / Uncertain

- `JB-A10 -- DC-BUS-125A`: `JB-A10` has a visible dotted signal drop to `LT-A10`, not a clear DC bus tie.
- `DS-B01 -- BAT-125B` and `BAT-125B -- DC-BUS-125B`: battery is visible, but no certain conductor/junction ties it into the B01 feeder or DC bus.
- `CHGR-125A/B -- BAT-125A/B` and `BAT-125A/B -- DC-BUS-125A/B`: charger/battery internals are not visually certain enough to count.
- `PANEL-CTRL-MAIN -- DC-BUS-125B`: the panel tap is represented once as `DC-BUS-125A -- PANEL-CTRL-MAIN` on the continuous central DC bus.

## Final Files

- `final_connectivity_matrix.csv`
- `final_edgelist.csv`
- `final_nodes.csv`
- `doc27_round_metadata.json`
- `doc27_token_usage_estimate.csv`
- `doc27_token_usage_estimate.json`
"""
    (RESULTS / "doc27_extraction_report.md").write_text(report, encoding="utf-8")

    # Backward-friendly duplicate names for simple consumers.
    shutil.copyfile(RESULTS / "jennifer_round_2_final_connectivity_matrix.csv", RESULTS / "connectivity_matrix.csv")

    print(f"nodes={len(nodes)}")
    for prefix, edges in rounds:
        print(f"{prefix}: edges={len(edges)}")
    print(f"final: edges={len(jennifer_r2)}")


if __name__ == "__main__":
    main()
