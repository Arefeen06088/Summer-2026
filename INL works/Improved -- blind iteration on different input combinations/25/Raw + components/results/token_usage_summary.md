# Document 25 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 25 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 32000 | unavailable | 7480 | 2200 | 24000 | 50400 | 65680 | 91000 |
| 25 | 1 | Diego: round1_high_recall_extraction | 8000 | unavailable | 32130 | 43740 | 38000 | 81574 | 121870 | 186114 |
| 25 | 1 | Jennifer: round1_precision_review | 52240 | unavailable | 32130 | 44162 | 35000 | 124868 | 163532 | 225030 |
| 25 | 1 | Diego: round2_saturation_review | 70574 | unavailable | 0 | 43965 | 10000 | 100953 | 124539 | 160918 |
| 25 | 1 | Jennifer: round2_final_precision_confirmation | 71499 | unavailable | 32130 | 44239 | 14000 | 135773 | 161868 | 202412 |
| 25 | 1 | **TOTAL** | 234313 | unavailable | 103870 | 178306 | 121000 | 493568 | 637489 | 865474 |
