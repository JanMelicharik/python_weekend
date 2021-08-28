import httpx


class Scraper:
    LOCATIONS_API = "https://brn-ybus-pubapi.sa.cz/restapi/consts/locations"
    SEARCH = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"
    CARRIER = "REGIOJET"

    def __init__(self, origin, destination):
        self.locations_ids = self._read_locations_cache() or self._locations()
        self.search_params = {
            "origin": origin,
            "destination": destination,
            "origin_id": self.locations_ids[origin],
            "destination_id": self.locations_ids[destination],
        }

    @classmethod
    def _read_locations_cache(cls):
        pass

    @classmethod
    def _locations(cls):
        locations_ids = {}
        response = httpx.get(cls.LOCATIONS_API)
        response.raise_for_status()
        for country in response.json():
            for city in country.get("cities", []):
                locations_ids[city["name"].lower()] = city["id"]

        return locations_ids

    def _format_results(self, routes: list) -> list:
        formatted_routes = [
            self._format_connection(route)
            for route in routes
            if route["bookable"]
        ]
        return sorted(formatted_routes, key=lambda item: item["price"])

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

    def find_connection(self):
        response = httpx.get(
            Scraper.SEARCH,
            params={
                "fromLocationId": self.search_params["origin_id"],
                "toLocationId": self.search_params["destination_id"],
                "fromLocationType": "CITY",
                "toLocationType": "CITY"
            },
            headers={"X-Currency": "EUR"}
        )
        return self._format_results(response.json().get("routes", []))
