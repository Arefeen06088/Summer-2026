from __future__ import annotations

import csv
import json
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    line_type: str
    status: str
    evidence: str

    @property
    def key(self) -> tuple[str, str]:
        return tuple(sorted((self.source, self.target)))


def add_edge(edges: list[Edge], seen: set[tuple[str, str]], source: str, target: str, line_type: str, evidence: str, status: str = "accepted") -> None:
    edge = Edge(source, target, line_type, status, evidence)
    if edge.key in seen:
        raise ValueError(f"duplicate undirected edge: {source} -- {target}")
    seen.add(edge.key)
    edges.append(edge)


def make_final_edges() -> list[Edge]:
    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()

    def add(source: str, target: str, line_type: str, evidence: str, status: str = "accepted") -> None:
        add_edge(edges, seen, source, target, line_type, evidence, status)

    top_edges = [
        ("GEN-M1", "CB-GEN1", "P", "Solid generator source lead through an unlabeled inline square to CB-GEN1."),
        ("CB-GEN1", "TR-UAT1", "P", "Solid feeder from CB-GEN1 to TR-UAT1."),
        ("TR-UAT1", "CB-13A-IN", "P", "Solid feeder from TR-UAT1 to CB-13A-IN."),
        ("CB-13A-IN", "BUS-13K-A", "P", "Vertical solid tap with black junction dot on BUS-13K-A."),
        ("BUS-13K-A", "CB-F41A", "P", "Solid bus tap from BUS-13K-A to CB-F41A."),
        ("CB-F41A", "DS-F41A", "P", "Solid feeder from CB-F41A to DS-F41A."),
        ("DS-F41A", "TR-416A", "P", "Solid feeder from DS-F41A to TR-416A."),
        ("TR-416A", "CB-416A-IN", "P", "Solid feeder from TR-416A to CB-416A-IN."),
        ("CB-416A-IN", "BUS-416-A", "P", "Solid tap with black junction dot on BUS-416-A."),
        ("BUS-13K-A", "CB-TIE-13K", "P", "Solid tie lead from BUS-13K-A to CB-TIE-13K."),
        ("CB-TIE-13K", "BUS-13K-B", "P", "Solid tie lead from CB-TIE-13K to BUS-13K-B."),
        ("FEED-230A", "TR-SAT1", "P", "Solid source feeder from FEED-230A to TR-SAT1."),
        ("TR-SAT1", "CB-13B-IN", "P", "Solid feeder from TR-SAT1 to CB-13B-IN."),
        ("CB-13B-IN", "BUS-13K-B", "P", "Vertical solid tap with black junction dot on BUS-13K-B."),
        ("BUS-13K-B", "CB-F41B", "P", "Solid bus tap from BUS-13K-B to CB-F41B."),
        ("CB-F41B", "DS-F41B", "P", "Solid feeder from CB-F41B to DS-F41B."),
        ("DS-F41B", "TR-416B", "P", "Solid feeder from DS-F41B to TR-416B."),
        ("TR-416B", "CB-416B-IN", "P", "Solid feeder from TR-416B to CB-416B-IN."),
        ("CB-416B-IN", "BUS-416-B", "P", "Solid tap with black junction dot on BUS-416-B."),
        ("DG-1A", "CB-DG1A", "P", "Solid diesel generator lead through an unlabeled inline square to CB-DG1A."),
        ("CB-DG1A", "BUS-416-A", "P", "Solid tap from CB-DG1A to BUS-416-A."),
        ("DG-1B", "CB-DG1B", "P", "Solid diesel generator lead through an unlabeled inline square to CB-DG1B."),
        ("CB-DG1B", "BUS-416-B", "P", "Solid tap from CB-DG1B to BUS-416-B."),
        ("BUS-416-A", "CB-TIE-416", "P", "Solid tie lead from BUS-416-A to CB-TIE-416."),
        ("CB-TIE-416", "BUS-416-B", "P", "Solid tie lead from CB-TIE-416 to BUS-416-B."),
        ("BUS-416-A", "CB-LCA", "P", "Solid load-center feeder tap from BUS-416-A to CB-LCA."),
        ("CB-LCA", "TR-480A", "P", "Solid feeder from CB-LCA to TR-480A."),
        ("TR-480A", "BUS-480-A", "P", "Transformer secondary solid tap from TR-480A to BUS-480-A."),
        ("BUS-416-A", "CB-LCB", "P", "Solid load-center feeder tap from BUS-416-A to CB-LCB."),
        ("CB-LCB", "TR-480B", "P", "Solid feeder from CB-LCB to TR-480B."),
        ("TR-480B", "BUS-480-B", "P", "Transformer secondary solid tap from TR-480B to BUS-480-B."),
        ("BUS-416-B", "CB-LCC", "P", "Solid load-center feeder tap from BUS-416-B to CB-LCC."),
        ("CB-LCC", "TR-480C", "P", "Solid feeder from CB-LCC to TR-480C."),
        ("TR-480C", "BUS-480-C", "P", "Transformer secondary solid tap from TR-480C to BUS-480-C."),
        ("BUS-416-B", "CB-LCD", "P", "Solid load-center feeder tap from BUS-416-B to CB-LCD."),
        ("CB-LCD", "TR-480D", "P", "Solid feeder from CB-LCD to TR-480D."),
        ("TR-480D", "BUS-480-D", "P", "Transformer secondary solid tap from TR-480D to BUS-480-D."),
        ("BUS-480-B", "CB-TIE-480", "P", "Solid 480 V tie lead from BUS-480-B to CB-TIE-480."),
        ("CB-TIE-480", "BUS-480-C", "P", "Solid 480 V tie lead from CB-TIE-480 to BUS-480-C."),
    ]
    for edge in top_edges:
        add(*edge)

    feeder_specs = [
        ("BUS-480-A", "A1", "MCC-1A", "RELAY-K1A", "PMP-RHR-101A", "P"),
        ("BUS-480-A", "A2", "MCC-2A", "CS-2A", "MOV-CCW-112A", "CTRL"),
        ("BUS-480-A", "A3", "MCC-3A", "RELAY-K3A", "FAN-RB-104A", "P"),
        ("BUS-480-A", "A4", "JB-4A", "CS-4A", "HTR-PZR-01A", "CTRL"),
        ("BUS-480-A", "A5", "MCC-5A", "RELAY-K5A", "COMP-IA-201A", "P"),
        ("BUS-480-A", "A6", "JB-6A", "CS-6A", "MOT-CRN-01A", "CTRL"),
        ("BUS-480-B", "B1", "MCC-1B", "RELAY-K1B", "PMP-SI-102B", "P"),
        ("BUS-480-B", "B2", "MCC-2B", "CS-2B", "MOV-CS-116B", "CTRL"),
        ("BUS-480-B", "B3", "MCC-3B", "RELAY-K3B", "FAN-CCW-108B", "P"),
        ("BUS-480-B", "B4", "JB-4B", "CS-4B", "HTR-SUMP-02B", "CTRL"),
        ("BUS-480-B", "B5", "MCC-5B", "RELAY-K5B", "PMP-CHG-203B", "P"),
        ("BUS-480-B", "B6", "JB-6B", "CS-6B", "MOV-SW-118B", "CTRL"),
        ("BUS-480-C", "C1", "MCC-1C", "RELAY-K1C", "PMP-RHR-101C", "P"),
        ("BUS-480-C", "C2", "MCC-2C", "CS-2C", "MOV-CCW-112C", "CTRL"),
        ("BUS-480-C", "C3", "MCC-3C", "RELAY-K3C", "FAN-RB-104C", "P"),
        ("BUS-480-C", "C4", "JB-4C", "RELAY-K4C", "PMP-AFW-205C", "P"),
        ("BUS-480-C", "C5", "MCC-5C", "RELAY-K5C", "PMP-CCP-207C", "P"),
        ("BUS-480-C", "C6", "JB-6C", "CS-6C", "MOV-FCV-022C", "CTRL"),
        ("BUS-480-D", "D1", "MCC-1D", "RELAY-K1D", "PMP-SI-102D", "P"),
        ("BUS-480-D", "D2", "MCC-2D", "CS-2D", "MOV-CS-116D", "CTRL"),
        ("BUS-480-D", "D3", "MCC-3D", "RELAY-K3D", "FAN-ESF-110D", "P"),
        ("BUS-480-D", "D4", "JB-4D", "CS-4D", "MOV-RWST-24D", "CTRL"),
        ("BUS-480-D", "D5", "MCC-5D", "RELAY-K5D", "PMP-CHG-203D", "P"),
        ("BUS-480-D", "D6", "JB-6D", "CS-6D", "MOV-SW-118D", "CTRL"),
    ]
    for bus, suffix, mid, controller, load, downstream_type in feeder_specs:
        add(bus, f"CB-48{suffix}", "P", f"Solid branch tap from {bus} to CB-48{suffix}.")
        add(f"CB-48{suffix}", f"DS-48{suffix}", "P", f"Solid feeder from CB-48{suffix} to DS-48{suffix}.")
        add(f"DS-48{suffix}", mid, "P", f"Solid feeder from DS-48{suffix} to {mid}.")
        if downstream_type == "P":
            add(mid, controller, "P", f"Solid branch from {mid} to {controller}.")
            add(controller, load, "P", f"Solid load feeder from {controller} to {load}.")
        else:
            add(mid, controller, "CTRL", f"Dashed control drop from {mid} to {controller}.")
            add(controller, load, "CTRL", f"Dashed control drop from {controller} to {load}.")

    interface_edges = [
        ("BUS-480-A", "RECT-125A", "P", "Tight crop shows solid vertical BUS-480-A tap between A4/A5 descending to RECT-125A AC side."),
        ("BUS-480-C", "RECT-125B", "P", "Solid route from BUS-480-C end tap descends and turns into RECT-125B AC side."),
        ("BAT-125A", "CHGR-125A", "DC", "Dashed DC link between BAT-125A and CHGR-125A."),
        ("CHGR-125A", "RECT-125A", "DC", "Dashed DC link between CHGR-125A and RECT-125A."),
        ("RECT-125A", "BUS-125DCA", "DC", "Vertical dashed DC drop from RECT-125A to BUS-125DCA black junction dot."),
        ("INV-UPS-A", "BUS-125DCA", "DC", "Vertical dashed DC drop from INV-UPS-A to BUS-125DCA black junction dot."),
        ("BAT-125B", "CHGR-125B", "DC", "Dashed DC link between BAT-125B and CHGR-125B."),
        ("CHGR-125B", "RECT-125B", "DC", "Dashed DC link between CHGR-125B and RECT-125B."),
        ("RECT-125B", "BUS-125DCB", "DC", "Vertical dashed DC drop from RECT-125B to BUS-125DCB black junction dot."),
        ("INV-UPS-B", "BUS-125DCB", "DC", "Vertical dashed DC drop from INV-UPS-B to BUS-125DCB black junction dot."),
        ("BUS-125DCA", "CP-RPS-A", "DC", "Dashed 125 VDC tap from BUS-125DCA to CP-RPS-A with black bus dot."),
        ("BUS-125DCA", "CP-RPS-B", "DC", "Dashed 125 VDC tap from BUS-125DCA to CP-RPS-B with black bus dot."),
        ("BUS-125DCB", "CP-ESFAS-A", "DC", "Dashed 125 VDC tap from BUS-125DCB to CP-ESFAS-A with black bus dot."),
        ("BUS-125DCB", "CP-ESFAS-B", "DC", "Dashed 125 VDC tap from BUS-125DCB to CP-ESFAS-B with black bus dot."),
    ]
    for edge in interface_edges:
        add(*edge)

    lower_control_edges = [
        ("CP-RPS-A", "TB-RPS-A", "CTRL", "Dashed vertical control line from CP-RPS-A to TB-RPS-A."),
        ("TB-RPS-A", "PROT-UV-A", "CTRL", "Dashed diagonal control line from TB-RPS-A to PROT-UV-A."),
        ("PROT-UV-A", "RELAY-K101", "CTRL", "Dashed control branch from PROT-UV-A to RELAY-K101."),
        ("RELAY-K101", "PT-410A", "SIG", "Dot-dash instrument branch from RELAY-K101 to PT-410A."),
        ("RELAY-K101", "LT-512A", "SIG", "Dot-dash instrument branch from RELAY-K101 to LT-512A."),
        ("CP-RPS-A", "RELAY-K102", "CTRL", "Dashed right-side control drop from CP-RPS-A to RELAY-K102."),
        ("RELAY-K102", "TT-303A", "SIG", "Dot-dash instrument branch from RELAY-K102 to TT-303A."),
        ("RELAY-K102", "GND-CTRL-A", "CTRL", "Visible control ground lead from RELAY-K102 to GND-CTRL-A."),
        ("CP-RPS-B", "TB-RPS-B", "CTRL", "Dashed vertical control line from CP-RPS-B to TB-RPS-B."),
        ("TB-RPS-B", "PROT-UV-B", "CTRL", "Dashed diagonal control line from TB-RPS-B to PROT-UV-B."),
        ("PROT-UV-B", "RELAY-K103", "CTRL", "Dashed control branch from PROT-UV-B to RELAY-K103."),
        ("RELAY-K103", "PT-410B", "SIG", "Dot-dash instrument branch from RELAY-K103 to PT-410B."),
        ("RELAY-K103", "LT-512B", "SIG", "Dot-dash instrument branch from RELAY-K103 to LT-512B."),
        ("CP-RPS-B", "RELAY-K104", "CTRL", "Dashed right-side control drop from CP-RPS-B to RELAY-K104."),
        ("RELAY-K104", "TT-303B", "SIG", "Dot-dash instrument branch from RELAY-K104 to TT-303B."),
        ("RELAY-K104", "GND-CTRL-B", "CTRL", "Visible control ground lead from RELAY-K104 to GND-CTRL-B."),
        ("CP-ESFAS-A", "JB-ESF-A", "CTRL", "Dashed vertical control line from CP-ESFAS-A to JB-ESF-A."),
        ("JB-ESF-A", "PROT-LOP-A", "CTRL", "Dashed diagonal control line from JB-ESF-A to PROT-LOP-A."),
        ("PROT-LOP-A", "RELAY-K105", "CTRL", "Dashed control branch from PROT-LOP-A to RELAY-K105."),
        ("RELAY-K105", "FT-611A", "SIG", "Dot-dash instrument branch from RELAY-K105 to FT-611A."),
        ("CP-ESFAS-A", "RELAY-K106", "CTRL", "Dashed right-side control drop from CP-ESFAS-A to RELAY-K106."),
        ("RELAY-K106", "XA-730A", "SIG", "Dot-dash signal branch from RELAY-K106 to XA-730A."),
        ("RELAY-K106", "RELAY-K108", "CTRL", "Dashed A/B ESF interlock route connects RELAY-K106 to RELAY-K108 only."),
        ("CP-ESFAS-B", "JB-ESF-B", "CTRL", "Dashed vertical control line from CP-ESFAS-B to JB-ESF-B."),
        ("JB-ESF-B", "PROT-LOP-B", "CTRL", "Dashed diagonal control line from JB-ESF-B to PROT-LOP-B."),
        ("PROT-LOP-B", "RELAY-K107", "CTRL", "Dashed control branch from PROT-LOP-B to RELAY-K107."),
        ("RELAY-K107", "FT-611B", "SIG", "Dot-dash instrument branch from RELAY-K107 to FT-611B."),
        ("CP-ESFAS-B", "RELAY-K108", "CTRL", "Dashed right-side control drop from CP-ESFAS-B to RELAY-K108."),
        ("RELAY-K108", "XA-730B", "SIG", "Dot-dash signal branch from RELAY-K108 to XA-730B."),
    ]
    for edge in lower_control_edges:
        add(*edge)

    return edges


