import streamlit as st, pandas as pd
from pages.data_loader import load_weather_data, load_disaster_data, REGION_COORDS
from pages.model import build_graph, run_monte_carlo
from pages.utils import plot_histogram, plot_correlation, plot_pie, make_damage_map

# ── 데이터 로드 ───────────────────────────────────────────
weather = load_weather_data()
disaster = load_disaster_data()

# ── 사용자 입력 ───────────────────────────────────────────
regions = sorted({c.split("_")[0] for c in weather.columns if "_temp" in c})
region = st.sidebar.selectbox("지역", regions)
policy = st.sidebar.slider("온실가스 감축률(%)", 0, 100, 20)
mean_temp = st.sidebar.slider("예상 기온 상승(°C)", 1.0, 4.0, 2.0, 0.1)
std_temp = st.sidebar.slider("기온 표준편차", 0.1, 1.0, 0.3, 0.1)
iterations = st.sidebar.number_input("반복 횟수", 1000, 10000, 2000, 500)

st.header(f"📈 {region} 시뮬레이션 결과")

# ── 데이터 추출 ───────────────────────────────────────────
mask = disaster["region"].str.lower() == region.lower()
base_damage = disaster.loc[mask, "damage_amount_hundred_million_won"].mean()
base_damage = 0 if pd.isna(base_damage) else base_damage

temp   = weather[f"{region}_temp"].dropna()
precip = weather[f"{region}_precip"].dropna()
wind   = weather[f"{region}_wind"].dropna()

# ── 시뮬레이션 ────────────────────────────────────────────
if st.button("▶ 실행"):
    damages = run_monte_carlo(base_damage, mean_temp, std_temp,
                              precip, wind, policy/100, iterations)
    st.success(f"예측 평균 피해액: {damages.mean():.2f} 억")

    plot_histogram(damages, "예측 피해액 분포")

    multiv_df = pd.DataFrame({
        "temp": temp, "precip": precip, "wind": wind
    }).dropna()
    plot_correlation(multiv_df, "기상 변수 상관관계")

    plot_pie(disaster.groupby("region")["damage_amount_hundred_million_won"].sum(),
             "지역별 누적 피해액")

    make_damage_map(disaster.groupby("region")["damage_amount_hundred_million_won"].mean(),
                    REGION_COORDS)

    G = build_graph(REGION_COORDS.keys())
    st.info(f"그래프 노드: {list(G.nodes())} / 엣지: {list(G.edges())}")
