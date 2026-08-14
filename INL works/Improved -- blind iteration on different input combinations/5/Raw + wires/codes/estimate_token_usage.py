from __future__ import annotations

import csv
import math
import os
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = RESULTS / "crops"
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png"
MASK = ROOT / "wires_mask.png"
OVERLAY = ROOT / "wires_mask_overlay.png"


def approx_text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def image_tokens_high_detail(path: Path) -> tuple[int, int, int, int, int]:
    with Image.open(path) as im:
        width, height = im.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width_1 = max(1, round(width * scale))
    height_1 = max(1, round(height * scale))
    shortest = min(width_1, height_1)
    if shortest > 768:
        scale_2 = 768 / shortest
        width_2 = max(1, round(width_1 * scale_2))
        height_2 = max(1, round(height_1 * scale_2))
    else:
        width_2, height_2 = width_1, height_1
    tiles = math.ceil(width_2 / 512) * math.ceil(height_2 / 512)
    return 85 + 170 * tiles, width, height, width_2, height_2


def image_token_sum(paths: list[Path]) -> int:
    return sum(image_tokens_high_detail(path)[0] for path in paths)


@dataclass
class CallEstimate:
    call_id: str
    actor: str
    round_name: str
    purpose: str
    images: list[Path] = field(default_factory=list)
    expected_input_text_tokens: int = 0
    expected_cached_tokens: int = 0
    output_expected: int = 0
    reasoning_expected: int = 0
    notes: str = ""

    def image_tokens(self) -> int:
        return image_token_sum(self.images)

    def input_expected(self) -> int:
        return self.expected_input_text_tokens + self.image_tokens() + self.expected_cached_tokens

    def input_low(self) -> int:
        return max(1, round(self.input_expected() * 0.75))

    def input_high(self) -> int:
        return max(1, round(self.input_expected() * 1.30))

    def output_low(self) -> int:
        return max(0, round(self.output_expected * 0.65))

    def output_high(self) -> int:
        return max(self.output_expected, round(self.output_expected * 1.45))

    def reasoning_low(self) -> int:
        return max(0, round(self.reasoning_expected * 0.50))

    def reasoning_high(self) -> int:
        return max(self.reasoning_expected, round(self.reasoning_expected * 1.75))

    def total_low(self) -> int:
        return self.input_low() + self.output_low() + self.reasoning_low()

    def total_expected(self) -> int:
        return self.input_expected() + self.output_expected + self.reasoning_expected

    def total_high(self) -> int:
        return self.input_high() + self.output_high() + self.reasoning_high()


