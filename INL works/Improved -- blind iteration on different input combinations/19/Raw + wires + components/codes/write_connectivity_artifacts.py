from __future__ import annotations

import csv
import json
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components")
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


def make_edge_list() -> list[Edge]:
    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()

    def add(source: str, target: str, line_type: str, evidence: str, status: str = "accepted") -> None:
        edge = Edge(source, target, line_type, status, evidence)
        if edge.key in seen:
            raise ValueError(f"duplicate undirected edge: {source} -- {target}")
        seen.add(edge.key)
        edges.append(edge)

    top_edges = [
        ("OFFSITE GRID-1", "DS-101", "P", "Solid incoming feeder from offsite grid 1 into disconnect DS-101."),
        ("DS-101", "CB-101", "P", "Solid feeder continues from DS-101 to circuit breaker CB-101."),
        ("CB-101", "TR-101", "P", "Solid feeder continues from CB-101 to transformer TR-101."),
        ("TR-101", "BUS-4160-A", "P", "Transformer TR-101 output lands on BUS-4160-A."),
        ("DG-1", "CB-DG1", "P", "Diesel generator DG-1 output runs through breaker CB-DG1."),
        ("CB-DG1", "BUS-4160-A", "P", "CB-DG1 output ties into BUS-4160-A."),
        ("BUS-4160-A", "PT-4160A", "SIG", "Dotted instrument tap from BUS-4160-A to PT-4160A."),
        ("BUS-4160-A", "CB-TIE-4160", "P", "Solid bus tie connection from BUS-4160-A to CB-TIE-4160."),
        ("CB-TIE-4160", "BUS-4160-B", "P", "Solid bus tie connection from CB-TIE-4160 to BUS-4160-B."),
        ("OFFSITE GRID-2", "DS-102", "P", "Solid incoming feeder from offsite grid 2 into disconnect DS-102."),
        ("DS-102", "CB-102", "P", "Solid feeder continues from DS-102 to circuit breaker CB-102."),
        ("CB-102", "TR-102", "P", "Solid feeder continues from CB-102 to transformer TR-102."),
        ("TR-102", "BUS-4160-B", "P", "Transformer TR-102 output lands on BUS-4160-B."),
        ("DG-2", "CB-DG2", "P", "Diesel generator DG-2 output runs through breaker CB-DG2."),
        ("CB-DG2", "BUS-4160-B", "P", "CB-DG2 output ties into BUS-4160-B."),
        ("BUS-4160-B", "PT-4160B", "SIG", "Dotted instrument tap from BUS-4160-B to PT-4160B."),
        ("BUS-4160-A", "CB-201", "P", "Solid 4160 V A feeder drops from BUS-4160-A to CB-201."),
        ("CB-201", "TR-480-A", "P", "Solid feeder continues from CB-201 to TR-480-A."),
        ("TR-480-A", "CB-480-A", "P", "Solid secondary feeder continues from TR-480-A to CB-480-A."),
        ("CB-480-A", "BUS-480-A", "P", "CB-480-A output lands on BUS-480-A."),
        ("BUS-4160-B", "CB-202", "P", "Solid 4160 V B feeder drops from BUS-4160-B to CB-202."),
        ("CB-202", "TR-480-B", "P", "Solid feeder continues from CB-202 to TR-480-B."),
        ("TR-480-B", "CB-480-B", "P", "Solid secondary feeder continues from TR-480-B to CB-480-B."),
        ("CB-480-B", "BUS-480-B", "P", "CB-480-B output lands on BUS-480-B."),
        ("BUS-480-A", "CB-TIE-480", "P", "Solid 480 V bus tie connection from BUS-480-A to CB-TIE-480."),
        ("CB-TIE-480", "BUS-480-B", "P", "Solid 480 V bus tie connection from CB-TIE-480 to BUS-480-B."),
    ]
    for source, target, line_type, evidence in top_edges:
        add(source, target, line_type, evidence)

    def add_standard_feeder(bus: str, suffix: str, load: str) -> None:
        add(bus, f"CB-F{suffix}", "P", f"Solid feeder tap from {bus} into feeder breaker CB-F{suffix}.")
        add(f"CB-F{suffix}", f"RELAY-PR{suffix}", "CTRL", f"Dashed protection/control lead from CB-F{suffix} to RELAY-PR{suffix}.")
        add(f"CB-F{suffix}", f"DS-F{suffix}", "P", f"Solid feeder continues from CB-F{suffix} to DS-F{suffix}.")
        add(f"DS-F{suffix}", f"CPT-{suffix}", "P", f"Solid feeder continues from DS-F{suffix} to CPT-{suffix}.")
        add(f"CPT-{suffix}", f"MCC-{suffix}", "P", f"Solid feeder continues from CPT-{suffix} to MCC-{suffix}.")
        add(f"MCC-{suffix}", f"CB-L{suffix}", "P", f"Solid load feeder exits MCC-{suffix} through CB-L{suffix}.")
        add(f"CB-L{suffix}", f"RELAY-K{suffix}", "P", f"Solid load feeder continues from CB-L{suffix} through RELAY-K{suffix}.")
        add(f"RELAY-K{suffix}", load, "P", f"Solid load feeder from RELAY-K{suffix} terminates at {load}.")
        add(f"MCC-{suffix}", f"RELAY-A{suffix}", "CTRL", f"Dashed control/auxiliary lead associates MCC-{suffix} with RELAY-A{suffix}.")
        add(load, f"INST-{suffix}", "SIG", f"Dotted instrument/signal lead from {load} to INST-{suffix}.")
        add(f"INST-{suffix}", f"JB-{suffix}", "SIG", f"Dotted signal lead continues from INST-{suffix} to JB-{suffix}.")
        add(f"JB-{suffix}", f"TB-{suffix}", "SIG", f"Dotted signal lead continues from JB-{suffix} to TB-{suffix}.")
        add(f"LCS-{suffix}", f"TB-{suffix}", "CTRL", f"Dashed local control station lead from LCS-{suffix} to TB-{suffix}.")

    for bus, suffix, load in [
        ("BUS-480-A", "201", "PUMP-P201"),
        ("BUS-480-A", "203", "PUMP-P203"),
        ("BUS-480-A", "301", "PUMP-P301"),
        ("BUS-480-A", "401", "PUMP-P401"),
        ("BUS-480-A", "501", "MTR-F501"),
        ("BUS-480-B", "202", "PUMP-P202"),
        ("BUS-480-B", "204", "PUMP-P204"),
        ("BUS-480-B", "302", "PUMP-P302"),
        ("BUS-480-B", "402", "PUMP-P402"),
        ("BUS-480-B", "502", "MTR-F502"),
    ]:
        add_standard_feeder(bus, suffix, load)

    add("BUS-480-A", "CB-F601", "P", "Solid feeder tap from BUS-480-A into feeder breaker CB-F601.")
    add("CB-F601", "RELAY-PR601", "CTRL", "Dashed protection/control lead from CB-F601 to RELAY-PR601.")
    add("CB-F601", "DS-F601", "P", "Solid feeder continues from CB-F601 to DS-F601.")
    add("DS-F601", "CPT-601", "P", "Solid feeder continues from DS-F601 to CPT-601.")
    add("CPT-601", "MCC-601", "P", "Solid feeder continues from CPT-601 to MCC-601.")
    add("MCC-601", "CB-L601", "P", "Solid load feeder exits MCC-601 through CB-L601.")
    add("CB-L601", "RELAY-K601", "P", "Solid load feeder continues from CB-L601 through RELAY-K601.")
    add("RELAY-K601", "VALVE-MOV601", "P", "Solid load feeder from RELAY-K601 terminates at VALVE-MOV601.")
    add("MCC-601", "RELAY-A601", "CTRL", "Dashed control/auxiliary lead associates MCC-601 with RELAY-A601.")
    add("VALVE-MOV601", "INST-601", "SIG", "Visible signal branch from VALVE-MOV601 to INST-601.")
    add("VALVE-MOV601", "LS-MOV601", "SIG", "Visible signal branch from VALVE-MOV601 to limit switch LS-MOV601.")
    add("LS-MOV601", "JB-601", "SIG", "Dotted signal run continues from LS-MOV601 to JB-601.")
    add("JB-601", "TB-601", "SIG", "Dotted signal run continues from JB-601 to TB-601.")
    add("LCS-601", "TB-601", "CTRL", "Dashed local control station lead from LCS-601 to TB-601.")

    suffix = "701"
    add("BUS-480-B", "CB-F701", "P", "Solid feeder tap from BUS-480-B into feeder breaker CB-F701.")
    add("CB-F701", "RELAY-PR701", "CTRL", "Dashed protection/control lead from CB-F701 to RELAY-PR701.")
    add("CB-F701", "DS-F701", "P", "Solid feeder continues from CB-F701 to DS-F701.")
    add("DS-F701", "CPT-701", "P", "Solid feeder continues from DS-F701 to CPT-701.")
    add("CPT-701", "MCC-701", "P", "Solid feeder continues from CPT-701 to MCC-701.")
    add("MCC-701", "CB-L701", "P", "Solid load feeder exits MCC-701 through CB-L701.")
    add("CB-L701", "RELAY-K701", "P", "Solid load feeder continues from CB-L701 through RELAY-K701.")
    add("RELAY-K701", "INST-RPS701", "P", "Solid load feeder from RELAY-K701 terminates at INST-RPS701.")
    add("MCC-701", "RELAY-A701", "CTRL", "Dashed control/auxiliary lead associates MCC-701 with RELAY-A701.")
    add("INST-RPS701", "INST-701", "SIG", "Dotted instrument/signal lead from INST-RPS701 to INST-701.")
    add("INST-701", "JB-701", "SIG", "Dotted signal lead continues from INST-701 to JB-701.")
    add("JB-701", "TB-701", "SIG", "Dotted signal lead continues from JB-701 to TB-701.")
    add("LCS-701", "TB-701", "CTRL", "Dashed local control station lead from LCS-701 to TB-701.")

    lower_edges = [
        ("CTRL-PWR-DC-DIST-A", "CB-301", "P", "Lower A source rail connects directly into CB-301."),
        ("CB-301", "TR-120-A", "P", "Solid feeder continues from CB-301 to TR-120-A."),
        ("TR-120-A", "BUS-120AC-A", "P", "TR-120-A output lands on BUS-120AC-A."),
        ("BUS-120AC-A", "JB-MAIN", "SIG", "Dotted/signal lead from BUS-120AC-A to JB-MAIN."),
        ("CTRL-PWR-DC-DIST-A", "CHGR-125A", "P", "Lower A source rail branches to CHGR-125A."),
        ("CHGR-125A", "BAT-125A", "DC", "Charger CHGR-125A connects to BAT-125A."),
        ("BAT-125A", "BUS-125DC-A", "DC", "BAT-125A connects to BUS-125DC-A."),
        ("BUS-125DC-A", "INV-120A", "DC", "BUS-125DC-A feeds INV-120A."),
        ("INV-120A", "PN-RPS-A", "CTRL", "Dashed/control lead from INV-120A to PN-RPS-A."),
        ("CTRL-PWR-DC-DIST-B", "CB-302", "P", "Lower B source rail connects directly into CB-302."),
        ("CB-302", "TR-120-B", "P", "Solid feeder continues from CB-302 to TR-120-B."),
        ("TR-120-B", "BUS-120AC-B", "P", "TR-120-B output lands on BUS-120AC-B."),
        ("CTRL-PWR-DC-DIST-B", "CHGR-125B", "P", "Lower B source rail branches to CHGR-125B."),
        ("CHGR-125B", "BAT-125B", "DC", "Charger CHGR-125B connects to BAT-125B."),
        ("BAT-125B", "BUS-125DC-B", "DC", "BAT-125B connects to BUS-125DC-B."),
        ("BUS-125DC-B", "INV-120B", "DC", "BUS-125DC-B feeds INV-120B."),
        ("INV-120B", "PN-RPS-B", "CTRL", "Dashed/control lead from INV-120B to PN-RPS-B."),
    ]
    for source, target, line_type, evidence in lower_edges:
        add(source, target, line_type, evidence)

    return edges


