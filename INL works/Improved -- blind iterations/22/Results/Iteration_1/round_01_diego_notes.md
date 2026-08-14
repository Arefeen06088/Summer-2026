# Round 01 Diego Connectivity Notes

## Source Boundary

Used only doc 22 raw/derived resources in `Input resources` and raw-derived inspection crops in `Codes and artifacts/inspection_crops`. Ground truth, evaluator output, metric feedback, and GT-derived files were not opened or used.

## Node List Rationale

- Started from the 181 physical-component labels in `component_labels_list.csv`.
- Added 14 raw-visible printed logical bus nodes: BUS-13A, BUS-13B, BUS-4160-A, BUS-4160-B, BUS-4160-C, BUS-4160-D, BUS-480-A, BUS-480-B, BUS-480-C, BUS-480-D, BUS-125A, BUS-125B, BUS-UPS-A, BUS-UPS-B.
- Added 5 raw-visible D-train components absent from the prepared inventory: INST-PT-D, CB-CH-D, CB-VLV1-D, CB-VLV2-D, CB-SPARE-D. These are visible in the raw right-edge 480 V train D area; the added crop `19_480_train_d_right_raw.png` documents the four D-side load breakers, and `18_inst_pt_d_raw.png` documents `INST-PT-D`.
- Did not add WN-* wire nodes, unlabeled junction dots, drawing titles, note text, voltage descriptions, or dashed section boundaries.

## Edge Evidence By Area

### Top generation, switchyard, 13.8 kV aux buses

- `AUX-XFMR-1A` -- `BUS-13A`
- `AUX-XFMR-1A` -- `CB-4A-IN`
- `AUX-XFMR-1B` -- `BUS-13A`
- `AUX-XFMR-1B` -- `CB-4B-IN`
- `BUS-13A` -- `CB-13A1`
- `BUS-13A` -- `CB-13T`
- `BUS-13A` -- `RELAY-87U`
- `BUS-13B` -- `CB-13B1`
- `BUS-13B` -- `CB-13T`
- `BUS-13B` -- `SAT-XFMR-1C`
- `BUS-13B` -- `SAT-XFMR-1D`
- `BUS-4160-A` -- `CB-4A-IN`
- `BUS-4160-A` -- `SYNC-PNL-1`
- `BUS-4160-B` -- `CB-4B-IN`
- `BUS-4160-C` -- `CB-4C-IN`
- `BUS-4160-D` -- `CB-4D-IN`
- `CB-13A1` -- `SWYD-345`
- `CB-13B1` -- `SWYD-345`
- `CB-4B-IN` -- `RELAY-87U`
- `CB-4C-IN` -- `SAT-XFMR-1C`
- `CB-4D-IN` -- `SAT-XFMR-1D`
- `CB-DG-A` -- `SYNC-PNL-1`
- `GEN-G01` -- `GSU-T01`
- `GSU-T01` -- `SWYD-345`

### 4160 V safety buses, DG feeders, ties, load-center transformers

- `BUS-4160-A` -- `CB-4AB-TIE`
- `BUS-4160-A` -- `CB-DG-A`
- `BUS-4160-A` -- `CB-LC-A`
- `BUS-4160-B` -- `CB-4AB-TIE`
- `BUS-4160-B` -- `CB-DG-B`
- `BUS-4160-B` -- `CB-LC-B`
- `BUS-4160-C` -- `CB-4CD-TIE`
- `BUS-4160-C` -- `CB-DG-C`
- `BUS-4160-C` -- `CB-LC-C`
- `BUS-4160-D` -- `CB-4CD-TIE`
- `BUS-4160-D` -- `CB-DG-D`
- `BUS-4160-D` -- `CB-LC-D`
- `BUS-480-A` -- `TR-LC-A`
- `BUS-480-B` -- `TR-LC-B`
- `BUS-480-C` -- `TR-LC-C`
- `BUS-480-D` -- `TR-LC-D`
- `CB-DG-A` -- `DG-1A`
- `CB-DG-B` -- `DG-1B`
- `CB-DG-C` -- `DG-1C`
- `CB-DG-D` -- `DG-1D`
- `CB-LC-A` -- `TR-LC-A`
- `CB-LC-B` -- `TR-LC-B`
- `CB-LC-C` -- `TR-LC-C`
- `CB-LC-D` -- `TR-LC-D`

### 480 V load centers and MCC/load branches

