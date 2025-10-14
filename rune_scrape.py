import requests
import time

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

def build_price_catalog():
    mapping = fetch_mapping()
    latest = fetch_latest_prices()
    
    catalog = []
    for item in mapping:
        item_id = item["id"]
        name = item["name"]
        price_info = latest.get(str(item_id))
        entry = {
            "id": item_id,
            "name": name,
            "metadata": item,
            "price": price_info,
        }
        catalog.append(entry)
    return catalog

if __name__ == "__main__":
    catalog = build_price_catalog()
    import json
    with open("osrs_prices.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)