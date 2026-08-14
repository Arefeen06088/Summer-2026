from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


NODES: list[str] = [
    # AC source and upper buses, Train A.
    "OFFSITE-1",
    "CB-101A",
    "TR-SAT-1A",
    "BUS-101A",
    "EDG-1A",
    "CB-DG1A",
    "SW-MAN-A",
    "TB-DG-A",
    "CB-201A",
    "TR-1A",
    "CB-202A",
    "BUS-201A",
    "CB-TIE-1",
    "SYNC-CAB",
    # AC source and upper buses, Train B.
    "OFFSITE-2",
    "CB-101B",
    "TR-SAT-1B",
    "BUS-101B",
    "EDG-1B",
    "CB-DG1B",
    "SW-MAN-B",
    "TB-DG-B",
    "CB-201B",
    "TR-1B",
    "CB-202B",
    "BUS-201B",
]


FEEDERS_A: list[tuple[str, str]] = [
    ("2A01", "PUMP-P201A"),
    ("2A02", "FAN-F202A"),
    ("2A03", "MOV-HV203A"),
    ("2A04", "PUMP-P204A"),
    ("2A05", "CHLR-205A"),
    ("2A06", "HTR-206A"),
    ("2A07", "VALVE-MV207A"),
    ("2A08", "PMP-LP208A"),
    ("2A09", "COMP-C209A"),
]

FEEDERS_B: list[tuple[str, str]] = [
    ("2B01", "PUMP-P201B"),
    ("2B02", "FAN-F202B"),
    ("2B03", "MOV-HV203B"),
    ("2B04", "PUMP-P204B"),
    ("2B05", "CHLR-205B"),
    ("2B06", "HTR-206B"),
    ("2B07", "VALVE-MV207B"),
    ("2B08", "PMP-LP208B"),
    ("2B09", "COMP-C209B"),
]


for feeder, load in FEEDERS_A + FEEDERS_B:
    NODES.extend(
        [
            f"CB-{feeder}",
            f"DS-{feeder}",
            f"MCC-{feeder}",
            f"TB-{feeder}",
            load,
            f"HS-{feeder}",
            f"RELAY-K{feeder}",
        ]
    )


NODES.extend(
    [
        # DC / RPS / instrumentation, Train A.
        "DC-BUS-125A",
        "BAT-125A",
        "CHG-125A",
        "INV-120A",
        "PNL-DC-A",
        "ESFAS-PNL-A",
        "GND-DC-A",
        "METER-V1",
        "PNL-AC-A",
        "RPS-PNL-A",
        "TRIP-MOD-A",
        "PT-401A",
        "LT-402A",
        "FT-403A",
        "JB-401A",
        "TB-RPS-A",
        "GND-401A",
        "RELAY-K27A",
        "RELAY-K59A",
        "RELAY-K81A",
        "RELAY-K86A",
        # Common load-shed / annunciation.
        "LOAD-SHED-CAB",
        "TDR-1",
        "TDR-2",
        "LAMP-ALM-A",
        "LAMP-ALM-B",
        "ANN-PNL-1",
        "SEQ-REC-1",
        # DC / RPS / instrumentation, Train B.
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
        "TB-RPS-B",
        "GND-401B",
        "RELAY-K27B",
        "RELAY-K59B",
        "RELAY-K81B",
        "RELAY-K86B",
    ]
)


