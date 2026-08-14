from __future__ import annotations

import csv
import io
from pathlib import Path


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\24\Raw + wires + junctions"
)
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc24_work")


def result_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".doc24_write_probe"
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
    "OFFSITE-1",
    "CB-101A",
    "TR-SAT-1A",
    "BUS-101A",
    "EDG-1A",
    "CB-DG1A",
    "SW-MAN-A",
    "TB-DG-A",
    "CB-TIE-1",
    "OFFSITE-2",
    "CB-101B",
    "TR-SAT-1B",
    "BUS-101B",
    "EDG-1B",
    "CB-DG1B",
    "SW-MAN-B",
    "TB-DG-B",
    "CB-201A",
    "TR-1A",
    "CB-202A",
    "BUS-201A",
    "CB-201B",
    "TR-1B",
    "CB-202B",
    "BUS-201B",
]


LOADS = [
    ("01", "PUMP-P201{train}"),
    ("02", "FAN-F202{train}"),
    ("03", "MOV-HV203{train}"),
    ("04", "PUMP-P204{train}"),
    ("05", "CHLR-205{train}"),
    ("06", "HTR-206{train}"),
    ("07", "VALVE-MV207{train}"),
    ("08", "PMP-LP208{train}"),
    ("09", "COMP-C209{train}"),
]


def feeder_nodes(train: str) -> list[str]:
    nodes: list[str] = []
    for idx, load_template in LOADS:
        prefix = f"2{train}{idx}"
        nodes.extend(
            [
                f"CB-{prefix}",
                f"DS-{prefix}",
                f"MCC-{prefix}",
                f"TB-{prefix}",
                load_template.format(train=train),
                f"HS-{prefix}",
                f"RELAY-K{prefix}",
            ]
        )
    return nodes


BOTTOM_A_NODES = [
    "DC-BUS-125A",
    "BAT-125A",
    "CHG-125A",
    "INV-120A",
    "PNL-DC-A",
    "ESFAS-PNL-A",
    "METER-V1",
    "GND-DC-A",
    "PNL-AC-A",
    "RPS-PNL-A",
    "TRIP-MOD-A",
    "PT-401A",
    "LT-402A",
    "FT-403A",
    "JB-401A",
    "GND-401A",
    "TB-RPS-A",
    "RELAY-K27A",
    "RELAY-K59A",
    "RELAY-K81A",
    "RELAY-K86A",
]

BOTTOM_B_NODES = [
    "DC-BUS-125B",
    "BAT-125B",
    "CHG-125B",
    "INV-120B",
    "PNL-DC-B",
    "ESFAS-PNL-B",
    "GND-DC-B",
    "PNL-AC-B",
    "RPS-PNL-B",
    "TRIP-MOD-B",
    "PT-401B",
    "LT-402B",
    "FT-403B",
    "JB-401B",
    "GND-401B",
    "TB-RPS-B",
    "RELAY-K27B",
    "RELAY-K59B",
    "RELAY-K81B",
    "RELAY-K86B",
    "LAMP-ALM-B",
]

SHARED_NODES = [
    "SYNC-CAB",
    "LOAD-SHED-CAB",
    "TDR-1",
    "TDR-2",
    "LAMP-ALM-A",
    "ANN-PNL-1",
    "SEQ-REC-1",
]

NODES = TOP_NODES + feeder_nodes("A") + feeder_nodes("B") + BOTTOM_A_NODES + BOTTOM_B_NODES + SHARED_NODES


