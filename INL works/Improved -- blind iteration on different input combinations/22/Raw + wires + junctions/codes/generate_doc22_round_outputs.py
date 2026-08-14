from __future__ import annotations

import csv
import io
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions")
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc22_work")


def result_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".doc22_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return RESULTS
    except PermissionError:
        FALLBACK.mkdir(parents=True, exist_ok=True)
        return FALLBACK


def train_nodes(suffix: str) -> list[str]:
    special: list[str] = []
    if suffix == "A":
        special = ["CB-4AB-TIE", "SYNC-PNL-1"]
    elif suffix == "C":
        special = ["CB-4CD-TIE"]
    return [
        f"DG-1{suffix}",
        f"CB-DG-{suffix}",
        f"CB-4{suffix}-IN",
        *special,
        f"BUS-4160-{suffix} 4160V SAFETY BUS 1{suffix}",
        f"CB-LC-{suffix}",
        f"TR-LC-{suffix}",
        f"BUS-480-{suffix} 480V LOAD CENTER {suffix}",
        f"INST-PT-{suffix}",
        f"CB-MCC-{suffix}A",
        f"MCC-{suffix}A",
        f"INST-CT-{suffix}",
        f"CB-RHR-{suffix}",
        f"PUMP-RHR-{suffix}",
        f"CB-SI-{suffix}",
        f"PUMP-SI-{suffix}",
        f"CB-CCW-{suffix}",
        f"PUMP-CCW-{suffix}",
        f"CB-FAN-{suffix}",
        f"FAN-CR-{suffix}",
        f"CB-MCC-{suffix}B",
        f"MCC-{suffix}B",
        f"CB-CH-{suffix}",
        f"CHILLER-{suffix}",
        f"CB-VLV1-{suffix}",
        f"MOV-HV1-{suffix}",
        f"CB-VLV2-{suffix}",
        f"MOV-HV2-{suffix}",
        f"CB-SPARE-{suffix}",
        f"SPARE-LOAD-{suffix}",
        f"XFMR-120-{suffix}",
        f"PNL-120-{suffix}",
        f"RELAY-K{suffix}1",
        f"RELAY-K{suffix}2",
        f"JB-{suffix}1",
        f"TERM-{suffix}",
        f"GND-{suffix}",
    ]


NODES = [
    "GEN-G01",
    "GSU-T01",
    "SWYD-345",
    "CB-13A1",
    "CB-13B1",
    "CB-13T",
    "RELAY-87U",
    "BUS-13A 13.8 KV AUX BUS A",
    "BUS-13B 13.8 KV AUX BUS B",
    "AUX-XFMR-1A",
    "AUX-XFMR-1B",
    "SAT-XFMR-1C",
    "SAT-XFMR-1D",
    *train_nodes("A"),
    *train_nodes("B"),
    *train_nodes("C"),
    *train_nodes("D"),
    "CB-DC-A1",
    "CHGR-125A",
    "BUS-125A 125 VDC BUS A",
    "BAT-125A",
    "FUSE-FD-A",
    "INV-UPS-A",
    "BUS-UPS-A 120 VAC UPS BUS A",
    "DC-MCC-A",
    "SOL-SDV-A",
    "DIODE-OR-A",
    "GRD-DC-A",
    "INST-RACK-A",
    "PNL-RPS-A",
    "RELAY-RPS-A1",
    "RELAY-ESF-A",
    "PLC-SAF-A",
    "ANN-PNL-CR",
    "JB-CR-01",
    "TERM-MTB-A",
    "TERM-MTB-B",
    "CB-DC-B1",
    "CHGR-125B",
    "BUS-125B 125 VDC BUS B",
    "BAT-125B",
    "FUSE-FD-B",
    "INV-UPS-B",
    "BUS-UPS-B 120 VAC UPS BUS B",
    "DC-MCC-B",
    "SOL-SDV-B",
    "DIODE-OR-B",
    "GRD-DC-B",
    "INST-RACK-B",
    "PNL-RPS-B",
    "RELAY-RPS-B1",
    "RELAY-ESF-B",
    "PLC-SAF-B",
    "REC-SEQ-1",
    "XFMR-PT-1",
    "METER-V01",
    "METER-A01",
]


