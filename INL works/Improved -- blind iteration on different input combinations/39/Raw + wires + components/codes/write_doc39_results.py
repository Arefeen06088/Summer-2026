from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + components")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def edge(source: str, target: str, evidence: str, confidence: str) -> dict[str, str]:
    return {"source": source, "target": target, "evidence": evidence, "confidence": confidence}


DIEGO_NODES = [
    "OFFSITE_230KV_A",
    "DS_230A",
    "TR_1A",
    "CB_1A",
    "EDG_1A",
    "CB_DG_A",
    "BUS_4160_A",
    "CB_TIE_AB",
    "OFFSITE_230KV_B",
    "DS_230B",
    "TR_1B",
    "CB_1B",
    "EDG_1B",
    "CB_DG_B",
    "BUS_4160_B",
    "TR_480_A",
    "CB_480_A",
    "BUS_480_A",
    "TR_480_B",
    "CB_480_B",
    "BUS_480_B",
    "GND_PLANT",
    "CHG_125A",
    "BAT_125A",
    "INV_120A",
    "PANEL_120A",
    "RPS_A",
    "RELAY_UV_A",
    "RELAY_KA1",
    "JB_A101",
    "CHG_125B",
    "BAT_125B",
    "INV_120B",
    "PANEL_120B",
    "RPS_B",
    "RELAY_UV_B",
    "RELAY_KB1",
    "JB_B101",
    "ANN_CR01",
    "REC_SOE01",
    "MCC_A1",
    "MCC_A2",
    "PUMP_RHR_A",
    "PUMP_CS_A",
    "PUMP_CCW_A",
    "MOV_881A",
    "MOV_742A",
    "MCC_B1",
    "MCC_B2",
    "PUMP_RHR_B",
    "PUMP_CS_B",
    "PUMP_CCW_B",
    "MOV_881B",
    "MOV_742B",
]


FINAL_NODES = [
    "OFFSITE_230KV_A",
    "DS_230A",
    "TR_1A",
    "CB_1A",
    "EDG_1A",
    "CB_DG_A",
    "BUS_4160_A",
    "CB_TIE_AB",
    "OFFSITE_230KV_B",
    "DS_230B",
    "TR_1B",
    "CB_1B",
    "EDG_1B",
    "CB_DG_B",
    "BUS_4160_B",
    "TR_480_A",
    "CB_480_A",
    "BUS_480_A",
    "TR_480_B",
    "CB_480_B",
    "BUS_480_B",
    "CHG_125A",
    "BAT_125A",
    "INV_120A",
    "PANEL_120A",
    "RPS_A",
    "RELAY_UV_A",
    "RELAY_KA1",
    "JB_A101",
    "CHG_125B",
    "BAT_125B",
    "INV_120B",
    "PANEL_120B",
    "RPS_B",
    "RELAY_UV_B",
    "RELAY_KB1",
    "JB_B101",
    "ANN_CR01",
    "REC_SOE01",
    "MCC_A1",
    "MCC_A2",
    "PUMP_RHR_A",
    "PUMP_CS_A",
    "PUMP_CCW_A",
    "MOV_881A",
    "MOV_742A",
    "MCC_B1",
    "MCC_B2",
    "PUMP_RHR_B",
    "PUMP_CS_B",
    "PUMP_CCW_B",
    "MOV_881B",
    "MOV_742B",
]


