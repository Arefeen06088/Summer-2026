# Case 16 Connectivity Extraction Note

Generated: 2026-07-14T03:31:20

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_revised(1).png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the full two-train topology and flagged bus/label/control uncertainties.
2. Jennifer precision review corrected `BUS-480-B`, `CB-31A-FDR30-B`, `JB-RPS-AB-1A`, `GND-NO`, removed unsupported battery-bus and RELAY-86/TB-3 edges, and excluded weak long dashed routes.
3. Diego saturation check agreed with Jennifer's corrections and added no edges.
4. Jennifer final confirmation removed `RTD-RCS101` from the accepted final node list because its only visible connection remained uncertain.

## Final Counts

- Nodes: 177
- Undirected edges in matrix: 173
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- `BUS-480-B` is kept as the lower 480 V header. `CB-480B-IN` crosses the upper A header without a filled dot and lands on the lower B header.
- `CB-31A-FDR30-B` is connected to `BUS-480-B`, not `BUS-480-A`.
- Direct `BUS-125DC-* -- BATT-125*` edges were removed; the visible connection is `BATT-125* -- CHGR-125* -- BUS-125DC-*`.
- `RELAY-86A/B -- TB-3A/B` and `MG-RPS-B -- RTD-RCS101` remain excluded/uncertain.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
