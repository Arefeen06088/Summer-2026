from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


DOC = "21"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = CODES / "crops"

RAW_IMAGE = BASE / "raw -- synthetic_npp_electrical_schematic_fixed.png"
OVERLAY_IMAGE = BASE / "wires_mask_overlay.png"
MASK_IMAGE = BASE / "wires_mask.png"


def ensure_dirs() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)


def add_chain(edges: list[tuple[str, str, str]], chain: list[str], evidence: str) -> None:
    for a, b in zip(chain, chain[1:]):
        edges.append((a, b, evidence))


def add_star(edges: list[tuple[str, str, str]], center: str, leaves: list[str], evidence: str) -> None:
    for leaf in leaves:
        edges.append((center, leaf, evidence))


NODES = [
    "GEN-UT",
    "CB-101",
    "DS-101A",
    "TR-UAT1",
    "CB-201A",
    "CB-102",
    "DS-101B",
    "TR-UAT2",
    "CB-201B",
    "BUS-101",
    "CB-103",
    "DS-102A",
    "TR-SU1",
    "CB-202A",
    "BUS-102",
    "CB-104",
    "DS-102B",
    "TR-SU2",
    "CB-202B",
    "BUS-201A",
    "BUS-201B",
    "BUS-202A",
    "BUS-202B",
    "DS-201A",
    "CB-105",
    "EDG-1A",
    "CB-204A",
    "DS-201B",
    "CB-106",
    "EDG-1B",
    "UCB-202A-EDG2A",
    "DS-202A",
    "CB-203A",
    "EDG-2A",
    "DS-202B",
    "CB-203B",
    "EDG-2B",
    "CB-301A",
    "DS-301A",
    "TR-SA",
    "CB-501A",
    "CB-302A",
    "DS-302A",
    "TR-NA",
    "CB-502A",
    "CB-301B",
    "DS-301B",
    "TR-SB",
    "CB-501B",
    "CB-302B",
    "DS-302B",
    "TR-NB",
    "CB-502B",
    "BUS-301A",
    "BUS-302A",
    "GND-1",
    "CB-303A",
    "MCC-1A",
    "MOTOR-SI101A",
    "PUMP-SI101A",
    "MOTOR-CCW101A",
    "PUMP-CCW101A",
    "VLV-8801A",
    "CB-304A",
    "MCC-2A",
    "MOTOR-AFW101A",
    "PUMP-AFW101A",
    "MOTOR-RHR101A",
    "PUMP-RHR101A",
    "VLV-8802A",
    "CB-503A",
    "MCC-3A",
    "MOTOR-SW101A",
    "PUMP-SW101A",
    "MOTOR-CHG101A",
    "PUMP-CHG101A",
    "MOTOR-FAN101A",
    "VLV-8901A",
    "GND-5",
    "BUS-301B",
    "BUS-302B",
    "GND-2",
    "CB-303B",
    "MCC-1B",
    "MOTOR-SI101B",
    "PUMP-SI101B",
    "MOTOR-CCW101B",
    "PUMP-CCW101B",
    "VLV-8801B",
    "CB-304B",
    "MCC-2B",
    "MOTOR-AFW101B",
    "PUMP-AFW101B",
    "MOTOR-RHR101B",
    "PUMP-RHR101B",
    "VLV-8802B",
    "CB-503B",
    "MCC-3B",
    "MOTOR-SW101B",
    "PUMP-SW101B",
    "MOTOR-CHG101B",
    "PUMP-CHG101B",
    "MOTOR-FAN101B",
    "VLV-8901B",
    "GND-6",
    "DS-401A",
    "TR-DC-A",
    "RECT-125A",
    "BUS-401A",
    "BAT-1A",
    "BAT-2A",
    "GND-3",
    "DS-401B",
    "TR-DC-B",
    "RECT-125B",
    "BUS-401B",
    "BAT-1B",
    "BAT-2B",
    "GND-4",
    "DS-402A",
    "TR-INV-A",
    "INV-120C",
    "INV-120A",
    "INV-120B",
    "DS-402B",
    "TR-INV-B",
    "RECT-24C",
    "BAT-EDG-A",
    "BAT-EDG-B",
    "BUS-501A",
    "BUS-501B",
    "CP-SWGR",
    "UVLS-A",
    "UVLS-B",
    "CP-SI-A",
    "CP-SI-B",
    "CP-CCW-A",
    "CP-CCW-B",
    "CP-EDG-A",
    "CP-EDG-B",
    "RPS-A",
    "RPS-B",
    "ESFAS-A",
    "ESFAS-B",
    "CP-CRD",
    "K101",
    "K102",
    "K103",
    "K104",
    "K105",
    "K106",
    "K107",
    "K108",
    "K109",
    "K110",
    "K111",
    "K112",
    "K113",
    "K114",
    "K115",
    "K116",
    "K117",
    "K118",
    "K119",
    "K120",
    "K121",
    "K122",
    "K123",
    "K124",
    "K125",
    "K126",
    "K127",
    "K128",
    "K129",
    "K130",
    "JB-101",
    "JB-102",
    "JB-103",
    "JB-104",
    "JB-105",
    "JB-106",
    "JB-107",
    "JB-108",
    "JB-109",
    "JB-110",
    "PT101",
    "PT102",
    "PT103",
    "FT201",
    "FT202",
    "LT301",
    "LT302",
    "TT401",
    "TT402",
    "CT501",
    "CT502",
    "VT601",
    "VT602",
    "ZS701",
    "ZS702",
]


