#main.py

import random
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

from data_generation import generate_network, generate_news, generate_users
from imbd_dataset import generate_news_from_imdb
from graph_utils import (
    draw_network_graph,
    plot_opinion_evolution,
    plot_opinion_variance,
    plot_user_trajectories,
    plot_distribution_kde,
    plot_opinion_distribution_per_iteration
)

SEED = 42
# random.seed(SEED)

# PATH SETUP (IMPORTANT)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
LOGS_DIR = BASE_DIR / "results" / "logs"
PLOTS_DIR = BASE_DIR / "results" / "plots"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# 4. Core Bias Functions

def ideological_congruence(user, row):
    return user["opinion"] * row["polarity"]

def bias_susceptibility(user, row):
    return max(0, min(1,
        0.4 * user["belief_strength"] +
        0.3 * (1 - user["thinking_style"]) +
        0.3 * row["issue_strength"]
    ))

def news_score(user, row):
    congruence = ideological_congruence(user, row)
    bias = bias_susceptibility(user, row)
    return (1 - bias) * 0.5 + bias * congruence

def rank_news(user, news_df):
    scores = {nid: news_score(user, row) for nid, row in news_df.iterrows()}
    return sorted(scores, key=scores.get, reverse=True)

def perceived_trust(user, row):
    congruence = ideological_congruence(user, row)
    bias = bias_susceptibility(user, row)
    trust = 0.5 + 0.5 * congruence * bias
    return max(0, min(1, trust))

def update_opinion_from_news(user, row, lr=0.1):
    trust = perceived_trust(user, row)
    user["opinion"] += lr * trust * (row["polarity"] - user["opinion"])
    user["belief_strength"] = min(
        1, user["belief_strength"] + 0.05 * trust * abs(row["polarity"])
    )

def social_influence(user_id, users, G, alpha=0.2):
    neighbors = list(G.neighbors(user_id))
    if neighbors:
        avg = sum(users[n]["opinion"] for n in neighbors) / len(neighbors)
        users[user_id]["opinion"] += alpha * (avg - users[user_id]["opinion"])


# 5. Simulation Parameters

NUM_USERS = 100
FEED_ROUNDS = 20
TOP_K = 10

# 6. Generate Static Data

# news = generate_news()
news = generate_news_from_imdb("D:/SEM-6/Project/data/raw/IMDB Dataset.csv", output_path="D:/SEM-6/Project/data/raw/imdb_generated_dataset.xlsx")
# news = pd.read_excel("D:/SEM-6/Project/data/raw/imdb_generated_dataset.xlsx")
# news.set_index("news_id", inplace=True)
# news = news.sample(5000, random_state=42)
users = generate_users(NUM_USERS)
G = generate_network(NUM_USERS)

# Save datasets
news.reset_index().to_excel(DATA_RAW_DIR / "news_generated.xlsx", index=False)
pd.DataFrame.from_dict(users, orient="index").to_excel(
    DATA_RAW_DIR / "users_generated.xlsx"
)
pd.DataFrame(G.edges(), columns=["source", "target"]).to_excel(
    DATA_RAW_DIR / "network_edges.xlsx", index=False
)

#    NETWORK GRAPH

draw_network_graph(G, users, PLOTS_DIR / "network_initial.png")


# 7. Simulation Loop

log_rows = []
ranking_log = []

for t in range(FEED_ROUNDS):
    for uid, user in users.items():

        ranking = rank_news(user, news)

        ranking_log.append({
            "iteration": t,
            "user_id": uid,
            "top_news": ranking[:TOP_K]
        })

        for nid in ranking[:TOP_K]:
            update_opinion_from_news(user, news.loc[nid])

        social_influence(uid, users, G)

        log_rows.append({
            "iteration": t,
            "user_id": uid,
            "opinion": user["opinion"],
            "belief_strength": user["belief_strength"],
            "thinking_style": user["thinking_style"]
        })


# 8. Save Logs

pd.DataFrame(log_rows).to_excel(
    LOGS_DIR / "confirmation_bias_network_log.xlsx",
    index=False
)

# Convert logs to DataFrame
log_df = pd.DataFrame(log_rows)

# ======================
# GENERATE ALL GRAPHS
# ======================

# 1. Final network graph
draw_network_graph(G, users, PLOTS_DIR / "network_final.png", title="Final Network")

# 2. Opinion evolution
plot_opinion_evolution(log_df, PLOTS_DIR / "opinion_evolution.png")

# 3. Polarization (variance)
plot_opinion_variance(log_df, PLOTS_DIR / "polarization.png")

# 5. Opinion distribution (KDE)
plot_distribution_kde(log_df, PLOTS_DIR / "distribution_kde.png")

# 6. User trajectories
plot_user_trajectories(log_df, PLOTS_DIR / "user_trajectories.png")

# 7. Opinion distribution per iteration
plot_opinion_distribution_per_iteration(log_df, PLOTS_DIR / "opinion_distribution_per_iteration.png")


pd.DataFrame(ranking_log).to_excel(
    LOGS_DIR / "ranking_log.xlsx",
    index=False
)


