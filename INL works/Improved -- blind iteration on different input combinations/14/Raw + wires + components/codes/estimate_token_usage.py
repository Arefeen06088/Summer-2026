from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"
FOCUSED = CROPS_DIR / "focused_raw"
RAW_CROPS = CROPS_DIR / "raw_--_synthetic_npp_electrical_schematic_even_bus_spacing_1"
OVERLAY_CROPS = CROPS_DIR / "wires_mask_overlay"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
DETECTED = BASE_DIR / "detected_components_overlay.png"
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
    # Practical no-key fallback used here: rough English/code tokenization ~= 4 chars/token.
    return max(1, math.ceil(char_count / 4))


def image_dimensions(path: Path) -> tuple[int, int]:
    if Image is None or not path.exists():
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

    short_side = min(width, height)
    if short_side > 768:
        scale = 768 / short_side
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
    prompt_chars_expected: int,
    images: list[Path],
    output_tokens_expected: int,
) -> CallEstimate:
    text_expected = estimate_text_tokens(prompt_chars_expected)
    image_expected = image_tokens(images)
    input_expected = text_expected + image_expected
    input_low = math.floor(text_expected * 0.80 + image_expected * 0.90)
    input_high = math.ceil(text_expected * 1.25 + image_expected * 1.15)
    output_low = math.floor(output_tokens_expected * 0.65)
    output_high = math.ceil(output_tokens_expected * 1.45)
    return CallEstimate(
        document="14",
        iteration="1",
        round=round_name,
        call_id=call_id,
        caller=caller,
        purpose=purpose,
        input_tokens_low=input_low,
        input_tokens_expected=input_expected,
        input_tokens_high=input_high,
        cached_input_tokens="not exposed; assumed 0 in totals",
        image_file_input_tokens_expected=image_expected,
        output_tokens_low=output_low,
        output_tokens_expected=output_tokens_expected,
        output_tokens_high=output_high,
        reasoning_tokens="not exposed by local/subagent tools",
        total_tokens_low=input_low + output_low,
        total_tokens_expected=input_expected + output_tokens_expected,
        total_tokens_high=input_high + output_high,
        usage_object_available="no",
        estimation_method="No API key for Responses input-token counting endpoint; text ~= chars/4 and images ~= high-detail 512-tile formula.",
    )


