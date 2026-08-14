# Round 01 Jennifer Notes - Doc 18

Scope: precision review/refinement of Diego round 01 using only doc 18 Input resources and generated inspection artifacts. No GT, evaluator feedback, metric feedback, or prior document outputs used.

Matrix policy: accepted edges only are encoded as 1 in `round_01_jennifer_matrix.csv`; uncertain/plausible edges are documented below and left as 0. Matrix rows/columns keep Diego's 201-node order: 188 inventory rows plus 11 printed logical buses and 2 extra raw-visible components. No anonymous WN-* nodes are used.

## Key Jennifer decisions

- Kept all 11 printed logical buses and the extra visible `DG-1B` / `CB-DG-B` nodes.
- Isolated the inventory row `CB-SWYD-230`: the raw close-up shows the `BB-SWYD-230` junction/heavy bus label there, not a separate breaker symbol.
- Replaced Diego's `CB-GRID-A/B -> CB-SWYD-230 -> BB-SWYD-230` switchyard chain with direct `CB-GRID-A -> BB-SWYD-230` and `CB-GRID-B -> BB-SWYD-230` edges.
- Removed `CB-UAT-A -> BUS-4160B` and `CB-UAT-B -> BUS-4160B`; both UAT breakers stop above the bus with visible white space and no tap/junction.
- Kept `BUS-4160A -> TB-RPS-A -> TR-480-A1`; the solid A-side feeder visibly enters and exits `TB-RPS-A`, while `TB-RPS-B` remains dashed-control only.
- Kept the long charger feeds `BUS-480B -> CHG-125A` and `BUS-480C -> CHG-125B`; both are continuous solid drops from the stated 480 V buses.
- Kept the relay/JB/annunciator cluster candidates out of the matrix because the dashed routing is shared and not endpoint-specific enough.

## Verified added logical/extra nodes

| Node | Decision note |
|---|---|
| `BB-SWYD-230` | Visible printed heavy switchyard bus/junction label at the top source tie; kept as the direct bus endpoint. |
| `BUS-4160A` | Visible printed 4.16 kV bus segment; kept as a logical bus endpoint. |
| `BUS-4160B` | Visible printed 4.16 kV bus segment; kept as a logical bus endpoint. |
| `BUS-480A` | Visible printed 480 V load-center bus; kept as a logical bus endpoint. |
| `BUS-480B` | Visible printed 480 V load-center bus; kept as a logical bus endpoint. |
| `BUS-480C` | Visible printed 480 V load-center bus; kept as a logical bus endpoint. |
| `BUS-480D` | Visible printed 480 V load-center bus; kept as a logical bus endpoint. |
| `BUS-125A` | Visible printed 125 VDC bus in the lower control-power block; kept as a logical bus endpoint. |
| `BUS-125B` | Visible printed 125 VDC bus in the lower control-power block; kept as a logical bus endpoint. |
| `BUS-120A` | Visible printed 120 VAC bus in the lower control-power block; kept as a logical bus endpoint. |
| `BUS-120B` | Visible printed 120 VAC bus in the lower control-power block; kept as a logical bus endpoint. |
| `DG-1B` | Raw-visible generator source symbol missed by inventory; kept. |
| `CB-DG-B` | Raw-visible breaker between `DG-1B` and `BUS-4160B` missed by inventory; kept. |

## Corrected accepted edge list

Accepted edges encoded in matrix: 189.

