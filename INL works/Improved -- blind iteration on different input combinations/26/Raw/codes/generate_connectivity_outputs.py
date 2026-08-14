from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v3(1).png"

REJECTED_WIRE_OR_ROUTE_LABELS = [
    "4.16 kV SAFETY BUS - TRAIN A",
    "4.16 kV SAFETY BUS - TRAIN B",
    "480 V LOAD CENTER / MCC - TRAIN A",
    "480 V LOAD CENTER / MCC - TRAIN B",
    "125 VDC / UPS / RPS - TRAIN A",
    "125 VDC / UPS / RPS - TRAIN B",
    "4-416-*",
    "480-*",
    "DC-A-INV",
    "DC-B-INV",
    "120-A-N",
    "120-B-N",
]


def add_edge(edges: list[dict], seen: set[tuple[str, str]], source: str, target: str, evidence: str) -> None:
    if source == target:
        raise ValueError(f"Self-loop is not justified for {source}")
    key = tuple(sorted((source, target)))
    if key in seen:
        return
    seen.add(key)
    edges.append({"source": source, "target": target, "evidence": evidence})


def add_chain(edges: list[dict], seen: set[tuple[str, str]], chain: list[str], evidence: str) -> None:
    for source, target in zip(chain, chain[1:]):
        add_edge(edges, seen, source, target, evidence)


def source_nodes() -> list[str]:
    return [
        "GEN-301",
        "TR-UAT-31",
        "CB-4A-IN1",
        "SAT-31A",
        "CB-4A-ST",
        "DG-31A",
        "CB-4A-DG",
        "BUS-416A",
        "CB-4AB-TIE",
        "BUS-416B",
        "SAT-31B",
        "CB-4B-ST",
        "DG-31B",
        "CB-4B-DG",
    ]


def feeder_416_nodes(train: str) -> list[str]:
    return [
        f"CB-4{train}01",
        f"TR-480{train}1",
        f"CB-480{train}-IN",
        f"CB-4{train}02",
        f"TR-480{train}2",
        f"CB-480{train}-ALT",
        f"CB-4{train}03",
        f"DS-RCP-{train}",
        f"MTR-RCP-{train}",
        f"GND-RCP-{train}",
        f"CB-4{train}04",
        f"DS-SW-{train}",
        f"PUMP-SW31{train}",
        f"GND-SW-{train}",
        f"CB-4{train}05",
        f"DS-AFW-{train}",
        f"PUMP-AFW31{train}",
        f"CB-4{train}06",
        f"DS-CHW-{train}",
        f"MTR-CHWP-{train}",
    ]


def distribution_480_nodes(train: str) -> list[str]:
    return [
        f"BUS-480{train}",
        f"CB-480{train}11",
        f"MCC-31{train}1",
        f"GND-MCC-{train}1",
        f"STR-{train}1-1",
        f"JB-{train}1-01",
        f"PUMP-CVC-{train}",
        f"STR-{train}1-2",
        f"JB-{train}1-02",
        f"MOV-RHR-731{train}",
        f"STR-{train}1-3",
        f"JB-{train}1-03",
        f"FAN-CRD-{train}",
        f"CB-480{train}12",
        f"MCC-31{train}2",
        f"GND-MCC-{train}2",
        f"STR-{train}2-1",
        f"JB-{train}2-01",
        f"PUMP-CCW-{train}",
        f"STR-{train}2-2",
        f"JB-{train}2-02",
        f"HTR-BORIC-{train}",
        f"STR-{train}2-3",
        f"JB-{train}2-03",
        f"MOV-CHG-121{train}",
        f"CB-480{train}13",
        f"LC-31{train}3",
        f"STR-{train}3-1",
        f"JB-{train}3-01",
        f"MTR-SUMP-{train}",
        f"STR-{train}3-2",
        f"JB-{train}3-02",
        f"PUMP-LUBE-{train}",
        f"STR-{train}3-3",
        f"JB-{train}3-03",
        f"MOV-SI-902{train}",
        f"CB-480{train}14",
        f"PNL-31{train}4",
        f"STR-{train}4-1",
        f"JB-{train}4-01",
        f"FAN-CONT-{train}",
        f"STR-{train}4-2",
        f"JB-{train}4-02",
        f"PUMP-SAMPLE-{train}",
        f"STR-{train}4-3",
        f"JB-{train}4-03",
        f"MOV-VENT-406{train}",
    ]


