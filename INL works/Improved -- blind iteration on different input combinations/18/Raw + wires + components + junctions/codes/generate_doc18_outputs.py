import csv
import json
import math
from collections import OrderedDict
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover - fallback only
    tiktoken = None


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + components + junctions"
)
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"


def tokenize_estimate(text: str) -> int:
    if not text:
        return 0
    if tiktoken is not None:
        try:
            try:
                enc = tiktoken.encoding_for_model("gpt-4o")
            except Exception:
                enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    return math.ceil(len(text) / 4)


def image_tokens_tile_high(path: Path) -> int:
    """Fallback high-detail image estimate: 85 base + 170 per 512px tile."""
    width, height = Image.open(path).size
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    short_side = min(width, height)
    if short_side > 768:
        scale = 768 / short_side
        width *= scale
        height *= scale
    tiles = math.ceil(width / 512) * math.ceil(height / 512)
    return 85 + 170 * tiles


def image_tokens_patch_high(path: Path, patch_budget: int = 2500) -> int:
    """Patch-style high estimate for current image APIs: 32px patches, capped."""
    width, height = Image.open(path).size
    scale = min(2048 / width, 2048 / height, 1.0)
    width *= scale
    height *= scale
    patches = math.ceil(width / 32) * math.ceil(height / 32)
    if patches <= patch_budget:
        return patches
    scale = math.sqrt((patch_budget * 32 * 32) / (width * height))
    width *= scale
    height *= scale
    patches = math.ceil(width / 32) * math.ceil(height / 32)
    while patches > patch_budget:
        width *= 0.995
        height *= 0.995
        patches = math.ceil(width / 32) * math.ceil(height / 32)
    return patches


def add_path(edges, nodes, edge_type, evidence):
    for source, target in zip(nodes, nodes[1:]):
        edges.append((source, target, edge_type, evidence))


def dedupe_edges(edges):
    seen = OrderedDict()
    for source, target, edge_type, evidence in edges:
        key = tuple(sorted((source, target)))
        if key not in seen:
            seen[key] = [source, target, edge_type, evidence]
        else:
            # Preserve the first edge but retain additional evidence/type notes.
            prev = seen[key]
            if edge_type not in prev[2].split("|"):
                prev[2] += "|" + edge_type
            if evidence not in prev[3]:
                prev[3] += " | " + evidence
    return [tuple(v) for v in seen.values()]


def write_edge_list(path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "edge_type", "evidence"])
        for row in dedupe_edges(edges):
            writer.writerow(row)


def write_matrix(path, nodes, edges):
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target, _edge_type, _evidence in dedupe_edges(edges):
        if source not in index or target not in index:
            raise ValueError(f"Unknown node in edge: {source!r}, {target!r}")
        i = index[source]
        j = index[target]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


PRIMARY_NODES = [
    "GRID-SWYD 1",
    "CB-GRID-A",
    "GRID-SWYD 2",
    "CB-GRID-B",
    "BB-SWYD-230",
    "CB-GEN-ISO",
    "GEN-MAIN-1",
    "TR-UAT-1A",
    "CB-UAT-A",
    "TR-UAT-1B",
    "CB-UAT-B",
    "TR-SAT-1A",
    "CB-SAT-A",
    "TR-SAT-1B",
    "CB-SAT-B",
    "BUS-4160A",
    "BUS-4160B",
    "CB-4160 TIE",
    "DG-1A",
    "CB-DG-A",
    "DG-1B",
    "CB-DG-B",
    "GND-4160A",
    "GND-4160B",
    "PT-4160A",
    "FU-PT-A",
    "XFMR-CTRL A",
    "TB-RPS-A",
    "SW-43A",
    "PT-4160B",
    "FU-PT-B",
    "XFMR-CTRL B",
    "TB-RPS-B",
    "SW-43B",
    "TR-480-A1",
    "CB-480A-IN",
    "BUS-480A",
    "TR-480-B1",
    "CB-480B-IN",
    "BUS-480B",
    "TR-480-C1",
    "CB-480C-IN",
    "BUS-480C",
    "TR-480-D1",
    "CB-480D-IN",
    "BUS-480D",
]

