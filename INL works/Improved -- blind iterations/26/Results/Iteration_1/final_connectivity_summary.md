# Doc 26 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 26 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 200
- Final unique undirected edges: 201
- Final uncertain/not accepted candidates: 5
- Rejected/removed candidates documented: 7
- Matrix symmetry: True
- Diagonal zero: True
- Inventory component labels retained: 190 of 190
- Isolated nodes: none

## Final Node Policy

- Kept detected component labels from the doc 26 inventory when visually supported by the raw schematic.
- Added visually labeled logical buses and extra visible components retained by the final reviewers.
- Excluded anonymous `WN-*` wire-node points and explanatory route/section labels.

## Final Edge Policy

- Accepted direct solid power/DC links, bus taps, ground taps, feeder chains, and local direct dashed/signal endpoint pairs retained by both reviewers.
- Tie and source breakers are modeled through the breaker nodes, without direct bus-to-bus shortcut edges.
- Ambiguous routed control channels, PLC/relay bundles, and unclear annunciator/JB paths remain outside the final matrix.

## Round Trail

- `round_01_diego_matrix.csv`: Diego high-recall proposal.
- `round_01_jennifer_matrix.csv`: Jennifer precision-refined proposal.
- `round_02_diego_matrix.csv`: Diego saturation agreement/review.
- `round_02_jennifer_matrix.csv`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
- `final_rejected_candidates.csv`
