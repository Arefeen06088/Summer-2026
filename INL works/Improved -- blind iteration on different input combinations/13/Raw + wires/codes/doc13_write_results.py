from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except Exception:  # pragma: no cover - token estimate can fall back to known sizes.
    Image = None


DOC = "13"
ITERATION = "1"
RESOURCE_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires"
)
DEFAULT_OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc13_work\results")
OUT = Path(os.environ.get("DOC13_OUTPUT_DIR", str(DEFAULT_OUT)))

RAW = RESOURCE_DIR / "raw -- synthetic diagram _.png"
OVERLAY = RESOURCE_DIR / "wires_mask_overlay.png"
MASK = RESOURCE_DIR / "wires_mask.png"
CROP_DIR = Path(r"C:\Asif_all_python_projects\INL\INL\doc13_work\crops")


def pairs_from_chain(chain: list[str]) -> list[tuple[str, str]]:
    return list(zip(chain, chain[1:]))


def add_edge(edges: set[tuple[str, str]], a: str, b: str) -> None:
    if a == b:
        raise ValueError(f"self-loop requested for {a}")
    edges.add(tuple(sorted((a, b))))


def add_edges(edges: set[tuple[str, str]], pairs: Iterable[tuple[str, str]]) -> None:
    for a, b in pairs:
        add_edge(edges, a, b)


shared_nodes = [
    "GRID-230KV",
    "SWYD-230",
    "DS-101",
    "CB-101",
    "TR-SUT-1A",
    "TR-SUT-1B",
    "GEN-G1",
    "CB-201",
    "UNIT-GEN-AUX-FEED",
    "TR-UAT-1A",
    "TR-UAT-1B",
    "EDG-A",
    "CB-DGA",
    "EDG-B",
    "CB-DGB",
    "EDG-C",
    "CB-DGC",
    "EDG-D",
    "CB-DGD",
    "CB-TIE-AB",
    "CB-TIE-CD",
]


train_loads = {
    "A": [
        ("CB-A01", "DS-A01", "PMP-SI-A01"),
        ("CB-A02", None, "PMP-RHR-A02"),
        ("CB-A03", "DS-A03", "MTR-CCW-A03"),
        ("CB-A04", None, "FAN-VC-A04"),
        ("CB-A05", None, "MOV-RCS-A05"),
        ("CB-A06", "DS-A06", "PMP-CHG-A06"),
        ("CB-A07", None, "HTR-CAB-A07"),
        ("CB-A08", None, "INST-RK-A08"),
        ("CB-A09", None, "VLV-HPI-A09"),
        ("CB-A10", None, "PNL-ESF-A10"),
    ],
    "B": [
        ("CB-B01", None, "PMP-SI-B01"),
        ("CB-B02", "DS-B02", "PMP-RHR-B02"),
        ("CB-B03", None, "MTR-CCW-B03"),
        ("CB-B04", None, "FAN-VC-B04"),
        ("CB-B05", "DS-B05", "MOV-RCS-B05"),
        ("CB-B06", None, "PMP-CHG-B06"),
        ("CB-B07", None, "HTR-CAB-B07"),
        ("CB-B08", "DS-B08", "INST-RK-B08"),
        ("CB-B09", None, "VLV-HPI-B09"),
        ("CB-B10", None, "PNL-ESF-B10"),
    ],
    "C": [
        ("CB-C01", "DS-C01", "PMP-SI-C01"),
        ("CB-C02", None, "PMP-RHR-C02"),
        ("CB-C03", None, "MTR-CCW-C03"),
        ("CB-C04", "DS-C04", "FAN-VC-C04"),
        ("CB-C05", None, "MOV-RCS-C05"),
        ("CB-C06", None, "PMP-CHG-C06"),
        ("CB-C07", "DS-C07", "HTR-CAB-C07"),
        ("CB-C08", None, "INST-RK-C08"),
        ("CB-C09", None, "VLV-HPI-C09"),
        ("CB-C10", None, "PNL-ESF-C10"),
    ],
    "D": [
        ("CB-D01", None, "PMP-SI-D01"),
        ("CB-D02", "DS-D02", "PMP-RHR-D02"),
        ("CB-D03", None, "MTR-CCW-D03"),
        ("CB-D04", None, "FAN-VC-D04"),
        ("CB-D05", None, "MOV-RCS-D05"),
        ("CB-D06", "DS-D06", "PMP-CHG-D06"),
        ("CB-D07", None, "HTR-CAB-D07"),
        ("CB-D08", None, "INST-RK-D08"),
        ("CB-D09", "DS-D09", "VLV-HPI-D09"),
        ("CB-D10", None, "PNL-ESF-D10"),
    ],
}

