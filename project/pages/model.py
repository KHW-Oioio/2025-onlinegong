import numpy as np, networkx as nx

REGION_EDGES = [
    ("RegionA", "RegionB"),
    ("RegionA", "RegionC"),
    ("RegionB", "RegionC"),
]

def build_graph(regions):
    G = nx.Graph()
    for r in regions:
        G.add_node(r)
    for u, v in REGION_EDGES:
        if u in regions and v in regions:
            G.add_edge(u, v, weight=1)
    return G


def run_monte_carlo(base_damage, mean_temp, std_temp,
                    precip, wind, policy_reduction=0.0,
                    iterations=1000):
    np.random.seed(42)
    temp   = np.random.normal(mean_temp, std_temp, iterations)
    precip = np.random.choice(precip, iterations)
    wind   = np.random.choice(wind, iterations)

    damages = (
        base_damage *
        (1 + 0.25*temp) *
        (1 + 0.1*precip/100) *
        (1 + 0.05*wind/10)
    )
    damages *= (1 - policy_reduction)
    return damages
