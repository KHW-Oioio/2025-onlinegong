import os, sys, streamlit as st

# 현재 디렉토리를 sys.path에 추가하여 모듈을 인식하도록 설정
CURRENT_DIR = os.path.dirname(__file__)
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs‑13 기후 피해 예측", layout="wide")
st.title("🌍 SDGs‑13 기후 변화 피해 분석 대시보드")
st.markdown("사이드바 메뉴에서 'SDGs‑13' 페이지를 눌러 시뮬레이션을 실행하세요.")

# 데이터 미리보기
st.header("🔎 데이터 미리보기")
st.dataframe(load_weather_data().head())
st.dataframe(load_disaster_data().head())

