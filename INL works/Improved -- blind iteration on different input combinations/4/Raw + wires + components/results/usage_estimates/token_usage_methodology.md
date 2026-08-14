# Token Usage Estimate Methodology

The exact OpenAI Responses `usage` objects were not exposed by the Codex
main-agent or subagent tools in this run, so this folder contains estimates.

The official OpenAI input token counting endpoint is `POST /v1/responses/input_tokens`.
It was not called because no API key was available in this environment. If an
API key is added later, the payloads represented by `model_call_token_estimates.csv`
can be sent to that endpoint for exact input counts.

Offline method used here:

- Text input tokens: low/expected/high ranges estimated from visible prompt,
  subagent payload, prior conversation, and tool-result sizes.
- Image/file input tokens: patch-count estimates from actual local image
  dimensions in `image_token_estimates.csv`.
- Main-agent image estimates use the detail levels explicitly requested in
  `view_image` calls where known.
- Subagent `local_image` detail is not exposed; expected estimates assume the
  local image payload is preserved at original detail.
- Cached input tokens and exact reasoning tokens are not exposed. Cached tokens
  are treated as 0 for totals; reasoning tokens are low/expected/high estimates.
- The rejected Jennifer spawn with both `message` and `items` was a tool schema
  validation error, not a subagent model call, so it is not included.

Official docs used:

- https://developers.openai.com/api/docs/guides/token-counting
- https://developers.openai.com/api/docs/guides/images-vision
- https://developers.openai.com/api/docs/guides/prompt-caching

Expected total tokens for document 4, iteration 1: 362719.
Low/high range: 135726 - 541200.
