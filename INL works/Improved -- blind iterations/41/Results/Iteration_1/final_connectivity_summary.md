# Doc 41 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only doc 41 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 58
- Final unique undirected edges: 60
- Uncertain candidates left in final notes: 0
- Rejected/removed candidates documented: 0
- Matrix symmetry: True
- Diagonal zero: True
- Inventory nodes retained: 58 of 58
- Missing inventory nodes: none
- Extra nodes not in inventory: none
- Isolated nodes: none

## Final Node Policy

- Kept visually supported physical components and named logical buses from the corrected inventory.
- Kept manual raw-visible ground `GND-1E`.
- Excluded drawing regions/enclosures, title block, notes, legends, reference tables, cable labels, anonymous wire-node points, and pure crossings.

## Final Edge Policy

- Represented direct visually supported solid power feeders and dashed control/interlock routes.
- Connected named components to named buses rather than expanding bus cliques.
- Did not add anonymous intermediate node points.
- Did not collapse through named panels, relays, junction boxes, or buses.
