# Round 1 Diego Notes

## Scope and policy

Inspected only doc 13 Input resources and generated doc 13 artifacts/crops under the paths specified in the task. The raw schematic is treated as authoritative; component/OCR overlays, wire masks, and wire-node overlays were used as navigation aids only.

Nodes include visually supported labeled physical components, major named buses, grounds, and named logical/off-sheet nodes. Anonymous wire-node IDs from `wire_nodes.csv` are not included because the task asks to avoid intermediate topology points unless they are named bus/node concepts. Thick bus-like assemblies such as `BUS-4A`, `LC-480A`, `MCC-A1`, and `DC-BUS-A` are represented as connectivity nodes even when the component detector also treated the label as a component.

## Label fixes and additions

`SWYD-230` is visible in the raw top-left source crop between `GRID-230KV` and `DS-101`, but it is not in the 178-row component inventory. I added it as a physical component.

Added named bus/logical nodes visible in raw crops: `BUS-4A` through `BUS-4D`, `DC-BUS-A` through `DC-BUS-D`, `LOCAL-IO-A` through `LOCAL-IO-D`, `ESFAS-LO-PERMISSIVE-A` through `ESFAS-LO-PERMISSIVE-D`, `AUTO-START-EDG-A` through `AUTO-START-EDG-D`, `UNIT-GENERATOR-AUX-FEED`, `CONTINUATION-125VDC-SHT-DC-2`, and `TO-ANNUNCIATOR-PLANT-PROCESS-COMPUTER`.

## Bus and ground choices

`BUS-4A`/`BUS-4B`/`BUS-4C`/`BUS-4D` are the labeled 4.16 kV train buses. `LC-480*` labels are used as the 480 V load-center buses. `MCC-*` labels are used as the named motor-control-center bus sections feeding branch breakers. `DC-BUS-*` labels are used as 125 VDC bus nodes for battery, charger, inverter, and UPS connectivity.

`GND-A`, `GND-B`, `GND-C`, `GND-D`, and `GND-PLANT` are included as ground nodes. The overview and lower crops show the individual grounds connected through the plant grounding network, so those edges are high-confidence. Grounding conductors were not expanded into anonymous intermediate route points.

## Accepted high-confidence pattern

High-confidence edges emphasize direct solid-line connections: source-to-switchgear chains, bus ties, transformer/breaker/load-center feeds, LC-to-MCC/PP/JB taps, MCC branch feeders, disconnect-to-load branches, DC-bus to battery/charger/inverter/UPS, and the common ground network. For the repeated train patterns, I used the local crop for each train and only generalized where the same labeled feeder geometry is visible.

## Plausible/uncertain pattern

The plausible file captures high-recall candidates where geometry or semantics are visually supported but not clean enough for high-confidence. This includes SUT/EDG top-source cross-routing around A/B, UAT lower-source cross-routing around C/D, AC inputs to battery chargers, JB-to-DC/local-I/O relationships, UPS-to-local-I/O outputs, diesel auto-start logical labels, ESFAS permissive dashed control/trip relationships, and off-sheet continuations.

Dashed/control/trip lines are deliberately kept out of the power-feeder high-confidence set unless the relationship was a direct named component-to-component drawing feature. The notes box says dashed lines denote control/trip circuits and crossings without dots are not connected, so dashed ESFAS and relay/control associations are proposed as plausible logical/control edges rather than accepted power edges.

## Difficult regions

The upper source region around `TR-SUT-1A`, `TR-SUT-1B`, `EDG-A`, `CB-DGA`, `EDG-B`, and `CB-DGB` has thin long source/control-looking conductors near the thick 4.16 kV bus and the A/B tie. I accepted the obvious associated-train EDG breaker-to-bus feeds but kept cross-bus/SUT-B interpretations plausible.

The lower source region around `GEN-G1`, `CB-201`, `TR-UAT-1A`, `TR-UAT-1B`, `EDG-C`, `EDG-D`, and `CB-TIE-CD` has long source conductors that overlap the C/D bus area. Direct associated-train UAT and EDG feeds are high-confidence; cross-routing between UATs and the opposite bus is plausible only.

The DC/UPS/local-I/O areas are visually dense. Battery, charger, DC bus, inverter, and UPS vertical connections are clear. The LC AC input to chargers, JB-to-DC/local-I/O path, and UPS output to local I/O are visually/semantically likely but left plausible.