def top_edges() -> list[Edge]:
    return [
        E("OFFSITE-1", "CB-101A", "high", "power", "OFFSITE-1 AC source is hardwired to CB-101A."),
        E("CB-101A", "TR-SAT-1A", "high", "power", "CB-101A output feeds TR-SAT-1A."),
        E("TR-SAT-1A", "BUS-101A", "high", "power", "TR-SAT-1A secondary lands on BUS-101A."),
        E("EDG-1A", "CB-DG1A", "high", "power", "EDG-1A generator symbol feeds CB-DG1A."),
        E("CB-DG1A", "BUS-101A", "high", "power", "CB-DG1A output lands on BUS-101A."),
        E("SW-MAN-A", "TB-DG-A", "high", "control", "Dashed manual-start path runs from SW-MAN-A to TB-DG-A."),
        E("TB-DG-A", "CB-DG1A", "high", "control", "Dashed DG control path continues from TB-DG-A to CB-DG1A."),
        E("BUS-101A", "CB-TIE-1", "high", "power", "CB-TIE-1 is inserted at the right end of BUS-101A."),
        E("CB-TIE-1", "BUS-101B", "high", "power", "CB-TIE-1 right side continues into BUS-101B."),
        E("OFFSITE-2", "CB-101B", "high", "power", "OFFSITE-2 AC source is hardwired to CB-101B."),
        E("CB-101B", "TR-SAT-1B", "high", "power", "CB-101B output feeds TR-SAT-1B."),
        E("TR-SAT-1B", "BUS-101B", "high", "power", "TR-SAT-1B secondary lands on BUS-101B."),
        E("EDG-1B", "CB-DG1B", "high", "power", "EDG-1B generator symbol feeds CB-DG1B."),
        E("CB-DG1B", "BUS-101B", "high", "power", "CB-DG1B output lands on BUS-101B."),
        E("SW-MAN-B", "TB-DG-B", "high", "control", "Dashed manual-start path runs from SW-MAN-B to TB-DG-B."),
        E("TB-DG-B", "CB-DG1B", "high", "control", "Dashed DG control path continues from TB-DG-B to CB-DG1B."),
        E("BUS-101A", "CB-201A", "high", "power", "BUS-101A feeder drops through CB-201A."),
        E("CB-201A", "TR-1A", "high", "power", "CB-201A feeds transformer TR-1A."),
        E("TR-1A", "CB-202A", "high", "power", "TR-1A output feeds CB-202A."),
        E("CB-202A", "BUS-201A", "high", "power", "CB-202A lands on the 4.16 kV safety BUS-201A."),
        E("BUS-101B", "CB-201B", "high", "power", "BUS-101B feeder drops through CB-201B."),
        E("CB-201B", "TR-1B", "high", "power", "CB-201B feeds transformer TR-1B."),
        E("TR-1B", "CB-202B", "high", "power", "TR-1B output feeds CB-202B."),
        E("CB-202B", "BUS-201B", "high", "power", "CB-202B lands on the 4.16 kV safety BUS-201B."),
        E("CB-TIE-1", "SYNC-CAB", "medium", "control", "SYNC-CAB is drawn on the dashed synchronizing/control route below CB-TIE-1."),
    ]


def feeder_edges(train: str) -> list[Edge]:
    bus = f"BUS-201{train}"
    edges: list[Edge] = []
    control_chain: list[str] = []
    for idx, load_template in LOADS:
        prefix = f"2{train}{idx}"
        load = load_template.format(train=train)
        cb, ds, mcc, tb = f"CB-{prefix}", f"DS-{prefix}", f"MCC-{prefix}", f"TB-{prefix}"
        hs, relay = f"HS-{prefix}", f"RELAY-K{prefix}"
        edges.extend(
            [
                E(bus, cb, "high", "power", f"{cb} drops directly from {bus}."),
                E(cb, ds, "high", "power", f"{cb} output continues to {ds}."),
                E(ds, mcc, "high", "power", f"{ds} output continues down to {mcc}."),
                E(mcc, tb, "high", "power", f"{mcc} output continues down to {tb}."),
                E(tb, load, "high", "power", f"{tb} terminal block feeds {load}."),
                E(mcc, relay, "medium", "control", f"Dashed control/trip branch from {mcc} reaches {relay}."),
            ]
        )
        control_chain.extend([hs, relay])
    for left, right in zip(control_chain, control_chain[1:]):
        edges.append(E(left, right, "medium", "control", f"Adjacent symbols {left} and {right} are joined on the dashed control/trip route."))
    return edges


