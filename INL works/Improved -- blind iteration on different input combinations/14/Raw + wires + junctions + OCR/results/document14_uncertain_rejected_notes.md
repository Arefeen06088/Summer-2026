# Document 14 Uncertain And Rejected Notes

## Scope Used
Only the document 14 resource folder was used: raw drawing, component CSV, wire node CSV, overlays, wire mask, and evidence crops. No ground truth, evaluator output, metric feedback, previous-document files, or off-the-shelf OCR were used.

## Included Low-Confidence Classes
- Relay-to-disconnect edges are included at low confidence. The dashed relay/contact graphics are visibly adjacent to each breaker/disconnect stack, but the explicit control terminal is not drawn as a solid junction.
- `PANEL-RPS-A` to the A-side charger feeder is included at low confidence because the solid vertical charger feeder passes through the panel rectangle. This could be a real panel feed or a drafting overlap; the direct `BUS-480A` to `CHG-125A` feed is the higher-confidence power interpretation.
- The `MASTER_TERMINAL_BLOCKS` aggregate node and its `BUS-UPS-A` edge are low confidence. The strip and label are visible below `BUS-UPS-A`, but individual terminal cell conductors are not resolved.

## Dashed Control/Interlock Treatment
- Dashed verticals from feeder columns and dashed horizontals over the lower panels were not expanded into all possible pairwise panel-to-feeder edges. Instead, two logical nodes, `CTRL-TRAIN-A-DASHED` and `CTRL-TRAIN-B-DASHED`, capture the shared dashed control/interlock bundles.
- `PANEL-MCR`, `PANEL-ANN`, and `CB-DG-TIE` are connected by the central dashed vertical because the raw drawing shows a continuous dashed line through those objects.
- Tie breakers `CB-TIE-4KV` and `CB-480-TIE` were connected only by their solid bus tie conductors. I did not add panel-control edges for them because no explicit dashed control line to those tie breakers was visible in the inspected crops.

## Rejected/Not Expanded
- Crossing wires without junction dots were not connected. This affects several dashed/solid crossings in the lower control bundles and feeder drops.
- The three small circles inside each panel were not split into individual terminal nodes; they are treated as part of the panel symbol.
- Individual cells in the bottom master terminal block strip were not enumerated. The label is readable, but per-cell labels/conductors are not sufficiently explicit in the raw drawing.
- Dashed train-control bundles were not treated as power continuity. They are represented only with `dashed_control` edges.
- Title block metadata was not used as scoring feedback; it was treated only as in-drawing schematic metadata.
