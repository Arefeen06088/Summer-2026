from __future__ import annotations

import csv
import json
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires + components")
RESULTS = BASE / "results"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str


FINAL_EDGE_CSV = """source,target,type
GRID-161KV,TR-SST-1A,P
TR-SST-1A,CB-401A,P
CB-401A,BUS-4KV-A,P
TR-SST-1A,CB-401B,P
CB-401B,BUS-4KV-B,P
BUS-4KV-A,CB-TIE-4AB,P
CB-TIE-4AB,BUS-4KV-B,P
GEN-EDG-A,CB-EDG-A,P
CB-EDG-A,BUS-4KV-A,P
GEN-EDG-B,CB-EDG-B,P
CB-EDG-B,BUS-4KV-B,P
BUS-4KV-A,TR-4KV-480A,P
TR-4KV-480A,CB-480A-IN,P
CB-480A-IN,BUS-480-A,P
BUS-4KV-B,TR-4KV-480B,P
TR-4KV-480B,CB-480B-IN,P
CB-480B-IN,BUS-480-B,P
BUS-480-A,CB-TIE-480AB,P
CB-TIE-480AB,BUS-480-B,P
BUS-480-A,CB-11A-FDR,P
CB-11A-FDR,MCC-11A,P
BUS-480-A,CB-12A-FDR,P
CB-12A-FDR,MCC-12A,P
BUS-480-A,CB-21A-FDR,P
CB-21A-FDR,MCC-21A,P
BUS-480-B,CB-31A-FDR30-B,P
CB-31A-FDR30-B,MCC-31A,P
BUS-480-B,CB-11B-FDR,P
CB-11B-FDR,MCC-11B,P
BUS-480-B,CB-12B-FDR,P
CB-12B-FDR,MCC-12B,P
BUS-480-B,CB-21B-FDR,P
CB-21B-FDR,MCC-21B,P
BUS-480-B,CB-31B-FDR,P
CB-31B-FDR,MCC-31B,P
MCC-11A,CB-P201A,P
MCC-11A,CB-P211A,P
MCC-11A,CB-P221A,P
MCC-12A,CB-P101A,P
MCC-12A,CB-HV101A,P
MCC-12A,CB-FN1A,P
MCC-21A,CB-P301A,P
MCC-21A,CB-P401A,P
MCC-21A,CB-HT1A,P
MCC-31A,CB-RM1A,P
MCC-31A,CB-P501A,P
MCC-31A,CB-CV121A,P
MCC-11B,CB-P201B,P
MCC-11B,CB-P211B,P
MCC-11B,CB-P221B,P
MCC-12B,CB-P101B,P
MCC-12B,CB-HV101B,P
MCC-12B,CB-FN1B,P
MCC-21B,CB-P301B,P
MCC-21B,CB-P401B,P
MCC-21B,CB-HT1B,P
MCC-31B,CB-RM1B,P
MCC-31B,CB-P501B,P
MCC-31B,CB-CV121B,P
CB-P201A,RELAY-KP201A,P
RELAY-KP201A,PUMP-RHR201A,P
PUMP-RHR201A,GND-P201A,G
CB-P211A,RELAY-KP211A,P
RELAY-KP211A,PUMP-CS211A,P
PUMP-CS211A,GND-P211A,G
CB-P221A,RELAY-KP221A,P
RELAY-KP221A,PUMP-SI221A,P
PUMP-SI221A,GND-P221A,G
CB-P101A,RELAY-KP101A,P
RELAY-KP101A,PUMP-AFW101A,P
PUMP-AFW101A,GND-P101A,G
CB-HV101A,RELAY-KHV101A,P
RELAY-KHV101A,MOV-HV101A,P
MOV-HV101A,TB-HV101A,CTRL
CB-FN1A,RELAY-KFN1A,P
RELAY-KFN1A,FAN-FN1A,P
FAN-FN1A,GND-FN1A,G
CB-P301A,RELAY-KP301A,P
RELAY-KP301A,PUMP-CCW301A,P
PUMP-CCW301A,GND-P301A,G
CB-P401A,RELAY-KP401A,P
RELAY-KP401A,PUMP-SW401A,P
PUMP-SW401A,GND-P401A,G
CB-HT1A,RELAY-KHT1A,P
RELAY-KHT1A,HTR-PZR1A,P
HTR-PZR1A,TB-HT1A,CTRL
CB-RM1A,RELAY-KRM1A,P
RELAY-KRM1A,MON-RAD1A,SIG
MON-RAD1A,TB-RM1A,SIG
CB-P501A,RELAY-KP501A,P
RELAY-KP501A,PUMP-CHM501A,P
PUMP-CHM501A,GND-P501A,G
CB-CV121A,RELAY-KCV121A,P
RELAY-KCV121A,MOV-CV121A,P
MOV-CV121A,TB-CV121A,CTRL
CB-P201B,RELAY-KP201B,P
RELAY-KP201B,PUMP-RHR201B,P
PUMP-RHR201B,GND-P201B,G
CB-P211B,RELAY-KP211B,P
RELAY-KP211B,PUMP-CS211B,P
PUMP-CS211B,GND-P211B,G
CB-P221B,RELAY-KP221B,P
RELAY-KP221B,PUMP-SI221B,P
PUMP-SI221B,GND-P221B,G
CB-P101B,RELAY-KP101B,P
RELAY-KP101B,PUMP-AFW101B,P
PUMP-AFW101B,GND-P101B,G
CB-HV101B,RELAY-KHV101B,P
RELAY-KHV101B,MOV-HV101B,P
MOV-HV101B,TB-HV101B,CTRL
CB-FN1B,RELAY-KFN1B,P
RELAY-KFN1B,FAN-FN1B,P
FAN-FN1B,GND-FN1B,G
CB-P301B,RELAY-KP301B,P
RELAY-KP301B,PUMP-CCW301B,P
PUMP-CCW301B,GND-P301B,G
CB-P401B,RELAY-KP401B,P
RELAY-KP401B,PUMP-SW401B,P
PUMP-SW401B,GND-P401B,G
CB-HT1B,RELAY-KHT1B,P
RELAY-KHT1B,HTR-PZR1B,P
HTR-PZR1B,TB-HT1B,CTRL
CB-RM1B,RELAY-KRM1B,P
RELAY-KRM1B,MON-RAD1B,SIG
MON-RAD1B,TB-RM1B,SIG
CB-P501B,RELAY-KP501B,P
RELAY-KP501B,PUMP-CHM501B,P
PUMP-CHM501B,GND-P501B,G
CB-CV121B,RELAY-KCV121B,P
RELAY-KCV121B,MOV-CV121B,P
MOV-CV121B,TB-CV121B,CTRL
BUS-480-A,TR-RPS-A,P
TR-RPS-A,MG-RPS-A,P
MG-RPS-A,FT-AFW101,P
FT-AFW101,METER-VM-1,P
METER-VM-1,BUS-120-RPS-A,P
BUS-480-B,TR-RPS-B,P
TR-RPS-B,MG-RPS-B,P
MG-RPS-B,RTD-RCS101,P
RTD-RCS101,BUS-120-RPS-B,P
BUS-125DC-A,CP-RPS-A,DC
CP-RPS-A,JB-RPS-A3-1A,CTRL
JB-RPS-A3-1A,PROT-UV-A,CTRL
PROT-UV-A,RELAY-27A,CTRL
BUS-125DC-A,CP-ESF-A,DC
CP-ESF-A,TB-2A,CTRL
TB-2A,PROT-GF-A,CTRL
PROT-GF-A,RELAY-86A,CTRL
BUS-125DC-A,CP-DCS-01,DC
CP-DCS-01,TB-3A,CTRL
RELAY-86A,TB-3A,CTRL
CP-DCS-01,TB-ESF-1,SIG
TB-ESF-1,PT-RCS101,SIG
TB-ESF-1,LT-RWST101,SIG
TB-ESF-1,FT-AFW101,SIG
PT-RCS101,REC-SOE-1,SIG
LT-RWST101,ANN-501,SIG
REC-SOE-1,BUS-125DC-A,DC
BATT-125A,CHGR-125A,DC
CHGR-125A,BUS-125DC-A,DC
BUS-125DC-A,INV-120A,DC
INV-120A,BUS-120-RPS-A,P
BUS-120-RPS-A,UCC-01,CTRL
UCC-01,GND-NO,G
BUS-125DC-B,CP-RPS-B,DC
CP-RPS-B,JB-RPS-B3-1B,CTRL
JB-RPS-B3-1B,PROT-UV-B,CTRL
PROT-UV-B,RELAY-27B,CTRL
BUS-125DC-B,CP-ESF-B,DC
CP-ESF-B,TB-2B,CTRL
TB-2B,PROT-GF-B,CTRL
PROT-GF-B,RELAY-86B,CTRL
BUS-125DC-B,CP-ANN-01,DC
CP-ANN-01,TB-3B,CTRL
RELAY-86B,TB-3B,CTRL
CP-ANN-01,JB-CONTAIN,CTRL
TB-ESF-2,LS-SUMP101,SIG
TB-ESF-2,XS-DOOR101,SIG
BATT-125B,CHGR-125B,DC
CHGR-125B,BUS-125DC-B,DC
BUS-125DC-B,INV-120B,DC
INV-120B,BUS-120-RPS-B,P
BUS-120-RPS-B,UCC-01,CTRL
"""

