from __future__ import annotations

import csv
import math
import struct
from pathlib import Path

from build_connectivity_outputs import EDGE_SPECS, NODES


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw + wires + junctions")
CROPS = BASE / "codes" / "crops"
RESULTS = BASE / "results"

RAW = BASE / "raw -- schematic_image_variant_b_100.png"
WIRE_NODES_OVERLAY = BASE / "wire_nodes_overlay.png"
WIRE_NODES_CSV = BASE / "wire_nodes.csv"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a PNG: {path}")
        length = struct.unpack(">I", f.read(4))[0]
        chunk_type = f.read(4)
        if chunk_type != b"IHDR" or length < 8:
            raise ValueError(f"No IHDR header: {path}")
        return struct.unpack(">II", f.read(8))


def high_detail_image_tokens(path: Path) -> int:
    """Approximate high-detail image input tokens with a common 512-tile rule."""
    width, height = png_size(path)
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    short_side = min(width, height)
    if short_side > 0 and short_side != 768:
        scale = 768 / short_side
        width *= scale
        height *= scale
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def count_text_tokens(text: str) -> int:
    # No API key was available for the Responses input-token counting endpoint.
    # This conservative local fallback is good enough for round-to-round estimates.
    return max(1, math.ceil(len(text) / 4))


def nodes_text() -> str:
    return "\n".join(f"{node_id},{label}" for node_id, label in NODES)


def edges_text() -> str:
    return "; ".join(f"{u},{v},{kind}" for u, v, kind in EDGE_SPECS)


MAIN_IMAGES = [
    RAW,
    WIRE_NODES_OVERLAY,
    CROPS / "raw_top_train_a.png",
    CROPS / "raw_top_tie.png",
    CROPS / "raw_top_train_b.png",
    CROPS / "raw_loads_train_a_left.png",
    CROPS / "raw_loads_train_a_right.png",
    CROPS / "raw_loads_train_b_left.png",
    CROPS / "raw_loads_train_b_right.png",
    CROPS / "raw_lower_rps.png",
    CROPS / "raw_title_notes.png",
    CROPS / "overlay_lower_rps.png",
]

DIEGO_IMAGES = [
    RAW,
    WIRE_NODES_OVERLAY,
    CROPS / "raw_top_train_a.png",
    CROPS / "raw_top_tie.png",
    CROPS / "raw_top_train_b.png",
    CROPS / "raw_loads_train_a_left.png",
    CROPS / "raw_loads_train_a_right.png",
    CROPS / "raw_loads_train_b_left.png",
    CROPS / "raw_loads_train_b_right.png",
    CROPS / "raw_lower_rps.png",
    CROPS / "raw_title_notes.png",
    CROPS / "overlay_top_train_a.png",
    CROPS / "overlay_top_tie.png",
    CROPS / "overlay_loads_train_a_right.png",
    CROPS / "overlay_loads_train_b_left.png",
    CROPS / "overlay_lower_rps.png",
]

JENNIFER_IMAGES = [
    RAW,
    WIRE_NODES_OVERLAY,
    CROPS / "raw_top_train_a.png",
    CROPS / "raw_top_tie.png",
    CROPS / "raw_top_train_b.png",
    CROPS / "raw_loads_train_a_left.png",
    CROPS / "raw_loads_train_a_right.png",
    CROPS / "raw_loads_train_b_left.png",
    CROPS / "raw_loads_train_b_right.png",
    CROPS / "raw_lower_rps.png",
    CROPS / "raw_title_notes.png",
    CROPS / "overlay_top_tie.png",
    CROPS / "overlay_loads_train_a_right.png",
    CROPS / "overlay_loads_train_b_right.png",
    CROPS / "overlay_lower_rps.png",
]

MAIN_TEXT = f"""
Main Codex agent orchestration for iteration 2: user instructions, file inventory, wire_nodes.csv,
visual observations from raw image and crops, subagent outputs, matrix generation, validation,
and token-estimate artifact creation. wire_nodes.csv:
{WIRE_NODES_CSV.read_text(encoding='utf-8')}
"""

DIEGO_TEXT = f"""
Diego high-recall extraction prompt: use only Raw + wires + junctions iteration 2 resources,
no GT and no OCR. Extract buses, components, explicit tie devices, solid feeder edges, and
visibly terminated dashed signal/control edges. wire_nodes.csv:
{WIRE_NODES_CSV.read_text(encoding='utf-8')}
"""

JENNIFER_TEXT = f"""
Jennifer precision review prompt: inspect Diego's graph against the allowed raw/crop/overlay files,
remove unsupported edges, fix labels, retain only visibly supported dashed signal/control endpoints,
and do not add crossing-only junctions. Diego proposal:
{nodes_text()}

{edges_text()}
"""

DIEGO_OUTPUT_PROXY = f"""
Diego returned a 100-node, 100-edge proposal with nodes and chain-expanded edges:
{nodes_text()}

{edges_text()}
"""

JENNIFER_OUTPUT_PROXY = f"""
Jennifer accepted Diego's 100-node, 100-edge graph unchanged and clarified tie/signal semantics:
{nodes_text()}

{edges_text()}
"""


