# 기후 변수 ↔ 피해액 상관 분석
import os, sys, streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
WEATHER_CSV  = os.path.join(DATA_DIR, "weather_data.csv")
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")

weather_df  = pd.read_csv(WEATHER_CSV)
disaster_df = pd.read_csv(DISASTER_CSV)

COUNTRY_LIST = weather_df["country"].unique().tolist()
st.title("🔬 변수 상관관계 분석")

country = st.selectbox("국가", COUNTRY_LIST)
w = load_weather_data()
d = load_disaster_data()

cw = w[w["country"] == country]
cd = d[d["country"] == country]

merged = pd.merge(cw, cd, on=["country","year"])
corr = merged[["avg_temp","precip","damage"]].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title(f"{country} – Temp/Precip/Damage Correlation")
st.pyplot(fig)