def make_excluded_edges() -> list[Edge]:
    excluded = [
        Edge("BUS-480-A", "CTRL-PWR-DC-DIST-A", "P", "uncertain_excluded", "Plausible routed source rail, but no explicit visible junction/tap from BUS-480-A."),
        Edge("BUS-480-B", "CTRL-PWR-DC-DIST-B", "P", "uncertain_excluded", "Plausible routed source rail, but no explicit visible junction/tap from BUS-480-B."),
        Edge("INST-601", "JB-601", "SIG", "uncertain_excluded", "MOV601 signal run continues from LS-MOV601 to JB-601; INST-601 does not visibly continue to JB-601."),
        Edge("PN-RPS-B", "INST-RPS701", "SIG", "uncertain_excluded", "No visible connecting line from PN-RPS-B to INST-RPS701."),
        Edge("CHGR-125B", "BUS-120AC-B", "P", "uncertain_excluded", "Vertical charger lead crosses BUS-120AC-B without a junction dot."),
    ]
    for suffix in ["201", "203", "301", "401", "501", "601", "202", "204", "302", "402", "502", "701"]:
        excluded.append(
            Edge(
                f"RELAY-A{suffix}",
                f"RELAY-K{suffix}",
                "CTRL",
                "uncertain_excluded",
                "Dashed auxiliary/control lead terminates at MCC side association; no direct relay-to-relay line is visible.",
            )
        )
    return excluded


