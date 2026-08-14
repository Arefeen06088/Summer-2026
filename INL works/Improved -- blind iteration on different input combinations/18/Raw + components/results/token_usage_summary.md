# Document 18 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 18 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 18 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 71570 | 39397 | 40000 | 128709 | 160467 | 224106 |
| 18 | 1 | Jennifer: round1_precision_review | 44797 | unavailable | 71570 | 40330 | 36000 | 162165 | 192697 | 252895 |
| 18 | 1 | Diego: round2_saturation_review | 63218 | unavailable | 0 | 39694 | 10500 | 93335 | 113412 | 147729 |
| 18 | 1 | Jennifer: round2_final_precision_confirmation | 64115 | unavailable | 19040 | 47351 | 14500 | 120266 | 145006 | 187917 |
| 18 | 1 | **TOTAL** | 211630 | unavailable | 164390 | 168972 | 123000 | 551205 | 667992 | 892377 |
