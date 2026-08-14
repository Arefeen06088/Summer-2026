# Round 01 Diego Connectivity Notes

Scope: derived from the doc31 raw schematic and the listed doc31 artifacts/crops only. The raw PNG was treated as authoritative; overlays and inventories were used only as visual aids.

## Node List Rationale

- Matrix node order is the 169 inventory labels from `component_labels_list.csv`, followed by visible non-inventory endpoints/components that act as connection endpoints.
- Total nodes: 189. Inventory nodes represented with at least one edge: 169 of 169.
- Added visible/non-inventory endpoints: OPC-101, HV-101, SUH-201, QH-203, LV-401, SP-401, OPC-905, OPC-90_AUX_VENT, OPC-50_SW_SUPPLY, OPC-50_SW_RETURN, OPC-40_SUPPLY_HDR, OPC-40_CCW_RETURN, OPC-90_INST_AIR, OPC-90_DCS_LINK, OPC-90_DRAIN_SUMP, MOV-401, PCV-401, LSH-401, LSL-401, MOV-402.
- The repeated/truncated visible OPC labels were service-qualified in node names so distinct off-page connectors are not merged: `OPC-90_AUX_VENT`, `OPC-90_INST_AIR`, `OPC-90_DCS_LINK`, `OPC-90_DRAIN_SUMP`, `OPC-50_SW_SUPPLY`, `OPC-50_SW_RETURN`, `OPC-40_SUPPLY_HDR`, and `OPC-40_CCW_RETURN`.
- `SUH-201`, `FH-301`, `DIH-201`, `COH-301`, `DH-401`, `RTH-401`, `CHH-601`, `IAH-101`, `WTH-101`, `DRH-101`, `SWS-501`, `SWR-501`, and `VTH-101` were treated as named headers or named header-like endpoint blocks where visible.
- `QH-203` was included as a named recirc return tie because the label is drawn at a filled-dot connection to the pump suction header; this is more explicit than creating an anonymous junction node.

## Edge Evidence By Region

### Aux vent and closed drain headers
- `VTH-101` -- `PI-901`: PI bubble taps the VTH-101 aux vent header.
- `VTH-101` -- `OPC-90_AUX_VENT`: Aux vent header runs right to visible OPC-90 off-page connector.
- `DRH-101` -- `PI-902`: PI bubble taps the DRH-101 closed drain header.
- `DRH-101` -- `OPC-90_DRAIN_SUMP`: Closed drain header line continues right to drain-sump OPC-90 connector.

### TK-101 makeup and surge tank
- `OPC-101` -- `HV-101`: Makeup line enters from OPC-101 through visible manual valve HV-101.
- `HV-101` -- `STR-101`: Makeup pipe continues from HV-101 into makeup strainer STR-101.
- `STR-101` -- `FCV-101`: Strainer outlet pipe runs directly to FCV-101.
- `FCV-101` -- `TK-101`: FCV-101 outlet pipe enters TK-101 side nozzle.
- `FT-101` -- `STR-101`: FT-101 dashed/tap line lands on makeup pipe at the strainer outlet region.
- `FT-101` -- `FIC-101`: Dashed instrument signal links FT-101 to FIC-101.
- `FIC-101` -- `FCV-101`: Dashed control signal from FIC-101 reaches FCV-101 actuator.
- `LT-101` -- `TK-101`: Dashed level transmitter line ties LT-101 to TK-101.
- `LT-101` -- `LIC-101`: Dashed signal connects LT-101 to LIC-101.
- `LIC-101` -- `FCV-101`: LIC-101 dashed control path reaches the FCV-101 actuator loop.
- `LSHH-101` -- `TK-101`: Dashed high-high level switch line lands on TK-101.
- `LSLL-101` -- `TK-101`: Dashed low-low level switch line lands on TK-101.
- `LG-101` -- `TK-101`: LG-101 gauge is shown with a dashed connection to TK-101.
- `PI-101` -- `TK-101`: PI-101 dashed pressure tap lands on the lower tank/nozzle area.
- `TK-101` -- `VT-101`: Tank top slanted vent/relief line reaches VT-101.
- `TK-101` -- `PSV-101`: Tank top vertical vent line reaches PSV-101.
- `PSV-101` -- `HV-103`: PSV-101 outlet line turns to the visible HV-103 valve.
- `TK-101` -- `SV-101`: Side sample/utility line leaves TK-101 through SV-101.
- `SV-101` -- `AT-101`: Dashed analyzer/sample signal connects SV-101 to AT-101.
- `TK-101` -- `HV-102`: Tank bottom outlet pipe goes through HV-102.
- `HV-102` -- `RD-101`: Horizontal branch downstream of HV-102 goes to RD-101.
- `HV-102` -- `DV-101`: Bottom drain leg continues from HV-102 to DV-101.
- `RD-101` -- `SUH-201`: RD-101 outlet ties into the vertical suction header SUH-201.
- `SUH-201` -- `PI-102`: PI-102 taps the pump suction header near SUH-201.
- `SUH-201` -- `TI-102`: TI-102 taps the pump suction header near SUH-201.
- `SUH-201` -- `HV-201A`: Suction header branch to train A starts through HV-201A.
- `SUH-201` -- `HV-201B`: Suction header branch to train B starts through HV-201B.
- `SUH-201` -- `QH-203`: Filled-dot recirc return tie labeled QH-203 joins the suction header.

