# Document 15 Uncertain And Rejected Notes

Scope used: only the raw drawing and provided aids in this document 15 folder, especially the raw image, component labels CSV, wire-node overlay/CSV, and evidence crops. No ground truth, evaluator output, metric feedback, previous documents, or off-the-shelf OCR were used.

## Included With Uncertainty

- DG/NSS shared risers: each diesel-generator riser visually intersects the NSS busbar before continuing to the CB-DG breaker. I included DG-to-CB-DG as high-confidence solid power and NSS-to-CB-DG as medium-confidence visual bus-tap/shared-source connectivity because the junction dot is visible but the physical intent is somewhat schematic-specific.
- AB/CD sequence and RPS controls: SEQ-1AB, RPS-AC-1, SEQ-2CD, and RPS-AC-2 are not present in the component CSV but are visible in the raw/crop images. I added them as logical control nodes and connected them to the dashed vertical control paths. I also included low-confidence associations from each sequence/RPS block to the nearby tie breaker because the blocks sit inside the dashed normally-open tie/control enclosure, even though a direct lead to the tie breaker is not explicitly drawn.
- Feeder-06 to terminal-block drops: each division has a dashed lead descending from the sixth MCC feeder relay/control area into the lower terminal block. I included RLY-A06/B06/C06/D06 to TB-1A/B/C/D as low-confidence dashed control paths because the vertical dashed trace is visible but passes through a long unlabelled run.
- Battery-to-charger links: the lower DC crop shows dashed or weak linework from each battery to its charger. These were included as medium-confidence dashed DC/control paths rather than high-confidence solid power.

## Rejected Or Not Connected

- Wire crossings without junction dots were not treated as connections.
- Dashed division boundaries, equipment-zone boxes, crop/overlay labels, title-block/grid lines, and legend examples were not treated as electrical connectivity.
- BUS-SWY-1 and BUS-SWY-2 are connected only through CB-SWY-TIE; no direct bus-to-bus edge was added.
- BUS-NSS-1 and BUS-NSS-2 are kept separate; no direct NSS tie is visible.
- BUS-416A/B and BUS-416C/D are connected only through the visible breaker/disconnect tie paths; no direct class-1E bus-to-bus edge was added.
- 480 V load-center buses A/B/C/D and MCC buses A/B/C/D are kept per-division; no cross-division 480 V or MCC ties are visible.
- Grounds GND-A/B/C/D are individual references from their matching DC buses and were not connected to each other.
- Relay coils were associated with their matching feeder breaker through dashed trip/control leads, but I did not add relay-to-load solid power edges because no solid conductor from the relay symbol to the load is drawn.
