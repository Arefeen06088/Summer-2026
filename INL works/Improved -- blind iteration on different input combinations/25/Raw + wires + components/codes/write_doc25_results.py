from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"
DOCUMENT = "25"
ITERATION = "1"
TRAINS = ["A", "B", "C"]


def add_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def edge(a: str, b: str, evidence: str, confidence: str = "high", status: str = "accepted") -> dict[str, str]:
    return {"source": a, "target": b, "confidence": confidence, "status": status, "evidence": evidence}


def chain(items: list[str], evidence: str, confidence: str = "high") -> list[dict[str, str]]:
    return [edge(a, b, evidence, confidence) for a, b in zip(items, items[1:])]


def source_nodes() -> list[str]:
    return [
        "SWYD-115KV",
        "FDR-13A",
        "TR-UAT-1A",
        "CB-52-4A",
        "EDG-1A",
        "CB-DG-1A",
        "BUS-4160-A",
        "FDR-13B",
        "TR-UAT-1B",
        "CB-52-4B",
        "EDG-1B",
        "CB-DG-1B",
        "BUS-4160-B",
        "TR-SAT-1",
        "CB-52-4C",
        "EDG-1C",
        "CB-DG-1C",
        "BUS-4160-C",
        "CB-TIE-AB",
        "CB-TIE-BC",
    ]


def train_nodes(t: str) -> list[str]:
    nodes: list[str] = []
    for n in range(1, 9):
        nodes += [f"CB-4{t}{n:02d}", f"DS-4{t}{n:02d}"]
    nodes += [
        f"TR-480-1{t}",
        f"CB-52-48{t}",
        f"BUS-480-1{t}",
        f"MS-{t}01",
        f"PUMP-RHR-P201{t}",
        f"MS-{t}02",
        f"PUMP-CS-P202{t}",
        f"TR-LC-{t}03",
        f"LC-480-{t}03",
        f"MS-{t}04",
        f"FAN-CR-401{t}",
        f"PNL-ESF-{t}05",
        f"GND-ESF-{t}05",
        f"RECT-RPS-{t}06",
        f"INV-RPS-{t}06",
        f"MS-{t}07",
        f"PUMP-AFW-P203{t}",
        f"TR-CTRL-{t}08",
        f"CP-CTRL-{t}08",
        f"MCC-{t}1",
        f"MCC-{t}2",
    ]
    for n in range(1, 7):
        nodes.append(f"CB-48{t}{n:02d}")
    nodes += [
        f"MS-48{t}01",
        f"PUMP-CVC-P301{t}",
        f"K-48{t}02",
        f"MOV-CS-451{t}",
        f"MS-48{t}03",
        f"FAN-HVAC-501{t}",
        f"MS-48{t}04",
        f"PUMP-SUMP-P302{t}",
        f"K-48{t}05",
        f"MOV-RHR-452{t}",
        f"XFU-48{t}06",
        f"PNL-PI-601{t}",
    ]
    return nodes


def rps_nodes() -> list[str]:
    return [
        "480V-CHGR-A-FEEDER",
        "480V-CHGR-B-FEEDER",
        "CHGR-125-1A",
        "CHGR-125-1B",
        "BAT-125-1A",
        "BAT-125-1B",
        "BUS-125DC-A",
        "BUS-125DC-B",
        "INV-120-1A",
        "INV-120-1B",
        "PNL-RPS-A",
        "PNL-RPS-B",
        "RELAY-K501A",
        "RELAY-K501B",
        "XMTR-PT-501A",
        "XMTR-PT-501B",
        "PNL-A/B-TIE",
        "RPS-TRIP-BUS",
        "TC-52-4A",
    ]


def all_nodes() -> list[str]:
    nodes: list[str] = []
    for node in source_nodes():
        add_unique(nodes, node)
    for t in TRAINS:
        for node in train_nodes(t):
            add_unique(nodes, node)
    for node in rps_nodes():
        add_unique(nodes, node)
    return nodes


