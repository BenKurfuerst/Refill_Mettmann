import requests
import json

# 1. Daten abrufen von alter API
url = "https://kartevonmorgen.org/api/place?query=refill"
headers = {
    "User-Agent": "ArcGISDataBot/1.0"
}
response = requests.get(url, headers=headers)
data = response.json()

# 2. GeoJSON erstellen
features = []
for entry in data:
    if "lat" in entry and "lng" in entry:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [entry["lng"], entry["lat"]]
            },
            "properties": {
                "title": entry.get("name"),
                "description": entry.get("description"),
                "tags": entry.get("tags")
            }
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# 3. Speichern
with open("refill.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)
