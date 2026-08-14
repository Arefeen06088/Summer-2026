from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except ImportError:  # pragma: no cover
    tiktoken = None


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + wires + junctions")
RESULTS = BASE / "results"
CROPS = RESULTS / "inspection_crops"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png"
WIRE_OVERLAY = BASE / "wires_mask_overlay.png"
NODE_OVERLAY = BASE / "wire_nodes_overlay.png"
WIRE_NODES = BASE / "wire_nodes.csv"

SUBAGENT_R1_IMAGES = [
    RAW,
    WIRE_OVERLAY,
    NODE_OVERLAY,
    CROPS / "raw__top_left_offsite.png",
    CROPS / "raw__top_center_generator_aux.png",
    CROPS / "raw__top_right_offsite.png",
    CROPS / "raw__aux_bus_tie.png",
    CROPS / "raw__train_a.png",
    CROPS / "raw__train_b.png",
    CROPS / "raw__train_c.png",
    CROPS / "raw__train_d.png",
    CROPS / "raw__dc_ups_a.png",
    CROPS / "raw__dc_ups_b.png",
    CROPS / "raw__bottom_power_control.png",
    CROPS / "raw__protection_control.png",
    CROPS / "raw__legend_notes.png",
    CROPS / "nodes_overlay__train_a.png",
    CROPS / "nodes_overlay__train_c.png",
    CROPS / "nodes_overlay__protection_control.png",
    CROPS / "nodes_overlay__bottom_power_control.png",
]

MAIN_VIEWED_IMAGES = [
    RAW,
    CROPS / "raw__top_center_generator_aux.png",
    CROPS / "raw__train_a.png",
    CROPS / "raw__train_c.png",
    CROPS / "raw__dc_ups_a.png",
    CROPS / "raw__bottom_power_control.png",
    CROPS / "raw__protection_control.png",
    CROPS / "raw__top_left_offsite.png",
    CROPS / "raw__top_right_offsite.png",
    CROPS / "raw__aux_bus_tie.png",
    CROPS / "raw__train_b.png",
    CROPS / "raw__train_d.png",
    CROPS / "raw__dc_ups_b.png",
    CROPS / "nodes_overlay__train_a.png",
    CROPS / "nodes_overlay__train_c.png",
    CROPS / "nodes_overlay__protection_control.png",
    CROPS / "nodes_overlay__bottom_power_control.png",
    BASE / "wires_mask.png",
    CROPS / "wires_overlay__train_a.png",
    CROPS / "wires_overlay__protection_control.png",
    CROPS / "wires_overlay__bottom_power_control.png",
]


def encoding():
    if tiktoken is None:
        return None
    try:
        return tiktoken.get_encoding("o200k_base")
    except Exception:
        try:
            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None


ENCODING = encoding()


def text_tokens(text: str) -> int:
    if ENCODING is None:
        return math.ceil(len(text) / 4)
    return len(ENCODING.encode(text))


def file_text_tokens(path: Path) -> int:
    return text_tokens(path.read_text(encoding="utf-8", errors="replace"))


def prompt_tokens(*parts: str) -> int:
    return text_tokens("\n\n".join(parts))


