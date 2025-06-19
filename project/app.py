# app.py
import os, sys

# 현재 디렉터리를 모듈 경로에 추가
CURRENT_DIR = os.path.dirname(__file__)
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

import streamlit as st
from data_loader import weather_df, disaster_df  # 함수가 아니라 직접 변수 import

st.set_page_config(page_title="SDGs13 기후 피해 예측", layout="wide")

st.title("🌏 SDGs‑13 기후 변화 피해 분석 대시보드")
st.markdown("사이드바에서 분석 페이지를 선택하세요.")
st.write("데이터 및 CSV 파일 로딩 중…")

# 미리보기 출력
if not weather_df.empty:
    st.subheader("📊 기상 데이터 미리보기")
    st.dataframe(weather_df.head())
else:
    st.warning("weather.csv 파일이 없거나 데이터가 비어 있습니다.")

if not disaster_df.empty:
    st.subheader("📊 재난 피해 데이터 미리보기")
    st.dataframe(disaster_df.head())
else:
    st.warning("disaster.csv 파일이 없거나 데이터가 비어 있습니다.")