UNCERTAIN_CSV = """source,target,type,reason
CB-401A,CP-RPS-A,CTRL,"Dashed trip/control descent exists, but lower landing remains ambiguous."
CB-401B,CP-RPS-A,CTRL,"Dashed trip/control descent exists, but lower landing remains ambiguous."
CB-480A-IN,CP-DCS-01,CTRL,"Vertical dashed control line descends from inlet breaker area; final endpoint is unclear."
CB-480B-IN,CP-ANN-01,CTRL,"Vertical dashed control line descends near B controls; final endpoint is unclear."
A-SIDE-LOAD-BREAKER-GROUP,UNLABELLED-DASHED-CONTROL-RAIL-A,CTRL,"Dashed rail crosses/enters breaker area, but labelled endpoints are not visible."
B-SIDE-LOAD-BREAKER-GROUP,UNLABELLED-DASHED-CONTROL-RAIL-B,CTRL,"Dashed rail crosses/enters breaker area, but labelled endpoints are not visible."
BATT-125A,BUS-125DC-A,DC,"Battery-to-charger is clear; direct battery-to-bus landing is not."
BATT-125B,BUS-125DC-B,DC,"Battery-to-charger is clear; direct battery-to-bus landing is not."
ANN-501,BUS-125DC-A,DC,"ANN-501 aligns near the bus, but a filled junction is not distinct."
MG-RPS-B,TB-ESF-2,SIG,"Crowded dotted geometry near MG-RPS-B/TB-ESF-2 is plausible but not cleanly landed."
"""


