import csv
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


SOURCE_NODES = [
    "GRID-1",
    "TR-SST-A",
    "CB-SST-A",
    "GEN-TG1",
    "TR-UAT-1",
    "CB-UAT-1",
    "DG-1A",
    "TR-DG-A",
    "CB-DG-A",
    "BUS-4A",
    "CB-TIE-4KV",
    "GRID-2",
    "TR-SST-B",
    "CB-SST-B",
    "DG-1B",
    "TR-DG-B",
    "CB-DG-B",
    "BUS-4B",
    "TR-480A",
    "BUS-480A",
    "CB-480-TIE",
    "TR-480B",
    "BUS-480B",
]

PANEL_NODES = [
    "PANEL-ESF-A",
    "PANEL-RPS-A",
    "PANEL-LS-A",
    "PANEL-MCR",
    "PANEL-ANN",
    "PANEL-LS-B",
    "PANEL-RPS-B",
    "PANEL-ESF-B",
]

DC_NODES = [
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "BUS-125DCA",
    "BUS-UPS-A",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "BUS-125DCB",
    "BUS-UPS-B",
    "CB-DC-TIE",
]

BRANCHES = [
    {
        "bus": "BUS-4A",
        "cb": "CB-4A-01",
        "ds": "DS-4A-01",
        "device": "FU-A01",
        "tb": "TB-A01",
        "load": "PUMP-CS-1A",
        "gnd": "GND-A01",
        "instrument": "FI-A01",
        "relay": "RELAY-KA01",
    },
    {
        "bus": "BUS-4A",
        "cb": "CB-4A-02",
        "ds": "DS-4A-02",
        "device": "OL-A02",
        "tb": "TB-A02",
        "load": "PUMP-RHR-1A",
        "gnd": "GND-A02",
        "instrument": "PI-A02",
        "relay": "RELAY-KA02",
    },
    {
        "bus": "BUS-4A",
        "cb": "CB-4A-07",
        "ds": "DS-4A-07",
        "device": "FU-A07",
        "tb": "TB-A07",
        "load": "PUMP-CCW-1A",
        "gnd": "GND-A07",
        "instrument": "PT-A07",
        "relay": "RELAY-KA07",
    },
    {
        "bus": "BUS-4B",
        "cb": "CB-4B-01",
        "ds": "DS-4B-01",
        "device": "FU-B01",
        "tb": "TB-B01",
        "load": "PUMP-CS-1B",
        "gnd": "GND-B01",
        "instrument": "FI-B01",
        "relay": "RELAY-KB01",
    },
    {
        "bus": "BUS-4B",
        "cb": "CB-4B-02",
        "ds": "DS-4B-02",
        "device": "OL-B02",
        "tb": "TB-B02",
        "load": "PUMP-RHR-1B",
        "gnd": "GND-B02",
        "instrument": "PI-B02",
        "relay": "RELAY-KB02",
    },
    {
        "bus": "BUS-4B",
        "cb": "CB-4B-07",
        "ds": "DS-4B-07",
        "device": "FU-B07",
        "tb": "TB-B07",
        "load": "PUMP-CCW-1B",
        "gnd": "GND-B07",
        "instrument": "PT-B07",
        "relay": "RELAY-KB07",
    },
    {
        "bus": "BUS-480A",
        "cb": "CB-48A-03",
        "ds": "DS-48A-03",
        "device": "KON-A03",
        "tb": "TB-A03",
        "load": "PUMP-SW-1A",
        "gnd": "GND-A03",
        "instrument": "FS-A03",
        "relay": "RELAY-KA03",
        "diego_cb": "CB-480A-03",
        "diego_ds": "DS-480A-03",
    },
    {
        "bus": "BUS-480A",
        "cb": "CB-48A-04",
        "ds": "DS-48A-04",
        "device": "FU-A04",
        "tb": "TB-A04",
        "load": "FAN-CR-1A",
        "gnd": "GND-A04",
        "instrument": "TS-A04",
        "relay": "RELAY-KA04",
        "diego_cb": "CB-480A-04",
        "diego_ds": "DS-480A-04",
    },
    {
        "bus": "BUS-480A",
        "cb": "CB-48A-05",
        "ds": "DS-48A-05",
        "device": "OL-A05",
        "tb": "TB-A05",
        "load": "MOV-SI-101A",
        "gnd": "GND-A05",
        "instrument": "ZS-A05",
        "relay": "RELAY-KA05",
        "diego_cb": "CB-480A-05",
        "diego_ds": "DS-480A-05",
    },
    {
        "bus": "BUS-480A",
        "cb": "CB-48A-06",
        "ds": "DS-48A-06",
        "device": "KON-A06",
        "tb": "TB-A06",
        "load": "RECT-AUX-1A",
        "gnd": "GND-A06",
        "instrument": "VM-A06",
        "relay": "RELAY-KA06",
        "diego_cb": "CB-480A-06",
        "diego_ds": "DS-480A-06",
    },
    {
        "bus": "BUS-480A",
        "cb": "CB-48A-08",
        "ds": "DS-48A-08",
        "device": "OL-A08",
        "tb": "TB-A08",
        "load": "HTR-PZR-A",
        "gnd": "GND-A08",
        "instrument": "TT-A08",
        "relay": "RELAY-KA08",
        "diego_cb": "CB-480A-08",
        "diego_ds": "DS-480A-08",
    },
    {
        "bus": "BUS-480A",
        "cb": "CB-48A-09",
        "ds": "DS-48A-09",
        "device": "KON-A09",
        "tb": "TB-A09",
        "load": "COMP-IA-1A",
        "gnd": "GND-A09",
        "instrument": "PS-A09",
        "relay": "RELAY-KA09",
        "diego_cb": "CB-480A-09",
        "diego_ds": "DS-480A-09",
        "diego_load": "COMP-ITA-1A",
    },
    {
        "bus": "BUS-480B",
        "cb": "CB-48B-03",
        "ds": "DS-48B-03",
        "device": "KON-B03",
        "tb": "TB-B03",
        "load": "PUMP-SW-1B",
        "gnd": "GND-B03",
        "instrument": "FS-B03",
        "relay": "RELAY-KB03",
        "diego_cb": "CB-480B-03",
        "diego_ds": "DS-480B-03",
    },
    {
        "bus": "BUS-480B",
        "cb": "CB-48B-04",
        "ds": "DS-48B-04",
        "device": "FU-B04",
        "tb": "TB-B04",
        "load": "FAN-CR-1B",
        "gnd": "GND-B04",
        "instrument": "TS-B04",
        "relay": "RELAY-KB04",
        "diego_cb": "CB-480B-04",
        "diego_ds": "DS-480B-04",
    },
    {
        "bus": "BUS-480B",
        "cb": "CB-48B-05",
        "ds": "DS-48B-05",
        "device": "OL-B05",
        "tb": "TB-B05",
        "load": "MOV-SI-101B",
        "gnd": "GND-B05",
        "instrument": "ZS-B05",
        "relay": "RELAY-KB05",
        "diego_cb": "CB-480B-05",
        "diego_ds": "DS-480B-05",
    },
    {
        "bus": "BUS-480B",
        "cb": "CB-48B-06",
        "ds": "DS-48B-06",
        "device": "KON-B06",
        "tb": "TB-B06",
        "load": "INV-AUX-1B",
        "gnd": "GND-B06",
        "instrument": "VM-B06",
        "relay": "RELAY-KB06",
        "diego_cb": "CB-480B-06",
        "diego_ds": "DS-480B-06",
    },
    {
        "bus": "BUS-480B",
        "cb": "CB-48B-08",
        "ds": "DS-48B-08",
        "device": "OL-B08",
        "tb": "TB-B08",
        "load": "HVAC-CHLR-1B",
        "gnd": "GND-B08",
        "instrument": "LT-B08",
        "relay": "RELAY-KB08",
        "diego_cb": "CB-480B-08",
        "diego_ds": "DS-480B-08",
    },
]

