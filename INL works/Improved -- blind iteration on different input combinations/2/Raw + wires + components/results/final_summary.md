# Final Connectivity Extraction

Document: `2 / Raw + wires + components`

Iteration: `1`

Round sequence:

1. Diego round 1: high-recall extraction.
2. Jennifer round 1: precision review; no node or edge changes.
3. Diego round 2: accepted Jennifer round 1 unchanged.

Final graph:

- Nodes: 100
- Undirected edges: 100
- Dense matrix: `final_connectivity_matrix.csv`
- Sparse symmetric matrix: `final_sparse_symmetric_matrix.csv`
- Edge list: `final_edges.csv`
- Node list: `final_nodes.txt`

Key precision decisions:

- The 4160 V bus tie is represented only through the explicit `CB-TIE-4AB` device: `BUS-4160-A -- CB-TIE-4AB -- BUS-4160-B`.
- Dashed/control lines are included where visibly connected: `CP-RPS-A -- CP-RPS-B`, `PUMP-CVCS-A -- VLV-LCV201A`, and `PUMP-CVCS-B -- VLV-LCV201B`.
- No direct shortcut edges were added across breakers, transformers, MCCs, motors, pumps, rectifiers, inverters, or the bus tie.

No OCR tooling was used. The extraction used visual inspection of the raw schematic plus the supplied wire/component visual aids.
