from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


DOC_ID = "20"
ITERATION = "1"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    edge_type: str
    evidence: str
    normally_open: str = ""
    note: str = ""

    def key(self) -> tuple[str, str]:
        return tuple(sorted((self.source, self.target)))


def add_edge(edges: list[Edge], source: str, target: str, edge_type: str, evidence: str, normally_open: str = "", note: str = "") -> None:
    edge = Edge(source, target, edge_type, evidence, normally_open, note)
    if edge.key() in {existing.key() for existing in edges}:
        return
    edges.append(edge)


def add_chain(edges: list[Edge], nodes: list[str], edge_type: str, evidence: str, normally_open: str = "", note: str = "") -> None:
    for source, target in zip(nodes, nodes[1:]):
        add_edge(edges, source, target, edge_type, evidence, normally_open, note)


def build_final_edges() -> list[Edge]:
    edges: list[Edge] = []

    # Top 13.8 kV, 4.16 kV, and 480 V distribution.
    add_chain(edges, ["GEN-M1", "CB-GEN1", "TR-UAT1", "CB-13A-IN", "BUS-13K-A"], "power", "solid top-left source chain")
    add_chain(edges, ["BUS-13K-A", "CB-TIE-13K", "BUS-13K-B"], "tie", "13.8 kV bus tie drawn between BUS-13K-A and BUS-13K-B")
    add_chain(edges, ["FEED-230A", "TR-SAT1", "CB-13B-IN", "BUS-13K-B"], "power", "solid top-right source chain")
    add_chain(edges, ["BUS-13K-A", "CB-F41A", "DS-F41A", "TR-416A", "CB-416A-IN", "BUS-416-A"], "power", "left 13.8 kV to 4.16 kV feeder")
    add_chain(edges, ["BUS-13K-B", "CB-F41B", "DS-F41B", "TR-416B", "CB-416B-IN", "BUS-416-B"], "power", "right 13.8 kV to 4.16 kV feeder")
    add_chain(edges, ["DG-1A", "CB-DG1A", "BUS-416-A"], "power", "DG-1A feeder to BUS-416-A")
    add_chain(edges, ["DG-1B", "CB-DG1B", "BUS-416-B"], "power", "DG-1B feeder to BUS-416-B")
    add_chain(edges, ["BUS-416-A", "CB-TIE-416", "BUS-416-B"], "tie", "4.16 kV tie breaker between BUS-416-A and BUS-416-B", normally_open="true", note="N.O. label visible; included as topology")
    add_chain(edges, ["BUS-416-A", "CB-LCA", "TR-480A", "BUS-480-A"], "power", "480 V load center A transformer branch")
    add_chain(edges, ["BUS-416-A", "CB-LCB", "TR-480B", "BUS-480-B"], "power", "480 V load center B transformer branch")
    add_chain(edges, ["BUS-416-B", "CB-LCC", "TR-480C", "BUS-480-C"], "power", "480 V load center C transformer branch")
    add_chain(edges, ["BUS-416-B", "CB-LCD", "TR-480D", "BUS-480-D"], "power", "480 V load center D transformer branch")
    add_chain(edges, ["BUS-480-B", "CB-TIE-480", "BUS-480-C"], "tie", "480 V tie breaker between BUS-480-B and BUS-480-C")

    feeder_specs = {
        "A": [
            ("1", "MCC-1A", "RELAY-K1A", "PMP-RHR-101A", "power"),
            ("2", "MCC-2A", "CS-2A", "MOV-CCW-112A", "control"),
            ("3", "MCC-3A", "RELAY-K3A", "FAN-RB-104A", "power"),
            ("4", "JB-4A", "CS-4A", "HTR-PZR-01A", "control"),
            ("5", "MCC-5A", "RELAY-K5A", "COMP-IA-201A", "power"),
            ("6", "JB-6A", "CS-6A", "MOT-CRN-01A", "control"),
        ],
        "B": [
            ("1", "MCC-1B", "RELAY-K1B", "PMP-SI-102B", "power"),
            ("2", "MCC-2B", "CS-2B", "MOV-CS-116B", "control"),
            ("3", "MCC-3B", "RELAY-K3B", "FAN-CCW-108B", "power"),
            ("4", "JB-4B", "CS-4B", "HTR-SUMP-02B", "control"),
            ("5", "MCC-5B", "RELAY-K5B", "PMP-CHG-203B", "power"),
            ("6", "JB-6B", "CS-6B", "MOV-SW-118B", "control"),
        ],
        "C": [
            ("1", "MCC-1C", "RELAY-K1C", "PMP-RHR-101C", "power"),
            ("2", "MCC-2C", "CS-2C", "MOV-CCW-112C", "control"),
            ("3", "MCC-3C", "RELAY-K3C", "FAN-RB-104C", "power"),
            ("4", "JB-4C", "RELAY-K4C", "PMP-AFW-205C", "power"),
            ("5", "MCC-5C", "RELAY-K5C", "PMP-CCP-207C", "power"),
            ("6", "JB-6C", "CS-6C", "MOV-FCV-022C", "control"),
        ],
        "D": [
            ("1", "MCC-1D", "RELAY-K1D", "PMP-SI-102D", "power"),
            ("2", "MCC-2D", "CS-2D", "MOV-CS-116D", "control"),
            ("3", "MCC-3D", "RELAY-K3D", "FAN-ESF-110D", "power"),
            ("4", "JB-4D", "CS-4D", "MOV-RWST-24D", "control"),
            ("5", "MCC-5D", "RELAY-K5D", "PMP-CHG-203D", "power"),
            ("6", "JB-6D", "CS-6D", "MOV-SW-118D", "control"),
        ],
    }

    for bank, specs in feeder_specs.items():
        bus = f"BUS-480-{bank}"
        for number, cabinet, actuator, load, feeder_type in specs:
            cb = f"CB-48{bank}{number}"
            ds = f"DS-48{bank}{number}"
            evidence = f"480 V load center {bank} feeder {number} vertical branch"
            edge_type = "power" if feeder_type == "power" else "control_signal"
            add_chain(edges, [bus, cb, ds, cabinet, actuator, load], edge_type, evidence)

    # DC supply and UPS/inverter branches.
    add_chain(edges, ["BUS-480-A", "RECT-125A", "BUS-125DCA"], "dc_supply", "rectifier A vertical feed to 125 VDC bus A")
    add_chain(edges, ["BAT-125A", "CHGR-125A", "RECT-125A"], "dc_supply", "battery/charger/rectifier A dashed linkage")
    add_edge(edges, "BUS-125DCA", "INV-UPS-A", "dc_supply", "INV-UPS-A vertical tap on BUS-125DCA")
    add_chain(edges, ["BUS-480-C", "RECT-125B", "BUS-125DCB"], "dc_supply", "rectifier B vertical feed to 125 VDC bus B")
    add_chain(edges, ["BAT-125B", "CHGR-125B", "RECT-125B"], "dc_supply", "battery/charger/rectifier B dashed linkage")
    add_edge(edges, "BUS-125DCB", "INV-UPS-B", "dc_supply", "INV-UPS-B vertical tap on BUS-125DCB")

    # 125 VDC RPS and ESFAS control/signal wiring.
    add_chain(edges, ["BUS-125DCA", "CP-RPS-A", "TB-RPS-A", "PROT-UV-A", "RELAY-K101", "PT-410A"], "control_signal", "RPS A primary protection/instrument chain")
    add_edge(edges, "RELAY-K101", "LT-512A", "control_signal", "LT-512A branches from RELAY-K101")
    add_chain(edges, ["CP-RPS-A", "RELAY-K102", "TT-303A"], "control_signal", "RPS A side relay branch")
    add_edge(edges, "RELAY-K102", "GND-CTRL-A", "control_signal", "RPS A relay branch to control ground")

    add_chain(edges, ["BUS-125DCA", "CP-RPS-B", "TB-RPS-B", "PROT-UV-B", "RELAY-K103", "PT-410B"], "control_signal", "RPS B primary protection/instrument chain")
    add_edge(edges, "RELAY-K103", "LT-512B", "control_signal", "LT-512B branches from RELAY-K103")
    add_chain(edges, ["CP-RPS-B", "RELAY-K104", "TT-303B"], "control_signal", "RPS B side relay branch")
    add_edge(edges, "RELAY-K104", "GND-CTRL-B", "control_signal", "RPS B relay branch to control ground")

    add_chain(edges, ["BUS-125DCB", "CP-ESFAS-A", "JB-ESF-A", "PROT-LOP-A", "RELAY-K105", "FT-611A"], "control_signal", "ESFAS A protection/instrument chain")
    add_chain(edges, ["CP-ESFAS-A", "RELAY-K106", "XA-730A"], "control_signal", "ESFAS A relay branch")
    add_chain(edges, ["BUS-125DCB", "CP-ESFAS-B", "JB-ESF-B", "PROT-LOP-B", "RELAY-K107", "FT-611B"], "control_signal", "ESFAS B protection/instrument chain")
    add_chain(edges, ["CP-ESFAS-B", "RELAY-K108", "XA-730B"], "control_signal", "ESFAS B relay branch")
    add_edge(edges, "RELAY-K106", "RELAY-K108", "control_signal", "A/B ESF interlock dashed conductor between relay branches")

    return edges