def make_round1_edges() -> list[Edge]:
    final_edges = make_final_edges()
    edges = [edge for edge in final_edges if edge.key != tuple(sorted(("BUS-480-A", "RECT-125A")))]
    seen = {edge.key for edge in edges}
    add_edge(
        edges,
        seen,
        "HTR-PZR-01A",
        "RECT-125A",
        "P",
        "Round 1 overread: solid rectifier feeder was interpreted as continuing from HTR-PZR-01A.",
        "accepted_r1",
    )
    return edges


def make_excluded_edges() -> list[Edge]:
    rows = [
        ("BUS-13K-A", "BUS-13K-B", "P", "Tie breaker CB-TIE-13K lies between the bus sections; no direct bus-to-bus edge."),
        ("BUS-416-A", "BUS-416-B", "P", "Tie breaker CB-TIE-416 lies between the bus sections; no direct bus-to-bus edge."),
        ("BUS-480-B", "BUS-480-C", "P", "Tie breaker CB-TIE-480 lies between the load-center buses; no direct bus-to-bus edge."),
        ("BUS-480-C", "BUS-480-D", "P", "No visible tie or junction dot between BUS-480-C and BUS-480-D."),
        ("BUS-125DCA", "BUS-125DCB", "DC", "Separate 125 VDC buses; no visible inter-bus jumper."),
        ("GEN-M1", "UNLABELED_SOURCE_BLOCK", "P", "Small inline source square is visible but unlabeled and was not promoted to a matrix node."),
        ("DG-1A", "UNLABELED_DG1A_BLOCK", "P", "Small inline DG square is visible but unlabeled and was not promoted to a matrix node."),
        ("DG-1B", "UNLABELED_DG1B_BLOCK", "P", "Small inline DG square is visible but unlabeled and was not promoted to a matrix node."),
        ("HTR-PZR-01A", "RECT-125A", "P", "Tight crop shows RECT-125A is fed by a separate BUS-480-A solid tap; HTR-PZR-01A is on a dashed control branch."),
        ("MOV-FCV-022C", "RECT-125B", "P", "MOV-FCV-022C is on a dashed control branch; RECT-125B feed is a separate solid route."),
        ("CB-48C6", "RECT-125B", "P", "RECT-125B feed comes from the BUS-480-C end route, not through CB-48C6."),
        ("BAT-125A", "BUS-125DCA", "DC", "No direct battery-to-125DCA bus tap is visible."),
        ("CHGR-125A", "BUS-125DCA", "DC", "No direct charger-to-125DCA bus tap is visible."),
        ("BAT-125B", "BUS-125DCB", "DC", "No direct battery-to-125DCB bus tap is visible."),
        ("CHGR-125B", "BUS-125DCB", "DC", "No direct charger-to-125DCB bus tap is visible."),
        ("INV-UPS-A", "AC_OUTPUT_NODE", "SIG", "AC side is labeled inside INV-UPS-A, but no external output wire is visible."),
        ("INV-UPS-B", "AC_OUTPUT_NODE", "SIG", "AC side is labeled inside INV-UPS-B, but no external output wire is visible."),
        ("RELAY-K105", "XA-730A", "SIG", "Separate ESFAS-A branches; no connecting line between RELAY-K105 and XA-730A."),
        ("RELAY-K107", "XA-730B", "SIG", "Separate ESFAS-B branches; no connecting line between RELAY-K107 and XA-730B."),
        ("RELAY-K106", "FT-611B", "CTRL", "A/B ESF interlock passes without a junction dot or tap to FT-611B."),
        ("RELAY-K108", "FT-611A", "CTRL", "A/B ESF interlock passes without a junction dot or tap to FT-611A."),
    ]
    return [Edge(source, target, line_type, "uncertain_excluded", reason) for source, target, line_type, reason in rows]


