# Round 01 Jennifer Precision Review Notes

## Source Boundary

Used only doc 22 raw/derived resources in `Input resources`, doc 22 `Codes and artifacts`, and Diego round 1 artifacts from `Results/Iteration_1`. I did not use ground truth, evaluator output, metric feedback, or anything derived from GT. The raw schematic was the primary evidence; overlays, wire masks, component labels, and crops were used only as aids.

## Node List Decision

Accepted Diego's node list unchanged.

- Kept all 181 detected physical components from `component_labels_list.csv`.
- Kept Diego's 14 visually printed bus nodes: `BUS-13A`, `BUS-13B`, `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-C`, `BUS-4160-D`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `BUS-125A`, `BUS-125B`, `BUS-UPS-A`, `BUS-UPS-B`.
- Kept Diego's five raw-visible D-train additions: `INST-PT-D`, `CB-CH-D`, `CB-VLV1-D`, `CB-VLV2-D`, `CB-SPARE-D`. Crop `18_inst_pt_d_raw.png` shows `INST-PT-D` tapped to `BUS-480-D`; crop `19_480_train_d_right_raw.png` shows the D-side breaker/load group including `CB-CH-D`, `CB-VLV1-D`, `CB-VLV2-D`, and `CB-SPARE-D`.
- Did not add section headers, voltage descriptions, title-block text, WN IDs, unlabeled junctions, or intermediate wire nodes.

## Edge Change Log

No matrix edge changes were made relative to Diego round 1.

- Removed edges: none.
- Added edges: none.
- Renamed/reordered nodes or edges: none.

The reviewed matrix is therefore structurally identical to `round_01_diego_matrix.csv`, with Jennifer review notes documenting the precision acceptance of the high-risk cases.

## High-Priority Review Evidence

### Dashed/protection/control paths kept

- Kept `BUS-13A -- RELAY-87U` and `RELAY-87U -- CB-4B-IN`. In `13_left_half_full_raw.png` and `03_4160_left_bus_area_raw.png`, the dashed C-031 path visibly leaves the 13.8 kV aux bus area, lands on `RELAY-87U`, and continues to the named `CB-4B-IN` breaker.
- Kept `SYNC-PNL-1 -- BUS-4160-A` and `SYNC-PNL-1 -- CB-DG-A`. In `03_4160_left_bus_area_raw.png`, dashed C-030 connections terminate at the synchronizing panel and the 4160 A / DG-A area with clear named endpoints.
- Kept `CB-RHR-* -- CB-SI-*` for A, B, C, and D trains. The 480 V train crops show short dashed links drawn directly between each RHR breaker and the matching SI breaker. The longer dashed continuation below the SI pumps has no clear named endpoint and remains excluded.
- Kept the 120 V panel-to-relay/JB/terminal dashed links. In the 480 train lower portions, each `PNL-120-*` has clear dashed terminations to its two relays and a dashed route to the matching junction box, followed by a clear JB-to-terminal dashed link.
- Kept lower RPS/PLC/annunciator dashed links where endpoints are clear: `BUS-UPS-A -- PNL-RPS-A`, `BUS-UPS-A -- PLC-SAF-A`, `BUS-UPS-A -- ANN-PNL-CR`, `PNL-RPS-A -- RELAY-RPS-A1`, `PNL-RPS-A -- RELAY-ESF-A`, `ANN-PNL-CR -- JB-CR-01`, `JB-CR-01 -- TERM-MTB-A`, `JB-CR-01 -- TERM-MTB-B`, and the analogous B-side `BUS-UPS-B` links to `PNL-RPS-B`, `PLC-SAF-B`, and `REC-SEQ-1` plus the two B relays.

### Long solid runs kept

- Kept `BUS-480-A -- CB-DC-A1`. In `13_left_half_full_raw.png`, a solid perimeter conductor leaves the left side of `BUS-480-A` and runs down to the `CB-DC-A1` / `CHGR-125A` area without a crossing-dot ambiguity.
- Kept `BUS-480-B -- CB-DC-B1`. The matching solid run is visible from the B load-center region down to `CB-DC-B1` in the left/right half and lower DC/UPS crops.

### 480 V MCC branch structure kept

- Kept the bus-to-incoming-breaker-to-MCC pattern for all MCCs and did not add breaker-to-breaker cliques. The raw crops show each `BUS-480-*` tap landing on a named `CB-MCC-*`, then on a named MCC block, with individual branches from the MCC block to load breakers.
- Kept the CT/RHR chain as `MCC-* -- INST-CT-* -- CB-RHR-*`, then `CB-RHR-* -- PUMP-RHR-*`; the CT appears on the RHR feeder path, and the named endpoints are visible.

### Top generation/switchyard kept

- Kept `GEN-G01 -- GSU-T01`, `GSU-T01 -- SWYD-345`, and the two switchyard breaker connections `SWYD-345 -- CB-13A1` and `SWYD-345 -- CB-13B1`. The top raw crops show the generator step-up path to the switchyard and separate switchyard-connected breaker drops.
- Kept `CB-13T -- BUS-13A` and `CB-13T -- BUS-13B`; the tie breaker is drawn between the two printed 13.8 kV aux buses.

### Grounds kept narrowly

- Kept only the printed bus/rail ground attachments: `GND-A/B/C/D -- BUS-480-A/B/C/D` and `GRD-DC-A/B -- BUS-125A/B`. The raw crops show these symbols connected to the adjacent bus/rail conductors, and no extra nearby component ground edges were added.

### Lower DC/UPS buses kept

- Kept the `BUS-125A/B` attachments to batteries, chargers, DC MCCs, diode blocks, fuses, and DC grounds. The lower DC/UPS crop shows each of these as a direct tap from the printed 125 VDC bus.
- Kept the `BUS-UPS-A/B` attachments to inverters, instrument racks, PLC/RPS panels, annunciator/recorder endpoints, and the related JB/terminal links where the dashed or solid path lands on a named endpoint.
- Kept `XFMR-PT-1 -- METER-V01` and `XFMR-PT-1 -- METER-A01`; the transformer-to-meter dashed lines are visually clear in the lower right control area.

## Remaining Uncertain Cases

- Included the clear dashed/control paths listed above because both named endpoints are visible. These remain lower-confidence than short solid feeder edges, but they are visually supported.
- Deliberately excluded the longer dashed continuations below SI pump branches because they do not land on another clear named endpoint within the reviewed node list.
- Deliberately excluded crossings without dots and all unlabeled junctions/WN IDs, following the schematic note that crossings without dots are not connected.
- Deliberately represented printed buses as bus nodes rather than expanding all same-bus components into pairwise component cliques.

## Validation Summary

- Node count: 200
- Edge count: 207 unique undirected edges
- Symmetric: True
- Diagonal zero: True
- Rows and columns same names/order: True
- Isolated nodes: none
