# Document 12 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 12 | 1 | Main Codex: main_orchestration_grouped | 16075 | 14875 | 900 | 18000 | 21750 | 34975 | 62200 |
| 12 | 1 | Diego: diego_round1_high_recall_extraction | 13315 | 12665 | 91779 | 24000 | 90150 | 129094 | 188039 |
| 12 | 1 | Jennifer: jennifer_round1_precision_review | 93771 | 14875 | 21188 | 22000 | 117662 | 136959 | 175256 |
| 12 | 1 | Diego: diego_round2_saturation_review | 21518 | 0 | 20897 | 8000 | 39191 | 50415 | 67640 |
| 12 | 1 | Jennifer: jennifer_round2_final_confirmation | 21217 | 0 | 28017 | 6000 | 44230 | 55234 | 72239 |
| **12** | **1** | **TOTAL** | **165896** | **42415** | **162781** | **78000** | **312983** | **406677** | **565374** |