def call_estimates() -> list[CallEstimate]:
    diego_r1_images = [RAW, MASK, OVERLAY]
    jennifer_r1_images = [
        RAW,
        MASK,
        OVERLAY,
        CROPS / "raw_01_top_left_grid_bus_aux_a.png",
        CROPS / "raw_02_top_center_station_bus_ties.png",
        CROPS / "raw_03_top_right_grid_bus_aux_b.png",
        CROPS / "raw_04_division_i_left.png",
        CROPS / "raw_05_division_ii_mid_left.png",
        CROPS / "raw_06_division_iii_mid_right.png",
        CROPS / "raw_07_division_iv_right.png",
        CROPS / "raw_08_esf_control_right.png",
        CROPS / "raw_09_bottom_dc_left.png",
        CROPS / "raw_10_bottom_dc_right.png",
        CROPS / "raw_13_full_bottom_title.png",
        CROPS / "overlay_04_division_i_left.png",
        CROPS / "overlay_05_division_ii_mid_left.png",
        CROPS / "overlay_06_division_iii_mid_right.png",
        CROPS / "overlay_07_division_iv_right.png",
        CROPS / "overlay_08_esf_control_right.png",
        CROPS / "overlay_09_bottom_dc_left.png",
        CROPS / "overlay_10_bottom_dc_right.png",
    ]
    diego_r2_images = [
        CROPS / "raw_08_esf_control_right.png",
        CROPS / "overlay_08_esf_control_right.png",
        CROPS / "raw_09_bottom_dc_left.png",
        CROPS / "overlay_09_bottom_dc_left.png",
        CROPS / "raw_10_bottom_dc_right.png",
        CROPS / "overlay_10_bottom_dc_right.png",
        CROPS / "raw_13_full_bottom_title.png",
        CROPS / "raw_04_division_i_left.png",
        CROPS / "raw_06_division_iii_mid_right.png",
        CROPS / "raw_07_division_iv_right.png",
    ]
    jennifer_final_images = [
        CROPS / "zoom_esf_upper_raw.png",
        CROPS / "zoom_esf_mid_raw.png",
        CROPS / "zoom_esf_left_routes_raw.png",
        CROPS / "zoom_esf_upper_overlay.png",
        CROPS / "zoom_esf_mid_overlay.png",
        CROPS / "raw_13_full_bottom_title.png",
    ]
    main_visual_images = [
        RAW,
        CROPS / "raw_02_top_center_station_bus_ties.png",
        CROPS / "raw_01_top_left_grid_bus_aux_a.png",
        CROPS / "raw_03_top_right_grid_bus_aux_b.png",
        CROPS / "raw_04_division_i_left.png",
        CROPS / "overlay_04_division_i_left.png",
        CROPS / "raw_05_division_ii_mid_left.png",
        CROPS / "overlay_05_division_ii_mid_left.png",
        CROPS / "raw_06_division_iii_mid_right.png",
        CROPS / "overlay_06_division_iii_mid_right.png",
        CROPS / "raw_07_division_iv_right.png",
        CROPS / "overlay_07_division_iv_right.png",
        CROPS / "raw_08_esf_control_right.png",
        CROPS / "overlay_08_esf_control_right.png",
        CROPS / "raw_09_bottom_dc_left.png",
        CROPS / "overlay_09_bottom_dc_left.png",
        CROPS / "raw_10_bottom_dc_right.png",
        CROPS / "overlay_10_bottom_dc_right.png",
        CROPS / "raw_13_full_bottom_title.png",
        CROPS / "zoom_esf_upper_raw.png",
        CROPS / "zoom_esf_mid_raw.png",
        CROPS / "zoom_esf_left_routes_raw.png",
    ]

    diego_r1_cached = image_token_sum(diego_r1_images) + 5200
    jennifer_r1_cached = image_token_sum(jennifer_r1_images) + 8200

    return [
        CallEstimate(
            call_id="main_01_intake_crop_spawn",
            actor="Main",
            round_name="setup",
            purpose="Task intake, file inventory, crop creation, Diego R1 spawn.",
            expected_input_text_tokens=3100,
            output_expected=1100,
            reasoning_expected=1900,
            notes="Aggregated main-agent setup estimate; exact internal usage unavailable.",
        ),
        CallEstimate(
            call_id="diego_01_high_recall_extract",
            actor="Diego",
            round_name="round1",
            purpose="High-recall extraction from full raw, mask, and overlay.",
            images=diego_r1_images,
            expected_input_text_tokens=1450,
            output_expected=4700,
            reasoning_expected=5800,
            notes="Actual subagent usage object not exposed.",
        ),
        CallEstimate(
            call_id="main_02_visual_crosscheck",
            actor="Main",
            round_name="round1_review_prep",
            purpose="Main-agent visual inspection of crops and local edge-count modeling.",
            images=main_visual_images,
            expected_input_text_tokens=4600,
            output_expected=1900,
            reasoning_expected=3600,
            notes="Aggregates image-bearing tool results consumed by main agent.",
        ),
        CallEstimate(
            call_id="jennifer_01_precision_review",
            actor="Jennifer",
            round_name="round1",
            purpose="Precision review of Diego R1 using full images and selected crops.",
            images=jennifer_r1_images,
            expected_input_text_tokens=5000,
            output_expected=3900,
            reasoning_expected=5900,
            notes="Actual subagent usage object not exposed.",
        ),
        CallEstimate(
            call_id="diego_02_narrow_recheck",
            actor="Diego",
            round_name="round2",
            purpose="Narrow control-bay, ground, and ATS recheck.",
            images=diego_r2_images,
            expected_input_text_tokens=2400,
            expected_cached_tokens=diego_r1_cached,
            output_expected=3700,
            reasoning_expected=4300,
            notes="Follow-up in Diego thread; cached context estimate only.",
        ),
        CallEstimate(
            call_id="jennifer_02_final_audit",
            actor="Jennifer",
            round_name="round2_final",
            purpose="Final precision audit of Diego R2 additions.",
            images=jennifer_final_images,
            expected_input_text_tokens=1900,
            expected_cached_tokens=jennifer_r1_cached,
            output_expected=420,
            reasoning_expected=1600,
            notes="Follow-up in Jennifer thread; cached context estimate only.",
        ),
        CallEstimate(
            call_id="main_03_artifacts_final",
            actor="Main",
            round_name="artifacts",
            purpose="Write matrices, QA, token report, and final synthesis.",
            expected_input_text_tokens=2600,
            output_expected=900,
            reasoning_expected=2200,
            notes="Aggregated main-agent artifact generation estimate.",
        ),
    ]


