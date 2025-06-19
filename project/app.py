# 루트 진입점 – Streamlit Cloud는 이 파일부터 실행합니다.
import streamlit as st
from pages.data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs‑13 기후 피해 예측", layout="wide")

st.title("🌍 SDGs‑13 Climate‑Disaster Dashboard")
st.markdown("좌측 사이드바에서 **‘SDGs‑13’** 페이지를 눌러 상세 시뮬레이션을 실행하세요.")

# ── 데이터 미리보기 ─────────────────────────────────────────
try:
    st.subheader("📑 Weather Data Preview (Top‑5)")
    st.dataframe(load_weather_data().head())
    st.subheader("📑 Disaster Data Preview (Top‑5)")
    st.dataframe(load_disaster_data().head())
except FileNotFoundError as e:
    st.error(str(e))
