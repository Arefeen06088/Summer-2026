# Document 7 Connectivity Extraction

Final interpretation: all visually supported solid power/DC feeder and dashed control/trip/status/alarm connections from the raw schematic.

Artifacts:
- `final_connectivity_matrix.csv`: 120 x 120 symmetric adjacency matrix.
- `final_connectivity_edges.csv`: 140 direct undirected edges with metadata.
- `round_*_matrix.csv` and `round_*_edges.csv`: Diego/Jennifer round history.
- `special_status_edges.csv`: dashed control/trip/status/alarm edges.
- `model_call_usage_estimates.csv`: per-call token estimates.
- `token_usage_totals_by_document.csv`: document/iteration token total estimate.

Counts:
- Component-label nodes from CSV: 110
- Explicit visible logical bus nodes: 10
- Total matrix nodes: 120
- Solid power/DC feeder edges: 111
- Dashed control/trip/status/alarm edges: 29
- Final drawn connections: 140

Notes:
- Raw revision status says `120 NODES / 140 EDGES`; the final graph matches it.
- Crossings without dots were not encoded as edges.
- `BAT-125B--BCHG-125B` is not included.
- No API key was present, so the Responses input-token counting endpoint and response usage objects were not available.
