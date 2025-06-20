# ────────────────────────────────────────────────
# pages/SDGs_13.py   –   완전 자급자족(All‑in‑One) 버전
# ────────────────────────────────────────────────
import os, streamlit as st, pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns

# 1. CSV 로드 (data 폴더는 project/data 에 위치)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
WEATHER_CSV  = os.path.join(DATA_DIR, "weather_data.csv")
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")

weather_df  = pd.read_csv(WEATHER_CSV)
disaster_df = pd.read_csv(DISASTER_CSV)

COUNTRY_LIST = weather_df["country"].unique().tolist()

# 2. 페이지 UI
st.title("🌍 SDGs‑13 주요8개국 weather , disaster 분석 대쉬보드 ")

country = st.selectbox("분석할 국가 선택:", COUNTRY_LIST)

# 3. 기후 시각화
ct_weather  = weather_df[weather_df["country"] == country]
st.subheader(f"📈 {country} – 기후 변화 (2018‑2022)")

fig, ax1 = plt.subplots(figsize=(10,5))
ax1.set_xlabel("Year")
ax1.set_ylabel("Avg Temp (°C)", color="tab:red")
ax1.plot(ct_weather["year"], ct_weather["avg_temp"], marker="o", color="tab:red")
ax2 = ax1.twinx()
ax2.set_ylabel("Precip (mm)", color="tab:blue")
ax2.bar(ct_weather["year"], ct_weather["precip"], alpha=0.3, color="tab:blue")
plt.title(f"{country} – Temperature & Precipitation")
st.pyplot(fig)

# 4. 국가별 재난 피해 파이차트
st.subheader("💥 국가별 누적 재난 피해 비율")
agg = disaster_df.groupby("country")["damage"].sum()
fig2, ax = plt.subplots()
ax.pie(agg, labels=agg.index, autopct="%1.1f%%", startangle=140)
ax.set_title("전체 피해액 기준 비율")
st.pyplot(fig2)

# 5. 몬테카를로 시뮬레이션 설명
st.markdown("""### 🎲 몬테카를로 시뮬레이션 설명
몬테카를로 시뮬레이션은 확률 분포를 바탕으로 **불확실성을 정량화**하는 기법입니다.  
여기서는 정책 개입(인프라 개선, 경보 시스템 향상 등)이 재난 피해액을 얼마나 줄이는지 **1000회 난수 실험**으로 추정합니다.
""")

# 6. 시뮬레이션 실행
ct_disaster = disaster_df[disaster_df["country"] == country]
base_damage = ct_disaster["damage"].mean()

policy = st.slider("정책 효과 (0 ~ 0.5)", 0.0, 0.5, 0.1, 0.01)
runs   = st.slider("시뮬레이션 횟수", 500, 5000, 1000, 500)

np.random.seed(42)
factors = np.random.normal(loc=1-policy, scale=0.05, size=runs)  # 정책으로 평균 감소
results = np.maximum(base_damage * factors, 0)

# 7. 결과 히스토그램
st.subheader(f"결과 분포 – 평균 피해 {results.mean():.1f} 억원")
fig3, ax3 = plt.subplots()
sns.histplot(results, kde=True, color="purple", ax=ax3)
ax3.set_xlabel("예상 피해액 (억원)")
ax3.set_ylabel("빈도")
st.pyplot(fig3)

st.success(f"✔️ 시나리오 평균 피해: {results.mean():,.1f} 억원 / 최소 {results.min():.1f} ~ 최대 {results.max():.1f}")
st.caption("데이터: /data/weather_data.csv, /data/disaster_data.csv (주요 8개국, 2018‑2022)")
