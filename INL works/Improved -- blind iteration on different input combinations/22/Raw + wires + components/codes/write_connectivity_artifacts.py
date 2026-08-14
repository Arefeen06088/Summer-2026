from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"


TOP_NODES = [
    "GEN-G01",
    "GSU-T01",
    "SWYD-345",
    "CB-13A1",
    "BUS-13A",
    "CB-13T",
    "BUS-13B",
    "CB-13B1",
    "AUX-XFMR-1A",
    "AUX-XFMR-1B",
    "SAT-XFMR-1C",
    "SAT-XFMR-1D",
    "CB-4A-IN",
    "CB-4B-IN",
    "CB-4C-IN",
    "CB-4D-IN",
    "DG-1A",
    "DG-1B",
    "DG-1C",
    "DG-1D",
    "CB-DG-A",
    "CB-DG-B",
    "CB-DG-C",
    "CB-DG-D",
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-4160-C",
    "BUS-4160-D",
    "CB-4AB-TIE",
    "CB-4CD-TIE",
    "SYNC-PNL-1",
    "RELAY-87U",
    "CB-LC-A",
    "CB-LC-B",
    "CB-LC-C",
    "CB-LC-D",
    "TR-LC-A",
    "TR-LC-B",
    "TR-LC-C",
    "TR-LC-D",
]


def train_nodes(suffix: str) -> list[str]:
    first_mcc = f"MCC-{suffix}A"
    second_mcc = f"MCC-{suffix}B"
    return [
        f"BUS-480-{suffix}",
        f"INST-PT-{suffix}",
        f"CB-MCC-{suffix}A",
        f"CB-MCC-{suffix}B",
        first_mcc,
        second_mcc,
        f"INST-CT-{suffix}",
        f"CB-RHR-{suffix}",
        f"CB-SI-{suffix}",
        f"CB-CCW-{suffix}",
        f"CB-FAN-{suffix}",
        f"CB-CH-{suffix}",
        f"CB-VLV1-{suffix}",
        f"CB-VLV2-{suffix}",
        f"CB-SPARE-{suffix}",
        f"PUMP-RHR-{suffix}",
        f"PUMP-SI-{suffix}",
        f"PUMP-CCW-{suffix}",
        f"FAN-CR-{suffix}",
        f"CHILLER-{suffix}",
        f"MOV-HV1-{suffix}",
        f"MOV-HV2-{suffix}",
        f"SPARE-LOAD-{suffix}",
        f"XFMR-120-{suffix}",
        f"PNL-120-{suffix}",
        f"RELAY-K{suffix}1",
        f"RELAY-K{suffix}2",
        f"JB-{suffix}1",
        f"TERM-{suffix}",
        f"GND-{suffix}",
    ]


UPS_NODES = [
    "CB-DC-A1",
    "CHGR-125A",
    "BUS-125A",
    "BAT-125A",
    "FUSE-FD-A",
    "INV-UPS-A",
    "DC-MCC-A",
    "SOL-SDV-A",
    "DIODE-OR-A",
    "GRD-DC-A",
    "BUS-UPS-A",
    "PNL-RPS-A",
    "RELAY-RPS-A1",
    "RELAY-ESF-A",
    "PLC-SAF-A",
    "INST-RACK-A",
    "ANN-PNL-CR",
    "JB-CR-01",
    "TERM-MTB-A",
    "TERM-MTB-B",
    "DIODE-OR-B",
    "CB-DC-B1",
    "CHGR-125B",
    "BUS-125B",
    "BAT-125B",
    "FUSE-FD-B",
    "INV-UPS-B",
    "DC-MCC-B",
    "SOL-SDV-B",
    "GRD-DC-B",
    "BUS-UPS-B",
    "PNL-RPS-B",
    "RELAY-RPS-B1",
    "RELAY-ESF-B",
    "PLC-SAF-B",
    "INST-RACK-B",
    "REC-SEQ-1",
    "XFMR-PT-1",
    "METER-V01",
    "METER-A01",
]


NODES = TOP_NODES + train_nodes("A") + train_nodes("B") + train_nodes("C") + train_nodes("D") + UPS_NODES