| # | Node A | Node B | Kind | Confidence | Evidence / decision note |
|---:|---|---|---|---|---|
| 1 | `GRID-SWYD-1` | `CB-GRID-A` | solid power/DC | high | Top-left raw crop: solid line from GRID-SWYD-1 source symbol directly into CB-GRID-A. |
| 2 | `GRID-SWYD-2` | `CB-GRID-B` | solid power/DC | high | Top-left raw crop: solid line from GRID-SWYD-2 source symbol directly into CB-GRID-B. |
| 3 | `CB-GRID-A` | `BB-SWYD-230` | solid power/DC | high | Top-left raw zoom: CB-GRID-A output turns directly into the BB-SWYD-230 junction/heavy bus; no separate CB-SWYD-230 breaker is visible between them. |
| 4 | `CB-GRID-B` | `BB-SWYD-230` | solid power/DC | high | Top-left raw zoom: CB-GRID-B output rises into the same BB-SWYD-230 junction/heavy bus; no separate CB-SWYD-230 breaker is visible between them. |
| 5 | `BB-SWYD-230` | `TR-SAT-1A` | solid power/DC | high | Top-left/top-center raw crops: vertical solid feeder drops from BB-SWYD-230 into TR-SAT-1A. |
| 6 | `BB-SWYD-230` | `TR-SAT-1B` | solid power/DC | high | Top-center raw crop: vertical solid feeder drops from BB-SWYD-230 into TR-SAT-1B. |
| 7 | `BB-SWYD-230` | `CB-GEN-ISO` | solid power/DC | high | Top-center/right raw crops: CB-GEN-ISO sits on the generator path from the heavy BB-SWYD-230 bus. |
| 8 | `CB-GEN-ISO` | `GEN-MAIN-1` | solid power/DC | high | Top-right raw crop: solid generator lead runs from CB-GEN-ISO into GEN-MAIN-1. |
| 9 | `GEN-MAIN-1` | `TR-UAT-1A` | solid power/DC | high | Top-right raw crop: solid vertical lead from GEN-MAIN-1 to TR-UAT-1A. |
| 10 | `GEN-MAIN-1` | `TR-UAT-1B` | solid power/DC | high | Top-right raw crop: solid routed lead from GEN-MAIN-1 to TR-UAT-1B. |
| 11 | `TR-SAT-1A` | `CB-SAT-A` | solid power/DC | high | Top-left raw crop: TR-SAT-1A secondary lead drops directly into CB-SAT-A. |
| 12 | `CB-SAT-A` | `BUS-4160A` | solid power/DC | high | Top-left raw crop: CB-SAT-A output lands by dot on heavy bus labeled BUS-4160A. |
| 13 | `TR-SAT-1B` | `CB-SAT-B` | solid power/DC | high | Top-center raw crop: TR-SAT-1B secondary lead drops directly into CB-SAT-B. |
| 14 | `CB-SAT-B` | `BUS-4160B` | solid power/DC | high | Top-center raw crop: CB-SAT-B output lands by dot on heavy bus labeled BUS-4160B. |
| 15 | `TR-UAT-1A` | `CB-UAT-A` | solid power/DC | high | Top-right close-up: TR-UAT-1A drops directly to CB-UAT-A. The lower side of CB-UAT-A does not visibly continue to BUS-4160B. |
| 16 | `TR-UAT-1B` | `CB-UAT-B` | solid power/DC | high | Top-right close-up: TR-UAT-1B drops directly to CB-UAT-B. The lower side of CB-UAT-B does not visibly continue to BUS-4160B. |
| 17 | `DG-1A` | `CB-DG-A` | solid power/DC | high | Upper-left raw crop: solid feeder from DG-1A into CB-DG-A. |
| 18 | `CB-DG-A` | `BUS-4160A` | solid power/DC | high | Upper-left raw crop: CB-DG-A output rises to a dot on BUS-4160A. |
| 19 | `DG-1B` | `CB-DG-B` | solid power/DC | high | Upper-right raw crop: visible DG-1B source symbol connects by solid line to CB-DG-B. |
| 20 | `CB-DG-B` | `BUS-4160B` | solid power/DC | high | Upper-right raw crop: CB-DG-B output rises to the right-hand 4.16 kV bus. |
| 21 | `BUS-4160A` | `CB-4160-TIE` | solid power/DC | high | Top-center raw crop: CB-4160-TIE is drawn in-line between the left 4.16 kV bus and the right bus. |
| 22 | `CB-4160-TIE` | `BUS-4160B` | solid power/DC | high | Top-center raw crop: CB-4160-TIE output is dot-connected to BUS-4160B. |
| 23 | `BUS-4160A` | `GND-4160A` | solid power/DC | high | Upper-center raw crop: ground symbol GND-4160A is attached directly below BUS-4160A. |
| 24 | `BUS-4160B` | `GND-4160B` | solid power/DC | high | Upper-center raw crop: ground symbol GND-4160B is attached directly below BUS-4160B. |
| 25 | `BUS-4160A` | `PT-4160A` | dashed control/signal | medium-high | Upper A raw crop: dashed PT/control takeoff from BUS-4160A to PT-4160A is directly readable. |
| 26 | `PT-4160A` | `FU-PT-A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from PT-4160A to FU-PT-A. |
| 27 | `FU-PT-A` | `XFRM-CTRL-A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from FU-PT-A to XFRM-CTRL-A. |
| 28 | `XFRM-CTRL-A` | `TB-RPS-A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from XFRM-CTRL-A to TB-RPS-A. |
| 29 | `TB-RPS-A` | `SW-43A` | dashed control/signal | medium-high | Upper A raw crop: dashed control chain runs directly from TB-RPS-A to SW-43A. |
| 30 | `BUS-4160B` | `PT-4160B` | dashed control/signal | medium-high | Upper B raw crop: dashed PT/control takeoff from BUS-4160B to PT-4160B is directly readable. |
| 31 | `PT-4160B` | `FU-PT-B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from PT-4160B to FU-PT-B. |
| 32 | `FU-PT-B` | `XFRM-CTRL-B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from FU-PT-B to XFRM-CTRL-B. |
| 33 | `XFRM-CTRL-B` | `TB-RPS-B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from XFRM-CTRL-B to TB-RPS-B. |
| 34 | `TB-RPS-B` | `SW-43B` | dashed control/signal | medium-high | Upper B raw crop: dashed control chain runs directly from TB-RPS-B to SW-43B. |
| 35 | `BUS-4160A` | `TB-RPS-A` | solid power/DC | high | A-side close-up: the solid 4.16 kV feeder drops from BUS-4160A into the top of TB-RPS-A; this is not merely the dashed PT/control chain. |
| 36 | `TB-RPS-A` | `TR-480-A1` | solid power/DC | high | A-side close-up: the solid feeder exits below TB-RPS-A and jogs into TR-480-A1 before CB-480A-IN. |
| 37 | `TR-480-A1` | `CB-480A-IN` | solid power/DC | high | Upper-left raw crop: TR-480-A1 secondary drops directly into CB-480A-IN. |
| 38 | `CB-480A-IN` | `BUS-480A` | solid power/DC | high | Upper-left raw crop: CB-480A-IN output lands on heavy bus labeled BUS-480A. |
| 39 | `BUS-4160A` | `TR-480-B1` | solid power/DC | high | Upper-left raw crop: vertical solid feeder from BUS-4160A drops into TR-480-B1. |
| 40 | `TR-480-B1` | `CB-480B-IN` | solid power/DC | high | Upper-left raw crop: TR-480-B1 secondary drops directly into CB-480B-IN. |
| 41 | `CB-480B-IN` | `BUS-480B` | solid power/DC | high | Upper-left raw crop: CB-480B-IN output lands on heavy bus labeled BUS-480B. |
| 42 | `BUS-4160B` | `TR-480-C1` | solid power/DC | high | Upper-center raw crop: vertical solid feeder from BUS-4160B drops into TR-480-C1. |
| 43 | `TR-480-C1` | `CB-480C-IN` | solid power/DC | high | Upper-center raw crop: TR-480-C1 secondary drops directly into CB-480C-IN. |
| 44 | `CB-480C-IN` | `BUS-480C` | solid power/DC | high | Upper-center raw crop: CB-480C-IN output lands on heavy bus labeled BUS-480C. |
| 45 | `BUS-4160B` | `TR-480-D1` | solid power/DC | high | Upper-right raw crop: vertical solid feeder from BUS-4160B drops into TR-480-D1. |
| 46 | `TR-480-D1` | `CB-480D-IN` | solid power/DC | high | Upper-right raw crop: TR-480-D1 secondary drops directly into CB-480D-IN. |
| 47 | `CB-480D-IN` | `BUS-480D` | solid power/DC | high | Upper-right raw crop: CB-480D-IN output lands on heavy bus labeled BUS-480D. |
| 48 | `BUS-480A` | `CB-A01` | solid power/DC | high | Middle/upper load-center crops: A01 vertical branch has a junction dot from BUS-480A to CB-A01. |
| 49 | `CB-A01` | `DS-A01` | solid power/DC | high | Middle load-center crop: A01 solid vertical chain continues directly from CB-A01 to DS-A01. |
| 50 | `DS-A01` | `MS-A01` | solid power/DC | high | Middle load-center crop: A01 solid vertical chain continues directly from DS-A01 to MS-A01. |
| 51 | `MS-A01` | `PUMP-CCW-A1` | solid power/DC | high | Middle load-center crop: A01 solid vertical chain continues directly from MS-A01 to PUMP-CCW-A1. |
| 52 | `BUS-480A` | `CB-A02` | solid power/DC | high | Middle/upper load-center crops: A02 vertical branch has a junction dot from BUS-480A to CB-A02. |
| 53 | `CB-A02` | `DS-A02` | solid power/DC | high | Middle load-center crop: A02 solid vertical chain continues directly from CB-A02 to DS-A02. |
| 54 | `DS-A02` | `MS-A02` | solid power/DC | high | Middle load-center crop: A02 solid vertical chain continues directly from DS-A02 to MS-A02. |
| 55 | `MS-A02` | `PUMP-RHR-A1` | solid power/DC | high | Middle load-center crop: A02 solid vertical chain continues directly from MS-A02 to PUMP-RHR-A1. |
| 56 | `BUS-480A` | `CB-A03` | solid power/DC | high | Middle/upper load-center crops: A03 vertical branch has a junction dot from BUS-480A to CB-A03. |
| 57 | `CB-A03` | `FS-A03` | solid power/DC | high | Middle load-center crop: A03 solid vertical chain continues directly from CB-A03 to FS-A03. |
| 58 | `FS-A03` | `MS-A03` | solid power/DC | high | Middle load-center crop: A03 solid vertical chain continues directly from FS-A03 to MS-A03. |
| 59 | `MS-A03` | `FAN-RB-A1` | solid power/DC | high | Middle load-center crop: A03 solid vertical chain continues directly from MS-A03 to FAN-RB-A1. |
| 60 | `BUS-480A` | `CB-A04` | solid power/DC | high | Middle/upper load-center crops: A04 vertical branch has a junction dot from BUS-480A to CB-A04. |
| 61 | `CB-A04` | `DS-A04` | solid power/DC | high | Middle load-center crop: A04 solid vertical chain continues directly from CB-A04 to DS-A04. |
| 62 | `DS-A04` | `RY-A04` | solid power/DC | high | Middle load-center crop: A04 solid vertical chain continues directly from DS-A04 to RY-A04. |
| 63 | `RY-A04` | `MOV-SI-A11` | solid power/DC | high | Middle load-center crop: A04 solid vertical chain continues directly from RY-A04 to MOV-SI-A11. |
| 64 | `BUS-480A` | `CB-A05` | solid power/DC | high | Middle/upper load-center crops: A05 vertical branch has a junction dot from BUS-480A to CB-A05. |
| 65 | `CB-A05` | `DS-A05` | solid power/DC | high | Middle load-center crop: A05 solid vertical chain continues directly from CB-A05 to DS-A05. |
| 66 | `DS-A05` | `CP-A05` | solid power/DC | high | Middle load-center crop: A05 solid vertical chain continues directly from DS-A05 to CP-A05. |
| 67 | `CP-A05` | `PNL-LTG-A1` | solid power/DC | high | Middle load-center crop: A05 solid vertical chain continues directly from CP-A05 to PNL-LTG-A1. |
| 68 | `BUS-480A` | `CB-A06` | solid power/DC | high | Middle/upper load-center crops: A06 vertical branch has a junction dot from BUS-480A to CB-A06. |
| 69 | `CB-A06` | `DS-A06` | solid power/DC | high | Middle load-center crop: A06 solid vertical chain continues directly from CB-A06 to DS-A06. |
| 70 | `DS-A06` | `MS-A06` | solid power/DC | high | Middle load-center crop: A06 solid vertical chain continues directly from DS-A06 to MS-A06. |
| 71 | `MS-A06` | `PUMP-AFW-A1` | solid power/DC | high | Middle load-center crop: A06 solid vertical chain continues directly from MS-A06 to PUMP-AFW-A1. |
| 72 | `BUS-480A` | `CB-A07` | solid power/DC | high | Middle/upper load-center crops: A07 vertical branch has a junction dot from BUS-480A to CB-A07. |
| 73 | `CB-A07` | `FS-A07` | solid power/DC | high | Middle load-center crop: A07 solid vertical chain continues directly from CB-A07 to FS-A07. |
| 74 | `FS-A07` | `FU-A07` | solid power/DC | high | Middle load-center crop: A07 solid vertical chain continues directly from FS-A07 to FU-A07. |
| 75 | `FU-A07` | `HTR-PZR-A1` | solid power/DC | high | Middle load-center crop: A07 solid vertical chain continues directly from FU-A07 to HTR-PZR-A1. |
| 76 | `BUS-480A` | `CB-A08` | solid power/DC | high | Middle/upper load-center crops: A08 vertical branch has a junction dot from BUS-480A to CB-A08. |
| 77 | `CB-A08` | `DS-A08` | solid power/DC | high | Middle load-center crop: A08 solid vertical chain continues directly from CB-A08 to DS-A08. |
| 78 | `DS-A08` | `TB-A08` | solid power/DC | high | Middle load-center crop: A08 solid vertical chain continues directly from DS-A08 to TB-A08. |
| 79 | `TB-A08` | `SPARE-A8` | solid power/DC | high | Middle load-center crop: A08 solid vertical chain continues directly from TB-A08 to SPARE-A8. |
| 80 | `BUS-480B` | `CB-B01` | solid power/DC | high | Middle/upper load-center crops: B01 vertical branch has a junction dot from BUS-480B to CB-B01. |
| 81 | `CB-B01` | `DS-B01` | solid power/DC | high | Middle load-center crop: B01 solid vertical chain continues directly from CB-B01 to DS-B01. |
| 82 | `DS-B01` | `MS-B01` | solid power/DC | high | Middle load-center crop: B01 solid vertical chain continues directly from DS-B01 to MS-B01. |
| 83 | `MS-B01` | `PUMP-CCW-B1` | solid power/DC | high | Middle load-center crop: B01 solid vertical chain continues directly from MS-B01 to PUMP-CCW-B1. |
| 84 | `BUS-480B` | `CB-B02` | solid power/DC | high | Middle/upper load-center crops: B02 vertical branch has a junction dot from BUS-480B to CB-B02. |
| 85 | `CB-B02` | `DS-B02` | solid power/DC | high | Middle load-center crop: B02 solid vertical chain continues directly from CB-B02 to DS-B02. |
| 86 | `DS-B02` | `MS-B02` | solid power/DC | high | Middle load-center crop: B02 solid vertical chain continues directly from DS-B02 to MS-B02. |
| 87 | `MS-B02` | `PUMP-RHR-B1` | solid power/DC | high | Middle load-center crop: B02 solid vertical chain continues directly from MS-B02 to PUMP-RHR-B1. |
| 88 | `BUS-480B` | `CB-B03` | solid power/DC | high | Middle/upper load-center crops: B03 vertical branch has a junction dot from BUS-480B to CB-B03. |
| 89 | `CB-B03` | `FS-B03` | solid power/DC | high | Middle load-center crop: B03 solid vertical chain continues directly from CB-B03 to FS-B03. |
| 90 | `FS-B03` | `MS-B03` | solid power/DC | high | Middle load-center crop: B03 solid vertical chain continues directly from FS-B03 to MS-B03. |
| 91 | `MS-B03` | `FAN-FUEL-B1` | solid power/DC | high | Middle load-center crop: B03 solid vertical chain continues directly from MS-B03 to FAN-FUEL-B1. |
| 92 | `BUS-480B` | `CB-B04` | solid power/DC | high | Middle/upper load-center crops: B04 vertical branch has a junction dot from BUS-480B to CB-B04. |
| 93 | `CB-B04` | `DS-B04` | solid power/DC | high | Middle load-center crop: B04 solid vertical chain continues directly from CB-B04 to DS-B04. |
| 94 | `DS-B04` | `RY-B04` | solid power/DC | high | Middle load-center crop: B04 solid vertical chain continues directly from DS-B04 to RY-B04. |
| 95 | `RY-B04` | `MOV-CCW-B21` | solid power/DC | high | Middle load-center crop: B04 solid vertical chain continues directly from RY-B04 to MOV-CCW-B21. |
| 96 | `BUS-480B` | `CB-B05` | solid power/DC | high | Middle/upper load-center crops: B05 vertical branch has a junction dot from BUS-480B to CB-B05. |
| 97 | `CB-B05` | `DS-B05` | solid power/DC | high | Middle load-center crop: B05 solid vertical chain continues directly from CB-B05 to DS-B05. |
| 98 | `DS-B05` | `CP-B05` | solid power/DC | high | Middle load-center crop: B05 solid vertical chain continues directly from DS-B05 to CP-B05. |
| 99 | `CP-B05` | `MCC-AUX-B6` | solid power/DC | high | Middle load-center crop: B05 solid vertical chain continues directly from CP-B05 to MCC-AUX-B6. |
| 100 | `BUS-480B` | `CB-B06` | solid power/DC | high | Middle/upper load-center crops: B06 vertical branch has a junction dot from BUS-480B to CB-B06. |
| 101 | `CB-B06` | `DS-B06` | solid power/DC | high | Middle load-center crop: B06 solid vertical chain continues directly from CB-B06 to DS-B06. |
| 102 | `DS-B06` | `MS-B06` | solid power/DC | high | Middle load-center crop: B06 solid vertical chain continues directly from DS-B06 to MS-B06. |
| 103 | `MS-B06` | `AIR-CMP-B1` | solid power/DC | high | Middle load-center crop: B06 solid vertical chain continues directly from MS-B06 to AIR-CMP-B1. |
| 104 | `BUS-480B` | `CB-B07` | solid power/DC | high | Middle/upper load-center crops: B07 vertical branch has a junction dot from BUS-480B to CB-B07. |
| 105 | `CB-B07` | `FS-B07` | solid power/DC | high | Middle load-center crop: B07 solid vertical chain continues directly from CB-B07 to FS-B07. |
| 106 | `FS-B07` | `RY-B07` | solid power/DC | high | Middle load-center crop: B07 solid vertical chain continues directly from FS-B07 to RY-B07. |
| 107 | `RY-B07` | `VLV-CHG-B1` | solid power/DC | high | Middle load-center crop: B07 solid vertical chain continues directly from RY-B07 to VLV-CHG-B1. |
| 108 | `BUS-480C` | `CB-C01` | solid power/DC | high | Middle/upper load-center crops: C01 vertical branch has a junction dot from BUS-480C to CB-C01. |
| 109 | `CB-C01` | `DS-C01` | solid power/DC | high | Middle load-center crop: C01 solid vertical chain continues directly from CB-C01 to DS-C01. |
| 110 | `DS-C01` | `MS-C01` | solid power/DC | high | Middle load-center crop: C01 solid vertical chain continues directly from DS-C01 to MS-C01. |
| 111 | `MS-C01` | `PUMP-HPCI-C1` | solid power/DC | high | Middle load-center crop: C01 solid vertical chain continues directly from MS-C01 to PUMP-HPCI-C1. |
| 112 | `BUS-480C` | `CB-C02` | solid power/DC | high | Middle/upper load-center crops: C02 vertical branch has a junction dot from BUS-480C to CB-C02. |
| 113 | `CB-C02` | `DS-C02` | solid power/DC | high | Middle load-center crop: C02 solid vertical chain continues directly from CB-C02 to DS-C02. |
| 114 | `DS-C02` | `MS-C02` | solid power/DC | high | Middle load-center crop: C02 solid vertical chain continues directly from DS-C02 to MS-C02. |
| 115 | `MS-C02` | `PUMP-RCW-C1` | solid power/DC | high | Middle load-center crop: C02 solid vertical chain continues directly from MS-C02 to PUMP-RCW-C1. |
| 116 | `BUS-480C` | `CB-C03` | solid power/DC | high | Middle/upper load-center crops: C03 vertical branch has a junction dot from BUS-480C to CB-C03. |
| 117 | `CB-C03` | `FS-C03` | solid power/DC | high | Middle load-center crop: C03 solid vertical chain continues directly from CB-C03 to FS-C03. |
| 118 | `FS-C03` | `MS-C03` | solid power/DC | high | Middle load-center crop: C03 solid vertical chain continues directly from FS-C03 to MS-C03. |
| 119 | `MS-C03` | `FAN-RB-C1` | solid power/DC | high | Middle load-center crop: C03 solid vertical chain continues directly from MS-C03 to FAN-RB-C1. |
| 120 | `BUS-480C` | `CB-C04` | solid power/DC | high | Middle/upper load-center crops: C04 vertical branch has a junction dot from BUS-480C to CB-C04. |
| 121 | `CB-C04` | `DS-C04` | solid power/DC | high | Middle load-center crop: C04 solid vertical chain continues directly from CB-C04 to DS-C04. |
| 122 | `DS-C04` | `RY-C04` | solid power/DC | high | Middle load-center crop: C04 solid vertical chain continues directly from DS-C04 to RY-C04. |
| 123 | `RY-C04` | `MOV-RHR-C11` | solid power/DC | high | Middle load-center crop: C04 solid vertical chain continues directly from RY-C04 to MOV-RHR-C11. |
| 124 | `BUS-480C` | `CB-C05` | solid power/DC | high | Middle/upper load-center crops: C05 vertical branch has a junction dot from BUS-480C to CB-C05. |
| 125 | `CB-C05` | `DS-C05` | solid power/DC | high | Middle load-center crop: C05 solid vertical chain continues directly from CB-C05 to DS-C05. |
| 126 | `DS-C05` | `MS-C05` | solid power/DC | high | Middle load-center crop: C05 solid vertical chain continues directly from DS-C05 to MS-C05. |
| 127 | `MS-C05` | `PUMP-SEAL-C1` | solid power/DC | high | Middle load-center crop: C05 solid vertical chain continues directly from MS-C05 to PUMP-SEAL-C1. |
| 128 | `BUS-480C` | `CB-C06` | solid power/DC | high | Middle/upper load-center crops: C06 vertical branch has a junction dot from BUS-480C to CB-C06. |
| 129 | `CB-C06` | `DS-C06` | solid power/DC | high | Middle load-center crop: C06 solid vertical chain continues directly from CB-C06 to DS-C06. |
| 130 | `DS-C06` | `CP-C06` | solid power/DC | high | Middle load-center crop: C06 solid vertical chain continues directly from DS-C06 to CP-C06. |
| 131 | `CP-C06` | `PNL-IC-C7` | solid power/DC | high | Middle load-center crop: C06 solid vertical chain continues directly from CP-C06 to PNL-IC-C7. |
| 132 | `BUS-480C` | `CB-C07` | solid power/DC | high | Middle/upper load-center crops: C07 vertical branch has a junction dot from BUS-480C to CB-C07. |
| 133 | `CB-C07` | `FS-C07` | solid power/DC | high | Middle load-center crop: C07 solid vertical chain continues directly from CB-C07 to FS-C07. |
| 134 | `FS-C07` | `MS-C07` | solid power/DC | high | Middle load-center crop: C07 solid vertical chain continues directly from FS-C07 to MS-C07. |
| 135 | `MS-C07` | `SUMP-PMP-C1` | solid power/DC | high | Middle load-center crop: C07 solid vertical chain continues directly from MS-C07 to SUMP-PMP-C1. |
| 136 | `BUS-480C` | `CB-C08` | solid power/DC | high | Middle/upper load-center crops: C08 vertical branch has a junction dot from BUS-480C to CB-C08. |
| 137 | `CB-C08` | `DS-C08` | solid power/DC | high | Middle load-center crop: C08 solid vertical chain continues directly from CB-C08 to DS-C08. |
| 138 | `DS-C08` | `FU-C08` | solid power/DC | high | Middle load-center crop: C08 solid vertical chain continues directly from DS-C08 to FU-C08. |
| 139 | `FU-C08` | `HTR-VENT-C2` | solid power/DC | high | Middle load-center crop: C08 solid vertical chain continues directly from FU-C08 to HTR-VENT-C2. |
| 140 | `BUS-480D` | `CB-D01` | solid power/DC | high | Middle/upper load-center crops: D01 vertical branch has a junction dot from BUS-480D to CB-D01. |
| 141 | `CB-D01` | `DS-D01` | solid power/DC | high | Middle load-center crop: D01 solid vertical chain continues directly from CB-D01 to DS-D01. |
| 142 | `DS-D01` | `MS-D01` | solid power/DC | high | Middle load-center crop: D01 solid vertical chain continues directly from DS-D01 to MS-D01. |
| 143 | `MS-D01` | `PUMP-AFW-D1` | solid power/DC | high | Middle load-center crop: D01 solid vertical chain continues directly from MS-D01 to PUMP-AFW-D1. |
| 144 | `BUS-480D` | `CB-D02` | solid power/DC | high | Middle/upper load-center crops: D02 vertical branch has a junction dot from BUS-480D to CB-D02. |
| 145 | `CB-D02` | `DS-D02` | solid power/DC | high | Middle load-center crop: D02 solid vertical chain continues directly from CB-D02 to DS-D02. |
| 146 | `DS-D02` | `MS-D02` | solid power/DC | high | Middle load-center crop: D02 solid vertical chain continues directly from DS-D02 to MS-D02. |
| 147 | `MS-D02` | `FAN-CR-D1` | solid power/DC | high | Middle load-center crop: D02 solid vertical chain continues directly from MS-D02 to FAN-CR-D1. |
| 148 | `BUS-480D` | `CB-D03` | solid power/DC | high | Middle/upper load-center crops: D03 vertical branch has a junction dot from BUS-480D to CB-D03. |
| 149 | `CB-D03` | `FS-D03` | solid power/DC | high | Middle load-center crop: D03 solid vertical chain continues directly from CB-D03 to FS-D03. |
| 150 | `FS-D03` | `RY-D03` | solid power/DC | high | Middle load-center crop: D03 solid vertical chain continues directly from FS-D03 to RY-D03. |
| 151 | `RY-D03` | `MOV-SI-D21` | solid power/DC | high | Middle load-center crop: D03 solid vertical chain continues directly from RY-D03 to MOV-SI-D21. |
| 152 | `BUS-480D` | `CB-D04` | solid power/DC | high | Middle/upper load-center crops: D04 vertical branch has a junction dot from BUS-480D to CB-D04. |
| 153 | `CB-D04` | `DS-D04` | solid power/DC | high | Middle load-center crop: D04 solid vertical chain continues directly from CB-D04 to DS-D04. |
| 154 | `DS-D04` | `MS-D04` | solid power/DC | high | Middle load-center crop: D04 solid vertical chain continues directly from DS-D04 to MS-D04. |
| 155 | `MS-D04` | `PUMP-LUBE-D1` | solid power/DC | high | Middle load-center crop: D04 solid vertical chain continues directly from MS-D04 to PUMP-LUBE-D1. |
| 156 | `BUS-480D` | `CB-D05` | solid power/DC | high | Middle/upper load-center crops: D05 vertical branch has a junction dot from BUS-480D to CB-D05. |
| 157 | `CB-D05` | `DS-D05` | solid power/DC | high | Middle load-center crop: D05 solid vertical chain continues directly from CB-D05 to DS-D05. |
| 158 | `DS-D05` | `CP-D05` | solid power/DC | high | Middle load-center crop: D05 solid vertical chain continues directly from DS-D05 to CP-D05. |
| 159 | `CP-D05` | `PNL-ESS-D5` | solid power/DC | high | Middle load-center crop: D05 solid vertical chain continues directly from CP-D05 to PNL-ESS-D5. |
| 160 | `BUS-480D` | `CB-D06` | solid power/DC | high | Middle/upper load-center crops: D06 vertical branch has a junction dot from BUS-480D to CB-D06. |
| 161 | `CB-D06` | `DS-D06` | solid power/DC | high | Middle load-center crop: D06 solid vertical chain continues directly from CB-D06 to DS-D06. |
| 162 | `DS-D06` | `MS-D06` | solid power/DC | high | Middle load-center crop: D06 solid vertical chain continues directly from DS-D06 to MS-D06. |
| 163 | `MS-D06` | `COMP-AIR-D1` | solid power/DC | high | Middle load-center crop: D06 solid vertical chain continues directly from MS-D06 to COMP-AIR-D1. |
| 164 | `BUS-480D` | `CB-D07` | solid power/DC | high | Middle/upper load-center crops: D07 vertical branch has a junction dot from BUS-480D to CB-D07. |
| 165 | `CB-D07` | `FS-D07` | solid power/DC | high | Middle load-center crop: D07 solid vertical chain continues directly from CB-D07 to FS-D07. |
| 166 | `FS-D07` | `TB-D07` | solid power/DC | high | Middle load-center crop: D07 solid vertical chain continues directly from FS-D07 to TB-D07. |
| 167 | `TB-D07` | `SPARE-D7` | solid power/DC | high | Middle load-center crop: D07 solid vertical chain continues directly from TB-D07 to SPARE-D7. |
| 168 | `BUS-480B` | `CHG-125A` | solid power/DC | high | Left-half raw view: a long solid drop from the left side of BUS-480B is continuous into CHG-125A; no intervening component or wrong-bus tap is visible. |
| 169 | `CHG-125A` | `REC-125A` | solid power/DC | high | Lower-left raw crop: CHG-125A output line runs directly to REC-125A. |
| 170 | `REC-125A` | `CB-DC-A` | solid power/DC | high | Lower-left raw crop: REC-125A output line runs directly to CB-DC-A. |
| 171 | `CB-DC-A` | `BUS-125A` | solid power/DC | high | Lower-left raw crop: CB-DC-A vertical output lands on heavy BUS-125A rail. |
| 172 | `BUS-125A` | `BAT-125A` | solid power/DC | high | Lower-left raw crop: BAT-125A is directly tapped from BUS-125A. |
| 173 | `BUS-125A` | `GND-DC-A` | solid power/DC | high | Lower-left raw crop: GND-DC-A ground symbol is attached directly below BUS-125A. |
| 174 | `BUS-125A` | `INV-120A` | solid power/DC | medium-high | Lower-left raw crop: BUS-125A rail terminates at the DC side of INV-120A. |
| 175 | `INV-120A` | `UPS-120A` | dashed control/signal | medium-high | Lower-left raw crop: short dashed line runs directly from INV-120A to UPS-120A. |
| 176 | `UPS-120A` | `BUS-120A` | solid power/DC | high | Lower-left raw crop: UPS-120A vertical output lands on heavy BUS-120A rail. |
| 177 | `BUS-120A` | `RPS-PNL-A` | solid power/DC | high | Lower-left raw crop: RPS-PNL-A is directly tapped from BUS-120A. |
| 178 | `RPS-PNL-A` | `PLC-RPS-A` | dashed control/signal | medium-high | Lower-left raw crop: short dashed line runs directly from RPS-PNL-A to PLC-RPS-A. |
| 179 | `BUS-480C` | `CHG-125B` | solid power/DC | high | Right/center raw view: a long solid drop from the left side of BUS-480C is continuous into CHG-125B; no intervening component or wrong-bus tap is visible. |
| 180 | `CHG-125B` | `REC-125B` | solid power/DC | high | Lower-center raw crop: CHG-125B output line runs directly to REC-125B. |
| 181 | `REC-125B` | `CB-DC-B` | solid power/DC | high | Lower-center raw crop: REC-125B output line runs directly to CB-DC-B. |
| 182 | `CB-DC-B` | `BUS-125B` | solid power/DC | high | Lower-center raw crop: CB-DC-B vertical output lands on heavy BUS-125B rail. |
| 183 | `BUS-125B` | `BAT-125B` | solid power/DC | high | Lower-center raw crop: BAT-125B is directly tapped from BUS-125B. |
| 184 | `BUS-125B` | `GND-DC-B` | solid power/DC | high | Lower-center raw crop: GND-DC-B ground symbol is attached directly below BUS-125B. |
| 185 | `BUS-125B` | `INV-120B` | solid power/DC | medium-high | Lower-center raw crop: BUS-125B rail terminates at the DC side of INV-120B. |
| 186 | `INV-120B` | `UPS-120B` | dashed control/signal | medium-high | Lower-center raw crop: short dashed line runs directly from INV-120B to UPS-120B. |
| 187 | `UPS-120B` | `BUS-120B` | solid power/DC | high | Lower-center raw crop: UPS-120B vertical output lands on heavy BUS-120B rail. |
| 188 | `BUS-120B` | `RPS-PNL-B` | solid power/DC | high | Lower-center/right raw crop: RPS-PNL-B is directly tapped from BUS-120B. |
| 189 | `RPS-PNL-B` | `PLC-RPS-B` | dashed control/signal | medium-high | Lower-right raw crop: short dashed line runs directly from RPS-PNL-B to PLC-RPS-B. |

