# Document 23 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 23 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 31000 | unavailable | 6715 | 2200 | 24000 | 48635 | 63915 | 89235 |
| 23 | 1 | Diego: round1_high_recall_extraction | 7600 | unavailable | 25670 | 134831 | 38000 | 129369 | 206101 | 325000 |
| 23 | 1 | Jennifer: round1_precision_review | 143031 | unavailable | 25670 | 136141 | 35000 | 264386 | 339842 | 456527 |
| 23 | 1 | Diego: round2_saturation_review | 254334 | unavailable | 0 | 135537 | 10000 | 339657 | 399871 | 491194 |
| 23 | 1 | Jennifer: round2_final_precision_confirmation | 255440 | unavailable | 25670 | 45130 | 14000 | 313788 | 340240 | 381318 |
| 23 | 1 | **TOTAL** | 691405 | unavailable | 83725 | 453839 | 121000 | 1095835 | 1349969 | 1743274 |
