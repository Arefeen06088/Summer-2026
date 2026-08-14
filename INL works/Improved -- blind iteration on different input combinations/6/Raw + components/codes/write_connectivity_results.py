from __future__ import annotations

import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + components")
RESULTS = BASE / "results"


NODES = [
    "GEN-G201", "IPB-201", "CB-GEN-201", "GSU-201", "SWYD-BUS-A", "SWYD-BUS-B",
    "CB-TIE-230", "CB-GRID-A", "GRID-230A", "CB-GRID-B", "GRID-230B",
    "TR-UAT-201", "TR-UAT-202", "TR-SST-201", "TR-SST-202",
    "EDG-201A", "CB-DG-A", "ATS-A", "CB-UAT-1", "CB-SST-1", "BUS-6KV-A",
    "CT-EDG-A", "PT-6KV-A", "DS-6KV-A", "CB-TIE-6KV", "BUS-4KV-N",
    "EDG-201B", "CB-DG-B", "ATS-B", "CB-UAT-2", "CB-SST-2", "BUS-6KV-B",
    "CT-EDG-B", "PT-6KV-B", "DS-6KV-B",
    "TR-480A", "CB-LC-A1", "LC-480A", "UV-SENS-A",
    "TR-480N", "CB-LC-N1", "LC-480N", "LP-N-A", "HTR-BLDG-A", "LP-N-B", "HTR-BLDG-B",
    "TR-480B", "CB-LC-B1", "LC-480B", "UV-SENS-B",
    "MCC-CCW-A", "JBX-CCW-A", "PUMP-CCW-A", "MOV-CCW-201A",
    "MCC-SW-A", "JBX-SW-A", "PUMP-SW-A",
    "MCC-HPI-A", "PUMP-HPI-A", "MOV-SI-201A",
    "MCC-VENT-A", "FAN-CR-A",
    "MCC-CCW-B", "JBX-CCW-B", "PUMP-CCW-B", "MOV-CCW-201B",
    "MCC-SW-B", "JBX-SW-B", "PUMP-SW-B",
    "MCC-HPI-B", "PUMP-HPI-B", "MOV-SI-201B",
    "MCC-VENT-B", "FAN-CR-B",
    "CHGR-A", "BAT-125A", "PNL-DC-A", "REC-A", "INV-A", "UPS-A",
    "CHGR-B", "BAT-125B", "PNL-DC-B", "REC-B", "INV-B", "UPS-B",
    "PNL-INST-A", "PNL-INST-B", "CP-ESFAS-A", "CP-ESFAS-B",
    "PLC-RPS-A", "PLC-RPS-B", "JBX-ESF-A", "JBX-ESF-B",
    "RELAY-UV-A", "RELAY-UV-B", "RELAY-SI-A", "RELAY-SI-B",
    "RELAY-LOAD-A", "RELAY-LOAD-B", "RELAY-DG-A", "RELAY-DG-B",
    "GND-A", "GND-B", "GND-MAIN",
]


