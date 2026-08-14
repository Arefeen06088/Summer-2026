# Document 21 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 21 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 21 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 51510 | 47134 | 40000 | 113291 | 148144 | 216425 |
| 21 | 1 | Jennifer: round1_precision_review | 52534 | unavailable | 51510 | 48425 | 36000 | 154699 | 188469 | 253524 |
| 21 | 1 | Diego: round2_saturation_review | 78487 | unavailable | 0 | 47529 | 10500 | 113305 | 136516 | 175534 |
| 21 | 1 | Jennifer: round2_final_precision_confirmation | 79482 | unavailable | 17680 | 49334 | 14500 | 135463 | 160996 | 205097 |
| 21 | 1 | **TOTAL** | 250003 | unavailable | 122910 | 194622 | 123000 | 563488 | 690535 | 930310 |
