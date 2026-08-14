# Jennifer R2

- Node count: 55
- Edge count: 56
- Note: Final precision confirmation; no additional changes after Diego R2.
- Source restriction: Raw + wires only; no GT/GT-derived files used.
- OCR restriction: no off-the-shelf OCR used.
- Matrix type: undirected, symmetric, diagonal zero.

## Nodes

01. DG-21A
02. UAT-2A
03. DS-21A
04. ATS-21A
05. SWGR-21A
06. TIE-BKR-21AB
07. SWGR-21B
08. SAT-2B
09. DS-21B
10. ATS-21B
11. DG-21B
12. CB-21A1
13. TR-21A
14. MCC-21A
15. VT-21A
16. CT-21A
17. CB-MPA1
18. PUMP-SI21A
19. PUMP-CCW21A
20. FAN-RB21A
21. MOV-HV211A
22. MOV-RWST21A
23. XFMR-CPT21A
24. AC-PNL-120A
25. RECT-21A
26. DC-BUS-21A
27. BAT-21A
28. INV-21A
29. LOCA-SIG-A
30. JB-21A
31. RPS-PNL-A
32. RELAY-K21A
33. RELAY-86A
34. CB-21B1
35. TR-21B
36. MCC-21B
37. VT-21B
38. CT-21B
39. CB-MPB1
40. PUMP-SI21B
41. PUMP-CCW21B
42. FAN-RB21B
43. MOV-HV211B
44. MOV-RWST21B
45. XFMR-CPT21B
46. AC-PNL-120B
47. RECT-21B
48. DC-BUS-21B
49. BAT-21B
50. INV-21B
51. LOCA-SIG-B
52. JB-21B
53. RPS-PNL-B
54. RELAY-K21B
55. RELAY-86B

## Edges

- DG-21A -- ATS-21A (high): solid feeder from DG into ATS source terminal
- UAT-2A -- DS-21A (high): solid vertical feeder between UAT and disconnect
- DS-21A -- ATS-21A (high): solid feeder from disconnect into ATS terminal
- ATS-21A -- SWGR-21A (high): solid ATS drop lands on SWGR bus junction dot
- SWGR-21A -- TIE-BKR-21AB (high): SWGR bus enters tie breaker left terminal
- TIE-BKR-21AB -- SWGR-21B (high): tie breaker right terminal continues as SWGR bus
- SWGR-21A -- CB-21A1 (high): solid bus tap with junction dot drops to breaker
- CB-21A1 -- TR-21A (high): solid feeder from breaker to transformer
- TR-21A -- MCC-21A (high): solid feeder from transformer lands on MCC bus dot
- SAT-2B -- DS-21B (high): solid vertical feeder between SAT and disconnect
- DS-21B -- ATS-21B (high): solid feeder from disconnect into ATS terminal
- DG-21B -- ATS-21B (high): solid feeder from DG into ATS source terminal
- ATS-21B -- SWGR-21B (high): solid ATS drop lands on SWGR bus junction dot
- SWGR-21B -- CB-21B1 (high): solid bus tap with junction dot drops to breaker
- CB-21B1 -- TR-21B (high): solid feeder from breaker to transformer
- TR-21B -- MCC-21B (high): solid feeder from transformer lands on MCC bus dot
- MCC-21A -- CB-MPA1 (high): solid MCC feeder enters breaker
- CB-MPA1 -- PUMP-SI21A (high): solid feeder exits breaker to pump
- MCC-21A -- PUMP-CCW21A (high): solid MCC branch lands on pump
- MCC-21A -- FAN-RB21A (high): solid MCC branch lands on fan
- MCC-21A -- MOV-HV211A (high): solid MCC branch lands on MOV
- MCC-21A -- MOV-RWST21A (high): solid MCC branch lands on MOV
- MCC-21A -- XFMR-CPT21A (high): solid MCC branch feeds CPT transformer
- XFMR-CPT21A -- AC-PNL-120A (high): solid feeder from CPT transformer to AC panel
- AC-PNL-120A -- RECT-21A (high): solid feeder from AC panel to rectifier
- RECT-21A -- DC-BUS-21A (high): solid rectifier output joins 125 VDC bus at dot
- DC-BUS-21A -- BAT-21A (high): solid battery lead joins DC bus at dot
- DC-BUS-21A -- INV-21A (high): solid inverter lead joins DC bus at dot
- VT-21A -- RPS-PNL-A (high): short-dash Voltage Sig A path lands on RPS top terminal
- CT-21A -- RPS-PNL-A (high): short-dash CT signal lands on RPS top terminal
- LOCA-SIG-A -- JB-21A (high): dashed logic line terminates at LOCA and JB
- JB-21A -- RPS-PNL-A (high): dashed logic line from JB lands on RPS terminal
- RPS-PNL-A -- RELAY-K21A (high): dashed control line connects RPS to K relay
- RELAY-K21A -- RELAY-86A (high): dashed control line connects K relay to 86 relay
- RELAY-86A -- CB-MPA1 (high): dash-dot trip control route lands at breaker trip MPA1
- RPS-PNL-A -- INV-21A (high): dashed control line connects RPS to inverter terminal
- MCC-21B -- XFMR-CPT21B (high): solid MCC branch feeds CPT transformer
- XFMR-CPT21B -- AC-PNL-120B (high): solid feeder from CPT transformer to AC panel
- AC-PNL-120B -- RECT-21B (high): solid feeder from AC panel to rectifier
- RECT-21B -- DC-BUS-21B (high): solid rectifier output joins 125 VDC bus at dot
- DC-BUS-21B -- BAT-21B (high): solid battery lead joins DC bus at dot
- DC-BUS-21B -- INV-21B (high): solid inverter lead joins DC bus at dot
- MCC-21B -- CB-MPB1 (high): solid MCC feeder enters breaker
- CB-MPB1 -- PUMP-SI21B (high): solid feeder exits breaker to pump
- MCC-21B -- PUMP-CCW21B (high): solid MCC branch lands on pump
- MCC-21B -- FAN-RB21B (high): solid MCC branch lands on fan
- MCC-21B -- MOV-HV211B (high): solid MCC branch lands on MOV
- MCC-21B -- MOV-RWST21B (high): solid MCC branch lands on MOV
- VT-21B -- RPS-PNL-B (high): short-dash Voltage Sig B path lands on RPS top terminal
- CT-21B -- RPS-PNL-B (high): short-dash CT signal lands on RPS top terminal
- LOCA-SIG-B -- JB-21B (high): dashed logic line terminates at LOCA and JB
- JB-21B -- RPS-PNL-B (high): dashed logic line from JB lands on RPS terminal
- RPS-PNL-B -- RELAY-K21B (high): dashed control line connects RPS to K relay
- RELAY-K21B -- RELAY-86B (high): dashed control line connects K relay to 86 relay
- RELAY-86B -- CB-MPB1 (high): dash-dot trip control route lands at breaker trip MPB1
- RPS-PNL-B -- INV-21B (high): dashed control line connects RPS to inverter terminal
