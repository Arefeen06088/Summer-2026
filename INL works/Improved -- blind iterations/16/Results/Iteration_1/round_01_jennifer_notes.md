# Round 01 Jennifer Notes - Doc 16 / Iteration 1

## Source Boundary
- Used only the doc 16 raw input resources, generated crops/artifacts derived from those resources, the corrected component inventory, and Diego Round 1 files.
- Kept title/legend/note text, anonymous WN-* nodes, line ticks, pure crossings, cable labels, and enclosure borders out of the matrix.

## Node Decision
- Adopted the corrected 177-node inventory order from `component_inventory_doc16.csv`.
- Included `UCP-01` as a real physical component. The raw UCP/GND crops show a labeled rectangular UCP-01 box above the `GND-NO` ground symbol.
- Continued to exclude `PP-E1-480-125R` as drawing/title-block text.

## Removed Edges From Diego
- `BATT-125A -- CHGR-125A`: both components visibly tie to `BUS-125DC-A`; the adjacent dashed segment is not needed as a direct component-to-component edge when the named DC bus is modeled.
- `BATT-125B -- CHGR-125B`: same pattern on the B train with `BUS-125DC-B`.
- `CP-RPS-A -- PROT-UV-A`: the visible path runs through the labeled local `JB/DB-RPS-A` box, so a direct collapse to `PROT-UV-A` would skip an intervening physical item.
- `CP-RPS-B -- PROT-UV-B`: same pattern through the labeled local `JB-RPS-B3-1B` box.
- `RELAY-86A -- TB-3A`: the dashed route from `RELAY-86A` goes through the control-panel route near `CP-DCS-01`; it does not directly terminate at `TB-3A`.
- `RELAY-86B -- TB-3B`: the dashed route from `RELAY-86B` goes through the control-panel route near `CP-ANN-01`; it does not directly terminate at `TB-3B`.

## Added Edges
- `UCP-01 -- GND-NO`: solid down-lead from the UCP-01 box to the ground symbol labeled `GND-NO`.
- `UCP-01 -- BUS-120-RPS-A`: dashed conductor from UCP-01 left terminal to the visible end/dot of `BUS-120-RPS-A`.
- `UCP-01 -- BUS-120-RPS-B`: dashed conductor from UCP-01 right terminal to the visible end/dot of `BUS-120-RPS-B`.

## Reviewed And Retained
- `MG-RPS-A -- FT-AFW101`: retained; solid vertical linework terminates through the MG/FT column with no named intervening component.
- `RTD-RCS101 -- BUS-120-RPS-B`: retained; solid vertical RTD line continues to a dot on `BUS-120-RPS-B`.
- `XS-DOOR101 -- JB-CONTAIN`: retained; dotted signal line visibly routes between the XS door device and the `JB-CONTAIN` terminal.
- Backbone assignments retained: 4 kV source chains, `BUS-4KV-A/B`, 480 V transformer/incomer paths, `CB-TIE-4AB`, and `CB-TIE-480AB` match visible bus dots/crossings.
- MCC hierarchy retained: named bus -> feeder breaker -> MCC -> branch breaker -> relay -> load -> ground/TB, with no adjacent MCC or branch-breaker boundary expansion added.

## File Checks
- Node count: 177
- Edge count: 171
- Matrix mirror check: True
- Matrix diagonal zero: True
- Edge/matrix count agreement: True
- Unknown edge endpoints: 0
