import streamlit as st
from data_loader import load_weather_data, load_disaster_data
from utils import plot_temperature_trend, plot_correlation_heatmap, plot_disaster_bar, plot_pie_by_region
from model import run_policy_simulation
import numpy as np

st.set_page_config(page_title="SDGs‑13 분석", layout="wide")
st.title("🔥 기후 변화에 따른 재난 피해 분석 및 시뮬레이션")

weather = load_weather_data()
disaster = load_disaster_data()

st.header("1️⃣ 국가별 기온 변화")
country = st.selectbox("국가 선택", weather.columns.drop("date"))
plot_temperature_trend(weather, country)

st.header("2️⃣ 기온 상관관계 히트맵")
plot_correlation_heatmap(weather.drop("date", axis=1))

st.header("3️⃣ 재난 피해 분포")
plot_disaster_bar(disaster)

st.header("4️⃣ 연도별 피해 비율")
year = st.selectbox("연도 선택", sorted(disaster["year"].unique()))
plot_pie_by_region(disaster, year)

st.header("5️⃣ 정책 시뮬레이션")
base_damage = st.number_input("기본 피해액 (억 원)", value=1000)
temp_increase = st.slider("예상 기온 상승 (°C)", 0.0, 3.0, 1.5)
policy = st.slider("정책 감축 효과 (0~1)", 0.0, 1.0, 0.3)

simulated = run_policy_simulation(base_damage, temp_increase, policy)
st.line_chart(simulated)
