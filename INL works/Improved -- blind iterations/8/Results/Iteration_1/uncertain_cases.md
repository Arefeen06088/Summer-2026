# Uncertain Cases

1. `CB-EDG-C` as a shared/swing diesel feeder

The raw geometry shows `EDG-2C` connected to `CB-EDG-C`, and `CB-EDG-C` has solid connections extending left and right toward both `BUS-4160-S2A` and `BUS-4160-S2B`. I accepted both edges because the solid geometry is clear, but the intended operating philosophy may be a swing diesel/tie arrangement rather than simultaneous service to both buses.

2. 480 V feeder tie endpoints

`DS-480-A` and `DS-480-B` are labeled as a normally open feeder tie. The visual lines suggest a tie across the central 480 V buses, but the exact endpoints are crowded by vertical transformer/CB feeders. I listed `DS-480-A -- DS-480-B` and both possible endpoint interpretations in lower-confidence edges.

3. `MCC-2C`/`MCC-2D` versus `PN-480-A`/`PN-480-B` load assignment

The center 480/DC/UPS area overlaps feeder routing. `MCC-2C` and `MCC-2D` are visible components missed by OCR. Some loads near the boundary (`PUMP-CHG-2A/B`, `FAN-VENT-2A/B`) appear fed by the panel/MCC region; I accepted the cleaner `PN-480-A/B` load edges and kept MCC alternatives lower-confidence.

4. Ground symbols

`GND-A` and `GND-B` are true ground symbols, but the precise equipment or bus they ground is not fully explicit from the crop. I kept them as logical ground nodes and listed their bus associations as lower-confidence.

5. Dashed CT/PT/control/trip circuits

The legend identifies dashed lines as control/signals and CT/PT signal lines. These are real electrical/control connections, but they are not solid power topology. I kept them in lower-confidence edges so they are not hidden, while preventing them from collapsing power buses together.

6. OCR label `GND-AJ`

The component CSV lists `GND-AJ`, while the raw crop reads as `GND-A`. I used `GND-A` in node/edge rows and recorded this as an OCR-label discrepancy.
