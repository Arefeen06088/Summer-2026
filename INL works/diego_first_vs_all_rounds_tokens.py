import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

base_all = r"C:\\Asif_all_python_projects\\INL\\Improved -- blind iteration on different input combinations"
folders = list(range(1, 28)) + [36, 37, 38, 39, 40, 41]

records = []
for folder in folders:
    results_dir = os.path.join(base_all, str(folder), "Raw + wires + junctions + OCR", "results")
    csv_path = os.path.join(results_dir, "model_call_usage_estimates.csv")
    if not os.path.exists(csv_path):
        continue
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    if not reader:
        continue

    def get_total_tokens(row):
        if row is None:
            return None
        v = (row.get("total_tokens_expected") or "").strip()
        if not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    first_diego = None
    for row in reader:
        if row.get("agent") == "Diego" and row.get("call_id") == "diego-r1":
            first_diego = row
            break
    if first_diego is None:
        for row in reader:
            if row.get("agent") == "Diego":
                first_diego = row
                break

    diego_first_tokens = get_total_tokens(first_diego)

    total_tokens = 0.0
    has_any = False
    for row in reader:
        v = get_total_tokens(row)
        if v is not None:
            total_tokens += v
            has_any = True
    if not has_any:
        total_tokens = None

    records.append({"folder": folder, "setup": "First Diego round", "tokens": diego_first_tokens})
    records.append({"folder": folder, "setup": "All rounds combined", "tokens": total_tokens})

summary_dir = os.path.join(base_all, "summary_docs_1_27_36_41_on_Aug_3rd")
os.makedirs(summary_dir, exist_ok=True)

raw_df = pd.DataFrame(records)
raw_out = os.path.join(summary_dir, "diego_first_vs_all_rounds_tokens_raw.csv")
raw_df.to_csv(raw_out, index=False)
print("Wrote raw token usage to", raw_out)

summary_rows = []
for setup in ["First Diego round", "All rounds combined"]:
    sub = raw_df[(raw_df["setup"] == setup) & raw_df["tokens"].notna()]
    vals = sub["tokens"].tolist()
    if vals:
        mean_tokens = float(np.mean(vals))
        sd_tokens = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    else:
        mean_tokens = np.nan
        sd_tokens = np.nan
    summary_rows.append({"setup": setup, "mean_tokens": mean_tokens, "sd_tokens": sd_tokens})

summary_df = pd.DataFrame(summary_rows)
summary_out = os.path.join(summary_dir, "diego_first_vs_all_rounds_tokens_summary.csv")
summary_df.to_csv(summary_out, index=False)
print("Wrote token summary to", summary_out)

TOK_SCALE = 1_000_000.0
summary_df = summary_df.set_index("setup")
setups = ["First Diego round", "All rounds combined"]
means_M = [summary_df.loc[s, "mean_tokens"] / TOK_SCALE for s in setups]
sds_M = [summary_df.loc[s, "sd_tokens"] / TOK_SCALE for s in setups]

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(7, 5))

x = np.arange(len(setups))
width = 0.5

sns.barplot(x=setups, y=means_M, ax=ax, color="#4d4d4d", errorbar=None, width=width)

for i, (m, s) in enumerate(zip(means_M, sds_M)):
    ax.errorbar(i, m, yerr=s, fmt="none", ecolor="black", capsize=4, linewidth=1)

ax.set_ylabel("Tokens Used (millions)")
ax.set_xlabel("Agent Setup")
ax.yaxis.grid(True, color="0.9", linestyle="-", linewidth=0.8)
ax.xaxis.grid(False)

for i, (m, s) in enumerate(zip(means_M, sds_M)):
    height = m
    label = f"{m:.2f}M\n+/-{s:.2f}M"
    ax.text(i, height + s + 0.2, label, ha="center", va="bottom", fontsize=8)

fig.tight_layout()
plot_out = os.path.join(summary_dir, "diego_first_vs_all_rounds_tokens.png")
fig.savefig(plot_out, dpi=300)
print("Saved Diego vs all-rounds token plot to", plot_out)
