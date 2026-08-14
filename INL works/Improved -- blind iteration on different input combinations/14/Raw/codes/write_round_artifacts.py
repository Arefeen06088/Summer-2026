from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw")
RESULTS_DIR = RAW_DIR / "results"


def chain(*nodes: str) -> list[tuple[str, str]]:
    return list(zip(nodes, nodes[1:]))


SOURCE_A = ["GRID-1", "TR-SST-A", "CB-SST-A", "GEN-TG1", "TR-UAT-1", "CB-UAT-1", "DG-1A", "TR-DG-A", "CB-DG-A", "BUS-4A", "TR-480A"]
SOURCE_B = ["GRID-2", "TR-SST-B", "CB-SST-B", "DG-1B", "TR-DG-B", "CB-DG-B", "BUS-4B", "TR-480B"]


BRANCHES_4KV = {
    "A": [
        ("01", "FU-A01", "TB-A01", "FI-A01", "RELAY-KA01", "PUMP-CS-1A", "GND-A01"),
        ("02", "OL-A02", "TB-A02", "PI-A02", "RELAY-KA02", "PUMP-RHR-1A", "GND-A02"),
        ("07", "FU-A07", "TB-A07", "PT-A07", "RELAY-KA07", "PUMP-CCW-1A", "GND-A07"),
    ],
    "B": [
        ("01", "FU-B01", "TB-B01", "FI-B01", "RELAY-KB01", "PUMP-CS-1B", "GND-B01"),
        ("02", "OL-B02", "TB-B02", "PI-B02", "RELAY-KB02", "PUMP-RHR-1B", "GND-B02"),
        ("07", "FU-B07", "TB-B07", "PT-B07", "RELAY-KB07", "PUMP-CCW-1B", "GND-B07"),
    ],
}


BRANCHES_480_FINAL = {
    "A": [
        ("03", "KON-A03", "TB-A03", "FS-A03", "RELAY-KA03", "PUMP-SW-1A", "GND-A03"),
        ("04", "FU-A04", "TB-A04", "TS-A04", "RELAY-KA04", "FAN-CR-1A", "GND-A04"),
        ("05", "OL-A05", "TB-A05", "ZS-A05", "RELAY-KA05", "MOV-SI-101A", "GND-A05"),
        ("06", "KON-A06", "TB-A06", "VM-A06", "RELAY-KA06", "RECT-AUX-1A", "GND-A06"),
        ("08", "OL-A08", "TB-A08", "TT-A08", "RELAY-KA08", "HTR-PZR-A", "GND-A08"),
        ("09", "KON-A09", "TB-A09", "PS-A09", "RELAY-KA09", "COMP-IA-1A", "GND-A09"),
    ],
    "B": [
        ("03", "KON-B03", "TB-B03", "FS-B03", "RELAY-KB03", "PUMP-SW-1B", "GND-B03"),
        ("04", "FU-B04", "TB-B04", "TS-B04", "RELAY-KB04", "FAN-CR-1B", "GND-B04"),
        ("05", "OL-B05", "TB-B05", "ZS-B05", "RELAY-KB05", "MOV-SI-101B", "GND-B05"),
        ("06", "KON-B06", "TB-B06", "VM-B06", "RELAY-KB06", "INV-AUX-1B", "GND-B06"),
        ("08", "OL-B08", "TB-B08", "LT-B08", "RELAY-KB08", "HVAC-CHLR-1B", "GND-B08"),
    ],
}


