import csv

nodes = [
    ("A", "yes"),
    ("B", "no"),
    ("C", "yes"),
    ("D", "no"),
    ("E", "yes"),
    ("F", "no"),
    ("G", "yes"),
    ("H", "no"),
    ("I", "yes"),
    ("J", "no")
]

with open("nodes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["node", "opinion"])
    writer.writerows(nodes)

print("nodes.csv created with 10 nodes")
