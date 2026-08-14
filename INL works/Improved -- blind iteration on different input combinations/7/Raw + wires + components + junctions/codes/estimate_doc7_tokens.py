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
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_clean (1).png"
DETECTED = BASE / "detected_components_and_logical_overlay.png"
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
    # GPT-5 low-detail floor from the public vision guide.
    return 70


def image_tile_high_tokens(width: int, height: int) -> int:
    # GPT-5 tile-based high-detail reference: fit in 2048 square, then make
    # the shortest side 768px and count 512px tiles.
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
    # GPT-5.6 original/auto behavior: 32px patches at original dimensions.
    return math.ceil(width / 32) * math.ceil(height / 32)


def image_token_estimates(paths: list[Path]) -> tuple[int, int, int, int]:
    low = expected = high = tile_reference = 0
    for path in paths:
        width, height = image_size(path)
        low += image_low_tokens(width, height)
        patch_tokens = image_original_patch_tokens(width, height)
        expected += patch_tokens
        high += math.ceil(patch_tokens * 1.15) + 50
        tile_reference += image_tile_high_tokens(width, height)
    return low, expected, high, tile_reference


DIEGO_ROUND1_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    r("raw__top_left_sources.png"),
    r("detected__top_left_sources.png"),
    r("raw__top_mid_buses.png"),
    r("detected__top_mid_buses.png"),
    r("raw__top_right_sources.png"),
    r("detected__top_right_sources.png"),
    r("raw__load_centers_left.png"),
    r("detected__load_centers_left.png"),
    r("raw__load_centers_right.png"),
    r("detected__load_centers_right.png"),
    r("raw__dc_control_left.png"),
    r("wire_nodes__dc_control_left.png"),
    r("raw__dc_control_right.png"),
    r("wire_nodes__dc_control_right.png"),
    r("raw__control_bottom_cross.png"),
    r("wire_nodes__control_bottom_cross.png"),
    r("raw__notes.png"),
    r("raw__legend.png"),
    r("raw__title_block.png"),
]

JENNIFER_ROUND2_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    r("raw__top_left_sources.png"),
    r("raw__top_mid_buses.png"),
    r("raw__top_right_sources.png"),
    r("raw__load_centers_left.png"),
    r("raw__load_centers_right.png"),
    r("raw__dc_control_left.png"),
    r("wire_nodes__dc_control_left.png"),
    r("raw__dc_control_right.png"),
    r("wire_nodes__dc_control_right.png"),
    r("raw__control_bottom_cross.png"),
    r("wire_nodes__control_bottom_cross.png"),
    r("raw__notes.png"),
    r("raw__legend.png"),
]

DIEGO_ROUND3_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    r("raw__dc_control_left.png"),
    r("wire_nodes__dc_control_left.png"),
    r("raw__dc_control_right.png"),
    r("wire_nodes__dc_control_right.png"),
    r("raw__control_bottom_cross.png"),
    r("wire_nodes__control_bottom_cross.png"),
    r("raw__top_mid_buses.png"),
    r("wire_nodes__top_mid_buses.png"),
    r("raw__notes.png"),
    r("raw__legend.png"),
]

MAIN_VIEWED_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    r("raw__notes.png"),
    r("raw__legend.png"),
    r("detected__top_left_sources.png"),
    r("detected__top_mid_buses.png"),
    r("detected__top_right_sources.png"),
    r("detected__load_centers_left.png"),
    r("detected__load_centers_right.png"),
    r("detected__dc_control_left.png"),
    r("detected__dc_control_right.png"),
    r("wire_nodes__dc_control_left.png"),
    r("wire_nodes__dc_control_right.png"),
    r("raw__top_left_sources.png"),
    r("raw__top_mid_buses.png"),
    r("raw__top_right_sources.png"),
    r("raw__load_centers_left.png"),
    r("raw__load_centers_right.png"),
    r("raw__control_bottom_cross.png"),
    r("wire_nodes__control_bottom_cross.png"),
]


