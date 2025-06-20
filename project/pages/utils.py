import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
import pandas as pd

def plot_temperature_trend(df, country):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df[country], label=f"{country} 평균기온", color="orange")
    ax.set_xlabel("날짜")
    ax.set_ylabel("온도 (°C)")
    ax.set_title(f"📈 {country} 일별 기온 추세")
    ax.legend()
    st.pyplot(fig)

def plot_correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("🌡️ 국가 간 기온 상관관계")
    st.pyplot(fig)

def plot_disaster_bar(df):
    grouped = df.groupby(["region", "disaster_type"])["damage_amount_hundred_million_won"].sum().unstack().fillna(0)
    st.bar_chart(grouped)

def plot_pie_by_region(df, year):
    filtered = df[df["year"] == year]
    data = filtered.groupby("region")["damage_amount_hundred_million_won"].sum()
    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct="%1.1f%%", startangle=140)
    ax.set_title(f"🌍 {year}년 국가별 피해 비율")
    st.pyplot(fig)