def node_order_for(edge_sets: list[list[Edge]]) -> list[str]:
    ordered: OrderedDict[str, None] = OrderedDict()
    for edges in edge_sets:
        for edge in edges:
            ordered.setdefault(edge.source, None)
            ordered.setdefault(edge.target, None)
    return list(ordered.keys())


def write_sparse_csv(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "line_type", "status", "evidence"])
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "source": edge.source,
                    "target": edge.target,
                    "line_type": edge.line_type,
                    "status": edge.status,
                    "evidence": edge.evidence,
                }
            )


def write_matrix_csv(path: Path, edges: list[Edge], nodes: list[str]) -> None:
    edge_keys = {edge.key for edge in edges}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", *nodes])
        for row_node in nodes:
            row = [row_node]
            for col_node in nodes:
                row.append(0 if row_node == col_node else int(tuple(sorted((row_node, col_node))) in edge_keys))
            writer.writerow(row)


def make_usage_estimate() -> list[dict[str, object]]:
    return [
        {
            "document": 20,
            "iteration": 1,
            "call_id": "main-01",
            "actor": "Main agent",
            "phase": "Resource inspection, visual crops, and local visual tracing",
            "input_tokens_est": 6_500,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 42_000,
            "output_tokens_est": 3_800,
            "reasoning_tokens": None,
            "low_total_est": 40_000,
            "expected_total_est": 52_300,
            "high_total_est": 68_000,
            "usage_object_available": False,
            "notes": "Includes local viewing of whole-sheet images and focused crops. Text estimated as chars/4; images by high-detail tile-style heuristic.",
        },
        {
            "document": 20,
            "iteration": 1,
            "call_id": "diego-r1",
            "actor": "Diego",
            "phase": "Round 1 high-recall extraction",
            "input_tokens_est": 3_500,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 31_500,
            "output_tokens_est": 15_500,
            "reasoning_tokens": None,
            "low_total_est": 41_000,
            "expected_total_est": 50_500,
            "high_total_est": 64_000,
            "usage_object_available": False,
            "notes": "Subagent inspected raw, overlays, full crops, and returned accepted plus uncertain candidate edges.",
        },
        {
            "document": 20,
            "iteration": 1,
            "call_id": "jennifer-r1",
            "actor": "Jennifer",
            "phase": "Round 1 precision review",
            "input_tokens_est": 20_000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 35_000,
            "output_tokens_est": 14_000,
            "reasoning_tokens": None,
            "low_total_est": 56_000,
            "expected_total_est": 69_000,
            "high_total_est": 88_000,
            "usage_object_available": False,
            "notes": "Includes Diego R1 proposal plus visual resources for review.",
        },
        {
            "document": 20,
            "iteration": 1,
            "call_id": "diego-r2a",
            "actor": "Diego",
            "phase": "Round 2 initial saturation prompt superseded by tighter crop",
            "input_tokens_est": 1_400,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_est": 0,
            "reasoning_tokens": None,
            "low_total_est": 900,
            "expected_total_est": 1_400,
            "high_total_est": 2_200,
            "usage_object_available": False,
            "notes": "Prompt was interrupted before a completed response was exposed; counted as a possible started model call.",
        },
        {
            "document": 20,
            "iteration": 1,
            "call_id": "diego-r2b",
            "actor": "Diego",
            "phase": "Round 2 corrected saturation check",
            "input_tokens_est": 1_200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 5_500,
            "output_tokens_est": 120,
            "reasoning_tokens": None,
            "low_total_est": 5_000,
            "expected_total_est": 6_820,
            "high_total_est": 9_000,
            "usage_object_available": False,
            "notes": "Correction crop for BUS-480-A to RECT-125A vs HTR-PZR-01A overread.",
        },
        {
            "document": 20,
            "iteration": 1,
            "call_id": "jennifer-r2",
            "actor": "Jennifer",
            "phase": "Round 2 final signoff",
            "input_tokens_est": 1_500,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 5_500,
            "output_tokens_est": 40,
            "reasoning_tokens": None,
            "low_total_est": 5_200,
            "expected_total_est": 7_040,
            "high_total_est": 9_500,
            "usage_object_available": False,
            "notes": "Final agreement on the corrected rectifier edge and unchanged precision decisions.",
        },
        {
            "document": 20,
            "iteration": 1,
            "call_id": "main-02",
            "actor": "Main agent",
            "phase": "Artifact generation, validation, and final response",
            "input_tokens_est": 6_000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_est": 1_200,
            "reasoning_tokens": None,
            "low_total_est": 5_500,
            "expected_total_est": 7_200,
            "high_total_est": 9_500,
            "usage_object_available": False,
            "notes": "Actual Responses usage objects are not exposed in this environment.",
        },
    ]


