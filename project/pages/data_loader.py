# pages/data_loader.py

import os
import pandas as pd

# 🔧 project/data 경로를 절대경로로 지정
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))  # pages/의 부모 = project/
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def load_weather_data():
    path = os.path.join(DATA_DIR, "weather.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"⚠️ weather.csv 파일이 {path} 경로에 존재하지 않습니다.")
    return pd.read_csv(path, parse_dates=["date"])

def load_disaster_data():
    path = os.path.join(DATA_DIR, "disaster.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"⚠️ disaster.csv 파일이 {path} 경로에 존재하지 않습니다.")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df
