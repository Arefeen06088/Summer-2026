from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


def image_size(path: str) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


def gpt5_low_tokens(_: int, __: int) -> int:
    return 70


def gpt5_high_tile_tokens(width: int, height: int) -> int:
    # Official GPT-5 high-detail tile estimate:
    # fit in 2048 square, shrink shortest side to 768 if still larger, then
    # add 70 base tokens plus 140 per 512 px tile.
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


def original_patch_tokens(width: int, height: int) -> int:
    # Conservative high estimate for GPT-5.6 original/auto behavior: 32px patches
    # at original size, without a resize cap.
    return math.ceil(width / 32) * math.ceil(height / 32)


def image_token_estimates(paths: list[str]) -> tuple[int, int, int]:
    low = expected = high = 0
    for path in paths:
        width, height = image_size(path)
        low += gpt5_low_tokens(width, height)
        expected += gpt5_high_tile_tokens(width, height)
        high += original_patch_tokens(width, height)
    return low, expected, high


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


def p(name: str) -> str:
    return str(BASE / name)


def r(name: str) -> str:
    return str(RESULTS / name)


RAW = p("raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png")
DETECTED = p("detected_components_and_logical_overlay.png")
WIRE_NODES = p("wire_nodes_overlay.png")
WIRE_MASK = p("wires_mask_overlay.png")

DIEGO_ROUND1_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    r("raw__top_left_generator_switchyard.png"),
    r("raw__top_mid_switchyard.png"),
    r("raw__medium_voltage_left.png"),
    r("raw__medium_voltage_right.png"),
    r("raw__load_centers_left.png"),
    r("raw__load_centers_mid.png"),
    r("raw__load_centers_right.png"),
    r("raw__dc_ups_left.png"),
    r("raw__dc_ups_right.png"),
    r("raw__control_bay_full.png"),
    r("wire_nodes__control_bay_full.png"),
    r("raw__grounds_bottom.png"),
    r("raw__legend.png"),
    r("raw__notes.png"),
]

JENNIFER_ROUND2_IMAGES = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    r("raw__top_left_generator_switchyard.png"),
    r("detected__top_left_generator_switchyard.png"),
    r("raw__medium_voltage_left.png"),
    r("raw__medium_voltage_right.png"),
    r("raw__load_centers_left.png"),
    r("raw__load_centers_mid.png"),
    r("raw__load_centers_right.png"),
    r("raw__dc_ups_left.png"),
    r("raw__dc_ups_right.png"),
    r("raw__control_bay_with_inputs.png"),
    r("wire_nodes__control_bay_with_inputs.png"),
    r("raw__grounds_bottom.png"),
    r("raw__legend.png"),
]

DIEGO_ROUND3_IMAGES = [
    RAW,
    r("raw__top_left_generator_switchyard.png"),
    r("raw__medium_voltage_left.png"),
    r("raw__medium_voltage_right.png"),
    r("raw__load_centers_left.png"),
    r("raw__load_centers_mid.png"),
    r("raw__load_centers_right.png"),
    r("raw__dc_ups_left.png"),
    r("raw__dc_ups_right.png"),
    r("raw__control_bay_with_inputs.png"),
    r("raw__grounds_bottom.png"),
]

MAIN_VIEWED_IMAGES = [
    r("raw__dc_ups_right.png"),
    r("raw__control_bay_full.png"),
    r("wire_nodes__control_bay_full.png"),
    r("detected__top_left_generator_switchyard.png"),
    r("detected__medium_voltage_left.png"),
    r("detected__medium_voltage_right.png"),
    r("detected__load_centers_left.png"),
    r("detected__load_centers_right.png"),
    r("detected__load_centers_mid.png"),
    r("raw__grounds_bottom.png"),
    r("wire_nodes__grounds_bottom.png"),
    r("raw__control_bay_with_inputs.png"),
    r("wire_nodes__control_bay_with_inputs.png"),
    r("raw__top_left_generator_switchyard.png"),
    r("raw__close_ipb_cbgen_gsu.png"),
    r("raw__close_gen_ipb_cbgen.png"),
    r("detected__dc_ups_left.png"),
]

NODES_TEXT = (RESULTS / "final_node_order.csv").read_text(encoding="utf-8") if (RESULTS / "final_node_order.csv").exists() else ""
EDGES_TEXT = (RESULTS / "final_edges.csv").read_text(encoding="utf-8") if (RESULTS / "final_edges.csv").exists() else ""
UNCERTAIN_TEXT = (RESULTS / "uncertain_excluded_edges.csv").read_text(encoding="utf-8") if (RESULTS / "uncertain_excluded_edges.csv").exists() else ""

VISIBLE_TEXT = {
    "diego_round_1_high_recall": """
You are Diego, the high-recall extractor for document 6. Inspect only the provided raw schematic, detected overlay,
wire masks, wire nodes, crops, legend, and notes. Propose all visually/geometrically plausible components, labels,
logical nodes, and edges, with evidence. Output node order, supported edges, uncertain candidates, CSV matrix, and
label ambiguities. Do not use GT, internet, outside files, or OCR. Raw is authoritative; crossings without dots are
visual crossings only.
""",
    "jennifer_round_2_precision": f"""
You are Jennifer, precision reviewer/refiner for document 6. Inspect only the provided folder resources and review
Diego's high-recall proposal. Remove unsupported or overconnected edges, fix labels, and mark ambiguous cases
uncertain. Treat all conductor styles as possible connections, but obey no-dot crossings. Diego proposal node/edge
payload follows.

{NODES_TEXT}

{EDGES_TEXT}

Uncertain excluded candidates from Diego:
{UNCERTAIN_TEXT}
""",
    "diego_round_3_saturation": f"""
You are Diego, final reconciliation pass for document 6. Jennifer kept all 115 supported edges unchanged, confirmed
TPB-201 and CB-GEN-201, added no edges, and excluded dense/unsupported control candidates. Inspect the provided
resources again and state whether the graph has saturated. If yes, return SATURATED: yes, final node order, supported
edges, uncertain excluded edges, and state the matrix equals the refined graph if unchanged.

{NODES_TEXT}

{EDGES_TEXT}
""",
}