def build_estimates() -> list[CallEstimate]:
    focused_overview = [
        FOCUSED / "notes_legend.png",
        FOCUSED / "train_a_sources_bus.png",
        FOCUSED / "train_b_sources_bus.png",
        FOCUSED / "train_a_safety_loads.png",
        FOCUSED / "train_b_safety_loads.png",
        FOCUSED / "train_a_480_feeders_left.png",
        FOCUSED / "train_a_480_feeders_right.png",
        FOCUSED / "train_b_480_feeders_left.png",
        FOCUSED / "train_b_480_feeders_right.png",
        FOCUSED / "train_a_dc_bus_ups.png",
        FOCUSED / "train_b_dc_bus_ups.png",
        FOCUSED / "center_intertrain_links.png",
    ]
    broad = [
        RAW_CROPS / "whole_drawing_area.png",
        RAW_CROPS / "train_a_upper_4160.png",
        RAW_CROPS / "train_b_upper_4160.png",
        RAW_CROPS / "train_a_480_mcc.png",
        RAW_CROPS / "train_b_480_mcc.png",
        RAW_CROPS / "train_a_dc_ups.png",
        RAW_CROPS / "train_b_dc_ups.png",
    ]
    main_visual_checks = [
        FOCUSED / "center_intertrain_links.png",
        FOCUSED / "train_a_panel_links.png",
        FOCUSED / "train_b_panel_links.png",
        FOCUSED / "master_terminal_blocks.png",
        FOCUSED / "train_a_dc_bus_ups.png",
        FOCUSED / "train_b_dc_bus_ups.png",
        RAW_CROPS / "train_a_dc_ups.png",
        RAW_CROPS / "train_b_dc_ups.png",
        RAW_CROPS / "train_a_480_mcc.png",
        RAW_CROPS / "train_b_480_mcc.png",
        OVERLAY_CROPS / "train_a_dc_ups.png",
        OVERLAY_CROPS / "train_b_dc_ups.png",
    ]
    critical_review = [
        RAW,
        DETECTED,
        WIRES_OVERLAY,
        *focused_overview,
        FOCUSED / "train_a_panel_links.png",
        FOCUSED / "train_b_panel_links.png",
        FOCUSED / "master_terminal_blocks.png",
    ]
    final_review = [
        FOCUSED / "center_intertrain_links.png",
        FOCUSED / "train_a_panel_links.png",
        FOCUSED / "train_b_panel_links.png",
        FOCUSED / "train_a_dc_bus_ups.png",
        FOCUSED / "train_b_dc_bus_ups.png",
        RAW_CROPS / "train_a_480_mcc.png",
        RAW_CROPS / "train_b_480_mcc.png",
    ]

    return [
        make_call(
            round_name="setup",
            call_id="main-01",
            caller="Main",
            purpose="Continuation/orientation, resource policy check, subagent-tool discovery, and Jennifer R1 dispatch.",
            prompt_chars_expected=36_000,
            images=[],
            output_tokens_expected=700,
        ),
        make_call(
            round_name="round01_diego",
            call_id="diego-01",
            caller="Diego",
            purpose="High-recall extraction from raw schematic, overlays, broad crops, and focused crops.",
            prompt_chars_expected=6_500,
            images=[RAW, DETECTED, WIRES_OVERLAY, *broad, *focused_overview],
            output_tokens_expected=8_700,
        ),
        make_call(
            round_name="round01_jennifer",
            call_id="jennifer-01",
            caller="Jennifer",
            purpose="Precision review of Diego R1 edge/node proposal against visual resources.",
            prompt_chars_expected=31_500,
            images=critical_review,
            output_tokens_expected=6_900,
        ),
        make_call(
            round_name="integration",
            call_id="main-02",
            caller="Main",
            purpose="Local visual inspection of panel, relay, DC/UPS, tie, and terminal-block crops while Jennifer reviewed.",
            prompt_chars_expected=10_500,
            images=main_visual_checks,
            output_tokens_expected=650,
        ),
        make_call(
            round_name="round02_diego",
            call_id="diego-02",
            caller="Diego",
            purpose="Saturation review of Jennifer corrections and final-add/remove decision.",
            prompt_chars_expected=24_000,
            images=final_review,
            output_tokens_expected=180,
        ),
        make_call(
            round_name="round02_jennifer",
            call_id="jennifer-02",
            caller="Jennifer",
            purpose="Final precision signoff after Diego R2 agreement.",
            prompt_chars_expected=700,
            images=[],
            output_tokens_expected=130,
        ),
        make_call(
            round_name="artifacts",
            call_id="main-03",
            caller="Main",
            purpose="Artifact writing, validation, token estimate generation, and final user summary.",
            prompt_chars_expected=22_000,
            images=[],
            output_tokens_expected=1_000,
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
    totals = {
        "input_low": sum(row.input_tokens_low for row in rows),
        "input_expected": sum(row.input_tokens_expected for row in rows),
        "input_high": sum(row.input_tokens_high for row in rows),
        "image_expected": sum(row.image_file_input_tokens_expected for row in rows),
        "output_low": sum(row.output_tokens_low for row in rows),
        "output_expected": sum(row.output_tokens_expected for row in rows),
        "output_high": sum(row.output_tokens_high for row in rows),
        "total_low": sum(row.total_tokens_low for row in rows),
        "total_expected": sum(row.total_tokens_expected for row in rows),
        "total_high": sum(row.total_tokens_high for row in rows),
    }
    lines = [
        "# Document 14 Token Usage Estimate",
        "",
        "Actual Responses usage objects were not exposed by this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. This file is therefore a reproducible estimate.",
        "",
        "## Grouped Total",
        "",
        "| Document | Iteration | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| 14 | 1 | {totals['input_expected']} | {totals['image_expected']} | {totals['output_expected']} | {totals['total_low']} | {totals['total_expected']} | {totals['total_high']} |",
        "",
        "## Call Inventory",
        "",
        "| Document | Iteration | Round | Call | Caller | Input low | Input expected | Input high | Cached input | Image/file expected | Output low | Output expected | Output high | Reasoning | Total low | Total expected | Total high | Usage object |",
        "|---|---:|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.document} | {row.iteration} | {row.round} | {row.call_id} | {row.caller} | "
            f"{row.input_tokens_low} | {row.input_tokens_expected} | {row.input_tokens_high} | {row.cached_input_tokens} | "
            f"{row.image_file_input_tokens_expected} | {row.output_tokens_low} | {row.output_tokens_expected} | {row.output_tokens_high} | "
            f"{row.reasoning_tokens} | {row.total_tokens_low} | {row.total_tokens_expected} | {row.total_tokens_high} | {row.usage_object_available} |"
        )
    lines.extend(
        [
            "",
            "## Method",
            "",
            "- Planned Responses input-token counting was not possible without an API key.",
            "- Text input: estimated as character count divided by 4.",
            "- Image/file input: estimated locally with the high-detail image formula: scale within 2048 px, short side to 768 px, then `85 + 170 * 512px tiles`.",
            "- Cached input tokens and reasoning tokens were not exposed by the available tools; totals assume 0 cached tokens and do not separately account for hidden reasoning.",
            "- Low/high ranges vary text inputs, image estimates, and unknown outputs to give the requested low / expected / high band.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_estimates()
    write_csv(RESULTS_DIR / "token_usage_estimate.csv", rows)
    (RESULTS_DIR / "token_usage_estimate.json").write_text(
        json.dumps([asdict(row) for row in rows], indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(RESULTS_DIR / "token_usage_estimate.md", rows)
    total = sum(row.total_tokens_expected for row in rows)
    print(f"Wrote token usage estimates for {len(rows)} model-call groups.")
    print(f"Expected total tokens: {total}")


if __name__ == "__main__":
    main()