def pair(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop not expected: {a}")
    return tuple(sorted((a, b)))


def edge_set(edges: Iterable[tuple[str, str]]) -> set[tuple[str, str]]:
    return {pair(a, b) for a, b in edges}


def top_edges(include_bus_87u: bool) -> set[tuple[str, str]]:
    edges = [
        ("GEN-G01", "GSU-T01"),
        ("GSU-T01", "SWYD-345"),
        ("SWYD-345", "CB-13A1"),
        ("SWYD-345", "CB-13B1"),
        ("CB-13A1", "BUS-13A"),
        ("BUS-13A", "CB-13T"),
        ("CB-13T", "BUS-13B"),
        ("CB-13B1", "BUS-13B"),
        ("BUS-13A", "AUX-XFMR-1A"),
        ("AUX-XFMR-1A", "CB-4A-IN"),
        ("CB-4A-IN", "BUS-4160-A"),
        ("BUS-13A", "AUX-XFMR-1B"),
        ("AUX-XFMR-1B", "CB-4B-IN"),
        ("CB-4B-IN", "BUS-4160-B"),
        ("BUS-13B", "SAT-XFMR-1C"),
        ("SAT-XFMR-1C", "CB-4C-IN"),
        ("CB-4C-IN", "BUS-4160-C"),
        ("BUS-13B", "SAT-XFMR-1D"),
        ("SAT-XFMR-1D", "CB-4D-IN"),
        ("CB-4D-IN", "BUS-4160-D"),
        ("DG-1A", "CB-DG-A"),
        ("CB-DG-A", "BUS-4160-A"),
        ("DG-1B", "CB-DG-B"),
        ("CB-DG-B", "BUS-4160-B"),
        ("DG-1C", "CB-DG-C"),
        ("CB-DG-C", "BUS-4160-C"),
        ("DG-1D", "CB-DG-D"),
        ("CB-DG-D", "BUS-4160-D"),
        ("BUS-4160-A", "CB-4AB-TIE"),
        ("CB-4AB-TIE", "BUS-4160-B"),
        ("BUS-4160-C", "CB-4CD-TIE"),
        ("CB-4CD-TIE", "BUS-4160-D"),
        ("BUS-4160-A", "CB-LC-A"),
        ("CB-LC-A", "TR-LC-A"),
        ("BUS-4160-B", "CB-LC-B"),
        ("CB-LC-B", "TR-LC-B"),
        ("BUS-4160-C", "CB-LC-C"),
        ("CB-LC-C", "TR-LC-C"),
        ("BUS-4160-D", "CB-LC-D"),
        ("CB-LC-D", "TR-LC-D"),
        ("SYNC-PNL-1", "CB-DG-A"),
        ("RELAY-87U", "CB-4B-IN"),
    ]
    if include_bus_87u:
        edges.append(("BUS-13A", "RELAY-87U"))
    return edge_set(edges)


def train_edges_final(suffix: str) -> set[tuple[str, str]]:
    mcc_a = f"MCC-{suffix}A"
    mcc_b = f"MCC-{suffix}B"
    return edge_set(
        [
            (f"TR-LC-{suffix}", f"BUS-480-{suffix}"),
            (f"BUS-480-{suffix}", f"INST-PT-{suffix}"),
            (f"BUS-480-{suffix}", f"CB-MCC-{suffix}A"),
            (f"CB-MCC-{suffix}A", mcc_a),
            (f"BUS-480-{suffix}", f"CB-MCC-{suffix}B"),
            (f"CB-MCC-{suffix}B", mcc_b),
            (mcc_a, f"INST-CT-{suffix}"),
            (f"INST-CT-{suffix}", f"CB-RHR-{suffix}"),
            (f"CB-RHR-{suffix}", f"PUMP-RHR-{suffix}"),
            (mcc_a, f"CB-SI-{suffix}"),
            (f"CB-SI-{suffix}", f"PUMP-SI-{suffix}"),
            (mcc_a, f"CB-CCW-{suffix}"),
            (f"CB-CCW-{suffix}", f"PUMP-CCW-{suffix}"),
            (mcc_a, f"CB-FAN-{suffix}"),
            (f"CB-FAN-{suffix}", f"FAN-CR-{suffix}"),
            (mcc_b, f"CB-CH-{suffix}"),
            (f"CB-CH-{suffix}", f"CHILLER-{suffix}"),
            (mcc_b, f"CB-VLV1-{suffix}"),
            (f"CB-VLV1-{suffix}", f"MOV-HV1-{suffix}"),
            (mcc_b, f"CB-VLV2-{suffix}"),
            (f"CB-VLV2-{suffix}", f"MOV-HV2-{suffix}"),
            (mcc_b, f"CB-SPARE-{suffix}"),
            (f"CB-SPARE-{suffix}", f"SPARE-LOAD-{suffix}"),
            (f"BUS-480-{suffix}", f"XFMR-120-{suffix}"),
            (f"XFMR-120-{suffix}", f"PNL-120-{suffix}"),
            (f"PNL-120-{suffix}", f"RELAY-K{suffix}1"),
            (f"PNL-120-{suffix}", f"RELAY-K{suffix}2"),
            (f"PNL-120-{suffix}", f"JB-{suffix}1"),
            (f"JB-{suffix}1", f"TERM-{suffix}"),
            (f"BUS-480-{suffix}", f"GND-{suffix}"),
        ]
    )


def train_edges_diego_r1(suffix: str) -> set[tuple[str, str]]:
    mcc_a = f"MCC-{suffix}A"
    mcc_b = f"MCC-{suffix}B"
    return edge_set(
        [
            (f"TR-LC-{suffix}", f"BUS-480-{suffix}"),
            (f"BUS-480-{suffix}", f"INST-PT-{suffix}"),
            (f"BUS-480-{suffix}", f"CB-MCC-{suffix}A"),
            (f"CB-MCC-{suffix}A", mcc_a),
            (f"BUS-480-{suffix}", f"CB-MCC-{suffix}B"),
            (f"CB-MCC-{suffix}B", mcc_b),
            (mcc_a, f"CB-RHR-{suffix}"),
            (f"CB-RHR-{suffix}", f"PUMP-RHR-{suffix}"),
            (mcc_a, f"CB-SI-{suffix}"),
            (f"CB-SI-{suffix}", f"PUMP-SI-{suffix}"),
            (mcc_a, f"CB-CCW-{suffix}"),
            (f"CB-CCW-{suffix}", f"PUMP-CCW-{suffix}"),
            (mcc_a, f"CB-FAN-{suffix}"),
            (f"CB-FAN-{suffix}", f"FAN-CR-{suffix}"),
            (mcc_b, f"CB-CH-{suffix}"),
            (f"CB-CH-{suffix}", f"CHILLER-{suffix}"),
            (mcc_b, f"CB-VLV1-{suffix}"),
            (f"CB-VLV1-{suffix}", f"MOV-HV1-{suffix}"),
            (mcc_b, f"CB-VLV2-{suffix}"),
            (f"CB-VLV2-{suffix}", f"MOV-HV2-{suffix}"),
            (mcc_b, f"CB-SPARE-{suffix}"),
            (f"CB-SPARE-{suffix}", f"SPARE-LOAD-{suffix}"),
            (f"BUS-480-{suffix}", f"XFMR-120-{suffix}"),
            (f"XFMR-120-{suffix}", f"PNL-120-{suffix}"),
            (f"PNL-120-{suffix}", f"RELAY-K{suffix}1"),
            (f"PNL-120-{suffix}", f"RELAY-K{suffix}2"),
            (f"RELAY-K{suffix}1", f"JB-{suffix}1"),
            (f"JB-{suffix}1", f"TERM-{suffix}"),
            (f"BUS-480-{suffix}", f"GND-{suffix}"),
            (f"CB-RHR-{suffix}", f"CB-SI-{suffix}"),
        ]
    )


def ups_edges_final() -> set[tuple[str, str]]:
    return edge_set(
        [
            ("CB-DC-A1", "CHGR-125A"),
            ("CHGR-125A", "BUS-125A"),
            ("BUS-125A", "BAT-125A"),
            ("BUS-125A", "FUSE-FD-A"),
            ("FUSE-FD-A", "INV-UPS-A"),
            ("INV-UPS-A", "BUS-UPS-A"),
            ("BUS-125A", "DC-MCC-A"),
            ("BUS-125A", "GRD-DC-A"),
            ("DC-MCC-A", "SOL-SDV-A"),
            ("BUS-UPS-A", "PNL-RPS-A"),
            ("PNL-RPS-A", "RELAY-RPS-A1"),
            ("PNL-RPS-A", "RELAY-ESF-A"),
            ("BUS-UPS-A", "PLC-SAF-A"),
            ("BUS-UPS-A", "INST-RACK-A"),
            ("BUS-UPS-A", "ANN-PNL-CR"),
            ("ANN-PNL-CR", "JB-CR-01"),
            ("JB-CR-01", "TERM-MTB-A"),
            ("JB-CR-01", "TERM-MTB-B"),
            ("CB-DC-B1", "CHGR-125B"),
            ("CHGR-125B", "BUS-125B"),
            ("BUS-125B", "BAT-125B"),
            ("BUS-125B", "FUSE-FD-B"),
            ("FUSE-FD-B", "INV-UPS-B"),
            ("INV-UPS-B", "BUS-UPS-B"),
            ("BUS-125B", "DC-MCC-B"),
            ("BUS-125B", "GRD-DC-B"),
            ("DC-MCC-B", "SOL-SDV-B"),
            ("BUS-UPS-B", "PNL-RPS-B"),
            ("PNL-RPS-B", "RELAY-RPS-B1"),
            ("PNL-RPS-B", "RELAY-ESF-B"),
            ("BUS-UPS-B", "PLC-SAF-B"),
            ("BUS-UPS-B", "INST-RACK-B"),
            ("BUS-UPS-B", "REC-SEQ-1"),
            ("XFMR-PT-1", "METER-V01"),
            ("XFMR-PT-1", "METER-A01"),
        ]
    )


def ups_edges_diego_r1() -> set[tuple[str, str]]:
    return ups_edges_final() | edge_set(
        [
            ("SOL-SDV-A", "DIODE-OR-A"),
            ("DIODE-OR-B", "CB-DC-B1"),
        ]
    )


FINAL_EDGES = top_edges(include_bus_87u=True) | ups_edges_final()
for train in "ABCD":
    FINAL_EDGES |= train_edges_final(train)

DIEGO_R1_EDGES = top_edges(include_bus_87u=False) | ups_edges_diego_r1()
for train in "ABCD":
    DIEGO_R1_EDGES |= train_edges_diego_r1(train)

JENNIFER_R1_EDGES = FINAL_EDGES
DIEGO_R2_EDGES = FINAL_EDGES
JENNIFER_R2_EDGES = FINAL_EDGES


ROUND_DEFS = [
    ("round_01_diego", "Diego", "high-recall extraction", DIEGO_R1_EDGES),
    ("round_02_jennifer", "Jennifer", "precision refinement", JENNIFER_R1_EDGES),
    ("round_03_diego", "Diego", "acceptance after precision review", DIEGO_R2_EDGES),
    ("round_04_jennifer", "Jennifer", "final confirmation", JENNIFER_R2_EDGES),
]


UNCERTAIN_EDGES = [
    {
        "edge": ["CB-RHR-X", "CB-SI-X"],
        "reason": "for X=A/B/C/D, dashed line near the two breakers is not a clear breaker-to-breaker termination",
    },
    {
        "edge": ["MCC-XA", "CB-RHR-X"],
        "reason": "for X=A/B/C/D, precision review supports the CT path MCC-XA--INST-CT-X--CB-RHR-X instead of a direct RHR feeder edge",
    },
    {
        "edge": ["RELAY-KX1", "JB-X1"],
        "reason": "for X=A/B/C/D, visible dashed run to JB-X1 appears to originate at PNL-120-X rather than through RELAY-KX1",
    },
    {
        "edge": ["CB-SI-X or PUMP-SI-X", "relay/control area"],
        "reason": "dashed vertical path is suggestive but lacks a clear named termination",
    },
    {
        "edge": ["RELAY-KX1", "RELAY-KX2"],
        "reason": "nearby dashed geometry may be passing control routing rather than relay-to-relay connection",
    },
    {
        "edge": ["SOL-SDV-A", "DIODE-OR-A"],
        "reason": "diode symbol/label is visible but raw crop does not show a clean component termination suitable for a supported matrix edge",
    },
    {
        "edge": ["SOL-SDV-B", "DIODE-OR-B"],
        "reason": "same ambiguity as DIODE-OR-A; retained as visible node but without supported edge",
    },
    {
        "edge": ["DIODE-OR-A", "DIODE-OR-B"],
        "reason": "possible diode-OR relation is not cleanly continuous in the raw crop",
    },
    {
        "edge": ["DIODE-OR-B", "CB-DC-B1"],
        "reason": "left side of CB-DC-B1 has an incoming conductor, but the diode-to-breaker pairing is not a clean named termination",
    },
    {
        "edge": ["CB-13T or BUS-13B", "RELAY-87U"],
        "reason": "visible dashed branch comes from the BUS-13A side; RELAY-87U-to-CB-4B-IN is separately supported",
    },
    {
        "edge": ["meter upstream trunk", "XFMR-PT-1/METER-A01"],
        "reason": "only XFMR-PT-1--METER-V01 and XFMR-PT-1--METER-A01 are supported; upstream trunk is unnamed/unclear",
    },
]


@dataclass(frozen=True)
class TokenCall:
    call_id: str
    document: int
    iteration: int
    actor: str
    round_name: str
    model_call: str
    text_prompt_tokens: int
    image_file_tokens: int
    cached_input_tokens: str
    output_tokens: int
    reasoning_tokens: str
    notes: str

    @property
    def input_tokens(self) -> int:
        return self.text_prompt_tokens + self.image_file_tokens

    @property
    def expected_total(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def low_total(self) -> int:
        return math.ceil(self.expected_total * 0.8)

    @property
    def high_total(self) -> int:
        return math.ceil(self.expected_total * 1.25)


def estimate_text_tokens(text: str) -> int:
    return math.ceil(len(text) / 4)


def estimate_image_tokens(path: Path) -> int:
    # Transparent local fallback for high-detail vision payloads. This is not
    # the OpenAI billing counter, but tracks the documented tile-style behavior
    # closely enough for planning when no API key/counting endpoint is available.
    with Image.open(path) as img:
        w, h = img.size
    scale = min(2048 / max(w, h), 1.0)
    w = int(math.ceil(w * scale))
    h = int(math.ceil(h * scale))
    short = min(w, h)
    if short > 768:
        scale = 768 / short
        w = int(math.ceil(w * scale))
        h = int(math.ceil(h * scale))
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


DIEGO_R1_IMAGES = [
    "raw_full_thumb.png",
    "doc22_full_power_top_raw.png",
    "doc22_full_power_top_wires_overlay.png",
    "doc22_train_a_all_raw.png",
    "doc22_train_b_all_raw.png",
    "doc22_train_c_all_raw.png",
    "doc22_train_d_all_raw.png",
    "doc22_bottom_ups_all_raw.png",
    "doc22_bottom_ups_all_wires_overlay.png",
    "doc22_meter_area_raw.png",
]

JENNIFER_R1_IMAGES = [
    "doc22_full_power_top_raw.png",
    "doc22_full_power_top_wires_overlay.png",
    "doc22_4160_buses_all_raw.png",
    "doc22_train_a_all_raw.png",
    "doc22_train_b_all_raw.png",
    "doc22_train_c_all_raw.png",
    "doc22_train_d_all_raw.png",
    "doc22_bottom_ups_all_raw.png",
    "doc22_bottom_ups_all_wires_overlay.png",
    "doc22_meter_area_raw.png",
]

MAIN_VIEWED_IMAGES = [
    "raw_full_thumb.png",
    "components_full_thumb.png",
    "wires_overlay_full_thumb.png",
    "notes_legend_raw.png",
    "doc22_full_power_top_raw.png",
    "doc22_source_and_aux_bus_raw.png",
    "doc22_4160_buses_all_raw.png",
    "doc22_train_a_all_raw.png",
    "doc22_train_b_all_raw.png",
    "doc22_train_c_all_raw.png",
    "doc22_train_d_all_raw.png",
    "doc22_bottom_ups_all_raw.png",
    "doc22_bottom_ups_left_a_raw.png",
    "doc22_bottom_ups_right_b_raw.png",
    "doc22_bottom_control_center_raw.png",
    "doc22_meter_area_raw.png",
    "doc22_full_power_top_wires_overlay.png",
    "doc22_4160_buses_all_wires_overlay.png",
    "doc22_bottom_ups_all_wires_overlay.png",
    "doc22_train_a_all_wires_overlay.png",
    "doc22_source_and_aux_bus_wires_overlay.png",
    "top_left_aux_sources_raw.png",
    "top_left_aux_sources_wires_overlay.png",
    "top_center_416_buses_raw.png",
    "top_center_416_buses_wires_overlay.png",
    "top_edg_feeders_detail_raw.png",
    "top_edg_feeders_detail_wires_overlay.png",
    "feeders_416_to_480_raw.png",
    "feeders_416_to_480_wires_overlay.png",
    "doc22_zoom_sync_panel_raw.png",
    "doc22_zoom_sync_panel_overlay.png",
    "doc22_zoom_diodes_raw.png",
    "doc22_zoom_diodes_overlay.png",
]


def images_tokens(names: list[str]) -> int:
    return sum(estimate_image_tokens(CROPS_DIR / name) for name in names if (CROPS_DIR / name).exists())


def token_calls() -> list[TokenCall]:
    diego_r1_prompt = (
        "Diego high-recall visual extraction prompt with raw/overlay crops, no GT/OCR, "
        "requesting node list, supported edges, uncertain edges, and evidence."
    )
    jennifer_r1_prompt = (
        "Jennifer precision review prompt plus Diego R1 proposal, no GT/OCR, "
        "requesting corrected nodes, supported edges, uncertain omissions, and agreement notes."
    )
    diego_r2_prompt = (
        "Diego round 2 prompt with Jennifer R1 corrections, asking acceptance or edge changes "
        "for disputed CT, relay, diode, and RELAY-87U areas."
    )
    jennifer_r2_prompt = (
        "Jennifer final confirmation prompt with Diego R2 acceptance, asking whether final matrix "
        "is exactly Jennifer R1 and to restate uncertain omissions."
    )
    return [
        TokenCall(
            call_id="doc22-main-aggregate",
            document=22,
            iteration=1,
            actor="Main agent",
            round_name="orchestration",
            model_call="aggregate local visual inspection, agent coordination, artifact writing",
            text_prompt_tokens=estimate_text_tokens("doc22 user instructions and main-agent working notes") + 3500,
            image_file_tokens=images_tokens(MAIN_VIEWED_IMAGES),
            cached_input_tokens="unavailable",
            output_tokens=3000,
            reasoning_tokens="unavailable",
            notes="aggregate estimate; exact internal main-agent calls/usage are not exposed in this local session",
        ),
        TokenCall(
            call_id="doc22-r1-diego",
            document=22,
            iteration=1,
            actor="Diego",
            round_name="round_01_diego",
            model_call="spawn_agent high-recall extraction",
            text_prompt_tokens=estimate_text_tokens(diego_r1_prompt),
            image_file_tokens=images_tokens(DIEGO_R1_IMAGES),
            cached_input_tokens="unavailable",
            output_tokens=4300,
            reasoning_tokens="unavailable",
            notes="actual usage object not exposed by subagent tool; output estimated from returned text length",
        ),
        TokenCall(
            call_id="doc22-r2-jennifer",
            document=22,
            iteration=1,
            actor="Jennifer",
            round_name="round_02_jennifer",
            model_call="spawn_agent precision review",
            text_prompt_tokens=estimate_text_tokens(jennifer_r1_prompt) + 3600,
            image_file_tokens=images_tokens(JENNIFER_R1_IMAGES),
            cached_input_tokens="unavailable",
            output_tokens=3300,
            reasoning_tokens="unavailable",
            notes="actual usage object not exposed by subagent tool; includes Diego R1 proposal in prompt",
        ),
        TokenCall(
            call_id="doc22-r3-diego",
            document=22,
            iteration=1,
            actor="Diego",
            round_name="round_03_diego",
            model_call="send_input acceptance/refinement",
            text_prompt_tokens=estimate_text_tokens(diego_r2_prompt) + 1300,
            image_file_tokens=0,
            cached_input_tokens="unavailable",
            output_tokens=500,
            reasoning_tokens="unavailable",
            notes="incremental text-only follow-up; prior visual context may be cached by service but amount is unavailable",
        ),
        TokenCall(
            call_id="doc22-r4-jennifer",
            document=22,
            iteration=1,
            actor="Jennifer",
            round_name="round_04_jennifer",
            model_call="send_input final confirmation",
            text_prompt_tokens=estimate_text_tokens(jennifer_r2_prompt) + 350,
            image_file_tokens=0,
            cached_input_tokens="unavailable",
            output_tokens=350,
            reasoning_tokens="unavailable",
            notes="incremental text-only final confirmation; exact response usage unavailable",
        ),
    ]


def validate_edges(edges: set[tuple[str, str]]) -> list[str]:
    node_set = set(NODES)
    issues: list[str] = []
    for a, b in sorted(edges):
        if a not in node_set:
            issues.append(f"unknown node in edge: {a}")
        if b not in node_set:
            issues.append(f"unknown node in edge: {b}")
        if a == b:
            issues.append(f"self-loop: {a}")
    return issues


def write_matrix(prefix: str, edges: set[tuple[str, str]]) -> None:
    matrix_path = RESULTS_DIR / f"{prefix}_connectivity_matrix.csv"
    sparse_path = RESULTS_DIR / f"{prefix}_edges.csv"
    json_path = RESULTS_DIR / f"{prefix}_edges.json"
    edge_lookup = set(edges)

    with matrix_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([""] + NODES)
        for row_node in NODES:
            row = [row_node]
            for col_node in NODES:
                row.append(0 if row_node == col_node else int(pair(row_node, col_node) in edge_lookup))
            writer.writerow(row)

    with sparse_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["source", "target"])
        for a, b in sorted(edges):
            writer.writerow([a, b])

    json_path.write_text(
        json.dumps(
            {
                "nodes": NODES,
                "edges": [list(edge) for edge in sorted(edges)],
                "edge_count": len(edges),
                "node_count": len(NODES),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def write_reports() -> None:
    summary_lines = [
        "# Document 22 Connectivity Extraction",
        "",
        "Raw/derived visual resources only; no GT or GT-derived feedback used. No OCR tools used.",
        "",
        "## Rounds",
        "",
    ]
    for prefix, actor, role, edges in ROUND_DEFS:
        summary_lines.append(f"- `{prefix}` ({actor}, {role}): {len(NODES)} nodes, {len(edges)} supported edges.")
    summary_lines.extend(
        [
            "",
            "## Saturation",
            "",
            "Jennifer R1 corrected Diego R1. Diego R2 accepted Jennifer R1 with no additions/removals. "
            "Jennifer R2 confirmed that the final supported matrix is exactly Jennifer R1.",
            "",
            "## Final Matrix",
            "",
            "- `final_connectivity_matrix.csv` is copied from `round_04_jennifer_connectivity_matrix.csv`.",
            "- `final_edges.csv` is copied from `round_04_jennifer_edges.csv`.",
            "",
            "## Isolated Visible Nodes",
            "",
            "- `DIODE-OR-A` and `DIODE-OR-B` are kept as visible component nodes, but no supported edge was added.",
        ]
    )
    (RESULTS_DIR / "round_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    uncertain_lines = ["# Document 22 Uncertain/Omitted Edges", ""]
    for item in UNCERTAIN_EDGES:
        uncertain_lines.append(f"- {item['edge']}: {item['reason']}")
    (RESULTS_DIR / "uncertain_edges.md").write_text("\n".join(uncertain_lines) + "\n", encoding="utf-8")
    (RESULTS_DIR / "uncertain_edges.json").write_text(json.dumps(UNCERTAIN_EDGES, indent=2), encoding="utf-8")


def write_token_usage() -> None:
    calls = token_calls()
    csv_path = RESULTS_DIR / "token_usage_estimates.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "document",
                "iteration",
                "call_id",
                "actor",
                "round",
                "model_call",
                "input_tokens_est",
                "cached_input_tokens",
                "output_tokens_est",
                "reasoning_tokens",
                "image_file_input_tokens_est",
                "low_total_est",
                "expected_total_est",
                "high_total_est",
                "notes",
            ]
        )
        for call in calls:
            writer.writerow(
                [
                    call.document,
                    call.iteration,
                    call.call_id,
                    call.actor,
                    call.round_name,
                    call.model_call,
                    call.input_tokens,
                    call.cached_input_tokens,
                    call.output_tokens,
                    call.reasoning_tokens,
                    call.image_file_tokens,
                    call.low_total,
                    call.expected_total,
                    call.high_total,
                    call.notes,
                ]
            )

    totals = {
        "document": 22,
        "iteration": 1,
        "input_tokens_est": sum(call.input_tokens for call in calls),
        "image_file_input_tokens_est": sum(call.image_file_tokens for call in calls),
        "output_tokens_est": sum(call.output_tokens for call in calls),
        "low_total_est": sum(call.low_total for call in calls),
        "expected_total_est": sum(call.expected_total for call in calls),
        "high_total_est": sum(call.high_total for call in calls),
        "method": "local heuristic: text chars/4 plus high-detail image tile estimate; Responses token-counting endpoint unavailable without API key",
    }
    (RESULTS_DIR / "token_usage_estimates.json").write_text(
        json.dumps({"calls": [call.__dict__ | {"input_tokens": call.input_tokens} for call in calls], "totals": totals}, indent=2),
        encoding="utf-8",
    )
    md_lines = [
        "# Token Usage Estimates",
        "",
        "OpenAI Responses input-token counting endpoint was not called because no API key is available.",
        "The local estimate uses text characters / 4 plus a high-detail image tile estimate from image dimensions.",
        "Actual cached input tokens, usage objects, and reasoning tokens were not exposed by the local subagent tools.",
        "",
        "| Document | Iteration | Call | Actor | Input Est | Image/File Est | Output Est | Low | Expected | High |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for call in calls:
        md_lines.append(
            f"| {call.document} | {call.iteration} | {call.call_id} | {call.actor} | "
            f"{call.input_tokens} | {call.image_file_tokens} | {call.output_tokens} | "
            f"{call.low_total} | {call.expected_total} | {call.high_total} |"
        )
    md_lines.append(
        f"| 22 | 1 | TOTAL | all | {totals['input_tokens_est']} | {totals['image_file_input_tokens_est']} | "
        f"{totals['output_tokens_est']} | {totals['low_total_est']} | {totals['expected_total_est']} | {totals['high_total_est']} |"
    )
    (RESULTS_DIR / "token_usage_estimates.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    validation_issues: list[str] = []
    if len(NODES) != len(set(NODES)):
        seen: set[str] = set()
        duplicates = []
        for node in NODES:
            if node in seen:
                duplicates.append(node)
            seen.add(node)
        validation_issues.append(f"duplicate nodes: {duplicates}")

    for prefix, _actor, _role, edges in ROUND_DEFS:
        validation_issues.extend(f"{prefix}: {issue}" for issue in validate_edges(edges))
        write_matrix(prefix, edges)

    write_matrix("final", FINAL_EDGES)
    write_reports()
    write_token_usage()

    degrees = {node: 0 for node in NODES}
    for a, b in FINAL_EDGES:
        degrees[a] += 1
        degrees[b] += 1
    isolated = [node for node, degree in degrees.items() if degree == 0]
    validation_lines = [
        "Document 22 validation report",
        f"nodes: {len(NODES)}",
        f"final_edges: {len(FINAL_EDGES)}",
        f"rounds: {len(ROUND_DEFS)}",
        f"isolated_final_nodes: {', '.join(isolated) if isolated else 'none'}",
        f"issues: {len(validation_issues)}",
    ]
    validation_lines.extend(validation_issues)
    (RESULTS_DIR / "validation_report.txt").write_text("\n".join(validation_lines) + "\n", encoding="utf-8")
    if validation_issues:
        raise SystemExit("\n".join(validation_issues))


if __name__ == "__main__":
    main()
