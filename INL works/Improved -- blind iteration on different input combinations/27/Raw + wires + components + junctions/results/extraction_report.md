# Document 27 Connectivity Extraction

Blind extraction using only the `Raw + wires + components + junctions` resources.

## Final Counts

- Nodes: 200
- Undirected edges: 201
- Matrix: 200 x 200
- Symmetric: True
- Diagonal sum: 0
- Off-diagonal nonzero entries: 402
- Line type counts: {'solid': 92, 'bus-tap': 59, 'normally_open_tie': 2, 'dc_ground': 7, 'dashed': 15, 'dotted': 26}

## Round Saturation

1. Diego high-recall: 200 nodes, 203 candidate edges.
2. Jennifer precision: removed four unsupported charger/battery overconnections; status-marked normally-open tie.
3. Diego convergence: accepted corrections and retained `CB-TIE-41` terminal edges as drawn physical adjacency.
4. Jennifer final: saturated physical-adjacency matrix confirmed.

## Important Interpretation Notes

- The final matrix represents drawn component/node adjacency, not energized operating alignment.
- `CB-TIE-41` terminal edges are retained and marked `normally_open`; `BUS-4160-A` and `BUS-4160-B` are not collapsed.
- Solid, dashed, dotted, and DC/ground lines are included where they terminate at labeled devices, buses, panels, or ground symbols.
- No off-the-shelf OCR was used.
- GT, validation metrics, and GT-derived feedback were not used.
