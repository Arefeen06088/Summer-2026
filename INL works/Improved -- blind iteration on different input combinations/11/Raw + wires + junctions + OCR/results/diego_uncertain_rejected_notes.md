# Diego uncertain / rejected notes for document 11

Allowed sources used only from this folder: raw schematic image, component_labels_banners_overlay.png, wire_nodes_overlay.png, wires_mask_overlay.png, component_visual_ocr_labels.csv, and the prepared crop images under codes. No Ground Truth, evaluator feedback, or off-the-shelf OCR was used.

## Included but uncertain / lower-confidence edges

- BUS-480-X1 to BUS-480-X2 edges are included as power_bus_connection with medium confidence. The solid 480 V horizontal line visually connects the two bus sections, but the nearby TIE-X12 text sits on a dashed interlock/control line, so the semantic role of the tie label is not purely power.
- ATS input edges from MCC-X1 through ATS-X1 into ATS-480-A/B are included with medium confidence. The vertical MCC load feeder continues into the lower ATS area, but the bottom region is crowded and partly outside some division crops.
- L-XP2 and L-XF1 are split from the crowded visual text bundle L-XP2-L-XF1; the individual feeder-to-load geometry is clear, but the text separation is only medium confidence.
- Dashed relay and SSPS paths are included as control_interlock edges, not power edges. They are visually/geometrically connected by dashed lines, but their logical direction/function is not derivable from geometry alone.
- PANEL-IC-X to SSPS-X and ATS-480-A/B to CONTROL-POWER-RPS-INTERLOCKS are retained as low-confidence interlock edges because the dashed interlock region appears to include them, but exact terminal landing is indirect.
- Diesel generator component labels in the CSV are retained as DG-2A ... DG-2D; possible aliases/corrections DG-1A ... DG-1D are noted because the text directly under each DG symbol appears to read DG 1X while the adjacent vertical feeder reads DG-2X.

## Rejected / not promoted to graph nodes

- Title block, revision table, legend symbols, note text, grid letters/numbers, and drawing-number text were ignored.
- Generic ratings and descriptors such as SIZE 2, SIZE 3, 4.16 KV, 480V, 125VDC, and 600V/3PH LOADS TYP. were used as evidence only, not graph nodes.
- Small terminal-block squares labeled TB were not promoted to nodes because they are shown as generic normal incoming feeder detail without distinct component tags.
- Wire topology IDs from wire_nodes.csv (WN-xxxx) were used only as visual/geometric aids and were not exported as final graph node names.
- Junction dots without printed names were not individually exported unless they corresponded to a named bus, feeder, ground, DC rail, ATS lead, or interlock label.
