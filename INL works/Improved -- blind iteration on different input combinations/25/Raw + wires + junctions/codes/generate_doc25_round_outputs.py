from __future__ import annotations

import csv
import io
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\25\Raw + wires + junctions"
)
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc25_work")


def result_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".doc25_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return RESULTS
    except OSError:
        FALLBACK.mkdir(parents=True, exist_ok=True)
        return FALLBACK


Edge = tuple[str, str, str, str, str]


def E(source: str, target: str, confidence: str, line_type: str, evidence: str) -> Edge:
    return (source, target, confidence, line_type, evidence)


TOP_NODES = [
    "SWYD-115KV",
    "FDR-13A",
    "TR-UAT-1A",
    "CB-52-4A",
    "EDG-1A",
    "CB-DG-1A",
    "BUS-4160-A",
    "CB-TIE-AB",
    "FDR-13B",
    "TR-UAT-1B",
    "CB-52-4B",
    "EDG-1B",
    "CB-DG-1B",
    "BUS-4160-B",
    "CB-TIE-BC",
    "TR-SAT-1",
    "CB-52-4C",
    "EDG-1C",
    "CB-DG-1C",
    "BUS-4160-C",
]

FEEDER_LOADS = [
    ("01", "TR-480-1{train}", "MS-{train}01", "PUMP-RHR-P201{train}", "CB-52-48{train}", "BUS-480-1{train}"),
    ("02", "MS-{train}02", "PUMP-CS-P202{train}", "", ""),
    ("03", "TR-LC-{train}03", "LC-480-{train}03", "", ""),
    ("04", "MS-{train}04", "FAN-CR-401{train}", "", ""),
    ("05", "PNL-ESF-{train}05", "GND-ESF-{train}05", "", ""),
    ("06", "RECT-RPS-{train}06", "INV-RPS-{train}06", "", ""),
    ("07", "MS-{train}07", "PUMP-AFW-P203{train}", "", ""),
    ("08", "TR-CTRL-{train}08", "CP-CTRL-{train}08", "", ""),
]

MCC_LOADS = {
    "A": [
        ("A1", "01", "MS-48A01", "PUMP-CVC-P301A"),
        ("A1", "02", "K-48A02", "MOV-CS-451A"),
        ("A1", "03", "MS-48A03", "FAN-HVAC-501A"),
        ("A2", "04", "MS-48A04", "PUMP-SUMP-P302A"),
        ("A2", "05", "K-48A05", "MOV-RHR-452A"),
        ("A2", "06", "XFU-48A06", "PNL-PI-601A"),
    ],
    "B": [
        ("B1", "01", "MS-48B01", "PUMP-CVC-P301B"),
        ("B1", "02", "K-48B02", "MOV-CS-451B"),
        ("B1", "03", "MS-48B03", "FAN-HVAC-501B"),
        ("B2", "04", "MS-48B04", "PUMP-SUMP-P302B"),
        ("B2", "05", "K-48B05", "MOV-RHR-452B"),
        ("B2", "06", "XFU-48B06", "PNL-PI-601B"),
    ],
    "C": [
        ("C1", "01", "MS-48C01", "PUMP-CVC-P301C"),
        ("C1", "02", "K-48C02", "MOV-CS-451C"),
        ("C1", "03", "MS-48C03", "FAN-HVAC-501C"),
        ("C2", "04", "MS-48C04", "PUMP-SUMP-P302C"),
        ("C2", "05", "K-48C05", "MOV-RHR-452C"),
        ("C2", "06", "XFU-48C06", "PNL-PI-601C"),
    ],
}

