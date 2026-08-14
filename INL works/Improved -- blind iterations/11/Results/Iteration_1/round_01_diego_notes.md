# Round 01 Diego Notes

## Node Policy
I included all 99 visually/OCR-listed physical component tags from `component_visual_ocr_labels.csv`, plus one visually recovered breaker node, `CB-MCC-A1`, visible on the A-train MCC branch but missed by the table. I also added only visually labeled matrix-level non-component nodes: named buses, named grounds, safety-train/reference areas, 125 VDC division labels, and the lower control/RPS interlock zone. I did not include anonymous wire-node points from `wire_nodes.csv`; those are used only as visual support for dots, endpoints, and crossings.

## Buses And Grounds Added
Added buses: `BUS-13-8A`, `BUS-13-8B`, `BUS-4160-A/B/C/D`, `BUS-480-A1/A2/B1/B2/C1/C2/D1/D2`, and `BUS-DC-125A/B`. Added grounds: `GND-A/B/C/D`. Added reference areas: `SAFETY-TRAIN-A/B/C/D`, `125-VDC-DIVISION-A/B`, and `CTRL-RPS-INTERLOCKS`.

## Major Connectivity Groups
The top 13.8 kV section has `GEN-01 -> TR-UAT-1 -> CB-UAT-1 -> BUS-13-8A`, `TR-SUT-1 -> CB-SUT-1 -> BUS-13-8A`, tie `BUS-13-8A -> CB-13-TIE -> BUS-13-8B`, `GEN-02 -> TR-UAT-2 -> CB-UAT-2 -> BUS-13-8B`, and `TR-SUT-2 -> CB-SUT-2 -> BUS-13-8B`.

Each safety train has a normal incoming breaker from the proper 13.8 kV bus to `BUS-4160-*`, a diesel generator path through `CB-DG-*`, two transformer strings from `BUS-4160-*` to `BUS-480-*1/*2`, MCC branches to local loads, and a rectifier/I-C/ground branch from the `*2` 480 V bus.

The bottom DC section has clear battery-to-DC-bus-to-inverter-to-RPS paths for `BUS-DC-125A` and `BUS-DC-125B`. Candidate longer routes pair A/C with Division A and B/D with Division B, especially the rectifier/DC and ATS input wiring, but these were placed in the plausible file where crossings and crop boundaries make endpoints less certain.

## Ambiguity Hotspots
The long dashed `SSPS-*`, relay, RPS, and ATS interlock routes are visually plausible but cross many power feeders; these are mostly in the plausible file. The lower ATS inputs labeled `ATS-A1`, `ATS-C1`, `ATS-B1`, and `ATS-D1` appear to route from MCC load clusters into `ATS-480-A/B`, but the endpoint trace is not as clean as the local MCC-to-load branches. The DC rectifier-to-division-bus paths and ground-to-DC-bus references are also candidates rather than high-confidence direct edges because the routes share vertical panel/ground conductors and long lower runs.