### P-201A/B pump trains and discharge header
- `HV-201A` -- `STR-201A`: Train A suction line continues from HV-201A to STR-201A.
- `STR-201A` -- `P-201A`: Train A strainer outlet feeds P-201A.
- `PI-201A` -- `STR-201A`: PI-201A taps the train A suction strainer region.
- `P-201A` -- `PT-201A`: PT-201A dashed pressure tap lands on P-201A/top discharge tap.
- `PT-201A` -- `VT-201A`: VT-201A is on the same top tap above PT-201A.
- `P-201A` -- `DV-201A`: Bottom drain leg from P-201A reaches DV-201A.
- `P-201A` -- `CKV-201A`: P-201A discharge pipe runs to CKV-201A.
- `CKV-201A` -- `MOV-201A`: Train A discharge continues from CKV-201A to MOV-201A.
- `MOV-201A` -- `DIH-201`: MOV-201A outlet ties into the DIH-201 pump discharge header.
- `HV-201B` -- `STR-201B`: Train B suction line continues from HV-201B to STR-201B.
- `STR-201B` -- `P-201B`: Train B strainer outlet feeds P-201B.
- `PI-201B` -- `STR-201B`: PI-201B taps the train B suction strainer region.
- `P-201B` -- `PT-201B`: PT-201B dashed pressure tap lands on P-201B/top discharge tap.
- `PT-201B` -- `VT-201B`: VT-201B is on the same top tap above PT-201B.
- `P-201B` -- `DV-201B`: Bottom drain leg from P-201B reaches DV-201B.
- `P-201B` -- `CKV-201B`: P-201B discharge pipe runs to CKV-201B.
- `CKV-201B` -- `MOV-201B`: Train B discharge continues from CKV-201B to MOV-201B.
- `MOV-201B` -- `DIH-201`: MOV-201B outlet ties into the DIH-201 pump discharge header.
- `DV-201B` -- `QH-203`: Lower recirc/tie line passes through the DV-201B drain/tie area and QH-203.
- `DIH-201` -- `PI-203`: PI-203 taps the pump discharge header near the upper branch.
- `PI-203` -- `TI-203`: PI-203 is shown with a dashed instrument link to TI-203.
- `DIH-201` -- `IQ-601`: Chemical injection quill IQ-601 is on the pump discharge header branch.
- `IQ-601` -- `FH-301`: Pipe continues from IQ-601 into FH-301 filter inlet header.
- `DIH-201` -- `HV-203`: Lower pump-discharge/recirc branch leaves DIH-201 through HV-203.

