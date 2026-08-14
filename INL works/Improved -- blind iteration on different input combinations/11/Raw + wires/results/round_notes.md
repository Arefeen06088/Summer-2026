# Document 11 Connectivity Extraction Notes

Only the raw schematic, wires mask, and wires mask overlay under `Raw + wires` were used for extraction. Existing result/validation files were not opened or used. No GT-derived feedback or off-the-shelf OCR was used.

## Final Result

- Nodes: 120
- Edges: 142
- Symmetric matrix: True
- Diagonal zero: True

## Round Progress

- `round1_diego`: 120 nodes, 144 edges.
- `round1_jennifer`: 120 nodes, 142 edges.
- `round2_diego`: 120 nodes, 142 edges.
- `round2_jennifer`: 120 nodes, 142 edges.

## Precision Decisions

- Removed `ATS-480-A--PANEL-SSPS` and `ATS-480-B--PANEL-SSPS`; dashed routing is adjacent/crossing without a clear ATS-to-SSPS terminal.
- Kept `BUS-480-X1--BUS-480-X2` solid bus ties at `TIE-X12`; no separate `TIE-X12` nodes were added.
- Kept relay-27, I/C, ground, and DC bus assignments that terminate at visible dots or panel terminals.
- Treated labels such as `FDR-*`, `52-*`, `LC-*`, `BC-*`, `DC-*125`, `ATS-*OUT`, `UPS-*IN/OUT`, and `SSPS-A/B/C/D` as route labels, not component nodes.

## Token Estimate

- Expected total tokens estimated: 93464 (low 80964, high 112864).
