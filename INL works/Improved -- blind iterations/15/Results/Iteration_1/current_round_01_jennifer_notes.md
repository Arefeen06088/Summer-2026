# Current Round 01 - Jennifer Precision Notes

## Source Boundary And Node Policy
- Reviewed only doc 15 input resources, current doc 15 support artifacts, and Diego's current Round 1 files allowed for this task.
- Used the exact 183-node order from `component_inventory_doc15_current.csv`.
- Did not add WN-* wire nodes, anonymous junctions, enclosure boundaries, schedule/legend/title text, division labels, feeder note labels, or `OFFSITE SOURCES`.
- I did not find a clear visual node inventory mistake; the current inventory is retained unchanged.

## Accepted Topology
- Top switchyard: `GEN-101 -> CB-GEN-101 -> TR-GSU-1 -> BUS-SWY-1`, `GEN-102 -> CB-GEN-102 -> TR-GSU-2 -> BUS-SWY-2`, with `BUS-SWY-1 -> CB-SWY-TIE -> BUS-SWY-2` as the only switchyard bus tie.
- Station service taps: `TR-UAT-1` and `TR-SAT-1` connect from `BUS-SWY-1` to `BUS-NSS-1`; `TR-UAT-2` and `TR-SAT-2` connect from `BUS-SWY-2` to `BUS-NSS-2`.
- Medium-voltage divisions: each NSS feeder lands on its matching normal-feed breaker, each DG lands on its DG breaker, each DG/normal-feed breaker lands on the matching 4.16 kV bus, and each 4.16 kV bus feeds `CB-TX-* -> TR-480* -> BUS-480* -> MCC-1*`.
- Tie breakers: A/B is retained only as `BUS-416A -> CB-TIE-AB -> DS-TIE-AB -> BUS-416B`; C/D is retained only as `BUS-416C -> CB-TIE-CD -> DS-TIE-CD -> BUS-416D`.
- MCCs: retained six solid feeder chains per division as MCC-to-breaker-to-disconnect/fuse-to-load, plus the matching breaker-to-relay dashed lead where the dashed line visibly lands on the relay block.
- DC/control: retained the visible battery/charger/DC bus/inverter/control-panel/terminal-block/junction-box/ground chains. Grounds are included only for the bus-to-ground dashed conductor that visibly lands on the ground symbol.

## Removed Diego Edges
- `SEQ-1AB -- RPS-AC-1`: removed because the two blocks share dashed side risers, but the crop does not show a direct named block-to-block landing.
- `SEQ-2CD -- RPS-AC-2`: removed for the same reason; shared risers are not treated as a direct relay-to-relay edge without WN junction nodes.

## Retained Uncertain Or Lower-Confidence Edges
- `BUS-NSS-1 -- DG-1A` and `BUS-NSS-2 -- DG-1C` remain uncertain. The DG symbols are drawn inline with the NSS bus, but symbol overlap cannot be completely excluded. No analogous NSS edge is added for `DG-1B` or `DG-1D`.
- Tie-control edges from `SEQ-1AB`/`RPS-AC-1` to `CB-DG-A` and `CB-NF-B`, and from `SEQ-2CD`/`RPS-AC-2` to `CB-DG-C` and `CB-NF-D`, remain uncertain. The named blocks visibly land on shared dashed risers, but no WN junctions were added and I avoided extra tie-device fan-out.
- `RLY-A06/B06/C06/D06 -- TB-1A/B/C/D` remain uncertain. The dashed lead leaves the sixth relay area and reappears landing on the terminal block, but the middle span is mostly open sheet.

## Isolated Nodes
- Isolated nodes after refinement: none.

## Saturation Judgment
- I agree visual saturation is reached for the current source set. A Diego re-review is not needed unless the project decides dashed control associations should be excluded categorically rather than retained as lower-confidence connectivity.

## Output Summary
- Jennifer edge proposals written: 196.
- Removed Diego edge proposals: 2.
- Matrix size: 183 x 183 plus leading `node_name` column.
