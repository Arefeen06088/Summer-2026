from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + components + junctions"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def edge(source: str, target: str, evidence: str, confidence: str) -> dict[str, str]:
    lower = f"{source} {target} {evidence}".lower()
    if "ground" in lower:
        edge_type = "ground_reference"
    elif "sensing" in lower or "relay-uv" in lower:
        edge_type = "dc_sensing"
    elif "dc" in lower or "bat-" in lower or "inv-" in lower or "chg-" in lower:
        edge_type = "dc_power"
    elif "dashed" in lower or "control" in lower or "relay-k" in lower or "jb-" in lower or "ann-" in lower or "rec-" in lower:
        edge_type = "control"
    else:
        edge_type = "power"
    return {
        "source": source,
        "target": target,
        "edge_type": edge_type,
        "confidence": confidence,
        "evidence": evidence,
    }


DIEGO_NODES = [
    "OFFSITE-230KV-A",
    "DS-230A",
    "TR-1A",
    "CB-1A",
    "EDG-1A",
    "CB-DG-A",
    "BUS-4160-A",
    "CB-TIE-AB",
    "OFFSITE-230KV-B",
    "DS-230B",
    "TR-1B",
    "CB-1B",
    "EDG-1B",
    "CB-DG-B",
    "BUS-4160-B",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A",
    "TR-480-B",
    "CB-480-B",
    "BUS-480-B",
    "GND-PLANT",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "PANEL-120A",
    "RPS-A",
    "RELAY-UV-A",
    "RELAY-KA1",
    "JB-A101",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "PANEL-120B",
    "RPS-B",
    "RELAY-UV-B",
    "RELAY-KB1",
    "JB-B101",
    "ANN-CR01",
    "REC-SOE01",
    "MCC-A1",
    "MCC-A2",
    "PUMP-RHR-A",
    "PUMP-CS-A",
    "PUMP-CCW-A",
    "MOV-881A",
    "MOV-742A",
    "MCC-B1",
    "MCC-B2",
    "PUMP-RHR-B",
    "PUMP-CS-B",
    "PUMP-CCW-B",
    "MOV-881B",
    "MOV-742B",
]


FINAL_NODES = [
    "OFFSITE-230KV-A",
    "DS-230A",
    "TR-1A",
    "CB-1A",
    "EDG-1A",
    "CB-DG-A",
    "BUS-4160-A",
    "CB-TIE-AB",
    "OFFSITE-230KV-B",
    "DS-230B",
    "TR-1B",
    "CB-1B",
    "EDG-1B",
    "CB-DG-B",
    "BUS-4160-B",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A",
    "TR-480-B",
    "CB-480-B",
    "BUS-480-B",
    "CHG-125A",
    "BAT-125A",
    "INV-120A",
    "PANEL-120A",
    "RPS-A",
    "RELAY-UV-A",
    "RELAY-KA1",
    "JB-A101",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "PANEL-120B",
    "RPS-B",
    "RELAY-UV-B",
    "RELAY-KB1",
    "JB-B101",
    "ANN-CR01",
    "REC-SOE01",
    "MCC-A1",
    "MCC-A2",
    "PUMP-RHR-A",
    "PUMP-CS-A",
    "PUMP-CCW-A",
    "MOV-881A",
    "MOV-742A",
    "MCC-B1",
    "MCC-B2",
    "PUMP-RHR-B",
    "PUMP-CS-B",
    "PUMP-CCW-B",
    "MOV-881B",
    "MOV-742B",
]


