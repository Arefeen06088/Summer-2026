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

DOC_ID = "24"
ITERATION = 1
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\24\Raw + wires"
)
CODES_DIR = ROOT / "codes"
RESULTS_DIR = ROOT / "results"
CROPS_DIR = CODES_DIR / "crops"


@dataclass(frozen=True)
class TypedEdge:
    source: str
    target: str
    edge_type: str
    evidence: str = ""


def te(source: str, target: str, edge_type: str, evidence: str = "") -> TypedEdge:
    if source == target:
        raise ValueError(f"self-edge not expected: {source}")
    return TypedEdge(source, target, edge_type, evidence)


def canonical_edge(edge: TypedEdge | tuple[str, str]) -> tuple[str, str]:
    if isinstance(edge, TypedEdge):
        a, b = edge.source, edge.target
    else:
        a, b = edge
    return tuple(sorted((a, b)))


def unique_typed_edges(edges: Iterable[TypedEdge]) -> list[TypedEdge]:
    seen: set[tuple[str, str]] = set()
    result: list[TypedEdge] = []
    for edge in edges:
        ce = canonical_edge(edge)
        if ce not in seen:
            seen.add(ce)
            result.append(edge)
    return result


TOP_NODES = [
    "OFFSITE-1",
    "CB-101A",
    "TR-SAT-1A",
    "BUS-101A",
    "EDG-1A",
    "CB-DG1A",
    "SW-MAN-A",
    "TB-DG-A",
    "CB-201A",
    "TR-1A",
    "CB-202A",
    "BUS-201A",
    "CB-TIE-1",
    "BUS-101B",
    "OFFSITE-2",
    "CB-101B",
    "TR-SAT-1B",
    "EDG-1B",
    "CB-DG1B",
    "SW-MAN-B",
    "TB-DG-B",
    "CB-201B",
    "TR-1B",
    "CB-202B",
    "BUS-201B",
]

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


def feeder_nodes(train: str, loads: dict[str, str]) -> list[str]:
    nodes: list[str] = []
    for n in loads:
        prefix = f"2{train}{n}"
        nodes.extend(
            [
                f"CB-{prefix}",
                f"DS-{prefix}",
                f"MCC-{prefix}",
                f"TB-{prefix}",
                f"HS-{prefix}",
                f"RELAY-K{prefix}",
                loads[n],
            ]
        )
    return nodes


BOTTOM_NODES = [
    "DC-BUS-125A",
    "BAT-125A",
    "CHG-125A",
    "INV-120A",
    "PNL-DC-A",
    "ESFAS-PNL-A",
    "METER-V1",
    "PNL-AC-A",
    "RPS-PNL-A",
    "TRIP-MOD-A",
    "GND-DC-A",
    "PT-401A",
    "LT-402A",
    "FT-403A",
    "JB-401A",
    "TB-RPS-A",
    "GND-401A",
    "RELAY-K27A",
    "RELAY-K59A",
    "RELAY-K81A",
    "RELAY-K86A",
    "DC-BUS-125B",
    "BAT-125B",
    "CHG-125B",
    "INV-120B",
    "PNL-DC-B",
    "ESFAS-PNL-B",
    "PNL-AC-B",
    "RPS-PNL-B",
    "TRIP-MOD-B",
    "GND-DC-B",
    "PT-401B",
    "LT-402B",
    "FT-403B",
    "JB-401B",
    "TB-RPS-B",
    "GND-401B",
    "RELAY-K27B",
    "RELAY-K59B",
    "RELAY-K81B",
    "RELAY-K86B",
    "SYNC-CAB",
    "LOAD-SHED-CAB",
    "TDR-1",
    "TDR-2",
    "LAMP-ALM-A",
    "LAMP-ALM-B",
    "ANN-PNL-1",
    "SEQ-REC-1",
]

NODES = [*TOP_NODES, *feeder_nodes("A", A_LOADS), *feeder_nodes("B", B_LOADS), *BOTTOM_NODES]


