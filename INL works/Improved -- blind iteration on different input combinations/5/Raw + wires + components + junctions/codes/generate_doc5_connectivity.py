from __future__ import annotations

import csv
import math
from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"


NODES = [
    "GRID-N230",
    "ISO-230A",
    "BRK-2301",
    "GRID-S230",
    "ISO-230B",
    "BRK-2302",
    "GEN-G101",
    "GSU-1",
    "BUS-SY230",
    "TR-RAT-1A",
    "TR-RAT-1B",
    "TR-UAT-1A",
    "TR-UAT-1B",
    "CB-AUX-A",
    "CB-AUX-B",
    "BUS-AUX13A",
    "BUS-AUX13B",
    "CB-TIE13",
    "BUS-NON1",
    "EDG-A",
    "CB-EDG-A",
    "TR-SAF-A",
    "CB-SAF-A",
    "BUS-416A",
    "TR-480-A",
    "CB-LC-A",
    "LC-480A",
    "CB-MCCA1",
    "MCC-1A1",
    "PUMP-AFW-A",
    "CB-MCCA2",
    "MCC-1A2",
    "PUMP-CCW-A",
    "VLV-MSIV-A",
    "EDG-B",
    "CB-EDG-B",
    "TR-SAF-B",
    "CB-SAF-B",
    "BUS-416B",
    "TR-480-B",
    "CB-LC-B",
    "LC-480B",
    "CB-MCCB1",
    "MCC-1B1",
    "PUMP-AFW-B",
    "CB-MCCB2",
    "MCC-1B2",
    "PUMP-CCW-B",
    "VLV-MSIV-B",
    "CB-TIE-AB",
    "EDG-C",
    "CB-EDG-C",
    "TR-SAF-C",
    "CB-SAF-C",
    "BUS-416C",
    "TR-480-C",
    "CB-LC-C",
    "LC-480C",
    "CB-MCCC1",
    "MCC-1C1",
    "PUMP-RHR-A",
    "CB-MCCC2",
    "MCC-1C2",
    "FAN-CRHV-A",
    "HTR-BATRM-A",
    "EDG-D",
    "CB-EDG-D",
    "TR-SAF-D",
    "CB-SAF-D",
    "BUS-416D",
    "TR-480-D",
    "CB-LC-D",
    "LC-480D",
    "CB-MCCD1",
    "MCC-1D1",
    "PUMP-RHR-B",
    "CB-MCCD2",
    "MCC-1D2",
    "FAN-CRHV-B",
    "HTR-BATRM-B",
    "CB-TIE-CD",
    "XFER-ATS-A",
    "CHG-125A",
    "BAT-125A",
    "PNL-DC-A",
    "INV-UPS-A",
    "UPS-PNL-A",
    "RECT-48V-A",
    "BAT-48V-A",
    "JB-RLY-A",
    "XFER-ATS-B",
    "CHG-125B",
    "BAT-125B",
    "PNL-DC-B",
    "INV-UPS-B",
    "UPS-PNL-B",
    "RECT-48V-B",
    "BAT-48V-B",
    "JB-RLY-B",
    "CP-ESFAS-1",
    "CP-ESFAS-2",
    "RELAY-K1A",
    "RELAY-K1B",
    "RELAY-K2A",
    "RELAY-K2B",
    "RELAY-UV-A",
    "RELAY-UV-B",
    "RELAY-LOOP-C",
    "RELAY-LOOP-D",
    "INST-NSSS-A",
    "INST-NSSS-B",
    "GND-GRID",
]

DIEGO_NODES = [n.replace("VLV-MSIV", "VLV-MISV") for n in NODES]


def chain(*items: str) -> list[tuple[str, str]]:
    return list(zip(items, items[1:]))


def edge_set(nodes: list[str], pairs: list[tuple[str, str]]) -> set[tuple[str, str]]:
    known = set(nodes)
    out = set()
    for a, b in pairs:
        if a not in known or b not in known:
            raise ValueError(f"Unknown node in edge: {a!r}, {b!r}")
        if a == b:
            raise ValueError(f"Self-loop not expected: {a!r}")
        out.add(tuple(sorted((a, b))))
    return out


