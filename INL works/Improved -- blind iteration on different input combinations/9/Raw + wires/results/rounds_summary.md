# Document 9 Connectivity Extraction

Resources used: only document 9 `Raw + wires` images and generated crops.
No GT, GT-derived feedback, or OCR engine was used.

## Rounds

### round01_diego (Diego)
- Nodes: 180
- Edges: 182
- Note: Diego R1 high-recall accepted graph. Kept the initially read tie label CB-TIE-416-N and included the visually plausible FAN-CR-B--PN-MOV-B MOV feed. Uncertain edges from Diego R1 are documented separately, but not set to 1 in this round matrix.
- Uncertain/rejected notes: 17

### round02_jennifer (Jennifer)
- Nodes: 180
- Edges: 185
- Note: Jennifer R1 precision graph. Corrected CB-TIE-416-N to CB-TIE-41N; replaced FAN-CR-B--PN-MOV-B with MCC-SAF-B2--PN-MOV-B; promoted CB-EDG-A--CB-482A, CB-EDG-B--CB-482B, and RELAY-27B--CB-481B.
- Added/removed vs previous: not compared because node label changed.
- Uncertain/rejected notes: 17

### round03_diego (Diego)
- Nodes: 180
- Edges: 186
- Note: Diego R2 saturation check over Jennifer R1. Added the plausible B-side lower control edge JB-2B--PLC-ESF-B; the other R2 mentions were already present in Jennifer R1.
- Added vs previous: 1
  - JB-2B--PLC-ESF-B
- Removed vs previous: 0
- Uncertain/rejected notes: 3

### round04_jennifer (Jennifer)
- Nodes: 180
- Edges: 187
- Note: Jennifer R2 precision graph. Accepted JB-2B--PLC-ESF-B and RELAY-86A--CB-482A. Other R2 additions were duplicates of already accepted relay edges.
- Added vs previous: 1
  - CB-482A--RELAY-86A
- Removed vs previous: 0
- Uncertain/rejected notes: 1

### round05_diego (Diego)
- Nodes: 180
- Edges: 196
- Note: Diego R3 count-sanity high-recall graph. Added all R3 candidate edges that had some visual plausibility, including low-confidence shared-trunk candidates, so Jennifer could filter them.
- Added vs previous: 9
  - CB-482B--RELAY-27B; JB-1A--PUMP-RHR-A; JB-1B--PUMP-RHR-B; JB-2A--PUMP-CCW-A; JB-2A--PUMP-SI-A; JB-2B--PUMP-CCW-B; JB-2B--PUMP-SI-B; JB-NORM-A--PN-LTG-1B; RTD-PNL-A--RTD-PNL-B
- Removed vs previous: 0
- Uncertain/rejected notes: 8

### round06_jennifer_final (Jennifer)
- Nodes: 180
- Edges: 189
- Note: Jennifer R3 final precision graph. Accepted PN-LTG-1B--JB-NORM-A and PUMP-SI-B--JB-2B only; rejected the remaining R3 shared-trunk or endpoint-ambiguous candidates. Final saturated matrix.
- Added vs previous: 0
- Removed vs previous: 7
  - CB-482B--RELAY-27B; JB-1A--PUMP-RHR-A; JB-1B--PUMP-RHR-B; JB-2A--PUMP-CCW-A; JB-2A--PUMP-SI-A; JB-2B--PUMP-CCW-B; RTD-PNL-A--RTD-PNL-B
- Uncertain/rejected notes: 12

## Final

- Final nodes: 180
- Final unique undirected edges: 189
- Diagonal: 0 for all nodes; no self-loops observed.
- Matrix: `final_matrix.csv`
- Edge list: `final_edges.csv`
- Node order: `final_nodes.csv`

Saturation: Jennifer R3 accepted only PN-LTG-1B--JB-NORM-A and PUMP-SI-B--JB-2B from Diego R3. Remaining count shortfall was not filled because the candidate routes were shared trunks, crossings, near-routes, or lacked clear endpoints.