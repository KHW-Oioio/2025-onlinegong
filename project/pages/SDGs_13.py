import streamlit as st
from data_loader import load_weather_data, load_disaster_data, COUNTRY_LIST
from model import run_monte_carlo
from utils import plot_weather, plot_disaster_pie, plot_monte_carlo

st.title("🌱 SDGs-13: 기후 변화 & 재난 피해 분석")

country = st.selectbox("분석할 국가를 선택하세요:", COUNTRY_LIST)

weather_df = load_weather_data()
disaster_df = load_disaster_data()

country_weather = weather_df[weather_df["country"] == country]
country_disaster = disaster_df[disaster_df["country"] == country]

st.markdown("## ☁️ 기후 데이터 시각화")
plot_weather(country_weather, country)

st.markdown("## 💥 재난 피해 현황")
plot_disaster_pie(disaster_df)

st.markdown("## 🎲 몬테카를로 시뮬레이션 설명")
st.info(
    """
    몬테카를로 시뮬레이션은 확률 분포를 바탕으로 불확실한 상황을 수천 번 반복 실험하여 평균적인 예측 결과를 도출하는 방법입니다.  
    아래의 시뮬레이션은 재난 피해에 대한 정책적 개입(예: 인프라 개선, 경보 시스템 강화 등)이 평균 피해액에 미치는 영향을 시뮬레이션합니다.
    """
)

base_damage = country_disaster["damage"].mean()
effectiveness = st.slider("정책 개입 효과 (0.0~0.5)", 0.0, 0.5, 0.1, step=0.01)

results = run_monte_carlo(base_damage, policy_effectiveness=effectiveness)
plot_monte_carlo(results)

st.success(f"✔️ 평균 예상 피해액: {round(sum(results)/len(results), 2)} 억원")