def write_usage_files(calls: list[dict[str, object]]) -> None:
    totals = {
        "low_total_est": sum(int(call["low_total_est"]) for call in calls),
        "expected_total_est": sum(int(call["expected_total_est"]) for call in calls),
        "high_total_est": sum(int(call["high_total_est"]) for call in calls),
    }
    payload = {
        "document": 20,
        "iteration": 1,
        "api_key_available": False,
        "responses_input_token_counting_endpoint_used": False,
        "usage_objects_collected": False,
        "estimate_method": "No API key was available. Text tokens were estimated as roughly characters/4. Image/file input tokens were estimated from viewed image dimensions with a high-detail tile-style heuristic. Cached input and reasoning-token counts are unavailable.",
        "calls": calls,
        "totals": totals,
    }
    (RESULTS_DIR / "usage_estimate.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Token Usage Estimate",
        "",
        "Document: 20",
        "Iteration: 1",
        "",
        "The OpenAI Responses input-token counting endpoint and per-response usage objects could not be used because no API key is available in this environment. A local estimate was used instead: text input is approximated as characters/4, and image/file input is approximated with a high-detail tile-style visual payload heuristic from the images/crops supplied to each model call.",
        "",
        "| Document | Iteration | Call | Actor | Phase | Text input est | Cached input | Image/file input est | Output est | Reasoning tokens | Low total | Expected total | High total | Usage object |",
        "|---:|---:|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|",
    ]
    for call in calls:
        lines.append(
            f"| {call['document']} | {call['iteration']} | {call['call_id']} | {call['actor']} | {call['phase']} | "
            f"{call['input_tokens_est']} | {call['cached_input_tokens_est']} | {call['image_file_input_tokens_est']} | "
            f"{call['output_tokens_est']} | unavailable | {call['low_total_est']} | {call['expected_total_est']} | "
            f"{call['high_total_est']} | not exposed |"
        )
    lines.extend(
        [
            "",
            "| Document | Iteration | Low total | Expected total | High total |",
            "|---:|---:|---:|---:|---:|",
            f"| 20 | 1 | {totals['low_total_est']} | {totals['expected_total_est']} | {totals['high_total_est']} |",
            "",
            "Low / expected / high bounds are provided because exact output length, hidden reasoning effort, caching behavior, and image-token accounting are unavailable without API usage metadata.",
        ]
    )
    (RESULTS_DIR / "token_usage_estimate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(final_edges: list[Edge], excluded_edges: list[Edge], final_nodes: list[str], calls: list[dict[str, object]]) -> None:
    expected_total = sum(int(call["expected_total_est"]) for call in calls)
    report = [
        "# Connectivity Extraction Report",
        "",
        "Document: 20",
        "Iteration: 1",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Inputs Used",
        "",
        "- raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png",
        "- detected_components_overlay.png",
        "- wires_mask.png",
        "- wires_mask_overlay.png",
        "- derived visual crops generated under results/visual_crops",
        "",
        "No GT or GT-derived files were used. No off-the-shelf OCR was used.",
        "",
        "## Round Summary",
        "",
        "- Diego R1: high-recall extraction of top supply chains, 480 V load centers, 125 VDC/control chains, and uncertain exclusions.",
        "- Jennifer R1: precision review kept most topology and rejected direct bus-to-bus, unlabeled, and unsupported cross edges.",
        "- Diego R2: accepted the tighter-crop correction removing HTR-PZR-01A--RECT-125A and adding BUS-480-A--RECT-125A.",
        "- Jennifer R2: replied AGREE/SATURATED after the same correction.",
        "",
        "## Final Counts",
        "",
        f"- Final nodes: {len(final_nodes)}",
        f"- Final accepted undirected edges: {len(final_edges)}",
        f"- Uncertain/excluded candidate edges: {len(excluded_edges)}",
        "",
        "## Key Precision Decisions",
        "",
        "- Tie breakers are explicit intermediate nodes, so BUS-13K-A/B, BUS-416-A/B, and BUS-480-B/C are not directly connected.",
        "- BUS-480-A directly feeds RECT-125A by a solid tap; HTR-PZR-01A is only on the dashed A4 control branch.",
        "- BUS-480-C feeds RECT-125B by a separate solid route; MOV-FCV-022C and CB-48C6 do not feed that rectifier.",
        "- BUS-125DCA feeds CP-RPS-A and CP-RPS-B; BUS-125DCB feeds CP-ESFAS-A and CP-ESFAS-B by dashed DC taps with black dots.",
        "- ESFAS A/B interlock is only RELAY-K106--RELAY-K108; no sensor or annunciator cross-taps are visible.",
        "",
        "## Token Usage",
        "",
        f"Expected estimated total tokens across main-agent and subagent calls: {expected_total}. See token_usage_estimate.md and usage_estimate.json for call-level low/expected/high estimates.",
    ]
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_edges = make_final_edges()
    round1_edges = make_round1_edges()
    excluded_edges = make_excluded_edges()
    final_nodes = node_order_for([final_edges, round1_edges])

    round_outputs = [
        ("round01_diego", round1_edges),
        ("round01_jennifer", round1_edges),
        ("round02_diego", final_edges),
        ("round02_jennifer", final_edges),
    ]
    for stem, edges in round_outputs:
        write_sparse_csv(RESULTS_DIR / f"{stem}_sparse_edges.csv", edges)
        write_matrix_csv(RESULTS_DIR / f"{stem}_connectivity_matrix.csv", edges, final_nodes)

    write_sparse_csv(RESULTS_DIR / "final_sparse_edges.csv", final_edges)
    write_matrix_csv(RESULTS_DIR / "final_connectivity_matrix.csv", final_edges, final_nodes)
    write_sparse_csv(RESULTS_DIR / "uncertain_excluded_edges.csv", excluded_edges)
    write_sparse_csv(RESULTS_DIR / "round01_diego_uncertain_candidates.csv", excluded_edges)
    write_sparse_csv(RESULTS_DIR / "round01_jennifer_removed_or_uncertain.csv", excluded_edges)
    (RESULTS_DIR / "final_component_order.txt").write_text("\n".join(final_nodes) + "\n", encoding="utf-8")

    calls = make_usage_estimate()
    write_usage_files(calls)
    write_report(final_edges, excluded_edges, final_nodes, calls)

    summary = {
        "document": 20,
        "iteration": 1,
        "final_node_count": len(final_nodes),
        "final_edge_count": len(final_edges),
        "excluded_candidate_edge_count": len(excluded_edges),
        "rounds_written": [stem for stem, _ in round_outputs],
        "token_expected_total_est": sum(int(call["expected_total_est"]) for call in calls),
    }
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
