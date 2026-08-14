# Document 39 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 39 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 39 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 54230 | 8984 | 40000 | 93121 | 112714 | 158105 |
| 39 | 1 | Jennifer: round1_precision_review | 14384 | unavailable | 54230 | 8723 | 36000 | 95448 | 113337 | 154571 |
| 39 | 1 | Diego: round2_saturation_review | 20687 | unavailable | 0 | 12969 | 10500 | 34769 | 44156 | 62438 |
| 39 | 1 | Jennifer: round2_final_precision_confirmation | 25387 | unavailable | 19040 | 8834 | 14500 | 58428 | 67761 | 87562 |
| 39 | 1 | **TOTAL** | 99958 | unavailable | 129710 | 41710 | 123000 | 328496 | 394378 | 542406 |
