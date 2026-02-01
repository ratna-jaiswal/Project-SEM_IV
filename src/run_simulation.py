#src/run_simulation.py
import random
from opinion_updation import update_opinion
from constants import REV_OPINION_MAP


def simulate(G, max_iter=20):
    history = []           # per-iteration snapshot
    matrix_history = {}    # node-wise history
    stats_history = []   # per-iteration stats

    for node in G.nodes:
        matrix_history[node] = []

    for itr in range(max_iter):
        changes = {}
        snapshot = []

        for node in G.nodes:
            new_op = update_opinion(G, node)
            changes[node] = new_op

        # apply synchronously
        stable = True
        for node, new_op in changes.items():
            if G.nodes[node]["opinion"] != new_op:
                stable = False
            G.nodes[node]["opinion"] = new_op

        # store data
        for node in G.nodes:
            op = G.nodes[node]["opinion"]
            th = G.nodes[node]["threshold"]

            snapshot.append([itr, node, REV_OPINION_MAP[op], th])
            matrix_history[node].append(REV_OPINION_MAP[op])

        history.append(snapshot)

        stats = {"A":0,"B":0,"C":0,"D":0,"E":0}
        for node in G.nodes:
            stats[REV_OPINION_MAP[G.nodes[node]["opinion"]]] += 1

        stats_history.append(stats)

        if stable:
            print(f"✔ Saturation reached at iteration {itr}")
            break

    return history, matrix_history, stats_history
