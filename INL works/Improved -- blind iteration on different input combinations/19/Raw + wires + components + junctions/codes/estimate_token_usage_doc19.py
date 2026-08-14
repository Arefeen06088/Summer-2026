from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import tiktoken

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components + junctions")
RESULTS = BASE / "results"
CROPS = BASE / "codes" / "crops"


def enc() -> tiktoken.Encoding:
    # gpt-5 tokenizer metadata may not be available locally; o200k_base is the
    # closest OpenAI-family fallback available through tiktoken.
    return tiktoken.get_encoding("o200k_base")


def text_tokens(text: str) -> int:
    try:
        return len(enc().encode(text))
    except Exception:
        # Offline fallback: a conservative English/code estimate based on
        # word-like chunks plus punctuation. This avoids network/API reliance.
        pieces = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        return max(1, int(len(pieces) * 1.25))


def image_tokens_high_detail(path: Path) -> int:
    """OpenAI-style high-detail image estimate: 85 base + 170 per 512px tile.

    This follows the public GPT-4o/GPT-4.1 image-token estimation heuristic and
    is used only because no API key is available for the Responses token counter.
    """
    with Image.open(path) as img:
        width, height = img.size
    scale = min(2048 / width, 2048 / height, 1.0)
    width = max(1, math.ceil(width * scale))
    height = max(1, math.ceil(height * scale))
    if min(width, height) > 768:
        scale = 768 / min(width, height)
        width = max(1, math.ceil(width * scale))
        height = max(1, math.ceil(height * scale))
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_sum(paths: list[Path]) -> int:
    return sum(image_tokens_high_detail(p) for p in paths if p.exists())


@dataclass
class CallEstimate:
    document: str
    iteration: str
    round_name: str
    call_id: str
    agent: str
    input_summary: str
    prompt_text: str
    image_paths: list[Path]
    output_low: int
    output_expected: int
    output_high: int
    reasoning_low: int
    reasoning_expected: int
    reasoning_high: int

    def row(self) -> dict[str, object]:
        text_expected = text_tokens(self.prompt_text)
        image_expected = image_sum(self.image_paths)
        # Context/system/tool overhead for Codex is not exposed. Multipliers
        # give a practical range without pretending to be official accounting.
        text_low = int(text_expected * 0.85)
        text_high = int(text_expected * 1.35)
        image_low = int(image_expected * 0.75)
        image_high = int(image_expected * 1.35)
        total_low = text_low + image_low + self.output_low + self.reasoning_low
        total_expected = text_expected + image_expected + self.output_expected + self.reasoning_expected
        total_high = text_high + image_high + self.output_high + self.reasoning_high
        return {
            "document": self.document,
            "iteration": self.iteration,
            "round": self.round_name,
            "call_id": self.call_id,
            "agent": self.agent,
            "input_summary": self.input_summary,
            "input_tokens_low": text_low,
            "input_tokens_expected": text_expected,
            "input_tokens_high": text_high,
            "cached_input_tokens": "not_exposed",
            "image_file_tokens_low": image_low,
            "image_file_tokens_expected": image_expected,
            "image_file_tokens_high": image_high,
            "output_tokens_low": self.output_low,
            "output_tokens_expected": self.output_expected,
            "output_tokens_high": self.output_high,
            "reasoning_tokens_low": self.reasoning_low,
            "reasoning_tokens_expected": self.reasoning_expected,
            "reasoning_tokens_high": self.reasoning_high,
            "total_tokens_low": total_low,
            "total_tokens_expected": total_expected,
            "total_tokens_high": total_high,
            "usage_object": "not_available_from_codex_subagent_tool_or_no_api_key",
        }


