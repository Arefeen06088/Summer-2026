# Extraction Note - Document 39

Generated: 2026-07-14T13:43:12

## Scope

Only the raw schematic image and crops generated from that raw image were used. Sibling derived folders and any ground-truth resources were not inspected.

## Final Connectivity

- Nodes: 54
- Edges: 56
- Symmetric matrix: True
- Diagonal zero: True

## Multi-Agent Rounds

- Round 1 (Diego, high_recall): 56 nodes, 69 edges. High-recall proposal kept the direct graph and added uncertain LC tap nodes, UV-to-tie logic, direct RPS-to-MOV shortcuts, JB-to-control-room links, and B-side ground reference.
- Round 2 (Jennifer, precision_review): 54 nodes, 56 edges. Precision review removed unsupported high-recall extras while keeping GND-PLANT from BUS-480-A and ANN-CR01--REC-SOE01.
- Round 3 (Diego, saturation): 54 nodes, 56 edges. Diego accepted Jennifer's precision graph with no corrections.
- Round 4 (Jennifer, final): 54 nodes, 56 edges. Final confirmation of the saturated graph.

## Precision Decisions

Jennifer rejected LC tap labels as standalone nodes, removed function-only or route-ambiguous extras, kept GND-PLANT only where the A-side 480 V bus visibly terminates, and kept only the direct ANN-CR01--REC-SOE01 control-room edge.

- Rejected LC-A / LC-B as nodes: They are bus/tap labels, not standalone retained components.
- Rejected RELAY-UV-A 27/59 -- CB-TIE-AB: Functionally plausible, but no direct conductor is shown.
- Rejected RELAY-UV-B 27/59 -- CB-TIE-AB: Functionally plausible, but no direct conductor is shown.
- Rejected RPS-A DIV I -- MOV-881A / MOV-742A: MOV control is visually routed through JB-A101, not directly from RPS-A.
- Rejected RPS-B DIV II -- MOV-881B / MOV-742B: MOV control is visually routed through JB-B101, not directly from RPS-B.
- Rejected BUS-480-B 480 V LOAD CENTER B -- GND-PLANT: Only the A-side bus has a visible terminating conductor to GND-PLANT.
- Rejected JB-A101 -- ANN-CR01: Lower control-room route does not visibly terminate at both endpoints.
- Rejected JB-B101 -- REC-SOE01: Lower control-room route does not visibly terminate at both endpoints.

## Final Edges

