from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = RAW_DIR / "results"
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v2(1).png"
DOCUMENT = "37"
ITERATION = "1"


NODES = [
    "GRID-345",
    "CB-101",
    "CB-102",
    "AUX-TR-1A",
    "AUX-TR-1B",
    "BUS-6KA",
    "BUS-6KB",
    "CB-TIE-6K",
    "CB-103A",
    "SWGR-1EA",
    "DG-1A",
    "CB-DG1A",
    "ATS-1A",
    "RELAY-K12A",
    "TR-480A",
    "BUS-480A",
    "MCC-1A",
    "PUMP-SI-1A",
    "PUMP-RHR-1A",
    "PUMP-CCW-1A",
    "FAN-RB-1A",
    "MOV-HPCI-1A",
    "VALVE-SW-1A",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DCA",
    "GND-01A",
    "INV-120A",
    "BUS-120A",
    "PAN-RPS-A",
    "INST-RACK-A",
    "PLC-ESF",
    "CB-103B",
    "SWGR-1EB",
    "DG-1B",
    "CB-DG1B",
    "ATS-1B",
    "RELAY-K12B",
    "TR-480B",
    "BUS-480B",
    "MCC-1B",
    "PUMP-SI-1B",
    "PUMP-RHR-1B",
    "PUMP-CCW-1B",
    "FAN-RB-1B",
    "MOV-HPCI-1B",
    "VALVE-SW-1B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DCB",
    "GND-01B",
    "INV-120B",
    "BUS-120B",
    "PAN-RPS-B",
    "INST-RACK-B",
]


FINAL_EDGES = [
    ("AUX-TR-1A", "CB-101"),
    ("CB-101", "GRID-345"),
    ("GRID-345", "CB-102"),
    ("CB-102", "AUX-TR-1B"),
    ("AUX-TR-1A", "BUS-6KA"),
    ("AUX-TR-1B", "BUS-6KB"),
    ("BUS-6KA", "CB-TIE-6K"),
    ("CB-TIE-6K", "BUS-6KB"),
    ("BUS-6KA", "CB-103A"),
    ("CB-103A", "SWGR-1EA"),
    ("DG-1A", "CB-DG1A"),
    ("CB-DG1A", "SWGR-1EA"),
    ("SWGR-1EA", "ATS-1A"),
    ("ATS-1A", "RELAY-K12A"),
    ("ATS-1A", "TR-480A"),
    ("TR-480A", "BUS-480A"),
    ("BUS-480A", "MCC-1A"),
    ("MCC-1A", "PUMP-SI-1A"),
    ("MCC-1A", "PUMP-RHR-1A"),
    ("MCC-1A", "PUMP-CCW-1A"),
    ("MCC-1A", "FAN-RB-1A"),
    ("MCC-1A", "MOV-HPCI-1A"),
    ("MCC-1A", "VALVE-SW-1A"),
    ("BUS-480A", "CHGR-125A"),
    ("CHGR-125A", "BUS-125DCA"),
    ("BAT-125A", "BUS-125DCA"),
    ("BUS-125DCA", "INV-120A"),
    ("BUS-125DCA", "GND-01A"),
    ("INV-120A", "BUS-120A"),
    ("BUS-120A", "PAN-RPS-A"),
    ("BUS-120A", "INST-RACK-A"),
    ("PAN-RPS-A", "PLC-ESF"),
    ("BUS-6KB", "CB-103B"),
    ("CB-103B", "SWGR-1EB"),
    ("DG-1B", "CB-DG1B"),
    ("CB-DG1B", "SWGR-1EB"),
    ("SWGR-1EB", "ATS-1B"),
    ("ATS-1B", "RELAY-K12B"),
    ("ATS-1B", "TR-480B"),
    ("TR-480B", "BUS-480B"),
    ("BUS-480B", "MCC-1B"),
    ("MCC-1B", "PUMP-SI-1B"),
    ("MCC-1B", "PUMP-RHR-1B"),
    ("MCC-1B", "PUMP-CCW-1B"),
    ("MCC-1B", "FAN-RB-1B"),
    ("MCC-1B", "MOV-HPCI-1B"),
    ("MCC-1B", "VALVE-SW-1B"),
    ("BUS-480B", "CHGR-125B"),
    ("CHGR-125B", "BUS-125DCB"),
    ("BAT-125B", "BUS-125DCB"),
    ("BUS-125DCB", "INV-120B"),
    ("BUS-125DCB", "GND-01B"),
    ("INV-120B", "BUS-120B"),
    ("BUS-120B", "PAN-RPS-B"),
    ("BUS-120B", "INST-RACK-B"),
    ("PLC-ESF", "PAN-RPS-B"),
]


