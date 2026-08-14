from __future__ import annotations

import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + components")
RESULTS = BASE / "results"


NODES = [
    "GRID-N230", "ISO-230A", "BRK-2301", "GRID-S230", "ISO-230B", "BRK-2302",
    "GEN-G101", "GSU-1", "BUS-SY230", "TR-RAT-1A", "TR-UAT-1A", "CB-AUX-A",
    "BUS-AUX13A", "TR-UAT-1B", "CB-AUX-B", "BUS-AUX13B", "TR-RAT-1B",
    "CB-TIE13", "BUS-NON1",
    "EDG-A", "CB-EDG-A", "TR-SAF-A", "CB-SAF-A", "BUS-416A", "CB-TIE-AB",
    "TR-480-A", "CB-LC-A", "LC-480A", "CB-MCCA1", "MCC-1A1", "PUMP-AFW-A",
    "CB-MCCA2", "MCC-1A2", "VLV-MSIV-A", "PUMP-CCW-A", "XFER-ATS-A",
    "CHG-125A", "BAT-125A", "PNL-DC-A", "INV-UPS-A", "UPS-PNL-A",
    "RECT-48V-A", "BAT-48V-A", "JB-RLY-A",
    "EDG-B", "CB-EDG-B", "TR-SAF-B", "CB-SAF-B", "BUS-416B", "TR-480-B",
    "CB-LC-B", "LC-480B", "CB-MCCB1", "MCC-1B1", "PUMP-AFW-B",
    "CB-MCCB2", "MCC-1B2", "VLV-MSIV-B", "PUMP-CCW-B",
    "EDG-C", "CB-EDG-C", "TR-SAF-C", "CB-SAF-C", "BUS-416C", "CB-TIE-CD",
    "TR-480-C", "CB-LC-C", "LC-480C", "CB-MCCC1", "MCC-1C1", "PUMP-RHR-A",
    "CB-MCCC2", "MCC-1C2", "HTR-BATRM-A", "FAN-CRHV-A", "XFER-ATS-B",
    "CHG-125B", "BAT-125B", "PNL-DC-B", "INV-UPS-B", "UPS-PNL-B",
    "RECT-48V-B", "BAT-48V-B", "JB-RLY-B",
    "EDG-D", "CB-EDG-D", "TR-SAF-D", "CB-SAF-D", "BUS-416D", "TR-480-D",
    "CB-LC-D", "LC-480D", "CB-MCCD1", "MCC-1D1", "PUMP-RHR-B",
    "CB-MCCD2", "MCC-1D2", "HTR-BATRM-B", "FAN-CRHV-B",
    "CP-ESFAS-1", "CP-ESFAS-2", "RELAY-K1A", "RELAY-K2A", "RELAY-UV-A",
    "RELAY-LOOP-C", "INST-NSSS-A", "RELAY-K1B", "RELAY-K2B", "RELAY-UV-B",
    "RELAY-LOOP-D", "INST-NSSS-B", "GND-GRID",
]