def final_edges() -> list[TypedEdge]:
    edges: list[TypedEdge] = [
        te("OFFSITE-1", "CB-101A", "solid power/DC", "offsite A solid source line"),
        te("CB-101A", "TR-SAT-1A", "solid power/DC", "inline source transformer chain"),
        te("TR-SAT-1A", "BUS-101A", "solid power/DC", "solid tap with junction dot"),
        te("EDG-1A", "CB-DG1A", "solid power/DC", "EDG A solid breaker feed"),
        te("CB-DG1A", "BUS-101A", "solid power/DC", "junction dot on BUS-101A"),
        te("SW-MAN-A", "TB-DG-A", "dashed control/trip", "generator manual control dashed path"),
        te("TB-DG-A", "CB-DG1A", "dashed control/trip", "dashed path terminates at DG breaker"),
        te("BUS-101A", "CB-201A", "solid power/DC", "vertical transformer feed from BUS-101A"),
        te("CB-201A", "TR-1A", "solid power/DC", "inline transformer chain"),
        te("TR-1A", "CB-202A", "solid power/DC", "inline transformer chain"),
        te("CB-202A", "BUS-201A", "solid power/DC", "junction dot on BUS-201A"),
        te("BUS-101A", "CB-TIE-1", "solid power/DC", "101 bus tie breaker"),
        te("CB-TIE-1", "BUS-101B", "solid power/DC", "101 bus tie breaker"),
        te("OFFSITE-2", "CB-101B", "solid power/DC", "offsite B solid source line"),
        te("CB-101B", "TR-SAT-1B", "solid power/DC", "inline source transformer chain"),
        te("TR-SAT-1B", "BUS-101B", "solid power/DC", "solid tap with junction dot"),
        te("EDG-1B", "CB-DG1B", "solid power/DC", "EDG B solid breaker feed"),
        te("CB-DG1B", "BUS-101B", "solid power/DC", "junction dot on BUS-101B"),
        te("SW-MAN-B", "TB-DG-B", "dashed control/trip", "generator manual control dashed path"),
        te("TB-DG-B", "CB-DG1B", "dashed control/trip", "dashed path terminates at DG breaker"),
        te("BUS-101B", "CB-201B", "solid power/DC", "vertical transformer feed from BUS-101B"),
        te("CB-201B", "TR-1B", "solid power/DC", "inline transformer chain"),
        te("TR-1B", "CB-202B", "solid power/DC", "inline transformer chain"),
        te("CB-202B", "BUS-201B", "solid power/DC", "junction dot on BUS-201B"),
    ]

    def add_feeder(train: str, bus: str, loads: dict[str, str]) -> None:
        for n, load in loads.items():
            prefix = f"2{train}{n}"
            edges.extend(
                [
                    te(bus, f"CB-{prefix}", "solid power/DC", "solid feeder tap from safety bus"),
                    te(f"CB-{prefix}", f"DS-{prefix}", "solid power/DC", "vertical feeder chain"),
                    te(f"DS-{prefix}", f"MCC-{prefix}", "solid power/DC", "vertical feeder chain"),
                    te(f"MCC-{prefix}", f"TB-{prefix}", "solid power/DC", "vertical feeder chain"),
                    te(f"TB-{prefix}", load, "solid power/DC", "vertical feeder chain to load"),
                    te(f"MCC-{prefix}", f"RELAY-K{prefix}", "dashed control/trip", "dashed MCC control drop"),
                ]
            )
        ordered = list(loads)
        for i, n in enumerate(ordered):
            prefix = f"2{train}{n}"
            edges.append(
                te(f"HS-{prefix}", f"RELAY-K{prefix}", "dashed control/trip", "dashed HS/relay row")
            )
            if i < len(ordered) - 1:
                next_prefix = f"2{train}{ordered[i + 1]}"
                edges.append(
                    te(
                        f"RELAY-K{prefix}",
                        f"HS-{next_prefix}",
                        "dashed control/trip",
                        "dashed daisy chain across HS/relay row",
                    )
                )

    add_feeder("A", "BUS-201A", A_LOADS)
    add_feeder("B", "BUS-201B", B_LOADS)

    edges.extend(
        [
            te("DC-BUS-125A", "BAT-125A", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125A", "CHG-125A", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125A", "INV-120A", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125A", "PNL-DC-A", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125A", "METER-V1", "solid power/DC", "125 VDC meter tap"),
            te("PNL-DC-A", "ESFAS-PNL-A", "solid power/DC", "solid panel link"),
            te("PNL-DC-A", "GND-DC-A", "ground/reference", "solid ground drop"),
            te("INV-120A", "PNL-AC-A", "solid power/DC", "inverter output to AC panel"),
            te("PNL-AC-A", "RPS-PNL-A", "dashed control/trip", "dashed control route"),
            te("RPS-PNL-A", "TRIP-MOD-A", "dashed control/trip", "dashed control route"),
            te("RPS-PNL-A", "RELAY-K27A", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K27A", "RELAY-K59A", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K59A", "RELAY-K81A", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K81A", "RELAY-K86A", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K86A", "TRIP-MOD-A", "dashed control/trip", "dashed relay trip chain"),
            te("PT-401A", "JB-401A", "dotted signal", "instrument signal route"),
            te("LT-402A", "JB-401A", "dotted signal", "instrument signal route"),
            te("FT-403A", "JB-401A", "dotted signal", "instrument signal route"),
            te("JB-401A", "TB-RPS-A", "dotted signal", "signal route through terminal block"),
            te("TB-RPS-A", "RPS-PNL-A", "dotted signal", "signal route into RPS panel"),
            te("JB-401A", "GND-401A", "ground/reference", "solid ground/reference drop"),
            te("DC-BUS-125B", "BAT-125B", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125B", "CHG-125B", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125B", "INV-120B", "solid power/DC", "125 VDC bus tap"),
            te("DC-BUS-125B", "PNL-DC-B", "solid power/DC", "125 VDC bus tap"),
            te("PNL-DC-B", "ESFAS-PNL-B", "solid power/DC", "solid panel link"),
            te("PNL-DC-B", "GND-DC-B", "ground/reference", "solid ground drop"),
            te("INV-120B", "PNL-AC-B", "solid power/DC", "inverter output to AC panel"),
            te("PNL-AC-B", "RPS-PNL-B", "dashed control/trip", "dashed control route"),
            te("RPS-PNL-B", "TRIP-MOD-B", "dashed control/trip", "dashed control route"),
            te("RPS-PNL-B", "RELAY-K27B", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K27B", "RELAY-K59B", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K59B", "RELAY-K81B", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K81B", "RELAY-K86B", "dashed control/trip", "dashed relay trip chain"),
            te("RELAY-K86B", "TRIP-MOD-B", "dashed control/trip", "dashed relay trip chain"),
            te("PT-401B", "JB-401B", "dotted signal", "instrument signal route"),
            te("LT-402B", "JB-401B", "dotted signal", "instrument signal route"),
            te("FT-403B", "JB-401B", "dotted signal", "instrument signal route"),
            te("JB-401B", "TB-RPS-B", "dotted signal", "signal route through terminal block"),
            te("TB-RPS-B", "RPS-PNL-B", "dotted signal", "signal route into RPS panel"),
            te("JB-401B", "GND-401B", "ground/reference", "solid ground/reference drop"),
            te("LOAD-SHED-CAB", "TDR-1", "dashed control/trip", "load-shed control route"),
            te("LOAD-SHED-CAB", "TDR-2", "dashed control/trip", "load-shed control route"),
            te("LOAD-SHED-CAB", "LAMP-ALM-A", "dotted signal", "alarm signal route"),
            te("LOAD-SHED-CAB", "LAMP-ALM-B", "dotted signal", "alarm signal route"),
            te("LOAD-SHED-CAB", "ANN-PNL-1", "dotted signal", "annunciator signal route"),
            te("ANN-PNL-1", "SEQ-REC-1", "dotted signal", "signal route to sequence recorder"),
        ]
    )
    return unique_typed_edges(edges)


FINAL_EDGES = final_edges()

UNCERTAIN_OR_REJECTED = [
    te("CB-TIE-1", "SYNC-CAB", "rejected/uncertain", "dashed route nearby, no clean terminal edge"),
    te("CB-TIE-1", "LOAD-SHED-CAB", "rejected/uncertain", "route corridor, no clean terminal edge"),
    te("SYNC-CAB", "LOAD-SHED-CAB", "rejected/uncertain", "route corridor, no clean terminal edge"),
    te("ESFAS-PNL-A", "TDR-1", "rejected/uncertain", "dashed routing but no clean endpoint"),
    te("ESFAS-PNL-B", "TDR-2", "rejected/uncertain", "dashed routing but no clean endpoint"),
    te("ESFAS-PNL-A", "LOAD-SHED-CAB", "rejected/uncertain", "dashed routing but no clean endpoint"),
    te("ESFAS-PNL-B", "LOAD-SHED-CAB", "rejected/uncertain", "dashed routing but no clean endpoint"),
    te("TRIP-MOD-A", "LOAD-SHED-CAB", "rejected/uncertain", "dashed routing but no clean endpoint"),
    te("TRIP-MOD-B", "LOAD-SHED-CAB", "rejected/uncertain", "dashed routing but no clean endpoint"),
    te("LAMP-ALM-A", "ANN-PNL-1", "rejected/uncertain", "lamp and annunciator route via load-shed/alarm bus"),
    te("LAMP-ALM-B", "ANN-PNL-1", "rejected/uncertain", "lamp and annunciator route via load-shed/alarm bus"),
    te("BUS-101A", "BUS-101B", "rejected/uncertain", "tie breaker CB-TIE-1 is the intervening component"),
]


def diego_round1_edges() -> list[TypedEdge]:
    edges: list[TypedEdge] = []
    for edge in FINAL_EDGES:
        src = edge.source.replace("EDG-1A", "DG-1A").replace("EDG-1B", "DG-1B")
        dst = edge.target.replace("EDG-1A", "DG-1A").replace("EDG-1B", "DG-1B")
        edges.append(te(src, dst, edge.edge_type, edge.evidence))
    edges.extend(
        [
            te("CB-TIE-1", "SYNC-CAB", "candidate", "Diego Round 1 route-channel candidate"),
            te("CB-TIE-1", "LOAD-SHED-CAB", "candidate", "Diego Round 1 route-channel candidate"),
            te("SYNC-CAB", "LOAD-SHED-CAB", "candidate", "Diego Round 1 route-channel candidate"),
            te("ESFAS-PNL-A", "TDR-1", "candidate", "Diego Round 1 dashed-control candidate"),
            te("ESFAS-PNL-B", "TDR-2", "candidate", "Diego Round 1 dashed-control candidate"),
            te("ESFAS-PNL-A", "LOAD-SHED-CAB", "candidate", "Diego Round 1 dashed-control candidate"),
            te("ESFAS-PNL-B", "LOAD-SHED-CAB", "candidate", "Diego Round 1 dashed-control candidate"),
            te("TRIP-MOD-A", "LOAD-SHED-CAB", "candidate", "Diego Round 1 dashed-control candidate"),
            te("TRIP-MOD-B", "LOAD-SHED-CAB", "candidate", "Diego Round 1 dashed-control candidate"),
            te("LAMP-ALM-A", "ANN-PNL-1", "candidate", "Diego Round 1 alarm-signal candidate"),
            te("LAMP-ALM-B", "ANN-PNL-1", "candidate", "Diego Round 1 alarm-signal candidate"),
        ]
    )
    return unique_typed_edges(edges)


ROUND1_NODES = [node.replace("EDG-1A", "DG-1A").replace("EDG-1B", "DG-1B") for node in NODES]


@dataclass(frozen=True)
class RoundResult:
    filename_stem: str
    agent: str
    round_label: str
    stance: str
    nodes: list[str]
    edges: list[TypedEdge]
    note: str


ROUNDS = [
    RoundResult(
        "round_01_diego",
        "Diego",
        "Round 1",
        "high-recall extractor",
        ROUND1_NODES,
        diego_round1_edges(),
        "High-recall pass used DG labels and included several route-channel/dashed candidates.",
    ),
    RoundResult(
        "round_02_jennifer",
        "Jennifer",
        "Round 1",
        "precision reviewer/refiner",
        NODES,
        FINAL_EDGES,
        "Precision pass corrected labels to EDG/PMP-LP, accepted all visually connected line types, and rejected route-channel candidates.",
    ),
    RoundResult(
        "round_03_diego",
        "Diego",
        "Round 2",
        "high-recall extractor",
        NODES,
        FINAL_EDGES,
        "Second pass agreed with Jennifer and recommended binary 1 for all accepted line types with edge_type metadata stored separately.",
    ),
    RoundResult(
        "round_04_jennifer",
        "Jennifer",
        "Round 2 final",
        "precision reviewer/refiner",
        NODES,
        FINAL_EDGES,
        "Final review confirmed all accepted line types in the binary matrix and declared saturation.",
    ),
]


def validate(nodes: list[str], edges: list[TypedEdge]) -> dict:
    duplicate_nodes = sorted({node for node in nodes if nodes.count(node) > 1})
    node_set = set(nodes)
    missing = sorted({endpoint for edge in edges for endpoint in (edge.source, edge.target) if endpoint not in node_set})
    self_edges = sorted([(edge.source, edge.target) for edge in edges if edge.source == edge.target])
    duplicate_edges = []
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        ce = canonical_edge(edge)
        if ce in seen:
            duplicate_edges.append((edge.source, edge.target))
        seen.add(ce)
    return {
        "node_count": len(nodes),
        "edge_count": len(unique_typed_edges(edges)),
        "duplicate_nodes": duplicate_nodes,
        "missing_edge_nodes": missing,
        "self_edges": self_edges,
        "duplicate_edges": duplicate_edges,
        "symmetric": True,
        "diagonal_zero": len(self_edges) == 0,
        "valid": not duplicate_nodes and not missing and not self_edges and not duplicate_edges,
    }


def make_matrix(nodes: list[str], edges: list[TypedEdge]) -> list[list[int]]:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for edge in unique_typed_edges(edges):
        ia = idx[edge.source]
        ib = idx[edge.target]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    return matrix


def write_matrix_csv(path: Path, nodes: list[str], edges: list[TypedEdge]) -> None:
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


def write_edges_csv(path: Path, edges: list[TypedEdge], include_type: bool = True) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        fields = ["source", "target"]
        if include_type:
            fields.extend(["edge_type", "evidence"])
        writer = csv.writer(f)
        writer.writerow(fields)
        for edge in unique_typed_edges(edges):
            row = [edge.source, edge.target]
            if include_type:
                row.extend([edge.edge_type, edge.evidence])
            writer.writerow(row)


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
        cached = image_tokens if self.image_context_cached else ""
        total_expected = input_expected + self.output_tokens_expected
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
            "cached_input_tokens_expected": cached,
            "output_tokens_low": self.output_tokens_low,
            "output_tokens_expected": self.output_tokens_expected,
            "output_tokens_high": self.output_tokens_high,
            "reasoning_tokens_expected": "",
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
    img("raw__top_source_bus.png"),
    img("wires_overlay__top_source_bus.png"),
    img("raw__upper_left_trains.png"),
    img("raw__upper_right_trains.png"),
    img("raw__bottom_left_controls.png"),
    img("raw__bottom_right_controls.png"),
    img("wires_overlay__bottom_band.png"),
    img("wires_mask_inv__overview_large.png"),
]

