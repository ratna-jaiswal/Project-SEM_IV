# src/save_csv2.py
import csv
import os
from constants import REV_OPINION_MAP


BASE_DIR = "results/logs"
FILE_NAME = "node_opinion_matrix.csv"

def save_node_wise(matrix_history, G):
    os.makedirs(BASE_DIR, exist_ok=True)
    path = os.path.join(BASE_DIR, FILE_NAME)

    max_len = max(len(v) for v in matrix_history.values())

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["node", "final_opinion", "threshold"] + \
                 [f"itr{i}" for i in range(max_len)]
        writer.writerow(header)

        for node, ops in matrix_history.items():
            row = [
                node,
                REV_OPINION_MAP[G.nodes[node]["opinion"]],
                G.nodes[node]["threshold"]
            ] + ops
            writer.writerow(row)

    print(f"💾 Node-wise matrix saved → {path}")
