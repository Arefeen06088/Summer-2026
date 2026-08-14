import base64
import csv
import json
import math
import os
from pathlib import Path
from urllib import request

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CROPS = BASE / "codes" / "crops"
MODEL = os.environ.get("OPENAI_RESPONSES_MODEL", "gpt-5.6-sol")

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


def data_url(path):
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def endpoint_count(call, image_paths):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None, "skipped: OPENAI_API_KEY not set"
    content = [{"type": "input_text", "text": call["input_text"]}]
    for path in image_paths:
        content.append({"type": "input_image", "image_url": data_url(path)})
    payload = {"model": MODEL, "input": [{"role": "user", "content": content}]}
    req = request.Request(
        "https://api.openai.com/v1/responses/input_tokens",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body.get("input_tokens"), "ok"
    except Exception as exc:
        return None, f"endpoint failed: {exc}"


def read_results(*names):
    chunks = []
    for name in names:
        path = RESULTS / name
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def call(call_id, agent, round_name, input_text, images, output_text, notes):
    return {
        "document": 14,
        "iteration": 1,
        "call_id": call_id,
        "agent": agent,
        "round": round_name,
        "input_text": input_text,
        "images": [Path(p) for p in images],
        "output_text": output_text,
        "notes": notes,
    }


RAW = BASE / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
DETECTED = BASE / "detected_components_overlay.png"
WIRE_NODES = BASE / "wire_nodes_overlay.png"
WIRE_MASK = BASE / "wires_mask_overlay.png"

main_images = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    CROPS / "raw__train_a_4160.png",
    CROPS / "raw__train_b_4160.png",
    CROPS / "raw__train_a_480_mcc.png",
    CROPS / "raw__train_b_480_mcc.png",
    CROPS / "raw__train_a_dc_ups.png",
    CROPS / "raw__train_b_dc_ups.png",
    CROPS / "raw__center_ties.png",
    CROPS / "raw__a_panel_harness_close.png",
    CROPS / "raw__b_panel_harness_close.png",
    CROPS / "raw__center_panel_control_close.png",
    CROPS / "raw__notes_legend.png",
    CROPS / "raw__title_block.png",
]

diego1_images = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    CROPS / "raw__train_a_4160.png",
    CROPS / "raw__train_b_4160.png",
    CROPS / "raw__train_a_480_mcc.png",
    CROPS / "raw__train_b_480_mcc.png",
    CROPS / "raw__train_a_dc_ups.png",
    CROPS / "raw__train_b_dc_ups.png",
    CROPS / "raw__center_ties.png",
    CROPS / "raw__a_mcc_left_close.png",
    CROPS / "raw__a_mcc_right_close.png",
    CROPS / "raw__b_mcc_left_close.png",
    CROPS / "raw__b_mcc_right_close.png",
    CROPS / "raw__notes_legend.png",
    CROPS / "wire_nodes__train_a_480_mcc.png",
    CROPS / "wire_nodes__train_b_480_mcc.png",
    CROPS / "wire_nodes__center_ties.png",
]

jennifer2_images = [
    RAW,
    DETECTED,
    WIRE_NODES,
    WIRE_MASK,
    CROPS / "raw__train_a_4160.png",
    CROPS / "raw__train_b_4160.png",
    CROPS / "raw__train_a_480_mcc.png",
    CROPS / "raw__train_b_480_mcc.png",
    CROPS / "raw__train_a_dc_ups.png",
    CROPS / "raw__train_b_dc_ups.png",
    CROPS / "raw__center_ties.png",
    CROPS / "raw__a_mcc_left_close.png",
    CROPS / "raw__a_mcc_right_close.png",
    CROPS / "raw__b_mcc_left_close.png",
    CROPS / "raw__b_mcc_right_close.png",
    CROPS / "raw__title_block.png",
    CROPS / "wire_nodes__center_ties.png",
    CROPS / "wire_nodes__train_a_dc_ups.png",
    CROPS / "wire_nodes__train_b_dc_ups.png",
]

diego3_images = [
    RAW,
    CROPS / "raw__left_half.png",
    CROPS / "raw__right_half.png",
    CROPS / "raw__center_ties.png",
    CROPS / "raw__train_a_dc_ups.png",
    CROPS / "raw__train_b_dc_ups.png",
    CROPS / "wire_nodes__center_ties.png",
]

