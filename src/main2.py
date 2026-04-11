import pandas as pd
import networkx as nx
import random
from tqdm import tqdm
import os
import math

# =========================
# PARAMETERS
# =========================
NUM_ITERATIONS = 50
REVIEWS_PER_ITER = 100

alpha = 0.15   # neighbors influence
beta = 0.1   # reviews influence

base_path = r"D:\SEM-6\Project\data\raw"

# =========================
# LOAD FILES
# =========================
edges_df = pd.read_csv(os.path.join(base_path, "social_network.csv"))
users_df = pd.read_csv(os.path.join(base_path, "users.csv"))
reviews_df = pd.read_excel(os.path.join(base_path, "IMDB_Opinions_dataset.xlsx"))

opinion_list = reviews_df["Opinion"].dropna().tolist()

# =========================
# CREATE GRAPH
# =========================
G = nx.from_pandas_edgelist(edges_df, "source", "target")

# =========================
# ASSIGN INITIAL OPINIONS
# =========================
opinion_dict = dict(zip(users_df["user"], users_df["opinion"]))

for node in G.nodes():
    val = opinion_dict.get(node, None)
    if pd.isna(val):
        G.nodes[node]['opinion'] = None
    else:
        G.nodes[node]['opinion'] = float(val)

# =========================
# LOG STORAGE
# =========================
opinion_logs = {node: [] for node in G.nodes()}

# store initial state
for node in G.nodes():
    opinion_logs[node].append(G.nodes[node]['opinion'])

# =========================
# SIMULATION LOOP
# =========================
for it in tqdm(range(NUM_ITERATIONS), desc="Iterations"):

    new_opinions = {}

    for node in G.nodes():
        current_opinion = G.nodes[node]['opinion']

        # -------- neighbors --------
        neighbors = list(G.neighbors(node))
        neighbor_opinions = [
            G.nodes[n]['opinion']
            for n in neighbors
            if G.nodes[n]['opinion'] is not None
        ]

        if neighbor_opinions:
            neighbor_avg = sum(neighbor_opinions) / len(neighbor_opinions)
        else:
            neighbor_avg = 0

        # -------- reviews --------
        review_sample = random.sample(opinion_list, REVIEWS_PER_ITER)
        review_avg = sum(review_sample) / len(review_sample)

        # -------- update rule (NON-LINEAR) --------

        if current_opinion is None:
            raw_update = 0.5 * neighbor_avg + 0.5 * review_avg
        else:
            raw_update = (
                (1 - alpha - beta) * current_opinion
                + alpha * neighbor_avg
                + beta * review_avg
            )

        # Apply non-linear transformation
        new_opinion = math.tanh(1.5 * raw_update)

        new_opinions[node] = new_opinion

    # apply updates
    for node in G.nodes():
        G.nodes[node]['opinion'] = new_opinions[node]

    # store logs
    for node in G.nodes():
        opinion_logs[node].append(G.nodes[node]['opinion'])

# =========================
# CONVERT TO DATAFRAME
# =========================
log_df = pd.DataFrame(opinion_logs).T

log_df.columns = [f"Iter_{i}" for i in range(NUM_ITERATIONS + 1)]
log_df = log_df.sort_index()
log_df.insert(0, "Node", log_df.index)

# =========================
# SAVE OUTPUT
# =========================
output_path = os.path.join(r"D:\SEM-6\Project\results\logs", "opinion_dynamics.xlsx")
log_df.to_excel(output_path, index=False)

print(f"✅ Simulation complete. File saved at: {output_path}")