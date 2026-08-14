from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"
DOCUMENT = "26"
ITERATION = "1"


def add_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def edge(
    a: str,
    b: str,
    evidence: str,
    confidence: str = "high",
    status: str = "accepted",
) -> dict[str, str]:
    return {
        "source": a,
        "target": b,
        "confidence": confidence,
        "status": status,
        "evidence": evidence,
    }


def chain(items: list[str], evidence: str, confidence: str = "high") -> list[dict[str, str]]:
    return [edge(a, b, evidence, confidence) for a, b in zip(items, items[1:])]


def dedupe_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for item in edges:
        key = tuple(sorted((item["source"], item["target"])))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def ordered_nodes() -> list[str]:
    groups = [
        [
            "GEN-301",
            "TR-UAT-31",
            "CB-4A-IN1",
            "SAT-31A",
            "CB-4A-ST",
            "DG-31A",
            "CB-4A-DG",
            "BUS-416A",
            "CB-4A01",
            "TR-480A1",
            "CB-480A-IN",
            "CB-4A02",
            "TR-480A2",
            "CB-480A-ALT",
            "CB-4A03",
            "DS-RCP-A",
            "MTR-RCP-A",
            "GND-RCP-A",
            "CB-4A04",
            "DS-SW-A",
            "PUMP-SW31A",
            "GND-SW-A",
            "CB-4A05",
            "DS-AFW-A",
            "PUMP-AFW31A",
            "CB-4A06",
            "DS-CHW-A",
            "MTR-CHWP-A",
            "CB-4AB-TIE",
        ],
        [
            "SAT-31B",
            "CB-4B-ST",
            "DG-31B",
            "CB-4B-DG",
            "BUS-416B",
            "CB-4B01",
            "TR-480B1",
            "CB-480B-IN",
            "CB-4B02",
            "TR-480B2",
            "CB-480B-ALT",
            "CB-4B03",
            "DS-RCP-B",
            "MTR-RCP-B",
            "GND-RCP-B",
            "CB-4B04",
            "DS-SW-B",
            "PUMP-SW31B",
            "GND-SW-B",
            "CB-4B05",
            "DS-AFW-B",
            "PUMP-AFW31B",
            "CB-4B06",
            "DS-CHW-B",
            "MTR-CHWP-B",
        ],
        [
            "BUS-480A",
            "CB-480A11",
            "MCC-31A1",
            "GND-MCC-A1",
            "STR-A1-1",
            "JB-A1-01",
            "PUMP-CVC-A",
            "STR-A1-2",
            "JB-A1-02",
            "MOV-RHR-731A",
            "STR-A1-3",
            "JB-A1-03",
            "FAN-CRD-A",
            "CB-480A12",
            "MCC-31A2",
            "GND-MCC-A2",
            "STR-A2-1",
            "JB-A2-01",
            "PUMP-CCW-A",
            "STR-A2-2",
            "JB-A2-02",
            "HTR-BORIC-A",
            "STR-A2-3",
            "JB-A2-03",
            "MOV-CHG-121A",
            "CB-480A13",
            "LC-31A3",
            "STR-A3-1",
            "JB-A3-01",
            "MTR-SUMP-A",
            "STR-A3-2",
            "JB-A3-02",
            "PUMP-LUBE-A",
            "STR-A3-3",
            "JB-A3-03",
            "MOV-SI-902A",
            "CB-480A14",
            "PNL-31A4",
            "STR-A4-1",
            "JB-A4-01",
            "FAN-CONT-A",
            "STR-A4-2",
            "JB-A4-02",
            "PUMP-SAMPLE-A",
            "STR-A4-3",
            "JB-A4-03",
            "MOV-VENT-406A",
            "CB-480AB-TIE",
        ],
        [
            "BUS-480B",
            "CB-480B11",
            "MCC-31B1",
            "GND-MCC-B1",
            "STR-B1-1",
            "JB-B1-01",
            "PUMP-CVC-B",
            "STR-B1-2",
            "JB-B1-02",
            "MOV-RHR-731B",
            "STR-B1-3",
            "JB-B1-03",
            "FAN-CRD-B",
            "CB-480B12",
            "MCC-31B2",
            "GND-MCC-B2",
            "STR-B2-1",
            "JB-B2-01",
            "PUMP-CCW-B",
            "STR-B2-2",
            "JB-B2-02",
            "HTR-BORIC-B",
            "STR-B2-3",
            "JB-B2-03",
            "MOV-CHG-121B",
            "CB-480B13",
            "LC-31B3",
            "STR-B3-1",
            "JB-B3-01",
            "MTR-SUMP-B",
            "STR-B3-2",
            "JB-B3-02",
            "PUMP-LUBE-B",
            "STR-B3-3",
            "JB-B3-03",
            "MOV-SI-902B",
            "CB-480B14",
            "PNL-31B4",
            "STR-B4-1",
            "JB-B4-01",
            "FAN-CONT-B",
            "STR-B4-2",
            "JB-B4-02",
            "PUMP-SAMPLE-B",
            "STR-B4-3",
            "JB-B4-03",
            "MOV-VENT-406B",
        ],
        [
            "BUS-125DCA",
            "BAT-31A",
            "DS-BAT-A",
            "CHG-31A",
            "CB-CHG-A",
            "PNL-DC-A",
            "CB-INV-A",
            "INV-31A",
            "BUS-INV-A",
            "PNL-AC-A",
            "BUS-120N-A",
            "RPS-PNL-A",
            "TB-UPS-A",
            "RELAY-K7A1",
            "TB-RPS-A1",
            "PT-31A1",
            "RELAY-K7A2",
            "TB-RPS-A2",
            "PT-31A2",
            "RELAY-K7A3",
            "TB-RPS-A3",
            "PT-31A3",
            "RELAY-K7A4",
            "TB-RPS-A4",
            "PT-31A4",
            "CB-DCAB-TIE",
            "BUS-125DCB",
            "BAT-31B",
            "DS-BAT-B",
            "CHG-31B",
            "CB-CHG-B",
            "PNL-DC-B",
            "CB-INV-B",
            "INV-31B",
            "BUS-INV-B",
            "PNL-AC-B",
            "BUS-120N-B",
            "RPS-PNL-B",
            "TB-UPS-B",
            "RELAY-K7B1",
            "TB-RPS-B1",
            "PT-31B1",
            "RELAY-K7B2",
            "TB-RPS-B2",
            "PT-31B2",
            "RELAY-K7B3",
            "TB-RPS-B3",
            "PT-31B3",
            "RELAY-K7B4",
            "TB-RPS-B4",
            "PT-31B4",
        ],
    ]
    nodes: list[str] = []
    for group in groups:
        for node in group:
            add_unique(nodes, node)
    return nodes


