import networkx as nx

def opinion_counts(G):
    counts = {"Yes": 0, "No": 0, "Neutral": 0}
    for _, d in G.nodes(data=True):
        if d["opinion"] == "Yes":
            counts["Yes"] += 1
        elif d["opinion"] == "No":
            counts["No"] += 1
        else:
            counts["Neutral"] += 1
    return counts


def opinion_fractions(G):
    total = G.number_of_nodes()
    return {k: round(v / total, 3) for k, v in opinion_counts(G).items()}


def degree_stats(G):
    degrees = [deg for _, deg in G.degree()]
    return {
        "min": min(degrees),
        "max": max(degrees),
        "avg": round(sum(degrees) / len(degrees), 2)
    }


def clustering_stats(G):
    return round(nx.average_clustering(G), 3)


def connected_components_stats(G):
    comps = list(nx.connected_components(G))
    sizes = [len(c) for c in comps]
    return {
        "num_components": len(comps),
        "largest_component_size": max(sizes)
    }


def centrality_stats(G, top_k=5):
    deg_c = nx.degree_centrality(G)
    bet_c = nx.betweenness_centrality(G)

    return {
        "top_degree_centrality": sorted(deg_c.items(), key=lambda x: x[1], reverse=True)[:top_k],
        "top_betweenness_centrality": sorted(bet_c.items(), key=lambda x: x[1], reverse=True)[:top_k]
    }


def convergence_type(G):
    c = opinion_counts(G)
    non_neutral = c["Yes"] + c["No"]

    if non_neutral == 0:
        return "All Neutral"
    if c["Yes"] == non_neutral:
        return "Yes Consensus"
    if c["No"] == non_neutral:
        return "No Consensus"
    return "Polarized"


def print_detailed_stats(G):
    print("\n===== OPINION STATS =====")
    print("Counts     :", opinion_counts(G))
    print("Fractions  :", opinion_fractions(G))

    print("\n===== NETWORK STATS =====")
    print("Degree     :", degree_stats(G))
    print("Clustering :", clustering_stats(G))
    print("Components :", connected_components_stats(G))

    print("\n===== INFLUENCE =====")
    c = centrality_stats(G)
    print("Top Degree Centrality     :", c["top_degree_centrality"])
    print("Top Betweenness Centrality:", c["top_betweenness_centrality"])

    print("\n===== OUTCOME =====")
    print("Convergence Type:", convergence_type(G))
