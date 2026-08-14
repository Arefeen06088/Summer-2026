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


DOC_ID = "22"
ITERATION = 1
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires"
)
CODES_DIR = ROOT / "codes"
RESULTS_DIR = ROOT / "results"
CROPS_DIR = CODES_DIR / "crops"


def train_nodes(prefix: str, trains: Iterable[str]) -> list[str]:
    return [f"{prefix}-{t}" for t in trains]


def load_breakers(prefix: str) -> list[str]:
    return [f"CB-{prefix}-{t}" for t in "ABCD"]


def load_nodes(prefix: str) -> list[str]:
    return [f"{prefix}-{t}" for t in "ABCD"]


NODES: list[str] = [
    "GEN-G01",
    "GSU-T01",
    "SWYD-345",
    "SRC-13.8-HDR",
    "CB-13A1",
    "CB-13B1",
    "CB-13T",
    "BUS-13A",
    "BUS-13B",
    "AUX-XFMR-1A",
    "AUX-XFMR-1B",
    "SAT-XFMR-1C",
    "SAT-XFMR-1D",
    "CB-4A-IN",
    "CB-4B-IN",
    "CB-4C-IN",
    "CB-4D-IN",
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-4160-C",
    "BUS-4160-D",
    "DG-1A",
    "DG-1B",
    "DG-1C",
    "DG-1D",
    "CB-DG-A",
    "CB-DG-B",
    "CB-DG-C",
    "CB-DG-D",
    "CB-4AB-TIE",
    "CB-4CD-TIE",
    "CB-LC-A",
    "CB-LC-B",
    "CB-LC-C",
    "CB-LC-D",
    "TR-LC-A",
    "TR-LC-B",
    "TR-LC-C",
    "TR-LC-D",
    "BUS-480-A",
    "BUS-480-B",
    "BUS-480-C",
    "BUS-480-D",
    "SYNC-PNL-1",
    "RELAY-87U",
    "CB-MCC-AA",
    "MCC-AA",
    "CB-MCC-AB",
    "MCC-AB",
    "CB-MCC-BA",
    "MCC-BA",
    "CB-MCC-BB",
    "MCC-BB",
    "CB-MCC-CA",
    "MCC-CA",
    "CB-MCC-CB",
    "MCC-CB",
    "CB-MCC-DA",
    "MCC-DA",
    "CB-MCC-DB",
    "MCC-DB",
]

for train in "ABCD":
    NODES.extend(
        [
            f"CB-RHR-{train}",
            f"PUMP-RHR-{train}",
            f"CB-SI-{train}",
            f"PUMP-SI-{train}",
            f"CB-CCW-{train}",
            f"PUMP-CCW-{train}",
            f"CB-FAN-{train}",
            f"FAN-CR-{train}",
            f"CB-CH-{train}",
            f"CHILLER-{train}",
            f"CB-VLV1-{train}",
            f"MOV-HV1-{train}",
            f"CB-VLV2-{train}",
            f"MOV-HV2-{train}",
            f"CB-SPARE-{train}",
            f"SPARE-LOAD-{train}",
            f"INST-PT-{train}",
            f"INST-CT-{train}",
            f"XFMR-120-{train}",
            f"PNL-120-{train}",
            f"RELAY-K{train}1",
            f"RELAY-K{train}2",
            f"JB-{train}1",
            f"TERM-{train}",
            f"GND-{train}",
        ]
    )

NODES.extend(
    [
        "CB-DC-A1",
        "CB-DC-B1",
        "CHGR-125A",
        "CHGR-125B",
        "BUS-125A",
        "BUS-125B",
        "BAT-125A",
        "BAT-125B",
        "FUSE-FD-A",
        "FUSE-FD-B",
        "INV-UPS-A",
        "INV-UPS-B",
        "BUS-UPS-A",
        "BUS-UPS-B",
        "DC-MCC-A",
        "DC-MCC-B",
        "SOL-SDV-A",
        "SOL-SDV-B",
        "DIODE-OR-A",
        "DIODE-OR-B",
        "GRD-DC-A",
        "GRD-DC-B",
        "INST-RACK-A",
        "INST-RACK-B",
        "PNL-RPS-A",
        "PNL-RPS-B",
        "RELAY-RPS-A1",
        "RELAY-RPS-B1",
        "RELAY-ESF-A",
        "RELAY-ESF-B",
        "PLC-SAF-A",
        "PLC-SAF-B",
        "ANN-PNL-CR",
        "JB-CR-01",
        "TERM-MTB-A",
        "TERM-MTB-B",
        "REC-SEQ-1",
        "XFRM-PT-1",
        "METER-V01",
        "METER-A01",
    ]
)


