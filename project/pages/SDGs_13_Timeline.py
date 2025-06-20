import os, streamlit as st, plotly.express as px, pandas as pd

# 데이터 경로 설정 및 CSV 로드
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")
disaster_df = pd.read_csv(DISASTER_CSV)

st.title("⏰ 글로벌 재난 피해 타임라인")

fig = px.line(
    disaster_df, x="year", y="damage", color="country",
    title="Yearly Disaster Damage by Country (2018‑2022)",
    labels={"damage": "Damage (billion KRW)", "year": "Year"}
)
st.plotly_chart(fig, use_container_width=True)
