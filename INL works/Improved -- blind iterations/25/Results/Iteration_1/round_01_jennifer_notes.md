# Jennifer precision review notes - Improved doc 25 / Iteration 1

## Evidence Boundary
I inspected only the raw schematic and the allowed derived/crop artifacts under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\25\Input resources` and `C:\Asif_all_python_projects\INL\Improved -- blind iterations\25\Codes and artifacts`, plus Diego's round-01 files under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\25\Results\Iteration_1`. The raw schematic was treated as primary and crops/overlays were used only as visual aids. No ground truth, GT-derived evaluator output, score feedback, or resources from any other document or iteration were used.

## Output Summary
- Matrix file: `round_01_jennifer_matrix.csv`
- Node count: 203
- Undirected edge count: 202
- Matrix convention: same row/column labels and order as Diego; symmetric 0/1 adjacency; diagonal entries are 0.

## Final Node Policy
- Kept Diego's component nodes because the labels correspond to visible schematic component symbols in the allowed raw/crop resources.
- Kept raw-visible named buses: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-C`, `BUS-480-1A`, `BUS-480-1B`, `BUS-480-1C`, `BUS-125DC-A`, and `BUS-125DC-B`.
- Kept named dashed/logical route nodes only where the raw schematic prints the name as a connectivity object and a direct endpoint is visible: `480V-CHGR-A-FEEDER`, `480V-CHGR-B-FEEDER`, `RPS-TRIP-BUS`, and `PNL-A-B-TIE`.
- Did not add intermediate wire-node IDs, WN/W route points, unlabeled junctions, or inferred upstream/source nodes.
- Did not clique-expand any bus section, route lane, tie route, or trip/control lane.

## Edge Changes vs Diego
| Edge | Jennifer action | Reason |
|---|---|---|
| `INV-120-1A` -- `BUS-125DC-B` | Removed from matrix | A solid lower conductor is visible from the A inverter region toward the B DC bus structure, but its role is not clearly labeled as a direct inverter-to-B-bus feed. Because it may be a routed return/cross-feed feature and the precision pass should avoid guessing, I left it as uncertain rather than accepted connectivity. |

No other Diego edges were changed.

## Accepted Edge Rationale By Region
### Top Sources and 4.16 kV Buses
- Kept visible source chains: `FDR-13A` - `TR-UAT-1A` - `CB-52-4A` - `BUS-4160-A`; `FDR-13B` - `TR-UAT-1B` - `CB-52-4B` - `BUS-4160-B`; and `TR-SAT-1` - `CB-52-4C` - `BUS-4160-C`.
- Kept EDG chains `EDG-1A/B/C` - `CB-DG-1A/B/C` - matching `BUS-4160-A/B/C`.
- Kept tie breaker endpoints only: `BUS-4160-A` - `CB-TIE-AB` - `BUS-4160-B` and `BUS-4160-B` - `CB-TIE-BC` - `BUS-4160-C`.

### 4 kV Feeder Rows
- Kept each `BUS-4160-X` - `CB-4X##` - `DS-4X##` feeder chain because the breaker drops visibly land on the train bus and continue to the disconnects.
- Kept the first feeder split for each train: each `DS-4X01` connects to both `TR-480-1X` and `MS-X01`. The raw crop shows a real branch/parallel landing at feeder position 01, not just label proximity.
- Kept the remaining direct equipment chains: feeder 02 to `MS-X02`/CS pump, 03 to `TR-LC-X03`/load center, 04 to `MS-X04`/fan, 05 to `PNL-ESF-X05`/ground, 06 to `RECT-RPS-X06`/inverter, 07 to `MS-X07`/AFW pump, and 08 to `TR-CTRL-X08`/control panel.

### 480 V Buses and MCC Branches
- Kept `TR-480-1X` - `CB-52-48X` - `BUS-480-1X` and `BUS-480-1X` - `MCC-X1` because the transformer secondary/breaker/bus/MCC feed path is directly drawn.
- Kept `MCC-X1` - `MCC-X2` for trains A/B/C because the upper and lower MCC sections are joined by a raw-visible vertical continuation conductor.
- Kept each MCC branch only as drawn: MCC section to breaker, breaker to starter/relay/fuse, and starter/relay/fuse to the endpoint load.

