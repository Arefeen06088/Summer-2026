# Document 21 Connectivity Extraction

This folder contains the saturated Diego/Jennifer extraction for document 21.

## Final Files

- `final_connectivity_matrix.csv`: final saturated matrix.
- `connectivity_matrix.csv`: copy of the final matrix for downstream consumers.
- `final_connectivity_edges.csv`: final saturated edge list.
- `nodes.csv`: final matrix node order and node kind.
- `round_*_matrix.csv`: per-round matrices. Round 01 includes the high-recall-only rejected riser node.

## Round Progression

- Round 01 Diego high recall: 208 proposed edges.
- Round 02 Jennifer precision: 202 edges after 7 removals and 1 replacement edge.
- Round 03 Diego saturation: 202 edges with no changes from Jennifer.
- Round 04 Jennifer final: 202 confirmed final edges.

## Final Edge Counts By Kind

- control_interlock: 58
- ground: 6
- instrument_signal: 15
- normally_open_tie: 1
- power_feeder: 122

## Final Edge Counts By Confidence

- high: 186
- medium: 16

## Key Precision Decisions

- Removed `4KV_SWITCHGEAR_LEFT_RISER` to avoid overconnecting four 4.16 kV buses.
- Added direct `BUS-201A -- CB-301A` replacement for the visible feeder.
- Removed low-confidence `BUS-501A -- CP-CRD` and `BUS-501B -- CP-CRD`.
- Kept raw-only supported nodes `CB-204A`, `CB-204B`, and `DS-401B`.

## Token Accounting

See `model_call_usage_estimates.csv`, `token_usage_totals_by_document.csv`, `local_artifact_token_counts.csv`, and `token_estimation_method.md`.
