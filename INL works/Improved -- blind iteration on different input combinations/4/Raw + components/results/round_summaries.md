# Connectivity Extraction Summary

Document: 4 / Raw + components

Allowed visual inputs:
- raw.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Proposed 120 components, 122 asserted edges, and 6 uncertain/plausible dashed-control candidates.
2. Jennifer round 1: precision refinement. Kept the 120-component set, retained Diego's asserted edges, added ANN-CP-A--REC-SER-01, and excluded the other 5 dashed candidates as crossings/routing without visible component termination.
3. Diego round 2: agreed with Jennifer round 1; final round-2 set is 120 components and 123 asserted edges.
4. Jennifer round 2: saturated=true.

Final component count: 120
Final undirected edge count: 123

Important modeling decisions:
- BUS-480-RB1 and BUS-480-RB2 are separate bus nodes connected only through CB-TIE-480.
- BUS-480-LCA and BUS-480-LCB are separate load-center buses connected through CB-LC-TIE.
- CB-LC-TIE and CB-TIE-480 are included as physical tie connections even though the symbols show normally open breakers.
- TR-LC-A--GND-NG-A and TR-LC-B--GND-NG-B are included as ground-reference edges.
- CB-CHG-A and CB-CHG-B are supplied from BUS-480-LCB.
- ANN-CP-A--REC-SER-01 is included as the only cross-panel dashed-control edge added during precision review.
- Dashed crossings near BUS-UPS-B, TB-ESF-A/B, CB-LC-B, and CB-LC-B2 are not included without terminal evidence.
