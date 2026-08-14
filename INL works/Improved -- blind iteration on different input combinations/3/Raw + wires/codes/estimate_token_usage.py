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
RAW = ROOT / "raw -- synthetic_npp_100_component_electrical_schematic.png"
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
    """Approximate OpenAI high-detail image input tokens.

    Method: fit within 2048x2048, then scale shortest side to 768 if larger,
    count 512px tiles, and add the 85-token base. This is an estimate because
    no API key/usage object is available in this workflow.
    """
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
    tokens = 85 + 170 * tiles
    return tokens, width, height, width_2, height_2


def image_token_sum(paths: list[Path]) -> int:
    return sum(image_tokens_high_detail(path)[0] for path in paths)


@dataclass
class CallEstimate:
    call_id: str
    actor: str
    round_name: str
    purpose: str
    text_prompt: str = ""
    images: list[Path] = field(default_factory=list)
    expected_input_text_tokens: int | None = None
    expected_cached_tokens: int = 0
    output_expected: int = 0
    reasoning_expected: int = 0
    notes: str = ""

    def text_tokens(self) -> int:
        if self.expected_input_text_tokens is not None:
            return self.expected_input_text_tokens
        return approx_text_tokens(self.text_prompt)

    def image_tokens(self) -> int:
        return image_token_sum(self.images)

    def input_expected(self) -> int:
        return self.text_tokens() + self.image_tokens() + self.expected_cached_tokens

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

    def total_expected(self) -> int:
        return self.input_expected() + self.output_expected + self.reasoning_expected

    def total_low(self) -> int:
        return self.input_low() + self.output_low() + self.reasoning_low()

    def total_high(self) -> int:
        return self.input_high() + self.output_high() + self.reasoning_high()


