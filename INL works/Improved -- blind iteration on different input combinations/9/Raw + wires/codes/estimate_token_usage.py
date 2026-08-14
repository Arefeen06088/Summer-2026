from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw + wires"
)
RESULTS = ROOT / "results"


def text_tokens(text: str) -> int:
    """Best local estimate when the Responses token counter is unavailable."""
    try:
        import tiktoken  # type: ignore

        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def high_detail_image_tokens(path: Path) -> tuple[int, int, int, int]:
    """Approximate OpenAI high-detail image tokens: 85 base + 170 per 512 tile."""
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
    tiles = math.ceil(resized_w / 512) * math.ceil(resized_h / 512)
    return 85 + 170 * tiles, width, height, tiles


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
        image_tokens = sum(high_detail_image_tokens(path)[0] for path in self.image_paths)
        input_expected = text_input + image_tokens
        input_low = math.ceil(input_expected * 0.88)
        input_high = math.ceil(input_expected * 1.18)
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
            "usage_object_note": "Subagent/main runtime usage objects were not exposed to this tool session.",
            "responses_count_endpoint_used": "no_openai_api_key",
            "counting_method": "text via tiktoken o200k_base if installed, else chars/4; images via 85+170*512-tile high-detail heuristic",
            "input_text_tokens_est": text_input,
            "image_file_input_tokens_est": image_tokens,
            "file_input_tokens_est": 0,
            "input_tokens_low": input_low,
            "input_tokens_expected": input_expected,
            "input_tokens_high": input_high,
            "cached_input_tokens_recorded": "unavailable",
            "cached_input_tokens_est": 0,
            "output_tokens_low": self.output_low,
            "output_tokens_expected": self.output_expected,
            "output_tokens_high": self.output_high,
            "reasoning_tokens_recorded": "unavailable",
            "reasoning_tokens_low": self.reasoning_low,
            "reasoning_tokens_expected": self.reasoning_expected,
            "reasoning_tokens_high": self.reasoning_high,
            "total_tokens_low": input_low + self.output_low + self.reasoning_low,
            "total_tokens_expected": input_expected + self.output_expected + self.reasoning_expected,
            "total_tokens_high": input_high + self.output_high + self.reasoning_high,
            "image_count": len(self.image_paths),
            "image_names": "; ".join(path.name for path in self.image_paths),
        }


def p(name: str) -> Path:
    return ROOT / name


def c(name: str) -> Path:
    return RESULTS / "crops" / name


def cc(name: str) -> Path:
    return RESULTS / "close_crops" / name


RAW = p("raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png")
MASK = p("wires_mask.png")
OVERLAY = p("wires_mask_overlay.png")

COMMON = """
Document 9 connectivity extraction from Raw + wires only. No ground truth, no
GT-derived feedback, and no OCR engines. Matrix is undirected and symmetric
with identical row/column node order. Diego is high recall; Jennifer is the
precision reviewer. Model requested for subagents: gpt-5.5 with xhigh effort.
"""

DIEGO_R1 = COMMON + """
Initial high-recall extraction from full raw schematic and wire aids. Proposed
all visually plausible components, logical nodes, accepted edges, and uncertain
edges. Returned a full node order and accepted-edge list.
"""

JENNIFER_R1 = COMMON + """
Precision review of Diego R1 using the full raw schematic, overlay, and selected
crops. Corrected the tie label, revised MOV-panel feed interpretation, rejected
near-pass and unsupported control routes, and returned a refined full graph.
"""

DIEGO_R2 = COMMON + """
Targeted high-recall saturation pass over Jennifer R1, focused on relay/trip
controls, lower DC/control blocks, normal instrumentation, and MOV feeds.
"""

JENNIFER_R2 = COMMON + """
Precision review of Diego R2 deltas. Confirmed the B lower control link and
A relay/trip edge, rejected unsupported A-side JB-to-PLC route, and declared
temporary agreement.
"""

