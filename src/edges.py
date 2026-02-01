# src/edges.py
import os
import csv
import random

RAW_DIR = "data/raw"

def create_edges_csv(n=100, min_deg=3, max_deg=10, filename="edges.csv"):

    os.makedirs(RAW_DIR, exist_ok=True)
    filename = os.path.join(RAW_DIR, filename)
    
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target"])

        for u in range(n):
            k = random.randint(min_deg, max_deg)
            targets = random.sample(range(n), k)
            for v in targets:
                if u != v:
                    writer.writerow([u, v])
