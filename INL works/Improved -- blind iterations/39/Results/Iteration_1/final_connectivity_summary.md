# Final Connectivity Summary - Improved Doc 39 Iteration 1

Selected final round: `round_02_jennifer`

Saturation reached: yes. Jennifer R02 agreed with Diego R02 after a focused review of the only remaining disagreement.

Final counts:
- Nodes: 54
- Kept connectivity edges: 56
- Removed/non-final review edges: 23
- Uncertain edges: 0

Final node policy:
- Kept named physical components, explicit 4160/480 buses, and the visible plant ground.
- Excluded intermediate `WIRE-NODE-*` points.
- Excluded annotation-only labels: `LC-A`, `LC-B`, `CONTROL-ROOM-ANNUNCIATION`, division headings, normal offsite feed notes, and `N.O. TIE`.

Key final refinements:
- Charger feeds are modeled as `BUS-480-A -> CHG-125A` and `BUS-480-B -> CHG-125B`.
- `RPS-A -> JB-A101` and `RPS-B -> JB-B101` are kept after focused raw-image review of continuous dashed control conductors.
- `ANN-CR01 -> REC-SOE01` is kept as a direct dashed segment.
- `JB-A101 -> ANN-CR01`, `REC-SOE01 -> JB-B101`, and logical taps to `CONTROL-ROOM-ANNUNCIATION` are not kept.

Primary files:
- `final_connectivity_matrix.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_edge_review.csv`
- `final_connectivity_validation.json`