BASE_PROMPT = (
    "Inspect only Raw + wires visual resources for document 24. Extract or review the undirected "
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
        "User request plus conversation context; create crops, coordinate Diego and Jennifer, write artifacts.",
        [],
        900,
        500,
        1500,
        28000,
        False,
        "estimated; main-agent usage object is not exposed in this environment",
        "Conversation cache and reasoning-token counts are unavailable.",
    ),
    ModelCallEstimate(
        "subagent_01_diego_round1",
        DOC_ID,
        ITERATION,
        "Diego",
        "019f7687-6b5a-7af1-b3b1-2074e1ede6f3",
        "Round 1",
        "gpt-5.5",
        BASE_PROMPT + " Role: high-recall extractor. Propose all visually/geometrically plausible nodes and edges.",
        ROUND_IMAGES,
        1900,
        1300,
        3000,
        None,
        False,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Initial payload included 10 visual crops.",
    ),
    ModelCallEstimate(
        "subagent_02_jennifer_round1",
        DOC_ID,
        ITERATION,
        "Jennifer",
        "019f768a-4be4-7f11-8d9c-756f779bfe9c",
        "Round 1",
        "gpt-5.5",
        BASE_PROMPT + " Role: precision reviewer/refiner. Review Diego Round 1 and remove unsupported edges.",
        ROUND_IMAGES,
        1500,
        1000,
        2400,
        None,
        False,
        "estimated; multi-agent tool did not expose Responses usage object",
        "Payload included Diego's proposal plus the same 10 visual crops.",
    ),
    ModelCallEstimate(
        "subagent_03_diego_round2",
        DOC_ID,
        ITERATION,
        "Diego",
        "019f7687-6b5a-7af1-b3b1-2074e1ede6f3",
        "Round 2",
        "gpt-5.5",
        BASE_PROMPT + " Follow-up in same Diego thread: review Jennifer corrections and decide final binary matrix scope.",
        ROUND_IMAGES,
        320,
        180,
        650,
        None,
        True,
        "estimated; persistent subagent thread did not expose cached-token or total usage details",
        "Images were reused from Diego's existing thread; cached amount is estimated as image proxy total.",
    ),
    ModelCallEstimate(
        "subagent_04_jennifer_round2_final",
        DOC_ID,
        ITERATION,
        "Jennifer",
        "019f768a-4be4-7f11-8d9c-756f779bfe9c",
        "Round 2 final",
        "gpt-5.5",
        BASE_PROMPT + " Follow-up in same Jennifer thread: confirm final labels, matrix scope, and saturation.",
        ROUND_IMAGES,
        180,
        90,
        400,
        None,
        True,
        "estimated; persistent subagent thread did not expose cached-token or total usage details",
        "Images were reused from Jennifer's existing thread; cached amount is estimated as image proxy total.",
    ),
]


