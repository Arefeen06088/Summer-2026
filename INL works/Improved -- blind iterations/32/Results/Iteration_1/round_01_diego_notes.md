# Round 01 Diego Connectivity Notes

## Scope And Method

I inspected only the doc32 raw image and the supplied doc32 artifact crops/overlays listed in the request. The raw schematic was treated as authoritative. Solid process/utility piping was used for process adjacency, and dashed/dot-dashed lines were used only where they visibly terminate at named instruments, controls, off-page connectors, or named header/control boxes. Filled dots were treated as true junctions; line crossings without filled dots were not expanded into connections.

## Node List Rationale

The matrix includes all 166 named physical components from `component_labels_list.csv`, because each is visually part of a process, utility, drain/vent, or signal/control connection. I added named non-inventory endpoints where the drawing uses them as real connection endpoints: `OPC-IA-501`, `HDR-IA-501`, `OPC-DMW-501`, `OPC-CHM-501`, `OPC-VENT-501`, `OPC-SMP-501`, `HDR-SUC-501`, `HDR-DIS-501`, `HDR-SUP-501`, `HDR-RET-501`, `HDR-DRN-501`, `OPC-SW-IN-501`, `OPC-SW-OUT-501`, `HDR-SW-SUP-501`, `HDR-SW-RET-501`, `HDR-VENT-501`, `OPC-DRN-501`, `DCS-501`.

I did not include anonymous wire-node IDs, crop IDs, bend/elbow points, line-number-only labels such as `6"-CCW-550-C1`, repeated text-only area titles, or unlabelled junction/t-section symbols. The long supply, discharge, return, service-water, drain, and vent runs are represented by named header/off-page nodes instead of synthetic branch nodes.

## Edge Evidence By Region

### Top Utility/Header Lines
- `OPC-IA-501` -- `HDR-IA-501`: Solid top instrument-air run from OPC-IA-501 to HDR-IA-501.

### Left TK-501 / V-501 / Makeup / Chemical / Sample
- `OPC-DMW-501` -- `HV-501`: Demineralized-water makeup enters through OPC-DMW-501 then HV-501.
- `HV-501` -- `PRV-501`: Same horizontal makeup line continues from HV-501 to PRV-501.
- `PRV-501` -- `LCV-501`: Same horizontal makeup line continues from PRV-501 to LCV-501.
- `LCV-501` -- `CV-501`: Same horizontal makeup line continues from LCV-501 to CV-501.
- `CV-501` -- `TK-501`: CV-501 outlet drops/returns visually toward the surge tank inlet line.
- `LIC-501` -- `LCV-501`: Dashed level-control signal from LIC-501 to LCV-501.
- `LIC-501` -- `LT-501`: Level control loop visually associated with LT-501/LIC-501 in tank area.
- `HV-501` -- `HV-503`: Filled-dot branch from the makeup line down to vent valve HV-503.
- `PRV-501` -- `HV-503`: HV-503 branch shares the makeup segment near the HV-501/PRV-501 span.
- `HV-503` -- `HDR-VENT-501`: HV-503 is on the labeled 2-inch VENT-501 branch to the vent header.
- `HV-503` -- `OPC-VENT-501`: Visible OPC-VENT-501 box marked to vent header near the local vent branch.
- `PRV-501` -- `PSV-501`: Relief branch drops from the PRV/LCV makeup segment to PSV-501.
- `PSV-501` -- `LCV-501`: PSV-501 branch is attached at the filled dot between PRV-501 and LCV-501.
- `PSV-501` -- `TK-501`: PSV-501 relief/return leg visually drops toward the tank top.
- `PSV-501` -- `HDR-VENT-501`: PSV-501 uses the nearby 2-inch vent/relief header convention.
- `OPC-CHM-501` -- `TK-501`: Corrosion inhibitor off-page connector feeds the tank-side chemical line.
- `OPC-CHM-501` -- `LIC-501`: OPC-CHM-501 callout touches the LIC/local control symbol area; treated as supported logical adjacency.
- `TK-501` -- `HV-506`: Chemical/circulation line leaves the tank top through HV-506.
- `HV-506` -- `P-503`: Solid 3/4-inch CHM-501-A1 line runs from HV-506 to P-503.
- `P-503` -- `CV-503`: P-503 discharge continues to check valve CV-503.
- `CV-503` -- `TK-501`: CV-503 outlet loops back on CHM-503-A1 toward the tank.
- `PT-501` -- `TK-501`: PT-501 has a dashed tap to the surge tank wall/top line.
- `PT-501` -- `PAH-501`: PAH-501 is signal-linked to PT-501 by dashed line.
- `LT-501` -- `TK-501`: LT-501 has a dashed level tap to the tank.
- `LT-501` -- `LAH-501`: LAH-501 is linked to the tank level transmitter path.
- `LT-501` -- `LAL-501`: LAL-501 is linked to the tank level transmitter path.
- `TK-501` -- `TI-501`: TI-501 sits on the tank bottom/side drain leg.
- `TK-501` -- `PI-501`: Tank outlet/sample line passes through the PI-501 tap.
- `PI-501` -- `V-501`: PI-501 is on the solid line between TK-501 and V-501.
- `TK-501` -- `V-501`: Solid equalizing/process line directly spans tank to air separator region.
- `V-501` -- `HV-502`: V-501 bottom outlet goes through HV-502.
- `HV-502` -- `HDR-SUC-501`: HV-502 outlet enters the named suction header line.
- `TK-501` -- `HDR-SUC-501`: Tank bottom 6-inch CCW-593-C1 line ties to HDR-SUC-501.
- `TK-501` -- `HV-504`: Tank drain leg drops through HV-504.
- `HV-504` -- `HDR-DRN-501`: HV-504 drain is labeled DRN-501-A1 toward the drain header.
- `V-501` -- `SP-501`: Sample point SP-501 is drawn on the V-501 local sample/side connection.
- `SP-501` -- `OPC-SMP-501`: Dashed sample line from SP-501 goes to OPC-SMP-501/sample sink.
- `V-501` -- `SV-501`: SV-501 is on the local dashed sample/service line adjacent to V-501.
- `SV-501` -- `SP-501`: SV-501 dashed outlet points to the SP-501 sample point.
- `V-501` -- `ORF-520`: V-501 return line labeled CCW-523-R1 descends to the pump recycle/ORF-520 area.

