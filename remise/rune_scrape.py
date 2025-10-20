import requests
import time
import json
import os

BASE = "https://prices.runescape.wiki/api/v1/osrs"
HEADERS = {
    "User-Agent": "MyOSRSPriceScraper/1.0 (contact: myemail@example.com)"
}

def fetch_mapping():
    url = f"{BASE}/mapping"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def fetch_latest_prices():
    url = f"{BASE}/latest"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get("data", {})

def fetch_timeseries(item_id, timestep="5m"):
    url = f"{BASE}/timeseries"
    params = {
        "id": item_id,
        "timestep": timestep
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()

def calculate_roi(price_info):
    try:
        high = price_info.get("high")
        low = price_info.get("low")
        if high is not None and low and low != 0:
            return (high - low) / low
    except Exception:
        pass
    return None

def build_price_catalog():
    mapping = fetch_mapping()
    latest = fetch_latest_prices()
    
    catalog = []
    for item in mapping:
        item_id = item["id"]
        name = item["name"]
        examine = item.get("examine", "")
        
        price_info = latest.get(str(item_id))

        roi = calculate_roi(price_info) if price_info else None

        entry = {
            "id": item_id,
            "metadata": item,
            "price": price_info,
            "roi": roi,
        }
        catalog.append(entry)
    return catalog

if __name__ == "__main__":
    catalog = build_price_catalog()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "osrs_prices.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
