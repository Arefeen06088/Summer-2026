# Round 01 Diego Extraction Notes - Doc 24

## Evidence Boundary
- Used only doc 24 input resources and doc 24 artifacts derived from those resources: raw PNG, wire masks/overlays, wire node overlay, component inventory, summaries, and visual crops.
- Raw schematic was treated as primary evidence. Wire nodes were used only as geometric aids and were not included as matrix nodes.
- No ground truth, evaluator output, metric feedback, or derived scoring information was used.

## Node List Rationale
- Matrix includes all 194 physical component labels from `component_labels_list.csv`.
- Added six compact printed bus nodes visible in the raw schematic: `BUS-101A`, `BUS-101B`, `BUS-201A`, `BUS-201B`, `DC-BUS-125A`, and `DC-BUS-125B`.
- Did not add WN IDs, unlabeled junction dots, feeder text, voltage descriptions, title text, raceway/routing text, or dashed area boundaries.
- Kept prepared inventory labels `SW-PGA-A` and `SW-PGA-B` as row/column names, but the raw crop reads `SW-MAN-A` and `SW-MAN-B`; this is a label ambiguity in the generated inventory, not a separate component.
- Printed buses are modeled as bus hubs. Loads and feeders on the same printed bus are not expanded into pairwise cliques.

## Edge Evidence By Area
### Top Sources And 4.16 kV Buses
- Train A offsite source path: `OFFSITE-1 -> CB-101A -> TR-SAT-1A -> BUS-101A`.
- Train B offsite source path: `OFFSITE-2 -> CB-101B -> TR-SAT-1B -> BUS-101B`.
- EDG source paths: `EDG-1A -> CB-DG1A -> BUS-101A` and `EDG-1B -> CB-DG1B -> BUS-101B`.
- EDG dashed/manual control paths: `SW-PGA-A -> TB-DG-A -> CB-DG1A` and `SW-PGA-B -> TB-DG-B -> CB-DG1B`; raw switch text appears to be `SW-MAN-*`.
- Tie breaker is modeled as `BUS-101A -> CB-TIE-1 -> BUS-101B`. A high-recall dashed sync-control candidate `CB-TIE-1 -> SYNC-CAB` is included because the sync cabinet has a vertical lead aligned with the tie routing channel.

### Transformer Feeds To Safety Buses
- Train A transformer feed: `BUS-101A -> CB-201A -> TR-1A -> CB-202A -> BUS-201A`.
- Train B transformer feed: `BUS-101B -> CB-201B -> TR-1B -> CB-202B -> BUS-201B`.

### MCC Feeder Matrix
| Feeder | Upstream bus | Solid power chain | Dashed control chain |
|---|---|---|---|
| 2A01 | BUS-201A | `CB-2A01 -> DS-2A01 -> MCC-2A01 -> TB-2A01 -> PUMP-P201A` | `MCC-2A01 -> RELAY-K2A01; HS-2A01 -> RELAY-K2A01` |
| 2A02 | BUS-201A | `CB-2A02 -> DS-2A02 -> MCC-2A02 -> TB-2A02 -> FAN-F202A` | `MCC-2A02 -> RELAY-K2A02; HS-2A02 -> RELAY-K2A02` |
| 2A03 | BUS-201A | `CB-2A03 -> DS-2A03 -> MCC-2A03 -> TB-2A03 -> MOV-HV203A` | `MCC-2A03 -> RELAY-K2A03; HS-2A03 -> RELAY-K2A03` |
| 2A04 | BUS-201A | `CB-2A04 -> DS-2A04 -> MCC-2A04 -> TB-2A04 -> PUMP-P204A` | `MCC-2A04 -> RELAY-K2A04; HS-2A04 -> RELAY-K2A04` |
| 2A05 | BUS-201A | `CB-2A05 -> DS-2A05 -> MCC-2A05 -> TB-2A05 -> CHLR-205A` | `MCC-2A05 -> RELAY-K2A05; HS-2A05 -> RELAY-K2A05` |
| 2A06 | BUS-201A | `CB-2A06 -> DS-2A06 -> MCC-2A06 -> TB-2A06 -> HTR-206A` | `MCC-2A06 -> RELAY-K2A06; HS-2A06 -> RELAY-K2A06` |
| 2A07 | BUS-201A | `CB-2A07 -> DS-2A07 -> MCC-2A07 -> TB-2A07 -> VALVE-MV207A` | `MCC-2A07 -> RELAY-K2A07; HS-2A07 -> RELAY-K2A07` |
| 2A08 | BUS-201A | `CB-2A08 -> DS-2A08 -> MCC-2A08 -> TB-2A08 -> PMP-LP208A` | `MCC-2A08 -> RELAY-K2A08; HS-2A08 -> RELAY-K2A08` |
| 2A09 | BUS-201A | `CB-2A09 -> DS-2A09 -> MCC-2A09 -> TB-2A09 -> COMP-C209A` | `MCC-2A09 -> RELAY-K2A09; HS-2A09 -> RELAY-K2A09` |
| 2B01 | BUS-201B | `CB-2B01 -> DS-2B01 -> MCC-2B01 -> TB-2B01 -> PUMP-P201B` | `MCC-2B01 -> RELAY-K2B01; HS-2B01 -> RELAY-K2B01` |
| 2B02 | BUS-201B | `CB-2B02 -> DS-2B02 -> MCC-2B02 -> TB-2B02 -> FAN-F202B` | `MCC-2B02 -> RELAY-K2B02; HS-2B02 -> RELAY-K2B02` |
| 2B03 | BUS-201B | `CB-2B03 -> DS-2B03 -> MCC-2B03 -> TB-2B03 -> MOV-HV203B` | `MCC-2B03 -> RELAY-K2B03; HS-2B03 -> RELAY-K2B03` |
| 2B04 | BUS-201B | `CB-2B04 -> DS-2B04 -> MCC-2B04 -> TB-2B04 -> PUMP-P204B` | `MCC-2B04 -> RELAY-K2B04; HS-2B04 -> RELAY-K2B04` |
| 2B05 | BUS-201B | `CB-2B05 -> DS-2B05 -> MCC-2B05 -> TB-2B05 -> CHLR-205B` | `MCC-2B05 -> RELAY-K2B05; HS-2B05 -> RELAY-K2B05` |
| 2B06 | BUS-201B | `CB-2B06 -> DS-2B06 -> MCC-2B06 -> TB-2B06 -> HTR-206B` | `MCC-2B06 -> RELAY-K2B06; HS-2B06 -> RELAY-K2B06` |
| 2B07 | BUS-201B | `CB-2B07 -> DS-2B07 -> MCC-2B07 -> TB-2B07 -> VALVE-MV207B` | `MCC-2B07 -> RELAY-K2B07; HS-2B07 -> RELAY-K2B07` |
| 2B08 | BUS-201B | `CB-2B08 -> DS-2B08 -> MCC-2B08 -> TB-2B08 -> PMP-LP208B` | `MCC-2B08 -> RELAY-K2B08; HS-2B08 -> RELAY-K2B08` |
| 2B09 | BUS-201B | `CB-2B09 -> DS-2B09 -> MCC-2B09 -> TB-2B09 -> COMP-C209B` | `MCC-2B09 -> RELAY-K2B09; HS-2B09 -> RELAY-K2B09` |

