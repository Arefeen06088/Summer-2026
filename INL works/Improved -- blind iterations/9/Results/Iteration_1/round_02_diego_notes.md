# Round 02 Diego Notes

## Scope and decision

Reviewed only doc 9 input resources, generated inspection crops, and Jennifer's Round 1 refinement files. I did not use GT, evaluator output, validation metrics, or any answer key material.

I agree with Jennifer's precision decisions and made no node or edge changes. `round_02_diego_nodes.csv` is the accepted Jennifer node set, and `round_02_diego_edges.csv` is the accepted Jennifer edge set.

## Re-check points

1. `CB-TIE-41N` dashed trip/control ownership: keep out/uncertain. The raw and wire-node crops show dashed drops/bends near `CB-TIE-41N`, but the route merges into broader dashed control/interlock geometry without a clean named relay endpoint. A direct `CB-TIE-41N -- RELAY-86A` or `CB-TIE-41N -- RELAY-86B` edge would overclaim terminal ownership.

2. B-side `RELAY-86B` to `CB-481B` / `CB-482B`: keep both out/uncertain. `RELAY-86B -- RELAY-27B` is visually supported, but the B-side dashed paths run near `CB-481B` and across/near `CB-482B` without an unambiguous endpoint into either breaker. No exact breaker trip edge should be promoted from the current visual evidence.

3. A-side `PN-MOV-A` upstream feed: keep `FAN-CR-A -- PN-MOV-A`. The visible solid conductor continues from the `FAN-CR-A` vertical branch and angles into `PN-MOV-A`; a direct `MCC-SAF-A2 -- PN-MOV-A` edge would bypass visible named intermediate geometry and is less faithful to the endpoint-to-endpoint drawing.

4. Junction-box labels: agree with `JB-1A`, `JB-2A`, `JB-1B`, and `JB-2B`. The raw lower-control crops show the side circles as terminal marks beside the junction boxes, not trailing `O` or `0` label characters.

## Saturation note

The graph is saturated for the requested round-2 checks: keeping the ambiguous dashed trip/interlock candidates out preserves precision, while the accepted dashed/control edges have named endpoints visible in the raw crops.
