# Token Usage Estimate - Document 3, Iteration 1

No OpenAI API key was available, so the Responses input-token counting endpoint was not called. Actual usage objects were not exposed by the Codex subagent tools. Estimates use local text token counting where possible plus a high-detail image tiling heuristic.

Low / expected / high total estimate: 70,515 / 101,615 / 142,005 tokens.

| Call | Actor | Round | Input exp | Cached exp | Image exp | Output exp | Reasoning exp | Total low/exp/high |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| main_01_intake_crop_spawn | Main | setup | 2,600 | 0 | 0 | 900 | 1,500 | 3,285/5,000/7,310 |
| diego_01_high_recall_extract | Diego | round1 | 4,565 | 0 | 3,315 | 3,600 | 4,500 | 8,014/12,665/19,029 |
| jennifer_01_precision_review | Jennifer | round1 | 19,010 | 0 | 15,810 | 3,100 | 4,800 | 18,673/26,910/37,608 |
| main_02_visual_crosscheck | Main | between_rounds | 13,025 | 0 | 10,625 | 1,200 | 2,200 | 11,649/16,425/22,522 |
| diego_02_narrow_recheck | Diego | round2 | 8,215 | 7,515 | 0 | 1,900 | 2,600 | 8,696/12,715/17,985 |
| jennifer_02_final_resolution | Jennifer | round2_final | 22,660 | 22,010 | 0 | 90 | 850 | 17,478/23,600/31,076 |
| main_03_artifacts_final | Main | artifacts | 1,800 | 0 | 0 | 800 | 1,700 | 2,720/4,300/6,475 |

## Method Notes
- The subagent model calls were Diego R1, Jennifer R1, Diego R2, and Jennifer final R2, all requested with `gpt-5.5`.
- Main-agent calls are grouped into logical workflow phases because exact internal Codex model-call boundaries and usage objects are not available.
- Cached input token estimates are only estimates for follow-up messages in the same subagent thread.
- Image/file input token estimates are already included in the input-token estimates.
