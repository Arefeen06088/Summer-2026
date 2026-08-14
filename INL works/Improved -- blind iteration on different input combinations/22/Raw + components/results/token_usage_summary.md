# Document 22 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 22 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 9945 | 2200 | 22000 | 54465 | 64145 | 87465 |
| 22 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 51510 | 44907 | 40000 | 111955 | 145917 | 212862 |
| 22 | 1 | Jennifer: round1_precision_review | 50307 | unavailable | 34000 | 45264 | 36000 | 133066 | 165571 | 228730 |
| 22 | 1 | Diego: round2_saturation_attempt_failed_503 | 73043 | unavailable | 0 | 0 | 3000 | 74843 | 76043 | 79043 |
| 22 | 1 | Diego: round2_saturation_review_fresh_spawn | 73643 | unavailable | 11135 | 46538 | 10500 | 119001 | 141816 | 180239 |
| 22 | 1 | Jennifer: round2_final_precision_confirmation | 75274 | unavailable | 9945 | 45656 | 14500 | 121313 | 145375 | 187269 |
| 22 | 1 | **TOTAL** | 311767 | unavailable | 116535 | 184565 | 126000 | 614643 | 738867 | 975608 |
