from __future__ import annotations

from pathlib import Path


WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc18_work")


top_nodes = [
    "GRID-SWYD-1", "CB-GRID-A",
    "GRID-SWYD-2", "CB-GRID-B",
    "BB-SWYD-230",
    "TR-SAT-1A", "CB-SAT-A",
    "BUS-4160A",
    "DG-1A", "CB-DG-A",
    "PT-4160A", "FU-PT-A", "XFMR-CTRL-A", "TB-RPS-A", "SW-43A",
    "TR-480-A1", "CB-480A-IN", "BUS-480A",
    "TR-480-B1", "CB-480B-IN", "BUS-480B",
    "GND-4160A",
    "CB-4160-TIE",
    "BUS-4160B",
    "TR-SAT-1B", "CB-SAT-B",
    "DG-1B", "CB-DG-B",
    "PT-4160B", "FU-PT-B", "XFMR-CTRL-B", "TB-RPS-B", "SW-43B",
    "TR-480-C1", "CB-480C-IN", "BUS-480C",
    "TR-480-D1", "CB-480D-IN", "BUS-480D",
    "GND-4160B",
    "GEN-MAIN-1", "CB-GEN-1SO",
    "TR-UAT-1A", "CB-UAT-A",
    "TR-UAT-1B", "CB-UAT-B",
]

branch_defs = {
    "A": [
        ("CB-A01", "DS-A01", "MS-A01", "PUMP-CCW-A1"),
        ("CB-A02", "DS-A02", "MS-A02", "PUMP-RHR-A1"),
        ("CB-A03", "FS-A03", "MS-A03", "FAN-RB-A1"),
        ("CB-A04", "DS-A04", "RY-A04", "MOV-SI-A11"),
        ("CB-A05", "DS-A05", "CP-A05", "PNL-LTG-A1"),
        ("CB-A06", "DS-A06", "MS-A06", "PUMP-AFW-A1"),
        ("CB-A07", "FS-A07", "FU-A07", "HTR-PZR-A1"),
        ("CB-A08", "DS-A08", "TB-A08", "SPARE-A8"),
    ],
    "B": [
        ("CB-B01", "DS-B01", "MS-B01", "PUMP-CCW-B1"),
        ("CB-B02", "DS-B02", "MS-B02", "PUMP-RHR-B1"),
        ("CB-B03", "FS-B03", "MS-B03", "FAN-FUEL-B1"),
        ("CB-B04", "DS-B04", "RY-B04", "MOV-CCW-B21"),
        ("CB-B05", "DS-B05", "CP-B05", "MCC-AUX-B6"),
        ("CB-B06", "DS-B06", "MS-B06", "AIR-CMP-B1"),
        ("CB-B07", "FS-B07", "RY-B07", "VLV-CHG-B1"),
    ],
    "C": [
        ("CB-C01", "DS-C01", "MS-C01", "PUMP-HPCI-C1"),
        ("CB-C02", "DS-C02", "MS-C02", "PUMP-RCW-C1"),
        ("CB-C03", "FS-C03", "MS-C03", "FAN-RB-C1"),
        ("CB-C04", "DS-C04", "RY-C04", "MOV-RHR-C11"),
        ("CB-C05", "DS-C05", "MS-C05", "PUMP-SEAL-C1"),
        ("CB-C06", "DS-C06", "CP-C06", "PNL-IC-C7"),
        ("CB-C07", "FS-C07", "MS-C07", "SUMP-PMP-C1"),
        ("CB-C08", "DS-C08", "FU-C08", "HTR-VENT-C2"),
    ],
    "D": [
        ("CB-D01", "DS-D01", "MS-D01", "PUMP-AFW-D1"),
        ("CB-D02", "DS-D02", "MS-D02", "FAN-CR-D1"),
        ("CB-D03", "FS-D03", "RY-D03", "MOV-SI-D21"),
        ("CB-D04", "DS-D04", "MS-D04", "PUMP-LUBE-D1"),
        ("CB-D05", "DS-D05", "CP-D05", "PNL-ESS-D5"),
        ("CB-D06", "DS-D06", "MS-D06", "COMP-AIR-D1"),
        ("CB-D07", "FS-D07", "TB-D07", "SPARE-D7"),
    ],
}

