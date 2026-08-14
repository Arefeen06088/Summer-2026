# Token Estimation Method

Document: 15
Iteration: 1

No OpenAI API key was available in this environment, so the Responses input-token
counting endpoint and response usage objects could not be collected. The token
tables therefore use local estimates:

- Text/file tokens: `ceil(character_count / 4)`.
- Image tokens: high-detail tile estimate after PNG dimension parsing:
  fit within 2048 px, scale shortest side to 768 px when larger, then
  `85 + 170 * ceil(width / 512) * ceil(height / 512)`.
- Cached input tokens are estimates for repeated subagent context only; the
  local tools do not expose actual cache-hit accounting.
- Output and reasoning tokens are low/expected/high estimates because actual
  model usage objects were unavailable.

The per-call estimates are in `model_call_usage_estimates.csv`; grouped totals
are in `token_usage_totals_by_document.csv`.
