# Document 37 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 37 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 37 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 52190 | 7707 | 40000 | 90315 | 109397 | 154022 |
| 37 | 1 | Jennifer: round1_precision_review | 13107 | unavailable | 52190 | 7702 | 36000 | 91519 | 108999 | 149621 |
| 37 | 1 | Diego: round2_saturation_review | 18437 | unavailable | 0 | 7991 | 10500 | 29532 | 36928 | 52223 |
| 37 | 1 | Jennifer: round2_final_precision_confirmation | 19321 | unavailable | 18020 | 9752 | 14500 | 51893 | 61593 | 81945 |
| 37 | 1 | **TOTAL** | 90365 | unavailable | 124610 | 35352 | 123000 | 309989 | 373327 | 517541 |