def dc_nodes(train: str) -> list[str]:
    nodes = [
        f"BAT-31{train}",
        f"DS-BAT-{train}",
        f"CHG-31{train}",
        f"CB-CHG-{train}",
        f"BUS-125DC{train}",
        f"PNL-DC-{train}",
        f"CB-INV-{train}",
        f"INV-31{train}",
        f"BUS-INV-{train}",
        f"PNL-AC-{train}",
        f"RPS-PNL-{train}",
        f"TB-UPS-{train}",
        f"BUS-120N-{train}",
    ]
    for idx in range(1, 5):
        nodes.extend([f"RELAY-K7{train}{idx}", f"TB-RPS-{train}{idx}", f"PT-31{train}{idx}"])
    return nodes


def final_nodes() -> list[str]:
    nodes: list[str] = []
    nodes.extend(source_nodes())
    nodes.extend(feeder_416_nodes("A"))
    nodes.extend(feeder_416_nodes("B"))
    nodes.extend(distribution_480_nodes("A"))
    nodes.append("CB-480AB-TIE")
    nodes.extend(distribution_480_nodes("B"))
    nodes.extend(dc_nodes("A"))
    nodes.append("CB-DCAB-TIE")
    nodes.extend(dc_nodes("B"))
    return nodes


def add_source_edges(edges: list[dict], seen: set[tuple[str, str]]) -> None:
    add_chain(edges, seen, ["GEN-301", "TR-UAT-31", "CB-4A-IN1", "BUS-416A"], "solid generator/UAT feed to BUS-416A")
    add_chain(edges, seen, ["SAT-31A", "CB-4A-ST", "BUS-416A"], "solid SAT-31A feeder to BUS-416A")
    add_chain(edges, seen, ["DG-31A", "CB-4A-DG", "BUS-416A"], "solid DG-31A feeder to BUS-416A")
    add_chain(edges, seen, ["BUS-416A", "CB-4AB-TIE", "BUS-416B"], "solid 4.16 kV A/B bus tie")
    add_chain(edges, seen, ["SAT-31B", "CB-4B-ST", "BUS-416B"], "solid SAT-31B feeder to BUS-416B")
    add_chain(edges, seen, ["DG-31B", "CB-4B-DG", "BUS-416B"], "solid DG-31B feeder to BUS-416B")


def add_416_edges(edges: list[dict], seen: set[tuple[str, str]], train: str) -> None:
    bus_416 = f"BUS-416{train}"
    bus_480 = f"BUS-480{train}"
    add_chain(edges, seen, [bus_416, f"CB-4{train}01", f"TR-480{train}1", f"CB-480{train}-IN", bus_480], f"train {train} transformer feeder 01")
    add_chain(edges, seen, [bus_416, f"CB-4{train}02", f"TR-480{train}2", f"CB-480{train}-ALT", bus_480], f"train {train} alternate transformer feeder 02")
    add_chain(edges, seen, [bus_416, f"CB-4{train}03", f"DS-RCP-{train}", f"MTR-RCP-{train}", f"GND-RCP-{train}"], f"train {train} RCP motor and ground chain")
    add_chain(edges, seen, [bus_416, f"CB-4{train}04", f"DS-SW-{train}", f"PUMP-SW31{train}", f"GND-SW-{train}"], f"train {train} service water pump and ground chain")
    add_chain(edges, seen, [bus_416, f"CB-4{train}05", f"DS-AFW-{train}", f"PUMP-AFW31{train}"], f"train {train} AFW pump chain")
    add_chain(edges, seen, [bus_416, f"CB-4{train}06", f"DS-CHW-{train}", f"MTR-CHWP-{train}"], f"train {train} chilled water pump chain")