ASSERTED_EDGES = [
    ("GEN-G201", "IPB-201", "solid_power", "Generator output connects to isolated phase bus."),
    ("IPB-201", "CB-GEN-201", "solid_power", "IPB output connects to generator breaker."),
    ("CB-GEN-201", "GSU-201", "solid_power", "Generator breaker feeds GSU transformer."),
    ("GSU-201", "SWYD-BUS-A", "solid_power", "GSU transformer lands on switchyard bus A."),
    ("IPB-201", "TR-UAT-201", "solid_power", "Solid IPB tap feeds unit auxiliary transformer 201."),
    ("IPB-201", "TR-UAT-202", "solid_power", "Solid IPB tap feeds unit auxiliary transformer 202."),
    ("SWYD-BUS-A", "CB-GRID-A", "solid_power", "Switchyard bus A terminal feeds grid breaker A."),
    ("CB-GRID-A", "GRID-230A", "solid_power", "Grid breaker A connects to 230 kV grid A."),
    ("SWYD-BUS-B", "CB-GRID-B", "solid_power", "Switchyard bus B terminal feeds grid breaker B."),
    ("CB-GRID-B", "GRID-230B", "solid_power", "Grid breaker B connects to 230 kV grid B."),
    ("SWYD-BUS-A", "TR-SST-201", "solid_power", "Switchyard bus A tap feeds station service transformer 201."),
    ("SWYD-BUS-B", "TR-SST-202", "solid_power", "Switchyard bus B tap feeds station service transformer 202."),
    ("TR-UAT-201", "CB-UAT-1", "solid_power", "UAT 201 secondary connects to UAT breaker 1."),
    ("CB-UAT-1", "BUS-6KV-A", "solid_power", "UAT breaker 1 lands on 6 kV bus A."),
    ("TR-SST-201", "CB-SST-1", "solid_power", "SST 201 secondary connects to SST breaker 1."),
    ("CB-SST-1", "BUS-6KV-A", "solid_power", "SST breaker 1 lands on 6 kV bus A."),
    ("EDG-201A", "CB-DG-A", "solid_power", "Diesel generator A connects to DG breaker A."),
    ("CB-DG-A", "ATS-A", "solid_power", "DG breaker A connects to ATS-A."),
    ("ATS-A", "BUS-6KV-A", "solid_power", "ATS-A output lands on 6 kV bus A."),
    ("TR-UAT-202", "CB-UAT-2", "solid_power", "UAT 202 secondary connects to UAT breaker 2."),
    ("CB-UAT-2", "BUS-6KV-B", "solid_power", "UAT breaker 2 lands on 6 kV bus B."),
    ("TR-SST-202", "CB-SST-2", "solid_power", "SST 202 secondary connects to SST breaker 2."),
    ("CB-SST-2", "BUS-6KV-B", "solid_power", "SST breaker 2 lands on 6 kV bus B."),
    ("EDG-201B", "CB-DG-B", "solid_power", "Diesel generator B connects to DG breaker B."),
    ("CB-DG-B", "ATS-B", "solid_power", "DG breaker B connects to ATS-B."),
    ("ATS-B", "BUS-6KV-B", "solid_power", "ATS-B output lands on 6 kV bus B."),
    ("BUS-6KV-A", "TR-480A", "solid_power", "6 kV bus A feeds transformer 480A."),
    ("TR-480A", "CB-LC-A1", "solid_power", "Transformer 480A secondary connects to load-center breaker A1."),
    ("CB-LC-A1", "LC-480A", "solid_power", "Breaker A1 feeds load center 480A."),
    ("BUS-4KV-N", "TR-480N", "solid_power", "Non-safety 4 kV bus feeds transformer 480N."),
    ("TR-480N", "CB-LC-N1", "solid_power", "Transformer 480N secondary connects to load-center breaker N1."),
    ("CB-LC-N1", "LC-480N", "solid_power", "Breaker N1 feeds load center 480N."),
    ("BUS-6KV-B", "TR-480B", "solid_power", "6 kV bus B feeds transformer 480B."),
    ("TR-480B", "CB-LC-B1", "solid_power", "Transformer 480B secondary connects to load-center breaker B1."),
    ("CB-LC-B1", "LC-480B", "solid_power", "Breaker B1 feeds load center 480B."),
    ("LC-480A", "MCC-CCW-A", "solid_power", "Load center A feeder to CCW MCC A."),
    ("MCC-CCW-A", "JBX-CCW-A", "solid_power", "CCW MCC A feeder to CCW junction box A."),
    ("JBX-CCW-A", "PUMP-CCW-A", "solid_power", "CCW junction box A to CCW pump A."),
    ("MCC-CCW-A", "MOV-CCW-201A", "solid_power", "CCW MCC A branch to CCW MOV 201A."),
    ("LC-480A", "MCC-SW-A", "solid_power", "Load center A feeder to service-water MCC A."),
    ("MCC-SW-A", "JBX-SW-A", "solid_power", "SW MCC A feeder to SW junction box A."),
    ("JBX-SW-A", "PUMP-SW-A", "solid_power", "SW junction box A to SW pump A."),
    ("LC-480A", "MCC-HPI-A", "solid_power", "Load center A feeder to HPI MCC A."),
    ("MCC-HPI-A", "PUMP-HPI-A", "solid_power", "HPI MCC A branch to HPI pump A."),
    ("MCC-HPI-A", "MOV-SI-201A", "solid_power", "HPI MCC A branch to SI MOV 201A."),
    ("LC-480A", "MCC-VENT-A", "solid_power", "Load center A feeder to ventilation MCC A."),
    ("MCC-VENT-A", "FAN-CR-A", "solid_power", "Ventilation MCC A feeder to control-room fan A."),
    ("LC-480B", "MCC-CCW-B", "solid_power", "Load center B feeder to CCW MCC B."),
    ("MCC-CCW-B", "JBX-CCW-B", "solid_power", "CCW MCC B feeder to CCW junction box B."),
    ("JBX-CCW-B", "PUMP-CCW-B", "solid_power", "CCW junction box B to CCW pump B."),
    ("MCC-CCW-B", "MOV-CCW-201B", "solid_power", "CCW MCC B branch to CCW MOV 201B."),
    ("LC-480B", "MCC-SW-B", "solid_power", "Load center B feeder to service-water MCC B."),
    ("MCC-SW-B", "JBX-SW-B", "solid_power", "SW MCC B feeder to SW junction box B."),
    ("JBX-SW-B", "PUMP-SW-B", "solid_power", "SW junction box B to SW pump B."),
    ("LC-480B", "MCC-HPI-B", "solid_power", "Load center B feeder to HPI MCC B."),
    ("MCC-HPI-B", "PUMP-HPI-B", "solid_power", "HPI MCC B branch to HPI pump B."),
    ("MCC-HPI-B", "MOV-SI-201B", "solid_power", "HPI MCC B branch to SI MOV 201B."),
    ("LC-480B", "MCC-VENT-B", "solid_power", "Load center B feeder to ventilation MCC B."),
    ("MCC-VENT-B", "FAN-CR-B", "solid_power", "Ventilation MCC B feeder to control-room fan B."),
    ("LC-480N", "LP-N-A", "solid_power", "Non-safety load center branch to panel LP-N-A."),
    ("LP-N-A", "HTR-BLDG-A", "solid_power", "LP-N-A feeds building heater A."),
    ("LC-480N", "LP-N-B", "solid_power", "Non-safety load center branch to panel LP-N-B."),
    ("LP-N-B", "HTR-BLDG-B", "solid_power", "LP-N-B feeds building heater B."),
    ("LC-480A", "CHGR-A", "solid_power", "Load center A solid drop supplies charger A."),
    ("CHGR-A", "BAT-125A", "dc_power", "Charger A connects to 125 V battery A."),
    ("CHGR-A", "PNL-DC-A", "dc_power", "Charger A connects to DC panel A."),
    ("BAT-125A", "PNL-DC-A", "dc_power", "Battery A connects to DC panel A."),
    ("PNL-DC-A", "REC-A", "dc_power", "DC panel A connects to rectifier/rec A."),
    ("REC-A", "INV-A", "dc_power", "REC-A connects to inverter A."),
    ("INV-A", "UPS-A", "dc_power", "Inverter A feeds UPS-A."),
    ("LC-480B", "CHGR-B", "solid_power", "Load center B solid drop supplies charger B."),
    ("CHGR-B", "BAT-125B", "dc_power", "Charger B connects to 125 V battery B."),
    ("CHGR-B", "PNL-DC-B", "dc_power", "Charger B connects to DC panel B."),
    ("BAT-125B", "PNL-DC-B", "dc_power", "Battery B connects to DC panel B."),
    ("PNL-DC-B", "REC-B", "dc_power", "DC panel B connects to rectifier/rec B."),
    ("REC-B", "INV-B", "dc_power", "REC-B connects to inverter B."),
    ("INV-B", "UPS-B", "dc_power", "Inverter B feeds UPS-B."),
    ("SWYD-BUS-A", "CB-TIE-230", "tie", "A-side terminal of 230 kV switchyard tie breaker."),
    ("CB-TIE-230", "SWYD-BUS-B", "tie", "B-side terminal of 230 kV switchyard tie breaker."),
    ("BUS-6KV-A", "CB-TIE-6KV", "tie", "A-side terminal of 6 kV tie breaker."),
    ("CB-TIE-6KV", "BUS-6KV-B", "tie", "B-side terminal of 6 kV tie breaker."),
    ("BUS-6KV-A", "DS-6KV-A", "tie", "6 kV bus A terminal to disconnect switch A."),
    ("DS-6KV-A", "BUS-4KV-N", "tie", "Disconnect switch A terminal to non-safety 4 kV bus."),
    ("BUS-6KV-B", "DS-6KV-B", "tie", "6 kV bus B terminal to disconnect switch B."),
    ("DS-6KV-B", "BUS-4KV-N", "tie", "Disconnect switch B terminal to non-safety 4 kV bus."),
    ("BUS-6KV-A", "PT-6KV-A", "sensing", "Potential transformer A taps 6 kV bus A."),
    ("BUS-6KV-B", "PT-6KV-B", "sensing", "Potential transformer B taps 6 kV bus B."),
    ("LC-480A", "UV-SENS-A", "sensing", "Undervoltage sensor A taps load center A."),
    ("LC-480B", "UV-SENS-B", "sensing", "Undervoltage sensor B taps load center B."),
    ("PNL-INST-A", "RELAY-UV-A", "dashed_control", "Same-channel dashed path from instrument panel A to UV relay A."),
    ("PNL-INST-B", "RELAY-UV-B", "dashed_control", "Same-channel dashed path from instrument panel B to UV relay B."),
    ("CP-ESFAS-A", "RELAY-SI-A", "dashed_control", "Same-channel dashed path from ESFAS cabinet A to SI relay A."),
    ("CP-ESFAS-B", "RELAY-SI-B", "dashed_control", "Same-channel dashed path from ESFAS cabinet B to SI relay B."),
    ("PLC-RPS-A", "RELAY-LOAD-A", "dashed_control", "Same-channel dashed path from RPS PLC A to load relay A."),
    ("PLC-RPS-B", "RELAY-LOAD-B", "dashed_control", "Same-channel dashed path from RPS PLC B to load relay B."),
    ("JBX-ESF-A", "RELAY-DG-A", "dashed_control", "Same-channel dashed path from ESF junction box A to DG relay A."),
    ("JBX-ESF-B", "RELAY-DG-B", "dashed_control", "Same-channel dashed path from ESF junction box B to DG relay B."),
    ("BAT-125A", "GND-A", "ground_reference", "Dotted ground bond from battery A to GND-A."),
    ("REC-A", "GND-A", "ground_reference", "Dotted ground bond from REC-A to GND-A."),
    ("BAT-125B", "GND-B", "ground_reference", "Dotted ground bond from battery B to GND-B."),
    ("REC-B", "GND-B", "ground_reference", "Dotted ground bond from REC-B to GND-B."),
    ("GND-A", "GND-MAIN", "ground_reference", "Ground A bonds to main ground node."),
    ("GND-B", "GND-MAIN", "ground_reference", "Ground B bonds to main ground node."),
]


