# data_loader.py
import os
import pandas as pd

# 데이터 폴더 경로 설정
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 파일 경로 설정
WEATHER_PATH = os.path.join(DATA_DIR, "weather.csv")
DISASTER_PATH = os.path.join(DATA_DIR, "disaster.csv")

# 날씨 데이터 불러오기
if os.path.exists(WEATHER_PATH):
    try:
        weather_df = pd.read_csv(WEATHER_PATH, parse_dates=["date"])
    except Exception as e:
        print(f"[오류] weather.csv 로딩 실패: {e}")
        weather_df = pd.DataFrame()
else:
    print(f"[경고] {WEATHER_PATH} 파일이 존재하지 않습니다.")
    weather_df = pd.DataFrame()

# 재난 피해 데이터 불러오기
if os.path.exists(DISASTER_PATH):
    try:
        disaster_df = pd.read_csv(DISASTER_PATH)
        disaster_df.columns = disaster_df.columns.str.strip().str.lower()
    except Exception as e:
        print(f"[오류] disaster.csv 로딩 실패: {e}")
        disaster_df = pd.DataFrame()
else:
    print(f"[경고] {DISASTER_PATH} 파일이 존재하지 않습니다.")
    disaster_df = pd.DataFrame()