def image_total(paths: list[Path]) -> int:
    return sum(high_detail_image_tokens(path) for path in paths)


def call_rows() -> list[dict[str, object]]:
    document = "Raw + wires + junctions"
    iteration = 2
    calls = [
        {
            "call_id": "main_group_estimate",
            "agent": "Main Codex agent",
            "model": "GPT-5/Codex session",
            "round": "orchestration + local visual inspection",
            "text": MAIN_TEXT,
            "images": MAIN_IMAGES,
            "output_low": 1200,
            "output_expected": 2500,
            "output_high": 4500,
            "reasoning_low": 3000,
            "reasoning_expected": 9000,
            "reasoning_high": 22000,
            "notes": "Grouped because individual main-agent model usage objects are not exposed by this interface.",
        },
        {
            "call_id": "diego_round_01",
            "agent": "Diego",
            "model": "gpt-5.5",
            "round": "high-recall extraction",
            "text": DIEGO_TEXT,
            "images": DIEGO_IMAGES,
            "output_low": max(1700, count_text_tokens(DIEGO_OUTPUT_PROXY) // 2),
            "output_expected": max(3200, count_text_tokens(DIEGO_OUTPUT_PROXY)),
            "output_high": max(6400, count_text_tokens(DIEGO_OUTPUT_PROXY) * 2),
            "reasoning_low": 3000,
            "reasoning_expected": 10000,
            "reasoning_high": 28000,
            "notes": "Subagent tool did not expose an actual usage object.",
        },
        {
            "call_id": "jennifer_round_01",
            "agent": "Jennifer",
            "model": "gpt-5.5",
            "round": "precision review",
            "text": JENNIFER_TEXT,
            "images": JENNIFER_IMAGES,
            "output_low": max(1300, count_text_tokens(JENNIFER_OUTPUT_PROXY) // 2),
            "output_expected": max(2400, count_text_tokens(JENNIFER_OUTPUT_PROXY)),
            "output_high": max(4800, count_text_tokens(JENNIFER_OUTPUT_PROXY) * 2),
            "reasoning_low": 2000,
            "reasoning_expected": 7000,
            "reasoning_high": 18000,
            "notes": "Subagent tool did not expose an actual usage object.",
        },
    ]

    rows: list[dict[str, object]] = []
    for call in calls:
        text_tokens = count_text_tokens(str(call["text"]))
        image_tokens = image_total(call["images"])
        total_input = text_tokens + image_tokens
        output_low = int(call["output_low"])
        output_expected = int(call["output_expected"])
        output_high = int(call["output_high"])
        reasoning_low = int(call["reasoning_low"])
        reasoning_expected = int(call["reasoning_expected"])
        reasoning_high = int(call["reasoning_high"])
        rows.append(
            {
                "document": document,
                "iteration": iteration,
                "call_id": call["call_id"],
                "agent": call["agent"],
                "model": call["model"],
                "round": call["round"],
                "input_text_tokens_est": text_tokens,
                "cached_input_tokens_recorded": "unavailable",
                "image_file_input_tokens_est": image_tokens,
                "total_input_tokens_est": total_input,
                "output_tokens_low": output_low,
                "output_tokens_expected": output_expected,
                "output_tokens_high": output_high,
                "reasoning_tokens_low": reasoning_low,
                "reasoning_tokens_expected": reasoning_expected,
                "reasoning_tokens_high": reasoning_high,
                "total_tokens_low": total_input + output_low + reasoning_low,
                "total_tokens_expected": total_input + output_expected + reasoning_expected,
                "total_tokens_high": total_input + output_high + reasoning_high,
                "usage_object": "not exposed/no API key",
                "notes": call["notes"],
            }
        )
    return rows


def write_csv(rows: list[dict[str, object]]) -> None:
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]]) -> None:
    total_low = sum(int(row["total_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_tokens_high"]) for row in rows)
    total_input = sum(int(row["total_input_tokens_est"]) for row in rows)
    lines = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key was available, so the Responses input-token counting endpoint could not be used.",
        "The subagent tool did not expose response usage objects.",
        "Text estimates use ceil(characters/4); image estimates use a high-detail 512-tile approximation.",
        "",
        "| Document | Iteration | Call | Agent | Input est | Image/file input est | Output low/exp/high | Reasoning low/exp/high | Total low/exp/high |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call_id']} | {row['agent']} | "
            f"{row['total_input_tokens_est']} | {row['image_file_input_tokens_est']} | "
            f"{row['output_tokens_low']}/{row['output_tokens_expected']}/{row['output_tokens_high']} | "
            f"{row['reasoning_tokens_low']}/{row['reasoning_tokens_expected']}/{row['reasoning_tokens_high']} | "
            f"{row['total_tokens_low']}/{row['total_tokens_expected']}/{row['total_tokens_high']} |"
        )
    lines.extend(
        [
            "",
            "Grouped totals for Raw + wires + junctions, iteration 2:",
            f"- Total input estimate: {total_input}",
            f"- Total tokens low/expected/high: {total_low}/{total_expected}/{total_high}",
        ]
    )
    (RESULTS / "token_usage_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = call_rows()
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote token estimates for {len(rows)} call groups to {RESULTS}")


if __name__ == "__main__":
    main()
