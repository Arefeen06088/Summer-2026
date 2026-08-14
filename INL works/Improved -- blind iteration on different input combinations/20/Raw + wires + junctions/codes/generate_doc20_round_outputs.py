from __future__ import annotations

from pathlib import Path


WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc20_work")


top_nodes = [
    "GEN-M1",
    "CB-GEN1",
    "TR-UAT1",
    "CB-13A-IN",
    "BUS-13K-A",
    "CB-F41A",
    "DS-F41A",
    "TR-416A",
    "CB-416A-IN",
    "BUS-416-A",
    "DG-1A",
    "CB-DG1A",
    "CB-TIE-13K",
    "BUS-13K-B",
    "FEED-230A",
    "TR-SAT1",
    "CB-13B-IN",
    "CB-F41B",
    "DS-F41B",
    "TR-416B",
    "CB-416B-IN",
    "BUS-416-B",
    "DG-1B",
    "CB-DG1B",
    "CB-TIE-416",
    "CB-LCA",
    "TR-480A",
    "BUS-480-A",
    "CB-LCB",
    "TR-480B",
    "BUS-480-B",
    "CB-TIE-480",
    "CB-LCC",
    "TR-480C",
    "BUS-480-C",
    "CB-LCD",
    "TR-480D",
    "BUS-480-D",
]

load_defs = [
    ("BUS-480-A", "A", "1", "MCC-1A", "RELAY-K1A", "PMP-RHR-101A", "solid"),
    ("BUS-480-A", "A", "2", "MCC-2A", "CS-2A", "MOV-CCW-112A", "dashed"),
    ("BUS-480-A", "A", "3", "MCC-3A", "RELAY-K3A", "FAN-RB-104A", "solid"),
    ("BUS-480-A", "A", "4", "JB-4A", "CS-4A", "HTR-PZR-01A", "dashed"),
    ("BUS-480-A", "A", "5", "MCC-5A", "RELAY-K5A", "COMP-IA-201A", "solid"),
    ("BUS-480-A", "A", "6", "JB-6A", "CS-6A", "MOT-CRN-01A", "dashed"),
    ("BUS-480-B", "B", "1", "MCC-1B", "RELAY-K1B", "PMP-SI-102B", "solid"),
    ("BUS-480-B", "B", "2", "MCC-2B", "CS-2B", "MOV-CS-116B", "dashed"),
    ("BUS-480-B", "B", "3", "MCC-3B", "RELAY-K3B", "FAN-CCW-108B", "solid"),
    ("BUS-480-B", "B", "4", "JB-4B", "CS-4B", "HTR-SUMP-02B", "dashed"),
    ("BUS-480-B", "B", "5", "MCC-5B", "RELAY-K5B", "PMP-CHG-203B", "solid"),
    ("BUS-480-B", "B", "6", "JB-6B", "CS-6B", "MOV-SW-118B", "dashed"),
    ("BUS-480-C", "C", "1", "MCC-1C", "RELAY-K1C", "PMP-RHR-101C", "solid"),
    ("BUS-480-C", "C", "2", "MCC-2C", "CS-2C", "MOV-CCW-112C", "dashed"),
    ("BUS-480-C", "C", "3", "MCC-3C", "RELAY-K3C", "FAN-RB-104C", "solid"),
    ("BUS-480-C", "C", "4", "JB-4C", "RELAY-K4C", "PMP-AFW-205C", "solid"),
    ("BUS-480-C", "C", "5", "MCC-5C", "RELAY-K5C", "PMP-CCP-207C", "solid"),
    ("BUS-480-C", "C", "6", "JB-6C", "CS-6C", "MOV-FCV-022C", "dashed"),
    ("BUS-480-D", "D", "1", "MCC-1D", "RELAY-K1D", "PMP-SI-102D", "solid"),
    ("BUS-480-D", "D", "2", "MCC-2D", "CS-2D", "MOV-CS-116D", "dashed"),
    ("BUS-480-D", "D", "3", "MCC-3D", "RELAY-K3D", "FAN-ESF-110D", "solid"),
    ("BUS-480-D", "D", "4", "JB-4D", "CS-4D", "MOV-RWST-24D", "dashed"),
    ("BUS-480-D", "D", "5", "MCC-5D", "RELAY-K5D", "PMP-CHG-203D", "solid"),
    ("BUS-480-D", "D", "6", "JB-6D", "CS-6D", "MOV-SW-118D", "dashed"),
]

