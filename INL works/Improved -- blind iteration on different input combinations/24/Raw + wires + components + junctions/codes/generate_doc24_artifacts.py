from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Iterable

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def feeder_nodes(prefix: str, loads: dict[str, str]) -> list[str]:
    nodes: list[str] = []
    for idx, load in loads.items():
        nodes.extend(
            [
                f"CB-{prefix}{idx}",
                f"DS-{prefix}{idx}",
                f"MCC-{prefix}{idx}",
                f"TB-{prefix}{idx}",
                load,
                f"HS-{prefix}{idx}",
                f"RELAY-K{prefix}{idx}",
            ]
        )
    return nodes


A_LOADS = {
    "01": "PUMP-P201A",
    "02": "FAN-F202A",
    "03": "MOV-HV203A",
    "04": "PUMP-P204A",
    "05": "CHLR-205A",
    "06": "HTR-206A",
    "07": "VALVE-MV207A",
    "08": "PMP-LP208A",
    "09": "COMP-C209A",
}
B_LOADS = {
    "01": "PUMP-P201B",
    "02": "FAN-F202B",
    "03": "MOV-HV203B",
    "04": "PUMP-P204B",
    "05": "CHLR-205B",
    "06": "HTR-206B",
    "07": "VALVE-MV207B",
    "08": "PMP-LP208B",
    "09": "COMP-C209B",
}

NODES = [
    "OFFSITE-1",
    "CB-101A",
    "TR-SAT-1A",
    "BUS-101A",
    "EDG-1A",
    "CB-DG1A",
    "SW-MAN-A",
    "TB-DG-A",
    "CB-TIE-1",
    "SYNC-CAB",
    "LOAD-SHED-CAB",
    "OFFSITE-2",
    "CB-101B",
    "TR-SAT-1B",
    "BUS-101B",
    "EDG-1B",
    "CB-DG1B",
    "SW-MAN-B",
    "TB-DG-B",
    "CB-201A",
    "TR-1A",
    "CB-202A",
    "BUS-201A",
    "CB-201B",
    "TR-1B",
    "CB-202B",
    "BUS-201B",
    *feeder_nodes("2A", A_LOADS),
    *feeder_nodes("2B", B_LOADS),
    "DC-BUS-125A",
    "BAT-125A",
    "CHG-125A",
    "INV-120A",
    "PNL-DC-A",
    "GND-DC-A",
    "ESFAS-PNL-A",
    "PNL-AC-A",
    "PT-401A",
    "LT-402A",
    "FT-403A",
    "JB-401A",
    "GND-401A",
    "TB-RPS-A",
    "RPS-PNL-A",
    "TRIP-MOD-A",
    "RELAY-K27A",
    "RELAY-K59A",
    "RELAY-K81A",
    "RELAY-K86A",
    "METER-V1",
    "TDR-1",
    "TDR-2",
    "LAMP-ALM-A",
    "LAMP-ALM-B",
    "ANN-PNL-1",
    "SEQ-REC-1",
    "DC-BUS-125B",
    "BAT-125B",
    "CHG-125B",
    "INV-120B",
    "PNL-DC-B",
    "GND-DC-B",
    "ESFAS-PNL-B",
    "PNL-AC-B",
    "PT-401B",
    "LT-402B",
    "FT-403B",
    "JB-401B",
    "GND-401B",
    "TB-RPS-B",
    "RPS-PNL-B",
    "TRIP-MOD-B",
    "RELAY-K27B",
    "RELAY-K59B",
    "RELAY-K81B",
    "RELAY-K86B",
]


def edge(a: str, b: str, kind: str, evidence: str) -> dict[str, str]:
    if a == b:
        raise ValueError(f"self-loop not expected: {a}")
    if a not in NODES or b not in NODES:
        missing = [n for n in (a, b) if n not in NODES]
        raise ValueError(f"unknown node(s): {missing}")
    return {"source": a, "target": b, "type": kind, "evidence": evidence}


