import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# LOAD DATA
# =========================
logs_path = r"D:\SEM-6\Project\results\logs\opinion_dynamics.xlsx"
log_df = pd.read_excel(logs_path)

# =========================
# COMPUTE AVERAGE OPINION PER ITERATION
# =========================
# Drop the 'Node' column and compute mean for each iteration
iteration_columns = [col for col in log_df.columns if col.startswith('Iter_')]
avg_opinions = log_df[iteration_columns].mean(axis=0)

# Extract iteration numbers
iterations = [int(col.split('_')[1]) for col in iteration_columns]

# =========================
# CREATE LINE PLOT
# =========================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(
    iterations,
    avg_opinions,
    marker='o',
    linestyle='-'
    , color='#0072B2',
    linewidth=3,
    markersize=8,
    markerfacecolor='#FFFFFF',
    markeredgewidth=1.8,
    markeredgecolor='#0072B2',
)
ax.fill_between(iterations, avg_opinions, color='#0072B2', alpha=0.12)

ax.axhline(0, color='#333333', linestyle='--', linewidth=1, alpha=0.7)

ax.set_xlabel('Iteration', fontsize=14)
ax.set_ylabel('Average Opinion', fontsize=14)
ax.set_title('Average Opinion Evolution Over Iterations', fontsize=18, pad=16)

# Focus y-axis on the actual data range with a small margin
y_min, y_max = avg_opinions.min(), avg_opinions.max()
y_margin = max(0.02, (y_max - y_min) * 0.1)
ax.set_ylim(y_min - y_margin, y_max + y_margin)

ax.set_xlim(min(iterations) - 0.5, max(iterations) + 0.5)
ax.tick_params(axis='both', labelsize=12)
ax.grid(True, alpha=0.25)

# Annotate first and last values
ax.annotate(
    f'Start: {avg_opinions.iloc[0]:.3f}',
    xy=(iterations[0], avg_opinions.iloc[0]),
    xytext=(iterations[0] + 1, avg_opinions.iloc[0] + 0.15),
    arrowprops=dict(arrowstyle='->', color='#0072B2', lw=1.5),
    fontsize=11,
    color='#0072B2',
)
ax.annotate(
    f'End: {avg_opinions.iloc[-1]:.3f}',
    xy=(iterations[-1], avg_opinions.iloc[-1]),
    xytext=(iterations[-1] - 6, avg_opinions.iloc[-1] - 0.18),
    arrowprops=dict(arrowstyle='->', color='#0072B2', lw=1.5),
    fontsize=11,
    color='#0072B2',
)

plt.tight_layout()

# =========================
# SAVE PLOT
# =========================
plots_path = r"D:\SEM-6\Project\results\plots"
os.makedirs(plots_path, exist_ok=True)
output_file = os.path.join(plots_path, "average_opinion_evolution.png")
fig.savefig(output_file, dpi=300, bbox_inches='tight')

print(f"✅ Average opinion evolution plot saved at: {output_file}")

# Show plot
plt.show()