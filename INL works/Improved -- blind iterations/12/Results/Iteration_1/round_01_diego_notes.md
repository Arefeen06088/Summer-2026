# Round 1 Diego Notes - Doc 12

## Node Policy

- Sources used: only `12\Input resources` and `12\Codes and artifacts` raw/overlay/crop artifacts supplied for doc 12.
- Excluded: ground truth, evaluator outputs, scores, validation metrics, prior answer keys, and anonymous `wire_nodes.csv` point IDs as matrix nodes.
- Included as matrix nodes: named physical devices, named MCC/load-center buses, visible logical buses, and equipment ground reference labels.
- Breaker ratings, device ratings, one-line notes, and functional captions such as `UV`, `OC`, `LOCKOUT`, `ANN A`, `RPS A`, `SER`, and `PT-A/PT-B` were treated as evidence/captions, not separate nodes.
- MCC labels (`MCC-1A`, `MCC-1B`, `MCC-2A`, `MCC-2B`) are kept as the named motor-control-center bus/component nodes, not duplicated as separate logical bus aliases.
- Repeated feeder OCR corrections were made from the raw inspection crops: examples include `FU-F001`, `MS-F002`, `DS-F004`, `MS-F020`, `DS-F023`, `MS-F009`, `FU-F012`, and `FU-F028`.

## Buses And Grounds Added

- Added logical buses from raw labels: `BUS-4KV-A`, `BUS-4KV-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-A`, `DC-BUS-B`, and `BUS-120VAC-ESF`.
- The raw drawing labels the 4.16 kV buses as `BUS-4KV-A` and `BUS-4KV-B`, not `BUS-4160-A/B`.
- The lower AC instrument bus is labeled `BUS-120VAC-ESF`, not `BUS-120VAC-RPS`.
- `GND-1` and `GND-2` are included as equipment ground reference nodes only, following the note that grounds shown are reference only.

## Major High-Confidence Connectivity Groups

- Train/source 4.16 kV power: `GEN-G1 -> CB-GEN-1 -> TR-UAT-1 -> CB-101 -> BUS-4KV-A`; standby and EDG A sources feed `BUS-4KV-A`; EDG/standby B/C sources feed `BUS-4KV-B`; `CB-TIE-1` bridges the two 4.16 kV buses.
- Transformer feeders: `BUS-4KV-A` feeds `TR-480-A` and `TR-480-C` through `CB-111`/`CB-112`; `BUS-4KV-B` feeds `TR-480-B` and `TR-480-D` through `CB-211`/`CB-212`; PT taps are included for `PT-4160A/B`.
- 480 V distribution: `BUS-480-A/C/B/D` feed `MCC-1A/MCC-2A/MCC-1B/MCC-2B` through `CB-M1A`, `CB-M2A`, `CB-M1B`, and `CB-M2B`.
- MCC load chains: each visible feeder is represented as `MCC -> CB-Fxxx -> starter/fuse/disconnect -> named load`, including the spare chain `MCC-2A -> CB-F015 -> DS-F015 -> SPARE-A2`.
- DC/static inverter group: `MCC-2A/B` feed `CB-DC-1A/B` and `CHGR-125A/B`; batteries and chargers land on `DC-BUS-A/B`; `INV-1A/B` feed `ATS-INV`, which feeds `BUS-120VAC-ESF`.
- Ground references: `PNL-RPS-A -> GND-1` and `PNL-RPS-B -> GND-2` are high-confidence reference connections, not protective-ground network expansion.

## Ambiguity Hotspots

- Lower RPS/ESFAS/control area: dashed, dotted, and dash-dot routes converge around `TB-RPS-A/B`, `PNL-RPS-A/B`, `RELAY-27A/B`, `RELAY-50A/B`, and `RELAY-86A/B`. Crossings without dots were not promoted to high-confidence edges.
- Annunciator/SER routing: the note and dotted trunks support `ANN-480A/B`, `TB-ANN-1`, `PNL-ESFAS-A/B`, and `SEQ-REC-1` signal candidates, but exact terminal endpoints are partly obscured by long trunks and compact terminal-block geometry.
- 120 VAC ESF downstream taps: `BUS-120VAC-ESF` clearly exists and is fed by `ATS-INV`; candidate feeds to RPS/ESFAS panels and terminal blocks are visually plausible but placed in the plausible edge file.
- 4.16 kV interlocks: the dash-dot interlock spine across the top breaker row is visible, but individual breaker-to-breaker logical edges are inferred from adjacency to the routed spine and therefore kept plausible.
- Long vertical/horizontal control trunks from the top switchgear and PT regions descend toward the lower panels; only named endpoints with visual support were proposed, and unnamed wire-node points were omitted.