def e(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-edge not expected: {a}")
    return (a, b)


FINAL_EDGES: list[tuple[str, str]] = [
    e("GEN-G01", "GSU-T01"),
    e("GSU-T01", "SWYD-345"),
    e("SWYD-345", "SRC-13.8-HDR"),
    e("SRC-13.8-HDR", "CB-13A1"),
    e("CB-13A1", "BUS-13A"),
    e("SRC-13.8-HDR", "CB-13B1"),
    e("CB-13B1", "BUS-13B"),
    e("BUS-13A", "CB-13T"),
    e("CB-13T", "BUS-13B"),
    e("BUS-13A", "AUX-XFMR-1A"),
    e("AUX-XFMR-1A", "CB-4A-IN"),
    e("CB-4A-IN", "BUS-4160-A"),
    e("BUS-13A", "AUX-XFMR-1B"),
    e("AUX-XFMR-1B", "CB-4B-IN"),
    e("CB-4B-IN", "BUS-4160-B"),
    e("BUS-13B", "SAT-XFMR-1C"),
    e("SAT-XFMR-1C", "CB-4C-IN"),
    e("CB-4C-IN", "BUS-4160-C"),
    e("BUS-13B", "SAT-XFMR-1D"),
    e("SAT-XFMR-1D", "CB-4D-IN"),
    e("CB-4D-IN", "BUS-4160-D"),
    e("DG-1A", "CB-DG-A"),
    e("CB-DG-A", "BUS-4160-A"),
    e("DG-1B", "CB-DG-B"),
    e("CB-DG-B", "BUS-4160-B"),
    e("DG-1C", "CB-DG-C"),
    e("CB-DG-C", "BUS-4160-C"),
    e("DG-1D", "CB-DG-D"),
    e("CB-DG-D", "BUS-4160-D"),
    e("BUS-4160-A", "CB-4AB-TIE"),
    e("CB-4AB-TIE", "BUS-4160-B"),
    e("BUS-4160-C", "CB-4CD-TIE"),
    e("CB-4CD-TIE", "BUS-4160-D"),
    e("BUS-4160-A", "SYNC-PNL-1"),
    e("SYNC-PNL-1", "CB-DG-A"),
    e("BUS-13A", "RELAY-87U"),
    e("RELAY-87U", "CB-4B-IN"),
]

for train in "ABCD":
    FINAL_EDGES.extend(
        [
            e(f"BUS-4160-{train}", f"CB-LC-{train}"),
            e(f"CB-LC-{train}", f"TR-LC-{train}"),
            e(f"TR-LC-{train}", f"BUS-480-{train}"),
            e(f"BUS-480-{train}", f"XFMR-120-{train}"),
            e(f"XFMR-120-{train}", f"PNL-120-{train}"),
            e(f"BUS-480-{train}", f"GND-{train}"),
            e(f"BUS-480-{train}", f"INST-PT-{train}"),
        ]
    )

MCC_PAIRS = {
    "A": ("MCC-AA", "MCC-AB", "CB-MCC-AA", "CB-MCC-AB"),
    "B": ("MCC-BA", "MCC-BB", "CB-MCC-BA", "CB-MCC-BB"),
    "C": ("MCC-CA", "MCC-CB", "CB-MCC-CA", "CB-MCC-CB"),
    "D": ("MCC-DA", "MCC-DB", "CB-MCC-DA", "CB-MCC-DB"),
}

LEFT_FEEDERS = [
    ("CB-RHR", "PUMP-RHR"),
    ("CB-SI", "PUMP-SI"),
    ("CB-CCW", "PUMP-CCW"),
    ("CB-FAN", "FAN-CR"),
]
RIGHT_FEEDERS = [
    ("CB-CH", "CHILLER"),
    ("CB-VLV1", "MOV-HV1"),
    ("CB-VLV2", "MOV-HV2"),
    ("CB-SPARE", "SPARE-LOAD"),
]

for train, (left_mcc, right_mcc, left_cb, right_cb) in MCC_PAIRS.items():
    FINAL_EDGES.extend(
        [
            e(f"BUS-480-{train}", left_cb),
            e(left_cb, left_mcc),
            e(f"BUS-480-{train}", right_cb),
            e(right_cb, right_mcc),
        ]
    )
    for cb_prefix, load_prefix in LEFT_FEEDERS:
        FINAL_EDGES.extend(
            [
                e(left_mcc, f"{cb_prefix}-{train}"),
                e(f"{cb_prefix}-{train}", f"{load_prefix}-{train}"),
            ]
        )
    for cb_prefix, load_prefix in RIGHT_FEEDERS:
        FINAL_EDGES.extend(
            [
                e(right_mcc, f"{cb_prefix}-{train}"),
                e(f"{cb_prefix}-{train}", f"{load_prefix}-{train}"),
            ]
        )

for train in "ABCD":
    FINAL_EDGES.extend(
        [
            e(f"PNL-120-{train}", f"RELAY-K{train}1"),
            e(f"PNL-120-{train}", f"RELAY-K{train}2"),
            e(f"RELAY-K{train}1", f"JB-{train}1"),
            e(f"JB-{train}1", f"TERM-{train}"),
        ]
    )

FINAL_EDGES.extend(
    [
        e("CB-DC-A1", "CHGR-125A"),
        e("CHGR-125A", "BUS-125A"),
        e("BUS-125A", "BAT-125A"),
        e("BUS-125A", "DC-MCC-A"),
        e("DC-MCC-A", "SOL-SDV-A"),
        e("BUS-125A", "DIODE-OR-A"),
        e("BUS-125A", "GRD-DC-A"),
        e("BUS-125A", "FUSE-FD-A"),
        e("FUSE-FD-A", "INV-UPS-A"),
        e("INV-UPS-A", "BUS-UPS-A"),
        e("CB-DC-B1", "CHGR-125B"),
        e("CHGR-125B", "BUS-125B"),
        e("BUS-125B", "BAT-125B"),
        e("BUS-125B", "DC-MCC-B"),
        e("DC-MCC-B", "SOL-SDV-B"),
        e("BUS-125B", "DIODE-OR-B"),
        e("BUS-125B", "GRD-DC-B"),
        e("BUS-125B", "FUSE-FD-B"),
        e("FUSE-FD-B", "INV-UPS-B"),
        e("INV-UPS-B", "BUS-UPS-B"),
        e("BUS-UPS-A", "PNL-RPS-A"),
        e("PNL-RPS-A", "RELAY-RPS-A1"),
        e("PNL-RPS-A", "RELAY-ESF-A"),
        e("BUS-UPS-A", "PLC-SAF-A"),
        e("BUS-UPS-A", "INST-RACK-A"),
        e("BUS-UPS-A", "ANN-PNL-CR"),
        e("ANN-PNL-CR", "JB-CR-01"),
        e("JB-CR-01", "TERM-MTB-A"),
        e("JB-CR-01", "TERM-MTB-B"),
        e("BUS-UPS-B", "PNL-RPS-B"),
        e("PNL-RPS-B", "RELAY-RPS-B1"),
        e("PNL-RPS-B", "RELAY-ESF-B"),
        e("BUS-UPS-B", "PLC-SAF-B"),
        e("BUS-UPS-B", "INST-RACK-B"),
        e("BUS-UPS-B", "REC-SEQ-1"),
        e("XFRM-PT-1", "METER-V01"),
    ]
)


DIEGO_R1_EXTRA_EDGES: list[tuple[str, str]] = [
    e("XFRM-PT-1", "METER-A01"),
]

for train, (left_mcc, _right_mcc, _left_cb, _right_cb) in MCC_PAIRS.items():
    DIEGO_R1_EXTRA_EDGES.extend(
        [
            e(left_mcc, f"INST-CT-{train}"),
            e(f"INST-CT-{train}", f"CB-RHR-{train}"),
        ]
    )


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
        FINAL_EDGES + DIEGO_R1_EXTRA_EDGES,
        "High-recall pass retained visually plausible CT-series and ammeter/PT candidates for review.",
    ),
    RoundResult(
        "round_02_jennifer",
        "Jennifer",
        "Round 1",
        "precision reviewer/refiner",
        NODES,
        FINAL_EDGES,
        "Precision pass removed unsupported CT-series and METER-A01 links; added explicit SRC-13.8-HDR.",
    ),
    RoundResult(
        "round_03_diego",
        "Diego",
        "Round 2",
        "high-recall extractor",
        NODES,
        FINAL_EDGES,
        "Second extraction agreed with Jennifer and made every MCC incomer path explicit.",
    ),
    RoundResult(
        "round_04_jennifer",
        "Jennifer",
        "Round 2 final",
        "precision reviewer/refiner",
        NODES,
        FINAL_EDGES,
        "Final review found no remaining supported corrections; matrix saturated.",
    ),
]


