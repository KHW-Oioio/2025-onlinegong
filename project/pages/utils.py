import matplotlib.pyplot as plt, seaborn as sns, folium, streamlit as st

# 히스토그램
def plot_histogram(data, title):
    fig, ax = plt.subplots(); ax.hist(data, bins=30, color="skyblue", edgecolor="black")
    ax.set_title(title); ax.set_xlabel("예측 피해액(억)"); ax.set_ylabel("빈도")
    st.pyplot(fig)

# 상관 Heatmap
def plot_correlation(df, title):
    fig, ax = plt.subplots(); sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="YlOrBr", ax=ax)
    ax.set_title(title); st.pyplot(fig)

# 파이차트
def plot_pie(series, title):
    fig, ax = plt.subplots(); ax.pie(series, labels=series.index, autopct="%1.1f%%", startangle=90)
    ax.set_title(title); st.pyplot(fig)

# 피해 지도
def make_damage_map(series, coords):
    center = [sum(lat for lat, _ in coords.values())/len(coords),
              sum(lon for _, lon in coords.values())/len(coords)]
    m = folium.Map(location=center, zoom_start=6, tiles="cartodbpositron")
    max_dmg = series.max()
    for reg, dmg in series.items():
        lat, lon = coords[reg]
        folium.CircleMarker([lat, lon], radius=5+20*dmg/max_dmg,
                            popup=f"{reg}: {dmg:.2f}억", color="red", fill=True, fill_opacity=0.6).add_to(m)
    st.components.v1.html(m._repr_html_(), height=500)
