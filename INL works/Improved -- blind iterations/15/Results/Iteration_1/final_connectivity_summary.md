# Doc 15 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only doc 15 input resources, generated current inspection artifacts, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `current_round_02_jennifer`
- Final nodes: 183
- Final unique undirected edges: 196
- Uncertain candidates left in final notes: 14
- Rejected/removed candidates documented: 2
- Matrix symmetry: True
- Diagonal zero: True
- Inventory order exact: True
- Inventory nodes retained: 183 of 183
- Missing inventory nodes: none
- Extra nodes not in inventory: none
- Isolated nodes: none

## Final Node Policy

- Kept physical/OCR components from the input CSV.
- Added four visually named tie-control components and sixteen visually labeled bus nodes from the raw/overlay.
- Excluded `OFFSITE SOURCES`, drawing regions/enclosures, title block, notes, legends, feeder note text, anonymous wire-node points, and pure crossings.

## Final Edge Policy

- Represented visually supported solid power, dashed control/DC, and ground-route connections between named endpoints.
- Connected named components to named buses rather than expanding same-bus cliques.
- Did not add anonymous intermediate wire-node points or collapse through named devices.
