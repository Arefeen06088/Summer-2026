# Document 5 Connectivity Extraction Rounds

Scope: include visually supported power, DC/vital AC, control/trip/close, sensing/instrument, and grounding-conductor links between accepted real nodes. Annotation-only tags are not nodes.

## round1_diego (Diego)
High-recall first pass with broad control and ground candidates retained as matrix edges for audit.
- Nodes: 112
- Edges: 173
- Isolated nodes: none

## round1_jennifer (Jennifer)
Precision review preserving the main AC/DC skeleton and limited ground links; ESF/control nodes left for R2.
- Nodes: 112
- Edges: 113
- Isolated nodes: CP-ESFAS-1, CP-ESFAS-2, RELAY-K1A, RELAY-K2A, RELAY-K1B, RELAY-K2B, RELAY-UV-A, RELAY-UV-B, RELAY-LOOP-C, RELAY-LOOP-D, INST-NSSS-A, INST-NSSS-B

## round2_diego (Diego)
Narrow recheck adding 27 terminal-dot-supported ESF/control links and retaining Jennifer's rejections.
- Nodes: 112
- Edges: 140
- Isolated nodes: none

## round2_jennifer_final (Jennifer)
Final precision acceptance of Diego R2; saturated at 112 nodes and 140 edges.
- Nodes: 112
- Edges: 140
- Isolated nodes: none

## Final Decisions
- Final saturated graph: 112 nodes, 140 edges, no isolated nodes.
- Normally-open tie breakers `CB-TIE13`, `CB-TIE-AB`, and `CB-TIE-CD` are included as visible physical connectivity through breaker nodes.
- `JB-RLY-A--JB-RLY-B` and `PNL-DC-A--PNL-DC-B` are excluded because the dashed routing lacks accepted terminal-dot support for direct matrix edges.
- Load-to-ATS crossing interpretations are excluded; accepted ATS links are `LC-480A/B--XFER-ATS-A` and `LC-480C/D--XFER-ATS-B`.
- Ground is limited to seven visibly supported `GND-GRID` links accepted by both subagents.
- ESF/control final adds the 27 terminal-dot-supported pairs accepted in Diego R2 and Jennifer final.
