# Round 01 Jennifer Notes - Doc 41 / Iteration 1

## Scope and node policy
- Reviewed Diego Round 1 from the allowed doc 41 corrected inventory, input resources, and inspection crops only.
- Kept the corrected inventory order exactly for the matrix: 58 nodes.
- Kept named components, named buses, `JB-ESF-01`, relays, panels, UPS/DC buses, and `GND-1E` as nodes.
- Excluded region boxes, title/legend/reference/terminal tables, notes, cable labels, WN-* wire points, and pure crossings.
- Did not collapse through named buses, panels, relays, junction boxes, or `JB-ESF-01`.

## Changes from Diego Round 1
- Removed `BUS-480E1B` -- `CHGR-125B`. The right-side raw zoom shows the CHGR-125B AC feeder running on the separate right-side `CABLE 1B-480-9` route; it passes near the ESS-B area but has no visible terminal landing on `BUS-480E1B`.
- Kept `BUS-480B` -- `CHGR-125B` as `probable`. The source is supported by the 1B-480 feeder label/routing and the absence of an ESS-B bus landing, but the exact BUS-480B terminal landing is not as cleanly exposed as the Train A charger source.
- Updated `BUS-480A` -- `CHGR-125A` to `certain`; the Train A charger feed visibly leaves the BUS-480A left terminal and lands on CHGR-125A.
- Retained the remaining Diego edges after visual review of the top 4.16 kV, transformer/480 V, MCC load, vital DC/UPS, rack, and dashed-control crops.

## Rejected edges and non-edges
- Rejected `BUS-480E1B` -- `CHGR-125B` as an overconnection from adjacent routing/alternate bus landing.
- Did not add `BUS-480B` -- `BUS-480E1B`; the buses are adjacent with nearby feeder routing but no named bus-tie connection.
- Did not add `UPS-BUS-A` -- `UPS-BUS-B`; the center zoom shows separate UPS buses.
- Did not add `UPS-BUS-B` -- `INST-RACK-1` or RPS-panel-to-rack edges; only `UPS-BUS-A` has the visible rack feed.
- Did not add charger-to-battery direct edges; chargers and batteries land through the named DC buses.
- Did not add direct relay-to-JB edges; the dashed wiring runs through the named RPS panels.

## Uncertain/probable cases retained
- `BUS-480B` -- `CHGR-125B`: retained as `probable` due to the 1B-480 feeder route, while excluding the unsupported ESS-B alternative.
- `CB-105` -- `RELAY-K86A` and `CB-106` -- `RELAY-K86B`: retained as `probable`; the dashed lockout leads leave the breakers and reappear at the matching relay area, but the full run is distributed across crops.

## Final validation counts
- Nodes in matrix: 58.
- Undirected edges: 60.
- Confidence counts: certain=57, probable=3, uncertain=0.
- Matrix shape: 58 rows by 58 columns, plus the row-label column/header.
- Matrix is symmetric; diagonal forced to zero.
- Matrix one-count: 120 total directed entries, matching 2 x 60 undirected edges.
