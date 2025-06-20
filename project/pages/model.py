import numpy as np, networkx as nx

REGION_EDGES = [("Seoul","Busan"),("Seoul","Daegu"),("Busan","Daegu")]

def build_graph(nodes):
    G = nx.Graph()
    for n in nodes: G.add_node(n)
    for u,v in REGION_EDGES:
        if u in nodes and v in nodes:
            G.add_edge(u,v)
    return G

def run_mc(base, mean, std, precip, wind, policy=0.0, n=1000):
    np.random.seed(42)
    t = np.random.normal(mean,std,n)
    p = np.random.choice(precip,n)
    w = np.random.choice(wind,n)
    dmg = base*(1+0.25*t)*(1+0.1*p/100)*(1+0.05*w/10)
    return dmg*(1-policy)
