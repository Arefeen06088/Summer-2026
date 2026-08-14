# Jennifer Round 01 Notes - Improved doc 14, Iteration 1

## Scope

Reviewed Diego's round 1 extraction against the raw schematic and the current inspection crops/list only. I did not use GT, scoring outputs, evaluation files, prior archived results, or anonymous/intermediate wire nodes as final graph nodes.

## Visual decisions

- Kept the explicit bus nodes visible in the raw/crops: BUS-4A, BUS-4B, BUS-480A, BUS-480B, BUS-125DCA, BUS-125DCB, BUS-UPS-A, and BUS-UPS-B.
- Kept the 4.16 kV source chains, the TR-480A/TR-480B feeds, and both tie breakers as bus-to-breaker-to-bus paths rather than direct bus-to-bus shortcuts.
- Kept clear vertical solid feeder stacks for 4.16 kV and 480 V loads, including terminal-block-to-instrument stubs and load-to-ground conductors where visibly landed.
- Added/kept raw-visible nodes that were not in the detector CSV: FS-B03, PANEL-MCR, PANEL-ANN, and INV-120B.
- Added missing solid 480 V panel feeder edges from BUS-480A/B to the named panels. The B-side charger feed was refined to BUS-480B -> PANEL-RPS-B -> CHG-125B instead of a direct bus-to-charger jump.
- Kept the dashed PANEL-MCR -> PANEL-ANN -> CB-DG-TIE control chain because the dashed line visibly lands on labeled components.

## Conservative changes from Diego

- Marked Diego's long relay-to-panel dashed routing assignments as `uncertain`. The dashed corridors are visible, but many merge/branch before panel landings, so exact relay-to-panel endpoints are not reliable enough for the kept matrix.
- Marked PANEL-LS-A/PANEL-LS-B to PANEL-MCR corridor edges as `uncertain` for the same reason.
- Marked BUS-480B -> CHG-125B as `remove` because it skips the visually supported PANEL-RPS-B endpoint on the same solid feeder.
- Excluded all `uncertain` and `remove` edges from the matrix.

## Validation summary

- Nodes: 178
- Edge rows reviewed/written: 199
- Kept edges in matrix: 179
- Uncertain edges excluded from matrix: 19
- Removed edges excluded from matrix: 1
- Symmetric matrix: True
- Zero diagonal: True
- Invalid edge endpoints: 0
