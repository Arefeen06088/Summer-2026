from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except ImportError:  # pragma: no cover
    tiktoken = None


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires + junctions")
RESULTS = BASE / "results"
CROPS = RESULTS / "inspection_crops"

RAW = BASE / "raw -- synthetic diagram _.png"
WIRE_OVERLAY = BASE / "wires_mask_overlay.png"
NODE_OVERLAY = BASE / "wire_nodes_overlay.png"
WIRE_NODES = BASE / "wire_nodes.csv"

SUBAGENT_R1_IMAGES = [
    RAW,
    WIRE_OVERLAY,
    NODE_OVERLAY,
    CROPS / "raw_startup_source_top_left.png",
    CROPS / "raw_top_intertrain_sources.png",
    CROPS / "raw_train_A_full.png",
    CROPS / "raw_train_B_full.png",
    CROPS / "raw_train_C_full.png",
    CROPS / "raw_train_D_full.png",
    CROPS / "raw_train_A_loads_left.png",
    CROPS / "raw_train_A_loads_right_dc.png",
    CROPS / "raw_train_B_loads_left.png",
    CROPS / "raw_train_B_loads_right_dc.png",
    CROPS / "raw_train_C_loads_left.png",
    CROPS / "raw_train_C_loads_right_dc.png",
    CROPS / "raw_train_D_loads_left.png",
    CROPS / "raw_train_D_loads_right_dc.png",
    CROPS / "raw_bottom_grounding_shared.png",
    CROPS / "raw_center_vertical_ties.png",
    CROPS / "nodes_center_vertical_ties.png",
    CROPS / "wires_center_vertical_ties.png",
]