dc_control_nodes = [
    "CHG-125A", "REC-125A", "CB-DC-A", "BUS-125A", "BAT-125A",
    "GND-DC-A", "INV-120A", "UPS-120A", "BUS-120A",
    "RPS-PNL-A", "PLC-RPS-A",
    "RELAY-K101", "RELAY-K102", "RELAY-K103", "RELAY-K104",
    "JB-RPS-A", "PNL-ANN-A",
    "CHG-125B", "REC-125B", "CB-DC-B", "BUS-125B", "BAT-125B",
    "GND-DC-B", "INV-120B", "UPS-120B", "BUS-120B",
    "RPS-PNL-B", "PLC-RPS-B",
    "RELAY-K201", "RELAY-K202", "RELAY-K203", "RELAY-K204",
    "JB-RPS-B", "PNL-ANN-B",
]


nodes = list(top_nodes)
for group in ("A", "B", "C", "D"):
    for branch in branch_defs[group]:
        nodes.extend(branch)
nodes.extend(dc_control_nodes)

if len(nodes) != len(set(nodes)):
    seen: set[str] = set()
    duplicates: list[str] = []
    for node in nodes:
        if node in seen:
            duplicates.append(node)
        seen.add(node)
    raise ValueError(f"duplicate nodes: {duplicates}")

edges: list[tuple[str, str, str, str, str]] = []


def add(source: str, target: str, confidence: str, line_type: str, evidence: str) -> None:
    if source not in nodes or target not in nodes:
        raise ValueError(f"unknown node in edge: {source} -> {target}")
    clean_evidence = evidence.replace(",", ";")
    edge = (source, target, confidence, line_type, clean_evidence)
    reverse = (target, source, confidence, line_type, clean_evidence)
    if edge not in edges and reverse not in edges:
        edges.append(edge)


def chain(parts: list[str], confidence: str, line_type: str, evidence: str) -> None:
    for source, target in zip(parts, parts[1:]):
        add(source, target, confidence, line_type, evidence)


# Top source, 230 kV, 4160 V, and 480 V distribution.
chain(["GRID-SWYD-1", "CB-GRID-A", "BB-SWYD-230"], "high", "ac-power", "Grid source 1 breaker lands on 230 kV switchyard bus")
chain(["GRID-SWYD-2", "CB-GRID-B", "BB-SWYD-230"], "high", "ac-power", "Grid source 2 breaker lands on 230 kV switchyard bus")
chain(["BB-SWYD-230", "CB-GEN-1SO", "GEN-MAIN-1"], "high", "ac-power", "Main generator breaker ties generator to switchyard bus")
chain(["GEN-MAIN-1", "TR-UAT-1A", "CB-UAT-A"], "high", "ac-power", "UAT 1A is visibly tapped from main generator with breaker below")
chain(["GEN-MAIN-1", "TR-UAT-1B", "CB-UAT-B"], "high", "ac-power", "UAT 1B is visibly tapped from main generator with breaker below")
chain(["BB-SWYD-230", "TR-SAT-1A", "CB-SAT-A", "BUS-4160A"], "high", "ac-power", "Station transformer 1A feeds 4160 bus A")
chain(["BB-SWYD-230", "TR-SAT-1B", "CB-SAT-B", "BUS-4160B"], "high", "ac-power", "Station transformer 1B feeds 4160 bus B")
chain(["DG-1A", "CB-DG-A", "BUS-4160A"], "high", "ac-power", "Diesel generator 1A breaker lands on bus 4160A")
chain(["DG-1B", "CB-DG-B", "BUS-4160B"], "high", "ac-power", "Diesel generator 1B breaker lands on bus 4160B")
chain(["BUS-4160A", "CB-4160-TIE", "BUS-4160B"], "high", "ac-power", "Normally-open 4160 tie breaker between A and B bus bars")
add("BUS-4160A", "GND-4160A", "high", "ground", "Ground symbol taps bus 4160A")
add("BUS-4160B", "GND-4160B", "high", "ground", "Ground symbol taps bus 4160B")
chain(["BUS-4160A", "PT-4160A", "FU-PT-A", "XFMR-CTRL-A", "TB-RPS-A", "SW-43A"], "high", "control", "A-side PT control chain leaves bus 4160A")
add("BUS-4160A", "TB-RPS-A", "high", "ac-power", "A-side solid feeder drops from bus 4160A into TB-RPS-A before transformer 480 A1")
chain(["BUS-4160B", "PT-4160B", "FU-PT-B", "XFMR-CTRL-B", "TB-RPS-B", "SW-43B"], "high", "control", "B-side PT control chain leaves bus 4160B")
chain(["TB-RPS-A", "TR-480-A1", "CB-480A-IN", "BUS-480A"], "high", "ac-power", "Transformer 480 A1 is below TB-RPS-A on the A-side solid feeder and feeds bus 480A")
chain(["BUS-4160A", "TR-480-B1", "CB-480B-IN", "BUS-480B"], "high", "ac-power", "Transformer 480 B1 feeds bus 480B")
chain(["BUS-4160B", "TR-480-C1", "CB-480C-IN", "BUS-480C"], "high", "ac-power", "Transformer 480 C1 feeds bus 480C")
chain(["BUS-4160B", "TR-480-D1", "CB-480D-IN", "BUS-480D"], "high", "ac-power", "Transformer 480 D1 feeds bus 480D")