UNCERTAIN_EDGES = [
    ("CT-EDG-A", "EDG-201A", "CT/sensing branch lacks clear two-terminal adjacency."),
    ("CT-EDG-A", "PNL-INST-A", "Dashed sensing route enters shared corridor without unambiguous endpoint."),
    ("CT-EDG-A", "RELAY-DG-A", "Dashed route is not clean terminal-to-terminal."),
    ("CT-EDG-B", "EDG-201B", "CT/sensing branch lacks clear two-terminal adjacency."),
    ("CT-EDG-B", "PNL-INST-B", "Dashed sensing route enters shared corridor without unambiguous endpoint."),
    ("CT-EDG-B", "RELAY-DG-B", "Dashed route is not clean terminal-to-terminal."),
    ("PT-6KV-A", "PNL-INST-A", "Visible sensing path exists but exact component adjacency is ambiguous."),
    ("PT-6KV-B", "PNL-INST-B", "Visible sensing path exists but exact component adjacency is ambiguous."),
    ("UV-SENS-A", "PNL-INST-A", "Dashed route to instrument/control panels is ambiguous."),
    ("UV-SENS-B", "PNL-INST-B", "Dashed route to instrument/control panels is ambiguous."),
    ("MOV-CCW-201A", "JBX-ESF-A", "Control routing not a clear direct endpoint."),
    ("MOV-CCW-201B", "JBX-ESF-B", "Control routing not a clear direct endpoint."),
    ("MOV-SI-201A", "CP-ESFAS-A", "Control routing not a clear direct endpoint."),
    ("MOV-SI-201B", "CP-ESFAS-B", "Control routing not a clear direct endpoint."),
    ("FAN-CR-A", "PLC-RPS-A", "Control routing not a clear direct endpoint."),
    ("FAN-CR-B", "PLC-RPS-B", "Control routing not a clear direct endpoint."),
    ("UPS-A", "CP-ESFAS-A/B", "UPS/control-bay dashed paths are shared and ambiguous."),
    ("UPS-B", "CP-ESFAS-A/B", "UPS/control-bay dashed paths are shared and ambiguous."),
]


