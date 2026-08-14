# Round 02 Diego Saturation Review Notes

Scope: I used only the doc31 raw schematic/crops and the Round 01 Diego/Jennifer files in `Results\Iteration_1`. No GT, evaluator output, or score feedback was used.

## Decision

I agree with Jennifer's Round 01 precision pass and copied `round_01_jennifer_matrix.csv` exactly to `round_02_diego_matrix.csv`.

No Round 02 edge disagreements or additional saturation edges were added. Jennifer's edits are the better local representation of the disputed regions because they preserve the nearest visible named endpoint rather than jumping across an intervening tag or uncertain crowded signal path.

## Disputed Region Review

### Service-Water Branches Around SWS-501/SWR-501 and HX-301A/B

Accepted Jennifer changes:

- Removed `FT-511A -- FCV-511A`; kept/accepted `FT-511A -- HV-511A`.
- Removed `HV-511A -- HX-301A`; accepted `FCV-511A -- HX-301A`.
- Removed `HV-511B -- HX-301A` and `HV-511B -- HX-301B`; accepted the nearer FCV/cooler adjacencies, including `FCV-511B -- HX-301A`, while retaining the existing `FCV-511B -- HX-301B` edge from the Jennifer matrix.

Raw-image evidence: in crops `07_supply_return_controls_top_raw.png` and `06_filter_cooler_a_b_raw.png`, `FT-511A` is located on the upper service-water branch/header side, and the immediate local branch valve to its left/lower side is `HV-511A`. The `FCV-511A` and `FCV-511B` valve symbols are the named components on the service-water branches that descend into the cooler manifold near `HX-301A` and onward toward the `HX-301B` area. Keeping the older HV-to-HX edges skipped over these nearer named valve endpoints.

### FH-301 / FT-203 / HV-203 / FCV-203 Bypass Area

Accepted Jennifer change:

- Removed `FH-301 -- HV-203`; accepted `FT-203 -- HV-203`.

Raw-image evidence: in `05_filter_inlet_and_pump_headers_raw.png` and `06_filter_cooler_a_b_raw.png`, `FT-203` is drawn directly on the vertical filter-inlet/header segment below `FH-301`, before the lower horizontal branch toward `HV-203`/`FCV-203`. The older `FH-301 -- HV-203` edge skipped this named endpoint, so `FH-301 -- FT-203 -- HV-203` is the more local representation.

### TIC-310 Termination Near HV-512B

Accepted Jennifer change:

- Removed `TIC-310 -- HV-512B`.

Raw-image evidence: in `07_supply_return_controls_top_raw.png` and `08_right_controls_v401_raw.png`, the dot-dashed/dashed TIC-310 path runs through a crowded area near `HV-512A`, `TI-512A`, `TT-310`, `FT-401`, and `HV-512B`, but it does not visibly terminate on `HV-512B`. The supported direct endpoints remain the clearer temperature/control links already in Jennifer's matrix.

## Saturation Check

I did not add any new edges beyond Jennifer's matrix. The reviewed regions already include the visually supported local chains without adding anonymous junctions, WN nodes, crossing points, or header clique expansions.

## Basic Validation

- Node count: 189
- Edge count: 212
- Shape/header check: pass
- Diagonal check: pass
- Symmetry check: pass
- Isolated nodes: 0
- Matrix provenance: exact copy of `round_01_jennifer_matrix.csv`