relay_edges_by_train = {
    "A": [
        ("RLY-KA01", "CB-A01"),
        ("RLY-KA02", "CB-A02"),
        ("RLY-KA05", "CB-A05"),
        ("RLY-KA07", "CB-A07"),
    ],
    "B": [
        ("RLY-KB02", "CB-B02"),
        ("RLY-KB04", "CB-B04"),
        ("RLY-KB06", "CB-B06"),
    ],
    "C": [
        ("RLY-KC01", "CB-C01"),
        ("RLY-KC03", "CB-C03"),
        ("RLY-KC08", "CB-C08"),
    ],
    "D": [
        ("RLY-KD02", "CB-D02"),
        ("RLY-KD05", "CB-D05"),
        ("RLY-KD07", "CB-D07"),
        ("RLY-KD10", "CB-D10"),
    ],
}


def train_nodes(t: str) -> list[str]:
    nodes = [
        f"BUS-4{t}",
        f"CB-4{t}-48",
        f"TR-480{t}",
        f"CB-48{t}",
        f"LC-480{t}",
        f"PP-{t}1",
        f"MCC-{t}1",
        f"MCC-{t}2",
        f"LOCAL-I/O-{t}",
        f"JB-{t}1",
        f"BAT-125{t}",
        f"CHG-125{t}",
        f"DC-BUS-{t}",
        f"INV-{t}",
        f"UPS-{t}",
    ]
    for cb, ds, load in train_loads[t]:
        nodes.append(cb)
        if ds:
            nodes.append(ds)
        nodes.append(load)
    nodes.extend(a for a, _ in relay_edges_by_train[t])
    return nodes


final_nodes = shared_nodes + train_nodes("A") + train_nodes("B") + train_nodes("C") + train_nodes("D")


def build_final_edges() -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    add_edges(edges, pairs_from_chain(["GRID-230KV", "SWYD-230", "DS-101", "CB-101"]))
    add_edges(edges, [("CB-101", "TR-SUT-1A"), ("CB-101", "TR-SUT-1B")])
    add_edges(edges, [("TR-SUT-1A", "BUS-4A"), ("TR-SUT-1B", "BUS-4A")])
    add_edges(edges, pairs_from_chain(["EDG-A", "CB-DGA", "BUS-4A"]))
    add_edges(edges, pairs_from_chain(["BUS-4A", "CB-TIE-AB", "BUS-4B"]))
    add_edges(edges, pairs_from_chain(["EDG-B", "CB-DGB", "BUS-4B"]))
    add_edges(edges, pairs_from_chain(["GEN-G1", "CB-201", "UNIT-GEN-AUX-FEED"]))
    add_edges(edges, pairs_from_chain(["UNIT-GEN-AUX-FEED", "TR-UAT-1A", "BUS-4C"]))
    add_edges(edges, pairs_from_chain(["UNIT-GEN-AUX-FEED", "TR-UAT-1B", "BUS-4D"]))
    add_edges(edges, pairs_from_chain(["EDG-C", "CB-DGC", "BUS-4C"]))
    add_edges(edges, pairs_from_chain(["BUS-4C", "CB-TIE-CD", "BUS-4D"]))
    add_edges(edges, pairs_from_chain(["EDG-D", "CB-DGD", "BUS-4D"]))

    for t in "ABCD":
        add_edges(edges, pairs_from_chain([f"BUS-4{t}", f"CB-4{t}-48", f"TR-480{t}", f"CB-48{t}", f"LC-480{t}"]))
        for node in [f"PP-{t}1", f"MCC-{t}1", f"MCC-{t}2", f"LOCAL-I/O-{t}", f"JB-{t}1"]:
            add_edge(edges, f"LC-480{t}", node)
        add_edge(edges, f"PP-{t}1", f"UPS-{t}")
        add_edges(edges, pairs_from_chain([f"BAT-125{t}", f"CHG-125{t}", f"DC-BUS-{t}", f"INV-{t}", f"UPS-{t}"]))
        add_edge(edges, f"JB-{t}1", f"DC-BUS-{t}")

        for index, (cb, ds, load) in enumerate(train_loads[t], start=1):
            mcc = f"MCC-{t}1" if index <= 5 else f"MCC-{t}2"
            add_edge(edges, mcc, cb)
            if ds:
                add_edge(edges, cb, ds)
                add_edge(edges, ds, load)
            else:
                add_edge(edges, cb, load)
        add_edges(edges, relay_edges_by_train[t])
    return edges


