# Connectivity Extraction Results

Final selected file: `round_04_jennifer_final_matrix.csv`, duplicated as `final_connectivity_matrix.csv`.

Interpretation: closed solid power/DC connectivity. Buses are explicit nodes. `CB-TIE-480`, normally-open `CB-LC-TIE`, and dashed control/signal components are retained as nodes but encoded with 0 closed-power degree unless they also have accepted solid-power edges. Nonclosed/signal paths are listed in `final_excluded_or_nonclosed_edges.csv`.

Token accounting note: no OpenAI API key or model usage object was available. Local tokenizer use was not reliable in this environment, so local text token counts use the transparent `chars_div_4` fallback and image counts use a high-detail tiling estimate.

Rows and columns use the same ordered component/node names. Matrices are symmetric and have zero diagonals.
