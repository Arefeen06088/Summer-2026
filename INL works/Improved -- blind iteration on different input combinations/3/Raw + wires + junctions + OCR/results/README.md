# Document 3 Connectivity Extraction

Final interpretation: all visible drawn electrical connections from the raw schematic, using the raw title-block count of 100 visible components and 100 visible connections as a sanity check.

Artifacts:
- `final_connectivity_matrix.csv`: 100 x 100 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 100 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `special_status_edges.csv`: N.O. tie, ground-reference, control-power, signal, interlock, and terminal-control edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.
- `local_artifact_token_counts.csv`: local file/image token estimate inputs.

Counts:
- Component-label nodes from CSV: 89
- Explicit visible logical/reference nodes: 11
- Total matrix nodes: 100
- Final drawn connections: 100

Notes:
- `BUS-TIE-41` is included as a drawn normally-open tie connection, with status metadata.
- `GND-1E` is represented by two dot-dash ground-reference edges to `BUS-416A` and `BUS-416B`.
- `GND-A`, `GND-B`, and `AFW-B2` were not promoted to matrix nodes.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
