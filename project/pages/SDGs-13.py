# ✅ SDGs_13.py (Streamlit Cloud용, pages 폴더에 위치할 때)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pages.data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs‑13 시뮬레이션", layout="wide")
st.title("🔥 기후 변화에 따른 재난 피해 예측 시뮬레이션")

# 데이터 불러오기
weather = load_weather_data()
disaster = load_disaster_data()

st.subheader("📊 기온 및 강수량 시각화")
region = st.selectbox("지역을 선택하세요", weather.columns.drop("date"))

fig, ax1 = plt.subplots(figsize=(10, 4))
ax2 = ax1.twinx()
ax1.plot(weather["date"], weather[region], color="tab:blue", label="온도")
ax2.plot(weather["date"], weather[region]*0.1, color="tab:green", alpha=0.3, label="강수량(가정)")
ax1.set_xlabel("날짜")
ax1.set_ylabel("온도(℃)")
ax2.set_ylabel("강수량(mm)")
fig.tight_layout()
st.pyplot(fig)

st.subheader("📉 과거 재난 피해 통계")
if "region" in disaster.columns:
    region_list = disaster["region"].unique().tolist()
    selected = st.selectbox("재난 통계 지역 선택", region_list)
    filtered = disaster[disaster["region"] == selected]
    st.write(filtered.groupby("year")["damage_amount_hundred_million_won"].sum().reset_index())
else:
    st.warning("disaster.csv에 'region' 컬럼이 존재하지 않습니다. 컬럼명을 확인해주세요.")

st.markdown("---")
st.markdown("시뮬레이션 및 예측 분석은 추후 구현 예정입니다.")
