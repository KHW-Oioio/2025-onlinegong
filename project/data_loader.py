# data_loader.py
import os, requests, pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = "data"; os.makedirs(DATA_DIR, exist_ok=True)

# ---------- 실제 기상 데이터(Open‑Meteo) ----------
REGION_COORDS = {
    "RegionA": (37.5665, 126.9780),
    "RegionB": (35.1796, 129.0756),
    "RegionC": (35.8714, 128.6014),
}

def _fetch_weather(region, start, end):
    lat, lon = REGION_COORDS[region]
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        "&daily=temperature_2m_mean,precipitation_sum,windspeed_10m_max"
        "&timezone=Asia%2FSeoul"
    )
    j = requests.get(url, timeout=30).json()
    return pd.DataFrame({
        "date": j["daily"]["time"],
        f"{region}_temp": j["daily"]["temperature_2m_mean"],
        f"{region}_precip": j["daily"]["precipitation_sum"],
        f"{region}_wind": j["daily"]["windspeed_10m_max"],
    })

def build_weather_csv(start="2022-01-01", end="2022-12-31"):
    dfs = [_fetch_weather(r, start, end) for r in REGION_COORDS]
    out = dfs[0]
    for df in dfs[1:]:
        out = out.merge(df, on="date")
    out.to_csv(f"{DATA_DIR}/weather.csv", index=False)
    return out

# ---------- 재난 피해 데이터(샘플 CSV 생성) ----------
def _create_dummy_disaster():
    csv = """year,region,damage_amount_hundred_million_won,deaths
2020,RegionA,1.5,2
2021,RegionB,0.8,0
2022,RegionC,2.1,1
2022,RegionA,1.2,0
"""
    with open(f"{DATA_DIR}/disaster.csv", "w", encoding="utf-8") as f:
        f.write(csv)

# ---------- 로딩 함수 (Streamlit 캐시 X) ----------
def load_weather_data():
    path = f"{DATA_DIR}/weather.csv"
    if not os.path.exists(path):
        build_weather_csv()
    return pd.read_csv(path, parse_dates=["date"])

def load_disaster_data():
    path = f"{DATA_DIR}/disaster.csv"
    if not os.path.exists(path):
        _create_dummy_disaster()
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df

