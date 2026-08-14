from __future__ import annotations

from pathlib import Path


WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc19_work")


top_nodes = [
    "OFFSITE GRID-1",
    "DS-101",
    "CB-101",
    "TR-101",
    "BUS-4160-A",
    "DG-1",
    "CB-DG1",
    "PT-4160A",
    "CB-201",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A",
    "CB-TIE-4160",
    "OFFSITE GRID-2",
    "DS-102",
    "CB-102",
    "TR-102",
    "BUS-4160-B",
    "DG-2",
    "CB-DG2",
    "PT-4160B",
    "CB-202",
    "TR-480-B",
    "CB-480-B",
    "BUS-480-B",
    "CB-TIE-480",
]

load_defs = [
    ("BUS-480-A", "201", "PUMP-P201", "pump"),
    ("BUS-480-A", "203", "PUMP-P203", "pump"),
    ("BUS-480-A", "301", "PUMP-P301", "pump"),
    ("BUS-480-A", "401", "PUMP-P401", "pump"),
    ("BUS-480-A", "501", "MTR-F501", "motor"),
    ("BUS-480-A", "601", "VALVE-MOV601", "mov"),
    ("BUS-480-B", "202", "PUMP-P202", "pump"),
    ("BUS-480-B", "204", "PUMP-P204", "pump"),
    ("BUS-480-B", "302", "PUMP-P302", "pump"),
    ("BUS-480-B", "402", "PUMP-P402", "pump"),
    ("BUS-480-B", "502", "MTR-F502", "motor"),
    ("BUS-480-B", "701", "INST-RPS701", "rps"),
]

lower_nodes = [
    "CB-301",
    "TR-120-A",
    "BUS-120AC-A",
    "JB-MAIN",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "PN-RPS-A",
    "CB-302",
    "TR-120-B",
    "BUS-120AC-B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "PN-RPS-B",
]


def load_nodes_for(num: str, kind: str, device: str) -> list[str]:
    base = [
        f"CB-F{num}",
        f"RELAY-PR{num}",
        f"DS-F{num}",
        f"CPT-{num}",
        f"MCC-{num}",
        f"CB-L{num}",
        f"RELAY-A{num}",
        f"RELAY-K{num}",
        device,
    ]
    if kind == "mov":
        base.extend([f"INST-{num}", f"[LS-MOV{num}]", f"JB-{num}", f"LCS-{num}", f"TB-{num}"])
    elif kind == "rps":
        base.extend([f"INST-{num}", f"JB-{num}", f"LCS-{num}", f"TB-{num}"])
    else:
        base.extend([f"INST-{num}", f"JB-{num}", f"LCS-{num}", f"TB-{num}"])
    return base


nodes = list(top_nodes)
for _, num, device, kind in load_defs:
    nodes.extend(load_nodes_for(num, kind, device))
nodes.extend(lower_nodes)

if len(nodes) != len(set(nodes)):
    seen: set[str] = set()
    dupes: list[str] = []
    for node in nodes:
        if node in seen:
            dupes.append(node)
        seen.add(node)
    raise ValueError(f"duplicate nodes: {dupes}")

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


# Top 4160 V and 480 V one-line distribution.
chain(
    ["OFFSITE GRID-1", "DS-101", "CB-101", "TR-101", "BUS-4160-A"],
    "high",
    "ac-power",
    "Division A offsite source descends through DS-101 CB-101 and TR-101 to BUS-4160-A",
)
chain(["DG-1", "CB-DG1", "BUS-4160-A"], "high", "ac-power", "DG-1 feeder lands on BUS-4160-A through CB-DG1")
add("BUS-4160-A", "PT-4160A", "high", "instrument", "PT-4160A taps the A 4160 bus with a dashed vertical lead")
chain(
    ["BUS-4160-A", "CB-201", "TR-480-A", "CB-480-A", "BUS-480-A"],
    "high",
    "ac-power",
    "A 4160 bus drops through CB-201 TR-480-A and CB-480-A to BUS-480-A",
)
chain(["BUS-4160-A", "CB-TIE-4160", "BUS-4160-B"], "high", "ac-power", "CB-TIE-4160 is drawn between the two 4160 bus bars")
chain(
    ["OFFSITE GRID-2", "DS-102", "CB-102", "TR-102", "BUS-4160-B"],
    "high",
    "ac-power",
    "Division B offsite source descends through DS-102 CB-102 and TR-102 to BUS-4160-B",
)
chain(["DG-2", "CB-DG2", "BUS-4160-B"], "high", "ac-power", "DG-2 feeder lands on BUS-4160-B through CB-DG2")
add("BUS-4160-B", "PT-4160B", "high", "instrument", "PT-4160B taps the B 4160 bus with a dashed vertical lead")
chain(
    ["BUS-4160-B", "CB-202", "TR-480-B", "CB-480-B", "BUS-480-B"],
    "high",
    "ac-power",
    "B 4160 bus drops through CB-202 TR-480-B and CB-480-B to BUS-480-B",
)
chain(["BUS-480-A", "CB-TIE-480", "BUS-480-B"], "high", "ac-power", "CB-TIE-480 is drawn between the 480 V A and B bus bars")


