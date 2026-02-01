# src/stats.py
import csv
import os
import matplotlib.pyplot as plt
from constants import OPINION_MAP, REV_OPINION_MAP

LOG_DIR = "results/logs"
PLOT_DIR = "results/plots"

def save_stats(stats_history):
    os.makedirs(LOG_DIR, exist_ok=True)
    path = os.path.join(LOG_DIR, "stats.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["itr", "A", "B", "C", "D", "E"])

        for itr, stats in enumerate(stats_history):
            writer.writerow([itr] + list(stats.values()))

    print(f"💾 Stats CSV saved → {path}")


def plot_stats(stats_history):
    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, "opinion_stats.png")

    opinions = ["A", "B", "C", "D", "E"]
    plt.figure(figsize=(10, 6))

    for op in opinions:
        plt.plot(
            [s[op] for s in stats_history],
            label=op,
            linewidth=2
        )

    plt.xlabel("Iteration")
    plt.ylabel("Number of Nodes")
    plt.title("Opinion Evolution Over Iterations")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()

    print(f"📈 Opinion evolution plot saved → {path}")
