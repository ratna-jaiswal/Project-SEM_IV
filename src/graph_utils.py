import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns


# ==============================
# 1. NETWORK GRAPH (Improved)
# ==============================

def draw_network_graph(G, users, output_path, title="User Network"):

    plt.figure(figsize=(10, 10))

    # Better layout (more spacing)
    pos = nx.spring_layout(G, seed=42, k=0.35, iterations=50)

    # Extract properties
    opinions = np.array([users[n]["opinion"] for n in G.nodes()])
    belief_strengths = np.array([users[n]["belief_strength"] for n in G.nodes()])

    # Normalize node size
    node_sizes = 200 + 1000 * belief_strengths

    # 🎨 Custom RED → YELLOW → GREEN colormap
    cmap = LinearSegmentedColormap.from_list(
        "custom_ryg",
        ["red", "yellow", "green"]
    )

    # Normalize opinions (-1 to +1 → 0 to 1)
    norm_opinions = (opinions + 1) / 2

    # Draw edges (lighter + less clutter)
    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.08,       # much lighter
        width=0.4,
        edge_color="gray"
    )

    # Draw nodes
    nodes = nx.draw_networkx_nodes(
        G,
        pos,
        node_color=norm_opinions,
        cmap=cmap,
        node_size=node_sizes,
        alpha=0.95,
        edgecolors="black",   # outline improves clarity
        linewidths=0.3
    )

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array([])

    ax = plt.gca()
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Opinion (Red = Negative, Yellow = Neutral, Green = Positive)")

    plt.title(title, fontsize=14)
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


# ==============================
# 2. OPINION EVOLUTION
# ==============================
def plot_opinion_evolution(log_df, output_path):

    avg_opinion = log_df.groupby("iteration")["opinion"].mean()

    plt.figure(figsize=(8, 4))
    plt.plot(avg_opinion.index, avg_opinion.values, marker="o")

    plt.axhline(0, linestyle="--")

    plt.xlabel("Iteration")
    plt.ylabel("Average Opinion")
    plt.title("Opinion Evolution")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# ==============================
# 3. POLARIZATION (VARIANCE)
# ==============================
def plot_opinion_variance(log_df, output_path):

    variance = log_df.groupby("iteration")["opinion"].var()

    plt.figure(figsize=(8, 4))
    plt.plot(variance.index, variance.values, marker="o")

    plt.xlabel("Iteration")
    plt.ylabel("Variance")
    plt.title("Opinion Polarization (Variance)")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# ==============================
# 4. opinion_distribution_over_time
# ==============================

def plot_distribution_kde(log_df, output_path):

    import matplotlib.pyplot as plt

    iterations = [0,1, 2, 3, 4, 5, 10, log_df["iteration"].max()]

    plt.figure(figsize=(10, 6))

    for it in iterations:
        subset = log_df[log_df["iteration"] == it]["opinion"]
        sns.kdeplot(subset, label=f"Iteration {it}")

    plt.title("Opinion Distribution Evolution (KDE)")
    plt.xlabel("Opinion")
    plt.legend()

    plt.savefig(output_path)
    plt.close()




# ==============================
# 6. USER TRAJECTORIES
# ==============================
def plot_user_trajectories(log_df, output_path, num_users=10):

    sample_users = log_df["user_id"].unique()[:num_users]

    plt.figure(figsize=(8, 4))

    for uid in sample_users:
        user_data = log_df[log_df["user_id"] == uid]
        plt.plot(user_data["iteration"], user_data["opinion"], label=f"User {uid}")

    plt.xlabel("Iteration")
    plt.ylabel("Opinion")
    plt.title("User Opinion Trajectories")

    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()



def plot_opinion_distribution_per_iteration(log_df, save_path):
    """
    Creates a grid of small bar plots showing opinion distribution at each iteration
    """

    iterations = sorted(log_df["iteration"].unique())
    num_iters = len(iterations)

    # Grid size (adjust automatically)
    cols = 5
    rows = int(np.ceil(num_iters / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 3))
    axes = axes.flatten()

    for i, t in enumerate(iterations):
        ax = axes[i]

        data = log_df[log_df["iteration"] == t]["opinion"]

        # Create histogram bins
        ax.hist(data, bins=10)

        ax.set_title(f"Iter {t}")
        ax.set_xlim(-1, 1)  # opinion range
        ax.set_ylim(0, None)

    # Remove extra empty plots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle("Opinion Distribution at Each Iteration", fontsize=16)
    plt.tight_layout()

    plt.savefig(save_path)
    plt.close()
