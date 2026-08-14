from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + wires"
)
RESULTS = ROOT / "results"


def text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def high_detail_image_tokens(path: Path) -> tuple[int, int, int, int]:
    """Approximate OpenAI high-detail image token accounting.

    This mirrors the public 85 + 170-per-512px-tile heuristic used by
    high-detail vision models. It is an estimate, not a billing record.
    """
    with Image.open(path) as image:
        width, height = image.size

    scale = min(2048 / width, 2048 / height, 1.0)
    resized_w = width * scale
    resized_h = height * scale
    shortest = min(resized_w, resized_h)
    if shortest > 768:
        scale2 = 768 / shortest
        resized_w *= scale2
        resized_h *= scale2

    tiles_w = math.ceil(resized_w / 512)
    tiles_h = math.ceil(resized_h / 512)
    tiles = tiles_w * tiles_h
    tokens = 85 + 170 * tiles
    return tokens, width, height, tiles


@dataclass(frozen=True)
class CallEstimate:
    document: str
    iteration: str
    round_name: str
    call_id: str
    agent: str
    model: str
    reasoning_effort: str
    prompt_summary: str
    text_payload: str
    image_paths: tuple[Path, ...]
    output_low: int
    output_expected: int
    output_high: int
    reasoning_low: int
    reasoning_expected: int
    reasoning_high: int

    def row(self) -> dict[str, object]:
        text_input = text_tokens(self.text_payload)
        image_details = [high_detail_image_tokens(path) for path in self.image_paths]
        image_tokens = sum(item[0] for item in image_details)
        input_expected = text_input + image_tokens
        return {
            "document": self.document,
            "iteration": self.iteration,
            "round": self.round_name,
            "call_id": self.call_id,
            "agent": self.agent,
            "model": self.model,
            "reasoning_effort": self.reasoning_effort,
            "prompt_summary": self.prompt_summary,
            "usage_object_available": "no",
            "responses_count_endpoint_used": "no_openai_api_key",
            "cached_input_tokens_recorded": "",
            "input_text_tokens_est": text_input,
            "image_file_input_tokens_est": image_tokens,
            "file_input_tokens_est": 0,
            "input_tokens_expected": input_expected,
            "input_tokens_low": math.ceil(input_expected * 0.88),
            "input_tokens_high": math.ceil(input_expected * 1.18),
            "output_tokens_low": self.output_low,
            "output_tokens_expected": self.output_expected,
            "output_tokens_high": self.output_high,
            "reasoning_tokens_low": self.reasoning_low,
            "reasoning_tokens_expected": self.reasoning_expected,
            "reasoning_tokens_high": self.reasoning_high,
            "total_tokens_low": math.ceil(input_expected * 0.88)
            + self.output_low
            + self.reasoning_low,
            "total_tokens_expected": input_expected
            + self.output_expected
            + self.reasoning_expected,
            "total_tokens_high": math.ceil(input_expected * 1.18)
            + self.output_high
            + self.reasoning_high,
            "image_count": len(self.image_paths),
            "image_names": "; ".join(path.name for path in self.image_paths),
        }


def p(name: str) -> Path:
    return ROOT / name


def c(name: str) -> Path:
    return ROOT / "results" / "crops" / name


RAW = p("raw -- synthetic_npp_electrical_schematic_clean (1).png")
MASK = p("wires_mask.png")
OVERLAY = p("wires_mask_overlay.png")

COMMON_TASK = """
Extract document 7 connectivity matrix from Raw + wires only. No ground truth,
no GT-derived feedback, no OCR engines. Rows and columns use the same component
order, undirected symmetric matrix, diagonal zero unless a self-loop is justified.
"""

DIEGO_R1_TEXT = COMMON_TASK + """
Diego round 1 high-recall extraction. Inspect full raw schematic, wires mask, and
wire overlay. Propose all visually/geometrically plausible components, labels,
logical nodes, and edges with evidence. Prefer recall for visually plausible
connections, but flag uncertainty.
"""

JENNIFER_R1_TEXT = COMMON_TASK + """
Jennifer round 1 precision review. Inspect Diego R1 node/edge proposal and the
full image plus regional crops. Remove unsupported or overconnected edges, fix
labels where visually supported, and mark ambiguous cases uncertain instead of
guessing. Focus on station transformer routing, bottom DC/control panels, relay
links, PPS/PNL/bus crossings, and raceway controls.
"""

DIEGO_R2_TEXT = COMMON_TASK + """
Diego round 2 targeted adjudication. Recheck Jennifer R1 changes only: DS-SAT-1
to TR-SAT-B, RELAY-K202 to SR-101, BUS-125DC* to PNL-AC-CR*, and whether any
additional named bottom dashed control edges are uniquely resolved. Return delta
or accept Jennifer R1.
"""

JENNIFER_R2_TEXT = COMMON_TASK + """
Jennifer round 2 final precision pass. Inspect Diego R2 verdict and the added
SR-to-B-relay crop. Decide whether RELAY-K202--SR-101 or DS-SAT-1--TR-SAT-B is
supported, check for any missed unambiguous named-device bottom edges, and state
final saturation status.
"""

