# Token Usage Estimate

Document: 1

Iteration: 1

Low estimate: 57,403 tokens

Expected estimate: 81,840 tokens

High estimate: 110,490 tokens

The OpenAI Responses input-token counting endpoint was not called because `OPENAI_API_KEY` was not present in the environment. The multi-agent tool did not expose response usage objects, cached-input counts, or reasoning-token details. Text counts use a 4 characters/token heuristic; image/file counts use a reproducible tiled vision heuristic implemented in `codes/estimate_token_usage.py`.