def feeder_edges(bus: str, prefix: str, loads: dict[str, str]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    for idx, load in loads.items():
        cb = f"CB-{prefix}{idx}"
        ds = f"DS-{prefix}{idx}"
        mcc = f"MCC-{prefix}{idx}"
        tb = f"TB-{prefix}{idx}"
        hs = f"HS-{prefix}{idx}"
        relay = f"RELAY-K{prefix}{idx}"
        edges.extend(
            [
                edge(bus, cb, "power", "vertical feeder tap from bus"),
                edge(cb, ds, "power", "solid feeder column"),
                edge(ds, mcc, "power", "solid feeder column"),
                edge(mcc, tb, "power", "solid feeder column"),
                edge(tb, load, "power", "solid feeder column to load"),
                edge(mcc, relay, "control", "dashed drop from MCC to relay row"),
                edge(hs, relay, "control", "dashed hand-switch to relay segment"),
            ]
        )
    idxs = list(loads)
    for left, right in zip(idxs, idxs[1:]):
        edges.append(
            edge(
                f"RELAY-K{prefix}{left}",
                f"HS-{prefix}{right}",
                "control",
                "dashed relay-row chain between adjacent feeder controls",
            )
        )
    return edges


BASE_EDGES = [
    edge("OFFSITE-1", "CB-101A", "power", "solid offsite feed"),
    edge("CB-101A", "TR-SAT-1A", "power", "solid offsite feed"),
    edge("TR-SAT-1A", "BUS-101A", "power", "solid transformer drop to bus"),
    edge("EDG-1A", "CB-DG1A", "power", "solid EDG lead"),
    edge("CB-DG1A", "BUS-101A", "power", "solid EDG breaker drop to bus"),
    edge("BUS-101A", "CB-TIE-1", "power", "solid bus tie segment"),
    edge("CB-TIE-1", "BUS-101B", "power", "solid bus tie segment"),
    edge("OFFSITE-2", "CB-101B", "power", "solid offsite feed"),
    edge("CB-101B", "TR-SAT-1B", "power", "solid offsite feed"),
    edge("TR-SAT-1B", "BUS-101B", "power", "solid transformer drop to bus"),
    edge("EDG-1B", "CB-DG1B", "power", "solid EDG lead"),
    edge("CB-DG1B", "BUS-101B", "power", "solid EDG breaker drop to bus"),
    edge("BUS-101A", "CB-201A", "power", "solid transformer feeder drop"),
    edge("CB-201A", "TR-1A", "power", "solid transformer feeder chain"),
    edge("TR-1A", "CB-202A", "power", "solid transformer feeder chain"),
    edge("CB-202A", "BUS-201A", "power", "solid drop to 4.16 kV safety bus"),
    edge("BUS-101B", "CB-201B", "power", "solid transformer feeder drop"),
    edge("CB-201B", "TR-1B", "power", "solid transformer feeder chain"),
    edge("TR-1B", "CB-202B", "power", "solid transformer feeder chain"),
    edge("CB-202B", "BUS-201B", "power", "solid drop to 4.16 kV safety bus"),
    *feeder_edges("BUS-201A", "2A", A_LOADS),
    *feeder_edges("BUS-201B", "2B", B_LOADS),
    edge("DC-BUS-125A", "BAT-125A", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125A", "CHG-125A", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125A", "INV-120A", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125A", "PNL-DC-A", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125A", "METER-V1", "signal_tap", "meter tap on A DC bus"),
    edge("INV-120A", "PNL-AC-A", "power", "solid inverter-to-AC-panel link"),
    edge("PNL-DC-A", "ESFAS-PNL-A", "dc_power", "solid panel-to-panel link"),
    edge("PNL-DC-A", "GND-DC-A", "ground", "ground reference lead"),
    edge("DC-BUS-125B", "BAT-125B", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125B", "CHG-125B", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125B", "INV-120B", "dc_power", "solid DC bus tap"),
    edge("DC-BUS-125B", "PNL-DC-B", "dc_power", "solid DC bus tap"),
    edge("INV-120B", "PNL-AC-B", "power", "solid inverter-to-AC-panel link"),
    edge("PNL-DC-B", "ESFAS-PNL-B", "dc_power", "solid panel-to-panel link"),
    edge("PNL-DC-B", "GND-DC-B", "ground", "ground reference lead"),
    edge("SW-MAN-A", "TB-DG-A", "control", "dashed DG manual-control path"),
    edge("TB-DG-A", "CB-DG1A", "control", "dashed DG manual-control path"),
    edge("SW-MAN-B", "TB-DG-B", "control", "dashed DG manual-control path"),
    edge("TB-DG-B", "CB-DG1B", "control", "dashed DG manual-control path"),
    edge("CB-TIE-1", "SYNC-CAB", "control", "dashed tie/sync path with visible landing"),
    edge("PNL-AC-A", "RPS-PNL-A", "control", "dashed panel control path"),
    edge("RPS-PNL-A", "TRIP-MOD-A", "control", "dashed RPS-to-trip-module path"),
    edge("ESFAS-PNL-A", "TRIP-MOD-A", "control", "dashed ESFAS-to-trip-module path"),
    edge("TRIP-MOD-A", "LOAD-SHED-CAB", "control", "dashed route into load-shed cabinet"),
    edge("RPS-PNL-A", "RELAY-K27A", "control", "dashed RPS drop to relay chain"),
    edge("RELAY-K27A", "RELAY-K59A", "control", "dashed relay-chain segment"),
    edge("RELAY-K59A", "RELAY-K81A", "control", "dashed relay-chain segment"),
    edge("RELAY-K81A", "RELAY-K86A", "control", "dashed relay-chain segment"),
    edge("TRIP-MOD-A", "RELAY-K86A", "control", "dashed trip-module drop to relay chain"),
    edge("PNL-AC-B", "RPS-PNL-B", "control", "dashed panel control path"),
    edge("RPS-PNL-B", "TRIP-MOD-B", "control", "dashed RPS-to-trip-module path"),
    edge("LOAD-SHED-CAB", "TRIP-MOD-B", "control", "dashed route from load-shed cabinet"),
    edge("RPS-PNL-B", "RELAY-K27B", "control", "dashed RPS drop to relay chain"),
    edge("RELAY-K27B", "RELAY-K59B", "control", "dashed relay-chain segment"),
    edge("RELAY-K59B", "RELAY-K81B", "control", "dashed relay-chain segment"),
    edge("RELAY-K81B", "RELAY-K86B", "control", "dashed relay-chain segment"),
    edge("TRIP-MOD-B", "RELAY-K86B", "control", "dashed trip-module drop to relay chain"),
    edge("LOAD-SHED-CAB", "TDR-1", "control", "dashed TDR path"),
    edge("LOAD-SHED-CAB", "TDR-2", "control", "dashed TDR path"),
    edge("PT-401A", "JB-401A", "signal", "dotted instrument signal into junction box"),
    edge("LT-402A", "JB-401A", "signal", "dotted instrument signal into junction box"),
    edge("FT-403A", "JB-401A", "signal", "dotted instrument signal into junction box"),
    edge("JB-401A", "TB-RPS-A", "signal", "dotted signal path"),
    edge("TB-RPS-A", "RPS-PNL-A", "signal", "dotted signal path"),
    edge("JB-401A", "GND-401A", "ground", "ground reference lead"),
    edge("RPS-PNL-A", "ANN-PNL-1", "signal", "dotted annunciator signal route"),
    edge("LOAD-SHED-CAB", "LAMP-ALM-A", "signal", "dotted alarm signal route"),
    edge("LOAD-SHED-CAB", "LAMP-ALM-B", "signal", "dotted alarm signal route"),
    edge("LOAD-SHED-CAB", "ANN-PNL-1", "signal", "dotted annunciator signal route"),
    edge("ANN-PNL-1", "SEQ-REC-1", "signal", "dotted annunciator-to-sequence-recorder route"),
    edge("PT-401B", "JB-401B", "signal", "dotted instrument signal into junction box"),
    edge("LT-402B", "JB-401B", "signal", "dotted instrument signal into junction box"),
    edge("FT-403B", "JB-401B", "signal", "dotted instrument signal into junction box"),
    edge("JB-401B", "TB-RPS-B", "signal", "dotted signal path"),
    edge("TB-RPS-B", "RPS-PNL-B", "signal", "dotted signal path"),
    edge("JB-401B", "GND-401B", "ground", "ground reference lead"),
]

R1_EXTRA_EDGES = [
    edge("SYNC-CAB", "LOAD-SHED-CAB", "control_uncertain", "Diego R1 high-recall central corridor inference"),
    edge("RPS-PNL-B", "RELAY-K59B", "control_uncertain", "Diego R1 high-recall B relay branch inference"),
]


def canonical_pair(e: dict[str, str]) -> tuple[str, str]:
    a, b = e["source"], e["target"]
    return tuple(sorted((a, b)))


def unique_edges(edges: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for e in edges:
        pair = canonical_pair(e)
        if pair in seen:
            raise ValueError(f"duplicate undirected edge: {pair}")
        seen.add(pair)
        out.append(e)
    return out


ROUNDS = [
    {
        "round": "round_01_diego_high_recall",
        "agent": "Diego",
        "summary": "High-recall proposal; included two later-pruned uncertain control edges.",
        "edges": unique_edges([*BASE_EDGES, *R1_EXTRA_EDGES]),
    },
    {
        "round": "round_02_jennifer_precision",
        "agent": "Jennifer",
        "summary": "Precision review removed SYNC-CAB to LOAD-SHED-CAB and RPS-PNL-B to RELAY-K59B.",
        "edges": unique_edges(BASE_EDGES),
    },
    {
        "round": "round_03_diego_saturation",
        "agent": "Diego",
        "summary": "Diego accepted Jennifer's two removals; no additions.",
        "edges": unique_edges(BASE_EDGES),
    },
    {
        "round": "round_04_jennifer_final",
        "agent": "Jennifer",
        "summary": "Jennifer confirmed final graph equals Diego R1 minus the two removed edges.",
        "edges": unique_edges(BASE_EDGES),
    },
]


def write_nodes(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(NODES):
            writer.writerow([i, node])


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def matrix_for(edges: list[dict[str, str]]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for e in edges:
        i = index[e["source"]]
        j = index[e["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def write_matrix(path: Path, matrix: list[list[int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + NODES)
        for node, row in zip(NODES, matrix):
            writer.writerow([node] + row)


def validate(edges: list[dict[str, str]]) -> dict[str, int | bool]:
    matrix = matrix_for(edges)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(NODES)) for j in range(len(NODES)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(NODES)))
    return {
        "node_count": len(NODES),
        "edge_count": len(edges),
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
    }


def approx_text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def approx_image_tokens(path: Path) -> int:
    with Image.open(path) as im:
        w, h = im.size
    scale = min(2048 / w, 2048 / h, 1.0)
    w2 = w * scale
    h2 = h * scale
    short = min(w2, h2)
    if short > 768:
        scale2 = 768 / short
        w2 *= scale2
        h2 *= scale2
    tiles = math.ceil(w2 / 512) * math.ceil(h2 / 512)
    return 85 + 170 * tiles


def token_rows() -> list[dict[str, str | int]]:
    crops = BASE / "codes" / "crops"
    diego_r1_images = [
        "raw__overview.png",
        "components__overview.png",
        "wire_nodes__overview.png",
        "raw__top_left_2x.png",
        "raw__top_center_2x.png",
        "raw__top_right_2x.png",
        "raw__mid_left_2x.png",
        "raw__mid_center_2x.png",
        "raw__mid_right_2x.png",
        "raw__bottom_left_2x.png",
        "raw__bottom_center_2x.png",
        "raw__bottom_right_2x.png",
        "wire_nodes__bottom_center_2x.png",
        "wire_nodes__bottom_right_2x.png",
    ]
    jennifer_r1_images = [
        "raw__overview.png",
        "wire_nodes__overview.png",
        "raw__top_left_2x.png",
        "raw__top_center_2x.png",
        "raw__top_right_2x.png",
        "raw__mid_left_2x.png",
        "raw__mid_center_2x.png",
        "raw__mid_right_2x.png",
        "raw__bottom_left_2x.png",
        "raw__bottom_center_2x.png",
        "raw__bottom_right_2x.png",
        "wire_nodes__bottom_center_2x.png",
        "wire_nodes__bottom_right_2x.png",
    ]
    diego_r2_images = [
        "raw__central_tie_loadshed_2x.png",
        "wire_nodes__central_tie_loadshed_2x.png",
        "components__central_tie_loadshed_2x.png",
        "raw__bottom_b_control_detail_2x.png",
    ]
    jennifer_final_images = [
        "raw__central_tie_loadshed_2x.png",
        "raw__bottom_b_control_detail_2x.png",
    ]
    main_images = [
        "raw__overview.png",
        "wire_nodes__overview.png",
        "components__overview.png",
        "raw__top_left_2x.png",
        "raw__top_center_2x.png",
        "raw__top_right_2x.png",
        "raw__mid_left_2x.png",
        "raw__mid_center_2x.png",
        "raw__mid_right_2x.png",
        "raw__bottom_left_2x.png",
        "raw__bottom_center_2x.png",
        "raw__bottom_right_2x.png",
        "wire_nodes__bottom_center_2x.png",
        "wire_nodes__bottom_right_2x.png",
        "raw__working_area.png",
        "raw__central_tie_loadshed_2x.png",
        "wire_nodes__central_tie_loadshed_2x.png",
        "raw__bottom_a_control_detail_2x.png",
        "wire_nodes__bottom_a_control_detail_2x.png",
        "raw__bottom_b_control_detail_2x.png",
    ]

    def image_sum(names: list[str]) -> int:
        return sum(approx_image_tokens(crops / name) for name in names)

    calls = [
        {
            "round": "main_visual_orchestration",
            "agent": "Main",
            "prompt": "Main agent inspected doc24 resources, viewed allowed raw/overlay crops, coordinated subagents, and generated artifacts.",
            "text_in": 3800,
            "image_in": image_sum(main_images),
            "out": 2600,
            "notes": "Aggregate estimate for main-agent visual/tool orchestration in this turn.",
        },
        {
            "round": "round_01_diego_high_recall",
            "agent": "Diego",
            "prompt": "High-recall extraction prompt with doc24-only constraint and 14 raw/overlay crops.",
            "text_in": 700,
            "image_in": image_sum(diego_r1_images),
            "out": 6400,
            "notes": "Actual usage object was not exposed by the subagent tool.",
        },
        {
            "round": "round_02_jennifer_precision",
            "agent": "Jennifer",
            "prompt": "Precision-review prompt containing Diego R1 summary and 13 raw/overlay crops.",
            "text_in": 4300,
            "image_in": image_sum(jennifer_r1_images),
            "out": 520,
            "notes": "Actual usage object was not exposed by the subagent tool.",
        },
        {
            "round": "round_03_diego_saturation",
            "agent": "Diego",
            "prompt": "Focused saturation prompt with Jennifer corrections and 4 diagnostic crops.",
            "text_in": 420,
            "image_in": image_sum(diego_r2_images),
            "out": 520,
            "notes": "Actual usage object was not exposed by the subagent tool.",
        },
        {
            "round": "round_04_jennifer_final",
            "agent": "Jennifer",
            "prompt": "Final confirmation prompt with Diego R2 acceptance and 2 diagnostic crops.",
            "text_in": 180,
            "image_in": image_sum(jennifer_final_images),
            "out": 90,
            "notes": "Actual usage object was not exposed by the subagent tool.",
        },
    ]
    rows: list[dict[str, str | int]] = []
    for call_id, call in enumerate(calls, start=1):
        prompt_tokens = approx_text_tokens(call["prompt"]) + int(call["text_in"])
        expected = prompt_tokens + int(call["image_in"]) + int(call["out"])
        rows.append(
            {
                "document": 24,
                "iteration": 1,
                "model_call_id": call_id,
                "round": call["round"],
                "agent": call["agent"],
                "input_tokens_est": prompt_tokens + int(call["image_in"]),
                "cached_input_tokens_est": 0,
                "image_file_input_tokens_est": call["image_in"],
                "output_tokens_est": call["out"],
                "reasoning_tokens_est": "unavailable",
                "low_total_tokens_est": round(expected * 0.8),
                "expected_total_tokens_est": expected,
                "high_total_tokens_est": round(expected * 1.25),
                "usage_object_available": "no",
                "notes": call["notes"],
            }
        )
    return rows


def write_token_usage() -> None:
    rows = token_rows()
    path = RESULTS / "token_usage_estimate.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def write_round_summary() -> None:
    rows = []
    for round_info in ROUNDS:
        v = validate(round_info["edges"])
        rows.append(
            {
                "document": 24,
                "iteration": 1,
                "round": round_info["round"],
                "agent": round_info["agent"],
                "node_count": v["node_count"],
                "edge_count": v["edge_count"],
                "symmetric": v["symmetric"],
                "diagonal_zero": v["diagonal_zero"],
                "summary": round_info["summary"],
            }
        )
    with (RESULTS / "round_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_notes() -> None:
    final_v = validate(BASE_EDGES)
    text = f"""# Document 24 Extraction Notes

Allowed resources only: raw schematic, detected-components overlay, wire mask/overlay, wire nodes, and local crops from the doc24 `Raw + wires + components + junctions` folder.

No ground-truth files or GT-derived feedback were used. No off-the-shelf OCR was used; labels were read visually from the schematic/crops.

## Rounds

1. Diego high recall: proposed all visually plausible nodes and edges, including two uncertain control edges.
2. Jennifer precision: removed `(RPS-PNL-B, RELAY-K59B)` and `(SYNC-CAB, LOAD-SHED-CAB)`.
3. Diego saturation: accepted both removals after focused crop review.
4. Jennifer final: confirmed the corrected graph as final.

## Final Graph

- Nodes: {final_v["node_count"]}
- Edges: {final_v["edge_count"]}
- Matrix symmetric: {final_v["symmetric"]}
- Matrix diagonal zero: {final_v["diagonal_zero"]}

`BUS-201A` represents the labeled 4.16 kV Safety Bus 101A / normal-EDG source bus. `BUS-201B` represents the matching 4.16 kV Safety Bus 101B. Ground symbols are represented as named ground-reference nodes when a drawn lead lands on them.

Token accounting is estimated locally because the OpenAI Responses token-counting endpoint and response usage objects were not available without an API key / tool exposure. The estimate combines text-token approximation with a high-detail image-tile heuristic and gives low/expected/high totals.
"""
    (RESULTS / "extraction_notes.md").write_text(text, encoding="utf-8")


def main() -> None:
    write_nodes(RESULTS / "final_nodes.csv")
    for round_info in ROUNDS:
        prefix = round_info["round"]
        edges = round_info["edges"]
        write_nodes(RESULTS / f"{prefix}_nodes.csv")
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_connectivity_matrix.csv", matrix_for(edges))
    write_edges(RESULTS / "final_edges.csv", BASE_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", matrix_for(BASE_EDGES))
    write_round_summary()
    write_token_usage()
    write_notes()
    graph = {
        "document": 24,
        "iteration": 1,
        "nodes": [{"id": node, "index": i} for i, node in enumerate(NODES)],
        "edges": BASE_EDGES,
        "validation": validate(BASE_EDGES),
    }
    (RESULTS / "final_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    print(json.dumps(validate(BASE_EDGES), indent=2))


if __name__ == "__main__":
    main()
