from .helpers import layover, format_time_difference
from typing import List, Dict


class RouteMaster:
    def __init__(
            self,
            criteria,
            flights,
    ):
        self.criteria = criteria
        self.flights = flights
        self.routes = None

    def find_routes(self):
        routes = []
        for flight in self.flights:
            if flight["origin"] == self.criteria.origin:
                if flight["destination"] == self.criteria.destination:
                    routes.append([flight])
                else:
                    next_flights = self._explore(flight["destination"], [flight["origin"]], flight["arrival"])
                    if next_flights:
                        routes.append([flight] + next_flights)

        self.routes = self._post_processing(routes)

    def _explore(self, origin, visited, prev_arrival):
        for flight in self.flights:
            if flight["origin"] == origin:
                if (
                    flight["destination"] == self.criteria.destination
                    and (
                        flight["departure"] > prev_arrival
                        and (1 <= layover(flight["departure"], prev_arrival) <= 6)
                    )
                ):
                    return [flight]
                elif flight["destination"] not in visited:
                    next_flights = self._explore(
                        flight["destination"],
                        visited + [flight["origin"]],
                        flight["arrival"]
                    )
                    if next_flights:
                        return [flight] + next_flights

        return []

    def _post_processing(self, routes) -> List[Dict]:
        final_routes = []
        if routes:
            for route in routes:
                flights_price = sum([f["base_price"] for f in route]) * self.criteria.pax
                bags_price = sum([f["base_price"] for f in route]) * self.criteria.pax
                final_routes.append(
                    {
                        "flights": route,
                        "bags_allowed": min([f["bags_allowed"] for f in route]),
                        "bags_count": self.criteria.bags,
                        "destination": self.criteria.destination,
                        "origin": self.criteria.origin,
                        "total_price": flights_price + bags_price,
                        "travel_time": format_time_difference(route[-1]["arrival"], route[0]["departure"])
                    }
                )

        return sorted(final_routes, key=lambda item: item.get("total_price", 0))
