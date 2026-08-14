# Uncertain And Rejected Notes

Scope used: only files inside `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires + junctions + OCR` were inspected. I used the raw schematic image, the allowed overlays, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, and the provided crop images. I did not use Ground Truth, GT-derived feedback, external OCR, or files outside the allowed document 12 folder.

## Included But Uncertain

- `DS-F023`: the raw right MCC-1B crop visibly shows the disconnect under `CB-F023`; the small label reads like `DS-F23`, but the adjacent feeder numbering pattern supports normalized `DS-F023`. Edges through `DS-F023` are marked medium confidence.
- `CB-M2A -> MCC-2A` and `CB-M2B -> MCC-2B`: the solid feeder routing descends from the bus-feeder breaker regions to the lower MCC buses, but the long route crosses crop boundaries. Both are included as medium confidence.
- `MCC-2A -> CB-DC-1A` and `MCC-2B -> CB-DC-1B`: the solid routes visually feed the battery charger breaker areas from the lower MCC feeder regions. Included as medium confidence because the vertical run is long.
- `BUS-120VAC-ESF -> RPS-A-CONTROL-NET` and `BUS-120VAC-ESF -> RPS-B-CONTROL-NET`: dashed control routing sits adjacent to the ESF instrument bus and lower RPS logic. Included low confidence because exact terminal landing is abstracted.
- `ATS-INV -> RPS-A-CONTROL-NET` and `ATS-INV -> RPS-B-CONTROL-NET`: dashed static transfer control/status routes are visible but terminal endpoints are not explicit. Included low confidence.
- `TRAIN-A-INTERLOCK-NET` and `TRAIN-B-INTERLOCK-NET`: the upper dash-dot routes are visibly bundled around the 4 kV and MCC feeder breakers, but terminal-by-terminal interlock contacts are not drawn. I represented these as logical interlock nets.
- `RPS-A-INTERLOCK-NET -> TRAIN-A-INTERLOCK-NET` and `RPS-B-INTERLOCK-NET -> TRAIN-B-INTERLOCK-NET`: vertical dash-dot routing suggests upper/lower interlock continuity. Included low confidence.
- `PNL-ESFAS-A/B` interlock edges are low confidence because dash-dot routing reaches the ESFAS area but exact terminal connection is not shown.
- `TB-ANN-1 -> SEQ-REC-1`: the note and dotted annunciation route imply annunciation to the sequence recorder, but the exact line is bundled. Included medium confidence.

## Rejected Or Not Expanded

- Crossings without a dot were not treated as electrical connections, following the schematic note.
- Off-border dashed or dotted continuations with no visible named endpoint were not converted into extra nodes.
- The note "MCC feeders shown single-line; control contacts internal to starters" was not expanded into individual starter-control edges. The feeder chains were captured as power edges only.
- The title-block text naming a connectivity matrix was not used as a data source.
- The equipment-ground symbols are reference grounds only. They were included only as `ground` edges from `PNL-RPS-A` to `GND-1` and from `PNL-RPS-B` to `GND-2`.
