# Extraction Note - Document 37

Generated: 2026-07-14T13:12:53

## Scope

Only the raw schematic image and raw-derived crops made from that image were used. Ground-truth and GT-derived folders were not used.

## Final Connectivity

- Nodes: 55
- Edges: 56
- Symmetric matrix: True
- Diagonal zero: True

## Multi-Agent Rounds

- Round 1 (Diego, high_recall): 63 edges. High-recall proposal retained plausible but visually over-broad logical ties for reviewer pruning.
- Round 2 (Jennifer, precision_review): 56 edges. Precision review removed unsupported extra relay, rack, charger-battery, and grid-tie shortcuts.
- Round 3 (Diego, saturation): 56 edges. Diego accepted Jennifer's precision edge set after rechecking the raw image and raw-only crops.
- Round 4 (Jennifer, final): 56 edges. Final precision confirmation: no additional supported edges beyond the saturated graph.

## Precision Decisions

Jennifer removed Diego's high-recall extras where the schematic showed a common bus, route annotation, or dashed routing path rather than a direct component-to-component termination.

- Rejected PAN-RPS-A -- INST-RACK-A: Both land on BUS-120A, but no direct wire between the panel and rack is visually supported.
- Rejected INST-RACK-A -- PLC-ESF: Dashed C03 is traced from PAN-RPS-A to PLC-ESF, not from INST-RACK-A.
- Rejected RELAY-K12A -- PLC-ESF: RELAY-K12A terminates C01 from ATS-1A; no continuous supported segment to PLC-ESF.
- Rejected RELAY-K12B -- PLC-ESF: C05 appears as routing/annotation near the relay area without a clear PLC-ESF termination.
- Rejected CHGR-125A -- BAT-125A: Both connect to BUS-125DCA; the charger and battery are not directly connected to each other.
- Rejected CHGR-125B -- BAT-125B: Both connect to BUS-125DCB; the charger and battery are not directly connected to each other.
- Rejected GRID-345 -- CB-TIE-6K: CB-TIE-6K ties BUS-6KA and BUS-6KB only; GRID-345 reaches the buses through CB-101/CB-102 and transformers.

## Final Edges

