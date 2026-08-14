# Doc 6 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 6 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 58
- Final unique undirected edges: 60
- Final uncertain/not accepted candidates: 2
- Rejected/removed candidates documented: 8
- Matrix symmetry: True
- Diagonal zero: True
- Inventory labels retained: 57 of 60
- Isolated nodes: none

## Final Node Policy

- Kept detected physical components and visually meaningful logical bus/ground nodes when supported by the raw schematic.
- Excluded context-only region boxes if they did not function as electrical nodes.
- Excluded anonymous `WN-*` wire-node points, junction dots, line tags, cable callouts, and drawing annotations.

## Final Edge Policy

- Accepted visually supported solid electrical feeder adjacencies, named busbar taps, transformer/source chains, breaker/load chains, DC/UPS power chains, and direct dashed control endpoints retained by both reviewers.
- Long buses are represented through explicit named bus nodes, without clique-expanding all objects on the same drawn busbar.
- Ambiguous dashed interlocks and boundary continuations without clear endpoint termination remain outside the final matrix.

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
