import numpy as np

def run_policy_simulation(base_damage, temp_increase, policy_effectiveness, iterations=1000):
    np.random.seed(42)
    random_temp = np.random.normal(temp_increase, 0.5, iterations)
    damages = base_damage * (1 + 0.2 * random_temp)
    damages *= (1 - policy_effectiveness)
    return damages
