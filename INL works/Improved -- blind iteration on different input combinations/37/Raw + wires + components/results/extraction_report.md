# Document 37 Connectivity Extraction

Final saturated result from Diego and Jennifer, using only Input resources/raw and derived visual aids.

- Final nodes: 53
- Final edges: 55
- High-confidence edges: 52
- Medium-confidence edges: 3
- Excluded ground/reference labels: GND-01A, GND-01B
- GT/validation/feedback files: not used
- Off-the-shelf OCR: not used

## Final Medium-Confidence Edges

- RELAY-K12B -- PLC-ESF: dashed C05 routed to PLC-ESF/ESF logic area
- PAN-RPS-A -- INST-RACK-A: dashed C03 functional route
- PLC-ESF -- PAN-RPS-B: dashed C06 functional route

## Token Usage Estimate

Actual OpenAI usage objects and Responses input-token counting were unavailable because no API key or usage-returning model-call interface was available in this environment.

- Low estimate: 185500
- Expected estimate: 189090
- High estimate: 194360

Local estimate method: text tokens are approximated as characters/4; image/file input tokens use 85 + 170 * ceil(width/512) * ceil(height/512) per image crop.

## Main Output Files

- final_connectivity_matrix.csv
- final_edges.csv
- final_node_order.csv
- round_01_diego_matrix.csv through round_04_jennifer_final_matrix.csv
- token_usage_estimate.csv
- token_usage_summary.csv/json
- uncertain_or_excluded_edges.csv
