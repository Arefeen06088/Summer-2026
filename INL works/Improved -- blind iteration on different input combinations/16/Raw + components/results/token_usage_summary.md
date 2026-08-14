# Document 16 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent tool did not expose usage objects, cached input tokens, or reasoning-token counts. Text/file input estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 16 | 1 | Main Codex: main_orchestration_grouped | 24000 | unavailable | 13600 | 1300 | 20000 | 46380 | 58900 | 79680 |
| 16 | 1 | Diego: diego_round1_high_recall_extraction | 6800 | unavailable | 29155 | 27969 | 32000 | 65537 | 95924 | 144706 |
| 16 | 1 | Jennifer: jennifer_round1_precision_review | 34969 | unavailable | 29155 | 28277 | 30000 | 93091 | 122401 | 169368 |
| 16 | 1 | Diego: diego_round2_saturation_review | 31277 | unavailable | 0 | 28131 | 9000 | 51756 | 68408 | 94287 |
| 16 | 1 | Jennifer: jennifer_round2_final_confirmation | 30531 | unavailable | 0 | 28204 | 7000 | 50254 | 65735 | 89658 |
| 16 | 1 | **TOTAL** | 127577 | unavailable | 71910 | 113881 | 98000 | 307018 | 411368 | 577699 |
