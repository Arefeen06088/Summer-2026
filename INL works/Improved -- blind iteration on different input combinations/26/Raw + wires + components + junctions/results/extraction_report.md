# Document 26 Connectivity Extraction

## Scope

Only resources inside:

`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + components + junctions`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, validation metrics, prior result files, or off-the-shelf OCR outputs were used. Existing validation files in the results folder were not used as extraction evidence.

## Multi-Agent Rounds

1. Diego round 1: high-recall graph with 200 nodes and 209 plausible edges.
2. Jennifer round 2: removed six route-adjacent dashed control candidates, leaving 200 nodes and 203 edges.
3. Diego round 3: agreed with Jennifer's corrected set.
4. Jennifer round 4: confirmed saturation.

The raw title block visibly states 200 components and 209 connections. The agents treated that as a consistency clue only. The final precision graph keeps the 200 visible component/node tags and excludes six dashed route-adjacent candidates that do not visually land on the tagged endpoints.

## Final Result

- Final nodes: 200
- Final undirected edges: 203
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`

## Final Edges

- GEN-301 -- TR-UAT-31 (solid_power, high)
- TR-UAT-31 -- CB-4A-IN1 (solid_power, high)
- CB-4A-IN1 -- BUS-416A (solid_power, high)
- SAT-31A -- CB-4A-ST (solid_power, high)
- CB-4A-ST -- BUS-416A (solid_power, high)
- DG-31A -- CB-4A-DG (solid_power, high)
- CB-4A-DG -- BUS-416A (solid_power, high)
- BUS-416A -- CB-4A01 (solid_power, high)
- CB-4A01 -- TR-480A1 (solid_power, high)
- TR-480A1 -- CB-480A-IN (solid_power, high)
- CB-480A-IN -- BUS-480A (solid_ground, medium_high)
- BUS-416A -- CB-4A02 (solid_power, high)
- CB-4A02 -- TR-480A2 (solid_power, high)
- TR-480A2 -- CB-480A-ALT (solid_power, high)
- CB-480A-ALT -- BUS-480A (solid_ground, medium_high)
- BUS-416A -- CB-4A03 (solid_power, high)
- CB-4A03 -- DS-RCP-A (solid_power, high)
- DS-RCP-A -- MTR-RCP-A (solid_power, high)
- MTR-RCP-A -- GND-RCP-A (solid_ground, medium_high)
- BUS-416A -- CB-4A04 (solid_power, high)
- CB-4A04 -- DS-SW-A (solid_power, high)
- DS-SW-A -- PUMP-SW31A (solid_power, high)
- PUMP-SW31A -- GND-SW-A (solid_ground, medium_high)
- BUS-416A -- CB-4A05 (solid_power, high)
- CB-4A05 -- DS-AFW-A (solid_power, high)
- DS-AFW-A -- PUMP-AFW31A (solid_power, high)
- BUS-416A -- CB-4A06 (solid_power, high)
- CB-4A06 -- DS-CHW-A (solid_power, high)
- DS-CHW-A -- MTR-CHWP-A (solid_power, high)
- SAT-31B -- CB-4B-ST (solid_power, high)
- CB-4B-ST -- BUS-416B (solid_power, high)
- DG-31B -- CB-4B-DG (solid_power, high)
- CB-4B-DG -- BUS-416B (solid_power, high)
- BUS-416B -- CB-4B01 (solid_power, high)
- CB-4B01 -- TR-480B1 (solid_power, high)
- TR-480B1 -- CB-480B-IN (solid_power, high)
- CB-480B-IN -- BUS-480B (solid_ground, medium_high)
- BUS-416B -- CB-4B02 (solid_power, high)
- CB-4B02 -- TR-480B2 (solid_power, high)
- TR-480B2 -- CB-480B-ALT (solid_power, high)
- CB-480B-ALT -- BUS-480B (solid_ground, medium_high)
- BUS-416B -- CB-4B03 (solid_power, high)
- CB-4B03 -- DS-RCP-B (solid_power, high)
- DS-RCP-B -- MTR-RCP-B (solid_power, high)
- MTR-RCP-B -- GND-RCP-B (solid_ground, medium_high)
- BUS-416B -- CB-4B04 (solid_power, high)
- CB-4B04 -- DS-SW-B (solid_power, high)
- DS-SW-B -- PUMP-SW31B (solid_power, high)
- PUMP-SW31B -- GND-SW-B (solid_ground, medium_high)
- BUS-416B -- CB-4B05 (solid_power, high)
- CB-4B05 -- DS-AFW-B (solid_power, high)
- DS-AFW-B -- PUMP-AFW31B (solid_power, high)
- BUS-416B -- CB-4B06 (solid_power, high)
- CB-4B06 -- DS-CHW-B (solid_power, high)
- DS-CHW-B -- MTR-CHWP-B (solid_power, high)
- BUS-416A -- CB-4AB-TIE (solid_power, high)
- CB-4AB-TIE -- BUS-416B (solid_power, high)
- BUS-480A -- CB-480A11 (solid_power, high)
- CB-480A11 -- MCC-31A1 (solid_power, high)
- MCC-31A1 -- GND-MCC-A1 (solid_ground, medium_high)
- BUS-480A -- CB-480A12 (solid_power, high)
- CB-480A12 -- MCC-31A2 (solid_power, high)
- MCC-31A2 -- GND-MCC-A2 (solid_ground, medium_high)
- BUS-480A -- CB-480A13 (solid_power, high)
- CB-480A13 -- LC-31A3 (solid_power, high)
- BUS-480A -- CB-480A14 (solid_power, high)
- CB-480A14 -- PNL-31A4 (solid_power, high)
- MCC-31A1 -- STR-A1-1 (solid_power, high)
- STR-A1-1 -- JB-A1-01 (solid_power, high)
- JB-A1-01 -- PUMP-CVC-A (solid_power, high)
- MCC-31A1 -- STR-A1-2 (solid_power, high)
- STR-A1-2 -- JB-A1-02 (solid_power, high)
- JB-A1-02 -- MOV-RHR-731A (solid_power, high)
- MCC-31A1 -- STR-A1-3 (solid_power, high)
- STR-A1-3 -- JB-A1-03 (solid_power, high)
- JB-A1-03 -- FAN-CRD-A (solid_power, high)
- MCC-31A2 -- STR-A2-1 (solid_power, high)
- STR-A2-1 -- JB-A2-01 (solid_power, high)
- JB-A2-01 -- PUMP-CCW-A (solid_power, high)
- MCC-31A2 -- STR-A2-2 (solid_power, high)
- STR-A2-2 -- JB-A2-02 (solid_power, high)
- JB-A2-02 -- HTR-BORIC-A (solid_power, high)
- MCC-31A2 -- STR-A2-3 (solid_power, high)
- STR-A2-3 -- JB-A2-03 (solid_power, high)
- JB-A2-03 -- MOV-CHG-121A (solid_power, high)
- LC-31A3 -- STR-A3-1 (solid_power, high)
- STR-A3-1 -- JB-A3-01 (solid_power, high)
- JB-A3-01 -- MTR-SUMP-A (solid_power, high)
- LC-31A3 -- STR-A3-2 (solid_power, high)
- STR-A3-2 -- JB-A3-02 (solid_power, high)
- JB-A3-02 -- PUMP-LUBE-A (solid_power, high)
- LC-31A3 -- STR-A3-3 (solid_power, high)
- STR-A3-3 -- JB-A3-03 (solid_power, high)
- JB-A3-03 -- MOV-SI-902A (solid_power, high)
- PNL-31A4 -- STR-A4-1 (solid_power, high)
- STR-A4-1 -- JB-A4-01 (solid_power, high)
- JB-A4-01 -- FAN-CONT-A (solid_power, high)
- PNL-31A4 -- STR-A4-2 (solid_power, high)
- STR-A4-2 -- JB-A4-02 (solid_power, high)
- JB-A4-02 -- PUMP-SAMPLE-A (solid_power, high)
- PNL-31A4 -- STR-A4-3 (solid_power, high)
- STR-A4-3 -- JB-A4-03 (solid_power, high)
- JB-A4-03 -- MOV-VENT-406A (solid_power, high)
- BUS-480B -- CB-480B11 (solid_power, high)
- CB-480B11 -- MCC-31B1 (solid_power, high)
- MCC-31B1 -- GND-MCC-B1 (solid_ground, medium_high)
- BUS-480B -- CB-480B12 (solid_power, high)
- CB-480B12 -- MCC-31B2 (solid_power, high)
- MCC-31B2 -- GND-MCC-B2 (solid_ground, medium_high)
- BUS-480B -- CB-480B13 (solid_power, high)
- CB-480B13 -- LC-31B3 (solid_power, high)
- BUS-480B -- CB-480B14 (solid_power, high)
- CB-480B14 -- PNL-31B4 (solid_power, high)
- MCC-31B1 -- STR-B1-1 (solid_power, high)
- STR-B1-1 -- JB-B1-01 (solid_power, high)
- JB-B1-01 -- PUMP-CVC-B (solid_power, high)
- MCC-31B1 -- STR-B1-2 (solid_power, high)
- STR-B1-2 -- JB-B1-02 (solid_power, high)
- JB-B1-02 -- MOV-RHR-731B (solid_power, high)
- MCC-31B1 -- STR-B1-3 (solid_power, high)
- STR-B1-3 -- JB-B1-03 (solid_power, high)
- JB-B1-03 -- FAN-CRD-B (solid_power, high)
- MCC-31B2 -- STR-B2-1 (solid_power, high)
- STR-B2-1 -- JB-B2-01 (solid_power, high)
- JB-B2-01 -- PUMP-CCW-B (solid_power, high)
- MCC-31B2 -- STR-B2-2 (solid_power, high)
- STR-B2-2 -- JB-B2-02 (solid_power, high)
- JB-B2-02 -- HTR-BORIC-B (solid_power, high)
- MCC-31B2 -- STR-B2-3 (solid_power, high)
- STR-B2-3 -- JB-B2-03 (solid_power, high)
- JB-B2-03 -- MOV-CHG-121B (solid_power, high)
- LC-31B3 -- STR-B3-1 (solid_power, high)
- STR-B3-1 -- JB-B3-01 (solid_power, high)
- JB-B3-01 -- MTR-SUMP-B (solid_power, high)
- LC-31B3 -- STR-B3-2 (solid_power, high)
- STR-B3-2 -- JB-B3-02 (solid_power, high)
- JB-B3-02 -- PUMP-LUBE-B (solid_power, high)
- LC-31B3 -- STR-B3-3 (solid_power, high)
- STR-B3-3 -- JB-B3-03 (solid_power, high)
- JB-B3-03 -- MOV-SI-902B (solid_power, high)
- PNL-31B4 -- STR-B4-1 (solid_power, high)
- STR-B4-1 -- JB-B4-01 (solid_power, high)
- JB-B4-01 -- FAN-CONT-B (solid_power, high)
- PNL-31B4 -- STR-B4-2 (solid_power, high)
- STR-B4-2 -- JB-B4-02 (solid_power, high)
- JB-B4-02 -- PUMP-SAMPLE-B (solid_power, high)
- PNL-31B4 -- STR-B4-3 (solid_power, high)
- STR-B4-3 -- JB-B4-03 (solid_power, high)
- JB-B4-03 -- MOV-VENT-406B (solid_power, high)
- BUS-480A -- CB-480AB-TIE (solid_power, high)
- CB-480AB-TIE -- BUS-480B (solid_power, high)
- BUS-125DCA -- CB-DCAB-TIE (solid_dc, high)
- CB-DCAB-TIE -- BUS-125DCB (solid_dc, high)
- BAT-31A -- DS-BAT-A (solid_dc, high)
- DS-BAT-A -- BUS-125DCA (solid_dc, high)
- CHG-31A -- CB-CHG-A (solid_dc, high)
- CB-CHG-A -- BUS-125DCA (solid_dc, high)
- BUS-125DCA -- PNL-DC-A (solid_dc, high)
- BUS-125DCA -- CB-INV-A (solid_dc, high)
- CB-INV-A -- INV-31A (solid_dc, high)
- INV-31A -- BUS-INV-A (solid_ac, high)
- BUS-INV-A -- PNL-AC-A (solid_ac, high)
- PNL-AC-A -- BUS-120N-A (solid_ac, high)
- BUS-INV-A -- RPS-PNL-A (solid_ac, high)
- RPS-PNL-A -- TB-UPS-A (dashed_control, medium_high)
- BUS-120N-A -- RELAY-K7A1 (solid_ac, high)
- RELAY-K7A1 -- TB-RPS-A1 (dotted_instrument, medium_high)
- TB-RPS-A1 -- PT-31A1 (dotted_instrument, high)
- BUS-120N-A -- RELAY-K7A2 (solid_ac, high)
- RELAY-K7A2 -- TB-RPS-A2 (dotted_instrument, medium_high)
- TB-RPS-A2 -- PT-31A2 (dotted_instrument, high)
- BUS-120N-A -- RELAY-K7A3 (solid_ac, high)
- RELAY-K7A3 -- TB-RPS-A3 (dotted_instrument, medium_high)
- TB-RPS-A3 -- PT-31A3 (dotted_instrument, high)
- BUS-120N-A -- RELAY-K7A4 (solid_ac, high)
- RELAY-K7A4 -- TB-RPS-A4 (dotted_instrument, medium_high)
- TB-RPS-A4 -- PT-31A4 (dotted_instrument, high)
- BAT-31B -- DS-BAT-B (solid_dc, high)
- DS-BAT-B -- BUS-125DCB (solid_dc, high)
- CHG-31B -- CB-CHG-B (solid_dc, high)
- CB-CHG-B -- BUS-125DCB (solid_dc, high)
- BUS-125DCB -- PNL-DC-B (solid_dc, high)
- BUS-125DCB -- CB-INV-B (solid_dc, high)
- CB-INV-B -- INV-31B (solid_dc, high)
- INV-31B -- BUS-INV-B (solid_ac, high)
- BUS-INV-B -- PNL-AC-B (solid_ac, high)
- PNL-AC-B -- BUS-120N-B (solid_ac, high)
- BUS-INV-B -- RPS-PNL-B (solid_ac, high)
- RPS-PNL-B -- TB-UPS-B (dashed_control, medium_high)
- BUS-120N-B -- RELAY-K7B1 (solid_ac, high)
- RELAY-K7B1 -- TB-RPS-B1 (dotted_instrument, medium_high)
- TB-RPS-B1 -- PT-31B1 (dotted_instrument, high)
- BUS-120N-B -- RELAY-K7B2 (solid_ac, high)
- RELAY-K7B2 -- TB-RPS-B2 (dotted_instrument, medium_high)
- TB-RPS-B2 -- PT-31B2 (dotted_instrument, high)
- BUS-120N-B -- RELAY-K7B3 (solid_ac, high)
- RELAY-K7B3 -- TB-RPS-B3 (dotted_instrument, medium_high)
- TB-RPS-B3 -- PT-31B3 (dotted_instrument, high)
- BUS-120N-B -- RELAY-K7B4 (solid_ac, high)
- RELAY-K7B4 -- TB-RPS-B4 (dotted_instrument, medium_high)
- TB-RPS-B4 -- PT-31B4 (dotted_instrument, high)
- CB-480A13 -- STR-A3-3 (dashed_control, medium)
- CB-480B13 -- STR-B3-3 (dashed_control, medium)

## Excluded Or Ambiguous Items

- CB-4A03--MTR-RCP-A: removed in Jennifer/Diego convergence: dashed route is adjacent to RCP branch, not landed on motor
- CB-4B03--MTR-RCP-B: removed in Jennifer/Diego convergence: dashed route is adjacent to RCP branch, not landed on motor
- STR-A1-1--MOV-RHR-731A: removed in Jennifer/Diego convergence: dashed route is adjacent to RHR branch
- STR-B1-1--MOV-RHR-731B: removed in Jennifer/Diego convergence: dashed route is adjacent to RHR branch
- STR-A3-3--MOV-SI-902A: removed in Jennifer/Diego convergence: dashed route is adjacent to SI branch
- STR-B3-3--MOV-SI-902B: removed in Jennifer/Diego convergence: dashed route is adjacent to SI branch
- RPS-PNL-A--BUS-120N-A: not added: RPS panel has no visible solid downlead to 120N bus
- RPS-PNL-B--BUS-120N-B: not added: RPS panel has no visible solid downlead to 120N bus
- wire tag labels: excluded as cable/wire labels, not component or logical-node names

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: 102450
- Estimated total expected: 116860
- Estimated total high: 136690
- Estimated image/file input tokens: 47500

Detailed estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
