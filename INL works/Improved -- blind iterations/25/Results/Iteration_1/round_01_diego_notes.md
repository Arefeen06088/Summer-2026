# Diego extraction notes - Improved doc 25 / Iteration 1

## Evidence boundary
I inspected only the raw schematic and derived/crop artifacts under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\25\Input resources` and `C:\Asif_all_python_projects\INL\Improved -- blind iterations\25\Codes and artifacts`. No ground truth, GT-derived evaluator output, score feedback, or resources from any other document/iteration were used.

## Output summary
- Matrix file: `round_01_diego_matrix.csv`
- Node count: 203
- Undirected edge count: 203
- Matrix convention: symmetric 0/1 adjacency matrix; diagonal entries are 0; intermediate wire-node IDs such as WN/W labels are not included as graph nodes.

## Node list rationale
- Included all 191 physical/logical component labels listed in `component_labels_list.csv`, because these labels correspond to visible component symbols and OCR/manual label evidence from the allowed raw schematic resources.
- Added only raw-visible named bus or logical conductor nodes that are not represented as component rows. These are: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-C`, `BUS-480-1A`, `BUS-480-1B`, `BUS-480-1C`, `BUS-125DC-A`, `BUS-125DC-B`, `480V-CHGR-A-FEEDER`, `480V-CHGR-B-FEEDER`, `RPS-TRIP-BUS`, `PNL-A-B-TIE`.
- Confirmed raw-visible main buses: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-C`, `BUS-480-1A`, `BUS-480-1B`, `BUS-480-1C`, `BUS-125DC-A`, and `BUS-125DC-B`.
- Did not add a `BUS-120...` node: I saw `INV-120-1A` and `INV-120-1B` equipment labels, but no separate printed lower AC bus label in the raw/crop evidence.
- Did not include intermediate geometric wire labels (`W###`, `WN-####`) because they are routing aids rather than named logical nodes/components in the schematic.

