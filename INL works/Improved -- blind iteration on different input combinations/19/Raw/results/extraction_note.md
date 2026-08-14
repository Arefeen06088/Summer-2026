# Case 19 Connectivity Extraction Note

Generated: 2026-07-14T05:56:12

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_v3.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the two-division 4160 V/480 V/load-feeder/control-power topology, including two broad lower route-label nodes.
2. Jennifer precision review removed the artificial `CONTROL POWER / DC DISTRIBUTION` route nodes, connected lower control power from `BUS-480-A/B`, and confirmed exact labels such as `PN-RPS-A/B`, `JB-MAIN`, `[LS-MOV601]`, and `INST-RPS701`.
3. Diego saturation check accepted Jennifer corrections and added no supported nodes or edges.
4. Jennifer final confirmation used the saturated matrix unchanged.

## Final Counts

- Nodes: 200
- Undirected edges in matrix: 200
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings without junction dots were not modeled as edges.
- `BUS-4160-A` and `BUS-4160-B` connect only through `CB-TIE-4160`.
- `BUS-480-A` and `BUS-480-B` connect only through `CB-TIE-480`.
- `CONTROL POWER / DC DISTRIBUTION` text was treated as a route label, not an equipment node.
- PR relays connect only to their matching `CB-F###`; auxiliary `RELAY-A###` nodes connect only to the MCC side.
- Dashed signal chains are modeled through the visible sequence `LOAD/endpoint -> INST -> JB -> TB -> LCS`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
