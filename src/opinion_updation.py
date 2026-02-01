# src/opinion_updation.py

def update_opinion(G, node):
    current = G.nodes[node]["opinion"]
    threshold = G.nodes[node]["threshold"]

    influencers = list(G.predecessors(node))
    if not influencers:
        return current

    avg = sum(G.nodes[n]["opinion"] for n in influencers) / len(influencers)

    if avg > current + threshold and current < 5:
        return current + 1
    elif avg < current - threshold and current > 1:
        return current - 1
    else:
        return current