def with_diego_round1_interlock(final_edges: list[Edge]) -> list[Edge]:
    edges = [edge for edge in final_edges if edge.key() != tuple(sorted(("RELAY-K106", "RELAY-K108")))]
    add_edge(edges, "RELAY-K106", "A-B-ESF-INTERLOCK", "control_signal", "Diego round 1 synthetic interlock node")
    add_edge(edges, "A-B-ESF-INTERLOCK", "RELAY-K108", "control_signal", "Diego round 1 synthetic interlock node")
    return edges


def ordered_nodes(edges: list[Edge]) -> list[str]:
    order: list[str] = []
    for edge in edges:
        for node in (edge.source, edge.target):
            if node not in order:
                order.append(node)
    return order


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes):
            writer.writerow([index, node])


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "edge_type", "evidence", "normally_open", "note"])
        writer.writeheader()
        for edge in edges:
            writer.writerow(asdict(edge))


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    matrix = [[0 for _ in nodes] for _ in nodes]
    index = {node: i for i, node in enumerate(nodes)}
    for edge in edges:
        i = index[edge.source]
        j = index[edge.target]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def estimate_text_tokens(text: str) -> int:
    # Local fallback when the OpenAI token counting endpoint is unavailable.
    return max(1, round(len(text) / 4))


