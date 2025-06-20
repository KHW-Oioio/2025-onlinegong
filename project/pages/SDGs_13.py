import streamlit as st
import pandas as pd
import os, sys

# 상위 폴더 경로를 Python 모듈 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__init__), "..")))

from data_loader import load_weather_data, load_disaster_data, COUNTRY_COORDS
from model import build_graph, run_mc
from utils import hist, heat, pie

st.title("🌍 SDGs‑13 Climate & Disaster Simulation Dashboard")
st.markdown("이 대시보드는 기후 변수 및 재난 데이터를 기반으로 **의사결정 및 정책 영향**을 분석합니다.")

# 국가 선택
country = st.sidebar.selectbox("국가를 선택하세요", list(COUNTRY_COORDS.keys()))
weather = load_weather_data(country)
disaster_df = load_disaster_data()

st.header(f"📊 {country} 기상 데이터 요약")
st.line_chart(weather.set_index("date")["temp"], use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    hist(weather["precip"], "📈 강수량 분포")
with col2:
    heat(weather[["temp", "precip", "wind"]], "📊 변수 간 상관관계")

st.subheader("💥 재난 피해 시각화")
agg = disaster_df.groupby("region")["damage_amount_hundred_million_won"].sum().sort_values(ascending=False)
pie(agg, "🌪️ 누적 재난 피해 (억원)")

# 몬테카를로 시뮬레이션
st.header("🎲 정책 시뮬레이션")
st.markdown("정책 효과를 반영한 피해 예측 (Monte Carlo)")

region_name = country.split(",")[0]
region_df = disaster_df[disaster_df["region"].str.contains(region_name, case=False)]

if region_df.empty:
    st.warning("해당 국가에 대한 재난 통계가 부족합니다. 다른 국가를 선택해보세요.")
else:
    base_damage = region_df["damage_amount_hundred_million_won"].mean()
    t_mean = weather["temp"].mean()
    t_std = weather["temp"].std()
    precip = weather["precip"].values
    wind = weather["wind"].values

    st.markdown(f"기준 피해: 약 {base_damage:.1f} 억원")

    col1, col2 = st.columns(2)
    with col1:
        policy = st.slider("정책 적용 효과 (0=무효, 1=100% 감축)", 0.0, 1.0, 0.25, 0.05)
    with col2:
        n = st.slider("시뮬레이션 횟수", 100, 3000, 1000, 100)

    sim_result = run_mc(base_damage, t_mean, t_std, precip, wind, policy, n=n)
    hist(sim_result, f"시뮬레이션 결과 (정책 반영률 {policy*100:.0f}%)")

    st.write(f"📌 평균 피해 예상: {sim_result.mean():,.1f} 억원")
    st.write(f"📌 피해 최소 ~ 최대 범위: {sim_result.min():.1f} ~ {sim_result.max():.1f} 억원")

st.caption("Data: Open‑Meteo API / UNDRR GAR API")
