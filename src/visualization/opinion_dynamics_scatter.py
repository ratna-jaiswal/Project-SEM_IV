import os

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

# =========================
# LOAD DATA
# =========================
logs_path = r"D:\SEM-6\Project\results\logs\opinion_dynamics.xlsx"
log_df = pd.read_excel(logs_path)

# =========================
# PREPARE DATA FOR PLOTTING
# =========================
melted_df = log_df.melt(id_vars=['Node'], var_name='Iteration', value_name='Opinion')
melted_df['Iteration_Num'] = melted_df['Iteration'].str.extract(r'Iter_(\d+)').astype(int)

# Summary statistics by iteration
summary_df = (
    melted_df.groupby('Iteration_Num')['Opinion']
    .agg(median='median', q1=lambda x: x.quantile(0.25), q3=lambda x: x.quantile(0.75))
    .reset_index()
)

# =========================
# PLOT STYLING
# =========================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 8))

norm = mcolors.Normalize(vmin=-1, vmax=1)
cmap = plt.cm.RdYlGn
colors = [cmap(norm(op)) for op in melted_df['Opinion']]

ax.scatter(
    melted_df['Iteration_Num'],
    melted_df['Opinion'],
    c=colors,
    s=24,
    alpha=0.28,
    edgecolors='none',
    linewidths=0,
    rasterized=True,
)

ax.plot(summary_df['Iteration_Num'], summary_df['median'], color='#333333', linewidth=2.0, label='Median opinion')
ax.fill_between(
    summary_df['Iteration_Num'],
    summary_df['q1'],
    summary_df['q3'],
    color='#777777',
    alpha=0.2,
    label='Interquartile range',
)

ax.set_title('Opinion Dynamics: All Nodes Across Iterations', fontsize=18, pad=18)
ax.set_xlabel('Iteration', fontsize=14)
ax.set_ylabel('Opinion', fontsize=14)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(melted_df['Iteration_Num'].min() - 0.5, melted_df['Iteration_Num'].max() + 0.5)
ax.tick_params(axis='both', labelsize=12)
ax.grid(True, alpha=0.35)
ax.legend(frameon=True, framealpha=0.95, fontsize=12)

# Colorbar for opinion values
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.02)
cbar.set_label('Opinion value', fontsize=12)

# =========================
# SAVE PLOT
# =========================
plots_path = r"D:\SEM-6\Project\results\plots"
os.makedirs(plots_path, exist_ok=True)
output_file = os.path.join(plots_path, 'opinion_dynamics_scatter.png')
fig.savefig(output_file, dpi=300, bbox_inches='tight')

print(f"✅ Scatter plot saved at: {output_file}")
plt.show()