A_CHAINS = [
    ["CB-A01", "DS-A01", "MS-A01", "PUMP-CCW-A1"],
    ["CB-A02", "DS-A02", "MS-A02", "PUMP-RHR-A1"],
    ["CB-A03", "FS-A03", "MS-A03", "FAN-RB-A1"],
    ["CB-A04", "DS-A04", "RY-A04", "MOV-SI-A11"],
    ["CB-A05", "DS-A05", "CP-A05", "PNL-LTG-A1"],
    ["CB-A06", "DS-A06", "MS-A06", "PUMP-AFW-A1"],
    ["CB-A07", "FS-A07", "FU-A07", "HTR-PZR-A1"],
    ["CB-A08", "DS-A08", "TB-A08", "SPARE-A8"],
]
B_CHAINS = [
    ["CB-B01", "DS-B01", "MS-B01", "PUMP-CCW-B1"],
    ["CB-B02", "DS-B02", "MS-B02", "PUMP-RHR-B1"],
    ["CB-B03", "FS-B03", "MS-B03", "FAN-FUEL-B1"],
    ["CB-B04", "DS-B04", "RY-B04", "MOV-CCW-B21"],
    ["CB-B05", "DS-B05", "CP-B05", "MCC-AUX-B6"],
    ["CB-B06", "DS-B06", "MS-B06", "AIR-CMP-B1"],
    ["CB-B07", "FS-B07", "RY-B07", "VLV-CHG-B1"],
]
C_CHAINS = [
    ["CB-C01", "DS-C01", "MS-C01", "PUMP-HPCI-C1"],
    ["CB-C02", "DS-C02", "MS-C02", "PUMP-RCW-C1"],
    ["CB-C03", "FS-C03", "MS-C03", "FAN-RB-C1"],
    ["CB-C04", "DS-C04", "RY-C04", "MOV-RHR-C11"],
    ["CB-C05", "DS-C05", "MS-C05", "PUMP-SEAL-C1"],
    ["CB-C06", "DS-C06", "CP-C06", "PNL-IC-C7"],
    ["CB-C07", "FS-C07", "MS-C07", "SUMP-PMP-C1"],
    ["CB-C08", "DS-C08", "FU-C08", "HTR-VENT-C2"],
]
D_CHAINS = [
    ["CB-D01", "DS-D01", "MS-D01", "PUMP-AFW-D1"],
    ["CB-D02", "DS-D02", "MS-D02", "FAN-CR-D1"],
    ["CB-D03", "FS-D03", "RY-D03", "MOV-SI-D21"],
    ["CB-D04", "DS-D04", "MS-D04", "PUMP-LUBE-D1"],
    ["CB-D05", "DS-D05", "CP-D05", "PNL-ESS-D5"],
    ["CB-D06", "DS-D06", "MS-D06", "COMP-AIR-D1"],
    ["CB-D07", "FS-D07", "TB-D07", "SPARE-D7"],
]

CONTROL_A = [
    "BUS-125A",
    "BAT-125A",
    "CHG-125A",
    "REC-125A",
    "CB-DC-A",
    "GND-DC-A",
    "INV-120A",
    "UPS-120A",
    "BUS-120A",
    "RPS-PNL-A",
    "PLC-RPS-A",
    "RELAY-K101",
    "RELAY-K102",
    "RELAY-K103",
    "RELAY-K104",
    "JB-RPS-A",
    "PNL-ANN-A",
]
CONTROL_B = [
    "BUS-125B",
    "BAT-125B",
    "CHG-125B",
    "REC-125B",
    "CB-DC-B",
    "GND-DC-B",
    "INV-120B",
    "UPS-120B",
    "BUS-120B",
    "RPS-PNL-B",
    "PLC-RPS-B",
    "RELAY-K201",
    "RELAY-K202",
    "RELAY-K203",
    "RELAY-K204",
    "JB-RPS-B",
    "PNL-ANN-B",
]

NODES = (
    PRIMARY_NODES
    + [node for chain in A_CHAINS for node in chain]
    + [node for chain in B_CHAINS for node in chain]
    + [node for chain in C_CHAINS for node in chain]
    + [node for chain in D_CHAINS for node in chain]
    + CONTROL_A
    + CONTROL_B
)


