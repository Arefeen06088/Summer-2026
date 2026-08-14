# Final Connectivity Extraction

Document: 3 / Raw + wires + components

Iteration: 1

Final accepted round: diego_round2_accepted

Nodes: 101

Undirected edges: 100

Diagonal: 0

Matrix symmetry: undirected/symmetric

Visual workflow:
- Diego round 1: high-recall extraction.
- Jennifer round 1: precision refinement.
- Diego round 2: accepted Jennifer's refinement; saturation reached.

Key refinements:
- Removed unsupported BUS-120A--BUS-120B edge; the two 120 VAC instrument buses have a visible gap.
- Removed unsupported BUS-TIE-41--GND-1E edge; GND-1E is visible but not geometrically tied to BUS-TIE-41.
- Added terminal blocks TB-A401 and TB-B501, connected from JB-A401 and JB-B501.
- Kept INST-PT-A, INST-LT-A, INST-PT-B, and INST-LT-B as component identifiers; PT-A/LT-A/PT-B/LT-B are secondary visible labels.

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
