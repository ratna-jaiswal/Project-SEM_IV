# data_generation.py

import random

import networkx as nx
import pandas as pd


# =================================================
# 1. Generate Synthetic News (Paper-aligned)
# =================================================

def generate_news():
    news = []
    topics = [
        "abortion",
        "same_sex_marriage",
        "vegetarianism",
        "data_privacy",
        "drug_legalization",
        "gender_neutral_pronouns",
        "ai_surveillance",
    ]
    nid = 0

    for topic in topics:
        for stance in [-1, 1]:
            for _ in range(4):
                news.append(
                    {
                        "news_id": f"N{nid}",
                        "topic": topic,
                        "polarity": stance,
                        "issue_strength": random.uniform(0.4, 1.0),
                        "truth": random.uniform(0.4, 0.9),
                    }
                )
                nid += 1

    return pd.DataFrame(news).set_index("news_id")


# =================================================
# 2. Generate Users
# =================================================

def generate_users(n):
    users = {}
    for i in range(n):
        users[i] = {
            "opinion": random.uniform(-0.3, 0.3),
            "belief_strength": random.uniform(0.3, 0.7),
            "thinking_style": random.uniform(0.2, 0.8),
        }
    return users


# =================================================
# 3. Generate Network
# =================================================

def generate_network(n, p=0.2):
    return nx.erdos_renyi_graph(n, p, directed=True)
