import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from tqdm import tqdm
import os

# Download once
nltk.download('vader_lexicon')

# Initialize
sia = SentimentIntensityAnalyzer()

# Enable progress bar for pandas
tqdm.pandas()

# Load dataset
df = pd.read_csv("D:/SEM-6/Project/data/raw/IMDB Dataset.csv")

# Opinion function
def compute_opinion(text):
    text = str(text)

    vader_score = sia.polarity_scores(text)["compound"]
    polarity = TextBlob(text).sentiment.polarity

    intensity = abs(vader_score)

    opinion = polarity * intensity

    return opinion

# Apply with progress bar
df["Opinion"] = df["review"].progress_apply(compute_opinion)

# Create Review IDs
df["Review_ID"] = ["R" + str(i+1) for i in range(len(df))]

# Select required columns
output_df = df[["Review_ID", "Opinion"]]

# Output path
output_path = r"D:\SEM-6\Project\data\raw\IMDB_Opinions_dataset.xlsx"

# Ensure folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save file
output_df.to_excel(output_path, index=False)

print(f"✅ File saved at: {output_path}")