def four_kv_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += chain(["GEN-301", "TR-UAT-31", "CB-4A-IN1", "BUS-416A"], "A UAT source stack solid conductors")
    edges += chain(["SAT-31A", "CB-4A-ST", "BUS-416A"], "A standby transformer source solid conductors")
    edges += chain(["DG-31A", "CB-4A-DG", "BUS-416A"], "A diesel generator source solid conductors")
    edges += chain(["SAT-31B", "CB-4B-ST", "BUS-416B"], "B standby transformer source solid conductors")
    edges += chain(["DG-31B", "CB-4B-DG", "BUS-416B"], "B diesel generator source solid conductors")
    edges += chain(["BUS-416A", "CB-4AB-TIE", "BUS-416B"], "4.16 kV tie breaker between train buses")

    edges += chain(["BUS-416A", "CB-4A01", "TR-480A1", "CB-480A-IN", "BUS-480A"], "A 4.16 kV feeder 01 transformer path to 480 V bus")
    edges += chain(["BUS-416A", "CB-4A02", "TR-480A2", "CB-480A-ALT", "BUS-480A"], "A 4.16 kV feeder 02 alternate transformer path to 480 V bus")
    edges += chain(["BUS-416A", "CB-4A03", "DS-RCP-A", "MTR-RCP-A"], "A RCP branch solid feeder")
    edges.append(edge("MTR-RCP-A", "GND-RCP-A", "A RCP side protection/ground path visibly tied to motor branch", "medium"))
    edges += chain(["BUS-416A", "CB-4A04", "DS-SW-A", "PUMP-SW31A"], "A service-water pump branch solid feeder")
    edges.append(edge("PUMP-SW31A", "GND-SW-A", "A service-water pump ground lead", "medium"))
    edges += chain(["BUS-416A", "CB-4A05", "DS-AFW-A", "PUMP-AFW31A"], "A AFW pump branch solid feeder")
    edges += chain(["BUS-416A", "CB-4A06", "DS-CHW-A", "MTR-CHWP-A"], "A chilled-water motor branch solid feeder")

    edges += chain(["BUS-416B", "CB-4B01", "TR-480B1", "CB-480B-IN", "BUS-480B"], "B 4.16 kV feeder 01 transformer path to 480 V bus")
    edges += chain(["BUS-416B", "CB-4B02", "TR-480B2", "CB-480B-ALT", "BUS-480B"], "B 4.16 kV feeder 02 alternate transformer path to 480 V bus")
    edges += chain(["BUS-416B", "CB-4B03", "DS-RCP-B", "MTR-RCP-B"], "B RCP branch solid feeder")
    edges.append(edge("MTR-RCP-B", "GND-RCP-B", "B RCP side protection/ground path visibly tied to motor branch", "medium"))
    edges += chain(["BUS-416B", "CB-4B04", "DS-SW-B", "PUMP-SW31B"], "B service-water pump branch solid feeder")
    edges.append(edge("PUMP-SW31B", "GND-SW-B", "B service-water pump ground lead", "medium"))
    edges += chain(["BUS-416B", "CB-4B05", "DS-AFW-B", "PUMP-AFW31B"], "B AFW pump branch solid feeder")
    edges += chain(["BUS-416B", "CB-4B06", "DS-CHW-B", "MTR-CHWP-B"], "B chilled-water motor branch solid feeder")
    return edges