def add_common_loads(edges: list[tuple[str, str, str]]) -> None:
    add_star(edges, "MCC-1A", ["MOTOR-SI101A", "PUMP-SI101A", "MOTOR-CCW101A", "PUMP-CCW101A", "VLV-8801A"], "solid MCC-1A load branches")
    add_star(edges, "MCC-2A", ["MOTOR-AFW101A", "PUMP-AFW101A", "MOTOR-RHR101A", "PUMP-RHR101A", "VLV-8802A"], "solid MCC-2A load branches")
    add_star(edges, "MCC-3A", ["MOTOR-SW101A", "PUMP-SW101A", "MOTOR-CHG101A", "PUMP-CHG101A", "MOTOR-FAN101A", "VLV-8901A"], "solid MCC-3A load branches")
    add_star(edges, "MCC-1B", ["MOTOR-SI101B", "PUMP-SI101B", "MOTOR-CCW101B", "PUMP-CCW101B", "VLV-8801B"], "solid MCC-1B load branches")
    add_star(edges, "MCC-2B", ["MOTOR-AFW101B", "PUMP-AFW101B", "MOTOR-RHR101B", "PUMP-RHR101B", "VLV-8802B"], "solid MCC-2B load branches")
    add_star(edges, "MCC-3B", ["MOTOR-SW101B", "PUMP-SW101B", "MOTOR-CHG101B", "PUMP-CHG101B", "MOTOR-FAN101B", "VLV-8901B"], "solid MCC-3B load branches")


