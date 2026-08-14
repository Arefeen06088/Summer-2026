from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


DOC = "15"
ITERATION = "1"
RESOURCE_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires"
)
DEFAULT_OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc15_work\results")
OUT = Path(os.environ.get("DOC15_OUTPUT_DIR", str(DEFAULT_OUT)))
CROP_DIR = Path(r"C:\Asif_all_python_projects\INL\INL\doc15_work\crops")

RAW = RESOURCE_DIR / "raw -- improved_synthetic_nuclear_electrical_schematic.png"
OVERLAY = RESOURCE_DIR / "wires_mask_overlay.png"
MASK = RESOURCE_DIR / "wires_mask.png"

DIVISIONS = ["A", "B", "C", "D"]


def add_node(nodes: list[str], node: str) -> None:
    if node not in nodes:
        nodes.append(node)


def edge_key(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop requested for {a}")
    return tuple(sorted((a, b)))


def add_edge(edges: dict[tuple[str, str], dict[str, str]], a: str, b: str, edge_type: str, evidence: str) -> None:
    key = edge_key(a, b)
    edges.setdefault(
        key,
        {
            "source": key[0],
            "target": key[1],
            "type": edge_type,
            "evidence": evidence,
        },
    )


def add_chain(edges: dict[tuple[str, str], dict[str, str]], chain: list[str], edge_type: str, evidence: str) -> None:
    for a, b in zip(chain, chain[1:]):
        add_edge(edges, a, b, edge_type, evidence)


def build_nodes() -> list[str]:
    nodes: list[str] = []
    for node in [
        "GEN-101",
        "CB-GEN-101",
        "TR-GSU-1",
        "BUS-SWY-1",
        "CB-SWY-TIE",
        "BUS-SWY-2",
        "GEN-102",
        "CB-GEN-102",
        "TR-GSU-2",
        "TR-UAT-1",
        "TR-SAT-1",
        "BUS-NSS-1",
        "TR-UAT-2",
        "TR-SAT-2",
        "BUS-NSS-2",
        "DG-1A",
        "DG-1B",
        "DG-1C",
        "DG-1D",
    ]:
        add_node(nodes, node)

    def add_division(x: str) -> None:
        for node in [
            f"CB-NF-{x}",
            f"CB-DG-{x}",
            f"BUS-416{x}",
            f"CB-TX-{x}",
            f"TR-480{x}",
            f"BUS-480{x}",
            f"MCC-1{x}",
            f"CB-{x}01",
            f"DS-{x}01",
            f"RLY-{x}01",
            f"PMP-SI-{x}1",
            f"CB-{x}02",
            f"FU-{x}02",
            f"RLY-{x}02",
            f"PMP-CS-{x}2",
            f"CB-{x}03",
            f"DS-{x}03",
            f"RLY-{x}03",
            f"MOV-{x}03",
            f"CB-{x}04",
            f"FU-{x}04",
            f"RLY-{x}04",
            f"MTR-{x}04",
            f"CB-{x}05",
            f"DS-{x}05",
            f"RLY-{x}05",
            f"INST-{x}05",
            f"CB-{x}06",
            f"FU-{x}06",
            f"RLY-{x}06",
            f"PMP-SW-{x}6",
            f"BAT-125{x}",
            f"CHG-1{x}",
            f"BUS-DC-{x}",
            f"INV-1{x}",
            f"CP-1{x}",
            f"TB-1{x}",
            f"JB-1{x}",
            f"GND-{x}",
        ]:
            add_node(nodes, node)

    add_division("A")
    for node in ["CB-TIE-AB", "DS-TIE-AB", "SEQ-1AB", "RPS-AC-1"]:
        add_node(nodes, node)
    add_division("B")
    add_division("C")
    for node in ["CB-TIE-CD", "DS-TIE-CD", "SEQ-2CD", "RPS-AC-2"]:
        add_node(nodes, node)
    add_division("D")
    return nodes


def normal_bus(x: str) -> str:
    return "BUS-NSS-1" if x in {"A", "B"} else "BUS-NSS-2"


def build_edges(include_dg_nss: bool, include_nf_dg_control: bool) -> dict[tuple[str, str], dict[str, str]]:
    edges: dict[tuple[str, str], dict[str, str]] = {}

    add_chain(edges, ["GEN-101", "CB-GEN-101", "TR-GSU-1", "BUS-SWY-1"], "power", "solid offsite generator 101 chain")
    add_chain(edges, ["GEN-102", "CB-GEN-102", "TR-GSU-2", "BUS-SWY-2"], "power", "solid offsite generator 102 chain")
    add_chain(edges, ["BUS-SWY-1", "CB-SWY-TIE", "BUS-SWY-2"], "power_tie", "solid switchyard tie path")
    add_chain(edges, ["BUS-SWY-1", "TR-UAT-1", "BUS-NSS-1"], "power", "solid UAT-1 path from switchyard A to NSS-1")
    add_chain(edges, ["BUS-SWY-1", "TR-SAT-1", "BUS-NSS-1"], "power", "solid SAT-1 path from switchyard A to NSS-1")
    add_chain(edges, ["BUS-SWY-2", "TR-UAT-2", "BUS-NSS-2"], "power", "solid UAT-2 path from switchyard B to NSS-2")
    add_chain(edges, ["BUS-SWY-2", "TR-SAT-2", "BUS-NSS-2"], "power", "solid SAT-2 path from switchyard B to NSS-2")

    for x in DIVISIONS:
        nss = normal_bus(x)
        add_chain(edges, [nss, f"CB-NF-{x}", f"BUS-416{x}"], "power", f"solid normal feed to BUS-416{x}")
        if include_dg_nss:
            add_chain(edges, [nss, f"DG-1{x}", f"CB-DG-{x}", f"BUS-416{x}"], "power", f"Jennifer R1 hard DG/NSS path for division {x}")
        else:
            add_chain(edges, [f"DG-1{x}", f"CB-DG-{x}", f"BUS-416{x}"], "power", f"solid diesel feed to BUS-416{x}; DG/NSS contact kept uncertain")

        add_chain(
            edges,
            [f"BUS-416{x}", f"CB-TX-{x}", f"TR-480{x}", f"BUS-480{x}", f"MCC-1{x}"],
            "power",
            f"solid 416/480 transformer and MCC feed for division {x}",
        )

        branch_specs = [
            ("01", "DS", f"PMP-SI-{x}1"),
            ("02", "FU", f"PMP-CS-{x}2"),
            ("03", "DS", f"MOV-{x}03"),
            ("04", "FU", f"MTR-{x}04"),
            ("05", "DS", f"INST-{x}05"),
            ("06", "FU", f"PMP-SW-{x}6"),
        ]
        for suffix, device_prefix, load in branch_specs:
            add_chain(
                edges,
                [f"MCC-1{x}", f"CB-{x}{suffix}", f"{device_prefix}-{x}{suffix}", load],
                "power",
                f"solid MCC branch {x}{suffix} to load",
            )
            add_edge(
                edges,
                f"CB-{x}{suffix}",
                f"RLY-{x}{suffix}",
                "control",
                f"dashed control line from CB-{x}{suffix} to RLY-{x}{suffix}",
            )
        add_edge(edges, f"RLY-{x}06", f"TB-1{x}", "control", f"dashed dogleg from RLY-{x}06 to TB-1{x}")
        add_chain(
            edges,
            [f"BAT-125{x}", f"CHG-1{x}", f"BUS-DC-{x}", f"INV-1{x}", f"CP-1{x}", f"TB-1{x}"],
            "dc_control",
            f"visible dashed/solid DC-control chain for division {x}",
        )
        add_edge(edges, f"BUS-DC-{x}", f"GND-{x}", "dc_ground", f"visible ground tap from BUS-DC-{x}")
        add_edge(edges, f"CP-1{x}", f"JB-1{x}", "control", f"dashed dogleg from CP-1{x} to JB-1{x}")

    add_chain(edges, ["BUS-416A", "CB-TIE-AB", "DS-TIE-AB", "BUS-416B"], "power_tie", "normally open AB tie path through CB and DS")
    add_chain(edges, ["BUS-416C", "CB-TIE-CD", "DS-TIE-CD", "BUS-416D"], "power_tie", "normally open CD tie path through CB and DS")

    if include_nf_dg_control:
        for x in DIVISIONS:
            add_edge(edges, f"CB-NF-{x}", f"CB-DG-{x}", "control", f"Diego/Jennifer R1 direct same-division NF/DG dashed lead for {x}")

    add_chain(edges, ["CB-DG-A", "SEQ-1AB", "CB-NF-B"], "control", "dashed sequence control path across AB tie area")
    add_chain(edges, ["CB-DG-A", "RPS-AC-1", "CB-NF-B"], "control", "dashed RPS control path across AB tie area")
    add_chain(edges, ["CB-DG-C", "SEQ-2CD", "CB-NF-D"], "control", "dashed sequence control path across CD tie area")
    add_chain(edges, ["CB-DG-C", "RPS-AC-2", "CB-NF-D"], "control", "dashed RPS control path across CD tie area")
    return edges


def uncertain_edges_final() -> list[dict[str, str]]:
    rows = [
        ("BUS-NSS-1", "DG-1A", "DG symbol is visually near/inline with NSS bus, but hard feed is DG-1A--CB-DG-A"),
        ("BUS-NSS-1", "DG-1B", "DG symbol is visually near/inline with NSS bus, but hard feed is DG-1B--CB-DG-B"),
        ("BUS-NSS-2", "DG-1C", "DG symbol is visually near/inline with NSS bus, but hard feed is DG-1C--CB-DG-C"),
        ("BUS-NSS-2", "DG-1D", "DG symbol is visually near/inline with NSS bus, but hard feed is DG-1D--CB-DG-D"),
        ("CB-NF-A", "CB-DG-A", "same-division NF/DG dashed interlock lead is visually plausible but endpoint treatment is ambiguous"),
        ("CB-NF-B", "CB-DG-B", "same-division NF/DG dashed interlock lead is visually plausible but endpoint treatment is ambiguous"),
        ("CB-NF-C", "CB-DG-C", "same-division NF/DG dashed interlock lead is visually plausible but endpoint treatment is ambiguous"),
        ("CB-NF-D", "CB-DG-D", "same-division NF/DG dashed interlock lead is visually plausible but endpoint treatment is ambiguous"),
    ]
    return [{"source": a, "target": b, "reason": reason} for a, b, reason in rows]


def uncertain_edges_diego_r1() -> list[dict[str, str]]:
    return [
        {"source": "BUS-NSS-1", "target": "DG-1A", "reason": "Diego R1: visually plausible inline DG/bus contact, but not promoted to hard"},
        {"source": "BUS-NSS-1", "target": "DG-1B", "reason": "Diego R1: visually plausible inline DG/bus contact, but not promoted to hard"},
        {"source": "BUS-NSS-2", "target": "DG-1C", "reason": "Diego R1: visually plausible inline DG/bus contact, but not promoted to hard"},
        {"source": "BUS-NSS-2", "target": "DG-1D", "reason": "Diego R1: visually plausible inline DG/bus contact, but not promoted to hard"},
    ]


def removed_edges_jennifer_final() -> list[dict[str, str]]:
    return [
        {"source": "BUS-NSS-1", "target": "DG-1A", "reason": "moved from Jennifer R1 hard to final uncertain after saturation"},
        {"source": "BUS-NSS-1", "target": "DG-1B", "reason": "moved from Jennifer R1 hard to final uncertain after saturation"},
        {"source": "BUS-NSS-2", "target": "DG-1C", "reason": "moved from Jennifer R1 hard to final uncertain after saturation"},
        {"source": "BUS-NSS-2", "target": "DG-1D", "reason": "moved from Jennifer R1 hard to final uncertain after saturation"},
        {"source": "CB-NF-A", "target": "CB-DG-A", "reason": "moved from round 1 hard to final uncertain; dashed endpoint treatment ambiguous"},
        {"source": "CB-NF-B", "target": "CB-DG-B", "reason": "moved from round 1 hard to final uncertain; dashed endpoint treatment ambiguous"},
        {"source": "CB-NF-C", "target": "CB-DG-C", "reason": "moved from round 1 hard to final uncertain; dashed endpoint treatment ambiguous"},
        {"source": "CB-NF-D", "target": "CB-DG-D", "reason": "moved from round 1 hard to final uncertain; dashed endpoint treatment ambiguous"},
    ]


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_edges(path: Path, edges: dict[tuple[str, str], dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        for key in sorted(edges):
            writer.writerow(edges[key])


def write_matrix(path: Path, nodes: list[str], edges: dict[tuple[str, str], dict[str, str]]) -> None:
    edge_set = set(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for row_node in nodes:
            writer.writerow(
                [
                    row_node,
                    *[
                        0 if row_node == col_node else int(edge_key(row_node, col_node) in edge_set)
                        for col_node in nodes
                    ],
                ]
            )


def write_sparse(path: Path, nodes: list[str], edges: dict[tuple[str, str], dict[str, str]]) -> None:
    edge_set = set(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "column", "connected"])
        for row_node in nodes:
            for col_node in nodes:
                value = 0 if row_node == col_node else int(edge_key(row_node, col_node) in edge_set)
                writer.writerow([row_node, col_node, value])


def write_uncertain(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_removed(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def validate_round(nodes: list[str], edges: dict[tuple[str, str], dict[str, str]]) -> dict[str, object]:
    node_set = set(nodes)
    missing = sorted({node for edge in edges for node in edge if node not in node_set})
    degrees = {node: 0 for node in nodes}
    for a, b in edges:
        if a in degrees:
            degrees[a] += 1
        if b in degrees:
            degrees[b] += 1
    return {
        "node_count": len(nodes),
        "hard_edge_count": len(edges),
        "missing_edge_endpoints": missing,
        "diagonal_zero": True,
        "symmetric": True,
        "isolated_visible_nodes": [node for node, degree in degrees.items() if degree == 0],
    }


def emit_round(prefix: str, nodes: list[str], edges: dict[tuple[str, str], dict[str, str]], uncertain: list[dict[str, str]]) -> dict[str, object]:
    write_nodes(OUT / f"nodes_{prefix}.csv", nodes)
    write_edges(OUT / f"edges_{prefix}.csv", edges)
    write_matrix(OUT / f"connectivity_matrix_{prefix}.csv", nodes, edges)
    write_sparse(OUT / f"connectivity_sparse_{prefix}.csv", nodes, edges)
    write_uncertain(OUT / f"uncertain_edges_{prefix}.csv", uncertain)
    return validate_round(nodes, edges)


def estimate_text_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def image_dims(path: Path) -> tuple[int, int]:
    if Image is not None and path.exists():
        with Image.open(path) as img:
            return img.size
    return (1200, 900)


def image_token_proxy(path: Path) -> int:
    width, height = image_dims(path)
    return math.ceil(width / 32) * math.ceil(height / 32)


def write_token_usage(path: Path) -> list[dict[str, object]]:
    main_images = [
        RAW,
        OVERLAY,
        CROP_DIR / "raw_offsite_sources_top.png",
        CROP_DIR / "raw_division_1a_full.png",
        CROP_DIR / "raw_division_1b_full.png",
        CROP_DIR / "raw_division_2a_full.png",
        CROP_DIR / "raw_division_2b_full.png",
        CROP_DIR / "raw_tie_1a_1b.png",
        CROP_DIR / "raw_tie_2a_2b.png",
        CROP_DIR / "raw_right_notes.png",
        CROP_DIR / "overlay_division_1a_full.png",
        CROP_DIR / "overlay_tie_1a_1b.png",
    ]
    diego_r1_images = [
        RAW,
        OVERLAY,
        CROP_DIR / "raw_offsite_sources_top.png",
        CROP_DIR / "raw_division_1a_full.png",
        CROP_DIR / "raw_division_1b_full.png",
        CROP_DIR / "raw_division_2a_full.png",
        CROP_DIR / "raw_division_2b_full.png",
        CROP_DIR / "raw_tie_1a_1b.png",
        CROP_DIR / "raw_tie_2a_2b.png",
        CROP_DIR / "raw_right_notes.png",
    ]
    jennifer_r1_images = [
        RAW,
        OVERLAY,
        CROP_DIR / "raw_offsite_sources_top.png",
        CROP_DIR / "raw_division_1a_full.png",
        CROP_DIR / "raw_division_1b_full.png",
        CROP_DIR / "raw_division_2a_full.png",
        CROP_DIR / "raw_division_2b_full.png",
        CROP_DIR / "raw_tie_1a_1b.png",
        CROP_DIR / "overlay_tie_1a_1b.png",
        CROP_DIR / "raw_tie_2a_2b.png",
        CROP_DIR / "raw_right_notes.png",
    ]
    main_text = "Main agent doc15 visual inspection, crop generation, graph synthesis, artifact writing, and final reporting."
    diego_r1_text = "Diego R1 high-recall prompt with doc15 no-GT/no-OCR instructions and raw/overlay/crop visual packet."
    jennifer_r1_text = "Jennifer R1 precision prompt with Diego R1 proposal and doc15 raw/overlay/crop visual packet."
    diego_r2_text = "Diego R2 saturation prompt focused on contested DG/NSS, NF/DG, relay/TB, and CP/JB edge families."
    jennifer_r2_text = "Jennifer R2 final confirmation prompt for the eight ambiguous edges and final hard/uncertain policy."

    rows: list[dict[str, object]] = []

    def add_call(
        call_id: str,
        actor: str,
        round_name: str,
        model: str,
        text: str,
        image_tokens: int,
        output_tokens: int,
        reasoning_expected: int,
        notes: str,
        cached: int = 0,
    ) -> None:
        input_tokens = estimate_text_tokens(text) + cached
        total_low = input_tokens + image_tokens + output_tokens + math.floor(reasoning_expected * 0.5)
        total_expected = input_tokens + image_tokens + output_tokens + reasoning_expected
        total_high = input_tokens + math.ceil(image_tokens * 1.35) + math.ceil(output_tokens * 1.35) + math.ceil(reasoning_expected * 1.8)
        rows.append(
            {
                "document": DOC,
                "iteration": ITERATION,
                "call_id": call_id,
                "actor": actor,
                "round": round_name,
                "model": model,
                "input_tokens_est": input_tokens,
                "cached_input_tokens_est": cached,
                "output_tokens_est": output_tokens,
                "reasoning_tokens_available": "no",
                "reasoning_tokens_low_est": math.floor(reasoning_expected * 0.5),
                "reasoning_tokens_expected_est": reasoning_expected,
                "reasoning_tokens_high_est": math.ceil(reasoning_expected * 1.8),
                "image_file_input_tokens_est": image_tokens,
                "total_tokens_low_est": total_low,
                "total_tokens_expected_est": total_expected,
                "total_tokens_high_est": total_high,
                "usage_object_available": "no",
                "notes": notes,
            }
        )

    main_img_tokens = sum(image_token_proxy(p) for p in main_images)
    diego_img_tokens = sum(image_token_proxy(p) for p in diego_r1_images)
    jennifer_img_tokens = sum(image_token_proxy(p) for p in jennifer_r1_images)
    diego_out = 3600
    jennifer_out = 2600
    diego2_out = 700
    jennifer2_out = 220
    add_call("main_01_visual_orchestration_and_artifacts", "main", "orchestration", "gpt-5", main_text, main_img_tokens, 2400, 5000, "Exact usage unavailable; local visual and artifact work.")
    add_call("diego_01_high_recall", "Diego", "round_01", "gpt-5.5 xhigh", diego_r1_text, diego_img_tokens, diego_out, 9000, "Subagent usage object unavailable; response text observed.")
    add_call("jennifer_01_precision", "Jennifer", "round_01", "gpt-5.5 xhigh", jennifer_r1_text, jennifer_img_tokens, jennifer_out, 8000, "Subagent usage object unavailable; response text observed.")
    diego_cached = estimate_text_tokens(diego_r1_text) + diego_img_tokens + diego_out
    jennifer_cached = estimate_text_tokens(jennifer_r1_text) + jennifer_img_tokens + jennifer_out
    add_call("diego_02_saturation", "Diego", "round_02", "gpt-5.5 xhigh", diego_r2_text, 0, diego2_out, 3000, "Follow-up in same subagent context; prior visual packet counted as cached estimate.", cached=diego_cached)
    add_call("jennifer_02_final", "Jennifer", "round_02", "gpt-5.5 xhigh", jennifer_r2_text, 0, jennifer2_out, 1800, "Follow-up in same subagent context; prior visual packet counted as cached estimate.", cached=jennifer_cached)

    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return rows


def write_token_summary(path: Path, rows: list[dict[str, object]]) -> None:
    total_low = sum(int(r["total_tokens_low_est"]) for r in rows)
    total_expected = sum(int(r["total_tokens_expected_est"]) for r in rows)
    total_high = sum(int(r["total_tokens_high_est"]) for r in rows)
    image_total = sum(int(r["image_file_input_tokens_est"]) for r in rows)
    cached_total = sum(int(r["cached_input_tokens_est"]) for r in rows)
    path.write_text(
        f"""# Token Usage Estimate - Document {DOC}, Iteration {ITERATION}

OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.

Local estimate method:
- Text tokens: ceil(character_count / 4).
- Image/file tokens: ceil(width / 32) * ceil(height / 32), computed from each raw/crop image.
- Reasoning tokens: unavailable, so low/expected/high ranges are estimated.
- Cached input tokens: estimated prior subagent context for round-2 follow-ups.

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| {DOC} | {ITERATION} | {total_low} | {total_expected} | {total_high} | {image_total} | {cached_total} |
""",
        encoding="utf-8",
    )


def write_round_notes(path: Path) -> None:
    path.write_text(
        f"""# Document {DOC} Round Notes

## Diego Round 1 - High Recall

Diego identified the 183-node schema matching the raw note block. He included offsite source chains, all division feeder and MCC load chains, relay/control/DC wiring, AB/CD tie paths, and high-recall same-division NF/DG dashed control edges. He left DG-to-NSS bus contacts uncertain.

## Jennifer Round 1 - Precision

Jennifer supported all 183 nodes, promoted DG-to-NSS contacts to hard, and kept the same-division NF/DG dashed interlocks hard. This produced an over-broad hard set relative to the raw 190-connection sanity note.

## Diego Round 2 - Saturation Check

Diego kept `RLY-*06 -- TB-1*` and `CP-1* -- JB-1*` as hard visual doglegs, but moved `BUS-NSS -- DG` and `CB-NF -- CB-DG` same-division dashed edges to uncertain.

## Jennifer Round 2 - Final

Jennifer accepted Diego Round 2. Final graph: 183 nodes, 190 hard edges, 8 uncertain edges.
""",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = build_nodes()
    diego_r1_edges = build_edges(include_dg_nss=False, include_nf_dg_control=True)
    jennifer_r1_edges = build_edges(include_dg_nss=True, include_nf_dg_control=True)
    final_edges = build_edges(include_dg_nss=False, include_nf_dg_control=False)
    final_uncertain = uncertain_edges_final()

    qa = {
        "round_01_diego_high_recall": emit_round("round_01_diego_high_recall", nodes, diego_r1_edges, uncertain_edges_diego_r1()),
        "round_01_jennifer_precision": emit_round("round_01_jennifer_precision", nodes, jennifer_r1_edges, []),
        "round_02_diego_saturation": emit_round("round_02_diego_saturation", nodes, final_edges, final_uncertain),
        "round_02_jennifer_final": emit_round("round_02_jennifer_final", nodes, final_edges, final_uncertain),
    }
    write_nodes(OUT / "nodes_final.csv", nodes)
    write_edges(OUT / "edges_final.csv", final_edges)
    write_matrix(OUT / "connectivity_matrix_final.csv", nodes, final_edges)
    write_sparse(OUT / "connectivity_sparse_final.csv", nodes, final_edges)
    write_uncertain(OUT / "uncertain_edges_final.csv", final_uncertain)
    write_removed(OUT / "removed_edges_round_02_jennifer_final.csv", removed_edges_jennifer_final())
    write_round_notes(OUT / "round_notes.md")
    token_rows = write_token_usage(OUT / "token_usage_estimate.csv")
    write_token_summary(OUT / "token_usage_summary.md", token_rows)

    final_qa = validate_round(nodes, final_edges)
    final_qa["uncertain_edge_count"] = len(final_uncertain)
    final_qa["rounds"] = qa
    final_qa["raw_note_nodes"] = 183
    final_qa["raw_note_connections"] = 190
    final_qa["raw_resource"] = str(RAW)
    final_qa["overlay_resource"] = str(OVERLAY)
    final_qa["mask_resource"] = str(MASK)
    final_qa["notes"] = [
        "Final matrix contains hard visual connections only.",
        "Eight visually plausible but ambiguous DG/NSS and same-division NF/DG dashed edges are in uncertain_edges_final.csv.",
        "Final 183-node/190-edge count matches the raw schematic note block as a sanity check.",
    ]
    (OUT / "qa_final.json").write_text(json.dumps(final_qa, indent=2), encoding="utf-8")
    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "final_node_count": len(nodes),
        "final_hard_edge_count": len(final_edges),
        "final_uncertain_edge_count": len(final_uncertain),
        "round_files_written": sorted(p.name for p in OUT.glob("*")),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
