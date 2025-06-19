import os, requests, pandas as pd
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 좌표 사전 (예시)
REGION_COORDS = {
    "RegionA": (37.5665, 126.9780),  # 서울
    "RegionB": (35.1796, 129.0756),  # 부산
    "RegionC": (35.8714, 128.6014),  # 대구
}

# ───────────────────────── 기상 데이터 (Open‑Meteo) ─────────────────────────

def _fetch_weather_openmeteo(region:str, start:str, end:str):
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
        f"{region}_temp":   j["daily"]["temperature_2m_mean"],
        f"{region}_precip": j["daily"]["precipitation_sum"],
        f"{region}_wind":   j["daily"]["windspeed_10m_max"],
    })

def _build_weather_csv(start="2022-01-01", end="2022-12-31"):
    merged = None
    for r in REGION_COORDS:
        df = _fetch_weather_openmeteo(r, start, end)
        merged = df if merged is None else merged.merge(df, on="date")
    merged.to_csv(os.path.join(DATA_DIR, "weather.csv"), index=False)
    return merged

# ───────────────────────── 재난 데이터 (샘플 CSV) ─────────────────────────

def _create_dummy_disaster():
    csv = """year,region,damage_amount_hundred_million_won,deaths
2020,RegionA,1.5,2
2021,RegionB,0.8,0
2022,RegionC,2.1,1
2022,RegionA,1.2,0
"""
    with open(os.path.join(DATA_DIR, "disaster.csv"), "w", encoding="utf-8") as f:
        f.write(csv)

# ───────────────────────── 공개 API 호출 → CSV 로컬 저장 ─────────────────────────

def load_weather_data():
    path = os.path.join(DATA_DIR, "weather.csv")
    if not os.path.exists(path):
        _build_weather_csv()
    return pd.read_csv(path, parse_dates=["date"])


def load_disaster_data():
    path = os.path.join(DATA_DIR, "disaster.csv")
    if not os.path.exists(path):
        _create_dummy_disaster()
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df
```
