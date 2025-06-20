import os, streamlit as st, pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt

# 데이터 경로 설정 및 CSV 로드
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
WEATHER_CSV  = os.path.join(DATA_DIR, "weather_data.csv")
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")

weather_df  = pd.read_csv(WEATHER_CSV)
disaster_df = pd.read_csv(DISASTER_CSV)

COUNTRY_LIST = weather_df["country"].unique().tolist()

st.title("🌡️ SDGs‑13 8개국의 기후 리스크 점수 자동 계산")

# 1. 지표 정규화 (min-max scaling)
metrics = []
for c in COUNTRY_LIST:
    cw = weather_df[weather_df["country"] == c]
    cd = disaster_df[disaster_df["country"] == c]
    temp = cw["avg_temp"].mean()
    precip = cw["precip"].mean()
    damage = cd["damage"].mean()
    metrics.append({"country": c, "temp": temp, "precip": precip, "damage": damage})

df = pd.DataFrame(metrics).set_index("country")
norm = (df - df.min()) / (df.max() - df.min())

weights = {"temp": 0.4, "precip": 0.2, "damage": 0.4}
score = (norm * pd.Series(weights)).sum(axis=1).sort_values(ascending=False)

st.subheader("📊 Risk Scores by Country")
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=score.values, y=score.index, ax=ax, palette="Reds_r")
ax.set_xlabel("Risk Score (0 to 1)")
ax.set_ylabel("")
ax.set_title("Climate & Disaster Risk Score by Country")
st.pyplot(fig)

st.markdown("""
**Risk Score Formula:**  
- Risk Score = 0.4 × Normalized Temperature + 0.2 × Normalized Precipitation + 0.4 × Normalized Disaster Damage  
- 각 지표는 국가별 평균값에 대해 0~1 범위로 정규화하였으며, 가중치는 임의로 설정했습니다.  
""")
