from src.graph_loader import load_graph
from src.diffusion_model import run_diffusion
# from src.stats import print_detailed_stat
from src.visualization import draw_graph  

G = load_graph(
    "data/raw/nodes.csv",
    "data/raw/edges.csv",
    alpha=0.25
)

# print("Initial state:")
# print_detailed_stats(G)

draw_graph(G, "results/initial_graph.png")

print("\nRunning diffusion...\n")
run_diffusion(G, max_iterations=100)

draw_graph(G, "results/final_graph.png")

# print("\nFinal state:")
# print_detailed_stats(G)
