# Document 15 Connectivity Extraction

## Scope

Only resources inside:

`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires + components + junctions`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, validation metrics, prior result files, or off-the-shelf OCR outputs were used. Existing validation files in the results folder were not used as extraction evidence.

## Multi-Agent Rounds

1. Diego round 1: high-recall graph with 183 nodes and 196 plausible edges.
2. Jennifer round 2: removed the two NSS-to-DG proximity edges.
3. Diego round 3: selected Option B; removed four local dashed breaker-to-breaker context edges and retained ground edges.
4. Jennifer round 4: confirmed saturation at Diego round 3 Option B.

## Final Result

- Final nodes: 183
- Final undirected edges: 190
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`
- Visible raw-sheet drafting QC: 183 nodes / 190 connections.

## Final Edges

- GEN-101 -- CB-GEN-101 (solid_power, high)
- CB-GEN-101 -- TR-GSU-1 (solid_power, high)
- TR-GSU-1 -- BUS-SWY-1 (solid_power, high)
- BUS-SWY-1 -- CB-SWY-TIE (solid_power, high)
- CB-SWY-TIE -- BUS-SWY-2 (solid_power, high)
- GEN-102 -- CB-GEN-102 (solid_power, high)
- CB-GEN-102 -- TR-GSU-2 (solid_power, high)
- TR-GSU-2 -- BUS-SWY-2 (solid_power, high)
- BUS-SWY-1 -- TR-UAT-1 (solid_power, high)
- TR-UAT-1 -- BUS-NSS-1 (solid_power, high)
- BUS-SWY-1 -- TR-SAT-1 (solid_power, high)
- TR-SAT-1 -- BUS-NSS-1 (solid_power, high)
- BUS-SWY-2 -- TR-UAT-2 (solid_power, high)
- TR-UAT-2 -- BUS-NSS-2 (solid_power, high)
- BUS-SWY-2 -- TR-SAT-2 (solid_power, high)
- TR-SAT-2 -- BUS-NSS-2 (solid_power, high)
- BUS-NSS-1 -- CB-NF-A (solid_power, high)
- DG-1A -- CB-DG-A (solid_power, high)
- CB-NF-A -- BUS-416A (solid_power, high)
- CB-DG-A -- BUS-416A (solid_power, high)
- BUS-NSS-1 -- CB-NF-B (solid_power, high)
- DG-1B -- CB-DG-B (solid_power, high)
- CB-NF-B -- BUS-416B (solid_power, high)
- CB-DG-B -- BUS-416B (solid_power, high)
- BUS-NSS-2 -- CB-NF-C (solid_power, high)
- DG-1C -- CB-DG-C (solid_power, high)
- CB-NF-C -- BUS-416C (solid_power, high)
- CB-DG-C -- BUS-416C (solid_power, high)
- BUS-NSS-2 -- CB-NF-D (solid_power, high)
- DG-1D -- CB-DG-D (solid_power, high)
- CB-NF-D -- BUS-416D (solid_power, high)
- CB-DG-D -- BUS-416D (solid_power, high)
- BUS-416A -- CB-TX-A (solid_power, high)
- CB-TX-A -- TR-480A (solid_power, high)
- TR-480A -- BUS-480A (solid_power, high)
- BUS-480A -- MCC-1A (solid_power, high)
- BUS-416B -- CB-TX-B (solid_power, high)
- CB-TX-B -- TR-480B (solid_power, high)
- TR-480B -- BUS-480B (solid_power, high)
- BUS-480B -- MCC-1B (solid_power, high)
- BUS-416C -- CB-TX-C (solid_power, high)
- CB-TX-C -- TR-480C (solid_power, high)
- TR-480C -- BUS-480C (solid_power, high)
- BUS-480C -- MCC-1C (solid_power, high)
- BUS-416D -- CB-TX-D (solid_power, high)
- CB-TX-D -- TR-480D (solid_power, high)
- TR-480D -- BUS-480D (solid_power, high)
- BUS-480D -- MCC-1D (solid_power, high)
- BUS-416A -- CB-TIE-AB (solid_power, high)
- CB-TIE-AB -- DS-TIE-AB (solid_power, high)
- DS-TIE-AB -- BUS-416B (solid_power, high)
- BUS-416C -- CB-TIE-CD (solid_power, high)
- CB-TIE-CD -- DS-TIE-CD (solid_power, high)
- DS-TIE-CD -- BUS-416D (solid_power, high)
- CB-DG-A -- SEQ-1AB (dashed_control, high)
- CB-NF-B -- SEQ-1AB (dashed_control, high)
- CB-DG-A -- RPS-AC-1 (dashed_control, high)
- CB-NF-B -- RPS-AC-1 (dashed_control, high)
- CB-DG-C -- SEQ-2CD (dashed_control, high)
- CB-NF-D -- SEQ-2CD (dashed_control, high)
- CB-DG-C -- RPS-AC-2 (dashed_control, high)
- CB-NF-D -- RPS-AC-2 (dashed_control, high)
- MCC-1A -- CB-A01 (solid_power, high)
- CB-A01 -- DS-A01 (solid_power, high)
- DS-A01 -- PMP-SI-A1 (solid_power, high)
- CB-A01 -- RLY-A01 (dashed_control, medium_high)
- MCC-1A -- CB-A02 (solid_power, high)
- CB-A02 -- FU-A02 (solid_power, high)
- FU-A02 -- PMP-CS-A2 (solid_power, high)
- CB-A02 -- RLY-A02 (dashed_control, medium_high)
- MCC-1A -- CB-A03 (solid_power, high)
- CB-A03 -- DS-A03 (solid_power, high)
- DS-A03 -- MOV-A03 (solid_power, high)
- CB-A03 -- RLY-A03 (dashed_control, medium_high)
- MCC-1A -- CB-A04 (solid_power, high)
- CB-A04 -- FU-A04 (solid_power, high)
- FU-A04 -- MTR-A04 (solid_power, high)
- CB-A04 -- RLY-A04 (dashed_control, medium_high)
- MCC-1A -- CB-A05 (solid_power, high)
- CB-A05 -- DS-A05 (solid_power, high)
- DS-A05 -- INST-A05 (solid_power, high)
- CB-A05 -- RLY-A05 (dashed_control, medium_high)
- MCC-1A -- CB-A06 (solid_power, high)
- CB-A06 -- FU-A06 (solid_power, high)
- FU-A06 -- PMP-SW-A6 (solid_power, high)
- CB-A06 -- RLY-A06 (dashed_control, medium_high)
- RLY-A06 -- TB-1A (dashed_control, medium_high)
- BAT-125A -- CHG-1A (dashed_control, medium_high)
- CHG-1A -- BUS-DC-A (dashed_control, medium_high)
- BUS-DC-A -- INV-1A (dashed_control, medium_high)
- INV-1A -- CP-1A (dashed_control, medium_high)
- CP-1A -- TB-1A (dashed_control, medium_high)
- CP-1A -- JB-1A (dashed_control, medium_high)
- BUS-DC-A -- GND-A (dashed_control, medium)
- MCC-1B -- CB-B01 (solid_power, high)
- CB-B01 -- DS-B01 (solid_power, high)
- DS-B01 -- PMP-SI-B1 (solid_power, high)
- CB-B01 -- RLY-B01 (dashed_control, medium_high)
- MCC-1B -- CB-B02 (solid_power, high)
- CB-B02 -- FU-B02 (solid_power, high)
- FU-B02 -- PMP-CS-B2 (solid_power, high)
- CB-B02 -- RLY-B02 (dashed_control, medium_high)
- MCC-1B -- CB-B03 (solid_power, high)
- CB-B03 -- DS-B03 (solid_power, high)
- DS-B03 -- MOV-B03 (solid_power, high)
- CB-B03 -- RLY-B03 (dashed_control, medium_high)
- MCC-1B -- CB-B04 (solid_power, high)
- CB-B04 -- FU-B04 (solid_power, high)
- FU-B04 -- MTR-B04 (solid_power, high)
- CB-B04 -- RLY-B04 (dashed_control, medium_high)
- MCC-1B -- CB-B05 (solid_power, high)
- CB-B05 -- DS-B05 (solid_power, high)
- DS-B05 -- INST-B05 (solid_power, high)
- CB-B05 -- RLY-B05 (dashed_control, medium_high)
- MCC-1B -- CB-B06 (solid_power, high)
- CB-B06 -- FU-B06 (solid_power, high)
- FU-B06 -- PMP-SW-B6 (solid_power, high)
- CB-B06 -- RLY-B06 (dashed_control, medium_high)
- RLY-B06 -- TB-1B (dashed_control, medium_high)
- BAT-125B -- CHG-1B (dashed_control, medium_high)
- CHG-1B -- BUS-DC-B (dashed_control, medium_high)
- BUS-DC-B -- INV-1B (dashed_control, medium_high)
- INV-1B -- CP-1B (dashed_control, medium_high)
- CP-1B -- TB-1B (dashed_control, medium_high)
- CP-1B -- JB-1B (dashed_control, medium_high)
- BUS-DC-B -- GND-B (dashed_control, medium)
- MCC-1C -- CB-C01 (solid_power, high)
- CB-C01 -- DS-C01 (solid_power, high)
- DS-C01 -- PMP-SI-C1 (solid_power, high)
- CB-C01 -- RLY-C01 (dashed_control, medium_high)
- MCC-1C -- CB-C02 (solid_power, high)
- CB-C02 -- FU-C02 (solid_power, high)
- FU-C02 -- PMP-CS-C2 (solid_power, high)
- CB-C02 -- RLY-C02 (dashed_control, medium_high)
- MCC-1C -- CB-C03 (solid_power, high)
- CB-C03 -- DS-C03 (solid_power, high)
- DS-C03 -- MOV-C03 (solid_power, high)
- CB-C03 -- RLY-C03 (dashed_control, medium_high)
- MCC-1C -- CB-C04 (solid_power, high)
- CB-C04 -- FU-C04 (solid_power, high)
- FU-C04 -- MTR-C04 (solid_power, high)
- CB-C04 -- RLY-C04 (dashed_control, medium_high)
- MCC-1C -- CB-C05 (solid_power, high)
- CB-C05 -- DS-C05 (solid_power, high)
- DS-C05 -- INST-C05 (solid_power, high)
- CB-C05 -- RLY-C05 (dashed_control, medium_high)
- MCC-1C -- CB-C06 (solid_power, high)
- CB-C06 -- FU-C06 (solid_power, high)
- FU-C06 -- PMP-SW-C6 (solid_power, high)
- CB-C06 -- RLY-C06 (dashed_control, medium_high)
- RLY-C06 -- TB-1C (dashed_control, medium_high)
- BAT-125C -- CHG-1C (dashed_control, medium_high)
- CHG-1C -- BUS-DC-C (dashed_control, medium_high)
- BUS-DC-C -- INV-1C (dashed_control, medium_high)
- INV-1C -- CP-1C (dashed_control, medium_high)
- CP-1C -- TB-1C (dashed_control, medium_high)
- CP-1C -- JB-1C (dashed_control, medium_high)
- BUS-DC-C -- GND-C (dashed_control, medium)
- MCC-1D -- CB-D01 (solid_power, high)
- CB-D01 -- DS-D01 (solid_power, high)
- DS-D01 -- PMP-SI-D1 (solid_power, high)
- CB-D01 -- RLY-D01 (dashed_control, medium_high)
- MCC-1D -- CB-D02 (solid_power, high)
- CB-D02 -- FU-D02 (solid_power, high)
- FU-D02 -- PMP-CS-D2 (solid_power, high)
- CB-D02 -- RLY-D02 (dashed_control, medium_high)
- MCC-1D -- CB-D03 (solid_power, high)
- CB-D03 -- DS-D03 (solid_power, high)
- DS-D03 -- MOV-D03 (solid_power, high)
- CB-D03 -- RLY-D03 (dashed_control, medium_high)
- MCC-1D -- CB-D04 (solid_power, high)
- CB-D04 -- FU-D04 (solid_power, high)
- FU-D04 -- MTR-D04 (solid_power, high)
- CB-D04 -- RLY-D04 (dashed_control, medium_high)
- MCC-1D -- CB-D05 (solid_power, high)
- CB-D05 -- DS-D05 (solid_power, high)
- DS-D05 -- INST-D05 (solid_power, high)
- CB-D05 -- RLY-D05 (dashed_control, medium_high)
- MCC-1D -- CB-D06 (solid_power, high)
- CB-D06 -- FU-D06 (solid_power, high)
- FU-D06 -- PMP-SW-D6 (solid_power, high)
- CB-D06 -- RLY-D06 (dashed_control, medium_high)
- RLY-D06 -- TB-1D (dashed_control, medium_high)
- BAT-125D -- CHG-1D (dashed_control, medium_high)
- CHG-1D -- BUS-DC-D (dashed_control, medium_high)
- BUS-DC-D -- INV-1D (dashed_control, medium_high)
- INV-1D -- CP-1D (dashed_control, medium_high)
- CP-1D -- TB-1D (dashed_control, medium_high)
- CP-1D -- JB-1D (dashed_control, medium_high)
- BUS-DC-D -- GND-D (dashed_control, medium)

## Excluded Or Collapsed Items

- BUS-NSS-1--DG-1A: removed as proximity/overlap; diesel source clearly connects to CB-DG-A
- BUS-NSS-2--DG-1C: removed as proximity/overlap; diesel source clearly connects to CB-DG-C
- CB-NF-A--CB-DG-A: removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing
- CB-NF-B--CB-DG-B: removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing
- CB-NF-C--CB-DG-C: removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing
- CB-NF-D--CB-DG-D: removed as offset/context dashed control-trip lead without clean terminal-to-terminal landing
- BUS-416A--BUS-416B: not added directly; normally-open tie passes through CB-TIE-AB and DS-TIE-AB
- BUS-416C--BUS-416D: not added directly; normally-open tie passes through CB-TIE-CD and DS-TIE-CD

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: 83470
- Estimated total expected: 96660
- Estimated total high: 115050
- Estimated image/file input tokens: 29500

Detailed estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
