# Document 16 Connectivity Extraction

Final saturated graph:

- Nodes: 179
- Undirected edges: 183
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Precision decisions:

- Accepted all non-rejected component CSV labels plus 11 added logical/physical nodes.
- Excluded only `PP-E1-480-125R` as a title-block/drawing-number artifact.
- Retained `JB-R` as an isolated real component.
- Removed 15 unsupported lower control/DC/control-trip edges.
- Retained `RTD-RCS101 -- BUS-120-RPS-B` and `UCP-01 -- BUS-120-RPS-B` as medium-confidence edges.
- Ties are breaker-mediated only; A/B buses are not merged.

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was run.