def canonical_edge(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


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
    # High-detail proxy when exact API token counting is unavailable:
    # one base image plus 512 px tiles over the supplied pixel dimensions.
    with Image.open(path) as im:
        width, height = im.size
    return 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)


@dataclass(frozen=True)
class ModelCallEstimate:
    call_id: str
    document: str
    iteration: int
    agent: str
    round_label: str
    agent_path: str
    model: str
    input_text: str
    image_files: list[Path]
    output_tokens_expected: int
    output_tokens_low: int
    output_tokens_high: int
    reasoning_tokens_expected: int | None
    cached_input_tokens: int | None
    manual_text_input_tokens: int | None
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
        output_expected = self.output_tokens_expected
        reasoning_expected = self.reasoning_tokens_expected
        total_expected = input_expected + output_expected + (reasoning_expected or 0)
        return {
            "document": self.document,
            "iteration": self.iteration,
            "call_id": self.call_id,
            "agent": self.agent,
            "agent_path": self.agent_path,
            "round": self.round_label,
            "model": self.model,
            "input_tokens_low": max(0, math.floor(input_expected * 0.85)),
            "input_tokens_expected": input_expected,
            "input_tokens_high": math.ceil(input_expected * 1.15),
            "cached_input_tokens": "" if self.cached_input_tokens is None else self.cached_input_tokens,
            "output_tokens_low": self.output_tokens_low,
            "output_tokens_expected": output_expected,
            "output_tokens_high": self.output_tokens_high,
            "reasoning_tokens_expected": "" if reasoning_expected is None else reasoning_expected,
            "image_file_count": len(self.image_files),
            "image_input_tokens_expected": image_tokens,
            "text_input_tokens_expected": text_tokens,
            "total_tokens_low": max(0, math.floor(input_expected * 0.85)) + self.output_tokens_low,
            "total_tokens_expected": total_expected,
            "total_tokens_high": math.ceil(input_expected * 1.15) + self.output_tokens_high,
            "usage_source": self.usage_source,
            "notes": self.notes,
        }


