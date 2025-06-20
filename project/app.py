import streamlit as st
from pages.data_loader import load_weather_data, load_disaster_data, COUNTRY_COORDS

st.set_page_config(page_title="SDGs‑13 Global Simulator", layout="wide")

st.title("🌍 SDGs‑13 Global Climate‑Disaster Dashboard")
st.markdown("왼쪽 메뉴에서 **‘SDGs‑13 Dashboard’** 페이지를 클릭하세요.")

st.write("**지원 국가 수:**", len(COUNTRY_COORDS))

try:
    st.subheader("📑 Weather CSV (Top‑5 rows)")
    st.dataframe(load_weather_data(list(COUNTRY_COORDS.keys())[0]).head())
except Exception as e:
    st.warning(e)

try:
    st.subheader("📑 Disaster CSV (Top‑5 rows)")
    st.dataframe(load_disaster_data().head())
except Exception as e:
    st.warning(e)
