# Document 26 Round 01 Diego Notes

## Method

- Inspected the raw schematic first, then checked the label overlay, wire-node overlay, wire mask overlay, and precision review crops.
- Used `component_index_by_position.csv` only as a label/position aid after visual inspection. No Ground Truth, evaluator output, previous-document connectivity, or off-the-shelf OCR was used.
- Modeled all 190 visible tagged physical components as nodes, plus 10 named logical bus backbones: BUS-416A, BUS-416B, BUS-480A, BUS-480B, BUS-125DCA, BUS-125DCB, BUS-INV-A, BUS-INV-B, BUS-120N-A, and BUS-120N-B.
- Treated crossings without visible junction dots as non-connections. Small wire labels such as 480-A-11, DC-A-INV, and 120-A-N were used as evidence but not promoted to nodes because the named bus/backbone node captures the physical connection.

## Counts

- Node count: 200
- Edge count: 209
- Edge kind counts: {'bus_tie': 6, 'control_interlock': 10, 'ground': 8, 'instrument_signal': 16, 'power_feeder': 169}
- Confidence counts: {'high': 195, 'low': 4, 'medium': 10}

## Assumptions

- Breakers/contactors are modeled as graph nodes with two adjacent conductor edges where they are visually in series with a feeder.
- Named horizontal double-line buses are explicit logical nodes and absorb the repeated bus tap/junction points.
- The three bus-tie breakers are represented by two `bus_tie` edges each: bus-to-tie and tie-to-bus.
- Dotted relay-to-terminal-block-to-PT paths are `instrument_signal`; dashed interlock/control paths are `control_interlock`.

## Ambiguous Or Lower-Confidence Items

- `CB-4A03 -- MTR-RCP-A` and `CB-4B03 -- MTR-RCP-B`: dashed protection/control routes run beside the RCP feeder branches; direct endpoint is visually inferred from proximity to the motor/grounded branch.
- `CB-480A13 -- STR-A3-3` and `CB-480B13 -- STR-B3-3`: dashed routes leave the LC-31A3/LC-31B3 breaker area and touch the third starter branch; they are parallel to solid feeder chains and should be scrutinized.
- `CB-INV-A -- INV-31A` and `CB-INV-B -- INV-31B`: the DC inverter breaker, DC bus tap, and inverter are vertically aligned; the in-series relation is plausible but the bus crossing is visually dense.
- `BUS-INV-A/B -- PNL-AC-A/B` and `PNL-AC-A/B -- BUS-120N-A/B`: lower panel routing is partially overlapped by dashed verticals and terminal ticks.
- `STR-A1-1 -- BAT-31A`, `STR-B1-1 -- BAT-31B`, and the dashed battery-to-charger control links are visible but represent control/interlock routing rather than solid feeder power.

## Rejected Or Not Modeled

- Descriptive zone labels such as `4.16 kV SAFETY BUS - TRAIN A`, `480 V LOAD CENTER / MCC - TRAIN A`, and title-block/legend/note text were not modeled as connection nodes.
- Small branch/wire labels (`4-416-A-01`, `480-A-11`, `DC-A-INV`, `120-A-N`, etc.) were retained only in evidence text, not as separate graph nodes.
- Unnamed wire-node overlay IDs were not introduced as graph nodes.
- Dashed vertical routes that merely cross named buses without a visible junction dot were not connected to those buses.
- The drawing border, revision table, legend symbols, and sheet title block were excluded from the connectivity graph.

## Validation

- No unknown nodes in edges.
- No duplicate undirected edge pairs.
- Adjacency matrix is symmetric.
- Adjacency matrix diagonal is zero.
