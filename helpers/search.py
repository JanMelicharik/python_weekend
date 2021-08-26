from typing import List, Dict, Optional
from .helpers import get_layover


class RouteMaster:
    def __init__(
            self,
            criteria,
            flights,
    ):
        self.criteria = criteria
        self.flights = flights

    def search(self):
        single = self._single_flight_search()
        layover = self._layover_search()

    def _single_flight_search(self, roundtrip: bool = False) -> List[Optional[Dict]]:
        """Not optimal"""
        connections = []
        for flight in self.flights:
            if (
                flight["origin"] == self.criteria.origin
                and flight["destination"] == self.criteria.destination
                and flight["bags_allowed"] >= self.criteria.bags
            ):
                connections.append(
                    {
                        "flights": [flight]
                    }
                )

        if roundtrip:
            for connection in connections:
                for flight in self.flights:
                    if (
                        flight["origin"] == connection["flights"][0]["destination"]
                        and flight["destination"] == connection["flights"][0]["origin"]
                        and flight["bags_allowed"] >= self.criteria.bags
                        and get_layover(connection["flights"][0], flight) > self.criteria.stay_duration
                    ):
                        connection["flights"].append(flight)
                        connection["total_price"] = sum(
                            [fl["base_price"] for fl in connection["flights"]]
                        ) * self.criteria.pax

        return results

    def _layover_search(self) -> [List[Optional[Dict]]]:
        """To be implemented"""
        return []

    def _create_graph(self):
        """Not finished"""
        edges = []
        for flight in self.flights:
            for another_flight in self.flights:
                layover = get_layover(flight, another_flight)
                if (
                    flight["destination"] == another_flight["origin"]
                    and flight["bags_allowed"] >= self.criteria.bags
                    and another_flight["bags_allowed"] >= self.criteria.bags
                    and 1 >= layover <= 6
                ):
                    edges.append(f"{flight['id']}-{another_flight['id']}")

        return edges
