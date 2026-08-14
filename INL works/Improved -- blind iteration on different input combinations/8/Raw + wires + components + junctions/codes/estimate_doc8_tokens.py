from __future__ import annotations

import csv
import math
import os
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
DETECTED = BASE / "detected_components_overlay.png"
WIRE_NODES = BASE / "wire_nodes_overlay.png"
WIRE_MASK = BASE / "wires_mask_overlay.png"


def r(name: str) -> Path:
    return RESULTS / name


def text_tokens(text: str) -> int:
    if tiktoken is None:
        return max(1, math.ceil(len(text) / 4))
    try:
        try:
            enc = tiktoken.get_encoding("o200k_base")
        except Exception:
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


def image_low_tokens(_: int, __: int) -> int:
    return 70


def image_tile_high_tokens(width: int, height: int) -> int:
    scale = min(2048 / width, 2048 / height, 1.0)
    w = width * scale
    h = height * scale
    short = min(w, h)
    if short > 768:
        scale2 = 768 / short
        w *= scale2
        h *= scale2
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 70 + 140 * tiles


def image_original_patch_tokens(width: int, height: int) -> int:
    return math.ceil(width / 32) * math.ceil(height / 32)


def image_token_estimates(paths: list[Path]) -> tuple[int, int, int, int]:
    low = expected = high = tile_reference = 0
    for path in paths:
        width, height = image_size(path)
        low += image_low_tokens(width, height)
        patches = image_original_patch_tokens(width, height)
        expected += patches
        high += math.ceil(patches * 1.15) + 50
        tile_reference += image_tile_high_tokens(width, height)
    return low, expected, high, tile_reference


MAIN_VIEWED_IMAGES = [
    RAW,
    DETECTED,
    r("raw__top_left.png"),
    r("raw__top_mid.png"),
    r("raw__top_right.png"),
    r("raw__middle_left.png"),
    r("raw__middle_mid.png"),
    r("raw__middle_right.png"),
    r("raw__bottom_left.png"),
    r("raw__bottom_mid.png"),
    r("raw__bottom_right.png"),
    r("wire_nodes__left_full.png"),
    r("wire_nodes__center_full.png"),
    r("wire_nodes__right_full.png"),
    r("raw__left_full.png"),
    r("raw__center_full.png"),
    r("raw__switchgear_center.png"),
    r("raw__dc_control_a.png"),
    r("wire_nodes__dc_control_a.png"),
    r("raw__dc_control_b.png"),
]

DIEGO_ROUND1_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    r("raw__top_left.png"),
    r("raw__top_mid.png"),
    r("raw__top_right.png"),
    r("raw__middle_left.png"),
    r("raw__middle_mid.png"),
    r("raw__middle_right.png"),
    r("raw__bottom_left.png"),
    r("raw__bottom_mid.png"),
    r("raw__bottom_right.png"),
    r("wire_nodes__left_full.png"),
    r("wire_nodes__center_full.png"),
    r("wire_nodes__right_full.png"),
    r("raw__title_notes_legend.png"),
]

JENNIFER_ROUND2_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    r("raw__switchgear_center.png"),
    r("wire_nodes__switchgear_center.png"),
    r("raw__left_full.png"),
    r("wire_nodes__left_full.png"),
    r("raw__center_full.png"),
    r("wire_nodes__center_full.png"),
    r("raw__right_full.png"),
    r("wire_nodes__right_full.png"),
    r("raw__dc_control_a.png"),
    r("wire_nodes__dc_control_a.png"),
    r("raw__dc_control_b.png"),
    r("wire_nodes__dc_control_b.png"),
    r("raw__title_notes_legend.png"),
]

DIEGO_ROUND3_IMAGES = [
    RAW,
    WIRE_NODES,
    r("raw__switchgear_center.png"),
    r("wire_nodes__switchgear_center.png"),
    r("raw__left_full.png"),
    r("wire_nodes__left_full.png"),
    r("raw__center_full.png"),
    r("wire_nodes__center_full.png"),
    r("raw__right_full.png"),
    r("wire_nodes__right_full.png"),
    r("raw__dc_control_a.png"),
    r("wire_nodes__dc_control_a.png"),
    r("raw__title_notes_legend.png"),
]


def read_if_exists(name: str) -> str:
    path = RESULTS / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


PROMPTS = {
    "main": """
Main Codex orchestration for document 8: inspect only the allowed folder, create crops, visually inspect raw and
derived aids, run Diego and Jennifer subagents through extraction/review/saturation, write all round matrices, validate
symmetry/diagonal/edge counts, and produce token accounting.
""",
    "diego1": """
Diego high-recall extraction prompt for document 8. Inspect raw schematic, detected component overlay, wire mask,
wire-node overlay, regional crops, notes, and legend. Propose stable node order, supported sparse edge list, evidence,
uncertain/excluded candidates, and label ambiguities. Do not use GT or outside files.
""",
    "jennifer2": """
Jennifer precision review prompt for document 8. Inspect raw/derived resources and review Diego's high-recall graph.
Remove unsupported or overconnected edges, add missed visible edges, and mark uncertainty. Focus on 480 V center tie,
EDG-C, DC charger/battery/bus, PN-to-120VAC taps, and dashed control/JB/K1/ESFAS/RPS paths.

Diego edge payload:
"""
    + read_if_exists("round_01_diego_high_recall_edges.csv"),
    "diego3": """
Diego final saturation prompt for document 8. Review Jennifer's patch: remove nine edges, add five edges, confirm
selected kept edges, and decide whether the Jennifer-patched graph is saturated. Return only final agreement or exact
remaining edge changes.

Final edge payload:
"""
    + read_if_exists("final_edges.csv"),
}


