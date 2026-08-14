from __future__ import annotations

import csv
import json
import math
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

DOC_ID = "23"
ITERATION = 1
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires"
)
CODES_DIR = ROOT / "codes"
RESULTS_DIR = ROOT / "results"
CROPS_DIR = CODES_DIR / "crops"


TOP_NODES = [
    "GRID-161A",
    "DS-101",
    "CB-101",
    "TR-UAT-1A",
    "CB-102",
    "BUS-4160-A",
    "CB-TIE-41",
    "SYNC-41",
    "BUS-4160-B",
    "CB-104",
    "TR-UAT-1B",
    "CB-103",
    "DS-102",
    "GRID-161B",
    "CB-ESF-A",
    "BUS-4160-ESF-A",
    "DG-1A",
    "CB-DG1A",
    "ATS-1A",
    "CB-ESF-B",
    "BUS-4160-ESF-B",
    "DG-1B",
    "CB-DG1B",
    "ATS-1B",
    "RELAY-87A",
    "RELAY-27A",
    "METER-A",
    "PT-41A",
    "GND-41A",
    "RELAY-87B",
    "RELAY-27B",
    "METER-B",
    "PT-41B",
    "GND-41B",
]


LOAD_CENTERS = [
    {
        "id": "1A",
        "source": "BUS-4160-A",
        "pump": "PUMP-P101",
        "motor": "MOTOR-M102",
        "mov": "VALVE-MOV103",
        "fan": "FAN-F104",
        "heater": "HTR-H105",
        "xv": "VALVE-XV106",
        "relays": ("RELAY-K11", "RELAY-K12"),
    },
    {
        "id": "1C",
        "source": "BUS-4160-A",
        "pump": "PUMP-P131",
        "motor": "MOTOR-M132",
        "mov": "VALVE-MOV133",
        "fan": "FAN-F134",
        "heater": "HTR-H135",
        "xv": "VALVE-XV136",
        "relays": ("RELAY-K21", "RELAY-K22"),
    },
    {
        "id": "1B",
        "source": "BUS-4160-B",
        "pump": "PUMP-P161",
        "motor": "MOTOR-M162",
        "mov": "VALVE-MOV163",
        "fan": "FAN-F164",
        "heater": "HTR-H165",
        "xv": "VALVE-XV166",
        "relays": ("RELAY-K31", "RELAY-K32"),
    },
    {
        "id": "2A",
        "source": "BUS-4160-ESF-A",
        "pump": "PUMP-P201",
        "motor": "MOTOR-M202",
        "mov": "VALVE-MOV203",
        "fan": "FAN-F204",
        "heater": "HTR-H205",
        "xv": "VALVE-XV206",
        "relays": ("RELAY-K41", "RELAY-K42"),
    },
    {
        "id": "2C",
        "source": "BUS-4160-ESF-A",
        "pump": "PUMP-P231",
        "motor": "MOTOR-M232",
        "mov": "VALVE-MOV233",
        "fan": "FAN-F234",
        "heater": "HTR-H235",
        "xv": "VALVE-XV236",
        "relays": ("RELAY-K51", "RELAY-K52"),
    },
    {
        "id": "2B",
        "source": "BUS-4160-ESF-B",
        "pump": "PUMP-P261",
        "motor": "MOTOR-M262",
        "mov": "VALVE-MOV263",
        "fan": "FAN-F264",
        "heater": "HTR-H265",
        "xv": "VALVE-XV266",
        "relays": ("RELAY-K61", "RELAY-K62"),
    },
]