def base_edges(final_tb_rps_a: bool, final_relays: bool):
    edges = []
    add_path(edges, ["GRID-SWYD 1", "CB-GRID-A", "BB-SWYD-230"], "solid", "incoming grid feeder to 230 bus")
    add_path(edges, ["GRID-SWYD 2", "CB-GRID-B", "BB-SWYD-230"], "solid", "incoming grid feeder to 230 bus")
    add_path(edges, ["BB-SWYD-230", "TR-SAT-1A", "CB-SAT-A", "BUS-4160A"], "solid", "station auxiliary transformer A feeder")
    add_path(edges, ["BB-SWYD-230", "TR-SAT-1B", "CB-SAT-B", "BUS-4160B"], "solid", "station auxiliary transformer B feeder")
    add_path(edges, ["BB-SWYD-230", "CB-GEN-ISO", "GEN-MAIN-1"], "solid", "generator isolation connection to 230 bus")
    add_path(edges, ["GEN-MAIN-1", "TR-UAT-1A", "CB-UAT-A"], "solid", "generator auxiliary transformer branch")
    add_path(edges, ["GEN-MAIN-1", "TR-UAT-1B", "CB-UAT-B"], "solid", "generator auxiliary transformer branch")
    add_path(edges, ["DG-1A", "CB-DG-A", "BUS-4160A"], "solid", "diesel generator A feeder")
    add_path(edges, ["DG-1B", "CB-DG-B", "BUS-4160B"], "solid", "diesel generator B feeder")
    add_path(edges, ["BUS-4160A", "CB-4160 TIE", "BUS-4160B"], "solid_normally_open_physical", "drawn 4160 bus tie marked N.O.; physical edge, not bus merge")
    add_path(edges, ["BUS-4160A", "GND-4160A"], "solid", "ground tap from bus")
    add_path(edges, ["BUS-4160B", "GND-4160B"], "solid", "ground tap from bus")
    if final_tb_rps_a:
        add_path(edges, ["BUS-4160A", "TB-RPS-A", "TR-480-A1", "CB-480A-IN", "BUS-480A"], "solid", "A-side 480 transformer feeder through visible TB-RPS-A")
    else:
        add_path(edges, ["BUS-4160A", "TR-480-A1", "CB-480A-IN", "BUS-480A"], "solid", "A-side 480 transformer feeder; TB-RPS-A omitted in this round")
    add_path(edges, ["BUS-4160A", "TR-480-B1", "CB-480B-IN", "BUS-480B"], "solid", "B 480 transformer feeder")
    add_path(edges, ["BUS-4160B", "TR-480-C1", "CB-480C-IN", "BUS-480C"], "solid", "C 480 transformer feeder")
    add_path(edges, ["BUS-4160B", "TR-480-D1", "CB-480D-IN", "BUS-480D"], "solid", "D 480 transformer feeder")
    add_path(edges, ["BUS-4160A", "PT-4160A", "FU-PT-A", "XFMR-CTRL A", "TB-RPS-A", "SW-43A"], "dashed", "A PT/RPS dashed control chain")
    add_path(edges, ["BUS-4160B", "PT-4160B", "FU-PT-B", "XFMR-CTRL B", "TB-RPS-B", "SW-43B"], "dashed", "B PT/RPS dashed control chain")

    for bus, chains in [
        ("BUS-480A", A_CHAINS),
        ("BUS-480B", B_CHAINS),
        ("BUS-480C", C_CHAINS),
        ("BUS-480D", D_CHAINS),
    ]:
        for chain in chains:
            add_path(edges, [bus] + chain, "solid", f"{bus} vertical feeder chain")

    add_path(edges, ["BUS-480B", "CHG-125A", "REC-125A", "CB-DC-A", "BUS-125A"], "solid", "Train A DC supply chain")
    add_path(edges, ["BAT-125A", "BUS-125A"], "solid", "Train A battery tap")
    add_path(edges, ["BUS-125A", "GND-DC-A"], "solid", "Train A DC ground")
    add_path(edges, ["BUS-125A", "INV-120A"], "solid", "Train A inverter DC feed")
    add_path(edges, ["INV-120A", "UPS-120A"], "dashed", "Train A inverter to UPS dashed link")
    add_path(edges, ["UPS-120A", "BUS-120A"], "solid", "Train A UPS output to 120 VAC bus")
    add_path(edges, ["BUS-120A", "RPS-PNL-A"], "solid", "Train A RPS panel feed")
    add_path(edges, ["RPS-PNL-A", "PLC-RPS-A"], "dashed", "Train A RPS panel to PLC dashed signal")

    add_path(edges, ["BUS-480C", "CHG-125B", "REC-125B", "CB-DC-B", "BUS-125B"], "solid", "Train B DC supply chain")
    add_path(edges, ["BAT-125B", "BUS-125B"], "solid", "Train B battery tap")
    add_path(edges, ["BUS-125B", "GND-DC-B"], "solid", "Train B DC ground")
    add_path(edges, ["BUS-125B", "INV-120B"], "solid", "Train B inverter DC feed")
    add_path(edges, ["INV-120B", "UPS-120B"], "dashed", "Train B inverter to UPS dashed link")
    add_path(edges, ["UPS-120B", "BUS-120B"], "solid", "Train B UPS output to 120 VAC bus")
    add_path(edges, ["BUS-120B", "RPS-PNL-B"], "solid", "Train B RPS panel feed")
    add_path(edges, ["RPS-PNL-B", "PLC-RPS-B"], "dashed", "Train B RPS panel to PLC dashed signal")

    if final_relays:
        for target in ["RELAY-K101", "RELAY-K102", "RELAY-K103", "RELAY-K104", "JB-RPS-A"]:
            add_path(edges, ["PLC-RPS-A", target], "dashed", "Train A PLC dashed branch")
        for target in ["RELAY-K201", "RELAY-K202", "RELAY-K203", "RELAY-K204", "JB-RPS-B"]:
            add_path(edges, ["PLC-RPS-B", target], "dashed", "Train B PLC dashed branch")

    add_path(edges, ["RELAY-K102", "PNL-ANN-A"], "dashed", "Train A relay annunciator branch")
    add_path(edges, ["RELAY-K202", "PNL-ANN-B"], "dashed", "Train B relay annunciator branch")
    return dedupe_edges(edges)


