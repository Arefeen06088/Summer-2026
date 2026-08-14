# Document 27 Round 02 Jennifer Notes

## Scope

- Blind precision review used only the allowed document-27 folder: raw/overlay/crop images, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, crop index files, Diego round01 outputs, and `codes/build_matrix_from_edges.py`.
- No Ground Truth, GT-derived feedback, evaluator outputs, or off-the-shelf OCR were used.

## Kept / Removed / Renamed Summary

- Renamed logical source bus `BUS-13.8KV` to `BUS-13KV-N` because the top-band crop visibly prints `BUS-13KV-N`.
- Kept manually added `PANEL-CTRL-MAIN`; it is visibly printed below the central CTRL panel in `labels__row2_col2.png`.
- Kept manually added `GND-EQ-B`; it is visibly printed beside the right ground symbol in `labels__row3_col3.png`.
- Rejected `TE-41` as an included graph node and removed `CB-TIE-41 -- TE-41`; raw/labels/wires row1-col2 crops do not show a distinct TE symbol or connected signal line below `CB-TIE-41`.
- Removed `DS-A10 -- CHGR-125A`; the A charger is fed by its own visible solid bus tap, not through the A10 disconnect branch.
- Added `BUS-480-A -- CHGR-125A` as a medium-confidence power feeder matching the visible unlabelled charger tap pattern also present for `CHGR-125B`.
- Added `DS-A10 -- JB-A10` as a high-confidence power feeder to restore the visible A10 branch pattern: bus -> `CB-A10` -> `DS-A10` -> `JB-A10`.
- Kept `BUS-480-B -- CHGR-125B` as medium confidence; the bus tap into the charger is visible, but no separate breaker label is printed.
- Kept `DC-BUS-125A -- DC-BUS-125B` as medium confidence; the horizontal DC bus band is visibly continuous, though A/B logical separation remains schematic-style.
- Kept `DC-BUS-125A -- PANEL-CTRL-MAIN` as medium confidence and removed duplicate direct `DC-BUS-125B -- PANEL-CTRL-MAIN` to avoid overconnecting one visible panel tap.
- Kept `BUS-480-C -- GND-EQ-A` and `BUS-480-D -- GND-EQ-B` as medium-confidence ground edges following the dash-dot DC/ground style to labelled ground symbols.
- Retained regular A/B/C/D load-center branch chains where visually present and avoided direct bus-to-device shortcuts except the separately tapped charger feeders.
- No additional source, generator, transformer, DG, 4160 bus, 480 C/D transformer input, charger, battery, or DC-bus feed was found missing after the above A charger correction.

## Counts

- Node CSV rows: 201 total.
- Included final nodes in matrix: 200 (`TE-41` is marked `decision=reject`).
- Included final edge rows: 201.
- Unique undirected edges: 201.

## Validation

- Matrix built with `python codes\build_matrix_from_edges.py results\document27_round02_jennifer_edges.csv results\document27_round02_jennifer_nodes.csv results\document27_round02_jennifer_adjacency_matrix.csv results\document27_round02_jennifer_matrix_summary.json`.
- No unknown endpoints.
- No duplicate undirected pairs.
- Matrix is symmetric.
- Matrix diagonal is zero.

## Remaining Uncertainty

- `BUS-480-A -- CHGR-125A` and `BUS-480-B -- CHGR-125B`: visible solid taps are clear, but the branch devices are unlabelled as breakers, so both remain medium confidence.
- `DC-BUS-125A -- DC-BUS-125B`: visual continuity is clear, but the drawing does not fully disambiguate whether the A/B labels denote one continuous DC bus band or two logical sections.
- `DC-BUS-125A -- PANEL-CTRL-MAIN`: the panel tap is visible, but the exact A/B side assignment is ambiguous; round02 keeps only the A-side direct edge plus the DC bus tie.
- `BUS-480-C -- GND-EQ-A` and `BUS-480-D -- GND-EQ-B`: ground paths are visible via dash-dot style, but the graph-level attachment is represented as a medium-confidence bus-to-ground edge.