### FH-301 filter inlet and FLT/HX-301A/B branches
- `FH-301` -- `PI-310`: PI-310 taps the filter inlet header above FH-301.
- `FH-301` -- `HV-301A`: Upper A branch leaves FH-301 through HV-301A.
- `FH-301` -- `HV-301B`: Lower B branch leaves FH-301 through HV-301B.
- `FH-301` -- `FT-203`: FT-203 sits on/taps the lower filter inlet header leg.
- `FH-301` -- `HV-203`: Lower inlet/recirc line is visually tied near FH-301 and HV-203.
- `FT-203` -- `FIC-203`: Dashed flow signal links FT-203 and FIC-203.
- `FIC-203` -- `FCV-203`: Dashed control signal links FIC-203 to FCV-203.
- `HV-301A` -- `FLT-301A`: A-side inlet valve feeds FLT-301A.
- `FLT-301A` -- `HV-302A`: FLT-301A outlet pipe reaches HV-302A.
- `HV-302A` -- `HX-301A`: HV-302A outlet pipe feeds HX-301A.
- `HX-301A` -- `HV-303A`: HX-301A outlet goes through HV-303A.
- `HV-303A` -- `COH-301`: A outlet line drops/continues to COH-301 cooler outlet header.
- `FLT-301A` -- `PI-301A`: PI-301A taps FLT-301A.
- `FLT-301A` -- `PDT-301A`: PDT-301A taps FLT-301A top differential-pressure connection.
- `PDT-301A` -- `VT-301A`: VT-301A is on the same top tap as PDT-301A.
- `FLT-301A` -- `DV-301A`: FLT-301A bottom drain reaches DV-301A.
- `HX-301A` -- `TT-301A`: TT-301A dashed temperature tap lands on HX-301A.
- `HX-301A` -- `TI-301A`: TI-301A taps the HX-301A outlet/adjacent line.
- `HX-301A` -- `PSV-301A`: PSV-301A relief branch is drawn from HX-301A.
- `HV-301B` -- `FLT-301B`: B-side inlet valve feeds FLT-301B.
- `FLT-301B` -- `HV-302B`: FLT-301B outlet pipe reaches HV-302B.
- `HV-302B` -- `HX-301B`: HV-302B outlet pipe feeds HX-301B.
- `HX-301B` -- `HV-303B`: HX-301B outlet goes through HV-303B.
- `HV-303B` -- `COH-301`: B outlet line continues to COH-301 cooler outlet header.
- `FLT-301B` -- `PI-301B`: PI-301B taps FLT-301B.
- `FLT-301B` -- `PDT-301B`: PDT-301B taps FLT-301B top differential-pressure connection.
- `PDT-301B` -- `VT-301B`: VT-301B is on the same top tap as PDT-301B.
- `FLT-301B` -- `DV-301B`: FLT-301B bottom drain reaches DV-301B.
- `HX-301B` -- `TT-301B`: TT-301B dashed temperature tap lands on HX-301B.
- `HX-301B` -- `TI-301B`: TI-301B taps the HX-301B outlet/adjacent line.
- `HX-301B` -- `PSV-301B`: PSV-301B relief branch is drawn from HX-301B.

### Bypass, recirc, and RTH-401 return header
- `HV-203` -- `FCV-203`: Recirc/bypass line continues from HV-203 through FCV-203.
- `FCV-203` -- `CKV-203`: Same line continues from FCV-203 to CKV-203.
- `CKV-203` -- `HV-310`: Bypass/check-valve leg visually joins the HV-310 branch.
- `HV-310` -- `FCV-310`: Bypass line continues from HV-310 to FCV-310.
- `FCV-310` -- `HV-311`: Bypass line continues from FCV-310 through HV-311.
- `HV-311` -- `RTH-401`: HV-311 outlet ties into RTH-401 return header.
- `FCV-310` -- `HV-403`: Vertical/parallel bypass arrangement links FCV-310 area to HV-403 return leg.
- `HV-403` -- `CKV-402`: Lower return leg continues from HV-403 to CKV-402.
- `CKV-402` -- `RTH-401`: Lower return leg ties into RTH-401.
- `QH-203` -- `HV-203`: Recirc return tie line and HV-203 lower branch are visually continuous.
- `FT-310` -- `FCV-310`: FT-310 taps the FCV-310 bypass line.
- `FT-310` -- `FIC-310`: Dashed flow signal links FT-310 and FIC-310.
- `FIC-310` -- `FCV-310`: Dashed control signal links FIC-310 to FCV-310.

