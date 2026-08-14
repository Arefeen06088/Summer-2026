# Document 13 Connectivity Extraction

Final saturated graph:

- Nodes: 192
- Undirected edges: 195
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Round progression:

- Round 01 Diego high recall: 203 nodes / 243 edges.
- Round 02 Jennifer precision: 192 nodes / 195 edges.
- Round 03 Diego saturation: agreed with Jennifer.
- Round 04 Jennifer final: confirmed no further changes.

Precision decisions:

- Included missing physical node `SWYD-230`.
- Included logical buses `BUS-4A/B/C/D`, `DC-BUS-A/B/C/D`, `LOCAL-IO-A/B/C/D`, and `UNIT-GENERATOR-AUX-FEED`.
- Excluded `BUS-230KV-SWITCHYARD`, ESFAS/diesel note-only control nodes, and offpage endpoints from the precise graph.
- Removed unsupported LOCAL I/O to JB, JB to DC bus, MCC to relay, note-only control, diesel auto-start, and offpage edges.
- Replaced the two-step switchyard descriptor path with `GRID-230KV -- SWYD-230`.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
