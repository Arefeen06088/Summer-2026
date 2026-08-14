import csv
import json
import math
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required for image-size estimates") from exc


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CALLS_PATH = RESULTS / "token_usage_calls.json"


def estimate_text_tokens(text):
    try:
        import tiktoken

        try:
            enc = tiktoken.encoding_for_model("gpt-5.5")
        except Exception:
            enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        # Conservative fallback for English/code-ish prompts.
        return math.ceil(len(text) / 3.7)


def scaled_dimensions(width, height, max_side):
    if max(width, height) <= max_side:
        return width, height
    scale = max_side / max(width, height)
    return max(1, math.floor(width * scale)), max(1, math.floor(height * scale))


def estimate_image_tokens(path, detail):
    width, height = Image.open(path).size
    if detail == "low":
        return {
            "width": width,
            "height": height,
            "detail": detail,
            "patches": 85,
            "estimated_tokens": 85,
        }

    # GPT-5.5 documentation describes high as a 2048 px max-side / 2500-patch
    # budget and original as a 6000 px max-side / 10000-patch budget. One patch
    # is approximated as a 32x32 image patch for offline accounting.
    if detail == "original":
        max_side, cap = 6000, 10000
    else:
        max_side, cap = 2048, 2500

    scaled_w, scaled_h = scaled_dimensions(width, height, max_side)
    patches = math.ceil(scaled_w / 32) * math.ceil(scaled_h / 32)
    if patches > cap:
        scale = math.sqrt(cap / patches)
        scaled_w = max(1, math.floor(scaled_w * scale))
        scaled_h = max(1, math.floor(scaled_h * scale))
        patches = min(cap, math.ceil(scaled_w / 32) * math.ceil(scaled_h / 32))

    return {
        "width": width,
        "height": height,
        "detail": detail,
        "patches": patches,
        "estimated_tokens": patches,
    }


def estimate_call(call):
    if "text_input_tokens_override_est" in call:
        text_tokens = int(call["text_input_tokens_override_est"])
        text_counting_method = "manual/offline override"
    else:
        text_tokens = estimate_text_tokens(call.get("prompt_text", ""))
        text_counting_method = "tiktoken_or_chars"
    image_details = [
        estimate_image_tokens(ROOT / rel_path, call.get("image_detail", "high"))
        for rel_path in call.get("image_paths", [])
    ]
    image_tokens = sum(item["estimated_tokens"] for item in image_details)
    expected_output = call.get("expected_output_tokens", 0)
    expected_reasoning = call.get("expected_reasoning_tokens", 0)
    low_reasoning = call.get("low_reasoning_tokens", expected_reasoning)
    high_reasoning = call.get("high_reasoning_tokens", expected_reasoning)
    total_expected = text_tokens + image_tokens + expected_output + expected_reasoning
    low = text_tokens + image_tokens + call.get("low_output_tokens", expected_output) + low_reasoning
    high = text_tokens + image_tokens + call.get("high_output_tokens", expected_output) + high_reasoning
    return {
        "document": call.get("document", "5"),
        "iteration": call.get("iteration", "1"),
        "call_id": call["call_id"],
        "agent": call.get("agent", "main"),
        "purpose": call.get("purpose", ""),
        "text_input_tokens_est": text_tokens,
        "text_counting_method": text_counting_method,
        "cached_input_tokens_recorded": call.get("cached_input_tokens_recorded", "unavailable"),
        "image_file_count": len(image_details),
        "image_file_input_tokens_est": image_tokens,
        "output_tokens_low_est": call.get("low_output_tokens", ""),
        "output_tokens_expected_est": expected_output,
        "output_tokens_high_est": call.get("high_output_tokens", ""),
        "reasoning_tokens_recorded": call.get("reasoning_tokens_recorded", "unavailable"),
        "reasoning_tokens_low_est": low_reasoning,
        "reasoning_tokens_expected_est": expected_reasoning,
        "reasoning_tokens_high_est": high_reasoning,
        "usage_object_available": call.get("usage_object_available", "no"),
        "total_tokens_low_est": low,
        "total_tokens_expected_est": total_expected,
        "total_tokens_high_est": high,
        "notes": call.get("notes", ""),
    }


def main():
    if not CALLS_PATH.exists():
        raise FileNotFoundError(f"missing {CALLS_PATH}")

    payload = json.loads(CALLS_PATH.read_text(encoding="utf-8"))
    rows = [estimate_call(call) for call in payload["calls"]]
    out_path = RESULTS / "token_usage_estimates.csv"
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    totals = {}
    for row in rows:
        key = (row["document"], row["iteration"])
        bucket = totals.setdefault(
            key,
            {
                "document": row["document"],
                "iteration": row["iteration"],
                "calls": 0,
                "text_input_tokens_est": 0,
                "image_file_input_tokens_est": 0,
                "total_tokens_low_est": 0,
                "total_tokens_expected_est": 0,
                "total_tokens_high_est": 0,
            },
        )
        bucket["calls"] += 1
        for field in (
            "text_input_tokens_est",
            "image_file_input_tokens_est",
            "total_tokens_low_est",
            "total_tokens_expected_est",
            "total_tokens_high_est",
        ):
            bucket[field] += int(row[field])

    total_path = RESULTS / "token_usage_totals_by_document_iteration.csv"
    with total_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(next(iter(totals.values())).keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(totals.values())

    print(f"wrote {out_path}")
    print(f"wrote {total_path}")


if __name__ == "__main__":
    main()
