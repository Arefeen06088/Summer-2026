# Case 22 Connectivity Extraction Note

Generated: 2026-07-14T08:47:12

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_clean.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the source/switchgear, 480 V train loads, 120 V control, and DC/UPS topology, including uncertain sync, relay-to-JB, and PT-to-ammeter candidates.
2. Jennifer precision review removed unsupported sync and relay-to-JB direct edges, added DC charger upstream feeders, and marked dashed/control edges as control associations.
3. Diego saturation review corrected the B charger source to `BUS-480-B 480V LOAD CENTER B`, rejected `XFMR-PT-1 -- METER-A01`, and kept diode OR devices only as 125 VDC bus taps.
4. Jennifer accepted Diego's final corrections and locked the final graph.

## Final Counts

- Nodes: 200
- Undirected edges in matrix: 209
- Diagonal: zero
- Matrix: symmetric

## Key Decisions

- `CB-DC-A1` is fed from `BUS-480-A 480V LOAD CENTER A`; `CB-DC-B1` is fed from `BUS-480-B 480V LOAD CENTER B`.
- `METER-V01` is connected to `XFMR-PT-1`; `METER-A01` remains a visible isolated/uncertain meter because its dashed lead does not visibly join the PT drop.
- `DIODE-OR-A/B` are connected to their 125 VDC buses; no diode-to-solenoid edges were added.
- Dashed RHR/SI interlocks, relay branches, RPS/ESF branches, and UPS panel feeds are retained as drawn control associations.
- Crossings without junction dots were not modeled as connections.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