## Removed/rejected edge list

| # | Node A | Node B | Reason |
|---:|---|---|---|
| 1 | `CB-GRID-A` | `CB-SWYD-230` | Rejected: raw close-up shows no distinct CB-SWYD-230 breaker symbol; the detected row lies on the switchyard junction/bus label area. CB-GRID-A connects directly to BB-SWYD-230. |
| 2 | `CB-GRID-B` | `CB-SWYD-230` | Rejected: raw close-up shows no distinct CB-SWYD-230 breaker symbol; the lower grid breaker output joins the same switchyard junction directly to BB-SWYD-230. |
| 3 | `CB-SWYD-230` | `BB-SWYD-230` | Rejected: CB-SWYD-230 is not a separate visible endpoint at that location; preserve the inventory row isolated and use BB-SWYD-230 as the printed heavy-bus/junction node. |
| 4 | `CB-UAT-A` | `BUS-4160B` | Rejected: close-up shows clear white space/no solid tap or junction from the lower side of CB-UAT-A to BUS-4160B. Only TR-UAT-1A -> CB-UAT-A is visible. |
| 5 | `CB-UAT-B` | `BUS-4160B` | Rejected: close-up shows clear white space/no solid tap or junction from the lower side of CB-UAT-B to BUS-4160B. Only TR-UAT-1B -> CB-UAT-B is visible. |

## Uncertain/plausible edge list kept out of matrix

These remain visually plausible but not encoded because the dashed/control routing is shared, loops through multiple relays, or lacks a clean direct endpoint-specific connection.

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

## Matrix validation

- Shape: 201 x 201.
- Accepted undirected edges: 189.
- Symmetric: yes.
- Diagonal: all 0.
- Row and column labels: identical and in the same order.
