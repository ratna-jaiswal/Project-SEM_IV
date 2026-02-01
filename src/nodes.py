# src/nodes.py
import csv
import random
import os
from constants import OPINION_MAP

RAW_DIR = "data/raw"

def create_nodes_csv(n=100, filename="nodes.csv"):
    os.makedirs(RAW_DIR, exist_ok=True)
    filename = os.path.join(RAW_DIR, filename)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "opinion", "threshold"])

        for i in range(n):
            opinion = random.choice(list(OPINION_MAP.keys()))
            threshold = random.randint(1, 2)
            # threshold = random.uniform(0.4, 0.9)
            writer.writerow([i, opinion, threshold])
