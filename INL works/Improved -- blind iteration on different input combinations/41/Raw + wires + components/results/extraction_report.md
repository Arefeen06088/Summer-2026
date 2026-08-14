# Document 41 Connectivity Extraction

Blind extraction used only the document 41 input resources and derived visual aids. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Saturated Result

- Final node count: 57
- Final undirected edge count: 59
- Matrix: final_connectivity_matrix.csv
- Edge list: final_edges.csv
- Symmetric: True
- Diagonal zero: True
- Duplicate undirected edges: 0
- Unknown edge endpoints: 0

## Round Progress

- Round 01 Diego: high-recall graph, 58 nodes, 60 edges.
- Round 02 Jennifer: precision-refined graph, 57 nodes, 59 edges.
- Round 03 Diego: agreed with Jennifer's refined graph.
- Round 04 Jennifer final: saturation confirmed.

## Key Precision Decisions

- Excluded GND-1E as a ground/reference symbol rather than a peer matrix node.
- Excluded cable labels, feeder callouts, title block, terminal schedule, notes, and grid labels.
- Kept charger AC source edges from BUS-480A to CHGR-125A and BUS-480E1B to CHGR-125B.
- Kept only UPS-BUS-A to INST-RACK-1; no supported UPS-BUS-B to INST-RACK-1 edge.
- Routed the lower dashed interlock as CB-105 - RELAY-K86A - PANEL-RPS-A - JB-ESF-01 - PANEL-RPS-B - RELAY-K86B - CB-106.

## Token Accounting

Usage objects were not exposed by the subagent tool or main-agent interface. The token files provide low/expected/high local estimates, with image/file tokens estimated from crop dimensions because no API key was available for the Responses counting endpoint.
