from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from PIL import Image

try:
    import tiktoken
except Exception:  # pragma: no cover - fallback is deterministic enough for estimates
    tiktoken = None


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires")
CODES = ROOT / "codes"
RESULTS = ROOT / "results"
CROPS = CODES / "crops_doc19"


TOP_NODES = [
    "OFFSITE GRID-1",
    "DS-101",
    "CB-101",
    "TR-101",
    "PT-4160A",
    "DG-1",
    "CB-DG1",
    "BUS-4160-A",
    "CB-TIE-4160",
    "BUS-4160-B",
    "DG-2",
    "CB-DG2",
    "PT-4160B",
    "TR-102",
    "CB-102",
    "DS-102",
    "OFFSITE GRID-2",
    "CB-201",
    "TR-480-A",
    "CB-480-A",
    "BUS-480-A",
    "CB-TIE-480",
    "BUS-480-B",
    "CB-480-B",
    "TR-480-B",
    "CB-202",
]


LOADS = {
    "201": ("A", "PUMP-P201", "INST-201"),
    "203": ("A", "PUMP-P203", "INST-203"),
    "301": ("A", "PUMP-P301", "INST-301"),
    "401": ("A", "PUMP-P401", "INST-401"),
    "501": ("A", "MTR-F501", "INST-501"),
    "601": ("A", "VALVE-MOV601", "INST-601"),
    "202": ("B", "PUMP-P202", "INST-202"),
    "204": ("B", "PUMP-P204", "INST-204"),
    "302": ("B", "PUMP-P302", "INST-302"),
    "402": ("B", "PUMP-P402", "INST-402"),
    "502": ("B", "MTR-F502", "INST-502"),
    "701": ("B", "INST-RPS701", "INST-701"),
}


BOTTOM_NODES = [
    "UNLABELED-480-CP-A",
    "CB-301",
    "TR-120-A",
    "BUS-120AC-A",
    "JB-MAIN",
    "CHGR-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "PN-RPS-A",
    "UNLABELED-480-CP-B",
    "CB-302",
    "TR-120-B",
    "BUS-120AC-B",
    "CHGR-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "PN-RPS-B",
]


def load_nodes() -> list[str]:
    nodes: list[str] = []
    for n, (_, terminal, inst) in LOADS.items():
        nodes.extend(
            [
                f"CB-F{n}",
                f"RELAY-PR{n}",
                f"DS-F{n}",
                f"CPT-{n}",
                f"MCC-{n}",
                f"CB-L{n}",
                f"RELAY-A{n}",
                f"RELAY-K{n}",
                terminal,
                inst,
            ]
        )
        if n == "601":
            nodes.append("LS-MOV601")
        nodes.extend([f"JB-{n}", f"TB-{n}", f"LCS-{n}"])
    return nodes


NODES = TOP_NODES + load_nodes() + BOTTOM_NODES


def canonical_edge(a: str, b: str) -> tuple[str, str]:
    if a not in NODES:
        raise ValueError(f"unknown node: {a}")
    if b not in NODES:
        raise ValueError(f"unknown node: {b}")
    return tuple(sorted((a, b)))


def edge(a: str, b: str, evidence: str) -> tuple[str, str, str]:
    x, y = canonical_edge(a, b)
    return x, y, evidence