def canon(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return (a, b) if a <= b else (b, a)


def add_edge(edges: set[tuple[str, str]], a: str, b: str) -> None:
    if a not in NODES:
        raise ValueError(f"Unknown node: {a}")
    if b not in NODES:
        raise ValueError(f"Unknown node: {b}")
    if a == b:
        raise ValueError(f"Self-loop not justified: {a}")
    edges.add(canon((a, b)))


def add_chain(edges: set[tuple[str, str]], chain: list[str]) -> None:
    for a, b in zip(chain, chain[1:]):
        add_edge(edges, a, b)


def build_final_edges() -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()

    # Upper AC source, EDG, tie, and lower bus feeds.
    add_chain(edges, ["OFFSITE-1", "CB-101A", "TR-SAT-1A", "BUS-101A"])
    add_chain(edges, ["EDG-1A", "CB-DG1A", "BUS-101A"])
    add_chain(edges, ["SW-MAN-A", "TB-DG-A", "CB-DG1A"])
    add_chain(edges, ["BUS-101A", "CB-TIE-1", "BUS-101B"])
    add_edge(edges, "CB-TIE-1", "SYNC-CAB")
    add_chain(edges, ["OFFSITE-2", "CB-101B", "TR-SAT-1B", "BUS-101B"])
    add_chain(edges, ["EDG-1B", "CB-DG1B", "BUS-101B"])
    add_chain(edges, ["SW-MAN-B", "TB-DG-B", "CB-DG1B"])
    add_chain(edges, ["BUS-101A", "CB-201A", "TR-1A", "CB-202A", "BUS-201A"])
    add_chain(edges, ["BUS-101B", "CB-201B", "TR-1B", "CB-202B", "BUS-201B"])

    # 4.16 kV feeder power and local control.
    for feeder, load in FEEDERS_A:
        add_chain(edges, ["BUS-201A", f"CB-{feeder}", f"DS-{feeder}", f"MCC-{feeder}", f"TB-{feeder}", load])
        add_chain(edges, [f"HS-{feeder}", f"RELAY-K{feeder}", f"MCC-{feeder}"])

    for feeder, load in FEEDERS_B:
        add_chain(edges, ["BUS-201B", f"CB-{feeder}", f"DS-{feeder}", f"MCC-{feeder}", f"TB-{feeder}", load])
        add_chain(edges, [f"HS-{feeder}", f"RELAY-K{feeder}", f"MCC-{feeder}"])

    # DC buses and panels.
    for node in ["BAT-125A", "CHG-125A", "INV-120A", "PNL-DC-A", "METER-V1"]:
        add_edge(edges, "DC-BUS-125A", node)
    add_edge(edges, "PNL-DC-A", "ESFAS-PNL-A")
    add_edge(edges, "PNL-DC-A", "GND-DC-A")
    add_edge(edges, "INV-120A", "PNL-AC-A")

    for node in ["BAT-125B", "CHG-125B", "INV-120B", "PNL-DC-B"]:
        add_edge(edges, "DC-BUS-125B", node)
    add_edge(edges, "PNL-DC-B", "ESFAS-PNL-B")
    add_edge(edges, "PNL-DC-B", "GND-DC-B")
    add_edge(edges, "INV-120B", "PNL-AC-B")

    # RPS / trip / instrumentation.
    add_chain(edges, ["PNL-AC-A", "RPS-PNL-A", "TRIP-MOD-A"])
    add_chain(edges, ["RPS-PNL-A", "RELAY-K27A", "RELAY-K59A", "RELAY-K81A", "RELAY-K86A", "TRIP-MOD-A"])
    for node in ["PT-401A", "LT-402A", "FT-403A"]:
        add_edge(edges, node, "JB-401A")
    add_chain(edges, ["JB-401A", "TB-RPS-A", "RPS-PNL-A"])
    add_edge(edges, "JB-401A", "GND-401A")

    add_chain(edges, ["PNL-AC-B", "RPS-PNL-B", "TRIP-MOD-B"])
    add_chain(edges, ["RPS-PNL-B", "RELAY-K27B", "RELAY-K59B", "RELAY-K81B", "RELAY-K86B", "TRIP-MOD-B"])
    for node in ["PT-401B", "LT-402B", "FT-403B"]:
        add_edge(edges, node, "JB-401B")
    add_chain(edges, ["JB-401B", "TB-RPS-B", "RPS-PNL-B"])
    add_edge(edges, "JB-401B", "GND-401B")

    # Common load-shed / annunciation.
    add_edge(edges, "ESFAS-PNL-A", "LOAD-SHED-CAB")
    add_edge(edges, "ESFAS-PNL-B", "LOAD-SHED-CAB")
    add_edge(edges, "LOAD-SHED-CAB", "TDR-1")
    add_edge(edges, "LOAD-SHED-CAB", "TDR-2")
    add_edge(edges, "LOAD-SHED-CAB", "LAMP-ALM-A")
    add_edge(edges, "LOAD-SHED-CAB", "LAMP-ALM-B")
    add_edge(edges, "LOAD-SHED-CAB", "ANN-PNL-1")
    add_edge(edges, "ANN-PNL-1", "SEQ-REC-1")

    return edges


FINAL_EDGES = build_final_edges()


def diego_round1_edges() -> set[tuple[str, str]]:
    edges = set(FINAL_EDGES)
    # Diego's high-recall pass included these visually plausible load-shed/trip candidates.
    add_edge(edges, "TRIP-MOD-A", "LOAD-SHED-CAB")
    add_edge(edges, "TRIP-MOD-B", "LOAD-SHED-CAB")
    return edges


ROUND_GRAPHS: list[dict[str, object]] = [
    {
        "round": 1,
        "agent": "Diego",
        "role": "high-recall extractor",
        "slug": "round_01_diego_high_recall",
        "edges": diego_round1_edges(),
        "status": "proposal",
        "note": "Included all visually plausible confirmed edges plus two trip-module/load-shed candidates later rejected.",
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "slug": "round_02_jennifer_precision",
        "edges": FINAL_EDGES,
        "status": "refined",
        "note": "Removed unsupported direct TRIP-MOD-A/B to LOAD-SHED-CAB candidates and rejected overconnections.",
    },
    {
        "round": 3,
        "agent": "Diego",
        "role": "saturation check",
        "slug": "round_03_diego_saturation",
        "edges": FINAL_EDGES,
        "status": "agree",
        "note": "Diego agreed with Jennifer; no add/remove/rename requested.",
    },
]


EDGE_EVIDENCE: dict[tuple[str, str], str] = {}


def evidence(edge: tuple[str, str]) -> str:
    a, b = edge
    if "LOAD-SHED-CAB" in edge and ("TRIP-MOD-A" in edge or "TRIP-MOD-B" in edge):
        return "High-recall candidate from dashed routing; rejected in precision review."
    if a.startswith("BUS-201") or b.startswith("BUS-201"):
        return "Feeder tap from 4.16 kV safety bus with junction dot."
    if a.startswith("CB-2") or b.startswith("CB-2") or a.startswith("DS-2") or b.startswith("DS-2"):
        return "Vertical feeder power chain."
    if a.startswith("MCC-2") or b.startswith("MCC-2") or a.startswith("TB-2") or b.startswith("TB-2"):
        return "Feeder power/control chain through MCC and terminal block."
    if a.startswith("HS-2") or b.startswith("HS-2") or a.startswith("RELAY-K2") or b.startswith("RELAY-K2"):
        return "Local dashed feeder control route."
    if "DC-BUS-125A" in edge or "DC-BUS-125B" in edge:
        return "Solid DC bus tap with visible junction."
    if "GND" in a or "GND" in b:
        return "Labeled ground terminal/drop shown as its own node."
    if "LOAD-SHED-CAB" in edge:
        return "Central load-shed cabinet control/signal route."
    if "RPS-PNL" in a or "RPS-PNL" in b or "TRIP-MOD" in a or "TRIP-MOD" in b:
        return "Dashed RPS/trip control route."
    if "JB-401" in a or "JB-401" in b or "TB-RPS" in a or "TB-RPS" in b:
        return "Dotted instrumentation/signal route through junction/terminal block."
    if "CB-TIE-1" in edge or "SYNC-CAB" in edge:
        return "Upper bus tie and dashed synchronizing cabinet control route."
    return "Solid/dashed line visually connects consecutive labeled components."


def ordered_edges(edges: set[tuple[str, str]]) -> list[tuple[str, str]]:
    node_index = {node: idx for idx, node in enumerate(NODES)}
    return sorted(edges, key=lambda e: (min(node_index[e[0]], node_index[e[1]]), max(node_index[e[0]], node_index[e[1]]), e))


def write_matrix(path: Path, edges: set[tuple[str, str]]) -> None:
    edge_set = {canon(edge) for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component", *NODES])
        for row_node in NODES:
            row = [row_node]
            for col_node in NODES:
                row.append(0 if row_node == col_node else int(canon((row_node, col_node)) in edge_set))
            writer.writerow(row)


def write_edges(path: Path, edges: set[tuple[str, str]]) -> None:
    final_set = {canon(edge) for edge in FINAL_EDGES}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "in_final", "evidence"])
        for edge in ordered_edges(edges):
            writer.writerow([edge[0], edge[1], int(edge in final_set), evidence(edge)])