### COH-301, DH-401, V-401, and supply controls
- `COH-301` -- `FCV-401`: Cooler outlet header feeds FCV-401.
- `FCV-401` -- `DH-401`: FCV-401 outlet feeds DH-401 supply header.
- `DH-401` -- `MOV-401`: Supply header outlet passes through visible MOV-401.
- `MOV-401` -- `OPC-40_SUPPLY_HDR`: MOV-401 discharge goes to the supply-header OPC-40 connector.
- `COH-301` -- `FT-401`: FT-401 taps the cooler outlet line near COH-301.
- `FT-401` -- `FIC-401`: Dashed flow signal links FT-401 and FIC-401.
- `FIC-401` -- `FCV-401`: Dashed control signal links FIC-401 to FCV-401.
- `DH-401` -- `PT-401`: PT-401 taps the DH-401/supply header region.
- `PT-401` -- `PIC-401`: Dashed pressure signal links PT-401 and PIC-401.
- `PIC-401` -- `PCV-401`: Dashed pressure-control signal links PIC-401 to PCV-401.
- `DH-401` -- `PCV-401`: Bypass/pressure-control branch leaves DH-401 through PCV-401.
- `PCV-401` -- `RTH-401`: PCV-401 return branch ties back toward the RTH-401 return header.
- `COH-301` -- `RTH-401`: Vertical cooler outlet/return trunk visually connects COH-301 and RTH-401.
- `DH-401` -- `HV-430`: Vertical connection from DH-401 rises through HV-430 toward V-401.
- `HV-430` -- `V-401`: HV-430 continues to V-401 air separator bottom connection.
- `V-401` -- `DV-401`: Small V-401 drain/utility branch reaches DV-401.
- `FI-401` -- `MOV-401`: FI-401 dashed indication line is tied to the MOV-401/outlet area.
- `V-401` -- `LT-401`: LT-401 dashed level tap lands on V-401.
- `V-401` -- `LSH-401`: LSH-401 dashed switch line lands on V-401.
- `V-401` -- `LSL-401`: LSL-401 dashed switch line lands on V-401.
- `LT-401` -- `LIC-401`: Dashed level signal links LT-401 and LIC-401.
- `LIC-401` -- `LV-401`: LIC-401 dashed control signal reaches LV-401.
- `V-401` -- `LV-401`: V-401 side/bottom level-control branch reaches LV-401.
- `LV-401` -- `STR-402`: LV-401 outlet/return line turns into the return-strainer line.

### SWS-501/SWR-501 service-water controls
- `OPC-50_SW_SUPPLY` -- `VT-401`: S.W. supply off-page connector feeds the visible VT-401 valve.
- `VT-401` -- `SWS-501`: VT-401 outlet line enters SWS-501 supply header.
- `SWS-501` -- `PT-501`: PT-501 pressure tap lands on SWS-501.
- `PT-501` -- `PIC-501`: Dashed pressure signal links PT-501 to PIC-501.
- `PIC-501` -- `PCV-501`: Dashed pressure-control signal reaches PCV-501.
- `SWS-501` -- `PSV-401`: PSV-401 relief branch is drawn below/at SWS-501.
- `PSV-401` -- `V-401`: PSV-401 branch continues toward the V-401 separator connection.
- `V-401` -- `PCV-501`: V-401/S.W. return branch passes through PCV-501.
- `PCV-501` -- `SWR-501`: PCV-501 ties into SWR-501 return header.
- `SWR-501` -- `OPC-50_SW_RETURN`: SWR-501 return line continues to S.W. return OPC-50 connector.
- `V-401` -- `VT-401`: Vertical V-401 service-water connection visually meets the VT-401 line.
- `SWS-501` -- `FT-511A`: FT-511A sits on/taps the SWS supply branch.
- `FT-511A` -- `FIC-511A`: Dashed flow signal links FT-511A and FIC-511A.
- `FIC-511A` -- `FCV-511A`: Dashed control signal links FIC-511A to FCV-511A.
- `FT-511A` -- `FCV-511A`: FT-511A branch is adjacent to the FCV-511A flow-control leg.
- `FCV-511A` -- `HV-511A`: Service-water branch continues from FCV-511A to HV-511A.
- `HV-511A` -- `HX-301A`: HV-511A branch descends/continues to HX-301A service side.
- `PI-511A` -- `HV-511A`: PI-511A taps the upper service-water branch near HV-511A.
- `HX-301A` -- `HV-511B`: HX-301A service-water return/parallel branch reaches HV-511B.
- `HV-511B` -- `FT-511B`: HV-511B branch is adjacent to FT-511B return/tap.
- `FT-511B` -- `FIC-511B`: Dashed flow signal links FT-511B and FIC-511B.
- `FIC-511B` -- `FCV-511B`: Dashed control signal links FIC-511B to FCV-511B.
- `FT-511B` -- `FCV-511B`: FT-511B branch is adjacent to FCV-511B.
- `FCV-511B` -- `SWR-501`: FCV-511B outlet/return branch ties to SWR-501.
- `PI-511B` -- `HV-511B`: PI-511B taps the lower service-water branch near HV-511B.
- `HX-301B` -- `HV-511B`: Shared lower service-water/cooler return manifold is visually adjacent to HX-301B and HV-511B.
- `HX-301B` -- `FCV-511B`: Shared service-water branch continues toward FCV-511B.
- `SWR-501` -- `HV-512A`: Vertical branch below SWR-501 reaches HV-512A.
- `HV-512A` -- `COH-301`: HV-512A branch drops toward COH-301/cooler outlet area.
- `TI-512A` -- `HV-512A`: TI-512A dashed/tap line lands near HV-512A.
- `TIC-310` -- `TI-512A`: TIC-310 dashed temperature-control line connects to TI-512A.
- `TIC-310` -- `TT-310`: TIC-310 is connected by dashed signal to TT-310.
- `TT-310` -- `COH-301`: TT-310 taps the cooler outlet/supply control line near COH-301.
- `SWR-501` -- `HV-512B`: Lower vertical branch from SWR-501/HX area reaches HV-512B.
- `HV-512B` -- `HV-303A`: HV-512B branch meets the HV-303A outlet manifold area.
- `PI-320` -- `HV-512B`: PI-320 taps the HV-512B vertical branch.
- `TI-512B` -- `HV-512B`: TI-512B taps the lower service-water/return branch.
- `TIC-310` -- `HV-512B`: Dashed TIC-310 control line extends to the HV-512B branch.