DIEGO_EXTRA_EDGES = [
    ("PAN-RPS-A", "INST-RACK-A"),
    ("INST-RACK-A", "PLC-ESF"),
    ("RELAY-K12A", "PLC-ESF"),
    ("RELAY-K12B", "PLC-ESF"),
    ("CHGR-125A", "BAT-125A"),
    ("CHGR-125B", "BAT-125B"),
    ("GRID-345", "CB-TIE-6K"),
]


ROUND_DEFINITIONS = [
    {
        "round": 1,
        "agent": "Diego",
        "label": "high_recall",
        "edges": FINAL_EDGES + DIEGO_EXTRA_EDGES,
        "comment": "High-recall proposal retained plausible but visually over-broad logical ties for reviewer pruning.",
    },
    {
        "round": 2,
        "agent": "Jennifer",
        "label": "precision_review",
        "edges": FINAL_EDGES,
        "comment": "Precision review removed unsupported extra relay, rack, charger-battery, and grid-tie shortcuts.",
    },
    {
        "round": 3,
        "agent": "Diego",
        "label": "saturation",
        "edges": FINAL_EDGES,
        "comment": "Diego accepted Jennifer's precision edge set after rechecking the raw image and raw-only crops.",
    },
    {
        "round": 4,
        "agent": "Jennifer",
        "label": "final",
        "edges": FINAL_EDGES,
        "comment": "Final precision confirmation: no additional supported edges beyond the saturated graph.",
    },
]


