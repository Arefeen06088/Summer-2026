# Extraction Note - Document 38

Generated: 2026-07-14T13:28:55

## Scope

Only the raw schematic image and crops generated from that raw image were used. Sibling derived folders and any ground-truth resources were not inspected.

## Final Connectivity

- Nodes: 54
- Edges: 55
- Symmetric matrix: True
- Diagonal zero: True

## Multi-Agent Rounds

- Round 1 (Diego, high_recall): 74 nodes, 78 edges. High-recall proposal included off-sheet continuation, MCC bucket numbers, cable-route labels, ESF area labels, and ambiguous A-side/bus/ground extras.
- Round 2 (Jennifer, precision_review): 54 nodes, 55 edges. Precision review folded MCC bucket numbers into MCC-to-load edges and removed route labels, continuation boxes, ground/reference labels, and unsupported A-side inferred edges.
- Round 3 (Diego, saturation): 54 nodes, 55 edges. Diego accepted Jennifer's precision graph after checking the raw-only crops.
- Round 4 (Jennifer, final): 54 nodes, 55 edges. Final confirmation using normalized primary device IDs and exact bus labels.

## Precision Decisions

The final graph excludes off-sheet continuation boxes, route-label text, MCC bucket numbers, ESF area labels, and station ground because those did not constitute supported retained component nodes in the raw schematic.

- Rejected TO UNIT AUX BUS CONT.: Off-sheet continuation box, not retained as a matrix component.
- Rejected MCC-2A1-01..06: MCC bucket/local-disconnect numbers were folded into MCC-to-load edges.
- Rejected MCC-2B1-01..06: MCC bucket/local-disconnect numbers were folded into MCC-to-load edges.
- Rejected 2A-C72/2A-C86/2B-C72/2B-C86: Dashed cable-route labels, not components.
- Rejected ESF DIESEL A/B: Area/enclosure text labels; actual electrical nodes are DG-2A and DG-2B.
- Rejected GND-STA: Station ground reference symbol only; not a visible direct electrical connection to a retained component.
- Rejected TR-CPT-A--BUS-120AC-A: A-side transformer secondary ends at an isolated dot/gap and does not visibly land on BUS-120AC-A.
- Rejected BUS-120AC-A--RELAY-27A: No visible BUS-120AC-A tap to RELAY-27A; RELAY-27A is only dashed to RPS-PNL-A.

## Final Edges