DIEGO_ROUND1_EDGES = [
    edge("OFFSITE-230KV-A", "DS-230A", "solid vertical from offsite block into DS-230A", "HIGH"),
    edge("DS-230A", "TR-1A", "solid vertical from DS-230A to transformer", "HIGH"),
    edge("TR-1A", "CB-1A", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB-1A", "BUS-4160-A", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG-1A", "CB-DG-A", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB-DG-A", "BUS-4160-A", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS-4160-A", "CB-TIE-AB", "left bus terminates at normally open tie breaker", "HIGH"),
    edge("CB-TIE-AB", "BUS-4160-B", "right side of normally open tie terminates at B bus", "HIGH"),
    edge("OFFSITE-230KV-B", "DS-230B", "solid vertical from offsite block into DS-230B", "HIGH"),
    edge("DS-230B", "TR-1B", "solid vertical from DS-230B to transformer", "HIGH"),
    edge("TR-1B", "CB-1B", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB-1B", "BUS-4160-B", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG-1B", "CB-DG-B", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB-DG-B", "BUS-4160-B", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS-4160-A", "RELAY-UV-A", "dashed/dash-dot sensing tap from A bus to relay UV-A 27/59", "HIGH"),
    edge("BUS-4160-B", "RELAY-UV-B", "dashed/dash-dot sensing tap from B bus to relay UV-B 27/59", "HIGH"),
    edge("BUS-4160-A", "TR-480-A", "solid branch from A 4.16 kV bus to TR-480-A", "HIGH"),
    edge("TR-480-A", "CB-480-A", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB-480-A", "BUS-480-A", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS-4160-B", "TR-480-B", "solid branch from B 4.16 kV bus to TR-480-B", "HIGH"),
    edge("TR-480-B", "CB-480-B", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB-480-B", "BUS-480-B", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS-480-A", "GND-PLANT", "ground/reference symbol near A 480 V bus", "PSEUDO"),
    edge("BUS-480-A", "MCC-A1", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS-480-A", "MCC-A2", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS-480-B", "MCC-B1", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS-480-B", "MCC-B2", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS-480-A", "CHG-125A", "LC-A side riser/branch visually reaches charger stack", "MED"),
    edge("CHG-125A", "BAT-125A", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT-125A", "INV-120A", "vertical DC path; terminal schedule also indicates BAT-A to INV-A", "HIGH"),
    edge("INV-120A", "PANEL-120A", "vertical stack conductor", "MED"),
    edge("PANEL-120A", "RPS-A", "vertical stack conductor", "MED"),
    edge("BUS-480-B", "CHG-125B", "LC-B side riser/branch visually reaches charger stack", "MED"),
    edge("CHG-125B", "BAT-125B", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT-125B", "INV-120B", "vertical DC path in B stack", "HIGH"),
    edge("INV-120B", "PANEL-120B", "vertical stack conductor", "MED"),
    edge("PANEL-120B", "RPS-B", "vertical stack conductor", "MED"),
    edge("MCC-A1", "PUMP-RHR-A", "solid feeder routed from MCC-A1 to RHR-A pump", "HIGH"),
    edge("MCC-A1", "PUMP-CS-A", "solid feeder routed from MCC-A1 to CS-A pump", "HIGH"),
    edge("MCC-A2", "PUMP-CCW-A", "solid feeder routed from MCC-A2 to CCW-A pump", "HIGH"),
    edge("MCC-A2", "MOV-881A", "solid feeder to MOV-881A", "HIGH"),
    edge("MCC-A2", "MOV-742A", "solid feeder to MOV-742A", "HIGH"),
    edge("MCC-B1", "PUMP-RHR-B", "solid feeder routed from MCC-B1 to RHR-B pump", "HIGH"),
    edge("MCC-B1", "PUMP-CS-B", "solid feeder routed from MCC-B1 to CS-B pump", "HIGH"),
    edge("MCC-B2", "PUMP-CCW-B", "solid feeder routed from MCC-B2 to CCW-B pump", "HIGH"),
    edge("MCC-B2", "MOV-881B", "solid feeder to MOV-881B", "HIGH"),
    edge("MCC-B2", "MOV-742B", "solid feeder to MOV-742B", "HIGH"),
    edge("RPS-A", "RELAY-KA1", "dashed branch and terminal schedule KA1 RPS-A to RLY", "HIGH"),
    edge("RPS-B", "RELAY-KB1", "dashed branch and terminal schedule KB1 RPS-B to RLY", "HIGH"),
    edge("RPS-A", "JB-A101", "dashed bottom run and terminal schedule A101 RPS-A to MOV-A", "HIGH"),
    edge("JB-A101", "MOV-881A", "dashed vertical leg from MOV-881A area to JB-A101", "MED"),
    edge("JB-A101", "MOV-742A", "dashed vertical leg from MOV-742A area to JB-A101", "MED"),
    edge("RPS-B", "JB-B101", "dashed bottom/right run and terminal schedule B101 RPS-B to MOV-B", "HIGH"),
    edge("JB-B101", "MOV-881B", "dashed vertical leg from MOV-881B area to JB-B101", "MED"),
    edge("JB-B101", "MOV-742B", "dashed vertical leg from MOV-742B area to JB-B101", "MED"),
]


FINAL_EDGES = [
    edge("OFFSITE-230KV-A", "DS-230A", "solid vertical from offsite block into DS-230A", "HIGH"),
    edge("DS-230A", "TR-1A", "solid vertical from DS-230A to transformer", "HIGH"),
    edge("TR-1A", "CB-1A", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB-1A", "BUS-4160-A", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG-1A", "CB-DG-A", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB-DG-A", "BUS-4160-A", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS-4160-A", "CB-TIE-AB", "left bus terminates at normally open tie breaker; represented through breaker node", "HIGH"),
    edge("CB-TIE-AB", "BUS-4160-B", "right side of normally open tie terminates at B bus; no direct bus splice", "HIGH"),
    edge("OFFSITE-230KV-B", "DS-230B", "solid vertical from offsite block into DS-230B", "HIGH"),
    edge("DS-230B", "TR-1B", "solid vertical from DS-230B to transformer", "HIGH"),
    edge("TR-1B", "CB-1B", "solid vertical from transformer to breaker", "HIGH"),
    edge("CB-1B", "BUS-4160-B", "solid vertical terminates at 4.16 kV bus dot", "HIGH"),
    edge("EDG-1B", "CB-DG-B", "solid emergency diesel drop to diesel breaker", "HIGH"),
    edge("CB-DG-B", "BUS-4160-B", "solid vertical into 4.16 kV bus dot", "HIGH"),
    edge("BUS-4160-A", "RELAY-UV-A", "dashed/dash-dot sensing tap from A bus to relay UV-A 27/59", "HIGH"),
    edge("BUS-4160-B", "RELAY-UV-B", "dashed/dash-dot sensing tap from B bus to relay UV-B 27/59", "HIGH"),
    edge("BUS-4160-A", "TR-480-A", "solid branch from A 4.16 kV bus to TR-480-A", "HIGH"),
    edge("TR-480-A", "CB-480-A", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB-480-A", "BUS-480-A", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS-4160-B", "TR-480-B", "solid branch from B 4.16 kV bus to TR-480-B", "HIGH"),
    edge("TR-480-B", "CB-480-B", "solid vertical through transformer to breaker", "HIGH"),
    edge("CB-480-B", "BUS-480-B", "solid vertical into 480 V load-center bus", "HIGH"),
    edge("BUS-480-A", "MCC-A1", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS-480-A", "MCC-A2", "solid vertical branch from 480 A bus", "HIGH"),
    edge("BUS-480-B", "MCC-B1", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS-480-B", "MCC-B2", "solid vertical branch from 480 B bus", "HIGH"),
    edge("BUS-480-A", "CHG-125A", "LC-A side riser/branch visually reaches charger stack", "MED"),
    edge("CHG-125A", "BAT-125A", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT-125A", "INV-120A", "vertical DC path; terminal schedule also indicates BAT-A to INV-A", "HIGH"),
    edge("INV-120A", "PANEL-120A", "vertical stack conductor", "MED"),
    edge("PANEL-120A", "RPS-A", "vertical stack conductor", "MED"),
    edge("BUS-480-B", "CHG-125B", "LC-B side riser/branch visually reaches charger stack", "MED"),
    edge("CHG-125B", "BAT-125B", "stacked vertical DC path between charger and battery", "MED"),
    edge("BAT-125B", "INV-120B", "vertical DC path in B stack", "HIGH"),
    edge("INV-120B", "PANEL-120B", "vertical stack conductor", "MED"),
    edge("PANEL-120B", "RPS-B", "vertical stack conductor", "MED"),
    edge("MCC-A1", "PUMP-RHR-A", "solid feeder routed from MCC-A1 to RHR-A pump", "HIGH"),
    edge("MCC-A1", "PUMP-CS-A", "solid feeder routed from MCC-A1 to CS-A pump", "HIGH"),
    edge("MCC-A2", "PUMP-CCW-A", "solid feeder routed from MCC-A2 to CCW-A pump", "HIGH"),
    edge("MCC-A2", "MOV-881A", "solid feeder to MOV-881A", "HIGH"),
    edge("MCC-A2", "MOV-742A", "solid feeder to MOV-742A", "HIGH"),
    edge("MCC-B1", "PUMP-RHR-B", "solid feeder routed from MCC-B1 to RHR-B pump", "HIGH"),
    edge("MCC-B1", "PUMP-CS-B", "solid feeder routed from MCC-B1 to CS-B pump", "HIGH"),
    edge("MCC-B2", "PUMP-CCW-B", "solid feeder routed from MCC-B2 to CCW-B pump", "HIGH"),
    edge("MCC-B2", "MOV-881B", "solid feeder to MOV-881B", "HIGH"),
    edge("MCC-B2", "MOV-742B", "solid feeder to MOV-742B", "HIGH"),
    edge("RPS-A", "RELAY-KA1", "dashed branch and terminal schedule KA1 RPS-A to RLY", "HIGH"),
    edge("RPS-B", "RELAY-KB1", "dashed branch and terminal schedule KB1 RPS-B to RLY", "HIGH"),
    edge("RPS-A", "JB-A101", "dashed bottom run and terminal schedule A101 RPS-A to MOV-A", "HIGH"),
    edge("JB-A101", "MOV-881A", "dashed vertical leg from MOV-881A area to JB-A101", "MED"),
    edge("JB-A101", "MOV-742A", "dashed vertical leg from MOV-742A area to JB-A101", "MED"),
    edge("RPS-B", "JB-B101", "dashed bottom/right run and terminal schedule B101 RPS-B to MOV-B", "HIGH"),
    edge("JB-B101", "MOV-881B", "dashed vertical leg from MOV-881B area to JB-B101", "MED"),
    edge("JB-B101", "MOV-742B", "dashed vertical leg from MOV-742B area to JB-B101", "MED"),
    edge("ANN-CR01", "REC-SOE01", "dashed segment visibly terminates between annunciation and SOE boxes", "HIGH"),
]


UNCERTAIN_OR_EXCLUDED = [
    {"item": "GND-PLANT", "status": "excluded", "reason": "ground/reference symbol, not an equipment endpoint"},
    {"item": "BUS-480-A-GND-PLANT", "status": "removed", "reason": "reference/ground branch excluded from connectivity matrix"},
    {"item": "BUS-4160-A-BUS-4160-B", "status": "excluded", "reason": "only connected through CB-TIE-AB; no direct bus splice"},
    {"item": "JB-A101-ANN-CR01", "status": "excluded", "reason": "no clear terminal-to-terminal conductor endpoint"},
    {"item": "REC-SOE01-JB-B101", "status": "excluded", "reason": "no clear terminal-to-terminal conductor endpoint"},
    {"item": "dashed division/control-room boundaries", "status": "excluded", "reason": "boundaries/regions, not schematic conductors"},
    {"item": "notes, title block, reference drawings, terminal schedule", "status": "excluded", "reason": "metadata; used only as visual context where adjacent wiring also supports it"},
]


ROUND_TEXT = {
    "round_02_jennifer_review.md": """# Jennifer round 2 precision review

Jennifer removed `GND-PLANT` and `BUS-480-A-GND-PLANT`, kept `CB-TIE-AB` as a breaker node with two bus-side edges, rejected direct `BUS-4160-A-BUS-4160-B`, and rejected unsupported `JB-A101-ANN-CR01` / `REC-SOE01-JB-B101`.

She added `ANN-CR01-REC-SOE01` because the dashed segment visibly terminates between those two boxes.
""",
    "round_03_diego_reconciliation.md": """# Diego round 3 reconciliation

Diego agreed with Jennifer's precision graph and did not restore `GND-PLANT`, the direct A/B bus splice, or the unsupported JB-to-annunciation edges.
""",
    "round_04_jennifer_final_saturation_check.md": """# Jennifer round 4 final saturation check

Jennifer confirmed saturation of the 53-node, 55-edge graph. Remaining exclusions are pseudo/reference items, drawing boundaries, metadata tables, and endpoints lacking visible terminal-to-terminal support.
""",
}


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "edge_type", "confidence", "evidence"])
        writer.writeheader()
        for row in edges:
            writer.writerow(row)


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "node"])
        for index, node in enumerate(nodes, start=1):
            writer.writerow([index, node])


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
    this_file = Path(__file__)
    (CODES / this_file.name).write_text(this_file.read_text(encoding="utf-8"), encoding="utf-8")
    crop_script = this_file.with_name("doc39_make_visual_crops.py")
    if crop_script.exists():
        (CODES / crop_script.name).write_text(crop_script.read_text(encoding="utf-8"), encoding="utf-8")

    round_specs = [
        ("round_01_diego", DIEGO_NODES, DIEGO_ROUND1_EDGES),
        ("round_02_jennifer", FINAL_NODES, FINAL_EDGES),
        ("round_03_diego", FINAL_NODES, FINAL_EDGES),
        ("round_04_jennifer_final", FINAL_NODES, FINAL_EDGES),
    ]
    validations = {}
    for prefix, nodes, edges in round_specs:
        write_nodes(RESULTS / f"{prefix}_nodes.csv", nodes)
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        validations[prefix] = write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edges)

    write_nodes(RESULTS / "final_nodes.csv", FINAL_NODES)
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

- `CB-TIE-AB` is retained as a breaker node; no direct `BUS-4160-A-BUS-4160-B` edge is added.
- `GND-PLANT` is excluded as a reference symbol.
- `ANN-CR01-REC-SOE01` is included as a visible dashed endpoint-to-endpoint connection.
- `JB-A101-ANN-CR01` and `REC-SOE01-JB-B101` remain excluded because endpoints are not visually supported.
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

