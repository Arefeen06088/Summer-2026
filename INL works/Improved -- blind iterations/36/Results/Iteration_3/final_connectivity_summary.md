# Final Connectivity Extraction - Iteration 3

Source round: `round_02_jennifer_*`, after Diego and Jennifer converged.

- Nodes: 55 (47 physical components + 8 buses)
- Undirected edges: 59
- Matrix headers match row order: True
- Symmetric matrix: True
- Zero diagonal: True
- Edge list and matrix counts match: True

Retained real bus nodes: `BUS-13K-A`, `BUS-13K-B`, `BUS-4K-A`, `BUS-4K-B`, `BUS-480-A`, `BUS-480-B`, `BUS-DC125-A`, `BUS-DC125-B`.

Removed intermediate tap/point labels: `SU-A`, `EDG-A`, `SU-B`, `EDG-B`, `LC-A1`, `LC-A2`, `LC-B1`, `LC-B2`. Their connectivity is collapsed into direct component-to-bus edges.

No Ground Truth or GT-derived feedback was used.
