# Doc 32 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 32 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 184
- Final unique undirected edges: 208
- Final uncertain/not accepted candidates: 6
- Rejected/removed candidates documented: 13
- Matrix symmetry: True
- Diagonal zero: True
- Inventory component labels retained: 166 of 166
- Isolated nodes: none

## Final Node Policy

- Kept detected component labels from the doc 32 inventory when visually supported by the raw schematic.
- Added visually labeled process headers, off-page connectors, and extra visible components retained by the final reviewers.
- Excluded anonymous `WN-*` wire-node points, unlabeled elbows/intersections, continuation bubbles, and line-number-only annotations.

## Final Edge Policy

- Accepted visually supported solid process-piping adjacencies, named header/off-page connector adjacencies, and local direct dashed/signal endpoint pairs retained by both reviewers.
- Long process/sample/utility headers are represented through adjacent components and explicit named header nodes, without clique-expanding every object on the same drawn line.
- Ambiguous routed control channels, panel/JB/DCS/PLC bundles, and dashed lines without clear endpoint termination remain outside the final matrix.

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