ROUND_EDGES = {
    "round_01_diego": base_edges(final_tb_rps_a=True, final_relays=True),
    "round_02_jennifer": base_edges(final_tb_rps_a=False, final_relays=False),
    "round_03_diego": base_edges(final_tb_rps_a=False, final_relays=True),
    "round_04_jennifer_final": base_edges(final_tb_rps_a=True, final_relays=True),
}
FINAL_EDGES = ROUND_EDGES["round_04_jennifer_final"]


def write_node_list():
    with (RESULTS / "final_node_list.txt").open("w", encoding="utf-8") as f:
        for node in NODES:
            f.write(node + "\n")


def write_uncertain_files():
    rows = [
        ["round", "source", "target", "status", "note"],
        ["round_01_diego", "CB-GEN-ISO", "GEN-MAIN-1", "kept_final", "Diego flagged a small visual gap; Jennifer kept as supported."],
        ["round_01_diego", "BUS-125A", "INV-120A", "kept_final", "Initially uncertain; final supported by visual bus stub."],
        ["round_01_diego", "BUS-125B", "INV-120B", "kept_final", "Initially uncertain; final supported by visual bus stub."],
        ["round_01_diego", "CB-4160 TIE", "BUS-4160B", "kept_final_normally_open", "Physical edge kept; buses not collapsed because tie is marked N.O."],
        ["round_02_jennifer", "PLC-RPS-A", "RELAY-K101/K102/K103/K104/JB-RPS-A", "reopened", "Jennifer initially held relay branches uncertain."],
        ["round_02_jennifer", "PLC-RPS-B", "RELAY-K201/K202/K203/K204/JB-RPS-B", "reopened", "Jennifer initially held relay branches uncertain."],
        ["round_03_diego", "PLC-RPS-A", "RELAY-K102/RELAY-K104/JB-RPS-A", "kept_final", "Diego marked less explicit; final Jennifer accepted from zoom crop."],
        ["round_03_diego", "PLC-RPS-B", "RELAY-K202/RELAY-K204/JB-RPS-B", "kept_final", "Diego marked less explicit; final Jennifer accepted from zoom crop."],
        ["round_04_jennifer_final", "", "", "none_remaining", "No final uncertain edges included in the matrix."],
    ]
    with (RESULTS / "uncertain_candidates_by_round.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

    excluded = [
        ["source", "target", "reason"],
        ["CB-UAT-A", "BUS-4160A", "No visible downstream edge from CB-UAT-A to a 4160 bus."],
        ["CB-UAT-B", "BUS-4160B", "No visible downstream edge from CB-UAT-B to a 4160 bus."],
        ["BUS-4160A", "TR-480-A1", "Direct edge replaced by BUS-4160A -> TB-RPS-A -> TR-480-A1."],
        ["BUS-4160B", "TB-RPS-B", "TB-RPS-B is dashed PT/control only; no solid B-side transformer feeder edge."],
        ["TB-RPS-B", "TR-480-D1", "B-side transformer feeder is separate from TB-RPS-B."],
        ["RELAY-K101", "RELAY-K102", "No relay-to-relay edge confirmed; dashed branches are PLC-to-device."],
        ["PLC-RPS-A", "PNL-ANN-A", "Annunciator connection is via RELAY-K102, not direct from PLC."],
        ["PLC-RPS-B", "PNL-ANN-B", "Annunciator connection is via RELAY-K202, not direct from PLC."],
    ]
    with (RESULTS / "excluded_edges.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(excluded)


def write_round_notes():
    note = f"""# Document 18 Connectivity Extraction Notes

Allowed resource folder only:
`{BASE}`

No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels and topology were read visually from the raw image and allowed derived overlays/crops.

## Rounds

1. Diego high-recall extraction: broad primary/4160/480/control topology, all 480 feeder chains, lower Train A/B control power, and plausible PLC-to-relay/JB dashed branches.
2. Jennifer precision review: retained power topology, pruned relay fanout as uncertain, and removed unsupported UAT-to-4160 downstream edges.
3. Diego second extraction: agreed on power topology and reintroduced visible PLC-to-relay/JB dashed branches as visually supported.
4. Jennifer final correction: accepted all PLC-to-relay/JB dashed branches, kept K102/K202 annunciator branches, and corrected the A-side supply path to `BUS-4160A -> TB-RPS-A -> TR-480-A1`.

## Final Matrix Policy

- `1` means a visually supported undirected connection.
- Solid power, dashed control/signal, and normally-open physical ties are all represented as `1` in the matrix.
- Edge type/status is preserved in `final_edge_list.csv`.
- The normally-open `CB-4160 TIE` is kept as a physical edge but `BUS-4160A` and `BUS-4160B` are not collapsed into one node.

## Final Size

- Nodes: {len(NODES)}
- Edges: {len(FINAL_EDGES)}
"""
    (RESULTS / "round_notes.md").write_text(note, encoding="utf-8")


def write_token_usage():
    raw = BASE / "raw -- synthetic_nuclear_electrical_schematic_readable.png"
    components = BASE / "detected_components_overlay.png"
    wire_nodes = BASE / "wire_nodes_overlay.png"
    prompts = {
        "main_agent_aggregate": "Main agent inspected allowed images, generated crops, orchestrated Diego and Jennifer, reconciled final edges, and wrote artifacts.",
        "diego_round_01": "High-recall visual extractor prompt with full raw/derived overlays and major crops; propose nodes, edges, uncertain candidates.",
        "jennifer_round_02": "Precision reviewer prompt with Diego proposal and focused images; remove unsupported edges and refine labels/topology.",
        "diego_round_03": "Second Diego prompt reviewing Jennifer refinement, relay topology, source ties, inverter feeds, and normally-open tie.",
        "jennifer_round_04a_interrupted": "Relay-only Jennifer final prompt; interrupted before usable completion by expanded final review.",
        "jennifer_round_04b_final": "Expanded Jennifer final prompt covering relay branches and TB-RPS-A/TB-RPS-B feeder decisions.",
    }
    main_images = [
        raw,
        wire_nodes,
        components,
        CROPS / "raw__middle_panel_450a.png",
        CROPS / "raw__middle_panel_400b.png",
        CROPS / "raw__bottom_train_a.png",
        CROPS / "raw__top_left_power_sources.png",
        CROPS / "raw__top_center_bus_links.png",
        CROPS / "raw__top_right_power_sources.png",
        CROPS / "raw__middle_panel_400c.png",
        CROPS / "raw__middle_panel_400d.png",
        CROPS / "raw__bottom_train_b.png",
        CROPS / "wire_nodes__top_right_power_sources.png",
        CROPS / "components__top_right_power_sources.png",
        CROPS / "raw__top_right_generator_detail.png",
        CROPS / "raw__source_to_4160a_detail.png",
        CROPS / "raw__source_to_4160b_detail.png",
        CROPS / "raw__dg_b_far_right_detail.png",
        CROPS / "wire_nodes__dg_b_far_right_detail.png",
        CROPS / "raw__relay_block_train_a.png",
        CROPS / "wire_nodes__relay_block_train_a.png",
        CROPS / "raw__relay_block_train_b.png",
        CROPS / "wire_nodes__relay_block_train_b.png",
        CROPS / "raw__relay_block_train_a_detail_2x.png",
        CROPS / "raw__relay_block_train_b_detail_2x.png",
        CROPS / "components__source_to_4160a_detail.png",
        CROPS / "wire_nodes__source_to_4160a_detail.png",
        CROPS / "wires__source_to_4160a_detail.png",
        CROPS / "components__source_to_4160b_detail.png",
        CROPS / "wire_nodes__source_to_4160b_detail.png",
        CROPS / "wires__source_to_4160b_detail.png",
    ]
    diego_r1_images = [
        raw,
        components,
        wire_nodes,
        CROPS / "raw__top_left_power_sources.png",
        CROPS / "raw__top_center_bus_links.png",
        CROPS / "raw__top_right_power_sources.png",
        CROPS / "raw__middle_panel_450a.png",
        CROPS / "raw__middle_panel_400b.png",
        CROPS / "raw__middle_panel_400c.png",
        CROPS / "raw__middle_panel_400d.png",
        CROPS / "raw__bottom_train_a.png",
        CROPS / "raw__bottom_train_b.png",
    ]
    jennifer_r2_images = [
        raw,
        wire_nodes,
        CROPS / "raw__source_to_4160a_detail.png",
        CROPS / "raw__source_to_4160b_detail.png",
        CROPS / "raw__dg_b_far_right_detail.png",
        CROPS / "raw__middle_panel_450a.png",
        CROPS / "raw__middle_panel_400b.png",
        CROPS / "raw__middle_panel_400c.png",
        CROPS / "raw__middle_panel_400d.png",
        CROPS / "raw__bottom_train_a.png",
        CROPS / "raw__bottom_train_b.png",
        CROPS / "raw__relay_block_train_a.png",
        CROPS / "raw__relay_block_train_b.png",
    ]
    diego_r3_images = [
        CROPS / "raw__relay_block_train_a_detail_2x.png",
        CROPS / "raw__relay_block_train_b_detail_2x.png",
        CROPS / "raw__source_to_4160a_detail.png",
        CROPS / "raw__source_to_4160b_detail.png",
        CROPS / "raw__bottom_train_a.png",
        CROPS / "raw__bottom_train_b.png",
    ]
    jennifer_r4a_images = [
        CROPS / "raw__relay_block_train_a_detail_2x.png",
        CROPS / "raw__relay_block_train_b_detail_2x.png",
        CROPS / "wire_nodes__relay_block_train_a.png",
        CROPS / "wire_nodes__relay_block_train_b.png",
    ]
    jennifer_r4b_images = [
        CROPS / "raw__relay_block_train_a_detail_2x.png",
        CROPS / "raw__relay_block_train_b_detail_2x.png",
        CROPS / "raw__source_to_4160a_detail.png",
        CROPS / "wire_nodes__source_to_4160a_detail.png",
        CROPS / "wires__source_to_4160a_detail.png",
        CROPS / "raw__source_to_4160b_detail.png",
        CROPS / "wires__source_to_4160b_detail.png",
    ]

    calls = [
        ("main_agent_aggregate", "main", "completed_estimated", main_images, 650, 520, "Aggregate main-agent orchestration; exact internal call count and usage are not exposed."),
        ("diego_round_01", "Diego", "completed", diego_r1_images, 2700, 2600, "High-recall extractor output estimated from returned proposal."),
        ("jennifer_round_02", "Jennifer", "completed", jennifer_r2_images, 3000, 2500, "Precision reviewer output estimated from returned refinement."),
        ("diego_round_03", "Diego", "completed", diego_r3_images, 1800, 320, "Second Diego delta output estimated from returned message."),
        ("jennifer_round_04a_interrupted", "Jennifer", "interrupted_no_matrix", jennifer_r4a_images, 420, 0, "Likely submitted then interrupted; no usable output/usage object returned."),
        ("jennifer_round_04b_final", "Jennifer", "completed_final", jennifer_r4b_images, 520, 520, "Final agreement output estimated from returned message."),
    ]
    rows = []
    totals = {
        "input_text_tokens_est": 0,
        "image_file_input_tokens_tile_est": 0,
        "image_file_input_tokens_patch_high_est": 0,
        "output_tokens_est": 0,
        "expected_total_tokens_tile_est": 0,
        "high_total_tokens_patch_est": 0,
    }
    for call_id, agent, status, images, extra_text_tokens, output_tokens, notes in calls:
        text_tokens = tokenize_estimate(prompts[call_id]) + extra_text_tokens
        image_tile = sum(image_tokens_tile_high(p) for p in images)
        image_patch = sum(image_tokens_patch_high(p) for p in images)
        cached = 0
        expected_total = text_tokens + image_tile + output_tokens
        high_total = text_tokens + image_patch + math.ceil(output_tokens * 1.2)
        low_output = 0 if "interrupted" in call_id else math.floor(output_tokens * 0.85)
        high_output = 800 if "interrupted" in call_id else math.ceil(output_tokens * 1.2)
        row = {
            "document": "18",
            "iteration": "1",
            "round": call_id,
            "agent": agent,
            "status": status,
            "input_text_tokens_est": text_tokens,
            "cached_input_tokens_est": cached,
            "image_file_input_tokens_tile_est": image_tile,
            "image_file_input_tokens_patch_high_est": image_patch,
            "output_tokens_est": output_tokens,
            "reasoning_tokens": "unavailable",
            "low_output_tokens_est": low_output,
            "expected_output_tokens_est": output_tokens,
            "high_output_tokens_est": high_output,
            "expected_total_tokens_tile_est": expected_total,
            "high_total_tokens_patch_est": high_total,
            "usage_object_available": "no",
            "notes": notes,
        }
        rows.append(row)
        for key in totals:
            totals[key] += row[key] if isinstance(row[key], int) else 0

    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "document": "18",
        "iteration": "1",
        "method": "OPENAI_API_KEY missing, so Responses input-token endpoint was not called. Text estimated with tiktoken when local encoding assets are available, otherwise chars/4 fallback; image/file input estimated locally.",
        "responses_input_token_endpoint": "https://platform.openai.com/docs/api-reference/responses/input-tokens",
        "image_token_estimate_notes": "tile_est uses 85 + 170 per 512 tile after high-detail resizing; patch_high_est uses 32px patches capped at 2500 per image as a conservative current-model alternative.",
        "actual_usage_objects": "not exposed by Codex subagent tools in this run",
        "totals": totals,
        "calls": rows,
    }
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    md = [
        "# Token Usage Estimate",
        "",
        "No `OPENAI_API_KEY` was present, so the Responses input-token counting endpoint could not be called.",
        "Actual usage objects were not exposed by the Codex subagent tool responses.",
        "Text estimates use local tokenizer assets when available, otherwise a chars/4 fallback; image/file estimates are local approximations.",
        "",
        "| Document | Iteration | Call | Agent | Text In | Image/File In Tile Est | Output Est | Expected Total | Status |",
        "|---|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        md.append(
            f"| 18 | 1 | {row['round']} | {row['agent']} | {row['input_text_tokens_est']} | "
            f"{row['image_file_input_tokens_tile_est']} | {row['output_tokens_est']} | "
            f"{row['expected_total_tokens_tile_est']} | {row['status']} |"
        )
    md.extend(
        [
            "",
            f"Expected total, tile estimate: {totals['expected_total_tokens_tile_est']}",
            f"High total, patch estimate: {totals['high_total_tokens_patch_est']}",
            "",
            "Low/expected/high output estimates are in `token_usage_estimates.csv`.",
        ]
    )
    (RESULTS / "token_usage_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    if len(NODES) != len(set(NODES)):
        duplicates = [node for node in NODES if NODES.count(node) > 1]
        raise ValueError(f"Duplicate nodes: {sorted(set(duplicates))}")

    write_node_list()
    for round_name, edges in ROUND_EDGES.items():
        write_edge_list(RESULTS / f"{round_name}_edge_list.csv", edges)
        write_matrix(RESULTS / f"{round_name}_connectivity_matrix.csv", NODES, edges)
    write_edge_list(RESULTS / "final_edge_list.csv", FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", NODES, FINAL_EDGES)
    write_uncertain_files()
    write_round_notes()
    write_token_usage()
    print(f"Wrote results to {RESULTS}")
    print(f"Nodes: {len(NODES)}")
    print(f"Final edges: {len(FINAL_EDGES)}")


if __name__ == "__main__":
    main()
