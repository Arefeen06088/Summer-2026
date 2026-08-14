# Case 15 Connectivity Extraction Note

Generated: 2026-07-14T03:03:49

## Allowed Evidence

- Raw schematic: `raw -- improved_synthetic_nuclear_electrical_schematic.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed 183 nodes and the visually supported edge set.
2. Jennifer precision review accepted Diego's node list/order and confirmed edge list, while explicitly excluding near-alignments and ambiguous alternates.
3. Diego saturation check found no missing/retracted edges and agreed with Jennifer.
4. Jennifer final confirmation accepted the 194-edge visible-termination set and recommended no count-forcing removals.

## Final Counts

- Nodes: 183
- Undirected edges in matrix: 194
- Diagonal: zero
- Matrix: symmetric

The raw title block prints `NODES: 183 CONNECTIONS: 190`. The accepted visible-termination set has 194 edges. The four-edge difference can be made only by removing a visually drawn four-edge class, most plausibly either the `CB-NF-X -- CB-DG-X` dashed breaker interlocks or the `RLY-X06 -- TB-1X` long dashed terminal-block leads. Both Diego and Jennifer retained those edges because the terminations are visually present and the legend defines dashed lines as control/trip/status wiring. The 190/194 tension is documented here rather than silently forcing the matrix to the title-block count.

## Excluded Ambiguous Edges

The excluded uncertain edges are listed in `uncertain_excluded_edges.csv`. They include direct DG-to-NSS bus near-alignments, alternate SEQ/RPS returns to the right-side DG breakers, direct SEQ-to-RPS links, and direct TB-to-JB links.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