### P-501A/B Pump Trains And Recycle
- `HDR-SUC-501` -- `HV-510A`: A suction branch leaves HDR-SUC-501 through HV-510A.
- `HV-510A` -- `STR-510A`: A train solid suction line continues from HV-510A to STR-510A.
- `STR-510A` -- `P-501A`: A train strainer outlet feeds P-501A.
- `P-501A` -- `CV-510A`: P-501A discharge goes to CV-510A.
- `CV-510A` -- `MOV-511A`: A train line continues from CV-510A to MOV-511A.
- `MOV-511A` -- `PI-520`: A discharge line includes PI-520 after MOV-511A.
- `PI-520` -- `HV-511A`: A discharge line continues from PI-520 to HV-511A.
- `HV-511A` -- `HDR-DIS-501`: A train joins the common discharge manifold after HV-511A.
- `PSLL-510A` -- `HV-510A`: PSLL-510A dashed suction-low signal is tied to A suction branch.
- `PI-510A` -- `P-501A`: PI-510A dashed pressure tap is associated with P-501A/discharge.
- `STR-510A` -- `DV-510A`: A strainer drain drops to DV-510A.
- `DV-510A` -- `HDR-DRN-501`: DV-510A drain leg leaves toward the common drain header.
- `HDR-SUC-501` -- `HV-510B`: B suction branch leaves HDR-SUC-501 through HV-510B.
- `HV-510B` -- `STR-510B`: B train solid suction line continues from HV-510B to STR-510B.
- `STR-510B` -- `P-501B`: B train strainer outlet feeds P-501B.
- `P-501B` -- `CV-510B`: P-501B discharge goes to CV-510B.
- `CV-510B` -- `MOV-511B`: B train line continues from CV-510B to MOV-511B.
- `MOV-511B` -- `HV-511B`: B discharge line continues from MOV-511B to HV-511B.
- `HV-511B` -- `HDR-DIS-501`: B train joins the common discharge manifold after HV-511B.
- `PSLL-510B` -- `HV-510B`: PSLL-510B dashed suction-low signal is tied to B suction branch.
- `PI-510B` -- `P-501B`: PI-510B dashed pressure tap is associated with P-501B/discharge.
- `STR-510B` -- `DV-510B`: B strainer drain drops to DV-510B.
- `DV-510B` -- `HDR-DRN-501`: DV-510B drain leg leaves toward the common drain header.
- `HDR-DIS-501` -- `HV-520`: Recycle/return branch leaves common discharge through HV-520.
- `HV-520` -- `PCV-520`: Recycle line continues from HV-520 to PCV-520.
- `PCV-520` -- `ORF-520`: Recycle line continues from PCV-520 to ORF-520.
- `ORF-520` -- `HDR-SUC-501`: Recycle/minimum-flow branch returns toward the suction/return side near the suction header.
- `PIC-520` -- `PCV-520`: Dashed pressure-control signal from PIC-520 to PCV-520.
- `PIC-520` -- `PT-520`: PIC-520 has dashed signal association with PT-520.
- `PT-520` -- `HDR-DIS-501`: PT-520 taps the common discharge header.
- `HDR-DIS-501` -- `FT-521`: FT-521 taps the common discharge/transfer header.
- `FT-521` -- `FI-521`: Dashed flow signal from FT-521 to FI-521.