DIEGO_ROUND1_EDGES = [
    edge("OFFSITE_230KV_A", "DS_230A", "solid vertical from offsite block into DS-230A", "HIGH"),
    edge("DS_230A", "TR_1A", "solid vertical from DS-230A to transformer", "HIGH"),
    edge("TR_1A", "CB_1A", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB_1A", "BUS_4160_A", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG_1A", "CB_DG_A", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB_DG_A", "BUS_4160_A", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS_4160_A", "CB_TIE_AB", "left bus terminates at normally open tie breaker", "HIGH"),
    edge("CB_TIE_AB", "BUS_4160_B", "right side of normally open tie terminates at B bus", "HIGH"),
    edge("OFFSITE_230KV_B", "DS_230B", "solid vertical from offsite block into DS-230B", "HIGH"),
    edge("DS_230B", "TR_1B", "solid vertical from DS-230B to transformer", "HIGH"),
    edge("TR_1B", "CB_1B", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB_1B", "BUS_4160_B", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG_1B", "CB_DG_B", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB_DG_B", "BUS_4160_B", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS_4160_A", "RELAY_UV_A", "dashed/dash-dot sensing tap from A bus to relay UV-A 27/59", "HIGH"),
    edge("BUS_4160_B", "RELAY_UV_B", "dashed/dash-dot sensing tap from B bus to relay UV-B 27/59", "HIGH"),
    edge("BUS_4160_A", "TR_480_A", "solid branch from A 4.16 kV bus to TR-480-A", "HIGH"),
    edge("TR_480_A", "CB_480_A", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB_480_A", "BUS_480_A", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS_4160_B", "TR_480_B", "solid branch from B 4.16 kV bus to TR-480-B", "HIGH"),
    edge("TR_480_B", "CB_480_B", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB_480_B", "BUS_480_B", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS_480_A", "GND_PLANT", "ground/reference symbol near A 480 V bus", "PSEUDO"),
    edge("BUS_480_A", "MCC_A1", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS_480_A", "MCC_A2", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS_480_B", "MCC_B1", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS_480_B", "MCC_B2", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS_480_A", "CHG_125A", "LC-A side riser/branch visually reaches charger stack", "MED"),
    edge("CHG_125A", "BAT_125A", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT_125A", "INV_120A", "vertical DC path; terminal schedule also indicates BAT-A to INV-A", "HIGH"),
    edge("INV_120A", "PANEL_120A", "vertical stack conductor", "MED"),
    edge("PANEL_120A", "RPS_A", "vertical stack conductor", "MED"),
    edge("BUS_480_B", "CHG_125B", "LC-B side riser/branch visually reaches charger stack", "MED"),
    edge("CHG_125B", "BAT_125B", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT_125B", "INV_120B", "vertical DC path in B stack", "HIGH"),
    edge("INV_120B", "PANEL_120B", "vertical stack conductor", "MED"),
    edge("PANEL_120B", "RPS_B", "vertical stack conductor", "MED"),
    edge("MCC_A1", "PUMP_RHR_A", "solid feeder routed from MCC-A1 to RHR-A pump", "HIGH"),
    edge("MCC_A1", "PUMP_CS_A", "solid feeder routed from MCC-A1 to CS-A pump", "HIGH"),
    edge("MCC_A2", "PUMP_CCW_A", "solid feeder routed from MCC-A2 to CCW-A pump", "HIGH"),
    edge("MCC_A2", "MOV_881A", "solid feeder to MOV-881A", "HIGH"),
    edge("MCC_A2", "MOV_742A", "solid feeder to MOV-742A", "HIGH"),
    edge("MCC_B1", "PUMP_RHR_B", "solid feeder routed from MCC-B1 to RHR-B pump", "HIGH"),
    edge("MCC_B1", "PUMP_CS_B", "solid feeder routed from MCC-B1 to CS-B pump", "HIGH"),
    edge("MCC_B2", "PUMP_CCW_B", "solid feeder routed from MCC-B2 to CCW-B pump", "HIGH"),
    edge("MCC_B2", "MOV_881B", "solid feeder to MOV-881B", "HIGH"),
    edge("MCC_B2", "MOV_742B", "solid feeder to MOV-742B", "HIGH"),
    edge("RPS_A", "RELAY_KA1", "dashed branch and terminal schedule KA1 RPS-A to RLY", "HIGH"),
    edge("RPS_B", "RELAY_KB1", "dashed branch and terminal schedule KB1 RPS-B to RLY", "HIGH"),
    edge("RPS_A", "JB_A101", "dashed bottom run and terminal schedule A101 RPS-A to MOV-A", "HIGH"),
    edge("JB_A101", "MOV_881A", "dashed vertical leg from MOV-881A area to JB-A101", "MED"),
    edge("JB_A101", "MOV_742A", "dashed vertical leg from MOV-742A area to JB-A101", "MED"),
    edge("RPS_B", "JB_B101", "dashed bottom/right run and terminal schedule B101 RPS-B to MOV-B", "HIGH"),
    edge("JB_B101", "MOV_881B", "dashed vertical leg from MOV-881B area to JB-B101", "MED"),
    edge("JB_B101", "MOV_742B", "dashed vertical leg from MOV-742B area to JB-B101", "MED"),
]


FINAL_EDGES = [
    edge("OFFSITE_230KV_A", "DS_230A", "solid vertical from offsite block into DS-230A", "HIGH"),
    edge("DS_230A", "TR_1A", "solid vertical from DS-230A to transformer", "HIGH"),
    edge("TR_1A", "CB_1A", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB_1A", "BUS_4160_A", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG_1A", "CB_DG_A", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB_DG_A", "BUS_4160_A", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS_4160_A", "CB_TIE_AB", "left bus terminates at normally open tie breaker; represented through breaker node", "HIGH"),
    edge("CB_TIE_AB", "BUS_4160_B", "right side of normally open tie terminates at B bus; no direct bus splice", "HIGH"),
    edge("OFFSITE_230KV_B", "DS_230B", "solid vertical from offsite block into DS-230B", "HIGH"),
    edge("DS_230B", "TR_1B", "solid vertical from DS-230B to transformer", "HIGH"),
    edge("TR_1B", "CB_1B", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB_1B", "BUS_4160_B", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG_1B", "CB_DG_B", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB_DG_B", "BUS_4160_B", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS_4160_A", "RELAY_UV_A", "dashed/dash-dot sensing tap from A bus to relay UV-A 27/59", "HIGH"),
    edge("BUS_4160_B", "RELAY_UV_B", "dashed/dash-dot sensing tap from B bus to relay UV-B 27/59", "HIGH"),
    edge("BUS_4160_A", "TR_480_A", "solid branch from A 4.16 kV bus to TR-480-A", "HIGH"),
    edge("TR_480_A", "CB_480_A", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB_480_A", "BUS_480_A", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS_4160_B", "TR_480_B", "solid branch from B 4.16 kV bus to TR-480-B", "HIGH"),
    edge("TR_480_B", "CB_480_B", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB_480_B", "BUS_480_B", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS_480_A", "MCC_A1", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS_480_A", "MCC_A2", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS_480_B", "MCC_B1", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS_480_B", "MCC_B2", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS_480_A", "CHG_125A", "LC-A side riser/branch visually reaches charger stack", "MED"),
    edge("CHG_125A", "BAT_125A", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT_125A", "INV_120A", "vertical DC path; terminal schedule also indicates BAT-A to INV-A", "HIGH"),
    edge("INV_120A", "PANEL_120A", "vertical stack conductor", "MED"),
    edge("PANEL_120A", "RPS_A", "vertical stack conductor", "MED"),
    edge("BUS_480_B", "CHG_125B", "LC-B side riser/branch visually reaches charger stack", "MED"),
    edge("CHG_125B", "BAT_125B", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT_125B", "INV_120B", "vertical DC path in B stack", "HIGH"),
    edge("INV_120B", "PANEL_120B", "vertical stack conductor", "MED"),
    edge("PANEL_120B", "RPS_B", "vertical stack conductor", "MED"),
    edge("MCC_A1", "PUMP_RHR_A", "solid feeder routed from MCC-A1 to RHR-A pump", "HIGH"),
    edge("MCC_A1", "PUMP_CS_A", "solid feeder routed from MCC-A1 to CS-A pump", "HIGH"),
    edge("MCC_A2", "PUMP_CCW_A", "solid feeder routed from MCC-A2 to CCW-A pump", "HIGH"),
    edge("MCC_A2", "MOV_881A", "solid feeder to MOV-881A", "HIGH"),
    edge("MCC_A2", "MOV_742A", "solid feeder to MOV-742A", "HIGH"),
    edge("MCC_B1", "PUMP_RHR_B", "solid feeder routed from MCC-B1 to RHR-B pump", "HIGH"),
    edge("MCC_B1", "PUMP_CS_B", "solid feeder routed from MCC-B1 to CS-B pump", "HIGH"),
    edge("MCC_B2", "PUMP_CCW_B", "solid feeder routed from MCC-B2 to CCW-B pump", "HIGH"),
    edge("MCC_B2", "MOV_881B", "solid feeder to MOV-881B", "HIGH"),
    edge("MCC_B2", "MOV_742B", "solid feeder to MOV-742B", "HIGH"),
    edge("RPS_A", "RELAY_KA1", "dashed branch and terminal schedule KA1 RPS-A to RLY", "HIGH"),
    edge("RPS_B", "RELAY_KB1", "dashed branch and terminal schedule KB1 RPS-B to RLY", "HIGH"),
    edge("RPS_A", "JB_A101", "dashed bottom run and terminal schedule A101 RPS-A to MOV-A", "HIGH"),
    edge("JB_A101", "MOV_881A", "dashed vertical leg from MOV-881A area to JB-A101", "MED"),
    edge("JB_A101", "MOV_742A", "dashed vertical leg from MOV-742A area to JB-A101", "MED"),
    edge("RPS_B", "JB_B101", "dashed bottom/right run and terminal schedule B101 RPS-B to MOV-B", "HIGH"),
    edge("JB_B101", "MOV_881B", "dashed vertical leg from MOV-881B area to JB-B101", "MED"),
    edge("JB_B101", "MOV_742B", "dashed vertical leg from MOV-742B area to JB-B101", "MED"),
    edge("ANN_CR01", "REC_SOE01", "dashed segment visibly terminates between annunciation and SOE boxes", "HIGH"),
]


UNCERTAIN_OR_EXCLUDED = [
    {"item": "GND_PLANT", "status": "excluded", "reason": "ground/reference symbol, not an equipment endpoint"},
    {"item": "BUS_480_A-GND_PLANT", "status": "removed", "reason": "reference/ground branch excluded from connectivity matrix"},
    {"item": "BUS_4160_A-BUS_4160_B", "status": "excluded", "reason": "only connected through CB_TIE_AB; no direct bus splice"},
    {"item": "JB_A101-ANN_CR01", "status": "excluded", "reason": "no clear terminal-to-terminal conductor endpoint"},
    {"item": "REC_SOE01-JB_B101", "status": "excluded", "reason": "no clear terminal-to-terminal conductor endpoint"},
    {"item": "dashed division/control-room boundaries", "status": "excluded", "reason": "boundaries/regions, not schematic conductors"},
    {"item": "notes, title block, reference drawings, terminal schedule", "status": "excluded", "reason": "metadata; used only as visual context where adjacent wiring also supports it"},
]


ROUND_TEXT = {
    "round_02_jennifer_review.md": """# Jennifer round 2 precision review

Jennifer removed `GND_PLANT` and `BUS_480_A-GND_PLANT`, kept `CB_TIE_AB` as a breaker node with two bus-side edges, rejected direct `BUS_4160_A-BUS_4160_B`, and rejected unsupported `JB_A101-ANN_CR01` / `REC_SOE01-JB_B101`.

She added `ANN_CR01-REC_SOE01` because the dashed segment visibly terminates between those two boxes.
""",
    "round_03_diego_reconciliation.md": """# Diego round 3 reconciliation

Diego agreed with Jennifer's precision graph and did not restore `GND_PLANT`, the direct A/B bus splice, or the unsupported JB-to-annunciation edges.
""",
    "round_04_jennifer_final_saturation_check.md": """# Jennifer round 4 final saturation check

Jennifer confirmed saturation of the 53-node, 55-edge graph. Remaining exclusions are pseudo/reference items, drawing boundaries, metadata tables, and endpoints lacking visible terminal-to-terminal support.
""",
}


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "confidence", "evidence"])
        writer.writeheader()
        for row in edges:
            writer.writerow(row)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> dict[str, object]:
    index = {name: i for i, name in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    unknown: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    duplicate_count = 0
    for row in edges:
        source, target = row["source"], row["target"]
        if source not in index or target not in index:
            unknown.append((source, target))
            continue
        key = tuple(sorted((source, target)))
        if key in seen:
            duplicate_count += 1
        seen.add(key)
        if source != target:
            i, j = index[source], index[target]
            matrix[i][j] = 1
            matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "unknown_nodes": unknown,
        "duplicate_undirected_edges": duplicate_count,
        "diagonal_zero": diagonal_zero,
        "symmetric": symmetric,
        "matrix_header_nodes": len(nodes),
    }


def estimate_image_tokens(paths: list[Path]) -> int:
    total = 0
    for path in paths:
        if not path.exists():
            continue
        with Image.open(path) as img:
            w, h = img.size
        tiles = math.ceil(w / 512) * math.ceil(h / 512)
        total += 85 + 170 * tiles
    return total


def token_rows() -> list[dict[str, object]]:
    main_imgs = [
        CROPS / "raw_full_thumb.png",
        CROPS / "components_full_thumb.png",
        CROPS / "wires_overlay_full_thumb.png",
        CROPS / "focus_top_distribution_raw.png",
        CROPS / "focus_middle_distribution_raw.png",
        CROPS / "focus_lower_distribution_raw.png",
        CROPS / "focus_left_loads_raw.png",
        CROPS / "focus_right_loads_raw.png",
        CROPS / "focus_dc_controls_raw.png",
    ]
    diego_imgs = main_imgs
    jennifer_imgs = main_imgs + [CROPS / "grid_r3_c1_raw.png", CROPS / "grid_r3_c2_raw.png"]
    small_imgs = [CROPS / "raw_full_thumb.png", CROPS / "focus_lower_distribution_raw.png"]
    rows = [
        {
            "round": "main-prep-and-visual-inspection",
            "model_call": "main_agent_resource_inspection_crop_generation_visual_review",
            "input_text_tokens_est": 3600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": estimate_image_tokens(main_imgs),
            "output_tokens_low": 500,
            "output_tokens_expected": 900,
            "output_tokens_high": 1600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent inspected resources, generated crops, and visually reviewed focused regions.",
        },
        {
            "round": "round_01_diego",
            "model_call": "Diego high-recall extractor",
            "input_text_tokens_est": 2800,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": estimate_image_tokens(diego_imgs),
            "output_tokens_low": 3200,
            "output_tokens_expected": 5200,
            "output_tokens_high": 7600,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Diego reviewed full and focused crops; subagent notification exposed no usage object.",
        },
        {
            "round": "round_02_jennifer",
            "model_call": "Jennifer precision reviewer/refiner",
            "input_text_tokens_est": 7600,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": estimate_image_tokens(jennifer_imgs),
            "output_tokens_low": 1900,
            "output_tokens_expected": 3200,
            "output_tokens_high": 5000,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Jennifer reviewed Diego text plus focused/bottom crops and pruned pseudo or unsupported endpoints.",
        },
        {
            "round": "round_03_diego",
            "model_call": "Diego convergence reconciliation",
            "input_text_tokens_est": 3200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 250,
            "output_tokens_expected": 550,
            "output_tokens_high": 1000,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Diego reconciled against Jennifer's final graph and restored no edges.",
        },
        {
            "round": "round_04_jennifer_final",
            "model_call": "Jennifer final saturation check",
            "input_text_tokens_est": 1900,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 250,
            "output_tokens_expected": 500,
            "output_tokens_high": 900,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Jennifer confirmed saturation and residual exclusions.",
        },
        {
            "round": "main-final",
            "model_call": "main_agent_write_validate_report",
            "input_text_tokens_est": 3400,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 400,
            "output_tokens_expected": 800,
            "output_tokens_high": 1400,
            "reasoning_tokens": "unavailable",
            "usage_object": "unavailable",
            "notes": "Main agent wrote artifacts, validated matrices, closed agents, and reported results.",
        },
    ]
    for row in rows:
        row["document"] = "39"
        row["iteration"] = "1"
        for label in ("low", "expected", "high"):
            row[f"total_tokens_{label}"] = (
                int(row["input_text_tokens_est"])
                + int(row["cached_input_tokens_est"])
                + int(row["image_file_input_tokens_est"])
                + int(row[f"output_tokens_{label}"])
            )
    return rows


def write_token_tables() -> dict[str, object]:
    rows = token_rows()
    fields = [
        "document",
        "iteration",
        "round",
        "model_call",
        "input_text_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens",
        "usage_object",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "notes",
    ]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "document": "39",
        "iteration": "1",
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "method": "text ~= chars/4 or prompt-size estimate; images estimated with high-detail 512-tile heuristic; usage objects unavailable.",
        "counting_endpoint_used": False,
        "counting_endpoint_reason": "No API key available for the OpenAI Responses input-token counting endpoint.",
        "calls": rows,
    }
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"])
        writer.writeheader()
        writer.writerow({k: summary[k] for k in ["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"]})
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (CODES / "write_doc39_results.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")

    round_specs = [
        ("round_01_diego", DIEGO_NODES, DIEGO_ROUND1_EDGES),
        ("round_02_jennifer", FINAL_NODES, FINAL_EDGES),
        ("round_03_diego", FINAL_NODES, FINAL_EDGES),
        ("round_04_jennifer_final", FINAL_NODES, FINAL_EDGES),
    ]
    validations = {}
    for prefix, nodes, edges in round_specs:
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        validations[prefix] = write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edges)

    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    final_validation = write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)

    with (RESULTS / "uncertain_or_excluded_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item", "status", "reason"])
        writer.writeheader()
        writer.writerows(UNCERTAIN_OR_EXCLUDED)

    for name, text in ROUND_TEXT.items():
        (RESULTS / name).write_text(text, encoding="utf-8")

    report = f"""# Document 39 Extraction Report

Blind visual extraction used only the raw schematic and derived component/wire visual aids in the resource folder. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Final Result

- Nodes: {len(FINAL_NODES)}
- Edges: {len(FINAL_EDGES)}
- Symmetric matrix: {final_validation['symmetric']}
- Diagonal zero: {final_validation['diagonal_zero']}
- Unknown edge endpoints: {len(final_validation['unknown_nodes'])}
- Duplicate undirected edges: {final_validation['duplicate_undirected_edges']}

## Saturated Decisions

- `CB_TIE_AB` is retained as a breaker node; no direct `BUS_4160_A-BUS_4160_B` edge is added.
- `GND_PLANT` is excluded as a reference symbol.
- `ANN_CR01-REC_SOE01` is included as a visible dashed endpoint-to-endpoint connection.
- `JB_A101-ANN_CR01` and `REC_SOE01-JB_B101` remain excluded because endpoints are not visually supported.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")
    token_summary = write_token_tables()

    summary = {
        "document": "39",
        "iteration": "1",
        "rounds": {name: {"nodes": validations[name]["nodes"], "edges": validations[name]["edges"]} for name, _, _ in round_specs},
        "final": final_validation,
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
        "token_usage": {
            "low": token_summary["total_tokens_low"],
            "expected": token_summary["total_tokens_expected"],
            "high": token_summary["total_tokens_high"],
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
