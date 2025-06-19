import streamlit as st
from data_loader import load_weather_data, load_disaster_data
st.set_page_config(page_title="SDGs13 기후 피해 예측", layout="wide")

st.title("🌏 SDGs‑13 기후 변화 피해 분석 대시보드")
st.markdown("사이드바에서 분석 페이지를 선택하세요.")
st.write("데이터 및 API 키 로딩 중…")
# 단순 미리보기
st.dataframe(load_weather_data().head())
st.dataframe(load_disaster_data().head())