MASTER_TB_NODES = [
    "MASTER-TB-XA1",
    "MASTER-TB-XA2",
    "MASTER-TB-XA3",
    "MASTER-TB-XB1",
    "MASTER-TB-XB2",
    "MASTER-TB-XB3",
    "MASTER-TB-XC1",
    "MASTER-TB-XC2",
    "MASTER-TB-YD1",
    "MASTER-TB-YD2",
]

CTRL_NODES = [
    "CTRL-A-4KV-HDR",
    "CTRL-A-480-HDR",
    "CTRL-B-4KV-HDR",
    "CTRL-B-480-HDR",
    "CTRL-CENTER-MCR-ANN",
]


def unique(items):
    seen = set()
    output = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def edge(a, b, edge_type, evidence):
    return (a, b, edge_type, evidence)


def branch_nodes(branch, diego=False):
    cb = branch.get("diego_cb", branch["cb"]) if diego else branch["cb"]
    ds = branch.get("diego_ds", branch["ds"]) if diego else branch["ds"]
    load = branch.get("diego_load", branch["load"]) if diego else branch["load"]
    return [
        cb,
        ds,
        branch["device"],
        branch["tb"],
        load,
        branch["gnd"],
        branch["instrument"],
        branch["relay"],
    ]


def final_nodes():
    nodes = SOURCE_NODES + PANEL_NODES + DC_NODES
    for branch in BRANCHES:
        nodes.extend(branch_nodes(branch, diego=False))
    return unique(nodes)


