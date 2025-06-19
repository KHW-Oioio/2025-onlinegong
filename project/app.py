# ✅ app.py
import os, sys, streamlit as st

# 🔧 루트 경로 및 pages 경로를 모듈 탐색 경로에 추가
ROOT_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(ROOT_DIR, "pages")

for path in [ROOT_DIR, PAGES_DIR]:
    if path not in sys.path:
        sys.path.append(path)

from data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs‑13 기후 피해 예측", layout="wide")
st.title("🌍 SDGs‑13 기후 변화 피해 분석 대시보드")
st.markdown("사이드바 메뉴에서 'SDGs‑13' 페이지를 눌러 시뮬레이션을 실행하세요.")

