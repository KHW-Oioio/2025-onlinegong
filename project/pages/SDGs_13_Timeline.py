# 재난 타임라인 애니메이션 (Plotly)
import os, sys, streamlit as st, plotly.express as px, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_loader import load_disaster_data

st.title("⏰ 글로벌 재난 피해 타임라인")

ddf = load_disaster_data()
fig = px.line(
    ddf, x="year", y="damage", color="country",
    title="연도별 국가별 피해액 추이 (2018‑2022)",
    labels={"damage":"Damage (억원)", "year":"Year"}
)
st.plotly_chart(fig, use_container_width=True)
