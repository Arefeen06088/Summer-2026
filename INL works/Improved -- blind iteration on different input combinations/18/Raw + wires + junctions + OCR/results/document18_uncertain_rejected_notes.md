# Document 18 Extraction Notes

## Sources Used

Worked only from the document 18 folder contents: the raw schematic image, component label overlay, wire mask/overlay, wire node overlay, `component_visual_ocr_labels.csv`, and `wire_nodes.csv`. I did not use Ground Truth, evaluator feedback, files outside the folder, or off-the-shelf OCR.

## Modeling Choices

- Added logical bus nodes for the drawn busbars: `BUS-SWYD-230`, `BUS-4160A`, `BUS-4160B`, `BUS-480A`, `BUS-480B`, `BUS-480C`, `BUS-480D`, `BUS-125A`, `BUS-120A`, `BUS-125B`, and `BUS-120B`.
- Added `BUS-GEN-TERMINAL` for the common conductor after `CB-GEN-ISO` that visibly ties `GEN-MAIN-1` to `TR-UAT-1A` and `TR-UAT-1B`.
- Preserved mediated connectivity. The 4.16 kV bus tie is represented as `BUS-4160A -- CB-4160-TIE -- BUS-4160B`; transformer incoming breakers and feeder breakers are not collapsed into direct bus-to-load edges.
- Modeled the Train A and Train B dashed RPS/control wiring as `RPS-A-DASHED-NET` and `RPS-B-DASHED-NET`. The dashed bundles visibly connect the PLC/relay/junction/annunciator groups, but the exact point-to-point sequence is not unique from the drawing.
- Feeder chains under the 480 V busbars were represented in their visible vertical order: busbar to breaker, then disconnect/fuse/flow switch/relay/control panel/motor starter as drawn, then the terminal load.

## Crossing Policy

No crossing was treated as connected unless there was a filled dot, a clear T-section/landing on a busbar, or a component terminal landing. Faint sheet grid lines, border ticks, title-block rules, and legend/notes graphics were rejected as artifacts. Vertical feeder lines that pass through page/grid/background markings were not connected to those markings.

## Medium-Confidence Edges

- `CB-GRID-A -- CB-SWYD-230` and `CB-GRID-B -- CB-SWYD-230`: the compact top-left switchyard source geometry is visually plausible as both grid source paths feeding the switchyard breaker before `BUS-SWYD-230`, but the small symbols are dense.
- `BUS-480B -- CHG-125A` and `BUS-480C -- CHG-125B`: the long solid drops from the 480 V buses into the Train A/B control-power boxes are clear, but the exact first device on the charger/rectifier row is compact. I attached each to the charger row endpoint for high recall.
- All `RPS-*-DASHED-NET` edges are medium confidence because the dashed control wiring shows network membership more clearly than exact individual conductor order.

## Rejected / Not Promoted

- Title block, legend, notes, border, and sheet-grid graphics were not promoted to nodes.
- Unlabeled `wire_nodes.csv` endpoints were used only as geometry evidence unless they corresponded to a labeled component, logical busbar, or explicit junction role.
- Dotless wire crossings were rejected as non-connections even when the wire mask visually overlaps due to line thickness.
