import os, streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt

# 데이터 경로 설정 (현재 파일 기준 ../data 폴더 내 csv)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
WEATHER_CSV  = os.path.join(DATA_DIR, "weather_data.csv")
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")

# CSV 데이터 로드
weather_df  = pd.read_csv(WEATHER_CSV)
disaster_df = pd.read_csv(DISASTER_CSV)

# 국가 리스트 생성
COUNTRY_LIST = weather_df["country"].unique().tolist()

st.title("🔬 변수 상관관계 분석")

country = st.selectbox("국가", COUNTRY_LIST)

# 선택 국가 데이터 필터링
cw = weather_df[weather_df["country"] == country]
cd = disaster_df[disaster_df["country"] == country]

# 년도, 국가 기준으로 병합
merged = pd.merge(cw, cd, on=["country","year"])

# 관심 변수 상관계수 계산
corr = merged[["avg_temp","precip","damage"]].corr()

# 상관계수 히트맵 시각화
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title(f"{country} – Temp/Precip/Damage Correlation")
st.pyplot(fig)