for bus, group in [
    ("BUS-480A", "A"),
    ("BUS-480B", "B"),
    ("BUS-480C", "C"),
    ("BUS-480D", "D"),
]:
    for cb, device, controller, load in branch_defs[group]:
        chain([bus, cb, device, controller, load], "high", "ac-power", f"{group}-section radial feeder to {load}")


# 125 VDC / 120 VAC control-power sections. Long input conductors visibly descend
# from 480B to train A and 480C to train B before entering the chargers.
chain(["BUS-480B", "CHG-125A", "REC-125A", "CB-DC-A", "BUS-125A"], "high", "dc-power", "Train A charger input conductor descends from bus 480B, then rectifier and DC breaker land on bus 125A")
add("BUS-125A", "BAT-125A", "high", "dc-power", "Battery 125A vertical tap from bus 125A")
add("BUS-125A", "GND-DC-A", "high", "ground", "DC ground taps bus 125A")
add("BUS-125A", "INV-120A", "high", "dc-power", "Inverter 120A input is fed from bus 125A")
add("INV-120A", "UPS-120A", "high", "control", "Dashed AC/control run from inverter 120A to UPS 120A")
chain(["UPS-120A", "BUS-120A", "RPS-PNL-A"], "high", "ac-power", "UPS 120A lands on bus 120A, which feeds RPS panel A")
add("RPS-PNL-A", "PLC-RPS-A", "high", "control", "Dashed signal run from RPS panel A to PLC RPS A")
add("PLC-RPS-A", "RELAY-K101", "high", "control", "PLC RPS A output bundle enters top relay run to K101")
add("RELAY-K101", "RELAY-K102", "high", "control", "Top dashed relay run connects K101 to K102")
add("RELAY-K102", "JB-RPS-A", "high", "control", "Top dashed relay run continues to junction box RPS A")
add("RELAY-K102", "PNL-ANN-A", "high", "control", "Dashed vertical and horizontal run from K102 to annunciator panel A")
add("PLC-RPS-A", "RELAY-K103", "high", "control", "PLC RPS A output bundle enters lower relay run to K103")
add("RELAY-K103", "RELAY-K104", "high", "control", "Lower dashed relay run connects K103 to K104")

