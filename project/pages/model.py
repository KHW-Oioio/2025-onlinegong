# pages/model.py

import numpy as np
import networkx as nx
import pandas as pd

# --- 1. 지역 연결 그래프 (가중치 = 가까움) ----------------------
REGION_EDGES = [
    ("RegionA", "RegionB"),
    ("RegionA", "RegionC"),
    ("RegionB", "RegionC")
]

def build_graph(regions):
    G = nx.Graph()
    for r in regions:
        G.add_node(r)
    for u, v in REGION_EDGES:
        if u in regions and v in regions:
            G.add_edge(u, v, weight=1)
    return G

# --- 2. 몬테카를로 + 정책 시나리오 ---------------------------
def run_monte_carlo(base_damage, mean_temp, std_temp,
                    precip, wind, policy_reduction=0.0,
                    iterations=1000):
    """
    base_damage : 기본 피해액(억)
    mean_temp, std_temp : 온도 평균과 표준편차
    precip, wind : 강수량·풍속 시계열 (리스트)
    policy_reduction : 온실가스 감축률(0~1) → 피해감소율에 선형 반영
    """
    np.random.seed(42)
    temp_rng = np.random.normal(mean_temp, std_temp, iterations)
    precip_rng = np.random.choice(precip, iterations)
    wind_rng = np.random.choice(wind, iterations)

    # 다변량 영향 계수 (가중치 임의 설정)
    damages = (
        base_damage *
        (1 + 0.25 * temp_rng) *
        (1 + 0.1 * precip_rng / 100) *
        (1 + 0.05 * wind_rng / 10)
    )

    # 정책 시나리오 반영
    damages *= (1 - policy_reduction)
    return damages