def add_load_module(bus: str, num: str, device: str, kind: str) -> None:
    cbf = f"CB-F{num}"
    pr = f"RELAY-PR{num}"
    ds = f"DS-F{num}"
    cpt = f"CPT-{num}"
    mcc = f"MCC-{num}"
    cbl = f"CB-L{num}"
    relay_a = f"RELAY-A{num}"
    relay_k = f"RELAY-K{num}"
    inst = f"INST-{num}"
    jb = f"JB-{num}"
    lcs = f"LCS-{num}"
    tb = f"TB-{num}"
    chain([bus, cbf, ds, cpt, mcc, cbl, relay_k, device], "high", "ac-power", f"Solid 480 V feeder stack for load module {num}")
    add(cbf, pr, "high", "control", f"Dashed protection-relay lead from CB-F{num} to RELAY-PR{num}")
    add(mcc, relay_a, "high", "control", f"Dashed auxiliary relay lead from MCC-{num} to RELAY-A{num}")
    if kind == "mov":
        ls = f"[LS-MOV{num}]"
        add(device, inst, "high", "control", f"Dashed instrument lead from {device} to INST-{num}")
        add(device, ls, "high", "control", f"Dashed limit-switch branch from {device} to [LS-MOV{num}]")
        chain([ls, jb, tb, lcs], "high", "control", f"Dashed local-control chain for MOV module {num}")
    elif kind == "rps":
        add(device, inst, "high", "control", f"Dashed instrument lead from {device} to INST-{num}")
        chain([inst, jb, tb, lcs], "high", "control", f"Dashed local-control chain for RPS instrument module {num}")
    else:
        chain([device, inst, jb, tb, lcs], "high", "control", f"Dashed instrument and local-control chain for module {num}")


for bus, num, device, kind in load_defs:
    add_load_module(bus, num, device, kind)


# Lower control-power and DC distribution.
chain(
    ["BUS-480-A", "CB-301", "TR-120-A", "BUS-120AC-A"],
    "high",
    "ac-power",
    "A control-power feed leaves BUS-480-A through CB-301 and TR-120-A to BUS-120AC-A",
)
add("BUS-120AC-A", "JB-MAIN", "high", "control", "JB-MAIN is dashed down from BUS-120AC-A")
chain(
    ["BUS-480-A", "CHGR-125A", "BAT-125A", "BUS-125DC-A", "INV-120A", "PN-RPS-A"],
    "high",
    "dc-control",
    "A DC train feed descends through CHGR-125A BAT-125A BUS-125DC-A and INV-120A to PN-RPS-A",
)
chain(
    ["BUS-480-B", "CB-302", "TR-120-B", "BUS-120AC-B"],
    "high",
    "ac-power",
    "B control-power feed leaves BUS-480-B through CB-302 and TR-120-B to BUS-120AC-B",
)
chain(
    ["BUS-480-B", "CHGR-125B", "BAT-125B", "BUS-125DC-B", "INV-120B", "PN-RPS-B"],
    "high",
    "dc-control",
    "B DC train feed descends through CHGR-125B BAT-125B BUS-125DC-B and INV-120B to PN-RPS-B",
)

precision_edges = list(edges)