def diego_round1_nodes():
    nodes = SOURCE_NODES + PANEL_NODES + DC_NODES
    for branch in BRANCHES:
        nodes.extend(branch_nodes(branch, diego=True))
    nodes.extend(MASTER_TB_NODES)
    nodes.extend(CTRL_NODES)
    return unique(nodes)


def source_edges():
    return [
        edge("GRID-1", "TR-SST-A", "power", "high"),
        edge("TR-SST-A", "CB-SST-A", "power", "high"),
        edge("CB-SST-A", "BUS-4A", "power", "high"),
        edge("GEN-TG1", "TR-UAT-1", "power", "high"),
        edge("TR-UAT-1", "CB-UAT-1", "power", "high"),
        edge("CB-UAT-1", "BUS-4A", "power", "high"),
        edge("DG-1A", "TR-DG-A", "power", "high"),
        edge("TR-DG-A", "CB-DG-A", "power", "high"),
        edge("CB-DG-A", "BUS-4A", "power", "high"),
        edge("BUS-4A", "CB-TIE-4KV", "power", "high"),
        edge("CB-TIE-4KV", "BUS-4B", "power", "high"),
        edge("GRID-2", "TR-SST-B", "power", "high"),
        edge("TR-SST-B", "CB-SST-B", "power", "high"),
        edge("CB-SST-B", "BUS-4B", "power", "high"),
        edge("DG-1B", "TR-DG-B", "power", "high"),
        edge("TR-DG-B", "CB-DG-B", "power", "high"),
        edge("CB-DG-B", "BUS-4B", "power", "high"),
        edge("BUS-4A", "TR-480A", "power", "high"),
        edge("TR-480A", "BUS-480A", "power", "high"),
        edge("BUS-4B", "TR-480B", "power", "high"),
        edge("TR-480B", "BUS-480B", "power", "high"),
        edge("BUS-480A", "CB-480-TIE", "power", "high"),
        edge("CB-480-TIE", "BUS-480B", "power", "high"),
        edge("BUS-125DCA", "CB-DC-TIE", "power", "high"),
        edge("CB-DC-TIE", "BUS-125DCB", "power", "high"),
        edge("BUS-480A", "PANEL-RPS-A", "power", "high"),
        edge("PANEL-RPS-A", "CHG-125A", "power", "high"),
        edge("CHG-125A", "BUS-125DCA", "power", "high"),
        edge("BUS-125DCA", "BAT-125A", "power", "high"),
        edge("BUS-125DCA", "INV-120A", "power", "high"),
        edge("INV-120A", "BUS-UPS-A", "power", "high"),
        edge("BUS-480B", "CHG-125B", "power", "high"),
        edge("CHG-125B", "BUS-125DCB", "power", "high"),
        edge("BUS-125DCB", "BAT-125B", "power", "high"),
        edge("BUS-125DCB", "INV-120B", "power", "high"),
        edge("INV-120B", "BUS-UPS-B", "power", "high"),
        edge("PANEL-MCR", "PANEL-ANN", "control", "high"),
        edge("PANEL-ANN", "CB-DC-TIE", "control", "high"),
    ]