def write_csv(calls: list[CallEstimate]) -> None:
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "document",
            "iteration",
            "call_id",
            "actor",
            "round",
            "model",
            "input_tokens_low",
            "input_tokens_expected",
            "input_tokens_high",
            "cached_input_tokens_expected",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens_low",
            "reasoning_tokens_expected",
            "reasoning_tokens_high",
            "image_file_input_tokens_expected",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
            "usage_object_available",
            "responses_counting_endpoint_used",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for call in calls:
            writer.writerow(
                {
                    "document": 5,
                    "iteration": 1,
                    "call_id": call.call_id,
                    "actor": call.actor,
                    "round": call.round_name,
                    "model": "gpt-5.5" if call.actor in {"Diego", "Jennifer"} else "main-agent",
                    "input_tokens_low": call.input_low(),
                    "input_tokens_expected": call.input_expected(),
                    "input_tokens_high": call.input_high(),
                    "cached_input_tokens_expected": call.expected_cached_tokens,
                    "output_tokens_low": call.output_low(),
                    "output_tokens_expected": call.output_expected,
                    "output_tokens_high": call.output_high(),
                    "reasoning_tokens_low": call.reasoning_low(),
                    "reasoning_tokens_expected": call.reasoning_expected,
                    "reasoning_tokens_high": call.reasoning_high(),
                    "image_file_input_tokens_expected": call.image_tokens(),
                    "total_tokens_low": call.total_low(),
                    "total_tokens_expected": call.total_expected(),
                    "total_tokens_high": call.total_high(),
                    "usage_object_available": "no",
                    "responses_counting_endpoint_used": "no_api_key" if not os.environ.get("OPENAI_API_KEY") else "not_called_in_codex_tooling",
                    "notes": call.notes,
                }
            )


def write_image_details(calls: list[CallEstimate]) -> None:
    rows = []
    seen: set[Path] = set()
    for call in calls:
        for image in call.images:
            if image in seen:
                continue
            seen.add(image)
            tokens, width, height, scaled_width, scaled_height = image_tokens_high_detail(image)
            rows.append(
                {
                    "image": str(image),
                    "width": width,
                    "height": height,
                    "scaled_width": scaled_width,
                    "scaled_height": scaled_height,
                    "estimated_high_detail_tokens": tokens,
                }
            )
    with (RESULTS / "image_token_estimate_details.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(calls: list[CallEstimate]) -> None:
    low = sum(call.total_low() for call in calls)
    expected = sum(call.total_expected() for call in calls)
    high = sum(call.total_high() for call in calls)
    lines = [
        "# Token Usage Estimate - Document 5, Iteration 1",
        "",
        "No OpenAI API key was available, so the Responses input-token counting endpoint was not called. Actual usage objects were not exposed by the Codex subagent tools. Estimates use local text-token approximation plus a high-detail image tiling heuristic.",
        "",
        f"Low / expected / high total estimate: {low:,} / {expected:,} / {high:,} tokens.",
        "",
        "| Call | Actor | Round | Input exp | Cached exp | Image exp | Output exp | Reasoning exp | Total low/exp/high |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for call in calls:
        lines.append(
            "| "
            + " | ".join(
                [
                    call.call_id,
                    call.actor,
                    call.round_name,
                    f"{call.input_expected():,}",
                    f"{call.expected_cached_tokens:,}",
                    f"{call.image_tokens():,}",
                    f"{call.output_expected:,}",
                    f"{call.reasoning_expected:,}",
                    f"{call.total_low():,}/{call.total_expected():,}/{call.total_high():,}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Method Notes",
            "- Subagent calls were Diego R1, Jennifer R1, Diego R2, and Jennifer final R2, all requested with `gpt-5.5`.",
            "- Main-agent calls are grouped into logical workflow phases because exact internal Codex model-call boundaries are unavailable.",
            "- Cached input token estimates are estimates for follow-up messages in the same subagent thread.",
            "- Image/file input token estimates are already included in input-token estimates.",
            "",
        ]
    )
    (RESULTS / "token_usage_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    calls = call_estimates()
    write_csv(calls)
    write_image_details(calls)
    write_markdown(calls)
    print(f"Expected total tokens: {sum(call.total_expected() for call in calls)}")


if __name__ == "__main__":
    main()