ROUND_NOTES = """# Document 24 Round Notes

## Scope
- Used only resources under `Raw + wires`.
- No ground-truth file or GT-derived feedback was used.
- No OCR engine was used. Labels were read by visual inspection.

## Diego Round 1 - High Recall
Diego identified the two-train class 1E AC/DC drawing: offsite sources, EDG/generator paths, `BUS-101A/B`, tie breaker `CB-TIE-1`, transformer feeds to `BUS-201A/B`, 18 feeder channels, and bottom DC/control/signal panels. His high-recall pass used `DG-1A/B` for the generator labels and included route-channel candidates around `SYNC-CAB`, `LOAD-SHED-CAB`, `ESFAS`, `TRIP-MOD`, and alarm signals.

## Jennifer Round 1 - Precision Refinement
Jennifer corrected generator labels to `EDG-1A/B`, confirmed `PMP-LP208A/B`, full relay labels, and accepted visually confirmed solid, dashed, and dotted connections as typed edges. She rejected route-channel candidates without clean terminal evidence and crossings without junction dots.

## Diego Round 2 - Agreement Check
Diego agreed with Jennifer's corrections and recommended that the required binary matrix set `1` for every visually accepted line type, while the edge list preserves `edge_type` metadata.

## Jennifer Round 2 - Saturated Final
Jennifer confirmed the same scope: final binary matrix includes solid power/DC, dashed control/trip, dotted signal, and ground/reference edges. Rejected or uncertain routes remain excluded. Final status: SATURATED FINAL.
"""


