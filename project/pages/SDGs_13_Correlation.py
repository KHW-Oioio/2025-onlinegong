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

st.markdown("""
**용어 설명:**  
- **avg_temp**: 해당 연도 평균 기온 (°C)  
- **precip**: 연간 강수량 (mm)  
- **damage**: 재난으로 인한 피해액 (억원)  

**상관계수 값의 의미:**  
- **1**: 완전한 양의 상관관계 (두 변수는 함께 증가)  
- **0**: 상관관계 없음 (두 변수는 서로 관련 없음)  
- **-1**: 완전한 음의 상관관계 (한 변수가 증가하면 다른 변수는 감소)  
""")