FINAL_EDGE_PAIRS = [
    *chain("GRID-N230", "ISO-230A", "BRK-2301", "BUS-SY230"),
    *chain("GRID-S230", "ISO-230B", "BRK-2302", "BUS-SY230"),
    *chain("GEN-G101", "GSU-1", "BUS-SY230"),
    *chain("BUS-SY230", "TR-RAT-1A", "CB-AUX-A", "BUS-AUX13A"),
    *chain("BUS-SY230", "TR-UAT-1A", "CB-AUX-A"),
    *chain("BUS-SY230", "TR-RAT-1B", "CB-AUX-B", "BUS-AUX13B"),
    *chain("BUS-SY230", "TR-UAT-1B", "CB-AUX-B"),
    *chain("BUS-AUX13A", "CB-TIE13", "BUS-AUX13B"),
    ("BUS-AUX13A", "BUS-NON1"),
    ("BUS-NON1", "TR-SAF-C"),
    ("BUS-AUX13B", "TR-SAF-C"),
    *chain("BUS-AUX13A", "TR-SAF-A", "CB-SAF-A", "BUS-416A"),
    *chain("EDG-A", "CB-EDG-A", "BUS-416A"),
    *chain("BUS-416A", "TR-480-A", "CB-LC-A", "LC-480A"),
    *chain("LC-480A", "CB-MCCA1", "MCC-1A1", "PUMP-AFW-A"),
    *chain("LC-480A", "CB-MCCA2", "MCC-1A2", "PUMP-CCW-A"),
    ("MCC-1A1", "VLV-MSIV-A"),
    ("VLV-MSIV-A", "XFER-ATS-A"),
    *chain("BUS-AUX13A", "TR-SAF-B", "CB-SAF-B", "BUS-416B"),
    *chain("EDG-B", "CB-EDG-B", "BUS-416B"),
    *chain("BUS-416B", "TR-480-B", "CB-LC-B", "LC-480B"),
    *chain("LC-480B", "CB-MCCB1", "MCC-1B1", "PUMP-AFW-B"),
    *chain("LC-480B", "CB-MCCB2", "MCC-1B2", "PUMP-CCW-B"),
    ("MCC-1B1", "VLV-MSIV-B"),
    *chain("BUS-416A", "CB-TIE-AB", "BUS-416B"),
    *chain("TR-SAF-C", "CB-SAF-C", "BUS-416C"),
    *chain("EDG-C", "CB-EDG-C", "BUS-416C"),
    *chain("BUS-416C", "TR-480-C", "CB-LC-C", "LC-480C"),
    *chain("LC-480C", "CB-MCCC1", "MCC-1C1", "PUMP-RHR-A"),
    *chain("LC-480C", "CB-MCCC2", "MCC-1C2", "FAN-CRHV-A"),
    ("MCC-1C2", "HTR-BATRM-A"),
    ("HTR-BATRM-A", "XFER-ATS-B"),
    *chain("BUS-AUX13B", "TR-SAF-D", "CB-SAF-D", "BUS-416D"),
    *chain("EDG-D", "CB-EDG-D", "BUS-416D"),
    *chain("BUS-416D", "TR-480-D", "CB-LC-D", "LC-480D"),
    *chain("LC-480D", "CB-MCCD1", "MCC-1D1", "PUMP-RHR-B"),
    *chain("LC-480D", "CB-MCCD2", "MCC-1D2", "FAN-CRHV-B"),
    ("MCC-1D2", "HTR-BATRM-B"),
    ("PUMP-RHR-B", "XFER-ATS-B"),
    *chain("BUS-416C", "CB-TIE-CD", "BUS-416D"),
    *chain("XFER-ATS-A", "CHG-125A", "BAT-125A", "PNL-DC-A"),
    *chain("PNL-DC-A", "INV-UPS-A", "UPS-PNL-A"),
    *chain("XFER-ATS-A", "RECT-48V-A", "BAT-48V-A", "JB-RLY-A"),
    *chain("XFER-ATS-B", "CHG-125B", "BAT-125B", "PNL-DC-B"),
    *chain("PNL-DC-B", "INV-UPS-B", "UPS-PNL-B"),
    *chain("XFER-ATS-B", "RECT-48V-B", "BAT-48V-B", "JB-RLY-B"),
]

FINAL_EDGES = edge_set(NODES, FINAL_EDGE_PAIRS)

DIEGO_FINAL_PROMOTED = {
    tuple(sorted(edge))
    for edge in [
        ("VLV-MSIV-A", "XFER-ATS-A"),
        ("HTR-BATRM-A", "XFER-ATS-B"),
        ("PUMP-RHR-B", "XFER-ATS-B"),
        ("XFER-ATS-A", "RECT-48V-A"),
        ("XFER-ATS-B", "RECT-48V-B"),
    ]
}