### Lower DC, RPS Panels, and Trip Logic
- Kept `CHGR-125-1A` - `BUS-125DC-A`, `BAT-125-1A` - `BUS-125DC-A`, and `BUS-125DC-A` - `INV-120-1A`.
- Kept `CHGR-125-1B` - `BUS-125DC-B`, `BAT-125-1B` - `BUS-125DC-B`, and `BUS-125DC-B` - `INV-120-1B`.
- Kept `480V-CHGR-A-FEEDER` - `CHGR-125-1A` and `480V-CHGR-B-FEEDER` - `CHGR-125-1B` only as printed feeder-route endpoints. No upstream 480 V source was inferred.
- Kept panel endpoint edges `INV-120-1A` - `PNL-RPS-A`, `PNL-RPS-A` - `RELAY-K501A`, `PNL-RPS-A` - `XMTR-PT-501A`, `INV-120-1B` - `PNL-RPS-B`, `PNL-RPS-B` - `RELAY-K501B`, and `PNL-RPS-B` - `XMTR-PT-501B`.
- Kept `PNL-A-B-TIE` as a named logical tie node with only `PNL-RPS-A` and `PNL-RPS-B` endpoints, because the printed `PNL A/B TIE` route visibly ties those panel lanes and should not be expanded beyond them.
- Kept trip endpoint edges `RELAY-K501A` - `TC-52-4A`, `RELAY-K501B` - `TC-52-4A`, and `RPS-TRIP-BUS` - `TC-52-4A`. The printed trip bus was not connected to relays except through the visible trip coil endpoint.

## Uncertain / Plausible Candidates
| Candidate | Matrix disposition | Visual basis | Precision note |
|---|---|---|---|
| `INV-120-1A` -- `BUS-125DC-B` | Omitted | Solid lower conductor routes from the A inverter area to the B DC bus junction area. | Plausible physical route, but not clear enough as direct inverter-to-B-bus connectivity; may be a return/cross-feed/routed lane. |
| `480V-CHGR-A-FEEDER` upstream source | Omitted | Printed dashed feeder route enters/aligns with charger A. | No direct raw-visible endpoint to a specific `BUS-480-*` bus or breaker was present in the reviewed crop. |
| `480V-CHGR-B-FEEDER` upstream source | Omitted | Printed dashed feeder route enters/aligns with charger B. | No direct raw-visible endpoint to a specific `BUS-480-*` bus or breaker was present in the reviewed crop. |
| `RPS-TRIP-BUS` to relay nodes | Omitted | Printed trip bus route is visible near the trip coil and control lines. | Relay-to-trip-bus connection is not directly endpoint-supported; only relay-to-`TC-52-4A` and `RPS-TRIP-BUS`-to-`TC-52-4A` were accepted. |
| Direct `PNL-RPS-A` -- `PNL-RPS-B` without tie node | Omitted | The raw label says `PNL A/B TIE`. | Modeled through the named tie node instead of a direct panel-panel edge to preserve the printed logical object. |

## Removed / Rejected Candidates
| Candidate | Removed/rejected | Reason |
|---|---|---|
| `INV-120-1A` -- `BUS-125DC-B` | Removed from Diego | Ambiguous lower conductor; not accepted as a direct component-to-B-bus feed in the precision matrix. |
| `480V-CHGR-A-FEEDER` -- any `BUS-480-*` node | Rejected/not added | Upstream 480 V endpoint was not visible; only charger endpoint is supported. |
| `480V-CHGR-B-FEEDER` -- any `BUS-480-*` node | Rejected/not added | Upstream 480 V endpoint was not visible; only charger endpoint is supported. |
| `RPS-TRIP-BUS` -- `RELAY-K501A` | Rejected/not added | The relay has a visible route to the trip coil, but not a direct endpoint to the named trip bus node. |
| `RPS-TRIP-BUS` -- `RELAY-K501B` | Rejected/not added | The relay has a visible route to the trip coil, but not a direct endpoint to the named trip bus node. |
| Clique connections among `PNL-RPS-A`, `PNL-RPS-B`, `RELAY-K501A`, `RELAY-K501B`, `RPS-TRIP-BUS`, and `TC-52-4A` | Rejected/not added | Dashed routes cross and run in parallel; only direct endpoint-supported signal/control edges were kept. |
| Intermediate `WN-*`/`W###` route nodes | Rejected/not added | These are routing aids/intermediate wire labels rather than schematic connectivity objects for this matrix. |
