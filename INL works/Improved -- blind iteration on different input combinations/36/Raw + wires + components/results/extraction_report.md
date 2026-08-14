# Document 36 Connectivity Extraction Report

Resources used: raw schematic plus wire/component overlays and visual crops. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Saturated Decision

The final matrix uses Jennifer's conservative correction confirmed by Diego: tap labels (`SU-*`, `EDG-*`, `LC-*`) and state/routing labels (`TIE OPEN`, `RPS LOCKOUT`, `RPS TRIP`) are not standalone nodes. The visual `CB-4K-TIE` label is retained. Generic MOV actuator boxes are folded into the labeled valve nodes. Lower dashed ESF trunk routes are kept uncertain/excluded rather than promoted to binary edges.

## Final Counts

- Nodes: 55
- Edges: 55

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