def high_detail_expected_image_tokens(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    scale = min(2048 / w, 2048 / h, 1.0)
    w2, h2 = w * scale, h * scale
    shortest = min(w2, h2)
    if shortest > 768:
        scale2 = 768 / shortest
        w2, h2 = w2 * scale2, h2 * scale2
    tiles = math.ceil(w2 / 512) * math.ceil(h2 / 512)
    return 85 + 170 * tiles


def high_bound_image_tokens(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def image_token_bundle(paths: list[Path]) -> tuple[int, int, int]:
    existing = [path for path in paths if path.exists()]
    low = 85 * len(existing)
    expected = sum(high_detail_expected_image_tokens(path) for path in existing)
    high = sum(high_bound_image_tokens(path) for path in existing)
    return low, expected, high


def add_row(
    rows: list[dict[str, object]],
    call_id: str,
    agent: str,
    model: str,
    round_name: str,
    call_type: str,
    text_in: int,
    image_tokens: tuple[int, int, int],
    cached_tokens: tuple[int, int, int],
    output_tokens: tuple[int, int, int],
    reasoning_tokens: tuple[int, int, int],
    notes: str,
) -> tuple[int, int, int]:
    image_low, image_expected, image_high = image_tokens
    cached_low, cached_expected, cached_high = cached_tokens
    output_low, output_expected, output_high = output_tokens
    reasoning_low, reasoning_expected, reasoning_high = reasoning_tokens
    input_low = text_in + image_low + cached_low
    input_expected = text_in + image_expected + cached_expected
    input_high = text_in + image_high + cached_high
    rows.append(
        {
            "document": 5,
            "iteration": 1,
            "call_id": call_id,
            "agent": agent,
            "model": model,
            "round": round_name,
            "call_type": call_type,
            "input_tokens_low": input_low,
            "input_tokens_expected": input_expected,
            "input_tokens_high": input_high,
            "input_text_tokens_est": text_in,
            "image_file_input_tokens_low": image_low,
            "image_file_input_tokens_expected": image_expected,
            "image_file_input_tokens_high": image_high,
            "cached_input_tokens_low": cached_low,
            "cached_input_tokens_expected": cached_expected,
            "cached_input_tokens_high": cached_high,
            "output_tokens_low": output_low,
            "output_tokens_expected": output_expected,
            "output_tokens_high": output_high,
            "reasoning_tokens_low": reasoning_low,
            "reasoning_tokens_expected": reasoning_expected,
            "reasoning_tokens_high": reasoning_high,
            "total_tokens_low": input_low + output_low + reasoning_low,
            "total_tokens_expected": input_expected + output_expected + reasoning_expected,
            "total_tokens_high": input_high + output_high + reasoning_high,
            "usage_object_available": "no",
            "notes": notes,
        }
    )
    return input_low, input_expected, input_high


def main() -> None:
    rows: list[dict[str, object]] = []

    user_request_summary = (
        "Document 5 connectivity extraction request with Diego high-recall and Jennifer "
        "precision reviewer, one blind iteration, no GT/GT-derived feedback, no OCR, "
        "store codes/results, estimate token usage."
    )

    diego_r1_prompt = (
        "Diego high-recall extractor prompt: inspect raw schematic and visual aids only, "
        "propose plausible components, labels, logical nodes, edges, evidence, ambiguities, "
        "and a symmetric connectivity matrix."
    )
    jennifer_r1_prompt = (
        "Jennifer precision reviewer prompt: inspect Diego round-1 proposal and visual "
        "resources, remove unsupported edges, fix labels, mark ambiguity, output revised "
        "node order, edge list, notes, and matrix."
    )
    diego_r2_prompt = (
        "Diego round 2 prompt: review Jennifer round-1 removals and changes against the "
        "same allowed resources, reinstate only visually supported edges, report saturation."
    )
    jennifer_r2_prompt = (
        "Jennifer round 2 final prompt: review Diego agreement, make final precision "
        "correction if needed, output final node order, edge list, ambiguity notes, matrix."
    )

    subagent_images = image_token_bundle(SUBAGENT_R1_IMAGES)

    diego_r1_text = prompt_tokens(diego_r1_prompt) + file_text_tokens(WIRE_NODES)
    diego_r1_output = file_text_tokens(RESULTS / "inspection_crops" / "proposed_graph_output.txt")
    diego_r1_input = add_row(
        rows,
        "main_to_diego_round1_spawn",
        "Diego",
        "gpt-5.5",
        "Diego round 1",
        "spawn_agent",
        diego_r1_text,
        subagent_images,
        (0, 0, 0),
        (diego_r1_output, diego_r1_output, diego_r1_output),
        (2_000, 8_000, 20_000),
        "Actual usage object unavailable; output tokens estimated from written transcript.",
    )

    jennifer_r1_text = prompt_tokens(jennifer_r1_prompt) + file_text_tokens(RESULTS / "inspection_crops" / "proposed_graph_output.txt")
    jennifer_r1_output = file_text_tokens(RESULTS / "jennifer_round1_review.txt")
    jennifer_r1_input = add_row(
        rows,
        "main_to_jennifer_round1_spawn",
        "Jennifer",
        "gpt-5.5",
        "Jennifer round 1",
        "spawn_agent",
        jennifer_r1_text,
        subagent_images,
        (0, 0, 0),
        (jennifer_r1_output, jennifer_r1_output, jennifer_r1_output),
        (2_000, 7_000, 18_000),
        "Includes Diego round-1 proposal as file-text input estimate.",
    )

    diego_r2_text = prompt_tokens(diego_r2_prompt) + file_text_tokens(RESULTS / "jennifer_round1_review.txt")
    diego_r2_output = file_text_tokens(RESULTS / "diego_round2_response.txt")
    add_row(
        rows,
        "main_to_diego_round2_send_input",
        "Diego",
        "gpt-5.5",
        "Diego round 2",
        "send_input",
        diego_r2_text,
        (0, 0, 0),
        (0, diego_r1_input[1] + diego_r1_output, diego_r1_input[2] + diego_r1_output),
        (diego_r2_output, diego_r2_output, diego_r2_output),
        (500, 1_500, 5_000),
        "Continuation call; cached-token range estimates prior Diego context reuse.",
    )

    jennifer_r2_text = prompt_tokens(jennifer_r2_prompt) + file_text_tokens(RESULTS / "diego_round2_response.txt")
    jennifer_r2_output = file_text_tokens(RESULTS / "jennifer_round2_final.txt")
    add_row(
        rows,
        "main_to_jennifer_round2_send_input",
        "Jennifer",
        "gpt-5.5",
        "Jennifer round 2 final",
        "send_input",
        jennifer_r2_text,
        (0, 0, 0),
        (0, jennifer_r1_input[1] + jennifer_r1_output, jennifer_r1_input[2] + jennifer_r1_output),
        (jennifer_r2_output, jennifer_r2_output, jennifer_r2_output),
        (1_000, 3_000, 8_000),
        "Continuation call; cached-token range estimates prior Jennifer context reuse.",
    )

    main_text = (
        prompt_tokens(user_request_summary)
        + file_text_tokens(WIRE_NODES)
        + file_text_tokens(RESULTS / "inspection_crops" / "proposed_graph_output.txt")
        + file_text_tokens(RESULTS / "jennifer_round1_review.txt")
        + file_text_tokens(RESULTS / "jennifer_round2_final.txt")
    )
    add_row(
        rows,
        "main_agent_orchestration_aggregate",
        "Main Codex agent",
        "not exposed",
        "All rounds",
        "aggregate_estimate",
        main_text,
        image_token_bundle(MAIN_VIEWED_IMAGES),
        (0, 0, 0),
        (800, 1_800, 4_000),
        (1_000, 4_000, 12_000),
        "Aggregate only: individual main-agent model-call usage is not exposed in this environment.",
    )

    csv_path = RESULTS / "token_usage_estimate.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)

    md_path = RESULTS / "token_usage_estimate.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate - Document 5, Iteration 1\n\n")
        handle.write("No OpenAI API key was available, and the multi-agent tool did not expose usage objects. ")
        if ENCODING is None:
            handle.write("The local tiktoken package could not initialize an encoding in this environment, so text tokens were estimated with len(text)/4. ")
        else:
            handle.write("Text tokens were estimated locally with tiktoken. ")
        handle.write("Image/file token estimates use a low thumbnail bound, an expected high-detail tile estimate after resizing, and a high no-resize tile bound.\n\n")
        handle.write("| Call | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |\n")
        handle.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            handle.write(
                f"| {row['round']} | {row['agent']} | {row['input_tokens_expected']} | "
                f"{row['cached_input_tokens_expected']} | {row['image_file_input_tokens_expected']} | "
                f"{row['output_tokens_expected']} | {row['reasoning_tokens_expected']} | "
                f"{row['total_tokens_expected']} |\n"
            )
        handle.write("\n")
        handle.write(f"Low total estimate: {total_low}\n\n")
        handle.write(f"Expected total estimate: {total_expected}\n\n")
        handle.write(f"High total estimate: {total_high}\n")

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    print({"total_low": total_low, "total_expected": total_expected, "total_high": total_high})


if __name__ == "__main__":
    main()
