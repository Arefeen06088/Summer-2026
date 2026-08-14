# Token Usage Estimate

No OpenAI API key or Responses token-counting endpoint access was available in this environment, and subagent usage objects were not exposed to the main agent. Estimates use local text bands plus image token proxies of ceil(width/32) * ceil(height/32). Cached input tokens are recorded as 0/unknown.

| document | iteration | calls | low | expected | high |
|---|---:|---:|---:|---:|---:|
| 13 | 1 | 5 | 384619 | 512824 | 692320 |

Image proxy token estimates:
- bottom: 1980
- full_overlay: 27000
- full_raw: 27000
- grid_r1c1: 2250
- grid_r1c2: 2250
- grid_r1c3: 2250
- grid_r2c1: 2250
- grid_r2c2: 2250
- grid_r2c3: 2250
- middle: 2310
- overlay_full_left: 16380
- startup_crop: 912
- train_a: 2312
- train_a_dc: 308
- train_b: 2346
- train_b_dc: 308
- train_c: 2856
- train_c_dc: 420
- train_d: 2898
- train_d_dc: 420
