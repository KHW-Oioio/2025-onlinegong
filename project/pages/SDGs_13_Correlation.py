import os, streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
WEATHER_CSV  = os.path.join(DATA_DIR, "weather_data.csv")
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")

weather_df  = pd.read_csv(WEATHER_CSV)
disaster_df = pd.read_csv(DISASTER_CSV)
COUNTRY_LIST = weather_df["country"].unique().tolist()

st.title("🔬 변수 상관관계 분석")

country = st.selectbox("국가", COUNTRY_LIST)
cw = weather_df[weather_df["country"] == country]
cd = disaster_df[disaster_df["country"] == country]
merged = pd.merge(cw, cd, on=["country","year"])

corr = merged[["avg_temp","precip","damage"]].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title(f"{country} – Temp/Precip/Damage Correlation")
st.pyplot(fig)

# 축 및 주요 용어 설명 추가
st.markdown("""
**용어 설명:**  
- **avg_temp**: 해당 연도 평균 기온 (°C)  
- **precip**: 연간 강수량 (mm)  
- **damage**: 재난으로 인한 피해액 (억원)  
""")