def branch_edges(diego=False):
    edges = []
    for branch in BRANCHES:
        cb = branch.get("diego_cb", branch["cb"]) if diego else branch["cb"]
        ds = branch.get("diego_ds", branch["ds"]) if diego else branch["ds"]
        load = branch.get("diego_load", branch["load"]) if diego else branch["load"]
        edges.extend(
            [
                edge(branch["bus"], cb, "power", "high"),
                edge(cb, ds, "power", "high"),
                edge(ds, branch["device"], "power", "high"),
                edge(branch["device"], branch["tb"], "power", "high"),
                edge(branch["tb"], load, "power", "high"),
                edge(load, branch["gnd"], "ground", "high"),
                edge(branch["tb"], branch["instrument"], "instrument", "high"),
                edge(branch["relay"], cb, "control", "high"),
            ]
        )
    return edges


def final_edges():
    return source_edges() + branch_edges(diego=False)


def diego_round1_edges():
    edges = source_edges() + branch_edges(diego=True)
    for relay in ["RELAY-KA01", "RELAY-KA02", "RELAY-KA07"]:
        edges.append(edge(relay, "CTRL-A-4KV-HDR", "control", "diego_high_recall_pseudo_header"))
    edges.append(edge("CTRL-A-4KV-HDR", "CTRL-A-480-HDR", "control", "diego_high_recall_pseudo_header"))
    for relay in ["RELAY-KB01", "RELAY-KB02", "RELAY-KB07"]:
        edges.append(edge(relay, "CTRL-B-4KV-HDR", "control", "diego_high_recall_pseudo_header"))
    edges.append(edge("CTRL-B-4KV-HDR", "CTRL-B-480-HDR", "control", "diego_high_recall_pseudo_header"))
    for relay in ["RELAY-KA03", "RELAY-KA04", "RELAY-KA05", "RELAY-KA06", "RELAY-KA08", "RELAY-KA09"]:
        edges.append(edge(relay, "CTRL-A-480-HDR", "control", "diego_high_recall_pseudo_header"))
    for panel in ["PANEL-ESF-A", "PANEL-RPS-A", "PANEL-LS-A"]:
        edges.append(edge("CTRL-A-480-HDR", panel, "control", "diego_high_recall_pseudo_header"))
    for relay in ["RELAY-KB03", "RELAY-KB04", "RELAY-KB05", "RELAY-KB06", "RELAY-KB08"]:
        edges.append(edge(relay, "CTRL-B-480-HDR", "control", "diego_high_recall_pseudo_header"))
    for panel in ["PANEL-LS-B", "PANEL-RPS-B", "PANEL-ESF-B"]:
        edges.append(edge("CTRL-B-480-HDR", panel, "control", "diego_high_recall_pseudo_header"))
    edges.extend(
        [
            edge("PANEL-MCR", "CTRL-CENTER-MCR-ANN", "control", "diego_high_recall_pseudo_header"),
            edge("PANEL-ANN", "CTRL-CENTER-MCR-ANN", "control", "diego_high_recall_pseudo_header"),
            edge("CTRL-CENTER-MCR-ANN", "CTRL-A-480-HDR", "control", "diego_high_recall_pseudo_header"),
            edge("CTRL-CENTER-MCR-ANN", "CTRL-B-480-HDR", "control", "diego_high_recall_pseudo_header"),
        ]
    )
    return edges