def read_if_exists(name: str) -> str:
    path = RESULTS / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


PROMPTS = {
    "main_agent_aggregate": """
Main Codex orchestration for document 7: inspect resource inventory, create visual crops, coordinate Diego/Jennifer
subagents, review the saturated result, write CSV matrices for all rounds, validate matrix shape/symmetry, create token
accounting artifacts, and summarize results to the user. This is an aggregate estimate because per-turn main-agent
usage objects are not exposed by the local Codex tool wrapper.
""",
    "diego_round_1_high_recall": """
You are Diego, the high-recall extractor for document 7. Inspect only resources in Raw + wires + components +
junctions. Use the raw schematic as authoritative and derived masks/overlays/crops as aids. Propose every
visually/geometrically plausible component, label, logical node, and edge with evidence. Do not use GT, GT-derived
feedback, internet, outside folders, or off-the-shelf OCR. Output node order, supported edges, uncertain candidates,
and a connectivity matrix.
""",
    "jennifer_round_2_precision": """
You are Jennifer, the precision reviewer for document 7. Inspect the same raw and derived resources and review Diego's
high-recall extraction. Remove unsupported or overconnected edges, fix visually supported component labels, and mark
ambiguous cases uncertain instead of guessing. Diagram notes say crossings without dots are not electrically connected.

Diego proposal payload:
"""
    + read_if_exists("round_01_diego_high_recall_edges.csv")
    + "\n"
    + read_if_exists("final_node_order.csv"),
    "diego_round_3_saturation": """
You are Diego, final reconciliation for document 7. Jennifer removed BAT-125A--BCHG-125A, BAT-125B--BCHG-125B,
PNL-AC-CR1--RELAY-K101, and PNL-AC-CR2--RELAY-K201, and added RELAY-K101--SR-101. Inspect the key raw/derived
images again and say whether the Jennifer-refined graph is saturated/final. If not, list only exact edge changes.

Jennifer-refined final graph:
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
        "document": 7,
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
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = [
        make_row(
            1,
            "Main agent",
            "main_doc7_orchestration_aggregate",
            "n/a",
            "orchestration",
            "Resource inspection, crop generation, subagent coordination, artifact writing, validation, final answer.",
            MAIN_VIEWED_IMAGES,
            PROMPTS["main_agent_aggregate"],
            output_low=3000,
            output_expected=6500,
            output_high=14000,
            notes="Aggregate estimate; the runtime does not expose individual main-agent usage objects.",
        ),
        make_row(
            2,
            "Diego",
            "diego_round_01_high_recall",
            "019f6760-0285-7552-8dce-401f8ea2b625",
            "round_01_high_recall",
            "High-recall visual extraction with evidence.",
            DIEGO_ROUND1_IMAGES,
            PROMPTS["diego_round_1_high_recall"],
            output_low=5500,
            output_expected=9000,
            output_high=15000,
            notes="Output unknown after-the-fact; range based on node/edge/evidence payload size.",
        ),
        make_row(
            3,
            "Jennifer",
            "jennifer_round_02_precision",
            "019f6765-22c5-7d91-af9c-e74986b91fda",
            "round_02_precision",
            "Precision review/refinement of Diego proposal.",
            JENNIFER_ROUND2_IMAGES,
            PROMPTS["jennifer_round_2_precision"],
            output_low=2200,
            output_expected=4500,
            output_high=8500,
            notes="Output unknown after-the-fact; range based on refined edge list and rationale.",
        ),
        make_row(
            4,
            "Diego",
            "diego_round_03_saturation",
            "019f676a-41ea-79e0-897f-56e660058e53",
            "round_03_saturation",
            "Final reconciliation and saturation check.",
            DIEGO_ROUND3_IMAGES,
            PROMPTS["diego_round_3_saturation"],
            output_low=250,
            output_expected=550,
            output_high=1200,
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
        "# Document 7 Token Usage Estimate",
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
