# Round 2 Jennifer Final Notes - Doc 12

## Scope

- Final precision/saturation review used only doc 12 `Input resources`, doc 12 `Codes and artifacts` including inspection crops and Jennifer zoom crops, and Round 1/Round 2 files in `Results\Iteration_1`.
- I did not use ground truth, evaluator outputs, scores, validation metrics, prior answer keys, or anything outside the allowed doc 12 folders.
- Raw legend rules were followed: solid = power, dashed = control, dotted = signal, dash-dot = interlock; black dots mark taps/connections; crossings without dots are not connected; grounds are equipment ground reference only.

## Final Counts

- Final node count: 160.
- Final accepted edge count: 144.
- Final uncertain/not accepted candidate count: 54.
- Saturation reached: yes. After the final visual pass, no additional direct named-endpoint edges were supported beyond the two restored 120 VAC RPS panel feeds.

## Final Node Set

- Kept the 160-node policy from Jennifer Round 1 and Diego Round 2.
- Retained raw-supported bus names: `BUS-4KV-A`, `BUS-4KV-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-A`, `DC-BUS-B`, and `BUS-120VAC-ESF`.
- Kept `MCC-1A`, `MCC-1B`, `MCC-2A`, and `MCC-2B` as physical motor-control-center nodes only; no bus aliases were added.
- Kept `GND-1` and `GND-2` as equipment ground reference nodes only.
- Retained the visually supported feeder label corrections, including the corrected `MS-Fxxx`, `FU-Fxxx`, and `DS-Fxxx` labels in the repeated MCC branches. No anonymous intermediate wire nodes were added.

## Restored Edge Decision

- Accepted `BUS-120VAC-ESF --ac_control_power-- PNL-RPS-A`.
- Accepted `BUS-120VAC-ESF --ac_control_power-- PNL-RPS-B`.
- Reason: crops `13_rps_relay_tb_panels_raw.png` and `19_full_bottom_controls_raw.png`, plus Jennifer zoom crops `round02_jennifer_rps_a_bus_tap_zoom.png` and `round02_jennifer_rps_b_bus_tap_zoom.png`, show black-dot taps on the solid `BUS-120VAC-ESF` bus. Each tap drops as a short solid vertical conductor directly into the top edge of the named RPS panel. These are direct named endpoint edges, not inferred TB/trunk overconnections.

## Candidates Kept Uncertain

- PT bus taps remain uncertain/not accepted: `BUS-4KV-A -- PT-4160A` and `BUS-4KV-B -- PT-4160B` lack the clear black bus-tap dot used for accepted bus connections.
- PT-to-relay, relay-to-TB, relay-to-relay, TB-to-panel, RPS-to-ESFAS, ANN/TB-ANN/SEQ-REC, ATS-to-TB, and DC-bus-to-TB/panel candidates remain uncertain/not accepted.
- `BUS-120VAC-ESF` feeds to TBs, ESFAS panels, or `SEQ-REC-1` remain uncertain/not accepted; their visible routes use trunks, compact terminal clusters, or non-solid/dotted/dashed paths without direct named endpoint evidence comparable to the two accepted RPS panel taps.
