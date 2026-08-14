# Document 18 Connectivity Results

Final extraction used only files in `Raw + wires + junctions + OCR`. No Ground Truth, evaluator feedback, or off-the-shelf OCR was used.

## Final Consensus

- Final nodes in matrix: 201
- Final undirected edges: 193
- Matrix file: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`
- Agreement: Diego round 03 and Jennifer round 04 agree.

## Round Progression

- Round 01 Diego high recall: 204 proposed edges.
- Round 02 Jennifer precision: 193 kept edges.
- Round 03 Diego saturation: 193 edges with no changes from Jennifer.
- Round 04 Jennifer final: 193 confirmed final edges.

## Final Edge Counts By Kind

- ac_control_power: 6
- bus_tie: 2
- dc_control_power: 12
- grounding: 4
- instrumentation_control: 10
- power_480_feeder: 120
- power_primary_230_4160: 19
- power_transformer_infeed: 12
- rps_dashed_control: 8

## Final Edge Counts By Confidence

- high: 185
- medium: 8

## Key Precision Decisions

- Normalized the source bus label to `BB-SWYD-230`.
- Rejected unsupported intermediate `CB-SWYD-230`.
- Normalized `BUS-GEN-TERMINAL` to `GEN-MAIN-1-TERMINAL`.
- Dropped unsupported `CB-UAT-A/B -- BUS-4160B` edges.
- Kept limited logical `RPS-A-DASHED-NET` and `RPS-B-DASHED-NET` nodes for clearly landed PLC/JB/annunciator dashed endpoints.
- Dropped relay dashed-net memberships without unambiguous landed terminals.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
