# Round 01 Jennifer Connectivity Notes

## Accepted Node Policy

- Kept Diego's 190 visually detected physical component labels and the 10 visually printed logical bus nodes: `BUS-13K-A`, `BUS-13K-B`, `BUS-416-A`, `BUS-416-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `BUS-125DCA`, and `BUS-125DCB`.
- Kept logical BUS-* nodes as bus representatives instead of expanding components sharing a bus into direct cliques.
- Did not add WN-* wire nodes, arbitrary intermediate junction dots, cable/boundary segments, or section titles such as AC/DC distribution headings.
- Node removals: none.
- Node additions: none.

## Accepted Edge Categories

- Accepted the solid single-line source, transformer, breaker, disconnect, tie, diesel-generator, and 480 V load-center paths where the conductor visibly terminates at each named component or bus.
- Accepted the repeated 480 V feeder branches as bus-to-breaker, breaker-to-disconnect, disconnect-to-MCC/JB, and MCC/JB-to-relay/control-switch/load chains.
- Accepted the dashed 125 VDC source chains from `BAT-125A - CHGR-125A - RECT-125A - BUS-125DCA` and `BAT-125B - CHGR-125B - RECT-125B - BUS-125DCB`; the dashed conductors visibly terminate at each source component and at the 125 VDC bus.
- Accepted the inverter taps `INV-UPS-A - BUS-125DCA` and `INV-UPS-B - BUS-125DCB`; each dashed vertical tap lands on the printed bus.
- Accepted the lower RPS and ESFAS control-panel drops and device chains where the dashed or solid line terminates at both named endpoints.
- Accepted the long A/B ESF interlock `RELAY-K106 - RELAY-K108`; the dashed run is labeled as the A/B ESF interlock and visually ties the K106 branch to the left side of K108, while not landing on K107.

## Refinements From Diego

- Added visually supported omitted AC-feed edges: `BUS-480-A - RECT-125A`, `BUS-480-C - RECT-125B`. `RECT-125A` has a solid upper feed from the 480 V load center A bus, and `RECT-125B` has the analogous solid upper feed from the 480 V load center C bus.
- Removed/rejected Diego candidates: none. The reviewed high-recall dashed candidates were supported closely enough to keep.

## Uncertain Candidates Kept Out

- Did not add any unlabeled intermediate wire nodes, junction dots, dashed boundary-box contacts, or section-title nodes.
- Did not add direct component cliques across any printed bus; bus-tapped equipment remains connected through the corresponding BUS-* node.
- Did not add an ESF interlock edge to `RELAY-K107`; the visible interlock route terminates at the K108 side, not the K107 instrument branch.
- Did not add AC-side inverter source edges because no clear named upstream endpoint was visible for those inverter boxes beyond the 125 VDC bus tap.

## Validation Summary

- Node count: 200
- Edge count: 202
- Matrix is symmetric: yes
- Matrix diagonal is zero: yes
- Row and column labels are identical and in the same order: yes
