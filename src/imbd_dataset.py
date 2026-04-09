# imdb_dataset.py

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk

# Initialize VADER
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def compute_features(text):
    text = str(text)

    # 1. VADER sentiment intensity
    vader_score = abs(sia.polarity_scores(text)["compound"])

    # 2. Subjectivity (TextBlob)
    subjectivity = TextBlob(text).sentiment.subjectivity

    # 3. Emphasis (simple heuristic)
    emphasis = min(1, (text.count("!") + text.isupper()) / 5)

    # 4. Issue Strength (combined)
    issue_strength = 0.5 * vader_score + 0.3 * subjectivity + 0.2 * emphasis

    return issue_strength


def generate_news_from_imdb(input_path, output_path=None, sample_size=5000):
    # Load dataset
    df = pd.read_csv(input_path)

    # Clean
    df = df.dropna(subset=["review", "sentiment"])

    # Optional: reduce size for simulation
    if sample_size is not None:
        df = df.sample(sample_size, random_state=42)

    # Polarity mapping
    df["polarity"] = df["sentiment"].map({
        "positive": 1,
        "negative": -1
    })

    # Compute features
    issue_strength_list = []

    for text in df["review"]:
        issue_strength = compute_features(text)
        issue_strength_list.append(issue_strength)

    df["issue_strength"] = issue_strength_list

    # Create news_id
    df["news_id"] = ["N" + str(i) for i in range(len(df))]
    df.set_index("news_id", inplace=True)

    # Final dataset (topic not needed)
    final_df = df[["polarity", "issue_strength"]]

    # Save if needed
    if output_path:
        final_df.to_excel(output_path)

    return final_df