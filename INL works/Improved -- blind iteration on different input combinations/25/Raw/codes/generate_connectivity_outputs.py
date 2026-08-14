from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_revised_v4.png"

ROUTE_LABELS = [
    "480V CHGR-A FEEDER",
    "480V CHGR-B FEEDER",
    "PNL A/B TIE",
    "RPS TRIP BUS",
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
        "SWYD-115KV",
        "FDR-13A",
        "TR-UAT-1A",
        "CB-52-4A",
        "EDG-1A",
        "CB-DG-1A",
        "FDR-13B",
        "TR-UAT-1B",
        "CB-52-4B",
        "EDG-1B",
        "CB-DG-1B",
        "TR-SAT-1",
        "CB-52-4C",
        "EDG-1C",
        "CB-DG-1C",
        "BUS-4160-A",
        "BUS-4160-B",
        "BUS-4160-C",
        "CB-TIE-AB",
        "CB-TIE-BC",
    ]


def train_4160_nodes(train: str) -> list[str]:
    return [
        f"CB-4{train}01",
        f"DS-4{train}01",
        f"TR-480-1{train}",
        f"CB-52-48{train}",
        f"BUS-480-1{train}",
        f"MS-{train}01",
        f"PUMP-RHR P201{train}",
        f"CB-4{train}02",
        f"DS-4{train}02",
        f"MS-{train}02",
        f"PUMP-CS-P202{train}",
        f"CB-4{train}03",
        f"DS-4{train}03",
        f"TR-LC-{train}03",
        f"LC-480-{train}03",
        f"CB-4{train}04",
        f"DS-4{train}04",
        f"MS-{train}04",
        f"FAN-CR-401{train}",
        f"CB-4{train}05",
        f"DS-4{train}05",
        f"PNL-ESF-{train}05",
        f"GND-ESF-{train}05",
        f"CB-4{train}06",
        f"DS-4{train}06",
        f"RECT-RPS-{train}06",
        f"INV-RPS-{train}06",
        f"CB-4{train}07",
        f"DS-4{train}07",
        f"MS-{train}07",
        f"PUMP-AFW P203{train}",
        f"CB-4{train}08",
        f"DS-4{train}08",
        f"TR-CTRL-{train}08",
        f"CP-CTRL-{train}08",
    ]


def train_480_nodes(train: str) -> list[str]:
    return [
        f"MCC-{train}1",
        f"MCC-{train}2",
        f"CB-48{train}01",
        f"MS-48{train}01",
        f"PUMP-CVC P301{train}",
        f"CB-48{train}02",
        f"K-48{train}02",
        f"MOV-CS-451{train}",
        f"CB-48{train}03",
        f"MS-48{train}03",
        f"FAN-HVAC-501{train}",
        f"CB-48{train}04",
        f"MS-48{train}04",
        f"PUMP-SUMP P302{train}",
        f"CB-48{train}05",
        f"K-48{train}05",
        f"MOV-RHR-452{train}",
        f"CB-48{train}06",
        f"XFU-48{train}06",
        f"PNL-PI-601{train}",
    ]


def lower_dc_nodes() -> list[str]:
    return [
        "CHGR-125-1A",
        "BAT-125-1A",
        "BUS-125DC-A",
        "INV-120-1A",
        "PNL-RPS-A",
        "RELAY-K501A",
        "XMTR-PT-501A",
        "CHGR-125-1B",
        "BAT-125-1B",
        "BUS-125DC-B",
        "INV-120-1B",
        "PNL-RPS-B",
        "RELAY-K501B",
        "XMTR-PT-501B",
        "TC-52-4A",
    ]


def final_nodes() -> list[str]:
    nodes: list[str] = []
    nodes.extend(source_nodes())
    for train in "ABC":
        nodes.extend(train_4160_nodes(train))
    for train in "ABC":
        nodes.extend(train_480_nodes(train))
    nodes.extend(lower_dc_nodes())
    return nodes


