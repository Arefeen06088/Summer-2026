# Document 8 Connectivity Extraction

Resources used: only document 8 `Raw + wires` images and generated crops.
GT and GT-derived feedback were not used.

## Rounds

### round1_diego
- Nodes: 120
- Edges: 139
- Note: Diego R1 high-recall proposal. This is reconstructed from the final list plus Jennifer's explicit deltas: it includes PN-480-B--CHGR-125B and JB-2B1--CP-ESFAS-B, but excludes Jennifer's promoted edges.

### round1_jennifer
- Nodes: 120
- Edges: 140
- Note: Jennifer R1 precision correction. Promoted BUS-480-E2B--CHGR-125B, MCC-2C--PUMP-CHG-2A, PN-480-B--VLV-HV-302B; removed PN-480-B--CHGR-125B and JB-2B1--CP-ESFAS-B.
- Added vs previous: 3
  - BUS-480-E2B--CHGR-125B; MCC-2C--PUMP-CHG-2A; PN-480-B--VLV-HV-302B
- Removed vs previous: 2
  - CHGR-125B--PN-480-B; CP-ESFAS-B--JB-2B1

### round2_diego_saturation
- Nodes: 120
- Edges: 140
- Note: Diego R2 accepted Jennifer R1 unchanged. Matrix saturated at 120 nodes and 140 accepted edges.
- Added vs previous: 0
- Removed vs previous: 0

## Final

Final matrix: `final_matrix.csv`.
Final edge list: `final_edges.csv`.
Final node order: `final_nodes.csv`.

Saturation: Diego R2 agreed with Jennifer R1 without further deltas.