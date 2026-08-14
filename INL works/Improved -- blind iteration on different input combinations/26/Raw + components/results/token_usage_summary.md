# Document 26 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 26 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 32000 | unavailable | 7480 | 2200 | 24000 | 50400 | 65680 | 91000 |
| 26 | 1 | Diego: round1_high_recall_extraction | 8000 | unavailable | 33490 | 48592 | 38000 | 85846 | 128082 | 195238 |
| 26 | 1 | Jennifer: round1_precision_review | 57092 | unavailable | 33490 | 49156 | 35000 | 134076 | 174738 | 239232 |
| 26 | 1 | Diego: round2_saturation_review | 81284 | unavailable | 0 | 49071 | 10000 | 114727 | 140355 | 179798 |
| 26 | 1 | Jennifer: round2_final_precision_confirmation | 82463 | unavailable | 33490 | 49475 | 14000 | 151238 | 179428 | 223113 |
| 26 | 1 | **TOTAL** | 260839 | unavailable | 107950 | 198494 | 121000 | 536287 | 688283 | 928381 |