DIEGO_R3_TEXT = COMMON_TASK + """
Diego round 3 saturation check. Inspect Jennifer R2's final delta accepting
RELAY-K202--SR-101, recheck DS-SAT-1--TR-SAT-B, review the 120-node/127-edge
named-node matrix against the raw revision note as sanity text only, and state
whether the matrix is saturated.
"""

MAIN_TEXT = COMMON_TASK + """
Main Codex orchestration for document 7. Inventory local files, generate crops,
spawn Diego/Jennifer subagents, inspect crops, reconcile round outputs, write
CSV matrices/edge lists/QA summaries, and estimate token usage. This row is an
aggregate estimate because individual main-agent runtime usage objects are not
exposed in this environment.
"""

CALLS = [
    CallEstimate(
        document="7",
        iteration="1",
        round_name="main",
        call_id="main_agent_orchestration_aggregate",
        agent="main",
        model="gpt-5-codex",
        reasoning_effort="not_exposed",
        prompt_summary="Aggregate main-agent orchestration, local image inspections, and final reporting.",
        text_payload=MAIN_TEXT * 5,
        image_paths=(
            c("raw_02_top_center_bus_ties.png"),
            c("raw_03_top_right_sources_train_b.png"),
            c("raw_01_top_left_sources_train_a.png"),
            c("raw_06_train_a_dc_control.png"),
            c("raw_08_bottom_cross_control.png"),
            c("raw_07_train_b_dc_control.png"),
            c("raw_11_full_right_system.png"),
            c("raw_13_sr_to_b_relays.png"),
            c("overlay_13_sr_to_b_relays.png"),
            c("raw_14b_ds_sat1_bus13a_detail.png"),
            c("raw_18_full_control_raceway_lower.png"),
            c("raw_19_sat_source_full_trace.png"),
            c("raw_16_mcc_a_b_control_bottom.png"),
        ),
        output_low=900,
        output_expected=1600,
        output_high=2600,
        reasoning_low=1500,
        reasoning_expected=4500,
        reasoning_high=9000,
    ),
    CallEstimate(
        document="7",
        iteration="1",
        round_name="round1_diego",
        call_id="subagent_019f6e2d-a5bc-7b10-8609-a43e28e1e601",
        agent="Diego",
        model="gpt-5.5",
        reasoning_effort="xhigh",
        prompt_summary="High-recall extraction from full raw, mask, and overlay.",
        text_payload=DIEGO_R1_TEXT * 5,
        image_paths=(RAW, MASK, OVERLAY),
        output_low=1800,
        output_expected=2800,
        output_high=4200,
        reasoning_low=3000,
        reasoning_expected=8000,
        reasoning_high=16000,
    ),
    CallEstimate(
        document="7",
        iteration="1",
        round_name="round1_jennifer",
        call_id="subagent_019f6e37-1596-7191-8831-8eae28058473",
        agent="Jennifer",
        model="gpt-5.5",
        reasoning_effort="xhigh",
        prompt_summary="Precision review of Diego R1 with full images and regional crops.",
        text_payload=JENNIFER_R1_TEXT * 8,
        image_paths=(
            RAW,
            MASK,
            OVERLAY,
            c("raw_01_top_left_sources_train_a.png"),
            c("raw_02_top_center_bus_ties.png"),
            c("raw_03_top_right_sources_train_b.png"),
            c("raw_04_train_a_load_centers.png"),
            c("raw_05_train_b_load_centers.png"),
            c("raw_06_train_a_dc_control.png"),
            c("raw_07_train_b_dc_control.png"),
            c("raw_08_bottom_cross_control.png"),
            c("raw_09_notes_legend_title.png"),
            c("overlay_04_train_a_load_centers.png"),
            c("overlay_05_train_b_load_centers.png"),
            c("overlay_06_train_a_dc_control.png"),
            c("overlay_07_train_b_dc_control.png"),
            c("overlay_08_bottom_cross_control.png"),
        ),
        output_low=2200,
        output_expected=3300,
        output_high=4800,
        reasoning_low=3500,
        reasoning_expected=9000,
        reasoning_high=18000,
    ),
    CallEstimate(
        document="7",
        iteration="1",
        round_name="round2_diego",
        call_id="subagent_019f6e3f-79c7-7432-948d-094a3b6b52aa",
        agent="Diego",
        model="gpt-5.5",
        reasoning_effort="xhigh",
        prompt_summary="Targeted adjudication of Jennifer R1 uncertainties.",
        text_payload=DIEGO_R2_TEXT * 7,
        image_paths=(
            RAW,
            OVERLAY,
            c("raw_02_top_center_bus_ties.png"),
            c("raw_03_top_right_sources_train_b.png"),
            c("raw_06_train_a_dc_control.png"),
            c("raw_07_train_b_dc_control.png"),
            c("raw_08_bottom_cross_control.png"),
            c("overlay_06_train_a_dc_control.png"),
            c("overlay_07_train_b_dc_control.png"),
            c("overlay_08_bottom_cross_control.png"),
        ),
        output_low=180,
        output_expected=300,
        output_high=600,
        reasoning_low=2500,
        reasoning_expected=6500,
        reasoning_high=13000,
    ),
    CallEstimate(
        document="7",
        iteration="1",
        round_name="round2_jennifer_final",
        call_id="subagent_019f6e49-a718-7340-9a51-c47635639e5f",
        agent="Jennifer",
        model="gpt-5.5",
        reasoning_effort="xhigh",
        prompt_summary="Final precision saturation check using added SR-to-B-relay crop.",
        text_payload=JENNIFER_R2_TEXT * 7,
        image_paths=(
            RAW,
            OVERLAY,
            c("raw_01_top_left_sources_train_a.png"),
            c("raw_02_top_center_bus_ties.png"),
            c("raw_03_top_right_sources_train_b.png"),
            c("raw_06_train_a_dc_control.png"),
            c("raw_07_train_b_dc_control.png"),
            c("raw_08_bottom_cross_control.png"),
            c("raw_13_sr_to_b_relays.png"),
            c("overlay_13_sr_to_b_relays.png"),
        ),
        output_low=180,
        output_expected=350,
        output_high=700,
        reasoning_low=2500,
        reasoning_expected=6500,
        reasoning_high=13000,
    ),
    CallEstimate(
        document="7",
        iteration="1",
        round_name="round3_diego_saturation",
        call_id="subagent_019f6e4e-1638-7e12-a167-c8702c10bf59",
        agent="Diego",
        model="gpt-5.5",
        reasoning_effort="xhigh",
        prompt_summary="Saturation check after Jennifer R2 accepted RELAY-K202--SR-101.",
        text_payload=DIEGO_R3_TEXT * 7,
        image_paths=(
            RAW,
            OVERLAY,
            c("raw_01_top_left_sources_train_a.png"),
            c("raw_02_top_center_bus_ties.png"),
            c("raw_03_top_right_sources_train_b.png"),
            c("raw_04_train_a_load_centers.png"),
            c("raw_05_train_b_load_centers.png"),
            c("raw_06_train_a_dc_control.png"),
            c("raw_07_train_b_dc_control.png"),
            c("raw_08_bottom_cross_control.png"),
            c("raw_13_sr_to_b_relays.png"),
            c("overlay_13_sr_to_b_relays.png"),
        ),
        output_low=150,
        output_expected=250,
        output_high=500,
        reasoning_low=2200,
        reasoning_expected=6000,
        reasoning_high=12000,
    ),
]


