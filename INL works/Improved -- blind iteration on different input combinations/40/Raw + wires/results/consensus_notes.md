# Document 40 Consensus Notes

Final graph saturated after Diego R1 -> Jennifer R1 -> Diego R2 -> Jennifer R2.

- Final node count: 55
- Final edge count: 56
- Matrix type: undirected, symmetric, diagonal zero.
- Source restriction: only files in Raw + wires were used.
- OCR restriction: no off-the-shelf OCR was used.

## Precision Decisions

- `DC-BUS-21A -- RPS-PNL-A` and `DC-BUS-21B -- RPS-PNL-B` were removed; the dashed signal drops cross the 125 VDC buses without filled junction dots before landing at RPS terminals.
- `VOLTAGE SIG A` and `VOLTAGE SIG B` were treated as route labels, not nodes. The modeled edges are `VT-21A -- RPS-PNL-A` and `VT-21B -- RPS-PNL-B`.
- Cable IDs such as `D21A-07` and `D21B-07` were treated as conductor labels, not nodes.
- MOV-RWST21A/B have only their MCC power feeders modeled; nearby dashed/short-dash routes cross without junction dots or belong to voltage/trip routing.
- Relay-86 trip/control routes to `CB-MPA1` and `CB-MPB1` were retained because the dash-dot trip route visibly lands at the breaker trip terminals.

## Removed High-Recall Candidates

- DC-BUS-21A -- RPS-PNL-A
- DC-BUS-21B -- RPS-PNL-B

## Final Edges

- DG-21A -- ATS-21A
- UAT-2A -- DS-21A
- DS-21A -- ATS-21A
- ATS-21A -- SWGR-21A
- SWGR-21A -- TIE-BKR-21AB
- TIE-BKR-21AB -- SWGR-21B
- SWGR-21A -- CB-21A1
- CB-21A1 -- TR-21A
- TR-21A -- MCC-21A
- SAT-2B -- DS-21B
- DS-21B -- ATS-21B
- DG-21B -- ATS-21B
- ATS-21B -- SWGR-21B
- SWGR-21B -- CB-21B1
- CB-21B1 -- TR-21B
- TR-21B -- MCC-21B
- MCC-21A -- CB-MPA1
- CB-MPA1 -- PUMP-SI21A
- MCC-21A -- PUMP-CCW21A
- MCC-21A -- FAN-RB21A
- MCC-21A -- MOV-HV211A
- MCC-21A -- MOV-RWST21A
- MCC-21A -- XFMR-CPT21A
- XFMR-CPT21A -- AC-PNL-120A
- AC-PNL-120A -- RECT-21A
- RECT-21A -- DC-BUS-21A
- DC-BUS-21A -- BAT-21A
- DC-BUS-21A -- INV-21A
- VT-21A -- RPS-PNL-A
- CT-21A -- RPS-PNL-A
- LOCA-SIG-A -- JB-21A
- JB-21A -- RPS-PNL-A
- RPS-PNL-A -- RELAY-K21A
- RELAY-K21A -- RELAY-86A
- RELAY-86A -- CB-MPA1
- RPS-PNL-A -- INV-21A
- MCC-21B -- XFMR-CPT21B
- XFMR-CPT21B -- AC-PNL-120B
- AC-PNL-120B -- RECT-21B
- RECT-21B -- DC-BUS-21B
- DC-BUS-21B -- BAT-21B
- DC-BUS-21B -- INV-21B
- MCC-21B -- CB-MPB1
- CB-MPB1 -- PUMP-SI21B
- MCC-21B -- PUMP-CCW21B
- MCC-21B -- FAN-RB21B
- MCC-21B -- MOV-HV211B
- MCC-21B -- MOV-RWST21B
- VT-21B -- RPS-PNL-B
- CT-21B -- RPS-PNL-B
- LOCA-SIG-B -- JB-21B
- JB-21B -- RPS-PNL-B
- RPS-PNL-B -- RELAY-K21B
- RELAY-K21B -- RELAY-86B
- RELAY-86B -- CB-MPB1
- RPS-PNL-B -- INV-21B
