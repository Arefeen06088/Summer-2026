# Document 17 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 17 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 17 | 1 | Diego: round1_high_recall_extraction | 9000 | unavailable | 54230 | 44660 | 40000 | 114026 | 147890 | 214686 |
| 17 | 1 | Jennifer: round1_precision_review | 49860 | unavailable | 54230 | 44793 | 36000 | 152566 | 184883 | 247759 |
| 17 | 1 | Diego: round2_saturation_review | 71315 | unavailable | 0 | 44675 | 10500 | 104420 | 126490 | 163795 |
| 17 | 1 | Jennifer: round2_final_precision_confirmation | 71930 | unavailable | 19040 | 54677 | 14500 | 132477 | 160147 | 207454 |
| 17 | 1 | **TOTAL** | 232105 | unavailable | 129710 | 191005 | 123000 | 550219 | 675820 | 913424 |
