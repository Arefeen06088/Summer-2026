from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"
RAW_CROPS = CROPS_DIR / "raw_--_synthetic_npp_electrical_schematic_relocated_names"
FOCUSED = CROPS_DIR / "focused_raw"


RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_relocated_names.png"
DETECTED = BASE_DIR / "detected_components_overlay.png"
WIRES_MASK = BASE_DIR / "wires_mask.png"
WIRES_OVERLAY = BASE_DIR / "wires_mask_overlay.png"


@dataclass
class CallEstimate:
    document: str
    iteration: str
    round: str
    call_id: str
    caller: str
    purpose: str
    input_tokens_low: int
    input_tokens_expected: int
    input_tokens_high: int
    cached_input_tokens: str
    image_file_input_tokens_expected: int
    output_tokens_low: int
    output_tokens_expected: int
    output_tokens_high: int
    reasoning_tokens: str
    total_tokens_low: int
    total_tokens_expected: int
    total_tokens_high: int
    usage_object_available: str
    estimation_method: str


def estimate_text_tokens(char_count: int) -> int:
    return max(1, math.ceil(char_count / 4))


def image_dimensions(path: Path) -> tuple[int, int]:
    if Image is None:
        return (0, 0)
    with Image.open(path) as img:
        return img.size


def estimate_image_tokens(path: Path, detail: str = "high") -> int:
    if not path.exists():
        return 0
    if detail == "low":
        return 85
    width, height = image_dimensions(path)
    if not width or not height:
        return 0

    scale = min(2048 / width, 2048 / height, 1.0)
    width = int(math.floor(width * scale))
    height = int(math.floor(height * scale))
    short = min(width, height)
    if short > 768:
        scale = 768 / short
        width = int(math.floor(width * scale))
        height = int(math.floor(height * scale))

    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_tokens(paths: list[Path]) -> int:
    return sum(estimate_image_tokens(path) for path in paths)


def make_call(
    *,
    round_name: str,
    call_id: str,
    caller: str,
    purpose: str,
    prompt_chars: int,
    images: list[Path],
    output_expected: int,
    output_low: int | None = None,
    output_high: int | None = None,
) -> CallEstimate:
    text_expected = estimate_text_tokens(prompt_chars)
    img_expected = image_tokens(images)
    input_expected = text_expected + img_expected
    input_low = math.floor(text_expected * 0.8 + img_expected * 0.9)
    input_high = math.ceil(text_expected * 1.25 + img_expected * 1.15)
    output_low = output_low if output_low is not None else math.floor(output_expected * 0.65)
    output_high = output_high if output_high is not None else math.ceil(output_expected * 1.45)
    return CallEstimate(
        document="11",
        iteration="1",
        round=round_name,
        call_id=call_id,
        caller=caller,
        purpose=purpose,
        input_tokens_low=input_low,
        input_tokens_expected=input_expected,
        input_tokens_high=input_high,
        cached_input_tokens="not exposed; assumed 0 in totals",
        image_file_input_tokens_expected=img_expected,
        output_tokens_low=output_low,
        output_tokens_expected=output_expected,
        output_tokens_high=output_high,
        reasoning_tokens="not exposed",
        total_tokens_low=input_low + output_low,
        total_tokens_expected=input_expected + output_expected,
        total_tokens_high=input_high + output_high,
        usage_object_available="no",
        estimation_method="Text ~= chars/4; images ~= high-detail 512-tile estimate; no API key for Responses token counting endpoint.",
    )


