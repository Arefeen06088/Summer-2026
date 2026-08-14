# Document 38 Iteration 1 Round Log

Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires`

Ground-truth policy: no GT or GT-derived files used. Only Raw + wires images and generated crops from that folder were inspected.

Rounds:
1. Diego R1 high-recall extraction: proposed 54 nodes and included dashed/control ambiguous edges in the draft matrix.
2. Jennifer R1 precision review: normalized batteries to `BAT-125A/B`, removed dashed/control/ground edges, excluded `TR-CPT-A--BUS-120AC-A`, kept `BUS-120AC-B--RELAY-27B`.
3. Diego R2 reconciliation: agreed with Jennifer R1 and reported consensus, while omitting isolated relay nodes from his proposed final node list.
4. Jennifer R2 final confirmation: final node policy applied in generated final files.

Final validation:
- Nodes: 54
- Edges: 51
- Symmetric: True
- Diagonal zero: True

Final excluded/uncertain:
- Dashed control/routing/ground paths are excluded.
- `TR-CPT-A--BUS-120AC-A` excluded due visible gap/terminal dot rather than solid tie.
- `125VDC-TRAIN-A/B--RELAY-86A/B`, `BUS-120AC-A--RELAY-27A`, and relay-to-RPS dashed paths excluded.
- Direct bus collapses (`BUS-4160A--BUS-4160B`, `BUS-480A--BUS-480B`) excluded.
- `S-125DC-A/B` treated as equipment text associated with `BAT-125A/B`, not separate nodes.
