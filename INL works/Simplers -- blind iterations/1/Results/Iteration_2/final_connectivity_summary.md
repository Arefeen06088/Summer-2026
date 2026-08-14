# Final Connectivity Extraction - Iteration 2

Source round: `round_02_jennifer_*`, after Diego and Jennifer converged.

- Nodes: 63
- Undirected edges: 67
- Matrix headers match row order: True
- Symmetric matrix: True
- Zero diagonal: True
- Edge list and matrix counts match: True

Iteration 2 collapses `RPS-TRIP` and `RPS-LOCKOUT` out of the matrix node set as route annotations. The visible solid lockout route is represented directly as `CB-4K-TIE` to `PNL-RPS-1`. The uncertain dashed trip route near `CB-13-TIE` is documented in `final_uncertain_candidates.csv` and excluded from the final matrix.

No Ground Truth or GT-derived feedback was used.