def make_row(
    call_order: int,
    caller: str,
    model_call: str,
    subagent_id: str,
    round_name: str,
    purpose: str,
    images: list[Path],
    prompt_text: str,
    output_low: int,
    output_expected: int,
    output_high: int,
    notes: str,
) -> dict[str, object]:
    image_low, image_expected, image_high, tile_reference = image_token_estimates(images)
    text_expected = text_tokens(prompt_text)
    text_low = max(1, int(text_expected * 0.85))
    text_high = int(text_expected * 1.2) + 300
    input_low = text_low + image_low
    input_expected = text_expected + image_expected
    input_high = text_high + image_high
    return {
        "document": 8,
        "iteration": 1,
        "call_order": call_order,
        "caller": caller,
        "model_call": model_call,
        "subagent_id": subagent_id,
        "round": round_name,
        "purpose": purpose,
        "input_text_tokens_low": text_low,
        "input_text_tokens_expected": text_expected,
        "input_text_tokens_high": text_high,
        "cached_input_tokens_recorded": "unavailable",
        "image_count": len(images),
        "image_file_input_tokens_low": image_low,
        "image_file_input_tokens_expected": image_expected,
        "image_file_input_tokens_high": image_high,
        "image_tile_high_reference_tokens": tile_reference,
        "file_input_tokens_est": 0,
        "input_tokens_low": input_low,
        "input_tokens_expected": input_expected,
        "input_tokens_high": input_high,
        "output_tokens_low": output_low,
        "output_tokens_expected": output_expected,
        "output_tokens_high": output_high,
        "reasoning_tokens_recorded": "unavailable",
        "usage_object_recorded": "unavailable in Codex main/subagent tool wrapper",
        "responses_input_tokens_endpoint_status": (
            "not_called_no_OPENAI_API_KEY" if not os.getenv("OPENAI_API_KEY") else "api_key_present_but_not_used_by_offline_estimator"
        ),
        "total_tokens_low": input_low + output_low,
        "total_tokens_expected": input_expected + output_expected,
        "total_tokens_high": input_high + output_high,
        "notes": notes,
    }


def main() -> None:
    rows = [
        make_row(
            1,
            "Main agent",
            "main_doc8_orchestration_aggregate",
            "n/a",
            "orchestration",
            "Folder inspection, crop creation, visual checks, subagent orchestration, artifact writing, validation.",
            MAIN_VIEWED_IMAGES,
            PROMPTS["main"],
            output_low=3500,
            output_expected=7000,
            output_high=14500,
            notes="Aggregate estimate; per-turn main-agent usage objects are not exposed.",
        ),
        make_row(
            2,
            "Diego",
            "diego_round_01_high_recall",
            "019f6770-ce87-7a42-9768-1a94458411e5",
            "round_01_high_recall",
            "High-recall visual extraction.",
            DIEGO_ROUND1_IMAGES,
            PROMPTS["diego1"],
            output_low=6500,
            output_expected=11000,
            output_high=18000,
            notes="Output unknown exactly; range based on 120-node/144-edge evidence payload.",
        ),
        make_row(
            3,
            "Jennifer",
            "jennifer_round_02_precision",
            "019f677a-5c19-7f80-af23-0ee457e6e389",
            "round_02_precision",
            "Precision patch review.",
            JENNIFER_ROUND2_IMAGES,
            PROMPTS["jennifer2"],
            output_low=1600,
            output_expected=3200,
            output_high=6000,
            notes="Output known qualitatively as a concise patch; exact token usage unavailable.",
        ),
        make_row(
            4,
            "Diego",
            "diego_round_03_saturation",
            "019f6785-c2b6-7d13-99d1-f1c13aa94333",
            "round_03_saturation",
            "Final reconciliation and saturation check.",
            DIEGO_ROUND3_IMAGES,
            PROMPTS["diego3"],
            output_low=300,
            output_expected=700,
            output_high=1500,
            notes="Saturation confirmed; visible final message was short.",
        ),
    ]

    out = RESULTS / "model_call_token_estimates.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)

    summary = [
        "# Document 8 Token Usage Estimate",
        "",
        "No `OPENAI_API_KEY` was present, so the official `POST /v1/responses/input_tokens` endpoint could not be called.",
        "Usage objects for the Codex main-agent/subagent wrapper calls were not exposed in this environment.",
        "",
        "Local method:",
        "- Text: `tiktoken` with `o200k_base` if available; otherwise deterministic `ceil(characters / 4)` fallback.",
        "- Image low: 70 tokens per image as a low-detail floor.",
        "- Image expected: `ceil(width / 32) * ceil(height / 32)` original patch count, matching GPT-5.6 `auto/original` guidance.",
        "- Image high: original patch count plus 15 percent and a small per-image overhead allowance.",
        "- `image_tile_high_reference_tokens` is included as a separate GPT-5 tile-based comparison column.",
        "",
        f"Total low estimate: {total_low:,} tokens",
        f"Total expected estimate: {total_expected:,} tokens",
        f"Total high estimate: {total_high:,} tokens",
        "",
        "See `model_call_token_estimates.csv` for per-call details.",
        "",
        "Official references:",
        "- https://developers.openai.com/api/docs/guides/token-counting",
        "- https://developers.openai.com/api/docs/guides/images-vision",
    ]
    (RESULTS / "token_usage_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(f"wrote {out}")
    print(f"total_low={total_low} total_expected={total_expected} total_high={total_high}")


if __name__ == "__main__":
    main()