- OFFSITE 230 kV A -- DS-230A: Solid vertical offsite source feed to disconnect DS-230A.
- DS-230A -- TR-1A 230/4.16: Solid vertical conductor from disconnect into transformer TR-1A.
- TR-1A 230/4.16 -- CB-1A: Transformer TR-1A feeds breaker CB-1A.
- CB-1A -- BUS-4160-A DIV I 4.16 kV ESF: CB-1A lands on BUS-4160-A with a junction dot.
- EDG-1A -- CB-DG-A: Emergency diesel generator EDG-1A feeds CB-DG-A.
- CB-DG-A -- BUS-4160-A DIV I 4.16 kV ESF: CB-DG-A lands on BUS-4160-A with a junction dot.
- BUS-4160-A DIV I 4.16 kV ESF -- RELAY-UV-A 27/59: Dashed control/sensing drop from BUS-4160-A to RELAY-UV-A.
- BUS-4160-A DIV I 4.16 kV ESF -- CB-TIE-AB: Left side of normally-open tie breaker connects to BUS-4160-A.
- CB-TIE-AB -- BUS-4160-B DIV II 4.16 kV ESF: Right side of normally-open tie breaker connects to BUS-4160-B.
- BUS-4160-B DIV II 4.16 kV ESF -- RELAY-UV-B 27/59: Dashed control/sensing drop from BUS-4160-B to RELAY-UV-B.
- OFFSITE 230 kV B -- DS-230B: Solid vertical offsite source feed to disconnect DS-230B.
- DS-230B -- TR-1B 230/4.16: Solid vertical conductor from disconnect into transformer TR-1B.
- TR-1B 230/4.16 -- CB-1B: Transformer TR-1B feeds breaker CB-1B.
- CB-1B -- BUS-4160-B DIV II 4.16 kV ESF: CB-1B lands on BUS-4160-B with a junction dot.
- EDG-1B -- CB-DG-B: Emergency diesel generator EDG-1B feeds CB-DG-B.
- CB-DG-B -- BUS-4160-B DIV II 4.16 kV ESF: CB-DG-B lands on BUS-4160-B with a junction dot.
- BUS-4160-A DIV I 4.16 kV ESF -- TR-480-A 4.16/0.48: BUS-4160-A vertical feeder drops to transformer TR-480-A.
- TR-480-A 4.16/0.48 -- CB-480-A: TR-480-A output feeds breaker CB-480-A.
- CB-480-A -- BUS-480-A 480 V LOAD CENTER A: CB-480-A lands on BUS-480-A with a junction dot.
- BUS-480-A 480 V LOAD CENTER A -- MCC-A1 SAFETY LOADS: BUS-480-A has a solid feeder to MCC-A1.
- BUS-480-A 480 V LOAD CENTER A -- MCC-A2 VALVE/PUMP: BUS-480-A has a solid feeder to MCC-A2.
- BUS-480-A 480 V LOAD CENTER A -- GND-PLANT: Ground-reference conductor terminates from BUS-480-A to GND-PLANT.
- BUS-480-A 480 V LOAD CENTER A -- CHG-125A: Solid LC-A labeled branch feeds CHG-125A from BUS-480-A.
- MCC-A1 SAFETY LOADS -- PUMP-RHR-A RHR A: Solid load conductor from MCC-A1 to PUMP-RHR-A.
- MCC-A1 SAFETY LOADS -- PUMP-CS-A CORE SPRAY: Solid load conductor from MCC-A1 to PUMP-CS-A.
- MCC-A2 VALVE/PUMP -- PUMP-CCW-A CCW A: Solid load conductor from MCC-A2 to PUMP-CCW-A.
- MCC-A2 VALVE/PUMP -- MOV-881A: Solid load conductor from MCC-A2 to MOV-881A.
- MCC-A2 VALVE/PUMP -- MOV-742A: Solid load conductor from MCC-A2 to MOV-742A.
- CHG-125A -- BAT-125A: Adjacent side-stack DC/sensing conductor between charger and battery.
- BAT-125A -- INV-120A: Adjacent side-stack DC/sensing conductor between battery and inverter.
- INV-120A -- PANEL-120A: Adjacent side-stack conductor between inverter and 120 V panel.
- PANEL-120A -- RPS-A DIV I: Adjacent side-stack conductor between panel and RPS-A.
- RPS-A DIV I -- RELAY-KA1: Dashed control conductor from RPS-A to relay KA1.
- RPS-A DIV I -- JB-A101: Dashed control route from RPS-A to junction box JB-A101.
- JB-A101 -- MOV-881A: Dashed MOV control conductor terminates at JB-A101 and MOV-881A.
- JB-A101 -- MOV-742A: Dashed MOV control conductor terminates at JB-A101 and MOV-742A.
- BUS-4160-B DIV II 4.16 kV ESF -- TR-480-B 4.16/0.48: BUS-4160-B vertical feeder drops to transformer TR-480-B.
- TR-480-B 4.16/0.48 -- CB-480-B: TR-480-B output feeds breaker CB-480-B.
- CB-480-B -- BUS-480-B 480 V LOAD CENTER B: CB-480-B lands on BUS-480-B with a junction dot.
- BUS-480-B 480 V LOAD CENTER B -- MCC-B1 SAFETY LOADS: BUS-480-B has a solid feeder to MCC-B1.
- BUS-480-B 480 V LOAD CENTER B -- MCC-B2 VALVE/PUMP: BUS-480-B has a solid feeder to MCC-B2.
- BUS-480-B 480 V LOAD CENTER B -- CHG-125B: Solid LC-B labeled branch feeds CHG-125B from BUS-480-B.
- MCC-B1 SAFETY LOADS -- PUMP-RHR-B RHR B: Solid load conductor from MCC-B1 to PUMP-RHR-B.
- MCC-B1 SAFETY LOADS -- PUMP-CS-B CORE SPRAY: Solid load conductor from MCC-B1 to PUMP-CS-B.
- MCC-B2 VALVE/PUMP -- PUMP-CCW-B CCW B: Solid load conductor from MCC-B2 to PUMP-CCW-B.
- MCC-B2 VALVE/PUMP -- MOV-881B: Solid load conductor from MCC-B2 to MOV-881B.
- MCC-B2 VALVE/PUMP -- MOV-742B: Solid load conductor from MCC-B2 to MOV-742B.
- CHG-125B -- BAT-125B: Adjacent side-stack DC/sensing conductor between charger and battery.
- BAT-125B -- INV-120B: Adjacent side-stack DC/sensing conductor between battery and inverter.
- INV-120B -- PANEL-120B: Adjacent side-stack conductor between inverter and 120 V panel.
- PANEL-120B -- RPS-B DIV II: Adjacent side-stack conductor between panel and RPS-B.
- RPS-B DIV II -- RELAY-KB1: Dashed control conductor from RPS-B to relay KB1.
- RPS-B DIV II -- JB-B101: Dashed control route from RPS-B to junction box JB-B101.
- JB-B101 -- MOV-881B: Dashed MOV control conductor terminates at JB-B101 and MOV-881B.
- JB-B101 -- MOV-742B: Dashed MOV control conductor terminates at JB-B101 and MOV-742B.
- ANN-CR01 -- REC-SOE01: Direct dashed control-room annunciation conductor between ANN-CR01 and REC-SOE01.

## Token Performance Tracking

Actual per-response usage objects and reasoning-token counts were not exposed through the available Codex/subagent tools. OPENAI_API_KEY was not available, so the OpenAI Responses input-token counting endpoint could not be called for planned payloads. The CSVs therefore contain low/expected/high estimates and mark actual usage unavailable.

- Estimated total tokens low: 124800
- Estimated total tokens expected: 162300
- Estimated total tokens high: 220100

Detailed token rows are in token_performance_tracking.csv and token_usage_estimates_by_call.csv. The misspelled compatibility file token_performance_traking.csv is also written.
