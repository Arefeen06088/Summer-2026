# Document 3 Round Notes

Only resources from `Raw + wires + components + junctions` were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Sequence

1. Diego R1 high-recall extraction proposed component nodes, feeder-label nodes, accepted edges, and uncertain candidates.
2. Jennifer R1 removed non-component line-label nodes, rejected unsupported source-bus and ground-reference edges, and accepted BUS-120A/B to RPS panel risers.
3. Diego R2 agreed with Jennifer after one correction: exclude isolated `GND-1E` from the final matrix.

## Final Excluded / Ambiguous Cases

- CB-101--BUS-416A and CB-102--BUS-416B: visible lower stubs stop above BUS-416A/B; no hidden tie inferred.
- FDR-A1/FDR-A2/FDR-B1/FDR-B2: feeder line labels, not equipment nodes; collapsed to direct visual component edges.
- GND-1E/GND-A/GND-B: standalone reference/ground markings; no unambiguous connected conductor in the graph.
- BUS-120A/B--PANEL-ESF-A/B: ESF panels connect via relay path, not directly to the 120 VAC bus.
- PANEL-RPS-A/B--PANEL-ESF-A/B: no direct panel-to-panel conductor; connection is through RELAY-K27A/B.

## Final Counts

- Final nodes: 99
- Final undirected edges: 96
