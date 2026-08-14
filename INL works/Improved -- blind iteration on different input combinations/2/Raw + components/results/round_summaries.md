# Connectivity Extraction Summary

Document: 2 / Raw + components

Allowed visual inputs:
- raw -- schematic_image_variant_b_100.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Proposed 100 components and 100 asserted edges, including dashed CVCS valve links and the dashed CP-RPS-A/CP-RPS-B cross-link.
2. Jennifer round 1: precision refinement. Kept the same component set and topology; normalized edge types to solid_power, solid_tie, and dashed_control; excluded direct BUS-4160-A/B merge and direct CP-to-INST shortcuts.
3. Diego round 2: agreed with Jennifer round 1; no changes requested.
4. Jennifer round 2: saturated=true.

Final component count: 100
Final undirected edge count: 100

Important modeling decisions:
- BUS-4160-A and BUS-4160-B are separate bus nodes connected only through CB-TIE-4AB.
- Dashed CP-RPS-A--CP-RPS-B is included as a control/signal connection.
- CP-RPS to instrument paths are represented in series through RLY-K501A/B.
- Dashed CVCS pump-to-valve paths are included as control/signal connections.
- Dashed feeder area boundaries, cable labels, title text, notes, and legends are not treated as nodes.
