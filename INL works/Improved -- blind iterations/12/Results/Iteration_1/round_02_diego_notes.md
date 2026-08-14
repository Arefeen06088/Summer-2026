# Round 2 Diego Notes - Doc 12

## Scope

Used only doc 12 `Input resources`, doc 12 generated crops/artifacts, and Round 1 files in `Results\Iteration_1`. I did not use GT, evaluator outputs, scores, validation metrics, or answer keys. Anonymous wire-node points remain excluded as matrix nodes.

## Node Review

Jennifer's 160-node set stands. I kept the accepted raw-label corrections for repeated feeders and the same visible bus names: `BUS-4KV-A`, `BUS-4KV-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-A`, `DC-BUS-B`, and `BUS-120VAC-ESF`. I did not add `BUS-4160-A/B` or `BUS-120VAC-RPS` aliases.

## Edge Decision

I do not fully agree with Jennifer's 142-edge set. Round 2 restores two short, local, named-endpoint edges:

- `BUS-120VAC-ESF --ac_control_power-- PNL-RPS-A`
- `BUS-120VAC-ESF --ac_control_power-- PNL-RPS-B`

Reason: zoomed review of `13_rps_relay_tb_panels_raw.png` and `19_full_bottom_controls_raw.png` shows black-dot taps on the solid `BUS-120VAC-ESF` bus dropping as solid vertical conductors directly into the top edges of `PNL-RPS-A` and `PNL-RPS-B`. These are not long trunks and do not rely on crossings without dots.

Round 2 accepted edge count is therefore 144: Jennifer's 142 accepted edges plus these 2 restored panel-feed edges.

## Candidates Kept Uncertain

- PT taps: I agree with Jennifer's removal of `BUS-4KV-A -- PT-4160A` and `BUS-4KV-B -- PT-4160B`. The PT symbols are visible, but the raw geometry does not show the same clear black bus-tap dot used elsewhere for direct bus connections.
- `PT-4160A/B -> RELAY-27A/B`: plausible signal relationship, but the path leaves the top crop and enters lower control routing through trunks/crossings; no direct named endpoint evidence.
- `RELAY-27A/B -> TB-RPS-A/B` and `RELAY-86A/B -> TB-RPS-A/B`: local wiring is visible, but the relay/TB clusters are compact and endpoint attribution is not clean enough to promote.
- `TB-RPS-A/B -> PNL-RPS-A/B`: short conductors are visually plausible, but the TB and panel wiring overlaps with adjacent bus taps and dashed/dotted trunks; left uncertain.
- `PNL-RPS-A/B -> PNL-ESFAS-A/B`: visible dashed routes bend toward ESFAS panels, but they are not direct panel-to-panel terminal edges.
- `BUS-120VAC-ESF` to terminal blocks, ESFAS panels, or `SEQ-REC-1`: no direct solid named endpoint/tap comparable to the two restored RPS panel taps.
- ANN/TB-ANN/SEQ signal paths: kept uncertain because they are long dotted trunks with compact terminal landings and no clear direct endpoint dots.
