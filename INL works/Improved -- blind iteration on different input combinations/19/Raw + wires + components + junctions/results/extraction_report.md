# Document 19 Connectivity Extraction Report

## Scope

- Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components + junctions`
- Ground truth / GT-derived resources: not used.
- OCR: no off-the-shelf OCR used. Labels were read by visual inspection of the raw image and deterministic crops/overlays.
- Final matrix format: dense symmetric CSV, zero diagonal.

## Agent Rounds

| Round | Agent | Outcome |
|---|---|---|
| 1 | Diego | High-recall extraction. Included all main buses, feeders, dashed control links, ties, MOV/RPS special links, and control/DC distribution. |
| 1 | Jennifer | Precision review. Corrected RPS chain to pass through `INST-701`; corrected MOV dashed chain through `[LS-MOV601]`; removed `CHGR-125B--BUS-120AC-B`; initially misread `CB-101/CB-102` as `CR-101/CR-102`. |
| 2 | Diego | Accepted edge refinements, disputed only `CR-101/CR-102`, proposing `CB-101/CB-102`. |
| 2 | Jennifer | Accepted 4x crop evidence for `CB-101/CB-102`; Diego and Jennifer saturated/agreed. |

## Final Corrections

- Final labels are `CB-101` and `CB-102`, verified from `raw__offsite_a_stack_4x.png`, `raw__offsite_b_stack_4x.png`, and matching component-overlay crops.
- Final RPS chain: `INST-RPS701--INST-701--JB-701`.
- Final MOV chain: `VALVE-MOV601--INST-601--[LS-MOV601]--JB-601`.
- No edge between `CHGR-125B` and `BUS-120AC-B`; the vertical line crosses the 120 VAC bus without a junction dot.

## Final Artifacts

- `final_matrix.csv`: 200 x 200 dense connectivity matrix.
- `final_sparse.csv`: sparse final edge list in matrix-row form.
- `final_edges.csv`: final edges with evidence notes.
- `final_nodes.txt`: final node order.
- `round_01_diego_*`, `round_01_jennifer_*`, `round_02_diego_*`, `round_02_jennifer_*`: round-by-round matrices, edges, sparse rows, and node orders.
- `round_manifest.json`: node/edge counts and artifact names.
- `token_usage_estimate.csv`: per-call token estimate.
- `token_usage_totals.csv`: document-level total token estimate.

## Validation

All generated dense matrices were mechanically checked:

- 200 nodes.
- 200 undirected edges.
- Symmetric adjacency.
- Diagonal values are all 0.

## Token Usage Estimate

Actual API usage objects were not available through the Codex subagent tooling, and no OpenAI API key was available for the Responses token counting endpoint. The estimator uses:

- local `tiktoken` where available;
- offline word/punctuation approximation if tokenizer files cannot be loaded;
- OpenAI-style high-detail image tile estimate: `85 + 170 * 512px tiles`;
- low / expected / high estimates for unknown output and reasoning tokens.

Document 19, iteration 1 estimate:

| Calls | Low | Expected | High |
|---:|---:|---:|---:|
| 6 | 70,602 | 101,214 | 149,506 |