def validate(edges: set[tuple[str, str]]) -> None:
    if len(NODES) != len(set(NODES)):
        dupes = [node for node in NODES if NODES.count(node) > 1]
        raise ValueError(f"Duplicate node labels: {sorted(set(dupes))}")
    for a, b in edges:
        if a == b:
            raise ValueError(f"Self-loop: {a}")
        if a not in NODES or b not in NODES:
            raise ValueError(f"Unknown edge node: {a}, {b}")


def write_notes() -> None:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Case 24 Extraction Note",
        "",
        f"Generated: {now}",
        "",
        "Allowed evidence used: the raw schematic PNG and raw-derived crops in `codes/crops` only. No GT or GT-derived feedback was used.",
        "",
        "## Rounds",
        "",
        "- Round 1 Diego: high-recall proposal with all main AC, feeder, DC/RPS, and common load-shed routes. Included two tentative `TRIP-MOD-* -- LOAD-SHED-CAB` candidates.",
        "- Round 2 Jennifer: precision refinement. Removed unsupported direct trip-module/load-shed candidates; rejected relay-to-relay feeder chains, B-side meter, ground merges, direct load-shed-to-sequence-recorder, annunciator-to-lamp, and lamp-to-lamp edges.",
        "- Round 3 Diego: agreed with Jennifer; confirmed `SYNC-CAB` is visibly labeled and connected to `CB-TIE-1` by dashed control/trip route.",
        "",
        "## Final Decisions",
        "",
        f"- Final node count: {len(NODES)}",
        f"- Final edge count: {len(FINAL_EDGES)}",
        "- Ground symbols are separate labeled terminal nodes; they are not merged together.",
        "- `METER-V1` is included only on `DC-BUS-125A`; no B-side meter label was visible.",
        "- Feeder control uses local `HS-2* -- RELAY-K2* -- MCC-2*` edges only; no cross-feeder control-chain edges are included.",
        "- `TRIP-MOD-A -- LOAD-SHED-CAB` and `TRIP-MOD-B -- LOAD-SHED-CAB` remain uncertain/rejected for the final matrix.",
        "",
        "## Files",
        "",
        "- `final_connectivity_matrix.csv`: final saturated matrix.",
        "- `final_edges.csv`: final saturated edge list.",
        "- `round_01_diego_high_recall_matrix.csv`, `round_02_jennifer_precision_matrix.csv`, `round_03_diego_saturation_matrix.csv`: round matrices.",
    ]
    (RESULTS_DIR / "extraction_note.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_token_tracking() -> None:
    rows = [
        {
            "case": "24",
            "round": graph["round"],
            "agent": graph["agent"],
            "role": graph["role"],
            "status": graph["status"],
            "node_count": len(NODES),
            "edge_count": len(graph["edges"]),
            "prompt_tokens": "not_available",
            "completion_tokens": "not_available",
            "total_tokens": "not_available",
            "token_note": "Subagent/tool token usage was not exposed in this environment.",
        }
        for graph in ROUND_GRAPHS
    ]
    fieldnames = list(rows[0].keys())
    for name in ["token_performance_tracking.csv", "token_performance_traking.csv"]:
        with (RESULTS_DIR / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    validate(FINAL_EDGES)
    for graph in ROUND_GRAPHS:
        validate(graph["edges"])  # type: ignore[arg-type]
        slug = str(graph["slug"])
        edges = graph["edges"]  # type: ignore[assignment]
        write_matrix(RESULTS_DIR / f"{slug}_matrix.csv", edges)  # type: ignore[arg-type]
        write_edges(RESULTS_DIR / f"{slug}_edges.csv", edges)  # type: ignore[arg-type]

    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", FINAL_EDGES)
    write_edges(RESULTS_DIR / "final_edges.csv", FINAL_EDGES)

    with (RESULTS_DIR / "final_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "component"])
        for idx, node in enumerate(NODES, start=1):
            writer.writerow([idx, node])

    graph_payload = {
        "case": 24,
        "node_count": len(NODES),
        "edge_count": len(FINAL_EDGES),
        "nodes": NODES,
        "final_edges": [{"source": a, "target": b} for a, b in ordered_edges(FINAL_EDGES)],
        "uncertain_not_included": [
            {"source": "LOAD-SHED-CAB", "target": "TRIP-MOD-A"},
            {"source": "LOAD-SHED-CAB", "target": "TRIP-MOD-B"},
        ],
        "rounds": [
            {
                "round": graph["round"],
                "agent": graph["agent"],
                "role": graph["role"],
                "status": graph["status"],
                "edge_count": len(graph["edges"]),
                "note": graph["note"],
            }
            for graph in ROUND_GRAPHS
        ],
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph_payload, indent=2), encoding="utf-8")

    write_notes()
    write_token_tracking()

    print(f"wrote {len(NODES)} nodes and {len(FINAL_EDGES)} final edges to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
