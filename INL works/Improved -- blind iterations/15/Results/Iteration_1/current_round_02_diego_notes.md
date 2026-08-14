# Current Round 02 - Diego Saturation Notes

## Source Boundary And Node Policy
- Reviewed only doc 15 Input resources, current doc 15 support artifacts/crops, Diego Round 1 files, and Jennifer Round 1 files.
- Used the exact 183-node order from `component_inventory_doc15_current.csv`.
- Did not add WN-* wire nodes, anonymous junctions, old result files, GT/evaluation files, title/legend/schedule text, or the removed `OFFSITE SOURCES` label.

## Agreement Decision
- I agree exactly with Jennifer's 196-edge Round 1 matrix.
- `current_round_02_diego_edges.csv` is an exact copy of `current_round_01_jennifer_edges.csv`.
- `current_round_02_diego_matrix.csv` is an exact copy of `current_round_01_jennifer_matrix.csv`.
- No edge deltas were introduced in Diego Round 2.

## Focused Re-Review
- `SEQ-1AB -- RPS-AC-1` and `SEQ-2CD -- RPS-AC-2` should remain removed. The tie-control crops show shared dashed side risers, but no direct named block-to-block landing.
- `BUS-NSS-1 -- DG-1A` and `BUS-NSS-2 -- DG-1C` should remain as low-confidence high-recall edges. The NSS bus line is visually drawn through those DG symbols with wire-node markers at the symbol sides; symbol-overlap remains possible, so the uncertain classification is appropriate.
- No analogous `BUS-NSS -- DG-1B/D` edge should be added. The B and D medium-voltage crops do not show the same clear inline bus passage through the DG symbol.
- Dashed CB-to-relay leads should remain. Across the MCC load crops, each dashed lead visibly leaves its matching feeder breaker and lands at the corresponding relay block.
- `RLY-A06/B06/C06/D06 -- TB-1A/B/C/D` should remain as uncertain control edges. The sixth-relay dashed lead exits the MCC crop downward and reappears at the matching terminal block area; the middle span is sparse, but this is plausible enough for saturation/high-recall retention.
- Tie-control edges from `SEQ/RPS` blocks to the nearby normal/diesel breaker control network should remain uncertain, not expanded. The dashed risers support the retained named endpoint associations, but they do not justify additional fan-out to the solid tie devices or direct `SEQ -- RPS` shortcuts.
- DC bus-to-ground and CP/TB/JB edges are immediate enough to retain. The DC crops show the bus-to-ground tap landing on the ground symbol and the CP dashed conductors landing on TB and JB.

## Saturation Judgment
- From Diego's Round 2 review, visual saturation is reached for the current source set and 183-node inventory.
- Remaining questionable edges are already marked lower-confidence and are appropriate for Jennifer/final precision review rather than another high-recall expansion.

## Output Summary
- Edge proposals written: 196.
- Matrix size: 183 x 183 plus leading `node_name` column.
- Round 2 deltas versus Jennifer Round 1: none.
