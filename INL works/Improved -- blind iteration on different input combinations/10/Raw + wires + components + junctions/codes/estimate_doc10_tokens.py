import base64
import csv
import json
import math
import os
from pathlib import Path
from urllib import request

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CROPS = BASE / "codes" / "crops"
MODEL = "gpt-5.6"


try:
    import tiktoken

    try:
        ENCODING = tiktoken.encoding_for_model(MODEL)
    except Exception:
        ENCODING = tiktoken.get_encoding("o200k_base")
except Exception:
    ENCODING = None


def text_tokens(text):
    if not text:
        return 0
    if ENCODING is None:
        return math.ceil(len(text) / 4)
    return len(ENCODING.encode(text))


def vision_tokens_high(path):
    # OpenAI vision-token estimate for GPT-5-class high-detail images:
    # fit within 2048px square, then downscale the shortest side to 768px
    # when it is larger than 768px; 70 base + 140 per 512px tile.
    image = Image.open(path)
    w, h = image.size
    scale = min(2048 / max(w, h), 1.0)
    w1, h1 = w * scale, h * scale
    if min(w1, h1) > 768:
        scale2 = 768 / min(w1, h1)
        w1, h1 = w1 * scale2, h1 * scale2
    tiles = math.ceil(w1 / 512) * math.ceil(h1 / 512)
    return 70 + 140 * tiles


def image_token_range(paths):
    low = 70 * len(paths)
    expected = sum(vision_tokens_high(p) for p in paths)
    high = math.ceil(expected * 1.15 + 50 * len(paths))
    return low, expected, high


def read_result_text(*names):
    chunks = []
    for name in names:
        path = RESULTS / name
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def data_url(path):
    mime = "image/png"
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def count_with_openai_endpoint(call, image_paths):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None, "skipped: OPENAI_API_KEY not set"
    content = [{"type": "input_text", "text": call["input_text"]}]
    for path in image_paths:
        content.append({"type": "input_image", "image_url": data_url(path)})
    payload = {
        "model": MODEL,
        "input": [{"role": "user", "content": content}],
    }
    req = request.Request(
        "https://api.openai.com/v1/responses/input_tokens",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
            return body.get("input_tokens"), "ok"
    except Exception as exc:
        return None, f"endpoint failed: {exc}"


def make_call(call_id, agent, round_name, input_text, images, output_text, notes):
    return {
        "document": 10,
        "iteration": 1,
        "call_id": call_id,
        "agent": agent,
        "round": round_name,
        "input_text": input_text,
        "images": [Path(p) for p in images],
        "output_text": output_text,
        "notes": notes,
    }


RAW = BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png"
DETECTED = BASE / "detected_components_overlay.png"
WIRE_NODES = BASE / "wire_nodes_overlay.png"
WIRE_MASK_OVERLAY = BASE / "wires_mask_overlay.png"

diego_round1_images = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK_OVERLAY,
    CROPS / "raw__top_sources.png",
    CROPS / "raw__mid_left_a_switchgear.png",
    CROPS / "raw__mid_right_b_switchgear.png",
    CROPS / "raw__bottom_left_a_loads.png",
    CROPS / "raw__bottom_right_b_loads.png",
    CROPS / "raw__dc_a.png",
    CROPS / "raw__dc_b.png",
    CROPS / "raw__mcr_notes_legend.png",
    CROPS / "wire_nodes__mid_left_a_switchgear.png",
    CROPS / "wire_nodes__mid_right_b_switchgear.png",
    CROPS / "wire_nodes__bottom_left_a_loads.png",
    CROPS / "wire_nodes__bottom_right_b_loads.png",
]

jennifer_round2_images = [
    RAW,
    DETECTED,
    WIRE_NODES,
    CROPS / "raw__top_sources.png",
    CROPS / "raw__left_full.png",
    CROPS / "raw__center_full.png",
    CROPS / "raw__right_full.png",
    CROPS / "wire_nodes__left_full.png",
    CROPS / "wire_nodes__center_full.png",
    CROPS / "wire_nodes__right_full.png",
    CROPS / "raw__mcr_notes_legend.png",
]

diego_round3_images = [
    RAW,
    CROPS / "raw__a_source_tie_close.png",
    CROPS / "raw__b_source_tie_close.png",
    CROPS / "raw__a_fuses_ds_close.png",
    CROPS / "raw__b_fuses_ds_close.png",
    CROPS / "raw__mcr_notes_legend.png",
]

main_visual_images = [
    RAW,
    CROPS / "raw__top_sources.png",
    CROPS / "raw__top_left_a_source.png",
    CROPS / "raw__top_right_b_source_mcr.png",
    CROPS / "raw__mid_left_a_switchgear.png",
    CROPS / "wire_nodes__mid_left_a_switchgear.png",
    CROPS / "detected__mid_left_a_switchgear.png",
    CROPS / "raw__bottom_left_a_loads.png",
    CROPS / "raw__a_control_close.png",
    CROPS / "wire_nodes__bottom_left_a_loads.png",
    CROPS / "raw__bottom_right_b_loads.png",
    CROPS / "raw__dc_a.png",
    CROPS / "raw__mcr_notes_legend.png",
    CROPS / "wire_nodes__mcr_notes_legend.png",
    CROPS / "raw__right_full.png",
    CROPS / "raw__mid_right_b_switchgear.png",
    CROPS / "raw__left_full.png",
    CROPS / "raw__center_full.png",
    CROPS / "wire_nodes__center_full.png",
    CROPS / "raw__a_source_tie_close.png",
    CROPS / "raw__b_source_tie_close.png",
    CROPS / "raw__a_fuses_ds_close.png",
    CROPS / "wire_nodes__a_fuses_ds_close.png",
    CROPS / "detected__a_fuses_ds_close.png",
    CROPS / "detected__dc_a.png",
    CROPS / "wire_mask_overlay__a_fuses_ds_close.png",
]