def p(name: str) -> Path:
    if name.startswith("raw --") or name.endswith("_overlay.png") or name == "detected_components_overlay.png":
        return BASE / name
    return CROPS / name


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    main_images = [
        p("raw -- synthetic_npp_electrical_schematic_v3.png"),
        p("detected_components_overlay.png"),
        p("wire_nodes_overlay.png"),
        p("wires_mask_overlay.png"),
        p("raw__full_working_area.png"),
        p("raw__top_division_a_4160.png"),
        p("raw__top_division_b_4160.png"),
        p("raw__top_center_tie.png"),
        p("raw__division_a_loads_wide.png"),
        p("raw__division_b_loads_wide.png"),
        p("raw__bottom_control_a.png"),
        p("raw__bottom_control_b.png"),
        p("wire_nodes__bottom_control_a.png"),
        p("wire_nodes__bottom_control_b.png"),
        p("raw__mid_division_a_right_2x.png"),
        p("wire_nodes__mid_division_a_right_2x.png"),
        p("components__mid_division_a_right_2x.png"),
        p("raw__offsite_a_stack_4x.png"),
        p("raw__offsite_b_stack_4x.png"),
        p("components__offsite_a_stack_4x.png"),
        p("components__offsite_b_stack_4x.png"),
    ]

    diego_images = [
        p("raw -- synthetic_npp_electrical_schematic_v3.png"),
        p("detected_components_overlay.png"),
        p("wire_nodes_overlay.png"),
        p("wires_mask_overlay.png"),
        p("raw__top_division_a_4160.png"),
        p("raw__top_division_b_4160.png"),
        p("raw__top_center_tie.png"),
        p("raw__division_a_loads_wide.png"),
        p("raw__division_b_loads_wide.png"),
        p("raw__bottom_control_a.png"),
        p("raw__bottom_control_b.png"),
        p("raw__mid_division_a_left_2x.png"),
        p("raw__mid_division_a_center_2x.png"),
        p("raw__mid_division_a_right_2x.png"),
        p("raw__mid_division_b_left_2x.png"),
        p("raw__mid_division_b_center_2x.png"),
        p("raw__mid_division_b_right_2x.png"),
    ]

    jennifer_images = diego_images + [
        p("wire_nodes__division_a_loads_wide.png"),
        p("wire_nodes__bottom_control_a.png"),
        p("wire_nodes__bottom_control_b.png"),
    ]

    doc_prompt = (
        "Document 19 connectivity extraction. Use raw schematic plus allowed wires, "
        "component overlay, wire masks and junction aids. Deploy Diego and Jennifer. "
        "No GT. No OCR. Store round matrices and estimate token usage."
    )
    diego_r1_prompt = (
        "Diego high-recall extractor: inspect allowed resources and propose all plausible "
        "components, labels, logical nodes and edges with evidence; output node list, edge "
        "list and compact connectivity matrix. Preliminary structure: Division A/B 4160V, "
        "480V load groups, bottom 120VAC/125VDC distribution. No GT, no OCR."
    )
    jennifer_r1_prompt = (
        "Jennifer precision reviewer: review Diego round 1 proposal. Remove unsupported "
        "or overconnected edges, fix labels, mark ambiguity. Review normal load template, "
        "MOV 601, RPS 701, and control/DC crossings. No GT, no OCR."
    )
    diego_r2_prompt = (
        "Diego round 2 saturation check: evaluate Jennifer corrections to labels, RPS "
        "chain, MOV chain, and charger/battery crossing. Return agreement or remaining "
        "disputes. No GT, no OCR."
    )
    jennifer_r2_prompt = (
        "Jennifer round 2 final check: deterministic 4x crops show CB-101 and CB-102. "
        "Confirm final labels and corrected edges: RPS through INST-701, MOV through "
        "[LS-MOV601], no CHGR-125B to BUS-120AC-B junction. No GT, no OCR."
    )
    report_prompt = (
        "Main agent writes round matrices, final matrix, edge list, report, validation, "
        "and token usage estimate table with no Responses endpoint because no API key."
    )

    calls = [
        CallEstimate("19", "1", "main", "main_01_orchestration", "main", doc_prompt, doc_prompt, main_images, 1200, 2400, 4200, 1500, 3200, 6500),
        CallEstimate("19", "1", "round_01", "diego_01_extract", "Diego", "High-recall visual extraction", diego_r1_prompt, diego_images, 4500, 6500, 9000, 2500, 4500, 8000),
        CallEstimate("19", "1", "round_01", "jennifer_01_review", "Jennifer", "Precision review of Diego round 1", jennifer_r1_prompt, jennifer_images, 2200, 3500, 5500, 1800, 3200, 6500),
        CallEstimate("19", "1", "round_02", "diego_02_saturation", "Diego", "Agreement check after Jennifer round 1", diego_r2_prompt, [], 250, 650, 1300, 500, 1000, 2500),
        CallEstimate("19", "1", "round_02", "jennifer_02_saturation", "Jennifer", "Final agreement check after 4x label crops", jennifer_r2_prompt, [p("raw__offsite_a_stack_4x.png"), p("raw__offsite_b_stack_4x.png"), p("components__offsite_a_stack_4x.png"), p("components__offsite_b_stack_4x.png")], 250, 600, 1200, 500, 900, 2200),
        CallEstimate("19", "1", "main", "main_02_report", "main", "Artifact writing and final report", report_prompt, [], 900, 1600, 2800, 800, 1600, 3200),
    ]

    rows = [call.row() for call in calls]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    totals = {
        "document": "19",
        "iteration": "1",
        "call_count": len(rows),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in rows),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in rows),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in rows),
        "method": "tiktoken_o200k_base_for_text_plus_OpenAI_style_high_detail_image_tile_estimate; output/reasoning estimated; usage objects unavailable",
    }
    with (RESULTS / "token_usage_totals.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(totals.keys()))
        writer.writeheader()
        writer.writerow(totals)


if __name__ == "__main__":
    main()