### Physical node groups
- `battery` (2): `BAT-125-1A`, `BAT-125-1B`
- `battery_charger` (2): `CHGR-125-1A`, `CHGR-125-1B`
- `breaker` (53): `CB-DG-1A`, `CB-DG-1B`, `CB-DG-1C`, `CB-52-4A`, `CB-52-4B`, `CB-52-4C`, `CB-TIE-AB`, `CB-TIE-BC`, `CB-4A01`, `CB-4A02`, `CB-4A03`, `CB-4A04`, `CB-4A05`, `CB-4A06`, `CB-4A07`, `CB-4A08`, `CB-4B01`, `CB-4B02`, `CB-4B03`, `CB-4B04`, `CB-4B05`, `CB-4B06`, `CB-4B07`, `CB-4B08`, `CB-4C01`, `CB-4C02`, `CB-4C03`, `CB-4C04`, `CB-4C05`, `CB-4C06`, `CB-4C07`, `CB-4C08`, `CB-52-48A`, `CB-52-48B`, `CB-52-48C`, `CB-48A01`, `CB-48A02`, `CB-48A03`, `CB-48B01`, `CB-48B02`, `CB-48B03`, `CB-48C01`, `CB-48C02`, `CB-48C03`, `CB-48A04`, `CB-48A05`, `CB-48A06`, `CB-48B04`, `CB-48B05`, `CB-48B06`, `CB-48C04`, `CB-48C05`, `CB-48C06`
- `control_panel` (3): `CP-CTRL-A08`, `CP-CTRL-B08`, `CP-CTRL-C08`
- `diesel_generator` (3): `EDG-1A`, `EDG-1B`, `EDG-1C`
- `disconnect_switch` (24): `DS-4A01`, `DS-4A02`, `DS-4A03`, `DS-4A04`, `DS-4A05`, `DS-4A06`, `DS-4A07`, `DS-4A08`, `DS-4B01`, `DS-4B02`, `DS-4B03`, `DS-4B04`, `DS-4B05`, `DS-4B06`, `DS-4B07`, `DS-4B08`, `DS-4C01`, `DS-4C02`, `DS-4C03`, `DS-4C04`, `DS-4C05`, `DS-4C06`, `DS-4C07`, `DS-4C08`
- `fan_motor` (6): `FAN-CR-401A`, `FAN-CR-401B`, `FAN-CR-401C`, `FAN-HVAC-501A`, `FAN-HVAC-501B`, `FAN-HVAC-501C`
- `feeder_disconnect` (2): `FDR-13A`, `FDR-13B`
- `fuse` (3): `XFU-48A06`, `XFU-48B06`, `XFU-48C06`
- `ground` (3): `GND-ESF-A05`, `GND-ESF-B05`, `GND-ESF-C05`
- `inverter` (5): `INV-RPS-A06`, `INV-RPS-B06`, `INV-RPS-C06`, `INV-120-1A`, `INV-120-1B`
- `load_center` (3): `LC-480-A03`, `LC-480-B03`, `LC-480-C03`
- `motor_control_center` (6): `MCC-A1`, `MCC-B1`, `MCC-C1`, `MCC-A2`, `MCC-B2`, `MCC-C2`
- `motor_starter` (21): `MS-A01`, `MS-A02`, `MS-A04`, `MS-A07`, `MS-B01`, `MS-B02`, `MS-B04`, `MS-B07`, `MS-C01`, `MS-C02`, `MS-C04`, `MS-C07`, `MS-48A01`, `MS-48A03`, `MS-48B01`, `MS-48B03`, `MS-48C01`, `MS-48C03`, `MS-48A04`, `MS-48B04`, `MS-48C04`
- `panel` (8): `PNL-ESF-A05`, `PNL-ESF-B05`, `PNL-ESF-C05`, `PNL-PI-601A`, `PNL-PI-601B`, `PNL-PI-601C`, `PNL-RPS-A`, `PNL-RPS-B`
- `pid_valve` (6): `MOV-CS-451A`, `MOV-CS-451B`, `MOV-CS-451C`, `MOV-RHR-452A`, `MOV-RHR-452B`, `MOV-RHR-452C`
- `pump_motor` (15): `PUMP-RHR-P201A`, `PUMP-CS-P202A`, `PUMP-AFW-P203A`, `PUMP-RHR-P201B`, `PUMP-CS-P202B`, `PUMP-AFW-P203B`, `PUMP-RHR-P201C`, `PUMP-CS-P202C`, `PUMP-AFW-P203C`, `PUMP-CVC-P301A`, `PUMP-CVC-P301B`, `PUMP-CVC-P301C`, `PUMP-SUMP-P302A`, `PUMP-SUMP-P302B`, `PUMP-SUMP-P302C`
- `rectifier` (3): `RECT-RPS-A06`, `RECT-RPS-B06`, `RECT-RPS-C06`
- `relay` (8): `K-48A02`, `K-48B02`, `K-48C02`, `K-48A05`, `K-48B05`, `K-48C05`, `RELAY-K501A`, `RELAY-K501B`
- `transformer` (12): `TR-SAT-1`, `TR-UAT-1A`, `TR-UAT-1B`, `TR-480-1A`, `TR-480-1B`, `TR-480-1C`, `TR-LC-A03`, `TR-CTRL-A08`, `TR-LC-B03`, `TR-CTRL-B08`, `TR-LC-C03`, `TR-CTRL-C08`
- `transmitter` (2): `XMTR-PT-501A`, `XMTR-PT-501B`
- `trip_coil` (1): `TC-52-4A`

## Edge evidence by schematic region

### Top sources and 4.16 kV bus ties
- Offsite/UAT source chains were entered as visible series adjacency: `FDR-13A` - `TR-UAT-1A` - `CB-52-4A` - `BUS-4160-A`, and `FDR-13B` - `TR-UAT-1B` - `CB-52-4B` - `BUS-4160-B`.
- SAT source chain was entered as `TR-SAT-1` - `CB-52-4C` - `BUS-4160-C`; no separate named upstream offsite bus was printed, so none was invented.
- EDG source chains were entered as `EDG-1A/B/C` - `CB-DG-1A/B/C` - matching `BUS-4160-A/B/C`.
- Tie breakers were entered only as direct bus-to-breaker adjacencies: `BUS-4160-A` - `CB-TIE-AB` - `BUS-4160-B` and `BUS-4160-B` - `CB-TIE-BC` - `BUS-4160-C`. The buses were not clique-expanded.

### 4 kV feeder rows
- For each train A/B/C and each feeder position 01-08, the visible chain `BUS-4160-X` - `CB-4X##` - `DS-4X##` was included.
- Feeder 01 in each train shows both the 480 transformer path and the RHR motor-starter path below the disconnect; I included both `DS-4X01` - `TR-480-1X` - `CB-52-48X` - `BUS-480-1X` and `DS-4X01` - `MS-X01` - `PUMP-RHR-P201X`.
- Feeder 02: `DS-4X02` - `MS-X02` - `PUMP-CS-P202X`.
- Feeder 03: `DS-4X03` - `TR-LC-X03` - `LC-480-X03`.
- Feeder 04: `DS-4X04` - `MS-X04` - `FAN-CR-401X`.
- Feeder 05: `DS-4X05` - `PNL-ESF-X05` - `GND-ESF-X05`; the ground edge follows the visible ground symbol/wire under the ESF panel.
- Feeder 06: `DS-4X06` - `RECT-RPS-X06` - `INV-RPS-X06`.
- Feeder 07: `DS-4X07` - `MS-X07` - `PUMP-AFW-P203X`.
- Feeder 08: `DS-4X08` - `TR-CTRL-X08` - `CP-CTRL-X08`.

