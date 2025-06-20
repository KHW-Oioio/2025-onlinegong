import streamlit as st, matplotlib.pyplot as plt, seaborn as sns, folium

def hist(x,title):
    fig,ax=plt.subplots(); ax.hist(x,bins=30,color="steelblue",edgecolor="k"); ax.set_title(title); st.pyplot(fig)

def heat(df,title):
    fig,ax=plt.subplots(); sns.heatmap(df.corr(),annot=True,fmt=".2f",cmap="YlOrRd",ax=ax); ax.set_title(title); st.pyplot(fig)

def pie(series,title):
    fig,ax=plt.subplots(); ax.pie(series,labels=series.index,autopct="%1.1f%%"); ax.set_title

