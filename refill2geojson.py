import requests
import csv
import json
from io import StringIO

# 1. CSV abrufen – bbox für Deutschland (damit wir Koordinaten bekommen)
url = "https://api.ofdb.io/export/entries.csv?text=refill&bbox=47.27,5.87,55.06,15.04"
headers = {
    "User-Agent": "ArcGISDataBot/1.0"
}
response = requests.get(url, headers=headers)

# 2. CSV einlesen
csv_text = response.text
csv_file = StringIO(csv_text)
reader = csv.DictReader(csv_file)

# 3. GeoJSON erzeugen
features = []
for row in reader:
    try:
        lat = float(row["lat"])
        lng = float(row["lng"])
    except (ValueError, KeyError):
        continue  # überspringe Zeilen ohne Koordinaten

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat]
        },
        "properties": {
            "title": row.get("title"),
            "description": row.get("description"),
            "tags": row.get("tags"),
            "city": row.get("city"),
            "street": row.get("street")
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# 4. GeoJSON speichern
with open("refill.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)