### Center Filter / Heat Exchanger Trains
- `HDR-DIS-501` -- `HV-530A`: A filter train branches from HDR-DIS-501 through HV-530A.
- `HV-530A` -- `FLT-501A`: A train line enters FLT-501A after HV-530A.
- `FLT-501A` -- `HV-531A`: A train line exits FLT-501A to HV-531A.
- `HV-531A` -- `HX-501A`: A train line enters HX-501A after HV-531A.
- `HX-501A` -- `MOV-532A`: A train outlet leaves HX-501A through MOV-532A.
- `MOV-532A` -- `HDR-SUP-501`: A train outlet ties into the named supply/distribution header.
- `FLT-501A` -- `VV-530A`: Vent valve VV-530A is drawn above FLT-501A.
- `FLT-501A` -- `DV-530A`: Drain valve DV-530A is drawn below FLT-501A.
- `HX-501A` -- `VV-540A`: Vent valve VV-540A is drawn above HX-501A.
- `HX-501A` -- `DV-540A`: Drain valve DV-540A is drawn below HX-501A.
- `PDT-530A` -- `FLT-501A`: PDT-530A dashed pressure-differential tap is associated with FLT-501A.
- `PDT-530A` -- `PDAH-530A`: Dashed signal link from PDT-530A to PDAH-530A.
- `TT-541A` -- `HX-501A`: TT-541A dashed temperature tap is associated with HX-501A.
- `HDR-DIS-501` -- `HV-530B`: B filter train branches from HDR-DIS-501 through HV-530B.
- `HV-530B` -- `FLT-501B`: B train line enters FLT-501B after HV-530B.
- `FLT-501B` -- `HV-531B`: B train line exits FLT-501B to HV-531B.
- `HV-531B` -- `HX-501B`: B train line enters HX-501B after HV-531B.
- `HX-501B` -- `MOV-532B`: B train outlet leaves HX-501B through MOV-532B.
- `MOV-532B` -- `HDR-SUP-501`: B train outlet ties into the named supply/distribution header.
- `FLT-501B` -- `VV-530B`: Vent valve VV-530B is drawn above FLT-501B.
- `FLT-501B` -- `DV-530B`: Drain valve DV-530B is drawn below FLT-501B.
- `HX-501B` -- `VV-540B`: Vent valve VV-540B is drawn above HX-501B.
- `HX-501B` -- `DV-540B`: Drain valve DV-540B is drawn below HX-501B.
- `PDT-530B` -- `FLT-501B`: PDT-530B dashed pressure-differential tap is associated with FLT-501B.
- `PDT-530B` -- `PDAH-530B`: Dashed signal link from PDT-530B to PDAH-530B.
- `TT-541B` -- `HX-501B`: TT-541B dashed temperature tap is associated with HX-501B.

