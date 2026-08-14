# Case 17 Connectivity Extraction Note

Generated: 2026-07-14T04:03:12

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the two-train 4160 V/480 V/DC/UPS/control topology.
2. Jennifer precision review removed routing-only wireway nodes, unsupported recorder-tail edges, and long dashed branch tails.
3. Diego saturation check agreed with Jennifer and added no nodes or edges.
4. Jennifer final confirmation removed edge-free visible components `MASTER TERMINAL BLOCKS 21-29` and `REC-SOE-2` from the final matrix.

## Final Counts

- Nodes: 199
- Undirected edges in matrix: 199
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings/overlaps without black-dot terminations were not modeled as edges.
- `WIREWAY A/B CONTROL LANES 2380/2420` were treated as routing annotations, not equipment nodes.
- `REC-SOE-2` and `MASTER TERMINAL BLOCKS 21-29` are visible but omitted from the final matrix because no accepted edge terminates on them.
- The accepted final set keeps the three A/B ties: `CB-TIE-4AB`, `CB-TIE-480AB`, and `CB-DCTIE-AB`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