DIEGO_R3 = COMMON + """
Count-sanity high-recall pass. The raw title block looked consistent with 180
components and 200 connections, while the precision graph had fewer edges. The
prompt explicitly said not to fill the count unless endpoints were visible.
"""

JENNIFER_R3 = COMMON + """
Final precision review of Diego R3 candidates. Accepted only two additional
dashed/control edges and rejected shared-trunk or endpoint-ambiguous routes.
"""

MAIN = COMMON + """
Main Codex orchestration aggregate: inventoried files, generated standard and
close crops, visually inspected images, spawned Diego/Jennifer rounds, reconciled
round deltas, wrote matrices/QA artifacts/token estimates, and produced the
final response. This is an aggregate estimate because the runtime does not expose
a single usage object for the main agent here.
"""

MAIN_IMAGES = (
    c("raw_15_title_block.png"),
    c("raw_01_top_sources_full.png"),
    c("raw_05_left_train_a_4160_480.png"),
    c("raw_06_center_normal_4160_480.png"),
    c("raw_07_right_train_b_4160_480.png"),
    c("raw_08_left_train_a_loads.png"),
    c("raw_09_center_normal_loads_controls.png"),
    c("raw_10_right_train_b_loads.png"),
    c("raw_11_bottom_train_a_dc_control.png"),
    c("raw_12_bottom_train_b_dc_control.png"),
    c("raw_13_lower_cross_control.png"),
    c("raw_16_full_left_system.png"),
    c("raw_17_full_center_system.png"),
    c("raw_18_full_right_system.png"),
    c("overlay_08_left_train_a_loads.png"),
    c("overlay_09_center_normal_loads_controls.png"),
    c("overlay_10_right_train_b_loads.png"),
    c("overlay_11_bottom_train_a_dc_control.png"),
    c("overlay_13_lower_cross_control.png"),
    c("overlay_16_full_left_system.png"),
    c("overlay_17_full_center_system.png"),
    c("overlay_18_full_right_system.png"),
    c("mask_13_lower_cross_control.png"),
    c("mask_17_full_center_system.png"),
    cc("raw_a_relay_4160.png"),
    cc("overlay_a_relay_4160.png"),
    cc("raw_b_relay_left_4160.png"),
    cc("overlay_b_relay_left_4160.png"),
    cc("raw_a_safety_controls.png"),
    cc("overlay_a_safety_controls.png"),
    cc("raw_b_safety_controls.png"),
    cc("overlay_b_safety_controls.png"),
    cc("raw_tie_to_normal_control.png"),
    cc("overlay_tie_to_normal_control.png"),
    cc("raw_normal_lower_control.png"),
    cc("overlay_normal_lower_control.png"),
)

