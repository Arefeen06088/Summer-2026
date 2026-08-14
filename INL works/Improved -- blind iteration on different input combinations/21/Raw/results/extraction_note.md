# Case 21 Connectivity Extraction Note

Generated: 2026-07-14T07:35:16

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_fixed.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the AC source/switchgear, 480 V load-center, DC/UPS, and control/instrument topology.
2. Jennifer precision review added the visible unlabeled EDG-2A inboard breaker, supported DC/feed edges, and removed guessed labels/no-tie crossings.
3. Diego focused on isolated control/DC features and added only visually supported UVLS auxiliary, vertical control-trunk, and `RECT-24C` output edges.
4. Jennifer accepted those focused additions and locked the final matrix.

## Final Counts

- Nodes: 200
- Undirected edges in matrix: 202
- Diagonal: zero
- Matrix: symmetric

## Key Decisions

- Crossings without junction dots, including the EDG feeder/no-tie crossing, were not modeled as edges.
- The EDG-2A inboard breaker is drawn but unlabeled, so it is named `CB-UNLABELED-EDG2A-INBOARD`.
- The visible vertical dashed control trunk is represented by adjacent component pairs from `CP-EDG-A` through `CP-CRD`.
- `BAT-EDG-A`, `BAT-EDG-B`, and the `INV-120C` output remain visible but edge-uncertain/excluded rather than guessed.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
