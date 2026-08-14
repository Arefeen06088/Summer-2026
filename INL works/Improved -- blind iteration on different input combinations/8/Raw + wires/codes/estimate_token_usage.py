from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires"
)
RESULTS = ROOT / "results"


def text_tokens(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def high_detail_image_tokens(path: Path) -> tuple[int, int, int, int]:
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


RAW = p("raw -- synthetic_npp_schematic_improved_local_refined_v3.png")
MASK = p("wires_mask.png")
OVERLAY = p("wires_mask_overlay.png")

COMMON = """
Document 8 connectivity extraction from Raw + wires only. No ground truth,
no GT-derived feedback, and no OCR engines. Matrix is undirected and symmetric
with identical row/column node order.
"""

DIEGO_R1 = COMMON + """
High-recall extraction from full raw schematic, wire mask, and overlay. Identify
all visually plausible components, labels, nodes, accepted edges, and uncertain
edges with evidence.
"""

JENNIFER_R1 = COMMON + """
Precision review of Diego R1. Review node list and long accepted edge list with
full image and crops. Remove overconnections, promote visually supported
uncertain edges, and hold ambiguous raceway/control links out.
"""

DIEGO_R2 = COMMON + """
Targeted saturation check of Jennifer R1 deltas: B charger source, A MCC-2C
to PUMP-CHG-2A, B PN-480-B to VLV-HV-302B, removed PN-480-B to CHGR-125B,
removed JB-2B1 to CP-ESFAS-B, and remaining ambiguous dashed controls.
"""

MAIN = COMMON + """
Main Codex orchestration: inventory files, generate crops, inspect raw/crops,
spawn Diego/Jennifer subagents, reconcile saturation, write round matrices,
QA files, final matrix, and token estimates. This row is an aggregate estimate;
the runtime does not expose a single main-agent usage object here.
"""

CALLS = [
    CallEstimate(
        "8",
        "1",
        "main",
        "main_agent_orchestration_aggregate",
        "main",
        "gpt-5-codex",
        "not_exposed",
        "Main orchestration, crop inspection, artifact generation, and final reporting.",
        MAIN * 5,
        (
            RAW,
            c("raw_08_notes_legend_title.png"),
            c("raw_01_top_4160_sources.png"),
            c("raw_02_mid_4160_buses_dg.png"),
            c("raw_03_left_480_loads.png"),
            c("raw_04_right_480_loads.png"),
            c("raw_05_train_a_dc_ups_control.png"),
            c("raw_06_train_b_dc_ups_control.png"),
            c("raw_11_center_ties.png"),
            c("overlay_03_left_480_loads.png"),
            c("overlay_04_right_480_loads.png"),
            c("raw_16_train_a_load_control_detail.png"),
            c("raw_17_train_b_load_control_detail.png"),
        ),
        900,
        1600,
        2600,
        1500,
        4500,
        9000,
    ),
    CallEstimate(
        "8",
        "1",
        "round1_diego",
        "subagent_019f6e53-4085-7763-bb73-be62447a1d7b",
        "Diego",
        "gpt-5.5",
        "xhigh",
        "High-recall extraction from raw, mask, and overlay.",
        DIEGO_R1 * 5,
        (RAW, MASK, OVERLAY),
        2200,
        3800,
        5600,
        3500,
        9000,
        18000,
    ),
    CallEstimate(
        "8",
        "1",
        "round1_jennifer",
        "subagent_019f6e5c-b531-7ad2-b3e6-bf379e43106a",
        "Jennifer",
        "gpt-5.5",
        "xhigh",
        "Precision review of Diego R1 with full images and selected crops.",
        JENNIFER_R1 * 10,
        (
            RAW,
            OVERLAY,
            c("raw_01_top_4160_sources.png"),
            c("raw_02_mid_4160_buses_dg.png"),
            c("raw_03_left_480_loads.png"),
            c("raw_04_right_480_loads.png"),
            c("raw_05_train_a_dc_ups_control.png"),
            c("raw_06_train_b_dc_ups_control.png"),
            c("raw_07_lower_cross_controls.png"),
            c("raw_08_notes_legend_title.png"),
            c("raw_11_center_ties.png"),
            c("raw_16_train_a_load_control_detail.png"),
            c("raw_17_train_b_load_control_detail.png"),
        ),
        1800,
        3000,
        4500,
        3500,
        8500,
        17000,
    ),
    CallEstimate(
        "8",
        "1",
        "round2_diego_saturation",
        "subagent_019f6e64-cf81-7af3-ba94-1de550c88667",
        "Diego",
        "gpt-5.5",
        "xhigh",
        "Targeted saturation check of Jennifer R1 deltas.",
        DIEGO_R2 * 8,
        (
            RAW,
            OVERLAY,
            c("raw_02_mid_4160_buses_dg.png"),
            c("raw_03_left_480_loads.png"),
            c("raw_04_right_480_loads.png"),
            c("raw_05_train_a_dc_ups_control.png"),
            c("raw_06_train_b_dc_ups_control.png"),
            c("raw_07_lower_cross_controls.png"),
            c("overlay_03_left_480_loads.png"),
            c("overlay_04_right_480_loads.png"),
            c("raw_11_center_ties.png"),
        ),
        250,
        450,
        800,
        2500,
        6500,
        13000,
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
    with (RESULTS / "token_usage_estimate.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    totals = {
        "document": "8",
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
            "Text tokens estimated with tiktoken o200k_base when installed, "
            "otherwise characters/4. Image input estimated with the high-detail "
            "85 + 170*512px tile heuristic after resizing. Usage/cached/reasoning "
            "objects were not exposed by the local Codex/subagent runtime."
        ),
    }
    (RESULTS / "token_usage_totals.json").write_text(
        json.dumps(totals, indent=2),
        encoding="utf-8",
    )

    summary = [
        "# Token Usage Estimate - Document 8",
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
