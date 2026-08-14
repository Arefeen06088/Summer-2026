# Document 3 Connectivity Extraction Rounds

Scope: include visually supported power, DC power, control/interlock, instrument-signal, and ground-reference links between accepted real nodes. Do not promote gray run labels unless they are accepted as logical nodes.

## round1_diego (Diego)
High-recall first pass. Included two source-to-bus edges and promoted 120A/120B control-run labels to nodes.
- Nodes: 101
- Edges: 100
- Isolated nodes: none

## round1_jennifer (Jennifer)
Precision review. Removed 120A/120B run labels as nodes, added GND-1E, excluded source-gap and ground-label edges.
- Nodes: 100
- Edges: 96
- Isolated nodes: GND-1E

## round2_diego (Diego)
Narrow recheck. Accepted Jennifer's 96-edge set and rejected the two source-gap and two ground-label uncertainties.
- Nodes: 100
- Edges: 96
- Isolated nodes: GND-1E

## round2_jennifer_final (Jennifer)
Final precision saturation. Kept GND-1E as a visible zero-degree node; no visually supported edge was added.
- Nodes: 100
- Edges: 96
- Isolated nodes: GND-1E

## Final Ambiguity Decisions
- `CB-101--BUS-416A`: excluded; source stub stops above the bus with no visually supported terminal connection.
- `BUS-416B--CB-102`: excluded; source stub stops above the bus with no visually supported terminal connection.
- `120A-CNTRL` and `120B-CNTRL`: excluded as nodes; treated as gray control-run labels, with direct accepted edges from `BUS-120A/B` to `PANEL-RPS-A/B`.
- `GND-A` and `GND-B`: excluded as matrix nodes; treated as gray ground-reference labels.
- `GND-1E`: retained as a visible ground symbol/node, but zero-degree because no accepted real-node edge is visually supported without promoting `GND-A/B` or inventing a link.
- `AFW-B2`: excluded; no visible pair is present.