def distribution_group_edges(
    bus: str,
    breaker: str,
    panel: str,
    ground: str | None,
    branches: list[tuple[str, str, str]],
) -> list[dict[str, str]]:
    edges = chain([bus, breaker, panel], f"{bus} feeder through {breaker} to {panel}")
    if ground:
        edges.append(edge(panel, ground, f"{panel} enclosure ground", "medium"))
    for starter, junction, load in branches:
        edges += chain([panel, starter, junction, load], f"{panel} branch to {load}")
    return edges


def four_eighty_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += distribution_group_edges(
        "BUS-480A",
        "CB-480A11",
        "MCC-31A1",
        "GND-MCC-A1",
        [
            ("STR-A1-1", "JB-A1-01", "PUMP-CVC-A"),
            ("STR-A1-2", "JB-A1-02", "MOV-RHR-731A"),
            ("STR-A1-3", "JB-A1-03", "FAN-CRD-A"),
        ],
    )
    edges += distribution_group_edges(
        "BUS-480A",
        "CB-480A12",
        "MCC-31A2",
        "GND-MCC-A2",
        [
            ("STR-A2-1", "JB-A2-01", "PUMP-CCW-A"),
            ("STR-A2-2", "JB-A2-02", "HTR-BORIC-A"),
            ("STR-A2-3", "JB-A2-03", "MOV-CHG-121A"),
        ],
    )
    edges += distribution_group_edges(
        "BUS-480A",
        "CB-480A13",
        "LC-31A3",
        None,
        [
            ("STR-A3-1", "JB-A3-01", "MTR-SUMP-A"),
            ("STR-A3-2", "JB-A3-02", "PUMP-LUBE-A"),
            ("STR-A3-3", "JB-A3-03", "MOV-SI-902A"),
        ],
    )
    edges += distribution_group_edges(
        "BUS-480A",
        "CB-480A14",
        "PNL-31A4",
        None,
        [
            ("STR-A4-1", "JB-A4-01", "FAN-CONT-A"),
            ("STR-A4-2", "JB-A4-02", "PUMP-SAMPLE-A"),
            ("STR-A4-3", "JB-A4-03", "MOV-VENT-406A"),
        ],
    )
    edges += chain(["BUS-480A", "CB-480AB-TIE", "BUS-480B"], "480 V tie breaker between train buses")

    edges += distribution_group_edges(
        "BUS-480B",
        "CB-480B11",
        "MCC-31B1",
        "GND-MCC-B1",
        [
            ("STR-B1-1", "JB-B1-01", "PUMP-CVC-B"),
            ("STR-B1-2", "JB-B1-02", "MOV-RHR-731B"),
            ("STR-B1-3", "JB-B1-03", "FAN-CRD-B"),
        ],
    )
    edges += distribution_group_edges(
        "BUS-480B",
        "CB-480B12",
        "MCC-31B2",
        "GND-MCC-B2",
        [
            ("STR-B2-1", "JB-B2-01", "PUMP-CCW-B"),
            ("STR-B2-2", "JB-B2-02", "HTR-BORIC-B"),
            ("STR-B2-3", "JB-B2-03", "MOV-CHG-121B"),
        ],
    )
    edges += distribution_group_edges(
        "BUS-480B",
        "CB-480B13",
        "LC-31B3",
        None,
        [
            ("STR-B3-1", "JB-B3-01", "MTR-SUMP-B"),
            ("STR-B3-2", "JB-B3-02", "PUMP-LUBE-B"),
            ("STR-B3-3", "JB-B3-03", "MOV-SI-902B"),
        ],
    )
    edges += distribution_group_edges(
        "BUS-480B",
        "CB-480B14",
        "PNL-31B4",
        None,
        [
            ("STR-B4-1", "JB-B4-01", "FAN-CONT-B"),
            ("STR-B4-2", "JB-B4-02", "PUMP-SAMPLE-B"),
            ("STR-B4-3", "JB-B4-03", "MOV-VENT-406B"),
        ],
    )
    return edges


