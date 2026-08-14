# Final Connectivity Extraction

Document: 4 / Raw + wires + components

Iteration: 1

Final accepted round: diego_round2_accepted

Nodes: 118

Undirected edges: 121

Diagonal: 0

Matrix symmetry: undirected/symmetric

Visual workflow:
- Diego round 1: high-recall extraction.
- Jennifer round 1: precision refinement.
- Diego round 2: accepted Jennifer's refinement; saturation reached.

Key refinements:
- Removed GND-NG-A and GND-NG-B from the matrix as neutral/ground reference symbols.
- Changed CB-CHG-A source from BUS-480-LCA to BUS-480-LCB after reviewing the LC-B vertical supply.
- Added ANN-CP-A--REC-SER-01 as a visible dashed signal link.
- Preserved the odd/even RB feeder alternation: odd F101/F103/.../F115 on BUS-480-RB1, even F102/F104/.../F114 on BUS-480-RB2.

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
