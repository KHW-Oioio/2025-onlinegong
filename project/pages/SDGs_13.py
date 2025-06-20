import streamlit as st, pandas as pd
from pages.data_loader import load_weather_data, load_disaster_data, REGION_COORDS
from pages.model import run_mc, build_graph
from pages.utils import hist, heat, pie, fmap

st.header("🛰️ SDGs‑13 Climate‑Disaster Simulator")

weather=load_weather_data(); disaster=load_disaster_data()
regions=sorted({c.split("_")[0] for c in weather.columns if "_temp" in c})

r=st.sidebar.selectbox("지역",regions)
policy=st.sidebar.slider("감축률(%)",0,100,20)
mean_t=st.sidebar.slider("예상 기온 상승(°C)",1.0,4.0,2.0,0.1)
std_t=st.sidebar.slider("온도 표준편차",0.1,1.0,0.3,0.1)
its=st.sidebar.number_input("반복 횟수",1000,10000,2000,500)

mask=disaster["region"].str.contains(r,case=False,na=False)
base=float(disaster.loc[mask,"damage_amount_hundred_million_won"].mean() or 0)

temp=weather[f"{r}_temp"].dropna()
prec=weather[f"{r}_precip"].dropna(); wind=weather[f"{r}_wind"].dropna()

if st.button("▶ 시뮬레이션"):
    dmg=run_mc(base,mean_t,std_t,prec,wind,policy/100,its)
    st.success(f"평균 피해액: {dmg.mean():.2f}억 (n={its})")
    hist(dmg,"Monte‑Carlo 결과 분포")
    heat(pd.DataFrame({"temp":temp,"prec":prec,"wind":wind}).dropna(),"기상 변수 상관관계")
    pie(disaster.groupby("region")['damage_amount_hundred_million_won'].sum(),"지역별 누적 피해")
    fmap(disaster.groupby("region")['damage_amount_hundred_million_won'].mean(),REGION_COORDS)
    G=build_graph(REGION_COORDS.keys()); st.info(f"그래프 노드:{list(G.nodes())} 엣지:{list(G.edges())}")
