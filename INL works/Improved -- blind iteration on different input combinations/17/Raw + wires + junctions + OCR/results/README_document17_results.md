# Document 17 Connectivity Results

Final extraction used only files in `Raw + wires + junctions + OCR`. No Ground Truth, evaluator feedback, or off-the-shelf OCR was used.

## Final Consensus

- Final nodes in matrix: 196
- Final undirected edges: 193
- Matrix file: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`
- Agreement: Diego round 03 and Jennifer round 04 agree.

## Round Progression

- Round 01 Diego high recall: 223 normalized proposed edges.
- Round 02 Jennifer precision: 191 kept edges.
- Round 03 Diego saturation: 193 edges after adding two corrected ESF-panel-to-RPS-relay edges.
- Round 04 Jennifer final: 193 confirmed final edges.

## Final Edge Counts By Kind

- control_power: 2
- control_signal: 17
- ground: 12
- instrument_tap: 6
- power: 136
- terminal_continuation: 14
- tie: 6

## Final Edge Counts By Confidence

- high: 157
- low: 6
- medium: 30

## Key Precision Decisions

- Normalized top buses to raw labels `BUS-4160-A` and `BUS-4160-B`.
- Normalized inverter buses to raw labels `BUS-120AC-A` and `BUS-120AC-B`.
- Kept ties only through breakers: `CB-TIE-4AB`, `CB-TIE-480AB`, and `CB-DCTIE-AB`.
- Dropped unsupported long dashed lower-control corridor overconnections.
- Added corrected final edges `PNL-ESF-A -- RELAY-RPS-A` and `PNL-ESF-B -- RELAY-RPS-B`.
- Kept visible isolated `MASTER-TERMINAL-BLOCKS` as a node with no final retained edges.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
