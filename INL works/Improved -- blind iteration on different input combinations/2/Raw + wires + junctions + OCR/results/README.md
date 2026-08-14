# Document 2 Connectivity Extraction

Final interpretation: all drawn electrical links from the raw schematic, matching the raw title block count of 100 components and 100 connections.

Artifacts:
- `final_connectivity_matrix.csv`: 100 x 100 symmetric adjacency matrix for final drawn-link connectivity.
- `final_connectivity_edges.csv`: 100 direct undirected edges with status metadata.
- `operational_solid_subset_matrix.csv`: 91-edge derived subset excluding N.O./dashed/control links.
- `special_status_edges.csv`: the 9 final-matrix edges that are N.O. or dashed/control/signal.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `model_call_usage_estimates.csv`: estimated model-call usage; no API key was available, and usage objects were not exposed by the subagent tool.

Counts:
- Component labels from CSV: 86
- Explicit visible bus nodes: 14
- Total matrix nodes: 100
- Final drawn-link edges: 100
- Operational solid subset edges: 91
