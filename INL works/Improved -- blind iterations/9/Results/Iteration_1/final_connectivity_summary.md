# Doc 9 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 9 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final nodes: 180
- Final unique undirected edges: 180
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes

## Final Node Decisions

- Kept 159 detected physical component rows, with raw-label corrections where visually supported.
- Added 17 explicit named buses: `BUS-13K-01`, `BUS-4160-N1`, `BUS-4160-N2`, `BUS-4160S1A`, `BUS-4160S1B`, `BUS-480-A1`, `BUS-480-A2`, `BUS-480-B1`, `BUS-480-B2`, `BUS-480-N1A`, `BUS-480-N1B`, `BUS-480-N2A`, `BUS-480-N2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`.
- Added four visible center sequence/control devices missed by the component CSV: `RTD-PNL-A`, `RTD-PNL-B`, `TDR-SEQ-A`, `TDR-SEQ-B`.
- Corrected lower junction-box names to `JB-1A`, `JB-2A`, `JB-1B`, `JB-2B`; side circles are terminal marks, not trailing `O/0` label characters.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal, including high-confidence and plausible candidates.
- `round_01_jennifer_*`: Jennifer precision-refined accepted set and uncertain exclusions.
- `round_02_diego_*`: Diego agreement with Jennifer's refined set.
- `round_02_jennifer_*`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
