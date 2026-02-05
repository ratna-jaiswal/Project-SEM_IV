import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

 
# Paths & folders
 
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "raw"
PLOTS_DIR = BASE_DIR / "results" / "plots"
LOGS_DIR = BASE_DIR / "results" / "logs"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

 
# Load news data
 
news = pd.read_csv(DATA_DIR / "news.csv")
news_map = news.set_index("news_id")

 
# Initial preference ranking (given by the person)
 
initial_ranking = [
    "N3", "N1", "N7", "N5", "N2",
    "N4", "N6", "N8", "N9", "N10"
]

 
# Scoring function (FEATURE-WISE)
 
def news_score(row, revealed_features):
    score = 0

    if "polarity" in revealed_features:
        score += row["polarity"] * 1
        # score += row["polarity"] * 0.95

    if "truth" in revealed_features:
        score += row["truth"] * 1
        # score += row["truth"] * 0.81

    if "emotion_strength" in revealed_features:
        score += row["emotion_strength"] * 1
        # score += row["emotion_strength"] * 0.78

    if "reach" in revealed_features:
        score += row["reach"] * 1
        # score += row["reach"] * 0.23

    if "novelty" in revealed_features:
        score += row["novelty"] * 1
        # score += row["novelty"] * 0.58

    return score

 
# Re-ranking logic
 
def rerank(current_ranking, revealed_features):
    scores = {}

    for nid in current_ranking:
        scores[nid] = news_score(news_map.loc[nid], revealed_features)

    return sorted(current_ranking, key=lambda x: scores[x], reverse=True)

 
# Feature-wise reveal order
 
feature_reveal_order = [
    "polarity",
    "truth",
    "emotion_strength",
    "reach",
    "novelty"
]

 
# Simulation
 
ranking = initial_ranking.copy()
revealed_features = []
ranking_history = []

for step, feature in enumerate(feature_reveal_order):
    revealed_features.append(feature)
    ranking = rerank(ranking, revealed_features)

    ranking_history.append({
        "step": step,
        "revealed_feature": feature,
        "ranking": ranking.copy()
    })

    print(f"After revealing feature: {feature}")
    print(ranking)
    print("-" * 40)

 
# Helper: rank position
 
def rank_position(ranking, news_id):
    return ranking.index(news_id) + 1

 
# Save ranking log in WIDE format
 
all_news_ids = news["news_id"].tolist()

wide_log = {"news_id": all_news_ids}

for step in ranking_history:
    step_no = step["step"]
    ranking = step["ranking"]

    col_name = f"step{step_no}"
    wide_log[col_name] = [
        rank_position(ranking, nid) for nid in all_news_ids
    ]

wide_log_df = pd.DataFrame(wide_log)

wide_log_df.to_csv(
    LOGS_DIR / "preference_ranking_log_wide1.csv",
    index=False
)

 
# Plot: all news preference changes
 
all_news_ids = news["news_id"].tolist()
rank_positions = {nid: [] for nid in all_news_ids}

for step in ranking_history:
    ranking = step["ranking"]
    for nid in all_news_ids:
        rank_positions[nid].append(rank_position(ranking, nid))

plt.figure(figsize=(10, 6))

for nid, positions in rank_positions.items():
    plt.plot(positions, marker="o", label=nid, alpha=0.8)

plt.xlabel("Feature reveal step")
plt.ylabel("Rank position")
plt.title("Change in Preference Order (Feature-wise Reveal)")
plt.gca().invert_yaxis()
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

plt.savefig(PLOTS_DIR / "all_news_preference_changes1.png")
plt.show()