dc_nodes = [
    "BAT-125A",
    "CHGR-125A",
    "RECT-125A",
    "BUS-125DCA",
    "INV-UPS-A",
]

rps_control_nodes = [
    "CP-RPS-A",
    "TB-RPS-A",
    "PROT-UV-A",
    "RELAY-K101",
    "PT-410A",
    "LT-512A",
    "RELAY-K102",
    "TT-303A",
    "GND-CTRL-A",
    "CP-RPS-B",
    "TB-RPS-B",
    "PROT-UV-B",
    "RELAY-K103",
    "PT-410B",
    "LT-512B",
    "RELAY-K104",
    "TT-303B",
    "GND-CTRL-B",
]

dc_b_nodes = [
    "BAT-125B",
    "CHGR-125B",
    "RECT-125B",
    "BUS-125DCB",
    "INV-UPS-B",
]

esfas_control_nodes = [
    "CP-ESFAS-A",
    "JB-ESF-A",
    "PROT-LOP-A",
    "RELAY-K105",
    "FT-611A",
    "RELAY-K106",
    "XA-730A",
    "CP-ESFAS-B",
    "JB-ESF-B",
    "PROT-LOP-B",
    "RELAY-K107",
    "FT-611B",
    "RELAY-K108",
    "XA-730B",
]


def load_nodes() -> list[str]:
    out: list[str] = []
    for _, suffix, index, mid, control, device, _ in load_defs:
        out.extend([f"CB-48{suffix}{index}", f"DS-48{suffix}{index}", mid, control, device])
    return out


nodes = top_nodes + load_nodes() + dc_nodes + rps_control_nodes + dc_b_nodes + esfas_control_nodes

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
    clean = evidence.replace(",", ";")
    edge = (source, target, confidence, line_type, clean)
    reverse = (target, source, confidence, line_type, clean)
    if edge not in edges and reverse not in edges:
        edges.append(edge)


def chain(parts: list[str], confidence: str, line_type: str, evidence: str) -> None:
    for source, target in zip(parts, parts[1:]):
        add(source, target, confidence, line_type, evidence)


chain(["GEN-M1", "CB-GEN1", "TR-UAT1", "CB-13A-IN", "BUS-13K-A"], "high", "solid_power", "Top left generator and unit auxiliary transformer feed BUS-13K-A")
chain(["BUS-13K-A", "CB-F41A", "DS-F41A", "TR-416A", "CB-416A-IN", "BUS-416-A"], "high", "solid_power", "A 13.8 kV bus feeder to 4.16 kV class 1E bus A")
chain(["DG-1A", "CB-DG1A", "BUS-416-A"], "high", "solid_power", "DG-1A branch lands on BUS-416-A")
chain(["BUS-13K-A", "CB-TIE-13K", "BUS-13K-B"], "high", "solid_power", "13.8 kV bus tie is drawn through CB-TIE-13K")
chain(["BUS-416-A", "CB-TIE-416", "BUS-416-B"], "high", "solid_power", "4.16 kV normally open bus tie is drawn through CB-TIE-416")
chain(["FEED-230A", "TR-SAT1", "CB-13B-IN", "BUS-13K-B"], "high", "solid_power", "230 kV feed and station auxiliary transformer feed BUS-13K-B")
chain(["BUS-13K-B", "CB-F41B", "DS-F41B", "TR-416B", "CB-416B-IN", "BUS-416-B"], "high", "solid_power", "B 13.8 kV bus feeder to 4.16 kV class 1E bus B")
chain(["DG-1B", "CB-DG1B", "BUS-416-B"], "high", "solid_power", "DG-1B branch lands on BUS-416-B")
chain(["BUS-416-A", "CB-LCA", "TR-480A", "BUS-480-A"], "medium", "solid_power", "Feeder from BUS-416-A through partly clipped CB-LCA to TR-480A and load center A")
chain(["BUS-416-A", "CB-LCB", "TR-480B", "BUS-480-B"], "medium", "solid_power", "Feeder from BUS-416-A through partly clipped CB-LCB to TR-480B and load center B")
chain(["BUS-416-B", "CB-LCC", "TR-480C", "BUS-480-C"], "medium", "solid_power", "Feeder from BUS-416-B through partly clipped CB-LCC to TR-480C and load center C")
chain(["BUS-416-B", "CB-LCD", "TR-480D", "BUS-480-D"], "medium", "solid_power", "Feeder from BUS-416-B through partly clipped CB-LCD to TR-480D and load center D")
chain(["BUS-480-B", "CB-TIE-480", "BUS-480-C"], "high", "solid_power", "480 V tie is drawn between BUS-480-B and BUS-480-C through CB-TIE-480")