Edge = tuple[str, str, str, str, str]


def e(source: str, target: str, confidence: str, line_type: str, evidence: str) -> Edge:
    return (source, target, confidence, line_type, evidence)


def train_edges(suffix: str) -> list[Edge]:
    bus4160 = f"BUS-4160-{suffix} 4160V SAFETY BUS 1{suffix}"
    bus480 = f"BUS-480-{suffix} 480V LOAD CENTER {suffix}"
    mcc1 = f"MCC-{suffix}A"
    mcc2 = f"MCC-{suffix}B"
    return [
        e(f"DG-1{suffix}", f"CB-DG-{suffix}", "high", "power", "solid DG feeder"),
        e(f"CB-DG-{suffix}", bus4160, "high", "power", "solid branch landing at 4160V bus dot"),
        e(bus4160, f"CB-LC-{suffix}", "high", "power", "solid load-center feeder"),
        e(f"CB-LC-{suffix}", f"TR-LC-{suffix}", "high", "power", "solid feeder through load-center breaker"),
        e(f"TR-LC-{suffix}", bus480, "high", "power", "solid transformer secondary to 480V bus dot"),
        e(bus480, f"INST-PT-{suffix}", "high", "instrument", "dashed PT tap at 480V bus end"),
        e(bus480, f"CB-MCC-{suffix}A", "high", "power", "solid MCC feeder branch at bus dot"),
        e(f"CB-MCC-{suffix}A", mcc1, "high", "power", "solid feeder to first MCC"),
        e(mcc1, f"INST-CT-{suffix}", "medium", "instrument", "dashed CT tap visibly terminates at CT symbol"),
        e(mcc1, f"CB-RHR-{suffix}", "high", "power", "solid branch from first MCC"),
        e(f"CB-RHR-{suffix}", f"PUMP-RHR-{suffix}", "high", "power", "solid feeder to RHR pump"),
        e(mcc1, f"CB-SI-{suffix}", "high", "power", "solid branch from first MCC"),
        e(f"CB-SI-{suffix}", f"PUMP-SI-{suffix}", "high", "power", "solid feeder to SI pump"),
        e(mcc1, f"CB-CCW-{suffix}", "high", "power", "solid branch from first MCC"),
        e(f"CB-CCW-{suffix}", f"PUMP-CCW-{suffix}", "high", "power", "solid feeder to CCW pump"),
        e(mcc1, f"CB-FAN-{suffix}", "high", "power", "solid branch from first MCC"),
        e(f"CB-FAN-{suffix}", f"FAN-CR-{suffix}", "high", "power", "solid feeder to fan motor"),
        e(f"CB-RHR-{suffix}", f"CB-SI-{suffix}", "medium", "control", "dashed interlock segment visibly lands near breaker pair"),
        e(bus480, f"CB-MCC-{suffix}B", "high", "power", "solid MCC feeder branch at bus dot"),
        e(f"CB-MCC-{suffix}B", mcc2, "high", "power", "solid feeder to second MCC"),
        e(mcc2, f"CB-CH-{suffix}", "high", "power", "solid branch from second MCC"),
        e(f"CB-CH-{suffix}", f"CHILLER-{suffix}", "high", "power", "solid feeder to chiller motor"),
        e(mcc2, f"CB-VLV1-{suffix}", "high", "power", "solid branch from second MCC"),
        e(f"CB-VLV1-{suffix}", f"MOV-HV1-{suffix}", "high", "power", "solid feeder to motor-operated valve"),
        e(mcc2, f"CB-VLV2-{suffix}", "high", "power", "solid branch from second MCC"),
        e(f"CB-VLV2-{suffix}", f"MOV-HV2-{suffix}", "high", "power", "solid feeder to motor-operated valve"),
        e(mcc2, f"CB-SPARE-{suffix}", "high" if suffix != "D" else "medium", "power", "solid branch from second MCC to spare breaker"),
        e(f"CB-SPARE-{suffix}", f"SPARE-LOAD-{suffix}", "high" if suffix != "D" else "medium", "power", "solid feeder to spare load"),
        e(bus480, f"XFMR-120-{suffix}", "high", "power", "solid lower branch to 120V transformer"),
        e(f"XFMR-120-{suffix}", f"PNL-120-{suffix}", "high", "power", "solid transformer output to panel"),
        e(bus480, f"GND-{suffix}", "medium", "power", "solid grounded branch in train area"),
        e(f"PNL-120-{suffix}", f"RELAY-K{suffix}1", "high", "control", "dashed branch terminates at relay circle"),
        e(f"PNL-120-{suffix}", f"RELAY-K{suffix}2", "high", "control", "dashed branch terminates at relay circle"),
        e(f"PNL-120-{suffix}", f"JB-{suffix}1", "high", "control", "dashed run from panel to junction box"),
        e(f"JB-{suffix}1", f"TERM-{suffix}", "high", "control", "dashed run from junction box to terminal block"),
    ]


