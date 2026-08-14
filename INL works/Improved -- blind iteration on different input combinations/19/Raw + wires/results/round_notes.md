# Document 19 Extraction Notes

Only resources in the `Raw + wires` folder were used. Existing validation/GT-derived result files were not opened.

Round summary:
- Diego round 1 represented the shared bottom source conductors as direct breaker-to-charger relations.
- Jennifer round 1 replaced those shortcuts with `UNLABELED-480-CP-A/B` logical conductor nodes and left the 480 bus-to-conductor edges uncertain.
- Diego round 2 accepted Jennifer's corrections and retained the two possible 480 bus-to-conductor edges for high recall.
- Jennifer round 2 ruled the 480 bus-to-conductor edges visually supported; saturation reached.

Final node count: 202
Final undirected edge count: 202

Final special cases:
- `PT-4160A` and `PT-4160B` are treated as dashed taps to the 4160 buses, not series devices.
- `VALVE-MOV601` has two dashed indication branches: to `INST-601` and to `LS-MOV601`; `LS-MOV601` then goes to `JB-601`.
- The B-side sixth load group is `RPS INSTR TRAIN B` with `701` labels, not a `602` MOV group.
- Control-power source conductors are represented as `UNLABELED-480-CP-A/B`, connected to their respective `BUS-480` nodes and to both the breaker/transformer and charger branches.