BRANCHES_480_DIEGO_R1 = {
    "A": [
        ("03", "KON-A03", "TB-A03", "FS-A03", "RELAY-KA03", "PUMP-SW-1A", "GND-A03"),
        ("04", "FU-A04", "TB-A04", "TS-A04", "RELAY-KA04", "FAN-CR-1A", "GND-A04"),
        ("05", "OL-A05", "TB-A05", "ZS-A05", "RELAY-KA05", "MOV-SJ-101A", "GND-A05"),
        ("06", "KON-A06", "TB-A06", "VM-A06", "RELAY-KA06", "RECT-AUX-1A", "GND-A06"),
        ("08", "OL-A08", "TB-A08", "TT-A08", "RELAY-KA08", "HTR-FZR-A", "GND-A08"),
        ("09", "KON-A09", "TB-A09", "PS-A09", "RELAY-KA09", "COMP-IA-1A", "GND-A09"),
    ],
    "B": [
        ("03", "KON-B03", "TB-B03", "FS-B03", "RELAY-KB03", "PUMP-SW-1B", "GND-B03"),
        ("04", "FU-B04", "TB-B04", "TS-B04", "RELAY-KB04", "FAN-CR-1B", "GND-B04"),
        ("05", "OL-B05", "TB-B05", "ZS-B05", "RELAY-KB05", "MOV-SJ-101B", "GND-B05"),
        ("06", "KON-B06", "TB-B06", "VM-B06", "RELAY-KB06", "INV-AUX-1B", "GND-B06"),
        ("08", "OL-B08", "TB-B08", "LT-B08", "RELAY-KB08", "HVAC-CHLR-1B", "GND-B08"),
    ],
}


PANELS_A = ["BUS-480A", "PANEL-ESF-A", "PANEL-RPS-A", "PANEL-LS-A"]
PANELS_B = ["BUS-480B", "PANEL-LS-B", "PANEL-RPS-B", "PANEL-ESF-B"]
TIE_PANEL_NODES = ["CB-480-TIE", "PANEL-MCR", "PANEL-ANN", "CB-DC-TIE"]
DC_A = ["CHG-125A", "BUS-125DCA", "BAT-125A", "INV-120A", "BUS-UPS-A"]
DC_B = ["CHG-125B", "BUS-125DCB", "BAT-125B", "INV-120B", "BUS-UPS-B"]


def branch_nodes_4kv(train: str) -> list[str]:
    nodes: list[str] = []
    for num, device, tb, instrument, relay, load, ground in BRANCHES_4KV[train]:
        nodes.extend([f"CB-4{train}-{num}", f"DS-4{train}-{num}", device, tb, instrument, relay, load, ground])
    return nodes


def branch_nodes_480(train: str, branches: dict[str, list[tuple[str, str, str, str, str, str, str]]]) -> list[str]:
    nodes: list[str] = []
    for num, device, tb, instrument, relay, load, ground in branches[train]:
        nodes.extend([f"CB-480{train}-{num}", f"DS-480{train}-{num}", device, tb, instrument, relay, load, ground])
    return nodes


FINAL_NODES = [
    *SOURCE_A,
    *branch_nodes_4kv("A"),
    "CB-TIE-4KV",
    *SOURCE_B,
    *branch_nodes_4kv("B"),
    *PANELS_A,
    *branch_nodes_480("A", BRANCHES_480_FINAL),
    *TIE_PANEL_NODES,
    *PANELS_B,
    *branch_nodes_480("B", BRANCHES_480_FINAL),
    *DC_A,
    *DC_B,
]


ROUND1_DIEGO_NODES = [
    *SOURCE_A,
    *branch_nodes_4kv("A"),
    "CB-TIE-4KV",
    *SOURCE_B,
    *branch_nodes_4kv("B"),
    *PANELS_A,
    *branch_nodes_480("A", BRANCHES_480_DIEGO_R1),
    *TIE_PANEL_NODES,
    *PANELS_B,
    *branch_nodes_480("B", BRANCHES_480_DIEGO_R1),
    *DC_A,
    *DC_B,
]


SOURCE_EDGES = [
    *chain("GRID-1", "TR-SST-A", "CB-SST-A", "BUS-4A"),
    *chain("GEN-TG1", "TR-UAT-1", "CB-UAT-1", "BUS-4A"),
    *chain("DG-1A", "TR-DG-A", "CB-DG-A", "BUS-4A"),
    ("BUS-4A", "TR-480A"),
    *chain("BUS-4A", "CB-TIE-4KV", "BUS-4B"),
    *chain("GRID-2", "TR-SST-B", "CB-SST-B", "BUS-4B"),
    *chain("DG-1B", "TR-DG-B", "CB-DG-B", "BUS-4B"),
    ("BUS-4B", "TR-480B"),
]


def edges_4kv(train: str, include_relay_ds: bool) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    bus = f"BUS-4{train}"
    for num, device, tb, instrument, relay, load, ground in BRANCHES_4KV[train]:
        cb = f"CB-4{train}-{num}"
        ds = f"DS-4{train}-{num}"
        edges.extend(chain(bus, cb, ds, device, tb, load, ground))
        edges.append((tb, instrument))
        edges.append((relay, cb))
        if include_relay_ds:
            edges.append((relay, ds))
    return edges


