# Document 40 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 40 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 40 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 51510 | 9812 | 40000 | 90898 | 110822 | 156710 |
| 40 | 1 | Jennifer: round1_precision_review | 15212 | unavailable | 51510 | 15325 | 36000 | 97517 | 118047 | 163242 |
| 40 | 1 | Diego: round2_saturation_review | 27917 | unavailable | 0 | 10043 | 10500 | 40243 | 48460 | 64986 |
| 40 | 1 | Jennifer: round2_final_precision_confirmation | 28748 | unavailable | 17680 | 15882 | 14500 | 64658 | 76810 | 100840 |
| 40 | 1 | **TOTAL** | 111377 | unavailable | 122910 | 53262 | 123000 | 340046 | 410549 | 565508 |
