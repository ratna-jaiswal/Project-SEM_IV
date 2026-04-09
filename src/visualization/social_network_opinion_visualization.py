import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# =========================
# LOAD FILES
# =========================
base_path = r"D:\SEM-6\Project\data\raw"

edges_df = pd.read_csv(f"{base_path}\\social_network.csv")
users_df = pd.read_csv(f"{base_path}\\users.csv")

# =========================
# CREATE GRAPH
# =========================
G = nx.from_pandas_edgelist(edges_df, 'source', 'target')

# =========================
# ASSIGN OPINIONS
# =========================
opinion_dict = dict(zip(users_df["user"], users_df["opinion"]))

for node in G.nodes():
    G.nodes[node]['opinion'] = opinion_dict.get(node, None)

# =========================
# PREPARE COLORS
# =========================
opinions = []

for node in G.nodes():
    op = G.nodes[node]['opinion']

    if pd.isna(op):
        op = 0  # treat no opinion as neutral

    opinions.append(op)

# Normalize from [-1,1] → [0,1]
norm = mcolors.Normalize(vmin=-1, vmax=1)

# Choose colormap
cmap = plt.cm.RdYlGn

node_colors = [cmap(norm(op)) for op in opinions]

# =========================
# DRAW GRAPH
# =========================
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
output_folder = project_root / "results" / "plots"
output_folder.mkdir(parents=True, exist_ok=True)
output_file = output_folder / "social_network_opinion_visualization.png"

fig, ax = plt.subplots(figsize=(10, 8))

pos = nx.spring_layout(G, seed=42)  # layout

nx.draw(
    G,
    pos,
    node_color=node_colors,
    node_size=300,
    edge_color="gray",
    with_labels=False,
    ax=ax
)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, label="Opinion (-1 = Negative, +1 = Positive)")

ax.set_title("Social Network Opinion Visualization")
ax.axis("off")

fig.tight_layout()
fig.savefig(output_file, dpi=300)
print(f"Saved plot to: {output_file}")