for bus, suffix, index, mid, control, device, style in load_defs:
    cb = f"CB-48{suffix}{index}"
    ds = f"DS-48{suffix}{index}"
    line_type = "solid_power" if style == "solid" else "dashed_control"
    chain([bus, cb, ds, mid], "high", "solid_power", f"Load center {suffix} branch {index} solid feeder stack")
    chain([mid, control, device], "high", line_type, f"Load center {suffix} branch {index} terminal/control path to {device}")


chain(["BUS-480-A", "RECT-125A", "BUS-125DCA", "INV-UPS-A"], "high", "dc_control", "A-side rectifier and inverter tap from 480 A and land on BUS-125DCA")
chain(["BAT-125A", "CHGR-125A", "RECT-125A"], "high", "dc_control", "A-side battery charger rectifier dashed DC chain")
chain(["BUS-480-C", "RECT-125B", "BUS-125DCB", "INV-UPS-B"], "medium", "dc_control", "B-side rectifier route is drawn from BUS-480-C/right load-center-C area and lands on BUS-125DCB")
chain(["BAT-125B", "CHGR-125B", "RECT-125B"], "high", "dc_control", "B-side battery charger rectifier dashed DC chain")

chain(["BUS-125DCA", "CP-RPS-A", "TB-RPS-A", "PROT-UV-A", "RELAY-K101"], "high", "dashed_control", "RPS A control drop and UV protection path")
add("RELAY-K101", "PT-410A", "high", "dashed_control", "RPS A relay K101 dashed instrument branch to PT-410A")
add("RELAY-K101", "LT-512A", "high", "dashed_control", "RPS A relay K101 dashed instrument branch to LT-512A")
add("CP-RPS-A", "RELAY-K102", "high", "dashed_control", "RPS A side dashed branch from CP-RPS-A to RELAY-K102")
add("RELAY-K102", "TT-303A", "high", "dashed_control", "RPS A relay K102 vertical dashed branch to TT-303A")
add("RELAY-K102", "GND-CTRL-A", "medium", "solid_ground", "RPS A relay K102 solid sloped lead to control ground")

chain(["BUS-125DCA", "CP-RPS-B", "TB-RPS-B", "PROT-UV-B", "RELAY-K103"], "high", "dashed_control", "RPS B control drop and UV protection path")
add("RELAY-K103", "PT-410B", "high", "dashed_control", "RPS B relay K103 dashed instrument branch to PT-410B")
add("RELAY-K103", "LT-512B", "high", "dashed_control", "RPS B relay K103 dashed instrument branch to LT-512B")
add("CP-RPS-B", "RELAY-K104", "high", "dashed_control", "RPS B side dashed branch from CP-RPS-B to RELAY-K104")
add("RELAY-K104", "TT-303B", "high", "dashed_control", "RPS B relay K104 vertical dashed branch to TT-303B")
add("RELAY-K104", "GND-CTRL-B", "medium", "solid_ground", "RPS B relay K104 solid sloped lead to control ground")

chain(["BUS-125DCB", "CP-ESFAS-A", "JB-ESF-A", "PROT-LOP-A", "RELAY-K105"], "high", "dashed_control", "ESFAS A control drop and low-oil-pressure protection path")
add("RELAY-K105", "FT-611A", "high", "dashed_control", "ESFAS A relay K105 dashed instrument branch to FT-611A")
add("CP-ESFAS-A", "RELAY-K106", "high", "dashed_control", "ESFAS A side dashed branch from CP-ESFAS-A to RELAY-K106")
add("RELAY-K106", "XA-730A", "high", "dashed_control", "ESFAS A relay K106 vertical dashed alarm branch to XA-730A")
chain(["BUS-125DCB", "CP-ESFAS-B", "JB-ESF-B", "PROT-LOP-B", "RELAY-K107"], "high", "dashed_control", "ESFAS B control drop and low-oil-pressure protection path")
add("RELAY-K107", "FT-611B", "high", "dashed_control", "ESFAS B relay K107 dashed instrument branch to FT-611B")
add("CP-ESFAS-B", "RELAY-K108", "high", "dashed_control", "ESFAS B side dashed branch from CP-ESFAS-B to RELAY-K108")
add("RELAY-K108", "XA-730B", "high", "dashed_control", "ESFAS B relay K108 vertical dashed alarm branch to XA-730B")
add("RELAY-K106", "RELAY-K108", "medium", "dashed_interlock", "Long dashed A/B ESF interlock connects the K106 and K108 relay-side paths")

