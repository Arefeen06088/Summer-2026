# Round 01 Diego Notes - Doc 18

Scope: high-recall extraction from doc 18 Input resources and derived inspection crops only. No GT, evaluator feedback, metric feedback, or prior document outputs used.

Matrix policy: accepted edges only are encoded as 1 in `round_01_diego_matrix.csv`; uncertain/plausible edges are documented below and left as 0 in the matrix. No anonymous WN/intermediate wire nodes are used.

## Proposed node list

Total matrix nodes: 201. This includes 188 prepared component labels, 11 visually printed logical buses, and 2 additional raw-image visible components missed by the prepared inventory (`DG-1B`, `CB-DG-B`).

1. `BB-SWYD-230` - logical_bus
2. `BUS-4160A` - logical_bus
3. `BUS-4160B` - logical_bus
4. `BUS-480A` - logical_bus
5. `BUS-480B` - logical_bus
6. `BUS-480C` - logical_bus
7. `BUS-480D` - logical_bus
8. `BUS-125A` - logical_bus
9. `BUS-125B` - logical_bus
10. `BUS-120A` - logical_bus
11. `BUS-120B` - logical_bus
12. `GRID-SWYD-1` - grid_source
13. `CB-GRID-A` - breaker
14. `GEN-MAIN-1` - generator
15. `CB-GEN-ISO` - breaker
16. `CB-SWYD-230` - breaker
17. `CB-GRID-B` - breaker
18. `GRID-SWYD-2` - grid_source
19. `TR-SAT-1A` - transformer
20. `TR-SAT-1B` - transformer
21. `TR-UAT-1A` - transformer
22. `TR-UAT-1B` - transformer
23. `CB-SAT-A` - breaker
24. `CB-UAT-A` - breaker
25. `CB-UAT-B` - breaker
26. `CB-SAT-B` - breaker
27. `CB-4160-TIE` - breaker
28. `DG-1A` - diesel_generator
29. `CB-DG-A` - breaker
30. `TB-RPS-A` - terminal_block
31. `GND-4160A` - ground
32. `GND-4160B` - ground
33. `PT-4160A` - pid_instrument
34. `FU-PT-A` - fuse
35. `FU-PT-B` - fuse
36. `XFRM-CTRL-A` - transformer_control
37. `SW-43A` - switch
38. `PT-4160B` - pid_instrument
39. `XFRM-CTRL-B` - transformer_control
40. `TB-RPS-B` - terminal_block
41. `SW-43B` - switch
42. `TR-480-B1` - transformer
43. `TR-480-C1` - transformer
44. `TR-480-D1` - transformer
45. `TR-480-A1` - transformer
46. `CB-480A-IN` - breaker
47. `CB-480B-IN` - breaker
48. `CB-480C-IN` - breaker
49. `CB-480D-IN` - breaker
50. `CB-B07` - breaker
51. `CB-A07` - breaker
52. `CB-C07` - breaker
53. `CB-D07` - breaker
54. `CB-A03` - breaker
55. `CB-B03` - breaker
56. `CB-C03` - breaker
57. `CB-D03` - breaker
58. `CB-A05` - breaker
59. `CB-B05` - breaker
60. `CB-C05` - breaker
61. `CB-D05` - breaker
62. `CB-A01` - breaker
63. `CB-B01` - breaker
64. `CB-C01` - breaker
65. `CB-D01` - breaker
66. `CB-B04` - breaker
67. `CB-A08` - breaker
68. `CB-C08` - breaker
69. `CB-A04` - breaker
70. `CB-C04` - breaker
71. `CB-D04` - breaker
72. `CB-B06` - breaker
73. `CB-B02` - breaker
74. `CB-C02` - breaker
75. `CB-D02` - breaker
76. `CB-A02` - breaker
77. `CB-A06` - breaker
78. `CB-C06` - breaker
79. `CB-D06` - breaker
80. `DS-D05` - disconnect_switch
81. `DS-A05` - disconnect_switch
82. `DS-B05` - disconnect_switch
83. `DS-C05` - disconnect_switch
84. `DS-A01` - disconnect_switch
85. `FS-A03` - pid_instrument
86. `FS-A07` - pid_instrument
87. `FS-B07` - pid_instrument
88. `DS-C01` - disconnect_switch
89. `FS-C07` - pid_instrument
90. `DS-D01` - disconnect_switch
91. `FS-D07` - pid_instrument
92. `FS-B03` - pid_instrument
93. `FS-C03` - pid_instrument
94. `FS-D03` - pid_instrument
95. `DS-B01` - disconnect_switch
96. `DS-A08` - disconnect_switch
97. `DS-C08` - disconnect_switch
98. `DS-A04` - disconnect_switch
99. `DS-B04` - disconnect_switch
100. `DS-C04` - disconnect_switch
101. `DS-D04` - disconnect_switch
102. `DS-B02` - disconnect_switch
103. `DS-A02` - disconnect_switch
104. `DS-C02` - disconnect_switch
105. `DS-D02` - disconnect_switch
106. `DS-A06` - disconnect_switch
107. `DS-B06` - disconnect_switch
108. `DS-C06` - disconnect_switch
109. `DS-D06` - disconnect_switch
110. `TB-A08` - terminal_block
111. `FU-A07` - fuse
112. `MS-C03` - motor_starter
113. `MS-C07` - motor_starter
114. `MS-A03` - motor_starter
115. `MS-B03` - motor_starter
116. `RY-A04` - relay
117. `RY-B04` - relay
118. `RY-B07` - relay
119. `RY-C04` - relay
120. `RY-D03` - relay
121. `TB-D07` - terminal_block
122. `MS-C05` - motor_starter
123. `MS-A01` - motor_starter
124. `MS-B01` - motor_starter
125. `MS-C01` - motor_starter
126. `MS-D01` - motor_starter
127. `FU-C08` - fuse
128. `MS-D04` - motor_starter
129. `MS-B02` - motor_starter
130. `MS-C02` - motor_starter
131. `MS-A02` - motor_starter
132. `MS-A06` - motor_starter
133. `MS-D06` - motor_starter
134. `MS-B06` - motor_starter
135. `MS-D02` - motor_starter
136. `CP-A05` - control_panel
137. `CP-D05` - control_panel
138. `CP-B05` - control_panel
139. `CP-C06` - control_panel
140. `HTR-PZR-A1` - heater_load
141. `FAN-RB-C1` - fan_motor
142. `FAN-FUEL-B1` - fan_motor
143. `FAN-RB-A1` - fan_motor
144. `SPARE-D7` - spare_component
145. `SUMP-PMP-C1` - physical_component
146. `PUMP-CCW-A1` - pump_motor
147. `PUMP-CCW-B1` - pump_motor
148. `PUMP-AFW-D1` - pump_motor
149. `PUMP-HPCI-C1` - pump_motor
150. `AIR-CMP-B1` - physical_component
151. `MOV-CCW-B21` - pid_valve
152. `VLV-CHG-B1` - valve
153. `MOV-RHR-C11` - pid_valve
154. `MOV-SI-D21` - pid_valve
155. `MOV-SI-A11` - pid_valve
156. `PUMP-SEAL-C1` - pump_motor
157. `PUMP-LUBE-D1` - pump_motor
158. `PNL-ESS-D5` - panel
159. `PNL-LTG-A1` - panel
160. `PUMP-AFW-A1` - pump_motor
161. `COMP-AIR-D1` - compressor
162. `PNL-IC-C7` - panel
163. `HTR-VENT-C2` - heater_load
164. `SPARE-A8` - spare_component
165. `PUMP-RHR-A1` - pump_motor
166. `PUMP-RHR-B1` - pump_motor
167. `PUMP-RCW-C1` - pump_motor
168. `FAN-CR-D1` - fan_motor
169. `MCC-AUX-B6` - motor_control_center
170. `JB-RPS-A` - junction_box
171. `JB-RPS-B` - junction_box
172. `CHG-125A` - battery_charger
173. `CHG-125B` - battery_charger
174. `CB-DC-A` - breaker
175. `REC-125B` - rectifier
176. `CB-DC-B` - breaker
177. `REC-125A` - rectifier
178. `RELAY-K101` - relay
179. `RELAY-K102` - relay
180. `RELAY-K201` - relay
181. `RELAY-K202` - relay
182. `RPS-PNL-A` - panel
183. `PLC-RPS-A` - plc
184. `RPS-PNL-B` - panel
185. `PLC-RPS-B` - plc
186. `PNL-ANN-A` - panel
187. `PNL-ANN-B` - panel
188. `RELAY-K103` - relay
189. `RELAY-K104` - relay
190. `RELAY-K203` - relay
191. `RELAY-K204` - relay
192. `INV-120A` - inverter
193. `UPS-120A` - ups
194. `INV-120B` - inverter
195. `UPS-120B` - ups
196. `BAT-125A` - battery
197. `BAT-125B` - battery
198. `GND-DC-A` - ground
199. `GND-DC-B` - ground
200. `DG-1B` - physical_component_extra_visible
201. `CB-DG-B` - physical_component_extra_visible

