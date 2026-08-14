from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\6")
INPUT = BASE / "Input resources"
RESULTS = BASE / "Results" / "Iteration_1"

BUS_NODES = [
    "SWYD-BUS-A",
    "SWYD-BUS-B",
    "BUS-6KV-A",
    "BUS-6KV-B",
    "BUS-4KV-N",
]


def read_component_nodes() -> list[str]:
    with (INPUT / "component_visual_ocr_labels.csv").open(newline="", encoding="utf-8-sig") as f:
        return [row["final_label"].strip() for row in csv.DictReader(f)]


def normalize_edge(source: str, target: str) -> tuple[str, str]:
    if source == target:
        raise ValueError(f"self edge is not allowed: {source}")
    return tuple(sorted((source, target)))


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
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "confidence", "evidence", "review_action"])
        writer.writeheader()
        writer.writerows(rows)


def write_notes(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "decision", "evidence", "uncertainty"])
        writer.writeheader()
        writer.writerows(rows)


def edge(source: str, target: str, confidence: str, evidence: str, action: str = "diego_proposed") -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "confidence": confidence,
        "evidence": evidence,
        "review_action": action,
    }


def round_01_diego_edges() -> list[dict[str, str]]:
    rows = [
        edge("GEN-G201", "IPB-201", "high", "Solid generator conductor into isolated phase bus."),
        edge("IPB-201", "CB-GEN-201", "high", "Solid conductor from IPB-201 to generator breaker."),
        edge("CB-GEN-201", "GSU-201", "high", "Solid conductor from generator breaker to GSU primary."),
        edge("GSU-201", "SWYD-BUS-A", "high", "GSU secondary rises by filled tap to SWYD-BUS-A."),
        edge("SWYD-BUS-A", "CB-GRID-A", "high", "Switchyard bus A terminates at CB-GRID-A."),
        edge("CB-GRID-A", "GRID-230A", "high", "Solid conductor from CB-GRID-A to GRID-230A source block."),
        edge("SWYD-BUS-A", "CB-TIE-230", "high", "Filled vertical tap from SWYD-BUS-A to tie breaker."),
        edge("CB-TIE-230", "SWYD-BUS-B", "high", "Filled vertical tap from tie breaker to SWYD-BUS-B."),
        edge("SWYD-BUS-B", "CB-GRID-B", "high", "Switchyard bus B terminates at CB-GRID-B."),
        edge("CB-GRID-B", "GRID-230B", "high", "Solid conductor from CB-GRID-B to GRID-230B source block."),
        edge("SWYD-BUS-A", "TR-SST-201", "high", "Filled tap from SWYD-BUS-A down to TR-SST-201; crossing over BUS-B has no junction dot."),
        edge("SWYD-BUS-B", "TR-SST-202", "medium", "Diego interpreted SST-202 feed as tied to SWYD-BUS-B."),
        edge("IPB-201", "TR-UAT-201", "high", "Auxiliary tap from IPB-201 lower terminal to TR-UAT-201."),
        edge("IPB-201", "TR-UAT-202", "high", "Auxiliary tap from IPB-201 lower terminal to TR-UAT-202."),
        edge("TR-UAT-201", "CB-UAT-1", "high", "TR-UAT-201 secondary drops to CB-UAT-1."),
        edge("CB-UAT-1", "BUS-6KV-A", "high", "CB-UAT-1 bottom terminal lands on BUS-6KV-A."),
        edge("TR-UAT-202", "CB-UAT-2", "high", "TR-UAT-202 secondary drops to CB-UAT-2."),
        edge("CB-UAT-2", "BUS-6KV-B", "high", "CB-UAT-2 bottom terminal lands on BUS-6KV-B."),
        edge("TR-SST-201", "CB-SST-1", "high", "TR-SST-201 secondary drops to CB-SST-1."),
        edge("CB-SST-1", "BUS-6KV-A", "high", "CB-SST-1 bottom terminal lands on BUS-6KV-A."),
        edge("TR-SST-202", "CB-SST-2", "high", "TR-SST-202 secondary drops to CB-SST-2."),
        edge("CB-SST-2", "BUS-6KV-B", "high", "CB-SST-2 bottom terminal lands on BUS-6KV-B."),
        edge("DG-201A", "CB-DG-A", "high", "Solid feeder from diesel generator A to CB-DG-A."),
        edge("CB-DG-A", "ATS-A", "high", "Solid feeder from CB-DG-A to ATS-A."),
        edge("ATS-A", "BUS-6KV-A", "high", "ATS-A output drops to BUS-6KV-A."),
        edge("DG-201B", "CB-DG-B", "high", "Solid feeder from diesel generator B to CB-DG-B."),
        edge("CB-DG-B", "ATS-B", "high", "Solid feeder from CB-DG-B to ATS-B."),
        edge("ATS-B", "BUS-6KV-B", "high", "ATS-B output drops to BUS-6KV-B."),
        edge("BUS-6KV-A", "CB-TIE-6KV", "high", "BUS-6KV-A terminates at left side of CB-TIE-6KV."),
        edge("CB-TIE-6KV", "BUS-6KV-B", "high", "Right side of CB-TIE-6KV terminates on BUS-6KV-B."),
        edge("BUS-6KV-A", "PT-6KV-A", "high", "Potential transformer A has a dotted/vertical tap from BUS-6KV-A."),
        edge("BUS-6KV-B", "PT-6KV-B", "high", "Potential transformer B has a dotted/vertical tap from BUS-6KV-B."),
        edge("BUS-6KV-A", "DS-6KV-A", "high", "BUS-6KV-A tap feeds DS-6KV-A."),
        edge("DS-6KV-A", "BUS-4KV-N", "high", "DS-6KV-A lower terminal lands on BUS-4KV-N."),
        edge("BUS-6KV-B", "DS-6KV-B", "high", "BUS-6KV-B tap feeds DS-6KV-B."),
        edge("DS-6KV-B", "BUS-4KV-N", "high", "DS-6KV-B lower terminal lands on BUS-4KV-N."),
        edge("BUS-6KV-A", "TR-480A", "high", "BUS-6KV-A vertical feeder to TR-480A."),
        edge("TR-480A", "CB-LC-A1", "high", "TR-480A secondary drops to CB-LC-A1."),
        edge("CB-LC-A1", "LC-480A", "high", "CB-LC-A1 bottom terminal drops to LC-480A."),
        edge("LC-480A", "UV-SENS-A", "medium", "Dotted sensing tap from LC-480A terminal area to UV-SENS-A."),
        edge("LC-480A", "MCC-CCW-A", "high", "Solid feeder from LC-480A to MCC-CCW-A."),
        edge("LC-480A", "MCC-SW-A", "high", "Solid feeder from LC-480A to MCC-SW-A."),
        edge("LC-480A", "MCC-HPI-A", "high", "Solid feeder from LC-480A to MCC-HPI-A."),
        edge("LC-480A", "MCC-VENT-A", "high", "Solid feeder from LC-480A to MCC-VENT-A."),
        edge("LC-480A", "CHGR-A", "medium", "Diego retained visible long down-feed from the A-side load center region to CHGR-A."),
        edge("BUS-6KV-B", "TR-480B", "high", "BUS-6KV-B vertical feeder to TR-480B."),
        edge("TR-480B", "CB-LC-B1", "high", "TR-480B secondary drops to CB-LC-B1."),
        edge("CB-LC-B1", "LC-480B", "high", "CB-LC-B1 bottom terminal drops to LC-480B."),
        edge("LC-480B", "UV-SENS-B", "medium", "Dotted sensing tap from LC-480B terminal area to UV-SENS-B."),
        edge("LC-480B", "MCC-CCW-B", "high", "Solid feeder from LC-480B to MCC-CCW-B."),
        edge("LC-480B", "MCC-SW-B", "high", "Solid feeder from LC-480B to MCC-SW-B."),
        edge("LC-480B", "MCC-HPI-B", "high", "Solid feeder from LC-480B to MCC-HPI-B."),
        edge("LC-480B", "MCC-VENT-B", "high", "Solid feeder from LC-480B to MCC-VENT-B."),
        edge("LC-480B", "CHGR-B", "medium", "Diego retained visible long down-feed from the B-side load center region to CHGR-B."),
        edge("BUS-4KV-N", "TR-480N", "high", "BUS-4KV-N vertical feeder to TR-480N."),
        edge("TR-480N", "CB-LC-N1", "high", "TR-480N secondary drops to CB-LC-N1."),
        edge("CB-LC-N1", "LC-480N", "high", "CB-LC-N1 drops to LC-480N."),
        edge("LC-480N", "LP-N-A", "high", "Solid feeder from LC-480N to LP-N-A."),
        edge("LP-N-A", "HTR-BLDG-A", "high", "LP-N-A drops to HTR-BLDG-A."),
        edge("LC-480N", "LP-N-B", "high", "Solid feeder from LC-480N to LP-N-B."),
        edge("LP-N-B", "HTR-BLDG-B", "high", "LP-N-B drops to HTR-BLDG-B."),
        edge("MCC-CCW-A", "JBX-CCW-A", "high", "MCC-CCW-A vertical feeder to JBX-CCW-A."),
        edge("JBX-CCW-A", "PUMP-CCW-A", "high", "JBX-CCW-A drops to PUMP-CCW-A."),
        edge("MCC-CCW-A", "MOV-CCW-201A", "high", "MCC-CCW-A routed feeder to MOV-CCW-201A."),
        edge("MCC-SW-A", "JBX-SW-A", "high", "MCC-SW-A vertical feeder to JBX-SW-A."),
        edge("JBX-SW-A", "PUMP-SW-A", "high", "JBX-SW-A drops to PUMP-SW-A."),
        edge("MCC-HPI-A", "PUMP-HPI-A", "high", "MCC-HPI-A vertical feeder to PUMP-HPI-A."),
        edge("MCC-HPI-A", "MOV-SI-201A", "high", "MCC-HPI-A routed feeder to MOV-SI-201A."),
        edge("MCC-VENT-A", "FAN-CR-A", "high", "MCC-VENT-A drops to FAN-CR-A."),
        edge("MCC-CCW-B", "JBX-CCW-B", "high", "MCC-CCW-B vertical feeder to JBX-CCW-B."),
        edge("JBX-CCW-B", "PUMP-CCW-B", "high", "JBX-CCW-B drops to PUMP-CCW-B."),
        edge("MCC-CCW-B", "MOV-CCW-201B", "high", "MCC-CCW-B routed feeder to MOV-CCW-201B."),
        edge("MCC-SW-B", "JBX-SW-B", "high", "MCC-SW-B vertical feeder to JBX-SW-B."),
        edge("JBX-SW-B", "PUMP-SW-B", "high", "JBX-SW-B drops to PUMP-SW-B."),
        edge("MCC-HPI-B", "PUMP-HPI-B", "high", "MCC-HPI-B vertical feeder to PUMP-HPI-B."),
        edge("MCC-HPI-B", "MOV-SI-201B", "high", "MCC-HPI-B routed feeder to MOV-SI-201B."),
        edge("MCC-VENT-B", "FAN-CR-B", "high", "MCC-VENT-B drops to FAN-CR-B."),
        edge("CHGR-A", "PNL-DC-A", "high", "Solid conductor from CHGR-A to PNL-DC-A."),
        edge("CHGR-A", "BAT-125A", "high", "CHGR-A drops to BAT-125A."),
        edge("BAT-125A", "PNL-DC-A", "high", "Solid side feeder from BAT-125A to PNL-DC-A."),
        edge("PNL-DC-A", "REC-A", "high", "PNL-DC-A drops to REC-A."),
        edge("REC-A", "INV-A", "high", "REC-A routes to INV-A."),
        edge("INV-A", "UPS-A", "high", "INV-A drops to UPS-A."),
        edge("BAT-125A", "GND-A", "high", "Dotted ground bond from BAT-125A to GND-A."),
        edge("REC-A", "GND-A", "high", "Dotted ground bond from REC-A to GND-A."),
        edge("GND-A", "GND-MAIN", "high", "Dotted grounding path from GND-A to GND-MAIN."),
        edge("CHGR-B", "PNL-DC-B", "high", "Solid conductor from CHGR-B to PNL-DC-B."),
        edge("CHGR-B", "BAT-125B", "high", "CHGR-B drops to BAT-125B."),
        edge("BAT-125B", "PNL-DC-B", "high", "Solid side feeder from BAT-125B to PNL-DC-B."),
        edge("PNL-DC-B", "REC-B", "high", "PNL-DC-B drops to REC-B."),
        edge("REC-B", "INV-B", "high", "REC-B routes to INV-B."),
        edge("INV-B", "UPS-B", "high", "INV-B drops to UPS-B."),
        edge("BAT-125B", "GND-B", "high", "Dotted ground bond from BAT-125B to GND-B."),
        edge("REC-B", "GND-B", "high", "Dotted ground bond from REC-B to GND-B."),
        edge("GND-B", "GND-MAIN", "high", "Dotted grounding path from GND-B to GND-MAIN."),
        edge("PNL-INST-A", "RELAY-UV-A", "medium", "Same-row dashed route between instrument panel A and UV relay A."),
        edge("PNL-INST-B", "RELAY-UV-B", "medium", "Same-row dashed route between instrument panel B and UV relay B."),
        edge("CP-ESFAS-A", "RELAY-SI-A", "medium", "Same-row dashed route between ESFAS panel A and SI relay A."),
        edge("CP-ESFAS-B", "RELAY-SI-B", "medium", "Same-row dashed route between ESFAS panel B and SI relay B."),
        edge("PLC-RPS-A", "RELAY-LOAD-A", "medium", "Same-row dashed route between RPS PLC A and load relay A."),
        edge("PLC-RPS-B", "RELAY-LOAD-B", "medium", "Same-row dashed route between RPS PLC B and load relay B."),
        edge("JBX-ESF-A", "RELAY-DG-A", "medium", "Same-row dashed route between ESF junction box A and DG relay A."),
        edge("JBX-ESF-B", "RELAY-DG-B", "medium", "Same-row dashed route between ESF junction box B and DG relay B."),
    ]
    return rows


