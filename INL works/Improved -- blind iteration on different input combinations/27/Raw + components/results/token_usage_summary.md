# Document 27 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 27 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 34000 | unavailable | 7480 | 2200 | 24000 | 52400 | 67680 | 93000 |
| 27 | 1 | Diego: round1_high_recall_extraction | 8500 | unavailable | 31790 | 42969 | 40000 | 82072 | 123259 | 189041 |
| 27 | 1 | Jennifer: round1_precision_review | 51969 | unavailable | 31790 | 42979 | 36000 | 123947 | 162738 | 224526 |
| 27 | 1 | Diego: round2_saturation_review | 69095 | unavailable | 0 | 42910 | 10500 | 99041 | 122505 | 158751 |
| 27 | 1 | Jennifer: round2_final_precision_confirmation | 69636 | unavailable | 31790 | 51499 | 14500 | 138126 | 167425 | 212825 |
| 27 | 1 | **TOTAL** | 233200 | unavailable | 102850 | 182557 | 125000 | 495586 | 643607 | 878143 |
