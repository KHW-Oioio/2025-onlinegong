import streamlit as st, matplotlib.pyplot as plt, seaborn as sns, folium


def hist(data,title):
    fig,ax=plt.subplots(); ax.hist(data,bins=30,color="steelblue",edgecolor="black");
    ax.set_title(title); ax.set_xlabel("Damage (억원)"); ax.set_ylabel("Freq"); st.pyplot(fig)

def heat(df,title):
    fig,ax=plt.subplots(); sns.heatmap(df.corr(),annot=True,fmt=".2f",cmap="YlOrRd",ax=ax);
    ax.set_title(title); st.pyplot(fig)

def pie(series,title):
    fig,ax=plt.subplots(); ax.pie(series,labels=series.index,autopct="%1.1f%%"); ax.set_title(title); st.pyplot(fig)

def fmap(series,coords):
    center=[sum(x for x,_ in coords.values())/len(coords), sum(y for _,y in coords.values())/len(coords)]
    mp=folium.Map(center,zoom_start=6,tiles="cartodbpositron")
    mx=series.max()
    for reg,val in series.items():
        lat,lon=coords[reg]; folium.CircleMarker([lat,lon],radius=5+20*val/mx,color="red",fill=True,fill_opacity=0.6,
        popup=f"{reg}: {val:.2f}억").add_to(mp)
    st.components.v1.html(mp._repr_html_(),height=500)