## Accepted edge list

Accepted edges encoded in matrix: 192.

| # | Node A | Node B | Kind | Confidence | Evidence |
|---:|---|---|---|---|---|
| 1 | `GRID-SWYD-1` | `CB-GRID-A` | solid power/DC | high | Top-left raw crop: solid line from GRID-SWYD-1 source symbol directly into CB-GRID-A. |
| 2 | `GRID-SWYD-2` | `CB-GRID-B` | solid power/DC | high | Top-left raw crop: solid line from GRID-SWYD-2 source symbol directly into CB-GRID-B. |
| 3 | `CB-GRID-A` | `CB-SWYD-230` | solid power/DC | medium-high | Top-left raw/components crop: CB-GRID-A output enters the common switchyard feeder at the CB-SWYD-230 labeled/detected section. |
| 4 | `CB-GRID-B` | `CB-SWYD-230` | solid power/DC | medium-high | Top-left raw/components crop: CB-GRID-B output joins the same switchyard feeder at the CB-SWYD-230 section. |
| 5 | `CB-SWYD-230` | `BB-SWYD-230` | solid power/DC | medium-high | Top-left raw crop: feeder dot/tap lands on heavy bus labeled BB-SWYD-230. |
| 6 | `BB-SWYD-230` | `TR-SAT-1A` | solid power/DC | high | Top-left/top-center raw crops: vertical solid feeder drops from BB-SWYD-230 into TR-SAT-1A. |
| 7 | `BB-SWYD-230` | `TR-SAT-1B` | solid power/DC | high | Top-center raw crop: vertical solid feeder drops from BB-SWYD-230 into TR-SAT-1B. |
| 8 | `BB-SWYD-230` | `CB-GEN-ISO` | solid power/DC | high | Top-center/right raw crops: CB-GEN-ISO sits on the generator path from the heavy BB-SWYD-230 bus. |
| 9 | `CB-GEN-ISO` | `GEN-MAIN-1` | solid power/DC | high | Top-right raw crop: solid generator lead runs from CB-GEN-ISO into GEN-MAIN-1. |
| 10 | `GEN-MAIN-1` | `TR-UAT-1A` | solid power/DC | high | Top-right raw crop: solid vertical lead from GEN-MAIN-1 to TR-UAT-1A. |
| 11 | `GEN-MAIN-1` | `TR-UAT-1B` | solid power/DC | high | Top-right raw crop: solid routed lead from GEN-MAIN-1 to TR-UAT-1B. |
| 12 | `TR-SAT-1A` | `CB-SAT-A` | solid power/DC | high | Top-left raw crop: TR-SAT-1A secondary lead drops directly into CB-SAT-A. |
| 13 | `CB-SAT-A` | `BUS-4160A` | solid power/DC | high | Top-left raw crop: CB-SAT-A output lands by dot on heavy bus labeled BUS-4160A. |
| 14 | `TR-SAT-1B` | `CB-SAT-B` | solid power/DC | high | Top-center raw crop: TR-SAT-1B secondary lead drops directly into CB-SAT-B. |
| 15 | `CB-SAT-B` | `BUS-4160B` | solid power/DC | high | Top-center raw crop: CB-SAT-B output lands by dot on heavy bus labeled BUS-4160B. |
| 16 | `TR-UAT-1A` | `CB-UAT-A` | solid power/DC | high | Top-right raw crop: TR-UAT-1A lead drops directly into CB-UAT-A. |
| 17 | `CB-UAT-A` | `BUS-4160B` | solid power/DC | medium-high | Top-right raw crop: CB-UAT-A output drops to the right-hand 4.16 kV bus span. |
| 18 | `TR-UAT-1B` | `CB-UAT-B` | solid power/DC | high | Top-right raw crop: TR-UAT-1B lead drops directly into CB-UAT-B. |
| 19 | `CB-UAT-B` | `BUS-4160B` | solid power/DC | medium-high | Top-right raw crop: CB-UAT-B output drops to the right-hand 4.16 kV bus span. |
| 20 | `DG-1A` | `CB-DG-A` | solid power/DC | high | Upper-left raw crop: solid feeder from DG-1A into CB-DG-A. |
| 21 | `CB-DG-A` | `BUS-4160A` | solid power/DC | high | Upper-left raw crop: CB-DG-A output rises to a dot on BUS-4160A. |
| 22 | `DG-1B` | `CB-DG-B` | solid power/DC | high | Upper-right raw crop: visible DG-1B source symbol connects by solid line to CB-DG-B. |
| 23 | `CB-DG-B` | `BUS-4160B` | solid power/DC | high | Upper-right raw crop: CB-DG-B output rises to the right-hand 4.16 kV bus. |
| 24 | `BUS-4160A` | `CB-4160-TIE` | solid power/DC | high | Top-center raw crop: CB-4160-TIE is drawn in-line between the left 4.16 kV bus and the right bus. |
| 25 | `CB-4160-TIE` | `BUS-4160B` | solid power/DC | high | Top-center raw crop: CB-4160-TIE output is dot-connected to BUS-4160B. |
| 26 | `BUS-4160A` | `GND-4160A` | solid power/DC | high | Upper-center raw crop: ground symbol GND-4160A is attached directly below BUS-4160A. |
| 27 | `BUS-4160B` | `GND-4160B` | solid power/DC | high | Upper-center raw crop: ground symbol GND-4160B is attached directly below BUS-4160B. |
| 28 | `BUS-4160A` | `PT-4160A` | dashed control/signal | medium-high | Upper A raw crop: dashed PT/control takeoff from BUS-4160A to PT-4160A is directly readable. |
| 29 | `PT-4160A` | `FU-PT-A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from PT-4160A to FU-PT-A. |
| 30 | `FU-PT-A` | `XFRM-CTRL-A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from FU-PT-A to XFRM-CTRL-A. |
| 31 | `XFRM-CTRL-A` | `TB-RPS-A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from XFRM-CTRL-A to TB-RPS-A. |
| 32 | `TB-RPS-A` | `SW-43A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from TB-RPS-A to SW-43A. |
| 33 | `BUS-4160B` | `PT-4160B` | dashed control/signal | medium-high | Upper B raw crop: dashed PT/control takeoff from BUS-4160B to PT-4160B is directly readable. |
| 34 | `PT-4160B` | `FU-PT-B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from PT-4160B to FU-PT-B. |
| 35 | `FU-PT-B` | `XFRM-CTRL-B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from FU-PT-B to XFRM-CTRL-B. |
| 36 | `XFRM-CTRL-B` | `TB-RPS-B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from XFRM-CTRL-B to TB-RPS-B. |
| 37 | `TB-RPS-B` | `SW-43B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from TB-RPS-B to SW-43B. |
| 38 | `BUS-4160A` | `TB-RPS-A` | solid power/DC | medium-high | Upper-left raw crop: vertical feeder at the BUS-4160A tap passes through/into TB-RPS-A before TR-480-A1. |
| 39 | `TB-RPS-A` | `TR-480-A1` | solid power/DC | medium-high | Upper-left raw crop: solid vertical feeder continues from TB-RPS-A into TR-480-A1. |
| 40 | `TR-480-A1` | `CB-480A-IN` | solid power/DC | high | Upper-left raw crop: TR-480-A1 secondary drops directly into CB-480A-IN. |
| 41 | `CB-480A-IN` | `BUS-480A` | solid power/DC | high | Upper-left raw crop: CB-480A-IN output lands on heavy bus labeled BUS-480A. |
| 42 | `BUS-4160A` | `TR-480-B1` | solid power/DC | high | Upper-left raw crop: vertical solid feeder from BUS-4160A drops into TR-480-B1. |
| 43 | `TR-480-B1` | `CB-480B-IN` | solid power/DC | high | Upper-left raw crop: TR-480-B1 secondary drops directly into CB-480B-IN. |
| 44 | `CB-480B-IN` | `BUS-480B` | solid power/DC | high | Upper-left raw crop: CB-480B-IN output lands on heavy bus labeled BUS-480B. |
| 45 | `BUS-4160B` | `TR-480-C1` | solid power/DC | high | Upper-center raw crop: vertical solid feeder from BUS-4160B drops into TR-480-C1. |
| 46 | `TR-480-C1` | `CB-480C-IN` | solid power/DC | high | Upper-center raw crop: TR-480-C1 secondary drops directly into CB-480C-IN. |
| 47 | `CB-480C-IN` | `BUS-480C` | solid power/DC | high | Upper-center raw crop: CB-480C-IN output lands on heavy bus labeled BUS-480C. |
| 48 | `BUS-4160B` | `TR-480-D1` | solid power/DC | high | Upper-right raw crop: vertical solid feeder from BUS-4160B drops into TR-480-D1. |
| 49 | `TR-480-D1` | `CB-480D-IN` | solid power/DC | high | Upper-right raw crop: TR-480-D1 secondary drops directly into CB-480D-IN. |
| 50 | `CB-480D-IN` | `BUS-480D` | solid power/DC | high | Upper-right raw crop: CB-480D-IN output lands on heavy bus labeled BUS-480D. |
| 51 | `BUS-480A` | `CB-A01` | solid power/DC | high | Middle/upper load-center crops: A01 vertical branch has a junction dot from BUS-480A to CB-A01. |
| 52 | `CB-A01` | `DS-A01` | solid power/DC | high | Middle load-center crop: A01 solid vertical chain continues directly from CB-A01 to DS-A01. |
| 53 | `DS-A01` | `MS-A01` | solid power/DC | high | Middle load-center crop: A01 solid vertical chain continues directly from DS-A01 to MS-A01. |
| 54 | `MS-A01` | `PUMP-CCW-A1` | solid power/DC | high | Middle load-center crop: A01 solid vertical chain continues directly from MS-A01 to PUMP-CCW-A1. |
| 55 | `BUS-480A` | `CB-A02` | solid power/DC | high | Middle/upper load-center crops: A02 vertical branch has a junction dot from BUS-480A to CB-A02. |
| 56 | `CB-A02` | `DS-A02` | solid power/DC | high | Middle load-center crop: A02 solid vertical chain continues directly from CB-A02 to DS-A02. |
| 57 | `DS-A02` | `MS-A02` | solid power/DC | high | Middle load-center crop: A02 solid vertical chain continues directly from DS-A02 to MS-A02. |
| 58 | `MS-A02` | `PUMP-RHR-A1` | solid power/DC | high | Middle load-center crop: A02 solid vertical chain continues directly from MS-A02 to PUMP-RHR-A1. |
| 59 | `BUS-480A` | `CB-A03` | solid power/DC | high | Middle/upper load-center crops: A03 vertical branch has a junction dot from BUS-480A to CB-A03. |
| 60 | `CB-A03` | `FS-A03` | solid power/DC | high | Middle load-center crop: A03 solid vertical chain continues directly from CB-A03 to FS-A03. |
| 61 | `FS-A03` | `MS-A03` | solid power/DC | high | Middle load-center crop: A03 solid vertical chain continues directly from FS-A03 to MS-A03. |
| 62 | `MS-A03` | `FAN-RB-A1` | solid power/DC | high | Middle load-center crop: A03 solid vertical chain continues directly from MS-A03 to FAN-RB-A1. |
| 63 | `BUS-480A` | `CB-A04` | solid power/DC | high | Middle/upper load-center crops: A04 vertical branch has a junction dot from BUS-480A to CB-A04. |
| 64 | `CB-A04` | `DS-A04` | solid power/DC | high | Middle load-center crop: A04 solid vertical chain continues directly from CB-A04 to DS-A04. |
| 65 | `DS-A04` | `RY-A04` | solid power/DC | high | Middle load-center crop: A04 solid vertical chain continues directly from DS-A04 to RY-A04. |
| 66 | `RY-A04` | `MOV-SI-A11` | solid power/DC | high | Middle load-center crop: A04 solid vertical chain continues directly from RY-A04 to MOV-SI-A11. |
| 67 | `BUS-480A` | `CB-A05` | solid power/DC | high | Middle/upper load-center crops: A05 vertical branch has a junction dot from BUS-480A to CB-A05. |
| 68 | `CB-A05` | `DS-A05` | solid power/DC | high | Middle load-center crop: A05 solid vertical chain continues directly from CB-A05 to DS-A05. |
| 69 | `DS-A05` | `CP-A05` | solid power/DC | high | Middle load-center crop: A05 solid vertical chain continues directly from DS-A05 to CP-A05. |
| 70 | `CP-A05` | `PNL-LTG-A1` | solid power/DC | high | Middle load-center crop: A05 solid vertical chain continues directly from CP-A05 to PNL-LTG-A1. |
| 71 | `BUS-480A` | `CB-A06` | solid power/DC | high | Middle/upper load-center crops: A06 vertical branch has a junction dot from BUS-480A to CB-A06. |
| 72 | `CB-A06` | `DS-A06` | solid power/DC | high | Middle load-center crop: A06 solid vertical chain continues directly from CB-A06 to DS-A06. |
| 73 | `DS-A06` | `MS-A06` | solid power/DC | high | Middle load-center crop: A06 solid vertical chain continues directly from DS-A06 to MS-A06. |
| 74 | `MS-A06` | `PUMP-AFW-A1` | solid power/DC | high | Middle load-center crop: A06 solid vertical chain continues directly from MS-A06 to PUMP-AFW-A1. |
| 75 | `BUS-480A` | `CB-A07` | solid power/DC | high | Middle/upper load-center crops: A07 vertical branch has a junction dot from BUS-480A to CB-A07. |
| 76 | `CB-A07` | `FS-A07` | solid power/DC | high | Middle load-center crop: A07 solid vertical chain continues directly from CB-A07 to FS-A07. |
| 77 | `FS-A07` | `FU-A07` | solid power/DC | high | Middle load-center crop: A07 solid vertical chain continues directly from FS-A07 to FU-A07. |
| 78 | `FU-A07` | `HTR-PZR-A1` | solid power/DC | high | Middle load-center crop: A07 solid vertical chain continues directly from FU-A07 to HTR-PZR-A1. |
| 79 | `BUS-480A` | `CB-A08` | solid power/DC | high | Middle/upper load-center crops: A08 vertical branch has a junction dot from BUS-480A to CB-A08. |
| 80 | `CB-A08` | `DS-A08` | solid power/DC | high | Middle load-center crop: A08 solid vertical chain continues directly from CB-A08 to DS-A08. |
| 81 | `DS-A08` | `TB-A08` | solid power/DC | high | Middle load-center crop: A08 solid vertical chain continues directly from DS-A08 to TB-A08. |
| 82 | `TB-A08` | `SPARE-A8` | solid power/DC | high | Middle load-center crop: A08 solid vertical chain continues directly from TB-A08 to SPARE-A8. |
| 83 | `BUS-480B` | `CB-B01` | solid power/DC | high | Middle/upper load-center crops: B01 vertical branch has a junction dot from BUS-480B to CB-B01. |
| 84 | `CB-B01` | `DS-B01` | solid power/DC | high | Middle load-center crop: B01 solid vertical chain continues directly from CB-B01 to DS-B01. |
| 85 | `DS-B01` | `MS-B01` | solid power/DC | high | Middle load-center crop: B01 solid vertical chain continues directly from DS-B01 to MS-B01. |
| 86 | `MS-B01` | `PUMP-CCW-B1` | solid power/DC | high | Middle load-center crop: B01 solid vertical chain continues directly from MS-B01 to PUMP-CCW-B1. |
| 87 | `BUS-480B` | `CB-B02` | solid power/DC | high | Middle/upper load-center crops: B02 vertical branch has a junction dot from BUS-480B to CB-B02. |
| 88 | `CB-B02` | `DS-B02` | solid power/DC | high | Middle load-center crop: B02 solid vertical chain continues directly from CB-B02 to DS-B02. |
| 89 | `DS-B02` | `MS-B02` | solid power/DC | high | Middle load-center crop: B02 solid vertical chain continues directly from DS-B02 to MS-B02. |
| 90 | `MS-B02` | `PUMP-RHR-B1` | solid power/DC | high | Middle load-center crop: B02 solid vertical chain continues directly from MS-B02 to PUMP-RHR-B1. |
| 91 | `BUS-480B` | `CB-B03` | solid power/DC | high | Middle/upper load-center crops: B03 vertical branch has a junction dot from BUS-480B to CB-B03. |
| 92 | `CB-B03` | `FS-B03` | solid power/DC | high | Middle load-center crop: B03 solid vertical chain continues directly from CB-B03 to FS-B03. |
| 93 | `FS-B03` | `MS-B03` | solid power/DC | high | Middle load-center crop: B03 solid vertical chain continues directly from FS-B03 to MS-B03. |
| 94 | `MS-B03` | `FAN-FUEL-B1` | solid power/DC | high | Middle load-center crop: B03 solid vertical chain continues directly from MS-B03 to FAN-FUEL-B1. |
| 95 | `BUS-480B` | `CB-B04` | solid power/DC | high | Middle/upper load-center crops: B04 vertical branch has a junction dot from BUS-480B to CB-B04. |
| 96 | `CB-B04` | `DS-B04` | solid power/DC | high | Middle load-center crop: B04 solid vertical chain continues directly from CB-B04 to DS-B04. |
| 97 | `DS-B04` | `RY-B04` | solid power/DC | high | Middle load-center crop: B04 solid vertical chain continues directly from DS-B04 to RY-B04. |
| 98 | `RY-B04` | `MOV-CCW-B21` | solid power/DC | high | Middle load-center crop: B04 solid vertical chain continues directly from RY-B04 to MOV-CCW-B21. |
| 99 | `BUS-480B` | `CB-B05` | solid power/DC | high | Middle/upper load-center crops: B05 vertical branch has a junction dot from BUS-480B to CB-B05. |
| 100 | `CB-B05` | `DS-B05` | solid power/DC | high | Middle load-center crop: B05 solid vertical chain continues directly from CB-B05 to DS-B05. |
| 101 | `DS-B05` | `CP-B05` | solid power/DC | high | Middle load-center crop: B05 solid vertical chain continues directly from DS-B05 to CP-B05. |
| 102 | `CP-B05` | `MCC-AUX-B6` | solid power/DC | high | Middle load-center crop: B05 solid vertical chain continues directly from CP-B05 to MCC-AUX-B6. |
| 103 | `BUS-480B` | `CB-B06` | solid power/DC | high | Middle/upper load-center crops: B06 vertical branch has a junction dot from BUS-480B to CB-B06. |
| 104 | `CB-B06` | `DS-B06` | solid power/DC | high | Middle load-center crop: B06 solid vertical chain continues directly from CB-B06 to DS-B06. |
| 105 | `DS-B06` | `MS-B06` | solid power/DC | high | Middle load-center crop: B06 solid vertical chain continues directly from DS-B06 to MS-B06. |
| 106 | `MS-B06` | `AIR-CMP-B1` | solid power/DC | high | Middle load-center crop: B06 solid vertical chain continues directly from MS-B06 to AIR-CMP-B1. |
| 107 | `BUS-480B` | `CB-B07` | solid power/DC | high | Middle/upper load-center crops: B07 vertical branch has a junction dot from BUS-480B to CB-B07. |
| 108 | `CB-B07` | `FS-B07` | solid power/DC | high | Middle load-center crop: B07 solid vertical chain continues directly from CB-B07 to FS-B07. |
| 109 | `FS-B07` | `RY-B07` | solid power/DC | high | Middle load-center crop: B07 solid vertical chain continues directly from FS-B07 to RY-B07. |
| 110 | `RY-B07` | `VLV-CHG-B1` | solid power/DC | high | Middle load-center crop: B07 solid vertical chain continues directly from RY-B07 to VLV-CHG-B1. |
| 111 | `BUS-480C` | `CB-C01` | solid power/DC | high | Middle/upper load-center crops: C01 vertical branch has a junction dot from BUS-480C to CB-C01. |
| 112 | `CB-C01` | `DS-C01` | solid power/DC | high | Middle load-center crop: C01 solid vertical chain continues directly from CB-C01 to DS-C01. |
| 113 | `DS-C01` | `MS-C01` | solid power/DC | high | Middle load-center crop: C01 solid vertical chain continues directly from DS-C01 to MS-C01. |
| 114 | `MS-C01` | `PUMP-HPCI-C1` | solid power/DC | high | Middle load-center crop: C01 solid vertical chain continues directly from MS-C01 to PUMP-HPCI-C1. |
| 115 | `BUS-480C` | `CB-C02` | solid power/DC | high | Middle/upper load-center crops: C02 vertical branch has a junction dot from BUS-480C to CB-C02. |
| 116 | `CB-C02` | `DS-C02` | solid power/DC | high | Middle load-center crop: C02 solid vertical chain continues directly from CB-C02 to DS-C02. |
| 117 | `DS-C02` | `MS-C02` | solid power/DC | high | Middle load-center crop: C02 solid vertical chain continues directly from DS-C02 to MS-C02. |
| 118 | `MS-C02` | `PUMP-RCW-C1` | solid power/DC | high | Middle load-center crop: C02 solid vertical chain continues directly from MS-C02 to PUMP-RCW-C1. |
| 119 | `BUS-480C` | `CB-C03` | solid power/DC | high | Middle/upper load-center crops: C03 vertical branch has a junction dot from BUS-480C to CB-C03. |
| 120 | `CB-C03` | `FS-C03` | solid power/DC | high | Middle load-center crop: C03 solid vertical chain continues directly from CB-C03 to FS-C03. |
| 121 | `FS-C03` | `MS-C03` | solid power/DC | high | Middle load-center crop: C03 solid vertical chain continues directly from FS-C03 to MS-C03. |
| 122 | `MS-C03` | `FAN-RB-C1` | solid power/DC | high | Middle load-center crop: C03 solid vertical chain continues directly from MS-C03 to FAN-RB-C1. |
| 123 | `BUS-480C` | `CB-C04` | solid power/DC | high | Middle/upper load-center crops: C04 vertical branch has a junction dot from BUS-480C to CB-C04. |
| 124 | `CB-C04` | `DS-C04` | solid power/DC | high | Middle load-center crop: C04 solid vertical chain continues directly from CB-C04 to DS-C04. |
| 125 | `DS-C04` | `RY-C04` | solid power/DC | high | Middle load-center crop: C04 solid vertical chain continues directly from DS-C04 to RY-C04. |
| 126 | `RY-C04` | `MOV-RHR-C11` | solid power/DC | high | Middle load-center crop: C04 solid vertical chain continues directly from RY-C04 to MOV-RHR-C11. |
| 127 | `BUS-480C` | `CB-C05` | solid power/DC | high | Middle/upper load-center crops: C05 vertical branch has a junction dot from BUS-480C to CB-C05. |
| 128 | `CB-C05` | `DS-C05` | solid power/DC | high | Middle load-center crop: C05 solid vertical chain continues directly from CB-C05 to DS-C05. |
| 129 | `DS-C05` | `MS-C05` | solid power/DC | high | Middle load-center crop: C05 solid vertical chain continues directly from DS-C05 to MS-C05. |
| 130 | `MS-C05` | `PUMP-SEAL-C1` | solid power/DC | high | Middle load-center crop: C05 solid vertical chain continues directly from MS-C05 to PUMP-SEAL-C1. |
| 131 | `BUS-480C` | `CB-C06` | solid power/DC | high | Middle/upper load-center crops: C06 vertical branch has a junction dot from BUS-480C to CB-C06. |
| 132 | `CB-C06` | `DS-C06` | solid power/DC | high | Middle load-center crop: C06 solid vertical chain continues directly from CB-C06 to DS-C06. |
| 133 | `DS-C06` | `CP-C06` | solid power/DC | high | Middle load-center crop: C06 solid vertical chain continues directly from DS-C06 to CP-C06. |
| 134 | `CP-C06` | `PNL-IC-C7` | solid power/DC | high | Middle load-center crop: C06 solid vertical chain continues directly from CP-C06 to PNL-IC-C7. |
| 135 | `BUS-480C` | `CB-C07` | solid power/DC | high | Middle/upper load-center crops: C07 vertical branch has a junction dot from BUS-480C to CB-C07. |
| 136 | `CB-C07` | `FS-C07` | solid power/DC | high | Middle load-center crop: C07 solid vertical chain continues directly from CB-C07 to FS-C07. |
| 137 | `FS-C07` | `MS-C07` | solid power/DC | high | Middle load-center crop: C07 solid vertical chain continues directly from FS-C07 to MS-C07. |
| 138 | `MS-C07` | `SUMP-PMP-C1` | solid power/DC | high | Middle load-center crop: C07 solid vertical chain continues directly from MS-C07 to SUMP-PMP-C1. |
| 139 | `BUS-480C` | `CB-C08` | solid power/DC | high | Middle/upper load-center crops: C08 vertical branch has a junction dot from BUS-480C to CB-C08. |
| 140 | `CB-C08` | `DS-C08` | solid power/DC | high | Middle load-center crop: C08 solid vertical chain continues directly from CB-C08 to DS-C08. |
| 141 | `DS-C08` | `FU-C08` | solid power/DC | high | Middle load-center crop: C08 solid vertical chain continues directly from DS-C08 to FU-C08. |
| 142 | `FU-C08` | `HTR-VENT-C2` | solid power/DC | high | Middle load-center crop: C08 solid vertical chain continues directly from FU-C08 to HTR-VENT-C2. |
| 143 | `BUS-480D` | `CB-D01` | solid power/DC | high | Middle/upper load-center crops: D01 vertical branch has a junction dot from BUS-480D to CB-D01. |
| 144 | `CB-D01` | `DS-D01` | solid power/DC | high | Middle load-center crop: D01 solid vertical chain continues directly from CB-D01 to DS-D01. |
| 145 | `DS-D01` | `MS-D01` | solid power/DC | high | Middle load-center crop: D01 solid vertical chain continues directly from DS-D01 to MS-D01. |
| 146 | `MS-D01` | `PUMP-AFW-D1` | solid power/DC | high | Middle load-center crop: D01 solid vertical chain continues directly from MS-D01 to PUMP-AFW-D1. |
| 147 | `BUS-480D` | `CB-D02` | solid power/DC | high | Middle/upper load-center crops: D02 vertical branch has a junction dot from BUS-480D to CB-D02. |
| 148 | `CB-D02` | `DS-D02` | solid power/DC | high | Middle load-center crop: D02 solid vertical chain continues directly from CB-D02 to DS-D02. |
| 149 | `DS-D02` | `MS-D02` | solid power/DC | high | Middle load-center crop: D02 solid vertical chain continues directly from DS-D02 to MS-D02. |
| 150 | `MS-D02` | `FAN-CR-D1` | solid power/DC | high | Middle load-center crop: D02 solid vertical chain continues directly from MS-D02 to FAN-CR-D1. |
| 151 | `BUS-480D` | `CB-D03` | solid power/DC | high | Middle/upper load-center crops: D03 vertical branch has a junction dot from BUS-480D to CB-D03. |
| 152 | `CB-D03` | `FS-D03` | solid power/DC | high | Middle load-center crop: D03 solid vertical chain continues directly from CB-D03 to FS-D03. |
| 153 | `FS-D03` | `RY-D03` | solid power/DC | high | Middle load-center crop: D03 solid vertical chain continues directly from FS-D03 to RY-D03. |
| 154 | `RY-D03` | `MOV-SI-D21` | solid power/DC | high | Middle load-center crop: D03 solid vertical chain continues directly from RY-D03 to MOV-SI-D21. |
| 155 | `BUS-480D` | `CB-D04` | solid power/DC | high | Middle/upper load-center crops: D04 vertical branch has a junction dot from BUS-480D to CB-D04. |
| 156 | `CB-D04` | `DS-D04` | solid power/DC | high | Middle load-center crop: D04 solid vertical chain continues directly from CB-D04 to DS-D04. |
| 157 | `DS-D04` | `MS-D04` | solid power/DC | high | Middle load-center crop: D04 solid vertical chain continues directly from DS-D04 to MS-D04. |
| 158 | `MS-D04` | `PUMP-LUBE-D1` | solid power/DC | high | Middle load-center crop: D04 solid vertical chain continues directly from MS-D04 to PUMP-LUBE-D1. |
| 159 | `BUS-480D` | `CB-D05` | solid power/DC | high | Middle/upper load-center crops: D05 vertical branch has a junction dot from BUS-480D to CB-D05. |
| 160 | `CB-D05` | `DS-D05` | solid power/DC | high | Middle load-center crop: D05 solid vertical chain continues directly from CB-D05 to DS-D05. |
| 161 | `DS-D05` | `CP-D05` | solid power/DC | high | Middle load-center crop: D05 solid vertical chain continues directly from DS-D05 to CP-D05. |
| 162 | `CP-D05` | `PNL-ESS-D5` | solid power/DC | high | Middle load-center crop: D05 solid vertical chain continues directly from CP-D05 to PNL-ESS-D5. |
| 163 | `BUS-480D` | `CB-D06` | solid power/DC | high | Middle/upper load-center crops: D06 vertical branch has a junction dot from BUS-480D to CB-D06. |
| 164 | `CB-D06` | `DS-D06` | solid power/DC | high | Middle load-center crop: D06 solid vertical chain continues directly from CB-D06 to DS-D06. |
| 165 | `DS-D06` | `MS-D06` | solid power/DC | high | Middle load-center crop: D06 solid vertical chain continues directly from DS-D06 to MS-D06. |
| 166 | `MS-D06` | `COMP-AIR-D1` | solid power/DC | high | Middle load-center crop: D06 solid vertical chain continues directly from MS-D06 to COMP-AIR-D1. |
| 167 | `BUS-480D` | `CB-D07` | solid power/DC | high | Middle/upper load-center crops: D07 vertical branch has a junction dot from BUS-480D to CB-D07. |
| 168 | `CB-D07` | `FS-D07` | solid power/DC | high | Middle load-center crop: D07 solid vertical chain continues directly from CB-D07 to FS-D07. |
| 169 | `FS-D07` | `TB-D07` | solid power/DC | high | Middle load-center crop: D07 solid vertical chain continues directly from FS-D07 to TB-D07. |
| 170 | `TB-D07` | `SPARE-D7` | solid power/DC | high | Middle load-center crop: D07 solid vertical chain continues directly from TB-D07 to SPARE-D7. |
| 171 | `BUS-480B` | `CHG-125A` | solid power/DC | medium-high | Left-half/full raw crop: long solid drop from the BUS-480B area feeds the Train A charger CHG-125A. |
| 172 | `CHG-125A` | `REC-125A` | solid power/DC | high | Lower-left raw crop: CHG-125A output line runs directly to REC-125A. |
| 173 | `REC-125A` | `CB-DC-A` | solid power/DC | high | Lower-left raw crop: REC-125A output line runs directly to CB-DC-A. |
| 174 | `CB-DC-A` | `BUS-125A` | solid power/DC | high | Lower-left raw crop: CB-DC-A vertical output lands on heavy BUS-125A rail. |
| 175 | `BUS-125A` | `BAT-125A` | solid power/DC | high | Lower-left raw crop: BAT-125A is directly tapped from BUS-125A. |
| 176 | `BUS-125A` | `GND-DC-A` | solid power/DC | high | Lower-left raw crop: GND-DC-A ground symbol is attached directly below BUS-125A. |
| 177 | `BUS-125A` | `INV-120A` | solid power/DC | medium-high | Lower-left raw crop: BUS-125A rail terminates at the DC side of INV-120A. |
| 178 | `INV-120A` | `UPS-120A` | dashed control/signal | medium-high | Lower-left raw crop: short dashed line runs directly from INV-120A to UPS-120A. |
| 179 | `UPS-120A` | `BUS-120A` | solid power/DC | high | Lower-left raw crop: UPS-120A vertical output lands on heavy BUS-120A rail. |
| 180 | `BUS-120A` | `RPS-PNL-A` | solid power/DC | high | Lower-left raw crop: RPS-PNL-A is directly tapped from BUS-120A. |
| 181 | `RPS-PNL-A` | `PLC-RPS-A` | dashed control/signal | medium-high | Lower-left raw crop: short dashed line runs directly from RPS-PNL-A to PLC-RPS-A. |
| 182 | `BUS-480C` | `CHG-125B` | solid power/DC | medium-high | Center/full raw crop: long solid drop from the BUS-480C area feeds the Train B charger CHG-125B. |
| 183 | `CHG-125B` | `REC-125B` | solid power/DC | high | Lower-center raw crop: CHG-125B output line runs directly to REC-125B. |
| 184 | `REC-125B` | `CB-DC-B` | solid power/DC | high | Lower-center raw crop: REC-125B output line runs directly to CB-DC-B. |
| 185 | `CB-DC-B` | `BUS-125B` | solid power/DC | high | Lower-center raw crop: CB-DC-B vertical output lands on heavy BUS-125B rail. |
| 186 | `BUS-125B` | `BAT-125B` | solid power/DC | high | Lower-center raw crop: BAT-125B is directly tapped from BUS-125B. |
| 187 | `BUS-125B` | `GND-DC-B` | solid power/DC | high | Lower-center raw crop: GND-DC-B ground symbol is attached directly below BUS-125B. |
| 188 | `BUS-125B` | `INV-120B` | solid power/DC | medium-high | Lower-center raw crop: BUS-125B rail terminates at the DC side of INV-120B. |
| 189 | `INV-120B` | `UPS-120B` | dashed control/signal | medium-high | Lower-center raw crop: short dashed line runs directly from INV-120B to UPS-120B. |
| 190 | `UPS-120B` | `BUS-120B` | solid power/DC | high | Lower-center raw crop: UPS-120B vertical output lands on heavy BUS-120B rail. |
| 191 | `BUS-120B` | `RPS-PNL-B` | solid power/DC | high | Lower-center/right raw crop: RPS-PNL-B is directly tapped from BUS-120B. |
| 192 | `RPS-PNL-B` | `PLC-RPS-B` | dashed control/signal | medium-high | Lower-right raw crop: short dashed line runs directly from RPS-PNL-B to PLC-RPS-B. |