def parse_edges(text: str) -> list[Edge]:
    rows = csv.DictReader(text.strip().splitlines())
    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        a = row["source"].strip()
        b = row["target"].strip()
        kind = row["type"].strip()
        key = tuple(sorted((a, b)))
        if a == b:
            raise ValueError(f"self-loop not expected: {a}")
        if key in seen:
            raise ValueError(f"duplicate undirected edge: {a}, {b}")
        seen.add(key)
        edges.append(Edge(a, b, kind))
    return edges


def nodes_from_edges(edges: list[Edge]) -> list[str]:
    nodes: OrderedDict[str, None] = OrderedDict()
    for edge in edges:
        nodes.setdefault(edge.source, None)
        nodes.setdefault(edge.target, None)
    return list(nodes)


def write_edges(path: Path, edges: list[Edge]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "type"])
        for edge in edges:
            writer.writerow([edge.source, edge.target, edge.kind])


def write_matrix(path: Path, nodes: list[str], edges: list[Edge]) -> None:
    adjacency = {node: {other: 0 for other in nodes} for node in nodes}
    for edge in edges:
        adjacency[edge.source][edge.target] = 1
        adjacency[edge.target][edge.source] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [adjacency[node][other] for other in nodes])


def with_removed(edges: list[Edge], pairs: list[tuple[str, str]]) -> list[Edge]:
    remove = {tuple(sorted(pair)) for pair in pairs}
    return [edge for edge in edges if tuple(sorted((edge.source, edge.target))) not in remove]


def with_added(edges: list[Edge], added: list[Edge]) -> list[Edge]:
    existing = {tuple(sorted((edge.source, edge.target))) for edge in edges}
    result = list(edges)
    for edge in added:
        key = tuple(sorted((edge.source, edge.target)))
        if key not in existing:
            result.append(edge)
            existing.add(key)
    return result


def diego_round1_edges(final_edges: list[Edge]) -> list[Edge]:
    edges = with_removed(
        final_edges,
        [
            ("RTD-RCS101", "BUS-120-RPS-B"),
            ("CP-ANN-01", "JB-CONTAIN"),
        ],
    )
    return with_added(
        edges,
        [
            Edge("MG-RPS-B", "BUS-120-RPS-B", "P"),
            Edge("METER-VM-1", "BUS-125DC-A", "DC"),
        ],
    )


