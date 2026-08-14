# Doc 14 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 14 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 178
- Final unique undirected edges: 172
- Final uncertain/not accepted candidates: 26
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes
- Inventory component labels retained: 166 of 166

## Final Node Policy

- Kept all visually supported detected component labels from the doc 14 inventory unless the final reviewer explicitly pruned a non-connective annotation.
- Kept visually supported missed raw labels such as `PANEL-MCR`, `PANEL-ANN`, `INV-120B`, and `FS-B03` when present in the final node set.
- Kept named buses such as `BUS-4A`, `BUS-4B`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-UPS-A`, and `BUS-UPS-B` when present in the final node set.
- Excluded anonymous `WN-*` wire-node points and cable callout labels.

## Final Edge Policy

- Accepted visually direct solid power/feeder links, named bus ties, DC/UPS bus links, and clearly terminated instrument-signal links where retained by the final reviewer.
- Treated dashed control/interlock routes cautiously; ambiguous panel/relay/interlock paths remain in the uncertainty file.
- Crossings without dots were not treated as connections.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal with high and plausible candidates.
- `round_01_jennifer_*`: Jennifer precision-refined accepted set and uncertainty list.
- `round_02_diego_*`: Diego saturation pass.
- `round_02_jennifer_*`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
