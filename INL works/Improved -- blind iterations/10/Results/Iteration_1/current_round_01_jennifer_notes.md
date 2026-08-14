# Jennifer Round 01 Precision Review

Scope: reviewed only the allowed input resources, the current input-derived aids/crops, and Diego's current round 01 proposal. Ground Truth, evaluator/scoring outputs, prior results, archived results, and tracker metrics were not used.

## Node Decisions

- Confirmed `TR-UPS-A` and `TR-UPS-B` as raw-visible transformer labels; both remain.
- Kept `BUS-480V-LC-FEEDERS-A` and `BUS-480V-LC-FEEDERS-B` as explicit raw-labeled conductor/bus segments because the label sits on the shared 480 V feeder with visible taps to `FAN-CR-*`, `LC-101*`, and `LC-102*`.
- Kept the other named components, explicit raw-labeled buses, UPS/DC buses, and grounds from Diego. No final `WN-*` nodes are present.

## Edge Refinements

- Kept the top source/tie topology that routes through `CB-UAT`, `CB-SAT`, `CB-TIE-AB`, `CB-DGA`, `CB-DGB`, transformers, and the 4160 V buses; Diego's removed top-bus-to-`UAT-1` shortcut stays removed.
- Removed Diego's direct relay-to-relay trunk edges (`RLY-27*`/`RLY-50*`/`RLY-86*`) because the raw view supports relay branches from the local terminal/control trunk, not direct relay terminals between adjacent relays.
- Removed direct `PT-4160-*`/`CT-4160-*` to `BUS-4160-*` matrix edges and `CT-4160-*` to `FUSE-*01` edges; these are visually adjacent or route nearby, but the raw image does not show clean terminal endpoints.
- Kept `PNL-MCR-01` to `JB-CONTROL` and changed `PNL-ANN-01` to `JB-CONTROL` to keep, because the MCR bay shows direct dashed/dotted terminal paths. Removed `PNL-ANN-01` to `SER-01` and `SER-01` to `JB-CONTROL`; the dotted path runs beside `SER-01` without a clear SER terminal.
- Removed direct lower load-to-load `PUMP-CCW-*` to `FAN-AB-*` edges; the supported endpoints are the MCC/load/disconnect paths.
- Removed long `TB-SWGR-*` to `PNL-MCR-01` control-tray links from the matrix because they rely on cable-tray proximity rather than a clear terminal path. Long tray paths that remain ambiguous are marked `uncertain`, not kept.
- Kept ground edges only where the dash-dot reference route visibly terminates at `GND-A` or `GND-B`.

## Counts

- Nodes: 120
- Edge candidates reviewed: 152
- Keep edges in matrix: 123
- Uncertain edges excluded from matrix: 8
- Removed edges excluded from matrix: 21
- Status changes from Diego: 17

## Diego Follow-Up

Another focused Diego round is recommended for the RPS/ESFAS dotted instrumentation endpoints and long control-tray endpoints. The primary source, breaker, transformer, 480 V feeder, DC/UPS, MCC/load, and ground topology is otherwise stable after this precision pass.
