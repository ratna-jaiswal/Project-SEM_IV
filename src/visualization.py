import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, title="Opinion Network"):
    colors = []

    for _, data in G.nodes(data=True):
        if data["opinion"] == "Yes":
            colors.append("green")
        elif data["opinion"] == "No":
            colors.append("red")
        else:
            colors.append("gray")

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        node_color=colors,
        node_size=80,
        edge_color="lightgray",
        with_labels=False
    )

    plt.title(title)
    plt.show()

