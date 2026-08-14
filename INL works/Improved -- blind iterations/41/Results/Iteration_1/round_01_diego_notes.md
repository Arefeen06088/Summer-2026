# Round 01 Diego Notes - Doc 41 / Iteration 1

## Node policy
- Used only doc 41 input resources and derived inspection artifacts from `Input resources` and `Codes and artifacts`.
- Kept the corrected inventory order exactly for the matrix: 58 nodes including components, named buses/logical nodes, and manual raw-visible ground `GND-1E`.
- Excluded unit/region boxes, title block, notes, legend/reference tables, cable labels, row/column coordinates, anonymous `WN-*` wire points, pure crossings, and label-only artifacts as connectivity nodes.
- Did not collapse across named buses, panels, relays, or `JB-ESF-01`; edges land on the nearest named endpoint where visible.

## Evidence highlights
- Top 4.16 kV: OFFSITE/TR/CB/BUS chains are visible for both trains, with `CB-TIE-1AB` connecting the two named 4.16 kV buses. `GND-1E` is tied only to `TR-1A` by the visible grounding conductor.
- 480 V distribution: each 4.16 kV bus drops to named transformers, then through named breakers to `BUS-480A`, `BUS-480E1A`, `BUS-480B`, and `BUS-480E1B`. The Train B `CB-204` route was kept as `CB-204` to `BUS-480E1B`, not as a `BUS-480B`/`BUS-480E1B` tie.
- MCC loads: normal/aux/essential MCC feeders fan out to the pumps, fans, and MOVs shown by solid feeder lines.
- Vital DC/UPS: chargers and batteries land on their named DC buses; DC buses feed inverters; inverters feed UPS buses; UPS buses feed the RPS panels. `UPS-BUS-A` also visibly feeds `INST-RACK-1`.
- Control/interlocks: dashed wiring supports `RELAY-K86A` to `PANEL-RPS-A`, `RELAY-K86B` to `PANEL-RPS-B`, both RPS panels to `JB-ESF-01`, and probable EDG lockout control edges `CB-105` to `RELAY-K86A` and `CB-106` to `RELAY-K86B`.

## Uncertain candidates included
- `BUS-480E1B` to `CHGR-125B` is included as `uncertain` because the B charger AC feeder runs adjacent to the ESS-B feeder/bus route in the wide/zoom inspection views.
- `BUS-480B` to `CHGR-125B` is retained as `probable` because the visible `1B-480` charger feed is most consistent with the normal B 480 V feeder route, but the exact source landing is indirect.
- `CB-105` to `RELAY-K86A` and `CB-106` to `RELAY-K86B` are `probable` because the dashed lockout runs are visible across separate top/control crops rather than as one uninterrupted close-up edge.

## Exclusions and non-edges
- Did not add direct `BUS-1A-4.16KV` to `BUS-1B-4.16KV`; the tie is represented through `CB-TIE-1AB`.
- Did not add `BUS-480B` to `BUS-480E1B`; the overlapping Train B feeder geometry was treated as routing/crossing, not a named bus tie.
- Did not add charger-to-battery direct edges; both chargers and batteries terminate at their named DC buses.
- Did not add `UPS-BUS-A` to `UPS-BUS-B`; the rack zoom shows separate UPS buses, with only `UPS-BUS-A` feeding `INST-RACK-1`.
- Did not add RPS panel to instrument rack direct edges; vertical/horizontal crossings lack terminal dots and named terminations.
- Did not convert cable labels or WN wire points into nodes.

## Validation counts
- Nodes in matrix: 58.
- Undirected candidate edges: 61.
- Confidence counts: certain=56, probable=4, uncertain=1.
- Matrix shape: 58 rows by 58 columns, plus the row-label column/header.
- Diagonal forced to zero; matrix entries mirrored symmetrically from `round_01_diego_edges.csv`.
