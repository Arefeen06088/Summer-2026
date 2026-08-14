import csv
import math
from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = RESULTS / "crops"


def image_patch_tokens(path: Path) -> int:
    """GPT-5.5/GPT-5.6 original-detail estimate: ceil(w/32) * ceil(h/32)."""
    image = Image.open(path)
    width, height = image.size
    return math.ceil(width / 32) * math.ceil(height / 32)


def capped_high_detail_tokens(path: Path, patch_budget: int = 2500, max_dim: int = 2048) -> int:
    """Approximate lower bound if images had been sent with high detail instead of original."""
    image = Image.open(path)
    width, height = image.size
    scale = min(1.0, max_dim / max(width, height))
    width_s = width * scale
    height_s = height * scale
    patches = math.ceil(width_s / 32) * math.ceil(height_s / 32)
    if patches <= patch_budget:
        return patches
    scale *= math.sqrt(patch_budget / patches)
    width_s = width * scale
    height_s = height * scale
    return min(patch_budget, math.ceil(width_s / 32) * math.ceil(height_s / 32))


def image_totals(paths: list[Path]) -> tuple[int, int, int]:
    expected = sum(image_patch_tokens(path) for path in paths)
    low = sum(capped_high_detail_tokens(path) for path in paths)
    high = math.ceil(expected * 1.15)
    return low, expected, high


RAW = BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png"
MASK = BASE / "wires_mask.png"
OVERLAY = BASE / "wires_mask_overlay.png"


calls = [
    {
        "call_order": "M01",
        "agent": "Main Codex",
        "model": "session model",
        "purpose": "Aggregate orchestration, local visual inspection, crop generation, graph integration, artifact writing.",
        "images": [
            RAW,
            OVERLAY,
            CROPS / "raw_left.png",
            CROPS / "raw_center.png",
            CROPS / "raw_right.png",
            CROPS / "overlay_left.png",
            CROPS / "raw_bottom.png",
            CROPS / "raw_top.png",
            CROPS / "raw_r2c2.png",
            CROPS / "raw_r2c1.png",
            CROPS / "raw_r2c3.png",
            CROPS / "raw_r3c2.png",
            CROPS / "raw_r3c1.png",
            CROPS / "raw_r3c3.png",
            CROPS / "raw_r1c1.png",
            CROPS / "raw_r1c2.png",
            CROPS / "raw_r1c3.png",
            CROPS / "raw_r2c4.png",
            CROPS / "overlay_right.png",
            CROPS / "raw_mcr_zoom.png",
            CROPS / "overlay_r2c1.png",
            CROPS / "overlay_r2c3.png",
            CROPS / "overlay_bottom.png",
            CROPS / "overlay_r3c1.png",
        ],
        "text_expected": 16000,
        "output_expected": 4200,
        "reasoning_expected": 9000,
    },
    {
        "call_order": "S01",
        "agent": "Diego R1",
        "model": "gpt-5.5 xhigh",
        "purpose": "High-recall extraction from raw, mask, overlay, and broad crops.",
        "images": [
            RAW,
            OVERLAY,
            MASK,
            CROPS / "raw_top.png",
            CROPS / "raw_middle.png",
            CROPS / "raw_bottom.png",
            CROPS / "overlay_top.png",
            CROPS / "overlay_middle.png",
            CROPS / "overlay_bottom.png",
        ],
        "text_expected": 1100,
        "output_expected": 5200,
        "reasoning_expected": 12000,
    },
    {
        "call_order": "S02",
        "agent": "Jennifer R1",
        "model": "gpt-5.5 xhigh",
        "purpose": "Precision review of Diego R1, route-node pruning, final matrix draft.",
        "images": [
            RAW,
            OVERLAY,
            CROPS / "raw_left.png",
            CROPS / "raw_center.png",
            CROPS / "raw_right.png",
            CROPS / "raw_mcr_zoom.png",
            CROPS / "overlay_left.png",
            CROPS / "overlay_right.png",
        ],
        "text_expected": 5600,
        "output_expected": 9800,
        "reasoning_expected": 14000,
    },
    {
        "call_order": "S03",
        "agent": "Diego R2",
        "model": "gpt-5.5 xhigh",
        "purpose": "Convergence review of Jennifer R1 with targeted questions.",
        "images": [
            RAW,
            OVERLAY,
            CROPS / "raw_left.png",
            CROPS / "raw_center.png",
            CROPS / "raw_mcr_zoom.png",
            CROPS / "overlay_left.png",
            CROPS / "overlay_right.png",
        ],
        "text_expected": 1800,
        "output_expected": 420,
        "reasoning_expected": 5000,
    },
]


def band(value: int) -> tuple[int, int, int]:
    return math.floor(value * 0.75), value, math.ceil(value * 1.35)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for call in calls:
        image_low, image_expected, image_high = image_totals(call["images"])
        text_low, text_expected, text_high = band(call["text_expected"])
        output_low, output_expected, output_high = band(call["output_expected"])
        reasoning_low, reasoning_expected, reasoning_high = band(call["reasoning_expected"])
        rows.append(
            {
                "document": 10,
                "iteration": 1,
                "call_order": call["call_order"],
                "agent": call["agent"],
                "model": call["model"],
                "purpose": call["purpose"],
                "input_text_tokens_low": text_low,
                "input_text_tokens_expected": text_expected,
                "input_text_tokens_high": text_high,
                "cached_input_tokens": 0,
                "image_file_count": len(call["images"]),
                "image_input_tokens_low": image_low,
                "image_input_tokens_expected": image_expected,
                "image_input_tokens_high": image_high,
                "output_tokens_low": output_low,
                "output_tokens_expected": output_expected,
                "output_tokens_high": output_high,
                "reasoning_tokens_low": reasoning_low,
                "reasoning_tokens_expected": reasoning_expected,
                "reasoning_tokens_high": reasoning_high,
                "total_tokens_low": text_low + image_low + output_low + reasoning_low,
                "total_tokens_expected": text_expected + image_expected + output_expected + reasoning_expected,
                "total_tokens_high": text_high + image_high + output_high + reasoning_high,
                "usage_object_available": "no; subagent/main response usage not exposed in this interface",
            }
        )

    csv_path = RESULTS / "token_usage_estimate.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(row["total_tokens_low"] for row in rows)
    total_expected = sum(row["total_tokens_expected"] for row in rows)
    total_high = sum(row["total_tokens_high"] for row in rows)
    image_expected = sum(row["image_input_tokens_expected"] for row in rows)

    summary = f"""# Token Usage Estimate - Document 10

No API key was available, so the OpenAI Responses counting endpoint was not called and no response `usage` objects were exposed by this environment.

Method:
- Text tokens are local estimates from the retained prompt/output sizes, banded low/expected/high.
- Image tokens use the current OpenAI vision patch method for GPT-5.5/GPT-5.6 original detail: `ceil(width/32) * ceil(height/32)`.
- Low image estimate assumes high-detail capped processing; expected assumes original detail; high adds 15 percent for model/accounting variance.
- Cached input tokens are recorded as 0 because cache usage was not observable.

| document | iteration | model calls counted | expected image/file input tokens | total low | total expected | total high |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1 | {len(rows)} | {image_expected} | {total_low} | {total_expected} | {total_high} |

See `token_usage_estimate.csv` for per-call rows.
"""
    (RESULTS / "token_usage_summary.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
