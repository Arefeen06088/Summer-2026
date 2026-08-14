# Document 7 Connectivity Extraction

Resources used: only files under `Raw + wires` plus generated crops stored in `results/crops`.
Ground truth and GT-derived feedback were not used.

## Rounds

### round1_diego
- Nodes: 120
- Edges: 123
- Note: High-recall proposal. Candidate matrix includes visually plausible items later rejected or left uncertain, including DS-SAT-1--TR-SAT-B, BUS-125DC*--PNL-* and RELAY-K202--SR-101.

### round1_jennifer
- Nodes: 120
- Edges: 126
- Note: Precision refinement. Removed unsupported/ambiguous high-recall edges and added resolved bottom control-panel dashed edges.
- Added vs previous: 8
  - ANN-101--PPS-A; ANN-101--UPS-120A; ANN-201--PPS-B; ANN-201--UPS-120B; PNL-AC-CR1--RELAY-K101; PNL-AC-CR2--RELAY-K201; PPS-A--RELAY-K102; PPS-B--RELAY-K202
- Removed vs previous: 5
  - BUS-125DCA--PNL-AC-CR1; BUS-125DCB--PNL-AC-CR2; DS-SAT-1--TR-SAT-B; RELAY-K201--RELAY-K202; RELAY-K202--SR-101

### round2_diego
- Nodes: 120
- Edges: 126
- Note: Targeted adjudication. Diego accepted Jennifer R1 unchanged.
- Added vs previous: 0
- Removed vs previous: 0

### round2_jennifer_final
- Nodes: 120
- Edges: 127
- Note: Final precision pass. Jennifer R2 accepted RELAY-K202--SR-101 based on the added SR-to-B-relay crop and otherwise kept Diego R2/Jennifer R1 unchanged.
- Added vs previous: 1
  - RELAY-K202--SR-101
- Removed vs previous: 0

### round3_diego_saturation
- Nodes: 120
- Edges: 127
- Note: Saturation pass. Diego R3 agreed with Jennifer R2: RELAY-K202--SR-101 accepted, DS-SAT-1--TR-SAT-B rejected/uncertain, no further deltas.
- Added vs previous: 0
- Removed vs previous: 0

## Final

Final matrix: `final_matrix.csv`.
Final edge list: `final_edges.csv`.
Final node order: `final_nodes.csv`.

Saturation: Jennifer R2 added RELAY-K202--SR-101, and Diego R3 agreed with no further deltas.