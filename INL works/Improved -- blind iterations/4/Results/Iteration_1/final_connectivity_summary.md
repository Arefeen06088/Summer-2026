# Doc 4 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the matching doc 4 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 120
- Final unique undirected edges: 124
- Final uncertain/not accepted candidates: 0
- Rejected/removed candidates documented: 0
- Matrix symmetry: True
- Diagonal zero: True
- Inventory nodes retained: 120 of 120
- Isolated nodes: none

## Final Node Policy

- Kept the 110 physical components from the matching 8800px component OCR resource.
- Added only named visual bus/ground nodes read from the matching raw/overlay.
- Excluded the mismatched 5500px/62-label resource set, anonymous `WN-*` wire-node points, unlabeled elbows/intersections, cable tags, title text, and pure line crossings.

## Final Edge Policy

- Accepted visually supported solid electrical power adjacencies, source/transformer/breaker chains, busbar taps, load-center branch chains, DC/UPS bus taps, visible grounds, and clearly terminated dashed signal/control edges retained by both reviewers.
- Named buses are represented as hub nodes without clique-expanding every object on the same bus.
- Ambiguous crossing geometry and unsupported signal trunk expansion remain outside the final matrix.
