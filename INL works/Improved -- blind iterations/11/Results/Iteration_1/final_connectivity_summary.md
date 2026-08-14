# Doc 11 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 11 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 120
- Final unique undirected edges: 132
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes

## Final Node Decisions

- Kept component-table physical components with visually supported DG tag correction from `DG-2A/B/C/D` to `DG-1A/B/C/D`.
- Added raw-visible missing physical breaker `CB-MCC-A1`.
- Removed printed reference-area labels as matrix nodes.
- Kept named buses: `BUS-13-8A`, `BUS-13-8B`, `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-C`, `BUS-4160-D`, `BUS-480-A1`, `BUS-480-A2`, `BUS-480-B1`, `BUS-480-B2`, `BUS-480-C1`, `BUS-480-C2`, `BUS-480-D1`, `BUS-480-D2`, `BUS-DC-125A`, `BUS-DC-125B`.
- Kept explicit grounds `GND-A`, `GND-B`, `GND-C`, and `GND-D`.

## Final Edge Policy

- Intermediate wire-node points were excluded.
- 480 V split-bus tie segments were represented as direct bus-to-bus edges where the raw diagram shows a labeled `TIE-*12` segment with junction dots.
- Long dashed SSPS/RPS/interlock routes and dense lower DC shortcuts were accepted only when both named endpoints were visually unambiguous.
- Crossings without dots were not treated as taps.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal, including high-confidence and plausible candidates.
- `round_01_jennifer_*`: Jennifer precision-refined accepted set and uncertain exclusions.
- `round_02_diego_*`: Diego focused recall review after Jennifer.
- `round_02_jennifer_*`: Jennifer final saturation confirmation.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
