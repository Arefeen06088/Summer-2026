# Document 5 Connectivity Extraction

Final interpretation: all visible drawn connections from the raw schematic, using the raw title-block count of 112 components and 140 connections as a sanity check.

Artifacts:
- `final_connectivity_matrix.csv`: 112 x 112 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 140 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `round_02_jennifer_changed_edge_diff.csv`: the precision diff from Diego Round 1.
- `special_status_edges.csv`: N.O. ties and non-solid line-type/status edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.
- `local_artifact_token_counts.csv`: local file/image token estimate inputs.

Counts:
- Component-label nodes from CSV: 103
- Explicit visible logical/reference nodes: 9
- Total matrix nodes: 112
- Final solid edges: 106
- Final dashed control/trip/close edges: 19
- Dash-dot sensing/instrument edges: 6
- Dotted grounding-conductor edges: 9
- Final drawn connections: 140

Notes:
- Normally-open tie breakers are included as visible drawn connections and annotated in metadata.
- `JB-RLY-A--JB-RLY-B` and `CP-ESFAS-1--CP-ESFAS-2` are not in the final matrix.
- `XFER-ATS-A--RECT-48V-A` and `XFER-ATS-B--RECT-48V-B` are in the final matrix.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