EDGE_EVIDENCE = {
    "AUX-TR-1A--CB-101": "Top-left offsite feeder. CB-101 is drawn inline between GRID-345 and AUX-TR-1A.",
    "CB-101--GRID-345": "GRID-345 bus ties directly into CB-101 at the left top feeder.",
    "GRID-345--CB-102": "GRID-345 bus ties directly into CB-102 at the right top feeder.",
    "CB-102--AUX-TR-1B": "Top-right offsite feeder. CB-102 is drawn inline between GRID-345 and AUX-TR-1B.",
    "AUX-TR-1A--BUS-6KA": "Transformer secondary drops to BUS-6KA.",
    "AUX-TR-1B--BUS-6KB": "Transformer secondary drops to BUS-6KB.",
    "BUS-6KA--CB-TIE-6K": "Horizontal bus tie breaker connects between the two 6 kV buses.",
    "CB-TIE-6K--BUS-6KB": "Horizontal bus tie breaker connects between the two 6 kV buses.",
    "BUS-6KA--CB-103A": "Train A feeder leaves BUS-6KA through CB-103A.",
    "CB-103A--SWGR-1EA": "CB-103A output enters SWGR-1EA.",
    "DG-1A--CB-DG1A": "Emergency diesel generator 1A feeds its breaker.",
    "CB-DG1A--SWGR-1EA": "DG breaker output connects into Train A switchgear.",
    "SWGR-1EA--ATS-1A": "Train A switchgear feeder runs to ATS-1A.",
    "ATS-1A--RELAY-K12A": "Dashed control C01 leaves ATS-1A and terminates at RELAY-K12A.",
    "ATS-1A--TR-480A": "ATS-1A output feeds transformer TR-480A.",
    "TR-480A--BUS-480A": "TR-480A secondary connects to BUS-480A.",
    "BUS-480A--MCC-1A": "480 V bus feeds Train A MCC.",
    "MCC-1A--PUMP-SI-1A": "MCC-1A branch to safety injection pump 1A.",
    "MCC-1A--PUMP-RHR-1A": "MCC-1A branch to residual heat removal pump 1A.",
    "MCC-1A--PUMP-CCW-1A": "MCC-1A branch to component cooling water pump 1A.",
    "MCC-1A--FAN-RB-1A": "MCC-1A branch to reactor building fan 1A.",
    "MCC-1A--MOV-HPCI-1A": "MCC-1A branch to HPCI motor-operated valve 1A.",
    "MCC-1A--VALVE-SW-1A": "MCC-1A branch to service water valve 1A.",
    "BUS-480A--CHGR-125A": "480 V bus supplies charger CHGR-125A.",
    "CHGR-125A--BUS-125DCA": "Charger output lands on the 125 VDC A bus.",
    "BAT-125A--BUS-125DCA": "Battery BAT-125A lands directly on the 125 VDC A bus.",
    "BUS-125DCA--INV-120A": "DC bus feeds inverter INV-120A.",
    "BUS-125DCA--GND-01A": "Labeled ground/reference tap GND-01A connects to the DC A bus.",
    "INV-120A--BUS-120A": "Inverter output feeds BUS-120A.",
    "BUS-120A--PAN-RPS-A": "AC instrumentation bus feeds RPS panel A.",
    "BUS-120A--INST-RACK-A": "AC instrumentation bus feeds instrument rack A.",
    "PAN-RPS-A--PLC-ESF": "Dashed functional cable C03 runs from PAN-RPS-A to PLC-ESF.",
    "BUS-6KB--CB-103B": "Train B feeder leaves BUS-6KB through CB-103B.",
    "CB-103B--SWGR-1EB": "CB-103B output enters SWGR-1EB.",
    "DG-1B--CB-DG1B": "Emergency diesel generator 1B feeds its breaker.",
    "CB-DG1B--SWGR-1EB": "DG breaker output connects into Train B switchgear.",
    "SWGR-1EB--ATS-1B": "Train B switchgear feeder runs to ATS-1B.",
    "ATS-1B--RELAY-K12B": "Dashed control C04 leaves ATS-1B and terminates at RELAY-K12B.",
    "ATS-1B--TR-480B": "ATS-1B output feeds transformer TR-480B.",
    "TR-480B--BUS-480B": "TR-480B secondary connects to BUS-480B.",
    "BUS-480B--MCC-1B": "480 V bus feeds Train B MCC.",
    "MCC-1B--PUMP-SI-1B": "MCC-1B branch to safety injection pump 1B.",
    "MCC-1B--PUMP-RHR-1B": "MCC-1B branch to residual heat removal pump 1B.",
    "MCC-1B--PUMP-CCW-1B": "MCC-1B branch to component cooling water pump 1B.",
    "MCC-1B--FAN-RB-1B": "MCC-1B branch to reactor building fan 1B.",
    "MCC-1B--MOV-HPCI-1B": "MCC-1B branch to HPCI motor-operated valve 1B.",
    "MCC-1B--VALVE-SW-1B": "MCC-1B branch to service water valve 1B.",
    "BUS-480B--CHGR-125B": "480 V bus supplies charger CHGR-125B.",
    "CHGR-125B--BUS-125DCB": "Charger output lands on the 125 VDC B bus.",
    "BAT-125B--BUS-125DCB": "Battery BAT-125B lands directly on the 125 VDC B bus.",
    "BUS-125DCB--INV-120B": "DC bus feeds inverter INV-120B.",
    "BUS-125DCB--GND-01B": "Labeled ground/reference tap GND-01B connects to the DC B bus.",
    "INV-120B--BUS-120B": "Inverter output feeds BUS-120B.",
    "BUS-120B--PAN-RPS-B": "AC instrumentation bus feeds RPS panel B.",
    "BUS-120B--INST-RACK-B": "AC instrumentation bus feeds instrument rack B.",
    "PLC-ESF--PAN-RPS-B": "Dashed functional cable C06 runs from PLC-ESF to PAN-RPS-B.",
}


REJECTED_EDGES = [
    ("PAN-RPS-A", "INST-RACK-A", "Both land on BUS-120A, but no direct wire between the panel and rack is visually supported."),
    ("INST-RACK-A", "PLC-ESF", "Dashed C03 is traced from PAN-RPS-A to PLC-ESF, not from INST-RACK-A."),
    ("RELAY-K12A", "PLC-ESF", "RELAY-K12A terminates C01 from ATS-1A; no continuous supported segment to PLC-ESF."),
    ("RELAY-K12B", "PLC-ESF", "C05 appears as routing/annotation near the relay area without a clear PLC-ESF termination."),
    ("CHGR-125A", "BAT-125A", "Both connect to BUS-125DCA; the charger and battery are not directly connected to each other."),
    ("CHGR-125B", "BAT-125B", "Both connect to BUS-125DCB; the charger and battery are not directly connected to each other."),
    ("GRID-345", "CB-TIE-6K", "CB-TIE-6K ties BUS-6KA and BUS-6KB only; GRID-345 reaches the buses through CB-101/CB-102 and transformers."),
]