def round_01_jennifer_edges() -> list[dict[str, str]]:
    rows = []
    for row in round_01_diego_edges():
        if normalize_edge(row["source"], row["target"]) == normalize_edge("SWYD-BUS-B", "TR-SST-202"):
            continue
        reviewed = dict(row)
        reviewed["review_action"] = "jennifer_retained"
        rows.append(reviewed)
    rows.append(
        edge(
            "GRID-230B",
            "TR-SST-202",
            "high",
            "Jennifer correction: SST-202 primary visually lands on the GRID-230B/post-CB-GRID-B conductor, not directly on SWYD-BUS-B.",
            "jennifer_replaced_swyd_bus_b_source",
        )
    )
    return rows


def round_02_diego_edges() -> list[dict[str, str]]:
    rows = []
    for row in round_01_jennifer_edges():
        agreed = dict(row)
        agreed["review_action"] = "diego_round2_agreed_with_jennifer"
        rows.append(agreed)
    return rows


def round_02_jennifer_edges() -> list[dict[str, str]]:
    rows = []
    for row in round_02_diego_edges():
        saturated = dict(row)
        saturated["review_action"] = "saturated_retained"
        rows.append(saturated)
    return rows


ROUND_NOTES = {
    "round_01_diego": [
        {
            "item": "node_policy",
            "decision": "Included 100 final_label components from component_visual_ocr_labels.csv plus five visible named electrical buses; excluded broad green area boxes and anonymous WN-* nodes.",
            "evidence": "Raw diagram and detected/logical overlay show SWYD-BUS-A, SWYD-BUS-B, BUS-6KV-A, BUS-6KV-B, BUS-4KV-N as true buses.",
            "uncertainty": "low",
        },
        {
            "item": "BUS-4KV-N label",
            "decision": "Used BUS-4KV-N from raw visual label, despite Diego noting overlay/OCR ambiguity.",
            "evidence": "Raw crop reads BUS-4KV-N; raw is the most reliable resource.",
            "uncertainty": "medium",
        },
        {
            "item": "uncertain_high_recall_candidates",
            "decision": "Did not include CT-to-control, PT-to-control, UV-to-control, long DC/control-bay routes, right relay output trunks, or MOV/FAN/HPI-to-control routes in Diego matrix because endpoints were ambiguous.",
            "evidence": "Diego listed these separately as uncertain candidates; no GT or validation feedback used.",
            "uncertainty": "high",
        },
    ],
    "round_01_jennifer": [
        {
            "item": "TR-SST-202 source",
            "decision": "Replaced SWYD-BUS-B--TR-SST-202 with GRID-230B--TR-SST-202.",
            "evidence": "Raw crop shows SST-202 primary landing on the GRID-230B conductor after CB-GRID-B; it does not directly tap SWYD-BUS-B.",
            "uncertainty": "low",
        },
        {
            "item": "BUS-4KV-N label",
            "decision": "Kept BUS-4KV-N from raw visual label.",
            "evidence": "Raw bus label is clearer than overlay ambiguity.",
            "uncertainty": "low",
        },
        {
            "item": "charger feeders",
            "decision": "Kept LC-480A--CHGR-A and LC-480B--CHGR-B.",
            "evidence": "Long but continuous solid feeders descend from A/B 480 V load-center regions to the charger inputs.",
            "uncertainty": "medium",
        },
        {
            "item": "ct_and_control_pruning",
            "decision": "Did not add CT-EDG-A/B to DG or panel endpoints, nor extra PT/UV/DC/control-bay trunk edges beyond direct same-row panel-relay ties.",
            "evidence": "Visible lanes exist, but exact endpoints/crossing junctions are not sufficiently supported.",
            "uncertainty": "high",
        },
    ],
    "round_02_diego": [
        {
            "item": "saturation_check",
            "decision": "Diego agreed exactly with Jennifer's Round 1 corrected graph.",
            "evidence": "Second high-recall pass found no visually supported additions/removals; retained GRID-230B--TR-SST-202 correction.",
            "uncertainty": "low",
        },
        {
            "item": "excluded_uncertain_candidates",
            "decision": "No CT/PT/UV/DC/control-bay trunk candidates added in Round 2.",
            "evidence": "Exact named endpoints remain ambiguous in the raw and derived resources.",
            "uncertainty": "high",
        },
    ],
    "round_02_jennifer": [
        {
            "item": "saturation",
            "decision": "Jennifer agreed with Diego Round 2 with no changes.",
            "evidence": "Final precision check retained GRID-230B--TR-SST-202, BUS-4KV-N, A/B load-center-to-charger feeds, and same-row control-panel/relay edges.",
            "uncertainty": "low",
        },
        {
            "item": "excluded_edges",
            "decision": "CT-EDG-A/B, extra PT/UV/DC/control-bay trunk candidates, and right relay output trunks remain excluded.",
            "evidence": "Named endpoints are ambiguous or crossings lack junction proof in raw and derived resources.",
            "uncertainty": "high",
        },
    ],
}


