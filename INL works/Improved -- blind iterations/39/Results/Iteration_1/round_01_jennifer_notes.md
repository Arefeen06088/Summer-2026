# Round 01 Jennifer Precision Review Notes

## Scope

Reviewed only the allowed input resources, current aids derived from those inputs, and Diego's round 01 files. The raw schematic image was treated as authoritative; overlays and crops were used only as navigation aids.

## Node Refinements

- Removed `LC-A` and `LC-B` as final nodes. They appear as end labels for `BUS-480-A` and `BUS-480-B`, not separate electrical terminals.
- Removed `CONTROL-ROOM-ANNUNCIATION` as a final node. It is route text under the lower dashed wiring, not a distinct component or bus endpoint.
- Kept the named physical components, explicit 4160/480 buses, and `GND-PLANT` where the raw symbols/labels are visible.

## Edge Refinements

- Kept solid power paths only through visible intervening devices: offsite sources through disconnects/transformers/breakers, the A/B bus tie through `CB-TIE-AB`, and 4160-to-480 feeds through the 480 transformers and breakers.
- Replaced Diego's `BUS-4160-*` to `CHG-125*` charger feeds with `BUS-480-*` to `CHG-125*`. The visible solid conductor lands at the 480 V load-center end label and charger terminal; no clear 4160-to-charger terminal is visible.
- Kept the DC stack sequences where vertical stack conductors visibly touch the component boxes: charger to battery to inverter to panel to RPS.
- Kept short, visible dashed control/sensing edges: 4160 bus to UV relay, RPS to local relay, MOVs to their junction boxes, and `ANN-CR01` to `REC-SOE01`.
- Excluded the lower `CONTROL ROOM ANNUNCIATION` route as a logical bus and removed Diego's taps to it.
- Marked the long `RPS-A` to `JB-A101` and `RPS-B` to `JB-B101` dashed routes uncertain. They are visually plausible, but too long and route-like for a precision keep.
- Removed `JB-A101` to `ANN-CR01` and `REC-SOE01` to `JB-B101`: the zoomed lower crop shows gaps rather than short box-to-box dashed connections.
- Removed `MCC-A1` to `RELAY-KA1`: the solid load routing passes near the relay but does not land on a relay terminal.

## Diego Disagreements

- Diego over-promoted `LC-A`, `LC-B`, and `CONTROL-ROOM-ANNUNCIATION` into final nodes.
- Diego kept charger feeds from the 4160 buses; the clearer raw connection is from the 480 buses to the chargers.
- Diego's logical lower control bus collapsed several visually separate dashed route/annotation features.
- Diego was correctly cautious on the long RPS-to-JB routes; I retained them as uncertain and excluded them from the matrix.

## Follow-Up

A targeted Diego round would be useful only for the long RPS-to-JB control-routing ambiguity and charger-feed confirmation. The solid power topology appears stable after this precision pass.