### Service Water 560 / 540 / 550 Area
- `OPC-SW-IN-501` -- `HDR-SW-SUP-501`: Service-water inlet off-page connector feeds HDR-SW-SUP-501.
- `HDR-SW-SUP-501` -- `FT-560A`: FT-560A is drawn on/tapping the supply header.
- `FT-560A` -- `FI-560A`: Dashed flow signal from FT-560A to FI-560A.
- `HDR-SW-SUP-501` -- `HV-560A`: Supply header branches down through HV-560A.
- `HV-560A` -- `TCV-560A`: A service-water branch continues from HV-560A to TCV-560A.
- `TCV-560A` -- `HV-561A`: A service-water branch continues from TCV-560A to HV-561A.
- `HV-561A` -- `HX-501A`: A service-water leg visually turns down into the HX-501A service side.
- `OPC-SW-OUT-501` -- `HDR-SW-RET-501`: Service-water outlet off-page connector is on the return header.
- `HDR-SW-RET-501` -- `FT-560B`: FT-560B is drawn on/tapping the return header.
- `FT-560B` -- `FI-560B`: Dashed flow signal from FT-560B to FI-560B.
- `HDR-SW-RET-501` -- `HV-560B`: Return-side/lower service-water branch includes HV-560B.
- `HV-560B` -- `TCV-560B`: B service-water branch continues from HV-560B to TCV-560B.
- `TCV-560B` -- `HV-561B`: B service-water branch continues from TCV-560B to HV-561B.
- `HV-561B` -- `HX-501B`: B service-water leg visually turns down into the HX-501B service side.
- `TIC-540` -- `TCV-560A`: Dashed temperature-control signal toward TCV-560A.
- `TIC-540` -- `TCV-560B`: Dashed temperature-control signal toward TCV-560B.
- `TT-540` -- `TIC-540`: TT-540 is signal-linked to TIC-540.
- `PT-550` -- `PI-550`: PT-550 and PI-550 are connected by dashed pressure indication signal.
- `PI-550` -- `HX-501A`: PI-550 sits on the vertical service-water line feeding the HX area.
- `PSV-550` -- `TT-540`: PSV-550/TT-540 are on the same vertical 4-inch SW-563/vent leg.
- `PSV-550` -- `HDR-VENT-501`: PSV-550 is tied to the visible service-water vent header convention.
- `HDR-SUP-501` -- `TT-540`: TT-540 sits on the vertical leg adjacent to the HDR-SUP-501 CCW-550 header box.

