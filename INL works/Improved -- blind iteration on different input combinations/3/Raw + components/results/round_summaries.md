# Connectivity Extraction Summary

Document: 3 / Raw + components

Allowed visual inputs:
- raw -- synthetic_npp_100_component_electrical_schematic.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Proposed 104 nodes by treating GND-A, GND-B, 120A-CNTRL, and 120B-CNTRL as possible nodes; carried the two source breaker-to-bus edges and BUS-TIE-41--GND-1E as uncertain/plausible.
2. Jennifer round 1: precision refinement. Reduced to the 100 visually supported components, collapsed control labels, replaced local ground labels with BUS-416A/B--GND-1E, and withheld CB-101--BUS-416A plus CB-102--BUS-416B as uncertain because of the small visual gap.
3. Diego round 2: agreed with Jennifer round 1; no changes requested.
4. Jennifer round 2: saturated=true. Added CB-101--BUS-416A and CB-102--BUS-416B after considering the raw annotation VISIBLE COMPONENTS = 100; VISIBLE CONNECTIONS = 100 and the aligned source leads/bus landing dots. BUS-TIE-41--GND-1E remains excluded.

Final component count: 100
Final undirected edge count: 100

Important modeling decisions:
- GND-A and GND-B are local reference labels, not standalone matrix nodes.
- 120A-CNTRL and 120B-CNTRL are control-line labels, not standalone matrix nodes.
- BUS-416A and BUS-416B remain separate bus nodes connected through BUS-TIE-41.
- CB-101--BUS-416A and CB-102--BUS-416B are included in the final matrix.
- BUS-TIE-41--GND-1E is not included.
- B2 contains five visible feeder/load pairs; no AFW-B2 component is visible.
