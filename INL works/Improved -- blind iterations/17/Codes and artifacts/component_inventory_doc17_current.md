# Doc 17 Input-Only Component Inventory

This inventory is derived from `Input resources` and raw visual review only. It is not ground truth.

Inventory rows: 200
OCR/component CSV rows: 186
Raw-visual additions: 14

## Component Type Counts

- annunciator: 2
- battery: 2
- battery_charger: 2
- breaker: 43
- bus: 8
- current_transformer: 2
- diesel_generator: 2
- disconnect_switch: 12
- fan_motor: 2
- fuse: 12
- generator: 1
- ground: 12
- heater_load: 2
- instrument: 2
- inverter: 2
- junction_box: 2
- meter: 4
- motor: 2
- panel: 6
- physical_component: 24
- pid_instrument: 8
- pid_valve: 4
- pump_motor: 10
- relay: 14
- terminal_block: 12
- transformer: 8

## Node Kind Counts

- logical_node: 8
- physical_component: 192

## Ordered Nodes

1. `GEN-001` - generator; physical_component; centroid=(2137.5, 347.5); source=raw_visual_review
2. `DG-1A` - diesel_generator; physical_component; centroid=(1570.0, 430.0); source=component_visual_ocr_labels.csv
3. `DG-1B` - diesel_generator; physical_component; centroid=(3390.0, 430.0); source=component_visual_ocr_labels.csv
4. `SAT-1A` - transformer; physical_component; centroid=(422.5, 467.5); source=component_visual_ocr_labels.csv
5. `UAT-1A` - transformer; physical_component; centroid=(797.5, 467.5); source=component_visual_ocr_labels.csv
6. `UAT-1B` - transformer; physical_component; centroid=(2805.0, 467.5); source=component_visual_ocr_labels.csv
7. `SAT-1B` - transformer; physical_component; centroid=(3810.0, 472.5); source=component_visual_ocr_labels.csv
8. `CB-SAT-1A` - breaker; physical_component; centroid=(431.5, 620.0); source=component_visual_ocr_labels.csv
9. `CB-UAT-1A` - breaker; physical_component; centroid=(807.5, 620.0); source=component_visual_ocr_labels.csv
10. `CB-DG-1A` - breaker; physical_component; centroid=(1572.5, 620.0); source=component_visual_ocr_labels.csv
11. `CB-UAT-1B` - breaker; physical_component; centroid=(2807.5, 622.5); source=component_visual_ocr_labels.csv
12. `CB-DG-1B` - breaker; physical_component; centroid=(3401.5, 622.5); source=component_visual_ocr_labels.csv
13. `CB-SAT-1B` - breaker; physical_component; centroid=(3822.5, 622.5); source=component_visual_ocr_labels.csv
14. `BUS-4160-A` - bus; logical_node; centroid=(1125.0, 705.0); source=raw_visual_review
15. `BUS-4160-B` - bus; logical_node; centroid=(3135.0, 705.0); source=raw_visual_review
16. `CB-TIE-4AB` - breaker; physical_component; centroid=(2092.5, 720.0); source=component_visual_ocr_labels.csv
17. `PT-4160-A` - pid_instrument; physical_component; centroid=(974.0, 795.0); source=component_visual_ocr_labels.csv
18. `PT-4160-B` - pid_instrument; physical_component; centroid=(2974.0, 795.0); source=component_visual_ocr_labels.csv
19. `CB-TR-B2` - breaker; physical_component; centroid=(3455.0, 852.0); source=component_visual_ocr_labels.csv
20. `CB-TR-A1` - breaker; physical_component; centroid=(655.5, 853.0); source=component_visual_ocr_labels.csv
21. `CB-TR-B1` - breaker; physical_component; centroid=(2656.0, 853.0); source=component_visual_ocr_labels.csv
22. `CB-TR-A2` - breaker; physical_component; centroid=(1455.0, 855.0); source=component_visual_ocr_labels.csv
23. `TR-LC-A1` - transformer; physical_component; centroid=(657.5, 940.0); source=component_visual_ocr_labels.csv
24. `TR-LC-A2` - transformer; physical_component; centroid=(1457.5, 940.0); source=component_visual_ocr_labels.csv
25. `TR-LC-B1` - transformer; physical_component; centroid=(2656.5, 940.0); source=component_visual_ocr_labels.csv
26. `TR-LC-B2` - transformer; physical_component; centroid=(3456.5, 940.0); source=component_visual_ocr_labels.csv
27. `CB-480-A1` - breaker; physical_component; centroid=(660.0, 1022.5); source=component_visual_ocr_labels.csv
28. `CB-480-A2` - breaker; physical_component; centroid=(1460.0, 1022.5); source=component_visual_ocr_labels.csv
29. `CB-480-B1` - breaker; physical_component; centroid=(2660.0, 1022.5); source=component_visual_ocr_labels.csv
30. `CB-480-B2` - breaker; physical_component; centroid=(3460.0, 1022.5); source=component_visual_ocr_labels.csv
31. `AM-480-A` - meter; physical_component; centroid=(1797.5, 1047.5); source=raw_visual_review
32. `VM-480-A` - meter; physical_component; centroid=(1947.5, 1047.5); source=raw_visual_review
33. `AM-480-B` - meter; physical_component; centroid=(3797.5, 1047.5); source=raw_visual_review
34. `VM-480-B` - meter; physical_component; centroid=(3947.5, 1047.5); source=raw_visual_review
35. `CT-4B8-A1` - current_transformer; physical_component; centroid=(1520.5, 1053.5); source=component_visual_ocr_labels.csv
36. `CT-4B8-B1` - current_transformer; physical_component; centroid=(3520.5, 1053.5); source=component_visual_ocr_labels.csv
37. `GND-SMGR-A` - ground; physical_component; centroid=(1876.5, 1140.0); source=component_visual_ocr_labels.csv
38. `GND-SMGR-B` - ground; physical_component; centroid=(3960.0, 1140.0); source=component_visual_ocr_labels.csv
39. `CB-TIE-480AB` - breaker; physical_component; centroid=(2100.0, 1150.0); source=component_visual_ocr_labels.csv
40. `BUS-480-A` - bus; logical_node; centroid=(1125.0, 1152.5); source=raw_visual_review
41. `BUS-480-B` - bus; logical_node; centroid=(3135.0, 1152.5); source=raw_visual_review
42. `CB-101A` - breaker; physical_component; centroid=(365.0, 1265.0); source=component_visual_ocr_labels.csv
43. `CB-102A` - breaker; physical_component; centroid=(495.0, 1265.0); source=component_visual_ocr_labels.csv
44. `CB-103A` - breaker; physical_component; centroid=(625.0, 1265.0); source=component_visual_ocr_labels.csv
45. `CB-104A` - breaker; physical_component; centroid=(755.0, 1265.0); source=component_visual_ocr_labels.csv
46. `CB-105A` - breaker; physical_component; centroid=(885.0, 1265.0); source=component_visual_ocr_labels.csv
47. `CB-106A` - breaker; physical_component; centroid=(1015.0, 1265.0); source=component_visual_ocr_labels.csv
48. `CB-107A` - breaker; physical_component; centroid=(1145.0, 1265.0); source=component_visual_ocr_labels.csv
49. `CB-108A` - breaker; physical_component; centroid=(1275.0, 1265.0); source=component_visual_ocr_labels.csv
50. `CB-109A` - breaker; physical_component; centroid=(1405.0, 1265.0); source=component_visual_ocr_labels.csv
51. `CB-110A` - breaker; physical_component; centroid=(1535.0, 1265.0); source=component_visual_ocr_labels.csv
52. `CB-111A` - breaker; physical_component; centroid=(1665.0, 1265.0); source=component_visual_ocr_labels.csv
53. `CB-112A` - breaker; physical_component; centroid=(1795.0, 1265.0); source=component_visual_ocr_labels.csv
54. `CB-201B` - breaker; physical_component; centroid=(2365.0, 1265.0); source=component_visual_ocr_labels.csv
55. `CB-202B` - breaker; physical_component; centroid=(2495.0, 1265.0); source=component_visual_ocr_labels.csv
56. `CB-203B` - breaker; physical_component; centroid=(2625.0, 1265.0); source=component_visual_ocr_labels.csv
57. `CB-204B` - breaker; physical_component; centroid=(2755.0, 1265.0); source=component_visual_ocr_labels.csv
58. `CB-205B` - breaker; physical_component; centroid=(2885.0, 1265.0); source=component_visual_ocr_labels.csv
59. `CB-206B` - breaker; physical_component; centroid=(3015.0, 1265.0); source=component_visual_ocr_labels.csv
60. `CB-207B` - breaker; physical_component; centroid=(3145.0, 1265.0); source=component_visual_ocr_labels.csv
61. `CB-208B` - breaker; physical_component; centroid=(3275.0, 1265.0); source=component_visual_ocr_labels.csv
62. `CB-209B` - breaker; physical_component; centroid=(3405.0, 1265.0); source=component_visual_ocr_labels.csv
63. `CB-210B` - breaker; physical_component; centroid=(3535.0, 1265.0); source=component_visual_ocr_labels.csv
64. `CB-211B` - breaker; physical_component; centroid=(3665.0, 1265.0); source=component_visual_ocr_labels.csv
65. `CB-212B` - breaker; physical_component; centroid=(3795.0, 1265.0); source=component_visual_ocr_labels.csv
66. `DS-101A` - disconnect_switch; physical_component; centroid=(365.0, 1353.0); source=component_visual_ocr_labels.csv
67. `FU-102A` - fuse; physical_component; centroid=(495.0, 1353.0); source=component_visual_ocr_labels.csv
68. `DS-103A` - disconnect_switch; physical_component; centroid=(625.0, 1353.0); source=component_visual_ocr_labels.csv
69. `FU-104A` - fuse; physical_component; centroid=(755.0, 1353.0); source=component_visual_ocr_labels.csv
70. `DS-105A` - disconnect_switch; physical_component; centroid=(885.0, 1353.0); source=component_visual_ocr_labels.csv
71. `FU-106A` - fuse; physical_component; centroid=(1015.0, 1353.0); source=component_visual_ocr_labels.csv
72. `DS-107A` - disconnect_switch; physical_component; centroid=(1145.0, 1353.0); source=component_visual_ocr_labels.csv
73. `FU-108A` - fuse; physical_component; centroid=(1275.0, 1353.0); source=component_visual_ocr_labels.csv
74. `DS-109A` - disconnect_switch; physical_component; centroid=(1405.0, 1353.0); source=component_visual_ocr_labels.csv
75. `FU-110A` - fuse; physical_component; centroid=(1535.0, 1353.0); source=component_visual_ocr_labels.csv
76. `DS-111A` - disconnect_switch; physical_component; centroid=(1665.0, 1353.0); source=component_visual_ocr_labels.csv
77. `FU-112A` - fuse; physical_component; centroid=(1795.0, 1353.0); source=component_visual_ocr_labels.csv
78. `DS-201B` - disconnect_switch; physical_component; centroid=(2365.0, 1353.0); source=component_visual_ocr_labels.csv
79. `FU-202B` - fuse; physical_component; centroid=(2495.0, 1353.0); source=component_visual_ocr_labels.csv
80. `DS-203B` - disconnect_switch; physical_component; centroid=(2625.0, 1353.0); source=component_visual_ocr_labels.csv
81. `FU-204B` - fuse; physical_component; centroid=(2755.0, 1353.0); source=component_visual_ocr_labels.csv
82. `DS-205B` - disconnect_switch; physical_component; centroid=(2885.0, 1353.0); source=component_visual_ocr_labels.csv
83. `FU-206B` - fuse; physical_component; centroid=(3015.0, 1353.0); source=component_visual_ocr_labels.csv
84. `DS-207B` - disconnect_switch; physical_component; centroid=(3145.0, 1353.0); source=component_visual_ocr_labels.csv
85. `FU-208B` - fuse; physical_component; centroid=(3275.0, 1353.0); source=component_visual_ocr_labels.csv
86. `DS-209B` - disconnect_switch; physical_component; centroid=(3405.0, 1353.0); source=component_visual_ocr_labels.csv
87. `FU-210B` - fuse; physical_component; centroid=(3535.0, 1353.0); source=component_visual_ocr_labels.csv
88. `DS-211B` - disconnect_switch; physical_component; centroid=(3665.0, 1353.0); source=component_visual_ocr_labels.csv
89. `FU-212B` - fuse; physical_component; centroid=(3795.0, 1353.0); source=component_visual_ocr_labels.csv
90. `FIS-101A` - physical_component; physical_component; centroid=(365.0, 1452.5); source=component_visual_ocr_labels.csv
91. `FIS-102A` - physical_component; physical_component; centroid=(495.0, 1452.5); source=component_visual_ocr_labels.csv
92. `FIS-103A` - physical_component; physical_component; centroid=(625.0, 1452.5); source=component_visual_ocr_labels.csv
93. `FIS-104A` - physical_component; physical_component; centroid=(755.0, 1452.5); source=component_visual_ocr_labels.csv
94. `FIS-105A` - physical_component; physical_component; centroid=(885.0, 1452.5); source=component_visual_ocr_labels.csv
95. `FIS-108A` - physical_component; physical_component; centroid=(1275.0, 1452.5); source=component_visual_ocr_labels.csv
96. `FIS-109A` - physical_component; physical_component; centroid=(1405.0, 1452.5); source=component_visual_ocr_labels.csv
97. `FIS-110A` - physical_component; physical_component; centroid=(1535.0, 1452.5); source=component_visual_ocr_labels.csv
98. `FIS-111A` - physical_component; physical_component; centroid=(1665.0, 1452.5); source=component_visual_ocr_labels.csv
99. `FIS-201B` - physical_component; physical_component; centroid=(2365.0, 1452.5); source=component_visual_ocr_labels.csv
100. `FIS-202B` - physical_component; physical_component; centroid=(2495.0, 1452.5); source=component_visual_ocr_labels.csv
101. `FIS-203B` - physical_component; physical_component; centroid=(2625.0, 1452.5); source=component_visual_ocr_labels.csv
102. `FIS-204B` - physical_component; physical_component; centroid=(2755.0, 1452.5); source=component_visual_ocr_labels.csv
103. `FIS-205B` - physical_component; physical_component; centroid=(2885.0, 1452.5); source=component_visual_ocr_labels.csv
104. `FIS-208B` - physical_component; physical_component; centroid=(3275.0, 1452.5); source=component_visual_ocr_labels.csv
105. `FIS-209B` - physical_component; physical_component; centroid=(3405.0, 1452.5); source=component_visual_ocr_labels.csv
106. `FIS-210B` - physical_component; physical_component; centroid=(3535.0, 1452.5); source=component_visual_ocr_labels.csv
107. `FIS-211B` - physical_component; physical_component; centroid=(3665.0, 1452.5); source=component_visual_ocr_labels.csv
108. `RELAY-K106A` - relay; physical_component; centroid=(1015.0, 1490.0); source=component_visual_ocr_labels.csv
109. `RELAY-K107A` - relay; physical_component; centroid=(1145.0, 1490.0); source=component_visual_ocr_labels.csv
110. `RELAY-K112A` - relay; physical_component; centroid=(1795.0, 1490.0); source=component_visual_ocr_labels.csv
111. `RELAY-K206B` - relay; physical_component; centroid=(3015.0, 1490.0); source=component_visual_ocr_labels.csv
112. `RELAY-K207B` - relay; physical_component; centroid=(3145.0, 1490.0); source=component_visual_ocr_labels.csv
113. `RELAY-K212B` - relay; physical_component; centroid=(3795.0, 1490.0); source=component_visual_ocr_labels.csv
114. `PUMP-SLC-1A` - pump_motor; physical_component; centroid=(365.0, 1577.5); source=component_visual_ocr_labels.csv
115. `PUMP-CCW-1A` - pump_motor; physical_component; centroid=(495.0, 1577.5); source=component_visual_ocr_labels.csv
116. `PUMP-RHR-1A` - pump_motor; physical_component; centroid=(625.0, 1577.5); source=component_visual_ocr_labels.csv
117. `PUMP-CS-1A` - pump_motor; physical_component; centroid=(755.0, 1577.5); source=component_visual_ocr_labels.csv
118. `FAN-CDR1-1A` - fan_motor; physical_component; centroid=(885.0, 1577.5); source=component_visual_ocr_labels.csv
119. `PUMP-SW-1A` - pump_motor; physical_component; centroid=(1405.0, 1577.5); source=component_visual_ocr_labels.csv
120. `MTR-AHU-1A` - motor; physical_component; centroid=(1535.0, 1577.5); source=component_visual_ocr_labels.csv
121. `CFP-AIR-1A` - physical_component; physical_component; centroid=(1665.0, 1577.5); source=component_visual_ocr_labels.csv
122. `PUMP-SLC-1B` - pump_motor; physical_component; centroid=(2365.0, 1577.5); source=component_visual_ocr_labels.csv
123. `PUMP-CCW-1B` - pump_motor; physical_component; centroid=(2495.0, 1577.5); source=component_visual_ocr_labels.csv
124. `PUMP-RHR-1B` - pump_motor; physical_component; centroid=(2625.0, 1577.5); source=component_visual_ocr_labels.csv
125. `PUMP-CS-1B` - pump_motor; physical_component; centroid=(2755.0, 1577.5); source=component_visual_ocr_labels.csv
126. `FAN-CDR1-1B` - fan_motor; physical_component; centroid=(2885.0, 1577.5); source=component_visual_ocr_labels.csv
127. `PUMP-SW-1B` - pump_motor; physical_component; centroid=(3405.0, 1577.5); source=component_visual_ocr_labels.csv
128. `MTR-AHU-1B` - motor; physical_component; centroid=(3535.0, 1577.5); source=component_visual_ocr_labels.csv
129. `CFP-AIR-1B` - physical_component; physical_component; centroid=(3665.0, 1577.5); source=component_visual_ocr_labels.csv
130. `MOV-RHCU-101A` - pid_valve; physical_component; centroid=(1015.0, 1604.0); source=component_visual_ocr_labels.csv
131. `MOV-RHR-102A` - pid_valve; physical_component; centroid=(1145.0, 1604.0); source=component_visual_ocr_labels.csv
132. `HTR-PZR-1A` - heater_load; physical_component; centroid=(1275.0, 1604.0); source=component_visual_ocr_labels.csv
133. `MOV-RHCU-101B` - pid_valve; physical_component; centroid=(3015.0, 1604.0); source=component_visual_ocr_labels.csv
134. `MOV-RHR-102B` - pid_valve; physical_component; centroid=(3145.0, 1604.0); source=component_visual_ocr_labels.csv
135. `HTR-PZR-1B` - heater_load; physical_component; centroid=(3275.0, 1604.0); source=component_visual_ocr_labels.csv
136. `INST-RAD-1A` - instrument; physical_component; centroid=(1795.0, 1609.0); source=component_visual_ocr_labels.csv
137. `INST-RAD-1B` - instrument; physical_component; centroid=(3795.0, 1609.0); source=component_visual_ocr_labels.csv
138. `LS-RHR-1A` - pid_instrument; physical_component; centroid=(625.0, 1702.5); source=component_visual_ocr_labels.csv
139. `LS-RHCU-101A` - pid_instrument; physical_component; centroid=(1015.0, 1702.5); source=component_visual_ocr_labels.csv
140. `LS-RHR-102A` - pid_instrument; physical_component; centroid=(1145.0, 1702.5); source=component_visual_ocr_labels.csv
141. `LS-RHR-1B` - pid_instrument; physical_component; centroid=(2625.0, 1702.5); source=component_visual_ocr_labels.csv
142. `LS-RHCU-101B` - pid_instrument; physical_component; centroid=(3015.0, 1702.5); source=component_visual_ocr_labels.csv
143. `LS-RHR-102B` - pid_instrument; physical_component; centroid=(3145.0, 1702.5); source=component_visual_ocr_labels.csv
144. `TB-SLC-1A` - terminal_block; physical_component; centroid=(365.0, 1705.0); source=component_visual_ocr_labels.csv
145. `GND-CCW-1A` - ground; physical_component; centroid=(495.0, 1705.0); source=component_visual_ocr_labels.csv
146. `TB-CS-1A` - terminal_block; physical_component; centroid=(755.0, 1705.0); source=component_visual_ocr_labels.csv
147. `GND-FAN-1A` - ground; physical_component; centroid=(885.0, 1705.0); source=component_visual_ocr_labels.csv
148. `TB-HTR-1A` - terminal_block; physical_component; centroid=(1275.0, 1705.0); source=component_visual_ocr_labels.csv
149. `GND-SW-1A` - ground; physical_component; centroid=(1405.0, 1705.0); source=component_visual_ocr_labels.csv
150. `GND-AHU-1A` - ground; physical_component; centroid=(1535.0, 1705.0); source=component_visual_ocr_labels.csv
151. `TB-AIR-1A` - terminal_block; physical_component; centroid=(1665.0, 1705.0); source=component_visual_ocr_labels.csv
152. `JB-RAD-1A` - junction_box; physical_component; centroid=(1795.0, 1705.0); source=component_visual_ocr_labels.csv
153. `TB-SLC-1B` - terminal_block; physical_component; centroid=(2365.0, 1705.0); source=component_visual_ocr_labels.csv
154. `GND-CCW-1B` - ground; physical_component; centroid=(2495.0, 1705.0); source=component_visual_ocr_labels.csv
155. `TB-CS-1B` - terminal_block; physical_component; centroid=(2755.0, 1705.0); source=component_visual_ocr_labels.csv
156. `GND-FAN-1B` - ground; physical_component; centroid=(2885.0, 1705.0); source=component_visual_ocr_labels.csv
157. `TB-HTR-1B` - terminal_block; physical_component; centroid=(3275.0, 1705.0); source=component_visual_ocr_labels.csv
158. `GND-SW-1B` - ground; physical_component; centroid=(3405.0, 1705.0); source=component_visual_ocr_labels.csv
159. `GND-AHU-1B` - ground; physical_component; centroid=(3535.0, 1705.0); source=component_visual_ocr_labels.csv
160. `TB-AIR-1B` - terminal_block; physical_component; centroid=(3665.0, 1705.0); source=component_visual_ocr_labels.csv
161. `JB-RAD-1B` - junction_box; physical_component; centroid=(3795.0, 1705.0); source=component_visual_ocr_labels.csv
162. `CB-DC-A` - breaker; physical_component; centroid=(361.0, 2394.0); source=component_visual_ocr_labels.csv
163. `CB-DC-B` - breaker; physical_component; centroid=(4040.5, 2394.0); source=component_visual_ocr_labels.csv
164. `BAT-125-A` - battery; physical_component; centroid=(710.0, 2486.0); source=component_visual_ocr_labels.csv
165. `BAT-125-B` - battery; physical_component; centroid=(3691.0, 2486.0); source=component_visual_ocr_labels.csv
166. `CHGR-125-A` - battery_charger; physical_component; centroid=(536.0, 2492.5); source=component_visual_ocr_labels.csv
167. `CHGR-125-B` - battery_charger; physical_component; centroid=(3866.0, 2492.5); source=component_visual_ocr_labels.csv
168. `BUS-125DC-A` - bus; logical_node; centroid=(1150.0, 2572.5); source=raw_visual_review
169. `BUS-125DC-B` - bus; logical_node; centroid=(3140.0, 2572.5); source=raw_visual_review
170. `CB-DCTIE-AB` - breaker; physical_component; centroid=(2110.0, 2644.5); source=component_visual_ocr_labels.csv
171. `GND-DC-A` - ground; physical_component; centroid=(525.5, 2716.5); source=component_visual_ocr_labels.csv
172. `GND-DC-B` - ground; physical_component; centroid=(3885.0, 2717.5); source=raw_visual_review
173. `INV-120-A` - inverter; physical_component; centroid=(1035.0, 2745.0); source=component_visual_ocr_labels.csv
174. `INV-120-B` - inverter; physical_component; centroid=(3211.5, 2745.0); source=component_visual_ocr_labels.csv
175. `STS-120-A` - physical_component; physical_component; centroid=(1042.5, 2922.5); source=component_visual_ocr_labels.csv
176. `BUS-120AC-A` - bus; logical_node; centroid=(1110.0, 2922.5); source=raw_visual_review
177. `BUS-120AC-B` - bus; logical_node; centroid=(3130.0, 2922.5); source=raw_visual_review
178. `STS-120-B` - physical_component; physical_component; centroid=(3212.5, 2922.5); source=component_visual_ocr_labels.csv
179. `PNL-RPS-A` - panel; physical_component; centroid=(900.0, 3069.0); source=component_visual_ocr_labels.csv
180. `PNL-ESF-A` - panel; physical_component; centroid=(1262.5, 3069.0); source=component_visual_ocr_labels.csv
181. `PNL-RPS-B` - panel; physical_component; centroid=(3012.5, 3069.0); source=component_visual_ocr_labels.csv
182. `PNL-ESF-B` - panel; physical_component; centroid=(3405.0, 3069.0); source=component_visual_ocr_labels.csv
183. `PNL-DCS` - panel; physical_component; centroid=(1762.5, 3072.5); source=component_visual_ocr_labels.csv
184. `TB-RPS-A` - terminal_block; physical_component; centroid=(764.0, 3076.0); source=component_visual_ocr_labels.csv
185. `TB-ESF-A` - terminal_block; physical_component; centroid=(1430.0, 3076.0); source=component_visual_ocr_labels.csv
186. `TB-RPS-B` - terminal_block; physical_component; centroid=(2859.0, 3076.0); source=component_visual_ocr_labels.csv
187. `TB-ESF-B` - terminal_block; physical_component; centroid=(3552.0, 3076.0); source=component_visual_ocr_labels.csv
188. `PNL-ANN` - panel; physical_component; centroid=(2111.5, 3189.0); source=component_visual_ocr_labels.csv
189. `RELAY-UV-A1` - relay; physical_component; centroid=(800.0, 3261.0); source=component_visual_ocr_labels.csv
190. `RELAY-UV-A2` - relay; physical_component; centroid=(930.0, 3261.0); source=component_visual_ocr_labels.csv
191. `RELAY-RPS-A` - relay; physical_component; centroid=(1100.0, 3261.0); source=component_visual_ocr_labels.csv
192. `RELAY-ESF-A` - relay; physical_component; centroid=(1270.0, 3261.0); source=component_visual_ocr_labels.csv
193. `RELAY-UV-B1` - relay; physical_component; centroid=(2903.5, 3261.0); source=component_visual_ocr_labels.csv
194. `RELAY-UV-B2` - relay; physical_component; centroid=(3050.0, 3263.0); source=component_visual_ocr_labels.csv
195. `RELAY-RPS-B` - relay; physical_component; centroid=(3284.0, 3263.0); source=component_visual_ocr_labels.csv
196. `RELAY-ESF-B` - relay; physical_component; centroid=(3385.0, 3263.0); source=component_visual_ocr_labels.csv
197. `REC-SOE-1` - physical_component; physical_component; centroid=(1661.5, 3275.0); source=component_visual_ocr_labels.csv
198. `ANN-ESF-A` - annunciator; physical_component; centroid=(1910.0, 3275.0); source=component_visual_ocr_labels.csv
199. `ANN-ESF-B` - annunciator; physical_component; centroid=(2327.5, 3275.0); source=component_visual_ocr_labels.csv
200. `REC-SOE-2` - physical_component; physical_component; centroid=(3572.5, 3275.0); source=component_visual_ocr_labels.csv
