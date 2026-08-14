import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

base_combo = r"C:\\Asif_all_python_projects\\INL\\Improved -- blind iteration on different input combinations"
summary_dir = os.path.join(base_combo, "summary_docs_1_27_36_41_on_Aug_3rd")
raw_csv = os.path.join(summary_dir, "connectivity_f1_and_rounds_by_configuration_adjusted.csv")
summary_csv = os.path.join(summary_dir, "connectivity_f1_and_rounds_summary_adjusted.csv")

# Load data
df = pd.read_csv(raw_csv)
ordered = [
    "Raw",
    "Raw + wires",
    "Raw + components",
    "Raw + wires + components",
    "Raw + wires + junctions",
    "Raw + wires + components + junctions",
    "Raw + wires + junctions + OCR",
    "All",
]
configs = [c for c in ordered if c in df["configuration"].unique()]

df = df[df["configuration"].isin(configs)].copy()
df["configuration"] = pd.Categorical(df["configuration"], categories=configs, ordered=True)

summary = pd.read_csv(summary_csv)
summary = summary[summary["configuration"].isin(configs)].set_index("configuration")

# Seaborn styling
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(13, 5))

# Boxplot with seaborn
flierprops = dict(
    marker="o",
    markerfacecolor="goldenrod",
    markeredgecolor="goldenrod",
    markersize=4,
    linestyle="none",
)

sns.boxplot(
    data=df,
    x="configuration",
    y="F1",
    order=configs,
    ax=ax1,
    showcaps=True,
    showfliers=True,
    width=0.6,
    boxprops=dict(facecolor="#cbe5ff", edgecolor="navy"),
    medianprops=dict(color="navy", linewidth=1.5),
    whiskerprops=dict(color="navy", linewidth=1),
    capprops=dict(color="navy", linewidth=1),
    flierprops=flierprops,
)

# Overlay jittered points for F1 distribution
sns.stripplot(
    data=df,
    x="configuration",
    y="F1",
    order=configs,
    ax=ax1,
    color="steelblue",
    size=3,
    alpha=0.6,
    jitter=0.18,
)

ax1.set_ylabel("Connectivity F1-score")
ymin = max(0.0, df["F1"].min() - 0.05)
ymax = min(1.0, df["F1"].max() + 0.05)
ax1.set_ylim(ymin, ymax)

# Light horizontal grids only on primary y-axis
ax1.yaxis.grid(True, color="0.9", linestyle="-", linewidth=0.8)
ax1.set_axisbelow(True)
ax1.xaxis.grid(False)

# Build display labels with "Name tags" and manual wrapping
base_labels = [c.replace("OCR", "Name tags") for c in configs]
wrapped_labels = []
for label in base_labels:
    if label in ("Raw", "All"):
        wrapped_labels.append(label)
    elif label == "Raw + wires":
        wrapped_labels.append("Raw +\nwires")
    elif label == "Raw + components":
        wrapped_labels.append("Raw +\ncomponents")
    elif label == "Raw + wires + components":
        wrapped_labels.append("Raw + wires\n+ components")
    elif label == "Raw + wires + junctions":
        wrapped_labels.append("Raw + wires\n+ junctions")
    elif label == "Raw + wires + components + junctions":
        wrapped_labels.append("Raw + wires +\ncomponents + junctions")
    elif label == "Raw + wires + junctions + Name tags":
        wrapped_labels.append("Raw + wires +\njunctions + Name tags")
    else:
        parts = label.split("+ ", 1)
        if len(parts) == 2:
            wrapped_labels.append(parts[0] + "+\n" + parts[1])
        else:
            wrapped_labels.append(label)

ax1.set_xticks(range(len(configs)))
ax1.set_xticklabels(wrapped_labels, rotation=0, ha="center", fontsize=8)

# Mean F1 markers
mean_f1_vals = [df.loc[df["configuration"] == c, "F1"].mean() for c in configs]
x = np.arange(len(configs))
ax1.scatter(x, mean_f1_vals, marker="D", color="white", edgecolor="black", zorder=5)

# Secondary axis for mean conversation rounds
round_means = [df.loc[df["configuration"] == c, "rounds"].mean() for c in configs]
ax2 = ax1.twinx()
ax2.set_ylabel("Mean Conversation Rounds")
ax2.set_ylim(0, 6)
ax2.plot(x, round_means, color="brown", marker="o", linestyle="-")
ax2.grid(False)

# Annotations: mean +/- SD for F1 and mean rounds
for i, cfg in enumerate(configs):
    if cfg not in summary.index:
        continue
    mean_f1 = float(summary.loc[cfg, "mean_F1"])
    sd_f1 = float(summary.loc[cfg, "sd_F1"])
    mean_r = float(summary.loc[cfg, "mean_rounds"])
    max_f1 = df.loc[df["configuration"] == cfg, "F1"].max()
    # Use a smaller offset for the first 5 boxes so labels sit lower
    offset = 0.03 if i < 5 else 0.04
    txt_y = min(ymax - 0.01, max_f1 + offset)
    ax1.text(
        x[i],
        txt_y,
        f"mean +/- SD =\n{mean_f1:.3f}+/-{sd_f1:.3f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )
    ax2.text(
        x[i],
        round_means[i] + 0.15,
        f"{mean_r:.1f}",
        color="darkred",
        ha="center",
        va="bottom",
        fontsize=8,
    )

# Legend
legend_elements = [
    Patch(facecolor="#cbe5ff", edgecolor="navy", label="F1 distribution, median line"),
    Line2D(
        [0],
        [0],
        marker="D",
        color="w",
        markerfacecolor="white",
        markeredgecolor="black",
        label="Mean F1 marker",
        linestyle="None",
    ),
    Line2D([0], [0], color="brown", marker="o", label="Mean conversation rounds"),
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="goldenrod",
        markeredgecolor="goldenrod",
        label="Outlier F1 score",
        linestyle="None",
    ),
]

ax1.legend(handles=legend_elements, loc="lower right")
fig.tight_layout()

out_path = os.path.join(summary_dir, "connectivity_f1_boxplot_with_rounds_seaborn_adjusted.png")
fig.savefig(out_path, dpi=300)
print("Saved seaborn-adjusted figure to:", out_path)
