# src/save_csv1.py
import csv
import os

BASE_DIR = "results/logs"
FILE_NAME = "iteration_log.csv"

def save_iteration_wise(history):
    os.makedirs(BASE_DIR, exist_ok=True)
    path = os.path.join(BASE_DIR, FILE_NAME)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["itr", "node", "opinion", "threshold"])

        for snapshot in history:
            for row in snapshot:
                writer.writerow(row)

    print(f"💾 Iteration-wise log saved → {path}")