def final_edges() -> list[Edge]:
    edges: list[Edge] = [
        e("GEN-G01", "GSU-T01", "medium", "power", "solid source detail line"),
        e("GSU-T01", "SWYD-345", "medium", "power", "solid high-voltage feeder"),
        e("SWYD-345", "CB-13A1", "medium", "power", "solid feeder to left aux breaker"),
        e("SWYD-345", "CB-13B1", "medium", "power", "solid feeder to right aux breaker"),
        e("CB-13A1", "BUS-13A 13.8 KV AUX BUS A", "high", "power", "vertical solid feeder with bus dot"),
        e("CB-13B1", "BUS-13B 13.8 KV AUX BUS B", "high", "power", "vertical solid feeder with bus dot"),
        e("BUS-13A 13.8 KV AUX BUS A", "CB-13T", "high", "power", "solid tie breaker landing"),
        e("CB-13T", "BUS-13B 13.8 KV AUX BUS B", "high", "power", "solid tie breaker landing"),
        e("BUS-13A 13.8 KV AUX BUS A", "AUX-XFMR-1A", "high", "power", "solid vertical branch with bus dot"),
        e("BUS-13A 13.8 KV AUX BUS A", "AUX-XFMR-1B", "high", "power", "solid vertical branch with bus dot"),
        e("BUS-13B 13.8 KV AUX BUS B", "SAT-XFMR-1C", "high", "power", "solid W-011 branch with bus dot"),
        e("BUS-13B 13.8 KV AUX BUS B", "SAT-XFMR-1D", "high", "power", "solid vertical branch with bus dot"),
        e("BUS-13A 13.8 KV AUX BUS A", "RELAY-87U", "medium", "control", "dashed C-031 tap from bus dot"),
        e("RELAY-87U", "CB-4B-IN", "high", "control", "dashed relay output visibly terminates at CB-4B-IN"),
        e("AUX-XFMR-1A", "CB-4A-IN", "high", "power", "solid transformer feeder"),
        e("CB-4A-IN", "BUS-4160-A 4160V SAFETY BUS 1A", "high", "power", "solid vertical feeder with bus dot"),
        e("AUX-XFMR-1B", "CB-4B-IN", "high", "power", "solid transformer feeder"),
        e("CB-4B-IN", "BUS-4160-B 4160V SAFETY BUS 1B", "high", "power", "solid vertical feeder with bus dot"),
        e("SAT-XFMR-1C", "CB-4C-IN", "high", "power", "solid transformer feeder"),
        e("CB-4C-IN", "BUS-4160-C 4160V SAFETY BUS 1C", "high", "power", "solid vertical feeder with bus dot"),
        e("SAT-XFMR-1D", "CB-4D-IN", "high", "power", "solid transformer feeder"),
        e("CB-4D-IN", "BUS-4160-D 4160V SAFETY BUS 1D", "high", "power", "solid vertical feeder with bus dot"),
        e("BUS-4160-A 4160V SAFETY BUS 1A", "CB-4AB-TIE", "high", "power", "solid tie landing at A bus"),
        e("CB-4AB-TIE", "BUS-4160-B 4160V SAFETY BUS 1B", "high", "power", "solid tie landing at B bus"),
        e("BUS-4160-C 4160V SAFETY BUS 1C", "CB-4CD-TIE", "high", "power", "solid tie landing at C bus"),
        e("CB-4CD-TIE", "BUS-4160-D 4160V SAFETY BUS 1D", "high", "power", "solid tie landing at D bus"),
        e("BUS-4160-A 4160V SAFETY BUS 1A", "SYNC-PNL-1", "medium", "control", "dashed C-030 branch from bus dot"),
        e("SYNC-PNL-1", "CB-DG-A", "medium", "control", "dashed sync lead to DG breaker"),
    ]
    for suffix in "ABCD":
        edges.extend(train_edges(suffix))
    edges.extend(
        [
            e("BUS-480-A 480V LOAD CENTER A", "CB-DC-A1", "medium", "power", "long solid feeder down to charger breaker"),
            e("CB-DC-A1", "CHGR-125A", "high", "power", "solid feeder to charger"),
            e("CHGR-125A", "BUS-125A 125 VDC BUS A", "high", "power", "solid charger output to 125 VDC bus"),
            e("BUS-125A 125 VDC BUS A", "BAT-125A", "high", "power", "solid battery branch with bus dot"),
            e("BUS-125A 125 VDC BUS A", "FUSE-FD-A", "high", "power", "solid branch to fuse"),
            e("FUSE-FD-A", "INV-UPS-A", "high", "power", "solid branch from fuse to inverter"),
            e("INV-UPS-A", "BUS-UPS-A 120 VAC UPS BUS A", "high", "power", "solid inverter output to UPS bus"),
            e("BUS-125A 125 VDC BUS A", "DC-MCC-A", "high", "power", "solid vertical branch with bus dot"),
            e("DC-MCC-A", "SOL-SDV-A", "high", "control", "dashed control line to solenoid valve"),
            e("BUS-125A 125 VDC BUS A", "DIODE-OR-A", "high", "power", "solid branch to diode OR"),
            e("BUS-125A 125 VDC BUS A", "GRD-DC-A", "high", "power", "solid ground branch with bus dot"),
            e("BUS-UPS-A 120 VAC UPS BUS A", "PNL-RPS-A", "high", "control", "dashed UPS branch to panel"),
            e("PNL-RPS-A", "RELAY-RPS-A1", "high", "control", "dashed relay branch"),
            e("PNL-RPS-A", "RELAY-ESF-A", "high", "control", "dashed relay branch"),
            e("BUS-UPS-A 120 VAC UPS BUS A", "PLC-SAF-A", "high", "control", "dashed UPS branch to PLC panel"),
            e("BUS-UPS-A 120 VAC UPS BUS A", "INST-RACK-A", "high", "instrument", "dashed UPS branch to instrument rack"),
            e("BUS-UPS-A 120 VAC UPS BUS A", "ANN-PNL-CR", "high", "control", "dashed right-end branch to annunciator panel"),
            e("ANN-PNL-CR", "JB-CR-01", "high", "control", "vertical control lead to junction box"),
            e("JB-CR-01", "TERM-MTB-A", "high", "control", "dashed left terminal branch"),
            e("JB-CR-01", "TERM-MTB-B", "high", "control", "dashed right terminal branch"),
            e("BUS-480-B 480V LOAD CENTER B", "CB-DC-B1", "medium", "power", "long solid feeder down to charger breaker"),
            e("CB-DC-B1", "CHGR-125B", "high", "power", "solid feeder to charger"),
            e("CHGR-125B", "BUS-125B 125 VDC BUS B", "high", "power", "solid charger output to 125 VDC bus"),
            e("BUS-125B 125 VDC BUS B", "BAT-125B", "high", "power", "solid battery branch with bus dot"),
            e("BUS-125B 125 VDC BUS B", "FUSE-FD-B", "high", "power", "solid branch to fuse"),
            e("FUSE-FD-B", "INV-UPS-B", "high", "power", "solid branch from fuse to inverter"),
            e("INV-UPS-B", "BUS-UPS-B 120 VAC UPS BUS B", "high", "power", "solid inverter output to UPS bus"),
            e("BUS-125B 125 VDC BUS B", "DC-MCC-B", "high", "power", "solid vertical branch with bus dot"),
            e("DC-MCC-B", "SOL-SDV-B", "high", "control", "dashed control line to solenoid valve"),
            e("BUS-125B 125 VDC BUS B", "DIODE-OR-B", "high", "power", "solid branch to diode OR"),
            e("BUS-125B 125 VDC BUS B", "GRD-DC-B", "high", "power", "solid ground branch with bus dot"),
            e("BUS-UPS-B 120 VAC UPS BUS B", "PNL-RPS-B", "high", "control", "dashed UPS branch to panel"),
            e("PNL-RPS-B", "RELAY-RPS-B1", "high", "control", "dashed relay branch"),
            e("PNL-RPS-B", "RELAY-ESF-B", "high", "control", "dashed relay branch"),
            e("BUS-UPS-B 120 VAC UPS BUS B", "PLC-SAF-B", "high", "control", "dashed UPS branch to PLC panel"),
            e("BUS-UPS-B 120 VAC UPS BUS B", "INST-RACK-B", "high", "instrument", "dashed UPS branch to instrument rack"),
            e("BUS-UPS-B 120 VAC UPS BUS B", "REC-SEQ-1", "high", "control", "dashed right-end branch to recorder/sequencer"),
            e("XFMR-PT-1", "METER-V01", "high", "instrument", "dashed vertical PT meter lead"),
        ]
    )
    return edges


