# Diego Round 01 Notes

Scope: blind extraction for Improved doc 10 Iteration_1 using only the raw schematic/input resources and current input-derived aids. Ground truth, evaluator/scoring outputs, prior results, archived result folders, and tracker metrics were not used.

## Rationale

- Kept named physical components from the current component/OCR inventory and added raw-visible TR-UPS-A and TR-UPS-B, which are clearly labeled on the schematic even though they were omitted by the current CSV aid.
- Added only visible logical electrical buses: BUS-SWY-345KV, BUS-4160-A, BUS-4160-B, BUS-480V-LC-FEEDERS-A/B, BUS-DC-A/B, and BUS-UPS-A/B.
- Treated solid lines as power, dashed as control, dotted as signal, and dash-dot as ground/reference, matching the visible legend.
- Preserved named breakers, fuses, disconnects, transformers, MCCs, load centers, panels, terminal blocks, junction boxes, and grounds rather than shortcutting across them.
- Treated BUS-480V-LC-FEEDERS-A/B as logical bus nodes because the raw geometry labels a common solid conductor feeding the fan/load-center region.
- Used line breaks/crossing gaps to avoid false junctions, especially around the transformer/pump branch conductors and long cable-tray runs.

## Excluded Annotation Labels

Excluded as non-final nodes: CLASS-1E-DIV A/B headings, 4.16 kV / 480 V / UPS class labels, CT-CAB-A/B control cable tray labels, MCR / ANNUNCIATOR CONTROL BAY heading, DIVISION BOUNDARY, PHYSICAL SEPARATION CLEARWAY, DC/UPS TRAIN A/B labels, notes, legend entries, title/revision block text, sheet border/grid coordinates, and wire-node/intermediate WN-* labels.

## Uncertainty Highlights

- CB-A09/FUSE-A01 and CB-B09/FUSE-B01 have visually plausible dotted/protective-route relationships, but the exact terminal endpoint is partly obscured; included as uncertain only.
- CT-4160-A/B dotted routes toward CB-A08/B08 are plausible breaker-signal links, but not clean enough for the matrix.
- Long dashed cable-tray routes from switchgear/low-voltage terminal areas to the MCR/UPS regions are preserved as uncertain where endpoints are ambiguous.
- Ground edges were kept only from BUS-DC-A/B to GND-A/B where the dash-dot ground/reference route visibly reaches the lower ground symbols.
- The lower MCC-102/MCC-103 shared-conductor area near PUMP-CCW and FAN-AB is visually plausible as a shared region; clearer MCC-to-load edges are kept, direct pump-to-fan links are uncertain.

## Counts

- Final nodes: 120
- Edge candidates: 152 total, 134 keep, 13 uncertain, 5 remove
- Matrix edges: 134 keep edges only