## Uncertain/plausible edge list

These are visually plausible but not encoded in the accepted matrix because the line is dashed/control-routed, long, shared by multiple parallel legs, or has ambiguous endpoint assignment.

| # | Node A | Node B | Why uncertain |
|---:|---|---|---|
| 1 | `PLC-RPS-A` | `RELAY-K101` | Dashed output bundle from PLC-RPS-A appears to route into relay cluster, but multiple parallel dashed legs share a vertical riser. |
| 2 | `PLC-RPS-A` | `RELAY-K102` | Dashed path is plausible through the upper relay loop, but endpoint assignment is ambiguous near the shared relay-cluster routing. |
| 3 | `PLC-RPS-A` | `RELAY-K103` | Lower dashed branch from PLC-RPS-A reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 4 | `PLC-RPS-A` | `RELAY-K104` | Lower dashed branch from PLC-RPS-A reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 5 | `RELAY-K101` | `JB-RPS-A` | JB-RPS-A is printed adjacent to the relay cluster; dashed routing suggests a possible endpoint, but the raw crop does not show a clean isolated terminal connection. |
| 6 | `RELAY-K102` | `JB-RPS-A` | JB-RPS-A lies by the upper relay dashed route; path/endpoint is visually plausible but not clean enough for the accepted matrix. |
| 7 | `RELAY-K102` | `PNL-ANN-A` | Dashed route drops from the upper relay area toward PNL-ANN-A, but it shares bends and possible junctions with the relay loop. |
| 8 | `RELAY-K104` | `PNL-ANN-A` | Lower relay loop is routed near PNL-ANN-A; endpoint is plausible but not visually unambiguous. |
| 9 | `PLC-RPS-B` | `RELAY-K201` | Dashed output bundle from PLC-RPS-B appears to route into relay cluster, but multiple parallel dashed legs share a vertical riser. |
| 10 | `PLC-RPS-B` | `RELAY-K202` | Dashed path is plausible through the upper relay loop, but endpoint assignment is ambiguous near the shared relay-cluster routing. |
| 11 | `PLC-RPS-B` | `RELAY-K203` | Lower dashed branch from PLC-RPS-B reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 12 | `PLC-RPS-B` | `RELAY-K204` | Lower dashed branch from PLC-RPS-B reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 13 | `RELAY-K201` | `JB-RPS-B` | JB-RPS-B is printed adjacent to the upper relay route; possible dashed endpoint, but no clean direct connection is visible. |
| 14 | `RELAY-K202` | `JB-RPS-B` | JB-RPS-B lies by the upper relay dashed route; path/endpoint is visually plausible but not clean enough for the accepted matrix. |
| 15 | `RELAY-K202` | `PNL-ANN-B` | Dashed route drops from RELAY-K202 toward PNL-ANN-B, but it shares the relay-loop routing and is left uncertain. |
| 16 | `RELAY-K204` | `PNL-ANN-B` | Lower relay loop is routed near PNL-ANN-B; endpoint is plausible but not visually unambiguous. |

## Additional notes

- Heavy printed bars were treated as named logical bus nodes only where visually labeled: `BB-SWYD-230`, `BUS-4160A`, `BUS-4160B`, `BUS-480A`, `BUS-480B`, `BUS-480C`, `BUS-480D`, `BUS-125A`, `BUS-125B`, `BUS-120A`, and `BUS-120B`.
- Crossings without junction dots were not used to create connections.
- `JB-RPS-A`, `JB-RPS-B`, `PNL-ANN-A`, `PNL-ANN-B`, and several relay contacts are preserved as matrix nodes even where accepted connectivity is not reliable enough from the dashed cluster routing.
- Medium-high accepted edges include the readable `BUS-4160B` to `PT-4160B` dashed takeoff and the `CB-SWYD-230` to `BB-SWYD-230` switchyard feeder tap; neither should be extended beyond the named endpoints.
- The matrix is symmetric with diagonal 0 by construction; row and column labels are identical and in the same order.
