# Diego Round 01 Connectivity Notes

## Scope and Inputs
- Used only doc 19 raw schematic and derived doc 19 artifacts under `Input resources` and `Codes and artifacts`.
- Matrix rows and columns are the same ordered node list; WN-* intermediate wire-node IDs are not included.
- Section/header text such as `DIVISION A SAFETY BUS AND LOAD GROUPS`, `480 V LOAD FEEDERS - SOLID POWER DROPS`, and `CONTROL POWER / DC DISTRIBUTION` is not included as a node.

## Node List Rationale
- Physical component nodes start from `component_labels_list.csv`, checked against the raw schematic crops.
- Feeder transformer labels shown in the CSV as `PT-201`, `PT-202`, etc. are corrected to the raw printed `CPT-*` labels: `CPT-201`, `CPT-202`, `CPT-203`, `CPT-204`, `CPT-301`, `CPT-302`, `CPT-401`, `CPT-402`, `CPT-501`, `CPT-502`, `CPT-601`, `CPT-701`.
- `PT-4160A` and `PT-4160B` are retained as PT labels because the top bus instruments are printed that way.
- Added visually printed logical buses: BUS-4160-A, BUS-4160-B, BUS-480-A, BUS-480-B, BUS-120AC-A, BUS-120AC-B, BUS-125DC-A, BUS-125DC-B.
- Added visually printed nodes missed by the CSV: `DS-F301`, `CB-F402`, and `LS-MOV601`.

## Evidence Summary
- Solid evidence means continuous solid conductor/power drop in the raw crop.
- Dashed evidence means visible dashed control/signal conductor in the raw crop.
- Uncertain included edges are in the matrix because Diego is high recall, but they depend on interpreting the unlabeled lower distribution frame as a continuation from the 480 V deck rather than as a separately named node.

### Top Switchgear and Bus Solid Edges
- GRID-1 -- DS-101
- DS-101 -- CB-101
- CB-101 -- TR-101
- TR-101 -- BUS-4160-A
- DG-1 -- CB-DG1
- CB-DG1 -- BUS-4160-A
- PT-4160A -- BUS-4160-A
- BUS-4160-A -- CB-TIE-4160
- CB-TIE-4160 -- BUS-4160-B
- BUS-4160-A -- CB-201
- CB-201 -- TR-480-A
- TR-480-A -- CB-480-A
- CB-480-A -- BUS-480-A
- GRID-2 -- DS-102
- DS-102 -- CB-102
- CB-102 -- TR-102
- TR-102 -- BUS-4160-B
- DG-2 -- CB-DG2
- CB-DG2 -- BUS-4160-B
- PT-4160B -- BUS-4160-B
- BUS-4160-B -- CB-202
- CB-202 -- TR-480-B
- TR-480-B -- CB-480-B
- CB-480-B -- BUS-480-B
- BUS-480-A -- CB-TIE-480
- CB-TIE-480 -- BUS-480-B

### Repeated Feeder Evidence
- A-side feeders from `BUS-480-A`: 201, 203, 301, 401, 501, 601.
- B-side feeders from `BUS-480-B`: 202, 204, 302, 402, 502, 701.
- For each feeder, the solid chain is `BUS-480-* -- CB-Fxxx -- DS-Fxxx -- CPT-xxx -- MCC-xxx -- CB-Lxxx -- RELAY-Kxxx -- load`.
- For each feeder, dashed/control evidence includes `CB-Fxxx -- RELAY-PRxxx`, `MCC-xxx -- RELAY-Axxx`, load/instrument/JB/TB/LCS links.
- Load endpoints: pumps for 201/202/203/204/301/302/401/402, motors for 501/502, valve path for 601, and RPS instrument path for 701.

### Lower Control/DC Solid Edges
- CB-301 -- TR-120-A
- TR-120-A -- BUS-120AC-A
- CB-302 -- TR-120-B
- TR-120-B -- BUS-120AC-B
- CHGR-125A -- BAT-125A
- BAT-125A -- BUS-125DC-A
- INV-120A -- BUS-125DC-A
- CHGR-125B -- BAT-125B
- BAT-125B -- BUS-125DC-B
- INV-120B -- BUS-125DC-B