UNCERTAIN_EXCLUDED = [
    ("CTRL-A-4KV-HDR", "removed: artificial high-recall pseudo node, not a labeled component/logical node"),
    ("CTRL-A-480-HDR", "removed: artificial high-recall pseudo node, not a labeled component/logical node"),
    ("CTRL-B-4KV-HDR", "removed: artificial high-recall pseudo node, not a labeled component/logical node"),
    ("CTRL-B-480-HDR", "removed: artificial high-recall pseudo node, not a labeled component/logical node"),
    ("CTRL-CENTER-MCR-ANN", "removed: artificial high-recall pseudo node, not a labeled component/logical node"),
    ("MASTER-TB-XA1..MASTER-TB-YD2", "terminal strip visible but no clear individual conductor landings"),
    ("relay-to-ESF/RPS/LS/MCR panel mesh", "dashed bundles visible but exact landings/branch assignments ambiguous"),
    ("panel-to-panel edges among ESF/RPS/LS panels", "shared dashed bundle runs without clean direct panel-to-panel terminals"),
    ("CB-480-TIE to PANEL-MCR/PANEL-ANN", "no clear dashed control lead from the 480 V tie breaker"),
]


ROUNDS = [
    ("round_01_diego_high_recall", diego_round1_nodes, diego_round1_edges),
    ("round_02_jennifer_precision", final_nodes, final_edges),
    ("round_03_diego_saturation", final_nodes, final_edges),
]


def validate(nodes, edges):
    node_set = set(nodes)
    missing = sorted({n for a, b, _, _ in edges for n in (a, b) if n not in node_set})
    if missing:
        raise ValueError(f"Missing nodes referenced by edges: {missing}")
    seen = set()
    duplicates = []
    for a, b, _, _ in edges:
        if a == b:
            raise ValueError(f"Self-loop found: {a}")
        key = tuple(sorted((a, b)))
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    if duplicates:
        raise ValueError(f"Duplicate undirected edges: {duplicates}")


def write_node_order(path, nodes):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type", "evidence_conf"])
        writer.writerows(edges)


def write_matrix(path, nodes, edges):
    positions = {node: index for index, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b, _, _ in edges:
        i = positions[a]
        j = positions[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_uncertain():
    with (RESULTS / "uncertain_excluded_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["edge_or_node", "reason"])
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_round_notes():
    text = """# Document 14 round notes

## Round 1 - Diego high recall
Diego extracted the physical source, bus, branch, panel, DC/UPS, instrument, relay, load, and ground graph.
He also included artificial CTRL-* header nodes to preserve lower dashed control-bundle possibilities and used expanded CB-480A/B branch labels.

## Round 2 - Jennifer precision
Jennifer removed artificial CTRL-* nodes, removed MASTER-TB-XA1..YD2 because no individual terminal landings are clear,
pruned the implied relay-to-panel mesh through ambiguous dashed bundles, corrected 480 V breaker labels to CB-48A/B-*,
and corrected COMP-ITA-1A to COMP-IA-1A.

## Round 3 - Diego saturation
Diego agreed Jennifer's corrected graph was saturated. Final matrix equals round 2.
"""
    (RESULTS / "round_notes.md").write_text(text, encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    for prefix, nodes_fn, edges_fn in ROUNDS:
        nodes = nodes_fn()
        edges = edges_fn()
        validate(nodes, edges)
        write_node_order(RESULTS / f"{prefix}_node_order.csv", nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", nodes, edges)

    nodes = final_nodes()
    edges = final_edges()
    validate(nodes, edges)
    write_node_order(RESULTS / "final_node_order.csv", nodes)
    write_edges(RESULTS / "final_edges.csv", edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, edges)
    write_uncertain()
    write_round_notes()
    print(f"Final nodes: {len(nodes)}")
    print(f"Final edges: {len(edges)}")
    print(RESULTS)


if __name__ == "__main__":
    main()
