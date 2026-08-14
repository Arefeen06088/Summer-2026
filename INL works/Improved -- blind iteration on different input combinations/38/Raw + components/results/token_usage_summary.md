# Document 38 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 38 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 38 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 52190 | 11361 | 40000 | 92507 | 113051 | 159868 |
| 38 | 1 | Jennifer: round1_precision_review | 16761 | unavailable | 52190 | 11075 | 36000 | 97196 | 116026 | 158671 |
| 38 | 1 | Diego: round2_saturation_review | 24059 | unavailable | 0 | 9968 | 10500 | 36340 | 44527 | 61008 |
| 38 | 1 | Jennifer: round2_final_precision_confirmation | 23761 | unavailable | 18020 | 11191 | 14500 | 57196 | 67472 | 88687 |
| 38 | 1 | **TOTAL** | 104081 | unavailable | 124610 | 45795 | 123000 | 329969 | 397486 | 547964 |