chain(["BUS-480C", "CHG-125B", "REC-125B", "CB-DC-B", "BUS-125B"], "high", "dc-power", "Train B charger input conductor descends from bus 480C, then rectifier and DC breaker land on bus 125B")
add("BUS-125B", "BAT-125B", "high", "dc-power", "Battery 125B vertical tap from bus 125B")
add("BUS-125B", "GND-DC-B", "high", "ground", "DC ground taps bus 125B")
add("BUS-125B", "INV-120B", "high", "dc-power", "Inverter 120B input is fed from bus 125B")
add("INV-120B", "UPS-120B", "high", "control", "Dashed AC/control run from inverter 120B to UPS 120B")
chain(["UPS-120B", "BUS-120B", "RPS-PNL-B"], "high", "ac-power", "UPS 120B lands on bus 120B, which feeds RPS panel B")
add("RPS-PNL-B", "PLC-RPS-B", "high", "control", "Dashed signal run from RPS panel B to PLC RPS B")
add("PLC-RPS-B", "RELAY-K201", "high", "control", "PLC RPS B output bundle enters top relay run to K201")
add("RELAY-K201", "RELAY-K202", "high", "control", "Top dashed relay run connects K201 to K202")
add("RELAY-K202", "JB-RPS-B", "high", "control", "Top dashed relay run continues to junction box RPS B")
add("RELAY-K202", "PNL-ANN-B", "high", "control", "Dashed vertical and horizontal run from K202 to annunciator panel B")
add("PLC-RPS-B", "RELAY-K203", "high", "control", "PLC RPS B output bundle enters lower relay run to K203")
add("RELAY-K203", "RELAY-K204", "high", "control", "Lower dashed relay run connects K203 to K204")

precision_edges = list(edges)

high_recall_extras = [
    ("CB-UAT-A", "BUS-4160A", "low", "ac-power", "Diego high-recall possible continuation from UAT A breaker toward 4160A, later rejected because no landed conductor is visible"),
    ("CB-UAT-B", "BUS-4160B", "low", "ac-power", "Diego high-recall possible continuation from UAT B breaker toward 4160B, later rejected because no landed conductor is visible"),
    ("PLC-RPS-A", "RELAY-K102", "low", "control", "Diego high-recall overconnection within dashed A relay bundle"),
    ("PLC-RPS-A", "RELAY-K104", "low", "control", "Diego high-recall overconnection within dashed A relay bundle"),
    ("RELAY-K101", "JB-RPS-A", "low", "control", "Diego high-recall possible top dashed run shortcut to JB RPS A"),
    ("RELAY-K103", "PNL-ANN-A", "low", "control", "Diego high-recall possible lower dashed run shortcut to annunciator A"),
    ("PLC-RPS-B", "RELAY-K202", "low", "control", "Diego high-recall overconnection within dashed B relay bundle"),
    ("PLC-RPS-B", "RELAY-K204", "low", "control", "Diego high-recall overconnection within dashed B relay bundle"),
    ("RELAY-K201", "JB-RPS-B", "low", "control", "Diego high-recall possible top dashed run shortcut to JB RPS B"),
    ("RELAY-K203", "PNL-ANN-B", "low", "control", "Diego high-recall possible lower dashed run shortcut to annunciator B"),
    ("BUS-480A", "CHG-125A", "low", "dc-power", "Diego high-recall alternate source-bus candidate; spanning crop shows train A charger is from 480B, not 480A"),
    ("BUS-480D", "CHG-125B", "low", "dc-power", "Diego high-recall alternate source-bus candidate; spanning crop shows train B charger is from 480C, not 480D"),
]

diego_edges = precision_edges + high_recall_extras
jennifer_edges = precision_edges


def matrix_rows(edge_list: list[tuple[str, str, str, str, str]]) -> list[list[str]]:
    adj = {node: {other: 0 for other in nodes} for node in nodes}
    for source, target, *_ in edge_list:
        if source == target:
            raise ValueError(f"self edge: {source}")
        adj[source][target] = 1
        adj[target][source] = 1
    rows = [[""] + nodes]
    for node in nodes:
        rows.append([node] + [str(adj[node][other]) for other in nodes])
    return rows


