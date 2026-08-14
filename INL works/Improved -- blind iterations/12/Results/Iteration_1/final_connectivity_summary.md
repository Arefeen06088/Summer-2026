# Doc 12 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 12 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final source: `round_02_jennifer`
- Final nodes: 160
- Final unique undirected edges: 144
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes

## Final Node Decisions

- Kept physical components and visually supported raw-label corrections for repeated feeder fuses, starters, and disconnect switches.
- Kept named logical buses: `BUS-4KV-A`, `BUS-4KV-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-A`, `DC-BUS-B`, and `BUS-120VAC-ESF`.
- Kept `MCC-1A`, `MCC-1B`, `MCC-2A`, and `MCC-2B` as physical motor-control-center nodes, not duplicate bus aliases.
- Kept explicit ground references `GND-1` and `GND-2`.

## Final Edge Policy

- Intermediate wire-node points were excluded.
- Clean solid power/DC chains were accepted through each named component in order.
- Lower RPS/ESFAS/control routes were accepted only when both named endpoints were visually direct; ambiguous dashed/dotted trunks remained in the uncertainty file.
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