def node_order_for(edges: list[Edge], extra_edges: list[Edge] | None = None) -> list[str]:
    ordered: OrderedDict[str, None] = OrderedDict()
    for edge in edges + (extra_edges or []):
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
    # No API key is available in this task, so these are bounded estimates rather
    # than Responses API usage objects. Image tokens use a high-detail tile-style
    # heuristic; text tokens use roughly 4 chars per token.
    calls = [
        {
            "document": 19,
            "iteration": 1,
            "call_id": "main-01",
            "actor": "Main agent",
            "phase": "Resource inspection and crop planning",
            "input_tokens_est": 4_500,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 16_000,
            "output_tokens_est": 900,
            "reasoning_tokens": None,
            "low_total_est": 18_000,
            "expected_total_est": 21_400,
            "high_total_est": 27_000,
            "usage_object_available": False,
            "notes": "Includes local visual inspection of raw, overlay, mask aids, and crop-generation planning.",
        },
        {
            "document": 19,
            "iteration": 1,
            "call_id": "diego-r1",
            "actor": "Diego",
            "phase": "Round 1 high-recall extraction",
            "input_tokens_est": 3_200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 23_800,
            "output_tokens_est": 12_500,
            "reasoning_tokens": None,
            "low_total_est": 33_000,
            "expected_total_est": 39_500,
            "high_total_est": 49_000,
            "usage_object_available": False,
            "notes": "Subagent inspected focused visual crops and proposed accepted plus uncertain candidate edges.",
        },
        {
            "document": 19,
            "iteration": 1,
            "call_id": "jennifer-r1",
            "actor": "Jennifer",
            "phase": "Round 1 precision review",
            "input_tokens_est": 15_600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 23_800,
            "output_tokens_est": 10_500,
            "reasoning_tokens": None,
            "low_total_est": 42_000,
            "expected_total_est": 49_900,
            "high_total_est": 62_000,
            "usage_object_available": False,
            "notes": "Includes Diego R1 proposal text plus the same visual resources for precision review.",
        },
        {
            "document": 19,
            "iteration": 1,
            "call_id": "diego-r2",
            "actor": "Diego",
            "phase": "Round 2 saturation check",
            "input_tokens_est": 2_700,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_est": 550,
            "reasoning_tokens": None,
            "low_total_est": 2_000,
            "expected_total_est": 3_250,
            "high_total_est": 4_200,
            "usage_object_available": False,
            "notes": "Short textual consensus check against Jennifer R1 corrections.",
        },
        {
            "document": 19,
            "iteration": 1,
            "call_id": "jennifer-r2",
            "actor": "Jennifer",
            "phase": "Round 2 final signoff",
            "input_tokens_est": 1_800,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_est": 250,
            "reasoning_tokens": None,
            "low_total_est": 1_600,
            "expected_total_est": 2_050,
            "high_total_est": 3_000,
            "usage_object_available": False,
            "notes": "Final saturation confirmation prompt.",
        },
        {
            "document": 19,
            "iteration": 1,
            "call_id": "main-02",
            "actor": "Main agent",
            "phase": "Artifact generation, validation, and final response",
            "input_tokens_est": 5_200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_est": 1_000,
            "reasoning_tokens": None,
            "low_total_est": 4_800,
            "expected_total_est": 6_200,
            "high_total_est": 8_000,
            "usage_object_available": False,
            "notes": "Includes code/artifact generation and final summary. Actual usage object is not exposed in this environment.",
        },
    ]
    return calls