def img(name: str) -> Path:
    return CROPS_DIR / name


DIEGO_R1_IMAGES = [
    img("raw__overview.png"),
    img("raw__top_band.png"),
    img("raw__upper_middle_band.png"),
    img("raw__middle_band.png"),
    img("raw__bottom_band.png"),
    *[img(f"raw__grid_r{r}c{c}_2x.png") for r in range(1, 5) for c in range(1, 5)],
    img("wires_overlay__overview.png"),
    img("wires_overlay__upper_middle_band.png"),
    img("wires_overlay__middle_band.png"),
    img("wires_overlay__bottom_band.png"),
]

JENNIFER_R1_IMAGES = [
    img("raw__overview.png"),
    img("raw__top_band.png"),
    img("raw__upper_middle_band.png"),
    img("raw__middle_band.png"),
    img("raw__bottom_band.png"),
    *[img(f"raw__grid_r1c{c}_2x.png") for c in range(1, 5)],
    *[img(f"raw__grid_r2c{c}_2x.png") for c in range(1, 5)],
    *[img(f"raw__grid_r3c{c}_2x.png") for c in range(1, 4)],
    *[img(f"raw__grid_r4c{c}_2x.png") for c in range(1, 4)],
    img("wires_overlay__top_band.png"),
    img("wires_overlay__upper_middle_band.png"),
    img("wires_overlay__middle_band.png"),
    img("wires_overlay__bottom_band.png"),
]

DIEGO_R2_IMAGES = [
    img("raw__overview.png"),
    img("raw__top_band.png"),
    img("raw__upper_middle_band.png"),
    img("raw__middle_band.png"),
    img("raw__bottom_band.png"),
    img("raw__grid_r1c1_2x.png"),
    img("raw__grid_r1c2_2x.png"),
    img("raw__grid_r2c1_2x.png"),
    img("raw__trainA_mcc_feeders_3x.png"),
    img("raw__grid_r4c1_2x.png"),
    img("raw__grid_r4c2_2x.png"),
    img("raw__grid_r4c3_2x.png"),
    img("wires_overlay__bottom_band.png"),
    img("wires_overlay__middle_band.png"),
]

