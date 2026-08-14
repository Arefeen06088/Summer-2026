# Diego Round 02 Connectivity Notes

## Review Scope
- Re-inspected doc 21 raw schematic crops and derived artifacts only from doc 21 `Input resources` and doc 21 `Codes and artifacts`.
- Focused review on Jennifer's 16 removed round 01 edges.
- No GT, evaluator outputs, prior metric feedback, or external folders were used.

## Agreement With Jennifer
- I agree with Jennifer's precision review.
- I accepted all 16 removals and added no edges back.
- The round 02 Diego matrix is therefore aligned with Jennifer's reviewed 199-node matrix.

## Visual Rationale
- The control ladder rails `BUS-501A` and `BUS-501B` are printed as two vertical rails. The dashed ladder rows visually land on one rail/side by row, not both rails for every control/protection panel. My round 01 opposite-rail edges were high-recall over-inclusions.
- `CP-SWGR` sits above the main dashed row structure; I do not see a clear direct rail tap to either `BUS-501A` or `BUS-501B`, so both removed rail edges should stay removed.
- `CP-CRD` is visible at the bottom of the ladder area, but the visual evidence does not clearly support the removed `CP-CRD -- BUS-501B` edge.
- `BAT-EDG-A` and `BAT-EDG-B` have dashed paths in the lower DC/UPS area, but the dashed routing is not clear enough to support direct `BAT-EDG-A -- BAT-EDG-B`, `CP-EDG-A -- BAT-EDG-A`, or `CP-EDG-B -- BAT-EDG-B` connectivity.

## Accepted Removed Edges
- `BAT-EDG-A` -- `BAT-EDG-B`
- `CP-CCW-A` -- `BUS-501B`
- `CP-CCW-B` -- `BUS-501A`
- `CP-CRD` -- `BUS-501B`
- `CP-EDG-A` -- `BAT-EDG-A`
- `CP-EDG-A` -- `BUS-501B`
- `CP-EDG-B` -- `BAT-EDG-B`
- `CP-EDG-B` -- `BUS-501A`
- `CP-SI-A` -- `BUS-501B`
- `CP-SI-B` -- `BUS-501A`
- `CP-SWGR` -- `BUS-501A`
- `CP-SWGR` -- `BUS-501B`
- `ESFAS-A` -- `BUS-501B`
- `ESFAS-B` -- `BUS-501A`
- `RPS-A` -- `BUS-501B`
- `RPS-B` -- `BUS-501A`

## Differences From Jennifer
- None. I found no clear visual evidence requiring any removed edge to be restored.

## Validation Summary
- Node count: 199
- Edge count: 204
- Symmetric: True
- Diagonal zero: True
- Row/column labels identical: True
- Isolated node count: 2
- Isolated nodes: `BAT-EDG-A`, `BAT-EDG-B`