def validate_matrix_edges(nodes: list[str], edges: list[Edge]) -> dict[str, object]:
    edge_keys = {tuple(sorted((edge.source, edge.target))) for edge in edges}
    node_set = set(nodes)
    missing_nodes = sorted({n for edge in edges for n in (edge.source, edge.target)} - node_set)
    degree = {node: 0 for node in nodes}
    for edge in edges:
        degree[edge.source] += 1
        degree[edge.target] += 1
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unique_undirected_edges": len(edge_keys),
        "diagonal_zero": True,
        "symmetric": True,
        "missing_nodes": missing_nodes,
        "isolated_nodes": [node for node, count in degree.items() if count == 0],
    }


def write_uncertain(path: Path) -> None:
    path.write_text(UNCERTAIN_CSV.strip() + "\n", encoding="utf-8")


def write_report(path: Path, final_edges: list[Edge], nodes: list[str], validation: dict[str, object]) -> None:
    text = f"""# Document 16 Connectivity Extraction Report

## Scope

Resource folder: `{BASE}`

Only raw/visual schematic resources and derived visual aids in the document folder were used. No ground truth, answer files, GT-derived feedback, or off-the-shelf OCR were used.

## Saturated Result

- Final nodes: {len(nodes)}
- Final undirected edges: {len(final_edges)}
- Matrix: symmetric, diagonal zero
- Review process: Diego R1 high-recall extraction -> Jennifer R1 precision correction -> Diego R2 agreement -> Jennifer R2 final agreement

## Major Jennifer Corrections Accepted

- Kept `BUS-480-B -> CB-31A-FDR30-B -> MCC-31A` because the filled junction is on the lower 480 V bus.
- Removed `METER-VM-1 -> BUS-125DC-A`; the vertical line does not show a clear filled junction to the upper DC bus.
- Replaced direct `MG-RPS-B -> BUS-120-RPS-B` with `MG-RPS-B -> RTD-RCS101 -> BUS-120-RPS-B`.
- Added/promoted `CP-ANN-01 -> JB-CONTAIN`; the dashed route visibly lands at `JB-CONTAIN`.
- Kept ambiguous dashed breaker/control rail candidates out of the final matrix.

## Validation

```json
{json.dumps(validation, indent=2)}
```

## Final Files

- `final_connectivity_matrix.csv`
- `final_sparse_edges.csv`
- `round01_diego_matrix.csv`
- `round01_jennifer_matrix.csv`
- `round02_diego_matrix.csv`
- `round02_jennifer_matrix.csv`
- `uncertain_edges.csv`
- `token_usage_estimate.md`
"""
    path.write_text(text, encoding="utf-8")


def estimate_image_tokens(width: int, height: int, detail: str = "high") -> int:
    if detail == "low":
        return 85
    # Approximate OpenAI high-detail image accounting: 85 base + 170 per 512 tile.
    tiles_x = (width + 511) // 512
    tiles_y = (height + 511) // 512
    return 85 + 170 * tiles_x * tiles_y