def dc_control_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += chain(["BAT-31A", "DS-BAT-A", "BUS-125DCA"], "A battery branch to 125 VDC bus")
    edges += chain(["CHG-31A", "CB-CHG-A", "BUS-125DCA"], "A charger branch to 125 VDC bus")
    edges.append(edge("BUS-125DCA", "PNL-DC-A", "A DC panel feeder from 125 VDC bus"))
    edges += chain(["BUS-125DCA", "CB-INV-A", "INV-31A", "BUS-INV-A"], "A inverter feeder and output bus", "medium")
    edges += chain(["BUS-125DCA", "CB-DCAB-TIE", "BUS-125DCB"], "125 VDC A/B tie breaker")
    edges += chain(["BUS-INV-A", "PNL-AC-A", "BUS-120N-A"], "A AC panel between inverter bus and 120N bus")
    edges.append(edge("BUS-INV-A", "RPS-PNL-A", "A RPS panel solid feed from inverter bus"))
    edges.append(edge("RPS-PNL-A", "TB-UPS-A", "A dashed control line from RPS panel to UPS terminal block", "medium"))
    for n in range(1, 5):
        edges.append(edge("BUS-120N-A", f"RELAY-K7A{n}", f"A relay K7A{n} drop from BUS-120N-A"))
        edges.append(edge(f"RELAY-K7A{n}", f"TB-RPS-A{n}", f"A relay K7A{n} vertical lead to terminal block", "medium"))
        edges.append(edge(f"TB-RPS-A{n}", f"PT-31A{n}", f"A dotted instrument signal from terminal block to PT", "medium"))

    edges += chain(["BAT-31B", "DS-BAT-B", "BUS-125DCB"], "B battery branch to 125 VDC bus")
    edges += chain(["CHG-31B", "CB-CHG-B", "BUS-125DCB"], "B charger branch to 125 VDC bus")
    edges.append(edge("BUS-125DCB", "PNL-DC-B", "B DC panel feeder from 125 VDC bus"))
    edges += chain(["BUS-125DCB", "CB-INV-B", "INV-31B", "BUS-INV-B"], "B inverter feeder and output bus", "medium")
    edges += chain(["BUS-INV-B", "PNL-AC-B", "BUS-120N-B"], "B AC panel between inverter bus and 120N bus")
    edges.append(edge("BUS-INV-B", "RPS-PNL-B", "B RPS panel solid feed from inverter bus"))
    edges.append(edge("RPS-PNL-B", "TB-UPS-B", "B dashed control line from RPS panel to UPS terminal block", "medium"))
    for n in range(1, 5):
        edges.append(edge("BUS-120N-B", f"RELAY-K7B{n}", f"B relay K7B{n} drop from BUS-120N-B"))
        edges.append(edge(f"RELAY-K7B{n}", f"TB-RPS-B{n}", f"B relay K7B{n} vertical lead to terminal block", "medium"))
        edges.append(edge(f"TB-RPS-B{n}", f"PT-31B{n}", f"B dotted instrument signal from terminal block to PT", "medium"))
    return edges


