# /main.py

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from nodes import create_nodes_csv
from edges import create_edges_csv
from load_graph import load_graph
from draw_graph import draw_graph
from run_simulation import simulate
from save_csv1 import save_iteration_wise
from save_csv2 import save_node_wise
from stats import save_stats, plot_stats


def main():
    create_nodes_csv()
    create_edges_csv()

    G = load_graph()
    draw_graph(G)

    history, matrix_history, stats_history = simulate(G)

    save_iteration_wise(history)
    save_node_wise(matrix_history, G)
    save_stats(stats_history)
    plot_stats(stats_history)


if __name__ == "__main__":
    main()