MAIN_VIEWED_IMAGES = [
    RAW,
    CROPS / "raw_startup_source_top_left.png",
    CROPS / "raw_top_intertrain_sources.png",
    CROPS / "raw_train_A_full.png",
    CROPS / "raw_train_D_full.png",
    CROPS / "raw_bottom_grounding_shared.png",
    CROPS / "raw_center_vertical_ties.png",
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
    if not path.exists():
        return 0
    return text_tokens(path.read_text(encoding="utf-8", errors="replace"))


def expected_image_tokens(path: Path) -> int:
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


def high_image_tokens(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)


def image_bundle(paths: list[Path]) -> tuple[int, int, int]:
    existing = [path for path in paths if path.exists()]
    return (
        85 * len(existing),
        sum(expected_image_tokens(path) for path in existing),
        sum(high_image_tokens(path) for path in existing),
    )


def prompt_tokens(text: str) -> int:
    return text_tokens(text)


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
    img_low, img_exp, img_high = image_tokens
    cached_low, cached_exp, cached_high = cached_tokens
    out_low, out_exp, out_high = output_tokens
    reason_low, reason_exp, reason_high = reasoning_tokens
    in_low = text_in + img_low + cached_low
    in_exp = text_in + img_exp + cached_exp
    in_high = text_in + img_high + cached_high
    rows.append(
        {
            "document": 13,
            "iteration": 1,
            "call_id": call_id,
            "agent": agent,
            "model": model,
            "round": round_name,
            "call_type": call_type,
            "input_tokens_low": in_low,
            "input_tokens_expected": in_exp,
            "input_tokens_high": in_high,
            "input_text_tokens_est": text_in,
            "image_file_input_tokens_low": img_low,
            "image_file_input_tokens_expected": img_exp,
            "image_file_input_tokens_high": img_high,
            "cached_input_tokens_low": cached_low,
            "cached_input_tokens_expected": cached_exp,
            "cached_input_tokens_high": cached_high,
            "output_tokens_low": out_low,
            "output_tokens_expected": out_exp,
            "output_tokens_high": out_high,
            "reasoning_tokens_low": reason_low,
            "reasoning_tokens_expected": reason_exp,
            "reasoning_tokens_high": reason_high,
            "total_tokens_low": in_low + out_low + reason_low,
            "total_tokens_expected": in_exp + out_exp + reason_exp,
            "total_tokens_high": in_high + out_high + reason_high,
            "usage_object_available": "no",
            "notes": notes,
        }
    )
    return in_low, in_exp, in_high


def main() -> None:
    rows: list[dict[str, object]] = []
    image_tokens = image_bundle(SUBAGENT_R1_IMAGES)
    diego_r1_text = prompt_tokens("Diego high-recall extractor prompt for document 13 with raw and visual aids.") + file_text_tokens(WIRE_NODES)
    diego_r1_output = file_text_tokens(RESULTS / "diego_round1_output.txt")
    diego_r1_input = add_row(
        rows,
        "main_to_diego_round1_send_input",
        "Diego",
        "gpt-5.5",
        "Diego round 1",
        "send_input_reused_agent",
        diego_r1_text,
        image_tokens,
        (0, 0, 0),
        (diego_r1_output, diego_r1_output, diego_r1_output),
        (2_000, 8_000, 20_000),
        "Subagent thread reused because spawn limit was reached; actual usage object unavailable.",
    )

    jennifer_r1_text = prompt_tokens("Jennifer precision reviewer prompt for document 13 against Diego round 1.") + file_text_tokens(RESULTS / "diego_round1_output.txt")
    jennifer_r1_output = file_text_tokens(RESULTS / "jennifer_round1_review.txt")
    jennifer_r1_input = add_row(
        rows,
        "main_to_jennifer_round1_send_input",
        "Jennifer",
        "gpt-5.5",
        "Jennifer round 1",
        "send_input_reused_agent",
        jennifer_r1_text,
        image_tokens,
        (0, 0, 0),
        (jennifer_r1_output, jennifer_r1_output, jennifer_r1_output),
        (2_000, 7_000, 18_000),
        "Includes Diego round-1 proposal as file-text input estimate.",
    )

    diego_r2_text = prompt_tokens("Diego round 2 prompt to review Jennifer round 1 and saturate or revise.") + file_text_tokens(RESULTS / "jennifer_round1_review.txt")
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
        "Continuation call; cached-token range estimates possible prior Diego context reuse.",
    )

    jennifer_r2_text = prompt_tokens("Jennifer round 2 final prompt to confirm or correct final graph.") + file_text_tokens(RESULTS / "diego_round2_response.txt")
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
        "Continuation call; cached-token range estimates possible prior Jennifer context reuse.",
    )

    main_text = (
        prompt_tokens("Document 13 main-agent orchestration and report generation.")
        + file_text_tokens(WIRE_NODES)
        + file_text_tokens(RESULTS / "diego_round1_output.txt")
        + file_text_tokens(RESULTS / "jennifer_round1_review.txt")
        + file_text_tokens(RESULTS / "diego_round2_response.txt")
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
        image_bundle(MAIN_VIEWED_IMAGES),
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
    total_exp = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)
    md_path = RESULTS / "token_usage_estimate.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate - Document 13, Iteration 1\n\n")
        handle.write("No OpenAI API key was available, and the multi-agent tool did not expose usage objects. ")
        handle.write("Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. ")
        handle.write("Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.\n\n")
        handle.write("| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |\n")
        handle.write("|---:|---:|---|---|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            handle.write(
                f"| {row['document']} | {row['iteration']} | {row['round']} | {row['agent']} | "
                f"{row['input_tokens_expected']} | {row['cached_input_tokens_expected']} | "
                f"{row['image_file_input_tokens_expected']} | {row['output_tokens_expected']} | "
                f"{row['reasoning_tokens_expected']} | {row['total_tokens_expected']} |\n"
            )
        handle.write("\n")
        handle.write(f"Low total estimate: {total_low}\n\n")
        handle.write(f"Expected total estimate: {total_exp}\n\n")
        handle.write(f"High total estimate: {total_high}\n")

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    print({"total_low": total_low, "total_expected": total_exp, "total_high": total_high})


if __name__ == "__main__":
    main()
