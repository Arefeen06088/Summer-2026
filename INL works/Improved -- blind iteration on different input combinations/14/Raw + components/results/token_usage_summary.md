# Document 14 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 14 | 1 | Main Codex: main_orchestration_grouped | 20950 | 19550 | 900 | 18000 | 26625 | 39850 | 67075 |
| 14 | 1 | Diego: diego_round1_high_recall_extraction | 19505 | 18785 | 28395 | 30000 | 50802 | 77900 | 129999 |
| 14 | 1 | Jennifer: jennifer_round1_precision_review | 32014 | 19550 | 28605 | 28000 | 63468 | 88619 | 137771 |
| 14 | 1 | Diego: diego_round2_saturation_review | 28965 | 0 | 27898 | 8000 | 51889 | 64863 | 83838 |
| 14 | 1 | Jennifer: jennifer_round2_final_confirmation | 28238 | 0 | 38892 | 6000 | 59407 | 73130 | 92853 |
| **14** | **1** | **TOTAL** | **129672** | **57885** | **124690** | **90000** | **252191** | **344362** | **511536** |
