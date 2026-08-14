# Round 1 Jennifer Notes

## Review scope

Inspected only doc 13 input resources, doc 13 generated artifacts/crops, and Diego round 1 files in the specified doc 13 folders. I used the raw schematic as the authority and the overlays/crops as navigation aids.

## Nodes kept

Kept the visually supported physical components from the component inventory, including relays, breakers, transformers, generators, batteries, chargers, inverters, UPS units, panels, disconnects, motors/loads, junction boxes, and grounds. Kept `SWYD-230` because it is visibly labeled in the raw top-left source chain even though it is absent from the detector inventory.

Kept the major named buses and bus-like sections: `BUS-4A` through `BUS-4D`, `LC-480A` through `LC-480D`, `MCC-*`, and `DC-BUS-A` through `DC-BUS-D`. Kept `LOCAL-IO-A` through `LOCAL-IO-D` only as external terminal endpoints because each appears at a drawn terminal tap on its 480 V load-center bus. Kept the two off-sheet labels only as external endpoint candidates, not as accepted connectivity.

## Nodes removed

Removed `AUTO-START-EDG-A` through `AUTO-START-EDG-D`: the text is visible but behaves as a note/annotation near EDG conductors, not a terminal component. Removed `ESFAS-LO-PERMISSIVE-A` through `ESFAS-LO-PERMISSIVE-D`: the labels are note text beside dashed control/trip regions, not actual named wiring endpoints. Removed `UNIT-GENERATOR-AUX-FEED`: it is a descriptive source label near `GEN-G1`/grounding, not a component or bus node.

## Edges kept

Accepted only visually direct solid-line power/ground connections and bus taps: the 230 kV source chain to `CB-101`, direct source transformer/breaker/bus links where a clean landing is visible, EDG breaker-to-associated-bus links, bus ties, 4.16 kV-to-480 V transformer chains, 480 V load-center taps to PP/MCC/JB/local terminal endpoints, MCC branch feeders, disconnect-to-load branches, DC bus-to-charger/inverter/UPS links, and the plant ground network.

Changed the battery connectivity from Diego's direct `BAT-125*` to `DC-BUS-*` edges to direct `BAT-125*` to `CHG-125*` edges. The raw DC/UPS crops show each battery symbol landing into its charger cluster; the separate direct battery-to-DC-bus connection is not clean enough to accept.

## Edges removed or left uncertain

Removed the accepted edge from `UNIT-GENERATOR-AUX-FEED` to `GND-A` because the source-feed text is not a node. Did not accept auto-start label edges, ESFAS note-to-relay edges, or off-sheet continuation edges as confirmed connectivity.

Moved cross-routing and control candidates to `round_01_jennifer_uncertain.csv`: SUT/UAT cross-bus interpretations, alternate EDG cross-bus interpretations, `CB-201` to `TR-UAT-1B`, LC-to-charger AC-input candidates, JB-to-DC-bus candidates, UPS-to-local-I/O candidates, relay-to-breaker dashed control/trip candidates, and the visible off-sheet continuation candidates. These may be real schematic relationships, but they are not clean direct physical edges from the visible drawing alone.