def call_estimates() -> list[CallEstimate]:
    diego_r1_images = [RAW, MASK, OVERLAY]
    jennifer_r1_images = [
        RAW,
        MASK,
        OVERLAY,
        CROPS / "raw_01_top_left_sources_bus_a.png",
        CROPS / "raw_02_top_center_tie_dc.png",
        CROPS / "raw_03_top_right_sources_bus_b.png",
        CROPS / "raw_04_mcc_a1_a2_feeders.png",
        CROPS / "raw_05_mcc_b1_b2_feeders.png",
        CROPS / "raw_10_bottom_rps_esf_a.png",
        CROPS / "raw_11_bottom_rps_esf_b.png",
        CROPS / "raw_12_notes_legend_title.png",
        CROPS / "overlay_02_top_center_tie_dc.png",
        CROPS / "overlay_10_bottom_rps_esf_a.png",
        CROPS / "overlay_11_bottom_rps_esf_b.png",
    ]
    main_visual_images = [
        CROPS / "raw_02_top_center_tie_dc.png",
        CROPS / "overlay_02_top_center_tie_dc.png",
        CROPS / "raw_01_top_left_sources_bus_a.png",
        CROPS / "overlay_01_top_left_sources_bus_a.png",
        CROPS / "overlay_03_top_right_sources_bus_b.png",
        CROPS / "_zoom_ground_reference_review.png",
        CROPS / "_zoom_ground_left_review.png",
        RAW,
        CROPS / "raw_10_bottom_rps_esf_a.png",
    ]

    diego_r1_image_tokens = image_token_sum(diego_r1_images)
    jennifer_r1_image_tokens = image_token_sum(jennifer_r1_images)

    return [
        CallEstimate(
            call_id="main_01_intake_crop_spawn",
            actor="Main",
            round_name="setup",
            purpose="Task intake, file discovery, crop plan, Diego R1 spawn.",
            expected_input_text_tokens=2600,
            output_expected=900,
            reasoning_expected=1500,
            notes="Aggregated main-agent orchestration estimate; exact internal calls unavailable.",
        ),
        CallEstimate(
            call_id="diego_01_high_recall_extract",
            actor="Diego",
            round_name="round1",
            purpose="High-recall visual extraction from full raw, mask, overlay.",
            images=diego_r1_images,
            expected_input_text_tokens=1250,
            output_expected=3600,
            reasoning_expected=4500,
            notes="Actual usage object not exposed by subagent tool.",
        ),
        CallEstimate(
            call_id="jennifer_01_precision_review",
            actor="Jennifer",
            round_name="round1",
            purpose="Precision review using Diego R1 plus selected full images and crops.",
            images=jennifer_r1_images,
            expected_input_text_tokens=3200,
            output_expected=3100,
            reasoning_expected=4800,
            notes="Actual usage object not exposed by subagent tool.",
        ),
        CallEstimate(
            call_id="main_02_visual_crosscheck",
            actor="Main",
            round_name="between_rounds",
            purpose="Local visual inspection of top-center, source-gap, ground, and RPS crops.",
            images=main_visual_images,
            expected_input_text_tokens=2400,
            output_expected=1200,
            reasoning_expected=2200,
            notes="Aggregates image-bearing tool results consumed by the main agent.",
        ),
        CallEstimate(
            call_id="diego_02_narrow_recheck",
            actor="Diego",
            round_name="round2",
            purpose="Narrow recheck of source-gap and ground-reference uncertainties.",
            expected_input_text_tokens=700,
            expected_cached_tokens=diego_r1_image_tokens + 4200,
            output_expected=1900,
            reasoning_expected=2600,
            notes="Follow-up in same Diego thread; cached estimate assumes prior image/context reuse.",
        ),
        CallEstimate(
            call_id="jennifer_02_final_resolution",
            actor="Jennifer",
            round_name="round2_final",
            purpose="Final resolution of GND-1E zero-degree consistency issue.",
            expected_input_text_tokens=650,
            expected_cached_tokens=jennifer_r1_image_tokens + 6200,
            output_expected=90,
            reasoning_expected=850,
            notes="Follow-up in same Jennifer thread; cached estimate assumes prior image/context reuse.",
        ),
        CallEstimate(
            call_id="main_03_artifacts_final",
            actor="Main",
            round_name="artifacts",
            purpose="Write matrices, QA, token report, and final synthesis.",
            expected_input_text_tokens=1800,
            output_expected=800,
            reasoning_expected=1700,
            notes="Aggregated main-agent code/artifact generation estimate.",
        ),
    ]


def write_csv(calls: list[CallEstimate]) -> None:
    path = RESULTS / "token_usage_estimate.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
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
            ],
        )
        writer.writeheader()
        for call in calls:
            writer.writerow(
                {
                    "document": 3,
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
    path = RESULTS / "image_token_estimate_details.csv"
    rows = []
    seen: set[Path] = set()
    for call in calls:
        for image in call.images:
            if image not in seen:
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
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(calls: list[CallEstimate]) -> None:
    total_low = sum(call.total_low() for call in calls)
    total_expected = sum(call.total_expected() for call in calls)
    total_high = sum(call.total_high() for call in calls)

    lines = [
        "# Token Usage Estimate - Document 3, Iteration 1",
        "",
        "No OpenAI API key was available, so the Responses input-token counting endpoint was not called. Actual usage objects were not exposed by the Codex subagent tools. Estimates use local text token counting where possible plus a high-detail image tiling heuristic.",
        "",
        f"Low / expected / high total estimate: {total_low:,} / {total_expected:,} / {total_high:,} tokens.",
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
            "- The subagent model calls were Diego R1, Jennifer R1, Diego R2, and Jennifer final R2, all requested with `gpt-5.5`.",
            "- Main-agent calls are grouped into logical workflow phases because exact internal Codex model-call boundaries and usage objects are not available.",
            "- Cached input token estimates are only estimates for follow-up messages in the same subagent thread.",
            "- Image/file input token estimates are already included in the input-token estimates.",
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
    total = sum(call.total_expected() for call in calls)
    print(f"Expected total tokens: {total}")


if __name__ == "__main__":
    main()