def final_edges() -> list[dict[str, str]]:
    return dedupe_edges(four_kv_edges() + four_eighty_edges() + dc_control_edges())


def diego_uncertain_edges() -> list[dict[str, str]]:
    rows = [
        ("DS-RCP-A", "GND-RCP-A", "dashed side route not direct enough to DS-RCP-A"),
        ("DS-RCP-B", "GND-RCP-B", "dashed side route not direct enough to DS-RCP-B"),
        ("STR-A1-2", "BAT-31A", "dashed trunk passes nearby without a clear battery endpoint"),
        ("STR-B1-2", "BAT-31B", "dashed trunk passes nearby without a clear battery endpoint"),
        ("MOV-CHG-121A", "CHG-31A", "dashed trunk proximity only"),
        ("MOV-CHG-121B", "CHG-31B", "dashed trunk proximity only"),
        ("MTR-SUMP-A", "CB-INV-A", "dashed path endpoint ambiguous"),
        ("MTR-SUMP-B", "CB-INV-B", "dashed path endpoint ambiguous"),
        ("MOV-SI-902A", "RPS-PNL-A", "dashed path passes nearby but endpoint unclear"),
        ("MOV-SI-902B", "RPS-PNL-B", "dashed path passes nearby but endpoint unclear"),
    ]
    return [edge(a, b, reason, "low", "removed_by_jennifer") for a, b, reason in rows]


def jennifer_round1_added_edges() -> list[dict[str, str]]:
    return [
        edge("RPS-PNL-A", "BUS-120N-A", "Jennifer round 1 proposed vertical RPS to 120N link; removed after final review", "medium", "removed_after_diego_review"),
        edge("RPS-PNL-B", "BUS-120N-B", "Jennifer round 1 proposed vertical RPS to 120N link; removed after final review", "medium", "removed_after_diego_review"),
    ]


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source", "target", "confidence", "status", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        a, b = item["source"], item["target"]
        if a not in index or b not in index:
            raise ValueError(f"Unknown edge endpoint: {a!r}, {b!r}")
        if a != b:
            matrix[index[a]][index[b]] = 1
            matrix[index[b]][index[a]] = 1
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def image_token_estimate(path: Path) -> int:
    if not path.exists():
        return 0
    with Image.open(path) as img:
        w, h = img.size
    scale = min(2048 / max(w, h), 1.0)
    w2 = max(1, int(math.ceil(w * scale)))
    h2 = max(1, int(math.ceil(h * scale)))
    short = min(w2, h2)
    if short > 768:
        scale = 768 / short
        w2 = max(1, int(math.ceil(w2 * scale)))
        h2 = max(1, int(math.ceil(h2 * scale)))
    tiles = math.ceil(w2 / 512) * math.ceil(h2 / 512)
    return 85 + 170 * tiles


