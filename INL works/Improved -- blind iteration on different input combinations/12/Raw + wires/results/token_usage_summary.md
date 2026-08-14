# Token Usage Estimate

No OpenAI API key was available, so the Responses input-token counting endpoint could not be called. Subagent usage objects were not exposed to the main agent. Estimates use local text bands plus image token proxies of ceil(width/32) * ceil(height/32). Cached input tokens are recorded as 0/unknown.

| document | iteration | calls | low | expected | high |
|---|---:|---:|---:|---:|---:|
| 12 | 1 | 6 | 230414 | 307214 | 414748 |

Image proxy token estimates:
- bottom_logic: 1440
- bottom_overlay: 1440
- center_tie: 242
- full_overlay: 12408
- full_raw: 12408
- grid_r2c2: 1056
- left_dc: 405
- overlay_full_left_center: 7350
- right_dc: 390
- top_left: 1000
- top_right: 980
- train_a_mcc1: 975
- train_a_mcc2_dc: 1050
- train_b_mcc1: 1025
- train_b_mcc2_dc: 1025
