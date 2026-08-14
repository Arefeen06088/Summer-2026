# Document 36 Token Usage Estimate

No API key was available, so the OpenAI Responses input-token counting endpoint could not be used. The subagent interface did not expose response usage objects, cached input tokens, or actual reasoning-token counts. Text/file estimates use characters/4. Image estimates use a high-detail tile approximation: downscale to max side 2048px, then short side 768px, then `85 + 170 * 512px_tiles`.

| Document | Iteration | Call | Input est | Cached | Image/file est | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| 36 | 1 | Main Codex: grouped orchestration, visual triage, prompts, packaging | 30000 | unavailable | 2210 | 2200 | 22000 | 46730 | 56410 | 79730 |
| 36 | 1 | Diego: round1_high_recall_extraction | 9500 | unavailable | 51510 | 9793 | 40000 | 90886 | 110803 | 156679 |
| 36 | 1 | Jennifer: round1_precision_review | 15193 | unavailable | 51510 | 10054 | 36000 | 94336 | 112757 | 154790 |
| 36 | 1 | Diego: round2_saturation_review | 21955 | unavailable | 0 | 10069 | 10500 | 34297 | 42524 | 59066 |
| 36 | 1 | Jennifer: round2_final_precision_confirmation | 22831 | unavailable | 17680 | 12807 | 14500 | 56896 | 67818 | 90003 |
| 36 | 1 | **TOTAL** | 99479 | unavailable | 122910 | 44923 | 123000 | 323145 | 390312 | 540268 |
