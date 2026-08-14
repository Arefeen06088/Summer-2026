# Round 2 Jennifer Precision Review

Jennifer removed Diego's overconnections in the 125 V charger/battery/DC cluster and corrected the charger AC inputs to direct 480 V bus taps.

## Corrected Node List

GRID-345; DS-101; CB-101; GEN-G1; CB-G1; GEN-G2; CB-G2; BUS-13KV-N; TR-1A; CB-4A-IN; TR-1B; CB-4B-IN; BUS-4160-A; BUS-4160-B; DG-1A; CB-DG1A; DG-1B; CB-DG1B; CB-TIE-41; TR-480-A; CB-480A-IN; BUS-480-A; TR-480-B; CB-480B-IN; BUS-480-B; TR-480-C; CB-480C-IN; BUS-480-C; TR-480-D; CB-480D-IN; BUS-480-D; CB-A01; DS-A01; PMP-A01; RLY-A01; CB-A02; FU-A02; MOV-A02; LS-A02; CB-A03; DS-A03; MTR-A03; RLY-A03; CB-A04; DS-A04; PNL-A04; JB-A04; CB-A05; FU-A05; PMP-A05; FT-A05; CB-A06; DS-A06; MOV-A06; RLY-A06; CB-A07; DS-A07; MCC-A07; TB-A07; CB-A08; FU-A08; PMP-A08; PT-A08; CB-A09; DS-A09; FAN-A09; HS-A09; CB-A10; DS-A10; JB-A10; LT-A10; CB-B01; DS-B01; PMP-B01; RLY-B01; CB-B02; FU-B02; MOV-B02; LS-B02; CB-B03; DS-B03; MTR-B03; RLY-B03; CB-B04; DS-B04; PNL-B04; JB-B04; CB-B05; FU-B05; PMP-B05; FT-B05; CB-B06; DS-B06; MOV-B06; RLY-B06; CB-B07; DS-B07; MCC-B07; TB-B07; CB-B08; FU-B08; PMP-B08; PT-B08; CB-B09; DS-B09; FAN-B09; HS-B09; CB-B10; DS-B10; JB-B10; LT-B10; CB-C01; DS-C01; MOV-C01; RLY-C01; CB-C02; FU-C02; PNL-C02; JB-C02; CB-C03; DS-C03; PMP-C03; FT-C03; CB-C04; DS-C04; HTR-C04; HS-C04; CB-C05; FU-C05; INST-C05; JB-C05; CB-C06; DS-C06; MOV-C06; LS-C06; CB-C07; DS-C07; MCC-C07; TB-C07; CB-C08; FU-C08; PMP-C08; PT-C08; CB-C09; DS-C09; PNL-C09; RLY-C09; CB-C10; DS-C10; JB-C10; TB-C10; CB-D01; DS-D01; MOV-D01; RLY-D01; CB-D02; FU-D02; PNL-D02; JB-D02; CB-D03; DS-D03; PMP-D03; FT-D03; CB-D04; DS-D04; HTR-D04; HS-D04; CB-D05; FU-D05; INST-D05; JB-D05; CB-D06; DS-D06; MOV-D06; LS-D06; CB-D07; DS-D07; MCC-D07; TB-D07; CB-D08; FU-D08; PMP-D08; PT-D08; CB-D09; DS-D09; PNL-D09; RLY-D09; CB-D10; DS-D10; JB-D10; TB-D10; CHGR-125A; BAT-125A; DC-BUS-125A; CHGR-125B; BAT-125B; DC-BUS-125B; PANEL-CTRL-MAIN; GND-EQ-A; GND-EQ-B

## Removed From Diego

- DS-A10,CHGR-125A: Removed: CHGR-125A has its own solid tap from BUS-480-A, not a downstream connection from DS-A10.
- DS-B01,CHGR-125B: Removed: CHGR-125B has its own solid tap from BUS-480-B, not a downstream connection from DS-B01.
- BAT-125A,DC-BUS-125A: Removed as a direct edge: BAT-125A appears tied through the charger/DC dash-dot cluster, not directly to the bus tap.
- BAT-125B,DC-BUS-125B: Removed as a direct edge: BAT-125B appears tied through the charger/DC dash-dot cluster, not directly to the bus tap.
- DC-BUS-125B,PANEL-CTRL-MAIN: Removed as an extra direct edge: panel taps the common span; represented by DC-BUS-125A to panel plus the A-B bus-span edge.

## Kept Ambiguous / Medium Confidence

- BUS-4160-A,TR-480-C: Kept Medium: long feeder is visually continuous through the left routing run, but it is less compact than the A/B transformer feeds.
- BUS-4160-B,TR-480-D: Kept Medium: long feeder is visually continuous through the right routing run, but it is less compact than the A/B transformer feeds.
- CHGR-125A,BAT-125A: Kept Medium: dash-dot DC/control cluster touches the charger and battery, but terminal detail is small.
- CHGR-125B,BAT-125B: Kept Medium: dash-dot DC/control cluster touches the charger and battery, but terminal detail is small.
- CHGR-125A,DC-BUS-125A: Kept Medium: dash-dot DC/control cluster visually ties CHGR-125A to the DC-BUS-125A tap, but terminal detail is small.
- CHGR-125B,DC-BUS-125B: Kept Medium: dash-dot DC/control cluster visually ties CHGR-125B to the DC-BUS-125B tap, but terminal detail is small.
- DC-BUS-125A,DC-BUS-125B: Kept Medium: labels sit on a continuous horizontal DC bus span with filled tap marks.
- DC-BUS-125A,PANEL-CTRL-MAIN: Kept Medium: the tap lands on the common DC span; represented through the A-side bus node.
- BUS-480-C,GND-EQ-A: Kept Medium: labeled ground node is connected by dotted/dc-ground line from BUS-480-C area.
- BUS-480-D,GND-EQ-B: Kept Medium: labeled ground node is connected by dotted/dc-ground line from BUS-480-D area.

## Round 2 Edge Count

201
