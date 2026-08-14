# Round 01 Jennifer Notes - Improved doc 6 / Iteration_1

## Scope

Blind precision review used only the listed input resources, fresh input-derived inspection crops, and Diego round 01 files. The raw schematic was treated as authoritative. GT, scoring/evaluation files, previous result archives, and unrelated files were not used.

## Main Label Fix

- Corrected Diego's `BUS-6KV-N` to `BUS-4KV-N`.
- Evidence: `inspection_crops_improved/11_bus_6kv_label_focus_raw.png` and `03_safety_bus_full_raw.png` show the central lower bus label as `BUS-4KV-N`.
- Updated affected edges: `DS-6KV-A` to `BUS-4KV-N`, `DS-6KV-B` to `BUS-4KV-N`, and `BUS-4KV-N` to `TR-480N`.

## Precision Changes From Diego

- Retained the solid generator, switchyard, safety bus, 480 V load center, MCC/load, DC/UPS, heater/load, and named ground-bond paths where a drawn conductor terminates at named components or explicit buses.
- Retained clean direct dashed control/sensing pairs in the control bay: panels to their corresponding relays, UV sensors to instrument panels, PT/CT sensing leads to instrument panels, DG breaker/ATS interlocks to DG relays, SI relay routes to MCC-HPI/MOV endpoints, and load relay routes to fan endpoints.
- Replaced Diego's `RELAY-SI-A` to `PUMP-HPI-A` and `RELAY-SI-B` to `PUMP-HPI-B` inferences with direct dashed endpoint edges `RELAY-SI-A` to `MCC-HPI-A` and `RELAY-SI-B` to `MCC-HPI-B`.
- Removed relay/control and DC/UPS edges that depended on visual crossings, nearby parallel lanes, or semantic association rather than an identifiable terminal.

## Rejected Or Marked Uncertain From Diego

- `CT-EDG-A` - `DG-201A`: CT symbol is on a dashed sensing/instrument line; no drawn CT terminal to DG-201A.
- `CT-EDG-A` - `CB-DG-A`: no direct CT terminal to CB-DG-A; nearby association only.
- `CT-EDG-B` - `DG-201B`: CT symbol is on a dashed sensing/instrument line; no drawn CT terminal to DG-201B.
- `CT-EDG-B` - `CB-DG-B`: no direct CT terminal to CB-DG-B; nearby association only.
- `REC-A` - `BAT-125A`: battery branch routes to PNL-DC-A; no direct REC-A to BAT-125A line visible.
- `REC-B` - `BAT-125B`: battery branch routes to PNL-DC-B; no direct REC-B to BAT-125B line visible.
- `PNL-DC-A` - `GND-A`: dotted ground bond lands at battery/rectifier area, not PNL-DC-A.
- `PNL-DC-B` - `GND-B`: dotted ground bond lands at battery/rectifier area, not PNL-DC-B.
- `UPS-A` - `JBX-ESF-A`: long dash-dot UPS/control bundle lacks an unambiguous named JBX-A termination.
- `PNL-DC-A` - `JBX-ESF-A`: long dash-dot DC panel bundle lacks an unambiguous named JBX-A termination.
- `UPS-B` - `JBX-ESF-B`: long dash-dot UPS/control bundle lacks an unambiguous named JBX-B termination.
- `PNL-DC-B` - `JBX-ESF-B`: long dash-dot DC panel bundle lacks an unambiguous named JBX-B termination.
- `RELAY-UV-A` - `RELAY-UV-B`: cross-train relay loop has crossings/returns without clear dot-confirmed direct relay-to-relay connectivity.
- `RELAY-SI-A` - `RELAY-SI-B`: cross-train relay loop has crossings/returns without clear dot-confirmed direct relay-to-relay connectivity.
- `RELAY-LOAD-A` - `RELAY-LOAD-B`: cross-train relay loop has crossings/returns without clear dot-confirmed direct relay-to-relay connectivity.
- `RELAY-DG-A` - `RELAY-DG-B`: cross-train relay loop has crossings/returns without clear dot-confirmed direct relay-to-relay connectivity.
- `DG-201A` - `RELAY-DG-A`: dashed DG relay route does not visibly terminate on DG-201A; keep CB/ATS terminations only.
- `DG-201B` - `RELAY-DG-B`: dashed DG relay route does not visibly terminate on DG-201B; keep CB/ATS terminations only.
- `CP-ESFAS-A` - `JBX-ESF-A`: shared control-bay routing is ambiguous; no direct named endpoint edge retained.
- `CP-ESFAS-B` - `JBX-ESF-B`: shared control-bay routing is ambiguous; no direct named endpoint edge retained.
- `PLC-RPS-A` - `JBX-ESF-A`: shared control-bay routing is ambiguous; no direct named endpoint edge retained.
- `PLC-RPS-B` - `JBX-ESF-B`: shared control-bay routing is ambiguous; no direct named endpoint edge retained.
- `RELAY-SI-A` - `PUMP-HPI-A`: SI dashed line terminates at MCC-HPI-A/MOV-SI-201A, not directly at PUMP-HPI-A.
- `RELAY-SI-B` - `PUMP-HPI-B`: SI dashed line terminates at MCC-HPI-B/MOV-SI-201B, not directly at PUMP-HPI-B.
- `RELAY-LOAD-A` - `LC-480A`: load relay route not visibly terminated on LC-480A; LC line is UV sensing branch.
- `RELAY-LOAD-B` - `LC-480B`: load relay route not visibly terminated on LC-480B; LC line is UV sensing branch.
- `RELAY-LOAD-A` - `MCC-VENT-A`: no clear dashed terminal on MCC-VENT-A; keep direct FAN-CR-A control termination.
- `RELAY-LOAD-B` - `MCC-VENT-B`: no clear dashed terminal on MCC-VENT-B; keep direct FAN-CR-B control termination.
- `UPS-A` - `PNL-INST-A`: long UPS/control power route is not unambiguously terminated at PNL-INST-A.
- `UPS-A` - `CP-ESFAS-A`: long UPS/control power route is not unambiguously terminated at CP-ESFAS-A.
- `UPS-A` - `PLC-RPS-A`: long UPS/control power route is not unambiguously terminated at PLC-RPS-A.
- `UPS-B` - `PNL-INST-B`: long UPS/control power route is not unambiguously terminated at PNL-INST-B.
- `UPS-B` - `CP-ESFAS-B`: long UPS/control power route is not unambiguously terminated at CP-ESFAS-B.
- `UPS-B` - `PLC-RPS-B`: long UPS/control power route is not unambiguously terminated at PLC-RPS-B.

## Added Precision Edges

- `RELAY-SI-A` - `MCC-HPI-A`: replaces Diego pump-level inference with the drawn MCC-HPI-A dashed side-port termination.
- `RELAY-SI-B` - `MCC-HPI-B`: replaces Diego pump-level inference with the drawn MCC-HPI-B dashed side-port termination.

## Output Summary

- Node count: 105 named components/buses.
- Edge count: 121 reviewed edges.
- Matrix: symmetric binary adjacency with zero diagonal.
- Ambiguous dashed crossings were not expanded into all-to-all connectivity; the drawing note says no dot means visual crossing only.