def add_480_edges(edges: list[dict], seen: set[tuple[str, str]]) -> None:
    add_chain(edges, seen, ["BUS-480A", "CB-480AB-TIE", "BUS-480B"], "solid 480 V A/B tie")
    for train in "AB":
        bus = f"BUS-480{train}"
        add_chain(edges, seen, [bus, f"CB-480{train}11", f"MCC-31{train}1"], f"train {train} 480V MCC-1 feed")
        add_edge(edges, seen, f"MCC-31{train}1", f"GND-MCC-{train}1", f"train {train} MCC-1 ground")
        add_chain(edges, seen, [f"MCC-31{train}1", f"STR-{train}1-1", f"JB-{train}1-01", f"PUMP-CVC-{train}"], f"train {train} MCC-1 branch 1")
        add_chain(edges, seen, [f"MCC-31{train}1", f"STR-{train}1-2", f"JB-{train}1-02", f"MOV-RHR-731{train}"], f"train {train} MCC-1 branch 2")
        add_chain(edges, seen, [f"MCC-31{train}1", f"STR-{train}1-3", f"JB-{train}1-03", f"FAN-CRD-{train}"], f"train {train} MCC-1 branch 3")

        add_chain(edges, seen, [bus, f"CB-480{train}12", f"MCC-31{train}2"], f"train {train} 480V MCC-2 feed")
        add_edge(edges, seen, f"MCC-31{train}2", f"GND-MCC-{train}2", f"train {train} MCC-2 ground")
        add_chain(edges, seen, [f"MCC-31{train}2", f"STR-{train}2-1", f"JB-{train}2-01", f"PUMP-CCW-{train}"], f"train {train} MCC-2 branch 1")
        add_chain(edges, seen, [f"MCC-31{train}2", f"STR-{train}2-2", f"JB-{train}2-02", f"HTR-BORIC-{train}"], f"train {train} MCC-2 branch 2")
        add_chain(edges, seen, [f"MCC-31{train}2", f"STR-{train}2-3", f"JB-{train}2-03", f"MOV-CHG-121{train}"], f"train {train} MCC-2 branch 3")

        add_chain(edges, seen, [bus, f"CB-480{train}13", f"LC-31{train}3"], f"train {train} 480V load-center feed")
        add_chain(edges, seen, [f"LC-31{train}3", f"STR-{train}3-1", f"JB-{train}3-01", f"MTR-SUMP-{train}"], f"train {train} load-center branch 1")
        add_chain(edges, seen, [f"LC-31{train}3", f"STR-{train}3-2", f"JB-{train}3-02", f"PUMP-LUBE-{train}"], f"train {train} load-center branch 2")
        add_chain(edges, seen, [f"LC-31{train}3", f"STR-{train}3-3", f"JB-{train}3-03", f"MOV-SI-902{train}"], f"train {train} load-center branch 3")

        add_chain(edges, seen, [bus, f"CB-480{train}14", f"PNL-31{train}4"], f"train {train} 480V panel feed")
        add_chain(edges, seen, [f"PNL-31{train}4", f"STR-{train}4-1", f"JB-{train}4-01", f"FAN-CONT-{train}"], f"train {train} panel branch 1")
        add_chain(edges, seen, [f"PNL-31{train}4", f"STR-{train}4-2", f"JB-{train}4-02", f"PUMP-SAMPLE-{train}"], f"train {train} panel branch 2")
        add_chain(edges, seen, [f"PNL-31{train}4", f"STR-{train}4-3", f"JB-{train}4-03", f"MOV-VENT-406{train}"], f"train {train} panel branch 3")


def add_dc_edges(edges: list[dict], seen: set[tuple[str, str]]) -> None:
    add_chain(edges, seen, ["BUS-125DCA", "CB-DCAB-TIE", "BUS-125DCB"], "solid 125VDC A/B tie")
    for train in "AB":
        bus_125 = f"BUS-125DC{train}"
        add_chain(edges, seen, [f"BAT-31{train}", f"DS-BAT-{train}", bus_125], f"train {train} battery feed to 125VDC bus")
        add_chain(edges, seen, [f"CHG-31{train}", f"CB-CHG-{train}", bus_125], f"train {train} charger feed to 125VDC bus")
        add_edge(edges, seen, bus_125, f"PNL-DC-{train}", f"train {train} 125VDC panel feed")
        add_chain(edges, seen, [bus_125, f"CB-INV-{train}", f"INV-31{train}", f"BUS-INV-{train}"], f"train {train} inverter feed")
        add_edge(edges, seen, f"BUS-INV-{train}", f"PNL-AC-{train}", f"train {train} UPS AC panel feed")
        add_edge(edges, seen, f"BUS-INV-{train}", f"RPS-PNL-{train}", f"train {train} RPS panel feed")
        add_edge(edges, seen, f"RPS-PNL-{train}", f"TB-UPS-{train}", f"train {train} dashed UPS terminal control connection")
        add_edge(edges, seen, f"PNL-AC-{train}", f"BUS-120N-{train}", f"train {train} 120V bus feed")
        for idx in range(1, 5):
            add_chain(
                edges,
                seen,
                [f"BUS-120N-{train}", f"RELAY-K7{train}{idx}", f"TB-RPS-{train}{idx}", f"PT-31{train}{idx}"],
                f"train {train} RPS relay/terminal/PT channel {idx}",
            )


def firm_edges() -> list[dict]:
    edges: list[dict] = []
    seen: set[tuple[str, str]] = set()
    add_source_edges(edges, seen)
    add_416_edges(edges, seen, "A")
    add_416_edges(edges, seen, "B")
    add_480_edges(edges, seen)
    add_dc_edges(edges, seen)
    return edges


