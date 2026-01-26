import csv
import random
import math

def generate_nodes_csv(path, num_nodes=100):
    """
    Realistic initialization:
    ~70% Neutral
    ~15% Yes
    ~15% No
    """
    opinions = (
        ["Neutral"] * 60 +
        ["Yes"] * 20 +
        ["No"] * 20
    )
    random.shuffle(opinions)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "opinion"])

        for i in range(num_nodes):
            writer.writerow([i, opinions[i]])


def generate_edges_csv(path, num_nodes=100):
    edges = set()

    for i in range(num_nodes):
        num_connections = random.randint(3, 8)
        for _ in range(num_connections):
            j = random.randint(0, num_nodes - 1)
            if i != j:
                edges.add(tuple(sorted((i, j))))

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])
        for u, v in edges:
            writer.writerow([u, v])



if __name__ == "__main__":
    generate_nodes_csv("data/raw/nodes.csv")
    generate_edges_csv("data/raw/edges.csv")