DC_NODES = [
    "CB-DC-A",
    "RECT-125A",
    "BUS-125DC-A",
    "BAT-125A",
    "CHGR-AUX-A",
    "METER-DC-A",
    "INV-1A",
    "UPS-1A",
    "CB-UPS-A",
    "BUS-120AC-A",
    "FUSE-FU-A",
    "RELAY-KA1",
    "RELAY-KA2",
    "ANN-A",
    "REC-SER-A",
    "PNL-RPS-A",
    "INST-NIS-A",
    "PNL-DCS-A",
    "JB-CTRL/A",
    "GND-DC-A",
    "CB-DC-B",
    "RECT-125B",
    "BUS-125DC-B",
    "BAT-125B",
    "CHGR-AUX-B",
    "METER-DC-B",
    "INV-1B",
    "UPS-1B",
    "CB-UPS-B",
    "BUS-120AC-B",
    "FUSE-FU-B",
    "RELAY-KB1",
    "RELAY-KB2",
    "ANN-B",
    "REC-SER-B",
    "PNL-RPS-B",
    "INST-NIS-B",
    "PNL-DCS-B",
    "JB-CTRL-B",
    "GND-DC-B",
    "CB-DCTIE",
    "DC-DC-1",
    "BUS-24DC-C",
    "BAT-24C",
    "PNL-RADMON",
    "RELAY-KTIE",
]


def load_center_nodes(lc: dict) -> list[str]:
    x = lc["id"]
    r1, r2 = lc["relays"]
    return [
        f"CB-{x}-FDR",
        f"DS-{x}-ISO",
        f"TR-{x}",
        f"CB-{x}-MAIN",
        f"BUS-480-{x}",
        f"MCC-{x}-1",
        lc["pump"],
        lc["motor"],
        f"MCC-{x}-2",
        lc["mov"],
        lc["fan"],
        f"MCC-{x}-3",
        lc["heater"],
        lc["xv"],
        f"PNL-{x}",
        f"JB-{x}-1",
        r1,
        r2,
        f"INST-{x}",
        f"GND-{x}",
    ]


NODES: list[str] = [*TOP_NODES]
for item in LOAD_CENTERS:
    NODES.extend(load_center_nodes(item))
NODES.extend(DC_NODES)