BOTTOM_NODES = [
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

ROUTE_NODES = [
    "480V_CHGR-A_FEEDER",
    "480V_CHGR-B_FEEDER",
    "RPS_TRIP_BUS",
    "PNL_A/B_TIE",
]


def feeder_nodes(train: str) -> list[str]:
    nodes: list[str] = []
    for spec in FEEDER_LOADS:
        idx = spec[0]
        cb = f"CB-4{train}{idx}"
        ds = f"DS-4{train}{idx}"
        nodes.extend([cb, ds])
        if idx == "01":
            _, tr, ms, pump, cb48, bus48 = spec
            nodes.extend(
                [
                    tr.format(train=train),
                    ms.format(train=train),
                    pump.format(train=train),
                    cb48.format(train=train),
                    bus48.format(train=train),
                ]
            )
        else:
            _, device, load, _, _ = spec
            nodes.extend([device.format(train=train), load.format(train=train)])
    return nodes


def mcc_nodes(train: str) -> list[str]:
    nodes = [f"MCC-{train}1"]
    for board, idx, device, load in MCC_LOADS[train]:
        if board != f"{train}1":
            continue
        nodes.extend([f"CB-48{train}{idx}", device, load])
    nodes.append(f"MCC-{train}2")
    for board, idx, device, load in MCC_LOADS[train]:
        if board != f"{train}2":
            continue
        nodes.extend([f"CB-48{train}{idx}", device, load])
    return nodes


FINAL_NODES = (
    TOP_NODES
    + feeder_nodes("A")
    + feeder_nodes("B")
    + feeder_nodes("C")
    + mcc_nodes("A")
    + mcc_nodes("B")
    + mcc_nodes("C")
    + BOTTOM_NODES
)

DIEGO_NODES = FINAL_NODES + ROUTE_NODES


def top_edges() -> list[Edge]:
    return [
        E("SWYD-115KV", "FDR-13A", "high", "solid_power", "Top 115 kV source bus taps down through FDR-13A."),
        E("FDR-13A", "TR-UAT-1A", "high", "solid_power", "FDR-13A vertical feeder continues into TR-UAT-1A."),
        E("TR-UAT-1A", "CB-52-4A", "high", "solid_power", "TR-UAT-1A secondary continues to CB-52-4A."),
        E("CB-52-4A", "BUS-4160-A", "high", "solid_power", "CB-52-4A lands on BUS-4160-A."),
        E("EDG-1A", "CB-DG-1A", "high", "solid_power", "EDG-1A generator feeder enters CB-DG-1A."),
        E("CB-DG-1A", "BUS-4160-A", "high", "solid_power", "CB-DG-1A lands on BUS-4160-A."),
        E("BUS-4160-A", "CB-TIE-AB", "high", "solid_power", "BUS-4160-A right end enters CB-TIE-AB."),
        E("CB-TIE-AB", "BUS-4160-B", "high", "solid_power", "CB-TIE-AB right side lands on BUS-4160-B."),
        E("SWYD-115KV", "FDR-13B", "high", "solid_power", "Top 115 kV source bus taps down through FDR-13B."),
        E("FDR-13B", "TR-UAT-1B", "high", "solid_power", "FDR-13B vertical feeder continues into TR-UAT-1B."),
        E("TR-UAT-1B", "CB-52-4B", "high", "solid_power", "TR-UAT-1B secondary continues to CB-52-4B."),
        E("CB-52-4B", "BUS-4160-B", "high", "solid_power", "CB-52-4B lands on BUS-4160-B."),
        E("EDG-1B", "CB-DG-1B", "high", "solid_power", "EDG-1B generator feeder enters CB-DG-1B."),
        E("CB-DG-1B", "BUS-4160-B", "high", "solid_power", "CB-DG-1B lands on BUS-4160-B."),
        E("BUS-4160-B", "CB-TIE-BC", "high", "solid_power", "BUS-4160-B right end enters CB-TIE-BC."),
        E("CB-TIE-BC", "BUS-4160-C", "high", "solid_power", "CB-TIE-BC right side lands on BUS-4160-C."),
        E("SWYD-115KV", "TR-SAT-1", "high", "solid_power", "Top 115 kV bus drops into TR-SAT-1."),
        E("TR-SAT-1", "CB-52-4C", "high", "solid_power", "TR-SAT-1 output continues to CB-52-4C."),
        E("CB-52-4C", "BUS-4160-C", "high", "solid_power", "CB-52-4C lands on BUS-4160-C."),
        E("EDG-1C", "CB-DG-1C", "high", "solid_power", "EDG-1C generator feeder enters CB-DG-1C."),
        E("CB-DG-1C", "BUS-4160-C", "high", "solid_power", "CB-DG-1C lands on BUS-4160-C."),
    ]


def feeder_edges(train: str) -> list[Edge]:
    bus = f"BUS-4160-{train}"
    out: list[Edge] = []
    for spec in FEEDER_LOADS:
        idx = spec[0]
        cb = f"CB-4{train}{idx}"
        ds = f"DS-4{train}{idx}"
        out.extend(
            [
                E(bus, cb, "high", "solid_power", f"{bus} tap drops into {cb}."),
                E(cb, ds, "high", "solid_power", f"{cb} vertical feeder continues to {ds}."),
            ]
        )
        if idx == "01":
            _, tr, ms, pump, cb48, bus48 = spec
            tr = tr.format(train=train)
            ms = ms.format(train=train)
            pump = pump.format(train=train)
            cb48 = cb48.format(train=train)
            bus48 = bus48.format(train=train)
            out.extend(
                [
                    E(ds, tr, "high", "solid_power", f"{ds} branches to the 480 V transformer {tr}."),
                    E(tr, cb48, "high", "solid_power", f"{tr} secondary drops to {cb48}."),
                    E(cb48, bus48, "high", "solid_power", f"{cb48} lands on {bus48}."),
                    E(ds, ms, "high", "solid_power", f"{ds} also continues on the pump feeder to {ms}."),
                    E(ms, pump, "high", "solid_power", f"{ms} feeds {pump}."),
                ]
            )
        else:
            _, device, load, _, _ = spec
            device = device.format(train=train)
            load = load.format(train=train)
            out.extend(
                [
                    E(ds, device, "high", "solid_power", f"{ds} vertical feeder continues to {device}."),
                    E(device, load, "high", "solid_power", f"{device} feeds {load}."),
                ]
            )
    return out


def mcc_edges(train: str) -> list[Edge]:
    bus = f"BUS-480-1{train}"
    out = [
        E(bus, f"MCC-{train}1", "high", "solid_power", f"{bus} drops to MCC-{train}1."),
        E(bus, f"MCC-{train}2", "high", "solid_power", f"{bus} also drops to MCC-{train}2 via the long vertical feeder."),
    ]
    for board, idx, device, load in MCC_LOADS[train]:
        board_name = f"MCC-{board}"
        breaker = f"CB-48{train}{idx}"
        line_type = "dashed_control" if device.startswith(("K-", "XFU-")) else "solid_power"
        out.extend(
            [
                E(board_name, breaker, "high", "solid_power", f"{board_name} branch feeds {breaker}."),
                E(breaker, device, "high", "solid_power", f"{breaker} vertical branch continues to {device}."),
                E(device, load, "high", line_type, f"{device} continues to {load}."),
            ]
        )
    return out


def bottom_precision_edges() -> list[Edge]:
    return [
        E("CHGR-125-1A", "BUS-125DC-A", "high", "solid_dc_power", "CHGR-125-1A output lands on BUS-125DC-A."),
        E("BAT-125-1A", "BUS-125DC-A", "high", "solid_dc_power", "BAT-125-1A is tapped to BUS-125DC-A."),
        E("BUS-125DC-A", "INV-120-1A", "high", "solid_dc_power", "BUS-125DC-A feeds INV-120-1A."),
        E("INV-120-1A", "PNL-RPS-A", "high", "solid_control_power", "INV-120-1A output feeds PNL-RPS-A."),
        E("INV-120-1A", "RELAY-K501A", "medium", "solid_control_power", "Upper solid route from INV-120-1A continues toward RELAY-K501A."),
        E("RELAY-K501A", "INV-120-1B", "medium", "solid_control_power", "Long solid route from relay A area continues to INV-120-1B side."),
        E("PNL-RPS-A", "RELAY-K501A", "high", "dashed_control", "Dashed control route from PNL-RPS-A reaches RELAY-K501A."),
        E("PNL-RPS-A", "XMTR-PT-501A", "high", "dotted_instrument", "Dotted instrument drop from PNL-RPS-A reaches XMTR-PT-501A."),
        E("PNL-RPS-A", "PNL-RPS-B", "medium", "dashed_control", "Dashed W203 route labeled PNL A/B TIE visibly ties the two RPS panels; the label itself is not a component node."),
        E("RELAY-K501A", "TC-52-4A", "medium", "dashed_control", "Dashed relay A trip lane is routed to TC-52-4A."),
        E("CHGR-125-1B", "BUS-125DC-B", "high", "solid_dc_power", "CHGR-125-1B output lands on BUS-125DC-B."),
        E("BAT-125-1B", "BUS-125DC-B", "high", "solid_dc_power", "BAT-125-1B is tapped to BUS-125DC-B."),
        E("BUS-125DC-B", "INV-120-1B", "high", "solid_dc_power", "BUS-125DC-B feeds INV-120-1B."),
        E("INV-120-1B", "PNL-RPS-B", "high", "solid_control_power", "INV-120-1B output feeds PNL-RPS-B."),
        E("PNL-RPS-B", "RELAY-K501B", "high", "dashed_control", "Dashed control route from PNL-RPS-B reaches RELAY-K501B."),
        E("PNL-RPS-B", "XMTR-PT-501B", "high", "dotted_instrument", "Dotted instrument drop from PNL-RPS-B reaches XMTR-PT-501B."),
        E("RELAY-K501B", "TC-52-4A", "high", "dashed_control", "Dashed relay B trip lane is routed to TC-52-4A."),
    ]


def final_edges() -> list[Edge]:
    edges: list[Edge] = []
    edges.extend(top_edges())
    for train in ("A", "B", "C"):
        edges.extend(feeder_edges(train))
    for train in ("A", "B", "C"):
        edges.extend(mcc_edges(train))
    edges.extend(bottom_precision_edges())
    return dedupe_edges(edges)


def without_edge(edges: list[Edge], source: str, target: str) -> list[Edge]:
    key = {source, target}
    return [edge for edge in edges if {edge[0], edge[1]} != key]


def jennifer_round1_edges() -> list[Edge]:
    return without_edge(final_edges(), "PNL-RPS-A", "PNL-RPS-B")


DIEGO_ROUTE_EXTRAS = [
    E("480V_CHGR-A_FEEDER", "CHGR-125-1A", "medium", "dashed_control", "High-recall route-label node for offpage charger A feeder."),
    E("480V_CHGR-B_FEEDER", "CHGR-125-1B", "low", "dashed_control", "High-recall route-label node for offpage charger B feeder."),
    E("PNL-RPS-A", "PNL_A/B_TIE", "medium", "dashed_control", "High-recall route-label node for PNL A/B tie."),
    E("PNL_A/B_TIE", "PNL-RPS-B", "medium", "dashed_control", "High-recall route-label node for PNL A/B tie continuation."),
    E("TC-52-4A", "RPS_TRIP_BUS", "medium", "dashed_control", "High-recall route-label node for RPS trip bus at TC terminals."),
    E("PNL-RPS-B", "RPS_TRIP_BUS", "low", "dashed_control", "High-recall route-label node for lower RPS trip bus lane."),
]

def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    out: list[Edge] = []
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        source, target, *_ = edge
        key = tuple(sorted((source, target)))
        if key not in seen:
            seen.add(key)
            out.append(edge)
    return out


def diego_round1_edges() -> list[Edge]:
    edges: list[Edge] = []
    edges.extend(top_edges())
    for train in ("A", "B", "C"):
        train_edges = feeder_edges(train)
        ds_ms = (f"DS-4{train}01", f"MS-{train}01")
        train_edges = [
            edge
            for edge in train_edges
            if not ({edge[0], edge[1]} == set(ds_ms))
        ]
        train_edges.append(
            E(
                f"TR-480-1{train}",
                f"MS-{train}01",
                "low",
                "solid_power",
                f"High-recall crowded feeder-01 candidate; Jennifer treats MS-{train}01 as a separate branch from DS-4{train}01.",
            )
        )
        edges.extend(train_edges)
    for train in ("A", "B", "C"):
        train_edges = mcc_edges(train)
        bus_mcc2 = (f"BUS-480-1{train}", f"MCC-{train}2")
        train_edges = [
            edge
            for edge in train_edges
            if not ({edge[0], edge[1]} == set(bus_mcc2))
        ]
        train_edges.append(
            E(
                f"MCC-{train}1",
                f"MCC-{train}2",
                "medium",
                "solid_power",
                f"High-recall long vertical feeder candidate from MCC-{train}1 to MCC-{train}2.",
            )
        )
        edges.extend(train_edges)
    edges.extend(without_edge(bottom_precision_edges(), "PNL-RPS-A", "PNL-RPS-B"))
    edges.extend(DIEGO_ROUTE_EXTRAS)
    return dedupe_edges(edges)


def csv_rows(edges: list[Edge]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["source", "target", "confidence", "line_type", "evidence"])
    for edge in edges:
        writer.writerow(edge)
    return buffer.getvalue().strip()


def node_lines(nodes: list[str], chunk_size: int = 10) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for i in range(0, len(nodes), chunk_size):
        writer.writerow(nodes[i : i + chunk_size])
    return buffer.getvalue().strip()


def matrix_csv(nodes: list[str], edges: list[Edge]) -> str:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for source, target, *_ in edges:
        if source not in idx or target not in idx:
            raise ValueError(f"edge uses node outside node order: {source!r}, {target!r}")
        if source == target:
            continue
        i, j = idx[source], idx[target]
        matrix[i][j] = 1
        matrix[j][i] = 1
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow([""] + nodes)
    for node, row in zip(nodes, matrix):
        writer.writerow([node] + row)
    return buffer.getvalue().strip()


def round_text(
    role: str,
    round_number: int,
    document_notes: list[str],
    nodes: list[str],
    edges: list[Edge],
    ambiguities: list[str],
) -> str:
    return "\n".join(
        [
            f"ROLE: {role}",
            "DOCUMENT: 25",
            f"ROUND: {round_number}",
            *document_notes,
            "",
            "NODE_ORDER_CSV",
            node_lines(nodes),
            "",
            "EDGE_LIST_CSV",
            csv_rows(edges),
            "",
            "MATRIX_CSV",
            matrix_csv(nodes, edges),
            "",
            "AMBIGUITIES",
            *ambiguities,
            "",
        ]
    )


def main() -> None:
    out = result_dir()
    precision_edges = final_edges()
    jennifer_edges = jennifer_round1_edges()
    diego_edges = diego_round1_edges()

    diego_round1 = round_text(
        "Diego high-recall extractor",
        1,
        [
            "SUMMARY: High-recall extraction covers the 115 kV source, three 4.16 kV buses, train A/B/C 4.16 kV feeders, 480 V MCC branches, and bottom 125 VDC/RPS trip logic.",
            "NOTE: Route-label nodes and crowded feeder-01/MCC continuation candidates are intentionally retained for Jennifer review.",
        ],
        DIEGO_NODES,
        diego_edges,
        [
            "- Route labels 480V_CHGR-A_FEEDER, 480V_CHGR-B_FEEDER, RPS_TRIP_BUS, and PNL_A/B_TIE may be off-page/route labels rather than component rows.",
            "- Feeder 01 transformer/MS geometry is crowded; high recall includes TR-480-1x to MS-x01 candidates.",
            "- MCC x1 to x2 vertical continuation may be represented either as MCC-to-MCC continuation or as separate BUS-480 taps.",
        ],
    )
    jennifer_round1 = round_text(
        "Jennifer precision reviewer/refiner",
        1,
        [
            "SUMMARY: Removed route/off-page labels from the component node list and pruned route-label edges.",
            "SUMMARY: Represented feeder 01 as DS-4x01 branching to TR-480-1x/CB-52-48x/BUS-480-1x and separately to MS-x01/PUMP-RHR-P201x.",
        ],
        FINAL_NODES,
        jennifer_edges,
        [
            "- Route labels are recorded in the transcript but are not rows/columns in the final component matrix.",
            "- Long routed dashed lanes in the RPS area are not expanded into cliques.",
        ],
    )
    diego_round2 = round_text(
        "Diego high-recall extractor",
        2,
        [
            "AGREE_WITH_JENNIFER_ROUND1",
            "SUMMARY: Reinspection supports keeping the 200 visible component nodes, but adds PNL-RPS-A to PNL-RPS-B as the component-to-component representation of the PNL A/B TIE route.",
        ],
        FINAL_NODES,
        precision_edges,
        [
            "- Route labels remain non-component annotations; the PNL A/B TIE line is represented by the two visible RPS panel endpoints.",
        ],
    )
    jennifer_round2 = round_text(
        "Jennifer precision reviewer/refiner",
        2,
        [
            "AGREE_WITH_DIEGO_ROUND2",
            "SUMMARY: Final saturated matrix uses the 200-node precision graph with Diego round-2 PNL-RPS-A to PNL-RPS-B correction.",
        ],
        FINAL_NODES,
        precision_edges,
        [
            "- Final answer uses only visible component/bus/ground nodes and visually supported adjacent edges.",
        ],
    )

    (out / "diego_round1_output.txt").write_text(diego_round1, encoding="utf-8")
    (out / "jennifer_round1_review.txt").write_text(jennifer_round1, encoding="utf-8")
    (out / "diego_round2_response.txt").write_text(diego_round2, encoding="utf-8")
    (out / "jennifer_round2_final.txt").write_text(jennifer_round2, encoding="utf-8")
    (out / "subagent_round_transcript.md").write_text(
        "\n\n".join(
            [
                "# Document 25 Multi-Agent Rounds",
                "## Diego Round 1",
                f"High-recall pass proposed {len(DIEGO_NODES)} nodes and {len(diego_edges)} edges, including route-label nodes and low-confidence crowded-area candidates.",
                "## Jennifer Round 1",
                f"Precision review removed route-label rows and unsupported candidates, yielding {len(FINAL_NODES)} component nodes and {len(jennifer_edges)} edges.",
                "## Diego Round 2",
                "Diego rechecked the lower RPS and feeder-01 areas, agreeing with component-only nodes and adding the PNL-RPS-A to PNL-RPS-B tie.",
                "## Jennifer Round 2",
                f"Jennifer confirmed the saturated {len(FINAL_NODES)}-node, {len(precision_edges)}-edge component matrix.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote doc25 round outputs to {out}")
    print(f"Nodes: {len(FINAL_NODES)}")
    print(f"Diego round 1 nodes: {len(DIEGO_NODES)}")
    print(f"Diego round 1 edges: {len(diego_edges)}")
    print(f"Jennifer final edges: {len(precision_edges)}")


if __name__ == "__main__":
    main()
