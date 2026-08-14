# Round 01 Diego High-Recall Connectivity Notes

Scope and evidence rules: I used only doc 23 raw/input resources and doc 23 generated input-derived aids in the specified folders. I did not open or use ground truth, evaluator output, metrics, or feedback-derived artifacts. The raw schematic PNG was treated as primary evidence; component labels, wire overlays, and crops were aids.

## Node List Rationale

- Base physical component nodes: 184 from `component_labels_list.csv`; the inventory text says these are raw visual/OCR manual labels. Component type counts: annunciator=2, automatic_transfer_switch=2, battery=3, battery_charger=2, breaker=26, diesel_generator=2, disconnect_switch=8, fan_motor=6, fuse=2, grid_source=2, ground=10, heater_load=6, instrument=8, inverter=2, junction_box=8, meter=4, motor=6, motor_control_center=18, panel=11, pid_instrument=2, pump_motor=6, rectifier=2, relay=21, sequence_recorder=2, sync_device=1, transformer=8, ups=2, valve=12.
- Added one raw-visible physical component not present in the 184-node inventory: `DC-DC-1`, seen as a small DC/DC converter near the printed `BUS-24DC-C` / `BAT-24C` lower control area.
- Added printed logical bus nodes verified on raw/crop imagery: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-ESF-A`, `BUS-4160-ESF-B`, `BUS-480-1A`, `BUS-480-1C`, `BUS-480-1B`, `BUS-480-2A`, `BUS-480-2C`, `BUS-480-2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`, `BUS-24DC-C`.
- Excluded WN-* IDs, unlabeled junction dots, title/section text, voltage-only descriptions, and orthogonal crossings without visible connection dots.
- Buses are used as mediator nodes: components tapping the same printed bus are connected to the bus, not expanded into pairwise cliques.

## Edge Evidence By Area

### Top 161kV/UAT/4160 buses
Evidence pattern: raw top crops show grid source through DS/CB/UAT/low-side CB to printed 4160 bus; meters/PTs/relays/grounds terminate on bus dots; tie breaker sits between the A/B bus spans with SYNC-41 above it.
- `GRID-161A` -- `DS-101`
- `DS-101` -- `CB-101`
- `CB-101` -- `TR-UAT-1A`
- `TR-UAT-1A` -- `CB-102`
- `CB-102` -- `BUS-4160-A`
- `RELAY-87A` -- `BUS-4160-A`
- `RELAY-27A` -- `BUS-4160-A`
- `METER-A` -- `BUS-4160-A`
- `PT-41A` -- `BUS-4160-A`
- `GND-41A` -- `BUS-4160-A`
- `BUS-4160-A` -- `CB-TIE-41`
- `CB-TIE-41` -- `BUS-4160-B`
- `SYNC-41` -- `CB-TIE-41`
- `GRID-161B` -- `DS-102`
- `DS-102` -- `CB-103`
- `CB-103` -- `TR-UAT-1B`
- `TR-UAT-1B` -- `CB-104`
- `CB-104` -- `BUS-4160-B`
- `RELAY-87B` -- `BUS-4160-B`
- `RELAY-27B` -- `BUS-4160-B`
- `METER-B` -- `BUS-4160-B`
- `PT-41B` -- `BUS-4160-B`
- `GND-41B` -- `BUS-4160-B`

### 4160 ESF/diesel/ATS
Evidence pattern: raw full/crop views show `CB-ESF-*` linking 4160 bus to printed ESF bus; diesel generator path is `DG -> CB-DG -> ATS -> BUS-4160-ESF-*`.
- `BUS-4160-A` -- `CB-ESF-A`
- `CB-ESF-A` -- `BUS-4160-ESF-A`
- `DG-1A` -- `CB-DG1A`
- `CB-DG1A` -- `ATS-1A`
- `ATS-1A` -- `BUS-4160-ESF-A`
- `BUS-4160-B` -- `CB-ESF-B`
- `CB-ESF-B` -- `BUS-4160-ESF-B`
- `DG-1B` -- `CB-DG1B`
- `CB-DG1B` -- `ATS-1B`
- `ATS-1B` -- `BUS-4160-ESF-B`

### 480 V load center 1A
Evidence pattern: raw crop shows upstream feeder entering `CB-*FDR`, then vertical chain `CB-*FDR -> DS-*ISO -> TR-* -> CB-*MAIN -> BUS-480-*`; bus dots/taps feed MCCs, panel/instrument/ground. MCC branch wires feed loads; dashed lower relay/JB control edges are retained as high-recall candidates.
- `BUS-4160-A` -- `CB-1A-FDR`
- `CB-1A-FDR` -- `DS-1A-ISO`
- `DS-1A-ISO` -- `TR-1A`
- `TR-1A` -- `CB-1A-MAIN`
- `CB-1A-MAIN` -- `BUS-480-1A`
- `BUS-480-1A` -- `MCC-1A-1`
- `BUS-480-1A` -- `MCC-1A-2`
- `BUS-480-1A` -- `MCC-1A-3`
- `BUS-480-1A` -- `PNL-1A`
- `BUS-480-1A` -- `INST-1A`
- `BUS-480-1A` -- `GND-1A`
- `MCC-1A-1` -- `PUMP-P101`
- `MCC-1A-1` -- `MOTOR-M102`
- `MCC-1A-2` -- `VALVE-MOV103`
- `MCC-1A-2` -- `FAN-F104`
- `MCC-1A-3` -- `HTR-H105`
- `MCC-1A-3` -- `VALVE-XV106`
- `VALVE-XV106` -- `JB-1A-1`
- `PNL-1A` -- `JB-1A-1` (dashed panel/JB control run)
- `PNL-1A` -- `RELAY-K11` (dashed panel-to-relay control run)
- `RELAY-K11` -- `RELAY-K12` (relay pair joined on lower control line)
- `RELAY-K12` -- `JB-1A-1` (dashed relay/JB control return)

### 480 V load center 1C
Evidence pattern: raw crop shows upstream feeder entering `CB-*FDR`, then vertical chain `CB-*FDR -> DS-*ISO -> TR-* -> CB-*MAIN -> BUS-480-*`; bus dots/taps feed MCCs, panel/instrument/ground. MCC branch wires feed loads; dashed lower relay/JB control edges are retained as high-recall candidates.
- `BUS-4160-A` -- `CB-1C-FDR`
- `CB-1C-FDR` -- `DS-1C-ISO`
- `DS-1C-ISO` -- `TR-1C`
- `TR-1C` -- `CB-1C-MAIN`
- `CB-1C-MAIN` -- `BUS-480-1C`
- `BUS-480-1C` -- `MCC-1C-1`
- `BUS-480-1C` -- `MCC-1C-2`
- `BUS-480-1C` -- `MCC-1C-3`
- `BUS-480-1C` -- `PNL-1C`
- `BUS-480-1C` -- `INST-1C`
- `BUS-480-1C` -- `GND-1C`
- `MCC-1C-1` -- `PUMP-P131`
- `MCC-1C-1` -- `MOTOR-M132`
- `MCC-1C-2` -- `VALVE-MOV133`
- `MCC-1C-2` -- `FAN-F134`
- `MCC-1C-3` -- `HTR-H135`
- `MCC-1C-3` -- `VALVE-XV136`
- `VALVE-XV136` -- `JB-1C-1`
- `PNL-1C` -- `JB-1C-1` (dashed panel/JB control run)
- `PNL-1C` -- `RELAY-K21` (dashed panel-to-relay control run)
- `RELAY-K21` -- `RELAY-K22` (relay pair joined on lower control line)
- `RELAY-K22` -- `JB-1C-1` (dashed relay/JB control return)

### 480 V load center 1B
Evidence pattern: raw crop shows upstream feeder entering `CB-*FDR`, then vertical chain `CB-*FDR -> DS-*ISO -> TR-* -> CB-*MAIN -> BUS-480-*`; bus dots/taps feed MCCs, panel/instrument/ground. MCC branch wires feed loads; dashed lower relay/JB control edges are retained as high-recall candidates.
- `BUS-4160-B` -- `CB-1B-FDR`
- `CB-1B-FDR` -- `DS-1B-ISO`
- `DS-1B-ISO` -- `TR-1B`
- `TR-1B` -- `CB-1B-MAIN`
- `CB-1B-MAIN` -- `BUS-480-1B`
- `BUS-480-1B` -- `MCC-1B-1`
- `BUS-480-1B` -- `MCC-1B-2`
- `BUS-480-1B` -- `MCC-1B-3`
- `BUS-480-1B` -- `PNL-1B`
- `BUS-480-1B` -- `INST-1B`
- `BUS-480-1B` -- `GND-1B`
- `MCC-1B-1` -- `PUMP-P161`
- `MCC-1B-1` -- `MOTOR-M162`
- `MCC-1B-2` -- `VALVE-MOV163`
- `MCC-1B-2` -- `FAN-F164`
- `MCC-1B-3` -- `HTR-H165`
- `MCC-1B-3` -- `VALVE-XV166`
- `VALVE-XV166` -- `JB-1B-1`
- `PNL-1B` -- `JB-1B-1` (dashed panel/JB control run)
- `PNL-1B` -- `RELAY-K31` (dashed panel-to-relay control run)
- `RELAY-K31` -- `RELAY-K32` (relay pair joined on lower control line)
- `RELAY-K32` -- `JB-1B-1` (dashed relay/JB control return)

### 480 V load center 2A
Evidence pattern: raw crop shows upstream feeder entering `CB-*FDR`, then vertical chain `CB-*FDR -> DS-*ISO -> TR-* -> CB-*MAIN -> BUS-480-*`; bus dots/taps feed MCCs, panel/instrument/ground. MCC branch wires feed loads; dashed lower relay/JB control edges are retained as high-recall candidates.
- `BUS-4160-ESF-A` -- `CB-2A-FDR`
- `CB-2A-FDR` -- `DS-2A-ISO`
- `DS-2A-ISO` -- `TR-2A`
- `TR-2A` -- `CB-2A-MAIN`
- `CB-2A-MAIN` -- `BUS-480-2A`
- `BUS-480-2A` -- `MCC-2A-1`
- `BUS-480-2A` -- `MCC-2A-2`
- `BUS-480-2A` -- `MCC-2A-3`
- `BUS-480-2A` -- `PNL-2A`
- `BUS-480-2A` -- `INST-2A`
- `BUS-480-2A` -- `GND-2A`
- `MCC-2A-1` -- `PUMP-P201`
- `MCC-2A-1` -- `MOTOR-M202`
- `MCC-2A-2` -- `VALVE-MOV203`
- `MCC-2A-2` -- `FAN-F204`
- `MCC-2A-3` -- `HTR-H205`
- `MCC-2A-3` -- `VALVE-XV206`
- `VALVE-XV206` -- `JB-2A-1`
- `PNL-2A` -- `JB-2A-1` (dashed panel/JB control run)
- `PNL-2A` -- `RELAY-K41` (dashed panel-to-relay control run)
- `RELAY-K41` -- `RELAY-K42` (relay pair joined on lower control line)
- `RELAY-K42` -- `JB-2A-1` (dashed relay/JB control return)

### 480 V load center 2C
Evidence pattern: raw crop shows upstream feeder entering `CB-*FDR`, then vertical chain `CB-*FDR -> DS-*ISO -> TR-* -> CB-*MAIN -> BUS-480-*`; bus dots/taps feed MCCs, panel/instrument/ground. MCC branch wires feed loads; dashed lower relay/JB control edges are retained as high-recall candidates.
- `BUS-4160-ESF-A` -- `CB-2C-FDR`
- `CB-2C-FDR` -- `DS-2C-ISO`
- `DS-2C-ISO` -- `TR-2C`
- `TR-2C` -- `CB-2C-MAIN`
- `CB-2C-MAIN` -- `BUS-480-2C`
- `BUS-480-2C` -- `MCC-2C-1`
- `BUS-480-2C` -- `MCC-2C-2`
- `BUS-480-2C` -- `MCC-2C-3`
- `BUS-480-2C` -- `PNL-2C`
- `BUS-480-2C` -- `INST-2C`
- `BUS-480-2C` -- `GND-2C`
- `MCC-2C-1` -- `PUMP-P231`
- `MCC-2C-1` -- `MOTOR-M232`
- `MCC-2C-2` -- `VALVE-MOV233`
- `MCC-2C-2` -- `FAN-F234`
- `MCC-2C-3` -- `HTR-H235`
- `MCC-2C-3` -- `VALVE-XV236`
- `VALVE-XV236` -- `JB-2C-1`
- `PNL-2C` -- `JB-2C-1` (dashed panel/JB control run)
- `PNL-2C` -- `RELAY-K51` (dashed panel-to-relay control run)
- `RELAY-K51` -- `RELAY-K52` (relay pair joined on lower control line)
- `RELAY-K52` -- `JB-2C-1` (dashed relay/JB control return)

### 480 V load center 2B
Evidence pattern: raw crop shows upstream feeder entering `CB-*FDR`, then vertical chain `CB-*FDR -> DS-*ISO -> TR-* -> CB-*MAIN -> BUS-480-*`; bus dots/taps feed MCCs, panel/instrument/ground. MCC branch wires feed loads; dashed lower relay/JB control edges are retained as high-recall candidates.
- `BUS-4160-ESF-B` -- `CB-2B-FDR`
- `CB-2B-FDR` -- `DS-2B-ISO`
- `DS-2B-ISO` -- `TR-2B`
- `TR-2B` -- `CB-2B-MAIN`
- `CB-2B-MAIN` -- `BUS-480-2B`
- `BUS-480-2B` -- `MCC-2B-1`
- `BUS-480-2B` -- `MCC-2B-2`
- `BUS-480-2B` -- `MCC-2B-3`
- `BUS-480-2B` -- `PNL-2B`
- `BUS-480-2B` -- `INST-2B`
- `BUS-480-2B` -- `GND-2B`
- `MCC-2B-1` -- `PUMP-P261`
- `MCC-2B-1` -- `MOTOR-M262`
- `MCC-2B-2` -- `VALVE-MOV263`
- `MCC-2B-2` -- `FAN-F264`
- `MCC-2B-3` -- `HTR-H265`
- `MCC-2B-3` -- `VALVE-XV266`
- `VALVE-XV266` -- `JB-2B-1`
- `PNL-2B` -- `JB-2B-1` (dashed panel/JB control run)
- `PNL-2B` -- `RELAY-K61` (dashed panel-to-relay control run)
- `RELAY-K61` -- `RELAY-K62` (relay pair joined on lower control line)
- `RELAY-K62` -- `JB-2B-1` (dashed relay/JB control return)

### Lower DC/UPS power
Evidence pattern: lower crops show CB-DC to rectifier to 125 VDC bus; batteries/chargers/meters/grounds tap the 125 VDC bus; inverter/UPS/CB-UPS feeds printed 120 VAC bus; `CB-DCTIE` bridges the A/B 125 VDC buses.
- `BUS-480-2A` -- `CB-DC-A` (upstream feed routed from 2A lower-left boundary to DC breaker)
- `CB-DC-A` -- `RECT-125A`
- `RECT-125A` -- `BUS-125DC-A`
- `BUS-125DC-A` -- `BAT-125A`
- `BUS-125DC-A` -- `CHGR-AUX-A`
- `BUS-125DC-A` -- `METER-DC-A`
- `BUS-125DC-A` -- `GND-DC-A`
- `BUS-125DC-A` -- `INV-1A`
- `INV-1A` -- `UPS-1A`
- `UPS-1A` -- `CB-UPS-A`
- `CB-UPS-A` -- `BUS-120AC-A`
- `BUS-125DC-A` -- `CB-DCTIE`
- `CB-DCTIE` -- `BUS-125DC-B`
- `BUS-480-2B` -- `CB-DC-B` (upstream feed routed from 2B lower-right boundary to DC breaker)
- `CB-DC-B` -- `RECT-125B`
- `RECT-125B` -- `BUS-125DC-B`
- `BUS-125DC-B` -- `BAT-125B`
- `BUS-125DC-B` -- `CHGR-AUX-B`
- `BUS-125DC-B` -- `METER-DC-B`
- `BUS-125DC-B` -- `GND-DC-B`
- `BUS-125DC-B` -- `INV-1B`
- `INV-1B` -- `UPS-1B`
- `UPS-1B` -- `CB-UPS-B`
- `CB-UPS-B` -- `BUS-120AC-B`

### 120 VAC RPS/control A
Evidence pattern: raw lower A/B crops show printed 120 VAC bus with fuse, relay, annunciator, recorder, RPS panel and NIS taps; dashed logic bundles run into the RPS and DCS/JB panels.
- `BUS-120AC-A` -- `FUSE-FU-A`
- `BUS-120AC-A` -- `RELAY-KA1`
- `BUS-120AC-A` -- `RELAY-KA2`
- `BUS-120AC-A` -- `ANN-A`
- `BUS-120AC-A` -- `REC-SER-A`
- `BUS-120AC-A` -- `PNL-RPS-A`
- `BUS-120AC-A` -- `INST-NIS-A`
- `RELAY-KA1` -- `RELAY-KA2` (dashed relay-to-relay control line)
- `RELAY-KA1` -- `PNL-RPS-A` (dashed relay input to RPS panel)
- `RELAY-KA2` -- `PNL-RPS-A` (dashed relay input to RPS panel)
- `ANN-A` -- `PNL-RPS-A` (dashed annunciator bundle into RPS panel)
- `REC-SER-A` -- `PNL-RPS-A` (dashed recorder bundle into RPS panel)
- `INST-NIS-A` -- `PNL-RPS-A` (dashed NIS/RPS association)
- `PNL-RPS-A` -- `PNL-DCS-A` (vertical RPS-to-DCS panel run)
- `PNL-DCS-A` -- `JB-CTRL-A` (dashed DCS-to-control-JB run)

### 120 VAC RPS/control B
Evidence pattern: raw lower A/B crops show printed 120 VAC bus with fuse, relay, annunciator, recorder, RPS panel and NIS taps; dashed logic bundles run into the RPS and DCS/JB panels.
- `BUS-120AC-B` -- `FUSE-FU-B`
- `BUS-120AC-B` -- `RELAY-KB1`
- `BUS-120AC-B` -- `RELAY-KB2`
- `BUS-120AC-B` -- `ANN-B`
- `BUS-120AC-B` -- `REC-SER-B`
- `BUS-120AC-B` -- `PNL-RPS-B`
- `BUS-120AC-B` -- `INST-NIS-B`
- `RELAY-KB1` -- `RELAY-KB2` (dashed relay-to-relay control line)
- `RELAY-KB1` -- `PNL-RPS-B` (dashed relay input to RPS panel)
- `RELAY-KB2` -- `PNL-RPS-B` (dashed relay input to RPS panel)
- `ANN-B` -- `PNL-RPS-B` (dashed annunciator bundle into RPS panel)
- `REC-SER-B` -- `PNL-RPS-B` (dashed recorder bundle into RPS panel)
- `INST-NIS-B` -- `PNL-RPS-B` (dashed NIS/RPS association)
- `PNL-RPS-B` -- `PNL-DCS-B` (vertical RPS-to-DCS panel run)
- `PNL-DCS-B` -- `JB-CTRL-B` (dashed DCS-to-control-JB run)

### 24 VDC/control center
Evidence pattern: raw lower-control crop shows printed `BUS-24DC-C`, `BAT-24C`, `DC-DC-1`, `JB-CTRL-A`, `PNL-RADMON`, and dashed `PNL-RADMON` to `RELAY-KTIE` association.
- `BUS-125DC-A` -- `DC-DC-1` (probable input to raw-visible DC/DC converter from upper DC run)
- `DC-DC-1` -- `BUS-24DC-C` (converter output to printed 24 VDC bus)
- `BUS-24DC-C` -- `BAT-24C`
- `BUS-24DC-C` -- `JB-CTRL-A` (solid lower control bus passes through/at JB-CTRL-A)
- `BUS-24DC-C` -- `PNL-RADMON`
- `PNL-RADMON` -- `RELAY-KTIE` (dashed rad-monitor tie relay run)

## Uncertain / High-Recall Candidates

- Included feeder-source edges from the 4160/ESF buses into the 480 V load-center FDR breakers where the crop shows routed feeder trunks, even when part of the trunk leaves a focused crop.
- Included `BUS-480-2A -- CB-DC-A` and `BUS-480-2B -- CB-DC-B` because the lower DC breaker upstream lines are routed from the adjacent 480 V ESF load-center boundaries; these are visually plausible long-run feed associations.
- Included dashed panel/JB/relay edges in each 480 V load center (`PNL-*`, `JB-*`, `RELAY-K*`) as high-recall control candidates, not as same-bus cliques.
- Included dashed RPS/control fanout edges among `RELAY-KA/KB*`, `ANN-*`, `REC-SER-*`, `INST-NIS-*`, `PNL-RPS-*`, `PNL-DCS-*`, and `JB-CTRL-*`; these are dashed/control-line evidence and should be treated as lower confidence than solid power-bus taps.
- Included `BUS-125DC-A -- DC-DC-1` as a probable input to the raw-visible DC/DC converter, and `DC-DC-1 -- BUS-24DC-C` as the output; the converter output to 24 VDC is visually stronger than its upstream source.
- Included `BUS-24DC-C -- JB-CTRL-A` because the 24 V/control bus appears to pass through or terminate at that junction box; no arbitrary WN node was added.

Detailed uncertain edges retained in the matrix:
- `PNL-1A` -- `JB-1A-1` (480 V load center 1A; dashed panel/JB control run)
- `PNL-1A` -- `RELAY-K11` (480 V load center 1A; dashed panel-to-relay control run)
- `RELAY-K11` -- `RELAY-K12` (480 V load center 1A; relay pair joined on lower control line)
- `RELAY-K12` -- `JB-1A-1` (480 V load center 1A; dashed relay/JB control return)
- `PNL-1C` -- `JB-1C-1` (480 V load center 1C; dashed panel/JB control run)
- `PNL-1C` -- `RELAY-K21` (480 V load center 1C; dashed panel-to-relay control run)
- `RELAY-K21` -- `RELAY-K22` (480 V load center 1C; relay pair joined on lower control line)
- `RELAY-K22` -- `JB-1C-1` (480 V load center 1C; dashed relay/JB control return)
- `PNL-1B` -- `JB-1B-1` (480 V load center 1B; dashed panel/JB control run)
- `PNL-1B` -- `RELAY-K31` (480 V load center 1B; dashed panel-to-relay control run)
- `RELAY-K31` -- `RELAY-K32` (480 V load center 1B; relay pair joined on lower control line)
- `RELAY-K32` -- `JB-1B-1` (480 V load center 1B; dashed relay/JB control return)
- `PNL-2A` -- `JB-2A-1` (480 V load center 2A; dashed panel/JB control run)
- `PNL-2A` -- `RELAY-K41` (480 V load center 2A; dashed panel-to-relay control run)
- `RELAY-K41` -- `RELAY-K42` (480 V load center 2A; relay pair joined on lower control line)
- `RELAY-K42` -- `JB-2A-1` (480 V load center 2A; dashed relay/JB control return)
- `PNL-2C` -- `JB-2C-1` (480 V load center 2C; dashed panel/JB control run)
- `PNL-2C` -- `RELAY-K51` (480 V load center 2C; dashed panel-to-relay control run)
- `RELAY-K51` -- `RELAY-K52` (480 V load center 2C; relay pair joined on lower control line)
- `RELAY-K52` -- `JB-2C-1` (480 V load center 2C; dashed relay/JB control return)
- `PNL-2B` -- `JB-2B-1` (480 V load center 2B; dashed panel/JB control run)
- `PNL-2B` -- `RELAY-K61` (480 V load center 2B; dashed panel-to-relay control run)
- `RELAY-K61` -- `RELAY-K62` (480 V load center 2B; relay pair joined on lower control line)
- `RELAY-K62` -- `JB-2B-1` (480 V load center 2B; dashed relay/JB control return)
- `BUS-480-2A` -- `CB-DC-A` (Lower DC/UPS power; upstream feed routed from 2A lower-left boundary to DC breaker)
- `BUS-480-2B` -- `CB-DC-B` (Lower DC/UPS power; upstream feed routed from 2B lower-right boundary to DC breaker)
- `RELAY-KA1` -- `RELAY-KA2` (120 VAC RPS/control A; dashed relay-to-relay control line)
- `RELAY-KA1` -- `PNL-RPS-A` (120 VAC RPS/control A; dashed relay input to RPS panel)
- `RELAY-KA2` -- `PNL-RPS-A` (120 VAC RPS/control A; dashed relay input to RPS panel)
- `ANN-A` -- `PNL-RPS-A` (120 VAC RPS/control A; dashed annunciator bundle into RPS panel)
- `REC-SER-A` -- `PNL-RPS-A` (120 VAC RPS/control A; dashed recorder bundle into RPS panel)
- `INST-NIS-A` -- `PNL-RPS-A` (120 VAC RPS/control A; dashed NIS/RPS association)
- `PNL-RPS-A` -- `PNL-DCS-A` (120 VAC RPS/control A; vertical RPS-to-DCS panel run)
- `PNL-DCS-A` -- `JB-CTRL-A` (120 VAC RPS/control A; dashed DCS-to-control-JB run)
- `RELAY-KB1` -- `RELAY-KB2` (120 VAC RPS/control B; dashed relay-to-relay control line)
- `RELAY-KB1` -- `PNL-RPS-B` (120 VAC RPS/control B; dashed relay input to RPS panel)
- `RELAY-KB2` -- `PNL-RPS-B` (120 VAC RPS/control B; dashed relay input to RPS panel)
- `ANN-B` -- `PNL-RPS-B` (120 VAC RPS/control B; dashed annunciator bundle into RPS panel)
- `REC-SER-B` -- `PNL-RPS-B` (120 VAC RPS/control B; dashed recorder bundle into RPS panel)
- `INST-NIS-B` -- `PNL-RPS-B` (120 VAC RPS/control B; dashed NIS/RPS association)
- `PNL-RPS-B` -- `PNL-DCS-B` (120 VAC RPS/control B; vertical RPS-to-DCS panel run)
- `PNL-DCS-B` -- `JB-CTRL-B` (120 VAC RPS/control B; dashed DCS-to-control-JB run)
- `BUS-125DC-A` -- `DC-DC-1` (24 VDC/control center; probable input to raw-visible DC/DC converter from upper DC run)
- `BUS-24DC-C` -- `JB-CTRL-A` (24 VDC/control center; solid lower control bus passes through/at JB-CTRL-A)
- `PNL-RADMON` -- `RELAY-KTIE` (24 VDC/control center; dashed rad-monitor tie relay run)

## Validation Summary

- Node count: 200 (184 inventory components + 1 added physical + 15 printed bus nodes).
- Undirected edge count: 225.
- Matrix shape: 200 rows x 200 columns, with the same node order on rows and columns.
- Symmetric: True.
- Diagonal zero: True.
- Isolated nodes: 0.

Output files:
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\23\Results\Iteration_1\round_01_diego_matrix.csv`
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\23\Results\Iteration_1\round_01_diego_notes.md`
