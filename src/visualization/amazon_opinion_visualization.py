import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# =========================
# LOAD DATA
# =========================
results_path = r"D:\SEM-6\Project\results\logs\amazon_opinion_dynamics.xlsx"
log_df = pd.read_csv(results_path.replace('.xlsx', '.csv')) if not os.path.exists(results_path) else pd.read_excel(results_path)

# Set Node as index if it's a column
if 'Node' in log_df.columns:
    log_df.set_index('Node', inplace=True)

# =========================
# FIGURE 1: OPINION EVOLUTION OVER TIME (Line Plot)
# =========================
plt.figure(figsize=(14, 6))

# Plot a sample of nodes (every 10th node for clarity)
sample_nodes = log_df.index[::max(1, len(log_df) // 10)]

for node in sample_nodes:
    plt.plot(log_df.loc[node], marker='o', label=f'Node {node}', alpha=0.7, markersize=3)

plt.xlabel('Iteration', fontsize=12)
plt.ylabel('Opinion', fontsize=12)
plt.title('Opinion Evolution Over Iterations (Sample Nodes)', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(r"D:\SEM-6\Project\results\plots\opinion_evolution_line.png", dpi=300, bbox_inches='tight')
print("✅ Saved: opinion_evolution_line.png")
plt.close()

# =========================
# FIGURE 2: HEATMAP OF ALL OPINIONS
# =========================
plt.figure(figsize=(16, 8))
sns.heatmap(log_df, cmap='RdYlGn', center=0, cbar_kws={'label': 'Opinion'})
plt.title('Opinion Heatmap - All Nodes Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('Node', fontsize=12)
plt.tight_layout()
plt.savefig(r"D:\SEM-6\Project\results\plots\opinion_heatmap.png", dpi=300, bbox_inches='tight')
print("✅ Saved: opinion_heatmap.png")
plt.close()

# =========================
# FIGURE 3: AVERAGE OPINION TREND
# =========================
avg_opinion = log_df.mean(axis=0)

plt.figure(figsize=(12, 6))
plt.plot(avg_opinion, marker='o', linewidth=2, markersize=6, color='#2E86AB')
plt.fill_between(range(len(avg_opinion)), avg_opinion, alpha=0.3, color='#2E86AB')
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('Average Opinion', fontsize=12)
plt.title('Average Network Opinion Over Time', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(r"D:\SEM-6\Project\results\plots\average_opinion_trend.png", dpi=300, bbox_inches='tight')
print("✅ Saved: average_opinion_trend.png")
plt.close()

# =========================
# FIGURE 4: OPINION DISTRIBUTION BOXPLOT
# =========================
# Get opinions at different iterations
iterations_to_plot = [0, len(avg_opinion)//4, len(avg_opinion)//2, 3*len(avg_opinion)//4, len(avg_opinion)-1]
box_data = []
labels = []

for it in iterations_to_plot:
    if it < len(log_df.columns):
        col_name = log_df.columns[it]
        box_data.append(log_df[col_name].dropna())
        labels.append(f'Iter {it}')

plt.figure(figsize=(12, 6))
bp = plt.boxplot(box_data, labels=labels, patch_artist=True)

# Color the boxes
colors = plt.cm.RdYlGn(np.linspace(0, 1, len(box_data)))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

plt.ylabel('Opinion', fontsize=12)
plt.title('Opinion Distribution at Different Iterations', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(r"D:\SEM-6\Project\results\plots\opinion_distribution_boxplot.png", dpi=300, bbox_inches='tight')
print("✅ Saved: opinion_distribution_boxplot.png")
plt.close()

# =========================
# FIGURE 5: VARIANCE OVER TIME
# =========================
variance = log_df.var(axis=0)
std_dev = log_df.std(axis=0)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Variance
ax1.plot(variance, marker='s', linewidth=2, color='#A23B72', markersize=5)
ax1.fill_between(range(len(variance)), variance, alpha=0.3, color='#A23B72')
ax1.set_ylabel('Variance', fontsize=11)
ax1.set_title('Opinion Variance Over Time', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Standard Deviation
ax2.plot(std_dev, marker='o', linewidth=2, color='#F18F01', markersize=5)
ax2.fill_between(range(len(std_dev)), std_dev, alpha=0.3, color='#F18F01')
ax2.set_xlabel('Iteration', fontsize=11)
ax2.set_ylabel('Standard Deviation', fontsize=11)
ax2.set_title('Opinion Standard Deviation Over Time', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(r"D:\SEM-6\Project\results\plots\opinion_variance_trend.png", dpi=300, bbox_inches='tight')
print("✅ Saved: opinion_variance_trend.png")
plt.close()

# =========================
# FIGURE 6: HISTOGRAM - INITIAL vs FINAL OPINIONS
# =========================
initial_opinions = log_df.iloc[:, 0].dropna()
final_opinions = log_df.iloc[:, -1].dropna()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.hist(initial_opinions, bins=20, color='#E63946', alpha=0.7, edgecolor='black')
ax1.set_xlabel('Opinion', fontsize=11)
ax1.set_ylabel('Frequency', fontsize=11)
ax1.set_title('Initial Opinions Distribution', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

ax2.hist(final_opinions, bins=20, color='#06A77D', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Opinion', fontsize=11)
ax2.set_ylabel('Frequency', fontsize=11)
ax2.set_title('Final Opinions Distribution', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(r"D:\SEM-6\Project\results\plots\initial_vs_final_distribution.png", dpi=300, bbox_inches='tight')
print("✅ Saved: initial_vs_final_distribution.png")
plt.close()

# =========================
# SUMMARY STATISTICS
# =========================
print("\n" + "="*60)
print("OPINION DYNAMICS SUMMARY")
print("="*60)
print(f"Total Nodes: {len(log_df)}")
print(f"Total Iterations: {len(log_df.columns)}")
print(f"\nInitial Average Opinion: {initial_opinions.mean():.4f}")
print(f"Final Average Opinion: {final_opinions.mean():.4f}")
print(f"Opinion Change: {final_opinions.mean() - initial_opinions.mean():.4f}")
print(f"\nInitial Std Dev: {initial_opinions.std():.4f}")
print(f"Final Std Dev: {final_opinions.std():.4f}")
print(f"Convergence (Δ Std): {initial_opinions.std() - final_opinions.std():.4f}")
print("="*60 + "\n")

print("✅ All visualizations saved to D:\\SEM-6\\Project\\results\\plots\\")