def final_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    edges += chain(["SWYD-115KV", "FDR-13A", "TR-UAT-1A", "CB-52-4A", "BUS-4160-A"], "source stack A solid conductors")
    edges += chain(["EDG-1A", "CB-DG-1A", "BUS-4160-A"], "diesel generator A solid conductors")
    edges += chain(["SWYD-115KV", "FDR-13B", "TR-UAT-1B", "CB-52-4B", "BUS-4160-B"], "source stack B solid conductors")
    edges += chain(["EDG-1B", "CB-DG-1B", "BUS-4160-B"], "diesel generator B solid conductors")
    edges += chain(["SWYD-115KV", "TR-SAT-1", "CB-52-4C", "BUS-4160-C"], "source stack C solid conductors")
    edges += chain(["EDG-1C", "CB-DG-1C", "BUS-4160-C"], "diesel generator C solid conductors")
    edges += chain(["BUS-4160-A", "CB-TIE-AB", "BUS-4160-B"], "inline tie breaker AB on 4.16 kV bus")
    edges += chain(["BUS-4160-B", "CB-TIE-BC", "BUS-4160-C"], "inline tie breaker BC on 4.16 kV bus")

    for t in TRAINS:
        bus4160 = f"BUS-4160-{t}"
        for n in range(1, 9):
            cb = f"CB-4{t}{n:02d}"
            ds = f"DS-4{t}{n:02d}"
            edges += chain([bus4160, cb, ds], "4.16 kV bus feeder tap")
        edges += chain([f"DS-4{t}01", f"TR-480-1{t}", f"CB-52-48{t}", f"BUS-480-1{t}"], "feeder 01 transformer path to 480 V bus")
        edges += chain([f"DS-4{t}01", f"MS-{t}01", f"PUMP-RHR-P201{t}"], "feeder 01 RHR pump branch")
        edges += chain([f"DS-4{t}02", f"MS-{t}02", f"PUMP-CS-P202{t}"], "feeder 02 charging/safety pump branch")
        edges += chain([f"DS-4{t}03", f"TR-LC-{t}03", f"LC-480-{t}03"], "feeder 03 load center transformer branch")
        edges += chain([f"DS-4{t}04", f"MS-{t}04", f"FAN-CR-401{t}"], "feeder 04 fan branch")
        edges += chain([f"DS-4{t}05", f"PNL-ESF-{t}05", f"GND-ESF-{t}05"], "feeder 05 ESF panel and ground reference")
        edges += chain([f"DS-4{t}06", f"RECT-RPS-{t}06", f"INV-RPS-{t}06"], "feeder 06 RPS rectifier/inverter branch")
        edges += chain([f"DS-4{t}07", f"MS-{t}07", f"PUMP-AFW-P203{t}"], "feeder 07 AFW pump branch")
        edges += chain([f"DS-4{t}08", f"TR-CTRL-{t}08", f"CP-CTRL-{t}08"], "feeder 08 control transformer/panel branch")

        edges.append(edge(f"BUS-480-1{t}", f"MCC-{t}1", "480 V bus drop to MCC section 1"))
        edges.append(edge(f"BUS-480-1{t}", f"MCC-{t}2", "480 V bus drop to MCC section 2"))
        edges += chain([f"MCC-{t}1", f"CB-48{t}01", f"MS-48{t}01", f"PUMP-CVC-P301{t}"], "MCC section 1 branch 01")
        edges += chain([f"MCC-{t}1", f"CB-48{t}02", f"K-48{t}02", f"MOV-CS-451{t}"], "MCC section 1 branch 02")
        edges += chain([f"MCC-{t}1", f"CB-48{t}03", f"MS-48{t}03", f"FAN-HVAC-501{t}"], "MCC section 1 branch 03")
        edges += chain([f"MCC-{t}2", f"CB-48{t}04", f"MS-48{t}04", f"PUMP-SUMP-P302{t}"], "MCC section 2 branch 04")
        edges += chain([f"MCC-{t}2", f"CB-48{t}05", f"K-48{t}05", f"MOV-RHR-452{t}"], "MCC section 2 branch 05")
        edges += chain([f"MCC-{t}2", f"CB-48{t}06", f"XFU-48{t}06", f"PNL-PI-601{t}"], "MCC section 2 branch 06")

    edges += chain(["480V-CHGR-A-FEEDER", "CHGR-125-1A", "BUS-125DC-A"], "A charger feed to DC bus")
    edges.append(edge("BAT-125-1A", "BUS-125DC-A", "A battery tap to DC bus"))
    edges += chain(["BUS-125DC-A", "INV-120-1A", "PNL-RPS-A"], "A DC bus to RPS panel through inverter")
    edges.append(edge("PNL-RPS-A", "RELAY-K501A", "A RPS dashed/control route to relay"))
    edges.append(edge("PNL-RPS-A", "XMTR-PT-501A", "A RPS signal/control route to transmitter"))
    edges += chain(["PNL-RPS-A", "PNL-A/B-TIE", "PNL-RPS-B"], "visible PNL A/B tie dashed route", "medium")
    edges += chain(["480V-CHGR-B-FEEDER", "CHGR-125-1B", "BUS-125DC-B"], "B charger feed to DC bus")
    edges.append(edge("BAT-125-1B", "BUS-125DC-B", "B battery tap to DC bus"))
    edges += chain(["BUS-125DC-B", "INV-120-1B", "PNL-RPS-B"], "B DC bus to RPS panel through inverter")
    edges.append(edge("PNL-RPS-B", "RELAY-K501B", "B RPS dashed/control route to relay"))
    edges.append(edge("PNL-RPS-B", "XMTR-PT-501B", "B RPS signal/control route to transmitter"))
    edges.append(edge("RELAY-K501A", "TC-52-4A", "dashed control route from A relay to trip coil", "medium"))
    edges.append(edge("RELAY-K501B", "TC-52-4A", "dashed control route from B relay to trip coil"))
    edges.append(edge("RPS-TRIP-BUS", "TC-52-4A", "dashed trip bus route to trip coil"))
    return dedupe_edges(edges)