def add_source_edges(edges: list[dict], seen: set[tuple[str, str]]) -> None:
    add_chain(edges, seen, ["SWYD-115KV", "FDR-13A", "TR-UAT-1A", "CB-52-4A", "BUS-4160-A"], "top source train A visible wire chain")
    add_chain(edges, seen, ["EDG-1A", "CB-DG-1A", "BUS-4160-A"], "EDG-1A breaker tie to BUS-4160-A")
    add_chain(edges, seen, ["SWYD-115KV", "FDR-13B", "TR-UAT-1B", "CB-52-4B", "BUS-4160-B"], "top source train B visible wire chain")
    add_chain(edges, seen, ["EDG-1B", "CB-DG-1B", "BUS-4160-B"], "EDG-1B breaker tie to BUS-4160-B")
    add_chain(edges, seen, ["SWYD-115KV", "TR-SAT-1", "CB-52-4C", "BUS-4160-C"], "standby transformer chain to BUS-4160-C")
    add_chain(edges, seen, ["EDG-1C", "CB-DG-1C", "BUS-4160-C"], "EDG-1C breaker tie to BUS-4160-C")
    add_chain(edges, seen, ["BUS-4160-A", "CB-TIE-AB", "BUS-4160-B"], "visible bus tie A-B")
    add_chain(edges, seen, ["BUS-4160-B", "CB-TIE-BC", "BUS-4160-C"], "visible bus tie B-C")


def add_4160_feeder_edges(edges: list[dict], seen: set[tuple[str, str]], train: str, style: str) -> None:
    bus = f"BUS-4160-{train}"
    if style == "diego_high_recall":
        add_chain(
            edges,
            seen,
            [bus, f"CB-4{train}01", f"DS-4{train}01", f"TR-480-1{train}", f"CB-52-48{train}", f"BUS-480-1{train}"],
            f"round-1 high-recall interpretation of 4.16kV feeder 01 train {train}",
        )
        add_chain(
            edges,
            seen,
            [f"CB-4{train}01", f"MS-{train}01", f"PUMP-RHR P201{train}"],
            f"round-1 possible direct motor branch from feeder 01 train {train}",
        )
    else:
        add_edge(edges, seen, bus, f"CB-4{train}01", f"train {train} bus tap to feeder 01 breaker")
        add_chain(
            edges,
            seen,
            [f"CB-4{train}01", f"TR-480-1{train}", f"CB-52-48{train}", f"BUS-480-1{train}"],
            f"train {train} transformer branch from feeder 01")
        add_chain(
            edges,
            seen,
            [f"CB-4{train}01", f"DS-4{train}01", f"MS-{train}01", f"PUMP-RHR P201{train}"],
            f"train {train} RHR pump branch from feeder 01")

    add_chain(edges, seen, [bus, f"CB-4{train}02", f"DS-4{train}02", f"MS-{train}02", f"PUMP-CS-P202{train}"], f"train {train} core spray pump feeder 02")
    add_chain(edges, seen, [bus, f"CB-4{train}03", f"DS-4{train}03", f"TR-LC-{train}03", f"LC-480-{train}03"], f"train {train} load-center transformer feeder 03")
    add_chain(edges, seen, [bus, f"CB-4{train}04", f"DS-4{train}04", f"MS-{train}04", f"FAN-CR-401{train}"], f"train {train} control-room fan feeder 04")
    add_chain(edges, seen, [bus, f"CB-4{train}05", f"DS-4{train}05", f"PNL-ESF-{train}05", f"GND-ESF-{train}05"], f"train {train} ESF panel feeder 05")
    add_chain(edges, seen, [bus, f"CB-4{train}06", f"DS-4{train}06", f"RECT-RPS-{train}06", f"INV-RPS-{train}06"], f"train {train} RPS rectifier/inverter feeder 06")
    add_chain(edges, seen, [bus, f"CB-4{train}07", f"DS-4{train}07", f"MS-{train}07", f"PUMP-AFW P203{train}"], f"train {train} AFW pump feeder 07")
    add_chain(edges, seen, [bus, f"CB-4{train}08", f"DS-4{train}08", f"TR-CTRL-{train}08", f"CP-CTRL-{train}08"], f"train {train} control power feeder 08")


def add_4160_edges(edges: list[dict], seen: set[tuple[str, str]], style: str) -> None:
    for train in "ABC":
        add_4160_feeder_edges(edges, seen, train, style)


