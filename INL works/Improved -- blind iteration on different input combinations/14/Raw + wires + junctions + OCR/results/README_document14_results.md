# Document 14 Connectivity Extraction

Final saturated graph:

- Nodes: 180
- Undirected edges: 198
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Round progression:

- Round 01 Diego high recall: 181 nodes / 218 edges.
- Round 02 Jennifer precision: 180 nodes / 198 edges.
- Round 03 Diego saturation: agreed with Jennifer.
- Round 04 Jennifer final: confirmed no further changes.

Precision decisions:

- Added named logical buses `BUS-4A/B`, `BUS-480A/B`, `BUS-125DCA/B`, `BUS-UPS-A/B`.
- Added missing physical nodes `FS-B03`, `PANEL-MCR`, `PANEL-ANN`, and `INV-120B`.
- Kept dashed control trunk nodes `CTRL-TRAIN-A-DASHED` and `CTRL-TRAIN-B-DASHED`.
- Dropped `MASTER_TERMINAL_BLOCKS` as an unresolved aggregate terminal strip.
- Corrected `CB-DG-TIE` to `CB-DC-TIE`.
- Removed relay-to-disconnect edges; retained relay-to-breaker interlocks.
- Kept individual grounds only; no shared ground bus.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
