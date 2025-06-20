import pandas as pd
import os

def load_weather_data():
    path = os.path.join("data", "weather_data.csv")
    return pd.read_csv(path)

def load_disaster_data():
    path = os.path.join("data", "disaster_data.csv")
    return pd.read_csv(path)

COUNTRY_LIST = [
    "United States", "China", "India", "Germany", "South Korea",
    "Japan", "France", "Brazil"
]
