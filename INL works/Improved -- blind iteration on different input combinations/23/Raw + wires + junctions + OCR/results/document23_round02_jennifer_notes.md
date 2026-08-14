# Document 23 Round 02 Jennifer Notes

## Method
- Worked only inside the allowed document 23 resource folder.
- Reviewed Diego round-01 as a proposal against the raw schematic first, then the provided label/wire/node overlays and precision crops.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, Tesseract, RapidOCR, or other off-the-shelf OCR.
- Kept Diego's node set and order unchanged: 200 nodes, including the visible added `DC-DC-1` node.

## Validation Counts
- Node count: 200
- Edge count: 208
- Edge kind counts: {'power_solid': 142, 'control_signal_dashed': 42, 'instrument_dashed': 14, 'ground': 10}
- Confidence counts: {'high': 178, 'medium': 30}
- Unknown nodes in edges: 0
- Duplicate undirected pairs: 0
- Adjacency matrix: symmetric with zero diagonal

## Main Accepted Connectivity
- Kept the 4160 V source chains, 4160 tie/ESF buses, diesel/ATS feeders, 480 V feeder/main/MCC load-center chains, DC distribution chains, and UPS/inverter chains where Diego's edges matched visible solid wiring.
- Kept `BUS-4160-ESF-A -> CB-1C-FDR` and `BUS-4160-ESF-A -> CB-2C-FDR` as medium-confidence ESF-A feeder sources. The visible lower ESF-A routing/dots support these paths, but the long runs and nearby crossings keep them below high confidence.
- Verified `BUS-480-2A -> CB-DC-A` and `BUS-480-2B -> CB-DC-B` as solid branch feeds into the 125 VDC rectifier section.
- Kept `DC-DC-1` as a visible added node. Its adjacent modeled connections are `BUS-120AC-A -> DC-DC-1` and `DC-DC-1 -> BUS-24DC-C`.

## Precision Pruning From Diego
- Removed six direct heater-to-first-relay shortcuts: `HTR-H105/H135/H165/H205/H235/H265 -> RELAY-K*1`. The raw load-center blocks show nearby local control stubs, not direct heater-to-relay conductors.
- Removed six direct XV-valve-to-second-relay shortcuts: `VALVE-XV106/XV136/XV166/XV206/XV236/XV266 -> RELAY-K*2`. The supported valve control adjacency is through the local JB/control segment.
- Removed six extra `JB-* -> RELAY-K*2` shortcuts. Each repeated load-center block is modeled conservatively as `PNL -> JB`, `JB -> XV`, `JB -> RELAY-K*1`, and `RELAY-K*1 -> RELAY-K*2`.
- Removed `FUSE-FU-A -> RELAY-KA1` and `FUSE-FU-B -> RELAY-KB1`. The fuses are solid taps from the 120 VAC buses, while the relay/annunciator chains are separate dashed control runs.
- Removed `BUS-24DC-C -> PNL-DCS-A`, `BUS-24DC-C -> PNL-DCS-B`, and `BUS-24DC-C -> RELAY-KTIE`; these are nearby bottom-strip elements without a clear direct adjacent bus edge.

## Edge Kind And Confidence Changes
- Reclassified `BUS-24DC-C -> JB-CTRL-A` and `BUS-24DC-C -> JB-CTRL-B` from `control_signal_dashed` to `power_solid` because the retained adjacency is to the lower 24 VDC solid bus node, not the dashed DCS-to-JB control line.
- Raised confidence on the visually clear 480 V to DC feeder branches and the solid 120 VAC taps to the RPS panels.
- Kept local load-center relay/JB control links at medium confidence where the visible short control stub is small or partially obscured by component symbols.

## Remaining Ambiguities
- The 1C and 2C feeder sources remain medium confidence because their source runs are long and pass near other conductors, even though the visible junction evidence favors `BUS-4160-ESF-A`.
- The lower `BUS-24DC-C -> JB-CTRL-A/B` taps remain medium confidence because the 24 VDC bus and dashed control/JB graphics are tightly packed.
- Bottom RPS/control-strip edges are undirected adjacency abstractions of visible dashed wiring, not signal direction or functional logic.
