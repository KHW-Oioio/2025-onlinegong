import numpy as np
import pandas as pd

def run_monte_carlo(base_damage, policy_effectiveness=0.1, simulations=1000):
    results = []
    for _ in range(simulations):
        random_factor = np.random.normal(loc=1 - policy_effectiveness, scale=0.05)
        result = max(base_damage * random_factor, 0)
        results.append(result)
    return results