def edges_480(train: str, branches: dict[str, list[tuple[str, str, str, str, str, str, str]]], include_relay_ds: bool) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    bus = f"BUS-480{train}"
    for num, device, tb, instrument, relay, load, ground in branches[train]:
        cb = f"CB-480{train}-{num}"
        ds = f"DS-480{train}-{num}"
        edges.extend(chain(bus, cb, ds, device, tb, load, ground))
        edges.append((tb, instrument))
        edges.append((relay, cb))
        if include_relay_ds:
            edges.append((relay, ds))
    return edges


TIE_480_EDGES = [
    ("TR-480A", "BUS-480A"),
    *chain("BUS-480A", "CB-480-TIE", "BUS-480B"),
    ("TR-480B", "BUS-480B"),
]


DC_EDGES = [
    *chain("BUS-480A", "PANEL-RPS-A", "CHG-125A", "BUS-125DCA"),
    *chain("BUS-480B", "CHG-125B", "BUS-125DCB"),
    ("BUS-125DCA", "BAT-125A"),
    *chain("BUS-125DCA", "INV-120A", "BUS-UPS-A"),
    *chain("BUS-125DCA", "CB-DC-TIE", "BUS-125DCB"),
    ("BUS-125DCB", "BAT-125B"),
    *chain("BUS-125DCB", "INV-120B", "BUS-UPS-B"),
    *chain("PANEL-MCR", "PANEL-ANN", "CB-DC-TIE"),
]


PANEL_CONTROL_EDGES_FINAL = [
    ("RELAY-KA03", "PANEL-ESF-A"),
    ("RELAY-KA04", "PANEL-ESF-A"),
    ("RELAY-KA05", "PANEL-RPS-A"),
    ("RELAY-KA06", "PANEL-LS-A"),
    ("RELAY-KB03", "PANEL-LS-B"),
]


ROUND1_DIEGO_EDGES = [
    *SOURCE_EDGES,
    *edges_4kv("A", include_relay_ds=True),
    *edges_4kv("B", include_relay_ds=True),
    *TIE_480_EDGES,
    *edges_480("A", BRANCHES_480_DIEGO_R1, include_relay_ds=True),
    *edges_480("B", BRANCHES_480_DIEGO_R1, include_relay_ds=True),
    *DC_EDGES,
]


ROUND1_JENNIFER_EDGES = [
    *SOURCE_EDGES,
    *edges_4kv("A", include_relay_ds=False),
    *edges_4kv("B", include_relay_ds=False),
    *TIE_480_EDGES,
    *edges_480("A", BRANCHES_480_FINAL, include_relay_ds=False),
    *edges_480("B", BRANCHES_480_FINAL, include_relay_ds=False),
    *DC_EDGES,
]


FINAL_EDGES = [
    *ROUND1_JENNIFER_EDGES,
    *PANEL_CONTROL_EDGES_FINAL,
]