JENNIFER_R2_IMAGES = [
    img("raw__overview.png"),
    img("raw__top_band.png"),
    img("raw__middle_band.png"),
    img("raw__bottom_band.png"),
    img("raw__trainA_mcc_feeders_3x.png"),
    img("raw__grid_r4c2_2x.png"),
    img("raw__grid_r4c3_2x.png"),
]

BASE_SUBAGENT_PROMPT = (
    "Inspect only the Raw + wires visual resources for document 22. Extract or review the "
    "undirected schematic connectivity matrix. Ground-truth files and GT-derived feedback are "
    "forbidden. Do not use OCR engines. Use visual inspection of raw, wire mask, and overlay crops."
)

MODEL_CALLS = [
    ModelCallEstimate(
        "main_01_orchestration",
        DOC_ID,
        ITERATION,
        "main",
        "orchestration",
        "",
        "gpt-5",
        "User request plus current conversation context; create crops, coordinate Diego and Jennifer, write artifacts.",
        [],
        900,
        500,
        1500,
        None,
        None,
        24000,
        "estimated; main-agent usage object is not exposed in this environment",
        "Conversation cache and reasoning-token counts are unavailable.",
    ),
    ModelCallEstimate(
        "subagent_01_diego_round1",
        DOC_ID,
        ITERATION,
        "Diego",
        "Round 1",
        "019f7656-2121-7330-bf54-5c11023313c6",
        "gpt-5.5",
        BASE_SUBAGENT_PROMPT
        + " Role: high-recall extractor. Propose every visually or geometrically plausible component, label, node, and edge with evidence.",
        DIEGO_R1_IMAGES,
        1700,
        1200,
        2600,
        None,
        None,
        None,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Image token estimate uses a high-detail 512-px tile proxy.",
    ),
    ModelCallEstimate(
        "subagent_02_jennifer_round1",
        DOC_ID,
        ITERATION,
        "Jennifer",
        "Round 1",
        "019f765c-96cb-7a40-af9c-9ae5e5e9da3a",
        "gpt-5.5",
        BASE_SUBAGENT_PROMPT
        + " Role: precision reviewer/refiner. Check Diego Round 1, remove unsupported edges, and mark ambiguity instead of guessing.",
        JENNIFER_R1_IMAGES,
        1450,
        1000,
        2200,
        None,
        None,
        None,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Output includes accepted and rejected edge decisions.",
    ),
    ModelCallEstimate(
        "subagent_03_diego_round2",
        DOC_ID,
        ITERATION,
        "Diego",
        "Round 2",
        "019f7662-4236-7193-bd19-b46c177fba3f",
        "gpt-5.5",
        BASE_SUBAGENT_PROMPT
        + " Review Jennifer Round 1 corrections and state whether any high-recall supported edges remain missing.",
        DIEGO_R2_IMAGES,
        450,
        250,
        800,
        None,
        None,
        None,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Second pass reached agreement and explicitly checked MCC incomers.",
    ),
    ModelCallEstimate(
        "subagent_04_jennifer_round2_final",
        DOC_ID,
        ITERATION,
        "Jennifer",
        "Round 2 final",
        "019f7666-51a2-7d01-a35a-095d5a93a072",
        "gpt-5.5",
        BASE_SUBAGENT_PROMPT
        + " Final saturation review. Confirm no supported corrections remain and identify any still-isolated visible components.",
        JENNIFER_R2_IMAGES,
        180,
        100,
        400,
        None,
        None,
        None,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Final response confirmed saturation.",
    ),
]


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
            "No API key or usage object was available. Text tokens use tiktoken o200k_base when installed, "
            "else chars/4. Image tokens use 85 + 170 * ceil(width/512) * ceil(height/512) per supplied image."
        ),
        "responses_count_input_tokens_endpoint": "https://developers.openai.com/api/reference/responses/count-input-tokens",
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
        f.write("# Token Usage Estimate - Document 22\n\n")
        f.write(
            "Exact Responses usage objects were not exposed by the available subagent tooling, and no API key "
            "was available for the Responses input-token counting endpoint. These values are proxy estimates.\n\n"
        )
        f.write("| Call | Agent | Round | Input expected | Image input expected | Output expected | Total expected |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            f.write(
                f"| {row['call_id']} | {row['agent']} | {row['round']} | "
                f"{row['input_tokens_expected']} | {row['image_input_tokens_expected']} | "
                f"{row['output_tokens_expected']} | {row['total_tokens_expected']} |\n"
            )
        f.write("\n")
        f.write(
            f"Expected total: {grouped['totals']['total_tokens_expected']} tokens "
            f"(low {grouped['totals']['total_tokens_low']}, high {grouped['totals']['total_tokens_high']}).\n"
        )
    return rows