CALLS = [
    CallEstimate(
        "9",
        "1",
        "main",
        "main_agent_orchestration_aggregate",
        "main",
        "gpt-5-codex",
        "not_exposed",
        "Main orchestration, visual inspection, crop generation, artifact generation, and final report.",
        MAIN * 12,
        MAIN_IMAGES,
        9000,
        16000,
        26000,
        4000,
        10000,
        22000,
    ),
    CallEstimate(
        "9",
        "1",
        "round01_diego",
        "subagent_019f6e6c-341e-7191-b72d-7fc67eb4ecf6",
        "Diego",
        "gpt-5.5",
        "xhigh",
        "Initial high-recall extraction from raw plus wire aids.",
        DIEGO_R1 * 5,
        (RAW, MASK, OVERLAY),
        3500,
        6200,
        9500,
        4500,
        12000,
        24000,
    ),
    CallEstimate(
        "9",
        "1",
        "round02_jennifer",
        "subagent_019f6e74-b4a1-7bd2-b616-dc13407ad390",
        "Jennifer",
        "gpt-5.5",
        "xhigh",
        "Precision review of Diego R1 with full raw/overlay and key crops.",
        JENNIFER_R1 * 12,
        (
            RAW,
            OVERLAY,
            c("raw_01_top_sources_full.png"),
            c("raw_05_left_train_a_4160_480.png"),
            c("raw_06_center_normal_4160_480.png"),
            c("raw_08_left_train_a_loads.png"),
            c("raw_09_center_normal_loads_controls.png"),
            c("raw_10_right_train_b_loads.png"),
            c("raw_11_bottom_train_a_dc_control.png"),
            c("raw_12_bottom_train_b_dc_control.png"),
            c("raw_15_title_block.png"),
        ),
        3200,
        5600,
        8500,
        4500,
        11000,
        22000,
    ),
    CallEstimate(
        "9",
        "1",
        "round03_diego",
        "subagent_019f6e7a-caf2-77f0-b916-8a6405cbf694",
        "Diego",
        "gpt-5.5",
        "xhigh",
        "Second high-recall saturation check over Jennifer R1.",
        DIEGO_R2 * 9,
        (
            RAW,
            OVERLAY,
            c("raw_05_left_train_a_4160_480.png"),
            c("raw_07_right_train_b_4160_480.png"),
            c("raw_08_left_train_a_loads.png"),
            c("raw_09_center_normal_loads_controls.png"),
            c("raw_10_right_train_b_loads.png"),
            c("raw_11_bottom_train_a_dc_control.png"),
            c("raw_12_bottom_train_b_dc_control.png"),
            c("raw_13_lower_cross_control.png"),
            c("overlay_16_full_left_system.png"),
            c("overlay_18_full_right_system.png"),
        ),
        250,
        500,
        1000,
        2500,
        6500,
        14000,
    ),
    CallEstimate(
        "9",
        "1",
        "round04_jennifer",
        "subagent_019f6e81-f0be-7bd3-9bfe-2d2eedf60e6f",
        "Jennifer",
        "gpt-5.5",
        "xhigh",
        "Precision review of Diego R2 deltas using close relay/control crops.",
        JENNIFER_R2 * 7,
        (
            RAW,
            OVERLAY,
            cc("raw_b_relay_left_4160.png"),
            cc("overlay_b_relay_left_4160.png"),
            cc("raw_a_relay_4160.png"),
            cc("overlay_a_relay_4160.png"),
            cc("raw_a_safety_controls.png"),
            cc("overlay_a_safety_controls.png"),
            cc("raw_b_safety_controls.png"),
            cc("overlay_b_safety_controls.png"),
        ),
        180,
        350,
        700,
        2200,
        6000,
        12000,
    ),
    CallEstimate(
        "9",
        "1",
        "round05_diego",
        "subagent_019f6e86-dca4-7df2-9939-2586b24e0c2d",
        "Diego",
        "gpt-5.5",
        "xhigh",
        "Count-sanity high-recall pass; do not force the raw count.",
        DIEGO_R3 * 10,
        (
            RAW,
            OVERLAY,
            cc("raw_a_relay_4160.png"),
            cc("overlay_a_relay_4160.png"),
            cc("raw_b_relay_left_4160.png"),
            cc("overlay_b_relay_left_4160.png"),
            cc("raw_a_safety_controls.png"),
            cc("overlay_a_safety_controls.png"),
            cc("raw_b_safety_controls.png"),
            cc("overlay_b_safety_controls.png"),
            cc("raw_tie_to_normal_control.png"),
            cc("overlay_tie_to_normal_control.png"),
            cc("raw_normal_lower_control.png"),
            cc("overlay_normal_lower_control.png"),
            c("raw_17_full_center_system.png"),
            c("overlay_17_full_center_system.png"),
        ),
        900,
        1600,
        2600,
        3500,
        9000,
        18000,
    ),
    CallEstimate(
        "9",
        "1",
        "round06_jennifer_final",
        "subagent_019f6e8d-0baf-7913-bc8f-23d0cd978e08",
        "Jennifer",
        "gpt-5.5",
        "xhigh",
        "Final precision review of Diego R3 candidates.",
        JENNIFER_R3 * 9,
        (
            RAW,
            OVERLAY,
            cc("raw_a_relay_4160.png"),
            cc("overlay_a_relay_4160.png"),
            cc("raw_b_relay_left_4160.png"),
            cc("overlay_b_relay_left_4160.png"),
            cc("raw_a_safety_controls.png"),
            cc("overlay_a_safety_controls.png"),
            cc("raw_b_safety_controls.png"),
            cc("overlay_b_safety_controls.png"),
            cc("raw_tie_to_normal_control.png"),
            cc("overlay_tie_to_normal_control.png"),
            cc("raw_normal_lower_control.png"),
            cc("overlay_normal_lower_control.png"),
        ),
        300,
        650,
        1100,
        2600,
        7000,
        15000,
    ),
]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = [call.row() for call in CALLS]
    write_csv(RESULTS / "token_usage_estimate.csv", rows)

    image_rows = []
    for call in CALLS:
        for image_path in call.image_paths:
            tokens, width, height, tiles = high_detail_image_tokens(image_path)
            image_rows.append(
                {
                    "document": call.document,
                    "iteration": call.iteration,
                    "round": call.round_name,
                    "call_id": call.call_id,
                    "agent": call.agent,
                    "image": str(image_path),
                    "width": width,
                    "height": height,
                    "estimated_image_tokens": tokens,
                    "estimated_512_tiles_after_resize": tiles,
                }
            )
    write_csv(RESULTS / "image_token_estimate_details.csv", image_rows)

    totals: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        key = (str(row["document"]), str(row["iteration"]))
        if key not in totals:
            totals[key] = {
                "document": key[0],
                "iteration": key[1],
                "model_calls": 0,
                "input_tokens_low": 0,
                "input_tokens_expected": 0,
                "input_tokens_high": 0,
                "image_file_input_tokens_est": 0,
                "output_tokens_low": 0,
                "output_tokens_expected": 0,
                "output_tokens_high": 0,
                "reasoning_tokens_low": 0,
                "reasoning_tokens_expected": 0,
                "reasoning_tokens_high": 0,
                "total_tokens_low": 0,
                "total_tokens_expected": 0,
                "total_tokens_high": 0,
            }
        total = totals[key]
        total["model_calls"] = int(total["model_calls"]) + 1
        for field in (
            "input_tokens_low",
            "input_tokens_expected",
            "input_tokens_high",
            "image_file_input_tokens_est",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens_low",
            "reasoning_tokens_expected",
            "reasoning_tokens_high",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
        ):
            total[field] = int(total[field]) + int(row[field])

    totals_rows = list(totals.values())
    write_csv(RESULTS / "token_usage_totals.csv", totals_rows)
    (RESULTS / "token_usage_totals.json").write_text(
        json.dumps(totals_rows, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key was available, so the Responses input-token counting "
        "endpoint and model usage objects could not be queried.",
        "",
        "Local method: text is counted with `tiktoken` `o200k_base` when installed "
        "and falls back to `ceil(chars/4)`. Image input tokens use the common "
        "high-detail heuristic `85 + 170 * 512px_tiles_after_resize`.",
        "",
        "| Document | Iteration | Model calls | Input expected | Image/file input | "
        "Output expected | Reasoning expected | Total low | Total expected | Total high |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in totals_rows:
        lines.append(
            "| {document} | {iteration} | {model_calls} | {input_tokens_expected} | "
            "{image_file_input_tokens_est} | {output_tokens_expected} | "
            "{reasoning_tokens_expected} | {total_tokens_low} | "
            "{total_tokens_expected} | {total_tokens_high} |".format(**row)
        )
    lines.extend(
        [
            "",
            "Detailed per-call estimates are in `token_usage_estimate.csv`; "
            "per-image estimates are in `image_token_estimate_details.csv`.",
        ]
    )
    (RESULTS / "token_usage_summary.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(totals_rows, indent=2))


if __name__ == "__main__":
    main()