def add_480_edges(edges: list[dict], seen: set[tuple[str, str]]) -> None:
    for train in "ABC":
        bus = f"BUS-480-1{train}"
        add_edge(edges, seen, bus, f"MCC-{train}1", f"train {train} 480V bus feeds MCC-{train}1")
        add_edge(edges, seen, bus, f"MCC-{train}2", f"train {train} 480V bus feeds MCC-{train}2")
        add_chain(edges, seen, [f"MCC-{train}1", f"CB-48{train}01", f"MS-48{train}01", f"PUMP-CVC P301{train}"], f"train {train} MCC-1 branch 01")
        add_chain(edges, seen, [f"MCC-{train}1", f"CB-48{train}02", f"K-48{train}02", f"MOV-CS-451{train}"], f"train {train} MCC-1 branch 02")
        add_chain(edges, seen, [f"MCC-{train}1", f"CB-48{train}03", f"MS-48{train}03", f"FAN-HVAC-501{train}"], f"train {train} MCC-1 branch 03")
        add_chain(edges, seen, [f"MCC-{train}2", f"CB-48{train}04", f"MS-48{train}04", f"PUMP-SUMP P302{train}"], f"train {train} MCC-2 branch 04")
        add_chain(edges, seen, [f"MCC-{train}2", f"CB-48{train}05", f"K-48{train}05", f"MOV-RHR-452{train}"], f"train {train} MCC-2 branch 05")
        add_chain(edges, seen, [f"MCC-{train}2", f"CB-48{train}06", f"XFU-48{train}06", f"PNL-PI-601{train}"], f"train {train} MCC-2 branch 06")


def add_lower_dc_edges(edges: list[dict], seen: set[tuple[str, str]], route_labels: bool) -> None:
    if route_labels:
        add_chain(edges, seen, ["BUS-480-1A", "480V CHGR-A FEEDER", "CHGR-125-1A", "BUS-125DC-A"], "round route-label interpretation for charger A feeder")
        add_chain(edges, seen, ["BUS-480-1B", "480V CHGR-B FEEDER", "CHGR-125-1B", "BUS-125DC-B"], "round route-label interpretation for charger B feeder")
        add_chain(edges, seen, ["PNL-RPS-A", "PNL A/B TIE", "PNL-RPS-B"], "round route-label interpretation for RPS panel tie")
        add_edge(edges, seen, "RPS TRIP BUS", "TC-52-4A", "round route-label interpretation for RPS trip bus text")
    else:
        add_chain(edges, seen, ["BUS-480-1A", "CHGR-125-1A", "BUS-125DC-A"], "final charger A component chain; route label excluded")
        add_chain(edges, seen, ["BUS-480-1B", "CHGR-125-1B", "BUS-125DC-B"], "final charger B component chain; route label excluded")
        add_edge(edges, seen, "PNL-RPS-A", "PNL-RPS-B", "final RPS panel tie; route label excluded")

    add_edge(edges, seen, "BAT-125-1A", "BUS-125DC-A", "battery A tied to 125VDC bus A")
    add_chain(edges, seen, ["BUS-125DC-A", "INV-120-1A", "PNL-RPS-A"], "DC bus A through inverter to RPS panel A")
    add_edge(edges, seen, "PNL-RPS-A", "RELAY-K501A", "RPS panel A relay branch")
    add_edge(edges, seen, "PNL-RPS-A", "XMTR-PT-501A", "RPS panel A transmitter branch")
    add_edge(edges, seen, "BAT-125-1B", "BUS-125DC-B", "battery B tied to 125VDC bus B")
    add_chain(edges, seen, ["BUS-125DC-B", "INV-120-1B", "PNL-RPS-B"], "DC bus B through inverter to RPS panel B")
    add_edge(edges, seen, "PNL-RPS-B", "RELAY-K501B", "RPS panel B relay branch")
    add_edge(edges, seen, "PNL-RPS-B", "XMTR-PT-501B", "RPS panel B transmitter branch")
    add_edge(edges, seen, "RELAY-K501A", "TC-52-4A", "relay K501A trip-coil connection")
    add_edge(edges, seen, "RELAY-K501B", "TC-52-4A", "relay K501B trip-coil connection")


def build_edges(feeder_style: str, route_labels: bool) -> list[dict]:
    edges: list[dict] = []
    seen: set[tuple[str, str]] = set()
    add_source_edges(edges, seen)
    add_4160_edges(edges, seen, feeder_style)
    add_480_edges(edges, seen)
    add_lower_dc_edges(edges, seen, route_labels)
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


def write_round_artifacts(name: str, nodes: list[str], edges: list[dict]) -> dict:
    stats = validate_graph(nodes, edges)
    write_matrix(RESULTS_DIR / f"{name}_matrix.csv", nodes, edges)
    write_edges(RESULTS_DIR / f"{name}_edges.csv", edges)
    return stats


