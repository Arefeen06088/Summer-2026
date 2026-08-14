from __future__ import annotations

import csv
import json
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def add_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def edge(edges: list[dict[str, str]], source: str, target: str, evidence: str) -> None:
    if source == target:
        raise ValueError(f"self-edge requested for {source}")
    key = tuple(sorted((source, target)))
    for existing in edges:
        if tuple(sorted((existing["source"], existing["target"]))) == key:
            return
    edges.append({"source": source, "target": target, "evidence": evidence})


def source_nodes() -> list[str]:
    return [
        "GRID-345",
        "DS-101",
        "CB-101",
        "BUS-13KV-N",
        "GEN-G1",
        "CB-G1",
        "GEN-G2",
        "CB-G2",
        "TR-1A",
        "CB-4A-IN",
        "BUS-4160-A",
        "DG-1A",
        "CB-DG1A",
        "TR-1B",
        "CB-4B-IN",
        "BUS-4160-B",
        "DG-1B",
        "CB-DG1B",
        "CB-TIE-41",
        "TR-480-A",
        "CB-480A-IN",
        "BUS-480-A",
        "TR-480-B",
        "CB-480B-IN",
        "BUS-480-B",
        "TR-480-C",
        "CB-480C-IN",
        "BUS-480-C",
        "TR-480-D",
        "CB-480D-IN",
        "BUS-480-D",
    ]


AB_PATTERN = OrderedDict(
    [
        ("01", ("DS", "PMP", "RLY")),
        ("02", ("FU", "MOV", "LS")),
        ("03", ("DS", "MTR", "RLY")),
        ("04", ("DS", "PNL", "JB")),
        ("05", ("FU", "PMP", "FT")),
        ("06", ("DS", "MOV", "RLY")),
        ("07", ("DS", "MCC", "TB")),
        ("08", ("FU", "PMP", "PT")),
        ("09", ("DS", "FAN", "HS")),
        ("10", ("DS", "JB", "LT")),
    ]
)

C_PATTERN = OrderedDict(
    [
        ("01", ("DS", "MOV", "RLY")),
        ("02", ("FU", "PNL", "JB")),
        ("03", ("DS", "PMP", "FT")),
        ("04", ("DS", "HTR", "HS")),
        ("05", ("FU", "INST", "JB")),
        ("06", ("DS", "MOV", "LS")),
        ("07", ("DS", "MCC", "TB")),
        ("08", ("FU", "PMP", "PT")),
        ("09", ("DS", "PNL", "RLY")),
        ("10", ("DS", "JB", "TB")),
    ]
)


def branch_nodes(prefix: str, special_a10: bool = False) -> list[str]:
    nodes: list[str] = []
    pattern = AB_PATTERN if prefix in {"A", "B"} else C_PATTERN
    for number, (protection, load, endpoint) in pattern.items():
        add_unique(nodes, f"CB-{prefix}{number}")
        add_unique(nodes, f"{protection}-{prefix}{number}")
        if special_a10 and prefix == "A" and number == "10":
            add_unique(nodes, "BAT-125A")
            add_unique(nodes, "JB-A10")
            add_unique(nodes, "LT-A10")
        else:
            add_unique(nodes, f"{load}-{prefix}{number}")
            add_unique(nodes, f"{endpoint}-{prefix}{number}")
    return nodes