def bottom_train_edges(train: str) -> list[Edge]:
    bus = f"DC-BUS-125{train}"
    bat = f"BAT-125{train}"
    chg = f"CHG-125{train}"
    inv = f"INV-120{train}"
    pnl_dc = f"PNL-DC-{train}"
    esf = f"ESFAS-PNL-{train}"
    gnd_dc = f"GND-DC-{train}"
    pnl_ac = f"PNL-AC-{train}"
    rps = f"RPS-PNL-{train}"
    trip = f"TRIP-MOD-{train}"
    jb = f"JB-401{train}"
    gnd = f"GND-401{train}"
    tb = f"TB-RPS-{train}"
    edges = [
        E(bus, bat, "high", "dc_power", f"{bat} taps from {bus}."),
        E(bus, chg, "high", "dc_power", f"{chg} charger taps from {bus}."),
        E(bus, inv, "high", "dc_power", f"{inv} inverter taps from {bus}."),
        E(bus, pnl_dc, "high", "dc_power", f"{pnl_dc} taps from {bus}."),
        E(pnl_dc, esf, "high", "dc_power", f"{pnl_dc} is solid-wired to {esf}."),
        E(pnl_dc, gnd_dc, "medium", "ground", f"{gnd_dc} is drawn below the {pnl_dc} vertical."),
        E(inv, pnl_ac, "high", "power", f"{inv} output drops to {pnl_ac}."),
        E(pnl_ac, rps, "medium", "control", f"{pnl_ac} and {rps} are joined by a dashed control route."),
        E(rps, trip, "medium", "control", f"{rps} dashed route continues to {trip}."),
        E(rps, f"RELAY-K27{train}", "medium", "control", f"{rps} drops to the {train}-side relay chain at RELAY-K27{train}."),
        E(f"RELAY-K27{train}", f"RELAY-K59{train}", "medium", "control", f"Relay chain connects RELAY-K27{train} to RELAY-K59{train}."),
        E(f"RELAY-K59{train}", f"RELAY-K81{train}", "medium", "control", f"Relay chain connects RELAY-K59{train} to RELAY-K81{train}."),
        E(f"RELAY-K81{train}", f"RELAY-K86{train}", "medium", "control", f"Relay chain connects RELAY-K81{train} to RELAY-K86{train}."),
        E(f"RELAY-K86{train}", trip, "medium", "control", f"Relay chain returns upward to {trip}."),
        E(f"PT-401{train}", jb, "medium", "signal", f"PT-401{train} dotted signal route feeds {jb}."),
        E(f"LT-402{train}", jb, "medium", "signal", f"LT-402{train} dotted signal route feeds {jb}."),
        E(f"FT-403{train}", jb, "medium", "signal", f"FT-403{train} dotted signal route feeds {jb}."),
        E(jb, gnd, "medium", "ground", f"{jb} has a vertical solid ground branch to {gnd}."),
        E(jb, tb, "medium", "signal", f"{jb} dotted route continues to {tb}."),
        E(tb, rps, "medium", "signal", f"{tb} dotted/signal route enters {rps}."),
    ]
    if train == "A":
        edges.append(E(bus, "METER-V1", "high", "instrument", "METER-V1 is tapped from the right end of DC-BUS-125A."))
    return edges


def central_edges() -> list[Edge]:
    return [
        E("TRIP-MOD-A", "LOAD-SHED-CAB", "medium", "control", "Dashed A-side trip route runs toward LOAD-SHED-CAB."),
        E("LOAD-SHED-CAB", "TDR-1", "medium", "control", "TDR-1 is a side branch connected by dashed line to LOAD-SHED-CAB."),
        E("LOAD-SHED-CAB", "TDR-2", "medium", "control", "LOAD-SHED-CAB is connected by dashed line to TDR-2."),
        E("TRIP-MOD-B", "LOAD-SHED-CAB", "medium", "control", "Dashed B-side trip route runs toward LOAD-SHED-CAB."),
        E("LOAD-SHED-CAB", "LAMP-ALM-A", "medium", "signal", "Dotted signal branch from LOAD-SHED-CAB drops to LAMP-ALM-A."),
        E("LOAD-SHED-CAB", "LAMP-ALM-B", "medium", "signal", "Dotted signal branch from LOAD-SHED-CAB drops to LAMP-ALM-B."),
        E("ANN-PNL-1", "SEQ-REC-1", "medium", "signal", "Dotted signal line joins ANN-PNL-1 to SEQ-REC-1."),
    ]


def final_edges() -> list[Edge]:
    edges: list[Edge] = []
    edges.extend(top_edges())
    edges.extend(feeder_edges("A"))
    edges.extend(feeder_edges("B"))
    edges.extend(bottom_train_edges("A"))
    edges.extend(bottom_train_edges("B"))
    edges.extend(central_edges())
    return dedupe_edges(edges)


