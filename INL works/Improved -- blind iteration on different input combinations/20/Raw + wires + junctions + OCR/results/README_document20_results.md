# Document 20 Connectivity Extraction

This folder contains the saturated Diego/Jennifer extraction for document 20.

## Final Files

- `final_connectivity_matrix.csv`: final saturated matrix, 200 nodes by 200 nodes.
- `connectivity_matrix.csv`: copy of the final matrix for downstream consumers.
- `final_connectivity_edges.csv`: final saturated edge list.
- `nodes.csv`: final matrix node order and node kind.
- `round_*_matrix.csv`: per-round matrices. Round 01 includes the high-recall-only rejected logical nodes; later rounds do not.

## Round Progression

- Round 01 Diego high recall: 205 proposed edges.
- Round 02 Jennifer precision: 202 edges after 4 removals and 1 replacement edge.
- Round 03 Diego saturation: 202 edges with no changes from Jennifer.
- Round 04 Jennifer final: 202 confirmed final edges.

## Final Edge Counts By Kind

- control: 41
- dc: 12
- ground: 2
- instrument_signal: 8
- power: 139

## Final Edge Counts By Confidence

- high: 195
- medium: 7

## Key Precision Decisions

- Removed unsupported `UPS-A AC OUTPUT` and `UPS-B AC OUTPUT` logical stubs.
- Treated `A/B ESF INTERLOCK` as a conductor label, not a matrix node; retained direct `RELAY-K106 -- RELAY-K108`.
- Kept 480 VAC-to-rectifier AC feeds as medium confidence where no separate breaker label is visible.
- Kept seven residual medium-confidence edges documented in `round_04_jennifer_final_notes.md`.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
