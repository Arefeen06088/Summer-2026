# Case 23 Connectivity Extraction Note

Generated: 2026-07-14T09:29:26

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder was present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the shifted 4160 V source/ATS topology, all 480 V load-center nodes, broad relay/JB control clusters, and broad DC/RPS candidates.
2. Jennifer precision review kept real `PNL-x` nodes, removed `AUX METERING BUS`, fixed 1A/1B normal feeder sources, kept 1C/2A/2C on ESF-A and 2B on ESF-B, and narrowed dashed control paths.
3. Diego saturation review accepted the graph except for the repeated load-center ground pattern, correcting each ground to `BUS-480-x -- GND-x` rather than `INST-x -- GND-x`.
4. Jennifer final precision lock accepted the Diego-corrected graph for final output.

## Final Counts

- Nodes: 200
- Undirected edges in matrix: 201
- Diagonal: zero
- Matrix: symmetric

## Key Decisions

- `SYNC-41` is connected to `CB-TIE-41`.
- `1A` is fed from `BUS-4160-A`; `1B` is fed from `BUS-4160-B`.
- `1C`, `2A`, and `2C` are fed from `BUS-4160-ESF-A`; `2B` is fed from `BUS-4160-ESF-B`.
- Each `PNL-1A/1C/1B/2A/2C/2B` is a real separate panel node tapped from its local 480 V bus.
- Load-center `INST-x` and `GND-x` are separate drops from `BUS-480-x`.
- Load-center control clusters use only `VALVE-XVxxx -- JB-x-1`, `JB-x-1 -- second relay`, and `first relay -- second relay`.
- `DC-DC-1` input is from `BUS-125DC-A`; output is to `BUS-24DC-C`.
- Crossings without junction dots were not modeled as connections.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