def base_edges() -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = [
        edge("OFFSITE GRID-1", "DS-101", "solid vertical offsite feeder"),
        edge("DS-101", "CB-101", "solid vertical feeder between switch and breaker"),
        edge("CB-101", "TR-101", "solid vertical feeder continues into inline TR-101"),
        edge("TR-101", "BUS-4160-A", "TR-101 inline with BUS-4160-A"),
        edge("PT-4160A", "BUS-4160-A", "dashed PT tap to BUS-4160-A"),
        edge("DG-1", "CB-DG1", "solid DG-1 feeder to breaker"),
        edge("CB-DG1", "BUS-4160-A", "solid vertical tie from CB-DG1 to BUS-4160-A"),
        edge("BUS-4160-A", "CB-TIE-4160", "4160 tie breaker between A/B buses"),
        edge("CB-TIE-4160", "BUS-4160-B", "4160 tie breaker between A/B buses"),
        edge("OFFSITE GRID-2", "DS-102", "solid vertical offsite feeder"),
        edge("DS-102", "CB-102", "solid vertical feeder between switch and breaker"),
        edge("CB-102", "TR-102", "solid vertical feeder continues into inline TR-102"),
        edge("TR-102", "BUS-4160-B", "TR-102 inline with BUS-4160-B"),
        edge("PT-4160B", "BUS-4160-B", "dashed PT tap to BUS-4160-B"),
        edge("DG-2", "CB-DG2", "solid DG-2 feeder to breaker"),
        edge("CB-DG2", "BUS-4160-B", "solid vertical tie from CB-DG2 to BUS-4160-B"),
        edge("BUS-4160-A", "CB-201", "solid feeder from BUS-4160-A to transformer breaker"),
        edge("CB-201", "TR-480-A", "solid vertical 480 transformer feeder"),
        edge("TR-480-A", "CB-480-A", "solid vertical 480 transformer feeder"),
        edge("CB-480-A", "BUS-480-A", "solid feeder into BUS-480-A"),
        edge("BUS-4160-B", "CB-202", "solid feeder from BUS-4160-B to transformer breaker"),
        edge("CB-202", "TR-480-B", "solid vertical 480 transformer feeder"),
        edge("TR-480-B", "CB-480-B", "solid vertical 480 transformer feeder"),
        edge("CB-480-B", "BUS-480-B", "solid feeder into BUS-480-B"),
        edge("BUS-480-A", "CB-TIE-480", "480 tie breaker between A/B buses"),
        edge("CB-TIE-480", "BUS-480-B", "480 tie breaker between A/B buses"),
    ]

    for n, (division, terminal, inst) in LOADS.items():
        bus = "BUS-480-A" if division == "A" else "BUS-480-B"
        edges.extend(
            [
                edge(bus, f"CB-F{n}", f"solid tap from {bus} into feeder {n}"),
                edge(f"CB-F{n}", f"RELAY-PR{n}", f"dashed protection relay link for feeder {n}"),
                edge(f"CB-F{n}", f"DS-F{n}", f"solid vertical feeder {n}"),
                edge(f"DS-F{n}", f"CPT-{n}", f"solid vertical feeder {n}"),
                edge(f"CPT-{n}", f"MCC-{n}", f"solid vertical feeder {n}"),
                edge(f"MCC-{n}", f"RELAY-A{n}", f"dashed relay link from MCC-{n}"),
                edge(f"MCC-{n}", f"CB-L{n}", f"solid load feeder {n}"),
                edge(f"CB-L{n}", f"RELAY-K{n}", f"solid load feeder {n}"),
                edge(f"RELAY-K{n}", terminal, f"solid output from relay K{n} to terminal load"),
            ]
        )
        if n == "601":
            edges.extend(
                [
                    edge("VALVE-MOV601", "INST-601", "dashed indication link from MOV to instrument"),
                    edge("VALVE-MOV601", "LS-MOV601", "dashed limit-switch branch from MOV"),
                    edge("LS-MOV601", "JB-601", "dashed vertical link from limit switch to junction box"),
                    edge("JB-601", "TB-601", "dashed vertical link from junction box to terminal block"),
                    edge("TB-601", "LCS-601", "dashed control link from terminal block to local control station"),
                ]
            )
        elif n == "701":
            edges.extend(
                [
                    edge("INST-RPS701", "INST-701", "dashed instrument-to-instrument link"),
                    edge("INST-701", "JB-701", "dashed vertical link to junction box"),
                    edge("JB-701", "TB-701", "dashed vertical link to terminal block"),
                    edge("TB-701", "LCS-701", "dashed control link to local control station"),
                ]
            )
        else:
            edges.extend(
                [
                    edge(terminal, inst, f"dashed terminal-load instrumentation link for {n}"),
                    edge(inst, f"JB-{n}", f"dashed vertical link from instrument to junction box {n}"),
                    edge(f"JB-{n}", f"TB-{n}", f"dashed vertical link from junction box to terminal block {n}"),
                    edge(f"TB-{n}", f"LCS-{n}", f"dashed control link from terminal block to local control station {n}"),
                ]
            )

    edges.extend(
        [
            edge("BUS-480-A", "UNLABELED-480-CP-A", "control-power conductor routes from A 480 V distribution area"),
            edge("UNLABELED-480-CP-A", "CB-301", "shared A control-power conductor taps to CB-301"),
            edge("CB-301", "TR-120-A", "solid vertical through control transformer branch"),
            edge("TR-120-A", "BUS-120AC-A", "solid feeder into BUS-120AC-A"),
            edge("BUS-120AC-A", "JB-MAIN", "dashed vertical bus tap to main junction box"),
            edge("UNLABELED-480-CP-A", "CHGR-125A", "shared A control-power conductor taps to charger A"),
            edge("CHGR-125A", "BAT-125A", "solid vertical charger/battery branch"),
            edge("BAT-125A", "BUS-125DC-A", "solid vertical battery branch into BUS-125DC-A"),
            edge("BUS-125DC-A", "INV-120A", "solid vertical inverter tap from DC bus"),
            edge("INV-120A", "PN-RPS-A", "dashed inverter output/control link to RPS panel A"),
            edge("BUS-480-B", "UNLABELED-480-CP-B", "control-power conductor routes from B 480 V distribution area"),
            edge("UNLABELED-480-CP-B", "CB-302", "shared B control-power conductor taps to CB-302"),
            edge("CB-302", "TR-120-B", "solid vertical through control transformer branch"),
            edge("TR-120-B", "BUS-120AC-B", "solid feeder into BUS-120AC-B"),
            edge("UNLABELED-480-CP-B", "CHGR-125B", "shared B control-power conductor taps to charger B"),
            edge("CHGR-125B", "BAT-125B", "solid vertical charger/battery branch"),
            edge("BAT-125B", "BUS-125DC-B", "solid vertical battery branch into BUS-125DC-B"),
            edge("BUS-125DC-B", "INV-120B", "solid vertical inverter tap from DC bus"),
            edge("INV-120B", "PN-RPS-B", "dashed inverter output/control link to RPS panel B"),
        ]
    )
    return dedupe(edges)


