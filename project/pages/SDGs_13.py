# ────────────────────────────────────────────────
# pages/SDGs_13.py  ―  Streamlit Cloud 경로 오류 해결 버전
# ────────────────────────────────────────────────
import os, sys, streamlit as st
import pandas as pd

# 1️⃣  부모 디렉터리(project/)를 모듈 경로에 추가
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

# 2️⃣  이제 루트에 있는 모듈을 정상 import
from data_loader import load_weather_data, load_disaster_data, COUNTRY_LIST
from model import run_monte_carlo
from utils import plot_weather, plot_disaster_pie, plot_monte_carlo

# ────────────────────────────────────────────────
# 대시보드 시작
# ────────────────────────────────────────────────
st.title("🌱 SDGs‑13 기후 변화 & 재난 피해 분석")

country = st.selectbox("분석할 국가를 선택하세요:", COUNTRY_LIST)

weather_df  = load_weather_data()
disaster_df = load_disaster_data()

country_weather  = weather_df[weather_df["country"] == country]
country_disaster = disaster_df[disaster_df["country"] == country]

st.markdown("## ☁️ 기후 데이터 시각화")
plot_weather(country_weather, country)

st.markdown("## 💥 재난 피해 현황")
plot_disaster_pie(disaster_df)

st.markdown("## 🎲 몬테카를로 시뮬레이션 설명")
st.info(
    """
    **몬테카를로 시뮬레이션**은 확률 분포를 이용해 불확실한 상황을 수천 번 반복 실험하여
    평균적인 예측 결과를 얻는 방법입니다.
    여기서는 정책 개입 효과(인프라 개선, 경보 시스템 강화 등)가
    재난 피해를 얼마나 줄이는지 가상 실험합니다.
    """
)

base_damage  = country_disaster["damage"].mean()
effectiveness = st.slider("정책 개입 효과 (0.0 ~ 0.5)", 0.0, 0.5, 0.1, step=0.01)

results = run_monte_carlo(base_damage, policy_effectiveness=effectiveness)
plot_monte_carlo(results)

st.success(f"✔️ 평균 예상 피해액: {round(pd.Series(results).mean(), 2)} 억원")
st.caption("Data source: csv files in /data (8 major countries, 2018‑2022)")