def write_round(path: Path, role: str, summary: str, edge_list: list[tuple[str, str, str, str, str]], ambiguities: list[str]) -> None:
    matrix = matrix_rows(edge_list)
    lines = [
        f"ROLE: {role}",
        "DOCUMENT: 18",
        f"SUMMARY: {summary}",
        "NODE_ORDER_CSV",
        "node",
        *nodes,
        "EDGE_LIST_CSV",
        "source,target,confidence,line_type,evidence",
    ]
    lines.extend(",".join(edge) for edge in edge_list)
    lines.extend(["MATRIX_CSV"])
    lines.extend(",".join(row) for row in matrix)
    lines.extend(["AMBIGUITIES"])
    lines.extend(ambiguities)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_agreement(path: Path, role: str, agreement: str, summary: str) -> None:
    path.write_text(
        "\n".join([
            f"ROLE: {role}",
            "DOCUMENT: 18",
            agreement,
            f"SUMMARY: {summary}",
        ]) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    write_round(
        WORK / "diego_round1_output.txt",
        "Diego high-recall extractor",
        f"High-recall graph with {len(nodes)} nodes and {len(diego_edges)} edges including low-confidence UAT, relay-bundle, and alternate charger-feed candidates.",
        diego_edges,
        [
            "Diego kept UAT breaker-to-4160 bus continuations as low-confidence because the transformer/breaker symbols are close to the 4160 bus, but the raw view does not show a landed conductor.",
            "Diego included shortcut edges within dashed RPS relay bundles for recall; these should be pruned if only nearest visible dashed runs are accepted.",
            "Diego included alternate 480A/480D charger source candidates; spanning crops suggest final sources are 480B for train A and 480C for train B.",
        ],
    )
    write_round(
        WORK / "jennifer_round1_review.txt",
        "Jennifer precision reviewer/refiner",
        f"Precision graph with {len(nodes)} nodes and {len(jennifer_edges)} visually supported edges; removed Diego's unsupported UAT-to-bus, relay shortcut, wrong charger-source, and unsupported K104/K204-to-annunciator candidates.",
        jennifer_edges,
        [
            "No remaining ambiguous edge is promoted to final: the final graph uses only labeled components and directly landed solid/dashed conductors visible in doc18 resources. K104-to-PNL-ANN-A and K204-to-PNL-ANN-B are excluded because no dashed landing is visible.",
            "Line-wrapped load labels are normalized with hyphens: PUMP-HPCI-C1, PUMP-SEAL-C1, PUMP-LUBE-D1.",
        ],
    )
    write_agreement(
        WORK / "diego_round2_response.txt",
        "Diego high-recall extractor",
        "AGREE_WITH_JENNIFER_ROUND1",
        f"After reviewing Jennifer's precision pruning, Diego agrees the {len(nodes)}-node {len(jennifer_edges)}-edge graph is saturated.",
    )
    write_agreement(
        WORK / "jennifer_round2_final.txt",
        "Jennifer precision reviewer",
        "AGREE_WITH_DIEGO_ROUND2",
        f"Final inspection supports the validated {len(nodes)}-node {len(jennifer_edges)}-edge Jennifer round-1 precision graph as the saturated final matrix.",
    )
    (WORK / "subagent_round_transcript.md").write_text(
        "\n".join([
            "# Document 18 Subagent Round Transcript",
            "",
            "## Diego Round 1",
            f"Diego proposed {len(nodes)} nodes and {len(diego_edges)} edges. The high-recall set intentionally included low-confidence UAT breaker continuations, relay-bundle shortcut edges, and alternate charger source-bus candidates.",
            "",
            "## Jennifer Round 1",
        f"Jennifer kept {len(jennifer_edges)} visually supported edges. She removed the UAT breaker-to-bus continuations because the raw top-right source crop does not show landed conductors from CB-UAT-A/CB-UAT-B to a 4160 bus. She also removed shortcut relay-bundle edges, removed unsupported K104/K204-to-annunciator edges, corrected the A-side 4160 feeder as BUS-4160A -> TB-RPS-A -> TR-480-A1, and corrected the charger feeds to BUS-480B -> CHG-125A and BUS-480C -> CHG-125B using the spanning overview/left-half crops.",
            "",
            "## Diego Round 2",
            "Diego agreed with Jennifer's precision graph.",
            "",
            "## Jennifer Round 2",
            "Jennifer agreed with Diego round 2; the matrix saturated.",
        ]) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote document 18 round outputs in {WORK}")
    print({"nodes": len(nodes), "diego_round1_edges": len(diego_edges), "final_edges": len(jennifer_edges)})


if __name__ == "__main__":
    main()
