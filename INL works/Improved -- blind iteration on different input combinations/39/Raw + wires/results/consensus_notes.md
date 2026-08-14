# Document 39 Consensus Notes

Final graph saturated after Diego R1 -> Jennifer R1 -> Diego R2. Jennifer final confirmation was requested as R2; the saved final matrix follows the saturated Jennifer R1 / Diego R2 graph.

- Final node count: 54
- Final edge count: 56
- Matrix type: undirected, symmetric, diagonal zero.
- Source restriction: only files in Raw + wires were used.
- OCR restriction: no off-the-shelf OCR was used.

## Precision Decisions

- `CONTROL-ROOM-ANNUNCIATION` was treated as a route/area label, not a component node.
- `ANN-CR01 -- REC-SOE01` was retained as the only direct annunciation edge.
- `JB-A101` and `JB-B101` were retained only for RPS/MOV control circuits; no JB-to-annunciation edge was retained.
- `GND-PLANT` was retained only as connected to `BUS-480-A/LC-A`.
- `LC-A` and `LC-B` were merged into the corresponding 480 V bus/load-center nodes.
- Direct RPS-to-MOV edges were omitted; visible/control-schedule evidence supports RPS-to-JB and JB-to-MOV.

## Final Edges

- OFFSITE-230KV-A -- DS-230A
- DS-230A -- TR-1A
- TR-1A -- CB-1A
- CB-1A -- BUS-4160-A
- EDG-1A -- CB-DG-A
- CB-DG-A -- BUS-4160-A
- BUS-4160-A -- RELAY-UV-A
- BUS-4160-A -- TR-480-A
- TR-480-A -- CB-480-A
- CB-480-A -- BUS-480-A/LC-A
- BUS-480-A/LC-A -- GND-PLANT
- BUS-480-A/LC-A -- CHG-125A
- CHG-125A -- BAT-125A
- BAT-125A -- INV-120A
- INV-120A -- PANEL-120A
- PANEL-120A -- RPS-A
- RPS-A -- RELAY-KA1
- RPS-A -- JB-A101
- BUS-480-A/LC-A -- MCC-A1
- MCC-A1 -- PUMP-RHR-A
- MCC-A1 -- PUMP-CS-A
- BUS-480-A/LC-A -- MCC-A2
- MCC-A2 -- PUMP-CCW-A
- MCC-A2 -- MOV-881A
- MCC-A2 -- MOV-742A
- JB-A101 -- MOV-881A
- JB-A101 -- MOV-742A
- ANN-CR01 -- REC-SOE01
- BUS-4160-A -- CB-TIE-AB
- CB-TIE-AB -- BUS-4160-B
- OFFSITE-230KV-B -- DS-230B
- DS-230B -- TR-1B
- TR-1B -- CB-1B
- CB-1B -- BUS-4160-B
- EDG-1B -- CB-DG-B
- CB-DG-B -- BUS-4160-B
- BUS-4160-B -- RELAY-UV-B
- BUS-4160-B -- TR-480-B
- TR-480-B -- CB-480-B
- CB-480-B -- BUS-480-B/LC-B
- BUS-480-B/LC-B -- CHG-125B
- CHG-125B -- BAT-125B
- BAT-125B -- INV-120B
- INV-120B -- PANEL-120B
- PANEL-120B -- RPS-B
- RPS-B -- RELAY-KB1
- RPS-B -- JB-B101
- BUS-480-B/LC-B -- MCC-B1
- MCC-B1 -- PUMP-RHR-B
- MCC-B1 -- PUMP-CS-B
- BUS-480-B/LC-B -- MCC-B2
- MCC-B2 -- PUMP-CCW-B
- MCC-B2 -- MOV-881B
- MCC-B2 -- MOV-742B
- JB-B101 -- MOV-881B
- JB-B101 -- MOV-742B