def e(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-edge not expected: {a}")
    return a, b


FINAL_EDGES: list[tuple[str, str]] = [
    e("GRID-161A", "DS-101"),
    e("DS-101", "CB-101"),
    e("CB-101", "TR-UAT-1A"),
    e("TR-UAT-1A", "CB-102"),
    e("CB-102", "BUS-4160-A"),
    e("GRID-161B", "DS-102"),
    e("DS-102", "CB-103"),
    e("CB-103", "TR-UAT-1B"),
    e("TR-UAT-1B", "CB-104"),
    e("CB-104", "BUS-4160-B"),
    e("BUS-4160-A", "CB-TIE-41"),
    e("CB-TIE-41", "BUS-4160-B"),
    e("BUS-4160-A", "CB-ESF-A"),
    e("CB-ESF-A", "BUS-4160-ESF-A"),
    e("BUS-4160-B", "CB-ESF-B"),
    e("CB-ESF-B", "BUS-4160-ESF-B"),
    e("DG-1A", "CB-DG1A"),
    e("CB-DG1A", "ATS-1A"),
    e("ATS-1A", "BUS-4160-ESF-A"),
    e("DG-1B", "CB-DG1B"),
    e("CB-DG1B", "ATS-1B"),
    e("ATS-1B", "BUS-4160-ESF-B"),
    e("BUS-4160-A", "GND-41A"),
    e("BUS-4160-B", "GND-41B"),
]


def add_load_center_edges(edges: list[tuple[str, str]], lc: dict) -> None:
    x = lc["id"]
    edges.extend(
        [
            e(lc["source"], f"CB-{x}-FDR"),
            e(f"CB-{x}-FDR", f"DS-{x}-ISO"),
            e(f"DS-{x}-ISO", f"TR-{x}"),
            e(f"TR-{x}", f"CB-{x}-MAIN"),
            e(f"CB-{x}-MAIN", f"BUS-480-{x}"),
            e(f"BUS-480-{x}", f"MCC-{x}-1"),
            e(f"MCC-{x}-1", lc["pump"]),
            e(f"MCC-{x}-1", lc["motor"]),
            e(f"BUS-480-{x}", f"MCC-{x}-2"),
            e(f"MCC-{x}-2", lc["mov"]),
            e(f"MCC-{x}-2", lc["fan"]),
            e(f"BUS-480-{x}", f"MCC-{x}-3"),
            e(f"MCC-{x}-3", lc["heater"]),
            e(f"MCC-{x}-3", lc["xv"]),
            e(f"BUS-480-{x}", f"PNL-{x}"),
            e(f"BUS-480-{x}", f"GND-{x}"),
            e(lc["xv"], f"JB-{x}-1"),
        ]
    )


for load_center in LOAD_CENTERS:
    add_load_center_edges(FINAL_EDGES, load_center)

FINAL_EDGES.extend(
    [
        e("BUS-480-2A", "CB-DC-A"),
        e("CB-DC-A", "RECT-125A"),
        e("RECT-125A", "BUS-125DC-A"),
        e("BUS-480-2B", "CB-DC-B"),
        e("CB-DC-B", "RECT-125B"),
        e("RECT-125B", "BUS-125DC-B"),
        e("BUS-125DC-A", "CB-DCTIE"),
        e("CB-DCTIE", "BUS-125DC-B"),
        e("BUS-125DC-A", "BAT-125A"),
        e("BUS-125DC-A", "CHGR-AUX-A"),
        e("BUS-125DC-A", "GND-DC-A"),
        e("BUS-125DC-A", "INV-1A"),
        e("INV-1A", "UPS-1A"),
        e("UPS-1A", "CB-UPS-A"),
        e("CB-UPS-A", "BUS-120AC-A"),
        e("BUS-125DC-B", "BAT-125B"),
        e("BUS-125DC-B", "CHGR-AUX-B"),
        e("BUS-125DC-B", "GND-DC-B"),
        e("BUS-125DC-B", "INV-1B"),
        e("INV-1B", "UPS-1B"),
        e("UPS-1B", "CB-UPS-B"),
        e("CB-UPS-B", "BUS-120AC-B"),
        e("BUS-120AC-A", "FUSE-FU-A"),
        e("BUS-120AC-A", "PNL-RPS-A"),
        e("BUS-120AC-B", "FUSE-FU-B"),
        e("BUS-120AC-B", "PNL-RPS-B"),
        e("BUS-125DC-A", "DC-DC-1"),
        e("DC-DC-1", "BUS-24DC-C"),
        e("BUS-24DC-C", "BAT-24C"),
        e("BUS-24DC-C", "PNL-RADMON"),
    ]
)


DIEGO_R2_ADDITIONS = [
    e("BUS-4160-A", "GND-41A"),
    e("BUS-4160-B", "GND-41B"),
    e("BUS-125DC-A", "BAT-125A"),
    e("BUS-125DC-A", "CHGR-AUX-A"),
    e("BUS-125DC-A", "GND-DC-A"),
    e("BUS-125DC-B", "BAT-125B"),
    e("BUS-125DC-B", "CHGR-AUX-B"),
    e("BUS-125DC-B", "GND-DC-B"),
    e("BUS-120AC-A", "FUSE-FU-A"),
    e("BUS-120AC-A", "PNL-RPS-A"),
    e("BUS-120AC-B", "FUSE-FU-B"),
    e("BUS-120AC-B", "PNL-RPS-B"),
]


def canonical_edge(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


def without_edges(edges: Iterable[tuple[str, str]], remove: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    remove_set = {canonical_edge(edge) for edge in remove}
    return [edge for edge in edges if canonical_edge(edge) not in remove_set]


def diego_round1_edges() -> list[tuple[str, str]]:
    edges = without_edges(FINAL_EDGES, [e("BUS-4160-A", "CB-1C-FDR")])
    edges.append(e("BUS-4160-ESF-A", "CB-1C-FDR"))
    edges.extend(
        [
            e("CB-TIE-41", "SYNC-41"),
            e("BUS-4160-A", "RELAY-87A"),
            e("BUS-4160-A", "RELAY-27A"),
            e("BUS-4160-A", "METER-A"),
            e("BUS-4160-A", "PT-41A"),
            e("BUS-4160-B", "RELAY-87B"),
            e("BUS-4160-B", "RELAY-27B"),
            e("BUS-4160-B", "METER-B"),
            e("BUS-4160-B", "PT-41B"),
            e("BUS-125DC-A", "METER-DC-A"),
            e("BUS-125DC-B", "METER-DC-B"),
        ]
    )
    for lc in LOAD_CENTERS:
        x = lc["id"]
        r1, r2 = lc["relays"]
        edges.extend(
            [
                e(f"BUS-480-{x}", f"INST-{x}"),
                e(f"PNL-{x}", f"JB-{x}-1"),
                e(f"JB-{x}-1", r1),
                e(f"JB-{x}-1", r2),
            ]
        )
    for suffix, relay1, relay2, ann, rec, rps, inst, dcs, jb in [
        ("A", "RELAY-KA1", "RELAY-KA2", "ANN-A", "REC-SER-A", "PNL-RPS-A", "INST-NIS-A", "PNL-DCS-A", "JB-CTRL/A"),
        ("B", "RELAY-KB1", "RELAY-KB2", "ANN-B", "REC-SER-B", "PNL-RPS-B", "INST-NIS-B", "PNL-DCS-B", "JB-CTRL-B"),
    ]:
        bus = f"BUS-120AC-{suffix}"
        edges.extend(
            [
                e(bus, relay1),
                e(bus, relay2),
                e(bus, ann),
                e(bus, rec),
                e(rps, relay1),
                e(rps, relay2),
                e(rps, ann),
                e(rps, rec),
                e(rps, inst),
                e(rps, dcs),
                e(dcs, jb),
            ]
        )
    edges.extend([e("PNL-RADMON", "RELAY-KTIE"), e("RELAY-KTIE", "PNL-DCS-B")])
    return edges


DIEGO_R1_UNCERTAIN_EDGES = [
    e("BUS-4160-A", "CB-1C-FDR"),
    e("BUS-4160-A", "CB-2C-FDR"),
    e("BUS-4160-B", "CB-2B-FDR"),
    e("BUS-480-2C", "CB-DC-B"),
    e("BUS-120AC-A", "INST-NIS-A"),
    e("BUS-120AC-B", "INST-NIS-B"),
    e("BUS-24DC-C", "PNL-RPS-A"),
    e("BUS-24DC-C", "PNL-RPS-B"),
    e("BUS-24DC-C", "PNL-DCS-A"),
    e("BUS-24DC-C", "PNL-DCS-B"),
    e("BUS-24DC-C", "JB-CTRL/A"),
    e("BUS-24DC-C", "JB-CTRL-B"),
]


@dataclass(frozen=True)
class RoundResult:
    filename_stem: str
    agent: str
    round_label: str
    stance: str
    nodes: list[str]
    edges: list[tuple[str, str]]
    note: str


ROUNDS = [
    RoundResult(
        "round_01_diego",
        "Diego",
        "Round 1",
        "high-recall extractor",
        NODES,
        diego_round1_edges(),
        "High-recall pass included dashed/control/instrument candidates and initially fed 1C from ESF-A.",
    ),
    RoundResult(
        "round_02_jennifer",
        "Jennifer",
        "Round 1",
        "precision reviewer/refiner",
        NODES,
        without_edges(FINAL_EDGES, DIEGO_R2_ADDITIONS),
        "Precision pass removed dashed-only edges, corrected 1C to BUS-4160-A, and omitted several solid taps for Diego's recall check.",
    ),
    RoundResult(
        "round_03_diego",
        "Diego",
        "Round 2",
        "high-recall extractor",
        NODES,
        FINAL_EDGES,
        "Second pass agreed with dashed-edge removals and restored supported ground, DC-battery/charger, and 120 VAC panel/fuse taps.",
    ),
    RoundResult(
        "round_04_jennifer",
        "Jennifer",
        "Round 2 final",
        "precision reviewer/refiner",
        NODES,
        FINAL_EDGES,
        "Final review accepted Diego Round 2 supported taps and declared the extraction saturated.",
    ),
]


def unique_edges(edges: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str]] = []
    for edge in edges:
        ce = canonical_edge(edge)
        if ce not in seen:
            seen.add(ce)
            result.append(edge)
    return result


def validate(nodes: list[str], edges: list[tuple[str, str]]) -> dict:
    duplicate_nodes = sorted({node for node in nodes if nodes.count(node) > 1})
    node_set = set(nodes)
    missing = sorted({endpoint for edge in edges for endpoint in edge if endpoint not in node_set})
    self_edges = sorted([edge for edge in edges if edge[0] == edge[1]])
    duplicate_edges = []
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        ce = canonical_edge(edge)
        if ce in seen:
            duplicate_edges.append(edge)
        seen.add(ce)
    return {
        "node_count": len(nodes),
        "edge_count": len(unique_edges(edges)),
        "duplicate_nodes": duplicate_nodes,
        "missing_edge_nodes": missing,
        "self_edges": self_edges,
        "duplicate_edges": duplicate_edges,
        "symmetric": True,
        "diagonal_zero": len(self_edges) == 0,
        "valid": not duplicate_nodes and not missing and not self_edges and not duplicate_edges,
    }


def make_matrix(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in unique_edges(edges):
        ia = idx[a]
        ib = idx[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    return matrix


def write_matrix_csv(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = make_matrix(nodes, edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix, strict=True):
            writer.writerow([node, *row])


def write_nodes_csv(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_edges_csv(path: Path, edges: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        for a, b in unique_edges(edges):
            writer.writerow([a, b])


def estimate_text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def estimate_image_tokens(path: Path) -> int:
    with Image.open(path) as im:
        width, height = im.size
    return 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)


@dataclass(frozen=True)
class ModelCallEstimate:
    call_id: str
    document: str
    iteration: int
    agent: str
    agent_path: str
    round_label: str
    model: str
    input_text: str
    image_files: list[Path]
    output_tokens_expected: int
    output_tokens_low: int
    output_tokens_high: int
    reasoning_tokens_expected: int | None
    manual_text_input_tokens: int | None
    image_context_cached: bool
    usage_source: str
    notes: str

    def row(self) -> dict:
        text_tokens = (
            self.manual_text_input_tokens
            if self.manual_text_input_tokens is not None
            else estimate_text_tokens(self.input_text)
        )
        image_tokens = sum(estimate_image_tokens(path) for path in self.image_files if path.exists())
        input_expected = text_tokens + image_tokens
        reasoning_expected = self.reasoning_tokens_expected
        total_expected = input_expected + self.output_tokens_expected + (reasoning_expected or 0)
        cached_expected = image_tokens if self.image_context_cached else ""
        return {
            "document": self.document,
            "iteration": self.iteration,
            "call_id": self.call_id,
            "agent": self.agent,
            "agent_path": self.agent_path,
            "round": self.round_label,
            "model": self.model,
            "input_tokens_low": max(0, math.floor(input_expected * 0.80)),
            "input_tokens_expected": input_expected,
            "input_tokens_high": math.ceil(input_expected * 1.20),
            "cached_input_tokens_expected": cached_expected,
            "output_tokens_low": self.output_tokens_low,
            "output_tokens_expected": self.output_tokens_expected,
            "output_tokens_high": self.output_tokens_high,
            "reasoning_tokens_expected": "" if reasoning_expected is None else reasoning_expected,
            "image_file_count": len(self.image_files),
            "image_input_tokens_expected": image_tokens,
            "text_input_tokens_expected": text_tokens,
            "total_tokens_low": max(0, math.floor(input_expected * 0.80)) + self.output_tokens_low,
            "total_tokens_expected": total_expected,
            "total_tokens_high": math.ceil(input_expected * 1.20) + self.output_tokens_high,
            "usage_source": self.usage_source,
            "notes": self.notes,
        }


def img(name: str) -> Path:
    return CROPS_DIR / name


ROUND_IMAGES = [
    img("raw__overview_large.png"),
    img("wires_overlay__overview_large.png"),
    img("raw__top_band.png"),
    img("wires_overlay__top_band.png"),
    img("raw__upper_left_trains.png"),
    img("raw__upper_right_trains.png"),
    img("raw__lower_left.png"),
    img("raw__lower_mid.png"),
    img("raw__lower_right.png"),
    img("wires_overlay__bottom_band.png"),
    img("raw__dc_ups_left.png"),
    img("raw__dc_ups_right.png"),
]

BASE_PROMPT = (
    "Inspect only Raw + wires visual resources for document 23. Extract or review the undirected "
    "schematic connectivity matrix. GT and GT-derived feedback are forbidden. OCR engines are forbidden."
)

MODEL_CALLS = [
    ModelCallEstimate(
        "main_01_orchestration",
        DOC_ID,
        ITERATION,
        "main",
        "",
        "orchestration",
        "gpt-5",
        "User request plus current conversation context; create crops, coordinate Diego and Jennifer, write artifacts.",
        [],
        900,
        500,
        1500,
        None,
        26000,
        False,
        "estimated; main-agent usage object is not exposed in this environment",
        "Conversation cache and reasoning-token counts are unavailable.",
    ),
    ModelCallEstimate(
        "subagent_01_diego_round1",
        DOC_ID,
        ITERATION,
        "Diego",
        "019f7671-accf-7760-b815-bc67463a50e8",
        "Round 1",
        "gpt-5.5",
        BASE_PROMPT + " Role: high-recall extractor. Propose all visually/geometrically plausible components and edges.",
        ROUND_IMAGES,
        1750,
        1200,
        2800,
        None,
        None,
        False,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Initial payload included 12 downscaled visual crops.",
    ),
    ModelCallEstimate(
        "subagent_02_jennifer_round1",
        DOC_ID,
        ITERATION,
        "Jennifer",
        "019f7676-62e0-7080-bf82-83ce61b700ff",
        "Round 1",
        "gpt-5.5",
        BASE_PROMPT + " Role: precision reviewer/refiner. Review Diego Round 1 and remove unsupported edges.",
        ROUND_IMAGES,
        1250,
        850,
        2200,
        None,
        None,
        False,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Initial payload included Diego's proposal plus the same 12 visual crops.",
    ),
    ModelCallEstimate(
        "subagent_03_diego_round2",
        DOC_ID,
        ITERATION,
        "Diego",
        "019f7671-accf-7760-b815-bc67463a50e8",
        "Round 2",
        "gpt-5.5",
        BASE_PROMPT + " Follow-up in the same Diego thread: review Jennifer corrections and report any missing solid/grounding edge.",
        ROUND_IMAGES,
        250,
        120,
        500,
        None,
        None,
        True,
        "estimated; persistent subagent thread did not expose cached-token or total usage details",
        "Images were reused from the existing Diego thread; cached token amount is estimated as the image proxy total.",
    ),
    ModelCallEstimate(
        "subagent_04_jennifer_round2_final",
        DOC_ID,
        ITERATION,
        "Jennifer",
        "019f7676-62e0-7080-bf82-83ce61b700ff",
        "Round 2 final",
        "gpt-5.5",
        BASE_PROMPT + " Follow-up in the same Jennifer thread: adjudicate Diego Round 2 corrections and confirm saturation.",
        ROUND_IMAGES,
        170,
        90,
        350,
        None,
        None,
        True,
        "estimated; persistent subagent thread did not expose cached-token or total usage details",
        "Images were reused from the existing Jennifer thread; cached token amount is estimated as the image proxy total.",
    ),
]


ROUND_NOTES = """# Document 23 Round Notes

## Scope
- Used only resources under `Raw + wires`.
- No ground-truth file or GT-derived feedback was used.
- No OCR engine was used. Labels were read by visual inspection.

## Diego Round 1 - High Recall
Diego identified the 4160/source chains, ESF buses, ATS/DG feeds, six 480 V load centers (`1A`, `1C`, `1B`, `2A`, `2C`, `2B`), local MCC/load groups, DC/UPS buses, and lower control panels. His high-recall graph included dashed control/instrument candidates and initially placed `CB-1C-FDR` on `BUS-4160-ESF-A`.

## Jennifer Round 1 - Precision Refinement
Jennifer corrected `CB-1C-FDR` to `BUS-4160-A`, kept `CB-2A-FDR` and `CB-2C-FDR` on `BUS-4160-ESF-A`, kept `CB-2B-FDR` on `BUS-4160-ESF-B`, and confirmed `CB-DC-B` feeds from `BUS-480-2B`. She rejected dashed-only relay, metering, PT, instrument, DCS/JB, and KTIE/RADMON chains from the binary connectivity matrix. She confirmed labels `BUS-24DC-C` and `JB-CTRL/A`.

## Diego Round 2 - Recall Check
Diego accepted the dashed-edge removals and identified supported solid/grounding taps that Jennifer's first refinement had left out: 4160 bus grounds, 125 VDC battery/charger/ground taps, and 120 VAC fuse/RPS-panel drops.

## Jennifer Round 2 - Saturated Final
Jennifer accepted Diego Round 2's remaining supported taps and declared the extraction saturated. Final graph includes solid power lines and light-solid grounding. Dashed-only visual components are retained as visible nodes but isolated unless they also have a solid/grounding edge.
"""


FINAL_REJECTED_EDGES = [
    e("CB-TIE-41", "SYNC-41"),
    e("BUS-4160-A", "RELAY-87A"),
    e("BUS-4160-A", "RELAY-27A"),
    e("BUS-4160-A", "METER-A"),
    e("BUS-4160-A", "PT-41A"),
    e("BUS-4160-B", "RELAY-87B"),
    e("BUS-4160-B", "RELAY-27B"),
    e("BUS-4160-B", "METER-B"),
    e("BUS-4160-B", "PT-41B"),
    e("BUS-125DC-A", "METER-DC-A"),
    e("BUS-125DC-B", "METER-DC-B"),
    e("PNL-DCS-A", "JB-CTRL/A"),
    e("PNL-DCS-B", "JB-CTRL-B"),
    e("PNL-RADMON", "RELAY-KTIE"),
    e("RELAY-KTIE", "PNL-DCS-B"),
]

for lc in LOAD_CENTERS:
    x = lc["id"]
    r1, r2 = lc["relays"]
    FINAL_REJECTED_EDGES.extend(
        [
            e(f"BUS-480-{x}", f"INST-{x}"),
            e(f"PNL-{x}", f"JB-{x}-1"),
            e(f"JB-{x}-1", r1),
            e(f"JB-{x}-1", r2),
        ]
    )

for suffix, relay1, relay2, ann, rec, rps, inst, dcs, jb in [
    ("A", "RELAY-KA1", "RELAY-KA2", "ANN-A", "REC-SER-A", "PNL-RPS-A", "INST-NIS-A", "PNL-DCS-A", "JB-CTRL/A"),
    ("B", "RELAY-KB1", "RELAY-KB2", "ANN-B", "REC-SER-B", "PNL-RPS-B", "INST-NIS-B", "PNL-DCS-B", "JB-CTRL-B"),
]:
    bus = f"BUS-120AC-{suffix}"
    FINAL_REJECTED_EDGES.extend(
        [
            e(bus, relay1),
            e(bus, relay2),
            e(bus, ann),
            e(bus, rec),
            e(rps, relay1),
            e(rps, relay2),
            e(rps, ann),
            e(rps, rec),
            e(rps, inst),
            e(rps, dcs),
            e(dcs, jb),
        ]
    )


def write_rounds() -> dict:
    validations: dict[str, dict] = {}
    for round_result in ROUNDS:
        edges = unique_edges(round_result.edges)
        stem = round_result.filename_stem
        write_matrix_csv(RESULTS_DIR / f"{stem}_matrix.csv", round_result.nodes, edges)
        write_nodes_csv(RESULTS_DIR / f"{stem}_nodes.csv", round_result.nodes)
        write_edges_csv(RESULTS_DIR / f"{stem}_edges.csv", edges)
        validations[stem] = validate(round_result.nodes, edges)
    return validations


def write_token_estimates() -> list[dict]:
    rows = [call.row() for call in MODEL_CALLS]
    fields = list(rows[0].keys())
    with (RESULTS_DIR / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    grouped = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "estimation_method": (
            "No API key or Responses usage object was available. The preferred current endpoint is "
            "POST /v1/responses/input_tokens. Text tokens use tiktoken o200k_base when installed, "
            "else chars/4. Image tokens use 85 + 170 * ceil(width/512) * ceil(height/512) per image."
        ),
        "official_token_counting_guide": "https://developers.openai.com/api/docs/guides/token-counting",
        "official_count_endpoint_reference": "https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count/",
        "calls": rows,
        "totals": {
            "input_tokens_expected": sum(int(row["input_tokens_expected"]) for row in rows),
            "image_input_tokens_expected": sum(int(row["image_input_tokens_expected"]) for row in rows),
            "text_input_tokens_expected": sum(int(row["text_input_tokens_expected"]) for row in rows),
            "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in rows),
            "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
            "total_tokens_expected": sum(int(row["total_tokens_expected"]) for row in rows),
            "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        },
    }
    with (RESULTS_DIR / "token_usage_estimate.json").open("w", encoding="utf-8") as f:
        json.dump(grouped, f, indent=2)
    with (RESULTS_DIR / "token_usage_estimate.md").open("w", encoding="utf-8") as f:
        f.write("# Token Usage Estimate - Document 23\n\n")
        f.write(
            "Exact Responses usage objects were not exposed by the available subagent tooling, and no API key "
            "was available for `POST /v1/responses/input_tokens`. These values are proxy estimates.\n\n"
        )
        f.write("| Call | Agent | Round | Input expected | Cached expected | Image input expected | Output expected | Total expected |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            cached = row["cached_input_tokens_expected"] or ""
            f.write(
                f"| {row['call_id']} | {row['agent']} | {row['round']} | "
                f"{row['input_tokens_expected']} | {cached} | {row['image_input_tokens_expected']} | "
                f"{row['output_tokens_expected']} | {row['total_tokens_expected']} |\n"
            )
        f.write("\n")
        f.write(
            f"Expected total: {grouped['totals']['total_tokens_expected']} tokens "
            f"(low {grouped['totals']['total_tokens_low']}, high {grouped['totals']['total_tokens_high']}).\n"
        )
    return rows


def write_final_files() -> dict:
    final_edges = unique_edges(FINAL_EDGES)
    validation = validate(NODES, final_edges)
    write_matrix_csv(RESULTS_DIR / "connectivity_matrix_final.csv", NODES, final_edges)
    write_nodes_csv(RESULTS_DIR / "nodes_final.csv", NODES)
    write_edges_csv(RESULTS_DIR / "edges_final.csv", final_edges)
    write_edges_csv(RESULTS_DIR / "connectivity_sparse_final.csv", final_edges)
    write_edges_csv(RESULTS_DIR / "round_01_diego_uncertain_edges.csv", unique_edges(DIEGO_R1_UNCERTAIN_EDGES))
    write_edges_csv(RESULTS_DIR / "rejected_edges_final.csv", unique_edges(FINAL_REJECTED_EDGES))
    matrix = make_matrix(NODES, final_edges)
    isolated = sorted([node for node in NODES if all(node not in edge for edge in final_edges)])
    with (RESULTS_DIR / "isolated_visible_nodes_final.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"])
        for node in isolated:
            writer.writerow([node])
    with (RESULTS_DIR / "connectivity_matrix_final.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "nodes": NODES,
                "edges": final_edges,
                "matrix": matrix,
                "validation": validation,
                "isolated_visible_nodes": isolated,
                "edge_scope": "solid power lines plus light-solid grounding; dashed-only visual connections are rejected",
            },
            f,
            indent=2,
        )
    return validation


def main() -> None:
    CODES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    round_validations = write_rounds()
    final_validation = write_final_files()
    token_rows = write_token_estimates()

    with (RESULTS_DIR / "round_notes.md").open("w", encoding="utf-8") as f:
        f.write(ROUND_NOTES)

    validation_report = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "final": final_validation,
        "rounds": round_validations,
    }
    with (RESULTS_DIR / "validation_report.json").open("w", encoding="utf-8") as f:
        json.dump(validation_report, f, indent=2)

    manifest = {
        "document": DOC_ID,
        "iteration": ITERATION,
        "resource_root": str(ROOT),
        "codes_dir": str(CODES_DIR),
        "results_dir": str(RESULTS_DIR),
        "files": sorted(path.name for path in RESULTS_DIR.iterdir() if path.is_file()),
        "final_node_count": final_validation["node_count"],
        "final_edge_count": final_validation["edge_count"],
        "round_count": len(ROUNDS),
        "token_expected_total": sum(int(row["total_tokens_expected"]) for row in token_rows),
    }
    with (RESULTS_DIR / "artifact_manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    for script_name in ["doc23_make_visual_crops.py", "doc23_write_results.py"]:
        source = Path(script_name).resolve()
        if source.exists() and source != CODES_DIR / source.name:
            shutil.copy2(source, CODES_DIR / source.name)

    print(json.dumps({"final": final_validation, "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
