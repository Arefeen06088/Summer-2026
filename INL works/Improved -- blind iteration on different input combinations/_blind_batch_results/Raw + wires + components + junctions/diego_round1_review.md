# Diego Round 1 Review

High-recall review used only blind input resources and current generated outputs, with no GT/evaluation feedback.

Key additions requested:
- Add net-net stitching for collinear wire fragments.
- Recover terminal stubs and stacked component bridges where component masking removes short conductors.
- Use wire_nodes.csv as graph anchors for bus/tap continuity.
- Add edge evidence with edge_type, basis, distance, and confidence.
- Repair common OCR labels such as DS-N501, CP-RPS-A/B, MCC*, REC-125*, and source/generator tags.

Outcome: implemented in Diego round 2 candidate extraction and saved per case as diego_round2_* artifacts.