calls = [
    call(
        "main_grouped_visual_artifact",
        "main",
        "orchestration + visual inspection + artifact writing",
        "Document 14 main orchestration, local visual inspection, subagent coordination, crop/artifact writing, validation, token accounting, final response.",
        main_images,
        read_results("round_notes.md", "final_edges.csv", "final_node_order.csv"),
        "Grouped because internal main-agent response boundaries and usage objects are not exposed.",
    ),
    call(
        "diego_round_01_high_recall",
        "Diego",
        "round 1 high recall",
        "High-recall extraction prompt: inspect document 14 raw and derived aids; propose all plausible visible nodes and edges, no GT.",
        diego1_images,
        read_results("round_01_diego_high_recall_node_order.csv", "round_01_diego_high_recall_edges.csv"),
        "Explicit subagent call; usage object not exposed by multi_agent_v1.",
    ),
    call(
        "jennifer_round_02_precision",
        "Jennifer",
        "round 2 precision review",
        "Precision review prompt including Diego's node/edge proposal; remove unsupported pseudo-control nodes and ambiguous panel meshes.",
        jennifer2_images,
        read_results(
            "round_02_jennifer_precision_node_order.csv",
            "round_02_jennifer_precision_edges.csv",
            "uncertain_excluded_edges.csv",
        ),
        "Explicit subagent call; usage object not exposed by multi_agent_v1.",
    ),
    call(
        "diego_round_03_saturation",
        "Diego",
        "round 3 saturation check",
        "Saturation check prompt including Jennifer's refined graph, removals, and label fixes.",
        diego3_images,
        "AGREED SATURATED. Caveats: dashed lower control bundles ambiguous; master terminal compartments have no clear landings; tie breakers retained only as direct bus-tie edges.",
        "Explicit subagent call; usage object not exposed by multi_agent_v1.",
    ),
]


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for c in calls:
        txt = text_tokens(c["input_text"])
        image_low, image_expected, image_high = image_token_range(c["images"])
        out = text_tokens(c["output_text"])
        endpoint_tokens, endpoint_status = endpoint_count(c, c["images"])
        input_expected = endpoint_tokens or (txt + image_expected)
        rows.append(
            {
                "document": c["document"],
                "iteration": c["iteration"],
                "call_id": c["call_id"],
                "agent": c["agent"],
                "round": c["round"],
                "endpoint_status": endpoint_status,
                "input_tokens_endpoint": endpoint_tokens if endpoint_tokens is not None else "",
                "input_text_tokens_est": txt,
                "image_file_input_tokens_low": image_low,
                "image_file_input_tokens_expected": image_expected,
                "image_file_input_tokens_high": image_high,
                "total_input_tokens_low": math.ceil(txt * 0.9 + image_low),
                "total_input_tokens_expected": input_expected,
                "total_input_tokens_high": math.ceil(txt * 1.15 + image_high),
                "cached_input_tokens": "not exposed; estimated 0 for fallback",
                "output_tokens_low": math.floor(out * 0.85),
                "output_tokens_expected": out,
                "output_tokens_high": math.ceil(out * 1.2 + 50),
                "reasoning_tokens": "not exposed",
                "usage_object_available": "no",
                "notes": c["notes"],
            }
        )

    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "document": 14,
        "iteration": 1,
        "model_calls_counted": len(rows),
        "total_tokens_low": sum(int(r["total_input_tokens_low"]) + int(r["output_tokens_low"]) for r in rows),
        "total_tokens_expected": sum(
            int(r["total_input_tokens_expected"]) + int(r["output_tokens_expected"]) for r in rows
        ),
        "total_tokens_high": sum(int(r["total_input_tokens_high"]) + int(r["output_tokens_high"]) for r in rows),
        "usage_objects_collected": "not exposed by Codex/multi_agent_v1 tools",
        "endpoint": "POST /v1/responses/input_tokens",
        "endpoint_result": rows[0]["endpoint_status"],
    }
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    print(RESULTS / "token_usage_estimates.csv")
    print(RESULTS / "token_usage_summary.csv")


if __name__ == "__main__":
    main()
