import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_weather(df, country):
    st.subheader(f"📈 {country} - 연도별 기온 및 강수량 변화")
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel("연도")
    ax1.set_ylabel("평균 기온 (°C)", color="tab:red")
    ax1.plot(df["year"], df["avg_temp"], color="tab:red", label="평균 기온")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("연 강수량 (mm)", color="tab:blue")
    ax2.bar(df["year"], df["precip"], alpha=0.3, color="tab:blue", label="강수량")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    plt.title(f"{country}의 기후 변화 추이")
    st.pyplot(fig)

def plot_disaster_pie(df):
    st.subheader("🌪️ 국가별 재난 피해 비율")
    agg = df.groupby("country")["damage"].sum()
    fig, ax = plt.subplots()
    ax.pie(agg, labels=agg.index, autopct="%1.1f%%", startangle=140)
    ax.set_title("전체 피해액 기준 비율")
    st.pyplot(fig)

def plot_monte_carlo(results):
    st.subheader("🎲 몬테카를로 시뮬레이션 결과 분포")
    fig, ax = plt.subplots()
    sns.histplot(results, kde=True, color="purple")
    ax.set_xlabel("예상 피해액 (억원)")
    ax.set_ylabel("시뮬레이션 횟수")
    ax.set_title("정책 시행 후 피해 예측 분포")
    st.pyplot(fig)

