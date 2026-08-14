# Document 24 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 24 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 32000 | unavailable | 7480 | 2200 | 24000 | 50400 | 65680 | 91000 |
| 24 | 1 | Diego: round1_high_recall_extraction | 8000 | unavailable | 31110 | 41763 | 38000 | 79368 | 118873 | 181931 |
| 24 | 1 | Jennifer: round1_precision_review | 50263 | unavailable | 31110 | 42001 | 35000 | 120574 | 158374 | 218575 |
| 24 | 1 | Diego: round2_saturation_review | 67348 | unavailable | 0 | 41854 | 10000 | 96461 | 119202 | 154315 |
| 24 | 1 | Jennifer: round2_final_attempt_context_overflow | 68139 | unavailable | 31110 | 0 | 0 | 99249 | 99249 | 99249 |
| 24 | 1 | Jennifer: round2_final_precision_confirmation_retry | 67739 | unavailable | 7480 | 42154 | 11000 | 104912 | 128373 | 164666 |
| 24 | 1 | **TOTAL** | 293489 | unavailable | 108290 | 169972 | 118000 | 550964 | 689751 | 909736 |
