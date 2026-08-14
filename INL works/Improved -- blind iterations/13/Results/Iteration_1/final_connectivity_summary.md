# Doc 13 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 13 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 191
- Final unique undirected edges: 170
- Final uncertain/not accepted candidates: 33
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes
- Inventory component labels retained: 178 of 178

## Final Node Decisions

- Kept all 178 detected component-inventory labels.
- Added visually labeled `SWYD-230` from the raw top-left 230 kV source chain.
- Added named logical buses `BUS-4A`, `BUS-4B`, `BUS-4C`, `BUS-4D`, `DC-BUS-A`, `DC-BUS-B`, `DC-BUS-C`, and `DC-BUS-D`.
- Kept `LC-480A` through `LC-480D`, `MCC-A1` through `MCC-D2`, and `GND-A` through `GND-PLANT` as named bus/ground-like component nodes.
- Kept `LOCAL-IO-A` through `LOCAL-IO-D` as drawn named terminal endpoints on the 480 V load-center buses.
- Removed floating annotation nodes for EDG auto-start, ESFAS permissive notes, unit-generator-aux-feed text, and off-sheet continuation labels.

## Final Edge Policy

- Accepted direct solid-line power/DC/ground connections, bus ties, load-center taps, MCC branch feeders, disconnect-to-load branches, and charger-to-DC/inverter/UPS chains.
- Represented batteries through their visible charger connection: `BAT-125* -> CHG-125* -> DC-BUS-*`.
- Left relay-to-breaker dashed control/trip associations uncertain rather than accepted.
- Left cross-routing, charger AC input, JB-to-DC, UPS-to-local-I/O, and off-sheet continuation candidates uncertain unless a clean visible endpoint and junction were present.
- Excluded anonymous wire-node points.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal with high and plausible candidates.
- `round_01_jennifer_*`: Jennifer precision-refined accepted set and uncertainty list.
- `round_02_diego_*`: Diego saturation pass, agreeing with Jennifer and pruning isolated off-sheet annotations.
- `round_02_jennifer_*`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
