import pandas as pd
import networkx as nx
import random
import os

# =========================
# PARAMETERS
# =========================
NUM_NODES = 100
INITIAL_OPINION_PERCENT = 0.5

# Save path
base_path = r"D:\SEM-6\Project\data\raw"
os.makedirs(base_path, exist_ok=True)

# =========================
# CREATE NETWORK (Scale-Free - Highly Connected)
# =========================
G = nx.barabasi_albert_graph(NUM_NODES, m=4)  # Uncomment for scale-free network

# Or keep Small World for controlled connectivity
# G = nx.watts_strogatz_graph(NUM_NODES, k=10, p=0.1)

# =========================
# SAVE EDGES (source-target)
# =========================
edges_df = pd.DataFrame(G.edges(), columns=["source", "target"])

edges_path = os.path.join(base_path, "social_network.csv")
edges_df.to_csv(edges_path, index=False)

# =========================
# GENERATE USER OPINIONS
# =========================
nodes = list(G.nodes())
initial_nodes = random.sample(nodes, int(INITIAL_OPINION_PERCENT * NUM_NODES))

user_data = []

for node in nodes:
    if node in initial_nodes:
        # random opinion between -1 and 1
        opinion = round(random.uniform(-1, 1), 4)
    else:
        opinion = None

    user_data.append([node, opinion])

user_df = pd.DataFrame(user_data, columns=["user", "opinion"])

user_path = os.path.join(base_path, "users.csv")
user_df.to_csv(user_path, index=False)

# =========================
# DONE
# =========================
print("✅ Files generated:")
print(f"📁 {edges_path}")
print(f"📁 {user_path}")