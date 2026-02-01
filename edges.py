import csv
import random

from nodes import NUM_NODES

edges = set()

for i in range(NUM_NODES):
    # each node can connect to ANY number of nodes
    num_connections = random.randint(1, NUM_NODES // 2)

    for _ in range(num_connections):
        j = random.randint(0, NUM_NODES - 1)
        if i != j:
            edges.add(tuple(sorted((i, j))))  # avoid duplicates

with open("edges.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target"])

    for u, v in edges:
        writer.writerow([u, v])

print("edges.csv created with random edges")