def build_base_edges(b_side_neutral_corrected: bool) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for chain, evidence in [
        (["GEN-UT", "CB-101", "DS-101A", "TR-UAT1", "CB-201A", "BUS-201A"], "solid utility generator feed to 4.16 kV bus A"),
        (["GEN-UT", "CB-102", "DS-101B", "TR-UAT2", "CB-201B", "BUS-201B"], "solid utility generator feed to 4.16 kV bus B"),
        (["BUS-101", "CB-103", "DS-102A", "TR-SU1", "CB-202A", "BUS-202A"], "solid startup feed to non-1E bus A"),
        (["BUS-102", "CB-104", "DS-102B", "TR-SU2", "CB-202B", "BUS-202B"], "solid startup feed to non-1E bus B"),
        (["BUS-201A", "DS-201A", "CB-105", "EDG-1A"], "solid EDG-1A feeder"),
        (["BUS-201B", "CB-204A", "DS-201B", "CB-106", "EDG-1B"], "solid EDG-1B feeder"),
        (["BUS-202A", "UCB-202A-EDG2A", "DS-202A", "CB-203A", "EDG-2A"], "solid EDG-2A feeder with unreadable breaker tag"),
        (["BUS-202B", "DS-202B", "CB-203B", "EDG-2B"], "solid EDG-2B feeder"),
        (["BUS-201A", "CB-301A", "DS-301A", "TR-SA", "CB-501A", "BUS-301A"], "solid 4.16 kV to Train A load center A1"),
        (["BUS-202A", "CB-302A", "DS-302A", "TR-NA", "CB-502A", "BUS-302A"], "solid 4.16 kV to Train A MCC bus A2"),
        (["BUS-201B", "CB-301B", "DS-301B", "TR-SB", "CB-501B", "BUS-301B"], "solid 4.16 kV to Train B load center B1"),
    ]:
        add_chain(edges, chain, evidence)
    if b_side_neutral_corrected:
        add_chain(edges, ["BUS-202B", "CB-302B", "DS-302B", "CB-502B", "TR-NB", "BUS-302B"], "solid 4.16 kV to Train B MCC bus B2, reviewer-corrected visual order")
    else:
        add_chain(edges, ["BUS-202B", "CB-302B", "DS-302B", "TR-NB", "CB-502B", "BUS-302B"], "solid 4.16 kV to Train B MCC bus B2, Diego round1 order")

    for chain, evidence in [
        (["BUS-301A", "CB-303A", "MCC-1A"], "solid feeder to MCC-1A"),
        (["BUS-301A", "CB-304A", "MCC-2A"], "solid feeder to MCC-2A"),
        (["BUS-302A", "CB-503A", "MCC-3A"], "solid feeder to MCC-3A"),
        (["BUS-301B", "CB-303B", "MCC-1B"], "solid feeder to MCC-1B"),
        (["BUS-301B", "CB-304B", "MCC-2B"], "solid feeder to MCC-2B"),
        (["BUS-302B", "CB-503B", "MCC-3B"], "solid feeder to MCC-3B"),
    ]:
        add_chain(edges, chain, evidence)
    add_star(edges, "BUS-301A", ["GND-1"], "ground tap from BUS-301A")
    add_star(edges, "MCC-3A", ["GND-5"], "ground tap from MCC-3A")
    add_star(edges, "BUS-301B", ["GND-2"], "ground tap from BUS-301B")
    add_star(edges, "MCC-3B", ["GND-6"], "ground tap from MCC-3B")
    add_common_loads(edges)

    for chain, evidence in [
        (["BUS-301A", "DS-401A", "TR-DC-A", "RECT-125A", "BUS-401A"], "solid Train A 125 VDC supply"),
        (["BUS-301B", "DS-401B", "TR-DC-B", "RECT-125B", "BUS-401B"], "solid Train B 125 VDC supply"),
        (["BUS-302A", "DS-402A", "TR-INV-A", "INV-120C", "BUS-501A"], "solid inverter supply to 120 VAC instrument bus A"),
        (["BUS-302B", "DS-402B", "TR-INV-B", "RECT-24C", "BUS-501B"], "solid supply to 120 VAC instrument bus B"),
    ]:
        add_chain(edges, chain, evidence)
    add_star(edges, "BUS-401A", ["BAT-1A", "BAT-2A", "GND-3", "INV-120A"], "125 VDC bus A taps")
    edges.append(("INV-120A", "BUS-501A", "solid DC/AC output to 120 VAC bus A"))
    add_star(edges, "BUS-401B", ["BAT-1B", "BAT-2B", "GND-4", "INV-120B"], "125 VDC bus B taps")
    edges.append(("INV-120B", "BUS-501B", "solid DC/AC output to 120 VAC bus B"))

    add_star(edges, "BUS-501A", ["CP-SWGR", "CP-SI-A", "CP-CCW-A", "CP-EDG-A", "RPS-A", "ESFAS-A"], "dashed control taps from 120 VAC bus A")
    add_star(edges, "BUS-501B", ["CP-SI-B", "CP-CCW-B", "CP-EDG-B", "RPS-B", "ESFAS-B"], "dashed control taps from 120 VAC bus B")
    add_chain(edges, ["CP-SWGR", "CP-SI-A"], "dashed vertical control connection")
    for chain, evidence in [
        (["CP-SI-A", "K101", "K102", "K103", "JB-101"], "dashed CP-SI-A control rung"),
        (["CP-SI-B", "K104", "K105", "K106", "JB-102"], "dashed CP-SI-B control rung"),
        (["CP-CCW-A", "K107", "K108", "K109", "JB-103"], "dashed CP-CCW-A control rung"),
        (["CP-CCW-B", "K110", "K111", "K112", "JB-104"], "dashed CP-CCW-B control rung"),
        (["CP-EDG-A", "K113", "K114", "K115", "JB-105"], "dashed CP-EDG-A control rung"),
        (["CP-EDG-B", "K116", "K117", "K118", "JB-106"], "dashed CP-EDG-B control rung"),
        (["RPS-A", "K119", "K120", "K121", "JB-107"], "dashed RPS-A control rung"),
        (["RPS-B", "K122", "K123", "K124", "JB-108"], "dashed RPS-B control rung"),
        (["ESFAS-A", "K125", "K126", "K127", "JB-109"], "dashed ESFAS-A control rung"),
        (["ESFAS-B", "K128", "K129", "K130", "JB-110"], "dashed ESFAS-B control rung"),
    ]:
        add_chain(edges, chain, evidence)
    for chain, evidence in [
        (["JB-101", "PT101", "PT102"], "dotted signal from JB-101"),
        (["JB-102", "PT103", "FT201"], "dotted signal from JB-102"),
        (["JB-103", "FT202", "LT301"], "dotted signal from JB-103"),
        (["JB-104", "LT302", "TT401"], "dotted signal from JB-104"),
        (["JB-105", "TT402", "CT501"], "dotted signal from JB-105"),
        (["JB-106", "CT502"], "dotted signal from JB-106"),
        (["JB-107", "VT601"], "dotted signal from JB-107"),
        (["JB-108", "VT602"], "dotted signal from JB-108"),
        (["JB-109", "ZS701"], "dotted signal from JB-109"),
        (["JB-110", "ZS702"], "dotted signal from JB-110"),
    ]:
        add_chain(edges, chain, evidence)
    return edges


