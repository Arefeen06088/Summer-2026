# Document 19 Connectivity Results

Final extraction used only files in `Raw + wires + junctions + OCR`. No Ground Truth, evaluator feedback, or off-the-shelf OCR was used.

## Final Consensus

- Final nodes in matrix: 201
- Final undirected edges: 200
- Matrix file: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`
- Agreement: Diego round 03 and Jennifer round 04 agree.

## Round Progression

- Round 01 Diego high recall: 202 proposed edges.
- Round 02 Jennifer precision: 200 kept edges.
- Round 03 Diego saturation: 200 edges with no changes from Jennifer.
- Round 04 Jennifer final: 200 confirmed final edges.

## Final Edge Counts By Kind

- ac_power: 5
- control: 24
- control_power: 4
- control_signal: 2
- dc_power: 6
- instrumentation_signal: 27
- power: 104
- protection_signal: 12
- signal: 12
- tie_power: 4

## Final Edge Counts By Confidence

- high: 188
- medium: 12

## Key Precision Decisions

- Preserved raw logical bus labels `BUS-4160-A/B`, `BUS-480-A/B`, `BUS-120AC-A/B`, and `BUS-125DC-A/B`.
- Corrected feeder transformer component labels from `PT-*` to `CPT-*` while retaining true bus instruments `PT-4160A` and `PT-4160B`.
- Corrected `LCS-MOV601` to `LS-MOV601`.
- Removed unsupported compact lower-area edges `BUS-125DC-A -- JB-MAIN` and `BUS-120AC-B -- CHGR-125B`.
- Kept `CONTROL_POWER_DC_DISTRIBUTION_HEADER` drops only where visibly landed.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