final_edges = build_final_edges()

restored_visual_edges = set()
for train in "ABCD":
    add_edge(restored_visual_edges, f"INV-{train}", f"UPS-{train}")
    add_edge(restored_visual_edges, f"JB-{train}1", f"DC-BUS-{train}")
    add_edges(restored_visual_edges, relay_edges_by_train[train])

jennifer_r1_edges = final_edges - restored_visual_edges

diego_r1_extra_nodes = [
    "GND-A",
    "GND-B",
    "GND-C",
    "GND-D",
    "GND-PLANT",
    "CONTINUATION TO 125 VDC SYSTEM SHT-DC-2",
    "TO ANNUNCIATOR / PLANT PROCESS COMPUTER",
]
diego_r1_extra_edges: set[tuple[str, str]] = set()
for t in "ABCD":
    add_edge(diego_r1_extra_edges, f"LC-480{t}", f"CHG-125{t}")
for g in ["GND-A", "GND-B", "GND-C", "GND-D"]:
    add_edge(diego_r1_extra_edges, g, "GND-PLANT")
add_edge(diego_r1_extra_edges, "DC-BUS-C", "CONTINUATION TO 125 VDC SYSTEM SHT-DC-2")
add_edge(diego_r1_extra_edges, "BUS-4D", "TO ANNUNCIATOR / PLANT PROCESS COMPUTER")

rounds = [
    {
        "slug": "round_01_diego_high_recall",
        "agent": "Diego",
        "nodes": final_nodes + diego_r1_extra_nodes,
        "edges": sorted(final_edges | diego_r1_extra_edges),
        "uncertain_edges": sorted(diego_r1_extra_edges),
        "notes": "High-recall proposal; includes plausible but later excluded label/ground/continuation edges.",
    },
    {
        "slug": "round_01_jennifer_precision",
        "agent": "Jennifer",
        "nodes": final_nodes,
        "edges": sorted(jennifer_r1_edges),
        "uncertain_edges": sorted(restored_visual_edges),
        "notes": "Precision pass; demoted dashed/control and inverter-to-UPS visual links to uncertain.",
    },
    {
        "slug": "round_02_diego_saturation",
        "agent": "Diego",
        "nodes": final_nodes,
        "edges": sorted(final_edges),
        "uncertain_edges": [],
        "notes": "Saturation pass; restored visibly terminating dashed/control and inverter-to-UPS links.",
    },
    {
        "slug": "round_02_jennifer_final",
        "agent": "Jennifer",
        "nodes": final_nodes,
        "edges": sorted(final_edges),
        "uncertain_edges": [],
        "notes": "Final precision agreement with visual/geometric policy.",
    },
]


edge_evidence = {
    "source": "visually traced in raw schematic plus wires_mask_overlay",
    "policy": "solid or dashed lines that visibly terminate on components/buses count as undirected visual edges; crossings and off-page annotations do not",
}