def validate(nodes: list[str], edge_rows: list[dict[str, str]]) -> dict[str, object]:
    missing = sorted({n for row in edge_rows for n in (row["source"], row["target"]) if n not in nodes})
    duplicates = []
    seen = set()
    for row in edge_rows:
        key = normalize_edge(row["source"], row["target"])
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    return {
        "node_count": len(nodes),
        "edge_count": len(seen),
        "missing_nodes_in_edges": missing,
        "duplicate_edges": duplicates,
    }


def write_round(round_name: str, edge_rows: list[dict[str, str]], notes: list[dict[str, str]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = read_component_nodes() + BUS_NODES
    validation = validate(nodes, edge_rows)
    if validation["missing_nodes_in_edges"]:
        raise ValueError(f"missing nodes: {validation['missing_nodes_in_edges']}")
    if validation["duplicate_edges"]:
        raise ValueError(f"duplicate edges: {validation['duplicate_edges']}")
    write_matrix(RESULTS / f"{round_name}_matrix.csv", nodes, edge_rows)
    write_edges(RESULTS / f"{round_name}_edges.csv", edge_rows)
    write_notes(RESULTS / f"{round_name}_notes.csv", notes)
    with (RESULTS / f"{round_name}_validation.json").open("w", encoding="utf-8") as f:
        json.dump(validation, f, indent=2)


def write_final_outputs() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    nodes = read_component_nodes() + BUS_NODES
    final_edges = round_02_jennifer_edges()
    validation = validate(nodes, final_edges)
    if validation["missing_nodes_in_edges"] or validation["duplicate_edges"]:
        raise ValueError(validation)

    final_matrix = RESULTS / "final_connectivity_matrix.csv"
    final_edges_path = RESULTS / "final_connectivity_edges.csv"
    final_nodes_path = RESULTS / "final_connectivity_nodes.csv"
    final_uncertain_path = RESULTS / "final_uncertain_candidates.csv"
    final_summary_path = RESULTS / "final_connectivity_summary.md"
    final_validation_path = RESULTS / "final_connectivity_validation.json"

    write_matrix(final_matrix, nodes, final_edges)
    write_edges(final_edges_path, final_edges)
    shutil.copyfile(final_edges_path, RESULTS / "final_edges.csv")

    component_meta = {}
    with (INPUT / "component_visual_ocr_labels.csv").open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            component_meta[row["final_label"]] = row
    with final_nodes_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["node", "node_kind", "component_type", "source", "bbox", "centroid", "confidence"],
        )
        writer.writeheader()
        for node in nodes:
            if node in component_meta:
                meta = component_meta[node]
                writer.writerow(
                    {
                        "node": node,
                        "node_kind": meta.get("node_kind", "physical_component"),
                        "component_type": meta.get("component_type", ""),
                        "source": "component_visual_ocr_labels.csv",
                        "bbox": meta.get("bbox", ""),
                        "centroid": meta.get("centroid", ""),
                        "confidence": meta.get("confidence", ""),
                    }
                )
            else:
                writer.writerow(
                    {
                        "node": node,
                        "node_kind": "logical_bus",
                        "component_type": "named_bus",
                        "source": "raw schematic visual label plus detected/logical overlay",
                        "bbox": "",
                        "centroid": "",
                        "confidence": "high",
                    }
                )

    uncertain_rows = [
        {
            "candidate": "CT-EDG-A / CT-EDG-B to DG or control-panel endpoints",
            "decision": "excluded",
            "reason": "CT symbols are present, but no direct named endpoint is visually supported strongly enough for a matrix edge.",
        },
        {
            "candidate": "PT-6KV-A/B or UV-SENS-A/B to PNL-INST/RELAY-UV endpoints",
            "decision": "excluded except bus/load-center sensing taps already listed",
            "reason": "Long dashed/dotted continuations exist, but exact named endpoints/crossing junctions are ambiguous.",
        },
        {
            "candidate": "PNL-DC/UPS/REC long dash-dot routes to ESFAS/RPS control bay",
            "decision": "excluded",
            "reason": "Routes are visible but endpoints are ambiguous; adding them would overconnect the control bay.",
        },
        {
            "candidate": "right-side relay output trunks and cross-row relay interconnects",
            "decision": "excluded",
            "reason": "Same-row panel-to-relay edges are retained; trunk crossings lack filled junction proof.",
        },
    ]
    with final_uncertain_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate", "decision", "reason"])
        writer.writeheader()
        writer.writerows(uncertain_rows)

    isolated = sorted({node for node in nodes} - {n for row in final_edges for n in (row["source"], row["target"])})
    validation.update(
        {
            "isolated_nodes": isolated,
            "final_source_round": "round_02_jennifer",
            "ground_truth_used": False,
        }
    )
    with final_validation_path.open("w", encoding="utf-8") as f:
        json.dump(validation, f, indent=2)

    final_summary_path.write_text(
        "\n".join(
            [
                "# Doc 6 Iteration 1 Final Connectivity Summary",
                "",
                "Workflow: Diego high-recall extraction -> Jennifer precision review -> Diego agreement -> Jennifer saturation.",
                "",
                f"Nodes: {validation['node_count']}",
                f"Edges: {validation['edge_count']}",
                f"Isolated named components retained as rows: {', '.join(isolated) if isolated else 'none'}",
                "",
                "Node policy: 100 component/OCR labels plus five visible named electrical buses: SWYD-BUS-A, SWYD-BUS-B, BUS-6KV-A, BUS-6KV-B, BUS-4KV-N.",
                "",
                "Key final correction: TR-SST-202 is connected to GRID-230B, not directly to SWYD-BUS-B.",
                "",
                "No GT, GT-derived validation, or metric feedback was used during extraction.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    write_round("round_01_diego", round_01_diego_edges(), ROUND_NOTES["round_01_diego"])
    write_round("round_01_jennifer", round_01_jennifer_edges(), ROUND_NOTES["round_01_jennifer"])
    write_round("round_02_diego", round_02_diego_edges(), ROUND_NOTES["round_02_diego"])
    write_round("round_02_jennifer", round_02_jennifer_edges(), ROUND_NOTES["round_02_jennifer"])
    write_final_outputs()


if __name__ == "__main__":
    main()
