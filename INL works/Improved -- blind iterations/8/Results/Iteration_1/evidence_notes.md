# Evidence Notes

Inspected input resources:
- `raw -- synthetic_npp_schematic_improved_local_refined_v3.png`
- `component_visual_ocr_labels.csv`
- `detected_components_and_logical_detection_plus_ocr_overlay.png`
- `wires_mask.png`
- `wires_mask_overlay.png`
- `wire_nodes.csv`
- `wire_nodes_overlay.png`

Inspection crops created under `Codes and artifacts`:
- `crop_top_left_345_4160.png`
- `crop_top_center_gen_tie.png`
- `crop_top_right_345_4160.png`
- `crop_mid_left_4160_480.png`
- `crop_mid_center_480_dc.png`
- `crop_mid_right_4160_480.png`
- `crop_center_edgc_4160_480tie.png`
- `crop_center_480_tie_detail.png`
- `crop_left_480_load_bus.png`
- `crop_right_480_load_bus.png`
- `crop_lower_left_loads.png`
- `crop_lower_center_dc_ac.png`
- `crop_lower_right_loads.png`

Main extraction observations:
- Top left source path: `GRID-345-01 -> SUT-2A -> CB-402A -> BUS-4160-N2A`.
- Top right source path: `GRID-345-02 -> SUT-2B -> CB-402B -> BUS-4160-N2B`.
- Generator/UAT source run: `GEN-U2`, `UAT-2A`, and `UAT-2B` are tied to the visibly labeled `2E-100` line.
- 4160 tie: `CB-TIE-4160` bridges `BUS-4160-N2A` and `BUS-4160-N2B`.
- Train A safety bus: `BUS-4160-S2A` connects to `BUS-4160-N2A`, `CB-EDG-A/EDG-2A`, `CB-EDG-C/EDG-2C`, `TR-480-2A`, and `TR-480-N2A`.
- Train B safety bus: `BUS-4160-S2B` connects to `BUS-4160-N2B`, `CB-EDG-B/EDG-2B`, `CB-EDG-C/EDG-2C`, `TR-480-2B`, and `TR-480-N2B`.
- 480 V buses: `BUS-480-E2A`, `BUS-480-N2A`, `BUS-480-N2B`, and `BUS-480-E2B` are explicit named bus nodes. The DS-480 feeder tie is labeled normally open and is treated as plausible rather than as a bus merge.
- OCR missed visible MCCs: `MCC-2A1`, `MCC-2A2`, `MCC-2B1`, `MCC-2B2`, `MCC-2C`, and `MCC-2D`.
- Train A load feeders: `MCC-2A1` feeds CB-51A..CB-54A to pumps; `MCC-2A2` feeds CB-55A..CB-58A to fan/MOV/pump loads; `PN-480-A` feeds the charger/valve/fan branch area.
- Train B load feeders mirror Train A with `MCC-2B1`, `MCC-2B2`, and `PN-480-B`.
- DC/UPS/control: `BUS-125DC-A/B` and `BUS-120AC-A/B` are explicit bus nodes with charger, battery, inverter, fuse, and panel connections.
