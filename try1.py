import csv
import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()

# ---------- LOAD NODES ----------
opinion_count = {"Yes": 0, "No": 0, "Neutral": 0}
thresholds = []

with open("nodes.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        node = int(row["node"])
        opinion = row["opinion"] if row["opinion"] != "" else None
        threshold = int(row["threshold"])

        G.add_node(node, opinion=opinion, threshold=threshold)
        thresholds.append(threshold)

        if opinion == "Yes":
            opinion_count["Yes"] += 1
        elif opinion == "No":
            opinion_count["No"] += 1
        else:
            opinion_count["Neutral"] += 1


# ---------- LOAD EDGES ----------
with open("edges.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        G.add_edge(int(row["source"]), int(row["target"]))


# ---------- PRINT DATASET STATS ----------
print("===== DATASET STATS =====")
print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())
print("Yes Opinions:", opinion_count["Yes"])
print("No Opinions:", opinion_count["No"])
print("Neutral (No Opinion):", opinion_count["Neutral"])
print("Threshold -> Min:", min(thresholds),
      "Max:", max(thresholds),
      "Average:", round(sum(thresholds) / len(thresholds), 2))


# ---------- DRAW GRAPH ----------
color_map = []

for node in G.nodes(data=True):
    if node[1]["opinion"] == "Yes":
        color_map.append("green")
    elif node[1]["opinion"] == "No":
        color_map.append("red")
    else:
        color_map.append("yellow")

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    node_color=color_map,
    node_size=80,
    edge_color="lightgray",
    with_labels=False
)

plt.title("Opinion Network (Green=Yes, Red=No, Gray=Neutral)")
plt.show()
