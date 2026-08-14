# Token Usage Estimate

No OpenAI API key was available in this environment, so actual usage objects and the Responses input-token counting endpoint could not be used. Estimates use `ceil(chars / 4)` for text and a high-detail image tile approximation for image/file inputs.

Diego round 1 image evidence package estimate: 25585 image/file input tokens.
Jennifer round 1 image evidence package estimate: 27115 image/file input tokens.

| Document | Iteration | Calls | Low Total | Expected Total | High Total |
|---|---:|---:|---:|---:|---:|
| 4 | 1 | 5 | 105049 | 134369 | 184999 |

See `token_usage_estimate.csv` for per-call detail, including estimated cached-input fields where previous thread context was likely reusable.
