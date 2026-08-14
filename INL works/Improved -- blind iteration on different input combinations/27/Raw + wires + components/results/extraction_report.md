# Document 27 Connectivity Extraction Report

Resources used: raw schematic plus wire/component overlays and visual crops under Input resources/results visual crops. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Saturated Decision

The final matrix uses Jennifer's conservative correction: CHGR-125A/B are fed by direct BUS-480-A/B taps, not by DS-A10 or DS-B01. BAT-125A/B are connected to their chargers, and the chargers connect to the labeled DC bus taps. The A and B DC bus labels sit on a continuous horizontal span; the main control panel tap is represented once, through DC-BUS-125A plus the DC-BUS-125A to DC-BUS-125B span.

Round 3 Diego agreed with the Round 2 corrections and added no further changes. Round 4 Jennifer confirmed saturation. The residual Medium-confidence edges are listed in uncertain_or_excluded_edges.csv and the saturation note.

## Final Counts

- Nodes: 200
- Edges: 201

## Output Files

- round_01_diego_edges.csv / round_01_diego_matrix.csv
- round_02_jennifer_edges.csv / round_02_jennifer_matrix.csv
- round_03_diego_edges.csv / round_03_diego_matrix.csv
- round_03_diego_reconciliation.md
- round_04_jennifer_final_edges.csv / round_04_jennifer_final_matrix.csv
- round_04_jennifer_final_saturation_check.md
- final_edges.csv / final_connectivity_matrix.csv
- uncertain_or_excluded_edges.csv
- token_usage_estimate.csv / token_usage_summary.csv / token_usage_summary.json
