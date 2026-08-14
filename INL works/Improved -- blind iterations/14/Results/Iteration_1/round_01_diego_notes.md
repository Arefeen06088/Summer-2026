# Diego Round 01 Notes - Improved doc 14, Iteration 1

## Scope and allowed inputs used

Used only the supplied raw schematic/current crop images plus `component_labels_list_current.csv`, `component_visual_ocr_labels.csv` as a label aid, and `wire_nodes.csv`/wire-node overlays as geometry aids. I did not use GT, scoring/evaluation outputs, prior results, archives, or prior completed matrices.

## Included nodes

- Started from the 166 current detected named components in `component_labels_list_current.csv`.
- Added explicit bus/logical nodes visible in the raw/current crops: `BUS-4A`, `BUS-4B`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-UPS-A`, `BUS-UPS-B`.
- Added raw-visible named components missed by the current component CSV: `FS-B03`, `PANEL-MCR`, `PANEL-ANN`, `INV-120B`.
- Grounds with explicit labels were retained as named nodes.
- Anonymous wire-node points such as `WN-*` were used only as geometry aids and are not present in the final node list.

## Edge/evidence logic

- Solid power/feeder segments were included when the line visibly terminates at two named components or at a named bus/component endpoint.
- Breaker-to-relay edges are included as control edges where the local dashed lead terminates at the breaker area and named relay symbol.
- Terminal-block-to-instrument edges are included where the short signal/instrument lead visibly terminates at the terminal block and instrument circle.
- Relay-to-panel edges are included at lower confidence when a dashed vertical/control route clearly drops from that feeder relay channel into a named panel/control corridor; exact panel assignment is based on visible routing/grouping in the current crops.
- Bus ties are represented through the named tie breaker nodes rather than direct bus-to-bus shortcuts.
- Crossings without visible junction dots were treated as crossings only and were not added as edges.

## Uncertain or deliberately excluded cases

- `PANEL-MCR`/`PANEL-ANN` and `INV-120B` are raw/crop visual additions because they are visibly named but absent from the current component CSV.
- `FS-B03` is visibly labeled beside `TB-B03` in the Train B 480 V crop and is included as a raw-only instrument node.
- Cable identifiers such as `C-48A-03-P` and section titles such as `125 VDC / UPS TRAIN B` were not promoted to nodes because they label wires/areas rather than standalone electrical nodes.
- The `MASTER TERMINAL BLOCKS` area label was not promoted to a single node because the current crops do not show a unique named electrical endpoint for that aggregate strip.
- Some long dashed panel/control corridors are marked low confidence where they land in multi-line panel routing; these are retained for high recall and documented in the edge evidence.

## Validation summary

- Nodes: 178
- Edges: 193
- Symmetric matrix: True
- Zero diagonal: True
- Duplicate edges recorded during build: 0
- Invalid edge endpoints: 0
