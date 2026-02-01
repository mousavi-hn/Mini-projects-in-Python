from flask import Flask, request, jsonify, render_template
import googlemaps
import time
import random
import requests

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.nchc.org.tw/api/interpreter",
]

app = Flask(__name__)
gmaps = googlemaps.Client(key='YOUR-KEY')

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafes")
def cafes():
    lat = float(request.args["lat"])
    lng = float(request.args["lng"])
    radius = int(request.args.get("radius", 5000))

    resp = gmaps.places_nearby(location=(lat, lng), radius=radius, type="cafe")
    results = resp.get("results", [])

    # (optional) limit to reduce timeouts for now
    results = results[:20]

    filtered = {}  # place_id -> cafe object (dedupe)

    for cafe in results:
        place_id = cafe.get("place_id")
        if not place_id:
            continue

        cafe_lat = cafe["geometry"]["location"]["lat"]
        cafe_lng = cafe["geometry"]["location"]["lng"]

        base_obj = {
            "place_id": place_id,
            "name": cafe.get("name"),
            "rating": cafe.get("rating"),
            "user_ratings_total": cafe.get("user_ratings_total"),
            "lat": cafe_lat,
            "lng": cafe_lng,
            "vicinity": cafe.get("vicinity"),
        }

        # 1) Google reviews evidence
        details = gmaps.place(place_id=place_id, fields=["reviews"])
        reviews = details.get("result", {}).get("reviews", [])
        analysis = analyze_reviews_for_amenities(reviews)

        wifi = analysis["wifi"]
        power = analysis["power"]
        confidence = analysis["score"]

        # 2) If Google didn't confirm wifi, try OSM (cheaper than calling it always)
        if not wifi:
            lookup = osm_lookup(cafe_lat, cafe_lng)
            if lookup:
                evidence = osm_evidence_from_element(lookup[0])
                wifi = wifi or evidence["wifi"]
                power = power or evidence["power"]

        # 3) Filter rule: keep only wifi cafes
        if wifi:
            base_obj.update({
                "wifi": True,
                "power": bool(power),
                "confidence": confidence,
            })
            filtered[place_id] = base_obj

    return jsonify({"count": len(filtered), "cafes": list(filtered.values())})

def analyze_reviews_for_amenities(reviews):
    keywords = ['wifi', 'internet', 'power', 'outlet', 'plug', 'laptop']
    matches = []

    for r in reviews:
        text = r.get('text', '').lower()
        found = [word for word in keywords if word in text]
        matches.extend(found)

    return {
        "detected": sorted(set(matches)),
        "wifi": any(k in matches for k in ['wifi', 'internet']),
        "power": any(k in matches for k in ['power', 'outlet', 'plug']),
        "score": "High" if len(matches) > 2 else "Medium/Low"
    }

def osm_lookup(lat: float, lng: float, radius_m: int = 50, retries: int = 3):
    query = f"""
    [out:json][timeout:25];
    (
      nwr(around:{radius_m},{lat},{lng})[amenity=cafe];
    );
    out tags center;
    """

    headers = {
        "User-Agent": "CafeWifiCVProject/1.0 (local dev)"
    }

    last_err = None

    for attempt in range(retries):
        url = random.choice(OVERPASS_URLS)
        try:
            # timeout=(connect_timeout, read_timeout)
            r = requests.post(url, data={"data": query}, headers=headers, timeout=(5, 30))
            r.raise_for_status()
            return r.json().get("elements", [])
        except requests.exceptions.RequestException as e:
            last_err = e
            # small backoff
            time.sleep(1.5 * (attempt + 1))

    # If all retries fail, return empty (don’t crash your whole /cafes request)
    print("OSM lookup failed:", repr(last_err))
    return []


def osm_evidence_from_element(el: dict):
    tags = el.get("tags", {})
    internet = tags.get("internet_access")  # wlan / yes / no etc. :contentReference[oaicite:3]{index=3}
    wifi_legacy = tags.get("wifi")          # yes/no (legacy) :contentReference[oaicite:4]{index=4}
    electricity = tags.get("service:electricity")  # yes/no :contentReference[oaicite:5]{index=5}

    wifi = (internet in ("wlan", "yes")) or (wifi_legacy == "yes")  # wlan tag exists :contentReference[oaicite:6]{index=6}
    power = (electricity == "yes")

    return {"wifi": wifi, "power": power, "tags": tags}


if __name__ == '__main__':
    app.run(debug=True)