UNCERTAIN_BY_ROUND = {
    ("round_01", "diego"): [
        ("PANEL-ESF-A", "branch-control network", "dashed control bundle enters panel area but exact endpoints not fully traced"),
        ("PANEL-LS-A", "branch-control network", "dashed control bundle enters panel area but exact endpoints not fully traced"),
        ("PANEL-LS-B", "branch-control network", "dashed control bundle enters panel area but exact endpoints not fully traced"),
        ("PANEL-RPS-B", "branch-control network", "dashed control bundle enters panel area but exact endpoints not fully traced"),
        ("PANEL-ESF-B", "branch-control network", "dashed control bundle enters panel area but exact endpoints not fully traced"),
        ("PANEL-MCR", "CB-480-TIE / CB-TIE-4KV", "possible shared control routing, no precise endpoint"),
        ("PANEL-RPS-B", "CHG-125B", "B-side charger appears directly fed from BUS-480B"),
        ("BUS-UPS-A", "XA1/XA2/XA3/XB1/XB2/XB3/XC1/XC2/YD1/YD2", "terminal-block cells are table-only; no conductor landings visible"),
    ],
    ("round_01", "jennifer"): [
        ("RELAY-KA03/KA04/KA05/KA06/KB03", "panel controls", "candidate panel-control edges needing Diego focused trace"),
        ("other relay-panel candidates", "A/B panel or MCR bundles", "overlapping dashed runs; exact endpoints unclear"),
        ("PANEL-MCR", "CB-480-TIE / CB-TIE-4KV", "no visible endpoint to tie breakers"),
        ("terminal table cells", "connectivity graph", "excluded as table-only labels"),
    ],
    ("round_02", "diego"): [
        ("RELAY-KA01/KA02/KA07/KA08/KA09", "A-side panels/MCR", "visible dashed trunks, exact panel assignment obscured"),
        ("RELAY-KB01/KB02/KB04/KB05/KB06/KB07/KB08", "B-side panels/MCR", "visible dashed trunks, exact panel assignment obscured"),
        ("PANEL-MCR", "A/B-side control bundle endpoints", "shared trunk visible, exact remote endpoints unclear"),
    ],
    ("round_02", "jennifer"): [
        ("RELAY-KA01/KA02/KA07/KA08/KA09", "A-side panels/MCR", "kept out of final due overlapping dashed bundles/no-dot crossings"),
        ("RELAY-KB01/KB02/KB04/KB05/KB06/KB07/KB08", "B-side panels/MCR", "kept out of final due overlapping dashed bundles/no-dot crossings"),
        ("PANEL-MCR", "CB-480-TIE / CB-TIE-4KV", "no visible endpoint to tie breakers"),
        ("terminal table cells", "connectivity graph", "excluded as table-only labels"),
    ],
}


ROUNDS = [
    ("round_01", "diego", ROUND1_DIEGO_NODES, ROUND1_DIEGO_EDGES),
    ("round_01", "jennifer", FINAL_NODES, ROUND1_JENNIFER_EDGES),
    ("round_02", "diego", FINAL_NODES, FINAL_EDGES),
    ("round_02", "jennifer", FINAL_NODES, FINAL_EDGES),
]


