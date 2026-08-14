# Connectivity Extraction Summary

Document: 1 / Raw + components

Allowed visual inputs:
- raw -- schematic_image_clean_100_connected.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Kept PT-A/PT-B as inferred local names and marked the unboxed N.O. DC TIE as uncertain-plausible.
2. Jennifer round 1: precision refinement. Renamed PT-A/PT-B to PT-A-LINE_VISUAL_LABEL_PT and PT-B-LINE_VISUAL_LABEL_PT because the printed label is only PT. Retained N.O. DC TIE as a logical normally-open tie node.
3. Diego round 2: agreed with Jennifer round 1; no changes requested.
4. Jennifer round 2: saturated=true; endorsed final matrix.

Final component count: 103
Final undirected edge count: 103

Important modeling decisions:
- BUS-4KV-A/B/C, BUS-480-A/B/C, BUS-125DC-A/B, and BUS-120AC-A/B are explicit logical nodes.
- The 4 kV normally-open ties are represented through CB-TIE/DS-TIE components, with no direct bus-to-bus merge.
- The unboxed N.O. DC TIE is represented as a logical normally-open tie node, with no direct BUS-125DC-A to BUS-125DC-B merge.
- The two small inline PT circles are retained as visual-label nodes using disambiguating names because the raw schematic only prints PT.
- Annotation text such as elementary-diagram sheet references and feeder cable IDs is not treated as a node.
