# Doc 16 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only doc 16 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_04_jennifer`
- Final nodes: 178
- Final unique undirected edges: 175
- Final uncertain/not accepted candidates: 0
- Rejected/removed candidates documented: 0
- Matrix symmetry: True
- Diagonal zero: True
- Inventory nodes retained: 178 of 178
- Missing inventory nodes: none
- Extra nodes not in inventory: none
- Isolated nodes: none

## Final Node Policy

- Kept visually supported physical components from the corrected OCR/manual inventory.
- Applied the final saturated RPS correction: `DB-RPS-A3-1A` is the A-side lower RPS box, and OCR-truncated `JB-R` is corrected to `JB-RPS-B3-1B`.
- Kept named visual bus nodes required to represent shared buses without clique expansion.
- Excluded title-block metadata, note/legend text, anonymous `WN-*` points, line ticks, and pure crossings.

## Final Edge Policy

- Accepted visually supported source, transformer, breaker, bus, MCC, branch-load, ground, DC/vital, and named control/signal endpoint connections retained by the reviewers.
- Long buses are represented as hub nodes; branch devices connect to the named bus rather than to every other object on that bus.
- Ambiguous dashed/dotted control routes remain outside the final matrix unless both named endpoints were visually supported by final reviewers.
