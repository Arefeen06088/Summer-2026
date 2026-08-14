# Document 41 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 41 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 41 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 51510 | 13679 | 40000 | 93218 | 114689 | 162897 |
| 41 | 1 | Jennifer: round1_precision_review | 19079 | unavailable | 51510 | 9341 | 36000 | 97794 | 115930 | 157535 |
| 41 | 1 | Diego: round2_saturation_review | 25719 | unavailable | 0 | 14045 | 10500 | 40446 | 50264 | 69191 |
| 41 | 1 | Jennifer: round2_final_precision_confirmation | 26685 | unavailable | 17680 | 9842 | 14500 | 58971 | 68707 | 89113 |
| 41 | 1 | **TOTAL** | 110983 | unavailable | 122910 | 49107 | 123000 | 337159 | 406000 | 558466 |