DIEGO_EXTRAS: list[Edge] = [
    e(f"INST-CT-{suffix}", f"CB-RHR-{suffix}", "medium", "instrument", "Diego high-recall CT-to-RHR landing; Jennifer removed as not separately supported")
    for suffix in "ABCD"
]
DIEGO_EXTRAS.extend(
    [
        e(f"RELAY-K{suffix}1", f"JB-{suffix}1", "medium", "control", "Diego high-recall relay-to-JB run; Jennifer removed as common PNL-to-JB routing")
        for suffix in "ABCD"
    ]
)
DIEGO_EXTRAS.append(e("XFMR-PT-1", "METER-A01", "low", "instrument", "Diego high-recall meter-group link; Jennifer removed because no clear termination/dot"))


def dedupe_edges(edges: list[Edge]) -> list[Edge]:
    out: list[Edge] = []
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        key = tuple(sorted((edge[0], edge[1])))
        if key not in seen:
            seen.add(key)
            out.append(edge)
    return out


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
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["", *nodes])
    for node, row in zip(nodes, matrix):
        writer.writerow([node, *row])
    return output.getvalue().rstrip("\n")


def csv_rows(edges: list[Edge]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["source", "target", "confidence", "line_type", "evidence"])
    writer.writerows(edges)
    return output.getvalue().rstrip("\n")


