# Case 20 Connectivity Extraction Note

Generated: 2026-07-14T06:12:39

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the AC class 1E, 480 V load-center, 125 VDC, and lower control/interlock topology, including three unlabeled source/interface symbols.
2. Jennifer precision review removed the unlabeled symbols from the final graph, canonicalized bus tags, confirmed `JB-ESF-A/B`, and kept only the visually supported A/B ESF interlock edge `RELAY-K106 -- RELAY-K108`.
3. Diego saturation check accepted Jennifer corrections and added no supported nodes or edges.
4. Jennifer final confirmation used the saturated matrix unchanged.

## Final Counts

- Nodes: 200
- Undirected edges in matrix: 202
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings and near-passes without junction dots were not modeled as edges.
- 13 kV, 4.16 kV, and 480 V bus ties are represented only through their named tie breakers.
- No A-B or C-D 480 V tie was accepted; only `BUS-480-B -- CB-TIE-480 -- BUS-480-C`.
- No 125 VDC bus tie between `BUS-125DCA` and `BUS-125DCB` was accepted.
- Even 480 V branches with `CS-*` devices are kept as adjacent schematic/control connections; C4 is the supported relay branch `JB-4C -- RELAY-K4C -- PMP-AFW-205C`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