ROUND1_EDGES = [
    ("GRID-N230", "ISO-230A", "solid_power", "Left offsite source through isolator."),
    ("ISO-230A", "BRK-2301", "solid_power", "Series 230 kV isolator to breaker."),
    ("BRK-2301", "BUS-SY230", "solid_power", "Breaker drop lands on 230 kV switchyard bus."),
    ("GRID-S230", "ISO-230B", "solid_power", "Right offsite source through isolator."),
    ("ISO-230B", "BRK-2302", "solid_power", "Series 230 kV isolator to breaker."),
    ("BRK-2302", "BUS-SY230", "solid_power", "Breaker drop lands on 230 kV switchyard bus."),
    ("GEN-G101", "GSU-1", "solid_power", "Generator terminals feed step-up transformer."),
    ("GSU-1", "BUS-SY230", "solid_power", "Transformer output lands on 230 kV bus."),
    ("BUS-SY230", "TR-RAT-1A", "solid_power", "Bus tap down to reserve auxiliary transformer A."),
    ("BUS-SY230", "TR-UAT-1A", "solid_power", "Bus/generator-side tap to unit auxiliary transformer A."),
    ("TR-RAT-1A", "CB-AUX-A", "solid_power", "Transformer secondary feeds AUX A breaker."),
    ("TR-UAT-1A", "CB-AUX-A", "solid_power", "Unit auxiliary transformer A feeds AUX A breaker."),
    ("CB-AUX-A", "BUS-AUX13A", "solid_power", "Breaker lands on 13.8 kV aux bus A."),
    ("BUS-SY230", "TR-UAT-1B", "solid_power", "Bus/generator-side tap to unit auxiliary transformer B."),
    ("TR-UAT-1B", "CB-AUX-B", "solid_power", "Unit auxiliary transformer B feeds AUX B breaker."),
    ("CB-AUX-B", "BUS-AUX13B", "solid_power", "Breaker lands on 13.8 kV aux bus B."),
    ("BUS-SY230", "TR-RAT-1B", "solid_power", "Bus tap down to reserve auxiliary transformer B."),
    ("CB-AUX-B", "TR-RAT-1B", "solid_power", "Reserve auxiliary transformer B feeds AUX B breaker."),
    ("BUS-AUX13A", "BUS-NON1", "solid_power", "Non-safety service bus taps from the left 13.8 kV aux bus section."),
    ("BUS-AUX13A", "CB-TIE13", "tie", "A-side terminal of 13.8 kV tie breaker."),
    ("BUS-AUX13B", "CB-TIE13", "tie", "B-side terminal of 13.8 kV tie breaker."),
    ("BUS-416A", "CB-TIE-AB", "tie", "A-side terminal of 4.16 kV tie breaker."),
    ("CB-TIE-AB", "BUS-416B", "tie", "B-side terminal of 4.16 kV tie breaker."),
    ("BUS-416C", "CB-TIE-CD", "tie", "C-side terminal of 4.16 kV tie breaker."),
    ("CB-TIE-CD", "BUS-416D", "tie", "D-side terminal of 4.16 kV tie breaker."),
    ("BUS-AUX13A", "TR-SAF-A", "solid_power", "Aux bus A tap to safety transformer A."),
    ("TR-SAF-A", "CB-SAF-A", "solid_power", "Transformer A secondary to breaker."),
    ("CB-SAF-A", "BUS-416A", "solid_power", "Breaker lands on safety bus A."),
    ("EDG-A", "CB-EDG-A", "solid_power", "Emergency diesel generator A to breaker."),
    ("CB-EDG-A", "BUS-416A", "solid_power", "EDG breaker lands on safety bus A."),
    ("BUS-416A", "TR-480-A", "solid_power", "Safety bus A feeds 480 V transformer A."),
    ("TR-480-A", "CB-LC-A", "solid_power", "Transformer A secondary to load-center breaker."),
    ("CB-LC-A", "LC-480A", "solid_power", "Breaker lands on load center A."),
    ("LC-480A", "CB-MCCA1", "solid_power", "Load center A left feeder to MCC breaker."),
    ("CB-MCCA1", "MCC-1A1", "solid_power", "Breaker feeds motor control center A1."),
    ("MCC-1A1", "PUMP-AFW-A", "solid_power", "MCC A1 branch to AFW pump A."),
    ("MCC-1A1", "VLV-MSIV-A", "solid_power", "MCC A1 branch to MSIV A."),
    ("LC-480A", "CB-MCCA2", "solid_power", "Load center A right feeder to MCC breaker."),
    ("CB-MCCA2", "MCC-1A2", "solid_power", "Breaker feeds motor control center A2."),
    ("MCC-1A2", "PUMP-CCW-A", "solid_power", "MCC A2 branch to CCW pump A."),
    ("LC-480A", "XFER-ATS-A", "solid_power", "ATS-A normal feed from LC-480A side."),
    ("BUS-AUX13A", "TR-SAF-B", "solid_power", "Aux bus A tap to safety transformer B."),
    ("TR-SAF-B", "CB-SAF-B", "solid_power", "Transformer B secondary to breaker."),
    ("CB-SAF-B", "BUS-416B", "solid_power", "Breaker lands on safety bus B."),
    ("EDG-B", "CB-EDG-B", "solid_power", "Emergency diesel generator B to breaker."),
    ("CB-EDG-B", "BUS-416B", "solid_power", "EDG breaker lands on safety bus B."),
    ("BUS-416B", "TR-480-B", "solid_power", "Safety bus B feeds 480 V transformer B."),
    ("TR-480-B", "CB-LC-B", "solid_power", "Transformer B secondary to load-center breaker."),
    ("CB-LC-B", "LC-480B", "solid_power", "Breaker lands on load center B."),
    ("LC-480B", "CB-MCCB1", "solid_power", "Load center B left feeder to MCC breaker."),
    ("CB-MCCB1", "MCC-1B1", "solid_power", "Breaker feeds motor control center B1."),
    ("MCC-1B1", "PUMP-AFW-B", "solid_power", "MCC B1 branch to AFW pump B."),
    ("MCC-1B1", "VLV-MSIV-B", "solid_power", "MCC B1 branch to MSIV B."),
    ("LC-480B", "CB-MCCB2", "solid_power", "Load center B right feeder to MCC breaker."),
    ("CB-MCCB2", "MCC-1B2", "solid_power", "Breaker feeds motor control center B2."),
    ("MCC-1B2", "PUMP-CCW-B", "solid_power", "MCC B2 branch to CCW pump B."),
    ("XFER-ATS-A", "LC-480B", "solid_power", "ATS-A alternate feed from LC-480B side."),
    ("BUS-AUX13B", "TR-SAF-C", "solid_power", "Aux bus B tap to safety transformer C."),
    ("BUS-NON1", "TR-SAF-C", "solid_power", "Non-safety service bus also lands at transformer C upper terminal."),
    ("TR-SAF-C", "CB-SAF-C", "solid_power", "Transformer C secondary to breaker."),
    ("CB-SAF-C", "BUS-416C", "solid_power", "Breaker lands on safety bus C."),
    ("EDG-C", "CB-EDG-C", "solid_power", "Emergency diesel generator C to breaker."),
    ("CB-EDG-C", "BUS-416C", "solid_power", "EDG breaker lands on safety bus C."),
    ("BUS-416C", "TR-480-C", "solid_power", "Safety bus C feeds 480 V transformer C."),
    ("TR-480-C", "CB-LC-C", "solid_power", "Transformer C secondary to load-center breaker."),
    ("CB-LC-C", "LC-480C", "solid_power", "Breaker lands on load center C."),
    ("LC-480C", "CB-MCCC1", "solid_power", "Load center C left feeder to MCC breaker."),
    ("CB-MCCC1", "MCC-1C1", "solid_power", "Breaker feeds motor control center C1."),
    ("MCC-1C1", "PUMP-RHR-A", "solid_power", "MCC C1 branch to RHR pump A."),
    ("LC-480C", "CB-MCCC2", "solid_power", "Load center C right feeder to MCC breaker."),
    ("CB-MCCC2", "MCC-1C2", "solid_power", "Breaker feeds motor control center C2."),
    ("MCC-1C2", "HTR-BATRM-A", "solid_power", "MCC C2 branch to battery room heater A."),
    ("MCC-1C2", "FAN-CRHV-A", "solid_power", "MCC C2 branch to control room HVAC fan A."),
    ("LC-480C", "XFER-ATS-B", "solid_power", "ATS-B normal feed from LC-480C side."),
    ("BUS-AUX13B", "TR-SAF-D", "solid_power", "Aux bus B tap to safety transformer D."),
    ("TR-SAF-D", "CB-SAF-D", "solid_power", "Transformer D secondary to breaker."),
    ("CB-SAF-D", "BUS-416D", "solid_power", "Breaker lands on safety bus D."),
    ("EDG-D", "CB-EDG-D", "solid_power", "Emergency diesel generator D to breaker."),
    ("CB-EDG-D", "BUS-416D", "solid_power", "EDG breaker lands on safety bus D."),
    ("BUS-416D", "TR-480-D", "solid_power", "Safety bus D feeds 480 V transformer D."),
    ("TR-480-D", "CB-LC-D", "solid_power", "Transformer D secondary to load-center breaker."),
    ("CB-LC-D", "LC-480D", "solid_power", "Breaker lands on load center D."),
    ("LC-480D", "CB-MCCD1", "solid_power", "Load center D left feeder to MCC breaker."),
    ("CB-MCCD1", "MCC-1D1", "solid_power", "Breaker feeds motor control center D1."),
    ("MCC-1D1", "PUMP-RHR-B", "solid_power", "MCC D1 branch to RHR pump B."),
    ("LC-480D", "CB-MCCD2", "solid_power", "Load center D right feeder to MCC breaker."),
    ("CB-MCCD2", "MCC-1D2", "solid_power", "Breaker feeds motor control center D2."),
    ("MCC-1D2", "HTR-BATRM-B", "solid_power", "MCC D2 branch to battery room heater B."),
    ("MCC-1D2", "FAN-CRHV-B", "solid_power", "MCC D2 branch to control room HVAC fan B."),
    ("XFER-ATS-B", "LC-480D", "solid_power", "ATS-B alternate feed from LC-480D side."),
    ("XFER-ATS-A", "CHG-125A", "dc_power", "ATS-A output down to 125 VDC charger A."),
    ("CHG-125A", "BAT-125A", "dc_power", "Charger A to 125 VDC battery A."),
    ("BAT-125A", "PNL-DC-A", "dc_power", "Battery A to DC panel A."),
    ("PNL-DC-A", "INV-UPS-A", "dc_power", "DC panel A feeds inverter A."),
    ("INV-UPS-A", "UPS-PNL-A", "dc_power", "Inverter A output to vital AC panel A."),
    ("XFER-ATS-A", "RECT-48V-A", "dc_power", "ATS-A feed to 48 V rectifier A."),
    ("RECT-48V-A", "BAT-48V-A", "dc_power", "Rectifier A to 48 V battery A."),
    ("BAT-48V-A", "JB-RLY-A", "dc_power", "48 V battery A to relay power junction box A."),
    ("XFER-ATS-B", "CHG-125B", "dc_power", "ATS-B output down to 125 VDC charger B."),
    ("CHG-125B", "BAT-125B", "dc_power", "Charger B to 125 VDC battery B."),
    ("BAT-125B", "PNL-DC-B", "dc_power", "Battery B to DC panel B."),
    ("PNL-DC-B", "INV-UPS-B", "dc_power", "DC panel B feeds inverter B."),
    ("INV-UPS-B", "UPS-PNL-B", "dc_power", "Inverter B output to vital AC panel B."),
    ("XFER-ATS-B", "RECT-48V-B", "dc_power", "ATS-B feed to 48 V rectifier B."),
    ("RECT-48V-B", "BAT-48V-B", "dc_power", "Rectifier B to 48 V battery B."),
    ("BAT-48V-B", "JB-RLY-B", "dc_power", "48 V battery B to relay power junction box B."),
    ("CP-ESFAS-1", "CP-ESFAS-2", "dashed_control", "Parallel ESF actuation cabinets share visible dashed trunking."),
    ("CP-ESFAS-1", "RELAY-K1A", "dashed_control", "Dashed ESF/control line lands on relay K1A path."),
    ("CP-ESFAS-2", "RELAY-K2A", "dashed_control", "Dashed ESF/control line lands on relay K2A path."),
    ("CP-ESFAS-1", "RELAY-K1B", "dashed_control", "Dashed ESF/control line lands on relay K1B path."),
    ("CP-ESFAS-2", "RELAY-K2B", "dashed_control", "Dashed ESF/control line lands on relay K2B path."),
    ("CB-EDG-A", "RELAY-K1A", "dashed_control", "Control/trip line from EDG breaker A to start relay A."),
    ("CB-SAF-A", "RELAY-K1A", "dashed_control", "Control/trip line from safety breaker A to start relay A."),
    ("CB-EDG-B", "RELAY-K1B", "dashed_control", "Control/trip line from EDG breaker B to start relay B."),
    ("CB-SAF-B", "RELAY-K1B", "dashed_control", "Control/trip line from safety breaker B to start relay B."),
    ("CB-EDG-C", "RELAY-K2A", "dashed_control", "Control/trip line from EDG breaker C to start relay C."),
    ("CB-SAF-C", "RELAY-K2A", "dashed_control", "Control/trip line from safety breaker C to start relay C."),
    ("CB-EDG-D", "RELAY-K2B", "dashed_control", "Control/trip line from EDG breaker D to start relay D."),
    ("CB-SAF-D", "RELAY-K2B", "dashed_control", "Control/trip line from safety breaker D to start relay D."),
    ("BUS-416A", "RELAY-UV-A", "dashed_control", "Undervoltage sensing/control from safety bus A side."),
    ("BUS-416B", "RELAY-UV-A", "dashed_control", "Undervoltage sensing/control from safety bus B side."),
    ("BUS-416C", "RELAY-UV-B", "dashed_control", "Undervoltage sensing/control from safety bus C side."),
    ("BUS-416D", "RELAY-UV-B", "dashed_control", "Undervoltage sensing/control from safety bus D side."),
    ("BUS-416C", "RELAY-LOOP-C", "dashed_control", "Load-shed loop control from train C bus region."),
    ("BUS-416D", "RELAY-LOOP-D", "dashed_control", "Load-shed loop control from train D bus region."),
    ("CP-ESFAS-1", "INST-NSSS-A", "dashed_control", "Round-1 high-recall CP-to-instrument trunk, later demoted."),
    ("CP-ESFAS-2", "INST-NSSS-A", "dashed_control", "Round-1 high-recall CP-to-instrument trunk, later demoted."),
    ("CP-ESFAS-1", "INST-NSSS-B", "dashed_control", "Round-1 high-recall CP-to-instrument trunk, later demoted."),
    ("CP-ESFAS-2", "INST-NSSS-B", "dashed_control", "Round-1 high-recall CP-to-instrument trunk, later demoted."),
]


