# Document 38 Connectivity Extraction Report

Resources used: raw schematic plus wire/component overlays and visual crops. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Saturated Decision

The final matrix follows Jennifer's conservative correction confirmed by Diego: off-page labels, source labels, feeder IDs, dashed risers, enclosures, tables, and imprecise dashed relay/control relationships are excluded from the binary topology. Feeder labels are folded into direct MCC-to-load edges. `S-125DC-A/B` and `125 VDC TRAIN A/B` are represented as `BUS-125VDC-A/B`.

## Final Counts

- Nodes: 52
- Edges: 53

## Output Files

- round_01_diego_edges.csv / round_01_diego_matrix.csv
- round_02_jennifer_edges.csv / round_02_jennifer_matrix.csv
- round_03_diego_edges.csv / round_03_diego_matrix.csv
- round_04_jennifer_final_edges.csv / round_04_jennifer_final_matrix.csv
- final_edges.csv / final_connectivity_matrix.csv
- uncertain_or_excluded_edges.csv
- token_usage_estimate.csv / token_usage_summary.csv / token_usage_summary.json
