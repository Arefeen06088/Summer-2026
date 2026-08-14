from __future__ import annotations

import csv
import math
import struct
from pathlib import Path

try:
    import tiktoken
except ImportError:  # pragma: no cover
    tiktoken = None

from build_connectivity_outputs import EDGES, NODES


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\1\Raw + wires + junctions")
CROPS = BASE / "codes" / "crops"
RESULTS = BASE / "results"

RAW = BASE / "raw -- schematic_image_clean_100_connected.png"
WIRE_NODES_OVERLAY = BASE / "wire_nodes_overlay.png"
WIRE_NODES_CSV = BASE / "wire_nodes.csv"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        signature = f.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a PNG: {path}")
        length = struct.unpack(">I", f.read(4))[0]
        chunk_type = f.read(4)
        if chunk_type != b"IHDR" or length < 8:
            raise ValueError(f"No IHDR header: {path}")
        width, height = struct.unpack(">II", f.read(8))
        return width, height


def high_detail_image_tokens(path: Path) -> int:
    """Approximate high-detail image input tokens with the common 512-tile rule."""
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
    if tiktoken is None:
        return max(1, math.ceil(len(text) / 4))
    for name in ("o200k_base", "cl100k_base", "p50k_base"):
        try:
            enc = tiktoken.get_encoding(name)
            return len(enc.encode(text))
        except Exception:
            continue
    # Offline fallback when tiktoken is installed but its encoding files are not cached.
    return max(1, math.ceil(len(text) / 4))


def nodes_text() -> str:
    return "\n".join(f"{node_id},{label}" for node_id, label in NODES)


def edges_text() -> str:
    return "; ".join(f"{u},{v}" for u, v in EDGES)


DIEGO_IMAGES = [
    RAW,
    WIRE_NODES_OVERLAY,
    CROPS / "raw_top_A.png",
    CROPS / "raw_top_B.png",
    CROPS / "raw_top_C.png",
    CROPS / "raw_loads_A.png",
    CROPS / "raw_loads_B.png",
    CROPS / "raw_loads_C.png",
    CROPS / "raw_dc_ups.png",
]

JENNIFER_IMAGES = [
    RAW,
    WIRE_NODES_OVERLAY,
    CROPS / "raw_top_A.png",
    CROPS / "raw_top_B.png",
    CROPS / "raw_top_C.png",
    CROPS / "raw_xfmr_A.png",
    CROPS / "raw_xfmr_B.png",
    CROPS / "raw_xfmr_C.png",
    CROPS / "raw_tie_AB.png",
    CROPS / "raw_tie_BC.png",
    CROPS / "raw_loads_A.png",
    CROPS / "raw_loads_B.png",
    CROPS / "raw_loads_C.png",
    CROPS / "raw_dc_ups.png",
    CROPS / "overlay_dc_ups.png",
]

MAIN_VIEWED_IMAGES = JENNIFER_IMAGES

DIEGO_PROMPT = """
You are Diego, the high-recall extractor. Use only allowed Raw + wires + junctions resources.
Do not use GT or OCR. Inspect raw schematic, wire overlay, and crops. Return nodes, edges,
evidence, matrix, and ambiguity notes. Include all visually/geometrically plausible buses,
sources, breakers, transformers, load devices, control devices, and explicit tie devices.
"""

JENNIFER_PROMPT = f"""
You are Jennifer, the precision reviewer/refiner. Use only allowed Raw + wires + junctions resources.
Review Diego's high-recall proposal; remove unsupported nodes/edges and fix names.
Diego nodes:
{nodes_text()}

Diego edges:
{edges_text()}
"""

MAIN_VISIBLE_TEXT = f"""
Main agent orchestration included the user's task, directory inventory, wire_nodes.csv contents,
visual observations, subagent outputs, and matrix generation/validation logs. This is a visible
payload approximation; platform/developer instructions and rolling conversation cache are not
recoverable here. wire_nodes.csv:
{WIRE_NODES_CSV.read_text(encoding='utf-8')}
"""

DIEGO_OUTPUT_PROXY = f"""
Diego returned high-recall nodes, edge evidence, a partial explicit matrix, and ambiguity notes.
Nodes:
{nodes_text()}

Edges:
{edges_text()}
"""

