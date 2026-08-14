# Token Usage Estimate - Document 5, Iteration 1

No OpenAI API key was available, so the Responses input-token counting endpoint was not called. Actual usage objects were not exposed by the Codex subagent tools. Estimates use local text-token approximation plus a high-detail image tiling heuristic.

Low / expected / high total estimate: 115,719 / 164,940 / 228,299 tokens.

| Call | Actor | Round | Input exp | Cached exp | Image exp | Output exp | Reasoning exp | Total low/exp/high |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| main_01_intake_crop_spawn | Main | setup | 3,100 | 0 | 0 | 1,100 | 1,900 | 3,990/6,100/8,950 |
| diego_01_high_recall_extract | Diego | round1 | 4,765 | 0 | 3,315 | 4,700 | 5,800 | 9,529/15,265/23,159 |
| main_02_visual_crosscheck | Main | round1_review_prep | 27,210 | 0 | 22,610 | 1,900 | 3,600 | 23,443/32,710/44,428 |
| jennifer_01_precision_review | Jennifer | round1 | 26,845 | 0 | 21,845 | 3,900 | 5,900 | 25,619/36,645/50,878 |
| diego_02_narrow_recheck | Diego | round2 | 20,945 | 8,515 | 10,030 | 3,700 | 4,300 | 20,264/28,945/40,118 |
| jennifer_02_final_audit | Jennifer | round2_final | 37,555 | 30,045 | 5,610 | 420 | 1,600 | 29,239/39,575/52,231 |
| main_03_artifacts_final | Main | artifacts | 2,600 | 0 | 0 | 900 | 2,200 | 3,635/5,700/8,535 |

## Method Notes
- Subagent calls were Diego R1, Jennifer R1, Diego R2, and Jennifer final R2, all requested with `gpt-5.5`.
- Main-agent calls are grouped into logical workflow phases because exact internal Codex model-call boundaries are unavailable.
- Cached input token estimates are estimates for follow-up messages in the same subagent thread.
- Image/file input token estimates are already included in input-token estimates.
