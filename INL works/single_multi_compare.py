import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

base_all = r"C:\\Asif_all_python_projects\\INL\\Improved -- blind iterations"
folders = list(range(1, 28)) + [36, 37, 38, 39, 40, 41]

rows = []
for folder in folders:
    metrics_path = os.path.join(base_all, str(folder), "Results", "evaluation", "connectivity_matrix_validation_metrics.csv")
    if not os.path.exists(metrics_path):
        continue
    with open(metrics_path, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    if len(reader) < 3:
        continue
    header = reader[0]
    data_rows = [r for r in reader[1:] if any(c.strip() for c in r)]
    if not data_rows:
        continue
    col_map = {name.strip(): i for i, name in enumerate(header)}

    def get_float(row, name):
        idx = col_map.get(name)
        if idx is None or idx >= len(row):
            return None
        v = row[idx].strip()
        if not v:
            return None
        try:
            return float(v)
        except ValueError:
            return None

    sa_row = data_rows[0]
    ma_row = data_rows[-1]
    rows.append({
        "folder": folder,
        "setup": "Single Agent",
        "precision": get_float(sa_row, "Precision"),
        "recall": get_float(sa_row, "Recall"),
        "f1": get_float(sa_row, "F1 score"),
    })
    rows.append({
        "folder": folder,
        "setup": "Multi-Agent",
        "precision": get_float(ma_row, "Precision"),
        "recall": get_float(ma_row, "Recall"),
        "f1": get_float(ma_row, "F1 score"),
    })

summary_eval_dir = os.path.join(base_all, "summary_docs_1_27_36_41", "evaluation")
os.makedirs(summary_eval_dir, exist_ok=True)

# Save raw metrics
df = pd.DataFrame(rows)
raw_out = os.path.join(summary_eval_dir, "single_vs_multi_agent_metrics_raw.csv")
df.to_csv(raw_out, index=False)
print("Wrote raw metrics to", raw_out)

# Compute summary stats for precision/recall/F1
metric_cols = ["precision", "recall", "f1"]
summary_rows = []
for setup in ["Single Agent", "Multi-Agent"]:
    sub = df[df["setup"] == setup]
    row = {"setup": setup}
    for col in metric_cols:
        vals = sub[col].dropna().tolist()
        if vals:
            row[f"mean_{col}"] = float(np.mean(vals))
            row[f"sd_{col}"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        else:
            row[f"mean_{col}"] = np.nan
            row[f"sd_{col}"] = np.nan
    summary_rows.append(row)

summary_df = pd.DataFrame(summary_rows)
summary_out = os.path.join(summary_eval_dir, "single_vs_multi_agent_metrics_summary.csv")
summary_df.to_csv(summary_out, index=False)
print("Wrote summary metrics to", summary_out)

# Prepare plotting data
summary_df = summary_df.set_index("setup")
setups = ["Single Agent", "Multi-Agent"]

prec_means = [summary_df.loc[s, "mean_precision"] for s in setups]
prec_sds = [summary_df.loc[s, "sd_precision"] for s in setups]
rec_means = [summary_df.loc[s, "mean_recall"] for s in setups]
rec_sds = [summary_df.loc[s, "sd_recall"] for s in setups]
f1_means = [summary_df.loc[s, "mean_f1"] for s in setups]
f1_sds = [summary_df.loc[s, "sd_f1"] for s in setups]

# Token usage copied from reference image (millions)
TOK_SCALE = 1_000_000.0
single_tok_mean_M, single_tok_sd_M = 3.15, 1.02
multi_tok_mean_M, multi_tok_sd_M = 7.95, 2.08

# Convert to absolute token counts
single_tok_mean = single_tok_mean_M * TOK_SCALE
single_tok_sd = single_tok_sd_M * TOK_SCALE
multi_tok_mean = multi_tok_mean_M * TOK_SCALE
multi_tok_sd = multi_tok_sd_M * TOK_SCALE

tok_means = [single_tok_mean, multi_tok_mean]
tok_sds = [single_tok_sd, multi_tok_sd]

x = np.arange(len(setups))
width = 0.18

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(10, 5))

# Primary metric bars
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

# Secondary axis for tokens
ax2 = ax1.twinx()
ax2.set_ylabel("Mean Tokens Used (millions)")

# Convert token stats to millions for plotting
tok_means_m = [single_tok_mean_M, multi_tok_mean_M]
tok_sds_m = [single_tok_sd_M, multi_tok_sd_M]

b4 = ax2.bar(x + 2*width, tok_means_m, width, yerr=tok_sds_m, capsize=4, color="#4d4d4d", label="Mean Tokens Used")

max_tok = max([m + s for m, s in zip(tok_means_m, tok_sds_m)])
ax2.set_ylim(0, max_tok * 1.4)
# Remove grids on secondary y-axis
ax2.grid(False)


def annotate_bars(ax, bars, means, sds, is_tokens=False):
    for bar, mean, sd in zip(bars, means, sds):
        if mean != mean:  # NaN
            continue
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width() / 2
        if is_tokens:
            label = f"{mean:.2f}M\n+/-{sd:.2f}M"
            offset = sd * 0.15
        else:
            label = f"{mean:.3f}\n+/-{sd:.3f}"
            offset = 0.03
        ax.text(x_pos, height + offset, label, ha="center", va="bottom", fontsize=8)

annotate_bars(ax1, b1, prec_means, prec_sds)
annotate_bars(ax1, b2, rec_means, rec_sds)
annotate_bars(ax1, b3, f1_means, f1_sds)
annotate_bars(ax2, b4, tok_means_m, tok_sds_m, is_tokens=True)

handles = [
    Patch(color="#004c8c", label="Precision"),
    Patch(color="#d3d3d3", label="Recall"),
    Patch(color="#c62828", label="F1 Score"),
    Patch(color="#4d4d4d", label="Mean Tokens Used"),
]
ax1.legend(handles=handles, loc="lower left")

fig.tight_layout()
plot_out = os.path.join(summary_eval_dir, "single_vs_multi_agent_precision_recall_f1_tokens.png")
fig.savefig(plot_out, dpi=300)
print("Saved comparison plot to", plot_out)
