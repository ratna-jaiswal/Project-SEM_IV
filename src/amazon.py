import pandas as pd
import networkx as nx
import random
from tqdm import tqdm
import os
import math
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# =========================
# DOWNLOAD (FIRST TIME ONLY)
# =========================
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# =========================
# PARAMETERS
# =========================
NUM_ITERATIONS = 50
REVIEWS_PER_ITER = 100

alpha = 0.3   # neighbors influence (recommended)
beta = 0.2    # reviews influence

base_path = r"D:\SEM-6\Project\data\raw"

# =========================
# LOAD FILES
# =========================
edges_df = pd.read_csv(os.path.join(base_path, "social_network.csv"))
users_df = pd.read_csv(os.path.join(base_path, "users.csv"))

amazon_df = pd.read_csv(
    os.path.join(base_path, "Amazon_Reviews.csv"),
    on_bad_lines='skip',
    engine='python'
)

# =========================
# PREPROCESS AMAZON DATA
# =========================

# ---- Rating → numeric ----
amazon_df['Rating'] = amazon_df['Rating'].astype(str).str.extract(r'(\d)').astype(float)

# ---- Normalize rating [-1,1] ----
amazon_df['rating_opinion'] = (amazon_df['Rating'] - 3) / 2

# ---- Sentiment from text ----
def get_sentiment(text):
    text = str(text)
    return sia.polarity_scores(text)["compound"]

amazon_df['sentiment'] = amazon_df['Review Text'].apply(get_sentiment)

# ---- Final opinion ----
amazon_df['final_opinion'] = 0.5 * amazon_df['rating_opinion'] + 0.5 * amazon_df['sentiment']

# ---- Review count → weight ----
amazon_df['Review Count'] = amazon_df['Review Count'].astype(str).str.extract(r'(\d+)').astype(float)
amazon_df['weight'] = 1 + amazon_df['Review Count'].fillna(1)

# ---- Optional: time decay (can comment if not needed) ----
amazon_df['Review Date'] = pd.to_datetime(amazon_df['Review Date'], errors='coerce')
latest_date = amazon_df['Review Date'].max()

amazon_df['time_diff'] = (latest_date - amazon_df['Review Date']).dt.days
amazon_df['time_diff'] = amazon_df['time_diff'].fillna(0)

amazon_df['time_weight'] = 1 / (1 + amazon_df['time_diff'])
amazon_df['weight'] = amazon_df['weight'] * amazon_df['time_weight']

# ---- Clean ----
amazon_df = amazon_df.dropna(subset=['final_opinion'])

# ---- Create sampling lists ----
review_opinions = amazon_df['final_opinion'].tolist()
review_weights = amazon_df['weight'].tolist()

# =========================
# CREATE GRAPH
# =========================
G = nx.from_pandas_edgelist(edges_df, "source", "target")

# =========================
# INITIAL OPINIONS
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

# initial state
for node in G.nodes():
    opinion_logs[node].append(G.nodes[node]['opinion'])

# =========================
# FUNCTION: SAMPLE REVIEWS
# =========================
def sample_reviews(k=100):
    sampled = random.choices(
        list(zip(review_opinions, review_weights)),
        weights=review_weights,
        k=k
    )
    opinions = [x[0] for x in sampled]
    return sum(opinions) / len(opinions)

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
        review_avg = sample_reviews(REVIEWS_PER_ITER)

        # -------- update rule --------
        if current_opinion is None:
            raw_update = 0.5 * neighbor_avg + 0.5 * review_avg
        else:
            raw_update = (
                (1 - alpha - beta) * current_opinion
                + alpha * neighbor_avg
                + beta * review_avg
            )

        # -------- NON-LINEAR TRANSFORMATION --------
        new_opinion = math.tanh(1.2 * raw_update)  # smoother than 1.5

        new_opinions[node] = new_opinion

    # apply updates
    for node in G.nodes():
        G.nodes[node]['opinion'] = new_opinions[node]

    # store logs
    for node in G.nodes():
        opinion_logs[node].append(G.nodes[node]['opinion'])

# =========================
# SAVE RESULTS
# =========================
log_df = pd.DataFrame(opinion_logs).T

log_df.columns = [f"Iter_{i}" for i in range(NUM_ITERATIONS + 1)]
log_df.insert(0, "Node", log_df.index)

output_path = r"D:\SEM-6\Project\results\logs\amazon_opinion_dynamics.xlsx"
log_df.to_excel(output_path, index=False)

print(f"✅ Simulation complete. File saved at: {output_path}")