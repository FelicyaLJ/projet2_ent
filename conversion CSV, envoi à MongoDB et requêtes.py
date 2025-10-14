import json
import csv
from pymongo import MongoClient


def flatten_json(data, parent_key='', sep='.'):
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

with open(r"C:\Users\Felicya\Desktop\Exploration nouvelles technologies\projet2\osrs_prices.json", mode="r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict):
    data_list = [data]
elif isinstance(data, list):
    data_list = data
else:
    raise ValueError("Input JSON must be an object or a list of objects.")

flat_data = [flatten_json(item) for item in data_list]

all_keys = set()
for item in flat_data:
    all_keys.update(item.keys())
fieldnames = sorted(all_keys)

with open(r"C:\Users\Felicya\Desktop\Exploration nouvelles technologies\projet2\osrs_prices.csv", mode="w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(flat_data)

client = MongoClient("mongodb+srv://projet2:aW8LDLFknVINy1xh@cluster0.h5uygoo.mongodb.net/")
db = client["Projet2"]
collection = db["Rune"]

result = collection.delete_many({})

with open(r"C:\Users\Felicya\Desktop\Exploration nouvelles technologies\projet2\osrs_prices.json", encoding="utf-8") as f:
    data = json.load(f)

collection.insert_many(data)


print("Requête #1")
result = collection.find_one({"name": "3rd age amulet"})
print(result)

print ("Requête #2")
result = collection.find_one({"metadata.value": 50500})
print(result)

print("Requête #3")
result = collection.find({"price.low": {"$gt": 500000}}).limit(4)

for doc in result:
    print(doc)