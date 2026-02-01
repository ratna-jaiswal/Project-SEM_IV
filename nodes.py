import csv
import random

NUM_NODES = 100

opinions = ["Yes", "No", None]  # None = neutral / no opinion

with open("nodes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["node", "opinion", "threshold"])

    for i in range(NUM_NODES):
        opinion = random.choice(opinions)
        threshold = random.randint(1, 50)
        writer.writerow([i, opinion, threshold])

print("nodes.csv created with random opinions and thresholds")