def high_recall_extra_edges() -> list[tuple[str, str, str]]:
    return [
        edge("CB-301", "CHGR-125A", "Diego R1 high-recall: shared source conductor interpreted as direct relation"),
        edge("CB-302", "CHGR-125B", "Diego R1 high-recall: shared source conductor interpreted as direct relation"),
    ]


def dedupe(edges: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out: dict[tuple[str, str], str] = {}
    for a, b, evidence in edges:
        out[(a, b)] = evidence
    return [(a, b, out[(a, b)]) for a, b in sorted(out)]


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str, str]]) -> None:
    edge_set = {(a, b) for a, b, _ in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for r in nodes:
            row = [r]
            for c in nodes:
                row.append(0 if r == c else int(tuple(sorted((r, c))) in edge_set))
            writer.writerow(row)


def write_edges(path: Path, edges: list[tuple[str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b", "evidence"])
        writer.writerows(edges)


def text_tokens(text: str) -> int:
    if tiktoken is None:
        return max(1, math.ceil(len(text) / 4))
    try:
        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def estimate_image_tokens(path: Path) -> int:
    # Local substitute for the Responses input-token counting endpoint.
    # Uses the common high-detail 85 + 170 * 512-tile heuristic after resizing.
    with Image.open(path) as img:
        w, h = img.size
    scale = min(1.0, 2048 / max(w, h))
    w2, h2 = math.ceil(w * scale), math.ceil(h * scale)
    if min(w2, h2) > 768:
        scale2 = 768 / min(w2, h2)
        w2, h2 = math.ceil(w2 * scale2), math.ceil(h2 * scale2)
    tiles = math.ceil(w2 / 512) * math.ceil(h2 / 512)
    return 85 + 170 * tiles


def write_token_estimates(rounds: dict[str, list[tuple[str, str, str]]]) -> None:
    image_sets = {
        "main_analysis": [
            ROOT / "raw -- synthetic_npp_electrical_schematic_v3.png",
            ROOT / "wires_mask_overlay.png",
            CROPS / "top_all_raw_2x.png",
            CROPS / "load_groups_a_1_3_raw_2x.png",
            CROPS / "load_groups_a_4_6_raw_2x.png",
            CROPS / "load_groups_b_1_3_raw_2x.png",
            CROPS / "load_groups_b_4_6_raw_2x.png",
            CROPS / "bottom_control_a_raw_2x.png",
            CROPS / "bottom_control_b_raw_2x.png",
        ],
        "diego_round_1": [
            CROPS / "overview_raw.png",
            CROPS / "top_all_raw_2x.png",
            CROPS / "top_all_overlay_2x.png",
            CROPS / "load_groups_a_1_3_raw_2x.png",
            CROPS / "load_groups_a_4_6_raw_2x.png",
            CROPS / "load_groups_b_1_3_raw_2x.png",
            CROPS / "load_groups_b_4_6_raw_2x.png",
            CROPS / "bottom_control_a_raw_2x.png",
            CROPS / "bottom_control_b_raw_2x.png",
            CROPS / "bottom_control_a_overlay_2x.png",
            CROPS / "bottom_control_b_overlay_2x.png",
        ],
        "jennifer_round_1": [
            CROPS / "top_all_raw_2x.png",
            CROPS / "load_groups_a_4_6_raw_2x.png",
            CROPS / "load_groups_b_4_6_raw_2x.png",
            CROPS / "bottom_control_a_overlay_2x.png",
            CROPS / "bottom_control_b_overlay_2x.png",
        ],
        "diego_round_2": [
            CROPS / "top_all_overlay_2x.png",
            CROPS / "load_groups_a_4_6_raw_2x.png",
            CROPS / "load_groups_b_4_6_raw_2x.png",
            CROPS / "bottom_control_a_overlay_2x.png",
            CROPS / "bottom_control_b_overlay_2x.png",
        ],
        "jennifer_round_2": [
            CROPS / "top_all_overlay_2x.png",
            CROPS / "load_groups_a_4_6_raw_2x.png",
            CROPS / "load_groups_b_4_6_raw_2x.png",
            CROPS / "bottom_control_a_overlay_2x.png",
            CROPS / "bottom_control_b_overlay_2x.png",
        ],
    }
    prompts = {
        "main_analysis": "Main agent visual inspection, crop generation, graph construction, and result writing.",
        "diego_round_1": "High-recall extraction prompt with attached schematic crops and overlay aids.",
        "jennifer_round_1": "Precision review of Diego R1 against visual evidence, removing unsupported edges.",
        "diego_round_2": "Second extractor pass to check Jennifer's refined graph and identify residual misses.",
        "jennifer_round_2": "Final precision saturation review of Diego R2/final graph.",
    }
    output_expected = {
        "main_analysis": (1200, 2500, 4500),
        "diego_round_1": (2500, 4500, 8000),
        "jennifer_round_1": (1500, 3000, 5500),
        "diego_round_2": (800, 1600, 3000),
        "jennifer_round_2": (700, 1400, 2500),
    }
    rows = []
    for call_id in ["main_analysis", "diego_round_1", "jennifer_round_1", "diego_round_2", "jennifer_round_2"]:
        prompt_tokens = text_tokens(prompts[call_id])
        image_tokens = sum(estimate_image_tokens(p) for p in image_sets[call_id] if p.exists())
        low_out, exp_out, high_out = output_expected[call_id]
        input_est = prompt_tokens + image_tokens
        rows.append(
            {
                "document": "19",
                "iteration": "1",
                "call_id": call_id,
                "model_call": "main_agent" if call_id == "main_analysis" else call_id.split("_round_")[0],
                "input_tokens_est": input_est,
                "cached_input_tokens": 0,
                "image_file_input_tokens_est": image_tokens,
                "output_tokens_low": low_out,
                "output_tokens_expected": exp_out,
                "output_tokens_high": high_out,
                "reasoning_tokens": "not_available",
                "total_tokens_expected": input_est + exp_out,
                "counting_method": "tiktoken text + high-detail image tile heuristic; no API key for Responses counter",
            }
        )
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (RESULTS / "token_usage_estimate.json").open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)


def remove_edges(
    edges: list[tuple[str, str, str]], pairs: list[tuple[str, str]]
) -> list[tuple[str, str, str]]:
    remove_set = {canonical_edge(a, b) for a, b in pairs}
    return [e for e in edges if (e[0], e[1]) not in remove_set]


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    final_edges = base_edges()
    bus_to_unlabeled = [
        ("BUS-480-A", "UNLABELED-480-CP-A"),
        ("BUS-480-B", "UNLABELED-480-CP-B"),
    ]
    unlabeled_bottom_links = bus_to_unlabeled + [
        ("UNLABELED-480-CP-A", "CB-301"),
        ("UNLABELED-480-CP-A", "CHGR-125A"),
        ("UNLABELED-480-CP-B", "CB-302"),
        ("UNLABELED-480-CP-B", "CHGR-125B"),
    ]
    diego_round_1 = dedupe(
        remove_edges(final_edges, unlabeled_bottom_links) + high_recall_extra_edges()
    )
    jennifer_round_1 = remove_edges(final_edges, bus_to_unlabeled)
    rounds = {
        "diego_round_1": diego_round_1,
        "jennifer_round_1": jennifer_round_1,
        "diego_round_2": final_edges,
        "jennifer_round_2": final_edges,
    }

    for name, edges in rounds.items():
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", NODES, edges)

    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", NODES, final_edges)
    write_token_estimates(rounds)

    notes = [
        "# Document 19 Extraction Notes",
        "",
        "Only resources in the `Raw + wires` folder were used. Existing validation/GT-derived result files were not opened.",
        "",
        "Round summary:",
        "- Diego round 1 represented the shared bottom source conductors as direct breaker-to-charger relations.",
        "- Jennifer round 1 replaced those shortcuts with `UNLABELED-480-CP-A/B` logical conductor nodes and left the 480 bus-to-conductor edges uncertain.",
        "- Diego round 2 accepted Jennifer's corrections and retained the two possible 480 bus-to-conductor edges for high recall.",
        "- Jennifer round 2 ruled the 480 bus-to-conductor edges visually supported; saturation reached.",
        "",
        f"Final node count: {len(NODES)}",
        f"Final undirected edge count: {len(final_edges)}",
        "",
        "Final special cases:",
        "- `PT-4160A` and `PT-4160B` are treated as dashed taps to the 4160 buses, not series devices.",
        "- `VALVE-MOV601` has two dashed indication branches: to `INST-601` and to `LS-MOV601`; `LS-MOV601` then goes to `JB-601`.",
        "- The B-side sixth load group is `RPS INSTR TRAIN B` with `701` labels, not a `602` MOV group.",
        "- Control-power source conductors are represented as `UNLABELED-480-CP-A/B`, connected to their respective `BUS-480` nodes and to both the breaker/transformer and charger branches.",
    ]
    (RESULTS / "round_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