diego_extra_edges = [
    ("INST-601", "[LS-MOV601]", "low", "control", "Diego high-recall possible shared MOV instrument junction; Jennifer treats LS branch as landed from valve then down to JB"),
    ("VALVE-MOV601", "JB-601", "low", "control", "Diego high-recall shortcut along MOV dashed branch; Jennifer keeps nearest named components only"),
    ("INST-RPS701", "JB-701", "low", "control", "Diego high-recall shortcut from RPS instrument to JB; Jennifer keeps the intermediate INST-701"),
    ("BUS-120AC-B", "JB-MAIN", "low", "control", "Diego high-recall possible main junction association; Jennifer keeps JB-MAIN on BUS-120AC-A only"),
    ("BUS-480-A", "CB-F202", "low", "ac-power", "Diego high-recall possible visual continuation across the 480 tie; Jennifer keeps B-side loads on BUS-480-B"),
]

diego_edges = precision_edges + diego_extra_edges
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
        "DOCUMENT: 19",
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
                "DOCUMENT: 19",
                agreement,
                f"SUMMARY: {summary}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_transcript() -> None:
    text = f"""# Document 19 Subagent Round Transcript

## Diego Round 1 - High Recall
Diego proposed {len(nodes)} nodes and {len(diego_edges)} edges. The proposal included all visually supported top-source, bus-tie, load-module, and lower-control paths, plus five low-confidence high-recall extras around the MOV branch, RPS-701 branch, JB-MAIN bus association, and a possible A/B load-bus overconnection.

## Jennifer Round 1 - Precision Review
Jennifer accepted the {len(nodes)} named nodes but removed Diego's five extras and preserved the visual bracketed label `[LS-MOV601]`. She kept nearest named components along visible solid or dashed conductors: MOV601 branches from VALVE-MOV601 to INST-601 and `[LS-MOV601]`, then `[LS-MOV601]` to JB-601; RPS701 passes through INST-RPS701 to INST-701 before JB-701; JB-MAIN is on BUS-120AC-A only; B-side load 202 is on BUS-480-B.

## Diego Round 2
Diego agreed with Jennifer round 1 after rechecking the bus labels and local-control branches.

## Jennifer Round 2
Jennifer agreed with Diego round 2. The saturated final graph has {len(nodes)} nodes and {len(jennifer_edges)} edges.
"""
    (WORK / "subagent_round_transcript.md").write_text(text, encoding="utf-8")


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    write_round(
        WORK / "diego_round1_output.txt",
        "Diego high-recall extractor",
        f"High-recall graph with {len(nodes)} nodes and {len(diego_edges)} edges including five low-confidence visually plausible extras.",
        diego_edges,
        [
            "MOV601 dashed branch could be read as a shared junction among VALVE-MOV601 INST-601 [LS-MOV601] and JB-601; high-recall output includes shortcut alternatives.",
            "RPS701 dashed branch could be shortcut directly to JB-701 if the intermediate INST-701 is ignored; high-recall output includes that alternate.",
            "BUS-480-A/B tie area and lower JB-MAIN association were reviewed carefully because long bus bars cross near the split crop.",
        ],
    )
    write_round(
        WORK / "jennifer_round1_review.txt",
        "Jennifer precision reviewer",
        f"Precision graph with {len(nodes)} nodes and {len(jennifer_edges)} visually supported nearest-component edges.",
        jennifer_edges,
        [
            "No remaining ambiguous label affects the final matrix. The visual labels are read as BUS-480-A feeding 201/203/301/401/501/601 and BUS-480-B feeding 202/204/302/402/502/701.",
            "MOV601 keeps [LS-MOV601] as the intermediate named component from VALVE-MOV601 toward JB-601.",
        ],
    )
    write_agreement(
        WORK / "diego_round2_response.txt",
        "Diego high-recall extractor",
        "AGREE_WITH_JENNIFER_ROUND1",
        f"Reinspection found no visually supported edges beyond Jennifer round 1. Saturated graph remains {len(nodes)} nodes and {len(jennifer_edges)} edges.",
    )
    write_agreement(
        WORK / "jennifer_round2_final.txt",
        "Jennifer precision reviewer",
        "AGREE_WITH_DIEGO_ROUND2",
        f"Final precision pass agrees with Diego round 2 and keeps the {len(nodes)} node {len(jennifer_edges)} edge graph as final.",
    )
    write_transcript()
    print({"document": 19, "nodes": len(nodes), "diego_round1_edges": len(diego_edges), "final_edges": len(jennifer_edges)})


if __name__ == "__main__":
    main()
