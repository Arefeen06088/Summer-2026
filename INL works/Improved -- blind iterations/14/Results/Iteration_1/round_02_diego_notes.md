# Diego Round 02 Notes - Improved doc 14, Iteration 1

## Scope

Reviewed Jennifer's round 1 precision pass using only the allowed current resources: input resources, the current component aid/crops, and Diego/Jennifer round 1 files in `Results/Iteration_1`. I did not use GT, scoring outputs, evaluation files, prior archives, or prior result folders outside the current round files.

## Node decisions

- Retained Jennifer's 178-node set and requested node schema: detected named components, explicit bus nodes, and raw-visible additions `FS-B03`, `PANEL-MCR`, `PANEL-ANN`, and `INV-120B`.
- Did not add anonymous `WN-*` geometry nodes to the final graph.

## Edge decisions

- Kept Jennifer's added solid 480 V panel feeders where the raw/panel crops show direct landings from `BUS-480A`/`BUS-480B` to named panels.
- Kept the corrected B charger path `BUS-480B -> PANEL-RPS-B -> CHG-125B`; retained `BUS-480B -> CHG-125B` as `remove` because it skips the visible panel endpoint.
- Promoted the 11 lower 480 V relay-to-panel/control edges that have visible or locally traceable dashed routes to named panel endpoints in the current crops, including the center-crop-supported `RELAY-KA09 -> PANEL-MCR`.
- Kept `PANEL-MCR -> PANEL-ANN -> CB-DG-TIE` because `14_center_mcr_ann_dg_tie_raw.png` visibly shows the dashed chain landing on those labels.
- Left the six 4.16 kV relay-to-panel assignments uncertain because their long dashed routes enter shared corridors and the endpoint panel labels are not decisive enough.
- Left `PANEL-LS-A -> PANEL-MCR` and `PANEL-LS-B -> PANEL-MCR` uncertain: the MCR-side dashed corridor is visible, but the LS panel side is entangled with shared relay/panel routing, so I did not keep it as a direct panel-panel edge.

## Validation summary

- Nodes: 178
- Edge rows: 199
- Kept edges in matrix: 190
- Uncertain edges excluded from matrix: 8
- Removed edges excluded from matrix: 1
- Symmetric matrix: True
- Zero diagonal: True
- Duplicate edge rows: 0
- Invalid edge endpoints: 0