def build_estimates() -> list[CallEstimate]:
    all_train_overalls = [
        RAW_CROPS / "train_a_overall.png",
        RAW_CROPS / "train_b_overall.png",
        RAW_CROPS / "train_c_overall.png",
        RAW_CROPS / "train_d_overall.png",
    ]
    focused_dc = [
        FOCUSED / "bottom_division_a_dc_rps.png",
        FOCUSED / "bottom_division_b_dc_rps.png",
        FOCUSED / "ssps_and_ats_center.png",
        FOCUSED / "train_a_dc_ground_panel.png",
        FOCUSED / "train_b_dc_ground_panel.png",
        FOCUSED / "train_c_dc_ground_panel.png",
        FOCUSED / "train_d_dc_ground_panel.png",
    ]
    top_and_bottom = [
        RAW_CROPS / "top_source_and_13kv_buses.png",
        RAW_CROPS / "bottom_dc_and_interlocks.png",
    ]

    return [
        make_call(
            round_name="setup",
            call_id="main-01",
            caller="Main",
            purpose="Resource listing, crop planning, no GT check, crop script creation and execution.",
            prompt_chars=7_000,
            images=[],
            output_expected=900,
        ),
        make_call(
            round_name="round01_diego",
            call_id="diego-01",
            caller="Diego",
            purpose="High-recall extraction from raw, overlays, broad crops, and focused crops.",
            prompt_chars=9_500,
            images=[RAW, DETECTED, WIRES_MASK, WIRES_OVERLAY] + top_and_bottom + all_train_overalls + focused_dc,
            output_expected=5_300,
        ),
        make_call(
            round_name="round01_jennifer",
            call_id="jennifer-01",
            caller="Jennifer",
            purpose="Precision review of Diego R1 with raw, overlays, top, train, bottom, and focused DC/SSPS crops.",
            prompt_chars=24_000,
            images=[RAW, DETECTED, WIRES_OVERLAY] + top_and_bottom + all_train_overalls + focused_dc[:3],
            output_expected=4_200,
        ),
        make_call(
            round_name="round02_diego",
            call_id="diego-02",
            caller="Diego",
            purpose="Saturation review of Jennifer R1 corrections and critical crops.",
            prompt_chars=3_800,
            images=[RAW, WIRES_OVERLAY, RAW_CROPS / "top_source_and_13kv_buses.png"] + focused_dc,
            output_expected=900,
        ),
        make_call(
            round_name="round02_jennifer",
            call_id="jennifer-02",
            caller="Jennifer",
            purpose="Final precision signoff after Diego saturation response.",
            prompt_chars=2_800,
            images=[RAW_CROPS / "top_source_and_13kv_buses.png", RAW_CROPS / "bottom_dc_and_interlocks.png"] + focused_dc,
            output_expected=750,
        ),
        make_call(
            round_name="artifacts",
            call_id="main-02",
            caller="Main",
            purpose="Artifact writing, matrix validation, token table/report creation, and final response.",
            prompt_chars=14_000,
            images=[RAW_CROPS / "top_source_and_13kv_buses.png", RAW_CROPS / "bottom_dc_and_interlocks.png"] + focused_dc[:2],
            output_expected=1_400,
        ),
    ]


def write_csv(path: Path, rows: list[CallEstimate]) -> None:
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_markdown(path: Path, rows: list[CallEstimate]) -> None:
    total_low = sum(row.total_tokens_low for row in rows)
    total_expected = sum(row.total_tokens_expected for row in rows)
    total_high = sum(row.total_tokens_high for row in rows)
    input_expected = sum(row.input_tokens_expected for row in rows)
    image_expected = sum(row.image_file_input_tokens_expected for row in rows)
    output_expected = sum(row.output_tokens_expected for row in rows)

    lines = [
        "# Document 11 Token Usage Estimate",
        "",
        "Actual Responses usage objects were not available from this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. The table below is therefore a reproducible local estimate.",
        "",
        f"- Expected input tokens: {input_expected}",
        f"- Expected image/file input tokens: {image_expected}",
        f"- Expected output tokens: {output_expected}",
        f"- Expected total tokens: {total_expected}",
        f"- Low / expected / high total: {total_low} / {total_expected} / {total_high}",
        "",
        "| Document | Iteration | Round | Call | Caller | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high | Usage object |",
        "|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.document} | {row.iteration} | {row.round} | {row.call_id} | {row.caller} | "
            f"{row.input_tokens_expected} | {row.image_file_input_tokens_expected} | {row.output_tokens_expected} | "
            f"{row.total_tokens_low} | {row.total_tokens_expected} | {row.total_tokens_high} | {row.usage_object_available} |"
        )
    lines.extend(
        [
            "",
            "## Method",
            "",
            "- Text input estimate: character count divided by 4.",
            "- Image/file estimate: local high-detail 512-tile approximation for each attached PNG.",
            "- Cached input tokens: not exposed by the tools here; totals assume 0 cached tokens.",
            "- Reasoning tokens: not exposed.",
            "- Output ranges: low/expected/high estimates because subagent and final output length is not known in advance by the local estimator.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_estimates()
    write_csv(RESULTS_DIR / "token_usage_estimate.csv", rows)
    write_markdown(RESULTS_DIR / "token_usage_estimate.md", rows)
    (RESULTS_DIR / "token_usage_estimate.json").write_text(
        json.dumps([asdict(row) for row in rows], indent=2), encoding="utf-8"
    )
    totals = {
        "document": "11",
        "iteration": "1",
        "total_low": sum(row.total_tokens_low for row in rows),
        "total_expected": sum(row.total_tokens_expected for row in rows),
        "total_high": sum(row.total_tokens_high for row in rows),
    }
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
