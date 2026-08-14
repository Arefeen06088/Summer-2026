from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\7")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_1"

BUS_NODES = [
    "BUS-13A",
    "BUS-13B",
    "BUS-4A",
    "BUS-4B",
    "LC-480A",
    "LC-480B",
    "LC-480C",
    "LC-480D",
    "BUS-125DCA",
    "BUS-125DCB",
]


def read_component_nodes() -> list[str]:
    with (INPUT / "component_visual_ocr_labels.csv").open(newline="", encoding="utf-8-sig") as f:
        return [row["final_label"].strip() for row in csv.DictReader(f)]


def normalize_edge(source: str, target: str) -> tuple[str, str]:
    if source == target:
        raise ValueError(f"self edge is not allowed: {source}")
    return tuple(sorted((source, target)))


def edge(
    source: str,
    target: str,
    confidence: str,
    evidence: str,
    action: str,
    line_type: str = "mixed",
) -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "confidence": confidence,
        "line_type": line_type,
        "evidence": evidence,
        "review_action": action,
    }


def add_edge(
    rows: list[dict[str, str]],
    source: str,
    target: str,
    confidence: str,
    evidence: str,
    action: str,
    line_type: str = "mixed",
) -> None:
    rows.append(edge(source, target, confidence, evidence, action, line_type))


def add_chain(
    rows: list[dict[str, str]],
    labels: list[str],
    confidence: str,
    evidence: str,
    action: str,
    line_type: str,
) -> None:
    for source, target in zip(labels, labels[1:]):
        add_edge(rows, source, target, confidence, evidence, action, line_type)


def write_matrix(path: Path, nodes: list[str], edge_rows: list[dict[str, str]]) -> None:
    edge_set = {normalize_edge(row["source"], row["target"]) for row in edge_rows}
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for source in nodes:
            writer.writerow(
                [source]
                + [
                    "0" if source == target else ("1" if normalize_edge(source, target) in edge_set else "0")
                    for target in nodes
                ]
            )