TOKEN_ROWS = [
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "main-setup-and-resource-inspection",
        "agent": "Main",
        "purpose": "Read task, inspect raw-only resources, create crop script, coordinate workflow.",
        "model_call_count": 2,
        "input_tokens_expected": 12500,
        "input_tokens_low": 9000,
        "input_tokens_high": 17000,
        "cached_input_tokens_expected": 3500,
        "output_tokens_expected": 1300,
        "output_tokens_low": 800,
        "output_tokens_high": 2200,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Codex transcript does not expose per-response usage objects in this environment.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "diego-round-01-high-recall",
        "agent": "Diego",
        "purpose": "High-recall raw schematic extraction from raw image and raw-only crops.",
        "model_call_count": 1,
        "input_tokens_expected": 16500,
        "input_tokens_low": 12000,
        "input_tokens_high": 23000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 4200,
        "output_tokens_low": 2800,
        "output_tokens_high": 6500,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 9500,
        "actual_usage_available": "no",
        "usage_source": "Estimated from prompt, local-image payload count, crop count, and response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "jennifer-round-02-precision",
        "agent": "Jennifer",
        "purpose": "Precision review, removal of unsupported Diego edges, final label normalization.",
        "model_call_count": 1,
        "input_tokens_expected": 18000,
        "input_tokens_low": 13000,
        "input_tokens_high": 25000,
        "cached_input_tokens_expected": 0,
        "output_tokens_expected": 3800,
        "output_tokens_low": 2400,
        "output_tokens_high": 6000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 9500,
        "actual_usage_available": "no",
        "usage_source": "Estimated from Diego proposal, raw/crop image payloads, and reviewer response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "diego-round-03-saturation",
        "agent": "Diego",
        "purpose": "Recheck Jennifer corrections and accept or contest the precision matrix.",
        "model_call_count": 1,
        "input_tokens_expected": 11500,
        "input_tokens_low": 8000,
        "input_tokens_high": 16500,
        "cached_input_tokens_expected": 3000,
        "output_tokens_expected": 1800,
        "output_tokens_low": 1000,
        "output_tokens_high": 3000,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 4500,
        "actual_usage_available": "no",
        "usage_source": "Estimated from review prompt, selected crop reinspection, and short saturation response.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "jennifer-round-04-final",
        "agent": "Jennifer",
        "purpose": "Final precision confirmation after Diego saturation.",
        "model_call_count": 1,
        "input_tokens_expected": 8500,
        "input_tokens_low": 6000,
        "input_tokens_high": 12500,
        "cached_input_tokens_expected": 2500,
        "output_tokens_expected": 700,
        "output_tokens_low": 300,
        "output_tokens_high": 1200,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from compact final-confirmation payload and final response length.",
    },
    {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "call_id": "main-output-generation-and-finalization",
        "agent": "Main",
        "purpose": "Write and validate matrices, token tracking, notes, and final response.",
        "model_call_count": 2,
        "input_tokens_expected": 14500,
        "input_tokens_low": 10000,
        "input_tokens_high": 21000,
        "cached_input_tokens_expected": 5000,
        "output_tokens_expected": 5200,
        "output_tokens_low": 3500,
        "output_tokens_high": 8500,
        "reasoning_tokens_expected": "",
        "image_file_input_tokens_expected": 0,
        "actual_usage_available": "no",
        "usage_source": "Estimated from artifact-generation context and generated source/note text.",
    },
]


