import requests
from app.config import Config


def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": Config.AMADEUS_API_KEY,
        "client_secret": Config.AMADEUS_API_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    return response.json().get("access_token")


def search_hotels_by_city(city):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 1: convert city → city code
    city_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

    city_res = requests.get(
        city_url,
        headers=headers,
        params={"keyword": city, "max": 1}
    ).json()

    if not city_res.get("data"):
        return []

    city_code = city_res["data"][0]["iataCode"]

    # Step 2: fetch hotels
    hotel_url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"

    hotel_res = requests.get(
        hotel_url,
        headers=headers,
        params={"cityCode": city_code}
    ).json()

    return hotel_res.get("data", [])