### Right Distribution Branches 601-607
- `HDR-SUP-501` -- `HV-601A`: Branch 601 drops from the shared supply header into HV-601A.
- `HV-601A` -- `FT-601`: Branch 601 continues from HV-601A to FT-601.
- `FT-601` -- `FCV-601`: Branch 601 main line continues from FT-601 to FCV-601.
- `FCV-601` -- `HX-601`: Branch 601 main line enters HX-601 after FCV-601.
- `HX-601` -- `CV-601`: Branch 601 outlet continues from HX-601 to CV-601.
- `CV-601` -- `HV-601B`: Branch 601 outlet continues from CV-601 to HV-601B.
- `HV-601B` -- `HDR-RET-501`: Branch 601 returns from HV-601B to the common lower return header.
- `FT-601` -- `FIC-601`: Dashed flow signal from FT-601 to FIC-601.
- `FIC-601` -- `FCV-601`: Dashed control signal from FIC-601 to FCV-601.
- `HX-601` -- `VV-601`: Vent valve VV-601 is drawn as the local dashed tap for HX-601.
- `HX-601` -- `DV-601`: Drain valve DV-601 is drawn as the local dashed tap for HX-601.
- `HX-601` -- `PI-601`: PI-601 is the local pressure indicator/tap for HX-601.
- `HDR-SUP-501` -- `HV-602A`: Branch 602 drops from the shared supply header into HV-602A.
- `HV-602A` -- `FT-602`: Branch 602 continues from HV-602A to FT-602.
- `FT-602` -- `FCV-602`: Branch 602 main line continues from FT-602 to FCV-602.
- `FCV-602` -- `HX-602`: Branch 602 main line enters HX-602 after FCV-602.
- `HX-602` -- `CV-602`: Branch 602 outlet continues from HX-602 to CV-602.
- `CV-602` -- `HV-602B`: Branch 602 outlet continues from CV-602 to HV-602B.
- `HV-602B` -- `HDR-RET-501`: Branch 602 returns from HV-602B to the common lower return header.
- `FT-602` -- `FIC-602`: Dashed flow signal from FT-602 to FIC-602.
- `FIC-602` -- `FCV-602`: Dashed control signal from FIC-602 to FCV-602.
- `HX-602` -- `VV-602`: Vent valve VV-602 is drawn as the local dashed tap for HX-602.
- `HX-602` -- `DV-602`: Drain valve DV-602 is drawn as the local dashed tap for HX-602.
- `HX-602` -- `PI-602`: PI-602 is the local pressure indicator/tap for HX-602.
- `HDR-SUP-501` -- `HV-603A`: Branch 603 drops from the shared supply header into HV-603A.
- `HV-603A` -- `FT-603`: Branch 603 continues from HV-603A to FT-603.
- `FT-603` -- `FCV-603`: Branch 603 main line continues from FT-603 to FCV-603.
- `FCV-603` -- `HX-603`: Branch 603 main line enters HX-603 after FCV-603.
- `HX-603` -- `CV-603`: Branch 603 outlet continues from HX-603 to CV-603.
- `CV-603` -- `HV-603B`: Branch 603 outlet continues from CV-603 to HV-603B.
- `HV-603B` -- `HDR-RET-501`: Branch 603 returns from HV-603B to the common lower return header.
- `FT-603` -- `FIC-603`: Dashed flow signal from FT-603 to FIC-603.
- `FIC-603` -- `FCV-603`: Dashed control signal from FIC-603 to FCV-603.
- `HX-603` -- `VV-603`: Vent valve VV-603 is drawn as the local dashed tap for HX-603.
- `HX-603` -- `DV-603`: Drain valve DV-603 is drawn as the local dashed tap for HX-603.
- `HX-603` -- `PI-603`: PI-603 is the local pressure indicator/tap for HX-603.
- `HDR-SUP-501` -- `HV-604A`: Branch 604 drops from the shared supply header into HV-604A.
- `HV-604A` -- `FT-604`: Branch 604 continues from HV-604A to FT-604.
- `FT-604` -- `FCV-604`: Branch 604 main line continues from FT-604 to FCV-604.
- `FCV-604` -- `HX-604`: Branch 604 main line enters HX-604 after FCV-604.
- `HX-604` -- `CV-604`: Branch 604 outlet continues from HX-604 to CV-604.
- `CV-604` -- `HV-604B`: Branch 604 outlet continues from CV-604 to HV-604B.
- `HV-604B` -- `HDR-RET-501`: Branch 604 returns from HV-604B to the common lower return header.
- `FT-604` -- `FIC-604`: Dashed flow signal from FT-604 to FIC-604.
- `FIC-604` -- `FCV-604`: Dashed control signal from FIC-604 to FCV-604.
- `HX-604` -- `VV-604`: Vent valve VV-604 is drawn as the local dashed tap for HX-604.
- `HX-604` -- `DV-604`: Drain valve DV-604 is drawn as the local dashed tap for HX-604.
- `HX-604` -- `PI-604`: PI-604 is the local pressure indicator/tap for HX-604.
- `HDR-SUP-501` -- `HV-605A`: Branch 605 drops from the shared supply header into HV-605A.
- `HV-605A` -- `FT-605`: Branch 605 continues from HV-605A to FT-605.
- `FT-605` -- `FCV-605`: Branch 605 main line continues from FT-605 to FCV-605.
- `FCV-605` -- `HX-605`: Branch 605 main line enters HX-605 after FCV-605.
- `HX-605` -- `CV-605`: Branch 605 outlet continues from HX-605 to CV-605.
- `CV-605` -- `HV-605B`: Branch 605 outlet continues from CV-605 to HV-605B.
- `HV-605B` -- `HDR-RET-501`: Branch 605 returns from HV-605B to the common lower return header.
- `FT-605` -- `FIC-605`: Dashed flow signal from FT-605 to FIC-605.
- `FIC-605` -- `FCV-605`: Dashed control signal from FIC-605 to FCV-605.
- `HX-605` -- `VV-605`: Vent valve VV-605 is drawn as the local dashed tap for HX-605.
- `HX-605` -- `DV-605`: Drain valve DV-605 is drawn as the local dashed tap for HX-605.
- `HX-605` -- `PI-605`: PI-605 is the local pressure indicator/tap for HX-605.
- `HDR-SUP-501` -- `HV-606A`: Branch 606 drops from the shared supply header into HV-606A.
- `HV-606A` -- `FT-606`: Branch 606 continues from HV-606A to FT-606.
- `FT-606` -- `FCV-606`: Branch 606 main line continues from FT-606 to FCV-606.
- `FCV-606` -- `HX-606`: Branch 606 main line enters HX-606 after FCV-606.
- `HX-606` -- `CV-606`: Branch 606 outlet continues from HX-606 to CV-606.
- `CV-606` -- `HV-606B`: Branch 606 outlet continues from CV-606 to HV-606B.
- `HV-606B` -- `HDR-RET-501`: Branch 606 returns from HV-606B to the common lower return header.
- `FT-606` -- `FIC-606`: Dashed flow signal from FT-606 to FIC-606.
- `FIC-606` -- `FCV-606`: Dashed control signal from FIC-606 to FCV-606.
- `HX-606` -- `VV-606`: Vent valve VV-606 is drawn as the local dashed tap for HX-606.
- `HX-606` -- `DV-606`: Drain valve DV-606 is drawn as the local dashed tap for HX-606.
- `HX-606` -- `PI-606`: PI-606 is the local pressure indicator/tap for HX-606.
- `HDR-SUP-501` -- `HV-607A`: Branch 607 drops from the shared supply header into HV-607A.
- `HV-607A` -- `FT-607`: Branch 607 continues from HV-607A to FT-607.
- `FT-607` -- `FCV-607`: Branch 607 main line continues from FT-607 to FCV-607.
- `FCV-607` -- `HX-607`: Branch 607 main line enters HX-607 after FCV-607.
- `HX-607` -- `CV-607`: Branch 607 outlet continues from HX-607 to CV-607.
- `CV-607` -- `HV-607B`: Branch 607 outlet continues from CV-607 to HV-607B.
- `HV-607B` -- `HDR-RET-501`: Branch 607 returns from HV-607B to the common lower return header.
- `FT-607` -- `FIC-607`: Dashed flow signal from FT-607 to FIC-607.
- `FIC-607` -- `FCV-607`: Dashed control signal from FIC-607 to FCV-607.
- `HX-607` -- `VV-607`: Vent valve VV-607 is drawn as the local dashed tap for HX-607.
- `HX-607` -- `DV-607`: Drain valve DV-607 is drawn as the local dashed tap for HX-607.
- `HX-607` -- `PI-607`: PI-607 is the local pressure indicator/tap for HX-607.
- `HX-607` -- `TI-607`: TI-607 is the local temperature indicator beside HX-607.

