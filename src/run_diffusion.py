import random
import csv

def log_iteration(G, iteration, writer):
    """Log all nodes' state for the given iteration."""
    for node in G.nodes():
        opinion = G.nodes[node]["opinion"]
        threshold = G.nodes[node]["threshold"]
        writer.writerow([iteration, node, opinion, threshold])

def decide_opinion(current, yes_count, no_count, threshold):
    yes_ok = yes_count >= threshold
    no_ok = no_count >= threshold

    if yes_ok and no_ok:
        return random.choice(["Yes", "No"])

    if yes_ok:
        return "Yes"

    if no_ok:
        return "No"

    return current


def run_diffusion(G, max_iterations=100, log_csv_path="results/simulation_log.csv"):
    history = {
        "Yes": [],
        "No": [],
        "Neutral": []
    }

    # 🔹 NEW: open CSV file
    with open(log_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "node", "opinion", "threshold"])

        # 🔹 NEW: log initial state (iteration 0)
        log_iteration(G, 0, writer)

        for iteration in range(1, max_iterations + 1):
            updates = {}

            # READ phase
            for node in G.nodes():
                current = G.nodes[node]["opinion"]
                threshold = G.nodes[node]["threshold"]

                yes_count = 0
                no_count = 0

                for nbr in G.neighbors(node):
                    op = G.nodes[nbr]["opinion"]
                    if op == "Yes":
                        yes_count += 1
                    elif op == "No":
                        no_count += 1

                new_opinion = decide_opinion(
                    current, yes_count, no_count, threshold
                )

                if new_opinion != current:
                    updates[node] = new_opinion

            # STOP if converged
            if not updates:
                print(f"Converged at iteration {iteration}")
                break

            # WRITE phase
            for node, op in updates.items():
                G.nodes[node]["opinion"] = op

            # 🔹 NEW: log current iteration
            log_iteration(G, iteration, writer)

            # Track stats
            yes = no = neutral = 0
            for _, data in G.nodes(data=True):
                if data["opinion"] == "Yes":
                    yes += 1
                elif data["opinion"] == "No":
                    no += 1
                else:
                    neutral += 1

            history["Yes"].append(yes)
            history["No"].append(no)
            history["Neutral"].append(neutral)

            print(
                f"Iteration {iteration}: "
                f"Yes={yes}, No={no}, Neutral={neutral}"
            )

    return history
