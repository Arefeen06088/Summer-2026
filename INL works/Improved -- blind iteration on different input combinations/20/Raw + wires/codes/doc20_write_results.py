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


DOC = "20"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = CODES / "crops"

RAW_IMAGE = BASE / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png"
OVERLAY_IMAGE = BASE / "wires_mask_overlay.png"
MASK_IMAGE = BASE / "wires_mask.png"


def ensure_dirs() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)


def add_chain(edges: list[tuple[str, str, str]], chain: list[str], evidence: str) -> None:
    for a, b in zip(chain, chain[1:]):
        edges.append((a, b, evidence))


def build_diego_round1_edges() -> tuple[list[str], list[tuple[str, str, str]]]:
    nodes = [
        "GEN-M1",
        "CB-GEN1",
        "TR-UAT1",
        "CB-13A-IN",
        "BUS-13K-A",
        "CB-TIE-13K",
        "BUS-13K-B",
        "FEED-230A",
        "TR-SAT1",
        "CB-13B-IN",
        "CB-F41A",
        "DS-F41A",
        "TR-416A",
        "CB-416A-IN",
        "BUS-416-A",
        "DG-1A",
        "CB-DG1A",
        "CB-TIE-416",
        "BUS-416-B",
        "CB-F41B",
        "DS-F41B",
        "TR-416B",
        "CB-416B-IN",
        "DG-1B",
        "CB-DG1B",
        "CB-LCA",
        "TR-480A",
        "BUS-480-A",
        "CB-LCB",
        "TR-480B",
        "BUS-480-B",
        "CB-TIE-480",
        "BUS-480-C",
        "CB-LCC",
        "TR-480C",
        "CB-LCD",
        "TR-480D",
        "BUS-480-D",
    ]
    edges: list[tuple[str, str, str]] = []
    add_chain(edges, ["GEN-M1", "CB-GEN1", "TR-UAT1", "CB-13A-IN", "BUS-13K-A"], "solid AC power, top band")
    add_chain(edges, ["BUS-13K-A", "CB-TIE-13K", "BUS-13K-B"], "solid AC tie, top band")
    add_chain(edges, ["FEED-230A", "TR-SAT1", "CB-13B-IN", "BUS-13K-B"], "solid AC offsite feed, top band")
    add_chain(edges, ["BUS-13K-A", "CB-F41A", "DS-F41A", "TR-416A", "CB-416A-IN", "BUS-416-A"], "solid AC stepdown, upper-left")
    add_chain(edges, ["BUS-13K-B", "CB-F41B", "DS-F41B", "TR-416B", "CB-416B-IN", "BUS-416-B"], "solid AC stepdown, upper-middle")
    add_chain(edges, ["DG-1A", "CB-DG1A", "BUS-416-A"], "solid emergency generator feed")
    add_chain(edges, ["DG-1B", "CB-DG1B", "BUS-416-B"], "solid emergency generator feed")
    add_chain(edges, ["BUS-416-A", "CB-TIE-416", "BUS-416-B"], "solid 4.16 kV bus tie")
    add_chain(edges, ["BUS-416-A", "CB-LCA", "TR-480A", "BUS-480-A"], "solid 480 V load-center feed")
    add_chain(edges, ["BUS-416-A", "CB-LCB", "TR-480B", "BUS-480-B"], "solid 480 V load-center feed")
    add_chain(edges, ["BUS-416-B", "CB-LCC", "TR-480C", "BUS-480-C"], "solid 480 V load-center feed")
    add_chain(edges, ["BUS-416-B", "CB-LCD", "TR-480D", "BUS-480-D"], "solid 480 V load-center feed")
    add_chain(edges, ["BUS-480-B", "CB-TIE-480", "BUS-480-C"], "solid 480 V bus tie")

    feeders = {
        "A": [
            ("1", "MCC-1A", "RELAY-K1A", "PMP-RHR-101A"),
            ("2", "MCC-2A", "CS-2A", "MOV-CCW-112A"),
            ("3", "MCC-3A", "RELAY-K3A", "FAN-RB-104A"),
            ("4", "JB-4A", "CS-4A", "HTR-PZR-01A"),
            ("5", "MCC-5A", "RELAY-K5A", "COMP-IA-201A"),
            ("6", "JB-6A", "CS-6A", "MOT-CRN-01A"),
        ],
        "B": [
            ("1", "MCC-1B", "RELAY-K1B", "PMP-SI-102B"),
            ("2", "MCC-2B", "CS-2B", "MOV-CS-116B"),
            ("3", "MCC-3B", "RELAY-K3B", "FAN-CCW-108B"),
            ("4", "JB-4B", "CS-4B", "HTR-SUMP-02B"),
            ("5", "MCC-5B", "RELAY-K5B", "PMP-CHG-203B"),
            ("6", "JB-6B", "CS-6B", "MOV-SW-118B"),
        ],
        "C": [
            ("1", "MCC-1C", "RELAY-K1C", "PMP-RHR-101C"),
            ("2", "MCC-2C", "CS-2C", "MOV-CCW-112C"),
            ("3", "MCC-3C", "RELAY-K3C", "FAN-RB-104C"),
            ("4", "JB-4C", "RELAY-K4C", "PMP-AFW-205C"),
            ("5", "MCC-5C", "RELAY-K5C", "PMP-CCP-207C"),
            ("6", "JB-6C", "CS-6C", "MOV-FCV-022C"),
        ],
        "D": [
            ("1", "MCC-1D", "RELAY-K1D", "PMP-SI-102D"),
            ("2", "MCC-2D", "CS-2D", "MOV-CS-116D"),
            ("3", "MCC-3D", "RELAY-K3D", "FAN-ESF-110D"),
            ("4", "JB-4D", "CS-4D", "MOV-RWST-24D"),
            ("5", "MCC-5D", "RELAY-K5D", "PMP-CHG-203D"),
            ("6", "JB-6D", "CS-6D", "MOV-SW-118D"),
        ],
    }
    for train, rows in feeders.items():
        bus = f"BUS-480-{train}"
        for n, mid, device, load in rows:
            cb = f"CB-48{train}{n}"
            ds = f"DS-48{train}{n}"
            add_chain(edges, [bus, cb, ds, mid, device, load], f"480 VAC feeder {train}{n}")
            nodes.extend([cb, ds, mid, device, load])

    dc_nodes = [
        "BAT-125A",
        "CHGR-125A",
        "RECT-125A",
        "INV-UPS-A",
        "BUS-125DCA",
        "BAT-125B",
        "CHGR-125B",
        "RECT-125B",
        "INV-UPS-B",
        "BUS-125DCB",
        "CP-RPS-A",
        "TB-RPS-A",
        "PROT-UV-A",
        "RELAY-K101",
        "PT-410A",
        "LT-512A",
        "RELAY-K102",
        "TT-303A",
        "GND-CTRL-A",
        "CP-RPS-B",
        "TB-RPS-B",
        "PROT-UV-B",
        "RELAY-K103",
        "PT-410B",
        "LT-512B",
        "RELAY-K104",
        "TT-303B",
        "GND-CTRL-B",
        "CP-ESFAS-A",
        "JB-ESF-A",
        "PROT-LOP-A",
        "RELAY-K105",
        "FT-611A",
        "RELAY-K106",
        "XA-730A",
        "A/B-ESF-INTERLOCK",
        "CP-ESFAS-B",
        "JB-ESF-B",
        "PROT-LOP-B",
        "RELAY-K107",
        "FT-611B",
        "RELAY-K108",
        "XA-730B",
    ]
    nodes.extend(dc_nodes)
    add_chain(edges, ["BUS-480-A", "RECT-125A"], "solid AC rectifier feed")
    add_chain(edges, ["BAT-125A", "CHGR-125A", "RECT-125A", "BUS-125DCA"], "DC supply chain")
    add_chain(edges, ["INV-UPS-A", "BUS-125DCA"], "DC/UPS connection")
    add_chain(edges, ["BUS-480-C", "RECT-125B"], "solid AC rectifier feed")
    add_chain(edges, ["BAT-125B", "CHGR-125B", "RECT-125B", "BUS-125DCB"], "DC supply chain")
    add_chain(edges, ["INV-UPS-B", "BUS-125DCB"], "DC/UPS connection")
    add_chain(edges, ["BUS-125DCA", "CP-RPS-A", "TB-RPS-A", "PROT-UV-A", "RELAY-K101"], "dashed control/protection")
    add_chain(edges, ["RELAY-K101", "PT-410A"], "instrument signal")
    add_chain(edges, ["RELAY-K101", "LT-512A"], "instrument signal")
    add_chain(edges, ["CP-RPS-A", "RELAY-K102", "TT-303A"], "instrument/control")
    add_chain(edges, ["RELAY-K102", "GND-CTRL-A"], "ground/control lead")
    add_chain(edges, ["BUS-125DCA", "CP-RPS-B", "TB-RPS-B", "PROT-UV-B", "RELAY-K103"], "dashed control/protection")
    add_chain(edges, ["RELAY-K103", "PT-410B"], "instrument signal")
    add_chain(edges, ["RELAY-K103", "LT-512B"], "instrument signal")
    add_chain(edges, ["CP-RPS-B", "RELAY-K104", "TT-303B"], "instrument/control")
    add_chain(edges, ["RELAY-K104", "GND-CTRL-B"], "ground/control lead")
    add_chain(edges, ["BUS-125DCB", "CP-ESFAS-A", "JB-ESF-A", "PROT-LOP-A", "RELAY-K105", "FT-611A"], "ESFAS dashed control/protection")
    add_chain(edges, ["CP-ESFAS-A", "RELAY-K106", "XA-730A"], "ESFAS control/alarm")
    add_chain(edges, ["RELAY-K106", "A/B-ESF-INTERLOCK", "RELAY-K108"], "dashed A/B ESF interlock")
    add_chain(edges, ["BUS-125DCB", "CP-ESFAS-B", "JB-ESF-B", "PROT-LOP-B", "RELAY-K107", "FT-611B"], "ESFAS dashed control/protection")
    add_chain(edges, ["CP-ESFAS-B", "RELAY-K108", "XA-730B"], "ESFAS control/alarm")
    return nodes, edges