### Return strainer and return sample
- `OPC-40_CCW_RETURN` -- `MOV-402`: CCW return enters from OPC-40 through visible MOV-402.
- `MOV-402` -- `STR-402`: MOV-402 outlet line feeds return strainer STR-402.
- `STR-402` -- `HV-402`: STR-402 outlet line goes through HV-402.
- `HV-402` -- `RTH-401`: HV-402 outlet ties into RTH-401 return header.
- `STR-402` -- `PT-402`: PT-402 dashed/tap line lands on STR-402 return strainer.
- `STR-402` -- `TI-402`: TI-402 dashed/tap line lands on STR-402 return strainer/outlet.
- `STR-402` -- `SV-401`: Return-sample branch leaves STR-402/HV-402 area through SV-401.
- `SV-401` -- `SP-401`: SV-401 sample line reaches visible SP-401 sample point.
- `SP-401` -- `SAM-101`: Sample line from SP-401 continues across the sheet to SAM-101 sample panel.

### TK-601 chemical dosing and sample panel
- `OPC-905` -- `HV-610`: Demin water makeup enters from OPC-905 through HV-610.
- `HV-610` -- `FCV-610`: Demin makeup line continues from HV-610 to FCV-610.
- `FCV-610` -- `TK-601`: FCV-610 outlet line enters TK-601.
- `FCV-610` -- `LIC-601`: LIC-601 dashed control signal reaches FCV-610.
- `LIC-601` -- `LT-601`: LIC-601 receives dashed level signal from LT-601.
- `LT-601` -- `TK-601`: LT-601 dashed tap lands on TK-601.
- `TK-601` -- `LSH-601`: LSH-601 dashed switch line lands on TK-601.
- `TK-601` -- `LSL-601`: LSL-601 dashed switch line lands on TK-601.
- `TK-601` -- `VT-601`: TK-601 top vent line reaches VT-601.
- `TK-601` -- `DV-601`: TK-601 bottom drain reaches DV-601.
- `TK-601` -- `HV-602A`: A chemical pump suction leaves TK-601 through HV-602A.
- `HV-602A` -- `P-601A`: HV-602A outlet feeds P-601A.
- `P-601A` -- `CKV-601A`: P-601A discharge goes to CKV-601A.
- `CKV-601A` -- `HV-603A`: A discharge line continues from CKV-601A to HV-603A.
- `HV-603A` -- `CHH-601`: A discharge line ties into CHH-601 chemical discharge header.
- `TK-601` -- `HV-602B`: B chemical pump suction leaves TK-601 through HV-602B.
- `HV-602B` -- `P-601B`: HV-602B outlet feeds P-601B.
- `P-601B` -- `CKV-601B`: P-601B discharge goes to CKV-601B.
- `CKV-601B` -- `HV-603B`: B discharge line continues from CKV-601B to HV-603B.
- `HV-603B` -- `CHH-601`: B discharge line ties into CHH-601 chemical discharge header.
- `CHH-601` -- `FT-601`: FT-601 taps the CHH-601 chemical header region.
- `FT-601` -- `FIC-601`: Dashed flow signal links FT-601 and FIC-601.
- `FIC-601` -- `FCV-601`: Dashed control signal links FIC-601 to FCV-601.
- `CHH-601` -- `FCV-601`: Chemical discharge header outlet goes through FCV-601.
- `FCV-601` -- `RD-601`: FCV-601 outlet/relief loop reaches RD-601.
- `RD-601` -- `PSV-601`: RD-601 loop connects to PSV-601 pulsation protector branch.
- `PSV-601` -- `PI-601`: PI-601 pressure indication taps PSV-601/pulsation protector branch.
- `RD-601` -- `IQ-601`: Chemical injection line continues from RD-601 toward IQ-601.
- `FCV-601` -- `FI-601`: FCV-601 outlet/main chemical-injection line is adjacent to FI-601.
- `FI-601` -- `PI-602`: PI-602 taps the same downstream injection/main line as FI-601.
- `CHH-601` -- `SV-601`: Chemical sample branch leaves CHH-601 through SV-601.
- `SV-601` -- `SP-601`: SV-601 sample branch reaches SP-601.
- `SP-601` -- `SAM-101`: SP-601 sample point line enters SAM-101 panel.
- `PH-601` -- `SP-601`: PH-601 dashed analyzer/sample connection lands on SP-601.
- `SAM-101` -- `WTH-101`: SAM-101 drain/waste line feeds WTH-101 waste sample/drain trough.