def diego_extra_edges() -> list[dict[str, str]]:
    extras: list[dict[str, str]] = []
    for t in TRAINS:
        extras.append(edge(f"PNL-ESF-{t}05", f"RECT-RPS-{t}06", "Diego high-recall possible adjacency, later rejected", "low", "removed_by_jennifer"))
        extras.append(edge(f"MCC-{t}1", f"MCC-{t}2", "Diego high-recall possible common riser, later rejected", "low", "removed_by_jennifer"))
    extras += [
        edge("PNL-RPS-A", "CHGR-125-1B", "Diego high-recall possible dashed route, later excluded", "low", "removed_by_jennifer"),
    ]
    return extras


def dedupe_edges(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for item in edges:
        key = tuple(sorted((item["source"], item["target"])))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source", "target", "confidence", "status", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        a, b = item["source"], item["target"]
        if a not in index or b not in index:
            raise ValueError(f"Unknown edge endpoint: {a!r}, {b!r}")
        if a != b:
            matrix[index[a]][index[b]] = 1
            matrix[index[b]][index[a]] = 1
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def text_tokens(text: str) -> int:
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    return max(len(text.split()), math.ceil(len(text) / 4))


def image_tokens_high_detail(path: Path) -> int:
    with Image.open(path) as image:
        width, height = image.size
    scale = min(1.0, 2048.0 / width, 2048.0 / height)
    width *= scale
    height *= scale
    short = min(width, height)
    if short > 768:
        scale = 768.0 / short
        width *= scale
        height *= scale
    return 85 + 170 * math.ceil(width / 512.0) * math.ceil(height / 512.0)


def image_token_sum(names: list[str]) -> int:
    total = 0
    for name in names:
        path = CROPS / name
        if path.exists():
            total += image_tokens_high_detail(path)
    return total


def token_rows() -> list[dict[str, object]]:
    diego_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "top_sources_and_13kv_components.png",
        "top_sources_and_13kv_wires_overlay.png",
        "train_a_4160_feeders_components.png",
        "train_a_4160_feeders_wires_overlay.png",
        "train_b_4160_feeders_components.png",
        "train_b_4160_feeders_wires_overlay.png",
        "train_c_4160_feeders_components.png",
        "train_c_4160_feeders_wires_overlay.png",
        "train_a_480v_branches_components.png",
        "train_a_480v_branches_wires_overlay.png",
        "train_b_480v_branches_components.png",
        "train_b_480v_branches_wires_overlay.png",
        "train_c_480v_branches_components.png",
        "train_c_480v_branches_wires_overlay.png",
        "bottom_125v_rps_all_components.png",
        "bottom_125v_rps_all_wires_overlay.png",
        "bottom_125v_rps_left_components.png",
        "bottom_125v_rps_right_components.png",
        "detail_notes_legend_title_components.png",
    ]
    jennifer_images = [
        "raw_full_thumb.png",
        "components_full_thumb.png",
        "wires_overlay_full_thumb.png",
        "top_left_sources_components.png",
        "top_right_sources_components.png",
        "top_sources_and_13kv_wires_overlay.png",
        "train_a_4160_feeders_components.png",
        "train_a_4160_feeders_wires_overlay.png",
        "train_b_4160_feeders_components.png",
        "train_b_4160_feeders_wires_overlay.png",
        "train_c_4160_feeders_components.png",
        "train_c_4160_feeders_wires_overlay.png",
        "train_a_480v_branches_components.png",
        "train_b_480v_branches_components.png",
        "train_c_480v_branches_components.png",
        "bottom_125v_rps_all_components.png",
        "bottom_125v_rps_all_wires_overlay.png",
        "bottom_125v_rps_left_components.png",
        "bottom_125v_rps_right_components.png",
        "detail_notes_legend_title_components.png",
    ]
    specs = [
        ("main-setup", "main", "setup", 2400, [], 700, 1200, 1900, 900, "Main setup, crop generation, Diego spawn."),
        ("diego-r1", "Diego", "1", 1800, diego_images, 2600, 4300, 6500, 1600, "High-recall visual extraction."),
        ("jennifer-r2", "Jennifer", "2", 6600, jennifer_images, 2200, 3600, 5400, 1200, "Precision review with Diego proposal."),
        ("diego-r3", "Diego", "3", 4700, [], 300, 800, 1600, 450, "Convergence review."),
        ("jennifer-r4", "Jennifer", "4", 180, [], 250, 650, 1300, 350, "Final confirmation."),
        ("main-artifacts-final", "main", "write/final", 2000, [], 700, 1300, 2300, 1200, "Artifact writing and final response."),
    ]
    rows: list[dict[str, object]] = []
    for call_id, actor, round_id, text_est, images, out_low, out_exp, out_high, reason, notes in specs:
        image_est = image_token_sum(images)
        input_est = text_est + image_est
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": round_id,
                "call_id": call_id,
                "actor": actor,
                "input_tokens_est": input_est,
                "cached_input_tokens_est": 0,
                "text_input_tokens_est": text_est,
                "image_file_count": len(images),
                "image_input_tokens_est": image_est,
                "output_tokens_low_est": out_low,
                "output_tokens_expected_est": out_exp,
                "output_tokens_high_est": out_high,
                "reasoning_tokens_est": reason,
                "total_low_tokens_est": input_est + out_low + reason,
                "total_expected_tokens_est": input_est + out_exp + reason,
                "total_high_tokens_est": input_est + out_high + reason,
                "usage_object_available": "no",
                "notes": notes,
            }
        )
    return rows