### DC And AC Power
- `DC-BUS-125A` connects to `BAT-125A`, `CHG-125A`, `INV-120A`, `PNL-DC-A`, and `METER-V1`.
- `DC-BUS-125B` connects to `BAT-125B`, `CHG-125B`, `INV-120B`, and `PNL-DC-B`; no separate B-side meter label is visible.
- DC panel grounding and ESFAS feeds: `PNL-DC-A -> GND-DC-A`, `PNL-DC-B -> GND-DC-B`, `PNL-DC-A -> ESFAS-PNL-A`, and `PNL-DC-B -> ESFAS-PNL-B`.
- Inverters feed AC panels: `INV-120A -> PNL-AC-A` and `INV-120B -> PNL-AC-B`.

### RPS, Instruments, Relays, Alarm, And Recording
- Instrument trains are modeled as `PT/LT/FT -> JB-401* -> TB-RPS-* -> RPS-PNL-*`, with `JB-401* -> GND-401*` ground edges.
- AC/RPS/trip chain: `PNL-AC-* -> RPS-PNL-* -> TRIP-MOD-*`, plus `RPS-PNL-* -> RELAY-K27* -> RELAY-K59* -> RELAY-K81* -> RELAY-K86*` and `TRIP-MOD-* -> RELAY-K86*`.
- Dotted RPS/annunciator signal routes are represented as `RPS-PNL-A -> ANN-PNL-1`, `RPS-PNL-B -> ANN-PNL-1`, and `ANN-PNL-1 -> SEQ-REC-1`.
- Load-shed and alarm center includes `ESFAS-PNL-A -> LOAD-SHED-CAB`, `ESFAS-PNL-B -> LOAD-SHED-CAB`, `LOAD-SHED-CAB -> TDR-1`, `LOAD-SHED-CAB -> TDR-2`, `LOAD-SHED-CAB -> LAMP-ALM-A`, and `LOAD-SHED-CAB -> LAMP-ALM-B`.
- `ESFAS-PNL-A -> TRIP-MOD-A` is included as a visible dashed branch; no equally clear B-side ESFAS-to-trip branch was added.

## Uncertain/High-Recall Candidates
- `CB-TIE-1 -> SYNC-CAB` is included as high-recall: the sync cabinet lead aligns with the central dashed tie/control routing, but the route resembles a cabinet/raceway boundary in places.
- `ESFAS-PNL-B -> LOAD-SHED-CAB` is included from A/B symmetry and the dashed load-shed/control channel, but the B-side route is less direct than the A-side ESFAS route.
- Dotted alarm/annunciator routes are simplified to named component endpoints; unlabeled junction dots and crossing points were not converted into nodes.
- MCC dashed controls are encoded as `MCC -> RELAY` and `HS -> RELAY` for each feeder. I did not add `MCC -> HS` clique edges.
- Crossings without visible connection dots were not used to create edges.

## Validation Summary
- Node count: 200 (194 inventory components + 6 added printed bus nodes).
- Edge count: 202.
- Symmetric: True.
- Diagonal zero: True.
- Isolated nodes: 0.
- Output matrix: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\24\Results\Iteration_1\round_01_diego_matrix.csv`
- Output notes: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\24\Results\Iteration_1\round_01_diego_notes.md`