def build_diego_round1_edges() -> tuple[list[str], list[tuple[str, str, str]]]:
    edges = build_base_edges(b_side_neutral_corrected=False)
    add_chain(edges, ["CP-EDG-A", "CP-EDG-B", "RPS-A", "RPS-B", "ESFAS-A", "ESFAS-B", "CP-CRD"], "candidate dashed control-spine adjacency")
    edges.extend(
        [
            ("BAT-EDG-A", "CP-EDG-A", "candidate dashed lead from EDG battery A"),
            ("BAT-EDG-B", "CP-EDG-B", "candidate dashed lead from EDG battery B"),
            ("CP-SI-A", "UVLS-A", "candidate UVLS serial insertion"),
            ("UVLS-A", "K101", "candidate UVLS serial insertion"),
            ("K101", "UVLS-B", "candidate UVLS serial insertion"),
            ("UVLS-B", "K102", "candidate UVLS serial insertion"),
        ]
    )
    return list(NODES), edges


def build_final_edges() -> tuple[list[str], list[tuple[str, str, str]]]:
    edges = build_base_edges(b_side_neutral_corrected=True)
    edges.append(("BUS-501A", "BUS-501B", "visible normally-open tie between 120 VAC buses"))
    edges.extend(
        [
            ("K101", "UVLS-A", "UVLS-A branch tap on K101 rung"),
            ("K101", "UVLS-B", "UVLS-B branch tap on K101 rung"),
        ]
    )
    add_chain(edges, ["CP-EDG-A", "CP-EDG-B", "RPS-A", "RPS-B", "ESFAS-A", "ESFAS-B", "CP-CRD"], "dashed control-spine adjacency")
    return list(NODES), edges