REJECTED_EDGES = [
    ("SWYD-BUS-A", "SWYD-BUS-B", "Buses connect only through CB-TIE-230."),
    ("BUS-6KV-A", "BUS-6KV-B", "Buses connect only through CB-TIE-6KV."),
    ("BUS-6KV-A/B", "BUS-4KV-N", "Connection is through DS-6KV-A/B, not direct."),
    ("cross-channel ESF/RPS pairs", "relays", "Cross-channel dashed corridors lack direct terminal evidence."),
    ("crossings without filled dots", "any component", "Crossings are not electrical junctions per drawing notes."),
]


def normalize(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


def validate(edges: list[tuple[str, str, str, str]], expected_edges: int) -> None:
    node_set = set(NODES)
    if len(NODES) != len(node_set):
        raise ValueError("Duplicate nodes found")
    edge_set = set()
    for source, target, *_ in edges:
        if source not in node_set:
            raise ValueError(f"Unknown source node: {source}")
        if target not in node_set:
            raise ValueError(f"Unknown target node: {target}")
        if source == target:
            raise ValueError(f"Unexpected self-loop: {source}")
        edge_set.add(normalize((source, target)))
    if len(edge_set) != expected_edges:
        raise ValueError(f"Expected {expected_edges} unique edges, got {len(edge_set)}")


def write_matrix(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    edge_set = {normalize((a, b)) for a, b, _, _ in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *NODES])
        for row in NODES:
            writer.writerow([row, *[0 if row == col else int(normalize((row, col)) in edge_set) for col in NODES]])


def write_edges(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "value", "status", "edge_type", "evidence"])
        for source, target, edge_type, evidence in edges:
            writer.writerow([source, target, 1, "asserted", edge_type, evidence])


