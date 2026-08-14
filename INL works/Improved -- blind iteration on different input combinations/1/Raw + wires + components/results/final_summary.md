# Final Connectivity Extraction

Document: `1 / Raw + wires + components`

Iteration: `1`

Round sequence:

1. Diego round 1: high-recall extraction.
2. Jennifer round 1: precision review.
3. Diego round 2: accepted Jennifer round 1 unchanged.

Final graph:

- Nodes: 102
- Undirected edges: 101
- Dense matrix: `final_connectivity_matrix.csv`
- Sparse symmetric matrix: `final_sparse_symmetric_matrix.csv`
- Edge list: `final_edges.csv`
- Node list: `final_nodes.txt`

Key precision decisions:

- The small circular `PT` symbols on the 120 VAC instrumentation branches are modeled as separate nodes `PT-A` and `PT-B`.
- The labeled `N.O. DC TIE` between `BUS-125DC-A` and `BUS-125DC-B` is not included as a direct edge because no discrete tie device symbol is visible.

No OCR tooling was used. The extraction used visual inspection of the raw schematic plus the supplied wire/component visual aids.