def write_matrix(path: Path, nodes: list[str], edges: Iterable[tuple[str, str]]) -> None:
    edge_set = {tuple(sorted(e)) for e in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for row in nodes:
            writer.writerow([row] + [0 if row == col else int(tuple(sorted((row, col))) in edge_set) for col in nodes])


def write_edges(path: Path, edges: Iterable[tuple[str, str]], include_evidence: bool = True) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["source", "target"]
        if include_evidence:
            fieldnames += ["edge_type", "evidence"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for a, b in sorted(edges):
            row = {"source": a, "target": b}
            if include_evidence:
                row["edge_type"] = "visual_schematic"
                row["evidence"] = edge_evidence["policy"]
            writer.writerow(row)


def write_sparse_matrix(path: Path, nodes: list[str], edges: Iterable[tuple[str, str]]) -> None:
    edge_set = {tuple(sorted(e)) for e in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "connected"])
        for i, a in enumerate(nodes):
            for b in nodes[i + 1 :]:
                writer.writerow([a, b, int(tuple(sorted((a, b))) in edge_set)])


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def token_image_estimate(path: Path) -> int:
    if Image is not None and path.exists():
        with Image.open(path) as img:
            w, h = img.size
    else:
        # Fallback for the doc13 full-sheet images.
        w, h = 6400, 4300
    return math.ceil(w / 32) * math.ceil(h / 32)


def token_low_expected_high(expected: int) -> tuple[int, int, int]:
    return (math.ceil(expected * 0.75), expected, math.ceil(expected * 1.35))


def write_token_usage() -> None:
    images = {
        "full_raw": RAW,
        "full_overlay": OVERLAY,
        "startup_crop": CROP_DIR / "raw_startup_feed_top_left.png",
        "train_a": CROP_DIR / "raw_train_A_upper_left.png",
        "train_b": CROP_DIR / "raw_train_B_upper_right.png",
        "train_c": CROP_DIR / "raw_train_C_lower_left.png",
        "train_d": CROP_DIR / "raw_train_D_lower_right.png",
        "train_a_dc": CROP_DIR / "raw_train_A_dc_right.png",
        "train_b_dc": CROP_DIR / "raw_train_B_dc_right.png",
        "train_c_dc": CROP_DIR / "raw_train_C_dc_right.png",
        "train_d_dc": CROP_DIR / "raw_train_D_dc_right.png",
        "middle": CROP_DIR / "raw_middle_intertrain_bus.png",
        "bottom": CROP_DIR / "raw_bottom_ground_and_dc.png",
        "overlay_full_left": CROP_DIR / "overlay_full_left_logic.png",
        "grid_r1c1": CROP_DIR / "raw_grid_r1_c1.png",
        "grid_r1c2": CROP_DIR / "raw_grid_r1_c2.png",
        "grid_r1c3": CROP_DIR / "raw_grid_r1_c3.png",
        "grid_r2c1": CROP_DIR / "raw_grid_r2_c1.png",
        "grid_r2c2": CROP_DIR / "raw_grid_r2_c2.png",
        "grid_r2c3": CROP_DIR / "raw_grid_r2_c3.png",
    }
    image_tokens = {name: token_image_estimate(path) for name, path in images.items()}

    call_specs = [
        {
            "document": DOC,
            "iteration": ITERATION,
            "call": "main_agent_orchestration",
            "model": "gpt-5",
            "text_input_expected": 22000,
            "image_expected": sum(
                image_tokens[n]
                for n in [
                    "full_raw",
                    "full_overlay",
                    "startup_crop",
                    "train_a",
                    "train_b",
                    "train_c",
                    "train_d",
                    "grid_r1c1",
                    "grid_r1c2",
                    "grid_r1c3",
                    "grid_r2c1",
                    "grid_r2c2",
                    "grid_r2c3",
                    "overlay_full_left",
                    "train_a_dc",
                    "middle",
                ]
            ),
            "output_expected": 2500,
            "reasoning_expected": 9000,
            "notes": "Estimated from visible tool context; API usage object unavailable.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "call": "Diego_R1_high_recall",
            "model": "gpt-5.5",
            "text_input_expected": 900,
            "image_expected": sum(
                image_tokens[n]
                for n in [
                    "full_raw",
                    "full_overlay",
                    "startup_crop",
                    "train_a",
                    "train_b",
                    "train_c",
                    "train_d",
                    "middle",
                    "bottom",
                    "overlay_full_left",
                ]
            ),
            "output_expected": 4200,
            "reasoning_expected": 6500,
            "notes": "Subagent model response usage object not exposed to main agent.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "call": "Jennifer_R1_precision",
            "model": "gpt-5.5",
            "text_input_expected": 5200,
            "image_expected": sum(
                image_tokens[n]
                for n in [
                    "full_raw",
                    "full_overlay",
                    "startup_crop",
                    "train_a",
                    "train_b",
                    "train_c",
                    "train_d",
                    "grid_r1c1",
                    "grid_r1c2",
                    "grid_r1c3",
                    "grid_r2c1",
                    "grid_r2c2",
                    "grid_r2c3",
                    "train_a_dc",
                    "overlay_full_left",
                ]
            ),
            "output_expected": 2600,
            "reasoning_expected": 5500,
            "notes": "Includes Diego R1 proposal text plus images.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "call": "Diego_R2_saturation",
            "model": "gpt-5.5",
            "text_input_expected": 1600,
            "image_expected": sum(
                image_tokens[n]
                for n in [
                    "full_raw",
                    "full_overlay",
                    "train_a",
                    "train_b",
                    "train_c",
                    "train_d",
                    "train_a_dc",
                    "train_b_dc",
                    "train_c_dc",
                    "train_d_dc",
                    "overlay_full_left",
                ]
            ),
            "output_expected": 900,
            "reasoning_expected": 3500,
            "notes": "Saturation check of disputed visual edges.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "call": "Jennifer_R2_final",
            "model": "gpt-5.5",
            "text_input_expected": 900,
            "image_expected": sum(
                image_tokens[n]
                for n in [
                    "full_raw",
                    "full_overlay",
                    "train_a_dc",
                    "train_b_dc",
                    "train_c_dc",
                    "train_d_dc",
                    "train_a",
                    "train_b",
                    "train_c",
                    "train_d",
                    "overlay_full_left",
                ]
            ),
            "output_expected": 700,
            "reasoning_expected": 3000,
            "notes": "Final agreement on visual/geometric edge policy.",
        },
    ]

    with (OUT / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "document",
            "iteration",
            "call",
            "model",
            "text_input_tokens_low",
            "text_input_tokens_expected",
            "text_input_tokens_high",
            "cached_input_tokens",
            "image_file_input_tokens_low",
            "image_file_input_tokens_expected",
            "image_file_input_tokens_high",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens_low",
            "reasoning_tokens_expected",
            "reasoning_tokens_high",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
            "usage_object_available",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        totals = [0, 0, 0]
        for spec in call_specs:
            text_l, text_e, text_h = token_low_expected_high(spec["text_input_expected"])
            img_l, img_e, img_h = token_low_expected_high(spec["image_expected"])
            out_l, out_e, out_h = token_low_expected_high(spec["output_expected"])
            rsn_l, rsn_e, rsn_h = token_low_expected_high(spec["reasoning_expected"])
            low = text_l + img_l + out_l + rsn_l
            expected = text_e + img_e + out_e + rsn_e
            high = text_h + img_h + out_h + rsn_h
            totals[0] += low
            totals[1] += expected
            totals[2] += high
            writer.writerow(
                {
                    "document": spec["document"],
                    "iteration": spec["iteration"],
                    "call": spec["call"],
                    "model": spec["model"],
                    "text_input_tokens_low": text_l,
                    "text_input_tokens_expected": text_e,
                    "text_input_tokens_high": text_h,
                    "cached_input_tokens": 0,
                    "image_file_input_tokens_low": img_l,
                    "image_file_input_tokens_expected": img_e,
                    "image_file_input_tokens_high": img_h,
                    "output_tokens_low": out_l,
                    "output_tokens_expected": out_e,
                    "output_tokens_high": out_h,
                    "reasoning_tokens_low": rsn_l,
                    "reasoning_tokens_expected": rsn_e,
                    "reasoning_tokens_high": rsn_h,
                    "total_tokens_low": low,
                    "total_tokens_expected": expected,
                    "total_tokens_high": high,
                    "usage_object_available": "no",
                    "notes": spec["notes"],
                }
            )

    summary = [
        "# Token Usage Estimate",
        "",
        "No OpenAI API key or Responses token-counting endpoint access was available in this environment, and subagent usage objects were not exposed to the main agent. Estimates use local text bands plus image token proxies of ceil(width/32) * ceil(height/32). Cached input tokens are recorded as 0/unknown.",
        "",
        "| document | iteration | calls | low | expected | high |",
        "|---|---:|---:|---:|---:|---:|",
        f"| {DOC} | {ITERATION} | {len(call_specs)} | {totals[0]} | {totals[1]} | {totals[2]} |",
        "",
        "Image proxy token estimates:",
    ]
    for name, value in sorted(image_tokens.items()):
        summary.append(f"- {name}: {value}")
    (OUT / "token_usage_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    for round_info in rounds:
        slug = round_info["slug"]
        nodes = round_info["nodes"]
        edges = round_info["edges"]
        write_nodes(OUT / f"nodes_{slug}.csv", nodes)
        write_edges(OUT / f"edges_{slug}.csv", edges)
        write_edges(OUT / f"uncertain_edges_{slug}.csv", round_info["uncertain_edges"], include_evidence=False)
        write_matrix(OUT / f"connectivity_matrix_{slug}.csv", nodes, edges)
        write_sparse_matrix(OUT / f"connectivity_sparse_{slug}.csv", nodes, edges)

    write_nodes(OUT / "nodes_final.csv", final_nodes)
    write_edges(OUT / "edges_final.csv", sorted(final_edges))
    write_edges(OUT / "uncertain_edges_final.csv", [], include_evidence=False)
    write_matrix(OUT / "connectivity_matrix_final.csv", final_nodes, sorted(final_edges))
    write_sparse_matrix(OUT / "connectivity_sparse_final.csv", final_nodes, sorted(final_edges))

    duplicates = sorted({n for n in final_nodes if final_nodes.count(n) > 1})
    endpoints = {n for edge in final_edges for n in edge}
    missing_endpoints = sorted(endpoints - set(final_nodes))
    isolated = sorted(set(final_nodes) - endpoints)
    qa = {
        "document": DOC,
        "iteration": ITERATION,
        "node_count_final": len(final_nodes),
        "edge_count_final": len(final_edges),
        "duplicates": duplicates,
        "missing_edge_endpoints": missing_endpoints,
        "isolated_nodes_final": isolated,
        "diagonal_policy": "all zero; no self-loops justified",
        "symmetry": "matrix writer mirrors undirected edge set",
        "final_policy": edge_evidence["policy"],
        "excluded_policy": "unsupported crossings, proximity-only labels, off-page continuation arrows, and ground/reference labels excluded",
        "source_files": [str(RAW), str(OVERLAY), str(MASK)],
    }
    (OUT / "qa_final.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")

    notes = [
        "# Document 13 Round Notes",
        "",
        "Inputs used: raw schematic, wires mask, wires mask overlay, and local crops derived from those same files. No GT or GT-derived resources were used.",
        "",
        "| round | agent | matrix | notes |",
        "|---|---|---|---|",
    ]
    for round_info in rounds:
        slug = round_info["slug"]
        notes.append(
            f"| {slug} | {round_info['agent']} | connectivity_matrix_{slug}.csv | {round_info['notes']} |"
        )
    notes.extend(
        [
            "",
            "Final saturation: Jennifer R2 agreed with Diego R2 that the requested visual/geometric matrix should include visibly terminating dashed/control links and solid inverter-to-UPS links.",
            "",
            "Final excluded classes: unsupported crossings, continuation arrows without a component termination, ground/reference labels, and label-only associations.",
        ]
    )
    (OUT / "round_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    write_token_usage()

    print(json.dumps({"out": str(OUT), "nodes": len(final_nodes), "edges": len(final_edges)}, indent=2))


if __name__ == "__main__":
    main()