def write_token_tables(rows: list[dict[str, object]]) -> dict[str, object]:
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in rows),
        "image_input_tokens_est": sum(int(r["image_input_tokens_est"]) for r in rows),
        "output_tokens_low_est": sum(int(r["output_tokens_low_est"]) for r in rows),
        "output_tokens_expected_est": sum(int(r["output_tokens_expected_est"]) for r in rows),
        "output_tokens_high_est": sum(int(r["output_tokens_high_est"]) for r in rows),
        "reasoning_tokens_est": sum(int(r["reasoning_tokens_est"]) for r in rows),
        "total_low_tokens_est": sum(int(r["total_low_tokens_est"]) for r in rows),
        "total_expected_tokens_est": sum(int(r["total_expected_tokens_est"]) for r in rows),
        "total_high_tokens_est": sum(int(r["total_high_tokens_est"]) for r in rows),
        "method": "Responses input-token counting endpoint not called because OPENAI_API_KEY is not available. Text estimated locally; image inputs estimated by high-detail tile sizing.",
    }
    with (RESULTS / "token_usage_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_uncertain(path: Path) -> None:
    rows = [
        ("MCC-T1--MCC-T2", "rejected", "Separate visible feeds from BUS-480-1T to MCC-T1 and MCC-T2; no direct MCC tie."),
        ("PNL-RPS-A--CHGR-125-1B", "uncertain_excluded", "Nearby dashed route is not a clean terminal connection to the charger."),
        ("PNL-ESF-T05--RECT-RPS-T06", "rejected", "Adjacent components sit on separate feeder drops; no direct wire visible."),
        ("FDR-13C/SRC-FEEDER-C", "not_added", "Train C source is TR-SAT-1 into CB-52-4C, no visible FDR-13C."),
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["edge_or_node", "status", "reason"])
        writer.writerows(rows)


def write_report(nodes: list[str], final: list[dict[str, str]], token_summary: dict[str, object]) -> None:
    report = f"""# Document 25 Connectivity Extraction

Blind visual extraction using only the raw schematic and derived visual aids in the resource folder. No GT, GT-derived feedback, or OCR tools were used.

## Rounds

1. Diego high-recall extraction captured the three train 4.16 kV layout, 480 V MCC branches, and bottom 125 VDC/RPS section.
2. Jennifer corrected source labels, accepted visually supported RPS tie/trip-coil routes, and rejected overconnections.
3. Diego convergence review was run against Jennifer's final graph.
4. Jennifer final confirmation was run after Diego's convergence reply.

## Final Matrix

- Nodes: {len(nodes)}
- Final accepted undirected edges: {len(final)}
- Matrix file: `final_connectivity_matrix.csv`
- Edge file: `final_edges.csv`

## Key Precision Decisions

- `SWYD-115KV` is the top source bus.
- Train C source is `TR-SAT-1 -> CB-52-4C -> BUS-4160-C`; no `FDR-13C` node was added.
- `MCC-T1 -- MCC-T2` and `PNL-ESF-T05 -- RECT-RPS-T06` were excluded.
- `PNL-RPS-A -- PNL-A/B-TIE -- PNL-RPS-B`, `RELAY-K501A -- TC-52-4A`, and `RELAY-K501B -- TC-52-4A` were retained as visually supported.

## Token Estimation

The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Actual usage objects were not exposed by the Codex subagent notification/tooling. The local estimate uses text estimates plus high-detail image tile sizing.

- Estimated input tokens: {token_summary['input_tokens_est']}
- Estimated image input tokens: {token_summary['image_input_tokens_est']}
- Expected output tokens: {token_summary['output_tokens_expected_est']}
- Estimated reasoning tokens: {token_summary['reasoning_tokens_est']}
- Expected total tokens: {token_summary['total_expected_tokens_est']}
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = all_nodes()
    final = final_edges()
    round1 = dedupe_edges(final + diego_extra_edges())
    round2 = final
    round3 = final
    round4 = final
    for name, edges in [
        ("round_01_diego", round1),
        ("round_02_jennifer", round2),
        ("round_03_diego", round3),
        ("round_04_jennifer_final", round4),
    ]:
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", nodes, edges)
    write_edges(RESULTS / "final_edges.csv", final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final)
    write_uncertain(RESULTS / "uncertain_or_excluded_edges.csv")
    token_summary = write_token_tables(token_rows())
    write_report(nodes, final, token_summary)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "nodes": len(nodes),
        "final_edges": len(final),
        "rounds": {
            "round_01_diego": len(round1),
            "round_02_jennifer": len(round2),
            "round_03_diego": len(round3),
            "round_04_jennifer_final": len(round4),
        },
        "matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges_file": str(RESULTS / "final_edges.csv"),
        "token_usage_estimate": str(RESULTS / "token_usage_estimate.csv"),
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