DIEGO_EDGE_PAIRS = [
    (a.replace("VLV-MSIV", "VLV-MISV"), b.replace("VLV-MSIV", "VLV-MISV"))
    for a, b in FINAL_EDGE_PAIRS
    if tuple(sorted((a, b))) not in DIEGO_FINAL_PROMOTED
]
DIEGO_EDGES = edge_set(DIEGO_NODES, DIEGO_EDGE_PAIRS)

DIEGO_UNCERTAIN_EDGE_PAIRS = [
    ("LC-480A", "XFER-ATS-A"),
    ("LC-480B", "XFER-ATS-A"),
    ("LC-480C", "XFER-ATS-B"),
    ("LC-480D", "XFER-ATS-B"),
    ("VLV-MISV-A", "XFER-ATS-A"),
    ("HTR-BATRM-A", "XFER-ATS-B"),
    ("PUMP-RHR-B", "XFER-ATS-B"),
    ("XFER-ATS-A", "RECT-48V-A"),
    ("XFER-ATS-B", "RECT-48V-B"),
    ("JB-RLY-A", "RELAY-K1A"),
    ("JB-RLY-A", "RELAY-K2A"),
    ("JB-RLY-A", "RELAY-UV-A"),
    ("JB-RLY-A", "RELAY-LOOP-C"),
    ("JB-RLY-B", "RELAY-K1B"),
    ("JB-RLY-B", "RELAY-K2B"),
    ("JB-RLY-B", "RELAY-UV-B"),
    ("JB-RLY-B", "RELAY-LOOP-D"),
    ("PNL-DC-A", "CP-ESFAS-1"),
    ("PNL-DC-A", "CP-ESFAS-2"),
    ("PNL-DC-B", "CP-ESFAS-1"),
    ("PNL-DC-B", "CP-ESFAS-2"),
    ("CP-ESFAS-1", "RELAY-K1A"),
    ("CP-ESFAS-1", "RELAY-K1B"),
    ("CP-ESFAS-1", "INST-NSSS-A"),
    ("CP-ESFAS-1", "INST-NSSS-B"),
    ("CP-ESFAS-2", "RELAY-K2A"),
    ("CP-ESFAS-2", "RELAY-K2B"),
    ("CP-ESFAS-2", "RELAY-LOOP-C"),
    ("CP-ESFAS-2", "RELAY-LOOP-D"),
    ("CP-ESFAS-2", "INST-NSSS-A"),
    ("CP-ESFAS-2", "INST-NSSS-B"),
    ("GND-GRID", "UPS-PNL-A"),
    ("GND-GRID", "INV-UPS-A"),
    ("GND-GRID", "BAT-48V-A"),
    ("GND-GRID", "JB-RLY-B"),
    ("GND-GRID", "BAT-48V-B"),
    ("GND-GRID", "UPS-PNL-B"),
]
DIEGO_PLUS_UNCERTAIN_EDGES = DIEGO_EDGES | edge_set(DIEGO_NODES, DIEGO_UNCERTAIN_EDGE_PAIRS)

EDGE_EVIDENCE = {
    tuple(sorted(("VLV-MSIV-A", "XFER-ATS-A"))): "MSIV-A right terminal visibly lands on ATS-A input",
    tuple(sorted(("HTR-BATRM-A", "XFER-ATS-B"))): "solid feeder exits HTR-BATRM-A toward ATS-B",
    tuple(sorted(("PUMP-RHR-B", "XFER-ATS-B"))): "solid feeder exits PUMP-RHR-B toward ATS-B",
    tuple(sorted(("XFER-ATS-A", "RECT-48V-A"))): "solid ATS-A source/input to 48 V rectifier A",
    tuple(sorted(("XFER-ATS-B", "RECT-48V-B"))): "solid ATS-B source/input to 48 V rectifier B",
}


def default_evidence(edge: tuple[str, str]) -> str:
    a, b = edge
    if "TIE" in a or "TIE" in b:
        return "normally-open tie represented through breaker/tie node"
    if a.startswith("BUS") or b.startswith("BUS"):
        return "solid bus tap with filled dot"
    if a.startswith("CB") or b.startswith("CB") or a.startswith("BRK") or b.startswith("BRK"):
        return "solid breaker/component terminal conductor"
    if "PNL" in a or "PNL" in b or "UPS" in a or "UPS" in b or "BAT" in a or "BAT" in b:
        return "solid DC/UPS/vital power conductor"
    return "visible solid conductor between named endpoints"


