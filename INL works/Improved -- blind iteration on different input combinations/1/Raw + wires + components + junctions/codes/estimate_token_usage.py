import csv
import json
import math
import os
from pathlib import Path

from PIL import Image
import tiktoken

from generate_connectivity_outputs import (
    FINAL_EDGES,
    FINAL_NODES,
    diego_round_1_edges,
    diego_round_1_label,
)
from matrix_writer import BASE, RESULTS


ENC = None
ENCODING_NAME = "chars_div_4_fallback"
for candidate in ("o200k_base", "cl100k_base", "p50k_base", "gpt2"):
    try:
        ENC = tiktoken.get_encoding(candidate)
        ENCODING_NAME = candidate
        break
    except Exception:
        continue


IMAGE_SETS = {
    "main_agent_orchestration_aggregate": [
        "raw -- schematic_image_clean_100_connected.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        "results/crop_raw_schematic_image_clean_100_connected_top_4kv_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_left_480_feeders_a.png",
        "results/crop_raw_schematic_image_clean_100_connected_center_480_feeders_b.png",
        "results/crop_raw_schematic_image_clean_100_connected_right_480_feeders_c.png",
        "results/crop_raw_schematic_image_clean_100_connected_right_480_feeders_c_full.png",
        "results/crop_raw_schematic_image_clean_100_connected_left_dc_ac_detail.png",
        "results/crop_raw_schematic_image_clean_100_connected_bottom_dc_ac_buses.png",
        "results/crop_detected_components_and_logical_overlay_bottom_dc_ac_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_left_class_1e_4kv_a.png",
        "results/crop_raw_schematic_image_clean_100_connected_center_class_1e_4kv_b.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_a2.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_b2.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_c2.png",
    ],
    "round_01_diego_high_recall": [
        "raw -- schematic_image_clean_100_connected.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        "results/crop_raw_schematic_image_clean_100_connected_top_4kv_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_middle_480_loads.png",
        "results/crop_raw_schematic_image_clean_100_connected_bottom_dc_ac_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_right_480_feeders_c_full.png",
    ],
    "round_02_jennifer_precision": [
        "raw -- schematic_image_clean_100_connected.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        "results/crop_raw_schematic_image_clean_100_connected_top_4kv_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_middle_480_loads.png",
        "results/crop_raw_schematic_image_clean_100_connected_bottom_dc_ac_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_a2.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_b2.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_c2.png",
        "results/crop_raw_schematic_image_clean_100_connected_right_480_feeders_c_full.png",
    ],
    "round_03_diego_saturation": [
        "raw -- schematic_image_clean_100_connected.png",
        "wire_nodes_overlay.png",
        "results/crop_raw_schematic_image_clean_100_connected_top_4kv_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_middle_480_loads.png",
        "results/crop_raw_schematic_image_clean_100_connected_bottom_dc_ac_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_xfmr_a2.png",
        "results/crop_raw_schematic_image_clean_100_connected_right_480_feeders_c_full.png",
    ],
    "round_04_jennifer_final_agreed": [
        "raw -- schematic_image_clean_100_connected.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        "results/crop_raw_schematic_image_clean_100_connected_top_4kv_buses.png",
        "results/crop_raw_schematic_image_clean_100_connected_middle_480_loads.png",
        "results/crop_raw_schematic_image_clean_100_connected_bottom_dc_ac_buses.png",
    ],
}


def count_text(text):
    if ENC is None:
        return math.ceil(len(text) / 4)
    return len(ENC.encode(text))


def high_detail_image_tokens(path):
    image = Image.open(path)
    w, h = image.size
    scale = min(1.0, 2048 / max(w, h))
    w1 = math.ceil(w * scale)
    h1 = math.ceil(h * scale)
    if min(w1, h1) > 768:
        scale = 768 / min(w1, h1)
        w1 = math.ceil(w1 * scale)
        h1 = math.ceil(h1 * scale)
    tiles = math.ceil(w1 / 512) * math.ceil(h1 / 512)
    return 85 + 170 * tiles


def image_tokens_for(call_name):
    return sum(high_detail_image_tokens(BASE / rel) for rel in IMAGE_SETS[call_name])


def diego_round_1_nodes():
    return [diego_round_1_label(node) for node in FINAL_NODES] + [
        "TO 4KV BUS A ELEMENTARY DIAGRAM SH-2",
        "TO 4KV BUS B ELEMENTARY DIAGRAM SH-3",
        "TO AAC BUS C ELEMENTARY DIAGRAM SH-4",
    ]


def graph_json(nodes, edges):
    return json.dumps({"nodes": nodes, "edges": edges}, separators=(",", ":"))


def build_text_payload_estimates():
    wire_csv = (BASE / "wire_nodes.csv").read_text(encoding="utf-8")
    diego_1_json = graph_json(diego_round_1_nodes(), diego_round_1_edges())
    final_json = graph_json(FINAL_NODES, FINAL_EDGES)
    base_instruction = (
        "Use only allowed raw schematic, wires, components, junctions, overlays, and crops. "
        "Do not use ground truth. Extract or review visual schematic connectivity."
    )
    main_visible_context_proxy = (
        base_instruction
        + wire_csv
        + diego_1_json
        + final_json
        + final_json
        + final_json
        + " Main agent also received directory listings, image-inspection notes, "
        + "matrix validation outputs, and subagent status notifications."
    )
    return {
        "main_agent_orchestration_aggregate": count_text(main_visible_context_proxy),
        "round_01_diego_high_recall": count_text(
            base_instruction
            + " Diego high recall extraction with node CSV and instructions. "
            + wire_csv
        ),
        "round_02_jennifer_precision": count_text(
            base_instruction
            + " Jennifer precision review of Diego round 1. "
            + diego_1_json
        ),
        "round_03_diego_saturation": count_text(
            base_instruction
            + " Diego round 2 checks Jennifer refined proposal. "
            + final_json
        ),
        "round_04_jennifer_final_agreed": count_text(
            base_instruction
            + " Jennifer final precision check of saturated candidate. "
            + final_json
        ),
    }