def dedupe_edges(edges: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[tuple[str, str, str]] = []
    for a, b, evidence in edges:
        key = tuple(sorted((a, b)))
        if key not in seen:
            seen.add(key)
            deduped.append((a, b, evidence))
    return deduped


def validate(prefix: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    if len(nodes) != len(set(nodes)):
        duplicates = sorted({node for node in nodes if nodes.count(node) > 1})
        raise ValueError(f"{prefix}: duplicate nodes: {duplicates}")
    index = {node: i for i, node in enumerate(nodes)}
    missing = sorted({x for edge in edges for x in edge[:2] if x not in index})
    if missing:
        raise ValueError(f"{prefix}: edge references missing nodes: {missing}")
    if any(a == b for a, b, _ in edges):
        raise ValueError(f"{prefix}: self-loop found")


def write_matrix(prefix: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> dict[str, int]:
    edges = dedupe_edges(edges)
    validate(prefix, nodes, edges)
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b, _ in edges:
        i, j = index[a], index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

    if any(matrix[i][i] != 0 for i in range(len(nodes))):
        raise ValueError(f"{prefix}: diagonal is not zero")
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"{prefix}: matrix is not symmetric at {i},{j}")

    with (RESULTS / f"{prefix}_connectivity_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)

    with (RESULTS / f"{prefix}_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["idx", "label"])
        for i, node in enumerate(nodes, start=1):
            writer.writerow([i, node])

    with (RESULTS / f"{prefix}_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["from", "to", "evidence"])
        for a, b, evidence in edges:
            writer.writerow([a, b, evidence])

    with (RESULTS / f"{prefix}_sparse_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row_component", "column_component", "value"])
        for a, b, _ in edges:
            writer.writerow([a, b, 1])
            writer.writerow([b, a, 1])
    return {"nodes": len(nodes), "edges": len(edges), "ones": len(edges) * 2}


def estimate_text_tokens(text: str) -> int:
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    return max(1, int(len(text) / 4))


def estimate_image_tokens(path: Path) -> dict[str, int | str]:
    if Image is None or not path.exists():
        return {"path": str(path), "width": 0, "height": 0, "image_tokens_est": 0}
    with Image.open(path) as img:
        width, height = img.size
    scale = min(1.0, 2048 / max(width, height))
    scaled_w = int(width * scale)
    scaled_h = int(height * scale)
    tiles_x = (scaled_w + 511) // 512
    tiles_y = (scaled_h + 511) // 512
    tokens = 85 + 170 * tiles_x * tiles_y
    return {"path": str(path), "width": width, "height": height, "image_tokens_est": tokens}


def image_paths_for_round(round_name: str) -> list[Path]:
    raw_grids = [CROPS / f"raw__grid_r{r}c{c}_2x.png" for r in range(1, 5) for c in range(1, 5)]
    if round_name == "diego_r1":
        return [
            CROPS / "raw__overview.png",
            CROPS / "raw__top_band.png",
            CROPS / "raw__upper_middle_band.png",
            CROPS / "raw__middle_band.png",
            CROPS / "raw__bottom_band.png",
            CROPS / "raw__left_core.png",
            CROPS / "raw__middle_core.png",
            CROPS / "raw__right_core.png",
            *raw_grids,
            CROPS / "wires_overlay__overview.png",
            CROPS / "wires_overlay__middle_band.png",
            CROPS / "wires_overlay__bottom_band.png",
        ]
    if round_name == "jennifer_r1":
        return [
            CROPS / "raw__overview.png",
            CROPS / "raw__top_band.png",
            CROPS / "raw__upper_middle_band.png",
            CROPS / "raw__middle_band.png",
            CROPS / "raw__bottom_band.png",
            *raw_grids,
            CROPS / "wires_overlay__overview.png",
            CROPS / "wires_overlay__upper_middle_band.png",
            CROPS / "wires_overlay__middle_band.png",
            CROPS / "wires_overlay__bottom_band.png",
        ]
    return []


def write_notes_and_usage(stats: dict[str, dict[str, int]]) -> None:
    notes = [
        "# Document 21 Extraction Notes",
        "",
        "Ground truth used: no. OCR used: no. Source scope was limited to the `Raw + wires` folder.",
        "",
        "## Rounds",
        "",
        "- Round 1 Diego: high-recall graph with 200 nodes. Included the visible but unreadable EDG-2A breaker as `UCB-202A-EDG2A`, plus candidate UVLS serial edges and candidate EDG battery/control edges.",
        "- Round 1 Jennifer: kept all nodes; retained `UCB-202A-EDG2A`; corrected `DS-302B--CB-502B--TR-NB--BUS-302B`; added `BUS-501A--BUS-501B` N.O. tie; changed UVLS to branch taps from `K101`; removed unsupported `BAT-EDG-A/B` to `CP-EDG-A/B` edges.",
        "- Round 2 Diego: saturation check against Jennifer's corrections.",
        "- Round 2 Jennifer: final confirmation. Graph saturated and unchanged from round 1 Jennifer.",
        "",
        "## Final Ambiguity Handling",
        "",
        "- `BAT-EDG-A` and `BAT-EDG-B` remain visible isolated component nodes because their dashed lead destinations are not visually supported enough for a direct edge.",
        "- `CB-204A` is retained on the `BUS-201B--CB-204A--DS-201B--CB-106--EDG-1B` path with low-confidence tag readability.",
        "- `UCB-202A-EDG2A` is a visible circuit-breaker symbol on the EDG-2A feeder with no readable external tag; it is retained as an unlabeled logical breaker placeholder rather than collapsed.",
        "",
        "## Matrix Checks",
        "",
        f"- Final nodes: {stats['final']['nodes']}",
        f"- Final undirected edges: {stats['final']['edges']}",
        f"- Final nonzero matrix entries: {stats['final']['ones']}",
        "- Symmetric matrix: yes",
        "- Diagonal zeros: yes",
    ]
    (RESULTS / "round_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    diego_prompt = "Diego high-recall visual extraction prompt, node/edge schema, and Raw + wires image list."
    jennifer_prompt = "Jennifer precision review prompt with Diego node/edge proposal and Raw + wires image list."
    diego_r2_prompt = "Diego round 2 saturation prompt containing Jennifer corrections."
    jennifer_r2_prompt = "Jennifer final confirmation prompt containing Diego round 2 agreement."
    main_prompt = "Main Codex orchestration: inspect resources, create crops, manage subagents, validate graph, write artifacts, summarize usage."

    image_estimates = {
        "diego_r1": [estimate_image_tokens(p) for p in image_paths_for_round("diego_r1")],
        "jennifer_r1": [estimate_image_tokens(p) for p in image_paths_for_round("jennifer_r1")],
    }
    diego_image_total = sum(int(item["image_tokens_est"]) for item in image_estimates["diego_r1"])
    jennifer_image_total = sum(int(item["image_tokens_est"]) for item in image_estimates["jennifer_r1"])

    calls = [
        {
            "document": DOC,
            "iteration": 1,
            "call": "Main Codex orchestration and crop generation",
            "model": "gpt-5",
            "status": "actual usage unavailable in local tool transcript",
            "input_tokens_est": estimate_text_tokens(main_prompt) + 12000,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 1500,
            "output_tokens_est_expected": 3000,
            "output_tokens_est_high": 6000,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Diego R1 high-recall extractor",
            "model": "gpt-5.5",
            "status": "subagent usage object unavailable to main agent",
            "input_tokens_est": estimate_text_tokens(diego_prompt) + 5000,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 4000,
            "output_tokens_est_expected": 7500,
            "output_tokens_est_high": 12000,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": diego_image_total,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Jennifer R1 precision reviewer",
            "model": "gpt-5.5",
            "status": "subagent usage object unavailable to main agent",
            "input_tokens_est": estimate_text_tokens(jennifer_prompt) + 7500,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 1500,
            "output_tokens_est_expected": 3000,
            "output_tokens_est_high": 6000,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": jennifer_image_total,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Diego R2 saturation check",
            "model": "gpt-5.5",
            "status": "subagent usage object unavailable to main agent",
            "input_tokens_est": estimate_text_tokens(diego_r2_prompt) + 1700,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 150,
            "output_tokens_est_expected": 500,
            "output_tokens_est_high": 1200,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Jennifer R2 final confirmation",
            "model": "gpt-5.5",
            "status": "subagent usage object unavailable to main agent",
            "input_tokens_est": estimate_text_tokens(jennifer_r2_prompt) + 900,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 100,
            "output_tokens_est_expected": 250,
            "output_tokens_est_high": 800,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Main Codex artifact finalization",
            "model": "gpt-5",
            "status": "actual usage unavailable in local tool transcript",
            "input_tokens_est": 3500,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 500,
            "output_tokens_est_expected": 1200,
            "output_tokens_est_high": 2500,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
        },
    ]
    for call in calls:
        call["total_expected_est"] = (
            int(call["input_tokens_est"])
            + int(call["image_file_tokens_est"])
            + int(call["output_tokens_est_expected"])
        )
        call["total_low_est"] = (
            int(call["input_tokens_est"])
            + int(call["image_file_tokens_est"])
            + int(call["output_tokens_est_low"])
        )
        call["total_high_est"] = (
            int(call["input_tokens_est"])
            + int(call["image_file_tokens_est"])
            + int(call["output_tokens_est_high"])
        )

    usage = {
        "document": DOC,
        "iteration": 1,
        "method": "No OPENAI_API_KEY was available, so the Responses input-token counting endpoint and exact usage objects could not be queried. Text estimates use tiktoken o200k_base if installed, otherwise chars/4. Image/file estimates use the high-detail 512px tile heuristic: 85 base + 170 per tile after scaling longest side to 2048px.",
        "image_inputs": image_estimates,
        "calls": calls,
        "total_expected_est": sum(int(call["total_expected_est"]) for call in calls),
        "total_low_est": sum(int(call["total_low_est"]) for call in calls),
        "total_high_est": sum(int(call["total_high_est"]) for call in calls),
    }
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(usage, indent=2), encoding="utf-8")

    fieldnames = [
        "document",
        "iteration",
        "call",
        "model",
        "status",
        "input_tokens_est",
        "cached_input_tokens",
        "output_tokens_est_low",
        "output_tokens_est_expected",
        "output_tokens_est_high",
        "reasoning_tokens",
        "image_file_tokens_est",
        "total_low_est",
        "total_expected_est",
        "total_high_est",
    ]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    md_lines = [
        "# Document 21 Token Usage Estimate",
        "",
        "No `OPENAI_API_KEY` was available, so exact usage objects and the Responses input-token counting endpoint were unavailable.",
        "Text estimates use `tiktoken` when installed; image estimates use the high-detail 512px-tile heuristic.",
        "",
        "| Document | Iteration | Model call | Input est | Cached | Image/file est | Output low | Output expected | Output high | Reasoning | Expected total |",
        "|---|---:|---|---:|---|---:|---:|---:|---:|---|---:|",
    ]
    for call in calls:
        md_lines.append(
            "| {document} | {iteration} | {call} | {input_tokens_est} | {cached_input_tokens} | {image_file_tokens_est} | {output_tokens_est_low} | {output_tokens_est_expected} | {output_tokens_est_high} | {reasoning_tokens} | {total_expected_est} |".format(
                **call
            )
        )
    md_lines.extend(
        [
            "",
            f"Low estimate: {usage['total_low_est']}",
            f"Expected estimate: {usage['total_expected_est']}",
            f"High estimate: {usage['total_high_est']}",
        ]
    )
    (RESULTS / "token_usage_estimate.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def write_manifest(stats: dict[str, dict[str, int]]) -> None:
    manifest = {
        "document": DOC,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "resource_folder": str(BASE),
        "raw_resources_used": [str(RAW_IMAGE), str(OVERLAY_IMAGE), str(MASK_IMAGE), str(CROPS)],
        "ground_truth_used": False,
        "ocr_used": False,
        "subagents": ["Diego", "Jennifer"],
        "rounds": [
            "round1_diego",
            "round1_jennifer",
            "round2_diego",
            "round2_jennifer",
        ],
        "stats": stats,
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
        "final_edges": str(RESULTS / "final_edges.csv"),
        "final_nodes": str(RESULTS / "final_nodes.csv"),
    }
    (RESULTS / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def copy_code_artifacts() -> None:
    here = Path(__file__).resolve()
    target = CODES / here.name
    if here != target:
        shutil.copy2(here, target)
    crop_script = Path("doc21_make_visual_crops.py").resolve()
    if crop_script.exists():
        shutil.copy2(crop_script, CODES / crop_script.name)


def main() -> None:
    ensure_dirs()
    diego_nodes, diego_edges = build_diego_round1_edges()
    final_nodes, final_edges = build_final_edges()

    stats = {
        "round1_diego": write_matrix("round1_diego", diego_nodes, diego_edges),
        "round1_jennifer": write_matrix("round1_jennifer", final_nodes, final_edges),
        "round2_diego": write_matrix("round2_diego", final_nodes, final_edges),
        "round2_jennifer": write_matrix("round2_jennifer", final_nodes, final_edges),
        "final": write_matrix("final", final_nodes, final_edges),
    }
    if stats["final"]["nodes"] != 200 or stats["final"]["edges"] != 204:
        raise ValueError(f"final count mismatch: {stats['final']}")

    write_notes_and_usage(stats)
    write_manifest(stats)
    copy_code_artifacts()
    print(f"wrote {stats['final']['nodes']} nodes and {stats['final']['edges']} edges to {RESULTS}")


if __name__ == "__main__":
    main()