- AUX-TR-1A -- CB-101: Top-left offsite feeder. CB-101 is drawn inline between GRID-345 and AUX-TR-1A.
- CB-101 -- GRID-345: GRID-345 bus ties directly into CB-101 at the left top feeder.
- GRID-345 -- CB-102: GRID-345 bus ties directly into CB-102 at the right top feeder.
- CB-102 -- AUX-TR-1B: Top-right offsite feeder. CB-102 is drawn inline between GRID-345 and AUX-TR-1B.
- AUX-TR-1A -- BUS-6KA: Transformer secondary drops to BUS-6KA.
- AUX-TR-1B -- BUS-6KB: Transformer secondary drops to BUS-6KB.
- BUS-6KA -- CB-TIE-6K: Horizontal bus tie breaker connects between the two 6 kV buses.
- CB-TIE-6K -- BUS-6KB: Horizontal bus tie breaker connects between the two 6 kV buses.
- BUS-6KA -- CB-103A: Train A feeder leaves BUS-6KA through CB-103A.
- CB-103A -- SWGR-1EA: CB-103A output enters SWGR-1EA.
- DG-1A -- CB-DG1A: Emergency diesel generator 1A feeds its breaker.
- CB-DG1A -- SWGR-1EA: DG breaker output connects into Train A switchgear.
- SWGR-1EA -- ATS-1A: Train A switchgear feeder runs to ATS-1A.
- ATS-1A -- RELAY-K12A: Dashed control C01 leaves ATS-1A and terminates at RELAY-K12A.
- ATS-1A -- TR-480A: ATS-1A output feeds transformer TR-480A.
- TR-480A -- BUS-480A: TR-480A secondary connects to BUS-480A.
- BUS-480A -- MCC-1A: 480 V bus feeds Train A MCC.
- MCC-1A -- PUMP-SI-1A: MCC-1A branch to safety injection pump 1A.
- MCC-1A -- PUMP-RHR-1A: MCC-1A branch to residual heat removal pump 1A.
- MCC-1A -- PUMP-CCW-1A: MCC-1A branch to component cooling water pump 1A.
- MCC-1A -- FAN-RB-1A: MCC-1A branch to reactor building fan 1A.
- MCC-1A -- MOV-HPCI-1A: MCC-1A branch to HPCI motor-operated valve 1A.
- MCC-1A -- VALVE-SW-1A: MCC-1A branch to service water valve 1A.
- BUS-480A -- CHGR-125A: 480 V bus supplies charger CHGR-125A.
- CHGR-125A -- BUS-125DCA: Charger output lands on the 125 VDC A bus.
- BAT-125A -- BUS-125DCA: Battery BAT-125A lands directly on the 125 VDC A bus.
- BUS-125DCA -- INV-120A: DC bus feeds inverter INV-120A.
- BUS-125DCA -- GND-01A: Labeled ground/reference tap GND-01A connects to the DC A bus.
- INV-120A -- BUS-120A: Inverter output feeds BUS-120A.
- BUS-120A -- PAN-RPS-A: AC instrumentation bus feeds RPS panel A.
- BUS-120A -- INST-RACK-A: AC instrumentation bus feeds instrument rack A.
- PAN-RPS-A -- PLC-ESF: Dashed functional cable C03 runs from PAN-RPS-A to PLC-ESF.
- BUS-6KB -- CB-103B: Train B feeder leaves BUS-6KB through CB-103B.
- CB-103B -- SWGR-1EB: CB-103B output enters SWGR-1EB.
- DG-1B -- CB-DG1B: Emergency diesel generator 1B feeds its breaker.
- CB-DG1B -- SWGR-1EB: DG breaker output connects into Train B switchgear.
- SWGR-1EB -- ATS-1B: Train B switchgear feeder runs to ATS-1B.
- ATS-1B -- RELAY-K12B: Dashed control C04 leaves ATS-1B and terminates at RELAY-K12B.
- ATS-1B -- TR-480B: ATS-1B output feeds transformer TR-480B.
- TR-480B -- BUS-480B: TR-480B secondary connects to BUS-480B.
- BUS-480B -- MCC-1B: 480 V bus feeds Train B MCC.
- MCC-1B -- PUMP-SI-1B: MCC-1B branch to safety injection pump 1B.
- MCC-1B -- PUMP-RHR-1B: MCC-1B branch to residual heat removal pump 1B.
- MCC-1B -- PUMP-CCW-1B: MCC-1B branch to component cooling water pump 1B.
- MCC-1B -- FAN-RB-1B: MCC-1B branch to reactor building fan 1B.
- MCC-1B -- MOV-HPCI-1B: MCC-1B branch to HPCI motor-operated valve 1B.
- MCC-1B -- VALVE-SW-1B: MCC-1B branch to service water valve 1B.
- BUS-480B -- CHGR-125B: 480 V bus supplies charger CHGR-125B.
- CHGR-125B -- BUS-125DCB: Charger output lands on the 125 VDC B bus.
- BAT-125B -- BUS-125DCB: Battery BAT-125B lands directly on the 125 VDC B bus.
- BUS-125DCB -- INV-120B: DC bus feeds inverter INV-120B.
- BUS-125DCB -- GND-01B: Labeled ground/reference tap GND-01B connects to the DC B bus.
- INV-120B -- BUS-120B: Inverter output feeds BUS-120B.
- BUS-120B -- PAN-RPS-B: AC instrumentation bus feeds RPS panel B.
- BUS-120B -- INST-RACK-B: AC instrumentation bus feeds instrument rack B.
- PLC-ESF -- PAN-RPS-B: Dashed functional cable C06 runs from PLC-ESF to PAN-RPS-B.

## Token Performance Tracking

Actual per-response usage objects and reasoning-token counts were not exposed through the available Codex subagent tools in this session. OPENAI_API_KEY was not available, so the Responses input-token counting endpoint could not be called for the planned payloads. The CSVs therefore contain low/expected/high estimates and mark actual usage unavailable.

- Estimated total tokens low: 92300
- Estimated total tokens expected: 122000
- Estimated total tokens high: 165900

Detailed token rows are in token_performance_tracking.csv and token_usage_estimates_by_call.csv. The misspelled compatibility file token_performance_traking.csv is also written.
