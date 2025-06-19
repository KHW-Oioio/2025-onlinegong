import matplotlib.pyplot as plt, seaborn as sns, folium, streamlit as st
import pandas as pd

# -------- 일반 차트 ----------------------------------------
def plot_histogram(data, title):
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, color="skyblue", edgecolor="black")
    ax.set_title(title); ax.set_xlabel("예측 피해액(억)"); ax.set_ylabel("빈도")
    st.pyplot(fig)

def plot_correlation(df, title):
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="YlOrBr", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

def plot_pie(series, title):
    fig, ax = plt.subplots()
    ax.pie(series, labels=series.index, autopct="%1.1f%%", startangle=90)
    ax.set_title(title); st.pyplot(fig)

# -------- 지도 시각화 --------------------------------------
def make_damage_map(damage_series, region_coords, title):
    center_lat = sum(lat for lat, _ in region_coords.values())/len(region_coords)
    center_lon = sum(lon for _, lon in region_coords.values())/len(region_coords)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="cartodbpositron")
    max_dmg = damage_series.max()

    for region, dmg in damage_series.items():
        lat, lon = region_coords[region]
        folium.CircleMarker(
            location=[lat, lon],
            radius=5 + 20*dmg/max_dmg,
            popup=f"{region}: {dmg:.2f} 억",
            color="red",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
    st.components.v1.html(m._repr_html_(), height=500)