JENNIFER_OUTPUT_PROXY = f"""
Jennifer accepted Diego's nodes and edges unchanged, clarified tie interpretation, and retained
dashed control/instrumentation links.
Accepted nodes:
{nodes_text()}

Accepted edges:
{edges_text()}
"""


def image_total(paths: list[Path]) -> int:
    return sum(high_detail_image_tokens(path) for path in paths)


def call_rows() -> list[dict[str, object]]:
    document = "Raw + wires + junctions"
    iteration = 1

    calls = [
        {
            "call_id": "main_group_estimate",
            "agent": "Main Codex agent",
            "model": "GPT-5/Codex session",
            "round": "orchestration + local visual inspection",
            "text": MAIN_VISIBLE_TEXT,
            "images": MAIN_VIEWED_IMAGES,
            "file_text_tokens_est": count_text_tokens(WIRE_NODES_CSV.read_text(encoding="utf-8")),
            "output_low": 1200,
            "output_expected": 2500,
            "output_high": 4500,
            "reasoning_low": 3000,
            "reasoning_expected": 9000,
            "reasoning_high": 22000,
            "notes": "Grouped because individual main-agent invocations and usage objects are not exposed by this interface.",
        },
        {
            "call_id": "diego_round_01",
            "agent": "Diego",
            "model": "gpt-5.5",
            "round": "high-recall extraction",
            "text": DIEGO_PROMPT,
            "images": DIEGO_IMAGES,
            "file_text_tokens_est": 0,
            "output_low": max(1800, count_text_tokens(DIEGO_OUTPUT_PROXY) // 2),
            "output_expected": max(3500, count_text_tokens(DIEGO_OUTPUT_PROXY)),
            "output_high": max(7000, count_text_tokens(DIEGO_OUTPUT_PROXY) * 2),
            "reasoning_low": 3000,
            "reasoning_expected": 10000,
            "reasoning_high": 28000,
            "notes": "Payload text and image files counted locally; actual usage object was not returned by subagent tool.",
        },
        {
            "call_id": "jennifer_round_01",
            "agent": "Jennifer",
            "model": "gpt-5.5",
            "round": "precision review",
            "text": JENNIFER_PROMPT,
            "images": JENNIFER_IMAGES,
            "file_text_tokens_est": 0,
            "output_low": max(1200, count_text_tokens(JENNIFER_OUTPUT_PROXY) // 2),
            "output_expected": max(2200, count_text_tokens(JENNIFER_OUTPUT_PROXY)),
            "output_high": max(4500, count_text_tokens(JENNIFER_OUTPUT_PROXY) * 2),
            "reasoning_low": 2000,
            "reasoning_expected": 7000,
            "reasoning_high": 18000,
            "notes": "Payload text and image files counted locally; actual usage object was not returned by subagent tool.",
        },
    ]

    rows: list[dict[str, object]] = []
    for call in calls:
        text_tokens = count_text_tokens(str(call["text"]))
        image_tokens = image_total(call["images"])
        total_input = text_tokens + image_tokens + int(call["file_text_tokens_est"])
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
                "file_text_tokens_est": call["file_text_tokens_est"],
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
    path = RESULTS / "token_usage_estimate.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
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
        "No OpenAI API key was available, and the subagent tool did not expose response usage objects.",
        "Estimates use local tiktoken text counts when cached; otherwise they fall back to ceil(characters/4).",
        "Image tokens use a high-detail 512-tile approximation.",
        "",
        "| Document | Iteration | Call | Agent | Input est | Image/file input est | Output low/exp/high | Reasoning low/exp/high | Total low/exp/high |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        image_file = int(row["image_file_input_tokens_est"]) + int(row["file_text_tokens_est"])
        lines.append(
            f"| {row['document']} | {row['iteration']} | {row['call_id']} | {row['agent']} | "
            f"{row['total_input_tokens_est']} | {image_file} | "
            f"{row['output_tokens_low']}/{row['output_tokens_expected']}/{row['output_tokens_high']} | "
            f"{row['reasoning_tokens_low']}/{row['reasoning_tokens_expected']}/{row['reasoning_tokens_high']} | "
            f"{row['total_tokens_low']}/{row['total_tokens_expected']}/{row['total_tokens_high']} |"
        )
    lines.extend(
        [
            "",
            f"Grouped totals for Raw + wires + junctions, iteration 1:",
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
