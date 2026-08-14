from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except ImportError:  # pragma: no cover
    tiktoken = None


DOC = 25
ITERATION = 1
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\25\Raw + wires + junctions"
)
RESULTS = BASE / "results"
FALLBACK = Path(r"C:\Asif_all_python_projects\INL\INL\doc25_work")
RESULT_CROPS = RESULTS / "inspection_crops"
FALLBACK_CROPS = FALLBACK / "inspection_crops"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_revised_v4.png"
WIRE_OVERLAY = BASE / "wires_mask_overlay.png"
NODE_OVERLAY = BASE / "wire_nodes_overlay.png"
WIRE_NODES = BASE / "wire_nodes.csv"

R1_IMAGE_NAMES = [
    "raw_overview_1800.png",
    "raw_doc25_top_full.png",
    "raw_doc25_top_left.png",
    "raw_doc25_top_right.png",
    "raw_doc25_mid_left.png",
    "raw_doc25_mid_right.png",
    "raw_doc25_bottom_full.png",
    "raw_doc25_bottom_left.png",
    "raw_doc25_bottom_right.png",
    "nodes_doc25_top_full.png",
    "nodes_doc25_bottom_full.png",
    "wires_doc25_top_full.png",
    "wires_doc25_bottom_full.png",
]

R2_FOCUS_IMAGE_NAMES = [
    "raw_doc25_bottom_full.png",
    "raw_doc25_bottom_left.png",
    "raw_doc25_bottom_right.png",
    "raw_doc25_center_control.png",
    "raw_doc25_A_feeder01_close.png",
    "nodes_doc25_bottom_full.png",
    "wires_doc25_bottom_full.png",
]

MAIN_VIEWED_IMAGE_NAMES = [
    "raw_overview_1800.png",
    "raw_doc25_top_left.png",
    "raw_doc25_top_right.png",
    "raw_doc25_mid_left.png",
    "raw_doc25_mid_right.png",
    "raw_doc25_bottom_full.png",
    "raw_doc25_bottom_left.png",
    "raw_doc25_bottom_right.png",
    "raw_doc25_center_control.png",
    "raw_doc25_A_feeder01_close.png",
]


def result_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        test = RESULTS / ".write_test_doc25_tokens"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return RESULTS
    except OSError:
        FALLBACK.mkdir(parents=True, exist_ok=True)
        return FALLBACK


def encoding():
    if tiktoken is None:
        return None
    for name in ("o200k_base", "cl100k_base"):
        try:
            return tiktoken.get_encoding(name)
        except Exception:
            continue
    return None


ENCODING = encoding()


def text_tokens(text: str) -> int:
    if ENCODING is None:
        return math.ceil(len(text) / 4)
    return len(ENCODING.encode(text))


def file_text_tokens(path: Path | None) -> int:
    if not path or not path.exists():
        return 0
    return text_tokens(path.read_text(encoding="utf-8", errors="replace"))


def first_existing(name: str) -> Path | None:
    for root in (RESULTS, FALLBACK):
        path = root / name
        if path.exists():
            return path
    return None


def crop_path(name: str) -> Path | None:
    for root in (RESULT_CROPS, FALLBACK_CROPS):
        path = root / name
        if path.exists():
            return path
    return None


def crop_paths(names: list[str]) -> list[Path]:
    return [path for name in names if (path := crop_path(name)) is not None]


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