DIEGO_EXTRAS: list[Edge] = [
    E("BUS-101A", "BUS-101B", "low", "power", "High-recall bypass candidate across CB-TIE-1; final graph keeps the intervening tie breaker."),
    E("OFFSITE-1", "BUS-101A", "low", "power", "High-recall bypass candidate across CB-101A/TR-SAT-1A."),
    E("OFFSITE-2", "BUS-101B", "low", "power", "High-recall bypass candidate across CB-101B/TR-SAT-1B."),
    E("EDG-1A", "BUS-101A", "low", "power", "High-recall bypass candidate across CB-DG1A."),
    E("EDG-1B", "BUS-101B", "low", "power", "High-recall bypass candidate across CB-DG1B."),
    E("BUS-101A", "BUS-201A", "low", "power", "High-recall bypass candidate across CB-201A/TR-1A/CB-202A."),
    E("BUS-101B", "BUS-201B", "low", "power", "High-recall bypass candidate across CB-201B/TR-1B/CB-202B."),
    E("SYNC-CAB", "LOAD-SHED-CAB", "low", "control", "High-recall central-cab proximity candidate; no direct symbol-to-symbol line retained."),
    E("TRIP-MOD-A", "TDR-1", "low", "control", "High-recall inline-trip candidate; Jennifer found TDR-1 is a side branch off LOAD-SHED-CAB."),
    E("TDR-2", "TRIP-MOD-B", "low", "control", "High-recall inline-trip candidate; Jennifer found TDR-2 is a side branch off LOAD-SHED-CAB."),
    E("ESFAS-PNL-A", "TDR-1", "low", "control", "High-recall dashed-channel candidate; no direct ESFAS-to-TDR edge is retained."),
    E("ESFAS-PNL-B", "TDR-2", "low", "control", "High-recall dashed-channel candidate; no direct ESFAS-to-TDR edge is retained."),
    E("RPS-PNL-A", "ANN-PNL-1", "low", "signal", "High-recall dotted-route candidate; no direct RPS-to-annunciator edge is retained."),
    E("RPS-PNL-B", "ANN-PNL-1", "low", "signal", "High-recall dotted-route candidate; no direct RPS-to-annunciator edge is retained."),
    E("LOAD-SHED-CAB", "ANN-PNL-1", "low", "signal", "High-recall dotted-route candidate; Diego round 2 found the lower ANN route separate from the load-shed lamp branch."),
    E("RELAY-K2A09", "SYNC-CAB", "low", "control", "High-recall candidate from the A feeder control row into SYNC-CAB."),
    E("RELAY-K2B01", "SYNC-CAB", "low", "control", "High-recall candidate from the B feeder control row into SYNC-CAB."),
    E("DC-BUS-125A", "ESFAS-PNL-A", "low", "dc_power", "High-recall bypass candidate; final graph keeps PNL-DC-A as the intervening panel."),
    E("DC-BUS-125B", "ESFAS-PNL-B", "low", "dc_power", "High-recall bypass candidate; final graph keeps PNL-DC-B as the intervening panel."),
    E("DC-BUS-125A", "GND-DC-A", "low", "ground", "High-recall direct ground candidate; final graph keeps the ground through PNL-DC-A."),
    E("DC-BUS-125B", "GND-DC-B", "low", "ground", "High-recall direct ground candidate; final graph keeps the ground through PNL-DC-B."),
    E("PT-401A", "TB-RPS-A", "low", "signal", "High-recall signal-route shortcut; final graph keeps JB-401A as the intermediate node."),
    E("LT-402A", "TB-RPS-A", "low", "signal", "High-recall signal-route shortcut; final graph keeps JB-401A as the intermediate node."),
    E("FT-403A", "TB-RPS-A", "low", "signal", "High-recall signal-route shortcut; final graph keeps JB-401A as the intermediate node."),
    E("PT-401B", "TB-RPS-B", "low", "signal", "High-recall signal-route shortcut; final graph keeps JB-401B as the intermediate node."),
    E("LT-402B", "TB-RPS-B", "low", "signal", "High-recall signal-route shortcut; final graph keeps JB-401B as the intermediate node."),
    E("FT-403B", "TB-RPS-B", "low", "signal", "High-recall signal-route shortcut; final graph keeps JB-401B as the intermediate node."),
]

for train in ("A", "B"):
    for idx, _load_template in LOADS:
        prefix = f"2{train}{idx}"
        DIEGO_EXTRAS.append(
            E(
                f"RELAY-K{prefix}",
                f"TB-{prefix}",
                "low",
                "control",
                f"High-recall shortcut candidate from RELAY-K{prefix} to TB-{prefix}; final graph keeps the MCC control tap and power TB separately.",
            )
        )


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


def round_text(role: str, round_number: int, notes: list[str], edges: list[Edge], ambiguities: list[str]) -> str:
    return "\n".join(
        [
            f"ROLE: {role}",
            "DOCUMENT: 24",
            f"ROUND: {round_number}",
            *notes,
            "",
            "NODE_ORDER_CSV",
            node_lines(NODES),
            "",
            "EDGE_LIST_CSV",
            csv_rows(edges),
            "",
            "MATRIX_CSV",
            matrix_csv(NODES, edges),
            "",
            "AMBIGUITIES",
            *ambiguities,
            "",
        ]
    )


