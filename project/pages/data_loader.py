import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_weather_data():
    path = os.path.join(DATA_DIR, "weather_data.csv")
    df = pd.read_csv(path)        # ⬅️ parse_dates 삭제
    # 연도 → 날짜(datetime) 컬럼 추가(옵션)
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01")
    return df

def load_disaster_data():
    path = os.path.join(DATA_DIR, "disaster_data.csv")
    return pd.read_csv(path)

COUNTRY_LIST = [
    "United States", "China", "India", "Germany",
    "South Korea", "Japan", "France", "Brazil"
]