### Bottom Return / Drain / Control Bay
- `HDR-RET-501` -- `CV-580`: Common return/drain header passes through CV-580.
- `CV-580` -- `HV-580`: CV-580 is immediately followed by HV-580 on the bottom header.
- `HV-580` -- `OPC-DRN-501`: HV-580 outlet is on the line labeled toward waste sump/OPC-DRN-501.
- `HDR-RET-501` -- `HDR-DRN-501`: Lower common return and named drain header are visually adjacent and tied by the bottom header run.
- `HDR-DRN-501` -- `OPC-DRN-501`: HDR-DRN-501 points to the OPC-DRN-501/waste-sump endpoint.
- `HDR-DRN-501` -- `TT-590`: TT-590 has a dashed tap to the bottom drain/return header.
- `HDR-DRN-501` -- `PT-590`: PT-590 has a dashed tap to the bottom drain/return header.
- `CP-501` -- `JB-501`: Dashed signal cable from local control panel CP-501 to field junction box JB-501.
- `JB-501` -- `JB-502`: Solid cable tray/line from JB-501 to remote I/O JB-502.
- `JB-502` -- `DCS-501`: Solid signal line from JB-502 to DCS-501.

## Ambiguous Or Uncertain Cases

- `HDR-VENT-501`, `OPC-VENT-501`, and the PSV/HV vent branches are represented conservatively as named vent endpoints. The exact common vent routing is partly off-page/indirect, so these are plausible endpoint connections rather than full header clique expansion.
- `V-501` to `ORF-520` is included because the visible return line `3"-CCW-523-R1` descends from the air separator area to the pump recycle region; the intermediate bend/junction is intentionally not named.
- `HDR-SW-RET-501` to `HV-560B` and `HV-561B` to `HX-501B` follow the visually local lower service-water branch. The service-water side crosses/turns around the exchanger area, so these are high-recall process-side endpoint calls.
- `HDR-RET-501` and `HDR-DRN-501` are both retained because both named boxes are visible around the lower common header. I connected them as adjacent common lower-header endpoints rather than replacing one with the other.
- Instruments on dashed taps, such as `PDT-530A/B`, `TT-541A/B`, `PI-60x`, `TT-590`, and `PT-590`, are connected to their nearest named equipment/header endpoint rather than to anonymous tap points.

## Labels Not Included

- Anonymous `WN-*` IDs and all wire-node CSV junctions/t-sections were not included.
- Line-number-only labels, pipe sizes, arrows, crop labels, revision text, title-block text, and legend labels were not included as nodes.
- Generic ground/terminal marks near drain valves were not included because they are unlabeled and not necessary named endpoints.
- Area titles such as `SURGE / MAKEUP`, `FILTER / HEAT EXCHANGER TRAINS`, `DISTRIBUTION BRANCHES`, and `CONTROL AND SIGNAL MARSHALLING` were not included because they are boundaries/section labels rather than connection endpoints.

## Basic Validation

- Node count: 184
- Edge count: 216
- Diagonal check: pass, all diagonal entries are 0
- Symmetry check: pass, matrix is symmetric
- Isolated included nodes: None.