DEMOTED_FINAL = {
    ("CP-ESFAS-1", "INST-NSSS-A"),
    ("CP-ESFAS-2", "INST-NSSS-A"),
    ("CP-ESFAS-1", "INST-NSSS-B"),
    ("CP-ESFAS-2", "INST-NSSS-B"),
}


UNCERTAIN_FINAL = sorted(DEMOTED_FINAL | {
    ("CP-ESFAS-1/2", "RELAY-UV-A"),
    ("CP-ESFAS-1/2", "RELAY-LOOP-C"),
    ("CP-ESFAS-1/2", "RELAY-UV-B"),
    ("CP-ESFAS-1/2", "RELAY-LOOP-D"),
    ("INST-NSSS-A", "RELAY-LOOP-C"),
    ("INST-NSSS-B", "RELAY-LOOP-D"),
})


REJECTED_FINAL = [
    ("BUS-AUX13B", "BUS-NON1", "No solid tap from AUX13B to BUS-NON1 visible."),
    ("VLV-MSIV-A", "XFER-ATS-A", "Nearby ATS conductor is not a clean valve terminal."),
    ("VLV-MSIV-B", "XFER-ATS-A", "Nearby ATS conductor is not a clean valve terminal."),
    ("HTR-BATRM-A", "XFER-ATS-B", "Nearby ATS conductor is not a clean heater terminal."),
    ("HTR-BATRM-B", "XFER-ATS-B", "Nearby ATS conductor is not a clean heater terminal."),
    ("MCC-1A2", "VLV-MSIV-A", "Valve feed is visually from MCC-1A1 branch."),
    ("MCC-1B2", "VLV-MSIV-B", "Valve feed is visually from MCC-1B1 branch."),
    ("GND-GRID", "equipment dotted drops", "Grounding network left as non-matrix grounding layer."),
]


