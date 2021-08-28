import httpx
import json
from slugify import slugify
from ..redis_service import init_redis
from ..helpers import helpers


class Scraper:
    LOCATIONS_API = "https://brn-ybus-pubapi.sa.cz/restapi/consts/locations"
    SEARCH = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"
    CARRIER = "REGIOJET"
    AUTHOR = "melicharik"

    def __init__(self, origin, destination, dep_date):
        self.redis = init_redis()
        self.locations_ids = self._read_locations_cache() or self._locations()
        self.search_params = {
            "origin": origin,
            "destination": destination,
            "origin_id": self.locations_ids[slugify(origin.lower())],
            "destination_id": self.locations_ids[slugify(destination.lower())],
            "dep_date": dep_date,
        }
        self.day_route_id = self._generate_day_route_id()

    def _locations(self) -> dict:
        locations_ids = {}
        response = httpx.get(self.LOCATIONS_API)
        response.raise_for_status()
        for country in response.json():
            for city in country.get("cities", []):
                city_slug = slugify(city["name"].lower())
                locations_ids[city_slug] = city["id"]

        self._store_data_to_redis("locations", helpers.stringify_data(locations_ids))
        return locations_ids

    def _format_results(self, routes: list) -> list:
        formatted_routes = [self._format_connection(route) for route in routes if route["bookable"]]
        return sorted(formatted_routes, key=lambda item: item["price"])

    def _read_locations_cache(self) -> dict:
        redis_data = self.redis.get("locations")
        if redis_data:
            return helpers.jsonize_data(redis_data)

        return {}

    def _format_connection(self, route):
        return {
            "departure_datetime": route["departureTime"],
            "arrival_datetime": route["arrivalTime"],
            "source": self.search_params["origin"],
            "destination": self.search_params["destination"],
            "price": route["priceFrom"],
            "type": [v.lower() for v in route["vehicleTypes"]],
            "source_id": self.search_params["origin_id"],
            "destination_id": self.search_params["destination_id"],
            "free_seats": route["freeSeatsCount"],
            "carrier": Scraper.CARRIER,
        }

    def _generate_day_route_id(self):
        return (
            f"{self.AUTHOR}:"
            f"{self.search_params['origin']}_"
            f"{self.search_params['destination']}_"
            f"{self.search_params['dep_date']}"
        )

    def _fetch_from_redis(self):
        redis_data = self.redis.get(self.day_route_id)
        if redis_data:
            print("Loaded from redis")
            return helpers.jsonize_data(redis_data)

        return []

    def _find_connection(self):
        response = httpx.get(
            Scraper.SEARCH,
            params={
                "fromLocationId": self.search_params["origin_id"],
                "toLocationId": self.search_params["destination_id"],
                "departureDate": self.search_params["dep_date"] ,
                "fromLocationType": "CITY",
                "toLocationType": "CITY",
            },
            headers={"X-Currency": "EUR"}
        )
        formatted_results = self._format_results(response.json().get("routes", []))
        self._store_data_to_redis(self.day_route_id, formatted_results)

        return formatted_results

    def _store_data_to_redis(self, key, connections):
        self.redis.set(key, helpers.stringify_data(connections))

    def get_results(self):
        connections = self._fetch_from_redis()
        if not connections:
            connections = self._find_connection()

        return connections