### MCC, CP, PLC, DCS, junction boxes, and instrument air
- `REG-601` -- `IAH-101`: Instrument-air line passes through REG-601 into IAH-101.
- `IAH-101` -- `OPC-90_INST_AIR`: IAH-101 instrument air header continues to visible OPC-90 connector.
- `JB-101` -- `CP-101`: Dashed control wiring links JB-101 to CP-101.
- `JB-102` -- `PLC-101`: Dashed control wiring links JB-102 to PLC-101.
- `PLC-101` -- `DCS-001`: Dashed signal line connects PLC-101 to DCS-001.
- `PLC-101` -- `OPC-90_DCS_LINK`: Dashed DCS link exits PLC-101 to the OPC-90 connector.
- `HS-201A` -- `MCC-201`: Dashed hand-switch signal from HS-201A lands on MCC-201.
- `HS-201B` -- `MCC-201`: Dashed hand-switch signal from HS-201B lands on MCC-201.

## Ambiguous Or Uncertain Cases

- The service-water manifold around `SWS-501`, `SWR-501`, `FCV-511A/B`, `HV-511A/B`, `HV-512A/B`, and the two `HX-301` coolers is dense. I included visually plausible local adjacencies and control/tap edges, but avoided expanding the SWS/SWR headers into all-to-all cooler/control cliques.
- The lower recirc/bypass area around `HV-203`, `FCV-203`, `CKV-203`, `HV-310`, `FCV-310`, `HV-311`, `HV-403`, `CKV-402`, and `RTH-401` has close parallel lines. I encoded the visible local path segments and the named `QH-203` tie rather than anonymous intermediate elbows.
- `LV-401`, `PCV-401`, `MOV-401`, `MOV-402`, `LSH-401`, and `LSL-401` are visible on the raw drawing but absent from the supplied component inventory, so they were added as named nodes.
- Several OPC labels are visibly repeated or partly truncated at the arrowhead. They were not merged because they terminate different services on the drawing.
- Some dashed controller loops, especially `LIC-101`/`FIC-101` to `FCV-101` and `TIC-310` to the 512 valves, are interpreted as direct endpoint signal connections where the dashed path visibly lands on the target symbol/actuator.

## Labels Not Included

- No `WN-*` wire nodes, anonymous elbows, anonymous t-sections, crossing points, or unfilled line crossings were included.
- Line-number-only labels such as `4"-CCW-...`, `6"-SW-...`, `1"-CHM-...`, `1/2"-SMP-...`, and `3/4"-DR-...` were not treated as nodes.
- Small motor boxes marked `M`, grid labels, title/revision/general-note text, flow arrows, and legend symbols were not included.
- Descriptive text without a unique tag, such as plain `PUMP DISCHARGE HEADER`, `FILTER INLET HEADER`, `CCW RETURN`, or `S.W. SUPPLY`, was represented only by the adjacent named endpoint when present, not as a separate node.

## Basic Validation

- Node count: 189
- Edge count: 214
- Diagonal check: pass
- Symmetry check: pass
- Isolated nodes: 0