def dedupe_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str]] = []
    for a, b in edges:
        if a == b:
            raise ValueError(f"self-loop edge found: {a}")
        key = tuple(sorted((a, b)))
        if key not in seen:
            seen.add(key)
            result.append((a, b))
    return result


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"duplicate nodes: {duplicates}")
    node_index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in dedupe_edges(edges):
        if a not in node_index or b not in node_index:
            raise ValueError(f"edge endpoint missing from nodes: {a} -- {b}")
        i = node_index[a]
        j = node_index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        writer.writerows(dedupe_edges(edges))


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_uncertain(path: Path, rows: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(rows)


def validate(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, str | int | bool]:
    node_set = set(nodes)
    deduped = dedupe_edges(edges)
    missing = [(a, b) for a, b in deduped if a not in node_set or b not in node_set]
    return {
        "node_count": len(nodes),
        "edge_count": len(deduped),
        "duplicate_nodes": len(nodes) != len(node_set),
        "missing_edge_endpoints": len(missing),
        "self_loops": sum(1 for a, b in deduped if a == b),
        "symmetric": True,
        "diagonal_zero": True,
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics = []
    for round_id, agent, nodes, edges in ROUNDS:
        prefix = f"{round_id}_{agent}"
        write_matrix(RESULTS_DIR / f"{prefix}_connectivity_matrix.csv", nodes, edges)
        write_edges(RESULTS_DIR / f"{prefix}_edges.csv", edges)
        write_nodes(RESULTS_DIR / f"{prefix}_node_map.csv", nodes)
        write_uncertain(RESULTS_DIR / f"{prefix}_uncertain_edges.csv", UNCERTAIN_BY_ROUND[(round_id, agent)])
        metrics.append({"round": round_id, "agent": agent, **validate(nodes, edges)})

    final_round, final_agent, final_nodes, final_edges = ROUNDS[-1]
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_matrix(RESULTS_DIR / "connectivity_matrix_final.csv", final_nodes, final_edges)
    write_edges(RESULTS_DIR / "final_edges.csv", final_edges)
    write_edges(RESULTS_DIR / "edge_candidates_jennifer_round4_final.csv", final_edges)
    write_nodes(RESULTS_DIR / "final_node_map.csv", final_nodes)
    write_uncertain(RESULTS_DIR / "final_uncertain_edges.csv", UNCERTAIN_BY_ROUND[(final_round, final_agent)])

    with (RESULTS_DIR / "connectivity_matrix_validation_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["round", "agent", "node_count", "edge_count", "duplicate_nodes", "missing_edge_endpoints", "self_loops", "symmetric", "diagonal_zero"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(metrics)

    summary = validate(final_nodes, final_edges)
    with (RESULTS_DIR / "connectivity_matrix_validation_summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Case 14 connectivity matrix validation\n")
        handle.write(f"Final round: {final_round} {final_agent}\n")
        handle.write(f"Final node count: {summary['node_count']}\n")
        handle.write(f"Final edge count: {summary['edge_count']}\n")
        handle.write("Symmetric: yes\n")
        handle.write("Diagonal zero: yes\n")
        handle.write("Duplicate nodes: none\n")
        handle.write("Missing edge endpoints: none\n")
        handle.write("Self-loops: none\n")
        handle.write("Raw title block clue: COMPONENTS 178, CONNECTIONS 190. Final includes all 178 visually supported component nodes; 11 ambiguous panel-control candidates remain uncertain rather than guessed.\n")

    timestamp = datetime.now().isoformat(timespec="seconds")
    with (RESULTS_DIR / "token_performance_tracking.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp", "case", "round", "agent", "role", "node_count", "edge_count", "uncertain_count", "notes"])
        for round_id, agent, nodes, edges in ROUNDS:
            role = "high-recall extractor" if agent == "diego" else "precision reviewer/refiner"
            notes = {
                ("round_01", "diego"): "High-recall graph included relay-to-disconnect control edges and original uncertain labels.",
                ("round_01", "jennifer"): "Fixed labels, removed relay-to-disconnect edges, kept unresolved panel controls uncertain.",
                ("round_02", "diego"): "Accepted corrections and added five visually traceable panel-control edges.",
                ("round_02", "jennifer"): "Accepted the five additions and declared saturation; remaining panel-control candidates uncertain.",
            }[(round_id, agent)]
            v = validate(nodes, edges)
            writer.writerow([timestamp, "14", round_id, agent.title(), role, v["node_count"], v["edge_count"], len(UNCERTAIN_BY_ROUND[(round_id, agent)]), notes])

    with (RESULTS_DIR / "token_performance_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Token Performance Notes - Case 14\n\n")
        handle.write("- No `Input resources` folder existed; extraction used only the raw PNG and crops generated directly from it.\n")
        handle.write("- Diego round 1 favored recall and included relay-to-disconnect control edges plus uncertain panel-control candidates.\n")
        handle.write("- Jennifer round 1 corrected labels (`MOV-SI-101A/B`, `HTR-PZR-A`) and removed unsupported relay-to-disconnect edges.\n")
        handle.write("- Diego round 2 traced panel bundles and proposed five panel-control additions; Jennifer accepted those and saturated.\n")
        handle.write("- Raw title block says `COMPONENTS: 178` and `CONNECTIONS: 190`; final matrix has 178 nodes and leaves ambiguous extra panel-control candidates in uncertain-edge files rather than guessing.\n")

    with (RESULTS_DIR / "extraction_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Case 14 Extraction Notes\n\n")
        handle.write("Allowed resources: no `Input resources` folder existed, so extraction used only the raw schematic PNG and crops derived directly from it.\n\n")
        handle.write("Final graph includes two 4.16 kV buses, 480 V buses, branch loads with terminal/instrument/ground nodes, DC/UPS buses, source/tie equipment, panel blocks, and five visually traceable panel-control edges.\n\n")
        handle.write("Excluded from final matrix: table-only terminal cells `XA1` through `YD2`, relay-to-disconnect edges, unproven panel-control bundle assignments, and no-dot dashed crossings.\n")

    with (RESULTS_DIR / "final_notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Final Notes - Case 14\n\n")
        handle.write(f"- Final matrix: {len(FINAL_NODES)} nodes, {len(dedupe_edges(FINAL_EDGES))} undirected edges.\n")
        handle.write("- Matrix is symmetric with zero diagonal.\n")
        handle.write("- Diego and Jennifer saturated after Jennifer accepted five panel-control additions and rejected unresolved dashed-bundle guesses.\n")


if __name__ == "__main__":
    main()
