# Document 24 Extraction Notes

Allowed resources only: raw schematic, detected-components overlay, wire mask/overlay, wire nodes, and local crops from the doc24 `Raw + wires + components + junctions` folder.

No ground-truth files or GT-derived feedback were used. No off-the-shelf OCR was used; labels were read visually from the schematic/crops.

## Rounds

1. Diego high recall: proposed all visually plausible nodes and edges, including two uncertain control edges.
2. Jennifer precision: removed `(RPS-PNL-B, RELAY-K59B)` and `(SYNC-CAB, LOAD-SHED-CAB)`.
3. Diego saturation: accepted both removals after focused crop review.
4. Jennifer final: confirmed the corrected graph as final.

## Final Graph

- Nodes: 200
- Edges: 218
- Matrix symmetric: True
- Matrix diagonal zero: True

`BUS-201A` represents the labeled 4.16 kV Safety Bus 101A / normal-EDG source bus. `BUS-201B` represents the matching 4.16 kV Safety Bus 101B. Ground symbols are represented as named ground-reference nodes when a drawn lead lands on them.

Token accounting is estimated locally because the OpenAI Responses token-counting endpoint and response usage objects were not available without an API key / tool exposure. The estimate combines text-token approximation with a high-detail image-tile heuristic and gives low/expected/high totals.