def call_row(
    call_order: int,
    caller: str,
    round_name: str,
    purpose: str,
    images: list[str],
    visible_text: str,
    output_expected: int,
    output_low: int | None = None,
    output_high: int | None = None,
    notes: str = "",
) -> dict[str, object]:
    image_low, image_expected, image_high = image_token_estimates(images)
    text_expected = text_tokens(visible_text)
    text_low = max(1, int(text_expected * 0.9))
    text_high = int(text_expected * 1.2) + 500
    output_low = output_low if output_low is not None else int(output_expected * 0.7)
    output_high = output_high if output_high is not None else int(output_expected * 1.35)
    return {
        "document": 6,
        "iteration": 1,
        "call_order": call_order,
        "caller": caller,
        "round": round_name,
        "purpose": purpose,
        "model": "inherited Codex/subagent model (exact API model not exposed)",
        "input_text_tokens_low": text_low,
        "input_text_tokens_expected": text_expected,
        "input_text_tokens_high": text_high,
        "cached_input_tokens_recorded": "unavailable",
        "image_count": len(images),
        "image_file_input_tokens_low": image_low,
        "image_file_input_tokens_expected": image_expected,
        "image_file_input_tokens_high": image_high,
        "file_input_tokens_est": 0,
        "output_tokens_low": output_low,
        "output_tokens_expected": output_expected,
        "output_tokens_high": output_high,
        "reasoning_tokens_recorded": "unavailable",
        "usage_object_recorded": "unavailable in Codex subagent/tool wrapper",
        "total_tokens_low": text_low + image_low + output_low,
        "total_tokens_expected": text_expected + image_expected + output_expected,
        "total_tokens_high": text_high + image_high + output_high,
        "notes": notes,
    }


def main() -> None:
    rows = [
        call_row(
            1,
            "Main agent",
            "orchestration_aggregate",
            "Resource inspection, crop creation, visual checks, subagent orchestration, artifact writing, final synthesis.",
            MAIN_VIEWED_IMAGES,
            "Aggregate main-agent visible context estimate. Includes inspected images and workflow text; excludes hidden system/developer/tool protocol overhead.",
            output_expected=12000,
            output_low=8000,
            output_high=22000,
            notes="Coarse aggregate because per-turn main-agent usage objects are not exposed.",
        ),
        call_row(
            2,
            "Diego",
            "round_01_high_recall",
            "High-recall visual extraction.",
            DIEGO_ROUND1_IMAGES,
            VISIBLE_TEXT["diego_round_1_high_recall"],
            output_expected=7600,
            output_low=5200,
            output_high=10500,
            notes="Visible prompt plus image estimate; actual usage object unavailable.",
        ),
        call_row(
            3,
            "Jennifer",
            "round_02_precision",
            "Precision review/refinement of Diego proposal.",
            JENNIFER_ROUND2_IMAGES,
            VISIBLE_TEXT["jennifer_round_2_precision"],
            output_expected=1100,
            output_low=700,
            output_high=2200,
            notes="Visible prompt includes generated node/edge payload, not hidden wrapper tokens.",
        ),
        call_row(
            4,
            "Diego",
            "round_03_saturation",
            "Final reconciliation and saturation check.",
            DIEGO_ROUND3_IMAGES,
            VISIBLE_TEXT["diego_round_3_saturation"],
            output_expected=3000,
            output_low=1800,
            output_high=5000,
            notes="Saturation confirmed; matrix unchanged.",
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
    summary_path = RESULTS / "token_usage_summary.md"
    summary_path.write_text(
        "\n".join(
            [
                "# Document 6 Token Usage Estimate",
                "",
                "No `OPENAI_API_KEY` was present, so `/v1/responses/input_tokens` could not be called.",
                "Usage objects for Codex main-agent/subagent wrapper calls were not exposed by the tool environment.",
                "",
                "Local method:",
                "- Text: `tiktoken` with `o200k_base` when available; deterministic `ceil(characters/4)` fallback if local encoder data cannot load.",
                "- Image low estimate: GPT-5 low-detail base, 70 tokens/image.",
                "- Image expected estimate: GPT-5 high-detail tile formula, 70 base + 140 per 512px tile after documented resizing.",
                "- Image high estimate: 32px original patch count, a conservative proxy for GPT-5.6 original/auto behavior on large images.",
                "",
                f"Total low estimate: {total_low:,} tokens",
                f"Total expected estimate: {total_expected:,} tokens",
                f"Total high estimate: {total_high:,} tokens",
                "",
                "See `model_call_token_estimates.csv` for per-call details.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print(f"total_low={total_low} total_expected={total_expected} total_high={total_high}")


if __name__ == "__main__":
    main()