def normalize(edge: tuple[str, str]) -> tuple[str, str]:
    a, b = edge
    return tuple(sorted((a, b)))


def write_matrix(path: Path, edges: list[tuple[str, str, str, str]]) -> None:
    edge_set = {normalize((a, b)) for a, b, _, _ in edges}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *NODES])
        for row in NODES:
            writer.writerow([row, *[0 if row == col else int(normalize((row, col)) in edge_set) for col in NODES]])


def write_edges(path: Path, edges: list[tuple[str, str, str, str]], status: str = "asserted") -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "value", "status", "edge_type", "evidence"])
        for source, target, edge_type, evidence in edges:
            writer.writerow([source, target, 1, status, edge_type, evidence])


def write_lists() -> None:
    with (RESULTS / "final_uncertain_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "status", "reason"])
        for source, target in UNCERTAIN_FINAL:
            writer.writerow([source, target, "uncertain", "Visible dashed/control routing is not unambiguous enough for asserted adjacency."])

    with (RESULTS / "final_rejected_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "status", "reason"])
        for source, target, reason in REJECTED_FINAL:
            writer.writerow([source, target, "rejected", reason])


def write_summaries(final_edges: list[tuple[str, str, str, str]]) -> None:
    summary = f"""# Document 5 Round Summaries

Resource folder: `{BASE}`

Allowed visual resources used:
- `raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | {len(NODES)} | {len(ROUND1_EDGES)} | no | Included four CP-ESFAS-to-INST-NSSS dashed trunk edges as high-recall assertions. |
| 1 | Jennifer precision | {len(NODES)} | {len(ROUND1_EDGES)} | no | Kept Diego topology but marked several alternatives uncertain/rejected. |
| 2 | Diego high-recall | {len(NODES)} | {len(final_edges)} | near | Confirmed MCC labels are `MCC-1A1` style, kept ATS feeds, demoted CP-to-instrument links. |
| 2 | Jennifer precision final | {len(NODES)} | {len(final_edges)} | yes | Agreed with 125 asserted edges and demoted four CP-to-instrument links to uncertain. |

## Final Demoted Edges

These were asserted in round 1 and excluded from the final matrix:
- `CP-ESFAS-1 -- INST-NSSS-A`
- `CP-ESFAS-2 -- INST-NSSS-A`
- `CP-ESFAS-1 -- INST-NSSS-B`
- `CP-ESFAS-2 -- INST-NSSS-B`

## Final Matrix Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled bus taps/component terminals are asserted.
- Crossings without filled dots are not asserted.
- Dashed control/sensing connections are asserted only where terminal assignment is visually supported.
- `GND-GRID` is included as a labeled node but left isolated because the agents treated dotted grounding as a separate grounding layer rather than asserted power/control adjacency.
"""
    (RESULTS / "round_summaries.md").write_text(summary, encoding="utf-8")


def write_token_estimates() -> None:
    rows = [
        {
            "document": "5",
            "iteration": "1",
            "call_id": "main-orchestration-aggregate",
            "agent": "Main agent",
            "model": "Codex session model",
            "input_tokens_est": 42000,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 22000,
            "output_tokens_est": 9000,
            "reasoning_tokens_est": "not exposed",
            "total_low": 52000,
            "total_expected": 73000,
            "total_high": 100000,
            "usage_object_available": "no",
            "notes": "Aggregate estimate for visible orchestration, tool-result digestion, image inspection, and artifact generation. Exact per-call main usage is not exposed in this environment.",
        },
        {
            "document": "5",
            "iteration": "1",
            "call_id": "diego-round-1",
            "agent": "Diego",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 11500,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 17000,
            "output_tokens_est": 5200,
            "reasoning_tokens_est": "not exposed",
            "total_low": 26000,
            "total_expected": 33700,
            "total_high": 47000,
            "usage_object_available": "no",
            "notes": "Prompt plus full raw/overlay and nine crop images; official Responses token counter unavailable because OPENAI_API_KEY was not set.",
        },
        {
            "document": "5",
            "iteration": "1",
            "call_id": "jennifer-round-1",
            "agent": "Jennifer",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 16200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 17000,
            "output_tokens_est": 4200,
            "reasoning_tokens_est": "not exposed",
            "total_low": 31000,
            "total_expected": 37400,
            "total_high": 52000,
            "usage_object_available": "no",
            "notes": "Includes Diego round-1 proposal text and same visual package.",
        },
        {
            "document": "5",
            "iteration": "1",
            "call_id": "diego-round-2",
            "agent": "Diego",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 2200,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 10000,
            "output_tokens_est": 1000,
            "reasoning_tokens_est": "not exposed",
            "total_low": 10500,
            "total_expected": 13200,
            "total_high": 20000,
            "usage_object_available": "no",
            "notes": "Focused saturation prompt with full raw plus seven focused crops.",
        },
        {
            "document": "5",
            "iteration": "1",
            "call_id": "jennifer-round-2-final",
            "agent": "Jennifer",
            "model": "gpt-5.5 requested; reused existing agent due thread limit",
            "input_tokens_est": 900,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 7000,
            "output_tokens_est": 300,
            "reasoning_tokens_est": "not exposed",
            "total_low": 6500,
            "total_expected": 8200,
            "total_high": 13000,
            "usage_object_available": "no",
            "notes": "Final precision check with raw, protection crop, and ATS zoom crops.",
        },
    ]
    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total_expected = sum(int(row["total_expected"]) for row in rows)
    with (RESULTS / "token_usage_summary.md").open("w", encoding="utf-8") as f:
        f.write(
            "# Token Usage Estimate\n\n"
            "No `OPENAI_API_KEY` was present, so the OpenAI Responses input-token counting endpoint could not be called, "
            "and subagent usage objects were not exposed by the local multi-agent tool. Estimates use prompt text length plus "
            "image-count/resolution heuristics for the submitted visual payloads.\n\n"
            f"Expected total tokens across identified document-5 calls: **{total_expected:,}**.\n"
        )


def validate(edges: list[tuple[str, str, str, str]], expected_count: int) -> None:
    node_set = set(NODES)
    if len(NODES) != len(node_set):
        duplicates = [node for node in NODES if NODES.count(node) > 1]
        raise ValueError(f"Duplicate nodes: {duplicates}")
    normalized = set()
    for a, b, *_ in edges:
        if a not in node_set:
            raise ValueError(f"Unknown source node: {a}")
        if b not in node_set:
            raise ValueError(f"Unknown target node: {b}")
        if a == b:
            raise ValueError(f"Self-loop not allowed here: {a}")
        normalized.add(normalize((a, b)))
    if len(normalized) != expected_count:
        raise ValueError(f"Expected {expected_count} unique edges, got {len(normalized)}")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    final_edges = [edge for edge in ROUND1_EDGES if (edge[0], edge[1]) not in DEMOTED_FINAL]

    validate(ROUND1_EDGES, 129)
    validate(final_edges, 125)

    round_specs = [
        ("diego_round1", ROUND1_EDGES),
        ("jennifer_round1", ROUND1_EDGES),
        ("diego_round2", final_edges),
        ("jennifer_round2_final", final_edges),
        ("final", final_edges),
    ]
    for name, edges in round_specs:
        write_matrix(RESULTS / f"{name}_connectivity_matrix.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", edges)
        write_edges(RESULTS / f"{name}_edges.csv", edges)

    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_edges)
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_lists()
    write_summaries(final_edges)
    write_token_estimates()

    print(f"nodes={len(NODES)}")
    print(f"round1_edges={len({normalize((a, b)) for a, b, _, _ in ROUND1_EDGES})}")
    print(f"final_edges={len({normalize((a, b)) for a, b, _, _ in final_edges})}")
    print(RESULTS)


if __name__ == "__main__":
    main()
