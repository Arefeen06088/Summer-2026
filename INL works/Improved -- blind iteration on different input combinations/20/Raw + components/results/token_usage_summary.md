# Document 20 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 20 | 1 | Main Codex: orchestration_visual_review_packaging | 26000 | unavailable | 10030 | 1600 | 22000 | 45790 | 59630 | 82590 |
| 20 | 1 | Diego: round1_high_recall_extraction | 6200 | unavailable | 18955 | 132740 | 34000 | 118399 | 191895 | 305539 |
| 20 | 1 | Jennifer: round1_precision_review | 139940 | unavailable | 18955 | 132781 | 32000 | 251364 | 323676 | 435345 |
| 20 | 1 | Diego: round2_saturation_review | 248170 | unavailable | 0 | 133345 | 9000 | 331777 | 390515 | 479522 |
| 20 | 1 | Jennifer: round2_final_confirmation | 248375 | unavailable | 0 | 42451 | 8000 | 277046 | 298826 | 332297 |
| 20 | 1 | **TOTAL** | 668685 | unavailable | 47940 | 442917 | 105000 | 1024376 | 1264542 | 1635293 |