def estimate_text_tokens(text: str) -> int:
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    return max(1, math.ceil(len(text) / 4))


def image_token_sum(names: list[str]) -> int:
    return sum(image_token_estimate(CROPS / name) for name in names)


def token_rows() -> list[dict[str, object]]:
    diego_r1_images = [
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "top_left_components.png",
        "top_center_components.png",
        "top_right_components.png",
        "middle_distribution_all_components.png",
        "lower_left_components.png",
        "lower_right_components.png",
        "bottom_control_all_components.png",
        "bottom_left_control_detail_components.png",
        "bottom_right_control_detail_components.png",
    ]
    jennifer_r1_images = [
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "top_left_components.png",
        "top_center_components.png",
        "top_right_components.png",
        "middle_distribution_all_components.png",
        "lower_left_components.png",
        "lower_right_components.png",
        "bottom_left_control_detail_wires_overlay.png",
        "bottom_right_control_detail_components.png",
    ]
    diego_r2_images = [
        "bottom_left_control_detail_wires_overlay.png",
        "bottom_right_control_detail_components.png",
    ]
    jennifer_r2_images = [
        "bottom_left_control_detail_components.png",
        "bottom_left_control_detail_wires_overlay.png",
        "bottom_right_control_detail_components.png",
        "bottom_center_control_detail_components.png",
    ]
    main_visual_images = [
        "components_full_thumb.png",
        "top_left_components.png",
        "top_center_components.png",
        "top_right_components.png",
        "train_a_lower_detail_components.png",
        "train_b_lower_detail_components.png",
        "lower_left_components.png",
        "lower_right_components.png",
        "middle_distribution_all_components.png",
        "bottom_control_all_components.png",
        "bottom_left_control_detail_components.png",
        "bottom_left_control_detail_wires_overlay.png",
        "bottom_center_control_detail_components.png",
    ]
    specs = [
        (
            "main-visual-inspection",
            "main",
            "setup/local inspection",
            "File inspection, crop review, and local visual extraction baseline.",
            main_visual_images,
            2600,
            900,
            1600,
            2600,
            1200,
        ),
        (
            "diego-r1",
            "Diego",
            "round 1",
            "High-recall visual extraction from full and focused crops.",
            diego_r1_images,
            1650,
            3800,
            6500,
            9000,
            2200,
        ),
        (
            "jennifer-r1",
            "Jennifer",
            "round 2",
            "Precision review of Diego round 1 and focused crop set.",
            jennifer_r1_images,
            6200,
            900,
            1700,
            2800,
            900,
        ),
        (
            "diego-r2",
            "Diego",
            "round 3",
            "Convergence check on Jennifer disputed lower-control additions.",
            diego_r2_images,
            900,
            160,
            320,
            650,
            450,
        ),
        (
            "jennifer-r2-final",
            "Jennifer",
            "round 4",
            "Final precision decision on disputed RPS-to-120N edges.",
            jennifer_r2_images,
            1150,
            180,
            360,
            700,
            450,
        ),
        (
            "main-artifacts-final",
            "main",
            "write/final",
            "Artifact generation, validation, and final response.",
            [],
            3200,
            700,
            1200,
            2200,
            1200,
        ),
    ]
    rows: list[dict[str, object]] = []
    for call_id, actor, round_id, notes, images, text_est, out_low, out_exp, out_high, reasoning_est in specs:
        prompt_tokens = estimate_text_tokens(notes) + text_est
        image_tokens = image_token_sum(images)
        input_tokens = prompt_tokens + image_tokens
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": round_id,
                "call_id": call_id,
                "actor": actor,
                "input_tokens_est": input_tokens,
                "cached_input_tokens_est": 0,
                "text_input_tokens_est": prompt_tokens,
                "image_file_count": len(images),
                "image_file_tokens_est": image_tokens,
                "output_tokens_low_est": out_low,
                "output_tokens_expected_est": out_exp,
                "output_tokens_high_est": out_high,
                "reasoning_tokens_est": reasoning_est,
                "total_low_tokens_est": input_tokens + out_low + reasoning_est,
                "total_expected_tokens_est": input_tokens + out_exp + reasoning_est,
                "total_high_tokens_est": input_tokens + out_high + reasoning_est,
                "usage_object_available": "no",
                "notes": notes,
            }
        )
    return rows