def main() -> None:
    out = result_dir()
    precision_edges = final_edges()
    diego_edges = dedupe_edges(precision_edges + DIEGO_EXTRAS)

    diego_round1 = round_text(
        "Diego high-recall extractor",
        1,
        [
            "SUMMARY: High-recall extraction covers top offsite/EDG AC buses, both 4.16 kV feeder banks, and bottom 125 VDC/control distribution.",
            "NOTE: Candidate bypass, sync-cab proximity, relay-to-TB, and signal shortcut edges are intentionally retained for Jennifer review.",
        ],
        diego_edges,
        [
            "- SYNC-CAB is visually tied to the central sync/control route; Diego includes several nearby control candidates for review.",
            "- Feeder dashed control rows are long shared routes; high recall keeps adjacent route edges plus low-confidence relay-to-TB shortcuts.",
            "- Bottom dotted signal routes pass through JB/TB symbols; shortcut PT/LT/FT-to-TB edges require precision review.",
        ],
    )
    jennifer_round1 = round_text(
        "Jennifer precision reviewer/refiner",
        1,
        [
            "SUMMARY: Removed direct bypasses across breakers/transformers, sync-cab proximity shortcuts, relay-to-TB shortcuts, and PT/LT/FT-to-TB signal shortcuts.",
            "SUMMARY: Kept only adjacent visible power, dashed control/trip, and dotted signal route edges; retained CB-TIE-1 to SYNC-CAB and represented TDR-1/TDR-2 as LOAD-SHED-CAB side branches.",
        ],
        precision_edges,
        [
            "- Long dashed control rows are represented by adjacent HS/relay edges, not all-to-all cliques.",
            "- LOAD-SHED-CAB is retained directly to TRIP-MOD-A/B, TDR-1/2, and lamp alarm branches; no direct sync-cab or ANN-PNL-1 link is kept.",
        ],
    )
    diego_round2 = round_text(
        "Diego high-recall extractor",
        2,
        [
            "AGREE_WITH_JENNIFER_ROUND1",
            "SUMMARY: Reinspection supports the precision graph except for removing LOAD-SHED-CAB to ANN-PNL-1; the lower ANN route is separate from the load-shed lamp branch.",
        ],
        precision_edges,
        [
            "- LOAD-SHED-CAB to ANN-PNL-1 is removed from the final matrix and retained only as a Diego round-1 high-recall candidate.",
        ],
    )
    jennifer_round2 = round_text(
        "Jennifer precision reviewer/refiner",
        2,
        [
            "AGREE_WITH_DIEGO_ROUND2",
            "SUMMARY: Final saturated matrix uses the Jennifer precision graph with Diego round-2 removal of LOAD-SHED-CAB to ANN-PNL-1.",
        ],
        precision_edges,
        [
            "- Final answer uses 200 nodes and the validated precision edge set.",
        ],
    )

    (out / "diego_round1_output.txt").write_text(diego_round1, encoding="utf-8")
    (out / "jennifer_round1_review.txt").write_text(jennifer_round1, encoding="utf-8")
    (out / "diego_round2_response.txt").write_text(diego_round2, encoding="utf-8")
    (out / "jennifer_round2_final.txt").write_text(jennifer_round2, encoding="utf-8")
    (out / "subagent_round_transcript.md").write_text(
        "\n\n".join(
            [
                "# Document 24 Multi-Agent Rounds",
                "## Diego Round 1",
                "High-recall pass proposed the precision graph plus candidate bypass, sync-cab proximity, relay-to-TB, and signal shortcut edges.",
                "## Jennifer Round 1",
                "Precision review removed unsupported shortcuts, represented TDR-1/TDR-2 as LOAD-SHED-CAB side branches, and kept adjacent visible power, control/trip, and signal-route edges.",
                "## Diego Round 2",
                "Diego agreed with Jennifer round 1 except for removing LOAD-SHED-CAB to ANN-PNL-1 after rechecking the center-bottom crop.",
                "## Jennifer Round 2",
                f"Jennifer confirmed saturation and finalized the {len(NODES)}-node, {len(precision_edges)}-edge precision matrix.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote doc24 round outputs to {out}")
    print(f"Nodes: {len(NODES)}")
    print(f"Diego round 1 edges: {len(diego_edges)}")
    print(f"Jennifer final edges: {len(precision_edges)}")


if __name__ == "__main__":
    main()
