# Document 20 Uncertain And Rejected Notes

## Scope Discipline

- Inspected only the allowed document 20 resource folder and its generated crops.
- Used the raw schematic as authority. The labels CSV and wire/node overlays were used only as visual aids.
- Did not use ground truth files, evaluator feedback, previous-document outputs, or off-the-shelf OCR.

## Medium Or Low Confidence Included Edges

- `BUS-480-A` to `RECT-125A` and `BUS-480-C` to `RECT-125B` are included as medium confidence power edges. The raw drawing shows solid vertical AC-side feeds descending from the 480 V load-center area into the rectifiers, but no separate breaker label is visible on those rectifier feeds.
- `INV-UPS-A` to `UPS-A AC OUTPUT` and `INV-UPS-B` to `UPS-B AC OUTPUT` are included as low confidence logical AC-output stubs. The inverter AC-side dashed horizontal stubs are visible, but no labeled receiving component is visible on the crop.
- `CS-4A` to `HTR-PZR-01A`, `CS-4B` to `HTR-SUMP-02B`, and `CS-6A` to `MOT-CRN-01A` are included as medium confidence control edges because the raw lines are dashed even though the terminal symbols are load-like devices.
- `RELAY-K101` to `LT-512A` and `RELAY-K103` to `LT-512B` are included as medium confidence `instrument_signal` edges. The branches to the level transmitters are visible, but the dashed versus dot-dash style is less distinct than the pressure transmitter branches.
- `RELAY-K106` and `RELAY-K108` to `A/B ESF INTERLOCK` are included as medium confidence logical interlock edges. The lower center dashed loop is clearly labeled, but the edge list abstracts the continuous loop into a logical node.

## Rejected Or Not Promoted

- Crossings without black junction dots were rejected as non-connections per the visible notes and raw geometry.
- Repeated short tick marks along bus bars were rejected as bus markings rather than taps.
- Large dashed zone/enclosure boundaries around the control and DC regions were rejected as non-conductors.
- Right-side title block, revision table, border grid, and line legend samples were rejected as drawing artifacts.
- `N.O. BUS TIE`, `480V TIE`, and wire-size text such as `3/C #2 AWG` were treated as annotations, not nodes.
- Small unlabeled squares next to `GEN-M1`, `DG-1A`, and `DG-1B` were reviewed but not promoted to separate canonical nodes because they have no readable tags. The adjacent generator-to-breaker edges were retained.

## Coverage Notes

- Top source and bus area includes the main generator, 230 kV feed, 13.8 kV buses, 4.16 kV buses, diesel generators, transformers, disconnects, and all tie breakers.
- 480 V area includes load centers A through D, the 480 V tie breaker, and all 24 feeder columns through breaker, disconnect, MCC/JB, relay/control switch, and terminal load.
- DC and UPS area includes both battery/charger/rectifier strings, both 125 VDC control buses, and both UPS inverters.
- Lower controls include RPS A/B, ESFAS A/B, terminal or junction blocks, protection modules, relay branches, instruments, annunciators, grounds, and the A/B ESF interlock.