def add_row(
    rows: list[dict[str, int | str]],
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
    row = {
        "document": DOC,
        "iteration": ITERATION,
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
    rows.append(row)
    return in_low, in_exp, in_high


def token_range_from_file(name: str, low_mult: float = 0.85, high_mult: float = 1.15) -> tuple[int, int, int]:
    expected = file_text_tokens(first_existing(name))
    if expected == 0:
        return (800, 2_000, 5_000)
    return (math.ceil(expected * low_mult), expected, math.ceil(expected * high_mult))


def main() -> None:
    out = result_dir()
    rows: list[dict[str, int | str]] = []
    r1_images = crop_paths(R1_IMAGE_NAMES)
    r2_images = crop_paths(R2_FOCUS_IMAGE_NAMES)
    main_images = crop_paths(MAIN_VIEWED_IMAGE_NAMES)

    base_resource_text = (
        file_text_tokens(WIRE_NODES)
        + text_tokens(str(RAW))
        + text_tokens(str(WIRE_OVERLAY))
        + text_tokens(str(NODE_OVERLAY))
    )

    add_row(
        rows,
        "main_agent_visual_inventory_and_orchestration",
        "Main Codex agent",
        "not exposed",
        "Setup and visual inspection",
        "aggregate_estimate",
        text_tokens("Main Codex visual inventory, crop planning, schematic inspection, and workflow orchestration for document 25.")
        + base_resource_text,
        image_bundle(main_images),
        (0, 0, 0),
        (600, 1_500, 3_500),
        (1_000, 5_000, 14_000),
        "Aggregate estimate only; this environment does not expose main-agent usage objects.",
    )

    diego_r1_text = text_tokens(
        "Diego high-recall extractor prompt for document 25 using raw, wire masks, node overlays, top, feeder-bank, bottom DC/control, and MCC crops."
    ) + base_resource_text
    diego_r1_output = token_range_from_file("diego_round1_output.txt")
    diego_r1_input = add_row(
        rows,
        "diego_round1_spawn_agent",
        "Diego",
        "gpt-5.5",
        "Diego round 1",
        "spawn_agent",
        diego_r1_text,
        image_bundle(r1_images),
        (0, 0, 0),
        diego_r1_output,
        (2_000, 8_000, 22_000),
        "High-recall subagent. Actual Responses/token usage object was unavailable.",
    )

    jennifer_r1_text = (
        text_tokens("Jennifer precision reviewer prompt for document 25 against Diego round 1.")
        + file_text_tokens(first_existing("diego_round1_output.txt"))
        + base_resource_text
    )
    jennifer_r1_output = token_range_from_file("jennifer_round1_review.txt")
    jennifer_r1_input = add_row(
        rows,
        "jennifer_round1_spawn_agent",
        "Jennifer",
        "gpt-5.5",
        "Jennifer round 1",
        "spawn_agent",
        jennifer_r1_text,
        image_bundle(r1_images),
        (0, 0, 0),
        jennifer_r1_output,
        (2_000, 7_000, 20_000),
        "Precision review subagent. Actual Responses/token usage object was unavailable.",
    )

    diego_r2_text = (
        text_tokens("Diego round 2 prompt to review Jennifer round 1 and recheck lower RPS route labels.")
        + file_text_tokens(first_existing("jennifer_round1_review.txt"))
    )
    diego_r2_output = token_range_from_file("diego_round2_response.txt")
    add_row(
        rows,
        "diego_round2_send_input",
        "Diego",
        "gpt-5.5",
        "Diego round 2",
        "send_input",
        diego_r2_text,
        image_bundle(r2_images),
        (0, diego_r1_input[1] + diego_r1_output[1], diego_r1_input[2] + diego_r1_output[2]),
        diego_r2_output,
        (500, 1_500, 5_000),
        "Continuation estimate; cached-token range approximates possible reuse of Diego round-1 context.",
    )

    jennifer_r2_text = (
        text_tokens("Jennifer round 2 final prompt to confirm saturated document 25 matrix.")
        + file_text_tokens(first_existing("diego_round2_response.txt"))
    )
    jennifer_r2_output = token_range_from_file("jennifer_round2_final.txt")
    add_row(
        rows,
        "jennifer_round2_final_send_input",
        "Jennifer",
        "gpt-5.5",
        "Jennifer round 2 final",
        "send_input",
        jennifer_r2_text,
        image_bundle(r2_images),
        (0, jennifer_r1_input[1] + jennifer_r1_output[1], jennifer_r1_input[2] + jennifer_r1_output[2]),
        jennifer_r2_output,
        (1_000, 3_000, 8_000),
        "Final precision confirmation estimate; actual usage object was unavailable.",
    )

    main_generation_text = (
        text_tokens("Main Codex final generation, matrix validation, artifact copy, and final report for document 25.")
        + file_text_tokens(first_existing("diego_round1_output.txt"))
        + file_text_tokens(first_existing("jennifer_round1_review.txt"))
        + file_text_tokens(first_existing("diego_round2_response.txt"))
        + file_text_tokens(first_existing("jennifer_round2_final.txt"))
    )
    add_row(
        rows,
        "main_agent_generation_validation_final",
        "Main Codex agent",
        "not exposed",
        "Generation and validation",
        "aggregate_estimate",
        main_generation_text,
        (0, 0, 0),
        (0, 0, 0),
        (700, 1_800, 4_500),
        (1_000, 4_000, 12_000),
        "Aggregate estimate for local artifact generation, validation, and final response.",
    )

    csv_path = out / "token_usage_estimate_doc25.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_exp = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)

    md_path = out / "token_usage_estimate_doc25.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Token Usage Estimate - Document 25, Iteration 1\n\n")
        handle.write(
            "No OpenAI API key was available, the Responses input-token counting endpoint could not be called, "
            "and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with "
            "tiktoken when available, otherwise len(text)/4. Image/file input tokens use low thumbnail, expected "
            "high-detail tile, and high no-resize tile estimates.\n\n"
        )
        handle.write(
            "| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |\n"
        )
        handle.write("|---:|---:|---|---|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            handle.write(
                f"| {row['document']} | {row['iteration']} | {row['round']} | {row['agent']} | "
                f"{row['input_tokens_expected']} | {row['cached_input_tokens_expected']} | "
                f"{row['image_file_input_tokens_expected']} | {row['output_tokens_expected']} | "
                f"{row['reasoning_tokens_expected']} | {row['total_tokens_expected']} |\n"
            )
        handle.write(
            f"\nLow total estimate: {total_low}\n\nExpected total estimate: {total_exp}\n\nHigh total estimate: {total_high}\n"
        )

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    print({"total_low": total_low, "total_expected": total_exp, "total_high": total_high})


if __name__ == "__main__":
    main()