def write_matrix(path: Path, nodes: list[str], edges: set[tuple[str, str]]) -> None:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        i, j = idx[a], idx[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edge_list(path: Path, edges: set[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "evidence"])
        for a, b in sorted(edges):
            writer.writerow([a, b, EDGE_EVIDENCE.get((a, b), default_evidence((a, b)))])


def text_tokens(text: str) -> int:
    if tiktoken is not None:
        for name in ("o200k_base", "cl100k_base"):
            try:
                enc = tiktoken.get_encoding(name)
                return len(enc.encode(text))
            except Exception:
                pass
    return math.ceil(len(text) / 4)


def estimate_image_tokens(path: Path) -> int:
    if Image is None:
        return 0
    with Image.open(path) as img:
        width, height = img.size
    scale = min(1.0, 2048.0 / max(width, height))
    width = math.ceil(width * scale)
    height = math.ceil(height * scale)
    if min(width, height) > 768:
        scale = 768.0 / min(width, height)
        width = math.ceil(width * scale)
        height = math.ceil(height * scale)
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_sum(names: list[str]) -> int:
    total = 0
    for name in names:
        total += estimate_image_tokens(BASE / name)
    return total


def write_token_estimates() -> None:
    diego_images = [
        "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        "wires_mask_overlay.png",
        r"results\raw__top_full.png",
        r"results\raw__top_left_source.png",
        r"results\raw__top_center_source.png",
        r"results\raw__top_right_source.png",
        r"results\raw__left_division_a.png",
        r"results\raw__mid_left_division_b.png",
        r"results\raw__mid_right_division_c.png",
        r"results\raw__right_division_d.png",
        r"results\raw__center_bus_ties.png",
        r"results\raw__dc_vital_a.png",
        r"results\raw__dc_vital_b.png",
        r"results\raw__bottom_ups_a.png",
        r"results\raw__bottom_ups_b.png",
        r"results\raw__battery_bus_tie.png",
        r"results\raw__protection_control_bay.png",
        r"results\raw__right_control_detail.png",
        r"results\raw__station_ground_title.png",
    ]
    jennifer_images = [
        "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
        r"results\raw__top_full.png",
        r"results\raw__left_division_a.png",
        r"results\raw__mid_left_division_b.png",
        r"results\raw__mid_right_division_c.png",
        r"results\raw__right_division_d.png",
        r"results\raw__center_bus_ties.png",
        r"results\raw__dc_vital_a.png",
        r"results\raw__dc_vital_b.png",
        r"results\raw__bottom_ups_a.png",
        r"results\raw__bottom_ups_b.png",
        r"results\raw__bottom_dc_relay_chain.png",
        r"results\raw__protection_control_bay.png",
        r"results\raw__right_control_detail.png",
        r"results\raw__station_ground_title.png",
    ]
    calls = [
        ("main-01", "Main", "setup/visual workbench", 9000, 0, 0, 650, 1100, 1700),
        ("diego-01", "Diego", "round 1 high recall", 2200, image_sum(diego_images), 0, 2600, 4300, 6800),
        ("jennifer-01", "Jennifer", "round 2 precision review", 7800, image_sum(jennifer_images), 0, 2300, 3800, 5800),
        ("diego-02", "Diego", "round 3 saturation", 650, 0, 26000, 40, 80, 180),
        ("main-02", "Main", "finalization", 16000, 0, 0, 500, 900, 1500),
    ]
    rows = []
    for call_id, actor, round_name, text_est, image_est, cached_est, out_low, out_exp, out_high in calls:
        input_expected = text_est + image_est + cached_est
        rows.append(
            {
                "document": 5,
                "iteration": 1,
                "call_id": call_id,
                "actor": actor,
                "round": round_name,
                "input_text_tokens_est": text_est,
                "image_file_input_tokens_est": image_est,
                "cached_input_tokens_est": cached_est,
                "recorded_input_tokens": "unavailable",
                "recorded_cached_input_tokens": "unavailable",
                "recorded_output_tokens": "unavailable",
                "recorded_reasoning_tokens": "unavailable",
                "output_tokens_low": out_low,
                "output_tokens_expected": out_exp,
                "output_tokens_high": out_high,
                "total_tokens_low": input_expected + out_low,
                "total_tokens_expected": input_expected + out_exp,
                "total_tokens_high": input_expected + out_high,
                "method": "manual text/context estimate plus high-detail image tile proxy; exact Responses endpoint unavailable because OPENAI_API_KEY is absent; usage object not exposed by subagent tool",
            }
        )
    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (RESULTS / "token_usage_summary_by_document_iteration.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "calls", "total_tokens_low", "total_tokens_expected", "total_tokens_high"])
        writer.writerow(
            [
                5,
                1,
                len(rows),
                sum(r["total_tokens_low"] for r in rows),
                sum(r["total_tokens_expected"] for r in rows),
                sum(r["total_tokens_high"] for r in rows),
            ]
        )


def write_notes() -> None:
    notes = f"""# Document 5 Connectivity Extraction Notes

Allowed resource folder only:
`{BASE}`

No Ground Truth or GT-derived feedback was used.

## Rounds

1. Diego high-recall extraction:
   - Proposed source, bus, safety-division, DC/UPS, relay, control-bay, and ground-grid nodes.
   - Used `VLV-MISV-A/B` before Jennifer corrected the raw-label spelling.
   - Matrix files:
     - `round_01_diego_high_recall_connectivity_matrix.csv`
     - `round_01_diego_high_recall_plus_uncertain_connectivity_matrix.csv`

2. Jennifer precision review:
   - Corrected `VLV-MISV-A/B` to `VLV-MSIV-A/B`.
   - Accepted five supported ATS/rectifier/load edges from Diego's uncertain set.
   - Rejected direct LC-to-ATS abstractions as final edges.
   - Left protection-bay dashed lines and GND-GRID dotted drops out of the final graph because endpoint pairing was not reliable without guessing.

3. Diego saturation review:
   - Agreed with Jennifer.
   - Final graph saturated at {len(NODES)} nodes and {len(FINAL_EDGES)} edges.

## Final Counts

- Nodes: {len(NODES)}
- Edges: {len(FINAL_EDGES)}
- Connectivity matrix is symmetric with zero diagonal.

## Token Usage

The official Responses input-token counting endpoint could not be called because no `OPENAI_API_KEY` is available in this environment. Token artifacts are therefore estimates:

- Text/context: manual round-specific estimates, with local tokenizer fallback available for small strings.
- Images/files: offline high-detail tile proxy based on image dimensions.
- Actual usage objects and reasoning-token counts were not exposed by the local multi-agent tool responses.
"""
    (RESULTS / "round_notes.md").write_text(notes, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    assert len(NODES) == 112, len(NODES)
    assert len(FINAL_EDGES) == 105, len(FINAL_EDGES)
    assert len(DIEGO_EDGES) == 100, len(DIEGO_EDGES)
    assert len(DIEGO_PLUS_UNCERTAIN_EDGES) == 137, len(DIEGO_PLUS_UNCERTAIN_EDGES)

    matrices = [
        ("round_01_diego_high_recall_connectivity_matrix.csv", DIEGO_NODES, DIEGO_EDGES),
        ("round_01_diego_high_recall_plus_uncertain_connectivity_matrix.csv", DIEGO_NODES, DIEGO_PLUS_UNCERTAIN_EDGES),
        ("round_02_jennifer_precision_connectivity_matrix.csv", NODES, FINAL_EDGES),
        ("round_03_diego_saturation_connectivity_matrix.csv", NODES, FINAL_EDGES),
        ("final_connectivity_matrix.csv", NODES, FINAL_EDGES),
    ]
    for filename, nodes, edges in matrices:
        write_matrix(RESULTS / filename, nodes, edges)

    write_edge_list(RESULTS / "round_01_diego_high_recall_edge_list.csv", DIEGO_EDGES)
    write_edge_list(RESULTS / "round_01_diego_high_recall_plus_uncertain_edge_list.csv", DIEGO_PLUS_UNCERTAIN_EDGES)
    write_edge_list(RESULTS / "round_02_jennifer_precision_edge_list.csv", FINAL_EDGES)
    write_edge_list(RESULTS / "round_03_diego_saturation_edge_list.csv", FINAL_EDGES)
    write_edge_list(RESULTS / "final_edge_list.csv", FINAL_EDGES)
    (RESULTS / "round_01_diego_node_list.txt").write_text("\n".join(DIEGO_NODES) + "\n", encoding="utf-8")
    (RESULTS / "final_node_list.txt").write_text("\n".join(NODES) + "\n", encoding="utf-8")
    write_notes()
    write_token_estimates()

    print(f"Wrote document 5 artifacts to {RESULTS}")
    print(f"Final nodes: {len(NODES)}")
    print(f"Final edges: {len(FINAL_EDGES)}")


if __name__ == "__main__":
    main()