ROUND_NOTES = """# Document 22 Round Notes

## Scope
- Used only resources under `Raw + wires`.
- No ground-truth file or GT-derived feedback was used.
- No OCR engine was used. Labels were read by visual inspection.

## Diego Round 1 - High Recall
Diego identified the full power-distribution structure: generator, GSU, switchyard, 13.8 kV source/header, 13.8 kV buses, 4160 V trains A-D, DG incomers, 480 V load centers, MCCs, AC loads, 125 V DC/UPS systems, RPS/ESF/PLC panels, junctions, terminals, and metering.

High-recall candidates retained for Jennifer included `XFRM-PT-1--METER-A01` and per-train CT series candidates from the left MCC to `INST-CT-*` and `CB-RHR-*`.

## Jennifer Round 1 - Precision Refinement
Jennifer kept the visually supported bus, breaker, transformer, MCC, load, DC/UPS, control-panel, junction, and metering connections. She removed the CT-series and `METER-A01` candidates because the raw and overlay crops did not show confirmed solid-wire connections. She treated `C-030`, `C-031`, `W-011`, and `W-022` as wire/cable annotations, not components. She added `SRC-13.8-HDR` as the unlabeled physical top source/header node feeding both `CB-13A1` and `CB-13B1` from the switchyard.

## Diego Round 2 - Agreement Check
Diego accepted Jennifer's corrections and made the eight MCC incomer paths explicit:
`BUS-480-A--CB-MCC-AA--MCC-AA`, `BUS-480-A--CB-MCC-AB--MCC-AB`,
`BUS-480-B--CB-MCC-BA--MCC-BA`, `BUS-480-B--CB-MCC-BB--MCC-BB`,
`BUS-480-C--CB-MCC-CA--MCC-CA`, `BUS-480-C--CB-MCC-CB--MCC-CB`,
`BUS-480-D--CB-MCC-DA--MCC-DA`, and `BUS-480-D--CB-MCC-DB--MCC-DB`.

## Jennifer Round 2 - Saturated Final
Jennifer confirmed the final matrix:
- `SRC-13.8-HDR` remains a logical/physical unlabeled source header.
- `INST-CT-A`, `INST-CT-B`, `INST-CT-C`, `INST-CT-D`, and `METER-A01` remain visible but isolated because direct solid-wire edges are not confirmed.
- The only confirmed PT/meter connection is `XFRM-PT-1--METER-V01`.
- The final edge set is saturated with Diego's Round 2 proposal.
"""


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


def write_final_files() -> dict:
    final_edges = unique_edges(FINAL_EDGES)
    validation = validate(NODES, final_edges)
    write_matrix_csv(RESULTS_DIR / "connectivity_matrix_final.csv", NODES, final_edges)
    write_nodes_csv(RESULTS_DIR / "nodes_final.csv", NODES)
    write_edges_csv(RESULTS_DIR / "edges_final.csv", final_edges)
    write_edges_csv(RESULTS_DIR / "connectivity_sparse_final.csv", final_edges)
    matrix = make_matrix(NODES, final_edges)
    with (RESULTS_DIR / "connectivity_matrix_final.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "document": DOC_ID,
                "iteration": ITERATION,
                "nodes": NODES,
                "edges": final_edges,
                "matrix": matrix,
                "validation": validation,
                "isolated_visible_nodes": [
                    "INST-CT-A",
                    "INST-CT-B",
                    "INST-CT-C",
                    "INST-CT-D",
                    "METER-A01",
                ],
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

    source = Path(__file__).resolve()
    target = CODES_DIR / source.name
    if source != target:
        shutil.copy2(source, target)

    crop_script = Path("doc22_make_visual_crops.py").resolve()
    if crop_script.exists():
        shutil.copy2(crop_script, CODES_DIR / crop_script.name)

    print(json.dumps({"final": final_validation, "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
