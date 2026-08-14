# Document 9 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 9 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 9 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 52190 | 33648 | 40000 | 105879 | 135338 | 195527 |
| 9 | 1 | Jennifer: round1_precision_review | 39048 | unavailable | 52190 | 44252 | 36000 | 139390 | 171490 | 234042 |
| 9 | 1 | Diego: round2_saturation_review | 65612 | unavailable | 0 | 34814 | 10500 | 92801 | 110926 | 142315 |
| 9 | 1 | Jennifer: round2_final_precision_confirmation | 67378 | unavailable | 18020 | 46901 | 14500 | 122239 | 146799 | 189440 |
| 9 | 1 | **TOTAL** | 211538 | unavailable | 124610 | 161815 | 123000 | 507039 | 620963 | 841054 |