def edge_key(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


def display_key(edge: tuple[str, str]) -> str:
    return "--".join(edge)


def unique_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = set()
    ordered = []
    for a, b in edges:
        key = edge_key((a, b))
        if key not in seen:
            seen.add(key)
            ordered.append((a, b))
    return ordered


def matrix_for(edges: list[tuple[str, str]]) -> list[list[int]]:
    idx = {node: i for i, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for a, b in unique_edges(edges):
        if a not in idx or b not in idx:
            raise ValueError(f"Unknown edge endpoint: {a!r}, {b!r}")
        if a == b:
            raise ValueError(f"Unexpected self-loop: {a}")
        i, j = idx[a], idx[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, edges: list[tuple[str, str]]) -> None:
    matrix = matrix_for(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component", *NODES])
        for node, row in zip(NODES, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for edge in unique_edges(edges):
            writer.writerow([edge[0], edge[1], EDGE_EVIDENCE.get(display_key(edge), "")])


def write_nodes(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "component"])
        for i, node in enumerate(NODES, start=1):
            writer.writerow([i, node])


def token_totals(row: dict[str, object], tier: str) -> int:
    input_key = f"input_tokens_{tier}"
    output_key = f"output_tokens_{tier}"
    return int(row[input_key]) + int(row[output_key]) + int(row["image_file_input_tokens_expected"])


def write_token_files() -> None:
    fields = [
        "document",
        "iteration",
        "call_id",
        "agent",
        "purpose",
        "model_call_count",
        "input_tokens_expected",
        "input_tokens_low",
        "input_tokens_high",
        "cached_input_tokens_expected",
        "output_tokens_expected",
        "output_tokens_low",
        "output_tokens_high",
        "reasoning_tokens_expected",
        "image_file_input_tokens_expected",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_available",
        "usage_source",
    ]
    enriched = []
    for row in TOKEN_ROWS:
        item = dict(row)
        item["total_tokens_low"] = token_totals(row, "low")
        item["total_tokens_expected"] = token_totals(row, "expected")
        item["total_tokens_high"] = token_totals(row, "high")
        enriched.append(item)

    for filename in ("token_performance_tracking.csv", "token_performance_traking.csv", "token_usage_estimates_by_call.csv"):
        with (RESULTS_DIR / filename).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(enriched)

    summary_fields = [
        "document",
        "iteration",
        "model_call_count",
        "input_tokens_low",
        "input_tokens_expected",
        "input_tokens_high",
        "cached_input_tokens_expected",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "image_file_input_tokens_expected",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "actual_usage_available",
    ]
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "model_call_count": sum(int(r["model_call_count"]) for r in enriched),
        "input_tokens_low": sum(int(r["input_tokens_low"]) for r in enriched),
        "input_tokens_expected": sum(int(r["input_tokens_expected"]) for r in enriched),
        "input_tokens_high": sum(int(r["input_tokens_high"]) for r in enriched),
        "cached_input_tokens_expected": sum(int(r["cached_input_tokens_expected"]) for r in enriched),
        "output_tokens_low": sum(int(r["output_tokens_low"]) for r in enriched),
        "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in enriched),
        "output_tokens_high": sum(int(r["output_tokens_high"]) for r in enriched),
        "image_file_input_tokens_expected": sum(int(r["image_file_input_tokens_expected"]) for r in enriched),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in enriched),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in enriched),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in enriched),
        "actual_usage_available": "no",
    }
    with (RESULTS_DIR / "token_usage_summary_by_document.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerow(summary)

    manifest = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "responses_input_token_count_endpoint": {
            "attempted": False,
            "reason": "OPENAI_API_KEY was not available to this Codex environment; no authenticated Responses input-token counting request could be made.",
        },
        "actual_usage_collection": {
            "available": False,
            "reason": "Subagent and main-agent per-response usage objects are not exposed through the available Codex tools in this session.",
        },
        "estimate_method": "Token estimates were derived from visible prompt/response sizes, local image/crop payload count, and typical Responses image-token accounting ranges. Reasoning token counts were not available.",
        "summary_totals": summary,
    }
    (RESULTS_DIR / "responses_input_token_count_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def validate() -> dict[str, object]:
    final_edges = unique_edges(FINAL_EDGES)
    matrix = matrix_for(final_edges)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(NODES)) for j in range(len(NODES)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(NODES)))
    degree = {node: sum(row) for node, row in zip(NODES, matrix)}
    return {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "raw_image": str(RAW_IMAGE),
        "node_count": len(NODES),
        "edge_count": len(final_edges),
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "duplicate_final_edges_removed": len(FINAL_EDGES) - len(final_edges),
        "unknown_endpoint_count": 0,
        "degree_by_node": degree,
        "round_edge_counts": [
            {
                "round": r["round"],
                "agent": r["agent"],
                "label": r["label"],
                "edge_count": len(unique_edges(r["edges"])),
            }
            for r in ROUND_DEFINITIONS
        ],
    }