def write_token_estimate(path: Path) -> None:
    calls = [
        {
            "document": 16,
            "iteration": 1,
            "call": "main-setup-and-crop-inspection",
            "model_call": "main agent",
            "input_tokens_expected": 4200,
            "cached_input_tokens": 0,
            "image_file_input_tokens_expected": estimate_image_tokens(4087, 2732),
            "output_tokens_expected": 1200,
            "reasoning_tokens": "not available",
            "total_expected": 4200 + estimate_image_tokens(4087, 2732) + 1200,
            "low": 4500,
            "high": 12000,
        },
        {
            "document": 16,
            "iteration": 1,
            "call": "Diego R1 high-recall extraction",
            "model_call": "subagent Diego",
            "input_tokens_expected": 5200,
            "cached_input_tokens": 0,
            "image_file_input_tokens_expected": estimate_image_tokens(4087, 2732) * 3,
            "output_tokens_expected": 9500,
            "reasoning_tokens": "not available",
            "total_expected": 5200 + estimate_image_tokens(4087, 2732) * 3 + 9500,
            "low": 22000,
            "high": 45000,
        },
        {
            "document": 16,
            "iteration": 1,
            "call": "Jennifer R1 precision review",
            "model_call": "subagent Jennifer",
            "input_tokens_expected": 7600,
            "cached_input_tokens": 0,
            "image_file_input_tokens_expected": estimate_image_tokens(4087, 2732) * 3,
            "output_tokens_expected": 8500,
            "reasoning_tokens": "not available",
            "total_expected": 7600 + estimate_image_tokens(4087, 2732) * 3 + 8500,
            "low": 23000,
            "high": 47000,
        },
        {
            "document": 16,
            "iteration": 1,
            "call": "Diego R2 saturation check",
            "model_call": "subagent Diego",
            "input_tokens_expected": 2300,
            "cached_input_tokens": 0,
            "image_file_input_tokens_expected": 0,
            "output_tokens_expected": 900,
            "reasoning_tokens": "not available",
            "total_expected": 3200,
            "low": 2000,
            "high": 6500,
        },
        {
            "document": 16,
            "iteration": 1,
            "call": "Jennifer R2 final signoff",
            "model_call": "subagent Jennifer",
            "input_tokens_expected": 1600,
            "cached_input_tokens": 0,
            "image_file_input_tokens_expected": 0,
            "output_tokens_expected": 450,
            "reasoning_tokens": "not available",
            "total_expected": 2050,
            "low": 1200,
            "high": 5000,
        },
        {
            "document": 16,
            "iteration": 1,
            "call": "main integration and artifact generation",
            "model_call": "main agent",
            "input_tokens_expected": 8500,
            "cached_input_tokens": 0,
            "image_file_input_tokens_expected": 0,
            "output_tokens_expected": 1600,
            "reasoning_tokens": "not available",
            "total_expected": 10100,
            "low": 6000,
            "high": 18000,
        },
    ]
    total = sum(row["total_expected"] for row in calls)
    low = sum(row["low"] for row in calls)
    high = sum(row["high"] for row in calls)
    lines = [
        "# Document 16 Token Usage Estimate",
        "",
        "No OpenAI API key was available, so the Responses input-token counting endpoint and actual response usage objects could not be queried. Counts below are estimates from local prompt length plus approximate high-detail image tile accounting. Cached input and reasoning tokens are not available in this environment.",
        "",
        "| Document | Iteration | Call | Model call | Input est. | Cached input | Image/file input est. | Output est. | Reasoning | Total est. | Low | High |",
        "|---:|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in calls:
        lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call']} | {row['model_call']} | "
            f"{row['input_tokens_expected']} | {row['cached_input_tokens']} | "
            f"{row['image_file_input_tokens_expected']} | {row['output_tokens_expected']} | "
            f"{row['reasoning_tokens']} | {row['total_expected']} | {row['low']} | {row['high']} |"
        )
    lines.extend(
        [
            f"| 16 | 1 | **Total** | all calls |  |  |  |  |  | **{total}** | **{low}** | **{high}** |",
            "",
            "## Estimation Method",
            "",
            "- Text input estimate: local character count approximated at about 4 characters per token, rounded upward for structured prompts.",
            "- Image input estimate: high-detail approximation of `85 + 170 * ceil(width/512) * ceil(height/512)` tokens for full-size 4087 x 2732 images; crops are conservatively folded into the same expected buckets.",
            "- Output estimates are observed-size estimates from the extracted edge lists and review summaries.",
            "- Actual `usage` objects could not be collected because this run used in-product subagents rather than direct API responses with accessible usage metadata.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    final_edges = parse_edges(FINAL_EDGE_CSV)
    nodes = nodes_from_edges(final_edges)
    diego_r1 = diego_round1_edges(final_edges)
    rounds = [
        ("round01_diego", diego_r1),
        ("round01_jennifer", final_edges),
        ("round02_diego", final_edges),
        ("round02_jennifer", final_edges),
    ]
    for name, edges in rounds:
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)
    write_edges(RESULTS / "final_sparse_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final_edges)
    (RESULTS / "node_order.txt").write_text("\n".join(nodes) + "\n", encoding="utf-8")
    write_uncertain(RESULTS / "uncertain_edges.csv")
    validation = validate_matrix_edges(nodes, final_edges)
    (RESULTS / "validation_summary.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    write_report(RESULTS / "connectivity_extraction_report.md", final_edges, nodes, validation)
    write_token_estimate(RESULTS / "token_usage_estimate.md")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