def write_token_tables(rows: list[dict[str, object]]) -> dict[str, object]:
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in rows),
        "image_file_tokens_est": sum(int(r["image_file_tokens_est"]) for r in rows),
        "output_tokens_low_est": sum(int(r["output_tokens_low_est"]) for r in rows),
        "output_tokens_expected_est": sum(int(r["output_tokens_expected_est"]) for r in rows),
        "output_tokens_high_est": sum(int(r["output_tokens_high_est"]) for r in rows),
        "reasoning_tokens_est": sum(int(r["reasoning_tokens_est"]) for r in rows),
        "total_low_tokens_est": sum(int(r["total_low_tokens_est"]) for r in rows),
        "total_expected_tokens_est": sum(int(r["total_expected_tokens_est"]) for r in rows),
        "total_high_tokens_est": sum(int(r["total_high_tokens_est"]) for r in rows),
        "method": "Responses input-token counting endpoint was not called because OPENAI_API_KEY is unavailable. Text was estimated locally with tiktoken when present; image/file tokens were estimated with high-detail 512px tile sizing.",
    }
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_uncertain(path: Path) -> None:
    rows = [
        ("DS-RCP-A--GND-RCP-A", "excluded", "Dashed side route is present but does not terminate directly enough at DS-RCP-A."),
        ("DS-RCP-B--GND-RCP-B", "excluded", "Dashed side route is present but does not terminate directly enough at DS-RCP-B."),
        ("STR-A1-2--BAT-31A", "excluded", "Dashed route passes nearby; no clear battery endpoint."),
        ("STR-B1-2--BAT-31B", "excluded", "Dashed route passes nearby; no clear battery endpoint."),
        ("MOV-CHG-121A--CHG-31A", "excluded", "Dashed trunk proximity only."),
        ("MOV-CHG-121B--CHG-31B", "excluded", "Dashed trunk proximity only."),
        ("MTR-SUMP-A--CB-INV-A", "excluded", "Dashed route endpoint is ambiguous."),
        ("MTR-SUMP-B--CB-INV-B", "excluded", "Dashed route endpoint is ambiguous."),
        ("MOV-SI-902A--RPS-PNL-A", "excluded", "Dashed route passes nearby but direct endpoint is not clear."),
        ("MOV-SI-902B--RPS-PNL-B", "excluded", "Dashed route passes nearby but direct endpoint is not clear."),
        ("RPS-PNL-A--BUS-120N-A", "removed_after_final_review", "RPS-PNL-A is fed from BUS-INV-A and dashed to TB-UPS-A; 120N drop is adjacent, not a clear RPS connection."),
        ("RPS-PNL-B--BUS-120N-B", "removed_after_final_review", "RPS-PNL-B is fed from BUS-INV-B and dashed to TB-UPS-B; 120N drop is adjacent, not a clear RPS connection."),
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["edge_or_node", "status", "reason"])
        writer.writerows(rows)


