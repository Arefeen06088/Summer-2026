# Token Usage Estimate - Document 10

No API key was available, so the OpenAI Responses counting endpoint was not called and no response `usage` objects were exposed by this environment.

Method:
- Text tokens are local estimates from the retained prompt/output sizes, banded low/expected/high.
- Image tokens use the current OpenAI vision patch method for GPT-5.5/GPT-5.6 original detail: `ceil(width/32) * ceil(height/32)`.
- Low image estimate assumes high-detail capped processing; expected assumes original detail; high adds 15 percent for model/accounting variance.
- Cached input tokens are recorded as 0 because cache usage was not observable.

| document | iteration | model calls counted | expected image/file input tokens | total low | total expected | total high |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1 | 4 | 135518 | 136952 | 219638 | 269412 |

See `token_usage_estimate.csv` for per-call rows.