diego_round1_prompt = """
High-recall extraction prompt for Diego: inspect document 10 raw schematic and derived visual aids.
Use only the Raw + wires + components + junctions folder. Extract all visually/geometrically
plausible components, logical nodes, and power/control/signal/ground edges with evidence.
"""

jennifer_round2_prompt = """
Precision review prompt for Jennifer: review Diego's high-recall nodes/edges, remove unsupported
or overconnected edges, fix labels, and mark ambiguous cases uncertain.
""" + read_result_text(
    "round_01_diego_high_recall_node_order.csv",
    "round_01_diego_high_recall_edges.csv",
)

diego_round3_prompt = """
Saturation prompt for Diego: re-check Jennifer's precision graph and either agree or list only
minimal visually necessary changes.
""" + read_result_text(
    "round_02_jennifer_precision_node_order.csv",
    "round_02_jennifer_precision_edges.csv",
    "uncertain_excluded_edges.csv",
)

main_input_text = """
Main agent grouped estimate: user task for document 10, file inventory, local visual crop inspection,
subagent coordination, artifact writing, validation, token-estimate generation, and final response.
Hidden system/developer/tool schema tokens are not exposed and are therefore not included exactly.
"""

calls = [
    make_call(
        "main_grouped_visual_artifact",
        "main",
        "orchestration + visual inspection + artifact writing",
        main_input_text,
        main_visual_images,
        read_result_text("round_notes.md", "final_edges.csv", "final_node_order.csv"),
        "Grouped because internal main-agent model response boundaries and usage objects are not exposed.",
    ),
    make_call(
        "diego_round_01_high_recall",
        "Diego",
        "round 1 high recall",
        diego_round1_prompt,
        diego_round1_images,
        read_result_text("round_01_diego_high_recall_node_order.csv", "round_01_diego_high_recall_edges.csv"),
        "Explicit subagent call; usage object not exposed by the multi-agent tool.",
    ),
    make_call(
        "jennifer_round_02_precision",
        "Jennifer",
        "round 2 precision review",
        jennifer_round2_prompt,
        jennifer_round2_images,
        read_result_text("round_02_jennifer_precision_node_order.csv", "round_02_jennifer_precision_edges.csv", "uncertain_excluded_edges.csv"),
        "Explicit subagent call; usage object not exposed by the multi-agent tool.",
    ),
    make_call(
        "diego_round_03_saturation",
        "Diego",
        "round 3 saturation check",
        diego_round3_prompt,
        diego_round3_images,
        "Diego agreed Jennifer's corrected set was visually saturated. Final edge list is unchanged.",
        "Explicit subagent call; usage object not exposed by the multi-agent tool.",
    ),
]


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for call in calls:
        input_text_expected = text_tokens(call["input_text"])
        image_low, image_expected, image_high = image_token_range(call["images"])
        output_expected = text_tokens(call["output_text"])
        endpoint_count, endpoint_status = count_with_openai_endpoint(call, call["images"])
        input_expected = endpoint_count or (input_text_expected + image_expected)
        rows.append(
            {
                "document": call["document"],
                "iteration": call["iteration"],
                "call_id": call["call_id"],
                "agent": call["agent"],
                "round": call["round"],
                "endpoint_status": endpoint_status,
                "input_tokens_endpoint": endpoint_count if endpoint_count is not None else "",
                "input_text_tokens_est": input_text_expected,
                "image_file_input_tokens_low": image_low,
                "image_file_input_tokens_expected": image_expected,
                "image_file_input_tokens_high": image_high,
                "total_input_tokens_low": math.ceil(input_text_expected * 0.9 + image_low),
                "total_input_tokens_expected": input_expected,
                "total_input_tokens_high": math.ceil(input_text_expected * 1.15 + image_high),
                "cached_input_tokens": "not exposed; estimated 0 for billing fallback",
                "output_tokens_low": math.floor(output_expected * 0.85),
                "output_tokens_expected": output_expected,
                "output_tokens_high": math.ceil(output_expected * 1.2 + 50),
                "reasoning_tokens": "not exposed",
                "usage_object_available": "no",
                "notes": call["notes"],
            }
        )

    detail_path = RESULTS / "token_usage_estimates.csv"
    with detail_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_low = sum(int(row["total_input_tokens_low"]) + int(row["output_tokens_low"]) for row in rows)
    total_expected = sum(int(row["total_input_tokens_expected"]) + int(row["output_tokens_expected"]) for row in rows)
    total_high = sum(int(row["total_input_tokens_high"]) + int(row["output_tokens_high"]) for row in rows)
    summary_rows = [
        {
            "document": 10,
            "iteration": 1,
            "model_calls_counted": len(rows),
            "total_tokens_low": total_low,
            "total_tokens_expected": total_expected,
            "total_tokens_high": total_high,
            "usage_objects_collected": "not exposed by Codex/multi_agent_v1 tools",
            "endpoint": "POST /v1/responses/input_tokens",
            "endpoint_result": rows[0]["endpoint_status"],
        }
    ]
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(detail_path)
    print(RESULTS / "token_usage_summary.csv")


if __name__ == "__main__":
    main()