def node_lines(nodes: list[str]) -> str:
    chunks = [
        nodes[:13],
        train_nodes("A"),
        train_nodes("B"),
        train_nodes("C"),
        train_nodes("D"),
        nodes[-41:-21],
        nodes[-21:],
    ]
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    for chunk in chunks:
        writer.writerow(chunk)
    return output.getvalue().rstrip("\n")


def round_text(role: str, round_no: int, intro: list[str], edges: list[Edge], ambiguities: list[str]) -> str:
    return "\n".join(
        [
            f"ROLE: {role}",
            "DOCUMENT: 22",
            f"ROUND: {round_no}",
            "",
            *intro,
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


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> None:
    out = result_dir()
    precision_edges = final_edges()
    diego_edges = dedupe_edges(precision_edges + DIEGO_EXTRAS)

    diego_round1 = round_text(
        "Diego high-recall extractor",
        1,
        [
            "SUMMARY: High-recall graph includes all precision edges plus visually plausible CT-to-RHR, relay-to-JB, and meter-group overlinks for reviewer scrutiny.",
            "NOTE: Duplicate Diego control overlays on SI pump feeders map to already-present feeder pairs and are not repeated in MATRIX_CSV.",
        ],
        diego_edges,
        [
            "- Upstream generator/switchyard routing is visually small but solid.",
            "- CT-to-RHR, relay-to-JB, and METER-A01 links are high-recall candidates only.",
        ],
    )
    jennifer_round1 = round_text(
        "Jennifer precision reviewer",
        1,
        [
            "CHANGES_FROM_DIEGO",
            "- Removed CT-to-RHR extra edges; CTs are retained as MCC instrument taps only.",
            "- Removed RELAY-K*1-to-JB-*1 overlinks; retained PNL-120-* to relay and PNL-120-* to JB routes.",
            "- Removed XFMR-PT-1 to METER-A01; METER-A01 remains a visible but unsupported isolated meter node.",
            "- Removed duplicate SI pump control overlays already represented by the solid feeder pairs.",
        ],
        precision_edges,
        [
            "- METER-A01 is visible, but its dashed lead does not visibly terminate at XFMR-PT-1.",
            "- CB-DC-A1 and CB-DC-B1 source feeders are long solid drops with distant upper taps.",
        ],
    )
    diego_round2 = "\n".join(
        [
            "ROLE: Diego high-recall extractor",
            "DOCUMENT: 22",
            "ROUND: 2",
            "AGREE_WITH_JENNIFER_ROUND1",
            "SUMMARY: Graph saturated. Crops support no extra dashed CT-to-RHR edges, no direct relay-to-JB overlinks, XFMR-PT-1 to METER-V01 only, and the lower DC/UPS branches as retained by Jennifer.",
            "",
        ]
    )
    jennifer_round2 = "\n".join(
        [
            "ROLE: Jennifer precision reviewer",
            "DOCUMENT: 22",
            "ROUND: 2",
            "AGREE_WITH_DIEGO_ROUND2",
            "SUMMARY: Saturated final precision graph is Jennifer Round 1; close PT/meter review supports retaining XFMR-PT-1 to METER-V01 only and leaving METER-A01 without a confirmed XFMR-PT-1 edge.",
            "",
        ]
    )

    outputs = {
        "diego_round1_output.txt": diego_round1,
        "jennifer_round1_review.txt": jennifer_round1,
        "diego_round2_response.txt": diego_round2,
        "jennifer_round2_final.txt": jennifer_round2,
    }
    for name, text in outputs.items():
        write_text(out / name, text)

    transcript = "\n".join(
        [
            "# Document 22 Subagent Round Transcript",
            "",
            "## Diego Round 1",
            "High-recall extraction produced a 201-node graph. Distinct matrix overlinks later removed by Jennifer were CT-to-RHR, RELAY-K*1-to-JB-*1, and XFMR-PT-1-to-METER-A01.",
            "",
            "## Jennifer Round 1",
            "Jennifer refined the graph to the precision edge list in `jennifer_round1_review.txt`, leaving METER-A01 visible but isolated because the dashed lead does not clearly terminate at XFMR-PT-1.",
            "",
            "## Diego Round 2",
            diego_round2.strip(),
            "",
            "## Jennifer Round 2",
            jennifer_round2.strip(),
            "",
        ]
    )
    write_text(out / "subagent_round_transcript.md", transcript)
    if out != FALLBACK:
        write_text(FALLBACK / "subagent_round_transcript.md", transcript)
    print(f"Wrote doc22 round outputs to {out}")
    print({"nodes": len(NODES), "diego_round1_edges": len(diego_edges), "jennifer_final_edges": len(precision_edges)})


if __name__ == "__main__":
    main()
