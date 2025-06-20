# 정책 시나리오별 피해 감소 시뮬레이터
import os, sys, streamlit as st, numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_loader import load_disaster_data, COUNTRY_LIST
from model import run_monte_carlo

st.title("🏛️ 정책 시나리오 시뮬레이션")

policy_options = {
    "A안 - 경보 시스템 강화": 0.15,
    "B안 - 하천 정비": 0.25,
    "C안 - 인프라 내진": 0.35
}

country = st.selectbox("국가 선택", COUNTRY_LIST)
policy_name = st.radio("정책 선택", list(policy_options.keys()))
effect = policy_options[policy_name]
runs = st.slider("반복 횟수", 500, 5000, 1000, 500)

df = load_disaster_data()
base = df[df["country"] == country]["damage"].mean()

results = run_monte_carlo(base, policy_effectiveness=effect, simulations=runs)

st.markdown(f"**{policy_name}** 적용 시 평균 피해: **{np.mean(results):,.1f} 억원**")
fig, ax = plt.subplots()
sns.histplot(results, kde=True, ax=ax, color="teal")
ax.set_xlabel("예상 피해액(억원)"); ax.set_ylabel("빈도")
st.pyplot(fig)
