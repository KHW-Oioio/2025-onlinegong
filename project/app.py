import streamlit as st
from pages.data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs‑13 Simulator", layout="wide")

st.title("🌍 SDGs‑13 Climate & Disaster Dashboard (Streamlit Cloud edition)")
st.markdown("사이드바 메뉴에서 **‘SDGs‑13 Dashboard’** 페이지를 클릭해 시뮬레이션을 실행하세요.")

try:
    st.subheader("📑 Weather CSV preview (top‑5 rows)")
    st.dataframe(load_weather_data().head())
except Exception as e:
    st.warning(f"Weather CSV 로드 실패: {e}")

try:
    st.subheader("📑 Disaster CSV preview (top‑5 rows)")
    st.dataframe(load_disaster_data().head())
except Exception as e:
    st.warning(f"Disaster CSV 로드 실패: {e}")
