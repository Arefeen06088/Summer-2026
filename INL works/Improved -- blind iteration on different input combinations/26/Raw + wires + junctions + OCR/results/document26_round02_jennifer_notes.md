# Document 26 Round 02 Jennifer Notes

## Method

- Reviewed the raw schematic first, then used the allowed label, wire mask, wire-node overlays, component index, and precision crops only as visual aids.
- Did not use Ground Truth, evaluator output, previous-document connectivity, or off-the-shelf OCR.
- Treated crossings without junction dots as non-connections and preserved Diego's node order and labels unless raw visual evidence required a change.

## Node And Bus Review

- Node count remains 200. No node labels were changed and no nodes were added or removed.
- Kept the 10 logical bus nodes because they are visually named horizontal backbones and have repeated junction-supported taps: BUS-416A, BUS-416B, BUS-480A, BUS-480B, BUS-125DCA, BUS-125DCB, BUS-INV-A, BUS-INV-B, BUS-120N-A, and BUS-120N-B.
- Upper Train A/B 4.16 kV buses, SAT/DG source feeders, and CB-4AB-TIE paths are visually supported by solid conductors and bus junction dots. No crossing-only connections were introduced.

## Edge Review Summary

- Edge count remains 209. No Diego round-01 edges were pruned after raw/crop review.
- Upgraded confidence/evidence for 8 visually supported non-high-confidence edges: CB-INV-A -- INV-31A, CB-INV-B -- INV-31B, BUS-INV-A -- PNL-AC-A, BUS-INV-B -- PNL-AC-B, PNL-AC-A -- BUS-120N-A, PNL-AC-B -- BUS-120N-B, BAT-31A -- CHG-31A, and BAT-31B -- CHG-31B.
- Retained but kept ambiguous the long/crowded dashed control routes: STR-A1-1 -- BAT-31A, STR-B1-1 -- BAT-31B, CB-4A03 -- MTR-RCP-A, CB-4B03 -- MTR-RCP-B, CB-480A13 -- STR-A3-3, and CB-480B13 -- STR-B3-3.

## Line Style Decisions

- Solid feeders remain `power_feeder` except explicit bus tie breaker paths, which remain `bus_tie`.
- Dashed control/protection routes remain `control_interlock`.
- Dotted relay/TB/PT routes remain `instrument_signal`.
- Ground symbols and grounded motor/MCC conductors remain `ground`.

## Remaining Ambiguities

- The RCP dashed routes from CB-4A03/CB-4B03 run beside motor/ground branches and appear to terminate at the motor-side branch, but the endpoint is not a crisp junction-dot landing; retained at low confidence.
- The LC-31A3/LC-31B3 dashed interlocks from CB-480A13/CB-480B13 reach the rightmost starter branch areas, but nearby solid vertical feeders and branch geometry make the exact endpoint crowded; retained at low confidence.
- The STR-A1-1/STR-B1-1 to BAT-31A/B dashed routes are visible but long and pass through dense lower MCC/battery boundaries; retained at medium confidence.

## Counts

- Node count: 200
- Edge count: 209
- Edge kind counts: {'bus_tie': 6, 'control_interlock': 10, 'ground': 8, 'instrument_signal': 16, 'power_feeder': 169}
- Confidence counts: {'high': 203, 'low': 4, 'medium': 2}

## Validation

- No unknown nodes in edges: True
- No duplicate undirected pairs: True
- Symmetric adjacency matrix: True
- Diagonal zero: True
