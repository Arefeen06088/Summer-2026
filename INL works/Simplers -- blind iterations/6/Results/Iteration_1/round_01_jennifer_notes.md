# Round 01 Jennifer Connectivity Notes

## Bus/Ground list
- AC buses retained: BUS-1A-4.16KV, BUS-1B-4.16KV, BUS-480A, BUS-480B, BUS-480E1A, BUS-480E1B.
- DC and vital AC buses retained: DC-BUS-125A, DC-BUS-125B, UPS-BUS-A, UPS-BUS-B.
- Ground retained: GND-1E, connected only to TR-1A by the visible grounding conductor.
- Context labels excluded: CLASS-1E-AC-DC, VITAL-POWER-TRAIN-A, and VITAL-POWER-TRAIN-B remain region labels only, not electrical nodes.
- Anonymous wire endpoints, terminal dots, cable callouts, FDR labels, CTRL labels, line tags, and WN-* nodes remain excluded.

## Accepted Changes
- Kept BUS-480A--CHGR-125A. The raw left-half crop shows solid cable 1A-480-7 tapping BUS-480A and landing on the CHGR-125A AC input.
- Kept BUS-480E1B--CHGR-125B. The raw right-half crop shows solid cable 1B-480-9 tied to the 480 ESS B/BUS-480E1B feeder and landing on the CHGR-125B AC input.
- Raised both charger source edges to high confidence because the solid feeder paths are visually supported by the named bus/cable routing.
- Kept CB-105--RELAY-K86A and RELAY-K86B--CB-106 as medium confidence. The dashed CTRL-86A/B paths have visible breaker control terminals and visible K86 relay ports, but they remain long control routes rather than direct solid power feeders.
- Did not add UPS-BUS-B--INST-RACK-1. INST-RACK-1 has a clear solid feeder from UPS-BUS-A only; no clear B-bus rack endpoint is visible.

## Removed / Rejected
- Removed no Diego topology edges.
- Rejected BUS-480B--BUS-480E1B: nearby lines cross or route over the bus area without a terminal dot showing a direct bus-to-bus junction.
- Rejected UPS-BUS-A--UPS-BUS-B: the two UPS buses are separate; the nearby horizontal routes do not show a direct bus tie.
- Rejected PANEL-RPS-A--PANEL-RPS-B: the panels communicate through JB-ESF-01, not by a direct panel-to-panel edge.
- Rejected relay-to-JB edges: the visible dashed relay paths go to their RPS panels or breaker control routes, not directly to JB-ESF-01.
- Rejected region-label edges involving CLASS-1E-AC-DC, VITAL-POWER-TRAIN-A, or VITAL-POWER-TRAIN-B.

## Uncertain / Plausible
- CB-105--RELAY-K86A remains medium confidence. It is visually plausible as the CTRL-86A interlock path from CB-105 to the K86A relay terminal, supported by the EDG lockout-control note, but the route is long and dashed.
- RELAY-K86B--CB-106 remains medium confidence. It is visually plausible as the CTRL-86B interlock path from CB-106 to the K86B relay terminal, supported by the EDG lockout-control note, but the route is long and dashed.

