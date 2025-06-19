import streamlit as st, pandas as pd
from data_loader import load_weather_data, load_disaster_data, REGION_COORDS
from model import build_graph, run_monte_carlo
from utils import plot_histogram, plot_correlation, plot_pie, make_damage_map

# --- 0. 데이터 로드 -------------------------------------------------
weather = load_weather_data()
disaster = load_disaster_data()

# --- 1. 사용자 입력 -------------------------------------------------
region_cols = [c.split("_")[0] for c in weather.columns if "_temp" in c]
region = st.sidebar.selectbox("지역 선택", sorted(set(region_cols)))
policy = st.sidebar.slider("온실가스 감축률(%)", 0, 100, 20)
mean_temp = st.sidebar.slider("예상 기온 상승(°C)", 1.0, 4.0, 2.0, 0.1)
std_temp = st.sidebar.slider("기온 상승 표준편차", 0.1, 1.0, 0.3, 0.1)
iterations = st.sidebar.number_input("시뮬레이션 반복 횟수", 1000, 10000, 2000, 500)

st.header(f"📈 {region} 기후‑재난 시뮬레이션")

# --- 2. 데이터 추출 ------------------------------------------------
mask = disaster["region"].str.lower() == region.lower()
base_damage = disaster.loc[mask, "damage_amount_hundred_million_won"].mean()
if pd.isna(base_damage): base_damage = 0

# 온·강·풍 변수
temp_series   = weather[f"{region}_temp"].dropna()
precip_series = weather[f"{region}_precip"].dropna()
wind_series   = weather[f"{region}_wind"].dropna()

# --- 3. 시뮬레이션 실행 -------------------------------------------
if st.button("▶ 시뮬레이션 실행"):
    damages = run_monte_carlo(
        base_damage=base_damage,
        mean_temp=mean_temp,
        std_temp=std_temp,
        precip=precip_series,
        wind=wind_series,
        policy_reduction=policy/100,
        iterations=iterations,
    )
    st.success(f"예측 평균 피해액: {damages.mean():.2f} 억")

    # 히스토그램
    plot_histogram(damages, "예측 피해액 분포")

    # 다변량 상관 Heatmap
    multiv_df = pd.DataFrame({
        "temp": temp_series,
        "precip": precip_series,
        "wind": wind_series,
    }).dropna()
    plot_correlation(multiv_df, "기상 변수 상관관계")

    # 누적 피해 비율 파이차트
    plot_pie(
        disaster.groupby("region")["damage_amount_hundred_million_won"].sum(),
        "지역별 누적 피해액"
    )

    # 지도 시각화
    avg_damage_by_region = disaster.groupby("region")["damage_amount_hundred_million_won"].mean()
    st.subheader("🗺️ 지역별 평균 피해 지도")
    make_damage_map(avg_damage_by_region, REGION_COORDS, "평균 피해 지도")

    # 그래프 자료구조 시각 (텍스트 설명)
    G = build_graph(REGION_COORDS.keys())
    st.info(f"그래프 노드: {G.nodes()}, 엣지: {G.edges()}")