def final_nodes() -> list[str]:
    nodes = source_nodes()
    nodes.extend(branch_nodes("A", special_a10=True))
    nodes.extend(["CHGR-125A", "DC-BUS-125A"])
    nodes.extend(branch_nodes("B"))
    nodes.extend(["CHGR-125B", "BAT-125B", "DC-BUS-125B", "PANEL-CTRL-MAIN"])
    nodes.extend(branch_nodes("C"))
    nodes.append("GND-EO-A")
    nodes.extend(branch_nodes("D"))
    nodes.append("GND-EO-B")
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({n for n in nodes if nodes.count(n) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")
    return nodes


def diego_round1_nodes() -> list[str]:
    nodes = final_nodes()
    return ["GND-EQ-A" if n == "GND-EO-A" else "GND-EQ-B" if n == "GND-EO-B" else n for n in nodes]


def add_source_edges(edges: list[dict[str, str]]) -> None:
    edge(edges, "GRID-345", "DS-101", "solid grid source chain")
    edge(edges, "DS-101", "CB-101", "solid grid source chain")
    edge(edges, "CB-101", "BUS-13KV-N", "solid grid source chain to 13 kV bus")
    edge(edges, "GEN-G1", "CB-G1", "generator G1 vertical feeder")
    edge(edges, "CB-G1", "BUS-13KV-N", "generator G1 tap to 13 kV bus")
    edge(edges, "GEN-G2", "CB-G2", "generator G2 vertical feeder")
    edge(edges, "CB-G2", "BUS-13KV-N", "generator G2 tap to 13 kV bus")
    edge(edges, "BUS-13KV-N", "TR-1A", "normal transformer A feed")
    edge(edges, "TR-1A", "CB-4A-IN", "normal transformer A incomer")
    edge(edges, "CB-4A-IN", "BUS-4160-A", "normal transformer A incomer to 4.16 kV bus")
    edge(edges, "BUS-13KV-N", "TR-1B", "normal transformer B feed")
    edge(edges, "TR-1B", "CB-4B-IN", "normal transformer B incomer")
    edge(edges, "CB-4B-IN", "BUS-4160-B", "normal transformer B incomer to 4.16 kV bus")
    edge(edges, "DG-1A", "CB-DG1A", "diesel generator A feeder")
    edge(edges, "CB-DG1A", "BUS-4160-A", "diesel generator A bus tap")
    edge(edges, "DG-1B", "CB-DG1B", "diesel generator B feeder")
    edge(edges, "CB-DG1B", "BUS-4160-B", "diesel generator B bus tap")
    edge(edges, "BUS-4160-A", "CB-TIE-41", "4.16 kV bus tie")
    edge(edges, "CB-TIE-41", "BUS-4160-B", "4.16 kV bus tie")
    edge(edges, "BUS-4160-A", "TR-480-A", "480 V transformer A feeder")
    edge(edges, "TR-480-A", "CB-480A-IN", "480 V transformer A incomer")
    edge(edges, "CB-480A-IN", "BUS-480-A", "480 V load center A incomer")
    edge(edges, "BUS-4160-B", "TR-480-B", "480 V transformer B feeder")
    edge(edges, "TR-480-B", "CB-480B-IN", "480 V transformer B incomer")
    edge(edges, "CB-480B-IN", "BUS-480-B", "480 V load center B incomer")
    edge(edges, "BUS-4160-A", "TR-480-C", "480 V transformer C feeder")
    edge(edges, "TR-480-C", "CB-480C-IN", "480 V transformer C incomer")
    edge(edges, "CB-480C-IN", "BUS-480-C", "480 V load center C incomer")
    edge(edges, "BUS-4160-B", "TR-480-D", "480 V transformer D feeder")
    edge(edges, "TR-480-D", "CB-480D-IN", "480 V transformer D incomer")
    edge(edges, "CB-480D-IN", "BUS-480-D", "480 V load center D incomer")


def add_branch_edges(edges: list[dict[str, str]], prefix: str, special_a10: bool = False) -> None:
    pattern = AB_PATTERN if prefix in {"A", "B"} else C_PATTERN
    bus = f"BUS-480-{prefix}"
    for number, (protection, load, endpoint) in pattern.items():
        cb = f"CB-{prefix}{number}"
        prot = f"{protection}-{prefix}{number}"
        evidence = f"load center {prefix} branch {number}"
        edge(edges, bus, cb, f"{evidence} bus tap")
        edge(edges, cb, prot, f"{evidence} CB to protection device")
        if special_a10 and prefix == "A" and number == "10":
            edge(edges, prot, "BAT-125A", "A10 branch passes through BAT-125A")
            edge(edges, "BAT-125A", "JB-A10", "A10 battery to junction box chain")
            edge(edges, "JB-A10", "LT-A10", "A10 dotted signal to LT-A10")
        else:
            load_node = f"{load}-{prefix}{number}"
            endpoint_node = f"{endpoint}-{prefix}{number}"
            edge(edges, prot, load_node, f"{evidence} protection to load")
            edge(edges, load_node, endpoint_node, f"{evidence} control/signal drop")


def base_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    add_source_edges(edges)
    add_branch_edges(edges, "A", special_a10=True)
    add_branch_edges(edges, "B")
    add_branch_edges(edges, "C")
    add_branch_edges(edges, "D")
    return edges


def final_edges() -> list[dict[str, str]]:
    edges = base_edges()
    edge(edges, "JB-A10", "DC-BUS-125A", "A10 junction box solid tie to 125 VDC bus A")
    edge(edges, "BUS-480-A", "CHGR-125A", "charger A tapped from 480 V bus A")
    edge(edges, "CHGR-125A", "DC-BUS-125A", "charger A dash-dot tie to 125 VDC bus A")
    edge(edges, "BUS-480-B", "CHGR-125B", "charger B tapped from 480 V bus B")
    edge(edges, "CHGR-125B", "DC-BUS-125B", "charger B dash-dot tie to 125 VDC bus B")
    edge(edges, "BAT-125B", "DC-BUS-125B", "battery B vertical tie to 125 VDC bus B")
    edge(edges, "DC-BUS-125A", "DC-BUS-125B", "continuous horizontal 125 VDC bus")
    edge(edges, "DC-BUS-125A", "PANEL-CTRL-MAIN", "control panel tap from 125 VDC bus A side")
    edge(edges, "PANEL-CTRL-MAIN", "DC-BUS-125B", "control panel tap to 125 VDC bus B side")
    edge(edges, "BUS-480-C", "GND-EO-A", "dash-dot ground electrode tie from bus C")
    edge(edges, "BUS-480-D", "GND-EO-B", "dash-dot ground electrode tie from bus D")
    return edges


def diego_round1_edges() -> list[dict[str, str]]:
    edges = base_edges()
    edge(edges, "JB-A10", "DC-BUS-125A", "Diego accepted A10/JB tie to DC bus A")
    edge(edges, "BAT-125B", "DC-BUS-125B", "Diego accepted battery B tie to DC bus B")
    edge(edges, "DC-BUS-125A", "PANEL-CTRL-MAIN", "Diego accepted DC bus A control-panel tap")
    edge(edges, "PANEL-CTRL-MAIN", "DC-BUS-125B", "Diego accepted control-panel/DC bus B tap")
    edge(edges, "BUS-480-C", "GND-EQ-A", "Diego round-1 ground tie with misread label")
    edge(edges, "BUS-480-D", "GND-EQ-B", "Diego round-1 ground tie with misread label")
    edge(edges, "CHGR-125A", "DC-BUS-125A", "Diego high-recall charger A to DC bus candidate")
    edge(edges, "CHGR-125A", "BAT-125A", "Diego high-recall charger A to battery A candidate")
    edge(edges, "CHGR-125B", "DC-BUS-125B", "Diego high-recall charger B to DC bus candidate")
    edge(edges, "CHGR-125B", "BAT-125B", "Diego high-recall charger B to battery B candidate")
    edge(edges, "DS-B01", "BAT-125B", "Diego high-recall B01/battery adjacency candidate")
    edge(edges, "DC-BUS-125A", "DC-BUS-125B", "Diego high-recall continuous DC bus candidate")
    return edges


def validate(nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    node_set = set(nodes)
    referenced = {e["source"] for e in edges} | {e["target"] for e in edges}
    missing = sorted(referenced - node_set)
    if missing:
        raise ValueError(f"edges reference missing nodes: {missing}")
    pairs = [tuple(sorted((e["source"], e["target"]))) for e in edges]
    if len(pairs) != len(set(pairs)):
        raise ValueError("duplicate undirected edges")
    matrix = [[0 for _ in nodes] for _ in nodes]
    index = {node: i for i, node in enumerate(nodes)}
    for item in edges:
        i = index[item["source"]]
        j = index[item["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    zero_diagonal = all(matrix[i][i] == 0 for i in range(len(nodes)))
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "symmetric": symmetric,
        "zero_diagonal": zero_diagonal,
        "unique_nodes": len(nodes) == len(node_set),
    }


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        i = index[item["source"]]
        j = index[item["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node"])
        for node in nodes:
            writer.writerow([node])


def write_note(rounds: dict[str, tuple[list[str], list[dict[str, str]]]], final_validation: dict[str, object]) -> None:
    now = datetime.now().replace(microsecond=0).isoformat()
    rows = "\n".join(
        f"| `{name}` | {len(nodes)} | {len(edges)} |"
        for name, (nodes, edges) in rounds.items()
    )
    note = f"""# Case 27 Connectivity Extraction Note

Generated: {now}

## Scope

- Raw resource: `raw -- synthetic_npp_electrical_schematic_readable.png`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Sibling derived-resource folders and any ground-truth material were not opened or used.

## Subagent Rounds

1. Diego high-recall pass: proposed the full component set, kept visually plausible DC/battery/charger extras, and misread `GND-EO-A/B` as `GND-EQ-A/B`.
2. Jennifer precision pass: corrected the ground labels to `GND-EO-A/B`, removed unsupported direct charger-to-battery and `DS-B01 -- BAT-125B` edges, and accepted the A10 battery chain plus the continuous 125 VDC bus.
3. Diego saturation pass: AGREED with Jennifer's precision graph.
4. Jennifer final confirmation: AGREED.

## Final Decisions

- Final rows are component/node labels only.
- Wire route captions, titles, notes, grid markings, legend labels, and unlabeled tick marks are excluded as rows.
- Direct drawn adjacencies are encoded, not transitive closure across an entire bus.
- `BAT-125A` is modeled in the A10 branch: `DS-A10 -- BAT-125A -- JB-A10`.
- `BAT-125B` is modeled as a separate battery tied to `DC-BUS-125B`, not part of the B01 pump branch.
- `DC-BUS-125A` and `DC-BUS-125B` are retained as separate labels with a direct edge because they are drawn on a continuous horizontal bus.

## Counts

- Final nodes: {final_validation["node_count"]}
- Final undirected component edges: {final_validation["edge_count"]}
- Matrix is symmetric with zero diagonal: {final_validation["symmetric"] and final_validation["zero_diagonal"]}

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
{rows}

## Output Files

- `connectivity_matrix.csv`
- `final_connectivity_matrix.csv`
- `final_nodes.csv`
- `final_edges.csv`
- `connectivity_graph.json`
- `validation_summary.json`
- `round_01_diego_high_recall_matrix.csv`
- `round_02_jennifer_precision_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_agreement_matrix.csv`
- `token_performance_tracking.csv`
- `token_performance_traking.csv`
"""
    (RESULTS_DIR / "extraction_note.md").write_text(note, encoding="utf-8")


def write_tracking(round_validations: dict[str, dict[str, object]]) -> None:
    rows = [
        [
            "stage",
            "agent",
            "role",
            "artifact",
            "node_count",
            "edge_count",
            "token_accounting",
            "decision",
        ],
        [
            "prep",
            "Codex",
            "orchestrator",
            "codes/make_crops.py and codes/crops",
            "",
            "",
            "runtime exact token counts not exposed; artifacts updated for traceability",
            "raw-derived crops generated for visual inspection",
        ],
        [
            "round_01",
            "Diego",
            "high-recall extractor",
            "round_01_diego_high_recall_matrix.csv",
            round_validations["round_01_diego_high_recall"]["node_count"],
            round_validations["round_01_diego_high_recall"]["edge_count"],
            "exact subagent token count not exposed",
            "included DC/charger/battery candidates and preserved the initial ground-label read",
        ],
        [
            "round_02",
            "Jennifer",
            "precision reviewer/refiner",
            "round_02_jennifer_precision_matrix.csv",
            round_validations["round_02_jennifer_precision"]["node_count"],
            round_validations["round_02_jennifer_precision"]["edge_count"],
            "exact subagent token count not exposed",
            "fixed GND-EO labels and removed unsupported direct charger-to-battery/B01-battery edges",
        ],
        [
            "round_03",
            "Diego",
            "saturation extractor",
            "round_03_diego_saturation_matrix.csv",
            round_validations["round_03_diego_saturation"]["node_count"],
            round_validations["round_03_diego_saturation"]["edge_count"],
            "exact subagent token count not exposed",
            "AGREED with Jennifer precision graph",
        ],
        [
            "round_04",
            "Jennifer",
            "final precision confirmation",
            "round_04_jennifer_agreement_matrix.csv",
            round_validations["round_04_jennifer_agreement"]["node_count"],
            round_validations["round_04_jennifer_agreement"]["edge_count"],
            "exact subagent token count not exposed",
            "AGREED final saturated matrix",
        ],
        [
            "final",
            "Codex",
            "orchestrator",
            "final_connectivity_matrix.csv",
            round_validations["final"]["node_count"],
            round_validations["final"]["edge_count"],
            "runtime exact token counts not exposed; see note for audit trail",
            "validated symmetric zero-diagonal component matrix",
        ],
    ]
    for name in ("token_performance_tracking.csv", "token_performance_traking.csv"):
        with (RESULTS_DIR / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows)


def main() -> None:
    final_node_list = final_nodes()
    final_edge_list = final_edges()
    round_map: dict[str, tuple[list[str], list[dict[str, str]]]] = {
        "round_01_diego_high_recall": (diego_round1_nodes(), diego_round1_edges()),
        "round_02_jennifer_precision": (final_node_list, final_edge_list),
        "round_03_diego_saturation": (final_node_list, final_edge_list),
        "round_04_jennifer_agreement": (final_node_list, final_edge_list),
    }
    validations = {name: validate(nodes, edges) for name, (nodes, edges) in round_map.items()}
    validations["final"] = validate(final_node_list, final_edge_list)

    for name, (nodes, edges) in round_map.items():
        write_matrix(RESULTS_DIR / f"{name}_matrix.csv", nodes, edges)
        write_edges(RESULTS_DIR / f"{name}_edges.csv", edges)

    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", final_node_list, final_edge_list)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_node_list, final_edge_list)
    write_edges(RESULTS_DIR / "final_edges.csv", final_edge_list)
    write_nodes(RESULTS_DIR / "final_nodes.csv", final_node_list)

    graph = {
        "case": 27,
        "raw_resource": str(RAW_DIR / "raw -- synthetic_npp_electrical_schematic_readable.png"),
        "nodes": final_node_list,
        "edges": final_edge_list,
        "validation": validations["final"],
        "rounds": validations,
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(validations, indent=2), encoding="utf-8")
    write_note(round_map, validations["final"])
    write_tracking(validations)
    print(json.dumps(validations, indent=2))


if __name__ == "__main__":
    main()