- `BUS-480-A` -- `CB-MCC-AA`
- `BUS-480-A` -- `CB-MCC-AB`
- `BUS-480-A` -- `GND-A`
- `BUS-480-A` -- `INST-PT-A`
- `BUS-480-A` -- `XFMR-120-A`
- `BUS-480-B` -- `CB-MCC-BA`
- `BUS-480-B` -- `CB-MCC-BB`
- `BUS-480-B` -- `GND-B`
- `BUS-480-B` -- `INST-PT-B`
- `BUS-480-B` -- `XFMR-120-B`
- `BUS-480-C` -- `CB-MCC-CA`
- `BUS-480-C` -- `CB-MCC-CB`
- `BUS-480-C` -- `GND-C`
- `BUS-480-C` -- `INST-PT-C`
- `BUS-480-C` -- `XFMR-120-C`
- `BUS-480-D` -- `CB-MCC-DA`
- `BUS-480-D` -- `CB-MCC-DB`
- `BUS-480-D` -- `GND-D`
- `BUS-480-D` -- `INST-PT-D`
- `BUS-480-D` -- `XFMR-120-D`
- `CB-CCW-A` -- `MCC-AA`
- `CB-CCW-A` -- `PUMP-CCW-A`
- `CB-CCW-B` -- `MCC-BA`
- `CB-CCW-B` -- `PUMP-CCW-B`
- `CB-CCW-C` -- `MCC-CA`
- `CB-CCW-C` -- `PUMP-CCW-C`
- `CB-CCW-D` -- `MCC-DA`
- `CB-CCW-D` -- `PUMP-CCW-D`
- `CB-CH-A` -- `CHILLER-A`
- `CB-CH-A` -- `MCC-AB`
- `CB-CH-B` -- `CHILLER-B`
- `CB-CH-B` -- `MCC-BB`
- `CB-CH-C` -- `CHILLER-C`
- `CB-CH-C` -- `MCC-CB`
- `CB-CH-D` -- `CHILLER-D`
- `CB-CH-D` -- `MCC-DB`
- `CB-FAN-A` -- `FAN-CR-A`
- `CB-FAN-A` -- `MCC-AA`
- `CB-FAN-B` -- `FAN-CR-B`
- `CB-FAN-B` -- `MCC-BA`
- `CB-FAN-C` -- `FAN-CR-C`
- `CB-FAN-C` -- `MCC-CA`
- `CB-FAN-D` -- `FAN-CR-D`
- `CB-FAN-D` -- `MCC-DA`
- `CB-MCC-AA` -- `MCC-AA`
- `CB-MCC-AB` -- `MCC-AB`
- `CB-MCC-BA` -- `MCC-BA`
- `CB-MCC-BB` -- `MCC-BB`
- `CB-MCC-CA` -- `MCC-CA`
- `CB-MCC-CB` -- `MCC-CB`
- `CB-MCC-DA` -- `MCC-DA`
- `CB-MCC-DB` -- `MCC-DB`
- `CB-RHR-A` -- `CB-SI-A`
- `CB-RHR-A` -- `INST-CT-A`
- `CB-RHR-A` -- `PUMP-RHR-A`
- `CB-RHR-B` -- `CB-SI-B`
- `CB-RHR-B` -- `INST-CT-B`
- `CB-RHR-B` -- `PUMP-RHR-B`
- `CB-RHR-C` -- `CB-SI-C`
- `CB-RHR-C` -- `INST-CT-C`
- `CB-RHR-C` -- `PUMP-RHR-C`
- `CB-RHR-D` -- `CB-SI-D`
- `CB-RHR-D` -- `INST-CT-D`
- `CB-RHR-D` -- `PUMP-RHR-D`
- `CB-SI-A` -- `MCC-AA`
- `CB-SI-A` -- `PUMP-SI-A`
- `CB-SI-B` -- `MCC-BA`
- `CB-SI-B` -- `PUMP-SI-B`
- `CB-SI-C` -- `MCC-CA`
- `CB-SI-C` -- `PUMP-SI-C`
- `CB-SI-D` -- `MCC-DA`
- `CB-SI-D` -- `PUMP-SI-D`
- `CB-SPARE-A` -- `MCC-AB`
- `CB-SPARE-A` -- `SPARE-LOAD-A`
- `CB-SPARE-B` -- `MCC-BB`
- `CB-SPARE-B` -- `SPARE-LOAD-B`
- `CB-SPARE-C` -- `MCC-CB`
- `CB-SPARE-C` -- `SPARE-LOAD-C`
- `CB-SPARE-D` -- `MCC-DB`
- `CB-SPARE-D` -- `SPARE-LOAD-D`
- `CB-VLV1-A` -- `MCC-AB`
- `CB-VLV1-A` -- `MOV-HV1-A`
- `CB-VLV1-B` -- `MCC-BB`
- `CB-VLV1-B` -- `MOV-HV1-B`
- `CB-VLV1-C` -- `MCC-CB`
- `CB-VLV1-C` -- `MOV-HV1-C`
- `CB-VLV1-D` -- `MCC-DB`
- `CB-VLV1-D` -- `MOV-HV1-D`
- `CB-VLV2-A` -- `MCC-AB`
- `CB-VLV2-A` -- `MOV-HV2-A`
- `CB-VLV2-B` -- `MCC-BB`
- `CB-VLV2-B` -- `MOV-HV2-B`
- `CB-VLV2-C` -- `MCC-CB`
- `CB-VLV2-C` -- `MOV-HV2-C`
- `CB-VLV2-D` -- `MCC-DB`
- `CB-VLV2-D` -- `MOV-HV2-D`
- `INST-CT-A` -- `MCC-AA`
- `INST-CT-B` -- `MCC-BA`
- `INST-CT-C` -- `MCC-CA`
- `INST-CT-D` -- `MCC-DA`

