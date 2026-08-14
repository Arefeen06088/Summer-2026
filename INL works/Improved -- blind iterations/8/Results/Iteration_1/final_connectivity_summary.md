# Doc 8 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 8 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final nodes: 120
- Final unique undirected edges: 134
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes

## Final Node Decisions

- Dropped unsupported OCR/overlay artifact `CB-303`.
- Normalized `GND-AJ` to raw visual label `GND-A`.
- Replaced OCR-bad `NCC-*` labels with raw visual `MCC-*` labels.
- Corrected raw labels `MOV-8816A/B` to `MOV-8810A/B`.
- Added visible physical components missed by OCR: `MCC-2C`, `CB-52B`, `PN-125B`, `PUMP-AF-2B`.
- Added 12 explicit bus nodes and excluded cable/run labels such as `2E-100`.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal, including plausible lower-confidence candidates.
- `round_01_jennifer_*`: Jennifer precision-refined proposal before final label/DC-link corrections.
- `round_02_diego_*`: Diego agreement with Jennifer's first refinement.
- `round_02_jennifer_*`: Jennifer final correction adding charger-battery links and correcting `MOV-8810A/B`.
- `round_03_diego_*`: Diego final agreement; same matrix as saturated final.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