def write_auxiliary_files() -> None:
    with (RESULTS / "final_uncertain_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "status", "reason"])
        for source, target, reason in UNCERTAIN_EDGES:
            writer.writerow([source, target, "uncertain", reason])

    with (RESULTS / "final_rejected_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "status", "reason"])
        for source, target, reason in REJECTED_EDGES:
            writer.writerow([source, target, "rejected", reason])

    summary = f"""# Document 6 Round Summaries

Resource folder: `{BASE}`

Allowed visual resources used:
- `raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | {len(NODES)} | {len(ASSERTED_EDGES)} | no | Proposed solid power, selected same-channel dashed control, and explicit ground-bond edges. |
| 1 | Jennifer precision | {len(NODES)} | {len(ASSERTED_EDGES)} | no | Kept Diego topology exactly; kept ambiguous CT/sensing/control trunks out of matrix. |
| 2 | Diego high-recall | {len(NODES)} | {len(ASSERTED_EDGES)} | yes | No deltas; confirmed uncertain edges should remain excluded. |
| 2 | Jennifer precision final | {len(NODES)} | {len(ASSERTED_EDGES)} | yes | Confirmed final 105-node, 103-edge graph and kept uncertain edges out of the matrix. |

## Final Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled terminals, solid feeders, bus taps, explicit tie/disconnect components, selected same-channel dashed terminal paths, and labeled ground bonds are asserted.
- Dashed shared corridors, crossings without filled dots, and ambiguous sensor/control trunks are excluded and recorded as uncertain/rejected.
"""
    (RESULTS / "round_summaries.md").write_text(summary, encoding="utf-8")


def write_token_estimates() -> None:
    rows = [
        {
            "document": "6",
            "iteration": "1",
            "call_id": "main-orchestration-aggregate",
            "agent": "Main agent",
            "model": "Codex session model",
            "input_tokens_est": 50000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 28000,
            "output_tokens_est": 11000,
            "reasoning_tokens_est": "not exposed",
            "total_low": 65000,
            "total_expected": 89000,
            "total_high": 125000,
            "usage_object_available": "no",
            "notes": "Aggregate estimate for orchestration, image inspection, tool-result digestion, and artifact generation.",
        },
        {
            "document": "6",
            "iteration": "1",
            "call_id": "diego-round-1",
            "agent": "Diego",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 13000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 26000,
            "output_tokens_est": 13000,
            "reasoning_tokens_est": "not exposed",
            "total_low": 43000,
            "total_expected": 52000,
            "total_high": 70000,
            "usage_object_available": "no",
            "notes": "Prompt plus full raw/overlay and crop set; official token counter unavailable because OPENAI_API_KEY was not set.",
        },
        {
            "document": "6",
            "iteration": "1",
            "call_id": "jennifer-round-1",
            "agent": "Jennifer",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 17000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 21000,
            "output_tokens_est": 1100,
            "reasoning_tokens_est": "not exposed",
            "total_low": 34000,
            "total_expected": 39100,
            "total_high": 56000,
            "usage_object_available": "no",
            "notes": "Includes Diego proposal text and focused visual package.",
        },
        {
            "document": "6",
            "iteration": "1",
            "call_id": "diego-round-2",
            "agent": "Diego",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 900,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 9000,
            "output_tokens_est": 450,
            "reasoning_tokens_est": "not exposed",
            "total_low": 8000,
            "total_expected": 10350,
            "total_high": 16000,
            "usage_object_available": "no",
            "notes": "Focused saturation prompt with raw and three focused crops.",
        },
        {
            "document": "6",
            "iteration": "1",
            "call_id": "jennifer-round-2-final",
            "agent": "Jennifer",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 450,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 7000,
            "output_tokens_est": 250,
            "reasoning_tokens_est": "not exposed",
            "total_low": 6200,
            "total_expected": 7700,
            "total_high": 12000,
            "usage_object_available": "no",
            "notes": "Final confirmation prompt with raw, control bay, and DC/UPS crop.",
        },
    ]
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_expected = sum(int(row["total_expected"]) for row in rows)
    (RESULTS / "token_usage_summary.md").write_text(
        "# Token Usage Estimate\n\n"
        "No `OPENAI_API_KEY` was present, so the OpenAI Responses input-token counting endpoint could not be called, "
        "and subagent usage objects were not exposed by the local multi-agent tool. Estimates use prompt text length plus "
        "image-count/resolution heuristics for the submitted visual payloads.\n\n"
        f"Expected total tokens across identified document-6 calls: **{total_expected:,}**.\n",
        encoding="utf-8",
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    validate(ASSERTED_EDGES, 103)

    for name in ["diego_round1", "jennifer_round1", "diego_round2", "jennifer_round2_final", "final"]:
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", ASSERTED_EDGES)
        write_matrix(RESULTS / f"{name}_matrix.csv", ASSERTED_EDGES)
        write_edges(RESULTS / f"{name}_edges.csv", ASSERTED_EDGES)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", ASSERTED_EDGES)
    write_edges(RESULTS / "final_edges.csv", ASSERTED_EDGES)
    write_auxiliary_files()
    write_token_estimates()

    print(f"nodes={len(NODES)}")
    print(f"edges={len({normalize((a, b)) for a, b, _, _ in ASSERTED_EDGES})}")
    print(RESULTS)


if __name__ == "__main__":
    main()
