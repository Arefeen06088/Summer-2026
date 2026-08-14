# Round 02 Diego Saturation Notes - Doc 18

Scope: saturation review of Jennifer's precision pass using only doc 18 Input resources and generated inspection artifacts. No GT, evaluator feedback, metric feedback, or prior document outputs used.

## Saturation Decision

I agree fully with Jennifer's round 01 precision matrix. I copied `round_01_jennifer_matrix.csv` exactly to `round_02_diego_matrix.csv`; no edge or node changes were made.

Final accepted matrix state:

- Matrix nodes: 201.
- Accepted undirected edges: 189.
- Row and column labels: identical and in the same order.
- Diagonal: all 0.
- Symmetric: yes.

## Reviewed Corrections

- `CB-SWYD-230` remains isolated. In the top-left raw crop, the detection lies over the printed `BB-SWYD-230` junction/heavy-bus label area; no separate breaker/protector symbol is visible there.
- `CB-GRID-A -> BB-SWYD-230` and `CB-GRID-B -> BB-SWYD-230` are accepted as direct solid source-to-switchyard-bus edges.
- `CB-GRID-A -> CB-SWYD-230`, `CB-GRID-B -> CB-SWYD-230`, and `CB-SWYD-230 -> BB-SWYD-230` remain rejected because `CB-SWYD-230` is not a distinct visible endpoint.
- `CB-UAT-A -> BUS-4160B` and `CB-UAT-B -> BUS-4160B` remain rejected. The top-right UAT close-up shows each UAT breaker connected upward to its transformer only; the lower breaker sides stop above the 4.16 kV bus with visible white space and no tap/junction.
- `BUS-4160A -> TB-RPS-A -> TR-480-A1` remains accepted. The A-side solid feeder visibly enters and exits `TB-RPS-A`; this is separate from the dashed PT/control chain.
- `TB-RPS-B` remains dashed-control only, with no solid transformer-feed analog visible.
- `BUS-480B -> CHG-125A` and `BUS-480C -> CHG-125B` remain accepted as long continuous solid charger feeds.
- The regular 480 V load-center branch chains and the direct lower DC/AC rail edges remain accepted.
- The relay/JB/annunciator clusters remain out of the matrix because their dashed routing is shared and endpoint assignment is not visually reliable enough.

## Remaining Uncertain/Plausible Edges Kept Out Of Matrix

These are plausible from dashed/control routing but are not encoded in `round_02_diego_matrix.csv`.

| # | Node A | Node B | Why uncertain |
|---:|---|---|---|
| 1 | `PLC-RPS-A` | `RELAY-K101` | Dashed output bundle from `PLC-RPS-A` appears to route into the relay cluster, but multiple parallel dashed legs share a vertical riser. |
| 2 | `PLC-RPS-A` | `RELAY-K102` | Plausible upper relay-loop path, but exact endpoint assignment is ambiguous near shared dashed routing. |
| 3 | `PLC-RPS-A` | `RELAY-K103` | Lower dashed branch reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 4 | `PLC-RPS-A` | `RELAY-K104` | Lower dashed branch reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 5 | `RELAY-K101` | `JB-RPS-A` | `JB-RPS-A` is adjacent to the relay cluster; dashed routing suggests a possible endpoint, but no clean isolated terminal connection is visible. |
| 6 | `RELAY-K102` | `JB-RPS-A` | `JB-RPS-A` lies by the upper dashed relay route; path/endpoint remains visually ambiguous. |
| 7 | `RELAY-K102` | `PNL-ANN-A` | Dashed route drops from the upper relay area toward `PNL-ANN-A`, but it shares bends and possible junctions with the relay loop. |
| 8 | `RELAY-K104` | `PNL-ANN-A` | Lower relay loop is routed near `PNL-ANN-A`; endpoint is plausible but not unambiguous. |
| 9 | `PLC-RPS-B` | `RELAY-K201` | Dashed output bundle from `PLC-RPS-B` appears to route into the relay cluster, but multiple parallel dashed legs share a vertical riser. |
| 10 | `PLC-RPS-B` | `RELAY-K202` | Plausible upper relay-loop path, but exact endpoint assignment is ambiguous near shared dashed routing. |
| 11 | `PLC-RPS-B` | `RELAY-K203` | Lower dashed branch reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 12 | `PLC-RPS-B` | `RELAY-K204` | Lower dashed branch reaches the lower relay loop, but exact relay endpoint is not isolated cleanly. |
| 13 | `RELAY-K201` | `JB-RPS-B` | `JB-RPS-B` is adjacent to the upper relay route; possible dashed endpoint, but no clean direct connection is visible. |
| 14 | `RELAY-K202` | `JB-RPS-B` | `JB-RPS-B` lies by the upper dashed relay route; path/endpoint remains visually ambiguous. |
| 15 | `RELAY-K202` | `PNL-ANN-B` | Dashed route drops from `RELAY-K202` toward `PNL-ANN-B`, but it shares relay-loop routing. |
| 16 | `RELAY-K204` | `PNL-ANN-B` | Lower relay loop is routed near `PNL-ANN-B`; endpoint is plausible but not unambiguous. |

## Validation

Round 02 validation was run after saving:

- `round_02_diego_matrix.csv` is 201 x 201.
- Row labels equal column labels.
- Diagonal entries are all 0.
- Matrix is symmetric.
- Accepted undirected edge count is 189.