def build_jennifer_round1_edges() -> tuple[list[str], list[tuple[str, str, str]]]:
    nodes, edges = build_diego_round1_edges()
    nodes = [node for node in nodes if node != "A/B-ESF-INTERLOCK"]
    filtered: list[tuple[str, str, str]] = []
    for a, b, evidence in edges:
        if "A/B-ESF-INTERLOCK" in (a, b):
            continue
        filtered.append((a, b, evidence))
    filtered.append(("RELAY-K106", "RELAY-K108", "dashed control-interlock labeled A/B ESF INTERLOCK"))
    return nodes, filtered


def dedupe_edges(edges: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[tuple[str, str, str]] = []
    for a, b, evidence in edges:
        key = tuple(sorted((a, b)))
        if key not in seen:
            seen.add(key)
            deduped.append((a, b, evidence))
    return deduped


def write_matrix(prefix: str, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edges = dedupe_edges(edges)
    index = {node: i for i, node in enumerate(nodes)}
    missing = sorted({x for edge in edges for x in edge[:2] if x not in index})
    if missing:
        raise ValueError(f"{prefix}: edge references missing nodes: {missing}")
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b, _ in edges:
        if a == b:
            continue
        i, j = index[a], index[b]
        matrix[i][j] = 1
        matrix[j][i] = 1

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
        writer.writerow(["idx", "label", "ones_columns"])
        for row_i, node in enumerate(nodes):
            ones = [f"{col_i + 1:03d}" for col_i, value in enumerate(matrix[row_i]) if value]
            writer.writerow([f"{row_i + 1:03d}", node, " ".join(ones)])


def estimate_text_tokens(text: str) -> int:
    if tiktoken is not None:
        try:
            enc = tiktoken.get_encoding("o200k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    return max(1, round(len(text) / 4))


def estimate_image_tokens(path: Path) -> dict[str, int | str]:
    if Image is None or not path.exists():
        return {"path": str(path), "width": 0, "height": 0, "estimated_tokens": 0}
    with Image.open(path) as im:
        w, h = im.size
    # Approximate OpenAI high-detail image tokenization: 85 base + 170 per 512px tile
    # after scaling to fit within 2048x2048 and shortest side 768.
    scale = min(2048 / max(w, h), 1.0)
    sw, sh = int(round(w * scale)), int(round(h * scale))
    if min(sw, sh) > 768:
        scale2 = 768 / min(sw, sh)
        sw, sh = int(round(sw * scale2)), int(round(sh * scale2))
    tiles = ((sw + 511) // 512) * ((sh + 511) // 512)
    return {
        "path": str(path),
        "width": w,
        "height": h,
        "scaled_width": sw,
        "scaled_height": sh,
        "tiles_512": tiles,
        "estimated_tokens": 85 + 170 * tiles,
    }


def write_notes_and_usage(final_nodes: list[str], final_edges: list[tuple[str, str, str]]) -> None:
    diego_round1_summary = """Diego R1 high-recall proposal:
- 201 nodes.
- Included all AC supply, 13.8 kV/4.16 kV ties, four 480 VAC load centers, 24 feeder chains, DC supply/conversion, RPS/ESFAS control and instrumentation.
- Modeled A/B-ESF-INTERLOCK as a node between RELAY-K106 and RELAY-K108.
- Omitted unlabeled source terminal squares and bus tick marks as nodes.
"""
    jennifer_round1_summary = """Jennifer R1 precision review:
- Accepted Diego's graph with one structural correction.
- Removed A/B-ESF-INTERLOCK as a component node because it is a label on the dashed interlock wire.
- Added direct RELAY-K106 -- RELAY-K108 edge labeled A/B ESF INTERLOCK.
- Kept collapsed source-to-breaker edges through omitted unlabeled terminal squares.
- Clarified style of CS-to-MOV/HTR branches as dashed control/interlock.
"""
    diego_round2_summary = """Diego R2 saturation check:
- Accepted Jennifer's correction with no remaining visually supported objection.
- Confirmed final graph is Diego R1 with A/B-ESF-INTERLOCK removed as a node and RELAY-K106 -- RELAY-K108 added directly.
- Confirmed final count: 200 nodes, 202 undirected edges.
"""
    jennifer_round2_summary = """Jennifer R2 saturation check:
- No final objections or corrections.
- Confirmed the Diego/Jennifer workflow saturated.
- Confirmed collapsed GEN/DG source-to-breaker edges and rectifier feeds remain accepted.
"""
    final_summary = f"""Final connectivity summary:
- Document: {DOC}
- Final nodes: {len(final_nodes)}
- Final undirected edges: {len(dedupe_edges(final_edges))}
- Matrix is symmetric with diagonal zero.
- Unlabeled terminal squares beside GEN-M1, DG-1A, and DG-1B are omitted as unlabeled symbols; source-to-breaker links are collapsed.
- Crossings without junction dots are not represented as connections.
"""
    (RESULTS / "round_notes.md").write_text(
        "\n".join(
            [
                "# Document 20 Multi-Agent Rounds",
                "",
                diego_round1_summary,
                jennifer_round1_summary,
                diego_round2_summary,
                jennifer_round2_summary,
                final_summary,
            ]
        ),
        encoding="utf-8",
    )

    prompt_text = """
Main prompt: extract connectivity matrix from document 20 raw schematic using Raw + wires only; deploy Diego and Jennifer; save all rounds and token estimates.
Diego R1 prompt: high-recall visual connectivity extraction with raw/overlay/crop images.
Jennifer R1 prompt: precision review of Diego proposal with raw/overlay/crop images.
Diego R2 prompt: saturation check after Jennifer correction.
Jennifer R2 prompt: final saturation confirmation.
"""
    image_inputs_round_heavy = [
        CROPS / "raw__overview.png",
        CROPS / "raw__top_band_2x.png",
        CROPS / "raw__middle_band_2x.png",
        CROPS / "raw__bottom_band_2x.png",
        CROPS / "raw__grid_r1c1_2x.png",
        CROPS / "raw__grid_r1c2_2x.png",
        CROPS / "raw__grid_r1c3_2x.png",
        CROPS / "raw__grid_r2c1_2x.png",
        CROPS / "raw__grid_r2c2_2x.png",
        CROPS / "raw__grid_r2c3_2x.png",
        CROPS / "raw__grid_r3c1_2x.png",
        CROPS / "raw__grid_r3c2_2x.png",
        CROPS / "raw__grid_r3c3_2x.png",
        CROPS / "wires_overlay__working_area.png",
        CROPS / "wires_overlay__middle_band_2x.png",
        CROPS / "wires_overlay__bottom_band_2x.png",
    ]
    image_estimates = [estimate_image_tokens(p) for p in image_inputs_round_heavy]
    image_total = sum(int(x["estimated_tokens"]) for x in image_estimates)

    calls = [
        {
            "document": DOC,
            "iteration": 1,
            "call": "main-agent orchestration",
            "model": "Codex GPT-5",
            "status": "actual usage unavailable",
            "input_tokens_est": estimate_text_tokens(prompt_text),
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 1200,
            "output_tokens_est_expected": 2500,
            "output_tokens_est_high": 4500,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
            "total_expected_est": estimate_text_tokens(prompt_text) + 2500,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Diego R1 high-recall extractor",
            "model": "gpt-5.5",
            "status": "subagent response usage object unavailable to main agent",
            "input_tokens_est": estimate_text_tokens(prompt_text),
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 7000,
            "output_tokens_est_expected": 12000,
            "output_tokens_est_high": 18000,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": image_total,
            "total_expected_est": estimate_text_tokens(prompt_text) + image_total + 12000,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Jennifer R1 precision reviewer",
            "model": "gpt-5.5",
            "status": "subagent response usage object unavailable to main agent",
            "input_tokens_est": estimate_text_tokens(prompt_text) + 6500,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 700,
            "output_tokens_est_expected": 1500,
            "output_tokens_est_high": 3500,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": image_total,
            "total_expected_est": estimate_text_tokens(prompt_text) + 6500 + image_total + 1500,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Diego R2 saturation response",
            "model": "gpt-5.5",
            "status": "subagent response usage object unavailable to main agent",
            "input_tokens_est": 650,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 150,
            "output_tokens_est_expected": 350,
            "output_tokens_est_high": 900,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
            "total_expected_est": 1000,
        },
        {
            "document": DOC,
            "iteration": 1,
            "call": "Jennifer R2 final confirmation",
            "model": "gpt-5.5",
            "status": "subagent response usage object unavailable to main agent",
            "input_tokens_est": 650,
            "cached_input_tokens": "unavailable",
            "output_tokens_est_low": 100,
            "output_tokens_est_expected": 250,
            "output_tokens_est_high": 800,
            "reasoning_tokens": "unavailable",
            "image_file_tokens_est": 0,
            "total_expected_est": 900,
        },
    ]
    usage = {
        "method": "No OPENAI_API_KEY was present, so Responses token counting endpoint could not be called. Text estimates use tiktoken o200k_base when available. Image/file estimates use the documented high-detail 512px-tile heuristic: 85 base + 170 per tile after scaling.",
        "image_inputs_heavy_round": image_estimates,
        "calls": calls,
        "total_expected_est": sum(int(call["total_expected_est"]) for call in calls),
        "total_low_est": sum(
            int(call["input_tokens_est"])
            + int(call["image_file_tokens_est"])
            + int(call["output_tokens_est_low"])
            for call in calls
        ),
        "total_high_est": sum(
            int(call["input_tokens_est"])
            + int(call["image_file_tokens_est"])
            + int(call["output_tokens_est_high"])
            for call in calls
        ),
    }
    (RESULTS / "token_usage_estimate.json").write_text(json.dumps(usage, indent=2), encoding="utf-8")

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
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
            "total_expected_est",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(calls)

    md_lines = [
        "# Document 20 Token Usage Estimate",
        "",
        "No `OPENAI_API_KEY` or `OPENAI_BASE_URL` was present in the shell, so the OpenAI Responses input-token counting endpoint and actual response usage objects were not available.",
        "Text token estimates use `tiktoken` with `o200k_base`; image/file token estimates use the high-detail 512px tile heuristic.",
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
            f"Expected total estimate: {usage['total_expected_est']}",
            f"Low estimate: {usage['total_low_est']}",
            f"High estimate: {usage['total_high_est']}",
        ]
    )
    (RESULTS / "token_usage_estimate.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def write_manifest(final_nodes: list[str], final_edges: list[tuple[str, str, str]]) -> None:
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
        "final_nodes": len(final_nodes),
        "final_edges": len(dedupe_edges(final_edges)),
        "final_matrix": str(RESULTS / "final_connectivity_matrix.csv"),
    }
    (RESULTS / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def copy_code_artifacts() -> None:
    here = Path(__file__).resolve()
    target = CODES / here.name
    if here != target:
        shutil.copy2(here, target)
    crop_script = Path("doc20_make_visual_crops.py").resolve()
    if crop_script.exists():
        shutil.copy2(crop_script, CODES / crop_script.name)


def main() -> None:
    ensure_dirs()
    diego_nodes, diego_edges = build_diego_round1_edges()
    j_nodes, j_edges = build_jennifer_round1_edges()
    write_matrix("round1_diego", diego_nodes, diego_edges)
    write_matrix("round1_jennifer", j_nodes, j_edges)
    write_matrix("round2_diego", j_nodes, j_edges)
    write_matrix("round2_jennifer", j_nodes, j_edges)
    write_matrix("final", j_nodes, j_edges)
    write_notes_and_usage(j_nodes, j_edges)
    write_manifest(j_nodes, j_edges)
    copy_code_artifacts()
    print(f"wrote {len(j_nodes)} nodes and {len(dedupe_edges(j_edges))} edges to {RESULTS}")


if __name__ == "__main__":
    main()