def output_token_estimates():
    diego_1 = count_text(
        graph_json(diego_round_1_nodes(), diego_round_1_edges())
        + " uncertain_edges label_uncertainties notes_for_reviewer"
    )
    final = count_text(graph_json(FINAL_NODES, FINAL_EDGES))
    return {
        "main_agent_orchestration_aggregate": (3500, 5200, 7500),
        "round_01_diego_high_recall": (int(diego_1 * 0.9), diego_1, int(diego_1 * 1.2)),
        "round_02_jennifer_precision": (int(final * 0.95), final + 500, int((final + 500) * 1.2)),
        "round_03_diego_saturation": (int(final * 0.85), final, int(final * 1.1)),
        "round_04_jennifer_final_agreed": (int(final * 0.85), final, int(final * 1.1)),
    }


def main():
    text_inputs = build_text_payload_estimates()
    outputs = output_token_estimates()
    api_key_available = bool(os.environ.get("OPENAI_API_KEY"))
    usage_available = "not_exposed_by_codex_tools"
    doc = "1"
    iteration = "1"
    call_specs = [
        (
            "main_agent_orchestration_aggregate",
            "main",
            "main-agent",
            "aggregate of visible orchestration model calls; exact per-call usage unavailable",
        ),
        (
            "round_01_diego_high_recall",
            "subagent",
            "019f66b6-0255-7c52-af76-ac6947f97785",
            "Diego high-recall extractor",
        ),
        (
            "round_02_jennifer_precision",
            "subagent",
            "019f66bb-70f5-78e2-8015-926e5f12360b",
            "Jennifer precision reviewer",
        ),
        (
            "round_03_diego_saturation",
            "subagent",
            "019f66c0-bed8-72f1-8979-28ac8b1e77cf",
            "Diego saturation check",
        ),
        (
            "round_04_jennifer_final_agreed",
            "subagent",
            "019f66c3-a23a-71a0-8c86-9d81e9f06c33",
            "Jennifer final agreement check",
        ),
    ]

    rows = []
    for call_name, caller, agent_id, notes in call_specs:
        text_tokens = text_inputs[call_name]
        image_tokens = image_tokens_for(call_name)
        out_low, out_expected, out_high = outputs[call_name]
        input_expected = text_tokens + image_tokens
        total_low = input_expected + out_low
        total_expected = input_expected + out_expected
        total_high = int(input_expected * 1.08) + out_high
        rows.append(
            {
                "document": doc,
                "iteration": iteration,
                "call_id": call_name,
                "caller": caller,
                "agent_id": agent_id,
                "usage_object": usage_available,
                "input_text_tokens_est": text_tokens,
                "image_file_input_tokens_est": image_tokens,
                "input_tokens_expected_est": input_expected,
                "cached_input_tokens_recorded": "unavailable",
                "output_tokens_low_est": out_low,
                "output_tokens_expected_est": out_expected,
                "output_tokens_high_est": out_high,
                "reasoning_tokens_recorded": "unavailable",
                "total_tokens_low_est": total_low,
                "total_tokens_expected_est": total_expected,
                "total_tokens_high_est": total_high,
                "notes": notes,
            }
        )

    call_path = RESULTS / "token_usage_call_estimates.csv"
    with call_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    grouped = {
        "document": doc,
        "iteration": iteration,
        "calls_counted": len(rows),
        "openai_api_key_available": api_key_available,
        "responses_input_token_endpoint_used": False,
        "reason_endpoint_not_used": "OPENAI_API_KEY was not available in this environment.",
        "input_tokens_expected_est": sum(r["input_tokens_expected_est"] for r in rows),
        "image_file_input_tokens_est": sum(r["image_file_input_tokens_est"] for r in rows),
        "output_tokens_low_est": sum(r["output_tokens_low_est"] for r in rows),
        "output_tokens_expected_est": sum(r["output_tokens_expected_est"] for r in rows),
        "output_tokens_high_est": sum(r["output_tokens_high_est"] for r in rows),
        "total_tokens_low_est": sum(r["total_tokens_low_est"] for r in rows),
        "total_tokens_expected_est": sum(r["total_tokens_expected_est"] for r in rows),
        "total_tokens_high_est": sum(r["total_tokens_high_est"] for r in rows),
    }
    grouped_path = RESULTS / "token_usage_by_document_iteration.csv"
    with grouped_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(grouped.keys()))
        writer.writeheader()
        writer.writerow(grouped)

    methodology = {
        "method": [
            "The exact OpenAI Responses input-token counting endpoint was not called because no API key was available.",
            "Text token estimates use a local tiktoken encoding when available, otherwise characters / 4.",
            f"Tokenizer actually used: {ENCODING_NAME}.",
            "Image/file input estimates use a local high-detail tile approximation from image dimensions.",
            "Cached input tokens and reasoning tokens were not exposed by Codex or subagent tool responses.",
            "Output estimates use visible/generated JSON payload size where known; main-agent aggregate output is a range.",
        ],
        "official_counting_endpoint": "POST /v1/responses/input_tokens",
        "official_docs": "https://developers.openai.com/api/docs/guides/token-counting",
        "api_key_available": api_key_available,
    }
    (RESULTS / "token_usage_methodology.json").write_text(
        json.dumps(methodology, indent=2), encoding="utf-8"
    )

    print(json.dumps(grouped, indent=2))


if __name__ == "__main__":
    main()
