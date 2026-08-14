# Document 19 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 19 | 1 | Main Codex: main_orchestration_grouped | 23000 | unavailable | 9945 | 1300 | 19000 | 41325 | 53245 | 73025 |
| 19 | 1 | Diego: diego_round1_high_recall_extraction | 6100 | unavailable | 18530 | 32129 | 32000 | 56708 | 88759 | 140037 |
| 19 | 1 | Jennifer: jennifer_round1_precision_review | 38929 | unavailable | 18530 | 32342 | 30000 | 88865 | 119801 | 169207 |
| 19 | 1 | Diego: diego_round2_saturation_review | 35342 | unavailable | 0 | 32189 | 8500 | 58056 | 76031 | 103845 |
| 19 | 1 | Jennifer: jennifer_round2_final_confirmation | 34589 | unavailable | 0 | 32287 | 7000 | 56762 | 73876 | 100249 |
| 19 | 1 | **TOTAL** | 137960 | unavailable | 47005 | 130247 | 96500 | 301716 | 411712 | 586363 |
