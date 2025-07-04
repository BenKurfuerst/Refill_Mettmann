import requests
import json

# Schritt 1: Daten abrufen
url = "https://api.ofdb.io/v0/search"
params = {
    "text": "refill",
    "limit": 1000
}

response = requests.get(url, params=params)
data = response.json()

# Schritt 2: GeoJSON erzeugen
features = []
for entry in data.get("visible", []):
    if "lat" in entry and "lng" in entry:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [entry["lng"], entry["lat"]]
            },
            "properties": {
                "title": entry.get("title"),
                "description": entry.get("description"),
                "tags": entry.get("tags"),
                "categories": entry.get("categories")
            }
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Schritt 3: Datei speichern
with open("refill.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)
