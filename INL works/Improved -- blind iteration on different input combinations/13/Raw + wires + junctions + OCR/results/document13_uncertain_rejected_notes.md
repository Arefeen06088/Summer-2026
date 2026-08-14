# Document 13 Uncertain / Rejected Notes

Scope: extraction used only files in this document 13 folder: raw schematic, component label overlay/CSV, wire overlays/mask, and the prepared crop/contrast images in `codes`. No Ground Truth, evaluator output, GT-derived feedback, or off-the-shelf OCR was used.

## Included But Uncertain

- `ESFAS-LO-PERMISSIVE-A/B/C/D` to relay edges are low confidence. The notes explicitly say L.O. permissive from ESFAS near the relay areas, but individual ESFAS wires are not separately traced.
- `DIESEL-GEN-*-AUTO-START` edges to EDGs and diesel-generator breakers are low confidence control candidates. The labels are visually present near the EDG source paths, but the exact terminal endpoints are not drawn as ordinary point-to-point wires.
- `JB-*1 -- DC-BUS-*`, `LOCAL-IO-* -- JB-*1`, and `UPS-* -- PP-*1` are retained as low/medium confidence because the thin/dashed local I/O and rectangular auxiliary loops are visually connected but semantically different from the main solid power feeders.
- `PP-*1 -- GND-*` and `GND-* -- GND-PLANT` are included as grounding candidates. The individual and plant ground conductors are visible, but the panel/enclosure-to-ground semantics are less explicit than the main feeder paths.
- `BUS-4D -- ANNUNCIATOR-PLANT-PROCESS-COMPUTER` and `125VDC-SYSTEM-SHT-DC-2 -- DC-BUS-C` are off-page/continuation candidates with low confidence.
- `TR-SUT-1B -- BUS-4B` and `UNIT-GENERATOR-AUX-FEED -- TR-UAT-1B` are medium confidence because they are long routed feeder continuations across crop boundaries.

## Rejected / Not Listed As Edges

- Wire crossings without junction dots were not connected, following note 5 on the drawing.
- Title block, revision table, notes, legend, and cable/feed schedule text were not treated as nodes.
- Direct all-to-all edges among loads on the same MCC or load-center bus were not emitted; bus nodes (`LC-480*`, `MCC-*`, `BUS-4*`, `DC-BUS-*`) carry that shared connectivity.
- Direct `BAT-125* -- DC-BUS-*` edges were not listed because the visible path runs through `CHG-125*`.
- Direct `LC-480* -- CHG-125*` AC-input edges were not listed because no ordinary solid conductor is clearly visible from the LC bus to the charger symbol; the charger/DC-bus/battery path is retained instead.
- Components that are visually close but separated by non-junction crossings or gaps were not connected.
