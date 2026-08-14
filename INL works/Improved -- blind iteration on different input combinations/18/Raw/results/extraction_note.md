# Case 18 Connectivity Extraction Note

Generated: 2026-07-14T04:28:45

## Allowed Evidence

- Raw schematic: `raw -- synthetic_nuclear_electrical_schematic_readable.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the source, 4160 V, 480 V load-center, and lower control-power topology.
2. Jennifer precision review corrected `CB-GEN-ISO`, `CB-480*-IN`, and `PNL-1C-C7`; she kept B/D at seven load branches and removed unsupported relay-to-relay/direct bus/UAT-bus edges.
3. Diego saturation check accepted the precision corrections and added no supported nodes or edges.
4. Jennifer final confirmation used the same saturated matrix.

## Final Counts

- Nodes: 200
- Undirected edges in matrix: 200
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings without junction dots were not modeled as edges.
- The 4160 A/B connection is represented through `CB-4160-TIE`, not as a direct bus-to-bus edge.
- `CB-UAT-A` and `CB-UAT-B` remain as visible endpoints in the UAT chains, but no 4160 bus connection was accepted.
- The PLC/relay dashed groups are represented as component-level PLC fanout associations plus the visible K102/K202 annunciator drops.
- Train A control power is sourced from `BUS-480B`; Train B control power is sourced from `BUS-480C`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