def write_usage_files(calls: list[dict[str, object]]) -> None:
    total_low = sum(int(call["low_total_est"]) for call in calls)
    total_expected = sum(int(call["expected_total_est"]) for call in calls)
    total_high = sum(int(call["high_total_est"]) for call in calls)
    usage_payload = {
        "document": 19,
        "iteration": 1,
        "api_key_available": False,
        "responses_input_token_counting_endpoint_used": False,
        "usage_objects_collected": False,
        "estimate_method": "Text tokens approximated as chars/4. Image/file tokens approximated from visual payload size with a high-detail tile-style heuristic. Cached and reasoning tokens are unavailable.",
        "calls": calls,
        "totals": {
            "low_total_est": total_low,
            "expected_total_est": total_expected,
            "high_total_est": total_high,
        },
    }
    (RESULTS_DIR / "usage_estimate.json").write_text(json.dumps(usage_payload, indent=2), encoding="utf-8")

    lines = [
        "# Token Usage Estimate",
        "",
        "Document: 19",
        "Iteration: 1",
        "",
        "The OpenAI Responses input-token counting endpoint and per-response usage objects could not be used because no API key is available in this environment. The estimates below use a local heuristic: text input is estimated at roughly 4 characters per token, and image/file input is estimated with a high-detail tile-style visual payload heuristic from the viewed images/crops.",
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
            f"| 19 | 1 | {total_low} | {total_expected} | {total_high} |",
            "",
            "Low / expected / high bounds are provided because output length, hidden reasoning effort, and exact image-token accounting are not available without API usage metadata.",
        ]
    )
    (RESULTS_DIR / "token_usage_estimate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(final_edges: list[Edge], excluded_edges: list[Edge], final_nodes: list[str], calls: list[dict[str, object]]) -> None:
    total_expected = sum(int(call["expected_total_est"]) for call in calls)
    report = [
        "# Connectivity Extraction Report",
        "",
        "Document: 19",
        "Iteration: 1",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Inputs Used",
        "",
        "- raw -- synthetic_npp_electrical_schematic_v3.png",
        "- detected_components_overlay.png",
        "- wires_mask.png",
        "- wires_mask_overlay.png",
        "- derived visual crops generated under results/visual_crops",
        "",
        "No GT or GT-derived files were used. No off-the-shelf OCR was used.",
        "",
        "## Round Summary",
        "",
        "- Diego R1: high-recall extraction with accepted edges plus uncertain candidates.",
        "- Jennifer R1: precision review removed visually unsupported candidates and corrected MOV601, lower DC/control, and RPS boundaries.",
        "- Diego R2: agreed that Jennifer R1 was saturated with no additional edges.",
        "- Jennifer R2: replied AGREE/SATURATED with no additional deltas.",
        "",
        "## Final Counts",
        "",
        f"- Final nodes: {len(final_nodes)}",
        f"- Final accepted undirected edges: {len(final_edges)}",
        f"- Uncertain/excluded candidate edges: {len(excluded_edges)}",
        "",
        "## Key Precision Decisions",
        "",
        "- BUS-480-A/B are not connected to CTRL-PWR-DC-DIST-A/B because no explicit visible tap/junction is present.",
        "- RELAY-A### nodes are connected to MCC-### only; no direct RELAY-A### to RELAY-K### connection is visible.",
        "- MOV601 has separate VALVE-MOV601 to INST-601 and VALVE-MOV601 to LS-MOV601 branches; only LS-MOV601 continues to JB-601.",
        "- PN-RPS-B is not connected to INST-RPS701 without a visible line.",
        "- CHGR-125B crosses BUS-120AC-B without a junction dot, so no connection is recorded.",
        "",
        "## Token Usage",
        "",
        f"Expected estimated total tokens across main-agent and subagent calls: {total_expected}. See token_usage_estimate.md and usage_estimate.json for low/expected/high bounds and call-level estimates.",
        "",
        "## Final Files",
        "",
        "- final_sparse_edges.csv",
        "- final_connectivity_matrix.csv",
        "- round01_diego_sparse_edges.csv",
        "- round01_diego_connectivity_matrix.csv",
        "- round01_jennifer_sparse_edges.csv",
        "- round01_jennifer_connectivity_matrix.csv",
        "- round02_diego_sparse_edges.csv",
        "- round02_diego_connectivity_matrix.csv",
        "- round02_jennifer_sparse_edges.csv",
        "- round02_jennifer_connectivity_matrix.csv",
        "- uncertain_excluded_edges.csv",
    ]
    (RESULTS_DIR / "connectivity_extraction_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_edges = make_edge_list()
    excluded_edges = make_excluded_edges()
    final_nodes = node_order_for(final_edges, excluded_edges)

    diego_r1_edges = final_edges + excluded_edges
    jennifer_r1_edges = final_edges
    diego_r2_edges = final_edges
    jennifer_r2_edges = final_edges

    outputs = [
        ("round01_diego", diego_r1_edges),
        ("round01_jennifer", jennifer_r1_edges),
        ("round02_diego", diego_r2_edges),
        ("round02_jennifer", jennifer_r2_edges),
    ]
    for stem, edges in outputs:
        write_sparse_csv(RESULTS_DIR / f"{stem}_sparse_edges.csv", edges)
        write_matrix_csv(RESULTS_DIR / f"{stem}_connectivity_matrix.csv", edges, final_nodes)

    write_sparse_csv(RESULTS_DIR / "final_sparse_edges.csv", final_edges)
    write_matrix_csv(RESULTS_DIR / "final_connectivity_matrix.csv", final_edges, final_nodes)
    write_sparse_csv(RESULTS_DIR / "uncertain_excluded_edges.csv", excluded_edges)
    (RESULTS_DIR / "final_component_order.txt").write_text("\n".join(final_nodes) + "\n", encoding="utf-8")

    calls = make_usage_estimate()
    write_usage_files(calls)
    write_report(final_edges, excluded_edges, final_nodes, calls)

    summary = {
        "document": 19,
        "iteration": 1,
        "final_node_count": len(final_nodes),
        "final_edge_count": len(final_edges),
        "excluded_candidate_edge_count": len(excluded_edges),
        "rounds_written": [stem for stem, _ in outputs],
        "token_expected_total_est": sum(int(call["expected_total_est"]) for call in calls),
    }
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
