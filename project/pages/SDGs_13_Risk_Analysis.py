# 국가별 리스크 점수 산출 페이지
import os, sys, streamlit as st, pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_loader import load_weather_data, load_disaster_data, COUNTRY_LIST

st.title("🌡️ SDGs‑13 Risk Score Analysis")

wdf = load_weather_data()
ddf = load_disaster_data()

# 1. 지표 정규화 (min‑max)
metrics = []
for c in COUNTRY_LIST:
    cw = wdf[wdf["country"] == c]
    cd = ddf[ddf["country"] == c]
    temp = cw["avg_temp"].mean()
    precip = cw["precip"].mean()
    damage = cd["damage"].mean()
    metrics.append({"country": c, "temp": temp, "precip": precip, "damage": damage})

df = pd.DataFrame(metrics).set_index("country")
norm = (df - df.min()) / (df.max() - df.min())
weights = {"temp": 0.4, "precip": 0.2, "damage": 0.4}
score = (norm * pd.Series(weights)).sum(axis=1).sort_values(ascending=False)

st.subheader("📊 국가별 기후 리스크 점수")
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=score.values, y=score.index, ax=ax, palette="Reds_r")
ax.set_xlabel("Risk Score (0~1)")
ax.set_ylabel("")
st.pyplot(fig)

st.caption("Risk Score = 0.4✕Temp Z + 0.2✕Precip Z + 0.4✕Damage Z")