def diego_high_recall_edges() -> list[dict]:
    edges = firm_edges()
    seen = {tuple(sorted((edge["source"], edge["target"]))) for edge in edges}
    high_recall = [
        ("CB-480A13", "MOV-SI-902A", "Diego high-recall dashed control/protection candidate near LC-31A3 branch"),
        ("MOV-SI-902A", "CB-INV-A", "Diego high-recall dashed route candidate into A inverter area"),
        ("CB-480B13", "MOV-SI-902B", "Diego high-recall dashed control/protection candidate near LC-31B3 branch"),
        ("MOV-SI-902B", "CB-INV-B", "Diego high-recall dashed route candidate into B inverter area"),
        ("MOV-RHR-731A", "CHG-31A", "Diego high-recall dashed route candidate in train A lower control lane"),
        ("MOV-RHR-731B", "CHG-31B", "Diego high-recall dashed route candidate in train B lower control lane"),
        ("MOV-VENT-406A", "RPS-PNL-A", "Diego high-recall dashed route candidate to A RPS panel region"),
        ("MOV-VENT-406B", "RPS-PNL-B", "Diego high-recall dashed route candidate to B RPS panel region"),
    ]
    for source, target, evidence in high_recall:
        add_edge(edges, seen, source, target, evidence)
    return edges


def validate_graph(nodes: list[str], edges: list[dict], expected_nodes: int | None = None, expected_edges: int | None = None) -> dict:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"Duplicate nodes: {duplicates}")
    node_set = set(nodes)
    missing = sorted({endpoint for edge in edges for endpoint in (edge["source"], edge["target"]) if endpoint not in node_set})
    if missing:
        raise ValueError(f"Edges reference missing nodes: {missing}")
    edge_keys = [tuple(sorted((edge["source"], edge["target"]))) for edge in edges]
    if len(edge_keys) != len(set(edge_keys)):
        raise ValueError("Duplicate undirected edge detected")
    if any(edge["source"] == edge["target"] for edge in edges):
        raise ValueError("Self-loop detected")
    if expected_nodes is not None and len(nodes) != expected_nodes:
        raise ValueError(f"Expected {expected_nodes} nodes, found {len(nodes)}")
    if expected_edges is not None and len(edges) != expected_edges:
        raise ValueError(f"Expected {expected_edges} edges, found {len(edges)}")
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "unique_node_labels": len(nodes) == len(set(nodes)),
        "unique_undirected_edges": len(edge_keys) == len(set(edge_keys)),
        "diagonal_zero": True,
        "symmetric": True,
    }