### 120 V transformers, panels, relays, junction boxes, terminal blocks

- `JB-A1` -- `PNL-120-A`
- `JB-A1` -- `TERM-A`
- `JB-B1` -- `PNL-120-B`
- `JB-B1` -- `TERM-B`
- `JB-C1` -- `PNL-120-C`
- `JB-C1` -- `TERM-C`
- `JB-D1` -- `PNL-120-D`
- `JB-D1` -- `TERM-D`
- `PNL-120-A` -- `RELAY-KA1`
- `PNL-120-A` -- `RELAY-KA2`
- `PNL-120-A` -- `XFMR-120-A`
- `PNL-120-B` -- `RELAY-KB1`
- `PNL-120-B` -- `RELAY-KB2`
- `PNL-120-B` -- `XFMR-120-B`
- `PNL-120-C` -- `RELAY-KC1`
- `PNL-120-C` -- `RELAY-KC2`
- `PNL-120-C` -- `XFMR-120-C`
- `PNL-120-D` -- `RELAY-KD1`
- `PNL-120-D` -- `RELAY-KD2`
- `PNL-120-D` -- `XFMR-120-D`

### 125 VDC and UPS buses

- `ANN-PNL-CR` -- `BUS-UPS-A`
- `ANN-PNL-CR` -- `JB-CR-01`
- `BAT-125A` -- `BUS-125A`
- `BAT-125B` -- `BUS-125B`
- `BUS-125A` -- `CHGR-125A`
- `BUS-125A` -- `DC-MCC-A`
- `BUS-125A` -- `DIODE-OR-A`
- `BUS-125A` -- `FUSE-FD-A`
- `BUS-125A` -- `GRD-DC-A`
- `BUS-125B` -- `CHGR-125B`
- `BUS-125B` -- `DC-MCC-B`
- `BUS-125B` -- `DIODE-OR-B`
- `BUS-125B` -- `FUSE-FD-B`
- `BUS-125B` -- `GRD-DC-B`
- `BUS-480-A` -- `CB-DC-A1`
- `BUS-480-B` -- `CB-DC-B1`
- `BUS-UPS-A` -- `INST-RACK-A`
- `BUS-UPS-A` -- `INV-UPS-A`
- `BUS-UPS-A` -- `PLC-SAF-A`
- `BUS-UPS-A` -- `PNL-RPS-A`
- `BUS-UPS-B` -- `INST-RACK-B`
- `BUS-UPS-B` -- `INV-UPS-B`
- `BUS-UPS-B` -- `PLC-SAF-B`
- `BUS-UPS-B` -- `PNL-RPS-B`
- `BUS-UPS-B` -- `REC-SEQ-1`
- `CB-DC-A1` -- `CHGR-125A`
- `CB-DC-B1` -- `CHGR-125B`
- `DC-MCC-A` -- `SOL-SDV-A`
- `DC-MCC-B` -- `SOL-SDV-B`
- `FUSE-FD-A` -- `INV-UPS-A`
- `FUSE-FD-B` -- `INV-UPS-B`
- `JB-CR-01` -- `TERM-MTB-A`
- `JB-CR-01` -- `TERM-MTB-B`
- `METER-A01` -- `XFMR-PT-1`
- `METER-V01` -- `XFMR-PT-1`
- `PNL-RPS-A` -- `RELAY-ESF-A`
- `PNL-RPS-A` -- `RELAY-RPS-A1`
- `PNL-RPS-B` -- `RELAY-ESF-B`
- `PNL-RPS-B` -- `RELAY-RPS-B1`

## Uncertain / High-Recall Candidates

- Included `BUS-13A` -- `RELAY-87U` and `RELAY-87U` -- `CB-4B-IN` because the raw crop shows a dashed protection/control path from the 13.8 kV bus area down through relay 87U toward the 4B incoming breaker.
- Included `SYNC-PNL-1` -- `BUS-4160-A` and `SYNC-PNL-1` -- `CB-DG-A` because the dashed synchronizing panel path visibly terminates at the 4160 A / DG-A area.
- Included short dashed `CB-RHR-*` -- `CB-SI-*` links in each 480 V train. The longer dashed continuation below the SI pumps was left out as a matrix edge because its named endpoint is not visually unambiguous.
- Included `BUS-480-A` -- `CB-DC-A1` and `BUS-480-B` -- `CB-DC-B1` as long solid charger supply runs. They are less local than most bus taps but are traceable in the raw lower section.
- Did not connect line crossings without dots. Printed buses are represented as bus nodes, so components on the same printed bus attach to the bus node rather than being expanded into pairwise cliques.

## Validation Summary

- Node count: 200
- Edge count: 207
- Symmetric: True
- Diagonal zero: True
- Isolated nodes: none