### Dashed Control/Signal Edges
- CB-F201 -- RELAY-PR201
- MCC-201 -- RELAY-A201
- PUMP-P201 -- INST-201
- INST-201 -- JB-201
- JB-201 -- TB-201
- TB-201 -- LCS-201
- CB-F203 -- RELAY-PR203
- MCC-203 -- RELAY-A203
- PUMP-P203 -- INST-203
- INST-203 -- JB-203
- JB-203 -- TB-203
- TB-203 -- LCS-203
- CB-F301 -- RELAY-PR301
- MCC-301 -- RELAY-A301
- PUMP-P301 -- INST-301
- INST-301 -- JB-301
- JB-301 -- TB-301
- TB-301 -- LCS-301
- CB-F401 -- RELAY-PR401
- MCC-401 -- RELAY-A401
- PUMP-P401 -- INST-401
- INST-401 -- JB-401
- JB-401 -- TB-401
- TB-401 -- LCS-401
- CB-F501 -- RELAY-PR501
- MCC-501 -- RELAY-A501
- MTR-F501 -- INST-501
- INST-501 -- JB-501
- JB-501 -- TB-501
- TB-501 -- LCS-501
- CB-F601 -- RELAY-PR601
- MCC-601 -- RELAY-A601
- VALVE-MOV601 -- INST-601
- INST-601 -- LS-MOV601
- LS-MOV601 -- JB-601
- JB-601 -- TB-601
- TB-601 -- LCS-601
- CB-F202 -- RELAY-PR202
- MCC-202 -- RELAY-A202
- PUMP-P202 -- INST-202
- INST-202 -- JB-202
- JB-202 -- TB-202
- TB-202 -- LCS-202
- CB-F204 -- RELAY-PR204
- MCC-204 -- RELAY-A204
- PUMP-P204 -- INST-204
- INST-204 -- JB-204
- JB-204 -- TB-204
- TB-204 -- LCS-204
- CB-F302 -- RELAY-PR302
- MCC-302 -- RELAY-A302
- PUMP-P302 -- INST-302
- INST-302 -- JB-302
- JB-302 -- TB-302
- TB-302 -- LCS-302
- CB-F402 -- RELAY-PR402
- MCC-402 -- RELAY-A402
- PUMP-P402 -- INST-402
- INST-402 -- JB-402
- JB-402 -- TB-402
- TB-402 -- LCS-402
- CB-F502 -- RELAY-PR502
- MCC-502 -- RELAY-A502
- MTR-F502 -- INST-502
- INST-502 -- JB-502
- JB-502 -- TB-502
- TB-502 -- LCS-502
- CB-F701 -- RELAY-PR701
- MCC-701 -- RELAY-A701
- INST-RPS701 -- INST-701
- INST-701 -- JB-701
- JB-701 -- TB-701
- TB-701 -- LCS-701
- BUS-120AC-A -- JB-MAIN
- INV-120A -- PN-RPS-A
- INV-120B -- PN-RPS-B

### Uncertain Included Candidates
- BUS-480-A -- CB-301
- BUS-480-A -- CHGR-125A
- BUS-480-B -- CB-302
- BUS-480-B -- CHGR-125B

## Uncertain Candidates Kept Out
- Did not add `CONTROL POWER / DC DISTRIBUTION` as a row/column node because it reads as section/header text rather than a clear bus label.
- Did not connect `CHGR-125A` or `CHGR-125B` directly to the 120VAC buses: the vertical charger/battery conductors do not show clear connection dots at the 120VAC bus crossings.
- Did not add direct component-to-component clique edges along buses; logical `BUS-*` nodes represent those shared conductors.
- Did not add WN-* wire-node IDs or arbitrary intermediate bends/endpoints.

## Validation Summary
- Node count: 200
- Edge count: 200
- Symmetric: True
- Diagonal zero: True
- Row/column labels identical: True