def write_round_files() -> None:
    with (RESULTS_DIR / "all_rounds_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["round", "agent", "label", "node_count", "edge_count", "comment"])
        for r in ROUND_DEFINITIONS:
            writer.writerow([r["round"], r["agent"], r["label"], len(NODES), len(unique_edges(r["edges"])), r["comment"]])

    for r in ROUND_DEFINITIONS:
        stem = f"round_{int(r['round']):02d}_{str(r['agent']).lower()}_{r['label']}"
        write_matrix(RESULTS_DIR / f"{stem}_matrix.csv", r["edges"])
        write_edges(RESULTS_DIR / f"{stem}_edges.csv", r["edges"])


def write_graph_json(validation: dict[str, object]) -> None:
    graph = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "nodes": [{"id": node, "index": i} for i, node in enumerate(NODES, start=1)],
        "edges": [
            {
                "source": a,
                "target": b,
                "evidence": EDGE_EVIDENCE.get(display_key((a, b)), ""),
            }
            for a, b in unique_edges(FINAL_EDGES)
        ],
        "rejected_edges": [
            {"source": a, "target": b, "reason": reason}
            for a, b, reason in REJECTED_EDGES
        ],
        "validation": validation,
    }
    (RESULTS_DIR / "connectivity_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")


def write_note(validation: dict[str, object]) -> None:
    token_total = sum(token_totals(r, "expected") for r in TOKEN_ROWS)
    token_low = sum(token_totals(r, "low") for r in TOKEN_ROWS)
    token_high = sum(token_totals(r, "high") for r in TOKEN_ROWS)
    lines = [
        "# Extraction Note - Document 37",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Scope",
        "",
        "Only the raw schematic image and raw-derived crops made from that image were used. Ground-truth and GT-derived folders were not used.",
        "",
        "## Final Connectivity",
        "",
        f"- Nodes: {validation['node_count']}",
        f"- Edges: {validation['edge_count']}",
        f"- Symmetric matrix: {validation['symmetric']}",
        f"- Diagonal zero: {validation['diagonal_zero']}",
        "",
        "## Multi-Agent Rounds",
        "",
    ]
    for r in ROUND_DEFINITIONS:
        lines.append(f"- Round {r['round']} ({r['agent']}, {r['label']}): {len(unique_edges(r['edges']))} edges. {r['comment']}")

    lines.extend([
        "",
        "## Precision Decisions",
        "",
        "Jennifer removed Diego's high-recall extras where the schematic showed a common bus, route annotation, or dashed routing path rather than a direct component-to-component termination.",
        "",
    ])
    for a, b, reason in REJECTED_EDGES:
        lines.append(f"- Rejected {a} -- {b}: {reason}")

    lines.extend([
        "",
        "## Final Edges",
        "",
    ])
    for a, b in unique_edges(FINAL_EDGES):
        evidence = EDGE_EVIDENCE.get(display_key((a, b)), "")
        lines.append(f"- {a} -- {b}: {evidence}")

    lines.extend([
        "",
        "## Token Performance Tracking",
        "",
        "Actual per-response usage objects and reasoning-token counts were not exposed through the available Codex subagent tools in this session. OPENAI_API_KEY was not available, so the Responses input-token counting endpoint could not be called for the planned payloads. The CSVs therefore contain low/expected/high estimates and mark actual usage unavailable.",
        "",
        f"- Estimated total tokens low: {token_low}",
        f"- Estimated total tokens expected: {token_total}",
        f"- Estimated total tokens high: {token_high}",
        "",
        "Detailed token rows are in token_performance_tracking.csv and token_usage_estimates_by_call.csv. The misspelled compatibility file token_performance_traking.csv is also written.",
        "",
    ])
    (RESULTS_DIR / "extraction_note.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_nodes(RESULTS_DIR / "final_nodes.csv")
    write_edges(RESULTS_DIR / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS_DIR / "connectivity_matrix.csv", FINAL_EDGES)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_EDGES)
    write_round_files()
    validation = validate()
    (RESULTS_DIR / "validation_summary.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    write_graph_json(validation)
    write_token_files()
    write_note(validation)
    print(f"Wrote outputs to {RESULTS_DIR}")
    print(f"Final nodes: {validation['node_count']}")
    print(f"Final edges: {validation['edge_count']}")
    print(f"Symmetric: {validation['symmetric']}")
    print(f"Diagonal zero: {validation['diagonal_zero']}")


if __name__ == "__main__":
    main()
