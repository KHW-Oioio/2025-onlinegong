import os, requests, json, pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# project/data directory (one level up from pages)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------------------------------------------------
# 1. Real WEATHER data via Open‑Meteo archive (free & key‑less)
#    3 demo regions with coords; easy to add more.
# ------------------------------------------------------------
REGION_COORDS = {
    "Seoul":   (37.5665, 126.9780),
    "Busan":   (35.1796, 129.0756),
    "Daegu":   (35.8714, 128.6014),
}

ARCHIVE_START = "2023-01-01"
ARCHIVE_END   = "2023-12-31"

def _fetch_region_weather(region:str):
    lat, lon = REGION_COORDS[region]
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={ARCHIVE_START}&end_date={ARCHIVE_END}"
        "&daily=temperature_2m_mean,precipitation_sum,windspeed_10m_max"
        "&timezone=Asia%2FSeoul"
    )
    r = requests.get(url, timeout=30)
    ds = r.json()["daily"]
    return pd.DataFrame({
        "date": ds["time"],
        f"{region}_temp":   ds["temperature_2m_mean"],
        f"{region}_precip": ds["precipitation_sum"],
        f"{region}_wind":   ds["windspeed_10m_max"],
    })

def _build_weather_csv():
    dfs = [_fetch_region_weather(r) for r in REGION_COORDS]
    df = dfs[0]
    for d in dfs[1:]:
        df = df.merge(d, on="date")
    df.to_csv(os.path.join(DATA_DIR, "weather.csv"), index=False)
    return df

# ------------------------------------------------------------
# 2. Real DISASTER stats: try UNDRR GAR API (public, no auth)   
#    Fallback to internal demo CSV if API fails.
# ------------------------------------------------------------

def _fetch_disaster_undrr():
    # GAR API: https://risk-informed-dev.github.io/gar-api/
    # We'll pull Korea (410) summary for 2000‑2023.
    try:
        url = "https://garapi.globalgarhub.org/v1/risks/iso/KOR"
        recs = requests.get(url, timeout=30).json()["records"]
        rows = []
        for r in recs:
            rows.append({
                "year": r["year"],
                "region": "Korea",
                "damage_amount_hundred_million_won": r.get("economic_loss_avg", 0)/1e8,
                "deaths": r.get("mortality_avg", 0),
            })
        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(DATA_DIR, "disaster.csv"), index=False)
        return df
    except Exception:
        return None

def _build_demo_disaster_csv():
    demo = """year,region,damage_amount_hundred_million_won,deaths
2020,Seoul,1.5,2
2021,Busan,0.8,0
2022,Daegu,2.1,1
2022,Seoul,1.2,0
"""
    with open(os.path.join(DATA_DIR, "disaster.csv"), "w", encoding="utf-8") as f:
        f.write(demo)
    return pd.read_csv(os.path.join(DATA_DIR, "disaster.csv"))

# ------------------------------------------------------------
# Public loader functions
# ------------------------------------------------------------

def load_weather_data():
    path = os.path.join(DATA_DIR, "weather.csv")
    if not os.path.exists(path):
        _build_weather_csv()
    return pd.read_csv(path, parse_dates=["date"])


def load_disaster_data():
    path = os.path.join(DATA_DIR, "disaster.csv")
    if not os.path.exists(path):
        df = _fetch_disaster_undrr()
        if df is None:
            df = _build_demo_disaster_csv()
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df