## Final Edge Table
| source | target | confidence | evidence |
|---|---|---|---|
| OFFSITE-A | TR-1A | high | Solid feeder from OFFSITE-A source terminals into TR-1A primary. |
| TR-1A | CB-101 | high | Solid feeder from TR-1A secondary/right terminal to drawout breaker CB-101. |
| TR-1A | GND-1E | high | Grounding conductor drops from TR-1A to the visible ground symbol labeled GND-1E. |
| CB-101 | BUS-1A-4.16KV | high | Solid 4160 V Feed A conductor exits CB-101 and lands on BUS-1A-4.16KV. |
| EDG-1A | CB-105 | high | Solid EDG-1A feeder runs from generator symbol to CB-105. |
| CB-105 | BUS-1A-4.16KV | high | Solid EDG A incoming feeder leaves CB-105 and taps BUS-1A-4.16KV. |
| BUS-1A-4.16KV | CB-TIE-1AB | high | BUS-1A-4.16KV right end connects by solid line to the normally-open tie breaker. |
| CB-TIE-1AB | BUS-1B-4.16KV | high | Tie breaker right terminal connects by solid line to BUS-1B-4.16KV. |
| BUS-1B-4.16KV | CB-102 | high | BUS-1B-4.16KV right-side solid feeder enters CB-102. |
| CB-102 | TR-1B | high | Solid feeder from CB-102 to TR-1B secondary/left terminal. |
| TR-1B | OFFSITE-B | high | Solid feeder from TR-1B primary/right terminal to OFFSITE-B source. |
| BUS-1B-4.16KV | CB-106 | high | Solid EDG B incoming feeder connects BUS-1B-4.16KV to CB-106. |
| CB-106 | EDG-1B | high | Solid feeder from CB-106 to EDG-1B generator symbol. |
| BUS-1A-4.16KV | TR-LC-1A | high | Vertical solid tap from BUS-1A-4.16KV feeds transformer TR-LC-1A. |
| TR-LC-1A | CB-201 | high | Short solid feeder from TR-LC-1A secondary to CB-201. |
| CB-201 | BUS-480A | high | Solid 480 V feeder from CB-201 lands on BUS-480A. |
| BUS-1A-4.16KV | TR-SAF-1A | high | Vertical solid tap from BUS-1A-4.16KV feeds transformer TR-SAF-1A. |
| TR-SAF-1A | CB-203 | high | Short solid feeder from TR-SAF-1A secondary to CB-203. |
| CB-203 | BUS-480E1A | high | Solid 480 V ESS A feeder from CB-203 lands on BUS-480E1A. |
| BUS-1B-4.16KV | TR-LC-1B | high | Vertical solid tap from BUS-1B-4.16KV feeds transformer TR-LC-1B. |
| TR-LC-1B | CB-202 | high | Short solid feeder from TR-LC-1B secondary to CB-202. |
| CB-202 | BUS-480B | high | Solid 480 V feeder from CB-202 lands on BUS-480B. |
| BUS-1B-4.16KV | TR-SAF-1B | high | Vertical solid tap from BUS-1B-4.16KV feeds transformer TR-SAF-1B. |
| TR-SAF-1B | CB-204 | high | Short solid feeder from TR-SAF-1B secondary to CB-204. |
| CB-204 | BUS-480E1B | high | Solid 480 V ESS B feeder from CB-204 lands on BUS-480E1B. |
| BUS-480A | MCC-1A | high | Direct solid vertical tap from BUS-480A to MCC-1A. |
| BUS-480A | MCC-1C | high | Direct solid vertical tap from BUS-480A to MCC-1C. |
| BUS-480A | CHGR-125A | high | Solid cable 1A-480-7 visibly taps BUS-480A and lands on the CHGR-125A AC input. |
| MCC-1A | PUMP-CCW-103A | high | Solid feeder from MCC-1A bottom terminal to PUMP-CCW-103A. |
| MCC-1C | FAN-CRHV-104A | high | Solid feeder from MCC-1C bottom terminal to FAN-CRHV-104A. |
| BUS-480E1A | MCC-ESS-A | high | Direct solid vertical tap from BUS-480E1A to MCC-ESS-A. |
| MCC-ESS-A | PUMP-SI-101A | high | Left solid feeder from MCC-ESS-A to PUMP-SI-101A. |
| MCC-ESS-A | PUMP-RHR-102A | high | Center solid feeder from MCC-ESS-A to PUMP-RHR-102A. |
| MCC-ESS-A | MOV-1201A | high | Right solid feeder from MCC-ESS-A to MOV-1201A. |
| BUS-480B | MCC-1B | high | Direct solid vertical tap from BUS-480B to MCC-1B. |
| BUS-480B | MCC-1D | high | Direct solid vertical tap from BUS-480B to MCC-1D. |
| MCC-1B | PUMP-CCW-103B | high | Solid feeder from MCC-1B bottom terminal to PUMP-CCW-103B. |
| MCC-1D | FAN-CRHV-104B | high | Solid feeder from MCC-1D bottom terminal to FAN-CRHV-104B. |
| BUS-480E1B | MCC-ESS-B | high | Direct solid vertical tap from BUS-480E1B to MCC-ESS-B. |
| BUS-480E1B | CHGR-125B | high | Solid cable 1B-480-9 visibly tees from the 480 ESS B/BUS-480E1B feeder and lands on the CHGR-125B AC input. |
| MCC-ESS-B | PUMP-SI-101B | high | Left solid feeder from MCC-ESS-B to PUMP-SI-101B. |
| MCC-ESS-B | PUMP-RHR-102B | high | Center solid feeder from MCC-ESS-B to PUMP-RHR-102B. |
| MCC-ESS-B | MOV-1201B | high | Right solid feeder from MCC-ESS-B to MOV-1201B. |
| CHGR-125A | DC-BUS-125A | high | Solid DC output from CHGR-125A right terminal to DC-BUS-125A. |
| BAT-125A | DC-BUS-125A | high | Solid battery feeder from BAT-125A to DC-BUS-125A. |
| DC-BUS-125A | INV-120A | high | Solid feeder from DC-BUS-125A to INV-120A. |
| INV-120A | UPS-BUS-A | high | Solid 125 VDC/120 VAC inverter output from INV-120A to UPS-BUS-A. |
| UPS-BUS-A | PANEL-RPS-A | high | Solid vital 120 VAC feeder from UPS-BUS-A up to PANEL-RPS-A. |
| UPS-BUS-A | INST-RACK-1 | high | Solid feeder exits UPS-BUS-A right side and drops into INST-RACK-1. |
| CHGR-125B | DC-BUS-125B | high | Solid DC output from CHGR-125B right terminal to DC-BUS-125B. |
| BAT-125B | DC-BUS-125B | high | Solid battery feeder from BAT-125B to DC-BUS-125B. |
| DC-BUS-125B | INV-120B | high | Solid feeder from DC-BUS-125B to INV-120B. |
| INV-120B | UPS-BUS-B | high | Solid 125 VDC/120 VAC inverter output from INV-120B to UPS-BUS-B. |
| UPS-BUS-B | PANEL-RPS-B | high | Solid vital 120 VAC feeder from UPS-BUS-B up to PANEL-RPS-B. |
| CB-105 | RELAY-K86A | medium | Dashed CTRL-86A route leaves CB-105 bottom control terminal and runs to the visible K86A relay terminal/port. |
| RELAY-K86A | PANEL-RPS-A | high | Dashed vertical interlock path drops from RELAY-K86A to the left side of PANEL-RPS-A. |
| PANEL-RPS-A | JB-ESF-01 | high | Dashed interlock cable leaves PANEL-RPS-A top/right and lands on JB-ESF-01 left port. |
| JB-ESF-01 | PANEL-RPS-B | high | Dashed interlock cable leaves JB-ESF-01 right port and lands on PANEL-RPS-B top/left. |
| PANEL-RPS-B | RELAY-K86B | high | Dashed vertical interlock path connects PANEL-RPS-B right side to RELAY-K86B. |
| RELAY-K86B | CB-106 | medium | Dashed CTRL-86B route leaves CB-106 bottom control terminal and runs to the visible K86B relay terminal/port. |