### 480 V bus and MCC branches
- Each 480 bus was connected to the visible MCC feed path: `BUS-480-1X` - `MCC-X1`, then `MCC-X1` - `MCC-X2` for the continuing/drop feeder drawn between the upper and lower MCC sections.
- MCC-X1 branch 01: `MCC-X1` - `CB-48X01` - `MS-48X01` - `PUMP-CVC-P301X`.
- MCC-X1 branch 02: `MCC-X1` - `CB-48X02` - `K-48X02` - `MOV-CS-451X`; the relay-to-MOV connection is drawn as the actuator/control path and is included as a real endpoint-supported edge.
- MCC-X1 branch 03: `MCC-X1` - `CB-48X03` - `MS-48X03` - `FAN-HVAC-501X`.
- MCC-X2 branch 04: `MCC-X2` - `CB-48X04` - `MS-48X04` - `PUMP-SUMP-P302X`.
- MCC-X2 branch 05: `MCC-X2` - `CB-48X05` - `K-48X05` - `MOV-RHR-452X`; the relay-to-MOV connection is endpoint-supported in the raw branch drawing.
- MCC-X2 branch 06: `MCC-X2` - `CB-48X06` - `XFU-48X06` - `PNL-PI-601X`.

### Lower DC/RPS/control/trip region
- DC bus A: `480V-CHGR-A-FEEDER` - `CHGR-125-1A` - `BUS-125DC-A`, plus `BAT-125-1A` - `BUS-125DC-A` and `BUS-125DC-A` - `INV-120-1A`.
- DC bus B: `480V-CHGR-B-FEEDER` - `CHGR-125-1B` - `BUS-125DC-B`, plus `BAT-125-1B` - `BUS-125DC-B` and `BUS-125DC-B` - `INV-120-1B`.
- RPS panel feeds/control: `INV-120-1A` - `PNL-RPS-A`, `PNL-RPS-A` - `RELAY-K501A`, `PNL-RPS-A` - `XMTR-PT-501A`; and `INV-120-1B` - `PNL-RPS-B`, `PNL-RPS-B` - `RELAY-K501B`, `PNL-RPS-B` - `XMTR-PT-501B`.
- The printed `PNL A/B TIE` dashed route was represented as `PNL-A-B-TIE` connected to `PNL-RPS-A` and `PNL-RPS-B` only, avoiding a clique across nearby dashed conductors.
- Trip logic was represented as endpoint-supported edges `RELAY-K501A` - `TC-52-4A`, `RELAY-K501B` - `TC-52-4A`, and `RPS-TRIP-BUS` - `TC-52-4A`.

## Ambiguous or high-recall cases
- The first 4 kV feeder position in each train appears to split from the disconnect to both the 480 transformer/480 bus path and the RHR motor starter. I included both paths because the parallel/drop conductors are visually present.
- The MCC upper-to-lower continuation (`MCC-X1` - `MCC-X2`) is included because the vertical feeder is drawn through the MCC sections, but the precise internal bus sectionalization is not explicit.
- The lower `INV-120-1A` has a solid lower conductor that visually routes to the B-side DC bus region. I included `INV-120-1A` - `BUS-125DC-B` as high-recall, but it should be treated cautiously as a possible shared/return/cross-feed conductor rather than a clearly labelled device-to-bus feed.
- The dashed `480V CHGR-A/B FEEDER` lanes are included only as named logical feeder nodes connected to their associated chargers. I did not infer their upstream 480 bus source because no direct endpoint to a specific 480 bus is visible in the lower crop.
- Dashed trip/control lines in the RPS region are visually cluttered near `RPS TRIP BUS`, `PNL A/B TIE`, relays, and `TC-52-4A`; I included only endpoint-supported panel/relay/trip-coil adjacencies and documented them as uncertain rather than expanding every crossing route.
- No separate lower `BUS-120...` node was included; only equipment labels `INV-120-1A` and `INV-120-1B` were visible.

