import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# Paths
base_all = r"C:\\Asif_all_python_projects\\INL\\Improved -- blind iterations"
metrics_summary_path = os.path.join(base_all, "summary_docs_1_27_36_41", "evaluation", "single_vs_multi_agent_metrics_summary.csv")

base_combo = r"C:\\Asif_all_python_projects\\INL\\Improved -- blind iteration on different input combinations"
token_summary_path = os.path.join(base_combo, "summary_docs_1_27_36_41_on_Aug_3rd", "diego_first_vs_all_rounds_tokens_summary.csv")

# Load summaries
metrics_df = pd.read_csv(metrics_summary_path).set_index("setup")

tokens_df = pd.read_csv(token_summary_path).set_index("setup")
# Map token setups to agent setups
tokens_df = tokens_df.rename(index={
    "First Diego round": "Single Agent",
    "All rounds combined": "Multi-Agent",
})

setups = ["Single Agent", "Multi-Agent"]

prec_means = [metrics_df.loc[s, "mean_precision"] for s in setups]
prec_sds = [metrics_df.loc[s, "sd_precision"] for s in setups]
rec_means = [metrics_df.loc[s, "mean_recall"] for s in setups]
rec_sds = [metrics_df.loc[s, "sd_recall"] for s in setups]
f1_means = [metrics_df.loc[s, "mean_f1"] for s in setups]
f1_sds = [metrics_df.loc[s, "sd_f1"] for s in setups]

tok_means = [tokens_df.loc[s, "mean_tokens"] for s in setups]
tok_sds = [tokens_df.loc[s, "sd_tokens"] for s in setups]

# Plot
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(10, 5))

x = np.arange(len(setups))
width = 0.18

b1 = ax1.bar(x - width, prec_means, width, yerr=prec_sds, capsize=4, color="#004c8c", label="Precision")
b2 = ax1.bar(x, rec_means, width, yerr=rec_sds, capsize=4, color="#d3d3d3", label="Recall")
b3 = ax1.bar(x + width, f1_means, width, yerr=f1_sds, capsize=4, color="#c62828", label="F1 Score")

ax1.set_ylabel("Score")
ax1.set_xticks(x)
ax1.set_xticklabels(setups)
ax1.set_ylim(0.0, 1.1)
# Light horizontal grids only on primary y-axis; no vertical grids
ax1.yaxis.grid(True, color="0.9", linestyle="-", linewidth=0.8)
ax1.xaxis.grid(False)
ax1.set_axisbelow(True)

ax2 = ax1.twinx()
ax2.set_ylabel("Mean Tokens Used")

b4 = ax2.bar(x + 2*width, tok_means, width, yerr=tok_sds, capsize=4, color="#4d4d4d", label="Mean Tokens Used")

# Choose tokens axis range based on data
valid_tok = [m + s for m, s in zip(tok_means, tok_sds) if not np.isnan(m)]
if valid_tok:
    max_tok = max(valid_tok)
    ax2.set_ylim(0, max_tok * 1.4)
else:
    ax2.set_ylim(0, 1)

# Remove grids on secondary y-axis
ax2.grid(False)


def annotate_bars(ax, bars, means, sds, is_tokens=False):
    for bar, mean, sd in zip(bars, means, sds):
        if np.isnan(mean):
            continue
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width() / 2
        if is_tokens:
            label = f"{mean:,.0f}\n+/-{sd:,.0f}"
            offset = sd * 0.05 if sd > 0 else max_tok * 0.02
        else:
            label = f"{mean:.3f}\n+/-{sd:.3f}"
            offset = 0.03
        ax.text(x_pos, height + offset, label, ha="center", va="bottom", fontsize=8)

annotate_bars(ax1, b1, prec_means, prec_sds)
annotate_bars(ax1, b2, rec_means, rec_sds)
annotate_bars(ax1, b3, f1_means, f1_sds)
annotate_bars(ax2, b4, tok_means, tok_sds, is_tokens=True)

handles = [
    Patch(color="#004c8c", label="Precision"),
    Patch(color="#d3d3d3", label="Recall"),
    Patch(color="#c62828", label="F1 Score"),
    Patch(color="#4d4d4d", label="Mean Tokens Used"),
]
ax1.legend(handles=handles, loc="lower left")

fig.tight_layout()
plot_out = os.path.join(base_all, "summary_docs_1_27_36_41", "evaluation", "single_vs_multi_agent_precision_recall_f1_tokens_from_model_calls.png")
fig.savefig(plot_out, dpi=300)
print("Saved combined metrics+tokens plot to", plot_out)
