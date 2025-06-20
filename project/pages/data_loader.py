import os, requests, pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- 1. Country coordinate list (10 대표 국가) ----------
COUNTRY_COORDS = {
    "Seoul, KR":        (37.5665, 126.9780),
    "Washington, US":   (38.9072, -77.0369),
    "Beijing, CN":      (39.9042, 116.4074),
    "New Delhi, IN":    (28.6139, 77.2090),
    "Berlin, DE":       (52.5200, 13.4050),
    "Tokyo, JP":        (35.6895, 139.6917),
    "Paris, FR":        (48.8566, 2.3522),
    "Brasília, BR":     (-15.7939, -47.8828),
    "Ottawa, CA":       (45.4215, -75.6972),
    "Canberra, AU":     (-35.2809, 149.1300),
}
START_DATE = "2023-01-01"; END_DATE = "2023-12-31"

# ---------- Weather fetch ----------
def _fetch_weather(lat, lon):
    url=("https://archive-api.open-meteo.com/v1/archive"
         f"?latitude={lat}&longitude={lon}&start_date={START_DATE}&end_date={END_DATE}"
         "&daily=temperature_2m_mean,precipitation_sum,windspeed_10m_max"
         "&timezone=UTC")
    j = requests.get(url, timeout=30).json()["daily"]
    return j

def _build_weather_csv(country:str):
    lat,lon = COUNTRY_COORDS[country]
    j=_fetch_weather(lat,lon)
    df=pd.DataFrame({
        "date": j["time"],
        "temp": j["temperature_2m_mean"],
        "precip": j["precipitation_sum"],
        "wind": j["windspeed_10m_max"],
        "country": country,
    })
    df.to_csv(os.path.join(DATA_DIR,f"weather_{country.split(',')[0]}.csv"), index=False)
    return df

def load_weather_data(country:str):
    fname=os.path.join(DATA_DIR,f"weather_{country.split(',')[0]}.csv")
    if not os.path.exists(fname):
        return _build_weather_csv(country)
    return pd.read_csv(fname, parse_dates=["date"])

# ---------- Disaster fetch ----------
DISASTER_PATH=os.path.join(DATA_DIR,"disaster.csv")

def _fetch_disaster_global():
    try:
        url="https://garapi.globalgarhub.org/v1/risks/iso/KOR"  # sample call
        _=requests.get(url,timeout=10).json();  # just test connectivity
    except Exception:
        return None
    rows=[]
    for iso,name in [("USA","United States"),("CHN","China"),("IND","India"),("BRA","Brazil"),("DEU","Germany"),("FRA","France"),("JPN","Japan"),("KOR","South Korea"),("CAN","Canada"),("AUS","Australia")]:
        try:
            recs=requests.get(f"https://garapi.globalgarhub.org/v1/risks/iso/{iso}",timeout=20).json()["records"]
            for r in recs:
                rows.append({
                    "year": r["year"],
                    "region": name,
                    "damage_amount_hundred_million_won": r.get("economic_loss_avg",0)/1e8,
                    "deaths": r.get("mortality_avg",0),
                })
        except Exception:
            pass
    pd.DataFrame(rows).to_csv(DISASTER_PATH,index=False)


def _build_demo_disaster():
    demo="""year,region,damage_amount_hundred_million_won,deaths
2021,United States,120,5
2021,China,130,8
2021,India,60,3
2021,Brazil,25,1
2021,Germany,18,0
"""
    with open(DISASTER_PATH,"w",encoding="utf-8") as f: f.write(demo)


def load_disaster_data():
    if not os.path.exists(DISASTER_PATH):
        if _fetch_disaster_global() is None:
            _build_demo_disaster()
    df=pd.read_csv(DISASTER_PATH)
    df.columns=df.columns.str.strip().str.lower()
    return df
