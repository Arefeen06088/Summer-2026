# Document 15 Connectivity Extraction

Final saturated graph:

- Nodes: 183
- Undirected edges: 198
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Round progression:

- Round 01 Diego high recall: 183 nodes / 202 edges.
- Round 02 Jennifer precision: 183 nodes / 198 edges.
- Round 03 Diego saturation: agreed with Jennifer.
- Round 04 Jennifer final: confirmed no further changes.

Precision decisions:

- Accepted buses `BUS-SWY-1/2`, `BUS-NSS-1/2`, `BUS-416A/B/C/D`, `BUS-480A/B/C/D`, and `BUS-DC-A/B/C/D`.
- Accepted control nodes `SEQ-1AB`, `RPS-AC-1`, `SEQ-2CD`, and `RPS-AC-2`.
- Confirmed `MCC-1A/B/C/D` as busbar-style physical components already in the component CSV.
- Removed four low-confidence direct `SEQ/RPS` to tie-breaker control associations.
- Kept medium `BUS-NSS` to `CB-DG` tap edges and all solid source/tie/transformer/MCC feeder paths.
- Kept lower DC/control strings and individual `BUS-DC` to ground references.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