- GEN-U2A -- CB-101: Solid conductor from generator GEN-U2A to breaker CB-101.
- CB-101 -- TR-UAT-2A: CB-101 output is wired into transformer TR-UAT-2A.
- TR-UAT-2A -- BUS-4160A: Transformer secondary lands on BUS-4160A with a junction dot.
- DG-2A -- CB-103: Diesel generator DG-2A feeds breaker CB-103.
- CB-103 -- BUS-4160A: CB-103 feeder ties into the BUS-4160A riser.
- BUS-4160A -- CB-105: Left side of the normally open bus-tie breaker connects to BUS-4160A.
- CB-105 -- BUS-4160B: Right side of the normally open bus-tie breaker connects to BUS-4160B.
- TR-SUT-2B -- CB-102: Startup auxiliary transformer TR-SUT-2B feeds breaker CB-102.
- CB-102 -- BUS-4160B: CB-102 drops onto BUS-4160B with a junction dot.
- DG-2B -- CB-104: Diesel generator DG-2B feeds breaker CB-104.
- CB-104 -- BUS-4160B: CB-104 feeder lands on BUS-4160B.
- BUS-4160A -- CB-201A: BUS-4160A vertical feeder enters CB-201A.
- CB-201A -- TR-201A: CB-201A is in series above transformer TR-201A.
- TR-201A -- CB-301A: Transformer TR-201A output passes through CB-301A.
- CB-301A -- BUS-480A: CB-301A lands on BUS-480A.
- BUS-4160B -- CB-201B: BUS-4160B vertical feeder enters CB-201B.
- CB-201B -- TR-201B: CB-201B is in series above transformer TR-201B.
- TR-201B -- CB-301B: Transformer TR-201B output passes through CB-301B.
- CB-301B -- BUS-480B: CB-301B lands on BUS-480B.
- BUS-480A -- CB-401A: BUS-480A feeder enters CB-401A.
- CB-401A -- MCC-2A1: CB-401A output enters MCC-2A1.
- MCC-2A1 -- PUMP-RHR2A: MCC-2A1 bucket 01 feeder 2A-F1 drops to PUMP-RHR2A.
- MCC-2A1 -- PUMP-CCW2A: MCC-2A1 bucket 02 feeder 2A-F2 drops to PUMP-CCW2A.
- MCC-2A1 -- PUMP-SW2A: MCC-2A1 bucket 03 feeder 2A-F3 drops to PUMP-SW2A.
- MCC-2A1 -- FAN-CR2A: MCC-2A1 bucket 04 feeder 2A-F4 drops to FAN-CR2A.
- MCC-2A1 -- MOV-RHR141A: MCC-2A1 bucket 05 feeder 2A-F5 drops to MOV-RHR141A.
- MCC-2A1 -- MOV-SI221A: MCC-2A1 bucket 06 feeder 2A-F6 drops to MOV-SI221A.
- BUS-480A -- TR-CPT-A: A solid feeder from BUS-480A drops to TR-CPT-A.
- BUS-480A -- CHGR-2A: A separate solid feeder from BUS-480A supplies CHGR-2A.
- CHGR-2A -- 125 VDC TRAIN A: Charger output lands on the Train A 125 VDC bus.
- BAT-125A -- 125 VDC TRAIN A: Battery BAT-125A lands directly on the Train A 125 VDC bus.
- 125 VDC TRAIN A -- INV-2A: Train A 125 VDC bus feeds inverter INV-2A.
- INV-2A -- BUS-120AC-A: INV-2A AC output lands on BUS-120AC-A.
- 125 VDC TRAIN A -- RELAY-86A: Dashed control lead terminates at the Train A DC bus and RELAY-86A.
- BUS-120AC-A -- RPS-PNL-A: BUS-120AC-A has a solid vertical feed to RPS-PNL-A.
- RPS-PNL-A -- RELAY-27A: Dashed control connection runs between RPS-PNL-A and RELAY-27A.
- BUS-480B -- CB-401B: BUS-480B feeder enters CB-401B.
- CB-401B -- MCC-2B1: CB-401B output enters MCC-2B1.
- MCC-2B1 -- PUMP-RHR2B: MCC-2B1 bucket 01 feeder 2B-F1 drops to PUMP-RHR2B.
- MCC-2B1 -- PUMP-CCW2B: MCC-2B1 bucket 02 feeder 2B-F2 drops to PUMP-CCW2B.
- MCC-2B1 -- PUMP-SW2B: MCC-2B1 bucket 03 feeder 2B-F3 drops to PUMP-SW2B.
- MCC-2B1 -- FAN-CR2B: MCC-2B1 bucket 04 feeder 2B-F4 drops to FAN-CR2B.
- MCC-2B1 -- MOV-RHR142B: MCC-2B1 bucket 05 feeder 2B-F5 drops to MOV-RHR142B.
- MCC-2B1 -- MOV-SI222B: MCC-2B1 bucket 06 feeder 2B-F6 drops to MOV-SI222B.
- BUS-480B -- TR-CPT-B: A solid feeder from BUS-480B drops to TR-CPT-B.
- BUS-480B -- CHGR-2B: A separate solid feeder from BUS-480B supplies CHGR-2B.
- TR-CPT-B -- BUS-120AC-B: TR-CPT-B secondary visibly lands on BUS-120AC-B.
- CHGR-2B -- 125 VDC TRAIN B: Charger output lands on the Train B 125 VDC bus.
- BAT-125B -- 125 VDC TRAIN B: Battery BAT-125B lands directly on the Train B 125 VDC bus.
- 125 VDC TRAIN B -- INV-2B: Train B 125 VDC bus feeds inverter INV-2B.
- INV-2B -- BUS-120AC-B: INV-2B AC output lands on BUS-120AC-B.
- 125 VDC TRAIN B -- RELAY-86B: Dashed control lead terminates at the Train B DC bus and RELAY-86B.
- BUS-120AC-B -- RPS-PNL-B: BUS-120AC-B has a solid vertical feed to RPS-PNL-B.
- BUS-120AC-B -- RELAY-27B: RELAY-27B is visibly tied at the BUS-120AC-B junction.
- RPS-PNL-B -- RELAY-27B: Dashed control connection runs between RPS-PNL-B and RELAY-27B.

## Token Performance Tracking

Actual per-response usage objects and reasoning-token counts were not exposed through the available Codex/subagent tools. OPENAI_API_KEY was not available, so the OpenAI Responses input-token counting endpoint could not be called for planned payloads. The CSVs therefore contain low/expected/high estimates and mark actual usage unavailable.

- Estimated total tokens low: 110150
- Estimated total tokens expected: 144400
- Estimated total tokens high: 195300

Detailed token rows are in token_performance_tracking.csv and token_usage_estimates_by_call.csv. The misspelled compatibility file token_performance_traking.csv is also written.