def write_image_details() -> None:
    image_paths = sorted({path for call in CALLS for path in call.image_paths})
    with (RESULTS / "image_token_estimate_details.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["image", "width", "height", "tiles", "high_detail_tokens_est"])
        for path in image_paths:
            tokens, width, height, tiles = high_detail_image_tokens(path)
            writer.writerow([str(path), width, height, tiles, tokens])


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = [call.row() for call in CALLS]
    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    totals = {
        "document": "7",
        "iteration": "1",
        "call_count_estimated": len(rows),
        "input_tokens_expected": sum(int(row["input_tokens_expected"]) for row in rows),
        "image_file_input_tokens_est": sum(
            int(row["image_file_input_tokens_est"]) for row in rows
        ),
        "output_tokens_expected": sum(int(row["output_tokens_expected"]) for row in rows),
        "reasoning_tokens_expected": sum(
            int(row["reasoning_tokens_expected"]) for row in rows
        ),
        "total_tokens_low": sum(int(row["total_tokens_low"]) for row in rows),
        "total_tokens_expected": sum(
            int(row["total_tokens_expected"]) for row in rows
        ),
        "total_tokens_high": sum(int(row["total_tokens_high"]) for row in rows),
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
        "responses_count_endpoint_used": False,
        "estimation_method": (
            "Text tokens estimated with tiktoken o200k_base when installed, otherwise "
            "characters/4. Image input estimated with high-detail 85 + 170*512px tile "
            "heuristic after resizing. Usage objects and cached/reasoning token details "
            "were not exposed by the local Codex/subagent runtime."
        ),
    }
    (RESULTS / "token_usage_totals.json").write_text(
        json.dumps(totals, indent=2),
        encoding="utf-8",
    )

    summary = [
        "# Token Usage Estimate - Document 7",
        "",
        "The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment.",
        "These are local estimates, not billing records.",
        "",
        "| Document | Iteration | Calls | Input Expected | Image Input | Output Expected | Reasoning Expected | Total Low | Total Expected | Total High |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        (
            f"| {totals['document']} | {totals['iteration']} | {totals['call_count_estimated']} | "
            f"{totals['input_tokens_expected']} | {totals['image_file_input_tokens_est']} | "
            f"{totals['output_tokens_expected']} | {totals['reasoning_tokens_expected']} | "
            f"{totals['total_tokens_low']} | {totals['total_tokens_expected']} | {totals['total_tokens_high']} |"
        ),
        "",
        "Per-call rows are in `token_usage_estimate.csv`; per-image estimates are in `image_token_estimate_details.csv`.",
    ]
    (RESULTS / "token_usage_summary.md").write_text(
        "\n".join(summary),
        encoding="utf-8",
    )
    write_image_details()
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
