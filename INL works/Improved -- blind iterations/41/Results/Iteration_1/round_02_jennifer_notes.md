# Round 02 Jennifer Notes - Doc 41 / Iteration 1

## Scope
- Performed final precision sanity check using only doc 41 input resources, generated artifacts/crops, the corrected inventory, and Diego Round 2 files.
- Did not use Results/evaluation files, validation metrics, ground truth, score feedback, or old prior outputs.
- Diego Round 2 matched the reviewed Jennifer Round 1 decisions, so no edge or matrix changes were made.

## No-change confirmation
- Copied `round_02_diego_edges.csv` exactly to `round_02_jennifer_edges.csv`.
- Copied `round_02_diego_matrix.csv` exactly to `round_02_jennifer_matrix.csv`.
- The copied edge and matrix file hashes match Diego Round 2 after copy.

## Final precision sanity checks
- `zoom_right_480_b_charger_feed__raw.png` still supports excluding `BUS-480E1B -- CHGR-125B`; the B charger AC feeder runs on the separate right-side `CABLE 1B-480-9` route and has no visible landing on `BUS-480E1B`.
- `BUS-480B -- CHGR-125B` remains a probable edge because the B charger feed is labeled/routed as the 1B-480 source, while the exact BUS-480B terminal landing is indirect.
- `middle_transformers_and_480_buses__raw.png` supports keeping `BUS-480B` and `BUS-480E1B` separate with no bus-tie edge.
- `zoom_center_vital_ups_panels_rack__raw.png` supports `UPS-BUS-A -- INST-RACK-1` and does not support `UPS-BUS-B -- INST-RACK-1`, `UPS-BUS-A -- UPS-BUS-B`, or direct RPS-panel-to-rack edges.
- The named dashed-control edges remain routed through the named relays, panels, and `JB-ESF-01`; no collapse through those named nodes was made.

## Validation counts
- Nodes in matrix: 58.
- Undirected edges: 60.
- Confidence counts: certain=57, probable=3, uncertain=0.
- Matrix shape: 58 rows by 58 columns, plus row-label column/header.
- Matrix row and column order matches `component_inventory_doc41.csv`.
- Matrix is symmetric; diagonal is zero.
- Matrix contains 120 directed one entries, matching 2 x 60 undirected edges.
- Edge CSV and matrix represent the same 60 undirected edges.