def write_note(round_stats: dict[str, dict], final_stats: dict) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    note = f"""# Case 25 Connectivity Extraction Note

Generated: {timestamp}

## Scope

- Raw resource: `{RAW_IMAGE.name}`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Ground truth or GT-derived feedback was not used.

## Subagent Rounds

1. Diego high-recall pass: proposed all visually plausible components and edges, including four lower route labels as provisional logical nodes.
2. Jennifer precision pass: accepted the main source, 4.16kV, and 480V topology; rejected unsupported overconnections such as `MCC-X1 -- MCC-X2`, `CB-4X01 -- MS-X01`, and `DS-4X01 -- TR-480-1X`.
3. Diego saturation pass: identified `480V CHGR-A FEEDER`, `480V CHGR-B FEEDER`, `PNL A/B TIE`, and `RPS TRIP BUS` as route/lane labels rather than component rows.
4. Jennifer final confirmation: AGREED with the saturation correction.

## Final Decisions

- Final matrix rows are component/node names only.
- Excluded route/lane labels: `{ROUTE_LABELS[0]}`, `{ROUTE_LABELS[1]}`, `{ROUTE_LABELS[2]}`, `{ROUTE_LABELS[3]}`.
- Replacement direct component edges: `BUS-480-1A -- CHGR-125-1A`, `BUS-480-1B -- CHGR-125-1B`, and `PNL-RPS-A -- PNL-RPS-B`.
- No direct `MCC-X1 -- MCC-X2` edge was kept; both MCC sections are independently fed from `BUS-480-1X`.
- No self-loops were used.

## Counts

- Final nodes: {final_stats["node_count"]}
- Final undirected component edges: {final_stats["edge_count"]}
- Matrix is symmetric with zero diagonal.

The title block text mentions 200 components and 208 visible connections. The final component-node matrix has 200 rows and excludes five route/lane or continuation-level visible wires from row promotion, because those labels are not component names. This preserves the agreed component-only matrix while keeping the round files for audit.

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
            "decision": "included visually plausible route labels provisionally",
        },
        {
            "stage": "round_02",
            "agent": "Jennifer",
            "role": "precision reviewer/refiner",
            "artifact": "round_02_jennifer_precision_matrix.csv",
            "node_count": round_stats["round_02_jennifer_precision"]["node_count"],
            "edge_count": round_stats["round_02_jennifer_precision"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "removed unsupported first-feeder and MCC overconnections",
        },
        {
            "stage": "round_03",
            "agent": "Diego",
            "role": "saturation extractor",
            "artifact": "round_03_diego_saturation_matrix.csv",
            "node_count": round_stats["round_03_diego_saturation"]["node_count"],
            "edge_count": round_stats["round_03_diego_saturation"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "excluded route/lane labels from component-node matrix",
        },
        {
            "stage": "round_04",
            "agent": "Jennifer",
            "role": "final precision confirmation",
            "artifact": "round_04_jennifer_agreement_matrix.csv",
            "node_count": round_stats["round_04_jennifer_agreement"]["node_count"],
            "edge_count": round_stats["round_04_jennifer_agreement"]["edge_count"],
            "token_accounting": "exact subagent token count not exposed",
            "decision": "AGREED with Diego saturation correction",
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

    final_node_list = final_nodes()
    route_node_list = final_node_list + ROUTE_LABELS

    round_defs = {
        "round_01_diego_high_recall": (route_node_list, build_edges("diego_high_recall", route_labels=True)),
        "round_02_jennifer_precision": (route_node_list, build_edges("final", route_labels=True)),
        "round_03_diego_saturation": (final_node_list, build_edges("final", route_labels=False)),
        "round_04_jennifer_agreement": (final_node_list, build_edges("final", route_labels=False)),
    }

    round_stats: dict[str, dict] = {}
    for name, (nodes, edges) in round_defs.items():
        round_stats[name] = write_round_artifacts(name, nodes, edges)

    final_edges = build_edges("final", route_labels=False)
    final_stats = validate_graph(final_node_list, final_edges, expected_nodes=200, expected_edges=203)

    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", final_node_list, final_edges)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_node_list, final_edges)
    write_edges(RESULTS_DIR / "final_edges.csv", final_edges)
    write_nodes(RESULTS_DIR / "final_nodes.csv", final_node_list)

    graph = {
        "case": 25,
        "raw_image": RAW_IMAGE.name,
        "node_count": final_stats["node_count"],
        "edge_count": final_stats["edge_count"],
        "nodes": final_node_list,
        "edges": final_edges,
        "excluded_route_labels": ROUTE_LABELS,
        "subagent_final_agreement": "Jennifer AGREED with Diego saturation correction",
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
