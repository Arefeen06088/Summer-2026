# Document 15 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 15 | 1 | Main Codex: main_orchestration_grouped | 22000 | unavailable | 18360 | 1200 | 18000 | 48280 | 59560 | 78280 |
| 15 | 1 | Diego: diego_round1_high_recall_extraction | 5200 | unavailable | 16915 | 26829 | 30000 | 50213 | 78944 | 125042 |
| 15 | 1 | Jennifer: jennifer_round1_precision_review | 33329 | unavailable | 16915 | 30467 | 28000 | 79725 | 108711 | 154992 |
| 15 | 1 | Diego: diego_round2_saturation_review | 33267 | unavailable | 0 | 30442 | 8000 | 54733 | 71709 | 97975 |
| 15 | 1 | Jennifer: jennifer_round2_final_confirmation | 32642 | unavailable | 0 | 27671 | 6000 | 51645 | 66313 | 88916 |
| 15 | 1 | **TOTAL** | 126438 | unavailable | 52190 | 116609 | 90000 | 284596 | 385237 | 545205 |