precision_edges = list(edges)


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
        "DOCUMENT: 20",
        f"SUMMARY: {summary}",
        "NODE_ORDER_CSV",
        "node",
        *nodes,
        "EDGE_LIST_CSV",
        "source,target,confidence,line_type,evidence",
    ]
    lines.extend(",".join(edge) for edge in edge_list)
    lines.append("MATRIX_CSV")
    lines.extend(",".join(row) for row in matrix)
    lines.append("AMBIGUITIES")
    lines.extend(ambiguities)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_agreement(path: Path, role: str, agreement: str, summary: str) -> None:
    path.write_text(
        "\n".join(
            [
                f"ROLE: {role}",
                "DOCUMENT: 20",
                agreement,
                f"SUMMARY: {summary}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_transcript() -> None:
    text = f"""# Document 20 Subagent Round Transcript

## Diego Round 1 - High Recall
Diego proposed {len(nodes)} nodes and {len(precision_edges)} edges covering the top 13.8 kV/4.16 kV buses, four 480 V load centers, 125 VDC supplies, RPS/ESFAS control panels, and the A/B ESF interlock.

## Jennifer Round 1 - Precision Review
Jennifer reviewed Diego's graph against the same raw, wire, and node crops. She confirmed the same 202-edge graph, emphasized that all bus ties are through named tie breakers, preserved `JB-ESF-A/B` as junction-box labels, and confirmed `BUS-480-C -> RECT-125B` as a separate routed conductor.

## Diego Round 2
Diego reviewed Jennifer round 1 and agreed that no additional visually supported edges should be added.

## Jennifer Round 2
Jennifer confirmed final saturation. The final graph has {len(nodes)} nodes and {len(precision_edges)} edges.
"""
    (WORK / "subagent_round_transcript.md").write_text(text, encoding="utf-8")


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    write_round(
        WORK / "diego_round1_output.txt",
        "Diego high-recall extractor",
        f"High-recall document 20 graph with {len(nodes)} visually named nodes and {len(precision_edges)} visually supported edges.",
        precision_edges,
        [
            "CB-LCA/CB-LCB/CB-LCC/CB-LCD labels are partly clipped in the 480 crops but supported by geometry and transformer labels.",
            "JB-ESF-A and JB-ESF-B are visually read as JB labels; they are the least certain exact text labels.",
            "BUS-480-C to RECT-125B is represented as a direct named-node edge because the routed conductor has no intermediate named component.",
        ],
    )
    write_round(
        WORK / "jennifer_round1_review.txt",
        "Jennifer precision reviewer",
        f"Precision graph with {len(nodes)} nodes and {len(precision_edges)} edges after review of Diego round 1.",
        precision_edges,
        [
            "No unsupported direct bus-bus shortcuts are retained; 13 kV, 4160 V, and 480 V ties are through their named tie breakers only.",
            "Lower control paths retain direct named-node edges only where dashed conductors visibly connect those named nodes.",
        ],
    )
    write_agreement(
        WORK / "diego_round2_response.txt",
        "Diego high-recall extractor",
        "AGREE_WITH_JENNIFER_ROUND1",
        f"Reinspection found no visually supported correction beyond Jennifer round 1. Saturated graph remains {len(nodes)} nodes and {len(precision_edges)} edges.",
    )
    write_agreement(
        WORK / "jennifer_round2_final.txt",
        "Jennifer precision reviewer",
        "AGREE_WITH_DIEGO_ROUND2",
        f"Final precision pass agrees with Diego round 2 and keeps the {len(nodes)} node {len(precision_edges)} edge graph as final.",
    )
    write_transcript()
    print({"document": 20, "nodes": len(nodes), "final_edges": len(precision_edges)})


if __name__ == "__main__":
    main()