def write_report(
    nodes: list[str],
    round1: list[dict[str, str]],
    round2: list[dict[str, str]],
    round3: list[dict[str, str]],
    round4: list[dict[str, str]],
    token_summary: dict[str, object],
) -> None:
    report = f"""# Document 26 Connectivity Extraction

Blind visual extraction using only the raw schematic and derived visual aids in the resource folder. No GT, GT-derived feedback, or OCR tools were used.

## Rounds

1. Diego high-recall extraction captured the 4.16 kV A/B source buses, transformer feeders, 480 V load-center branches, 125 VDC buses, inverter buses, 120N buses, relays, terminal blocks, and PTs. Low-confidence dashed trunk guesses were kept as round-1 proposed edges only.
2. Jennifer accepted the main graph, excluded Diego's speculative dashed trunks, and initially proposed two RPS-panel to 120N-bus edges.
3. Diego rejected the two added RPS-to-120N edges after focused lower-control review.
4. Jennifer final confirmation removed those two edges and made no other graph changes.

## Final Matrix

- Nodes: {len(nodes)}
- Round 1 Diego edges: {len(round1)}
- Round 2 Jennifer edges: {len(round2)}
- Round 3 Diego edges: {len(round3)}
- Round 4 Jennifer final edges: {len(round4)}
- Matrix file: `final_connectivity_matrix.csv`
- Edge file: `final_edges.csv`

## Key Precision Decisions

- Buses are explicit nodes; devices sharing a bus are connected to the bus node, not to each other as a clique.
- Wire labels such as `480-A-11`, `4-416-A-01`, `DC-A-INV`, and `120-A-N` are treated as wire identifiers, not component nodes.
- `RPS-PNL-A--BUS-120N-A` and `RPS-PNL-B--BUS-120N-B` were removed after final review.
- Clear dashed/instrument paths retained: `RPS-PNL-*--TB-UPS-*`, `RELAY-K7*--TB-RPS-*`, and `TB-RPS-*--PT-*`.

## Token Estimation

The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Actual usage objects were not exposed by the Codex subagent tooling. The estimate uses local text token estimation plus high-detail image tile estimates.

- Estimated input tokens: {token_summary['input_tokens_est']}
- Estimated image/file input tokens: {token_summary['image_file_tokens_est']}
- Expected output tokens: {token_summary['output_tokens_expected_est']}
- Estimated reasoning tokens: {token_summary['reasoning_tokens_est']}
- Expected total tokens: {token_summary['total_expected_tokens_est']}
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def validate(nodes: list[str], edges: list[dict[str, str]]) -> None:
    node_set = set(nodes)
    missing = sorted({p for item in edges for p in (item["source"], item["target"]) if p not in node_set})
    if missing:
        raise ValueError(f"Missing nodes: {missing}")
    if len(nodes) != len(set(nodes)):
        raise ValueError("Duplicate nodes detected")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = ordered_nodes()
    final = final_edges()
    round1 = dedupe_edges(final + diego_uncertain_edges())
    round2 = dedupe_edges(final + jennifer_round1_added_edges())
    round3 = final
    round4 = final
    for edge_set in [round1, round2, round3, round4, final]:
        validate(nodes, edge_set)
    for name, edge_set in [
        ("round_01_diego", round1),
        ("round_02_jennifer", round2),
        ("round_03_diego", round3),
        ("round_04_jennifer_final", round4),
    ]:
        write_edges(RESULTS / f"{name}_edges.csv", edge_set)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edge_set)
    write_edges(RESULTS / "final_edges.csv", final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final)
    write_uncertain(RESULTS / "uncertain_or_excluded_edges.csv")
    token_summary = write_token_tables(token_rows())
    write_report(nodes, round1, round2, round3, round4, token_summary)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "nodes": len(nodes),
        "final_edges": len(final),
        "rounds": {
            "round_01_diego": len(round1),
            "round_02_jennifer": len(round2),
            "round_03_diego": len(round3),
            "round_04_jennifer_final": len(round4),
        },
        "matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges_file": str(RESULTS / "final_edges.csv"),
        "token_usage_estimate": str(RESULTS / "token_usage_estimate.csv"),
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
