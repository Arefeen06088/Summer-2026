# Document 38 Connectivity Extraction

## Scope

Only resources inside:

`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + components + junctions`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, validation metrics, or off-the-shelf OCR outputs were used. Existing validation files in the results folder were not used as extraction evidence.

## Multi-Agent Rounds

1. Diego round 1: high-recall graph with plausible label/path/ground nodes retained.
2. Jennifer round 2: precision graph; removed label/path/ground nodes and unsupported A-side CPT output edge.
3. Diego round 3: agreed with Jennifer unchanged.
4. Jennifer round 4: confirmed saturation unchanged.

## Final Result

- Final nodes: 54
- Final undirected edges: 55
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`

## Final Edges

- GEN-U2A -- CB-101 (solid_power, high)
- CB-101 -- TR-UAT-2A (solid_power, high)
- TR-UAT-2A -- BUS-4160A (solid_power, high)
- DG-2A -- CB-103 (solid_power, high)
- CB-103 -- BUS-4160A (solid_power, high)
- BUS-4160A -- CB-105 (solid_power, high)
- CB-105 -- BUS-4160B (solid_power, high)
- TR-SUT-2B -- CB-102 (solid_power, high)
- CB-102 -- BUS-4160B (solid_power, high)
- DG-2B -- CB-104 (solid_power, high)
- CB-104 -- BUS-4160B (solid_power, high)
- BUS-4160A -- CB-201A (solid_power, high)
- CB-201A -- TR-201A (solid_power, high)
- TR-201A -- CB-301A (solid_power, high)
- CB-301A -- BUS-480A (solid_power, high)
- BUS-480A -- CB-401A (solid_power, high)
- CB-401A -- MCC-2A1 (solid_power, high)
- BUS-480A -- TR-CPT-A (solid_power, high)
- BUS-480A -- CHGR-2A (solid_power, medium_high)
- MCC-2A1 -- PUMP-RHR2A (solid_power, high)
- MCC-2A1 -- PUMP-CCW2A (solid_power, high)
- MCC-2A1 -- PUMP-SW2A (solid_power, high)
- MCC-2A1 -- FAN-CR2A (solid_power, high)
- MCC-2A1 -- MOV-RHR141A (solid_power, high)
- MCC-2A1 -- MOV-SI221A (solid_power, high)
- CHGR-2A -- BUS-125VDC-TRAIN-A (solid_dc, high)
- BAT-125A/S-125DC-A -- BUS-125VDC-TRAIN-A (solid_dc, high)
- BUS-125VDC-TRAIN-A -- INV-2A (solid_dc, high)
- INV-2A -- BUS-120AC-A (solid_ac, high)
- BUS-120AC-A -- RPS-PNL-A (solid_ac, high)
- BUS-125VDC-TRAIN-A -- RELAY-86A (dashed_control, medium)
- RPS-PNL-A -- RELAY-27A (dashed_control, medium)
- BUS-4160B -- CB-201B (solid_power, high)
- CB-201B -- TR-201B (solid_power, high)
- TR-201B -- CB-301B (solid_power, high)
- CB-301B -- BUS-480B (solid_power, high)
- BUS-480B -- CB-401B (solid_power, high)
- CB-401B -- MCC-2B1 (solid_power, high)
- BUS-480B -- TR-CPT-B (solid_power, high)
- BUS-480B -- CHGR-2B (solid_power, medium_high)
- MCC-2B1 -- PUMP-RHR2B (solid_power, high)
- MCC-2B1 -- PUMP-CCW2B (solid_power, high)
- MCC-2B1 -- PUMP-SW2B (solid_power, high)
- MCC-2B1 -- FAN-CR2B (solid_power, high)
- MCC-2B1 -- MOV-RHR142B (solid_power, high)
- MCC-2B1 -- MOV-SI222B (solid_power, high)
- CHGR-2B -- BUS-125VDC-TRAIN-B (solid_dc, high)
- BAT-125B/S-125DC-B -- BUS-125VDC-TRAIN-B (solid_dc, high)
- BUS-125VDC-TRAIN-B -- INV-2B (solid_dc, high)
- INV-2B -- BUS-120AC-B (solid_ac, high)
- TR-CPT-B -- BUS-120AC-B (solid_ac, high)
- BUS-120AC-B -- RPS-PNL-B (solid_ac, high)
- BUS-125VDC-TRAIN-B -- RELAY-86B (dashed_control, medium)
- BUS-120AC-B -- RELAY-27B (solid_control, medium_high)
- RPS-PNL-B -- RELAY-27B (dashed_control, medium)

## Excluded Or Collapsed Items

- UNIT_MAIN_GENERATOR_LABEL: source/context text, not a component node
- STARTUP_AUX_XFMR_SOURCE_LABEL: source/context text, not a component node
- TO_UNIT_AUX_BUS_CONT_LABEL: continuation box text without a clear terminal in this sheet
- TO_STATION_YARD_CONT_LABEL: continuation box text without a clear terminal in this sheet
- A_CONTROL_CABLES_2A-C72_2A-C86: dashed cable path labels/callouts, not equipment nodes
- B_CONTROL_CABLES_2B-C72_2B-C86: dashed cable path labels/callouts, not equipment nodes
- GND-STA: station-ground reference on dotted/dashed indication; excluded from component connectivity
- TR-CPT-A--BUS-120AC-A: A-side CPT output visually terminates and does not join BUS-120AC-A
- RELAY-86A--RPS-PNL-A: no direct visual termination from relay to panel
- RELAY-86B--RPS-PNL-B: no direct visual termination from relay to panel
- BUS-120AC-A--RELAY-27A: not visibly connected; only RPS-PNL-A dashed connection retained

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: 69070
- Estimated total expected: 78240
- Estimated total high: 92130
- Estimated image/file input tokens: 23500

Detailed estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
