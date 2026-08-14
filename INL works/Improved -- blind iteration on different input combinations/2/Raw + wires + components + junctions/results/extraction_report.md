# Document 2 Connectivity Extraction

Blind extraction using only `Raw + wires + components + junctions` resources.

## Final Counts

- Nodes: 100
- Undirected edges: 100
- Matrix: 100 x 100
- Symmetric: True
- Diagonal sum: 0
- Off-diagonal nonzero entries: 200
- Edge type counts: {'solid': 50, 'bus-tap': 43, 'dashed': 7}

## Round Saturation

1. Diego high-recall: proposed 100 nodes / 100 edges.
2. Jennifer precision review: removed no nodes/edges; clarified dashed/control edge typing.
3. Diego convergence: accepted Jennifer's correction without graph changes.
4. Jennifer final: saturated matrix confirmed.

## Important Interpretation Notes

- Dashed links were retained as control/instrument/permissive connectivity because the drawing legend says dashed lines indicate those wiring types.
- `CB-TIE-4AB` was retained as a physical drawn bus-tie component between `BUS-4160-A` and `BUS-4160-B`; its `N.O.` label is an operating-state note, not a reason to remove the drawn connection.
- Feeder-zone boxes, cable IDs, ratings, title-block text, and unconnected busbar endcaps were excluded.
- No off-the-shelf OCR was used.
- GT, validation metrics, and GT-derived feedback were not used.
