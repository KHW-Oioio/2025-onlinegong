import streamlit as st
import os, sys
ROOT = os.path.dirname(__file__)
PAGES = os.path.join(ROOT, "pages")
if PAGES not in sys.path:
    sys.path.append(PAGES)

from data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs‑13 기후 대시보드", layout="wide")
st.title("🌍 SDGs‑13 기후 변화 피해 분석")
st.markdown("사이드바에서 상세 분석 페이지를 선택하세요.")

try:
    weather = load_weather_data()
    disaster = load_disaster_data()
    st.success("✅ 데이터 로드 성공")
    st.dataframe(weather.head())
    st.dataframe(disaster.head())
except Exception as e:
    st.error(str(e))

