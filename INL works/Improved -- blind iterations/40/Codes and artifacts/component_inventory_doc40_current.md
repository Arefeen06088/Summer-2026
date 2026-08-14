# Doc 40 Input-Only Component Inventory

Source CSV: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\40\Input resources\component_and_logical_visual_ocr_labels.csv`
Raw schematic: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\40\Input resources\synthetic_nuclear_distribution_schematic.png`

Inventory rows: 65

## Component Type Counts

- battery: 2
- boundary: 2
- breaker: 4
- bus: 4
- control_lane: 2
- current_transformer: 2
- dc_bus: 2
- disconnect_switch: 2
- fan: 2
- feed_note: 2
- generator: 2
- instrument_signal: 2
- inverter: 2
- junction_box: 2
- mcc: 2
- motor_operated_valve: 4
- panel: 2
- pump: 4
- rectifier_charger: 2
- relay: 4
- rps_panel: 2
- signal: 2
- tie_breaker: 1
- transfer_switch: 2
- transformer: 6
- voltage_transformer: 2

## Node Kind Counts

- logical_node: 14
- physical_component: 51

## Ordered Nodes

1. `TRAIN-A-480V-SAFETY-CHANNEL` - boundary; centroid=(525.0, 532.5); bbox=[350.0, 500.0, 700.0, 565.0]
2. `TRAIN-B-480V-SAFETY-CHANNEL` - boundary; centroid=(3270.0, 532.5); bbox=[3060.0, 500.0, 3480.0, 565.0]
3. `SOURCE-NORMAL` - feed_note; centroid=(880.0, 598.5); bbox=[720.0, 572.0, 1040.0, 625.0]
4. `SOURCE-ALTERNATE` - feed_note; centroid=(4475.0, 598.5); bbox=[4210.0, 572.0, 4740.0, 625.0]
5. `SAT-2B` - transformer; centroid=(4442.5, 645.0); bbox=[4330.0, 545.0, 4555.0, 745.0]
6. `UAT-2A` - transformer; centroid=(1112.5, 652.5); bbox=[1010.0, 555.0, 1215.0, 750.0]
7. `DG-21A` - generator; centroid=(622.5, 667.5); bbox=[515.0, 575.0, 730.0, 760.0]
8. `DG-21B` - generator; centroid=(4935.0, 667.5); bbox=[4825.0, 575.0, 5045.0, 760.0]
9. `DS-21A` - disconnect_switch; centroid=(1112.5, 805.0); bbox=[1035.0, 735.0, 1190.0, 875.0]
10. `DS-21B` - disconnect_switch; centroid=(4442.5, 807.5); bbox=[4350.0, 735.0, 4535.0, 880.0]
11. `ATS-21A` - transfer_switch; centroid=(842.5, 955.0); bbox=[735.0, 865.0, 950.0, 1045.0]
12. `ATS-21B` - transfer_switch; centroid=(4687.5, 960.0); bbox=[4570.0, 865.0, 4805.0, 1055.0]
13. `SWGR-21A` - bus; centroid=(1510.0, 1148.0); bbox=[455.0, 1118.0, 2565.0, 1178.0]
14. `SWGR-21B` - bus; centroid=(4060.0, 1148.0); bbox=[3000.0, 1118.0, 5120.0, 1178.0]
15. `TIE-BKR-21AB` - tie_breaker; centroid=(2812.5, 1192.5); bbox=[2700.0, 1115.0, 2925.0, 1270.0]
16. `CB-21A1` - breaker; centroid=(1122.5, 1392.5); bbox=[1050.0, 1320.0, 1195.0, 1465.0]
17. `CB-21B1` - breaker; centroid=(4440.0, 1392.5); bbox=[4350.0, 1320.0, 4530.0, 1465.0]
18. `VT-21A` - voltage_transformer; centroid=(2237.5, 1397.5); bbox=[2160.0, 1315.0, 2315.0, 1480.0]
19. `VT-21B` - voltage_transformer; centroid=(5172.5, 1397.5); bbox=[5100.0, 1315.0, 5245.0, 1480.0]
20. `TR-21A` - transformer; centroid=(1120.0, 1592.5); bbox=[1025.0, 1500.0, 1215.0, 1685.0]
21. `TR-21B` - transformer; centroid=(4435.0, 1592.5); bbox=[4325.0, 1500.0, 4545.0, 1685.0]
22. `MCC-21A` - mcc; centroid=(1477.5, 1857.5); bbox=[480.0, 1770.0, 2475.0, 1945.0]
23. `MCC-21B` - mcc; centroid=(4175.0, 1857.5); bbox=[3190.0, 1770.0, 5160.0, 1945.0]
24. `MCC-21A-480V-3PH` - bus; centroid=(1475.0, 1886.5); bbox=[550.0, 1858.0, 2400.0, 1915.0]
25. `MCC-21B-480V-3PH` - bus; centroid=(4142.5, 1886.5); bbox=[3230.0, 1858.0, 5055.0, 1915.0]
26. `CT-21A` - current_transformer; centroid=(1525.0, 2147.5); bbox=[1435.0, 2070.0, 1615.0, 2225.0]
27. `CT-21B` - current_transformer; centroid=(3917.5, 2147.5); bbox=[3825.0, 2070.0, 4010.0, 2225.0]
28. `CB-MPA1` - breaker; centroid=(630.0, 2152.5); bbox=[555.0, 2085.0, 705.0, 2220.0]
29. `CB-MPB1` - breaker; centroid=(3297.5, 2152.5); bbox=[3220.0, 2090.0, 3375.0, 2215.0]
30. `XFMR-CPT21A` - transformer; centroid=(2462.5, 2157.5); bbox=[2365.0, 2070.0, 2560.0, 2245.0]
31. `XFMR-CPT21B` - transformer; centroid=(3122.5, 2162.5); bbox=[3020.0, 2075.0, 3225.0, 2250.0]
32. `AC-PNL-120B` - panel; centroid=(3111.5, 2467.5); bbox=[3005.0, 2385.0, 3218.0, 2550.0]
33. `AC-PNL-120A` - panel; centroid=(2467.5, 2470.0); bbox=[2350.0, 2385.0, 2585.0, 2555.0]
34. `MOV-HV211A` - motor_operated_valve; centroid=(1852.5, 2475.0); bbox=[1765.0, 2380.0, 1940.0, 2570.0]
35. `MOV-RWST21A` - motor_operated_valve; centroid=(2242.5, 2475.0); bbox=[2150.0, 2380.0, 2335.0, 2570.0]
36. `MOV-HV211B` - motor_operated_valve; centroid=(4507.5, 2475.0); bbox=[4410.0, 2380.0, 4605.0, 2570.0]
37. `MOV-RWST21B` - motor_operated_valve; centroid=(4905.0, 2475.0); bbox=[4800.0, 2380.0, 5010.0, 2570.0]
38. `FAN-RB21A` - fan; centroid=(1405.0, 2477.5); bbox=[1305.0, 2385.0, 1505.0, 2570.0]
39. `PUMP-SI21B` - pump; centroid=(3317.5, 2477.5); bbox=[3230.0, 2390.0, 3405.0, 2565.0]
40. `FAN-RB21B` - fan; centroid=(4085.0, 2477.5); bbox=[3985.0, 2385.0, 4185.0, 2570.0]
41. `PUMP-SI21A` - pump; centroid=(632.5, 2480.0); bbox=[535.0, 2390.0, 730.0, 2570.0]
42. `PUMP-CCW21A` - pump; centroid=(1022.5, 2480.0); bbox=[930.0, 2390.0, 1115.0, 2570.0]
43. `PUMP-CCW21B` - pump; centroid=(3700.0, 2480.0); bbox=[3600.0, 2390.0, 3800.0, 2570.0]
44. `VOLTAGE-SIG-A` - instrument_signal; centroid=(2142.5, 2760.0); bbox=[2040.0, 2715.0, 2245.0, 2805.0]
45. `VOLTAGE-SIG-B` - instrument_signal; centroid=(4455.0, 2760.0); bbox=[4350.0, 2715.0, 4560.0, 2805.0]
46. `LOCA-SIG-A` - signal; centroid=(550.0, 2837.5); bbox=[475.0, 2765.0, 625.0, 2910.0]
47. `LOCA-SIG-B` - signal; centroid=(5147.5, 2837.5); bbox=[5065.0, 2765.0, 5230.0, 2910.0]
48. `JB-21A` - junction_box; centroid=(867.5, 2887.5); bbox=[775.0, 2825.0, 960.0, 2950.0]
49. `JB-21B` - junction_box; centroid=(4877.5, 2887.5); bbox=[4785.0, 2825.0, 4970.0, 2950.0]
50. `RECT-21A` - rectifier_charger; centroid=(2442.5, 2892.5); bbox=[2350.0, 2790.0, 2535.0, 2995.0]
51. `RECT-21B` - rectifier_charger; centroid=(3285.0, 2892.5); bbox=[3185.0, 2790.0, 3385.0, 2995.0]
52. `BAT-21A` - battery; centroid=(1860.0, 2957.5); bbox=[1725.0, 2870.0, 1995.0, 3045.0]
53. `BAT-21B` - battery; centroid=(3857.5, 2957.5); bbox=[3715.0, 2870.0, 4000.0, 3045.0]
54. `DC-BUS-21A` - dc_bus; centroid=(1607.5, 3095.0); bbox=[650.0, 3065.0, 2565.0, 3125.0]
55. `DC-BUS-21B` - dc_bus; centroid=(4227.5, 3095.0); bbox=[3195.0, 3065.0, 5260.0, 3125.0]
56. `RPS-PNL-A` - rps_panel; centroid=(1657.5, 3410.0); bbox=[1510.0, 3320.0, 1805.0, 3500.0]
57. `INV-21A` - inverter; centroid=(2310.0, 3410.0); bbox=[2200.0, 3320.0, 2420.0, 3500.0]
58. `INV-21B` - inverter; centroid=(3512.5, 3410.0); bbox=[3420.0, 3320.0, 3605.0, 3500.0]
59. `RPS-PNL-B` - rps_panel; centroid=(4002.5, 3410.0); bbox=[3845.0, 3320.0, 4160.0, 3500.0]
60. `RELAY-K21B` - relay; centroid=(4460.0, 3410.0); bbox=[4360.0, 3320.0, 4560.0, 3500.0]
61. `RELAY-86B` - relay; centroid=(4942.5, 3410.0); bbox=[4840.0, 3320.0, 5045.0, 3500.0]
62. `RELAY-86A` - relay; centroid=(877.5, 3412.5); bbox=[785.0, 3330.0, 970.0, 3495.0]
63. `RELAY-K21A` - relay; centroid=(1235.0, 3412.5); bbox=[1135.0, 3330.0, 1335.0, 3495.0]
64. `RPS-CH-A-CONTROL-LANE` - control_lane; centroid=(1415.0, 3495.0); bbox=[450.0, 3425.0, 2380.0, 3565.0]
65. `RPS-CH-B-CONTROL-LANE` - control_lane; centroid=(4280.0, 3495.0); bbox=[3470.0, 3425.0, 5090.0, 3565.0]
