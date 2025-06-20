# 기후 변수 ↔ 피해액 상관 분석
import os, sys, streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_loader import load_weather_data, load_disaster_data, COUNTRY_LIST

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