def write_rounds() -> dict:
    validations: dict[str, dict] = {}
    for round_result in ROUNDS:
        edges = unique_typed_edges(round_result.edges)
        stem = round_result.filename_stem
        write_matrix_csv(RESULTS_DIR / f"{stem}_matrix.csv", round_result.nodes, edges)
        write_nodes_csv(RESULTS_DIR / f"{stem}_nodes.csv", round_result.nodes)
        write_edges_csv(RESULTS_DIR / f"{stem}_edges.csv", edges, include_type=True)
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
        f.write("# Token Usage Estimate - Document 24\n\n")
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
    final = unique_typed_edges(FINAL_EDGES)
    validation = validate(NODES, final)
    write_matrix_csv(RESULTS_DIR / "connectivity_matrix_final.csv", NODES, final)
    write_nodes_csv(RESULTS_DIR / "nodes_final.csv", NODES)
    write_edges_csv(RESULTS_DIR / "edges_final.csv", final, include_type=True)
    write_edges_csv(RESULTS_DIR / "edge_types_final.csv", final, include_type=True)
    write_edges_csv(RESULTS_DIR / "connectivity_sparse_final.csv", final, include_type=False)
    write_edges_csv(RESULTS_DIR / "rejected_uncertain_edges_final.csv", UNCERTAIN_OR_REJECTED, include_type=True)
    matrix = make_matrix(NODES, final)
    isolated = sorted([node for node in NODES if all(node not in (edge.source, edge.target) for edge in final)])
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
                "edges": [edge.__dict__ for edge in final],
                "matrix": matrix,
                "validation": validation,
                "isolated_visible_nodes": isolated,
                "edge_scope": "binary 1 for every visually accepted solid power/DC, dashed control/trip, dotted signal, or ground/reference connection",
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

    for script_name in ["doc24_make_visual_crops.py", "doc24_write_results.py"]:
        source = Path(script_name).resolve()
        if source.exists() and source != CODES_DIR / source.name:
            shutil.copy2(source, CODES_DIR / source.name)

    print(json.dumps({"final": final_validation, "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