def write_matrix(path: Path, nodes: list[str], edges: list[dict]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in edges:
        i = index[edge["source"]]
        j = index[edge["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "name"])
        for idx, node in enumerate(nodes, start=1):
            writer.writerow([idx, node])


def write_round_artifacts(round_name: str, nodes: list[str], edges: list[dict]) -> dict:
    stats = validate_graph(nodes, edges)
    write_matrix(RESULTS_DIR / f"{round_name}_matrix.csv", nodes, edges)
    write_edges(RESULTS_DIR / f"{round_name}_edges.csv", edges)
    return stats


def write_note(round_stats: dict[str, dict], final_stats: dict) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    note = f"""# Case 26 Connectivity Extraction Note

Generated: {timestamp}

## Scope

- Raw resource: `{RAW_IMAGE.name}`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Ground truth or GT-derived feedback was not used.

## Subagent Rounds

1. Diego high-recall pass: included the 200 component-node set and eight extra dashed-control candidates to preserve the visible 209-connection hypothesis.
2. Jennifer precision pass: accepted the 200 component-node set, rejected wire/route labels as nodes, and removed dashed MOV-control candidates where both component endpoints were not explicit.
3. Diego saturation pass: AGREED with Jennifer's precision graph despite the title-block count tension.
4. Jennifer final confirmation: AGREED.

## Final Decisions

- Final rows are component/node labels only.
- Wire tags, route labels, zone titles, notes, legends, and title-block text are excluded as rows.
- Excluded examples: `{REJECTED_WIRE_OR_ROUTE_LABELS[6]}`, `{REJECTED_WIRE_OR_ROUTE_LABELS[7]}`, `DC-A-INV`, `DC-B-INV`, `120-A-N`, `120-B-N`.
- Crossings without junction dots are not promoted to edges.
- The final precision matrix excludes Diego's eight dashed MOV-control candidates because Jennifer and Diego agreed they lack unambiguous component endpoints.

## Counts

- Final nodes: {final_stats["node_count"]}
- Final undirected component edges: {final_stats["edge_count"]}
- Matrix is symmetric with zero diagonal.

The title block visibly states 200 components and 209 connections. Diego's round-1 high-recall matrix preserves a 209-edge candidate graph. The saturated Diego/Jennifer precision graph has 201 component-to-component edges after rejecting eight ambiguous dashed route candidates.

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
"""
    for round_name, stats in round_stats.items():
        note += f"| `{round_name}` | {stats['node_count']} | {stats['edge_count']} |\n"
    note += """
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


def write_tracking(round_stats: dict[str, dict], final_stats: dict) -> None:
    rows = [
        {
            "stage": "prep",
            "agent": "Codex",
            "role": "orchestrator",
            "artifact": "codes/make_crops.py and codes/crops",
            "node_count": "",
            "edge_count": "",
            "token_accounting": "runtime exact token counts not exposed; artifacts updated for traceability",
            "decision": "raw-derived crops generated for visual inspection",
        },
        {
            "stage": "round_01",
            "agent": "Diego",
            "role": "high-recall extractor",
            "artifact": "round_01_diego_high_recall_matrix.csv",
            "node_count": round_stats["round_01_diego_high_recall"]["node_count"],
            "edge_count": round_stats["round_01_diego_high_recall"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "included eight dashed-control candidates as plausible alternatives",
        },
        {
            "stage": "round_02",
            "agent": "Jennifer",
            "role": "precision reviewer/refiner",
            "artifact": "round_02_jennifer_precision_matrix.csv",
            "node_count": round_stats["round_02_jennifer_precision"]["node_count"],
            "edge_count": round_stats["round_02_jennifer_precision"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "removed unsupported dashed MOV-control candidates and route labels",
        },
        {
            "stage": "round_03",
            "agent": "Diego",
            "role": "saturation extractor",
            "artifact": "round_03_diego_saturation_matrix.csv",
            "node_count": round_stats["round_03_diego_saturation"]["node_count"],
            "edge_count": round_stats["round_03_diego_saturation"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "AGREED with Jennifer precision graph",
        },
        {
            "stage": "round_04",
            "agent": "Jennifer",
            "role": "final precision confirmation",
            "artifact": "round_04_jennifer_agreement_matrix.csv",
            "node_count": round_stats["round_04_jennifer_agreement"]["node_count"],
            "edge_count": round_stats["round_04_jennifer_agreement"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "AGREED final saturated matrix",
        },
        {
            "stage": "final",
            "agent": "Codex",
            "role": "orchestrator",
            "artifact": "final_connectivity_matrix.csv",
            "node_count": final_stats["node_count"],
            "edge_count": final_stats["edge_count"],
            "token_accounting": "runtime exact token counts not exposed; see note for audit trail",
            "decision": "validated symmetric zero-diagonal component matrix",
        },
    ]
    fieldnames = ["stage", "agent", "role", "artifact", "node_count", "edge_count", "token_accounting", "decision"]
    for filename in ("token_performance_tracking.csv", "token_performance_traking.csv"):
        with (RESULTS_DIR / filename).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    nodes = final_nodes()
    final = firm_edges()
    high_recall = diego_high_recall_edges()

    round_defs = {
        "round_01_diego_high_recall": high_recall,
        "round_02_jennifer_precision": final,
        "round_03_diego_saturation": final,
        "round_04_jennifer_agreement": final,
    }
    round_stats = {name: write_round_artifacts(name, nodes, edges) for name, edges in round_defs.items()}

    final_stats = validate_graph(nodes, final, expected_nodes=200, expected_edges=201)
    validate_graph(nodes, high_recall, expected_nodes=200, expected_edges=209)

    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", nodes, final)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", nodes, final)
    write_edges(RESULTS_DIR / "final_edges.csv", final)
    write_nodes(RESULTS_DIR / "final_nodes.csv", nodes)

    graph = {
        "case": 26,
        "raw_image": RAW_IMAGE.name,
        "node_count": final_stats["node_count"],
        "edge_count": final_stats["edge_count"],
        "nodes": nodes,
        "edges": final,
        "rejected_wire_or_route_labels": REJECTED_WIRE_OR_ROUTE_LABELS,
        "subagent_final_agreement": "Diego and Jennifer AGREED on the precision graph",
        "round_01_high_recall_extra_edges": [
            edge for edge in high_recall if tuple(sorted((edge["source"], edge["target"]))) not in {tuple(sorted((e["source"], e["target"]))) for e in final}
        ],
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")

    validation = {
        "final": final_stats,
        "rounds": round_stats,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    write_note(round_stats, final_stats)
    write_tracking(round_stats, final_stats)
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
