# Document 13 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 13 | 1 | Main Codex: main_orchestration_grouped | 26135 | 24735 | 900 | 18000 | 31810 | 45035 | 72260 |
| 13 | 1 | Diego: diego_round1_high_recall_extraction | 19675 | 18955 | 30165 | 30000 | 52299 | 79840 | 132382 |
| 13 | 1 | Jennifer: jennifer_round1_precision_review | 36157 | 24735 | 30972 | 28000 | 69386 | 95129 | 144872 |
| 13 | 1 | Diego: diego_round2_saturation_review | 31332 | 0 | 30644 | 8000 | 56315 | 69976 | 89637 |
| 13 | 1 | Jennifer: jennifer_round2_final_confirmation | 30984 | 0 | 41136 | 6000 | 63836 | 78120 | 98404 |
| **13** | **1** | **TOTAL** | **144283** | **68425** | **133817** | **90000** | **273646** | **368100** | **537555** |
