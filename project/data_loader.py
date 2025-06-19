# data_loader.py (함수 제거하고 직접 불러오는 버전)
import os
import pandas as pd

DATA_DIR = "data"
WEATHER_PATH = os.path.join(DATA_DIR, "weather.csv")
DISASTER_PATH = os.path.join(DATA_DIR, "disaster.csv")

# 날씨 데이터 불러오기
if os.path.exists(WEATHER_PATH):
    weather_df = pd.read_csv(WEATHER_PATH, parse_dates=["date"])
else:
    print(f"[경고] {WEATHER_PATH} 파일이 존재하지 않습니다.")
    weather_df = pd.DataFrame()  # 빈 데이터프레임 반환

# 재난 피해 데이터 불러오기
if os.path.exists(DISASTER_PATH):
    disaster_df = pd.read_csv(DISASTER_PATH)
    disaster_df.columns = disaster_df.columns.str.strip().str.lower()
else:
    print(f"[경고] {DISASTER_PATH} 파일이 존재하지 않습니다.")
    disaster_df = pd.DataFrame()
