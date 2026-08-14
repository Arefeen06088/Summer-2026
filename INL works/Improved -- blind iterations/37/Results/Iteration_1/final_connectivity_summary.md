# Final Connectivity Extraction - Document 2 Iteration 1

Source round: `round_02_jennifer_*`, after Diego and Jennifer converged.

- Nodes: 55 (47 physical components + 8 buses)
- Undirected edges: 56
- Matrix headers match row order: True
- Symmetric matrix: True
- Zero diagonal: True
- Edge list and matrix counts match: True

Retained bus nodes: `BUS-6KA`, `BUS-6KB`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-120A`, `BUS-120B`.

Port/wire IDs such as `Pxx`, `Cxx`, and `Gxx` were treated as wire labels, not graph nodes. Ambiguous dashed-route candidates excluded from the matrix are documented in `final_uncertain_candidates.csv`.

No Ground Truth or GT-derived feedback was used.