def write_edges(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["source", "target", "confidence", "line_type", "evidence", "review_action"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_notes(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["item", "decision", "evidence", "uncertainty"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def dedupe(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        key = normalize_edge(row["source"], row["target"])
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def common_distribution_edges(action: str, include_ds_sat_b: bool = False) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    solid = "solid conductor in raw schematic; supported by component/logical overlay."
    add_chain(rows, ["GEN-G01", "ISO-GEN-1", "CB-GEN-A", "BUS-13A"], "high", solid, action, "solid")
    add_chain(rows, ["BUS-13A", "CB-TIE-13", "BUS-13B"], "high", solid, action, "solid")
    add_chain(rows, ["BUS-13A", "CB-UAT-A", "TR-UAT-A", "BUS-4A"], "high", solid, action, "solid")
    add_chain(rows, ["BUS-13B", "CB-UAT-B", "TR-UAT-B", "BUS-4B"], "high", solid, action, "solid")

    add_chain(rows, ["OFFSITE-345", "DS-SAT-1", "TR-SAT-A", "CB-SAT-A", "BUS-4A"], "high", solid, action, "solid")
    if include_ds_sat_b:
        add_edge(
            rows,
            "DS-SAT-1",
            "TR-SAT-B",
            "high",
            "SAT zooms show the DS-SAT-1 top/downstream terminal tying into the long upper solid feeder that drops to TR-SAT-B.",
            action,
            "solid",
        )
    add_chain(rows, ["TR-SAT-B", "CB-SAT-B", "BUS-4B"], "high", solid, action, "solid")

    add_chain(rows, ["DG-1A", "CB-DG-A", "BUS-4A"], "high", solid, action, "solid")
    add_chain(rows, ["DG-1B", "CB-DG-B", "BUS-4B"], "high", solid, action, "solid")
    add_chain(rows, ["BUS-4A", "CB-TIE-4", "BUS-4B"], "high", solid, action, "solid")

    for bus, breaker, transformer, lc in [
        ("BUS-4A", "CB-480A", "TR-480A", "LC-480A"),
        ("BUS-4A", "CB-480B", "TR-480B", "LC-480B"),
        ("BUS-4B", "CB-480C", "TR-480C", "LC-480C"),
        ("BUS-4B", "CB-480D", "TR-480D", "LC-480D"),
    ]:
        add_chain(rows, [bus, breaker, transformer, lc], "high", solid, action, "solid")

    for lc, breaker, mcc in [
        ("LC-480A", "CB-MCC-A1", "MCC-A1"),
        ("LC-480A", "CB-MCC-A2", "MCC-A2"),
        ("LC-480B", "CB-MCC-B1", "MCC-B1"),
        ("LC-480B", "CB-MCC-B2", "MCC-B2"),
        ("LC-480C", "CB-MCC-C1", "MCC-C1"),
        ("LC-480C", "CB-MCC-C2", "MCC-C2"),
        ("LC-480D", "CB-MCC-D1", "MCC-D1"),
        ("LC-480D", "CB-MCC-D2", "MCC-D2"),
    ]:
        add_chain(rows, [lc, breaker, mcc], "high", solid, action, "solid")

    load_groups = [
        ("MCC-A1", [("CB-P201A", "PUMP-P201A"), ("CB-MOV101A", "MOV-101A"), ("CB-FAN101A", "FAN-F101A")]),
        ("MCC-A2", [("CB-P202A", "PUMP-P202A"), ("CB-MOV102A", "MOV-102A"), ("CB-HTR101A", "HTR-H101A")]),
        ("MCC-B1", [("CB-P201B", "PUMP-P201B"), ("CB-MOV101B", "MOV-101B"), ("CB-FAN101B", "FAN-F101B")]),
        ("MCC-B2", [("CB-P202B", "PUMP-P202B"), ("CB-MOV102B", "MOV-102B"), ("CB-HTR101B", "HTR-H101B")]),
        ("MCC-C1", [("CB-P301A", "PUMP-P301A"), ("CB-MOV201A", "MOV-201A"), ("CB-FAN201A", "FAN-F201A")]),
        ("MCC-C2", [("CB-P302A", "PUMP-P302A"), ("CB-MOV202A", "MOV-202A"), ("CB-HTR201A", "HTR-H201A")]),
        ("MCC-D1", [("CB-P301B", "PUMP-P301B"), ("CB-MOV201B", "MOV-201B"), ("CB-FAN201B", "FAN-F201B")]),
        ("MCC-D2", [("CB-P302B", "PUMP-P302B"), ("CB-MOV202B", "MOV-202B"), ("CB-HTR201B", "HTR-H201B")]),
    ]
    for mcc, loads in load_groups:
        for breaker, load in loads:
            add_chain(rows, [mcc, breaker, load], "high", solid, action, "solid")
    return rows


def jennifer_round_1_edges(action: str = "jennifer_round_1_retained") -> list[dict[str, str]]:
    rows = common_distribution_edges(action, include_ds_sat_b=False)
    dc = "Solid DC/control-power bus ties in Train A/B control-power sections."
    for source, target in [
        ("BAT-125A", "BUS-125DCA"),
        ("BAT-125A", "BCHG-125A"),
        ("BCHG-125A", "BUS-125DCA"),
        ("BUS-125DCA", "INV-120A"),
        ("BUS-125DCA", "PPS-A"),
        ("BAT-125B", "BUS-125DCB"),
        ("BCHG-125B", "BUS-125DCB"),
        ("BUS-125DCB", "INV-120B"),
        ("BUS-125DCB", "PPS-B"),
    ]:
        add_edge(rows, source, target, "high", dc, action, "solid")

    dashed = "Direct dashed control/status line terminates on both named component terminals."
    for chain in [
        ["INV-120A", "UPS-120A", "PNL-AC-CR1", "PPS-A"],
        ["INV-120B", "UPS-120B", "PNL-AC-CR2", "PPS-B"],
    ]:
        add_chain(rows, chain, "high", dashed, action, "dashed")
    for source, target in [
        ("ANN-101", "RELAY-K101"),
        ("RELAY-K101", "RELAY-K102"),
        ("PPS-A", "RELAY-K102"),
        ("ANN-201", "RELAY-K201"),
        ("PPS-B", "RELAY-K202"),
    ]:
        add_edge(rows, source, target, "high", dashed, action, "dashed")
    return dedupe(rows)


def diego_round_1_edges() -> list[dict[str, str]]:
    rows = common_distribution_edges("diego_round_1_proposed", include_ds_sat_b=True)
    dc = "Diego high-recall DC/control-power interpretation from solid bus and nearby taps."
    for source, target in [
        ("BAT-125A", "BUS-125DCA"),
        ("BAT-125A", "BCHG-125A"),
        ("BCHG-125A", "BUS-125DCA"),
        ("BUS-125DCA", "INV-120A"),
        ("BUS-125DCA", "PNL-AC-CR1"),
        ("BUS-125DCA", "PPS-A"),
        ("BAT-125B", "BUS-125DCB"),
        ("BCHG-125B", "BUS-125DCB"),
        ("BUS-125DCB", "INV-120B"),
        ("BUS-125DCB", "PNL-AC-CR2"),
        ("BUS-125DCB", "PPS-B"),
    ]:
        add_edge(rows, source, target, "medium-high", dc, "diego_round_1_proposed", "mixed")

    dashed = "Diego high-recall probable dashed control edge."
    for chain in [
        ["INV-120A", "UPS-120A", "PNL-AC-CR1", "PPS-A"],
        ["INV-120B", "UPS-120B", "PNL-AC-CR2", "PPS-B"],
    ]:
        add_chain(rows, chain, "medium-high", dashed, "diego_round_1_proposed", "dashed")
    for source, target in [
        ("ANN-101", "RELAY-K101"),
        ("RELAY-K101", "RELAY-K102"),
        ("PPS-A", "RELAY-K102"),
        ("ANN-201", "RELAY-K201"),
        ("RELAY-K201", "RELAY-K202"),
        ("PPS-B", "RELAY-K202"),
    ]:
        add_edge(rows, source, target, "medium-high", dashed, "diego_round_1_proposed", "dashed")
    return dedupe(rows)


def round_2_delta(action: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    add_edge(
        rows,
        "DS-SAT-1",
        "TR-SAT-B",
        "high",
        "Long upper solid feeder leaves DS-SAT-1 downstream/top terminal and drops into TR-SAT-B.",
        action,
        "solid",
    )
    for source, target, confidence, evidence in [
        ("UPS-120A", "ANN-101", "high", "Vertical dashed line from UPS-120A bottom terminal to ANN-101 top terminal."),
        ("ANN-101", "PPS-A", "high", "Diagonal dashed line from ANN-101 terminal area to PPS-A left terminal."),
        ("PPS-A", "RELAY-K101", "high", "L-shaped dashed line from PPS-A lower-left terminal to RELAY-K101 top terminal route."),
        ("RELAY-K102", "SR-101", "high", "Horizontal dashed line exits RELAY-K102 right terminal and lands at SR-101 left terminal."),
        ("ANN-101", "SR-101", "medium-high", "ANN-101 bottom downlead joins the long lower dashed route terminating at SR-101."),
        ("UPS-120B", "ANN-201", "high", "Vertical dashed line from UPS-120B bottom terminal to ANN-201 control path."),
        ("ANN-201", "PPS-B", "high", "Long shallow diagonal dashed route from ANN-201 area to PPS-B left terminal."),
        ("PNL-AC-CR2", "RELAY-K201", "high", "Vertical dashed route from PNL-AC-CR2 down to RELAY-K201 top terminal."),
        ("PPS-B", "RELAY-K201", "high", "L-shaped dashed route from PPS-B lower-left terminal into RELAY-K201 top route."),
        ("ANN-201", "SR-101", "medium", "Lower SR dashed route appears to meet ANN-201 lower vertical control line."),
        ("SR-101", "RELAY-K202", "medium-high", "Lower SR route continues diagonally and lands at RELAY-K202 left terminal."),
    ]:
        add_edge(rows, source, target, confidence, evidence, action, "dashed")
    return rows


def final_edges(action: str = "saturated_retained") -> list[dict[str, str]]:
    rows = jennifer_round_1_edges(action)
    rows.extend(round_2_delta(action))
    return dedupe(rows)


def round_notes() -> dict[str, list[dict[str, str]]]:
    return {
        "round_01_diego": [
            {
                "item": "node_set",
                "decision": "Use 110 physical component labels plus 10 named electrical buses/load centers.",
                "evidence": "Component CSV and raw/logical overlay labels.",
                "uncertainty": "Raceways and container headings were listed but not connected as matrix nodes.",
            },
            {
                "item": "high_recall_edges",
                "decision": "Included visually plausible solid, DC, and direct dashed connections.",
                "evidence": "Raw schematic, wire overlays, and inspection crops.",
                "uncertainty": "DS-SAT-1--TR-SAT-B and several DC/dashed cases flagged for Jennifer review.",
            },
        ],
        "round_01_jennifer": [
            {
                "item": "precision_prune",
                "decision": "Removed DS-SAT-1--TR-SAT-B, BUS-125DCA--PNL-AC-CR1, BUS-125DCB--PNL-AC-CR2, and RELAY-K201--RELAY-K202.",
                "evidence": "Initial conservative raw-image review of ambiguous long feeder and dashed control routes.",
                "uncertainty": "Long dashed lower control network and SR-101 paths kept uncertain.",
            },
        ],
        "round_02_diego": [
            {
                "item": "high_recall_delta",
                "decision": "Restored DS-SAT-1--TR-SAT-B and added 11 dashed control terminal edges.",
                "evidence": "Zoomed SAT feeder crops and control crops 17-22/27-29.",
                "uncertainty": "Five remaining dashed candidates were not promoted.",
            },
        ],
        "round_02_jennifer": [
            {
                "item": "precision_acceptance",
                "decision": "Accepted all 12 Diego Round 2 additions; kept five ambiguous candidates out.",
                "evidence": "Terminal-to-terminal line landings were visible for the accepted additions.",
                "uncertainty": "Final count remains below the raw title-block edge clue because unclear dashed routes were not invented.",
            },
        ],
        "round_03_diego": [
            {
                "item": "saturation",
                "decision": "Agreed final five uncertain edges should stay out; no new confident additions.",
                "evidence": "Final review of raw control crops and annotated wire-node crops.",
                "uncertainty": "Ambiguous dashed crossings/pass-throughs remain documented but excluded.",
            },
        ],
    }


def uncertain_candidates() -> list[dict[str, str]]:
    return [
        {
            "source": "PNL-AC-CR1",
            "target": "RELAY-K101",
            "reason": "PNL downlead passes near the relay region, but final review did not find clean terminal-to-terminal landing.",
            "final_action": "excluded_uncertain",
        },
        {
            "source": "RELAY-K101",
            "target": "SR-101",
            "reason": "K101 lower lead approaches/crosses lower SR routing without clear junction evidence.",
            "final_action": "excluded_uncertain",
        },
        {
            "source": "SR-101",
            "target": "RELAY-K201",
            "reason": "SR-to-Train-B route passes near K201 but appears to land elsewhere.",
            "final_action": "excluded_uncertain",
        },
        {
            "source": "RELAY-K201",
            "target": "RELAY-K202",
            "reason": "No direct terminal-to-terminal line between relay boxes; nearby diagonal is better assigned to SR-101--RELAY-K202.",
            "final_action": "excluded_uncertain",
        },
        {
            "source": "PNL-AC-CR2",
            "target": "RELAY-K202",
            "reason": "PNL-CR2 routes to PPS-B/K201 area; K202 feed is clearer from PPS-B/SR-side routing.",
            "final_action": "excluded_uncertain",
        },
        {
            "source": "BUS-125DCA",
            "target": "PNL-AC-CR1",
            "reason": "Dashed PNL routing crosses/approaches the DC bus without a solid bus tap.",
            "final_action": "rejected",
        },
        {
            "source": "BUS-125DCB",
            "target": "PNL-AC-CR2",
            "reason": "Dashed PNL routing crosses/approaches the DC bus without a solid bus tap.",
            "final_action": "rejected",
        },
        {
            "source": "BAT-125B",
            "target": "BCHG-125B",
            "reason": "No Train B battery-to-charger horizontal connection analogous to Train A is visible.",
            "final_action": "rejected",
        },
    ]


def validate(nodes: list[str], rows: list[dict[str, str]]) -> dict[str, object]:
    node_set = set(nodes)
    edge_set = {normalize_edge(row["source"], row["target"]) for row in rows}
    invalid_edges = [
        {"source": row["source"], "target": row["target"]}
        for row in rows
        if row["source"] not in node_set or row["target"] not in node_set or row["source"] == row["target"]
    ]
    return {
        "node_count": len(nodes),
        "edge_count": len(edge_set),
        "matrix_is_symmetric_by_construction": True,
        "diagonal_all_zero": True,
        "invalid_edges": invalid_edges,
        "ground_nodes_added": [],
        "raw_title_block_note": "Raw schematic revision/status area visibly states 120 nodes / 140 edges; final keeps only visually supported unique component/bus pairs.",
        "gt_or_evaluator_feedback_used": False,
    }


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["node", "node_kind"])
        writer.writeheader()
        for node in nodes:
            kind = "electrical_bus_or_load_center" if node in BUS_NODES else "physical_component"
            writer.writerow({"node": node, "node_kind": kind})


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        fields = ["source", "target", "reason", "final_action"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(uncertain_candidates())


def write_summary(path: Path, nodes: list[str], rows: list[dict[str, str]]) -> None:
    text = f"""# Doc 7 Iteration 1 Final Connectivity Summary

Workflow: Diego high-recall extraction -> Jennifer precision review -> Diego high-recall challenge -> Jennifer precision acceptance -> Diego saturation check.

Nodes: {len(nodes)}
Edges: {len({normalize_edge(row['source'], row['target']) for row in rows})}

Node policy: 110 component/OCR labels plus ten visible named electrical buses/load centers: {', '.join(BUS_NODES)}.

Final key corrections:
- Restored DS-SAT-1--TR-SAT-B after zoom review of the long upper solid feeder.
- Rejected DC-bus-to-AC-panel taps because the panel routes are dashed/control and not solid DC bus taps.
- Added direct dashed control terminal edges for UPS/ANN/PPS/relay/SR paths where both endpoints were visually supported.
- Excluded raceways, container headings, feeder labels, and anonymous intermediate wire points.

Raw title-block sanity note: the drawing visibly says 120 nodes / 140 edges. The final matrix keeps 120 nodes and 131 visually supported unique edges; ambiguous dashed crossings/pass-throughs were documented rather than promoted.

No GT, GT-derived validation, evaluator output, or metric feedback was used during extraction.
"""
    path.write_text(text, encoding="utf-8")


def write_round(prefix: str, nodes: list[str], rows: list[dict[str, str]], notes: list[dict[str, str]]) -> None:
    write_edges(RESULTS / f"{prefix}_edges.csv", rows)
    write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, rows)
    write_notes(RESULTS / f"{prefix}_notes.csv", notes)
    with (RESULTS / f"{prefix}_validation.json").open("w", encoding="utf-8") as f:
        json.dump(validate(nodes, rows), f, indent=2)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = read_component_nodes() + BUS_NODES
    rounds = {
        "round_01_diego": diego_round_1_edges(),
        "round_01_jennifer": jennifer_round_1_edges(),
        "round_02_diego": final_edges("diego_round_2_proposed"),
        "round_02_jennifer": final_edges("jennifer_round_2_accepted"),
        "round_03_diego": final_edges("diego_round_3_saturated"),
    }
    notes = round_notes()
    for prefix, rows in rounds.items():
        write_round(prefix, nodes, rows, notes[prefix])

    final = final_edges()
    write_edges(RESULTS / "final_connectivity_edges.csv", final)
    write_edges(RESULTS / "final_edges.csv", final)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", nodes, final)
    write_nodes(RESULTS / "final_connectivity_nodes.csv", nodes)
    write_uncertain(RESULTS / "final_uncertain_candidates.csv")
    write_summary(RESULTS / "final_connectivity_summary.md", nodes, final)
    with (RESULTS / "final_connectivity_validation.json").open("w", encoding="utf-8") as f:
        json.dump(validate(nodes, final), f, indent=2)

    shutil.copy2(RESULTS / "final_connectivity_matrix.csv", RESULTS / "connectivity_matrix.csv")


if __name__ == "__main__":
    main()
