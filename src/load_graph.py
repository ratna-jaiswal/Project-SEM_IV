# src/load_graph.py
import csv
import networkx as nx
from constants import OPINION_MAP

def load_graph(nodes_file="data/raw/nodes.csv", edges_file="data/raw/edges.csv"):
    G = nx.DiGraph()

    with open(nodes_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            G.add_node(
                int(row["node"]),
                opinion=OPINION_MAP[row["opinion"]],
                threshold=int(row["threshold"])
                # threshold=float(row["threshold"])
            )

    with open(edges_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            G.add_edge(int(row["source"]), int(row["target"]))

    return G
