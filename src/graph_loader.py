import csv
import networkx as nx
import math

def load_graph(nodes_path, edges_path, alpha=0.25):
    """
    threshold = ceil(alpha * degree)
    """
    G = nx.Graph()

    with open(nodes_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            opinion = row["opinion"]
            if opinion == "Neutral":
                opinion = None

            G.add_node(
                int(row["node"]),
                opinion=opinion
            )

    with open(edges_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            G.add_edge(int(row["source"]), int(row["target"]))

    # Assign degree-based thresholds
    for node in G.nodes():
        degree = G.degree(node)
        G.nodes[node]["threshold"] = max(1, math.ceil(alpha * degree))

    return G
