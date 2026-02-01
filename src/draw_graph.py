# src/draw_graph.py
import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

PLOT_DIR = "results/plots"

def draw_graph(G):
    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, "final_graph.png")

    fig, ax = plt.subplots(figsize=(12, 10))

    pos = nx.spring_layout(G, seed=42, k=0.6)
    node_colors = [G.nodes[n]["opinion"] for n in G.nodes]

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=200,
        node_color=node_colors,
        cmap=plt.cm.viridis,
        ax=ax
    )

    # Draw edges (lighter + transparent)
    nx.draw_networkx_edges(
        G, pos,
        edge_color="gray",
        alpha=0.3,
        arrows=True,
        arrowsize=8,
        width=0.6,
        ax=ax
    )

     # ❌ No labels → much cleaner
    ax.set_title("Directed Opinion Network (Final State)")
    ax.axis("off")

    sm = plt.cm.ScalarMappable(
        cmap=plt.cm.viridis,
        norm=plt.Normalize(vmin=1, vmax=5)
    )
    sm.set_array([])

    plt.colorbar(sm, ax=ax, label="Opinion (A→E)")


    plt.savefig(path)
    plt.savefig(path, dpi=200)
    plt.close()

    print(f"📊 Graph saved → {path}")
