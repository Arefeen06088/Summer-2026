# Document 6 Connectivity Extraction

Final interpretation: all visually supported solid, dashed control/interlock, sensing/instrument, and ground-bond connections from the raw schematic.

Artifacts:
- `final_connectivity_matrix.csv`: 105 x 105 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 131 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `round_02_jennifer_promoted_edges.csv`: the 20 Diego candidate edges promoted by Jennifer.
- `special_status_edges.csv`: non-solid/control/sensing/ground metadata edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.

Counts:
- Component-label nodes from CSV: 100
- Explicit visible logical bus nodes: 5
- Total matrix nodes: 105
- Final power edges: 87
- Final sensing/instrument edges: 8
- Final control/interlock edges: 30
- Final ground-bond edges: 6
- Final drawn connections: 131

Notes:
- Crossings without dots were not encoded as edges.
- No extra DC/UPS bus nodes were added.
- The drawing has no visible title-block component/connection checksum; counts are visual-extraction results.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
