# Round 2 Jennifer Final Notes

## Scope

Final precision/saturation review used only doc 13 Input resources, doc 13 generated crops/artifacts, and Diego Round 2 files in the doc 13 Results folder. I did not use ground truth, evaluator files, metrics, or prior answers as authority. The raw schematic remains the authority; overlays and crops were used only for visual navigation.

## Final decision

Accepted Diego Round 2 as final. I found no visually justified last changes. The graph is saturated under the precision policy: physical inventory components are retained, visually supported named non-inventory component `SWYD-230` is retained, major named buses are retained, accepted edges are direct visible solid-line power/ground or named bus tap relationships, and ambiguous control/off-sheet/cross-routing relationships remain uncertain rather than promoted.

## Focus checks

No isolated off-sheet annotation nodes remain. The visible continuation annotations `CONTINUATION TO 125 VDC SYSTEM SHT-DC-2` and `TO ANNUNCIATOR / PLANT PROCESS COMPUTER` are not kept as accepted nodes because no accepted in-sheet direct endpoint edge uses them.

All 178 physical components from `component_labels_list.csv` are retained. `SWYD-230` is retained from the raw top-left source label. `BUS-4A` through `BUS-4D`, `DC-BUS-A` through `DC-BUS-D`, and the 480 V/MCC bus sections remain retained.

`LOCAL-IO-A` through `LOCAL-IO-D` remain retained only as external named terminal endpoints. The raw crops show `LOCAL I/O` text at terminal/tap symbols on the right end of each `LC-480*` bus, not as broad inferred control networks.

Relay/control relationships remain uncertain. Relay symbols are retained as physical components, but dashed relay-to-breaker/control-trip links are not accepted as direct physical power edges.

The battery/charger/DC/inverter/UPS chain remains corrected and accepted as `BAT-125* -> CHG-125* -> DC-BUS-* -> INV-* -> UPS-*`. I did not restore direct `BAT-125* -> DC-BUS-*` edges or LC-to-charger AC-input edges because those are not cleanly visible as direct conductor endpoint relationships.

## Final counts and validation

- `round_02_jennifer_nodes.csv`: 191 rows, columns `node,kind,type,evidence`.
- `round_02_jennifer_edges.csv`: 170 rows, columns `source,target,evidence`.
- `round_02_jennifer_uncertain.csv`: 33 rows, columns `source,target,evidence,uncertainty_reason`.
- Inventory physical components retained: 178 of 178.
- Duplicate node labels: 0.
- Duplicate accepted edges: 0.
- Duplicate uncertain rows: 0.
- Accepted-edge endpoint coverage against final nodes: pass.
- Uncertain-edge endpoint coverage against final nodes: pass.
- Off-sheet/auto-start/ESFAS/unit-generator annotation nodes or rows: none retained.
