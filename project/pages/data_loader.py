import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def load_weather_data():
    path = os.path.join(DATA_DIR, "weather.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"⚠️ weather.csv 파일이 {path}에 없습니다.")
    try:
        return pd.read_csv(path, parse_dates=["date"])
    except pd.errors.EmptyDataError:
        raise ValueError("⚠️ weather.csv가 비어 있습니다.")

def load_disaster_data():
    path = os.path.join(DATA_DIR, "disaster.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"⚠️ disaster.csv 파일이 {path}에 없습니다.")
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except pd.errors.EmptyDataError:
        raise ValueError("⚠️ disaster.csv가 비어 있습니다.")