def write_token_usage_estimate(path: Path) -> None:
    rows = [
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "setup",
            "call_id": "main_agent_01_inspect_resources",
            "caller": "main",
            "purpose": "Inspect allowed files, create crops, visually examine raw/overlays",
            "input_tokens_est": 6500,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 900,
            "reasoning_tokens_est": "",
            "image_file_input_tokens_est": 20000,
            "low_total_est": 20000,
            "expected_total_est": 27400,
            "high_total_est": 38000,
            "usage_source": "local estimate",
            "notes": "No API key; input estimated from text context plus viewed full-size/crop images.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_01_diego",
            "call_id": "subagent_diego_01_extract",
            "caller": "Diego",
            "purpose": "High-recall extraction from raw/crops/overlays",
            "input_tokens_est": 850,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 2600,
            "reasoning_tokens_est": "",
            "image_file_input_tokens_est": 24000,
            "low_total_est": 22000,
            "expected_total_est": 27450,
            "high_total_est": 42000,
            "usage_source": "local estimate",
            "notes": "Subagent usage object unavailable through local tool response.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_02_jennifer",
            "call_id": "subagent_jennifer_01_review",
            "caller": "Jennifer",
            "purpose": "Precision review of Diego round 1 graph",
            "input_tokens_est": 1850,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 720,
            "reasoning_tokens_est": "",
            "image_file_input_tokens_est": 18000,
            "low_total_est": 15000,
            "expected_total_est": 20570,
            "high_total_est": 34000,
            "usage_source": "local estimate",
            "notes": "Includes prompt containing Diego proposal plus likely visual crop checks.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_03_diego",
            "call_id": "subagent_diego_02_saturate",
            "caller": "Diego",
            "purpose": "Agree/revise after Jennifer correction",
            "input_tokens_est": 320,
            "cached_input_tokens_est": 2500,
            "output_tokens_est": 1650,
            "reasoning_tokens_est": "",
            "image_file_input_tokens_est": 0,
            "low_total_est": 1700,
            "expected_total_est": 4470,
            "high_total_est": 7000,
            "usage_source": "local estimate",
            "notes": "No new image payload expected; mostly text continuation.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "round_04_jennifer",
            "call_id": "subagent_jennifer_02_final",
            "caller": "Jennifer",
            "purpose": "Final saturation confirmation",
            "input_tokens_est": 170,
            "cached_input_tokens_est": 800,
            "output_tokens_est": 200,
            "reasoning_tokens_est": "",
            "image_file_input_tokens_est": 0,
            "low_total_est": 250,
            "expected_total_est": 1170,
            "high_total_est": 3000,
            "usage_source": "local estimate",
            "notes": "Short confirmation call; output estimate may vary.",
        },
        {
            "document": DOC_ID,
            "iteration": ITERATION,
            "round": "artifact_generation",
            "call_id": "main_agent_02_write_validate_summarize",
            "caller": "main",
            "purpose": "Generate CSV/JSON/MD artifacts, validate matrix, summarize results",
            "input_tokens_est": 4800,
            "cached_input_tokens_est": 0,
            "output_tokens_est": 900,
            "reasoning_tokens_est": "",
            "image_file_input_tokens_est": 0,
            "low_total_est": 5000,
            "expected_total_est": 5700,
            "high_total_est": 9000,
            "usage_source": "local estimate",
            "notes": "No actual OpenAI usage object exposed in this environment.",
        },
    ]
    for row in rows:
        row["total_tokens_est"] = row["expected_total_est"]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "method": "OpenAI Responses token counting endpoint was not used because no API key is available. Text tokens are estimated locally by chars/4; image/file tokens are rough visual-payload estimates based on the full image/crop inspection workload.",
        "low_total_est": sum(int(row["low_total_est"]) for row in rows),
        "expected_total_est": sum(int(row["expected_total_est"]) for row in rows),
        "high_total_est": sum(int(row["high_total_est"]) for row in rows),
        "calls": rows,
    }
    path.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_round_summary(path: Path, rounds: list[tuple[str, str, list[Edge]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["round_file_stem", "agent", "node_count", "edge_count", "notes"])
        for stem, agent, edges in rounds:
            note = "synthetic ESF interlock node" if "round_01" in stem else "final direct RELAY-K106--RELAY-K108 interlock edge"
            writer.writerow([stem, agent, len(ordered_nodes(edges)), len(edges), note])


def write_notes(path: Path, final_nodes: list[str], final_edges: list[Edge]) -> None:
    text = f"""# Document 20 Connectivity Extraction

Generated: {datetime.now().isoformat(timespec="seconds")}

Allowed resource folder: `{ROOT}`

No GT or GT-derived files were used. No off-the-shelf OCR was used; labels and topology were read visually from the raw image and deterministic crops/overlays.

## Rounds

- Round 01 Diego: high-recall graph. Diego represented the A/B ESF interlock as a synthetic node.
- Round 02 Jennifer: precision correction. Jennifer removed the synthetic interlock node and used a direct `RELAY-K106 -- RELAY-K108` edge.
- Round 03 Diego: agreed with Jennifer's correction; graph saturated.
- Round 04 Jennifer: final confirmation; graph saturated.

## Final Graph Policy

- Named buses, breakers, disconnects, transformers, MCCs, JBs, relays, switches, instruments, batteries, chargers, rectifiers, inverters, and loads are nodes.
- Unlabeled connector squares, black bus dots, tick marks, and ordinary wire junction geometry are not semantic nodes.
- Tie breakers are included as topological connectivity nodes. `CB-TIE-416` is marked normally open in the edge table where visible.
- The A/B ESF interlock is represented as direct edge `RELAY-K106 -- RELAY-K108` with evidence `A/B ESF interlock dashed conductor between relay branches`.

## Final Counts

- Nodes: {len(final_nodes)}
- Undirected edges: {len(final_edges)}
- Matrix diagonal: zero
- Matrix symmetry: enforced by generator
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    final_edges = build_final_edges()
    diego_round1_edges = with_diego_round1_interlock(final_edges)
    rounds = [
        ("round_01_diego_high_recall", "Diego", diego_round1_edges),
        ("round_02_jennifer_corrected", "Jennifer", final_edges),
        ("round_03_diego_saturated", "Diego", final_edges),
        ("round_04_jennifer_final", "Jennifer", final_edges),
    ]

    for stem, _agent, edges in rounds:
        nodes = ordered_nodes(edges)
        write_nodes(RESULTS / f"{stem}_nodes.csv", nodes)
        write_edges(RESULTS / f"{stem}_edges.csv", edges)
        write_matrix(RESULTS / f"{stem}_connectivity_matrix.csv", nodes, edges)

    final_nodes = ordered_nodes(final_edges)
    write_nodes(RESULTS / "final_nodes.csv", final_nodes)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_nodes, final_edges)
    (RESULTS / "final_graph.json").write_text(
        json.dumps(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "node_count": len(final_nodes),
                "edge_count": len(final_edges),
                "nodes": final_nodes,
                "edges": [asdict(edge) for edge in final_edges],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    write_round_summary(RESULTS / "round_summary.csv", rounds)
    write_token_usage_estimate(RESULTS / "token_usage_estimate.csv")
    write_notes(RESULTS / "extraction_notes.md", final_nodes, final_edges)

    print(f"Wrote document {DOC_ID} results to {RESULTS}")
    print(f"Final nodes: {len(final_nodes)}")
    print(f"Final edges: {len(final_edges)}")


if __name__ == "__main__":
    main()
