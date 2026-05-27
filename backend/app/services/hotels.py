import requests

def search_hotels_by_city(city):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"hotel in {city}",
        "format": "json",
        "limit": 10
    }

    headers = {
        "User-Agent": "innsight-app"
    }

    try:
        res = requests.get(url, params=params, headers=headers)

        if res.status_code != 200:
            return []

        data = res.json()

        return [
            {
                "name": item.get("display_name"),
                "lat": item.get("lat"),
                "lon": item.get("lon")
            }
            for item in data
        ]

    except Exception:
        return []