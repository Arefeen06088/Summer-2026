# Document 10 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 10 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 51510 | 20378 | 40000 | 97237 | 121388 | 173615 |
| 10 | 1 | Jennifer: round1_precision_review | 25778 | unavailable | 51510 | 21451 | 36000 | 111759 | 134739 | 183610 |
| 10 | 1 | Diego: round2_saturation_review | 38372 | unavailable | 0 | 22961 | 10500 | 58449 | 71833 | 96110 |
| 10 | 1 | Jennifer: round2_final_precision_confirmation | 41555 | unavailable | 17680 | 21595 | 14500 | 80892 | 95330 | 122787 |
| 10 | 1 | **TOTAL** | 145205 | unavailable | 122910 | 88585 | 123000 | 395067 | 479700 | 655852 |
